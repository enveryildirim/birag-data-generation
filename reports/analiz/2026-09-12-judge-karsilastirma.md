# Judge karşılaştırması — kendini kayırma ölçümü

**Girdi:** `datasets/v0.0.1/train.jsonl` (sha256:cff23210d80ebd81) · ham judge çıktıları `reports/analiz/judge-karsilastirma/` · **Betik:** `scripts/analiz/2026-09-12-judge-karsilastirma.py` · **Tarih:** 2026-09-12

Üç judge, birebir aynı prompt (`prompts/judge-eksen1.v1.md`), aynı 20 kayıt.
20 kaydı **claude-sonnet-5 yazdı** — yani o judge kendi çıktısını puanlıyor.

## Boyut ortalamaları

| Boyut | Ölçek | qwen3.8-27b (bağımsız) | claude-sonnet-5 (ÜRETİCİ) | claude-opus-5 (aynı aile) | gemini-3.8-flash (bağımsız) |
|---|---|---|---|---|---|
| duygusal_tepki | 0-2 | 1.25 | 1.50 | 1.35 | 1.10 |
| yorumlama | 0-2 | 1.35 | 1.65 | 1.45 | 1.10 |
| kesif | 0-2 | 1.75 | 1.90 | 1.95 | 1.55 |
| mi_uyumu | 0-5 | 3.90 | 4.80 | 4.55 | 4.40 |
| grounding | 0-5 | 4.95 | 4.95 | 4.90 | 5.00 |
| kisalik_dogallik | 0-5 | 4.45 | 4.95 | 4.75 | 4.80 |
| dil_butunlugu | 0-5 | 4.70 | 5.00 | 4.65 | 4.90 |

## Normalize genel ortalama (0-1)

- **qwen3.8-27b (bağımsız)**: 0.825
- **claude-sonnet-5 (ÜRETİCİ)**: 0.924
- **claude-opus-5 (aynı aile)**: 0.878
- **gemini-3.8-flash (bağımsız)**: 0.814

## Bağımsız judge'a göre fark

- **claude-sonnet-5 (ÜRETİCİ)**: +0.099 (+11.9%)
- **claude-opus-5 (aynı aile)**: +0.053 (+6.4%)
- **gemini-3.8-flash (bağımsız)**: -0.011 (-1.4%)

## Kayıt bazında anlaşma

- qwen3.8-27b (bağımsız) ↔ claude-sonnet-5 (ÜRETİCİ): ortalama mutlak fark **0.127** (maks 0.400)
- qwen3.8-27b (bağımsız) ↔ claude-opus-5 (aynı aile): ortalama mutlak fark **0.084** (maks 0.329)
- qwen3.8-27b (bağımsız) ↔ gemini-3.8-flash (bağımsız): ortalama mutlak fark **0.083** (maks 0.229)
- claude-sonnet-5 (ÜRETİCİ) ↔ claude-opus-5 (aynı aile): ortalama mutlak fark **0.064** (maks 0.157)
- claude-sonnet-5 (ÜRETİCİ) ↔ gemini-3.8-flash (bağımsız): ortalama mutlak fark **0.116** (maks 0.329)
- claude-opus-5 (aynı aile) ↔ gemini-3.8-flash (bağımsız): ortalama mutlak fark **0.074** (maks 0.243)

## Sert kapı boyutları

| Judge | klinik güvenlik ihlali | rol sınırı ihlali | tuzak ihlali (toplam) |
|---|---|---|---|
| qwen3.8-27b (bağımsız) | 0 | 0 | 0 |
| claude-sonnet-5 (ÜRETİCİ) | 0 | 0 | 0 |
| claude-opus-5 (aynı aile) | 0 | 0 | 0 |
| gemini-3.8-flash (bağımsız) | 0 | 0 | 1 |
