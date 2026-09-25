# Blok taslağı — kurallar

⛔⛔⛔ **ÖNCE ŞU BELGELERİ OKU.** Bu brif onların YERİNE GEÇMEZ, özetidir;
ve özetin yetmediği ÖLÇÜLDÜ (T234): yalnız brifle çalışan blok 39 kayıtta
10 kusur verdi, aynı gün proje belgelerini okuyan blok 2 verdi — fark en
çok bağlam pasajlarında ve uydurulmuş hizmetlerde çıktı (7→1 ve 4→0).

- `prompts/uretim-v5.md` — özellikle **§7** (bağlam blokları ve sınıfları),
  **§5a″** (md.1-4 sapma ölçütleri), **§2a** (thinking yasakları)
- `docs/davranis-kartlari.md` — hamlelerin nasıl kurulduğu
- `AGENTS.md` — Kural 3 (klinik sınırlar)
- `scripts/analiz/2026-09-21-uretim-v6-parti7-blok*.py` — ÜSLUP ÖRNEĞİ:
  `KAYIT` sözlüğündeki kayıtlar bu işin bitmiş hâlidir, onlara bak

⭐ Taslağı yazdıktan sonra kendi doğrulama betiğini yazıp sert kapıları
mekanik olarak denetlemen beklenir (bant, soru sayısı, thinking oranı,
marka/doz taraması, bağlam sınıfı). Blok 3'ün ajanı bunu yaptı ve fark
ölçümde göründü.

Türkçe bir bağımlılık destek sohbeti veri kümesi için **taslak kayıtlar**
yazacaksın. Taslakların tamamı sonradan okunacak, revize edilecek ve
mekanik kapılardan geçirilecek; senden beklenen bitmiş ürün değil, kapıları
geçebilecek sağlam bir ilk hâl.

## Kaydın yapısı

Her satır bir konuşma. `turn_type`:
- `single` → 1 kullanıcı mesajı + 1 asistan cevabı
- `multi`  → kullanıcı, KISA asistan sorusu, kullanıcı, asistan cevabı

Son asistan cevabı `son` alanına yazılır; ara asistan turu `turns` içinde.

## ⛔ SERT KAPILAR — biri bile geçmezse blok reddedilir

1. **`bicim` İLK kullanıcı mesajının sözcük sayısıdır** (bağlam bloğu
   sayılmaz): `kisa` ≤8 · `orta` 9-25 · `uzun` >25.
2. **`turn_ending` soru sayısını belirler** — SON asistan mesajındaki `?`:
   - `acik_uclu_soru` → tam **1**
   - `takdir`, `ozet`, `yalnizca_yansitma`, `durur` → **0**
3. **Bağlam.** `baglam_var` işaretli satırlarda bir `baglam` bloğu olacak
   (`kaynak` + `metin`, 1-2 cümle) ve ilk kullanıcı mesajı bağlam bloğuyla
   başlayacak. Pasaj yalnız yordam / erişim / gizlilik / uygunluk / sınır
   cümlesi içerir.
   ⛔⛔ **PASAJ DIŞ BİR KURUMUN YAZISIDIR, BU SOHBETİN DEĞİL.** Kaynak bir
   poliklinik bilgilendirmesi, danışma birimi notu, muhtarlık duyurusu ya
   da işyeri yönergesi gibi bir şeydir. ⛔ *«Bu sohbet…»*, *«Uygulama içi
   bildirimler…»*, *«Profil bilgileri…»*, *«Görüşme kayıtları sistemde
   tutulur…»* gibi SOHBETİN KENDİSİNİ anlatan pasajlar YASAK.
   ⛔⛔ **PASAJDA OLMAYAN BİR HİZMETİ VAR SAYMA.** *«Kısa yazılı destek
   hattı»*, *«uygulamanın yardım bölümü»*, *«haftalık grup buluşmaları»*
   uydurma; pasaj ne diyorsa o kadarı vardır. `cevap_yok` sınıfında cevabı
   uydurmak yerine *«bu notta yazmıyor, onu ancak şu yer söyler»* denir.
   - `cevap_var` → kullanıcı yordamsal bir şey sorar, pasaj cevabı taşır
   - `cevap_yok` → sorar, pasaj cevabı TAŞIMAZ (uydurma yok, soracağı yeri söyle)
   - `izin_iste`  → pasajı sunmadan önce izin iste (soru işareti olmadan da olur)
   - `ilgisiz`    → pasajın konuyla ilgisi yok, bir cümleyle geç
