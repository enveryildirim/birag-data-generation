---
base_model: unsloth/gemma-4-26B-A4B-it
library_name: transformers
language:
- tr
license: apache-2.0
pipeline_tag: text-generation
tags:
- gemma4
- moe
- unsloth
- gguf
- llama.cpp
- turkish
- addiction-support
- research-only
---

# BıRAG — Gemma 4 26B-A4B · `v0.1.1`

> ⛔ **Araştırma prototipi.** Kriz durumları için eğitilmedi ve klinik uzman onayından geçmedi. Kriz protokolü ve güvenlik
> katmanı olmadan gerçek kullanıcılarla kullanılmamalıdır.
>
> *Research prototype of a Turkish addiction-support assistant (Gemma 4 26B-A4B, LoRA merged). Not trained for crisis
> situations, not clinically validated. Do not deploy to real users without a crisis protocol and a safety layer.*

## Nedir

**BıRAG** (*Bağımlı Bireyler için Çoklu-ajan RAG Destekli Yapay Zekâ Sohbet Robotu*) projesinin sohbet modeli.
`unsloth/gemma-4-26B-A4B-it` üzerinde LoRA ile ince ayarlandı, LoRA tabana birleştirildi. Taban model bir uzmanlar karışımı
(MoE): 128 uzmandan her jetonda 8'i çalışır.

Hedeflenen üslup Türkçe, kısa ve yargılamayan; motivasyonel görüşme ilkelerine dayanıyor: kişiyi etiketlememek, özerkliğini
korumak, değişim nedenlerini onun kendi sözlerinden çıkarmak. Model cevaptan önce Türkçe bir düşünce yazar
(`<|channel>thought … <channel|>`), sonra cevabı verir.

## Dosyalar

| dosya | ne |
|---|---|
| `model-0000{1,2}-of-00002.safetensors` | birleştirilmiş model, bf16 (~52 GB) — transformers / Unsloth / vLLM |
| `gemma-4-26b-a4b-it.Q8_0.gguf` | llama.cpp, Q8_0 (~27 GB) |
| `gemma-4-26b-a4b-it.Q4_K_M.gguf` | llama.cpp, Q4_K_M (~17 GB) — ⚠️ etkisi ölçülmedi |
| `chat_template.jinja` | Gemma 4'ün resmi sohbet şablonu (değiştirilmedi) |
| `sistem_istemi.txt` | eğitimdeki sistem istemi — uygulama bunu göndermeli |
| `Modelfile` | ⚠️ **kullanmayın** — otomatik üretildi; asistan rolünü `assistant` yazıyor (Gemma 4: `model`) ve düşünmeyi açmıyor |

## Kapsam dışı

Model şunların **yerine geçmez** ve bunları yapmamak üzere eğitildi: tanı koymak · ilaç ya da doz önermek · bırakma protokolü
vermek · hukuki tavsiye vermek · terapist, doktor, avukat ya da acil servis yerine geçmek. **Kriz, intihar düşüncesi ya da
tıbbi aciliyet içeren konuşmalar eğitim verisinde yoktur**; modelin bu durumlardaki davranışı sınanmamıştır.

## Veri

