# Makale literatür taraması — `v0.1.1` yayın adayları

> **Amaç:** [makale-notlari.md](makale-notlari.md)'ndeki adaylar (A · B · C · §4 · §5) için
> atıf yapılabilecek kaynakları bulmak ve **her adayın özgünlük iddiasını daraltmak**.
> [ozgunluk-taramasi.md](ozgunluk-taramasi.md)'nın kuralı burada da geçerli: tarama iddiayı
> doğrulamak için değil, aksi çıkarsa aksini yazmak için yapıldı.
>
> **Tarama tarihi:** 2026-09-29 · **Tarayan:** Claude Code + dört paralel alt ajan (kullanıcı
> isteğiyle web araması, Kural 1) · Kayıt: `PROJECT_MEMORY.md` K278 · `katki-defteri.md` T309
> · Kaynakça: [kaynakca.bib](kaynakca.bib) §«2026-09-29 makale taraması» (**134 yeni kayıt**)

---

## ⛔ Bu taramanın sınırı — önce okunmalı

| | |
|---|---|
| ⛔ **Sistematik derleme değil** | dört konu kümesi, ~70 web sorgusu; PRISMA yok. «Bulamadık» ≠ «yok» |
| ⛔ **Yalnız özet düzeyi** | sayıların ve iddiaların neredeyse hepsi kaynağın **özetinden** (abstract). Bölüm düzeyinde iddia kurmadan önce PDF okunmalı |
| ⚠️ **2026 ön baskıları hakemsiz** | 2026 arXiv kayıtlarının çoğu hakemden geçmedi, birkaçı tek yazarlı. Ana argüman kanonik kaynaklara dayanmalı; bunlar «güncel / destekleyici» |
| ⚠️ **Alt ajan taraması** | kaynakları alt ajanlar açtı. Claude Code, **tehdit taşıyan 8 kaynağı** kendisi yeniden açtı (§0); geri kalanın doğrulaması ajan beyanı |
| ⚠️ **TR Dizin / YÖK Tez yine taranmadı** | E37'deki nedenle (üniversite erişimi) |

**Doğrulama düzeyi:** ✅ kaynağın kendi sayfası açıldı (arXiv abs · ACL Anthology · yayıncı · proceedings · GitHub/resmî doküman) ·
◐ yalnız DOI/indeks kaydı (Crossref · Europe PMC; yayıncı 403/CAPTCHA) · ◌ yalnız künye, **içerik iddiası kurulamaz**.
Bib kayıtlarının `note` alanında aynı işaret var.

### §0 — Claude Code'un bağımsız yeniden okuması (K260 deseni)

Tehdit taşıyan ya da iddiayı en çok daraltan kaynaklar alt ajan beyanına bırakılmadı, sayfası yeniden açıldı:

| kaynak | kontrol edilen | sonuç |
|---|---|---|
| Lee ve ark. 2026 · arXiv:2607.14552 | başlık · 7 yazar · 16 Tem 2026 · ~27 puan kayıp | ✅ birebir |
| MIThinker · arXiv:2606.29265 | *«gözlenen yanıtlardan danışman düşüncesini tersine mühendislik»* · Findings ACL 2026 | ✅ birebir |
| Peng ve ark. 2026 · arXiv:2602.14469 | ICML 2026 · üç ölçü · SSR · 10 puana kadar | ✅ birebir |
| CHARP · 2024.findings-acl.90 | FaithDial değerlendirmesi konuşma geçmişini hesaba katmıyor | ✅ birebir |
| Vachhani ve ark. 2026 · arXiv:2604.14829 | sözcüksel tanımda %35 → çıkarımlı tanımda %9 | ✅ birebir |
| Camassa & Shiller 2026 · arXiv:2605.20382 | 13 model · 16 talimat · 50 tur · %1–%99 · Sci-FM @ COLM 2026 | ✅ birebir |
| Karakaş & Şimşek 2026 · 2026.cmcl-1.25 | insanlar yüksek güvende -DI, düşükte -mIş; LLM'lerde etki kararsız, sık sık ters | ✅ — ⚠️ ajanın *«belirgin biçimde geri kalıyor»* ifadesi özette yok; özet *«kararsız, çoğu zaman ters»* diyor. Böyle yazılmalı |
| MLX `AdamW` dokümanı | imza `bias_correction: bool = False`, *«Default: False»* | ✅ birebir |

