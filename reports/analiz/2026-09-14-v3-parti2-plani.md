# v3 parti 2 — bağlamsız 32 satırın planı

**Çıktı:** `data/plan/v3-parti2.jsonl` · SHA256 `02d5f53aa59c5540a7c245631179084014c48aaf05866a6897862f491b08cb87`  
**Betik:** `scripts/analiz/2026-09-14-v3-parti2-plani.py` · **Tarih:** 2026-09-14 · **Havuz:** 1894 kullanılmamış tohum

---

## ⭐ Parti 1'den yapısal fark: plan SENARYO yazmıyor

Parti 1'de senaryo planda bağlanmıştı ve **40 satırın 13'ü tohumla çelişti** (K70) — anahtar kelime kapısı kelimeyi görüyor, durumu görmüyor. Senaryo artık tohumu okuyan **yazım adımında** belirleniyor; kapsama kaybolmasın diye üretim betiğinde **kota** olarak denetleniyor.

## Hedefler — parti 2'nin 40 kaydına göre

Bağlam dilimi (8 kayıt) ne harcadıysa kalan 32 onu tamamlıyor.

### turn_ending

| Değer | Plan | Hedef |
|---|---:|---:|
| `acik_uclu_soru` | 15 | 15 |
| `takdir` | 6 | 6 |
| `ozet` | 6 | 6 |
| `yalnizca_yansitma` | 4 | 4 |
| `durur` | 1 | 1 |

### konusma_durumu

| Değer | Plan | Hedef |
|---|---:|---:|
| `tetikleyici_an` | 13 | 13 |
| `suregiden_durum` | 7 | 7 |
| `iyi_giden_paylasim` | 6 | 6 |
| `plan_yapma` | 5 | 5 |
| `aradan_donus` | 1 | 1 |

### mi_process

| Değer | Plan | Hedef |
|---|---:|---:|
| `engaging` | 11 | 11 |
| `focusing` | 6 | 6 |
| `evoking` | 9 | 9 |
| `planning` | 6 | 6 |

### sysvar

| Değer | Plan | Hedef |
|---|---:|---:|
| `canon` | 25 | 25 |
| `paraphrase` | 7 | 7 |

### Diğer

| Ölçüm | Plan | Hedef |
|---|---:|---:|
| `is_negative` | 4 | 4 |
| özerklik görünür | 6 | 6 |
| çok turlu | 8 | 8 |
| ergen | 6 | 6 |

## ⚠️ Kriz listesi genişletildi

K65'te bulunan açık kapatıldı: `direksiyonda`, `gözüm kapandı`, `araba kullan` `KRIZ_ANAHTAR`'a eklendi. Tam liste hâlâ uzman Oturum 1'e bağlı.

