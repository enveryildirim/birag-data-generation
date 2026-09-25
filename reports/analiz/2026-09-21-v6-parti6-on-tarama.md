# v6-parti6 — üretim öncesi kriz taraması

**Betik:** `scripts/analiz/2026-09-21-v6-parti6-on-tarama.py` · **Tarih:** 2026-09-21  
**Girdi:** `data/plan/v6-parti6.jsonl` · **60** satır

⛔⛔⛔ **T213: parti5'te `md.` ölçütlerini ateşleyen dört satırın dördü de işaretsizdi.** İşaretleme ölçütü tohumun kendi `risk_seviyesi` etiketiydi, metnin okunması değil. ⇒ Bu partide okuma kümesi kuyruğa değil **partiye** eşit: 60 satırın 60'ının hükmü yazılı ve betik, hükmü olmayan tek bir satır kalırsa raporu yazmıyor.

| | |
|---|---:|
| plan satırı | **60** |
| ⭐ **hükmü yazılı** | **60 / 60** |
| ⛔ **üretilmeyecek** | **2** [2, 36] |
| ⚠️ üretim notu olan | 34 |
| ⭐ okundu, not gerekmiyor | 24 |
| süzgeç işareti taşıyan | 14 |
| — içerik/beyan süzgeci ateşleyen | 1 |

## ⭐⭐ İşaret ne kadar öngördü — T213'ün ölçüsü

| | |
|---|---:|
| hüküm gerektiren satır (eleme + not) | **36** |
| — bunlardan süzgecin işaretlediği | **10** (%28) |
| ⛔ — **süzgecin KAÇIRDIĞI** | **26** [1, 3, 6, 8, 13, 14, 16, 21, 25, 26, 28, 29, 34, 39, 40, 41, 43, 45, 47, 48, 49, 54, 55, 56, 57, 60] |

➡️ Süzgeç, hüküm gerektiren satırların %28'ini gördü. Kalanı yalnız okuma yakaladı. ⛔ Bu sayı süzgecin kusuru değil, **kapsamının ölçüsü**: süzgeç bir sıralama aracıdır, bir güvence değil.

## Satır satır hüküm

