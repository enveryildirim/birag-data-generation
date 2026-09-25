# 1.000 kayda ne kaldı

**Betik:** `scripts/analiz/2026-09-16-bin-kayit-mesafesi.py` · **Tarih:** 2026-09-16
**Çıktı:** `reports/analiz/2026-09-16-bin-kayit-mesafesi.json`

---

## 1. Hedef nereden geliyor

`plan.md` §6: **v0.1.0 = ~800-1.200 kayıt**, *"HER dilim temsil edilir —
iterasyon döngüsünün girdisi"*. Bu raporda **1.000** alınıyor, bandın ortası.

⚠️ Form hedefi (İP1) **bu değil**: o **10.000**. İkisi karıştırılmamalı —
v0.1.0 bir **ara durak**, 10.000 ise başvuru taahhüdü. Üstelik plan §6 10.000'i
kendisi koşullu bırakıyor: *"Faz 5 ölçekleme testi: kazanım düzse 10.000
gereksiz"*.

---

## 2. Bugünkü durum

| | adet |
|---|---:|
| **yayımlanmış tekil kayıt** (`datasets/v*` birleşimi) | **175** |
| en güncel sürüm `v0.0.5` | 155 |
| **üretilmiş tekil kayıt** (aday ∪ yayımlanmış) | **312** |
| yayımlanmayı bekleyen | 137 |
| ↳ bunun **v4-parti2** olanı (bugün) | **60** |

⛔ **`data/candidates/` ile `datasets/` TOPLANMAZ.** v4-parti1'in 40 kaydının
**38'i** zaten `v0.0.3+` içinde; toplamak onları iki kez sayar (T91).

**1.000'e kalan:** yayımlanmışa göre **825**,
üretilmişe göre **688**.

⚠️ **Aradaki 137 kaydın hepsi yayıma aday değil:**
`{'uretim-v2': 70, 'uretim-v3': 5, 'uretim-v4': 62}` — **70'i `uretim-v2`** ile üretilen `expert-70`, yani
uzman **puanlama seti**; süperse edilmiş bir talimat sürümüyle yazıldı ve
olduğu gibi yayımlanmaz. ⇒ Gerçekçi taban **175 + 60 (judge'dan geçerse)**.

---

## 3. Dilim açığı — 1.000 ölçeğinde

| dilim | hedef | üretilmiş | açık | kilit |
|---|---:|---:|---:|---|
| `terapotik_tek_tur` | 350 | 183 | **167** |  |
| `replay` | 150 | 18 | **132** | ⛔ Claude Code üretimi DEĞİL |
| `rag` | 100 | 30 | **70** |  |
| `terapotik_cok_tur` | 150 | 81 | **69** |  |
| `kriz_rol_siniri` | 100 | 38 | **62** | ⛔ kriz alt-dilimi ETİK KURUL bekliyor |
| `kapsam_disi_sinir` | 50 | 14 | **36** |  |
| `nazikce_karsi_cikma` | 50 | 17 | **33** |  |
| `direnc_inkar_discord` | 50 | 36 | **14** |  |

⚠️ **plan.md §6'nın 8 satırı bölüntü DEĞİL.** İlk dördü tur **yapısı**
(gerçek bölüntü: replay · rag · terapötik çok/tek tur), son dördü **senaryo**
ve birbirini kesiyor — aynı kayıt hem `terapotik_tek_tur` hem `rol_siniri`
olabilir. Yüzdeler 100 ediyor ama kesişim var ⇒ iki görünüm ayrı sayıldı ve
**satırlar toplanmamalı**.

⚠️ `kapsam_disi_sinir` için ayrı bir etiket yok; `scenario == bilgilendirme`
**vekil** olarak kullanıldı — bu satır en zayıf ölçüm.

---

## 4. ⛔ İki dilim Claude Code üretimiyle kapanmıyor

- **`replay` (açık 132)** — plan §6: *"açık genel amaçlı setlerden örneklenir"*.
  Bu bir üretim işi değil, **örnekleme** işi; 18 kayıt var.
- **`kriz_rol_siniri` (açık 62)** — rol sınırı tarafı bugün üretildi (parti2'nin
  §8b dilimi), ama **kriz alt-dilimi ETİK KURUL** bekliyor (K23, `uretim-v4` §8b'nin
  Kural 3 sınırı). Faz 4'ün çıkış kapısındaki tek kilit de bu.

⇒ Claude Code'un tek başına kapatabileceği açık ≈ **556** kayıt.

---

## 5. Hız

| parti | kayıt |
|---|---:|
| v3-parti1 | 40 |
| v3-parti2 | 40 |
| v3-parti3 | 24 |
| v4-parti1 | 40 |
| **v4-parti2** (bugün) | **60** |

Son parti hızıyla (**60/parti**) kalan üretilebilir açık ≈ **9-10 parti**.

⚠️ Bu bir **hız tahmini değil**, bir bölme işlemi: parti başına süre ölçülmedi
ve partiler eşit zorlukta değil (§8b dilimi elle tohum seçimi gerektirdi).
⛔ Ayrıca her parti judge'dan **kayıpsız geçmiyor**: v4-parti1'de 40 üretimden
**38** yayımlandı (%95).
