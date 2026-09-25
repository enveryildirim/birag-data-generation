# Kapsam kararı — h1 ↔ h7, aynı veri, kol başına üç tohum

**Betik:** `scripts/analiz/2026-09-19-kapsam-karari-uc-tohum.py` · **Tarih:** 2026-09-19  
**Veri:** `datasets/v0.0.14/train.jsonl` · **bölme:** `veri.seed 7` (sabit) · **tohumlar:** 7 / 13 / 23  
**Kapsam dışındaki her alan** h1 kolundakiyle birebir — alan alan denetlendi

## 1. ⭐⭐⭐ Altı kol

| kapsam | t7 | t13 | t23 | **ortalama** | sd | yayılım |
|---|---:|---:|---:|---:|---:|---:|
| _**E2 sert kapı** (/20)_ | | | | | | |
| h1 · 8 kat · q · r8 | 10 | 10 | 12 | **10.67** | 1.15 | 2 |
| h7 · 24 kat · q+o · r16 | 12 | 8 | 11 | **10.33** | 2.08 | 4 |
| _**E3 unutma** (/30)_ | | | | | | |
| h1 · 8 kat · q · r8 | 29 | 27 | 28 | **28.00** | 1.00 | 2 |
| h7 · 24 kat · q+o · r16 | 28 | 27 | 27 | **27.33** | 0.58 | 1 |

**E2 sert kapı:** h1 − h7 = **+0.33** · birleşik standart hata **1.37** ⇒ bu tasarımla **ancak 2.7 puandan büyük** bir fark görülebilirdi. ⛔⛔ **Fark eşiğin çok altında — iki kapsam ayırt edilemiyor.**

**E3 unutma:** h1 − h7 = **+0.67** · birleşik standart hata **0.67** ⇒ bu tasarımla **ancak 1.3 puandan büyük** bir fark görülebilirdi. ⛔⛔ **Fark eşiğin çok altında — iki kapsam ayırt edilemiyor.**

## 2. ⭐⭐⭐ Beklenmeyen bulgu — gürültü KAPSAMA BAĞLI

| kapsam | E2 yayılımı | E2 sd |
|---|---:|---:|
| h1 · 8 kat · q · r8 | 2 | 1.15 |
| h7 · 24 kat · q+o · r16 | 4 | 2.08 |

⛔⛔⛔ **Büyük kapsamın oynaklığı küçüğünkinin 1.8 katı** (2 → 4 puan yayılım). ➡️ *T183'te «kapsam bağımsızlığı VARSAYIM, ölçülmedi» diye şerh düşmüştüm — şimdi ölçüldü ve varsayım **yanlış** çıktı. Büyük kollar daha oynak; T183'ün büyük kapsamlı ailelere uyguladığı ±2 bandı bu yüzden **fazla dar**, yani o ailelerde bandın içinde kalan iddia sayısı raporladığımdan **daha fazla**.*

## 3. ⭐ Maliyet — eşit sonuç, eşit olmayan bedel

| kapsam | eğitim süresi (ort.) |
|---|---:|
| h1 · 8 kat · q · r8 | 6.9 dk |
| h7 · 24 kat · q+o · r16 | 9.1 dk |

⭐⭐ **Karar kuralı, ölçüm iddiası değil:** iki seçenek ayırt edilemiyorsa ucuz ve basit olan seçilir. ⇒ **h1 kapsamı korunur** — ama artık *«iki kapıyı da geçen tek kol»* olduğu için değil, **h7'den ayırt edilemediği ve daha ucuz olduğu için**. ➡️ *Aynı karar, başka gerekçe; ve gerekçenin doğru olması kararın doğru olmasından ayrı bir iştir.*

⛔ Üç yapılandırma dosyasının başındaki *«iki Pareto kapısını da geçen tek kol»* cümlesi bu bulguyla **yanlış**tır ve düzeltilmelidir.

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔⛔ **n=3 tohum/kol** | görülebilir eşik ~2.7 puan; daha küçük gerçek farklar bu tasarımla görünmez |
| ⛔⛔ **Sayılar ALT SINIR** | 20 öğenin hepsi `tip: judge` iddiası taşıyor, judge koşulmadı (K216) |
| ⛔ **İki kapsam noktası** | merdivenin tamamı üç tohumla koşulmadı; yalnız uçları |
| ⛔ **`veri.seed` sabit** | bölme oynaklığı hâlâ dahil değil ⇒ gerçek kol-kola bant bundan da geniş |
| ⚠️ **Eşit sonuç «ikisi de iyi» demek değil** | ikisi de sert kapıda tabanın (11/20) altında ya da civarında |
