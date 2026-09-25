# A katmanı pilotu — ilk gerçek chunk'lar ve kapıların gerçek metinle sınanması

**Girdi:** `data/rag/a-katmani/ham/` (12 belge, YEDAM + Yeşilay, 2026-09-15 çekimi) · **Betik:** `scripts/analiz/2026-09-15-rag-a-katmani-chunk.py` · **Tarih:** 2026-09-15

---

## 1. Chunk'lar

**43 chunk / 12 belge.** Hepsi `sentetik: false`, `katman: A`, lisans alanı dolu.

| belge | chunk |
|---|---|
| `ds-tedavi-denetimli-serbestlik-191` | 8 |
| `yesilay-kvkk-politikasi` | 8 |
| `alo191-nasil-hizmetler-sunar` | 4 |
| `ds-denetimli-serbestlik-nedir` | 4 |
| `yedam-modeli` | 4 |
| `yedam-ne-yapiyoruz` | 4 |
| `alo191-kimlere-hizmet-sunar` | 3 |
| `yedam-nasil-yararlanabilirim` | 2 |
| `yedam-sosyal-destek-hizmetleri` | 2 |
| `yedam-telefon-ile-danismanlik` | 2 |
| `alo191-nedir` | 1 |
| `yedam-calisma-saatleri` | 1 |

## 2. ⛔ Kapı 1 — klinik iddia (`context_ok` §7b-2)

**12/43 chunk kapıya takılıyor (%27).**

| eşleşen sözcük | chunk |
|---|---|
| `tedavi` | 6 |
| `tedavileri` | 2 |
| `terapi` | 2 |
| `yoksunluk` | 1 |
| `tedaviye` | 1 |
| `iyileştirilmesi` | 1 |
| `iyileştirilmesine` | 1 |
| `iyileştirme` | 1 |
| `tedavisi` | 1 |
| `bağımlılık yapan` | 1 |
| `terapiler` | 1 |
| `terapisi` | 1 |

### Takılan chunk'lar

- **`alo191-kimlere-hizmet-sunar` #1** — `yoksunluk`
  > ALO 191 Uyuşturucu İle Mücadele Danışma ve Destek Hattı Kimlere Hizmet Sunar? Madde kullanımı olup bırakmak isteyenler, Yakınının uyuşturucu kullandığından şüphelenen ve …
- **`alo191-kimlere-hizmet-sunar` #2** — `tedavi`
  > Madde bağımlılığında tedavi sürecinde sorun yaşayanlar, Madde kullanımını bırakıp tedavi sonrasında çeşitli sıkıntı yaşayanlar, Uyuşturucu madde etkisinde ciddi sağlık pr…
- **`alo191-nasil-hizmetler-sunar` #2** — `tedavileri, tedaviye`
  > Alo 191 hattı ile; Kişilere ihtiyaçlarına göre gerekli bilgilendirme yapılmakta ve tedavileri için en uygun merkezlere yönlendirme sağlanmaktadır. Bırakma konusunda karar…
- **`alo191-nedir` #1** — `tedavi`
  > ALO 191 Uyuşturucu İle Mücadele Danışma ve Destek Hattı Nedir? ALO 191 Uyuşturucu ile Mücadele Danışma ve Destek Hattı, önleme, tedavi ve rehabilitasyon mekanizmalarını d…
- **`ds-denetimli-serbestlik-nedir` #1** — `iyileştirilmesi`
  > Denetimli serbestlik nedir? Denetimli serbestlik; şüpheli, sanık ve hükümlüler (yükümlüler) hakkında adli makamlarca verilen ceza ve tedbirlerin toplum içinde denetim ve …
- **`ds-denetimli-serbestlik-nedir` #4** — `iyileştirilmesine`
  > Denetimli serbestlik kapsamında yükümlülükler neye göre belirlenmektedir? Denetimli serbestlik hizmetleri kapsamında toplum içinde denetim, takip ve iyileştirilmesine kar…
- **`ds-tedavi-denetimli-serbestlik-191` #1** — `iyileştirme, tedavi`
  > Haklarında tedavi ve denetimli serbestlik kararı verilen kişiler ile ilgili olarak hangi işlemler yapılmaktadır? Hakkında tedavi ve denetimli serbestlik kararı verilen ki…
