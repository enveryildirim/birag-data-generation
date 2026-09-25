# Yetki aşan güvence taraması

**Betik:** `scripts/analiz/2026-09-22-yetki-asan-guvence-taramasi.py` · **Tarih:** 2026-09-22  
**Girdi:** `data/candidates/` — 28 dosya, 1656 kayıt  
**Eşleşme:** 1  

⭐ **Bu betik bir KURAL koymaz, SAYAR.** `gd-033` elendi ama eleme bir kapı değildir; modelin mahremiyet konusunda ne diyebileceği **uzman kalemidir** (`docs/uzman-brifingi.md` §8.4, 2. soru açık). K66: bir sınır yazıldığında ya onu uygulayan kod ya da onu ölçen rapor satırı yazılır — bu, ikincisidir.

⛔⛔ **Sayı tek başına hüküm değildir.** Eşleşen her cümle aşağıda yazılı; **okunmadan** sayılmaz. Bu betiğin ilk sürümü `kimseye söylemem` kolunu `kimseye söylememişsin` içinde eşleştirmiş ve 14 eşleşmenin 13'ü yanlış pozitif çıkmıştı (T22 serisi, 17. satır) ⇒ kollar `\b` ile kapatıldı ve yalnız 1. tekil / kişisiz gelecek kipleri arıyor.

## Eşleşmeler — hepsi OKUNACAK

| dosya | kayıt | tür | cümle |
|---|---|---|---|
| `v6-parti8` | `ad5658bcb7` | gizlilik | Burada söylediklerinin dışarı çıkmayacağını bilmen önemli, bunu sana kimsenin bakışını düşünmeden anlatabilesin diye söylüyorum. |

## ⛔ Bu taramanın söylemedikleri

| | |
|---|---|
| ⛔⛔ **ALT SINIR** | sezici dizge tabanlı ve Türkçe serbest metinde koşuyor — T22 serisinin bütünü bu biçimin yanıldığını gösteriyor ⇒ bulunmayan, olmadığı anlamına gelmez |
| ⛔ **`gd-033` bu taramada ÇIKMAZ** | kayıt elendi ama `data/candidates/v6-parti8.jsonl` içinde duruyor (Kural 7) ⇒ eşleşmesi beklenir ve bu bir HATA değil, elemenin `build.py` karantinasında olduğunun kanıtıdır |
| ⚠️ **«Yetki aşan» tanımı YAZILI DEĞİL** | üç kalıp ailesi benim önerim; hangi güvencenin yetki aşımı sayılacağı uzman kararıdır |
