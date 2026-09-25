"""Uçtan uca eval — baseline vs LoRA, süre ve maliyet ölçümü. Bkz. plan.md §7, §13 Faz 2.

Faz 2'de KALİTE HEDEFİ YOK: amaç borunun uçtan uca aktığını görmek ve
maliyeti ölçmek ki Faz 4 döngüsünün bütçesi bilinsin.

Ölçülenler:
  1. Üretim — adaptersiz (baseline, §2 ilke 3) ve adapter'lı, aynı tutulan tohumlar
  2. thinking gerçekten üretiliyor mu (<|channel>thought) — K1/K44'ün çıkarım tarafı
  3. Gecikme: prompt/üretim token sayısı, tok/sn, kayıt başına duvar saati
  4. checks.py (bedava) + judge (agy:gemini, ücretli/yavaş) skorları
  5. Maliyet: kayıt başına saniye × Faz 4 ölçeğine ekstrapolasyon

Eval kümesi = eğitimde GÖRÜLMEYEN doğrulama dilimi (aynı config seed'i ile yeniden
türetilir). Golden set Faz 3'e ait (uzman gerekir — K27); bu bir duman testidir,
cetvel değil.

Kullanım: uv run python src/eval.py runs/<run-dizini> [--max-tokens 512]
"""
from __future__ import annotations
import json
import random
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import yaml

import dejenerasyon

sys.path.insert(0, str(Path(__file__).parent))
from checks import run_checks  # noqa: E402

ROOT = Path(__file__).parent.parent
THINK_ON = "<|think|>\n"
_THOUGHT_OPEN = "<|channel>"
_THOUGHT = re.compile(r"<\|channel>\s*thought\s*(.*?)<channel\|>", re.S)


def eval_seti(cfg: dict) -> list[dict]:
    """train.py'deki bölmeyi birebir yeniden üretir — aynı seed, aynı sıra."""
    kayitlar = [json.loads(l) for l in open(ROOT / cfg["dataset"]) if l.strip()]
    random.Random(cfg["veri"]["seed"]).shuffle(kayitlar)
    n_valid = max(1, round(len(kayitlar) * cfg["veri"]["valid_orani"]))
    return kayitlar[:n_valid]


def build_prompt(rec: dict, tokenizer) -> str:
    """Kaydın asistan turu atılır; thinking anahtarı system'e önekle verilir (K44)."""
    msgs = []
    for m in rec["messages"]:
        if m["role"] == "assistant":
            continue
        icerik = m["content"]
        if m["role"] == "system" and rec.get("has_thinking"):
            icerik = THINK_ON + icerik
        msgs.append({"role": m["role"], "content": icerik})
    return tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)


def split_output(text: str) -> tuple[str, str, bool]:
    """Ham çıktıyı (thinking, completion, thinking_kapandi) olarak ayırır.

    DİKKAT (2026-09-12 eval bulgusu): "kapanış etiketi yok" ile "thinking yok" AYNI ŞEY DEĞİL.
    İlk koşuda max_tokens thinking'in ortasında bittiği için kapanışsız kalan çıktılar
    "thinking üretilmedi" diye raporlandı — ölçüm aracının kendi hatasıydı.
    Bu yüzden açılış ve kapanış ayrı ayrı döndürülür.
    """
    m = _THOUGHT.search(text)
    if m:
        return m.group(1).strip(), text[m.end():].strip(), True
    if _THOUGHT_OPEN in text:  # açıldı ama kapanmadı -> completion'a hiç gelinmemiş
        govde = text.split(_THOUGHT_OPEN, 1)[1]
        return govde.removeprefix("thought").strip(), "", False
    return "", text.strip(), False


