# BıRAG veri kümesi — v0.1.1

**Tarih:** 2026-09-29 · **Taban:** `datasets/v0.1.0/train.jsonl` SHA256-16 `6fcb6b1e16290575`  
**Çıktı:** `train.jsonl` SHA256-16 **`f8fcaa1e96603cb2`** (ön kayıttaki hazırlık SHA'sıyla aynı — betik denetler)  
**Kayıt:** **1058** — kayıt kümesi ve sırası `v0.1.0` ile **birebir** (K277: yeni kayıt yok, silme yok)  
**Durum:** ⭐ araştırma sürümü, **ana hat DEĞİL** — ana hat olup olmayacağına ön kayıt karar verir (K277 · EK-1) · ⛔ kriz dilimi hariç (`v0.1.0` gibi)

## 1. Ne değişti

| | kayıt |
|---|---:|
| düşünmesi yeniden kurulan (`uretim-v6`, kararlar korunarak) | **1036** |
| cevabının **son cümlesi** değişen | **9** |
| `v0.1.0` hâliyle kalan (3 red + §1e örneği) | 4 |
| replay (düşünmesi yok, dokunulmadı) | 18 |

⛔ **Dokunulmayanlar:** kullanıcı turları, bağlam, önceki turlar, cevabın gövdesi, klinik kararlar, üstveri.

| veri düzeyi | `v0.1.0` | `v0.1.1` |
|---|---:|---:|
| son tur soruyla biten | %50,3 | %49,4 |
| düşünmede «sormuyorum» | %30,6 | %3,1 |
| düşünmede ⛔ ya da ⭐ | %22,8 | %0,2 |
| düşünme ortanca sözcük | 72 | 112 |

Kaynak: `reports/analiz/2026-09-29-v011-derleme.md` · süreç: `reports/analiz/2026-09-24-v011-faz2.md`

## 2. Güvenceler

- Her yeniden kurma: zarf · temizlik · `run_checks` · karar eşlemesi · bağımsız karar korunumu okuması (1143 okuma `karar-korunumu.v1`, 4 okuma `v2`) · bitişi değişende eski↔yeni aynı judge.
- Ön kayıt: `configs/deney/2026-09-29-v011-on-kayit.json` (`3bad7d71a1c8af6a`) + EK-1 kazanç şartı (`b1806d442a8683ff`).

## 3. ⛔ Bilinen kusurlar ve açık maddeler

| | |
|---|---|
| ⛔⛔ **Jeton uzunluğu doğrulanmadı** | ön kaydın adım 2'si: hiçbir kayıt `max_seq_length` 2048'i aşmamalı. Bu makinede tokenizer yok; en uzun kayıt 3359 karakter (~1100 jeton **tahmini**). **Eğitimden önce eğitim ortamında gerçek tokenizer ile denetlenmeli** — sessiz kırpma kıyası bozar |
| ⛔ **`v0.1.0` kusurları taşınıyor** | `data/candidates/v011-v010-kusurlari.jsonl` — 47 madde (cevap katmanı, `iyi_giden_paylasim` etiketi 9 kayıtta yanlış, biri güvenlikle ilgili: 0802) |
| ⚠️ **Düşünme %56 uzadı** | gecikme KPI'ı (K46) etkilenir |
| ⚠️ **İki rubrik sürümü** | korunum okumalarının 4'ü `karar-korunumu.v2` ile (T302-T304) |
| ⚠️ **Yazarlık** | 1039 yeniden kurmanın 206 taslağı Claude Code'a ait; hepsinin okuma ve revizyonu Claude Code (K260) |
| 👤 **İnsan okuması** | pilotun 40 kaydı henüz insan tarafından okunmadı (K277'nin ikinci güvence katmanı) |
