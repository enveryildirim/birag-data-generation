# Kullanıcı mesajı biçim analizi — uzunluk ve yazım register'ı

**Girdi:** `data/seeds.jsonl` (sha256:0631c02ec7510af3) · `datasets/v0.0.1/train.jsonl` (sha256:cff23210d80ebd81) · **Betik:** `scripts/analiz/2026-09-12-kullanici-mesaji-bicimi.py` · **Tarih:** 2026-09-12

Soru: gerçek sohbet robotu kullanıcısı uzun paragraf yazmaz. Korpusumuz bunu temsil ediyor mu?

| Ölçüt | Tohum korpusu | v0.0.1 |
|---|---|---|
| Kayıt | 2240 | 20 |
| Kelime medyanı | **36** | **33** |
| Kelime ortalaması | 36.2 | 34.5 |
| Kelime min–maks | 6–92 | 10–57 |
| Cümle medyanı | 4 | 4 |
| Tek cümlelik mesaj | %0.2 | %5.0 |
| kısa açılış (1-8 kelime) | %0.5 | %0.0 |
| orta (9-25) | %19.6 | %20.0 |
| uzun (26-60) | %75.4 | %80.0 |
| çok uzun (60+) | %4.5 | %0.0 |
| Küçük harfle başlayan | %16.6 | %10.0 |
| Noktalamayla biten | %96.8 | %95.0 |
| Hiç noktalama yok | %0.0 | %0.0 |

## Yorum

**1-8 kelimelik mesaj ve noktalamasız mesaj korpusta hiç yok.** Gerçek kullanımda en sık
görülecek açılış biçimi (*"bırakamıyorum ya"*) eğitim verisinde %0 temsil ediliyor.

⚠️ Bu medyan **kullanıcılar hakkında bir kanıt değil** — korpus sentetik üretim, yani
bir LLM'e kullanıcı personası yazdırıldığında ne çıktığının kanıtı. Üretici artefaktı.

**İkinci risk (daha tehlikeli):** veri "zengin girdi → çok detaylı yansıtma" eşleşmesi
öğretiyor. Model bunu öğrenip karşısında iki kelime bulduğunda en olası başarısızlık
**detay uydurmak**tır. v0.0.1'de grounding 4.95/5 çıktı ama yalnızca zengin girdilerde
ölçüldü — metrik, riskin en yüksek olduğu yerde kör.

Karar: **K42** (plan.md §6).