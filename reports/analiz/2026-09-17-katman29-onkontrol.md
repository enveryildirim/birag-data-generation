# Katman 29 deneyi — kapsam önkontrolü

**Betik:** `scripts/analiz/2026-09-17-katman29-onkontrol.py` · **Tarih:** 2026-09-17

⛔ Bu deney `mlx_lm`'in belgelenmemiş bir yolunu kullanıyor (tam modül yolu + `num_layers: 0`). K49: sessiz eşleşmezlik **yanlış koşuyu doğru sandırır** ⇒ kapsam koşudan ÖNCE ölçülür.

| config | `num_layers` | **uygulanan katmanlar** | sayı | beklenen | |
|---|---:|---|---:|---|---|
| `u-k12` | 12 | `[30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]` | **12** | `30`… | ✅ |
| `u-k13` | 13 | `[29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]` | **13** | `29`… | ✅ |
| `p-atla29` | 0 | `[28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]` | **13** | `28`… | ✅ |
| `p-sadece29` | 0 | `[29, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]` | **12** | `29`… | ✅ |

## ⭐ Deneyin tasarımı — kapasite ile KATMAN ayrılıyor

| kol | katman | kapasite | soru |
|---|---|---:|---|
| `u-k12` | 30–41 | 12 | ölçüldü: **%46** |
| `u-k13` | 29–41 | 13 | ölçüldü: **%8** |
| ⭐ `p-atla29` | **28** + 30–41 | **13** | 13 katman ama **29 YOK** |
| ⭐ `p-sadece29` | **29** + 31–41 | **12** | 12 katman ama **29 VAR** |

➡️ *Kapasite (katman sayısı) ile kimliğin (hangi katman) etkisi ancak ikisi ÇAPRAZLANIRSA ayrılır: 13 katman 29'suz ve 12 katman 29'lu.*

| sonuç | çıkarım |
|---|---|
| `p-atla29` ≈ %46 **ve** `p-sadece29` ≈ %8 | ⭐ **katman 29** |
| `p-atla29` ≈ %8 **ve** `p-sadece29` ≈ %46 | ⭐ **kapasite**, katman değil |
| ikisi de ≈ %46 ya da ikisi de ≈ %8 | ⛔ ikisi de değil — başka bir şey |
| karışık | ⛔ tek yönlü okuma yok |

⭐ **Tahmin koşudan ÖNCE yazıldı:** `p-atla29` ≈ %46, `p-sadece29` ≈ %8 (yani katman 29 hipotezi).
