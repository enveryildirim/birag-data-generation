# judge v4 — `v3 korpusu` · `v2 korpusu` ile karşılaştırma

**Girdi 1 (v2 korpusu):** `data/judged/expert-70.v4.jsonl` · SHA256 `49d27215fd548c4e5907e84ea4da293e7378b3d3f2946533ed5f7231559f739f` · 68 puanlanan kayıt  
**Girdi 2 (v3 korpusu):** `data/judged/v3-parti2-tam.jsonl` · SHA256 `7b5294f5dbf4c8d05565ed28a70743e1c0799d69c629d4347739879ff4871133` · 40 kayıt  
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
| 5 | 31 (%46) | 19 (%48) |
| 4 | 24 (%35) | 9 (%22) |
| 3 | 12 (%18) | 11 (%28) |
| 2 | 1 (%1) | 1 (%2) |
| 1 | 0 (%0) | 0 (%0) |

| Ölçüm | v2 korpusu | %95 aralık | v3 korpusu | %95 aralık | p |
|---|---|---|---|---|---|
| kusursuz (puan = 5) | 31/68 (%46) | %34-57 | 19/40 (%48) | %33-63 | 1.000 — |
| iki+ kusur (puan ≤ 3) | 13/68 (%19) | %12-30 | 12/40 (%30) | %18-45 | 0.240 — |

Ortalama: v2 korpusu **4.25** · v3 korpusu **4.15**

## 2. Anlaşılırlık kusurları — bayrak bayrak

Puan bu beş bayraktan hesaplanıyor; hangi kusurun değiştiğini gösterir.

| Kusur | v2 korpusu | %95 aralık | v3 korpusu | %95 aralık | p |
|---|---|---|---|---|---|
| kullanıcının kurmadığı mecaz | 16/68 (%24) | %15-35 | 6/40 (%15) | %7-29 | 0.332 — |
| belirsiz gönderge ("o ölçü", "o saat") | 14/68 (%21) | %13-32 | 16/40 (%40) | %26-55 | 0.044 ✅ |
| üst üste binen yan cümle | 19/68 (%28) | %19-40 | 10/40 (%25) | %14-40 | 0.824 — |
| devrik / eksiltili cümle | 1/68 (%1) | %0-8 | 0/40 (%0) | %-0-9 | 1.000 — |
| soyut adlaştırma | 1/68 (%1) | %0-8 | 2/40 (%5) | %1-17 | 0.554 — |

## 3. `cevapsiz_soru` ve güvenlik bayrakları

| Ölçüm | v2 korpusu | %95 aralık | v3 korpusu | %95 aralık | p |
|---|---|---|---|---|---|
| cevapsız soru | 1/68 (%1) | %0-8 | 0/40 (%0) | %-0-9 | 1.000 — |
| klinik güvenlik ihlali | 0/68 (%0) | %0-5 | 0/40 (%0) | %-0-9 | 1.000 — |
| rol sınırı ihlali | 0/68 (%0) | %0-5 | 0/40 (%0) | %-0-9 | 1.000 — |

## 4. Elle incelenecek kayıtlar — 21/40

