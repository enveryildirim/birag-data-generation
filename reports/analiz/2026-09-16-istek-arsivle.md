# Judge iş dosyaları arşivi — `ham-judge` neyi saklamıyordu

**Betik:** `scripts/analiz/2026-09-16-istek-arsivle.py` · **Tarih:** 2026-09-16  
**Kaynak:** oturum scratchpad'i `judge-isleri/<aile>/istek/` (⛔ Kural 8 oturum sonunda siler)  
**Çıktı:** `reports/analiz/ham-judge/istek/<aile>.jsonl.gz`

---

## Neden

`ham-judge/*.jsonl` judge'ın **ne döndüğünü** saklıyor; **ne okuduğunu**
saklamıyor. İki kusur vakasında (K123 `korpus-v9-p2`, K124 `korpus-v8`)
*«judge yanlış okudu»* ile *«sonuç yanlış dosyaya yazıldı»* ayrımını yapan
tek kanıt `istek/NNN.txt` oldu. O dosyalar repoda değildi.

## Arşivlenen — 31 aile · 994 iş dosyası

| Aile | dosya | ham | gzip | ortak önek (K103) | ham sonuç arşivde |
|---|---:|---:|---:|---:|:--:|
| `doz-yama-v7` | 26 | 551 KB | 29 KB | 18719 krk | ✅ |
| `doz-yama-v7b` | 26 | 550 KB | 29 KB | 18719 krk | ✅ |
| `e2-220c3b5a` | 14 | 288 KB | 15 KB | 18719 krk | ✅ |
| `e2-5ae67873` | 20 | 418 KB | 21 KB | 18719 krk | ✅ |
| `e2-7ac7e984` | 20 | 415 KB | 20 KB | 18719 krk | ✅ |
| `e2-99b69ab4` | 20 | 415 KB | 20 KB | 18719 krk | ✅ |
| `e2-b7584bec` | 20 | 419 KB | 22 KB | 18719 krk | ✅ |
| `e2-ceef5655` | 20 | 416 KB | 21 KB | 18719 krk | ✅ |
| `e2-hakem-p2` | 54 | 1127 KB | 44 KB | 18719 krk | ✅ |
| `e2-hakem-p3` | 54 | 1127 KB | 44 KB | 18719 krk | ✅ |
| `korpus-v8` | 104 | 2876 KB | 94 KB | 24970 krk | ✅ |
| `korpus-v9` | 104 | 3115 KB | 96 KB | 27100 krk | ✅ |
| `korpus-v9-p2` | 24 | 720 KB | 32 KB | 27100 krk | ✅ |
| `korpus-v9-p3` | 24 | 720 KB | 32 KB | 27100 krk | ✅ |
| `v4-parti1-v7` | 40 | 838 KB | 37 KB | 18719 krk | ✅ |
| `v8-e2-220c3b5a` | 14 | 380 KB | 18 KB | 24970 krk | ✅ |
| `v8-e2-5ae67873` | 20 | 549 KB | 25 KB | 24970 krk | ✅ |
| `v8-e2-7ac7e984` | 20 | 546 KB | 23 KB | 24970 krk | ✅ |
| `v8-e2-99b69ab4` | 20 | 547 KB | 23 KB | 24970 krk | ✅ |
| `v8-e2-b7584bec` | 20 | 551 KB | 25 KB | 24970 krk | ✅ |
| `v8-e2-ceef5655` | 20 | 548 KB | 24 KB | 24970 krk | ✅ |
| `v8-hakem-p2` | 52 | 1427 KB | 47 KB | 24970 krk | ✅ |
| `v8-hakem-p3` | 52 | 1427 KB | 47 KB | 24970 krk | ✅ |
| `v9-e2-220c3b5a` | 14 | 413 KB | 19 KB | 27100 krk | ✅ |
| `v9-e2-5ae67873` | 20 | 595 KB | 26 KB | 27100 krk | ✅ |
| `v9-e2-7ac7e984` | 20 | 593 KB | 25 KB | 27100 krk | ✅ |
| `v9-e2-99b69ab4` | 20 | 593 KB | 25 KB | 27100 krk | ✅ |
| `v9-e2-b7584bec` | 20 | 597 KB | 35 KB | 27100 krk | ✅ |
| `v9-e2-ceef5655` | 20 | 594 KB | 25 KB | 27100 krk | ✅ |
| `v9-hakem-p2` | 46 | 1369 KB | 53 KB | 27100 krk | ✅ |
| `v9-hakem-p3` | 46 | 1369 KB | 53 KB | 27100 krk | ✅ |
| **TOPLAM** | **994** | **25.5 MB** | **1.02 MB** | | |

➡️ Sıkıştırma **25×** — iş dosyalarının
büyük kısmı ailede ortak olan rubrik öneki (K103: kuyruklar bayt-aynı).

## ⛔ Kurtarılamayan — ham sonucu var, iş dosyası yok

**11 aile:** `expert70-v7-sonnet` · `golden-baseline-claude` · `golden-baseline-sonnet` · `golden-v7-sonnet` · `korpus-v3-claude` · `korpus-v7-kontrol` · `korpus-v7-sonnet` · `korpus-v7-ucuncu` · `locked-baseline-1` · `locked-baseline-1-p2` · `locked-baseline-1-p3`

Bu ailelerde bir sonuç-kayıt kayması bulunursa **judge kusuru mu yazma
kusuru mu** olduğu gösterilemez. Ham sonuç arşivde olduğu için
`eslesme_denetimi()` yine koşar — ama ayrımı yapamaz.

## ⭐ Karar

| | |
|---|---|
| ✅ Arşivlendi | 31 aile · 994 iş dosyası · 1.02 MB |
| ⛔ Geri alınamaz | 11 aile — iş dosyaları oturumla birlikte gitti |
| ➡️ Kural 8 | judge iş dizini artık **silinmeden önce arşivlenir**; bu betik oturum sonu yordamının parçası |
