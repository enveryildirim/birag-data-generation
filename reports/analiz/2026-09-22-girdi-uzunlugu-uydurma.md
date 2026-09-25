# Uzun kullanıcı girdisi uydurmadan koruyor mu?

**Betik:** `scripts/analiz/2026-09-22-girdi-uzunlugu-uydurma.py` · **Tarih:** 2026-09-22  
**Küme:** `data/judged/v0.0.18.jsonl` · 1089 yargılı, replay dışı  
**Birim:** ilk kullanıcı mesajı, bağlam çıkarılmış (T231) · permütasyon 20000  

⭐ T243 bunu keşifsel bölümünde işaret etmişti (`bicim = uzun`, −12,7 puan) ama çokluk yüzünden bulgu saymamıştı; burada **2,6 kat büyük** kümede ve **girdi uzunluğu doğrudan ölçülerek** yineleniyor.

## Ölçüm

| girdi dilimi | uydurma | oran | %95 Wilson |
|---|---:|---:|---|
| **kısa** (≤8 sözcük) | 26/397 | %6.5 | %4.5–%9.4 |
| **orta** (≤26 sözcük) | 28/343 | %8.2 | %5.7–%11.5 |
| **uzun** (>26 sözcük) | 4/349 | %1.1 | %0.4–%2.9 |

**uzun ↔ öteki: -6.2 puan · p = 0.0000 · 6.4 kat fark.** Güven aralıkları **çakışmıyor**.

⛔ İlişki **tek yönlü değil**: kısa %6.5 ↔ orta %8.2 arasında fark yok; ayrılan şey **uzun** dilim. ⇒ *«Seyrek girdi uydurma ÜRETİR»* değil, *«zengin girdi uydurmayı BASTIRIR»* biçiminde okunmalı.

## ⛔⛔ Alternatif açıklama — ölçüyle ayrılamıyor

`grounding` bir **tek-ayrıntı sondasıdır** (T238): judge bir ayrıntı adlandırır, kod onu konuşmada **arar**. ⇒ Kullanıcı metni uzadıkça adlandırılan ayrıntının orada **rastlantısal olarak bulunma olasılığı da artar.**

| girdi dilimi | ort. cevap (sözcük) | ort. adlandırılan ayrıntı |
|---|---:|---:|
| kısa | 47 | 6.4 |
| orta | 49 | 6.0 |
| uzun | 51 | 6.4 |

⚠️ Cevap uzunluğu dilimler arasında benzer kalıyorsa *«judge daha çok yazdığı için tutturuyor»* açıklaması zayıflar; ama **arama yüzeyi** (kullanıcı metni) tanımı gereği uzun dilimde daha büyük ⇒ **bu veriyle ayrılamaz.**

⭐ **Ayıracak ölçüm:** aynı cevaplar, kullanıcı metni **kısaltılmış** bir kopyayla yeniden puanlanır; sonda kolaylaşması tek başına etkiyi üretiyorsa oran oynar. *Bu benim önerim*, koşulmadı.

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔⛔ **Nedensellik yok** | girdi uzunluğu üretim anında **tasarlanmış** bir değişken (`bicim` kotası); uzun girdili kayıtlar başka açılardan da farklı olabilir |
| ⛔⛔ **Sonda kolaylaşması ayrılamadı** | yukarıdaki bölüm; etkinin ne kadarının gerçek olduğu **bilinmiyor** |
| ⛔ **T13-D'yi KAPATMAZ** | o kalem MODEL tarafını soruyor (*«seyrek girdide uydurma artar mı»*); bu ölçüm **korpus** tarafında ve aynı sonda kusurunu taşıyor ⇒ destekleyici, belirleyici değil |
| ⚠️ **T243'ün çokluk şerhi kısmen kalkıyor** | bulgu önceden keşifseldi; **önceden belirtilmiş bir hipotez olarak** 2,6 kat büyük kümede yinelendi ⇒ güçlendi, ama aynı ölçütle |
