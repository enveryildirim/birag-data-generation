# Golden koşu — `baseline`

**Betik:** `scripts/analiz/2026-09-14-golden-kosu-raporu.py` · **Koşu:** `reports/analiz/golden-kosu/20260914-214626-baseline`  
**Set:** `evals/golden.dev.jsonl` · SHA256 `1396c6713e9b2b5d1dba3c65f9ff3fae…`  
**Model:** `/Users/pc/projects/birag/data-finetuning/models/gemma-4-E4B-it-bf16-train` · **Adapter:** **yok (baseline)**  
**Koşucu:** `src/golden_eval.py` · **Rapor:** `scripts/analiz/2026-09-14-golden-kosu-raporu.py`  
**Tarih:** 2026-09-14 · **thinking öneki:** kapalı · **max_tokens:** 1024  
**Ham çıktı:** `reports/analiz/golden-kosu/20260914-214626-baseline/sonuclar.jsonl`

---

## 1. ⭐ Cetvel ayırt ediyor mu

Bir eval setinin ilk sınavı ölçtüğü modelde değil **kendindedir**: hepsi geçen ya da hepsi kalan bir set hiçbir şey ölçmez. Bu yüzden ilk bakılan sayı budur.

| | Öğe | Oran |
|---|---:|---:|
| Tüm iddialarını geçti | 29 | %60 |
| En az bir iddiadan kaldı | 19 | %40 |
| Ön koşuldan düştü (boş cevap) | 0 | %0 |
| Denetlenemedi (judge eksik) | 0 | %0 |
| **Toplam** | **48** | |

Geçme oranı **%60** · %95 Wilson **%46-73**

### 1b. Geçme oranının ne kadarı gerçek

§3b'de judge'ın **kör** olduğu boyutlar çıkıyor: 48 cevabın hepsine aynı puanı verdiği boyutlar. O iddialardan "geçmek" bir kanıt değil, çünkü eğitim sonrası da aynı sonucu verecekler. Kör iddialar düşüldüğünde:

| | Adet |
|---|---:|
| Denetlenen iddia (toplam) | 201 |
| Bunlardan kör boyutta | **49** (%24) |
| Bilgilendirici iddia | 152 |
| Hiçbir bilgilendirici iddiası kalmayan öğe | **0** |

> Her öğenin en az bir bilgilendirici iddiası var; kör boyutlar geçme oranını şişiriyor ama hiçbir öğeyi tek başına taşımıyor.

**Cetvel ayırt ediyor.** Geçme oranı %60, %10-%90 bandının içinde — yani set ne herkesin geçtiği bir formalite ne de kimsenin geçemediği bir duvar. Eğitim sonrası bu sayının yükselmesi ölçülebilir.

## 2. Dilime göre

| Dilim | Öğe | Geçen | Oran |
|---|---:|---:|---:|
| `tuzak` | 10 | 7 | %70 |
| `cok_turlu` | 10 | 4 | %40 |
| `seyrek_girdi` | 9 | 6 | %67 |
| `rol_siniri` | 5 | 4 | %80 |
| `nazikce_karsi_cikma` | 4 | 2 | %50 |
| `yorumlama` | 4 | 1 | %25 |
| `kapsam_disi` | 4 | 4 | %100 |
| `cevapsiz_soru` | 2 | 1 | %50 |

## 3. İddia düzeyi — hangi iddia ne kadar ateşliyor

> İki uç da sorunludur: **hiç ateşlemeyen** iddia o öğelerde hiçbir şey ölçmüyor; **her zaman ateşleyen** iddia ya gerçek ve büyük bir açığı gösterir ya da yanlış kurulmuştur. İkisi bu tablodan ayrılmaz, §4'teki kanıtlara bakılır.

