# Hücre düzeyi kapsama — marjinaller kapandıktan sonra

**Betik:** `scripts/analiz/2026-09-21-hucre-kapsama-envanteri.py` · **Tarih:** 2026-09-21  
**Havuz:** **2240** tohum · üretilmiş **1029** · asgari havuz sayısı **20**  
**Bakılan hücre:** 362 (eksen çifti: 21)

⛔⛔ **Marjinal ölçüt tükendi.** Beş parti sonra tek eksen değerlerinin hiçbirinde |fark| ≥ 3 yok (en büyüğü +2,7) ⇒ ufuk kuralı hedef üretmiyor. Bu rapor, envanterin kendi son şerhini uyguluyor: *«eksenler bağımsız sayıldı; birlikte dağılım bakılmadı»*.

⭐ Ölçü aynı (`havuz% − set%`), birim farklı: tek değer yerine iki eksenin kesişimi. Ufuk kuralı (T211) değişmiyor.

## 1. Eşiği aşan hücreler — eksik **0**, fazla **3**

| hücre | sette | havuz | fark | havuz tohum | set tohum |
|---|---:|---:|---:|---:|---:|
| `motivasyon_evresi=dusunme&profil=mavi_yakali` | %10.11 | %5.8 | -4.30 | 130 | 104 |
| `evre=tolerans&profil=mavi_yakali` | %9.14 | %5.8 | -3.33 | 130 | 94 |
| `risk_seviyesi=yuksek&profil=mavi_yakali` | %8.45 | %5.36 | -3.10 | 120 | 87 |
| `senaryo=rol_siniri&stres_tipi=yok` | %18.46 | %21.38 | +2.92 | 479 | 190 |
| `senaryo=belirsiz&motivasyon_evresi=dusunme` | %22.74 | %20.04 | -2.70 | 449 | 234 |
| `risk_seviyesi=yuksek&siddet_seviyesi=orta` | %19.44 | %16.74 | -2.70 | 375 | 200 |
| `risk_seviyesi=orta&stres_tipi=yok` | %40.52 | %43.12 | +2.60 | 966 | 417 |
| `risk_seviyesi=yuksek&motivasyon_evresi=dusunme` | %27.02 | %24.55 | -2.46 | 550 | 278 |
| `profil=beyaz_yakali&siddet_seviyesi=orta` | %22.06 | %19.64 | -2.42 | 440 | 227 |
| `senaryo=rol_siniri&motivasyon_evresi=dusunme` | %11.66 | %14.06 | +2.40 | 315 | 120 |
| `senaryo=belirsiz&evre=tolerans` | %18.85 | %16.47 | -2.38 | 369 | 194 |
| `risk_seviyesi=orta&siddet_seviyesi=hafif` | %7.48 | %9.82 | +2.34 | 220 | 77 |
| `motivasyon_evresi=on_dusunme&profil=beyaz_yakali` | %4.47 | %2.23 | -2.24 | 50 | 46 |
| `risk_seviyesi=orta&profil=lise_ergeni` | %6.03 | %8.26 | +2.23 | 185 | 62 |
| `motivasyon_evresi=on_dusunme&siddet_seviyesi=orta` | %12.93 | %10.71 | -2.21 | 240 | 133 |
| `profil=mavi_yakali&siddet_seviyesi=orta` | %8.45 | %6.25 | -2.20 | 140 | 87 |
| `motivasyon_evresi=dusunme&stres_tipi=yok` | %44.31 | %46.43 | +2.11 | 1040 | 456 |
| `evre=inkar&profil=beyaz_yakali` | %3.89 | %1.79 | -2.10 | 40 | 40 |
| `risk_seviyesi=yuksek&evre=tolerans` | %19.05 | %16.96 | -2.08 | 380 | 196 |
| `evre=tolerans&siddet_seviyesi=orta` | %40.23 | %38.17 | -2.06 | 855 | 414 |
| `profil=mavi_yakali&stres_tipi=yok` | %10.01 | %8.04 | -1.97 | 180 | 103 |
| `senaryo=rol_siniri&profil=universite_ogrencisi` | %0.58 | %2.54 | +1.96 | 57 | 6 |
| `motivasyon_evresi=dusunme&profil=ev_kadini` | %3.4 | %5.36 | +1.96 | 120 | 35 |
| `evre=inkar&siddet_seviyesi=orta` | %9.04 | %7.14 | -1.90 | 160 | 93 |
| `risk_seviyesi=orta&motivasyon_evresi=dusunme` | %34.5 | %36.38 | +1.88 | 815 | 355 |
| `senaryo=belirsiz&risk_seviyesi=yuksek` | %10.3 | %8.48 | -1.82 | 190 | 106 |
| `senaryo=belirsiz&siddet_seviyesi=orta` | %15.84 | %14.02 | -1.82 | 314 | 163 |
| `evre=tolerans&profil=kronik_issiz` | %4.47 | %2.68 | -1.79 | 60 | 46 |
| `senaryo=rol_siniri&siddet_seviyesi=agir` | %5.83 | %7.59 | +1.76 | 170 | 60 |
| `senaryo=belirsiz&profil=mavi_yakali` | %3.98 | %2.23 | -1.75 | 50 | 41 |
| `profil=kronik_issiz&siddet_seviyesi=orta` | %5.73 | %4.02 | -1.72 | 90 | 59 |
| `evre=tolerans&profil=ev_kadini` | %3.69 | %5.36 | +1.66 | 120 | 38 |
| `senaryo=rol_siniri&risk_seviyesi=orta` | %5.54 | %7.19 | +1.65 | 161 | 57 |
| `evre=nuksetme&stres_tipi=yok` | %7.29 | %8.93 | +1.64 | 200 | 75 |
| `senaryo=ambivalans&motivasyon_evresi=on_dusunme` | %7.87 | %6.25 | -1.62 | 140 | 81 |
| `motivasyon_evresi=dusunme&stres_tipi=yalnizlik` | %1.55 | %3.12 | +1.57 | 70 | 16 |
| `motivasyon_evresi=dusunme&evre=tolerans` | %40.62 | %39.06 | -1.56 | 875 | 418 |
| `senaryo=belirsiz&stres_tipi=yalnizlik` | %1.94 | %3.48 | +1.54 | 78 | 20 |
| `evre=tolerans&stres_tipi=yalnizlik` | %1.94 | %3.48 | +1.54 | 78 | 20 |
| `evre=dibe_vurma&profil=mavi_yakali` | %3.3 | %1.79 | -1.52 | 40 | 34 |

## ⛔ Bu envanterin söylemedikleri

| | |
|---|---|
| ⛔⛔ **Asgari 20 tohum SEÇİMDİR** | türetilmedi; altındaki hücrelerde yüzde farkı gürültüdür ama eşiğin nerede olduğu ölçülmedi |
| ⛔⛔ **İkili bakıldı, üçlü bakılmadı** | aynı itiraz bir üst düzeyde aynen geçerli; nerede duracağı bir seçim ve burada ikide durdu |
| ⛔⛔ **Hücre hedeflemek marjinali BOZABİLİR** | bir hücreyi doldurmak iki marjinali birden oynatır; planın bunu ölçmesi gerekir |
| ⛔⛔ **Kapsama ≠ kalite** | envanterin şerhi burada da geçerli; hücre payını havuza eşitlemek o hücrede iyi kayıt üretileceğini göstermez |
| ⛔ **Havuzun kendisi bir tasarım ürünü** | *«set havuzu yansıtmalı»* varsayımı hücre düzeyinde de kanıtlanmadı |
