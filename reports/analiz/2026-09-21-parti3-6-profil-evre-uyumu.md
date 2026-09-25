# `v6-parti3…6`: `profil` ve `evre` etiketleri kaydı tarif ediyor mu?

**Betik:** `scripts/analiz/2026-09-21-parti3-6-profil-evre-uyumu.py` · **Tarih:** 2026-09-21  
**Girdi:** `v6-parti3` `a82b8d16` · `v6-parti4` `2bc2e7ec` · `v6-parti5` `12c263e4` · `v6-parti6` `23186319` · **237** kayıt  
**Ölçek:** T220'nin ölçeği, aynen — `U` uyumlu · `Ç` çelişiyor · `S` sessiz; 237×2 = **474** hüküm, hepsi elle (K30)

⛔⛔ T220 parti1'i ölçmüş ve bir **tahmin** bırakmıştı: `profil`'in sessizliği rejimden BAĞIMSIZ, `evre`'nin çelişkisi parti1'e ÖZGÜ olacak. Bu rapor o tahmini sınıyor.

## 0. ⭐⭐⭐ Tahmin sınandı

| eksen | parti1 | parti3-6 | tahmin | sonuç |
|---|---|---|---|---|
| `profil` sessiz | %73 | **%53** | rejimden **bağımsız** | ◐ **YARI** — düştü ama iki rejimde de çoğunluk |
| `evre` çelişen | %8 | **%10** | parti1'e **özgü** | ⛔ **ÇÜRÜDÜ** — fark neredeyse yok |

⛔⛔⛔ **`evre` TAHMİNİ ÇÜRÜDÜ — VE BUNU GÖRMEK İKİ DÜZELTME GEREKTİRDİ.** İlk karşılaştırma %22 ↔ %12 diyordu ve farkı rejime yoruyordu. (1) `Ç`/`S` sınırı iki raporda farklı uygulanmıştı; ilan edilince parti1 %14'e indi (T222). (2) Sonra parti1'in künyesinin bozuk olduğu ortaya çıktı (T224): ölçüm **yanlış tohumlara** karşı yapılmıştı. Künye onarılıp doğru tohumlarla yeniden okununca karşılaştırma **%8 ↔ %10** oldu — parti1 artık **daha iyi**. ⇒ `evre` çelişkisi parti1'e özgü değil; her partide var ve rejimle hiç ilgisi yok. ➡️⭐⭐⭐ *Bir karşılaştırmanın iki yanı da aynı ölçekle VE aynı veriyle kurulmalıdır; ben ikisini de ayrı ayrı kaçırdım ve her seferinde farkı bir OLGUYA yordum.*

⭐ **`profil` tahmini ise kısmen tuttu:** sessizlik %73 → %53. Rejim sayıyor ama sessizlik iki rejimde de çoğunluk.

⭐ **Asıl bulgu `profil`'de ve tahminden bağımsız:** kayıtların %53'inde — metin tohumdan gelirken bile — kişinin mesleki profili hakkında hiçbir şey söylenmiyor. Çünkü tohumun kendi metni de çoğu zaman söylemiyor: kısa bir konuşmada meslek geçmiyor. ⇒ `profil` ekseni korpusun bir özelliğini değil, tohum dosyasının bir alanını ölçüyor ve bu **bütün partiler** için geçerli.

## 1. Parti parti

| parti | kayıt | `profil` U/S/Ç | `evre` U/S/Ç | `profil` doğrulanabilir | `evre` çelişen |
|---|---:|---|---|---:|---:|
| `v6-parti3` | 60 | 30/30/0 | 42/11/7 | %50 | **%12** |
| `v6-parti4` | 59 | 20/39/0 | 41/17/1 | %34 | **%2** |
| `v6-parti5` | 60 | 28/30/2 | 46/9/5 | %50 | **%8** |
| `v6-parti6` | 58 | 32/26/0 | 32/16/10 | %55 | **%17** |
| **parti1** *(T220)* | 59 | 15/43/1 | 28/26/5 | %27 | **%8** |

## 2. ⛔ Bunun kapsama ölçümüne anlamı

Kapsama envanteri `profil` eksenini de hedefliyor. Ölçülen şu: **296 v6 kaydının 168'inde** (%57) metin, kişinin mesleki profili hakkında hiçbir şey söylemiyor. ⇒ T211'in beş partide kapanmayan `profil=mavi_yakali` açığı, korpusta **görünmeyen** bir eksende ölçülüyordu; o açığı kapatmak korpusun içeriğini değil tohum seçimini değiştirir.

## 3. ⛔ Çelişen etiketler — gerekçeleriyle

