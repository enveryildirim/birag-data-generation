# v5-parti5 üretildi — 60 kayıt, altı eksende +0.0, tek sapma

*2026-09-17 · korpus `data/candidates/v5-parti5.jsonl` SHA256 `3e5acd3c63273074` · 60 kayıt*
*plan `data/plan/v5-parti5.jsonl` · prompt `prompts/uretim-v5.md`*

## 1. ⭐ Izgara — ilk kez SIFIR marjinal kayma

`bicim`, `register`, `konusma_durumu`, `turn_ending`, `mi_process`,
`turn_type` — altısı da **+0.0**. parti4'te `turn_ending` ±1.7 sapmıştı; burada
tek sapma `sinir_tipi` ekseninde ve o eksenin marjinali kota dışı.

## 2. Plan ↔ kayıt farkı: 1 — ilan edilmiş

| # | eksen | plan | kayıt | gerekçe |
|---|---|---|---|---|
| 35 | `sinir_tipi` | `yok` | `rol_siniri_yonlendirme` | 15 yaşında, evde yalnızken alkolü tatmış, «tuhaf hissediyorum» diyor |

⛔ `#35`'te bedensel bir aciliyet **olduğunu düşünmüyorum** — bir damla. Ama bunu
benim okumam belirliyor ve okuma yanlışsa bedelini reşit olmayan biri öder.
§5a′ gereği saptım, ölçülü tek cümleyle. §8b payı 9 → 10.

⭐ Kıyas için: `#3` (kafası dumanlı çocuk bırakma), `#24` (saat üçte kayıp,
uykusuzluk), `#46` (antrenmanda nefes yetmemesi), `#59` (damar tıkanıklığı)
**sapmadı** — dördünde de ya kullanıcı konuyu kendisi açmıştı ya da var olan bir
hekim ilişkisi vardı. Sapma refleks değil, her seferinde ayrı karar.

## 3. Kapılar

| kapı | sonuç |
|---|---|
| `src/checks.py` | **60/60** ✅ |
| zaman/kaynak atfı (T105/T109) | **0 bayrak** (blok bazında 2 → 1 → 0) |
| ızgara↔tohum çarpışması (T108) | **60/60 tam uyum, 0 uydurma** |
| beyanla kriz tohumu (T107) | SERT 0 · PERSONA 0 ✅ |
| K18 rakam + kurum özel adı | ihlal yok ✅ |
| K31 eval metniyle çakışma | çakışma yok ✅ |
| thinking:completion | ortanca **1.72x**, maks **3.52x** (tavan 4x) ✅ |
| tırnaklı alıntı — `content` | 22 aday **elle okundu**, **8 düzeltildi** (T112) |
| tırnaklı alıntı — `thinking` | ⚠️ 114 öge **okunmadı**, kusur sayılmadı |

## 4. Üretim sırasında bulunan üç kusur

| | |
|---|---|
| **T111** | Üretim iskeleti parti adını iki yollu sabit bir dalla türetiyordu; 15 kayıt `parti: v5-parti3` diye etiketlendi ve `checks.py` **15/15 geçti** — alan doluydu ve değer var olan bir partinin adıydı |
| **T112** | Cevap metnindeki 8 alıntı tırnak içinde **kelime eliyordu**; biri (`#33`) doğrudan T104'tü — banda sığsın diye kırpılan soru cevapta alıntılanmaya devam ediyordu |
| **kapı kusuru** | `tohum-beyan-kriz-kapisi` çıktı adı girdiden bağımsızdı ve tek partiye koşulunca tam korpus raporunu ezdi — T108'in aynı sınıfı, bu kez kendi kapımda |

⭐ `#22`, `#25`, `#43`'te aynı refleks üç kez yakalandı: kullanıcının
*«doktor»*unu *«hekim»* diye yeniden adlandırmak. `#25`'te atfın kendisi
uydurmaydı — kullanıcı o mesajda hiç hekim anmamıştı ve **kendi thinking'im
uydurmayı gerekçelendirmişti**.

## ⛔ Bu raporun söylemedikleri

- **Judge geçmedi.** Buradaki hiçbir sayı kalite ölçümü değil.
- **v5'in üç bahsi hâlâ ölçülmedi** — v0.0.8 eğitimi gerekiyor.
- `thinking` alanının 114 alıntısı okunmadı; parti1'in 23'ü, parti2.v2'nin 7'si,
  parti1'in 2'si de duruyor.
- `#54` (parti3) `kurum_yordam_ihlali` hâlâ düzeltilmedi ve veri setinde.
