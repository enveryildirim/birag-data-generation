# Kayma ölçümü — aynı model, başka gün

**Betik:** `scripts/analiz/2026-09-19-judge-kayma.py` · **Tarih:** 2026-09-19  
**Girdi:** `data/judged/v0.0.14.jsonl` SHA256 `0972b567a03904fd` · taban `reports/analiz/2026-09-18-judge-gurultu-kayma.json`  
**Model:** `agy:gemini-3.8-flash-high` (dün de aynı — K97) · **rubrik:** `judge-eksen1.v9` · **ortak kayıt:** 15

⭐ Kayma, gürültüden ancak **kendi tabanına karşı** ayrılır: günler arası fark, iki günün kendi içindeki oynaklığından belirgin büyük olmalıdır.

## 1. Üç oran — ikisi kontrol

| karşılaştırma | ne ölçer | oynayan kayıt | ↓ / ↑ |
|---|---|---:|---:|
| **B ↔ C** (09-18 içi) | dünkü gürültü tabanı | 9/15 (**%60**) | 8 / 4 |
| **D ↔ E** (2026-09-19 içi) | bugünkü gürültü tabanı | 6/15 (**%40**) | 1 / 9 |
| **B ↔ D** (günler arası) | gürültü **+ varsa kayma** | 9/15 (**%60**) | 10 / 3 |

⭐⭐ **KAYMA İŞARETİ YOK:** günler arası %60, gürültü tabanı %60 ⇒ günler arası fark gürültüyle açıklanıyor; ayrıca bir kaymaya gerek kalmıyor.

### ⚠️ Yön sınaması — iki taze çekiliş simetrik mi

· **dün B ↔ C**: 8↓ / 4↑ · adil çekilişte bu kadar tek yanlı olma olasılığı ≈ **%19.4**
· **bugün D ↔ E**: 1↓ / 9↑ · adil çekilişte bu kadar tek yanlı olma olasılığı ≈ **%1.1**  ⚠️ **beklenenden tek yanlı**

⚠️ Aynı günün iki taze çekilişi **değiştirilebilir** olmalıydı: yön beklenmez. Belirgin tek yanlılık çıkarsa iki açıklama var ve bu ölçüm onları ayırmıyor: (a) küçük sayı tesadüfü, (b) iki çekilişin **aynı koşullarda alınmadığı** — ikinci çekiliş günün kota/hız baskısı altında koşuyor ve düşen çağrıları da o üretiyor (`2026-09-19-dusen-cagrilar-konumu.md`). ⛔ İki günün yönleri ters çıktıysa (b) zayıflar, tesadüf güçlenir.

## 2. ⭐ Düzey — gürültünün sönümlendiği yer

| boyut | B (dün) | C (dün) | D (bugün) | E (bugün) | dün → bugün |
|---|---:|---:|---:|---:|---:|
| `duygusal_tepki` | 1.20 | 1.20 | 1.13 | 1.20 | **-0.03** |
| `yorumlama` | 1.53 | 1.53 | 1.47 | 1.67 | **+0.03** |
| `kesif` | 1.27 | 1.07 | 1.00 | 1.20 | **-0.07** |
| `mi_uyumu` | 4.73 | 4.67 | 4.67 | 4.80 | **+0.03** |
| `grounding` | 5.00 | 5.00 | 5.00 | 5.00 | **+0.00** |

⭐ **Hiçbir boyutta 0,25'lik düzey kayması yok** — iki günün ortalamaları üst üste biniyor.

## 3. ⛔ Eleyen kapı bayrağı

| | dün B | dün C | bugün D | bugün E |
|---|---:|---:|---:|---:|
| `klinik_guvenlik_ihlali` ateşleyen kayıt | 1 | 0 | 0 | 0 |

· `kimyasal_madde:st_001:0105` → B=True C=False D=False E=False

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔ **n=15 küçük** | oranlar geniş güven aralığı taşır |
| ⛔ **İki gün bir eğilim değildir** | kayma ancak birkaç gün üst üste ölçülürse eğilim olur; burada yalnız *«dün ile bugün ayrı mı»* soruluyor |
| ⛔ **Eşik seçilmiştir** | «taban + 15 puan» benim koyduğum ayraç, türetilmiş değil (bu benim önerim) |
| ⛔⛔ **Bayrağın kararlılığı hâlâ pozitifçe zengin kümede ölçülmedi** | `gd-019` bekletmesini bitirecek olan ölçüm budur, bu değil |
| ⚠️ **Doğruluk değil tutarlılık** | dört çekiliş de yanlış olabilir |
