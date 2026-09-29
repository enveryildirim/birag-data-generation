# Korunum okumalarında `uydurma` dökümü (T302 · T303)

**Betik:** `scripts/analiz/2026-09-29-korunum-uydurma-dokumu.py` · **Tarih:** 2026-09-29  
**Girdi:** `data/candidates/v011-faz2.korunum.jsonl` SHA256-16 `467c1758923cc887` · 1149 okuma satırı (`karar-korunumu.v1` 1145, `karar-korunumu.v2` 4)  
⚠️ Depo, metni sonradan değişen kayıtların **eski** okumalarını da saklar (bayat okumalar silinmez); sayılar okuma satırıdır, kayıt değil.

## 1. `uydurma` işaretli okumalar

`karar-korunumu.v1`: **7/1145** okuma `uydurma` taşıyor · gerekçesinde **cevabı** anan: **3**

| no | rubrik | metin SHA | gerekçe cevabı anıyor | işaretlenen parça |
|---|---|---|---|---|
| 0050 | `karar-korunumu.v1` | `605831890be9df0d` | — | adam iki duygunun arasında sıkışmış, mesele adres değil |
| 0060 | `karar-korunumu.v1` | `cf5edeefafc628ac` | — | bırakmayı düşünmesi ve sonrasından korkması |
| 0111 | `karar-korunumu.v1` | `4102068c6cb27605` | — | bu onun kendi ilişkisi, benim yorumumu istemedi |
| 0168 | `karar-korunumu.v1` | `9969a7461a349b94` | ✅ | saatler telefonda geçiyor |
| 0920 | `karar-korunumu.v1` | `ba67f6643d0aa822` | ✅ | Asıl merak ettiği şey sorunun içinde duruyor: tamamen bırakmadan bu yo |
| 0991 | `karar-korunumu.v1` | `7bfc36cdf72d8898` | ✅ | sigara bırakma poliklinikleri / söylenilen şey sigaranın kendisi mi, k |
| 21 | `karar-korunumu.v1` | `c7ed37483078601d` | — | ilk kez böyle bir şey yaşayan biri genelde eşiğin yüksekliğinde geri ç |

## 2. #0920 — aynı paragrafa iki karşıt hüküm

Onarımdan önce (`7aa5f57`) ve sonra (`87a7b34`) yeni düşünmenin paragrafları; **iki sürümde birebir aynı paragraflar: [1, 3]**.

| okuma (metin SHA) | `uydurma` |
|---|---:|
| `ba67f6643d0aa822` | 1 |
| `df74d4f5a90246b4` | 0 |

⇒ `uydurma` işaretlenen 1. paragraf iki sürümde de aynıysa, iki okuma **aynı metne** zıt sert-kapı hükmü vermiştir (onarım yalnız 2. ve 4. paragrafa dokundu).

## ⛔ Bunun söylemedikleri

| | |
|---|---|
| ⛔ **Gürültü tabanı ölçülmedi** | tek bir kayıtta iki okuma; tasarlanmış bir iki-kör-okuyucu deneyi değil |
| ⚠️ **«Cevabı anıyor» sözcük eşlemesi** | gerekçede *cevap* sözcüğü aranır; okuyucunun cevabı dayanak saydığını değil, andığını gösterir |
