# Korpus koşusu — v9'un iki mekanizması İLK KEZ uyarılabildi

*2026-09-15 · betik `scripts/analiz/2026-09-15-korpus-v9-raporu.py`*
*korpus `data/candidates/v3-kumulatif.jsonl` SHA256 `5867e31fc49e3dbf` · 104 kayıt*
*rubrik v9 SHA256 `4b78260a96d78311` · judge **claude-sonnet-subagent** (v7/v8 ile aynı aile)*
*tasarım `reports/analiz/2026-09-15-korpus-v9-tasarim.md` — Ö1-Ö7 koşudan önce*

## Küme

| | |
|---|---|
| kayıt | 104 |
| v7 | arşivli, **üç geçiş** (K106) |
| v8 | bu koşuda, k=1 — **korpusta ilk kez** |
| v9 | bu koşuda, k=1 + 24 kayıtta k=3 |
| kuyruk | v8 ↔ v9 baytı baytına aynı; render v7 commit'iyle **kod olarak** özdeş |
| doğrulama | **104/104** kayıtta kaynaklı |

⛔ **v8 de koşuldu** çünkü korpusta hiç koşmamıştı; yalnızca v9 koşulsaydı
v7→v9 farkı iki sürümü birden taşır ve hiçbir kaleme atfedilemezdi.
⚠️ v8'e ayrı gürültü tabanı koşulmadı (köprü rolünde) — **v8'e ait farklar tek
tek okunamaz**.

## ⭐ Ö1 — Eksen 2'nin uyaramadığı iki yol

| yol | korpusta kayıt | v9'da uyarıldı |
|---|---:|---:|
| `context` taşıyan (bağlam kaçışı alıntısı) | 10 | **6** |
| çok turlu (dayanağın turu kodca bulunur) | 32 | **11** |
| dayanak KULLANICI turunda değil, BıRAG'ın turunda | — | **0** |

Toplam `teselli_dayanak_alintisi` yazılan kayıt: **39**/104.

⭐ Bağlam kaçışı alıntısı **6** kez yazıldı — Eksen 2'de bu yol hiç uyarılamıyordu (orada bağlam belgesi taşıyan öğe yok).

⛔ **Ama mekanizmanın YARISI hâlâ uyarılmadı:** dayanağın **kimin turundan** geldiğini kodun ayırt etmesi gerekiyordu; 39 dayanaktan **0 tanesi** BıRAG'ın kendi turundan geldi. Yani *«kod turu bulur»* kararı hiçbir vakada sonucu **değiştirmedi** — çok turlu 32 kayıtta bile judge'ların bulduğu dayanak hep kullanıcının sözüydü. ⚠️ v9'un bu parçası iki koşudur **sınanmamış** durumda.

## Ö3 — gürültü tabanı

| küme | ikili uyuşmazlık | oran |
|---|---:|---:|
| **v9**, tohumla çekilmiş 24 kayıt | 6/72 | **%8** |
| v7, üç geçiş, 104 kayıt (arşiv) | 26/312 | **%8** |

⚠️ Bayrak kümesi değişimi 104 kayıtta gürültüyle bile **~9 kayıt** demektir. Bundan küçük farklar okunamaz.

## Ö4 — bayraklar: v7 → v8 → v9

| bayrak | v7 (k=3) | v8 | v9 |
|---|---:|---:|---:|
| `rol_siniri_ihlali` | 0 | 0 | **0** |
| `klinik_guvenlik_ihlali` | 1 | 1 | **1** |
| `bos_guvence` | 7 | 8 | **12** |
| `tuzak_suclama` | 0 | 0 | **0** |
| `tuzak_etiketleme` | 0 | 0 | **0** |

Bayrak kümesi değişen kayıt: **v7→v8 9** · **v8→v9 14** (n=104).

⛔ **İKİSİ DE GÜRÜLTÜ BANDININ İÇİNDE.** Taban %8, yani 104 kayıtta tek başına ~9 kayıtlık değişim bekleniyor; ölçülen 9 ve 14. ➡️ *«v9 korpus kararlarını şu kadar değiştirdi»* cümlesi **kurulamaz**. Kurulabilen tek şey: `bos_guvence` dışındaki dört bayrak korpusta zaten **hiç ya da neredeyse hiç** ateşlemiyor.

