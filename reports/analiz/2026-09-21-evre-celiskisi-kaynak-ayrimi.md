# `evre` çelişkisinin kaynağı — parti karışımı ne kadar açıklıyor?

**Betik:** `scripts/analiz/2026-09-21-evre-celiskisi-kaynak-ayrimi.py` · **Tarih:** 2026-09-21  
**Girdi:** T220/T222/**T224** ve T221'in hükümleri (yeniden verilmedi, çağrıldı) · **296** kayıt · Monte Carlo **B=10,000**

⛔⛔ T221 sormuştu: rejim açıklamıyorsa (T222: parti1 %14 ↔ parti3-6 %10) partiler arasındaki sekiz kat farkı ne açıklıyor?

## 0. ⭐⭐⭐ Sonuç

⛔⛔⛔ **ARADIĞIM ÜÇÜNCÜ KAYNAK İÇİN KANIT YOK.** Beş partinin beşi de %95 bandının İÇİNDE. T221'de *«rejim sabitken bile sekiz kat oynuyor, demek ki üçüncü bir kaynak var»* demiştim; o cümle bir ölçüme değil, bir orana bakmaya dayanıyordu. ➡️⭐⭐⭐ *Bir oran farkı, o farkın gürültüden ayırt edilebildiği gösterilmeden bir KAYNAĞA işaret etmez; «sekiz kat» ifadesi paydası 59 olan iki sayının (1 ve 10) arasındaki farkı büyütüyordu.*

⭐ **İki şey birlikte doğru.** (a) Çelişki oranı etiketin DEĞERİNE göre dört kat değişiyor (`tolerans` %4 ↔ `merak_deneme` %21) ve partilerin karışımları farklı ⇒ karışım gerçek bir etken. (b) Ama karışım gözlenen 16 puanlık yayılımın yalnız 4 puanını üretiyor; **geri kalanı da örnekleme gürültüsünün içinde kalıyor.** Yani karışım farkı tek başına açıklamıyor, ama açıklanacak bir kalıntı olduğu da gösterilemiyor.

| parti | kayıt | gözlenen Ç | karışımdan beklenen | %95 bant | bandın dışında mı |
|---|---:|---:|---:|---|---|
| `v6-parti1` | 59 | **5** (%8) | 5.5 (%9) | 2–10 | ⭐ hayır |
| `v6-parti3` | 60 | **7** (%12) | 4.7 (%8) | 1–9 | ⭐ hayır |
| `v6-parti4` | 59 | **1** (%2) | 4.8 (%8) | 1–9 | ⭐ hayır |
| `v6-parti5` | 60 | **5** (%8) | 6.0 (%10) | 2–11 | ⭐ hayır |
| `v6-parti6` | 58 | **10** (%17) | 7.0 (%12) | 3–12 | ⭐ hayır |

⭐ **Hiçbir parti bandın dışında değil** — en uç olan `v6-parti4` (1 gözlenen, bant 1-9) tam alt sınırda ve o bile içeride. ⛔ *«Bandın içinde»* demek *«fark yok»* demek değil: bu veriyle fark GÖSTERİLEMİYOR demek.

## 1. Çelişki oranı — `evre` değerine göre

| değer | kayıt | ⛔ çelişen | oran |
|---|---:|---:|---:|
| `merak_deneme` | 24 | 5 | **%21** |
| `sosyal_kullanim` | 11 | 2 | **%18** |
| `nuksetme` | 47 | 6 | **%13** |
| `birakma_cabasi` | 48 | 6 | **%12** |
| `dibe_vurma` | 25 | 3 | **%12** |
| `tolerans` | 117 | 5 | **%4** |
| `inkar` | 24 | 1 | **%4** |

## 2. ⭐⭐ Yön: hangi etiket hangi değerle karışıyor

| etiket | metinde görülen | kaç kez |
|---|---|---:|
| `merak_deneme` | `tolerans` | **5** |
| `tolerans` | `birakma_cabasi` | **3** |
| `birakma_cabasi` | `tolerans` | **3** |
| `sosyal_kullanim` | `tolerans` | **2** |
| `birakma_cabasi` | `inkar` | **2** |
| `dibe_vurma` | `birakma_cabasi` | **2** |
| `tolerans` | `nuksetme` | **2** |
| `nuksetme` | `tolerans` | **2** |
| `nuksetme` | `birakma_cabasi` | **2** |
| `nuksetme` | `inkar` | **1** |
| `inkar` | `tolerans` | **1** |
| `nuksetme` | `merak_deneme` | **1** |
| `dibe_vurma` | `nuksetme` | **1** |
| `birakma_cabasi` | `nuksetme` | **1** |

⭐⭐ **Yön tek taraflı:** 28 çelişkinin **13'inde** (%46) metinde görülen değer `tolerans`, yani süren bir durum; etiket ise bir hareket adı taşıyor. ⭐ Tersi seyrek: `tolerans` ETİKETİ 5 kez çelişti ve en az hata veren iki değerden biri. ➡️⭐⭐⭐ *Etiketler hareketi anlatıyor (deneme, çaba, nüks, dip), kayıtlar ise çoğu zaman SÜREN BİR DURUMU gösteriyor. Hata rastgele değil: hareket etiketleri, durağan metinlere yapıştırılıyor.*

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔⛔ **İÇ ÖRNEKLEM** | değer-başına oranlar, ayrıştırılan verinin kendisinden hesaplandı; bağımsız bir doğrulama kümesi yok ve bu, beklenen oranları gözlenene doğru çeker |
| ⛔⛤ **Sayılar küçük** | parti başına 1-10 çelişki; bant bu yüzden geniş ve *«bandın içinde»* demek *«fark yok»* demek değil, *«bu veriyle fark gösterilemiyor»* demek |
| ⛔ **Hükümler benim** (K30) ve `GORULEN` sütunu da benim; ikinci anotatör yok |
| ⛔ **Tohum düzeyi ölçülemez** | her tohum bir kez kullanıldığı için tohum-başına oran tahmin edilemiyor; ölçülebilen en ince birim etiketin DEĞERİ |
| ⚠️ **Düzeltme yapılmadı** | ne etiketler değişti ne kayıtlar |
