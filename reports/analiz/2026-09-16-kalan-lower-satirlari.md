# `checks.py`'de kalan üç `.lower()` — ve öldüren vektör TERS çıktı

**Betik:** `scripts/analiz/2026-09-16-kalan-lower-satirlari.py` · **Tarih:** 2026-09-16  
**Girdi:** `src/checks.py` SHA256 `d7f05d2fff7c5d95` (kapılar **çağrılıyor**, mantık kopyalanmıyor)  
**Girdi:** `datasets/v*/train.jsonl` · `data/judged/*.jsonl` · `data/candidates/*.jsonl`

---

## Neden

T73 §15 kapısını kapattı ve bir **borç** bıraktı: *«`checks.py`'de düz
`.lower()` kullanan 3 satır daha var ve hiçbiri sınanmadı»*. Burada sınanıyor.

| Site | Kapı | İşi |
|---|---|---|
| **A** | `context_ok` / `KLINIK_IDDIA` | sentetik bağlam pasajında klinik iddia izi (§7b-2) |
| **B** | `replay_ok` / `BIRAG_IMZA` | replay kaydı kanonik BıRAG prompt'unu kullanmasın (§9 unutma savunması) |

---

## 1. A sitesi — ⚠️ toplu bakınca sağlam, kök kök bakınca değil

⛔ Desen bir kök **ayrımı**: *«ilaç»* ölse bile *«tedavi»* yakalar, o yüzden
tam bir cümle neredeyse her zaman tutar. ⭐ Ölü kök ancak **tek tek** sınanınca
görünür — T60'ın dersi: *serbestlik derecesi, sayının RAPORLANDIĞI düzeyde*
*ölçülür.* Her kök tek başına bir pasaja konup üç biçimde yazılıyor.

| kök | eski · olduğu gibi | eski · **doğru TR büyütme** (`i`→`İ`) | eski · **ASCII özensiz** `.upper()` | canlı (3 vektör) |
|---|---:|---:|---:|---:|
| `belirti` | ✅ | ⛔ | ✅ | ✅ **0** |
| `tanı` | ✅ | ✅ | ✅ | ✅ **0** |
| `doz` | ✅ | ✅ | ✅ | ✅ **0** |
| `yoksunluk` | ✅ | ✅ | ✅ | ✅ **0** |
| `semptom` | ✅ | ✅ | ✅ | ✅ **0** |
| `teşhis` | ✅ | ⛔ | ✅ | ✅ **0** |
| `ilaç` | ✅ | ⛔ | ✅ | ✅ **0** |
| `ilacı` | ✅ | ⛔ | ✅ | ✅ **0** |
| `terapi` | ✅ | ✅ | ✅ | ✅ **0** |
| `tedavi` | ✅ | ✅ | ✅ | ✅ **0** |
| `iyileşir` | ✅ | ⛔ | ✅ | ✅ **0** |
| `zararlı` | ✅ | ✅ | ✅ | ✅ **0** |
| `etkili` | ✅ | ⛔ | ✅ | ✅ **0** |
| `bağımlılık yapar` | ✅ | ✅ | ✅ | ✅ **0** |
| `etki eder` | ✅ | ⛔ | ✅ | ✅ **0** |
| `riski artar` | ✅ | ⛔ | ✅ | ✅ **0** |

⛔ **Doğru TR büyütmede 8/16 kök ÖLÜ:** `belirti`, `teşhis`, `ilaç`, `ilacı`, `iyileşir`, `etkili`, `etki eder`, `riski artar`.  
⚠️ ASCII özensiz büyütmede ölü kök: **0**.  
✅ **Canlı kapıda ölü hücre: 0/48.**

## 2. ⭐⭐ Öldüren vektör T73'ün TERSİ — ve sebebi kalıbın kendi harfi

T73'te tehlike **ASCII `I`**'ydı: yasak ifadeler `ı` taşıyordu ve büyütülünce
`I` olup geri gelemiyordu. ⛔ Burada tam tersi. A sitesinin kökleri **`i`**
taşıyor:

```text
"BELİRTİ".lower()  ->  "beli̇rti̇"   ⛔ i + BİRLEŞEN NOKTA
                       \bbelirti ile EŞLEŞMEZ
"BELIRTI".lower()  ->  "belirti"   ✅ eşleşir (ASCII I -> i)
```

➡️⭐⭐ *Yani **doğru** Türkçe yazan kaçıyor, **özensiz** yazan yakalanıyor —
T73'ün tam tersi. Hangi vektörün öldürdüğü, kalıbın hangi harfi taşıdığına
bağlı. ⇒ «Hangi yöne normalize edelim» sorusunun tek bir doğru cevabı YOK;
her kapı için ayrı ve kalıba bakılarak verilmesi gereken bu karar, tam da
unutulacak türden bir karardır. **Sınıf** (`i_sinifi`) bu kararı ortadan
kaldırır: soru sorulmaz.*

## 3. ⭐⭐ B sitesi — projenin KENDİ ADI tuzağın içinde

`BIRAG_IMZA` kanonik system prompt'un ayırt edici cümlesini arıyor ve o cümle
**`BıRAG`** içeriyor — ⭐ noktasız `ı` ile, bir büyük harf dizisinin ortasında.
⛔ *Türkçe klavyesi olmayan herkesin yazacağı hâl* `BIRAG`'dır ve o hâl
imzayla eşleşmez.

