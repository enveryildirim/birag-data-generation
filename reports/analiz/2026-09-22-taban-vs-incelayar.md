# Taban ↔ ince ayarlı model — judge gerektirmeyen metrikler

**Betik:** `scripts/analiz/2026-09-22-taban-vs-incelayar.py` · **Tarih:** 2026-09-22  
**İnce ayarlı kol:** `d1-veri2x-k8qo-v018` (`datasets/v0.0.18`, 1033 kayıt) · **taban:** adaptersiz  

⛔ **Rubrik boyutları YOK:** judge kotası kapalı ve Claude üreticiyle aynı aile (K45) ⇒ buradaki her sayı deterministik bir iddia denetiminden ya da metnin kendisinden geliyor.

⛔⛔ **T248 şartı:** her puanın yanında boş cevap, uzunluk ve kesilme verilir.

## Eksenler

| eksen | taban | ince ayar (ort ± 2·SE) | Δ | okunabilir mi | tohum |
|---|---|---|---:|---|---:|
| `safety_crisis` | 11/20 | 8.75 ± 1.45 | **-2.25** | ⭐ **evet** | 8 |
| `forgetting_smoke` | 28/30 | 26.75 ± 0.73 | **-1.25** | ⭐ **evet** | 8 |
| `context_fidelity` | 14/20 | 14.33 ± 1.76 | **+0.33** | ⛔ hayır — gürültüde | 3 |
| `sycophancy` | 22/24 | 22.00 ± 0.00 | **+0.00** | ⛔ hayır — gürültüde | 3 |
| `context_fidelity.real` | 7/15 | 8.33 ± 0.67 | **+1.33** | ⭐ **evet** | 3 |

## ⛔⛔ T248 yan sütunları — puan bunlar olmadan okunmaz

| eksen | boş cevap (taban → kol) | kesilme | ort. uzunluk (sözcük) |
|---|---|---|---|
| `safety_crisis` | 0 → **3.8** | 0 → 0.4 | 50 → **31** |
| `forgetting_smoke` | 0 → **0.0** | 11 → 9.6 | 38 → **30** |
| `context_fidelity` | 0 → **1.0** | 0 → 0.3 | 17 → **15** |
| `sycophancy` | 2 → **1.0** | 0 → 0.0 | 25 → **24** |
| `context_fidelity.real` | 0 → **0.7** | 0 → 0.0 | 26 → **19** |

## Çeşitlilik ve uzunluk — `golden.dev` (48 öge)

⭐ *«Bu benim önerim»* — çeşitlilik metrikleri diyalog üretimi literatüründe standarttır ve burada **ölçülmüş** bir olguyu hedefliyor: K193 korpusun ikinci büyük kalıbını 43 kayıtta (%7,5) bulmuştu.

| model | distinct-1 | distinct-2 | yinelenen cümle | ort. uzunluk |
|---|---:|---:|---:|---:|
| taban | 0.491 | 0.855 | %0.0 | 23 |
| d1 · t7 | 0.553 | 0.883 | %0.0 | 17 |
| d1 · t13 | 0.447 | 0.733 | %0.0 | 22 |
| d1 · t23 | 0.557 | 0.880 | %2.1 | 19 |

⚠️ distinct-n **uzunluğa duyarlıdır**: kısa cevaplarda kendiliğinden yükselir. ⇒ Uzunluk sütunu olmadan okunamaz — bu, T248'in çeşitlilik metriğindeki karşılığıdır.

## ⛔ Bu raporun söylemedikleri

| | |
|---|---|
| ⛔⛔ **Rubrik boyutları yok** | judge erişimi açılmadan `mi_uyumu`, EPITOME üçlüsü, `anlasilirlik` ölçülemez ⇒ bu rapor *«kalite arttı/azaldı»* demez |
| ⛔⛔ **`safety_crisis` bu kolun etkisini ölçemez** | T247: korpusta `is_crisis` kaydı 0; eksen geçerli ama bu karşılaştırma için **yersiz** |
| ⛔ **Taban tek koşu** | adaptersiz üretim deterministik ⇒ tohum yayılımı yok; hata payı yalnız ince ayar kolu için |
| ⛔ **`otomatik_gecti` kapı sayımıdır, kalite değil** | K57; judge tipindeki iddialar bu koşucuda *«denetlenemedi»* kalır ve **geçti sayılmaz** |
| ⚠️ **Çeşitlilik metrikleri yeni** | bu projede ilk kez hesaplanıyor, gürültü tabanı ölçülmedi |
