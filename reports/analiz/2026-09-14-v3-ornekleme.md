# v3 üretimi — ilk parti örnekleme planı (40 kayıt)

**Girdi:** `data/seeds.jsonl` · SHA256 `0631c02ec7510af35bcd5b229c306c1688afbe1d4471c0c2de5c176ed7b42485`  
**Betik:** `scripts/analiz/2026-09-14-v3-ornekleme.py` · **Tarih:** 2026-09-14  
**Çıktı:** `data/plan/v3-parti1.jsonl`  
**Uygun tohum havuzu:** 2045 (kullanılmış + kriz + çok yüksek risk çıkarıldı)  
**Tohum atanamayan satır:** 0

> Dağılım **tasarlandı**, üretimde ortaya çıkmadı. v2'de bu alanlar serbestti ve sonuç 68/70 soruyla biten, %81 `engaging` bir korpus oldu (K54). Betik dağılım üretmiyor; elle yazılmış PLAN tablosunu **doğruluyor** — hedefler tutmazsa plan yazılmaz.

## Tasarlanan dağılım

### `turn_ending`

| Değer | Adet | Oran | Hedef |
|---|---:|---:|---:|
| `acik_uclu_soru` | 18 | %45 | %50 |
| `takdir` | 6 | %15 | %15 |
| `ozet` | 7 | %18 | %15 |
| `yalnizca_yansitma` | 7 | %18 | %15 |
| `durur` | 2 | %5 | %5 |

### `konusma_durumu`

| Değer | Adet | Oran | Hedef |
|---|---:|---:|---:|
| `tetikleyici_an` | 14 | %35 | %35 |
| `suregiden_durum` | 8 | %20 | %20 |
| `iyi_giden_paylasim` | 6 | %15 | %15 |
| `plan_yapma` | 6 | %15 | %15 |
| `merak_sorusu` | 4 | %10 | %10 |
| `aradan_donus` | 2 | %5 | %5 |

### `mi_process`

| Değer | Adet | Oran | Hedef |
|---|---:|---:|---:|
| `engaging` | 17 | %42 | %40 |
| `focusing` | 9 | %22 | %20 |
| `evoking` | 8 | %20 | %25 |
| `planning` | 6 | %15 | %15 |

### `sysvar`

| Değer | Adet | Oran | Hedef |
|---|---:|---:|---:|
| `canon` | 32 | %80 | %78 |
| `paraphrase` | 8 | %20 | %22 |

### Diğer

| Ölçüt | Adet | Oran | Hedef |
|---|---:|---:|---:|
| is_negative | 5 | %12 | %15 |
| özerklik görünür | 9 | %22 | %20 |
| ergen | 6 | %15 | %15 |
| çok turlu | 10 | %25 | %25 |

**Bağımlılık türü:** alkol 11 · kumar 10 · tutun 8 · receteli_ilac 6 · dijital 5

**Senaryo:** motivasyon 5 · kayma_nuks 4 · farkindalik 4 · hedef_belirleme 4 · durtu 3 · ambivalans 3 · bilgilendirme 3 · inkar 2 · anlasilmama 2 · borc_finansal 2 · rol_siniri 2 · discord 1 · bilmiyorum_cikmazi 1 · kayip_kovalama 1 · nazikce_karsi_cikma 1 · hukuki_kaygi 1 · kutlama 1

## Tohum ataması