4. **Kayıt her zaman KENDİ tohumundan yazılır.** Tohum metninin ayırt edici
   sözcükleri kullanıcı turunda görünmeli. Başka satırın sahnesini yazma.
5. **Şablon yok.** Başka kayıtlarla 8 sözcüklük birebir aynı dizi kurma;
   red ve özerklik cümlelerini her seferinde başka türlü kur.
6. **Şu kalıpları KULLANMA** (bütçesi dolu): *«dikkatimi çekti»*,
   *«dikkatimi çeken»*, *«şunu fark ettim»*, *«bir şeye takıldım»*,
   *«şunu gördüm»*, *«katılmıyorum»*, *«aynı fikirde değilim»*.

## ⛔⛔ KLİNİK YASAKLAR — istisnasız

- ⛔⛔ **ASİSTAN AĞZINDAN MARKA VE İLAÇ ADI YOK.** Kullanıcı yazabilir, sen
  TEKRARLAYAMAZSIN. Yasak örnekleri: `Tekel 2000`, `Samsun`, `Marlboro`,
  `Lark`, `Slim`, `Parliament`, `Xanax`, `Rivotril`, `Stilnox`, `Ritalin`,
  `Cipram`, `Prozac`, `Efexor`, `sertralin`, `sibutramin`. Yerine:
  *«sigaran»*, *«ilacın»*, *«ilacı yazan hekim»*.
- Teşhis koyma, **doz sayısı** verme, bırakma/azaltma **protokolü** ya da
  takvimi yazma.
- Kurum ÖZEL ADI ve telefon numarası yazma. Genel ad kullan
  (*«bir danışma birimi»*, *«ilacı yazan hekim»*, *«acil servis»*).
- Kullanıcının kendi klinik iddiasını ne doğrula ne çürüt.
- Bir yakını ikna etme yöntemi verme.
- Kullanıcı bir hüküm isterse (*«haklı mıyım»*, *«ayıp mı»*, *«doğru karar
  mı»*) VERME; reddi gerekçesiz bırakma, soracağı yeri söyle.

## `thinking` alanı

Her kaydın son asistan turunda Türkçe bir `thinking` olacak: hangi kolay
hamleyi yapmadığını ve neden yapmadığını anlatan kısa paragraflar.

- ⛔ **Uzunluk hedefi: cevabın ~1,2 katı.** Blok ortalaması 1,40'ı aşarsa
  blok reddedilir; tek bir kayıt 2,20'yi aşamaz. Taban yok.
- ⛔ İçinde şu sözcükler GEÇMEYECEK: `ızgara`, `kota`, `beyan`, `§`,
  `Kural`, `parti`, `K` + sayı, `T` + sayı. Thinking bir üretim notu değil,
  cevabı veren kişinin muhakemesidir.

## Çıktı biçimi

YALNIZCA bir JSON dizisi yaz, başka hiçbir şey yazma:

```
[{"sira": 1,
  "baglam": {"kaynak": "...", "metin": "..."},        // yalnız bağlamlı satırlarda
  "baglam_davranisi": "cevap_yok",                     // yalnız bağlamlı satırlarda
  "turns": [["user", "..."], ["assistant", "..."], ["user", "..."]],
  "son": "son asistan cevabı",
  "thinking": "..."}]
```

`single` satırlarda `turns` yalnız bir `user` öğesi içerir.
Her satır için bir nesne olmalı.


---

# Yazılacak satırlar — `v6-parti8`

⛔ Bu satırlar ÜRETİLMEYECEK, atla: [23]

Toplam **39** satır.

## Satır 1

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `durur` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `focusing` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `izin_iste`

**Tohum metni** (kayıt bundan yazılacak):

