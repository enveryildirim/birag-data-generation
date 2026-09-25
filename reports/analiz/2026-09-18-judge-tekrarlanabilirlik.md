# ⛔⛔⛔ Judge'ın kendi tekrarlanabilirliği — %50

**Betik:** `scripts/analiz/2026-09-18-judge-tekrarlanabilirlik.py` · **Tarih:** 2026-09-18

⛔ **Nasıl ortaya çıktı.** 32 bayat yargı yeniden koşuldu ve **23'ünün puanı
değişti**. Ama o kayıtlardaki metin değişikliği birer SÖZCÜKTÜ ⇒ *«bir»* eklemek
`duygusal_tepki`'yi 1'den 0'a indiremez.

## 1. ⭐ Ayrım: metni DEĞİŞMEMİŞ kayıtlar

Metni hiç değişmemiş, v9 ile yargılanmış **12** kayıt aynı judge'a
yeniden soruldu ⇒ **6'sı (%50) farklı puan aldı.**

| kayıt | değişim |
|---|---|
| `65270a0059` | duygusal_tepki 2→1 · yorumlama 2→1 |
| `50f5ebb517` | yorumlama 2→1 |
| `3a992f1291` | yorumlama 2→1 · kesif 2→1 |
| `d4fb7f82a9` | yorumlama 2→1 |
| `ab063ce6da` | duygusal_tepki 1→2 |
| `59bfb2dfcc` | yorumlama 2→1 |

➡️⭐⭐⭐ *Bu ölçüm, projedeki HER kayıt düzeyi judge sayısını yeniden okutur:
aynı metne aynı judge iki kez sorulduğunda yarısında başka puan geliyor. Bir
kaydın puanı bir ÖLÇÜM değil, bir ÇEKİLİŞtir; kayıt düzeyinde karşılaştırma
yapılamaz.*

## 2. ⛔⛔ Gürültü simetrik DEĞİL — iki boyutta sistematik düşüş

32 yeniden yargılanan kayıtta alan düzeyinde **25 düşüş**, **13 yükseliş** (düşme oranı %65).

| boyut | düştü | yükseldi | okuma |
|---|---:|---:|---|
| `cevapsiz_soru` | 1 | 0 | · simetrik gürültü |
| `duygusal_tepki` | 5 | 8 | · simetrik gürültü |
| `kesif` | 7 | 1 | ⛔ **sistematik düşüş** |
| `mi_uyumu` | 1 | 2 | · simetrik gürültü |
| `yorumlama` | 11 | 2 | ⛔ **sistematik düşüş** |

⚠️ **Ayırt edilemedi:** eski yargılar 2026-09-17'de, yenileri 09-18'de alındı ⇒
düşüş judge'ın kendisindeki (Gemini tarafındaki) bir kaymadan da gelebilir. İki
açıklama (gürültü ↔ kayma) bu veriyle ayrılamıyor.

## 3. ⭐ Ne DEĞİŞMEDİ

| | |
|---|---:|
| yeniden yargılanan | 32/32 |
| başarısız | 0 |
| ⭐ **güvenlik bayrağı değişen** | **0** |
| elenen kayıt kümesi | **aynı** (6 kayıt) |

⭐ Yani metodolojik bulgu ağır ama **veri değişmedi**: `build.py`'nin eleme
kararları `klinik_guvenlik_ihlali`ye bakıyor ve o bayrak **hiçbir kayıtta**
oynamadı.

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔⛔ **Hangi puanın «doğru» olduğu bilinmiyor** | ölçülen şey TUTARLILIK, doğruluk değil; iki çekiliş de yanlış olabilir |
| ⛔⛔ **Gürültü ↔ kayma ayrılamadı** | aynı gün içinde tekrar ölçülmedi; ayırmak için aynı metne aynı gün iki kez sormak gerekir |
| ⛔ **n=12 küçük** | %50 geniş bir güven aralığı taşır |
| ⛔ **Yalnız kayıt düzeyi** | ORTALAMALAR bu gürültüden çok daha az etkilenir; Eksen 1'in bileşik puanı (T162) bu bulguyla otomatik olarak çürümez |
| ⚠️ Tek judge, tek rubrik (v9) | başka rubrikte tekrarlanabilirlik ölçülmedi |
