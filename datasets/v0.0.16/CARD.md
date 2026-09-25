# BıRAG veri kümesi — v0.0.16

**Tarih:** 2026-09-22 · **Girdi:** `data/judged/v0.0.16.jsonl` SHA256-16 `2f1f3d0a770df057`
**Çıktı:** `train.jsonl` SHA256-16 `3e05a51c43bdb284`
**Kayıt:** **1089** / 1107 (elenen 18)

---

## 1. v0.0.15'ten farkı: METİN DEĞİŞMEDİ, tek bir ALAN düzeldi

⛔ **Kayıt kümesi v0.0.15 ile BİREBİR AYNI** — 1089 kaydın 1089'u aynı, fark 0.
Hiçbir kaydın metni, yargısı ya da elenme durumu değişmedi.

Değişen tek şey **`slice` alanı**: artık beyan edilmiyor, **türetiliyor**
(`src/dilim.py`). Kip `context`'in doluluğundan, tur sayısı `messages`'taki
`user` turlarından, `replay` kaydın kendi bayrağından.

| | v0.0.15 (beyan) | **v0.0.16 (türetme)** |
|---|---:|---:|
| `terapotik_tek_tur` | 256 | **457** |
| `terapotik_cok_tur` | 188 | **376** |
| `rag_tek_tur` | 395 | **193** |
| `rag_cok_tur` | 24 | **45** |
| `cok_tur` (v6'ya özgü, kipsiz) | 208 | — |
| `replay` | 18 | 18 |
| ⭐ **RAG toplamı** | **419** | **238** |
| bağlam belgesi olan kayıt | 238 | 238 |

⭐⭐⭐ **Sınama:** türetilmiş `rag_*` toplamı (238) **bağlamı olan kayıt
sayısına eşittir**. v0.0.15'te alan 419 RAG kaydı iddia ediyordu; gerçek 238.
⇒ Alan artık kendisiyle çelişemez.

⛔ **Sebep (T240):** `slice`'ın ANLAMI v5 ile v6 arasında sessizce değişmişti —
v4/v5'te `rag_*` kayıtların %100'ünde bağlam vardı, v6'da `rag_tek_tur`
kayıtların yalnız %35'inde. Dört katman da kördü: şema `slice: str`
(`Literal` değil), `checks.py`'de denetim yok, birleştirme raporu saymıyor,
judge görmüyor.

⭐ **Türetme kuralı uydurulmadı, sınandı:** v4/v5'in 460 beyanının **459'unu**
birebir yeniden üretiyor. Tek uyuşmazlık `v4-parti1 / d001bc7a8f` ve o zaten
**K69**'un belgelenmiş kusuru (varsayılan, çok turlu bir kaydı tek tur diye
damgalamıştı) ⇒ türetme K69'u **aramadan buldu**.

⭐ **Ve artık kapı var:** `checks.py::run_checks` içinde `dilim_ok` — beyan
türetilenden ayrışırsa kayıt düşer. Üç bozuk değerle sınandı, üçünü de
reddetti. 📎 `reports/analiz/2026-09-22-slice-anlami-degisti.md` ·
`reports/analiz/2026-09-22-slice-yeniden-etiketle.md`

---

## 2. ⛔⛔ JUDGE KARIŞIKTIR — bu kümede tek bir puanlayıcı yoktur

| judge | kayıt |
|---|---:|
| `claude-sonnet-subagent` | 921 |
| `agy:gemini-3.8-flash-high` | 150 |
| `replay` (yargı dışı, §9 yazılı muafiyet) | 18 |

⛔⛔ **K97: iki judge'ın puanları AYNI TABLOYA KONMAZ.** Bu kümeden türetilen
hiçbir boyut ortalaması, judge'ı ayırmadan raporlanamaz.

⭐ Köprü `v6-parti3`'ün 42 kaydı üzerinde ölçüldü (iki judge'ın ikisinde de
var):

| boyut | Claude−Gemini | okunabilir mi |
|---|---:|---|
| `yorumlama` | +0.38 | evet — Claude cömert |
| `kesif` | +0.19 | evet — Claude cömert |
| `grounding` | −0.29 | evet — Claude sert |
| `anlasilirlik` | −0.86 | evet — Claude çok sert |
| `duygusal_tepki` | +0.05 | ⛔ hayır — gürültünün içinde |
| `dogallik` | −0.05 | ⛔ hayır — gürültünün içinde |

