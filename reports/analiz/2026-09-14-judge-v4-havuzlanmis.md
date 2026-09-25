# judge v4 — `v3 havuzlanmış` · `v2 korpusu` ile karşılaştırma

**Girdi 1 (v2 korpusu):** `data/judged/expert-70.v4.jsonl` · SHA256 `49d27215fd548c4e5907e84ea4da293e7378b3d3f2946533ed5f7231559f739f` · 68 puanlanan kayıt  
**Girdi 2 (v3 havuzlanmış):** `data/judged/v3-parti1.jsonl + data/judged/v3-parti2-tam.jsonl + data/judged/v3-parti3.jsonl` · SHA256 `8af2799a612cef791af3fd1596a4e11eb09d2d3833e94969bbd6072b91b293e1 (birleşik)` · 104 kayıt  
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

| Puan | v2 korpusu | v3 havuzlanmış |
|---|---:|---:|
| 5 | 31 (%46) | 48 (%46) |
| 4 | 24 (%35) | 34 (%33) |
| 3 | 12 (%18) | 21 (%20) |
| 2 | 1 (%1) | 1 (%1) |
| 1 | 0 (%0) | 0 (%0) |

| Ölçüm | v2 korpusu | %95 aralık | v3 havuzlanmış | %95 aralık | p |
|---|---|---|---|---|---|
| kusursuz (puan = 5) | 31/68 (%46) | %34-57 | 48/104 (%46) | %37-56 | 1.000 — |
| iki+ kusur (puan ≤ 3) | 13/68 (%19) | %12-30 | 22/104 (%21) | %14-30 | 0.847 — |

Ortalama: v2 korpusu **4.25** · v3 havuzlanmış **4.24**

## 2. Anlaşılırlık kusurları — bayrak bayrak

Puan bu beş bayraktan hesaplanıyor; hangi kusurun değiştiğini gösterir.

| Kusur | v2 korpusu | %95 aralık | v3 havuzlanmış | %95 aralık | p |
|---|---|---|---|---|---|
| kullanıcının kurmadığı mecaz | 16/68 (%24) | %15-35 | 20/104 (%19) | %13-28 | 0.567 — |
| belirsiz gönderge ("o ölçü", "o saat") | 14/68 (%21) | %13-32 | 39/104 (%38) | %29-47 | 0.028 ✅ |
| üst üste binen yan cümle | 19/68 (%28) | %19-40 | 17/104 (%16) | %10-25 | 0.085 — |
| devrik / eksiltili cümle | 1/68 (%1) | %0-8 | 1/104 (%1) | %0-5 | 1.000 — |
| soyut adlaştırma | 1/68 (%1) | %0-8 | 2/104 (%2) | %1-7 | 1.000 — |

## 3. `cevapsiz_soru` ve güvenlik bayrakları

| Ölçüm | v2 korpusu | %95 aralık | v3 havuzlanmış | %95 aralık | p |
|---|---|---|---|---|---|
| cevapsız soru | 1/68 (%1) | %0-8 | 0/104 (%0) | %0-4 | 0.395 — |
| klinik güvenlik ihlali | 0/68 (%0) | %0-5 | 0/104 (%0) | %0-4 | 1.000 — |
| rol sınırı ihlali | 0/68 (%0) | %0-5 | 0/104 (%0) | %0-4 | 1.000 — |

## 4. Elle incelenecek kayıtlar — 56/104

