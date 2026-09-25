# Kapsama matrisi — eksen ↔ korpus

**Betik:** `scripts/analiz/2026-09-22-kapsama-matrisi.py` · **Tarih:** 2026-09-22  
**Korpus:** `datasets/v0.0.18` (1033 kayıt)  

⛔⛔ **Bu tablo koşudan ÖNCE bakılmak içindir.** Bir eksen korpus büyümesine cevap veremiyorsa, o eksende ölçülen fark bir **veri kararını değerlendiremez** — T248 bunu dört saatlik bir koşuyla öğrendi.

⚠️ **Eşleme benim yorumumdur**, ölçüm değil: hangi eval kategorisinin korpusta hangi alana karşılık geldiğine ben karar verdim. **Sayılar ölçülmüştür, eşleme tartışılabilir** — bu yüzden her satırda bakılan alan yazılıdır.

| eksen | eval kategorisi | korpusta karşılığı | kayıt | oran | eksen korpusa duyarlı mı |
|---|---|---|---:|---:|---|
| `safety_crisis` | kriz_acik · tibbi_aciliyet · rol_siniri_kriz | `is_crisis` | **0** | %0.0 | ⛔⛔ **HAYIR** — korpus bu davranışı hiç göstermiyor |
| `safety_crisis` | normallestirme | `is_crisis` | **0** | %0.0 | ⛔⛔ **HAYIR** — korpus bu davranışı hiç göstermiyor |
| `sycophancy` | eylem_onay · yanlis_inanc (onay yemi) | `is_negative` — kullanıcı istedi, asistan reddetti | **183** | %17.7 | ⭐ evet |
| `sycophancy` | sustain_talk | `talk_type = sustain` | **222** | %21.5 | ⭐ evet |
| `sycophancy` | insan_destegi (yönlendirme istendi) | `sinir_tipi = yonlendirme_istegi` | **33** | %3.2 | ⭐ evet |
| `sycophancy` | yanlis_red (gereksiz reddetme) | `sinir_tipi = yonlendirme_gereksiz` | **32** | %3.1 | ⭐ evet |
| `context_fidelity` | yeterli | `baglam_davranisi = cevap_var` | **89** | %8.6 | ⭐ evet |
| `context_fidelity` | yetersiz | `baglam_davranisi = cevap_yok` / `yetersiz` | **59** | %5.7 | ⭐ evet |
| `context_fidelity` | distractor | `baglam_davranisi = ilgisiz` | **40** | %3.9 | ⭐ evet |
| `context_fidelity` | celiskili | ⛔ korpusta karşılığı **yok** | **0** | %0.0 | ⛔⛔ **HAYIR** — korpus bu davranışı hiç göstermiyor |
| `forgetting_smoke` | matematik · mantik | yalın sayı / aritmetik cevap | **0** | %0.0 | ⛔⛔ **HAYIR** — korpus bu davranışı hiç göstermiyor |
| `forgetting_smoke` | genel_kultur | asistan turunda özel ad | **0** | %0.0 | ⛔⛔ **HAYIR** — korpus bu davranışı hiç göstermiyor |
| `forgetting_smoke` | kod · ceviri · ingilizce | `replay` dilimi (§9) | **18** | %1.7 | ⚠️ zayıf |
| `forgetting_smoke` | ozet · talimat | `ozet_var` (judge) — biçim talimatına uyma | **504** | %48.8 | ⭐ evet |

## Eksen düzeyinde hüküm

| eksen | eval ögesi | korpusta karşılığı olan kategori | hüküm |
|---|---:|---|---|
| `safety_crisis` | 20 | **0/2** | ⛔⛔⛔ **KÖR** — korpus büyümesi bu ekseni kıpırdatamaz (T248'in vakası) |
| `sycophancy` | 24 | **4/4** | ⭐ duyarlı |
| `context_fidelity` | 20 | **3/4** | ⚠️ **kısmi** — 1 kategori korpusta yok |
| `forgetting_smoke` | 30 | **2/4** | ⚠️ **kısmi** — 2 kategori korpusta yok |

## ⭐ Okunması

| | |
|---|---|
| ⛔⛔ `safety_crisis` **kör** | `is_crisis` = **0**; kriz dilimi uzman onayı bekliyor (Kural 3) ⇒ bu eksende ölçülen hiçbir fark bir **veri** kararını değerlendiremez. Eksen geçerli, **bu iş için yersiz** |
| ⚠️ `forgetting_smoke` **kısmi** | matematik/mantık ve genel kültür kategorilerinin korpusta karşılığı **yok** — T255'in kaybettiği ögeler tam bunlar. ⭐ Ama T257 gösterdi ki onarım **kipe özgü değil**: alan dışı sinyal genel olarak düzeltiyor |
| ⭐ `context_fidelity` **kısmi ama güçlü** | üç kategorinin üçü de korpusta var ve bu eksen ince ayarın **ölçülebilir kazanç verdiği tek eksen** (T254, +1,33). ⛔ Yalnız `celiskili` (çelişkili bağlam) korpusta **hiç yok** — açık bir boşluk |
| ⭐ `sycophancy` **duyarlı** | dört kategorinin dördü de korpusta temsil ediliyor. ⚠️ Ama ölçümde taban da kol da 22/24 verdi (T254) ⇒ eksen **doygun** olabilir |

## ⛔ Bu matrisin söylemedikleri

| | |
|---|---|
| ⛔⛔ **Eşleme ölçüm değil** | *«`sustain_talk` ↔ `talk_type=sustain`»* gibi karşılıklar benim yorumum; bir uzman başka eşleme kurabilir ve tablo değişir |
| ⛔ **Varlık ≠ yeterlilik** | bir kategorinin korpusta 40 kaydı olması onu ÖĞRETTİĞİ anlamına gelmez; yalnız **öğretebileceği** |
| ⛔ **Sinyal payı ölçülmedi** | T256: kayıt sayısı gradyan payıyla aynı şey değil. Bu tablo **kayıt** sayıyor ⇒ kısa cevaplı kategoriler burada büyük görünüp eğitimde küçük olabilir |
| ⚠️ **Tek korpus sürümü** | `v0.0.18`; deney sürümleri (`v0.0.19`/`v0.0.20`) dahil değil |
