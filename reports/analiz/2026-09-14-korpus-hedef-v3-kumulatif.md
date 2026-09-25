# Korpus hedef raporu — `v3-kumulatif.jsonl`

**Girdi:** `data/candidates/v3-kumulatif.jsonl` · SHA256 `5867e31fc49e3dbf1acf6a4ecba401a72d96e91f1d02da4dfac8582a66769cf9`  
**Betik:** `scripts/analiz/2026-09-14-korpus-hedef-raporu.py` · **Tarih:** 2026-09-14  
**Hedef kaynağı:** `prompts/uretim-v3.md` §2, §3b, §5a, §5c, §8  
**Kayıt sayısı:** 104 · **Üretim talimatı:** `uretim-v3` × 104

> Sapma bandı ✅ ≤ 5 puan · ⚠️ ≤ 10 puan · ❌ > 10 puan. **Bu band bizim konvansiyonumuzdur**, literatürden gelmiyor (Kural 6).

---

## 1. Sert kapılar (`src/checks.py`)

- Kapılardan geçen: **104/104**
- Soru sayısı ≤ 1 kapısı: tüm kayıtlarda geçerli (kapı `checks.py` içinde)

Kapı düşüren kayıt yok.

## 2. v3 korpus hedefleri

### 2a. Tur kapanışı (§5a) — beyan: `gen_meta.turn_ending`

| Değer | Adet | Oran | Hedef | Sapma | |
|---|---:|---:|---:|---:|:--:|
| `acik_uclu_soru` | 51 | %49 | %50 | -1 p | ✅ |
| `takdir` | 16 | %15 | %15 | +0 p | ✅ |
| `ozet` | 16 | %15 | %15 | +0 p | ✅ |
| `yalnizca_yansitma` | 16 | %15 | %15 | +0 p | ✅ |
| `durur` | 5 | %5 | %5 | -0 p | ✅ |

**Metinden doğrudan ölçüm:** soruyla biten cevap **51/104** (%49) — hedef ~%50, sapma -1 p ✅

> Bu satır beyandan bağımsızdır: soru işareti sayılır, beyan okunmaz. Beyan eksik olsa da bu ölçüm her korpusta yapılabilir.

Beyan ile metin arasında tutarsızlık yok.

### 2b. Konuşma durumu (§3b) — beyan: `gen_meta.konusma_durumu`

| Değer | Adet | Oran | Hedef | Sapma | |
|---|---:|---:|---:|---:|:--:|
| `tetikleyici_an` | 36 | %35 | %35 | -0 p | ✅ |
| `suregiden_durum` | 21 | %20 | %20 | +0 p | ✅ |
| `iyi_giden_paylasim` | 16 | %15 | %15 | +0 p | ✅ |
| `plan_yapma` | 16 | %15 | %15 | +0 p | ✅ |
| `merak_sorusu` | 10 | %10 | %10 | -0 p | ✅ |
| `aradan_donus` | 5 | %5 | %5 | -0 p | ✅ |

### 2c. MI süreci (§5c) — alan: `mi_process`

| Değer | Adet | Oran | Hedef | Sapma | |
|---|---:|---:|---:|---:|:--:|
| `engaging` | 41 | %39 | %40 | -1 p | ✅ |
| `focusing` | 21 | %20 | %20 | +0 p | ✅ |
| `evoking` | 26 | %25 | %25 | +0 p | ✅ |
| `planning` | 16 | %15 | %15 | +0 p | ✅ |

### 2d. System prompt varyantı (§2)

| Değer | Adet | Oran | Hedef | Sapma | |
|---|---:|---:|---:|---:|:--:|
| `canon` | 81 | %78 | %78 | +0 p | ✅ |
| `paraphrase` | 23 | %22 | %22 | -0 p | ✅ |

### 2e. Özerklik vurgusu (§5a)

| Ölçüm | Adet | Oran | Hedef | Sapma | |
|---|---:|---:|---:|---:|:--:|
| özerklik kalıbı — dar desen | 15 | %14 | %20 | -6 p | ⚠️ |
| özerklik kalıbı — geniş desen | 24 | %23 | %20 | +3 p | ✅ |

> İki vekil desen de **alt sınır ölçer** (K40): kalıp dışı kurulmuş özerklik cümlesini kaçırır. Dar desen K20 ifade bankası kalıplarından geliyor; geniş desen kararın sahibini adlandıran kalıpları da sayıyor (*"o karar senin", "ben karar vermiyorum"*). **Geçerli sayı geniş olandır**; dar desen v2 raporlarıyla karşılaştırılabilsin diye duruyor.

> ⚠️ Geniş desen 2026-09-14'te `v3-parti1` okunduktan sonra yazıldı, yani o korpus için kör bir ölçüm değil. Körlük sınaması `expert-70` üzerinde yapıldı: %3 → %6. Genişletme v2'yi hedefe taşımıyor.

### 2f. `is_negative` (§8)

| Ölçüm | Adet | Oran | Hedef | Sapma | |
|---|---:|---:|---:|---:|:--:|
| `is_negative` | 16 | %15 | %15 | +0 p | ✅ |

## 3. Hedefi olmayan dağılımlar (betimsel)

| Ölçüm | Değer |
|---|---|
| Çok turlu (`turn_type=multi`) | 32/104 (%31) |
| Bağlam modu (`context` dolu) | 10/104 (%10) |
| Kriz (`is_crisis`) | 0/104 |
| Cevap uzunluğu (karakter) | medyan 264 · min 93 · maks 494 |
| `thinking:completion` oranı | ortalama 2.56x · maks 3.96x (tavan 4x) |
| Tavanı aşan kayıt | 0  |
| Yinelenen `id` | 0 |
| Yinelenen son kullanıcı mesajı | 0 |

### 3a. Kullanıcı mesajı biçimi (§3a / K42)

| Bant | Adet |
|---|---:|
| kisa (1-8) | 3 |
| ara (9-14) | 18 |
| orta (15-40) | 53 |
| uzun (40+) | 30 |

> `ara (9-14)` v3 §3a'da tanımlı bir bant değil; oradaki kayıtlar biçim hedefinin dışında kalmış demektir.

## 4. Özet

- Beyana dayanmadan ölçülebilen 9 hedefin **9 tanesi bandın içinde**, **0 tanesi dışında**.
