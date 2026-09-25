# BıRAG veri kümesi — v0.0.18

**Tarih:** 2026-09-22 · **Girdi:** `data/judged/v0.0.18.jsonl` SHA256-16 `9871150f24d30932`
**Çıktı:** `train.jsonl` SHA256-16 `07bbeca3b41097c1`
**Kayıt:** **1033** / 1107 (elenen 74)

⭐ **Bu, fiilen İNCE AYAR EDİLEN sürümdür** — 8 tohumla eğitildi ve ölçüldü
(§6). `v0.0.15`–`v0.0.17` ara sürümlerdir.

---

## 1. v0.0.17'den farkı: uydurma kapısı

⛔ Hiç kayıt eklenmedi. Tek değişiklik: `grounding == 2` olan kayıtlar
**eğitime alınmıyor** (kullanıcı kararı, 2026-09-22).

| | |
|---|---:|
| v0.0.17 | 1089 |
| − `judge_uydurma` | **56** |
| ⭐ **v0.0.18** | **1033** |
| kalan `grounding`=2 | **0** |

`grounding == 2` = judge'ın adlandırdığı somut ayrıntı konuşmada **yok** ve
hipotez olarak da işaretlenmemiş ⇒ cevap, kullanıcının söylemediği bir şeyi
söylemiş gibi sunuyor. Böyle bir kaydı eğitmek modele uydurmayı öğretir.

⛔ Toplam 58 kayıt bu bayrağı taşıyordu; 2'si zaten başka kapılardan
düşmüştü. Elenenler **silinmedi** (Kural 7).

### ⛔⛔ Kapının üç şerhi — hepsi ölçülmüş

| | |
|---|---|
| ⛔⛔ **ALT SINIRDIR** | `grounding` **tek-ayrıntı sondasıdır** (T238): judge'ın adlandırdığı TEK ayrıntı dayanaklıysa 5 verir ve aynı cevaptaki başka bir uydurmayı **görmez** ⇒ kapı yakaladığını eler, korpusu uydurmadan **arındırmaz** |
| ⛔⛔ **Duyarlılık judge'a göre değişiyor** | Claude 921 yargıda 54, Gemini 150 yargıda 4 ateşledi (%5,6 ↔ %2,7) ⇒ Gemini ile puanlanmış kayıtlar **daha az süzüldü**. Kapı korpusa **judge-bağımlı bir asimetri** sokuyor: judge dağılımı 921/150 → **869/146** |
| ⚠️ **`replay` muaf** | `judge` alanı yok, §9'un yazılı muafiyetinden geçiyor |

---

## 2. Bileşim

| dilim | kayıt |
|---|---:|
| `terapotik_tek_tur` | 426 |
| `terapotik_cok_tur` | 361 |
| `rag_tek_tur` | 184 |
| `rag_cok_tur` | 44 |
| `replay` | 18 |

⭐ `slice` **türetiliyor** (`src/dilim.py`, `dilim_ok` kapısı): `rag_*`
toplamı **228** = bağlam belgesi olan kayıt sayısı.

| | |
|---|---:|
| bağlam belgeli | 228 |
| çok turlu (2+ kullanıcı turu) | ~421'den süzülmüş |
| ergen / yetişkin | 92 / 941 |
| alkol · tütün · kumar · reçeteli ilaç · dijital · yok | 280 · 266 · 218 · 173 · 78 · 18 |

**Hacim:** 4288 mesaj · ~198 bin sözcük konuşma · ~72,5 bin sözcük iç muhakeme.

---

## 3. ⛔⛔ Judge karışıktır

| judge | kayıt |
|---|---:|
| `claude-sonnet-subagent` | 869 |
| `agy:gemini-3.8-flash-high` | 146 |
| `replay` (yargı dışı, §9) | 18 |

⛔⛔ **K97: iki judge'ın puanları aynı tabloya konmaz.** Köprü 42 eşli kayıtla
ölçüldü, **sapma tek yönlü değil**: `yorumlama` +0,38 · `kesif` +0,19 (Claude
cömert) ↔ `anlasilirlik` −0,86 · `grounding` −0,29 (Claude sert);
`duygusal_tepki` ve `dogallik` **gürültünün içinde, okunamıyor**.
📎 `reports/analiz/2026-09-22-v6-kalan-judge.md`

---

## 4. Eleme

