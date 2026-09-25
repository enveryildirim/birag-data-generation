# Tez planı repodan türetildi — §2 ve §4 elle bakımdan çıktı

**Betik:** `scripts/analiz/2026-09-16-tez-plani-turetme.py` · **Tarih:** 2026-09-16  
**Yazdığı yer:** `docs/tez/tez-plani.md` — yalnızca `TÜRETİLEN:` işaretli bölgeler  
**Eşleme:** *«hangi bölüm hangi artefakttan yazılacak»* **bizim kararımız** (Kural 6); türetilen şey yalnızca **durum**

---

## Neden

`tez-plani.md` 2026-09-12'de yazıldı ve elle güncellenmedi. §2'nin
*«Sonuçlar 🔴 · Ablasyonlar 🔴 · Hata analizi 🔴»* satırları o gün doğruydu,
bugün değil. ⚠️ Bu T54'ün **EL** sınıfı: elle tutulan bir durum tablosu
gerçeğinden sessizce ayrılır. ➡️ *Çözüm tabloyu doğru doldurmak değil,
TÜRETMEK — bir daha elle bakım istemesin.*

## 1. Bölüm ↔ artefakt

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

**Durum:** ✅ 14 · 🟡 1 · 🔴 0 bölüm.

## 2. Yeniden üretilebilirlik kontrol listesi

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

**11/12 kontrol tutuyor.**

## ⛔ Bu türetmenin söylemedikleri

| | |
|---|---|
| ⛔ **Eşleme türetilmedi** | hangi bölümün hangi artefakttan yazılacağı editoryal bir karar; betik onu **ilan eder**, repodan çıkarmaz (Kural 6) |
| ⛔ **Varlık ≠ yeterlilik** | bir dosyanın durması o bölümün yazılabileceği anlamına gelmez; ölçülen şey **malzemenin varlığı**, olgunluğu değil |
| ⛔ Onay durumları | etik kurul, danışman, uzman onayı repoda **yok** ve olamaz — §5 ve §7 elle kalmaya devam ediyor |
| ⚠️ Sayılar glob'a bağlı | desen değişirse sayı değişir; desenler tabloda **açıkça yazılı** ki okuyucu neyin sayıldığını görsün |

