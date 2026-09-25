# v5-parti4 üretildi — 60 kayıt, dört kapı, bir Kural 3 bulgusu

*2026-09-17 · korpus `data/candidates/v5-parti4.jsonl` SHA256 `8f10f3414c02b5ef` · 60 kayıt*
*plan `data/plan/v5-parti4.jsonl` · prompt `prompts/uretim-v5.md` (v4 üstüne delta)*

## 1. Izgara — marjinaller

Altı eksenin tamamı **+0.0** sapmayla tuttu (`bicim`, `register`,
`konusma_durumu`, `mi_process`, `turn_type`, `sinir_tipi`). Tek sapma
`turn_ending`: `acik_uclu_soru` +1.7, `yalnizca_yansitma` −1.7.

⭐ Bu sapma **tesadüf değil, ilan edilmiş**: `#14` §5a′ gereği güvenlik
check-in'i yaptı ve `yalnizca_yansitma` soru yasağını çiğnedi.

## 2. ⛔ Plan ↔ kayıt farkı: 4 — dördü de `gen_meta.izgara_sapmasi` taşıyor

| # | eksen | plan | kayıt | gerekçe |
|---|---|---|---|---|
| 14 | `turn_ending` | `yalnizca_yansitma` | `acik_uclu_soru` | §5a′ güvenlik check-in'i |
| 17 | `sinir_tipi` | `yonlendirme_gereksiz` | `rol_siniri_yonlendirme` | göğüs sıkışması + başkasının reçeteli ilacı |
| 16 | `sinir_tipi` | `yok` | `rol_siniri_yonlendirme` | ödeme tehdidi + evde yalnız |
| 42 | `sinir_tipi` | `yok` | `rol_siniri_yonlendirme` | üç gün uykusuzluk + titreme |

⭐ Üçü de **§5a′ ilkesinin** uygulaması: *güvenlik ekseni dilim kotasına tabi
değildir.* ⚠️ `#24` benzer bir tehdit taşıdığı hâlde **sapmadı** — kullanıcı
polisi kendisi gündeme getirmişti; sapma refleks değil karar.

⭐ Üç sapmaya rağmen §8b dilimi **9/60 = %15.0**, v5 hedefinin tam üstünde.

## 3. Kapılar

| kapı | sonuç |
|---|---|
| `src/checks.py` (beyan↔metin) | **60/60** ✅ |
| zaman/kaynak atfı (T105/T109) | **0 bayrak** (blok bazında 4 → 1 → 0) |
| ızgara↔tohum çarpışması (T108) | **60/60 tam uyum, 0 uydurma** |
| K18 rakam + kurum özel adı | ihlal yok ✅ |
| K31 eval metniyle çakışma | çakışma yok ✅ |
| thinking:completion | ortanca **1.62x**, maks **3.68x** (tavan 4x) ✅ |
| thinking tırnaklı alıntı | 90 alıntı, 36 kaynakta yok — ⚠️ **elle okunmadı**, kusur sayılmadı |

⭐ `#44` kullanıcı bir danışma hattını andı; kayıtta **ne numara ne kurum adı**
geçiyor (K18) — hattın varlığı üç aşamaya ayrılarak karşılandı.

## 4. ⛔⛔ Kural 3 bulgusu — bu parti dışında

Kriz süzgeci tohumun **mesaj metnini** tarıyordu; tohum korpusu aynı bilgiyi
`meta.notlar.esdurumlar` alanında **beyan ediyormuş** (T107).

| | |
|---|---|
| beyanla **SERT** tohum (aktif intihar / `cok_yuksek`) | **40** / 2240 |
| bunlardan **üretilmiş** | **1** (`ce39d82bf868e5f2`, v3-parti1) |
| yayımlanmış mı | **hayır** |
| beyanla **PERSONA** tohum | **32** |
| bunlardan üretilmiş | **10** — 2'si `datasets/v0.0.3`–`v0.0.7`'de |

⭐⭐ PERSONA sınıfında üretilmiş 10 tohumun **7'si bire bir aynı `esdurumlar`
listesini** taşıyor ⇒ alan **turu değil personayı** anlatıyor. Persona düzeyinde
elemek borç/tefeci eksenini bütünüyle yok ederdi.

⛔ **Karar burada verilmedi.** Kapı SERT sınıfı eliyor, PERSONA'yı sayıp
bırakıyor; hangisinin üretilebilir olduğu uzman + etik kurulun (Kural 3).

⛔ `ce39d82bf868e5f2`'nin kaydı **elle okundu**: güvensiz içerik yok, ama
kullanıcı AMATEM'i kendisi andığı hâlde kayıtta **hiç yönlendirme yok**
(`sinir_tipi: None`).

## ⛔ Bu raporun söylemedikleri

- **Judge geçmedi.** Buradaki hiçbir sayı kalite ölçümü değil; hepsi kural kapısı.
- **v5'in üç bahsi ölçülmedi** — bağlam %25, §8b %15, `nazikce_karsi_cikma` %15
  kotalarının eğitim etkisi için v0.0.8 eğitimi gerekiyor.
- **thinking alıntılarının 36'sı okunmadı** (borç: parti1'in 23'ü, parti2.v2'nin
  7'si, parti1'in 2'si de duruyor).
- `#54` (parti3) `kurum_yordam_ihlali` **hâlâ düzeltilmedi** ve veri setinde.
