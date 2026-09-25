# Veriyi ikiye katlamak işe yaradı mı

**Betik:** `scripts/analiz/2026-09-22-veri-iki-kati.py` · **Tarih:** 2026-09-22  
**Kollar:** kapsam birebir aynı (8 kat · q+o · r8 · s20 · LR 1e-5 · aynı üç tohum · aynı bölme) — **değişen tek şey veri**  

⛔⛔ Ölçüt **koşudan önce** ilan edildi (`configs/training/d1-veri2x-k8qo-v018-t*.yaml`).

## Sonuç

| kol | kayıt | eğitim | adım | dereceli (8 tohum) | ortalama | SH |
|---|---:|---:|---:|---|---:|---:|
| z-h9 (v0.0.14) | 571 | 457 | 1368 | 8, 4, 11, 3, 6, 6, 4, 9 | **6.38** | 0.98 |
| **d1 (v0.0.18)** | 1033 | 826 | 2478 | 3, 6, 0, 4, 3, 10, 11, 4 | **5.12** | 1.32 |

**Fark: -1.25** · ilan edilen eşik **±2.4** · tohum yayılımından gelen hata payı ±3.28

⛔⛔⛔ **OKUNAMAZ — ve bu kez İKİ ÖLÇÜT DE AYNI ŞEYİ SÖYLÜYOR.**

|fark| = 1.25 hem ilan edilen eşiğin (±2.4) hem sekiz tohumun kendi yayılımının (±3.28) altında.

⭐⭐⭐ **ASIL BULGU DARALMADIR.** Üç tohumla fark **-4.67** görünüyordu; sekiz tohumla **-1.25**'e düştü ⇒ görünen etkinin **%73**'i tohum gürültüsüymüş. ➡️ *Az tohumla ölçülen bir fark, farkın büyüklüğünü değil örneklemin küçüklüğünü ölçüyor olabilir.*

⭐⭐ **Güç hesabı tuttu:** koşudan önce n=8 için ±3,27 öngörülmüştü, ölçülen **±3.28**.

⛔⛔ **ÖN KAYITLI SONUÇ UYGULANIR:** *«|fark| ≤ 2·SE çıkarsa sıradaki iş tohum eklemek değil ÖLÇÜTÜ DEĞİŞTİRMEK»*. Sayı bunu doğruluyor: bugünkü 1.25 puanlık farkı ayırt etmek için kol başına **~56 tohum** (toplam ~112 koşu, ~30 saat eğitim) gerekirdi. ⇒ Bu ölçüt bu karşılaştırmayı **makul maliyetle taşıyamıyor**.

⭐ Ve bu bir başarısızlık değil bir **sonuçtur**: korpusu 571'den 1033'e çıkarmak, bu ölçütte ölçülebilir bir kazanç **vermedi** ⇒ sıradaki iş veri ÜRETMEK değil, ölçütü ve veri KALİTESİNİ düzeltmek.

## Yan ölçüler

| kol | safety otomatik | forget otomatik |
|---|---:|---:|
| z-h9 (v0.0.14) | 9.0/20 | 27.6/30 |
| **d1 (v0.0.18)** | 8.8/20 | 26.8/30 |

⚠️ Otomatik geçen sayıları **kapı sayımıdır, kalite değil** (K57). Judge tipindeki iddialar bu koşucuda *«denetlenemedi»* kalır ve geçti SAYILMAZ.

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔⛔ **Epoch sabit, ADIM değil** | 1368 → 2478. İkisi birden sabitlenemezdi ⇒ bu kol *«iki katı veri, üç epoch»*u ölçer, *«aynı adımla iki katı veri»*yi değil |
| ⛔⛔ **v0.0.18, v0.0.14'ün ÜST KÜMESİ DEĞİL** | uydurma kapısı (`grounding`=2) eski kayıtlardan da 7 tanesini eledi ⇒ fark yalnız *«daha çok veri»* değil, *«daha çok + biraz farklı süzülmüş»* |
| ⛔ **Tek ölçüt ailesi** | dereceli puan `safety_crisis`'in kriz kutuplu 15 ögesinde ölçülüyor; başka eksenlerde ne olduğu bu sayıdan çıkarılamaz (K137) |
| ⛔ **Judge karışımı kolları etkiliyor olabilir** | `v0.0.18`'in 921 kaydı Claude-subagent, 150'si Gemini puanlı; `v0.0.14` başka bir karışım taşıyor ⇒ veri farkı yalnız BOYUT farkı değil |
| ⛔⛔⛔ **ÖN KAYITLI EŞİK YANLIŞ SEÇİLMİŞTİ** | ±2,4 T186'nın **başka bir bağlamda** ölçtüğü gürültü tabanıydı; bu ölçütün üç tohumdaki gerçek yayılımı çok daha geniş. ⇒ Ön kayıt disiplini doğru, **eşiğin kendisi yanlıştı** ve bunu ancak koşu gösterebilirdi |
| ⛔⛔ **Bu koşu bir SONUÇ değil bir GÜÇ ANALİZİDİR** | üç tohumla ayırt edilebilir en küçük fark ≈ ±3.3 puan; *«iki katı veri»*nin etkisi bundan küçükse bu tasarımla **ölçülemez**. Daha çok tohum ya da daha kararlı bir ölçüt gerekiyor |
| ⚠️ **Üç tohum azdır** | SH üç gözlemden; K213 tek koşunun bir çekiliş olduğunu ölçtü, üç koşu onu azaltır, yok etmez |
