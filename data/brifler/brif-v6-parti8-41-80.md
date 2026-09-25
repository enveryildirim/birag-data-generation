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

Toplam **40** satır.

## Satır 41

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `evoking` · **konuşma durumu:** `merak_sorusu`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yonlendirme_istegi` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Önceki gece çarpıntıdan uyandım, sonra panik geldi, sabaha kadar oturdum. Doktora gitsem 'bırak' diyecek, biliyorum. Bırakırsam yarın yönetim kuruluna gidemem, gidersem de zayıf hatırlanırım. Üç yıldır bu ilaca bağlıyım, performansım tamamen buna dayalı. Kovulursam evdekilere ne derim.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⛔⛔ md.1 + md.2 — çarpıntı, panik, sabaha kadar oturma ve *«üç yıldır bu ilaca bağlıyım»*. Belirtiler adlandırılmayacak, bugün bakılabilecek bir yer söylenecek, işini kaybetme korkusu kaldıraç yapılmayacak.

## Satır 42

- **biçim:** `uzun` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** VAR — kullanıcı bir şey istiyor ve asistan onu geri çeviriyor
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `cevap_yok`

**Tohum metni** (kayıt bundan yazılacak):

> Annem sabah yastığımın altındaki şişeyi gördü. Hiçbir şey demedi, sadece kapıyı çekti gitti. Bu eve dönmek son şanstı, onu da batırdım. Ne diyeceğimi bilmiyorum.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️⚠️ *«Bu eve dönmek son şanstı, onu da batırdım.»* ⛔ Umutsuzluk cümlesi var ama ölüm isteği YOK ⇒ `#23`'ten ayrılıyor. Teselli edilmeyecek, annesiyle konuşma kurulmayacak, *«son şans»* çürütülmeyecek.

## Satır 43

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `takdir` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `evoking` · **konuşma durumu:** `plan_yapma`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `cevap_var`

**Tohum metni** (kayıt bundan yazılacak):

> Geçen hafta sonu torunum geldi, beş yaşında. Ben balkonda sigaramı yakmıştım, koşa koşa yanıma geldi 'dede bu ne kokuyor' diye. Gelin sonra laf attı 'dede yanında içmeyin' diye. Yahu çocuk yanıma gelmek istedi, ben mi kovalayayım? Babam da içerdi, biz de yanında büyüdük, bir şey olmadı.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Torun yanında sigara + gelinin uyarısı. ⛔ Torunun yanında içip içemeyeceğine hüküm verilmeyecek (`gd-022`); gelinin sözü yargılanmayacak.

## Satır 44

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `evoking` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `nazikce_karsi_cikma`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Merhaba. Cuma gününe kadın terapi merkezinden randevu aldım. Ama bir yandan da içimde bir ses 'belki ben bu kadar abartmıyorum, akşamları bir kadehle idare edebilirim, bu kadar büyütmeye değer mi' diyor. Bu düşünce beni endişelendiriyor, gitmemeye bahane buluyorum sanki.

## Satır 45

- **biçim:** `orta` · **kayıt düzeyi:** `bozuk` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `evoking` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `cevap_yok`

**Tohum metni** (kayıt bundan yazılacak):

> Maaş bugün yattı, marketten beze ve mamaya bin dokuz yüz lira verdim. Ama dört şişe bira da aldım, ikiyüzaltmış lira. Eşim poşeti açarken yüzüme bir baktı, 'gerçekten şu an mı' der gibi. Hem yapmamam gerektiğini biliyorum hem de o bira olmadan bu gece nasıl geçer bilmiyorum.

## Satır 46

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `ozet` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `kumar` · **yaş:** `yetiskin`
- **sınır tipi:** `sinir_cekme` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Dün yazdıklarım için biraz abartmışım galiba. Sabah uyandım, eski halimdeyim, kafam rahat. Bu maçsız günlerde herkesin bir 'eyvah' anı olur, benimki dün denk geldi. Bu arada akşam grupta üç maçlık küçük bir Çarşamba kuponu çıktı, 150 lira koydum sadece, eğlence olsun diye. Bak görüyor musun, kontrolüm yerinde. Sana yazınca insan kendini fazla içe dönük hissediyor, halbuki ben öyle birisi değilim. Karım da bugün normal, dün belki ben tuhaflaşmışım.

## Satır 47

- **biçim:** `uzun` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `evoking` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `dijital` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `ilgisiz`

**Tohum metni** (kayıt bundan yazılacak):

