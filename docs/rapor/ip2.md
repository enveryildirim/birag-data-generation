<!-- ip_no: 2 -->
<!-- ip_adi: Model Geliştirme ve İnce Ayarının Yapılması -->
<!-- tamamlanma: %60 -->
<!--
Gelişme raporu (0–12. ay) · İP2 metni. `scripts/analiz/2026-10-21-rapor-docx.py` bu dosyayı
şablona döker. Her sayının kaynağı yanındaki yorumda (Kural 7). Yorumlar docx'e girmez.
Tamamlanma yüzdesi öneridir; kararı yürütücü verir (docs/rapor/gelisme-raporu-plani.md §1).
T311 (26B taban ↔ ince) mühürsüz bir keşif koşusudur; metinde öyle anılır.
-->

# Çalışmalar

## İP2.1 Amaç ve öneriyle ilişki

İP2'de, İP1'de hazırlanan talimat veri kümesiyle açık ağırlıklı bir LLM'i bağımlılık danışmanlığına özgü talimatlara uyacak şekilde ince ayarlamayı hedefledik. Modelden beklenen; terapötik diyalogda anlamlı ve bağlama uygun, Türkçeye göre iyileştirilmiş, hızlı ve güvenli cevaplar üretmesi. Dönem içinde (i) model ailesi seçildi, (ii) yerel keşif ve bulut üretim olmak üzere iki katmanlı bir eğitim altyapısı kuruldu, (iii) beş eksenli bir değerlendirme sistemi geliştirildi, (iv) ince ayarın hangi parametrelere ve hangi veri içeriğine duyarlı olduğu kontrollü deneylerle incelendi ve (v) üretim adayı Gemma 4 26B-A4B ince ayarlanıp taban modelle karşılaştırıldı.

Öneri formundaki yöntemden beş noktada ayrıldık. Bu farkları ve gerekçelerini Tablo 5'te topladık.

| Konu | Öneride | Gerçekleşen | Gerekçe |
|---|---|---|---|
| Temel model | Gemma 2 9B, Aya Expanse 8B, Llama 3.1 8B | Gemma 4 ailesi (E4B → 12B → 26B-A4B → 31B), aileler arası genelleme için Qwen3.8-27B | Formdaki modeller 2024 neslidir ve thinking (reasoning) kanalı yoktur. Gemma 4 ailesinde aynı kontrol token'ıyla açılıp kapanan bir thinking kanalı, Apache 2.0 lisansı ve 3,8B active parameter ile çalışan bir Mixture-of-Experts (MoE) modeli var. MoE modeli yanıt süresi hedefi için belirleyici oldu. |
| Eğitim yöntemi | ORPO | Supervised fine-tuning (SFT); ORPO ertelendi | Dar bir tercih verisiyle ORPO genel yetenek kaybını artırabilir. Önce SFT ve replay ile forgetting ölçüldü; ORPO, SFT'nin çözemediği hata kalıpları için sonraya bırakıldı. Judge'ın kabul/ret kararları ve uzman düzeltmeleri hazır bir tercih çifti kaynağı. |
| Quantization | QLoRA (4 bit) | bf16 LoRA; quantization eğitimden sonra | QLoRA'da adapter quantization hatasını telafi edecek şekilde öğrenir ve dağıtımdaki şema eğitimdekinden farklıysa kalite fark edilmeden düşer. Bu yüzden merge → quantization → yeniden değerlendirme sırası izlendi. |
| Metin benzerliği ölçütü | BLEU / ROUGE > %80 | Birincil ölçüt uzman + LLM-judge; BLEU/ROUGE ve BERTScore ikincil | Serbest terapötik diyalogda tek bir doğru cevap olmaz ve kelime örtüşmesine dayanan ölçütler insan yargısıyla zayıf ilişkilidir (Liu vd., 2016). BLEU/ROUGE yine de referanslı bir alt kümede raporlandı (Bölüm İP2.10). |
| Hesaplama | TRUBA | Yerel Apple M5 Max (keşif) + Google Colab A100 (üretim) | Hızlı denemeler yerelde, büyük model eğitimi ve değerlendirmesi Colab'da yapıldı. İki ortam aynı yapılandırma dosyasını kullanıyor. |

> Tablo 5. İP2'de öneri formundan yöntem sapmaları. Kaynak: `plan.md` (K6, K7, K9, K29, §14) · `docs/rapor/oneri-rapor-esleme.md`.

## İP2.2 Model seçimi

Modelleri bir merdiven olarak düzenledik (Tablo 6). Gemma 4 ailesinin bütün üyeleri aynı chat template'i ve aynı thinking kontrol token'ını kullandığı için küçük modelde görülen bir veri ya da eğitim etkisini büyük modelde sınamak mümkün. Hızlı deneyler E4B ile, transfer kontrolü 12B ile yapılıyor. 26B-A4B üretim adayı, 31B ise kalite tavanı için referans. Farklı aileden Qwen3.8-27B'yi yalnızca sonda bir kez, "veri kümesi Gemma'ya mı uydu, yoksa davranışı mı öğretiyor?" sorusu için genelleme kontrolü olarak kullanmayı planladık.

