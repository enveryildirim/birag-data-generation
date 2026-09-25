# Register etkisi sıfır — ama sebebi soruyu değiştiriyor

**Betik:** `scripts/analiz/2026-09-16-tohum-alani-tuketimi.py` · **Tarih:** 2026-09-16  
**Girdi:** `src/schemas.py` SHA256 `62c0d0664d2e1987`  
**Girdi:** `data/seeds.v2.jsonl` SHA256 `3399f543c8b882c7`  
**Girdi:** `data/seeds.jsonl` SHA256 `0631c02ec7510af3`  
**Girdi:** `data/plan/*.jsonl` · `prompts/uretim-v*.md` · `src/*.py` · `scripts/analiz/*.py` · `configs/*.yaml`

---

## Soru

T77 şunu açık bırakmıştı: kaybedilen **80** `ilkokul` etiketi üretilen metnin
**register**'ine ne yaptı? (T25 · K42 ekseni)

---

## 1. Önce maruziyet — 80 tohumun kaçı üretime girdi

| | |
|---|---:|
| `egitim=ilkokul` tohum (v2) | **80** |
| üretim planlarına giren tohum (toplam) | **144** |
| ⭐ bunlardan `ilkokul` olanı | **5** |

| plan | sıra | `register` | `bicim` | tohum `profil` |
|---|---:|---|---|---|
| `v3-parti2-baglam.jsonl` | 8 | `None` | `None` | `mavi_yakali` |
| `v4-parti1.jsonl` | 9 | `duzgun` | `orta` | `mavi_yakali` |
| `v4-parti1.jsonl` | 20 | `duzgun` | `kisa` | `emekli_yasli` |
| `v4-parti1.jsonl` | 26 | `duzgun` | `orta` | `emekli_yasli` |
| `v4-parti1.jsonl` | 36 | `duzgun` | `uzun` | `emekli_yasli` |

⚠️ **4/4** kotalı kayıt `duzgun` register aldı. ⛔ **Bu bir desen DEĞİL:** v4'ün `bozuk` kotası ~%25 ve n=4; hepsinin `duzgun` çıkma olasılığı ≈ **%32** — yani tamamen olağan. ➡️ *Küçük bir sayıda desen aramak, ölçüm değil beklenti okumaktır.*

---

## 2. ⭐⭐ Asıl cevap: `egitim` üretim hattına **hiç ulaşmıyor**

| Aşama | `egitim` var mı |
|---|---|
| örneklem planı satırı (`data/plan/*.jsonl`) — **değer eşleşmesiyle** | ⛔ **YOK** (hiçbir plan anahtarı taşımıyor) |
| üretim talimatı (`prompts/uretim-v*.md`) | `uretim-v4.md` |
| ⭐ **boru hattı** kodu (`src/`, `configs/`) | ⛔ **okuyan YOK** |
| yalnızca **denetim** betikleri | `scripts/analiz/2026-09-16-ham-meta-hasari.py`, `scripts/analiz/2026-09-16-normalize-kanonlastirma.py` ⚠️ *hepsi bugünkü ölçümler* |

⇒ **Register etkisi: yapısal olarak SIFIR.** `register` bağımsız bir
**kota** alanı (`prompts/uretim-v4.md` §3a) ve eğitim düzeyinden
**türetilmiyor**.

⛔ Bu bir rahatlama değil, **daha kötü bir soru**: `egitim` `SeedMeta`'da,
`configs/taxonomy.yaml`'da (6 kanonik değer) ve 2240 tohumun hepsinde duruyor
— ve **hiçbir tüketicisi yok**. ➡️ *Kaybının ölçülememesi kusurun*
*küçüklüğünden değil, alanın HİÇ KULLANILMAMASINDAN geliyor.*

⚠️ İlk arama `egitim`i `scripts/analiz/2026-09-15-f4-kapsam-raporu.py`'de
buldu — ama oradaki `egitim_ozeti()` bir **eğitim KOŞUSU** özeti (val loss,
tepe bellek), eğitim **düzeyi** tüketicisi değil. ⛔ Dizgeye dayalı ölçümün
ilk cevabı yanlıştı ve elle okunmadan düzelmezdi.

---

## 3. ⭐⭐ Soru genelleşti — ve ÖLÇMENİN KENDİSİ sorun çıkardı

`SeedMeta` **16** alan ilan ediyor. *«Bu alan tüketiliyor mu»*
sorusu mekanik olarak **iki** yoldan sorulabilir ve ⛔ **ikisi de yanlış**:

| yöntem | kaçırdığı | uydurduğu |
|---|---|---|
| **ad eşleşmesi** (`"alan"` ara) | ⛔ plan alanları **yeniden adlandırıyor** (`bagimlilik_turu` → `tur`): yanlış negatif | `egitim` için `egitim_ozeti()`'ni yakaladı — o bir **eğitim KOŞUSU** özeti |
| **değer eşleşmesi** (`seed_id` ile bağla) | ⛔ **sözcük dağarcığı** değişince kaçırıyor: `plan.motivasyon`=`ic` ↔ `tohum.motivasyon`=`ic_motivasyon` | ⛔ rastlantı: `risk_seviyesi` ↔ `bicim` **9/40** çünkü ikisinde de `orta` var |

