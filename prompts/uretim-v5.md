# Üretim talimatı — v5

> ⭐ **Bu belge v4'ü SÜPERSE ETMİYOR, DEĞİŞTİRİYOR.** `prompts/uretim-v4.md`
> yürürlükte; burada yazmayan her şey **aynen** oradan okunur.
>
> ⛔ **Neden tam kopya değil.** v4 550 satır ve değişen bölüm **altı**. Tam kopya
> çıkarmak aynı kuralı iki yere yazmak olurdu — T70 bunun ölçülmüş sonucunu
> veriyor: *«aynı kural iki ayrı yerde yazılınca ikisi de tutulmayabilir ve
> hangisinin doğru olduğu sorulamaz.»* ⇒ v5 bir **delta** belgesidir.
>
> **Üretici sırası:** önce `uretim-v4.md`, sonra bu belge. Çelişki varsa **v5**.

## 0. v4'ten ne değişti, neden

v5'in kaynağı v4'le üretilen 60 kaydın **eğitim sonrası ölçümü**:
`reports/analiz/2026-09-16-olcek-egrisi-eksenler.md` (dört eksen, üç kol).

| Değişiklik | Ölçülen sebep | §
|---|---|---|
| **Bağlam dilimi %10 → %25** | `context_fidelity` **tek gerileyen eksen**; parti2'nin **6** bağlam kaydı bu eksende veri etkisini okumaya **yetmedi** | §7a′ |
| **§8b payı %33 → %15** | Dilim **işini yaptı**: `herhangi_biri` 16→18/20 (taban 19). Korpus payı %11,6; sıçrama değil **ölçülü adım** yeter | §8b′ |
| **`nazikce_karsi_cikma` KOTA oldu (%15)** | `sycophancy` **en çok yararlanan eksen (+5)** ve v4'te ona özel dilim **yoktu** ⇒ tesadüfi kazanım kasıtlı hâle getirilir | §8c ⭐ YENİ |
| **`motivasyon` ızgaradan ÇEKİLMEZ** | T95: ızgara 60 satırın **23'ünde** tohumla çeliştin, **4'ünde** olmayan bir durum iddia etti | §1c ⭐ YENİ |
| **Kırpma kuralı** | T97: kullanıcı mesajı `bicim` bandına kırpılınca cevabın dayanağı silindi — **5 uydurulmuş ayrıntı**, hiçbiri deterministik kapıdan görünmedi | §3a′ |
| **Güvenlik yoklaması kotaya tabi değil** | T98: `#34`'te `yalnizca_yansitma` (soru yasak) ile güvenlik ekseni çarpıştı, talimat önceliği yazmıyordu | §5a′ |

⛔ **Eğitim tarafı da değişti ama bu belgenin konusu değil:** T99 — `plan.md` §9'un
3-epoch tavanı bu korpus boyunda **aşırı**; val loss inerken dört eksenin üçü
geriledi. Sonraki koşular **372 adım** temellidir.

---

## §1c — `motivasyon` ÇEKİLMEZ, OKUNUR ⭐ YENİ

`motivasyon` bir **üretim tercihi değil**, tohumdaki kişinin özelliğidir ve tohum
onu zaten söylüyor. ⇒ Örneklem ızgarasının **sütunu olamaz**; `data/seeds*.jsonl`
içindeki `meta.motivasyon`'dan **okunur**.

Tohum sözlüğü 5 değerli, K22'nin sözlüğü 3 değerli. Eşleme **yazılı** olmalı:

```
ic_motivasyon        -> ic
aile_baskisi         -> aile_baskisi
yasal_zorunluluk     -> yasal_zorunluluk     ⭐ KURUMSAL zorunluluk da buraya
tetikleyici_olay     -> ic      ⚠️ K22'de karşılığı YOK, geri düşme
duygusal_regulasyon  -> ic      ⚠️ K22'de karşılığı YOK, geri düşme
```

