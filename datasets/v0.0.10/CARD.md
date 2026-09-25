# BıRAG veri kümesi — v0.0.10

**Tarih:** 2026-09-18 · **Girdi:** `data/judged/v0.0.10.jsonl` SHA256-16 `f761ad0811c5b333`
**Çıktı:** `train.jsonl` SHA256-16 `0e196e88815defea`
**Kayıt:** 571/577 (elenen **6**) — v0.0.9 ile **aynı sayıda**

---

## 1. v0.0.9'dan farkı: 8 kayıt, iki kural

⛔ **Yeni kayıt YOK.** Bu sürüm de bir büyüme değil, bir **düzeltme** — ve düzeltilen
şey iki ayrı kapının **göremediği** yerde birikmişti.

| kural | kayıt | ne yapıldı |
|---|---:|---|
| **T104 yapısal atıf** | **7** | iddia *«aynı CÜMLEDE»* diyordu, iki öge kullanıcının aynı mesajındaki **ayrı cümlelerinde**ydi ⇒ *«aynı mesajda»* |
| **T142 alıntı birebirliği** | 1 | kullanıcı *«her şeye karışıyorlar»* yazmış, cevap *«her şeye karışmak»* diye alıntılıyordu ⇒ kullanıcının kendi çekimi |

⭐ Biri **çift kusurluydu** (`v5-parti4 #23`): *«iki tane içtiğini»* kullanıcının sözü
değil, *«bir tane… sonra bir tane daha»*dan çıkarılmış bir **sayım**dı ⇒ artık
kullanıcının kendi sözü tırnak içinde.

⭐ **İlke: en az değişiklik.** Yedisinde yanlış olan iddianın İÇERİĞİ değil **DÜZEYİ**;
tek sözcük değişti, retorik nokta ve cümle yapısı korundu.

**Ölçülen etki:**

| | v0.0.9 | v0.0.10 |
|---|---:|---:|
| yapısal atıf — elle okunacak iddia | 27 | **20** |
| yapısal atıf — otomatik ihlal | 0 | 0 |
| alıntı birebirliği — işaretli öge | 22 | **21** |
| asistan cevabında *«aynı cümlede»* | 29 | 22 |
| asistan cevabında *«aynı mesajda»* | 13 | 20 |

---

## 2. ⭐⭐ Bu sekiz kusuru kapı bulmadı — elle okuma buldu

Yapısal atıf kapısı bir iddiayı ancak **≥2 alıntı** taşıyorsa otomatik sınayabiliyor.
`v0.0.9`'daki 42 iddianın 15'i o eşiğin üstündeydi ve orada ihlal **0**'dı. Kalan 27'si
*«elle okunacak»* yığınına düşüyordu ve o yığın **hiç okunmamıştı** (T140'ın açık
kalemi). Okununca **7'si yanlış** çıktı — **%26**.

➡️⭐⭐ *Bir kapının «0 ihlal» demesi, kapının **bakabildiği yerde** 0 ihlal olduğu
demektir. Kapının eşiği (≥2 alıntı) kusurun kendisiyle ilgisiz, yalnız kapının görme
koşuluyla ilgili — ve kusur eşiğin altında da aynı sıklıkta vardı.*

⛔ **Biri tam olarak daha önce iki kez düzeltilmiş kusur:** `v5-parti8 #20`'nin iddiası
bir alıntı taşıyor (*«net kazanmışım»*) ama **tek** alıntı taşıdığı için kapı
sınayamadı; aynı kusur `v5-parti8 #13` ve `#15`'te iki alıntılı olduğu için v0.0.9'da
yakalanmıştı.

---

## 3. ⛔⛔ Sekiz kaydın yargısı BAYAT — ve bu ilan ediliyor

Judge bu sekiz kaydı **yanlış iddia taşıyan** metin üzerinde puanladı; `grounding` ve
`alinti_dogrulama` gibi alanlar doğrudan o iddiaya bakıyor. Metin değişince yargı artık
o metni tarif etmiyor.

➡️ *Bir yargı, kuyruğa girdiği andaki metni tarif eder.* ⇒ Sekiz kaydın `judge` alanında
**`bayat: true`** ve gerekçe duruyor.

⚠️ Puanlar **düşürülmedi** (veri kaybolmasın) ama bu sekiz kaydın judge alanları
**hiçbir sayıda sessizce kullanılamaz**. Yeniden yargılama **yapılmadı** — ayrı bir iştir.

