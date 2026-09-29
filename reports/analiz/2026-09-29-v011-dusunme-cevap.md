# Düşünme ↔ cevap uyuşmazlığı taraması — `v0.1.1` (T301)

**Betik:** `scripts/analiz/2026-09-29-v011-dusunme-cevap.py` · **Tarih:** 2026-09-29  
**Girdi:** `data/candidates/v011-faz2-b*.jsonl` + `v011-pilot.jsonl` (41 dosya, birleşik SHA256-16 `c7492ac50a0eb750`) — yeniden kurulmuş aday kayıtlar, reddedilenler dahil  
⛔ **Bu bir elek, hüküm değil.** İşaretlenen kayıt elle okunur; sayı, aşağıdaki hata profiliyle birlikte kullanılır.

## Sonuç: 97/1039 kayıt işaretlendi (%9.3)

| kategori | işaret | ölçülmüş hata profili |
|---|---:|---|
| cevapta var düşünmede yok | 64 | 5 örnekte 2 gerçek, 3 sınırda ⇒ kaba ~%40 gerçek |
| cevap soruyla bitiyor, düşünmede soru hamlesi yok | 28 | **alt sınır** — `\bsoru` «sorun»u da eşliyor, bazı gerçek boşluklar kaçıyor |
| düşünme yönlendirme YOK diyor, cevapta var | 7 | **7/7 yanlış olumlu** (elle okundu) ⇒ #0909 tipi gerçek çelişki seyrek |

## ⛔ Bunun söylemedikleri

| | |
|---|---|
| ⛔ **Hata profili bir önceki koşuda ölçüldü** | örneklemeler (A 7/7, B 5, C kalibrasyonu) 2026-09-29'daki ilk koşuda yapıldı; o koşu **98** işaret vermişti. Fark tek kayıt: #0920 (B, *«hekim»*) — blok 37 yeniden açılıp onarıldıktan sonra işaret düştü (T302). Profil yeniden ölçülmedi |
| ⛔ **İlk sürüm %37,1 veriyordu** | C kategorisi yalnız «soruyorum» arıyordu, 4/4 örnekte yanlış olumlu ⇒ ölçüt gevşetildi. Hata profili ölçülmeden bildirilseydi korpusun üçte biri uyuşmaz sayılacaktı (T293 §4) |
| ⚠️ **Anahtar sözcük eleği** | yönlendirme sözcük listesiyle aranır; eşanlamlı ya da dolaylı yönlendirme kaçar |
| ⚠️ **Reddedilenler dahil** | eleğin girdisi aday dosyalar; derlemede `v0.1.0` hâliyle kalan 3 red de taranıyor |

## İşaretlenen kayıtlar

