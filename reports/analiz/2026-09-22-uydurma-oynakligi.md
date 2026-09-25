# Partiler arası uydurma oynaklığının sebebi

**Betik:** `scripts/analiz/2026-09-22-uydurma-oynakligi.py` · **Tarih:** 2026-09-22  
**Küme:** `v6-parti3`–`parti8`, 412 kayıt, aynı judge + rubrik v9  
**Ölçü:** `grounding == 2` (51 kayıt, %12.4) · permütasyon 20000, tohum 20260922  

⛔⛔ **Hipotez sayılardan önce yazıldı** (betiğin başında). Birincil hipotezin kaynağı toplu bir sayı değil, **elle okunan vakalar**: işaretlenen uydurmaların biçimi tekrar tekrar sayıp dökmekti.

## (0) Açıklanacak şey

Parti heterojenliği: **G = 20.5**, sd = 5, p = **0.0000** ⇒ partiler tek bir tabandan gelmiyor. Aşağıdaki sorunun tamamı bu G'yi düşürmekle ilgili.

## ⭐⭐ (1) ÖN KAYITLI HİPOTEZ — özetleme

| cevap | uydurma | oran | %95 Wilson |
|---|---:|---:|---|
| `ozet_var` = **True** | 24/197 | %12.2 | %8.3–%17.5 |
| `ozet_var` = False | 27/215 | %12.6 | %8.8–%17.7 |

**Fark: -0.4 puan · permütasyon p = 1.0000**

⛔ **Doğrulanmadı.** Ön kayıtlı hipotez tutmadı ve bu **bir bulgudur** — okuduğum vakaların biçimi beni yanılttı.

## ⭐⭐⭐ (2) Asıl soru — parti oynaklığını AÇIKLIYOR mu

Her partinin beklenen uydurma sayısı kendi **özet payından** türetildi; artık heterojenlik G ile sınandı.

| | G | sd | p |
|---|---:|---:|---:|
| ham parti heterojenliği | 20.5 | 5 | 0.0000 |
| özete göre düzeltilmiş **artık** | **20.4** | 4 | **0.0004** |

⇒ Özetleme heterojenliğin **%0**'ini açıklıyor.

| parti | özet payı | uydurma |
|---|---:|---:|
| `v6-parti3` | %50 | %15.0 |
| `v6-parti4` | %49 | %16.9 |
| `v6-parti5` | %52 | %3.3 |
| `v6-parti6` | %48 | %1.7 |
| `v6-parti7` | %60 | %12.3 |
| `v6-parti8` | %38 | %18.6 |

## (3) ⛔ KEŞİFSEL — çoklu karşılaştırma, tek başına bulgu değil

22 karşılaştırma tarandı. ⛔⛔ Buradaki en küçük p **seçilerek** elde edilmiştir; Bonferroni eşiği 0,05/22 = **0.0023**.

| değişken | değer | fark (puan) | p |
|---|---|---:|---:|
| `bicim` | `uzun` | -12.7 | 0.0011 ⭐ |
| `turn_ending` | `yalnizca_yansitma` | +13.9 | 0.0044 |
| `uzunluk_dilimi` | `uzun` | -9.7 | 0.0064 |
| `bicim` | `orta` | +7.7 | 0.0276 |
| `uzunluk_dilimi` | `orta` | +7.3 | 0.0411 |
| `turn_ending` | `acik_uclu_soru` | -5.3 | 0.1389 |
| `register` | `bozuk` | -4.7 | 0.2280 |
| `register` | `duzgun` | +4.7 | 0.2325 |
| `turn_ending` | `takdir` | -5.1 | 0.3020 |
| `bicim` | `kisa` | +2.7 | 0.4459 |
| `takdir` | `True` | -3.1 | 0.4923 |
| `uzunluk_dilimi` | `kısa` | +2.5 | 0.5297 |

## ⭐⭐⭐ (4) Hangi etken parti oynaklığını AÇIKLIYOR

Ham heterojenlik **G = 20.5**. Her etken için: o etkene göre beklenen uydurma sayısı hesaplandı ve **artık** G ölçüldü. ⛔ Etkenler (3)'ün sonucuna bakılarak seçilmedi — kategorik olan **hepsi** sınandı.

| etken | artık G | açıkladığı | artık p |
|---|---:|---:|---:|
| `uzunluk_dilimi` | 17.7 | %14 | 0.0000 |
| `karmasik` | 19.7 | %4 | 0.0006 |
| `yansitma` | 20.3 | %1 | 0.0004 |
| `konusma_durumu` | 20.4 | %0 | 0.0000 |
| `ozet` | 20.4 | %0 | 0.0004 |
| `turn_ending` | 20.4 | %0 | 0.0000 |
| `register` | 20.5 | %-0 | 0.0004 |
| `takdir` | 20.5 | %-0 | 0.0004 |
| `bicim` | 20.7 | %-1 | 0.0000 |
| `risk` | 21.4 | %-4 | 0.0000 |

⭐ En çok açıklayan: **`uzunluk_dilimi`** — heterojenliğin **%14**'ini alıyor, ama artık p = **0.0000**.

