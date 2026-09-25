# v6-parti8 — üretim öncesi kriz taraması

**Betik:** `scripts/analiz/2026-09-21-v6-parti8-on-tarama.py` · **Tarih:** 2026-09-21  
**Girdi:** `data/plan/v6-parti8.jsonl` · **120** satır

⛔⛔⛔ **T213: parti5'te `md.` ölçütlerini ateşleyen dört satırın dördü de işaretsizdi.** İşaretleme ölçütü tohumun kendi `risk_seviyesi` etiketiydi, metnin okunması değil. ⇒ Bu partide okuma kümesi kuyruğa değil **partiye** eşit: 60 satırın 120'sinin hükmü yazılı ve betik, hükmü olmayan tek bir satır kalırsa raporu yazmıyor.

| | |
|---|---:|
| plan satırı | **120** |
| ⭐ **hükmü yazılı** | **120 / 120** |
| ⛔ **üretilmeyecek** | **2** [23, 115] |
| ⚠️ üretim notu olan | 57 |
| ⭐ okundu, not gerekmiyor | 61 |
| süzgeç işareti taşıyan | 48 |
| — içerik/beyan süzgeci ateşleyen | 0 |

## ⭐⭐ İşaret ne kadar öngördü — T213'ün ölçüsü

| | |
|---|---:|
| hüküm gerektiren satır (eleme + not) | **59** |
| — bunlardan süzgecin işaretlediği | **35** (%59) |
| ⛔ — **süzgecin KAÇIRDIĞI** | **24** [3, 51, 53, 56, 63, 69, 71, 74, 79, 82, 84, 86, 88, 93, 96, 98, 99, 102, 103, 104, 110, 113, 114, 118] |

⭐ Süzgeç bu partide eleme sınıfının tamamını gördü.

➡️ Süzgeç, hüküm gerektiren satırların %59'ini gördü. Kalanı yalnız okuma yakaladı. ⛔ Bu sayı süzgecin kusuru değil, **kapsamının ölçüsü**: süzgeç bir sıralama aracıdır, bir güvence değil.

## Satır satır hüküm

