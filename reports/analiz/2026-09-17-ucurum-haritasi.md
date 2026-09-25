# Uçurum haritası — güvenlik davranışı hangi katmanda çöküyor

**Betik:** `scripts/analiz/2026-09-17-ucurum-haritasi.py` · **Tarih:** 2026-09-17

Yalnız **kriz** dilimi (15 öğe). Bütün kollar aynı korpusla (`v0.0.8`), aynı tohumla, aynı adımda (1368), aynı anahtarla (`q_proj`), aynı rank'la (8) eğitildi. **Değişen tek şey `num_layers`.**

| katman | kesilen | ham puan | **kesilmeyenlerde** | ort. thinking |
|---|---:|---:|---:|---:|
| ***ham model*** | 0 | 21/30 | **21/30 = %70** | 2313 |
| **8** | 0 | 19/30 | **19/30 = %63** | 1202 |
| **10** | 2 | 14/30 | **14/26 = %54** | 1615 |
| **12** | 3 | 11/30 | **11/24 = %46** | 1506 |
| ****13**** | 3 | 2/30 | **2/24 = %8** | 1499 |
| **14** | 7 | 2/30 | **1/16 = %6** | 2166 |
| **16** | 4 | 1/30 | **1/22 = %5** | 1611 |
| 16 · `max_tokens` **2048** | 3 | 1/30 | **1/24 = %4** | 2266 |

## ⭐⭐ İki karıştırıcı da ayrıldı

**(a) Kesilme düşürmüyor.** Kesilenler dışarıda bırakılınca eğri değişmiyor; ayrıca tanı koşusu 16 katmanı **iki katı token bütçesiyle** yeniden ölçtü:

| | `max_tokens` 1024 | `max_tokens` **2048** |
|---|---:|---:|
| kesilen | 4 | **3** |
| kesilmeyenlerde puan | %5 | **%4** |

➡️⭐⭐⭐ *Bütçeyi ikiye katlamak puanı oynatmadı. ⇒ **Çöküş kesilme değil, DAVRANIŞ.** Bir ölçüt düşerken iki sebep aynı anda büyüyorsa, hangisinin düşürdüğü ancak birini sabitleyerek görülür.*

**(b) Ve bu tek bir uçurum DEĞİL — iki ayrı rejim.**

| geçiş | fark |
|---|---:|
| 8 → 10 | -9 puan |
| 10 → 12 | -8 puan |
| **12 → 13** | **-38 puan** |
| 13 → 14 | -2 puan |
| 14 → 16 | -2 puan |

➡️⭐⭐ *En büyük düşüş **12 → 13** geçişinde: **-38 puan**. Öncesi kademeli bir aşınma, sonrası düz bir taban.*

⭐⭐ **13 katman sınırı keskinleştirdi:** %8. *Çöküş 13'ten ÖNCE — yani 12 ile 13 arasında.*

➡️ *Bir eşiği iki gözlemden okumak, aradaki eğrinin biçimini VARSAYMAK demektir; üçüncü gözlem o varsayımı sınar.*


## ⭐⭐⭐ Kapasite mi, katman 29 mu?

Üstten-N kolları kapasiteyi ve kimliği **birlikte** oynatıyordu. Bu iki kol onları çaprazlıyor: aynı korpus, aynı tohum, aynı adım, aynı rank.

| kol | katman | kapasite | 29 | **kesilmeyenlerde** |
|---|---|---:|:--:|---:|
| `u-k12` | 30–41 | 12 | ✗ | **%46** |
| `u-k13` | 29–41 | 13 | ✓ | **%8** |
| `atla29` | 28+30-41 | 13 | ✗ | **%29** |
| `sadece29` | 29+31-41 | 12 | ✓ | **%0** |

⭐ **Tahmin koşudan ÖNCE yazılmıştı:** `atla29` ≈ üst rejim, `sadece29` ≈ alt rejim (yani katman 29 hipotezi).

### ⛔ İkili hüküm yerine ETKİ BÜYÜKLÜĞÜ

⛔⛔ *«Tahmin tuttu/tutmadı» demek burada veriden temiz bir iddia kurardı: `atla29` **%29**, iki rejimin ortasına (%27) yalnız **+2 puan** uzak ve `u-k12`'nin %46'sından belirgin DÜŞÜK. ⇒ Tek bir eşikle okumak yerine 2×2'nin iki ana etkisi ayrı ayrı hesaplanır.*

| **katman 29 eklemenin** etkisi | kapasite sabit | fark |
|---|---|---:|
| 12 katmanda | %46 → %0 | **-46** |
| 13 katmanda | %29 → %8 | **-21** |

| **bir katman eklemenin** etkisi | 29 durumu sabit | fark |
|---|---|---:|
| 29 YOKken (12→13) | %46 → %29 | **-17** |
| 29 VARken (12→13) | %0 → %8 | **+8** |

➡️⭐⭐⭐ *Katman 29'un toplam etkisi **67 puan**, bir katman eklemenin **25 puan** — ve kapasitenin etkisi **işaret olarak tutarlı bile değil** (-17 ve +8). ⇒ **Belirleyen şey ağırlıklı olarak katman 29'un KİMLİĞİ**, ama kapasite de sıfır değil: 29'suz 13 katman, 29'suz 12 katmandan düşük.*

⛔ **«Kanıtlandı» demek için fazla dar:** `atla29` iki rejimin ortasında duruyor ve n=15, tek tohum. Söylenebilen şey: *29'u içeren iki kolun ikisi de tabanda (%8, %0); içermeyen ikisi de üstte (%46, %29) — ayrışma tutarlı ama aradaki boşluk dar.*


⚠️ Bu iki kol `num_layers` ile değil **tam modül yoluyla** kuruldu; kapsam koşudan önce ölçüldü (`2026-09-17-katman29-onkontrol.md`).

## ⛔ Bu haritanın söylemedikleri

| | |
|---|---|
| ⛔ **Sebep bilinmiyor** | 12 ile 14 arasında ne olduğu ölçülmedi; harita NEREDE olduğunu söyler, NEDEN olduğunu değil |
| ⛔ **Tek tohum** | üretim deterministik (K105) ama tohum tek; eşik tohumla oynayabilir |
| ⛔ **n = 15 kriz öğesi** | dilim büyütülemiyor (Kural 3: yeni kriz öğesi = kriz içeriği üretimi) |
| ⛔ **Kesilmenin SEBEBİ açıklanmadı** | 14 katmanda 7 öğe kesildi ve thinking orada uzuyor; ayrı bir kalem |
| ⛔ **Yalnız `q_proj`, rank 8** | `o_proj` ve rank ekseninde eşik ölçülmedi |
| ⚠️ **Derece ≠ kalite** | 2 almak «tür adlandı ve devretti» demek, «doğru yönlendirdi» değil |
| ⚠️ **Kesilmeyen alt küme yanlı olabilir** | kesilen öğeler rastgele değil; uzun cevap üretilen öğeler |
