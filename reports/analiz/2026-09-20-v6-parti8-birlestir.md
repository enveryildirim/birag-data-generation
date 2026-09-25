# v6-parti8 — birleştirme ve kapı denetimi

**Betik:** `scripts/analiz/2026-09-20-v6-parti2-birlestir.py` · **Tarih:** 2026-09-20

## `v6-parti8`

| | |
|---|---:|
| plan satırı | 120 |
| ⭐ üretilen kayıt | **118** |
| ⛔ üretilmeyen | [23, 115] |
| ⭐ `run_checks` geçen | **118/118** |
| tohum eşleşmesi | 118/118 |

## Bağlam sınıfı dağılımı (§7a)

⛔ Parti2'nin ilk 13 bağlam kaydının 13'ü `cevap_var` çıktı: T197'yi (*«soruyu pasaja uyacak şekilde tasarla»*) tek biçimde uygulamışım. ⭐ Bütünde hedefe yakın durulması iki partinin TERS yönde sapmasının sonucudur, tasarımın değil.

| sınıf | v0.0.14 | v6-parti8 | **bütün** | hedef |
|---|---:|---:|---:|---:|
| `cevap_var` | 51 (%50) | 11 (%38) | **62 (%47)** | %50 |
| `cevap_yok` | 25 (%24) | 8 (%28) | **33 (%25)** | %25 |
| `izin_iste` | 14 (%14) | 4 (%14) | **18 (%14)** | %12 |
| `ilgisiz` | 8 (%8) | 6 (%21) | **14 (%11)** | %12 |

⚠️ v0.0.14'te ayrıca sınıf dışı 5 kayıt var (`cevapla`, `yetersiz`); toplam sütununa dahil değiller.

## §5a″ sapmaları ve elle onaylar

| | |
|---|---:|
| ızgaradan sapan kayıt | **0** / 118 |
| — v6-parti8 | 0 |
| elle onaylı `ozerklik_vurgusu` | 12 |
| elle onaylı `is_negative` | 9 |

⭐ Sapan satırlar: 

## ⭐⭐ Desen kapsaması — partiler arası

Bir kaydın özerklik/red taşıdığı iki yoldan biriyle saptanıyor: **sözlük deseni** ya da **elle onay**. Desenin tek başına yakaladığı oran:

| | v6-parti8 |
|---|---:|
| özerklik | 14/26 (%54) |
| red | 9/18 (%50) |

⭐ Kapsama bir **sözcük** ölçüsü, şablon kapısı bir **dizi** ölçüsü. Aynı fiil farklı cümlelerde geçerse kapsama yükselir, şablon yükselmez. Red cümlelerinin benzersizliği:

| | v6-parti8 |
|---|---:|
| benzersiz red cümlesi / toplam | 12/12 |

➡️ *Sözlük deseni yapıyı değil, KALIBA UYMAYI ölçüyor; şablonu azaltmak ölçülen oranı düşürür ve ölçüm bunu bir gerileme gibi gösterir.*

⛔ Bu, T193'ün ölçtüğü oranı da niteler: o oran bir **alt sınır** değil, **kalıp bağımlı** bir sayıdır.

## ⛔ Bu raporun söylemedikleri

| | |
|---|---|
| ⛔⛔ **Bu bir KALİTE raporu değil** | kapılar biçim ve dayanak denetler; terapötik kaliteyi judge ölçer ve v6-parti8 bu raporda yargılanmadı |
| ⛔ **2 plan satırı üretilmedi** | üretilmeyenler: v6-parti8#23, v6-parti8#115 — gerekçeleri `data/plan/elenen-tohumlar.jsonl` ve ilgili blok betiklerinde |
| ⚠️ **Elle onay bir İNSAN kararıdır** | desen görmedi, ben onayladım; onay cümlesi betikte yazılı ve kayıtta `gen_meta.elle_onay`ta duruyor |
