#!/usr/bin/env python3
"""v6-parti2 tasarım ızgarası — 60 kayıt. Üretimden ÖNCE yazılır, dondurulur.

⭐ Izgara çözücü, hücre yasakları, üç kriz süzgeci ve hedefli tohum sıralaması
`2026-09-20-v6-parti1-plan.py` (PP1) üzerinden **çağrılır** — yeniden
tanımlanmaz (K97).

⛔⛔ **PARTİ1'DEN TEK YAPISAL FARK: hedefler artık ELLE SEÇİLMİYOR, ÖLÇÜMDEN
TÜRETİLİYOR.** Parti1'de `TOHUM_HEDEF` sayılarını ben yazmıştım ve şerhi de
yazılıydı (*«kesin değerler benim önerim»*). Parti1 koşup 59 kayıt üretince
açıklar değişti — üçü (`siddet=agir`, `stres_tipi=kronik_agri`,
`stres_tipi=yalnizlik`) listeden tamamen düştü. ⇒ Hedefi sabit tutmak, kapanmış
bir açığı yeniden hedeflemek olurdu.
➡️ *Bir hedef listesi ölçümden türetilmiyorsa, ölçüm değiştiğinde de aynı kalır
ve kapanmış açığı kovalamaya devam eder.*

**Türetme kuralı (ilan edilmiştir):** envanterin «gerçek açıklar» tablosundan
azınlık sınıfları (havuz payı < %40) alınır; her biri için parti hedefi
`min(havuz_payı × 2, %40) × 60` kayıt — yani havuz payının **iki katı**, %40
tavanıyla. İki kat, kümülatif setin pariteye doğru hareket etmesi için;
tavan, tek bir eksenin partiyi ele geçirmemesi için.
⛔ Çarpan (2) ve tavan (%40) **seçilmiştir**, türetilmemiştir — bu benim önerim.

⚠️ `tur` bir IZGARA ekseni olduğu için tohum hedefi olarak alınmaz; kotası
zaten havuzdan türetiliyor (PP1).

⭐ **T197'nin taşınan hedefi ÜRETİM talimatıdır, plan kotası değil:** parti1'de
`cevap_var` 5/15 çıktı (hedef 8) ve sebebi yapısal — §7b pasajın yalnız
yordam/erişim/gizlilik cümlesi taşımasına izin veriyor, kullanıcı sorusu başka
bir şey hakkındaysa cevap doğal olarak belgede olmuyor. ⇒ Parti2'de bağlamlı
kayıtların sorusu **pasaja göre tasarlanacak**; bu plan dosyasına yazılamaz,
üretim betiğinin başına yazılır ve burada **hatırlatma** olarak durur.

Girdi : reports/analiz/2026-09-20-kapsama-acigi-envanteri.json
Çıktı : data/plan/v6-parti2.jsonl · reports/analiz/2026-09-20-v6-parti2-plan.md
"""
from __future__ import annotations

import json
import os
from collections import Counter
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
N = 60
TOHUM = int(os.environ.get("BIRAG_PLAN_TOHUM", "20260921"))
CIKTI = KOK / "data/plan/v6-parti2.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-v6-parti2-plan.md"
ENVANTER = KOK / "reports/analiz/2026-09-20-kapsama-acigi-envanteri.json"

_sp = _iu.spec_from_file_location("pp1", KOK / "scripts/analiz/2026-09-20-v6-parti1-plan.py")
PP1 = _iu.module_from_spec(_sp)
_sp.loader.exec_module(PP1)
P3, P1, ESLEME = PP1.P3, PP1.P1, PP1.ESLEME

CARPAN = 2.0        # havuz payının kaç katı hedeflensin — SEÇİM
TAVAN = 0.40        # tek eksen partiyi ele geçirmesin — SEÇİM
BUYUK_SINIF = 40.0  # havuz payı bunun üstündeyse «çoğunluk», hedeflenmez