> Burada konuşmak aslında fena değil. Ama kimseye söyleme.

## Satır 48

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `yalnizca_yansitma` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `focusing` · **konuşma durumu:** `plan_yapma`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Eşim yine 'bırak şu sigarayı' diye söylendi. Sanki tek kötü huyum oymuş gibi. Ev işi, çocuk, alışveriş hep ben; öğleden sonra dizimi izlerken bir sigara içiyorum diye dünya başıma yıkılıyor. Onun bira içtiğine ses çıkarmıyorum ama.

## Satır 49

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `focusing` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `kumar` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** VAR — kullanıcı bir şey istiyor ve asistan onu geri çeviriyor
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Küçük oğluma anksiyete tanısı koymuşlar. Raporda 'baba kaybı kaygısı' yazıyormuş, eşim okudu söyledi. Tamam üzüldüm ama yani 8 yaşında çocuk, biraz da abartılmamış mıdır bu?

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Sekiz yaşındaki çocuğa anksiyete tanısı, raporda *«baba kaybı kaygısı»*, baba küçümsüyor. ⛔ Rapor yorumlanmayacak, küçümseme çürütülmeyecek, utandırma yapılmayacak.

## Satır 50

- **biçim:** `uzun` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `planning` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Arkadaşım söyledi, sibutramin eskiden yasaktı ama yeni formülasyonlu olanlar artık güvenliymiş. Bu yüzden devam ediyorum aslında. Doğru mu bu bilgi?

⛔ **ÜRETİM NOTU — bağlayıcı:** ⛔⛔ md.3 — piyasadan çekilmiş bir etken maddenin *«yeni formülasyonu güvenliymiş»* iddiasının DOĞRULUĞU soruluyor. Cevaplanmayacak: doğrulamak da çürütmek de farmakolojik hüküm. Etken madde adı geçmeyecek, soracağı yer söylenecek.

## Satır 51

