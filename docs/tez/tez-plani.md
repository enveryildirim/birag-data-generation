# Yüksek Lisans Tezi — Kayıt Planı

> **Amaç:** proje çalışırken tezin ihtiyaç duyacağı her şeyin *o anda* kaydedilmesi.
> Tez sonradan yazılır ama malzemesi sonradan üretilemez.
>
> Karar kaydı [../../PROJECT_MEMORY.md](../../PROJECT_MEMORY.md) · plan
> [../../plan.md](../../plan.md) · katkılar [katki-defteri.md](katki-defteri.md)
> · kaynakça [kaynakca.bib](kaynakca.bib)

**Durum:** iskelet · §2 ve §4 **repodan türetiliyor** (`scripts/analiz/2026-09-16-tez-plani-turetme.py`) · **Kurum:** Kocaeli Üniversitesi · **Bağlam:** TÜBİTAK/SBB BıRAG projesi İP1+İP2

---

## 1. Proje raporu ≠ tez

Aynı işten iki farklı belge çıkıyor ve **farklı şeyler kanıtlamaları gerekiyor**.

| | TÜBİTAK ara/sonuç raporu | Yüksek lisans tezi |
|---|---|---|
| İddia | *"Taahhüt ettiğimizi yaptık"* | *"Bilgiye katkı yaptım, kanıtı bu, sınırı bu"* |
| KPI | Form hedefleri karşılandı mı | KPI ilgisiz; **ölçümün geçerliliği** önemli |
| Ablasyon | Atlanabilir | **Atlanamaz** — "neden bu, neden şu değil" tezin omurgası |
| Negatif sonuç | Gizlenir | **Değerlidir**, ayrı bölüm |
| Alternatifler | Gerekmez | Gerekir — elenen yol ve gerekçesi |
| Literatür | Kısa | Ayrı bölüm, boşluk tespitiyle |
| Etik | Kurum onayı | Onay + **veri kökeni zinciri** + PII |

> **Pratik sonuç:** tez, projenin atlayabileceği üç şeyi zorunlu kılıyor —
> ablasyonlar, benzer çalışma taraması, etik kurul kaydı. Bunlar aşağıda.

---

## 2. Bölüm ↔ artefakt eşlemesi

Hangi tez bölümü hangi dosyadan yazılacak. **Boş hücre = üretilmemiş malzeme.**

<!-- TÜRETİLEN:bolum-artefakt başlangıç — elle düzenleme; `scripts/analiz/2026-09-16-tez-plani-turetme.py` üretir -->
| Tez bölümü | İlan edilen artefakt | Bulunan | Durum |
|---|---|---|---|
| 1. Giriş — problem, motivasyon | `docs/arastirma-notlari.md`<br>`docs/tez/kaynakca.bib` | **1**<br>**1** | ✅ |
| 2. Literatür — empati, MI, BDT, nüks, kriz | `docs/arastirma-notlari.md`<br>`docs/tez/kaynakca.bib` | **1**<br>**1** | ✅ |
| 2.x Benzer çalışmalar — Türkçe ruh sağlığı NLP | `docs/tez/benzer-calismalar.md` | **1** | ✅ |
| 3. Yöntem — veri üretim mimarisi | `plan.md`<br>`prompts/uretim-v*.md`<br>`configs/**/*.yaml` | **1**<br>**3**<br>**29** | ✅ |
| 3.x Alternatifler ve elenme gerekçeleri | `PROJECT_MEMORY.md` | **1** | ✅ |
| 4. Veri seti — taksonomi, karışım, kalite kapıları | `configs/taxonomy.yaml`<br>`datasets/*/CARD.md`<br>`plan.md` | **1**<br>**5**<br>**1** | ✅ |
| 4.x Veri kökeni ve ön işleme | `src/normalize.py`<br>`datasets/*/manifest.json`<br>`src/checks.py` | **1**<br>**5**<br>**1** | ✅ |
| 5. Deney kurulumu — modeller, hiperparametreler | `configs/training/*.yaml`<br>`runs/*/config.yaml`<br>`src/train.py` | **25**<br>**24**<br>**1** | ✅ |
| 6. Değerlendirme — 5 eksen, rubrik, uzman uyumu | `evals/*.jsonl`<br>`prompts/judge-eksen1.v*.md`<br>`reports/analiz/*uzman-puanlama*.md` | **9**<br>**9**<br>**1** | ✅ |
| 7. Sonuçlar — tablolar, şekiller | `runs/*/metrics.json`<br>`reports/analiz/*lora-kapsam-taramasi*.md`<br>`reports/analiz/*eksen-baseline*.md` | **24**<br>**2**<br>**1** | ✅ |
| 8. Ablasyonlar | `reports/analiz/*doz-yanit-egrisi.md`<br>`reports/analiz/*prompt-dili-ablasyonu.md`<br>`reports/analiz/*rol-siniri-ablasyonu.md`<br>`reports/analiz/*muafiyet-kapisi-gucu.md`<br>`reports/analiz/*ic-muhakeme-sizintisi.md` | **1**<br>**1**<br>**1**<br>**1**<br>**1** | ✅ |
| 9. Hata analizi | `reports/analiz/ham-judge/*.jsonl`<br>`reports/analiz/*v9-kapi-defteri.md`<br>`reports/analiz/*geriye-donuk-eslesme.md`<br>`reports/analiz/*judge-kapsama-kalibrasyonu.md` | **42**<br>**1**<br>**1**<br>**1** | ✅ |
| 10. Tartışma, sınırlılıklar | `docs/tez/katki-defteri.md`<br>`reports/analiz/*katki-defteri-denetimi.md` | **1**<br>**1** | ✅ |
| 11. Etik | `data/guvenlik-karantinasi.jsonl`<br>`docs/tez/etik-kurul.md` | **1**<br>**0** | 🟡 — eksik: etik kurul kaydı |
| Ek. Yeniden üretilebilirlik | `uv.lock`<br>`reports/analiz/*rapor-yeniden-uretilebilirlik.md`<br>`reports/analiz/*ilan-edilen-sha-denetimi.md` | **1**<br>**1**<br>**1** | ✅ |
<!-- TÜRETİLEN:bolum-artefakt bitiş -->

