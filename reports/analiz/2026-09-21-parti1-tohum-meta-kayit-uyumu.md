# `v6-parti1`: tohumun meta eksenleri kaydı tarif ediyor mu?

**Betik:** `scripts/analiz/2026-09-21-parti1-tohum-meta-kayit-uyumu.py` · **Tarih:** 2026-09-21  
**Girdi:** `data/candidates/v6-parti1.jsonl` SHA256-16 `4eb76ca33d43bfb9` · **59** kayıt  
**Ölçek:** `U` uyumlu · `Ç` çelişiyor · `S` sessiz — 59 kayıt × 6 eksen = **354** hüküm, hepsi elle (K30)

⛔⛔ T219 parti1'in başka bir rejimde yazıldığını ölçmüştü (kaydın kendi tohumuyla örtüşmesi %6). Bu rapor, o rejimin **kapsama ölçümüne** ne yaptığını ölçüyor.

## 0. ⭐⭐⭐ Sonuç

| | | |
|---|---:|---:|
| ⭐ **uyumlu** | 192 | %54 |
| ⚠️ **sessiz** | 150 | %42 |
| ⛔ **çelişiyor** | **12** | **%3** |

## 1. Eksen eksen

| eksen | uyumlu | sessiz | ⛔ çelişiyor | kayıttan doğrulanabilen |
|---|---:|---:|---:|---:|
| `bagimlilik_turu` | 40 | 18 | **1** | %69 |
| `yas_grubu` | 34 | 25 | **0** | %58 |
| `profil` | 15 | 43 | **1** | %27 |
| `senaryo` | 28 | 31 | **0** | %47 |
| `evre` | 28 | 26 | **5** | %56 |
| `stres_tipi` | 47 | 7 | **5** | %88 |

⛔⛔ **Ölçülmeyen eksenler:** `risk_seviyesi`, `siddet_seviyesi`, `motivasyon_evresi` — üçü de bir DERECE ve kısa bir konuşmadan derece okumak eşiği benim koymam demek olurdu (`gd-024`). Ölçülmediler.

## 2. ⛔ Çelişen etiketler — gerekçeleriyle

| # | eksen | gerekçe |
|---:|---|---|
| 2 | `bagimlilik_turu` | `kumar`; metinde bahis yok, *«iş için sürekli ekrandayım»* — öne çıkan `dijital` |
| 2 | `profil` | `kronik_issiz`; metin *«iş için»* diyor, yani çalışıyor |
| 9 | `evre` | `sosyal_kullanim`; metin *«tek başıma uğruyorum»* ve artan sıklık diyor — öne çıkan `tolerans` |
| 17 | `stres_tipi` | `kronik_agri`; metinde ağrı yok, eş kaybı var (`yas_kayip`) |
| 19 | `stres_tipi` | `yok`; metin *«belim için»* diyor — `kronik_agri` öne çıkıyor |
| 20 | `stres_tipi` | `yok`; metin *«annemin yası»* diyor — `yas_kayip` öne çıkıyor |
| 22 | `evre` | `birakma_cabasi`; metin kullanımı savunuyor — `inkar` öne çıkıyor |
| 33 | `stres_tipi` | `kronik_agri`; metinde ağrı yok, kızının gelememesi ve yalnızlık var |
| 38 | `evre` | `tolerans`; metin temiz test ve seans anlatıyor — `birakma_cabasi` |
| 39 | `evre` | `nuksetme`; metin kullanımı savunuyor — `inkar` öne çıkıyor |
| 41 | `evre` | `birakma_cabasi`; metin *«benimki de zaten bir iki kadeh»* diye gerekçe kuruyor — `inkar` |
| 49 | `stres_tipi` | `yalnizlik`; metinde eşle süren bir çatışma var (`aile_catismasi`) |

## 3. Satır satır hüküm

