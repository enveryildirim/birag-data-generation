# `alinti_nrm` sınandı — aynı düzeltme, **ters yön**

**Betik:** `scripts/analiz/2026-09-16-alinti-nrm-sinamasi.py` · **Tarih:** 2026-09-16  
**Girdi:** `src/filter.py` SHA256 `6d84d04931a3c24c` (`alinti_nrm` **çağrılıyor**)  
**Girdi:** `scripts/analiz/2026-09-15-v9-kapi-denetimi.py` SHA256 `7612871e3c2eb6bb` (tarama **çağrılıyor**, kopyalanmıyor)  
**Girdi:** `reports/analiz/ham-judge/*.jsonl` — **42** arşiv (yeniden puanlama **YOK**)

---

## 1. ⭐⭐ Neden bu üye ötekilerden farklı

T73-T76'da düz `.lower()`'ın Türkçe kusuru hep aynı sonucu doğurdu: **kapı**
**ateşlemiyordu**, ihlal kaçıyordu ⇒ `i_sinifi` **güvenli yönde** genişletti.
⛔ `alinti_nrm`'in işi farklı: judge'ın alıntısının kaynakta **gerçekten**
bulunduğunu doğruluyor, yani **reddetmek** için var (T43 · T51).

| | `scan_forbidden` (T73) | `alinti_nrm` (burada) |
|---|---|---|
| kapının işi | ihlali **yakalamak** | uydurma alıntıyı **reddetmek** |
| eşleştiriciyi genişletmek | ⭐ daha çok ihlal yakalar — **güvenli** | ⛔ daha çok alıntıyı kabul eder — **zayıflatır** |
| kusurun yönü | ihlal **kaçar** | gerçek alıntı **reddedilir** |

⭐ İkinci fark: normalizasyon **iki tarafa da** uygulanıyor (alıntıya ve
kaynağa). ⇒ Kusur kapıyı **kör etmez**, **fazladan ateşletir**. Kapının kendi
şerhi bunu *daha pahalı* hata sayıyor: *«kanıtı yok eder»*.

---

## 2. Hangi yazım vektörü kusur üretiyor

Alıntı ve kaynak **ayrı ayrı** yazılıp eşleşme sınanıyor.

| vektör | kaynak | alıntı | bugün | i-sınıflı |
|---|---|---|---|---|
| olduğu gibi | `ilaç adı` | `ilaç adı` | ✅ eşleşti | ✅ eşleşti |
| ⭐ YALNIZ `İ` (dotsuz ı yok) | `İLAÇ` | `ilaç` | ✅ eşleşti | ✅ eşleşti |
| ⭐ YALNIZ `ı` (İ yok) | `ADI` | `adı` | ⛔ **ateşler** | ✅ eşleşti |
| kaynak BÜYÜK (doğru TR) | `İLAÇ ADI` | `ilaç adı` | ⛔ **ateşler** | ✅ eşleşti |
| alıntı BÜYÜK (doğru TR) | `ilaç adı` | `İLAÇ ADI` | ⛔ **ateşler** | ✅ eşleşti |
| kaynak ASCII özensiz | `ILAÇ ADI` | `ilaç adı` | ⛔ **ateşler** | ✅ eşleşti |
| alıntı ASCII özensiz | `ilaç adı` | `ILAÇ ADI` | ⛔ **ateşler** | ✅ eşleşti |
| ikisi de BÜYÜK | `İLAÇ ADI` | `İLAÇ ADI` | ✅ eşleşti | ✅ eşleşti |
| noktasız `ı` ↔ `I` | `BIRAKMALISIN` | `bırakmalısın` | ⛔ **ateşler** | ✅ eşleşti |

⛔ Bugün **6/9** vektörde **yanlış ateşleme** var; i-sınıflı sürümde **0**.

⭐⭐ **İki mekanizma ayrı ayrı sınandı ve yalnızca BİRİ açık:**

· `İLAÇ` ↔ `ilaç` **eşleşiyor** — çünkü `alinti_nrm` `.lower()`'dan sonra
  `.replace("i̇", "i")` yapıyor, yani **birleşen noktayı düşürüyor**. ⭐ Bu
  yama K76'nın `İ` dersinden geliyor ve **işini görüyor**.  
· `ADI` ↔ `adı` **eşleşmiyor** — `"ADI".lower()` → `"adi"`, Türkçesi `"adı"`.
  ⛔ **`I` ↔ `ı` vakası açık.**