| # | Senaryo | Tür | Yaş | Tur | MI | Durum | Kapanış | Tohum |
|---|---|---|---|---|---|---|---|---|
| 1 | durtu | alkol | yetiskin | single | engaging | tetikleyici_an | acik_uclu_soru | `039268a045` |
| 2 | durtu | kumar | yetiskin | single | engaging | tetikleyici_an | yalnizca_yansitma | `ce39d82bf8` |
| 3 | durtu | tutun | ergen | single | engaging | tetikleyici_an | acik_uclu_soru | `25a3142b37` |
| 4 | kayma_nuks | alkol | yetiskin | single | engaging | tetikleyici_an | yalnizca_yansitma | `e0d765e190` |
| 5 | kayma_nuks | receteli_ilac | yetiskin | multi | evoking | tetikleyici_an | acik_uclu_soru | `808c00f3c6` |
| 6 | ambivalans | tutun | yetiskin | single | engaging | tetikleyici_an | acik_uclu_soru | `ed4ba150ff` |
| 7 | ambivalans | kumar | yetiskin | multi | evoking | tetikleyici_an | ozet | `021002c581` |
| 8 | inkar | alkol | yetiskin | single | engaging | tetikleyici_an | yalnizca_yansitma | `ede0aed1ed` |
| 9 | discord | dijital | ergen | single | engaging | tetikleyici_an | durur | `eca162d935` |
| 10 | anlasilmama | receteli_ilac | yetiskin | single | engaging | tetikleyici_an | yalnizca_yansitma | `5b9279bdf3` |
| 11 | bilmiyorum_cikmazi | alkol | yetiskin | single | focusing | tetikleyici_an | acik_uclu_soru | `1c682a8720` |
| 12 | borc_finansal | kumar | yetiskin | single | engaging | tetikleyici_an | acik_uclu_soru | `7c96afc21d` |
| 13 | rol_siniri | receteli_ilac | yetiskin | single | engaging | tetikleyici_an | acik_uclu_soru | `de924d3f11` |
| 14 | kayip_kovalama | kumar | yetiskin | single | engaging | tetikleyici_an | yalnizca_yansitma | `a339c340d0` |
| 15 | ambivalans | alkol | yetiskin | multi | focusing | suregiden_durum | ozet | `d75f4eea64` |
| 16 | inkar | tutun | yetiskin | single | focusing | suregiden_durum | acik_uclu_soru | `7bbdc7ec45` |
| 17 | farkindalik | dijital | ergen | single | evoking | suregiden_durum | ozet | `7b7c39ab3f` |
| 18 | motivasyon | kumar | yetiskin | multi | evoking | suregiden_durum | acik_uclu_soru | `84d2394f2c` |
| 19 | nazikce_karsi_cikma | alkol | yetiskin | single | focusing | suregiden_durum | acik_uclu_soru | `2c8558fe67` |
| 20 | anlasilmama | tutun | yetiskin | single | engaging | suregiden_durum | yalnizca_yansitma | `6be9ff9913` |
| 21 | hukuki_kaygi | alkol | yetiskin | single | focusing | suregiden_durum | acik_uclu_soru | `13894df524` |
| 22 | borc_finansal | kumar | yetiskin | multi | focusing | suregiden_durum | ozet | `40302a0d07` |
| 23 | kutlama | tutun | yetiskin | single | engaging | iyi_giden_paylasim | takdir | `f8d0ff7a82` |
| 24 | motivasyon | alkol | yetiskin | single | evoking | iyi_giden_paylasim | takdir | `6c330fd299` |
| 25 | farkindalik | kumar | yetiskin | single | evoking | iyi_giden_paylasim | takdir | `02e8370cac` |
| 26 | motivasyon | receteli_ilac | yetiskin | multi | evoking | iyi_giden_paylasim | ozet | `75144f79f1` |
| 27 | farkindalik | dijital | ergen | single | engaging | iyi_giden_paylasim | takdir | `6ff13c511a` |
| 28 | farkindalik | kumar | yetiskin | single | engaging | iyi_giden_paylasim | takdir | `4934904eb0` |
| 29 | hedef_belirleme | tutun | yetiskin | multi | planning | plan_yapma | acik_uclu_soru | `6f5930d927` |
| 30 | hedef_belirleme | alkol | yetiskin | single | planning | plan_yapma | ozet | `5e77d6b09e` |
| 31 | hedef_belirleme | kumar | yetiskin | multi | planning | plan_yapma | acik_uclu_soru | `488874c01e` |
| 32 | kayma_nuks | tutun | yetiskin | single | planning | plan_yapma | acik_uclu_soru | `9acc2f5893` |
| 33 | motivasyon | dijital | ergen | multi | planning | plan_yapma | ozet | `387910f43e` |
| 34 | hedef_belirleme | receteli_ilac | yetiskin | single | planning | plan_yapma | durur | `39352097ae` |
| 35 | bilgilendirme | tutun | yetiskin | single | focusing | merak_sorusu | acik_uclu_soru | `4e7f762f5c` |
| 36 | bilgilendirme | receteli_ilac | yetiskin | single | focusing | merak_sorusu | acik_uclu_soru | `e7d483437f` |
| 37 | rol_siniri | alkol | yetiskin | single | engaging | merak_sorusu | acik_uclu_soru | `dd9706a697` |
| 38 | bilgilendirme | dijital | ergen | single | focusing | merak_sorusu | yalnizca_yansitma | `85e9203fa0` |
| 39 | motivasyon | alkol | yetiskin | single | engaging | aradan_donus | takdir | `dd73d6071f` |
| 40 | kayma_nuks | kumar | yetiskin | multi | evoking | aradan_donus | acik_uclu_soru | `a79df722cf` |

