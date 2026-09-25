# `is_negative` ölçüsünün noktalamaya bağımlılığı

**Betik:** `scripts/analiz/2026-09-21-red-olcusunun-noktalama-bagimliligi.py` · **Tarih:** 2026-09-21  
**Girdi:** `data/candidates/v6-parti{1..7}.jsonl`  

| dosya | SHA256-16 |
|---|---|
| `v6-parti1.jsonl` | `4eb76ca33d43bfb9` |
| `v6-parti2.jsonl` | `4f65ece0ba019105` |
| `v6-parti3.jsonl` | `a82b8d16705373f4` |
| `v6-parti4.jsonl` | `2bc2e7ec1336bdcd` |
| `v6-parti5.jsonl` | `12c263e4b2682b8d` |
| `v6-parti6.jsonl` | `23186319a6b008b1` |
| `v6-parti7.jsonl` | `c77fa6c82cb0c86c` |

Okunan kayıt **412** · kayıt düzeyi beyan edilmemiş **0** (sayımın dışında)

## 1. Kullanıcı turunda talep işareti

⭐ Doğrudan ölçüm: hipotezin dayandığı şey.

| kayıt düzeyi | kayıt | talep işareti taşıyan |
|---|---:|---:|
| `duzgun` | 309 | 130/309 (%42) |
| `bozuk` | 103 | 34/103 (%33) |

## 2. (a) red diyor, (b) demiyor

⛔ Bu kayıtlarda son asistan turunda red deseni VAR; (b) onları red saymıyor çünkü kullanıcı turunda talep işareti bulamıyor.

| kayıt düzeyi | (a) red sayan | (b)'nin kaçırdığı |
|---|---:|---:|
| `duzgun` | 50 | 17/50 (%34) |
| `bozuk` | 20 | 9/20 (%45) |

## 2b. Register farkı gerçek mi — permütasyon

Gözlenen fark **0.110** (`bozuk` − `duzgun`, mutlak). Etiketler 10000 kez karıştırıldı (tohum 20260921); en az bu kadar büyük fark üretme oranı **p = 0.421**.

⛔⛔ **Fark ayırt edilemiyor.** Register'a bağlanamaz.

⭐⭐ Asıl sayı register'da değil TOPLAMDA: (a)'nın red saydığı **70** kaydın **26**'inde iki tanım ayrılıyor.


## 3. Kaçan kayıtlar

| dosya | # | kayıt düzeyi |
|---|---:|---|
| `v6-parti1.jsonl` | 1 | `duzgun` |
| `v6-parti1.jsonl` | 7 | `duzgun` |
| `v6-parti1.jsonl` | 8 | `bozuk` |
| `v6-parti1.jsonl` | 11 | `bozuk` |
| `v6-parti1.jsonl` | 14 | `bozuk` |
| `v6-parti1.jsonl` | 18 | `bozuk` |
| `v6-parti1.jsonl` | 22 | `duzgun` |
| `v6-parti1.jsonl` | 34 | `duzgun` |
| `v6-parti1.jsonl` | 58 | `bozuk` |
| `v6-parti1.jsonl` | 59 | `duzgun` |
| `v6-parti2.jsonl` | 7 | `bozuk` |
| `v6-parti2.jsonl` | 41 | `duzgun` |
| `v6-parti2.jsonl` | 46 | `duzgun` |
| `v6-parti3.jsonl` | 8 | `duzgun` |
| `v6-parti3.jsonl` | 11 | `duzgun` |
| `v6-parti3.jsonl` | 26 | `bozuk` |
| `v6-parti3.jsonl` | 34 | `duzgun` |
| `v6-parti3.jsonl` | 44 | `duzgun` |
| `v6-parti3.jsonl` | 54 | `duzgun` |
| `v6-parti4.jsonl` | 20 | `bozuk` |
| `v6-parti4.jsonl` | 24 | `bozuk` |
| `v6-parti4.jsonl` | 51 | `duzgun` |
| `v6-parti4.jsonl` | 52 | `duzgun` |
| `v6-parti4.jsonl` | 55 | `duzgun` |
| `v6-parti5.jsonl` | 7 | `duzgun` |
| `v6-parti6.jsonl` | 54 | `duzgun` |

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔⛔ **Hangi tanımın DOĞRU olduğu söylenmiyor** | (b)'nin talep şartı kavramsal olarak haklı: red bir talep gerektirir, yoksa rol sınırı ve bilgi sınırıyla karışır. Sorgulanan şey şart değil, şartın SEZİCİSİ |
| ⛔ **Sezicinin kaçırdığı her kayıt gerçek red değildir** | desen (a) da bir sözlük; (a)'nın saydığı bir kayıt rol sınırı olabilir ⇒ bu tablo «kaçan red» değil, **iki tanımın ayrıldığı yer** sayımıdır |
| ⛔ **Külliyatı ben yazdım (K30)** | kullanıcı turlarındaki noktalamayı da ben koydum; ölçülen şey gerçek kullanıcıların yazım alışkanlığı DEĞİL, benim `bozuk` register'ı kurarken kullandığım işaretler |
| ⚠️ **Kayıt düzeyi bir IZGARA hücresi** | metinden ölçülmedi; `gen_meta.register`'dan okundu |
