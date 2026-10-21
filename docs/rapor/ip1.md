<!-- ip_no: 1 -->
<!-- ip_adi: LLM için Talimat Veri Kümesi Toplama ve Ön İşleme -->
<!-- tamamlanma: %75 -->
<!--
Gelişme raporu (0–12. ay) · İP1 metni. `scripts/analiz/2026-10-21-rapor-docx.py` bu dosyayı
şablona döker. Her sayının kaynağı yanındaki yorumda (Kural 7). Yorumlar docx'e girmez.
Tamamlanma yüzdesi öneridir; kararı yürütücü verir (docs/rapor/gelisme-raporu-plani.md §1).
-->

# Çalışmalar

## İP1.1 Amaç ve öneriyle ilişki

İP1'in amacı, bağımlılık danışmanlığında kullanılacak Türkçe büyük dil modelinin (LLM) ince ayarı için terapötik ilkelere uygun, kültürel ve dilsel bağlamı yansıtan bir talimat veri kümesi hazırlamaktır. Öneri formunda bu iş paketi için dört hedef yer alıyor: (i) 10.000 çeşitli ve bağlama uygun talimat örneği, (ii) tutarlılık ve anlam bütünlüğü, (iii) Türkçe ve kültürel bağlama uygunluk, (iv) etik onay ve anonimleştirme.

Bu hedeflere aşamalı ilerledik. Önce küçük ve her kaydı denetlenen bir çekirdek üzerinde ölçüm altyapısı kuruldu, hacim ondan sonra büyütüldü. Terapötik diyalog verisinde yargılayıcı dil, uydurulmuş bilgi ya da kriz anında yönlendirmenin unutulması gibi bir hata kalıbı, veri büyüdükçe çoğalır. Bu kalıpları yakalayan kontroller olmadan hacmi artırmak hatayı da artıracaktı. Dönemin ilk yarısı bu yüzden veri kalitesini ölçen altyapıya, ikinci yarısı hacme ayrıldı.

Dönemde izlenen akış Şekil 1'dedir. Öneri formunun Şekil 1'indeki "veri toplama → ön işleme → ince ayar → değerlendirme" sırası korunmuş, araya otomatik kalite kontrolleri, LLM-judge ve uzman örneklemi eklenmiştir.

