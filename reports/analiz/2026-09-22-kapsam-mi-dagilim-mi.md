# Unutmayı ne sürüyor — LoRA kapsamı mı, dağılım mı?

**Betik:** `scripts/analiz/2026-09-22-kapsam-mi-dagilim-mi.py` · **Tarih:** 2026-09-22  
**Ölçü:** `forgetting_smoke` otomatik sayım (tavan 30) · taban **28/30**  

⭐ **Yeni eğitim gerekmedi.** Kapsam merdiveni `v0.0.14` üzerinde zaten koşulmuştu ve `runs/` hiç silinmiyor (Kural 7).

## A. Dağılım değişir, KAPSAM SABİT

Üçünde de: 8 katman · q+o (16 modül) · rank 8 · scale 20 · LR 1e-5.

| kol | veri | adım | unutma | tohum |
|---|---|---:|---|---:|
| `z-h9` | v0.0.14 · 571 kayıt | 1368 | **27.62** ± 0.37 | 8 |
| `d1` | v0.0.18 · 1033 kayıt | 2478 | **26.75** ± 0.73 | 8 |
| `e2` | v0.0.20 · 1394 (%5 tazeleme) | 3345 | **28.00** ± 0.00 | 3 |

`d1` − `z-h9` = **-0.88 ± 0.82** (okunabilir) · `e2` − `d1` = **+1.25 ± 0.73** (⭐ **okunabilir**)

⇒ **Yayılım: 1.25 puan.**

⛔⛔ **Adım sayısı açıklamıyor:** 1368 → 27,62 · 2478 → 26,75 · 3345 → **28,00**. Eğer daha çok adım daha çok unutma demek olsaydı `e2` en kötü olurdu; **en iyisi o**. ⇒ Dağılım, adım sayısından bağımsız olarak belirleyici.

## B. Kapsam değişir, DAĞILIM SABİT (`v0.0.14`)

| kol | kapsam | modül | unutma | tohum |
|---|---|---:|---|---:|
| `h1` | 8 kat · q | **8** | 28.00 ± 1.15 | 3 |
| `h9` | 8 kat · q+o | **16** | 27.62 ± 0.37 | 8 |
| `h2` | 16 kat · q | **16** | 28.00 ± 0.00 | 3 |
| `h3` | 24 kat · q | **24** | 27.67 ± 0.67 | 3 |
| `h5` | 16 kat · q+o | **32** | 26.00 ± 1.15 | 3 |
| `h4` | 32 kat · q | **32** | 27.33 ± 1.33 | 3 |
| `h6` | 24 kat · q+o | **48** | 27.67 ± 1.33 | 3 |
| `—` | 24 kat · q+o · r16 | **48** | 27.33 ± 0.67 | 3 |
| `h8` | 24 kat · q+o · r16 s10 | **48** | 27.67 ± 0.67 | 3 |

Modül sayısı **8 → 48** (6 kat) · unutma yayılımı **2.00 puan** · korelasyon **r = -0.284** (n=9 kol).

⇒ ⛔ **Kapsamı altı kat büyütmek unutmayı anlamlı biçimde değiştirmiyor** ve işaret bile **ters** (daha geniş kapsam → biraz daha AZ unutma).

## ⭐⭐⭐ Sonuç

⛔⛔ **Ham yayılımları karşılaştırmak YANILTIR** — kapsam kollarının yayılımı (2.00) dağılımınkinden (1.25) **büyük**. Ayıran şey yayılımın büyüklüğü değil, **DÜZENİ**:

| | düzen var mı | kanıt |
|---|---|---|
| **dağılım** (kapsam sabit) | ⭐ **evet** | farklar sıralı ve `e2`−`d1` = +1.25 ± 0.73 **okunabilir**; tazeleme unutmayı tabana geri getiriyor |
| **kapsam** (dağılım sabit) | ⛔ **hayır** | modül 8→48 (6 kat) ama r = **-0.284** ve işaret ters; yayılım **dağınık**, sıralı değil — en düşük kol (`h5`, 26,00) **orta** kapsamda, en yüksek kollar hem en dar (`h1`) hem en geniş (`h2`) uçta |

➡️⭐⭐⭐ *Unutmayı **DAĞILIM** sürüyor, LoRA kapsamı değil. Dar dağılımlı bir korpusla eğitmek genel yeteneği bozuyor; kapsamı daraltmak ya da genişletmek bunu düzeltmiyor, ama dağılıma yeterince alan dışı sinyal katmak **tamamen geri alıyor** (T257).*

⇒ T255'nin bıraktığı iki aday sebepten **kapsam elendi**.

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔⛔ **B bölümü `v0.0.14` üzerinde** | dağılım orada da dardır; *«kapsam GENİŞ dağılımda da etkisiz»* denemez. Söylenebilen: **dar dağılımda** kapsam unutmayı sürmüyor |
| ⛔ **A'da iki şey birlikte değişti** | `z-h9` → `d1` geçişinde hem korpus büyüdü hem adım arttı. ⭐ Ama `e2` bu karışıklığı çözüyor: en çok adımı o aldı ve **en az unuttu** |
| ⛔⛔ **B'nin GÜCÜ DÜŞÜK** | kol başına 1-3 tohum ve yayılım 2.00 puan ⇒ *«kapsam etkisi YOK»* değil, **«sıralı bir kapsam etkisi SAPTANMADI»** denir. `h5`'in 26,00'ı açıklanamıyor ve kapsamla açıklanamayan bir oynaklığın varlığını gösteriyor |
| ⛔ **K174/K175 ile çelişmiyor** | orada ölçülen **güvenlik davranışı** ve kapsam onu 13 katmanda çökertiyor. Burada ölçülen **genel yetenek** ⇒ iki ayrı eksen, iki ayrı davranış |
| ⚠️ **Tek eksen** | `forgetting_smoke` 30 öge; başka unutma ölçütlerinde aynı sonucun çıkacağı gösterilmedi |
