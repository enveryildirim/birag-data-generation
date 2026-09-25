# Dejenerasyon ön koşulu — mühür açılmadan İKİNCİ OKUMA

**Betik:** `scripts/analiz/2026-09-16-dejenerasyon-ikinci-okuma.py` · **Tarih:** 2026-09-16  
**Girdi:** `reports/analiz/golden-kosu/*/sonuclar.jsonl` — **23** arşivlenmiş koşu (yeniden koşu **YOK**)  
**Girdi:** `src/dejenerasyon.py` SHA256 `d3dceb85959a0bd4` (kapı **çağrılıyor**)

---

## Neden mühür açılmıyor

T82 dejenerasyon kapısını ekledi ama `golden_eval`'de **`on_kosul`'a koymadı**:
`tekrar` bayrağı cevabı **olan** kayıtları da yakalıyor ve onları ön koşula
eklemek `golden.locked` tabanının sayılarını **değiştirirdi** ⇒ K31 mührü.

⭐⭐ **Ama karar mühür açılmadan da verilebilir** — T62'nin yaptığı gibi:
mühürlü set ve yayımlanmış taban **hiç değiştirilmeden**, arşivlenmiş koşu
çıktıları üzerinde **iki okuma yan yana** hesaplanır. ⛔ Hiçbir dosya
değişmiyor, hiçbir sayı yeniden yayımlanmıyor.

---

## 1. İki okuma

| | |
|---|---:|
| hüküm taşıyan arşiv kaydı | **1043** |
| **A okuması** — bugünkü `gecti` (yayımlanmış) | **250** |
| **B okuması** — `tekrar` ön koşul olsaydı | **250** |
| ⛔ **hükmü çevrilen** (geçti → kalırdı) | **0** |
| ⚪ zaten kalmış, `tekrar` da yanıyor (karar etkilemez) | 19 |

✅ **Hiçbir hüküm çevrilmiyor.**

⭐⭐ **Karar böylece ucuzladı:** ön koşulu eklemenin yayımlanmış golden
sayılarına etkisi **sıfır** ⇒ mühür açıldığında bu değişikliği yapmak
tabanı **bozmaz**. ➡️ *Bir mührü açmadan önce, açtığında ne değişeceğini*
*bilmek mührün maliyetini düşürür: karar koşu sırasında değil, ÖNCEDEN*
*verilir ve koşu yalnızca uygular.*

---

## 2. Arşivde dejenerasyon dağılımı

| koşu | dejenere | toplam |
|---|---:|---:|
| `20260915-143755-gd2-B-derin` | **11** | 48 |
| `20260915-122021-gd-B-derin` | **10** | 48 |

## ⛔ Bu okumanın söylemedikleri

| | |
|---|---|
| ⛔ **Mühür AÇILMADI** | hiçbir eval seti ve hiçbir yayımlanmış sayı değiştirilmedi; bu rapor yalnızca *«açıldığında ne olacak»*ı söylüyor |
| ⛔ **Karar verilmedi** | ön koşulun eklenip eklenmeyeceği hâlâ bir karar; bu okuma onu **ucuzlatıyor**, yerine geçmiyor |
| ⚠️ Yalnızca `golden-kosu` arşivi | Eksen 2/3/4/5 koşuları ayrı dizinlerde ve bu okumaya **dahil değil** |
| ⚠️ `tekrar` eşiği **tek koldan** kalibre (T82) | B okuması o eşiğe bağlı |