| Model | Parametre (total / active) | MMLU-Pro | GPQA-D | Merdivendeki rolü |
|---|---|---:|---:|---|
| Gemma 4 E4B | 8B / 2,3B | 69,4 | 58,6 | Hızlı deney döngüsü |
| Gemma 4 12B | 11,95B (dense) | 77,2 | 78,8 | Transfer kontrolü |
| Gemma 4 26B-A4B | 25,2B / 3,8B (MoE, 128 uzmandan 8'i) | 82,6 | 82,3 | Üretim adayı |
| Gemma 4 31B | 30,7B (dense) | 85,2 | 84,3 | Kalite tavanı |
| Qwen3.8-27B | 27B (dense) | — | 89,2 | Aileler arası genelleme kontrolü |

> Tablo 6. Model merdiveni. Benchmark puanları üretici beyanıdır (Google DeepMind, 2026; Qwen Team, 2026). Kaynak: `plan.md:670-681` · `docs/hf/model-karti-26b.md`.

Bu dönem merdivenin E4B ve 26B-A4B basamakları ince ayarlanıp değerlendirildi. 12B transfer kontrolü ile 31B ve Qwen3.8-27B ince ayarı sonraki döneme kaldı; 31B ve Qwen3.8-27B bu dönem judge olarak kullanıldı.

## İP2.3 Eğitim altyapısı ve deney disiplini

Eğitim altyapısı iki katmanlı. Keşif katmanında Apple M5 Max (128 GB birleşik bellek) üzerinde MLX ile bf16 LoRA eğitimi yapılıyor ve hipotezler küçük modelde (E4B) hızla sınanıyor. Üretim katmanında aynı tarif Google Colab A100 üzerinde Unsloth ve TRL ile uygulanıyor. İki çalıştırıcı da aynı YAML yapılandırma dosyasını okuyor. MLX ile PEFT arasındaki parametre mapping'ini yazılı olarak çıkardık; bulunan tek fark (optimizer'ın bias correction'ı) iki kolda eşitlendi. Keşif deneylerindeki tarif şöyle: üst 8 katmanın attention projection'larına (`q_proj`, `o_proj`) LoRA (Hu vd., 2022), rank 8, scale 20 (PEFT karşılığı α = 160), AdamW, learning rate 1·10⁻⁵, 3 epoch, en fazla 2.048 token. Loss yalnızca son danışman turundan hesaplanıyor ve thinking de loss'a dahil.
<!-- kaynak: plan.md:664-688 · configs/training/README.md · configs/training/e3-celiskili-k8qo-v022-t7.yaml · reports/analiz/2026-09-29-v011-onkayit-ek2.md · docs/colab-egitim-rehberi.md:73-77 -->

Deneylerde üç kurala uyduk. Karşılaştırmalı her deneyin hipotezi, birincil ve bekçi ölçüleri ve karar kuralı koşudan önce yazılıp ilgili dosyaların SHA-256 özetiyle mühürlendi (pre-registration). `v0.1.1` karşılaştırması için bir pre-registration ve üç eki, 26B karşılaştırması için ayrı bir pre-registration hazırlandı. Her eğitim ve değerlendirme koşusunun çıktısı zaman damgalı bir dizine yazılıyor ve üzerine yazılmıyor; raporladığımız her sayı, girdi dosyasının özetini çıktısına yazan bir analiz betiğinden geliyor. Tek seed'li sonuçları "keşif" diye işaretledik; karar gerektiren karşılaştırmaları 3–8 seed ile tekrarlayıp farkları standart hataya göre okuduk.
<!-- kaynak: reports/analiz/2026-09-29-v011-onkayit*.md · reports/analiz/2026-09-30-v011-onkayit-ek3.md · configs/deney/2026-10-12-taban-vs-ince-on-kayit*.json · PROJECT_MEMORY.md:98 (K47) -->

## İP2.4 Türkçe için optimizasyon: thinking kanalı

Gemma 4 modelleri cevaptan önce reasoning (thinking) üretebiliyor. Bu kanal danışmanın ne yapacağını planlaması için yararlı, ama eğitilmemiş modelde iki sorun gördük. Birincisi, Türkçe bir danışmanlık konuşmasında bile thinking İngilizce (E4B'de 8 örneğin 8'inde). System prompt'a "Türkçe düşün" talimatı eklemek bunu değiştirmedi (0/12). İkincisi, thinking cevaba göre çok uzun: ortanca thinking 350 sözcük, cevap 21 sözcük. Üretilen token'ların %95'i kullanıcıya hiç ulaşmıyor ve cevap başına süre 14,5 saniye.
<!-- kaynak: PROJECT_MEMORY.md:97 (K46), :100 (K48) -->

Thinking'in dilini ve uzunluğunu bu yüzden prompt yerine eğitimle değiştirmeye karar verdik. Veri kümesindeki her örneğe Türkçe ve cevapla orantılı bir thinking yazıldı (Bölüm İP1.6). Deneyler Türkçe thinking'in öğrenilebildiğini ve bunun LoRA'nın derinliğine bağlı olduğunu gösterdi; rank'ı artırmanın etkisi olmadı. LoRA yalnızca üst 8 katmana uygulandığında thinking hiç Türkçeye dönmedi, 42 katmanın tamamına uygulandığında 48 örneğin 48'inde Türkçe oldu. Rank'ı 32'ye çıkarmak bir şey değiştirmedi. 26B-A4B ince ayarında aynı sonuç üretim ölçeğinde de görüldü: thinking'i Türkçe olan cevapların oranı tabanda %46,8, ince ayarlı modelde %100. Ortanca thinking uzunluğu 583 sözcükten 90 sözcüğe, toplam token ortancası 1.144'ten 260'a indi.
<!-- kaynak: reports/analiz/2026-09-12-thinking-dili-ogrenilebilirlik.md (K50) · reports/analiz/2026-09-15-f4-lora-kapsam-taramasi.md:161-200 (T28) · reports/analiz/2026-10-20-ip2-olcutler.md:83-93 -->

## İP2.5 Değerlendirme sistemi

Öneri formundaki "doğruluk", "uzman memnuniyeti" ve "etik/güvenlik" ölçütlerini, terapötik bir diyalog modelinde birbirinden bağımsız bozulabilen beş eksene ayırdık. Her eksenin kendi seti var (Tablo 2):

1. Terapötik kalite. Elle yazılmış golden setlerde her öğe için otomatik denetlenen iddialar ("yargılamaz", "tek soru sorar", "numara uydurmaz" gibi) ve LLM-judge rubriği (EPITOME, MG uyumu, tuzak ihlali, context fidelity, dil bütünlüğü).
2. Güvenlik ve kriz. 15 risk ve 5 kontrol öğesi. Bu eksendeki her gerileme işi durdurur.
3. Forgetting. Aritmetik, özetleme, çeviri ve talimat izleme gibi genel yeteneklerin korunması.
4. Context fidelity. Verilen bağlamdaki bilgiyi doğru kullanmak ve bağlamda olmayanı uydurmamak; RAG modülüyle (İP3) birlikte çalışmanın ön koşulu.
5. Sycophancy / özerklik. Kullanıcının hatalı ya da zararlı önermesini onaylamamak. LLM'lerin kullanıcı haksızken bile onu onayladığı gösterildiği için ayrı eksen yapıldı (Cheng vd., 2025).

Yanıt süresi de operasyonel bir ölçüt olarak izleniyor. Model seçiminde en düşük validation loss'a bakmıyoruz, bir Pareto kuralı uyguluyoruz: güvenlik ekseninde hiç gerileme olmamalı ve forgetting eksenindeki düşüş %3'ü geçmemeli. Bu iki koşulu sağlayan adaylardan terapötik kalitesi en yüksek olanı seçiliyor. İkili karşılaştırmalarda iki bağımsız judge (Gemma-4-31B ve Qwen3.8-27B) kör olarak ve cevapların sırası değiştirilerek iki kez çalıştırıldı. Judge'ların geçerliliğini ekibin 40 çiftlik kör insan etiketiyle sınadık.
<!-- kaynak: plan.md:468-570, :636-642 · reports/analiz/2026-10-20-taban-vs-ince-basit-inceleme.md:5, :36-41 · PROJECT_MEMORY.md:755 -->

## İP2.6 Başlangıç (taban) ölçümleri

İnce ayardan önce eğitilmemiş E4B modelinin tüm eksenlerdeki tabanını ölçtük. Model genel yetenekte güçlü (forgetting 28/30, sycophancy 20/24, context fidelity 15/20). Kriz setindeki sonuç ise otomatik kuralın nasıl tanımlandığına bağlı: kriz öğelerinde düşen 8 cevabın 8'i 112 acil numarasını yazdığı için düşmüş, uydurulmuş numara yok. 112 ihlal sayılırsa taban 6/15, meşru sayılırsa 14/15. golden.locked setinde otomatik iddiaların 46/48'i geçildi; judge rubriğinde çoğunluk kuralıyla 22/48 öğe geçti. Model sert kuralları çiğnemiyor ama MG becerisi de göstermiyor.
<!-- kaynak: PROJECT_MEMORY.md:165 (K105), :164 (K106) · reports/analiz/2026-09-15-eksen-baseline.md · reports/analiz/2026-09-15-locked-baseline.md:13-45 -->

Yanıt süresi tabanı 142 öğede ölçüldü: ortanca 12,9 saniye, %90'lık dilim 16,2 saniye. Süreyi neredeyse tamamen thinking uzunluğu belirliyor. Thinking uzunluğuyla korelasyon 0,94, cevap uzunluğuyla 0,47; thinking'i boş kalan 16 öğede ortanca süre 0,5 saniye. 2 saniye hedefi için ilk yapılması gereken şey, donanımı büyütmekten önce thinking'i kısaltmak.
<!-- kaynak: reports/analiz/2026-09-15-gecikme-taban.md:7-34 (K107; E4B, MLX, M5 Max) -->

## İP2.7 LoRA kapsamı, derinliği ve veri dozu deneyleri

Öneri formunda forgetting'i sınırlamak için PEFT/LoRA kullanılması öngörülüyordu; literatür de LoRA'nın tam ince ayara göre daha az unuttuğunu gösteriyor (Biderman vd., 2024). Bizim deneylerimizde ise terapötik ince ayarda asıl kaybolan şey güvenlik davranışı oldu. E4B üzerinde beş LoRA kolunu karşılaştırdık (dar: 8 katman `q_proj`; derin: 42 katman; dikkat: + `o_proj`; tam: + MLP; geniş: rank 32). Hiçbiri Pareto kuralını geçemedi. Kriz öğelerinde profesyonel desteği hiç anmayan cevap sayısı tabanda 1 iken kollarda 2 ile 13 arasındaydı. Validation loss'u en düşük kol, güvenlikte en kötü ikinci koldu; loss eğrisine bakarak model seçmek bu yüzden yeterli değil.
<!-- kaynak: reports/analiz/2026-09-15-f4-lora-kapsam-taramasi.md:15-23 · PROJECT_MEMORY.md:170 (K109) -->

Bozulmanın nereden geldiğini ayırmak için iki kontrollü deney yaptık (Şekil 4).

İlkinde (Şekil 4a) veri, adım, rank ve hedef modül sabit tutuldu, yalnızca LoRA uygulanan katman sayısı değiştirildi. Kriz puanı 12 katmana kadar yavaş yavaş düştü (%63'ten %46'ya), 12'den 13'e geçerken %8'e çöktü. Token bütçesini iki katına çıkararak çöküşün cevapların kesilmesinden kaynaklanmadığını doğruladık. Ek deneyler çöküşün büyük kısmını tek bir katmanın, 29. katmanın eğitime girmesine bağlıyor. Ancak bu sonuç tek seed'li ve 15 öğelik, o yüzden şimdilik ön bulgu.

İkincisinde (Şekil 4b) eğitim verisinde yönlendirme içeren kayıtların payı %5,1'den %10,2'ye ve %24,1'e çıkarıldı. Beş kolun hiçbirinde yönlendirme kaybı azalmadı, eğri düz kaldı. "Veride yeterince yönlendirme yok" açıklaması böylece elendi. Elimizdeki açıklama şu: veride kriz örneği olmadığı için model yönlendirmeyi sıradan danışmanlık bağlamında öğreniyor ve kriz bağlamına taşımıyor.

![Şekil 4. a) LoRA derinliği ile kriz davranışı arasındaki ilişki (E4B, v0.0.8, tek seed). b) Eğitim verisindeki yönlendirme dozu ile kriz öğelerinde yönlendirmesiz cevap sayısı arasındaki ilişki (beş LoRA kolu, 16 öğe; düşük değer daha iyidir).](reports/analiz/sekiller/s5-lora-katman-doz.png)
<!-- kaynak: reports/analiz/2026-09-17-ucurum-haritasi.md · reports/analiz/2026-09-15-f4c-doz-egrisi.json · reports/analiz/2026-09-15-doz-yanit-egrisi.md · reports/analiz/2026-10-21-rapor-sekiller.md -->

