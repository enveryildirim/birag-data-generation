# v6-parti6 — birleştirme ve kapı denetimi

**Betik:** `scripts/analiz/2026-09-20-v6-parti2-birlestir.py` · **Tarih:** 2026-09-20

## `v6-parti6`

| | |
|---|---:|
| plan satırı | 60 |
| ⭐ üretilen kayıt | **58** |
| ⛔ üretilmeyen | [2, 36] |
| ⭐ `run_checks` geçen | **58/58** |
| tohum eşleşmesi | 58/58 |

## Bağlam sınıfı dağılımı (§7a)

⛔ Parti2'nin ilk 13 bağlam kaydının 13'ü `cevap_var` çıktı: T197'yi (*«soruyu pasaja uyacak şekilde tasarla»*) tek biçimde uygulamışım. ⭐ Bütünde hedefe yakın durulması iki partinin TERS yönde sapmasının sonucudur, tasarımın değil.

| sınıf | v0.0.14 | v6-parti6 | **bütün** | hedef |
|---|---:|---:|---:|---:|
| `cevap_var` | 51 (%50) | 3 (%20) | **54 (%46)** | %50 |
| `cevap_yok` | 25 (%24) | 4 (%27) | **29 (%25)** | %25 |
| `izin_iste` | 14 (%14) | 3 (%20) | **17 (%14)** | %12 |
| `ilgisiz` | 8 (%8) | 5 (%33) | **13 (%11)** | %12 |

⚠️ v0.0.14'te ayrıca sınıf dışı 5 kayıt var (`cevapla`, `yetersiz`); toplam sütununa dahil değiller.

## §5a″ sapmaları ve elle onaylar

| | |
|---|---:|
| ızgaradan sapan kayıt | **11** / 58 |
| — v6-parti6 | 11 |
| elle onaylı `ozerklik_vurgusu` | 12 |
| elle onaylı `is_negative` | 8 |

⭐ Sapan satırlar: parti6#6, parti6#8, parti6#13, parti6#23, parti6#25, parti6#39, parti6#43, parti6#45, parti6#46, parti6#47, parti6#60

## ⭐⭐ Desen kapsaması — partiler arası

Bir kaydın özerklik/red taşıdığı iki yoldan biriyle saptanıyor: **sözlük deseni** ya da **elle onay**. Desenin tek başına yakaladığı oran:

| | v6-parti6 |
|---|---:|
| özerklik | 0/12 (%0) |
| red | 0/8 (%0) |

⭐ Kapsama bir **sözcük** ölçüsü, şablon kapısı bir **dizi** ölçüsü. Aynı fiil farklı cümlelerde geçerse kapsama yükselir, şablon yükselmez. Red cümlelerinin benzersizliği:

| | v6-parti6 |
|---|---:|
| benzersiz red cümlesi / toplam | 2/2 |

➡️ *Sözlük deseni yapıyı değil, KALIBA UYMAYI ölçüyor; şablonu azaltmak ölçülen oranı düşürür ve ölçüm bunu bir gerileme gibi gösterir.*

⛔ Bu, T193'ün ölçtüğü oranı da niteler: o oran bir **alt sınır** değil, **kalıp bağımlı** bir sayıdır.

## ⛔ Bu raporun söylemedikleri

| | |
|---|---|
| ⛔⛔ **Bu bir KALİTE raporu değil** | kapılar biçim ve dayanak denetler; terapötik kaliteyi judge ölçer ve v6-parti6 bu raporda yargılanmadı |
| ⛔ **2 plan satırı üretilmedi** | üretilmeyenler: v6-parti6#2, v6-parti6#36 — gerekçeleri `data/plan/elenen-tohumlar.jsonl` ve ilgili blok betiklerinde |
| ⚠️ **Elle onay bir İNSAN kararıdır** | desen görmedi, ben onayladım; onay cümlesi betikte yazılı ve kayıtta `gen_meta.elle_onay`ta duruyor |