| # | tür / senaryo | süzgeç işareti | hüküm |
|---:|---|---|---|
| 1 | `tutun` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 2 | `alkol` / `belirsiz` | risk:yuksek | ⛔⛔ **ÜRETİLMEYECEK** |
| 3 | `tutun` / `belirsiz` | — | ⚠️ okundu, **üretim notu var** |
| 4 | `kumar` / `ambivalans` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 5 | `alkol` / `nazikce_karsi_cikma` | — | ⭐ okundu, not gerekmiyor |
| 6 | `receteli_ilac` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 7 | `alkol` / `ambivalans` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 8 | `receteli_ilac` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 9 | `alkol` / `rol_siniri` | — | ⭐ okundu, not gerekmiyor |
| 10 | `dijital` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 11 | `kumar` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 12 | `kumar` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 13 | `tutun` / `belirsiz` | — | ⚠️ okundu, **üretim notu var** |
| 14 | `alkol` / `rol_siniri` | — | ⚠️ okundu, **üretim notu var** |
| 15 | `kumar` / `nazikce_karsi_cikma` | — | ⭐ okundu, not gerekmiyor |
| 16 | `tutun` / `nazikce_karsi_cikma` | — | ⚠️ okundu, **üretim notu var** |
| 17 | `kumar` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 18 | `dijital` / `belirsiz` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 19 | `kumar` / `nazikce_karsi_cikma` | — | ⭐ okundu, not gerekmiyor |
| 20 | `alkol` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 21 | `alkol` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 22 | `kumar` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 23 | `receteli_ilac` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 24 | `dijital` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 25 | `receteli_ilac` / `rol_siniri` | — | ⚠️ okundu, **üretim notu var** |
| 26 | `tutun` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 27 | `tutun` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 28 | `alkol` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 29 | `alkol` / `nazikce_karsi_cikma` | — | ⚠️ okundu, **üretim notu var** |
| 30 | `dijital` / `belirsiz` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 31 | `alkol` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 32 | `kumar` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 33 | `receteli_ilac` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 34 | `alkol` / `rol_siniri` | — | ⚠️ okundu, **üretim notu var** |
| 35 | `kumar` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 36 | `receteli_ilac` / `discord` | TG:acil servis + risk:yuksek | ⛔⛔ **ÜRETİLMEYECEK** |
| 37 | `tutun` / `nazikce_karsi_cikma` | — | ⭐ okundu, not gerekmiyor |
| 38 | `kumar` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 39 | `receteli_ilac` / `nazikce_karsi_cikma` | — | ⚠️ okundu, **üretim notu var** |
| 40 | `receteli_ilac` / `rol_siniri` | — | ⚠️ okundu, **üretim notu var** |
| 41 | `kumar` / `nazikce_karsi_cikma` | — | ⚠️ okundu, **üretim notu var** |
| 42 | `alkol` / `rol_siniri` | — | ⭐ okundu, not gerekmiyor |
| 43 | `receteli_ilac` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 44 | `kumar` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 45 | `tutun` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 46 | `receteli_ilac` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 47 | `receteli_ilac` / `rol_siniri` | — | ⚠️ okundu, **üretim notu var** |
| 48 | `tutun` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 49 | `alkol` / `nazikce_karsi_cikma` | — | ⚠️ okundu, **üretim notu var** |
| 50 | `dijital` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 51 | `alkol` / `nazikce_karsi_cikma` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 52 | `receteli_ilac` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 53 | `kumar` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 54 | `tutun` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 55 | `tutun` / `nazikce_karsi_cikma` | — | ⚠️ okundu, **üretim notu var** |
| 56 | `receteli_ilac` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 57 | `kumar` / `nazikce_karsi_cikma` | — | ⚠️ okundu, **üretim notu var** |
| 58 | `alkol` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 59 | `kumar` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 60 | `receteli_ilac` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |

## ⛔⛔ Üretilmeyecek satırlar — gerekçeleriyle

**`#2`** — ⛔⛔⛔ **SÜREN AKUT TIBBİ DURUM + DOĞRUDAN İKİLEM.** 36 saattir içmiyor, kendi kararıyla bırakmış; şu an titreme, terleme, çarpıntı var ve kusmuş; evde yalnız. Üstüne *«bir kadeh içsem geçer mi, yoksa hastaneye mi gitsem?»* diye soruyor. İki cevabın da tıbbi sonucu var ve ikisi arasında seçim yapmak bir triyaj kararıdır. §5a″ md.1'in yönlendirmesi burada yetmiyor: soru yönlendirme değil, KARAR istiyor. ⇒ Uzman + etik kurul (`gd-026`).

**`#36`** — ⛔⛔⛔ **BİR ÇOCUĞUN CÜMLESİ BİR OLAYI BİLDİRİYOR.** *«Anne dün ölecek miydin»* — dün bir şey olmuş ve çocuk annesinin ölebileceğini düşünmüş; üstüne yıllardır gizlenen bir ilaç kullanımı ve çocukların evden gönderilmesi konuşuluyor. Olayın ne olduğu yazmıyor ve ben varsaymam. Bu bir kriz SONRASI kayıttır; nasıl karşılanacağı klinik ve etik bir karardır (`gd-023` ile aynı sınıf). ⇒ Uzman (`gd-027`).

## ⚠️ Üretim notları — eleme değil, talimat

**`#1`** — ⛔ md.4 SINIRINDA VE ATEŞLENMEYECEK — ergen, elektronik sigara sipariş etmiş, yaş sorulmamış; ama **kullanım henüz olmamış** (kutuyu açıyor). Ölçüt *«ilk kullanım»* diyor, *«yaklaşan ilk kullanım»* demiyor ve ben aradaki eşiği YİNE koymayacağım (`gd-024`). ⛔ *«satıyolarsa sıkıntı yok di mi»* iki soru birden: yasallık ve zarar. İkisi de cevaplanmayacak. Marka adı genelleştirilecek.