⛔⛔⛔ **HİÇBİR ETKEN OYNAKLIĞI AÇIKLAMIYOR.** En iyisi bile artık heterojenliği anlamlı bırakıyor ⇒ partiler arası fark, ölçebildiğim tasarım değişkenlerinin **hiçbirinden** gelmiyor. ➡️ *Geriye ölçmediğim şey kalıyor: partiyi yazan oturumun kendisi — hangi blok betiği, hangi gün, hangi dikkat.*

## ⭐⭐⭐ (5) «Yazan oturum» hipotezi — blok düzeyi

(4) bütün tasarım değişkenlerini eledi; geriye *«partiyi yazan oturumun kendisi»* kaldı. ⭐ Bunun **sınanabilir** bir sonucu var: her blok ayrı bir yazma turudur (33 blok, 412 kayıt eşleşti) ⇒ hipotez doğruysa uydurma, parti **içinde de** bloklara öbeklenmiş olmalı. Değilse hipotez düşer.

| | |
|---|---|
| parti içi, bloklar arası heterojenlik | **G = 30.9** |
| permütasyon (etiketler parti İÇİNDE karıştırıldı, 5000 tur) | p = **0.3523** |

⛔⛔⛔ **ÖBEKLENME YOK.** Uydurma parti içinde bloklara rastgele dağılıyor ⇒ *«yazan oturum»* hipotezi de **DÜŞTÜ**. ➡️ *Oynaklık parti düzeyinde gerçek, ama ne tasarım değişkenleri ne de yazma turu onu tutuyor. Ölçebildiğim hiçbir şey açıklamıyor — ve bunu söylemek, açıklayan bir şey uydurmaktan daha doğru.*

## ⭐⭐ (6) Parti düzeyinde ne farklı

(4) kayıt düzeyini, (5) blok düzeyini eledi. Geriye **parti düzeyi** kaldı — parti içinde sabit, partiler arasında değişen bir şey. Kayıtlardaki parti düzeyi değişkenlerin hepsi okundu:

| parti | uydurma | `prompt_version` | `generator_model` | `tohum_havuzu` | `date` |
|---|---:|---|---|---|---|
| `v6-parti3` | %15.0 | `uretim-v5` | `claude-opus-5` | `seeds` | 2026-09-20 |
| `v6-parti4` | %16.9 | `uretim-v5` | `claude-opus-5` | `seeds` | 2026-09-20 |
| `v6-parti5` | %3.3 | `uretim-v5` | `claude-opus-5` | `seeds` | 2026-09-20 |
| `v6-parti6` | %1.7 | `uretim-v5` | `claude-opus-5` | `seeds` | 2026-09-21 |
| `v6-parti7` | %12.3 | `uretim-v5` | `claude-opus-5` | `seeds` | 2026-09-21 |
| `v6-parti8` | %18.6 | `uretim-v5` | `claude-opus-5` | `seeds` | 2026-09-21 |

⛔⛔ **Üçü de sabit** (`uretim-v5`, `claude-opus-5`, `seeds`) ⇒ hiçbiri oynaklığı açıklayamaz. **Tarih de açıklamıyor:** aynı günde üretilen partiler birbirinden çok uzak — 09-20'de %15,0 / %16,9 / %3,3, 09-21'de %1,7 / %12,3 / %18,6.

⚠️ **Yan bulgu (T236 ailesi):** `v6-parti8`'in kayıtları `date: 2026-09-21` taşıyor ama parti **09-22'de** üretildi (betik adı ve commit tarihi). Tarih blok şablonunda **sabit yazılı** ve parti7'den taşınmış. ⭐ Aynı şablonda `parti` alanı aynı kusurdan dolayı düzeltilip **türetilir** yapılmıştı; `date` yanı başındaydı ve düzeltilmedi. ➡️ *Bir şablondaki bir beyanı türetmeye çevirmek, komşusunu düzeltmez.* ⛔ 118 kaydın tarihi yanlış; K126 zaten *«rapor tarihi betik ADINDAN»* diyor, aynı kural buraya da uygulanabilir — **bu raporda düzeltilmedi**.

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔⛔ **Ölçü bir ALT SINIR** | `grounding` tek-ayrıntı sondasıdır (T238); özet içeren cevaplar **daha çok ayrıntı** taşır ⇒ sondanın onlarda daha sık isabet etmesi mümkündür. ⚠️ Yani bulgu *«özet uydurmayı artırır»* kadar *«sonda özette daha iyi görür»* de olabilir — **ikisi bu veriyle ayrılamaz** |
| ⛔ **`ozet_var` judge'ın kararıdır** | kodun değil; judge'ın kendi gürültüsü bu alanda ölçülmedi |
| ⛔ **Nedensellik kurulmadı** | özet ile uydurma birlikte değişiyor; hangisinin hangisini getirdiği bir **müdahale** ister (özet oranı düşürülmüş bir parti) |
| ⚠️ **Keşifsel bölüm sıralamaya göre kesildi** | ilk 12 satır gösteriliyor, tamamı betikte |
