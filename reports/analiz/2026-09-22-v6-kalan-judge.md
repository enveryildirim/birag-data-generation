# `v6` kalan partiler — subagent judge koşusu

**Betik:** `scripts/analiz/2026-09-22-judge-sonuclari-v6-topla.py` · **Tarih:** 2026-09-22  
**Judge:** `claude-sonnet-subagent` · **Rubrik:** `judge-eksen1.v9`  
**Toplandı:** 412/412 · eksik 0 · bozuk 0  

⛔ **Bu koşu K43/K45'i çiğnemiyor, K97'yi uyguluyor:** judge Claude subagent'lara **09-15'te kullanıcı kararıyla** taşınmıştı, aynı gerekçeyle (Gemini kotası) ve iki şartla — körlük ve ölçülebilirlik. İkisi de bu koşuda yerinde.

## Partilere yazılanlar

⛔ Gemini dosyaları **yerinde duruyor**; Claude yargıları ayrı dosyaya yazıldı ve judge **dosya adında**.

| parti | yargılanan | dosya |
|---|---:|---|
| `v6-parti3` | 60/60 | `data/judged/v6-parti3.claude.jsonl` |
| `v6-parti4` | 59/59 | `data/judged/v6-parti4.claude.jsonl` |
| `v6-parti5` | 60/60 | `data/judged/v6-parti5.claude.jsonl` |
| `v6-parti6` | 58/58 | `data/judged/v6-parti6.claude.jsonl` |
| `v6-parti7` | 57/57 | `data/judged/v6-parti7.claude.jsonl` |
| `v6-parti8` | 118/118 | `data/judged/v6-parti8.claude.jsonl` |

## ⭐ A. Bu dalganın gürültü tabanı (v9)

24 kayıt aynı dalgada **iki ayrı numarayla**, ayrı öbeklerde soruldu. ⛔ K98'in tabanı **v6** rubriğiyle ölçülmüştü; aşağıdaki sütun yalnız karşılaştırma için.

| boyut | birebir uyum | ort. \|fark\| | (K98, v6) |
|---|---:|---:|---:|
| `duygusal_tepki` | %67 | 0.38 | %70 |
| `yorumlama` | %62 | 0.38 | %65 |
| `kesif` | %92 | 0.08 | %91 |
| `mi_uyumu` | %96 | 0.08 | %100 |
| `grounding` | %100 | 0 | %100 |
| `anlasilirlik` | %50 | 0.75 | %43 |
| `dogallik` | %88 | 0.12 | %91 |

## ⭐⭐ B. Claude ↔ Gemini — aynı 42 kayıt

`v6-parti3`'ün **42** kaydı iki judge'ın ikisinde de var. ⛔⛔ Bir fark ancak **A'daki tabandan büyükse** okunabilir.

⭐ **Ölçüt (K98):** judge KENDİSİYLE ne kadar anlaşıyorsa, iki judge arasındaki fark ancak ondan **daha büyükse** sapmadır. Kendiyle olan farktan küçük bir çapraz fark, sapma değil **oynaklık** ölçer — K98 K97'nin iki sayısını tam bunun için geçersiz kılmıştı.

| boyut | Claude−Gemini | çapraz \|fark\| | kendiyle \|fark\| (A) | okunabilir mi |
|---|---:|---:|---:|---|
| `duygusal_tepki` | +0.05 | 0.38 | 0.38 | ⛔ **HAYIR** — fark gürültünün içinde |
| `yorumlama` | +0.38 | 0.43 | 0.38 | ⭐ **evet** — çapraz fark tabanı aşıyor |
| `kesif` | +0.19 | 0.19 | 0.08 | ⭐ **evet** — çapraz fark tabanı aşıyor |
| `mi_uyumu` | +0.05 | 0.19 | 0.08 | ⭐ **evet** — çapraz fark tabanı aşıyor |
| `grounding` | -0.29 | 0.29 | 0 | ⭐ **evet** — çapraz fark tabanı aşıyor |
| `anlasilirlik` | -0.86 | 1 | 0.75 | ⭐ **evet** — çapraz fark tabanı aşıyor |
| `dogallik` | -0.05 | 0.1 | 0.12 | ⛔ **HAYIR** — fark gürültünün içinde |

