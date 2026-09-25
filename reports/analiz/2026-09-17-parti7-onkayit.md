# v5-parti7 — ÜRETİMDEN ÖNCE kaydedilen tahmin

*2026-09-17 · plan `data/plan/v5-parti7.jsonl` · üretim henüz başlamadı*

⛔⛔ **Bu dosya üretimden ÖNCE yazıldı ve sonradan değiştirilmeyecek.** Gerekçe:
T115 üreticinin güvenlik eşiğinin kaydığını ölçtü. §5a″ o kaymayı durdurmak
için yazıldı. Ama bir ölçütün işe yarayıp yaramadığı, sonuç görüldükten sonra
"beklediğim buydu" denerek gösterilemez.

## Tahmin

⭐ **§5a″ yazılı ve daraltılmış olarak uygulandığında, v5-parti7'nin güvenlik
sapması sayısı 1 ile 3 arasında olacak.**

Dayanak: dört partinin eksen bileşimi birebir aynı ve gözlenen sayılar
**0 / 2 / 1 / 6**. Ortalama 2.25. Ölçüt varyansı düşürüyorsa parti7 ortalamanın
yakınına düşmeli; uçlara (0 ya da 5+) düşerse ölçüt varyansı düşürmemiş demektir.

## ⛔ Bu tahminin zayıflıkları — şimdiden yazılı

| | |
|---|---|
| ⛔ **n=4** | dört gözlemden çıkarılan bir aralık; 1–3 aralığı zaten gözlemlerin %75'ini kapsıyor ⇒ tahmin **ucuz** |
| ⛔ **Aynı üretici tahmini de yapıyor** | tahmini bilen üretici üretirken ona doğru çekilebilir; bu ölçümü kirletir ve engellenemiyor (K30) |
| ⛔ **Tohum farkı denetlenmiyor** | eksen kotası aynı ama parti7'nin tohumları başka; içlerinde kaç akut işaret olduğu üretimden önce bilinmiyor |
| ⚠️ **Tek yönlü** | aralığa düşerse ölçüt "çalıştı" denemez, yalnız "çürümedi" denir |

## Ne ölçülecek

`scripts/analiz/2026-09-17-izgara-sapma-defteri.py` çıktısındaki
`parti_basina.v5-parti7.sapma` (yalnız `guvenlik_mi` olanlar).

---

## EK — yine üretimden önce (plan incelendikten sonra, üretim başlamadan)

⚠️ Plan **6 PERSONA sınıfı kriz tohumu** çekti (`#17 #31 #33 #35 #39 #59`).
Bu, sapma sayısını yukarı çekebilecek bir karışım farkı ⇒ tahmini kirletir mi
diye ÜRETİMDEN ÖNCE bakıldı:

| parti | PERSONA tohumu | güvenlik sapması |
|---|---:|---:|
| v5-parti3 | 0 | 0 |
| v5-parti4 | **6** | 4 |
| v5-parti5 | 0 | 1 |
| v5-parti6 | 0 | **5** |
| v5-parti7 | **6** | *tahmin: 1–3* |

⭐⭐ **Persona tohumu sayısı sapma sayısını ÖNGÖRMÜYOR:** en çok persona taşıyan
parti (parti4, 6 tohum) 4 sapma verdi; hiç persona taşımayan parti (parti6)
**5** verdi. ➡️ *Karışım farkı elendi; 0↔5 aralığını açıklayan şey tohumun risk
etiketi değil.* Bu, T115'in «değişen şey üreticinin eşiği» iddiasını
güçlendiriyor ve parti7 tahminini kirletmiyor.

⛔ Yine de: persona tohumlarının mesaj içerikleri okunmadı; «etiket öngörmüyor»
demek «içerik öngörmüyor» demek değil.
