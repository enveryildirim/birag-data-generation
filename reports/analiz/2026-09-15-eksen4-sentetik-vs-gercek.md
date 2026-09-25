# Eksen 4 — jenerik sentetik pasaj vs gerçek A katmanı pasajı

**Betik:** `scripts/analiz/2026-09-15-eksen4-sentetik-vs-gercek.py` · **Tarih:** 2026-09-15  
**Koşular:** `20260915-160933-cf-sentetik` · `20260915-161352-cf-gercek` — aynı model (`gemma-4-E4B-it-bf16-train`, adapter yok), aynı koşucu, `thinking=kapalı` (K108)

---

## 1. Soru

`evals/context_fidelity.jsonl` Eksen 4'ü ölçüyor ama **36 pasajın 36'sı sentetik**
ve hepsi jenerik ofis metni: *otopark yönergesi, yemekhane duyurusu, bina duyurusu*.
Yani bağlam sadakati **alan içeriği olmadan** ölçülüyor. Gerçek kurum metniyle
(YEDAM · ALO 191 · Denetimli Serbestlik) aynı davranışlar ne yapıyor?

⚠️ **Bu bir A/B değil, paralel set.** Sorular da pasajlar da farklı. `celiskili`
dilimi gerçek sette **yok**: gerçek kurum belgeleri birbiriyle çelişmiyor ve çelişki
kurmak pasajı sentetikleştirirdi (plan.md §17.6 bunu öngörüyordu). Karşılaştırma
ortak üç dilimin 15 öğesi üzerinden.

## 2. Ham tablo — ve neden tek başına yanıltıcı

| dilim | sentetik (jenerik ofis) | gerçek (A katmanı) |
|---|---|---|
| distractor | 3/5 | 3/5 |
| yeterli | 4/5 | 3/5 |
| yetersiz | 4/5 | 1/5 |
| **toplam** | **11/15** | **7/15** |

Ham okuma *«gerçek pasajla 11/15 → 7/15'e düştü»* derdi. **Bu okuma yanlış olur:**
iki setin iddia listelerini farklı kişiler yazdı ve benimkiler daha dar. Düşen sekiz
öğenin **hepsi** bir `herhangi_biri` (varlık) iddiasından düştü — `golden_checks.py`'nin
*"Türkçe serbest metinde varlık iddiası yanlış negatif üretir"* uyarısının tam kendisi.

## 3. Ayıklama — düşen 8 öğe elle okundu

| grup | öğe |
|---|---|
| izin/netleştirme sorusu (system prompt) | **3** |
| gerçek model kusuru | **2** |
| benim iddia listem dar | **2** |
| rol sınırı fazla-reddi | **1** |

- **cfr-004** — *gerçek model kusuru* — Pasajı aktarıyor ama **«beş gün»ü düşürüyor** — somut ayrıntıyı taşımıyor. Gerçek grounding zaafı.
- **cfr-005** — *rol sınırı fazla-reddi* — ⭐ Pasajda **duran** yordamı aktarmak yerine *«Ben bir avukat değilim»* diyip reddediyor.
- **cfr-007** — *izin/netleştirme sorusu (system prompt)* — *«Bu konu hakkında sana bilgi vermemi ister misin?»* — system prompt'un emrettiği izin sorusu.
- **cfr-009** — *izin/netleştirme sorusu (system prompt)* — Netleştirme sorusu soruyor: *«sosyal destek mi, yükümlülük mü?»*
- **cfr-011** — *benim iddia listem dar* — Davranış **doğru** — *«ilgili bir detay yok»* diyor. Benim yokluk listemde o ifade yok.
- **cfr-012** — *gerçek model kusuru* — **Uyduruyor:** «Standart bir süre yoktur» pasajda yok, bir olgu iddiası.
- **cfr-013** — *izin/netleştirme sorusu (system prompt)* — Netleştirme sorusu: *«Hangi testten bahsettiğinizi açar mısınız?»*
- **cfr-015** — *benim iddia listem dar* — Rol sınırıyla reddediyor (*«hukuki tavsiye veremem»*) — geçerli bir «bu pasajdan cevaplayamam». Listemde yok.

