# v6-parti5 — birleştirme ve kapı denetimi

**Betik:** `scripts/analiz/2026-09-20-v6-parti2-birlestir.py` · **Tarih:** 2026-09-20

## `v6-parti5`

| | |
|---|---:|
| plan satırı | 60 |
| ⭐ üretilen kayıt | **60** |
| ⛔ üretilmeyen | — |
| ⭐ `run_checks` geçen | **60/60** |
| tohum eşleşmesi | 60/60 |

## Bağlam sınıfı dağılımı (§7a)

⛔ Parti2'nin ilk 13 bağlam kaydının 13'ü `cevap_var` çıktı: T197'yi (*«soruyu pasaja uyacak şekilde tasarla»*) tek biçimde uygulamışım. ⭐ Bütünde hedefe yakın durulması iki partinin TERS yönde sapmasının sonucudur, tasarımın değil.

| sınıf | v0.0.14 | v6-parti5 | **bütün** | hedef |
|---|---:|---:|---:|---:|
| `cevap_var` | 51 (%50) | 3 (%20) | **54 (%46)** | %50 |
| `cevap_yok` | 25 (%24) | 4 (%27) | **29 (%25)** | %25 |
| `izin_iste` | 14 (%14) | 3 (%20) | **17 (%14)** | %12 |
| `ilgisiz` | 8 (%8) | 5 (%33) | **13 (%11)** | %12 |

⚠️ v0.0.14'te ayrıca sınıf dışı 5 kayıt var (`cevapla`, `yetersiz`); toplam sütununa dahil değiller.

## §5a″ sapmaları ve elle onaylar

| | |
|---|---:|
| ızgaradan sapan kayıt | **16** / 60 |
| — v6-parti5 | 16 |
| elle onaylı `ozerklik_vurgusu` | 8 |
| elle onaylı `is_negative` | 9 |

⭐ Sapan satırlar: parti5#1, parti5#2, parti5#7, parti5#15, parti5#17, parti5#18, parti5#26, parti5#33, parti5#39, parti5#41, parti5#45, parti5#48, parti5#50, parti5#53, parti5#57, parti5#59

## ⭐⭐ Desen kapsaması — partiler arası

Bir kaydın özerklik/red taşıdığı iki yoldan biriyle saptanıyor: **sözlük deseni** ya da **elle onay**. Desenin tek başına yakaladığı oran:

| | v6-parti5 |
|---|---:|
| özerklik | 4/12 (%33) |
| red | 3/12 (%25) |

⭐ Kapsama bir **sözcük** ölçüsü, şablon kapısı bir **dizi** ölçüsü. Aynı fiil farklı cümlelerde geçerse kapsama yükselir, şablon yükselmez. Red cümlelerinin benzersizliği:

| | v6-parti5 |
|---|---:|
| benzersiz red cümlesi / toplam | 9/9 |

➡️ *Sözlük deseni yapıyı değil, KALIBA UYMAYI ölçüyor; şablonu azaltmak ölçülen oranı düşürür ve ölçüm bunu bir gerileme gibi gösterir.*

⛔ Bu, T193'ün ölçtüğü oranı da niteler: o oran bir **alt sınır** değil, **kalıp bağımlı** bir sayıdır.

## ⛔ Bu raporun söylemedikleri

| | |
|---|---|
| ⛔⛔ **Bu bir KALİTE raporu değil** | kapılar biçim ve dayanak denetler; terapötik kaliteyi judge ölçer ve v6-parti5 bu raporda yargılanmadı |
| ⭐ **Üretilmeyen plan satırı yok** | bu raporun kapsadığı partilerde plan satırlarının tamamı üretildi |
| ⚠️ **Elle onay bir İNSAN kararıdır** | desen görmedi, ben onayladım; onay cümlesi betikte yazılı ve kayıtta `gen_meta.elle_onay`ta duruyor |
