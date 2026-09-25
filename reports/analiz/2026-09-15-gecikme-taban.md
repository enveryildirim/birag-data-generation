# Gecikme tabanı — ince ayar ÖNCESİ

- tarih: 2026-09-15 · betik: `scripts/analiz/2026-09-15-gecikme-taban.py`
- model: temel `gemma-4-E4B-it-bf16` · **adapter yok** · `max_tokens=1024`
- ⚠️ Sayılar bu makineye ve bu yığına özgü. Taşınan şey mutlak değer değil, **öncesi/sonrası farkı**.

| koşu | n | ortanca sn | ort sn | p90 sn | en yavaş | ortanca krk | krk/sn |
|---|---:|---:|---:|---:|---:|---:|---:|
| Eksen 1 · golden.locked | 48 | 13.1 | 11.6 | 15.6 | 17.8 | 152 | 12 |
| Eksen 2 · safety_crisis | 20 | 15.1 | 14.3 | 16.9 | 17.0 | 314 | 21 |
| Eksen 3 · forgetting_smoke | 30 | 5.2 | 6.8 | 15.2 | 19.7 | 62 | 12 |
| Eksen 4 · context_fidelity | 20 | 12.4 | 12.4 | 16.2 | 16.4 | 124 | 10 |
| Eksen 5 · sycophancy | 24 | 13.3 | 13.6 | 15.9 | 17.8 | 152 | 11 |
| **tümü** | **142** | **12.9** | 11.4 | 16.2 | 19.7 | 147 | 11 |

## Okuma

### Gecikmeyi ne belirliyor

| `thinking` uzunluğu | n | ortanca sn |
|---|---:|---:|
| boş krk | 16 | 0.5 |
| 1-500 krk | 1 | 4.8 |
| 501-1500 krk | 15 | 6.7 |
| 1501-3000 krk | 109 | 13.2 |
| >3000 krk | 1 | 17.8 |

| değişken | süreyle korelasyon |
|---|---:|
| **`thinking` uzunluğu** | **0.94** |
| cevap uzunluğu | 0.47 |

- ⭐ **Gecikme neredeyse tümüyle iç muhakeme bloğudur.** `thinking` boş olan 16 kayıt ortanca **0.5 sn**; dolu olan 126 kayıt **13.1 sn**. Cevabın kendisi süreyi çok az belirliyor (0.47).
- ⚠️ **Bu muhakeme istenmedi.** Koşuların hepsinde `thinking=false` — yani `<|think|>` öneki konmadı. Model muhakemeyi kendiliğinden üretiyor ve 109/142 kayıtta uzunluğu 1500-3000 karakter arasında, girdi ne olursa olsun.
- **Pratik sonuç:** gecikmeyi düşürmenin yolu daha hızlı yığın ya da daha kısa cevap değil, **muhakemenin uzunluğunu uyarlamak**. `plan.md` Faz 4 zaten *"uyarlanabilir thinking"* diyordu; bu ölçüm o karara sayı veriyor.
- **En yavaş kayıt 19.7 sn**, p90 16.2 sn. Tek turlu bir sohbet arayüzü için yüksek; İP4'te akışlı yanıt gerekir. **Bu benim okumam (Kural 6)** — ölçüm gecikmeyi söylüyor, kabul edilebilir eşiği söylemiyor.
- ⚠️ Eksen 3'ün ortancası (5.2 sn) yarı yarıya düşük çünkü o sette **sistem promptu yok**, model çoğu öğede hiç muhakeme üretmiyor. Setler arası gecikme karşılaştırması bu yüzden anlamsız; karşılaştırılacak şey her setin KENDİ öncesi/sonrasıdır.

