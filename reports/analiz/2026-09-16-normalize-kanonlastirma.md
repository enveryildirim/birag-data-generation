# `normalize.py` — ailenin sekizincisi, ve ilk kez kusur **sessizce yanlış değer**

**Betik:** `scripts/analiz/2026-09-16-normalize-kanonlastirma.py` · **Tarih:** 2026-09-16  
**Girdi:** `src/normalize.py` SHA256 `548c5c49ba59aef8` (fonksiyonlar **çağrılıyor**)  
**Girdi:** `configs/taxonomy.yaml` SHA256 `70f9697deeb68cdc`  
**Girdi:** `data/seeds.jsonl` SHA256 `0631c02ec7510af3` — **2240** tohum

---

## 1. ⭐ Bir site BAĞIŞIK — ve sebebi öğretici

`normalize.py`'de düz `.lower()` kullanan dört yer vardı. ⭐ Biri bu aileden
**etkilenmiyor**: `slug()` küçülttükten sonra `ç ğ ı ö ş ü` → `c g i o s u`
eşlemesi yapıyor, yani **`ı` ile `i` ayrımını tasarım gereği yok sayıyor**.
Her iki okuma da aynı slug'a düşüyor:

| girdi | `slug()` |
|---|---|
| `ilaç` | `ilac` |
| `ILAÇ` | `ilac` |
| `İLAÇ` | `ilac` |
| `ılaç` | `ilac` |

➡️ *Bir fonksiyonun bu aileden korunmuş olması dikkatten değil, ayrımı hiç*
*KULLANMAMASINDAN geliyor — `i_sinifi`'nin yaptığı şeyin aynısı, yalnızca*
*başka bir sebeple.* ⇒ Kural olarak: **ayrımı taşımak zorunda olmayan her yer**
**onu düşürmeli**; taşımak zorunda olan yer de sınıf kullanmalı.

---

## 2. ⭐⭐ Kusurun TÜRÜ değişti — fallback değil, **yanlış kova**

T73 ve T75'te kusurun biçimi hep *«kapı ateşlemiyor»*du: eksik bir uyarı
görünür bir şey bırakmaz ama **yanlış bir şey de söylemez**. ⛔ Burada iki
ayrı sonuç var ve ikincisi bu ailede **ilk**:

| girdi | eski sonuç | doğru | tür |
|---|---|---|---|
| `norm_egitim('İlkokul')` | `belirtilmemis` | `ilkokul` | ⚠️ fallback — **izi var** |
| `norm_egitim('LİSE')` | `belirtilmemis` | `lise` | ⚠️ fallback — **izi var** |
| `norm_sure('3 YILDAN FAZLA')` | `1_3_yil` | `3_10_yil` | ⛔⛔ **YANLIŞ KOVA — izi YOK** |

⛔⛔ *`3 YILDAN FAZLA` kaydı `1_3_yil` oluyor: çıktı **geçerli görünüyor**,
hiçbir alan «bilinmiyor» demiyor, ve kaydın 3+ yıllık kullanımı sessizce
1-3 yıla iniyor.* ➡️ **Bir kapının ateşlememesi ölçülebilir bir eksikliktir;**
**bir dönüştürücünün yanlış değer üretmesi ölçülemez bir yalandır.**

---

## 3. Matris — her site, beş yazım biçimi

### 3a. `norm_egitim`

| yazım | `lisansüstü` | `yüksek lisans` | `mba` | `üniversite` | `lisans` | `lise` | `ortaokul` | `ilkokul` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| olduğu gibi | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Başlık Yazımı** (`İlkokul`) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⛔ |
| **doğru TR BÜYÜK** | ⛔ | ⛔ | ✅ | ⛔ | ⛔ | ⛔ | ✅ | ⛔ |
| ASCII `.upper()` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| ⚠️ **aksansız** (`Universite`) | ⛔ | ⛔ | ✅ | ⛔ | ✅ | ✅ | ✅ | ✅ |

*(hücre = **eski**; `⁄⛔` varsa canlı da kaçırıyor)*

| yazım | eski ölü | 
|---|---:|
| olduğu gibi | **0**/8 |
| **Başlık Yazımı** (`İlkokul`) | **1**/8 |
| **doğru TR BÜYÜK** | **6**/8 |
| ASCII `.upper()` | **0**/8 |
| ⚠️ **aksansız** (`Universite`) | **3**/8 |

