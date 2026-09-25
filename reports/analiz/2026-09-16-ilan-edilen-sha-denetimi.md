# Raporların ilan ettiği SHA256 tutuyor mu

**Betik:** `scripts/analiz/2026-09-16-ilan-edilen-sha-denetimi.py` · **Tarih:** 2026-09-16  
**Kapsam:** `reports/analiz/*.md` içindeki her ``dosya`` + `SHA256` çifti

---

## Neden

Bir rapor girdi ya da çıktı dosyasının SHA'sını yazıyorsa o SHA
**sağlanabilir** bir iddiadır — ve sağlanmadığı sürece raporun anlattığı
nesnenin, adını verdiği nesne olduğunun güvencesi yoktur.

⛔ İlk koşuda üç eval raporu tutmadı: rapor zincirin **birinci** adımının
öğelerini anlatıyor, mühürlenen dosya **ikinci** adımın çıktısıydı (K130).

## Sonuç

| | sayı |
|---|---:|
| ✅ tutuyor | **125** |
| ⛔ tutmuyor | **0** |
| ⚠️ adı geçen dosya yok | 0 |
| ⧉ repo DIŞI ilan (SHA kayıtlı, buradan doğrulanamaz) | 4 |
| **toplam ilan** | **125** |

## ⭐ Karar

| | |
|---|---|
| ✅ Durum | her ilan sağlandı |
| ➡️ Kapı | tutmayan varsa **çıkış kodu 1** — oturum sonu yordamına konabilir |
| ⚠️ Kapsam | yalnızca SHA yazılmış ilanlar sağlanır; SHA **yazmayan** bir rapor bu denetimden sessizce geçer |
