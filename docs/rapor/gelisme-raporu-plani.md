# Gelişme raporu planı — dönem 0–12. ay · İP1 ve İP2

> - Karar (kullanıcı, 2026-10-20): rapor dönemi **0–12. ay**; bu ekip **İP1 ve İP2'yi** yazar.
>   İP4 bu raporda bizden çıkmaz.
> - Şablon: `rapor-bırag.docx` (1.1 Dönem İçinde Gerçekleştirilen Faaliyetler) · hoca notları: `z.md`
> - Taahhüt ↔ yapılan eşlemesi: [oneri-rapor-esleme.md](oneri-rapor-esleme.md) — bu plan onu rapora çevirir.
> - Kural 7: rapordaki her sayı `reports/analiz/` altındaki bir dosyaya bağlanır; sohbette üretilen sayı girmez.

## 0. Kapsam ve dikkat

| İP | Çizelgedeki ay | Bu dönemdeki payı | Bu raporda |
|---|---|---|---|
| İP1 Talimat veri kümesi | 0–12 | tamamı | ✅ bizden |
| İP2 Model geliştirme ve ince ayar | 6–10 | tamamı | ✅ bizden |
| İP3 RAG modülü | 10–15 | 10–12. ay | ⚠️ şablon *«dönem için planlanan **tüm** İP'ler»* diyor → İP3 sorumlusuna (Doç. Dr. M. H. B. UÇAR) haber verilmeli. Bizim katkımız: RAG bağlam sözleşmesi (K17) ve korpus şartnamesi (`plan.md` §17) |

İki İP'nin dönemi de 12. ayda **bitmiş olmalı**; tamamlanma yüzdesi bu yüzden «planlanana göre»
değil «hedefe göre» okunur ve eksik kalan her şey için gerekçe + sonraki dönem planı yazılır.

## 1. Tamamlanma yüzdesi — öneri (karar yürütücünün)

Yöntem: iş-zaman çizelgesindeki hedefler eşit ağırlıklı; her hedefe eşleme matrisine göre puan.

| İP1 hedefi (çizelge) | Puan | Dayanak |
|---|---:|---|
| 10.000 çeşitli ve bağlama uygun örnek | 60 | `v0.1.0` 1058 + ölçek-5k (bitince kesinleşir) ≈ 6.000 / 10.000 |
| Tutarlılık ve anlam bütünlüğü | 90 | Deterministik kapılar, judge, sürüm disiplini; uzman doğrulaması 50/70 |
| Türkçe, kültürel ve dilsel bağlam | 85 | İfade bankası, register çalışması; uzman kabulü %68 (hedef %70) |
| Etik onay ve anonimleştirme | 60 | Veri sentetik; PII raporu eksik; kriz ve forum verisi etik kurul bekliyor |
| **İP1 önerilen** | **≈ %75** | |

| İP2 hedefi (çizelge) | Puan | Dayanak |
|---|---:|---|
| Özelleştirilmiş talimatlara uyum için eğitmek | 80 | Eğitim hattı kuruldu, 26B-A4B eğitildi |
| Terapötik diyaloglarda anlamlı, bağlama uygun çıktı | 50 | Değerlendirme sistemi hazır; sonuç tabandan kötü |
| Türkçe için performansı optimize etmek | 80 | Düşünme kanalı %100 Türkçe |
| Yanıt hızı ve doğruluk | 50 | Düşünme ~5 kat kısaldı; gecikme yeniden ölçülmedi |
| Etik ve güvenlik protokolleri | 50 | Protokol ve sert kapı uygulandı; güvenlikte gerileme ölçüldü |
| **İP2 önerilen** | **≈ %60–65** | |

## 2. Rapor iskeleti

Şablondaki tablo İP başına bir kez kopyalanır: `İP No · İP Adı · Tamamlanma %` →
**Yapılan Çalışmalar ve Bulgular** (alt başlıklı) → **Başarı Ölçütlerine Göre Gerçekleşme** (tablo + değerlendirme).

### İP1 — LLM için Talimat Veri Kümesi Toplama ve Ön İşleme

