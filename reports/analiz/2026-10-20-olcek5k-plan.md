# Ölçek-5k — tasarım ızgarası (5000 kayıt, 200 parça × 25)

- Betik: `scripts/analiz/2026-10-20-olcek5k-plan.py` · tohum `20261021`
- Girdi: `data/plan/v6-parti8.jsonl` `b83155d0616addc9` · `data/seeds.v2.jsonl` `3399f543c8b882c7`
- Çıktı: `data/plan/olcek5k.jsonl` `922926a97588363c`
- Uygun tohum (tek turlu, kriz süzgeçlerinden geçmiş): **2153** / 2240; bu planda kullanılan farklı tohum **2153**
- ⛔ Önceden (v0.1.1 / eski partiler / pilot) kullanılmış tohumdan gelen satır: **5000** / 5000
- Tohum başına kullanım dağılımı: 2×: 1459 · 3×: 694
- `bicim` sapması 251 · uygun tohum bulunamayıp atlanan çekiliş 0

| sütun | dağılım |
|---|---|
| `bicim` | kisa 1980 · orta 1961 · uzun 1059 |
| `register` | duzgun 3718 · bozuk 1282 |
| `turn_ending` | acik_uclu_soru 2421 · yalnizca_yansitma 828 · ozet 758 · takdir 735 · durur 258 |
| `mi_process` | engaging 1998 · evoking 1221 · focusing 1031 · planning 750 |
| `turn_type` | single 3020 · multi 1980 |
| `konusma_durumu` | tetikleyici_an 1773 · suregiden_durum 969 · plan_yapma 770 · iyi_giden_paylasim 731 · merak_sorusu 500 · aradan_donus 257 |
| `sinir_tipi` | yok 4255 · rol_siniri_yonlendirme 229 · yonlendirme_gereksiz 190 · yonlendirme_istegi 163 · sinir_cekme 163 |
| `senaryo_hedefi` | serbest 4266 · nazikce_karsi_cikma 734 |
| `is_negative` | 0 4247 · 1 753 |
| `ozerklik` | 0 4003 · 1 997 |
| `context` | 0 3719 · 1 1281 |
| `baglam_davranisi` | None 3719 · cevap_var 478 · cevap_yok 337 · ilgisiz 285 · izin_iste 181 |
| `tur` | alkol 1358 · tutun 1128 · kumar 1105 · receteli_ilac 948 · dijital 461 |
| `yas` | yetiskin 4410 · ergen 590 |
| `tohum_senaryo` | ambivalans 1915 · belirsiz 1213 · rol_siniri 1070 · nazikce_karsi_cikma 731 · inkar 48 · discord 23 |
