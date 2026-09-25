# ⛔⛔ Bulaşma ölçümü — eğitim bankası ↔ `context_fidelity` eval'i

**Betik:** `scripts/analiz/2026-09-22-celiskili-eval-bulasma.py` · **Tarih:** 2026-09-22  
**Banka:** 25 çift · **eval `celiskili` ögesi:** 5  
**Bulgu:** 5/5 eval ögesinin bankada konu ortaklığı olan bir çifti var  

⛔⛔⛔ **Neden önemli.** `celiskili` sınıfı tam da bu 5 ögede kazanç versin diye tasarlandı. Eğer aynı konu — hatta aynı **değerler** — iki tarafta da varsa, ölçülecek kazanç **öğrenme değil ezber** olabilir. Bu ölçüm ince ayardan **önce** yapıldı ve ön kayda yazıldı.

## Öge başına en yakın eğitim çiftleri

| eval | sonda | bankadaki en yakın çift(ler) | ortak kök |
|---|---|---|---|
| `cf-016` | İki parça farklı saat veriyor — model çelişk | #18 kapanış saati | `acikti`, `vermek` |
| `cf-017` | Bir parça izin veriyor, diğeri şart koşuyor | #2 başvuru için randevu | `oncede`, `randev` |
| `cf-018` | Çelişki ÜÇ parçanın ikisinde — üçüncüsü alak | #6 ücret | `katili`, `ucrets` |
| `cf-019` | Künyesiz çelişki — iki pasaj birbirini doğru | #16 kayıtların saklanması | `kayitl`, `saklan`, `sureyl` |
| `cf-020` | Çelişki ÖRTÜK — iki cümle doğrudan karşıt de | #4 kimlik belgesi | `basvur`, `belge`, `belges`, `kimlik`, `sirasi` |

## ⛔⛔ Değer düzeyinde çakışma (en ağır biçim)

| eval | banka | çakışan değer |
|---|---:|---|
| `cf-017` | #2 | «randevu gerekir» |
| `cf-017` | #2 | «randevusuz» |
| `cf-018` | #6 | «ücretsiz» |
| `cf-020` | #4 | «belge gerekmez» |

⛔⛔⛔ **4 çakışma.** Bir eğitim çiftinin **değeri** eval ögesinin pasajlarında birebir geçiyor ⇒ o öge için ölçülecek kazanç **ezberden ayırt edilemez**.

## ⭐ Ön kayda yazılacak hüküm

⛔ `context_fidelity`'nin **`celiskili` alt puanı** (5/5 ögede konu ortaklığı, 4 değer çakışması) **temiz bir sınama değildir** ve baş sonuç olarak raporlanamaz.

⭐ **Temiz kalan ölçüler:** `context_fidelity`'nin öteki üç kategorisi (`yeterli`, `distractor`, `yetersiz` — 15 öge), `context_fidelity.real` (15 gerçek öge), `safety_crisis`, `forgetting_smoke`, `sycophancy`. Baş sonuç **bunlardan** okunacak.

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔ **Kök eşleme kaba** | 6 harflik ön ek, elle yazılmış durak listesi ⇒ hem yanlış pozitif hem yanlış negatif verir; sayı bir **işarettir**, kesin bir örtüşme ölçüsü değil |
| ⛔ **Anlamsal bulaşma ölçülmedi** | farklı sözcüklerle aynı yapıyı öğretmek de bulaşmadır ve bu tarama onu görmez |
| ⛔ **Bulaşma GİDERİLMEDİ** | bu betik yalnız ölçer; eğitim kayıtları olduğu gibi duruyor ve karar ayrı bir iştir |
| ⚠️ **Eval ögelerini de bu proje yazdı** | bağımsız bir sınama kümesi değil; bulaşma zaten yapısal olarak olası |