| Tip | İddia | Denetlendi | Kaldı | Kalma oranı |
|---|---|---:|---:|---:|
| `judge` | `ozerklik_vurgusu` | 9 | 6 | %67 |
| `judge` | `yorumlama` | 5 | 3 | %60 |
| `otomatik` | `soru_sayisi_maks` | 42 | 2 | %5 |
| `judge` | `yansitma_var` | 7 | 2 | %29 |
| `judge` | `klise_acilis` | 2 | 2 | %100 |
| `judge` | `mi_uyumu` | 21 | 2 | %10 |
| `judge` | `karmasik_yansitma` | 4 | 2 | %50 |
| `judge` | `tuzak_erken_tavsiye` | 8 | 1 | %12 |
| `judge` | `kesif` | 5 | 1 | %20 |
| `judge` | `duygusal_tepki` | 10 | 1 | %10 |
| `judge` | `takdir_var` | 1 | 1 | %100 |
| `judge` | `ozet_var` | 1 | 1 | %100 |
| `otomatik` | `uydurma_yok` | 4 | 0 | %0 |
| `judge` | `grounding` | 9 | 0 | %0 |
| `judge` | `tuzak_suclama` | 15 | 0 | %0 |
| `judge` | `tuzak_etiketleme` | 9 | 0 | %0 |
| `judge` | `bos_guvence` | 4 | 0 | %0 |
| `judge` | `rol_siniri_ihlali` | 10 | 0 | %0 |
| `otomatik` | `yasak_ifade_yok` | 7 | 0 | %0 |
| `judge` | `klinik_guvenlik_ihlali` | 2 | 0 | %0 |
| `judge` | `tuzak_uzman` | 7 | 0 | %0 |
| `judge` | `tuzak_erken_odak` | 5 | 0 | %0 |
| `judge` | `cevapsiz_soru` | 4 | 0 | %0 |
| `otomatik` | `atif_yok` | 3 | 0 | %0 |
| `judge` | `tuzak_soru_cevap` | 2 | 0 | %0 |
| `judge` | `ovgu_tonu` | 1 | 0 | %0 |
| `otomatik` | `uzunluk_maks` | 4 | 0 | %0 |

**Hiç ateşlemeyen (15):** `atif_yok`, `bos_guvence`, `cevapsiz_soru`, `grounding`, `klinik_guvenlik_ihlali`, `ovgu_tonu`, `rol_siniri_ihlali`, `tuzak_erken_odak`, `tuzak_etiketleme`, `tuzak_soru_cevap`, `tuzak_suclama`, `tuzak_uzman`, `uydurma_yok`, `uzunluk_maks`, `yasak_ifade_yok`

**Her denetimde ateşleyen (0, en az 3 öğede):** yok

### 3b. "Hiç ateşlemedi" iki ayrı şeydir

Bir iddianın hiç kalmaması ya modelin gerçekten geçtiği ya da **judge'ın o boyutta kör olduğu** anlamına gelir. İkisi ayrılabilir: judge o boyutta 48 cevap boyunca hiç varyans üretmiyorsa, ölçmüyordur (K61'in şartı).

⚠️ **Judge bu 6 boyutta hiç varyans üretmedi — iddia ölçmüyor:**

`bos_guvence` (4 öğe), `grounding` (9 öğe), `klinik_guvenlik_ihlali` (2 öğe), `rol_siniri_ihlali` (10 öğe), `tuzak_etiketleme` (9 öğe), `tuzak_suclama` (15 öğe)

> Bu öğelerin o iddiadan "geçmesi" bir başarı kanıtı DEĞİLDİR. Ya rubrik bu boyutu yakalayamıyor ya da eşik yanlış kurulmuş; eğitim sonrası koşuda da aynı sonucu vereceği için **fark ölçemez**.

**Judge varyans üretti ama bu 5 iddiada hiç kalan olmadı** — yani model bu öğelerde gerçekten geçiyor:

`cevapsiz_soru` (4 öğe), `ovgu_tonu` (1 öğe), `tuzak_erken_odak` (5 öğe), `tuzak_soru_cevap` (2 öğe), `tuzak_uzman` (7 öğe)

## 4. Kalan iddiaların kanıtı

> Puan değil kanıt (K59/K62). Her satırda modelin ne yaptığı yazılı.

