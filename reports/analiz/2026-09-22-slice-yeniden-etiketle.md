# `slice` yeniden etiketlendi — beyan yerine türetme

**Betik:** `scripts/analiz/2026-09-22-slice-yeniden-etiketle.py` · **Tarih:** 2026-09-22  
**Taranan:** 138 dosya, 5036 kayıt · **değişen: 1307**  

⭐ Kullanıcı kararı: *«slice'ı context'ten türet»* (T240). Alan artık `src/dilim.py`'de **tek bir yerden** türer: kip `context`'in doluluğundan, tur sayısı `messages`'taki `user` turlarından, `replay` ise kaydın kendi bayrağından.

## Ne değişti

| beyan | → türetilen | kayıt |
|---|---|---:|
| `rag_tek_tur` | `terapotik_tek_tur` | 643 |
| `cok_tur` | `terapotik_cok_tur` | 594 |
| `cok_tur` | `rag_cok_tur` | 66 |
| `terapotik_tek_tur` | `terapotik_cok_tur` | 4 |

⭐⭐ **En büyük iki kalem v6'nın sözlük kaymasıdır:** `rag_tek_tur` → `terapotik_tek_tur` ve `cok_tur` → `terapotik_cok_tur`. İkisi de aynı şeyi söylüyor: v6 kayıtları **bağlamı olmadığı hâlde RAG etiketi taşıyordu** ya da kipi hiç taşımıyordu.

⭐ **Bir kalem v6'dan değil:** `terapotik_tek_tur` → `terapotik_cok_tur`, **1 kayıt** (`v4-parti1 / d001bc7a8f`). Bu **K69**'un belgelenmiş kusuru — `kayit()`'in varsayılanı çok turlu bir kaydı tek tur diye damgalamıştı. ⇒ Türetme, K69'u aramadan buldu.

## Değişen dosyalar

| dosya | kayıt | değişen |
|---|---:|---:|
| `data/candidates/expert-70.jsonl` | 70 | 1 |
| `data/candidates/v0.0.4-doz10.jsonl` | 155 | 1 |
| `data/candidates/v0.0.5-doz25.jsonl` | 155 | 1 |
| `data/candidates/v4-parti1.jsonl` | 40 | 1 |
| `data/candidates/v4-parti1.v8.jsonl` | 40 | 1 |
| `data/candidates/v6-parti1.blok1.jsonl` | 4 | 4 |
| `data/candidates/v6-parti1.blok2.jsonl` | 6 | 4 |
| `data/candidates/v6-parti1.blok3.jsonl` | 8 | 7 |
| `data/candidates/v6-parti1.blok4.jsonl` | 8 | 8 |
| `data/candidates/v6-parti1.blok5.jsonl` | 7 | 3 |
| `data/candidates/v6-parti1.blok6.jsonl` | 8 | 7 |
| `data/candidates/v6-parti1.blok7.jsonl` | 8 | 7 |
| `data/candidates/v6-parti1.blok8.jsonl` | 8 | 7 |
| `data/candidates/v6-parti1.blok9.jsonl` | 2 | 1 |
| `data/candidates/v6-parti1.jsonl` | 59 | 48 |
| `data/candidates/v6-parti2.blok1.jsonl` | 10 | 9 |
| `data/candidates/v6-parti2.blok2.jsonl` | 10 | 8 |
| `data/candidates/v6-parti2.blok3.jsonl` | 10 | 6 |
| `data/candidates/v6-parti2.blok4.jsonl` | 10 | 5 |
| `data/candidates/v6-parti2.blok5.jsonl` | 10 | 9 |
| `data/candidates/v6-parti2.blok6.jsonl` | 9 | 8 |
| `data/candidates/v6-parti2.jsonl` | 59 | 45 |
| `data/candidates/v6-parti3.blok1.jsonl` | 10 | 7 |
| `data/candidates/v6-parti3.blok2.jsonl` | 10 | 8 |
| `data/candidates/v6-parti3.blok3.jsonl` | 10 | 9 |
| `data/candidates/v6-parti3.blok4.jsonl` | 10 | 9 |
| `data/candidates/v6-parti3.blok5.jsonl` | 10 | 8 |
| `data/candidates/v6-parti3.blok6.jsonl` | 10 | 7 |
| `data/candidates/v6-parti3.jsonl` | 60 | 48 |
| `data/candidates/v6-parti4.blok1.jsonl` | 10 | 7 |
| `data/candidates/v6-parti4.blok2.jsonl` | 9 | 7 |
| `data/candidates/v6-parti4.blok3.jsonl` | 10 | 10 |
| `data/candidates/v6-parti4.blok4.jsonl` | 10 | 8 |
| `data/candidates/v6-parti4.blok5.jsonl` | 10 | 8 |
| `data/candidates/v6-parti4.blok6.jsonl` | 10 | 7 |
| `data/candidates/v6-parti4.jsonl` | 59 | 47 |
| `data/candidates/v6-parti5.blok1.jsonl` | 10 | 9 |
| `data/candidates/v6-parti5.blok2.jsonl` | 10 | 6 |
| `data/candidates/v6-parti5.blok3.jsonl` | 10 | 8 |
| `data/candidates/v6-parti5.blok4.jsonl` | 10 | 8 |
| `data/candidates/v6-parti5.blok5.jsonl` | 10 | 8 |
| `data/candidates/v6-parti5.blok6.jsonl` | 10 | 9 |
| `data/candidates/v6-parti5.jsonl` | 60 | 48 |
| `data/candidates/v6-parti6.blok1.jsonl` | 9 | 7 |
| `data/candidates/v6-parti6.blok2.jsonl` | 10 | 7 |
| `data/candidates/v6-parti6.blok3.jsonl` | 10 | 9 |
| `data/candidates/v6-parti6.blok4.jsonl` | 9 | 5 |
| `data/candidates/v6-parti6.blok5.jsonl` | 10 | 9 |
| `data/candidates/v6-parti6.blok6.jsonl` | 10 | 7 |
| `data/candidates/v6-parti6.jsonl` | 58 | 44 |
| `data/candidates/v6-parti7.blok1.jsonl` | 9 | 6 |
| `data/candidates/v6-parti7.blok2.jsonl` | 10 | 9 |
| `data/candidates/v6-parti7.blok3.jsonl` | 10 | 6 |
| `data/candidates/v6-parti7.blok4.jsonl` | 10 | 8 |
| `data/candidates/v6-parti7.blok5.jsonl` | 9 | 6 |
| `data/candidates/v6-parti7.blok6.jsonl` | 9 | 8 |
| `data/candidates/v6-parti7.jsonl` | 57 | 43 |
| `data/candidates/v6-parti8.blok1.jsonl` | 39 | 31 |
| `data/candidates/v6-parti8.blok2.jsonl` | 40 | 30 |
| `data/candidates/v6-parti8.blok3.jsonl` | 39 | 34 |
| `data/candidates/v6-parti8.jsonl` | 118 | 95 |
| `data/judged/v6-parti1.jsonl` | 59 | 48 |
| `data/judged/v6-parti2.jsonl` | 59 | 45 |
| `data/judged/v6-parti3.claude.jsonl` | 60 | 48 |
| `data/judged/v6-parti3.jsonl` | 60 | 48 |
| `data/judged/v6-parti4.claude.jsonl` | 59 | 47 |
| `data/judged/v6-parti5.claude.jsonl` | 60 | 48 |
| `data/judged/v6-parti6.claude.jsonl` | 58 | 44 |
| `data/judged/v6-parti7.claude.jsonl` | 57 | 43 |
| `data/judged/v6-parti8.claude.jsonl` | 118 | 95 |

