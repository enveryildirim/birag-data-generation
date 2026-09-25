# golden.dev iddia dayanıklılığı

- tarih: 2026-09-15 · betik: `scripts/analiz/2026-09-15-golden-iddia-dayanikliligi.py`
- girdi: `evals/golden.dev.jsonl` · SHA256 `1396c6713e9b2b5d…` · öge: 48
- iddia: judge 141 · otomatik 60 · uzman 2

Kararlılık sütunu tekrar-test ölçümünden gelir (`reports/analiz/2026-09-15-judge-tekrar-test.md`, n=23, aynı Sonnet iki geçiş). Eşik: birebir uyum %85.

## Judge iddialarının dayandığı alanlar

| alan | iddia | kendisiyle uyum | |
|---|---:|---:|---|
| `mi_uyumu` | 21 | %100 |  |
| `tuzak_suclama` | 15 | %100 |  |
| `duygusal_tepki` | 10 | %70 | ⚠️ kararsız |
| `rol_siniri_ihlali` | 10 | %100 |  |
| `grounding` | 9 | %100 |  |
| `tuzak_etiketleme` | 9 | %100 |  |
| `ozerklik_vurgusu` | 9 | %87 |  |
| `tuzak_erken_tavsiye` | 8 | %100 |  |
| `yansitma_var` | 7 | %100 |  |
| `tuzak_uzman` | 7 | %100 |  |
| `kesif` | 5 | %91 |  |
| `tuzak_erken_odak` | 5 | %100 |  |
| `yorumlama` | 5 | %65 | ⚠️ kararsız |
| `bos_guvence` | 4 | %96 |  |
| `karmasik_yansitma` | 4 | %91 |  |
| `cevapsiz_soru` | 4 | %100 |  |
| `klise_acilis` | 2 | %100 |  |
| `klinik_guvenlik_ihlali` | 2 | %100 |  |
| `tuzak_soru_cevap` | 2 | %100 |  |
| `takdir_var` | 1 | %87 |  |
| `ozet_var` | 1 | %83 | ⚠️ kararsız |
| `ovgu_tonu` | 1 | %100 |  |

## Okuma

- Judge iddiası toplam **141**; kararsız eksene dayanan **16** (%11): `duygusal_tepki`×10, `yorumlama`×5, `ozet_var`×1.
- **`anlasilirlik` cetvelde hiç kullanılmıyor** — en kararsız eksen (%43 uyum) tabana girmiyor.
- En çok kullanılan iki alan `mi_uyumu` (21) ve `grounding` (9); ikisi de tekrar-testte %100.

## Bağlam (RAG) bulaşması

`rol_siniri_ihlali` üzerine **10** iddia var ve işaret ayıklaması o boyutun BAĞLAM taşıyan kayıtlarda sistematik yanlış pozitif verdiğini buldu (Fisher p=0.0001).

✅ golden.dev'de **hiç bağlamlı öge yok** — taban sayısı bu yanlış pozitiften etkilenmiyor.

⚠️ **Ama bu bir kapsam açığıdır.** Korpusta 9/104 kayıt bağlam taşıyor; cetvelde sıfır. RAG kipinde gerileme ÖLÇÜLEMEZ. Cetvel genişletilirken bağlamlı öge eklenmeli — v7'nin `rol_bilgi_baglamdan` düzeltmesinden SONRA, yoksa eklenen ögeler doğrudan yanlış pozitif üretir.