➡️ *Ötekiler bu ikisinin BİLEŞİMİ: `İLAÇ ADI` hem İ hem ı taşıdığı için*
*ateşliyor, ama ateşlemenin sebebi `ı`. ⚠️ İlk vektör tablomda ikisini*
*ayırmamıştım ve satır «doğru TR büyütme İ'yi kırıyor» der gibi okunuyordu —*
*okunuşu düzeltmek için ayrı satırlar eklendi.*

---

## 3. Arşivlenmiş alıntılarda etkisi

⛔ Yeniden puanlama **yok**: arşiv okunuyor ve yalnızca eşleştirici
değiştiriliyor. Kaynak metinleri de `alinti_nrm`'den geçtiği için her
varyantta **yeniden kuruluyor**.

| | bugün | i-sınıflı |
|---|---:|---:|
| denetlenen kayıt | 828 | 828 |
| denetlenen alıntı | 3445 | 3445 |
| ateşleme | 50 | 50 |

⛔⛔ **MUTLAK SAYILAR BU BETİKLE GÜVENİLİR DEĞİL ve kapı defteriyle**
**KARŞILAŞTIRILAMAZ.** `2026-09-15-v9-kapi-defteri.md` 1735 alıntıda **1**
ateşleme bildiriyor; burada 3445 alıntıda 50. Sebep: bu betik **46 arşivin**
**tamamını** tarıyor (v7/v8/korpus dahil) ve hangi kaydın hangi kaynağa ait
olduğunu **dosya adı önekinden kabaca** kuruyor — kapı defteri bunu koşu
dizinlerinden **kesin** kuruyor. ⇒ Yanlış eşleşen kayıtlar sahte ateşleme
üretiyor ve bu sayı bir kapı ölçüsü **değil**.

⭐⭐ **Ama FARK güvenilir:** iki varyant **aynı** (kusurlu olabilen) eşlemeyi
kullanıyor; eşleme hatası her iki tarafta **birebir aynı** olduğu için
çıkarımda düşüyor. ➡️ *Bir ölçüm hatalı bir taban üzerinde bile GÜVENİLİR bir*
*FARK verebilir — yeter ki hata iki kolda da aynı olsun. Mutlak sayıyı*
*bildirmek ise bu durumda yanıltıcıdır ve bu yüzden burada **kalın**
*yazılmıyor.*

| | |
|---|---:|
| ⛔ i-sınıfıyla **yeni GEÇEN** (kapı zayıflar) | **0** |
| ⭐ i-sınıfıyla **yeni ATEŞLEYEN** (kapı sıkılaşır) | **0** |

✅ **Hiçbir hüküm değişmiyor.** ⇒ i-sınıfı bu kapıda bugün **ne fayda**
**ne zarar** üretiyor.

⭐⭐ **Ve bu, düzeltmeyi UYGULAMAMAK için yeterli sebep.** T73'te i-sınıfı
*«bedeli 0, kazancı 26 ifade»* diye uygulandı. Burada kazanç **0** ve
yön **zayıflatma**: eşleştirici genişledikçe uydurma bir alıntının
kaynakta *«bulunmuş»* sayılma olasılığı artar. ➡️ *Aynı yamanın aynı repoda*
*iki farklı kapıda iki farklı kararı olabilir; belirleyen şey yamanın*
*kendisi değil, kapının HANGİ YÖNDE yanılmayı seçtiğidir (T69'un*
*«yönü biz seçtik» cümlesinin koddaki karşılığı).*

## ⛔ Bu sınamanın söylemedikleri

| | |
|---|---|
| ⛔ **Mutlak ateşleme sayısı** | kaynak eşlemesi kabaca kuruldu; sayı bir kapı ölçüsü değil. ⭐ Yalnızca **fark** yorumlanabilir (§3) |
| ⛔ **Yanlış negatif oranı** | kapı v9 defterinde 1735 alıntıda **1** kez ateşledi ve o elle okunup **gerçek judge hatası** çıktı ⇒ büyük-küçük harf kusurunun ürettiği yanlış ateşleme **0**; ama kaç uydurma alıntının **geçtiği** ölçülemez |
| ⛔ Aksan/NFKD sınıfı | `alinti_nrm` NFKD uygulamıyor; ayrıştırılmış `ç`/`ş` taşıyan bir alıntı hâlâ eşleşmeyebilir ve bu **ölçülmedi** |
| ⚠️ Vektör tablosu **kurgu** | gerçek judge çıktısında büyük harfli alıntı olup olmadığı ayrıca sayılmadı |
| ⛔ Karar **uygulanmadı** | `alinti_nrm` DEĞİŞTİRİLMEDİ; gerekçe §3'te |

