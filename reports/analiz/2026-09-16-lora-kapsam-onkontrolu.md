# LoRA anahtarları gerçekten eşleşiyor mu — K49'un tuzağı için önkontrol

**Betik:** `scripts/analiz/2026-09-16-lora-kapsam-onkontrolu.py` · **Tarih:** 2026-09-16  
**Girdi:** `configs/training/*.yaml` — **43** eğitim config'i  
**Girdi (repo DIŞI):** ⧉ mlx-lm modül ağacı — model **lokalde olmalı**

---

## Neden

K49: *«Eskiden burada yazan `self_attn.v_proj` hiçbir şeyle eşleşmiyordu ve
**mlx-lm uyarı vermiyordu** → koşular sanılanın yarısı kapsamla yapıldı.»*
⛔ Sessiz kalan bir eşleşmezlik, koşuyu düşürmez — **yanlış koşuyu doğru**
**sanmanıza** yol açar. ⇒ Koşudan **önce** sorulmalı.

---

## 1. Model modül ağacı

| model | lokalde | katman | ölçülen |
|---|---|---:|---|
| `mlx-community/gemma-4-12B-it-bf16` | ⛔ **hayır** | — | ⛔ **önkontrol yapılamadı** |
| `mlx-community/gemma-4-E4B-it-bf16` | ✅ evet | 42 | ✅ mlx-lm modül ağacı |

**`mlx-community/gemma-4-E4B-it-bf16` — katman başına modüller:**

| modül | katman sayısı | hangi katmanlar |
|---|---:|---|
| `mlp.down_proj` | **42**/42 | 0–41 |
| `mlp.gate_proj` | **42**/42 | 0–41 |
| `mlp.up_proj` | **42**/42 | 0–41 |
| `per_layer_input_gate` | **42**/42 | 0–41 |
| `per_layer_projection` | **42**/42 | 0–41 |
| `self_attn.k_proj` | **24**/42 | 0–23 |
| `self_attn.o_proj` | **42**/42 | 0–41 |
| `self_attn.q_proj` | **42**/42 | 0–41 |
| `self_attn.v_proj` | **24**/42 | 0–23 |

⭐⭐ **K49'un mekanizması düzeltildi:** `v_proj`/`k_proj` modelde **var** —
ama **alt** katmanlarda. `mlx_lm` `num_layers: N` **ÜSTTEN** N katman alır:

| `num_layers` | seçilen dilim | `v_proj` canlı |
|---:|---|---:|
| 8 | 34–41 | **0**/8 |
| 16 | 26–41 | **0**/16 |
| 24 | 18–41 | **0**/24 |
| 42 | 0–41 | **0**/42 |

➡️⭐⭐ *Anahtar «modelde yok» değil, **seçilen DİLİMDE yok**. Aynı anahtar*
*`num_layers` büyüyünce sessizce **canlanır**. ⇒ «Bu anahtar ölü mü»*
*sorusunun cevabı modele değil **config'in kendisine** bağlıdır ve her*
*config için ayrı sorulmalıdır. K49 doğru olguyu yanlış sebeple yazmıştı*
*ve o sebep, kapsam taramasında `num_layers` değişince yanıltıcı olurdu.*

---

## 2. Config başına — hangi anahtar kaç modüle değiyor

