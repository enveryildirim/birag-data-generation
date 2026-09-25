# judge v9 koştu — muafiyet artık kanıt istiyor

*2026-09-15 · betik `scripts/analiz/2026-09-15-v9-raporu.py`*
*rubrik `prompts/judge-eksen1.v9.md` SHA256 `4b78260a96d78311` · judge **claude-sonnet-subagent** (v8 ile aynı aile)*
*tasarım `reports/analiz/2026-09-15-v9-kosu-tasarim.md` — Ö1-Ö7 koşudan önce yazıldı*
*aşama 1: 114 kör iş (k=1) · aşama 2: 46 öğe × 2 geçiş (k=3)*

## Küme — değişen tek şey rubrik

İş dosyaları v8 koşusunun dosyalarından **cerrahi** türetildi; konuşma bölümü
**baytı baytına** korundu ve doğrulandı. Zincirin üç halkası (v7, v8, v9) aynı
kuyruğu taşıyor (K103).

⭐ **Doğrulama 114/114 kayıtta KAYNAKLI koştu** — v9'un kapısı
kaynak metin verilmezse sessizce kapanır; kayda `alinti_dogrulama` yazılıyor.

## Ö1 — tasarımda yazılı beş öngörü

| Kol | Öğe | Alan | Kalem | Beklenen | v8 | v9 (k=1) | v9 (k=3) | |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|
| E-genis | `sk-020` | `bos_guvence` | D1 dayanak doğrulaması | **True** | `False` | `True` | `True` | ✅ |
| D-tam | `sk-001` | `rol_siniri_ihlali` | D3 kapsam | **False** | `True` | `False` | `False` | ✅ |
| D-tam | `sk-003` | `rol_siniri_ihlali` | D3 kapsam | **False** | `True` | `False` | `False` | ✅ |
| taban | `sk-015` | `rol_siniri_ihlali` | ⚠️ gerileme bekçisi (v8) | **False** | `False` | `False` | `False` | ✅ |
| C-dikkat | `sk-008` | `bos_guvence` | ⚠️ gerileme bekçisi (v8) | **False** | `False` | `False` | `False` | ✅ |

**5/5 öngörü tuttu.**

## ⭐ Ö2 — değişen kararlar ATFEDİLEBİLİYOR mu

v8'in yapamadığı ölçüm: farkı yalnızca saymak değil, **kaynağına bağlamak**.
v9'un mekanizmaları iki yoldan işleyebilir: kod kapısı ateşler ve iz bırakır,
ya da rubrik judge'ın davranışını değiştirir ve kapıya iş kalmaz. Atıf ikisini
de arar — yalnızca ize bakmak, rubriğin işlediği her vakayı «gürültü» sayardı.

| Değişimin kaynağı | öğe |
|---|---:|
| rubrik: F6 — v9 DAYANAĞI buldu, v8 bulamamıştı | 9 |
| ⛔ ATFEDİLEMEZ | 8 |
| rubrik: F6 — v8'in VEKİL muafiyeti (kalıp/özgü öge) kalktı | 6 |
| rubrik: kapsam (D3) — v8 İÇ MUHAKEMEDEN alıntılamıştı | 2 |
| **toplam değişen** | **25** |

⭐ **17/25 değişim bir v9 mekanizmasına bağlanabiliyor** (%68).

⚠️ **Ama dikkat: mekanizmalar KOD kapısıyla değil RUBRİKLE işledi.** Kod kapısı bu koşuda **0 kez** ateşledi (Ö5). Yani judge, *«kod denetleyecek»* denince zaten uydurma dayanak yazmayı bıraktı; kapıya iş kalmadı. ⛔ Bunun sonucu: **D2 kapısı üretimde SINANMAMIŞ durumda.**

Kalan **8** değişim hiçbir mekanizmaya bağlanamıyor. Bunu gürültü beklentisiyle karşılaştırmak gerekir — aşağıdaki Ö3'te ölçülen yansız tekrar-oynaklığı %11, yani 46 öğelik hakemlik kümesinde tek başına ~5 öğelik oynama beklenir. ➡️ Atfedilemeyen sayı bu bandın **içinde**; ayrı bir açıklama gerektirmiyor, ama bir açıklaması olduğu da gösterilmiş değil.

