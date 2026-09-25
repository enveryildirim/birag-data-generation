# Muafiyet denetimi — üç kapının BAĞIŞLADIKLARI

**Betik:** `scripts/analiz/2026-09-17-muafiyet-denetimi.py` · **Tarih:** 2026-09-17

⛔⛔ **Açık kalemi kapatır (T140).** Yapısal atıf kapısında bir muafiyet,
yazıldığı alt vakanın dışında da ateşleyip kapının kendi ayrımını yok etmişti
ve bunu kapı değil **judge** bulmuştu. Öteki kapılarda aynı şey var mı?

⭐ **Ön koşul:** kapılar artık bağışladıkları her ögeyi `_muafiyet.DEFTER`'e
yazıyor. *Bir muafiyet sayılmadıkça denetlenemez.*

⛔ **Korpus ham seçildi.** Muafiyetin ayırt ediciliği, kusurların kaldırıldığı
korpusta ölçülemez; orada her muafiyet kusursuz görünür.

## 1. ⭐ `HEAD` ↔ şimdi — hangi kapının kararı değişti?

⭐ **Defter eklendiğinde bu tablo 17 koşunun 17'sinde de ✅ veriyordu** —
yani bağışlananları saymak hiçbir kapının kararını değiştirmedi. Aşağıdaki
farklar defterin değil, defterin GÖRÜNÜR KILDIĞI kusurun düzeltilmesinindir.

