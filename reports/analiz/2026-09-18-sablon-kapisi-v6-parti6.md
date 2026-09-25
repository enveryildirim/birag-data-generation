# Şablonlaşma kapısı — kalıplar sayılarak bulundu

**Betik:** `scripts/analiz/2026-09-18-sablon-kapisi.py` (yazıldı 2026-09-18) · **koşu tarihi:** 2026-09-21  
**Girdi:** `data/candidates/v6-parti6.jsonl` · SHA256-16 `23186319a6b008b1` · **58** kayıt  
**Eşik:** bir dizi en az **%2.0** (2 kayıt) içinde geçmeli

⛔⛔ **T139'un açık kalemi.** T139 şablonlaşmayı ölçmüştü ama kalıpları **elle**
yazmıştı ve şerh düşmüştü: *«sayı ALT SINIRDIR; sözlükte olmayan şablonlar
görünmez»*. Burada liste **yazılmıyor, çıkarılıyor**: asistan cevaplarındaki
bütün 5–10 sözcüklük diziler sayılıyor.

⚠️ **Bu bir SAYIM kapısıdır.** *«Şablon = kusur»* değildir — tekrarlanan bir cümle
doğru da olabilir. Kapı hiçbir kaydı düşürmez.

## 1. ⭐ Eşiği aşan diziler — **65**