Daha büyük veriyle (571 kayıt) tekrarlanan kapsam merdiveninde de katman sayısı ve kapsam ile güvenlik kaybı arasında anlamlı bir ilişki çıkmadı. Üç seed'le yapılan karşılaştırmada dar kol daha pahalı kollardan ayırt edilemediği için üretim tarifi olarak dar kolu tuttuk. E4B'nin `v0.0.18` ile 8 seed'li ince ayarında kriz seti 11/20'den 8,75/20'ye, forgetting seti 28/30'dan 26,75/30'a geriledi. Context fidelity ve sycophancy eksenlerindeki fark gürültü düzeyinde kaldı.
<!-- kaynak: reports/analiz/2026-09-17-kapsam-merdiveni.md:13-63 · reports/analiz/2026-09-19-kapsam-karari-uc-tohum.md · reports/analiz/2026-09-22-taban-vs-incelayar.md:12-18 -->

## İP2.8 Gemma 4 26B-A4B ince ayarı ve taban ile karşılaştırma

Üretim adayı Gemma 4 26B-A4B, `v0.1.1` veri kümesiyle Colab'da Unsloth ve TRL kullanılarak ince ayarlandı. Çıktı olarak merge edilmiş bf16 ağırlıklar ile Q8_0 ve Q4_K_M GGUF dosyaları üretildi. Model Hugging Face'te paylaşıldı (https://huggingface.co/yildirim34/birag-gemma4-26b). İnce ayarlı modeli tabanla aynı ortamda (A100, greedy decoding, thinking açık, en fazla 2.048 yeni token) Tablo 2'deki setlerde karşılaştırdık. Bu karşılaştırma pre-registration ile mühürlenmemiş bir keşif koşusu; sonuçlar yön gösteriyor ve sonraki dönem mühürlü olarak tekrarlanacak.
<!-- kaynak: reports/analiz/2026-10-20-taban-vs-ince-basit-inceleme.md:4-6 · configs/deney/2026-10-12-taban-vs-ince-on-kayit-ek2.json · docs/hf/model-karti-26b.md -->

### Kural uyumu ve Türkçe

İnce ayardan sonra model projenin yazılı davranış kurallarına belirgin şekilde daha iyi uydu (Tablo 7). Elle yazılmış öğelerin bütün otomatik iddialarını geçme oranı golden setlerde %87,4'ten %97,9'a, tüm terapötik setlerde %69,8'den %85,7'ye çıktı. Tabanın 2.048 token'da kesilen ya da boş kalan cevapları sonucu etkilemesin diye yalnızca iki modelin de dolu cevap verdiği öğelere baktığımızda da artış sürüyor (%79,4'ten %87,3'e). Thinking tamamen Türkçeye döndü, token ortancası 1.144'ten 260'a indi.

| Ölçü | Taban | İnce ayarlı |
|---|---:|---:|
| Doğruluk proxy'si, golden setler | 83/95 (%87,4) | 93/95 (%97,9) |
| Doğruluk proxy'si, tüm terapötik setler | 132/189 (%69,8) | 162/189 (%85,7) |
| Doğruluk proxy'si, iki modelin de cevap verdiği öğeler | 131/165 (%79,4) | 144/165 (%87,3) |
| Genel yetenek (forgetting seti) | 28/30 (%93,3) | 26/30 (%86,7) |
| Türkçe thinking / Türkçe cevap | %46,8 / %100 | %100 / %100 |
| Token ortancası (terapötik setler) | 1.144 | 260 |
| 2.048 token'da kesilen / boş cevap | 23 / 22 | 3 / 3 |
| Zararlı yanıt adayı (en az bir işaret) | 9/190 (%4,7) | 13/190 (%6,8) |

> Tablo 7. 26B-A4B taban ve ince ayarlı modelin otomatik ölçüleri (keşif koşusu). Doğruluk proxy'si kural uyumunu ölçer; cevabın terapötik kalitesini ölçmez. Kaynak: `reports/analiz/2026-10-20-ip2-olcutler.md`.

### Kalite: insan ve judge değerlendirmesi

Cevapların genel kalitesine bakan kör pairwise karşılaştırmalar ise tabanı üstün buldu (Şekil 5). Ekip 40 tabakalı çiftte 26'ya 8 taban lehine karar verdi (sign test p = 0,003). İnsanla en çok uyuşan judge (Gemma-4-31B, κ = 0,44) da 200 çiftte tabanı açık farkla tercih etti. Qwen3.8-27B'de belirgin bir position bias vardı: cevapların sırası değişince kararın yalnızca %47'si aynı kaldı, insanla uyumu κ = 0,22 ile geçerlilik eşiğinin (κ ≥ 0,40) altındaydı. İki judge'ın uyuşmasını şart koşan jüri kararı bu yüzden "eşit"e kaydı; jüri sonucunu fark olmadığı şeklinde okumamak gerekir. Tabanın kesilip boş kaldığı öğeler çıkarıldığında Gemma judge'ında taban üstünlüğü daha da açılıyor (110'a 10).

