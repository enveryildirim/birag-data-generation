# BıRAG veri kümesi — v0.2.1

**Tarih:** 2026-10-21 · **Taban:** `datasets/v0.2.0/train.jsonl` `eabc85f7b97c96c1` (4334 kayıt, bayt bayt aynen, sıra korunur)
**Çıktı:** `train.jsonl` SHA256-16 **`e73bf1eccbc335cb`** · **5013 kayıt** (= 4334 + 679 tamamlama)
**Durum:** ⭐ araştırma sürümü · ⛔ `v0.1.1` ile **birleşik DEĞİL** · ⛔ kriz dilimi hariç (tasarım gereği)

## 1. Tamamlama partisi

`v0.2.0`'ı 5000'e yaklaştırmak için 700 satırlık ızgara (`data/plan/olcek5k-ek.jsonl` `c7ce336c387ee978`, parça 201-228). Üretim `v0.2.0` ile aynı: A (Haiku) → B (Haiku, tohumsuz) → C (Haiku, hata avı). Fark: eval tohumu, eval metni, kalıcı eleme defteri ve BLEU referans seti tohumları **planda** dışlandı (K281 dersi).

| | kayıt |
|---|---:|
| planlanan | 700 |
| C düşürdü / birleştirmeye girmedi | 0 |
| dışlandı (sızıntı şüphesi vb.) | 21 — sizinti_supheli 21 |
| **eklendi** | **679** |

Tamamlama C kararları: aynen 492 · duzeltildi 187.

## 2. Dağılım (bütün sürüm)

| alan | dağılım |
|---|---|
| C modeli | claude-haiku-5-5 4736 · claude-sonnet-5-5 277 |
| tür | alkol 1339 · kumar 1168 · tutun 1108 · receteli_ilac 972 · dijital 426 |
| yaş | yetiskin 4413 · ergen 600 |
| dilim | terapotik_tek_tur 2021 · terapotik_cok_tur 1704 · rag_tek_tur 992 · rag_cok_tur 296 |
| tur | single 3013 · multi 2000 |
| sınır tipi | yok 3346 · rol_siniri_yonlendirme 1035 · yonlendirme_istegi 341 · yonlendirme_gereksiz 161 · sinir_cekme 130 |
| bitiş | acik_uclu_soru 2964 · yalnizca_yansitma 658 · ozet 608 · takdir 581 · durur 202 |

## 3. ⛔ Bilinen kusurlar

`datasets/v0.2.0/CARD.md` §4'tekilerin hepsi geçerli (kayıt kayıt okunmadı, Haiku-C kaçırma payı, açılış sızıntısı ~%1-2, tohumlar yeniden kullanıldı, jeton uzunluğu doğrulanmadı, kriz dilimi yok). Ek: tamamlama partisinin tohumları ölçek-5k'da zaten 2 kez kullanılmıştı ⇒ bu 700 tohum artık **3×**.
