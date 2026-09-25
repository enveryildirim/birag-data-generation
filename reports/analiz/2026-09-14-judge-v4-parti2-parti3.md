# judge v4 — `v3 parti 3` · `v3 parti 2` ile karşılaştırma

**Girdi 1 (v3 parti 2):** `data/judged/v3-parti2-tam.jsonl` · SHA256 `7b5294f5dbf4c8d05565ed28a70743e1c0799d69c629d4347739879ff4871133` · 40 puanlanan kayıt  
**Girdi 2 (v3 parti 3):** `data/judged/v3-parti3.jsonl` · SHA256 `6cb1815c299ef741742cd5ae30cc71c960f17b1fbdd4153e0a267c32e0839f73` · 24 kayıt  
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

| Puan | v3 parti 2 | v3 parti 3 |
|---|---:|---:|
| 5 | 19 (%48) | 9 (%38) |
| 4 | 9 (%22) | 13 (%54) |
| 3 | 11 (%28) | 2 (%8) |
| 2 | 1 (%2) | 0 (%0) |
| 1 | 0 (%0) | 0 (%0) |

| Ölçüm | v3 parti 2 | %95 aralık | v3 parti 3 | %95 aralık | p |
|---|---|---|---|---|---|
| kusursuz (puan = 5) | 19/40 (%48) | %33-63 | 9/24 (%38) | %21-57 | 0.603 — |
| iki+ kusur (puan ≤ 3) | 12/40 (%30) | %18-45 | 2/24 (%8) | %2-26 | 0.061 — |

Ortalama: v3 parti 2 **4.15** · v3 parti 3 **4.29**

## 2. Anlaşılırlık kusurları — bayrak bayrak

Puan bu beş bayraktan hesaplanıyor; hangi kusurun değiştiğini gösterir.

| Kusur | v3 parti 2 | %95 aralık | v3 parti 3 | %95 aralık | p |
|---|---|---|---|---|---|
| kullanıcının kurmadığı mecaz | 6/40 (%15) | %7-29 | 4/24 (%17) | %7-36 | 1.000 — |
| belirsiz gönderge ("o ölçü", "o saat") | 16/40 (%40) | %26-55 | 9/24 (%38) | %21-57 | 1.000 — |
| üst üste binen yan cümle | 10/40 (%25) | %14-40 | 3/24 (%12) | %4-31 | 0.339 — |
| devrik / eksiltili cümle | 0/40 (%0) | %-0-9 | 1/24 (%4) | %1-20 | 0.375 — |
| soyut adlaştırma | 2/40 (%5) | %1-17 | 0/24 (%0) | %0-14 | 0.524 — |

## 3. `cevapsiz_soru` ve güvenlik bayrakları

| Ölçüm | v3 parti 2 | %95 aralık | v3 parti 3 | %95 aralık | p |
|---|---|---|---|---|---|
| cevapsız soru | 0/40 (%0) | %-0-9 | 0/24 (%0) | %0-14 | 1.000 — |
| klinik güvenlik ihlali | 0/40 (%0) | %-0-9 | 0/24 (%0) | %0-14 | 1.000 — |
| rol sınırı ihlali | 0/40 (%0) | %-0-9 | 0/24 (%0) | %0-14 | 1.000 — |

## 4. Elle incelenecek kayıtlar — 15/24

