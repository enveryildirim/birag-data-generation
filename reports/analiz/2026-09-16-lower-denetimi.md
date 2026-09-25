# Düz `str.lower()` denetimi — yasak artık sınanıyor

**Betik:** `scripts/analiz/2026-09-16-lower-denetimi.py` · **Tarih:** 2026-09-16  
**Kapsam:** `src/*.py` (her zaman) + `scripts/analiz/*.py` (**2026-09-16**'dan itibaren)  
**Dışlanan:** `src/tohum_guvenlik.py` — foldların **tanımlandığı** yer

---

## Neden

Bu oturumda ailenin **on bir** örneği sayıldı ve beşi kapı/dönüştürücünün
**içindeydi**. ⛔ İkisi *«bunu artık biliyorum»* dedikten **sonra**, yeni
yazılan denetim betiklerinde tekrarladı. ➡️ *Aynı gün üç kez aynı elden çıkan
bir hata ailesinde çözüm «dikkat etmek» değildir; yanlış varsayılan*
***erişilemez** kılınmalıdır.* Bu betik erişilebilirliği ölçer.

⭐ **Muafiyet var ve olmalı:** `.lower()` ASCII üzerinde (hash, İngilizce
anahtar, uzantı) **doğrudur**. Muaf satır `# lower-muaf: <gerekçe>` taşır ⇒
muafiyet **görünür**, sessizce geçmez.

---

## 1. Canlı kapsam

| | |
|---|---:|
| denetlenen dosya | **46** |
| ⛔ **borçlu satır** | **0** |
| ✅ muaf (gerekçeli) | 67 |

✅ **Borçlu satır yok.** Canlı kodda düz `.lower()`/`.upper()` yalnızca
gerekçeli muafiyetle kullanılıyor.

### ✅ DOSYA düzeyi muafiyetler — gerekçeleriyle

| dosya | gerekçe |
|---|---|
| `scripts/analiz/2026-09-16-alinti-nrm-sinamasi.py` | `alinti_nrm`'in eski/yeni hâllerini karşılaştırıyor (T80) |
| `scripts/analiz/2026-09-16-buyuk-harf-kapisi.py` | bütün işi ESKİ `.lower()` davranışını ölçmek — referans uygulama (T73) |
| `scripts/analiz/2026-09-16-ham-meta-hasari.py` | 2026-09-16 öncesi davranış referans olarak duruyor (T77) |
| `scripts/analiz/2026-09-16-kalan-lower-satirlari.py` | aynı: eski davranış referans olarak duruyor (T75) |
| `scripts/analiz/2026-09-16-lower-denetimi.py` | denetimin KENDİSİ — `.lower()` dizgesini arıyor ve rapor metninde alıntılıyor (yapısal dışlama, T64'ün sınıfı) |
| `scripts/analiz/2026-09-16-normalize-kanonlastirma.py` | eski `norm_egitim`/`norm_sure`/`_keyword` referans uygulamaları (T76) |

### ✅ SATIR düzeyi muafiyetler

| dosya | satır | kod |
|---|---:|---|
| `src/checks.py` | 215 | `KLINIK_IDDIA = re.compile(i_sinifi(KLINIK_IDDIA_KAYNAK), re.IGNORECASE)  # lower-muaf: i` |
| `src/filter.py` | 141 | `return bool(v) and v.upper() not in ("YOK", "YOK.")  # lower-muaf: "yok" i/ı taşımıyor` |
| `src/filter.py` | 153 | `s = (s or "").lower().replace("i̇", "i")  # lower-muaf: T80 — kapı REDDETMEK için, geniş` |
| `src/golden_eval.py` | 50 | `r"because|about|which|there|their|when|what|need|user|user's)\b", re.I)  # lower-muaf: İ` |
| `src/golden_eval.py` | 106 | `bulunan = {m.group(0).lower() for m in _ING.finditer(thinking or "")}  # lower-muaf: yal` |
| `src/normalize.py` | 49 | `s = s.strip().lower()  # lower-muaf: slug() ı->i eşlemesi yapıyor, ayrımı TASARIM GEREĞİ` |
| `src/smoke_checks.py` | 42 | `r"was|were|has|had|if|or|as|by|so|no|yes|its|about)\b", re.I)  # lower-muaf: İngilizce i` |
| `src/smoke_checks.py` | 44 | `r"kadar|sonra|önce|hem|ya|ki|de|da|o|şu|ne|her|en|çünkü|ancak)\b", re.I)  # lower-muaf: ` |
| `src/smoke_checks.py` | 312 | `r"yetkim yok\b|sınırımın dışında\b)", re.I)  # lower-muaf: re.I Türkçe İ/I'yı .lower()'d` |
| `scripts/analiz/2026-09-16-ilan-edilen-sha-denetimi.py` | 35 | `r"SHA256[^`\n]{0,12}`([0-9a-f]{16,64})", re.I)  # lower-muaf: onaltılık hash — ASCII` |
| `scripts/analiz/2026-09-16-katki-defteri-denetimi.py` | 135 | `durum_uyan = sum(1 for r in ROW if len(r) > 3 and r[3].strip("*` ").lower() in DURUMLAR)` |
| `scripts/analiz/2026-09-16-rapor-serh-denetimi.py` | 125 | `sira = (bool(re.search(r"\|\s*(sıra|rank|#)\s*\|", metin, re.I))  # lower-muaf: tablo ba` |
| `scripts/analiz/2026-09-16-rapor-serh-denetimi.py` | 126 | `or bool(re.search(r"sırala|en iyi kol|birinci kol", metin, re.I))  # lower-muaf: aynı` |
| `scripts/analiz/2026-09-16-rapor-yeniden-uretilebilirlik.py` | 94 | `hexler = {h[:16].lower() for h in re.findall(r"\b([0-9a-f]{16,64})\b", t)}  # lower-muaf` |
| `scripts/analiz/2026-09-16-tez-plani-turetme.py` | 138 | `len(ds) >= 3 and all("sha256" in y.read_text(encoding="utf-8").lower() for y in ds),  # ` |

---

## 2. ⚠️ Kesme öncesi — değiştirilmiyor

`scripts/analiz/` içinde **122** betik kesme tarihinden önce yazıldı
ve toplam **93** riskli satır taşıyor. ⛔ Bunlar **kusur sayılmaz**: kural o
gün yoktu ve raporları dondurulmuş (Kural 7). ⭐ *Bir kuralın geriye dönük
borcu, ileriye dönük yükümlülüğünden ayrı bir sayıdır ve ikisi karıştırılırsa
hiçbiri okunamaz.*

⚠️ **Ama bu, o betiklerin doğru olduğu anlamına GELMEZ.** Raporlarından sayı
alınırken bu şerh birlikte okunmalı — T51'in *«erken dönem kayıtları
denetlenemez»* sınıfı.

## ⛔ Bu denetimin söylemedikleri

| | |
|---|---|
| ⛔ **Muafiyet gerekçesi okunmuyor** | işaretin **varlığı** sınanıyor, içeriği değil. Yanlış bir gerekçe de geçer ⇒ insan okuması gerekli |
| ⛔ Docstring ayıklama **kaba** | üçlü tırnak sayımı; tek satırlık docstring ve tırnak içi tırnak yanlış sayılabilir. Bilerek kaba — amaç kesin ayrıştırma değil, kod satırında riskli çağrı aramak |
| ⛔ `sorted(key=str.lower)` gibi **dolaylı** kullanımlar | desen `.lower()` çağrısını arıyor; `str.lower` referansı görünmez |
| ⚠️ `re.IGNORECASE` **her zaman yanlış değil** | İngilizce kalıpta doğrudur; denetim onu da borç sayar ve muafiyet beklemesi **kasıtlıdır** — gerekçe yazılsın diye |

