#!/usr/bin/env python3
"""Faz 4 kapsam taramasının EVAL koşucusu — üretimi yapar, yorum yapmaz.

Ayrı betik olmasının nedeni Kural 7: raporlanan sayının hangi komutla üretildiği
yazılı olmalı. Burada yalnızca `src/eksen_eval.py` ve `src/golden_eval.py`
çağrılıyor; koşu yolları ve bayraklar bu dosyada sabit.

⚠️ thinking bayrağı: Faz 3'ün BÜTÜN taban ölçümleri `thinking=kapalı` ile
alındı. Eğitilen model ise therapötik kayıtlarda `<|think|>` önekiyle eğitiliyor
(K44), yani üretim modu `açık`. Bu ikisi karıştırılırsa kapsam farkı sanılan şey
mod farkı olabilir. Bu yüzden önce **mod sondası** koşulur (aşama `mod`):
taban model, aynı sette, yalnızca bayrak değişerek. Sonuç tabanı oynatmıyorsa
eksenler Faz 3 moduna (kapalı) sabitlenir ve karşılaştırma korunur.

Kullanım:
  uv run python scripts/analiz/2026-09-15-f4-kapsam-kosu.py mod
  uv run python scripts/analiz/2026-09-15-f4-kapsam-kosu.py eksen
  uv run python scripts/analiz/2026-09-15-f4-kapsam-kosu.py thinking
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).parent.parent.parent
KOLLAR = ["A-dar", "B-derin", "C-dikkat", "D-tam", "E-genis"]


def adapter(kol: str) -> Path:
    eslesme = sorted(KOK.glob(f"runs/*-f4-kapsam-{kol}/adapters"))
    if not eslesme:
        raise SystemExit(f"adapter bulunamadı: {kol}")
    return eslesme[-1]


def kos(*argv: str) -> None:
    print(f"\n$ {' '.join(argv)}", flush=True)
    r = subprocess.run([sys.executable, *argv], cwd=KOK)
    if r.returncode != 0:
        raise SystemExit(f"koşu başarısız: {' '.join(argv)}")


def mod_sondasi() -> None:
    """Taban model, aynı set, yalnızca thinking bayrağı değişiyor.

    ⚠️ Sonda `safety_crisis` üzerinde koşuyor, `forgetting_smoke` üzerinde DEĞİL.
    Neden: `--thinking` bayrağı `<|think|>` önekini **system mesajının içeriğine**
    koyuyor (K44, `golden_eval.prompt_kur`). `forgetting_smoke`'un 30 öğesinin
    **hiçbirinde system mesajı yok** — yani o sette bayrak sessizce hiçbir şey
    yapmaz ve sonda "mod fark etmiyor" diye okunurdu. K44/K47 ailesinin üçüncü
    örneği: hata vermeyen, sessizce etkisiz katman.

    Karşılaştırma noktası: reports/analiz/eksen-kosu/20260915-105829-safety_crisis-baseline-1
    (aynı set, aynı model, thinking kapalı, 11/20).
    """
    kos("src/eksen_eval.py", "evals/safety_crisis.jsonl",
        "--etiket", "sc-taban-thinking-acik", "--thinking")


def eksenler() -> None:
    for kol in KOLLAR:
        a = str(adapter(kol))
        kos("src/eksen_eval.py", "evals/forgetting_smoke.jsonl",
            "--adapter", a, "--etiket", f"fs-{kol}")
        kos("src/eksen_eval.py", "evals/safety_crisis.jsonl",
            "--adapter", a, "--etiket", f"sc-{kol}")


def thinking_sondasi() -> None:
    """golden.dev — thinking KAPALI, Faz 3 tabanıyla aynı mod.

    Mod sondası (yukarıda) bayrağın tabanı 20 öğede 4'ünde oynattığını gösterdi,
    yani mod seçimi önemsiz değil. Yine de KAPALI seçiliyor ve gerekçesi kalıcı:
    `golden.locked` tabanı kapalı modda alındı ve mühür **bir kez daha** açılıyor
    (K31). Nihai koşu bu yüzden kapalı modda olmak ZORUNDA; taramanın da aynı
    modda olması, sonunda raporlanacak sayıyla tutarlı olmasını sağlıyor.
    Açık moddaki okuma ayrı bir soru olarak kayda geçiyor (rapor §3).

    Taban zaten var: reports/analiz/golden-kosu/20260915-083830-golden-v7-sonnet
    (48 öğe, kapalı, v7 rubriği). Yeniden koşulmuyor — üretim deterministik (K105).

    Judge ATLANIR: K97'ye göre judge ayrı yürüyor ve yalnızca Pareto kapısını
    geçen kollara koşulacak. `--yeniden-judge` ile sonradan aynı cevaplara koşulur.
    """
    for kol in KOLLAR:
        kos("src/golden_eval.py", "evals/golden.dev.jsonl",
            "--adapter", str(adapter(kol)), "--etiket", f"gd-{kol}", "--judge-atla")


if __name__ == "__main__":
    asama = sys.argv[1] if len(sys.argv) > 1 else ""
    {"mod": mod_sondasi, "eksen": eksenler, "thinking": thinking_sondasi}.get(
        asama, lambda: sys.exit(__doc__))()
