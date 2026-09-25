# Judge tekrar-test: aynı Sonnet, aynı rubrik, iki bağımsız geçiş

- tarih: 2026-09-15T07:24:41
- betik: `scripts/analiz/2026-09-15-judge-tekrar-test.py`
- rubrik: `judge-eksen1.v6` · judge: sonnet subagent (iki dalga)
- kaynak: `korpus-v3-claude/sonuc-ilk-dalga` (03:35 UTC dalgası) ile `korpus-v3-claude/sonuc` (03:59 UTC dalgası)
- iki bağımsız geçişi olan kayıt: **23** · anlık görüntü geç kalmış (iki kopya da 2. geçiş): 52 · karşılıksız: 0

## Sayısal eksenler

| eksen | birebir uyum | ort. |fark| | yön (2.−1.) | ≥2 puan sapan |
|---|---|---|---|---|
| `duygusal_tepki` | %70 | 0.30 | -0.13 | 0/23 |
| `yorumlama` | %65 | 0.35 | +0.26 | 0/23 |
| `kesif` | %91 | 0.09 | +0.09 | 0/23 |
| `grounding` | %100 | 0.00 | +0.00 | 0/23 |
| `anlasilirlik` | %43 | 0.78 | -0.35 | 4/23 |
| `dogallik` | %91 | 0.09 | -0.09 | 0/23 |
| `mi_uyumu` | %100 | 0.00 | +0.00 | 0/23 |

## İkili boyutlar

| boyut | uyum | kappa | 1. geçiş açık | 2. geçiş açık |
|---|---|---|---|---|
| `klinik_guvenlik_ihlali` | %100 | — | 0/23 | 0/23 |
| `rol_siniri_ihlali` | %100 | 1.00 | 1/23 | 1/23 |
| `cevapsiz_soru` | %100 | — | 0/23 | 0/23 |
| `kurulmamis_mecaz` | %65 | 0.21 | 5/23 | 9/23 |
| `belirsiz_gonderge` | %61 | 0.21 | 10/23 | 11/23 |
| `ust_uste_yan_cumle` | %65 | 0.31 | 11/23 | 13/23 |
| `devrik_eksiltili` | %70 | 0.37 | 9/23 | 10/23 |
| `soyut_adlastirma` | %100 | 1.00 | 1/23 | 1/23 |
| `siz_kaymasi` | %100 | 1.00 | 1/23 | 1/23 |
| `klise_acilis` | %100 | — | 0/23 | 0/23 |
| `terapi_jargonu` | %96 | 0.00 | 0/23 | 1/23 |
| `bos_guvence` | %96 | 0.78 | 2/23 | 3/23 |
| `ovgu_tonu` | %100 | — | 0/23 | 0/23 |
| `yansitma_var` | %100 | — | 23/23 | 23/23 |
| `karmasik_yansitma` | %91 | 0.78 | 16/23 | 18/23 |
| `takdir_var` | %87 | 0.59 | 4/23 | 5/23 |
| `ozet_var` | %83 | 0.62 | 16/23 | 14/23 |
| `ozerklik_vurgusu` | %87 | 0.74 | 10/23 | 11/23 |
| `tuzak_uzman` | %100 | — | 0/23 | 0/23 |
| `tuzak_etiketleme` | %100 | — | 0/23 | 0/23 |
| `tuzak_soru_cevap` | %100 | — | 0/23 | 0/23 |
| `tuzak_erken_odak` | %100 | — | 0/23 | 0/23 |
| `tuzak_suclama` | %100 | — | 0/23 | 0/23 |
| `tuzak_erken_tavsiye` | %100 | — | 0/23 | 0/23 |

## Kararsız boyutlar

Judge kendisiyle bile anlaşamıyor — bu eksende Sonnet-Gemini karşılaştırması yapmanın anlamı yok (K61):

- `belirsiz_gonderge` — uyum %61, kappa 0.21 (1. geçiş 10, 2. geçiş 11)
- `kurulmamis_mecaz` — uyum %65, kappa 0.21 (1. geçiş 5, 2. geçiş 9)
- `ust_uste_yan_cumle` — uyum %65, kappa 0.31 (1. geçiş 11, 2. geçiş 13)
- `devrik_eksiltili` — uyum %70, kappa 0.37 (1. geçiş 9, 2. geçiş 10)
- `ozet_var` — uyum %83, kappa 0.62 (1. geçiş 16, 2. geçiş 14)
- `terapi_jargonu` — uyum %96, kappa 0.00 (1. geçiş 0, 2. geçiş 1)

## Kayıt başına toplam oynaklık

Sayısal eksenlerde toplam |fark| ortalaması: **1.6** puan/kayıt (9 eksen üzerinden)

En oynak beş kayıt: `005` (4), `012` (4), `013` (4), `006` (3), `008` (3)
En durağan beş kayıt: `104` (1), `038` (0), `042` (0), `097` (0), `102` (0)

## Gürültü tabanı — ölçülen sapma gerçek mi?

Bir eksende judge KENDİSİYLE ne kadar anlaşmıyorsa, başka bir judge'la
olan farkın o kadarı zaten gürültüdür. Modeller arası fark bu tabanı
aşmıyorsa o eksende **sapma ölçülmemiştir**, oynaklık ölçülmüştür (K61).

⚠️ İki sütun FARKLI örneklemlerden: taban korpus v3 / Sonnet-Sonnet (n=23), sapma golden dev / Gemini-Claude (n=48). Kalemler aynı değil, bu yüzden bu bir **büyüklük karşılaştırması**, kesin bir sınama değil.

| eksen | gürültü tabanı (ort.\|fark\|) | modeller arası fark | taban aşılıyor mu |
|---|---|---|---|
| `duygusal_tepki` | 0.30 | 0.15 | **HAYIR** — judge kendisiyle daha az anlaşıyor |
| `yorumlama` | 0.35 | 0.23 | **HAYIR** — judge kendisiyle daha az anlaşıyor |
| `kesif` | 0.09 | 0.54 | **evet** — sapma gerçek |
| `grounding` | 0.00 | 0.00 | ikisi de 0 — eksen sabit |
| `anlasilirlik` | 0.78 | 0.92 | sınırda — ayırt edilemez |
| `dogallik` | 0.09 | 0.33 | **evet** — sapma gerçek |
| `mi_uyumu` | 0.00 | 0.15 | **evet** — sapma gerçek |
