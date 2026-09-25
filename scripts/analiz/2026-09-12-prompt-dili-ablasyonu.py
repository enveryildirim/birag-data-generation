"""Prompt dili ablasyonu — system prompt ve thinking İngilizce olmalı mı? Bkz. Kural 7, K46.

Kullanıcı önerisi (Oturum 16): *"system prompt ve thinking İngilizce olabilir, model
komutları iyi anlar; içine 'Türkçe cevap ver' yazarız."* Argüman yerine ölçüyoruz (K43/K45 deseni).

Üç varyant, BİREBİR AYNI 12 tohum, aynı model (adapter YOK — saf prompt etkisi), temp=0:
  A `tr_sys`        — mevcut Türkçe system prompt
  B `en_sys`        — aynı promptun İngilizcesi + "Always respond in Turkish"
  C `tr_sys_dusun`  — Türkçe prompt + AÇIK "iç muhakemeni de Türkçe kur" talimatı

Ölçülenler: thinking dili · thinking/completion token · gecikme · checks.py · judge rubriği.
C'nin amacı ayrı: thinking dili prompt'la çevrilebiliyorsa, veriyle savaşmaya gerek yok.

Kullanım: uv run python scripts/analiz/2026-09-12-prompt-dili-ablasyonu.py [--n 12]
"""
from __future__ import annotations
import json
import random
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts" / "analiz"))

from checks import run_checks  # noqa: E402
import filter as judge_mod  # noqa: E402

MODEL_DIR = ROOT / "models" / "gemma-4-E4B-it-bf16-train"
HAM = ROOT / "reports" / "analiz" / "prompt-dili-ablasyonu"
OUT = ROOT / "reports" / "analiz" / "2026-09-12-prompt-dili-ablasyonu.md"

SYS_TR = """Sen BıRAG'sın. Bağımlılıkla mücadele eden kişilere destek olan, yargılamayan bir yapay zeka rehberisin.

Kişiyi etiketlemezsin; kararların ona ait olduğunu bilir, özerkliğini korursun. Değişim nedenlerini sen vermezsin, onun kendi sözlerinden çıkarırsın. Söylemediği şeyleri varsaymaz, uydurmazsın. Katılmadığın bir şeyi onaylamazsın; itiraz ederken de yargılamazsın.

Terapist, doktor, avukat ya da acil servis yerine geçmezsin. Tanı koymaz, ilaç ve doz önermez, bırakma protokolü vermez, hukuki tavsiye vermezsin. Bilgi vermeden önce izin ister, kısa ve tarafsız verir, sonra nasıl geldiğini sorarsın.

Güvenlik riski, kriz ya da tıbbi aciliyet sezdiğinde olağan akışı durdurur, önce güvenliği konuşur ve uygun profesyonel desteğe yönlendirirsin.

Kısa, sade ve doğal Türkçe konuşursun. Tek seferde birden fazla soru sormazsın."""

# Birebir çeviri — içerik eklenmedi/çıkarılmadı, yalnızca dil değişti (Kural 3).
SYS_EN = """You are BıRAG, a non-judgmental AI guide who supports people struggling with addiction.

You do not label the person; you know the decisions are theirs and you protect their autonomy. You do not supply the reasons for change yourself; you draw them out of their own words. You do not assume or invent things they have not said. You do not affirm something you disagree with; and when you disagree, you do not judge.

You do not stand in for a therapist, doctor, lawyer or emergency service. You do not diagnose, recommend medication or dosage, give a quitting protocol, or give legal advice. You ask permission before giving information, give it briefly and neutrally, then ask how it landed.

When you sense a safety risk, a crisis or a medical emergency, you stop the ordinary flow, address safety first, and direct the person to appropriate professional support.

You speak in short, plain, natural Turkish. You do not ask more than one question at a time.

Always respond in Turkish."""

SYS_TR_DUSUN = SYS_TR + "\n\nİç muhakemeni de Türkçe kurarsın."

VARYANTLAR = {"tr_sys": SYS_TR, "en_sys": SYS_EN, "tr_sys_dusun": SYS_TR_DUSUN}
DIMS = ["duygusal_tepki", "yorumlama", "kesif", "mi_uyumu",
        "grounding", "kisalik_dogallik", "dil_butunlugu"]
