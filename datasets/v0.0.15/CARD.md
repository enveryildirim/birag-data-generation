# BıRAG veri kümesi — v0.0.15

**Tarih:** 2026-09-22 · **Girdi:** `data/judged/v0.0.15.jsonl` SHA256-16 `a2122934bacfbc0e`
**Çıktı:** `train.jsonl` SHA256-16 `64d64b8feaf04270`
**Kayıt:** **1089** / 1107 (elenen 18)

---

## 1. v0.0.14'ten farkı: korpus neredeyse İKİYE KATLANDI

571 → **1089**. Eklenen 530 kayıt `v6-parti1`–`parti8`; bunların **370'i bu
sürüm için yargılandı** (yedi partidir yargılanmamış duruyorlardı).

| | |
|---|---:|
| v0.0.14'ten gelen | 577 |
| yeni `v6` kaydı | 530 |
| ⭐ girdi | **1107** |
| elenen — `judge_safety_violation` | 14 |
| elenen — `guvenlik_karantinasi` | 4 |
| ⭐ **tutulan** | **1089** |

⛔ Elenen 18 kayıt **silinmedi**; `data/judged/v0.0.15.jsonl` ve
`data/guvenlik-karantinasi.jsonl` içinde duruyorlar (Kural 7).

---

## 2. ⛔⛔ JUDGE KARIŞIKTIR — bu kümede tek bir puanlayıcı yoktur

| judge | kayıt |
|---|---:|
| `claude-sonnet-subagent` | 921 |
| `agy:gemini-3.8-flash-high` | 150 |
| `replay` (yargı dışı, §9 yazılı muafiyet) | 18 |

⛔⛔ **K97: iki judge'ın puanları AYNI TABLOYA KONMAZ.** Bu kümeden türetilen
hiçbir boyut ortalaması, judge'ı ayırmadan raporlanamaz.

⭐ **Aralarındaki köprü bu sürümde ilk kez AYNI KAYITLAR üzerinde ölçüldü**
(`v6-parti3`'ün 42 kaydı iki judge'ın ikisinde de var):

| boyut | Claude−Gemini | okunabilir mi |
|---|---:|---|
| `yorumlama` | +0.38 | evet — Claude cömert |
| `kesif` | +0.19 | evet — Claude cömert |
| `grounding` | −0.29 | evet — Claude sert |
| `anlasilirlik` | −0.86 | evet — Claude çok sert |
| `duygusal_tepki` | +0.05 | ⛔ hayır — gürültünün içinde |
| `dogallik` | −0.05 | ⛔ hayır — gürültünün içinde |

➡️ **Sapma tek yönlü değildir.** «Claude cömert davranır» tek cümlesi bu
kümede yanlıştır. Ölçüt K98'indir: bir fark ancak judge'ın **kendisiyle**
farkından büyükse okunabilir; taban aynı dalgada 24 gizli tekrar-test
çiftiyle ölçüldü. 📎 `reports/analiz/2026-09-22-v6-kalan-judge.md`

---

## 3. Bileşim

| | |
|---|---:|
| kayıt | 1089 |
| **bağlam belgeli** | **238** |
| çok turlu (2+ kullanıcı turu) | 421 |
| ergen | 98 |
| yetişkin | 991 |

⛔⛔ **«Bağlam belgeli» sayısı `slice` alanından TÜRETİLMEDİ, `context`
alanının doluluğundan sayıldı.** Sebep **T240**: `slice`'ın anlamı v5 ile v6
arasında sessizce değişti — v5'te `rag_*` kayıtların %100'ünde bağlam vardı,
v6'da `rag_tek_tur` kayıtların yalnız %35'inde var. Bu kartta `slice`
dağılımı **bilerek yazılmamıştır**; yazılsaydı RAG payı iki katından fazla
şişerdi. 📎 `reports/analiz/2026-09-22-slice-anlami-degisti.md`

| bağımlılık türü | kayıt |
|---|---:|
| alkol | 291 |
| tütün | 285 |
| kumar | 234 |
| reçeteli ilaç | 181 |
| dijital | 80 |
| yok (replay) | 18 |

---

## 4. ⛔ Bu kümenin bilinen kusurları

| | |
|---|---|
| ⛔⛔ **Uydurma oranı ölçüldü ve düşük değil** | 412 yeni yargının **51'inde** (%12) `grounding`=2: cevap, konuşmada geçmeyen bir ayrıntıyı geçmiş gibi sunuyor. Bu kayıtlar **kümededir** — `grounding` bir eleme kapısı değildir, yalnız `klinik_guvenlik_ihlali` eler |
| ⛔⛔ **`grounding` tek-ayrıntı sondasıdır (T238)** | judge'ın adlandırdığı TEK ayrıntı dayanaklıysa puan 5 olur; aynı cevaptaki başka bir uydurma **görünmez**. ⇒ %12 bir **alt sınırdır** |
| ⛔ **`v6-parti8`'de oran daha yüksek** | 22/118 (%19) — parti8 hızlandırılmış üretildi (K260/K261). ⚠️ Ama partiler aynı tohum dağılımıyla üretilmedi (T233) ⇒ **bu karşılaştırma kurulmamıştır** |
| ⛔ **`thinking` ↔ `content` tutarlılığı denetlenmiyor** | T239: bir kaydın iç muhakemesi, cevabın yaptığı şeyi yapmadığını ilan ediyordu. O kayıt karantinaya alındı (`gd-033`), ama **denetim yok** ⇒ benzerleri kümede olabilir |
| ⚠️ **Kayıt düzeyinde puan bir ÇEKİLİŞTİR** | T175/K213: aynı kayda aynı judge iki kez sorulduğunda yarısında başka puan geliyor ⇒ tek kaydın puanına bakılıp karar verilemez, yalnız küme okunur |
| ⚠️ **Üretici ile judge'ın çoğu aynı aileden** | K45 öz-şişirmeyi ölçtü (+6/+11); körlük azaltır, sıfırlamaz |

---

## 5. Üretim ve denetim

Tamamı `uretim-v5` ile üretildi. Kapılar **tek sürümden** koştu: `_checks`
atılıp 1107 kaydın tamamında bugünkü `run_checks` yeniden çalıştırıldı —
**1107/1107 geçti**, eskiden geçip şimdi düşen kayıt **yok**.

📎 `reports/analiz/2026-09-22-v0015-girdi.md`