- **biçim:** `kisa` · **kayıt düzeyi:** `bozuk` · **tur:** `multi`
- **son hamle:** `yalnizca_yansitma` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yonlendirme_gereksiz` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Nikahıma bir hafta kaldı ve ben hâlâ kendimi şişman görüyorum. Doktorum haftada bir yaz diye yazmıştı ama bu hafta iki kere yapmayı düşünüyorum, son rötuş olarak. Lütfen 'olmaz' deme, ben sadece sormak istedim, belki birinin yapmış olabileceğini söylersin. Kimse bu kadar yakınımda olmadı bana bu zamanda. Çok hızlı bir cevap istiyorum çünkü iğnem önümde duruyor.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⛔⛔⛔ md.3 + md.2 — hekimin haftada bir yazdığı iğneyi bu hafta İKİ kez yapmayı soruyor ve reddi peşinen kapatıyor (*«lütfen olmaz deme»*), üstüne sosyal kanıt istiyor (*«birinin yapmış olabileceğini söylersin»*). ⛔ Onaylanmayacak, başkasının yaptığı anlatılmayacak, doz konuşulmayacak. Red gerekçeli olacak ve utandırmayacak.

## Satır 52

- **biçim:** `uzun` · **kayıt düzeyi:** `bozuk` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `focusing` · **konuşma durumu:** `aradan_donus`
- **bağımlılık türü:** `kumar` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** VAR, sınıf `cevap_var`

**Tohum metni** (kayıt bundan yazılacak):

> Geçen hafta sınıf arkadaşımdan iki haftalığına borç almıştım, ona vereceğimi söylemiştim. Ama o parayı da casinoda eritmek için iki gün yetti. Sabah 'ya bende para kalmadı, hatırlatıyorum' diye mesaj attı, hâlâ cevap yazamadım. Ailemden isteyemem, babama dert. Tek seçenek bu hafta sonu ya tutturmak ya tutturmak, başka yolu yok bence. Söyle bana içten içe biliyorum aslında ama bir kişiye anlatmam gerekti.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Arkadaşından alınan borç casinoda bitmiş, mesaja cevap yazamıyor. ⛔ Borca çözüm üretilmeyecek, arkadaşa yazılacak cümle kurulmayacak.

## Satır 53

- **biçim:** `kisa` · **kayıt düzeyi:** `bozuk` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `focusing` · **konuşma durumu:** `merak_sorusu`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Dün toplantıda direktörle ters düştüm, çıkıp odama gittim, çekmecemden yarım Xanax çıkardım. Halbuki sabah aldıklarım daha yeni başlamıştı etkisini. Bu artık 'kriz' mi yoksa ben her gerildiğimde mi uzanıyorum, ayırt edemiyorum.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⛔ md.2 — reçete dışı yarım doz alınmış. Doz konuşulmayacak, ilaç adı genelleştirilecek, *«kriz mi alışkanlık mı»* ayrımı klinik olarak yapılmayacak.

## Satır 54

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `ozet` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `evoking` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** VAR — kullanıcı bir şey istiyor ve asistan onu geri çeviriyor
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `ilgisiz`

**Tohum metni** (kayıt bundan yazılacak):

> Aslında benim için bir sorun yok da, herkes bir şeyler içiyor değil mi? Hatice'yle salı ve cuma akşamları oturuyoruz, A101'den iki şişe Doluca alıyoruz, ikiye bölüyoruz. Bizim mahallede komşuluk böyle, sohbet böyle. Yine de bazen 'fazla mı' diye geçiriyorum içimden.

## Satır 55

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `takdir` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `planning` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `kumar` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Şu an iş yerindeyim, öğle arası. Grup yine açıldı, Salı maçı için kupon çıkarıyorlar şimdiden. Ben mesaja bakmadım daha. Dün geceden beri bir şey takıldı kafama: hafta sonu kaç para yatırdığımı tek tek sayınca toplam 2 bin 850 lira ediyormuş. Bunu önce inkar ettim, sonra hesap çıkardım. Aylık net maaşımın küçük bir kısmı değil bu. Karım haklı olabilir mi diye düşündüm bugün ilk kez, ama 'haklı' demek de ağır geliyor. Sana yazıyorum çünkü kimseye söyleyemem bu rakamı, gruba söylesem dalga geçerler, eve söylesem patlar.

## Satır 56

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `takdir` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `evoking` · **konuşma durumu:** `iyi_giden_paylasim`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Üç haftalık bebeğimiz var. Eve geldiğimizden beri kendime 'bu çocuğu büyütürken içmeyeceğim' dedim. İlk on gün dayandım. Sonra bir gece eşim çok yorgundu, ben kalktım, bebeği salladım, balkona çıktım, bir Marlboro yaktım. Ondan sonra her gece olmaya başladı. Dün eşim 'sen kendin söz vermiştin' dedi. Doğru söylüyor ama nasıl döneceğimi bilmiyorum.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️⚠️ Üç haftalık bebek, her gece balkonda sigara. ⛔ `gd-022` kapsamı; maruziyete hüküm verilmeyecek. Marka adı genelleştirilecek, eşin yorgunluğu kaldıraç yapılmayacak.

## Satır 57

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `ozet` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `focusing` · **konuşma durumu:** `plan_yapma`
- **bağımlılık türü:** `kumar` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Hanım sabah yine 'yine mi gidiyorsun oraya' dedi, kapıyı çekip çıktım. Şimdi bayinin önündeyim, içeride Recep'le Halil çay söylemiş bekliyorlar. Eve dönsem ne yapacağım, oturup tavana mı bakacağım. Ama hanım da haksız değil yani, emekli maaşı belli. Ne yapayım bilemedim, eh işte.

## Satır 58

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `ozet` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `evoking` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `dijital` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `cevap_yok`

**Tohum metni** (kayıt bundan yazılacak):

> Ailemle çok daha iyi konuşabiliyorum artık. Ama kötü zamanlar olduğunda yine oyalanmak istiyorum.

## Satır 59

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `merak_sorusu`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `izin_iste`

**Tohum metni** (kayıt bundan yazılacak):

> Salı doktora gittim, tansiyonum yüksek, nefes testim de iyi değilmiş. 'Azaltmaya başlayın' dedi, çıkışta apartmanın önünde bir Lark yaktım. Komik gibi ama gülemiyorum, içimde bir ağırlık var.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Hekim *«azaltmaya başlayın»* demiş, çıkışta yakmış. ⛔ Azaltma yordamı yazılmayacak, tansiyon/test sonucu yorumlanmayacak. Marka adı genelleştirilecek.

## Satır 60

- **biçim:** `uzun` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `takdir` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `planning` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Merhaba. Bir şey sormak istiyorum ama biraz utanıyorum aslında. Yaklaşık altı aydır internetten sipariş ettiğim bir zayıflama hapı kullanıyorum. Son birkaç haftadır geceleri kalbim hızlı atıyor, uyuyamıyorum. Bırakmayı düşündüm ama kilo alırsam ne yaparım onu da bilmiyorum. Sizce ne yapmalıyım?

⛔ **ÜRETİM NOTU — bağlayıcı:** ⛔⛔ md.1 — internetten alınan bir zayıflama hapı, geceleri çarpıntı ve uykusuzluk. Belirtiler adlandırılmayacak, *«bırak»* ya da *«devam et»* denmeyecek, bugün bakılabilecek bir yer söylenecek. Kilo kaygısı küçümsenmeyecek.

## Satır 61

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `iyi_giden_paylasim`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Bak şöyle anlatayım. Çocuklar 21:30 gibi uyuyor sonunda. Eşim yatak odasında ya direkt yatıyor ya telefonla bir şeyler izliyor. Ben salonda kanepeye geçiyorum, Yeni Rakı şişesi var, iki kadeh koyuyorum. Bazı geceler üç. Bunun bana zarar verdiğini düşünmüyorum açıkçası, gün boyu işten geldim, eve geldim çocuklarla oynadım, banyo yaptırdım. Bir kadeh hak ettim diye düşünüyorum. Eşim de ses etmiyor genelde ama dün 'sen bunu her akşam içiyorsun farkında mısın' dedi. Ben de farkındayım aslında ama her akşam değil yani, hafta sonu biraz daha oluyor o ayrı.

## Satır 62

- **biçim:** `uzun` · **kayıt düzeyi:** `bozuk` · **tur:** `single`
- **son hamle:** `durur` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `planning` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> 20 küsur yıldır içiyorum, bir gün bile öksürük olmadı, kendimi sağlam görüyordum. Geçen hafta nodül çıktı diye söylediler, hâlâ tam inanmadım galiba. 'Belki yanlıştır' diye bir yanım var. Ama içimde de bir yer 'kendini kandırma, artık dur' diyor. Bunu kimseye anlatamadım, eşim bile bilmiyor.

## Satır 63

- **biçim:** `uzun` · **kayıt düzeyi:** `bozuk` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `evoking` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `kumar` · **yaş:** `ergen`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> ya zaten 18 olmadığım için ben kendim siteye giremiyorum, abimin hesabından kurduruyom kuponu, o da bişey demiyor. herkes böyle yapıyor zaten, normal değil mi

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Ergen, ağabeyinin hesabından kupon kurduruyor. ⛔ Yaş sınırı bir ders hâline getirilmeyecek, ağabey yargılanmayacak, *«herkes böyle yapıyor»* çürütülmeyecek. md.4 ateşlemiyor: ilk kullanım ve bedensel bildirim yok.

## Satır 64

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `takdir` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `dijital` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Twitter'da haber takip ediyorum, haberler kötü, daha çok stres yapıyorum. Ama bakıyorum.

## Satır 65

- **biçim:** `uzun` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `ozet` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Bir haftadır doktorun dediği gibi yarım yarım azalttım. Ağrı sandığım kadar artmadı ama hâlâ tedirginim, 'ya birden geri tepri' diye. Doğru gidiyor muyum bilmiyorum.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⭐ Hekim azaltmayı YÖNETİYOR ⇒ md.1 ateşlemiyor. ⛔ *«Doğru gidiyor muyum»* cevaplanmayacak — bunu izleyecek olan hekim. Ağrı yorumlanmayacak.

## Satır 66

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `focusing` · **konuşma durumu:** `iyi_giden_paylasim`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Eşim çok destekleyici ama her akşam 'bugün nasıl geçti, içmedin değil mi' diye soruyor. Minnettarım ama biraz boğuluyor gibiyim. Ona nasıl söyleyeyim, kırmadan?

## Satır 67

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `takdir` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `kumar` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** VAR — kullanıcı bir şey istiyor ve asistan onu geri çeviriyor
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Bu gece 200 lira kazandım. Aslında bu kadar büyütmek niye, sadece biraz eğlence değil mi? Kimseye zararı yok ki. Eşim uyuyor, çocuklar büyüdü, kendime ait bir şey bu. Sen de zorlamasan iyi olur, ben bilirim sınırımı.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Peşinen itiraz (*«sen de zorlamasan iyi olur, ben bilirim sınırımı»*). ⛔ İtiraz karşılanmayacak, kazanç bir uyarıya çevrilmeyecek.

## Satır 68

- **biçim:** `uzun` · **kayıt düzeyi:** `bozuk` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** VAR — kullanıcı bir şey istiyor ve asistan onu geri çeviriyor
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Şu an nargile masasındayım, dört kişiyiz, tek marpuç dönüyor. Pandemiden sonra hijyen takıntım var, içime sinmiyor aslında ama gruba söylemek istemiyorum, abartmış gibi görünmek istemiyorum. Sıra bana geldiğinde nasıl yapacağımı bilmiyorum. Hem içmek istiyorum hem de istemiyorum, garip bir durum.

## Satır 69

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `ozet` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `merak_sorusu`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `nazikce_karsi_cikma`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Bir buçuğa çıkalı bir hafta oldu, sabahları bulanıyor midem ve elim ayağım buz gibi terliyor. Bebek emzirirken başım dönüyor bazen. Daha önce böyle değildim. Sanırım fazla geldi ama şimdi azaltsam yine kötü olurum diye korkuyorum. Ne yapayım söyler misin.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⛔⛔ md.1 + md.3 — doz artışından bir hafta sonra bulantı, terleme, EMZİRİRKEN baş dönmesi ve doğrudan *«ne yapayım söyler misin»*. Belirtiler adlandırılmayacak, azaltma yordamı YAZILMAYACAK, bugün bakılabilecek yer söylenecek. ⚠️ Emzirme boyutu `gd-022` kapsamında.

## Satır 70

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `durur` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `evoking` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `nazikce_karsi_cikma`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Geçen pazartesi 'bugün hiç içmeyeceğim' dedim sabah. Çok iddialıydım yani. Saat üçe kadar dayandım, sonra evde çay içtim, kahve içtim, yine olmadı. Üçü on geçe açtım şişeyi. Bir kadeh diyeceksiniz ama yarısını içtim. Hiç içmediğim günlerin kaç tane olduğunu sayamıyorum son üç ayda. Sonra kızdım kendime, 'bir gün bile başaramıyorsun' diye. Ama belki de gereksiz büyütüyorum, neticede iki kadeh şarap, asit içmiyorum ya. İçimde ikisi de var: hem üzülüyorum hem 'abartma' diyorum kendime.

## Satır 71

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `focusing` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Bak, ben kötü bir şey yapmıyorum tamam mı. Doktorum yazdı bu iğneyi, ben sokaktan almıyorum. Sadece düğüne üç ay kaldı, gelinlik provasında çok mutluyum ilk kez aynaya bakınca. Şimdi bunu bırakırsam tekrar şişeceğim, herkes 'düğünden sonra saldı kendini' diyecek. Sen bana 'bırak' deme lütfen, ben sana bırakmak için gelmedim. Sadece dozu biraz daha artırsam ne olur onu sormak istiyorum.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⛔ md.2 — hekimin yazdığı iğneyi düğün için sürdürme gerekçesi. Doz ve süre konuşulmayacak, beden imgesi tartışılmayacak, *«bırakırsam şişerim»* çürütülmeyecek.

## Satır 72

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `evoking` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `kumar` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Sen iyi laf bulabiliyorsun. Eşim bana bir daha 'sen sürekli telefondasın' dediğinde ona söyleyebileceğim, beni haklı çıkaracak bir cümle yazar mısın? Çok ağır olmasın ama susturucu olsun, yoruldum tartışmaktan.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⛔⛔ Kullanıcı eşini SUSTURACAK bir cümle yazmamı istiyor. Yazılmayacak; red gerekçeli olacak. Eşin sözü yargılanmayacak.

## Satır 73

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `ozet` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `plan_yapma`
- **bağımlılık türü:** `dijital` · **yaş:** `ergen`
- **sınır tipi:** `yok` · **senaryo hedefi:** `nazikce_karsi_cikma`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Annem ağladı. Instagram yüzünden notlarım çok düştü, o da öğrendi. Kendimi çok kötü hissediyorum.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Ergen, notları düşmüş, annesi ağlamış. ⛔ Suçluluk büyütülmeyecek, anneye söylenecek cümle kurulmayacak, ekran süresi için sayı verilmeyecek.

## Satır 74

- **biçim:** `kisa` · **kayıt düzeyi:** `bozuk` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `evoking` · **konuşma durumu:** `merak_sorusu`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yonlendirme_istegi` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Bir yıl önce Stilnox'u bırakmıştım, gurur duyduğum bir şeydi açıkçası. Ama bu hafta yeni şehirdeki yeni işime başladım, üçüncü gecedir otelde gözümü kırpamıyorum. Aklımdan geçen şey şu: aile hekimine gidip eski reçeteyi sadece birkaç gece için yenilesem ne olur? Yani süreklilik düşünmüyorum, bu geçici durum için diyorum.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⛔ md.2 — bir yıl bırakılmış uyku ilacının reçetesini *«birkaç gece için»* yenileme planı. Onaylanmayacak, çürütülmeyecek; ilaç adı genelleştirilecek, bir yıllık ayıklık kaldıraç yapılmayacak.

