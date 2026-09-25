# Eksen 1'in judge gerektirmeyen yarısı

**Betik:** `scripts/analiz/2026-09-18-eksen1-judgesiz.py` · **Tarih:** 2026-09-18  
**Set:** `evals/golden.dev.jsonl` (48 öğe) — mühürlü, değiştirilmedi

⛔⛔ **Eksen 1 bu projede bir METRİK olarak hiç koşulmadı.** Golden koşuları
diskte duruyor ama **ince ayar kollarının hiçbiri yargılanmamış**; yargılanmış
olan yalnız tabanlar, o da **v4/v5/v6** rubrikleriyle. Güncel rubrik **v9** ve
K137 gereği sürümler arası karşılaştırma geçersiz.

## 1. Üretim ve judge durumu

| kol | öğe | ⛔ yargılanmış | boş | kesilen | dejenere | ort. token |
|---|---:|---:|---:|---:|---:|---:|
| *ham model* (taban) | 48 | **48**/48 | 0 | 0 | 0 | 555 |
| 8 katman · v0.0.5 (eski tarama) | 48 | **0**/48 | 0 | 0 | 0 | 428 |
| ⭐ 8 katman · **v0.0.10** | 48 | **0**/48 | 0 | 0 | 0 | 373 |

## 2. ⭐ Otomatik iddialar (judge'sız)

| kural | *ham model* (taban) | 8 katman · v0.0.5 (eski tarama) | ⭐ 8 katman · **v0.0.10** |
|---|---:|---:|---:|
| `atif_yok` | 3/3 | 3/3 | 3/3 |
| `soru_sayisi_maks` | 40/42 | 41/42 | 39/42 |
| `uydurma_yok` | 4/4 | 4/4 | 4/4 |
| `uzunluk_maks` | 4/4 | 4/4 | 4/4 |
| `yasak_ifade_yok` | 7/7 | 7/7 | 7/7 |

⚠️ *«Otomatik iddialar geçti»* **kalite demek değildir**: bunlar biçim
kapıları (soru sayısı, uydurma yok, uzunluk). **Terapötik kalite** EPITOME ve MI
boyutlarında ölçülür — duygusal tepki, yorumlama, keşif, MI uyumu — ve o boyutlar
**yalnız judge ile** ölçülebilir.

## 3. ⛔⛔ Öteki yarı neden koşulmadı — ve maliyeti

| yol | durum | maliyet |
|---|---|---|
| `agy:gemini-3.8-flash-high` (yapılandırılmış judge) | ⛔ **kota tükendi** (K96) | — |
| Claude subagent | ⛔ **puanlayan olamaz** (K43/K45) | — |
| `qwen3.8:27b-mlx` (yerel, kotasız) | ⭐ çalışıyor | **164 sn/kayıt** (bu oturumda ölçüldü, v9) |

⭐ **Ölçülen maliyet:** 48 öğe × 164 sn = **2.2 saat/kol**.
⛔ Ve **en az iki kol** gerekir: v9 rubriğiyle yargılanmış bir TABAN yok, yani
taban + v0.0.10 = **4.4 saat**.

⛔⛔ **Üstelik bir soru daha açık:** K45 qwen↔gemini uyumunu **%1,4** ölçmüştü ama
o ölçüm **v1/v4 rubriğiyleydi**; v9'da uyum **ölçülmedi**. qwen'i metrik yapmak,
ölçülmemiş bir uyuma dayanmak demek. ➡️ *Bir judge'ı değiştirmek, ölçüt değiştirmektir;
yeni judge'ın eskisiyle uyumu ÖLÇÜLMEDEN sayıları aynı tabloda okunamaz (K97/K137).*

⭐ **Ama cevaplar sabit ve kayıtlı** ⇒ judge sonradan koşulabilir
(`--yeniden-judge`) ve üretim tekrarlanmaz. Bu raporun ölçtüğü şey kaybolmaz.

## ⛔ Bu raporun söylemedikleri

| | |
|---|---|
| ⛔⛔ **Bu bir Eksen 1 SONUCU DEĞİL** | Pareto'nun üçüncü adımı hâlâ açık; burada ölçülen şey biçim kapıları ve üretim sağlığı |
| ⛔ **Kollar farklı veriden** | `gd2-A-dar` v0.0.5 korpusundan; v0.0.10 ile aynı tabloda yalnız ÜRETİM SAĞLIĞI için okunabilir, kalite için değil |
| ⚠️ **164 sn/kayıt tek kayıttan** | n=1 sonda; ortalama değil, büyüklük sırası |
| ⚠️ Ortalama token düşüyor (555 → 373) | bu bir kalite işareti DEĞİL; kısalık hem iyi hem kötü olabilir ve hangisi olduğunu judge söyler |
