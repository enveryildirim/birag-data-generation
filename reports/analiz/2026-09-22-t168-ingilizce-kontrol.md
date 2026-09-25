# T168 İngilizce kontrol deneyi — SONUÇ (tur1)

**Betik:** `scripts/analiz/2026-09-22-t168-kontrol-olcum.py` · **Tarih:** 2026-09-22  
**Ön kayıt:** `configs/deney/2026-09-22-t168-ingilizce-kontrol.yaml` (**üretimden önce** commit `07ce8d8`)  
**Öge kümesi (1):** `data/deney/2026-09-22-t168-ogeler.jsonl` SHA256 `af09a27e2c42be05`  
**Ham üretim:** `ham/tr_klitik.jsonl` `38e698277913b72e` · `ham/en_klitik.jsonl` `52d2a519a2765618` · `ham/tr_serbest.jsonl` `66d888937c5dc6af` · `ham/en_serbest.jsonl` `460b512ac96efb29`  
**Üretici:** `claude-sonnet-subagent`, kör (ölçülen şey söylenmedi) · ⛔ yeniden koşulamaz (K30) — ham çıktılar saklandı

---

## 1. Sonuç tablosu

| Hücre | Öge | Sayılan | Düşen | Düşme oranı |
|---|---:|---:|---:|---:|
| `tr_klitik` | 12 | 11 | 1 | **%9** |
| `en_klitik` | 12 | 7 | 0 | **%0** |
| `tr_serbest` | 12 | 5 | 0 | **%0** |
| `en_serbest` | 12 | 6 | 0 | **%0** |

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
