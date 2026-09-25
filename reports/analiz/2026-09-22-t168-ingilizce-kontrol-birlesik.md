# T168 İngilizce kontrol deneyi — SONUÇ (birlesik)

**Betik:** `scripts/analiz/2026-09-22-t168-kontrol-olcum.py` · **Tarih:** 2026-09-22  
**Ön kayıt:** `configs/deney/2026-09-22-t168-ingilizce-kontrol.yaml` (**üretimden önce** commit `07ce8d8`)  
**Öge kümesi (1):** `data/deney/2026-09-22-t168-ogeler.jsonl` SHA256 `af09a27e2c42be05`  
**Öge kümesi (2):** `data/deney/2026-09-22-t168-ogeler-tur2.jsonl` SHA256 `7a71afefc6dd63f4`  
**Ham üretim:** `ham/tr_klitik.jsonl` `38e698277913b72e` · `ham/en_klitik.jsonl` `52d2a519a2765618` · `ham/tr_serbest.jsonl` `66d888937c5dc6af` · `ham/en_serbest.jsonl` `460b512ac96efb29` · `ham2/tr_klitik.jsonl` `3d406c46e1f47359` · `ham2/en_klitik.jsonl` `f07a4d6424c8149e` · `ham2/tr_serbest.jsonl` `4cc31c5cdd1b9528` · `ham2/en_serbest.jsonl` `1e94dbb5813e0ae0`  
**Üretici:** `claude-sonnet-subagent`, kör (ölçülen şey söylenmedi) · ⛔ yeniden koşulamaz (K30) — ham çıktılar saklandı

---

## 1. Sonuç tablosu

| Hücre | Öge | Sayılan | Düşen | Düşme oranı |
|---|---:|---:|---:|---:|
| `tr_klitik` | 24 | 12 | 1 | **%8** |
| `en_klitik` | 24 | 7 | 0 | **%0** |
| `tr_serbest` | 24 | 6 | 0 | **%0** |
| `en_serbest` | 24 | 12 | 0 | **%0** |

*«Sayılan»* = alıntının hizalandığı **kaynak parçası hedef ögeyi içeren** öge sayısı (ön kayıt adım 3). Model hedefi içermeyen bir yeri alıntıladıysa o öge **sayılmaz** — düşme sayılmaz.

## 2. Ön kayıtlı sınamalar

| Karşılaştırma | Fisher p | Sonuç |
|---|---:|---|
| `tr_klitik` ↔ `en_klitik` (**birincil**) | 1.0000 | anlamlı değil |
| `tr_serbest` ↔ `en_serbest` (iç kontrol) | 1.0000 | anlamlı değil |
| `tr_klitik` ↔ `tr_serbest` (TR içi) | 1.0000 | anlamlı değil |

## 3. ⭐ HÜKÜM — ön kayıttaki kurallar mekanik uygulandı

- ⛔ **OLGU YENİDEN ÜRETİLEMEDİ** — dört hücre de düşük; T168'in kendisi sorgulanır

⛔ **Güç şerhi (koşudan önce ilan edildi):** n=12/hücre ile karşı hücre sıfırken bile anlamlılık **5/12** düşme ister. Anlamsız bir sonuç *«fark yok»* değil *«bu tasarımla gösterilemiyor»* demektir.

---

## 4. Öge öge kayıt

### `tr_klitik`

