#!/usr/bin/env python3
"""v8 iş dosyalarını kurar — v7 iş dosyasının RUBRİK bölümü değiştirilerek.

v7 iş dosyası tam olarak `<rubrik metni>` + `\\n\\n\\n---\\n\\n## Değerlendirilecek
konuşma\\n\\n` + `<konuşma>` biçiminde. v8 dosyası aynı kuyruğu **baytı baytına**
taşır; değişen tek şey baştaki rubrik.

Neden kopyalama/yeniden üretme değil: konuşma yeniden render edilseydi v7↔v8 farkının
kaynağı *«rubrik mi, render mı»* ayrılamazdı (K103'ün yöntemi).

⛔ v7'nin dizinleri OKUNUR, YAZILMAZ (Kural 7) — v8 `v8-` önekli kendi dizinlerini kurar.

Kullanım: uv run python scripts/analiz/2026-09-15-v8-is-hazirla.py
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
_sp = _iu.spec_from_file_location("plan", KOK / "scripts/analiz/2026-09-15-v8-kosu-plan.py")
PLAN = _iu.module_from_spec(_sp)
_sp.loader.exec_module(PLAN)

ISLER, KUME = PLAN.ISLER, PLAN.KUME
R7 = PLAN.RUBRIK7.read_text(encoding="utf-8").strip()
R8 = PLAN.RUBRIK8.read_text(encoding="utf-8").strip()


def main() -> int:
    toplam, hata = 0, []
    for kol, etiket in KUME:
        kaynak = ISLER / etiket
        hedef = ISLER / f"v8-{etiket}"
        if hedef.exists():
            shutil.rmtree(hedef)
        (hedef / "istek").mkdir(parents=True)
        (hedef / "sonuc").mkdir()
        for p in sorted((kaynak / "istek").glob("*.txt")):
            ham = p.read_text(encoding="utf-8")
            if not ham.startswith(R7):
                hata.append(f"{kol}/{p.name}: v7 rubriğiyle başlamıyor")
                continue
            kuyruk = ham[len(R7):]          # konuşma bölümü — DOKUNULMUYOR
            (hedef / "istek" / p.name).write_text(R8 + kuyruk, encoding="utf-8")
            # Kuyruk gerçekten aynı mı — yeni dosyadan geri okunarak doğrulanır.
            yeni = (hedef / "istek" / p.name).read_text(encoding="utf-8")
            if yeni[len(R8):] != kuyruk:
                hata.append(f"{kol}/{p.name}: konuşma bölümü değişti")
            if hashlib.sha256(kuyruk.encode()).hexdigest() != \
               hashlib.sha256(ham[len(R7):].encode()).hexdigest():
                hata.append(f"{kol}/{p.name}: kuyruk sha256 tutmadı")
            toplam += 1
        shutil.copyfile(kaynak / "kimlikler.json", hedef / "kimlikler.json")

    if hata:
        print(f"⛔ İŞ HAZIRLAMA DÜŞTÜ ({len(hata)}):")
        for h in hata[:10]:
            print("   ·", h)
        return 1

    # Bütün v8 dosyaları v8 rubriğiyle başlıyor ve v7 rubriği hiçbirinde GEÇMİYOR.
    for kol, etiket in KUME:
        for p in sorted((ISLER / f"v8-{etiket}" / "istek").glob("*.txt")):
            t = p.read_text(encoding="utf-8")
            if not t.startswith(R8) or "Eksen 1 (v7)" in t:
                print(f"⛔ {p} v8 rubriğiyle başlamıyor ya da v7 izi taşıyor")
                return 1

    print(f"✅ {toplam} v8 iş dosyası kuruldu · konuşma bölümü birebir doğrulandı")
    for kol, etiket in KUME:
        n = len(list((ISLER / f"v8-{etiket}" / "istek").glob("*.txt")))
        print(f"   {kol:9} v8-{etiket}  {n} iş")
    return 0


if __name__ == "__main__":
    sys.exit(main())