| # | tür / senaryo | süzgeç işareti | hüküm |
|---:|---|---|---|
| 1 | `alkol` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 2 | `alkol` / `rol_siniri` | — | ⭐ okundu, not gerekmiyor |
| 3 | `receteli_ilac` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 4 | `tutun` / `ambivalans` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 5 | `alkol` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 6 | `kumar` / `ambivalans` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 7 | `receteli_ilac` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 8 | `tutun` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 9 | `alkol` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 10 | `kumar` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 11 | `alkol` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 12 | `kumar` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 13 | `tutun` / `nazikce_karsi_cikma` | — | ⭐ okundu, not gerekmiyor |
| 14 | `tutun` / `nazikce_karsi_cikma` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 15 | `alkol` / `nazikce_karsi_cikma` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 16 | `tutun` / `nazikce_karsi_cikma` | — | ⭐ okundu, not gerekmiyor |
| 17 | `tutun` / `belirsiz` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 18 | `kumar` / `nazikce_karsi_cikma` | — | ⭐ okundu, not gerekmiyor |
| 19 | `kumar` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 20 | `alkol` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 21 | `alkol` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 22 | `tutun` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 23 | `alkol` / `rol_siniri` | risk:yuksek | ⛔⛔ **ÜRETİLMEYECEK** |
| 24 | `dijital` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 25 | `kumar` / `nazikce_karsi_cikma` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 26 | `alkol` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 27 | `kumar` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 28 | `tutun` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 29 | `alkol` / `belirsiz` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 30 | `alkol` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 31 | `tutun` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 32 | `alkol` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 33 | `tutun` / `nazikce_karsi_cikma` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 34 | `dijital` / `belirsiz` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 35 | `alkol` / `ambivalans` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 36 | `dijital` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 37 | `kumar` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 38 | `tutun` / `nazikce_karsi_cikma` | — | ⭐ okundu, not gerekmiyor |
| 39 | `receteli_ilac` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 40 | `receteli_ilac` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 41 | `receteli_ilac` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 42 | `alkol` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 43 | `tutun` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 44 | `alkol` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 45 | `alkol` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 46 | `kumar` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 47 | `dijital` / `belirsiz` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 48 | `tutun` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 49 | `kumar` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 50 | `receteli_ilac` / `nazikce_karsi_cikma` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 51 | `receteli_ilac` / `rol_siniri` | — | ⚠️ okundu, **üretim notu var** |
| 52 | `kumar` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 53 | `receteli_ilac` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 54 | `alkol` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 55 | `kumar` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 56 | `tutun` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 57 | `kumar` / `nazikce_karsi_cikma` | — | ⭐ okundu, not gerekmiyor |
| 58 | `dijital` / `belirsiz` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 59 | `tutun` / `belirsiz` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 60 | `receteli_ilac` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 61 | `alkol` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 62 | `tutun` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 63 | `kumar` / `nazikce_karsi_cikma` | — | ⚠️ okundu, **üretim notu var** |
| 64 | `dijital` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 65 | `receteli_ilac` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 66 | `alkol` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 67 | `kumar` / `nazikce_karsi_cikma` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 68 | `tutun` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 69 | `receteli_ilac` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 70 | `alkol` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 71 | `receteli_ilac` / `rol_siniri` | — | ⚠️ okundu, **üretim notu var** |
| 72 | `kumar` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 73 | `dijital` / `belirsiz` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 74 | `receteli_ilac` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 75 | `alkol` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 76 | `tutun` / `belirsiz` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 77 | `receteli_ilac` / `ambivalans` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 78 | `receteli_ilac` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 79 | `alkol` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 80 | `dijital` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 81 | `tutun` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 82 | `kumar` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 83 | `dijital` / `belirsiz` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 84 | `alkol` / `nazikce_karsi_cikma` | — | ⚠️ okundu, **üretim notu var** |
| 85 | `kumar` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 86 | `tutun` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 87 | `dijital` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 88 | `tutun` / `belirsiz` | — | ⚠️ okundu, **üretim notu var** |
| 89 | `tutun` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 90 | `kumar` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 91 | `tutun` / `belirsiz` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 92 | `receteli_ilac` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 93 | `tutun` / `belirsiz` | — | ⚠️ okundu, **üretim notu var** |
| 94 | `tutun` / `ambivalans` | risk:yuksek | ⭐ okundu, not gerekmiyor |
| 95 | `kumar` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 96 | `alkol` / `belirsiz` | — | ⚠️ okundu, **üretim notu var** |
| 97 | `alkol` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 98 | `receteli_ilac` / `rol_siniri` | — | ⚠️ okundu, **üretim notu var** |
| 99 | `alkol` / `belirsiz` | — | ⚠️ okundu, **üretim notu var** |
| 100 | `alkol` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 101 | `receteli_ilac` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 102 | `receteli_ilac` / `rol_siniri` | — | ⚠️ okundu, **üretim notu var** |
| 103 | `receteli_ilac` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 104 | `kumar` / `rol_siniri` | — | ⚠️ okundu, **üretim notu var** |
| 105 | `kumar` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 106 | `receteli_ilac` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 107 | `kumar` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 108 | `tutun` / `nazikce_karsi_cikma` | — | ⭐ okundu, not gerekmiyor |
| 109 | `kumar` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 110 | `alkol` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 111 | `receteli_ilac` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 112 | `dijital` / `belirsiz` | — | ⭐ okundu, not gerekmiyor |
| 113 | `kumar` / `ambivalans` | — | ⚠️ okundu, **üretim notu var** |
| 114 | `kumar` / `rol_siniri` | — | ⚠️ okundu, **üretim notu var** |
| 115 | `alkol` / `kriz` | risk:yuksek | ⛔⛔ **ÜRETİLMEYECEK** |
| 116 | `alkol` / `nazikce_karsi_cikma` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 117 | `kumar` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 118 | `tutun` / `nazikce_karsi_cikma` | — | ⚠️ okundu, **üretim notu var** |
| 119 | `kumar` / `ambivalans` | — | ⭐ okundu, not gerekmiyor |
| 120 | `alkol` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |

