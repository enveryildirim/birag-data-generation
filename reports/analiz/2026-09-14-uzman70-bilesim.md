# Uzman örneklemi — 70 kayıt, gerçekleşen bileşim

**Kayıt dosyası:** `data/candidates/expert-70.jsonl` · SHA256 `ee61043de8d38187cc41b7a6c5391b735bfcc8daf9e12af504317ef0041aa775`  
**Plan:** `data/expert_sample/plan-70.jsonl` · SHA256 `982ce10de56a8c588b89a08bafd98b2068d7c704adc105309bc41b6fb030dfdc`  
**Betik:** `scripts/analiz/2026-09-14-uzman70-bilesim.py`  
**Üretim:** `scripts/analiz/2026-09-14-uretim-uzman70.py` · talimat `prompts/uretim-v2.md`  
**Tarih:** 2026-09-14 · **Karar:** K27 seçenek B

> ⚠️ **2026-09-14 düzeltmesi.** Aşağıdaki "`checks.py` geçen 70/70" satırı, o günkü kapı
> setine göre doğruydu. Aynı gün `thinking:completion` **oran tavanı** (4x) kapıya eklendi
> — talimatta (v2 §4) tavan yazıyordu ama kapı yoktu. Yeni kapıyla korpus **68/70** geçiyor;
> #47 (4.16x) ve #50 (4.01x) tavanı aşıyor. Kayıtlar uzman puanlamasından sonra
> **değiştirilmedi**; düzeltme kapıda, veride değil.
> Güncel ölçüm: `reports/analiz/2026-09-14-korpus-hedef-expert70.md`

## Otomatik ölçümler

| Ölçüt | Değer |
|---|---|
| Kayıt | 70 |
| `checks.py` geçen | 70/70 |
| Yanıt başına soru | en çok 1 (kapı: ≤1) · sorusuz kayıt 2 |
| Cevap uzunluğu | ortanca 169 karakter · 98-282 |
| thinking : cevap | ortalama 2.63x · ortanca 2.51x · en yüksek 4.16x (tavan 4x) |

> thinking uzunluğu cevaba orantılı tutuldu; sabit oran hedeflenmedi (§4, K10).

## Bileşim

### Senaryo (gerçekleşen)

| Değer | Adet |
|---|---:|
| ambivalans | 10 |
| inkar | 8 |
| farkindalik | 7 |
| nazikce_karsi_cikma | 5 |
| durtu | 4 |
| hedef_belirleme | 4 |
| borc_finansal | 4 |
| motivasyon | 4 |
| rol_siniri | 4 |
| bilmiyorum_cikmazi | 3 |
| anlasilmama | 3 |
| hukuki_kaygi | 3 |
| bilgilendirme | 3 |
| kayma_nuks | 2 |
| kayip_kovalama | 2 |
| discord | 2 |
| kutlama | 2 |

### Bağımlılık türü

| Değer | Adet |
|---|---:|
| alkol | 18 |
| tutun | 18 |
| kumar | 16 |
| receteli_ilac | 12 |
| dijital | 6 |

### Yaş grubu

| Değer | Adet |
|---|---:|
| yetiskin | 64 |
| ergen | 6 |

### Dilim

| Değer | Adet |
|---|---:|
| terapotik_tek_tur | 47 |
| terapotik_cok_tur | 13 |
| rag_tek_tur | 9 |
| rag_cok_tur | 1 |

### Tur yapısı

| Değer | Adet |
|---|---:|
| single | 56 |
| multi | 14 |

### MI süreci

| Değer | Adet |
|---|---:|
| engaging | 57 |
| evoking | 9 |
| focusing | 2 |
| planning | 2 |

### Konuşma tipi

| Değer | Adet |
|---|---:|
| ambivalans | 33 |
| sustain | 25 |
| change_cat | 4 |
| change_darn | 4 |
| discord | 4 |

### System prompt

| Değer | Adet |
|---|---:|
| canon | 63 |
| paraphrase | 7 |

**Red / sınır kaydı (`is_negative`):** 15/70 (%21) — hedef ~%15, K16
**Context modu (`context`):** 9/70
**Kriz kaydı:** 0/70 — bilinçli sıfır, uzman onayı bekliyor (Kural 3)

## Plandan sapan senaryo atamaları

Sapma, tohum metninin hedef arketipi desteklememesinden kaynaklanır; arketip tohuma uydurulmak yerine tohuma uyan arketip yazılmıştır (K37 — senaryo ataması üretim zamanı kararıdır).

| # | Planlanan | Yazılan |
|---|---|---|
| 16 | inkar | hedef_belirleme |
| 19 | durtu | ambivalans |
| 25 | bilmiyorum_cikmazi | inkar |
| 27 | anlasilmama | bilmiyorum_cikmazi |
| 31 | kayma_nuks | borc_finansal |
| 32 | bilmiyorum_cikmazi | farkindalik |
| 35 | hedef_belirleme | ambivalans |
| 38 | kayma_nuks | ambivalans |
| 41 | kayma_nuks | farkindalik |
| 47 | discord | farkindalik |
| 53 | rol_siniri | discord |
| 56 | rol_siniri | inkar |
| 59 | discord | inkar |

Toplam sapma: **13/70**.