| | |
|---|---|
| veri seti | `datasets/v0.1.1` · SHA256-16 `f8fcaa1e96603cb2` · 1058 Türkçe sohbet kaydı (405'i çok turlu) |
| kaynak | büyük dil modeliyle üretilmiş **sentetik** veri; `v0.1.1`'de düşünce zincirleri, kayıtlı cevaplar ve kararlar korunarak yeniden kuruldu |
| düşünce | 1040 kayıtta var (son asistan turunda) |
| denetim | otomatik kapılar ve LLM denetçiler. ⛔ Klinik içerik **insan uzman onayından geçmedi** |
| hariç | kriz dilimi |
| bölme | `random.Random(7)` · **846 eğitim / 106 doğrulama / 106 test** |

## Eğitim

| | |
|---|---|
| taban model | `unsloth/gemma-4-26B-A4B-it` · $yukleme |
| yöntem | LoRA, Unsloth + TRL `SFTTrainer` · kayıp yalnız asistan turlarında (`train_on_responses_only`, düşünce dahil) |
| sohbet şablonu | Gemma 4'ün resmi şablonu; düşünce `reasoning_content` alanında, `enable_thinking` kayıt başına (düşüncesi olan kayıtta açık) |
| LoRA | r **$r** · alpha **$lora_alpha** · dropout $dropout · hedef: $hedef |
| optimizasyon | $optim · LR **$lr** ($zamanlayici, ısınma $isinma) · weight decay $wd |
| boyut | etkin batch $etkin_batch · $adim adım ($epoch tur) · en fazla $max_len jeton |
| dışa aktarma | LoRA tabana birleştirildi (bf16) · GGUF Q8_0 ve Q4_K_M |
| tarih | $tarih |

## Değerlendirme

| | |
|---|---|
| son doğrulama kaybı | $eval_loss |

⚠️ Bu model için **davranış ölçümü henüz tamamlanmadı.** Eğitilmemiş taban modelle kör karşılaştırma sürüyor: güvenlik, genel
yetenek, bağlama sadakat, dalkavukluk ve terapötik kalite setleri; iki bağımsız LLM judge (Qwen3-32B, Mistral-Small-3.2-24B)
ve insan etiketiyle doğrulama. Sonuçlar geldiğinde buraya eklenecek.

## Kullanım

**Kurallar** — üçü de davranışı doğrudan etkiler:

- **Düşünme `enable_thinking=True` ile açılır.** Sistem istemine elle `<|think|>` eklemeyin: bu modelin şablonu `enable_thinking`
  verilmezse istemin sonuna boş bir düşünce bloğu koyar ve düşünme sessizce kapanır.
- **Sistem istemi** `sistem_istemi.txt`'teki istemdir. İstem değiştirilirse davranış eğitimdekinden kopar.
- **Çok turda** geçmişe yalnız görünen cevabı koyun, düşünceyi koymayın. Kullanıcıya yalnız `<channel|>`'dan sonrasını gösterin.

Örnekleme: `temperature 1.0 · top_p 0.95 · top_k 64` (Gemma 4 önerisi).

### llama.cpp

```bash
llama-server -m gemma-4-26b-a4b-it.Q8_0.gguf --jinja --chat-template-kwargs '{"enable_thinking":true}' \
  --temp 1.0 --top-p 0.95 --top-k 64 -c 8192 --port 8001
```

`--jinja` ve `--chat-template-kwargs` **ikisi de şart.** 24 GB'lık bir GPU'da `--n-cpu-moe N` ile uzmanların bir kısmı CPU'da
tutulabilir. ⚠️ Ollama gömülü şablon yerine kendi şablonunu kullanabilir; cevaplar tuhafsa llama.cpp `--jinja` ile karşılaştırın.

### transformers / Unsloth

```python
from unsloth import FastModel
from huggingface_hub import hf_hub_download

REPO = "yildirim34/birag-gemma4-26b"
model, tokenizer = FastModel.from_pretrained(REPO, max_seq_length=4096, load_in_4bit=False)   # bf16 ~52 GB: A100 80GB
FastModel.for_inference(model)
tok = getattr(tokenizer, "tokenizer", tokenizer)
sistem = open(hf_hub_download(REPO, "sistem_istemi.txt"), encoding="utf-8").read()

mesajlar = [{"role": "system", "content": sistem}, {"role": "user", "content": "..."}]
istem = tok.apply_chat_template(mesajlar, tokenize=False, add_generation_prompt=True, enable_thinking=True)
x = tok(istem, add_special_tokens=False, return_tensors="pt").to("cuda")
y = model.generate(**x, max_new_tokens=2048, do_sample=True, temperature=1.0, top_p=0.95, top_k=64)
ham = tok.decode(y[0, x["input_ids"].shape[1]:], skip_special_tokens=False).split("<turn|>")[0]
cevap = ham.split("<channel|>")[-1].strip()
```

## Sınırlılıklar

- Düşünme açıkken her cevap birkaç yüz jeton gecikir.
- Veri sentetik: gerçek konuşmaların çeşitliliğini ve dilini tam taşımayabilir. Yalnız Türkçe.
- Q4_K_M nicemlemesinin davranışa etkisi ölçülmedi.
- Etik kurul değerlendirmesi ve klinik uzman onayı henüz yok.

## Lisans

Taban model `unsloth/gemma-4-26B-A4B-it` apache-2.0 lisanslıdır; bu model de apache-2.0 ile paylaşılır.
