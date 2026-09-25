# Şablonlaşma kapısı — kalıplar sayılarak bulundu

**Betik:** `scripts/analiz/2026-09-18-sablon-kapisi.py` (yazıldı 2026-09-18) · **koşu tarihi:** 2026-09-21  
**Girdi:** `data/candidates/v6-parti5.jsonl` · SHA256-16 `21a6a72faf0435fb` · **60** kayıt  
**Eşik:** bir dizi en az **%2.0** (2 kayıt) içinde geçmeli

⛔⛔ **T139'un açık kalemi.** T139 şablonlaşmayı ölçmüştü ama kalıpları **elle**
yazmıştı ve şerh düşmüştü: *«sayı ALT SINIRDIR; sözlükte olmayan şablonlar
görünmez»*. Burada liste **yazılmıyor, çıkarılıyor**: asistan cevaplarındaki
bütün 5–10 sözcüklük diziler sayılıyor.

⚠️ **Bu bir SAYIM kapısıdır.** *«Şablon = kusur»* değildir — tekrarlanan bir cümle
doğru da olabilir. Kapı hiçbir kaydı düşürmez.

## 1. ⭐ Eşiği aşan diziler — **44**

| kayıt | % | uzunluk | dizi |
|---:|---:|---:|---|
| 7 | %11.7 | 3 | *«bir şey var»* |
| 5 | %8.3 | 3 | *«ve ikisi de»* |
| 4 | %6.7 | 3 | *«bir şey değil»* |
| 3 | %5.0 | 3 | *«bir şeyi de»* |
| 3 | %5.0 | 3 | *«ikisini de sen»* |
| 3 | %5.0 | 3 | *«gereken bir şey»* |
| 3 | %5.0 | 3 | *«de sen yazdin»* |
| 3 | %5.0 | 3 | *«olan ben değilim»* |
| 3 | %5.0 | 3 | *«var ve onu»* |
| 2 | %3.3 | 5 | *«olup olmadiğini sana ben söyleyemem»* |
| 2 | %3.3 | 5 | *«ve bakabilecek olan ben değilim»* |
| 2 | %3.3 | 5 | *«bir şey var ve onu»* |
| 2 | %3.3 | 4 | *«bir yerde de katilmiyorum»* |
| 2 | %3.3 | 4 | *«bir şey var mi»* |
| 2 | %3.3 | 4 | *«ve ikisini de sen»* |
| 2 | %3.3 | 4 | *«bilmesi gereken bir şey»* |
| 2 | %3.3 | 4 | *«var ve onu sen»* |
| 2 | %3.3 | 3 | *«açarim sen söyle»* |
| 2 | %3.3 | 3 | *«dair bir hüküm»* |
| 2 | %3.3 | 3 | *«di mi diye»* |
| 2 | %3.3 | 3 | *«ve sen onlari»* |
| 2 | %3.3 | 3 | *«ikisi ayni anda»* |
| 2 | %3.3 | 3 | *«senin yerine kuramam»* |
| 2 | %3.3 | 3 | *«yan yana duruyor»* |
| 2 | %3.3 | 3 | *«sen onu bir»* |
| 2 | %3.3 | 3 | *«hanginizin hakli olduğunu»* |
| 2 | %3.3 | 3 | *«ilgisi olmayan bir»* |
| 2 | %3.3 | 3 | *«sorusunun cevabi da»* |
| 2 | %3.3 | 3 | *«elinde ne var»* |
| 2 | %3.3 | 3 | *«bilmiyorum bilseydim de»* |
| … | | | 14 dizi daha (JSON'da tamamı) |

## 2. ⭐ Sürümler boyunca büyüme

T139: *«her yeni kural, bir sonraki şablonun tohumu»*. En yaygın beş dizinin
sürümler boyunca **kayıt payı**:

| dizi | v0.0.1 | v0.0.2 | v0.0.3 | v0.0.4 | v0.0.5 | v0.0.6 | v0.0.7 | v0.0.8 | v0.0.9 | v0.0.10 | v0.0.11 | v0.0.12 | v0.0.13 | v0.0.14 | candidates |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| *«bir şey var»* | %0.0 | %1.7 | %3.9 | %3.9 | %3.9 | %3.7 | %3.3 | %3.3 | %3.3 | %3.3 | %3.3 | %3.3 | %3.3 | %3.3 | %11.7 |
| *«ve ikisi de»* | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.4 | %1.1 | %1.1 | %1.1 | %1.1 | %1.1 | %1.1 | %1.1 | %8.3 |
| *«bir şey değil»* | %0.0 | %4.3 | %3.2 | %3.2 | %3.2 | %2.3 | %2.9 | %2.5 | %2.5 | %2.5 | %2.5 | %2.5 | %2.5 | %2.5 | %6.7 |
| *«bir şeyi de»* | %0.0 | %0.0 | %0.6 | %0.6 | %0.6 | %0.5 | %0.7 | %1.2 | %1.2 | %1.2 | %1.2 | %1.2 | %1.2 | %1.2 | %6.7 |
| *«ikisini de sen»* | %0.0 | %0.9 | %0.6 | %0.6 | %0.6 | %0.5 | %0.4 | %2.5 | %2.5 | %2.5 | %2.5 | %2.5 | %2.5 | %2.5 | %5.0 |

## 3. ⭐⭐ Eşik duyarlılığı

⛔ *«%2»* bir SEÇİMDİR, ölçüm değil. Seçimin sonucu ne kadar belirlediği
gösterilmeden sayı okunamaz:

| eşik | kayıt | eşiği aşan dizi |
|---|---:|---:|
| %1.0 | 2 | 44 |
| %2.0 | 2 | 44 |
| %3.0 | 2 | 44 |
| %5.0 | 3 | 9 |

## 4. ⭐⭐ T139'un elle listesi ne kadar alt sınırdı?

T139 beş kalıbı **elle** yazmış ve şerh düşmüştü: *«sayı ALT SINIRDIR»*.
Şerh doğruydu ve şimdi ölçülebiliyor:

⛔ Ham fark yanıltıcı olurdu: eşiği aşan dizilerin bir kısmı **doğal Türkçe**
(*«başka bir şey»*). ⇒ En yaygın **22** dizi elle sınıflandırıldı ve iddia
yalnız sınıflandırılmış veriye dayanıyor.

| | |
|---|---:|
| kapının eşiği aşan dizisi | 44 |
| elle sınıflandırılan | **2** |
| · kural kaynaklı **formül** | **0** |
| · doğal Türkçe | 2 |
| ⛔ **formül olup T139'un listesinde OLMAYAN** | **0** |

| dizi | kayıt | sınıf | T139'da |
|---|---:|---|---|
| *«bir şey var»* | 7 | doğal dil | ⛔ **yok** |
| *«başka bir şey»* | 2 | doğal dil | ⛔ **yok** |

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
