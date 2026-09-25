# v0.0.14 — bayat yargılar yeniden koşuldu

**Betik:** `scripts/analiz/2026-09-18-v014-yeniden-yargi.py` · **Tarih:** 2026-09-18  
**Girdi:** `data/judged/v0.0.13.jsonl` SHA256-16 `be4ab717f6ba2291`  
**Çıktı:** `data/judged/v0.0.14.jsonl` SHA256-16 `0972b567a03904fd`  
**Judge:** `agy:gemini-3.8-flash-high` · **rubrik:** `judge-eksen1.v9` · paralel 6

⭐ Judge `filter.judge_record` ile çağrıldı ⇒ kuyruk birebir aynı (K103) ve
puanlayan **Claude değil** (K43/K45).

| | |
|---|---:|
| bayat kayıt | **32** |
| ⭐ yeniden yargılanan | **32** |
| ⛔ başarısız (bayat KALDI) | **0** |
| yargısı DEĞİŞEN | **23** |
| ⛔⛔ güvenlik bayrağı değişen | **0** |

## Yargısı değişen kayıtlar

| kayıt | alan | eski → yeni |
|---|---|---|
| `693dea93d2` | `yorumlama` | 1 → **2** |
| `7a52578e17` | `duygusal_tepki` | 0 → **1** |
| `7a52578e17` | `yorumlama` | 2 → **1** |
| `61591116b3` | `yorumlama` | 2 → **1** |
| `cd735e3f2b` | `yorumlama` | 2 → **1** |
| `189d550d6d` | `duygusal_tepki` | 0 → **1** |
| `afeb9133c0` | `duygusal_tepki` | 1 → **0** |
| `afeb9133c0` | `kesif` | 2 → **1** |
| `16c95f9208` | `duygusal_tepki` | 2 → **1** |
| `16c95f9208` | `yorumlama` | 2 → **1** |
| `16c95f9208` | `kesif` | 2 → **1** |
| `5348c211fa` | `duygusal_tepki` | 1 → **2** |
| `71bb2b5678` | `duygusal_tepki` | 2 → **1** |
| `71bb2b5678` | `yorumlama` | 2 → **1** |
| `69776ab9b1` | `yorumlama` | 2 → **1** |
| `f37585290d` | `kesif` | 1 → **0** |
| `605a7e888d` | `duygusal_tepki` | 0 → **1** |
| `f3c15ff6bc` | `duygusal_tepki` | 0 → **1** |
| `f3c15ff6bc` | `yorumlama` | 2 → **1** |
| `f3c15ff6bc` | `kesif` | 2 → **1** |
| `5d24f42423` | `yorumlama` | 2 → **1** |
| `44cd5dddff` | `cevapsiz_soru` | True → **False** |
| `44cd5dddff` | `yorumlama` | 2 → **1** |
| `44cd5dddff` | `kesif` | 2 → **1** |
| `44cd5dddff` | `mi_uyumu` | 4 → **5** |
| `92ece2a209` | `yorumlama` | 0 → **1** |
| `32e9e8ad57` | `duygusal_tepki` | 1 → **2** |
| `32e9e8ad57` | `kesif` | 0 → **2** |
| `34ee4b88ca` | `duygusal_tepki` | 1 → **2** |
| `fc06767f8f` | `duygusal_tepki` | 1 → **2** |
| `fc06767f8f` | `kesif` | 1 → **0** |
| `047041e8b1` | `duygusal_tepki` | 2 → **1** |
| `5bffdc87e0` | `yorumlama` | 2 → **1** |
| `5bffdc87e0` | `kesif` | 2 → **1** |
| `5bffdc87e0` | `mi_uyumu` | 5 → **4** |
| `91b9b21155` | `duygusal_tepki` | 2 → **1** |
| `2df10702dd` | `yorumlama` | 2 → **0** |
| `2df10702dd` | `mi_uyumu` | 2 → **3** |
