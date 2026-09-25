# Korpus hedef raporu — `expert-70.jsonl`

**Girdi:** `data/candidates/expert-70.jsonl` · SHA256 `ee61043de8d38187cc41b7a6c5391b735bfcc8daf9e12af504317ef0041aa775`  
**Betik:** `scripts/analiz/2026-09-14-korpus-hedef-raporu.py` · **Tarih:** 2026-09-14  
**Hedef kaynağı:** `prompts/uretim-v3.md` §2, §3b, §5a, §5c, §8  
**Kayıt sayısı:** 70 · **Üretim talimatı:** `uretim-v2` × 70

> Sapma bandı ✅ ≤ 5 puan · ⚠️ ≤ 10 puan · ❌ > 10 puan. **Bu band bizim konvansiyonumuzdur**, literatürden gelmiyor (Kural 6).

---

## 1. Sert kapılar (`src/checks.py`)

- Kapılardan geçen: **68/70**
- Soru sayısı ≤ 1 kapısı: tüm kayıtlarda geçerli (kapı `checks.py` içinde)

| Kayıt | Neden |
|---|---|
| 47 | thinking:completion oranı 4.16x > 4.0x tavanı |
| 50 | thinking:completion oranı 4.01x > 4.0x tavanı |

## 2. v3 korpus hedefleri

### 2a. Tur kapanışı (§5a) — beyan: `gen_meta.turn_ending`

> ⚠️ **70/70 kayıtta beyan yok** — bu hedef bu korpusta ölçülemiyor. Tutmuş sayılmaz (v3 §1).

_ölçülemedi._

**Metinden doğrudan ölçüm:** soruyla biten cevap **68/70** (%97) — hedef ~%50, sapma +47 p ❌

> Bu satır beyandan bağımsızdır: soru işareti sayılır, beyan okunmaz. Beyan eksik olsa da bu ölçüm her korpusta yapılabilir.

### 2b. Konuşma durumu (§3b) — beyan: `gen_meta.konusma_durumu`

> ⚠️ **70/70 kayıtta beyan yok** — bu hedef bu korpusta ölçülemiyor. Tutmuş sayılmaz (v3 §1).

_ölçülemedi._

### 2c. MI süreci (§5c) — alan: `mi_process`

| Değer | Adet | Oran | Hedef | Sapma | |
|---|---:|---:|---:|---:|:--:|
| `engaging` | 57 | %81 | %40 | +41 p | ❌ |
| `focusing` | 2 | %3 | %20 | -17 p | ❌ |
| `evoking` | 9 | %13 | %25 | -12 p | ❌ |
| `planning` | 2 | %3 | %15 | -12 p | ❌ |

### 2d. System prompt varyantı (§2)

| Değer | Adet | Oran | Hedef | Sapma | |
|---|---:|---:|---:|---:|:--:|
| `canon` | 63 | %90 | %78 | +12 p | ❌ |
| `paraphrase` | 7 | %10 | %22 | -12 p | ❌ |

### 2e. Özerklik vurgusu (§5a)

| Ölçüm | Adet | Oran | Hedef | Sapma | |
|---|---:|---:|---:|---:|:--:|
| özerklik kalıbı — dar desen | 2 | %3 | %20 | -17 p | ❌ |
| özerklik kalıbı — geniş desen | 4 | %6 | %20 | -14 p | ❌ |

> İki vekil desen de **alt sınır ölçer** (K40): kalıp dışı kurulmuş özerklik cümlesini kaçırır. Dar desen K20 ifade bankası kalıplarından geliyor; geniş desen kararın sahibini adlandıran kalıpları da sayıyor (*"o karar senin", "ben karar vermiyorum"*). **Geçerli sayı geniş olandır**; dar desen v2 raporlarıyla karşılaştırılabilsin diye duruyor.

> ⚠️ Geniş desen 2026-09-14'te `v3-parti1` okunduktan sonra yazıldı, yani o korpus için kör bir ölçüm değil. Körlük sınaması `expert-70` üzerinde yapıldı: %3 → %6. Genişletme v2'yi hedefe taşımıyor.

### 2f. `is_negative` (§8)

| Ölçüm | Adet | Oran | Hedef | Sapma | |
|---|---:|---:|---:|---:|:--:|
| `is_negative` | 15 | %21 | %15 | +6 p | ⚠️ |

## 3. Hedefi olmayan dağılımlar (betimsel)

| Ölçüm | Değer |
|---|---|
| Çok turlu (`turn_type=multi`) | 14/70 (%20) |
| Bağlam modu (`context` dolu) | 9/70 (%13) |
| Kriz (`is_crisis`) | 0/70 |
| Cevap uzunluğu (karakter) | medyan 169 · min 98 · maks 282 |
| `thinking:completion` oranı | ortalama 2.63x · maks 4.16x (tavan 4x) |
| Tavanı aşan kayıt | 2 [47, 50] |
| Yinelenen `id` | 0 |
| Yinelenen son kullanıcı mesajı | 0 |

### 3a. Kullanıcı mesajı biçimi (§3a / K42)

| Bant | Adet |
|---|---:|
| kisa (1-8) | 1 |
| ara (9-14) | 16 |
| orta (15-40) | 42 |
| uzun (40+) | 11 |

> `ara (9-14)` v3 §3a'da tanımlı bir bant değil; oradaki kayıtlar biçim hedefinin dışında kalmış demektir.

## 4. Özet

- Beyana dayanmadan ölçülebilen 9 hedefin **1 tanesi bandın içinde**, **8 tanesi dışında**.
  - ❌ tur kapanışı — soru oranı: %97 (hedef %50)
  - ❌ MI · engaging: %81 (hedef %40)
  - ❌ MI · focusing: %3 (hedef %20)
  - ❌ MI · evoking: %13 (hedef %25)
  - ❌ MI · planning: %3 (hedef %15)
  - ❌ özerklik vurgusu (geniş desen): %6 (hedef %20)
  - ❌ system prompt · canon: %90 (hedef %78)
  - ❌ system prompt · paraphrase: %10 (hedef %22)
- ❌ Kapıdan düşen kayıt: 2/70 (§1).
- ⚠️ Beyan eksikliği: `turn_ending` 70/70 · `konusma_durumu` 70/70 kayıtta yok — §5a ve §3b hedefleri bu korpusta **ölçülemez**.
