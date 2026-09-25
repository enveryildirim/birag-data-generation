# BıRAG veri kümesi — v0.0.17

**Tarih:** 2026-09-22 · **Girdi:** `data/judged/v0.0.17.jsonl` SHA256-16 `9871150f24d30932`
**Çıktı:** `train.jsonl` SHA256-16 `5999c15910dbacb3`
**Kayıt:** **1089** / 1107 (elenen 18)

---

## 1. v0.0.16'dan farkı: METİN DEĞİŞMEDİ, `gen_meta.date` düzeldi

⛔ **Kayıt kümesi v0.0.16 ile BİREBİR AYNI** — fark 0. Hiçbir kaydın metni,
yargısı, dilimi ya da elenme durumu değişmedi.

Değişen tek şey **178 kaydın künye tarihi** (kümeye giren 170'i). Tarih 48
üretim betiğinde **elle yazılıydı** ve bir partiden ötekine **kopyalanıyordu**;
artık `src/kunye.py::betik_tarihi` ile betiğin **adından** türetiliyor
(K126'nın künyeye uygulanışı).

| tarih | v0.0.16 | **v0.0.17** | ne oldu |
|---|---:|---:|---|
| 2026-09-20 | 290 | **234** | `v6-parti5`'in 56 kaydı 09-21'e taşındı |
| 2026-09-21 | 228 | **170** | parti5'ten 56 aldı, parti8'in 114'ünü verdi |
| 2026-09-22 | 0 | **114** | `v6-parti8` gerçek üretim gününe geldi |

⭐⭐ **Mekanizma ve dersi:** aynı `gen_meta` sözlüğünde `parti` alanı da sabit
yazılıydı, **aynı kopyalama kusurunu** üretti, yakalandı ve türetilir yapıldı.
`date` **yanı başındaki satırdaydı** ve düzeltilmedi. ➡️ *Bir kusuru bir
alanda onarmak, aynı kusuru taşıyan komşu alanı görünür kılmıyor.*

⛔ Denetim `checks.py`'ye **kapı olarak konulamadı**: bir kaydın hangi
betikten geldiği kayıtta yazmıyor, bağ yalnız blok dosyası adından
kuruluyor ⇒ boru hattı düzeyinde bir denetim (`kunye-tarihi-denetimi.py`,
kalıcı). ⚠️ Betik adı da bir **beyandır**, yalnız daha dayanıklı bir beyan;
gerçek üretim anını git zaman damgası ölçer ve denetim onu kullanmıyor.
📎 `reports/analiz/2026-09-22-kunye-tarihi-denetimi.md`

---

## 2. Bileşim ve `slice` (v0.0.16'dan devralındı)

`slice` beyan edilmiyor, **türetiliyor** (`src/dilim.py`; `dilim_ok` kapısı
ayrışmayı eler).

| dilim | kayıt |
|---|---:|
| `terapotik_tek_tur` | 457 |
| `terapotik_cok_tur` | 376 |
| `rag_tek_tur` | 193 |
| `rag_cok_tur` | 45 |
| `replay` | 18 |

⭐ Sınama: `rag_*` toplamı **238** = bağlam belgesi olan kayıt sayısı.

| | |
|---|---:|
| çok turlu (2+ kullanıcı turu) | 421 |
| ergen / yetişkin | 98 / 991 |
| alkol · tütün · kumar · reçeteli ilaç · dijital · yok | 291 · 285 · 234 · 181 · 80 · 18 |

---

## 3. ⛔⛔ JUDGE KARIŞIKTIR

| judge | kayıt |
|---|---:|
| `claude-sonnet-subagent` | 921 |
| `agy:gemini-3.8-flash-high` | 150 |
| `replay` (yargı dışı, §9) | 18 |

⛔⛔ **K97: iki judge'ın puanları AYNI TABLOYA KONMAZ.** Köprü 42 eşli kayıtla
ölçüldü ve **sapma tek yönlü değil**: `yorumlama` +0,38 · `kesif` +0,19
(Claude cömert) ↔ `anlasilirlik` −0,86 · `grounding` −0,29 (Claude sert);
`duygusal_tepki` ve `dogallik` **gürültünün içinde, okunamıyor**.
📎 `reports/analiz/2026-09-22-v6-kalan-judge.md`

---

## 4. Eleme

`judge_safety_violation` **14** · `guvenlik_karantinasi` **4** (biri
`gd-033` — veremeyeceğimiz gizlilik güvencesi, kullanıcı kararıyla elendi;
⚠️ modelin mahremiyet sınırı hâlâ **yazılı değil**, brifing §8.4 s.2-3 açık).

⛔ Elenen 18 kayıt **silinmedi** (Kural 7).

---

## 5. ⛔ Bu kümenin bilinen kusurları

| | |
|---|---|
| ⛔⛔ **Uydurma %12 ve kümenin İÇİNDE** | 412 yeni yargının 51'inde `grounding`=2; `grounding` bir eleme kapısı değildir |
| ⛔⛔ **Ve bu bir ALT SINIR** | `grounding` tek-ayrıntı sondasıdır (T238): judge'ın adlandırdığı TEK ayrıntı dayanaklıysa puan 5 olur, aynı cevaptaki başka uydurma görünmez |
| ⛔⛔ **Oynaklığın sebebi BİLİNMİYOR** | uydurma oranı partiler arasında %1,7–%18,6 salınıyor (G=20,5, p<0,0001) ve **ölçebildiğimiz hiçbir şey açıklamıyor**: on tasarım değişkeninin en iyisi %14 alıyor, blok düzeyinde öbeklenme yok (p=0,35), parti düzeyi değişkenleri sabit. 📎 T243 |
| ⭐ **«Hızlanma bozdu» iddiası KURULAMADI** | `v6-parti8` (hızlandırılmış) en yüksek orana sahip ama doğru birim **parti**'dir ve 6 parti içinde 1. olmanın olasılığı 1/6 = 0,167. 📎 T242 |
| ⛔ **`thinking` ↔ `content` denetlenmiyor** | T239: iç muhakeme de bir beyandır ve kaydın içinde durur |
| ⚠️ **Kayıt düzeyinde puan bir ÇEKİLİŞTİR** | T175/K213 ⇒ yalnız küme okunur |
| ⚠️ **Üretici ile judge'ın çoğu aynı aileden** | K45: +6/+11 öz-şişirme; körlük azaltır, sıfırlamaz |

---

## 6. Üretim ve denetim

Tamamı `uretim-v5` ile üretildi. Kapılar **tek sürümden** koştu: `_checks`
atılıp 1107 kaydın tamamında bugünkü `run_checks` yeniden çalıştırıldı —
**1107/1107 geçti**, eskiden geçip düşen **yok**.

📎 `reports/analiz/2026-09-22-v0.0.17-girdi.md`
