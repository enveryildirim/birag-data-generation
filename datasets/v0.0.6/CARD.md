# BıRAG veri kümesi — v0.0.6

**Tarih:** 2026-09-16 · **git** `eb621fe`
**Girdi:** `data/judged/v0.0.6.jsonl` SHA256 `587f2ad5ad7aa95b`
**Kayıt:** 214/215 (elenen **1**)

---

## 1. v0.0.5'ten farkı

| | v0.0.5 | **v0.0.6** |
|---|---:|---:|
| kayıt | 155 | **214** |
| yeni kayıt | — | **59** (`v4-parti2`) |
| kelime | 25.593 | **57079** |

`v4-parti2` bu kümedeki ilk **tasarım ızgarasıyla** üretilmiş partidir: 60 satırlık
grid deterministik bir betikle çekildi, altı korpus ekseninin altısı da hedefi
**+0.0 puan** sapmayla tuttu (`reports/analiz/2026-09-16-v4-parti2-korpus-hedef.md`).

**Dilim dağılımı:** {'terapotik_tek_tur': 111, 'terapotik_cok_tur': 66, 'rag_tek_tur': 15, 'rag_cok_tur': 4, 'replay': 18}

---

## 2. ⛔ Bu sürümde İKİ RUBRİK karışık

| judge rubriği | kayıt |
|---|---:|
| `judge-eksen1.v7` | 137 |
| **`judge-eksen1.v9`** | 59 |
| yok (replay dilimi) | 18 |

⛔ **İlk kez tek bir sette iki rubrik var.** Sebep: 155 kayıt v7 ile puanlanmıştı,
yeni parti v9 ile puanlandı (v9 geçerli sürüm ve asimetrik doğrulaması ihlali
*arttırma* yönünde çalışıyor — Kural 3 açısından güvenli yön).

⚠️ **Karışımın pratik etkisi dar:** `build.py`nin judge kapısı **tek alan**
(`klinik_guvenlik_ihlali`); öteki puanlar rapor, kapı değil. Ama **puanlar
rubrik sürümüne göre havuzlanamaz** (K137: rubrik sürümü sıralamayı çeviriyor)
⇒ bu kümeden judge puanı bildirilecekse **sürüme göre ayrılmalı**.

⛔ Tekdüzelik istenirse 155 kaydın v9 ile **yeniden** puanlanması gerekir; ayrı
ve büyük bir karar (155 iş), **yapılmadı**.

---

## 3. Elenen kayıt

**1 kayıt** — `judge_safety_violation`, tohum `kimyasal_madde:st_002:0513`.

Kullanıcı müşteri yemeğinde, üç dört kadeh içmiş, *"biraz dağıldım, masaya dönmem
lazım"* diyor; cevap içkiye hiç değinmiyor (`guvenlik_tipi: riski_atlama`).

⭐ **Bu bir tasarım çarpışması:** kaydın `turn_ending` beyanı `yalnizca_yansitma`,
yani §5a gereği **soru yasak** — güvenlik yoklaması ise bir sorudur. Talimat
hangisinin öncelikli olduğunu yazmıyor (T98, açık kalem).

⚠️ **Yön şerhi (T68):** güvenlik judge'ları tek yönlü tedbirli sapma gösteriyor ve
bizim asimetrimiz sapmayı **aynı yöne ekliyor** ⇒ bu eleme bir **üst sınırdır**;
judge'ın yanlış pozitif oranı uzmana karşı **hiç ölçülmedi**.

---

## 4. ⭐ Yeni partide düzeltilen kusurlar

Judge, beş deterministik denetimin göremediği **uydurulmuş ayrıntılar** buldu; üçü
düzeltildi ve kaynak dosya **üzerine yazılmadı**, `v4-parti2.v2.jsonl` olarak
versiyonlandı.

| kayıt | kusur | nerede |
|---|---|---|
| #25 | *"Bugün ilk kez farklı kokmuş"* — kullanıcı koku hakkında bir şey demedi | cevap |
| #25 | *"Otoparkta yanında kimse yoktu"* — konuşmada yok (ilk düzeltme sonrası çıktı) | cevap + thinking |
| #38 | *"Geçen hafta da yazmıştın"* — hiçbir turda yok | cevap |
| #18 | *"Rezil"* — kullanıcı o sözcüğü söylemedi | **thinking** |
| #34 | *"Bunu bir yere yazmak istedim" demişti* — söylememişti | **thinking** |

⛔⛔ **Ortak mekanizma: KIRPMA.** Beşinin de kaynağı tohum metniydi; kullanıcı
mesajı §3a'nın `bicim` bandına kırpılınca dayanak silindi, cevap ve thinking ona
atıf yapmayı sürdürdü. ➡️ *Bant yalnızca kullanıcı mesajına uygulanıyor; hiçbir
şey "cevap kalan metnin üstünde hâlâ duruyor mu" diye sormuyordu.*

⭐ **Düzeltme bağımsız alanla doğrulandı:** `grounding == 2` olan kayıtlar
düzeltmeden önce tam olarak #25 ve #38 idi; sonra **hiçbiri**.

⛔ **thinking eğitiliyor ama denetlenmiyordu.** Eğitim hedefi
`thinking + completion` (`mask_prompt: true`), judge ise thinking'i **kapsam dışı**
tutuyor (K120 §3, bilerek). Bu boşluk için yeni bir kapı yazıldı:
`scripts/analiz/2026-09-16-thinking-alinti-denetimi.py` — thinking'deki tırnaklı
alıntılar konuşmada aranır. Bu partide **hayalet 0** (22 karşıolgusal + 9 parafraz,
elle okundu). ⚠️ Vekil: **tırnaksız** uydurma iddiaları görmez.

---

## 5. Şerhler

- ⛔ **Kalite ölçülmedi.** Bu kart üretim ve kapı sonuçlarını bildirir; kümenin
  eğitimdeki değeri **ölçülmedi** (ölçüm Faz 5 eğrisinin işi).
- ⛔ `dogallik` ve `mi_uyumu` puanları **kanıt değil** (K61).
- ⛔ Judge **Claude** (K43/K45: puanlayan judge ilkece Claude olamaz; Gemini kotası
  tükendi — K96) ⇒ eleştirmen işlevinde okunmalı.
- ⛔ **k=1**; kayıt düzeyinde tek karar gürültü tabanının altında (K103).
- ⛔ **Kriz dilimi yok** (etik kurul) · **vahşi doğa dilimi yok**.
- ⚠️ `motivation` alanı 19 kayıtta tohumdan **düzleştirilmiş** (T95); ham değer
  `gen_meta.motivasyon_tohum`'da duruyor.
- ⚠️ parti1'in thinking alıntıları **elle okunmadı** (23 öge sınıflanmamış) — borç.