| # | `bagimlilik_t` | `yas_grubu` | `profil` | `senaryo` | `evre` | `stres_tipi` |
|---:|---|---|---|---|---|---|
| 1 | U | S | S | S | S | U |
| 2 | Ç | U | Ç | S | S | U |
| 3 | S | U | U | S | U | U |
| 4 | S | S | S | U | S | U |
| 5 | U | U | S | U | U | S |
| 6 | U | U | S | S | U | U |
| 7 | U | S | S | S | S | U |
| 8 | S | U | S | S | U | U |
| 9 | S | S | S | S | Ç | U |
| 10 | U | S | S | S | U | U |
| 11 | U | U | S | U | U | U |
| 12 | S | U | U | U | U | U |
| 13 | U | U | S | S | S | U |
| 14 | U | S | S | S | U | U |
| 15 | U | S | S | U | S | U |
| 16 | S | U | U | U | S | U |
| 17 | U | U | U | U | S | Ç |
| 18 | S | S | S | S | S | U |
| 19 | U | U | U | U | U | Ç |
| 20 | U | U | S | U | U | Ç |
| 21 | U | U | S | S | S | U |
| 22 | U | U | S | U | Ç | U |
| 23 | U | S | S | S | U | U |
| 24 | U | S | U | S | U | U |
| 25 | S | S | S | S | S | U |
| 26 | U | U | S | U | U | U |
| 27 | S | U | S | S | U | U |
| 28 | U | S | S | U | U | S |
| 30 | U | U | S | S | U | U |
| 31 | U | S | S | S | S | U |
| 32 | S | S | S | S | S | U |
| 33 | U | U | U | U | U | Ç |
| 34 | U | U | S | S | S | U |
| 35 | S | U | S | U | S | U |
| 36 | U | U | S | S | U | U |
| 37 | S | U | U | S | S | U |
| 38 | S | U | S | S | Ç | U |
| 39 | U | U | S | U | Ç | U |
| 40 | U | U | S | U | S | U |
| 41 | U | S | S | U | Ç | U |
| 42 | U | U | U | U | U | S |
| 43 | U | S | S | S | U | S |
| 44 | U | U | S | S | S | U |
| 45 | U | U | U | U | S | U |
| 46 | S | S | S | S | S | U |
| 47 | U | U | S | S | U | U |
| 48 | U | S | S | U | U | U |
| 49 | U | S | U | U | U | Ç |
| 50 | U | U | S | S | U | U |
| 51 | U | S | S | U | S | U |
| 52 | U | S | U | U | U | S |
| 53 | S | U | S | U | S | U |
| 54 | U | S | S | U | U | S |
| 55 | S | U | U | U | S | U |
| 56 | S | S | S | S | S | U |
| 57 | S | S | S | S | U | U |
| 58 | U | S | S | U | S | S |
| 59 | U | U | U | S | S | U |
| 60 | U | U | U | U | U | U |

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔⛔ **Hüküm BENİM okumam** (K30) | bağımsız bir okuyucu farklı ayırabilir; ikinci anotatör yok ve uyum oranı ölçülmedi |
| ⛔⛔ **`S` bir aklanma değil** | kapsama envanteri açısından `Ç` ile `S` aynı kapıya çıkar: ikisinde de sayılan şey kaydın kendisi değildir. Kayıttan doğrulanabilen oran yalnızca %58 |
| ⛔ **Karşılaştırma yok** | aynı ölçüm `v6-parti3-6` için yapılmadı; oradaki oranın daha yüksek olduğu BEKLENİYOR ama ölçülmedi ⇒ bu sayılar tek başına *«parti1 kötü»* demiyor, *«parti1 ölçülemiyor»* diyor |
| ⛔⛔ **Düzeltme yapılmadı** | ne etiketler değişti ne kayıtlar; `datasets/` dokunulmadı |
| ⚠️ **Etiketin kaynağı tohum, kaydın kaynağı ızgara** | ızgaranın kendi alanları (`tur`, `yas`) kayıtla tutarlı çünkü kayda plandan yazılıyorlar; ölçülen şey tohumun META'sı |