**`#3`** — ⭐ İyi giden an: ilk poliklinik randevusu, kâğıt çantada. Sabah içmiş olması bir suç konusu yapılmayacak; *«başaramayacak diye düşünmesinler»* korkusu da onaylanıp büyütülmeyecek. Marka adı genelleştirilecek.

**`#6`** — ⛔⛔ md.2 — lohusa, dört aylık bebek, hamilelikte bıraktığı ilacı iki haftadır yeniden alıyor ve hekim bilmiyor. ⛔ *«Sanırım depresyondayım»* ONAYLANMAYACAK da ÇÜRÜTÜLMEYECEK de. ⛔⛔ *«Bebeği elimden alırlar»* korkusuna hukuki bir güvence VERİLMEYECEK — bilmediğim bir şeyi bilmiş gibi yapmak olur — ve korku bir kaldıraç olarak da kullanılmayacak. İlaç adı genelleştirilecek.

**`#8`** — ⛔ md.3 — *«tek seferden bir şey olmaz herhalde değil mi»* doğrudan zarar sorusu. Cevaplanmayacak. ⛔ Doz kesri yazılmayacak (T215). Kurum adı genelleştirilecek.

**`#13`** — ⛔ md.3 — **iki tedavi arasında seçim** isteniyor (nikotin bandı mı akupunktur mu, *«hangisi bana göre»*). Seçim YAPILMAYACAK; seçecek olan hekimi zaten görmüş.

**`#14`** — ⭐ Yordamsal ve iyi: çevrimiçi destek grubuna kamerasız/isimsiz katılım ve evde mahremiyet. ⛔ Örgüt adı genelleştirilecek (K110). Eşin küçümsemesi tartışılmayacak.

**`#16`** — ⚠️ *«Bu kadarcığını da mı çok görecekler»* bir savunma; miktar tartışılmayacak ve iki çocukla yorgunluk küçümsenmeyecek.

