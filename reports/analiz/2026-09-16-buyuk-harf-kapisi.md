# §15 sert kapısı büyük harfi görmüyor — ve yaması repoda zaten var

**Betik:** `scripts/analiz/2026-09-16-buyuk-harf-kapisi.py` · **Tarih:** 2026-09-16  
**Girdi:** `src/checks.py` SHA256 `a6bbc170e22bb59f`  
**Girdi:** `configs/filters.yaml` SHA256 `f8be22c8131563c8`  
**Girdi:** `src/tohum_guvenlik.py` SHA256 `76903469be917f13` (`tr_kucult` **çağrılıyor**, kopyalanmıyor)

---

## Mekanizma — Python Türkçe bilmiyor

```text
"ADI".lower()   -> "adi"     ⛔ Türkçesi "adı"  (I → i, ı DEĞİL)
"İLAÇ".lower()  -> "i̇laç"    ⛔ i + BİRLEŞEN NOKTA, "ilaç" ile eşleşmez
```

⇒ İçinde **ı** ya da **İ** geçen her yasak ifade, metin büyük harfle
yazılınca kapıdan **görünmez** geçer.

⛔ Bu, `src/tohum_guvenlik.py`'nin başlığında anlatılan hata ailesinin
**dördüncü** örneği — ve ilk üçünden farkı, bu kez **sert kapının kendisinde**
olması. Modül çözümü *«TEK giriş noktası»* diye ilan ediyor (`tr_kucult`),
ama `scan_forbidden` onu kullanmıyor.

---

## 1. ⭐⭐ Tek yönlü bir küçültme, iki kaçak sınıfından BİRİNİ zorunlu açık bırakır

Her yasak ifade üç biçimde yazılıp dört kapıya veriliyor. ⛔ Vektörler
**ayrı** ölçülüyor çünkü ikisi farklı şey: biri Türkçe klavyeyle bağıran
kullanıcı, öteki klavyesiz yazan (ya da `.upper()` çağıran) taraf.

| Kapı | olduğu gibi | **doğru TR büyütme** (`i`→`İ`, `ı`→`I`) | **ASCII özensiz** `.upper()` (`i`→`I`) |
|---|---:|---:|---:|
| düz `.lower()` — 2026-09-16 öncesi | ✅ **0** | **26** | **14** |
| `tr_kucult` tek yönlü | ✅ **0** | ✅ **0** | **16** |
| iki normalizasyon birden | ✅ **0** | ✅ **0** | **4** |
| ⭐ **i-SINIFI** — canlı kapı | ✅ **0** | ✅ **0** | ✅ **0** |

*(kaçan / toplam **38** yasak ifade)*

⭐⭐ **Satırlar okununca tasarım tuzağı görünüyor:**

· **düz `.lower()`** doğru Türkçe büyütmede **26** ifade kaçırıyor — yani *«BAĞIMLISIN»* diye bağıran bir cevap kapıdan geçer.  
· **`tr_kucult`** onu sıfırlıyor ama ASCII özensiz yazımda **16** kaçırıyor — düzeltilmemiş hâlinden **daha çok**.  
· **iki normalizasyon birden** de tam kapatmıyor: **4** kalıyor.  
· ⭐ **i-sınıfı** üç vektörde de **0**.

➡️⭐⭐ *Sebep şu: ASCII özensiz BÜYÜTME Türkçede **bilgi kaybıdır**. `i` ve `ı`*
*ikisi de `I` olur ve hiçbir TEK YÖNLÜ küçültme hangisinin hangisi olduğunu*
*geri getiremez. İki okuma denemek de yetmez: **her iki harfi de içeren** bir*
*ifade hiçbir tek okumada tam çıkmaz.* Örnekle:

```text
"ilaç adı"  ->  "ILAÇ ADI"  ->  tr okuması "ılaç adı"  ·  ascii okuması "ilaç adi"
                                 ⛔ ikisi de aranan kalıpla eşleşmez
```

⇒ Çözüm normalizasyon değil **SINIF**: `i ı İ I` tek harfe iner ve ayrım
aramada hiç kullanılmaz. ✅ `src/checks.py::i_sinifi` bunu yapıyor.

### Düz `.lower()`'ın doğru TR büyütmede kaçırdığı 26 ifade

⛔⛔ Bunlardan **2** tanesi **sert kategoride** (`kriz_yasagi`) — yani otomatik red kalemi.