➡️⭐⭐ *«Bu alan kullanılıyor mu» sorusunun MEKANİK bir cevabı yok. Ad*
*eşleşmesi yeniden adlandırmayı, değer eşleşmesi yeniden sözcüklendirmeyi*
*göremez; ve değer eşleşmesi eşiksiz kullanıldığında ortak bir değer*
*(`orta`) iki ilgisiz alanı akraba gösterir.* ⇒ Üçüncü sütun **elle okundu**
(Kural 6) ve raporda **kaynağıyla** yazılıyor.

| alan | ad eşleşmesi | değer eşleşmesi | ⭐ **elle okuma** | |
|---|---|---|---|---|
| `bagimlilik_turu` | — | `tur` 144/144 | ✅ v4-parti1-plan | ✅ |
| `bagimlilik_alt_turu` | — | — | ⛔ **okuyan yok** | ⛔ |
| `senaryo` | ✅ | `tohum_senaryo` 136/136 | ✅ v3-ornekleme · v4-parti1-plan · uzman-ornekleme | ✅ |
| `stres_tipi` | — | `sinir_tipi` 10/40 | ⛔ **okuyan yok** | ⛔ |
| `profil` | — | — | ⛔ **okuyan yok** | ⛔ |
| `yas_grubu` | — | `yas` 124/144 | ✅ v3-ornekleme · v4-parti1-plan | ✅ |
| `evre` | — | — | ⛔ **okuyan yok** | ⛔ |
| `motivasyon_evresi` | — | — | ⛔ **okuyan yok** | ⛔ |
| `motivasyon` | — | `motivasyon` 2/40 | ⛔ **okuyan yok** | ⛔ |
| `risk_seviyesi` | ✅ | `bicim` 9/40 | ✅ v3-ornekleme · uzman-ornekleme | ✅ |
| `siddet_seviyesi` | — | `bicim` 10/40 | ⛔ **okuyan yok** | ⛔ |
| `egitim` | ✅ | — | ⛔ **okuyan yok** | ⛔ |
| `kullanim_suresi` | — | — | ⛔ **okuyan yok** | ⛔ |
| `onceki_tedavi` | — | `sinir_tipi` 22/40 | ⛔ **okuyan yok** | ⛔ |
| `cinsiyet` | — | — | ⛔ **okuyan yok** | ⛔ |
| `notlar` | ✅ | — | ✅ tohum_guvenlik.py (`notlar.esdurumlar` — K76) | ✅ |

⛔ **11/16 alanı boru hattında hiçbir şey okumuyor:** `bagimlilik_alt_turu`, `stres_tipi`, `profil`, `evre`, `motivasyon_evresi`, `motivasyon`, `siddet_seviyesi`, `egitim`, `kullanim_suresi`, `onceki_tedavi`, `cinsiyet`.

⛔⭐ **Ve tabloda bir tuzak var:** örneklem planında `motivasyon` adında bir
anahtar **var** ama tohumunkiyle **aynı şey değil** — planınki `ic`/`aile_baskisi`
sözcük dağarcığını, tohumunki `ic_motivasyon`/`tetikleyici_olay`'ı kullanıyor ve
plan betikleri tohumun alanını **hiç okumuyor**. ➡️ *Aynı adı taşıyan iki alan,*
*aynı alan olduğunun kanıtı değildir; ad eşleşmesi burada «tüketiliyor» derdi.*

⚠️ **Bu «gereksiz» demek DEĞİL:** bir alan bugün okunmuyor olabilir ve tezde
betimleyici istatistik olarak, ya da ileride tabakalı örneklemede
kullanılabilir. ⭐ Ama **kayıt disiplini açısından fark var**: okunmayan bir
alanın **yanlış olduğu hiçbir yerde ortaya çıkmaz**. T76'nın `egitim` kusuru
80 tohumda durdu ve onu gösteren şey üretim değil, **ayrı bir**
**denetim** oldu.

➡️⭐⭐ *Bir alanın doğruluğu, onu okuyan bir tüketici varsa **kendiliğinden***
*sınanır; okuyanı yoksa yalnızca ona bakan bir denetimle sınanır — ve o*
*denetim yazılmamışsa alan sessizce yanlıştır. ⇒ «Şemada duruyor» bir*
*doğruluk güvencesi değil, bir BAKIM BORCUDUR.*

---

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔ **Üretilen metinde register ÖLÇÜLMEDİ** | gerek kalmadı: `egitim` üretim hattına ulaşmıyor (§2). ⚠️ Ulaşsaydı bile maruziyet **5 kayıt**tı ve o sayıda register farkı ölçülemezdi |
| ⛔ **Tüketim taraması dizgeye dayalı** | alan adı `"alan"` biçiminde aranıyor; bir alanı **başka adla** okuyan kod (ör. `meta.get(k)` döngüsü) görünmez. ⚠️ İlk arama `egitim_ozeti`'ni yanlış yakaladı ve **elle okunmadan** düzelmedi |
| ⛔ *«Tüketilmiyor»* ≠ *«gereksiz»* | betimleyici istatistik ve ileride tabakalı örneklem meşru kullanımlar; ölçülen şey **bugünkü** tüketim |
| ⚠️ `data/plan` yalnızca **144** tohum kullanıyor | 2240'ın %6,4'ü; alanların çoğu için maruziyet zaten düşük |
| ⛔ `notlar` alt alanları | `notlar` bir sözlük ve içindeki anahtarlar (`esdurumlar` vb.) ayrıca taranmadı — `esdurumlar` `tohum_guvenlik.py`'de **tüketiliyor** (K76) ve bu tabloda görünmüyor |

