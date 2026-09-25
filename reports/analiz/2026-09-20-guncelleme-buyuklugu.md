# Puanı ne açıklıyor — kapasite mi, güncellemenin gerçek büyüklüğü mü

**Betik:** `scripts/analiz/2026-09-20-guncelleme-buyuklugu.py` · **Tarih:** 2026-09-20  
**Kaynak:** 24 adaptör (8 kol × 3 tohum), `runs/*/adapters/adapters.safetensors`  
**Güncelleme:** `(scale · lora_b.T) @ lora_a.T` — `mlx_lm/tuner/lora.py:52` ile birebir aynı ifade

⭐⭐ Yapılandırma alanlarını (`rank`, `scale`) tartışmak yerine, onların **ürettiği niceliği** ölçüyoruz: ağırlıklara gerçekte ne kadar dokunulduğu. `rank` ile `scale` iç içe; `‖ΔW‖` değil.

## 1. ⭐⭐⭐ Kollar, güncelleme büyüklükleri ve dereceli puan

| kol | kapsam | modül | ‖ΔW‖ toplam | modül başına | **dereceli** |
|---|---|---:|---:|---:|---:|
| **h1** | 8 kat · q · r8 · s20 | 8 | 10.4 | 3.66 | **16.33** |
| **h7** | 24 kat · q+o · r16 · s20 | 48 | 18.5 | 2.65 | **7.33** |
| **h8** | 24 kat · q+o · r16 · **s10** | 48 | 10.5 | 1.50 | **4.00** |
| **h2** | 16 kat · q · r8 · s20 | 16 | 12.1 | 3.00 | **2.00** |
| **h5** | 16 kat · q+o · r8 · s20 | 32 | 13.1 | 2.29 | **2.00** |
| **h6** | 24 kat · q+o · r8 · s20 | 48 | 14.0 | 2.00 | **1.33** |
| **h3** | 24 kat · q · r8 · s20 | 24 | 13.0 | 2.62 | **0.67** |
| **h4** | 32 kat · q · r8 · s20 | 32 | 14.5 | 2.52 | **0.67** |

| ilişki | Pearson r |
|---|---:|
| ‖ΔW‖ **toplam** ↔ dereceli puan | **-0.21** |
| ‖ΔW‖ **modül başına** ↔ dereceli puan | **+0.62** |
| **modül sayısı** ↔ dereceli puan | **-0.39** |

◐ **Tek bir nicelik puanı açıklamıyor** — toplam r=-0.21, modül başına r=+0.62, modül sayısı r=-0.39. ➡️ *Bu, «kapasite mi adım mı» sorusunun yanlış kurulmuş olabileceğini düşündürür: iki nicelik de tek başına sıralamayı vermiyor.*

## 2. ⭐⭐⭐ Tasarlanmamış doğal deney — eşit enerji, farklı yayılım

Toplam `‖ΔW‖` birbirine en yakın olup puanı en çok ayrılan çift aranır: toplam enerji eşitlenmişken geriye **yayılım** kalır.

| | h1 | h8 |
|---|---:|---:|
| kapsam | 8 kat · q · r8 · s20 | 24 kat · q+o · r16 · **s10** |
| ‖ΔW‖ **toplam** | 10.4 | 10.5 |
| dokunulan **modül** | 8 | 48 |
| **modül başına** | 3.66 | 1.50 |
| **dereceli puan** | **16.33** | **4.00** |

⭐⭐⭐ **Toplam enerji neredeyse aynı (10.4 ↔ 10.5) ama puan +12.33 ayrılıyor** (eşik 3.9 ⇒ **ayırt edilebiliyor**). Aradaki tek yapısal fark **yayılım**: 8 modül ↔ 48 modül. ➡️⭐⭐⭐ *Belirleyici olan ağırlıklara NE KADAR dokunulduğu değil, o dokunuşun NEREYE YAYILDIĞI. Aynı enerjiyi az sayıda yere yoğunlaştırmak kriz davranışını koruyor, çok sayıda yere dağıtmak bozuyor.*

⛔ **Bu çift TASARLANMADI**, tabloda bulundu ⇒ seçim sonradan yapıldı (post-hoc). Hipotez olarak güçlü, kanıt olarak zayıf: doğrulamak için yayılımı ÖNCEDEN değiştiren bir kol koşulmalı (örneğin 8 kat · q+o · r16, aynı toplam enerji, iki katı modül) — koşulmadı.

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔⛔ **§2'nin çifti post-hoc seçildi** | tabloya bakıp en ayrık çift alındı; önceden ilan edilmiş bir karşılaştırma değil |
| ⛔⛔ **n=8 kol** | korelasyon sekiz noktadan; bir eğilim işareti, ölçülmüş bir yasa değil |
| ⛔⛔ **Korelasyon nedensellik değil** | `‖ΔW‖` ile puan birlikte değişiyor; hangisinin ötekini ürettiği bu ölçümde YOK |
| ⛔ **Frobenius normu bir seçim** | başka bir norm (spektral, katman bazında ağırlıklı) başka sıralama verebilir; seçim önceden ilan edildi |
| ⛔ **Yalnız son kontrol noktası** | epok içi yörünge ölçülmedi |
| ⚠️ **Dereceli ölçüt doğrulanmış değil** | anahtar sözcük listesi (T186) |
