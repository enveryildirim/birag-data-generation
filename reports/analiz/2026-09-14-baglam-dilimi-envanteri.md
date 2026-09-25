# Bağlam (RAG) dilimi envanteri — parti 2 öncesi

**Girdi:** `data/candidates/expert-70.jsonl` · SHA256 `ee61043de8d38187cc41b7a6c5391b735bfcc8daf9e12af504317ef0041aa775`  
**Betik:** `scripts/analiz/2026-09-14-baglam-dilimi-envanteri.py` · **Tarih:** 2026-09-14

---

## 1. Durum

- Bağlamlı kayıt: **9/70** (`uretim-v2`) · v3 parti 1'de **0/40**
- Repoda belge korpusu: **yok**. `data/` yalnızca `seeds.jsonl` (tohum senaryoları), `candidates/`, `judged/`, `plan/` tutuyor. Tohumlarda `user_message` ve senaryo meta'sı var, **alınabilir pasaj yok**.
- Sonuç: v2'deki **9 pasajın 9'i de** ve kaynak adlarının tamamı üretim sırasında **yazıldı**.

> ⚠️ Kaynak adları gerçek kurum belgesi gibi duruyor (*"Fabrika Çalışan El Kitabı — Mola Düzeni"*, *"Üniversite Psikolojik Danışma Birimi — SSS"*). Hiçbiri var olan bir belge değil. Kural 3 açısından kayda geçmesi gereken şey budur.

## 2. Risk ne kadar büyük — pasaj içeriği cevaba geçiyor mu?

Asıl soru uydurmanın **yayılıp yayılmadığı**: model pasajdaki iddiayı kendi cevabında tekrarlıyorsa uydurma içerik çıktıya taşınır.

| # | kaynak (uydurma) | pasajdan cevaba geçen içerik sözcüğü |
|---|---|---|
| 1 | Gençler için Dijital İyi Oluş Rehberi | — yok |
| 2 | Çevrimiçi Oyun Platformları Kullanıcı Rehberi | araçları, belirleme |
| 3 | Dijital İyi Oluş Rehberi | — yok |
| 4 | Üniversite Psikolojik Danışma Birimi — SSS | — yok |
| 5 | Gebelik Öncesi Danışmanlık Bilgi Notu | — yok |
| 6 | Tütün Bırakma Destek Notları | — yok |
| 7 | Fabrika Çalışan El Kitabı — Mola Düzeni | — yok |
| 8 | İşyeri Ruh Sağlığı Bilgi Notu | — yok |
| 9 | Aile İçi İletişim Notu | — yok |

**8/9 kayıtta pasajdan cevaba HİÇBİR içerik sözcüğü geçmiyor.** Geçen tek kayıt `yetersiz` vakası: model pasajın neyden bahsettiğini **reddini gerekçelendirmek için** adlandırıyor (*"orada sınır belirleme araçlarından bahsediliyor, oranların uzun vadeli getirisinden değil"*) — istenen davranış bu.

**Okuma:** öğretilen şey pasajın **içeriği** değil, pasaj karşısındaki **davranış** (ne zaman kullan, ne zaman "bu bağlamda yok" de). Uydurma içerik çıktıya taşınmıyor. Yine de girdi tarafında var ve veri kartında yazılmalı.

## 2b. ⚠️ Asıl bulgu: v2'nin RAG dilimi bağlamı KULLANMAYI hiç öğretmiyor

Pasajın uydurma olması ikincil bir sorun çıktı. Birincil sorun şu: bağlamlı dokuz kaydın hiçbirinde model **bağlamdaki cevabı kullanıp kullanıcının sorusunu cevaplamıyor**.

| Davranış | Adet | Ne öğretiyor |
|---|---:|---|
| bağlamı görmezden geliyor (kullanıcı zaten soru sormamış) | 6/9 | "bağlam gelirse aldırma" |
| bağlam yetersiz, açıkça reddediyor | 2/9 | ✅ doğru davranış (§7 `yetersiz`) |
| bağlamda cevap **var**, model yine de vermiyor | 1/9 | ⛔ uzmanın **reddettiği** kayıt: *"cevap verilmesi gerekiyor, bu cevabı vermemiş"* |
| **bağlamdaki cevabı kullanıyor** | **0/9** | — |

Son satırdaki kayıt (`ambivalans`, üniversite danışma birimi) v3 §5b'nin yazılma sebebiydi: kullanıcı *"kayıt aileme gider mi"* diye sordu, pasajda gizlilik cümlesi duruyordu, model *"paylaşmamı ister misin?"* dedi. §5b o kuralı düzeltti ama **parti 1'de hiç bağlam kaydı olmadığı için kural hiç sınanmadı**.

**Parti 2'nin RAG dilimi buna göre kurulur:** çoğunluk, kullanıcının doğrudan sorduğu ve cevabı pasajda duran vakadır.

## 3. Kullanılan format varyantları (K17)

K17 tek format istemiyor, 4-5 varyant dolaşsın diyor. v2'de fiilen:

- `köşeli etiket` — [BAĞLAM]…
- `tire ayraç` — --- KAYNAK: Çevrimiçi Oyun Platformları Kullan…
- `tire başlık` — BAĞLAM — Dijital İyi Oluş Rehberi…
- `köşeli etiket` — [BAĞLAM]…
- `iki satır` — BAĞLAM…
- `XML etiketi` — <baglam kaynak="Tütün Bırakma Destek Notları">…
- `markdown başlık` — ### BAĞLAM…
- `parantezli` — BAĞLAM (kaynak: İşyeri Ruh Sağlığı Bilgi Notu)…
- `köşeli + nokta` — [BAĞLAM · Aile İçi İletişim Notu]…

**8 ayrı varyant** — K17'nin istediği çeşitlilik sağlanmış.

## 4. Parti 2 için karar gereken nokta

Bağlam dilimi pasaj metni olmadan yazılamaz. Üç yol var ve **hangisi seçilirse iş değişir**:

1. **Gerçek korpus** — İP3'ün alma korpusu komşu depolarda olabilir. AGENTS Kural 1 gereği okumadan önce **izin gerekir**.
2. **Sentetik pasaj, açık kayıtla** — v2'nin yolu; ama kaynak adları gerçek kurum belgesi taklidi olmaktan çıkarılır, pasajlar klinik iddia taşımaz (yalnızca yordam/sınır cümleleri), her kayıt `sentetik: true` ile işaretlenir.
3. **Yalnızca `yetersiz` vakası** — doğru davranışın *"bu bağlamda cevap yok"* olduğu kayıtlar. En az uydurma gerektirir ama yalnızca reddi öğretir.

