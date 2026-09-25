# v6-parti7 — üretim öncesi kriz taraması

**Betik:** `scripts/analiz/2026-09-21-v6-parti7-on-tarama.py` · **Tarih:** 2026-09-21  
**Girdi:** `data/plan/v6-parti7.jsonl` · **60** satır

⛔⛔⛔ **T213: parti5'te `md.` ölçütlerini ateşleyen dört satırın dördü de işaretsizdi.** İşaretleme ölçütü tohumun kendi `risk_seviyesi` etiketiydi, metnin okunması değil. ⇒ Bu partide okuma kümesi kuyruğa değil **partiye** eşit: 60 satırın 60'ının hükmü yazılı ve betik, hükmü olmayan tek bir satır kalırsa raporu yazmıyor.

| | |
|---|---:|
| plan satırı | **60** |
| ⭐ **hükmü yazılı** | **60 / 60** |
| ⛔ **üretilmeyecek** | **3** [2, 48, 57] |
| ⚠️ üretim notu olan | 34 |
| ⭐ okundu, not gerekmiyor | 23 |
| süzgeç işareti taşıyan | 35 |
| — içerik/beyan süzgeci ateşleyen | 2 |

## ⭐⭐ İşaret ne kadar öngördü — T213'ün ölçüsü

| | |
|---|---:|
| hüküm gerektiren satır (eleme + not) | **37** |
| — bunlardan süzgecin işaretlediği | **20** (%54) |
| ⛔ — **süzgecin KAÇIRDIĞI** | **17** [4, 5, 8, 17, 21, 29, 33, 40, 43, 44, 46, 49, 53, 54, 55, 57, 60] |

⛔⛔⛔ **VE İLK KEZ BİR ELEME SATIRINI KAÇIRDI: `#57`.** parti6'da süzgeç eleme sınıfını 2/2 yakalamıştı ve T213 *«sözlük ‹üretilemez›i tanıyor, ‹dikkatle üretilmeli›yi tanımıyor»* diye yazılmıştı. `#57` o cümleyi de çürütüyor: reçetesiz bir yatıştırıcıyı alkolle birlikte almayı soran, kriz sözlüğü taşımayan, `risk_seviyesi` işareti olmayan sıradan bir cümle. ➡️⭐⭐⭐ *Bir süzgecin en güvendiği sınıfta bile tavanı vardır; eleme sınıfını yakalıyor olması, yakalamaya DEVAM edeceği anlamına gelmez.*

➡️ Süzgeç, hüküm gerektiren satırların %54'ini gördü. Kalanı yalnız okuma yakaladı. ⛔ Bu sayı süzgecin kusuru değil, **kapsamının ölçüsü**: süzgeç bir sıralama aracıdır, bir güvence değil.

## Satır satır hüküm

| # | tür / senaryo | süzgeç işareti | hüküm |
|---:|---|---|---|
| 1 | `kumar` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 2 | `receteli_ilac` / `belirsiz` | TG:acil servis,doz aşımı + risk:yuksek | ⛔⛔ **ÜRETİLMEYECEK** |
| 3 | `alkol` / `ambivalans` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 4 | `tutun` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 5 | `receteli_ilac` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 6 | `kumar` / `ambivalans` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 7 | `tutun` / `belirsiz` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 8 | `receteli_ilac` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 9 | `dijital` / `belirsiz` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 10 | `kumar` / `ambivalans` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 11 | `alkol` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 12 | `kumar` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 13 | `kumar` / `nazikce_karsi_cikma` | — | ⭐ okundu, not gerekmiyor |
| 14 | `alkol` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 15 | `kumar` / `ambivalans` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 16 | `alkol` / `belirsiz` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 17 | `receteli_ilac` / `nazikce_karsi_cikma` | — | ⚠️ okundu, **üretim notu var** |
| 18 | `dijital` / `belirsiz` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 19 | `kumar` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 20 | `alkol` / `nazikce_karsi_cikma` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 21 | `tutun` / `belirsiz` | — | ⚠️ okundu, **üretim notu var** |
| 22 | `tutun` / `nazikce_karsi_cikma` | — | ⭐ okundu, not gerekmiyor |
| 23 | `kumar` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 24 | `kumar` / `ambivalans` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 25 | `alkol` / `ambivalans` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 26 | `alkol` / `nazikce_karsi_cikma` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 27 | `receteli_ilac` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 28 | `alkol` / `nazikce_karsi_cikma` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 29 | `receteli_ilac` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 30 | `alkol` / `nazikce_karsi_cikma` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 31 | `tutun` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 32 | `receteli_ilac` / `discord` | TG:taburcu + risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 33 | `alkol` / `rol_siniri` | — | ⚠️ okundu, **üretim notu var** |
| 34 | `tutun` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 35 | `kumar` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 36 | `alkol` / `belirsiz` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 37 | `dijital` / `belirsiz` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 38 | `dijital` / `belirsiz` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 39 | `dijital` / `belirsiz` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 40 | `kumar` / `nazikce_karsi_cikma` | — | ⚠️ okundu, **üretim notu var** |
| 41 | `kumar` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 42 | `alkol` / `kriz` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 43 | `alkol` / `belirsiz` | — | ⚠️ okundu, **üretim notu var** |
| 44 | `tutun` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 45 | `receteli_ilac` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 46 | `receteli_ilac` / `nazikce_karsi_cikma` | — | ⚠️ okundu, **üretim notu var** |
| 47 | `receteli_ilac` / `nazikce_karsi_cikma` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 48 | `alkol` / `belirsiz` | risk:yuksek | ⛔⛔ **ÜRETİLMEYECEK** |
| 49 | `receteli_ilac` / `nazikce_karsi_cikma` | — | ⚠️ okundu, **üretim notu var** |
| 50 | `receteli_ilac` / `discord` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 51 | `tutun` / `belirsiz` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 52 | `alkol` / `belirsiz` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 53 | `tutun` / `belirsiz` | — | ⚠️ okundu, **üretim notu var** |
| 54 | `tutun` / `belirsiz` | — | ⚠️ okundu, **üretim notu var** |
| 55 | `tutun` / `belirsiz` | — | ⚠️ okundu, **üretim notu var** |
| 56 | `kumar` / `ambivalans` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 57 | `receteli_ilac` / `rol_siniri` | — | ⛔⛔ **ÜRETİLMEYECEK** |
| 58 | `kumar` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 59 | `kumar` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 60 | `receteli_ilac` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |

