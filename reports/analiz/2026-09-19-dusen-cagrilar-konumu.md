# Düşen judge çağrıları kayda değil konuma bağlı

**Betik:** `scripts/analiz/2026-09-19-dusen-cagrilar-konumu.py` · **Tarih:** 2026-09-19  
**Sıra:** `data/judged/v0.0.14.jsonl` + tohum **11** (ölçüm betikleriyle aynı) ⇒ kuyruk 24 kayıt, 0 = ilk işlenen

⛔⛔ **Bu rapor 2026-09-18 tarihli kendi raporumu düzeltir.** Orada *«ayırt edici özellik arandı ve bulunamadı»* yazmıştım; içerikte aradım (kategori, istem uzunluğu) ve kaydın **kuyruktaki sırasına** hiç bakmadım.

## 1. ⭐⭐⭐ Düşenler nerede

| çekiliş | düşen | kuyruk konumları | ortanca konum | son çeyrekte |
|---|---:|---|---:|---:|
| C (09-18, ikinci çekiliş) | 6 | [13, 18, 20, 21, 22, 23] | 20 | 5/6 |
| E (09-19, ikinci çekiliş) | 9 | [9, 13, 17, 18, 19, 20, 21, 22, 23] | 19 | 6/9 |
| B (09-18, birinci) | 0 | — | — | — |
| D (09-19, birinci) | 0 | — | — | — |

⭐⭐ **İki günün düşenleri örtüşüyor:** 6 kayıt her iki ikinci çekilişte de düştü, konumları [13, 18, 20, 21, 22, 23]. Kuyruk sırası determinist olduğu için bu **aynı kayıtların** elenmesi demektir.

⭐⭐⭐ **Ve düşme yalnız İKİNCİ çekilişlerde:** birinci çekilişlerde (B, D) 24/24 başarılı. ➡️ *Kayıp kaydın değil **boru hattının** özelliğinden doğuyor; ölçüm aracının kendi sırası da bir değişkendir.*

## 2. ⛔ Bunun bozduğu şey

| | |
|---|---|
| ⛔⛔ **Hayatta kalan örneklem sabit bir ÖN EK** | rastgele bir alt küme değil; her ikinci çekilişte kuyruğun aynı başı ölçülüyor |
| ⛔ **T175'in «yansız sayılmadı ama yanlı da değil» şerhi zayıftı** | yanlılık vardı, yanlış yerde arandı |
| ⚠️ **Gürültü ölçümleri bundan çok etkilenmez** | karşılaştırma aynı kayıtlar üzerinde yapılıyor; etkilenen şey örneklemin TEMSİL gücü |

## 3. ⭐ Düzeltme

Ölçüm betiklerinde kuyruk sırası artık **her çekiliş için ayrı karıştırılıyor** ⇒ düşenler sabit bir ön ekte toplanmaz, örneklem kaybı rastgeleleşir. Karıştırma yalnız gönderim sırasını değiştirir; önbellek anahtarı sıraya bağlı olmadığı için `--kurtar` kipi etkilenmez.

## ⛔ Söylenmeyenler

| | |
|---|---|
| ⛔⛔ **Sebep ölçülmedi** | hız sınırlama, kota baskısı, hub sıra davranışı — hiçbiri bizden görünmüyor |
| ⛔ **İki koşu** | desen iki günde yinelendi ama n=2 koşu |
| ⛔ **Düşen listeleri elle taşındı** | koşu çıktılarından; kaynak betiğin başında yazılı (Kural 7'nin zayıf halkası) |
