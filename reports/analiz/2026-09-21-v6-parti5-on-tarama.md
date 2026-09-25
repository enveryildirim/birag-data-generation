# v6-parti5 — üretim öncesi kriz taraması

**Betik:** `scripts/analiz/2026-09-21-v6-parti5-on-tarama.py` · **Tarih:** 2026-09-21  
**Girdi:** `data/plan/v6-parti5.jsonl` · **60** satır

⛔⛔ T192: `v6-parti1 #29` **dört kapının dördünü de** geçmişti. T199: `#54`'ü yakalayan şey sınıfı değil **mesajıydı**. ➡️ *Bir süzgeç yalnız kendi sözlüğünü tanır; tohum metni okunmadan üretime girmez.*

| | |
|---|---:|
| işaret taşıyan satır | **18** / 60 |
| — yalnız `risk_seviyesi` alanından | 15 |
| ⛔ **içerik/beyan süzgeci ateşleyen** | **3** |
| ⛔ **üretilmeyecek satır** | **0**  |

⛔ **3 satır içerik/beyan süzgeci ateşledi** ve her biri aşağıda ayrı ayrı hükme bağlandı. Kalan işaretler `risk_seviyesi` alanından geliyor; o alan tek başına eleme ölçütü değil (SERT eşiği `cok_yuksek`).

⛔ **İşaretli 18 satırın tam metni okundu.** Bu bir BETİK çıktısı değil, benim beyanımdır (K30); betik yalnız hangi satırların okunması gerektiğini söyler.

## İşaretli satırlar

| # | tür / senaryo | işaret | hüküm |
|---:|---|---|---|
| 1 | `tutun` / `nazikce_karsi_cikma` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 10 | `dijital` / `belirsiz` | risk:yuksek | ⭐ okundu, kriz yok |
| 18 | `receteli_ilac` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 22 | `kumar` / `nazikce_karsi_cikma` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 23 | `dijital` / `belirsiz` | risk:yuksek | ⭐ okundu, kriz yok |
| 24 | `alkol` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 29 | `receteli_ilac` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 35 | `dijital` / `belirsiz` | risk:yuksek | ⭐ okundu, kriz yok |
| 36 | `kumar` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 37 | `kumar` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 41 | `receteli_ilac` / `belirsiz` | TG:acil servis,taburcu + risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 43 | `alkol` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 44 | `alkol` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 45 | `receteli_ilac` / `ambivalans` | TG:taburcu + risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 47 | `alkol` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 51 | `dijital` / `belirsiz` | risk:yuksek | ⭐ okundu, kriz yok |
| 53 | `receteli_ilac` / `ambivalans` | TG:acil servis + risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 58 | `alkol` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |

## ⚠️ Üretim notları — eleme değil, talimat

**`#1`** — ⛔⛔ ÜRETİM NOTU — **stent takılalı bir gün** olmuş ve sigara içmiş; üstüne *«bir kalp krizi her şeyi değiştirir mi?»* diye soruyor. §5a″ md.3 (doğrudan klinik soru) ve md.1'e komşu bir durum. Kalp krizinin ne değiştirdiği SÖYLENMEYECEK — yönlendirme dünkü taburcu eden yere.

**`#18`** — ⚠️ ÜRETİM NOTU — antidepresan + akşam rakısı, gece 11'e kadar bebekle yalnız. §5a″ md.2. İlaç adı kullanıcı turunda bile genelleştirilecek.

**`#22`** — ⭐ ÜRETİM NOTU — sponsor iki hafta sonra yazmış; **iyi giden bir an**. Randevuyu ertelemiş olması bir suç konusu yapılmayacak, ve sponsora ne yazacağı da ben kurmayacağım. Kurum adı genelleştirilecek.

