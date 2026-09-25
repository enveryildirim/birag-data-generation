# `v6-parti1` judge ↔ korpusun aynı-model dilimi

**Betik:** `scripts/analiz/2026-09-21-judge-parti1-taban.py` · **Tarih:** 2026-09-21  
**Model:** `agy:gemini-3.8-flash-high` · korpus dilimi **32** · parti1 **59**

⛔ K97: `v0.0.14`'ün 521 kaydı `claude-sonnet-subagent` ile puanlı ve buraya KONMADI. Karşılaştırma yalnız aynı modelle yargılanmış dilimle.

| boyut | ölçek | korpus dilimi | **parti1** | fark |
|---|---|---:|---:|---:|
| `duygusal_tepki` | 0-2 | 1.22 | **1.02** | -0.20 |
| `yorumlama` | 0-2 | 1.41 | **1.25** | -0.15 |
| `kesif` | 0-2 | 0.91 | **0.73** | -0.18 |
| `mi_uyumu` | 1-5 | 4.91 | **4.98** | +0.08 |
| `grounding` | 1-5 | 5.00 | **5.00** | +0.00 |

## ⭐⭐ Hipotez — düşük `kesif` bir KUSUR mu, bir TASARIM mı?

`kesif` *«kendini daha fazla açmaya davet ediyor mu»* diye soruyor. Izgara kayıtların yarısına **sorusuz** kapanış dayatıyor. Eğer düşük ortalama oradan geliyorsa, sayı bir kalite kusuru değil bir tasarım tercihinin ölçüdeki karşılığıdır.

| kapanış | n | `kesif` | `duygusal_tepki` | `yorumlama` |
|---|---:|---:|---:|---:|
| `acik_uclu_soru` | 29 | 1.45 | 1.03 | 1.31 |
| `ozet` | 9 | 0.11 | 1.22 | 1.33 |
| `yalnizca_yansitma` | 9 | 0.00 | 0.89 | 1.11 |
| `takdir` | 9 | 0.00 | 1.00 | 1.22 |
| `durur` | 3 | 0.00 | 0.67 | 1.00 |

⭐ Aynı ayrım korpus diliminde (kapanış karışımı benzer, o yüzden kalan fark kapanıştan gelmiyor):

| kapanış | n | `kesif` | `duygusal_tepki` | `yorumlama` |
|---|---:|---:|---:|---:|
| `acik_uclu_soru` | 16 | 1.69 | 1.12 | 1.50 |
| `ozet` | 7 | 0.00 | 1.43 | 1.43 |
| `yalnizca_yansitma` | 5 | 0.20 | 1.20 | 1.00 |
| `takdir` | 3 | 0.00 | 1.33 | 1.67 |
| `durur` | 1 | 1.00 | 1.00 | 1.00 |


⭐ **Sorulu kapanış** (n=29): `kesif` **1.45** · **sorusuz kapanış** (n=30): **0.03** — fark **+1.41** (ölçek 0-2).

⚠️ Korpus diliminde sorulu kapanış oranı **%50**, parti1'de **%49**. İki dilimin kapanış karışımı farklıysa, `kesif` ortalamalarını doğrudan karşılaştırmak **elmayla armut** olur.

## ⛔ Bu karşılaştırmanın söylemedikleri

| | |
|---|---|
| ⛔⛔ **Korpus dilimi küçük** | n=32; bir ortalama farkının gürültü bandı **ölçülmedi** — T175 kayıt düzeyinde %61 oynaklık ölçtü ama KÜME ORTALAMASI için bir taban yok |
| ⛔⛔ **Neden-sonuç kurulmadı** | kapanış türü ile `kesif` arasındaki ilişki bir korelasyondur; ızgara kapanışı dayattığı için ters nedensellik yok, ama başka bir ortak sebep olabilir |
| ⛔ **`kesif` düşüklüğü «iyi» demek değildir** | tasarım tercihi olması onu doğru yapmaz; yalnız bir KUSUR olmadığını gösterir. Sorusuz kapanışın terapötik değeri ayrı bir soru ve ölçülmedi |
| ⛔ **`mi_uyumu` ve `grounding` tavana yakın** | bu, ayırt etme gücü olmadığı anlamına da gelebilir (K57: judge kalite ölçmez, tarar) |
| ⛔⛔ **`kesif` bir KALİTE boyutu gibi raporlanıyor ama bu koşuda bir KAPANIŞ DEDEKTÖRÜ gibi davrandı** | sorulu 1.45 ↔ sorusuz 0.03; aradaki fark ölçeğin %70'i. Bu, rubriğin kusuru mu yoksa `kesif`in tanımı gereği mi böyle olduğu **karara bağlanmadı** |
