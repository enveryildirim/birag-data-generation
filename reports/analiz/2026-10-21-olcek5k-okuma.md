# Ölçek-5k — C sonrası örneklem okuması

- Betik: `scripts/analiz/2026-10-21-olcek5k-okuma.py` · tohum `20261021` · tarih 2026-10-21
- Girdi: `data/candidates/olcek5k.jsonl` `866a1e13c9b0fd60` (parça 191 hariç 4955 kayıt)
- Okuyan: Claude Code (K43 — hata avı; puan değil)

| C modeli | n | temiz | küçük | ciddi |
|---|---:|---:|---:|---:|
| haiku | 14 | 10 | 2 | 2 |
| sonnet | 6 | 5 | 1 | 0 |

| id | C | slice | C kararı | sınıf | not |
|---|---|---|---|---|---|
| `c333c5c3` | haiku | rag_tek_tur | aynen | temiz | ilgisiz bağlam kullanılmamış; özerklik cümlesi kalıba yakın |
| `0a39bdfb` | haiku | terapotik_cok_tur | aynen | ciddi | çok turlu yapı ters: ilk mesaj bütün anlatıyı taşıyor, ikinci mesaj onu tekrarlıyor; «zor olmuş olmalı» varsayımı |
| `fd9fb625` | haiku | terapotik_tek_tur | aynen | temiz | reçeteli ilaç → hekim; ders yok |
| `e6fa12a5` | haiku | terapotik_cok_tur | duzeltildi | temiz |  |
| `efb9c8b0` | haiku | terapotik_cok_tur | aynen | ciddi | A açılışı ilk mesajda olmayan «son» sözüne dayanıyor (ikinci mesajdan sızmış) |
| `d1942eb0` | haiku | terapotik_tek_tur | aynen | temiz |  |
| `b6f4d3bf` | haiku | terapotik_tek_tur | duzeltildi | temiz | kaynak türü doğru |
| `420ee66b` | haiku | rag_cok_tur | duzeltildi | temiz | §5a″ sapması yerinde; izin_iste doğru |
| `9b6fb9a7` | haiku | rag_tek_tur | aynen | temiz |  |
| `1214e892` | haiku | terapotik_tek_tur | aynen | küçük | nazikce_karsi_cikma hedefi için karşı çıkılacak iddia zayıf |
| `64b2ded2` | haiku | rag_tek_tur | aynen | temiz |  |
| `3ffaa85d` | haiku | terapotik_tek_tur | aynen | temiz |  |
| `6d570a2a` | haiku | terapotik_tek_tur | aynen | küçük | dil: «…sesin ise seni bırakmaya çektiğini söylüyor» özne bozuk |
| `33c40c23` | haiku | terapotik_cok_tur | aynen | temiz |  |
| `ef1a4ee8` | sonnet | terapotik_tek_tur | duzeltildi | küçük | dil: «aileye söyleyemediğini ve utandığını» iki kez |
| `b49bce77` | sonnet | rag_tek_tur | aynen | temiz |  |
| `edfaf9a4` | sonnet | terapotik_cok_tur | aynen | temiz | §8c′ göster-tartışma iyi |
| `a91014f8` | sonnet | terapotik_cok_tur | duzeltildi | temiz |  |
| `2ca6a84d` | sonnet | terapotik_tek_tur | aynen | temiz |  |
| `7e51f20d` | sonnet | terapotik_tek_tur | aynen | temiz | aldatma aracı reddi yerinde |
