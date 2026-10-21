# BLEU/ROUGE ve tek istek gecikmesi — İP2 ölçütleri

- Betik: `scripts/analiz/2026-10-20-rapor-bleu-gecikme-puanla.py` · tarih 2026-10-21
- Koşu: `notebooks/rapor-bleu-gecikme.ipynb` · taban `unsloth/gemma-4-26B-A4B-it` rev `60941ad6` (NVIDIA A100-SXM4-80GB, 2026-10-20 21:26) · ince `yildirim34/birag-gemma4-26b` rev `2f4a8b48` (NVIDIA A100-SXM4-80GB, 2026-10-21 02:51)
- BERTScore: `bert-base-multilingual-cased` · bert-score 0.3.12
- sacrebleu 2.6.0 · güven aralığı %95, 1000 bootstrap
- Girdiler (SHA256-16):

  - `data/eval-ref/olcek5k-ref.v1.jsonl` `d8cce150543a3470`
  - `birag-rapor-olcum/taban/referans.jsonl` `69b3138e9b5fa67f`
  - `birag-rapor-olcum/taban/bilgi.json` `2485757502c85ad9`
  - `birag-rapor-olcum/ince/referans.jsonl` `e488fcabd106bd70`
  - `birag-rapor-olcum/ince/bilgi.json` `e874422493db91b9`
  - `birag-rapor-olcum/bertscore.jsonl` `46efa77e2e3bf8f3`
  - `birag-rapor-olcum/bertscore_bilgi.json` `d07aeab5eb934df8`
  - `birag-rapor-olcum/gecikme/ince-dusunme.jsonl` `f853a1a735701fb0`
  - `birag-rapor-olcum/gecikme/ince-dusunmesiz.jsonl` `aae473ce6bb2ab9d`
  - `birag-rapor-olcum/gecikme/taban-dusunme.jsonl` `842f026d3efceffe`

## 1. Referansa benzerlik — form hedefi: BLEU veya ROUGE > %80

Referanslı set: 200 kayıt, eğitimde görülmemiş (`reports/analiz/2026-10-20-rapor-referans-seti.md`).

| ölçü | taban | ince |
|---|---:|---:|
| BLEU | **0.4** (0.2–0.5) | **5.1** (4.1–6.2) |
| chrF | **14.6** (13.3–15.8) | **33.2** (31.9–34.6) |
| ROUGE-1 | **11.3** (10.2–12.4) | **24.5** (23.1–25.8) |
| ROUGE-2 | **2.0** (1.6–2.4) | **7.7** (6.7–8.7) |
| ROUGE-L | **8.8** (7.9–9.6) | **16.3** (15.2–17.4) |
| BERTScore | **55.2** (51.6–58.4) | **69.6** (68.2–70.7) |

İki modelin de dolu cevap verdiği 163 kayıt (tabanın boş cevapları kıyas dışı):

| ölçü | taban | ince |
|---|---:|---:|
| BLEU | **0.6** (0.4–0.9) | **4.5** (3.4–5.6) |
| chrF | **17.7** (16.6–18.8) | **32.6** (31.2–34.1) |
| ROUGE-1 | **13.9** (12.7–15.0) | **24.1** (22.8–25.5) |
| ROUGE-2 | **2.4** (1.9–3.0) | **7.1** (6.1–8.1) |
| ROUGE-L | **10.7** (9.8–11.5) | **15.7** (14.6–16.7) |
| BERTScore | **67.0** (66.5–67.5) | **70.3** (69.8–70.8) |

Tek tur / çok tur:

| ölçü | taban · tek tur | taban · çok tur | ince · tek tur | ince · çok tur |
|---|---:|---:|---:|---:|
| BLEU | 0.6 | 0.1 | 5.1 | 5.1 |
| chrF | 17.3 | 10.5 | 32.9 | 33.7 |
| ROUGE-1 | 13.1 | 8.7 | 24.2 | 24.9 |
| ROUGE-2 | 2.4 | 1.3 | 7.8 | 7.5 |
| ROUGE-L | 10.2 | 6.6 | 16.3 | 16.4 |
| BERTScore | 61.7 | 45.2 | 69.3 | 70.1 |

- Boş cevap: taban 35 · ince 3 · 2048'de kesilen: taban 36 · ince 3
- Sözcük ortancası — referans 48 · taban 16 · ince 39

## 2. Tek istek gecikmesi — form hedefi: ortalama < 2 sn

| kol | n | ilk jeton ort / ortanca | görünen cevabın başlaması ort / ortanca | toplam ort / ortanca / p90 | toplam < 2 sn | jeton ortanca | üretim hızı ortanca (jeton/sn) | kesilen |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ince-dusunme | 48 | 0.48 / 0.48 | 30.13 / 28.98 | 40.07 / 39.85 / 49.74 | 0 / 48 | 278 | 7.0 | 0 |
| ince-dusunmesiz | 48 | 0.57 / 0.62 | 0.57 / 0.62 | 20.61 / 14.50 / 20.95 | 0 / 48 | 100 | 7.1 | 1 |
| taban-dusunme | 48 | 0.49 / 0.49 | 184.96 / 158.49 | 188.90 / 164.55 / 302.25 | 0 / 48 | 1122 | 6.8 | 12 |

- Ortam: Colab A100 80 GB, Hugging Face `generate` (Unsloth), bf16, açgözlü, parti 1, akışla. Üretim sunucusu (vLLM vb.) ve nicemleme bu sayıları değiştirir; burada ölçülen bu ortamdır.
- «Görünen cevabın başlaması» kullanıcının ilk harfi gördüğü an: düşünme açıkken düşünce bitene kadar bekler.
- Gecikme seti: `evals/golden.test.jsonl` (48 soru); ilk 2 istek ısınma, sayılmadı.

## Okuma

- BLEU/ROUGE «bu referansa sözcük benzerliği»dir; aynı duruma birçok doğru terapötik cevap verilebildiği için serbest diyalogda %80 beklenmez (K9). Rapor bu sayıları hedefle değil, iki modelin kıyasıyla ve BERTScore/chrF ile birlikte yorumlamalı.
