# İP1 başarı ölçütleri — gelişme raporu (0–12. ay)

- Betik: `scripts/analiz/2026-10-20-ip1-olcutler.py` · tarih 2026-10-20
- Ölçüt kaynağı: başvuru formu İP1 (s.3 Tablo 1 · s.16 iş-zaman çizelgesi); eşleme `docs/rapor/oneri-rapor-esleme.md`
- Girdiler (SHA256-16):

  - `datasets/v0.1.0/train.jsonl` `6fcb6b1e16290575`
  - `datasets/v0.1.1/train.jsonl` `f8fcaa1e96603cb2`
  - `datasets/v0.1.0/manifest.json` `51ec50cf450e1f1b`
  - `configs/taxonomy.yaml` `70f9697deeb68cdc`
  - `configs/chat_template_train.jinja` `0718cacd112f8e18`
  - `data/candidates/olcek5k/kayit/*.jsonl` — 144 parça, **anlık** (koşu sürüyor; SHA yok, sayı bitince değişir)

## 1. Hacim — hedef 10.000 talimat örneği

| küme | kayıt | durum |
|---|---:|---|
| `datasets/v0.1.0` | 1058 | dondurulmuş |
| `datasets/v0.1.1` | 1058 | dondurulmuş |
| ölçek-5k ara kayıtları | 3598 | üretimde · aşama dağılımı {'B': 144} · plan 5000 |

Dondurulmuş benzersiz kayıt: **1058** (%10.6 / 10.000). `v0.1.1`, `v0.1.0`'ın aynı kayıtlarıdır (düşünce yeniden kuruldu) — toplanmaz. Ölçek-5k tamamlanıp donarsa toplam ≈ 6058 olur.

## 2. Hedef senaryolarla uyum ve doğru biçim — hedef %90

**(a) Üretilen adayların kapılardan geçme oranı** (`v0.1.0` manifest): 1058 / 1132 = **%93.5**. Elenme sebepleri: {'judge_uydurma': 56, 'judge_safety_violation': 14, 'guvenlik_karantinasi': 4}

**(b) Senaryo alanı kanonik listede** (`v0.1.1`, replay hariç 1040 kayıt): 944 = **%90.8**. Liste dışı: {'belirsiz': 94, 'tetikleyici': 2}. `belirsiz` = tohum açılış mesajı, arketip üretim zamanında seçilmedi (K37); ayrı bir senaryo değil.

**(c) Son sürümde bütün deterministik kapılar** (`run_checks`): 1058 / 1058 = **%100.0**

Senaryo dağılımı (replay hariç):

| senaryo | kayıt |
|---|---:|
| ambivalans | 282 |
| rol_siniri | 191 |
| nazikce_karsi_cikma | 159 |
| belirsiz *(liste dışı)* | 94 |
| farkindalik | 88 |
| inkar | 47 |
| hedef_belirleme | 34 |
| kayma_nuks | 22 |
| anlasilmama | 22 |
| hukuki_kaygi | 18 |
| borc_finansal | 15 |
| durtu | 11 |
| kutlama | 11 |
| bilgilendirme | 11 |
| kayip_kovalama | 11 |
| discord | 10 |
| motivasyon | 8 |
| bilmiyorum_cikmazi | 2 |
| kriz | 2 |
| tetikleyici *(liste dışı)* | 2 |

## 3. Dil modeliyle uyum — hedef %95

Uyumlu = şema (`TrainRecord`) + konuşma yapısı + eğitim chat template'i (`configs/chat_template_train.jinja`, K44) kaydı hatasız işliyor ve son cevabı/düşünceyi koruyor + düşünce beyanı olan kayıtta düşünce dolu.

| sürüm | uyumlu | oran | uyumsuzluk sebepleri |
|---|---:|---:|---|
| `v0.1.0` | 1058 / 1058 | **%100.0** | — |
| `v0.1.1` | 1058 / 1058 | **%100.0** | — |

⚠️ Jeton uzunluğu (≤ 2048) bu makinede ölçülmedi; Colab eğitimi aşan kaydı durdurur (`src/colab_egitim.py`).

## 4. Etik ve anonim — hedef %100

Kişisel veri desen taraması — bütün mesajlar ve düşünceler:

| desen | `v0.1.0` | `v0.1.1` |
|---|---:|---:|
| e-posta | 0 | 0 |
| URL | 0 | 0 |
| cep telefonu | 0 | 0 |
| sabit telefon | 0 | 0 |
| TC kimlik (11 hane) | 0 | 0 |
| IBAN | 0 | 0 |
| kart numarası | 0 | 0 |
| adres | 0 | 0 |
| doğum tarihi biçimi | 0 | 0 |

Desenler her koşuda öz-sınamadan geçer (bilinen bir örneği yakalar, masum bir cümleyi yakalamaz) — sıfır, desenin kör olduğu anlamına gelmez.

Desen taşımayan kayıt: `v0.1.0` 1058 / 1058 = **%100.0** · `v0.1.1` 1058 / 1058 = **%100.0**

- §15 **sert** yasak ifade (`kriz_yasagi`) asistan turlarında, `v0.1.1`: **0**
- Kriz kaydı (`is_crisis`): **0** — kriz dilimi uzman ve etik onayına kadar bilerek üretilmedi (Kural 3).
- Veri tamamen sentetik: gerçek kişi, hasta kaydı ya da forum metni yok (form Tablo 3'teki bu iki kaynak etik onay beklediği için kullanılmadı). Uzman korpusu eğitim satırı olarak kullanılmadı (K20).
- ⚠️ Kişi adı taraması yapılmadı (bkz. betik başlığı).

## 5. %70 Türkçe olumlu değerlendirme

Bu betikte yeniden hesaplanmadı. Kaynak: `reports/analiz/2026-09-14-uzman-puanlama-analizi.md` (uzman puanlaması, 50/70 kayıt, K58).
