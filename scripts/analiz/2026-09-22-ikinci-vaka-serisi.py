#!/usr/bin/env python3
"""İkinci vaka serisi — «alan dolu, biçimi doğru, DEĞERİ yanlış».

⛔⛔ **T22'nin TERSİ bir aile.** T22'de kapı VAR ve yanlış ateşliyor;
burada kapı var ama **hiç göremiyor** — çünkü kapılar bir alanın
VARLIĞINI ve BİÇİMİNİ denetler, DEĞERİNİ ve KAYNAĞINI değil.

⭐ **ALMA ÖLÇÜTÜ (önce yazıldı — T22'nin dersi).** Bir vaka seriye girer
ancak ve ancak dördü birden doğruysa:
  1. alan **doluydu**,
  2. biçimi/şeması **geçerliydi**,
  3. **hiçbir kapı reddetmedi**,
  4. değeri yine de **yanlıştı** ya da **anlamı belirsizdi**.

⛔ Dışarıda kalanlar ve nedenleri:
  · **K66 ailesi** — *«belgede yazan, kodda olmayan kural»*: orada kapı
    HİÇ YOK, burada var ama yanlış şeye bakıyor.
  · **K87 / T216** — boru hattı yanlış bağlanması (yanlış dilime kapı,
    yanlış sıra): alanın değeri değil, AKIŞ hatalı. Aşağıda ayrı
    bölümde, seriye dahil değil.
  · **T22 serisi** — orada kusur yüzey biçiminde, burada değerde.

⛔⛔ Seri yine bir **ALT SINIRDIR** (yalnız yakalanmışlar) ve derleyeni
benim (K30) ⇒ sıklık iddiası kurulamaz.

Çıktı: reports/analiz/2026-09-22-ikinci-vaka-serisi.md
"""
from __future__ import annotations

import collections
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-ikinci-vaka-serisi.md"

# (kayıt, alan, değer nasıl yanlıştı, kapı neden göremedi, nasıl bulundu, bedeli)
VAKA = [
 ("K69", "`slice`", "`kayit()`'in `slice_=\"terapotik_tek_tur\"` varsayılanı "
  "vardı; `#5` ve `#7` **çok turlu** yazıldığı hâlde o varsayılanla kaydedildi",
  "varsayılan makul bir değer üretti — ve `slice` zaten bir kapı konusu değil",
  "boru hattı sınaması", "2 kayıt"),
 ("T111", "`parti`, `date`", "Parti adı `\"v5-parti4\" if \"parti4\" in yol "
  "else \"v5-parti3\"` diye türetiliyordu; v5-parti5'in planıyla koşulunca "
  "**15 kaydın 15'i** `parti: v5-parti3` aldı",
  "⭐ kaydın kendi ifadesiyle: *«alan DOLUYDU, şema geçerliydi, değer de var "
  "olan bir şeydi»* — `checks.py` **15/15 geçti**",
  "elle okuma", "15 kayıt"),
 ("T193", "`ozerklik_vurgusu`", "Beyan, yapılan hamleden değil **ızgaradan** "
  "kopyalanıyordu ⇒ kayıt niyete eşitlendi; ızgara 9 derken metinde 12 vardı",
  "kapı beyanın DOLU olmasını denetliyor, KAYNAĞINI değil",
  "desen genişletilirken ölçüm", "3 kayıt + oran yanlış"),
 ("T204", "`esdurumlar` ↔ `risk_seviyesi`", "Beyan kapısı SERT'i iki sinyalin "
  "VEYA'sı olarak kuruyordu; ikisi **hiç birlikte görünmüyor** ⇒ aynı şeyi "
  "gösterdikleri varsayımı yanlış",
  "her iki alan da dolu ve geçerli; kapı birlikte-dağılımı hiç sormuyor",
  "betiği yazılmamış bir sayıyı yeniden üretirken", "ölçüt tanımı"),
 ("T217", "`source_ids`", "`v6-parti6 #15` ve `#19`'un METİNLERİ komşu "
  "satırların tohumlarını anlatıyordu; alan plandan geldiği için **doğru "
  "görünüyordu**",
  "⭐ *«bir alanın DOLU olduğunu denetlemek DOĞRU olduğunu denetlemek "
  "değildir»* — birleştirme raporunun *«tohum eşleşmesi 60/60»*'ı yalnız "
  "SAYI sayıyor", "elle örtüşme taraması", "2 kayıt"),
 ("T219 / T224", "`source_ids`, `gen_meta.seed_id`", "Üretilmiş bir partinin "
  "planı üretimden SONRA yeniden üretilip üstüne yazıldı (60 tohumun 60'ı "
  "değişti) ve kayıtların künyesi yeni plandan yeniden damgalandı. "
  "⛔ Ayrıca alanın ANLAMI partiler arasında sessizce değişmişti: parti1'de "
  "*«ızgarayı veren tohum»*, parti3-6'da *«metni veren tohum»*",
  "künye biçimsel olarak tutarlıydı; hiçbir kapı *«bu plan üretimden sonra "
  "mı yazıldı»* diye sormuyordu",
  "geriye dönük tarama + git zaman damgaları",
  "⛔ T220/T222 geçersiz, T221 düştü, T219 ÇÜRÜDÜ"),
 ("T235", "`ozerklik_vurgusu`", "Alan korpusun iki yarısında iki ayrı yoldan "
  "doldu — 412 kayıt uzlaştırmayla, 118 kayıt desen+elle onayla — ve ikisi "
  "aynı kesinlikte değil",
  "değerler geçerli, kapılar memnun; eksik olan **kaynağın kendisi**",
  "bütünlük denetimi (önce kusurlu sanıldı)", "118 kayıt işaretsiz"),
]

