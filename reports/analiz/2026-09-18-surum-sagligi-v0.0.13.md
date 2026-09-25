# Sürüm sağlığı — `v0.0.13`

**Betik:** `scripts/analiz/2026-09-18-surum-sagligi.py` · **Tarih:** 2026-09-18  
**Girdi:** `datasets/v0.0.13/train.jsonl` · **571** kayıt

⛔⛔ **Neden tek sayfa.** Bu depoda otuzdan fazla analiz betiği var ve bu oturumda
bulunan kusurların çoğu **geç** bulundu: inceleme kuyruğu 2026-09-12'den beri
okunmamıştı · §7b kapısı sürüm ilerleyince sessizce kapanmıştı · elle okuma yığını
hiç okunmamıştı. ➡️ *Dağınık ölçüm okunmadığı sürece ölçülmemiş olmaya yakın durur;
kusurlar sayıların arasında değil, RAPORLARIN arasında saklanır.*

⭐ Hiçbir ölçüm yeniden tanımlanmadı (K97): her kapı **kendi betiğinden** çağrıldı.

## Üretim kapısı (`run_checks`)

| | |
|---|---:|
| kayıt | 571 |
| ⭐ geçen | **571** |
| ⛔ elenen | **0** |
| inceleme kuyruğu — yumuşak §15 vuruşu olan kayıt | 4 |
| inceleme kuyruğu — klinik ad izi | 6 |

## Dayanak kapıları

| kapı | otomatik ihlal | elle okunacak |
|---|---:|---:|
| alıntı birebirliği | **0** öge / 0 kayıt | — |
| zaman + kaynak atfı | **0** öge / 0 kayıt | — |
| yapısal atıf | **0** | ⚠️ **20** |
| mekân atfı | **11** | ⚠️ **2** |

⭐ Mekân bulguları **etiketli** — muafiyet değil, okuma önceliği:

| etiket | bulgu |
|---|---:|
| soyut | 4 |
| ⛔ ELLE OKU | 2 |
| soyut+varlık | 2 |
| varlık | 1 |
| kip | 1 |
| soyut+kip | 1 |

⚠️ *«soyut»* = yerde soyut bir nesne duruyor (*«masada iki şey var»*) · *«varlık»* = asistanın kendi bulunuşu (*«ben o odada olmayacağım»*) · *«kip»* = varsayımsal/soru çerçevesi. ⛔ Etiketsizler **elle okunmalı**.

## Şablonlaşma (T157)

Eşik %2 (11 kayıt) · eşiği aşan dizi: **47**

| dizi | kayıt | % |
|---|---:|---:|
| *«bir şeye katilmiyorum»* | 62 | %10.9 |
| *«bugüne kadar söylediklerin şunlar»* | 43 | %7.5 |
| *«benim işim değil»* | 25 | %4.4 |
| *«olduğunu ben söyleyemem»* | 25 | %4.4 |
| *«dair bir şey»* | 23 | %4.0 |
| *«sen karar vereceksin»* | 19 | %3.3 |
## Kullanıcının sözcüğünü koruma

⭐ Depo baştan beri *«kullanıcının KENDİ sözcüğünü kullan»* diyor (T142). Bu sinyal
bu raporun ilk koşusunda bulundu ve buraya **kalıcı** eklendi.

| | |
|---|---:|
| eş/hanım/karı geçen kayıt | 69 |
| ⭐ kullanıcının sözcüğü KORUNMUŞ | **69** |
| ⛔ cevap BAŞKA bir sözcük kullanmış | **0** |

## Okuma defteri

⭐ Elle okunan yığınların hükmü metin değişmedikçe **taşınır**; yalnız
yeni/değişmiş bulgular okunmak üzere listelenir (T171).

| kapı | yığın | ⛔ okunmalı |
|---|---:|---:|
| `yapisal-atif` | 20 | **0** |
| `mekan-atfi` | 2 | **0** |

⭐ **Hiçbir kapıda okunacak yeni bulgu yok.**


⚠️ *«Şablon = kusur»* değildir; ölçülen şey TEKRAR. Ama T162 zincirin son
halkasını gösterdi: §8 özerklik kalıbı modelin davranışında bir güvenlik
bayrağına dönüştü (`gd-018`, uzman kalemi).

## ⛔ Bu raporun söylemedikleri

| | |
|---|---|
| ⛔⛔ **Bu bir KALİTE raporu değil** | kapılar biçim ve dayanak denetler; terapötik kalite Eksen 1'in işidir ve judge gerektirir (T161/T162) |
| ⛔ **Elle okuma yığını otomatik değil** | yapısal atıf kapısının «elle okunacak» sütunu her sürümde İNSAN tarafından okunmalı; T155 o yığında %26 kusur buldu |
| ⛔ **Kapıların kendi kör noktaları duruyor** | süre dalı (T163), kip ayrımı (T165), kısa alıntılar (T143), sert kapının çok sözcüklü ifadeleri (T153) |
| ⚠️ **Sayılar kapıların ölçtüğü kadar** | bir kapının «0» demesi, kapının BAKABİLDİĞİ yerde 0 olduğu demektir (T155) |
