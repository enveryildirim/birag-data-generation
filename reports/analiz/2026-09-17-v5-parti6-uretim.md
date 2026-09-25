# v5-parti6 üretildi — 60 kayıt, altı eksen +0.0, ALTI güvenlik sapması

*2026-09-17 · `data/candidates/v5-parti6.jsonl` SHA256 `b8b351bfbada9e2b` · 60 kayıt*

## 1. Izgara

Altı eksen **+0.0**. Tek sapma ekseni `sinir_tipi` ve orada altı kayıt ilan
edilmiş sapma taşıyor: `#17` `#27` `#34` `#42` `#43` `#52`.

⛔ §8b dilimi **%15 → %21.7**. Kota tutmadı çünkü kota ÇEKİLENİ sayıyor,
korpusun gerçek payı ise çekilen + güvenlik.

## 2. ⛔⛔ Asıl bulgu — ölçütsüz ilan (T114)

| parti | `tur` kotası | güvenlik sapması |
|---|---|---:|
| v5-parti3 | tutun 22 · alkol 17 · kumar 11 · receteli_ilac 7 · dijital 3 | **0** |
| v5-parti4 | **aynı** | 2 |
| v5-parti5 | **aynı** | 1 |
| v5-parti6 | **aynı** | **6** |

Dört partinin eksen bileşimi birebir aynı. 0 ile 6 arasındaki fark ya tohum
şansı ya da **üreticinin eşiğinin kayması** — ve ölçütsüz bir defter ikisini
ayırt edemez. ⇒ `uretim-v5` **§5a″** yazıldı: dört maddelik sapma ölçütü.

⛔ Ölçüt parti6'nın vakalarından türetildi; parti6'nın ona uyması kanıt değil.
⛔ parti3–parti5 ölçüte göre **yeniden okunmadı** — borç.

## 3. Kapılar

| kapı | sonuç |
|---|---|
| `src/checks.py` | **60/60** ✅ |
| zaman/kaynak atfı | **0 bayrak** (blok bazında 2 → 0) |
| alıntı birebirlik (T113) | **0 bayrak** (blok bazında 3+4+2 → 0) |
| ızgara↔tohum | **60/60 tam uyum, 0 uydurma** |
| beyanla kriz tohumu | SERT 0 · PERSONA 0 ✅ |
| K18 · K31 | ihlal yok ✅ |
| thinking:completion | ortanca **1.48x**, maks **3.78x** |

⭐ Yeni alıntı kapısı ilk kez üretim sırasında çalıştı ve **9 kusur** yakaladı:
biri doğrudan T104'tü (`#44`, kırpılan «dün gece» cevapta kalmış), ikisi
*hanım→eş* yeniden adlandırması, kalanı kelime eleyen alıntı.

## ⛔ Bu raporun söylemedikleri

- Judge geçmedi; hiçbir sayı kalite ölçümü değil.
- v5'in üç bahsi hâlâ ölçülmedi (v0.0.8 eğitimi bekliyor).
- `thinking` alanının tırnaklı ögeleri okunmadı.
- `#54` (parti3) `kurum_yordam_ihlali` hâlâ veri setinde.
