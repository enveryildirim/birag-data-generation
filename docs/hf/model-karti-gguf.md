---
base_model: unsloth/gemma-4-E4B-it
library_name: gguf
language:
- tr
license: apache-2.0
pipeline_tag: text-generation
tags:
- gemma4
- gguf
- llama.cpp
- turkish
- addiction-support
- research-only
---

# BıRAG — Gemma 4 E4B · `v0.1.1` · GGUF ($nicemleme)

> ⛔ **Araştırma prototipi.** Kriz durumları için eğitilmedi ve klinik uzman onayından geçmedi. Kriz protokolü ve güvenlik
> katmanı olmadan gerçek kullanıcılarla kullanılmamalıdır.
>
> *Research prototype of a Turkish addiction-support assistant (Gemma 4 E4B + LoRA, merged, GGUF). Not trained for crisis
> situations, not clinically validated. Do not deploy to real users without a crisis protocol and a safety layer.*

LoRA adapter, eğitim ve veri ayrıntıları: [`$adapter_repo`](https://huggingface.co/$adapter_repo)

## Dosyalar

| | |
|---|---|
| `*.gguf` | LoRA tabana birleştirilmiş model, **$nicemleme**. Adı `mmproj` içeren dosya görü/ses içindir, yalnız metin için gerekmez |
| `sistem_istemi.txt` | uygulamanın göndereceği sistem istemi — eğitimdeki istem, başında `<|think|>` (düşünme açık) |

GGUF'a gömülü sohbet şablonu eğitimde kullanılan şablondur. Sohbette Gemma 4'ün resmi şablonuyla aynı istemi üretir.

## Kullanım — llama.cpp

```bash
./llama-server -m <model>.gguf --jinja --temp 1.0 --top-p 0.95 --top-k 64 --port 8001
```

- **`--jinja` şart:** GGUF'taki şablon ancak böyle kullanılır.
- **Düşünme:** `sistem_istemi.txt` başında `<|think|>` olduğu için açık. Bunun yanında `enable_thinking` ayarı **vermeyin**;
  iki kez açılmış olur.
- **Çıktı:** `<|channel>thought … <channel|>cevap`. Sunucu düşünceyi ayrı bir alana ayırmazsa uygulama yanıtı `<channel|>`'dan
  bölsün, kullanıcıya yalnız sonrasını göstersin.
- **Çok tur:** geçmişe yalnız görünen cevabı koyun, düşünceyi koymayın.

⚠️ **Ollama** gömülü şablon yerine kendi şablonunu kullanabilir. Cevaplar tuhafsa llama.cpp `--jinja` ile karşılaştırın.
Dışa aktarılmış modelin başka bir ortamda kötü davranmasının en sık nedeni yanlış şablon ya da EOS belirtecidir.

## Kapsam dışı

Tanı koymak · ilaç ya da doz önermek · bırakma protokolü vermek · hukuki tavsiye vermek · terapist, doktor, avukat ya da acil
servis yerine geçmek. **Kriz, intihar düşüncesi ya da tıbbi aciliyet içeren konuşmalar eğitim verisinde yoktur**; modelin bu
durumlardaki davranışı sınanmamıştır.

## Değerlendirme ve sınırlılıklar

- Son doğrulama kaybı $eval_loss · test kaybı $test_loss (ayrıntı adapter kartında).
- ⚠️ Bu model için **davranış ölçümü yapılmadı**. $nicemleme nicemlemenin etkisi ayrıca ölçülmedi.
- Veri sentetik ve yalnız Türkçe. Klinik içerik insan uzman onayından geçmedi; etik kurul değerlendirmesi henüz yok.
- E4B, projenin döngü modeli; üretim hedefi daha büyük bir Gemma 4 modeli.

## Lisans

Taban model `unsloth/gemma-4-E4B-it` apache-2.0 lisanslıdır; bu dosyalar da apache-2.0 ile paylaşılır.