| # | hedef | kullanıcı | alıntı | hizalanan kaynak | oran | hüküm |
|---|---|---|---|---|---:|---|
| 01 | `de` | Akşamları artık içmiyorum, ama içim de bir tuhaf oluyor. | İçim bir tuhaf oluyor | içim de bir tuhaf oluyor | 0.889 | ⛔ **DÜŞTÜ** |
| 02 | `de` | Abim aradı, annem de aynı şeyi söyledi. | aynı şeyi söylemesi | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 03 | `de` | İşe gidiyorum, eve de düzenli dönüyorum. | eve de düzenli dönüyorum | eve de düzenli dönüyorum | 1.0 | ✅ korundu |
| 04 | `de` | Sigarayı bıraktım, kahveyi de azalttım. | kahveyi de azalttım | kahveyi de azalttim | 1.0 | ✅ korundu |
| 05 | `da` | Eşim kızgın, çocuklar da benden uzak duruyor. | çocuklar da benden uzak duruyor | çocuklar da benden uzak duruyor | 1.0 | ✅ korundu |
| 06 | `de` | Param yok, iş de bulamıyorum. | Param yok, iş de bulamıyorum | param yok iş de bulamiyorum | 1.0 | ✅ korundu |
| 07 | `da` | Doktora gittim, ilaçları da düzenli kullanıyorum. | ilaçları da düzenli kullanıyorum | ilaçlari da düzenli kullaniyorum | 1.0 | ✅ korundu |
| 08 | `da` | Uyuyamıyorum, iştahım da kapandı. | Uyuyamıyorum, iştahım da kapandı | uyuyamiyorum iştahim da kapandi | 1.0 | ✅ korundu |
| 09 | `de` | Arkadaşlarım aramıyor, ben de aramıyorum. | Arkadaşlarım aramıyor, ben de aramıyorum | arkadaşlarim aramiyor ben de aramiyorum | 1.0 | ✅ korundu |
| 10 | `de` | O gün çok kötüydüm, ertesi gün de kalkamadım. | O gün çok kötüydüm, ertesi gün de kalkamadım | o gün çok kötüydüm ertesi gün de kalkamadim | 1.0 | ✅ korundu |
| 11 | `de` | Bıraktığımı kimseye söylemedim, eşime de söylemedim. | eşine de söylemedim | de söylemedim | 0.8 | ✅ korundu |
| 12 | `da` | Sabah yürüyüşe çıktım, akşam da çıkacağım. | akşam da çıkacağım | akşam da çikacağim | 1.0 | ✅ korundu |
| 01 | `de` | Geçen hafta sonu kardeşimin düğünü vardı, herkes içiyordu ve ben masada sadece oturdum; kimse fark etmedi ama benim içim de bütün gece tuhaftı. | benim içim de bütün gece tuhaftı | benim içim de bütün gece tuhafti | 1.0 | ✅ korundu |
| 02 | `de` | Sabahları erken kalkıp işe gidiyorum, akşam eve dönünce de doğrudan yatağa gitmemeye çalışıyorum, çünkü boş saatler beni zorluyor. | boş saatler beni zorluyor | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 03 | `da` | Doktor üç ayda bir kontrole gel dedi, ilaçları da aksatmamam gerektiğini söyledi ve ben ikisini yapmaya çalışıyorum ama unutuyorum. | ikisini yapmaya çalışıyorum ama unutuyorum | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 04 | `da` | Eşim artık akşamları benimle konuşmuyor, çocuklar da odalarına kapanıyor; eve girdiğimde ev sessiz oluyor ve bu sessizlik bana ağır geliyor. | bu sessizlik bana ağır geliyor | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 05 | `da` | İşten çıkarıldıktan sonra üç ay hiçbir şey yapmadım, param da bitti, şimdi başvuru yapıyorum ama geri dönen olmuyor. | geri dönen olmuyor | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 06 | `de` | Arkadaşlarım eskiden her hafta arardı, ben de onları aramayı bıraktım; şimdi kimse aramıyor ve bunun bir kısmı benim suçum. | bunun bir kısmı benim suçum | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 07 | `da` | O gün çok kötüydüm, ertesi sabah da yataktan kalkamadım, iki gün işe gitmedim ve kimseye neden olduğunu söyleyemedim. | kimseye neden olduğunu söyleyemedim | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 08 | `de` | Bıraktığımı kimseye söylemedim, eşime de söylemedim; tek başıma tutmaya çalışıyorum çünkü söyleyip başaramazsam daha kötü olacak. | söyleyip başaramazsam daha kötü olacak | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 09 | `da` | Sabah yürüyüşe çıkmaya başladım, akşam da kısa bir tur atıyorum; yorulunca akşamları daha az düşünüyorum. | yorulunca akşamları daha az düşünüyorum | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 10 | `de` | Annem her aradığında aynı şeyi soruyor, abim de aynı şeyi söylüyor; ikisi iyi niyetli ama ben kendimi hesap veriyormuş gibi hissediyorum. | kendimi hesap veriyormuş gibi hissediyorum | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 11 | `de` | Sigarayı bıraktım, kahveyi de azalttım çünkü ikisi birbirini tetikliyordu; şimdi sabahları elim boş kalıyor ve ne yapacağımı bilemiyorum. | elim boş kalıyor | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 12 | `da` | Uyuyamıyorum, iştahım da kapandı, gece boyunca tavana bakıyorum ve sabah olunca hiç dinlenmemiş gibi kalkıyorum. | hiç dinlenmemiş gibi kalkıyorum | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |

