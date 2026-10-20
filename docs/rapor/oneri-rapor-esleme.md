# Öneri ↔ gelişme raporu eşleme matrisi

> Amaç: gelişme raporunu (`rapor-bırag.docx`) doldururken **önerideki her taahhüdün**
> raporda karşılığı olsun, sapmalar gerekçesiyle yazılsın (hoca notu: *«öneride
> vadedilenlerle raporun örtüşmesi önemli»*).
>
> - Kaynak: `BASVURU_FORMU_(BASVURU_FORMU_SBB_BAGIMLILIK).PDF` (SHA256-16 `e4865d3254d92a70`, 22 sayfa)
> - Proje durumu: `PROJECT_MEMORY.md` (2026-10-20) · `plan.md`
> - Tarih: 2026-10-20 · Sayılar kayıtlardan aktarıldı; rapora girecek her sayı için
>   «Kanıt» sütunundaki dosya kaynaktır (Kural 7).

**Durum işaretleri:** ✅ karşılandı · ◐ kısmen / ölçüm eksik · ⛔ karşılanmadı ·
↺ yöntem değişti (gerekçesi yazılmalı) · ⏳ dönemi gelmedi

## 0. Çerçeve — formdan

| İP | Ad (formdaki gibi) | Ay | Sorumlu | Projeye katkı |
|---|---|---|---|---|
| 1 | LLM için Talimat Veri Kümesi Toplama ve Ön İşleme | 0–12 | Doç. Dr. Serdar SOLAK | %15 |
| 2 | Model Geliştirme ve İnce Ayarının Yapılması | 6–10 | Doç. Dr. Süleyman EKEN | %20 |
| 3 | RAG Destekli Modül Geliştirme | 10–15 | Doç. Dr. M. H. Bilgehan UÇAR | %20 |
| 4 | Sistem Entegrasyonu ve Mobil Uygulama Geliştirme | 13–18 | Doç. Dr. Süleyman EKEN | %15 |
| 5 | Mobil Uygulamanın Değerlendirilmesi ve Nihai Hale Getirilmesi | 18–20 | Doç. Dr. Bahadır GENİŞ | %15 |
| 6 | Veri Güdümlü Analiz ve Önleyici Çalışmalara Katkının Araştırılması | 21–24 | Doç. Dr. Hande ALBAYRAK | %15 |

✅ **Karar (kullanıcı, 2026-10-20):** rapor dönemi **0–12. ay**; bu ekip İP1 ve İP2'yi yazar,
İP4 bizden çıkmaz (§3 yalnız arayüz kaydı olarak kalır). İş planı: [gelisme-raporu-plani.md](gelisme-raporu-plani.md).

## 1. İP1 — başarı ölçütleri (form s.3 · s.16)