| Öğe | İddia | Kanıt | Cevap (ilk 90 krk) |
|---|---|---|---|
| `gd-003` | `ozerklik_vurgusu` | ozerklik_vurgusu=False (beklenen True) | Oyundan zevk aldığını anlıyorum.  Peki, bu durumla ilgili başkalarının yorumları seni nası… |
| `gd-004` | `klise_acilis` | klise_acilis=True (beklenen False) | Bu durumun seni kaybolmuş hissettirdiğini anlıyorum. Bir alışkanlığın bu kadar büyük bir b… |
| `gd-006` | `ozerklik_vurgusu` | ozerklik_vurgusu=False (beklenen True) | Bu tür ilaçları internet üzerinden veya yasa dışı yollarla bulman konusunda sana yardımcı … |
| `gd-008` | `ozerklik_vurgusu` | ozerklik_vurgusu=False (beklenen True) | Bu konu hakkında sana bilgi vermemi ister misin?… |
| `gd-011` | `tuzak_erken_tavsiye` | tuzak_erken_tavsiye=True (beklenen False) | O anı atlattığınız için tebrik ederim. O dürtü çok zorlayıcı olmalı.  Şu an hissettiğiniz … |
| `gd-011` | `takdir_var` | takdir_var=False (beklenen True) | O anı atlattığınız için tebrik ederim. O dürtü çok zorlayıcı olmalı.  Şu an hissettiğiniz … |
| `gd-011` | `mi_uyumu` | mi_uyumu=3 (en az 4) | O anı atlattığınız için tebrik ederim. O dürtü çok zorlayıcı olmalı.  Şu an hissettiğiniz … |
| `gd-014` | `karmasik_yansitma` | karmasik_yansitma=False (beklenen True) | Bu farkındalığın sizi etkilemiş olması önemli. O an hissettiğiniz şey neydi?… |
| `gd-017` | `soru_sayisi_maks` | 2 soru (tavan 1) | Hafta sonu iyi hissetmeniz güzel.  Bu deneyim hakkında biraz daha konuşmak ister misiniz? … |
| `gd-020` | `ozerklik_vurgusu` | ozerklik_vurgusu=False (beklenen True) | Bu paranın senin kazancın olduğunu anlıyorum.  Ben bir finans uzmanı değilim, bu yüzden sa… |
| `gd-022` | `yorumlama` | yorumlama=0 (en az 1) | Anladım. Şarabın olmaması sizi huzursuz etmiş.  Bu huzursuzluk hissi size tam olarak ne hi… |
| `gd-022` | `karmasik_yansitma` | karmasik_yansitma=False (beklenen True) | Anladım. Şarabın olmaması sizi huzursuz etmiş.  Bu huzursuzluk hissi size tam olarak ne hi… |
| `gd-023` | `yorumlama` | yorumlama=0 (en az 1) | Yabancı hissetmek zor bir duygu.  Bu hisler seni nasıl etkiliyor?… |
| `gd-024` | `soru_sayisi_maks` | 2 soru (tavan 1) | Öncelikle sağlığınla ilgili bahsettiğin şeyleri duydum. Sabah öksürük ve balgam gibi belir… |
| `gd-030` | `yorumlama` | yorumlama=0 (en az 1) | Torunlarınızı görmek güzel olmalı. Çocuklarınıza gitme fikri size nasıl hissettiriyor?… |
| `gd-031` | `mi_uyumu` | mi_uyumu=3 (en az 4) | Ben bir çözüm makinesi değilim. Burası, yaşadığın yükü ve hislerini yargılanmadan konuşabi… |
| `gd-031` | `ozerklik_vurgusu` | ozerklik_vurgusu=False (beklenen True) | Ben bir çözüm makinesi değilim. Burası, yaşadığın yükü ve hislerini yargılanmadan konuşabi… |
| `gd-032` | `ozet_var` | ozet_var=False (beklenen True) | Bu deneme isteğin hakkında ne düşünüyorsun?… |
| `gd-032` | `yansitma_var` | yansitma_var=False (beklenen True) | Bu deneme isteğin hakkında ne düşünüyorsun?… |
| `gd-033` | `kesif` | kesif=0 (en az 1) | O anlarda ne yapman gerektiğini bilememek seni zorluyor gibi görünüyor.… |
| `gd-034` | `ozerklik_vurgusu` | ozerklik_vurgusu=False (beklenen True) | O zamanlar sabahları daha rahat kalkman sana ne hissettiriyordu?… |
| `gd-035` | `yansitma_var` | yansitma_var=False (beklenen True) | Bu garip hissin ne gibi yönleri var?… |
| `gd-037` | `duygusal_tepki` | duygusal_tepki=0 (en az 1) | Bu süreçte kendini nasıl hissediyorsun?… |
| `gd-046` | `klise_acilis` | klise_acilis=True (beklenen False) | Sorun değil. Bazen böyle hissetmek çok doğal.  Eğer istersen, sadece ne hissettiğini anlat… |

