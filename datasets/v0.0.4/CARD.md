# BıRAG talimat veri seti — v0.0.4

*Datasheets for Datasets* yapısında (Gebru ve ark.). Bkz. `docs/tez/tez-plani.md` §3.5.

## Motivasyon

**Bu bir sürüm değil, T30'un DOZ-YANIT EĞRİSİ için üretilmiş deney kolu.**

T30 negatif bir sonuç kaydetti: yönlendirme hamlesini korpusa geri koymak ince ayarlı
modelde refleksi geri getirmedi. İki açıklama **ayırt edilemedi** — (a) doz yetersizdi,
(b) ilişki yapısal olarak asimetrik. Ayıracak tek deney doz-yanıt eğrisi. Bu set eğrinin
**ORTA noktası**: yönlendirme hamlesi taşıyan kayıt **14/137 = %10,2**.

| Nokta | Set | Yönlendirme | Ölçüldü mü |
|---|---|---|---|
| taban | `v0.0.2` | 2/99 = **%2,0** | ✅ (T30) |
| alt | `v0.0.3` | 7/137 = **%5,1** | ✅ (T30/K113) |
| orta | `v0.0.4` | 14/137 = **%10,2** | ⏳ |
| üst | `v0.0.5` | 33/137 = **%24,1** | ⏳ |

⚠️ Taban oranları **T32'de düzeltildi** (0 → 2 ve 5 → 7): K110'un envanteri tarayıcı
olarak eval'in **tıbbi** terim listesini kullanıyordu, *avukat* içinde yoktu ve hukuki
yönlendirme yapan iki kayıt hiç elle okunmadı. Tıbbi eksende v0.0.2 yine **0**'dır.

## ⭐ Tasarım — neden korpus BÜYÜTÜLMEDİ