## ⛔⛔ Üretilmeyecek satırlar — gerekçeleriyle

**`#2`** — ⛔⛔⛔ **NEREDEYSE ÖLÜMLE BİTEN BİR OLAYIN ERTESİ GÜNÜ.** *«Bir kadeh şaraptan sonra hapı içmişim sanırım. Neredeyse ölüyormuşum diyor doktor.»* Üstüne *«ben bunu istemedim»* — niyet sorusunu kullanıcının kendisi açıyor ve cevabı metinde yok. ⛔ Bu bir kriz SONRASI kayıttır ve nasıl karşılanacağı klinik/etik bir karardır (`gd-023` ile aynı sınıf). ⇒ Uzman + etik kurul (`gd-028`).

**`#48`** — ⛔⛔⛔ **EDİLGEN BİR ÖLÜM İSTEĞİ, TEKRARLAYAN.** *«Aklıma SÜREKLİ ‹keşke karşıdan biri çıksaydı da bu iş bitseydi› diye geliyor.»* Kaza, ehliyet, evden çıkarılma ve çocukları görememe üst üste. ⛔ Bu cümle `gd-021`/`gd-025`'te elenen sınıfın daha açık hâli: orada hayatın değerine dair bir cümle vardı, burada bitmesini isteyen bir cümle var. ⇒ Uzman + etik kurul (`gd-029`).

**`#57`** — ⛔⛔⛔ **BENZODİAZEPİN + ALKOLÜ BİRLİKTE ALMAYI SORUYOR, BU AKŞAM İÇİN.** *«Arkadaş bana yarım hap verdi, biraz da içeceğim orada. İkisini birlikte alınca daha rahat geçer mi?»* ⛔ Reçetesiz bir yatıştırıcı + alkol birleşimi ve tarihi belli. Reddetmek tek başına yetmiyor: *«söyleyemem»* demek, öngörülebilir ve bu geceye ait bir riski karşılıksız bırakır; bir şey söylemek ise klinik tavsiyedir. `#2` ile aynı biçim — cevap veremediğim ama sessizliğin de bedeli olan soru. ⇒ Uzman + etik kurul (`gd-030`).

## ⚠️ Üretim notları — eleme değil, talimat

**`#4`** — ⚠️ *«Abim KOAH oldu… bana bir şey olmaz»*. ⛔ KOAH riski ne doğrulanacak ne çürütülecek; abisiyle kıyas da bir kanıt gibi ele alınmayacak. Marka adı genelleştirilecek.

**`#5`** — ⛔ Terapi + doz azaltmayı aynı anda yürütmenin *«çok mu»* olduğu bir tedavi sorusu; cevaplanmayacak. Eşinin *«fazla yüklenme»*si tartışılmayacak.

**`#7`** — ⚠️ Marka adı genelleştirilecek. *«Ayıp gibi geliyor»* utancı büyütülmeyecek; çocukların uzakta olması bir kaldıraca çevrilmeyecek.

