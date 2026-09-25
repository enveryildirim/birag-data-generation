# judge v4 — `v3 korpusu` · `v2 korpusu` ile karşılaştırma

**Girdi 1 (v2 korpusu):** `data/judged/expert-70.v4.jsonl` · SHA256 `49d27215fd548c4e5907e84ea4da293e7378b3d3f2946533ed5f7231559f739f` · 68 puanlanan kayıt  
**Girdi 2 (v3 korpusu):** `data/judged/v3-parti1.jsonl` · SHA256 `4003bd2b959772f27b307946d943c65343e1559fd20affeaa8ccf2b3418bdb2b` · 40 kayıt  
**Rubrik:** `prompts/judge-eksen1.v4.md` (iki korpusta da aynı) · **Judge:** `agy:gemini-3.8-flash-high`  
**Betik:** `scripts/analiz/2026-09-14-judge-v4-karsilastirma.py` · **Tarih:** 2026-09-14

---

## 0. Bu rapor neyi söyleyebilir

| Boyut | Durum | Kaynak |
|---|---|---|
| `anlasilirlik` | ✅ **Kalite kanıtı.** Uzmanın kabul/ret kararını ayırdığı ölçüldü (uyum oranı 0.81-0.87) | K59 · K62 |
| `cevapsiz_soru` | ✅ Elle incelemeye yönlendirir | K57 |
| `dogallik` · `mi_uyumu` · EPITOME · `grounding` | ❌ **Tarama.** Uyum oranı tesadüf bandında, kalite kanıtı değil | K61 |

> ⚠️ **Bu kontrollü bir deney değil.** İki korpus yalnızca üretim talimatında değil; tohumlarda, senaryo karışımında ve yazım oturumunda da farklı (v3 yazılırken uzmanın 13 notu okunmuştu). Aradaki fark **v3 talimatına atfedilemez**. Aşağısı betimsel bir karşılaştırmadır.

> `p` sütunu Fisher kesin testi; ✅ = p < 0.05. Aralıklar Wilson %95.

## 1. `anlasilirlik` — koddan hesaplanan puan (✅ kalite kanıtı)

| Puan | v2 korpusu | v3 korpusu |
|---|---:|---:|
| 5 | 31 (%46) | 20 (%50) |
| 4 | 24 (%35) | 12 (%30) |
| 3 | 12 (%18) | 8 (%20) |
| 2 | 1 (%1) | 0 (%0) |
| 1 | 0 (%0) | 0 (%0) |

| Ölçüm | v2 korpusu | %95 aralık | v3 korpusu | %95 aralık | p |
|---|---|---|---|---|---|
| kusursuz (puan = 5) | 31/68 (%46) | %34-57 | 20/40 (%50) | %35-65 | 0.693 — |
| iki+ kusur (puan ≤ 3) | 13/68 (%19) | %12-30 | 8/40 (%20) | %10-35 | 1.000 — |

Ortalama: v2 korpusu **4.25** · v3 korpusu **4.30**

## 2. Anlaşılırlık kusurları — bayrak bayrak

Puan bu beş bayraktan hesaplanıyor; hangi kusurun değiştiğini gösterir.

| Kusur | v2 korpusu | %95 aralık | v3 korpusu | %95 aralık | p |
|---|---|---|---|---|---|
| kullanıcının kurmadığı mecaz | 16/68 (%24) | %15-35 | 10/40 (%25) | %14-40 | 1.000 — |
| belirsiz gönderge ("o ölçü", "o saat") | 14/68 (%21) | %13-32 | 14/40 (%35) | %22-50 | 0.115 — |
| üst üste binen yan cümle | 19/68 (%28) | %19-40 | 4/40 (%10) | %4-23 | 0.031 ✅ |
| devrik / eksiltili cümle | 1/68 (%1) | %0-8 | 0/40 (%0) | %-0-9 | 1.000 — |
| soyut adlaştırma | 1/68 (%1) | %0-8 | 0/40 (%0) | %-0-9 | 1.000 — |

## 3. `cevapsiz_soru` ve güvenlik bayrakları

| Ölçüm | v2 korpusu | %95 aralık | v3 korpusu | %95 aralık | p |
|---|---|---|---|---|---|
| cevapsız soru | 1/68 (%1) | %0-8 | 0/40 (%0) | %-0-9 | 1.000 — |
| klinik güvenlik ihlali | 0/68 (%0) | %0-5 | 0/40 (%0) | %-0-9 | 1.000 — |
| rol sınırı ihlali | 0/68 (%0) | %0-5 | 0/40 (%0) | %-0-9 | 1.000 — |

## 4. Elle incelenecek kayıtlar — 20/40

