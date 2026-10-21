# Haiku pilotu — şablon sıklığı

- Betik: `scripts/analiz/2026-10-20-haiku-pilot-sablon.py`
- Girdi: `data/candidates/haiku-pilot.taslak.blok1.jsonl` `f76d68f667856dd1` · `data/candidates/haiku-pilot.taslak.blok2.jsonl` `70cd68b2ce70fac9` · `data/candidates/haiku-pilot.taslak.blok3.jsonl` `144156b8817e08ca`
- Zemin: `datasets/v0.1.1/train.jsonl` `f8fcaa1e96603cb2`, yalnız `gen_meta.parti = v6-parti8*` (93 kayıt)
- Sayım KAYIT başına (bir kayıtta kaç kez geçtiği değil, geçip geçmediği). Desenler `tr_fold` edilmiş metinde aranır.

| kalıp | yer | Haiku | parti8 (Opus taslak + revizyon) |
|---|---|---:|---:|
| «… adım gibi duruyor / adım olabilir» | son | 11/60 (%18) | 1/93 (%1) |
| «yazman önemli / anlatman önemli» | son | 5/60 (%8) | 0/93 (%0) |
| «kolay olmamıştır / kolay olmaz» | son | 4/60 (%7) | 0/93 (%0) |
| «… duyuyorum» | son | 10/60 (%17) | 0/93 (%0) |
| «… karar sende / senin kararın» | son | 12/60 (%20) | 10/93 (%11) |
| «hüküm ver… / … bana düşmez» | son | 12/60 (%20) | 1/93 (%1) |
| iskele sözcüğü «adlandırıyorum / adıyla anıyorum» | son | 3/60 (%5) | 0/93 (%0) |
| açılış «Dinliyorum / Buradayım» | acilis | 21/25 (%84) | 4/40 (%10) |
