# Türkçe İfade Bankası

> **Ne için:** Faz 2+ üretiminde (Claude Code, K30) Türkçe terapötik register referansı.
> **Ne için DEĞİL:** klinik onay. Kaynak korpus DOĞRULANMAMIŞ (K26) — bir kalıbın burada
> olması "bu doğru cevap" demek değildir, yalnızca "Türkçede böyle bir cümle şekli var" demektir.
> Klinik doğruluk her zaman `docs/arastirma-notlari.md`'ye bağlanır.
>
> Kaynak: `reports/analiz/2026-09-12-turkce-ifade-bankasi.md` ← `scripts/analiz/2026-09-12-turkce-ifade-bankasi.py`
> (campaigns/ 2.240 + hf_ready_dataset_old 273, toplam 2.513 tamamlama, 6.875 cümle)
>
> **Kural (K20):** kalıp düzeyinde kullanılır — bu cümleler birebir kopyalanmaz, biçimleri
> (nasıl bağlandığı, hangi kelimelerle yumuşatıldığı) Türkçe yazarken referans alınır.

---

## ✅ Kullanılabilir kalıp kategorileri

### Yansıtma / doğrulama (EPITOME duygusal tepki, OARS Reflection)

Duyguyu adlandırıp meşrulaştıran, tavsiye vermeyen kapanışlar:

- *"Kafanın karışık olması bu yoğunlukta çok anlaşılır."*
- *"Bugün biraz konuşmak yerine sadece nefes almak istersen o da çok anlaşılır."*
- *"'Yorgunum' demen çok anlaşılır."*

Sık kalıp: **`{durum/duygu} ... çok anlaşılır`** · **`{duygu} olman önemli`** ·
**`bunu yargılamadan duyuyorum`**

### Çift yönlü yansıtma (ambivalans, TIP 35)

İki karşıt duyguyu aynı cümlede, biri diğerini geçersiz kılmadan tutmak:

- *"'Hem istiyorum hem yapamıyorum' cümlende ben şu an o 'istiyorum'u duyuyorum, küçük ama orada."*
- *"Bir yandan grupta tuhaf durmak istemiyorsun, öte yandan o yirmi liranın harçlıkta yer kapladığını fark ediyorsun; bu iki şeyi aynı anda görmen bence önemli."*

Sık kalıp: **`hem ... hem de ...`** · **`bir yandan ... diğer yandan ...`** ·
**`{X} hem {Y}`** (iki duygu bağlacı, sonra "bu ikisini aynı anda taşımak" tarzı kapanış)

### Özerklik saygısı (K1 kalın cümle, K21 dalkavukluk savunmasıyla karıştırılmasın)

Karar bildirmeden, kararı kullanıcıya bırakan cümleler — **onay değil, yalnızca yer açma**:

- *"Bırak demeyeceğim, o senin kararın..."*
- *"Çekip çekmemek senin kararın, ama bu kararı arkadaşların yerine sen verirsen sonradan kendine karşı daha tutarlı durabilirsin."*
- *"Senin yerine 'aç' ya da 'kapat' demek bana düşmez, bu senin kararın."*

⚠️ Bu kalıp **K21'in karşıtı gibi görünüp aslında onu tamamlar**: özerkliğe saygı,
kullanıcının hatalı bir inancını onaylamakla karıştırılmamalı (§16 anti-pattern).
Nazikçe karşı çıkma örnekleri bu korpusta ayrı, düşük sayıda (bkz. kapsama notu aşağıda).

### Yargısızlık

- *"Sigaranın o sessizlikle birlikte gelmesini de yargılamadan görüyorum..."*
- *"Bunu yargılamadan ama hafife de almadan duyuyorum..."*

Sık kalıp: **`{davranış/durum} yargılamadan {duyuyorum/görüyorum}`**

### Rol sınırı yönlendirme (Sor-Sun-Sor)

- *"Doktora bu soruyu sormaktan seni en çok çekindiren şey ne?"* — izin isteyip soruyla açma
- *"İki haftadır süren bir öksürüğün olması, doktora gitmek istemen çok önemli bir sezgi."* — yönlendirmeyi kullanıcının kendi sezgisine bağlama

---

## ❌ Kullanılmayacak kalıplar — K18 ihlali örnekleri

Ham çıkarımda **rol_siniri_yonlendirme** ve genel açılış kalıpları arasında doğrudan
numara içeren cümleler bulundu (10+ tekrar):

- ~~*"Hemen 112'yi ara..."*~~
- ~~*"ALO 182 üzerinden 7/24 ücretsiz bir uzmana ulaşabilirsin..."*~~
- ~~*"lütfen hemen ALO 182'yi ara ya da 112'yi arayıp en yakın acil servise ulaş"*~~

**K18 kararı:** model **kaynak türünü** adlandırır, numarayı **asla** söylemez —
uygulama (İP4) künyeyi render eder. Doğru kalıp şekli:

> *"...şu an bir kriz danışma hattını aramanı öneririm"* / *"...en yakın acil servise
> başvurmanı isterim"* (numara YOK, kurum adı YOK ya da yalnızca genel tür — "kriz hattı",
> "acil servis", "sağlık kuruluşu")

Bu, Oturum 9'daki 186-kayıt telefon bulgusunu **farklı bir yöntemle (cümle-açılış
frekansı) doğruluyor** — aynı ihlal iki ayrı ölçümle de görünür.

---

## ⚠️ Kapsama boşluğu — sıfır örnek

İki teknik kategoride **hiçbir eşleşme bulunamadı** (2.513 tamamlama, 6.875 cümle içinde):

| Teknik | Kaynak | Durum |
|---|---|---|
| **0-10 güven/hedef cetveli** | plan.md §4 teknik havuzu, TIP 35 | Korpusta **sıfır örnek** |
| **Dürtü somutlaştırma** ("fiziksel bir his mi, düşünce mi") | Marlatt, plan.md §4 | Korpusta **sıfır örnek** |

Bu iki teknik Faz 4'ün "kapsama açığı kapatma sırası" listesine eklenmeli — mevcut
korpus bu tekniklerde **hiç örnek vermiyor**, tamamen kendi üretimimize kalıyor
(ki zaten K20/K26 gereği klinik doğrulukları için elimizde referans yok, dolayısıyla
bu iki teknik `docs/arastirma-notlari.md`'deki kaynağa (SMART Recovery, Marlatt) çok
daha sıkı bağlı kalınarak üretilmeli).

---

## En sık cümle açılışları (register genel görünümü)

Ham liste `reports/analiz/2026-09-12-turkce-ifade-bankasi.md`'de. Genel gözlem:
kriz/güvenlik odaklı açılışlar ("Bu gece için…", "Şu an kendine…", "Şu an güvende…")
listenin başında — beklenen, çünkü kriz senaryoları yoğun şekilde temsil ediliyor
(bkz. Oturum 9: risk yüksek+çok yüksek %39, hedef %10 — kendi karışımımızda (§6)
bu oranı %10'a çekeceğiz, dolayısıyla bu açılışların üretimdeki ağırlığı korpustan düşük olmalı).
