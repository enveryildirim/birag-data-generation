#!/usr/bin/env python3
"""v9 iş dosyalarını kurar — v8 iş dosyasının RUBRİK bölümü değiştirilerek.

v8 iş dosyası `<rubrik metni>` + `<konuşma kuyruğu>` biçiminde ve o kuyruk v7'nin
kuyruğunun **birebir** kopyası (K103). v9 dosyası aynı kuyruğu taşır; değişen tek
şey baştaki rubrik. Böylece zincirin üç halkası da aynı konuşma metnini görüyor.

⛔ v8'in dizinleri OKUNUR, YAZILMAZ (Kural 7) — v9 `v9-` önekli kendi dizinlerini kurar.

Kullanım: uv run python scripts/analiz/2026-09-15-v9-is-hazirla.py
"""
from __future__ import annotations

import hashlib
import shutil
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
_sp = _iu.spec_from_file_location("plan9", KOK / "scripts/analiz/2026-09-15-v9-kosu-plan.py")
PLAN = _iu.module_from_spec(_sp)
_sp.loader.exec_module(PLAN)

ISLER, KUME = PLAN.ISLER, PLAN.KUME
R8 = PLAN.RUBRIK8.read_text(encoding="utf-8").strip()
R9 = PLAN.RUBRIK9.read_text(encoding="utf-8").strip()


def main() -> int:
    toplam, hata = 0, []
    for kol, etiket in KUME:
        kaynak = ISLER / etiket
        hedef = ISLER / f"v9-{etiket[3:]}"
        if hedef.exists():
            shutil.rmtree(hedef)
        (hedef / "istek").mkdir(parents=True)
        (hedef / "sonuc").mkdir()
        for p in sorted((kaynak / "istek").glob("*.txt")):
            ham = p.read_text(encoding="utf-8")
            if not ham.startswith(R8):
                hata.append(f"{kol}/{p.name}: v8 rubriğiyle başlamıyor")
                continue
            kuyruk = ham[len(R8):]          # konuşma bölümü — DOKUNULMUYOR
            (hedef / "istek" / p.name).write_text(R9 + kuyruk, encoding="utf-8")
            yeni = (hedef / "istek" / p.name).read_text(encoding="utf-8")
            if yeni[len(R9):] != kuyruk:
                hata.append(f"{kol}/{p.name}: konuşma bölümü değişti")
            if hashlib.sha256(yeni[len(R9):].encode()).hexdigest() != \
               hashlib.sha256(kuyruk.encode()).hexdigest():
                hata.append(f"{kol}/{p.name}: kuyruk sha256 tutmadı")
            toplam += 1
        shutil.copyfile(kaynak / "kimlikler.json", hedef / "kimlikler.json")

    if hata:
        print(f"⛔ İŞ HAZIRLAMA DÜŞTÜ ({len(hata)}):")
        for h in hata[:10]:
            print("   ·", h)
        return 1

    for kol, etiket in KUME:
        for p in sorted((ISLER / f"v9-{etiket[3:]}" / "istek").glob("*.txt")):
            t = p.read_text(encoding="utf-8")
            if not t.startswith(R9) or "Eksen 1 (v8)" in t or "Eksen 1 (v7)" in t:
                print(f"⛔ {p} v9 rubriğiyle başlamıyor ya da eski sürüm izi taşıyor")
                return 1

    print(f"✅ {toplam} v9 iş dosyası kuruldu · konuşma bölümü birebir doğrulandı")
    for kol, etiket in KUME:
        d = ISLER / f"v9-{etiket[3:]}"
        print(f"   {kol:9} {d.name}  {len(list((d / 'istek').glob('*.txt')))} iş")
    return 0


if __name__ == "__main__":
    sys.exit(main())
