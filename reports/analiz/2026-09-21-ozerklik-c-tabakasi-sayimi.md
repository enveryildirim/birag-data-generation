# `ozerklik_vurgusu` — `C` tabakasının tam sayımı

**Betik:** `scripts/analiz/2026-09-21-ozerklik-c-tabakasi-sayimi.py` · **Tarih:** 2026-09-21  
**Kapsam:** `C` tabakasının **323** kaydının tamamı (T228'de 26'sı okunmuştu)  

| anotatör | kim | rol |
|---|---|---|
| `X` | Claude Opus 5 alt ajanı | tam okuma |
| `Y` | Claude Sonnet alt ajanı | tam okuma |
| `H` | ben (Claude Code, Opus 5) | yalnız ayrışmalarda hakem |

## 1. İki anotatör ne kadar uyuştu

| | |
|---|---:|
| kayıt | 323 |
| ham uyum | %94 |
| κ | 0.80 |
| ⛔ hakeme düşen | **18** |

⛔⛔ **Ayrışmalar RASTGELE DEĞİL, tek bir sınırda toplanıyor.** 15/18'inde `X` *«evet»*, `Y` *«hayır»* dedi — yani `X` (Opus) daha geniş okuyor. Hakemin uyguladığı ilke:

> KAÇINMAK ≠ DEVRETMEK. Bir hüküm ya da talimat vermekten kaçınmak özerklik vurgusu DEĞİLDİR; kararın (ya da söylenecek cümlenin) kullanıcıya ait olduğunu söylemek özerklik vurgusudur. 18 ayrışmanın TAMAMI bu sınırda — 15'inde X kaçınmayı da özerklik saydı, 3'ünde aynı hatayı Y yaptı. ⛔ Hakem bir tarafa yaslanmadı: X ile 8, Y ile 10 kayıtta aynı fikirde.

⇒ Hakem bir tarafa yaslanmadı: `X` ile 8/18, `Y` ile 10/18 kayıtta aynı fikirde.

## 2. ⭐⭐ Gizli tekrar testi

⛔ T228'de okunmuş 26 kayıt listeye karıştırıldı ve anotatörlere söylenmedi. Aynı soruya ikinci kez aynı cevap veriliyor mu?

| | |
|---|---:|
| tekrar edilen kayıt | 26 |
| ⭐ aynı hükme varılan | **26/26** (%100) |

➡️ *Test-tekrar güvenilirliği %100; T227 ve T228'in bütün sayıları bu ölçülmeden duruyordu.*

## 3. Tabakanın gerçek oranı — kestirim yerine SAYIM

| | |
|---|---:|
| `C` tabakası | 323 |
| ⭐ özerklik taşıyan | **51** (%16) |
| T228'in 26 kayıtlık kestirimi | %19, %95 aralık %9-%38 (27-122 kayıt) |
| ⇒ kestirim tuttu mu | ⭐ **evet**, sayım aralığın içinde |

## 4. Korpus

| | |
|---|---:|
| T228 sonrası beyan | 90/412 (%22) |
| ⭐ bu sayımla eklenen | **+46** |
| ⭐⭐ **yeni toplam** | **136/412 (%33)** |
| T228 kestirimi | ~140 (%34), aralık 92-207 |

## ⛔ Bu sayımın söylemedikleri

| | |
|---|---|
| ⛔⛔ **Ayrışmayan kayıtların İKİ oyu var, üç değil** | üçüncü tam okuma yapılmadı; gerekçesi T228'de ölçülen κ 0,85-0,97 ama bu bir gerekçe, kanıt değil |
| ⛔⛔ **Anotatörlerin ikisi de Claude, hakem de ben** | T227'den beri süren şerh: ortak yanlılık uyumu yukarı çeker |
| ⛔ **`A` ve `B` tabakaları yeniden okunmadı** | onların oranları T228'den geliyor (`A` sayımdı, `B` 20/65 örneklem) ⇒ korpus sayısının `B`'den gelen bileşeni hâlâ bir kestirim |
| ⚠️ **Karar kayda yazılmadı** | bu betik hiçbir kayda dokunmaz |
