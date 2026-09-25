# Şablonlaşma kapısı — kalıplar sayılarak bulundu

**Betik:** `scripts/analiz/2026-09-18-sablon-kapisi.py` (yazıldı 2026-09-18) · **koşu tarihi:** 2026-09-20  
**Girdi:** `data/candidates/v6-parti4.jsonl` · SHA256-16 `ccbcade14175e020` · **59** kayıt  
**Eşik:** bir dizi en az **%2.0** (2 kayıt) içinde geçmeli

⛔⛔ **T139'un açık kalemi.** T139 şablonlaşmayı ölçmüştü ama kalıpları **elle**
yazmıştı ve şerh düşmüştü: *«sayı ALT SINIRDIR; sözlükte olmayan şablonlar
görünmez»*. Burada liste **yazılmıyor, çıkarılıyor**: asistan cevaplarındaki
bütün 5–10 sözcüklük diziler sayılıyor.

⚠️ **Bu bir SAYIM kapısıdır.** *«Şablon = kusur»* değildir — tekrarlanan bir cümle
doğru da olabilir. Kapı hiçbir kaydı düşürmez.

## 1. ⭐ Eşiği aşan diziler — **42**

| kayıt | % | uzunluk | dizi |
|---:|---:|---:|---|
| 6 | %10.2 | 3 | *«başka bir şey»* |
| 4 | %6.8 | 3 | *«bir şey söylemeyeceğim»* |
| 3 | %5.1 | 3 | *«olan sensin ve»* |
| 3 | %5.1 | 3 | *«ayni şey değil»* |
| 3 | %5.1 | 3 | *«ben karar veremem»* |
| 3 | %5.1 | 3 | *«dair bir hüküm»* |
| 3 | %5.1 | 3 | *«yazdin ve bu»* |
| 3 | %5.1 | 3 | *«bir şey var»* |
| 3 | %5.1 | 3 | *«orada yalniz randevu»* |
| 3 | %5.1 | 3 | *«yazmiyor orada yalniz»* |
| 3 | %5.1 | 3 | *«sana ben söyleyemem»* |
| 2 | %3.4 | 6 | *«yazmiyor orada yalniz randevu sirasi ve»* |
| 2 | %3.4 | 5 | *«ne yapacağini sana ben söyleyemem»* |
| 2 | %3.4 | 4 | *«ikisini de sen söyledin»* |
| 2 | %3.4 | 4 | *«olan da sen ama»* |
| 2 | %3.4 | 4 | *«oturacak olan sensin ve»* |
| 2 | %3.4 | 4 | *«olup olmadiğina bakamam ve»* |
| 2 | %3.4 | 4 | *«dair bir hüküm vermeyeceğim»* |
| 2 | %3.4 | 4 | *«var o yüzden bilmiyorum»* |
| 2 | %3.4 | 4 | *«bakilmasi gereken bir şey»* |
| 2 | %3.4 | 4 | *«olmamiş yapmiyor ve bu»* |
| 2 | %3.4 | 4 | *«ne yapman gerektiğini söylemeyeceğim»* |
| 2 | %3.4 | 4 | *«bir şey söyleyemem ne»* |
| 2 | %3.4 | 3 | *«ama şuna dikkat»* |
| 2 | %3.4 | 3 | *«ne kadar ağir»* |
| 2 | %3.4 | 3 | *«ne anlama geldiğini»* |
| 2 | %3.4 | 3 | *«kişi ben değilim»* |
| 2 | %3.4 | 3 | *«iki ayri şey»* |
| 2 | %3.4 | 3 | *«ve kayit var»* |
| 2 | %3.4 | 3 | *«benim işim değil»* |
| … | | | 12 dizi daha (JSON'da tamamı) |

## 2. ⭐ Sürümler boyunca büyüme

T139: *«her yeni kural, bir sonraki şablonun tohumu»*. En yaygın beş dizinin
sürümler boyunca **kayıt payı**:

| dizi | v0.0.1 | v0.0.2 | v0.0.3 | v0.0.4 | v0.0.5 | v0.0.6 | v0.0.7 | v0.0.8 | v0.0.9 | v0.0.10 | v0.0.11 | v0.0.12 | v0.0.13 | v0.0.14 | candidates |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| *«başka bir şey»* | %15.0 | %3.4 | %2.6 | %2.6 | %2.6 | %3.3 | %2.9 | %4.2 | %4.2 | %4.2 | %4.2 | %4.2 | %4.2 | %4.2 | %10.2 |
| *«bir şey söylemeyeceğim»* | %5.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %1.5 | %4.9 | %4.9 | %4.9 | %4.9 | %4.9 | %4.9 | %4.9 | %6.8 |
| *«olan sensin ve»* | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %0.0 | %5.1 |
| *«ayni şey değil»* | %0.0 | %0.9 | %0.6 | %0.6 | %0.6 | %1.4 | %2.6 | %3.3 | %3.3 | %3.3 | %3.3 | %3.3 | %3.3 | %3.3 | %5.1 |
| *«ben karar veremem»* | %0.0 | %2.6 | %4.5 | %4.5 | %4.5 | %4.7 | %5.1 | %3.0 | %3.0 | %3.0 | %3.0 | %3.0 | %3.0 | %3.0 | %5.1 |

## 3. ⭐⭐ Eşik duyarlılığı

⛔ *«%2»* bir SEÇİMDİR, ölçüm değil. Seçimin sonucu ne kadar belirlediği
gösterilmeden sayı okunamaz:

| eşik | kayıt | eşiği aşan dizi |
|---|---:|---:|
| %1.0 | 2 | 42 |
| %2.0 | 2 | 42 |
| %3.0 | 2 | 42 |
| %5.0 | 3 | 11 |

## 4. ⭐⭐ T139'un elle listesi ne kadar alt sınırdı?

T139 beş kalıbı **elle** yazmış ve şerh düşmüştü: *«sayı ALT SINIRDIR»*.
Şerh doğruydu ve şimdi ölçülebiliyor:

⛔ Ham fark yanıltıcı olurdu: eşiği aşan dizilerin bir kısmı **doğal Türkçe**
(*«başka bir şey»*). ⇒ En yaygın **22** dizi elle sınıflandırıldı ve iddia
yalnız sınıflandırılmış veriye dayanıyor.

| | |
|---|---:|
| kapının eşiği aşan dizisi | 42 |
| elle sınıflandırılan | **6** |
| · kural kaynaklı **formül** | **4** |
| · doğal Türkçe | 2 |
| ⛔ **formül olup T139'un listesinde OLMAYAN** | **3** |

| dizi | kayıt | sınıf | T139'da |
|---|---:|---|---|
| *«başka bir şey»* | 6 | doğal dil | ⛔ **yok** |
| *«bir şey söylemeyeceğim»* | 4 | kural formülü | ⛔ **yok** |
| *«ayni şey değil»* | 3 | kural formülü | ⛔ **yok** |
| *«ben karar veremem»* | 3 | kural formülü | ⛔ **yok** |
| *«bir şey var»* | 3 | doğal dil | ⛔ **yok** |
| *«benim işim değil»* | 2 | kural formülü | ✅ var |

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