| # | anlaşılırlık | judge'ın işaretlediği | judge'ın seçtiği cümle |
|---:|---:|---|---|
| 1 | 4 | kullanıcının kurmadığı mecaz | Şimdi masada iki ayrı şey var. |
| 2 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Büyük bir şey yapmadığını düşünmenle o anın aynı kişide durması tuhaf değil. |
| 3 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Dün gece söndürdüğün sigara, o listeye girmeyen tek şey oldu. |
| 7 | 4 | belirsiz gönderge ("o ölçü", "o saat") | O cümleyi duymanı yakınlaştıracak ilk şey ne olurdu? |
| 8 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Sabaha kadar onunla kalmışsın. |
| 9 | 4 | kullanıcının kurmadığı mecaz | Yani aynı yarım saatte hem dinleniyor hem bedel ödüyorsun. |
| 12 | 4 | belirsiz gönderge ("o ölçü", "o saat") | O cümleyi bugün çözmen gerekmiyor. |
| 14 | 3 | kullanıcının kurmadığı mecaz · belirsiz gönderge ("o ölçü", "o saat") | Masada iki şey duruyor. |
| 17 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Şu an aklında kalan hangisi? |
| 18 | 4 | kullanıcının kurmadığı mecaz | "Kötü görünüyor" derken başkalarının gözünü düşünüyorsun. |
| 19 | 4 | üst üste binen yan cümle | Hekiminle ne paylaşacağın senin kararın; buradan bir talimat verirsem yarın o odada duran sen olursun, ben değ |
| 20 | 4 | üst üste binen yan cümle | Midende olanın ne olduğunu ben söyleyemem; onu görecek olan bir hekim ve ben oradan konuşursam uydurmuş olurum |
| 21 | 4 | belirsiz gönderge ("o ölçü", "o saat") | Kafanın dağılması da oradan geliyor olabilir. |
| 22 | 4 | devrik / eksiltili cümle | Anahtar elindeydi ve vermedin. |
| 23 | 3 | belirsiz gönderge ("o ölçü", "o saat") · üst üste binen yan cümle | Orada yalnızca danışma hattının çalışma saatleri var, sorduğun şeye dair tek satır yok ve uydurmayacağım. |

### 4b. `belirsiz_gonderge` neyi yakalıyor — kodla teşhis

Bayrak `v3 parti 2`'nda %40, `v3 parti 3`'nde %38. Judge'ın çıktısını okuyup haklı ya da haksız demek yerine (metni ben yazdım, o yargıya ben veremem), bayrağın **neyle birlikte gittiğini** kodla aradım — K61'in yöntemi.

| | işaretli | işaretsiz | Fisher p |
|---|---:|---:|---:|
| son cümlede geri-gönderme zamiri (*onu, ikisi, o cümle*) | 0/9 | 0/15 | **1.0000** |
| son paragrafta "bunu sen yaptın" kapanışı | 0/9 | 0/15 | 1.0000 |

**Bulgu:** ilişki **YOK** (p = 1.0000). Bu korpusta bayrak son cümlenin zamiriyle birlikte gitmiyor. Kapanış retoriğiyle ilişkisi yok (p = 1.00).

> ⚠️ **Bu, cümlelerin gerçekten anlaşılmaz olduğunu göstermez.** Her örnekte göndergenin adı bir-iki cümle önce geçiyor; bu normal Türkçe bağlaşıklığı da olabilir, uzmanın şikâyet ettiği belirsizlik de. **Bunu metni yazan taraf karara bağlayamaz** — uzman Oturum 3'e gider (K58: ikinci değerlendirici).

**Ayrı ve judge'dan bağımsız bulgu:** kayıtların **0/24**'ü son paragrafını aynı retorikle kapatıyor (*"bunu sen yaptın / sen söyledin / senin yaptığın"*): #. Korpus raporu bunu göremez, çünkü §5a kapanışın **türünü** sayıyor, **ifadesini** değil. v2'nin 68/70 soruyla bitme kusuru başka bir eksende tekrarlıyor olabilir.

### 4c. Uzunluk karıştırıcısı — bantlarda eşleştirilmiş karşılaştırma

Cevap uzunluğu medyanı: `v3 parti 2` **284** · `v3 parti 3` **198** karakter. Uzun cevapta daha çok cümle, daha çok gönderge ve bayrağın ateşlemesi için daha çok fırsat var. Ham fark uzunluktan geliyor olabilir; aynı uzunluk bandındaki kayıtları karşılaştırmak bunu ayırır.

| Uzunluk bandı (karakter) | v3 parti 2 | v3 parti 3 | Fisher p |
|---|---|---|---:|
| 0-180 | 4 kayıt | 10 kayıt | _n yetersiz, karşılaştırılamaz_ |
| 180-260 | 4/11 (%36) | 2/5 (%40) | 1.000 |
| 260+ | 12/25 (%48) | 4/9 (%44) | 1.000 |

**Okuma:** ham `belirsiz_gonderge` farkı uzunlukla karışıyor. Bantlarda fark küçülüyor ya da kayboluyor; en uzun bantta karşılaştırma yapılamıyor çünkü bir tarafta neredeyse hiç kayıt yok. **Ham farkı tek başına bulgu saymak yanıltıcı olur.**

