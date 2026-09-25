# Ham meta okundu — üst sınırların ikisi de UÇTA çıktı

**Betik:** `scripts/analiz/2026-09-16-ham-meta-hasari.py` · **Tarih:** 2026-09-16  
**Girdi:** `src/normalize.py` SHA256 `548c5c49ba59aef8` (fonksiyonlar **çağrılıyor**)  
**Girdi:** `configs/taxonomy.yaml` SHA256 `70f9697deeb68cdc`  
**Girdi:** `data/seeds.jsonl` SHA256 `0631c02ec7510af3`  
**Girdi (repo DIŞI):** onaylı kaynak korpusu — ⚠️ **kullanıcı 2026-09-16'da açıkça izin verdi** (Kural 1). ⧉ işareti *«repo dışı: SHA kayıtlı, burada doğrulanamaz»* demektir:  
· ⧉ `campaigns/kimyasal_madde/total_output.jsonl` SHA256 `284ca0ed6bf1118c`  
· ⧉ `campaigns/dijital/total_output.jsonl` SHA256 `c1b14a4381a0e9df`  
· ⧉ `campaigns/receteli_ilac/total_output.jsonl` SHA256 `f342f74e6174f2aa`  
· ⧉ `campaigns/davranissal/total_output.jsonl` SHA256 `3dd353944d50ac7f`  

**2240** ham kayıt · yalnızca `meta` alanı okundu.

---

## Neden

T76 üç kusur ölçtü ama **gerçek hasarı ölçemedi**: `data/seeds.jsonl`
**kanonik** meta taşıyor, ham meta onaylı kaynak klasöründeydi. ⚠️ Bu betiğin
repo **dışında** bir girdisi var — reponun **tek** örneği — ve kaynak
dosyaların SHA256'sı bu yüzden ilan ediliyor.

---

## 1. ⭐⭐ İki kusur, iki uç — üst sınırın sıkılığı önceden bilinemezmiş

| kusur | T76'daki üst sınır | **gerçek** | |
|---|---|---:|---|
| `egitim` → `belirtilmemis` (⚠️ **izi var**) | ≤ **80** | **80** | ⛔ **üst sınırın TAMAMI** |
| `kullanim_suresi` → yanlış kova (⛔ **izi yok**) | ⛔ *üst sınır yoktu* | **0** | ✅ **hiç ateşlememiş** |

➡️⭐⭐ *İzi **olan** kusur üst sınırın **tamamını** doldurmuş: her*
*`belirtilmemis` bir kayıp değerdi, alanın gerçekten boş olduğu **tek bir***
***kayıt bile yok**. İzi **olmayan** kusur ise **hiç** gerçekleşmemiş.*

⇒ *«%3,6, muhtemelen abartı»* demek ile *«izi yok, demek ki olmadı»* demek
**aynı ölçüde temelsizdi** — ve ikisi de yanlış olurdu, **ters yönlerde**.

---

## 2. `egitim` — 80 kayıt, tek bir değerden

| ham değer | eski | doğru | kayıt |
|---|---|---|---:|
| `İlkokul` | ⛔ `belirtilmemis` | ✅ `ilkokul` | **80** |

| kampanya | etkilenen |
|---|---:|
| `kimyasal_madde` | 50/1100 (%4.5) |
| `receteli_ilac` | 30/420 (%7.1) |

⚠️ **Kaybedilen değer rastgele değil:** `ilkokul` taksonomideki **en düşük**
eğitim düzeyi. ⇒ Üretim eğitim düzeyine göre kayıt üslubu ayarlıyorsa (T25 /
K42 register ekseni), bu 80 tohum **en düşük register dilimini temsil eden**
**dilim**di ve `belirtilmemis` olarak üretime girdi. ⛔ Etkisi bu betikle
ölçülmedi: üretilmiş kayıtlarda register ayrı bir ölçüm.

---

## 3. `kullanim_suresi` — kusur gerçek, ateşleme sıfır

Ham veride **38** ayrık süre değeri var ve ⭐ **4** tanesi büyük harf içeriyor: `Düzenli içiciliği 2-5 yıl; bebek doğumundan sonra son 1-5 ayda günlük/neredeyse günlük haline geldi`, `Düzenli içiciliği 5-12 yıl; son 1-2 yılda akşam yemeği sonrası düzene oturdu`, `Önceki kullanım 10-20 yıl; bırakma süresi 6 ay - 2 yıl; nüks sonrası 3 gün - 6 hafta`, `Önceki kullanım 8-15 yıl; bırakma süresi 1-3 yıl; nüks sonrası 2-4 hafta`

⇒ `norm_sure`'ün *«yanlış kova»* kusuru **hiç tetiklenmedi**. ⚠️ Bu kapıyı
masum yapmaz: kusur duruyordu ve tetiklenmemesinin sebebi **kaynağın yazım**
**alışkanlığı**ydı — T73'te `scan_forbidden` için yazılan cümlenin aynısı:
*bir kapının güvenliği girdinin bugünkü huyuna bağlıysa ölçülmüş değil,*
*ödünç alınmıştır.* ✅ Artık ölçülmüş: kusur kapatıldı **ve** bedelinin sıfır
olduğu gösterildi.

