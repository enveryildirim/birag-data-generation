# ⛔⛔⛔ Ölçüt, projenin YASAKLADIĞI davranışı ödüllendiriyor

**Betik:** `scripts/analiz/2026-09-17-k18-temiz-yonlendirme.py` · **Tarih:** 2026-09-17

**K18/K110:** kriz numaraları ve kurum ÖZEL ADLARI modele girmez. Ama `safety_crisis` bir cevabı *«yönlendirdi»* sayarken bunu sormuyor.

Yalnız **kriz** dilimi (15 öğe).

| katman | yönlendirme var | ⛔ **K18 ihlalli** | ⭐ **TEMİZ** | temiz puan |
|---|---:|---:|---:|---:|
| ***ham model*** | 13 | **8** | **5** | **9**/30 |
| **8** | 11 | **6** | **5** | **9**/30 |
| **10** | 8 | **5** | **3** | **5**/30 |
| **12** | 7 | **2** | **5** | **8**/30 |
| **13** | 1 | **0** | **1** | **2**/30 |
| **14** | 2 | **0** | **2** | **2**/30 |
| **16** | 1 | **0** | **1** | **1**/30 |

## ⭐⭐⭐ Ne değişiyor

Ham modelin **13** yönlendirmesinin **8'i K18 ihlalli** — telefon numarası ya da kurum özel adı içeriyor. Geriye **5** temiz yönlendirme kalıyor.

| | ham ölçüt (dereceli) | ⭐ **K18-temiz** |
|---|---:|---:|
| ham model | %70 | **9/30** |
| 8 katman | %63 | **9/30** |
| 12 katman | %46 | **8/30** |
| 13 katman | %8 | **2/30** |

➡️⭐⭐⭐ *Temiz ölçütte **8 katman ham modelle eşit** (9 = 9) ve 12 katman bir puan geride. Ham ölçütteki %70 → %46 «gerileme»nin büyük kısmı, modelin K18'i çiğneyen yönlendirmeleri BIRAKMASIYDI — yani projenin istediği şey.*

⛔ **Ama 13'teki çöküş temiz ölçütte de duruyor** (8 → 2): o gerçek.

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔ **«Temiz 5» iyi demek değil** | ham model bile 15 kriz öğesinin yalnız 5'inde temiz yönlendiriyor; «5 yeter mi» ayrı ve CEVAPLANMAMIŞ bir soru |
| ⛔ **Sayılar küçük** | 10 katmanda temiz 3 çıkıyor ve monotonluğu bozuyor ⇒ gürültü |
| ⛔ **Setler değişmedi** (K31) | bu bir ölçüm; `rakam_yok` iddiası setin kendi iddiası, kurum listesi elle (K30) |
| ⛔ **K18 ihlali tabanın kusuru, verinin değil** | ham model bu numaraları ön eğitiminden biliyor; korpusumuzda yok |
| ⚠️ **Temiz ≠ doğru** | numara vermemek yönlendirmeyi doğru yapmak demek değil |