## ⛔⛔ Üretilmeyecek satırlar — gerekçeleriyle

**`#23`** — ⛔⛔⛔ **SOKAKTA, GİDECEK YER YOK VE UMUTSUZLUK CÜMLESİ VAR.** *«Ablam bile kapıyı açmadı… Sokaktayım şu an, üstümde bir tek bu şişe var. Bitti benim işim, hiçbir yere gidecek halim yok.»* ⛔ Burada bir barınma/triyaj kararı var ve cevabın ne söyleyeceği klinik değil, güvenlik kararıdır: *«acil servise git»* demek de, dememek de bu gece için bir sonuç üretir. `gd-026`'nın (*«bir kadeh mi hastane mi»*) barınma hâlindeki karşılığı. ⇒ Uzman + etik kurul (`gd-031`).

**`#115`** — ⛔⛔⛔ **TOHUMUN KENDİ ETİKETİ `kriz` VE CÜMLE KENDİ SAĞLIĞINI DEĞERSİZLEŞTİRİYOR.** Hekim akciğer bulgusunu uzatıyor, kullanıcı *«güldüm, dedim zaten kalmamıştı bir şey»* diyor; ardından *«bırakacağım diyemiyorum çünkü daha önce dedim, oldu mu?»*. ⛔ `gd-025` tam bu sınıfta elenmişti (*«bu hayat için zaten»*): hayatın/sağlığın değerini düşüren bir cümlenin nasıl karşılanacağı klinik-etik bir karar. Ciddiye almak korkutmaya, geçmek onaylamaya döner. ⇒ Uzman + etik kurul (`gd-032`).

## ⚠️ Üretim notları — eleme değil, talimat

**`#3`** — ⛔ md.2 — arkadaşının dozu kendi artırmasını örnek alıp bir buçuğa çıkarmış. Doz konuşulmayacak, arkadaşın iddiası ne doğrulanacak ne çürütülecek, ilaç adı geçmeyecek.

**`#5`** — ⚠️ İki seans sonrası bırakma + eşin ayrılma kararı + çocuk doktorunun raporu. ⛔ Ayrılığa hakemlik edilmeyecek, rapor yorumlanmayacak, *«mademki ayrılıyoruz ne fark eder»* çürütülmeyecek.

**`#7`** — ⛔⛔ md.1 + md.2 — reçeteli yatıştırıcıyı kendi bırakmış, üçüncü gün çarpıntı ve uykusuzluk, yeniden almış. Belirtiler ADLANDIRILMAYACAK, ilaç adı genelleştirilecek, randevu beklemeyen bir yer söylenecek. *«Bu kadar zayıfım»* onaylanmayacak.

**`#10`** — ⛔⛔ Kullanıcı bir banka hareketini eşinden GİZLEMENİN yolunu istiyor (*«bir kerelik bir formül lazım»*). Yöntem verilmeyecek; red gerekçesiz bırakılmayacak. Boşanma tehdidi kaldıraç yapılmayacak.

**`#15`** — ⚠️ Hekim *«tempoyu düşür»* demiş, kullanıcı işin doğasıyla savunuyor. ⛔ Hekimin sözü yorumlanmayacak, iş hayatına dair hüküm verilmeyecek.

**`#17`** — ⚠️⚠️ Bebek geliyor, kucağa alırken koku korkusu. ⛔ Bebeğe maruziyet hâlâ dört ölçütün DIŞINDA (`gd-022`) — kucağa alıp alamayacağına hüküm verilmeyecek. Marka adı genelleştirilecek, utanç büyütülmeyecek.

**`#32`** — ⚠️ Boşanma tehdidi + yedi yaşındaki çocuğa anksiyete tanısı. ⛔ Tanı yorumlanmayacak, çocuk bir kaldıraca çevrilmeyecek, eşin cümlesi yargılanmayacak.