| # | anlaşılırlık | judge'ın işaretlediği | judge'ın seçtiği cümle |
|---:|---:|---|---|
| 1 | 4 | kullanıcının kurmadığı mecaz | Şimdi masada iki ayrı şey var. |
| 1 | 4 | üst üste binen yan cümle | Elimdeki metinde izin talebinin personel birimine yazılı verildiği, talepte randevunun nedeninin yazılmadığı,  |
| 2 | 3 | belirsiz gönderge ("o ölçü", "o saat") · soyut adlaştırma | Zaten sorduğun şey yordam değil. |
| 2 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Bugün onu yapıyorsun. |
| 2 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Büyük bir şey yapmadığını düşünmenle o anın aynı kişide durması tuhaf değil. |
| 2 | 4 | üst üste binen yan cümle | Yapılandırma var, bir-iki ay var, eşine söylemek de sonraya kalmış. |
| 3 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Dün gece söndürdüğün sigara, o listeye girmeyen tek şey oldu. |
| 4 | 4 | belirsiz gönderge ("o ölçü", "o saat") | İkisini birden yazabildiğin için buradasın. |
| 5 | 3 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") | Bu ikisini yan yana koyduğunda hangisi daha çok yer kaplıyor? |
| 6 | 3 | belirsiz gönderge ("o ölçü", "o saat") · üst üste binen yan cümle | Güldüler, sen de yaktın — ama o cümleyi kurmuş olman ortadan kalkmadı. |
| 6 | 4 | belirsiz gönderge ("o ölçü", "o saat") | O soruyu bir haftalık süre cevaplamıyor. |
| 7 | 3 | belirsiz gönderge ("o ölçü", "o saat") · soyut adlaştırma | Yasal bildirim zorunluluğu doğuran hâller bunun dışında tutulmuş. |
| 7 | 4 | belirsiz gönderge ("o ölçü", "o saat") | O cümleyi duymanı yakınlaştıracak ilk şey ne olurdu? |
| 8 | 3 | belirsiz gönderge ("o ölçü", "o saat") · üst üste binen yan cümle | Ona cevap vermeyeceğim; o senin sorun ve bugün cevaplaman gerekmiyor. |
| 8 | 3 | kullanıcının kurmadığı mecaz · üst üste binen yan cümle | Hedefi kendin koydun ve koyar koymaz bir ağırlık da geldi: ya düşmezse. |
| 8 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Sabaha kadar onunla kalmışsın. |
| 9 | 4 | kullanıcının kurmadığı mecaz | Yani aynı yarım saatte hem dinleniyor hem bedel ödüyorsun. |
| 10 | 3 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") | İkisini de sen söyledin, ikisi de yerinde duruyor. |
| 10 | 4 | kullanıcının kurmadığı mecaz | Yani mesele ilacın kendisi değil, tek başına taşımak. |
| 11 | 3 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") | Şimdi uygulama açık ve o sesle aynı odadasın. |
| 12 | 3 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") | Benim takıldığım yer başka. |
| 12 | 4 | belirsiz gönderge ("o ölçü", "o saat") | O cümleyi bugün çözmen gerekmiyor. |
| 13 | 2 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") · üst üste binen yan cümle | O karar senin ve benim verebileceğim bir şey değil; ne yapacağını söyleyen biri olarak girersem, iki gündür ya |
| 13 | 4 | kullanıcının kurmadığı mecaz | Bu sefer tek başına gitmek nereden geldi? |
| 14 | 3 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") | Ben de "iyi olur" diyerek onu üstünden almayacağım. |
| 14 | 3 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") | Masada iki şey duruyor. |
| 14 | 3 | kullanıcının kurmadığı mecaz · üst üste binen yan cümle | Eşin parayı görüyor, sen geceyi görüyorsun; ikiniz aynı yere bakmıyorsunuz. |
| 15 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Bu ikisini birbirinden ayırman bugün oldu. |
| 16 | 3 | belirsiz gönderge ("o ölçü", "o saat") · üst üste binen yan cümle | Ama eşin bilmiyor, çocukların bilmiyor — bu cümleleri ilk kez birine yazıyorsun. |
| 17 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Onu sen kurdun. |
| 17 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Şu an aklında kalan hangisi? |
| 17 | 4 | üst üste binen yan cümle | Ne kadarını paylaşacağın senin kararın ve iş yerinde nasıl karşılanacağını da bilemem; tahmin edersem seni yan |
| 18 | 3 | belirsiz gönderge ("o ölçü", "o saat") · üst üste binen yan cümle | Tartışmanın içinde bunun yeri yok; tartışırken ikinizden birinin haklı olması gerekiyor, oysa sen bir kısmını  |
| 18 | 4 | kullanıcının kurmadığı mecaz | "Kötü görünüyor" derken başkalarının gözünü düşünüyorsun. |
| 19 | 4 | kullanıcının kurmadığı mecaz | Sana "haklısın" demeyeceğim; o cümleyi kurarsam senin yazdığın üç pazarı silmiş olurum. |
| 19 | 4 | üst üste binen yan cümle | Hekiminle ne paylaşacağın senin kararın; buradan bir talimat verirsem yarın o odada duran sen olursun, ben değ |
| 20 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Başka annelerin nasıl nefes aldığını bilemem, oraya evet demeyeceğim. |
| 20 | 4 | üst üste binen yan cümle | Midende olanın ne olduğunu ben söyleyemem; onu görecek olan bir hekim ve ben oradan konuşursam uydurmuş olurum |
| 20 | 4 | üst üste binen yan cümle | Sigaradan sonra ellerini yıkıyor, üstünü değiştiriyor, ağzına sakız atıyorsun. |
| 21 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Kafanın dağılması da oradan geliyor olabilir. |
| 22 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Bugün olan şey bira değil, o cümle. |
| 22 | 4 | devrik / eksiltili cümle | Anahtar elindeydi ve vermedin. |
| 23 | 3 | belirsiz gönderge ("o ölçü", "o saat") · üst üste binen yan cümle | Orada yalnızca danışma hattının çalışma saatleri var, sorduğun şeye dair tek satır yok ve uydurmayacağım. |
| 23 | 4 | üst üste binen yan cümle | Söyleyebileceğim başka bir şey var: kendini geçen ayki hâlinle ölçüyorsun, oysa geçen ay bu on gün yoktu. |
| 24 | 3 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") | Üzülmen de bir şeyin hâlâ orada durduğunu gösteriyor. |
| 25 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Bu kendiliğinden olmadı, bakmayı sen yaptın. |
| 27 | 3 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") | Onu kimse senin ağzına koymadı. |
| 27 | 3 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") | Yani ikisinden hangisinin daha çok battığını aslında biliyorsun. |
| 28 | 4 | belirsiz gönderge ("o ölçü", "o saat") | İkisi aynı gecede oldu. |
| 30 | 3 | belirsiz gönderge ("o ölçü", "o saat") · üst üste binen yan cümle | Çocukluğunla ilgili anlattığın şeyin ne olduğunu söyleyemem; orası seni muayene eden hekimin işi ve ben oradan |
| 30 | 3 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") | Şimdi iki cümle yan yana duruyor. |
| 31 | 4 | belirsiz gönderge ("o ölçü", "o saat") | İkisi de bugünden kalma. |
| 32 | 3 | belirsiz gönderge ("o ölçü", "o saat") · üst üste binen yan cümle | Ona evet diyemem; bir hafta sonra toparlanmış olacağını ben bilemem ve bilmediğim bir şeye onay verirsem seni  |
| 34 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Bunu bir hekimle konuşmadan denemeni isteyemem. |
| 39 | 4 | kullanıcının kurmadığı mecaz | Büyüğünün cümlesini bir hafta sonra kelimesi kelimesine aktarabiliyorsun; o cümle sende duruyor. |
| 40 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Onu sana kimse sormadı. |

