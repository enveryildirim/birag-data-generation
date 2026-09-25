# v3 parti 2 — bağlam (RAG) dilimi planı

**Çıktı:** `data/plan/v3-parti2-baglam.jsonl` · SHA256 `cbb38d0573ba0665e4bc499fa5fdeddad389c8a99ba99ac2e220598d627c58c7`  
**Betik:** `scripts/analiz/2026-09-14-v3-parti2-baglam-plani.py` · **Tarih:** 2026-09-14

---

## Neden 8 satır

`plan.md` §6 RAG dilimini **%10** istiyor. Parti 1'de **0/40** vardı; **8/80 = %10**, iki parti birlikte hedefe oturuyor.

## Davranış dağılımı (§7a)

| Davranış | Satır | Hedef |
|---|---:|---:|
| `cevapla` | 4 | 4 |
| `yetersiz` | 2 | 2 |
| `izin_iste` | 1 | 1 |
| `ilgisiz` | 1 | 1 |

> `cevapla` v2'de **0/9**'du — dilimin ana işi o.

## Satırlar

| # | davranış | senaryo | tür | yaş | MI | durum | kapanış | sysvar | neg | format |
|---:|---|---|---|---|---|---|---|---|:--:|---|
| 1 | cevapla | ambivalans | alkol | yetiskin | engaging | merak_sorusu | acik_uclu_soru | canon | — | `xml` |
| 2 | yetersiz | ambivalans | alkol | yetiskin | engaging | merak_sorusu | acik_uclu_soru | canon | ✔ | `koseli` |
| 3 | cevapla | nazikce_karsi_cikma | receteli_ilac | yetiskin | focusing | merak_sorusu | yalnizca_yansitma | paraphrase | — | `tire` |
| 4 | izin_iste | kayma_nuks | alkol | yetiskin | engaging | aradan_donus | acik_uclu_soru | canon | — | `markdown` |
| 5 | ilgisiz | ambivalans | tutun | yetiskin | evoking | suregiden_durum | yalnizca_yansitma | canon | — | `parantez` |
| 6 | yetersiz | rol_siniri | alkol | yetiskin | focusing | plan_yapma | acik_uclu_soru | canon | ✔ | `xml` |
| 7 | cevapla | ambivalans | kumar | ergen | engaging | merak_sorusu | acik_uclu_soru | canon | — | `koseli` |
| 8 | cevapla | rol_siniri | alkol | yetiskin | engaging | merak_sorusu | durur | paraphrase | — | `tire` |

**Format varyantı: 5** (koseli, markdown, parantez, tire, xml) — K17 4-5 istiyor.

## ⚠️ Yaş gevşetmesi

Şema yalnızca `yetiskin|ergen` tanıyor (v3 §1); tohumun kendi etiketi farklı:

- #3: tohum `yasli` → plan `yetiskin`

## ⚠️ Bu dilimin bilinen sapması

Kapanış: 5/8 soruyla bitiyor (%62), §5a hedefi %50. Sekiz satırlık bir dilimde bu **tek kayıtlık** bir oynama; parti 2'nin kalan 32 kaydı bunu dengelemek zorunda. Korpus raporu parti 2'nin tamamında denetleyecek.

> ⚠️ **§5a'da açık:** #4 bir **izin sorusu** ile bitiyor (*"paylaşmamı ister misin?"*) — bu açık uçlu bir soru değil, ama §5a'nın beş kategorisinde izin sorusunun karşılığı yok. `acik_uclu_soru` beyan ediliyor çünkü kapı soru VARLIĞINA bakıyor; kategorinin dar kaldığı Oturum 3'e not edildi.