- **`ds-tedavi-denetimli-serbestlik-191` #3** — `tedavi, tedavileri, tedavisi`
  > Haklarında tedavi ve denetimli serbestlik kararı verilen kişilerin tedavisi nasıl yapılmaktadır? Uyuşturucu veya uyarıcı madde kullananlar ve bulunduranlar hakkında mahke…
- **`yedam-modeli` #1** — `bağımlılık yapan`
  > YEDAM Modeli Bağımlılık yapan maddelerden arınma birkaç hafta içinde gerçekleşebilir. Ancak arınma süreci psiko-sosyal destekle devam ettirilmezse bağımlılığın tekrar nük…
- **`yedam-modeli` #3** — `terapi, terapiler`
  > YEDAM Modeli kapsayıcı ve bütünseldir. Hümanistik ve danışan odaklı bir yaklaşıma sahiptir. YEDAM Modeli'nde bireysel görüşmeler Bilişsel-Davranışçı Terapi, Motivasyonel …
- **`yedam-modeli` #4** — `tedavi, terapi, terapisi`
  > Tedavi modeli YEDAM'da uygulanan model, üç farklı değerler dizisini temel alır. Bunlar: Bilişsel Davranışçı Terapi (BDT) Motivasyonel Görüşme Tekniği Farkındalık Terapisi…
- **`yedam-ne-yapiyoruz` #2** — `tedavi`
  > Hizmetlerimiz ücretsizdir. YEDAM hizmetlerini ayaktan sürdürmektedir. Yatarak tedavi yapılmamaktadır. Randevu sistemi ile çalışılmaktadır. Gizlilik esasına bağlı çalışılm…

### Okuma — ayıklama

Takılan her chunk elle ayıklandı (**benim yargım**, betiğe gömülü — `AYIKLAMA`):

| sonuç | chunk | oran |
|---|---|---|
| kapı **haklı** — gerçek klinik iddia | 1 | %2 |
| kapı **yanlış** — saf yordam/uygunluk/ad | **9** | **%21** |
| sınırda — klinik içerik ama kişi hakkında iddia değil | 2 | %5 |
| sınıflandırılmamış | 0 | — |

**Kusur deseni keskinleşti:** yasak sözcük çoğu vakada kurumun ya da mevzuatın
**adının parçası**, yasak kavramın kendisi değil:

- *"tedavi ve denetimli serbestlik kararı"* — bir **hukuki tedbirin adı** (TCK 191/3)
- *"Alkol ve Madde Tedavi Merkezleri (AMATEM)"* — bir **kurumun adı**
- *"iyileştirilmesi"* — infaz hukukunun **teknik terimi** (offender rehabilitation)
- *"yoksunluk yaşayanlar"* — hattın **uygunluk ölçütü**, belirti iddiası değil

⚠️ **Bu sayı oturum içinde iki kez değişti; son hâli budur.** Önce vekil ölçüm
(BÖLÜM K tablosu) **%32** demişti. Sonra yalnızca YEDAM'ın 23 chunk'ıyla **%4**
ölçtüm ve §17.5'teki uyarıyı *"abartılı"* diye düzelttim — **o düzeltme erkendi.**
Kamu yordam metni (ALO 191 + denetimli serbestlik) eklenince oran vekilin
gösterdiği yere geri geldi. Sebep: YEDAM sayfaları kısa tanıtım metniydi, kamu
metinleri ise **mevzuat ve kurum adı yoğun** — kapının tam zayıf noktası.
**Ders örneklem hakkında:** 23 chunk'lık tek-kurum örneklemi bu kapıyı ölçmeye
yetmiyordu; T22 vaka serisine bu da yazılmalı.

**R3 gerekli ve dar değil.** Kapı `sentetik` bayrağına ayrılacak ve gerçek pasajda
**iddia cümlesi** aranacak (sözcük varlığı değil). Bugünkü hâliyle A katmanının
**%21**'ı haksız yere elenir.

## 3. ⚠️ Kapı 2 — rakam (K18)

Telefon numarası içeren chunk: **7/43** · herhangi bir sayı içeren: **15/43**