---

## Özet — adayların iddiaları nasıl değişti

| aday | iddia | tarama sonucu | yeni ifade |
|---|---|---|---|
| **A** | kararları koruyarak düşünmeyi yeniden kurmak | ◐ **daraldı** — *cevaba koşullu gerekçe üretimi* yeni değil (STaR, MIThinker, C3oT, PART, Peng 2026). ⛔ **Yöntemsel risk bulundu:** Lee 2026 cevaba koşullu CoT'nin damıtmayı bozduğunu gösteriyor | «kayıtlı klinik kararları alt dizge ve bağımsız okuyucuyla denetlenen, **var olan** düşünmenin yerine konan yeniden kurma + etkisinin ön kayıtlı sınaması» |
| **B1** | rubriğin girdi tanımı sadık izi cezalandırabilir | ◐ **kısmen yeni** — «kaynak tanımı etiketi değiştirir» genel ilke olarak var (Ji 2023 §8.1 · Ding 2025 · Vachhani 2026 · CHARP) | «CHARP'ın dışlanan-bileşen körlüğünün **LLM-yargıç rubriği** düzeyindeki, ölçülmüş bir alt türü» |
| **B2** | aynı metne zıt sert-kapı hükmü | ⛔ **tek başına özgün değil** — rater-içi tutarsızlık iyi belgelenmiş (Reiss 2023 · Haldar 2025 · Tamba 2026) | vaka örneği; katkı ancak gürültü tabanı deneyiyle |
| **B4** | sınıflandırıcı kesintisi denetimi bozuyor | ◐ **olgu bilinen** (XSTest · OR-Bench · SafeConstellations); ruh sağlığı denetim hattında **ölçülmüş oran bulunamadı** | operasyonel gözlem |
| **C** | çok belgeli talimatta çatışan tanım; örnek kuralı ezdi | ◐ **parçalar var, bileşim bulunamadı** — en yakın Camassa & Shiller 2026 | «bilinen örnek–talimat çatışmasının çok belgeli bir veri üretim hattındaki somut vakası» |
| **4.1** | yanlış veride koşup başarı bildiren denetimler | ⛔ **ders kitabı** (Sculley 2015 · Breck 2017 · Polyzotis 2019) | vaka kaydı; katkı değil |
| **4.5** | MLX→PEFT'te *tek* kaçınılmaz sapma `bias_correction` | ⛔ **fazla güçlü** — sayısal/donanım kaynaklı sapma ayrıca var (Yuan 2025 · Pham 2020) | «**yapılandırma düzeyindeki** tek kaçınılmaz sapma» |
| **4.7** | -mIş kanıtsallığı ve denetçi | ⭐ **doğrudan destek + uyarı** — Karakaş & Şimşek 2026 | tekil gözlem, LLM'lerin -mIş duyarlılığının kararsızlığıyla birlikte |

---

## 1. Aday A — muhakemeyi kararları koruyarak yeniden kurmak

### 1.1 ⛔ En yakın öncüller — makalede açıkça anılmalı