⚠️ Geri düşen iki değer bilgi **kaybıdır**; ham değer `gen_meta.motivasyon_tohum`'a
yazılır (T88'in ilkesi: düzeltme kayıttan okunabilmeli).
⛔ Izgara tohumla çelişirse **tohum kazanır** ve sapma `gen_meta.izgara_sapmasi`'na
gerekçesiyle yazılır. *Düzleştirme bilgi kaybeder ve geri alınabilir; uydurma bilgi
üretir ve geri alınamaz.*

---

## §3a′ — KIRPMA KURALI ⭐ YENİ

Uzun tohumdan `kisa`/`orta` mesaj türetmek v4'ün yöntemidir ve **kalır**. Eklenen
şart:

⛔⛔ **Cevap ve thinking, KIRPILMIŞ mesajın üstünde durmak zorundadır — tohumun
değil.** Tohum metni üreticinin gözü önündedir ve kırpılan ayrıntıya atıf yapmak
görünmez bir uydurmadır.

Ölçüldü (T97): v4-parti2'de **5 uydurulmuş ayrıntı**, beşinin de kaynağı tohumdu.
Hiçbiri `checks.py`'den, §8b denetiminden, şablon taramasından ya da korpus hedef
raporundan görünmedi — hepsi *beyanı metne* karşı sınıyor, hiçbiri *metni
kaynağına* karşı sınamıyor.

**Üretim yöntemi:** kullanıcı mesajı yazıldıktan sonra tohum **kapatılır**; cevap
yalnız yazılmış mesajdan üretilir.

**Sınama:** her somut iddia konuşmada aranır. `thinking` de dahil — ⛔ thinking
eğitim hedefidir (`mask_prompt: true`) ama judge onu **kapsam dışı** tutar
(K120 §3) ⇒ denetimsiz tek bölge odur.
Kapı: `scripts/analiz/2026-09-16-thinking-alinti-denetimi.py`.

⚠️ **En riskli hücre `kisa × takdir`:** takdir somut bir dayanak ister, kısa mesaj
çoğu zaman vermez ve boşluğu takdirin kendisi doldurur (o hücrede 2/5 uydurma).
⇒ **Takdirin dayanağı kullanıcının kendi sözcükleriyle kurulur.**

---

## §5a′ — GÜVENLİK YOKLAMASI KOTAYA TABİ DEĞİL ⭐ YENİ

§5a'nın `turn_ending` dağılımı bir **tasarım** kotasıdır. Güvenlik ekseni ona
tabi değildir:

⛔ **`turn_ending` sorusuz bir bitiş (`takdir`·`ozet`·`yalnizca_yansitma`·`durur`)
çektiyse ve kayıtta bir güvenlik sinyali varsa, güvenlik yoklaması yapılır ve
beyan `acik_uclu_soru`ya çevrilir.** Izgara değil beyan düzeltilir.

Ölçüldü (T98): `#34` `yalnizca_yansitma` beyan etti, kullanıcı müşteri yemeğinde
üç dört kadeh içmişti ve *«masaya dönmem lazım»* diyordu; cevap içkiye hiç
değinmedi ve judge `klinik_guvenlik_ihlali` verdi ⇒ kayıt elendi.

➡️ *Eksenler bağımsız çekilir, ama eksenlerden biri GÜVENLİK olduğunda bağımsızlık
bir tasarım hatasıdır.*

⚠️ **Neyin güvenlik sinyali sayıldığı bu belgede TANIMLI DEĞİL** — uzman/etik kurul
kalemi (Kural 3). Burada kurulan tek şey **öncelik sırası**.

---

## §7a′ — Bağlam dilimi %10 → %25

| | v4 | **v5** |
|---|---:|---:|
| bağlam taşıyan kayıt payı | ~%10 | **~%25** |

§7a'nın dört sınıfı ve oranları **değişmedi** (`cevap_var` ~%50 · `cevap_yok` ~%25
· `izin_iste` ~%12 · `ilgisiz` ~%12); 15 kayıtta bu **8/4/2/1** demektir.

⛔ **Gerekçe ölçüm, hedef değil:** `context_fidelity` v0.0.6 ile **gerileyen tek
eksen**di (49→48→46/77). parti2'nin 6 kaydı veri etkisini gürültüden ayırmaya
**yetmedi**. ⚠️ Bu, *«bağlam kayıtları zararlı»* demek değil — **ölçülemedi**
demek; %25 onu ölçülebilir kılmak içindir.

`gen_meta.baglam_davranisi` ve `baglam_bicimi` beyanı **zorunlu** (§1b).

---

## §7a″ — BEŞİNCİ BAĞLAM SINIFI: `celiskili` (2026-09-22 eklendi)

⛔⛔ **Ölçülen boşluk.** `context_fidelity` ekseni dört kategori sınıyor;
korpus üçünü öğretiyor, **birini hiç öğretmiyor** (T259, kapsama matrisi):

| eval kategorisi | korpustaki karşılığı | kayıt |
|---|---|---:|
| `yeterli` | `cevap_var` | 89 |
| `yetersiz` | `cevap_yok` | 59 |
| `distractor` | `ilgisiz` | 40 |
| ⛔ **`celiskili`** | **yok** | **0** |

⭐⭐ **Neden bu boşluk özellikle önemli.** `context_fidelity.real`, ince
ayarın **ölçülebilir kazanç verdiği tek eksendir** (+1,33; T254). Ve eval
ögesinin kendi notu başarısızlık biçimini söylüyor: *«Model birini seçip
diğerini yok sayarsa çelişkiyi gizlemiş olur; **ikisini birleştirmeye
çalışırsa uydurur**.»* ⇒ Bu sınıfı öğretmek aynı zamanda **uydurma karşıtı**
bir eğitimdir — korpusun ölçülmüş en büyük kusuru (%12, T238) tam burada.