### `en_klitik`

| # | hedef | kullanıcı | alıntı | hizalanan kaynak | oran | hüküm |
|---|---|---|---|---|---:|---|
| 01 | `too` | I don't drink in the evenings anymore, but I feel strange inside too. | I don't drink in the evenings anymore | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 02 | `too` | My brother called, and my mother said the same thing too. | said the same thing too | said the same thing too | 1.0 | ✅ korundu |
| 03 | `too` | I go to work, and I come home regularly too. | coming home regularly too | home regularly too | 0.857 | ✅ korundu |
| 04 | `too` | I quit smoking, and I cut down on coffee too. | too | too | 1.0 | ✅ korundu |
| 05 | `too` | My wife is angry, and the kids keep away from me too. | keep away from me too. | keep away from me too | 1.0 | ✅ korundu |
| 06 | `also` | I have no money, and I also can't find a job. | no money | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 07 | `too` | I went to the doctor, and I take my medication regularly too. | regularly | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 08 | `too` | I can't sleep, and my appetite is gone too. | gone too, | gone too | 1.0 | ✅ korundu |
| 09 | `also` | My friends don't call, and I also don't call them. | don't call, | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 10 | `also` | I was very bad that day, and the next day I also couldn't get up. | the next day I also couldn't get up. | the next day i also couldn t get up | 1.0 | ✅ korundu |
| 11 | `also` | I didn't tell anyone I quit, and I also didn't tell my wife. | I didn't tell anyone I quit | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 12 | `too` | I went for a walk in the morning, and I'll go in the evening too. | I'll go in the evening too | i ll go in the evening too | 1.0 | ✅ korundu |
| 01 | `also` | Last weekend was my brother's wedding, everyone was drinking and I just sat at the table; nobody noticed, but I also felt strange inside all night. | everyone was drinking / strange inside all night, | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 02 | `also` | I get up early and go to work in the mornings, and when I come home in the evening I also try not to go straight to bed, because the empty hours are hard. | the empty hours are hard. | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 03 | `also` | The doctor said to come for a check-up every three months, and he also said I shouldn't skip my medication, and I try to do both but I forget. | forget | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 04 | `also` | My wife doesn't talk to me in the evenings anymore, and the kids also shut themselves in their rooms; the house is silent when I walk in and that silence weighs on me. | weighs on | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 05 | `also` | After I was laid off I did nothing for three months, and my money also ran out; now I'm applying but nobody gets back to me. | applying | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 06 | `also` | My friends used to call every week, and I also stopped calling them; now nobody calls and part of that is my own fault. | part of that is my own fault | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 07 | `also` | I was very bad that day, and the next morning I also couldn't get out of bed, I didn't go to work for two days and I couldn't tell anyone why. | couldn't tell anyone why | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 08 | `also` | I didn't tell anyone I quit, and I also didn't tell my wife; I'm trying to hold it alone because if I say it and fail it will be worse. | if I say it and fail it will be worse, | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 09 | `also` | I started going for a walk in the morning, and in the evening I also take a short round; when I'm tired I think less at night. | a short round | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 10 | `also` | My mother asks the same thing every time she calls, and my brother also says the same thing; they both mean well but I feel like I'm giving an account of myself. | giving an account of myself, / mean well. | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 11 | `also` | I quit smoking, and I also cut down on coffee because the two triggered each other; now I don't know what to do in the mornings. | what to do in the mornings | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 12 | `also` | I can't sleep, and my appetite is also gone, I stare at the ceiling all night and when morning comes I get up feeling like I never rested. | at the ceiling / never rested | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |

### `tr_serbest`

