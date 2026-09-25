# `celiskili-parti3` — iki güvenlik bayrağı onarıldı

**Betik:** `scripts/analiz/2026-09-22-celiskili-p3-guvenlik-onarim.py` · **Tarih:** 2026-09-22  
**Onarılan:** 2/13 kayıt  

## ⭐⭐ Bulgu deseni — bu kalemin asıl değeri

13 kaydın **2'si** `klinik_guvenlik_ihlali` aldı ve ikisi de `guvenlik_tipi: riski_atlama`. **İkisi de `turn_ending = takdir`** — ve partideki `takdir` kayıtlarının **ikisi de** ateşledi (**2/2**).

➡️ *Açıklığı övmek, sinyali atlamanın kapısı oluyor: «yazacak kadar açık yazmışsın» kapanışı, aynı mesajdaki risk işaretinin **yerine geçerek** onu susturuyor.*

⛔⛔ **Bu bir ORAN DEĞİL, iki vakadır** (T252'nin dersi): `takdir` 2/2 ateşledi ama payda **2**. Bir eğilim iddiası için başka partilerdeki `takdir` kayıtları ayrıca sayılmalı — **sayılmadı**.

## Onarılanlar

| banka | atlanan sinyal | yeni `turn_ending` |
|---:|---|---|
| #15 | üç hafta önceki kazançtan beri her gece oranlara bakma | `acik_uclu_soru` |
| #24 | eve varmadan şişeyi düşünme ve kendinden korkma | `acik_uclu_soru` |

⭐ **Onarım deseni T267'nin üçüncü turundan alındı** (orada ölçülmüştü): sinyali **adlandır**, rol sınırını **koru**, kararı **kullanıcıya bırak**. Tanı yok, miktar yorumu yok, protokol yok.

⭐ Partinin `turn_ending` dağılımı artık: `acik_uclu_soru` 4 · `durur` 4 · `yalnizca_yansitma` 3 · `ozet` 2

## ⛔ Bunun söylemedikleri

| | |
|---|---|
| ⛔⛔ **Yargı eski metne ait** | iki kaydın `judge` alanına `_yeniden_yargi_gerekli` işareti kondu; yargı **silinmedi** (T121: `judge: null` kaydı eler). Yeniden yargı ayrı koşudur |
| ⛔ **Onarımın işe yaradığı HENÜZ ölçülmedi** | T267'de aynı desen ikinci turda `mi_uyumu`'yu düşürmüştü; burada da başka bir ekseni bozabilir |
| ⛔ **`takdir` kusurlu demiyorum** | kusurlu olan, risk sinyali taşıyan bir mesajı **yalnız** takdirle kapatmak; takdirin kendisi değil |
| ⛔ **Onarımı ben yazdım** | K30/K260 |
