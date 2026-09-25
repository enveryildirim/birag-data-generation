# v6-parti3 — birleştirme ve kapı denetimi

**Betik:** `scripts/analiz/2026-09-20-v6-parti2-birlestir.py` · **Tarih:** 2026-09-20

## `v6-parti3`

| | |
|---|---:|
| plan satırı | 60 |
| ⭐ üretilen kayıt | **60** |
| ⛔ üretilmeyen | — |
| ⭐ `run_checks` geçen | **60/60** |
| tohum eşleşmesi | 60/60 |

## Bağlam sınıfı dağılımı (§7a)

⛔ Parti2'nin ilk 13 bağlam kaydının 13'ü `cevap_var` çıktı: T197'yi (*«soruyu pasaja uyacak şekilde tasarla»*) tek biçimde uygulamışım. ⭐ Bütünde hedefe yakın durulması iki partinin TERS yönde sapmasının sonucudur, tasarımın değil.

| sınıf | v0.0.14 | v6-parti3 | **bütün** | hedef |
|---|---:|---:|---:|---:|
| `cevap_var` | 51 (%50) | 3 (%20) | **54 (%46)** | %50 |
| `cevap_yok` | 25 (%24) | 4 (%27) | **29 (%25)** | %25 |
| `izin_iste` | 14 (%14) | 3 (%20) | **17 (%14)** | %12 |
| `ilgisiz` | 8 (%8) | 5 (%33) | **13 (%11)** | %12 |

⚠️ v0.0.14'te ayrıca sınıf dışı 5 kayıt var (`cevapla`, `yetersiz`); toplam sütununa dahil değiller.

## §5a″ sapmaları ve elle onaylar

| | |
|---|---:|
| ızgaradan sapan kayıt | **13** / 60 |
| — v6-parti3 | 13 |
| elle onaylı `ozerklik_vurgusu` | 11 |
| elle onaylı `is_negative` | 5 |

⭐ Sapan satırlar: parti3#6, parti3#9, parti3#12, parti3#17, parti3#19, parti3#21, parti3#22, parti3#23, parti3#25, parti3#29, parti3#30, parti3#39, parti3#46

## ⭐⭐ Desen kapsaması — partiler arası

Bir kaydın özerklik/red taşıdığı iki yoldan biriyle saptanıyor: **sözlük deseni** ya da **elle onay**. Desenin tek başına yakaladığı oran:

| | v6-parti3 |
|---|---:|
| özerklik | 2/13 (%15) |
| red | 10/15 (%67) |

⭐ Kapsama bir **sözcük** ölçüsü, şablon kapısı bir **dizi** ölçüsü. Aynı fiil farklı cümlelerde geçerse kapsama yükselir, şablon yükselmez. Red cümlelerinin benzersizliği:

| | v6-parti3 |
|---|---:|
| benzersiz red cümlesi / toplam | 20/20 |

➡️ *Sözlük deseni yapıyı değil, KALIBA UYMAYI ölçüyor; şablonu azaltmak ölçülen oranı düşürür ve ölçüm bunu bir gerileme gibi gösterir.*

⛔ Bu, T193'ün ölçtüğü oranı da niteler: o oran bir **alt sınır** değil, **kalıp bağımlı** bir sayıdır.

## ⛔ Bu raporun söylemedikleri

| | |
|---|---|
| ⛔⛔ **Bu bir KALİTE raporu değil** | kapılar biçim ve dayanak denetler; terapötik kaliteyi judge ölçer ve v6-parti3 bu raporda yargılanmadı |
| ⭐ **Üretilmeyen plan satırı yok** | bu raporun kapsadığı partilerde plan satırlarının tamamı üretildi |
| ⚠️ **Elle onay bir İNSAN kararıdır** | desen görmedi, ben onayladım; onay cümlesi betikte yazılı ve kayıtta `gen_meta.elle_onay`ta duruyor |
