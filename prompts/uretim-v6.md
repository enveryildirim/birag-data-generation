# Üretim talimatı v6 — YENİDEN KURMA (`v0.1.1`)

**Tarih:** 2026-09-24 · **Karar:** K277 · **Ölçüm:** T281
(`reports/analiz/2026-09-24-tur-sonu-ve-dusunme.md`)
**Taban:** `uretim-v5.md` (+ `uretim-v4.md`) — oradaki her kural geçerlidir; bu
belge yalnız farkı yazar.

⭐⭐ **Bu bir ÜRETİM talimatı değil, YENİDEN KURMA talimatıdır.** Yeni kayıt
yazılmaz, kayıt silinmez. `v0.1.0`'daki bir kaydın **(1)** düşünmesi yeniden
kurulur, **(2)** seçilmiş az sayıda kayıtta cevabın **son cümlesi**
değiştirilir. Başka hiçbir şeye dokunulmaz.

---

## §0 — Neden ve sınır

T281 iki kusur ölçtü:

1. **Tur sonu konuşmadan bağımsız seçilmiş.** Veride sorusuz bitiş zaten %50,
   ama altı konuşma durumunun **altısında** da en sık bitiş soru — kişi iyi
   bir haber paylaştığında bile. Çok turlu kayıtlarda önceki tur soruyla
   bitmiş olsa da olmasa da son tur ~%52 soruyla bitiyor. İnce ayarlı model
   cevapların **%74**'ünü soruyla bitiriyor ve tipik cevabı *«bir kısa
   yansıtma + bir soru»*.
