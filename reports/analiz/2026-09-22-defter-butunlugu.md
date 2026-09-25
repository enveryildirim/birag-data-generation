# Katkı defteri bütünlük denetimi

**Betik:** `scripts/analiz/2026-09-22-defter-butunlugu.py` · **Tarih:** 2026-09-22  
**Defter:** 275 kalem · **gün süzgeci:** 2026-09-22  
**Bulgu:** ⛔ **16 kopukluk**  

⛔⛔ **Neden var:** bugün üç kez bir yama betiği düştü, `write_text` hiç koşmadı, ama commit *«kalem yazıldı»* dedi. K66/T237 ailesi — kural yazılı, kapı yok. Bu betik o kapıdır (ölçen türden).

## Sonuç

| kopukluk | sayı |
|---|---:|
| 1. çakışan numara | 0 |
| 2. kopuk 📎 (dosya yok) | 0 |
| 3. ölü atıf (kalem yok) | 0 |
| 4. deftere girmemiş rapor (2026-09-22) | 15 |
| 5. commit ↔ defter kopukluğu | 1 |

### ⛔ 4. Deftere girmemiş raporlar

- `reports/analiz/2026-09-22-celiskili-eval-bulasma.md`
- `reports/analiz/2026-09-22-celiskili-p3-yargi-tazele.md`
- `reports/analiz/2026-09-22-celiskili-yargi-tazele.md`
- `reports/analiz/2026-09-22-defter-butunlugu.md`
- `reports/analiz/2026-09-22-ozerklik-kaynagi-parti8.md`
- `reports/analiz/2026-09-22-slice-yeniden-etiketle.md`
- `reports/analiz/2026-09-22-t168-ingilizce-kontrol-birlesik.md`
- `reports/analiz/2026-09-22-t168-ingilizce-kontrol-onkayit.md`
- `reports/analiz/2026-09-22-t168-ingilizce-kontrol-tur2.md`
- `reports/analiz/2026-09-22-t168-ingilizce-kontrol.md`
- `reports/analiz/2026-09-22-v0.0.16-girdi.md`
- `reports/analiz/2026-09-22-v0.0.17-girdi.md`
- `reports/analiz/2026-09-22-v0.0.18-girdi.md`
- `reports/analiz/2026-09-22-v0015-girdi.md`
- `reports/analiz/2026-09-22-yetki-asan-guvence-taramasi.md`

### ⛔ 5. Commit ↔ defter

- `a153e03` **T250** — *«T250: unutma gerilemesi iki ayrı kusurdan — biçim korunuyor,»*

## ⛔ Bu denetimin söylemedikleri

| | |
|---|---|
| ⛔⛔ **İçeriği denetlemez** | bir kalemin **yazılmış** olduğunu gösterir, **doğru** olduğunu değil |
| ⛔ **4. madde yalnız bir günü tarar** | `--gun` ile değişir; bütün geçmiş taranmıyor çünkü eski raporların bir kısmı bilerek kalemsizdir |
| ⛔ **5. madde commit iletisi biçimine bağlı** | yalnız `Tn:` ile **başlayan** iletiler denetlenir; başka biçimde anılan kalemler görünmez |
| ⛔ **Kapının kendi yanlış pozitifi vardı** | ilk sürüm `…-t{7,13,23}.yaml` kısaltma yazımını kopuk yol sandı; **okuyarak** bulundu ve açılım eklendi — T22 ailesinin biçimi |
| ⚠️ **2. madde yalnız 📎'den sonrasına bakar** | gövde içinde örnek olarak geçen yollar denetlenmez, yoksa yanlış pozitif olur |
