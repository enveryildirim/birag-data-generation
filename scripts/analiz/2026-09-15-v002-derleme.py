#!/usr/bin/env python3
"""`datasets/v0.0.2/` girdisini derler — Faz 4 kalibrasyon ve döngü başlangıç seti.

Neden ayrı bir betik: elde üç ayrı kayıt var ve hiçbiri tek başına `build.py`'nin
beklediği biçimde değil —

  · `data/candidates/v3-kumulatif.jsonl`   104 kayıt, `_checks` YOK, `judge` YOK
  · `data/judged/v3-kumulatif.v7.jsonl`    aynı 104 kayıt, `judge` v7 rubriğiyle,
                                           ama `_checks` YOK (rubrik yeniden
                                           puanlama betiğinden çıktı, filter'dan değil)
  · `data/candidates/replay-v1.jsonl`      18 açık veri kaydı, judge'a GİRMEZ (K88/K89)

`build.py` `_checks.passed` görmezse kaydı eler; yani v7 dosyası doğrudan
verilseydi **104/104 sessizce düşerdi**. Bu yüzden kapılar burada YENİDEN
koşuluyor (deterministik, LLM gerektirmez) ve v7 judge sonucu üzerine bindiriliyor.

Çıktı: `data/judged/v0.0.2.jsonl` → `uv run python src/build.py data/judged/v0.0.2.jsonl v0.0.2`

Kullanım: uv run python scripts/analiz/2026-09-15-v002-derleme.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).parent.parent.parent
sys.path.insert(0, str(KOK / "src"))
from checks import run_checks  # noqa: E402

ADAY = KOK / "data/candidates/v3-kumulatif.jsonl"
JUDGE = KOK / "data/judged/v3-kumulatif.v7.jsonl"
REPLAY = KOK / "data/candidates/replay-v1.jsonl"
CIKTI = KOK / "data/judged/v0.0.2.jsonl"


def oku(p: Path) -> list[dict]:
    return [json.loads(l) for l in open(p) if l.strip()]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def main() -> int:
    aday, judge, replay = oku(ADAY), oku(JUDGE), oku(REPLAY)
    jmap = {r["id"]: r.get("judge") for r in judge}
    if set(jmap) != {r["id"] for r in aday}:
        print("HATA: aday ve judge kimlik kümeleri farklı — birleştirme güvenli değil.")
        return 1

    cikti, kapi_dusen = [], []
    for r in aday + replay:
        r = dict(r)
        if r["id"] in jmap:
            r["judge"] = jmap[r["id"]]          # v7 rubriği (K100)
        chk = run_checks(r)
        r["_checks"] = chk
        if not chk.get("passed"):
            kapi_dusen.append((r["id"], chk))
        cikti.append(r)

    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in cikti))

    jm = Counter(r["judge"].get("judge_model") for r in cikti
                 if isinstance(r.get("judge"), dict))
    print(f"aday      {ADAY.name:32} {len(aday):>4} kayıt  sha {sha(ADAY)}")
    print(f"judge v7  {JUDGE.name:32} {len(judge):>4} kayıt  sha {sha(JUDGE)}")
    print(f"replay    {REPLAY.name:32} {len(replay):>4} kayıt  sha {sha(REPLAY)}")
    print(f"\nkapı: {len(cikti) - len(kapi_dusen)}/{len(cikti)} geçti")
    for i, c in kapi_dusen:
        print(f"  DÜŞTÜ {i}: {[k for k, v in c.items() if v is False]}")
    print(f"judge_model: {dict(jm)}  (judge'suz {sum(1 for r in cikti if not r.get('judge'))} = replay, K88/K89)")
    print(f"\nyazıldı: {CIKTI.relative_to(KOK)}  sha {sha(CIKTI)}")
    print("sıradaki: uv run python src/build.py data/judged/v0.0.2.jsonl v0.0.2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
