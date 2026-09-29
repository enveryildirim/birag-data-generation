"""Colab + Unsloth eğitim ve üretim yardımcıları — `v0.1.1` ön kaydı EK-2 (2026-09-29).

👤 Kullanıcı kararı: bu makinede model çalışmaz; eğitim ve üretim Colab'da Unsloth ile.
⭐ EK-2: iki kol (`v010u` = `datasets/v0.1.0`, `v011u` = `datasets/v0.1.1`) AYNI Colab
ortamında, AYNI tarifle eğitilir ve üretilir; kayıtlı MLX `e3` koşuları yalnız başvurudur.

⭐⭐ Tek kaynak (K103) — MLX yolunun fonksiyonları ÇAĞRILIR, kopyalanmaz:
  tarif (hiperparametreler)   ← configs/training/{e3-celiskili-k8qo-v022,v011-k8qo}-t{t}.yaml
  veri biçimi + bölme         ← src/train.py: to_mlx_messages · prepare_data (random.Random(7))
  eksenler + tohumlar         ← scripts/analiz/2026-09-23-onkayit-ek1-yaz.py: EKSEN · TOHUM
  istem + çıktı ayrıştırma    ← src/golden_eval.py: prompt_kur · cikti_ayir
  çok turlu akış              ← src/cok_turlu_eval.py: konus
Yeniden kurulan TEK şey: eğitim döngüsü (HF Trainer) ve üretim çağrısı (HF generate).

⛔ torch / transformers / unsloth / peft yalnız fonksiyon İÇİNDE içe aktarılır ⇒ modül
modelsiz makinede içe aktarılır ve sınanır.

MLX ↔ PEFT eşlemesi (mlx_lm 0.31.3 kaynağından okundu):
  LoRA  y + scale·(x·A)·B, scale 20, r 8    ⇒ lora_alpha = scale·r = 160 (PEFT ölçeği alpha/r)
  A ~ U(±1/√in), B = 0                      ⇒ PEFT kaiming_uniform(a=√5) aynı dağılım, B = 0
  AdamW β(0,9, 0,999) ε 1e-8 wd 0,01        ⇒ aynı ⚠️ MLX'te bias_correction=False, torch'ta hep açık
  kırpma yok · sabit LR · ısınma yok         ⇒ max_grad_norm 0 · constant · warmup 0
  kayıp: tokens[offset:] üzerinde ortalama   ⇒ labels[:offset] = -100
  offset = len(şablon(messages[:-1], add_generation_prompt=True))   (mlx_lm ChatDataset)
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import tempfile
import time
from datetime import datetime
from importlib import util as _iu
from pathlib import Path

import yaml

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "src"))
import cok_turlu_eval as _ct  # noqa: E402
import golden_eval as _ge  # noqa: E402
import train as _train  # noqa: E402

SABLON = KOK / "configs/chat_template_train.jinja"
REFERANS = KOK / "configs/colab/sablon-referansi.json"
COK_TURLU = "evals/cok_turlu.jsonl"
KOLLAR = {  # kol → (tarif şablonu, veri, veri SHA256-16)
    "v010u": ("configs/training/e3-celiskili-k8qo-v022-t{t}.yaml", "datasets/v0.0.22/train.jsonl", "6fcb6b1e16290575"),
    "v011u": ("configs/training/v011-k8qo-t{t}.yaml", "datasets/v0.1.1/train.jsonl", "f8fcaa1e96603cb2"),
}
URETIM = {"thinking": False, "max_tokens": 1024, "do_sample": False}      # e3'ün 48 koşusu


def _modul(ad: str, yol: str):
    y = KOK / yol
    sp = _iu.spec_from_file_location(ad, y)
    m = _iu.module_from_spec(sp)
    argv, sys.argv = sys.argv[:], [str(y)]
    sp.loader.exec_module(m)
    sys.argv = argv
    return m


_EK = _modul("_ek1_yaz", "scripts/analiz/2026-09-23-onkayit-ek1-yaz.py")
TOHUM: list[int] = _EK.TOHUM
EKSEN: list[tuple[str, str]] = _EK.EKSEN


def sha16(yol: Path | str) -> str:
    return hashlib.sha256(Path(yol).read_bytes()).hexdigest()[:16]


def metin_sha16(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


# ─────────────────────────── tarif ve veri ───────────────────────────
def tarif(kol: str, t: int) -> dict:
    """Kolun tohum t tarifi — mühürlü MLX yapılandırmasından okunur."""
    sablon, veri, sha = KOLLAR[kol]
    cfg = yaml.safe_load((KOK / sablon.format(t=t)).read_text(encoding="utf-8"))
    assert cfg["dataset"] == veri and cfg["mlx"]["seed"] == t, (kol, t, cfg["dataset"])
    assert sha16(KOK / veri) == sha, f"⛔ {veri} SHA {sha16(KOK / veri)} ≠ {sha}"
    assert cfg["veri"]["chat_template"] == "configs/chat_template_train.jinja"
    x, lp = cfg["mlx"], cfg["mlx"]["lora_parameters"]
    assert x["fine_tune_type"] == "lora" and x["optimizer"] == "adamw" and x["mask_prompt"] is True
    return {"kol": kol, "tohum": t, "veri": veri, "veri_sha256_16": sha,
            "valid_orani": cfg["veri"]["valid_orani"], "bolme_tohumu": cfg["veri"]["seed"],
            "ust_katman": x["num_layers"], "adim": x["iters"], "lr": x["learning_rate"],
            "batch": x["batch_size"], "max_seq": x["max_seq_length"], "kayit_adimi": x["save_every"],
            "eval_adimi": x["steps_per_eval"], "rapor_adimi": x["steps_per_report"],
            "r": lp["rank"], "lora_alpha": lp["scale"] * lp["rank"], "dropout": lp["dropout"],
            "anahtarlar": [k.split(".")[-1] for k in lp["keys"]],
            "weight_decay": 0.01, "betas": (0.9, 0.999), "eps": 1e-8, "max_grad_norm": 0.0}


def veri_hazirla(kol: str, t: int) -> tuple[list[dict], list[dict]]:
    """`train.prepare_data` ile AYNI bölme ve biçim (dosyaya yazar, geri okur)."""
    c = tarif(kol, t)
    with tempfile.TemporaryDirectory() as d:
        nt, nv = _train.prepare_data(KOK / c["veri"], Path(d), c["valid_orani"], c["bolme_tohumu"])
        oku = lambda ad: [json.loads(x)["messages"] for x in (Path(d) / f"{ad}.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
        tr, va = oku("train"), oku("valid")
    assert (len(tr), len(va)) == (nt, nv)
    return tr, va


# ─────────────────────────── şablon ve kodlama ───────────────────────────
def metin_tokenizer(tokenizer):
    """Unsloth çok kipli modellerde işlemci (processor) döndürebilir; metin tokenizer'ı al."""
    return getattr(tokenizer, "tokenizer", tokenizer)