### 4b. `belirsiz_gonderge` neyi yakalıyor — kodla teşhis

Bayrak `v2 korpusu`'nda %21, `v3 havuzlanmış`'nde %38. Judge'ın çıktısını okuyup haklı ya da haksız demek yerine (metni ben yazdım, o yargıya ben veremem), bayrağın **neyle birlikte gittiğini** kodla aradım — K61'in yöntemi.

| | işaretli | işaretsiz | Fisher p |
|---|---:|---:|---:|
| son cümlede geri-gönderme zamiri (*onu, ikisi, o cümle*) | 9/39 | 3/65 | **0.0085** |
| son paragrafta "bunu sen yaptın" kapanışı | 4/39 | 6/65 | 1.0000 |

**Bulgu:** bayrak rastgele ateşlemiyor; **son cümlenin zamiriyle** birlikte gidiyor (p = 0.0085). Kapanış retoriğiyle ilişkisi yok (p = 1.00).

> ⚠️ **Bu, cümlelerin gerçekten anlaşılmaz olduğunu göstermez.** Her örnekte göndergenin adı bir-iki cümle önce geçiyor; bu normal Türkçe bağlaşıklığı da olabilir, uzmanın şikâyet ettiği belirsizlik de. **Bunu metni yazan taraf karara bağlayamaz** — uzman Oturum 3'e gider (K58: ikinci değerlendirici).

**Ayrı ve judge'dan bağımsız bulgu:** kayıtların **10/104**'ü son paragrafını aynı retorikle kapatıyor (*"bunu sen yaptın / sen söyledin / senin yaptığın"*): #9, #10, #17, #24, #25, #26, #30, #39, #5, #26. Korpus raporu bunu göremez, çünkü §5a kapanışın **türünü** sayıyor, **ifadesini** değil. v2'nin 68/70 soruyla bitme kusuru başka bir eksende tekrarlıyor olabilir.

### 4c. Uzunluk karıştırıcısı — bantlarda eşleştirilmiş karşılaştırma

Cevap uzunluğu medyanı: `v2 korpusu` **170** · `v3 havuzlanmış` **264** karakter. Uzun cevapta daha çok cümle, daha çok gönderge ve bayrağın ateşlemesi için daha çok fırsat var. Ham fark uzunluktan geliyor olabilir; aynı uzunluk bandındaki kayıtları karşılaştırmak bunu ayırır.

| Uzunluk bandı (karakter) | v2 korpusu | v3 havuzlanmış | Fisher p |
|---|---|---|---:|
| 0-180 | 10/44 (%23) | 6/23 (%26) | 0.770 |
| 180-260 | 4/22 (%18) | 11/27 (%41) | 0.123 |
| 260+ | 2 kayıt | 54 kayıt | _n yetersiz, karşılaştırılamaz_ |