**`#8`** — ⚠️ Hekim azaltmayı YÖNETİYOR ⇒ md.2 ateşlemiyor. İlaç adı genelleştirilecek. *«Eski karanlık»* korkusu yorumlanmayacak.

**`#16`** — ⛔⛔ md.1 + md.2 — üç gündür içmiyor; gece uykusuzluk, **el titremesi**, gece terlemesi var ve *«doktora bile söylemedim»*. Belirtiler ADLANDIRILMAYACAK (yoksunluk demek teşhis olur); randevu beklemeyen bir yer söylenecek. *«Kesince geçer sanıyordum»* çürütülmeyecek.

**`#17`** — ⛔ md.2 — komşunun *«bir gün alıp bir gün atlama»* yöntemini kopyalama isteği. Onaylanmayacak, çürütülmeyecek; yöntem hiç konuşulmayacak.

**`#19`** — ⚠️ Kayıt parası bahse yatırılmış ve eşin haberi yok. ⛔ Ne söyleyeceği kurulmayacak, borca çözüm üretilmeyecek.

**`#21`** — ⚠️ Ergen, ortak paket. md.4 ateşlemiyor: ilk kullanım ve bedensel bildirim yok. Harçlık aritmetiği bir kaldıraç yapılmayacak.

**`#23`** — ⚠️ Randevu kaçırılmış, anneye yalan söylenmiş, sponsor sessiz. ⛔ Kurum adı genelleştirilecek; cevaba bir kişi daha eklenmeyecek (parti5 `#37`).

**`#26`** — ⛔⛔ md.3 + md.2 — forumdan bulunmuş bir **azaltma takvimi** için onay isteniyor (*«siz öyle başlatalım der misiniz»*). Onaylanmayacak, yüzde yazılmayacak, ilaç adı geçmeyecek. Psikiyatri randevusu gelecek hafta.

**`#27`** — ⛔ md.2 — dozu kendi artırmış (*«e vücut alışıyor herhalde»*) ve *«bağımlı değilim»* diyor. Doz konuşulmayacak, etiket tartışılmayacak.

**`#29`** — ⭐ Hekim bilgilendirilmiş ve takip ediyor ⇒ md.1 ATEŞLEMİYOR. Baş dönmesinin sebebi (yaş mı ilaç mı) söylenmeyecek; torununa bakarken düşme korkusu bir uyarıya çevrilmeyecek.

**`#30`** — ⚠️ Denetimli serbestlik + şirket galası. ⛔ Mahkeme süreci hakkında tahmin yürütülmeyecek; galaya gidip gitmemesine karar verilmeyecek.

**`#32`** — ⚠️ Yakını yatmış; soru taburculuk sonrası için *«kime danışayım»*. ⛔ Kurum adı genelleştirilecek; annesinin ne yapacağı tahmin edilmeyecek.

**`#33`** — ⚠️ Eşin *«sen ne ararsın orada»*sı. ⛔ Eşin tutumu yargılanmayacak, onunla nasıl baş edileceğine dair taktik verilmeyecek.

**`#35`** — ⛔ Elli bin borç, KYK kesilmiş. Borca çözüm ÜRETİLMEYECEK; aileye söyleme kararı verilmeyecek ve söylenecek cümle kurulmayacak.

**`#40`** — ⚠️ Ergen, *«herkes telefonla çalışıyor, bilim insanları da diyor»*. md.4 ateşlemiyor. ⛔ Bilimsel iddia ne doğrulanacak ne çürütülecek.

**`#41`** — ⚠️ Otelde, eşi göndermiş, grup sohbeti açık. ⛔ Örgüt adı genelleştirilecek; gruba ne yazacağı kurulmayacak.

**`#42`** — ⛔⛔ Tohumun kendi etiketi `kriz`. Sekiz ay ayık, eşin *«çocukları alıp giderim»* tehdidi, mutfakta iki bira. ⛔ *«İç/içme»* denmeyecek (sonucunu taşımayacağım emir) ve eşin tehdidi bir kaldıraca çevrilmeyecek. Boş da bırakılmayacak.

**`#43`** — ⚠️⚠️ İki kadeh sonrası çocuğu kucağına almış, eş *«kokuyorsun»* demiş. ⛔ Çocuğu kucağına alacak durumda olup olmadığına HÜKÜM VERİLMEYECEK (klinik/güvenlik kararı) ama eşin cümlesi de yok sayılmayacak. ⚠️ Bebeğe maruziyet boyutu yine dört ölçütün dışında (`gd-022`).

**`#44`** — ⚠️ *«Ya sigara ya ben»*. ⛔ Bırakma kararı verilmeyecek; *«bin kere düşündüm, bir kere başaramadım»* bir başarısızlık listesi yapılmayacak.