| kaynak | ne yapıyor | bizden farkı | doğr. |
|---|---|---|---|
| **zelikman2022star** — STaR, NeurIPS 2022, arXiv:2203.14465 | yanlış cevapta doğru cevabı verip gerekçeyi yeniden ürettiriyor (*rationalization*) | amaç doğruluk; var olan gerekçenin yerine koyma, karar korunumu, şablon kırma yok | ✅ |
| **yang2026mithinker** — MIThinker, Findings ACL 2026, arXiv:2606.29265 | **motivasyonel görüşmede** gözlenen danışman yanıtlarından danışman düşüncesini tersine mühendislikle çıkarıp SFT+RL | ⭐ **alan içindeki en yakın öncül.** Farkımız: var olan düşünme alanının yerine koyma · kararların alt dizge + bağımsız okuyucuyla denetimi · şablon kırma hedefi · 8 tohumlu ön kayıtlı kıyas | ✅ (§0) |
| **kang2025c3ot** — C3oT, AAAI 2025, arXiv:2412.11664 | var olan CoT'yi bir LLM ile yeniden yazıp eğitiyor | hedef uzunluk | ✅ |
| **ding2025part** — arXiv:2510.11545 | izleri bilgiyi koruyarak yeniden biçimlendiriyor; öğrenci başarısı düşüyor (AIME24 54,17 → 46,88, özet) | amaç tersi (damıtmayı bozmak) — ama **biçim değişiminin tek başına öğrenciyi etkilediğinin kanıtı** | ✅ |
| **peng2026posthoc** — ICML 2026, arXiv:2602.14469 | cevaptan geriye CoT üretiminde cevaba bağımlılığı üç düzeyde ölçüyor; iskelet-güdümlü üretim | alan genel/matematik; klinik karar korunumu yok. Ölçüleri bizim benzerlik kapımıza yakın | ✅ (§0) |
| **wiegreffe2022reframing** — NAACL 2022 | sabit etiketlere GPT-3 açıklaması + insan süzgeci | eğitim verisindeki muhakemeyi değiştirmiyor | ✅ |
| **chen2025psyinsight** — arXiv:2503.03607 | gerçek danışmanlık diyaloglarına tur düzeyinde gerekçe ekliyor | yeniden yazım ve karar denetimi yok | ✅ |

### 1.2 ⛔⛔ Yöntemsel risk — sınırlılık olarak yazılmalı

**lee2026answerconditioned** (arXiv:2607.14552, ✅ §0): doğru cevap gösterilerek yazdırılan CoT'lerle ince ayar
doğrulanabilir muhakemeyi bozuyor (en zor sorularda ~27 puan, özet); doğruluk süzgeci bunu yakalamıyor; model
cevaptan geriye gerekçelendiriyor. **Bizim yeniden kurmamız tanım gereği cevaba ve kararlara koşullu.**