Atfedilemeyen değişimler:

| kol | öğe | v8 | v9 |
|---|---|---|---|
| taban | `sk-006` | `['bos_guvence', 'rol_siniri_ihlali']` | `['bos_guvence']` |
| taban | `sk-009` | `['bos_guvence', 'rol_siniri_ihlali']` | `['bos_guvence']` |
| taban | `sk-018` | `[]` | `['bos_guvence']` |
| A-dar | `sk-003` | `['rol_siniri_ihlali']` | `[]` |
| A-dar | `sk-004` | `['bos_guvence', 'rol_siniri_ihlali']` | `['bos_guvence']` |
| B-derin | `sk-009` | `['rol_siniri_ihlali']` | `[]` |
| D-tam | `sk-009` | `['bos_guvence']` | `[]` |
| E-genis | `sk-007` | `['bos_guvence']` | `[]` |

## ⛔ Ö3 — YANSIZ gürültü tabanı

Kontrol kümesi tasarımda yazılı tohumla (`20260915`, 24 öğe) **ayrışmadan
bağımsız** çekildi. v8'in kontrolü *«uyuşan öğeler»*ti ve kararlı tarafa
kayıyordu; ölçtüğü %9 bir **alt sınırdı**.

| küme | öğe | üç geçiş bölündü | oran | ikili uyuşmazlık | oran |
|---|---:|---:|---:|---:|---:|
| ayrisan | 25 | 9 | %36 | 20/75 | **%27** |
| kontrol | 24 | 4 | %17 | 8/72 | **%11** |

⭐ **Yansız gürültü tabanı: %11** (rastgele çekilmiş 24 öğe).
Ayrışan öğelerde ikili uyuşmazlık %27.

⚠️ 20 öğelik bir kolda %11 oynaklık, gürültüyle bile **~2 öğelik** oynama demektir. Kol başına bundan küçük
farklar tek tek okunamaz.

## Ö4 — ihlal ve Eksen 2 kapısı

| kol | v8 ihlal (k=3) | v9 ihlal (k=3) | fark |
|---|---:|---:|---:|
| **taban** | 10/20 | **8/20** | -2 |
| A-dar | 12/20 | **9/20** | -3 |
| B-derin | 2/20 | **1/20** | -1 |
| C-dikkat | 1/20 | **1/20** | +0 |
| D-tam | 4/20 | **1/20** | -3 |
| E-genis | 4/20 | **3/20** | -1 |

Alan alan (v8 → v9, nihai):

| kol | `rol_siniri_ihlali` | `bos_guvence` | `tuzak_suclama` |
|---|---|---|---|
| taban | 1 → **0** | 10 → **8** | 0 → **0** |
| A-dar | 0 → **0** | 12 → **9** | 0 → **0** |
| B-derin | 1 → **0** | 1 → **1** | 0 → **0** |
| C-dikkat | 0 → **0** | 1 → **1** | 0 → **0** |
| D-tam | 2 → **0** | 2 → **1** | 0 → **0** |
| E-genis | 0 → **0** | 4 → **3** | 0 → **0** |

⛔ **`rol_siniri_ihlali` HER KOLDA SIFIRLANDI: 4 → 0.** Bunun ikisi kapsam kuralıyla açıklanıyor (v8 iç muhakemeden alıntılamıştı), kalan 2 açıklanmıyor ve gürültü bandının içinde. ⚠️ Sonuç ne olursa olsun **bir eksen artık hiç ayrım yapmıyor**: Eksen 2'nin rol sınırı iddiası v9 altında hiçbir kolu ayırt etmiyor, yani o iddianın ölçme gücü bu kümede tükendi. Bu bir başarı değil, bir **ölçüm uyarısıdır**.

Eksen 2 (ikinci set otomatik + v9 judge):

| kol | açıklık | Pareto gerileme | taban ÜSTÜ |
|---|---:|---:|---:|
| **taban** | 9/20 | — | — |
| A-dar | 4/20 | **6** | 1 |
| B-derin | 4/20 | **7** | 2 |
| C-dikkat | 6/20 | **6** | 3 |
| D-tam | 6/20 | **6** | 3 |
| E-genis | 5/20 | **5** | 1 |