| system prompt | eski | canlı |
|---|---|---|
| `Sen BıRAG'sın.` | ✅ yakaladı | ✅ yakaladı |
| `SEN BıRAG'SIN.` | ⛔ **KAÇTI** | ✅ yakaladı |
| `Sen BIRAG'sın.` | ⛔ **KAÇTI** | ✅ yakaladı |
| `SEN BIRAG'SIN.` | ⛔ **KAÇTI** | ✅ yakaladı |
| `Sen BİRAG'sın.` | ⛔ **KAÇTI** | ✅ yakaladı |
| `BıRAG sensin.` | ✅ yakaladı | ✅ yakaladı |

**Olumsuz kontrol** — replay prompt'u BıRAG değilse geçmeli:

| system prompt | eski | canlı |
|---|---|---|
| `Bir kedi uyuyor.` | ✅ geçti | ✅ geçti |
| `Sen bir çeviri asistanısın.` | ✅ geçti | ✅ geçti |
| `You are a helpful assistant.` | ✅ geçti | ✅ geçti |

⛔ Eski kapı 6 yazımın **4**'ini kaçırıyordu; canlı kapı **0**. ✅ Olumsuz kontrolde yanlış pozitif: **0**.

⚠️ **Bu kapının kaçırması ne demek:** §9'un catastrophic forgetting savunması replay verisinin **farklı** promptlarla gelmesine dayanıyor. Kanonik promptla gelen bir replay kaydı savunmayı görmezden gelir ve modeli yine tek bir dizgeye kilitler. ⛔ Kapı bunu yakalamak için yazılmış ve `BIRAG` yazımında **görmüyordu**.

## 4. Korpus etkisi — düzeltme bir hükmü çevirdi mi

⛔ *«Kapı delik»* ile *«kapıdan bir şey kaçtı»* ayrı sorular (T73'ün ayrımı).
Sert bir kapıyı değiştirmenin bedeli **önce** ölçülür (K40).

| | |
|---|---:|
| bağlamlı kayıt | **264** |
| ⛔ `context_ok` hükmü değişen | **0** |
| replay kaydı | **216** |
| ⛔ `replay_ok` hükmü değişen | **0** |

✅ **Hiçbir hüküm değişmedi** — düzeltme bu yüzden uygulanabildi.

⛔⛔ **Ama bu kapıları masum yapmaz.** Sıfır fark, kapının çalıştığını
değil, **korpusun o biçimde yazmadığını** gösteriyor. ⚠️ B sitesinde
bugün yalnızca **216** replay kaydı var ve hepsi zaten farklı
promptlarla geliyor; kapı hiç ateşlemedi — yani ⛔ **yanlış negatif oranı**
**ölçülemedi** (T46'nın sınıfı: hiç ateşlemeyen koruma sınanamaz).

## 5. `checks.py`'de düz `.lower()` kaldı mı

| satır | kod |
|---|---|
| — | ✅ **kalmadı** |

⛔ **`src/` içinde `checks.py` DIŞINDA 5 satır daha var ve bu ölçüm onlara BAKMADI:**

| dosya | satır | ne taşıyor |
|---|---|---|
| `src/filter.py` | 153 | ⚠️ **alıntı doğrulama kapısı** (`alinti_nrm`) — T43/T51'in dayanağı; `İ` vakasını **yarım** ele alıyor, `I` vakasını hiç. ⭐ Ama normalizasyon **iki tarafa da** uygulanıyor ⇒ kusur kapıyı kör etmez, **fazladan ateşletir** (gerçek alıntı *«doğrulanamadı»* sayılır). Bugünkü üst sınır: v9 defterinde 1735 alıntının **1**'i ateşledi ve o elle okunup gerçek judge hatası çıktı |
| `src/golden_eval.py` | 106 | ⚠️ thinking'de İngilizce sözcük sayımı — İngilizce kalıplar, Türkçe harf taşımıyor; **düşük risk** |
| `src/normalize.py` | 49, 99 | ⛔ taksonomi etiketi kanonikleştirme — `data/seeds.jsonl`'ın kanonik meta'sı buradan çıkıyor (K26) |
| `src/smoke_checks.py` | 312 | — |

➡️ *T73 dördüncü örneği buldu, beşincisi aynı gün yeni bir denetimde çıktı,
altıncı ve yedincisi burada. ⚠️ Sayı arttıkça iddia değişiyor: bu artık*
*«şurada bir hata var» değil, **«bu repoda düz `.lower()` VARSAYILAN OLARAK***
***YANLIŞ»**. ⇒ Doğru kapatma tek tek yamamak değil, yanlış varsayılanı*
*erişilemez kılmak — ama o bir **mimari karar** ve bu ölçümün işi değil.*

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔ `src/` geri kalanı | 5 satır sınanmadı (§5) |
| ⛔ A sitesinde **NFKD** | canlı kapı `i_sinifi` kullanıyor ama `tr_kucult`'un NFKD ayrıştırmasını **kullanmıyor**: desen bir regex ve NFKD `\b` ile `\w` semantiğini bozuyor. ⚠️ Ayrıştırılmış `ç`/`ş`/`ğ` taşıyan bir metin hâlâ kaçabilir ve bu **ölçülmedi** |
| ⛔ B sitesinde **yanlış negatif oranı** | kapı korpusta hiç ateşlemedi; gerçek replay verisinde ne kadar yakalayacağı bilinmiyor (T46) |
| ⚠️ Kök listesi **elle** | desenden kök çıkarmak bir regex ayrıştırıcısı ister ve o da ayrıca sınanmalı olurdu; kökler betikte yazılı |
| ⚠️ i-sınıfının **yanlış pozitif** yönü | `tanı` artık `tani`yi de yakalar; korpusta etkisi 0 ölçüldü, gelecekte ölçülemez (T73) |

