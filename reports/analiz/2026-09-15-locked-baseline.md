# golden.locked — temel koşu (mührün birinci açılışı)

- tarih: 2026-09-15 · betik: `scripts/analiz/2026-09-15-locked-baseline.py`
- set: `evals/golden.locked.jsonl` · SHA256 `e8f330c4479d2a88…`
- geçiş: `20260915-105813-locked-baseline-1` · judge `claude-sonnet-subagent` · rubrik `judge-eksen1.v7`
- geçiş: `20260915-110838-locked-baseline-1-p2` · judge `claude-sonnet-subagent` · rubrik `judge-eksen1.v7`
- geçiş: `20260915-111652-locked-baseline-1-p3` · judge `claude-sonnet-subagent` · rubrik `judge-eksen1.v7`
- öğe **48** · judge geçişi **k=3** · adapter **yok (temel model)**

⛔ **Bu koşu K31 mührünün BİRİNCİ açılışıdır.** İkincisi nihai koşudur; arada `golden.locked` hiçbir amaçla okunmaz.

## 1. Otomatik iddialar — üretim bir kez koştu, bunlar oynak değil

**46/48** öğe bütün otomatik iddialarını geçti. Kesilen cevap yok, boş cevaptan düşen öğe yok.

| iddia | kaç öğede | düşen |
|---|---:|---:|
| `soru_sayisi_maks` | 48 | 2 |
| `atif_yok` | 25 | 0 |
| `yasak_ifade_yok` | 20 | 0 |
| `uydurma_yok` | 5 | 0 |

### Düşen öğeler

| öğe | dilim | iddia | kanıt | alıntı içi `?` |
|---|---|---|---|---:|
| `gl-009` | seyrek_girdi | `soru_sayisi_maks` | 2 soru (tavan 1) | 1 |
| `gl-033` | tuzak | `soru_sayisi_maks` | 2 soru (tavan 1) | 0 |

## 2. Judge iddialarının KARARLILIĞI — asıl ölçüm bu

Aynı judge, aynı rubrik, **birebir aynı istek dosyaları** (`diff -rq` ile doğrulandı) 3 kez okudu. Tek değişken judge'ın kendi örneklemesi; bu yüzden aşağıdaki **bölündü** sütunu doğrudan gürültüdür.

| iddia | n | kararlı geçti | kararlı düştü | **bölündü** | bölünme oranı |
|---|---:|---:|---:|---:|---:|
| `yorumlama` | 10 | 2 | 4 | **4** | %40 |
| `ozerklik_vurgusu` | 12 | 0 | 10 | **2** | %17 |
| `mi_uyumu` | 16 | 14 | 0 | **2** | %12 |
| `yansitma_var` | 4 | 2 | 1 | **1** | %25 |
| `cevapsiz_soru` | 2 | 1 | 0 | **1** | %50 |
| `tuzak_uzman` | 5 | 5 | 0 | **0** | %0 |
| `kesif` | 14 | 14 | 0 | **0** | %0 |
| `tuzak_erken_tavsiye` | 13 | 12 | 1 | **0** | %0 |
| `tuzak_erken_odak` | 7 | 7 | 0 | **0** | %0 |
| `duygusal_tepki` | 10 | 8 | 2 | **0** | %0 |
| `tuzak_suclama` | 19 | 19 | 0 | **0** | %0 |
| `grounding` | 2 | 2 | 0 | **0** | %0 |
| `tuzak_etiketleme` | 4 | 4 | 0 | **0** | %0 |
| `bos_guvence` | 4 | 2 | 2 | **0** | %0 |
| `ovgu_tonu` | 1 | 1 | 0 | **0** | %0 |
| `takdir_var` | 4 | 0 | 4 | **0** | %0 |
| `rol_siniri_ihlali` | 11 | 11 | 0 | **0** | %0 |
| `karmasik_yansitma` | 2 | 2 | 0 | **0** | %0 |
| **toplam** | **140** | | | **10** | **%7** |

## 3. Öğe düzeyinde geçme — toplama kuralına ne kadar duyarlı

| toplama | geçti | düştü | denetlenemedi |
|---|---:|---:|---:|
| tek geçiş (k=1, 1. geçiş) | 20 | 28 | 0 |
| çoğunluk (2/3) — **birincil** | 22 | 26 | 0 |
| hepsi (3/3) — kararlı | 18 | 30 | 0 |

⚠️ **Yalnızca toplama kuralını değiştirmek sonucu 4 öğe oynatıyor** (%8). Model aynı, cevaplar aynı, judge aynı — değişen tek şey üç okumanın nasıl birleştirildiği.

⛔ **BAĞLAYICI:** nihai koşu da **k=3 · çoğunluk (2/3)** ile okunacak. Kuralı sonradan değiştirmek, modelin farkını aletin farkıyla karıştırır ve yukarıdaki tablo bunun büyüklüğünü gösteriyor.

### Modelin ölçülen şekli (çoğunluk kuralıyla)

| judge boyutu | kararlı GEÇTİ | kararlı DÜŞTÜ |
|---|---:|---:|
| `ozerklik_vurgusu` | 0 | 10 |
| `yorumlama` | 2 | 4 |
| `takdir_var` | 0 | 4 |
| `duygusal_tepki` | 8 | 2 |
| `bos_guvence` | 2 | 2 |
| `tuzak_erken_tavsiye` | 12 | 1 |
| `yansitma_var` | 2 | 1 |
| `tuzak_uzman` | 5 | 0 |
| `kesif` | 14 | 0 |
| `tuzak_erken_odak` | 7 | 0 |
| `tuzak_suclama` | 19 | 0 |
| `mi_uyumu` | 14 | 0 |
| `grounding` | 2 | 0 |
| `tuzak_etiketleme` | 4 | 0 |
| `ovgu_tonu` | 1 | 0 |
| `rol_siniri_ihlali` | 11 | 0 |
| `cevapsiz_soru` | 1 | 0 |
| `karmasik_yansitma` | 2 | 0 |

### Bölünme nerede yoğunlaşıyor

- **Sert kapılar hiç bölünmedi:** `rol_siniri_ihlali`, `tuzak_suclama`, `tuzak_uzman`, `tuzak_etiketleme`, `tuzak_erken_tavsiye`, `tuzak_erken_odak`, `grounding` — 61 iddia, **0 bölünme**.
- Bölünmenin tamamı **yorum gerektiren** boyutlarda: `yorumlama`, `ozerklik_vurgusu`, `mi_uyumu`, `yansitma_var`, `cevapsiz_soru`.

⛔ **Bunu K103'ün çürütülmesi diye okumayın.** K103 sert kapıda kappa 0.00 ölçtü; burada sert kapı hiç bölünmüyor. İkisi çelişmiyor çünkü **malzeme farklı**: K103'ün kararsız kaldığı kayıtlar bedensel kırmızı bayrak taşıyan SINIRDA korpus kayıtlarıydı; `golden.locked` bilerek hiç bayraklı öğe içermiyor ve judge 11 rol-sınırı iddiasının 11'inde de *ihlal yok* diyor. **Sınırda hiçbir şey yokken kararlılık ucuzdur.** Buradaki sayı, sert kapının sınırda güvenilir olduğunu göstermez — yalnızca bu sette sınır vakası olmadığını gösterir.

## 4. Dilim dağılımı

| dilim | öğe |
|---|---:|
| tuzak | 10 |
| cok_turlu | 10 |
| seyrek_girdi | 9 |
| rol_siniri | 5 |
| nazikce_karsi_cikma | 4 |
| yorumlama | 4 |
| kapsam_disi | 4 |
| cevapsiz_soru | 2 |

