# Kapsam merdiveni — kayıp eğrileri (GPU'suz ara rapor)

**Betik:** `scripts/analiz/2026-09-17-merdiven-kayip-egrileri.py` · **Tarih:** 2026-09-17 · **Veri:** `datasets/v0.0.8` (456 eğitim / 115 doğrulama)

⛔⛔ **Bu rapor merdivenin sorusunu CEVAPLAMAZ.** Merdivenin sorusu davranışsal
(yönlendirme refleksi, genel yetenek) ve yalnız üretimle ölçülür. Burada ölçülen
şey **uyum kapasitesi**. *Kayıp düşmesi davranış demek değildir* — önceki iki
taramada en iyi uyan kollar güvenlik kapısında elendi.

| kol | katman | anahtar | rank | train ilk→son | val ilk | **val en iyi** | val son | süre |
|---|---:|---:|---:|---|---:|---|---:|---:|
| `h1-capa-k8` | 8 | 1 | 8 | 3.547 → **2.622** | 3.834 | **2.654** (adım 1368) | 2.654 | 411sn |
| `h2-k16` | 16 | 1 | 8 | 3.355 → **2.365** | 3.834 | **2.428** (adım 1368) | 2.428 | 492sn |
| `h3-k24` | 24 | 1 | 8 | 3.142 → **2.133** | 3.834 | **2.209** (adım 1368) | 2.209 | 555sn |
| `h4-k32` | 32 | 1 | 8 | 3.100 → **2.045** | 3.834 | **2.126** (adım 1368) | 2.126 | 604sn |
| `h5-k16-qo` | 16 | 2 | 8 | 2.877 → **2.007** | 3.834 | **2.073** (adım 1368) | 2.073 | 492sn |
| `h6-k24-qo` | 24 | 2 | 8 | 2.664 → **1.725** | 3.834 | **1.856** (adım 1368) | 1.856 | 537sn |
| `h7-k24-qo-r16` | 24 | 2 | 16 | 2.563 → **1.594** | 3.834 | **1.809** (adım 1368) | 1.809 | 539sn |
| `h8-capa-k42-qo` | 42 | 2 | 8 | ⛔ **YARIM** (600 adımda kesildi) | 3.834 | — | — | — |

## 1. ⭐ Kapasite eğrisi — derinlik

Yalnız `q_proj`, rank 8 — tek değişken **katman sayısı**:

| katman | en iyi val | kol |
|---:|---:|---|
| 8 | **2.654** | `h1-capa-k8` |
| 16 | **2.428** | `h2-k16` |
| 24 | **2.209** | `h3-k24` |
| 32 | **2.126** | `h4-k32` |

➡️ En düşük val: **32 katman** (2.126).
⚠️ Uçlar arası fark yalnız **0.528** — kapasite artışının uyuma katkısı bu ölçekte küçük.

## 2. ⭐ Genişlik ve rank — eşleştirilmiş karşılaştırma

| karşılaştırma | önce | sonra | fark |
|---|---:|---:|---:|
| 16 katmanda **+o_proj** | 2.428 | 2.073 | **-0.355** |
| 24 katmanda **+o_proj** | 2.209 | 1.856 | **-0.353** |
| 24+o_proj'da **rank 8 → 16** | 1.856 | 1.809 | **-0.047** |

### ⭐⭐ Genişlik, derinlikten ucuz

| kol | katman | anahtar | en iyi val |
|---|---:|---:|---:|
| `h4-k32` | 32 | 1 | 2.126 |
| `h5-k16-qo` | **16** | **2** | **2.073** |

➡️⭐⭐ *`o_proj` eklemek, katman sayısını DÖRDE KATLAMAKTAN daha çok kazandırıyor: 8→32 katman 0.528 indirdi, 16 katmanda yalnız `o_proj` eklemek 0.355. Ve `h5` YARI derinlikle `h4`'ten daha iyi oturuyor (2.073 < 2.126).*

⭐ **Bu §9 açısından önemli:** §9 dar kapsam istiyor ve «dar» burada **katman** anlamına geliyordu. Ölçüm başka bir dar yön gösteriyor — az katman + iki anahtar. ⚠️ Ama bu yalnız UYUM; davranış ölçülmedi.

### ⚠️ Rank neredeyse etkisiz

Rank 8 → 16, val kaybını yalnız **-0.047** oynatıyor — `o_proj` eklemenin (-0.353) **yedide biri**. ➡️ *Parametre sayısını rank'la büyütmek bu ölçekte karşılığını vermiyor; kapsamı anahtarla genişletmek veriyor.*


## 3. ⚠️ Aşırı uyum işareti

| kol | en iyi val adımı | son adım | |
|---|---:|---:|---|
| `h1-capa-k8` | 1368 | 1368 | · (+0.000) |
| `h2-k16` | 1368 | 1368 | · (+0.000) |
| `h3-k24` | 1368 | 1368 | · (+0.000) |
| `h4-k32` | 1368 | 1368 | · (+0.000) |
| `h5-k16-qo` | 1368 | 1368 | · (+0.000) |
| `h6-k24-qo` | 1368 | 1368 | · (+0.000) |
| `h7-k24-qo-r16` | 1368 | 1368 | · (+0.000) |

⭐ Kural 5: Pareto kontrol noktası **en iyi val adımında** seçilir, son adımda değil. Kontrol noktaları her epokta kaydedildi (`save_every: 456`).

⛔⛔ **YEDİ KOLUN YEDİSİNDE DE en iyi val SON ADIMDA.** Val kaybı hâlâ düşüyordu ⇒ eğitim **yakınsamamıştı**.

➡️⭐⭐ *Merdiven, kolları yakınsamamış bir noktada karşılaştırıyor. Sıralama burada doğru olabilir ama YAKINSAMA SONRASI sıralamanın aynı kalacağını söyleyen hiçbir şey yok — dar kapsamlı kollar daha geç doyabilir. ⇒ «3 epoch» §9'un tavanı olduğu için seçildi, verinin gerektirdiği için değil; ikisi karıştırılmamalı.*

⚠️ Bu, üretim ölçümünü geçersiz kılmaz (davranış bu ağırlıklarla ölçülecek) ama **kayıp karşılaştırmasının** geçiciliğini gösterir.

## ⛔ Bu raporun söylemedikleri

| | |
|---|---|
| ⛔ **Davranış ölçülmedi** | yönlendirme refleksi ve genel yetenek üretim gerektirir; koşulmadı |
| ⛔ **Üst çapa yok** | `h8` (42 katman) yarım kaldı ⇒ eski taramalarla geniş uçta köprü kurulamıyor |
| ⛔ **Kayıp ≠ kalite** | düşük val kaybı, güvenlik kapısını geçeceği anlamına gelmez; önceki iki taramada tersi oldu |
| ⚠️ Tek tohum | kollar arası farklar tek tohumda ölçüldü |
| ⛔ **Yakınsama yok** | yedi kolun yedisinde de val hâlâ düşüyordu; sıralama yakınsama sonrası değişebilir |