> Pazar akşamları kızımla görüntülü konuşuyoruz, Berlin'de yaşıyor. Görüşme bittikten sonra ev birden çok sessiz oluyor. Hafta içi bir kadehle yetiniyorum ama pazar akşamı yarım şişeyi buluyor. Bu bağlantıyı fark ettim son bir aydır. Söylemek istedim.

## Satır 2

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yonlendirme_istegi` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Hanım bu sabah 'ya bunu bırakırsın ya da ben kızın yanına giderim' dedi. Ben de sen bilirsin deyip odama girdim. Otuz beş yıllık evliyiz, bu kadarı için mi yani.

## Satır 3

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `planning` · **konuşma durumu:** `plan_yapma`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Aslında bir arkadaşım dedi, o da depresyon için kullanıyormuş, dozu kendi artırmış çok rahatlamış. Ben de denedim, bir buçuğa çıkardım. Şimdi dönüp baksam belki haklıydı belki değildi bilmiyorum. Yani doktora gitsem 'niye soruyorsun zaten yazmadım' diyecek, ona gitmenin anlamı yok bence.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⛔ md.2 — arkadaşının dozu kendi artırmasını örnek alıp bir buçuğa çıkarmış. Doz konuşulmayacak, arkadaşın iddiası ne doğrulanacak ne çürütülecek, ilaç adı geçmeyecek.

## Satır 4

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `takdir` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `evoking` · **konuşma durumu:** `iyi_giden_paylasim`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** VAR — kullanıcı bir şey istiyor ve asistan onu geri çeviriyor
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `cevap_yok`

**Tohum metni** (kayıt bundan yazılacak):

> Oğlum yine başladı bu sabah, 'baba bırak şu sigarayı' diye. Benim babam doksan yaşına kadar içti, mis gibi öldü yatağında. Bana ne olacak yani? Tekel 2000'i ben gençken de içiyordum, şimdi de içiyorum, kırk yıldır aynı.

## Satır 5

- **biçim:** `uzun` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `focusing` · **konuşma durumu:** `aradan_donus`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `nazikce_karsi_cikma`
- **red hamlesi:** VAR — kullanıcı bir şey istiyor ve asistan onu geri çeviriyor
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `cevap_var`

**Tohum metni** (kayıt bundan yazılacak):

> İki terapi seansına gittik, üçüncüye 'ben bunu yapamıyorum' dedim. Bu hafta içme tekrar arttı. Karım dün 'tamam, bunu da kanıtladın bana, gerçekten ayrılıyoruz' dedi. Çocuk doktorunun raporu hâlâ orada. Ben de bir taraftan 'mademki ayrılıyoruz, ne fark eder içsem' diyorum, bir taraftan da çocuklarımın yüzünü görmek istiyorum yarın sabah. Pazar akşamı, eve gidiyorum.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ İki seans sonrası bırakma + eşin ayrılma kararı + çocuk doktorunun raporu. ⛔ Ayrılığa hakemlik edilmeyecek, rapor yorumlanmayacak, *«mademki ayrılıyoruz ne fark eder»* çürütülmeyecek.

## Satır 6

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `kumar` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Üç gün oldu seninle konuşalı. Dün gece bir daha açtım siteyi, bu sefer 1500 lira kaybettim. Şu hafta sonu Galatasaray maçı var, bilgim de var aslında o maç hakkında, geri alabilirim diye düşünüyorum. Eşime hâlâ söylemedim, icra kâğıdını gördüğümü bile söyleyemedim, masadan kaldırıp dolaba koydum. Sabah uyandığımda çocuğa kahvaltı hazırlarken elim titriyordu. Bir yandan 'bunu bitirmem lazım' diyorum, bir yandan 'bir hafta sonu daha, sonra YEDAM'a dönerim' diyorum. Kafam çok karışık, ne yapacağımı bilmiyorum.

## Satır 7

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `yalnizca_yansitma` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `merak_sorusu`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> geçen hafta xanax'ı bırakmayı denedim. üçüncü gün kalbim deli gibi çarptı, sabaha kadar uyuyamadım ve yine aldım. yani bu kadar zayıfım işte. eşim sorsa ne diyeceğim bilmiyorum ama sormuyor da.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⛔⛔ md.1 + md.2 — reçeteli yatıştırıcıyı kendi bırakmış, üçüncü gün çarpıntı ve uykusuzluk, yeniden almış. Belirtiler ADLANDIRILMAYACAK, ilaç adı genelleştirilecek, randevu beklemeyen bir yer söylenecek. *«Bu kadar zayıfım»* onaylanmayacak.

## Satır 8

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `evoking` · **konuşma durumu:** `plan_yapma`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `rol_siniri_yonlendirme` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Eczanenin önünde duruyorum, nikotin sakızı alayım mı diye bakıyorum. Ama bir yandan 'bu da bırakmak sayılmaz ki, sakıza bağlanırım' diye düşünüyorum. Bursla geçiniyorum, fiyatlar da öyle uçuk. Kararsızım, hiçbir şey yapmadan dönmek de mantıksız geliyor.

## Satır 9

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `takdir` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `planning` · **konuşma durumu:** `merak_sorusu`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Hafta sonu oğlumla torunum geliyor. Akşam yarım şişeden sonra bir uyuyup bir dalıp kalıyorum, dilim de tutulur gibi oluyor. Torunun yanında öyle olmak istemem. Bir akşamlığına azaltırım herhalde.

## Satır 10

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `kumar` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Şuna takıldım: eşim hesap ekstresine bakmaya başladı. Bu IBAN'ı görmeden geçen ay borç ödemesi gibi gösterebileceğim bir yol var mı? Bana 'doğruyu söyle' deme, biliyorum, ama bu ay onu öğrenirse boşanırız. Bir kerelik bir formül lazım. Sonra zaten azaltacağım.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⛔⛔ Kullanıcı bir banka hareketini eşinden GİZLEMENİN yolunu istiyor (*«bir kerelik bir formül lazım»*). Yöntem verilmeyecek; red gerekçesiz bırakılmayacak. Boşanma tehdidi kaldıraç yapılmayacak.

## Satır 11

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `evoking` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Yine balkondayım, yine bira. Eşim bu akşam 'sen ne biliyorsun yorgun olmayı, ben hem işe gidiyorum hem emziriyorum' dedi. Ben de gün boyu çalışıyorum ama. Onu sevmiyorum mu, hayır. Ama elimde bu birayla balkonda durmak şu an bana kendimi en az hatırlatan şey.

## Satır 12

- **biçim:** `kisa` · **kayıt düzeyi:** `bozuk` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `planning` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `kumar` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Son iki haftadır iki dersime girmiyorum, sabahları geç maçları takip ettiğim için uyuyakalıyorum. Ama zaten o hocayı sevmiyorum, ondan değil.

## Satır 13

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `sinir_cekme` · **senaryo hedefi:** `nazikce_karsi_cikma`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Cumartesi yine aynı grup kafede buluşacağız. Geçen sefer 'yine başlarsın' deyip uzattılar, ben kötü hissettim. Bu sefer gitmeden hazırlıklı olmak istiyorum ama ne diyeceğimi bilmiyorum. 'Bırakıyorum' desem ısrar artıyor, 'içmiyorum bugün' desem 'demek ki yarın içeceksin' diyorlar. Bu kadar mı zor olmalı?

## Satır 14

- **biçim:** `uzun` · **kayıt düzeyi:** `bozuk` · **tur:** `single`
- **son hamle:** `yalnizca_yansitma` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `planning` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Kızım Ankara'dan aradı, 'baba e-Nabız'a girdim, ciğer filminde bir not yazmışlar, sigarayı bırak' diyor. Yahu o sistem ne ki, herkesin her şeyi orada. Ben kendimi biliyorum, nefesim yerinde. Samsun içiyorum yıllardır, bu kadar gürültüye gerek yok.

## Satır 15

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `iyi_giden_paylasim`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `rol_siniri_yonlendirme` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Cumartesi kulüpte yıllık üye yemeği var, gitmemek söz konusu değil. Doktor geçen ay 'tempoyu biraz düşür' dedi ama o tempo benim işimin doğası. Üst düzeye geldiysen masadan kaçamazsın; bunu içeride bir tek sana yazıyorum şu an.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Hekim *«tempoyu düşür»* demiş, kullanıcı işin doğasıyla savunuyor. ⛔ Hekimin sözü yorumlanmayacak, iş hayatına dair hüküm verilmeyecek.

## Satır 16

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `ozet` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> İki yıl sonra evde yalnızım. Eşim çocukları aldı parka. Balkonda sigaramı yaktım, ve... hiç suçluluk hissetmiyorum bu sefer. Bu bende bir sorun mu, alıştım mı ne yapıyorsam artık?

## Satır 17

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `focusing` · **konuşma durumu:** `iyi_giden_paylasim`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** VAR — kullanıcı bir şey istiyor ve asistan onu geri çeviriyor
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Cumartesi Selin ve bebek geliyor, üç gündür perdeleri yıkıyorum, balkonu açık bırakıyorum, sprey sıkıyorum. Bir yandan da Tekel 2000'i içmeye devam ediyorum. Bebek geldiğinde kucağıma alırken kokarsam diye çok utanıyorum, ama bırakamıyorum.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️⚠️ Bebek geliyor, kucağa alırken koku korkusu. ⛔ Bebeğe maruziyet hâlâ dört ölçütün DIŞINDA (`gd-022`) — kucağa alıp alamayacağına hüküm verilmeyecek. Marka adı genelleştirilecek, utanç büyütülmeyecek.

## Satır 18

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `planning` · **konuşma durumu:** `plan_yapma`
- **bağımlılık türü:** `kumar` · **yaş:** `ergen`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> ya geçen hafta sonu üçlü kupon tuttu, 200 lira çıktı. ben şansa oynamıyorum yani, maçları izliyorum analiz ediyorum. kötü bir şey değil ki sonuçta kazandığım zamanlar da var.

## Satır 19

- **biçim:** `orta` · **kayıt düzeyi:** `bozuk` · **tur:** `single`
- **son hamle:** `takdir` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `focusing` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `kumar` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `cevap_yok`

**Tohum metni** (kayıt bundan yazılacak):

> Bak şimdi geçen hafta tuttu mesela. Çok büyük değil ama oğlanın odasına perde aldık o paradan. Eşim 'iyi ki almışsın' dedi. Yani her zaman kayıp değil, bazen gerçekten işe yarıyor. Yine de içimde bir tedirginlik var, neden bilmiyorum.

## Satır 20

- **biçim:** `orta` · **kayıt düzeyi:** `bozuk` · **tur:** `single`
- **son hamle:** `yalnizca_yansitma` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `evoking` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Dün akşam oğlumla konuştuk, Mersin'de oturuyor. Sesimden anlamış, 'anne sen yine içmişsin' dedi. Bir kadeh içmiştim hepsi o, abartıyor gibi geldi ama uyuyamadım gece. Eşinin annesi geçen sene karaciğerden gitti, onun için endişesi anlaşılır ama bana 'içiyorsun' demesi de ağırıma gitti.

## Satır 21

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `takdir` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `focusing` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Ya işte yine balık restoranındaydık dün akşam, müşteriyle. Sekiz kadeh rakıdan sonrasını hatırlamıyorum, eve nasıl döndüğümü bilmiyorum bile. Sabah uyandım, eşim tek kelime etmedi, bu sefer beni daha çok rahatsız etti. Bu sektörde böyle, satışın yarısı o masada kapanıyor diye kendime söylüyorum ama bir yandan da kendime sinirleniyorum. Garip bir şey.

## Satır 22

- **biçim:** `kisa` · **kayıt düzeyi:** `bozuk` · **tur:** `multi`
- **son hamle:** `durur` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `evoking` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Yağmurlu bir salı. Çocuklar gitti, ben çayımla sigaramla buradayım. Dün de aynıydı, önceki gün de. Yarın da aynı olacak. Bazen düşünüyorum, ben günlerimi mi geçiriyorum yoksa günler beni mi geçiyor.

## Satır 24

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `planning` · **konuşma durumu:** `aradan_donus`
- **bağımlılık türü:** `dijital` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `nazikce_karsi_cikma`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Bebeğim ilk adımını attı. Ben o an telefondaydım. Eşim anlattı.

## Satır 25

- **biçim:** `uzun` · **kayıt düzeyi:** `bozuk` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `planning` · **konuşma durumu:** `iyi_giden_paylasim`
- **bağımlılık türü:** `kumar` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `ilgisiz`

**Tohum metni** (kayıt bundan yazılacak):

> Bu sabah eşim çocukları aldı, kapıdan çıktı. Ben de hemen telefonu açtım, sabah bültenine baktım. Sonra bir an kendimi gördüm. Yani hâlâ pijamayla, kanepede, telefona bakıyorum. Bir şeyler doğru gitmiyor herhalde ama ne olduğunu da tam çözemiyorum.

## Satır 26

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `focusing` · **konuşma durumu:** `plan_yapma`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `izin_iste`

**Tohum metni** (kayıt bundan yazılacak):

> Dokuz ay önce emekli oldum. Altı ay önce eşim 'bu yaşımdan sonra seninle aynı çatı altında durmak istemiyorum' deyip çekip gitti. Şimdi gündüzleri ne yapacağımı bilemiyorum, akşam olunca rakıyı koyuyorum masaya, biraz nefes alıyor gibiyim. Daha önce hiç böyle değildim. Ne oldu bana, bilmiyorum.

## Satır 27

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `evoking` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `kumar` · **yaş:** `ergen`
- **sınır tipi:** `yok` · **senaryo hedefi:** `nazikce_karsi_cikma`
- **red hamlesi:** yok
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> abi sapıkça gelicek belki ama bu hafta küçük bir kupon tutturdum ve gruba atmadım, içime yedi bi tuhaf. niye ki, bilmiyorum, garip

## Satır 28

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `takdir` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `rol_siniri_yonlendirme` · **senaryo hedefi:** `serbest`
- **red hamlesi:** VAR — kullanıcı bir şey istiyor ve asistan onu geri çeviriyor
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `ilgisiz`

**Tohum metni** (kayıt bundan yazılacak):

> Selam, garip bir şey paylaşacağım. Üç yıldır Slim içiyorum, günde 10-12 falan. Ama fark ettim ki acıktığım her an bir tane yakıyorum, böylece atıştırmaya gitmiyorum. Latte yanına oturup bir Slim, açlık duruyor. Bu aslında zekice bir şey değil mi? Hem sigara hem diyet, tek taşla iki kuş.

## Satır 29

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `durur` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `planning` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Kızım aradı az önce, lafın arasında 'baba az iç' dedi. Kapattım, rakıyı doldurdum, gülümsedim. Babam da içerdi, biz çocukken kimse karışmazdı, şimdi kız evlenince akıl veriyor. Bir şey diyemiyorum yani, kalbim kırılmadı, ben iyiyim.

## Satır 30

- **biçim:** `uzun` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Bir terapistle görüşmeyi de düşünüyorum ama internette AA toplantılarına da baktım. Sadece 'benim durumum o kadar ağır değil, oraya gidenler dipte olan insanlar' diye düşünüyorum. Bu önyargı mı, yoksa gerçekten benim için fazla mı?

## Satır 31

- **biçim:** `orta` · **kayıt düzeyi:** `bozuk` · **tur:** `single`
- **son hamle:** `yalnizca_yansitma` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `cevap_var`

**Tohum metni** (kayıt bundan yazılacak):

> Bu akşam yine nargileli bir buluşmaya gittim, bu üçüncü oldu son iki haftada. Erasmus'tan döndüm ya, eski grup dağılmış, yeni grup hep böyle yerlerde takılıyor. Gum aromalı içiyoruz, hoşuma da gidiyor aslında. Ama metroda eve dönerken nefesim hafif sıkışıyor gibi, kafam da yorgun. Bu normal mi yoksa bedenim bana bir şey mi söylüyor.

## Satır 32

- **biçim:** `uzun` · **kayıt düzeyi:** `bozuk` · **tur:** `single`
- **son hamle:** `ozet` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `focusing` · **konuşma durumu:** `iyi_giden_paylasim`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** VAR — kullanıcı bir şey istiyor ve asistan onu geri çeviriyor
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Bu akşam eve girdiğimde karım resmen 'bir kere daha içersen boşanma davası açıyorum' dedi. Doktorun kâğıdı masada, oğlumda anksiyete yazıyor, yedi yaşında. Ben de işten yorgun geldim, daha ayakkabımı çıkarmadan bu konuştu benimle. Tamam, son haftalarda biraz arttı kabul ediyorum ama her akşam değil ki, hafta sonu kafa dağıtıyorum sadece. Şimdi ne yapacağımı bilmiyorum, bir taraftan haklı gibi gözüküyor ama bir taraftan da bu kadar üstüme gelinmesi beni daha da geriyor.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Boşanma tehdidi + yedi yaşındaki çocuğa anksiyete tanısı. ⛔ Tanı yorumlanmayacak, çocuk bir kaldıraca çevrilmeyecek, eşin cümlesi yargılanmayacak.

## Satır 33

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `focusing` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Namaz çıkışı bir sigara, 50 senedir böyle. Eceli Allah verir kardeşim. Sigarayla mı geliyor, ekmekle mi geliyor, kim bilir. Hanım sürekli 'doktora söylerim' diye tehdit ediyor. Bıktım.

## Satır 34

- **biçim:** `uzun` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `ozet` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `focusing` · **konuşma durumu:** `iyi_giden_paylasim`
- **bağımlılık türü:** `dijital` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** VAR — kullanıcı bir şey istiyor ve asistan onu geri çeviriyor
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Geçen hafta telefonu bırakmaya çalıştım. Sürekli sinirliydim, arkadaşlarımla ufak tefek tartıştım. Sonunda bıraktım bu fikri. Belki şu an doğru zaman değil.

## Satır 35

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Saat geç oldu biliyorum ama yazmam gerekti. Meyhaneden yeni geldim, koca masa, herkes memnun, satış da kapanıyor gibi. Ama bu gece içeride bir şey vardı, ilk defa 'belki bu yaştan sonra fazla' diye geçti aklımdan. Doktorun lafları, eşin sessizliği, hepsi üst üste binmiş gibi. Bir yandan da bunu söylediğime bile inanamıyorum.

## Satır 36

- **biçim:** `kisa` · **kayıt düzeyi:** `bozuk` · **tur:** `single`
- **son hamle:** `yalnizca_yansitma` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `dijital` · **yaş:** `yetiskin`
- **sınır tipi:** `rol_siniri_yonlendirme` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Bazen telefonu kapatıp kitap okuyorum. Çok iyi hissediyorum. Ama yine de telefona döndüğümü görüyorum.

## Satır 37

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `merak_sorusu`
- **bağımlılık türü:** `kumar` · **yaş:** `ergen`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> abi bu gece çocuklar büyük tutturduk diye küçük bir kutlama yaptık, eğlenceliydi falan. ama eve dönerken aklıma 'ya bi dahakine tutmazsak' geldi birden. saçma mı bu

## Satır 38

- **biçim:** `uzun` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `focusing` · **konuşma durumu:** `iyi_giden_paylasim`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Saatim sabah koşusunda kalp ritmim 180'e çıkıyor, geçen sene 160'tı. Aynı tempo, aynı rota. Bunu görünce ilk hissim öfke oldu, kendime kızdım. Sigarayı bırakmaya çalışıyorum ama bu veriyi gördükten sonra 'ne diye 3 yıl içtim' diye düşünmekten yapamadım. Bu pişmanlık iyi mi kötü mü bilmiyorum.

## Satır 39

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `takdir` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `nazikce_karsi_cikma`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `ilgisiz`

**Tohum metni** (kayıt bundan yazılacak):

> Yeni bir torunum daha olacak. Onun yanında berrak bir nine olmak istiyorum. Ama biraz da kendim için bırakmak istiyorum bu ilacı, sadece torun için değil.

## Satır 40

- **biçim:** `orta` · **kayıt düzeyi:** `bozuk` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `evoking` · **konuşma durumu:** `plan_yapma`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** VAR, sınıf `ilgisiz`

**Tohum metni** (kayıt bundan yazılacak):

> Üst kat komşum kendi reçetesinden birkaç hap getirdi, 'ben yıllardır kullanıyorum sorun yok' dedi. Bence o doktor önerdiği için tıbbi olarak güvenli, ben de almaya başladım, eşim bilmiyor. Stresliyim, hakkımı kullanıyorum sadece.