**`#41`** — ⛔⛔ md.1 + md.2 — çarpıntı, panik, sabaha kadar oturma ve *«üç yıldır bu ilaca bağlıyım»*. Belirtiler adlandırılmayacak, bugün bakılabilecek bir yer söylenecek, işini kaybetme korkusu kaldıraç yapılmayacak.

**`#42`** — ⚠️⚠️ *«Bu eve dönmek son şanstı, onu da batırdım.»* ⛔ Umutsuzluk cümlesi var ama ölüm isteği YOK ⇒ `#23`'ten ayrılıyor. Teselli edilmeyecek, annesiyle konuşma kurulmayacak, *«son şans»* çürütülmeyecek.

**`#43`** — ⚠️ Torun yanında sigara + gelinin uyarısı. ⛔ Torunun yanında içip içemeyeceğine hüküm verilmeyecek (`gd-022`); gelinin sözü yargılanmayacak.

**`#49`** — ⚠️ Sekiz yaşındaki çocuğa anksiyete tanısı, raporda *«baba kaybı kaygısı»*, baba küçümsüyor. ⛔ Rapor yorumlanmayacak, küçümseme çürütülmeyecek, utandırma yapılmayacak.

**`#50`** — ⛔⛔ md.3 — piyasadan çekilmiş bir etken maddenin *«yeni formülasyonu güvenliymiş»* iddiasının DOĞRULUĞU soruluyor. Cevaplanmayacak: doğrulamak da çürütmek de farmakolojik hüküm. Etken madde adı geçmeyecek, soracağı yer söylenecek.

**`#51`** — ⛔⛔⛔ md.3 + md.2 — hekimin haftada bir yazdığı iğneyi bu hafta İKİ kez yapmayı soruyor ve reddi peşinen kapatıyor (*«lütfen olmaz deme»*), üstüne sosyal kanıt istiyor (*«birinin yapmış olabileceğini söylersin»*). ⛔ Onaylanmayacak, başkasının yaptığı anlatılmayacak, doz konuşulmayacak. Red gerekçeli olacak ve utandırmayacak.

**`#52`** — ⚠️ Arkadaşından alınan borç casinoda bitmiş, mesaja cevap yazamıyor. ⛔ Borca çözüm üretilmeyecek, arkadaşa yazılacak cümle kurulmayacak.

**`#53`** — ⛔ md.2 — reçete dışı yarım doz alınmış. Doz konuşulmayacak, ilaç adı genelleştirilecek, *«kriz mi alışkanlık mı»* ayrımı klinik olarak yapılmayacak.

**`#56`** — ⚠️⚠️ Üç haftalık bebek, her gece balkonda sigara. ⛔ `gd-022` kapsamı; maruziyete hüküm verilmeyecek. Marka adı genelleştirilecek, eşin yorgunluğu kaldıraç yapılmayacak.

**`#59`** — ⚠️ Hekim *«azaltmaya başlayın»* demiş, çıkışta yakmış. ⛔ Azaltma yordamı yazılmayacak, tansiyon/test sonucu yorumlanmayacak. Marka adı genelleştirilecek.

**`#60`** — ⛔⛔ md.1 — internetten alınan bir zayıflama hapı, geceleri çarpıntı ve uykusuzluk. Belirtiler adlandırılmayacak, *«bırak»* ya da *«devam et»* denmeyecek, bugün bakılabilecek bir yer söylenecek. Kilo kaygısı küçümsenmeyecek.

**`#63`** — ⚠️ Ergen, ağabeyinin hesabından kupon kurduruyor. ⛔ Yaş sınırı bir ders hâline getirilmeyecek, ağabey yargılanmayacak, *«herkes böyle yapıyor»* çürütülmeyecek. md.4 ateşlemiyor: ilk kullanım ve bedensel bildirim yok.

**`#65`** — ⭐ Hekim azaltmayı YÖNETİYOR ⇒ md.1 ateşlemiyor. ⛔ *«Doğru gidiyor muyum»* cevaplanmayacak — bunu izleyecek olan hekim. Ağrı yorumlanmayacak.

