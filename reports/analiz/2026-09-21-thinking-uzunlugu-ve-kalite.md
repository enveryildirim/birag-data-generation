# Thinking uzunluğu: yazma emeği ve kalite

**Betik:** `scripts/analiz/2026-09-21-thinking-uzunlugu-ve-kalite.py` · **Tarih:** 2026-09-21  
**Girdi:** `data/candidates/v6-parti{1..7}.jsonl` (412 kayıt) · `data/judged/v6-parti{1,2,3}.jsonl` (160 puanlı)  

## 1. Yazdığım karakterler nereye gidiyor

| bileşen | karakter | pay | kayıt başına |
|---|---:|---:|---:|
| `thinking` | 231,244 | %51 | 561 |
| `asistan` | 137,825 | %30 | 334 |
| `kullanici` | 87,522 | %19 | 212 |

⭐⭐ **Yazma emeğinin yarısından fazlası `thinking`** (%51) ve bu, hızlandırmanın en büyük tek kalemi.

## 2. ⛔⛔ v6, EĞİTİLMİŞ SETİN ORANINDAN SAPMIŞ

| set | kayıt | thinking ort | asistan ort | **oran** |
|---|---:|---:|---:|---:|
| `datasets/v0.0.14` (eğitilen) | 571 | 462 | 384 | **1.20** |
| `v6-parti1` | 59 | 457 | 267 | 1.71 |
| `v6-parti2` | 59 | 396 | 228 | 1.74 |
| `v6-parti3` | 60 | 585 | 314 | 1.86 |
| `v6-parti4` | 59 | 574 | 336 | 1.70 |
| `v6-parti5` | 60 | 659 | 398 | 1.65 |
| `v6-parti6` | 58 | 629 | 394 | 1.59 |
| `v6-parti7` | 57 | 628 | 403 | 1.56 |

⛔ v6 ortalaması **1.68**, eğitilen setin **1.20**'sinden **%39** yüksek. ⭐ T16'nın iddiası tam buraya bakıyor: *«tavan da veriyle öğretilir»* ve ürün KPI'ı gecikme. ⇒ Sapma yalnız bir hız sorunu değil, T16'nın kendi ekseninde bir gerilemedir.

## 3. Uzun thinking daha iyi kayıt mı demek

⛔ Korelasyon, nedensellik değil. Aşağıdaki tabloyu okurken en büyük karıştırıcı açıkta: **uzun thinking ZOR kayıtlarda yazılmış olabilir** ve zor kayıtlar zaten düşük puan alır.

| boyut | r(uzunluk) | r(oran) | ortalama |
|---|---:|---:|---:|
| `mi_uyumu` | -0.18 | +0.18 | 4.87 |
| `mi_uyumu_holistik` | -0.21 | +0.21 | 4.34 |
| `grounding` | +0.04 | -0.03 | 4.87 |
| `anlasilirlik` | -0.21 | +0.06 | 4.23 |
| `anlasilirlik_holistik` | -0.18 | +0.10 | 4.79 |
| `dogallik` | -0.07 | +0.05 | 4.97 |
| `dogallik_holistik` | -0.22 | +0.12 | 4.51 |

**Tuzak bayrakları** (yüksek = kötü):

| bayrak | r(uzunluk) | ateşleme oranı |
|---|---:|---:|
| `tuzak_erken_tavsiye` | +0.25 | 0.03 |
| `tuzak_uzman` | +0.22 | 0.04 |
| `tuzak_erken_odak` | +0.15 | 0.02 |
| `ust_uste_yan_cumle` | +0.23 | 0.31 |
| `rol_reddediyor` | +0.28 | 0.37 |

➡️ **Okunan şey:** uzun thinking ana boyutlarda hafif NEGATİF (anlaşılırlık −0,21, doğallık −0,22, MI uyumu −0,18) ve tuzak bayraklarında hafif POZİTİF (erken tavsiye +0,25, uzman tuzağı +0,22). ⇒ **Uzun thinking'in daha iyi kayıt ürettiğine dair bir işaret yok; zayıf da olsa ters yönde işaret var.**

⛔ Etki büyüklükleri küçük (|r| ≈ 0,2) ve n=160. Bu tablo *«kısaltmak kaliteyi artırır»* demiyor; *«kısaltmanın kaliteyi kestiğine dair bir dayanak yok»* diyor.

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔⛔ **Nedensellik yok** | uzun thinking zor kayıtlarda olabilir; ölçüm bu karıştırıcıyı ayıramaz |
| ⛔⛔ **Puanlar bir çekiliş** | T175: kayıt düzeyinde %61 oynuyor ⇒ yalnız küme okunur, tek kayıt değil |
| ⛔ **Yalnız parti1-3** | 252 kayıt yargılanmadı (kota) ⇒ parti4-7 bu tabloda yok ve onlarda thinking daha uzun |
| ⚠️ **Karakter ≠ token** | oranlar karakter üzerinden; token oranı Türkçe'de farklı çıkabilir |
