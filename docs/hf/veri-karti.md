---
language:
- tr
- en
license: $lisans
pretty_name: BıRAG — Türkçe bağımlılık destek sohbet verisi
size_categories:
- $boyut
task_categories:
- text-generation
tags:
- turkish
- addiction-support
- motivational-interviewing
- synthetic
- chain-of-thought
- conversational
- research-only
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train.jsonl
---

# BıRAG veri kümesi · `$surum` (`$seri`)

> ⛔ **Araştırma verisi.** Büyük dil modeliyle üretilmiş **sentetik** sohbetlerdir; klinik uzman onayından geçmemiştir.
> **Kriz, intihar düşüncesi ya da tıbbi aciliyet içeren konuşma yoktur** (`is_crisis` = 0). Bu veriyle eğitilen bir model, kriz
> protokolü ve güvenlik katmanı olmadan gerçek kullanıcılara açılmamalıdır.
>
> *Synthetic Turkish instruction data for an addiction-support assistant (motivational interviewing / CBT style, with
> Turkish chain-of-thought). Not clinically validated, contains no crisis conversations. Research use only. Two series:
> `refined` (record-by-record reviewed, used for the fine-tuning experiments) and `raw` (larger, automatically generated
> with Claude Haiku, not reviewed record by record).*

## Nedir

**BıRAG** (*Bağımlı Bireyler için Çoklu-ajan RAG Destekli Yapay Zekâ Sohbet Robotu*, TÜBİTAK/SBB, Kocaeli Üniversitesi)
projesinin talimat ince ayarı verisi. Her kayıt bir sohbettir: sistem istemi, kullanıcı turları ve asistan turları. Son asistan
turu cevaptan önce Türkçe bir düşünce (`thinking`) taşır.

Hedeflenen üslup kısa, yargılamayan ve motivasyonel görüşme ilkelerine dayalı: kişiyi etiketlememek, özerkliğini korumak,
değişim nedenlerini onun kendi sözlerinden çıkarmak. Model bağımlılık hakkında **olgusal bilgi ezberlemez**; bağlam verildiğinde
(RAG dilimi) cevabı yalnız o bağlama dayandırmayı öğrenir.

## Seriler

Sürümler iki seriye ayrılır. Seriler **birleşik değildir**: `raw` sürümleri `refined` kayıtlarını içermez; ikisi birlikte
kullanılacaksa dosyalar ayrıca birleştirilir.

| seri | sürümler | nasıl üretildi | en son |
|---|---|---|---|
| `refined` | $refined_surumler | Claude ile üretildi, her kayıt okunup denetlendi; `v0.1.1`'de düşünceler, cevaplar ve kararlar korunarak yeniden kuruldu. İnce ayar deneyleri (E4B, 26B-A4B) bu serinin sürümleriyle yapıldı. | `$refined_son` |
| `raw` | $raw_surumler | Claude Haiku ile üç aşamalı otomatik üretim: kullanıcı tarafı → cevap (tohumu görmeden) → hata avı. Kayıt kayıt okunmadı; 20 kayıtlık örneklem okuması var. Henüz bir modelin eğitiminde kullanılmadı. | `$raw_son` |

## Bu sürüm

| | |
|---|---|
| sürüm | `$surum` · seri `$seri` · $tarih |
| dosya | `data/train.jsonl` · SHA256-16 `$sha` |
| kayıt | **$n** · tek tur $tek · çok tur $cok |
| düşünceli kayıt | $dusunce |
| bağlamlı kayıt (RAG) | $baglam — bağlam pasajları sentetiktir (`sentetik: true`) |
| replay (genel yetenek) | $replay — düşüncesiz, Apache-2.0 kaynaklardan |

**Dilimler:** $dilimler

**Bağımlılık türleri:** $turler

**Yaş grubu:** $yas

Sürümün ayrıntılı kartı (ne değişti, güvenceler, **bilinen kusurlar**): [`CARD.md`](CARD.md) · üretim künyesi:
[`manifest.json`](manifest.json).

## Kullanım

```python
from datasets import load_dataset

ds = load_dataset("$repo", revision="refined", split="train")   # refined serisinin son sürümü
ds = load_dataset("$repo", revision="raw", split="train")       # raw serisinin son sürümü
ds = load_dataset("$repo", revision="v0.1.1", split="train")    # belirli bir sürüm
```