| kayıt | parti | metin SHA önce → sonra |
|---|---|---|
| `34ee4b88ca` | v4-parti2 #41 | `eff517aa161d1958` → `ebe2ce5cdadfdf73` |
| `fc06767f8f` | v4-parti2 #60 | `6032996790701541` → `8c77933c36fcdcdd` |
| `5bffdc87e0` | v5-parti3 #56 | `682865b1ab4a4ac1` → `57b9a143d219b496` |
| `e279f4f441` | v5-parti4 #23 | `19d56855456d868e` → `a934858e13731ac1` |
| `91b9b21155` | v5-parti6 #35 | `cd554d5642971332` → `f294ef07c445b530` |
| `53d8896213` | v5-parti6 #16 | `88f8a449e2af75e7` → `b33cf0512a656e0d` |
| `2df10702dd` | v5-parti8 #20 | `55b94245f2980e2e` → `fc4d6eedee8524af` |
| `935dfac08e` | v5-parti8 #27 | `791e656854c50b82` → `7570e678b40f2b89` |

⛔ Tam liste ve gerekçeler: `reports/analiz/2026-09-18-v010-revizyon.md`

---

## 4. Elenen 6 kayıt — değişmedi

v0.0.8'den beri aynı 6 kayıt eleniyor (`judge_safety_violation`). Bu sürüm onlara
dokunmadı; `manifest.json` gerekçeleriyle birlikte taşıyor.

---

## 5. Bu sürümde öğrenilenler (veriye girmeyen ama kararı belirleyen)

Sekiz düzeltme bir denetim turunun yan ürünü; asıl iş kapıların kendisindeydi ve
bulgular **veriye girmedi, karara girdi**:

| bulgu | nerede |
|---|---|
| ⛔⛔ §7b sert kapısı üretim sürümü ilerleyince **kendi kendine kapanmış** (4404 kayıt) | T149/T150 · düzeltildi, **0 kayıt düştü** |
| ⛔⛔ §15 taraması düz alt dizge arıyordu: *«merak etme»* ↔ *«merak etmek»* (16/16 yanlış pozitif) | T153 · düzeltildi |
| ⛔⛔ Sert kapı *«Senden bana söz vermeni istemiyorum»*i de düşürüyor — **kendi kuralını uygulayan cümleyi** | T153 · **DOKUNULMADI** (Kural 3, uzman kararı) |
| ⛔ *«keş»* *«keşke»*nin içinde eşleşiyordu — tuzak canlı | T154 · düzeltildi (önleyici) |
| ⛔ İnceleme kuyruğu **2026-09-12'den beri okunmamıştı**; okunca 16/16 yanlış pozitif | T152 · okuyucu yazıldı |

⚠️ Bu düzeltmelerin **hiçbiri** bu sürümün içeriğini değiştirmedi: hepsinde
`passed` değeri dönen kayıt **0**. Yani kapılar onarıldı, veri onarılmadı — bu
sürümdeki tek veri değişikliği yukarıdaki **8 kayıt**.

---

## ⛔ Bu kartın söylemedikleri

| | |
|---|---|
| ⛔ **20 iddia hâlâ elle okuma yığınında** | kapı onlara ulaşamıyor; bu sürümde bir kez okundular ama bir sonraki sürümde **yeniden okunmaları gerekecek** ve bunu hatırlatan bir mekanizma yok |
| ⛔ **Kapı güçlendirilmedi** | ≥2 alıntı eşiği duruyor; kusur eşiğin altında birikmeye devam edebilir |
| ⛔ **Yeniden yargılama yapılmadı** | sekiz kaydın judge alanı bayat işaretli; bu sürümün judge sayıları o sekizi dışarıda bırakmadan okunamaz |
| ⛔ **84 MI tuzağı ve 71 kayıtlık şablonlaşma sette DURUYOR** | ilk eğitim ölçülmeden düzeltilirse hangi revizyonun işe yaradığı ölçülemez |
| ⛔ **Şablonlaşmayı yakalayan kapı yok** | *«aynı cümlede»* asistan cevabında v0.0.2'de 1, v0.0.7'de 8, v0.0.8'de **31** — kuralın kendisi kalıbı doğuruyor (T139) |
| ⛔⛔ **«Temiz puan yeter mi» hâlâ cevaplanmadı** | ham model 15 kriz öğesinin yalnız 5'inde temiz yönlendiriyor; bütün Pareto kapısı bu cevaplanmamış sorunun üstünde duruyor ve cevabı **uzman kararıdır** |
| ⚠️ **Kararlar elle verildi** (K30) | ölçüt yazılı — *«aynı cümlede»* diyen iddia için kullanıcının TEK cümlesi iki ögeyi taşımalı — ama hüküm Claude'a ait |
