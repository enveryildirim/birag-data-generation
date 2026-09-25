# k-geçiş toplama — kararsız judge'dan kullanılabilir ölçüm

- tarih: 2026-09-15 · betik: `scripts/analiz/2026-09-15-k-gecis-toplama.py`
- **3 bağımsız geçiş**, aynı judge (Sonnet), aynı rubrik (v7), aynı 104 kayıt
- istek dosyaları üç geçişte de `diff -rq` ile byte-byte aynı doğrulandı
  - 1. geçiş: `data/judged/v3-kumulatif.v7.jsonl` · SHA256 `fa2ce941a7cce793…`
  - 2. geçiş: `data/judged/v3-kumulatif.v7-kontrol.jsonl` · SHA256 `c5baebcc8a70e78b…`
  - 3. geçiş: `data/judged/v3-kumulatif.v7-ucuncu.jsonl` · SHA256 `3d07e3a9d7be62fe…`

⚠️ Bu betik **doğruyu bilmiyor**. Ölçtüğü şey **kararlılık**: aynı kuralın
farklı geçiş altkümelerine uygulanınca aynı sonucu verip vermediği. Kararlılık
doğruluk değildir (K61) — ama kararlılık yoksa doğruluk hiç ölçülemez.

## 1. Tek geçişin oynaklığı — sorunun büyüklüğü

| Bayrak | 1. geçiş | 2. geçiş | 3. geçiş | üçünde de | hiçbirinde |
|---|---:|---:|---:|---:|---:|

**Okuma:** *üçünde de* ile *hiçbirinde* toplamı 104'ten ne kadar uzaksa,
o boyutta o kadar çok kayıt geçişten geçişe yer değiştiriyor.

## 2. ⭐ `any` mi çoğunluk mu — sert kapılarda

Eksen 2 sıfır toleranslı. Orada iki hata **simetrik değil**: kaçırılan bir
güvenlik ihlali, fazladan bir işaretten çok daha pahalı. Bu yüzden doğru
toplama kuralı `any`.

| Bayrak | kural | k=1 (ortalama) | k=2 | k=3 |
|---|---|---:|---:|---:|
| `klinik_guvenlik_ihlali` | `any` | 1.3 | 2.3 | 3 |
| `klinik_guvenlik_ihlali` | `çoğunluk` | 1.3 | 0.3 | 1 |
| `rol_siniri_ihlali` | `any` | 0.0 | 0.0 | 0 |
| `rol_siniri_ihlali` | `çoğunluk` | 0.0 | 0.0 | 0 |
| `bos_guvence` | `any` | 7.3 | 10.3 | 12 |
| `bos_guvence` | `çoğunluk` | 7.3 | 4.3 | 7 |

⚠️ **`çoğunluk` sert kapıda İŞE YARAMIYOR ve nedeni yapısal:** taban oranı
%1-3 iken üç geçişin ikisinin aynı kayıtta ateşlemesi neredeyse hiç olmuyor.
Çoğunluk kuralı bu eksende sinyali **bastırıyor**, kararlı hâle getirmiyor.

`any` ise ateşleme sayısını artırıyor — ama bu "daha çok yanlış pozitif" demek
değil, **"tek geçişin kaçırdığını yakalıyor"** demek. Hangisinin doğru olduğu
bu veriyle bilinemez (uzman çapası yok); bilinen tek şey tek geçişin kaçırdığı.

## 3. `any-of-k` doyuyor mu — kaç geçiş yeter

| Bayrak | k=1 | k=2 | k=3 | k=2→3 artış |
|---|---:|---:|---:|---:|
| `klinik_guvenlik_ihlali` | 1.3 | 2.3 | 3 | +0.7 |
| `rol_siniri_ihlali` | 0.0 | 0.0 | 0 | +0.0 |
| `bos_guvence` | 7.3 | 10.3 | 12 | +1.7 |
| `tuzak_suclama` | 0.0 | 0.0 | 0 | +0.0 |
| `cevapsiz_soru` | 1.3 | 2.3 | 3 | +0.7 |

**Doygunluk yoksa k'yı artırmak yeni işaret bulmaya devam eder** — yani
gerçek oran hâlâ bilinmiyor. Doygunluk varsa k orada kesilebilir.

## 3b. ⭐ Yakala-tekrar yakala — k=3'te hâlâ kaç işaret kaçıyor

§3 doygunluk göstermedi: her geçiş yeni kayıt buluyor. O zaman asıl soru
*"kaç geçiş yeter"* değil, **"şu an kaçını görüyoruz"**. Her geçişi bir
*yakalama seferi* saymak bu soruyu cevaplıyor (Chao1 tahmincisi):

> `f1` = yalnızca BİR geçişte görülen kayıt · `f2` = tam iki geçişte ·
> `f3` = üçünde de. Tahmin: `S + f1²/(2·f2)`.

| Bayrak | f1 | f2 | f3 | `any-of-3` | **tahmini gerçek** | görülen pay |
|---|---:|---:|---:|---:|---:|---:|
| `klinik_guvenlik_ihlali` | 2 | 1 | 0 | 3 | **5.0** | %60 |
| `rol_siniri_ihlali` | 0 | 0 | 0 | 0 | **0.0** | — |
| `bos_guvence` | 5 | 4 | 3 | 12 | **15.1** | %79 |
| `cevapsiz_soru` | 2 | 1 | 0 | 3 | **5.0** | %60 |
| `tuzak_etiketleme` | 1 | 0 | 0 | 1 | **1.0** | %100 |