✅ **Canlı `norm_egitim` ölü hücre: 0/40.**


### 3b. `_keyword` (`stres_tipi` — taksonomiden gelen anahtarlar)

| yazım | eski ölü anahtar | canlı ölü anahtar |
|---|---:|---:|
| olduğu gibi | **0**/76 | ✅ **0**/76 |
| **Başlık Yazımı** (`İlkokul`) | **6**/76 | **1**/76 |
| **doğru TR BÜYÜK** | **37**/76 | ✅ **0**/76 |
| ASCII `.upper()` | **8**/76 | ✅ **0**/76 |
| ⚠️ **aksansız** (`Universite`) | **16**/76 | **13**/76 |

⚠️ *«Ölü anahtar»* burada *«yanlış kanona düştü ya da hiç eşleşmedi»* demek —
ikisi ayrılmadı, çünkü ikisi de aynı sonucu doğuruyor: **kayıt yanlış etiketlenir**.

### 3b′. ⛔⛔ `_keyword` DÜZELTİLMEDİ — ve sebebi bu raporun en önemli kısmı

`tr_fold` bu siteye de uygulandı ve ⛔ **gerileme üretti**: taban durumda (hiç büyük harf yokken) **2 anahtar yanlış kanona düştü**.

| anahtar | beklenen | i-sınıfından sonra | sebep |
|---|---|---|---|
| `kaçış` | `ritüel_bagimliligi` | ⛔ `is_stresi` | `kaçış` → `kaçiş`, içinde **`iş`** var |
| `alışkanlık` | `ritüel_bagimliligi` | ⛔ `is_stresi` | `alışkanlık` → `alişkanlik`, içinde **`iş`** var |

⭐ Sebep i-sınıfının kendisi değil: **anahtarlar kısa alt-dizeler.** 18 anahtar ≤4 karakter (`iş`, `eş `, `boş`, `aile`, `okul`, `para`…). Bir karakter sınıfını genişletmek, kısa alt-dize eşleşmesinde **hemen** çakışma üretir.

⭐⭐ **Ve altında DAHA ESKİ bir kusur var — kasingden bağımsız, bugün de açık:**

| metin | `_keyword` bugün | |
|---|---|---|
| `girişimci bir hayatım var` | `is_stresi` | ⛔ **yanlış** |
| `gelişim çağında` | `is_stresi` | ⛔ **yanlış** |
| `değişim istiyorum` | `is_stresi` | ⛔ **yanlış** |
| `iş kurmayı düşünüyorum` | `is_stresi` | ✅ doğru |

⛔ `iş` anahtarı **kelime içinde** eşleşiyor. Bu **K65'in ailesi** ve çözümü `checks.KLINIK_IDDIA`'da zaten uygulanmış (`\b` + Türkçe ek serbest) — `_keyword`'e hiç gelmemiş.

➡️⭐⭐ *i-sınıfı kusuru YARATMADI; zaten bozuk olan eşleştiriciyi GENİŞLETİP*
*GÖRÜNÜR KILDI. Ve bu, düzeltmeyi uygulamamak için yeterli sebep: iki kusuru*
*birden kapatmak (`\b` + i-sınıfı) etiket semantiğini değiştirir, etkisi ancak*
*HAM kampanya meta'sına karşı ölçülebilir, ve o veri onaylı kaynak klasöründe*
*(Kural 1).* ⛔ **Ölçülmeden değiştirilmedi** — K40: kalibre edilmemiş kapı veri
öldürür. ⚠️ Gerekçe `normalize._keyword` docstring'ine yazıldı, kusur gizlenmiyor.

### 3c. `norm_sure`

| girdi | yazım | eski | canlı |
|---|---|---|---|
| `3 yıldan fazla` | **doğru TR BÜYÜK** | ⛔ **`1_3_yil`** | ✅ `3_10_yil` |
| `3 yıldan fazla` | ASCII `.upper()` | ⛔ **`1_3_yil`** | ✅ `3_10_yil` |

⛔ Eski: **2** yanlış sonuç · ✅ Canlı: **0**.

---

## 4. ⛔ Hasar ÖLÇÜLEMİYOR — yalnızca üst sınır, o da her alanda değil

`data/seeds.jsonl` **kanonik** meta taşıyor, **ham** meta'yı değil. Ham veri
onaylı kaynak klasöründe ve ⛔ **Kural 1 gereği sorulmadan okunmuyor**. ⇒ Burada
yalnızca **üst sınır** ölçülebiliyor: bir kayıt fallback değere düştüyse sebebi
bu kusur **olabilir** (ya da alan gerçekten boştur).

