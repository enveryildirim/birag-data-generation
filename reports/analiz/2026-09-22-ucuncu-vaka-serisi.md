# Üçüncü vaka serisi — «kural yazılı, KAPI YOK»

**Betik:** `scripts/analiz/2026-09-22-ucuncu-vaka-serisi.py` · **Tarih:** 2026-09-22  
**Seri satırı:** 10 · **belgelenmiş vaka:** 13  

⭐ **Alma ölçütü (önce yazıldı):** kural yazılıydı · onu uygulayan kod ya da ölçen rapor satırı yoktu (ya da hiç koşmuyordu) · ihlal sessizce geçti veya *«denetlendi»* ile *«denetlenmedi»* ayırt edilemez oldu · eksikliği başka bir iş ortaya çıkardı.

⛔⛔ **Üçlünün tamamlayıcısı** — aynı kusur üç ayrı yerde durabiliyor:

| seri | kapı | kusur nerede |
|---|---|---|
| T22 | **var**, yanlış ateşliyor | kapının **hükmünde** |
| T236 | **var**, hiç göremiyor | kapının **baktığı şeyde** |
| ⭐ **bu seri** | **yok** | kapının **varlığında** |

## Seri

| # | kayıt | yazılı kural | kapı neden yoktu | biçim | nasıl bulundu | sonra ne oldu | üye |
|---:|---|---|---|---|---|---|---:|
| 1 | K66 | dört ayrı kural: thinking 4x tavanı · §5a-§3b hedefleri · özerklik vurgusu · `ELENEN_GUVENLIK` sözlüğü | dördü de **yazıldı ve orada bırakıldı**; hiçbiri aynı commit'te koda ya da rapora bağlanmadı | kod hiç yazılmadı | ölçüm (3) + gözden geçirme (1) | ⭐ kalıp **adlandırıldı** ve kural oldu: *bir sınır yazıldığında aynı commit'te onu uygulayan kod ya da ölçen rapor satırı da yazılır* | **4** |
| 2 | K84 | *«rapor üreticisinde hiçbir hüküm cümlesi sabit yazılmaz»* (K80'de yazılmıştı) | kuralı denetleyen bir şey yoktu ⇒ **aynı kişi aynı gün ikinci betikte tekrarladı**; tablo *«3+ turlu 14»* derken metin *«istenilen derinlikte kayıt yok»* diyordu | kural insan için yazılı, sınama için değil | raporu okuma | kural yazıldı; ⛔ denetimi hâlâ okumaya bağlı | 1 |
| 3 | T35 | `safety_crisis`'in her öğesi **üç** `tip: judge` iddiası taşıyor (`rol_siniri_ihlali` · `bos_guvence` · `tuzak_suclama`) | üç taramada da *«denetlenemedi»* kaldı — iddia yazılıydı, onu soran hiçbir koşu yoktu | ⛔ iddia hiç denetlenmedi | ölçüm (üçü taramaya eklenerek) | ⭐ eksikliğin **yansız olmadığı** ölçüldü: ölçülmeyen eksen hangi taraftaysa orayı kayırıyor | 1 |
| 4 | T57 | **Kural 7** — *«bir sayı raporlanıyorsa nasıl ölçüldüğü yazılı olmalı»* | ⭐⭐ kural *«yazılı»*yı denetliyordu ama **iki ayrı şey** var: İNSAN için yazılı ve SINAMA için yazılı. 7 betiğin argümanları rapor başlığında ilan edilmişti — insan okuyup koşabilir, sınama koşamaz | kural insan için yazılı, sınama için değil | Kural 7 denetimi (T54 izi) | ⛔ ayrım adlandırıldı; kuralın kendisi değişmedi | 1 |
| 5 | T82 | `plan.md`: *«B-derin 3 öğede 1024 token'ı thinking içinde tüketip cevabı boş bıraktı»* | olgu belgede yazılıydı, **eval tarafında kapı yoktu** | kod hiç yazılmadı | arşivi sayma | ⭐ 3226 kaydın **183'ü** dejenere çıktı — ve tek kusur değil ÜÇ kusurdu (`uretim_yok` 133 · `bos_cevap` 41 · `tekrar` 48) | 1 |
| 6 | T121 | *«klinik güvenlik ihlali taşıyan kayıt korpusa giremez»* — `build.py`'nin **tek** otomatik güvenlik kapısı | ⛔⛔ kapı `if jr and jr.get("klinik_guvenlik_ihlali")` yazıyordu: `judge` alanı **NULL** olan kayıt koşulun ilk yarısında düşüyor ve **kabul ediliyordu** ⇒ *«denetlendi ve temiz»* ile *«hiç denetlenmedi»* aynı kapıdan geçiyordu | kapı vardı, kapsamı sessizce boştu | kapı koşulunu okuma | ⛔ v0.0.8 için hazırlanan **300 yargılanmamış kayıt** derlenseydi klinik kapı hiçbirinde koşmamış olacaktı | 1 |
| 7 | T139 | *«şablonlaşma korpusun kalitesini düşürür»* — §5a⁗ ve öncesi | kalıpları yakalayan **hiçbir alan yoktu**; `klise_acilis` yalnız *kabul* cümlelerini soruyor | kod hiç yazılmadı | judge'ın düştüğü not + ölçüm | ⭐⭐ kapı yazıldı (K193) ve **elle yazılan liste 13 kalıp kaçırmış** çıktı — korpusun en büyük ikinci kalıbı listede yoktu (%7,5) | 1 |
| 8 | T145 | *«çapa doğru cevabı düşürmemeli»* — `kacamak-kapisi`'nin OLUMLU sınaması | sınama vardı ve doğruydu, ama `if o["id"] not in DOGRU: continue` satırı ögelerin **%70'ini sessizce atlıyordu**; en kötü dağılım **sert** kapıda | kapı vardı, kapsamı sessizce daraldı | sınama betiğini okuma | ⛔ *«yanlış pozitif üretmiyor»* iddiası bu ögelerde **hiç sınanmamış** çıktı | 1 |
| 9 | T209 | iki cümle ailesinin oranı tavanı aşmamalı | parti3'te kural **yalnız talimatta** duruyordu; talimat dikkat kaymasına karşı işe yaramadı (itiraz %2→%8→**%20**, fark etme %3→%3→**%18**) | kod hiç yazılmadı | parti oranlarını ölçme | ⭐⭐⭐ **ÇARE ÖLÇÜLDÜ:** parti4'te aynı kural blok kapısına kondu (tavan %10, aşarsa **reddeder**) ⇒ talimat ve kapı **aynı kural üzerinde** yan yana kondu | 1 |
| 10 | T213 | *«planın her satırı üretimden önce okunur»* | ön tarama yalnız **işaretlediği** satırı okutuyordu; işaretlemediği satır üretim anına kadar hiç okunmuyordu | kapı vardı, kapsamı sessizce daraldı | üretim anında okuma | ⛔ `v6-parti5`'in **en ağır iki satırı** (`#33` emziren anne + md.2, `#39` el titremesi) işaretlenmemişti ⇒ kural *«her satır okunur»* oldu | 1 |

## Eksikliğin biçimi

| biçim | vaka |
|---|---:|
| kod hiç yazılmadı | 7 |
| kural insan için yazılı, sınama için değil | 2 |
| kapı vardı, kapsamı sessizce daraldı | 2 |
| ⛔ iddia hiç denetlenmedi | 1 |
| kapı vardı, kapsamı sessizce boştu | 1 |

⭐⭐ **İkisi aynı ağırlıkta değil.** *«Kod hiç yazılmadı»* görünür bir boşluktur: kimse *«bu denetlendi»* demiyor. ⛔⛔ *«Kapsamı sessizce daraldı»* ise **daha tehlikelidir** — kapı vardır, koşar, rapor *«geçti»* yazar, ama o satırlarda hiç bakmamıştır. `T121` bunun en saf hâli: kapı `NULL` yargıyı **kabul** ediyordu ⇒ *«denetlendi ve temiz»* ile *«hiç denetlenmedi»* aynı çıktıyı veriyordu.

## Bunları ne buldu

⛔ Sınıflar **elle** yazıldı, dizge eşlemesiyle değil — ilk sürümde `"okuma" in metin` karma bir vakayı okuma saymıştı. Satır bazındaki ayrıntı yukarıdaki tabloda duruyor.

| bulan | satır |
|---|---:|
| okuma | 4 |
| ölçüm | 3 |
| karma | 2 |
| denetim | 1 |

⭐⭐⭐ **10 satırın 4'ü doğrudan bir OKUMAYLA çıktı** (raporu okuma, kapı koşulunu okuma, sınama betiğini okuma, üretim anında satır okuma), ikisi de okuma+ölçüm karması. Kalanları ölçüm ve bir denetim buldu — ama **hiçbirini bir kapı bulmadı**, çünkü eksik olan şey zaten kapının kendisiydi. ⛔ Bu, serinin kurucu döngüsü: *var olmayan kapıyı var olmayan kapı bulamaz.*

## ⭐⭐⭐ Bu serinin ötekilerde olmayan şeyi: çare ölçüldü

T209 aynı kuralı **iki partide yan yana** koydu:

| | parti3 | parti4 |
|---|---|---|
| kural nerede | **yalnız talimatta** | **blok kapısında** |
| itiraz ailesi | %2 → %8 → **%20** | tavan %10, aşarsa **reddedilir** |
| fark etme ailesi | %3 → %3 → **%18** | — |

➡️⭐⭐⭐ *Bir kuralın ihlali ancak iş bittikten sonra görünüyorsa hatırlatma yetmez, kapı gerekir. Talimat dikkat kaymasına karşı korumaz; korpus büyüdükçe ihlal oranı artar, çünkü talimat yazarın belleğine, kapı ise koşuya bağlıdır.*

⭐ K66'nın kuralı bu serinin tek cümlelik özeti: **bir sınır, hedef ya da eleme yazıldığında aynı commit'te (a) onu uygulayan kod ya da (b) onu ölçen rapor satırı da yazılır.**

## ⛔ Hâlâ açık olan

| | |
|---|---|
| ⛔⛔ **`T121`'in canlı örneği bugüne kadar sürdü** | 370 kayıt yargılanmamıştı; `build.py`'nin kapısı onarıldı ama derleme o kayıtlarla yapılsaydı klinik kapı hiçbirinde koşmayacaktı |
| ⛔ **`T35` kapanmadı** | üç `tip: judge` iddiası ölçüldü, ama denetimleri sürekli bir kapıya bağlanmadı |
| ⚠️ **`T57` bir AYRIM, çare değil** | *«sınama için yazılı»* ölçütü adlandırıldı; Kural 7 hâlâ *«insan için yazılı»*yı ölçüyor |

## ⛔ Bu serinin söylemedikleri

| | |
|---|---|
| ⛔⛔ **ALT SINIR** | yalnız yakalanmış vakalar; **yazılıp hiç bağlanmamış ve hâlâ fark edilmemiş** kuralların sayısı tanımı gereği bilinemez ⇒ bu seri üçünün içinde **en eksik olanı** |
| ⛔⛔ **Derleyen benim (K30)** | ölçüt yazılı, uygulaması benim |
| ⛔ **T209 tek deney** | talimat↔kapı karşılaştırması bir kural ve iki parti üzerinde; yinelenmedi ⇒ *«kapı hep daha iyidir»* genellemesi bu tek karşılaştırmadan çıkarılamaz |
| ⚠️ **Kapı yazmanın MALİYETİ ölçülmedi** | her kural bir kapı olursa kapı sayısı artar ve T22 serisi **kapıların da yanıldığını** gösteriyor ⇒ *«her kurala kapı»* ücretsiz değil |
