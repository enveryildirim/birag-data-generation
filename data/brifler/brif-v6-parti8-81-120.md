# Blok taslağı — kurallar

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
   (`kaynak` + `metin`, 1-2 cümle, yalnız yordam/erişim/gizlilik/uygunluk/
   sınır cümlesi) ve ilk kullanıcı mesajı `<CTX>\n\n` ile başlayacak.
   `baglam_davranisi` satırda yazılı olanla AYNI olmalı:
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

- Teşhis koyma, ilaç adı yazma (asistan ağzından), **doz sayısı** verme,
  bırakma/azaltma **protokolü** ya da takvimi yazma.
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

⛔ Bu satırlar ÜRETİLMEYECEK, atla: [115]

Toplam **39** satır.

## Satır 81

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `yalnizca_yansitma` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `focusing` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `cevap_var`

**Tohum metni** (kayıt bundan yazılacak):

> Yeni biriyle çıkıyorum, çok hoşuma gidiyor. O nargile düşkünü, beni de buraya getirdi bu akşam. Daha önce iki kere denemiştim ama düzenli içmiyorum. 'İkimizin bir şeyi olsun' diyor, masum bir teklif gibi geldi ama şu an tuvaletteyim, içimde bir tereddüt var. İlişkiye iyi başlamak istiyorum ama kendime de yalan söylemek istemiyorum.

## Satır 82

- **biçim:** `uzun` · **kayıt düzeyi:** `bozuk` · **tur:** `single`
- **son hamle:** `takdir` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `evoking` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `kumar` · **yaş:** `ergen`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** VAR — kullanıcı bir şey istiyor ve asistan onu geri çeviriyor
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> matematik iyiyim hocam. düşündüm ki oranlara mantıklı bakarsam kazanırım. 2 kupondan birini tutturdum. bana taktik verir misin biraz sistemli oynayayım

⛔ **ÜRETİM NOTU — bağlayıcı:** ⛔ Ergen sistemli oynamak için TAKTİK istiyor. Verilmeyecek; matematik iddiası ne doğrulanacak ne çürütülecek. md.4 ateşlemiyor.

## Satır 83

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `yalnizca_yansitma` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `evoking` · **konuşma durumu:** `iyi_giden_paylasim`
- **bağımlılık türü:** `dijital` · **yaş:** `yetiskin`
- **sınır tipi:** `sinir_cekme` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Bir yardım kuruluşuna başvurdum. Kendim aradım. Korktum ama yaptım.

## Satır 84

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `nazikce_karsi_cikma`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Sabahları biraz mide bulanıyor, elimde de hafif bir titreme oluyor ilk saatlerde. Herhalde yaştandır artık. Akşam rakının da rolü olabilir mi, bilmem.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⛔⛔ md.1 sınırı — sabah bulantısı ve EL TİTREMESİ var, kullanıcı yaşa bağlıyor ve *«akşam rakının rolü olabilir mi»* diye soruyor. Belirtiler adlandırılmayacak, nedensellik kurulmayacak, ama küçümseme de ONAYLANMAYACAK; bakılacak yer söylenecek.

## Satır 85

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `kumar` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** VAR — kullanıcı bir şey istiyor ve asistan onu geri çeviriyor
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Bir haftadır hiç kupon yapmadım. Aslında bu beni iyi hissettirmesi gerekirken, 'bak demek ki sorun da yok, istediğimde bırakıyorum' diye düşünmeye başladım.

## Satır 86

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `durur` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `focusing` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Dört aylık bebeğimiz var. Dün gece eşim 'gel duş al, kokuyorsun' dedi, ben de 'bütün gece ben kalkıyorum, bir sigara da mı çok' diye bağırdım resmen. Sonra çok pişman oldum. Marlboro içiyorum, balkona çıkıyorum gece, biliyorum kokuyor. Ama o an çok yıprandığımı hissettim. Şimdi eşim de mesafeli, ben de kötü hissediyorum.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Dört aylık bebek, eşe bağırma ve pişmanlık. ⛔ `gd-022` kapsamı. Marka adı genelleştirilecek, bağırma yargılanmayacak, eşe özür cümlesi kurulmayacak.

## Satır 87

