# v0.0.9 — kümülatif yargı dosyasının kaynak defteri

**Betik:** `scripts/analiz/2026-09-17-v008-kumulatif.py` · **Tarih:** 2026-09-17

## 1. Katmanlar (sıra önemlidir; sonraki öncekini değiştirir)

| # | dosya | SHA256-16 | kayıt | yeni | değiştirilen | not |
|---:|---|---|---:|---:|---:|---|
| 0 | `data/judged/v0.0.8.jsonl` | `a807678eb52221a2` | 577 | — | — | v0.0.8'in yargılanmış dosyası (kendisi de betikle kuruldu) |
| 1 | `data/judged/v5-parti3.v7.v9.jsonl` | `5ff7d04c1202710c` | 60 | 0 | 60 | v5-parti3 — §5a⁗ çıkmaz düzeltmesi (2 kayıt) |
| 2 | `data/judged/v5-parti4.v5.v9.jsonl` | `e8387730e617f740` | 60 | 0 | 60 | v5-parti4 — §5a⁗ çıkmaz düzeltmesi (4 kayıt) |
| 3 | `data/judged/v5-parti6.v6.v9.jsonl` | `203ecaf87139b4ea` | 60 | 0 | 60 | v5-parti6 — §5a⁗ çıkmaz düzeltmesi (3 kayıt) |
| 4 | `data/judged/v5-parti7.v6.v9.jsonl` | `bc39c9bbec83c7a2` | 60 | 0 | 60 | v5-parti7 — §5a⁗ çıkmaz düzeltmesi (1 kayıt) |
| 5 | `data/judged/v5-parti8.v6.v9.jsonl` | `d2e4ac8d601ac410` | 60 | 0 | 60 | v5-parti8 — §5a⁗ (3) + tanı iddiası (1) + yapısal atıf (2) |

⭐ **Sonuç: 577 tekil kayıt** · çıktı `data/judged/v0.0.9.jsonl` SHA256 `269554e30d8c5025`

## 2. ⛔ Aynı `id`, farklı metin

**14 kayıt** tabandakinden farklı metinle geldi. ⛔ Bu, v0.0.7 ile v0.0.8'in aynı `id` altında **farklı içerik** taşıdığı anlamına gelir ve iki sürümün puanları kayıt düzeyinde karşılaştırılamaz.

| id | kaynak | parti sırası |
|---|---|---:|
| `4c4d529f571af9f2` | `data/judged/v5-parti3.v7.v9.jsonl` | 2 |
| `2fbce5884eb4d183` | `data/judged/v5-parti3.v7.v9.jsonl` | 16 |
| `8d7666e7d954f326` | `data/judged/v5-parti4.v5.v9.jsonl` | 10 |
| `97abbe56d391f529` | `data/judged/v5-parti4.v5.v9.jsonl` | 12 |
| `e3b9b1f341ec38ef` | `data/judged/v5-parti4.v5.v9.jsonl` | 24 |
| `1728f166bfd27e68` | `data/judged/v5-parti4.v5.v9.jsonl` | 51 |
| `77b95e8d2a1b0b43` | `data/judged/v5-parti6.v6.v9.jsonl` | 11 |
| `375db25edf10ecda` | `data/judged/v5-parti6.v6.v9.jsonl` | 56 |
| `526d1cf03a43cc9a` | `data/judged/v5-parti6.v6.v9.jsonl` | 54 |
| `c272e5cfcff9f2e7` | `data/judged/v5-parti7.v6.v9.jsonl` | 1 |
| `935dfac08ec6ae71` | `data/judged/v5-parti8.v6.v9.jsonl` | 27 |
| `b05ad7e0988efea2` | `data/judged/v5-parti8.v6.v9.jsonl` | 29 |
| `1c34e236dfe19357` | `data/judged/v5-parti8.v6.v9.jsonl` | 13 |
| `06ce9ab5ebb06a4e` | `data/judged/v5-parti8.v6.v9.jsonl` | 15 |

## 3. Rubrik karışımı (K137)

| rubrik | kayıt |
|---|---:|
| `judge-eksen1.v9` | 422 |
| `judge-eksen1.v7` | 137 |
| `yok (replay/yargısız)` | 18 |

⚠️ **Farklı rubrik sürümleriyle verilmiş puanlar aynı tabloda havuzlanamaz** (K137: rubrik sürümü sıralamayı değiştiriyor).

## 4. Kapı öncesi durum

- yargılanmamış (replay olmayan): **0** ⇒ `build.py` bunları `judge_yok` ile eler (T121)
- klinik güvenlik ihlali: **6** ⇒ elenir

## ⛔ Bu defterin söylemedikleri

| | |
|---|---|
| ⛔ **Taban katman türetilmedi** | `v0.0.7.jsonl` elle birleştirilmişti; bu betik onu bir bütün olarak alır ve İÇİNİ açıklayamaz |
| ⛔ **Kalite değil köken** | tablo hangi kaydın nereden geldiğini söyler, iyi olup olmadığını söylemez |
| ⚠️ Çakışma ölçütü yalnız `messages` | `gen_meta` ya da `judge` farkları çakışma sayılmıyor |