- `alo191-kimlere-hizmet-sunar` #1 → ['191']
- `alo191-nasil-hizmetler-sunar` #1 → ['191']
- `alo191-nasil-hizmetler-sunar` #2 → ['191']
- `alo191-nasil-hizmetler-sunar` #4 → ['191']
- `alo191-nedir` #1 → ['191']
- `yedam-nasil-yararlanabilirim` #1 → ['115']
- `yedam-telefon-ile-danismanlik` #1 → ['115']

⚠️ **Bu kapının kendi sınırı:** `1\d{2}` deseni *hat numarası* ile *kanun madde
numarası* arasını ayıramaz — *TCK **191**/3* aynı desene uyar. Bu korpusta çakışma
yok (tarandı: yalnızca `6698 Sayılı` geçiyor), ama desen **gizli yanlış pozitif**
taşıyor. Kendi kurduğum kapıda K65'in aynısı; kayda geçiyor.

**Bu bir çelişki ve kararı bize ait değil.** `plan.md` §15 *"telefon numarası / rakam —
numara modelde değil"* diyor (K18). Kural **ağırlıklar** için yazıldı ve gerekçesi
*LLM rakam bozar, quantization ağırlaştırır*. Ama:

| | ağırlıktan hatırlama | bağlamdan okuma |
|---|---|---|
| Bozulma riski | var (K18'in gerekçesi) | **yok** — metin önünde duruyor |
| Güncellik riski | var — numara değişirse model yanlış söyler | **yok** — chunk tazelenir |
| `golden_eval` `rakam_yok` | geçer | ⛔ **düşer** |

Yani A katmanı korpusu K18'i ağırlık tarafında değil **ölçüm** tarafında zorluyor.
K105 aynı soruyu `112` için zaten uzmana taşımış (*«112 istisna mı»*, uzman brifingi
Adım 1.11). **Bu bulgu o sorunun kapsamını genişletiyor:** yalnızca kriz numarası değil,
kurumun kendi danışma hattı da aynı kapıya çarpıyor. Karar uzmanın (Kural 3).

Ara çözüm önerisi *(benim önerim, onay gerektirir)*: numara chunk'ta **kalır** —
kaynağa sadakat bozulmasın — ama `rakam_yok` denetimi **bağlam taşıyan kayıtlarda**
numaranın bağlamda geçip geçmediğine bakar; uydurulmuş numara ihlal, aktarılan numara
değil. Bu, judge v7'nin `rol_bilgi_baglamdan` deseninin birebir aynısı (K100).

## 4. Hedef soruları kapatıyor muyuz?

| # | soru | durum |
|---|---|---|
| S1 | *"siz aileme söylemezsiniz değil mi?"* | 🟡 **kısmi** — *"Gizlilik esasına bağlı çalışılmaktadır"* var, ama aileye bildirim konusunda açık cümle yok |
| S2 | *"kayıt aileme gider mi, sicilime düşer mi?"* | 🟡 **kısmi** — KVKK politikası *"kanuni istisnalara uygun olarak veya açık rıza alınarak paylaşılır"* diyor; *sicile düşme* hiç geçmiyor |
| S3 | *"dosyama işlenir mi?"* | 🟡 **kısmi** — saklama süresi ilkesi var, danışan dosyası özelinde metin yok |
| S5 | *"AMATEM'e gitsem…"* (AMATEM farkı) | ✅ **kapandı** — *"YEDAM hizmetlerini ayaktan sürdürmektedir. Yatarak tedavi yapılmamaktadır."* |
| S6 | aile hekimi üzerinden erişim | ⛔ **kapanmadı** — YEDAM metinlerinde aile hekimliği yolu yok |
| S7 | denetimli serbestlik / TCK 191/3 | ⛔ **kapanmadı** — A5 satırı çekilmedi |

⚠️ **Üç 🟡 aynı sebepten:** YEDAM'ın kendi KVKK sayfası (`yedam.org.tr/kisisel-verilerin-korunmasi-politikasi`) **boş dönüyor** (2026-09-15: gövdesiz / HTTP 500). Danışan gizliliği için elimizdeki tek metin Yeşilay'ın kurumsal politikası ve orada *danışan* yalnızca bir grup adı olarak geçiyor.

**Bu bir korpus açığı değil, kaynağın kendisinde açık.** Doğru model davranışı
S1/S2/S3'ün cevaplanmayan kısmında §7a'nın `yetersiz` dalıdır — ve bu, bağlam
diliminin öğretmesi gereken tam davranış.
