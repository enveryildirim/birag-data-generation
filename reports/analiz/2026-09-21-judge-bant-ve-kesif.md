# Judge — `kesif`in yapısı ve ortalama farkının örnekleme bandı

**Betik:** `scripts/analiz/2026-09-21-judge-bant-ve-kesif.py` · **Tarih:** 2026-09-21  
**Servis çağrısı:** 0 (yalnız kayıtlı puanlar okundu)

## 1. ⭐⭐ `kesif` bir kapanış dedektörü mü — iki judge'da ayrı ayrı

⛔ **K97 ihlali değil:** iki modelin puan DÜZEYLERİ aynı tabloya konmuyor. Sorulan şey her modelin **kendi içindeki** kapanış etkisi.

| judge | n | sorulu kapanış | sorusuz kapanış | fark |
|---|---:|---:|---:|---:|
| Gemini (korpus dilimi) | 16+16 | **1.69** | **0.12** | +1.56 |
| Gemini (parti1) | 29+30 | **1.45** | **0.03** | +1.41 |
| Claude (korpus) | 262+259 | **1.73** | **0.17** | +1.55 |

⭐⭐ Etki **her iki judge'da da** var ve ölçeğin (0-2) büyük kısmını kaplıyor ⇒ bu bir model tuhaflığı değil, **rubriğin `kesif` tanımının sonucu**: *«kendini daha fazla açmaya davet ediyor mu»* sorusu, sorusuz biten bir turda tanımı gereği hayırdır.

➡️⭐⭐⭐ *Izgara kayıtların yarısına sorusuz kapanış dayatıyor; o yarı için `kesif` bir ÖLÇÜM değil, bir SABİT. Küme ortalamasını raporlamak, tasarım tercihini kalite puanı gibi göstermek olur.*

## 2. ⭐ Ortalama farkının örnekleme bandı (önyükleme, B=10.000)

⛔ Bu bant yalnız **örnekleme** belirsizliğini kapsar. Judge'ın yeniden çekiliş oynaklığı (T175: kayıt düzeyinde %61) **ayrıca** vardır ve servis gerektirdiği için ölçülmedi. ➡️ *Toplam belirsizlik en az bu kadardır; bu bir ALT SINIRDIR.*

| boyut | korpus dilimi | parti1 | fark | %95 bant | bandın dışında mı |
|---|---:|---:|---:|---|---|
| `duygusal_tepki` | 1.22 | 1.02 | -0.20 | [-0.47, +0.07] | ⛔ **hayır** |
| `yorumlama` | 1.41 | 1.25 | -0.15 | [-0.40, +0.11] | ⛔ **hayır** |
| `kesif` | 0.91 | 0.73 | -0.18 | [-0.55, +0.19] | ⛔ **hayır** |

⭐ `duygusal_tepki` kapanış karışımından arındırılmış hâliyle (yalnız sorulu kapanışlar, iki tarafta da en kalabalık kova):

| | n | ortalama |
|---|---:|---:|
| korpus dilimi | 16 | 1.12 |
| parti1 | 29 | 1.03 |

fark **-0.09**, %95 bant **[-0.48, +0.31]** ⇒ ⛔ **bandın içinde — bu farkı gösteremem**

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔⛔ **Judge oynaklığı KAPSANMADI** | T175 kayıt düzeyinde %61 oynaklık ölçtü; küme ortalaması için yeniden çekiliş gerekir ve kota kapalı. Gerçek bant buradan GENİŞ |
| ⛔⛔ **Önyükleme bir kanıt üretmez, belirsizliği ölçer** | bandın dışında olmak farkın gerçek olduğunu değil, ÖRNEKLEMEYLE açıklanamadığını söyler |
| ⛔ **Korpus dilimi n=32** | küçük bir grup geniş bant üretir; bandın genişliği bir bulgu değil, örneklem büyüklüğünün sonucu |
| ⛔ **`kesif` bulgusu rubriği KUSURLU ilan etmez** | tanım gereği böyle davranıyor olabilir; karar `gd`-kalemi değil, **rubrik sahibinin** işi ve verilmedi |