| § | Alt başlık | İçerik | Kaynak | Şekil |
|---|---|---|---|---|
| 1.1 | Amaç ve öneriyle ilişki | Tablo 1 hedefleri; dönemde izlenen yol | form s.3 | — |
| 1.2 | Veri kaynakları ve tohum talimatlar | 2.240 senaryo tohumu, normalizasyon, kontrollü sözlük; Tablo 3 kaynaklarının her birinin akıbeti | Faz 1 · `configs/taxonomy.yaml` | — |
| 1.3 | Terapötik çerçeve | MI/BDT ilkeleri, 19 senaryoluk davranış kartları, yasak ifade listesi, rol sınırı | `docs/arastirma-notlari.md` · `docs/davranis-kartlari.md` | — |
| 1.4 | Taksonomi ve veri karışımı | 16 senaryo tipi, Türkiye verisine göre bağımlılık türü ağırlıkları, kullanıcı mesajı biçimi ve register | `plan.md` §5–6 · K22 · K42 | Ş3 |
| 1.5 | Üretim boru hattı | Tohum → üretim → deterministik kapılar → LLM-judge → değişmez sürüm; önbellek ve idempotentlik | `plan.md` §8 · `src/` | **Ş1** |
| 1.6 | Ön işleme | Şema, rol etiketleri, chat template, düşünme + cevap biçimi; PII taraması | K44 · K5 | — |
| 1.7 | Kalite güvencesi | Judge sürümleri ve yanlılık ölçümleri; uzman puanlaması (50/70, %68); judge ↔ uzman uyumu | K43 · K58 · K104 | Ş5 |
| 1.8 | Değerlendirme setleri | Elle yazılan golden dev/test/locked (48'er), dört eksen seti | `evals/` · K31 | — |
| 1.9 | Elde edilen sürümler | `v0.0.1` → `v0.1.0` (1058, donduruldu) → `v0.1.1` → ölçek-5k | veri kartları · K275 · K279 | Ş4 |
| 1.10 | Karşılaşılan sorunlar ve B planları | Kriz dilimi (uzman ve etik onay), vahşi doğa dilimi, Türkçe büyük/küçük harf hatası, forum verisinin etik sorunu — formdaki risk tablosuyla eşlenir | form s.18 | — |
| 1.11 | Ara çıktılar | Ekler listesine gönderme | §5 | — |

### İP2 — Model Geliştirme ve İnce Ayarının Yapılması

| § | Alt başlık | İçerik | Kaynak | Şekil |
|---|---|---|---|---|
| 2.1 | Amaç ve öneriyle ilişki | Tablo 1 hedefleri; **dört yöntem güncellemesi ve gerekçeleri** (model ailesi, ORPO, QLoRA, BLEU/ROUGE) | K29 · K7 · K9 · `plan.md` §14 | — |
| 2.2 | Model seçimi | Gemma 4 merdiveni (E4B → 12B → 26B-A4B → 31B), Qwen3.8-27B genelleme kapısı | K29 | **Ş2** |
| 2.3 | Eğitim altyapısı | bf16 LoRA; MLX ile yerel keşif, Colab + Unsloth üretim; tek YAML; deney kaydı ve ön kayıt | K7 · T305–T308 | — |
| 2.4 | Düşünme kanalı | Türkçe ve kısa düşünme; dil ve uzunluk bulguları; gecikmeyle ilişkisi | K46 · K50 · K107 | Ş9 |
| 2.5 | Değerlendirme sistemi | 5 eksen (terapötik kalite, güvenlik, unutma, bağlam sadakati, dalkavukluk); Pareto seçim kuralı | `plan.md` §7 · §9 | — |
| 2.6 | Baseline | İnce ayar öncesi 5 eksen ve gecikme | K105–K107 | — |
| 2.7 | LoRA kapsam ve derinlik deneyleri | Kapsam merdiveni; derinlik ↔ rank; katman 29 bulgusu | K109 · K174/K175 · T28 | Ş6 |
| 2.8 | 26B-A4B ince ayar sonuçları | Taban ↔ ince: insan ve judge; kriz yönlendirmesi gerilemesi; unutma; teşhis | T311 raporları | **Ş7 · Ş8** |
| 2.9 | Tartışma | Krizsiz veriyle ince ayarın bedeli; neden model dışı güvenlik katmanı gerekli | T311 · İP4 teslim notu | — |
| 2.10 | Sonraki dönem | Kriz dilimi (uzman onayı), ölçek-5k ile yeniden eğitim, BLEU/ROUGE ve uzman değerlendirmesi, ORPO kararı | açık sorular | — |

## 3. Şekiller

Her şekil `scripts/analiz/2026-10-2x-rapor-sekil-*.py` ile üretilir, PNG `reports/analiz/sekiller/`
altına; başlıkta girdi SHA'sı. Çizim: `uv run --with matplotlib` (projeye bağımlılık eklenmez, Kural 4).

| # | Şekil | Girdi | Not |
|---|---|---|---|
| Ş1 | İP1–İP2 boru hattı | — (diyagram) | Formdaki Şekil 1'in gerçekleşen hâli; en önemli şekil |
| Ş2 | Model merdiveni | K29 | Diyagram |
| Ş3 | Senaryo ve bağımlılık türü dağılımı | `datasets/v0.1.0/train.jsonl` | Çubuk grafik |
| Ş4 | Sürümlerin gelişimi | `datasets/*/manifest.json` | Kayıt sayısı zaman çizgisi |
| Ş5 | Uzman ↔ judge uyumu | uzman puanlama raporu | |
| Ş6 | Doz-yanıt / LoRA kapsam eğrisi | `2026-09-15-doz-yanit-derleme.json` · `f4c-doz-egrisi.json` | |
| Ş7 | Taban ↔ ince karşılaştırma | T311 ham sonuçları | ⚠️ ham veri muhtemelen `birag-degerlendirme/` içinde |
| Ş8 | Kriz yönlendirmesi (15 risk öğesi) | aynı | ⚠️ aynı |
| Ş9 | Düşünme uzunluğu ↔ gecikme | `2026-09-15-gecikme-taban` girdisi | |

## 4. Rapordan önce kapatılacak eksikler

| Eksik | İP ölçütü | Bu makinede yapılabilir mi |
|---|---|---|
| PII taraması betiği ve raporu | İP1 %100 anonim | ✅ `reports/analiz/2026-10-20-ip1-olcutler.md` |
| Senaryo uyumu % ve dil modeli (şema + template) uyumu % | İP1 %90 · %95 | ✅ aynı rapor |
| İP2 doğruluk vekili · zararlı yanıt · Türkçe | İP2 | ✅ `reports/analiz/2026-10-20-ip2-olcutler.md` |
| Ölçek-5k'nın bitmesi (A 4975/5000 · B 3625 · C 0 — 2026-10-20) | İP1 10.000 | ⏳ koşu sürüyor |
| BLEU/ROUGE/chrF/F1/BERTScore (referanslı 200 kayıt) | İP2 BLEU/ROUGE | ⏳ `notebooks/rapor-bleu-gecikme.ipynb` → yerelde `2026-10-20-rapor-bleu-gecikme-puanla.py` |
| Tek istek gecikmesi | İP2 < 2 sn | ⏳ aynı defter |
| Duygu tonu etiketi (form s.9) | İP1 ön işleme | Karar gerek: etiketlenir mi, gerekçelendirilir mi |
| K9 (BLEU/ROUGE yeniden tanımı) yürütücü onayı | İP2 | 👤 yürütücü |

## 5. Ekler (ara çıktılar)

| Ek | Ara çıktı | Dosya |
|---|---|---|
| A | Veri kümesi kartı `v0.1.0` | `datasets/v0.1.0/CARD.md` |
| B | Kontrollü sözlük / taksonomi | `configs/taxonomy.yaml` |
| C | Davranış kartları ve yasak ifade listesi | `docs/davranis-kartlari.md` · `plan.md` §15 |
| D | Örnek talimat kayıtları (Tablo 4'ün gerçekleşen karşılığı, senaryo başına bir tane) | `datasets/v0.1.0/train.jsonl` |
| E | Değerlendirme protokolü ve rubrik | `docs/tez/degerlendirme-protokolu.md` |
| F | Uzman brifingi | `docs/uzman-brifingi.md` |
| G | Eğitim defteri ve model kartı | `notebooks/v011-unsloth-egitim.ipynb` · `docs/hf/model-karti-26b.md` |

## 6. İş sırası

1. Veriyle yapılabilen eksik betikler: PII, uyum yüzdeleri
2. Şekiller: Ş1–Ş6, Ş9 (veri hazır)
3. İP1 metni (markdown taslak, `docs/rapor/ip1.md`) → ekip okuması
4. İP2 metni (`docs/rapor/ip2.md`) — Ş7/Ş8 ve BLEU/ROUGE için `birag-degerlendirme/` izni gerekir
5. Ölçek-5k bitince İP1 sayılarını kesinleştirmek
6. Şablonun biçimi korunarak `rapor-bırag-dolu.docx` (özgün dosyaya dokunulmaz)
7. Hoca/yürütücü: tamamlanma yüzdeleri, K9 onayı, İP3 sorumlusuna haber
