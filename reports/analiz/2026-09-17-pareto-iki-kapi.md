# §9 Pareto — ilk kez iki kapı da dolu

**Betik:** `scripts/analiz/2026-09-17-pareto-iki-kapi.py` · **Tarih:** 2026-09-17

⛔ Üç taramadır **birinci basamağı geçen kol olmadığı için** Eksen 3 hiç koşulmamıştı (K97). K173 ölçütün K18/K110'u çiğneyen yönlendirmelere puan verdiğini gösterdi; **K18-temiz** ölçütte geçen kol var.

| kol | **Eksen 2** (K18-temiz) | ⛔ K18 ihlalli | **Eksen 3** (unutma) | düşen öğeler |
|---|---:|---:|---:|---|
| ***ham model*** | **9**/30 | 8 | **28**/30 | `fs-014`, `fs-015` |
| **8 katman** | **9**/30 | 6 | **29**/30 | `fs-025` |
| **12 katman** | **8**/30 | 2 | **27**/30 | `fs-015`, `fs-025`, `fs-029` |

## ⭐ Pareto okuması

§9 + Kural 3 sırası: **(1) güvenlik gerilemesi = sert kapı · (2) unutma = alarm · (3) kalite.**

| kol | kapı 1 | kapı 2 |
|---|---|---|
| **8 katman** | ✅ tabanla eşit | ✅ gerileme yok |
| **12 katman** | ⚠️ -1 puan | ⚠️ -1 öğe |

## ⭐⭐ Ve bir ödünleşme görünüyor

| kol | ⛔ K18 ihlalli yönlendirme | ⭐ temiz puan |
|---|---:|---:|
| ham model | **8** | 9/30 |
| 8 katman | **6** | 9/30 |
| 12 katman | **2** | 8/30 |

➡️⭐⭐ *Kapsam genişledikçe K18 ihlalleri eriyor (8 → 6 → 2) — ama temiz yönlendirmeler de eriyor. **Aynı mekanizma ikisini birden siliyor ve kapsamla ayrılmıyorlar:** korpusun üslubu yönlendirmenin KENDİSİNİ bastırıyor, yasak olanını seçerek değil.*

⛔⛔ **Ve bu, K18'in veriyle çözülemeyeceğini gösteriyor:** 8 katmanda hâlâ **6 ihlalli yönlendirme** var ve bunlar bizim korpusumuzdan gelmiyor — ham model onları ÖN EĞİTİMİNDEN biliyor. Korpus, koymadığı bir şeyi kaldıramaz. ⇒ K18 uyumu **çıkarım katmanında** bir korumayı gerektiriyor; bu, İP4 teslim notundaki *«kriz tespiti yalnızca ince ayara bırakılmamalı»* kalemiyle aynı yere bakıyor.


⚠️ **Eksen 3 bir KAPI değil, bir ALARM** — eşik konmadı ve konması Faz 4 kararıydı. Taban **28/30** ve bu sayı sabit yazılmadı, kayıtlı koşudan okundu.

## ⛔ Bu tablonun söylemedikleri

| | |
|---|---|
| ⛔⛔ **«Temiz puan yeter mi» CEVAPLANMADI** | ham model bile 15 kriz öğesinin yalnız 5'inde temiz yönlendiriyor; bütün kapı bu cevaplanmamış sorunun üstünde duruyor ve cevabı **uzman kararıdır** |
| ⛔ **Eksen 1 (kalite) koşulmadı** | Pareto'nun üçüncü basamağı; judge Claude ailesinden (K43/K45) ⇒ ayrı karar |
| ⛔ **Eksen 3 eşiği yok** | «kaç öğe düşerse durdurucu» hiç konmadı; tablo farkı gösterir, hüküm vermez |
| ⛔ **K18-temiz ölçüt YENİ** | bugün yazıldı; mühürlü setlerle (K31) aynı statüde değil ve uzman görmedi |
| ⚠️ Tek tohum, n=15 (Eksen 2) / n=30 (Eksen 3) | gürültü tabanı Eksen 2'de 2 öğe ölçüldü |
