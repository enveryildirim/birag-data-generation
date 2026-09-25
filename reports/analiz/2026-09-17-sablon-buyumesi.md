# Şablon büyümesi — her yeni kural, bir sonraki şablonun tohumu

**Betik:** `scripts/analiz/2026-09-17-sablon-buyumesi.py` · **Tarih:** 2026-09-17

⛔ Judge, çıkmaz revizyonunu okurken not düştü: bir ret kalıbı beş kayıtta **neredeyse birebir** tekrarlanıyor ve hiçbir alan yakalamıyor (`klise_acilis` yalnız **kabul** cümlelerini soruyor).

| şablon | v0.0.2 | v0.0.5 | v0.0.6 | v0.0.7 | v0.0.8 |
|---|---:|---:|---:|---:|---:|
| «Bir şeye katılmıyorum» | **0** (%0.0) | **0** (%0.0) | **0** (%0.0) | **4** (%1.5) | **71** (%12.4) |
| «…olup olmadığını ben söyleyemem» | **0** (%0.0) | **0** (%0.0) | **0** (%0.0) | **2** (%0.7) | **11** (%1.9) |
| «buradan uydurmayacağım» | **0** (%0.0) | **0** (%0.0) | **0** (%0.0) | **2** (%0.7) | **4** (%0.7) |
| «benim işim değil» | **2** (%1.7) | **4** (%2.6) | **5** (%2.3) | **8** (%2.9) | **25** (%4.4) |
| «İlk adım … olabilir» | **0** (%0.0) | **0** (%0.0) | **2** (%0.9) | **5** (%1.8) | **24** (%4.2) |

## ⭐⭐ Desen: üçü de aynı biçimde büyüyor

➡️⭐⭐ *Üretici bir kuralı öğrendiğinde onu bir CÜMLEYE dönüştürüyor ve o cümle korpusta hızla büyüyor. Kural doğru, kalıp yanlış — ve kalıbı doğuran şey kuralın kendisi.* ⇒ **Her yeni kural, bir sonraki şablonun tohumu.**

⭐ Bugün yazılan kurallar (§5a‴, §5a⁗, §8b′, §8c′, §8d′) bu riski taşıyor ve §8c′ bunu zaten bir kez gösterdi: «Bir şeye katılmıyorum» kalıbı §8c'nin kendi ürünüydü.

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔ **Kapı YOK** | bu bir ölçüm; şablonlaşmayı yakalayan bir kapı yazılmadı |
| ⛔ **Kalıplar elle** (K30) | sayı ALT SINIR; sözlükte olmayan şablonlar görünmez |
| ⛔ **«Şablon = kusur» değil** | tekrarlanan bir cümle doğru da olabilir; ölçülen şey TEKRAR, yanlışlık değil |
| ⚠️ Sürümler arası karşılaştırma | korpus büyüdükçe yeni partilerin payı artıyor; oran bunu düzeltir, mutlak sayı düzeltmez |
