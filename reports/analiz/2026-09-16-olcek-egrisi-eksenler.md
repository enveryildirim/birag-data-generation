# Ölçek eğrisi — ilk nokta, dört eksende

**Betikler:** `scripts/analiz/2026-09-16-olcek-egrisi-eksenler.py` ·
`...-olcek-egrisi-ilk-nokta.py` (golden.dev)
**Tarih:** 2026-09-16 · **Judge:** YOK (`eksen_eval` deterministik)

Üç kol; LoRA kapsamı · LR · tohum · template **birebir aynı** (K113'ün kontrol kolu):

| kol | veri | adım |
|---|---|---:|
| `TABAN` | — (ham model) | — |
| `v005-referans` | v0.0.5 · 155 kayıt | 372 |
| `v006-adimsabit` | v0.0.6 · 214 kayıt | 372 ⇒ v005 ile tek fark **VERİ** |
| `v006-3epoch` | v0.0.6 · 214 kayıt | 513 ⇒ adimsabit ile tek fark **ADIM** |

---

## 1. Otomatik iddia sonuçları

| set | TABAN | v005 | **adimsabit** | 3epoch |
|---|---:|---:|---:|---:|
| `safety_crisis` | 91/138 | 85/138 | **89/138** | 90/138 |
| `context_fidelity` | — | 49/77 | **48/77** | 46/77 |
| `forgetting_smoke` | — | 53/54 | **53/54** | 52/54 |
| `sycophancy` | — | 57/105 | **62/105** | 58/105 |

⭐ **En iyi kol `adimsabit`** — dört setin üçünde en iyi ya da berabere.

---

## 2. ⭐⭐ İki etki TERS yönde

| set | VERİ etkisi (155→214) | ADIM etkisi (372→513) |
|---|---:|---:|
| `safety_crisis` | **+4** | +1 |
| `context_fidelity` | **-1** | -2 |
| `forgetting_smoke` | **+0** | -1 |
| `sycophancy` | **+5** | -4 |
| **TOPLAM** | **+8** | **-6** |

---

## 3. ⛔⛔ Val loss inerken eksen performansı düştü

```
372 adım → val loss 2.823
513 adım → val loss 2.780      ← İNİYOR
```

Aynı 141 adımda **dört eksenin üçünde** otomatik iddia geçme sayısı **düştü**.

➡️ *Val loss bir checkpoint seçim ölçütü olarak yanıltıcıdır: aynı doğrulama
kümesinde inerken, eğitimin amacı olan eksenlerde gerileme oluyor.* Kural 5'in
*«checkpoint seçimi Pareto noktasıdır»* şartı burada somutlaştı.

⛔ **Pratik sonuç:** `plan.md` §9'un **3-epoch tavanı bu korpus boyunda aşırı**;
372 adım (~2,2 epoch) daha iyi. ⚠️ Tek korpus boyunda, tek LoRA kapsamında
ölçüldü — genel bir kural değil.

---

## 4. Eksen eksen okuma

**`safety_crisis` — §8b diliminin sınavı.** `herhangi_biri` (yönlendirme ölçütü):
**19** (taban) → **16** (v005, ⛔ gerileme) → **18** (v0.0.6). Faz 4'ün
*«eğitilen model yönlendirmeyi hiç yapmıyor»* teşhisinden tasarlanan dilim, o
teşhisin ölçüldüğü metriği **onardı** — ama tabana 2 kaldı.

⚠️ **Ölçütün kendi kusuru duruyor (T62/K136, T92):** kabul listesi kurum adlarını
geçiriyor ve elle okunmuş yönlendirmelerin yalnız **%75'ini** yakalıyor ⇒ 18/20
**iyimser**.

⛔ **`rakam_yok` 20 öğenin 9'unda düşüyor — HAM MODELDE DE.** Model kriz
öğelerinde `112` yazıyor; eğitim bunu değiştirmiyor (taban 12/20, kollar 11-12/20).
K18 sayıların ağırlıklara girmemesini şart koşuyor. ⛔ Kriz anında `112` yazmanın
klinik doğruluğu **uzman/etik kurul kalemi**; burada yalnız ölçütün ne dediği
bildiriliyor. **Hiç ele alınmamış açık.**

**`sycophancy` — en çok yararlanan eksen (+5).** parti2'de dalkavukluğa **özel bir
dilim yoktu**. ⚠️ Mekanizma **ölçülmedi**; §5a'nın sorusuz bitişleri ve
`nazikce_karsi_cikma` kayıtları olabilir — **bu benim tahminim**.

**`forgetting_smoke` — 53/54 sabit.** Veri eklemek genel yeteneği bozmadı. Tek
düşüş 3epoch'ta (`dil` 6→5), yani yine **adımdan**.

⛔ **`context_fidelity` — tek gerileyen eksen.** parti2'ye **6** bağlam kaydı
eklenmişti (§7a). Veri etkisi −1 (gürültü bandında), asıl düşüş adımdan (−2).
⚠️ 6 kayıt bu eksende veri etkisini okumak için **yetersiz**.

---

## 5. Şerhler

- ⛔ **n küçük:** set başına 15-30 öğe; tek öğe tabloda **1 puan**.
- ⛔ **Gürültü tabanı ölçülmedi.** Greedy üretim aynı adaptörde bayt aynı (K105),
  ama veri bölmesi tohumunun etkisi ölçülmedi ⇒ ±1-2'lik farklar okunamaz.
- ⛔ **Judge iddiaları denetlenemedi** (K96/K97): `safety_crisis`in 38,
  `sycophancy`nin 41, `context_fidelity`nin 22 iddiası tabloda **yok**.
- ⛔ **TABAN yalnız `safety_crisis`te var**; öteki üç sette ham model koşulmadı ⇒
  *«eğitim genel olarak yardı mı»* sorusu o setlerde **cevapsız**.
- ⛔ `golden.dev` ayrı raporda: orada ayrışan tek iddia `soru_sayisi_maks`'tı ve o
  da parti2'nin doğrudan öğrettiği şey ⇒ **manipülasyon kontrolü**, performans değil.
- ⚠️ Tek LoRA kapsamı (`A-dar`); kapsam × veri etkileşimi **ölçülmedi**.
