# Haiku pilotu — tasarım ızgarası (60 kayıt)

- Betik: `scripts/analiz/2026-10-20-haiku-pilot-plan.py` · tohum `20261020`
- Girdi: `data/plan/v6-parti8.jsonl` SHA256/16 `b83155d0616addc9` · `data/seeds.v2.jsonl` `3399f543c8b882c7`
- Çıktı: `data/plan/haiku-pilot.jsonl` `eb507c570435c69f`
- Serbest tohum (tek turlu, hiç kullanılmamış, kriz süzgeçlerinden geçmiş): **996** / 2240 · süzgeçlerin elediği 70
- `bicim` sapması (tohum kısa): 1

| sütun | dağılım |
|---|---|
| `bicim` | orta 25 · kisa 23 · uzun 12 |
| `register` | duzgun 44 · bozuk 16 |
| `turn_ending` | acik_uclu_soru 30 · takdir 11 · yalnizca_yansitma 8 · ozet 7 · durur 4 |
| `mi_process` | engaging 22 · evoking 14 · planning 13 · focusing 11 |
| `turn_type` | single 35 · multi 25 |
| `konusma_durumu` | tetikleyici_an 22 · plan_yapma 11 · suregiden_durum 10 · merak_sorusu 8 · iyi_giden_paylasim 6 · aradan_donus 3 |
| `sinir_tipi` | yok 53 · rol_siniri_yonlendirme 4 · yonlendirme_istegi 2 · sinir_cekme 1 |
| `senaryo_hedefi` | serbest 53 · nazikce_karsi_cikma 7 |
| `is_negative` | 0 50 · 1 10 |
| `ozerklik` | 0 48 · 1 12 |
| `context` | 0 45 · 1 15 |
| `baglam_davranisi` | None 45 · cevap_var 6 · cevap_yok 5 · izin_iste 2 · ilgisiz 2 |
| `tur` | alkol 18 · kumar 16 · receteli_ilac 13 · tutun 9 · dijital 4 |
| `yas` | yetiskin 54 · ergen 6 |
| `tohum_senaryo` | ambivalans 29 · nazikce_karsi_cikma 12 · belirsiz 10 · rol_siniri 8 · discord 1 |