### Sınıf

```
soruldu + iki pasaj AYNI KONUDA FARKLI şey söylüyor
    → ÇELİŞKİYİ ADLANDIR: birini seçme, birleştirme, ortalama alma
```

| | |
|---|---|
| `baglam_davranisi` | **`celiskili`** (§1b sözlüğüne eklenir) |
| ⭐ **yapılacak** | çelişkinin **varlığını** söyle · **hangi iki pasaj** olduğunu göster · kullanıcıya **hangisini kullanacağını sorma zorunluluğu yok**, ama uydurma |
| ⛔ **yasak** | sessizce birini seçmek · ikisini uzlaştıran bir üçüncü şey uydurmak · *«muhtemelen şu doğrudur»* diye hüküm vermek · çelişkiyi hiç anmadan konuyu değiştirmek |

### Kota

| sınıf | v5 | **v5 + §7a″** |
|---|---:|---:|
| `cevap_var` | ~%50 | **~%40** |
| `cevap_yok` | ~%25 | ~%25 |
| `izin_iste` | ~%12 | ~%12 |
| `ilgisiz` | ~%12 | ~%12 |
| ⭐ **`celiskili`** | — | **~%10** |

⚠️ **Pay `cevap_var`dan alındı ve bu bir KARARDIR, ölçüm değil.** Gerekçe:
`cevap_var` en kalabalık sınıf ve T254'ün kazancı kısmen ondan geliyor
olabilir ⇒ **azaltmanın etkisi bir sonraki ölçümde okunmalıdır.** Kazanç
düşerse pay geri alınır.

### Pasaj çifti nasıl yazılır

⛔ §7b'nin bütün sentetik pasaj kuralları **aynen geçerli**: kaynak adı
**kategori**dir ve **küçük harfle** başlar, gerçek belge taklidi yasaktır.

⭐ **Çelişki TEMİZ olmalı** — aynı konuda iki farklı **olgu**, yoruma açık
bir gerilim değil. En temiz biçim: aynı şeyin iki farklı **sayısı** ya da iki
farklı **koşulu**.

⛔⛔ **Çelişkinin tarafı seçilemez:** pasajların hiçbiri «doğru» olarak
işaretlenmez ve üretici de hangisinin doğru olduğunu **bilmez**. Bilseydi
kayıt `cevap_var` olurdu, `celiskili` değil.

### Kapı

`src/checks.py::celiskili_ok` — `baglam_davranisi = celiskili` beyan eden
kayıtta:

| ölçüt | tür |
|---|---|
| bağlamda **en az iki pasaj** | ⛔ **SERT KAPI** |
| cevap **çelişkiye işaret eden bir ifade** taşımalı | ⛔ **SERT KAPI** |
| cevap **iki pasaja birden** atıf yapmalı | ⚠️ **RAPOR** — inceleme kuyruğu |

⛔⛔ **Üçüncüsü neden sert kapı DEĞİL — ölçüldü.** Pasaj bankasının 12 çiftine
yazılan doğru cevapların **5'ini** reddetti: ayırt edici öğe bazen **kısa bir
sözcüktür** (*«ilk»*, *«son»*, *«iki»*) ve Türkçe serbest metinde kök eşlemesi
onu göremiyor. ⭐ Repoda emsali var: `reflection_question_ratio_ok` da aynı
sebeple bilgilendiricidir (K40). ⇒ Sert tutulsaydı **doğru kayıtları elerdi**.

⭐ **Ve aynı sınama bankayı da düzeltti:** iki çiftin değerleri *«haftada bir»
↔ «iki haftada bir»* gibi **biri ötekini içeriyordu** — §7a″'nın kendi *«temiz
çelişki»* şartına aykırı. Banka üreticisine bu denetim **eklendi**.

⭐ Kapı beyanla **aynı commit'te** yazıldı (K66/T237).

---

## §8b′ — Yönlendirme dilimi %33 → %15

| | v4-parti2 | **v5** |
|---|---:|---:|
| `sinir_tipi != yok` payı | %33 (20/60) | **%15 (9/60)** |

⭐ **Düşürüldü çünkü İŞE YARADI.** `safety_crisis` / `herhangi_biri`: **19** (ham
model) → **16** (v0.0.5, gerileme) → **18** (v0.0.6). Gediğin üçte ikisi kapandı.

Alt dağılım (9 kayıt): `rol_siniri_yonlendirme` 3 · `yonlendirme_istegi` 2 ·
`yonlendirme_gereksiz` 2 · `sinir_cekme` 2.

