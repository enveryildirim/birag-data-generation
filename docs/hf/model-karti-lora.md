---
base_model: unsloth/gemma-4-E4B-it
library_name: peft
language:
- tr
license: apache-2.0
pipeline_tag: text-generation
tags:
- gemma4
- lora
- unsloth
- turkish
- addiction-support
- research-only
---

# BıRAG — Gemma 4 E4B · `v0.1.1` LoRA adapter

> ⛔ **Araştırma prototipi.** Kriz durumları için eğitilmedi ve klinik uzman onayından geçmedi. Kriz protokolü ve güvenlik
> katmanı olmadan gerçek kullanıcılarla kullanılmamalıdır.
>
> *Research prototype of a Turkish addiction-support assistant (LoRA on Gemma 4 E4B). Not trained for crisis situations,
> not clinically validated. Do not deploy to real users without a crisis protocol and a safety layer.*

GGUF sürümü: [`$gguf_repo`](https://huggingface.co/$gguf_repo)

## Nedir

**BıRAG** (*Bağımlı Bireyler için Çoklu-ajan RAG Destekli Yapay Zekâ Sohbet Robotu*) projesinin sohbet bileşeni için
`unsloth/gemma-4-E4B-it` üzerine eğitilmiş bir LoRA adapter. Hedeflenen üslup Türkçe, kısa ve yargılamayan; motivasyonel
görüşme ilkelerine dayanıyor: kişiyi etiketlememek, özerkliğini korumak, değişim nedenlerini onun kendi sözlerinden çıkarmak.

Model cevaptan önce Türkçe bir düşünce zinciri yazar (`<|channel>thought … <channel|>`), sonra cevabı verir.

## Kapsam dışı

Model şunların **yerine geçmez** ve bunları yapmamak üzere eğitildi: tanı koymak · ilaç ya da doz önermek · bırakma protokolü
vermek · hukuki tavsiye vermek · terapist, doktor, avukat ya da acil servis yerine geçmek. **Kriz, intihar düşüncesi ya da
tıbbi aciliyet içeren konuşmalar eğitim verisinde yoktur**; modelin bu durumlardaki davranışı sınanmamıştır.

## Veri

| | |
|---|---|
| veri seti | `datasets/v0.1.1` · SHA256-16 `$veri_sha` · 1058 Türkçe sohbet kaydı (405'i çok turlu) |
| kaynak | büyük dil modeliyle üretilmiş **sentetik** veri. `v0.1.1`'de düşünce zincirleri, kayıtlı cevaplar ve kararlar korunarak yeniden kuruldu |
| düşünce | 1040 kayıtta var (son asistan turunda) |
| denetim | otomatik kapılar ve LLM denetçiler. ⛔ Klinik içerik **insan uzman onayından geçmedi** |
| hariç | kriz dilimi |
| bölme | `random.Random(7)` · **$n_egitim eğitim / $n_dogrulama doğrulama / $n_test test** |

## Eğitim

| | |
|---|---|
| taban model | `unsloth/gemma-4-E4B-it` · bf16 (4-bit değil) |
| yöntem | LoRA, Unsloth · kayıp yalnız asistan cevaplarında (düşünce dahil) |
| LoRA | r **$r** · alpha **$lora_alpha** · dropout $dropout · hedef: $hedef |
| optimizasyon | $optim · LR **$lr** ($zamanlayici, ısınma $isinma adım) · weight decay $wd |
| boyut | etkin batch $etkin_batch · $adim adım ($epoch tur) · en fazla $max_len jeton |
| sohbet şablonu | Gemma 4 şablonu. Tek fark: eğitim hedefi olan son turun düşüncesi silinmez. Sohbette Gemma'nın resmi şablonuyla aynı istemi üretir |
| tarih · kod | $tarih · depo `$git_rev` |

## Değerlendirme

| | |
|---|---|
| son doğrulama kaybı | $eval_loss |
| test kaybı | $test_loss |

⚠️ Bu model için **davranış ölçümü yapılmadı** (güvenlik, dalkavukluk, bağlama sadakat). Projenin ön kayıtlı karşılaştırması
(`v0.1.0` ↔ `v0.1.1`) ayrı yürüyor; `v0.1.1` o karşılaştırmanın sonucundan **önce** seçildi.

## Kullanım

- **Sistem istemi:** depodaki `sistem_istemi.txt` — eğitimdeki istem, başında `<|think|>` (düşünme açık). İstem değiştirilirse
  davranış eğitimdekinden kopar.
- **Çıktı:** `<|channel>thought … <channel|>cevap`. Kullanıcıya yalnız `<channel|>`'dan sonrasını gösterin.
- **Çok tur:** geçmişe yalnız görünen cevabı koyun, düşünceyi koymayın.
- **Örnekleme:** `temperature 1.0 · top_p 0.95 · top_k 64` (Gemma 4 önerisi).

```python
from unsloth import FastModel
from huggingface_hub import hf_hub_download

model, tokenizer = FastModel.from_pretrained("$adapter_repo", max_seq_length=2048, load_in_4bit=False, token=HF_TOKEN)
FastModel.for_inference(model)
tok = getattr(tokenizer, "tokenizer", tokenizer)
sistem = open(hf_hub_download("$adapter_repo", "sistem_istemi.txt", token=HF_TOKEN), encoding="utf-8").read()

mesajlar = [{"role": "system", "content": sistem}, {"role": "user", "content": "..."}]
x = tok.apply_chat_template(mesajlar, add_generation_prompt=True, tokenize=True, return_dict=True, return_tensors="pt").to("cuda")
y = model.generate(**x, max_new_tokens=1024, temperature=1.0, top_p=0.95, top_k=64)
ham = tok.decode(y[0, x["input_ids"].shape[1]:], skip_special_tokens=False).split("<turn|>")[0]
cevap = ham.split("<channel|>")[-1].strip()
```

## Sınırlılıklar

- **E4B, projenin döngü modeli.** Üretim hedefi daha büyük bir Gemma 4 modeli.
- Düşünme açıkken her cevap birkaç yüz jeton gecikir.
- Veri sentetik: gerçek konuşmaların çeşitliliğini ve dilini tam taşımayabilir. Yalnız Türkçe.
- Etik kurul değerlendirmesi ve klinik uzman onayı henüz yok.

## Lisans

Taban model `unsloth/gemma-4-E4B-it` apache-2.0 lisanslıdır; bu adapter da apache-2.0 ile paylaşılır.
