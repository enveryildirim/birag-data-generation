# Geçmiş kol karşılaştırmaları, ölçülmüş eğitim gürültüsüne karşı

**Betik:** `scripts/analiz/2026-09-19-gecmis-kollar-bant.py` · **Tarih:** 2026-09-19  
**Taban:** aynı veri (`v0.0.14`), aynı bölme, yalnız `mlx.seed` 7/13/23 (T182)

## 1. ⭐⭐ Üç ölçüt, üç ayrı bant

| ölçüt | tohum 7 | 13 | 23 | **bant** |
|---|---:|---:|---:|---:|
| E2 otomatik geçen (/20) | 10 | 10 | 12 | **±2** |
| E2 dereceli yönlendirme (kriz öğeleri) | 18 | 17 | 14 | **±4** |
| E3 otomatik geçen (/30) | 29 | 27 | 28 | **±2** |

⛔⛔ **İki ölçüt karıştırılmaz.** T134/T135'in uçurum iddiaları **dereceli** puanla kurulmuştu ⇒ onlara ±4 uygulanır, ±2 değil.

⛔⛔⛔ **Kapsam bağımsızlığı VARSAYIM:** taban 8 katman kolunda ölçüldü; 16-32 katmanlı kolların gürültüsü daha büyük olabilir ⇒ bu **en iyimser bant**. Gerçek bant genişse, içinde kalan karşılaştırma sayısı **artar**.

## kapsam merdiveni (h · 09-17)

| kol | otomatik /20 | dereceli (kriz) |
|---|---:|---:|
| h1 · 8 kat q | 10 | 19 |
| h2 · 16 kat q | 7 | 1 |
| h3 · 24 kat q | 7 | 1 |
| h4 · 32 kat q | 7 | 1 |
| h5 · 16 kat q+o | 6 | 0 |
| h6 · 24 kat q+o | 8 | 3 |
| h7 · 24 kat q+o r16 | 11 | 7 |

İkili karşılaştırma **21** · bandın İÇİNDE kalan: otomatik **12/21** · dereceli **11/21**

⭐ Otomatik ölçütte bandı AŞAN (yorumlanabilir) çiftler: **h1 · 8 kat q↔h2 · 16 kat q** (3) · **h1 · 8 kat q↔h3 · 24 kat q** (3) · **h1 · 8 kat q↔h4 · 32 kat q** (3) · **h1 · 8 kat q↔h5 · 16 kat q+o** (4) · **h2 · 16 kat q↔h7 · 24 kat q+o r16** (4) · **h3 · 24 kat q↔h7 · 24 kat q+o r16** (4) · **h4 · 32 kat q↔h7 · 24 kat q+o r16** (4) · **h5 · 16 kat q+o↔h7 · 24 kat q+o r16** (5) · **h6 · 24 kat q+o↔h7 · 24 kat q+o r16** (3)

## uçurum (u · 09-17)

| kol | otomatik /20 | dereceli (kriz) |
|---|---:|---:|
| 8 katman | 10 | 19 |
| 10 katman | 9 | 14 |
| 12 katman | 10 | 11 |
| 13 katman | 8 | 2 |
| 14 katman | 8 | 2 |
| 16 katman | 7 | 1 |

İkili karşılaştırma **15** · bandın İÇİNDE kalan: otomatik **13/15** · dereceli **4/15**

⭐ Otomatik ölçütte bandı AŞAN (yorumlanabilir) çiftler: **8 katman↔16 katman** (3) · **12 katman↔16 katman** (3)

## katman 29 (p · 09-17)

| kol | otomatik /20 | dereceli (kriz) |
|---|---:|---:|
| 13 kat · 29 YOK | 8 | 7 |
| 12 kat · 29 VAR | 4 | 1 |

İkili karşılaştırma **1** · bandın İÇİNDE kalan: otomatik **0/1** · dereceli **0/1**

⭐ Otomatik ölçütte bandı AŞAN (yorumlanabilir) çiftler: **13 kat · 29 YOK↔12 kat · 29 VAR** (4)

## ilan seyreltme (ka · 09-17)

| kol | otomatik /20 | dereceli (kriz) |
|---|---:|---:|
| A · ilan seyreltilmiş | 9 | 14 |
| P · plasebo | 10 | 21 |

