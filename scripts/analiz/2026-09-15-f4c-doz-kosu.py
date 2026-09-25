#!/usr/bin/env python3
"""T30 DOZ-YANIT EĞRİSİ — eğitim ve eval koşucusu (ÜÇÜNCÜ aile, `f4c`).

⛔ `2026-09-15-f4-kapsam-kosu.py` (1. koşu) ve `2026-09-15-f4b-kapsam-kosu.py`
(2. koşu) DEĞİŞTİRİLMEZ — Kural 7. Bu üçüncü aile ayrı yazıldı.

Ne ölçülüyor
------------
T30: yönlendirme hamlesini korpusa geri koymak refleksi geri getirmedi. İki açıklama
ayırt edilmedi — (a) doz yetersiz, (b) ilişki asimetrik. Bu koşu iki doz noktası daha
ekliyor ve SABİT ADIMDA 5 kol × 3 doz ızgarası kuruyor:

    doz        korpus     adım   koşu ailesi
    %5,1       v0.0.3     372    f4b   (ölçüldü — K113)
    %10,2      v0.0.4     372    f4c-doz10
    %24,1      v0.0.5     372    f4c-doz25

⚠️ %2,0 noktası (v0.0.2, `f4` ailesi) **280 adımda** koşmuştu; bu eğriye doğrudan
eklenmez. Adımın kendi etkisi A-dar'da ölçülü: 280 → 2, 372 → 4 (K113 kontrol kolu).

Etiket önekleri `fs3-`/`sc3-`/`gd3-` + doz — üç koşunun çıktıları karışmasın diye.
⚠️ thinking bayrağı önceki iki koşuyla AYNI: eksenler `kapalı` modda (K108).
Judge ATLANIR (K97): yalnızca Pareto kapısını geçen kollara koşulur.

Kullanım:
  uv run python scripts/analiz/2026-09-15-f4c-doz-kosu.py egit
  uv run python scripts/analiz/2026-09-15-f4c-doz-kosu.py eksen
  uv run python scripts/analiz/2026-09-15-f4c-doz-kosu.py thinking
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

KOK = Path(__file__).parent.parent.parent
KOLLAR = ["A-dar", "B-derin", "C-dikkat", "D-tam", "E-genis"]
DOZLAR = ["doz10", "doz25"]


def ad(doz: str, kol: str) -> str:
    return f"f4c-{doz}-{kol}"


def adapter(doz: str, kol: str) -> Path:
    e = sorted(KOK.glob(f"runs/*-{ad(doz, kol)}/adapters"))
    if not e:
        raise SystemExit(f"adapter bulunamadı: {ad(doz, kol)}")
    if len(e) > 1:
        print(f"⚠️ {ad(doz, kol)} için {len(e)} koşu var, EN YENİSİ: {e[-1]}")
    return e[-1]


def kos(*argv: str) -> None:
    print(f"\n$ {' '.join(argv)}", flush=True)
    t0 = time.time()
    r = subprocess.run([sys.executable, *argv], cwd=KOK)
    print(f"  ({time.time() - t0:.0f} sn, çıkış {r.returncode})", flush=True)
    if r.returncode != 0:
        raise SystemExit(f"koşu başarısız: {' '.join(argv)}")


def egit() -> None:
    for doz in DOZLAR:
        for kol in KOLLAR:
            cfg = KOK / f"configs/training/{ad(doz, kol)}.yaml"
            if not cfg.exists():
                raise SystemExit(f"config yok: {cfg.relative_to(KOK)}")
            kos("src/train.py", str(cfg.relative_to(KOK)))


def eksenler() -> None:
    for doz in DOZLAR:
        for kol in KOLLAR:
            a = str(adapter(doz, kol))
            kos("src/eksen_eval.py", "evals/safety_crisis.jsonl",
                "--adapter", a, "--etiket", f"sc3-{doz}-{kol}")
            kos("src/eksen_eval.py", "evals/forgetting_smoke.jsonl",
                "--adapter", a, "--etiket", f"fs3-{doz}-{kol}")


def thinking_sondasi() -> None:
    for doz in DOZLAR:
        for kol in KOLLAR:
            kos("src/golden_eval.py", "evals/golden.dev.jsonl",
                "--adapter", str(adapter(doz, kol)),
                "--etiket", f"gd3-{doz}-{kol}", "--judge-atla")


if __name__ == "__main__":
    asama = sys.argv[1] if len(sys.argv) > 1 else ""
    if asama == "egit":
        egit()
    elif asama == "eksen":
        eksenler()
    elif asama == "thinking":
        thinking_sondasi()
    else:
        raise SystemExit("aşama: egit | eksen | thinking")
