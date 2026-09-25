# İkinci vaka serisi — «alan dolu, biçimi doğru, değeri yanlış»

**Betik:** `scripts/analiz/2026-09-22-ikinci-vaka-serisi.py` · **Tarih:** 2026-09-22  
**Vaka:** 7 · komşu ama dışarıda: 2  

⭐ **Alma ölçütü (önce yazıldı):** alan doluydu · biçimi geçerliydi · hiçbir kapı reddetmedi · değeri yine de yanlış ya da anlamı belirsizdi. Dördü birden.

⛔ **T22'nin TERSİ:** orada kapı var ve yanlış ateşliyor; burada kapı var ama hiç göremiyor.

## Seri

| # | kayıt | alan | değer nasıl yanlıştı | kapı neden göremedi | nasıl bulundu | bedeli |
|---:|---|---|---|---|---|---|
| 1 | K69 | `slice` | `kayit()`'in `slice_="terapotik_tek_tur"` varsayılanı vardı; `#5` ve `#7` **çok turlu** yazıldığı hâlde o varsayılanla kaydedildi | varsayılan makul bir değer üretti — ve `slice` zaten bir kapı konusu değil | boru hattı sınaması | 2 kayıt |
| 2 | T111 | `parti`, `date` | Parti adı `"v5-parti4" if "parti4" in yol else "v5-parti3"` diye türetiliyordu; v5-parti5'in planıyla koşulunca **15 kaydın 15'i** `parti: v5-parti3` aldı | ⭐ kaydın kendi ifadesiyle: *«alan DOLUYDU, şema geçerliydi, değer de var olan bir şeydi»* — `checks.py` **15/15 geçti** | elle okuma | 15 kayıt |
| 3 | T193 | `ozerklik_vurgusu` | Beyan, yapılan hamleden değil **ızgaradan** kopyalanıyordu ⇒ kayıt niyete eşitlendi; ızgara 9 derken metinde 12 vardı | kapı beyanın DOLU olmasını denetliyor, KAYNAĞINI değil | desen genişletilirken ölçüm | 3 kayıt + oran yanlış |
| 4 | T204 | `esdurumlar` ↔ `risk_seviyesi` | Beyan kapısı SERT'i iki sinyalin VEYA'sı olarak kuruyordu; ikisi **hiç birlikte görünmüyor** ⇒ aynı şeyi gösterdikleri varsayımı yanlış | her iki alan da dolu ve geçerli; kapı birlikte-dağılımı hiç sormuyor | betiği yazılmamış bir sayıyı yeniden üretirken | ölçüt tanımı |
| 5 | T217 | `source_ids` | `v6-parti6 #15` ve `#19`'un METİNLERİ komşu satırların tohumlarını anlatıyordu; alan plandan geldiği için **doğru görünüyordu** | ⭐ *«bir alanın DOLU olduğunu denetlemek DOĞRU olduğunu denetlemek değildir»* — birleştirme raporunun *«tohum eşleşmesi 60/60»*'ı yalnız SAYI sayıyor | elle örtüşme taraması | 2 kayıt |
| 6 | T219 / T224 | `source_ids`, `gen_meta.seed_id` | Üretilmiş bir partinin planı üretimden SONRA yeniden üretilip üstüne yazıldı (60 tohumun 60'ı değişti) ve kayıtların künyesi yeni plandan yeniden damgalandı. ⛔ Ayrıca alanın ANLAMI partiler arasında sessizce değişmişti: parti1'de *«ızgarayı veren tohum»*, parti3-6'da *«metni veren tohum»* | künye biçimsel olarak tutarlıydı; hiçbir kapı *«bu plan üretimden sonra mı yazıldı»* diye sormuyordu | geriye dönük tarama + git zaman damgaları | ⛔ T220/T222 geçersiz, T221 düştü, T219 ÇÜRÜDÜ |
| 7 | T235 | `ozerklik_vurgusu` | Alan korpusun iki yarısında iki ayrı yoldan doldu — 412 kayıt uzlaştırmayla, 118 kayıt desen+elle onayla — ve ikisi aynı kesinlikte değil | değerler geçerli, kapılar memnun; eksik olan **kaynağın kendisi** | bütünlük denetimi (önce kusurlu sanıldı) | 118 kayıt işaretsiz |

## Kapı neden göremedi — üç sebep

| sebep | vaka |
|---|---:|
| kaynak denetlenmiyor | 3 |
| anlam ilan edilmemiş | 3 |
| varsayılan/dal makul değer üretti | 2 |

⭐⭐ Üçü de aynı şeyin yüzleri: **kapılar bir alanın VAR olduğunu ve BİÇİMİNE uyduğunu denetleyebiliyor; NEREDEN geldiğini ve NE ANLAMA geldiğini denetleyemiyor.** Bir varsayılan makul bir değer üretir, bir plan üstüne yazılır, bir alanın anlamı partiler arasında kayar — üçünde de şema geçerli kalır.

## Bunları ne buldu

| bulan | vaka |
|---|---:|
| boru hattı sınaması | 1 |
| elle okuma | 1 |
| desen genişletilirken ölçüm | 1 |
| betiği yazılmamış bir sayıyı yeniden üretirken | 1 |
| elle örtüşme taraması | 1 |
| geriye dönük tarama + git zaman damgaları | 1 |
| bütünlük denetimi (önce kusurlu sanıldı) | 1 |

⭐⭐⭐ **Hiçbirini bir kapı bulmadı.** Bulanlar: elle okuma, geriye dönük tarama, boru hattı sınaması, bir başka sayıyı yeniden üretme girişimi, ve bir bütünlük denetimi. ⛔ Sonuncusu (`T235`) **önce kusurlu sanıldı** — denetim *«118 tutarsızlık»* dedi ve ilk tepki denetimi kapatmaktı.

➡️⭐⭐⭐ *Bu ailede kusur, kapının BAKTIĞI yerde değil BAKMADIĞI yerde duruyor; ve bakmadığı yeri gösteren tek şey, alanın kaynağını ya da anlamını AYRICA sormak. Bir kapı «dolu mu» diye sorabilir, «nereden geldi» diye soramaz — o soru veriye yazılmak zorunda.*

⭐ Serinin uygulanmış karşılığı: `gen_meta.ozerklik_kaynak` (T235), künye kapısı ve plan kapısı (T224), tohum karşılığı kapısı (T217), sıra kapısı (T216). Hepsi *«değeri değil kaynağı denetle»* biçiminde.

## ⛔ Komşu aile — seriye DAHİL DEĞİL

Sınır burada çizilsin diye yazılı: bunlarda yanlış olan alanın değeri değil, **akış**.

| kayıt | ne | ne oldu |
|---|---|---|
| K87 | boru hattı | `checks.py` replay dilimini sessizce yok ediyordu; persona kapıları HER kayda uygulanıyordu ⇒ alan değil, kapının KAPSAMI yanlıştı |
| T216 | boru hattı | `beyan-metin-uyumu` düzeltmeyi blok dosyalarına, birleştirme korpus dosyasına yazıyor; sıra yanlışsa düzeltme korpusa HİÇ ULAŞMIYOR — değer doğru, AKIŞ hatalı |

⛔ Ayrıca **K66 ailesi** (*«belgede yazan, kodda olmayan kural»*) de dışarıda: orada kapı hiç yok.

## ⛔ Bu serinin söylemedikleri

| | |
|---|---|
| ⛔⛔ **ALT SINIR** | yalnız yakalanmış vakalar; yakalanmamışların sayısı bilinmiyor ⇒ sıklık iddiası kurulamaz |
| ⛔⛔ **Derleyen benim (K30)** | ölçüt yazılı ama uygulaması benim |
| ⛔ **«Bedeli» sütunu eksik ölçülmüş** | `T224`'ünki sayılabildi (üç ölçüm geçersiz), ötekilerin dolaylı etkisi ölçülmedi |
| ⚠️ **Kapıların faydası yine ölçülmedi** | seri kusurları topluyor; *«kapılar yetersiz»* sonucu çıkarılamaz — çıkarılabilecek tek şey, kapıların bu aileyi yapısal olarak göremediği |