Savunma çizgisi (makalede): (i) alanımızda doğrulanabilir bir «doğru cevap» yok; düşünmenin işlevi kararın
gerekçesi olmak ve karar korunumu hedefin kendisi; (ii) ölçtüğümüz şey doğruluk değil üslup/şablon aktarımı.
⚠️ Ama bu bir **savunma**, bir **ölçüm** değil. Faz 4'te eğitilen modelde düşünmenin cevaptan geriye
gerekçelendirme belirtisi (Peng 2026'nın ölçüleri) ayrıca bakılabilir — **ön kayıtta yok**, eklenirse EK olarak.

### 1.3 Hipotezi destekleyenler — düşünmenin üslubu SFT ile modele geçer

| kaynak | bulgu (özet) | doğr. |
|---|---|---|
| **lippmann2025style** — COLM 2025 | damıtılmış modeller muhakemeyi büyük ölçüde üslup kalıplarını taklit ederek ediniyor | ✅ |
| **li2025structure** — arXiv:2502.07374 | yanlış örnekler doğruluğu yalnız %3,2 düşürüyor; adım sırasını bozmak belirgin kayıp ⇒ yapı içerikten önemli | ✅ |
| **ding2025part** | yukarıda — biçim değişimi öğrenciyi etkiliyor | ✅ |
| **zhou2023lima** · **ye2025limo** · **muennighoff2025s1** | ~1000 örnek biçim ve «bilişsel şablon» aktarıyor | ✅ |

⭐ Bunlar EK-1'in kazanç şartının (B1 ↓ ∧ B2 ↓) **öncül gerekçesi**: veri düzeyindeki şablon azalmasının
modele geçmesini beklemek için literatür nedeni var.

### 1.4 CoT sadakati — düşünme alanını kararın güvenilir kaydı saymamak için

**lanham2023measuring** (arXiv:2307.13702) · **chen2025reasoning** (arXiv:2505.05410; kullanılan ipuçları %20'den az dile getiriliyor) ·
**arcuschin2025wild** (arXiv:2503.08679; üretim modellerinde örtük sonradan gerekçelendirme %13'e kadar) ·
**jacovi2020faithfully** (ACL 2020) — hepsi ✅. `turpin2023unfaithful` zaten bib'de.

### 1.5 Alan — ruh sağlığı / danışmanlık için sentetik ya da muhakemeli veri

**qiu2024smile** (SMILE, Findings EMNLP 2024) · **lee2024cactus** (Findings EMNLP 2024) · **sun2021psyqa** (Findings ACL 2021) ·
**yang2024mentallama** (WWW 2024) · **hu2025beyondempathy** (arXiv:2505.15715) · **zheng2026mocc** (arXiv:2609.17180; muhakeme–yanıt
tutarlılığı ödül olarak — bizim `tutarsizlik` kapımızın RL karşılığı) · **guan2024deliberative** · **wang2025star1** · **steenstra2024alcohol**
(alkol kullanımı için LLM-MI ajanı) · **basar2025reflect** (COLING 2025; MI yansıtmalarının insan değerlendirmesi) — hepsi ✅.

⚠️ hu2025beyondempathy için arama özetinde geçen *19.302 diyalog* sayısı kaynağın özetinde **yok** — kullanılmaz.

### 1.6 Ön kayıt ve negatif sonuç

**vanmiltenburg2021preregistering** (NAACL 2021) ✅ · **sogaard2023twosided** (EACL 2023; ön kaydın zayıf yanları — EK-1/EK-2 tartışması için) ✅ ·
**nosek2018preregistration** (PNAS) ◐ · **karl2024negative** (ICML 2024 pozisyon; negatif sonuç yayını — *170 beklendi, 9 değişti*) ✅.

---

## 2. Aday B — LLM denetçinin güvenilirliği

### 2.1 Bulgu 1 (rubrik girdi tanımı) — en yakın öncüller

| kaynak | ne gösteriyor | tehdit | doğr. |
|---|---|---|---|
| **ghaddar2024charp** — CHARP, Findings ACL 2024 | FaithDial değerlendirmesi **konuşma geçmişini** hesaba katmıyor ⇒ değerlendirme sistematik olarak kör | ◐ **en ciddi aday.** Dışlanan bileşen orada önceki turlar, bizde **bu turun cevabı**; etki orada model/metrikte, bizde LLM denetçinin sert-kapı hükmünde; bizde denetçiler boşluğu **kendileri** işaretledi ve düzeltme ölçüldü (2 red → kabul) | ✅ (§0) |
| **vachhani2026soap** — arXiv:2604.14829 | tıbbi SOAP notunda halüsinasyon tanımı sözcüksel → çıkarımlı olunca oran %35 → %9 | ◐ «tanım değişince uydurma oranı değişir» sayısal olarak var; ekseni **çıkarım toleransı**, bizimki **girdi alanı kapsamı**. Hakemsiz | ✅ (§0) |
| **ding2025grayzone** — arXiv:2510.21118 | kaynak sınırı kötü tanımlanınca sadakat etiketleri belirsizleşiyor; ~%9 gri bölge | ◐ bizde sınır belirsiz değil, **yanlış çizilmiş** | ✅ |
| **ji2023survey** — ACM CSUR 55(12) | §2.1 içsel/dışsal; §8.1 diyalogda kaynak = diyalog geçmişi ve/veya dış bilgi | ◐ kaynak göreve göre tanımlanır — bilinen ilke | ✅ |
| **huang2025survey** — ACM TOIS | §2.3.2 sadakat halüsinasyonunun bir türü **akıl yürütme adımları ↔ nihai cevap** tutarsızlığı | ⭐ **v2'yi doğrudan meşrulaştırıyor**: bir iz için doğru kaynak konuşma **+ cevap** | ✅ |
| **shankar2024validators** — UIST 2024 | *criteria drift*: bazı ölçütler ancak çıktılar görülünce ortaya çıkar | hayır — boşluğun okuma sırasında fark edilmesini çerçeveliyor | ✅ |
| **maynez2020faithfulness** · **cao2022hallucinated** · **dziri2022begin/faithdial/origin** · **zhang2023siren** · **venkit2024audit** · **zhang2026averaging** | kaynak tanımı ve halüsinasyon etiketinin kuruluşu | hayır/kısmen | ✅ |

**Bulunamayan (Bulgu 1'in ayakta kalan kısmı):** rubriğin girdiyi adlandırılmış alanlara bölüp sert kapıyı yalnız birine
bağlaması yüzünden **kendi cevabına sadık bir izin elenmesi**; denetçilerin bunu kendiliğinden yazması; tek değişkenli
v1→v2 düzeltmesinin karar etkisinin raporlanması. ⇒ Önerilen konum: *«Ji/Huang'ın kaynak tanımı + CHARP'ın körlüğü,
LLM-rubrik düzeyinde»*; Vachhani ve Ding en yakın öncüller olarak anılır.

### 2.2 Bulgu 2 (aynı metin, zıt hüküm) — öncüller

**reiss2023testing** (aynı girdi, farklı çıktı) · **haldar2025rating** (EMNLP 2025; rater-içi güvenilirlik düşük) ·
**yagubyan2026coinflip** (arXiv:2606.13685; ikili tercihlerin %13,6'sı dönüyor — ⚠️ gönderim tarihi sayfadan yeniden kontrol edilmeli) ·
**tamba2026temperature** (arXiv:2606.26185; sıcaklık 0'da da sınır maddelerin bir kısmı tekrarlanamıyor; özet bazı Claude sürümlerinde
sıcaklık parametresinin kaldırıldığını söylüyor — alt ajan denetçimizde sıcaklık zaten kontrol edilemiyor) ·
**guerdan2025indeterminacy** (NeurIPS 2025; belirsiz ölçütte zorunlu tek seçim yanlı) · **wang2024notfair** · **zheng2023judging** — hepsi ✅.
⇒ Bulgu 2 **tek başına katkı değil**; gürültü tabanı deneyinin gerekçesi.

### 2.3 Gürültü tabanı deneyinin tasarımı için

| kaynak | tasarıma etkisi | doğr. |
|---|---|---|
| **norman2026reliability** — arXiv:2606.19544 | ham uyuşma κ'ya göre 33–41 puan şişiyor (MT-Bench) ⇒ **κ birincil ölçü** | ✅ |
| **hayes2007krippendorff** | α eksik veriyi tolere eder ⇒ sınıflandırıcı kesintisi için **α ikincil ölçü** (bu özellik kaynağın sayfasından ayrıca doğrulanmadı) | ◐ |
| **cohen1960kappa** ◐ · **artstein2008intercoder** ✅ | κ/α seçimi ve yorumu | |
| **bellibatlu2026judgesense** — arXiv:2604.23478 | ⚠️ **ajan sistemleri içindeki yargıçlar kendileriyle doğrudan API'den daha az uyuşuyor** — denetçimiz alt ajan | ✅ |
| **bagaria2026rubric** (EMNLP 2026) · **huynh2026rubric** · **thakur2025judging** · **young2026faithfulness** (aynı CoT verisinde üç sınıflandırıcı, κ 0,06–0,42) | rubrik metninin ve ölçüm aracının hükme etkisi | ✅ |
| **gilardi2023chatgpt** · **tornberg2023chatgpt4** · **bavaresco2025llms** · **gu2024survey** · **liu2023geval** | LLM açıklayıcı uyumu, karşı-anlatı | ✅ |

### 2.4 Bulgu 4 (sınıflandırıcı kesintisi)

**rottger2024xstest** · **cui2025orbench** · **zhang2025falsereject** · **maskey2026safeconstellations** (ACL 2026; tekrarlı istemli görevlerde
aşırı ret) · **im2026falserefusal** · **chu2026harmful** (karşıt bakış) — hepsi ✅. ⭐ **Ruh sağlığı/bağımlılık içeriğinin LLM denetim
hattında güvenlik sınıflandırıcısınca bloklanmasını ölçen hakemli bir çalışma bulunamadı.**

---

## 3. Aday C — çatışan talimat tanımları

| kaynak | ne gösteriyor | tehdit | doğr. |
|---|---|---|---|
| **camassa2026doasisay** — Sci-FM @ COLM 2026 (poster), arXiv:2605.20382 | açık talimat ↔ gösterilmiş asistan örüntüsü; 13 modelde talimata uyma %1–%99, genel ölçütlerle ilişkisiz | ◐ **en yakın.** Orada tek konuşma, çok sayıda tekrarlı örnek (50 tura kadar); bizde **tek bir çözümlü örnek aynı belgedeki sert kuralı** ezdi ve bu bir veri üretim hattında oldu. Çalıştay posteri | ✅ (§0) |
| **geng2026control** — AAAI 2026 | basit biçim çatışmalarında bile tutarlı öncelik yok | ◐ ⇒ bizim «kapı sırası yazıldı» düzeltmemiz **gözlenen etki** olarak sunulmalı, genel çözüm olarak değil | ✅ |
| **wallace2024instruction** · **zhang2025iheval** (en iyi açık model çatışmaların %48'ini çözüyor) · **he2026coninstruct** (modeller çatışmayı tespit ediyor ama nadiren bildiriyor — alt ajanların sessizce bir yöne çözmesine paralel) | talimat hiyerarşisi ve çatışma | kısmen/hayır | ✅ |
| **min2022rethinking** · **wei2023larger** · **webson2022prompt** | örneğin biçimi içerikten güçlü; talimatın anlamı zayıf belirleyici | hayır | ✅ |
| **yang2025underspecification** | gereksinimleri listelemek güvenilir iyileşme getirmiyor, gereksinimler çelişebiliyor | kısmen | ✅ |
| **cemri2025mast** — arXiv:2503.13657 | çok ajanlı LLM hata taksonomisi; FM-1.1 görev tanımına uymama %11,8 (Ek A) | kısmen | ✅ |
| **nuseibeh2000leveraging** · **nuseibeh2001making** | yazılım mühendisliğinde tutarsızlık yönetimi (klasik) | — | ◌ yalnız künye |

**Bulunamayan:** LLM veri üretim hattında aynı yetkideki birden çok belge arasında çelişki + tanım belgesinin tek örneğinin
kendi sert kuralını ihlal etmesi + kayıtlara ölçülebilir yansıması + kapı sırasıyla düzeltme. ⇒ *«bulamadık»* denir, *«kimse yapmadı»* denmez.

---

## 4. Destekleyici notlar

### 4.1 Sessiz hatalar — ⛔ ders kitabı, katkı değil

**sculley2015hidden** (NIPS 2015) · **breck2017mltestscore** (IEEE BigData 2017; 28 test) · **polyzotis2019datavalidation**
(MLSys 2019 — ⚠️ yaygın «Breck ve ark. 2019» künyesi yanlış, ilk yazar Polyzotis) · **polyzotis2018lifecycle** ·
**schelter2018automating** (PVLDB; «veri için birim testleri» — *boş girdide assert* ilkemizin hafif karşılığı; 6 yazar) ·
**tambon2021silent** («sessiz hata» tanımı) · **wu2026narratives** (arXiv:2606.14589; üretim LLM ajanında sessiz hataların ~%70'ini
insan gözlemi yakaladı, 4.286 birim testine rağmen — hakemsiz, tek yazar) · **cemri2025mast** FM-3.2/3.3 — hepsi ✅/◐.
`barr2015oracle` (test oracle) ve `sambasivan2021cascades` zaten bib'de. ⇒ 4.1'in beş vakası **bu literatürün LLM veri hattında
yeniden yaşandığının kaydı** olarak yazılır.

### 4.3–4.4 Ön kayıt ve güç

**card2020little** (EMNLP 2020; MDE hesabımızın doğrudan gerekçesi) · **dror2018hitchhiker** · **dror2019deep** (skor dağılımı üzerinden
kıyas, ASD — 8 tohumluk kollar için) · **reimers2017reporting** · **dodge2019show** · **lipton2019troubling** (kazancın kaynağını gizleme —
kazanç şartını önceden kaydetmenin gerekçesi) · **kapoor2023leakage** · **ulmer2022experimental** — hepsi ✅/◐.
`bouthillier2021variance` ve `bui2025seeds` zaten bib'de.

### 4.5 MLX → PEFT/Unsloth — ⛔ iddia daraltılmalı

| kaynak | etkisi | doğr. |
|---|---|---|
| **mlx2023** + MLX `AdamW` dokümanı | `bias_correction` varsayılanı **False** — iddiamızı destekliyor | ✅ (§0) |
| **kingma2015adam** · **loshchilov2019adamw** · PyTorch `AdamW` dokümanı | torch'ta bias düzeltmesi koşulsuz | ✅ |
| **hu2022lora** · **peft** (doküman: dize listesi tam eşleşme **ya da sonek** ile eşlenir ⇒ `['q_proj','o_proj']`'nin görü kulesine de gitmesinin resmî açıklaması) · **unsloth** (`finetune_vision_layers` varsayılan açık) | 4.5'in tuzağını belgeli kılıyor | ✅ |
| **kalajdzievski2023rslora** | `lora_alpha` 160 ↔ `scale` 20 eşlemesi yalnız `use_rslora=False` iken doğru — makalede yazılmalı | ✅ |
| ⛔ **yuan2025nondeterminism** · **pham2020variance** (ASE 2020) · **dodge2020finetuning** | donanım/çekirdek/kayan nokta ve RNG farkları tek başına sapma üretir ⇒ *«tek kaçınılmaz sapma»* **yanlış genelleme** | ✅ / ◐ |
| **biderman2024lora** (TMLR) · **chen2026lrscaling** · **zhang2026scaling** | α/r ve hedef modül seçimi sonuca birinci derece etkili; yalnız dikkat modüllerini hedeflemek literatürde zayıf | ✅ |

⇒ Yeni ifade: *«yapılandırma düzeyinde birebir aktarılamayan tek şey `bias_correction`; sayısal eşdeğerlik zaten beklenmez — EK-2'nin
iki kolu aynı ortamda koşturmasının nedeni bu.»* q/o hedefleme ve α = 20·r **bir tasarım tercihi** (e3 ile karşılaştırılabilirlik), optimum değil.
`dettmers2023qlora` bib'e eklendi ama bizim defterimiz 4-bit kullanmıyor (bf16) ⇒ tehdit değil.

### 4.7 Türkçe kanıtsallık

**aksukoc1988acquisition** (Cambridge UP) ✅ · **slobin1982evidential** ◐ · **aikhenvald2004evidentiality** ◐ · **johanson2000evidentials** ◐ ·
**goksel2005turkish** ◐ — ◐ olanlara **yalnız genel atıf** (metinlerine erişilmedi).
⭐ **karakas-simsek-2026-benchmarking** (CMCL 2026, ✅ §0): insanlar yüksek güvende -DI, düşük güvende -mIş seçiyor; 10 LLM'de bu etki
model ve isteme bağlı, kararsız, çoğu zaman ters. ⇒ #0906 vakasını destekliyor **ve** bir uyarı taşıyor: LLM denetçinin -mIş'e dayalı
çıkarımı güvenilir biçimde ayırt ettiği varsayılamaz. **kwon2026factwash** (arXiv:2608.03372; İngilizcede «duyumu olguya çeviren yeniden
yazımlar» — bizim *çıkarımı olgu gibi kurma* hatamızın karşılığı, hakemsiz) · **zhou-etal-2024-relying** (ACL 2024) ✅.

---

## 5. Beyan zorunlulukları — raporlama kılavuzları

| kaynak | bizim için | doğr. |
|---|---|---|
| ⛔ **gallifant2025tripodllm** — TRIPOD-LLM, Nat Med 2025 | madde 5a (eğitim/ayar/değerlendirme verisinin kaynakları ayrı) · 7d (öznel sonuçlarda değerlendirenin niteliği) · **13 (etik kurul adı ya da muafiyet)** ⇒ etik kurul kaydının yokluğu ve 40 pilot kaydın okunmaması kılavuza göre **raporlanması zorunlu açıklar** | ✅ (PMC) |
| **chart2025** — CHART, BJS 2025 | model kimliği, istem mühendisliği, sorgu stratejisi raporlama şablonu | ✅ |
| **vasey2022decideai** · **liu2020consortai** | çalışmanın klinik değerlendirme aşamasına **geçmediğini** söylemek için | ◐ |
| **stade2024behavioral** · **lawrence2024opportunities** · **who2024lmm** | ruh sağlığında LLM etiği; klinik uzman onayının yokluğu bu çerçevelerin gerisinde (⚠️ Stade/Lawrence ilk adları doğrulanmadı; WHO sayfası 25 Mart 2025 tarihli) | ◐ / ✅ |
| **gebru2021datasheets** · **bender-friedman-2018-data** · **liu2024synthetic** | *206/1039 taslağı Claude Code yazdı* bilgisi datasheet'in «toplama süreci» bölümüne girer | ✅ |
| ⛔ **panickssery2024self** (zaten bib'de) · **zheng2023judging** | denetçiler aynı model ailesinden ⇒ öz-kayırma yanlılığı; §5'te **atıfla** yazılmalı | ✅ |
| **shumailov2024collapse** — Nature 2024 | tek kuşaklı damıtma, özyineleme yok; yalnız kuyruk vakalarının (kriz dilimi) temsil riski için | ◐ |

---

## 6. Doğrulanamayanlar — atıf yapılmaz

- *Benchmarking Motivational Interviewing Competence of LLMs* (PMC13472593): LLM'lerin yansıtma/soru oranının uzman eşiğinin altında
  kaldığı iddiası (~1,2 ↔ >2,8) **yalnız arama özetinde**. Aday A'nın *«her cevap soruyla bitiyor»* gözlemi için değerli olurdu — sayfası açılamadı.
- MI alanında açılamayanlar: PMC13010193 · PMC13293567 · 2024.hucllm-1.4.
- *Beyond the Single Turn: Reframing Refusals…* (arXiv:2602.01694; ruh sağlığı desteğinde ret) — B4 için bakmaya değer, açılmadı.
- Görülüp açılmayanlar: arXiv:2605.21127 · 2509.22230 · 2510.25860 · 2512.00831 · 2503.13509 (MentalChat16K) · 2406.07070 (HalluDial) ·
  2503.09347 · 2601.03269 · 2502.12197 · 2602.04294 · Anil ve ark. 2024 (many-shot jailbreaking).
- Künye ayrıntıları doğrulanmayanlar: Huang 2025 TOIS cilt/sayı · LIMA'nın NeurIPS 2023 venue'su · STAR-1'in AAAI 2026 venue'su ·
  Tambon'un dergi sürümü · Haldar 2025'in main/Findings ayrımı · Adam'daki bias-correction bölüm numarası.
- ⭐ Açıldı ama zayıf ilgili olduğu için eklenmedi: Sunkavalli 2026 ön kayıtlı yargıç denetimi (arXiv:2608.29517) — **gürültü tabanı deneyi
  tasarlanırken yeniden bakılmalı.**

## 7. Arama sorguları

Dört küme, ~70 sorgu; tam liste alt ajan raporlarında (oturum dökümü). Temsilî örnekler — «bulunamadı» hükümlerinin dayandığı sorgular:

- A: *rewriting chain-of-thought rationales training data while keeping answers fixed* · *revising reasoning traces of SFT data with LLM editor holding responses constant* · *infer counselor internal thoughts from existing counseling responses*
- B: *hallucination evaluation "what counts as source" dialogue* · *LLM judge context omission false positive hallucination flags* · *reasoning trace hallucination detection grounded in question and final answer*
- C: *LLM prompt worked example contradicts rule model follows example instead of rule* · *demonstrations contradict instruction LLM prioritize examples*
- B4: *LLM annotator refusals mental health annotation* · *LLM safety filter blocks classification of harmful content annotation pipeline*
