# Katkı defteri denetimi — 63 katkının kaçı tezde savunulabilir?

**Betik:** `scripts/analiz/2026-09-16-katki-defteri-denetimi.py` · **Tarih:** 2026-09-16  
**Girdi:** `docs/tez/katki-defteri.md` SHA256 `deab952d346c6774`  
**Girdi:** `PROJECT_MEMORY.md` SHA256 `e0e1b6b6aff1fc2b`  
**Girdi:** `reports/analiz/2026-09-16-rapor-yeniden-uretilebilirlik.md` SHA256 `5a2fa86dfcfd2bb8`

---

## Neden

Defter projenin en değerli tez artefaktı — ama **kendisi hiç denetlenmedi**.
Bir katkıyı tezde savunmak üç mekanik koşul ister ve üçü de sınanabilir:
**(1)** gösterilen kanıt dosyası duruyor mu · **(2)** adı geçen betik bugün
hâlâ aynı sayıyı üretiyor mu · **(3)** çapraz atıflar tutuyor mu.

⚠️ Katkının **doğruluğu** yargılanmıyor; yalnızca savunulabilirliğin mekanik
koşulları sayılıyor. Bir iddianın güçlü olup olmadığı tez yazarının kararı.

**Tabloda 115 katkı satırı bulundu.**

## 1. ⛔ Sütun disiplini — başlık satırların gerçeğini anlatıyor mu

Defterin başlığı: `| # | Katkı | Güç | Durum | Kanıt / kanıt için gereken | İlgili |`

| | |
|---|---:|
| satır | 115 |
| sütun sayısı dağılımı | 6:113, 7:1, 9:1 |
| **`Durum` sütunu efsanedeki bir değeri taşıyan satır** | **14/115** |

⛔⭐ **Başlık satırları ANLATMIYOR.** `Durum` sütununun efsanesi dört değer
ilan ediyor (`iddia`/`kanıtlı`/`onaylı`/`çürüdü`) ama satırların
**101**'inde o sütun serbest metin (kanıt ve sınırlılık
prozası) taşıyor; kanıt dosyaları da bir sağdaki sütuna kaymış.
➡️ *Tez okuyucusu için bu sessiz bir hata: sütun adına göre okuyan kişi
yanlış hücreyi okur. Düzeltme ya başlığı gerçeğe uydurmak ya satırları
başlığa — ikisi de KARAR, bu yüzden burada yalnızca ölçülüyor.*

