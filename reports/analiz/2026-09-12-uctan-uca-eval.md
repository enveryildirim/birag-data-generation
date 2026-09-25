# Uçtan uca eval — thinking dili, uzunluk ve gecikme bütçesi

**Girdi:** `runs/20260912-154712-e4b-v0.0.1-pilot/eval/20260912-171417-mt2048/generations.jsonl` (sha256:3dd2fe410a7967b6) · **Betik:** `scripts/analiz/2026-09-12-uctan-uca-eval.py` · **Tarih:** 2026-09-12

Koşu: `20260912-154712-e4b-v0.0.1-pilot` · eval kümesi **4 kayıt** (eğitimde görülmedi) · max_tokens=2048 · judge `agy:gemini-3.8-flash-high`

> **n=4.** Bu bir kalite ölçümü DEĞİL; borunun aktığını ve maliyetin ne olduğunu
> gösteren bir duman testidir. Varyantlar arası puan farkları bu ölçekte gürültüdür.

## 1. thinking dili (T12/K38'in çıkarım tarafı)

| Varyant | thinking tr | thinking en | completion tr | completion en |
|---|---|---|---|---|
| baseline | 0/4 | 4/4 | 4/4 | 0/4 |
| lora | 0/4 | 4/4 | 4/4 | 0/4 |
| *veri seti (referans)* | 20/20 | 0/20 | — | — |

**8/8** üretim thinking'e birebir aynı İngilizce kalıpla başlıyor: *"Here's a thinking process that leads to the suggested response:"* — bu Gemma'nın kendi post-training izi, bizim system prompt'umuzdan gelmiyor.

## 2. thinking uzunluğu ve thinking:cevap oranı

| Kaynak | thinking (kelime, medyan) | completion (kelime, medyan) | oran |
|---|---|---|---|
| baseline | 350 | 21 | **17x** |
| lora | 376 | 24 | **16x** |
| *veri seti (referans)* | 71 | 32 | **2x** |

## 3. Gecikme bütçesi

| Varyant | üretilen token (ort.) | tok/sn | cevap süresi (ort.) | kullanıcıya giden pay |
|---|---|---|---|---|
| baseline | 673 | 47.1 | **14.5 sn** | %5 |
| lora | 759 | 46.4 | **16.6 sn** | %6 |

## 4. Kapı ve judge sonuçları

| Varyant | checks geçen | klinik güvenlik | rol sınırı | tuzak ihlali | judge süresi (ort.) |
|---|---|---|---|---|---|
| baseline | 4/4 | 0 | 0 | 0 | 28 sn |
| lora | 2/4 | 0 | 0 | 2 | 16 sn |

### Judge rubriği (⚠️ n=4 — GÜRÜLTÜ, kalite okuması değil)

Kayda geçiriliyor çünkü ölçüldü; **yorumlanmıyor** çünkü 4 kayıtla iki varyant ayrılamaz.

| Boyut | baseline | lora |
|---|---|---|
| duygusal_tepki | 0.25 | 0.75 |
| yorumlama | 0.25 | 0.5 |
| kesif | 1.25 | 1.0 |
| mi_uyumu | 3.0 | 3.5 |
| grounding | 5.0 | 5.0 |
| kisalik_dogallik | 3.25 | 3.25 |
| dil_butunlugu | 4.75 | 4.25 |

### checks.py'nin elediği gerekçeler

- `lora` `b40d75fb` — soru sayısı 2
- `lora` `84080908` — thinking uzunluk 3260 > 3000

## 5. Kayıt başına maliyet ve Faz 4 ekstrapolasyonu

- Üretim (yerel, E4B bf16, M5 Max): **15.6 sn/kayıt** · tepe bellek 15.28 GB · model yükleme ~1 sn
- Judge (`agy`, uzaktan): **22 sn/kayıt** — yani darboğaz üretim değil, **judge**
- Eğitim (50 adım, 16 kayıt): 23.4 sn

**v0.1.0 ölçeğine (≈1.000 kayıt) doğrusal ekstrapolasyon:** eval üretimi ~4.3 saat, judge ~6.2 saat. Judge paralelleştirilmezse Faz 4'te her tur bir iş günü sürer.
