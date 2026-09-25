# Judge v4 — kanıt → puan deseni üç boyutta

**Betik:** `scripts/analiz/2026-09-14-judge-v4-uc-boyut.py` · **Tarih:** 2026-09-14  
**v2:** `data/judged/expert-70.v2.jsonl` · SHA256 `8988a94e7be238c4a71a538638601fd3b41c821dd5e8f5a9355d0efad409850a`  
**v3:** `data/judged/expert-70.v3.jsonl` · SHA256 `1973c8398ccdebe684929d3ae757a1e74e54c4523b3edeeb8f22092846379602`  
**v4:** `data/judged/expert-70.v4.jsonl` · SHA256 `49d27215fd548c4e5907e84ea4da293e7378b3d3f2946533ed5f7231559f739f`  
**Uzman:** `data/expert_sample/uzman-puanlari.json` · SHA256 `d9d36c10691157a90173da8452ceffc47c3d88782b91bd7a8e4ecf11e492263c`  
**Üç sürümde de puanlanan ve uzmanın değerlendirdiği kayıt:** 48

> **Hipotez (K59'un devamı):** `anlasilirlik`'te işe yarayan ayrıştırma deseni `dogallik` ve `mi_uyumu`'nda da ayrım kazandırır.

> **Protokol düzeltmesi:** v3'te holistik puan sorulardan **sonra** isteniyordu, yani kontrol kirliydi. v4'te holistik puanlar **en başta** isteniyor — bu tablodaki holistik kol artık gerçek bir taban. ⚠️ Karşılığında ters yönde bir risk doğuyor: önce verilen holistik puan, sonraki ikili cevapları çıpalayabilir.

> ⚠️ **Kalibrasyon testi, genelleme testi değil.** Taksonomiler projenin kendi kaynaklarından (§C.3 OARS, §C.5 TIP 35, K20 ifade bankası, K48 register bulgusu) geliyor ama test aynı korpusta, aynı tek uzmana karşı yapılıyor.

---

## 1. Bayraklar ateşledi mi

### Anlaşılırlık (B3)

| Alan | `true` | Oran |
|---|---:|---:|
| `kurulmamis_mecaz` | 16/68 | %24 |
| `belirsiz_gonderge` | 14/68 | %21 |
| `ust_uste_yan_cumle` | 19/68 | %28 |
| `devrik_eksiltili` | 1/68 | %1 |
| `soyut_adlastirma` | 1/68 | %1 |

### Doğallık (C) ⭐

| Alan | `true` | Oran |
|---|---:|---:|
| `siz_kaymasi` | 0/68 | %0 |
| `klise_acilis` | 0/68 | %0 |
| `terapi_jargonu` | 2/68 | %3 |
| `bos_guvence` | 0/68 | %0 |
| `ovgu_tonu` | 0/68 | %0 |

### OARS becerisi (D1) ⭐

| Alan | `true` | Oran |
|---|---:|---:|
| `yansitma_var` | 59/68 | %87 |
| `karmasik_yansitma` | 46/68 | %68 |
| `takdir_var` | 10/68 | %15 |
| `ozet_var` | 5/68 | %7 |
| `ozerklik_vurgusu` | 7/68 | %10 |

### TIP 35 tuzağı (D2) ⭐

| Alan | `true` | Oran |
|---|---:|---:|
| `tuzak_uzman` | 0/68 | %0 |
| `tuzak_etiketleme` | 0/68 | %0 |
| `tuzak_soru_cevap` | 0/68 | %0 |
| `tuzak_erken_odak` | 0/68 | %0 |
| `tuzak_suclama` | 1/68 | %1 |
| `tuzak_erken_tavsiye` | 0/68 | %0 |

**Kayıt başına kusur sayısı:** `{0: 66, 1: 2}`  
**Kayıt başına tuzak sayısı:** `{0: 67, 1: 1}`  
**Kayıt başına OARS becerisi sayısı:** `{0: 7, 1: 9, 2: 38, 3: 14}`  

⚠️ v2'de `tuzak_ihlali` **liste** olarak soruluyordu ve 70 kayıtta yalnızca 2 kez doldu. İkili sorulara çevrilince: 1/68 kayıtta en az bir tuzak. Aynı kusur, uzmanın 5. maddesinde de vardı (K58).

## 2.1 `anlasilirlik`

| Kol | n | Ort. | s | Dağılım |
|---|---:|---:|---:|---|
| v2 · `anlasilirlik` | 68 | 4.26 | 0.44 | `{4: 50, 5: 18}` |
| v3 · `anlasilirlik` | 68 | 4.04 | 0.93 | `{1: 1, 2: 3, 3: 13, 4: 26, 5: 25}` |
| v4 · `anlasilirlik` | 68 | 4.25 | 0.79 | `{2: 1, 3: 12, 4: 24, 5: 31}` |
| v4 · `anlasilirlik_holistik` | 68 | 4.91 | 0.33 | `{3: 1, 4: 4, 5: 63}` |

**Uzmanın `dil_butunlugu` dağılımı:** `{1: 2, 2: 3, 3: 1, 4: 1, 5: 37}` (n=44)

### anlasilirlik — `ret` vs `kabul` · n = 5 / 32

| Kol | kötü ort. | iyi ort. | uyum oranı | %95 aralık |
|---|---:|---:|---:|:---:|
| v2 · `anlasilirlik` | 4.20 | 4.25 | 0.53 ❌ | 0.25 – 0.80 |
| v3 · `anlasilirlik` | 2.80 | 4.22 | 0.87 ✅ | 0.66 – 1.00 |
| v4 · `anlasilirlik` | 3.40 | 4.41 | 0.81 ✅ | 0.57 – 1.00 |
| v4 · `anlasilirlik_holistik` | 4.60 | 4.94 | 0.57 ❌ | 0.29 – 0.86 |

### anlasilirlik — uzman ≤ 2 vs = 5 · n = 5 / 37

| Kol | kötü ort. | iyi ort. | uyum oranı | %95 aralık |
|---|---:|---:|---:|:---:|
| v2 · `anlasilirlik` | 4.20 | 4.24 | 0.52 ❌ | 0.25 – 0.80 |
| v3 · `anlasilirlik` | 2.60 | 4.11 | 0.82 ✅ | 0.59 – 1.00 |
| v4 · `anlasilirlik` | 3.20 | 4.30 | 0.79 ✅ | 0.55 – 1.00 |
| v4 · `anlasilirlik_holistik` | 4.60 | 4.92 | 0.57 ❌ | 0.29 – 0.85 |

**Uzmanın `dil_butunlugu` puanıyla korelasyon**

| Kol | n | r |
|---|---:|---:|
| v2 · `anlasilirlik` | 44 | +0.00 |
| v3 · `anlasilirlik` | 44 | +0.42 |
| v4 · `anlasilirlik` | 44 | +0.38 |
| v4 · `anlasilirlik_holistik` | 44 | +0.30 |

> ✅ ≥ 0.75 · ⚠️ ≥ 0.60 · ❌ < 0.60 — bizim konvansiyonumuz (Kural 6).

## 2.2 `dogallik`

| Kol | n | Ort. | s | Dağılım |
|---|---:|---:|---:|---|
| v2 · `dogallik` | 68 | 3.76 | 0.62 | `{2: 3, 3: 14, 4: 47, 5: 4}` |
| v3 · `dogallik` | 68 | 3.90 | 0.67 | `{2: 1, 3: 16, 4: 40, 5: 11}` |
| v4 · `dogallik` | 68 | 4.97 | 0.17 | `{4: 2, 5: 66}` |
| v4 · `dogallik_holistik` | 68 | 4.69 | 0.49 | `{3: 1, 4: 19, 5: 48}` |

**Uzmanın `kisalik_dogallik` dağılımı:** `{1: 5, 2: 1, 4: 1, 5: 37}` (n=44)

### dogallik — `ret` vs `kabul` · n = 5 / 32

| Kol | kötü ort. | iyi ort. | uyum oranı | %95 aralık |
|---|---:|---:|---:|:---:|
| v2 · `dogallik` | 3.40 | 3.66 | 0.57 ❌ | 0.29 – 0.85 |
| v3 · `dogallik` | 3.40 | 3.81 | 0.67 ⚠️ | 0.39 – 0.94 |
| v4 · `dogallik` | 5.00 | 4.97 | 0.48 ❌ | 0.21 – 0.76 |
| v4 · `dogallik_holistik` | 4.60 | 4.62 | 0.52 ❌ | 0.24 – 0.80 |

### dogallik — uzman ≤ 2 vs = 5 · n = 6 / 37

| Kol | kötü ort. | iyi ort. | uyum oranı | %95 aralık |
|---|---:|---:|---:|:---:|
| v2 · `dogallik` | 4.00 | 3.62 | 0.35 ❌ | 0.13 – 0.57 |
| v3 · `dogallik` | 3.83 | 3.78 | 0.47 ❌ | 0.22 – 0.72 |
| v4 · `dogallik` | 5.00 | 4.97 | 0.49 ❌ | 0.24 – 0.74 |
| v4 · `dogallik_holistik` | 4.67 | 4.59 | 0.47 ❌ | 0.22 – 0.72 |

**Uzmanın `kisalik_dogallik` puanıyla korelasyon**

| Kol | n | r |
|---|---:|---:|
| v2 · `dogallik` | 44 | -0.20 |
| v3 · `dogallik` | 44 | -0.03 |
| v4 · `dogallik` | 44 | -0.06 |
| v4 · `dogallik_holistik` | 44 | -0.04 |

> ✅ ≥ 0.75 · ⚠️ ≥ 0.60 · ❌ < 0.60 — bizim konvansiyonumuz (Kural 6).

## 2.3 `mi_uyumu`

| Kol | n | Ort. | s | Dağılım |
|---|---:|---:|---:|---|
| v2 · `mi_uyumu` | 68 | 4.12 | 0.83 | `{2: 5, 3: 5, 4: 35, 5: 23}` |
| v3 · `mi_uyumu` | 68 | 4.29 | 0.81 | `{2: 4, 3: 3, 4: 30, 5: 31}` |
| v4 · `mi_uyumu` | 68 | 4.88 | 0.36 | `{3: 1, 4: 6, 5: 61}` |
| v4 · `mi_uyumu_holistik` | 68 | 4.50 | 0.81 | `{1: 1, 2: 2, 3: 2, 4: 20, 5: 43}` |

**Uzmanın `mi_uyumu` dağılımı:** `{3: 1, 4: 1, 5: 16}` (n=18)

> ⚠️ Uzman bu boyutta neredeyse hiç ayrım yapmamış — *uzman ≤ 2 vs = 5* testi anlamsız. Yalnızca `ret` vs `kabul` raporlanıyor.

### mi_uyumu — `ret` vs `kabul` · n = 5 / 32

| Kol | kötü ort. | iyi ort. | uyum oranı | %95 aralık |
|---|---:|---:|---:|:---:|
| v2 · `mi_uyumu` | 4.20 | 3.91 | 0.41 ❌ | 0.15 – 0.67 |
| v3 · `mi_uyumu` | 4.40 | 4.19 | 0.46 ❌ | 0.19 – 0.73 |
| v4 · `mi_uyumu` | 5.00 | 4.81 | 0.41 ❌ | 0.15 – 0.66 |
| v4 · `mi_uyumu_holistik` | 4.80 | 4.34 | 0.35 ❌ | 0.11 – 0.59 |

**Uzmanın `mi_uyumu` puanıyla korelasyon**

| Kol | n | r |
|---|---:|---:|
| v2 · `mi_uyumu` | 18 | -0.20 |
| v3 · `mi_uyumu` | 18 | +0.11 |
| v4 · `mi_uyumu` | 18 | -0.21 |
| v4 · `mi_uyumu_holistik` | 18 | -0.25 |

> ✅ ≥ 0.75 · ⚠️ ≥ 0.60 · ❌ < 0.60 — bizim konvansiyonumuz (Kural 6).

## 3. Bayraklar güvenilir mi — deterministik çapraz kontrol ⭐

İki bayrağın karşılığı kodla da bulunabiliyor. Bu, **uzmandan bağımsız** bir geçerlilik sınaması: judge'ın *evet/hayır* cevapları metinle uyuşuyor mu?

| Bayrak | Deterministik kaynak | Uyum | Judge evet/kod hayır | Judge hayır/kod evet |
|---|---|---:|---:|---:|
| `bos_guvence` | `configs/filters.yaml` yasak ifade listesi | 68/68 (%100) | 0 | 0 |
| `siz_kaymasi` | `siz`/`-sınız` regex'i | 68/68 (%100) | 0 | 0 |

> Kod da kusursuz değil (kelime taraması bağlam görmez, K40'ın dersi) — bu tablo **mutabakat** ölçer, doğruluk değil. Yüksek uyuşmazlık, ikili sorunun sanıldığı kadar nesnel olmadığını gösterir.

## 4. `anlasilirlik` tekrar üretildi mi

v3 ile v4 **aynı hesaplanan puanı** verdi: **34/48**  
v3 ile v4 **aynı cümleyi** seçti: **45/48**

v4'te sorular aynı, ama holistik puan öne alındı ve iki yeni bölüm eklendi. Aynı kayıtta aynı puan çıkması mekanizmanın kararlı olduğunu gösterir; büyük fark çıkması çıpalama/bağlam etkisine işaret eder.

## 5. Alternatif MI formülü — keşifsel

MI'da **tuzaklar ateşlemiyor** (1/68) ama **OARS becerileri ateşliyor** (yansıtma %87 · karmaşık %68 · takdir %15 · özet %7 · özerklik %10). Formülüm puanı tuzaklardan türetiyordu, yani veride **duran sinyali kullanmıyordu**. Aynı ikili cevaplarla, yeni çağrı yapmadan başka bir formül denenebilir:

```
mi_alternatif = 1 + (OARS becerisi sayısı) − (tuzak sayısı),  1-5 arası
```

⚠️ **Post-hoc ve keşifseldir.** Tek bir alternatif önceden belirlendi ve yalnızca o raporlanıyor; n=5'te birkaç formül deneyip en iyisini seçmek aşırı uydurma olurdu. Buradaki sayı **hipotez üretir, doğrulamaz** — doğrulaması yeni bir korpus ve yeni bir uzman turu gerektirir.

| Formül | Dağılım (68 kayıt) | s | ret ort. | kabul ort. | uyum oranı | %95 aralık |
|---|---|---:|---:|---:|---:|:---:|
| mevcut (5 − tuzak) | `{3: 1, 4: 6, 5: 61}` | 0.36 | 5.00 | 4.81 | 0.41 | 0.15 – 0.66 |
| **alternatif (1 + beceri − tuzak)** | `{1: 7, 2: 9, 3: 38, 4: 14}` | 0.86 | 3.00 | 2.66 | **0.42** | 0.16 – 0.68 |

## 6. Sonuç

### `anlasilirlik` — tekrar üretildi, kontrol artık temiz

v3'ün sonucu v4'te tekrarlandı (uyum oranı 0.87 → 0.81; aynı cümle 45/48). Asıl kazanç şu: **K59'da zayıf diye işaretlediğim kontrol artık temiz.** v3'te holistik puan sorulardan sonra isteniyordu ve 0.82 çıkıyordu; v4'te sorulardan **önce** isteniyor ve **0.57**'ye düşüyor — v2'nin 0.53'ü ile aynı yerde.

| Kol | Uyum oranı |
|---|---:|
| v2 — soru yok, puanı LLM verdi | 0.53 |
| v4 holistik — soru **öncesi**, puanı LLM verdi | 0.57 |
| v3 holistik — soru **sonrası**, puanı LLM verdi | 0.82 |
| v3 / v4 hesaplanan — sorulardan kod hesapladı | 0.87 / 0.81 |

**Okuma:** yardımsız bir LLM'den alınan bütünsel puan ölçmüyor (0.53-0.57). Somut ikili sorular sorulduğunda, LLM'in **kendi** puanı bile düzeliyor (0.82). Yani aktif madde **ayrıştırma**; puanı koddan hesaplamak onun üstüne küçük bir katkı ve bir **garanti** koyuyor (kod, gördüğü kusuru saymak zorunda). K59'un yönü doğruydu, v4 onu temiz kontrolle **doğruluyor**.

### `dogallik` — başarısız, hem de daha kötüsü

Bayraklar ateşlemedi (en yüksek %3), puan 66/68 kayıtta 5, s=0.17, uyum oranı **0.48**. Ayrıştırma bu boyutu **iyileştirmedi, bozdu**: v3'ün LLM'den gelen `dogallik`'i 0.67 ile daha iyiydi.

Sebep `reports/analiz/2026-09-14-gosterge-secimi.md`'de, judge'a bakmadan gösterildi: seçtiğim beş göstergenin **hepsi korpusta yok** — üçü zaten `configs/filters.yaml` kapısında eleniyor, kod da 0/70 buluyor. Üstelik uzman `dil_butunlugu` ile `kisalik_dogallik`'i **r = +0.97** ile doldurmuş (43/46 kayıtta birebir aynı puan): bu korpusta doğallık ayrı bir boyut değil. **Var olmayan bir ayrım arandı.**

### `mi_uyumu` — başarısız, ölçüt de yok

Tuzaklar 1/68 ateşledi, puan 61/68 kayıtta 5, uyum oranı 0.41 — dört sürümün dördü de 0.50'nin **altında**. Ama burada bir de **ölçüt sorunu** var: uzman bu maddeyi 50 kaydın 18'inde doldurmuş ve 16'sına 5 vermiş. Yani MI uyumunda karşılaştırılacak bir insan yargısı pratikte **yok**; boyutun başarısız olduğunu bile kesin söyleyemeyiz.

OARS becerileri (D1) ise **ateşliyor** ve formülüm o sinyali kullanmıyordu — ama §5'teki keşifsel yeniden hesap bunu da kapatıyor: beceri sayısına dayalı alternatif formül varyansı 0.36'dan 0.86'ya çıkarıyor, **uyum oranını ise değiştirmiyor (0.41 → 0.42)**. Yani sorun formül değil; bu ikili cevaplar uzmanın kararını basitçe **öngörmüyor**.

### Genel ders

**Ayrıştırma her boyutta işe yaramaz; işe yaraması için üç şart var:**
1. Ayrıştırılan özellik korpusta **değişmeli** (doğallık: değişmiyordu).
2. Gösterge, üretim kapısının **zaten elemediği** bir kusur olmalı (doğallık bayraklarının üçü kapının kopyasıydı).
3. Karşılaştırılacak insan yargısında **varyans olmalı** (MI: uzmanın 18 puanının 16'sı 5).

`anlasilirlik` üçünü de sağlıyordu — bu yüzden çalıştı.

