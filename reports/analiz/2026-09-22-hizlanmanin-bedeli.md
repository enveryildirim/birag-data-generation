# Hızlanmanın bedeli — `v6-parti8`'in uydurma oranı

**Betik:** `scripts/analiz/2026-09-22-hizlanmanin-bedeli.py` · **Tarih:** 2026-09-22  
**Küme:** `v6-parti3`–`parti8`, 412 kayıt, hepsi `claude-sonnet-subagent` + rubrik v9  
**Ölçü:** `grounding == 2` · **permütasyon:** 20000, tohum 20260922  

⛔⛔ **Tasarım sayılardan önce yazıldı** (betiğin başında). İşlem grubunda **tek parti** var ⇒ *«hızlanma»* parti8'e özgü her şeyle tam karışıktır; hiçbir istatistik bunu ayıramaz.

## Parti oranları

| parti | uydurma | oran | %95 Wilson |
|---|---:|---:|---|
| `v6-parti3` | 9/60 | %15.0 | %8.1–%26.1 |
| `v6-parti4` | 10/59 | %16.9 | %9.5–%28.5 |
| `v6-parti5` | 2/60 | %3.3 | %0.9–%11.4 |
| `v6-parti6` | 1/58 | %1.7 | %0.3–%9.1 |
| `v6-parti7` | 7/57 | %12.3 | %6.1–%23.2 |
| `v6-parti8` ⭐ **hızlandırılmış** | 22/118 | %18.6 | %12.6–%26.6 |

## ⭐⭐⭐ BİRİNCİL DENETİM — kontrol partileri kendi aralarında

Hızlandırılmamış beş parti **%1.7** (`v6-parti6`) ile **%16.9** (`v6-parti4`) arasında değişiyor. parti8: **%18.6**.

⭐ parti8 kontrol yayılımının **dışında** — ama bu tek başına nedensellik kurmaz; aşağıdaki karıştırıcı denetimine bakın.

⛔ Kontrol partileri **kendi aralarında homojen değil**: G = 14.9, sd = 4, p = **0.0050** ⇒ *«kontrol»* tek bir taban değil, bir **dağılım**. Havuzlanmış tek bir kontrol oranıyla karşılaştırma bu yüzden yanıltıcıdır.

## İkincil sınamalar

| sınama | sonuç |
|---|---|
| (a) Fisher kesin, parti8 ↔ havuzlanmış kontrol (22/118 ↔ 29/294) | p = **0.0199** |
| (b) Katmanlı permütasyon (risk × bağlam × tur) | fark +8.8 puan, p = **0.0244** |
| ⭐⭐ **(c) KÜME düzeyinde (birim = parti)** | parti8, 6 partinin **1.** en yüksek oranlısı ⇒ H₀'da p = **0.167** |

⛔⛔⛔ **(a) ve (b) kayıtları BAĞIMSIZ sayıyor ve bu varsayım ÖLÇÜLEREK ÇÜRÜDÜ:** kontrol partileri kendi aralarında homojen değil (G = 14.9, p = 0.0050) ⇒ aşırı yayılım var, kayıt düzeyli p'ler **anti-muhafazakârdır** (gerçekte olduğundan küçük çıkar). Değişkenlik parti düzeyinde olduğu için doğru birim **parti**'dir ve o birimle fark **anlamlı değildir**.

## Riskin sonuçla ilişkisi

⭐ T233 riski bir karıştırıcı diye işaret etmişti. Ölçüldü:

| tohum riski | uydurma |
|---|---:|
| dusuk | 2/14 = %14.3 |
| orta | 32/242 = %13.2 |
| yuksek | 17/156 = %10.9 |

| parti | yüksek risk payı | uydurma |
|---|---:|---:|
| `v6-parti3` | %23 | %15.0 |
| `v6-parti4` | %56 | %16.9 |
| `v6-parti5` | %30 | %3.3 |
| `v6-parti6` | %21 | %1.7 |
| `v6-parti7` | %58 | %12.3 |
| `v6-parti8` | %39 | %18.6 |

⛔ **Risk, parti sıralamasını açıklamıyor:** en yüksek riskli iki parti (`parti7` %58, `parti4` %56) uydurmada 3. ve 2. sırada, en düşük riskli `parti6` (%21) sonuncu — ama `parti3` de düşük riskli (%23) ve uydurmada 4. ⇒ ilişki tek yönlü değil. ⭐⭐ **Ve parti8'in yüksek risk payı (%39) kontrollerin ikisinden DÜŞÜK** ⇒ T233'ün işaret ettiği karıştırıcı parti8'in oranını **açıklamıyor**, tersine onun aleyhine çalışıyor.

## Karıştırıcılar gerçekten farklı mı

| değişken | parti8 | kontroller |
|---|---:|---:|
| bağlam | %24.6 | %25.2 |
| çok tur | %39.8 | %39.8 |
| **yüksek risk** | %39.0 | %37.4 |

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔⛔⛔ **İŞLEM GRUBUNDA TEK PARTİ VAR** | *«hızlanma»* parti8'in planı, tohumları, boyu ve tarihiyle **tam karışıktır**. Ayırmanın tek yolu: aynı yöntemle **ikinci bir hızlandırılmış parti** üretmek ve kontrol partisi yanına koymak (T61'in şartı: her iki tasarımda da yinelenen geçiş) |
| ⛔⛔ **Ölçü bir ALT SINIR** | `grounding` tek-ayrıntı sondasıdır (T238); partiler arası karşılaştırma ancak sondanın darlığı her partide **aynıysa** geçerli ve bu **sınanmadı** |
| ⛔ **Uydurma ≠ kalite** | ölçülen tek şey, judge'ın adlandırdığı ayrıntının konuşmada bulunup bulunmadığı |
| ⚠️ **Judge sabit ama üretici değil** | parti3–7'yi ben yazdım, parti8'in taslağını alt ajanlar; okuma ve kapılar hepsinde bende |