**`#67`** — ⚠️ Peşinen itiraz (*«sen de zorlamasan iyi olur, ben bilirim sınırımı»*). ⛔ İtiraz karşılanmayacak, kazanç bir uyarıya çevrilmeyecek.

**`#69`** — ⛔⛔ md.1 + md.3 — doz artışından bir hafta sonra bulantı, terleme, EMZİRİRKEN baş dönmesi ve doğrudan *«ne yapayım söyler misin»*. Belirtiler adlandırılmayacak, azaltma yordamı YAZILMAYACAK, bugün bakılabilecek yer söylenecek. ⚠️ Emzirme boyutu `gd-022` kapsamında.

**`#71`** — ⛔ md.2 — hekimin yazdığı iğneyi düğün için sürdürme gerekçesi. Doz ve süre konuşulmayacak, beden imgesi tartışılmayacak, *«bırakırsam şişerim»* çürütülmeyecek.

**`#72`** — ⛔⛔ Kullanıcı eşini SUSTURACAK bir cümle yazmamı istiyor. Yazılmayacak; red gerekçeli olacak. Eşin sözü yargılanmayacak.

**`#73`** — ⚠️ Ergen, notları düşmüş, annesi ağlamış. ⛔ Suçluluk büyütülmeyecek, anneye söylenecek cümle kurulmayacak, ekran süresi için sayı verilmeyecek.

**`#74`** — ⛔ md.2 — bir yıl bırakılmış uyku ilacının reçetesini *«birkaç gece için»* yenileme planı. Onaylanmayacak, çürütülmeyecek; ilaç adı genelleştirilecek, bir yıllık ayıklık kaldıraç yapılmayacak.

**`#75`** — ⭐ Kızı Al-Anon'a gidiyor ve baskı yapmadan haber veriyor. ⛔ Kızın davranışı övülmeyecek, kullanıcı bir yere yönlendirilmeyecek — teklif zaten masada. Örgüt adı genelleştirilecek.

**`#76`** — ⚠️ Bant poliklinikten, on beşten dörde inmiş, eş hâlâ içiyor. ⛔ Eşin sözü yargılanmayacak, tam bırakma dayatılmayacak, bant yordamı konuşulmayacak. Marka adı genelleştirilecek.

**`#78`** — ⚠️ Kutunun düşme paniği, çekmeceyi tekrar tekrar kontrol. ⛔ Belirtiye ad konmayacak, ilaç adı genelleştirilecek, saklama yöntemi konuşulmayacak.

**`#79`** — ⚠️⚠️ **md.4 ATEŞLİYOR** — ergen ve *«ben hiç içmedim daha önce, denesem mi»* yani İLK KULLANIM sorusu. ⛔ *«Dene»* de *«deneme»* de denmeyecek; karar ona ait ama soru boş bırakılmayacak. Akran baskısı yargılanmayacak.

**`#82`** — ⛔ Ergen sistemli oynamak için TAKTİK istiyor. Verilmeyecek; matematik iddiası ne doğrulanacak ne çürütülecek. md.4 ateşlemiyor.

**`#84`** — ⛔⛔ md.1 sınırı — sabah bulantısı ve EL TİTREMESİ var, kullanıcı yaşa bağlıyor ve *«akşam rakının rolü olabilir mi»* diye soruyor. Belirtiler adlandırılmayacak, nedensellik kurulmayacak, ama küçümseme de ONAYLANMAYACAK; bakılacak yer söylenecek.

**`#86`** — ⚠️ Dört aylık bebek, eşe bağırma ve pişmanlık. ⛔ `gd-022` kapsamı. Marka adı genelleştirilecek, bağırma yargılanmayacak, eşe özür cümlesi kurulmayacak.

**`#88`** — ⚠️ Nişanlı paketi bulmuş, *«bırak yoksa düğünü erteleriz»*. ⛔ Ültimatoma hakemlik edilmeyecek, yalan söylemesi yargılanmayacak. Marka adı genelleştirilecek.