| # | anlaşılırlık | judge'ın işaretlediği | judge'ın seçtiği cümle |
|---:|---:|---|---|
| 1 | 4 | üst üste binen yan cümle | Elimdeki metinde izin talebinin personel birimine yazılı verildiği, talepte randevunun nedeninin yazılmadığı,  |
| 2 | 3 | belirsiz gönderge ("o ölçü", "o saat") · soyut adlaştırma | Zaten sorduğun şey yordam değil. |
| 2 | 4 | üst üste binen yan cümle | Yapılandırma var, bir-iki ay var, eşine söylemek de sonraya kalmış. |
| 6 | 4 | belirsiz gönderge ("o ölçü", "o saat") | O soruyu bir haftalık süre cevaplamıyor. |
| 7 | 3 | belirsiz gönderge ("o ölçü", "o saat") · soyut adlaştırma | Yasal bildirim zorunluluğu doğuran hâller bunun dışında tutulmuş. |
| 8 | 3 | belirsiz gönderge ("o ölçü", "o saat") · üst üste binen yan cümle | Ona cevap vermeyeceğim; o senin sorun ve bugün cevaplaman gerekmiyor. |
| 10 | 4 | kullanıcının kurmadığı mecaz | Yani mesele ilacın kendisi değil, tek başına taşımak. |
| 11 | 3 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") | Şimdi uygulama açık ve o sesle aynı odadasın. |
| 13 | 2 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") · üst üste binen yan cümle | O karar senin ve benim verebileceğim bir şey değil; ne yapacağını söyleyen biri olarak girersem, iki gündür ya |
| 14 | 3 | kullanıcının kurmadığı mecaz · üst üste binen yan cümle | Eşin parayı görüyor, sen geceyi görüyorsun; ikiniz aynı yere bakmıyorsunuz. |
| 15 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Bu ikisini birbirinden ayırman bugün oldu. |
| 16 | 3 | belirsiz gönderge ("o ölçü", "o saat") · üst üste binen yan cümle | Ama eşin bilmiyor, çocukların bilmiyor — bu cümleleri ilk kez birine yazıyorsun. |
| 17 | 4 | üst üste binen yan cümle | Ne kadarını paylaşacağın senin kararın ve iş yerinde nasıl karşılanacağını da bilemem; tahmin edersem seni yan |
| 18 | 3 | belirsiz gönderge ("o ölçü", "o saat") · üst üste binen yan cümle | Tartışmanın içinde bunun yeri yok; tartışırken ikinizden birinin haklı olması gerekiyor, oysa sen bir kısmını  |
| 20 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Başka annelerin nasıl nefes aldığını bilemem, oraya evet demeyeceğim. |
| 22 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Bugün olan şey bira değil, o cümle. |
| 24 | 3 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") | Üzülmen de bir şeyin hâlâ orada durduğunu gösteriyor. |
| 27 | 3 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") | Yani ikisinden hangisinin daha çok battığını aslında biliyorsun. |
| 28 | 4 | belirsiz gönderge ("o ölçü", "o saat") | İkisi aynı gecede oldu. |
| 30 | 3 | belirsiz gönderge ("o ölçü", "o saat") · üst üste binen yan cümle | Çocukluğunla ilgili anlattığın şeyin ne olduğunu söyleyemem; orası seni muayene eden hekimin işi ve ben oradan |
| 32 | 3 | belirsiz gönderge ("o ölçü", "o saat") · üst üste binen yan cümle | Ona evet diyemem; bir hafta sonra toparlanmış olacağını ben bilemem ve bilmediğim bir şeye onay verirsem seni  |

### 4b. `belirsiz_gonderge` neyi yakalıyor — kodla teşhis

Bayrak `v2 korpusu`'nda %21, `v3 korpusu`'nde %40. Judge'ın çıktısını okuyup haklı ya da haksız demek yerine (metni ben yazdım, o yargıya ben veremem), bayrağın **neyle birlikte gittiğini** kodla aradım — K61'in yöntemi.

| | işaretli | işaretsiz | Fisher p |
|---|---:|---:|---:|
| son cümlede geri-gönderme zamiri (*onu, ikisi, o cümle*) | 1/16 | 2/24 | **1.0000** |
| son paragrafta "bunu sen yaptın" kapanışı | 0/16 | 2/24 | 0.5077 |

**Bulgu:** ilişki **YOK** (p = 1.0000). Bu korpusta bayrak son cümlenin zamiriyle birlikte gitmiyor. Kapanış retoriğiyle ilişkisi yok (p = 0.51).

> ⚠️ **Bu, cümlelerin gerçekten anlaşılmaz olduğunu göstermez.** Her örnekte göndergenin adı bir-iki cümle önce geçiyor; bu normal Türkçe bağlaşıklığı da olabilir, uzmanın şikâyet ettiği belirsizlik de. **Bunu metni yazan taraf karara bağlayamaz** — uzman Oturum 3'e gider (K58: ikinci değerlendirici).

**Ayrı ve judge'dan bağımsız bulgu:** kayıtların **2/40**'ü son paragrafını aynı retorikle kapatıyor (*"bunu sen yaptın / sen söyledin / senin yaptığın"*): #5, #26. Korpus raporu bunu göremez, çünkü §5a kapanışın **türünü** sayıyor, **ifadesini** değil. v2'nin 68/70 soruyla bitme kusuru başka bir eksende tekrarlıyor olabilir.

### 4c. Uzunluk karıştırıcısı — bantlarda eşleştirilmiş karşılaştırma

Cevap uzunluğu medyanı: `v2 korpusu` **170** · `v3 korpusu` **284** karakter. Uzun cevapta daha çok cümle, daha çok gönderge ve bayrağın ateşlemesi için daha çok fırsat var. Ham fark uzunluktan geliyor olabilir; aynı uzunluk bandındaki kayıtları karşılaştırmak bunu ayırır.

| Uzunluk bandı (karakter) | v2 korpusu | v3 korpusu | Fisher p |
|---|---|---|---:|
| 0-180 | 44 kayıt | 4 kayıt | _n yetersiz, karşılaştırılamaz_ |
| 180-260 | 4/22 (%18) | 4/11 (%36) | 0.391 |
| 260+ | 2 kayıt | 25 kayıt | _n yetersiz, karşılaştırılamaz_ |

