# BıRAG veri kümesi — v0.0.20 ⚗️ **DENEY SÜRÜMÜ**

**Tarih:** 2026-09-22 · **Girdi:** `data/judged/v0.0.20.jsonl`
**Kayıt:** **1394** / 1468 (elenen 74)

⛔⛔ **KORPUSUN İLERLEYİŞİ DEĞİLDİR.** Ana hat `v0.0.18`. Bu, T255'nin
nedenselliğini sınamak için kurulmuş bir **deney kolu**dur ve
**%25,9'u alan dışıdır**.

---

## 1. v0.0.18'den farkı: 361 adımlı aritmetik tazeleme kaydı

| | v0.0.19 (ilk deneme) | **v0.0.20** |
|---|---:|---:|
| kayıt | 40 | **361** |
| cevap jetonu | 84 | **13.151** |
| ortalama cevap | 2,1 jeton | **36 jeton** |
| ⭐ **kayıp sinyalindeki pay** | %0,034 | **%5,01** |

⛔ **Neden bu fark önemli:** `mask_prompt: true` kaybı yalnız CEVAP
jetonlarına uyguluyor. `v0.0.19`'un 40 kaydı **kayıtların %3,7'siydi ama
gradyanın %0,034'ü** — deney bu yüzden hipotezi sınayamadı (T256).
⭐ Bu sürümde **pay koşudan ÖNCE ölçüldü** ve betik hedefi tutturana kadar
kayıt üretti.

**İki kip birden:** %78 **adımlı** (işlemi yazarak çözer — sinyal buradan) ·
%22 **yalın** (*«yalnızca sonucu yaz»* → yalın sayı — biçime uyum buradan).
İkincisi şart, çünkü eval'in bazı ögelerinde `uzunluk_maks` var.

| güvence | |
|---|---|
| ⭐ cevap doğrulaması | **361/361**, iki ayrı yoldan (üretimde + yazmadan önce) |
| ⭐ uydurma riski | **sıfır** — hiçbir olgu iddiası yazılmadı, cevaplar hesaplandı |
| ⭐ eval bulaşması | **0**, betikte denetleniyor |

---

## 2. ⭐⭐⭐ Sonuç: unutma tamamen geri alındı

| kol | sinyal payı | `forgetting_smoke` |
|---|---:|---|
| taban | — | **28/30** |
| `d1` (v0.0.18) | %0 | 26,75 ± 0,73 |
| `e1` (v0.0.19) | %0,034 | 26,67 ± 0,67 |
| ⭐ **`e2` (bu sürüm)** | **%5,01** | **28,00 ± 0,00** |

`e2` − `d1` = **+1,25 ± 0,73** ⇒ okunabilir. **Tabanla aynı** ve üç tohumun
üçü de aynı sayıyı verdi.

⭐⭐ **Terapötik eksen de düzeldi:** `safety_crisis` otomatik 8,75 → **12,33**
(+3,58 ± 2,28, okunabilir) ve **tabanı da aşıyor** (11). ⛔ Ama dereceli puan
hâlâ tabanın çok altında (8,33 ↔ 21) — T247 duruyor.

---

## 3. ⛔⛔ Ama etki KİPE ÖZGÜ DEĞİL

`fs-029` (*«Kürk Mantolu Madonna»nın yazarı*) **kontrol ögesiydi** — tazeleme
setinde tek bir olgu iddiası yok. Yine de 1/8 → **2/3** düzeldi: model artık
*«…**Enem Şişmanoğlu** değildir. …yazarı **Sabahattin Ali**'dir»* diyerek
kendini düzeltiyor.

➡️⭐⭐⭐ *Tazeleme öğrettiği kipi değil **genel bozulmayı** onarıyor.
⇒ T255'nin «korpusta o kip yok, o yüzden o kip bozuldu» açıklaması
**yetersiz**; ölçülen şey, dar dağılımlı bir ince ayarın genel yeteneği
bozması ve yeterince alan dışı sinyalin bunu geri alması.*

---

## 4. ⛔ Bu sürümün söylemedikleri

| | |
|---|---|
| ⛔⛔ **«Korpusa aritmetik ekleyelim» sonucu DEĞİLDİR** | ölçülen mekanizma; hangi içeriğin ekleneceği ayrı bir **ürün kararı** ve bu sürümün %25,9'u alan dışı |
| ⛔⛔ **LoRA kapsamı hipotezi ayrılmadı** | tazeleme genel onarım yaptığına göre sebep *«dar dağılım»* olabilir; kapsamdan ayıracak kol koşulmadı |
| ⛔ **Terapötik kalite değerlendirilmedi** | eklenen kayıtlar judge'a girmiyor; rubrik boyutları ölçülmedi |
| ⛔ **3 tohum** (`d1` 8 tohum) | asimetrik karşılaştırma |
| ⚠️ **Biçim uyumu tam değil** | model `fs-025`'e adımlı cevap veriyor (*«sadece son sayıyı yaz»* denmesine rağmen); `uzunluk_maks` sınırını aşmadığı için geçiyor ama uyum ölçülmedi |

📎 `scripts/analiz/2026-09-22-tazeleme-adimli.py` ·
`reports/analiz/2026-09-22-adimli-kol-sonuc.md`
