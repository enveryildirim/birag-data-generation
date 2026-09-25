# BıRAG veri kümesi — v0.0.14

**Tarih:** 2026-09-18 · **Girdi:** `data/judged/v0.0.14.jsonl`
**Çıktı:** `train.jsonl` SHA256-16 `34b7dce826c2d1e1`
**Kayıt:** 571/577 (elenen **6** — v0.0.13 ile **aynı küme**)

---

## 1. v0.0.13'ten farkı: metin DEĞİŞMEDİ, yargı yenilendi

⛔ **Hiçbir kaydın metni değişmedi.** Bu sürümde yalnız **32 bayat yargı** yeniden koşuldu.

| | |
|---|---:|
| bayat kayıt | 32 |
| ⭐ yeniden yargılanan | **32** |
| ⛔ başarısız | **0** |
| puanı değişen | 23 |
| ⭐ **güvenlik bayrağı değişen** | **0** |
| elenen kayıt kümesi | **aynı** |

⭐ Judge `filter.judge_record` ile çağrıldı ⇒ kuyruk birebir aynı (K103), puanlayan
**Claude değil** (K43/K45): `agy:gemini-3.8-flash-high`, rubrik `judge-eksen1.v9`.

---

## 2. ⛔⛔⛔ Ve bu koşu bir ÖLÇÜM ARACI kusuru ortaya çıkardı

32 kaydın **23'ünün** puanı değişti. Ama o kayıtlardaki metin değişikliği birer
**sözcüktü** (*«eşin»* → *«hanımın»*, alıntıya *«de»* geri konması). *«bir»* eklemek
`duygusal_tepki`'yi 1'den 0'a indiremez ⇒ değişimin kaynağı düzeltme olamaz.

⭐ **Ayrıldı:** metni **hiç değişmemiş**, v9 ile yargılanmış **12** kayıt aynı judge'a
yeniden soruldu ⇒ **6'sı (%50) farklı puan aldı.**

➡️⭐⭐⭐ *Aynı metne aynı judge iki kez sorulduğunda **yarısında** başka puan geliyor.
Bir kaydın puanı bir **ölçüm** değil, bir **çekiliş**tir; kayıt düzeyinde
karşılaştırma yapılamaz.*

⛔⛔ **Ve gürültü simetrik değil:**

| boyut | düştü | yükseldi | okuma |
|---|---:|---:|---|
| `yorumlama` | **11** | 2 | ⛔ sistematik düşüş |
| `kesif` | **7** | 1 | ⛔ sistematik düşüş |
| `duygusal_tepki` | 5 | 8 | · simetrik gürültü |

⚠️ Eski yargılar 09-17'de, yenileri 09-18'de alındı ⇒ düşüş **judge tarafındaki bir
kaymadan** da gelebilir. İki açıklama (gürültü ↔ kayma) bu veriyle **ayrılamadı**.

⭐ **Ne değişmedi:** `build.py`'nin eleme kararı `klinik_guvenlik_ihlali`ye bakıyor ve
o bayrak **hiçbir kayıtta** oynamadı ⇒ metodolojik bulgu ağır ama **veri değişmedi**.

---

## 3. Sürüm sağlığı (2026-09-18)

| kapı | durum |
|---|---|
| üretim kapısı (`run_checks`) | 571/571 geçti · 0 elendi |
| alıntı birebirliği · zaman+kaynak · yapısal atıf (otomatik) | **0 · 0 · 0** |
| mekân atfı | 11 (9 etiketli · 2 okunmuş, deftere geçti) |
| kullanıcının sözcüğünü koruma | 69/69 korunmuş |
| okuma defteri | ⭐ **okunacak yeni bulgu 0** |

---

## ⛔ Bu kartın söylemedikleri

| | |
|---|---|
| ⛔⛔⛔ **Judge kayıt düzeyinde %50 kararsız** | bu sürümün judge alanları artık *taze* ama **tek çekiliş**; kayıt düzeyinde karşılaştırma yapılamaz. ⚠️ ORTALAMALAR bu gürültüden çok daha az etkilenir ⇒ Eksen 1'in bileşik puanı (T162) bu bulguyla otomatik çürümez |
| ⛔⛔ **Hangi puanın «doğru» olduğu bilinmiyor** | ölçülen şey TUTARLILIK, doğruluk değil; iki çekiliş de yanlış olabilir |
| ⛔ **Gürültü ↔ kayma ayrılamadı** | ayırmak için aynı metne **aynı gün** iki kez sormak gerekir; yapılmadı |
| ⛔ **«0 ihlal» kapının bakabildiği yerde 0** | bu oturumda üç anma çerçevesi, bir rol kısıtı, iki yüklem dalı kapılara **elle okumayla** eklendi |
| ⛔ **Şablonlaşma ve 84 MI tuzağı sette DURUYOR** | ilk eğitim ölçülmeden düzeltilirse hangi revizyonun işe yaradığı ölçülemez |
| ⛔⛔ **İki klinik karar bekliyor** | *«temiz 5 yeter mi»* ve `gd-018` — **uzman + etik kurul** (Kural 3) |
| ⚠️ n=12 küçük | %50 geniş bir güven aralığı taşır |