`judge_uydurma` **56** · `judge_safety_violation` **14** ·
`guvenlik_karantinasi` **4**.

Karantinadakilerden biri **`gd-033`**: cevap sistemin veremeyeceği bir
gizlilik güvencesi veriyordu ve kaydın **kendi iç muhakemesi bunu yapmadığını
ilan ediyordu** (T239). Kullanıcı kararıyla elendi. ⚠️ Modelin mahremiyet
sınırı hâlâ **yazılı değil** (`docs/uzman-brifingi.md` §8.4, s.2-3 açık).

---

## 5. ⛔ Bilinen kusurlar

| | |
|---|---|
| ⛔⛔ **Uydurma temizlenmedi, yakalananlar elendi** | T238: sonda tek ayrıntı bakıyor ⇒ kümede **yakalanmamış uydurma var**, sayısı bilinmiyor |
| ⛔⛔ **Uydurma oranının kaynağı BİLİNMİYOR** | partiler arası %1,7–%18,6 salınıyor (G=20,5, p<0,0001) ve **ölçebildiğimiz hiçbir şey açıklamıyor**: on tasarım değişkeninin en iyisi %14 alıyor, blok düzeyinde öbeklenme yok (p=0,35), parti düzeyi değişkenleri sabit. 📎 T243 |
| ⛔ **Judge asimetrisi kümeye geçti** | §1'deki üçüncü şerh |
| ⛔ **`thinking` ↔ `content` denetlenmiyor** | T239 |
| ⚠️ **Kayıt düzeyinde puan bir ÇEKİLİŞ** | T175/K213 ⇒ yalnız küme okunur |
| ⚠️ **Üretici ile judge'ın çoğu aynı aileden** | K45: +6/+11; körlük azaltır, sıfırlamaz |

---

## 6. ⭐ Bu kümeyle yapılan ince ayar ve ölçüm

**Kol:** `d1-veri2x-k8qo-v018`, **8 tohum** (7·13·23·31·37·41·43·47).
Kapsam: 8 katman · q+o · rank 8 · scale 20 · LR 1e-5 · 826 eğitim / 207
doğrulama · 2478 adım (3 epoch). Karşılaştırma kolu `z-h9-k8qo-v014`
(571 kayıt) ile **kapsam birebir aynı** ⇒ değişen tek şey veri.

`safety_crisis`, kriz ögelerinde dereceli puan (tavan 30):

| | ham | boş cevap | ort. uzunluk | dolu cevapta öge başına |
|---|---:|---:|---:|---:|
| taban (ince ayarsız) | **21,0** | 0/15 | 59 sözcük | **1,40** / 2 |
| `z-h9` (571) | 6,38 | 3,2 | 31 | 0,56 |
| **`d1` (1033)** | **5,12** | 3,6 | 20 | 0,43 |

⛔⛔ **Korpusu 571'den 1033'e çıkarmak bu eksende ölçülebilir kazanç
VERMEDİ**: fark −1,25, hata payı ±3,28 ⇒ **okunamaz** (T246). Üç tohumda
−4,67 görünen fark sekiz tohumda −1,25'e düştü; görünen etkinin **%73'ü
gürültüymüş**.

⛔⛔⛔ **Ve sebebi ölçüm gücü değil, YAPISAL:** bu eksen kriz yönlendirmesini
ölçüyor, korpusta **`is_crisis` kaydı 0** — kriz dilimi uzman onayına kadar
bekletiliyor (Kural 3). ⇒ Korpusa kriz içermeyen kayıt eklendiği sürece bu
ölçüt kıpırdamaz. 📎 **T247**

⚠️ Unutma ekseninde gerileme yok (taban 28/30 · `z-h9` 27,6 · `d1` 26,8) ⇒
model genel yeteneğini kaybetmiyor, **bu davranışı** kaybediyor (T132/T248).

📎 `reports/analiz/2026-09-22-veri-iki-kati.md` ·
`reports/analiz/2026-09-22-olcut-korpus-uyumsuzlugu.md`

---

## 7. Üretim ve denetim

Tamamı `uretim-v5` ile üretildi. Kapılar **tek sürümden** koştu: `_checks`
atılıp 1107 kaydın tamamında bugünkü `run_checks` yeniden çalıştırıldı —
**1107/1107 geçti**, eskiden geçip düşen **yok**.

📎 `reports/analiz/2026-09-22-v0.0.18-girdi.md`