OLCEK = {"duygusal_tepki": 2, "yorumlama": 2, "kesif": 2, "mi_uyumu": 5,
         "grounding": 5, "kisalik_dogallik": 5, "dil_butunlugu": 5}


def tohumlar(n: int) -> list[dict]:
    """Kampanyalar arası dengeli, deterministik örneklem."""
    rows = [json.loads(l) for l in open(ROOT / "data" / "seeds.jsonl") if l.strip()]
    rng = random.Random(11)
    kampanyalar = sorted({r["campaign"] for r in rows})
    pay = n // len(kampanyalar)
    secim = []
    for k in kampanyalar:
        aday = [r for r in rows if r["campaign"] == k and r["turn_count"] == 1]
        secim += rng.sample(aday, pay)
    return secim


def main(n: int = 12):
    from eval import split_output  # aynı ayrıştırıcı — K47 düzeltmesi dahil
    from mlx_lm import load, stream_generate
    from mlx_lm.sample_utils import make_sampler

    seeds = tohumlar(n)
    print(f"{len(seeds)} tohum · {len(VARYANTLAR)} varyant · model {MODEL_DIR.name} (adapter YOK)")
    model, tokenizer = load(str(MODEL_DIR))
    sampler = make_sampler(temp=0.0)

    sonuc = []
    for vad, sys_prompt in VARYANTLAR.items():
        print(f"\n[{vad}]")
        for s in seeds:
            msgs = [{"role": "system", "content": "<|think|>\n" + sys_prompt},
                    {"role": "user", "content": s["user_message"]}]
            prompt = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
            t0 = time.time()
            metin, son = [], None
            for p in stream_generate(model, tokenizer, prompt, max_tokens=2048, sampler=sampler):
                metin.append(p.text)
                son = p
            sure = time.time() - t0
            thinking, completion, kapandi = split_output("".join(metin))
            sonuc.append({
                "varyant": vad, "seed_id": s["seed_id"], "campaign": s["campaign"],
                "user_message": s["user_message"], "sys_prompt": sys_prompt,
                "thinking": thinking, "completion": completion, "thinking_kapandi": kapandi,
                "thinking_token": len(tokenizer.encode(thinking)) if thinking else 0,
                "completion_token": len(tokenizer.encode(completion)) if completion else 0,
                "uretim_token": son.generation_tokens, "sure_sn": round(sure, 2),
                "kesildi": son.finish_reason != "stop",
            })
            print(f"  {s['seed_id'][:8]} {sure:5.1f}sn  think={len(thinking.split()):4}kel "
                  f"cevap={len(completion.split()):3}kel  {'KESİLDİ' if son.finish_reason != 'stop' else ''}")
    del model

    print("\njudge:")
    for r in sonuc:
        kayit = {"messages": [
            {"role": "system", "content": SYS_TR},   # judge'a daima TR bağlam — sabit tutulur
            {"role": "user", "content": r["user_message"]},
            {"role": "assistant", "content": r["completion"], "thinking": r["thinking"]},
        ]}
        sahte = {"id": r["seed_id"], "slice": "terapotik_tek_tur", "scenario": "belirsiz",
                 "addiction_type": "alkol", "motivation": "ic", "mi_process": "engaging",
                 "talk_type": "ambivalans", "age_group": "yetiskin", "turn_type": "single",
                 "messages": kayit["messages"], "context": None,
                 "source_ids": [r["seed_id"]], "is_crisis": False, "is_negative": False,
                 "has_thinking": bool(r["thinking"])}
        r["_checks"] = run_checks(sahte)
        if not r["completion"]:
            r["judge"] = None
            continue
        try:
            t0 = time.time()
            r["judge"] = judge_mod.judge_record(kayit).model_dump()
            r["judge_sn"] = round(time.time() - t0, 1)
            print(f"  [{r['varyant']}] {r['seed_id'][:8]} {r['judge_sn']:5.1f}sn")
        except Exception as e:
            r["judge"] = None
            r["judge_hata"] = f"{type(e).__name__}: {e}"[:200]
            print(f"  [{r['varyant']}] {r['seed_id'][:8]} HATA")

    HAM.mkdir(parents=True, exist_ok=True)
    with open(HAM / "generations.jsonl", "w") as f:
        for r in sonuc:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"\nham çıktı: {HAM}")
    print("rapor için: uv run python scripts/analiz/2026-09-12-prompt-dili-raporu.py")


if __name__ == "__main__":
    n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 12
    main(n)
