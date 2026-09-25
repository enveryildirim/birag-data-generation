# BıRAG veri kümesi — v0.0.7

**Tarih:** 2026-09-16 · **git** `944d722`
**Girdi:** `data/judged/v0.0.7.jsonl` SHA256 `71e501a047179dc6`
**Kayıt:** 272/275 (elenen **3**)

---

## 1. v0.0.6'dan farkı

| | v0.0.6 | **v0.0.7** |
|---|---:|---:|
| kayıt | 214 | **272** |
| yeni kayıt | 59 (`v4-parti2`) | **58** (`v5-parti3`) |
| kelime | 57.079 | **72815** |

`v5-parti3` ilk **`uretim-v5`** partisidir ve ızgarası ilk kez **elle değil KISITLA**
kuruldu: marjinal kotalar ile hücre yasakları birlikte çözüldü
(`scripts/analiz/2026-09-16-v5-parti3-plan.py`). Altı korpus ekseni **+0.0**.

**Dilim dağılımı:** {'terapotik_tek_tur': 137, 'terapotik_cok_tur': 83, 'rag_tek_tur': 25, 'rag_cok_tur': 9, 'replay': 18}

**v5'in üç bahsi** (`prompts/uretim-v5.md`, hepsi ölçümden):
- bağlam dilimi **%10 → %25** (6 → 15 kayıt) — `context_fidelity` gerileyen tek eksendi
- §8b **%33 → %15** (20 → 9) — dilim işini yapmıştı (`herhangi_biri` 16→18/20)
- `nazikce_karsi_cikma` **%15 KOTA oldu** (0 → 9) — `sycophancy` +5 ile en çok
  yararlanan eksendi ve özel dilimi yoktu

---

## 2. ⛔ Rubrik karışımı sürüyor

| judge rubriği | kayıt |
|---|---:|
| `judge-eksen1.v7` | 137 |
| **`judge-eksen1.v9`** | 117 |
| yok (replay) | 18 |

⚠️ v9 payı %43'e çıktı ama küme hâlâ karışık.
Puanlar **sürüme göre ayrılmadan havuzlanamaz** (K137). ⛔ Tekdüzelik için 137
kaydın v9 ile yeniden puanlanması gerekir — **yapılmadı**.

---

## 3. Elenen kayıtlar — 3

- `judge_safety_violation`

**v5-parti3'ten ikisi** (`#32`, `#35`): judge `guvenlik_tipi: riski_atlama` verdi —
kullanıcı bedensel bir işaret anlatıyor (sararmış parmak ucu / her sabah öksürük),
cevap doğrudan davranışsal çerçeveye geçiyor. ⛔ Hüküm **uzman/etik kurul kalemi**
(Kural 3); ⚠️ **yön şerhi T68**: güvenlik judge'ları tek yönlü tedbirli sapıyor ⇒
bu eleme bir **üst sınırdır**, yanlış pozitif oranı uzmana karşı **hiç ölçülmedi**.

Üçüncüsü `v4-parti2`'den geliyor (`#34`, aynı sınıf).

---

## 4. ⛔⛔ Bu sürümün en önemli kaydı: ÜRETİM GERİLEDİ

`uretim-v5` §3a′ (*«cevap, KIRPILMIŞ mesajın üstünde durmalı»*) tam olarak
uydurulmuş ayrıntıyı önlemek için yazıldı. Ölçüldü:

| | v4-parti2 | **v5-parti3** |
|---|---:|---:|
| uydurulmuş ayrıntı (judge) | 2/54 | ⛔ **6/58** |
| `klinik_guvenlik_ihlali` | 1 | **2** |
| `kurum_yordam_ihlali` | 0 | **1** |
| `anlasilirlik ≤ 2` | 5 | **8** |

⛔ **Kural yazıldı, kusur üçe katlandı.** Altısı da düzeltildi ve yeniden
puanlandı (**0/57**), ama düzeltilmiş olması gerilemeyi silmez: kural yazıldığı
hâlde üretim sırasında tutulmadı.

⭐ **Altı uydurmanın hiçbiri tırnaklı değildi** ⇒ `thinking-alinti-denetimi`
hiçbirini göremezdi. Biçimleri: kaynak atfı (*«doktorunun söylediği»*), zaman
damgası (*«öğleden sonra… gece»*), zamansal ilişki (*«üçü de aynı akşamda»*),
mekân (*«merdivende»*) ve anlatılmamış bir **örüntünün tamamı** (`#10`).

⛔⛔ **`#10` en ağırı:** kullanıcının beş kelimelik mesajında alkolden hiç söz
yokken cevap bir içki örüntüsü kurdu **ve** *«üçünü de sen yazdın»* diyerek onu
kullanıcıya **mal etti**.

⭐ **`#21` bir alt sınıf gösterdi:** uydurma son turda değil, modelin **kendi
önceki turunda** doğmuş (*«aynı akşam»*) ve son tur onu yerleşik olgu gibi
tekrarlamış. ⇒ Çok turlu kayıtta kaynak yalnız kullanıcı turları olmalı.

---

## 5. Şerhler

- ⛔ **Kalite ölçülmedi**; bu kart üretim ve kapı sonuçlarını bildirir.
- ⛔ `dogallik` ve `mi_uyumu` **kanıt değil** (K61).
- ⛔ Judge **Claude** (K43/K45; Gemini kotası tükendi — K96) ⇒ eleştirmen
  işlevinde okunmalı. **k=1**, kayıt düzeyinde tek karar gürültü tabanının
  altında (K103).
- ⛔ **Uydurma sayısı judge'ın bulduğu kadardır**; bulunmamış uydurma ölçülmedi.
  6 ve 2 sayıları **alt sınır**.
- ⛔ **Kriz dilimi yok** (etik kurul) · **vahşi doğa dilimi yok**.
- ⚠️ `motivation` bu partide **tohumdan** okundu (T95/T101) ve katmanlı örneklendi;
  v0.0.6 ve öncesinde ızgaradan geliyordu ⇒ **küme içinde iki ayrı yöntem** var,
  ham değer `gen_meta.motivasyon_tohum`'da.
- ⚠️ `#54`'ün `kurum_yordam_ihlali`'i düzeltilmedi: cevap *«Belge bir kâğıt
  istiyor, içmemeni değil»* derken bağlamsız bir yordam iddiası kuruyor.
  `build.py` bunu **elemiyor** (kapı yalnız `klinik_guvenlik_ihlali`) ⇒ kayıt
  sette **duruyor** ve açık kalem olarak yazıldı.
