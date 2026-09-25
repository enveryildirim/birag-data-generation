# Benzer çalışmalar — Türkçe ruh sağlığı ve bağımlılık NLP'si

> **Amaç:** tezin *«bilgiye katkı»* iddiasının dayanacağı boşluk tespiti (T1).
> Proje raporu bu bölümü atlayabilir, tez atlayamaz (`tez-plani.md` §1).
>
> **Tarama tarihi:** 2026-09-16 · **Tarayan:** Claude Code (kullanıcı onayıyla, Kural 1)
> · Kayıt: `PROJECT_MEMORY.md` K140 · `katki-defteri.md` T1

---

## ⛔ Bu belgenin sınırı — önce okunmalı

Bu **birinci tur** bir taramadır ve şunları **yapmaz**:

| | |
|---|---|
| ⛔ **Kapsamlı değil** | sistematik derleme protokolü (PRISMA vb.) uygulanmadı; arama motoru sonuçlarından yüründü |
| ⛔ **Türkçe dizinler eksik** | TR Dizin, YÖK Tez, ULAKBİM tam taranmadı — üniversite ağı gerektiriyor |
| ⛔ **Yayımlanmamış tez ve proje çıktıları yok** | BıRAG'ın kendi İP ortaklarının önceki işleri dahil |
| ⚠️ **«Bulunamadı» ≠ «yok»** | negatif bulgular **aranan sorgularla birlikte** yazıldı ki okuyucu neyin arandığını görsün |

⭐ **Doğrulama kuralı:** her atıf **çözülebilir bir kimlikle** (arXiv ID · DOI · dergi
cilt/sayı) yazıldı ve kaynağın kendisinden doğrulandı. Arama motorunun özetinde
geçip kaynağında doğrulayamadığım **hiçbir sayı bu belgeye girmedi** — doğrulanan
sayılar aşağıda açıkça işaretli.

---

## 1. Türkçe genel LLM altyapısı — ruh sağlığı bileşeni **yok**

Türkçe için genel amaçlı model ve ölçüt altyapısı son iki yılda belirgin biçimde
gelişti. ⛔ Ama hiçbiri ruh sağlığı ya da bağımlılık boyutu taşımıyor.

| Çalışma | Ne | Ruh sağlığı bileşeni |
|---|---|---|
| **Cetvel** (Er, Kesen, Şahin, Erdem · arXiv:2508.16431, 2025) | Türkçe için birleşik LLM ölçütü; **23 görev, yedi kategori** ✅*doğrulandı* | ⛔ **yok** — dilbilgisi düzeltme, çeviri, kültürel bilgi; tıbbi/psikiyatrik görev bulunmuyor ✅*doğrulandı* |
| **TURNA** (Türkçe encoder-decoder temel model) | Türkçe anlama + üretim | ⛔ yok |
| **Kanarya**, **Trendyol-LLM**, **cosmosGPT** (arXiv:2404.17336) | Türkçe merkezli önseğitim / yönerge ayarı | ⛔ yok |

➡️ **Birinci boşluk:** Türkçe'nin en kapsamlı LLM ölçütü (Cetvel) ruh sağlığı
ekseni **içermiyor**. Bir Türkçe terapötik modelin başarısı bugün Türkçe genel
ölçütlerle **ölçülemez**.

---

## 2. Türkçe tıp/klinik NLP — var, ama ruh sağlığı değil

| Çalışma | Ne | Not |
|---|---|---|
| **TurkMedNLI** (Oğul, Soygazi, Ergenç Bostanoğlu · PeerJ CS, 2025 · DOI 10.7717/peerj-cs.2662) | MedNLI'ın LLM tabanlı çeviriyle Türkçeye aktarımı; Türkçe tıbbi çıkarım veri seti | ⚠️ **çeviri kökenli** — K90'ın çeviri kusuru bulgusuyla doğrudan ilgili |
| **Türkçe tıbbi LLM** (ACM TALLIP, 2025 · DOI 10.1145/3772000) | 167.732 gerçek hasta-hekim soru-cevabıyla ince ayar | ⚠️ genel tıp; bağımlılık/ruh sağlığı dilimi bildirilmiyor |
| **TUS değerlendirmesi** (BMC Med Educ, 2025 · DOI 10.1186/s12909-025-07148-0) | Dört LLM'in Tıpta Uzmanlık Sınavı başarımı | ⛔ **sınav bilgisi ölçüyor**, terapötik davranış değil |

➡️ **İkinci boşluk:** Türkçe tıp NLP'si **bilgi doğruluğu** ekseninde ilerliyor.
BıRAG'ın ölçtüğü şey (rol sınırı, boş güvence, etiketleme, suçlama, kriz
yönlendirmesi) **davranış** ekseni ve bu eksende Türkçe bir çalışma bulunamadı.

---

## 3. ⭐ Çok dilli ruh sağlığı NLP'sinde Türkçe — ölçülmüş ve **en kötü**

