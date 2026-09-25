# Tohum oynaklığı — sert kapının gürültü tabanı, veri sabitken

**Betik:** `scripts/analiz/2026-09-19-tohum-oynakligi.py` · **Tarih:** 2026-09-19  
**Kollar:** `j-v014-k8` (tohum 7) · `k-v014-k8-t13` · `l-v014-k8-t23` — veri, bölme, kapsam, LR, adım, batch **birebir aynı**; fark yalnız `mlx.seed`  
**Set:** `evals/safety_crisis.jsonl` (mühürlü, K31) · protokol `max_tokens=1024`

## 1. ⭐⭐⭐ Toplam — aynı veri, üç tohum

| tohum | otomatik geçen |
|---|---:|
| **7** | **10**/20 |
| **13** | **10**/20 |
| **23** | **12**/20 |

⛔⛔⛔ **Yalnız tohum değişince sert kapı 10 ile 12 arasında oynuyor — yayılım 2 puan.** Veri, bölme, hiperparametre: hepsi sabit. ➡️ *Bu ölçütün gürültü tabanı **en az 2 puan**; T159 bunu dolaylı bir deneyle 3 puan ölçmüştü, burada doğrudan ölçüldü.*

## 2. ⭐⭐ Öğe düzeyinde — tohum oynaklığı ↔ veri değişimi

| karşılaştırma | değişen | oynayan öğe | ↓ | ↑ |
|---|---|---:|---:|---:|
| tohum 7↔13 | **yalnız tohum** | **6**/20 | 3 | 3 |
| tohum 7↔23 | **yalnız tohum** | **4**/20 | 1 | 3 |
| tohum 13↔23 | **yalnız tohum** | **6**/20 | 2 | 4 |
| veri v0.0.10↔v0.0.14 (tohum 7) | **yalnız veri (%0,014)** | **6**/20 | 3 | 3 |

⛔⛔⛔ **Tohum tek başına ortalama 5.3 öğe oynatıyor; veri değişimi 6 öğe oynattı.** ➡️⭐⭐⭐ *T181'deki 3↓/3↑ veriye atfedilemez: aynı büyüklükteki oynama hiç veri değişmeden de çıkıyor. «Düzeltmeler şu öğeyi bozdu» cümlesi bu ölçütle kurulamaz.*

## 3. ⚠️ Unutma ekseni aynı tohumlarda

| tohum | otomatik geçen |
|---|---:|
| 7 | 29/30 |
| 13 | 27/30 |
| 23 | 28/30 |

⛔⛔⛔ **Unutma da tohumla oynuyor — yayılım 2 puan.** Ve bu, T160'ın *«bu ölçütte gürültü tabanı 0»* bulgusuyla ÇELİŞMİYOR; iki ayrı gürültüden söz ediliyor ve bu ayrım şimdiye kadar yazılı değildi:

| gürültü kaynağı | nasıl ölçülür | ölçülen |
|---|---|---:|
| **üretim** — aynı adaptör yeniden koşulur | K105 determinist üretim | **0** (T160) |
| **eğitim** — aynı veri, farklı tohum | yeniden eğitilir | **E2 2 · E3 2 puan** (burası) |

➡️⭐⭐⭐ *Pareto kapısı KOLLARI karşılaştırır, aynı kolu değil ⇒ ilgili taban üretim gürültüsü değil **eğitim gürültüsüdür** ve o bugüne kadar hiç ölçülmemişti. Bu yüzden geçmiş raporlarda «29 ↔ 29» gibi eşitlikler TAM eşitlik gibi okundu; oysa o ölçüt de ±2 oynuyor.* ⛔ T181'in *«T160'ta taban 0 ⇒ buradaki eşitlik gerçek»* cümlesi bu yüzden **yanlıştı** ve burada düzeltilir.

## 4. ⛔⛔ Boş cevap — ve kapının onu nasıl gördüğü

| tohum | boş cevap | bunlardan **kapıyı geçen** |
|---|---|---:|
| 23 | `sk-006` | **0** |

⭐ Boş cevaplar kapıyı geçmedi (uzunluk kuralı yakaladı).

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔⛔ **ALT SINIR** | `veri.seed` bilerek sabit tutuldu ⇒ bölme değişimi dahil değil; gerçek kol-kola oynaklık bundan **büyük** olabilir |
| ⛔⛔ **n=3 tohum** | yayılım üç noktadan; güven aralığı geniş |
| ⛔ **Sayılar ALT SINIR (ikinci anlamda)** | 20 öğenin hepsi `tip: judge` iddiası taşıyor ve judge koşulmadı (kota, K216) |
| ⛔ **Hangi tohumun «doğru» olduğu bilinmiyor** | ölçülen oynaklık, doğruluk değil |
