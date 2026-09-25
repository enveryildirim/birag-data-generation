# Yönlendirme payı — eğitim verisi, EVAL'İN ARACIYLA ölçüldü

**Betik:** `scripts/analiz/2026-09-17-yonlendirme-payi.py` · **Tarih:** 2026-09-17

**Ölçüt:** `evals/safety_crisis.duzeltilmis.jsonl`'in kabul listesi (11 terim) — kopyalanmadı, **setten okundu**.

| sürüm | kayıt | **yönlendirme adlandıran** | oran |
|---|---:|---:|---:|
| `v0.0.2` | 117 | **20** | %17.1 |
| `v0.0.3` | 155 | **23** | %14.8 |
| `v0.0.5` | 155 | **30** | %19.4 |
| `v0.0.6` | 214 | **42** | %19.6 |
| `v0.0.7` | 272 | **47** | %17.3 |
| `v0.0.8` | 571 | **96** | %16.8 |

## ⭐ Karşılaştırma noktası

Kapsam taraması `v0.0.5` üzerinde koştu: **30/155** kayıt (%19.4) yönlendirmeyi adlandırıyordu.
Üçüncü tarama `v0.0.8` üzerinde: **96/571** (%16.8).

➡️ Mutlak sayı **3.2 kat** arttı, oran **%19.4 → %16.8**.

⭐ **Bu sayı üçüncü taramanın yorumunu belirler:** kollar yine elenirse, *«veride yönlendirme az»* açıklaması bu artışla birlikte **zayıflar** ve sıradaki aday veri MİKTARI değil, ya verinin BİÇİMİ ya da ölçütün kendisi olur.

## ⛔⛔ VE ÖLÇÜM KENDİ GEREKÇESİNİ DOĞRULADI: İKİ ARAÇ ÇELİŞİYOR

K109/T26 şunu yazmıştı: *«v0.0.2'de yönlendirme HAMLESİ **0** kayıttaydı»*.
Eval'in kendi aracıyla aynı korpusta **20 kayıt** (%17.1) çıkıyor.

⛔ İki sayı da yanlış değil — **aynı şeyi ölçmüyorlar**. «Hamle» dar bir tanım (izin isteme + kaynak türü + ilk adım, §8b'nin biçimi); kabul listesi ise yalnız bir **kaynak türü sözcüğü** arıyor.

➡️⭐⭐ *Ve ince ayarlı modeli eleyen kapı, dar tanımı değil GENİŞ olanı kullanıyor: `safety_crisis` bir kaynak türü sözcüğü arıyor. Yani «veride hamle yok» gerekçesi, modelin elendiği ölçütle hiç karşılaştırılmamış. Veri ile model üç taramadır **ayrı terazilerde** tartılıyor.*

⚠️ Bu, önceki taramaların sonucunu geçersiz kılmaz — onlar modeli doğru ölçtü. Geçersiz olan, sonuca verilen **açıklama**.

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔ **Üst sınır** | kabul listesi SÖZCÜK arar; hamlenin yerinde olup olmadığını sormaz |
| ⛔ **Dağılım eşleşmiyor** | eval KRİZ bağlamında soruyor, eğitim verisinde kriz dilimi YOK (Kural 3) ⇒ iki dağılım aynı değil ve bu fark kapatılamıyor |
| ⛔ **Nedensellik yok** | veride payın artması modelin davranışını açıklamaz; yalnız bir açıklamayı zayıflatır |
| ⚠️ Yalnız SON asistan turu taranıyor | ara turlardaki yönlendirme sayılmıyor |
| ⛔ **«Hamle» sayımı yeniden yapılmadı** | K109'un dar tanımıyla v0.0.8'de kaç kayıt olduğu ölçülmedi; burada yalnız İKİ ARACIN ayrıştığı gösterildi |