# ⛔ Seriye dahil DEĞİL — komşu aile, sınır burada çizilsin diye yazılı.
KOMSU = [
 ("K87", "boru hattı", "`checks.py` replay dilimini sessizce yok ediyordu; "
  "persona kapıları HER kayda uygulanıyordu ⇒ alan değil, kapının KAPSAMI "
  "yanlıştı"),
 ("T216", "boru hattı", "`beyan-metin-uyumu` düzeltmeyi blok dosyalarına, "
  "birleştirme korpus dosyasına yazıyor; sıra yanlışsa düzeltme korpusa HİÇ "
  "ULAŞMIYOR — değer doğru, AKIŞ hatalı"),
]


def main() -> int:
    neden = collections.Counter()
    for v in VAKA:
        neden["varsayılan/dal makul değer üretti"] += "varsayılan" in v[3] or "türetiliyordu" in v[2]
        neden["kaynak denetlenmiyor"] += "KAYNAĞINI" in v[3] or "DOĞRU olduğunu" in v[3] or "kaynağın kendisi" in v[3]
        neden["anlam ilan edilmemiş"] += "ANLAMI" in v[2] or "varsayımı yanlış" in v[2] or "iki ayrı yoldan" in v[2]
    bul = collections.Counter(v[4] for v in VAKA)

    sat = ["# İkinci vaka serisi — «alan dolu, biçimi doğru, değeri yanlış»", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Vaka:** {len(VAKA)} · komşu ama dışarıda: {len(KOMSU)}  ", "",
           "⭐ **Alma ölçütü (önce yazıldı):** alan doluydu · biçimi geçerliydi · "
           "hiçbir kapı reddetmedi · değeri yine de yanlış ya da anlamı "
           "belirsizdi. Dördü birden.", "",
           "⛔ **T22'nin TERSİ:** orada kapı var ve yanlış ateşliyor; burada "
           "kapı var ama hiç göremiyor.", "",
           "## Seri", "",
           "| # | kayıt | alan | değer nasıl yanlıştı | kapı neden göremedi | nasıl bulundu | bedeli |",
           "|---:|---|---|---|---|---|---|"]
    for i, v in enumerate(VAKA, 1):
        sat.append("| " + str(i) + " | " + " | ".join(v) + " |")

    sat += ["", "## Kapı neden göremedi — üç sebep", "", "| sebep | vaka |", "|---|---:|"]
    sat += [f"| {k} | {v} |" for k, v in neden.most_common() if v]
    sat += ["", "⭐⭐ Üçü de aynı şeyin yüzleri: **kapılar bir alanın VAR "
            "olduğunu ve BİÇİMİNE uyduğunu denetleyebiliyor; NEREDEN geldiğini "
            "ve NE ANLAMA geldiğini denetleyemiyor.** Bir varsayılan makul bir "
            "değer üretir, bir plan üstüne yazılır, bir alanın anlamı partiler "
            "arasında kayar — üçünde de şema geçerli kalır.", "",
            "## Bunları ne buldu", "", "| bulan | vaka |", "|---|---:|"]
    sat += [f"| {k} | {v} |" for k, v in bul.most_common()]
    sat += ["", "⭐⭐⭐ **Hiçbirini bir kapı bulmadı.** Bulanlar: elle okuma, "
            "geriye dönük tarama, boru hattı sınaması, bir başka sayıyı "
            "yeniden üretme girişimi, ve bir bütünlük denetimi. "
            "⛔ Sonuncusu (`T235`) **önce kusurlu sanıldı** — denetim "
            "*«118 tutarsızlık»* dedi ve ilk tepki denetimi kapatmaktı.", "",
            "➡️⭐⭐⭐ *Bu ailede kusur, kapının BAKTIĞI yerde değil BAKMADIĞI "
            "yerde duruyor; ve bakmadığı yeri gösteren tek şey, alanın "
            "kaynağını ya da anlamını AYRICA sormak. Bir kapı «dolu mu» diye "
            "sorabilir, «nereden geldi» diye soramaz — o soru veriye yazılmak "
            "zorunda.*", "",
            "⭐ Serinin uygulanmış karşılığı: `gen_meta.ozerklik_kaynak` "
            "(T235), künye kapısı ve plan kapısı (T224), tohum karşılığı "
            "kapısı (T217), sıra kapısı (T216). Hepsi *«değeri değil kaynağı "
            "denetle»* biçiminde.", "",
            "## ⛔ Komşu aile — seriye DAHİL DEĞİL", "",
            "Sınır burada çizilsin diye yazılı: bunlarda yanlış olan alanın "
            "değeri değil, **akış**.", "",
            "| kayıt | ne | ne oldu |", "|---|---|---|"]
    sat += [f"| {k} | {t} | {n} |" for k, t, n in KOMSU]
    sat += ["", "⛔ Ayrıca **K66 ailesi** (*«belgede yazan, kodda olmayan "
            "kural»*) de dışarıda: orada kapı hiç yok.", "",
            "## ⛔ Bu serinin söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **ALT SINIR** | yalnız yakalanmış vakalar; yakalanmamışların "
            "sayısı bilinmiyor ⇒ sıklık iddiası kurulamaz |",
            "| ⛔⛔ **Derleyen benim (K30)** | ölçüt yazılı ama uygulaması benim |",
            "| ⛔ **«Bedeli» sütunu eksik ölçülmüş** | `T224`'ünki sayılabildi "
            "(üç ölçüm geçersiz), ötekilerin dolaylı etkisi ölçülmedi |",
            "| ⚠️ **Kapıların faydası yine ölçülmedi** | seri kusurları "
            "topluyor; *«kapılar yetersiz»* sonucu çıkarılamaz — çıkarılabilecek "
            "tek şey, kapıların bu aileyi yapısal olarak göremediği |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[sat.index("## Kapı neden göremedi — üç sebep"):]))
    print(f"\n→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
