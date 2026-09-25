# `ozerklik_vurgusu`'nun karara bağlanması

**Betik:** `scripts/analiz/2026-09-21-ozerklik-tanimi-uzlastirma.py` · **Tarih:** 2026-09-21  
**Girdi:** 70 öğe — A tabakasının tamamı (24), B'den 20/65, C'den 26/323; karıştırılmış, tabaka bilgisi verilmedi  

| anotatör | kim |
|---|---|
| `A` | Claude Opus 5 alt ajanı |
| `B` | Claude Sonnet alt ajanı |
| `C` | ben (Claude Code, Opus 5) |

## 1. Anotatörler arası uyum

| soru | çift | ham uyum | κ |
|---|---|---:|---:|
| `karar_var` | A–B | %64 | 0.16 |
| `karar_var` | A–C | %79 | 0.52 |
| `karar_var` | B–C | %83 | 0.27 |
| `ozerklik` | A–B | %99 | 0.97 |
| `ozerklik` | A–C | %94 | 0.88 |
| `ozerklik` | B–C | %93 | 0.85 |

## 2. Tabaka tabaka — alan ne diyor, anotatörler ne diyor

| tabaka | alan | örneklem | çoğunluk `ozerklik`=evet | ⇒ |
|---|:-:|---:|---:|---|
| `A` (yalnız desen) | evet | 24 | 23/24 (%96) | ⛔ desen FAZLA saymış |
| `B` (yalnız elle onay) | evet | 20 | 17/20 (%85) | ⛔ onaylarım FAZLA saymış |
| `C` (hiçbiri) | hayır | 26 | 5/26 (%19) | ⛔ alan AZ saymış |

## 3. Korpusa taşıma

Alanın şu an *«özerklik var»* dediği: **89/412** (%22).  
Tabaka oranları evrene taşınınca kestirim: **~140/412** (%34), %95 aralık **92-207** (%22-%50).

⛔ `A` bir SAYIM (24 kaydın tamamı okundu); `B` ve `C` ÖRNEKLEM. Aralığı açan bileşen `C`: 26 kayıtta 5 ⇒ oran %19, Wilson aralığı %9-%38 ve bu 323 kayda çarpılıyor (27-122 kayıt).

⇒ **Kestirim, alanın %22'sinin bir ALT SINIR olduğunu söylüyor; kaç puan alt sınır olduğunu söylemiyor.** Aralığın alt ucu bile mevcut sayının üstünde (92 > 89), yani AZ SAYMA yönü aralıktan bağımsız.

## 4. Ön şart tutuyor mu — `karar_var`

⛔⛔ **BU BÖLÜMÜN SAYISINA GÜVENİLEMEZ VE SEBEBİ YUKARIDA:** `karar_var`'da anotatör uyumu κ **0,16-0,52** çıktı (`ozerklik`'te 0,85-0,97). ➡️ *T227'de `talep` ön şartı güvenilir biçimde etiketlenebiliyordu; «ortada bir karar var mı» etiketlenemiyor.* ⇒ Özerklik için T227'deki gibi bir ön şart kurulamaz — aşağıdaki sayı yalnız kayda geçsin diye duruyor.

