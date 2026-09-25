# BıRAG veri kümesi — v0.1.0

**Tarih:** 2026-09-24 · **Girdi:** `data/judged/v0.0.22.jsonl` SHA256-16 `fc1c117d3be48982`  
**Çıktı:** `train.jsonl` SHA256-16 `6fcb6b1e16290575`  
**Kayıt:** **1058** / 1132 (elenen 74)  
**Durum:** ⭐ **ilk dondurulmuş araştırma sürümü** (K275) · ⛔ **kriz dilimi HARİÇ** · ürün sürümü DEĞİL

⭐ **İçerik `v0.0.22` ile birebir aynıdır** — aynı girdiden yeniden derlendi, `train.jsonl` SHA'sı ve elenen liste eşit (betik denetler). `v0.0.18`'e göre +25 kayıt (`celiskili` sınıfı), düşen 0.

---

## 1. Neden şimdi dondu

| gerekçe | kanıt |
|---|---|
| **Hacim hedefi karşılandı** | `plan.md:280-288`: *v0.1.0 ~800-1.200*; bu sürüm 1058 |
| **Veri eklemek ölçülebilir kazanç vermiyor** | 571 → 1033: okunamaz (T246) · 1033 → 1058: 11 karşılaştırmanın 11'i okunamaz (T277) |
| **Kalan açıklar üretimle kapanmıyor** | kriz dilimi (uzman + etik kurul) · ikinci uzman + κ · bağımsız judge · K42 onayı · 12B — hepsi insan kararı |

⛔ Plan v0.1.0'da **her dilimin temsil edilmesini** istiyor (`plan.md:286`); bu sürüm bunu **karşılamıyor** — §2. Kriz verisi uydurulmadı (Kural 3); açık kartta yazılı bırakıldı ve `v0.2.0`'ın konusu.

## 2. Kapsam — plan hedefine karşı

| plan dilimi | hedef | bu sürüm (%) |
|---|---:|---|
| Terapötik, tek tur | %35 | 426 (40.3) |
| Çok turlu diyalog | %15 | 361 (34.1) terapötik + 44 RAG |
| Kriz + rol sınırı | %10 | kriz **0** · `rol_siniri` 191 (18.1) |
| Direnç / inkâr / discord | %5 | `inkar` 47 (4.4) · `discord` 12 |
| Nazikçe karşı çıkma | %5 | 159 (15.0) |
| RAG — context sadakati | %10 | 253 (23.9) |
| Kapsam dışı / sınır | %5 | ⚠️ ayrı alanla türetilemiyor |
| Replay (genel amaçlı) | %15 | **18** (1.7) |

⛔⛔ **İki yapısal açık:**

- **Kriz: 0 kayıt.** Uzman onayına kadar bekletiliyor (Kural 3). `safety_crisis` ekseni bu yüzden korpusa **kör** (T259) — §5'teki kriz gerilemesinin sebebi.
- **Replay: 18 kayıt (%1.7, hedef %15).** Unutma savunması zayıf; %5 alan dışı sinyalin unutmayı tabana döndürdüğü deney kolunda ölçüldü (T253/T257) ama ana hatta alınmadı.

⚠️ Tek/çok tur, RAG ve nazikçe karşı çıkma hedefin **üstünde**; bu bir kusur değil, hacim hedefin %10'unda olduğu için oranlar dengesiz.

### Kullanıcı mesajı biçimi (K42) — ⚠️ kota yürütücü onayı almadı

| bant | hedef | bu sürüm |
|---|---:|---:|
| `kisa` | %40 | 377 (%35.6) |
| `orta` | %35 | 308 (%29.1) |
| `uzun` | %25 | 373 (%35.3) |

⛔ Kota **tutmuyor**. Kota onaylanmadığı için sürüm buna bekletilmedi; T261'e göre uzun girdi uydurmayı 6,4 kat bastırıyor ⇒ fazlalık bilinçli olarak düzeltilmedi.

### Diğer dağılımlar

| alan | dağılım |
|---|---|
| bağımlılık | alkol 285 · tutun 271 · kumar 224 · receteli_ilac 178 · dijital 82 · yok 18 |
| yaş | yetiskin 961 · ergen 97 |
| tur | single 654 · multi 404 |
| MI süreci | engaging 422 · evoking 260 · focusing 207 · planning 151 · yok 18 |

## 3. ⛔⛔ Judge karışımı (K97)

| judge | kayıt |
|---|---:|
| `claude-sonnet-subagent` | 894 |
| `agy:gemini-3.8-flash-high` | 146 |
| `replay` | 18 |

⛔ İki judge'ın puanları aynı tabloya konmaz; uydurma kapısı judge'a göre farklı sıklıkta ateşliyor (%5,6 ↔ %2,7 — `v0.0.18` kartı §1).

## 4. Eleme

| sebep | kayıt |
|---|---:|
| `judge_uydurma` | 56 |
| `judge_safety_violation` | 14 |
| `guvenlik_karantinasi` | 4 |

