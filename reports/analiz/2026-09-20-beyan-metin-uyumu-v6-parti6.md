# `ozerklik_vurgusu` — beyan metinden yeniden ölçüldü

**Betik:** `scripts/analiz/2026-09-20-beyan-metin-uyumu.py` · **Tarih:** 2026-09-20  
**Kapsam:** üretilmiş **58** kayıt (`v6-parti6` blokları)

⭐ v4 §5a: *«beyan, yapılan hamlenin kaydıdır, niyetinin değil»*. Izgara bir TASARIM, `gen_meta` bir KAYIT — beyanı tasarımdan kopyalamak kaydı niyete eşitlemek olurdu.

| | |
|---|---:|
| ızgaranın özerklik dediği satır | 12 |
| ⭐ **metinde ÖLÇÜLEN** | **18** (%31) |
| ⭐ metinde ölçülen **red** | **9** (ızgara: 9) |
| beyanı düzeltilen kayıt | **12** |
| ⛔ ızgara 1 diyor ama metinde yok | 1 |

⛔ **Eksik satırlar: ['54(red)']**

⭐⭐ **Ölçülen oran %31**, §5a'nın hedefi ~%20 *(hedef «bu benim önerim» olarak işaretli, literatürden değil)*. Hedefin üstünde.

## Beyanı düzeltilen kayıtlar

| # | eskiden | **şimdi** |
|---|---|---|
| 5 | True | **False** |
| 7 | True | **False** |
| 10 | True | **False** |
| 14 | True | **False** |
| 16 | False | **True** |
| 20 | False | **True** |
| 37 | True | **False** |
| 42 | True | **False** |
| 45 | False | **True** |
| 53 | True | **False** |
| 57 | True | **False** |
| 58 | True | **False** |

## `is_negative` — okuma kuyruğu (YAZILMADI)

⛔ Desen ile beyan aşağıdaki kayıtlarda ayrılıyor. Bu bir düzeltme listesi DEĞİL: T227'de ölçüldüğü üzere desen iki yönde birden yanlış (ateşlediği 70 kaydın 26'sında fazla, ateşlemediği 7 kontrol kaydının 5,7'sinde az saydı). Tanımın tek evi `src/olcu_red.py`.

| # | beyan | desen |
|---|:-:|:-:|
| 54 | red | — |

## ⛔ Bu düzeltmenin söylemedikleri

| | |
|---|---|
| ⛔⛔ **`is_negative` ARTIK BU BETİKTE YAZILMIYOR (T227)** | üç anotatörle karara bağlanan 26 ayrışmanın 22'sinde desen fazla saymıştı; alan bir ÖLÇÜM değil BEYAN |
| ⛔⛔ **Desen bir ÖLÇÜT DEĞİL, sonda** | özerklik cümlesi sözlükle aranıyor; bu depoda mekanik kuralın Türkçe serbest metinde tavana vurduğu yedi örnek var ⇒ ölçülen oran bir **alt sınır** |
| ⛔ **Izgara DEĞİŞTİRİLMEDİ** | plan dondurulmuş (Kural 2); değişen yalnız kaydın beyanı, tasarım `izgara_ozerklik`te duruyor |
| ⚠️ **Ters yön eksik sayılmaz** | metinde var ızgarada yok ⇒ §5a özerkliği hedef sayıyor, tavan değil |
