# Anotasyon dosyaları — T227, T228, T229, T230'un kanıt tabanı

⛔⛔ **NEDEN BURADA.** Bu dosyalar oturum scratchpad'inde üretildi ve
defter kayıtları *«hazır dosyalar duruyor»* diyordu — oysa scratchpad
oturumla birlikte kaybolur. ➡️ *Bir kaydın kanıtı geçici bir dizindeyse,
kayıt kendi kanıtını kaybeder.* Depoya taşındılar.

## Ne var

| önek | tur | ne ölçüldü |
|---|---|---|
| `anot-*` | **T227** | `is_negative`'in iki tanımının ayrıştığı 26 kayıt + 15 kontrol · 3 anotatör |
| `oz-*` | **T228** | `ozerklik_vurgusu` üç tabaka örneklemi (70 öğe) · 3 anotatör |
| `cs-*` | **T229** | `C` tabakasının tam sayımı (323 kayıt, 4 parti) · 2 anotatör + hakem |
| `bs-*` | **T230** | `B` tabakasının tam sayımı (65 kayıt) · 2 anotatör + hakem |

Her turda: `*-talimat.md` anotatöre verilen görev · `*-girdi.json`
gösterilen öğeler (tabaka/grup bilgisi ÇIKARILMIŞ) · `*-anahtar.json`
öğe→kayıt eşlemesi ve tabaka · `*-A/B/X/Y*.json` anotatör çıktıları ·
`*-hakem.json` ayrışmalarda benim hükmüm · `*-karar.json` / `*-uzlasma.json`
sonuç.

## Nasıl yeniden kullanılır

⭐ Açık kalem: **dört turun dördünde de anotatörler Claude'du ve hakem
bendim.** Aynı `*-girdi.json` dosyaları bir uzmana ya da Claude dışı bir
model ailesine verilip uyum ölçülebilir; `*-karar.json` karşılaştırma
zeminidir. Talimatlar birebir duruyor, yeniden yazmak gerekmez.

⛔ `*-girdi.json` dosyalarında tabaka ve grup bilgisi YOKTUR ve
olmamalıdır — anotatörün hangi öğenin *«sorunlu»* olduğunu bilmemesi
tasarımın parçası.
