# Şablonlaşma kapısı — kalıplar sayılarak bulundu

**Betik:** `scripts/analiz/2026-09-18-sablon-kapisi.py` (yazıldı 2026-09-18) · **koşu tarihi:** 2026-09-20  
**Girdi:** `data/candidates/v6-parti3.jsonl` · SHA256-16 `d2ed7c00def24afc` · **60** kayıt  
**Eşik:** bir dizi en az **%2.0** (2 kayıt) içinde geçmeli

⛔⛔ **T139'un açık kalemi.** T139 şablonlaşmayı ölçmüştü ama kalıpları **elle**
yazmıştı ve şerh düşmüştü: *«sayı ALT SINIRDIR; sözlükte olmayan şablonlar
görünmez»*. Burada liste **yazılmıyor, çıkarılıyor**: asistan cevaplarındaki
bütün 5–10 sözcüklük diziler sayılıyor.

⚠️ **Bu bir SAYIM kapısıdır.** *«Şablon = kusur»* değildir — tekrarlanan bir cümle
doğru da olabilir. Kapı hiçbir kaydı düşürmez.

## 1. ⭐ Eşiği aşan diziler — **46**

| kayıt | % | uzunluk | dizi |
|---:|---:|---:|---|
| 4 | %6.7 | 3 | *«bir şey değil»* |
| 3 | %5.0 | 3 | *«başka bir şey»* |
| 3 | %5.0 | 3 | *«üçünü de sen»* |
| 3 | %5.0 | 3 | *«olan bir hekim»* |
| 3 | %5.0 | 3 | *«bir şeyi de»* |
| 3 | %5.0 | 3 | *«bir not var»* |
| 3 | %5.0 | 3 | *«olup olmadiğina bakamam»* |
| 3 | %5.0 | 3 | *«karar vermek benim»* |
| 2 | %3.3 | 6 | *«söyleyemem ve tahmin de etmem bu»* |
| 2 | %3.3 | 5 | *«bunu ben söylemedim sen söyledin»* |
| 2 | %3.3 | 5 | *«bu ilaci yazan hekimin işi»* |
| 2 | %3.3 | 5 | *«anlatan kisa bir not var»* |
| 2 | %3.3 | 5 | *«şeyin doğru olup olmadiğina bakamam»* |
| 2 | %3.3 | 5 | *«şu an elinde şunlar var»* |
| 2 | %3.3 | 5 | *«karar vermek benim işim değil»* |
| 2 | %3.3 | 4 | *«üçünü de sen siraladin»* |
| 2 | %3.3 | 4 | *«ikisini de sen yazdin»* |
| 2 | %3.3 | 4 | *«bir not var onu»* |
| 2 | %3.3 | 4 | *«olup olmadiğina bakamam ama»* |
| 2 | %3.3 | 4 | *«olduğuna karar vermek benim»* |
| 2 | %3.3 | 3 | *«bir şey ve»* |
| 2 | %3.3 | 3 | *«gidip gitmemek senin»* |
| 2 | %3.3 | 3 | *«ben de bilmiyorum»* |
| 2 | %3.3 | 3 | *«bir şey oldu»* |
| 2 | %3.3 | 3 | *«üçü de ayni»* |
| 2 | %3.3 | 3 | *«sen fark etmişsin»* |
| 2 | %3.3 | 3 | *«ama bir şeyi»* |
| 2 | %3.3 | 3 | *«aklindan ne geçiyor»* |
| 2 | %3.3 | 3 | *«yok orada yalniz»* |
| 2 | %3.3 | 3 | *«ayri bir mesele»* |
| … | | | 16 dizi daha (JSON'da tamamı) |

## 2. ⭐ Sürümler boyunca büyüme

T139: *«her yeni kural, bir sonraki şablonun tohumu»*. En yaygın beş dizinin
sürümler boyunca **kayıt payı**:

| dizi | v0.0.1 | v0.0.2 | v0.0.3 | v0.0.4 | v0.0.5 | v0.0.6 | v0.0.7 | v0.0.8 | v0.0.9 | v0.0.10 | v0.0.11 | v0.0.12 | v0.0.13 | v0.0.14 | candidates |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| *«bir şey değil»* | %0.0 | %4.3 | %3.2 | %3.2 | %3.2 | %2.3 | %2.9 | %2.5 | %2.5 | %2.5 | %2.5 | %2.5 | %2.5 | %2.5 | %6.7 |
| *«başka bir şey»* | %15.0 | %3.4 | %2.6 | %2.6 | %2.6 | %3.3 | %2.9 | %4.2 | %4.2 | %4.2 | %4.2 | %4.2 | %4.2 | %4.2 | %5.0 |
| *«üçünü de sen»* | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.7 | %1.4 | %1.4 | %1.4 | %1.4 | %1.4 | %1.4 | %1.4 | %5.0 |
| *«olan bir hekim»* | %0.0 | %1.7 | %1.3 | %1.9 | %3.2 | %2.3 | %1.8 | %0.9 | %1.1 | %1.1 | %1.1 | %1.1 | %1.1 | %1.1 | %5.0 |
| *«bir şeyi de»* | %0.0 | %0.0 | %0.6 | %0.6 | %0.6 | %0.5 | %0.7 | %1.2 | %1.2 | %1.2 | %1.2 | %1.2 | %1.2 | %1.2 | %5.0 |

## 3. ⭐⭐ Eşik duyarlılığı

⛔ *«%2»* bir SEÇİMDİR, ölçüm değil. Seçimin sonucu ne kadar belirlediği
gösterilmeden sayı okunamaz:

| eşik | kayıt | eşiği aşan dizi |
|---|---:|---:|
| %1.0 | 2 | 46 |
| %2.0 | 2 | 46 |
| %3.0 | 2 | 46 |
| %5.0 | 3 | 8 |

## 4. ⭐⭐ T139'un elle listesi ne kadar alt sınırdı?

T139 beş kalıbı **elle** yazmış ve şerh düşmüştü: *«sayı ALT SINIRDIR»*.
Şerh doğruydu ve şimdi ölçülebiliyor:

⛔ Ham fark yanıltıcı olurdu: eşiği aşan dizilerin bir kısmı **doğal Türkçe**
(*«başka bir şey»*). ⇒ En yaygın **22** dizi elle sınıflandırıldı ve iddia
yalnız sınıflandırılmış veriye dayanıyor.

| | |
|---|---:|
| kapının eşiği aşan dizisi | 46 |
| elle sınıflandırılan | **3** |
| · kural kaynaklı **formül** | **1** |
| · doğal Türkçe | 2 |
| ⛔ **formül olup T139'un listesinde OLMAYAN** | **1** |

| dizi | kayıt | sınıf | T139'da |
|---|---:|---|---|
| *«başka bir şey»* | 3 | doğal dil | ⛔ **yok** |
| *«ben karar veremem»* | 2 | kural formülü | ⛔ **yok** |
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
