# `gen_meta.bicim` yeniden etiketlendi — beyan yerine türetme

**Betik:** `scripts/analiz/2026-09-22-bant-yeniden-etiketle.py` · **Tarih:** 2026-09-22  
**Taranan:** 141 dosya, 4452 bant beyanı · **değişen: 0**  

⛔⛔ **Aynı `gen_meta` sözlüğündeki ÜÇÜNCÜ aynı kusur:** `slice` (T240) · `date` (T244) · **`bicim`**. Üçü de beyan edildi, üçü de sessizce kaydı, üçünü de kapı görmedi.

⭐ **Nasıl çıktı:** `celiskili` pilotunda bantları elle beyan ettim ve ikisi yanlış çıktı; **kendi işimi denetlerken** buldum, kapı değil.

## Geçişler

| beyan | → sayılan | kayıt |
|---|---|---:|
| `orta` | `uzun` | 286 _(tarihsel)_ |
| `kisa` | `orta` | 1 _(tarihsel)_ |

⚠️ Bu koşu **0 değişiklik** buldu; satırlar 2026-09-22 ilk uygulamasının sayımıdır.

⭐⭐ **Bulgu TEK YÖNLÜ:** uyumsuzlukların tamamı `orta` → `uzun`. Hiç `uzun → orta`, hiç `kisa` uyumsuzluğu yok. ⇒ `orta` bandı sistematik olarak **yukarı taşıyor**: üretici 25 sözcük sınırını aşarken fark etmiyor. Bu bir **üretim sadakati** bulgusudur, etiketleme kusuru değil.

## Kota dağılımına etkisi

| bant | beyan | **sayılan** |
|---|---:|---:|
| `kisa` | 397 | **396** |
| `orta` | 589 | **304** |
| `uzun` | 10 | **296** |

⚠️ **Düzeltme 2026-09-22'de UYGULANDI; bu koşu değişiklik bulmadı.** «Beyan» sütunu ilk uygulamanın geçiş sayımından **geri hesaplandı** {'orta→uzun': 286, 'kisa→orta': 1} ⇒ **tarihsel**, bu koşuda ölçülmüş değil.

⛔ §6 bant kotası o gün **tutturulmamıştı**: raporlanan `orta` payı gerçekte olduğundan yüksekti.

## Değişen dosyalar

| dosya | kayıt | değişen |
|---|---:|---:|
| _(bu koşuda değişen dosya yok)_ | — | 0 |

## ⛔ Bunun söylemedikleri

| | |
|---|---|
| ⛔ **Dokunulmayanlar** | `datasets/` IMMUTABLE ve `data/judged/v0.0.*.jsonl` anlık görüntüleri Kural 7 gereği yerinde; birleştirme bantı **türeterek** okumalı |
| ⛔ **Metin değişmedi** | yalnız etiket düzeldi; hiçbir kaydın kullanıcı mesajı kısaltılmadı |
| ⚠️ **Eşikler v4 §6'dan** | kisa ≤8 · orta 9-25 · uzun >25; eşik değişirse bu sayılar değişir |
| ⚠️ **Sebep izlenmedi** | `orta` bandının neden yukarı taştığı (üretici eğilimi mi, ızgara mı) **ölçülmedi** |
