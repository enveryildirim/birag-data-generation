# BıRAG veri kümesi — v0.0.12

**Tarih:** 2026-09-18 · **Girdi:** `data/judged/v0.0.12.jsonl` SHA256-16 `d55171dffb82edb9`
**Çıktı:** `train.jsonl` SHA256-16 `d22d99bf7d8019c9`
**Kayıt:** 571/577 (elenen **6**) — v0.0.11 ile **aynı sayıda**

---

## 1. v0.0.11'den farkı: 16 alıntı birebir hâline getirildi

⛔ **Yeni kayıt YOK.** Bu sürüm de bir düzeltme.

| kural | kayıt | ne yapıldı |
|---|---:|---|
| **alıntı birebirliği** (T168) | **16** | model alıntılarken Türkçenin *«de/da»* edatını ve hedge öbeklerini düşürüyordu ⇒ kullanıcının birebir sözü |

| kullanıcının yazdığı | modelin alıntıladığı | düzeltildi |
|---|---|---|
| *«içim **de** bir tuhaf»* | *«İçim bir tuhaf»* | ✅ |
| *«ben de **aslında buna** katılıyorum»* | *«ben de katılıyorum»* | ✅ |
| *«Hak ettim **bunu** galiba»* | *«Hak ettim galiba»* | ✅ |
| *«gerçeği söylemek **de** mümkün değil»* | *«Gerçeği söylemek mümkün değil»* | ✅ |
| *«niye **ben** hep yalnızım»* | *«niye hep yalnızım»* | ✅ |

➡️⭐⭐⭐ *Bu bir «yanlış alıntı» değil, bir **üslup**: alıntı kısaltılırken cümlenin
**vurgusunu** taşıyan öge atılıyordu. «içim **de** bir tuhaf» ile «içim bir tuhaf» aynı şeyi
söylemez — «de» başka bir şeyin daha olduğunu ima eder ve alıntıdan silinince kullanıcının
söylediğinden **başka bir cümle** tırnak içine alınmış olur.*

**Ölçüt önceden ilan edildi ve tutturuldu:**

| | v0.0.11 | v0.0.12 |
|---|---:|---:|
| alıntı birebirliği kapısı | **16** öge / 13 kayıt | **0** / **0** |

⭐ Her düzeltme betiğin kendisinde sınandı: yeni alıntı kullanıcının metninde **birebir**
bulunmalı **ve** `run_checks` geçmeli. On altısı da geçti.

---

## 2. İki düzeltme farklı sınıftan

| kayıt | neden farklı |
|---|---|
| *«icra dosyasına bir nefes olur, kimsenin haberi olmaz»* | kullanıcı *«…olur, **eşim duymaz**, kimsenin…»* yazmış ⇒ alıntı ortadaki **yan cümleyi atıp iki ucu bitiştiriyordu** (T104'ün özgün kırpma kusuru). Alıntı **kısaltıldı**, bitişik kısımla sınırlandı |
| *«Babam da idare etti»* | bir alıntı değil **sentez**di; kullanıcı *«babamda da olurdu böyle şeyler, hiç doktora gitmedi, idare etti»* yazmış ⇒ kendi ardışık sözü tırnağa alındı |

## 3. ⚠️ Üç düzeltmede noktalama dışarı taşındı

Kullanıcı o cümleyi noktayla bitirmemiş (*«…onlar bilmiyor, o kötü geliyor»*) ⇒ nokta
tırnağın içinde kalırsa alıntı birebir olmaz.

➡️⭐⭐ *Birebirlik noktalamayı da kapsar: bir nokta eklemek cümleyi **bitirmek** demektir ve
kullanıcı onu bitirmemiş olabilir.*

---

## 4. Kapıya eklenen üç muafiyet (aynı okumada bulundu)

21 bulgunun **5'i yanlış pozitifti** ve üç yeni **anma çerçevesi** kapıya eklendi:

| çerçeve | örnek |
|---|---|
| olumsuz yeterlilik | *«ben "olur" **diyemem**»* |
| ulaç | *«"iyi olur" **diyerek** … almayacağım»* |
| karşılaştırma | *«"Bir şey olmadı" **ile** "olmaz" **aynı şey değil**»* |

⚠️ Birincisinde Türkçe ses değişimi tökezletti: `de-` kökü `-y` önünde **`di-`** oluyor
(*demek → diyemem*) ve `\bde` yazan ilk desen hiç ateşlemedi. Regresyon **12/12**.

---

## 5. Sürüm sağlığı (2026-09-18)

| kapı | otomatik ihlal | elle okunacak |
|---|---:|---:|
| üretim kapısı (`run_checks`) | 571/571 geçti, 0 elendi | — |
| **alıntı birebirliği** | **0** | — |
| zaman + kaynak atfı | 3 öge | — |
| yapısal atıf | **0** | ⚠️ **20** |
| mekân atfı | 11 | — |
| kullanıcının sözcüğünü koruma | 69/69 korunmuş | — |
| inceleme kuyruğu | yumuşak §15: 4 · klinik ad izi: 6 | — |

---

## ⛔ Bu kartın söylemedikleri

| | |
|---|---|
| ⛔⛔ **29 kaydın yargısı BAYAT** | v0.0.10'dan 8 + v0.0.11'den 6 + bu sürümden 16 (bir kayıt iki kez düzeltildi) ⇒ bu sürümün judge sayıları onları dışarıda bırakmadan okunamaz; **yeniden yargılama yapılmadı** |
| ⛔⛔ **Anma çerçevesi listesi kapanmıyor** | bugün üç biçim daha eklendi ve her biri ancak **elle okumayla** görüldü ⇒ kapı bu sınıfta hep bir adım geride; *«0 ihlal»* bugün kapının bakabildiği yerde 0 demektir |
| ⛔ **20 iddia hâlâ elle okuma yığınında** | yapısal atıf kapısı onlara ulaşamıyor (≥2 alıntı eşiği); T155 bu yığında **%26** kusur bulmuştu |
| ⛔ **Mekân kapısının 11 bulgusu mecaz** | *«masada iki şey var»*, *«o odada olmayacağım»*; kapının `MECAZ` muafiyeti yalnız iki kalıbı tutuyor ve düzeltilmedi |
| ⛔⛔ **«Temiz 5 yeter mi» cevapsız** · **`gd-018` uzman kalemi açık** | ikisi de klinik karar, Kural 3 gereği uzman + etik kurul |
| ⛔ **Şablonlaşma sette DURUYOR** | *«bir şeye katılmıyorum»* %10,9 · *«bugüne kadar söylediklerin şunlar»* %7,5; kapı ölçüyor, **eleme yapmıyor** |
| ⚠️ **Kararlar elle** (K30) | on altı düzeltmenin her biri kullanıcının kendi cümlesi okunarak verildi; hüküm Claude'a ait |