def uret(model_dir: Path, adapter_path: Path | None, kayitlar: list[dict],
         max_tokens: int) -> tuple[list[dict], float]:
    """Tek model yüklemesiyle tüm tohumları üretir; her kayıt için gecikme toplar."""
    from mlx_lm import load, stream_generate
    from mlx_lm.sample_utils import make_sampler

    t0 = time.time()
    model, tokenizer = load(str(model_dir),
                            adapter_path=str(adapter_path) if adapter_path else None)
    yukleme_sn = time.time() - t0
    sampler = make_sampler(temp=0.0)  # deterministik — iki varyant karşılaştırılabilsin

    ciktilar = []
    for rec in kayitlar:
        prompt = build_prompt(rec, tokenizer)
        t1 = time.time()
        parca = son = None
        metin = []
        for parca in stream_generate(model, tokenizer, prompt,
                                     max_tokens=max_tokens, sampler=sampler):
            metin.append(parca.text)
            son = parca
        sure = time.time() - t1
        ham = "".join(metin)
        thinking, completion, kapandi = split_output(ham)
        ciktilar.append({
            "id": rec["id"], "senaryo": rec.get("scenario"),
            "ham": ham, "thinking": thinking, "completion": completion,
            "thinking_var": bool(thinking), "thinking_kapandi": kapandi,
            "thinking_token_tahmini": len(thinking.split()),
            "completion_bos": not completion,
            # Dejenerasyon kapısı (T82) — ⛔ ELEME değil SAYIM: plan «boş cevap
            # dağıtım anlamında güvenlik başarısızlığıdır» diyor, kayıt düşmez.
            "dejenerasyon": dejenerasyon.denetle(thinking, completion, kapandi),
            "prompt_token": son.prompt_tokens, "uretim_token": son.generation_tokens,
            "prompt_tps": round(son.prompt_tps, 1),
            "uretim_tps": round(son.generation_tps, 1),
            "sure_sn": round(sure, 2),
            "tepe_bellek_gb": round(son.peak_memory, 2),
            "kesildi": son.finish_reason != "stop",
        })
        print(f"  {rec['id'][:12]}  {sure:5.1f}sn  {son.generation_tokens:4d} tok  "
              f"{son.generation_tps:5.1f} tok/sn  "
              f"thinking={'✓' if thinking else '✗'}{'' if kapandi else '(kapanmadı)'}  "
              f"cevap={'✗BOŞ' if not completion else str(len(completion.split())) + ' kelime'}")
    del model
    return ciktilar, round(yukleme_sn, 1)


def judged(kayit: dict, cikti: dict) -> tuple[dict, float]:
    """Üretilen cevabı judge'a verir (K45 — agy:gemini). Süreyi de döndürür."""
    import filter as f
    sahte = {"messages": [
        {"role": m["role"], "content": m["content"]}
        for m in kayit["messages"] if m["role"] != "assistant"
    ] + [{"role": "assistant", "content": cikti["completion"],
          "thinking": cikti["thinking"]}]}
    t0 = time.time()
    jr = f.judge_record(sahte)
    return jr.model_dump(), round(time.time() - t0, 1)


def checks_icin(kayit: dict, cikti: dict) -> dict:
    """checks.py TrainRecord şeması bekliyor — üretilen cevabı kaydın kopyasına koyar."""
    kopya = json.loads(json.dumps(kayit))
    for m in reversed(kopya["messages"]):
        if m["role"] == "assistant":
            m["content"] = cikti["completion"]
            m["thinking"] = cikti["thinking"] or None
            break
    kopya.pop("judge", None)
    return run_checks(kopya)


