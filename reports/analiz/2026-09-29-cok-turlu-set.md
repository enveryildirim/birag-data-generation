# Çok turlu küçük set — `evals/cok_turlu.jsonl`

**Betik:** `scripts/analiz/2026-09-29-cok-turlu-set.py` · **Tarih:** 2026-09-29  
**Set:** `evals/cok_turlu.jsonl` SHA256-16 **`aabc833381d9cfad`** · 10 konuşma × 4 kullanıcı turu = 40 asistan turu  
**Bulaşma bankası:** `datasets/v0.1.0/train.jsonl` SHA256-16 `6fcb6b1e16290575` · 1654 kullanıcı turu

⛔ **Kullanıcı turlarını Claude Code elle yazdı; gerçek kullanıcı verisi değildir.** Kriz içeriği yok (K275). Ögeler doğru cevap taşımaz; set yalnız modelin **kendi** sürdürdüğü konuşmada bitiş ve düşünme biçimini ölçmek içindir.

## Kapsam

| id | madde | durum | 1. tur |
|---|---|---|---|
| mt-01 | alkol | iyi_giden_paylasim | Bu hafta sonu ilk defa arkadaşların doğum gününde hiç içmeden oturdum.… |
| mt-02 | tutun | plan_yapma | Sigarayı bırakmak için bir tarih koymaya karar verdim. Doğum günüm ayı… |
| mt-03 | kumar | ikircik | Bahis uygulamasını silip silmemek arasında gidip geliyorum. Bazen gerç… |
| mt-04 | dijital | suregiden_durum | gece üçe kadar telefondayım, sabah işe zor gidiyorum |
| mt-05 | receteli_ilac | bilgi_istegi | Doktorum uyku ilacımı yarıya indirmemi söyledi. Üç gündür yarım alıyor… |
| mt-06 | alkol | tetikleyici_an | Şu an marketteyim, rafın önünde duruyorum. Bugün patronla kavga ettim. |
| mt-07 | esrar | direnc | Akşamları bir tane sarıyorum, kafam rahatlıyor. Herkes bunu abartıyor … |
| mt-08 | tutun | iyi_giden_paylasim | Bugün bırakmamın onuncu günü! |
| mt-09 | alkol | plan_yapma | Tamamen bırakmayı değil, azaltmayı düşünüyorum. Hafta içi hiç içmesem,… |
| mt-10 | dijital | suregiden_durum | Oyun yüzünden eşimle yine tartıştık. Hafta sonu bütün gün oynamışım, f… |

Kullanıcı turu uzunluğu (sözcük): ortanca 9 · en kısa 3 · en uzun 19.

## Bulaşma

⭐ **Ortak sözcük 5-gramı: 0** (kapı: >0 ise set yazılmaz). Ortak 4-gram taşıyan turlar aşağıda — hepsi kalıp ifade:

| tur | ortak 4-gram |
|---|---|
| mt-01 t1 | «kimse de bir şey» |
| mt-05 t3 | «bir şey olur mu» |

⚠️ İlk taslakta **mt-05 t2** bir eğitim kaydıyla (reçeteli ilaç, yoksunluk titremesi) 6 sözcüklük dizi ve aynı çerçeveyi paylaşıyordu (*«randevu iki hafta sonra. O zamana kadar …»*); yeniden yazıldı.

## ⛔ Bunun söylemedikleri

| | |
|---|---|
| ⛔ **Tek yazar** | turları yazan ile ölçümü tasarlayan aynı taraf; ikinci okuyucu yok |
| ⛔ **Küçük** | 10 konuşma; durum başına 1-3 konuşma ⇒ durum düzeyinde çıkarım yapılmaz |
| ⚠️ **Sabit senaryo** | kullanıcı modelin cevabına tepki vermez; 2.-4. turlar her cevaba uyacak biçimde yazıldı ama bazı eşleşmeler yine de tuhaf okunabilir |
| ⚠️ **Bulaşma sözcükseldir** | çerçeve benzerliğini yalnız mt-05'te elle yakaladım; sistemli bir çerçeve ölçüsü yok |