**Skianis, Pavlopoulos, Doğruöz** — *Building Multilingual Datasets for Predicting
Mental Health Severity through LLMs: Prospects and Challenges* · arXiv:2409.17397
(25 Eylül 2024). Altı dil: Yunanca, **Türkçe**, Fransızca, Portekizce, Almanca, Fince.

| Görev | Türkçe başarım (GPT-3.5, 0-shot) | ✅ |
|---|---|---|
| Depresyon şiddeti (`Dep-Severity`) | Makro F1 **0,11** | *doğrulandı (Tablo 3)* |
| İntihar düşüncesi (`Sui-Twi`) | Makro F1 **0,35** | *doğrulandı (Tablo 4)* |

⛔ Çalışmanın kendi saptaması: **Türkçeye çeviri her iki görevde de en kötü
başarımı veriyor** ve bunu Türkçe sağlık — özellikle ruh sağlığı — kaynaklarının
kıtlığına bağlıyor.

➡️ **Üçüncü boşluk ve bu tezin en doğrudan dayanağı:** Türkçe'nin ruh sağlığı
NLP'sindeki zayıflığı **varsayım değil, yayımlanmış ölçüm**. Ve o ölçüm bir
**çeviri** hattında yapıldı — yani boşluk *«Türkçe veri az»*tan daha dar:
**Türkçe'de yazılmış** ruh sağlığı verisi az.

---

## 4. Danışmanlık diyaloğu ve motivasyonel görüşme veri setleri — **hiçbiri Türkçe değil**

| Veri seti | Dil | Not |
|---|---|---|
| **AnnoMI** (Wu, Balloccu, Kumar, Helaoui, Reforgiato Recupero, Riboni · *Future Internet* 15(3):110, 2023; ilk sürüm IEEE ICASSP 2022) | İngilizce | **133 uzman-etiketli MI görüşmesi** (110 yüksek / 23 düşük kalite) ✅*doğrulandı* — MI kalitesini **etiketli** veren tek açık küme |
| **ESConv** | İngilizce | duygusal destek stratejileri etiketli |
| **PsyQA** | Çince | ruh sağlığı soru-cevap |
| **Psych8k / ChatCounselor** (arXiv:2309.15461) | İngilizce | lisanslı danışmanların ürettiği yönerge verisi |
| **MentalChat16K** (arXiv:2503.13509) | İngilizce | danışmanlık ölçütü |
| **CounseLLMe** | İngilizce/İtalyanca | LLM-LLM simüle diyalog |

⚠️ Bu satırların **sayıları** (AnnoMI dışında) kaynağından doğrulanmadı; dilleri
doğrulandı. Sayı gerekirse tek tek açılmalı.

➡️ **Dördüncü boşluk:** MI temelli, **uzman kalitesi etiketli** açık veri
İngilizce'de **tek** (AnnoMI) ve Türkçe'de **hiç yok**. BıRAG'ın üretim talimatı
MI (TIP 35) + EPITOME + Marlatt temelli — bu bileşimin Türkçe karşılığı bulunamadı.

---

## 5. Bağımlılık alanı + LLM — alan taze, uyarılar yayımlanmış

**Digital interventions for substance use disorders** derlemesi (*Current Opinion
in Psychiatry*, 2026 · DOI 10.1097/YCO.0000000000001088) LLM'lerin bağımlılık
alanındaki fırsat ve risklerini derliyor: erken tespit ve sürekli izleme fırsat
tarafında; **halüsinasyon, damgalamayı pekiştirme, güvensiz tavsiye** risk
tarafında. ⭐ Derlemenin sonucu doğrudan bu projenin Kural 3'üyle örtüşüyor:
güvenli kullanım **doğrulama, önyargı azaltma, şeffaf veri yönetişimi ve insan
denetimi** istiyor.

➡️ **Beşinci boşluk:** bağımlılık + LLM literatürü **klinik not** ve **tespit**
tarafında yoğunlaşıyor; *«model kullanıcıyla nasıl konuşmalı»* sorusu — yani
BıRAG'ın konusu — bu derlemelerde **açık kalem** olarak duruyor.

---

## 6. ⭐ Boşluk tespiti — bu tezin iddia edebileceği yer

| # | Boşluk | Dayanak |
|---|---|---|
| 1 | Türkçe LLM ölçütlerinde **ruh sağlığı ekseni yok** | Cetvel 23 görev, hiçbiri klinik ✅ |
| 2 | Türkçe tıp NLP'si **bilgi** ölçüyor, **davranış** ölçmüyor | TurkMedNLI · TALLIP · TUS |
| 3 | Türkçe ruh sağlığı başarımı **ölçülmüş ve en kötü** | arXiv:2409.17397, F1 0,11 / 0,35 ✅ |
| 4 | MI temelli uzman etiketli veri **Türkçe'de yok** | AnnoMI tek ve İngilizce ✅ |
| 5 | Bağımlılıkta LLM literatürü **konuşma davranışını** ölçmüyor | Curr Opin Psychiatry 2026 |
| 6 | ⚠️ **Türkçe bağımlılık NLP'si bulunamadı** | aşağıdaki sorgular; ⛔ *bulunamadı ≠ yok* |