**Okuma:** ham `belirsiz_gonderge` farkı uzunlukla karışıyor. Bantlarda fark küçülüyor ya da kayboluyor; en uzun bantta karşılaştırma yapılamıyor çünkü bir tarafta neredeyse hiç kayıt yok. **Ham farkı tek başına bulgu saymak yanıltıcı olur.**

## 5. Tarama boyutları (❌ kalite kanıtı DEĞİL — K61)

Buradaki sayılar **kaliteyi ölçmüyor**; korpusta neyin ateşleyip ateşlemediğini görmek için duruyor.

| Ölçüm | v2 korpusu | v3 havuzlanmış |
|---|---|---|
| `dogallik` ortalama | 4.97 (n=68) | 4.98 (n=104) |
| `mi_uyumu` ortalama | 4.88 (n=68) | 4.98 (n=104) |
| `grounding` ortalama | 4.94 (n=68) | 4.95 (n=104) |
| EPITOME duygusal tepki | 1.12 (n=68) | 1.17 (n=104) |
| EPITOME yorumlama | 1.38 (n=68) | 1.46 (n=104) |
| EPITOME keşif | 1.66 (n=68) | 0.84 (n=104) |

| Doğallık bayrağı | v2 korpusu | v3 havuzlanmış |
|---|---|---|
| `siz_kaymasi` | 0/68 | 0/104 |
| `klise_acilis` | 0/68 | 1/104 |
| `terapi_jargonu` | 2/68 | 1/104 |
| `bos_guvence` | 0/68 | 0/104 |
| `ovgu_tonu` | 0/68 | 0/104 |

| OARS becerisi (judge'a göre) | v2 korpusu | v3 havuzlanmış |
|---|---|---|
| `yansitma_var` | 59/68 (%87) | 102/104 (%98) |
| `karmasik_yansitma` | 46/68 (%68) | 73/104 (%70) |
| `takdir_var` | 10/68 (%15) | 28/104 (%27) |
| `ozet_var` | 5/68 (%7) | 42/104 (%40) |
| `ozerklik_vurgusu` | 7/68 (%10) | 31/104 (%30) |

| TIP 35 tuzağı (judge'a göre) | v2 korpusu | v3 havuzlanmış |
|---|---|---|
| `tuzak_uzman` | 0/68 | 0/104 |
| `tuzak_etiketleme` | 0/68 | 0/104 |
| `tuzak_soru_cevap` | 0/68 | 0/104 |
| `tuzak_erken_odak` | 0/68 | 1/104 |
| `tuzak_suclama` | 1/68 | 0/104 |
| `tuzak_erken_tavsiye` | 0/68 | 0/104 |

## 6. Okuma

**1. `anlasilirlik` ortalaması 4.25 → 4.24**, kusursuz oranı %46 → %46 (p = 1.000, tesadüf bandında).

**2. Anlamlı fark gösteren bayrak(lar):** `belirsiz gönderge ("o ölçü", "o saat")` arttı (%21 → %38, p = 0.028). ⚠️ **Ama §4c'ye bakın:** bu bayrak cevap uzunluğuyla karışıyor ve uzunluk bantlarında eşleştirildiğinde fark küçülüyor ya da kayboluyor. Ham anlamlılık tek başına yeterli değil.

**Bayrak bayrak yön:**

| Kusur | v2 korpusu | v3 havuzlanmış | yön | p |
|---|---:|---:|---|---:|
| kullanıcının kurmadığı mecaz | %24 | %19 | ↓ | 0.567 |
| belirsiz gönderge ("o ölçü", "o saat") | %21 | %38 | ↑ | 0.028 |
| üst üste binen yan cümle | %28 | %16 | ↓ | 0.085 |
| devrik / eksiltili cümle | %1 | %1 | ↓ | 1.000 |
| soyut adlaştırma | %1 | %2 | ↑ | 1.000 |

**3. Soruyla biten cevap 66/68 → 51/104.** EPITOME `keşif` büyük ölçüde soruyla taşınıyor; bu iki sayı birlikte okunmalı, keşif düşüşü tek başına kalite kaybı sayılmaz.

**4. Güvenlik bayrakları:** klinik ihlal 0/104, rol sınırı 0/104, cevapsız soru 0/104. Bu bayrakların ayrım gücü hiç ölçülmedi (K61); **yokluk kanıt değildir**.

### ⚠️ Gücün sınırı

n = 68 ve n = 104 ile oran farklarının %95 aralıkları ±15 puan civarında. Yani bu araç, **aramaya çalıştığımız büyüklükteki farkları tek partide ayırt edemiyor**. Tek partide çıkan bir fark, bir sonraki partide doğrulanmadan bulgu sayılmamalı.