| | |
|---|---:|
| çoğunluk `ozerklik`=evet | 45 |
| ⛔ — bunların kararı olmayanı | **1** (v6-parti5#25) |

## 5. Kayıt kayıt karar

| # | kayıt | tabaka | A | B | C | **karar** | alan | değişir mi |
|---|---|:-:|:-:|:-:|:-:|:-:|:-:|---|
| Z01 | `v6-parti1#39` | A | E | E | E | **evet** | evet | — |
| Z02 | `v6-parti6#55` | B | E | E | H | **evet** | evet | — |
| Z03 | `v6-parti5#25` | A | E | E | H | **evet** | evet | — |
| Z04 | `v6-parti3#26` | B | E | E | E | **evet** | evet | — |
| Z05 | `v6-parti5#45` | B | E | E | H | **evet** | evet | — |
| Z06 | `v6-parti1#34` | A | E | E | E | **evet** | evet | — |
| Z07 | `v6-parti2#37` | A | E | E | E | **evet** | evet | — |
| Z08 | `v6-parti7#10` | B | E | E | E | **evet** | evet | — |
| Z09 | `v6-parti3#34` | B | H | H | H | **hayir** | evet | ⛔ **hayır** |
| Z10 | `v6-parti5#27` | A | H | H | H | **hayir** | evet | ⛔ **hayır** |
| Z11 | `v6-parti4#28` | C | H | H | H | **hayir** | hayır | — |
| Z12 | `v6-parti7#5` | A | E | H | E | **evet** | evet | — |
| Z13 | `v6-parti1#11` | A | E | E | E | **evet** | evet | — |
| Z14 | `v6-parti1#35` | C | E | E | E | **evet** | hayır | ⛔ **evet** |
| Z15 | `v6-parti2#24` | B | E | E | E | **evet** | evet | — |
| Z16 | `v6-parti1#38` | A | E | E | E | **evet** | evet | — |
| Z17 | `v6-parti6#41` | B | E | E | E | **evet** | evet | — |
| Z18 | `v6-parti2#27` | B | E | E | E | **evet** | evet | — |
| Z19 | `v6-parti7#46` | C | H | H | H | **hayir** | hayır | — |
| Z20 | `v6-parti5#14` | C | E | E | E | **evet** | hayır | ⛔ **evet** |
| Z21 | `v6-parti4#47` | B | E | E | E | **evet** | evet | — |
| Z22 | `v6-parti7#43` | C | H | H | H | **hayir** | hayır | — |
| Z23 | `v6-parti1#18` | A | E | E | E | **evet** | evet | — |
| Z24 | `v6-parti6#20` | B | H | H | H | **hayir** | evet | ⛔ **hayır** |
| Z25 | `v6-parti3#27` | A | E | E | E | **evet** | evet | — |
| Z26 | `v6-parti1#33` | A | E | E | E | **evet** | evet | — |
| Z27 | `v6-parti2#38` | A | E | E | E | **evet** | evet | — |
| Z28 | `v6-parti1#10` | A | E | E | E | **evet** | evet | — |
| Z29 | `v6-parti3#9` | C | H | H | H | **hayir** | hayır | — |
| Z30 | `v6-parti1#14` | C | H | H | H | **hayir** | hayır | — |
| Z31 | `v6-parti6#4` | B | E | E | E | **evet** | evet | — |
| Z32 | `v6-parti4#6` | C | H | H | H | **hayir** | hayır | — |
| Z33 | `v6-parti4#45` | B | E | E | E | **evet** | evet | — |
| Z34 | `v6-parti1#55` | A | E | E | E | **evet** | evet | — |
| Z35 | `v6-parti4#32` | C | H | H | H | **hayir** | hayır | — |
| Z36 | `v6-parti5#31` | A | E | E | E | **evet** | evet | — |
| Z37 | `v6-parti3#17` | B | E | E | E | **evet** | evet | — |
| Z38 | `v6-parti5#54` | A | E | E | H | **evet** | evet | — |
| Z39 | `v6-parti4#24` | A | E | E | E | **evet** | evet | — |
| Z40 | `v6-parti1#46` | A | E | E | E | **evet** | evet | — |
| Z41 | `v6-parti5#19` | C | H | H | H | **hayir** | hayır | — |
| Z42 | `v6-parti2#19` | B | E | E | E | **evet** | evet | — |
| Z43 | `v6-parti3#56` | C | H | H | H | **hayir** | hayır | — |
| Z44 | `v6-parti7#9` | C | H | H | H | **hayir** | hayır | — |
| Z45 | `v6-parti5#47` | C | H | H | H | **hayir** | hayır | — |
| Z46 | `v6-parti7#52` | C | H | H | H | **hayir** | hayır | — |
| Z47 | `v6-parti1#44` | A | E | E | E | **evet** | evet | — |
| Z48 | `v6-parti7#3` | C | H | H | H | **hayir** | hayır | — |
| Z49 | `v6-parti1#47` | C | H | H | H | **hayir** | hayır | — |
| Z50 | `v6-parti3#7` | A | E | E | E | **evet** | evet | — |
| Z51 | `v6-parti3#60` | C | H | H | H | **hayir** | hayır | — |
| Z52 | `v6-parti3#8` | C | H | H | H | **hayir** | hayır | — |
| Z53 | `v6-parti3#1` | B | E | E | E | **evet** | evet | — |
| Z54 | `v6-parti1#8` | A | E | E | E | **evet** | evet | — |
| Z55 | `v6-parti3#50` | B | H | H | H | **hayir** | evet | ⛔ **hayır** |
| Z56 | `v6-parti5#37` | C | E | E | E | **evet** | hayır | ⛔ **evet** |
| Z57 | `v6-parti1#5` | A | E | E | E | **evet** | evet | — |
| Z58 | `v6-parti6#33` | C | H | H | H | **hayir** | hayır | — |
| Z59 | `v6-parti5#43` | B | E | E | E | **evet** | evet | — |
| Z60 | `v6-parti4#37` | B | E | E | E | **evet** | evet | — |
| Z61 | `v6-parti1#56` | A | E | E | E | **evet** | evet | — |
| Z62 | `v6-parti1#15` | A | E | E | E | **evet** | evet | — |
| Z63 | `v6-parti6#49` | C | H | H | H | **hayir** | hayır | — |
| Z64 | `v6-parti3#57` | B | E | E | E | **evet** | evet | — |
| Z65 | `v6-parti4#2` | C | H | H | H | **hayir** | hayır | — |
| Z66 | `v6-parti6#23` | C | H | H | H | **hayir** | hayır | — |
| Z67 | `v6-parti2#16` | B | E | E | E | **evet** | evet | — |
| Z68 | `v6-parti1#23` | C | E | E | E | **evet** | hayır | ⛔ **evet** |
| Z69 | `v6-parti2#28` | C | H | H | H | **hayir** | hayır | — |
| Z70 | `v6-parti7#41` | C | E | E | E | **evet** | hayır | ⛔ **evet** |

⭐ Üç anotatörün tamamı aynı fikirde: **65/70**. Alanla ayrışan: **9/70**.

## ⛔ Bu kararın söylemedikleri

| | |
|---|---|
| ⛔⛔ **Üç anotatör de Claude** | T227'nin şerhi aynen geçerli: ortak yanlılık uyumu yukarı çeker, bu bir bağımsızlık kanıtı değildir |
| ⛔⛔ **`C` tabakası ÖRNEKLEM** | 323 kaydın 26'sı okundu; korpus kestirimi bu orana çok duyarlı ve güven aralığı hesaplanmadı |
| ⛔ **`B` tabakası benim kendi onaylarım** | anotatör `C` de benim ⇒ o sütunda kendi kararımı ikinci kez veriyorum, bağımsız değil |
| ⚠️ **Karar kayda yazılmadı** | bu betik hiçbir kayda dokunmaz |
