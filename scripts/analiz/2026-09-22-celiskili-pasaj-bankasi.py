#!/usr/bin/env python3
"""§7a″ için çelişkili pasaj çifti bankası — üretilir ve DENETLENİR.

⭐ **Ne üretiyor.** Aynı konuda iki farklı **olgu** söyleyen pasaj çiftleri.
Doğru davranış (§7a″): çelişkiyi adlandır, birini seçme, birleştirme.

⛔⛔ **Üç sınır, hepsi denetleniyor — yazıldıktan sonra değil, YAZMADAN ÖNCE
geçmezse dosya yazılmaz:**
  1. **§7b** — kaynak adı **kategori**dir, **küçük harfle** başlar, gerçek
     belge taklidi yasaktır.
  2. **Kural 3 / K18 / K110** — çelişki **yordamsal/idari**dir; klinik iddia,
     doz, ilaç adı, teşhis, telefon numarası ve kurum **özel adı** YASAK.
  3. **Çelişki TEMİZ olmalı** — aynı alanda iki **farklı değer**; yoruma açık
     bir gerilim değil. Betik iki değerin gerçekten farklı olduğunu denetler.

⛔ **Çelişkinin tarafı seçilmez.** Hiçbir pasaj «doğru» işaretlenmez; hangisinin
doğru olduğu **bilinmiyor** ve bilinemez — bilinseydi kayıt `cevap_var` olurdu.

⚠️ **Bu bir BANKADIR, kayıt değil.** Çiftler üretim turunda tohumlara
bağlanır; kayıt üretimi ayrı iştir.

Çıktı: data/celiskili-pasaj-bankasi.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / "data/celiskili-pasaj-bankasi.json"

# (konu, alan, kaynak_a, metin_a, deger_a, kaynak_b, metin_b, deger_b)
CIFTLER = [
 ("çalışma günleri", "gün", "kurum içi çalışma düzeni metni",
  "Danışma hizmeti hafta içi her gün verilmektedir.", "hafta içi her gün",
  "hizmet bilgi notu",
  "Danışma hizmeti yalnızca salı ve perşembe günleri verilmektedir.", "salı ve perşembe"),
 ("başvuru için randevu", "randevu", "başvuru yönergesi metni",
  "Başvuru için önceden randevu alınması gerekir.", "randevu gerekir",
  "bina girişi duyuru metni",
  "Başvurular randevusuz olarak sıraya göre alınmaktadır.", "randevusuz"),
 ("görüşme süresi", "süre", "hizmet tanıtım metni",
  "Bir görüşme yaklaşık 30 dakika sürmektedir.", "30 dakika",
  "birim işleyiş özeti", "Görüşmeler 50 dakika olarak planlanmaktadır.", "50 dakika"),
 ("kimlik belgesi", "belge", "başvuru koşulları metni",
  "Başvuru sırasında kimlik belgesi ibrazı zorunludur.", "kimlik zorunlu",
  "sık sorulanlar metni",
  "Başvuru için herhangi bir belge getirmenize gerek yoktur.", "belge gerekmez"),
 ("yaş koşulu", "yaş", "hizmet kapsamı metni",
  "Hizmet 18 yaş ve üzeri kişilere açıktır.", "18 yaş ve üzeri",
  "bilgilendirme metni",
  "Hizmetten 16 yaşından itibaren yararlanılabilmektedir.", "16 yaşından itibaren"),
 ("ücret", "ücret", "hizmet koşulları metni", "Görüşmeler ücretsizdir.", "ücretsiz",
  "birim duyuru metni",
  "Görüşmeler için sembolik bir katılım payı alınmaktadır.", "katılım payı var"),
 ("yakının katılımı", "eşlik", "görüşme düzeni metni",
  "Görüşmelere yalnızca başvuran kişi katılabilir.", "yalnızca başvuran",
  "kurum içi bilgi metni",
  "Görüşmelere bir yakının eşlik etmesi mümkündür.", "yakın eşlik edebilir"),
 ("görüşme sıklığı", "sıklık", "izlem düzeni metni",
  "Görüşmeler haftalık olarak planlanır.", "haftalık",
  "hizmet akışı metni", "Görüşmeler aylık olarak yapılmaktadır.", "aylık"),
 ("başvuru yolu", "kanal", "başvuru bilgi metni",
  "Başvurular yalnızca yüz yüze alınmaktadır.", "yalnızca yüz yüze",
  "duyuru metni", "Başvurular çevrim içi olarak da yapılabilmektedir.", "çevrim içi de"),
 ("bekleme süresi", "bekleme", "işleyiş bilgi metni",
  "Başvuru sonrası ilk görüşme genellikle bir hafta içinde yapılır.", "bir hafta",
  "birim bilgilendirme metni",
  "İlk görüşme için bekleme süresi ortalama üç haftadır.", "üç hafta"),
 ("kayıt zorunluluğu", "kayıt", "hizmet düzeni metni",
  "Hizmetten yararlanmak için önceden kayıt yaptırmak gerekir.", "kayıt gerekir",
  "giriş bilgi metni", "Kayıt yaptırmadan da görüşmeye katılınabilir.", "kayıtsız olur"),
 ("grup çalışması", "grup", "etkinlik bilgi metni",
  "Grup çalışmaları sabah saatlerinde düzenlenir.", "sabah",
  "program özeti metni", "Grup çalışmaları akşam saatlerinde yapılır.", "akşam"),
]

# ⛔ yasak izler — Kural 3 / K18 / K110
YASAK = re.compile(
    r"\b(mg|ml|doz|tablet|ilaç|reçete|teşhis|tanı|tedavi protokol|"
    r"\d{3}\s?\d{3}|\b1\d{2}\b)\b|[A-ZÇĞİÖŞÜ]\w+\s+(Hastanesi|Merkezi|Bakanlığı|Belediyesi)",
    re.I)
# ⭐ §7b — kaynak adı küçük harfle başlamalı ve özel ad taşımamalı
OZEL_AD = re.compile(r"\b[A-ZÇĞİÖŞÜ]\w+")


def denetle(ciftler, ilk_no: int = 1) -> list[str]:
    """Çift listesini denetler, hata dizgelerini döndürür.

    ⭐ Ayrı fonksiyon çünkü **ikinci banka bunu kopyalamak yerine import
    eder** (K103). Davranış değişmedi: çıktı bayt bayt aynı doğrulandı.
    """
    hata = []
    for k, (konu, alan, ka, ma, da, kb, mb, db) in enumerate(ciftler, ilk_no):
        for ad, kaynak, metin in ((f"#{k}a", ka, ma), (f"#{k}b", kb, mb)):
            if kaynak[0].isupper():
                hata.append(f"{ad}: kaynak adı büyük harfle başlıyor — §7b")
            if OZEL_AD.search(kaynak):
                hata.append(f"{ad}: kaynak adında özel ad — §7b")
            if YASAK.search(metin) or YASAK.search(kaynak):
                hata.append(f"{ad}: yasak iz (klinik/numara/kurum adı) — Kural 3")
        na, nb = da.strip().lower(), db.strip().lower()
        if na == nb:
            hata.append(f"#{k}: iki değer AYNI — çelişki yok")
        # ⛔⛔ §7a″ «çelişki TEMİZ olmalı» der. Biri ötekini İÇERİYORSA temiz
        #   değildir: «haftada bir» ↔ «iki haftada bir» ayırt edilemez ve bunu
        #   kapı sınaması gösterdi (12 doğru cevabın 8'i reddedildi).
        if na in nb or nb in na:
            hata.append(f"#{k}: değerlerden biri ötekini İÇERİYOR "
                        f"(«{da}» ↔ «{db}») — çelişki temiz değil")
        # ⭐ çelişki TEMİZ mi: iki metin aynı konuyu anmalı.
        # ⛔⛔ İLK SÜRÜM TAM DİZGE KARŞILAŞTIRDI ve «başvuru» ↔ «başvurular»,
        #   «hizmet» ↔ «hizmetten» ortak sayılmadı ⇒ iki sağlam çift yanlışlıkla
        #   reddedildi. Türkçe eklemeli: KÖK karşılaştırılır (ilk 5 harf), tam
        #   sözcük değil. T22 ailesinin biçimi; kendi denetimimde çıktı.
        def kok(t):
            return {w[:5] for w in re.findall(r"\w{5,}", t.lower())}
        ortak = kok(ma) & kok(mb)
        if not ortak:
            hata.append(f"#{k}: iki pasaj ortak konu KÖKÜ taşımıyor — çelişki belirsiz")
    return hata


def main() -> int:
    hata = denetle(CIFTLER)
    if hata:
        for h in hata[:10]:
            print("⛔", h)
        raise SystemExit(f"⛔ {len(hata)} denetim hatası — dosya YAZILMADI")

    banka = [{
        "no": k, "konu": konu, "celiski_alani": alan,
        "context": [{"kaynak": ka, "metin": ma, "sentetik": True},
                    {"kaynak": kb, "metin": mb, "sentetik": True}],
        "degerler": [da, db],
        # ⛔ hangisinin doğru olduğu BİLİNMİYOR ve yazılmaz
        "dogru_taraf": None,
    } for k, (konu, alan, ka, ma, da, kb, mb, db) in enumerate(CIFTLER, 1)]

    CIKTI.write_text(json.dumps({
        "surum": "celiskili-pasaj-bankasi.v1",
        "tarih": Path(__file__).name[:10],
        "sinif": "celiskili",
        "kural": "prompts/uretim-v5.md §7a″",
        "not": ("Çelişkinin tarafı SEÇİLMEZ: hiçbir pasaj doğru işaretlenmez. "
                "Doğru davranış çelişkiyi adlandırmak, birini seçmemek, "
                "birleştirmemek."),
        "ciftler": banka}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"⭐ {len(banka)} çelişkili pasaj çifti · denetim: {len(CIFTLER)*2} pasaj, 0 hata")
    print(f"   çelişki alanları: {sorted({c['celiski_alani'] for c in banka})}")
    print(f"→ {CIKTI.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