| # | anlaşılırlık | judge'ın işaretlediği | judge'ın seçtiği cümle |
|---:|---:|---|---|
| 2 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Bugün onu yapıyorsun. |
| 4 | 4 | belirsiz gönderge ("o ölçü", "o saat") | İkisini birden yazabildiğin için buradasın. |
| 5 | 3 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") | Bu ikisini yan yana koyduğunda hangisi daha çok yer kaplıyor? |
| 6 | 3 | belirsiz gönderge ("o ölçü", "o saat") · üst üste binen yan cümle | Güldüler, sen de yaktın — ama o cümleyi kurmuş olman ortadan kalkmadı. |
| 8 | 3 | kullanıcının kurmadığı mecaz · üst üste binen yan cümle | Hedefi kendin koydun ve koyar koymaz bir ağırlık da geldi: ya düşmezse. |
| 10 | 3 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") | İkisini de sen söyledin, ikisi de yerinde duruyor. |
| 12 | 3 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") | Benim takıldığım yer başka. |
| 13 | 4 | kullanıcının kurmadığı mecaz | Bu sefer tek başına gitmek nereden geldi? |
| 14 | 3 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") | Ben de "iyi olur" diyerek onu üstünden almayacağım. |
| 17 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Onu sen kurdun. |
| 19 | 4 | kullanıcının kurmadığı mecaz | Sana "haklısın" demeyeceğim; o cümleyi kurarsam senin yazdığın üç pazarı silmiş olurum. |
| 20 | 4 | üst üste binen yan cümle | Sigaradan sonra ellerini yıkıyor, üstünü değiştiriyor, ağzına sakız atıyorsun. |
| 23 | 4 | üst üste binen yan cümle | Söyleyebileceğim başka bir şey var: kendini geçen ayki hâlinle ölçüyorsun, oysa geçen ay bu on gün yoktu. |
| 25 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Bu kendiliğinden olmadı, bakmayı sen yaptın. |
| 27 | 3 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") | Onu kimse senin ağzına koymadı. |
| 30 | 3 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") | Şimdi iki cümle yan yana duruyor. |
| 31 | 4 | belirsiz gönderge ("o ölçü", "o saat") | İkisi de bugünden kalma. |
| 34 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Bunu bir hekimle konuşmadan denemeni isteyemem. |
| 39 | 4 | kullanıcının kurmadığı mecaz | Büyüğünün cümlesini bir hafta sonra kelimesi kelimesine aktarabiliyorsun; o cümle sende duruyor. |
| 40 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Onu sana kimse sormadı. |

### 4b. `belirsiz_gonderge` neyi yakalıyor — kodla teşhis

Bayrak `v2 korpusu`'nda %21, `v3 korpusu`'nde %35. Judge'ın çıktısını okuyup haklı ya da haksız demek yerine (metni ben yazdım, o yargıya ben veremem), bayrağın **neyle birlikte gittiğini** kodla aradım — K61'in yöntemi.

| | işaretli | işaretsiz | Fisher p |
|---|---:|---:|---:|
| son cümlede geri-gönderme zamiri (*onu, ikisi, o cümle*) | 8/14 | 1/26 | **0.0003** |
| son paragrafta "bunu sen yaptın" kapanışı | 4/14 | 4/26 | 0.4162 |

**Bulgu:** bayrak rastgele ateşlemiyor; **son cümlenin zamiriyle** birlikte gidiyor (p = 0.0003). Kapanış retoriğiyle ilişkisi yok (p = 0.42).

> ⚠️ **Bu, cümlelerin gerçekten anlaşılmaz olduğunu göstermez.** Her örnekte göndergenin adı bir-iki cümle önce geçiyor; bu normal Türkçe bağlaşıklığı da olabilir, uzmanın şikâyet ettiği belirsizlik de. **Bunu metni yazan taraf karara bağlayamaz** — uzman Oturum 3'e gider (K58: ikinci değerlendirici).

**Ayrı ve judge'dan bağımsız bulgu:** kayıtların **8/40**'ü son paragrafını aynı retorikle kapatıyor (*"bunu sen yaptın / sen söyledin / senin yaptığın"*): #9, #10, #17, #24, #25, #26, #30, #39. Korpus raporu bunu göremez, çünkü §5a kapanışın **türünü** sayıyor, **ifadesini** değil. v2'nin 68/70 soruyla bitme kusuru başka bir eksende tekrarlıyor olabilir.

### 4c. Uzunluk karıştırıcısı — bantlarda eşleştirilmiş karşılaştırma

Cevap uzunluğu medyanı: `v2 korpusu` **170** · `v3 korpusu` **250** karakter. Uzun cevapta daha çok cümle, daha çok gönderge ve bayrağın ateşlemesi için daha çok fırsat var. Ham fark uzunluktan geliyor olabilir; aynı uzunluk bandındaki kayıtları karşılaştırmak bunu ayırır.

