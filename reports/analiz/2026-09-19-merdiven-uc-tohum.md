# Kapsam merdiveni — yedi basamak, kol başına üç tohum

**Betik:** `scripts/analiz/2026-09-19-merdiven-uc-tohum.py` · **Tarih:** 2026-09-19  
**Veri:** `datasets/v0.0.14/train.jsonl` · **bölme:** `veri.seed 7` · **tohumlar:** 7, 13, 23  
**Kapsam dışındaki her alan** h1 kolundakiyle birebir — alan alan denetlendi

## 1. ⭐⭐⭐ Yedi basamak

| basamak | kapsam | t7 | t13 | t23 | **ort.** | sd | yayılım |
|---|---|---:|---:|---:|---:|---:|---:|
| **h1** | 8 kat · q · r8 | 10 | 10 | 12 | **10.67** | 1.15 | 2 |
| **h2** | 16 kat · q · r8 | 8 | 5 | 5 | **6.00** | 1.73 | 3 |
| **h3** | 24 kat · q · r8 | 7 | 4 | 7 | **6.00** | 1.73 | 3 |
| **h4** | 32 kat · q · r8 | 7 | 8 | 6 | **7.00** | 1.00 | 2 |
| **h5** | 16 kat · q+o · r8 | 8 | 5 | 9 | **7.33** | 2.08 | 4 |
| **h6** | 24 kat · q+o · r8 | 8 | 6 | 7 | **7.00** | 1.00 | 2 |
| **h7** | 24 kat · q+o · r16 | 12 | 8 | 11 | **10.33** | 2.08 | 4 |

_E3 unutma (/30):_

| basamak | t7 | t13 | t23 | **ort.** | sd |
|---|---:|---:|---:|---:|---:|
| h1 | 29 | 27 | 28 | **28.00** | 1.00 |
| h2 | 28 | 28 | 28 | **28.00** | 0.00 |
| h3 | 27 | 28 | 28 | **27.67** | 0.58 |
| h4 | 28 | 26 | 28 | **27.33** | 1.15 |
| h5 | 26 | 25 | 27 | **26.00** | 1.00 |
| h6 | 27 | 29 | 27 | **27.67** | 1.15 |
| h7 | 28 | 27 | 27 | **27.33** | 0.58 |

## 1b. ⭐⭐⭐ Aynı kollar, T134/T135'in KENDİ ölçütüyle (dereceli)

Kriz öğeleri: **15** · her öğe 0-2 puan ⇒ tavan **30**

| basamak | kapsam | t7 | t13 | t23 | **ort.** | sd |
|---|---|---:|---:|---:|---:|---:|
| **h1** | 8 kat · q · r8 | 18 | 17 | 14 | **16.33** | 2.08 |
| **h2** | 16 kat · q · r8 | 2 | 2 | 2 | **2.00** | 0.00 |
| **h3** | 24 kat · q · r8 | 1 | 0 | 1 | **0.67** | 0.58 |
| **h4** | 32 kat · q · r8 | 1 | 1 | 0 | **0.67** | 0.58 |
| **h5** | 16 kat · q+o · r8 | 1 | 0 | 5 | **2.00** | 2.65 |
| **h6** | 24 kat · q+o · r8 | 3 | 1 | 0 | **1.33** | 1.53 |
| **h7** | 24 kat · q+o · r16 | 10 | 3 | 9 | **7.33** | 3.79 |

⭐ Dereceli ölçütte ayırt edilebilen çift: **12/21** — **h1↔h2** (+14.3>2.4) · **h1↔h3** (+15.7>2.5) · **h1↔h4** (+15.7>2.5) · **h1↔h5** (+14.3>3.9) · **h1↔h6** (+15.0>3.0) · **h1↔h7** (+9.0>5.0) · **h2↔h3** (+1.3>0.7) · **h2↔h4** (+1.3>0.7) · **h2↔h7** (-5.3>4.4) · **h3↔h7** (-6.7>4.4) · **h4↔h7** (-6.7>4.4) · **h6↔h7** (-6.0>4.7)

⚠️ İki ölçüt **aynı tabloda karşılaştırılmaz** (K137); yan yana durmaları *«aynı kollar iki ölçütle nasıl görünüyor»* sorusunu cevaplar, hangisinin doğru olduğunu değil.


## 2. ⭐⭐ Gürültü kapsama bağlı mı — T184 yedi basamakta sınanıyor

| basamak | eğitilen katman | E2 sd |
|---|---:|---:|
| h1 | 8 | 1.15 |
| h2 | 16 | 1.73 |
| h3 | 24 | 1.73 |
| h4 | 32 | 1.00 |
| h5 | 16 | 2.08 |
| h6 | 24 | 1.00 |
| h7 | 24 | 2.08 |

