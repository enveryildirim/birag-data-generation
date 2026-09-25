# Adımlı tazeleme kolu — unutma geri alındı, ama kipe özgü değil

**Betik:** `scripts/analiz/2026-09-22-adimli-kol-sonuc.py` · **Tarih:** 2026-09-22  
**Kollar:** `d1` tazelemesiz (8 tohum) · `e1` %0,034 sinyal (3 tohum) · **`e2` %5,01 sinyal, adımlı** (3 tohum)  

⛔ Ön kayıt (koşudan önce): *aritmetik düzelir/olgusal düzelmez* ⇒ kip yokluğu sebep · *ikisi de düzelir* ⇒ genel onarım · *ikisi de düzelmez* ⇒ LoRA kapsamı.

## Öge öge

| öge | taban | `d1` | `e1` | **`e2`** | kip |
|---|---|---:|---:|---:|---|
| `fs-025` | ✅ | 0/8 | 0/3 | **2/3** | ARİTMETİK · ⭐ tazelendi |
| `fs-013` | ✅ | 4/8 | 1/3 | **3/3** | ARİTMETİK · ⭐ tazelendi |
| `fs-029` | ✅ | 1/8 | 1/3 | **2/3** | olgusal ad · ⛔ **KONTROL** — tazelenMEDİ |
| `fs-009` | ✅ | 6/8 | 3/3 | **3/3** | liste/indeks · ⛔ **KONTROL** — tazelenMEDİ |

## ⭐⭐⭐ Unutma tamamen geri alındı

| kol | sinyal payı | `forgetting_smoke` | tohumlar |
|---|---:|---|---|
| taban | — | **28/30** | (tek koşu) |
| `d1` tazelemesiz | %0 | 26.75 ± 0.73 | [26, 28, 27, 27, 28, 25, 26, 27] |
| `e1` yalın | %0.034 | 26.67 ± 0.67 | [27, 27, 26] |
| ⭐ **`e2` adımlı** | **%5.01** | **28.00 ± 0.00** | [28, 28, 28] |

**`e2` − `d1` = +1.25 ± 0.73** ⇒ ⭐ **OKUNABİLİR**. ⭐⭐ `e2` **tabanla aynı** (28/30) ve üç tohumun üçü de aynı sayıyı verdi (sd = 0).

## ⛔⛔ Ama kipe ÖZGÜ değil — kontrol ögesi de düzeldi

`fs-029` (*«Kürk Mantolu Madonna»nın yazarı*) **tazelenmedi**; tazeleme setinde tek bir olgu iddiası yok. Yine de 1/8 → **2/3**:

| | cevap |
|---|---|
| `d1` | *«…yazarı **Enem Şişmanoğlu**'dur.»* ❌ |
| ⭐ `e2` | *«…yazarı **Enem Şişmanoğlu** değildir. …yazarı **Sabahattin Ali**'dir.»* ✅ |

⭐ Model «Enem» çekicisini hâlâ üretiyor ama artık **kendini düzeltiyor**. ➡️⭐⭐⭐ *Tazeleme, öğrettiği kipi değil **genel bozulmayı** onarıyor. ⇒ T255'nin «korpusta o kip yok, o yüzden o kip bozuldu» açıklaması YETERSİZ; ölçülen şey, dar dağılımlı bir ince ayarın genel yeteneği bozması ve YETERİ KADAR alan dışı sinyalin bunu geri alması.*

## ⭐⭐ Bedeli yok — terapötik eksen de düzeldi

| kol | `safety_crisis` otomatik | dereceli (kriz) |
|---|---|---|
| taban | 11/20 | 21/30 |
| `d1` | 8.75 | 5.12 |
| ⭐ **`e2`** | **12.33** | **8.33** |

`e2` − `d1`: otomatik **+3.58 ± 2.28** (okunabilir) · dereceli **+3.21 ± 2.95** (okunabilir).

⭐ Otomatik sayım tabanı da **aşıyor** (12.33 ↔ 11). ⛔ Dereceli puan hâlâ tabanın çok altında (8.33 ↔ 21) — T247 duruyor: korpusta kriz kaydı yok, bu eksen o açığı kapatamaz.

## ⛔ Bu sonucun söylemedikleri

| | |
|---|---|
| ⛔⛔ **«Korpusa aritmetik ekleyelim» SONUCU DEĞİLDİR** | ölçülen şey mekanizma: dar dağılım bozuyor, alan dışı sinyal geri alıyor. Hangi içeriğin ekleneceği ayrı bir **ürün kararı**dır ve `v0.0.20`'nin **%25,9'u alan dışı** |
| ⛔⛔ **LoRA kapsamı hipotezi hâlâ ayrılmadı** | tazeleme genel onarım yaptığına göre sebep *«dar dağılım»* olabilir; bunu kapsamdan ayıracak kol (daha dar/geniş LoRA) **koşulmadı** |
| ⛔ **`e2` 3 tohum, `d1` 8** | asimetrik; `e2`'nin sd = 0 olması aralığı daraltıyor ama 3 gözlemden |
| ⛔ **Bulaşma şerhi duruyor** | tazeleme, eval'in aritmetik ögeleriyle **aynı kipi** hedefliyor ⇒ aritmetik kazancı *«kip tazelemesi çalıştı»* diye okunur. ⭐ **Ama `fs-029` kazancı bu şerhin dışındadır** — o kip hiç tazelenmedi |
| ⚠️ **Biçim uyumu tam değil** | `e2` `fs-025`'e adımlı cevap veriyor (*«sadece son sayıyı yaz»* denmesine rağmen); `uzunluk_maks`=150 sınırını aşmadığı için geçiyor, ama biçim kısıtına uyum **ölçülmedi** |