**`#45`** — ⚠️ İlaç adı genelleştirilecek. Eşine söyleme kararı ve söylenecek cümle kurulmayacak.

**`#46`** — ⛔ md.3 — *«ilaç azaldıkça ağrılar arttı, sen ne dersin»* doğrudan bir nedensellik sorusu. Cevaplanmayacak; hekime yönlendirilecek.

**`#47`** — ⚠️ Bedensel bildirim var (*«ayaklarım bana ait değil»*) ama kullanıcı ilaçla ilgisini kendisi reddediyor. ⛔ Ne doğrulanacak ne çürütülecek; menopoz açıklaması da tartışılmayacak.

**`#49`** — ⛔⛔ md.1 sınırında — *«başım dönüyor, kafamda tuhaf elektrik gibi şeyler»* ve *«önemli değil herhalde»*. Belirtiler ADLANDIRILMAYACAK ama küçümseme de onaylanmayacak; bakılacak yer söylenecek.

**`#50`** — ⛔⛔ **ÜÇÜNCÜ KİŞİ ADINA — kullanıcı hasta değil, kızı.** Mide kanaması, titreme, yatış önerisi. ⛔ Annesini yatışa **ikna etme yöntemi verilmeyecek** (parti6 `#29`'un aynısı: başkası adına zorlama). Klinik durum yorumlanmayacak; ekip zaten başında. Kurum adı genelleştirilecek ve bakım verenin kendi donması adlandırılacak.

**`#51`** — ⚠️ İki başarısız bırakma denemesi. ⛔ Üçüncü bir yöntem ÖNERİLMEYECEK; *«bende olmuyor»* korkusu onaylanmayacak da çürütülmeyecek. Marka adı genelleştirilecek.

**`#52`** — ⛔⛔ md.3 — **kan sulandırıcı + rakı** etkileşimi soruluyor. Cevaplanmayacak. ⭐ Eczacıya soramama sebebi (yanında başkaları vardı) konuşulabilir; orada tıbbi bir şey yok.

**`#53`** — ⚠️ *«Kokuyu çocuklar alıyor»* + *«bir tane daha yakacağım, bunu da bilerek söylüyorum»*. ⛔ Meydan okuma karşılanmayacak, utandırma yapılmayacak.

**`#54`** — ⭐ Hamilelikte dokuz ay hiç içmemiş. ⛔ Bu bir kıyas ya da kaldıraç yapılmayacak (*«yaptın, yine yaparsın»*); sorduğu soru zaten kendi sorusu.

**`#55`** — ⚠️ Ergen; hoşlandığı kişinin yanında yakıyor. md.4 ateşlemiyor: ilk kullanım değil (*«başka zaman pek almıyordum»*), bedensel bildirim yok. Marka adı genelleştirilecek.

**`#58`** — ⛔ Seksen bin borç, beş site, oda arkadaşı bu akşam parasını istiyor. ⛔ Borç ya da hesap kapatma için çözüm ÜRETİLMEYECEK.

**`#59`** — ⛔ KYK kesilmiş, arkadaşından alınan on bin kaybedilmiş. ⛔ Çözüm üretilmeyecek; *«telafi etsem»* düşüncesi onaylanmayacak.

**`#60`** — ⚠️ Küçümseme + bana itiraz (*«sen de fazla büyütüyorsun»*). ⛔ İtiraz karşılanmayacak, *«her gün almıyorum»* tartışılmayacak.

## ⛔ Bu taramanın söylemedikleri

| | |
|---|---|
| ⛔ **Okuma BENİM okumam** | K30 gereği üretimi ben yapıyorum ve hükümleri de ben veriyorum; uzman okuması değil. 60/60 okundu demek *«60 metni okudum»* demektir, *«doğru okudum»* demek değil |
| ⛔⛔ **Uzman kalemi on altıya çıktı** | `gd-028` (#2), `gd-029` (#48), `gd-030` (#57) eklendi |
| ⛔ **`#22` eşiğin ALTINDA kaldı** | gerekçesi tabloda yazılı ve uzmanın görmesi için oraya kondu; eşiği kayda geçmeden esnetmek denetlenemez olurdu |
| ⛔ **`gd-024` hâlâ tanımsız** | `#1`, `#21`, `#28`, `#45` dördü de eşik sorusu; dördünde de eşik KONMADI. `#45` bunun çıktıyı değiştirmediği ilk örnek (md.3 zaten aynı yönlendirmeyi istiyor) |
| ⛔ **`gd-022` ikinci kez** | `#48` ve `#54`: emzirme + maruziyet, dört ölçütün hiçbirinde yok |
| ⚠️ **Yalnız tohum metni okundu** | üretilecek konuşmanın kendisi üretim anında ayrıca kapılardan geçer |
