# `ozerklik_vurgusu` — beyan metinden yeniden ölçüldü

**Betik:** `scripts/analiz/2026-09-20-beyan-metin-uyumu.py` · **Tarih:** 2026-09-20  
**Kapsam:** üretilmiş **118** kayıt (`v6-parti8` blokları)

⭐ v4 §5a: *«beyan, yapılan hamlenin kaydıdır, niyetinin değil»*. Izgara bir TASARIM, `gen_meta` bir KAYIT — beyanı tasarımdan kopyalamak kaydı niyete eşitlemek olurdu.

| | |
|---|---:|
| ızgaranın özerklik dediği satır | 24 |
| ⭐ **metinde ÖLÇÜLEN** | **26** (%22) |
| ⭐ metinde ölçülen **red** | **18** (ızgara: 18) |
| beyanı düzeltilen kayıt | **2** |
| ⛔ ızgara 1 diyor ama metinde yok | 7 |

⛔ **Eksik satırlar: ['4(red)', '32(red)', '67(red)', '82(red)', '85(red)', '99(red)', '105(red)']**

⭐⭐ **Ölçülen oran %22**, §5a'nın hedefi ~%20 *(hedef «bu benim önerim» olarak işaretli, literatürden değil)*. Hedefin üstünde.

## Beyanı düzeltilen kayıtlar

| # | eskiden | **şimdi** |
|---|---|---|
| 105 | False | **True** |
| 116 | False | **True** |

## `is_negative` — okuma kuyruğu (YAZILMADI)

⛔ Desen ile beyan aşağıdaki kayıtlarda ayrılıyor. Bu bir düzeltme listesi DEĞİL: T227'de ölçüldüğü üzere desen iki yönde birden yanlış (ateşlediği 70 kaydın 26'sında fazla, ateşlemediği 7 kontrol kaydının 5,7'sinde az saydı). Tanımın tek evi `src/olcu_red.py`.

| # | beyan | desen |
|---|:-:|:-:|
| 4 | red | — |
| 10 | — | red |
| 32 | red | — |
| 58 | — | red |
| 67 | red | — |
| 74 | — | red |
| 82 | red | — |
| 85 | red | — |
| 99 | red | — |
| 105 | red | — |
| 118 | — | red |

## ⛔ Bu düzeltmenin söylemedikleri

| | |
|---|---|
| ⛔⛔ **`is_negative` ARTIK BU BETİKTE YAZILMIYOR (T227)** | üç anotatörle karara bağlanan 26 ayrışmanın 22'sinde desen fazla saymıştı; alan bir ÖLÇÜM değil BEYAN |
| ⛔⛔ **Desen bir ÖLÇÜT DEĞİL, sonda** | özerklik cümlesi sözlükle aranıyor; bu depoda mekanik kuralın Türkçe serbest metinde tavana vurduğu yedi örnek var ⇒ ölçülen oran bir **alt sınır** |
| ⛔ **Izgara DEĞİŞTİRİLMEDİ** | plan dondurulmuş (Kural 2); değişen yalnız kaydın beyanı, tasarım `izgara_ozerklik`te duruyor |
| ⚠️ **Ters yön eksik sayılmaz** | metinde var ızgarada yok ⇒ §5a özerkliği hedef sayıyor, tavan değil |
