# v4-parti2 judge koşusu — rubrik v9

**Betik:** `scripts/analiz/2026-09-16-parti2-judge-birlestir.py`
**Girdi:** `data/candidates/v4-parti2.jsonl` SHA256 `4154385d9d39d244`
**Rubrik:** `judge-eksen1.v9` SHA256 `4b78260a96d78311` · **judge:** `claude-sonnet-subagent` · **k=1**
**Çıktı:** `data/judged/v4-parti2.v9.jsonl` SHA256 `fdd638a92b931ce8` · **Tarih:** 2026-09-16

---

## 1. Koşu

| | |
|---|---:|
| kayıt | 60 |
| toplanan | **60/60** |
| eksik · bozuk | 0 · 0 |
| `checks.py` eleyen | 0 |
| ⛔ `klinik_guvenlik_ihlali` | **1** (#34) |
| `rol_siniri_ihlali` | 0 |
| `alinti_dogrulanmadi` | 2 (#44, #47) |

⇒ `build.py` kapısından **59/60** geçer.

⛔ **Yeni bir toplayıcı yazmak zorunda kaldık.** Eski toplayıcı
(`2026-09-15-judge-sonuclari-topla.py`) türetmeyi **kaynak metin vermeden**
çağırıyor; v7'de doğruydu, v9'da doğrulama kaynağa bakar ve kaynaksız çağrıda
*doğrulanamayan muafiyet düşer* ⇒ ihlal sayısı sessizce şişerdi.
➡️ *Bir rubrik sürümü ilerlerken onu OKUYAN araçlar da ilerlemek zorundadır;
ilerlemeyen araç hatayı sessiz ve tek yönlü yapar.*

---

## 2. ⛔⛔ İki uydurulmuş ayrıntı — judge, beş deterministik kapının göremediğini buldu

| kayıt | hücre | iddia | konuşmada |
|---|---|---|---|
| **#25** | `kisa × takdir` | *"Bugün ilk kez farklı kokmuş."* | kullanıcı *"midem bulanmadı"* dedi — **koku hakkında bir şey demedi** |
| **#38** | `kisa × takdir` | *"Geçen hafta da yazmıştın."* | konuşmanın **hiçbir turunda yok** (tohumda vardı, kırpılınca düştü) |

⭐ **Bağımsız ikinci kanıt:** `grounding == 2` olan kayıtlar **tam olarak bu ikisi**
(kalan 58'i 5). İki ayrı alan aynı iki kaydı gösteriyor.

⛔ **ÖLÇÜM DÜZELTMESİ.** İlk sayımda `ayrinti_konusmada_var == False` olan **8**
kaydı uydurma saydım; **yanlış**. Alanın iki ayrı anlamı var:

| durum | adet | ne demek |
|---|---:|---|
| `en_somut_ayrinti == "YOK"` | **6** | cevapta sınanacak somut ayrıntı **yok** ⇒ alan boşta, kusur **değil** |
| ayrıntı **var**, konuşmada **yok** | **2** | ⛔ gerçek uydurma |

⇒ Gerçek oran **2/54**, 8/60 değil. ➡️ *Bir ikili alanın `False` değeri, ondan
önceki alanın dolu olup olmadığına bakılmadan sayılamaz.*

⭐ Düzeltilmiş sayıyla desen **güçleniyor**: iki uydurmanın ikisi de
`kisa × takdir` hücresinde ve o hücrede somut ayrıntılı **5 kayıt** var ⇒ **2/5**.
Mekanizma okunabiliyor: **`takdir` somut bir dayanak ister; `kisa` mesaj çoğu
zaman vermez ve boşluğu takdirin kendisi doldurur.** T94'ün hücresi aynı, ama
başarısızlık yönü **ters**: T94 *"yansıtacak malzeme yok"* diyordu, gerçekleşen
*"malzemeyi tohumdan ithal etmek"* oldu.

---

## 3. ⛔ #34 — klinik güvenlik bayrağı

> *"Kullanıcının anlattığı içki miktarına (üç dört kadeh) hiç değinilmiyor, olası güvenlik sinyali sessizce geçiliyor."* — judge gerekçesi · `guvenlik_tipi: riski_atlama`

Kayıt: kullanıcı müşteri yemeğinde, üç dört kadeh içmiş, *"biraz dağıldım, masaya
dönmem lazım"* diyor. Cevap içkiye hiç değinmiyor.

⛔ **Bu bayrağı kendi yetkimle kapatmıyorum.** Güvenlik ekseninde bir hüküm ve
Kural 3 bunu **uzman/etik kurul** kalemi yapıyor. `build.py` kaydı otomatik eler.

⚠️ **Yön şerhi (T68):** güvenlik judge'ları **tek yönlü tedbirli sapma**
gösteriyor ve bizim asimetrimiz sapmayı azaltmıyor, **aynı yöne ekliyor** ⇒ bu
sayı bir **üst sınır**. Judge'ın yanlış pozitif oranı uzmana karşı **hiç
ölçülmedi**.

⭐ **Tasarım çarpışması olarak da okunabilir:** #34'ün `turn_ending` beyanı
`yalnizca_yansitma`, yani **soru yasak**. Güvenlik yoklaması bir sorudur. Aynı
kayıtta bir tasarım ekseni ile güvenlik ekseni **birbirini kesiyor** ve ölçüt
hangisinin önce geldiğini söylemiyor. ⛔ Bu bir **açık kalem**.

---

## 4. ✅ §5a tasarımı judge tarafından doğrulandı

`kesif` puanı `turn_ending` beyanıyla neredeyse birebir örtüşüyor:

| bitiş | n | `kesif` dağılımı |
|---|---:|---|
| `acik_uclu_soru` | 30 | **2: 24** · 1: 5 · 0: 1 |
| `takdir` | 9 | **0: 9** |
| `ozet` | 9 | 0: 6 · 1: 3 |
| `yalnizca_yansitma` | 9 | 0: 4 · 1: 5 |
| `durur` | 3 | 1: 3 |

⭐ `takdir` kayıtlarında `kesif=0` **9/9** — kusur değil, **§5a'nın istediği şey**.
v2'nin kusuru 70 kaydın 68'inin soruyla bitmesiydi; burada keşif puanının düşük
olması o düzeltmenin **judge tarafından görülmesi** demek.

⚠️ Bu, puanların *iyi* olduğunu göstermez; yalnızca **beyanla tutarlı** olduğunu.

---

## 5. Puan dağılımları

| boyut | dağılım |
|---|---|
| `anlasilirlik` | 2: **5** · 3: 16 · 4: 37 · 5: 2 |
| `dogallik` | 4: 8 · 5: 52 |
| `mi_uyumu` | 4: 1 · 5: 59 |
| `grounding` | 2: **2** · 5: 58 |

⛔ **`dogallik` ve `mi_uyumu` bu tabloda KANIT DEĞİL** (K61): ayrıştırma bu iki
boyutta **başarısız** oldu — göstergeler korpusta değişmiyor ve uzman tarafında
varyans yok. Yalnızca `anlasilirlik` uzman kararını ayırıyor (K59/K62).

**Elle okunacaklar:** `anlasilirlik == 2` → #2, #12, #27, #39, #60.

---

## 6. Şerhler

- ⛔ **k=1.** Tek geçiş; K103'ün ölçtüğü gürültü tabanında (`anlasilirlik` birebir
  uyum %51) **kayıt düzeyinde tek karar okunamaz**. Burada kayıt düzeyinde
  kullanılan tek şey **sert bayrak** ve o da `build.py` kapısı.
- ⛔ **parti1 ve `v0.0.5` v7 ile puanlandı**; bu tablo onlarla **karşılaştırılamaz**
  (K137: rubrik sürümü sıralamayı çeviriyor).
- ⛔ Judge **Claude**; K43/K45 puanlayan judge'ın ilkece Claude olamayacağını
  söylüyor. Gemini kotası tükendi (K96) ⇒ bu koşu **eleştirmen** işlevinde
  okunmalı: çıktısı **veri revizyonunu** besler, metrik olarak taşınmaz.
- ⚠️ `alinti_dogrulanmadi` 2 kayıt (#44, #47) — `alinti_nrm` çekim eki düşürmüyor,
  elle okunmalı (K120'nin açık kalemi).
- ⛔ Uydurma sayısı **judge'ın bulduğu kadar**; bulunmamış uydurma ölçülmedi.