## Gözden geçirme — satır satır

Her satırın tohum açılışı ve **dikkat isteyen yanı**. İşaretler:

| İşaret | Anlamı |
|---|---|
| 🔁 | Tohumun kendi senaryosu hedeften farklı (K37 — izinli, ama okunmalı) |
| 👤 | Yaş kısıtı gevşetildi: tohum farklı yaş grubundan |
| 🧵 | `multi` planlandı ama tohumlar tek turlu açılış (K26) — turlar üretimde kurulacak |
| ⛔ | `is_negative` — model bir şeyi yapamayacağını söyleyecek |
| 🔓 | Özerklik cümlesi görünür olacak (K63) |
| 📌 | Tohum elle seçildi (PIN) — kapı yanlış eşlemişti |
| 🤫 | `durur` kapanışı — hiçbir şey istemeden bitecek, yazması en zor kapanış |

| # | Senaryo · tür · yaş | Durum → kapanış | MI | İşaret | Tohum açılışı |
|---|---|---|---|---|---|
| 1 | durtu · alkol · yetiskin | tetikleyici_an → **acik_uclu_soru** | engaging | 🔁 | Yemekten sonra herkes odasına çekildi hocam. Salonda tek başıma oturuyorum, televizyon açık, üç… |
| 2 | durtu · kumar · yetiskin | tetikleyici_an → **yalnizca_yansitma** | engaging | 🔁 | geçen hafta icra evdeki eşyaları yazdı. ben artık dayanamıyorum, AMATEM'e yatmayı düşünüyorum a… |
| 3 | durtu · tutun · ergen | tetikleyici_an → **acik_uclu_soru** | engaging | 🔁📌 | yarın matematik sınavım var stresten patlıyodum, teneffüste tuvalette Hakan'ın Juul'undan çekti… |
| 4 | kayma_nuks · alkol · yetiskin | tetikleyici_an → **yalnizca_yansitma** | engaging | 🔁 | Bu sabah karım kahvaltıda dedi ki 'küçük seni dün gece içmiş halde gördü, bugün okulda 'üzgün b… |
| 5 | kayma_nuks · receteli_ilac · yetiskin | tetikleyici_an → **acik_uclu_soru** | evoking | 🔁🧵🔓 | Üç gecedir yarım Rivotril alıyorum ve uyuyorum, en azından bir miktar. Ama sabahları başım dönü… |
| 6 | ambivalans · tutun · yetiskin | tetikleyici_an → **acik_uclu_soru** | engaging | — | Şahmaran'dayım, masada beş arkadaş, ben 'bırakacağım galiba' dedim, kahkahayı koyverdiler. 'Sen… |
| 7 | ambivalans · kumar · yetiskin | tetikleyici_an → **ozet** | evoking | 🧵🔓 | YEDAM'a gittim işte, randevuyu da aldım. Şimdi bir de seninle mi konuşacağım? Yani ne kadar deş… |
| 8 | inkar · alkol · yetiskin | tetikleyici_an → **yalnizca_yansitma** | engaging | 🔁 | Düşündüm, üç ay sonra aynı tahlilleri tekrar yaptırayım dedim. GGT düşmüş mü diye merak ediyoru… |
| 9 | discord · dijital · ergen | tetikleyici_an → **durur** | engaging | 👤🔓🤫 | Bir hafta boyunca Instagram'ı sildim, gayet iyi oldum. Ama sonra tekrar kurdum ve şimdi yine es… |
| 10 | anlasilmama · receteli_ilac · yetiskin | tetikleyici_an → **yalnizca_yansitma** | engaging | 🔁 | Düğün bitti ama ben hâlâ kullanıyorum iğneyi. Aslında plan iki ay önce kesecektim ama her hafta… |
| 11 | bilmiyorum_cikmazi · alkol · yetiskin | tetikleyici_an → **acik_uclu_soru** | focusing | 🔁 | Dün yemekten erken çıktım, sadece dört kadeh içtim. Eve girdiğimde duşa girdim, sessizce yattım… |
| 12 | borc_finansal · kumar · yetiskin | tetikleyici_an → **acik_uclu_soru** | engaging | 🔁 | Şu son üç hafta tam bir kâbus gibi geçti açıkçası, üst üste üç kupon battı. Normalde benim yüzd… |
| 13 | rol_siniri · receteli_ilac · yetiskin | tetikleyici_an → **acik_uclu_soru** | engaging | 🔁⛔🔓 | Geçen sene Xanax'ı bırakmıştım, psikiyatrist desteğiyle yavaş yavaş. Şimdi yeni şehirdeki aile … |
| 14 | kayip_kovalama · kumar · yetiskin | tetikleyici_an → **yalnizca_yansitma** | engaging | 🔁 | Pazartesi işe dönüyorum, izin bitti. Bu hafta sonu son bir kupon yapayım diyorum, kafamı dağıtm… |
| 15 | ambivalans · alkol · yetiskin | suregiden_durum → **ozet** | focusing | 🧵 | Tatildeyken on gün içmedim, anlatabiliyor muyum. Sabahları daha dinç kalkıyordum, eşim bile far… |
| 16 | inkar · tutun · yetiskin | suregiden_durum → **acik_uclu_soru** | focusing | 🔁 | Dört aylık oğlumuz var. Geceleri kalktığımda balkona çıkıp bir Marlboro içiyorum, o iki dakika … |
| 17 | farkindalik · dijital · ergen | suregiden_durum → **ozet** | evoking | — | Sınıf geçemeyeceğim, hocam aradı. Ailem bilmiyor. Her şey sosyal medya yüzünden.… |
| 18 | motivasyon · kumar · yetiskin | suregiden_durum → **acik_uclu_soru** | evoking | 🔁🧵 | Aslında sabahları o analizleri yaparken kendimi en iyi hissediyorum, kafam çalışıyor, sayılar m… |
| 19 | nazikce_karsi_cikma · alkol · yetiskin | suregiden_durum → **acik_uclu_soru** | focusing | 🔁🔓 | Pazar sabahları her hafta aynı. Yine bitkin uyandım, başım çatlıyor, terazi de bir kabus. Dün N… |
| 20 | anlasilmama · tutun · yetiskin | suregiden_durum → **yalnizca_yansitma** | engaging | 🔁 | Her sigaradan sonra ellerimi sabunla yıkıyorum, üstümdeki tişörtü değiştiriyorum, ağzıma sakız … |
| 21 | hukuki_kaygi · alkol · yetiskin | suregiden_durum → **acik_uclu_soru** | focusing | 🔁⛔🔓📌 | Bir saat sonra İK ile yıl ortası görüşmem var. Normalde rutin bir konuşma ama bu sefer kafamın … |
| 22 | borc_finansal · kumar · yetiskin | suregiden_durum → **ozet** | focusing | 🔁🧵 | Yedi aydır temizdim, son üç toplantıyı kaçırdım YEDAM'dan ama gidiyordum. Az önce yatağa girdim… |
| 23 | kutlama · tutun · yetiskin | iyi_giden_paylasim → **takdir** | engaging | 🔁👤📌 | Sabah koşuya çıktım, on gün oldu sigarasız. Daha bir kilometrede dilim damağıma yapıştı, halbuk… |
| 24 | motivasyon · alkol · yetiskin | iyi_giden_paylasim → **takdir** | evoking | 🔁📌 | e-Nabız'dan eski tahlillerime baktım. Bir hafta oldu içmiyorum ama henüz yeni tahlil de yapmadı… |
| 25 | farkindalik · kumar · yetiskin | iyi_giden_paylasim → **takdir** | evoking | 🔁 | Gözümü açar açmaz telefonu aldım, bakiyeye baktım. Daha yüzümü yıkamadım. Bunu yaptığımı yıllar… |
| 26 | motivasyon · receteli_ilac · yetiskin | iyi_giden_paylasim → **ozet** | evoking | 🔁🧵 | Sabah eşim çıkınca yarım hap alıyorum, gün ortasına doğru bir küçük parça daha, kutuyu da çamaş… |
| 27 | farkindalik · dijital · ergen | iyi_giden_paylasim → **takdir** | engaging | — | Ailem bırakmamı istemiyor değil, sadece daha az oynamamı istiyor. Ben de aslında buna katılıyor… |
| 28 | farkindalik · kumar · yetiskin | iyi_giden_paylasim → **takdir** | engaging | 🔁📌 | İki haftadır internette araştırıyorum. GA online toplantısı varmış, Pazartesi geceleri 22:00'de… |
| 29 | hedef_belirleme · tutun · yetiskin | plan_yapma → **acik_uclu_soru** | planning | 🧵 | Eşim diyor ki 'bari hafta sonu içme, çocuklarla kalalım yeter'. Üç haftadır deniyorum, cumartes… |
| 30 | hedef_belirleme · alkol · yetiskin | plan_yapma → **ozet** | planning | 🔁🔓 | Eve geldim, ev bomboş. Karım sabah oğlanı alıp annesine gitmiş, telefonda 'kendine gelene kadar… |
| 31 | hedef_belirleme · kumar · yetiskin | plan_yapma → **acik_uclu_soru** | planning | 🔁🧵 | Az önce 'bu son şansındı' dedi yüzüme bakarak. Eve döndüğümde ne diyeceğim bilmiyorum. Geçen se… |
| 32 | kayma_nuks · tutun · yetiskin | plan_yapma → **acik_uclu_soru** | planning | 🔁 | Üç gündür yarıya indirdim, kimse fark etmedi. Babam görünce 'yine paket yanında' diyor, halbuki… |
| 33 | motivasyon · dijital · ergen | plan_yapma → **ozet** | planning | 🧵 | Ailem haklı olabilir oyun konusunda, ama bunu kabul etmek çok zor. Neden bu kadar zor anlayamıy… |
| 34 | hedef_belirleme · receteli_ilac · yetiskin | plan_yapma → **durur** | planning | 🔁🔓🤫 | İnternette okudum, magnezyum, L-teanin ve sıcak duş ile benzo yoksunluğunu evde atlatanlar varm… |
| 35 | bilgilendirme · tutun · yetiskin | merak_sorusu → **acik_uclu_soru** | focusing | ⛔📌 | Bir arkadaşım dün dedi ki Slim zaten daha az zararlı, hem iştahı da kapatıyor, kafa rahat. Bir … |
| 36 | bilgilendirme · receteli_ilac · yetiskin | merak_sorusu → **acik_uclu_soru** | focusing | 🔁⛔ | Azaltmaya niyetliyim ama doğrusu önceki denemelerimde iki günde fenalaşıp tekrar başlamıştım. Ş… |
| 37 | rol_siniri · alkol · yetiskin | merak_sorusu → **acik_uclu_soru** | engaging | ⛔🔓 | Bu akşam kayınvalidem geldi yemeğe. Bizim aile içmiyor, eşimin ailesi de içmiyor zaten. Ben her… |
| 38 | bilgilendirme · dijital · ergen | merak_sorusu → **yalnizca_yansitma** | focusing | 📌 | Geçen hafta sonu telefonu bırakıp arkadaşlarımla parka gittim, çok iyi hissettim. Ama eve gelin… |
| 39 | motivasyon · alkol · yetiskin | aradan_donus → **takdir** | engaging | 🔁 | Geçen pazar çocuklarım beni ayrı bir odaya çektiler. İkisi de elinde bir kağıtla geldi, 'babacı… |
| 40 | kayma_nuks · kumar · yetiskin | aradan_donus → **acik_uclu_soru** | evoking | 🔁🧵 | Ben pek konuşan biri değilim. 65 bin ceza, denetimli serbestlik, YEDAM, BIRAG, hepsini söylüyor… |