**`#17`** — ⚠️ Üçüncü nüks, sponsor cevap vermiyor. ⛔ Örgüt adı genelleştirilecek. Toplantıya girip girmeme kararı verilmeyecek ve cevaba bir kişi daha eklenmeyecek (parti5 `#37`'nin dersi).

**`#21`** — ⚠️ *«bazı şeyleri tam çıkaramıyorum»* — bir bellek boşluğu. Bedensel mi değil mi belirsiz ve eşiği YİNE koymayacağım (`gd-024`); ne adlandırılacak ne de yorumlanacak.

**`#22`** — ⛔⛔ **ELEME EŞİĞİNİN ALTINDA KALDI VE GEREKÇESİ BURADA YAZILI.** 920 bin borç, icra, eve giremiyor, eşinin haberi yok, *«kaçayım»* ve *«Yoruldum»*. Gerçek hayatta yüksek riskli bir örüntü. ⛔ Ama bu depoda eleme eşiği yazılı: `gd-021`/`gd-025`'te elenen şey **hayatın değerine ya da kaybolmaya dair bir CÜMLE** idi; burada öyle bir cümle yok, *«kaçayım»* borçtan kaçmayı anlatıyor. Eşiği kayda geçmeden esnetmem denetlenemez olurdu ⇒ üretiliyor. ⚠️ **Uzmanın görmesi için buraya yazıldı.** ⛔ Borca çözüm üretilmeyecek, *«kaç/kaçma»* denmeyecek, *«yoruldum»* sorgulanmayacak.

**`#23`** — ⛔ md.2 — antidepresan + akşam şarabı, üstüne sabah içmeleri başlamış, hekim bilmiyor. İlaç adı genelleştirilecek. *«Kendimden iğreniyorum»* bir kaldıraca çevrilmeyecek.

**`#25`** — ⛔ md.2 — lohusa, uyuyabilmek için gizlice ilaç alıyor. İlaç adı genelleştirilecek. Kayınvalidenin haklı olup olmadığı tartışılmayacak.

**`#26`** — ⭐ Kendi kendine yakalamış: doktorun cümlesini beraat gibi kullanmış ve utanmış. Üstüne ders konmayacak.

**`#28`** — ⚠️ Videonun çekildiği anı hatırlamıyor — `#21` ile aynı belirsizlik; adlandırılmayacak.

**`#29`** — ⛔⛔ **BAŞKASINI ZORLAMANIN YOLU SORULUYOR.** *«Onu zorla götürmenin bir yolu var mı?»* — verilmeyecek. Eşi burada değil ve rızası yok. ⭐ Sorunun ikinci yarısı (*«kendim mi gidip onu konuşmalıyım»*) cevaplanabilir.

**`#33`** — ⭐ Hekim zaten azaltıyor ve kendisi uyuyor ⇒ md.2 ATEŞLEMİYOR. ⛔ Gelinin torunları koz yapması tartışılacak bir haklılık meselesi değil; kendi cümlesi *«niye bu kadar sert»* karşılanacak.

**`#34`** — ⚠️ İşsizlik + her akşam içme. *«Elimde değil gibi»* bir teşhis istemiyor; teşhis verilmeyecek.

**`#39`** — ⛔⛔ md.2 — *«yarından itibaren hiç almayacağım… doğru karar değil mi sence»*. Reçeteli bir ilacı tek başına ve birden kesme kararı; ONAYLANMAYACAK, karşı da çıkılmayacak (ikisi de klinik hüküm). Doz kesri yazılmayacak (T215).

**`#40`** — ⛔ md.2 — babanın *«bu evin tek umudu o»* cümlesinden sonra yarım kutu ilaca bakmak. ⛔ Uyarıcı ilacın sınav için kullanımı konuşulmayacak; ilaç adı genelleştirilecek. ⚠️ *«Hiç bilmiyorum ne hissediyorum»* bir uyuşma; buradan kriz varsayımı ÜRETİLMEYECEK (beyan yok) ama duygu da adlandırılmayacak.

**`#41`** — ⛔ Aylık aidatlı bir tahminci grubuna para yollama planı onaylanmayacak; *«mantıklı geliyor di mi»* boş bırakılmayacak. Ödeme aracının adı geçmeyecek.

**`#43`** — ⛔ md.3 — *«öyle bağımlı olunmuyor değil mi»* doğrudan bir teşhis/zarar sorusu. Cevaplanmayacak. Oda arkadaşının iki yılı bir kanıt olarak ele alınmayacak.

**`#44`** — ⛔ Tefeci. Borca ve tefeciye dair hiçbir yol gösterilmeyecek; *«bırakırsam borcu nasıl öderim»* bir ikilem olarak karşılanacak.

**`#45`** — ⛔⛔ md.3 — *«sigara gibi mi yoksa daha az zararlı mı»* doğrudan karşılaştırmalı zarar sorusu, ve ilk kullanım. ⚠️ *«Hafif başım dönüyor»* şu ana ait bedensel bir bildirim; md.1'in eşiğini koymayacağım (`gd-024`) ve **buna gerek de yok: md.3 zaten aynı yönlendirmeyi gerektiriyor.** Bu, tanımsız eşiğin çıktıyı değiştirmediği ilk örnek ve kayda geçiyor.

**`#46`** — ⛔ md.2 — beş yıldır uyku ilacı, oğlu geçen haftaki düşmeyi ve unutmayı söylüyor. Hekim ilacı yazıyor ama DÜŞMEYİ bilmiyor; sürdürme kararı tek başına alınıyor. Belirtiler adlandırılmayacak, ilaç adı geçmeyecek.

**`#47`** — ⛔⛔ md.3 — *«tek seferlik bi şey için cidden zararlı olur mu»* + **reçetesiz satan bir site**. Zarar sorusu cevaplanmayacak, site hiçbir biçimde ele alınmayacak, doz sayısı ve ilaç adı yazılmayacak.

**`#48`** — ⚠️⚠️ **EMZİRME + SİGARA — DÖRT ÖLÇÜTÜN HİÇBİRİ ATEŞLEMİYOR.** Akut olay yok, reçeteli ilaç yok, ergen yok, doğrudan soru yok. Bebeğe maruziyet boyutu §5a″'da YOK (`gd-022` komşuluğu, parti5 `#33`'ten sonra ikinci kez). ⛔ Sütün etkilenip etkilenmediği söylenmeyecek; utanç da büyütülmeyecek.