⛔ **`klinik_guvenlik_ihlali`: `any-of-3` ile 3 kayıt görüyoruz, tahmin 5.**
Yani sıfır toleranslı eksende, üç geçişten sonra bile judge'ın **yakalayabileceği**
işaretlerin ~%60'ını görüyoruz. k=3 yetmiyor.

✅ **`rol_siniri_ihlali`: f1=f2=f3=0, tahmin 0.** Üç bağımsız geçişte sıfır —
v7'nin RAG düzeltmesi artık tek koşuya değil **üç koşuya** dayanıyor. Bu, bu
oturumdaki en sağlam bulgu.

⚠️ **Tahminci varsayımı ihlal ediliyor ve yön BELLİ.** Chao1 yakalamaların
bağımsız olduğunu varsayar; üç geçiş aynı model ve aynı prompt olduğu için
**pozitif korelasyonlu**. Pozitif korelasyon kaçan sayısını *küçük* gösterir →
**5 bir ALT sınırdır**, gerçek sayı daha yüksek olabilir.

⚠️ Ayrıca bu, *"korpusta 5 güvenlik ihlali var"* demek DEĞİL. Tahmin edilen şey
**judge'ın işaretleyebileceği kayıt sayısı**; işaretin doğru olup olmadığı ayrı
bir soru ve uzman çapası yok.

## 4. Sayısal eksenler — ortalama almanın kazancı

Kalite boyutlarında iki hata simetrik, o yüzden doğru toplama **ortalama**.
Kazanç standart hatada: k geçişin ortalaması, tek geçişten √k kat daha durağan
olmalı. Ölçülen:

| Eksen | tek geçiş ort. | 3 geçiş ort. | kayıt içi s (tek) | kayıt içi s (3 ort.) | kazanç |
|---|---:|---:|---:|---:|---:|
| `anlasilirlik_holistik` | 4.61 | 4.78 | 0.249 | 0.144 | 1.73× |
| `dogallik_holistik` | 4.36 | 4.40 | 0.304 | 0.175 | 1.73× |
| `mi_uyumu_holistik` | 4.82 | 4.80 | 0.150 | 0.086 | 1.73× |
| `duygusal_tepki` | 1.18 | 1.23 | 0.215 | 0.124 | 1.73× |
| `yorumlama` | 1.71 | 1.74 | 0.160 | 0.092 | 1.73× |
| `kesif` | 1.07 | 1.02 | 0.109 | 0.063 | 1.73× |
| `grounding` | 4.94 | 4.92 | 0.041 | 0.024 | 1.73× |
| `anlasilirlik` | 3.49 | 3.44 | 0.413 | 0.239 | 1.73× |
| `dogallik` | 4.88 | 4.91 | 0.050 | 0.029 | 1.73× |
| `mi_uyumu` | 4.99 | 4.99 | 0.014 | 0.008 | 1.73× |

⚠️ *kayıt içi s (3 ort.)* ölçülmedi, **türetildi** (s/√3). Gerçek kazancı
ölçmek için 3 geçişlik İKİ bağımsız üçlü gerekirdi, yani 6 geçiş.
Buradaki sütun bir üst sınır tahminidir ve öyle okunmalı.

## 5. ⭐ Karar ve maliyeti

| Eksen | Toplama kuralı | Gerekçe |
|---|---|---|
| **Eksen 2** sert kapılar | `any-of-k`, **k≥3 ve doygunluk ölçülerek** | yanlış negatif yanlış pozitiften pahalı |
| Eksen 1 kalite boyutları | **3 geçişin ortalaması** | iki hata simetrik |
| Eksen 1 ikili bayraklar | `çoğunluk-of-3` | taban oranı yüksek, çoğunluk çalışıyor |
| Eksen 3 | **toplama yok** | judge hiç kullanılmıyor, deterministik |
| Eksen 4/5 otomatik iddialar | **toplama yok** | deterministik |
| Eksen 4/5 judge iddiaları | Eksen 1 ile aynı | |

**Maliyet: judge çağrısı ×3.** Korpusta 104 kayıt → 312 çağrı. Eval
koşusunda da aynı çarpan geçerli ve bu, K45'te ölçülen judge darboğazını
(3× süre) doğrudan büyütüyor.

**Kazanç, sert kapıda somut:** `klinik_guvenlik_ihlali` tek geçişte ortalama
**1.3** kayıt işaretliyor, `any-of-3` ile **3**. Yani tek geçiş,
üç geçişin bulduğunun **%44**'ini buluyor. Sıfır toleranslı
bir eksende bu fark kabul edilemez.

⛔ **AMA k=3 DE YETMİYOR.** §3b'nin yakala-tekrar yakala tahmini `any-of-3`'ün
gördüğü 3 kaydın karşısına **5** koyuyor ve bu bir alt sınır. Yani karar
*"k=3 kullan"* değil, **"k'yı doygunluk görülene kadar artır ve doygunluğu**
**raporla"**. Bir sonraki adım 4. ve 5. geçiş; f1/f2 eğrisi düzleşiyor mu.

⛔ **Bu bir doğruluk iddiası DEĞİL.** `any-of-3`'ün bulduğu kayıtların gerçekten
ihlal olup olmadığı bilinmiyor — uzman çapası yok ve bedensel kırmızı bayrak
sorusu hâlâ açık (`data/guvenlik-karantinasi.jsonl`). Bilinen tek şey: **tek
geçişle ölçmek, ölçmemektir.**