K113'ün kontrol kolu şunu ölçtü: `A-dar`/v0.0.2/**280** → 2 · `A-dar`/v0.0.3/**280** → 2 ·
`A-dar`/v0.0.3/**372** → 4. Yani **adım sayısı metriği veriden daha çok oynattı.** Korpus
büyüseydi §9'un 3-epoch kuralı adımı da büyütürdü ve eğri okunamazdı.

Bu yüzden **N sabit**: 155 kayıt, üç doz noktasında da aynı. 155/155 kaydın
`id`'si v0.0.3 ile **aynı sırada aynı**. Replay payı da sabit (**11.6%**),
yani Eksen 3'ün ikinci değişkeni donduruldu. **Adım sayısı 372 olarak DEĞİŞMEZ** — doz
kolları `f4b` ailesiyle aynı adımda koşulabilir.

### Manipülasyon: eşleştirilmiş EKLEME, silme yok

7 kaydın son asistan cevabının **içine tek bir yönlendirme cümlesi eklendi**.
Kullanıcı turları, `context`, `source_ids` ve cevabın geri kalanı **bayt bayt aynı**.
Makineyle denetlenen değişmezler (`2026-09-15-doz-yanit-yamala.py`):

| | Değişmez |
|---|---|
| I1 | Kayıt sayısı, id'ler, kullanıcı mesajları, context, source_ids birebir aynı |
| I2 | Eklenen cümle çıkarılınca cevap **orijinaliyle bayt bayt aynı** |
| I3 | Orijinal cevabın **son cümlesi** yeni cevabın da son cümlesi (§5a `turn_ending` korunur) |
| I4 | Eklenen cümlede soru işareti yok → soru sayısı kapısı hiç oynamadı |
| I5 | Rakam yok · kurum özel adı yok · yordam iddiası yok (K18) |
| I6 | `v0.0.4`'ün ekleme kümesi `v0.0.5`'inkinin **öz alt kümesi** — eğri yapıca monoton |

⭐ Bunun ölçüm açısından sonucu: **sınır çekme metninin korpustaki maruziyeti üç dozda da
birebir aynı.** Silinen davranış yok; değişen tek şey, sınırın ardından bir **adım**
gösterilip gösterilmediği — T29'un ayrımı tam olarak budur.

## Bileşim

| Alan | Dağılım |
|---|---|
| Kayıt sayısı | **155** (v0.0.3 ile aynı; manifest: 155/155) |
| Terapötik / replay | 137 / 18 (**11.6%**) |
| Yönlendirme hamlesi taşıyan | **14** (**%10,2**) — 7 yama + 7 mevcut |
| Yamanın havuzu | `sinir_cekme` 5 · alan dışı 2 |
| Yamanın bağımlılık dağılımı | receteli_ilac 5 · tutun 1 · alkol 1 |
| Bağımlılık türü (korpus) | alkol 46 · tutun 31 · kumar 27 · receteli_ilac 19 · dijital 14 |
| Senaryo | farkindalik 25 · ambivalans 23 · rol_siniri 14 · inkar 10 · hedef_belirleme 10 · nazikce_karsi_cikma 9 … |
| Kriz | **0** — Kural 3, uzman onayı bekliyor |

## ⚠️ Bilinen açıklar — bu setin ölçtüğü şeyi sınırlar

1. ⚠️ **Yönlendirme dilimi KONUYA ÇARPIK.** Yamanın 5/7'i
   `receteli_ilac`, oysa korpustaki payı %14. Rol sınırı konuşmaları doğal olarak ilaç ve
   hukuk etrafında kümeleniyor. **Bilerek düzeltilmedi:** dengelemek, yönlendirmeyi yeri
   olmayan konuşmalara sokmak (U1'i çiğnemek) demekti. Çarpıklık iki dozda da benzer
   olduğu için *doz* karşılaştırmasını bozmaz, ama **genellemeyi sınırlar**.
2. ⚠️ **Üst nokta %25 değil %24,1.** Uygunluk ölçütü (U1-U7) uygulanınca havuzdan
   7 kayıt çıktı, 27 değil. Sayıyı tutturmak ölçütü sonradan gevşetmek olurdu (T24).
   Elenenlerin hepsi gerekçeli; **üçü**, kaydın KENDİ `thinking`'i yönlendirmeyi bilerek
   yapmadığını yazdığı için elendi.
3. ⚠️ **`sinir_tipi` etiketi kayıyor.** 7 kayıt `sinir_cekme`'den
   `rol_siniri_yonlendirme`'ye geçti. Defter kaydı değişti, **korpustaki metin değişmedi**
   (I2) — ama etiket üzerinden yapılacak sayımlarda bu akılda tutulmalı.
4. ⚠️ **Eklenen cümleler tek bir elden çıktı ve kalıplaşma riski taşıyor.** Bitiş kalıbı
   dağılımı üretimde denetlendi (hiçbir kalıp 2'ü aşmıyor), ama üslup
   çeşitliliği yine de 7 cümlelik bir örnekle sınırlı. Model kalıbı öğrenirse
   `safety_crisis`'in alt-dizge ölçütü bunu **başarı** sayar (T31 ailesi).
5. ⚠️ **Karşı kutup büyütülmedi.** `yonlendirme_gereksiz` iki kayıtta kaldı; doz %10,2'e
   çıkarken karşı kutup sabit. Aşırı yönlendirme bu setle ölçülemez — eval tarafında
   kontrol kutbuna bakılmalı (ve §8b onun kanıt gücünün düştüğünü yazmıştı).
6. **Kriz dilimi yok · vahşi doğa yok · yasadışı madde dilimi yok** (v0.0.3 ile aynı).
7. **Hacim.** 155 kayıt v0.1.0 hedefinin (~800-1.200, K34) beşte biri.

## Toplama süreci

- **Taban korpus:** `datasets/v0.0.3/train.jsonl`
  sha256[:16] `b50f7588e085f212` — hiçbir kaydı silinmedi.
- **Tasarım ve ölçüt:** `scripts/analiz/2026-09-15-doz-yanit-plan.py` — uygunluk ölçütü
  (U1-U7) ve düzeltme ölçütü (D1-D5) **üretimden önce** yazıldı; elenen 21 adayın hepsi
  gerekçesiyle betikte.
- **Eklemeler:** `data/candidates/doz-yonlendirme-ekleri.jsonl` — 7 cümle, elle
  yazıldı (K30), bağlamı içinde elle okundu (D5).
- **Judge:** 7 yamalı kayıt **yeniden** puanlandı (cevap değiştiği için eski
  karne geçersiz); rubrik **v7**, puanlayan `claude-sonnet-subagent` (K97). Yamasız
  130 terapötik kaydın karnesi K112'den **aynen taşındı** — metinleri
  bayt bayt aynı (I2).
- **Kapılar:** `src/checks.py` iki set için de yeniden koşuldu — **155/155 geçti**.

```
scripts/analiz/2026-09-15-yonlendirme-genis-tarama.py   # T32: taban düzeltildi
scripts/analiz/2026-09-15-doz-yanit-plan.py             # ızgara + ölçüt (üretimden ÖNCE)
  -> data/plan/doz-yanit-ekler.jsonl
  (eklemeler elle yazıldı — K30)
  data/candidates/doz-yonlendirme-ekleri.jsonl
scripts/analiz/2026-09-15-doz-yanit-yamala.py           # I1-I6 + kapılar
  -> data/candidates/v0.0.4-doz10.jsonl
scripts/analiz/2026-09-15-judge-isleri-hazirla.py --korpus <yamalı 26> --etiket doz-yama-v7
scripts/analiz/2026-09-15-judge-sonuclari-topla.py doz-yama-v7 ...
scripts/analiz/2026-09-15-doz-yanit-derleme.py          # karneleri birleştirir
  -> data/judged/v0.0.4.jsonl
uv run python src/build.py data/judged/v0.0.4.jsonl v0.0.4
  datasets/v0.0.4/train.jsonl                          sha256[:16] 8c15ee2349e45124
```

## Kullanım

**Kullanılır:** yalnızca **T30'un doz-yanıt eğrisi**. `v0.0.3` ile **aynı config, aynı
tohum, aynı adım sayısı (372)** koşulur ve `safety_crisis`'te profesyonel desteği hiç
adlandırmayan öğe sayısına bakılır. Üç nokta aynı eksende okunur.
**Kullanılmaz:** kalite iddiası, yayın, judge kalibrasyonu, altın küme, Eksen 3 yorumu.
⚠️ Yönlendirme sayıları **yukarı yönlü güvenilmez** olabilir: `safety_crisis` kabul
listesi düzeltilmeden (T31) kurum özel adı içeren bir cevap da geçer.

## Bakım

`datasets/` IMMUTABLE (Kural 4). Bu dizin bir daha yazılmaz.
