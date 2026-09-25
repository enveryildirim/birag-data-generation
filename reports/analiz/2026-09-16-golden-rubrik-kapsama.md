# Golden eval seti rubriğin ne kadarını **sınıyor**

**Betik:** `scripts/analiz/2026-09-16-golden-rubrik-kapsama.py` · **Tarih:** 2026-09-16  
**Rubrik:** `judge-eksen1.v9` · `src/schemas.py` SHA256 `62c0d0664d2e1987`  
**Golden:** `golden.dev.jsonl` `1396c6713e9b2b5d` · `golden.locked.jsonl` `e8f330c4479d2a88` · `golden.test.jsonl` `2608b58a989f9df1`

---

## Nasıl bulundu

`2026-09-14-golden-dev.py` kendi raporunu yeniden üretemedi (K126 denetimi).
Sebep tarih değil **girdi**: betik canlı rubriği okuyor. 09-14'te rubrikte
**37** boyut vardı ve o günün raporundaki *«öğe düzeyinde kapanmamış boyut
kalmadı»* cümlesi **doğruydu**. Bugün rubrik `judge-eksen1.v9`,
**75** boyut. Golden seti (K31 mühürlü) yerinde kaldı.

⚠️ Eşiksiz boyut *«ölçülmüyor»* demek DEĞİL: judge her boyutu her cevapta
puanlar. Demek ki **gerileme sayıda görünür, başarısızlık sayılmaz**.

## Ölçüm

| | |
|---|---:|
| Golden öğe | 144 |
| Rubrik boyutu (hüküm dışı alanlar hariç) | **75** |
| Eşik konulmuş boyut | **22** |
| Eşiksiz — bütünsel/üslup (öğe eşiği anlamsız) | 15 |
| Eşiksiz — girdi tasarımı gerektiren | 38 |
| ⛔ bunlardan **başarısızlık taşıyabilecek** (bool) | **17** |
| ⚠️ bunlardan kanıt/kategori alanı (metin, eşik anlamsız) | 21 |

➡️ ⭐ **Keskin sayı 17, 38 değil.** 38'in 21'i `rol_kaynak_turu`, `teselli_kalip` gibi **kanıt/kategori**
alanı: bunlara *«false olmalı»* denemez, eşik kavramı uymuyor. Geriye kalan
**17 bool bayrağı** ise gerçek kusur bayrağı — golden bugün o
kusurları **yakalayabilecek tek bir öğe bile taşımıyor**.

### ⛔ Hiç sondalanmayan boyutlar

| Boyut | tip |
|---|---|
| `alinti_dogrulama` | metin |
| `alinti_dogrulanmadi` | metin |
| `ayrinti_hipotez_olarak_isaretli` | bool |
| `ayrinti_konusmada_var` | bool |
| `en_somut_ayrinti` | metin |
| `en_teselli_edici` | metin |
| `etiket_kullanicinin` | bool |
| `genelleme_kategori_mi` | bool |
| `guvenlige_en_yakin` | metin |
| `guvenlik_tipi` | metin |
| `kisiye_dair_en_genel` | metin |
| `kullanicinin_kendi_sucu` | bool |
| `kurum_adi` | metin |
| `kurum_adi_kullanicidan` | bool |
| `kurum_yordam_en_yakin` | metin |
| `kurum_yordam_ihlali` | bool |
| `kusur_kullanicida_ima` | bool |
| `rol_alani` | metin |
| `rol_baglam_alintisi` | metin |
| `rol_bilgi_baglamdan` | bool |
| `rol_iddiasi` | metin |
| `rol_kaynak_turu` | metin |
| `rol_reddediyor` | bool |
| `rol_risk_olasilik_olarak` | bool |
| `rol_sinirina_en_yakin` | metin |
| `sorumluluga_en_yakin` | metin |
| `teselli_dayanak_alintisi` | metin |
| `teselli_dayanak_dogrulandi` | bool |
| `teselli_dayanakli` | bool |
| `teselli_islevi` | metin |
| `teselli_kalip` | bool |
| `teselli_kullanici_alintisi` | metin |
| `teselli_kullanicinin_sozunden` | bool |
| `teselli_ozgu_oge` | metin |
| `utanc_buyutuyor` | bool |
| `yordam_baglam_alintisi` | metin |
| `yordam_baglamdan` | bool |
| `yordam_iddiasi` | metin |

### Bütünsel/üslup — korpus düzeyi eşik gerekir

`anlasilirlik` · `anlasilirlik_holistik` · `belirsiz_gonderge` · `devrik_eksiltili` · `dil_butunlugu` · `dogallik` · `dogallik_holistik` · `kisalik_dogallik` · `kurulmamis_mecaz` · `mi_uyumu_holistik` · `siz_kaymasi` · `soyut_adlastirma` · `terapi_jargonu` · `tuzak_ihlali` · `ust_uste_yan_cumle`

## ⭐ Karar

| | |
|---|---|
| ⛔ Açık | **17** bool kusur bayrağında golden **gerileme yakalayamaz** (38 eşiksizin kusur taşıyabileni) |
| ⛔ K31 | mühürlü set DEĞİŞTİRİLEMEZ — kapatma yolu **İKİNCİ bir set** |
| ⚠️ Kaynak | açığın tamamı v8/v9'un kanıta bağlı alanları (`alinti_*`, `teselli_*`, `rol_*`, `yordam_*`, `kurum_*`) |
| ➡️ Kural 7 | `golden-dev` artık rubrik sürümünü **ilan ediyor**; rubrik büyüdüğünde bu betik yeniden koşulur |

⚠️ **17 de bir üst sınır.** Bool bayraklarının bir kısmı ihlal değil **kanıt** bayrağı (`teselli_dayanakli`, `ayrinti_konusmada_var`, `rol_bilgi_baglamdan`, `kurum_adi_kullanicidan`, `etiket_kullanicinin`, `teselli_dayanak_dogrulandi`): bunlara *«false olmalı»* demek de anlamsız. Kesin ihlal bayrağı olanlar: `kurum_yordam_ihlali`, `kusur_kullanicida_ima`, `kullanicinin_kendi_sucu`, `utanc_buyutuyor`, `genelleme_kategori_mi`, `teselli_kalip`. ➡️ Ayrımı **otomatik yapmadım** — her alanın niyetini okumak gerekir ve bu klinik bir karardır (Kural 3). Sayı bu yüzden *«en çok 17, en az 6»* diye raporlanır.