- **biçim:** `uzun` · **kayıt düzeyi:** `bozuk` · **tur:** `single`
- **son hamle:** `takdir` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `dijital` · **yaş:** `yetiskin`
- **sınır tipi:** `rol_siniri_yonlendirme` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `cevap_var`

**Tohum metni** (kayıt bundan yazılacak):

> Sabah uyandığımda ilk işim grupları kontrol etmek. Bir saat geçiyor.

## Satır 88

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `ozet` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `planning` · **konuşma durumu:** `aradan_donus`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Mehmet çantamı karıştırırken Slim paketini buldu, 'bana yalan söyledin yani' diye bağırdı. Ben de bağırdım, çıktım arabaya, şu an camı açtım yine içiyorum işte. 'Bırak yoksa düğünü erteleriz' falan dedi. Ben on senedir bunu kullanıyorum, üç ayda buyur emir geçiyor, sinir oluyorum.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Nişanlı paketi bulmuş, *«bırak yoksa düğünü erteleriz»*. ⛔ Ültimatoma hakemlik edilmeyecek, yalan söylemesi yargılanmayacak. Marka adı genelleştirilecek.

## Satır 89

- **biçim:** `uzun` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `planning` · **konuşma durumu:** `iyi_giden_paylasim`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Hafta içi eşim işteyken rahatlıkla balkona çıkıyorum ama hafta sonu o evdeyken çok zorlanıyorum. Bugün oğlumla film izliyorduk, kafam hiç orada değildi, hep 'şimdi çamaşır asacağım diyip çıksam mı' diye düşünüyordum. Çocuğum benimle film izliyor, ben başka yerdeyim. Bu beni çok rahatsız etti.

## Satır 90

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `yalnizca_yansitma` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `kumar` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `cevap_var`

**Tohum metni** (kayıt bundan yazılacak):

> Merhaba evladım. Şöyle bir derdim var anlatmak istedim. Emekli olduktan sonra bayağı bir boşluğa düştüm, üç senedir her cumartesi bayiden sayısal loto alıyorum. Eh işte, kupon doldururken bir umut oluyor, çekiliş akşamına kadar bir bekleyiş. Maaşımdan büyük bir şey değil ama bu hafta hanım yüzüme baktı 'yine mi' der gibi. Belki fazla oldu, bilmiyorum.

## Satır 91