def hedefleri_turet() -> dict[tuple[str, str], int]:
    env = json.loads(ENVANTER.read_text(encoding="utf-8"))
    h: dict[tuple[str, str], int] = {}
    for anahtar, v in env["acik"].items():
        eksen, deger = anahtar.split("=", 1)
        if eksen == "bagimlilik_turu":      # ızgara ekseni (`tur`), kotayla çözülür
            continue
        if v["havuz"] >= BUYUK_SINIF:        # çoğunluk sınıfı — mutlak eşik yanıltır
            continue
        pay = min(v["havuz"] / 100 * CARPAN, TAVAN)
        h[(eksen, deger)] = round(N * pay)
    return h


def main() -> int:
    hedef = hedefleri_turet()
    PP1.TOHUM_HEDEF.clear()
    PP1.TOHUM_HEDEF.update(hedef)           # PP1'in sıralayıcısı bunu okuyor
    PP1._TURETILMIS = True                  # rapor şerhi buna göre yazılır
    PP1.CIKTI = CIKTI
    PP1.RAPOR = RAPOR
    PP1.TOHUM = TOHUM
    print(f"⭐ ölçümden türetilen hedefler ({len(hedef)}):")
    for (e, d), n in sorted(hedef.items(), key=lambda x: -x[1]):
        print(f"   {e}={d:18s} {n:2d}")
    rc = PP1.main()
    if rc:
        return rc
    ek = ["", "## ⭐⭐ Parti1'den farkı — hedefler ölçümden türetildi", "",
          "Parti1'de `TOHUM_HEDEF` sayıları **elle** seçilmişti ve şerhi yazılıydı. "
          "Parti1 koşunca açıklar değişti: `siddet_seviyesi=agir`, "
          "`stres_tipi=kronik_agri` ve `stres_tipi=yalnizlik` listeden **tamamen "
          "düştü**. Hedefi sabit tutmak kapanmış bir açığı kovalamak olurdu.", "",
          f"**Türetme kuralı:** azınlık sınıfları (havuz payı < %{BUYUK_SINIF:.0f}) "
          f"için hedef = `min(havuz_payı × {CARPAN:g}, %{TAVAN*100:.0f}) × {N}`.",
          f"⛔ Çarpan ({CARPAN:g}) ve tavan (%{TAVAN*100:.0f}) **seçilmiştir**, "
          "türetilmemiştir — bu benim önerim.", "",
          "| eksen = değer | havuz payı | **türetilen hedef** |", "|---|---:|---:|"]
    env = json.loads(ENVANTER.read_text(encoding="utf-8"))
    for (e, d), n in sorted(hedef.items(), key=lambda x: -x[1]):
        ek.append(f"| `{e}={d}` | %{env['acik'][f'{e}={d}']['havuz']} | **{n}** |")
    ek += ["", "## ⛔ ÜRETİM TALİMATI — plan kotası değil, hatırlatma", "",
           "⭐ **T197:** parti1'de `cevap_var` **5/15** çıktı (§7a hedefi 8) ve sebebi "
           "yapısal: §7b pasajın yalnız yordam/erişim/gizlilik/uygunluk/sınır cümlesi "
           "taşımasına izin veriyor ⇒ kullanıcı sorusu başka bir şey hakkındaysa cevap "
           "**doğal olarak** belgede olmuyor. ⇒ Parti2'de bağlamlı kayıtların sorusu "
           "**pasaja göre tasarlanacak**. Bu bir plan alanı değil, üretim kararıdır ve "
           "üretim betiğinin başına yazılacaktır.", "",
           "⭐ **T197 (2):** `ilgisiz` sınıfı **görmezden gelinir** — pasaj aktarılmaz. "
           "Parti1'de üç kayıtta bu ihlal edildi ve düzeltildi.", "",
           "⭐ **T196:** red ve özerklik cümleleri parti1'de şablona dönüştü "
           "(*«sana ben söyleyemem»* %11,9 ↔ korpus %1,2). Parti2'de reddin ve "
           "özerkliğin **biçimi** kayıttan kayda değiştirilecek; kapı zaten sert red "
           "değil okuma kuyruğu.", ""]
    RAPOR.write_text(RAPOR.read_text(encoding="utf-8") + "\n".join(ek), encoding="utf-8")
    print("\n".join(ek))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