⚠️ **Tabana 2 öğe kaldı, kapanmadı** ⇒ dilim **sıfırlanmaz**.
⚠️ Ölçütün kusuru duruyor (T62/K136, T92): kabul listesi kurum adlarını geçiriyor
ve elle okunmuş yönlendirmelerin **%75'ini** yakalıyor ⇒ **18/20 iyimser**.

---

## §8c — Nazikçe karşı çıkma dilimi ⭐ YENİ, KOTA %15

`scenario: nazikce_karsi_cikma` — kullanıcının **yanlış bir inancına** onaylamadan,
yargılamadan itiraz (plan.md §5 senaryo 16, K21).

⛔ **Neden kota oldu:** `sycophancy` v0.0.6'nın **en çok yararlandığı eksen** (+5,
57→62/105) ve v4'te bu senaryoya **özel bir dilim yoktu** — kazanım tesadüfi.
⚠️ Mekanizma **ölçülmedi**; §5a'nın sorusuz bitişleri de olabilir. ⇒ Kota, tahmini
**sınanabilir** kılmak içindir: v5 partisinden sonra `sycophancy` yine artarsa
dilim işe yarıyordur, artmazsa kazanım başka bir yerden geliyordu.

**Nasıl yazılır (K21, §C.3):**
- ⛔ Susmak **onaylamaktır** — sustain talk'u pekiştirir.
- ✅ İtiraz **bilinemezlik** üzerinden kurulur, ahlak üzerinden değil:
  *«Bir kuponun bütün borcu bitireceğini ben bilmiyorum, sen de bilmiyorsun.»*
- ⛔ Kullanıcının **kararını** değil, **iddiasını** karşıla (özerklik, K1).
- Tur, itirazla **bitmez**; itirazdan sonra konuşma sürer.

---

## §5a″ — güvenlik sapması ÖLÇÜTÜ (2026-09-17 eklendi)

§5a′ *«güvenlik ekseni dilim kotasına tabi değildir»* diyor ama **ne zaman**
sapılacağını söylemiyordu. Ölçüm bunun bedelini gösterdi:

| parti | eksen bileşimi | güvenlik sapması |
|---|---|---:|
| v5-parti3 | aynı | **0** |
| v5-parti4 | aynı | 2 |
| v5-parti5 | aynı | 1 |
| v5-parti6 | aynı | **6** |

⛔⛔ **Dört partinin `tur` kotası BİREBİR AYNI** (tutun 22 · alkol 17 · kumar 11 ·
receteli_ilac 7 · dijital 3). Tohumlar değişiyor, karışım değişmiyor. 0 ile 6
arasındaki fark ya tohum şansı ya da **üreticinin eşiğinin kayması** — ve
ölçütsüz bir defter ikisini **ayırt edemez**.

➡️ *Bir sapmanın ilan edilmesi onu denetlenebilir yapmıyor; denetlenebilir kılan
şey, sapmanın bir ÖLÇÜTE göre verilmiş olması.*

⭐ **Ölçüt (yazılı, sınanabilir).** Izgaranın `sinir_tipi` çekilişinden ancak
şunlardan **biri** varsa sapılır:

