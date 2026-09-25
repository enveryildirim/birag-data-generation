# judge v4 — derin çok turlu ↔ tek turlu (korpus içi)

**Girdi:** `data/judged/v3-parti1.jsonl` (`4003bd2b9597…`) · `data/judged/v3-parti2-tam.jsonl` (`7b5294f5dbf4…`) · `data/judged/v3-parti3.jsonl` (`6cb1815c299e…`)  
**Betik:** `scripts/analiz/2026-09-14-judge-v4-derinlik.py` · **Tarih:** 2026-09-14 · **Kayıt:** 104

---

## Neden bu analiz

K79 tek partilik judge farklarının bulgu sayılamayacağını gösterdi ve korpuslar **arası** karşılaştırma zaten kontrollü değil (tohum, senaryo karışımı ve yazım oturumu birlikte değişiyor). Bu analiz **aynı korpusun içinde** kalıyor: talimat, yazar, gün ve tohum havuzu aynı, değişen tek şey kaydın derinliği.

> ⚠️ Yine de kontrollü değil: derin kayıtlar **zengin tohumlara** atandı (≥30 kelime), yani tohumlar da farklı. Fark derinliğe atfedilemez.

## 1. `anlasilirlik`

| Grup | n | ortalama | medyan | kusursuz (=5) |
|---|---:|---:|---:|---:|
| derin çok turlu (3-5 tur) | 14 | 4.36 | 4 | 6 (%43) |
| tek turlu | 72 | 4.14 | 4 | 30 (%42) |
| iki turlu | 18 | 4.56 | 5 | 12 |

Mann-Whitney (derin ↔ tek turlu): **p = 0.4452** — anlamlı fark yok; bu, grupların aynı olduğu anlamına gelmez, n = 14 ve n = 72 ile ayırt edilemiyor demektir.

## 2. Kusur bayrakları

| Kusur | derin | tek turlu | Fisher p |
|---|---:|---:|---:|
| kullanıcının kurmadığı mecaz | 3/14 (%21) | 14/72 (%19) | 1.000 |
| belirsiz gönderge | 6/14 (%43) | 28/72 (%39) | 0.774 |
| üst üste binen yan cümle | 0/14 (%0) | 17/72 (%24) | 0.062 |
| devrik / eksiltili cümle | 0/14 (%0) | 1/72 (%1) | 1.000 |
| soyut adlaştırma | 0/14 (%0) | 2/72 (%3) | 1.000 |

## 3. Güvenlik

| Ölçüm | derin | tek turlu |
|---|---:|---:|
| klinik güvenlik ihlali | 0/14 | 0/72 |
| rol sınırı ihlali | 0/14 | 0/72 |
| cevapsız soru | 0/14 | 0/72 |

> Bu bayrakların ayrım gücü hiç ölçülmedi (K61); yokluk kanıt değildir.

