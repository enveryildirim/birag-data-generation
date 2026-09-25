# Şablonlaşma kapısı — kalıplar sayılarak bulundu

**Betik:** `scripts/analiz/2026-09-18-sablon-kapisi.py` (yazıldı 2026-09-18) · **koşu tarihi:** 2026-09-20  
**Girdi:** `data/candidates/v6-parti2.jsonl` · SHA256-16 `4f65ece0ba019105` · **59** kayıt  
**Eşik:** bir dizi en az **%2.0** (2 kayıt) içinde geçmeli

⛔⛔ **T139'un açık kalemi.** T139 şablonlaşmayı ölçmüştü ama kalıpları **elle**
yazmıştı ve şerh düşmüştü: *«sayı ALT SINIRDIR; sözlükte olmayan şablonlar
görünmez»*. Burada liste **yazılmıyor, çıkarılıyor**: asistan cevaplarındaki
bütün 5–10 sözcüklük diziler sayılıyor.

⚠️ **Bu bir SAYIM kapısıdır.** *«Şablon = kusur»* değildir — tekrarlanan bir cümle
doğru da olabilir. Kapı hiçbir kaydı düşürmez.

## 1. ⭐ Eşiği aşan diziler — **39**

| kayıt | % | uzunluk | dizi |
|---:|---:|---:|---|
| 4 | %6.8 | 4 | *«yaziyor sorduğun şeyin cevabi»* |
| 4 | %6.8 | 3 | *«başka bir şey»* |
| 4 | %6.8 | 3 | *«kişinin kendi başvurusuyla»* |
| 3 | %5.1 | 7 | *«ve randevunun kişinin kendi başvurusuyla oluşturulduğu yaziyor»* |
| 3 | %5.1 | 6 | *«paylaşilmadiği yaziyor sorduğun şeyin cevabi orada»* |
| 3 | %5.1 | 4 | *«bir hekimin bilmesi gerekiyor»* |
| 3 | %5.1 | 3 | *«ne yapacağin sana»* |
| 3 | %5.1 | 3 | *«yaziyor sorunun cevabi»* |
| 3 | %5.1 | 3 | *«hakkinda bir şey»* |
| 3 | %5.1 | 3 | *«sorunun cevabi evet»* |
| 2 | %3.4 | 9 | *«ve randevunun kişinin kendi başvurusuyla oluşturulduğu yaziyor sorunun cevabi»* |
| 2 | %3.4 | 8 | *«alindiği ve randevunun kişinin kendi başvurusuyla oluşturulduğu yaziyor»* |
| 2 | %3.4 | 5 | *«bunu bir hekimin bilmesi gerekiyor»* |
| 2 | %3.4 | 4 | *«bir de şu var»* |
| 2 | %3.4 | 4 | *«yaziyor yani sorunun cevabi»* |
| 2 | %3.4 | 4 | *«ne yapacağin sana ait»* |
| 2 | %3.4 | 4 | *«yaziyor sorunun cevabi evet»* |
| 2 | %3.4 | 4 | *«seninle ayni fikirde değilim»* |
| 2 | %3.4 | 4 | *«notta görüşmelerin kişinin kendi»* |
| 2 | %3.4 | 4 | *«hakkinda bir şey söyleyemem»* |
| 2 | %3.4 | 3 | *«sorularin görüşmede alindiği»* |
| 2 | %3.4 | 3 | *«de sen söyledin»* |
| 2 | %3.4 | 3 | *«işe yarayacağini bilmiyorum»* |
| 2 | %3.4 | 3 | *«bilmiyorum ve tahmin»* |
| 2 | %3.4 | 3 | *«getiren ne oldu»* |
| 2 | %3.4 | 3 | *«ayni şey değil»* |
| 2 | %3.4 | 3 | *«bir şey değil»* |
| 2 | %3.4 | 3 | *«bir şey ve»* |
| 2 | %3.4 | 3 | *«bunun için çalişiyor»* |
| 2 | %3.4 | 3 | *«ve şimdi o»* |
| … | | | 9 dizi daha (JSON'da tamamı) |

## 2. ⭐ Sürümler boyunca büyüme

T139: *«her yeni kural, bir sonraki şablonun tohumu»*. En yaygın beş dizinin
sürümler boyunca **kayıt payı**:

| dizi | v0.0.1 | v0.0.2 | v0.0.3 | v0.0.4 | v0.0.5 | v0.0.6 | v0.0.7 | v0.0.8 | v0.0.9 | v0.0.10 | v0.0.11 | v0.0.12 | v0.0.13 | v0.0.14 | candidates |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| *«yaziyor sorduğun şeyin cevabi»* | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %6.8 |
| *«başka bir şey»* | %15.0 | %3.4 | %2.6 | %2.6 | %2.6 | %3.3 | %2.9 | %4.2 | %4.2 | %4.2 | %4.2 | %4.2 | %4.2 | %4.2 | %6.8 |
| *«kişinin kendi başvurusuyla»* | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %6.8 |
| *«ve randevunun kişinin kendi başvurusuyla oluşturulduğu yaz»* | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %5.1 |
| *«paylaşilmadiği yaziyor sorduğun şeyin cevabi orada»* | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %5.1 |

## 3. ⭐⭐ Eşik duyarlılığı

⛔ *«%2»* bir SEÇİMDİR, ölçüm değil. Seçimin sonucu ne kadar belirlediği
gösterilmeden sayı okunamaz:

| eşik | kayıt | eşiği aşan dizi |
|---|---:|---:|
| %1.0 | 2 | 39 |
| %2.0 | 2 | 39 |
| %3.0 | 2 | 39 |
| %5.0 | 3 | 10 |

## 4. ⭐⭐ T139'un elle listesi ne kadar alt sınırdı?

T139 beş kalıbı **elle** yazmış ve şerh düşmüştü: *«sayı ALT SINIRDIR»*.
Şerh doğruydu ve şimdi ölçülebiliyor:

⛔ Ham fark yanıltıcı olurdu: eşiği aşan dizilerin bir kısmı **doğal Türkçe**
(*«başka bir şey»*). ⇒ En yaygın **22** dizi elle sınıflandırıldı ve iddia
yalnız sınıflandırılmış veriye dayanıyor.

| | |
|---|---:|
| kapının eşiği aşan dizisi | 39 |
| elle sınıflandırılan | **2** |
| · kural kaynaklı **formül** | **1** |
| · doğal Türkçe | 1 |
| ⛔ **formül olup T139'un listesinde OLMAYAN** | **1** |

| dizi | kayıt | sınıf | T139'da |
|---|---:|---|---|
| *«başka bir şey»* | 4 | doğal dil | ⛔ **yok** |
| *«ayni şey değil»* | 2 | kural formülü | ⛔ **yok** |

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