⭐⭐ **Gerekçeleri yazmak sayıyı değiştirdi.** Bu raporun ilk hâli 28 çelişki saymıştı ve şerhinde *«gerekçeler tek tek yazılmadı, denetlenebilirlik T220'ninkinden düşük»* yazıyordu. Yazılınca **5'i gerekçelendirilemedi ve geri alındı**; sayı 23'e indi. ➡️⭐⭐⭐ *Yazılmamış bir hüküm dayanıksız bir hükümdür: gerekçe yazmak bir biçim işi değil, hükmün kendisini sınayan adımdır — ve burada hükümlerin **%18**'i sınavı geçemedi.*

| # | gerekçe |
|---|---|
| `v6-parti3#12` | `inkar`; metin *«çok mu sık alıyorum acaba»* diye SORUYOR — inkârın tersi |
| `v6-parti3#22` | `nuksetme`; metinde kırılan bir ayıklık dönemi yok, iki günlük yeni bir kullanım var |
| `v6-parti3#27` | `dibe_vurma`; metin ilk grup katılımını ve markete girip içmeden çıkmayı anlatıyor — bu bir çaba |
| `v6-parti3#33` | `tolerans`; metin her ay temiz çıkan testleri anlatıyor, artan kullanımı değil |
| `v6-parti3#45` | `sosyal_kullanim`; metin *«tek başıma uğruyorum»* diyor ve sıklığın arttığını söylüyor |
| `v6-parti3#46` | `birakma_cabasi`; metin dozu KENDİ artırdığını söylüyor |
| `v6-parti3#56` | `tolerans`; metin silme–yeniden indirme döngüsünü anlatıyor, artan kullanımı değil |
| `v6-parti4#2` | `tolerans`; metin içmediği bir akşamı ve *«aklımdan bile geçmedi»*yi anlatıyor |
| `v6-parti5#16` | `merak_deneme`; metinde grubun danıştığı yerleşik bir kimlik var, deneme yok |
| `v6-parti5#18` | `birakma_cabasi`; metin iki hafta önce BAŞLAYAN bir eklemeyi ve *«kendime dur diyemiyorum»*u anlatıyor |
| `v6-parti5#28` | `merak_deneme`; metinde oturmuş bir *«sistem»* ve ücretli bir grup var |
| `v6-parti5#33` | `birakma_cabasi`; metin yazılandan fazlasını aldığını söylüyor |
| `v6-parti5#53` | `dibe_vurma`; metin süren (ve denetimsiz) bir bırakma girişimini ve *«başaracağım galiba»*yı anlatıyor |
| `v6-parti6#19` | `merak_deneme`; metinde üç haftalık düzenli oyun ve kaybı kapatma planı var |
| `v6-parti6#21` | `nuksetme`; metin *«dönemde böyle bir şey yaşamamıştım»* diyor — kırılan bir ayıklık değil, yeni bir tırmanış |
| `v6-parti6#30` | `dibe_vurma`; metin azalmayı ve düzelen aile ilişkisini anlatıyor, kelimeyi de kendisi veriyor: *«nüks»* |
| `v6-parti6#35` | `tolerans`; metin üç günlük aradan sonraki kaymayı anlatıyor |
| `v6-parti6#39` | `nuksetme`; metin yarından itibaren bırakma KARARINI anlatıyor |
| `v6-parti6#41` | `merak_deneme`; metin aylık aidatlı bir aboneliği *«yatırım»* diye kuruyor |
| `v6-parti6#43` | `merak_deneme`; metin her sınav döneminde tekrarlanan bir kullanımı anlatıyor |
| `v6-parti6#56` | `nuksetme`; metin azaltılmış ama SÜREN bir kullanımı anlatıyor, geri dönüşü değil |
| `v6-parti6#57` | `birakma_cabasi`; metin *«üç aydır geri döndüm»* diyor |
| `v6-parti6#60` | `nuksetme`; metin hâlâ ayık olduğunu söylüyor — bu bir nüks değil, bir istek gecesi |

### ⭐ Geri alınan hükümler

| # | düzeltme |
|---|---|
| `v6-parti3#43` | Ç → **U**. Metin *«kendime kapı aralamak istemiştim, ama içimden gelmedi»* diyor: gerekçeyi arayıp KULLANMAMIŞ. `birakma_cabasi` bunu tarif ediyor. Kısaltılmış dökümde son cümleyi görmemiştim. |
| `v6-parti4#9` | Ç → **U**. Metinde *«hafta içi sekizleri görüyorum zaten, üç bira hiçbir şey»* var — bu doğrudan bir TOLERANS ifadesi. Cumartesi girişimine takılıp etiketin karşılığını atlamışım. |
| `v6-parti4#47` | Ç → **S**. Metinde bırakma girişimi YOK ama girişimle ÇELİŞEN bir şey de yok; yalnızca sessiz. Yokluğu çelişki saymışım. |
| `v6-parti5#54` | Ç → **S**. Etiket ilacın dozuyla ilgili; metin şarabı bırakmakla ilgili. Farklı şeylerden söz ediyorlar, çelişmiyorlar. |
| `v6-parti6#40` | Ç → **S**. Metinde kullanım hiç yok — kutuya bakmak var. Bir evreyi çürütmek için önce bir evre görünmeli. |