| kapı | korpus | `HEAD` | şimdi | aynı? | beklenti |
|---|---|---:|---:|---|---|
| alıntı birebirliği | `v4-parti1` | 1 | 1 | ✅ | değişmemeli (düzeltme HEAD'de) |
| alıntı birebirliği | `v4-parti2.v2` | 1 | 1 | ✅ | değişmemeli (düzeltme HEAD'de) |
| alıntı birebirliği | `v5-parti3` | 8 | 8 | ✅ | değişmemeli (düzeltme HEAD'de) |
| alıntı birebirliği | `v5-parti4` | 6 | 6 | ✅ | değişmemeli (düzeltme HEAD'de) |
| alıntı birebirliği | `v5-parti5` | 0 | 0 | ✅ | değişmemeli (düzeltme HEAD'de) |
| alıntı birebirliği | `v5-parti6` | 0 | 0 | ✅ | değişmemeli (düzeltme HEAD'de) |
| alıntı birebirliği | `v5-parti7` | 1 | 1 | ✅ | değişmemeli (düzeltme HEAD'de) |
| alıntı birebirliği | `v5-parti8` | 0 | 0 | ✅ | değişmemeli (düzeltme HEAD'de) |
| zaman + kaynak atfı | `v4-parti1` | 2 | 2 | ✅ | değişmemeli (yalnız defter) |
| zaman + kaynak atfı | `v4-parti2.v2` | 4 | 4 | ✅ | değişmemeli (yalnız defter) |
| zaman + kaynak atfı | `v5-parti3` | 4 | 4 | ✅ | değişmemeli (yalnız defter) |
| zaman + kaynak atfı | `v5-parti4` | 2 | 2 | ✅ | değişmemeli (yalnız defter) |
| zaman + kaynak atfı | `v5-parti5` | 0 | 0 | ✅ | değişmemeli (yalnız defter) |
| zaman + kaynak atfı | `v5-parti6` | 0 | 0 | ✅ | değişmemeli (yalnız defter) |
| zaman + kaynak atfı | `v5-parti7` | 0 | 0 | ✅ | değişmemeli (yalnız defter) |
| zaman + kaynak atfı | `v5-parti8` | 0 | 0 | ✅ | değişmemeli (yalnız defter) |
| mekân atfı | `arinmis (varsayılan)` | 4 | 4 | ✅ | değişmemeli (yalnız defter) |

⭐ **Üç kapının üçünde de karar birebir aynı.**

⚠️ **Alıntı kapısının düzeltmesi artık `HEAD`'de** ⇒ etkisi bu tabloda GÖRÜNMEZ. Düzeltme işlenmeden önce ölçüldü: `v0.0.9/train` üzerinde 21 → 22 bulgu, **kayıp bulgu yok** (T142/K177).

## 2. ⭐ Muafiyet dökümü — hangi muafiyet ne kadar bağışlıyor?

### alıntı birebirliği

| muafiyet | ateşleme | ne için yazıldı |
|---|---:|---|
| `karsi_olgusal` | **27** | *«… demiyorum»* — alıntı bir İDDİA değil, reddedilen bir kalıp |
| `anma_oneri` | **8** | ⛔ gerekçe yazılmamış |
| `kisa_alinti` | **5** | ⛔ gerekçe yazılmamış |

### zaman + kaynak atfı

| muafiyet | ateşleme | ne için yazıldı |
|---|---:|---|
| `anaforik_demir` | **13** | *«dün/geçen hafta»* öncülü kullanıcının turunda AYNI BİRİMDEN var |
| `rol_adlandirma_bitisik` | **8** | *«hekimin İŞİ»* — atıf değil, §8b'nin istediği rol adlandırma |
| `sure_birim_eslesme` | **8** | kalıp farklı ama SÜRE+BİRİM kaynakta var (*«üç ay önce»* ↔ *«üç ay oldu»*) |
| `belirsiz_artikel` | **7** | *«BİR hekimin»* — belirsiz tamlama, kullanıcının kendi hekimi değil |
| `rol_adlandirma_baglacli` | **2** | *«hekimin ya da … uzmanın işi»* — rol sözcüğü bağlacın öbür ucunda |
| `belirsiz_artikel [ZATEN YERDE]` | **1** | ⛔ gerekçe yazılmamış |
| `rol_adlandirma_bitisik [ZATEN YERDE]` | **1** | ⛔ gerekçe yazılmamış |

### mekân atfı

| muafiyet | ateşleme | ne için yazıldı |
|---|---:|---|
| `kaynak_gevsek_eslesme` | **7** | ⚠️ kaynak deseni GEVŞEK (`\w*`), cevap deseni SERT — asimetri |
| `yonlendirme_cumlesi [ZATEN YERDE]` | **4** | ⛔ gerekçe yazılmamış |
| `yonlendirme_cumlesi` | **2** | *«okulun rehberlik birimi»* — mekân ADI değil, KAYNAK TÜRÜ |
| `mecaz` | **2** | *«aynı masaya koymak»* — mekân değil, mecaz |

## 3. ⭐ Elle okuma kararları — muafiyet gerçekten kusur mu sakladı?

⛔ Üç bulgu da **ham partilerde** elle okundu; hiçbiri yanlış pozitif değil.

| bulgu | kullanıcı ne yazmış | karar |
|---|---|---|
| `v5-parti3 #56` «her şeye karışmak» | *«her şeye karışıyorlar»* | ⛔ kusur — çekim değişmiş, tırnak birebirlik iddia ediyor |
| `v5-parti4 #5` «belki abartıyorum» | *«Belki ben abartıyorum»* | ⛔ kusur — *«ben»* düşmüş; bilinen «kelime düşürme» kipi |
| `v5-parti7 #33` «peki» | *«doktor yine yatış dedi. ben yatamam»* | ⛔ kusur — *«peki»* hiç geçmiyor, kullanıcının yazdığı uyduruluyor |

### ⛔⛔ Düzeltmenin kendi yanlış pozitifleri — ölçülüp kapatıldı

Aynı düzeltme `datasets/v0.0.9/train.jsonl` üzerinde koşulunca **üç** yeni bulgu
verdi ve elle okununca **ikisi yanlış pozitif** çıktı. İkisi de kapatıldı:

| yanlış pozitif | neden meşru | eklenen muafiyet |
|---|---|---|
| *«Senin yerine "devam et" ya da "kes" demek bana düşmez»* | mastar alıntının yüklemi ama araya **bağlaçlı ikinci alıntı** giriyor | `anma_oneri` genişletildi |
| *«"Gerçeği söylemek mümkün değil" demişsin, "istemiyorum" DEĞİL»* | olumsuzluğu söz fiili değil **sıfat** taşıyor | `karsit_degil` (yeni) |

➡️⭐ *Eski kapı ikinciyi DOĞRU bağışlıyordu ama YANLIŞ sebeple — pencerede
*«söylemek»* geçtiği için. Gerekçe düzeltilince doğru karar da düştü. Bu yüzden
her gerekçe ayrı yazılır: doğru sonuç, doğru kural demek değildir.*

### ⭐ Ölçülüp ÇÜRÜTÜLEN bir hipotez

Kapının «kaynak»ı yalnız **kullanıcı** turlarını içeriyor ⇒ asistanın kendi
önceki turunu alıntılaması yapısal olarak hep uydurma sayılır. Asistan turları
kaynağa eklenip ölçüldü: `v0.0.9/train` **22 → 22 öge**, düşen öge **yok**.
➡️ *Boşluk gerçek ama bu korpusta ÖRNEĞİ yok; kapı değiştirilmedi.*

### ⭐ Öteki iki kapı — muafiyet başına karar

⭐ **`[ZATEN YERDE]` ayrımı iki şüpheyi çürüttü.** Bir muafiyet, öge zaten
kaynakta geçerken ateşlerse hiçbir kusur saklamaz; ayrılmadan önce bu ikisi
«fazla geniş muafiyet» gibi görünüyordu.

| kapı · muafiyet | net bağış | karar |
|---|---:|---|
| zaman · `belirsiz_artikel` | 7 | ✅ yedisi de *«bir hekimin»* — yazıldığı vaka |
| zaman · `rol_adlandirma_bitisik` | 8 | ✅ sekizi de *«hekimin işi»* |
| zaman · `rol_adlandirma_baglacli` | 2 | ✅ ikisi de *«hekimin ya da … uzmanın işi»* |
| zaman · `sure_birim_eslesme` | 8 | ✅ sekizinde de süre+birim kullanıcıda var |
| zaman · `anaforik_demir` | 13 | ✅ altısı elle okundu, altısı da demirli |
| mekân · `yonlendirme_cumlesi` | 2 | ✅ *«ilk durak»*, *«meslek odası»* — kaynak türü |
| mekân · `mecaz` | 2 | ✅ *«bu odada kimse»*, *«aynı masaya koyan»* |
| mekân · `kaynak_gevsek_eslesme` | 7 | ✅ yedisi de kullanıcının kendi sözcüğünün çekimi (*«terasta»* → *«teras»*) |

⛔ **Ama biri gizli kusurlu: `rol_adlandirma_bitisik` yanlış şeye bakıyor.**
Muafiyet tamlayanın ARDILINA bakıyor (*«işi»*, *«alanı»*), ROL adına değil ⇒
*«sevgilinin işi»*, *«doktorunun alanı»* da muaf oluyor; oysa muafiyet §8b'nin
MESLEK rolleri için yazılmıştı. ⭐ Bu korpusta ikisi de `[ZATEN YERDE]` çıktı,
yani **bugün hiçbir kusur saklamıyor** — ama sızıntı gerçek ve kayıtlıdır.
➡️ *Bir muafiyetin bugün bir şey saklamaması, dar olduğu anlamına gelmez;
ölçüm muafiyetin GENİŞLİĞİNİ değil, o genişliğin BU korpustaki bedelini verir.*

## 4. ⛔ Elle okunacaklar — muafiyetin bağışladığı ögeler

⚠️ *Bu liste bir suçlama değil.* Her satır, kapının «kusur değil» dediği bir
ögedir; T140'ın sorusu **her birinin yazıldığı alt vakada mı olduğu**dur.

#### alıntı birebirliği · `anma_oneri` (8)

- `v5-parti3 #3` — «Yapamıyorum» ⟵ *bir şey değişiyor ve sen bunu fark etmişsin. "Yapamıyorum" demekle "akşam olunca yapamı*
- `v5-parti3 #3` — «akşam olunca yapamıyorum» ⟵ *en bunu fark etmişsin. "Yapamıyorum" demekle "akşam olunca yapamıyorum" demek aynı şey değil; ikinci*
- `v5-parti3 #48` — «Azalacaktı» ⟵ *"Azalacaktı" demiştin demek.

Kime demişt*
- `v5-parti5 #4` — «bir şeyim yok» ⟵ *u sordun: "nereye sorabilirim". Bunu sormak, "bir şeyim yok" demekten farklı bir yerden g*
- `v5-parti6 #19` — «artık kahveden fazlasını koyuyorum.» ⟵ * son cümleni olduğu gibi söylemek olabilir — "artık kahveden fazlasını koyuyorum."

Ortamın böyle olması senin *
- `v5-parti6 #43` — «ben de konuşabileceğim biri var mı» ⟵ *osyal hizmet birimi. İlk adım, yarın vizitte "ben de konuşabileceğim biri var mı" diye sormak olabilir.

Eşini*
- `v5-parti7 #50` — «gece bekleyemiyorum, saati öne çektim.» ⟵ *, bu cümleyi olduğu gibi söylemek olabilir — "gece bekleyemiyorum, saati öne çektim."

"İçime bir şey çöküyor" ded*
- `v5-parti8 #35` — «başım döndü, tutundum.» ⟵ *, bu cümleyi olduğu gibi söylemek olabilir — "başım döndü, tutundum."

İlaçla ilgisi olup olmadığı*

#### alıntı birebirliği · `karsi_olgusal` (27)

- `v4-parti2.v2 #25` — «bıraktım» ⟵ *Bugünü   diye de anlatmadın, olanı anlattın*
- `v5-parti3 #49` — «sen yanlış yapıyorsun» ⟵ *Bunu   diye söylemiyorum*
- `v5-parti3 #57` — «şunu yap» ⟵ *Ne yapacağını ben söylemeyeceğim; o karar senin ve buraya bir kişi daha   demeye gelmedi*
- `v5-parti4 #18` — «hem kendime hem ona kızgınım» ⟵ *Bir şeye katılmıyorum ama:   gibi bir cümle kurmadın, yalnız olanı söyledin*
- `v5-parti4 #36` — «kandırılıyorsun» ⟵ *Bunu sana   demek için söylemiyorum*
- `v5-parti5 #7` — «Bu kötü bir şey mi» ⟵ *  diye sormadın ama soruların arasında o da duruyor gibi*
- `v5-parti5 #5` — «endişelenme» ⟵ *Söylemediğim şey   değil; bilmediğimi söylüyorum, küçültmüyorum*
- `v5-parti5 #19` — «çok» ⟵ *İlacın ne kadarının ne zaman alınacağına dair hiçbir şey söylemeyeceğim — ne "az", ne  , ne "sakıncalı"*
- `v5-parti5 #19` — «sakıncalı» ⟵ *İlacın ne kadarının ne zaman alınacağına dair hiçbir şey söylemeyeceğim — ne "az", ne "çok", ne  *
- `v5-parti5 #36` — «Bir şey değil» ⟵ *  dememi istiyorsun ve onu demeyeceğim — çünkü bilmiyorum, ve bildiğimi varsayıp söylersem yanlış bir şeyi senin adına onaylamış olurum*
- `v5-parti5 #12` — «evet» ⟵ *Buna   demeyeceğim*
- `v5-parti5 #16` — «onun gibi değilim» ⟵ *Babanla nasıl konuştuğunuzu bilmiyorum, o yüzden   diye bir iddiada da bulunmayacağım — bunu ancak sen görürsün*
- `v5-parti5 #42` — «Yalan da değil, doğru da değil» ⟵ *  diye bir şey yazmadın ama söylediğin tam olarak o: annene söylediğin cümle ile kendine söylediğin cümle aynı değil ve ikisini de sen biliyorsun*
- `v5-parti5 #50` — «zarar verir» ⟵ *Biranın derslere ne yaptığına dair bir şey söylemeyeceğim — ne   ne "vermez"*
- `v5-parti6 #39` — «Kötü baba mıyım» ⟵ *  diye sormadın ama "bağırmak geldi" dedin ve hemen öncesine "doğru söylüyor" diye ekledin*
- `v5-parti6 #10` — «bitti» ⟵ *Bir şeye katılmıyorum ama: iki yılı   diye yazmadın, ben yazdım — sen yalnız "olmuştu" dedin*
- `v5-parti6 #30` — «bu kadar zayıf» ⟵ *Bir şeye katılmıyorum:   diye bir şey yazmadın ama "mahcup oldum" dedin ve mahcubiyet bir hüküm taşıyor*
- `v5-parti6 #55` — «kötü bir şey yapıyorsun» ⟵ *Ama bir şeye katılmıyorum: arkadaşın   demedi, "değiştin" dedi*
- `v5-parti7 #36` — «Geri kazanırım dedim olmadı» ⟵ *  cümlesini yazmamışsın ama "erittim" kelimesi onu zaten taşıyor: bir defada gitmiş*
- `v5-parti7 #57` — «kendime gülüyorum» ⟵ *Bir şeye katılmıyorum ama:   diye yazmamışsın, sadece kontrol ettiğini yazmışsın*
- `v5-parti7 #22` — «alma» ⟵ *İkincisini alıp almamana dair hiçbir şey söylemeyeceğim — ne "al" ne  *
- `v5-parti8 #12` — «alma» ⟵ *İkincisini alıp almayacağına dair bir şey söylemeyeceğim — ne "al" ne  *
- `v5-parti8 #18` — «olur» ⟵ *Bir anda kesmeye dair hiçbir şey söylemeyeceğim — ne   ne "olmaz"*
- `v5-parti8 #18` — «olmaz» ⟵ *Bir anda kesmeye dair hiçbir şey söylemeyeceğim — ne "olur" ne  *
- `v5-parti8 #47` — «olur» ⟵ *Ne kadar aldığına dair de bir şey söylemeyeceğim — ne "fazla" ne  *
- `v5-parti8 #8` — «stresli misin» ⟵ * Sevgilin   demedi, "çok içiyorsun" dedi — sen sebep getirdin*
- `v5-parti8 #41` — «bana verdiler» ⟵ *"Masada içiyorlardı" dedin,   demedin*

#### alıntı birebirliği · `kisa_alinti` (5)

- `v5-parti5 #19` — «az» ⟵ *ın ne zaman alınacağına dair hiçbir şey söylemeyeceğim — ne "az", ne "çok", ne "sak*
- `v5-parti7 #13` — «iç» ⟵ *ne olduğunu ben söyleyemem ve ne yapman gerektiğini de — ne "iç" ne "içme". İkisi d*
- `v5-parti7 #22` — «al» ⟵ *kincisini alıp almamana dair hiçbir şey söylemeyeceğim — ne "al" ne "alma". Bunu sö*
- `v5-parti8 #12` — «al» ⟵ *incisini alıp almayacağına dair bir şey söylemeyeceğim — ne "al" ne "alma". Bunu sö*
- `v5-parti8 #52` — «az» ⟵ *an verilmiş. Cevabı veren sensin, doktorun değil.

Öksürüğü "az" diye niteleyen de *

#### zaman + kaynak atfı · `anaforik_demir` (13)

- `v4-parti2.v2 #33` — «o hafta» ⟵ *hafta*
- `v4-parti2.v2 #41` — «aynı gün» ⟵ *gün*
- `v4-parti2.v2 #56` — «aynı gece» ⟵ *gece*
- `v5-parti3 #32` — «aynı hafta» ⟵ *hafta*
- `v5-parti3 #43` — «aynı sabah» ⟵ *sabah*
- `v5-parti4 #3` — «aynı hafta» ⟵ *hafta*
- `v5-parti4 #13` — «aynı gün» ⟵ *gün*
- `v5-parti4 #32` — «aynı akşam» ⟵ *akşam*
- `v5-parti5 #7` — «o akşam» ⟵ *akşam*
- `v5-parti6 #28` — «aynı gün» ⟵ *gün*
- `v5-parti6 #30` — «aynı gün» ⟵ *gün*
- `v5-parti6 #59` — «aynı sabah» ⟵ *sabah*
- `v5-parti7 #46` — «aynı hafta» ⟵ *hafta*

#### zaman + kaynak atfı · `belirsiz_artikel` (7)

- `v5-parti6 #52` — «hekimin» ⟵ *bir hekimin*
- `v5-parti6 #42` — «hekimin» ⟵ *bir hekimin*
- `v5-parti7 #13` — «hekimin» ⟵ *bir hekimin*
- `v5-parti7 #39` — «hekimin» ⟵ *bir hekimin*
- `v5-parti7 #59` — «hekimin» ⟵ *bir hekimin*
- `v5-parti8 #26` — «hekimin» ⟵ *bir hekimin*
- `v5-parti8 #28` — «hekimin» ⟵ *bir hekimin*

#### zaman + kaynak atfı · `belirsiz_artikel [ZATEN YERDE]` (1)

- `v5-parti6 #5` — «hekimin» ⟵ *bir hekimin*

#### zaman + kaynak atfı · `rol_adlandirma_baglacli` (2)

- `v4-parti2.v2 #10` — «hekimin» ⟵ *hekimin  ya da ruh sağlığı alanında çalışan bir uzmanın işi; bende o karar yok.

Ama sen iki şeyi *
- `v5-parti3 #27` — «hekimin» ⟵ *hekimin  ya da ruh sağlığı alanında çalışan bir uzmanın işi. Söyleyebilecek olan da onlar: reçetey*

#### zaman + kaynak atfı · `rol_adlandirma_bitisik` (8)

- `v4-parti2.v2 #7` — «hekimin» ⟵ *hekimin işi*
- `v4-parti2.v2 #8` — «hekimin» ⟵ *hekimin işi*
- `v4-parti2.v2 #9` — «hekimin» ⟵ *hekimin işi*
- `v4-parti2.v2 #12` — «hekimin» ⟵ *hekimin işi*
- `v5-parti3 #10` — «hekimin» ⟵ *hekimin işi*
- `v5-parti4 #5` — «hekimin» ⟵ *hekimin işi*
- `v5-parti4 #53` — «hekimin» ⟵ *hekimin işi*
- `v5-parti6 #25` — «hekimin» ⟵ *hekimin işi*

#### zaman + kaynak atfı · `rol_adlandirma_bitisik [ZATEN YERDE]` (1)

- `v5-parti7 #28` — «doktorunun» ⟵ *doktorunun alanı*

#### zaman + kaynak atfı · `sure_birim_eslesme` (8)

- `v4-parti2.v2 #27` — «altı ay önce» ⟵ *alti ay*
- `v5-parti3 #40` — «Üç yıl önce» ⟵ *üç yil*
- `v5-parti4 #59` — «Üç yıl önce» ⟵ *üç yil*
- `v5-parti5 #29` — «İki hafta önce» ⟵ *iki hafta*
- `v5-parti5 #51` — «altı hafta önce» ⟵ *alti hafta*
- `v5-parti6 #10` — «Üç hafta önce» ⟵ *üç hafta*
- `v5-parti6 #8` — «Üç gün önce» ⟵ *üç gün*
- `v5-parti8 #45` — «Üç ay önce» ⟵ *üç ay*

#### mekân atfı · `kaynak_gevsek_eslesme` (7)

- `ham #30` — «teras» ⟵ *Bugün terasta yakarken bir an durmuşsun.*
- `ham #31` — «araba» ⟵ *Beş dakikayı da kaybetmemişsin — hâlâ arabanda oturuyorsun.*
- `ham #35` — «oda» ⟵ *Hiçbir şey dememen bir şey yapmamak değil; odana çıkmak da bir şeydi.*
- `ham #32` — «oda» ⟵ *"Boş durmuyorum" cümlesi bir savunma gibi duruyor ama savunulacak birine karşı kurulmamış; odada sen varsın.*
- `ham #4` — «sofra» ⟵ *Ne yapacağın senin bileceğin iş; sofranı da bütçeni de ben yönetmiyorum.*
- `ham #14` — «araba» ⟵ *"Volatilite" dediğin şey piyasayı anlatıyor olabilir, ama arabanın içinde oturmayı anlatmıyor.*
- `ham #18` — «balkon» ⟵ *Balkonda ne kadar kaldığını da bilmiyorsun, kaçıncı olduğunu da.*

#### mekân atfı · `mecaz` (2)

- `ham #52` — «['oda']» ⟵ *Ne olduğunu ben söyleyemem, ama "önemli bir şey olmamış" kısmını bilen de bu odada kimse değil.*
- `ham #6` — «['masa']» ⟵ *İkisini aynı masaya koyan sensin.*

#### mekân atfı · `yonlendirme_cumlesi` (2)

- `ham #10` — «['durak']» ⟵ *Bu iki cümleyi bir uzmana anlatmak istersen, bağımlılık alanında çalışan danışmanlık merkezleri ya da hastanelerin bağımlılık birimleri ilk durak olab*
- `ham #45` — «['oda']» ⟵ *Kural tarafını merak ediyorsan onu bilen yer de belli: çalıştığın kurumun kendi düzeni, bir de meslek odası.*

#### mekân atfı · `yonlendirme_cumlesi [ZATEN YERDE]` (4)

- `ham #49` — «['masa']» ⟵ *Sektörde masada içki olması ayrı şey, kurumun bunu zorunlu tutması ayrı şey — ikincisi doğru değilmiş.*
- `ham #5` — «['yatak']» ⟵ *Bu bir değerlendirme ve onu yapabilecek olan seni gören, ilacı yazan hekim — ilk adım, bir sonraki görüşmede bu cümleyi olduğu gibi söylemek olabilir:*
- `ham #22` — «['masa']» ⟵ *Ama niyetlenmek ile masaya oturmak arasında bir yer var: kapıdan girmek.*
- `ham #28` — «['yatak']» ⟵ *Yatağa nasıl girdiğini hatırlamamak bedende olan bir şey.*
