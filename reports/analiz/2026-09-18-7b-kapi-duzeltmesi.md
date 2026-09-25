# §7b düzeltmesi — iki parça, üç sınama

**Betik:** `scripts/analiz/2026-09-18-7b-kapi-duzeltmesi.py` · **Tarih:** 2026-09-18

T149: *«düzeltmenin tek parçası zarar verir»*. İki parça birlikte yazıldı:

| parça | ne değişti |
|---|---|
| **(a)** | `startswith("uretim-v3")` → `uretim_surumu(record) >= 3` (sürüm bir SAYIDIR; önek karşılaştırmak sayı karşılaştırmak değildir) |
| **(b)** | `KLINIK_IDDIA` ikiye ayrıldı: `KLINIK_YUKLEM` kapıyı kapatır, `KLINIK_AD` **inceleme kuyruğuna** gider (`rol_siniri` emsali) |

⚠️ **Olumsuzluk bir muafiyet olarak YAZILMADI.** *«Bu ilaç bağımlılık YAPMAZ»*
olumsuzdur ama klinik iddiadır. T142'nin dersi baştan uygulandı: ayrım
olumsuzlukta değil, **ad/yüklem** ayrımında.

## 1. ⭐ Birleşik desen korundu mu?

Dört analiz betiği `KLINIK_IDDIA`'yı içe aktarıyor; sayıları değişmemeli (K97).
`HEAD` deseni ile yeni birleşim **28083** metin parçasında karşılaştırıldı.

⭐ **Eşleşmeler birebir aynı** (28083/28083) ⇒ içe aktaran betiklerin sayıları değişmez.

## 2. ⭐ Regresyon — yakalanması gereken yakalanıyor mu?

⚠️ Vakalar **elle** yazıldı; korpustan alınsalardı sınama kendi kurulum
kümesinde koşmuş olurdu.