def sablon_kur(tokenizer):
    tok = metin_tokenizer(tokenizer)
    tok.chat_template = SABLON.read_text(encoding="utf-8")
    return tok


def kodla(tok, msgs: list[dict], max_seq: int) -> dict:
    """mlx_lm ChatDataset + default_loss ile aynı hedef: tokens[offset:]."""
    tam_m = tok.apply_chat_template(msgs, tokenize=False)
    on_m = tok.apply_chat_template(msgs[:-1], tokenize=False,
                                   add_generation_prompt=msgs[-1]["role"] == "assistant")
    tam = tok(tam_m, add_special_tokens=False)["input_ids"]
    on = tok(on_m, add_special_tokens=False)["input_ids"]
    if tam[:len(on)] != on:
        raise ValueError("⛔ önek hizası bozuk — maske hedefin içine kayar")
    if len(tam) > max_seq:
        raise ValueError(f"⛔ {len(tam)} jeton > max_seq {max_seq} — sessiz kırpma kıyası bozar (ön kayıt adım 2)")
    return {"input_ids": tam, "labels": [-100] * len(on) + tam[len(on):],
            "attention_mask": [1] * len(tam), "offset": len(on), "n": len(tam)}


def uzunluk_denetle(tok, kol: str, max_seq: int = 2048) -> dict:
    """Ön kaydın adım 2'si: kolun BÜTÜN kayıtları (bölmeden bağımsız) ≤ max_seq."""
    c = tarif(kol, TOHUM[0])
    kayit = [json.loads(x) for x in (KOK / c["veri"]).read_text(encoding="utf-8").splitlines() if x.strip()]
    n = [kodla(tok, _train.to_mlx_messages(r)["messages"], max_seq)["n"] for r in kayit]
    return {"kol": kol, "kayit": len(n), "en_uzun": max(n), "ortanca": sorted(n)[len(n) // 2], "max_seq": max_seq}


def sablon_referansi_uret(tok) -> dict:
    """Referans dizgeleri: eğitim (tam + önek) ve üretim istemi. Bu makinede tokenizer'sız
    (`render_jinja_template`) üretilir, Colab'da gerçek tokenizer ile yeniden üretilip karşılaştırılır."""
    out = {}
    for kol in KOLLAR:
        c = tarif(kol, TOHUM[0])
        kayit = [json.loads(x) for x in (KOK / c["veri"]).read_text(encoding="utf-8").splitlines() if x.strip()]
        cok = [r for r in kayit if sum(m["role"] == "assistant" for m in r["messages"]) > 1][:3]
        rep = [r for r in kayit if r.get("replay")][:2]
        for r in kayit[:3] + cok + rep:
            msgs = _train.to_mlx_messages(r)["messages"]
            out[f"{kol}:{r['id']}:tam"] = metin_sha16(tok.apply_chat_template(msgs, tokenize=False))
            out[f"{kol}:{r['id']}:onek"] = metin_sha16(tok.apply_chat_template(
                msgs[:-1], tokenize=False, add_generation_prompt=True))
    for kisa, yol in EKSEN + [("cokturlu", COK_TURLU)]:
        o = json.loads((KOK / yol).read_text(encoding="utf-8").splitlines()[0])
        if kisa == "cokturlu":
            o = {"id": o["id"], "messages": o["messages"] + [
                {"role": "user", "content": o["kullanici_turlari"][0]},
                {"role": "assistant", "content": "SABİT SINAMA CEVABI."},
                {"role": "user", "content": o["kullanici_turlari"][1]}]}
        out[f"istem:{kisa}:{o['id']}"] = metin_sha16(_ge.prompt_kur(o, tok, URETIM["thinking"]))
    return out


def sablon_referansi_denetle(tokenizer) -> int:
    ref = json.loads(REFERANS.read_text(encoding="utf-8"))
    tok = sablon_kur(tokenizer)            # denetlenen şey her zaman eğitimde kullanılacak yamalı şablon
    if tok.bos_token != ref["bos_token"]:
        raise SystemExit(f"⛔ bos_token {tok.bos_token!r} ≠ referans {ref['bos_token']!r}")
    simdi = sablon_referansi_uret(tok)
    kotu = [k for k, v in ref["dizgeler"].items() if simdi.get(k) != v]
    if kotu or set(simdi) != set(ref["dizgeler"]):
        raise SystemExit(f"⛔ şablon çıktısı referansla uyuşmuyor ({len(kotu)}/{len(ref['dizgeler'])}): {kotu[:4]}")
    return len(simdi)


# ─────────────────────────── LoRA hedefleri ───────────────────────────
_KATMAN = re.compile(r"(?:^|\.)layers\.(\d+)\.self_attn\.(q_proj|o_proj|k_proj|v_proj)$")


def lora_hedefleri(model, ust: int, anahtarlar: list[str]) -> tuple[list[str], int]:
    """Dil modelinin ÜSTTEN `ust` katmanındaki `anahtarlar` modüllerinin tam adları ve dil
    katmanı sayısı (mlx `num_layers` üstten N katman demektir). Görü/ses kuleleri hariç."""
    dil = {}
    for ad, mod in model.named_modules():
        m = _KATMAN.search(ad)
        if m and not re.search(r"vision|audio", ad):
            dil.setdefault(int(m.group(1)), {})[m.group(2)] = (ad, mod)
    katmanlar = sorted(dil)
    assert katmanlar == list(range(len(katmanlar))), "⛔ dil katmanları ardışık değil"
    ad_listesi = [dil[k][a][0] for k in katmanlar[-ust:] for a in anahtarlar]
    return ad_listesi, len(katmanlar)


def lora_parametre_beklenen(model, hedefler: list[str], r: int) -> int:
    mods = dict(model.named_modules())
    return sum(r * (mods[a].in_features + mods[a].out_features) for a in hedefler)


def lora_denetle(model, hedefler: list[str], beklenen: int) -> dict:
    """PEFT sonrası: LoRA taşıyan modüller TAM OLARAK hedefler mi, eğitilebilir parametre beklenen mi."""
    lora = set()
    for ad, mod in model.named_modules():
        if hasattr(mod, "lora_A") and len(getattr(mod, "lora_A", {})):
            lora.add(re.sub(r"^(base_model\.model\.)+", "", ad))
    hedef = {re.sub(r"^(base_model\.model\.)+", "", a) for a in hedefler}
    if lora != hedef:
        raise SystemExit(f"⛔ LoRA hedefleri uyuşmuyor: fazla {sorted(lora - hedef)[:3]} · eksik {sorted(hedef - lora)[:3]}")
    egit = sum(p.numel() for p in model.parameters() if p.requires_grad)
    if egit != beklenen:
        raise SystemExit(f"⛔ eğitilebilir parametre {egit} ≠ beklenen {beklenen}")
    return {"lora_modul": len(lora), "egitilebilir_parametre": egit}


# ─────────────────────────── üretim ───────────────────────────
def uret_yuklu_hf(model, tokenizer, ogeler: list[dict], max_tokens: int, thinking: bool) -> list[dict]:
    """`golden_eval.uret_yuklu`'nun HF karşılığı — AYNI dönüş şeması, AYNI istem ve ayrıştırma.
    Açgözlü (sıcaklık 0). Durma belirteçleri modelin `generation_config.eos_token_id`'si."""
    import torch
    tok = metin_tokenizer(tokenizer)
    eos = model.generation_config.eos_token_id
    eos = set(eos if isinstance(eos, (list, tuple)) else [eos])
    out = []
    for oge in ogeler:
        istem = _ge.prompt_kur(oge, tok, thinking)
        ids = tok(istem, add_special_tokens=False)["input_ids"]
        assert ids[0] == tok.bos_token_id and ids[1] != tok.bos_token_id, "⛔ bos yok ya da çift"
        x = torch.tensor([ids], device=model.device)
        t1 = time.time()
        with torch.no_grad():
            y = model.generate(input_ids=x, attention_mask=torch.ones_like(x), max_new_tokens=max_tokens,
                               do_sample=False, eos_token_id=sorted(eos), pad_token_id=tok.pad_token_id or sorted(eos)[0])
        yeni = y[0, len(ids):].tolist()
        durdu = bool(yeni) and yeni[-1] in eos
        while yeni and yeni[-1] in eos:
            yeni.pop()
        ham = tok.decode(yeni, skip_special_tokens=False)
        dus, cevap, kapandi = _ge.cikti_ayir(ham)
        out.append({"id": oge["id"], "ham": ham, "thinking": dus, "cevap": cevap, "thinking_kapandi": kapandi,
                    "sure_sn": round(time.time() - t1, 1), "uretim_token": len(yeni) + int(durdu),
                    "kesildi": not durdu})
    return out


def _yaz(d: Path, satirlar: list[dict], ham: list[dict], kosu: dict, ortam: dict) -> None:
    d.mkdir(parents=True, exist_ok=False)
    (d / "sonuclar.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in satirlar), encoding="utf-8")
    (d / "ham.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in ham), encoding="utf-8")
    (d / "kosu.json").write_text(json.dumps(kosu, ensure_ascii=False, indent=1), encoding="utf-8")
    (d / "ortam.json").write_text(json.dumps(ortam, ensure_ascii=False, indent=1), encoding="utf-8")


def bitmis_mi(kok: Path, kol: str, t: int, kisa: str, n: int) -> Path | None:
    for d in sorted(kok.glob(f"*-{kol}-t{t}-{kisa}")):
        s = d / "sonuclar.jsonl"
        if s.exists() and sum(1 for x in s.read_text(encoding="utf-8").splitlines() if x.strip()) == n:
            return d
    return None


def eksen_kos(model, tok, kol: str, t: int, kisa: str, set_yol: str, cikti: Path, ortam: dict, adapter: str) -> Path:
    ogeler = [json.loads(x) for x in (KOK / set_yol).read_text(encoding="utf-8").splitlines() if x.strip()]
    kok = cikti / "eksen-kosu"
    if (d := bitmis_mi(kok, kol, t, kisa, len(ogeler))):
        return d
    t0 = time.time()
    ham = uret_yuklu_hf(model, tok, ogeler, URETIM["max_tokens"], URETIM["thinking"])
    d = kok / f"{datetime.now():%Y%m%d-%H%M%S}-{kol}-t{t}-{kisa}"
    kosu = {"etiket": d.name.split("-", 2)[2], "set": set_yol, "set_sha256_16": sha16(KOK / set_yol),
            "adapter": adapter, "model": ortam["model_id"], "thinking": URETIM["thinking"],
            "max_tokens": URETIM["max_tokens"], "oge": len(ogeler), "uretim_sn": round(time.time() - t0),
            "tarih": datetime.now().isoformat(timespec="seconds")}
    _yaz(d, ham, ham, kosu, ortam)          # sonuclar.jsonl burada puanlanmamış; puanlama bu makinede
    return d


def cok_turlu_kos(model, tok, kol: str, t: int, cikti: Path, ortam: dict, adapter: str) -> Path:
    ogeler = [json.loads(x) for x in (KOK / COK_TURLU).read_text(encoding="utf-8").splitlines() if x.strip()]
    kok = cikti / "cok-turlu-kosu"
    if (d := bitmis_mi(kok, kol, t, "cokturlu", 4 * len(ogeler))):
        return d
    t0 = time.time()
    turlar = _ct.kos(ogeler, model, tok, URETIM["max_tokens"], URETIM["thinking"], uret_yuklu_hf)
    d = kok / f"{datetime.now():%Y%m%d-%H%M%S}-{kol}-t{t}-cokturlu"
    kosu = {"etiket": f"{kol}-t{t}-cokturlu", "set": COK_TURLU, "set_sha256_16": sha16(KOK / COK_TURLU),
            "adapter": adapter, "model": ortam["model_id"], "thinking": URETIM["thinking"],
            "max_tokens": URETIM["max_tokens"], "konusma": len(ogeler), "tur": len(turlar),
            "uretim_sn": round(time.time() - t0), "tarih": datetime.now().isoformat(timespec="seconds")}
    _yaz(d, turlar, turlar, kosu, ortam)
    return d


# ─────────────────────────── ortam ───────────────────────────
KUTUPHANE = ("torch", "transformers", "peft", "trl", "unsloth", "unsloth_zoo", "accelerate", "datasets", "bitsandbytes")


def ortam(model_id: str, revizyon: str | None, lora_yolu: str, git_rev: str) -> dict:
    import importlib.metadata as md
    import torch
    s = {}
    for k in KUTUPHANE:
        try:
            s[k] = md.version(k)
        except md.PackageNotFoundError:
            s[k] = None
    return {"model_id": model_id, "model_revizyon": revizyon, "lora_yolu": lora_yolu, "git_rev": git_rev,
            "sablon_sha256_16": sha16(SABLON), "surumler": s, "uretim": URETIM,
            "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            "cuda": torch.version.cuda, "python": sys.version.split()[0]}


SABIT_ALANLAR = ("model_id", "model_revizyon", "lora_yolu", "sablon_sha256_16", "surumler", "uretim")


def ortam_denetle(o: dict, referans: Path) -> str:
    """İlk çağrıda referansı yazar; sonrakilerde SABİT alanlar aynı olmak ZORUNDA (GPU kaydedilir, zorunlu değil)."""
    if not referans.exists():
        referans.parent.mkdir(parents=True, exist_ok=True)
        referans.write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding="utf-8")
        return "referans yazıldı"
    r = json.loads(referans.read_text(encoding="utf-8"))
    fark = {k: (r.get(k), o.get(k)) for k in SABIT_ALANLAR if r.get(k) != o.get(k)}
    if fark:
        raise SystemExit(f"⛔ ortam referanstan farklı — iki kol aynı ortamda olmalı (EK-2): {fark}")
    return "referansla aynı" + ("" if r.get("gpu") == o.get("gpu") else f" ⚠️ GPU farklı: {r.get('gpu')} → {o.get('gpu')}")


# ─────────────────────────── model yükleme, LoRA, eğitim ───────────────────────────
def unsloth_yukle(model_id: str, revizyon: str | None):
    """Eğitim/üretim için taban model yükleyici (Colab). bf16, 4-bit YOK (K7 · e3 bf16)."""
    def yukle(max_seq: int):
        from unsloth import FastModel  # noqa: F401  (unsloth transformers'tan ÖNCE içe aktarılmalı)
        import torch
        return FastModel.from_pretrained(model_id, revision=revizyon, max_seq_length=max_seq,
                                         dtype=torch.bfloat16, load_in_4bit=False, full_finetuning=False)
    return yukle


def lora_uygula(model, c: dict, hedef: list[str], t: int, yol: str):
    """`yol` iki koldan biri için değil, 16 koşunun HEPSİ için aynı olmalı (ortam referansı denetler)."""
    if yol == "unsloth":
        from unsloth import FastModel
        return FastModel.get_peft_model(model, r=c["r"], lora_alpha=c["lora_alpha"], lora_dropout=c["dropout"],
                                        target_modules=hedef, bias="none",
                                        use_gradient_checkpointing="unsloth", random_state=t)
    if yol == "peft":
        import torch
        from peft import LoraConfig, get_peft_model
        torch.manual_seed(t)
        return get_peft_model(model, LoraConfig(r=c["r"], lora_alpha=c["lora_alpha"], lora_dropout=c["dropout"],
                                                target_modules=hedef, bias="none", task_type="CAUSAL_LM"))
    raise ValueError(yol)


def _topla(pad_id: int):
    def f(b):
        import torch
        n = max(len(x["input_ids"]) for x in b)
        return {k: torch.tensor([x[k] + [p] * (n - len(x[k])) for x in b])
                for k, p in (("input_ids", pad_id), ("labels", -100), ("attention_mask", 0))}
    return f


def egit(kol: str, t: int, yukle, cikti: Path, lora_yolu: str, ortam_: dict, adim: int | None = None) -> dict:
    """Bir (kol, tohum) eğitimi. Adapter varsa ATLAR; yarıda kalmışsa son kontrol noktasından sürer.
    `adim` yalnız sınama içindir — gerçek koşuda tarifin adımı (2538) kullanılır."""
    import torch
    import transformers
    c = tarif(kol, t)
    kok = cikti / "runs" / f"{kol}-t{t}"
    adapter = kok / "adapter"
    if (adapter / "adapter_config.json").exists():
        return {"kol": kol, "tohum": t, "atlandi": True, "adapter": str(adapter)}
    transformers.set_seed(t)
    model, tokenizer = yukle(c["max_seq"])
    sablon_referansi_denetle(tokenizer)    # her eğitim kendi tokenizer'ını denetler (K44)
    tok = sablon_kur(tokenizer)
    hedef, n_katman = lora_hedefleri(model, c["ust_katman"], c["anahtarlar"])
    bek = lora_parametre_beklenen(model, hedef, c["r"])
    model = lora_uygula(model, c, hedef, t, lora_yolu)
    ld = lora_denetle(model, hedef, bek)
    tr, va = veri_hazirla(kol, t)
    from datasets import Dataset
    alan = ("input_ids", "labels", "attention_mask")
    kd = lambda L: Dataset.from_list([{k: v for k, v in kodla(tok, m, c["max_seq"]).items() if k in alan} for m in L])
    dtr, dva = kd(tr), kd(va)
    args = transformers.TrainingArguments(
        output_dir=str(kok / "ckpt"), per_device_train_batch_size=c["batch"], per_device_eval_batch_size=1,
        gradient_accumulation_steps=1, max_steps=adim or c["adim"], learning_rate=c["lr"],
        lr_scheduler_type="constant", warmup_steps=0, optim="adamw_torch", weight_decay=c["weight_decay"],
        adam_beta1=c["betas"][0], adam_beta2=c["betas"][1], adam_epsilon=c["eps"], max_grad_norm=c["max_grad_norm"],
        bf16=torch.cuda.is_available(), logging_steps=c["rapor_adimi"], eval_strategy="steps",
        eval_steps=c["eval_adimi"], save_strategy="steps", save_steps=c["kayit_adimi"],
        seed=t, data_seed=t, report_to="none", remove_unused_columns=False)
    pad = tok.pad_token_id if tok.pad_token_id is not None else 0
    tr_ = transformers.Trainer(model=model, args=args, train_dataset=dtr, eval_dataset=dva, data_collator=_topla(pad))
    surdu = any((kok / "ckpt").glob("checkpoint-*"))
    t0 = time.time()
    tr_.train(resume_from_checkpoint=True if surdu else None)
    model.save_pretrained(str(adapter))
    kayit = {"kol": kol, "tohum": t, "tarif": c, "lora": ld, "dil_katmani": n_katman, "hedefler": hedef,
             "egitim_kayit": len(dtr), "dogrulama_kayit": len(dva), "adim": args.max_steps,
             "surdu": surdu, "sure_dk": round((time.time() - t0) / 60, 1), "ortam": ortam_,
             "log": tr_.state.log_history, "tarih": datetime.now().isoformat(timespec="seconds")}
    (kok / "egitim.json").write_text(json.dumps(kayit, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    del tr_, model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return kayit


def adapter_yukle(yukle, adapter: Path, max_seq: int):
    """Üretim için: taban + adapter. Kalıp olarak iki kolda da AYNI."""
    from peft import PeftModel
    model, tokenizer = yukle(max_seq)
    sablon_referansi_denetle(tokenizer)
    tok = sablon_kur(tokenizer)
    model = PeftModel.from_pretrained(model, str(adapter))
    model.eval()
    return model, tok


# ─────────────────────────── mühür ───────────────────────────
EK2 = KOK / "configs/deney/2026-09-29-v011-on-kayit-ek2.json"


def muhur_denetle() -> int:
    """Colab'da klondan hemen sonra: ana ön kayıt, EK-1 ve EK-2'nin mühürlediği her dosya
    bugünküyle aynı mı. Değilse DUR — mühürlü olmayan kodla koşulan ölçüm ön kayda ait değildir."""
    kayitlar = [KOK / "configs/deney/2026-09-29-v011-on-kayit.json",
                KOK / "configs/deney/2026-09-29-v011-on-kayit-ek1.json", EK2]
    kotu, n = [], 0
    for y in kayitlar:
        for d, s in json.loads(y.read_text(encoding="utf-8"))["muhurlu_dosyalar"].items():
            n += 1
            if not (KOK / d).exists() or sha16(KOK / d) != s:
                kotu.append(d)
    if kotu:
        raise SystemExit(f"⛔ mühür bozuk ({len(kotu)}): {kotu[:5]}")
    return n