![Şekil 1. İP1 ve İP2'de gerçekleşen boru hattı. Üst sıra veri kümesinin üretimini (İP1), alt sıra ince ayar ve değerlendirmeyi (İP2) gösterir; kesikli oklar geri besleme döngüleridir.](reports/analiz/sekiller/s1-boru-hatti.png)

## İP1.2 Seed'ler ve taksonomi

Çıkış noktası, proje ekibinin önceki çalışmalarında hazırlanmış 2.240 kayıtlık Türkçe danışan mesajı korpusudur. Bu kayıtları önce uzmanlara incelettik; olumlu geri dönüş aldıktan sonra projede kullanmaya karar verdik. Korpusu senaryo seed'i olarak kullandık: her seed bir danışan durumunu (bağımlılık türü, evre, motivasyon, stres kaynağı) taşıyor, danışman cevabı ise bu duruma göre terapötik çerçeve izlenerek yazılıyor.
<!-- kaynak: configs/taxonomy.yaml:2 · PROJECT_MEMORY.md:74 (K26) · data/seeds.jsonl 2240 satır -->

Korpustaki kayıtların etiketleri serbest metin olarak yazılmıştı; aynı durum farklı kayıtlarda farklı adlarla geçiyordu. Bu etiketleri ortak bir listeye (taksonomi) bağladık. Listede 6 bağımlılık türü (tütün, alkol, kumar, reçeteli ilaç, madde, dijital), 19 senaryo tipi, 10 danışan profili, 7 evre, 5 motivasyon evresi, 4 risk düzeyi ve 8 üslup bulunuyor. Bu sırada "stres tipi" alanının iki farklı şeyi birlikte tuttuğunu gördük: danışmanın karşılaştığı durum ve danışanın stres kaynağı. Bu alanı ikiye böldük. Sonuçta 15 alanın 13'ü kayıtların tamamında doldu; stres tipi kayıtların %98,4'ünde, senaryo %76,3'ünde belirlenebildi. Senaryosu belirlenemeyen 531 kayda (%24) tahmini etiket vermedik, senaryoyu üretim sırasında atadık.
<!-- kaynak: configs/taxonomy.yaml:13-32, :53-96, :155-295 · PROJECT_MEMORY.md:425, :85 (K37) · K24 (16 → 19 senaryo) -->

Ham korpusta 186 kayıtta telefon numarası geçiyordu (182 numarası 128, 112 numarası 102 kez) ve bunların bir kısmı yanlış bağlamdaydı. Örneğin 182, MHRS randevu hattıdır, kriz hattı değildir. Bu yüzden telefon numaralarının model ağırlıklarına girmemesine karar verildi. Numara içeren her üretim otomatik kontrollerde işaretleniyor; hat numarası ve kurum adı gibi kriz kaynak bilgisinin uygulama katmanından verilmesi öngörülüyor (bkz. Bölüm İP2.9).
<!-- kaynak: PROJECT_MEMORY.md:423 · K18 PROJECT_MEMORY.md:66 -->

## İP1.3 Terapötik çerçeve ve davranış kuralları

Danışman cevaplarının uyması gereken davranış, literatüre dayanan bir terapötik çerçeve olarak yazıldı. Çerçevenin temeli Motivasyonel Görüşme'dir (MG; SAMHSA, 2019): iş birliği, kabul, şefkat ve uyandırma ruhu; açık uçlu soru, onaylama, yansıtma ve özetleme becerileri; değişim konuşmasının uyandırılması. MG uyumu için Motivasyonel Görüşme Tedavi Bütünlüğü kodlama el kitabındaki eşikler (Moyers vd., 2016) kullanıldı. Bunlara bilişsel davranışçı terapinin (BDT) temel ilkeleri, Marlatt ve Gordon'un kayma ile nüksü ayıran nüks önleme modeli (Larimer vd., 1999), kriz durumları için Stanley ve Brown'un Güvenlik Planı (Stanley ve Brown, 2012) ve empatiyi duygusal tepki, yorumlama ve keşif boyutlarında ölçen EPITOME çerçevesi (Sharma vd., 2020) eklendi. Damgalayıcı dilden kaçınmada NIDA'nın "Words Matter" kılavuzu, LLM'lerin sycophancy eğilimine karşı da Cheng vd. (2025) esas alındı.

Çerçeveyi üretimde ve değerlendirmede doğrudan kullanabilmek için iki belgeye dönüştürdük:

- 19 davranış yönergesi. Her yönerge bir terapötik durumu (ambivalans, inkâr, rol sınırının zorlanması, kayma sonrası utanç, hukuki kaygı vb.) ele alıyor ve o durumda danışmanın ne yapması, neden kaçınması gerektiğini yazıyor. Hukuki kaygı ve sanrılı söylem yönergeleri uzman onayı gelene kadar taslak durumunda.
- Yasak ifade listesi. Etiketleme, emredici kip, boş güvence, utanç büyütme, zararlı normalleştirme, ahlaki yargılı klinik dil, rol sınırı ihlali ve kriz yasakları başlıklarında 8 kategoride 38 ifade var. Kriz yasakları kesin kuraldır, tek bir eşleşme kaydı eler. Rol sınırı ifadeleri ise doğru retlerde de ("ben teşhis koyamam") geçtiği için yalnızca işaretlenir.
<!-- kaynak: docs/arastirma-notlari.md §C–F, §M–O, §R · docs/davranis-kartlari.md · plan.md:1622-1669 · configs/filters.yaml:9-58 · reports/analiz/2026-09-16-buyuk-harf-kapisi.md -->

## İP1.4 Veri karışımı: senaryo, bağımlılık türü ve mesaj biçimi

Bağımlılık türlerinin ağırlıkları Türkiye verilerine göre belirlendi: alkol ~%30, tütün ~%25, kumar ~%25, madde ~%20. Dayanak olarak TUBİM verileri (15–64 yaşta tütün kullanımı ~%47, alkol ~%22,1, yasa dışı madde %2,7) ve Yeşilay'ın 2025 kumar verisi (yetişkinlerin %10,1'i, yaklaşık 6,8 milyon kişi) alındı. Tedaviye geliş motivasyonu (içsel, aile baskısı, yasal zorunluluk) ayrı bir eksen olarak modellendi.
<!-- kaynak: plan.md:236-249 · PROJECT_MEMORY.md:70 (K22) -->