| Uzunluk bandı (karakter) | v2 korpusu | v3 korpusu | Fisher p |
|---|---|---|---:|
| 0-180 | 10/44 (%23) | 3/9 (%33) | 0.672 |
| 180-260 | 4/22 (%18) | 5/11 (%45) | 0.121 |
| 260+ | 2 kayıt | 20 kayıt | _n yetersiz, karşılaştırılamaz_ |

**Okuma:** ham `belirsiz_gonderge` farkı uzunlukla karışıyor. Bantlarda fark küçülüyor ya da kayboluyor; en uzun bantta karşılaştırma yapılamıyor çünkü bir tarafta neredeyse hiç kayıt yok. **Ham farkı tek başına bulgu saymak yanıltıcı olur.**

## 5. Tarama boyutları (❌ kalite kanıtı DEĞİL — K61)

Buradaki sayılar **kaliteyi ölçmüyor**; korpusta neyin ateşleyip ateşlemediğini görmek için duruyor.

| Ölçüm | v2 korpusu | v3 korpusu |
|---|---|---|
| `dogallik` ortalama | 4.97 (n=68) | 4.95 (n=40) |
| `mi_uyumu` ortalama | 4.88 (n=68) | 4.95 (n=40) |
| `grounding` ortalama | 4.94 (n=68) | 4.95 (n=40) |
| EPITOME duygusal tepki | 1.12 (n=68) | 1.20 (n=40) |
| EPITOME yorumlama | 1.38 (n=68) | 1.38 (n=40) |
| EPITOME keşif | 1.66 (n=68) | 0.80 (n=40) |

| Doğallık bayrağı | v2 korpusu | v3 korpusu |
|---|---|---|
| `siz_kaymasi` | 0/68 | 0/40 |
| `klise_acilis` | 0/68 | 1/40 |
| `terapi_jargonu` | 2/68 | 1/40 |
| `bos_guvence` | 0/68 | 0/40 |
| `ovgu_tonu` | 0/68 | 0/40 |

| OARS becerisi (judge'a göre) | v2 korpusu | v3 korpusu |
|---|---|---|
| `yansitma_var` | 59/68 (%87) | 39/40 (%98) |
| `karmasik_yansitma` | 46/68 (%68) | 27/40 (%68) |
| `takdir_var` | 10/68 (%15) | 11/40 (%28) |
| `ozet_var` | 5/68 (%7) | 18/40 (%45) |
| `ozerklik_vurgusu` | 7/68 (%10) | 12/40 (%30) |

| TIP 35 tuzağı (judge'a göre) | v2 korpusu | v3 korpusu |
|---|---|---|
| `tuzak_uzman` | 0/68 | 0/40 |
| `tuzak_etiketleme` | 0/68 | 0/40 |
| `tuzak_soru_cevap` | 0/68 | 0/40 |
| `tuzak_erken_odak` | 0/68 | 1/40 |
| `tuzak_suclama` | 1/68 | 0/40 |
| `tuzak_erken_tavsiye` | 0/68 | 0/40 |

## 6. Okuma

**1. `anlasilirlik` ortalaması 4.25 → 4.30**, kusursuz oranı %46 → %50 (p = 0.693, tesadüf bandında).

**2. Anlamlı fark gösteren bayrak(lar):** `üst üste binen yan cümle` düştü (%28 → %10, p = 0.031).

**Bayrak bayrak yön:**

| Kusur | v2 korpusu | v3 korpusu | yön | p |
|---|---:|---:|---|---:|
| kullanıcının kurmadığı mecaz | %24 | %25 | ↑ | 1.000 |
| belirsiz gönderge ("o ölçü", "o saat") | %21 | %35 | ↑ | 0.115 |
| üst üste binen yan cümle | %28 | %10 | ↓ | 0.031 |
| devrik / eksiltili cümle | %1 | %0 | ↓ | 1.000 |
| soyut adlaştırma | %1 | %0 | ↓ | 1.000 |

**3. Soruyla biten cevap 66/68 → 18/40.** EPITOME `keşif` büyük ölçüde soruyla taşınıyor; bu iki sayı birlikte okunmalı, keşif düşüşü tek başına kalite kaybı sayılmaz.

**4. Güvenlik bayrakları:** klinik ihlal 0/40, rol sınırı 0/40, cevapsız soru 0/40. Bu bayrakların ayrım gücü hiç ölçülmedi (K61); **yokluk kanıt değildir**.

### ⚠️ Gücün sınırı

n = 68 ve n = 40 ile oran farklarının %95 aralıkları ±15 puan civarında. Yani bu araç, **aramaya çalıştığımız büyüklükteki farkları tek partide ayırt edemiyor**. Tek partide çıkan bir fark, bir sonraki partide doğrulanmadan bulgu sayılmamalı.