İkili karşılaştırma **1** · bandın İÇİNDE kalan: otomatik **1/1** · dereceli **0/1**

⛔⛔ **Bu ailede otomatik ölçütte bandı aşan TEK bir çift bile yok** ⇒ kollar arası hiçbir sıralama bu ölçütle okunamaz.

## epok/adım (g1 · 09-16)

| kol | otomatik /20 | dereceli (kriz) |
|---|---:|---:|
| v006 3 epok | 10 | 20 |
| v006 adım sabit | 9 | 19 |
| v005 referans | 8 | 21 |

İkili karşılaştırma **3** · bandın İÇİNDE kalan: otomatik **3/3** · dereceli **3/3**

⛔⛔ **Bu ailede otomatik ölçütte bandı aşan TEK bir çift bile yok** ⇒ kollar arası hiçbir sıralama bu ölçütle okunamaz.

## veri sürümü (09-18/19)

| kol | otomatik /20 | dereceli (kriz) |
|---|---:|---:|
| v0.0.8 (h1) | 10 | 19 |
| v0.0.10 | 10 | 22 |
| v0.0.14 | 10 | 18 |

İkili karşılaştırma **3** · bandın İÇİNDE kalan: otomatik **3/3** · dereceli **3/3**

⛔⛔ **Bu ailede otomatik ölçütte bandı aşan TEK bir çift bile yok** ⇒ kollar arası hiçbir sıralama bu ölçütle okunamaz.

## ⭐⭐⭐ Hangi kayıtlı iddia ayakta

| iddia | tür | ölçüt | fark | bant | hüküm |
|---|---|---|---:|---:|---|
| T135 · «uçurum 12 ile 14 katman arasında» | fark | dereceli | **9** | ±4 | ⭐ **ayakta** — bandı aşıyor |
| T134/T135 · «8 ↔ 16 arasında çöküş» | fark | dereceli | **18** | ±4 | ⭐ **ayakta** — bandı aşıyor |
| uçurum ara nokta · «10 ile 12 farklı» | fark | dereceli | **3** | ±4 | ⛔⛔ **gösterilemez** — bandın içinde |
| «h1 iki Pareto kapısını da geçen tek kol» | fark | otomatik | **1** | ±2 | ⛔⛔ **gösterilemez** — bandın içinde |
| h-ailesi · «h6 h5'ten iyi» | fark | otomatik | **2** | ±2 | ⛔⛔ **gösterilemez** — bandın içinde |
| T-katman29 · «29 atlamak 29'u tek başına almaktan iyi» | fark | dereceli | **6** | ±4 | ⭐ **ayakta** — bandı aşıyor |
| ka · «ilan seyreltmek plasebodan farklı» | fark | dereceli | **7** | ±4 | ⭐ **ayakta** — bandı aşıyor |
| g1 · «3 epok adım-sabitten iyi» | fark | otomatik | **1** | ±2 | ⛔⛔ **gösterilemez** — bandın içinde |
| g1 · «v006 v005'ten iyi» | fark | dereceli | **1** | ±4 | ⛔⛔ **gösterilemez** — bandın içinde |
| T181 · «v0.0.14 v0.0.10'a göre gerilemedi» | yokluk | otomatik | **0** | ±2 | ⭐ **ayakta** — ama tespit sınırı ±2: bu kadar gerileme var olabilir ve görünmezdi |

⭐⭐ **5/10 iddia ayakta kalıyor.** ➡️ *Bir ölçütün gürültü tabanı ölçülene kadar, ondan çıkarılan her sıralama bir iddia değil bir ihtimaldir — ve bu depoda o taban 09-19'a kadar ölçülmemişti.*

⛔⛔ **«Okunamaz» ≠ «yanlış».** Bandın içinde kalan bir fark yanlış olduğunu değil, bu ölçütle **gösterilemediğini** söyler. Ayırt etmek için ya ölçüt keskinleştirilmeli ya kol başına birkaç tohum koşulmalı (ortalama bandı √n ile daraltır).

⛔ **İddia metinleri elle eşleştirildi** — hangi defter maddesinin hangi çifte dayandığı otomatik çıkarılmadı (Kural 7'nin zayıf halkası).
