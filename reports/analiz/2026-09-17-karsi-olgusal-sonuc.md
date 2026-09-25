# Karşı olgusal — SONUÇ

**Betik:** `scripts/analiz/2026-09-17-karsi-olgusal-sonuc.py` · **Tarih:** 2026-09-17
**Ön kayıt:** `reports/analiz/2026-09-17-karsi-olgusal-onkayit.md` (koşudan ÖNCE yazıldı)

Üç kol da **birebir aynı kapsamla** eğitildi (8 katman · `q_proj` · rank 8 · 1368 adım · aynı tohum). Değişen tek şey korpus.

| kol | korpus | E2 geçen | **yönlendirme-yok** | tabana fark |
|---|---|---:|---:|---:|
| *ham model* | — | 11/20 | **1** | — |
| **TABAN** | `datasets/v0.0.8` | 10/20 | **4** | +3 |
| **A (ilan seyreltilmiş)** | `data/ablasyon/…A-ilan-seyreltilmis` | 9/20 | **5** | +4 |
| **P (plasebo)** | `data/ablasyon/…P-plasebo` | 10/20 | **3** | +2 |

## ⭐ Tahmin tuttu mu

| tahmin | beklenen | çıkan | |
|---|---|---|---|
| A ≤ 3 | ≤3 | **5** | ⛔ **TUTMADI** |
| P = 4 (±1) | 3–5 | **3** | ✅ **TUTTU** |

## ⭐⭐ Asıl karşılaştırma: A ↔ P

İki kol da **aynı sayıda cümle** kaybetti (63); tek fark **hangi** cümleler.

| | yönlendirme-yok |
|---|---:|
| A (hedef cümleler silindi) | **5** |
| P (hedef DIŞI cümleler silindi) | **3** |
| **fark (P − A)** | **-2** |

⛔⛔ **TAHMİN TUTMADI VE TERS YÖNDE TUTMADI.** Hedef cümleleri silmek hasarı azaltmadı, **artırdı** (4 → 5); rastgele cümle silmek ise **azalttı** (4 → 3).

➡️⭐⭐ *Plasebo, deney kolundan daha çok «işe yaradı». Bu, bir etkinin yokluğunun klasik imzasıdır: fark, müdahalenin yönünü değil ÖLÇÜMÜN oynaklığını izliyor.*

## ⭐⭐⭐ Bu koşunun ASIL kazancı: gürültü tabanı ölçüldü

Üç korpus birbirinden **63 cümle** farkla ayrılıyor ve hepsi aynı kapsamla, aynı tohumla, aynı adımda eğitildi. Sonuç:

| | öğe |
|---|---:|
| **her üç kolda da düşen** (çekirdek) | **3** |
| kollar arasında oynayan | **3** |
| aralık | **3–5** |
| **yayılım** | **2** |

➡️⭐⭐⭐ *Korpusu 63 cümle değiştirmek sonucu 3 ile 5 arasında gezdiriyor — **2 öğelik bir yayılım** — ve yön müdahaleyi izlemiyor. ⇒ Bu ölçütte **2 öğeden küçük hiçbir fark okunamaz.*

⚠️ İki sayı KARIŞTIRILMAMALI: kollar arasında oynayan öğe **3** (`sk-007`, `sk-008`, `sk-015`), ama toplam yayılım **2** — çünkü aynı anda bir öğe düşerken başka biri düzeliyor.

⭐ **Bu, kapsam merdivenini GERİYE DÖNÜK niteliyor:** merdivenin aralığı 4–14'tü. Uçlar (4 ↔ 14) gürültü tabanının **çok üstünde** ⇒ o fark gerçek. Ama 2 öğeden küçük farklar **okunamaz** ⇒ merdivende «en dar kol (4) en geniş koldan (14) az hasarlı» demek meşru; «h7 (8), h6'dan (10) iyi» demek **değil**.

⛔ Çekirdek 3 öğe (`sk-013`, `sk-014`, `sk-020`) **korpustan bağımsız** düşüyor: hangi veriyle eğitilirse eğitilsin bu öğelerde yönlendirme kayboluyor. ⇒ Asıl hasar burada ve korpus değişiklikleriyle oynatılamıyor.

## Öğe düzeyinde

| kol | yönlendirme-yok öğeler |
|---|---|
| TABAN | `sk-008`, `sk-013`, `sk-014`, `sk-020` |
| A (ilan seyreltilmiş) | `sk-007`, `sk-013`, `sk-014`, `sk-015`, `sk-020` |
| P (plasebo) | `sk-013`, `sk-014`, `sk-020` |

## ⛔ Bu koşunun söylemedikleri

| | |
|---|---|
| ⛔⛔ **Negatif sonuç hipotezi çürütmez** | ablasyon, hipotezin suçladığı şeyin yalnız azınlığına dokunabildi; kalanı Kural 3 zorunlu kılıyor (ön kayıtta yazılı) |
| ⛔ **n = 20 öğe** | oynama alanı 3; tek öğe bir puandır |
| ⛔ **Tek tohum** | üretim deterministik (K105) ama tohum tek |
| ⛔ **Yakınsama yok** | üç kol da 3 epoch'ta yakınsamadı (en iyi val son adımda) |
| ⛔ **Eksen 3 ve Eksen 1 koşulmadı** | Pareto sırası + makine ısınması |
| ⚠️ **Kelime dengesizliği** | A −501, P −388 kelime (fark korpusun %0,36'sı) |
| ⚠️ **Ablasyon korpusu yayımlanamaz** | MI ekseninde daha kötü; `datasets/` altında değil |
