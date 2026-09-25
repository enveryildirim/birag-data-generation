# v6-parti1 — birleştirme ve kapı denetimi

**Betik:** `scripts/analiz/2026-09-20-v6-parti2-birlestir.py` · **Tarih:** 2026-09-20

## `v6-parti1`

| | |
|---|---:|
| plan satırı | 60 |
| ⭐ üretilen kayıt | **59** |
| ⛔ üretilmeyen | [29] |
| ⭐ `run_checks` geçen | **59/59** |
| tohum eşleşmesi | 59/59 |

## Bağlam sınıfı dağılımı (§7a)

⛔ Parti2'nin ilk 13 bağlam kaydının 13'ü `cevap_var` çıktı: T197'yi (*«soruyu pasaja uyacak şekilde tasarla»*) tek biçimde uygulamışım. ⭐ Bütünde hedefe yakın durulması iki partinin TERS yönde sapmasının sonucudur, tasarımın değil.

| sınıf | v0.0.14 | v6-parti1 | **bütün** | hedef |
|---|---:|---:|---:|---:|
| `cevap_var` | 51 (%50) | 5 (%33) | **56 (%47)** | %50 |
| `cevap_yok` | 25 (%24) | 6 (%40) | **31 (%26)** | %25 |
| `izin_iste` | 14 (%14) | 1 (%7) | **15 (%13)** | %12 |
| `ilgisiz` | 8 (%8) | 3 (%20) | **11 (%9)** | %12 |

⚠️ v0.0.14'te ayrıca sınıf dışı 5 kayıt var (`cevapla`, `yetersiz`); toplam sütununa dahil değiller.

## §5a″ sapmaları ve elle onaylar

| | |
|---|---:|
| ızgaradan sapan kayıt | **4** / 59 |
| — v6-parti1 | 4 |
| elle onaylı `ozerklik_vurgusu` | 2 |
| elle onaylı `is_negative` | 4 |

⭐ Sapan satırlar: parti1#11, parti1#48, parti1#51, parti1#59

## ⭐⭐ Desen kapsaması — partiler arası

Bir kaydın özerklik/red taşıdığı iki yoldan biriyle saptanıyor: **sözlük deseni** ya da **elle onay**. Desenin tek başına yakaladığı oran:

| | v6-parti1 |
|---|---:|
| özerklik | 14/16 (%88) |
| red | 8/12 (%67) |

⭐ Kapsama bir **sözcük** ölçüsü, şablon kapısı bir **dizi** ölçüsü. Aynı fiil farklı cümlelerde geçerse kapsama yükselir, şablon yükselmez. Red cümlelerinin benzersizliği:

| | v6-parti1 |
|---|---:|
| benzersiz red cümlesi / toplam | 16/16 |

➡️ *Sözlük deseni yapıyı değil, KALIBA UYMAYI ölçüyor; şablonu azaltmak ölçülen oranı düşürür ve ölçüm bunu bir gerileme gibi gösterir.*

⛔ Bu, T193'ün ölçtüğü oranı da niteler: o oran bir **alt sınır** değil, **kalıp bağımlı** bir sayıdır.

## ⛔ Bu raporun söylemedikleri

| | |
|---|---|
| ⛔⛔ **Bu bir KALİTE raporu değil** | kapılar biçim ve dayanak denetler; terapötik kaliteyi judge ölçer ve v6-parti1 bu raporda yargılanmadı |
| ⛔ **1 plan satırı üretilmedi** | üretilmeyenler: v6-parti1#29 — gerekçeleri `data/plan/elenen-tohumlar.jsonl` ve ilgili blok betiklerinde |
| ⚠️ **Elle onay bir İNSAN kararıdır** | desen görmedi, ben onayladım; onay cümlesi betikte yazılı ve kayıtta `gen_meta.elle_onay`ta duruyor |