**`#49`** — ⚠️ Ergen, babası bira uzatmış. md.4 ateşlemiyor: ilk kullanım belirtilmemiş, bedensel bildirim yok. ⛔ Babanın davranışı yargılanmayacak, dinî çerçeve tartışılmayacak. *«Ne hissediyor olabilirim sence»* — duygusu onun yerine adlandırılmayacak.

**`#51`** — ⛔ Yasal süreç. Mahkemeye dair hiçbir tahmin yürütülmeyecek; ofisteki bakışların ne anlama geldiği de yorumlanmayacak.

**`#54`** — ⚠️ Emzirme + üç günde yedi saat uyku. `#48` ile aynı sınıf; ölçüt yok. Uyku için yordam verilmeyecek, sütün etkisi konuşulmayacak.

**`#55`** — ⛔⛔ **GİZLEMEYE YARDIM İSTENİYOR:** *«Doktor sigarayı sorar mı, kıyafetimde koku kalır mı»* — bebeğin hekiminden bilgi saklamanın yolu. Yardım edilmeyecek; utandırma da yapılmayacak.

**`#56`** — ⚠️ Küçültme (*«sadece yarım hap»*). Hekimin bilip bilmediği yazmıyor ⇒ md.2 varsayılmayacak. Doz kesri yazılmayacak (T215).

**`#57`** — ⚠️ Beş aylık bebek, gece oyunları, *«bebekle göz göze gelmek zor»*. Utanç büyütülmeyecek; *«kimseye söylemedim»* bugünkü hareket olarak görülecek.

**`#58`** — ⭐ Karar anı (parti5 `#44`'ün biçimi ama kendi cümleleriyle): şişe masada, *«açayım mı kapatayım mı»*. ⛔ *«Açma»* denmeyecek, boş da bırakılmayacak. İki sesi de kendisi yazmış.

**`#60`** — ⛔⛔ md.3 + md.2 — bir yıllık aradan sonra *«bu geceyi atlatmak için yarım doz alsam… mantıklı bir orta yol mu»*. Onaylanmayacak; doz konuşulmayacak, kesir yazılmayacak (T215). ⛔ Bir yıl bir kaldıraç olarak kullanılmayacak (*«bozma»* denmeyecek).

## ⛔ Bu taramanın söylemedikleri

| | |
|---|---|
| ⛔ **Okuma BENİM okumam** | K30 gereği üretimi ben yapıyorum ve hükümleri de ben veriyorum; uzman okuması değil. 60/60 okundu demek *«60 metni okudum»* demektir, *«doğru okudum»* demek değil |
| ⛔⛔ **Uzman kalemi on üçe çıktı** | `gd-026` (#2: süren akut tıbbi durum + triyaj sorusu) ve `gd-027` (#36: bir çocuğun bildirdiği olay) eklendi |
| ⛔ **`#22` eşiğin ALTINDA kaldı** | gerekçesi tabloda yazılı ve uzmanın görmesi için oraya kondu; eşiği kayda geçmeden esnetmek denetlenemez olurdu |
| ⛔ **`gd-024` hâlâ tanımsız** | `#1`, `#21`, `#28`, `#45` dördü de eşik sorusu; dördünde de eşik KONMADI. `#45` bunun çıktıyı değiştirmediği ilk örnek (md.3 zaten aynı yönlendirmeyi istiyor) |
| ⛔ **`gd-022` ikinci kez** | `#48` ve `#54`: emzirme + maruziyet, dört ölçütün hiçbirinde yok |
| ⚠️ **Yalnız tohum metni okundu** | üretilecek konuşmanın kendisi üretim anında ayrıca kapılardan geçer |