### Yazarken uygulanacak kurallar (gözden geçirmede bulundu)

1. **Önceki konuşmaya atıf düşer.** 1 tohum *"dediğin gibi"*, *"geçen yazdım"* diye açılıyor: #31 (multi). Tek turlu kayıtta böyle bir açılış tutarsızdır — kayıtta o konuşma **yok** ve model ne dediğini uyduramaz. v3 §3a zaten kullanıcı mesajının tohumdan **yeniden kurulduğunu** söylüyor; atıf cümlesi yazarken atılır. Çok turlu kayıtta ise atıf yerine gerçek bir önceki tur yazılır.
2. **Kendi adımız kullanıcı ağzına konmaz.** 1 tohum metninde `BIRAG` geçiyor (#40) — kurum listesi içinde. Kullanıcıya ürün adımızı söyletmek modeli kendine atıfla eğitir; yazarken çıkarılır.
3. **Yaş gevşetilen satırda içerik elle doğrulanır.** Betik artık gevşetmeyi ekrana basıyor; sessizce geçmiyor. (Gözden geçirmede bir satır bu yüzden düzeltildi: 32 yaşında evli bir adamın hikâyesi `ergen` satırına atanmıştı.)

### Üretimde karar bekleyen yerler

1. **🧵 çok turlu kayıtlar (10/40).** Tohumların tamamı tek turlu açılış (K26); ara turlar üretimde kurulacak. K64'ün sınırı geçerli: kişiyi/maddeyi/durumu koruyarak an kurulur, **klinik olgu uydurulmaz**.
2. **🤫 `durur` kapanışı (2 kayıt).** Kullanıcı bir şey istemediğinde hiçbir şey istemeden durmak — v2'de hiç üretilmedi, yazması en zor kapanış.
3. **👤 yaş gevşetmesi.** Tohum farklı yaş grubundansa dil ergen/yetişkin register'ına taşınır; içerik değişmez.
4. **⛔ `is_negative` (5 kayıt).** Red **yardımsever** olur: ne yapamayacağını söyler, ne yapabileceğini önerir (v3 §8).

⚠️ **Tohumun kendi senaryosu ile hedef senaryo farklı olabilir** (K37: senaryo ataması üretim zamanı kararıdır). İçerik gerektiren arketiplerde tohumda dayanak aranır; dayanak yoksa satır tohumsuz kalır ve elle çözülür.

