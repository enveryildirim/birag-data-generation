# `is_negative` ayrışmasının karara bağlanması

**Betik:** `scripts/analiz/2026-09-21-red-tanimi-uzlastirma.py` · **Tarih:** 2026-09-21  
**Girdi:** T226'nın ayrışan 26 kaydı + 15 kontrol (toplam 41), üç anotatör  

| anotatör | kim |
|---|---|
| `A` | Claude Opus 5 alt ajanı |
| `B` | Claude Sonnet alt ajanı |
| `C` | ben (Claude Code, Opus 5) |

## 1. Anotatörler arası uyum

| soru | çift | ham uyum | κ |
|---|---|---:|---:|
| `talep` | A–B | %95 | 0.90 |
| `talep` | A–C | %98 | 0.95 |
| `talep` | B–C | %93 | 0.85 |
| `red` | A–B | %93 | 0.85 |
| `red` | A–C | %90 | 0.80 |
| `red` | B–C | %88 | 0.76 |

## 2. Kontrol öğeleri — görev geçerli mi

⛔ Kontrollerde iki tanım ZATEN aynı fikirde. Anotatörler burada da onlarla aynı fikirdeyse görev anlaşılmış demektir; ayrılıyorlarsa ayrışan gruptaki hükümleri de şüphelidir.

| anotatör | `a&b: red` (8 öğe) | `a: red YOK` (7 öğe) |
|---|---:|---:|
| `A` | 8/8 | 5/7 |
| `B` | 8/8 | 5/7 |
| `C` | 8/8 | 7/7 |

⭐⭐ **İkinci sütun beklenmedik ve ayrı bir bulgu.** Desen (a) bu 7 kayıtta HİÇ ateşlemiyor, ama anotatörler ortalama **5.7/7**'sinde red görüyor. ⇒ Sözlük yalnız FAZLA saymıyor, AZ da sayıyor: *«söylemeyeceğim»*, *«vermeyeceğim»*, *«demem»* gibi kuruluşlar listede yok. ➡️ *Şablondan kaçınmak için red cümlesini her seferinde başka türlü kurmak, sözlüğü yapısal olarak geride bırakıyor.*


## 3. Ayrışan 26 kaydın kararı — çoğunluk

| # | kayıt | A | B | C | **karar** | sonuç |
|---|---|:-:|:-:|:-:|:-:|---|
| K01 | `v6-parti2#46` | H | H | H | **hayir** | ⛔ (b) haklı — (a) fazla saymış |
| K02 | `v6-parti1#18` | H | H | H | **hayir** | ⛔ (b) haklı — (a) fazla saymış |
| K03 | `v6-parti3#8` | H | H | H | **hayir** | ⛔ (b) haklı — (a) fazla saymış |
| K04 | `v6-parti1#34` | H | H | H | **hayir** | ⛔ (b) haklı — (a) fazla saymış |
| K05 | `v6-parti1#7` | H | H | H | **hayir** | ⛔ (b) haklı — (a) fazla saymış |
| K06 | `v6-parti2#41` | E | E | E | **evet** | ⭐ (a) haklı — sezici talebi kaçırmış |
| K09 | `v6-parti1#22` | H | H | H | **hayir** | ⛔ (b) haklı — (a) fazla saymış |
| K11 | `v6-parti3#34` | H | H | E | **hayir** | ⛔ (b) haklı — (a) fazla saymış |
| K12 | `v6-parti1#14` | H | H | H | **hayir** | ⛔ (b) haklı — (a) fazla saymış |
| K13 | `v6-parti3#26` | H | H | H | **hayir** | ⛔ (b) haklı — (a) fazla saymış |
| K16 | `v6-parti6#54` | E | E | E | **evet** | ⭐ (a) haklı — sezici talebi kaçırmış |
| K17 | `v6-parti1#58` | H | H | H | **hayir** | ⛔ (b) haklı — (a) fazla saymış |
| K20 | `v6-parti3#54` | H | H | H | **hayir** | ⛔ (b) haklı — (a) fazla saymış |
| K21 | `v6-parti4#24` | H | H | H | **hayir** | ⛔ (b) haklı — (a) fazla saymış |
| K22 | `v6-parti1#1` | H | H | H | **hayir** | ⛔ (b) haklı — (a) fazla saymış |
| K24 | `v6-parti2#7` | H | H | H | **hayir** | ⛔ (b) haklı — (a) fazla saymış |
| K26 | `v6-parti4#52` | H | H | H | **hayir** | ⛔ (b) haklı — (a) fazla saymış |
| K28 | `v6-parti1#11` | E | E | E | **evet** | ⭐ (a) haklı — sezici talebi kaçırmış |
| K30 | `v6-parti1#59` | H | H | H | **hayir** | ⛔ (b) haklı — (a) fazla saymış |
| K31 | `v6-parti4#20` | H | E | E | **evet** | ⭐ (a) haklı — sezici talebi kaçırmış |
| K32 | `v6-parti5#7` | H | H | H | **hayir** | ⛔ (b) haklı — (a) fazla saymış |
| K34 | `v6-parti1#8` | H | E | H | **hayir** | ⛔ (b) haklı — (a) fazla saymış |
| K35 | `v6-parti4#51` | H | H | H | **hayir** | ⛔ (b) haklı — (a) fazla saymış |
| K36 | `v6-parti3#44` | H | E | H | **hayir** | ⛔ (b) haklı — (a) fazla saymış |
| K38 | `v6-parti4#55` | H | H | H | **hayir** | ⛔ (b) haklı — (a) fazla saymış |
| K41 | `v6-parti3#11` | H | H | H | **hayir** | ⛔ (b) haklı — (a) fazla saymış |

⭐ **4** kayıtta (a) haklı (sezici kaçırdı), **22** kayıtta (b) haklı ((a) fazla saydı). Üç anotatörün TAMAMI aynı fikirde: **22/26**.

## 4. `talep` vekili `red` hedefini ne kadar izliyor

| anotatör | `talep`≠`red` olan öğe |
|---|---:|
| `A` | 5/41 |
| `B` | 4/41 |
| `C` | 2/41 |

## ⛔ Bu kararın söylemedikleri

| | |
|---|---|
| ⛔⛔ **Üç anotatör de Claude** | ikisi alt ajan, biri ben; üçü aynı model ailesinden. Yüksek uyum **bağımsızlık kanıtı değildir** — ortak yanlılık uyumu yukarı çeker. Uzman anotatör hâlâ açık kalem |
| ⛔ **Çoğunluk bir doğruluk ölçütü değil** | 2/3 çoğunlukla karara bağlanan kayıtlar tablosunda ayrıca işaretli; tam uyum sayısı yukarıda |
| ⚠️ **Karar kayda YAZILMADI** | bu betik hiçbir kayda dokunmaz; tanımın onarımı ve yeniden ölçüm ayrı adımdır |