## ⛔ Dokunulmayanlar

| | |
|---|---|
| `datasets/` | IMMUTABLE (Kural 4) ⇒ **`v0.0.15` eski etiketlerle kaldı**; kartı zaten `slice` dağılımı yazmıyor ve nedenini açıklıyor |
| `data/judged/v0.0.*.jsonl` | derleme girdisi anlık görüntüleri; SHA256'ları manifest'lerde yazılı (Kural 7) ⇒ bir sonraki derleme bunları okumaz, dilimi **birleştirme anında yeniden türetir** |
| `data/seeds*.jsonl` | IMMUTABLE |

## ⭐ Artık bir kapı var

`src/checks.py` beyan ile türetileni karşılaştırır (`dilim_ok`) ve ayrışırsa kayıt **düşer**. ⛔ Bu, T237'nin dersinin uygulanmasıdır: *bir sınır yazıldığında aynı commit'te onu uygulayan kod da yazılır.* Kapı ancak biri dilimi **elle** yazarsa ateşler — çünkü üretim ve birleştirme artık türetiyor.

## ⛔ Bunun söylemedikleri

| | |
|---|---|
| ⛔ **Yayımlanmış kartlar geriye dönük düzelmedi** | `v0.0.5`–`v0.0.11` v5 sözlüğüyle derlendi ve o sözlükte sayıları **doğruydu**; `v0.0.15` ise `slice` dağılımını hiç yazmıyor |
| ⚠️ **Türetme bir TANIM seçimidir** | *«bağlamı olan kayıt RAG'dir»* denildi; bağlamı olup da cevabı bağlamı kullanmayan kayıt da RAG sayılır. Başka bir tanım (*«cevap bağlamı KULLANIYOR mu»*) ölçülmedi ve daha zordur |
| ⚠️ **`cok_tur` bağlamlı 21 kayıt** | yeni sözlükte `rag_cok_tur` oldular; v6'da bu birleşim hiç adlandırılmamıştı |
