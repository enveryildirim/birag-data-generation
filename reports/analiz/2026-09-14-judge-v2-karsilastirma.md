# Judge rubriği v1 → v2 — rubrik ölçmeye başladı mı?

**v1 çıktısı:** `data/judged/expert-70.jsonl` · SHA256 `c5e179ee0992ca64622078907f6e83f51378f3ca7fddffb81235bddd82ce82d4`  
**v2 çıktısı:** `data/judged/expert-70.v2.jsonl` · SHA256 `8988a94e7be238c4a71a538638601fd3b41c821dd5e8f5a9355d0efad409850a`  
**Uzman puanları:** `data/expert_sample/uzman-puanlari.json` · SHA256 `d9d36c10691157a90173da8452ceffc47c3d88782b91bd7a8e4ecf11e492263c`  
**Betik:** `scripts/analiz/2026-09-14-judge-v2-karsilastirma.py` · **Tarih:** 2026-09-14  
**Eşleşen kayıt:** 48 (uzmanın puanladığı ve iki rubrikle de puanlanan)

> ⚠️ **2 kayıt kapıda düştüğü için karşılaştırma dışı.** Kapıdan düşen kayıt judge'a gitmiyor (`filter.py` sözleşmesi); v1 koşusunda bu kapı yoktu, o yüzden v1 tarafında puanları var. form 9 (kabul): thinking:completion oranı 4.01x > 4.0x tavanı · form 10 (kabul): thinking:completion oranı 4.16x > 4.0x tavanı



> ⚠️ **Kalibrasyon testi, genelleme testi değil.** v2 rubriği uzmanın bulduğu kusur *türlerini* tarif ediyor; uzmanın reddettiği 5 gerçek cümle prompt'a konulmadı ama kusur türleri konuldu. Sonuç şunu söyler: v2 bu korpusta ayrım yapıyor. Yeni bir korpusta da yapacağını söylemez — onun için ikinci bir uzman turu gerekir.

---

## 1. Tavan etkisi — judge hâlâ herkese tam puan veriyor mu?

v1'in kusuru: `dil_butunlugu`'nde 50 kaydın 50'sine de 5 verdi (s=0.00). Ayrım yapmayan boyut hiçbir şey ölçmez.

| Rubrik · boyut | n | Ortalama | s | Dağılım | Tam puan oranı |
|---|---:|---:|---:|---|---:|
| `v1` · dil_butunlugu | 70 | 5.00 | 0.00 | `{5: 70}` | %100 |
| `v1` · kisalik_dogallik | 70 | 4.84 | 0.55 | `{2: 1, 3: 3, 4: 2, 5: 64}` | %91 |
| `v1` · grounding | 70 | 4.56 | 1.12 | `{1: 5, 2: 1, 3: 2, 4: 4, 5: 58}` | %83 |
| `v1` · mi_uyumu | 70 | 4.43 | 0.89 | `{1: 1, 2: 4, 3: 1, 4: 22, 5: 42}` | %60 |
| `v2` · anlasilirlik | 68 | 4.26 | 0.44 | `{4: 50, 5: 18}` | %26 |
| `v2` · dogallik | 68 | 3.76 | 0.62 | `{2: 3, 3: 14, 4: 47, 5: 4}` | %6 |
| `v2` · grounding | 68 | 4.91 | 0.37 | `{3: 2, 4: 2, 5: 64}` | %94 |
| `v2` · mi_uyumu | 68 | 4.12 | 0.83 | `{2: 5, 3: 5, 4: 35, 5: 23}` | %34 |

## 2. Ayrım gücü — uzmanın `ret` dediklerini judge ayırabiliyor mu?

Ölçüt: rastgele bir (`ret`, `kabul`) çiftinde judge'ın **ret'e daha düşük** puan verme olasılığı (Mann-Whitney uyum oranı). **0.50 = tesadüf.**

Uzmanın kararları: `kabul` 32 · `sınırda` 11 · `ret` 5

| Rubrik · boyut | ret ort. | sınırda ort. | kabul ort. | uyum oranı | %95 aralık |
|---|---:|---:|---:|---:|:---:|
| `v1` · dil_butunlugu | 5.00 | 5.00 | 5.00 | 0.50 ❌ | 0.22 – 0.78 |
| `v1` · kisalik_dogallik | 5.00 | 5.00 | 4.81 | 0.45 ❌ | 0.19 – 0.72 |
| `v1` · mi_uyumu | 4.80 | 4.55 | 4.34 | 0.33 ❌ | 0.10 – 0.56 |
| `v1` · grounding | 5.00 | 4.91 | 4.56 | 0.41 ❌ | 0.15 – 0.66 |
| `v2` · anlasilirlik | 4.20 | 4.18 | 4.25 | 0.53 ❌ | 0.25 – 0.80 |
| `v2` · dogallik | 3.40 | 3.82 | 3.66 | 0.57 ❌ | 0.29 – 0.85 |
| `v2` · mi_uyumu | 4.20 | 4.18 | 3.91 | 0.41 ❌ | 0.15 – 0.67 |
| `v2` · grounding | 5.00 | 4.82 | 4.88 | 0.47 ❌ | 0.20 – 0.74 |