## 4. Satır satır hüküm

**`v6-parti3`** — sıra: `profil``evre`

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 | 40 | 41 | 42 | 43 | 44 | 45 | 46 | 47 | 48 | 49 | 50 | 51 | 52 | 53 | 54 | 55 | 56 | 57 | 58 | 59 | 60 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| UU | UU | US | UU | UU | SU | SS | SU | UU | SS | SU | UÇ | SU | US | SU | UU | SS | UU | SU | UU | SU | UÇ | UU | SS | UU | SU | SÇ | SU | SU | SU | SS | UU | SÇ | UU | SU | SU | UU | UU | UU | UU | UU | UU | SU | SS | UÇ | UÇ | SU | SS | UU | UU | US | UU | SU | SU | SS | SÇ | SU | UU | SU | UU |

**`v6-parti4`** — sıra: `profil``evre`

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 | 40 | 41 | 42 | 43 | 44 | 45 | 46 | 47 | 48 | 49 | 50 | 51 | 52 | 53 | 54 | 55 | 56 | 57 | 58 | 59 | 60 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SS | SÇ | SU | SU | SU | SS | SU | SU | SU | SU | UU | US | UU | US | SU | UU | UU | UU | SU | UU | UU | SS | SU | SU | SS | UU | SU | SU | UU | SU | SU | UU | SU | SS | SS | UU | US | SS | SS | SU | SS | SU | SS | UU | SU | US | SU | SU | UU | SS | SU | UU | US | SU | SU | UU | SS | SU | SU |

**`v6-parti5`** — sıra: `profil``evre`

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 | 40 | 41 | 42 | 43 | 44 | 45 | 46 | 47 | 48 | 49 | 50 | 51 | 52 | 53 | 54 | 55 | 56 | 57 | 58 | 59 | 60 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| UU | SU | SU | SU | SU | SU | SU | SU | SS | UU | UU | SU | US | UU | UU | SÇ | SU | UÇ | SU | SU | SU | SS | UU | SU | SU | UU | UU | UÇ | UU | SU | UU | SU | UÇ | UU | ÇS | UU | SU | US | SU | SU | UU | UU | UU | SU | ÇS | UU | SS | SU | UU | US | UU | SU | SÇ | SS | UU | UU | SU | SU | UU | UU |

**`v6-parti6`** — sıra: `profil``evre`

| 1 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 | 31 | 32 | 33 | 34 | 35 | 37 | 38 | 39 | 40 | 41 | 42 | 43 | 44 | 45 | 46 | 47 | 48 | 49 | 50 | 51 | 52 | 53 | 54 | 55 | 56 | 57 | 58 | 59 | 60 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| UU | UU | SU | SS | UU | UU | UU | US | SU | UU | UU | UU | SU | SS | US | SU | SS | SÇ | SU | UÇ | SU | SU | UU | US | US | SU | SU | SS | UÇ | SU | UU | US | UU | SÇ | SS | UU | SÇ | US | SÇ | UU | UÇ | SS | SU | UU | UU | UU | SS | UU | US | UU | SU | US | US | SÇ | UÇ | UU | SU | SÇ |

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔⛔ **Hüküm BENİM okumam** (K30) | ve bu partilerin kayıtlarını da ben yazdım ⇒ kendi metnimi kendi etiketime karşı okuyorum; ikinci anotatör yok |
| ⭐ **Gerekçeler YAZILDI ve 5 hüküm geri alındı** | bu şerh ilk hâlde bir eksiklik olarak duruyordu; kapatıldı. ⛔ Ama geri alınanların hepsini de ben buldum: bir hükmü sınayan yine hükmü veren kişi (K30) |
| ⛔ **Diğer yedi eksen ölçülmedi** | yalnız `profil` ve `evre`; `risk_seviyesi`, `siddet_seviyesi`, `motivasyon_evresi` yine ölçülmedi (derece okumak eşiği benim koymam olurdu, `gd-024`) |
| ⛔⛔ **Düzeltme yapılmadı** | ne etiketler değişti ne kayıtlar |
| ⚠️ **`diger` profili çürütülemez** | metin onunla çelişemez; bu değerdeki kayıtlar yapısal olarak `S` alıyor |