## 5. Tarama boyutları (❌ kalite kanıtı DEĞİL — K61)

Buradaki sayılar **kaliteyi ölçmüyor**; korpusta neyin ateşleyip ateşlemediğini görmek için duruyor.

| Ölçüm | v3 parti 2 | v3 parti 3 |
|---|---|---|
| `dogallik` ortalama | 5.00 (n=40) | 5.00 (n=24) |
| `mi_uyumu` ortalama | 5.00 (n=40) | 5.00 (n=24) |
| `grounding` ortalama | 5.00 (n=40) | 4.88 (n=24) |
| EPITOME duygusal tepki | 1.18 (n=40) | 1.12 (n=24) |
| EPITOME yorumlama | 1.55 (n=40) | 1.46 (n=24) |
| EPITOME keşif | 0.85 (n=40) | 0.88 (n=24) |

| Doğallık bayrağı | v3 parti 2 | v3 parti 3 |
|---|---|---|
| `siz_kaymasi` | 0/40 | 0/24 |
| `klise_acilis` | 0/40 | 0/24 |
| `terapi_jargonu` | 0/40 | 0/24 |
| `bos_guvence` | 0/40 | 0/24 |
| `ovgu_tonu` | 0/40 | 0/24 |

| OARS becerisi (judge'a göre) | v3 parti 2 | v3 parti 3 |
|---|---|---|
| `yansitma_var` | 39/40 (%98) | 24/24 (%100) |
| `karmasik_yansitma` | 28/40 (%70) | 18/24 (%75) |
| `takdir_var` | 10/40 (%25) | 7/24 (%29) |
| `ozet_var` | 12/40 (%30) | 12/24 (%50) |
| `ozerklik_vurgusu` | 10/40 (%25) | 9/24 (%38) |

| TIP 35 tuzağı (judge'a göre) | v3 parti 2 | v3 parti 3 |
|---|---|---|
| `tuzak_uzman` | 0/40 | 0/24 |
| `tuzak_etiketleme` | 0/40 | 0/24 |
| `tuzak_soru_cevap` | 0/40 | 0/24 |
| `tuzak_erken_odak` | 0/40 | 0/24 |
| `tuzak_suclama` | 0/40 | 0/24 |
| `tuzak_erken_tavsiye` | 0/40 | 0/24 |

## 6. Okuma

**1. `anlasilirlik` ortalaması 4.15 → 4.29**, kusursuz oranı %48 → %38 (p = 0.603, tesadüf bandında).

**2. Hiçbir anlaşılırlık bayrağı anlamlı fark göstermedi** (hepsi p ≥ 0.05). Bu, iki korpusun aynı olduğu anlamına gelmez; **n bu büyüklükte farkı ayırt etmeye yetmiyor** demektir.

**Bayrak bayrak yön:**

| Kusur | v3 parti 2 | v3 parti 3 | yön | p |
|---|---:|---:|---|---:|
| kullanıcının kurmadığı mecaz | %15 | %17 | ↑ | 1.000 |
| belirsiz gönderge ("o ölçü", "o saat") | %40 | %38 | ↓ | 1.000 |
| üst üste binen yan cümle | %25 | %12 | ↓ | 0.339 |
| devrik / eksiltili cümle | %0 | %4 | ↑ | 0.375 |
| soyut adlaştırma | %5 | %0 | ↓ | 0.524 |

**3. Soruyla biten cevap 20/40 → 13/24.** EPITOME `keşif` büyük ölçüde soruyla taşınıyor; bu iki sayı birlikte okunmalı, keşif düşüşü tek başına kalite kaybı sayılmaz.

**4. Güvenlik bayrakları:** klinik ihlal 0/24, rol sınırı 0/24, cevapsız soru 0/24. Bu bayrakların ayrım gücü hiç ölçülmedi (K61); **yokluk kanıt değildir**.

### ⚠️ Gücün sınırı

n = 40 ve n = 24 ile oran farklarının %95 aralıkları ±15 puan civarında. Yani bu araç, **aramaya çalıştığımız büyüklükteki farkları tek partide ayırt edemiyor**. Tek partide çıkan bir fark, bir sonraki partide doğrulanmadan bulgu sayılmamalı.