Elenenler silinmedi (Kural 7); girdi dosyasında duruyor.

## 5. ⭐ Bu içerikle yapılan ince ayar ve ölçüm

`e3` = bu içerik (`v0.0.22`), `d1` = `v0.0.18` — ikisi de **8 tohum**, kapsam birebir aynı (8 katman · q+o · r8). Taban adaptersiz **tek greedy koşu**. Değerler ort ± 2·SE.

| ölçü | tavan | taban | `d1` | **`e3`** | e3 − taban | okuma |
|---|---:|---:|---:|---:|---:|---|
| `safety_crisis` kriz yönlendirmesi, dereceli | 30 | **21** | 5.12 ± 2.63 | **6.88 ± 1.39** | -14.12 | ↓ |
| `safety_crisis` otomatik | 20 | **11** | 8.75 ± 1.45 | **9.25 ± 0.82** | -1.75 | ↓ |
| `forgetting_smoke` | 30 | **28** | 26.75 ± 0.73 | **27.50 ± 0.38** | -0.50 | ↓ |
| `context_fidelity` | 20 | **15** | 13.50 ± 1.46 | **14.38 ± 1.19** | -0.62 | okunamaz |
| `context_fidelity` çakışmasız 8 (B2) | 8 | **6** | 4.75 ± 0.82 | **5.38 ± 0.75** | -0.62 | okunamaz |
| `context_fidelity.real` | 15 | **7** | 8.75 ± 0.50 | **9.62 ± 1.06** | +2.62 | ↑ |
| `context_fidelity.ortusmez` (B1, `celiskili`) | 15 | **5** | 3.38 ± 0.75 | **2.50 ± 1.07** | -2.50 | ↓ |
| `sycophancy` | 24 | **20** | 21.25 ± 0.98 | **21.38 ± 0.53** | +1.38 | ↑ |

Okuma: taban deterministik tek koşu (hata payı yok) ⇒ |e3 − taban| > 2·SE_e3 ise ↑/↓. Tabanlar 2026-09-24'te bugünkü set ve denetleyiciyle yeniden koşuldu (T278).

⛔⛔ **Model hâlâ ürüne verilemez:** kriz yönlendirmesi tabandan belirgin kötü; bu içerikte kriz kaydı olmadığı için veri eklemek onu kıpırdatmıyor (§2).
⚠️ `e3` ↔ `d1` farklarının hiçbiri okunabilir değil (T277). B1'de iki kol da tabanın altında — ön kayıtsız gözlem, ayrı sınanacak.
⛔ Gecikme KPI'ı (< 2 sn) bu sürümde ölçülmedi; `v0.0.18`'de ortanca ~6-7 sn idi.
⚠️ Demo gözlemi (ölçülmedi): düşünme bölümü aynı cümleyi tekrarlayarak döngüye girebiliyor.

## 6. ⛔ Bilinen kusurlar

| | |
|---|---|
| ⛔⛔ **Uydurma temizlenmedi, yakalananlar elendi** | tek-ayrıntı sondası (T238); %12 bir alt sınır |
| ⛔⛔ **Uydurma oranının kaynağı bilinmiyor** | partiler arası %1,7–%18,6 (T243) |
| ⛔⛔ **Judge doğrulanmadı** | ikinci uzman + κ yok; judge AUC 0,45–0,57 |
| ⛔ **`celiskili` sınıfı elle onarılmış** | uydurma ve güvenlik atlaması bulunup onarıldı (T265 · T267 · T271); yazar = onaran = okuyan (K30) |
| ⛔ **`thinking` ↔ `content` denetlenmiyor** | T239 |
| ⚠️ **`takdir` kapanışı risk sinyalini atlayabilir** | 2/2 vaka, payda sayılmadı (T271) |
| ⚠️ **Üretici ile judge'ın çoğu aynı aileden** | K45 |

## 7. ⚠️ `v0.0.22` kartındaki bayat cümleler — orada düzeltilmedi (Kural 7)

| o kartta | doğrusu |
|---|---|
| *«`v0.0.21` fiilen ince ayar edilen sürümdü»* | ince ayar edilen ana hat `v0.0.18`'di; `v0.0.21` eğitilmedi |
| *«Kota tutturulamadı … %10.1»* | %10,1 ile §7a″ kotası **tuttu** (T272); cümle `v0.0.21` kartından sürüklenmiş |
| *«Bu sürüm ÖLÇÜLMEDİ»* | 8 tohumla eğitildi ve ölçüldü (K272 · T277) |

## ⛔ Bu kartın söylemedikleri

| | |
|---|---|
| ⛔ **Dondurulmuş ≠ bitmiş** | kriz, replay ve vahşi doğa dilimleri eksik; `v0.2.0` bunlar için |
| ⛔ **Test bölmesi yok** | test işini `evals/golden.{dev,test,locked}` görür; `locked` Faz 7'ye kadar açılmaz |
| ⛔ **Eksen 1 (judge'lı golden) bu içerikte koşulmadı** | yalnız otomatik kapı sayımları var |
