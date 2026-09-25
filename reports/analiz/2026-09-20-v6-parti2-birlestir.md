# v6-parti2 — birleştirme ve kapı denetimi

**Betik:** `scripts/analiz/2026-09-20-v6-parti2-birlestir.py` · **Tarih:** 2026-09-20

## `v6-parti2`

| | |
|---|---:|
| plan satırı | 60 |
| ⭐ üretilen kayıt | **59** |
| ⛔ üretilmeyen | [54] |
| ⭐ `run_checks` geçen | **59/59** |
| tohum eşleşmesi | 59/59 |

## Bağlam sınıfı dağılımı (§7a)

⛔ Parti2'nin ilk 13 bağlam kaydının 13'ü `cevap_var` çıktı: T197'yi (*«soruyu pasaja uyacak şekilde tasarla»*) tek biçimde uygulamışım. ⭐ Bütünde hedefe yakın durulması iki partinin TERS yönde sapmasının sonucudur, tasarımın değil.

| sınıf | v0.0.14 | v6-parti2 | **bütün** | hedef |
|---|---:|---:|---:|---:|
| `cevap_var` | 51 (%50) | 13 (%87) | **64 (%54)** | %50 |
| `cevap_yok` | 25 (%24) | 1 (%7) | **26 (%22)** | %25 |
| `izin_iste` | 14 (%14) | 0 (%0) | **14 (%12)** | %12 |
| `ilgisiz` | 8 (%8) | 1 (%7) | **9 (%8)** | %12 |

⚠️ v0.0.14'te ayrıca sınıf dışı 5 kayıt var (`cevapla`, `yetersiz`); toplam sütununa dahil değiller.

## §5a″ sapmaları ve elle onaylar

| | |
|---|---:|
| ızgaradan sapan kayıt | **7** / 59 |
| — v6-parti2 | 7 |
| elle onaylı `ozerklik_vurgusu` | 10 |
| elle onaylı `is_negative` | 7 |

⭐ Sapan satırlar: parti2#1, parti2#15, parti2#28, parti2#48, parti2#52, parti2#59, parti2#60

## ⭐⭐ Desen kapsaması — partiler arası

Bir kaydın özerklik/red taşıdığı iki yoldan biriyle saptanıyor: **sözlük deseni** ya da **elle onay**. Desenin tek başına yakaladığı oran:

| | v6-parti2 |
|---|---:|
| özerklik | 2/12 (%17) |
| red | 4/11 (%36) |

⭐ Kapsama bir **sözcük** ölçüsü, şablon kapısı bir **dizi** ölçüsü. Aynı fiil farklı cümlelerde geçerse kapsama yükselir, şablon yükselmez. Red cümlelerinin benzersizliği:

| | v6-parti2 |
|---|---:|
| benzersiz red cümlesi / toplam | 5/5 |

➡️ *Sözlük deseni yapıyı değil, KALIBA UYMAYI ölçüyor; şablonu azaltmak ölçülen oranı düşürür ve ölçüm bunu bir gerileme gibi gösterir.*

⛔ Bu, T193'ün ölçtüğü oranı da niteler: o oran bir **alt sınır** değil, **kalıp bağımlı** bir sayıdır.

## ⛔ Bu raporun söylemedikleri

| | |
|---|---|
| ⛔⛔ **Bu bir KALİTE raporu değil** | kapılar biçim ve dayanak denetler; terapötik kaliteyi judge ölçer ve v6-parti2 bu raporda yargılanmadı |
| ⛔ **1 plan satırı üretilmedi** | üretilmeyenler: v6-parti2#54 — gerekçeleri `data/plan/elenen-tohumlar.jsonl` ve ilgili blok betiklerinde |
| ⚠️ **Elle onay bir İNSAN kararıdır** | desen görmedi, ben onayladım; onay cümlesi betikte yazılı ve kayıtta `gen_meta.elle_onay`ta duruyor |
