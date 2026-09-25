# BıRAG veri kümesi — v0.0.11

**Tarih:** 2026-09-18 · **Girdi:** `data/judged/v0.0.11.jsonl` SHA256-16 `eb8170396c096bcc`
**Çıktı:** `train.jsonl` SHA256-16 `70f566b1c583249d`
**Kayıt:** 571/577 (elenen **6**) — v0.0.10 ile **aynı sayıda**

---

## 1. v0.0.10'dan farkı: 6 kayıt, tek bir kural

⛔ **Yeni kayıt YOK.** Bu sürüm de bir düzeltme: **kullanıcının kendi sözcüğü geri konuldu.**

| kural | kayıt | ne yapıldı |
|---|---:|---|
| **kullanıcının sözcüğünü koru** (T166) | **6** | kullanıcı *«Hanım»* / *«Karım»* demiş, cevap *«Eşin»* diyordu ⇒ kullanıcının kendi sözcüğü |

⭐ Yön **tek taraflı**ydı: günlük konuşma dilindeki sözcük resmî olanla değiştiriliyordu,
tersi hiç yok. ➡️ *Korpusun kendi kaydı, kullanıcının kaydını bastırıyordu.* Depo baştan
beri *«kullanıcının KENDİ sözcüğünü kullan»* diyor (T142) — bu altı kayıt o kuralın kendi
ihlaliydi.

**Ölçülen etki:**

| | v0.0.10 | v0.0.11 |
|---|---:|---:|
| eş/hanım/karı geçen kayıt (payda) | 69 | 69 |
| ⭐ kullanıcının sözcüğü korunmuş | 63 | **69** |
| ⛔ cevap başka sözcük kullanmış | **6** | **0** |
| zaman + kaynak atfı kapısı | 7 öge | **3** öge |

⭐ Zaman kapısının 7 bulgusundan **4'ü kendiliğinden düştü**: o bulgular zaten bu
sözcük değişimiydi — asistan kullanıcının anmadığı bir kişi adı kullanıyordu.

---

## 2. ⛔⛔ Bu sayıya üç denemede ulaşıldı — ilk ikisi artefakttı

Bu sürümün asıl dersi düzeltmede değil, **ölçmede**:

| deneme | ölçüm | sonuç |
|---|---|---|
| 1 | ekler ELLE sayıldı | **4 ihlal** — *«karının»* listede yoktu; düzeltme o biçimi ürettiği için kayıt **paydadan düştü** ve *«0»* kısmen artefakt oldu |
| 2 | `AD_CEKIM_EKI` + `tr_fold` | **3 ihlal** — daha kötü: `tr_fold` *«ı»*yı *«i»*ye eşliyor, deseni katlayınca *«karı»* → *«kari»* oluyor ve **gövde, ekin ihtiyaç duyduğu ünlüyü yutuyor**; ayrıca liste ünlüyle biten gövdeler için yazılmamış (*«karı»* + *«m»* yok) |
| 3 | açık BİÇİM listesi, ham metin | ⭐ **6 ihlal** — payda iki sürümde de **69**'da sabit |

➡️⭐⭐⭐ *Bir eşleştirmeyi katlamak, metni katlamakla aynı şey değildir: katlama gövde-sonu
ünlüsünü siliyorsa, ek listesi artık o gövdeye uymaz. Ve bir ölçütün **paydası** ölçtüğü
düzeltmeden etkileniyorsa, sayı okunamaz — bu, Eksen 1'de judge kapsamının yaptığının
aynısıdır (T162).*

⚠️ Ölçüm bir yanlış pozitif de üretmişti: bir kayıtta *«eşin»* sözcüğü **kullanıcının
değil, BAĞLAM belgesinin**di (*«Görüşmeye eşin katılması istenirse»*); kullanıcı *«Karım»*,
cevap *«karın»* demiş, yani **doğru**. ⇒ Ölçüm artık bağlam bloklarını ayıklıyor.
*Bir kullanıcının «kendi sözcüğü», ona GÖSTERİLEN belgenin sözcüğü değildir.*

---

## 3. ⛔⛔ Altı kaydın yargısı BAYAT

Judge bu kayıtları düzeltmeden **önceki** metin üzerinde puanladı ⇒ `judge.bayat: true` ve
gerekçe yazıldı. Puanlar düşürülmedi ama bu altı kaydın judge alanları **hiçbir sayıda
sessizce kullanılamaz**. Yeniden yargılama **yapılmadı**.

⚠️ Bayat işaretli toplam kayıt **14** (v0.0.10'dan devralınan 8 + bu sürümün 6'sı).

---

## 4. Sürüm sağlığı (2026-09-18)

| kapı | otomatik ihlal | elle okunacak |
|---|---:|---:|
| üretim kapısı (`run_checks`) | 571/571 geçti, 0 elendi | — |
| alıntı birebirliği | 21 öge / 16 kayıt | — |
| zaman + kaynak atfı | **3** öge | — |
| yapısal atıf | **0** | ⚠️ **20** |
| mekân atfı | 11 | — |
| inceleme kuyruğu | yumuşak §15: 4 · klinik ad izi: 6 | — |

⚠️ Mekân kapısının 11 bulgusunun çoğu **mecaz** (*«masada iki şey var»*, *«o odada
olmayacağım»*) — kapının `MECAZ` muafiyeti yalnız iki kalıbı tutuyor ve düzeltilmedi.

---

## ⛔ Bu kartın söylemedikleri

| | |
|---|---|
| ⛔⛔ **20 iddia hâlâ elle okuma yığınında** | kapı onlara ulaşamıyor (≥2 alıntı eşiği); T155 bu yığında **%26** kusur bulmuştu ve yığın her sürümde **yeniden** okunmalı |
| ⛔⛔ **«Temiz 5 yeter mi» cevapsız** | bütün Pareto kapısı bu cevaplanmamış **uzman kararının** üstünde duruyor |
| ⛔⛔ **`gd-018` uzman kalemi açık** | §8 özerklik kalıbı riskli kullanımı normalleştiren bir savuşturmaya dönüştü (T162); karar klinik ve Kural 3 gereği uzman + etik kurul onayına bağlı |
| ⛔ **Yeniden yargılama yapılmadı** | 14 kaydın judge alanı bayat; bu sürümün judge sayıları onları dışarıda bırakmadan okunamaz |
| ⛔ **84 MI tuzağı ve şablonlaşma sette DURUYOR** | *«bir şeye katılmıyorum»* %10,9 · *«bugüne kadar söylediklerin şunlar»* %7,5; şablon kapısı ölçüyor ama **eleme yapmıyor** |
| ⛔ **Sözcük listesi elle** (K30) | yalnız eş/hanım/karı ölçüldü; *«oğlum»* ↔ *«çocuğun»* gibi çiftler taranmadı · *«karın»* Türkçede *«mide»* de demek ve bu korpusta çakışmadığı ÖLÇÜLDÜ, ama desen güvencesi değil |
| ⚠️ **Kararlar elle** (K30) | altı düzeltmenin her biri kullanıcının kendi cümlesi okunarak verildi; hüküm Claude'a ait |