| # | hedef | kullanıcı | alıntı | hizalanan kaynak | oran | hüküm |
|---|---|---|---|---|---:|---|
| 01 | `biraz` | Bugün biraz daha iyiyim. | Bugün biraz daha iyiyim | bugün biraz daha iyiyim | 1.0 | ✅ korundu |
| 02 | `aslında` | Aslında bırakmak istiyorum. | Bırakmak istiyorum | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 03 | `biraz` | Toplantıdan sonra biraz rahatladım. | biraz rahatladım | biraz rahatladim | 1.0 | ✅ korundu |
| 04 | `aslında` | Aslında kimseye kızgın değilim. | Kimseye kızgın değilim | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 05 | `biraz` | Akşamları biraz huzursuz oluyorum. | huzursuz | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 06 | `aslında` | Aslında bu ilk denemem değil. | İlk denemem değil | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 07 | `biraz` | Ailemle aram biraz düzeldi. | biraz düzeldi | biraz düzeldi | 1.0 | ✅ korundu |
| 08 | `aslında` | Aslında yalnız kalmaktan korkuyorum. | Yalnız kalmaktan korkuyorum | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 09 | `biraz` | Uyku düzenim biraz oturdu. | biraz oturdu | biraz oturdu | 1.0 | ✅ korundu |
| 10 | `aslında` | Aslında yardım istemeye utanıyorum. | Yardım istemeye utanıyorum | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 11 | `biraz` | İştahım biraz açıldı. | biraz açıldı | biraz açildi | 1.0 | ✅ korundu |
| 12 | `aslında` | Aslında o gün gitmek istememiştim. | O gün gitmek istememiştim | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 01 | `biraz` | Bu hafta üç kez yürüyüşe çıktım ve bugün kendimi biraz daha iyi hissediyorum, ama bunun ne kadar süreceğini bilmediğim için güvenmiyorum. | Bugün kendimi biraz daha iyi hissediyorum | bugün kendimi biraz daha iyi hissediyorum | 1.0 | ✅ korundu |
| 02 | `aslında` | Eşim bana kızdığında susuyorum çünkü aslında haklı olduğunu biliyorum ve tartışırsam kendimi savunmak zorunda kalacağım. | Kendimi savunmak zorunda kalacağım | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 03 | `biraz` | Toplantıdan sonra eve döndüm ve biraz rahatladım, orada oturup dinlemek bile beni yormuştu ama çıkarken içim hafiflemişti. | Çıkarken içim hafiflemişti | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 04 | `aslında` | Herkes bana kızgın olduğumu söylüyor ama aslında kimseye kızgın değilim, sadece çok yorgunum ve bunu anlatamıyorum. | Sadece çok yorgunum ve bunu anlatamıyorum | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 05 | `biraz` | Gün içinde iyiyim, akşamları biraz huzursuz oluyorum ve o saatlerde ne yapacağımı bilemediğim için telefona sarılıyorum. | O saatlerde ne yapacağımı bilemediğim için telefona sarılıyorum | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 06 | `aslında` | Kimseye söylemedim ama aslında bu ilk denemem değil, dört yıl önce bırakmıştım ve sekiz ay sonra geri döndüm. | Dört yıl önce bırakmıştım | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 07 | `biraz` | Kardeşim geçen ay taşındı ve ailemle aram biraz düzeldi, en azından artık telefonu açıyorum ve konuşabiliyoruz. | Artık telefonu açıyorum ve konuşabiliyoruz | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 08 | `aslında` | İnsanlar kalabalıkta rahat olduğumu sanıyor ama aslında yalnız kalmaktan korkuyorum ve bu yüzden gereksiz yere dışarıda kalıyorum. | Yalnız kalmaktan korkuyorum | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 09 | `biraz` | İlacı düzenli kullanmaya başladıktan sonra uyku düzenim biraz oturdu, artık gece ikide değil on birde yatabiliyorum. | Artık gece ikide değil on birde yatabiliyorum | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 10 | `aslında` | Danışmanla konuşmayı haftalardır erteliyorum çünkü aslında yardım istemeye utanıyorum, sanki bunu tek başıma beceremediğimi kabul etmiş olacağım. | Tek başıma beceremediğimi kabul etmiş olacağım | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 11 | `biraz` | İki haftadır düzenli yemek yiyorum ve iştahım biraz açıldı, eskiden öğle yemeğini tamamen atlıyor ve akşama kadar bir şey yemiyordum. | İki haftadır düzenli yemek yiyorum | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 12 | `aslında` | O gün gittim ama aslında gitmek istememiştim, eşim ısrar etti ve ben tartışmamak için arabaya bindim. | Tartışmamak için arabaya bindim | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |

### `en_serbest`