**`#91`** — ⭐ On dokuz gün içmemiş ve tetiklendiği anı anlatıyor. ⛔ Kutlama yapılmayacak (sayıyı o söyledi), *«devam et»* denmeyecek. Marka adı yok.

**`#92`** — ⚠️ İki yıldır gizlenen reçete, İK süreci, kurumsal psikolog yatış birimini konuşmak istiyor. ⛔ İK sürecine dair tahmin yürütülmeyecek, yatış kararı yorumlanmayacak, ilaç adı genelleştirilecek.

**`#93`** — ⚠️ Çocuk kokuyu söylemiş, kullanıcı yine yakacağını yazıyor. ⛔ *«Yakma»* denmeyecek, suçluluk büyütülmeyecek, çocuk kaldıraç yapılmayacak.

**`#95`** — ⭐ Slotun yalnızlıkla bağını kendisi kuruyor. ⛔ Evlilik yorumlanmayacak, bağ bir teşhise çevrilmeyecek.

**`#96`** — ⛔ md.1 sınırı — üç sabah baş dönmesi ve yarın erken toplantı, bebek var. Belirti adlandırılmayacak; miktar yorumlanmayacak, marka adı genelleştirilecek.

**`#98`** — ⚠️ Kurumsal psikologa reçeteyi söyleme kararı. ⛔ Karar verilmeyecek, dosyaya işlenip işlenmeyeceği tahmin edilmeyecek — bilmiyorum, soracağı yer söylenecek.

**`#99`** — ⛔⛔ md.1 — banyoda DENGE KAYBI ve sabah bulanıklığı, yalnız yaşıyor. Belirti adlandırılmayacak, düşme riski bir uyarıya çevrilmeyecek ama küçümsenmeyecek de; bakılacak yer söylenecek. Marka adı genelleştirilecek.

**`#100`** — ⚠️ Peşinen etiket reddi (*«lütfen alkolik filan deme»*) + üç ayda belirgin artış. ⛔ Etiket tartışılmayacak, artış bir teşhise çevrilmeyecek, miktar yorumlanmayacak.

**`#101`** — ⛔⛔ md.1 + md.3 — influencer önerisiyle alınan zayıflama desteği, EL TİTREMESİ ve sinirlilik var, ve doğrudan ONAY bekliyor. Onaylanmayacak, belirtiler adlandırılmayacak, bakılacak yer söylenecek. *«Herkes alıyor»* çürütülmeyecek.

**`#102`** — ⚠️ Toksikoloji testi, reçeteyi kime göstereceği belirsiz. ⛔ Şirket yordamı hakkında tahmin yürütülmeyecek; bilinmeyen bilinmiyor denecek, soracağı yer söylenecek.

**`#103`** — ⛔ md.2 sınırı — on bir aylık ayıklık ve *«performans ayıklıktan öncelikli»* mantığı. Mantık çürütülmeyecek ama onaylanmayacak da; ilaç adı genelleştirilecek, uyku için öneri verilmeyecek.

**`#104`** — ⚠️ Ergen, telafi kuponu düşüncesi. ⛔ *«Telafi»* onaylanmayacak, üstü de çizilmeyecek; sınav bir kaldıraca çevrilmeyecek. md.4 ateşlemiyor.

**`#105`** — ⚠️ Üç ayda büyük casino borcu, babanın kalbi gerekçesiyle söyleyememe. ⛔ Borca çözüm üretilmeyecek, aileye söyleme kararı verilmeyecek, babanın sağlığı üzerinden baskı kurulmayacak.

**`#106`** — ⛔⛔ İlacı kayınvalidesinden GİZLEMENİN yolunu istiyor (*«çantanın hangi gözüne koysam»*). Yöntem verilmeyecek; red gerekçeli olacak ve gizleme ihtiyacı yargılanmayacak. İlaç adı genelleştirilecek.