Cevapları tek tek okuduğumuzda ince ayarlı modelin cevapları mekanik ve "tutanak tutar gibi" geldi. Kullanıcının söylediğini tekrar eden kalıplar ("…yazdın / dedin") %1,5'ten %34,1'e, "bilemem / söyleyemem" kalıpları %2,0'dan %30,1'e çıktı. Aynı kalıplar eğitim verisinde de yüksek oranda (%21,4 ve %19,2) bulunuyor, yani sorun veriden geliyor.

![Şekil 5. Taban ve ince ayarlı 26B-A4B modelin kör pairwise karşılaştırması. Her satır bir değerlendirme kaynağıdır; p değerleri eşit kararlar dışarıda bırakılarak sign test ile hesaplanmıştır.](reports/analiz/sekiller/s6-taban-ince.png)
<!-- kaynak: reports/analiz/2026-10-20-taban-vs-ince-basit-inceleme.md:36-67, :107-116 · PROJECT_MEMORY.md:737 -->

### Güvenlik

Güvenlik ekseninde ciddi bir gerileme gördük (Şekil 6). Risk taşıyan 15 öğenin 4'ünde taban model danışanı bir profesyonele ya da kriz hattına yönlendirirken ince ayarlı model yönlendirmedi. Bunlardan biri setteki en yüksek şiddetli öğe ("tuhaf bir sakinlik", "karar verdim galiba"). İnce ayarlı model bir öğede de 182'yi kriz hattı olarak verdi; 182 Türkiye'de MHRS randevu hattı, kriz hattı değil. Kural tabanlı denetim bu kaybı göstermedi, çünkü aynı kural tabanın 112 yazan cevaplarını da düşürüyordu. Kaybı ancak cevapları öğe öğe okuyarak fark ettik. Kriz içermeyen 5 kontrol öğesinde ince ayarlı model gereksiz yere acil hat önermedi.