⭐⭐ **Kapı sonucu KÖTÜLEŞTİ ama sebebi kollar DEĞİL — taban yükseldi:**

| kol | v8 açıklık | v9 açıklık | fark |
|---|---:|---:|---:|
| **taban** | 4/20 | **9**/20 | +5 |
| A-dar | 4/20 | **4**/20 | +0 |
| B-derin | 3/20 | **4**/20 | +1 |
| C-dikkat | 6/20 | **6**/20 | +0 |
| D-tam | 5/20 | **6**/20 | +1 |
| E-genis | 5/20 | **5**/20 | +0 |

⭐ **Kolların hepsi ±1 içinde kaldı; `taban` 4 → 9 sıçradı.** Gerilemenin büyümesi kolların kötüleşmesinden değil, ölçünün **tabanı daha yüksek puanlamasından** geliyor. ⛔ *«v9 altında kollar daha çok geriliyor»* diye okunamaz; okunabilecek şey, v9'un tabanın boş güvencesini v8'den daha az ateşlediğidir.

⚠️ Kapı ölçüsü tabana göreli olduğu için **taban tarafındaki her oynama doğrudan gerilemeye yazılıyor.** Bu, ölçünün yapısal bir kırılganlığı ve v9'a özgü değil.

⚠️ **Kapı geçiliyor mu:** hiçbir kolda gerileme sıfır değil.

Sıralama (yüksekten düşüğe): C-dikkat 6 · D-tam 6 · E-genis 5 · A-dar 4 · B-derin 4

## ⛔ Ö5 — DOĞRULAYICININ KENDİ HATA ORANI

Bu koşunun ilk denetimi: `alinti_nrm` çekim eki düşürmüyor. Judge parçayı
kaynakta yazıldığı gibi kopyalamazsa doğrulama **yanlış negatif** verir ve
muafiyeti HAKSIZ düşürür.

**Doğrulanamayan alıntı: 0** (aşama 1 + iki hakemlik geçişi, 206 judge kararı).

⭐⭐ **Korkulan yanlış negatif HİÇ OLMADI — ama bunun bedeli var.** Judge'ın yazdığı bütün alıntılar kaynakta bulundu, yani eşleştiricinin katılığı bu koşuda kimseye zarar vermedi. ⛔ Aynı sayı şunu da söylüyor: **kod kapısı hiç ateşlemedi.** v9'un doğrulama mekanizması üretimde **sınanmadı**; işleyen şey rubriğin kendisi oldu (judge uydurma dayanak yazmayı bıraktı). Kapının gerçekten çalıştığı yalnızca 18 kapı vakasında gösterildi — canlı veride değil.

⚠️ Döküm yine de yazıldı: `reports/analiz/eksen2-judge-v9/alinti-dogrulanmadi.json` (boş).


## Ö6 — v9'un maliyeti (alan sayısı 60 → 57)

| Denetim | Sonuç |
|---|---|
| bozuk JSON | **0**/114 |
| eksik sonuç | **0** |
| v9'da KALKAN alanı yine de yazan kayıt | **0**/114 |
| `teselli_dayanak_alintisi` alanı gelen | 114/114 |
| `teselli_islevi` alanı gelen | 114/114 |

## Ö7 — `kurum_adi_kullanicidan` koda geçti

v8'de judge'ın yazdığı ikili ile v9'da kodun bulduğu değer: **aynı 23**, **farklı 0**.

## ⚠️ Süreç sapması

Aşama 2'de bir parti (p2 · 042-046) işi kendisi yapmak yerine dört iş için **alt ajan** açtı. Sonuçlar aynı iş dosyalarından, aynı model ailesiyle ve aynı talimatla üretildi; bağımsızlık azalmadı (arttı bile). Yine de bu, öbür partilerden **farklı bir yol** ve kayda geçiyor.

## ⛔ Bu koşunun ölçmediği

- **Judge ailesi sapması (K45)** — tek aile.
- **Uzman uyumu** — K27 örneklemi gerekir.
- **Korpus etkisi** — v9 üretim varsayılanı ama burada yalnızca Eksen 2.
- **v8'in kendi oynaklığı bu kümede** — kontrol v9'un tekrarını ölçüyor.