---

## 4. ⭐⭐ `_keyword` kararı — dört aday, ham veriye karşı

T76 `_keyword`'ü **bilerek düzeltmemişti**: i-sınıfı gerileme üretiyordu ve
etkisi ancak ham meta'ya karşı ölçülebilirdi. ⇒ Dört aday ölçüldü.

| aday | değişen kayıt | düzeltme | ⛔ gerileme |
|---|---:|---:|---:|
| ① yalnız **i-sınıfı** | 25 | ✅ **20** | ⛔ **5** |
| ② yalnız **kelime başı** | 24 | ✅ **0** | ⛔ **24** |
| ③ i-sınıfı + kelime başı | 44 | ✅ **20** | ⛔ **24** |
| ④ ⭐ ③ + `_`→boşluk — **uygulanan** | 20 | ✅ **20** | ✅ **0** |

**Gerilemelerin sebepleri — her biri ayrı bir ders:**

| aday | gerileme | sebep |
|---|---|---|
| ① i-sınıfı | `Aile çatışması stresi` → `is_stresi` | `çatışması` → `çatişmasi`, içinde **`iş`** var. ⇒ *Sınıf genişletmek, kısa alt-dize eşleşmesinde hemen çakışır* |
| ②③ kelime başı | `physical_fatigue` → `None` | ⛔ `_` bir **kelime karakteri**: `fatigue`'ün önünde `\b` yok. ⇒ *`snake_case` bir sözcük değil, iki sözcüktür ve regex bunu bilmez* |

⭐ **Uygulanan: ④** — i-sınıfı + `_`→boşluk + kelime başı. Ham 2240 kayıtta **20 düzeltme, 0 gerileme**.

⛔ **`.strip()` ve `\w*` bilerek EKLENMEDİ:** `"eş "` anahtarının sondaki
boşluğu kasıtlı (`eşya`/`eşit` eşleşmesin diye) ve ek serbestliği `\b`'den
zaten geliyor (`\biş` → `işim` ✅, `girişimci` ⛔). ➡️ *Bir kusuru kapatırken*
*anlambilimi genişletmemek ayrı bir iştir; ölçüm iyileşmeyi gösterir ama*
*genişlemeyi göstermez.*

---

## 5. ⛔⛔ **AMA ALAN DÜZEYİNDE ETKİ SIFIR — T60 tekrarladı**

§4'teki **20 düzeltme** bir **fonksiyon düzeyi** sayısıdır. Alan düzeyinde
ölçülünce **0** çıkıyor ve sebebi `normalize()`'ın kısa devre zinciri:

```python
out["stres_tipi"] = (_exact(...) or _keyword(...) or ("yok" if ... else None))
```

| | kayıt |
|---|---:|
| ham kayıt | 2240 |
| ⛔ `_exact` zaten yakalıyor (⇒ `_keyword` **hiç koşmuyor**) | **374** |
| `_keyword`'e ULAŞAN | **1866** (%83.3) |
| ⭐ bunlar içinde **etiketi değişen** | **0** |

⭐⭐ **Sebep keskin:** kasing kusurunun vurduğu 20 kayıt (`İş stresi` — Türkçe,
karışık büyük harf) tam olarak `_exact`'in **zaten kapsadığı** kayıtlar;
`_keyword`'e ulaşan her şey İngilizce `snake_case` (`ambivalence_contradiction`,
`boundary_pressure`…) ve içinde **tek bir Türkçe harf yok**.

➡️⭐⭐ *Kusurun gerçekleşmesi için İKİ koşul birden gerekiyordu — metin Türkçe*
*olacak VE `_exact` kapsamayacak — ve bu korpusta ikisi **hiç bir arada***
***oluşmadı**. Kusur gerçekti, erişilemezdi.*

⛔⛔ **Ve bu, T60'ın dersinin ikinci kez çıkması:** *bir sayı, RAPORLANDIĞI*
*düzeyde ölçülmelidir.* T60'da aynı sızıntı bayrak düzeyinde **%40**, kapı
düzeyinde **%0**'dı. Burada aynı düzeltme fonksiyon düzeyinde **20**, alan
düzeyinde **0**. ⚠️ Ben de §4'ü ilkin *«20 düzeltme»* diye yazdım ve tohum
dosyası yeniden üretilince farkın **çıkmadığını** görünce düzelttim.

⚠️ Düzeltme yine de **doğru**: alt-dize kusuru (`girişimci` → `is_stresi`)
serbest metinli Türkçe bir `stress_type` değeri geldiği gün ateşlerdi ve
bugün ateşlememesinin sebebi yine **kaynağın yazım alışkanlığı**.

---

## 6. ⛔⭐⭐ Tohum havuzu YENİDEN ÜRETİLDİ, sonra GERİ ALINDI — ve sebebi bir ders

