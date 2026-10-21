# BıRAG veri kümesi — v0.2.0

**Tarih:** 2026-10-21 · **Kaynak:** ölçek-5k (K279), `data/candidates/olcek5k.jsonl` `866a1e13c9b0fd60`
**Çıktı:** `train.jsonl` SHA256-16 **`eabc85f7b97c96c1`** · **4334 kayıt**
**Durum:** ⭐ araştırma sürümü · ⛔ `v0.1.1` ile **birleşik DEĞİL** (yalnız ölçek-5k kayıtları; birlikte eğitilecekse iki dosya ayrıca birleştirilir) · ⛔ kriz dilimi hariç (tasarım gereği)

## 1. Nasıl üretildi

Üç aşama, kayıt başına: **A** (Haiku) tohumdan kullanıcı tarafı · **B** (Haiku) son cevap + thinking, **tohumu görmeden** · **C** hata avı — düzelt / düşür (K43: puan değil). Mekanik kapılar her aşamada (`scripts/analiz/2026-10-20-olcek5k-arac.py`). Briefler `prompts/olcek5k-{A,B,C}.v1.md`.

| C modeli | kayıt |
|---|---:|
| claude-haiku-5-5 | 4057 |
| claude-sonnet-5-5 | 277 |

C kararları: aynen 3017 · duzeltildi 1317. Düzeltme+düşürme oranı Sonnet'te %62,5, Haiku'da %28,3 — **Haiku kusurların bir kısmını kaçırıyor** (`reports/analiz/2026-10-20-olcek5k-sonuc.md`).

## 2. Dışlananlar (4980 aday → 4334)

| sebep | kayıt |
|---|---:|
| tohum sızıntısı şüphesi (`gen_meta.sizinti_supheli`) | 131 |
| eval tohumu (`evals/*` `kaynak.seed_id`) | 309 |
| eval metni çakışması (60 karakter önek) | 0 |
| kalıcı eleme defteri | 13 |
| BLEU/ROUGE referans seti (`olcek5k-ref.v1`) | 193 |

⛔ Eval dışlamaları ölçek-5k planında uygulanmamıştı (önceki partilerin hepsinde vardı); donmadan önce bu betikle kapatıldı.

## 3. Dağılım

| alan | dağılım |
|---|---|
| tür | alkol 1167 · kumar 1006 · tutun 968 · receteli_ilac 837 · dijital 356 |
| yaş | yetiskin 3829 · ergen 505 |
| dilim | terapotik_tek_tur 1737 · terapotik_cok_tur 1484 · rag_tek_tur 853 · rag_cok_tur 260 |
| tur | single 2590 · multi 1744 |
| sınır tipi | yok 2900 · rol_siniri_yonlendirme 881 · yonlendirme_istegi 299 · yonlendirme_gereksiz 137 · sinir_cekme 117 |
| bitiş | acik_uclu_soru 2575 · yalnizca_yansitma 561 · ozet 526 · takdir 494 · durur 178 |

## 4. ⛔ Bilinen kusurlar ve açık maddeler

| | |
|---|---|
| ⛔⛔ **Kayıt kayıt okunmadı** | K260 bu üretim için askıda (K279). Örneklem okuması 20 kayıt: Haiku-C 14'te 2 ciddi + 2 küçük, Sonnet-C 6'da 0 ciddi + 1 küçük (`reports/analiz/2026-10-21-olcek5k-okuma.md`) |
| ⛔ **Açılış sızıntısı** | çok turlu kayıtların ~%1-2'sinde asistan açılışı ikinci kullanıcı mesajındaki bir ayrıntıyı anıyor (kaba tarama, kapı değil) |
| ⛔ **Tohumlar yeniden kullanıldı** | 5000 satırın tamamı `v0.1.1` / eski partilerde kullanılmış tohumlardan (2153 tohum × 2-3); kullanıcı metni yeni, senaryo tohumu ortak |
| ⚠️ **BLEU referans seti kardeşleri** | referans setinin tohumlarından üretilmiş 258 kayıt eğitimde kaldı (aynı kayıt / aynı ilk mesaj çıkarıldı). Referans set zaten tohumu `v0.1.1` ile paylaşıyor (`2026-10-20-rapor-referans-seti.py` sınırları) |
| ⚠️ **`sinir_tipi` normalleştirildi** | B'nin güvenlik sapmasında yazdığı serbest etiketler korpus sözlüğüne bağlandı; özgün etiket `gen_meta.sinir_tipi_b` |
| ⛔ **Jeton uzunluğu doğrulanmadı** | bu makinede tokenizer yok; eğitim ortamında ≤ 2048 denetlenmeli |
| ⚠️ **Yazarlık** | *Haiku taslakladı (A, B), Sonnet (parça 1-13) / Haiku (14-200) hata avı yaptı, Claude Code tasarladı ve örnekledi* |
| ⛔ **Kriz dilimi yok** | tasarım gereği; T311'in gerilemesini (kriz/yönlendirme) bu sürüm onaramaz |