| config | `num_layers` | anahtar | canlı modül | |
|---|---:|---|---:|---|
| `12b-transfer` | 8 | `self_attn.q_proj` | — | ⛔ model yok |
| `e4b-thinking-dili-genis` | 42 | `self_attn.q_proj` | **42**/42 | ✅ |
| `e4b-thinking-dili-genis` | 42 | `self_attn.o_proj` | **42**/42 | ✅ |
| `e4b-thinking-dili-genis` | 42 | `mlp.gate_proj` | **42**/42 | ✅ |
| `e4b-thinking-dili-genis` | 42 | `mlp.up_proj` | **42**/42 | ✅ |
| `e4b-thinking-dili-genis` | 42 | `mlp.down_proj` | **42**/42 | ✅ |
| `e4b-thinking-dili` | 8 | `self_attn.q_proj` | **8**/8 | ✅ |
| `e4b-thinking-dili` | 8 | `self_attn.v_proj` | **0**/8 | ⛔ **ÖLÜ** |
| `e4b` | 8 | `self_attn.q_proj` | **8**/8 | ✅ |
| `f4-kapsam-A-dar` | 8 | `self_attn.q_proj` | **8**/8 | ✅ |
| `f4-kapsam-B-derin` | 42 | `self_attn.q_proj` | **42**/42 | ✅ |
| `f4-kapsam-C-dikkat` | 42 | `self_attn.q_proj` | **42**/42 | ✅ |
| `f4-kapsam-C-dikkat` | 42 | `self_attn.o_proj` | **42**/42 | ✅ |
| `f4-kapsam-D-tam` | 42 | `self_attn.q_proj` | **42**/42 | ✅ |
| `f4-kapsam-D-tam` | 42 | `self_attn.o_proj` | **42**/42 | ✅ |
| `f4-kapsam-D-tam` | 42 | `mlp.gate_proj` | **42**/42 | ✅ |
| `f4-kapsam-D-tam` | 42 | `mlp.up_proj` | **42**/42 | ✅ |
| `f4-kapsam-D-tam` | 42 | `mlp.down_proj` | **42**/42 | ✅ |
| `f4-kapsam-E-genis` | 42 | `self_attn.q_proj` | **42**/42 | ✅ |
| `f4-kapsam-E-genis` | 42 | `self_attn.o_proj` | **42**/42 | ✅ |
| `f4-kapsam-E-genis` | 42 | `mlp.gate_proj` | **42**/42 | ✅ |
| `f4-kapsam-E-genis` | 42 | `mlp.up_proj` | **42**/42 | ✅ |
| `f4-kapsam-E-genis` | 42 | `mlp.down_proj` | **42**/42 | ✅ |
| `f4b-kapsam-A-dar-280adim` | 8 | `self_attn.q_proj` | **8**/8 | ✅ |
| `f4b-kapsam-A-dar` | 8 | `self_attn.q_proj` | **8**/8 | ✅ |
| `f4b-kapsam-B-derin` | 42 | `self_attn.q_proj` | **42**/42 | ✅ |
| `f4b-kapsam-C-dikkat` | 42 | `self_attn.q_proj` | **42**/42 | ✅ |
| `f4b-kapsam-C-dikkat` | 42 | `self_attn.o_proj` | **42**/42 | ✅ |
| `f4b-kapsam-D-tam` | 42 | `self_attn.q_proj` | **42**/42 | ✅ |
| `f4b-kapsam-D-tam` | 42 | `self_attn.o_proj` | **42**/42 | ✅ |
| `f4b-kapsam-D-tam` | 42 | `mlp.gate_proj` | **42**/42 | ✅ |
| `f4b-kapsam-D-tam` | 42 | `mlp.up_proj` | **42**/42 | ✅ |
| `f4b-kapsam-D-tam` | 42 | `mlp.down_proj` | **42**/42 | ✅ |
| `f4b-kapsam-E-genis` | 42 | `self_attn.q_proj` | **42**/42 | ✅ |
| `f4b-kapsam-E-genis` | 42 | `self_attn.o_proj` | **42**/42 | ✅ |
| `f4b-kapsam-E-genis` | 42 | `mlp.gate_proj` | **42**/42 | ✅ |
| `f4b-kapsam-E-genis` | 42 | `mlp.up_proj` | **42**/42 | ✅ |
| `f4b-kapsam-E-genis` | 42 | `mlp.down_proj` | **42**/42 | ✅ |
| `f4c-doz10-A-dar` | 8 | `self_attn.q_proj` | **8**/8 | ✅ |
| `f4c-doz10-B-derin` | 42 | `self_attn.q_proj` | **42**/42 | ✅ |
| `f4c-doz10-C-dikkat` | 42 | `self_attn.q_proj` | **42**/42 | ✅ |
| `f4c-doz10-C-dikkat` | 42 | `self_attn.o_proj` | **42**/42 | ✅ |
| `f4c-doz10-D-tam` | 42 | `self_attn.q_proj` | **42**/42 | ✅ |
| `f4c-doz10-D-tam` | 42 | `self_attn.o_proj` | **42**/42 | ✅ |
| `f4c-doz10-D-tam` | 42 | `mlp.gate_proj` | **42**/42 | ✅ |
| `f4c-doz10-D-tam` | 42 | `mlp.up_proj` | **42**/42 | ✅ |
| `f4c-doz10-D-tam` | 42 | `mlp.down_proj` | **42**/42 | ✅ |
| `f4c-doz10-E-genis` | 42 | `self_attn.q_proj` | **42**/42 | ✅ |
| `f4c-doz10-E-genis` | 42 | `self_attn.o_proj` | **42**/42 | ✅ |
| `f4c-doz10-E-genis` | 42 | `mlp.gate_proj` | **42**/42 | ✅ |
| `f4c-doz10-E-genis` | 42 | `mlp.up_proj` | **42**/42 | ✅ |
| `f4c-doz10-E-genis` | 42 | `mlp.down_proj` | **42**/42 | ✅ |
| `f4c-doz25-A-dar` | 8 | `self_attn.q_proj` | **8**/8 | ✅ |
| `f4c-doz25-B-derin` | 42 | `self_attn.q_proj` | **42**/42 | ✅ |
| `f4c-doz25-C-dikkat` | 42 | `self_attn.q_proj` | **42**/42 | ✅ |
| `f4c-doz25-C-dikkat` | 42 | `self_attn.o_proj` | **42**/42 | ✅ |
| `f4c-doz25-D-tam` | 42 | `self_attn.q_proj` | **42**/42 | ✅ |
| `f4c-doz25-D-tam` | 42 | `self_attn.o_proj` | **42**/42 | ✅ |
| `f4c-doz25-D-tam` | 42 | `mlp.gate_proj` | **42**/42 | ✅ |
| `f4c-doz25-D-tam` | 42 | `mlp.up_proj` | **42**/42 | ✅ |
| `f4c-doz25-D-tam` | 42 | `mlp.down_proj` | **42**/42 | ✅ |
| `f4c-doz25-E-genis` | 42 | `self_attn.q_proj` | **42**/42 | ✅ |
| `f4c-doz25-E-genis` | 42 | `self_attn.o_proj` | **42**/42 | ✅ |
| `f4c-doz25-E-genis` | 42 | `mlp.gate_proj` | **42**/42 | ✅ |
| `f4c-doz25-E-genis` | 42 | `mlp.up_proj` | **42**/42 | ✅ |
| `f4c-doz25-E-genis` | 42 | `mlp.down_proj` | **42**/42 | ✅ |
| `g1-olcek-v006-3epoch` | 8 | `self_attn.q_proj` | **8**/8 | ✅ |
| `g1-olcek-v006-adimsabit` | 8 | `self_attn.q_proj` | **8**/8 | ✅ |
| `g2-olcek-v007-adimsabit` | 8 | `self_attn.q_proj` | **8**/8 | ✅ |
| `g2-olcek-v007-epoksabit` | 8 | `self_attn.q_proj` | **8**/8 | ✅ |
| `h-h1-capa-k8` | 8 | `self_attn.q_proj` | **8**/8 | ✅ |
| `h-h2-k16` | 16 | `self_attn.q_proj` | **16**/16 | ✅ |
| `h-h3-k24` | 24 | `self_attn.q_proj` | **24**/24 | ✅ |
| `h-h4-k32` | 32 | `self_attn.q_proj` | **32**/32 | ✅ |
| `h-h5-k16-qo` | 16 | `self_attn.q_proj` | **16**/16 | ✅ |
| `h-h5-k16-qo` | 16 | `self_attn.o_proj` | **16**/16 | ✅ |
| `h-h6-k24-qo` | 24 | `self_attn.q_proj` | **24**/24 | ✅ |
| `h-h6-k24-qo` | 24 | `self_attn.o_proj` | **24**/24 | ✅ |
| `h-h7-k24-qo-r16` | 24 | `self_attn.q_proj` | **24**/24 | ✅ |
| `h-h7-k24-qo-r16` | 24 | `self_attn.o_proj` | **24**/24 | ✅ |
| `h-h8-capa-k42-qo` | 42 | `self_attn.q_proj` | **42**/42 | ✅ |
| `h-h8-capa-k42-qo` | 42 | `self_attn.o_proj` | **42**/42 | ✅ |
| `ka-A-ilan-seyreltilmis` | 8 | `self_attn.q_proj` | **8**/8 | ✅ |
| `ka-P-plasebo` | 8 | `self_attn.q_proj` | **8**/8 | ✅ |
| `u-k10` | 10 | `self_attn.q_proj` | **10**/10 | ✅ |
| `u-k12` | 12 | `self_attn.q_proj` | **12**/12 | ✅ |
| `u-k13` | 13 | `self_attn.q_proj` | **13**/13 | ✅ |
| `u-k14` | 14 | `self_attn.q_proj` | **14**/14 | ✅ |

⛔ **1 config-anahtar çifti ÖLÜ:** `e4b-thinking-dili` → `self_attn.v_proj` (num_layers=8)

⚠️ *Varsayılan* satırlar: config `keys` yazmıyor ve mlx-lm kendi varsayılanını
kullanıyor — ⛔ o varsayılanın ne olduğu **burada sınanmadı** ve bu bir açık.

## ⛔ Bu önkontrolün söylemedikleri

| | |
|---|---|
| ⛔ **Parametre sayısı** | kaç modüle değdiği sayılıyor, kaç **parametre** eğitileceği değil; `rank` ve modül boyutu hesaba katılmadı |
| ⛔ mlx-lm **varsayılan** anahtar kümesi | `keys` yazmayan config'lerde ne hedeflendiği sınanmadı |
| ⧉ **Repo dışı bağımlılık** | model lokalde olmalı; yoksa satır `⛔ model yok` der ve **sessizce geçmez** |
| ⚠️ `num_layers` semantiği | *«üstten N»* varsayımı mlx-lm davranışıdır; sürüm değişirse bu betik de yanılır |

