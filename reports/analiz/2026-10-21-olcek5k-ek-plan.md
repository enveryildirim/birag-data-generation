# Ölçek-5k tamamlama ızgarası (700 satır, parça 201-228)

- Betik: `scripts/analiz/2026-10-21-olcek5k-ek-plan.py` · tohum `20261022` · tarih 2026-10-21
- Girdi: `data/plan/v6-parti8.jsonl` `b83155d0616addc9` · `data/seeds.v2.jsonl` `3399f543c8b882c7` · `data/plan/olcek5k.jsonl` `922926a97588363c` · eval-ref `d8cce150543a3470` · eleme `39b95444c6c8fc96`
- Çıktı: `data/plan/olcek5k-ek.jsonl` `c7ce336c387ee978`
- Uygun tohum: **1818**; elenen: BLEU referans tohumu 190 · eval tohumu 137 · kriz süzgeci 87 · eleme defteri 8
- Bu planda farklı tohum **700** · ölçek-5k + bu plan toplam kullanım: 3×: 700
- `bicim` sapması 47 · atlanan çekiliş 0

| sütun | dağılım |
|---|---|
| `bicim` | orta 291 · kisa 265 · uzun 144 |
| `register` | duzgun 525 · bozuk 175 |
| `turn_ending` | acik_uclu_soru 296 · yalnizca_yansitma 129 · takdir 126 · ozet 114 · durur 35 |
| `mi_process` | engaging 289 · evoking 173 · focusing 129 · planning 109 |
| `turn_type` | single 441 · multi 259 |
| `konusma_durumu` | tetikleyici_an 234 · suregiden_durum 152 · plan_yapma 112 · iyi_giden_paylasim 100 · merak_sorusu 70 · aradan_donus 32 |
| `sinir_tipi` | yok 600 · rol_siniri_yonlendirme 34 · yonlendirme_gereksiz 29 · sinir_cekme 20 · yonlendirme_istegi 17 |
| `senaryo_hedefi` | serbest 606 · nazikce_karsi_cikma 94 |
| `is_negative` | 0 592 · 1 108 |
| `ozerklik` | 0 575 · 1 125 |
| `context` | 0 518 · 1 182 |
| `baglam_davranisi` | None 518 · cevap_var 71 · cevap_yok 44 · ilgisiz 43 · izin_iste 24 |
| `tur` | alkol 180 · kumar 166 · tutun 144 · receteli_ilac 140 · dijital 70 |
| `yas` | yetiskin 605 · ergen 95 |
| `tohum_senaryo` | ambivalans 280 · belirsiz 170 · rol_siniri 130 · nazikce_karsi_cikma 112 · discord 5 · inkar 3 |
