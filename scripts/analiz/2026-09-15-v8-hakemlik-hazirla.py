#!/usr/bin/env python3
"""v8 aşama 2 (hakemlik) iş dosyaları — aşama 1'in BİREBİR kopyası.

K103'ün yöntemi: kopyalar sha256 ile doğrulanır, değişen tek şey judge'ın kendi
örneklemesi olur. Yeniden üretseydim farkın kaynağı ayrılamazdı.

Küme `ayrisma-kumesi.json`'dan gelir ve **iki yönlüdür**: v7 ile v8'in ayrıştığı
öğeler + eşleştirilmiş AYRIŞMAYAN kontroller. Yalnızca ayrışanları yeniden koşmak
gürültüyü sistematik olarak küçük gösterirdi (K116'nın dersi).

Kullanım: uv run python scripts/analiz/2026-09-15-v8-hakemlik-hazirla.py
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
_sp = _iu.spec_from_file_location("b", KOK / "scripts/analiz/2026-09-15-v8-birlestir.py")
B = _iu.module_from_spec(_sp)
sys.argv = [sys.argv[0]]          # birleştirme betiği argparse kullanıyor
_sp.loader.exec_module(B)

ISLER, HEDEF = B.ISLER, B.HEDEF
TERS = {kol: etiket for etiket, (kol, _) in B.HARITA.items()}


def main() -> int:
    kume = json.loads((HEDEF / "ayrisma-kumesi.json").read_text())
    no = {}
    for kol, etiket in TERS.items():
        for k in json.loads((ISLER / f"v8-{etiket}" / "kimlikler.json").read_text()):
            no[(kol, k["id"])] = k["no"]

    for gecis in ("p2", "p3"):
        dizin = ISLER / f"v8-hakem-{gecis}"
        if dizin.exists():
            shutil.rmtree(dizin)
        (dizin / "istek").mkdir(parents=True)
        (dizin / "sonuc").mkdir()
        kimlikler = []
        for i, oge in enumerate(kume, 1):
            kaynak = (ISLER / f"v8-{TERS[oge['kol']]}" / "istek"
                      / f"{no[(oge['kol'], oge['id'])]}.txt")
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
        print(f"{gecis}: {len(kimlikler)} iş → {dizin.name}")
    n_a = sum(1 for x in kume if x["rol"] == "ayrisan")
    print(f"\nküme: {n_a} ayrışan + {len(kume) - n_a} kontrol · "
          f"istek dosyaları aşama 1'in BİREBİR kopyası (sha256 doğrulandı)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
