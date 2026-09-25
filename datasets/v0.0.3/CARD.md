# BıRAG talimat veri seti — v0.0.3

*Datasheets for Datasets* yapısında (Gebru ve ark.). Bkz. `docs/tez/tez-plani.md` §3.5.

## Motivasyon

**Bu bir sürüm değil, K109'un açtığı sorunun nedensellik sınaması için derlenen settir.**

Faz 4 LoRA kapsam taraması beş kolun beşini de Eksen 2'de eledi (K109). Sebep config
değil korpustu: eğitilen model `safety_crisis`'te **yönlendirmeyi hiç yapmıyordu**
(yönlendirmesiz öğe: taban 1 → kollar 2/9/12/9/13). K110/T29 mekanizmayı düzeltti —
v0.0.2'de yönlendirme *terimi* 21 kayıtta (%21,2) geçiyordu ama **yönlendirme hamlesi
0 kayıttaydı**; korpus 17 kez *sınır çekmeyi* öğretiyordu (*"orası hekimin işi"*).

v0.0.3 = **v0.0.2 + `uretim-v4` ilk partisi** (K111). Tek soruyu sınamak için var:
korpusa yönlendirme hamlesi girerse ince ayarlı modelde refleks geri gelir mi?

**Kalite hedefi yok.** 155 kayıt v0.1.0'ın (~800-1.200, K34) beşte biridir.

## Bileşim

| Alan | Dağılım |
|---|---|
| Kayıt sayısı | **155** (162 aday − 7 güvenlik karantinası) |
| Kaynak | `uretim-v3` **99** · `uretim-v4` **38** · replay **18** |
| v0.0.2 ile ilişki | **Tam üst küme** — v0.0.2'nin 117 kaydının tamamı burada, üstüne 38 yeni |
| Dilim | terapötik tek tur 79 · terapötik çok tur 45 · RAG tek tur 11 · RAG çok tur 2 · **replay 18** |
| Replay payı | ⚠️ **%11,6** — §9 önlem 1 hedefi %15 (K12). v0.0.2'de %15,4 idi |
| Bağımlılık türü | alkol 46 · tütün 31 · kumar 27 · reçeteli ilaç 19 · dijital 14 |
| Yaş grubu | yetişkin 116 · ergen 21 |
| Motivasyon | iç 114 · aile baskısı 16 · **yasal zorunluluk (TCK 191/3) 7** |
| MI süreci | engaging 52 · evoking 35 · focusing 29 · planning 21 |
| Tur yapısı | tek 90 · çok 47 (**%34,3**) |
| Context (RAG) | 13 kayıt |
| `is_negative` | 22 |
| Kriz | **0** — bilinçli dışlama, uzman onayı bekliyor (Kural 3) |
| thinking | 137/137 terapötik kayıtta · ortanca **86 kelime** · completion ortanca **40** · oran **2,08x** (§7 hedefi ~2x, tavan 4x) |

### ⭐ v0.0.2'den ne değişti

| Eksen | v0.0.2 | v0.0.3 | Hedef |
|---|---|---|---|
| **Yönlendirme hamlesi taşıyan kayıt** | **0** | **5** (%3,6) | — (sıfırdan çıkış) |
| Kısa açılış (1-8 kelime) | 9/99 = %9,1 | 17/137 = **%12,4** | ~%40 |
| Çok turlu | %26,5 | **%34,3** | ~%40 |
| Replay payı | %15,4 | ⚠️ **%11,6** | %15 |
| thinking:completion | 2,3x | **2,08x** | ~2x |

`uretim-v4` partisinin **kendi içinde** kotalar birebir tuttu (kısa açılış %40,0, çok
turlu %40,0 — `reports/analiz/2026-09-15-v4-parti1-korpus-hedef.txt`). Korpus geneli
hedefin altında çünkü kayıtların **%72'si hâlâ v3'ten** geliyor ve v3 o eksenleri
tutturamamıştı (T25).

### §8b yönlendirme dilimi (yalnızca v4 partisinde, `gen_meta.sinir_tipi`)

| Değer | Adet |
|---|---|
| `yonlendirme_istegi` | 2 |
| `rol_siniri_yonlendirme` | 3 |
| `yonlendirme_gereksiz` (karşı kutup) | 2 |
| `sinir_cekme` | 3 |
| `yok` | 28 |
| alan yok (v3 kayıtları) | 99 |

## ⚠️ Bilinen açıklar — bu setin ölçtüğü şeyi sınırlar

1. ⚠️ **REPLAY SEYRELDİ ve Eksen 3 okumasını iki değişkenli yapıyor.** Terapötik kayıt
   99 → 137 çıkarken replay 18'de kaldı; pay %15,4'ten **%11,6**'ya indi. Bu setle
   eğitilen modelde unutma ölçümü değişirse sebep *yeni dilim* mi *seyrelen replay* mi
   ayırt edilemez. Elimizde başka açık veri replay kaydı yok; replay'i büyütmek ayrı iş.
2. ⚠️ **Yönlendirme korpus düzeyinde %3,6.** Parti içinde kota tuttu ama korpusa
   karışınca seyreliyor. Refleksi geri getirmeye yetip yetmeyeceği **bilinmiyor**.
   Yetmezse sorgulanacak şey §8b kotası değil, kotanın parti düzeyinde tanımlanması.