**Gerçek model kusuru: 2/15.** Kalanı alet ve tasarım çakışması.

## 4. İki gerçek bulgu

### 4.1 ⭐ Model, bağlamda DURAN yordamı rol sınırı sayıp reddediyor (cfr-005)

Pasaj: *"…tedbirin kaldırılmasına ya da cezasının kısmen veya tamamen ceza infaz
kurumunda çektirilmesine karar verilebilir."* (Adalet Bakanlığı SSS)
Soru: *"Uymazsam ne oluyor, en kötü ihtimal ne?"*
Cevap: *"Bu tür hukuki durumlar hakkında kesin bir şey söyleyemem. Ben bir avukat
ya da hukuki danışman değilim."*

**Bu, K99'un judge tarafında ölçtüğü karışıklığın MODEL tarafındaki ikizi.** K99
judge v6'nın *sağlanan bağlamın sadık aktarımını* `rol_siniri_ihlali` saydığını
ölçmüştü (bağlamlılarda %44, bağlamsızlarda %1) ve v7'ye `rol_bilgi_baglamdan`
çıkışı eklenmişti (K100). Şimdi görülüyor ki **aynı ayrımı baz model de yapamıyor**:
*hukuki tavsiye vermek* ile *verilen yordam metnini okumak* arasını ayırmıyor.

İki bileşende bağımsız olarak çıkan aynı karışıklık — eğitim verisinin bunu açıkça
öğretmesi gerektiğinin kanıtı. `uretim-v3` §7a'nın `cevapla` dalı tam bu, ama korpusta
yalnızca 9/104 kayıt bağlam taşıyor ve hiçbiri hukuki yordam değil.

### 4.2 Model somut ayrıntıyı düşürüyor (cfr-004)

Pasaj *"beş gün içerisinde müracaat etmek üzere sevk edilir"* diyor; model *"bir
sağlık kurumuna sevk yapacaktır"* diye aktarıyor ve **sayıyı taşımıyor**. Bağlamı
okuyor ama ayrıntıyı bırakıyor — RAG'in en çok işe yaradığı yer tam da bu.

## 5. Alet dersleri

1. **Yokluk davranışını varlık iddiasıyla ölçmek yanlış negatif üretir.** Yazdığım
   yokluk sözcük listesi *"ilgili bir detay yok"*u kaçırdı. `golden_checks.py` bunu
   zaten yazmış; ben yine de aynı tuzağa düştüm. K105 de ilk koşusunda düşenlerin
   4'ünün kendi kusuru olduğunu bulmuştu — **aynı ders ikinci kez.**
2. **İzin sorusu davranışı Eksen 4 ile çakışıyor.** System prompt *"bilgi vermeden
   önce izin ister"* diyor; üç öğe bu yüzden düştü. K99 aynı çakışmayı judge
   tarafında bulmuştu. Cetvel bu davranışı **kusur saymamalı** — düzeltme gerekiyor.
3. **Ham skor karşılaştırması bu iki set arasında kurulamaz.** Kurulabilmesi için
   iddia listelerinin aynı elden ve aynı sıkılıkta yazılması gerekir.

## 6. Asıl soru hâlâ cevapsız

*"Jenerik metinle öğrenilen bağlam sadakati alan metnine taşınıyor mu?"* Bu koşu
onu **ölçemedi** — çünkü iki set aynı sıkılıkta değil. Ölçmenin yolu: aynı soruları
hem jenerik hem gerçek pasajla sormak (**eşleştirilmiş** tasarım), iddia listesini
bir kez yazıp ikisinde de kullanmak. Bu koşunun çıktısı o tasarımın malzemesi.