> ✅ ≥ 0.75 · ⚠️ ≥ 0.60 · ❌ < 0.60 — **bu eşikler bizim konvansiyonumuz** (Kural 6).

## 3. `cevapsiz_soru` — v1'de hiç olmayan boyut

70 kaydın **1**'inde işaretlendi; uzmanın puanladığı 50'nin **1**'inde.

| Form | Uzman kararı | Judge'ın alıntıladığı soru |
|---|---|---|
| 38 | ret | Acaba bunu yazdığımda kayıt aileme gider mi, ya da ileride işe girersem sicilime düşer mi? |

**Kritik sınama.** Bu boyutun hedeflediği kusurdan ötürü uzmanın reddettiği kayıt **form 38**'dir (kayıt #19): *"bağlam içerisinde paylaşılmaz diyor ama cevap verilmesi gerekiyor, bu cevabı vermemiş"*. Form 27 (#30) de aynı **izin isteme kalıbını** taşıyor ama uzmanın oradaki gerekçesi cevapsızlık değil *anlaşılmazlık*: *"bu cümle net değil"* — yani form 27 `cevapsiz_soru` için değil, `anlasilirlik` için sınamadır. (Bu ayrımı ilk yazımda karıştırmıştım.)

- Form 38: `cevapsiz_soru` = **True** · `anlasilirlik` = 5 · (v1 `dil_butunlugu` = 5)
- Form 27: `cevapsiz_soru` = **False** · `anlasilirlik` = 4 · (v1 `dil_butunlugu` = 5)

## 4. Uzmanla kayıt düzeyi korelasyon

v1'de bütün boyutlar sıfıra yakındı (0.06 · −0.08 · 0.26 · −0.01 · −0.13 · −0.10).

| Uzman boyutu | v1 judge boyutu | r (v1) | v2 judge boyutu | r (v2) |
|---|---|---:|---|---:|
| duygusal_tepki (n=47) | `duygusal_tepki` | +0.06 | `duygusal_tepki` | -0.06 |
| yorumlama (n=47) | `yorumlama` | -0.11 | `yorumlama` | +0.01 |
| kesif (n=46) | `kesif` | +0.26 | `kesif` | +0.22 |
| mi_uyumu (n=18) | `mi_uyumu` | -0.04 | `mi_uyumu` | -0.20 |
| grounding (n=43) | `grounding` | -0.13 | `grounding` | -0.09 |
| dil_butunlugu (n=44) | `dil_butunlugu` | — | `anlasilirlik` | +0.00 |
| kisalik_dogallik (n=44) | `kisalik_dogallik` | -0.10 | `dogallik` | -0.20 |

> `—` = boyut sabit olduğu için korelasyon tanımsız (v1 `dil_butunlugu`: s=0.00).

## 5. Kanıt alanları ve gerekçe dili

| Ölçüm | v1 | v2 |
|---|---:|---:|
| `en_belirsiz_cumle` dolu | yok | 68/70 |
| Gerekçesinde övgü sıfatı geçen kayıt | 39/70 | 3/70 |

> Övgü taraması: isabet, derin, güzel, mükemmel, ustaca, harika, kusursuz, son derece, başarıyla, etkileyici — kaba bir vekil, üslup ölçer, doğruluk değil.

**Uzmanın reddettiği kayıtlarda judge'ın çıkardığı en belirsiz cümle:**

| Form | Judge'ın alıntısı | `anlasilirlik` |
|---|---|---:|
| 19 | O söz belki sıradan bir laftı, ama sen içinin kıpkırmızı olduğunu yazmışsın — duyacağın şey buymuş gibi hazırdın. | 4 |
| 26 | Sorunun ters olmaması onu daha zor kılmış gibi; tartışacak bir şey bırakmamış, seni sadece hatırlamaya bırakmış. | 4 |
| 27 | O söylenene dair elimdekini paylaşmamı ister misin? | 4 |
| 28 | Fiyatı savunmadın, "ben de biliyorum" dedin — yani o cümleyi duymadan önce de içinde bir yerde duruyordu. | 4 |
| 38 | Elimde gizlilikle ilgili kısa bir not var, ama sorduğunun tamamını kapsamıyor. | 5 |