### ⛔⛔ Klinik güvenlik bayrağı

| judge | ateşleyen |
|---|---:|
| `claude-sonnet-subagent` | 0/42 |
| `agy:gemini-3.8-flash-high` | 0/42 |

⭐ T176 bu farkı korpus ölçeğinde ölçmüştü: Claude 85/7069 (%1,20), Gemini 0/430. ⛔ Bu bayrak `build.py`'nin **tek** otomatik klinik güvenlik kapısıdır (T121) ⇒ judge seçimi bir **güvenlik kararıdır**, yalnız bir ölçüm kararı değil.

## ⭐⭐⭐ C. Kapı bayrakları — bütün Claude yargıları

⛔⛔ `klinik_guvenlik_ihlali` `build.py`'nin **tek** otomatik klinik güvenlik kapısıdır (T121) ⇒ o satır bir ölçüm değil bir **eleme listesidir**.

| bayrak | `parti3` | `parti4` | `parti5` | `parti6` | `parti7` | `parti8` | **toplam** |
|---|---:|---:|---:|---:|---:|---:|---:|
| `grounding=2` | 9 | 10 | 2 | 1 | 7 | 22 | **51** |
| `klinik_guvenlik_ihlali` | 0 | 3 | 4 | 1 | 0 | 3 | **11** |
| `rol_siniri_ihlali` | 1 | 1 | 0 | 2 | 0 | 0 | **4** |
| `kurum_yordam_ihlali` | 1 | 2 | 3 | 1 | 3 | 3 | **13** |
| `bos_guvence` | 3 | 7 | 3 | 2 | 6 | 11 | **32** |
| `cevapsiz_soru` | 2 | 6 | 1 | 2 | 0 | 3 | **14** |
| _yargılanan_ | 60 | 59 | 60 | 58 | 57 | 118 | _412_ |

⛔ **`grounding` = 2 (uydurma) toplam 51/412 = %12.** En yüksek oran `v6-parti8`: 22/118 = **%19**.

⚠️ **`v6-parti8` bu oturumda HIZLANDIRILMIŞ üretilen partidir** (K260/K261: alt ajan taslak, benim yazma turum 6'dan 3'e indi). Oranını öteki partilerle karşılaştırmak hızlanmanın bedelini sormanın doğal yolu — ⛔⛔ **ama bu rapor o karşılaştırmayı KURMUYOR:** partiler aynı tohum dağılımıyla üretilmedi (T233: parti8 planı %50 yüksek riskli tohum çekti, havuz %38,7) ve uydurma oranının risk düzeyinden bağımsız olduğu gösterilmedi. ⇒ Ayrı ve tasarlanmış bir ölçüm gerekir.

⭐⭐⭐ **T238 burada SAYIYLA doğrulandı:** `grounding`'in kendiyle farkı **0** (judge hep aynı ayrıntıyı seçiyor) ama Gemini'yle farkı **0.29** ⇒ %100 tekrar-test uyumu güvenilirlik DEĞİL, **paylaşılan seçim eğilimi**. T238 bunu öngörmüştü.

## ⛔ Bu koşunun söylemedikleri

| | |
|---|---|
| ⛔⛔ **K97: bu sayılar Gemini sayılarıyla AYNI TABLOYA konmaz** | `v6-parti1` ve `v6-parti2` Gemini ile puanlı; B bölümü bir **köprü** kurar ama tabloları birleştirmez |
| ⛔⛔ **Öbekleme bir bağımsızlık kaybıdır** | Gemini her kaydı ayrı çağrıda gördü; bir subagent 16 kaydı aynı bağlamda gördü ⇒ sıra/çapa etkisi olabilir. A bölümü bu etkiyi tabana **dahil** ölçer, ondan **ayıramaz** |
| ⛔ **Üretici ile judge aynı aileden** | K45 öz-şişirmeyi ölçtü (+6/+11); körlük bunu azaltır, sıfırlamaz |
| ⚠️ **Judge kalite ölçmez, tarar** | K57'den beri geçerli |
