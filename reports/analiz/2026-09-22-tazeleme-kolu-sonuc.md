# Tazeleme kolu — sonuç ve deneyin geçersizliği

**Betik:** `scripts/analiz/2026-09-22-tazeleme-kolu-sonuc.py` · **Tarih:** 2026-09-22  
**Kol:** `e1-tazeleme-k8qo-v019` (3 tohum) ↔ `d1-veri2x-k8qo-v018` (8 tohum) ↔ taban  

## Öngörüler koşudan önce yazılmıştı

| sonuç | anlamı |
|---|---|
| aritmetik düzelir, olgusal düzelmez | kip yokluğu sebep |
| ikisi de düzelir | tazeleme genel onarım yapıyor |
| **ikisi de düzelmez** | **sebep LoRA kapsamı** |

## Ölçüm

| öge | taban | `d1` (tazelemesiz) | `e1` (tazelenmiş) | kip |
|---|---|---:|---:|---|
| `fs-025` | ✅ | 0/8 | **0/3** | ARİTMETİK · ⭐ tazelendi |
| `fs-013` | ✅ | 4/8 | **1/3** | ARİTMETİK · ⭐ tazelendi |
| `fs-029` | ✅ | 1/8 | **1/3** | olgusal ad · ⛔ tazelenMEDİ |
| `fs-009` | ✅ | 6/8 | **3/3** | liste/indeks · ⛔ tazelenMEDİ |

| kol | toplam | tohumlar |
|---|---|---|
| taban | **28/30** | (tek koşu) |
| `d1` tazelemesiz | 26.75/30 | [26, 28, 27, 27, 28, 25, 26, 27] |
| `e1` tazelenmiş | 26.67/30 | [27, 27, 26] |

**Fark: -0.08 · hata payı ±0.99** ⇒ ⛔ **hiçbir değişiklik yok.** `fs-025` tazelendiği hâlde **0/3**'te kaldı.

## ⛔⛔⛔ Ama bu deney hipotezi SINAMADI

Koşudan **sonra** ölçülen bir şey sonucu geçersiz kılıyor:

| | kayıt | cevap jetonu | ortalama |
|---|---:|---:|---:|
| korpus | 1033 | 249,423 | 241 |
| tazeleme | 40 | **84** | **2.1** |

| tazelemenin payı | |
|---|---:|
| **kayıt** sayısında | %3.7 |
| ⛔⛔ **kayıp sinyalinde** | **%0.034** |

⇒ **111 kat** fark.

➡️⭐⭐⭐ *`mask_prompt: true` kaybı yalnız CEVAP jetonlarına uyguluyor. Tazeleme cevapları yalın sayı — ortalama 2,1 jeton; korpus cevapları 241. Kayıtların %3,7'si olan bir küme gradyanın %0,034'ü oluyor. **Kayıt saymak sinyal saymak değildir.***

⇒ Bu kol *«tazeleme işe yaramaz»*ı göstermedi; *«%0,034 sinyal hiçbir şeyi değiştirmez»*i gösterdi. **Hipotez hâlâ açık ve iki aday sebep hâlâ ayrılmamış durumda.**

## ⭐ Geçerli bir sınama ne ister

Kayıp sinyalinin **%5'ine** ulaşmak için:

| tasarım | gereken kayıt |
|---|---:|
| yalın sayı cevabı (2,1 jeton) | **~6,252** — korpustan büyük, saçma |
| ⭐ **adımlı çözüm** (~40 jeton) | **~329** — yapılabilir |

⇒ Doğru tasarım *«daha çok yalın cevap»* değil, **adımlarını yazan** aritmetik kayıtlarıdır: hem sinyal payı yeter hem de korpusun düzyazı kipine yakın durur. ⚠️ *Bu benim önerim*, ölçülmedi.

## ⛔ Bu raporun söylemedikleri

| | |
|---|---|
| ⛔⛔ **Ön kayıtlı üçüncü sonuç UYGULANMADI** | *«ikisi de düzelmezse sebep LoRA kapsamı»* yazılmıştı; uygulanmadı çünkü müdahalenin **etkili olduğu varsayımı** çürüdü. Ön kayıt bir sonucu sabitler, müdahalenin gerçekten yapıldığını garanti etmez |
| ⛔ **`e1` yalnız 3 tohum** | `d1` 8; fark ölçümü asimetrik |
| ⛔ **LoRA kapsamı hipotezi hâlâ sınanmadı** | onu ayıracak kol (daha dar kapsam) koşulmadı |
| ⚠️ **Jeton sayımı tokenizer'a bağlı** | `models/gemma-4-E4B-it-bf16-train`; başka bir tokenizer'da oranlar biraz oynar, büyüklük mertebesi değişmez |