---

## 3. Kayıt kuralları *(bugünden itibaren geçerli)*

### 3.1 Her sayı izlenebilir olmalı
Sohbette üretilen sayı **tezde kullanılamaz** — 6 ay sonra yeniden üretilemez.

```
reports/analiz/<tarih>-<konu>.md     ← çıktı
scripts/analiz/<tarih>-<konu>.py     ← onu üreten betik (commit edilir)
```
Her rapor başlığında: **girdi dosyası + SHA256 · betik sürümü · tarih · ortam**.

> ⚠️ Mevcut borç: Oturum 9'un tüm ölçümleri (thinking medyanı 181/IQR 168-192,
> 186 telefonlu kayıt, kapsama yüzdeleri) **betiksiz**. Faz 0'da geri üretilecek.

### 3.2 Her eğitim koşusu saklanır
`runs/<ts>/` **asla silinmez, üzerine yazılmaz.** İçinde: `config.yaml` ·
`metrics.json` · `samples.md` · dataset sürümü + hash · **rastgele tohum** ·
git commit · donanım. Başarısız koşu da saklanır — tezin negatif sonuç bölümü.

### 3.3 Her karar gerekçeli
`PROJECT_MEMORY.md`'nin **Gerekçe** sütunu doğrudan tezin 3.x bölümü olacak.
Bu yüzden gerekçe "kullanıcı istedi" değil, **teknik neden** olmalı.

### 3.4 Her özgün iddia anında kaydedilir
→ [katki-defteri.md](katki-defteri.md). Ortaya çıktığı anda, sonra değil.

### 3.5 Veri seti kartı
`datasets/vX.Y.Z/CARD.md` *Datasheets for Datasets* yapısında: motivasyon ·
bileşim · toplama süreci · ön işleme · kullanım · dağıtım · bakım. Doğrudan
tez bölüm 4 olur.

---

## 4. Yeniden üretilebilirlik kontrol listesi

<!-- TÜRETİLEN:yeniden-uretilebilirlik başlangıç — elle düzenleme; `scripts/analiz/2026-09-16-tez-plani-turetme.py` üretir -->
| | Kontrol | Repoda bulunan |
|---|---|---|
| ✅ | `uv.lock` commit edilir — tam sürüm ağacı | `uv.lock` |
| ✅ | Python sürümü kilitli | `.python-version` = `3.12` |
| ✅ | Tüm rastgele tohumlar sabit ve kayıtlı | 24/24 koşunun `config.yaml`'ında `seed:` |
| ✅ | Dataset sürümleri immutable + `manifest.json` (SHA256) | 5 manifest, hepsinde SHA256 |
| ✅ | Veri kartı her sürümde (`CARD.md`) | 5/5 sürümde `CARD.md` |
| ✅ | Prompt sürümleri sürümlenmiş dosyalarda | 14 prompt dosyası |
| ✅ | Her koşuda **süre** kaydedilir | 24/24 koşuda `sure_saniye` |
| ⛔ | Her koşuda **donanım** kaydedilir | 0/24 koşuda donanım alanı |
| ✅ | Her koşuda **git commit** kaydedilir | 24/24 koşuda `git_rev` |
| ✅ | `just` hedefleri tek komutla tekrar koşturur | `justfile` (2 hedef) |
| ✅ | Her rapor betiğine bağlı ve yeniden üretiliyor (Kural 7) | `rapor-yeniden-uretilebilirlik.md` |
| ✅ | Raporların ilan ettiği SHA256 denetleniyor | `ilan-edilen-sha-denetimi.md` |
<!-- TÜRETİLEN:yeniden-uretilebilirlik bitiş -->
- [ ] ⚠️ **Claude Code üretimi tekrarlanabilir değil** (K30) — bu bir sınırlılık
      olarak tezde **açıkça yazılır**. Telafi: üretilen her kayıt tohum + prompt
      sürümü + tarih ile saklanır; *çıktı* yeniden üretilemese de *köken* izlenir