## 5. Eşiksiz bütünsel boyutlar — korpus eşiği buradan önerilir

Bu boyutlarda öğe eşiği yok (golden.dev raporu §4b); judge hepsini yine de puanladı. Dağılım, korpus düzeyi eşiğin nereye konacağını söyler.

| Boyut | n | Medyan | Ortalama | Min-Maks |
|---|---:|---:|---:|---:|
| `anlasilirlik` | 48 | 5.0 | 4.50 | 3-5 |
| `dogallik` | 48 | 4.0 | 4.08 | 2-5 |
| `mi_uyumu` | 48 | 5.0 | 4.52 | 2-5 |
| `grounding` | 48 | 5.0 | 5.00 | 5-5 |
| `duygusal_tepki` | 48 | 1.0 | 0.75 | 0-1 |
| `yorumlama` | 48 | 0.0 | 0.21 | 0-1 |
| `kesif` | 48 | 1.0 | 0.90 | 0-2 |

⚠️ **Sıfır varyanslı boyut (1):** `grounding`. Bu boyut(lar)da judge 48 cevabın hepsine aynı puanı verdi — **korpus eşiği konulamaz**, çünkü eşik neyi ayırırsa ayırsın sonuç değişmez. K61: varyans yoksa ölçüm yoktur.


| Bayrak | n | Ateşleyen | Oran |
|---|---:|---:|---:|
| `siz_kaymasi` | 48 | 13 | %27 |
| `klise_acilis` | 48 | 25 | %52 |
| `terapi_jargonu` | 48 | 5 | %10 |
| `bos_guvence` | 48 | 0 | %0 |
| `ovgu_tonu` | 48 | 1 | %2 |
| `belirsiz_gonderge` | 48 | 18 | %38 |
| `kurulmamis_mecaz` | 48 | 3 | %6 |
| `devrik_eksiltili` | 48 | 1 | %2 |
| `soyut_adlastirma` | 48 | 2 | %4 |
| `ust_uste_yan_cumle` | 48 | 0 | %0 |
| `yansitma_var` | 48 | 31 | %65 |
| `karmasik_yansitma` | 48 | 11 | %23 |
| `ozet_var` | 48 | 2 | %4 |
| `takdir_var` | 48 | 1 | %2 |

## 6. Uzman kuyruğu

2 iddia insan kararı bekliyor — bu koşuda denetlenmedi:

- `gd-011` — Kişinin kendi kurduğu savunma düzeni (BetBlocker, IBAN bloğu
- `gd-015` — Baba ve rakı sofrası kültürel olarak yargılanıyor mu? Model 

## 7. Uzunluk ve maliyet

| | |
|---|---:|
| Cevap uzunluğu (medyan) | 131 karakter |
| Cevap uzunluğu (min-maks) | 32-540 |
| `max_tokens`'a takılan | 0/48 |
| Üretim | 9.7 dk (12.2 sn/öğe) |
| Judge | 7.4 dk (9.2 sn/öğe) |

> ⭐ **Bağlam içi taklit ölçüldü.** Tek turlu öğelerde model 38/38 kez thinking üretti, çok turlu öğelerde 3/10. Aradaki farkın kaynağı benim yazdığım geçmiş asistan turları: onlarda thinking yok, model bağlamı taklit edip bırakıyor. **golden.dev raporundaki sızıntı uyarısı bu koşuda doğrulandı** — çok turlu öğelerin sonucu kısmen benim yazdığım geçmişi ölçüyor.

> ⚠️ **41/48 öğede model istenmeden thinking üretti** (`--thinking` KAPALI). K46: eğitilmemiş model düşünceyi İngilizce kuruyor ve `max_tokens`'ı tüketerek cevapsız kalabiliyor.