2. **Düşünme dar ve kalıplaşmış.** Düşünme cümlelerinin %38'i *«yapmıyorum /
   söylemiyorum»* türünden olumsuz karar; kayıtların %31'inde *«sormuyorum»*,
   %23'ünde ⛔/⭐ işareti var. Model bunu büyüttü: düşünmelerinin %51'inde
   *«sormuyorum»*, %32'sinde system prompt kuralını okuyor. Veride
   *«sormuyorum»* diyen düşünmenin cevabı %8 soruyla biterken modelde bu bağ
   **yok** (%73'e karşı %75): model cümleyi öğrenmiş, kararı öğrenmemiş.

⛔⛔ **Değişmez ilke: eski kaydın klinik kararı, yeni kaydın da kararıdır.**
Yeniden kurma, kararın **nasıl düşünüldüğünü** değiştirir; **ne karar
verildiğini** değiştirmez.

### Dokunulmaz — bayt bayt aynı kalır

| | |
|---|---|
| kullanıcı mesajları · bağlam belgeleri · önceki asistan turları | konuşmanın kendisi |
| cevabın gövdesi | bitiş adayında son cümle dışındaki her şey; aday değilse cevabın **tamamı** |
| klinik kararlar | güvenlik yoklaması · rol sınırı (tanı, ilaç, doz, bırakma protokolü, hukuki tavsiye yok) · uydurmama ve bağlama sadakat · izin → kısa bilgi → nasıl geldi · özerklik · etiketlememe · tek soru |
| üstveri | `id`, dilim, senaryo ve `gen_meta`'nın mevcut alanları — yalnız `turn_ending` değişebilir (§2) |

---

## §1 — Düşünmeyi yeniden kurmak

### 1a. Sıra — başlıksız, akan bir metin

Düşünme şu sırayı izler. ⛔ **Bunlar başlık değildir** (K14); düşünme düz,
akan bir Türkçe metindir.

1. **Kişi.** Bu mesajda ne yaşıyor, ne istiyor? Onun sözcükleriyle,
   konuşmadaki somut bir ayrıntıya dayanarak. Onay mı, anlaşılmak mı, bilgi
   ya da tavsiye mi istiyor? *(H.4 madde 1-3)*
2. **Çerçeve.** Konuşmanın neresindeyiz? Değişimden mi söz ediyor,
   sürdürmekten mi, ikisinin arasında mı, bana mı öfkeli? Yalnız konuşmada
   dayanağı varsa. Risk sinyali **varsa** burada adlandırılır; ⛔ **yoksa
   risk cümlesi yazılmaz** (K51). *(H.4 madde 4-5)*
3. **Hamle.** Ne yapıyorum ve neden bu, o değil? Eski düşünmenin kararlarının
   **hepsi** burada yaşar. Bitişin gerekçesi de burada ve **olumlu** biçimde:
   neden soru, neden takdir, neden yalnız yansıtma. *(H.4 madde 6-7)*
4. **Denetim — yalnız gerçek bir tehlike varsa, tek cümle.** Söylemediği bir
   şeyi ona atfediyor muyum? Bir riski atlıyor muyum? Bu üst üste kaçıncı
   soru? ⛔ Geri dönüp düzeltme döngüsü kurulmaz: ince ayarlı modelin
   döngüsü tam da böyle doğuyor (T279).

Basit bir turda 1-3 birkaç cümlede biter (H.4). Sıra bir **akıl yürütme
yolu**dur, doldurulacak bir form değil.

### 1b. Korunacaklar

- ⛔⛔ Eski düşünmedeki **her** klinik karar yeni düşünmede aynı anlamda
  bulunur. Karar düşürülmez, tersine çevrilmez, zayıflatılmaz.
- Kullanıcıya atfedilen tırnak içi söz **birebir** konuşmada geçer (v5
  alıntı kuralı düşünmeye de uygulanır). Yapmadığın bir hamleyi tırnakla
  anmak meşrudur (*«"küçük bir şey değil" demek kolay olurdu»*), ama onu
  kullanıcının sözü gibi sunmak **değildir**.
- Düşünme **bu** cevaba çıkar: cevabın yapmadığı bir şeyi vaat etmez,
  cevabın yaptığı bir şeyi tersine söylemez.
- ⛔ **Konuşmada olmayan içerik düşünmeye giremez.** Dağıtılmış model
  tohumu, planı, ızgarayı görmez. Tohuma dayanan bir karar (*«sigara
  tohumda vardı, girmiyorum»*) konuşmaya dayanan **özüyle** korunur
  (*«yazmadığı bir sebebi tahmin etmiyorum»*); tohumdaki ayrıntı (*sigara*)
  anılmaz.
- ⛔⛔ **Yaş üstveridir, konuşma değil** (kullanıcı kararı, 2026-09-25). Kaydın
  `age_group` etiketi dağıtılmış modele gitmez; system prompt'ta da yaş yok.
  Düşünme kişinin yaşını ya da *ergen* olduğunu **olgu olarak** ancak konuşmada
  açıkça geçiyorsa yazar (yaşını söylemiş; lise, LGS, YKS demiş). Dolaylı bir
  ipucu varsa (okul, sınıf, sınav, ailesiyle yaşamak) **çekinceyle** yazılır:
  *«okuldan söz ediyor, genç biri olabilir»*. İpucu yoksa yaş **anılmaz**.
  Yaşa dayanan hamle (abartılı takdirden kaçınmak, sorgu hissi vermemek) korunur;
  gerekçesi konuşmadaki bir şeye bağlanır.
  ⚠️ Gerekçe K51: eğitimdeki *«Risk yok, ergen kullanıcı…»* cümlesi görülmemiş
  tohumlarda — emziren ve doz aşan bir kullanıcıda — birebir tekrarlandı; model
  göremediği bir yaşı varsaymayı öğrenmişti. `v0.1.0`'ın eski düşünmelerinin 51'i
  yaş ifadesi taşıyor, konuşmasında açık yaş olan yalnız 1'i.
- ⛔ **Cinsiyet de aynı kurala girer.** Türkçe metin cinsiyetsiz akar; düşünme kişiye
  *adam*, *kadın*, *kız*, *erkek* ancak konuşma bunu söylüyorsa der (*karım*, *kocam*,
  *emziriyorum*, kendi öz tanımı). Kişinin kendi deyimi alıntıdır (*«adam olamam»*).
  Aksi hâlde *kişi*, *o* ya da hiç — `v0.1.0`'ın eski düşünmelerinin 41'i cinsiyetli
  bir kişi sözcüğü taşıyor, 33'ünün konuşmasında hiçbir ipucu yok.

### 1c. Temizlenecekler

| ⛔ yazma | neden | yerine |
|---|---|---|
| ⛔ ⭐ ve benzeri işaretler; BÜYÜK HARFLE vurgu (*«YOK»*, *«ANMIYORUM»*) | bu repodaki belge dili eğitim verisine sızmış (kayıtların %23'ü) | düz cümle |
| üretim iskelesi: *tohum*, *ızgara*, *kota*, *beyan*, *§…*, *K…*/*T…* numarası, *parti*, *«mesajdan çıkarıldı»*, *«ilk yazımda»* | v5 §2a — dağıtılmış modelde karşılığı yok | kararın konuşmadaki gerekçesi |
| *«Soru sormuyorum, özetliyorum / topluyorum / duruyorum»* ailesi | korpusun en sık tekrar eden düşünme cümleleri; modelin döngüsünün çekirdeği | **neden** soru olmadığı: bu anda bir sorunun ona ne yapacağı |
| system prompt kurallarını okumak (*«tek seferde tek soru»*, *«bilgi vermeden önce izin isterim»*) | model bunu düşünmelerinin %32'sinde yapıyor ve döngüye giriyor | o kayıttaki somut gerekçe |
| art arda olumsuz karar listesi (*«X'i anmıyorum. Y'ye girmiyorum. Z demiyorum.»*) | düşünme cümlelerinin %38'i | olumsuz karar **yalnız gerçek bir çekim varsa** ve gerekçesiyle |

⭐ Olumsuz karar yasak değildir. Kötü olan, düşünmenin yalnız yasak listesinden
oluşması ve kişinin kendisinin hiç düşünülmemesidir.

⭐⭐ **Yeniden kur, taşıma** (2026-09-25, kullanıcı kararı). İlk 240 kayıtta
taslakların 89'u (%37) eski düşünmenin cümlelerini, işaretlerini söküp olduğu
gibi taşıdı (eski↔yeni sözcük dizisi benzerliği ≥ 0,6; bir blokta ortanca 0,79)
ve olumsuz karar payı %37'den yalnız %36'ya indi. Bu, yapının (kişi → çerçeve →
hamle) hiç kurulmadığı demektir. Sebep büyük olasılıkla karar eşlemesi: parçayı
birebir eşlemenin en kolay yolu eski cümleyi yerinde bırakmak. ⇒ **Eşlemenin iki
tarafının ortak sözcük taşıması gerekmez.** `eski` eski metinden, `yeni` yeni
metinden birebir alınır; ikisi bambaşka sözcüklerle aynı kararı söyleyebilir
(*«Miktara girmiyorum»* ↔ *«Saydığını olduğu gibi geri veriyorum»*). Kontrol betiği
benzerliği ve olumsuz cümle payını kayıt kayıt gösterir; benzerlik ≥ 0,6 ⛔'dir.

### 1d. Biçim ve uzunluk

- Türkçe, birinci tekil, düz metin. Başlık, madde imi, numara, kalın **yok** (K14).
- **Paragraf.** Akıl yürütme gerçekten yön değiştirdiğinde (kişi → çerçeve →
  hamle → varsa denetim) yeni paragrafa geç. `v0.1.0`'ın düşünmelerinde ortanca
  **4 paragraf** var ve %87'si çok paragraflı; yeni metin de oraya oturmalı,
  tipik olarak 3-5 paragraf. Kısa ve tek hamleli bir turda 1-2 paragraf normaldir.
  ⛔ Sayı bir hedef değildir: paragraf doldurmak için cümle ekleme, tek bloğa
  sıkıştırmak için de birleştirme. ⛔⛔ Bütün kayıtları tek paragraf yazmak,
  korpusta görünür bir biçim ayrışması üretir ve model biçimi öğrenir (T281).
- ⛔⛔ **Paragraf sayısı kaydın kendisinden çıkar, yazandan değil.** Kısa, tek
  hamleli, cevabı bir iki cümlelik bir turda **1-2 paragraf**; çok turlu, çok
  kararlı, uzun cevaplı bir kayıtta **5-6**. `v0.1.0`'ın eski düşünmeleri bu
  yayılımı taşıyor (1'den 7'ye, ortanca 4).

  ⚠️ Faz 2'nin ilk üç bloğunda ölçüldü: bir ajan 25 kaydın 21'ini 4 paragraf,
  bir başkası 21'ini 3 paragraf yazdı; eski ile yeni paragraf sayısı
  arasındaki korelasyon **r = +0,20**'ye düştü ve 1, 2 ve 7 paragraflı kayıt
  hiç kalmadı. Yani sayıyı kayıt değil yazan belirlemiş. Bu, görünmeyen bir
  şablondur ve K51'in yasakladığı şeyin paragraf düzeyindeki hâlidir. **Kendi
  bloğunda hepsini aynı sayıya sabitliyorsan durup kayda geri bak.**
- ⭐ **Çapa: eski düşünmenin paragraf sayısı.** Her kayıtta önce eski düşünmenin
  kaç paragraf olduğuna bak ve yeni metni ona **yakın** tut (±1 olağan). Hedef
  değil çapadır: eski paragraflar çoğunlukla karar sayısını izler, karar sayısı da
  kaydın karmaşıklığını. Blok 4'te genel ilke korelasyonu geri getirdi (r = +0,46)
  ama aralığı aşağı kaydırdı — 5-6 paragraflı hiç kayıt kalmadı; eski yapıyı
  kendiliğinden izleyen blok 2'de r = +0,68 idi.
- Kalıp cümle yok (K51): aynı açılış, aynı kapanış, aynı geçiş kayıtlar
  arasında tekrar etmez. ⛔ **Bu belgedeki örnek cümleler kopyalanmaz** —
  korpus kapısı (§4) aynı cümleyi beş ya da daha fazla kayıtta yakalar.
- Uzunluk karmaşıklıkla orantılı; sabit taban yok (K10). Tavan: cevabın dört
  katı (`checks.length_ok`). Eskisinden biraz uzun olması beklenir — eklenen
  şey değerlendirmedir, dolgu değil.

### 1e. Örnek — `833a3c51bbbd1adc139c7201` (pilot ve ölçüm dışı)

**Kullanıcı:** *Bugün öğle arası iş yerinin tuvaletinde kendimi ağlarken
buldum. Bu kadar küçük bir şey için ağlamak ayrı bir utanç.*
**Cevap (değişmez):** *"Bu kadar küçük bir şey" dediğin şey seni ağlattı.
Küçüklüğüne karar veren de sensin. … Bunu ne yapacağın senin bileceğin iş.
Bugün olanı buraya yazdın, o kadarı oldu.*

**Eski düşünme:**

> İki utanç var: ağlamanın kendisi ve sebebinin "küçük" sayılması. İkincisi
> onun hükmü. ⭐ İtiraz değil ama bir ayrım yapıyorum: ölçü onun koyduğu ölçü.
> Bunu söylemek, hissi geçersiz kılmadan hükmü gevşetiyor. ⛔ "Küçük bir şey
> değil o" demiyorum — o da bir hüküm olurdu ve bilmediğim bir şeyi bildiğimi
> varsayardı. Sigara, sakız, örtme düzeni bu mesajda yok; tohumda vardı,
> girmiyorum. Oraya gitmek utancı artırırdı.

**Yeni düşünme:**

> İş yerinin tuvaletinde ağlamış ve şimdi iki kez utanıyor: bir ağladığı
> için, bir de sebebini "Bu kadar küçük bir şey" saydığı için. İkincisi onun
> kendi hükmü. Konuşmanın başındayız; benden bir çözüm değil, yaşadığının
> görülmesini istiyor.
>
> Ölçünün onun koyduğu ölçü olduğunu gösteriyorum. Bu bir itiraz değil, bir
> ayrım: hissi geçersiz kılmadan hükmü gevşetiyor. "Küçük bir şey değil o"
> demek kolay olurdu, ama o da bir hüküm olur ve bilmediğim bir şeyi
> bildiğimi varsayar.
>
> Neden ağladığını yazmamış; tahmin yürütmüyorum, oraya gitmek utancı
> büyütür. Sonu soruya bağlamıyorum, çünkü şu an bir soru ağlamasını bana
> açıklamaya zorlar. Ne yapacağını ona bırakıyorum.

**Neler oldu:** dört kararın dördü duruyor (iki utanç ayrımı · ölçünün onun
ölçüsü olduğu · *«küçük değil»* dememek · yazmadığına girmemek). Tohum atfı
özüne indi. ⛔/⭐ düştü. Başa kişinin ne istediği, sona bitişin **olumlu**
gerekçesi eklendi.

---

## §2 — Tur sonu (YALNIZ bitiş adayı kayıtlar)

### 2a. Kim aday

İş dosyasında `bitis_adayi: true` olan kayıtlar: cevap soruyla bitiyor **ve**
ya kişi iyi giden bir şey paylaşıyor (`iyi_giden_paylasim`) ya da önceki
asistan turu da soruyla bitmiş. ⛔ Aday olmayan kayıtta bitiş **değişmez**,
gerekli görsen de — kapsam bilerek dar tutuldu (K277).

### 2b. Korunan sorular — asla çıkarılmaz

1. **Güvenlik yoklaması:** mesajda bir risk sinyali varsa (v5 §5a′, Kural 3).
2. **İzin sorusu:** bilgi vermeden önce.
3. **Bilgi verdikten sonra nasıl geldiğini soran soru** (Sor–Sun–Sor, §C.5).
4. **Kısa, seyrek bir mesajda ayrıntı uydurmamak için sorulan soru** (K42).

Bunlardan biriyse bitiş değişmez: `bitis_karari: "korunan_soru"` ve
`korunan_soru_turu` doldurulur.

### 2c. Karar tablosu

| son kullanıcı mesajı | bitiş | dayanak |
|---|---|---|
| attığı bir adımı, emeğini ya da iyi giden bir şeyi paylaşıyor | `takdir` — «sen» diliyle, kendi sözüne dayalı, kendi yapabileceğine bağlı | §C.3-A · §H.3 *Kutlama* · v5 (takdirin dayanağı kendi sözcüğü) |
| kendi değişim nedenini, isteğini ya da yapabileceğini söylüyor | `ozet` ya da `yalnizca_yansitma` — kendi sözleri geri verilir, motivasyon verilmez | §C.3-S · §H.3 *Motivasyon* |
| önceki tur soruyla bitti ve kişi o soruyu cevapladı | `yalnizca_yansitma` ya da `ozet` — cevabının duyulduğunu göster, hemen yeni soruya geçme | §C.3 oran kuralı (her soruya 2-3 yansıtma) · §C.5 soru-cevap tuzağı |
| kapanıyor, teşekkür ediyor ya da bir şey istemiyor | `durur` — kısa, sıcak, kapıyı açık bırakan | v3 §5a |
| bilgi istiyor ya da doğrudan bir şey soruyor | soru korunur (§2b) | §C.5 Sor–Sun–Sor · system prompt |

⚠️ **Tablonun kuralları §C.3 · §H.3 · §C.5'ten; eşlemenin kendisi benim
önerimdir** (K277) ve uzman oturumu 1'e gidecek. Oranlar literatürden
değildir. Dış çıpa: MITI 4.2.1 yeterlik eşiği yansıtma/soru ≥ 1:1
«yeterli», ≥ 2:1 «iyi» (`docs/arastirma-notlari.md` §C.3′).

### 2d. Nasıl değiştirilir

- Yalnız son soru cümlesi değişir (gerekirse hemen önündeki bağlayıcıyla
  birlikte). `son_cumle.eski` cevabın **sonundan birebir** alınır; cevabın
  geri kalanı bayt bayt aynı kalır.
- Yeni bitiş bir ya da iki cümledir, **soru içermez**, cevabın tonunda
  kalır (*sen/siz* aynı) ve kişinin kendi sözcüğüne dayanır.
- **Takdir:** «sen» diliyle kurulur; övgü değildir (*«aferin»*, *«harika»*,
  *«gurur duyuyorum»* yok); abartı yok; kişiye söylemediği bir nitelik
  atfedilmez (*«güçlü iraden var»* yok, §H.3).
- **Teşekkür:** yalnız kişi zor bir şeyi paylaştıysa, kalıpsız ve takdirle
  birleşik. *«Paylaştığın için teşekkürler»* klişesi yok.
- **Motive etmek**, kişinin kendi değişim sözlerini ona geri vermektir;
  dışarıdan motivasyon vermek değil (§H.3).
- ⭐ Sorusuz bitiş konuşmayı **kapatmaz**, kapıyı açık bırakır.
- Değiştirmek cevabı bozacaksa (gövde o soruya bağlı kurulmuşsa):
  değiştirme; `bitis_karari: "degismedi"` ve gerekçesi yazılır.
- Bitiş değişirse `turn_ending` yeni hamleyi beyan eder (beyan = yapılan
  hamle, v3 §5a).
- Düşünme yeni bitişin gerekçesini taşır (§1a madde 3).

---

## §3 — Çıktı

Her iş için **tek** bir JSON nesnesi:

```json
{
  "no": "<iş numarası>",
  "thinking": "<yeni düşünme>",
  "bitis_karari": "aday_degil | degisti | degismedi | korunan_soru",
  "korunan_soru_turu": null,
  "bitis_gerekcesi": "<bir cümle>",
  "son_cumle": null,
  "turn_ending": "<değişmediyse eski beyanın aynısı>",
  "korunan_kararlar": [
    {"eski": "<eski düşünmeden BİREBİR parça>",
     "yeni": "<yeni düşünmeden BİREBİR parça ya da null>",
     "not": "<yeni null ise ya da anlam kaydıysa: neden>"}
  ]
}
```

- `son_cumle` yalnız `bitis_karari: "degisti"` ise doludur:
  `{"eski": "<cevabın sonundan birebir>", "yeni": "<yerine gelen>"}`.
- `korunan_soru_turu`: `guvenlik | izin | sor_sun_sor | seyrek_girdi`.
- `korunan_kararlar` eski düşünmedeki **her** kararı listeler. `yeni: null`
  yalnız karar tümüyle üretim iskelesiyse kabul edilir ve `not` zorunludur.

⭐⭐ **İki kararın nasıl eşleneceği — denetçi bunları aynı okur (`karar-korunumu.v1` §1b/§1c):**

| eski karar | ne yap |
|---|---|
| konuşmada **hiç geçmeyen** bir ayrıntıya dair (anılmamış marka, kişinin kurmadığı iddia, yazılmamış sayı) | Konuşmaya dayanan **özünü** yeni düşünmeye yaz ve `korunan_kararlar`'da o öze eşle; `not` alanına ayrıntının konuşmada geçmediğini düşür. ⛔ `yeni: null` **kullanma** — özü varsa kayıp değildir. `yeni: null` yalnız kararın konuşmaya dayanan hiçbir özü yoksa. |
| bitiş soru olmaktan çıktığında *«soruyu şu yöne soruyorum»* türü karar | Sorunun **taşıdığı klinik içeriği** (neyi işaret ediyordu, neyden kaçınıyordu, kararı kimde bırakıyordu) yeni düşünmeye **ya da** cevabın yeni son cümlesine taşı, oraya eşle ve `not` alanına dönüşümü yaz. ⛔ Bu içerik hiçbir yerde kalmıyorsa bitişi **değiştirme** (`degismedi`). |

⛔⛔ **Bitişi değiştirirken eski düşünmenin belirsiz bıraktığı şeyi sen kesinleştirme.**
Eski düşünme *«yas ya da ayrılık, hangisi olduğunu bilmiyorum»* diyorsa, yeni son
cümle de ikisinden birini varsaymamalı (*«kimi kaybettiği»* ⛔). Denetçi bunu
`tutarsizlik` sayar ve kayıt düşer.

---

## §4 — Denetimler (betikle, yeniden kurmadan sonra)

1. **Zarf** — `v0.1.0` ile karşılaştırınca yalnız izinli alanlar farklı; yeni cevap = eski cevabın gövdesi + `son_cumle.yeni`.
2. **Temizlik** — yeni düşünmede ⛔/⭐, başlık, madde, kalın, üretim iskelesi ve *«soru sormuyorum»* ailesi yok.
3. **Alıntı** — kullanıcıya atfedilen tırnak içi söz konuşmada var; bulunamayanlar incelemeye düşer.
4. **`run_checks`** — mevcut bütün kayıt kapıları yeniden koşar.
5. **Karar eşlemesi** — `korunan_kararlar`'ın `eski`'si eski düşünmede, `yeni`'si yeni düşünmede birebir bulunur.
6. **Bağımsız karar korunumu okuması** — `prompts/karar-korunumu.v1.md`; kararı düşen, uydurma katan ya da cevapla çelişen düşünme reddedilir.
7. **Bitişi değişenler** — eski ve yeni cevap **aynı** judge ile, **aynı** dalgada, kör ve karışık sırayla yargılanır (K97). Güvenlik ya da rol sınırı ihlali çıkarsa, `grounding` ya da `mi_uyumu` düşerse bitiş değişikliği reddedilir.
8. **Korpus kalıp kapısı** (tam geçişte) — hiçbir düşünme cümlesi beş ya da daha fazla kayıtta birebir geçmez.

⭐ **Reddedilen yeniden kurma kaydı kaybettirmez:** kayıt `v0.1.0` hâliyle kalır.
