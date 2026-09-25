# Şablonlaşma kapısı — kalıplar sayılarak bulundu

**Betik:** `scripts/analiz/2026-09-18-sablon-kapisi.py` (yazıldı 2026-09-18) · **koşu tarihi:** 2026-09-20  
**Girdi:** `data/candidates/v6-parti1.jsonl` · SHA256-16 `bbdc8057636d46d5` · **59** kayıt  
**Eşik:** bir dizi en az **%2.0** (2 kayıt) içinde geçmeli

⛔⛔ **T139'un açık kalemi.** T139 şablonlaşmayı ölçmüştü ama kalıpları **elle**
yazmıştı ve şerh düşmüştü: *«sayı ALT SINIRDIR; sözlükte olmayan şablonlar
görünmez»*. Burada liste **yazılmıyor, çıkarılıyor**: asistan cevaplarındaki
bütün 5–10 sözcüklük diziler sayılıyor.

⚠️ **Bu bir SAYIM kapısıdır.** *«Şablon = kusur»* değildir — tekrarlanan bir cümle
doğru da olabilir. Kapı hiçbir kaydı düşürmez.

## 1. ⭐ Eşiği aşan diziler — **64**

| kayıt | % | uzunluk | dizi |
|---:|---:|---:|---|
| 4 | %6.8 | 3 | *«bunun sende ne»* |
| 4 | %6.8 | 3 | *«bir şey değil»* |
| 4 | %6.8 | 3 | *«bir hekimin bilmesi»* |
| 4 | %6.8 | 3 | *«ne yapacağin senin»* |
| 4 | %6.8 | 3 | *«bunu senin yerine»* |
| 4 | %6.8 | 3 | *«olup olmadiğini ben»* |
| 3 | %5.1 | 4 | *«bunu bir hekimin bilmesi»* |
| 3 | %5.1 | 4 | *«ne yapacağin senin kararin»* |
| 3 | %5.1 | 4 | *«olup olmadiğini ben söyleyemem»* |
| 3 | %5.1 | 3 | *«bilmiyorum sen de»* |
| 3 | %5.1 | 3 | *«ikisi de ayni»* |
| 3 | %5.1 | 3 | *«sende ne yapacağini»* |
| 3 | %5.1 | 3 | *«sen karar vereceksin»* |
| 3 | %5.1 | 3 | *«doğru olup olmadiğini»* |
| 3 | %5.1 | 3 | *«ben de bilmiyorum»* |
| 3 | %5.1 | 3 | *«kişinin kendi başvurusuyla»* |
| 2 | %3.4 | 7 | *«notta randevunun kişinin kendi başvurusuyla oluştuğu yaziyor»* |
| 2 | %3.4 | 6 | *«sen karar vereceksin bunu senin yerine»* |
| 2 | %3.4 | 6 | *«senin kararin bunu senin yerine söylemem»* |
| 2 | %3.4 | 6 | *«bunu bir hekimin bilmesi gerekiyor ve»* |
| 2 | %3.4 | 5 | *«an genelde neye denk geliyor»* |
| 2 | %3.4 | 5 | *«bir hekimin bilmesi gereken şeylerden»* |
| 2 | %3.4 | 5 | *«bu bir bilgi eksikliği değil»* |
| 2 | %3.4 | 5 | *«geliyor ne yapacağin senin kararin»* |
| 2 | %3.4 | 5 | *«birlikte söylüyorsun bunun sende ne»* |
| 2 | %3.4 | 5 | *«ikisinin bir arada ne yapacağini»* |
| 2 | %3.4 | 5 | *«ne yapacağini bilmiyorum ve bilmeden»* |
| 2 | %3.4 | 4 | *«ben bilmiyorum sen de»* |
| 2 | %3.4 | 4 | *«gibi duruyor ve sen»* |
| 2 | %3.4 | 4 | *«bunun sende ne yapacağini»* |
| … | | | 34 dizi daha (JSON'da tamamı) |

## 2. ⭐ Sürümler boyunca büyüme

T139: *«her yeni kural, bir sonraki şablonun tohumu»*. En yaygın beş dizinin
sürümler boyunca **kayıt payı**:

| dizi | v0.0.1 | v0.0.2 | v0.0.3 | v0.0.4 | v0.0.5 | v0.0.6 | v0.0.7 | v0.0.8 | v0.0.9 | v0.0.10 | v0.0.11 | v0.0.12 | v0.0.13 | v0.0.14 | candidates |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| *«bunun sende ne»* | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %6.8 |
| *«bir şey değil»* | %0.0 | %4.3 | %3.2 | %3.2 | %3.2 | %2.3 | %2.9 | %2.5 | %2.5 | %2.5 | %2.5 | %2.5 | %2.5 | %2.5 | %6.8 |
| *«bir hekimin bilmesi»* | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %1.6 | %2.1 | %2.1 | %2.1 | %2.1 | %2.1 | %2.1 | %6.8 |
| *«ne yapacağin senin»* | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %1.4 | %1.4 | %1.4 | %1.4 | %1.4 | %1.4 | %1.4 | %6.8 |
| *«bunu senin yerine»* | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %6.8 |

## 3. ⭐⭐ Eşik duyarlılığı

⛔ *«%2»* bir SEÇİMDİR, ölçüm değil. Seçimin sonucu ne kadar belirlediği
gösterilmeden sayı okunamaz:

| eşik | kayıt | eşiği aşan dizi |
|---|---:|---:|
| %1.0 | 2 | 64 |
| %2.0 | 2 | 64 |
| %3.0 | 2 | 64 |
| %5.0 | 3 | 16 |

## 4. ⭐⭐ T139'un elle listesi ne kadar alt sınırdı?

T139 beş kalıbı **elle** yazmış ve şerh düşmüştü: *«sayı ALT SINIRDIR»*.
Şerh doğruydu ve şimdi ölçülebiliyor:

⛔ Ham fark yanıltıcı olurdu: eşiği aşan dizilerin bir kısmı **doğal Türkçe**
(*«başka bir şey»*). ⇒ En yaygın **22** dizi elle sınıflandırıldı ve iddia
yalnız sınıflandırılmış veriye dayanıyor.

| | |
|---|---:|
| kapının eşiği aşan dizisi | 64 |
| elle sınıflandırılan | **2** |
| · kural kaynaklı **formül** | **2** |
| · doğal Türkçe | 0 |
| ⛔ **formül olup T139'un listesinde OLMAYAN** | **1** |

| dizi | kayıt | sınıf | T139'da |
|---|---:|---|---|
| *«olup olmadiğini ben»* | 4 | kural formülü | ✅ var |
| *«sen karar vereceksin»* | 3 | kural formülü | ⛔ **yok** |

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
