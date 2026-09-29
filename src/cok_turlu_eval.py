#!/usr/bin/env python3
"""Çok turlu koşucu — `evals/cok_turlu.jsonl` (v0.1.1 Faz 3 · K277).

Her konuşmada model kendi önceki cevabını görerek sürer: tur k'de istem
[system, u1, a1, …, uk]; a_i modelin ÜRETTİĞİ cevaptır (yalnız `content`; önceki
turların düşünmesi istemde yer almaz — `golden_eval.prompt_kur`'un davranışı).

⭐ Üretim yolu `eksen_eval` ile BİREBİR: aynı `golden_eval.uret_yuklu` (sıcaklık 0),
aynı `prompt_kur`, aynı model dizini çözümü. Her tur, tek ögelik bir çağrıdır ⇒
yeni bir üretim yolu yazılmadı; iki koşucu arasındaki fark modelin değil koşucunun
farkı olamaz.

⛔ Boş cevap geçmişe BOŞ olarak girer (yumuşatılmaz); ölçüde soru sayılmaz.

Kullanım:
  uv run python src/cok_turlu_eval.py evals/cok_turlu.jsonl --adapter <dir> --etiket v011-t7-cokturlu
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime
from pathlib import Path

KOK = Path(__file__).parent.parent
sys.path.insert(0, str(KOK / "src"))


def konus(model, tokenizer, oge: dict, max_tokens: int, thinking: bool, uret_fn) -> list[dict]:
    msgs = [dict(m) for m in oge["messages"]]
    assert [m["role"] for m in msgs] == ["system"], f"⛔ {oge['id']}: yalnız system beklenir"
    turlar = []
    for k, u in enumerate(oge["kullanici_turlari"], 1):
        msgs.append({"role": "user", "content": u})
        c = uret_fn(model, tokenizer, [{"id": f"{oge['id']}-t{k}", "messages": list(msgs)}],
                    max_tokens, thinking)[0]
        turlar.append({"konusma": oge["id"], "tur": k, "kullanici": u, **c})
        msgs.append({"role": "assistant", "content": c["cevap"]})
    return turlar


def kos(ogeler: list[dict], model, tokenizer, max_tokens: int, thinking: bool, uret_fn) -> list[dict]:
    out = []
    for i, o in enumerate(ogeler, 1):
        print(f"konuşma {i}/{len(ogeler)} · {o['id']}")
        out += konus(model, tokenizer, o, max_tokens, thinking, uret_fn)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("set_yolu")
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--etiket", required=True)
    ap.add_argument("--max-tokens", type=int, default=1024)
    ap.add_argument("--thinking", action="store_true")
    a = ap.parse_args()

    import yaml
    from golden_eval import uret_yuklu
    from mlx_lm import load

    cfg = yaml.safe_load((KOK / "configs/training/e4b.yaml").read_text())
    model_dir = KOK / "models" / (cfg["model"].split("/")[-1] + "-train")
    if not model_dir.exists():
        model_dir = Path(cfg["model"])
    set_yol = KOK / a.set_yolu
    ogeler = [json.loads(l) for l in set_yol.read_text(encoding="utf-8").splitlines() if l.strip()]
    cikti = KOK / "reports/analiz/cok-turlu-kosu" / f"{datetime.now():%Y%m%d-%H%M%S}-{a.etiket}"
    cikti.mkdir(parents=True, exist_ok=False)

    model, tok = load(str(model_dir), adapter_path=a.adapter)
    t0 = time.time()
    turlar = kos(ogeler, model, tok, a.max_tokens, a.thinking, uret_yuklu)
    (cikti / "sonuclar.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in turlar), encoding="utf-8")
    (cikti / "kosu.json").write_text(json.dumps({
        "etiket": a.etiket, "set": a.set_yolu,
        "set_sha256_16": hashlib.sha256(set_yol.read_bytes()).hexdigest()[:16],
        "adapter": a.adapter, "model": str(model_dir), "thinking": a.thinking,
        "max_tokens": a.max_tokens, "konusma": len(ogeler), "tur": len(turlar),
        "uretim_sn": round(time.time() - t0), "tarih": datetime.now().isoformat(timespec="seconds"),
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"yazıldı: {cikti.relative_to(KOK)} · {len(turlar)} tur")
    return 0


if __name__ == "__main__":
    sys.exit(main())
