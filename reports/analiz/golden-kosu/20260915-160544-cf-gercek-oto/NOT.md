# ⛔ HATALI KOŞU — yanlış koşucu. Kanıt olarak korundu (Kural 7).

Eksen 4 seti `golden_eval.py` ile koşuldu; oysa Eksen 2/3/4/5'in koşucusu
`src/eksen_eval.py` ve iddia sözlüğü `src/smoke_checks.py`'de.

`golden_eval.py` bu setin kurallarını tanımıyor: her iddia
`BİLİNMEYEN KURAL: herhangi_biri` ile **false** döndü, dolayısıyla 0/20 ve 0/15
çıktı. Sayı modelin değil koşucunun sayısıdır; hiçbir yerde kullanılmamıştır.

Doğru koşular:
  reports/analiz/eksen-kosu/20260915-160933-cf-sentetik   (15/20 — K105 ile birebir)
  reports/analiz/eksen-kosu/20260915-161352-cf-gercek     (7/15)

Not: `BİLİNMEYEN KURAL` sessizce **false** dönüyor, hata vermiyor. Bilinmeyen kural
`None` (denetlenemedi) dönseydi bu koşu kendini ele verirdi — K44/T17 ailesinden
bir alet kusuru, ayrıca değerlendirilmeli.
