# v3 parti 3 — plan (24 satır, odağı derin çok turlu)

**Çıktı:** `data/plan/v3-parti3.jsonl` · SHA256 `282ec79c09e1b113aebb615ff32a2942ec73b686aa0b54054e4c19956192e7c9`  
**Betik:** `scripts/analiz/2026-09-14-v3-parti3-plani.py` · **Tarih:** 2026-09-14 · **Havuz:** 1858

---

## Neden bu parti farklı

`reports/analiz/2026-09-14-dilim-kapsama.md` §2 ölçtü: 80 kaydın çok turlu sayılan 18'inin **tamamı iki kullanıcı turlu**. `plan.md` §6 *"3-5 turluk alışveriş"*, `uretim-v3.md` §5c de **MI süreci geçişi** istiyor; ikisi de iki turda olmuyor. 3+ turlu kayıt sayımız **0/80**. Bu partinin **14/24** satırı 3-5 turlu ve her biri bir geçiş taşıyor.

> Geçiş **geriye** de olabilir — §C.2: MI süreçleri döngüseldir, doğrusal değil. Kullanıcı savunmaya geçtiğinde focusing'den engaging'e dönmek doğru hamledir.

## ⚠️ Hedefler kümülatif ölçülüyor

§5a/§3b/§5c **korpus düzeyi** hedefleri. Odaklı bir partiyi kendi içinde ölçmek onu haksız yere düşürürdü; bu partinin sayıları 80 mevcut kayda **eklenerek** 104 üzerinden hedefe oturacak biçimde seçildi.

## Satırlar

| # | tür | yaş | tur | MI geçişi | MI | durum | kapanış | sysvar | neg | özerk | ctx | tohum kelime |
|---:|---|---|---:|---|---|---|---|---|:--:|:--:|:--:|---:|
| 1 | alkol | yetiskin | 4 | engaging→focusing | focusing | tetikleyici_an | acik_uclu_soru | canon | — | — | — | 42 |
| 2 | kumar | yetiskin | 3 | engaging→evoking | evoking | tetikleyici_an | ozet | canon | — | — | — | 46 |
| 3 | tutun | yetiskin | 3 | focusing→evoking | evoking | suregiden_durum | acik_uclu_soru | paraphrase | — | — | — | 43 |
| 4 | receteli_ilac | yetiskin | 4 | engaging→focusing | focusing | tetikleyici_an | acik_uclu_soru | canon | ✔ | — | — | 36 |
| 5 | alkol | yetiskin | 3 | evoking→planning | planning | plan_yapma | ozet | canon | — | — | — | 44 |
| 6 | tutun | ergen | 3 | engaging→evoking | evoking | iyi_giden_paylasim | takdir | canon | — | — | — | 45 |
| 7 | kumar | yetiskin | 4 | focusing→planning | planning | plan_yapma | acik_uclu_soru | canon | — | — | — | 36 |
| 8 | alkol | yetiskin | 3 | focusing→engaging | engaging | tetikleyici_an | yalnizca_yansitma | canon | — | — | — | 31 |
| 9 | tutun | yetiskin | 3 | evoking→planning | planning | plan_yapma | acik_uclu_soru | paraphrase | — | — | — | 31 |
| 10 | receteli_ilac | yetiskin | 3 | engaging→evoking | evoking | suregiden_durum | acik_uclu_soru | canon | — | — | — | 35 |
| 11 | kumar | yetiskin | 4 | focusing→evoking | evoking | tetikleyici_an | acik_uclu_soru | canon | — | — | — | 51 |
| 12 | alkol | yetiskin | 3 | engaging→planning | planning | plan_yapma | ozet | canon | — | — | — | 45 |
| 13 | tutun | ergen | 3 | evoking→engaging | engaging | iyi_giden_paylasim | takdir | paraphrase | — | — | — | 33 |
| 14 | alkol | yetiskin | 3 | engaging→focusing | focusing | merak_sorusu | acik_uclu_soru | canon | — | — | ✔ | 38 |
| 15 | alkol | yetiskin | 1 | — | engaging | tetikleyici_an | acik_uclu_soru | canon | — | — | — | 46 |
| 16 | kumar | yetiskin | 1 | — | engaging | tetikleyici_an | yalnizca_yansitma | canon | — | — | — | 24 |
| 17 | tutun | ergen | 1 | — | engaging | tetikleyici_an | acik_uclu_soru | paraphrase | — | — | — | 37 |
| 18 | dijital | yetiskin | 1 | — | engaging | tetikleyici_an | durur | canon | — | — | — | 12 |
| 19 | receteli_ilac | yetiskin | 1 | — | focusing | suregiden_durum | acik_uclu_soru | canon | ✔ | ✔ | — | 27 |
| 20 | alkol | yetiskin | 1 | — | evoking | plan_yapma | yalnizca_yansitma | canon | — | — | — | 36 |
| 21 | tutun | yetiskin | 1 | — | evoking | iyi_giden_paylasim | takdir | canon | — | — | — | 37 |
| 22 | alkol | yetiskin | 1 | — | evoking | iyi_giden_paylasim | takdir | paraphrase | — | — | — | 46 |
| 23 | alkol | yetiskin | 1 | — | engaging | merak_sorusu | acik_uclu_soru | canon | ✔ | ✔ | ✔ | 27 |
| 24 | kumar | yetiskin | 1 | — | engaging | aradan_donus | acik_uclu_soru | paraphrase | ✔ | — | — | 27 |

## Kümülatif hedefe katkı

| Alan | Bu partide |
|---|---|
| turn_ending | `acik_uclu_soru` 13 · `takdir` 4 · `ozet` 3 · `yalnizca_yansitma` 3 · `durur` 1 |
| konusma_durumu | `tetikleyici_an` 9 · `suregiden_durum` 3 · `iyi_giden_paylasim` 4 · `plan_yapma` 5 · `merak_sorusu` 2 · `aradan_donus` 1 |
| mi_process | `engaging` 8 · `focusing` 4 · `evoking` 8 · `planning` 4 |
| sysvar | `canon` 18 · `paraphrase` 6 |
| is_negative | 4 |
| context (RAG) | 2 |
| ergen | 3 |
| özerklik görünür | 2 |

> ⚠️ **Özerklik yalnızca 2.** Kümülatif oran şu an %25, hedef %20 — yani **hedefin üstündeyiz**. Hedefin kendisi K63'te *"bu benim önerim"* diye işaretlenmişti; %25'in fazla olup olmadığı klinik bir soru ve uzmana gider. Bu partide yalnızca klinik olarak gerekli olan iki satıra kondu.