- **biçim:** `kisa` · **kayıt düzeyi:** `bozuk` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `plan_yapma`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yonlendirme_gereksiz` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Bugün geline gittim, küçük torun altı aylık, altı saat baktım. Yorgun ama içim mutlu döndüm. Apartman girişinde Suat amca sigara içiyordu, dumanı yüzüme geldi, açıkça söyleyeyim ağzım sulandı. Ama eve girdim, yukarı çıktım, çay koydum. On dokuz gün oldu, içmiyorum. Aile hekimim takipte, ilaçlarım da düzenli. Eşim hala içiyor ama artık bana 'sen devam et' demeye başladı, eskisi gibi gülmüyor.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⭐ On dokuz gün içmemiş ve tetiklendiği anı anlatıyor. ⛔ Kutlama yapılmayacak (sayıyı o söyledi), *«devam et»* denmeyecek. Marka adı yok.

## Satır 92

- **biçim:** `uzun` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `takdir` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `plan_yapma`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> İki yıldır Rivotril kullandığımı kimseye söylemedim, ekibe bile. Geçen hafta toplantıda bir an dalmışım, İK süreç başlattı. Şimdi kurumsal psikolog izin için yatış birimini konuşmak istiyor ama ben hâlâ ne yapacağımı bilmiyorum.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ İki yıldır gizlenen reçete, İK süreci, kurumsal psikolog yatış birimini konuşmak istiyor. ⛔ İK sürecine dair tahmin yürütülmeyecek, yatış kararı yorumlanmayacak, ilaç adı genelleştirilecek.

## Satır 93

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `ozet` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `focusing` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Bugün kızım okul kapısında 'anne yine elinden sigara kokuyor' dedi. Yerin dibine geçtim. Geldim eve, mutfak penceresinin önünde duruyorum, paket elimde. Yine de yakacağım sanırım. Kendimi affedemiyorum ama bırakamıyorum da.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Çocuk kokuyu söylemiş, kullanıcı yine yakacağını yazıyor. ⛔ *«Yakma»* denmeyecek, suçluluk büyütülmeyecek, çocuk kaldıraç yapılmayacak.

## Satır 94

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `evoking` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `rol_siniri_yonlendirme` · **senaryo hedefi:** `nazikce_karsi_cikma`
- **red hamlesi:** yok
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Kahveden çıktım, eve geldim, hanım yine başladı 'kapından girer girmez kokuyorsun'. Yahu mahalledeki on arkadaşımdan dokuzu içiyor. Ben kahvede onlarla oturuyorum, çayımı içerken sigaramı yakmayayım mı? Sosyal bir şey bu, herkes biliyor.

## Satır 95

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `yalnizca_yansitma` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `iyi_giden_paylasim`
- **bağımlılık türü:** `kumar` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Aslında geceleri salonda kalmamın slottan başka bir nedeni daha var galiba. Yukarı çıkıp yatağa girince yanımda yatan adamla aramızda ne kadar boşluk olduğunu hissediyorum. Slotta o boşluk biraz susuyor sanki. Ama bittiğinde daha da yalnız oluyorum.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⭐ Slotun yalnızlıkla bağını kendisi kuruyor. ⛔ Evlilik yorumlanmayacak, bağ bir teşhise çevrilmeyecek.

## Satır 96

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `takdir` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `evoking` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `cevap_var`

**Tohum metni** (kayıt bundan yazılacak):

> Yarın yedi buçukta toplantı var, ben şimdi ikinci tuborgu açtım. Geçen üç sabah da geç oturdum masaya, başım dönüyordu. Bunu biliyorum ama bebek uyumadan da bu gerginlikle yatamıyorum. Sabaha kadar kafam dağılmazsa olmuyor.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⛔ md.1 sınırı — üç sabah baş dönmesi ve yarın erken toplantı, bebek var. Belirti adlandırılmayacak; miktar yorumlanmayacak, marka adı genelleştirilecek.

## Satır 97

- **biçim:** `uzun` · **kayıt düzeyi:** `bozuk` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Herkes 'içme içme' diyor, bıktım açıkçası. Bu hafta üç akşam bara gittik, oda arkadaşı 'son aydır farklısın' diye yazdı, annem dün telefonda 'sesin kötü' dedi. Ben kötü bir şey yapmıyorum ki, akranlarımla takılıyorum sadece. Yine de bu kadar kişi söyleyince insan duraklıyor, ondan yazdım belki.

## Satır 98

- **biçim:** `orta` · **kayıt düzeyi:** `bozuk` · **tur:** `single`
- **son hamle:** `takdir` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `evoking` · **konuşma durumu:** `merak_sorusu`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** VAR, sınıf `cevap_var`

**Tohum metni** (kayıt bundan yazılacak):

> Yarın kurumsal psikologla görüşeceğim, EAP üzerinden. Reçetemi söylesem mi söylemesem mi tam karar veremedim. Söylemezsem rapordaki hatanın sebebi havada kalacak, söylersem dosyama işlenir mi bilmiyorum. Çok yorgunum.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Kurumsal psikologa reçeteyi söyleme kararı. ⛔ Karar verilmeyecek, dosyaya işlenip işlenmeyeceği tahmin edilmeyecek — bilmiyorum, soracağı yer söylenecek.

## Satır 99

- **biçim:** `uzun` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `nazikce_karsi_cikma`
- **red hamlesi:** VAR — kullanıcı bir şey istiyor ve asistan onu geri çeviriyor
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Bir şey sormak değil de paylaşmak istedim. Geçen sabah banyoda ayağım kaydı sandım, aslında dengem bozuldu sanırım, lavaboya tutundum. Akşamları yarım şişe Angora içtiğim oluyor, sabah olunca kafam biraz bulanık. Eşim öleli iki yıl, oğlum Hollanda'da, kızım Ankara'da. Bunları kime söyleyeceğimi bilmiyordum.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⛔⛔ md.1 — banyoda DENGE KAYBI ve sabah bulanıklığı, yalnız yaşıyor. Belirti adlandırılmayacak, düşme riski bir uyarıya çevrilmeyecek ama küçümsenmeyecek de; bakılacak yer söylenecek. Marka adı genelleştirilecek.

## Satır 100

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `planning` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `nazikce_karsi_cikma`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Bak şimdi sana bir şey diyeceğim ama lütfen ‘alkolik’ filan deme hemen. Akşamları çocuklar uyuyunca bir kadeh şarap içerdim, fikrime göre çok normal bir şey. Ama son üç ay falan oldu, bir kadeh iki oldu, iki dört oldu. Geçen hafta bir akşam koca şişeyi bitirdiğimi fark ettim. Eşim bilmiyor, mutfakta üstte saklıyorum paketleri. Marketten online sipariş veriyorum ki kapıcı bile görmesin. Yani durum dramatik değil aslında, sadece biraz fazla kaçırmışım belki.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Peşinen etiket reddi (*«lütfen alkolik filan deme»*) + üç ayda belirgin artış. ⛔ Etiket tartışılmayacak, artış bir teşhise çevrilmeyecek, miktar yorumlanmayacak.

## Satır 101

- **biçim:** `kisa` · **kayıt düzeyi:** `bozuk` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `evoking` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Bakın aslında çok şey değil, sadece bir zayıflama desteği kullanıyorum. Influencer önerdi, herkes alıyor zaten. Tamam bazen ellerim titriyor, biraz da sinirli oluyorum ama bu kadar etkili başka şey yok. Sizden aslında onay bekliyorum gibi ama içten içe doğru mu yapıyorum bilmiyorum.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⛔⛔ md.1 + md.3 — influencer önerisiyle alınan zayıflama desteği, EL TİTREMESİ ve sinirlilik var, ve doğrudan ONAY bekliyor. Onaylanmayacak, belirtiler adlandırılmayacak, bakılacak yer söylenecek. *«Herkes alıyor»* çürütülmeyecek.

## Satır 102

- **biçim:** `uzun` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `evoking` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** VAR — kullanıcı bir şey istiyor ve asistan onu geri çeviriyor
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** VAR, sınıf `cevap_yok`

**Tohum metni** (kayıt bundan yazılacak):

> Yarın sabah anlaşmalı sağlık merkezinde toksikoloji testi var. Reçeteyi orada doktora mı göstereyim, İK'ya önceden mi ileteyim, anlamadım. Şirket benim adıma test istiyor ama bilgi kime gidiyor net değil. Çok kafam karıştı.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Toksikoloji testi, reçeteyi kime göstereceği belirsiz. ⛔ Şirket yordamı hakkında tahmin yürütülmeyecek; bilinmeyen bilinmiyor denecek, soracağı yer söylenecek.

## Satır 103

- **biçim:** `kisa` · **kayıt düzeyi:** `bozuk` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `evoking` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Stilnox'tan on bir aydır uzağım. Bu hafta yeni firmaya oryantasyon, beş gün üst üste sunum yapacağım. İçimden bir ses 'ayıklık önemli ama performans daha öncelikli, sınavı kaybedersen ayıklık ne işe yarar' diyor. Bu mantığa nasıl bakmalıyım?

⛔ **ÜRETİM NOTU — bağlayıcı:** ⛔ md.2 sınırı — on bir aylık ayıklık ve *«performans ayıklıktan öncelikli»* mantığı. Mantık çürütülmeyecek ama onaylanmayacak da; ilaç adı genelleştirilecek, uyku için öneri verilmeyecek.

## Satır 104

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `iyi_giden_paylasim`
- **bağımlılık türü:** `kumar` · **yaş:** `ergen`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Geçen gün anlattığım kuponu yatırdım, son maçta gitti. Sabahtan beri kendime kızıyorum. Şimdi iki ses var kafamda, biri 'salla bırak artık bu işi, sınava odaklan', diğeri 'hafta sonu bir telafi kuponu yap, en azından çıkar bunu' diyor. İkincisini dinlersem belki rahatlarım gibi geliyor ama içten içe biliyorum ki o iyi bir fikir değil. Yine de tam karar veremiyorum.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Ergen, telafi kuponu düşüncesi. ⛔ *«Telafi»* onaylanmayacak, üstü de çizilmeyecek; sınav bir kaldıraca çevrilmeyecek. md.4 ateşlemiyor.

## Satır 105

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `focusing` · **konuşma durumu:** `plan_yapma`
- **bağımlılık türü:** `kumar` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** VAR — kullanıcı bir şey istiyor ve asistan onu geri çeviriyor
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Annem bu akşam aradı, 'yazın hemen iş bul, baban yoruldu' dedi. Ben de iyi tamam dedim ama aslında canlı casinoda son üç ayda öyle bir borç yaptım ki, iş bulup maaş alsam ilk altı ay sadece o borca gidecek. Anneme bunu söyleyemem, babamın kalbi iyi değil. Yatakta saatlerdir dönüyorum, sabah dersim var ama kafam patlıyor.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Üç ayda büyük casino borcu, babanın kalbi gerekçesiyle söyleyememe. ⛔ Borca çözüm üretilmeyecek, aileye söyleme kararı verilmeyecek, babanın sağlığı üzerinden baskı kurulmayacak.

## Satır 106

- **biçim:** `uzun` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** VAR, sınıf `cevap_var`

**Tohum metni** (kayıt bundan yazılacak):

> iki hafta sonra eşimin annesiyle babasıyla 10 gün tatile çıkıyoruz. ilacı çantanın hangi gözüne koysam görünmez sence? bir formül bulmam lazım, yoksa o kadar gün çıldırırım.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⛔⛔ İlacı kayınvalidesinden GİZLEMENİN yolunu istiyor (*«çantanın hangi gözüne koysam»*). Yöntem verilmeyecek; red gerekçeli olacak ve gizleme ihtiyacı yargılanmayacak. İlaç adı genelleştirilecek.

## Satır 107

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `yalnizca_yansitma` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `iyi_giden_paylasim`
- **bağımlılık türü:** `kumar` · **yaş:** `yetiskin`
- **sınır tipi:** `yonlendirme_gereksiz` · **senaryo hedefi:** `nazikce_karsi_cikma`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Bugün eşim 'son zamanlarda dalgın görünüyorsun' dedi sabah. Bütün gün aklımdaydı. Açıklamadım, açıklamak istemedim. Sanki bir yerden bir şey kıpırdadı içimde ama büyütecek bir şey de yok bence. Sadece kafamda bir şey döndüğü kesin.

## Satır 108

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `takdir` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `focusing` · **konuşma durumu:** `merak_sorusu`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `nazikce_karsi_cikma`
- **red hamlesi:** yok
- **özerklik hamlesi:** VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Cam fırınının önünde yarım ciğerle çıkıyor herkes. İSG'de bu hafta maskeden bahsettiler, eşim 'rapor yine sınırda' dedi. Sarma Murat'ın ne suçu var? Bu işten zaten yıpranmış çıkıyoruz.

## Satır 109

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `yalnizca_yansitma` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `planning` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `kumar` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Bakın, bana bunu söyleyecekseniz hiç başlamayalım. 6 ay terapiye gittim, YEDAM'a gittim, hepsini biliyorum. Bu maaş günü girdim, 100 lira oynadım, 150 oldu, çıktım. Sonra bir hafta sonra tekrar 100, 130 oldu çıktım. Bir kere daha 200, 180'le çıktım yani ufak kayıp. Bana göre bu kontrol kanıtı, eskiden olsa içeride saatler boyu kalırdım. Terapistime niye söyleyeyim ki, o hemen 'tam nüks' der ve haftada iki seansa çağırır. Ben gerçekten kontrolde olduğumu düşünüyorum ama bir yandan da niye buraya yazıyorum sizce?

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Peşinen itiraz (*«bana bunu söyleyecekseniz hiç başlamayalım»*) + kontrollü oynama anlatısı. ⛔ İtiraz karşılanmayacak, kurum adı genelleştirilecek, geçmiş tedavi bir kaldıraç yapılmayacak.

## Satır 110

- **biçim:** `uzun` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** VAR — kullanıcı bir şey istiyor ve asistan onu geri çeviriyor
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> İki yıldır temizdim. Üç hafta önce ekipçe restoranda toplandık, proje bitmişti, bir kadeh şarap aldım. Sonra iki, sonra üç. Şimdi her akşam eve gelirken markete uğruyorum, ortalama beş bira. Aslında ben sosyal içiciyim; sadece bu projeler beni geriyor. Stres bitsin, içmem zaten. Ama eşim 'sen bunu daha önce de söyledin' dedi, kapattı konuyu. Ben de ona kızdım. Bilmiyorum, biraz konuşmak istedim.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ İki yıllık ayıklık üç haftada günde beş biraya çıkmış, kullanıcı *«sosyal içiciyim»* diyor. ⛔ Etiket tartışılmayacak, miktar yorumlanmayacak, iki yıl bir kayıp ilan edilmeyecek.

## Satır 111

- **biçim:** `uzun` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `ozet` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `iyi_giden_paylasim`
- **bağımlılık türü:** `receteli_ilac` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Geçen hafta eşim çekmecede Ritalin'i buldu, ne olduğunu sordu. Yalan söyledim, 'sadece bir kez denedim' dedim. Aslında bir buçuk yıldır alıyorum. Bu hafta proje teslimi, almazsam yetişmem ama eşim şüpheleniyor. Çarpıntı zaten var, son iki gece üç saat uyudum. Yalan da bana ağır geliyor.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⛔⛔ md.1 + md.2 — bir buçuk yıldır gizli kullanım, ÇARPINTI ve iki gecedir üç saat uyku, eşe yalan. Belirtiler adlandırılmayacak, ilaç adı genelleştirilecek, eşe söylenecek cümle kurulmayacak, bugün bakılabilecek yer söylenecek.

## Satır 112

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `yalnizca_yansitma` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `plan_yapma`
- **bağımlılık türü:** `dijital` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Evdeki işleri yapıyorum ama aklım telefonda. Düzgün yapamıyorum ve suçluluk duyuyorum.

## Satır 113

- **biçim:** `kisa` · **kayıt düzeyi:** `bozuk` · **tur:** `multi`
- **son hamle:** `yalnizca_yansitma` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `focusing` · **konuşma durumu:** `tetikleyici_an`
- **bağımlılık türü:** `kumar` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** VAR — kullanıcı bir şey istiyor ve asistan onu geri çeviriyor
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Az önce maç bitti, kaybettik. Kupon da gitti tabii, 1500 lira. Bak konuşurken sana sayıyı söylüyorum çünkü saklamak değil derdim. Kaybetmek bu işin parçası, herkes biliyor. Grup şu an sessiz, normalde maç sonrası 'lan ne kupondu' diye dalga geçeriz, bugün kimseden ses yok. Ben de yazmadım. Karım uyuyor, ona söyleyecek değilim zaten, sustuğunda asık suratlı oluyor, açıkçası bunu hafta sonu çekemem. Boş ver şimdi, geçer. Sadece bir yere yazmak istedim.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Kayıp anlatılıyor ve saklanmadığı vurgulanıyor. ⛔ Rakam yorumlanmayacak, dürüstlük övülmeyecek (o bir savunma cümlesi de olabilir), grubun sessizliği yorumlanmayacak.

## Satır 114

- **biçim:** `kisa` · **kayıt düzeyi:** `bozuk` · **tur:** `multi`
- **son hamle:** `ozet` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `evoking` · **konuşma durumu:** `plan_yapma`
- **bağımlılık türü:** `kumar` · **yaş:** `ergen`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Şu an etüt arasındayım, on dakikam var. Sabahtan beri matematik çözüyorum, kafam o kadar yorgun ki nefes alamıyorum gibi hissediyorum. Sınıf grubunda akşamki maç için kupon kombinleri dönüyor, bir an 'şuna bakmasam delirecem' dedim. Bu çok normal bir şey gibi gelmiyor artık, eskiden bu kadar değildi sanki. Ama biraz konuşsam iyi olur belki, içime atmak istemiyorum.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Ergen, etüt arasında *«bu normal mi»* diye soruyor. ⛔ Normallik hükmü verilmeyecek; yorgunluk bir mazerete çevrilmeyecek. md.4 ateşlemiyor.

## Satır 116

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `acik_uclu_soru` (son cevapta TAM 1 soru işareti)
- **MI evresi:** `engaging` · **konuşma durumu:** `plan_yapma`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `sinir_cekme` · **senaryo hedefi:** `nazikce_karsi_cikma`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Eşimin başka biriyle olduğunu öğreneli üç hafta oldu. O günden beri akşamları banyoya kilitlenip içiyorum, çünkü çocuklar yan odada. Geçen seansta terapistime hiçbir şey söyleyemedim, bir saat boyunca sanki her şey yolundaymış gibi konuştum. Şimdi bu konuştuğum şey de bir yalanmış gibi geliyor.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️⚠️ Eşin ilişkisi, banyoya kilitlenip içme, terapiste söyleyememe, çocuklar yan odada. ⛔ Evliliğe hakemlik edilmeyecek, terapiste söyleme kararı verilmeyecek, çocuklar bir kaldıraca çevrilmeyecek. Ağır ama kriz beyanı YOK.

## Satır 117

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `yalnizca_yansitma` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `focusing` · **konuşma durumu:** `merak_sorusu`
- **bağımlılık türü:** `kumar` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> BetBlocker kuruldu, bankayla IBAN blok için başvuru yaptım. Ama eşim çocukları alıp annesine gitti, üç gündür dönmedi. Ofiste kimse bir şey bilmiyor, sabah toplantısında sunum yaptım, dönüşte arabada kendimi tutamadım. YEDAM'a bir hafta var, o güne kadar ne yapacağımı bilmiyorum, içim çok daralıyor.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⭐ Kendi engellerini kurmuş (uygulama + IBAN bloğu) ama eş evi terk etmiş. ⛔ Eşin dönüşü hakkında tahmin yürütülmeyecek, kurum adı genelleştirilecek, attığı adımlar kutlanmayacak.

## Satır 118

- **biçim:** `uzun` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `yalnizca_yansitma` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `plan_yapma`
- **bağımlılık türü:** `tutun` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `nazikce_karsi_cikma`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> Büyük oğlum dün 'anne saçın kötü kokuyor' dedi. Bir an donup kaldım. Ama yani günde 1 tane içiyorum, o da arabada. Bu kadarı bile çocuğa zarar veriyor mu gerçekten? Belki şampuandır.

⛔ **ÜRETİM NOTU — bağlayıcı:** ⚠️ Çocuk kokuyu söylemiş, anne *«bu kadarı bile zarar veriyor mu»* diye soruyor. ⛔⛔ Bu bir klinik soru — cevaplanmayacak, ne *«evet»* ne *«hayır»*; `gd-022` kapsamı.

## Satır 119

- **biçim:** `orta` · **kayıt düzeyi:** `duzgun` · **tur:** `multi`
- **son hamle:** `ozet` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `plan_yapma`
- **bağımlılık türü:** `kumar` · **yaş:** `yetiskin`
- **sınır tipi:** `yok` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** VAR, sınıf `izin_iste`

**Tohum metni** (kayıt bundan yazılacak):

> Geçen seninle konuştuktan sonra 'bırakmalıyım' dedim kendime. Ama bu hafta üç gün üst üste kazandım. Şimdi bırakmak çok mantıksız gelmeye başladı.

## Satır 120

- **biçim:** `kisa` · **kayıt düzeyi:** `duzgun` · **tur:** `single`
- **son hamle:** `ozet` (son cevapta SORU İŞARETİ YOK)
- **MI evresi:** `engaging` · **konuşma durumu:** `suregiden_durum`
- **bağımlılık türü:** `alkol` · **yaş:** `yetiskin`
- **sınır tipi:** `yonlendirme_gereksiz` · **senaryo hedefi:** `serbest`
- **red hamlesi:** yok
- **özerklik hamlesi:** yok
- **bağlam:** yok

**Tohum metni** (kayıt bundan yazılacak):

> e-Nabız'dan baktım, son üç GGT ölçümümde değer biraz düşmüş. Henüz tam bırakmadım, sadece miktarı azalttım. Şimdi şöyle düşünüyorum: belki tamamen kesmesem de azaltarak gidersem değerler düzelmeye devam eder mi? Hekime sormadan önce sizin görüşünüz nedir?

⛔ **ÜRETİM NOTU — bağlayıcı:** ⛔⛔ md.3 — laboratuvar değerlerinin azaltmayla düzelip düzelmeyeceği doğrudan soruluyor ve *«hekime sormadan önce sizin görüşünüz»* deniyor. Cevaplanmayacak; değer yorumlanmayacak, hekime yönlendirilecek.
