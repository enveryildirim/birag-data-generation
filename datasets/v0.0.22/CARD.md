# BıRAG veri kümesi — v0.0.22

**Tarih:** 2026-09-22 · **Girdi:** `data/judged/v0.0.22.jsonl` SHA256-16 `fc1c117d3be48982`
**Çıktı:** `train.jsonl` SHA256-16 `6fcb6b1e16290575`
**Kayıt:** **1058** / 1132 (elenen 74)

⭐ **Ana hattın devamıdır.** `v0.0.21` fiilen ince ayar edilen sürümdü; `v0.0.19`/`v0.0.20` **deney kollarıdır** (aritmetik tazeleme) ve korpusun ilerleyişi değildir.

---

## 1. v0.0.21'den farkı: §7a″ `celiskili` sınıfı

| | |
|---|---:|
| v0.0.21 | 1045 |
| + `celiskili` | **13** |
| − düşen | **0** |
| ⭐ **v0.0.22** | **1058** |

⭐ **Yeni olan tek şey bu sınıf.** T259'un kapsama matrisi `context_fidelity` eval'inin dört kategorisinden **`celiskili`**'nin korpusta **sıfır kaydı** olduğunu bulmuştu — üstelik o eksen ince ayarın ölçülebilir kazanç verdiği **tek** eksendi (T254, +1,33).

⛔⛔ **Ama bu sınıf kendi kusurunu da üretti ve kartta yazılı olmalı:** ilk 12 kaydın **3'ü** (%25) kullanıcının söylemediği bir ayrıntıyı ona atfediyordu — yani sınıfın **karşı çıkmak için tasarlandığı** kusuru (T265). Üçü de onarıldı ve **yeniden yargılandı**; bu sürümdeki 12 kaydın tamamı `grounding = 5`. ⇒ *Bu bir «uydurmasız sınıf» değil, **uydurması bulunup elle onarılmış** bir sınıftır.*

⛔ **Kota tutturulamadı:** §7a″ `celiskili` payını ~%10 hedefliyor; bu sürümde bağlamlı 247 kaydın **%10.1**'i. Sınıfın ince ayara etkisi bu sürümle **ölçülebilir olmayabilir**.

## 2. Bileşim

| dilim | kayıt |
|---|---:|
| `terapotik_tek_tur` | 426 |
| `terapotik_cok_tur` | 361 |
| `rag_tek_tur` | 209 |
| `rag_cok_tur` | 44 |
| `replay` | 18 |

| bant (`gen_meta.bicim`) | kayıt |
|---|---:|
| `kisa` | 377 |
| `uzun` | 373 |
| `orta` | 308 |

⛔ Bant **türetmedir, beyan değil** (T263): `bicim` beyan edilmiş üçüncü alan olarak sürüklenmişti ve birleştirme anında yeniden türetildi.

| bağlam sınıfı | kayıt |
|---|---:|
| `— (bağlamsız)` | 811 |
| `cevap_var` | 89 |
| `cevap_yok` | 57 |
| `ilgisiz` | 40 |
| `izin_iste` | 31 |
| `celiskili` | 25 |
| `cevapla` | 3 |
| `yetersiz` | 2 |

## 3. ⛔⛔ Judge karışımı (K97)

| judge | kayıt |
|---|---:|
| `claude-sonnet-subagent` | 894 |
| `agy:gemini-3.8-flash-high` | 146 |
| `replay` | 18 |

⛔⛔ **Bu korpus TEK BİR judge ile puanlanmamıştır.** K97: iki judge'ın sayıları aynı tabloya konmaz; buradaki tablo bir **dağılım beyanıdır**, bir karşılaştırma değil.

## 4. Eleme

| sebep | kayıt |
|---|---:|
| `judge_uydurma` | 56 |
| `judge_safety_violation` | 14 |
| `guvenlik_karantinasi` | 4 |

⛔ Elenenler **silinmedi** (Kural 7); girdi dosyasında duruyorlar ve SHA256'sı yukarıda yazılı.

## 5. ⭐ Bu sürümde ilk kez koşan kapılar

| kapı | ne yapar |
|---|---|
| `bant_ok` | `gen_meta.bicim` beyanını türetmeye karşı sınar (T263) |
| `celiskili_ok` | `celiskili` beyan eden cevap çelişkiyi **adlandırmalı** ve **iki pasaja birden** atıf yapmalı (T262) |
| `yansitma_ok` | kullanıcıya **alıntıyla** atfedilen söz, kullanıcı turlarında bulunmalı (T266) |

⭐ `_checks` atıldı ve girdinin tamamında bugünkü `run_checks` yeniden koştu ⇒ korpus **tek denetim sürümüyle** geçildi (T240). Eskiden geçip şimdi düşen kayıt: **0**.

⛔⛔ **`yansitma_ok` DAR bir kapıdır:** 1176 etiketli kayıtta kesinliği **%100** ama duyarlılığı **%1** — yalnız alıntıyla atfa bakar, alıntısız parafraz uydurmasını **görmez** (T266). Kapıdan geçmek temiz olmak değildir.

## ⛔ Bu kartın söylemedikleri

| | |
|---|---|
| ⛔⛔ **`grounding` alt sınırdır** | tek-ayrıntı sondası (T238): judge'ın adlandırdığı ayrıntı dayanaklıysa 5 verir ve aynı cevaptaki başka bir uydurmayı **görmez** |
| ⛔⛔ **`celiskili` kayıtlarını ben yazdım, onardım ve yargısını ben okudum** | K30/K260; bağımsız anotatör hâlâ borç |
| ⛔ **Sınıf DAR öğretiliyor** | 12 pasaj çiftinin tamamı **idari/usule ilişkin** çelişki (gün, ücret, yaş, belge, süre, sıklık); klinik çelişki **yok** ve bu bilinçli (Kural 3) |
| ⛔ **Bu sürüm ÖLÇÜLMEDİ** | ince ayar koşulmadı; buradaki hiçbir sayı model başarımı hakkında bir şey söylemez |
| ⚠️ **Yargı turları karışık** | `celiskili`'nin 9 kaydı ilk yargıdan, 3 kaydı onarım sonrası yeniden yargıdan |