3. **K42 mesaj biçimi hâlâ açık.** Kısa açılış %12,4, hedef ~%40. v4 partisi kendi
   içinde %40,0 tutturdu; korpus geneli sonraki partilerle kapanır.
4. **Kriz dilimi yok.** Eksen 2 ölçümü kriz verisinin etkisini göstermez.
5. **Kapsama:** yasadışı madde dilimi ve "vahşi doğa" girdi biçimi yok.
6. ⚠️ **§7a'nın *soruldu + cevap bağlamda YOK* hücresi v4 partisinde temsil edilmiyor**
   (v0.0.2'de var). v4'ün 4 bağlam kaydı: var · var · ilgisiz · izin isteme.
7. **Hacim.** 155 kayıtta okunan kapsam-kapasite dengesi 800-1.200 kayıtta aynı kalmayabilir.

## Toplama süreci

- **Asistan tarafı:** tamamı Claude Code ile elle yazıldı (K30). Talimatlar:
  `prompts/uretim-v3.md` (99 kayıt) · `prompts/uretim-v4.md` (38 kayıt, K111).
- **v4 tasarım ızgarası:** `data/plan/v4-parti1.jsonl` — kotalar **üretimden önce**
  makine tarafından denetlendi (`scripts/analiz/2026-09-15-v4-parti1-plan.py`).
- **Replay:** `data/candidates/replay-v1.jsonl` — Apache-2.0 açık veri, 18 kayıt.
  **Judge'a girmez** (K88/K89).
- **Kapılar:** `src/checks.py` yeniden koşuldu — **162/162 geçti**.
- **Judge:** rubrik **v7** (K100), puanlayan `claude-sonnet-subagent` (K97).
  ⭐ **137 terapötik kaydın tamamı TEK dalgada, TEK judge ve TEK rubrikle** puanlandı —
  K97'nin "iki judge aynı tabloda karşılaştırılmaz" kısıtı bu sette **doğmuyor**.
  Sette kalan kayıtlarda klinik güvenlik ihlali **0/137**, rol sınırı ihlali **0/137**.
- **Karantina:** **7 kayıt** elendi (K76) — **silinmediler**, `data/guvenlik-karantinasi.jsonl`
  içinde uzman kararı bekliyorlar. 5'i v3'ten (v0.0.2'de de elenmişlerdi), **2'si v4
  partisinden**: biri `riski_atlama` (kullanıcı hafıza boşluğu ve mide ağırlığı anlatıyor,
  cevap ikisine de değinmiyor — üretici judge'a **katılıyor**, yazım hatası), biri
  `normallestirme` (*"Bunların hepsi emek"* — üretici itirazı karantina kaydında yazılı,
  ama Kural 3 sert kapı olduğu için itiraz üstünde durulmadı).

### Üretim zinciri (yeniden üretilebilir)

```
# v4 partisi
scripts/analiz/2026-09-15-v4-parti1-plan.py          # ızgara + kota denetimi
  -> data/plan/v4-parti1.jsonl
  (kayıtlar elle yazıldı — K30)
  data/candidates/v4-parti1.jsonl                     sha256[:16] ea596190dd998935
scripts/analiz/2026-09-15-judge-isleri-hazirla.py --korpus data/candidates/v4-parti1.jsonl --etiket v4-parti1-v7
scripts/analiz/2026-09-15-judge-sonuclari-topla.py v4-parti1-v7 --korpus data/candidates/v4-parti1.jsonl \
    --cikti data/judged/v4-parti1.v7.jsonl --judge-adi claude-sonnet-subagent --rubrik judge-eksen1.v7
  data/judged/v4-parti1.v7.jsonl                      sha256[:16] 9788d8638005cb66

# derleme
scripts/analiz/2026-09-15-v003-derleme.py             # v3 + replay + v4 -> judged
  data/candidates/v3-kumulatif.jsonl                  sha256[:16] 5867e31fc49e3dbf
  data/judged/v3-kumulatif.v7.jsonl                   sha256[:16] fa2ce941a7cce793
  data/candidates/replay-v1.jsonl                     sha256[:16] d543e8c66edbb855
  -> data/judged/v0.0.3.jsonl                         sha256[:16] 9451388c0533f9ea
uv run python src/build.py data/judged/v0.0.3.jsonl v0.0.3
```

## Kullanım

**Kullanılır:** K109/T26/T29'un **nedensellik sınaması** — beş kollu kapsam taraması bu
setle **aynen** tekrarlanır ve yönlendirmesiz öğe sayısına bakılır.
**Kullanılmaz:** kalite iddiası, yayın, judge kalibrasyonu, altın küme.
⚠️ Eksen 3 (unutma) sonucu bu setle **tek başına** yorumlanamaz — açık 1'e bakınız.
Eval setleriyle tohum çakışması: **yok**; v4 partisinde hariç tutma `seed_id` beyanına
değil **metne** bakıyor (K111 — `safety_crisis` sk-016 `tip: elle` olduğu için
`seed_id` taşımıyor ama cümlesi bir tohumun birebir açılışı).

## Bakım

`datasets/` IMMUTABLE (Kural 4). Bu dizin bir daha yazılmaz; sonraki turlar v0.0.4,
v0.0.5 … olarak açılır, sürüm çıktısı **v0.1.0**'dır.
