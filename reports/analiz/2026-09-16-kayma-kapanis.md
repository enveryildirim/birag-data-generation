# Kayma denetimi kapanışı — hiç denetlenmemiş koşular + tespit gücü

*2026-09-16 · betik `scripts/analiz/2026-09-16-kayma-kapanis.py`*
*girdi: `data/judged/*.jsonl` · `reports/analiz/ham-judge/*.jsonl` — **yeni koşu / yeni judge / yeni üretim YOK**, tamamen geriye dönük*

## İki açık kalem, iki soru

2026-09-15 taraması `korpus-v8`'de bir takas buldu ve iki kalem açık bıraktı:

1. ⛔ **Tarama eksikti.** Yalnızca `reports/analiz/ham-judge/` denetlendi; ama o
   arşiv **sonradan** doğdu (K117) ve ondan önceki judge koşularının tek kaydı
   **veri kümesi dosyalarının kendisi** (`data/judged/`). Oradaki koşular hiç
   denetlenmemişti — ve asıl önemli olan onlar: eğitim verisi oradan seçiliyor.
2. ⛔ **Kusurun oranı bilinmiyordu.** Ama orandan önce şu sorulmalı: *bir kayma
   olsaydı görür müydüm?* Denetim bir kaymayı ancak alıntılar **ayırt ediciyse**
   görebiliyor.

⭐ `data/judged` kendi kendine yeter: her kayıt hem `messages` (kaynak) hem
`judge` (alıntılar) taşıyor, yani havuz dosyanın **içinde**.

## 1. Hiç denetlenmemiş koşular — `data/judged`

| Dosya | rubrik | kayıt | ⛔ alıntısız | **kayma** |
|---|---|---:|---:|---:|
| `doz-yama.v7.jsonl` | v7 | 26 | — | 0 |
| `expert-70.jsonl` | v1 | 70 | 70 | 0 |
| `expert-70.v2.jsonl` | v2 | 68 | 2 | 0 |
| `expert-70.v3.jsonl` | v3 | 68 | 1 | 0 |
| `expert-70.v4.jsonl` | v4 | 68 | 1 | 0 |
| `expert-70.v7.jsonl` | v7 | 70 | — | 0 |
| `v0.0.1-gemini.jsonl` | v1 | 20 | 20 | 0 |
| `v0.0.1.jsonl` | v1 | 20 | 20 | 0 |
| `v0.0.2.jsonl` | v7 | 104 | — | 0 |
| `v0.0.3.jsonl` | v7 | 144 | — | 0 |
| `v0.0.4.jsonl` | v7 | 137 | — | 0 |
| `v0.0.5.jsonl` | v7 | 137 | — | 0 |
| `v3-kumulatif.v6.jsonl` | v6 | 104 | — | 0 |
| `v3-kumulatif.v7-kontrol.jsonl` | v7 | 104 | 1 | 0 |
| `v3-kumulatif.v7-ucuncu.jsonl` | v7 | 104 | 2 | 0 |
| `v3-kumulatif.v7.jsonl` | v7 | 104 | — | 0 |
| `v3-parti1.jsonl` | v4 | 40 | 4 | 0 |
| `v3-parti2-tam.jsonl` | v4 | 40 | 3 | 0 |
| `v3-parti3.jsonl` | v4 | 24 | 1 | 0 |
| `v4-parti1.v7.jsonl` | v7 | 40 | — | 0 |
| **TOPLAM** | | **1492** | **125** | **0** |

✅ **1492 kayıtta kayma 0.** v1'den v7'ye altı rubrik sürümü, aralarında
`v0.0.2`–`v0.0.5`, `v3-parti1/2/3`, `expert-70.v2/v3/v4` ve
`v3-kumulatif.v6` — **hiçbiri daha önce bu denetimden geçmemişti.**
➡️ Bilinen takas `korpus-v8`'de kaldı; veri kümesi dosyalarına bulaşmamış.

## 2. Tespit gücü — bir kayma olsaydı görür müydüm

Her kümede **bütün takas çiftleri** tek tek hesaplandı: kaydın sonucu ötekinin
dosyasına yazılsaydı `eslesme_denetimi()` ateşler miydi? Karar kuralı kapının
kendi kuralından türetildi (skor = alıntının o cevapta bulunması; kapı,
yazıldığı dosyanın skoru **en yüksek skordan küçükse** ateşler). Bir takasta
**iki yön** vardır ve birinin ateşlemesi yeter.

| Küme | çift | ⛔ görülmeyen | **güç** |
|---|---:|---:|---:|
| `ham-judge` (31 arşiv, v3-v8) | 44989 | **8** | %99.98 |
| `data/judged` (21 dosya, v1-v7) | 70693 | **2806** | %96.03 |
| **TOPLAM** | **115682** | **2814** | **%97.57** |

### ⭐⭐ Güç rubriğin kendisine bağlı

Fark kümelerden değil **rubrik sürümünden** geliyor:

