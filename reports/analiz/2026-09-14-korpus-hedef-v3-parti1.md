# Korpus hedef raporu — `v3-parti1.jsonl`

**Girdi:** `data/candidates/v3-parti1.jsonl` · SHA256 `db683f22b74ec56b7b304b1b6ad898553d8514b0507f7f591b3e5ff57b14d6cc`  
**Betik:** `scripts/analiz/2026-09-14-korpus-hedef-raporu.py` · **Tarih:** 2026-09-14  
**Hedef kaynağı:** `prompts/uretim-v3.md` §2, §3b, §5a, §5c, §8  
**Kayıt sayısı:** 40 · **Üretim talimatı:** `uretim-v3` × 40

> Sapma bandı ✅ ≤ 5 puan · ⚠️ ≤ 10 puan · ❌ > 10 puan. **Bu band bizim konvansiyonumuzdur**, literatürden gelmiyor (Kural 6).

---

## 1. Sert kapılar (`src/checks.py`)

- Kapılardan geçen: **40/40**
- Soru sayısı ≤ 1 kapısı: tüm kayıtlarda geçerli (kapı `checks.py` içinde)

Kapı düşüren kayıt yok.

## 2. v3 korpus hedefleri

### 2a. Tur kapanışı (§5a) — beyan: `gen_meta.turn_ending`

| Değer | Adet | Oran | Hedef | Sapma | |
|---|---:|---:|---:|---:|:--:|
| `acik_uclu_soru` | 18 | %45 | %50 | -5 p | ✅ |
| `takdir` | 6 | %15 | %15 | +0 p | ✅ |
| `ozet` | 7 | %18 | %15 | +2 p | ✅ |
| `yalnizca_yansitma` | 7 | %18 | %15 | +2 p | ✅ |
| `durur` | 2 | %5 | %5 | +0 p | ✅ |

**Metinden doğrudan ölçüm:** soruyla biten cevap **18/40** (%45) — hedef ~%50, sapma -5 p ✅

> Bu satır beyandan bağımsızdır: soru işareti sayılır, beyan okunmaz. Beyan eksik olsa da bu ölçüm her korpusta yapılabilir.

Beyan ile metin arasında tutarsızlık yok.

### 2b. Konuşma durumu (§3b) — beyan: `gen_meta.konusma_durumu`

| Değer | Adet | Oran | Hedef | Sapma | |
|---|---:|---:|---:|---:|:--:|
| `tetikleyici_an` | 15 | %38 | %35 | +3 p | ✅ |
| `suregiden_durum` | 9 | %22 | %20 | +2 p | ✅ |
| `iyi_giden_paylasim` | 5 | %12 | %15 | -2 p | ✅ |
| `plan_yapma` | 6 | %15 | %15 | +0 p | ✅ |
| `merak_sorusu` | 3 | %8 | %10 | -3 p | ✅ |
| `aradan_donus` | 2 | %5 | %5 | +0 p | ✅ |

### 2c. MI süreci (§5c) — alan: `mi_process`

| Değer | Adet | Oran | Hedef | Sapma | |
|---|---:|---:|---:|---:|:--:|
| `engaging` | 17 | %42 | %40 | +2 p | ✅ |
| `focusing` | 9 | %22 | %20 | +2 p | ✅ |
| `evoking` | 8 | %20 | %25 | -5 p | ✅ |
| `planning` | 6 | %15 | %15 | +0 p | ✅ |

### 2d. System prompt varyantı (§2)

| Değer | Adet | Oran | Hedef | Sapma | |
|---|---:|---:|---:|---:|:--:|
| `canon` | 32 | %80 | %78 | +3 p | ✅ |
| `paraphrase` | 8 | %20 | %22 | -2 p | ✅ |

### 2e. Özerklik vurgusu (§5a)

| Ölçüm | Adet | Oran | Hedef | Sapma | |
|---|---:|---:|---:|---:|:--:|
| özerklik kalıbı — dar desen | 4 | %10 | %20 | -10 p | ⚠️ |
| özerklik kalıbı — geniş desen | 9 | %22 | %20 | +2 p | ✅ |

> İki vekil desen de **alt sınır ölçer** (K40): kalıp dışı kurulmuş özerklik cümlesini kaçırır. Dar desen K20 ifade bankası kalıplarından geliyor; geniş desen kararın sahibini adlandıran kalıpları da sayıyor (*"o karar senin", "ben karar vermiyorum"*). **Geçerli sayı geniş olandır**; dar desen v2 raporlarıyla karşılaştırılabilsin diye duruyor.

> ⚠️ Geniş desen 2026-09-14'te `v3-parti1` okunduktan sonra yazıldı, yani o korpus için kör bir ölçüm değil. Körlük sınaması `expert-70` üzerinde yapıldı: %3 → %6. Genişletme v2'yi hedefe taşımıyor.

### 2f. `is_negative` (§8)

| Ölçüm | Adet | Oran | Hedef | Sapma | |
|---|---:|---:|---:|---:|:--:|
| `is_negative` | 6 | %15 | %15 | +0 p | ✅ |

## 3. Hedefi olmayan dağılımlar (betimsel)

| Ölçüm | Değer |
|---|---|
| Çok turlu (`turn_type=multi`) | 10/40 (%25) |
| Bağlam modu (`context` dolu) | 0/40 (%0) |
| Kriz (`is_crisis`) | 0/40 |
| Cevap uzunluğu (karakter) | medyan 250 · min 141 · maks 441 |
| `thinking:completion` oranı | ortalama 2.58x · maks 3.96x (tavan 4x) |
| Tavanı aşan kayıt | 0  |
| Yinelenen `id` | 0 |
| Yinelenen son kullanıcı mesajı | 0 |

### 3a. Kullanıcı mesajı biçimi (§3a / K42)

| Bant | Adet |
|---|---:|
| kisa (1-8) | 1 |
| ara (9-14) | 6 |
| orta (15-40) | 23 |
| uzun (40+) | 10 |

> `ara (9-14)` v3 §3a'da tanımlı bir bant değil; oradaki kayıtlar biçim hedefinin dışında kalmış demektir.

## 4. Özet

- Beyana dayanmadan ölçülebilen 9 hedefin **9 tanesi bandın içinde**, **0 tanesi dışında**.