| beklenti | vaka | `KLINIK_YUKLEM` | sonuç |
|---|---|---|---|
| ⛔ yakalanmalı (etki iddiası) | Bu program bağımlılığı iyileştirir. | ✅ ateşledi | ✅ |
| ⛔ yakalanmalı (⭐ OLUMSUZ ama iddia) | Bu ilaç bağımlılık yapmaz. | ✅ ateşledi | ✅ |
| ⛔ yakalanmalı (süre iddiası) | Yoksunluk belirtileri üç gün içinde geçer. | ✅ ateşledi | ✅ |
| ⛔ yakalanmalı (⭐ OLUMSUZ ama iddia) | Bu yöntem zararlı değildir. | ✅ ateşledi | ✅ |
| ⛔ yakalanmalı (etkililik iddiası) | Grup terapisi bireysel görüşmeden daha etkilidir. | ✅ ateşledi | ✅ |
| ⭐ geçmeli (feragat) | Araç bir tarama aracıdır ve tanı koymaz. | ✅ sessiz | ✅ · ad izi: ['tanI'] |
| ⭐ geçmeli (uygunluk) | Programa katılmak için konulmuş bir tanı aranmaz; başvuru kişinin kend | ✅ sessiz | ✅ · ad izi: ['tanI'] |
| ⭐ geçmeli (birim adı) | Gündüz tedavi ünitelerinde geceleme yapılmaz; ünite kapanış saatinde k | ✅ sessiz | ✅ · ad izi: ['tedavI'] |
| ⭐ geçmeli (yordam) | Nöbetçi eczaneler gece boyunca açıktır. Reçeteli ilaçlar için reçete a | ✅ sessiz | ✅ · ad izi: ['Ilaçlar'] |
| ⭐ geçmeli (yordam) | Gebelik planlayan kişilerde ilaçların gözden geçirilmesi reçete eden h | ✅ sessiz | ✅ · ad izi: ['IlaçlarIn'] |
| ⭐ geçmeli (gizlilik) | Yanıtlar oturum kapandığında cihazda saklanmaz ve üçüncü kişilerle pay | ✅ sessiz | ✅ |
| ⭐ geçmeli (⭐ süre AD'ı, fiil değil) | Ödünç alınan materyal iki hafta süreyle kullanılabilir. | ✅ sessiz | ✅ |
| ⭐ geçmeli (⭐ kullanıcının geçen zamanı) | Altı ay geçti düğünden, hâlâ kullanıyorum. | ✅ sessiz | ✅ |
| ⭐ geçmeli (sınır) | Görüşmeler arasında verilen bir ödev yükümlülüğü yoktur. | ✅ sessiz | ✅ |

⭐ **14 vakanın hepsi beklendiği gibi.**

### ⛔⛔ Bilinen boşluk — bu düzeltmenin KAPATMADIĞI

Yüklem desenleri çekimsiz biçimlere bağlı. ⚠️ Boşluk `HEAD`'de de var ⇒ bu
düzeltmenin ürünü değil; bilerek karıştırılmadı, çünkü desen genişletmek bir
**sert kapıyı** genişletmektir ve kendi yanlış pozitif ölçümünü gerektirir.

| boşluk | vaka | şimdi |
|---|---|---|
| ⭐ KAPANDI: «riskini azaltır» | Bırakmak kalp riskini azaltır. | ⭐ artık yakalanıyor |
| ⭐ KAPANDI: «etki ediyor» | Bu madde uykuya etki ediyor. | ⭐ artık yakalanıyor |
| ⛔ AÇIK: «ay sürüyor» — serbest metinde 49 YP | Yoksunluk iki ay sürüyor. | ⛔ kaçıyor |
| ⛔ AÇIK: «haftada geçer» — serbest metinde 49 YP | Belirtiler üç haftada geçer. | ⛔ kaçıyor |

➡️ **2/4** hâlâ kaçıyor ve bu **ilan edilmiş** bir boşluktur — *«yakalanmadı»* ile *«yok»* karıştırılmasın.

## 3. ⛔ Bedel — hangi kayıtların kararı döndü?

`HEAD` `run_checks` ile yeni hâli **6213** kayıtta karşılaştırıldı.

| | |
|---|---|
| kararı DÖNEN kayıt | **0 tekil** (0 satır, sürüm kopyaları dahil) |
| ⭐ klinik AD izi raporlanan (inceleme kuyruğu) | **7 tekil kayıt** |

⭐⭐ **Hiçbir kaydın kararı dönmedi.** ⇒ (a) kapıyı 4404 kayıtta açtı ve
(b) o kapının bilinen yanlış pozitif sınıfını kapattı; ikisi birlikte
veri setine **dokunmadan** kapıyı çalışır hâle getirdi.

➡️⭐⭐ *T149'un öngörüsü ölçümle doğrulandı: tek parça 6 doğru kaydı
düşürecekti, iki parça birlikte 0 kayıt düşürüyor.*

## ⛔ Bu düzeltmenin söylemedikleri

| | |
|---|---|
| ⛔ **Kapı artık ADLARA bakmıyor** | *«tedavi», «tanı», «ilaç»* geçen bir pasaj kapıyı kapatmaz; yalnız raporlanır. Gerçek bir iddia AD ile kurulmuşsa (*«Bu tanı kesindir»*) kapı görmez ⇒ ad izleri kuyruğu **okunmalı** |
| ⛔ **İnceleme kuyruğunu okuyan yok** | `context_klinik_ad_izi` alanı yazılıyor ama onu tüketen bir betik henüz yazılmadı — `rol_siniri`'nin durumunun aynısı |
| ⛔ **Sürümsüz kayıtlar hâlâ kapsam dışı** | `dikey-dilim-v1` ve `prompt_version` taşımayan 224 kayıt için §7b yine kapalı; bu bir TASARIM kararıydı ve bu düzeltme onu değiştirmiyor |
| ⚠️ **«0 kayıt düştü» korpusa bağlıdır** | kapı kapalıyken üretilen bir korpusta üretici §7b'den geri bildirim almadı; sayı bugünün verisi için geçerli |
| ⚠️ Regresyon vakaları elle yazıldı (K30) | kapının genelleme gücü değil, ilan edilen iki sınıfta tutarlılığı sınandı |
| ⛔⛔ **Yüklem desenleri çekime kapalı** | *«riskini azaltır»*, *«iki ay sürüyor»*, *«etki ediyor»* kaçıyor. `HEAD`'de de kaçıyordu ⇒ bu düzeltmenin ürünü değil, ama artık **ölçülü ve ilan edilmiş** bir boşluk |