| rubrik | kayıt | ⛔ alıntısız | çift | görülmeyen | **güç** |
|---|---:|---:|---:|---:|---:|
| `v1` | 110 | 110 | 2795 | **2795** | %0.0 |
| `v2` | 68 | 2 | 2278 | **1** | %100.0 |
| `v3` | 172 | 1 | 7634 | **0** | %100.0 |
| `v4` | 172 | 9 | 4114 | **9** | %99.8 |
| `v6` | 200 | 5 | 7612 | **4** | %99.9 |
| `v7` | 1858 | 11 | 82200 | **4** | %100.0 |
| `v8` | 322 | 1 | 9049 | **1** | %100.0 |

⛔ **`v1` rubriğinde güç SIFIR.** O sürüm judge'dan hiç alıntı istemiyordu:
110 kaydın **tamamında** (110/110) tek bir uzun alıntı bile yok. Alıntı yoksa kaymanın
imzası da yok.

➡️ ⭐ *Kanıtı zorunlu kılan bir rubrik yalnızca judge'ı disipline etmiyor;
**ölçüm hattını geriye dönük denetlenebilir kılıyor.** Alıntı istemeyen bir
rubrikle puanlanmış kayıtlarda sonuç-kayıt kaymasını gösterecek hiçbir iz
yoktur ve o koşular bugün de, gelecekte de denetlenemez.* ⚠️ Bu, kanıta bağlı
rubriğin (v7→v9 hattı) ölçülmemiş bir **yan faydası**.

### Orana ne diyor

Gözlenen iki olay da **v8/v9 döneminde ve `ham-judge` kümesinde** oldu; o
kümede güç **%99.98**.
➡️ *O dönemde iki olay oldu ve ikisi de bulundu; görülmemiş bir üçüncünün
beklentisi ihmal edilebilir.*

⛔ **Ama bu, oranın ölçüldüğü anlamına gelmez** — üç sebeple:

1. **Erken dönem denetlenemez.** `v1`-`v4` rubrikleriyle puanlanmış kayıtlarda
   güç düşük ya da sıfır; oradaki *«kayma 0»* sonucu **kanıt değil, sessizlik**.
2. **Bağımsız parti sayımı yok.** Güç bir olayın *görülme* olasılığı; *olma*
   olasılığı için partileri bağımsız sayabileceğimiz bir düzenek gerekir.
   ⚠️ İki olay da aynı oturumda, aynı iş kurucusuyla çıktı.
3. **Takas dışındaki bozulmalar hesabın dışında** — sonucun hiç yazılmaması,
   aynı kayda iki kez yazılması, içeriğin kısmen karışması.

## ⛔ Yapısal kör nokta — hiç uzun alıntısı olmayan kayıtlar

Bir kaydın tek bir uzun alıntısı bile yoksa **o yön hiç ateşleyemez**;
kayma ancak karşı yönden görülebilir.

⭐ Görünmez 2814 çiftin **1'i** iki
tarafı da alıntılı; geri kalanın sebebi **alıntısızlık**. ➡️ Açık rubrikte
değil **kısa/boş cevaplarda** — ve alıntı isteyen bir rubrikle kapanıyor.

| küme | alıntısız kayıt |
|---|---:|
| `expert-70.jsonl` | 70/70 |
| `v0.0.1-gemini.jsonl` | 20/20 |
| `v0.0.1.jsonl` | 20/20 |
| `v3-parti1.jsonl` | 4/40 |
| `golden-baseline-sonnet` | 3/48 |
| `v3-parti2-tam.jsonl` | 3/40 |
| `korpus-v7-ucuncu` | 2/104 |
| `golden-baseline-claude` | 2/48 |
| `golden-v7-sonnet` | 2/48 |
| `expert-70.v2.jsonl` | 2/68 |
| `v3-kumulatif.v7-ucuncu.jsonl` | 2/104 |
| `e2-220c3b5a` | 1/14 |

## ⭐ Karar

| | |
|---|---|
| ✅ Tarama tamamlandı | ham arşiv **+** `data/judged`; toplam **2902** judge kararı denetlendi |
| ✅ Güç ölçüldü | yürürlükteki rubriklerde (`v6`-`v8`) **%99.99** — denetim **doygun**. Bütün sürümler birlikte %97.57; farkı `v1` açıyor |
| ⛔ Bilinen tek kusur | `korpus-v8` 075↔077 (bildirimle düzeltildi, etkisi yok) |
| ⚠️ Kimlik damgası | ⛔ **koşullu geri çekiliyor**: v7+ rubriklerinde güç zaten ~1, ek alan kazanç getirmez. ⚠️ Koşul: *rubrik alıntı istemeye devam ettiği sürece*. Alıntı zorunluluğu kalkarsa güç `v1`'deki gibi çöker ve damga **tek** denetim yolu olur |

➡️ *Kapının gücü sabit bir özellik değil, rubriğe bağlı bir ölçüdür.* Bu yüzden
güç hesabı rubrik değiştiğinde yeniden koşulmalı — betik bunu tek komutla yapar.

⚠️ **Erken dönem için hiçbir şey yapılamaz.** `v1`-`v4` ile puanlanmış kayıtlar
bugün de denetlenemez; oradaki *«kayma 0»* sonucu kanıt değil **sessizliktir**
ve bir sayı raporlanırken bu ayrım korunmalı (Kural 5).
