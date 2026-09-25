# Muafiyet kapısı 0/162 ateşledi — **ateşleseydi görür müydü**

**Betik:** `scripts/analiz/2026-09-16-muafiyet-kapisi-gucu.py` · **Tarih:** 2026-09-16  
**Nüfus ve karar kuralı:** `scripts/analiz/2026-09-15-v9-kapi-denetimi.py` **import edildi**, kopyalanmadı  
**Kapı:** `src/filter.py::_dogrula` — **çağrıldı**, yeniden yazılmadı  
**Arşiv:** `korpus-v9-p2`, `korpus-v9-p3`, `korpus-v9`, `v9-e2-220c3b5a`, `v9-e2-5ae67873`, `v9-e2-7ac7e984`, `v9-e2-99b69ab4`, `v9-e2-b7584bec`, `v9-e2-ceef5655`, `v9-hakem-p2`, `v9-hakem-p3`

---

## Soru

T46 ölçtü: v9'un muafiyet kapısı üretimde **hiç ateşlemedi** ve sebebini de
gösterdi — kapı ilan edildiği için judge uydurma dayanak yazmayı bıraktı.
Kapı **önleyerek** çalışıyor, **yakalayarak** sınanmamış kalıyor.
⛔ Bu, *«kapı çalışıyor»* demeye yetmez: bir uydurma dayanak GELSEYDİ kapı
onu görür müydü? ⭐ Yöntem T51'in aynısı — **kusuru üret, kapıyı ölç**.

## Nüfus — 162 muafiyet alıntısı

| Aile | vaka |
|---|---:|
| `korpus-v9` | 45 |
| `korpus-v9-p2` | 15 |
| `korpus-v9-p3` | 15 |
| `v9-e2-220c3b5a` | 7 |
| `v9-e2-5ae67873` | 7 |
| `v9-e2-7ac7e984` | 5 |
| `v9-e2-99b69ab4` | 9 |
| `v9-e2-b7584bec` | 9 |
| `v9-e2-ceef5655` | 6 |
| `v9-hakem-p2` | 17 |
| `v9-hakem-p3` | 27 |
| **TOPLAM** | **162** |

✅ Gerçek alıntıların **162/162**'i kapıdan geçiyor — *«0/162 ateşleme»* sonucunun öteki yüzü: kapı **yanlış pozitif vermiyor**.

## ⭐ Tespit gücü — bozma kipi başına

| Kip | gözlenmiş kusur | denenen | yakalanan | **güç** |
|---|---|---:|---:|---:|
| `yanlis_bolum` | ⭐ **dizge GERÇEK, yeri yanlış** — BıRAG'ın kendi cümlesi | 162 | 162 | **%100.0** |
| `ic_muhakeme` | v8 Eksen 2'de **33 vaka** (T45/T50) | 162 | 162 | **%100.0** |
| `birlestirme` | T49'un tek gerçek judge hatası | 162 | 162 | **%100.0** |
| `baska_kayit` | T50'nin takas imzası | 162 | 162 | **%100.0** |
| `kelime_dusur` | en hafif bozulma — eşleştiricinin sertliği | 107 | 107 | **%100.0** |
| **TOPLAM** | | **755** | **755** | **%100.0** |

## Alıntı uzunluğuna göre

| Gerçek alıntı | denenen | yakalanan | güç |
|---|---:|---:|---:|
| ≤25 karakter | 271 | 271 | **%100.0** |
| 26-60 karakter | 404 | 404 | **%100.0** |
| >60 karakter | 80 | 80 | **%100.0** |

## ⛔ Kaçanlar

_Yok — denenen her bozma yakalandı._

## ⭐ Karar

| | |
|---|---|
| ✅ Yanlış pozitif | 0/162 — gerçek dayanaklar kapıdan geçiyor |
| ✅ Tespit gücü | **%100.0** (755/755 bozma yakalandı) |
| ➡️ T46 | *«0 ateşleme»* artık **sessizlik değil**: nüfusun tamamında üretilen kusurlar bu oranda görülüyor |
| ⛔ Ölçmediği | judge'ın gerçek **uydurma oranı**. Bu bir duyarlılık ölçüsü; üretimde kusur gelmemesinin sebebi hâlâ **caydırıcılık** (T46) |
| ⛔ Ölçmediği | *«kaynakta var ve doğru bölümde, ama muafiyeti HAK ETMEYEN»* alıntı. Kapı dizge arar, **anlam** denetlemez — bu sınır ölçülemedi |

⚠️ **Dört kip yapı gereği kolaydır.** Kapı bir **alt-dizge** sınaması; metni
değiştiren her bozmanın yakalanması neredeyse kesin ve bu sonucu ucuzlatır.
⭐ Asıl sınama `yanlis_bolum`: dizge kaynakta **gerçekten var**, yalnızca
kapının baktığı bölümde değil (BıRAG'ın kendi cümlesine dayandırılmış bir
teselli). Gücün anlamlı kısmı orada okunmalı.