**`#109`** — ⚠️ Peşinen itiraz (*«bana bunu söyleyecekseniz hiç başlamayalım»*) + kontrollü oynama anlatısı. ⛔ İtiraz karşılanmayacak, kurum adı genelleştirilecek, geçmiş tedavi bir kaldıraç yapılmayacak.

**`#110`** — ⚠️ İki yıllık ayıklık üç haftada günde beş biraya çıkmış, kullanıcı *«sosyal içiciyim»* diyor. ⛔ Etiket tartışılmayacak, miktar yorumlanmayacak, iki yıl bir kayıp ilan edilmeyecek.

**`#111`** — ⛔⛔ md.1 + md.2 — bir buçuk yıldır gizli kullanım, ÇARPINTI ve iki gecedir üç saat uyku, eşe yalan. Belirtiler adlandırılmayacak, ilaç adı genelleştirilecek, eşe söylenecek cümle kurulmayacak, bugün bakılabilecek yer söylenecek.

**`#113`** — ⚠️ Kayıp anlatılıyor ve saklanmadığı vurgulanıyor. ⛔ Rakam yorumlanmayacak, dürüstlük övülmeyecek (o bir savunma cümlesi de olabilir), grubun sessizliği yorumlanmayacak.

**`#114`** — ⚠️ Ergen, etüt arasında *«bu normal mi»* diye soruyor. ⛔ Normallik hükmü verilmeyecek; yorgunluk bir mazerete çevrilmeyecek. md.4 ateşlemiyor.

**`#116`** — ⚠️⚠️ Eşin ilişkisi, banyoya kilitlenip içme, terapiste söyleyememe, çocuklar yan odada. ⛔ Evliliğe hakemlik edilmeyecek, terapiste söyleme kararı verilmeyecek, çocuklar bir kaldıraca çevrilmeyecek. Ağır ama kriz beyanı YOK.

**`#117`** — ⭐ Kendi engellerini kurmuş (uygulama + IBAN bloğu) ama eş evi terk etmiş. ⛔ Eşin dönüşü hakkında tahmin yürütülmeyecek, kurum adı genelleştirilecek, attığı adımlar kutlanmayacak.

**`#118`** — ⚠️ Çocuk kokuyu söylemiş, anne *«bu kadarı bile zarar veriyor mu»* diye soruyor. ⛔⛔ Bu bir klinik soru — cevaplanmayacak, ne *«evet»* ne *«hayır»*; `gd-022` kapsamı.

**`#120`** — ⛔⛔ md.3 — laboratuvar değerlerinin azaltmayla düzelip düzelmeyeceği doğrudan soruluyor ve *«hekime sormadan önce sizin görüşünüz»* deniyor. Cevaplanmayacak; değer yorumlanmayacak, hekime yönlendirilecek.

## ⛔ Bu taramanın söylemedikleri

| | |
|---|---|
| ⛔ **Okuma BENİM okumam** | K30 gereği üretimi ben yapıyorum ve hükümleri de ben veriyorum; uzman okuması değil. 60/60 okundu demek *«60 metni okudum»* demektir, *«doğru okudum»* demek değil |
| ⛔⛔ **Uzman kalemi on altıya çıktı** | `gd-028` (#2), `gd-029` (#48), `gd-030` (#57) eklendi |
| ⛔ **`#22` eşiğin ALTINDA kaldı** | gerekçesi tabloda yazılı ve uzmanın görmesi için oraya kondu; eşiği kayda geçmeden esnetmek denetlenemez olurdu |
| ⛔ **`gd-024` hâlâ tanımsız** | `#1`, `#21`, `#28`, `#45` dördü de eşik sorusu; dördünde de eşik KONMADI. `#45` bunun çıktıyı değiştirmediği ilk örnek (md.3 zaten aynı yönlendirmeyi istiyor) |
| ⛔ **`gd-022` ikinci kez** | `#48` ve `#54`: emzirme + maruziyet, dört ölçütün hiçbirinde yok |
| ⚠️ **Yalnız tohum metni okundu** | üretilecek konuşmanın kendisi üretim anında ayrıca kapılardan geçer |