Katman sayısı ↔ sd korelasyonu **r = -0.18** ⛔ (T184'ün 1,8 katlık bulgusu yedi basamakta YİNELENMEDİ; iki noktadan çıkarılan bir eğilimdi)

⚠️ n=7 basamak ve her sd yalnız 3 tohumdan ⇒ bu korelasyon bir eğilim işareti, ölçülmüş bir yasa değil.

## 3. ⭐⭐⭐ Hangi basamaklar birbirinden ayırt edilebiliyor

| çift | ortalamalar | fark | görülebilir eşik | hüküm |
|---|---|---:|---:|---|
| h1 ↔ h2 | 10.67 ↔ 6.00 | **+4.67** | 2.4 | ⭐ **ayırt edilebiliyor** |
| h1 ↔ h3 | 10.67 ↔ 6.00 | **+4.67** | 2.4 | ⭐ **ayırt edilebiliyor** |
| h1 ↔ h4 | 10.67 ↔ 7.00 | **+3.67** | 1.8 | ⭐ **ayırt edilebiliyor** |
| h1 ↔ h5 | 10.67 ↔ 7.33 | **+3.33** | 2.7 | ⭐ **ayırt edilebiliyor** |
| h1 ↔ h6 | 10.67 ↔ 7.00 | **+3.67** | 1.8 | ⭐ **ayırt edilebiliyor** |
| h1 ↔ h7 | 10.67 ↔ 10.33 | **+0.33** | 2.7 | ⛔ ayırt edilemiyor |
| h2 ↔ h3 | 6.00 ↔ 6.00 | **+0.00** | 2.8 | ⛔ ayırt edilemiyor |
| h2 ↔ h4 | 6.00 ↔ 7.00 | **-1.00** | 2.3 | ⛔ ayırt edilemiyor |
| h2 ↔ h5 | 6.00 ↔ 7.33 | **-1.33** | 3.1 | ⛔ ayırt edilemiyor |
| h2 ↔ h6 | 6.00 ↔ 7.00 | **-1.00** | 2.3 | ⛔ ayırt edilemiyor |
| h2 ↔ h7 | 6.00 ↔ 10.33 | **-4.33** | 3.1 | ⭐ **ayırt edilebiliyor** |
| h3 ↔ h4 | 6.00 ↔ 7.00 | **-1.00** | 2.3 | ⛔ ayırt edilemiyor |
| h3 ↔ h5 | 6.00 ↔ 7.33 | **-1.33** | 3.1 | ⛔ ayırt edilemiyor |
| h3 ↔ h6 | 6.00 ↔ 7.00 | **-1.00** | 2.3 | ⛔ ayırt edilemiyor |
| h3 ↔ h7 | 6.00 ↔ 10.33 | **-4.33** | 3.1 | ⭐ **ayırt edilebiliyor** |
| h4 ↔ h5 | 7.00 ↔ 7.33 | **-0.33** | 2.7 | ⛔ ayırt edilemiyor |
| h4 ↔ h6 | 7.00 ↔ 7.00 | **+0.00** | 1.6 | ⛔ ayırt edilemiyor |
| h4 ↔ h7 | 7.00 ↔ 10.33 | **-3.33** | 2.7 | ⭐ **ayırt edilebiliyor** |
| h5 ↔ h6 | 7.33 ↔ 7.00 | **+0.33** | 2.7 | ⛔ ayırt edilemiyor |
| h5 ↔ h7 | 7.33 ↔ 10.33 | **-3.00** | 3.4 | ⛔ ayırt edilemiyor |
| h6 ↔ h7 | 7.00 ↔ 10.33 | **-3.33** | 2.7 | ⭐ **ayırt edilebiliyor** |

⭐⭐ **9/21 çift ayırt edilebiliyor.** **h1↔h2** (+4.67 > 2.4) · **h1↔h3** (+4.67 > 2.4) · **h1↔h4** (+3.67 > 1.8) · **h1↔h5** (+3.33 > 2.7) · **h1↔h6** (+3.67 > 1.8) · **h2↔h7** (-4.33 > 3.1) · **h3↔h7** (-4.33 > 3.1) · **h4↔h7** (-3.33 > 2.7) · **h6↔h7** (-3.33 > 2.7)

## 4. ⭐⭐⭐ Merdiven düz değil — U biçimli

| basamak | kapsam | ort. |
|---|---|---:|
| ⭐ **h1** | 8 kat · q · r8 | **10.67** |
| ⭐ **h7** | 24 kat · q+o · r16 | **10.33** |
| h5 | 16 kat · q+o · r8 | 7.33 |
| h4 | 32 kat · q · r8 | 7.00 |
| h6 | 24 kat · q+o · r8 | 7.00 |
| h2 | 16 kat · q · r8 | 6.00 |
| h3 | 24 kat · q · r8 | 6.00 |
**İki ölçütün sıralaması yan yana:**

| sıra | otomatik geçen | dereceli yönlendirme |
|---:|---|---|
| 1 | h1 (10.67) | h1 (16.33) |
| 2 | h7 (10.33) | h7 (7.33) |
| 3 | h5 (7.33) | h2 (2.00) |
| 4 | h4 (7.00) | h5 (2.00) |
| 5 | h6 (7.00) | h6 (1.33) |
| 6 | h2 (6.00) | h3 (0.67) |
| 7 | h3 (6.00) | h4 (0.67) |

⛔⛔⛔ **VE «U» OTOMATİK SAYININ ÖZELLİĞİ, DAVRANIŞIN DEĞİL.** Dereceli ölçütte h1 ile h7 **ayırt edilebiliyor**: 16.33 ↔ 7.33, fark **+9.00** > eşik 5.0. Otomatik sayı ikisini aynı kefeye koyuyordu (10,67 ↔ 10,33). ➡️⭐⭐⭐ *İki kolu aynı gören bir ölçüt onların eşit olduğunu söylemez; kendi çözünürlüğünü söyler. «U» keskin ölçütte kayboluyor ve yerine h1'in açık ara önde olduğu bir sıralama geliyor.*

⛔⛔ **T184 DÜZELTİLİR:** orada *«iki kapsam ayırt edilemiyor ⇒ h1'i ucuzluk gerekçesiyle seç»* demiştim. Bu, otomatik sayıya dayanıyordu. Keskin ölçütte h1 **hak ederek** önde. ⭐ Karar değişmiyor, gerekçesi yine değişiyor — ikinci kez. ➡️ *Bir kararın doğru çıkması, ona götüren muhakemenin doğru olduğunu göstermez; bu oturumda aynı karar üç farklı gerekçeyle savunuldu ve ilk ikisi çürüdü.*


⛔⛔⛔ **Ayırt edilebilen 9 çiftin DOKUZUNUN da bir ucunda h1 ya da h7 var.** İkisi arasında fark yok; geri kalan beş basamak kendi aralarında da ayrışmıyor. ➡️⭐⭐⭐ *Yani ölçüt iki kümeyi görüyor — h1/h7 ve ötekiler — ve bu kümeler kapsam eksenine göre SIRALI DEĞİL: en küçük kapsam (h1: 8 kat, q, r8) ile en büyüğü (h7: 24 kat, q+o, r16) aynı tarafta, aradaki her şey öbür tarafta. Merdiven bir uçurum değil bir **U**; ve bir U, basamakları «az → çok» diye sıralayan bir merdiven tasarımıyla hiç görünmezdi.*

⛔⛔ **VE BU U'NUN OKUNMASINI ENGELLEYEN BİR KARIŞTIRICI VAR.** `h6 → h7` arasındaki tek YAPILANDIRMA farkı `rank` (8 → 16). Ama `mlx_lm/tuner/lora.py` güncellemeyi `self.scale * z` diye uyguluyor ve **`scale` rank'e BÖLÜNMÜYOR** (`scale: 20.0` bütün kollarda sabit) ⇒ rank'i ikiye katlamak etkin güncelleme büyüklüğünü de büyütüyor. *Yani h7'yi yukarı çeken şeyin «daha çok kapasite» mi yoksa «daha büyük etkin adım» mı olduğu bu tasarımla AYRILAMIYOR.* ⭐ Ayıracak deney bir satırlık: `rank: 16` + `scale: 10.0` (alfa/rank oranını h6'daki gibi sabitler) — koşulmadı.

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔⛔⛔ **`rank` ↔ `scale` karıştırıcısı** | yukarıda; h7'nin yüksekliğinin sebebi ayrılmadı |
| ⛔⛔ **n=3 tohum/basamak** | görülebilir eşikler 1-3 puan arası; daha küçük gerçek farklar bu tasarımla görünmez ⇒ *«ayırt edilemedi»* ≠ *«eşit»* |
| ⛔⛔ **Sayılar ALT SINIR** | 20 öğenin hepsi `tip: judge` iddiası taşıyor, judge koşulmadı (K216) |
| ⛔ **`veri.seed` sabit** | bölme oynaklığı dahil değil ⇒ gerçek bant daha geniş |
| ⭐ **Dereceli ölçüt §1b'de EKLENDİ** | T185'in bu şerhi kapatıldı; iki ölçüt yan yana ama aynı tabloda karşılaştırılmadan (K137) |
| ⚠️ **Tek veri sürümü** | `v0.0.14`; başka veride merdiven başka olabilir |