`v0.1.0` sürümünün senaryo ve bağımlılık türü dağılımı Şekil 2'de görülüyor. Öneri formunun Tablo 4'ündeki senaryo tipleri bu dağılımda yer alıyor, iki farkla. Kriz yönetimi dilimi, kriz davranışı uzman ve etik kurul onayı gerektirdiği için bu dönem üretilmedi (Bölüm İP1.10). Bilgilendirme senaryosunu ise bilerek az tuttuk ve RAG modülüne (İP3) bıraktık, çünkü güncel ve doğru bilginin modelin ezberinden çok doğrulanmış kaynaklardan gelmesi gerekiyor. Yasa dışı madde türü seed korpusunda hiç bulunmadığı için bu dönem temsil edilemedi.

![Şekil 2. v0.1.0 veri kümesinde senaryo ve bağımlılık türü dağılımı (genel yetenek koruma amaçlı 18 replay kaydı hariç, n = 1040). Kriz dilimi işaretli kayıt sayısı 0'dır; senaryo alanı "kriz" olan 2 kayıt bu dilime ait değildir.](reports/analiz/sekiller/s3-dagilim.png)
<!-- kaynak: datasets/v0.1.0/manifest.json · reports/analiz/2026-10-21-rapor-sekiller.md · reports/analiz/2026-10-20-ip1-olcutler.md:89 -->

Veri kümesi, sahada karşılaşılacak etkileşim tiplerine göre dilimlere ayrıldı: tek turlu danışmanlık (%40,3), çok turlu danışmanlık (%34,1), rol sınırı (%18,1), nazikçe karşı çıkma (%15,0), inkâr (%4,4), RAG bağlamıyla cevaplama (%23,9) ve genel yetenek koruması (replay, %1,7). Dilimler örtüşebildiği için toplam %100'ü geçiyor.

Danışan mesajlarının biçimine de ayrıca bakıldı. Seed korpusunda mesajların ortanca uzunluğu 36 sözcük ve %96,8'i düzgün noktalamayla bitiyor; bu, gerçek kullanıcıdan çok onu üreten modelin üslubuna benziyor. Kısa (1–8 sözcük), orta ve uzun mesajlar için hedef oranlar bu yüzden tanımlandı. `v0.1.0`'da dağılım kısa %35,6, orta %29,1, uzun %35,3 olarak gerçekleşti.
<!-- kaynak: datasets/v0.1.0/CARD.md:22-59 · plan.md:311-350 (K42) -->

## İP1.5 Üretim boru hattı

Talimat örnekleri seed'lerden şu adımlarla üretildi (Şekil 1):

1. Seed seçimi. Değerlendirme setlerinde kullanılan seed'ler dışarıda bırakılıp taksonomiye göre tabakalı seçim yapılır.
2. Üretim. Her kayıt için danışan mesaj(lar)ı, danışmanın reasoning'i (thinking) ve danışman cevabı yazılır. Bu iş LLM subagent'larıyla, davranış yönergeleri ve yasak listesi bağlama konarak yapıldı.
3. Otomatik kontroller. Kayıt sırasıyla şema geçerliliği, tur yapısı, dilim ve bağlam kuralları, thinking'in Türkçe olması, yasak ifade ve telefon numarası taraması, soru sayısı (cevap başına en çok bir soru), yansıtma/soru oranı, uzunluk ve thinking/cevap oranı sınırları ile exact-duplicate denetiminden geçer. Herhangi bir kontrolden geçemeyen kayıt elenir.
4. LLM-judge. Kontrollerden geçen kayıtları bir değerlendirici model EPITOME empati boyutları, MG uyumu, tuzak ihlali, klinik güvenlik ihlali, rol sınırı ihlali ve grounding (hallucination) açısından puanlar. Klinik güvenlik ihlali ya da hallucination içeren kayıtlar derlemede elenir.
5. Immutable sürüm. Kalan kayıtlar sürüm numarasıyla derlenir. Her sürümün bir manifesti (girdi dosyasının SHA-256 özeti, kod sürümü, tarih, eleme gerekçeleri) ve *Datasheets for Datasets* yapısında bir veri kartı (Gebru vd., 2021) vardır. Var olan bir sürümün üzerine yazılamaz.

Boru hattındaki bütün LLM çağrıları content hash ile cache'lendi, yani aynı girdi her zaman aynı çıktıyı veriyor. Bunu sınamak için beş sürüm baştan üretildi ve bayt bayt aynı çıktı.
<!-- kaynak: plan.md:90-99, :813-828 · src/checks.py:477-617 · src/build.py:40-125 · src/llm.py · PROJECT_MEMORY.md:206 (K145) -->

## İP1.6 Ön işleme, biçim ve anonimleştirme

Öneri formunda sayılan ön işleme adımlarının karşılığı aşağıdadır.

Her kayıt, doğrulanan bir şemaya göre JSONL satırı olarak saklanıyor. Şemada kimlik, dilim, senaryo, bağımlılık türü, motivasyon, MG süreci, yaş grubu, tur tipi, mesajlar, bağlam, kaynak seed'ler, kriz/negatif örnek işaretleri, judge sonucu ve üretim meta verisi yer alıyor. Mesajlar sistem / danışan / danışman rolleriyle etiketlenip modelin chat template'indeki rollere eşleniyor.

Her eğitim örneği, kullanıcıya gösterilmeyen bir reasoning (thinking) ile danışman cevabından oluşuyor. Çalışma sırasında modelin resmî chat template'inin eğitimde thinking içeriğini sessizce sildiğini fark ettik. Template'i yalnızca son danışman turunun thinking'ini koruyacak şekilde yamaladık. Yamalı template'in ürettiği prompt, resmî template'in thinking açık hâliyle bayt bayt aynı.

Veri tamamen sentetik ve gerçek kişi verisi içermiyor. Bunu ayrıca ölçtük: e-posta, web adresi, cep ve sabit telefon, sağlama toplamı tutan TC kimlik numarası, IBAN, kart numarası, açık adres ve doğum tarihi desenlerinin hiçbiri 1058 kayıtta çıkmadı. Desenler her çalıştırmada bilinen örnekler üzerinde kendini sınıyor. Kişi adı taraması yapılmadı.

Öneri formundaki pozitif/negatif/nötr duygu tonu etiketlemesi bu dönem yapılmadı. Bu etiket İP4'teki duygu analizi ajanının girdisi olacağı için şemasının o ajanla birlikte belirlenmesi planlanıyor.
<!-- kaynak: src/schemas.py:12-44 · configs/chat_template_train.jinja · PROJECT_MEMORY.md:92 (K44) · reports/analiz/2026-10-20-ip1-olcutler.md:68-91 · docs/rapor/oneri-rapor-esleme.md:53 -->

## İP1.7 Kalite güvencesi: LLM-judge ve uzman değerlendirmesi

LLM'lerin kendi çıktılarını ya da aynı ailedeki modellerin çıktılarını daha yüksek puanladığı biliniyor (Zheng vd., 2023). Bu etkiyi kendi verimizde de ölçtük. Aynı kayıtlara verilen ortalama puan bağımsız bir judge'da 0,825, üreticiyle aynı ailedeki judge'da 0,878 (+%6,4), üreticinin kendisinde 0,924 (+%11,9) çıktı. Şişme öznel boyutlarda görüldü (MG uyumu 3,90 / 4,55 / 4,80), context fidelity'de görülmedi (4,95 / 4,90 / 4,95). Dönem içinde judge modeli sırasıyla Qwen3.8-27B, Gemini 3.8 Flash ve kör iş dosyalarıyla çalışan Claude Sonnet oldu. `v0.1.0`'da 894 kaydı Claude Sonnet, 146 kaydı Gemini değerlendirdi; 18 replay kaydı muaf tutuldu. Judge'ın tutarlılığını da ölçtük: aynı kayıtlar yeniden puanlandığında context fidelity ve MG uyumunda puanların %100'ü, duygusal tepkide %70'i, yorumlamada %65'i aynı kaldı.
<!-- kaynak: PROJECT_MEMORY.md:91 (K43), :93 (K45), :157 (K97), :158 (K98) · datasets/v0.1.0/CARD.md:61-69 -->

Veri kümesinden rastgele seçilen 70 kaydın 50'sini bir klinik uzman puanladı (Tablo 1). Uzman kayıtların %68'ini doğrudan kabul etti, %22'sini sınırda buldu, %10'unu reddetti. Sınırda olanlarla birlikte kabul edilebilir oran %90. Klinik güvenlik ve rol sınırı ihlali ne uzmanın ne de judge'ın değerlendirmesinde 50 kaydın hiçbirinde çıkmadı.

| Ölçü | Uzman | LLM-judge |
|---|---:|---:|
| Kabul / sınırda / ret | 34 / 11 / 5 | — |
| Klinik güvenlik ihlali | 0/50 | 0/50 |
| Rol sınırı ihlali | 0/50 | 0/50 |
| Tuzak ihlali | 0/50 | 2/50 |
| Duygusal tepki (0–2) | 1,73 | 0,98 |
| Keşif (0–2) | 1,77 | 1,71 |
| Context fidelity (1–5) | 4,67 | 4,67 |
| Dil bütünlüğü (1–5) | 4,57 | 5,00 |

> Tablo 1. Uzman ve LLM-judge değerlendirmesinin karşılaştırması (50 kayıt). Kaynak: `reports/analiz/2026-09-14-uzman-puanlama-analizi.md`.

Judge puanları ortalamada uzmana yakın, ama kayıt düzeyinde uzmanla neredeyse hiç ilişkili değil. Boyutlar arası korelasyon −0,13 ile 0,26 arasında kaldı; uzmanın reddettiği beş kaydın beşine judge dil ve kısalıkta tam puan verdi. Bu yüzden judge'ı kalite puanı için değil, güvenlik ihlali ve hallucination gibi ağır hataları elemek için kullandık. Rubriği uzman yorumlarına bakarak dokuz kez yeniden yazdık; yorumlama boyutunda uzmanla birebir uyum %30'dan %62'ye çıktı. Yine de hiçbir boyut uzmanın genel kabul/ret kararını ayırt edemedi (AUC 0,45–0,57). Uzman yorumları veri tasarımına da yansıdı. Uzman, kayıtların %97'sinin soruyla bitmesini ve MG süreçlerinin çoğunun "ilişki kurma" aşamasında kalmasını (70 kayıttan 57'si) eleştirmişti; sonraki sürümlerde bu iki oran ayrıca izlendi.
<!-- kaynak: reports/analiz/2026-09-14-uzman-puanlama-analizi.md:13-123 · PROJECT_MEMORY.md:108 (K54), :120 (K58), :161 (K104) -->

## İP1.8 Değerlendirme setleri

İP2'de modelleri sınamak için veri kümesinden ayrı, elle yazılmış değerlendirme setleri hazırlandı (Tablo 2). Setler eğitimde kullanılan seed'lerle çakışmayacak şekilde ayrıldı. Terapötik kalite setleri dev / test / locked olarak üçe bölündü. Locked set yalnızca iki kez, başlangıçta ve final ölçümünde açılıyor; model seçerken test setine fazla uyum sağlamanın önüne böyle geçiliyor.

| Set | Eksen | Öğe |
|---|---|---:|
| golden.dev / golden.test / golden.locked | Terapötik kalite | 48 / 48 / 48 |
| safety_crisis | Güvenlik ve kriz (15 risk + 5 kontrol) | 20 |
| forgetting_smoke | Genel yeteneğin korunması | 30 |
| context_fidelity (+ gerçek bağlam, çelişkili bağlam) | Context fidelity | 20 + 15 + 15 |
| sycophancy | Sycophancy / özerklik | 24 |
| cok_turlu | Çok turlu tutarlılık | 10 konuşma × 4 tur |
| olcek5k-ref.v1 | Referanslı metin benzerliği (BLEU/ROUGE) | 200 |

> Tablo 2. Değerlendirme setleri. Kaynak: `evals/` · `reports/analiz/2026-10-20-rapor-referans-seti.md`.
<!-- kaynak: wc -l evals/*.jsonl · PROJECT_MEMORY.md:79 (K31) · reports/analiz/2026-09-29-cok-turlu-set.md -->

## İP1.9 Elde edilen sürümler ve ölçeklendirme

Veri kümesi 12 Eylül'de 20 kayıtlık bir vertical slice ile başladı ve 22 ara sürümde büyüdü (Şekil 3). Ara sürümlerin bir kısmı tek bir hipotezi sınamak için kurulan, ana hatta alınmayan deney kollarıdır; İP2'deki doz-yanıt kolları da bunlardandır.

![Şekil 3. Veri kümesi sürümlerinin gelişimi. Her sürüm immutable'dır ve manifestinde girdi özetini taşır; gri sütunlar ana hatta alınmayan deney kollarıdır.](reports/analiz/sekiller/s4-surumler.png)
<!-- kaynak: datasets/*/manifest.json · reports/analiz/2026-10-21-rapor-sekiller.md -->

Dönemde iki araştırma sürümü kesinleşti; bu sürümler artık değiştirilmiyor. 24 Eylül 2026 tarihli `v0.1.0`'da 1.132 aday kayıttan 1.058'i kabul edildi; elenen 74 kaydın 56'sı hallucination, 14'ü klinik güvenlik ihlali, 4'ü güvenlik karantinası nedeniyle elendi. 29 Eylül 2026 tarihli `v0.1.1`'de aynı 1.058 kaydın 1.036'sında thinking yeniden yazıldı. İlk sürümün thinking'lerinde biçimsel kalıplar ağır basıyordu: %30,6'sında "sormuyorum" gibi meta-yorumlar, %22,8'inde işaret simgeleri vardı. Yeni sürümde bu oranlar %3,1 ve %0,2'ye indi. İP2'deki 26B ince ayarı bu sürümle yapıldı. Veri kümesi Hugging Face'te paylaşıldı; bu sürümler deponun `refined` serisidir (https://huggingface.co/datasets/yildirim34/birag-dataset/tree/refined).
<!-- kaynak: datasets/v0.1.0/CARD.md:1-8, :71-77 · datasets/v0.1.1/CARD.md:1-42 -->

Hacmi büyütmek için dönem sonunda üç aşamalı bir üretim hattı (ölçek-5k) kurduk. A aşamasında seed'den danışan tarafı yazılıyor. B aşamasında danışman cevabı ve thinking, seed görülmeden yazılıyor. C aşamasında daha güçlü bir model kayıtlarda hata arıyor, kaydı düzeltiyor ya da düşürüyor. Otomatik kontroller her aşamada çalışıyor. Hattı kurmadan önce 60 kayıtlık bir pilot yaptık ve elle okumada 17 ciddi kusur bulduk. Bunların 11'i, tek modelin seed metnini cevaba sızdırmasından kaynaklanıyordu; seed'i cevap yazarından gizleme kararı buradan çıktı. Kalibrasyon turunda C aşaması 50 kaydın 27'sini düzeltti, 1'ini düşürdü. Hat 5.000 kayıt (200 parça × 25) için tasarlandı; 20 Ekim 2026 itibarıyla 200 parçanın 144'ü B aşamasını bitirmiş ve 3.598 ara kayıt üretilmişti. Ancak İP2'deki bulgular (Bölüm İP2.8) veri kalitesinde, özellikle kriz örneklerinin eksikliğinde ve bazı abartılı kalıplarda düzeltilmesi gereken noktalar olduğunu gösterdi. Bu yüzden önce kaliteyi artırmaya, 10.000 örneği ondan sonra aynı hatla üretmeye karar verdik.
<!-- kaynak: reports/analiz/2026-10-20-olcek5k-plan.md · reports/analiz/2026-10-20-haiku-pilot-okuma.md:12-33 · PROJECT_MEMORY.md:339 (K279) · reports/analiz/2026-10-20-ip1-olcutler.md:14-22 -->

## İP1.10 Karşılaşılan sorunlar, öneriden sapmalar ve B planları

| Konu | Öneride | Gerçekleşen ve gerekçe |
|---|---|---|
| Forum verisi (Reddit, Quora vb.) | Kazıma ile toplama | Yapılmadı. Savunmasız bireylere ait sağlık verisi niteliğinde olduğundan etik kurul kararı olmadan toplanmadı. Açık Türkçe veri kümeleri tarandı, uygun gerçek kullanıcı verisi bulunamadı (kümeler çeviri ya da sentetik; oasst2'de yalnızca 10 Türkçe kullanıcı mesajı var). |
| Anonim gerçek terapi diyalogları | Kaynak olarak kullanım | Kullanılmadı; erişim ve etik onay süreci açık. Uzman yazımı korpustan kalıp düzeyinde bir Türkçe ifade bankası çıkarıldı, satırların kendisi eğitime girmedi. |
| Kriz yönetimi senaryoları | Tablo 4'te yer alıyor | Üretilmedi (0 kayıt). Kriz davranışı klinik uzman ve etik kurul onayı gerektiriyor. Güvenlik Planı'na dayalı 6 adımlı protokol taslağı hazır, iki adımı uzman kararını bekliyor. Kriz dilimi olmamasının İP2'deki bedeli ölçüldü (Bölüm İP2.8). |
| Otomatik üretim modeli | GPT-4, turkish-gpt2 | Claude Code ve subagent'ları (Claude Sonnet / Haiku). Öneri yazıldıktan sonra çıkan daha yetenekli modeller tercih edildi. Üretici model her kaydın meta verisinde yazılı; judge bias'ı ayrıca ölçüldü (Bölüm İP1.7). |
| Türkçe büyük/küçük harf | — | Standart küçük harfe çevirme Türkçe I/İ harflerini yanlış dönüştürüyor. Yasak ifade kontrolü bu yüzden 38 ifadenin 26'sını Türkçe büyük harfle, 14'ünü ASCII büyük harfle yazıldığında yakalayamıyordu. Türkçeye özgü bir case folding işlevi yazılıp bütün kontrollere uygulandı; kaçak 0'a indi. |
| Genel yetenek koruması (replay) | — | Hedef %15, gerçekleşen %1,7. Daha yüksek oranın forgetting'i azalttığı yalnızca deney kolunda gösterilebildi; ana hatta alınması gelecek döneme kaldı. |
| Duygu tonu etiketi | Pozitif/negatif/nötr | Yapılmadı; etiket şeması İP4'teki duygu analizi ajanıyla birlikte belirlenecek. |

> Tablo 3. Öneriden sapmalar ve uygulanan B planları. Kaynak: `docs/rapor/oneri-rapor-esleme.md` · `reports/analiz/2026-09-15-vahsi-dilim-kaynak-taramasi.md` · `reports/analiz/2026-09-16-buyuk-harf-kapisi.md`.

## İP1.11 Ara çıktılar

İP1 kapsamındaki ara çıktılar ekler bölümündedir:

- Ek 1-A: Veri kümesi kartları (`v0.1.0`, `v0.1.1`) ve manifestler (`refined` serisi, https://huggingface.co/datasets/yildirim34/birag-dataset/tree/refined)
- Ek 1-B: Kontrollü sözlük / taksonomi (`configs/taxonomy.yaml`)
- Ek 1-C: Terapötik çerçeve notları, 19 davranış yönergesi ve yasak ifade listesi
- Ek 1-D: Senaryo başına örnek talimat kayıtları (öneri formu Tablo 4'ün gerçekleşen karşılığı)
- Ek 1-E: Değerlendirme setleri ve değerlendirme protokolü
- Ek 1-F: Uzman brifingi ve uzman puanlama analizi
- Ek 1-G: Üretim ve kalite kontrol yazılımı (`src/`), analiz betikleri ve raporları (`scripts/analiz/`, `reports/analiz/`); kaynak kodun tamamı: https://github.com/enveryildirim/birag-data-generation

## Kaynaklar

- Cheng, M. vd. (2025). Sycophantic AI decreases prosocial intentions and promotes dependence. arXiv:2510.01395.
- Gebru, T., Morgenstern, J., Vecchione, B., Wortman Vaughan, J., Wallach, H., Daumé III, H. ve Crawford, K. (2021). Datasheets for datasets. *Communications of the ACM*, 64(12), 86–92.
- Larimer, M. E., Palmer, R. S. ve Marlatt, G. A. (1999). Relapse prevention: An overview of Marlatt's cognitive-behavioral model. *Alcohol Research & Health*, 23(2), 151–160.
- Moyers, T. B., Manuel, J. K. ve Ernst, D. (2016). *Motivational Interviewing Treatment Integrity Coding Manual 4.2.1*. University of New Mexico, CASAA.
- SAMHSA (2019). *Enhancing Motivation for Change in Substance Use Disorder Treatment* (TIP 35). Substance Abuse and Mental Health Services Administration.
- Sharma, A., Miner, A. S., Atkins, D. C. ve Althoff, T. (2020). A computational approach to understanding empathy expressed in text-based mental health support. *Proceedings of EMNLP 2020*, 5263–5276.
- Stanley, B. ve Brown, G. K. (2012). Safety planning intervention: A brief intervention to mitigate suicide risk. *Cognitive and Behavioral Practice*, 19(2), 256–264.
- Zheng, L. vd. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. *NeurIPS 2023 Datasets and Benchmarks Track*.

# Gerçekleşme

| Başarı ölçütü (öneri formu) | Hedef | Gerçekleşen | Durum |
|---|---|---|---|
| Talimat örneği sayısı | 10.000 | Kesinleşmiş sürümde 1.058 kayıt (%10,6); ölçek-5k hattında 3.598 ara kayıt üretildi. 10.000'e kalite iyileştirmelerinden sonra tamamlanacak | Kısmen |
| Hedef senaryolarla uyumlu ve doğru biçimli | %90 | Kontrollerden ve judge'dan geçme %93,5 (1.058/1.132); senaryo listesine uyan %90,8 (944/1.040); biçim kontrolleri %100 | Karşılandı |
| Dil modeliyle uyumlu | %95 | Şema + chat template, thinking korunarak: %100 (1.058/1.058) | Karşılandı |
| Türkçe veride olumlu değerlendirme | %70 | Uzman doğrudan kabul %68; sınırda dahil %90 (tek uzman, 50 kayıt) | Sınırda |
| Etik ve anonim | %100 | Tamamen sentetik; 9 PII deseninde 0 eşleşme (%100); sert yasak ifade 0 | Karşılandı (kişi adı taraması ve etik kurul süreci açık) |

> Tablo 4. İP1 başarı ölçütlerinin gerçekleşme durumu. Kaynak: `reports/analiz/2026-10-20-ip1-olcutler.md` · `reports/analiz/2026-09-14-uzman-puanlama-analizi.md`.

Senaryo uyumu, dil modeli uyumu ve anonimlik ölçütleri hedefin üzerinde gerçekleşti; uzman kabulü sınırda kaldı. Eksik olan hacim: dönem sonunda kesinleşmiş sürümde 1.058 kayıt var. Dönemin ilk yarısında hacim yerine ölçüm altyapısına zaman ayırdığımız için bu fark beklenen bir sonuçtu. O sürede kalite kontrolleri, bias'ı ölçülmüş bir judge, uzman kalibrasyonu ve yeniden türetilebilir sürüm düzeni kuruldu. Altyapı hazır olduktan sonra hacim hızla büyüyebildi; üç aşamalı ölçek-5k hattı ilk günlerinde 3.598 ara kayıt üretti. Yine de şimdilik hacmi zorlamak yerine kaliteyi artırmayı seçtik. İP2'de görülen sorunlar (kriz örneklerinin eksikliği, abartılı sınır kalıpları) giderildikten sonra 10.000 örneği aynı hatla üreteceğiz.

Kriz dilimi ayrıca ele alınmalı. Uzman ve etik kurul onayı olmadan bu dilimi üretmedik; İP2'de bu eksikliğin ince ayarlı modelde kriz yönlendirmesini zayıflattığı görüldü (Bölüm İP2.8). Ölçek-5k üretiminde de risk sinyali taşıyan kullanıcı turu olmadığından hacmin artması bu açığı kapatmayacak. Sonraki dönemin önceliği bu yüzden uzman onaylı kriz protokolüne dayanan bir kriz dilimi üretmek ve etik kurul sürecini tamamlamak. Uzman değerlendirmesinin ikinci bir uzmanla genişletilip uzmanlar arası uyumun ölçülmesi ve duygu tonu etiket şemasının İP4 ile belirlenmesi de gelecek döneme kaldı. Veri kümesi, sözlük ve değerlendirme setleri İP2'nin girdisi oldu. Bilgilendirme senaryolarının RAG'e bırakılması da İP3 ile iş bölümünü belirliyor.
<!-- kaynak: reports/analiz/2026-10-20-olcek5k-kalip-kriz.md:117-131 -->