| # | hedef | kullanıcı | alıntı | hizalanan kaynak | oran | hüküm |
|---|---|---|---|---|---:|---|
| 01 | `a bit` | I'm a bit better today. | a bit better today | a bit better today | 1.0 | ✅ korundu |
| 02 | `actually` | Actually, I want to quit. | I want to quit | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 03 | `a bit` | I relaxed a bit after the meeting. | relax a bit after the meeting | a bit after the meeting | 0.909 | ✅ korundu |
| 04 | `actually` | Actually, I'm not angry at anyone. | not angry at anyone | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 05 | `a bit` | I get a bit restless in the evenings. | a bit restless in the evenings. | a bit restless in the evenings | 1.0 | ✅ korundu |
| 06 | `actually` | Actually, this isn't my first attempt. | this isn't my first attempt | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 07 | `a bit` | Things with my family got a bit better. | things with my family got a bit better. | things with my family got a bit better | 1.0 | ✅ korundu |
| 08 | `actually` | Actually, I'm afraid of being alone. | afraid of being alone | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 09 | `a bit` | My sleep schedule settled a bit. | my sleep schedule settled a bit. | my sleep schedule settled a bit | 1.0 | ✅ korundu |
| 10 | `actually` | Actually, I'm ashamed to ask for help. | ashamed to ask for help | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 11 | `a bit` | My appetite opened up a bit. | my appetite opened up a bit | my appetite opened up a bit | 1.0 | ✅ korundu |
| 12 | `actually` | Actually, I didn't want to go that day. | I didn't want to go that day | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 01 | `a bit` | I went for a walk three times this week and today I feel a bit better, but I don't trust it because I don't know how long it will last. | a bit better | a bit better | 1.0 | ✅ korundu |
| 02 | `actually` | When my wife gets angry at me I stay quiet because I actually know she's right, and if I argue I'll have to defend myself. | I actually know she's right | i actually know she s right | 1.0 | ✅ korundu |
| 03 | `a bit` | I came home after the meeting and relaxed a bit; even sitting there listening had worn me out, but I felt lighter on the way out. | even sitting there listening | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 04 | `actually` | Everyone tells me I'm angry but I'm actually not angry at anyone, I'm just very tired and I can't explain it. | I'm just very tired | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 05 | `a bit` | I'm fine during the day, in the evenings I get a bit restless, and at those hours I don't know what to do so I cling to my phone. | don't know what to do | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 06 | `actually` | I haven't told anyone, but this actually isn't my first attempt; I quit four years ago and came back eight months later. | this actually isn't my first attempt | this actually isn t my first attempt | 1.0 | ✅ korundu |
| 07 | `a bit` | My brother moved out last month and things with my family got a bit better; at least I answer the phone now and we can talk. | At least I answer the phone now | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 08 | `actually` | People think I'm comfortable in crowds but I'm actually afraid of being alone, and that's why I stay out longer than I need to. | I'm actually afraid of being alone | i m actually afraid of being alone | 1.0 | ✅ korundu |
| 09 | `a bit` | After I started taking the medication regularly my sleep schedule settled a bit; I can go to bed at eleven now instead of two. | instead of two | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 10 | `actually` | I keep putting off talking to the counsellor because I'm actually ashamed to ask for help, as if I'd be admitting I failed. | admitting I failed | — | — | ⚪ sayılmadı (hedefi içermeyen yer alıntılandı) |
| 11 | `a bit` | I've been eating regularly for two weeks and my appetite opened up a bit; I used to skip lunch completely. | opened up a bit | opened up a bit | 1.0 | ✅ korundu |
| 12 | `actually` | I went that day but I actually didn't want to go; my wife insisted and I got in the car to avoid an argument. | I actually didn't want to go | i actually didn t want to go | 1.0 | ✅ korundu |

---

## 5. ⛔ Sınırlar (ön kayıttan, değişmedi)

| | |
|---|---|
| ⛔ **`de/da` klitik, `too` serbest sözcük** | iki klitik hücresi yapıca eşit değil — sorunun kendisi bu |
| ⛔ **Ögeleri ben yazdım** (K30) | çeviri denkliği tek okuyucunun |
| ⛔ **Tek üretici ailesi** | Claude; agy kotası dolu, OPENAI_API_KEY yok |
| ⛔ **Blok üretimi** | 12 öge tek çağrıda ⇒ öge bağımsızlığı tam değil |
| ⛔ **Üretim yeniden koşulamaz** | K30; ham çıktı ve SHA saklandı, köken izlenir |
| ⚠️ **Hizalama eşiği 0.6** | bir SEÇİM; T168 de 0,53-0,60 aralığına şerh düşmüştü |