def main(run_dir_s: str, max_tokens: int = 512):
    run_dir = Path(run_dir_s)
    cfg = yaml.safe_load((run_dir / "config.yaml").read_text())
    model_dir = ROOT / "models" / (cfg["model"].split("/")[-1] + "-train")
    adapter = run_dir / "adapters"
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = run_dir / "eval" / f"{ts}-mt{max_tokens}"
    out_dir.mkdir(parents=True, exist_ok=True)

    kayitlar = eval_seti(cfg)
    print(f"eval kümesi: {len(kayitlar)} kayıt (eğitimde görülmedi) · model: {model_dir.name}")

    varyantlar = {}
    for ad, ap in (("baseline", None), ("lora", adapter)):
        print(f"\n[{ad}] üretim:")
        ciktilar, yukleme = uret(model_dir, ap, kayitlar, max_tokens)
        varyantlar[ad] = {"ciktilar": ciktilar, "model_yukleme_sn": yukleme}

    print("\njudge (agy:gemini-3.8-flash-high):")
    for ad, v in varyantlar.items():
        for kayit, cikti in zip(kayitlar, v["ciktilar"]):
            cikti["_checks"] = checks_icin(kayit, cikti)
            if cikti["completion_bos"]:
                cikti["judge"] = None
                cikti["judge_hata"] = "completion boş (thinking kesildi) — judge atlandı"
                print(f"  [{ad}] {cikti['id'][:12]}  ATLANDI: completion boş")
                continue
            try:
                cikti["judge"], cikti["judge_sn"] = judged(kayit, cikti)
                print(f"  [{ad}] {cikti['id'][:12]}  {cikti['judge_sn']:5.1f}sn")
            except Exception as e:  # judge hatası eval'i düşürmemeli, kayda geçsin
                cikti["judge"] = None
                cikti["judge_hata"] = f"{type(e).__name__}: {e}"[:300]
                print(f"  [{ad}] {cikti['id'][:12]}  HATA: {cikti['judge_hata'][:80]}")

    with open(out_dir / "generations.jsonl", "w") as f:
        for ad, v in varyantlar.items():
            for c in v["ciktilar"]:
                f.write(json.dumps({"varyant": ad, **c}, ensure_ascii=False) + "\n")

    DIMS = ["duygusal_tepki", "yorumlama", "kesif", "mi_uyumu",
            "grounding", "kisalik_dogallik", "dil_butunlugu"]
    ozet = {"run": run_dir.name, "tarih": ts,
            "n_eval": len(kayitlar), "max_tokens": max_tokens,
            "judge_model": __import__("filter").JUDGE_MODEL, "varyantlar": {}}
    for ad, v in varyantlar.items():
        cs = v["ciktilar"]
        ok = [c for c in cs if c.get("judge")]
        ozet["varyantlar"][ad] = {
            "model_yukleme_sn": v["model_yukleme_sn"],
            "thinking_uretilen": sum(c["thinking_var"] for c in cs),
            "thinking_kapanan": sum(c["thinking_kapandi"] for c in cs),
            "completion_bos": sum(c["completion_bos"] for c in cs),
            # T82 — dört bayrak ayrı ayrı sayılır; tek bir «bozuk» sayısı üç
            # farklı kusuru (üretim yok / cevap yok / tekrar) gizlerdi.
            "dejenere": sum(c["dejenerasyon"]["dejenere"] for c in cs),
            "dejenere_uretim_yok": sum(c["dejenerasyon"]["uretim_yok"] for c in cs),
            "dejenere_bos_cevap": sum(c["dejenerasyon"]["bos_cevap"] for c in cs),
            "dejenere_tekrar": sum(c["dejenerasyon"]["tekrar"] for c in cs),
            "dejenere_butce_tukendi": sum(c["dejenerasyon"]["butce_tukendi"] for c in cs),
            "kesilen": sum(c["kesildi"] for c in cs),
            "uretim_sn_toplam": round(sum(c["sure_sn"] for c in cs), 1),
            "uretim_sn_ortalama": round(sum(c["sure_sn"] for c in cs) / len(cs), 1),
            "uretim_tps_ortalama": round(sum(c["uretim_tps"] for c in cs) / len(cs), 1),
            "uretim_token_ortalama": round(sum(c["uretim_token"] for c in cs) / len(cs)),
            "tepe_bellek_gb": max(c["tepe_bellek_gb"] for c in cs),
            "checks_gecen": sum(c["_checks"]["passed"] for c in cs),
            "judge_sn_toplam": round(sum(c.get("judge_sn", 0) for c in cs), 1),
            "judge_basarili": len(ok),
            "judge_ortalama": {d: round(sum(c["judge"][d] for c in ok) / len(ok), 2)
                               for d in DIMS} if ok else None,
            "klinik_guvenlik_ihlali": sum(c["judge"]["klinik_guvenlik_ihlali"] for c in ok),
            "rol_siniri_ihlali": sum(c["judge"]["rol_siniri_ihlali"] for c in ok),
            "tuzak_ihlali_toplam": sum(len(c["judge"]["tuzak_ihlali"]) for c in ok),
        }
    (out_dir / "metrics.json").write_text(json.dumps(ozet, ensure_ascii=False, indent=2))
    print("\n" + json.dumps(ozet["varyantlar"], ensure_ascii=False, indent=2))
    print(f"\nyazıldı: {out_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("kullanım: uv run python src/eval.py runs/<run-dizini> [--max-tokens N]")
        sys.exit(1)
    mt = int(sys.argv[sys.argv.index("--max-tokens") + 1]) if "--max-tokens" in sys.argv else 512
    main(sys.argv[1], mt)
