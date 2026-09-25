# v0.0.8 — kümülatif yargı dosyasının kaynak defteri

**Betik:** `scripts/analiz/2026-09-17-v008-kumulatif.py` · **Tarih:** 2026-09-17

## 1. Katmanlar (sıra önemlidir; sonraki öncekini değiştirir)

| # | dosya | SHA256-16 | kayıt | yeni | değiştirilen | not |
|---:|---|---|---:|---:|---:|---|
| 0 | `data/judged/v0.0.7.jsonl` | `71e501a047179dc6` | 275 | — | — | v0.0.7'nin yargılanmış dosyası |
| 1 | `data/judged/v4-parti1.v8.v9.jsonl` | `b485312adc105eef` | 40 | 2 | 38 | v4-parti1 — alıntı düzeltmeleri; kapılar bu katmana ilk kez geriye dönük koşuldu (T129) |
| 2 | `data/judged/v4-parti2.v3.v9.jsonl` | `4c3f076e51369a70` | 60 | 0 | 60 | v4-parti2 — alıntı/mekân düzeltmeleri (T129) |
| 3 | `data/judged/v5-parti3.v6.v9.jsonl` | `00cde92f11d39b59` | 60 | 0 | 60 | v5-parti3 — §8b′, T115 ve yapısal atıf düzeltmeleri; ⛔ v0.0.7 bu kayıtları v2 hâliyle taşır ⇒ AYNI id, FARKLI metin |
| 4 | `data/judged/v5-parti4.v4.v9.jsonl` | `2eb3a2a82f76973b` | 60 | 60 | 0 | v5-parti4 — K1/K2 revizyonlu |
| 5 | `data/judged/v5-parti5.v5.v9.jsonl` | `67aa7a0b068ab652` | 60 | 60 | 0 | v5-parti5 — K1/K2 + yapısal atıf |
| 6 | `data/judged/v5-parti6.v5.v9.jsonl` | `9ce109ad375d2ff6` | 60 | 60 | 0 | v5-parti6 — K1/K2 + §5a⁗ + yapısal atıf |
| 7 | `data/judged/v5-parti7.v5.v9.jsonl` | `af611e4076a40031` | 60 | 60 | 0 | v5-parti7 — K1/K2 revizyonlu |
| 8 | `data/judged/v5-parti8.v5.v9.jsonl` | `71c8d147b73a3758` | 60 | 60 | 0 | v5-parti8 — K1/K2 + yapısal atıf |

⭐ **Sonuç: 577 tekil kayıt** · çıktı `data/judged/v0.0.8.jsonl` SHA256 `a807678eb52221a2`

## 2. ⛔ Aynı `id`, farklı metin

**16 kayıt** tabandakinden farklı metinle geldi. ⛔ Bu, v0.0.7 ile v0.0.8'in aynı `id` altında **farklı içerik** taşıdığı anlamına gelir ve iki sürümün puanları kayıt düzeyinde karşılaştırılamaz.

| id | kaynak | parti sırası |
|---|---|---:|
| `719823508e124d2a` | `data/judged/v4-parti1.v8.v9.jsonl` | 8 |
| `44cd5dddffa56418` | `data/judged/v4-parti1.v8.v9.jsonl` | 10 |
| `6bfb464c417925b4` | `data/judged/v4-parti1.v8.v9.jsonl` | 12 |
| `b1b92fd913b34c28` | `data/judged/v4-parti1.v8.v9.jsonl` | 15 |
| `e9c273a5ad251288` | `data/judged/v4-parti1.v8.v9.jsonl` | 18 |
| `c3e09721ddbdcfbb` | `data/judged/v4-parti1.v8.v9.jsonl` | 20 |
| `96df24c1ba532186` | `data/judged/v4-parti1.v8.v9.jsonl` | 26 |
| `ee3af4cdad15604c` | `data/judged/v4-parti2.v3.v9.jsonl` | 11 |
| `285fbe6111622a35` | `data/judged/v4-parti2.v3.v9.jsonl` | 20 |
| `4a9e763c02a1cc71` | `data/judged/v4-parti2.v3.v9.jsonl` | 32 |
| `c8b282befd6cb1c4` | `data/judged/v4-parti2.v3.v9.jsonl` | 49 |
| `8325fed79c8b5e89` | `data/judged/v5-parti3.v6.v9.jsonl` | 14 |
| `fc25f1cfd3d43b23` | `data/judged/v5-parti3.v6.v9.jsonl` | 9 |
| `277e97b617b85cb5` | `data/judged/v5-parti3.v6.v9.jsonl` | 37 |
| `c47c3e344c07e112` | `data/judged/v5-parti3.v6.v9.jsonl` | 52 |
| `92a16fd61bf1aa70` | `data/judged/v5-parti3.v6.v9.jsonl` | 54 |

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