➡️ **Sapma tek yönlü değildir.** Ölçüt K98'indir: bir fark ancak judge'ın
**kendisiyle** farkından büyükse okunabilir; taban aynı dalgada 24 gizli
tekrar-test çiftiyle ölçüldü ve K98'in v6 tabanını neredeyse birebir
yineledi. 📎 `reports/analiz/2026-09-22-v6-kalan-judge.md`

---

## 3. Bileşim

| | |
|---|---:|
| kayıt | 1089 |
| bağlam belgeli | 238 |
| çok turlu (2+ kullanıcı turu) | 421 |
| ergen | 98 |
| yetişkin | 991 |

| bağımlılık türü | kayıt |
|---|---:|
| alkol | 291 |
| tütün | 285 |
| kumar | 234 |
| reçeteli ilaç | 181 |
| dijital | 80 |
| yok (replay) | 18 |

---

## 4. Eleme

| sebep | kayıt |
|---|---:|
| `judge_safety_violation` | 14 |
| `guvenlik_karantinasi` | 4 |

⛔ Elenen 18 kayıt **silinmedi** (Kural 7); `data/judged/v0.0.16.jsonl` ve
`data/guvenlik-karantinasi.jsonl` içinde duruyorlar.

⭐ Karantinadakilerden biri **`gd-033`**: cevap sistemin veremeyeceği bir
gizlilik güvencesi veriyordu (*«Burada söylediklerinin dışarı çıkmayacağını
bilmen önemli»*) ve kaydın kendi iç muhakemesi bunu yapmadığını ilan
ediyordu (T239). Kullanıcı kararıyla **elendi**. ⚠️ `docs/uzman-brifingi.md`
§8.4'ün 2. ve 3. soruları AÇIK: modelin mahremiyet konusunda ne
diyebileceği hâlâ **yazılı bir sınır değil**.

---

## 5. ⛔ Bu kümenin bilinen kusurları

| | |
|---|---|
| ⛔⛔ **Uydurma oranı ölçüldü ve düşük değil** | 412 yeni yargının **51'inde** (%12) `grounding`=2: cevap, konuşmada geçmeyen bir ayrıntıyı geçmiş gibi sunuyor. Bu kayıtlar **kümededir** — `grounding` bir eleme kapısı değildir, yalnız `klinik_guvenlik_ihlali` eler |
| ⛔⛔ **`grounding` tek-ayrıntı sondasıdır (T238)** | judge'ın adlandırdığı TEK ayrıntı dayanaklıysa puan 5 olur; aynı cevaptaki başka bir uydurma **görünmez**. ⇒ %12 bir **alt sınırdır** |
| ⛔ **`v6-parti8`'de oran daha yüksek** | 22/118 (%19) — parti8 hızlandırılmış üretildi (K260/K261). ⚠️ Ama partiler aynı tohum dağılımıyla üretilmedi (T233) ⇒ **bu karşılaştırma kurulmamıştır** |
| ⛔ **`thinking` ↔ `content` tutarlılığı denetlenmiyor** | T239: iç muhakeme de bir beyandır ve kaydın içinde durur, ama hiçbir kapı onu cevaba karşı okumuyor |
| ⚠️ **Kayıt düzeyinde puan bir ÇEKİLİŞTİR** | T175/K213: aynı kayda aynı judge iki kez sorulduğunda yarısında başka puan geliyor ⇒ yalnız küme okunur |
| ⚠️ **Üretici ile judge'ın çoğu aynı aileden** | K45 öz-şişirmeyi ölçtü (+6/+11); körlük azaltır, sıfırlamaz |
| ⚠️ **RAG tanımı bir SEÇİMDİR** | *«bağlamı olan kayıt RAG'dir»* denildi; bağlamı olup cevabı onu kullanmayan kayıt da RAG sayılır. *«Cevap bağlamı KULLANIYOR mu»* tanımı ölçülmedi |

---

## 6. Üretim ve denetim

Tamamı `uretim-v5` ile üretildi. Kapılar **tek sürümden** koştu: `_checks`
atılıp 1107 kaydın tamamında bugünkü `run_checks` yeniden çalıştırıldı —
**1107/1107 geçti**, eskiden geçip şimdi düşen kayıt **yok**.

📎 `reports/analiz/2026-09-22-v0.0.16-girdi.md`