**Sorgu 6 için aranan** (2026-09-16): *«Türkçe bağımlılık madde kullanımı doğal
dil işleme AMATEM yapay zeka çalışma»* · *«Turkish mental health chatbot Türkçe
psikolojik destek yapay zeka dil modeli veri seti»* · *«Turkish counseling
dialogue dataset LLM psychological support Turkish»*. Üçünde de Türkçe bağımlılık
alanına özgü bir veri seti ya da model **çıkmadı**.

---

## 7. ⛔ Sonraki tur — bu belge tamamlanmadı

- [ ] **TR Dizin · YÖK Ulusal Tez Merkezi · ULAKBİM** taraması (üniversite erişimi gerekir)
- [ ] **AMATEM/ÇEMATEM** klinik bilişim yayınları — Türkçe psikiyatri dergileri
- [ ] §4'teki sayıların kaynağından doğrulanması
- [ ] ⭐ **Ayrı bir boşluk sorusu, henüz aranmadı:** *kanıta bağlı LLM-judge rubriği*
      (alıntının kaynakta doğrulanması — bu projenin v7→v9 hattı) literatürde var mı?
      Bulunursa T43/T46/T51'in özgünlük iddiası daralır; bulunmazsa güçlenir.
      **Aranmadan iddia edilmemeli.**
- [ ] Danışman onayı: tezin literatür bölümünün kapsamı nereye kadar

---

## 8. ⭐⭐ İkinci tur — Türkçe kaynaklar (2026-09-22, T251 / §EK-5)

§7'nin ilk üç maddesi **kısmen** kapandı. Ayrıntı ve sorgular
[ozgunluk-taramasi.md](ozgunluk-taramasi.md) §EK-5'te.

### 8.1 ⭐⭐ Boşluk #2 artık ruh sağlığı alanında da DOĞRUDAN kanıtlı

✅ **Türk, M. N., Akın, R., Şahin, D. Ö., Demirci, S. — «Büyük Dil Modellerinin
Ruh Sağlığı Uygulamaları İçin Performans ve Tutarlılık Analizi», Black Sea
Journal of Engineering and Science, 9(3), Mayıs 2026,
DOI 10.34248/bsengineering.1913122** — kaynağından okundu.

Bulunan **ilk Türkçe LLM × ruh sağlığı** çalışması; dokuz model karşılaştırılmış.
⭐⭐ Üç niteliği tam boşluğu çiziyor:

| | |
|---|---|
| Veri | **İngilizce** Kaggle *Mental Health FAQ for Chatbot*; **Türkçe küme yok** |
| Alan | **bağımlılık yok** |
| Ölçülen | **bilgi ve tutarlılık** (COMET/METEOR), **davranış değil** |

➡️ §6'nın 2. boşluğu (*«Türkçe tıp NLP'si bilgi ölçüyor, davranış ölçmüyor»*)
artık **varsayım değil**: ruh sağlığı alanında yapılmış bir Türkçe çalışma da
bilgi ölçüyor, İngilizce veriyle, bağımlılık dışında.

### 8.2 ⭐ Türkçe LLM ekosistemi — ve klinik boşluk

⚠️ (dizin kayıtlarından) **Mukayese** (arXiv:2203.01215) · Türkçe dil modelleri
başarım karşılaştırması (arXiv:2404.17010) · Türkçe verisetleriyle eğitim ve
ince ayar (arXiv:2306.03978) · **TurkEmbed4Retrieval** (arXiv:2511.07595).
**Hiçbiri klinik değil** ⇒ §1'in Cetvel bulgusu ikinci bir kaynak kümesiyle
destekleniyor.

### 8.3 ⛔ Saldırgan dil tarafı BOŞ DEĞİL — ve bu bizim aleyhimize

**SemEval-2020 Task 12 (OffensEval)** beş dilde saldırgan dil tespiti yaptı ve
**Türkçe o beş dilden biriydi** (Türkçe korpus **OffensCorpus**, 36.232 tweet).
⛔ Yani *«Türkçe'de güvenlik/denetim NLP'si yok»* denemez — **var**, yalnız
**terapötik davranış** tarafı yok. Sınır böyle çizilmeli.

### 8.4 ⛔ YÖK Tez · TR Dizin · ULAKBİM — taranamadı, ve nedeni değişti

`tez.yok.gov.tr` arama ekranı **oturum gerektiriyor**, arama motorları tez
içeriğini indekslemiyor. TR Dizin ve ULAKBİM doğrudan sorgulanamadı.
**DergiPark açık ve tarandı** (8.1 oradan çıktı).

➡️ ⚠️ **Tezde artık *«aranmadı»* değil *«erişilemedi»* yazılmalı** — bu bir
arama değil **erişim** eksiğidir, çözümü üniversite ağıdır. §7'nin ilk maddesi
bu şerhle **açık kalır**.