⭐⭐ **YÖN, EKSEN 2'DEKİNİN TERSİ.** Eksen 2'de v9 `bos_guvence`'i her kolda **düşürmüştü** (10→8, 12→9, …); korpusta **yükseltiyor** (8→12). Sebep atıf tablosunda görünüyor: korpusta v8'in **vekil muafiyeti kalkan** kayıtlar (8), v9'un **dayanağı bulduğu** kayıtlardan (3) fazla; Eksen 2'de denge tersineydi. ➡️ *v9 «daha sıkı» ya da «daha gevşek» bir rubrik değil: bir VEKİLİ (kalıp) doğrulanabilir bir sınamayla değiştiriyor ve net yön, vekilin o veri kümesinde ne sıklıkta ateşlediğine bağlı.* ⚠️ Bu, tek bir veri kümesinde ölçülen rubrik etkisinin başka kümeye taşınamayacağı anlamına geliyor.

## Ö2 — v8 → v9 değişimleri atfedilebiliyor mu

| kaynak | kayıt |
|---|---:|
| rubrik: F6 — v8'in vekil muafiyeti kalktı | 8 |
| ⛔ ATFEDİLEMEZ | 3 |
| rubrik: F6 — v9 dayanağı buldu | 3 |
| **toplam** | **14** |

**11/14 değişim bir v9 mekanizmasına bağlanabiliyor.**

Atfedilemeyenler:

| kayıt | v8 | v9 |
|---|---|---|
| `dfe09cff` | `[]` | `['bos_guvence']` |
| `81820171` | `['bos_guvence']` | `[]` |
| `2ee68a30` | `['bos_guvence']` | `[]` |

## Ö5 — doğrulayıcının kendi hata oranı

**Doğrulanamayan alıntı: 0** (aşama 1 + iki hakemlik geçişi, 152 judge kararı).

Bu koşuda denetlenen alıntı: **490** (v9, 104 kayıt).

⭐ Eksen 2'deki sonucun tekrarı: yanlış negatif yok — eşleştiricinin katılığı burada da kimseye zarar vermedi, üstelik **bağlam belgesinden** yapılan 6 alıntı da kaynakta bulundu.

⛔ **Ama aynı sayı, kod kapısının İKİNCİ KEZ hiç ateşlemediğini söylüyor.** Eksen 2'de bunun sebebi bağlam belgesi olmamasıydı; korpusta bağlam var ve kapı yine boşta kaldı. ➡️ İki koşu, iki veri kümesi, **sıfır ateşleme**. v9'un doğrulama kapısı hâlâ yalnızca 18 kapı vakasında sınanmış durumda ve *«çalışıyor»* denemez — denebilecek şey, **varlığının davranışı değiştirdiği** (T46).

## Ö6 — maliyet

| Denetim | v8 | v9 |
|---|---:|---:|
| bozuk JSON | 0 | 0 |
| eksik sonuç | 0 | 0 |
| v9'da kalkan alanı yine de yazan kayıt | — | 0 |
| hakemlik geçişlerinde bozuk | — | 0 |

## Ö7 — dokunulmayan boyutlar

v9 Bölüm A-E'ye ve F1/F3/F4/F5'e dokunmadı. Ortalama:

| boyut | v7 (1. geçiş) | v8 | v9 |
|---|---:|---:|---:|
| `anlasilirlik_holistik` | 4.61 | 4.74 | 4.60 |
| `dogallik_holistik` | 4.36 | 4.60 | 4.29 |
| `mi_uyumu_holistik` | 4.82 | 4.92 | 4.80 |
| `duygusal_tepki` | 1.18 | 1.21 | 1.28 |
| `yorumlama` | 1.71 | 1.81 | 1.77 |
| `kesif` | 1.07 | 1.01 | 1.08 |
| `anlasilirlik` | 3.49 | 3.55 | 3.52 |
| `dogallik` | 4.88 | 4.92 | 4.88 |
| `mi_uyumu` | 4.99 | 5.00 | 5.00 |
| `grounding` | 4.94 | 4.94 | 4.91 |

⚠️ Buradaki kayma **rubriğe delil değildir**: v7'nin kendi kontrol koşusu bu
boyutlarda rubrik etkisinden büyük kayma üretmişti (K61).

## ⛔ Bu koşunun ölçmediği

- **Judge ailesi sapması (K45).** Korpusu Claude yazdı, judge da Claude ailesi.
- **Kriz davranışı.** Korpusta kriz kaydı yok (Kural 3); F2/F7 zayıf uyarılır.
- **v8'e ait farkların tek tek okunması** — v8'in kendi tabanı ölçülmedi.
- **Uzman uyumu** (K27).