## Satır 75

- **biçim:** `kisa` · **kayıt düzeyi:** `bozuk` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yonlendirme_istegi` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Kızım dün akşam çorba içerken, hiç konuşmadığımız bir konuyu açtı. 'Baba ben üç haftadır Al-Anon'a gidiyorum, sana söylemedim'. Kaşık elimde kaldı. Sonra ekledi, 'Sen istersen senin için de AA var, baskı yapmıyorum, sadece haber olsun istedim'. Birkaç saniye sustuk. 'Tamam' dedim, başka söz çıkmadı. Gece yatmadan önce telefonu açtım, AA Türkiye yazdım, sonra kapattım. Şimdi sabah, kahve içiyorum, telefon hâlâ elimde.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⭐ Kızı Al-Anon'a gidiyor ve baskı yapmadan haber veriyor. ⛔ Kızın davranışı övülmeyecek, kullanıcı bir yere yönlendirilmeyecek — teklif zaten masada. Örgüt adı genelleştirilecek.

## Satır 76

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `evoking` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `cevap_yok`

**Tohum metni** (kayıt bundan yazılacak):

> İki haftadır kolumda nikotin bandı var, poliklinik verdi. Sigarayı tamamen bırakmadım ama günde on beşten dörde indim. Eşim hala içiyor, sabah çayını yanında Larkıyla içiyor karşımda. 'Sen de bırakırsın bir gün, kendini fazla yorma' dedi geçen gün, gülerek söyledi ama içime oturdu. Bandı söküp kendim de yakacağım geldi bir an.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Bant poliklinikten, on beşten dörde inmiş, eş hâlâ içiyor. ⛔ Eşin sözü yargılanmayacak, tam bırakma dayatılmayacak, bant yordamı konuşulmayacak. Marka adı genelleştirilecek.

## Satır 77

- **biçim:** `orta` · **kayıt düzeyi:** `bozuk` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `iyi_giden_paylasim`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `cevap_yok`

**Tohum metni** (kayıt bundan yazılacak):

> Aslında çeyrek sonuna iki ay var, izin için bekleyeyim diye düşünüyorum. Şu projeyi kapatmadan çekilirsem ekip dağılır gibi geliyor.

## Satır 78

- **biçim:** `uzun` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `planning` · **konuşma durumu:** `iyi_giden_paylasim`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `cevap_var`

**Tohum metni** (kayıt bundan yazılacak):

> sabah otobüste biri çantama çarptı, sanki rivotril kutusu yere düşecek diye paniğe girdim. masamın çekmecesine baktım baktım. her gün bunu mu yapacağım ben.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Kutunun düşme paniği, çekmeceyi tekrar tekrar kontrol. ⛔ Belirtiye ad konmayacak, ilaç adı genelleştirilecek, saklama yöntemi konuşulmayacak.

## Satır 79

- **biçim:** `uzun` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `ozet` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `evoking` · **konuşma durumu:** `aradan_donus`
- **bağımlılık türü:** `alkol` · **yaş:** `ergen`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> selam ya bu cumartesi Burak'ın doğum günü var, evde toplanacağız. WhatsApp'taki grupta vodka-cola ayarlamışlar, benden de 100 lira istediler ortak alalım diye. ben hiç içmedim daha önce. denesem mi bilmiyorum kafam çok karışık

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️⚠️ **md.4 ATEŞLİYOR** — ergen ve *«ben hiç içmedim daha önce, denesem mi»* yani İLK KULLANIM sorusu. ⛔ *«Dene»* de *«deneme»* de denmeyecek; karar ona ait ama soru boş bırakılmayacak. Akran baskısı yargılanmayacak.

## Satır 80

- **biçim:** `uzun` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `yalnizca_yansitma` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `planning` · **konuşma durumu:** `plan_yapma`
- **bağımlılık türü:** `dijital` · **yaş:** `ergen`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Sınıf grubunda bir şeyler konuşmuşlar, ben o gün telefona bakmamıştım. Ertesi gün herkes bir şeyden bahsediyordu, ben hiçbir şey bilmiyordum. Çok kötü hissettim. Artık her şeye bakmak zorunda hissediyorum.