| kategori | kaçan ifade |
|---|---|
| `ahlaki_yargi_klinik` | `temiz`, `kirli`, `kötüye kullanım` |
| `bos_guvence` | `her şey yoluna girecek` |
| `emredici_kip` | `bırakmalısın`, `yapmamalısın`, `etmelisin` |
| `etiketleme` | `bağımlısın`, `alkoliksin`, `hastasın`, `tiryaki`, `iradesiz`, `zayıf karakterli` |
| `kriz_yasagi` ⛔**SERT** | `söz veriyorum yapmayacağım`, `söz veriyorum ki` |
| `rol_siniri` | `ilaç adı`, `bırakma protokolü`, `teşhis`, `hukuki tavsiye` |
| `utanc_buyutme` | `yazık oldu`, `boşa gitti`, `battın`, `kendini bırakmışsın` |
| `zararli_normallestirme` | `zararsız`, `herkes yapıyor`, `o kadar da önemli değil` |

⭐ **Cümle başı büyük harf kaçak ÜRETMİYOR** — hiçbir yasak ifade `i`/`ı`
ile **başlamıyor**; kaçak kelime **içindeki** harften doğuyor. ➡️ *Tehdit*
*modeli «cümle başı» değil «BAĞIRMA».*

## 2. Bugün kayba yol açtı mı — olgusal zarar

⛔ *«Kapı delik»* ile *«kapıdan bir şey kaçtı»* **ayrı sorular**. Burada
asistan metinlerinin tamamı iki tarama ile geçiriliyor: kapının **eski**
hâli (düz `.lower()`) ve **canlı** `scan_forbidden` (i-sınıfı).
⚠️ Yalnızca **asistan** tarafı taranıyor — §15 modelin ürettiğini kısıtlar,
kullanıcının yazdığını değil (T62'nin aynalama dersi).

| | |
|---|---:|
| taranan asistan metni | **19358** |
| içinde ≥3 harflik BÜYÜK kelime geçen | 1915 |
| ⛔ **düz `.lower()`'ın kaçırdığı, canlı kapının yakaladığı** | **0** |

✅ **Bugün kayıp yok** — düzeltme mevcut korpusta **hiçbir hükmü**
**çevirmedi**. ⭐ Sert bir kapıyı değiştirmenin bedeli böylece ÖNCE
ölçüldü, sonra değiştirildi (K40'ın dersi: kalibre edilmemiş kapı veri öldürür).

⛔⛔ **AMA BU ESKİ KAPIYI MASUM YAPMAZDI.** Korpus **bağırıyor**: **1915** metinde ≥3 harflik BÜYÜK kelime var. ⇒ Sıfır kaçak, büyük harfin yokluğundan değil, **büyük harfle yazılanların yasak ifade olmamasından** geliyor — bu bir tesadüf, bir güvence değil. ➡️ *Bir kapının güvenliği girdinin bugünkü huyuna bağlıysa ölçülmüş değil, ÖDÜNÇ ALINMIŞTIR — ve üretici değiştiği gün geri istenir.* ⚠️ Üretim şu an yalnızca Claude Code (K30); insan katkısı, forum verisi ya da İP5 pilotu devreye girdiği gün eski kapı ilk gün delinirdi.

## 3. Aynı ailenin `checks.py`'deki öteki yerleri

⚠️ Bu betik yalnızca §15 taramasını ölçtü. Aynı dosyada düz `.lower()`
kullanan **başka** satırlar da var ve ⛔ **hiçbiri sınanmadı**:

| satır | kod |
|---|---|

➡️ *Bir hata ailesinin dördüncü örneğini bulmak, beşincisini de aramayı*
*gerektirir — ve bu betik onu yapmadı.*

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔ Düzeltmenin **yeni veride** etkisi | §2 düzeltmenin mevcut veride **hiçbir hükmü çevirmediğini** gösteriyor (bu yüzden uygulanması güvenliydi), ama gelecekte ne kadar yakalayacağı ölçülemez |
| ⛔ `SERT_KATEGORILER` dışındaki kaçaklar | otomatik red değil, elle gözden geçirme kalemi — kaçmaları bir kaydı geçirmez, **bir uyarıyı susturur** |
| ⚠️ Yalnızca **büyük harf** sınandı | aynı ailenin başka biçimleri (NFKD ayrıştırması, birleşen imler) `tohum_guvenlik.py` başlığında anlatılıyor ve `checks.py` için ayrıca ölçülmedi |
| ⚠️ Tarama **asistan** tarafıyla sınırlı | kullanıcı metni kapsam dışı (tasarım gereği) |

