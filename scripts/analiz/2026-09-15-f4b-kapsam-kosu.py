#!/usr/bin/env python3
"""Faz 4 kapsam taraması — İKİNCİ KOŞU (v0.0.3) eval koşucusu.

⛔ `2026-09-15-f4-kapsam-kosu.py`'nin YERİNE GEÇMEZ. O betik birinci koşunun
(v0.0.2, K109) üretim kaydıdır ve değiştirilmez (Kural 7).

Tek fark: adapter'lar `runs/*-f4b-kapsam-*` altından okunuyor ve etiketler
`fs2-`/`sc2-`/`gd2-` önekli — iki koşunun çıktıları `reports/analiz/eksen-kosu/`
içinde karışmasın diye.

⚠️ thinking bayrağı: birinci koşuyla AYNI — eksenler `kapalı` modda koşuyor (K108;
mühür gerekçesi). Mod sondası tekrarlanmıyor, çünkü mod modele değil bayrağa bağlı
ve birinci koşuda ölçüldü.

Kullanım:
  uv run python scripts/analiz/2026-09-15-f4b-kapsam-kosu.py eksen
  uv run python scripts/analiz/2026-09-15-f4b-kapsam-kosu.py thinking
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).parent.parent.parent
KOLLAR = ["A-dar", "B-derin", "C-dikkat", "D-tam", "E-genis"]
# Adım sayısı kontrolü: aynı veri, birinci koşunun adım sayısı. Yalnızca
# safety_crisis'te koşuluyor — sorusu tek: 280 -> 372 değişimi kararı oynatıyor mu.
KONTROL = "A-dar-280adim"


def adapter(kol: str) -> Path:
    eslesme = sorted(KOK.glob(f"runs/*-f4b-kapsam-{kol}/adapters"))
    if not eslesme:
        raise SystemExit(f"adapter bulunamadı: f4b-kapsam-{kol}")
    if len(eslesme) > 1:
        print(f"⚠️ {kol} için {len(eslesme)} koşu var, EN YENİSİ alınıyor: {eslesme[-1]}")
    return eslesme[-1]


def kos(*argv: str) -> None:
    print(f"\n$ {' '.join(argv)}", flush=True)
    r = subprocess.run([sys.executable, *argv], cwd=KOK)
    if r.returncode != 0:
        raise SystemExit(f"koşu başarısız: {' '.join(argv)}")


def eksenler() -> None:
    for kol in KOLLAR:
        a = str(adapter(kol))
        kos("src/eksen_eval.py", "evals/forgetting_smoke.jsonl",
            "--adapter", a, "--etiket", f"fs2-{kol}")
        kos("src/eksen_eval.py", "evals/safety_crisis.jsonl",
            "--adapter", a, "--etiket", f"sc2-{kol}")
    kos("src/eksen_eval.py", "evals/safety_crisis.jsonl",
        "--adapter", str(adapter(KONTROL)), "--etiket", f"sc2-{KONTROL}")


def thinking_sondasi() -> None:
    """golden.dev — thinking KAPALI (K31/K108 gerekçesi birinci koşuyla aynı).

    Judge ATLANIR (K97): yalnızca Pareto kapısını geçen kollara koşulur.
    """
    for kol in KOLLAR:
        kos("src/golden_eval.py", "evals/golden.dev.jsonl",
            "--adapter", str(adapter(kol)), "--etiket", f"gd2-{kol}", "--judge-atla")


if __name__ == "__main__":
    asama = sys.argv[1] if len(sys.argv) > 1 else ""
    {"eksen": eksenler, "thinking": thinking_sondasi}.get(
        asama, lambda: sys.exit(__doc__))()
