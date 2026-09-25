# T211'in hedefleri — onarım sonrası zeminde yeniden türetildi

**Betik:** `scripts/analiz/2026-09-21-t211-hedefler-onarim-sonrasi.py` · **Tarih:** 2026-09-21  
**Kural:** T211'in ufuk kuralı, parti6 planlayıcısının `paylar()` fonksiyonundan ÇAĞRILDI (yeniden tanımlanmadı) · **N₀ = 926** · n = 60

⛔⛔ T224: `v6-parti1`'in künyesi bozuktu ve kapsama envanteri *«kullanılmış tohum»* üzerinden ölçtüğü için parti1'in 59 kaydı yanlış tohumlarla sayılıyordu. Künye onarıldı ⇒ kuralın girdisi değişti.

## 0. ⭐⭐⭐ Onarımın hedeflemeye etkisi KÜÇÜK

| | onarım öncesi | onarım sonrası |
|---|---:|---:|
| kullanılmış (benzersiz) tohum | 985 | 972 |
| eşiği aşan marjinal sınıf | 6 | 6 |

⭐ Bozulma 59 kaydın künyesini değiştirmişti ama envanter ~970 tohum üzerinden ölçüyor: her eksenin payı **bir puanın çok altında** oynadı (`evre=tolerans` −3,30 → −3,60 · `profil=mavi_yakali` −4,10 → −4,20) ve eşiği aşan birimlerin **kümesi hiç değişmedi**. ➡️⭐⭐ *Bir veri bozulması, ölçümün paydası yeterince büyükse hedeflemeye yansımayabilir; bu, bozulmanın önemsiz olduğunu değil, bu ölçümün ona duyarsız olduğunu gösterir.*

## 0b. ⛔⛔⛔ ASIL SONUÇ: KURAL ARTIK YALNIZ İKİ EKSENDEN KONUŞUYOR — VE İKİSİ DE BU OTURUMDA SORUNLU ÇIKTI

⭐ Altı parti sonra ufuk kuralı **sıfır hedef, altı tavan** üretiyor (her iki zeminde ve her iki K'de). Yani *«eksik taşınan»* diye bir birim kalmadı; kural yalnızca *«fazla taşıma»* diyor.

⛔⛔ Altı tavanın **dördü `profil=mavi_yakali`** içeriyor (marjinal + üç hücre), kalan ikisi **`evre=tolerans`**. Başka hiçbir eksen eşiği aşmıyor.

⛔⛔⛔ **Bu iki eksen de bu oturumda ölçüm sorunu çıkardı:** T220/T221 `profil`in v6 kayıtlarının **yarısından fazlasında metinde hiç görünmediğini** ölçtü (parti1 %27, parti3-6 %53 doğrulanabilir); T223 `evre` etiketlerinin **%10'unun metinle çeliştiğini** ve hatanın tek taraflı olduğunu ölçtü. ➡️⭐⭐⭐ *Bir hedefleme kuralı, korpus yeterince büyüdükçe yalnız en zor kapanan birimlerde konuşmaya başlar; ve bir eksenin zor kapanması ile o eksenin KAYITTA GÖRÜNMEMESİ aynı şeyin iki yüzü olabilir. `profil=mavi_yakali` altı partidir kapanmıyor çünkü belki de kapatılacak bir şey yok — ölçülen şey metinde değil, tohum dosyasında.*

⛔ Bu bir **tasarım kararını** zorunlu kılıyor ve bu betik onu vermiyor: (a) `profil` ekseni hedeflemeden çıkarılsın mı, (b) tohum meta'sı yerine kayıttan okunabilir bir eksen tanımlansın mı, (c) kural olduğu gibi mi kalsın. Üçü de bir sonraki partinin planlayıcısında gerekçesiyle yazılmalı.

## 1. ⭐ Yeni hedefler (onarım sonrası zemin)

| birim | tür | fark | **K=2 payı** | **K=3 payı** |
|---|---|---:|---:|---:|
| `motivasyon_evresi=dusunme&profil=mavi_yakali` | hücre · tavan | -4.90 | **0** | **0** |
| `profil=mavi_yakali` | marjinal · tavan | -4.20 | **0** | **0** |
| `evre=tolerans&profil=mavi_yakali` | hücre · tavan | -3.87 | **0** | **0** |
| `evre=tolerans` | marjinal · tavan | -3.60 | **11** | **17** |
| `evre=tolerans&siddet_seviyesi=orta` | hücre · tavan | -3.60 | **6** | **12** |
| `risk_seviyesi=yuksek&profil=mavi_yakali` | hücre · tavan | -3.59 | **0** | **0** |

⛔ **K seçimi artık belirleyici.** N₀=926; K=2 korpusu 1046'ya, K=3 1106'ya taşır. Hedeflenen büyüklük ~1.000-1.100 olduğu için **ikisi de savunulabilir** ve payları yukarıdaki tabloda yan yana duruyor. Bu betik bir seçim YAPMIYOR; seçim bir sonraki partinin planlayıcısında ve gerekçesiyle yazılmalı.

## 2. İki zemin, aynı kural (K=3)

| birim | öncesi payı | sonrası payı |
|---|---:|---:|
| `evre=tolerans` | 18 | 17 ⛔ |
| `evre=tolerans&profil=mavi_yakali` | 0 | 0 |
| `evre=tolerans&siddet_seviyesi=orta` | 13 | 12 ⛔ |
| `motivasyon_evresi=dusunme&profil=mavi_yakali` | 0 | 0 |
| `profil=mavi_yakali` | 0 | 0 |
| `risk_seviyesi=yuksek&profil=mavi_yakali` | 0 | 0 |

## ⛔ Bu türetmenin söylemedikleri

| | |
|---|---|
| ⛔⛔ **Hedef ≠ kalite** | T211'in kendi şerhi: payı havuza yaklaştırmak o birimde iyi kayıt üretileceğini göstermez |
| ⛔⛤ **`profil` ekseni korpusta GÖRÜNMÜYOR** (T220/T221) | v6 kayıtlarının yarısından fazlasında metin mesleki profil hakkında hiçbir şey söylemiyor. `profil=mavi_yakali` tavanı bu yüzden **görünmeyen bir eksende** işliyor ve bu tabloda hâlâ en büyük birim. Kaldırmak ya da bırakmak bir tasarım kararı; verilmedi |
| ⛔ **37 çift kayıt sayıma dahil** | aynı tohumdan iki kayıt üretilmiş durumda; envanter tohumu bir kez sayıyor, korpus iki kayıt taşıyor |
| ⛔ **K seçilmedi** | iki değerle raporlandı; seçim planlayıcıya bırakıldı |
| ⚠️ **Fazla temsilin KUSUR olduğu hâlâ gösterilmedi** | envanterin varsayımı *«set havuzu yansıtmalı»* ve havuz bir tasarım ürünü (T211'den beri açık) |
