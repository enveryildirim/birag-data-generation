#!/usr/bin/env python3
"""Colab'dan gelen tek tur koşularını BU MAKİNEDE puanlar — EK-2.

Colab yalnız ham üretimi yazar (`sonuclar.jsonl` puanlanmamış + `ham.jsonl` + `ortam.json`).
Puanlama mühürlü `src/eksen_eval.py --yeniden` ile yapılır: üretim koşulmaz, iddialar
denetlenir, `sonuclar.jsonl` ve `kosu.json` yerinde yeniden yazılır. ⛔ `ham.jsonl` ve
`ortam.json`'a dokunulmaz (betik SHA ile denetler) — çözümleme jeton sayısını oradan okur.

İdempotent: puanlanmış dizin (ilk satırında `otomatik_gecti` var) atlanır.

Kullanım: Colab'ın `eksen-kosu/` ve `cok-turlu-kosu/` dizinlerini `reports/analiz/` altına
kopyala, sonra:  uv run python scripts/analiz/2026-09-29-v011-colab-puanla.py
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
EK = KOK / "reports/analiz/eksen-kosu"
KOLLAR = ("v010u", "v011u")


def _sha(y: Path) -> str:
    return hashlib.sha256(y.read_bytes()).hexdigest()


def main() -> int:
    yeni = atla = 0
    for kol in KOLLAR:
        for d in sorted(EK.glob(f"*-{kol}-t*-*")):
            for f in ("sonuclar.jsonl", "ham.jsonl", "ortam.json", "kosu.json"):
                if not (d / f).exists():
                    raise SystemExit(f"⛔ {d.name}: {f} yok — Colab çıktısı eksik kopyalanmış")
            ilk = json.loads((d / "sonuclar.jsonl").read_text(encoding="utf-8").splitlines()[0])
            if "otomatik_gecti" in ilk:
                atla += 1
                continue
            k = json.loads((d / "kosu.json").read_text(encoding="utf-8"))
            once = {f: _sha(d / f) for f in ("ham.jsonl", "ortam.json")}
            r = subprocess.run([sys.executable, str(KOK / "src/eksen_eval.py"), k["set"], "--yeniden", str(d)],
                               cwd=KOK, capture_output=True, text=True)
            if r.returncode != 0:
                raise SystemExit(f"⛔ {d.name} puanlanamadı:\n{r.stderr[-800:]}")
            assert {f: _sha(d / f) for f in once} == once, f"⛔ {d.name}: ham/ortam dosyası değişti"
            yeni += 1
            print(f"  puanlandı: {d.name}")
    print(f"✅ puanlanan {yeni} · zaten puanlı {atla}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
