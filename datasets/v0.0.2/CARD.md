# BıRAG talimat veri seti — v0.0.2

*Datasheets for Datasets* yapısında (Gebru ve ark.). Bkz. `docs/tez/tez-plani.md` §3.5.

## Motivasyon

**Bu bir sürüm değil, Faz 4'ün kalibrasyon ve döngü başlangıç setidir.**

Faz 4 iterasyon döngüsünün (plan.md §13) ilk adımı veri üretmek değil, **eğitim
config'ini karara bağlamaktır**: §9 "dar LoRA tut" önlemi ile §4 "Türkçe ve kısa
düşün" hedefi ölçülmüş biçimde çelişiyor (K50 — dar LoRA thinking dilini 0/36
çeviriyor, geniş LoRA 36/36). plan.md §9 bunu *"Faz 4 öncesi kapatılması gereken
kalibrasyon kalemi"* olarak işaretliyor. Kapsam taraması sabit bir eğitim setine
ihtiyaç duyar; bu dosya o settir.

Config kararı verilmeden üretilen her kayıt, sonraki ölçümlerde **veri etkisiyle
config etkisini birbirine karıştırır** — bu yüzden sıra böyle.

**Kalite hedefi yok.** 117 kayıt v0.1.0'ın (~800-1.200, K34) yaklaşık onda biridir
ve kapsama açıkları aşağıda tek tek yazılıdır.

## Bileşim

| Alan | Dağılım |
|---|---|
| Kayıt sayısı | **117** (122 aday − 5 karantina) |
| Dilim | terapötik tek tur 60 · terapötik çok tur 30 · RAG tek tur 8 · RAG çok tur 1 · **replay 18** |
| Replay payı | **%15,4** — §9 önlem 1 hedefi %15 (K12) |
| Bağımlılık türü | alkol 35 · kumar 20 · tütün 19 · reçeteli ilaç 14 · dijital 11 · (replay: yok 18) |
| Yaş grubu | yetişkin 102 · ergen 15 |
| Motivasyon | iç 100 · aile baskısı 13 · **yasal zorunluluk (TCK 191/3) 4** |
| MI süreci | engaging 37 · evoking 26 · focusing 21 · planning 15 |
| Tur yapısı | tek 86 · çok 31 |
| Context (RAG) | 9 kayıt |
| Kriz | **0** — bilinçli dışlama, uzman onayı bekliyor (Kural 3) |
| Negatif/tuzak örnek | 16 |
| thinking | 99 kayıtta açık (replay'de yok) · ortanca **90 kelime** · completion ortanca **37** · oran **2,3x** (§7 hedefi ~2x, tavan 4x) |

## ⚠️ Bilinen açıklar — bu setin ölçtüğü şeyi sınırlar

1. **K42 mesaj biçimi dağılımı düzeltilmedi.** İlk kullanıcı mesajı: 1-8 kelime
   **9/117 (%7,7)**, ortanca **35 kelime**. Provizyonel hedef kısa açılış ~%40.
   Yani set hâlâ "zengin girdi → detaylı yansıtma" öğretiyor. Bu Faz 4'ün
   **birinci üretim kalemi**dir ve bu sette kapatılmamıştır — kapsam taraması
   config sorusunu cevaplıyor, veri sorusunu değil.
2. **Kriz dilimi yok.** Eksen 2 ölçümü bu setle eğitilmiş modelde *kriz verisinin
   etkisini* göstermez; yalnızca **gerilemediğini** gösterebilir.
3. **Kapsama:** 19 senaryodan 17'si temsil ediliyor; yasadışı madde dilimi ve
   "vahşi doğa" girdi biçimi yok (ikincisi eval tarafında da açık — plan.md Faz 3).
4. **Hacim.** 117 kayıtta okunan kapsam-kapasite dengesi, 800-1.200 kayıtta
   **aynı kalmayabilir**: LoRA kapasitesi veri hacmiyle etkileşir. Bu setten
   çıkan config bir **başlangıç noktasıdır**, nihai değil; hacim ~8x büyüdüğünde
   tarama tekrarlanmalıdır.

## Toplama süreci

- **Asistan tarafı:** tamamı Claude Code ile elle yazıldı (K30), `prompts/uretim-v3.md`
  (K55) talimatıyla. Kaynak partiler: `v3-parti1` (40, K67) · `v3-parti2-tam`
  (40, K77) · `v3-parti3` (24, K82) → `v3-kumulatif.jsonl`.
- **Replay:** `data/candidates/replay-v1.jsonl` — Apache-2.0 açık veri, 18 kayıt.
  **Judge'a girmez** (K88/K89); genel yetenek çapası olarak eklendi.
- **Kapılar:** `src/checks.py` yeniden koşuldu — **122/122 geçti**.
- **Judge:** rubrik **v7** (K100), puanlayan `claude-sonnet-subagent` (K97).
  Klinik güvenlik ihlali **0/104**. Replay'in judge kaydı yoktur ve olmamalıdır.
- **Karantina:** 5 kayıt `data/guvenlik-karantinasi.jsonl` gereği elendi (K76).
  **Silinmediler**; uzman kararına kadar beklemedeler.

### Üretim zinciri (yeniden üretilebilir)

```
scripts/analiz/2026-09-15-v002-derleme.py     # aday + v7 judge + replay -> judged
  data/candidates/v3-kumulatif.jsonl          sha256[:16] 5867e31fc49e3dbf
  data/judged/v3-kumulatif.v7.jsonl           sha256[:16] fa2ce941a7cce793
  data/candidates/replay-v1.jsonl             sha256[:16] d543e8c66edbb855
  -> data/judged/v0.0.2.jsonl                 sha256[:16] ee1b6d88dafa6b49
uv run python src/build.py data/judged/v0.0.2.jsonl v0.0.2
```

## Kullanım

**Kullanılır:** Faz 4 LoRA kapsam taraması · döngünün ilk turlarında eğitim seti.
**Kullanılmaz:** kalite iddiası, yayın, judge kalibrasyonu, altın küme.
Eval setleriyle tohum çakışması: `evals/golden.*` K31 bölmesinden gelir ve bu
setin tohumlarıyla **çakışmaz** (Faz 3'te doğrulandı).

## Bakım

`datasets/` IMMUTABLE (Kural 4). Bu dizin bir daha yazılmaz; sonraki turlar
v0.0.3, v0.0.4 … olarak açılır, sürüm çıktısı **v0.1.0**'dır.
