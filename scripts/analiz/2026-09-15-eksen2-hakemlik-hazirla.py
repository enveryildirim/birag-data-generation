#!/usr/bin/env python3
"""Aşama 2 (hakemlik) iş dosyalarını kurar — aşama 1'in istek dosyalarının BİREBİR kopyası.

K103'ün yöntemi: istek dosyaları `diff -rq` ile aynı doğrulanır, değişen tek şey
judge'ın örneklemesi olur. Kopyalamak yerine yeniden üretseydim, farkın kaynağı
"judge mi, prompt mu" ayrılamazdı.

Küme `hakemlik-kumesi.json`'dan gelir ve **iki yönlüdür** (işaretli + eşleştirilmiş
kontrol); gerekçe tasarım belgesinde.

Kullanım: uv run python scripts/analiz/2026-09-15-eksen2-hakemlik-hazirla.py
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
ISLER = Path("/private/tmp/claude-501/-Users-pc-projects-birag-data-finetuning"
             "/fe6477c2-8e5e-439e-875d-df2b5ed62d91/scratchpad/judge-isleri")
HEDEF = KOK / "reports/analiz/eksen2-judge"

HARITA = {
    "taban":    "e2-5ae67873", "A-dar":   "e2-b7584bec", "B-derin": "e2-220c3b5a",
    "C-dikkat": "e2-99b69ab4", "D-tam":   "e2-7ac7e984", "E-genis": "e2-ceef5655",
}


def main() -> int:
    kume = json.loads((HEDEF / "hakemlik-kumesi.json").read_text())
    # aşama 1'in (kol, id) -> istek no eşlemesi
    no = {}
    for kol, etiket in HARITA.items():
        for k in json.loads((ISLER / etiket / "kimlikler.json").read_text()):
            no[(kol, k["id"])] = k["no"]

    for gecis in ("p2", "p3"):
        dizin = ISLER / f"e2-hakem-{gecis}"
        if dizin.exists():
            shutil.rmtree(dizin)
        (dizin / "istek").mkdir(parents=True)
        (dizin / "sonuc").mkdir()
        kimlikler = []
        for i, oge in enumerate(kume, 1):
            kaynak = ISLER / HARITA[oge["kol"]] / "istek" / f"{no[(oge['kol'], oge['id'])]}.txt"
            hedef = dizin / "istek" / f"{i:03d}.txt"
            shutil.copyfile(kaynak, hedef)
            if hashlib.sha256(kaynak.read_bytes()).digest() != \
               hashlib.sha256(hedef.read_bytes()).digest():
                print(f"⛔ kopya birebir değil: {kaynak}")
                return 1
            kimlikler.append({"no": f"{i:03d}", "id": oge["id"],
                              "kol": oge["kol"], "rol": oge["rol"]})
        (dizin / "kimlikler.json").write_text(
            json.dumps(kimlikler, ensure_ascii=False, indent=1))
        print(f"{gecis}: {len(kimlikler)} iş → {dizin}")
    print("\nistek dosyaları aşama 1'in BİREBİR kopyası (sha256 doğrulandı) — "
          "değişen tek şey judge'ın örneklemesi")
    return 0


if __name__ == "__main__":
    sys.exit(main())