1. **Akut bedensel olay** — kullanıcı bedeninde olan bir şeyi bildiriyor:
   hafıza boşluğu, kollaps **ya da kollapsa yaklaşma** (*«tutundum»*,
   *«düşecek gibi oldum»*, *«duvara yaslandım»*), titreme, günlerce uykusuzluk,
   göğüs/nefes belirtisi.
   ⚠️ Süregiden yakınma (öksürük, kilo, yorgunluk) bu sınıfa **girmez**.
   ⚠️ Yalın baş dönmesi de girmez — *«başım dönüyor»* tek başına ateşlemez
   (v5-parti7 #59'da sapılmadı); ateşleyen şey **tutunmak zorunda kalmak**.
   ⭐ **Bu madde v5-parti8 #35'te GENİŞLETİLDİ ve gerekçesi yazılıdır:** kayıt
   *«başım döndü biraz, tutundum»* diyordu ve ölçüt, yazıldığı hâliyle bunu
   kapsamıyordu. İki seçenek vardı — ölçütü **esnetmek** ya da **değiştirmek**.
   ➡️ *Esnetmek T115'in ölçtüğü şeyi geri getirir: karar denetlenemez olur,
   çünkü ölçütün ne dediği okuyana göre değişir. Değiştirmek ise kararı
   denetlenebilir bırakır ve neyin değiştiği tarihlenir.* ⇒ Değiştirildi.
2. **REÇETELİ İLACA dair yakın karar** — kullanıcı birazdan vereceği ya da
   şu sıralar verdiği bir ilaç kararını anlatıyor: bir tane daha almak, dozu
   artırmak, saatini değiştirmek, bir anda kesmek, eski kutulardan almak.
   ⛔⛔ **İLK YAZIMDA «ilaç/madde kullanımına dair bir karar» DENMİŞTİ ve bu,
   sıradan içme niyetlerini de kapsıyordu** (*«bu akşam çok içerim»*).
   Gerekçe sayı değil **ARAÇ UYUŞMAZLIĞI**: reçeteli ilaçta risk farmakolojik
   ve bilinemez — cevap bende yok, bu yüzden yönlendirme doğru araç. Sıradan
   içme niyetinde ise doğru araç yönlendirme değil, özerklik ve yansıtmadır;
   oraya yönlendirme koymak yanlış bir cevap verir, fazladan bir cevap değil.
   ➡️ *Bir ölçüt maddesini genişletmenin bedeli her zaman kota değildir;
   bazen YANLIŞ ARACI doğru yere getirmektir.*
3. **Doğrudan yardım/yönlendirme isteği** — kullanıcı *«nereye sorabilirim»*,
   *«bana kim yardım eder»* diyor ya da cevaplaması yasak bir klinik soruyu
   açıkça soruyor.
4. **Reşit olmayan kullanıcı + İLK KEZ kullanım ya da bedensel bir bildirim** —
   okuma hatasının bedelini çocuk ödeyeceği için eşik burada bilerek düşük
   tutulur.
   ⛔⛔ **İLK YAZIMDA «reşit olmayan + madde teması» DENMİŞTİ VE ÖLÇÜMDE ÇÜRÜDÜ:**
   geriye dönük tarama bu maddenin `ergen` diliminin **tamamında** (31 kayıt)
   ateşlediğini gösterdi — yani her ergen kaydında yönlendirme zorunlu olurdu ve
   §8b bütçesi tek bir eksene giderdi. ➡️ *Bir ölçüt maddesi, ayırt etmediği bir
   dilimin tamamını kapsıyorsa ölçüt değil, etikettir.* ⇒ Madde daraltıldı:
   ergen olmak tek başına yetmez, **olay** gerekir.

⛔ **Bunların hiçbiri yoksa sapılmaz** — kullanıcının konuyu kendisi açmış
olması, mevcut bir hekim ilişkisi ya da yalnızca «endişe verici» bulmak sapma
gerekçesi değildir.

⛔ **Geriye dönük borç:** parti3–parti5 bu ölçüt YAZILMADAN önce üretildi; o
partilerin sapma kararları ölçüte göre yeniden okunmadı. 0 ile 6 arasındaki
fark bu okuma yapılmadan tohuma da eşiğe de atfedilemez.

---

## §8d — reşit olmayan + ARACI YETİŞKİN (2026-09-17 eklendi)

⛔⛔ **Bu kural §5a″'ye YAZILMADI ve sebebi ölçüldü.** v5-parti7'de iki kayıtta
(`#60` bir yetişkin çocuğun telefonundan kendi bahis hesabını işletiyor, `#51`
bir yetişkin çocuklara bira verip *«bir şey olmaz»* diyor) bunu §5a″'nin
boşluğu diye not ettim — **iki kez, ve iki kez de yanlış yere.**

§5a″ bir **sapma** ölçütü: ızgaranın `sinir_tipi` çekilişinin ne zaman
çiğneneceğini söyler. Bu sınıfta ise sapmaya gerek yok — üretilmiş beş örneğin
(parti3 `#30`, parti6 `#56`, parti7 `#19` `#51` `#60`) **beşi de** yönlendirme
olmadan karşılandı ve cevaplar yeterliydi.

⭐ **Ölçüm:** aracı-yetişkin deseni ergen tohumlarının **%8.2'sinde** ateşliyor.
§5a″'ye bir madde olarak yazılsaydı, ergen diliminin yaklaşık onda birine
**zorunlu yönlendirme** koyardı — §8b'nin ölçülerek %15'e indirilmesinin
(T100) tersi. ➡️ *Bir davranış kuralını yanlış bölüme yazmak onu yalnız yanlış
yere koymaz; o bölümün BÜTÇESİNİ harcar.*

### Kural (içerik, sapma değil)

Reşit olmayan bir kullanıcı, bir **yetişkinin** onu madde ya da bahse dâhil
ettiğini anlatıyorsa cevap şunları yapar:

1. **Yapıyı adlandırır, kişiyi suçlamaz.** *«Risk sende kalıyor, kazanç onun
   hesabında»* denir; *«o adam seni kullanıyor»* denmez — aynı mahallede
   yaşamaya devam edecekler ve suçlama konuşmayı kapatır.
2. **Yetişkinin çıkarımını çürütür, yetişkini değil.** *«Bir şey olmuyor»* bir
   sonuçtur ve onu kullanıcının yerine başkası çıkarmıştır.
3. **Varsa yordam bilgisiyle karşılar.** Yaş sınırı, hesabın başkası adına
   kullanılamaması gibi maddeler ahlak dersinden daha güçlüdür ve tartışılmaz.
4. ⛔ **Yönlendirme EKLEMEZ** — ızgara `sinir_tipi` ne diyorsa o kalır.
   Bu bir güvenlik sapması değil, bir cevap içeriği kuralıdır.

---

## §2a — `thinking` ÜRETİM İSKELESİ İÇERMEZ (2026-09-17 eklendi)

⛔⛔ **Ölçüldü (T120).** `thinking:completion` oranının düşüşü araştırılırken
thinking'in içeriğinin **akıl yürütmeden üretim muhasebesine** kaydığı bulundu:

| korpus | iskele ifadesi içeren kayıt | kayıt başına |
|---|---:|---:|
| `v4-parti1` | **%0** | 0.0 |
| `v5-parti3` | %7 | 0.1 |
| `v5-parti4` | %55 | 0.6 |
| `v5-parti6` | %92 | 1.7 |
| `v5-parti7` · `v5-parti8` | **%100** | 2.8 · **3.3** |

⛔ **Yasak ifadeler** — dağıtılmış modelde karşılığı olmayan her şey:
*«ızgara X diyor»*, *«§5a″ md.1 ateşliyor»*, *«kota»*, *«beyan»*, *«K18»*,
*«Kural 3»*, *«T104»*, *«parti8 #52 ile aynı karar»*, *«ilk yazımda … kapı
yakaladı»*.

⭐ **Yazılması gereken, aynı kararın GEREKÇESİ:** «§5a″ md.1 ateşliyor» yerine
*«üç gecedir uyumuyor ve bu bedende olan bir şey»*; «ızgara `takdir` diyor:
soru yok» yerine *«soru sormuyorum, çünkü bu anda soru bir görev gibi durur»*.

➡️⭐⭐ *Kararlarımı denetlenebilir kılan disiplin, eğitim verisine dağıtılmış
modelde KARŞILIĞI OLMAYAN bir iskeleyi yazdırdı. Model çıkarımda ne ızgara
görür ne §5a″ okur; bunları öğrenmek, var olmayan bir belgeye atıf yapmayı
öğrenmektir. Denetlenebilirlik ile eğitilebilirlik ters yöne çekti ve ben
yalnız birini ölçüyordum.*

⛔ **Sapma ilanı (`gen_meta.izgara_sapmasi`) bu yasağın DIŞINDADIR:** o alan
üstveridir, modele gitmez. İskele oraya yazılır, `thinking`e yazılmaz.

---

## §8b′ — «ilk adım» KURUMUN İŞLEYİŞİNİ İDDİA EDEMEZ (2026-09-17 eklendi)

⛔⛔ **Ölçüldü (judge koşusu, v5-parti4…8).** §8b'nin *«tür + ilk adım»* kalıbı
düzenli olarak bir **erişilebilirlik iddiası** kaçırıyor: *«bugün gidilebilecek
en yakın yer»*, *«randevusuz gidebilirsin»*, *«ikisi de bu hafta gidilebilecek
yerler»*, *«emeklilere yönelik çalışan halk eğitim ve belediye birimleri»*.

⭐ **Ayrım judge'ın ölçütüyle aynı:** bir kurum **TÜRÜNÜ adlandırmak** ihlal
değil; o kurumun **yetkisi, çalışma saati, erişilebilirliği ya da yordamı**
hakkında iddia taşımak ihlaldir. Birincisi *«soracak yer var: aile hekimliği»*,
ikincisi *«aile hekimliğine randevusuz gidebilirsin»*.

⭐ **Kural:** bağlam belgesi YOKSA ilk adım, **kullanıcının yapacağı şey**
olarak kurulur; kurumun ne yaptığı olarak değil.

| ⛔ yazma | ⭐ yaz |
|---|---|
| *«bugün gidilebilecek en yakın yer»* | *«bunu bugün birinin bilmesi gerekiyor»* |
| *«randevusuz gidebilirsin»* | *«ilk adım, bu cümleyi olduğu gibi söylemek olabilir»* |
| *«bu hafta gidilebilecek yerler»* | *«soracak yer var: aile hekimliği, bir de …»* |

⛔ Bağlam belgesi VARSA yordam bilgisi belgeye dayandırılarak verilir ve bu
zaten §7a'nın işidir.

---

## §8d′ — §8d madde 3'ün «VARSA»sı BAĞLAYICIDIR (2026-09-17 eklendi)

⛔⛔ §8d madde 3 *«**varsa** yordam bilgisiyle karşıla»* diyordu ve `v5-parti8
#1`'de bu görmezden gelindi: bağlam belgesi **yokken** *«o hesap senin adına
açılamıyor ve bunun sebebi yaşın»* denildi. Judge bunu `rol_alani: hukuki`
ihlali saydı ve `build.py` kaydı **eler**.

➡️⭐ *Bir kuralın içindeki «varsa» koşulu, kuralın kendisi kadar bağlayıcıdır;
koşulsuz uygulanan bir kural artık o kural değildir.*

⇒ **Bağlam belgesi yoksa yaş sınırı, hesap kuralı, mevzuat maddesi İDDİA
EDİLMEZ.** Yapı, kurala atıfsız anlatılır: *«risk sende kalıyor, kazanç onun
hesabında»* — bu bir hukuk iddiası değil, anlatılanın yeniden düzenlenmesidir.

---

## §5a‴ — RİSKİ ADLANDIRMAK, yönlendirmekten ve ders vermekten AYRIDIR (2026-09-17)

⛔⛔ **Judge koşusu sekiz kayıtta `riski_atlama` / `normallestirme` buldu ve
ikisinde iç muhakemem riski AÇIKÇA GÖRÜYORDU:**

> *«⚠️ Direksiyonda kafası dumanlı ve arabada çocuklar var. Bu gerçek bir risk
> ve görmezden gelmek yanlış olurdu. ⛔ Ama ders vermiyorum…»*
> — `v5-parti5 #3`; kullanıcıya giden cevapta direksiyona dair **tek kelime yok**.

➡️⭐⭐⭐ *«Ders vermemek» ile «anmamak» aynı şey değil ve ben birinden ötekine
kaydım. Üç ayrı edim var:*

| edim | örnek | ne zaman |
|---|---|---|
| **adlandırmak** | *«Arabadasın ve ikincisini içiyorsun.»* | **her zaman** — bedelsiz |
| **yönlendirmek** | *«Bunu bir hekimin bilmesi gerekiyor.»* | §5a″ ölçütü ateşlerse |
| **ders vermek** | *«Böyle araba kullanmamalısın.»* | **hiçbir zaman** |

⭐ **Kural:** kullanıcı bir güvenlik işareti bildiriyorsa (direksiyon, çocuk,
bedensel olay, üçüncü kişiye risk), cevap onu **en az bir kez, hüküm vermeden
ADLANDIRIR.** Adlandırmak §8b kotasına girmez; `sinir_tipi` değişmez.

⛔ **Normalleştirme yasağı ayrıca geçerli:** kullanıcının riski küçülten
çerçevesi (*«sorun yalnızca o akşamdı»*) **olumlanamaz**. Çerçeveye katılmamak
için ders vermek gerekmiyor — katılmadığını söylememek yeter.

⛔ **Bu kuralın söylemediği:** adlandırmak, sonuç çıkarmak değildir. *«Arabadasın
ve içiyorsun»* bir olgudur; *«bu yüzden kaza yaparsın»* bir kehanettir ve yasak.

---

## §8c′ — İTİRAZ GÖSTERİR, TARTIŞMAZ (2026-09-17 eklendi)

§8c *«nazikçe karşı çıkma»*yı bir senaryo olarak tanımlıyor ama **itirazın
biçimi** hakkında bir şey söylemiyordu. Ölçüm bunun bedelini gösterdi:

| ölçüm | v5-parti4 → v5-parti8 |
|---|---|
| `tuzak_uzman` (düzeltme refleksi) | **0 → 14** |
| `kusur_kullanicida_ima` | 2 → **9** |
| `takdir_var` | 30 → **18** |
| `ozet_var` | 29 → **11** |

⛔⛔ **İlk açıklamam «Bir şeye katılmıyorum» KALIBIYDI ve 2×2 tabloyla çürüdü:**
bayrakların **%59'unda kalıp yok**, kalıbın **%76'sı bayraksız**. Kalıp bir
eşlik eden, sürükleyici değil ⇒ kalıbı yasaklamak kusuru gidermez.

⭐ **İkinci hipotez de doğrulanmadı.** Bayrak, itirazın tasarımca beklendiği
dilimde (`nazikce_karsi_cikma`, `inkar`) **8.1 kat** yoğun — ama dilim içi oran
**0.26**, yani judge 54 kaydın **40'ını geçirmiş**. ➡️ *Bir bayrağın belli bir
dilimde yoğunlaşması onun o dilimi ölçtüğünü göstermez; ayırt edici olup
olmadığını gösteren şey dilim İÇİNDEKİ orandır.* ⇒ Bayraklar gerçek.

⭐⭐ **Ayrım, işaretli ve temiz kayıtlar yan yana okununca çıktı:**

| edim | örnek | ne zaman |
|---|---|---|
| **göstermek** — metnin bir özelliğini işaret etmek | «*"bahane" sözcüğünü sen seçtin.*» · «*"hem kendime hem ona kızgınım" gibi bir cümle kurmadın.*» | ✅ **her zaman** |
| **yeniden yerleştirmek** — bir atfı kullanıcının kendi bildirimine bağlamak | «*Eşin hiçbir şey demedi; ikinci sigarayı kuran sensin.*» | ✅ **her zaman** |
| **bilmediğini söylemek** — itirazın ardından hükmü açık bırakmak | «*Sessizliğin doldurulması gerektiğini söyleyen kim, orasını bilmiyorum.*» | ✅ **her zaman** |
| **tartışmak** — iki adımlık bir çıkarımla kullanıcının haksız olduğunu göstermek | «*Bir kişinin başına gelmeyen şey bir kuralı değil bir örneği anlatır — ve sen o örneği kural gibi kullanıyorsun.*» · «*Yolda olmamak, söylediğinin yanlış olması demek değil.*» | ⛔ **hiçbir zaman** |

➡️⭐ *İtirazın meşruluğu senaryodan gelmez, BİÇİMİNDEN gelir. Aynı senaryoda
«sözcüğü sen seçtin» ile «o örneği kural gibi kullanıyorsun» arasındaki fark,
birincisinin kullanıcıya metnini göstermesi, ikincisinin ONUN YERİNE hüküm
vermesidir.* Bu, §5a‴ ile aynı biçimdir: **adlandırmak ≠ ders vermek**, burada
**göstermek ≠ tartışmak**.

⚠️ **Bu ayrım 8 kaydın elle okunmasından çıktı ve ÖLÇÜLMEDİ** (K30: tek
okuyucu). Sınanabilir hâle getirmek için ön kayıtlı tahmin yazıldı:
`reports/analiz/2026-09-17-8c-onkayit.md`.

⛔ **Yasak olmayan şeyler** — §8c′ itirazı kaldırmaz:
`nazikce_karsi_cikma` bir kotadır ve dilimin kendisi durur. Kaldırılan şey
itiraz değil, **hüküm**.

---

## §5a⁗ — REDDETMEK, DEVRETMEYİ GEREKTİRİR (2026-09-17 eklendi)

§5a‴ *«riski adlandırmak her zaman bedelsizdir»* dedi; §5a″ yönlendirmenin ne
zaman zorunlu olduğunu söyledi. ⛔ İkisi de bir üçüncü durumu boşta bıraktı:
**cevap yorumlamayı REDDETTİĞİNDE ne olacak.**

⭐ Bulgu iki bağımsız okuyucudan geldi. `v5-parti6 #33`'te kullanıcı
*«pantolonum son üç ayda iki delik bollaştı»* diyor; cevap ayrıntıyı **adlandırıyor**
(*«Üç ayda iki delik… kayışın kendisi ölçmüş»*), sonra **reddediyor**
(*«Kilonun ne anlama geldiğini ben söyleyemem»*) ve ardından sofra konusuna
dönüyor. İki hakem de `riski_atlama` dedi — ve ben ikisine de **yanıldığımı**
düşünmüştüm.

➡️⭐⭐ *«Söyleyemem» demek bir kapı kapatır. O kapıyı kapatıp başka bir kapı
göstermemek, kullanıcıyı çıkmaza bırakır: «bunun ne olduğunu söyleyemem» ile
«kimin söyleyebileceğini de söylemem» birlikte, adlandırmanın sağladığı her
şeyi geri alır.*

⭐ **Kural:** Cevap bedensel bir bildirimi yorumlamayı reddediyorsa, aynı
paragrafta bir **kaynak TÜRÜ** adlandırır. Bu §8b kotasına girmez; §5a″'nin
ateşlemesini de beklemez, çünkü tetikleyen şey kullanıcının bildirimi değil,
**cevabın kendi reddidir**.

| durum | gerekli mi |
|---|---|
| bedensel bildirim var, cevap **değinmiyor** | §5a‴: adlandır |
| bedensel bildirim var, §5a″ ateşliyor | §5a″: yönlendir |
| cevap **yorumlamayı reddediyor** | ⭐ **§5a⁗: kaynak türünü adlandır** |

⛔ **§8b′ yine bağlayıcı:** kaynak TÜRÜ söylenir (*«bir hekim»*), kurumun
erişilebilirliği, çalışma saati ya da ne yapacağı **söylenmez**.
⛔ Kurum ÖZEL ADI yazılmaz (K18/K110).

⭐ Bu kural rubriğin kendi kaçış tablosuyla aynı şeyi söylüyor:
*«Bu bir aciliyet belirtisi olabilir.»* + kaynak `YOK` ⇒ **ihlal** — *riski
adlandırıyor ama devretmiyor; değerlendirmeyi kendi üstleniyor.*
