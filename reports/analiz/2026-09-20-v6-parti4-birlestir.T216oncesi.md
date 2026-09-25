# v6-parti1 + v6-parti2 + v6-parti3 + v6-parti4 — birleştirme ve kapı denetimi

**Betik:** `scripts/analiz/2026-09-20-v6-parti2-birlestir.py` · **Tarih:** 2026-09-20

## `v6-parti1`

| | |
|---|---:|
| plan satırı | 60 |
| ⭐ üretilen kayıt | **59** |
| ⛔ üretilmeyen | [29] |
| ⭐ `run_checks` geçen | **59/59** |
| tohum eşleşmesi | 59/59 |

## `v6-parti2`

| | |
|---|---:|
| plan satırı | 60 |
| ⭐ üretilen kayıt | **59** |
| ⛔ üretilmeyen | [54] |
| ⭐ `run_checks` geçen | **59/59** |
| tohum eşleşmesi | 59/59 |

## `v6-parti3`

| | |
|---|---:|
| plan satırı | 60 |
| ⭐ üretilen kayıt | **60** |
| ⛔ üretilmeyen | — |
| ⭐ `run_checks` geçen | **60/60** |
| tohum eşleşmesi | 60/60 |

## `v6-parti4`

| | |
|---|---:|
| plan satırı | 60 |
| ⭐ üretilen kayıt | **59** |
| ⛔ üretilmeyen | [16] |
| ⭐ `run_checks` geçen | **59/59** |
| tohum eşleşmesi | 59/59 |

## Bağlam sınıfı dağılımı (§7a)

⛔ Parti2'nin ilk 13 bağlam kaydının 13'ü `cevap_var` çıktı: T197'yi (*«soruyu pasaja uyacak şekilde tasarla»*) tek biçimde uygulamışım. ⭐ Bütünde hedefe yakın durulması iki partinin TERS yönde sapmasının sonucudur, tasarımın değil.

| sınıf | v0.0.14 | v6-parti1 | v6-parti2 | v6-parti3 | v6-parti4 | **bütün** | hedef |
|---|---:|---:|---:|---:|---:|---:|---:|
| `cevap_var` | 51 (%50) | 5 (%33) | 13 (%87) | 3 (%20) | 3 (%21) | **75 (%46)** | %50 |
| `cevap_yok` | 25 (%24) | 6 (%40) | 1 (%7) | 4 (%27) | 4 (%29) | **40 (%25)** | %25 |
| `izin_iste` | 14 (%14) | 1 (%7) | 0 (%0) | 3 (%20) | 3 (%21) | **21 (%13)** | %12 |
| `ilgisiz` | 8 (%8) | 3 (%20) | 1 (%7) | 5 (%33) | 4 (%29) | **21 (%13)** | %12 |

⚠️ v0.0.14'te ayrıca sınıf dışı 5 kayıt var (`cevapla`, `yetersiz`); toplam sütununa dahil değiller.

## §5a″ sapmaları ve elle onaylar

| | |
|---|---:|
| ızgaradan sapan kayıt | **35** / 237 |
| — v6-parti1 | 4 |
| — v6-parti2 | 7 |
| — v6-parti3 | 13 |
| — v6-parti4 | 11 |
| elle onaylı `ozerklik_vurgusu` | 34 |
| elle onaylı `is_negative` | 23 |

⭐ Sapan satırlar: parti1#11, parti1#48, parti1#51, parti1#59, parti2#1, parti2#15, parti2#28, parti2#48, parti2#52, parti2#59, parti2#60, parti3#6, parti3#9, parti3#12, parti3#17, parti3#19, parti3#21, parti3#22, parti3#23, parti3#25, parti3#29, parti3#30, parti3#39, parti3#46, parti4#10, parti4#19, parti4#22, parti4#29, parti4#32, parti4#33, parti4#38, parti4#46, parti4#53, parti4#57, parti4#60

## ⭐⭐ Desen kapsaması — partiler arası

Bir kaydın özerklik/red taşıdığı iki yoldan biriyle saptanıyor: **sözlük deseni** ya da **elle onay**. Desenin tek başına yakaladığı oran:

| | v6-parti1 | v6-parti2 | v6-parti3 | v6-parti4 |
|---|---:|---:|---:|---:|
| özerklik | 14/16 (%88) | 2/12 (%17) | 2/13 (%15) | 1/12 (%8) |
| red | 8/12 (%67) | 4/11 (%36) | 10/15 (%67) | 2/9 (%22) |

⭐ Kapsama bir **sözcük** ölçüsü, şablon kapısı bir **dizi** ölçüsü. Aynı fiil farklı cümlelerde geçerse kapsama yükselir, şablon yükselmez. Red cümlelerinin benzersizliği:

| | v6-parti1 | v6-parti2 | v6-parti3 | v6-parti4 |
|---|---:|---:|---:|---:|
| benzersiz red cümlesi / toplam | 16/16 | 5/5 | 20/20 | 18/18 |

⭐⭐ **Parti2'de aynı desen çok daha azını görüyor.** İki partiyi aynı kişi aynı ölçütle yazdı; değişen tek şey, parti2'de özerklik ve red **biçimlerinin bilerek çeşitlendirilmesiydi**.

➡️ *Sözlük deseni yapıyı değil, KALIBA UYMAYI ölçüyor; şablonu azaltmak ölçülen oranı düşürür ve ölçüm bunu bir gerileme gibi gösterir.*

⛔ Bu, T193'ün ölçtüğü oranı da niteler: o oran bir **alt sınır** değil, **kalıp bağımlı** bir sayıdır.

## ⛔ Bu raporun söylemedikleri

| | |
|---|---|
| ⛔⛔ **Bu bir KALİTE raporu değil** | kapılar biçim ve dayanak denetler; terapötik kaliteyi judge ölçer ve parti2 henüz yargılanmadı |
| ⛔ **`#54` üretilmedi** | çıplak *«İntihar düşüncesi»* beyanı — `gd-021` uzman kaleminde; parti 59'da kapandı |
| ⚠️ **Elle onay bir İNSAN kararıdır** | desen görmedi, ben onayladım; onay cümlesi betikte yazılı ve kayıtta `gen_meta.elle_onay`ta duruyor |
