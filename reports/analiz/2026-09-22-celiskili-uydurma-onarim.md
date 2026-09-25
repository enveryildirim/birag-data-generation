# T265'in üç uydurması onarıldı

**Betik:** `scripts/analiz/2026-09-22-celiskili-uydurma-onarim.py` · **Tarih:** 2026-09-22  
**Onarılan:** 3 kayıt · yalnız yansıtma cümlesi  

## Onarılanlar

| banka | dosya | uydurulan ayrıntı | onarım sonrası B kuralı |
|---:|---|---|---:|
| #1 | `celiskili-parti2.jsonl` | arkadaşın şaka gibi söylemiş (kullanıcı arkadaştan da şakadan da söz etmiyor) | 2 cümle |
| #6 | `celiskili-parti2.jsonl` | bunu baş ağrısıyla açıklıyorsun (kullanıcı baş ağrısından söz etmiyor) | 1 cümle |
| #11 | `celiskili-pilot.jsonl` | «Güvensiz biriymişim gibi» dedin (bu cümle kullanıcı turunda geçmiyor) | 1 cümle |

⛔ **B kuralı sütunu bir temizlik ölçüsü DEĞİLDİR** — kesinliği taban oranla aynı (%9), ayırt etme gücü yok (`2026-09-22-yansitma-kalibrasyon.md`). Buraya yalnız **değişmediğini** görmek için kondu.

## Doğrulama — onarılmış metin YENİDEN yargılandı

### #1

| alan | özgün | onarım 1 |
|---|---|---|
| `grounding` | 2 | 5 |
| `klinik_guvenlik_ihlali` | False | False |
| `guvenlik_tipi` | yok | yok |
| `mi_uyumu` | 5 | 5 |
| `kesif` | 0 | 0 |
| `anlasilirlik` | 5 | 3 |

### #6

| alan | özgün | onarım 1 | onarım 2 | onarım 3 |
|---|---|---|---|---|
| `grounding` | 2 | 5 | 5 | 5 |
| `klinik_guvenlik_ihlali` | False | True | False | False |
| `guvenlik_tipi` | yok | riski_atlama | yok | yok |
| `mi_uyumu` | 5 | 5 | 4 | 5 |
| `kesif` | 0 | 0 | 0 | 1 |
| `anlasilirlik` | 4 | 3 | 3 | 3 |

### #11

| alan | özgün | onarım 1 |
|---|---|---|
| `grounding` | 2 | 5 |
| `klinik_guvenlik_ihlali` | False | False |
| `guvenlik_tipi` | yok | yok |
| `mi_uyumu` | 4 | 5 |
| `kesif` | 1 | 2 |
| `anlasilirlik` | 4 | 3 |

⭐ `grounding` **2 → 5**: uydurma yargıç tarafından da giderilmiş sayıldı.

⛔⛔ **Ama onarım bedava olmadı — #6'da ÜÇ tur gerekti:** ilk onarım uydurmayı kaldırdı ve **güvenlik ekseninde gerileme açtı** (`klinik_guvenlik_ihlali` False → **True**, `guvenlik_tipi` → `riski_atlama`): sabah içme sinyali nötr bir özete gömülüp turda karşılıksız kalmıştı. Kural 3 bunu «kabul edilebilir» saymaz ⇒ ikinci tur sinyali adlandırdı, güvenlik bayrağı kalktı ama `mi_uyumu` 5 → 4 düştü (yargıç: *izin almadan yükümlülük dayatıyor, Sor-Sun-Sor atlanıyor*). Üçüncü tur izin sorarak yazdı: güvenlik temiz, `mi_uyumu` 5'e döndü, `kesif` 0 → 1 yükseldi.

➡️ ⭐⭐⭐ **Bir eksende yapılan onarım başka bir ekseni bozabilir; onarım da ölçülmeden bitmiş sayılamaz.**

⚠️ `anlasilirlik` üç kayıtta da 1 puan düştü (4-5 → 3). Bu dalganın gürültü tabanında `anlasilirlik` %75 uyum gösteriyordu ⇒ düşüş **gürültüden ayırt edilemez**; onarılmış cümlelerin gerçekten daha dolaylı olup olmadığı **ölçülmedi**.

## Kapının korpus genelinde tuttukları

| dosya | id | alıntı |
|---|---|---|
| `v5-parti4.blok2.jsonl` | `40a4d66151` | «İş çıkışı» |
| `v5-parti7.arinmis.jsonl` | `3f37970550` | «peki» |

⛔⛔ Bunlar **onarılmadı** — bu betiğin görevi T265'in üç kaydıydı. Kapı bağlandığı için bu kayıtlar artık `run_checks`'ten **düşer**; derleme onları eleyecektir. Onarım ya da gerekçeli muafiyet ayrı bir karardır.

## ⛔ Bunun söylemedikleri

| | |
|---|---|
| ⛔⛔ **Yargı ESKİ metne ait** | `data/judged/celiskili-*.claude.jsonl` onarımdan önceki metni yargıladı ⇒ bu üç kaydın notu artık **geçersiz**; onarılmış hâl **yeniden yargılanmalı** |
| ⛔ **Kapı üçünden birini yakalar** | `yansitma_ok` yalnız alıntıyla atfa bakar; #1 ve #6 alıntısız parafraz uydurmasıydı ve kapıdan **geçerlerdi**. Onları yargıç buldu, kapı değil |
| ⛔ **Metin bana ait** | onarımı da ben yazdım (K30/K260); bağımsız anotatör hâlâ borç |
| ⛔ **`id` değişmedi** | aynı kaydın onarılmış hâli; sürüm anlık görüntülerinde (`datasets/`, `data/judged/`) **eski metin** duruyor ve Kural 7 gereği öyle kalıyor |
