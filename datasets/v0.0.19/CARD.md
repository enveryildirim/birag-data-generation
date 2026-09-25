# BıRAG veri kümesi — v0.0.19 ⚗️ **DENEY SÜRÜMÜ**

**Tarih:** 2026-09-22 · **Girdi:** `data/judged/v0.0.19.jsonl`
**Kayıt:** **1073** / 1147 (elenen 74)

⛔⛔ **BU SÜRÜM KORPUSUN İLERLEYİŞİ DEĞİLDİR.** Tek bir hipotezi sınamak için
kurulmuş bir **deney kolu**dur. Korpusun ana hattı `v0.0.18`'dir.

---

## 1. v0.0.18'den farkı: 40 aritmetik tazeleme kaydı

`v0.0.18` (1033) + **40 `replay` kaydı** = 1073.

Eklenen kayıtlar çok adımlı aritmetik soru ve **yalın sayı cevabı**
taşıyor — korpusta **%0,0** oranında bulunan bir çıktı kipi.

| | |
|---|---|
| dilim | `replay` (§9 — genel amaçlı, judge'a girmez) |
| üretim | `scripts/analiz/2026-09-22-tazeleme-seti.py`, tohum 20260922 |
| ⭐ **doğrulama** | cevaplar Python'da hesaplandı ve betik **40/40'ını doğruladı** ⇒ sıfır uydurma riski, hiçbir olgu iddiası yazılmadı |
| ⭐ **bulaşma** | `forgetting_smoke`'un 30 ögesiyle çakışma **0**, betikte denetleniyor |

---

## 2. ⛔⛔ Ne sınıyor — öngörüler koşudan ÖNCE yazıldı

**T255** ölçmüştü: ince ayar aritmetik (`fs-025` 0/8, `fs-013` 4/8) ve
olgusal ad (`fs-029` 1/8) ögelerini kaybediyor; korpusta bu kiplerin hiçbiri
yok. Ama nedensellik kurulmamıştı — aynı kaybı **LoRA kapsamı** da
üretebilirdi (K174/K175).

⭐⭐⭐ **Ayırıcı tasarım: yalnız ARİTMETİK tazelenir, OLGUSAL AD TAZELENMEZ.**

| sonuç | anlamı |
|---|---|
| aritmetik düzelir, olgusal düzelmez | ⭐ **kip yokluğu sebep** — tazeleme kipe özgü |
| ikisi de düzelir | tazeleme genel onarım yapıyor; kip açıklaması yetersiz |
| ikisi de düzelmez | ⛔ sebep korpus değil **LoRA kapsamı** |

⚠️ **Bulaşma şerhi, önceden yazılı:** tazeleme seti eval'in aritmetik
ögeleriyle **aynı kipi** hedefliyor (çok adımlı işlem → yalın sayı) ama
hiçbir ögeyi tekrarlamıyor. ⇒ Kazanç okunurken *«kip tazelemesi işe yaradı»*
denir, *«genel yetenek geri geldi»* **DENMEZ**.

---

## 3. Bileşim

`v0.0.18`'in bütün özellikleri geçerli (judge karışımı, uydurma kapısı,
türetilmiş `slice` ve `date`) — tek fark 40 `replay` kaydı. `replay` dilimi
18 → **58**.

⛔ Eleme `v0.0.18` ile aynı: 56 uydurma · 14 klinik güvenlik · 4 karantina.
Tazeleme kayıtlarının **40/40'ı** bugünkü `run_checks`'ten geçti.

---

## 4. ⛔ Bu sürümle ilgili uyarılar

| | |
|---|---|
| ⛔⛔ **Ana hat değildir** | korpusun ilerleyişi `v0.0.18`; bu kol bir hipotez sınaması |
| ⛔ **Terapötik kalite için değerlendirilmedi** | eklenen kayıtlar alan dışı ve judge'a girmiyor |
| ⚠️ **Eğer hipotez tutarsa bile** | *«korpusa aritmetik ekleyelim»* sonucu **çıkmaz**; çıkan sonuç, unutmanın sebebinin ölçülmüş olmasıdır. Ürün kararı ayrıdır |

📎 `scripts/analiz/2026-09-22-tazeleme-seti.py` ·
`reports/analiz/2026-09-22-unutma-gerilemesi.md` (T255)
