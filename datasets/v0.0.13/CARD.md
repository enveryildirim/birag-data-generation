# BıRAG veri kümesi — v0.0.13

**Tarih:** 2026-09-18 · **Girdi:** `data/judged/v0.0.13.jsonl` SHA256-16 `be4ab717f6ba2291`
**Çıktı:** `train.jsonl` SHA256-16 `acde7d23c3b47ea7`
**Kayıt:** 571/577 (elenen **6**)

---

## 1. v0.0.12'den farkı: 3 zaman/kişi çıpası

| kayıt | eski | yeni |
|---|---|---|
| `afeb9133c0` | *«**hekimin** planlayacağı bir şey»* | *«**bir hekimin** planlayacağı bir şey»* |
| `44cd5dddff` | *«**dün gece** ekranı en son kapatabildiğin an»* | *«ekranı en son kapatabildiğin an»* |
| `047041e8b1` | *«**bir hafta önce** bilmediğin bir şeyi»* | *«**daha önce** bilmediğin bir şeyi»* |

⚠️ Üçü de **küçük** kusur ve üçü de aynı aileden: **cevabın, kullanıcının koymadığı bir
çıpayı koyması.** Kullanıcı hiçbir hekim anmamış · bir ALIŞKANLIK anlatmış, belirli bir
gece değil · yalnız *«bu hafta»*yı çıpalamış. ➡️ *Ayrı ayrı bakınca önemsiz görünürler;
birlikte bakınca korpusun kullanıcıya kendi anlatmadığı bir çerçeve giydirme eğilimi.*

---

## 2. ⭐⭐ Dört dayanak kapısının üçü artık SIFIR

| kapı | v0.0.10 | v0.0.11 | v0.0.12 | **v0.0.13** |
|---|---:|---:|---:|---:|
| alıntı birebirliği | 22 | 16 | **0** | **0** |
| zaman + kaynak atfı | 7 | 3 | 3 | **0** |
| yapısal atıf (otomatik) | 0 | 0 | 0 | **0** |
| mekân atfı | 11 | 11 | 11 | 11 *(9'u etiketli)* |
| kullanıcının sözcüğünü koruma | 6 ihlal | **0** | 0 | **0** |

⛔⛔ **Ama *«sıfır»* kapının BAKABİLDİĞİ yerde sıfır demektir.** Bu sürüm boyunca üç
anma çerçevesi, bir rol kısıtı ve iki yüklem dalı kapılara **elle okuma sonucu** eklendi —
yani her *«0»*, o güne kadar görülebilen kusurların sıfırı.

---

## 3. ⭐ Okuma defteri — elle okumanın kaydı tutuluyor

`v0.0.12/CARD.md` bir eksik ilan etmişti: *«yığın her sürümde yeniden okunmalı ve bunu
hatırlatan bir mekanizma yok»*. Mekanizma yazıldı
(`scripts/analiz/2026-09-18-okuma-defteri.py`):

| | |
|---|---:|
| yapısal atıf yığınındaki iddia | **20** |
| ⭐ hükmü taşınan (metin değişmemiş) | **20** |
| ⛔ yeni/değişmiş — okunmalı | **0** |

➡️⭐⭐ *Elle verilmiş bir hüküm, verildiği METNE bağlıdır. Metin değişmediyse hüküm de
geçerlidir — ama bunu söyleyen bir şey yoksa, hükmün hâlâ geçerli olduğunu kimse bilemez
ve okuma her sürümde sıfırdan tekrarlanır.*

---

## 4. Sürüm sağlığı (2026-09-18)

| | |
|---|---:|
| üretim kapısı (`run_checks`) | 571/571 geçti · 0 elendi |
| inceleme kuyruğu | yumuşak §15: 4 · klinik ad izi: 6 |
| mekân bulgusu | 11 (9 etiketli · **2 elle okunacak**) |
| şablonlaşma | *«bir şeye katılmıyorum»* %10,9 · *«bugüne kadar söylediklerin şunlar»* %7,5 |

---

## ⛔ Bu kartın söylemedikleri

| | |
|---|---|
| ⛔⛔ **32 kaydın yargısı BAYAT** | 8 + 6 + 16 + 3 (bazı kayıtlar birden çok kez düzeltildi) ⇒ bu sürümün judge sayıları onları dışarıda bırakmadan okunamaz; **yeniden yargılama yapılmadı** |
| ⛔⛔ **«0» kapının bakabildiği yerde 0** | anma çerçevesi listesi kapanmıyor; bu oturumda üç biçim daha **elle okumayla** bulundu |
| ⛔ **2 mekân bulgusu elle okunacak** | *«masadan çekilmek»* (deyim, sinyal görmüyor) ve *«Dönüşte masaya oturdun»* (çıkarım) |
| ⛔ **Şablonlaşma sette DURUYOR** | kapı ölçüyor, **eleme yapmıyor**; 84 MI tuzağı da duruyor (ilk eğitim ölçülmeden düzeltilirse hangi revizyonun işe yaradığı ölçülemez) |
| ⛔⛔ **İki klinik karar bekliyor** | *«temiz 5 yeter mi»* ve `gd-018` uzman kalemi — ikisi de Kural 3 gereği **uzman + etik kurul** |
| ⛔ **Süre dalı açık** | §7b yüklem deseninde *«iki ay sürüyor»* kaçıyor; kapatmak bağlam pasajı ↔ serbest metin ayrımı gerektiriyor ve o ayrım kodda yok |
| ⚠️ **Kararlar elle** (K30) | üç düzeltmenin her biri kullanıcının kendi cümlesi okunarak verildi |
