# `tuzak_uzman` — kusur ölçüsü mü, senaryo ölçüsü mü

**Betik:** `scripts/analiz/2026-09-17-tuzak-uzman-senaryo.py` · **Tarih:** 2026-09-17
**Kaynak:** v5-parti4..8 · rubrik `judge-eksen1.v9` · k=1 · 300 kayıt

⚠️ Judge Claude ailesinden (K43/K45) ⇒ **metrik değil**, veri revizyonu sinyali.

## 1. Kalıp hipotezi — ÇÜRÜDÜ

| | `tuzak_uzman`=doğru | =yanlış |
|---|---:|---:|
| «Bir şeye katılmıyorum» var | **12** | 38 |
| yok | **17** | 233 |

P(bayrak | kalıp) = **0.24** · P(bayrak | kalıp yok) = **0.07** ⇒ oran **3.5×**

⛔ Ama bayrakların **17/29**'ünde kalıp YOK ve kalıbın **38/50**'i bayraksız. ➡️ *Kalıp ne gerekli ne yeterli; eşlik ediyor, sürüklemiyor.*

## 2. Senaryo hipotezi

| senaryo | kayıt | bayrak | **oran** | itiraz bekleniyor mu |
|---|---:|---:|---:|:--:|
| `inkar` | 30 | 8 | **0.27** | ⭐ evet |
| `nazikce_karsi_cikma` | 54 | 14 | **0.26** | ⭐ evet |
| `borc_finansal` | 10 | 2 | **0.20** | — |
| `durtu` | 5 | 1 | **0.20** | — |
| `kayma_nuks` | 13 | 1 | **0.08** | — |
| `ambivalans` | 52 | 2 | **0.04** | — |
| `farkindalik` | 43 | 1 | **0.02** | — |
| `kutlama` | 1 | 0 | **0.00** | — |
| `hedef_belirleme` | 16 | 0 | **0.00** | — |
| `kayip_kovalama` | 5 | 0 | **0.00** | — |
| `hukuki_kaygi` | 8 | 0 | **0.00** | — |
| `rol_siniri` | 44 | 0 | **0.00** | — |
| `discord` | 1 | 0 | **0.00** | — |
| `anlasilmama` | 18 | 0 | **0.00** | — |

## 3. ⭐ Karar sayısı

| dilim | kayıt | bayrak | oran |
|---|---:|---:|---:|
| itiraz **beklenen** (`nazikce_karsi_cikma`, `inkar`) | 84 | 22 | **0.26** |
| ötekiler | 216 | 7 | **0.03** |

➡️ Oran farkı **8.1×**.

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔ **Nedensellik yok** | senaryo ile bayrak arasındaki ilişki gözlemsel; hangi senaryonun hangi tohumla eşleştiği rastgele değil, örneklem planından geliyor |
| ⛔ **Judge doğruluğu ölçülmedi** | bayrağın kendisi doğru mu, bunu ancak uzman söyler (K58 dilimi 50/70'te kapandı) |
| ⚠️ k=1 | tek okuma; judge'ın kendi içi tutarlılığı ölçülmedi |
| ⚠️ `ITIRAZ_BEKLENEN` listesi **benim okumam** | senaryo tanımlarından türetildi, rubrikte böyle bir sınıf yok |