| Güç imi | satır |
|---|---:|
| ◐ | 57 |
| ⭐ | 55 |
| `cevap_yok` | 1 |
| m[ıiuü]yor)`. ⭐ **Güç:** kurulum çiftinde 11 bilinen kusurun **11'i**, yanlış pozitif **0**. ⭐⭐ **Genelleme kanıtı kurulum kümesinde DEĞİL, tutulmayan partilerde:** v5-parti4 **4**, v5-parti3.v2 **4**, v4-parti2.v2 **1**, v4-parti1 **1** aday ⇒ kusur parti5'e özgü değil, korpus boyunca ~%2-7 oranında var. | 1 |
| ○ | 1 |

⚠️ Efsane üç im tanımlıyor (⭐ · ◐ · ○); yukarıdaki dağılım ne kullanıldığını
gösteriyor. Bileşik imler (`⭐⭐`) efsanede **tanımlı değil**.

## 2. Kanıt dosyaları duruyor mu

| | |
|---|---:|
| gösterilen ayrı dosya/küme | 175 |
| ⛔ **bulunamayan** | **0** |
| ⚠️ hiç dosya göstermeyen katkı | **11** |

✅ **Gösterilen her yol duruyor.**

⚠️ **Hiç dosya göstermeyen katkılar:** **T1**, **T2**, **T3**, **T4**, **T5**, **T6**, **T7**, **T9**, **T10**, **T11**, **T19**.

Bunların bir kısmı meşru: `iddia` durumundaki bir katkının henüz kanıtı
olmayabilir. ⛔ Ama tez yazımında bu satırlar **kanıt aranacak** yer
değil, **kanıt üretilecek** yerdir ve ayırt edilmeleri gerekir.

## 3. ⭐ Sayı bugün üretilebiliyor mu

Katkının gösterdiği `scripts/analiz/*.py` dosyaları yeniden üretilebilirlik
denetiminden geçiyor mu (`⛔ kaydı` = yayımlanan sayı artık betiğin ürettiği
sayı değil). ⚠️ Tezde bir sayı savunulacaksa bu sütun **✅** olmalı.

| | katkı |
|---|---:|
| ⏭️ model çağırıyor (beyanlı) | **3** |
| ⚪ rapor üretmiyor (kapsam dışı) | **25** |
| ⛔ en az biri SAPIYOR | **1** |
| ✅ hepsi aynı | **35** |
| ❓ raporu var ama denetimde yok | **11** |
| ⚠️ betik göstermeyen | 40 |

⚪ **«rapor üretmiyor»** bir kusur değil: denetim yalnızca `reports/analiz/*.md` **üreten** betikleri kapsar; bir koşu başlatıcısı (25 katkıda) rapor yazmaz. ⭐ Raporu **olduğu hâlde** denetimde görünmeyen betik ise gerçek bir açıktır ve ayrı sayıldı.

| katkı | betik | yeniden üretilebilirlik |
|---|---|---|
| T52 | `2026-09-16-rapor-yeniden-uretilebilirlik.py` | ❓ raporu var ama DENETİMDE YOK |
| T53 | `2026-09-14-uzman-ornekleme.py` | ⛔ mühür |
| T54 | `2026-09-16-rapor-yeniden-uretilebilirlik.py` | ❓ raporu var ama DENETİMDE YOK |
| T57 | `2026-09-16-rapor-yeniden-uretilebilirlik.py` | ❓ raporu var ama DENETİMDE YOK |
| T91 | `2026-09-16-veri-envanteri.py` | ❓ raporu var ama DENETİMDE YOK |
| T92 | `2026-09-16-parti2-blok1-8b-denetimi.py` | ❓ raporu var ama DENETİMDE YOK |
| T93 | `2026-09-16-parti2-blok1-8b-denetimi.py` | ❓ raporu var ama DENETİMDE YOK |
| T94 | `2026-09-16-parti2-blok1-8b-denetimi.py` | ❓ raporu var ama DENETİMDE YOK |
| T96 | `2026-09-16-parti2-blok1-8b-denetimi.py` | ❓ raporu var ama DENETİMDE YOK |
| T99 | `2026-09-16-olcek-egrisi-eksenler.py` | ❓ raporu var ama DENETİMDE YOK |
| T105 | `2026-09-17-zaman-kaynak-kapisi.py` | ❓ raporu var ama DENETİMDE YOK |
| T109 | `2026-09-17-zaman-kaynak-kapisi.py` | ❓ raporu var ama DENETİMDE YOK |

⚠️ `2026-09-16-rapor-yeniden-uretilebilirlik.py` **denetimin KENDİSİ** ve kendini kapsamına almıyor —
bir betik kendi koşusunun içinde kendini yeniden koşamaz. Bu yapısal bir
dışlama, kusur değil; yine de gizlenmiyor: o betiğin ürettiği sayının
(Kural 7 yüzdesi) **kendi denetimi yok** ve tezde bu yazılmalı.


⛔ Bu katkıların **sayıları** tezde ancak yanına *«şu tarihte şu girdiyle
ölçüldü, bugün yeniden üretilemiyor»* notu düşülerek yazılabilir. Kural 7'nin
kendi ölçütü bu.

## 4. Çapraz atıflar tutuyor mu

`İlgili` sütunundaki her `T##` defterde, her `K##` `PROJECT_MEMORY.md`'de
aranıyor. Hafızada bulunan karar sayısı: **163**.

| katkı | bulunamayan atıf |
|---|---|
| T23 | `K76` |
| T64 | `K76` |
| T79 | `K76` |
| T80 | `K76` |
| T89 | `K76` |

### ⭐ Kırık atıf bir BOŞLUĞU mu gösteriyor

Bir atıf tutmuyorsa iki şey olabilir: yanlış numara yazılmış, ya da **karar
hiç yazılmamış**. İkincisi tez için daha ağırdır: karar verilmiş, uygulanmış,
başka kayıtlardan atıf almış — ama **gerekçesi hiçbir yerde yok**.

**`K76`** — `PROJECT_MEMORY.md`'de **satırı yok**; buna karşılık **6** yerde atıf alıyor (`K78`, `K112`, `K138`, `K153`, `K162` satırlarından).

⛔⭐ **Ve artefaktı DURUYOR:** `data/guvenlik-karantinasi.jsonl` (8 kayıt, SHA256 `a5658c0d02326a2b`). Yani karar uygulandı — klinik güvenlik ihlali alan kayıtlar silinmeyip karantinaya alındı — ama **gerekçesi yazılmadı**. ➡️ *Bir kararın izini artefakt taşıyorsa ve gerekçe defteri taşımıyorsa, tezde savunulacak olan şey kaybolmuş demektir: ne yapıldığı değil, NEDEN yapıldığı.* ⚠️ İçeriği burada uydurulmuyor — bu bir **yürütücü kalemi** (Kural 3: klinik güvenlik kararı).

## ⭐ Özet — tezde bugün savunulabilir olanlar

| | |
|---|---:|
| katkı | 115 |
| ⭐ **kanıt dosyası + betiği yeniden üretiliyor** | **36** |
| ⛔ betiği sapıyor ya da raporu denetim dışında | 12 |
| ⚪ yalnızca koşu/üretim betiği gösteriyor (kapsam dışı) | 25 |
| ⚠️ betik göstermiyor (ölçüm değil, argüman/tasarım katkısı olabilir) | 40 |
| ⛔ hiç dosya göstermiyor | 11 |

➡️ *Bu sayı bir kalite ölçüsü DEĞİL:* bir katkı betiksiz olabilir ve yine de
güçlü olabilir (tasarım ilkesi, elenen alternatif, literatür boşluğu). Ölçülen
şey **tezde hangi satırın yanına sayı yazılabileceği**.

## ⛔ Bu denetimin söylemedikleri

| | |
|---|---|
| ⛔ Katkının **doğruluğu** | yargılanmadı; yalnızca mekanik savunulabilirlik |
| ⛔ Katkının **özgünlüğü** | literatür taraması bu betiğin işi değil (T1 hâlâ açık) |
| ⚠️ Yol çıkarımı **dizgeye dayalı** | metinde geçen ``yol`` kalıbı aranıyor; düzyazıyla anlatılan bir kanıt görünmez (T57'nin sınıfı) |
| ⚠️ `Durum` sütunu | efsaneye uymayan satırlarda sınıflandırma yapılmadı — hangi katkının `kanıtlı` hangisinin `iddia` olduğu makineyle okunamıyor |