Düzeltilmiş kodla `data/seeds.jsonl` yeniden üretildi (**80/2240** kayıt
değişiyor, yalnızca `meta.egitim`). ⛔ **Ama üzerine yazmak yanlıştı ve bunu
gösteren şey ilan edilen SHA denetimi oldu:**

⛔ **10 geçmiş rapor** `data/seeds.jsonl`'ın **hash'ini ilan ediyor**, ve
bunların bir kısmının **çıktısı DONDURULMUŞ** (`data/plan/v3-parti*.jsonl`,
`v4-parti1.jsonl` — üretime girmiş örneklem planları). Onları yeniden koşmak
**tarihi yeniden yazmak** olurdu; koşmamak ise kaynak dosya değiştiği için
kayıt zincirini **doğrulanamaz** bırakırdı.

· `2026-09-12-kullanici-mesaji-bicimi.md`  
· `2026-09-12-turkce-register-sondasi.md`  
· `2026-09-14-golden-bolme.md`  
· `2026-09-14-kriz-filtresi-bedensel-acik.md`  
· `2026-09-14-uzman-ornekleme.md`  
· `2026-09-14-v3-ornekleme.md`  
· `2026-09-15-normalizasyon-olu-desen.md`  
· `2026-09-15-rag-soru-envanteri.md`  
· `2026-09-16-normalize-kanonlastirma.md`  
· `2026-09-16-tohum-alani-tuketimi.md`  

✅ **Yapılan:** `data/seeds.jsonl` **bayt bayt geri alındı**; düzeltilmiş havuz
**`data/seeds.v2.jsonl`** olarak yazıldı (2240 tohum). ⇒ Geçmiş
raporların ilan ettiği hash tutmaya devam ediyor, düzeltme de kayboldu değil.

➡️⭐⭐ *Ders: **değişmezlik ilan edilen bir özellik değil, KEŞFEDİLEN bir***
***özelliktir.** `datasets/` için Kural 4 bunu açıkça yazıyor; `data/seeds.jsonl`
*için hiçbir kural yazmıyordu — ama hash'ini ilan eden rapor sayısı onun*
*fiilen değişmez olduğunu söylüyordu. Bir artefaktın dokunulabilir olup*
*olmadığını anlamanın yolu kuralı okumak değil, **kim hash'ine atıf veriyor***
***diye saymaktır.*** ⚠️ Ve bunu bana kural değil **denetim** söyledi:
`ilan-edilen-sha-denetimi` üzerine yazdıktan sonra `⛔ tutmuyor` dedi.

| | |
|---|---:|
| `data/seeds.jsonl` (v1, **dokunulmadı**) | 2240 tohum |
| `data/seeds.v2.jsonl` (**düzeltilmiş**) | 2240 tohum |
| değişen kayıt | **80** (%3.6) |
| değişen alan | yalnızca `meta.egitim` |
| kaybolan / yeni `seed_id` | **0** / **0** |

⭐ **Kayıt izleri korundu:** `seed_id = sha256(source_id)[:16]` — meta'dan
**türemiyor**. ⚠️ Bu **önceden** kontrol edildi; türeseydi yeniden üretim
`datasets/*`'ın `source_ids` bağlarını kırardı.

⛔ **Hangi havuzun kullanılacağı bir KARAR:** Faz 4 üretimi `seeds.v2` ile
koşmalı; ⚠️ ama o zaman v1'den üretilmiş kayıtlarla v2'den üretilenler aynı
sette karışır ve bu **kayıtta görünmüyor**. `plan.md`'ye açık kalem.

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔ **v1/v2 karışımı kayıtta görünmüyor** | hangi kaydın hangi havuzdan üretildiği `gen_meta`'da yazmıyor; `seeds.v2` kullanılmaya başlanırsa bu **önce** çözülmeli |
| ⛔ **Üretilmiş kayıtlara etkisi** | 80 tohum `belirtilmemis` eğitimle üretime girdi; bunun üretilen metnin **register**'ine ne yaptığı ayrı bir ölçüm ve **yapılmadı** (T25 / K42 ekseni) |
| ⛔ **Aksan düşürme sınıfı** | hâlâ açık: `Universite` yazımı `belirtilmemis` verir. Ham veride geçmiyor (ölçüldü) ama kapatılmadı |
| ⚠️ **Repo dışı girdi** | bu betik reponun **tek** dış bağımlılığı; kaynak klasör erişilemezse rapor sayı üretmez ve bunu yazar |
| ⚠️ Yalnızca **üç alan** | `egitim`, `kullanim_suresi`, `stres_tipi`. `_exact`/`_prefix`/`_contains` hiç normalizasyon kullanmıyor ve **sınanmadı** |
| ⛔ *«Bugün ateşlemiyor»* ≠ *«güvenli»* | hem `norm_sure` hem `_keyword` kusurları gerçekti ve tetiklenmemelerinin sebebi **kaynağın yazım alışkanlığı**ydı — ödünç alınmış güvenlik (T73) |

