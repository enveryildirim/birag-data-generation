# Unutma gerilemesinin sebebi — öge öge

**Betik:** `scripts/analiz/2026-09-22-unutma-gerilemesi.py` · **Tarih:** 2026-09-22  
**Ölçülen:** `forgetting_smoke` 30 öge · taban (adaptersiz) ↔ `d1-veri2x-k8qo-v018`, 8 tohum  
**Gerileme:** 28/30 → 26,75 ± 0,73 = **−1,25** (T254, okunabilir)  

## Net −1,25 neyin toplamı

| öge | kolda geçen | ne sınıyor |
|---|---:|---|
| ⛔ `fs-025` | **0/8** | aritmetik — «5×6, sonra +10, sadece son sayıyı yaz» → 40 |
| ⛔ `fs-029` | **1/8** | olgusal — «Kürk Mantolu Madonna»nın yazarı → Sabahattin Ali |
| ⛔ `fs-013` | **4/8** | aritmetik — sayı = 35 |
| ⛔ `fs-009` | **6/8** | liste/indeks sorusu |
| ⭐ `fs-014` | **8/8** (tabanda ❌) | çeviri — Türkçe→İngilizce |
| ⭐ `fs-015` | **3/8** (tabanda ❌) | Türkçe yanıt kipi |

⇒ **4 öge kaybedildi, 2 öge kazanıldı.** Net −1,25 bu ikisinin farkı.

## ⭐⭐⭐ Cevaplar okundu — iki ayrı kusur

### 1. Aritmetik: biçim doğru, hesap yanlış

`fs-025` — *«Önce 5 ile 6'yı çarp, sonra sonuca 10 ekle, sadece son sayıyı yaz»* ⇒ doğru cevap **40**.

| | cevap |
|---|---|
| taban | **40** ✅ |
| kol (8 tohum) | **60 · 60 · 70 · 70 · 70 · 70 · 60 · 70** ❌ |

⭐ Model **yalın sayı** veriyor — yani istenen biçimi tutturuyor. Bozulan **hesabın kendisi**. `fs-025` 8 tohumun 8'inde birden kayıp ⇒ gürültü değil, sistematik.

### 2. Olgusal bilgi: ad uyduruyor

`fs-029` — *«Kürk Mantolu Madonna»nın yazarı kimdir?*

| tohum | cevap |
|---|---|
| taban | **Sabahattin Ali** ✅ |
| t13 | Sabahattin Ali ✅ |
| t7 · t23 · t31 · t43 · t47 | **«Enem Şişmanoğlu» · «Enem Şişkin» · «Enem Şentürk» · «Enem Dereli» ×2** |
| t37 · t41 | «Dostoyevski» |

⛔⛔ **Model *«bilmiyorum»* demiyor, makul görünen bir ad UYDURUYOR.** ⭐ Ve sekiz tohumun **beşi** «**Enem** …» ile başlayan bir ad üretiyor — «Enem» Türkçede bir ad değil ve korpusta **hiç geçmiyor** (0 eşleşme) ⇒ doğrudan veri bulaşması değil. Beş bağımsız tohumun aynı yapıyı üretmesi **jeton düzeyinde bir çöküşe** işaret ediyor; mekanizması bu raporda **ölçülmedi**.

## Korpus bu kipleri hiç göstermiyor

`datasets/v0.0.18`'in 1033 son asistan cevabı:

| kip | kayıt | oran |
|---|---:|---:|
| rakam içeren | 9 | %1 |
| **yalın sayı cevabı** (≤3 sözcük) | **0** | **%0.0** |
| **aritmetik ifadesi** | **0** | **%0.0** |
| ortalama uzunluk | — | 49 sözcük |

⭐ Asistan tarafında **özel ad da yok**: en sık büyük harfli sözcükler cümle başı işlev sözcükleri (*Bir · Ama · Bunu*). Kullanıcı tarafında ise gerçek özel adlar geçiyor (*Instagram · İstanbul · Defne*) ⇒ asimetri **tasarım gereği** (K18/K110: kurum adları ağırlığa girmemeli).

➡️ **Korpus tek bir çıktı kipi öğretiyor:** ~49 sözcüklük yansıtıcı düzyazı; yalın sayı yok, aritmetik yok, özel ad yok.

## ⛔ Ne söylenebilir, ne söylenemez

| | |
|---|---|
| ⭐ **Söylenebilir** | gerileme **iki ayrı kusurdan** geliyor: aritmetik hesap ve olgusal ad. İkisinde de **biçim korunuyor, içerik bozuluyor** ⇒ bu bir *«kip daralması»* değil, **bilgi/işlem kaybı** |
| ⭐ **Söylenebilir** | korpus bu kipleri **hiç** göstermiyor (%0,0 yalın sayı, %0,0 aritmetik, ~0 özel ad) ⇒ ilişki var |
| ⛔⛔ **SÖYLENEMEZ: nedensellik** | korpusun bu kipleri göstermemesi ile kaybın **aynı şey olduğu gösterilmedi**. Aynı kaybı LoRA kapsamı da üretebilir (K174/K175: güvenlik davranışı 13 katmanda çöküyor; bu kol 8 katman) |
| ⛔ **Sınanmadı** | (a) korpusa az miktarda aritmetik/olgusal içerik ekleyen bir kol, (b) daha dar LoRA kapsamı. İkisi de ayrımı gösterirdi |
| ⚠️ **«Enem» olgusu açıklanmadı** | beş tohumda yinelenen bir sözde-ad; korpusta yok, mekanizması ölçülmedi |
| ⚠️ **30 öge küçüktür** | 4 kayıp / 2 kazanç; öge düzeyinde güven aralıkları geniştir |
