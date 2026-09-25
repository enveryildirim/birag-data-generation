# K46'nın üç metriği koda girdi — biri kapı oldu, ikisi olmadı

**Betik:** `scripts/analiz/2026-09-16-k46-metrikleri.py` · **Tarih:** 2026-09-16  
**Girdi:** `src/checks.py` SHA256 `d7f05d2fff7c5d95` (metrikler **çağrılıyor**)  
**Girdi:** `src/smoke_checks.py` SHA256 `e8afafb95a8e7ee1` (dil dedektörü **oradan**, kopyalanmıyor)  
**Girdi:** korpus — **2680** thinking taşıyan asistan turu

---

## 1. Üç metrik ve birimleri

| metrik | tanım | birim |
|---|---|---|
| `thinking_dili` | `smoke_checks._dil` — Türkçeye özgü harf + işlev sözcüğü sayımı | sınıf (`tr`/`en`/`belirsiz`) |
| `thinking_completion_orani` | thinking ÷ completion | **kelime** |
| `kullaniciya_giden_pay` | completion ÷ (thinking + completion) | **kelime** |

⚠️ **Birim KELİME, token değil.** K46'nın *«~14x uzun»* ölçümü de kelimeyle
yapılmıştı (`2026-09-12-thinking-dili-raporu.py`, `len(t.split())`); birim
değişirse sayılar **karşılaştırılamaz** (Kural 5).

---

## 2. ⭐ Planın ŞARTI — vekil kapının yanlış pozitif oranı

`plan.md` dil tespitinin sert kapı olmasını **ölçüme bağlamıştı**. Korpusun
tamamı Türkçe yazılmış (K50: thinking Türkçe yazılmaya devam) ⇒ `en` ya da
`belirsiz` çıkan **her** kayıt bir yanlış pozitif adayıdır.

| sınıf | kayıt |
|---|---:|
| `tr` | 2680 |

⭐ **Yanlış pozitif: 0/2680.**

---

## 3. Gerçek etikete karşı — ve ⛔ kanıtın zayıf tarafı

`reports/analiz/thinking-dili-ogrenilebilirlik/` K50'nin üst sınır koşusundan
**etiketli** thinking taşıyor: dar LoRA kolu İngilizce, geniş LoRA kolu Türkçe.

| dosya | beklenen | dedektör | |
|---|---|---|---|
| `dar-lora.jsonl` | `en` | {'en': 36} | ✅ **36/36** |
| `genis-lora.jsonl` | `tr` | {'tr': 36} | ✅ **36/36** |

⛔⛔ **YANLIŞ NEGATİF KANITI ZAYIF ve bu raporun en önemli şerhi.** İngilizce örnek sayısı **36** ama ⭐ ilk 40 karakterine göre **yalnızca 3 ayrık kalıp** var (en sık: *«Here's a thinking process that leads to …»* ×21).

➡️ *Yani dedektör İngilizceyi değil, **avuç içi kadar bir İngilizce**
***örneklemini** doğru sınıflandırdığı ölçüde sınanmış durumda — üstelik
*örneklerin çoğu tek bir şablondan geliyor. ⚠️ Yanlış pozitif tarafı geniş ve
çeşitli bir korpusla ölçüldü; yanlış negatif tarafı **tek bir şablonla**.*
⇒ Kapının **veri öldürme** riski ölçülü, **kaçırma** riski değil — ve
`plan.md`'nin şartı tam olarak birincisiydi.

---

## 4. ⭐⭐ Üç metrik, iki farklı karar

| metrik | karar | gerekçe |
|---|---|---|
| `thinking_dili` | ⭐ **SERT KAPI** (yalnızca BıRAG kayıtları) | planın şartı karşılandı: yanlış pozitif **0/2680**; korpus etkisi **0 kayıt** |
| `thinking_completion_orani` | ⛔ **yalnızca rapor** | **T7**: §4'ün *«sabit taban koyma»* dersi — sabit eşik dağılımı kendine çeker ve ölçtüğü şeyi bozar |
| `kullaniciya_giden_pay` | ⛔ **yalnızca rapor** | aynı gerekçe; tavanın veriyle nasıl öğretileceği `plan.md`'de **açık kalem** |

⚠️ **Kapı replay dilimine uygulanmıyor:** §9 replay verisinin İngilizce olması
**tasarım gereğidir** (çeşitlilik). ⭐ Bugün replay kayıtlarının hiçbirinde
thinking yok (**0/72**, ölçüldü) — kapı yine de kapsam dışı bırakıldı, çünkü
*koşul veriye değil TASARIMA dayanmalı; veri yarın değişir, tasarım kararı*
*yazılıdır.*

⭐ Kapı bugün **0 kayıt** eliyor. ⚠️ Yani bir **tuzak teli**:
bugün hiçbir şey yapmıyor, İngilizce thinking üretildiği gün yakalıyor.

➡️⭐⭐ *Aynı üç metrik aynı dosyaya girdi ve ikisi kapı olmadı. **Bir metriği**
***kapıya çevirmek, onu ölçmekten AYRI bir karardır** ve ayrı bir gerekçe*
*ister. Ölçüm «şu an şöyle» der; kapı «bundan sonra böyle olmayacak» der.*

---

## 5. Bugünkü dağılımlar — eşik DEĞİL, taban

| metrik | en düşük | %10 | ortanca | %90 | en yüksek |
|---|---:|---:|---:|---:|---:|
| `thinking_completion_orani` | 1.00 | 1.56 | **2.20** | 3.48 | 4.72 |
| `kullaniciya_giden_pay` | 0.17 | 0.22 | **0.31** | 0.39 | 0.50 |

⭐ Ortanca oran **2.20** — K50'nin *«~2x hedefi»*
civarında. ⛔ K46'nın **~14x**'i eğitilmemiş MODELİN ölçüsüydü, veri setinin
değil; ikisi karıştırılmamalı.

⚠️ **Bu sayılar bir eşik önerisi DEĞİL**, bugünkü tabandır. Eşik koymak T7'nin
uyardığı şeydir ve ayrı bir karar.

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔ **Yanlış negatif oranı** | 36 örnek, ~1 kalıp (§3). İngilizcenin çeşitliliği sınanmadı |
| ⛔ `belirsiz` sınıfı | korpusta hiç çıkmadı ⇒ **hiç sınanmadı**; çok kısa bir thinking'te ne olacağı bilinmiyor. ⚠️ Kapı `belirsiz`'i **geçiriyor** (`tr` gibi değil, `None` gibi değil — açıkça `tr` değilse eler) |
| ⛔ Oran ve pay için **eşik yok** | bilerek; T7'nin dersi |
| ⚠️ Birim **kelime** | token değil; tokenizer'a bağlı bir sayı istenirse yeniden ölçülmeli ve K46'nın sayısıyla karşılaştırılamaz |

