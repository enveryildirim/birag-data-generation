# v6-parti4 — birleştirme ve kapı denetimi

**Betik:** `scripts/analiz/2026-09-20-v6-parti2-birlestir.py` · **Tarih:** 2026-09-20

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

| sınıf | v0.0.14 | v6-parti4 | **bütün** | hedef |
|---|---:|---:|---:|---:|
| `cevap_var` | 51 (%50) | 3 (%21) | **54 (%46)** | %50 |
| `cevap_yok` | 25 (%24) | 4 (%29) | **29 (%25)** | %25 |
| `izin_iste` | 14 (%14) | 3 (%21) | **17 (%15)** | %12 |
| `ilgisiz` | 8 (%8) | 4 (%29) | **12 (%10)** | %12 |

⚠️ v0.0.14'te ayrıca sınıf dışı 5 kayıt var (`cevapla`, `yetersiz`); toplam sütununa dahil değiller.

## §5a″ sapmaları ve elle onaylar

| | |
|---|---:|
| ızgaradan sapan kayıt | **11** / 59 |
| — v6-parti4 | 11 |
| elle onaylı `ozerklik_vurgusu` | 11 |
| elle onaylı `is_negative` | 7 |

⭐ Sapan satırlar: parti4#10, parti4#19, parti4#22, parti4#29, parti4#32, parti4#33, parti4#38, parti4#46, parti4#53, parti4#57, parti4#60

## ⭐⭐ Desen kapsaması — partiler arası

Bir kaydın özerklik/red taşıdığı iki yoldan biriyle saptanıyor: **sözlük deseni** ya da **elle onay**. Desenin tek başına yakaladığı oran:

| | v6-parti4 |
|---|---:|
| özerklik | 1/12 (%8) |
| red | 12/19 (%63) |

⭐ Kapsama bir **sözcük** ölçüsü, şablon kapısı bir **dizi** ölçüsü. Aynı fiil farklı cümlelerde geçerse kapsama yükselir, şablon yükselmez. Red cümlelerinin benzersizliği:

| | v6-parti4 |
|---|---:|
| benzersiz red cümlesi / toplam | 18/18 |

➡️ *Sözlük deseni yapıyı değil, KALIBA UYMAYI ölçüyor; şablonu azaltmak ölçülen oranı düşürür ve ölçüm bunu bir gerileme gibi gösterir.*

⛔ Bu, T193'ün ölçtüğü oranı da niteler: o oran bir **alt sınır** değil, **kalıp bağımlı** bir sayıdır.

## ⛔ Bu raporun söylemedikleri

| | |
|---|---|
| ⛔⛔ **Bu bir KALİTE raporu değil** | kapılar biçim ve dayanak denetler; terapötik kaliteyi judge ölçer ve v6-parti4 bu raporda yargılanmadı |
| ⛔ **1 plan satırı üretilmedi** | üretilmeyenler: v6-parti4#16 — gerekçeleri `data/plan/elenen-tohumlar.jsonl` ve ilgili blok betiklerinde |
| ⚠️ **Elle onay bir İNSAN kararıdır** | desen görmedi, ben onayladım; onay cümlesi betikte yazılı ve kayıtta `gen_meta.elle_onay`ta duruyor |