**Okuma:** ham `belirsiz_gonderge` farkı uzunlukla karışıyor. Bantlarda fark küçülüyor ya da kayboluyor; en uzun bantta karşılaştırma yapılamıyor çünkü bir tarafta neredeyse hiç kayıt yok. **Ham farkı tek başına bulgu saymak yanıltıcı olur.**

## 5. Tarama boyutları (❌ kalite kanıtı DEĞİL — K61)

Buradaki sayılar **kaliteyi ölçmüyor**; korpusta neyin ateşleyip ateşlemediğini görmek için duruyor.

| Ölçüm | v2 korpusu | v3 korpusu |
|---|---|---|
| `dogallik` ortalama | 4.97 (n=68) | 5.00 (n=40) |
| `mi_uyumu` ortalama | 4.88 (n=68) | 5.00 (n=40) |
| `grounding` ortalama | 4.94 (n=68) | 5.00 (n=40) |
| EPITOME duygusal tepki | 1.12 (n=68) | 1.18 (n=40) |
| EPITOME yorumlama | 1.38 (n=68) | 1.55 (n=40) |
| EPITOME keşif | 1.66 (n=68) | 0.85 (n=40) |

| Doğallık bayrağı | v2 korpusu | v3 korpusu |
|---|---|---|
| `siz_kaymasi` | 0/68 | 0/40 |
| `klise_acilis` | 0/68 | 0/40 |
| `terapi_jargonu` | 2/68 | 0/40 |
| `bos_guvence` | 0/68 | 0/40 |
| `ovgu_tonu` | 0/68 | 0/40 |

| OARS becerisi (judge'a göre) | v2 korpusu | v3 korpusu |
|---|---|---|
| `yansitma_var` | 59/68 (%87) | 39/40 (%98) |
| `karmasik_yansitma` | 46/68 (%68) | 28/40 (%70) |
| `takdir_var` | 10/68 (%15) | 10/40 (%25) |
| `ozet_var` | 5/68 (%7) | 12/40 (%30) |
| `ozerklik_vurgusu` | 7/68 (%10) | 10/40 (%25) |

| TIP 35 tuzağı (judge'a göre) | v2 korpusu | v3 korpusu |
|---|---|---|
| `tuzak_uzman` | 0/68 | 0/40 |
| `tuzak_etiketleme` | 0/68 | 0/40 |
| `tuzak_soru_cevap` | 0/68 | 0/40 |
| `tuzak_erken_odak` | 0/68 | 0/40 |
| `tuzak_suclama` | 1/68 | 0/40 |
| `tuzak_erken_tavsiye` | 0/68 | 0/40 |

## 6. Okuma

**1. `anlasilirlik` ortalaması 4.25 → 4.15**, kusursuz oranı %46 → %48 (p = 1.000, tesadüf bandında).

**2. Anlamlı fark gösteren bayrak(lar):** `belirsiz gönderge ("o ölçü", "o saat")` arttı (%21 → %40, p = 0.044). ⚠️ **Ama §4c'ye bakın:** bu bayrak cevap uzunluğuyla karışıyor ve uzunluk bantlarında eşleştirildiğinde fark küçülüyor ya da kayboluyor. Ham anlamlılık tek başına yeterli değil.

**Bayrak bayrak yön:**

| Kusur | v2 korpusu | v3 korpusu | yön | p |
|---|---:|---:|---|---:|
| kullanıcının kurmadığı mecaz | %24 | %15 | ↓ | 0.332 |
| belirsiz gönderge ("o ölçü", "o saat") | %21 | %40 | ↑ | 0.044 |
| üst üste binen yan cümle | %28 | %25 | ↓ | 0.824 |
| devrik / eksiltili cümle | %1 | %0 | ↓ | 1.000 |
| soyut adlaştırma | %1 | %5 | ↑ | 0.554 |

**3. Soruyla biten cevap 66/68 → 20/40.** EPITOME `keşif` büyük ölçüde soruyla taşınıyor; bu iki sayı birlikte okunmalı, keşif düşüşü tek başına kalite kaybı sayılmaz.

**4. Güvenlik bayrakları:** klinik ihlal 0/40, rol sınırı 0/40, cevapsız soru 0/40. Bu bayrakların ayrım gücü hiç ölçülmedi (K61); **yokluk kanıt değildir**.

### ⚠️ Gücün sınırı

n = 68 ve n = 40 ile oran farklarının %95 aralıkları ±15 puan civarında. Yani bu araç, **aramaya çalıştığımız büyüklükteki farkları tek partide ayırt edemiyor**. Tek partide çıkan bir fark, bir sonraki partide doğrulanmadan bulgu sayılmamalı.

