# BıRAG veri kümesi — v0.0.8

**Tarih:** 2026-09-17 · **git** `0df9faf`
**Girdi:** `data/judged/v0.0.8.jsonl` SHA256 `a807678eb52221a2`
**Çıktı:** `train.jsonl` SHA256 `5d605d7c7d7e9890`
**Kayıt:** 571/577 (elenen **6**)

---

## 1. v0.0.7'den farkı

| | v0.0.6 | v0.0.7 | **v0.0.8** |
|---|---:|---:|---:|
| kayıt | 214 | 272 | **571** |
| yeni kayıt | 59 | 58 | **299** |
| kelime | 57.079 | 72.815 | **88.594** |

**Yeni katmanlar:** `v5-parti4` … `v5-parti8` (5 × 60 = 300 kayıt, biri karantinada).
Hepsi `uretim-v5` ile üretildi; hepsi rubrik **v9** ile yargılandı.

**Dilim dağılımı:** `terapotik_tek_tur` 256 · `terapotik_cok_tur` 188 ·
`rag_tek_tur` 85 · `rag_cok_tur` 24 · `replay` 18

---

## 2. ⛔⛔ AYNI `id`, FARKLI METİN — 16 kayıt

**v0.0.7 ile v0.0.8'de aynı `id` altında 16 kaydın metni FARKLIDIR.**

| katman | ne değişti |
|---|---|
| `v5-parti3` (4 kayıt) | §8b′ (kurum yordamı iddiası), T115 (sapma eşiği), yapısal atıf |
| `v4-parti1` (2 kayıt) | alıntı birebirliği (T105) |
| `v4-parti2` (4 kayıt) | alıntı kırpması, uydurulmuş mekân/ilişki |
| … | kalanı `v5-parti3 #54`'ün `kurum_yordam_ihlali` düzeltmesi dahil |

➡️ ⛔ **İki sürümün puanları kayıt düzeyinde KARŞILAŞTIRILAMAZ.** v0.0.7 değişmez
(Kural 4) ve düzeltilmemiş metni taşımayı sürdürür; v0.0.8 düzeltilmiş metni
taşır. Bir eğitim karşılaştırmasında bu 16 kayıt **karıştırıcı**dır.

⭐ Tam liste ve her katmanın SHA256'sı:
`reports/analiz/2026-09-17-v008-kaynak-defteri.md`

---

## 3. ⛔ Rubrik karışımı sürüyor (K137)

| judge rubriği | kayıt |
|---|---:|
| **`judge-eksen1.v9`** | **418** |
| `judge-eksen1.v7` | 135 |
| yok (`replay`) | 18 |

v9 payı **%73** (v0.0.7'de %43). ⛔ Küme hâlâ karışık; **puanlar sürüme göre
ayrılmadan havuzlanamaz.** Tekdüzelik için 135 kayıt v9 ile yeniden puanlanmalı.

---

## 4. Elenen 6 kayıt

| gerekçe | kayıt |
|---|---:|
| `judge_safety_violation` | 3 |
| `guvenlik_karantinasi` | 3 |

⭐ Karantinaya bu sürümde **bir kayıt eklendi** (`v5-parti7 #31`): kullanıcı
*«öleceğim ama içeceğim»* diyor ve cevap susma isteğine uyup bu cümleye hiç
dokunmuyor. Bu cümleye nasıl karşılık verileceği **kriz davranışı kararıdır**
ve uzman + etik kurul onayına bağlıdır (Kural 3); kaydı düzeltmek de o kararı
vermek olurdu. Gerekçe `data/guvenlik-karantinasi.jsonl`'de yazılıdır.

---

## 5. Bu sürümde kapatılan kusurlar

Judge 360 kaydı kör okudu; kapılar eski katmanlara ilk kez geriye dönük koşuldu.

| kusur | önce | sonra |
|---|---:|---:|
| K1 — klinik güvenlik / rol sınırı | 13 | **3** |
| K2 — dayanaksız iddia | 48 | **5** |
| K3 — MI tuzağı | 86 | **84** |

⭐ En büyük K2 sınıfı tek bir kusurdu: **16 kayıt kurumun ne yaptığını ya da ne
zaman açık olduğunu dayanaksız iddia ediyordu** (§8b′). Düzeltme bilgiyi
silmedi, **yanlış kesinliği** sildi.

Bu döngüde yazılan kurallar: **§5a‴** (adlandırmak ≠ yönlendirmek ≠ ders vermek) ·
**§5a⁗** (reddetmek devretmeyi gerektirir) · **§8b′** (kurum erişilebilirliği
iddia edilemez) · **§8c′** (itiraz gösterir, tartışmaz) · **§8d′**.

---

## ⛔ Bu kartın söylemedikleri

| | |
|---|---|
| ⛔ **K3 kasten düzeltilmedi** | 84 MI tuzağı sette **duruyor**. İlk eğitim ölçülmeden hepsini düzeltmek, hangi revizyonun işe yaradığını ölçülemez yapardı |
| ⛔ **Hakem Claude ailesinden** (K43/K45) | judge çıktısı **metrik değil**, veri revizyonu sinyali; yanlış pozitif oranı uzmanla ölçülmedi (K58 50/70'te kapandı) |
| ⛔ **Kriz dilimi hâlâ yok** | ~%10 hedefti; etik kurul + uzman onayı bekliyor (Kural 3) |
| ⛔ **Vahşi doğa dilimi yok** | aday kaynakların tamamı elendi |
| ⛔ **Taban katman türetilemiyor** | `v0.0.7.jsonl` elle birleştirilmişti; kaynak defteri o noktada kopuyor |
| ⚠️ **Devralınan puanlar** | metni değişmeyen kayıtlar puanlarını ilk koşudan devraldı (metin birebirliği kanıtlanarak); hakem aynı metni bugün farklı puanlayabilirdi |
| ⚠️ **Kelime, token değil** | K46/T81 ile karşılaştırılabilirlik için |
| ⚠️ **`register` ekseninde resmiyet yok** | 3 kayıtta tek kişiye «siz» diye hitap ediliyor ve ızgarada bunu kuran bir eksen yok |