| kayıt | % | uzunluk | dizi |
|---:|---:|---:|---|
| 5 | %8.6 | 3 | *«bir şey değil»* |
| 5 | %8.6 | 3 | *«ikisini de sen»* |
| 4 | %6.9 | 3 | *«buradan çikacak bir»* |
| 3 | %5.2 | 3 | *«ve ikisi de»* |
| 3 | %5.2 | 3 | *«kişi ben değilim»* |
| 3 | %5.2 | 3 | *«ikisi de ayni»* |
| 3 | %5.2 | 3 | *«o hapi yazan»* |
| 3 | %5.2 | 3 | *«üçünü de sen»* |
| 3 | %5.2 | 3 | *«üçü de ayni»* |
| 3 | %5.2 | 3 | *«hakli olup olmadiğina»* |
| 3 | %5.2 | 3 | *«de sen yazdin»* |
| 3 | %5.2 | 3 | *«bir şey yok»* |
| 3 | %5.2 | 3 | *«bir de şu»* |
| 2 | %3.4 | 4 | *«orada seni nasil karşilayacaklarini»* |
| 2 | %3.4 | 4 | *«ve üçünü de sen»* |
| 2 | %3.4 | 4 | *«olup olmadiğina da girmiyorum»* |
| 2 | %3.4 | 4 | *«ikisini de sen yazdin»* |
| 2 | %3.4 | 4 | *«ve ikisini de sen»* |
| 2 | %3.4 | 4 | *«hakli olup olmadiğina girmiyorum»* |
| 2 | %3.4 | 4 | *«ve buradan çikacak bir»* |
| 2 | %3.4 | 4 | *«ama cümlenin kuruluşuna bakiyorum»* |
| 2 | %3.4 | 4 | *«ve o ben değilim»* |
| 2 | %3.4 | 3 | *«aklindan ne geçiyordu»* |
| 2 | %3.4 | 3 | *«şu an iki»* |
| 2 | %3.4 | 3 | *«ilk ne zaman»* |
| 2 | %3.4 | 3 | *«bir şey duruyor»* |
| 2 | %3.4 | 3 | *«ikisi arasinda bir»* |
| 2 | %3.4 | 3 | *«diye soran da»* |
| 2 | %3.4 | 3 | *«bilmediğim bir şeyi»* |
| 2 | %3.4 | 3 | *«sen yan yana»* |
| … | | | 35 dizi daha (JSON'da tamamı) |

## 2. ⭐ Sürümler boyunca büyüme

T139: *«her yeni kural, bir sonraki şablonun tohumu»*. En yaygın beş dizinin
sürümler boyunca **kayıt payı**:

| dizi | v0.0.1 | v0.0.2 | v0.0.3 | v0.0.4 | v0.0.5 | v0.0.6 | v0.0.7 | v0.0.8 | v0.0.9 | v0.0.10 | v0.0.11 | v0.0.12 | v0.0.13 | v0.0.14 | candidates |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| *«bir şey değil»* | %0.0 | %4.3 | %3.2 | %3.2 | %3.2 | %2.3 | %2.9 | %2.5 | %2.5 | %2.5 | %2.5 | %2.5 | %2.5 | %2.5 | %10.3 |
| *«ikisini de sen»* | %0.0 | %0.9 | %0.6 | %0.6 | %0.6 | %0.5 | %0.4 | %2.5 | %2.5 | %2.5 | %2.5 | %2.5 | %2.5 | %2.5 | %8.6 |
| *«buradan çikacak bir»* | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %1.1 | %1.1 | %1.1 | %1.1 | %1.1 | %1.1 | %1.1 | %6.9 |
| *«ve ikisi de»* | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.4 | %1.1 | %1.1 | %1.1 | %1.1 | %1.1 | %1.1 | %1.1 | %5.2 |
| *«kişi ben değilim»* | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.5 | %0.5 | %0.5 | %0.5 | %0.5 | %0.5 | %0.5 | %5.2 |

## 3. ⭐⭐ Eşik duyarlılığı

⛔ *«%2»* bir SEÇİMDİR, ölçüm değil. Seçimin sonucu ne kadar belirlediği
gösterilmeden sayı okunamaz:

| eşik | kayıt | eşiği aşan dizi |
|---|---:|---:|
| %1.0 | 2 | 65 |
| %2.0 | 2 | 65 |
| %3.0 | 2 | 65 |
| %5.0 | 3 | 13 |

## 4. ⭐⭐ T139'un elle listesi ne kadar alt sınırdı?

T139 beş kalıbı **elle** yazmış ve şerh düşmüştü: *«sayı ALT SINIRDIR»*.
Şerh doğruydu ve şimdi ölçülebiliyor:

⛔ Ham fark yanıltıcı olurdu: eşiği aşan dizilerin bir kısmı **doğal Türkçe**
(*«başka bir şey»*). ⇒ En yaygın **22** dizi elle sınıflandırıldı ve iddia
yalnız sınıflandırılmış veriye dayanıyor.

| | |
|---|---:|
| kapının eşiği aşan dizisi | 65 |
| elle sınıflandırılan | **2** |
| · kural kaynaklı **formül** | **0** |
| · doğal Türkçe | 2 |
| ⛔ **formül olup T139'un listesinde OLMAYAN** | **0** |

| dizi | kayıt | sınıf | T139'da |
|---|---:|---|---|
| *«başka bir şey»* | 2 | doğal dil | ⛔ **yok** |
| *«bir şey var»* | 2 | doğal dil | ⛔ **yok** |

⛔⛔ **Ve kaçan, korpusun en büyük ikinci kalıbı:** *«bugüne kadar söylediklerin
şunlar»* — **43 kayıt (%7,5)**, yani T139'un listesindeki beş kalıbın üçünden
daha yaygın. Elle yazılmış bir listede yoktu ve hiçbir yerde sayılmamıştı.

➡️⭐⭐⭐ *Bir olguyu elle yazılmış bir listeyle ölçmek, olgunun ancak AKLA GELEN
kısmını ölçer. «Alt sınır» şerhi dürüsttür ama ne kadar alt olduğunu söylemez —
onu ancak listesiz bir sayım söyler.*

## ⛔ Bu kapının söylemedikleri

| | |
|---|---|
| ⛔ **Kusur demiyor** | tekrarlanan bir cümle doğru da olabilir; ölçülen şey TEKRAR. Hangi şablonun kusur olduğunu **elle okuma** söyler |
| ⛔ **Doğal dil ile şablon ayrılmıyor** | *«bir şey olup olmadığını»* gibi diziler de eşiği aşabilir; uzunluk sütunu bu yüzden tabloda |
| ⛔ **Eşik seçimi sonucu belirliyor** | §3 duyarlılığı gösteriyor ama doğru eşiği söylemiyor |
| ⚠️ **Yalnız asistan cevabı** | `thinking` kapsam dışı; orada tekrar çok daha yoğun ve ayrı bir soru |
| ⛔ **Eleme yok** | kapı bir kaydı düşürmez; T139'un istediği denetim bu, ama denetimin SONUCUNU kullanan bir süreç henüz yok |
| ⛔ **İç içe geçme tam çözülmedi** | *«ne olduğunu ben»* (19) ve *«ne olduğunu ben söyleyemem»* (18) ayrı sayılıyor çünkü kapsamları FARKLI; aynı ailedendirler ve liste bu yüzden gerçek şablon sayısından uzun |
| ⛔ **Sınıflandırma elle** | hangi dizinin kural kaynaklı FORMÜL, hangisinin doğal Türkçe olduğunu (*«başka bir şey»*) kapı söylemiyor |