## 6. Uzmanın alıntısı ↔ judge'ın alıntısı

Kanıt çıkarma adımı gerçekten çalışıyorsa, judge'ın *en belirsiz* dediği cümle uzmanın şikâyet ettiği cümleyle örtüşmeli. Uzman notlarının yalnızca bir kısmı cümleyi tırnak içinde veriyor; sınanabilen kayıtlar bunlar.

**Örtüşme: 3/4**

| Form | Karar | Uzmanın alıntısı | Judge'ın alıntısı | Aynı mı |
|---|---|---|---|:--:|
| 25 | sınırda | O saat sana ne veriyor | O saat sana ne veriyor? | ✅ |
| 26 | ret | sen ne zaman bir akşam içmesen | Sorunun ters olmaması onu daha zor kılmış gibi; tartışacak bir şey bır | ❌ |
| 27 | ret | O söylenene dair elimdekini paylaşmamı ister misin? | O söylenene dair elimdekini paylaşmamı ister misin? | ✅ |
| 33 | sınırda | ölçüyü dışarıya bırakmışsın ve o ölçü her gün başka bir şey söylüyor. | Kendin fark etmişsin: ölçüyü dışarıya bırakmışsın ve o ölçü her gün ba | ✅ |

## 7. Sonuç — v2 neyi düzeltti, neyi düzeltmedi

### Düzelen

1. **Tavan kırıldı.** v1 dil boyutunda 70/70 tam puan (s=0.00) → v2 `anlasilirlik`'te 18/68. `dogallik`'te tam puan oranı %6. Boyutlar artık ayrım yapabilecek varyansa sahip.
2. **Övgü dili bitti.** Gerekçesinde övgü sıfatı geçen kayıt 39/70 → 3/70.
3. **`cevapsiz_soru` çalıştı.** v1'in tamamen kaçırdığı kusuru, uzmanın bu yüzden reddettiği kayıtta (form 38) yakaladı ve kullanıcının sorusunu doğru alıntıladı.

### Düzelmeyen — asıl sonuç

**Ayrım gücü yok.** Uyum oranları 0.41–0.57 aralığında, hepsi tesadüf bandında. v2, uzmanın `ret` dediği kayıtları `kabul`lerden ayıramıyor — v1 de ayıramıyordu. `mi_uyumu`'nda uyum oranı 0.50'nin **altında**: judge, uzmanın reddettiği kayıtlara sistematik olarak daha yüksek MI puanı veriyor.

⚠️ **Bu test zayıftır ve bunu gizlememek gerekir.** `ret` grubu 5 kayıt; %95 aralıklar yukarıdaki tabloda ve hepsi çok geniş. Test yalnızca **güçlü bir ayrımın olmadığını** söyleyebilir; orta düzey bir ayrımı ne doğrular ne yalanlar.

### Teşhis — sorun algıda değil, puanlamada

En açıklayıcı bulgu §6'da: judge, uzmanın şikâyet ettiği cümleyi **bulabiliyor** — sınanabilen 4 kaydın **3'ünde** uzmanla aynı cümleyi, üstelik bağımsız olarak seçti. Ama o cümleyi alıntıladıktan sonra verdiği puanlar: form 25 `anlasilirlik`=4 · form 27 `anlasilirlik`=4 · form 33 `anlasilirlik`=4. Uzman aynı cümlelere dil boyutunda form 25=2 · form 27=1 · form 33=2 verdi. **Judge kusuru görüyor, kusur saymıyor.**

Bunun anlamı: v2'nin yaptığı şey — kusur türlerini daha iyi tarif etmek — **yetersiz bir müdahaleydi**. Kanıt çıkarma adımı işini yaptı; puan, çıkarılan kanıttan bağımsız kaldı. Sonraki denemenin bu boşluğa girmesi gerekir: puanı kanıtın **fonksiyonu** yapmak (ör. *en_belirsiz_cumle* belirsiz gönderge ya da kurulmamış mecaz içeriyorsa `anlasilirlik` ≤ 3 kuralı), ya da mutlak ölçek yerine **ikili karşılaştırma** kullanmak. Bu, v3 rubriği demektir; bu raporda ölçülmemiştir.

### Karar

**Judge çıktısı hâlâ kalite kanıtı değildir** (`prompts/uretim-v3.md` §9 aynen geçerli). v2, v1'den *daha çok şey ölçüyor* ama **kaliteyi ölçmüyor**. Üretimde tarama amaçlı kullanılmaya devam eder; `cevapsiz_soru` bayrağı ise elle incelemeye yönlendirmek için doğrudan işe yarar.