| Taahhüt | Yapılan | Durum | Kanıt | Raporda |
|---|---|---|---|---|
| 10.000 talimat örneği | `v0.1.0` donduruldu (1058 kayıt); `v0.1.1` düşünme yeniden kurulumu; **ölçek-5k üretimi sürüyor** | ◐ | `datasets/v0.1.0/CARD.md` · K275 · K279 · `reports/analiz/2026-10-20-olcek5k-plan.md` | Aşamalı hacim stratejisi (K34): önce ölçekleme eğrisi, sonra hacim. Dönem sonu sayısı ölçek-5k bitince yazılır |
| %90 hedef senaryolarla uyumlu ve doğru biçimli | Kontrollü sözlük kapsaması %98–100; `checks.py` deterministik kapıları | ◐ | `configs/taxonomy.yaml` · `reports/analiz/2026-09-14-dilim-kapsama.md` | **Tek yüzde üreten betik eksik** → yazılacak |
| %95 dil modeliyle uyumlu | Şema doğrulama + `apply_chat_template` (K44); her derlemede | ◐ | `src/schemas.py` · `src/build.py` | Oranı üreten betik eksik → yazılacak |
| %70 Türkçe veride olumlu değerlendirme | Uzman puanlaması: 50/70 kayıtta **%68 kabul** | ◐ | K58 · `reports/analiz/2026-09-14-uzman-puanlama-analizi.md` | Sınırda; tek uzman, «kullanıcı» değil «uzman» geribildirimi — açıkça yazılır |
| %100 etik ve anonim | Veri sentetik; gerçek kişi verisi yok; uzman korpusu doğrudan satır olarak kullanılmadı (K20, PII riski) | ◐ | K20 · `plan.md` §8 | **PII tarama raporu yok** → betik yazılacak (`plan.md` §8'de söz verilmiş) |

### İP1 — yöntem taahhütleri (form s.8–10, Tablo 3–4)

| Taahhüt | Yapılan | Durum | Raporda |
|---|---|---|---|
| Bilimsel makale / WHO kılavuzu / BDT kitapları | Terapötik çerçeve (MI/BDT), davranış kartları, yasak ifade listesi — kaynakçalı | ✅ | `docs/arastirma-notlari.md` · `docs/davranis-kartlari.md` |
| Anonimleştirilmiş gerçek terapi diyalogları | Kullanılmadı; erişim ve etik onay açık soru | ⛔ | Etik onay bekliyor; gerekçe yazılır |
| Uzman yazımı sentetik diyaloglar | Uzman korpusu → kalıp düzeyinde çıkarım (Türkçe ifade bankası) | ✅ | K20 · `docs/turkce-ifade-bankasi.md` |
| Forum kazıma (Reddit, Quora…) | **Bilinçli olarak yapılmadı** — savunmasız bireylerin sağlık verisi; «vahşi doğa» dilimi etik kurul kararı bekliyor | ⛔ | Etik gerekçe; B planı |
| Açık veri tabanları | Replay dilimi (genel yetenek koruması) — `v0.1.0`'da %1,7, hedef %15 | ◐ | — |
| Otomatik üretim (GPT-4, turkish-gpt2…) | Claude Code + alt ajanlar (ölçek-5k'da Haiku/Sonnet) | ↺ | Model güncellemesi, gerekçe K30/K260/K279 |
| Tohum talimatlardan otomatik çoğaltma | 2.240 senaryo tohumu → üretim | ✅ | `data/seeds*.jsonl` |
| PII maskeleme | Sentetik veri; ayrı tarama raporu yok | ◐ | Tarama betiği |
| Ortak format (JSON), parçalama | JSONL şema, sürümlü değişmez setler | ✅ | `plan.md` §12 |
| Rol etiketleme (terapist/danışan) | Chat template rolleri | ✅ | K44 |
| **Duygu tonu etiketleme (pozitif/negatif/nötr)** | **Yapılmadı** | ⛔ | Ya etiketlenir ya gerekçelendirilir (İP4 duygu analizi ajanının işi) |
| Uzman doğrulaması | 50/70 | ◐ | K58 |
| Tablo 4 senaryoları (6 adet) | 16 senaryo tipi bunları kapsıyor; **kriz yönetimi** dilimi uzman onayı beklediği için 0 kayıt; **bilgilendirme** RAG'e (İP3) bırakıldı | ◐ ↺ | `plan.md` §3 · §5 |
| Tütün, alkol, madde, kumar | Türkiye verisine göre ağırlıklar | ✅ | K22 · `plan.md` §5 |

## 2. İP2 — başarı ölçütleri (form s.3 · s.17)

| Taahhüt | Yapılan | Durum | Kanıt | Raporda |
|---|---|---|---|---|
| Doğruluk > %90 | 5 eksenli değerlendirme; 26B-A4B ince modeli tabandan kötü | ⛔ | `reports/analiz/2026-10-20-taban-vs-ince-basit-inceleme.md` | Negatif bulgu + teşhis |
| Uzman memnuniyeti %85 | İnce model için uzman değerlendirmesi yok; ekip insan değerlendirmesi 26–8 taban lehine (p=0,003) | ⛔ | aynı | Uzman turu gelecek dönem |
| BLEU / ROUGE > %80 | **K9 ile yeniden tanımlandı** (serbest diyalogda anlamsız); uzman + judge birincil | ↺ ⚠️ | K9 — **yürütücü onayı hâlâ bekliyor** | Öneri: yine de golden sette BLEU/ROUGE/BERTScore hesaplanıp raporlanır, neden yetersiz olduğu tartışılır |
| Yanıt < 2 sn | Taban ortanca 12,9 sn (E4B, istenmemiş düşünme yüzünden; korelasyon 0,94). İnce modelde düşünme ~5 kat az jeton | ◐ | K107 · `reports/analiz/2026-09-15-gecikme-taban.md` · T311 | İnce modelde gecikme **yeniden ölçülmeli** |
| Kullanıcı geribildirimi %90 olumlu | Kullanıcı yok | ⏳ | — | İP5 pilotuna bağlı |
| %100 etik, zararlı yanıt ≈ %0 | İnce model 15 risk öğesinin 4'ünde yönlendirmeyi kaybetti; bir kriz hattı numarası uydurdu | ⛔ | T311 · `reports/analiz/2026-10-20-olcek5k-kalip-kriz.md` | Teşhis: veride kriz dilimi yok. B planı: kriz dilimi + **model dışı güvenlik katmanı** (İP4 koordinatör ajanına bağlanır) |

### İP2 — yöntem taahhütleri (form s.10)

| Taahhüt | Yapılan | Durum | Gerekçe (kayıt) |
|---|---|---|---|
| Gemma 2 9B It · Aya Expanse 8B · Llama-3.1-8B-Instruct | Gemma 4 ailesi (E4B → 12B → 26B-A4B → 31B) + Qwen3.8-27B genelleme kapısı | ↺ | K6 → K29: form modelleri 2024 nesli, düşünme kanalı yok; 26B-A4B 3,8B etkin parametreyle kalite/gecikme dengesi |
| ORPO ile eğitim | SFT; ORPO ertelendi | ↺ | `plan.md` §14: dar tercih verisiyle ORPO unutmayı artırır; önce SFT + replay ölçülür. Judge'ın kabul/ret ayrımı tercih çifti kaynağı olabilir |
| QLoRA (4-bit) | bf16 LoRA | ↺ | K7: QLoRA'da dağıtım şeması farklıyken kalite sessizce düşer |
| PEFT / LoRA, unutmaya karşı | LoRA kapsam ve derinlik deneyleri; katman 29 bulgusu; Eksen 3 unutma | ✅ | K109 · K174/K175 |
| Hiperparametre yapılandırması, GPU | Tek YAML; MLX (yerel) + Colab/Unsloth | ✅ ↺ | TRUBA yerine Colab — araştırma olanakları sapması |
| Deney takibi | `runs/` kayıtları, ön kayıt (pre-registration) mühürleri | ✅ | Kural 7 · T305/T306/T308 |
| Uzmanlarca klinik değerlendirme | Baz veri için 50/70; ince model için yok | ◐ | — |
| Risk B planı: çapraz doğrulama, otomatik hiperparametre | dev/test/locked bölmesi; kapsam merdiveni | ✅ | K31 · K109 |

## 3. İP4 — bu repodan sağlanabilecek kısım (form s.4 · s.12–13 · s.17)

İP4'ün kendisi (mobil uygulama, ruh hali takibi, hedef belirleme, nüks tahmini,
LangChain ile 5 ajan) **bu reponun kapsamı dışında**; anlatımı İP4 ekibi yazmalı.
Bu repo yalnızca şu arayüzleri sağlar:

| İP4 taahhüdü | Bu repodan katkı | Durum |
|---|---|---|
| İnce ayarlı LLM + RAG entegrasyonu | OpenAI-uyumlu uç nokta, GGUF sohbet defteri, RAG context sözleşmesi (K17) | ◐ |
| Terapi rehberlik ajanı | İnce ayarlı modelin kendisi + kanonik system prompt (K19) | ◐ |
| Risk değerlendirme / koordinatör ajan | Teslim notu: kriz tespiti yalnız modele bırakılmamalı, ayrı güvenlik katmanı gerekli | ✅ not hazır |
| Ajanlar < 1 sn | Gecikme ölçümü ve düşünme kısaltma bulguları | ◐ |

## 4. Rapora girmesi önerilen şekiller

Hepsi `scripts/analiz/` betikleriyle, girdi SHA'sı başlıkta (Kural 7).

1. İP1–İP2 boru hattı (tohum → üretim → kapılar → judge → sürüm → LoRA → 5 eksen) — formdaki Şekil 1'in gerçekleşen hâli
2. Model merdiveni (K29)
3. Senaryo ve bağımlılık türü dağılımı (`v0.1.0`)
4. Veri sürümlerinin gelişimi (`v0.0.1` → `v0.1.1` → ölçek-5k)
5. Uzman ↔ judge uyumu
6. Doz-yanıt / ölçekleme eğrisi
7. Taban ↔ ince model karşılaştırması (insan + judge)
8. Kriz yönlendirmesi gerilemesi (15 risk öğesi)
9. Düşünme uzunluğu ve gecikme ilişkisi

## 5. Rapordan önce kapatılması gereken eksikler

- [x] PII tarama, senaryo uyumu %, dil modeli uyumu % → `reports/analiz/2026-10-20-ip1-olcutler.md`
      (desen taşımayan %100 · kapı geçme %93,5 · kanonik senaryo %90,8 · şablon uyumu %100)
- [x] İP2 doğruluk vekili, zararlı yanıt, Türkçe oranı → `reports/analiz/2026-10-20-ip2-olcutler.md`
- [ ] BLEU/ROUGE/BERTScore — golden referanssız olduğu için ölçek-5k'dan referanslı set
      (`data/eval-ref/olcek5k-ref.v1.jsonl`) + `notebooks/rapor-bleu-gecikme.ipynb` → **Colab koşusu bekliyor**
- [ ] Tek istek gecikmesi (İP2 < 2 sn) → aynı defter → **Colab koşusu bekliyor**
- [ ] Duygu tonu etiketi: yapılacak mı, gerekçelendirilecek mi
- [ ] Rapor dönemi ayları ve tamamlanma yüzdeleri (yürütücü kararı)