| alan | fallback değeri | kayıt | üst sınır |
|---|---|---:|---|
| `egitim` | `belirtilmemis` | **80** | ≤ **80** (%3.6) |
| `stres_tipi` | `None` | **35** | ≤ **35** (%1.6) |
| `kullanim_suresi` | `belirtilmemis` | **0** | ⛔⛔ **ÜST SINIR YOK** — kusur fallback değil **yanlış kova** üretiyor, iz bırakmıyor |

⭐ **Kampanyaya göre dağılım — kümelenme bir işarettir:**

| kampanya | `egitim=belirtilmemis` | `stres_tipi=None` |
|---|---|---|
| `davranissal` | 0/520 (%0.0) | 0/520 (%0.0) |
| `dijital` | 0/200 (%0.0) | 15/200 (%7.5) |
| `kimyasal_madde` | 50/1100 (%4.5) | 20/1100 (%1.8) |
| `receteli_ilac` | 30/420 (%7.1) | 0/420 (%0.0) |

⚠️ **Kümelenme kanıt DEĞİL, işarettir.** Yazım biçimi kampanyaya göre değişiyorsa
kusur da kampanyaya göre kümelenir — ama alanın gerçekten boş bırakılması da
kampanyaya göre kümelenir. ⛔ İkisini ayıran tek şey **ham veri**.

---

## 5. ⚠️ Kapanmayan sınıf — **aksan düşürme** ayrı bir aile üyesi

`tr_fold` `i/ı/İ/I` ayrımını kaldırıyor ama `ü→u`, `ş→s`, `ğ→g` **değil**.
Türkçe klavyesi olmayan biri `Universite` yazar ve bu hâlâ eşleşmiyor:

| aksansız yazım | canlı sonuç |
|---|---|
| `lisansustu` | `lisansustu` |
| `yuksek lisans` | `lisansustu` |
| `mba` | `lisansustu` |
| `universite` | `universite` |
| `lisans` | `universite` |
| `lise` | `lise` |

⛔ Aksansız yazımda **0/8** kural hâlâ ölü: .

✅ **2026-09-16'da KAPATILDI (T84)** — ama yalnızca `norm_egitim` ve
`norm_sure`'de. `tohum_guvenlik.tr_sadelestir` aksanı da düşürüyor; bedeli
**önce ölçüldü**: taksonomide çakışma **yok**, ham 2240 kayıtta `egitim`
farkı **0**.

⛔⭐⭐ **`_keyword`'e UYGULANMADI ve sebebi ölçümden çıktı:** aksansız `iş` →
`is` olunca **`isolation`** içinde eşleşiyor. Bugün kural sırası bunu
maskeliyor (`monotony_isolation` önce `monoton`a düşüyor) ⚠️ ama maskeyi
tasarım değil **rastlantı** tutuyor. Kazanç 5 tartışmalı kayıt (`bos_zaman_caresizlik` → `yalnizlik`), risk **sessiz yanlış etiket** ⇒
uygulanmadı. ➡️ *Aynı modülde iki fold bir karmaşa değil, iki farklı RİSK*
*profilinin karşılığıdır — T80'in «yönü kapı belirler» dersinin ikinci*
*uygulanışı.*

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔⛔ **Gerçek hasar** | ölçülemedi — ham meta onaylı kaynak klasöründe, Kural 1. ⚠️ `kullanim_suresi` için **üst sınır bile yok** |
| ⛔ `data/seeds.jsonl` **yeniden üretilmedi** | düzeltilmiş `normalize.py` ile yeniden koşmak ham veriyi okumayı gerektirir; yapılmadı |
| ⛔ **Aksan düşürme sınıfı açık** (§5) | kapatmanın yan etkisi ölçülmedi |
| ⚠️ `_exact` / `_prefix` / `_contains` | hiç normalizasyon **kullanmıyor** (tasarım gereği: takma adlar kaynaktan birebir alınmış). ⛔ Ama bu, aynı kırılganlığın **daha sert** biçimi ve ayrıca sınanmadı |
| ⚠️ Kural listesi **elle** | `EGITIM_KURALLARI` betikte kopya duruyor çünkü `norm_egitim` onu gövdesinde taşıyor; kaynak değişirse **bu betik de** güncellenmeli |

