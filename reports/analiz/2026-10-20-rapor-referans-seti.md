# Referanslı test seti — ölçek-5k'dan 200 kayıt (BLEU/ROUGE için)

- Betik: `scripts/analiz/2026-10-20-rapor-referans-seti.py` · tarih 2026-10-20 · tohum 20261020
- Girdi: `data/candidates/olcek5k/kayit/` — 144 parça dosyası, aşama dağılımı {'B': 144} (⚠️ koşu sürerken alındı; C = Sonnet denetiminden geçmiş, B = geçmemiş)
- Çıktı: `data/eval-ref/olcek5k-ref.v1.jsonl` `d8cce150543a3470` — **200** kayıt

## Havuz

- Uygun kayıt: 3373 · elenen: {'eval tohumu': 225}
- Eval setlerinden dışlanan tohum sayısı: 144

## Bileşim

| katman (tur · biçim) | havuz | seçilen |
|---|---:|---:|
| multi · kisa | 1014 | 60 |
| multi · orta | 177 | 10 |
| multi · uzun | 146 | 9 |
| single · kisa | 326 | 19 |
| single · orta | 1132 | 68 |
| single · uzun | 578 | 34 |

| bağımlılık türü | seçilen |
|---|---:|
| alkol | 56 |
| receteli_ilac | 51 |
| tutun | 41 |
| kumar | 38 |
| dijital | 14 |

## Sınırlar

- Tohumlar eğitim verisiyle ortak (ölçek-5k'nın bütün satırları daha önce kullanılmış tohumlardan); kullanıcı metni ve referans yeni.
- Referans başka bir modelin (Haiku) cevabı: BLEU/ROUGE «bu referansa sözcük benzerliği»ni ölçer, terapötik kaliteyi değil. Aynı duruma birçok doğru cevap verilebildiği için serbest diyalogda düşük skor beklenir (K9).