![Şekil 6. Risk taşıyan 15 güvenlik öğesinde cevabın profesyonel/kriz kaynağına yönlendirme içerip içermediği. Turuncu halkalar tabanda bulunup ince ayarlı modelde kaybolan yönlendirmelerdir.](reports/analiz/sekiller/s7-risk-yonlendirme.png)
<!-- kaynak: reports/analiz/2026-10-20-taban-vs-ince-basit-inceleme.md:71-94 · reports/analiz/2026-10-20-ip2-olcutler.md:67-75 -->

## İP2.9 Tartışma: krizsiz verinin bedeli ve güvenlik katmanı

E4B deneyleri de 26B ince ayarı da aynı yere çıkıyor: içinde kriz örneği olmayan bir veri kümesiyle ince ayar yapınca tabanın kriz yönlendirmesi aşınıyor. LoRA'nın kapsamını ya da rank'ını değiştirmek, veri hacmini ya da verideki yönlendirme dozunu artırmak bunu düzeltmedi (Bölüm İP2.7). İP1'de kriz dilimini, uzman ve etik kurul onayı gerektiği için bilerek üretmemiştik. `v0.1.1`'in 1.654 danışman turunda 112, 182 ya da "kriz hattı" hiç geçmiyor. Ölçek-5k üretiminde de risk sinyali taşıyan kullanıcı turu olmadığından, hacmi artırmak bu açığı kapatmayacak. Alana özgü ince ayarın modelin güvenlik hizalamasını bozabildiği başka çalışmalarda da gösterilmiş (Hsu vd., 2024).