| blok | id | not |
|---|---|---|
| 01 | `b6c107d1` | düşünme yönlendirme YOK diyor, cevapta var: ['başvur', 'randevu'] |
| 01 | `6fab8b17` | cevapta var düşünmede yok: ['danışma'] |
| 01 | `f7cdb984` | cevapta var düşünmede yok: ['aile hekim', 'danışma'] |
| 02 | `846f79e0` | cevapta var düşünmede yok: ['başvur'] |
| 02 | `71982350` | düşünme yönlendirme YOK diyor, cevapta var: ['doktor'] |
| 03 | `6f66040d` | cevapta var düşünmede yok: ['avukat'] |
| 03 | `f3bae7f4` | cevapta var düşünmede yok: ['danışma'] |
| 04 | `d383afea` | cevapta var düşünmede yok: ['danışma', 'hastane'] |
| 04 | `f110f0a8` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 04 | `475400e6` | cevapta var düşünmede yok: ['poliklinik'] |
| 05 | `139b2542` | cevapta var düşünmede yok: ['avukat', 'danışma'] |
| 06 | `dd8d7628` | cevapta var düşünmede yok: ['danışma'] |
| 06 | `49180a24` | cevapta var düşünmede yok: ['danışma', 'hastane'] |
| 06 | `9836dd26` | düşünme yönlendirme YOK diyor, cevapta var: ['hekim'] |
| 06 | `6565558f` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 06 | `f74bf4c6` | cevapta var düşünmede yok: ['başvur', 'randevu'] |
| 07 | `b9bc8b7d` | düşünme yönlendirme YOK diyor, cevapta var: ['hekim'] |
| 07 | `405d3a57` | cevapta var düşünmede yok: ['başvur'] |
| 08 | `026af316` | cevapta var düşünmede yok: ['başvur'] |
| 08 | `3ef8184c` | cevapta var düşünmede yok: ['danışma'] |
| 08 | `9b3fd43f` | cevapta var düşünmede yok: ['danışma'] |
| 08 | `827bf3ac` | cevapta var düşünmede yok: ['başvur', 'randevu'] |
| 09 | `c977b4d0` | cevapta var düşünmede yok: ['başvur'] |
| 09 | `cb0b36a9` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 10 | `9476b9da` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 11 | `da7c1844` | cevapta var düşünmede yok: ['başvur'] |
| 11 | `4cf19ac5` | cevapta var düşünmede yok: ['hekim'] |
| 11 | `0369323c` | düşünme yönlendirme YOK diyor, cevapta var: ['hekim'] |
| 11 | `d74171b5` | cevapta var düşünmede yok: ['başvur'] |
| 12 | `ef8c5571` | cevapta var düşünmede yok: ['acil servis'] |
| 12 | `4394dc5e` | cevapta var düşünmede yok: ['hastane'] |
| 13 | `33187fab` | cevapta var düşünmede yok: ['başvur', 'randevu'] |
| 14 | `4583458d` | cevapta var düşünmede yok: ['hekim'] |
| 15 | `aab51926` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 15 | `09ae7f6c` | cevapta var düşünmede yok: ['hekim'] |
| 16 | `631dccc6` | cevapta var düşünmede yok: ['avukat'] |
| 18 | `ee198f5f` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 18 | `dbbc5e69` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 19 | `a83abd7a` | cevapta var düşünmede yok: ['hekim'] |
| 20 | `aaa1c9a0` | cevapta var düşünmede yok: ['hekim'] |
| 20 | `7ae5fce1` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 21 | `047041e8` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 21 | `528d51d4` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 21 | `78208097` | cevapta var düşünmede yok: ['başvur'] |
| 21 | `5d9eb503` | cevapta var düşünmede yok: ['başvur'] |
| 22 | `1c444ef3` | cevapta var düşünmede yok: ['Hekim', 'hekim'] |
| 22 | `41659cc0` | cevapta var düşünmede yok: ['danışma'] |
| 23 | `9a18e54c` | cevapta var düşünmede yok: ['aile hekim'] |
| 23 | `32e9e8ad` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 23 | `b1085207` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 23 | `2c6ecddc` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 23 | `8c735882` | cevapta var düşünmede yok: ['avukat'] |
| 23 | `91bec3d2` | cevapta var düşünmede yok: ['aile hekim'] |
| 24 | `80061dae` | cevapta var düşünmede yok: ['randevu'] |
| 25 | `620a46f8` | cevapta var düşünmede yok: ['randevu'] |
| 25 | `cb9d15fd` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 25 | `3c980fa0` | cevapta var düşünmede yok: ['hekim', 'randevu'] |
| 25 | `be0e0af5` | cevapta var düşünmede yok: ['başvur'] |
| 26 | `14414424` | cevapta var düşünmede yok: ['danışma'] |
| 26 | `badbebf8` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 26 | `d4fb7f82` | cevapta var düşünmede yok: ['aile hekim', 'danışma'] ; cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 26 | `ddf3d8e5` | cevapta var düşünmede yok: ['randevu'] |
| 27 | `839a4ee9` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 27 | `838aaddb` | cevapta var düşünmede yok: ['hekim'] |
| 27 | `cf501982` | cevapta var düşünmede yok: ['poliklinik'] ; cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 27 | `9369c080` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 28 | `fb891b3c` | cevapta var düşünmede yok: ['başvur', 'randevu'] |
| 28 | `ac69f9ad` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 28 | `682a0223` | cevapta var düşünmede yok: ['başvur'] |
| 29 | `951a450b` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 29 | `cd220a82` | cevapta var düşünmede yok: ['hekim'] |
| 29 | `2bf81fd4` | cevapta var düşünmede yok: ['başvur'] |
| 30 | `0387a035` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 30 | `8d7666e7` | cevapta var düşünmede yok: ['uzman'] |
| 30 | `677c665a` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 30 | `72e53a59` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 31 | `f3c15ff6` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 31 | `f79f4657` | cevapta var düşünmede yok: ['hekim'] |
| 32 | `cf1f6c73` | cevapta var düşünmede yok: ['başvur'] |
| 32 | `6e631d86` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 32 | `5a0a86ee` | cevapta var düşünmede yok: ['Acil servis'] |
| 32 | `0ef67edc` | cevapta var düşünmede yok: ['başvur'] |
| 33 | `1c885fdb` | cevapta var düşünmede yok: ['danışma', 'randevu'] |
| 33 | `920f5e48` | cevapta var düşünmede yok: ['başvur'] |
| 34 | `8c45a9af` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| 37 | `17908b51` | cevapta var düşünmede yok: ['Hastane'] |
| 40 | `40ff94ee` | düşünme yönlendirme YOK diyor, cevapta var: ['doktor'] |
| 40 | `0e672a31` | düşünme yönlendirme YOK diyor, cevapta var: ['danışma', 'randevu'] |
| v011-pilot | `df1bb280` | cevapta var düşünmede yok: ['başvur'] |
| v011-pilot | `a7a6b537` | cevapta var düşünmede yok: ['acil servis'] |
| v011-pilot | `14dfd2d4` | cevapta var düşünmede yok: ['randevu'] |
| v011-pilot | `d24c55e8` | cevapta var düşünmede yok: ['aile hekim', 'poliklinik'] |
| v011-pilot | `89a191d1` | cevap soruyla bitiyor, düşünmede soru hamlesi yok |
| v011-pilot | `899e4cc9` | cevapta var düşünmede yok: ['Aile hekim'] |
| v011-pilot | `e2d1402e` | cevapta var düşünmede yok: ['başvur'] |
| v011-pilot | `e4e14c93` | cevapta var düşünmede yok: ['Psikiyatr'] |
| v011-pilot | `efce7df4` | cevapta var düşünmede yok: ['başvur'] |
