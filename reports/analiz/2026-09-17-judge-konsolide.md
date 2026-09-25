# Judge döngüsü — konsolide rapor (v5-parti3..8)

**Betik:** `scripts/analiz/2026-09-17-judge-konsolide.py` · **Tarih:** 2026-09-17
**Rubrik:** `judge-eksen1.v9` · k=1 · 360 kayıt

⛔⛔ **«Sonra» sütunu korpusun yeniden yargılanmış hâli DEĞİL.** Yalnız metni
değişen kayıtlar yeniden puanlandı; kalanı, puanlanan metnin BİREBİR aynı
olduğu kanıtlanarak eski puanını devraldı. ⇒ Her fark revize edilen
kayıtlardan gelir.

⚠️ Hakem Claude ailesinden (K43/K45) ⇒ **metrik değil**, revizyon sinyali.

## 1. Kusur KATMANLARI — önce → sonra

⚠️ Katman ataması dışlayıcıdır (bir kayıt en üst katmanında sayılır).
⛔ Bu yüzden K3 sütunu **yanıltır**: K1/K2'si düzelen kayıt K3'e *terfi eder*.
Gerçek K3 hareketi için **Bölüm 2**'ye bakılmalı.

| parti | K1 önce→sonra | K2 önce→sonra | K3 önce→sonra | revize kayıt |
|---|---|---|---|---:|
| `v5-parti3` | 2 → **2** · | 5 → **4** ✅ | 0 → **1** ⛔ | 4 |
| `v5-parti4` | 0 → **0** · | 11 → **0** ✅ | 6 → **9** ⛔ | 4 |
| `v5-parti5` | 4 → **0** ✅ | 5 → **0** ✅ | 6 → **7** ⛔ | 8 |
| `v5-parti6` | 3 → **0** ✅ | 7 → **0** ✅ | 8 → **10** ⛔ | 9 |
| `v5-parti7` | 2 → **1** ✅ | 7 → **0** ✅ | 4 → **6** ⛔ | 8 |
| `v5-parti8` | 1 → **0** ✅ | 9 → **0** ✅ | 12 → **17** ⛔ | 12 |
| **toplam** | 12 → **3** | 44 → **4** | 36 → **50** | **45** |

## 2. ⭐ KATMANDAN BAĞIMSIZ bayrak sayısı

| katman | önce | sonra |
|---|---:|---:|
| **K1** | 13 | **3** ✅ |
| **K2** | 48 | **5** ✅ |
| **K3** | 86 | **84** ✅ |

➡️ *K3 katmanlı sayımda 36 → 50 görünüyordu; bağımsız sayımda 86 → 84. Fark tamamen katman terfisinden geliyor ve bunu ancak iki sayıyı yan yana koymak gösteriyor.*

⭐ **K1** = `build.py` eler (klinik güvenlik / rol sınırı) · **K2** = dayanaksız iddia · **K3** = MI tuzağı (elenmez, sete girer)

## 2. ⛔ Bu raporun söylemedikleri

| | |
|---|---|
| ⛔ **Müdahale ölçümü değil** | revizyon kararı da, ölçüm de aynı hakemin bulgularından geliyor; bağımsız bir sınama yok |
| ⛔ **K3 kasten düzeltilmedi** | 48 MI tuzağı sette duruyor: ilk eğitim ölçülmeden hepsini düzeltmek, hangi revizyonun işe yaradığını ölçülemez yapardı |
| ⛔ **Uzman yok** | judge'ın yanlış pozitif oranı hâlâ ölçülmedi (K58 50/70'te kapandı) |
| ⚠️ k=1 | hakemin kendi içi tutarlılığı ölçülmedi |
| ⚠️ Devralınan puanlar | değişmeyen kayıtların puanı ilk koşudan; hakem aynı metni bugün farklı puanlayabilirdi |