Bu sonucun proje açısından iki karşılığı var. Birincisi, uzman onaylı Güvenlik Planı protokolüne dayanan bir kriz dilimi üretilmeden hiçbir ince ayarlı model güvenlik kontrolünü geçemeyecek; bu, sonraki dönemde İP1 ve İP2'nin önceliği. İkincisi, kriz tespiti yalnızca ince ayarlı modele bırakılmamalı. Hat numarası ve kurum gibi kriz kaynak bilgisi model ağırlıklarında değil uygulama yapılandırmasında tutulmalı. Bu gerekliliği, öneri formunda İP4'te yer alan risk değerlendirme ve koordinatör ajanlarının tasarımına girdi olsun diye İP4'e bir teslim notuyla ilettik. Kriz onayı alınana kadar ince ayarlı modelin kullanıcıya açılmamasını öneriyoruz.

Ölçümün kendisiyle ilgili bir sonuç da var. Kural uyumunu ölçen doğruluk proxy'si ince ayarlı modeli açıkça üstün gösterirken insan değerlendirmesi ve insanla uyumlu judge tabanı üstün buldu. Terapötik kalitede kurallara uymak gerekli ama yetmiyor; İP2'nin "doğruluk %90" ölçütü için uzman değerlendirmesi şart.

## İP2.10 BLEU/ROUGE ve yanıt süresi ölçümleri

Değerlendirme setlerinde tasarım gereği referans cevap yok. BLEU/ROUGE için bu yüzden ayrı bir referans seti hazırladık: eğitimde kullanılmayan ve değerlendirme seed'leriyle çakışmayan ölçek-5k kayıtlarından, tur tipi ve mesaj biçimine göre tabakalı 200 kayıt. İki model bu setteki konuşmalara Colab'da cevap üretti (A100, greedy decoding, thinking açık, en fazla 2.048 yeni token). Puanlamada BLEU (Papineni vd., 2002), chrF, ROUGE-1/2/L (Lin, 2004) ve BERTScore (Zhang vd., 2020) kullanıldı. Metinler Türkçe case folding ile tokenize edildi, güven aralıkları 1.000 resample'lı bootstrap ile hesaplandı (Tablo 8).

| Ölçü | Taban (200) | İnce ayarlı (200) | Taban, ikisi dolu (163) | İnce ayarlı, ikisi dolu (163) |
|---|---:|---:|---:|---:|
| BLEU | 0,4 (0,2–0,5) | 5,1 (4,1–6,2) | 0,6 (0,4–0,9) | 4,5 (3,4–5,6) |
| chrF | 14,6 (13,3–15,8) | 33,2 (31,9–34,6) | 17,7 (16,6–18,8) | 32,6 (31,2–34,1) |
| ROUGE-1 | 11,3 (10,2–12,4) | 24,5 (23,1–25,8) | 13,9 (12,7–15,0) | 24,1 (22,8–25,5) |
| ROUGE-2 | 2,0 (1,6–2,4) | 7,7 (6,7–8,7) | 2,4 (1,9–3,0) | 7,1 (6,1–8,1) |
| ROUGE-L | 8,8 (7,9–9,6) | 16,3 (15,2–17,4) | 10,7 (9,8–11,5) | 15,7 (14,6–16,7) |
| BERTScore | 55,2 (51,6–58,4) | 69,6 (68,2–70,7) | 67,0 (66,5–67,5) | 70,3 (69,8–70,8) |

> Tablo 8. Referans setinde metin benzerliği (0–100, parantez içinde %95 güven aralığı). "İkisi dolu" sütunları yalnızca iki modelin de boş olmayan cevap verdiği kayıtları içerir. Kaynak: `reports/analiz/2026-10-20-rapor-bleu-gecikme.md`.
<!-- kaynak: reports/analiz/2026-10-20-rapor-bleu-gecikme.md §1 · reports/analiz/2026-10-20-rapor-referans-seti.md -->

Öneri formundaki %80 hedefine hiçbir ölçüde yaklaşılamadı; ince ayarlı modelde BLEU 5,1, ROUGE-L 16,3. Bunu bekliyorduk. Aynı danışan mesajına birçok doğru terapötik cevap verilebildiği için kelime düzeyinde örtüşme düşük kalıyor (Liu vd., 2016). İnce ayarlı model bütün ölçülerde tabanın üstünde: chrF 14,6'ya karşı 33,2, BERTScore 55,2'ye karşı 69,6. Tabanın 35 boş cevabı bu farkı büyütüyor. Yalnızca iki modelin de cevap verdiği 163 kayda bakınca fark daralıyor ama yönü değişmiyor (BERTScore 67,0'a karşı 70,3, chrF 17,7'ye karşı 32,6). Cevap uzunluğunda da ince ayarlı model referansa daha yakın: ortanca 39 sözcük, referansta 48, tabanda 16.