**`#24`** — ⚠️ ÜRETİM NOTU — *«senden zaten bir şey çıkmaz»* ve *«Niye uğraşıyorum ki yani»*. Annenin cümlesi kullanıcının kendi hükmüne dönüşmüş (parti4 `#47`'nin biçimi) ama orada baba, burada anne ve kullanıcı cümleyi henüz benimsememiş — *«ama»* ile devam ediyor.

**`#29`** — ⚠️ ÜRETİM NOTU — yaygınlık gerekçesi ÜÇÜNCÜ kez (parti3 `#23`, `#38`). *«Yaygınlık ≠ uygunluk»* itirazı bu partide TEKRARLANMAYACAK; burada karşılaştırma bir komşuyla ve asıl mesele eşinin gözü.

**`#36`** — ⚠️ ÜRETİM NOTU — ev arkadaşlarından üç kez aynı bahaneyle 18 bin lira alınmış ve kaybedilmiş; kayıt silinme riski var. ⛔ Borç ya da kayıt için bir çözüm ÜRETİLMEYECEK; ikisi de benim çözebileceğim şeyler değil.

**`#37`** — ⚠️⚠️ ÜRETİM NOTU — yalnızlık kümesi (parti4 `#56`'nın aynısı): kardeş *«sen değişmezsin»* demiş, sponsor iki haftadır cevap vermiyor, anne yorgun. ⛔ Cevaba **bir kişi daha eklenmeyecek**. Randevu zaten alınmış ve salı günü; gidip gitmeme kararı verilmeyecek.

**`#41`** — ⛔⛔ ÜRETİM NOTU — acil servis çıkışı, üç yıldır her gün alınan hap, ve küçümseme (*«ben içmedim bir kadehti»*). §5a″ md.2. ⛔ *«Mahalleye duyulursa»* korkusu bir utandırma fırsatına çevrilmeyecek. Kurum adı genelleştirilecek.

**`#43`** — ⚠️ ÜRETİM NOTU — iş teklifi geldi ve saat 03:25, masada açık şişe. *«Sevinmek mi korkmak mı»* — ikisinden biri seçilmeyecek.

**`#44`** — ⭐⭐ ÜRETİM NOTU — **karar anında**: ayakkabı giyilmiş, kapıya gidiyor, *«bu kapıyı çıkmadan bana iki cümle yaz»* diyor. ⛔ «Çıkma» denmeyecek (sonucunu taşımayacağım bir emir) ama boş da bırakılmayacak. İki sesi de kendisi yazmış; ikisi de ona ait.

**`#45`** — ⛔⛔ ÜRETİM NOTU — **kullanıcı hastanın kendisi DEĞİL**, kızı. Babasının ilaçlara erişimini soruyor ve bir güvenlik planı istiyor. ⛔ Plan VERİLMEYECEK — başkası adına ilaç erişimi klinik bir karar. Randevu tarihinin yordamsal olduğu söylenecek (parti2 `#59`) ve bakım verenin kendi yükü adlandırılacak. ⚠️ Bu, korpusta **üçüncü kişi adına** yazılan ilk kayıt.

**`#47`** — ⚠️ ÜRETİM NOTU — *«oğlum sayma seni»* + *«böyle bir oğul kim ister»*. Babanın haklı olup olmadığı tartışılmayacak; kendi *«haksızlık ediyor»* cümlesi de silinmeyecek.

**`#53`** — ⛔⛔⛔ ÜRETİM NOTU — **üç gündür ilacı kendi kesmiş** ve titreme, terleme, çarpıntı var; üstüne *«gitmeme gerek yok»* diyor. §5a″ md.1 ve md.2 birlikte. ⛔ Belirtiler adlandırılmayacak (yoksunluk demek teşhis olur) ama *«gerek yok»* cümlesi de onaylanmayacak.

**`#58`** — ⚠️ ÜRETİM NOTU — yatış önerilmiş, hasta çıkıp gitmiş, *«beni kilitleyecekler, deli gibi»* diyor. ⛔ Yatış ne savunulacak ne reddedilecek; karşılanacak şey damga ve korku. Kurum adı genelleştirilecek.

## ⛔ Bu taramanın söylemedikleri

| | |
|---|---|
| ⛔⛔ **«0 eleme» süzgeçlerin temiz olduğunu göstermez** | T192 tam tersini ölçtü: dördü de temiz derken kaçırmışlardı. Buradaki güvence süzgeç değil, **on dört metnin okunmuş olması** |
| ⛔ **Okuma BENİM okumam** | K30 gereği üretimi ben yapıyorum ve hükümleri de ben veriyorum; uzman okuması değil |
| ⛔ **`gd-021` açık** | çıplak *«İntihar düşüncesi»* sınıfı bu partiye düşmedi (havuzda 6 var); karar hâlâ verilmedi |
| ⚠️ **Yalnız tohum metni okundu** | üretilecek konuşmanın kendisi üretim anında ayrıca kapılardan geçer |
