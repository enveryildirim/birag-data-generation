# Golden eval bölmesi — K31 mührü

**Girdi:** `data/seeds.jsonl` · SHA256 `0631c02ec7510af35bcd5b229c306c1688afbe1d4471c0c2de5c176ed7b42485`  
**Betik:** `scripts/analiz/2026-09-14-golden-bolme.py` · **Tarih:** 2026-09-14  
**Çıktı:** `evals/bolme.json` · **Tuz:** `birag-golden-2026-09-14`

---

## 0. Neden bölme öğelerden önce

K31 `dev`in oyunlanmasını bekler, `test` ve `locked`ın oyunlanmamasını şart koşar. Üç seti sırayla yazsaydım mühür sahte olurdu: dev'de modelin nerede düştüğünü gördükten sonra test öğelerini yazarken o bilgi elime bulaşırdı. Bölme bu yüzden **tek bir öğe yazılmadan önce** ve seed_id hash'inden sabitlendi — benim seçimimden değil. Bir dilime öğe yazarken yalnızca o dilimin havuzundan tohum çekilebilir.

## 1. Havuz

| | Tohum |
|---|---:|
| `data/seeds.jsonl` toplam | 2240 |
| − elendi: risk_seviyesi | 759 |
| − elendi: üretimde kullanılmış | 235 |
| − elendi: senaryo | 40 |
| − elendi: kriz içeriği | 3 |
| **Eksen 1 golden havuzu** | **1203** |

> Elenenlerin çoğu `risk_seviyesi` yüzünden. **Bu bir kapsama açığıdır, kusur değil:** kriz ve yüksek risk Eksen 2'nin konusu ve protokolü uzman Oturum 1'e bağlı (Kural 3). golden.dev sınır davranışını ÖLÇMEZ; `evals/safety_crisis.jsonl` bekliyor.

## 2. Dilim dağılımı

| Dilim | Tohum | Oran | Hedef |
|---|---:|---:|---:|
| `dev` | 596 | %49.5 | %50 |
| `test` | 291 | %24.2 | %25 |
| `locked` | 316 | %26.3 | %25 |

## 3. Senaryoya göre çapraz

| Senaryo | dev | test | locked | toplam |
|---|---:|---:|---:|---:|
| `ambivalans` | 273 | 135 | 153 | 561 |
| `belirsiz` | 137 | 68 | 72 | 277 |
| `inkar` | 10 | 4 | 3 | 17 |
| `nazikce_karsi_cikma` | 95 | 48 | 52 | 195 |
| `rol_siniri` | 81 | 36 | 36 | 153 |

> `kriz`, `sanrili_soylem` ve yüksek risk havuzda YOK — §1'deki eleme. `inkar`, `discord`, `kayma_nuks` havuzda çok az; bu senaryolarda öğe gerekiyorsa **elle yazılacak** ve kaynağı öyle işaretlenecek.