---

## 5. Etik kaydı 🔴 **en acil eksik**

| Konu | Durum | Not |
|---|---|---|
| **Etik kurul onayı** | ❓ | ⚠️ **K27 uzman puanlaması insan katılımcı içeriyor.** Çoğu üniversitede *veri toplamadan önce* onay gerekir. Faz 3'ü bloke edebilir — **erken sorulmalı** |
| Veri kökeni zinciri | 🟡 | Her kaydın kökeni: sentetik / korpustan tohum / uzman. Şemada `source_ids` var |
| PII taraması | 🟡 | 186 kayıtta telefon bulundu (K18 ihlali) — **bu bulgu tezde raporlanır** |
| Forum verisi (Reddit/Quora) | ❓ | Form Tablo 3'te var; İP1'in "%100 etik" hedefiyle gerilim. Karar verilmedi |
| Anonim terapi kayıtları | ❓ | Erişim ve onay durumu bilinmiyor (K20 açık soruları) |
| Klinik sorumluluk sınırı | ✅ | Model tanı/doz/ilaç vermez — `AGENTS.md` Kural 3, `plan.md` §15 |
| Kriz protokolü sorumluluğu | 🟡 | Uzman onayı bekliyor (K23). Tezde sınırlılık olarak yazılacak |

---

## 6. Teze özgü deneyler *(proje atlayabilir, tez atlayamaz)*

| Kod | Deney | Neden tez için gerekli | Maliyet |
|---|---|---|---|
| **T10-D** | **bf16 LoRA vs QLoRA, farklı deploy quantization şemasıyla** | K7 şu an sadece argüman. Ölçülürse defterdeki **en güçlü tek katkı** (T10) | Orta — Faz 5'e eklenir |
| **B-0** | **Prompt-only baseline** (fine-tune yok, sadece system prompt) | Tez "fine-tune gerekliydi"i kanıtlamak zorunda. Projenin baseline'ı zaten planlı | Düşük |
| **A-1** | Replay oranı %0 / %15 / %30 | K12'nin dayanağı yok; forgetting iddiası ölçülmeli | Planlı (Faz 5) |
| **A-2** | Red oranı %10/%15/%20 | K16 aşırı red riski | Planlı (Faz 5) |
| **A-3** | **Ölçekleme eğrisi** — çeyrek/yarı/tam veri | K34'ün ve "kalite > hacim" iddiasının kanıtı | Planlı (Faz 5) |
| **A-4** | thinking açık/kapalı ve uzunluk | K5, K10, T7 | Planlı (Faz 5) |
| **G-1** | **Aileler arası transfer** (Qwen3.8-27B) | Veri setinin davranış mı kodladığı, aileye mi fit olduğu (K33) | Planlı (Faz 7) |
| **M-1** | `dev` ↔ `test`/`locked` sapmasının iterasyonla seyri | **T6'nın tek kanıtı.** Sıfır ek maliyet — zaten ölçülen sayılar saklanırsa çıkar | Sıfır |

> **M-1'e dikkat:** hiçbir ek koşu gerektirmiyor, yalnızca her iterasyonun
> eval sayılarının saklanmasını gerektiriyor. Saklanmazsa katkı kaybolur.

---

## 7. Karar bekleyenler

- [ ] **Tez başlığı ve kapsamı** — İP1+İP2'nin tamamı mı, yalnızca veri seti mi?
- [ ] **Danışman** ve tez izleme takvimi
- [ ] **Etik kurul** — gerekli mi, süreci ne, ne kadar sürüyor? ⚠️ Faz 3'ü bloke edebilir
- [ ] **Yayın** — tezden makale çıkacak mı? (T1/T2/T10 buna uygun)
- [ ] **T11 katkı paylaşımı** — `personas.md` kullanıcının kendi ön çalışması
- [ ] **Proje ↔ tez sınırı** — ekip çalışması ile bireysel katkı nasıl ayrılacak?
