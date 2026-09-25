# T227 kararının kayıtlara işlenmesi

**Betik:** `scripts/analiz/2026-09-21-red-beyani-uzlasmaya-gore.py` · **Tarih:** 2026-09-21  
**Kip:** YAZILDI  

Dokunulan kayıt örneği (blok + birleşik, yinelemeli): **52**  
Değeri değişen: **8**

| kayıt | dosya | eski | **yeni** |
|---|---|:-:|:-:|
| `v6-parti1#11` | `v6-parti1.blok2.jsonl` | — | **red** |
| `v6-parti1#11` | `v6-parti1.jsonl` | — | **red** |
| `v6-parti2#41` | `v6-parti2.blok5.jsonl` | — | **red** |
| `v6-parti2#41` | `v6-parti2.jsonl` | — | **red** |
| `v6-parti4#20` | `v6-parti4.blok2.jsonl` | — | **red** |
| `v6-parti4#20` | `v6-parti4.jsonl` | — | **red** |
| `v6-parti6#54` | `v6-parti6.blok6.jsonl` | — | **red** |
| `v6-parti6#54` | `v6-parti6.jsonl` | — | **red** |

⭐ Blok ↔ birleşik tutarsızlığı: **0**

## ⛔ Bu adımın söylemedikleri

| | |
|---|---|
| ⛔⛔ **Karar üç Claude anotatörünün çoğunluğu** | uzman değil; `gen_meta.is_negative_oylar`'da üç oy da duruyor ve geri alınabilir |
| ⛔ **`ozerklik_vurgusu` DEĞİŞMEDİ** | aynı yapı orada da var ama ölçülmedi; açık kalem |
| ⚠️ **Birleştirme yeniden koşulmadı** | parti1'in planı üretimden sonra değişmişti (T224) ⇒ künye kapısı reddederdi. Alan cerrahi güncellendi ve iki dosya arasındaki tutarlılık ayrıca denetlendi |