Referans cevapları da bir LLM yazdı ve bunlar henüz C aşaması denetiminden geçmedi. Bu yüzden sonuçları uzman cevabına benzerlik olarak değil, veri kümesinin üslubuna yakınlık olarak okuyoruz. Bu okuma, insan değerlendirmesinde tabanın üstün çıkmasıyla (Bölüm İP2.8) çelişmiyor: benzerlik ölçüleri cevabın üslubunu ölçer, terapötik olarak iyi olup olmadığını ölçmez. Bu ölçütün form hedefiyle değil, iki modelin kıyası olarak raporlanmasını ve uzman ile LLM-judge değerlendirmesinin birincil ölçüt sayılmasını öneriyoruz.

Yanıt süresini golden.test setindeki 48 soruda, istekleri tek tek göndererek ve cevabı akış hâlinde üreterek ölçtük (Şekil 7). Üç durum karşılaştırıldı: taban ve ince ayarlı model thinking açıkken, ince ayarlı model ayrıca thinking kapalıyken. İlk token her durumda yarım saniye civarında geliyor (ortanca 0,48–0,62 sn). Ancak thinking açıkken kullanıcı, thinking bitene kadar cevabın ilk kelimesini göremiyor. Bu bekleme tabanda ortanca 158,5 saniye, ince ayarlı modelde 29,0 saniye. Thinking kapalıyken görünen cevap 0,62 saniyede başlıyor ve ortanca 14,5 saniyede bitiyor.

![Şekil 7. Tek istek yanıt süresi (golden.test, 48 soru, ortanca). Gri bölüm thinking bitene kadar geçen süre, renkli bölüm görünen cevabın akışıdır; kesikli çizgi öneri formundaki 2 saniye hedefidir. Ortam: Colab A100, Hugging Face generate, batch 1.](reports/analiz/sekiller/s8-gecikme.png)
<!-- kaynak: reports/analiz/2026-10-20-rapor-bleu-gecikme.md §2 · reports/analiz/2026-10-21-rapor-sekiller.md (Ş8) -->

Toplam sürelerin 2 saniyeyi aşmasında çıkarım ortamının payı büyük. Ölçüm Hugging Face generate ile yapıldı ve üretim hızı üç durumda da saniyede yaklaşık 7 token oldu (ortanca 6,8–7,1). Hız modelden modele değişmediğine göre süreyi belirleyen, üretilen token sayısı ve bu ortamın yavaşlığı. vLLM gibi bir üretim sunucusunda ve quantization ile ölçüm sonraki döneme kaldı. Formdaki "yanıt süresi" ifadesi iki türlü okunabilir. Cevap akış hâlinde gösterilirse, thinking kapalı ince ayarlı model 2 saniye içinde yanıt vermeye başlıyor. Cevabın tamamı ise bu ortamda hiçbir durumda 2 saniyenin altına inmiyor.

## İP2.11 Ara çıktılar

İP2 kapsamındaki ara çıktılar ekler bölümündedir:

- Ek 2-A: Eğitim yapılandırmaları (YAML), MLX ve Colab/Unsloth eğitim defterleri, MLX ↔ PEFT parametre mapping'i (https://github.com/enveryildirim/birag-data-generation)
- Ek 2-B: Pre-registration belgeleri ve mühür özetleri
- Ek 2-C: Beş eksenli değerlendirme protokolü, judge rubrikleri ve değerlendirme defterleri
- Ek 2-D: Taban ölçüm raporları (eksenler, locked set, yanıt süresi)
- Ek 2-E: LoRA kapsam, derinlik ve doz deney raporları
- Ek 2-F: 26B-A4B taban ↔ ince ayar karşılaştırma raporları ve İP2 ölçüt raporu
- Ek 2-G: Model kartı (https://huggingface.co/yildirim34/birag-gemma4-26b) ve İP4'e güvenlik katmanı teslim notu
- Ek 2-H: BLEU/ROUGE referans seti, yanıt süresi ölçüm defteri ve ölçüm sonuçları

## Kaynaklar

- Biderman, D. vd. (2024). LoRA learns less and forgets less. *Transactions on Machine Learning Research*.
- Cheng, M. vd. (2025). Sycophantic AI decreases prosocial intentions and promotes dependence. arXiv:2510.01395.
- Google DeepMind (2026). Gemma 4 model family. https://huggingface.co/google/gemma-4-26B-A4B-it
- Hsu, C.-Y., Tsai, Y.-L., Lin, C.-H., Chen, P.-Y., Yu, C.-M. ve Huang, C.-Y. (2024). Safe LoRA: The silver lining of reducing safety risks when finetuning large language models. *NeurIPS 2024*.
- Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L. ve Chen, W. (2022). LoRA: Low-rank adaptation of large language models. *ICLR 2022*.
- Lin, C.-Y. (2004). ROUGE: A package for automatic evaluation of summaries. *Text Summarization Branches Out (ACL Workshop)*, 74–81.
- Liu, C.-W., Lowe, R., Serban, I. V., Noseworthy, M., Charlin, L. ve Pineau, J. (2016). How NOT to evaluate your dialogue system: An empirical study of unsupervised evaluation metrics for dialogue response generation. *Proceedings of EMNLP 2016*, 2122–2132.
- Papineni, K., Roukos, S., Ward, T. ve Zhu, W.-J. (2002). BLEU: A method for automatic evaluation of machine translation. *Proceedings of ACL 2002*, 311–318.
- Qwen Team (2026). Qwen3.8 model family.
- Zhang, T., Kishore, V., Wu, F., Weinberger, K. Q. ve Artzi, Y. (2020). BERTScore: Evaluating text generation with BERT. *ICLR 2020*.
- Zheng, L. vd. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. *NeurIPS 2023 Datasets and Benchmarks Track*.

# Gerçekleşme

| Başarı ölçütü (öneri formu) | Hedef | Gerçekleşen | Durum |
|---|---|---|---|
| Doğruluk | > %90 | Kural uyumu proxy'si: golden setlerde %97,9, tüm terapötik setlerde %85,7. İnsan ve judge değerlendirmesinde taban üstün | Proxy'de karşılandı; kalitede karşılanmadı |
| Uzman memnuniyeti | %85 | İnce ayarlı model için uzman turu yapılmadı; ekip değerlendirmesi 26–8 taban lehine | Karşılanmadı |
| BLEU / ROUGE | > %80 | İnce ayarlı: BLEU 5,1, ROUGE-L 16,3, chrF 33,2, BERTScore 69,6 (taban 0,4 / 8,8 / 14,6 / 55,2). Ölçütün yeniden tanımı yürütücü onayında | Karşılanmadı |
| Yanıt süresi | < 2 sn | İlk token ~0,5 sn; thinking kapalıyken görünen cevap 0,62 sn'de başlıyor, toplam ortanca 14,5 sn (thinking açık 39,9 sn, taban 164,6 sn). HF generate, ~7 token/sn | Akışlı başlangıçta karşılandı; toplam sürede karşılanmadı |
| Kullanıcı geribildirimi | %90 olumlu | Kullanıcı pilotu İP5 kapsamında | Dönemi gelmedi |
| Etik ve güvenlik | %100 etik, ≈ %0 zararlı | Zararlı yanıt adayı %6,8 (taban %4,7); 15 risk öğesinin 4'ünde yönlendirme kaybı | Karşılanmadı |

> Tablo 9. İP2 başarı ölçütlerinin gerçekleşme durumu (26B-A4B keşif koşusu). Kaynak: `reports/analiz/2026-10-20-ip2-olcutler.md` · `reports/analiz/2026-10-20-taban-vs-ince-basit-inceleme.md` · `reports/analiz/2026-10-20-rapor-bleu-gecikme.md`.

Altyapıya yönelik hedefler gerçekleşti. Model ailesi seçildi, yerel ve bulut eğitim hattı kuruldu, beş eksenli değerlendirme sistemi ve pre-registration düzeni işletildi, üretim adayı model ince ayarlandı. Türkçe için iyileştirme hedefi de karşılandı: thinking %100 Türkçeye döndü ve ortanca uzunluğu 583 sözcükten 90 sözcüğe indi. Thinking'in kısalması, kullanıcının cevabı görmeye başlamadan önce beklediği ortanca süreyi 158,5 saniyeden 29,0 saniyeye indirdi.

Öneri formundaki kalite ve güvenlik ölçütleri ise bu dönem karşılanmadı. BLEU/ROUGE %80 hedefinin de altında kalındı; serbest diyalogda bu düzey beklenmediği için ölçütün yeniden tanımlanmasını öneriyoruz. Yanıt süresinde cevap 0,62 saniyede başlıyor ama tamamı bu ortamda 2 saniyeyi aşıyor. İnce ayarlı model kurallara daha iyi uyuyor, ama insan değerlendiricilere daha mekanik geliyor ve kriz yönlendirmesinde tabanın gerisinde kalıyor. Kontrollü deneyler gerilemenin eğitim yönteminden ya da LoRA ayarlarından kaynaklanmadığını gösterdi. Sorun veri kümesinin içeriğinde: kriz dilimi yok ve abartılı sınır kalıpları fazla. Neyin düzeltileceği bu sayede belli.

Sonraki dönem için planımız:

1. Uzman ve etik kurul onayıyla kriz dilimini üretmek ve ince ayara eklemek (İP1 ile birlikte).
2. Ölçek-5k veri kümesiyle yeniden eğitmek. Bu kümenin kalibrasyonunda "…yazdın / dedin", "katılmıyorum" ve "benim işim değil" kalıplarının oranı %0.
3. Yanıt süresini vLLM gibi bir üretim sunucusunda ve quantization ile yeniden ölçmek; thinking'in açık mı kapalı mı kullanılacağına İP4 ile birlikte karar vermek.
4. İnce ayarlı model için klinik uzman değerlendirme turu yapmak.
5. 26B karşılaştırmasını pre-registration ile mühürlü olarak tekrarlamak; 12B transfer kontrolünü ve Qwen3.8-27B genelleme kontrolünü yapmak.
6. SFT'nin çözemediği hata kalıpları için ORPO kararını vermek.

Model dışı güvenlik katmanı gerekliliği İP4'e iletildi. Context fidelity ekseni İP3'ün RAG modülüyle birlikte ölçülecek.
<!-- kaynak: reports/analiz/2026-10-20-olcek5k-kalip-kriz.md:107-112 · PROJECT_MEMORY.md:1058-1066 -->
