# Düşünme döngüsü ne kadar yaygın

**Betik:** `scripts/analiz/2026-09-24-dusunme-dongusu.py` · **Tarih:** 2026-09-24  
**Veri:** kayıtlı eksen koşularının `thinking` alanı — yeni koşu yok. Taban tek koşu (124 öge), `d1`/`e3` 8 tohum × 124 öge. Değerler tohum başına yüzde, ort ± 2·SE.

## Bilinen pozitif — demo örneği

| ölçü | değer | yakaladı mı |
|---|---:|---|
| distinct-5 (eşik 0.5) | 0.881 | ⛔ HAYIR |
| cümle döngüsü (≥4 sözcük, ≥3 kez) | en çok 4 kez | ✓ |

## Kollara göre

| ölçü | taban | `d1` (v0.0.18) | `e3` (v0.1.0) |
|---|---:|---:|---:|
| cümle döngüsü | 0.0 | 14.3 ± 2.5 | 11.6 ± 2.3 |
| distinct-5 < 0,5 (mevcut kapı) | 0.0 | 8.0 ± 2.8 | 4.4 ± 1.1 |
| boş cevap | 0.0 | 6.1 ± 2.3 | 4.3 ± 0.9 |
| üretim yok | 0.0 | 0.0 ± 0.0 | 0.0 ± 0.0 |
| bütçe kesildi (1024 jeton) | 0.0 | 6.7 ± 2.0 | 5.1 ± 0.9 |
| herhangi dejenerasyon | 0.0 | 8.3 ± 2.7 | 5.2 ± 1.0 |
| düşünme uzunluğu, ortanca sözcük | 300 | 82 | 82 |

## Eksene göre — cümle döngüsü

| eksen | taban | `d1` | `e3` |
|---|---:|---:|---:|
| `safety` | 0.0 | 35.0 ± 5.0 | 25.0 ± 8.0 |
| `forget` | 0.0 | 0.0 ± 0.0 | 0.0 ± 0.0 |
| `context_fidelity` | 0.0 | 11.9 ± 5.6 | 12.5 ± 8.0 |
| `sycophancy` | 0.0 | 16.1 ± 7.1 | 12.5 ± 5.0 |
| `cfreal` | 0.0 | 12.5 ± 7.7 | 7.5 ± 3.9 |
| `cfo` | 0.0 | 17.5 ± 8.7 | 18.3 ± 4.9 |

## Döngü cevabı bozuyor mu

| kol | döngülü öge | bunların boş cevaplı olanı | döngüsüz ögelerde boş cevap |
|---|---:|---:|---:|
| `taban` | 0 / 124 | — | 0% |
| `d1` | 142 / 992 | 34% | 2% |
| `e3` | 115 / 992 | 28% | 1% |

## ⛔ Bunun söylemedikleri

| | |
|---|---|
| ⛔ **Cümle eşiği kalibre edilmedi** | ≥3 tekrar bir seçim; yalnız demo örneğiyle sınandı. Betimleyicidir, eleme ya da sürüm kapısı değildir |
| ⚠️ **Eval koşuları demo koşulu değil** | eval `max_tokens` 1024 ve ögenin kendi istemi; demo 2048 jeton ve kanonik system prompt |
| ⚠️ **Taban tek koşu** | tohum yok; yüzdesi bir ölçüm, dağılım değil |
| ⚠️ **Cevabın içi ölçülmedi** | yalnız `thinking` alanı; cevaptaki tekrar ayrı konu |
