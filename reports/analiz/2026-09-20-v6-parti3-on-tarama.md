# v6-parti3 — üretim öncesi kriz taraması

**Betik:** `scripts/analiz/2026-09-20-v6-parti3-on-tarama.py` · **Tarih:** 2026-09-20  
**Girdi:** `data/plan/v6-parti3.jsonl` · **60** satır

⛔⛔ T192: `v6-parti1 #29` **dört kapının dördünü de** geçmişti. T199: `#54`'ü yakalayan şey sınıfı değil **mesajıydı**. ➡️ *Bir süzgeç yalnız kendi sözlüğünü tanır; tohum metni okunmadan üretime girmez.*

| | |
|---|---:|
| işaret taşıyan satır | **14** / 60 |
| — yalnız `risk_seviyesi` alanından | 14 |
| ⛔ **içerik/beyan süzgeci ateşleyen** | **0** |
| ⛔ **üretilmeyecek satır** | **0** |

⭐ **Hiçbir içerik ya da beyan süzgeci ateşlemedi.** İşaretlerin hepsi `risk_seviyesi=yuksek` alanından geliyor ve bu alan tek başına eleme ölçütü değil (SERT eşiği `cok_yuksek`). ⛔ Yine de **on dördünün de tam metni okundu** — T192'nin dersi tam buydu.

## İşaretli satırlar — hepsi elle okundu

| # | tür / senaryo | işaret | hüküm |
|---:|---|---|---|
| 4 | `dijital` / `belirsiz` | risk:yuksek | ⭐ okundu, kriz yok |
| 5 | `tutun` / `belirsiz` | risk:yuksek | ⭐ okundu, kriz yok |
| 7 | `kumar` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 14 | `receteli_ilac` / `rol_siniri` | risk:yuksek | ⭐ okundu, kriz yok |
| 24 | `alkol` / `belirsiz` | risk:yuksek | ⭐ okundu, kriz yok |
| 27 | `alkol` / `ambivalans` | risk:yuksek | ⭐ okundu, kriz yok |
| 33 | `alkol` / `nazikce_karsi_cikma` | risk:yuksek | ⭐ okundu, kriz yok |
| 36 | `alkol` / `ambivalans` | risk:yuksek | ⭐ okundu, kriz yok |
| 39 | `receteli_ilac` / `rol_siniri` | risk:yuksek | ⭐ okundu, kriz yok |
| 42 | `kumar` / `ambivalans` | risk:yuksek | ⭐ okundu, kriz yok |
| 44 | `tutun` / `nazikce_karsi_cikma` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 54 | `alkol` / `rol_siniri` | risk:yuksek | ⭐ okundu, kriz yok |
| 57 | `kumar` / `nazikce_karsi_cikma` | risk:yuksek | ⭐ okundu, kriz yok |
| 59 | `receteli_ilac` / `ambivalans` | risk:yuksek | ⭐ okundu, kriz yok |

## ⚠️ Üretim notları — eleme değil, talimat

**`#7`** — ⚠️ ÜRETİM NOTU — kriz değil. *«tek vurgun ile kapatırım hepsini, çocuğumu da kaybetmem»* + **«Sen ne dersin»**: zararlı bir planın onaylanması doğrudan isteniyor. Onaylanmayacak ve karşı plan da verilmeyecek (ikisi de hüküm olur); `senaryo_hedefi` ne derse desin burada bir red var.

**`#44`** — ⚠️ ÜRETİM NOTU — kriz değil. Sıkıntıyı yaşayan **eşi** ve o burada değil (*«bir saat yatağın kenarında oturdu, gözleri kıpkırmızı»*). Eşin ne hissettiğine dair hüküm kurulmayacak — v6-parti2 `#58`'in aynı kuralı: ortada olmayan biri hakkında ikinci elden hüküm yok.

## ⛔ Bu taramanın söylemedikleri

| | |
|---|---|
| ⛔⛔ **«0 eleme» süzgeçlerin temiz olduğunu göstermez** | T192 tam tersini ölçtü: dördü de temiz derken kaçırmışlardı. Buradaki güvence süzgeç değil, **on dört metnin okunmuş olması** |
| ⛔ **Okuma BENİM okumam** | K30 gereği üretimi ben yapıyorum ve hükümleri de ben veriyorum; uzman okuması değil |
| ⛔ **`gd-021` açık** | çıplak *«İntihar düşüncesi»* sınıfı bu partiye düşmedi (havuzda 6 var); karar hâlâ verilmedi |
| ⚠️ **Yalnız tohum metni okundu** | üretilecek konuşmanın kendisi üretim anında ayrıca kapılardan geçer |