- **Sürüm etiketleri** (`v0.0.1` … `$son_surum`) değişmez; her birinin bir de seri önekli eşi vardır (`refined-v0.1.1`,
  `raw-v0.2.1`), ikisi aynı commit'i gösterir.
- **Dallar:** `refined` ve `raw` kendi serisinin son sürümünü, `main` en son yüklenen sürümü gösterir. Yeniden üretilebilir
  bir sonuç için dal yerine sürüm etiketi kullanın.
- Eğitimde sohbet şablonu **tokenizer'dan** uygulanmalıdır (`tokenizer.apply_chat_template`); düşünce alanı modelin
  şablonunun beklediği biçime dönüştürülmelidir.

## Alanlar

| alan | tür | açıklama |
|---|---|---|
| `id` | str | kayıt kimliği |
| `messages` | list | `{role, content}`; son asistan turunda ayrıca `thinking` |
| `context` | list \| null | RAG dilimi: `{kaynak, metin, sentetik}` pasajları; diğer dilimlerde boş liste ya da null |
| `slice` | str | `terapotik_tek_tur` · `terapotik_cok_tur` · `rag_tek_tur` · `rag_cok_tur` · `replay` |
| `scenario` | str | senaryo etiketi (ör. `ambivalans`, `rol_siniri`, `nazikce_karsi_cikma`) |
| `addiction_type` | str | `alkol` · `tutun` · `kumar` · `receteli_ilac` · `dijital` · `yok` |
| `motivation` · `mi_process` · `talk_type` | str | motivasyon kaynağı · MI süreci · konuşma türü |
| `age_group` · `turn_type` | str | `yetiskin`/`ergen` · `single`/`multi` |
| `is_crisis` · `is_negative` · `has_thinking` · `replay` | bool | bayraklar |
| `judge` | dict \| null | otomatik değerlendirme puanları |
| `gen_meta` | dict | üretim künyesi (üretici, istem sürümü, tarih, yeniden kurma kaydı) |
| `source_ids` | list | tohum / kaynak kimlikleri |

## Sınırlar

- **Sentetik.** Kullanıcı turları ve cevaplar dil modeliyle (Claude) üretildi; gerçek danışan konuşması içermez.
- **Kapsam dışı:** tanı, ilaç/doz, bırakma protokolü, hukuki tavsiye. Veri bunları yapmamayı öğretir; yerine geçmez.
- **Kriz dilimi yok** (iki seride de). Kriz davranışı uzman ve etik kurul onayı gerektirdiği için üretilmedi.
- ⛔ `refined` · `v0.1.1` ile ince ayarlanan Gemma 4 26B-A4B, değerlendirmede tabandan **kötü** çıktı ve güvenlikte geriledi
  (risk taşıyan 15 öğenin 4'ünde yönlendirme kayboldu). Bu veri tek başına güvenli bir model üretmeye yetmez.
- ⛔ `raw` · kayıtlar tek tek okunmadı ve son denetimi de Haiku yaptı; örneklem okumasında Haiku'nun denetlediği 14 kayıttan
  2'sinde ciddi kusur bulundu. Senaryo tohumları `refined` ile ortak ve 2-3 kez yeniden kullanıldı (kullanıcı metni yeni).
  Kriz dilimi olmadığı için hacmi artırmak yukarıdaki güvenlik gerilemesini onarmaz.
- `refined` serisindeki replay kayıtlarından Türkçeler makine çevirisi kaynaklardandır (`TFLai/Turkish-Alpaca`,
  `merve/turkish_instructions`); İngilizceler `OpenAssistant/oasst2`'den. `raw` serisinde replay yoktur.

## Sürümler

| sürüm | seri | tarih | kayıt | SHA256-16 |
|---|---|---|---:|---|
$surumler

Her etiketteki bu kart, sürüm yüklendiği günkü hâlindedir. ⚠️ `v0.2.1`'den önceki etiketlerin kartlarında «bağlamlı kayıt»
sayısı boş bağlam listelerini de sayıyordu (ör. `v0.1.1` 599 yazar, doğrusu 253); kayıtların kendisi doğrudur.
