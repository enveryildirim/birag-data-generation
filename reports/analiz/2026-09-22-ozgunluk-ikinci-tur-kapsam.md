# Özgünlük taraması ikinci turu — kapsam envanteri
**Betik:** `scripts/analiz/2026-09-22-ozgunluk-ikinci-tur-kapsam.py` · **Tarih:** 2026-09-22  
**Girdi:** `docs/tez/katki-defteri.md` SHA256 `b42c7be2be81e798`  
**Aralık:** T146–T245
---
## Neden
Birinci tur (T67-T69, 2026-09-16) defterde **115 satır** varken yapılmıştı.
Defter o günden beri büyüdü ve aradaki kayıtlar hiç taranmadı. Bu envanter
ikinci turun **neye baktığını ve neye bakmadığını** sayılabilir kılar.

⚠️ Küme eşlemesi **türetilmedi** — editoryal karardır (Kural 6), betikte
elle ilan edilir. Betik yalnız uygular ve kapsanmayanı sayar.
---
## 1. Kapsam
| | |
|---|---:|
| aralıktaki katkı satırı | **100** |
| taranan kümeye giren | **52** |
| **hiç taranmayan** | **48** |
| ilan edilip defterde bulunamayan | 0 |

➡️ Aralığın **%52**'i tarandı.

---
## 2. Taranan kümeler
| Küme | İddia | Üye | Kayıtlar |
|---|---|---:|---|
| `gurultu-tabani` | Ölçütün gürültü tabanı, tohum yayılımı, ön kayıtlı eşiğin geçerliliği | 13 | T159, T160, T174, T175, T178, T181, T182, T183, T186, T241, T242, T243, T245 |
| `judge-tekrarlanabilirlik` | Aynı judge'a iki çekiliş, önbellek/hafıza bulaşması, tek-ayrıntı sondası | 6 | T173, T174, T175, T178, T238, T241 |
| `sozluk-kapisi-goodhart` | Sözlükle kurulmuş kapı edimi değil formülü tanır; kapı şablonu zorunlu kılar | 10 | T192, T194, T196, T200, T201, T202, T205, T206, T226, T235 |
| `turkce-bicimbilim` | Türkçe çekim/ek sert kapının düz alt dizge aramasını deliyor | 3 | T153, T154, T199 |
| `test-orakl` | Kapıyı denetleyen betik kapının koşulunu kopyalıyor | 2 | T147, T151 |
| `lora-yayilim` | Belirleyici olan güncellemenin büyüklüğü değil yayılımı; güvenlik ekseni | 5 | T184, T185, T186, T187, T188 |
| `veri-kusuru-kaskadi` | Alan dolu, biçimi doğru, değeri yanlış; kural yazılı, kapı yok | 9 | T193, T217, T220, T221, T222, T223, T224, T236, T237 |
| `anotator-bagimsizligi` | Üç anotatörün üçü de aynı model ailesinden ⇒ uyum yukarı çekiliyor | 4 | T227, T228, T229, T230 |
| `kapi-bilesimi` | İki tutarlı kapı birlikte makul cevabı puanlanamaz kılıyor; aşırı red | 3 | T176, T177, T189 |
| `cot-sadakati` | İç muhakeme cevabın yaptığını yapmadığını ilan ediyor; denetleyen kapı yok | 1 | T239 |
| `thinking-orani` | Üretim emeğinin yarısından fazlası thinking'e gidiyor; eğitilen setten sapma | 1 | T232 |

---
## 3. ⛔ Hiç taranmayanlar
Bu kayıtlar ikinci turda **literatüre karşı aranmadı.** Çoğu depoya özgü
mühendislik/vaka kaydıdır ve genelleştirilebilir bir iddia taşımaz — ama
*bu da bir karardır*, ölçüm değil. Üçüncü tur buradan başlar.

| # | Başlık (kısaltılmış) |
|---|---|
| T146 | tekrar BAYRAĞININ İLAN EDİLMİŞ BAĞIMSIZLIĞININ ÖLÇÜLEBİLİR BİR TABANI VAR — VE ARŞİVDE BİR ÖRNEĞİ. src/dejener |
| T148 | BİR MUAFİYETİN BEDELİ, KURALI YENİDEN YAZARAK DEĞİL, KOŞULU ÇEVİRİP AYNI KURALI YENİDEN KOŞARAK ÖLÇÜLÜR. T141/ |
| T149 | BİR SERT KAPI, ÜRETİM SÜRÜMÜ İLERLEYİNCE KENDİ KENDİNE KAPANDI — VE KAPANMASI HİÇBİR HATA VERMEDİ. run_checks  |
| T150 | BİR AD, İDDİA DEĞİLDİR — VE §7b'NİN YEDİ YANLIŞ POZİTİFİNİN HEPSİ BU KARIŞIKLIKTAN GELİYORDU. T149'un iki parç |
| T152 | OKUNMAYAN BİR SİNYAL, SİNYAL DEĞİLDİR — VE KUYRUĞUN DEĞERİ İÇİNDEKİLER DEĞİL, OKUNMASI OLDU. src/checks.py bir |
| T155 | BİR KAPININ «0 İHLAL» DEMESİ, KAPININ BAKABİLDİĞİ YERDE 0 İHLAL OLDUĞU DEMEKTİR — VE BAKAMADIĞI YERDE ORAN %26 |
| T156 | BİR METİN DÜZELTMESİ, O METNE VERİLMİŞ YARGIYI DA GEÇERSİZ KILAR — VE BU İLAN EDİLEBİLİR BİR ŞEYDİR. datasets/ |
| T157 | ELLE YAZILMIŞ BİR LİSTE, OLGUNUN ANCAK AKLA GELEN KISMINI ÖLÇER — VE KAÇAN, KORPUSUN EN BÜYÜK İKİNCİ KALIBIYDI |
| T158 | ŞERH (T184): içindeki *«iki Pareto kapısını da geçen tek kol»* nitelemesi çürüdü — iki kapsam üç tohumla ayırt |
| T161 | EKSEN 1'İN NEDEN HİÇ KOŞULMADIĞI ARTIK BİR TAHMİN DEĞİL, ÖLÇÜM. Pareto'nun üçüncü adımı bu projede bir kez bil |
| T162 | EKSEN 1 İLK KEZ ÖLÇÜLDÜ — ÜSLUP BÜYÜK ÖLÇÜDE DÜZELDİ, KALİTE BİLEŞİĞİ OYNAMADI, GÜVENLİK BAYRAĞI YÜKSELDİ. Eng |
| T163 | BİR DESENİN GENİŞLETİLMESİ BEDAVA MI DEĞİL Mİ, DESENİN DEĞİL UYGULANDIĞI YERİN ÖZELLİĞİDİR. T150 iki boşluk il |
| T164 | T141'İN «BUGÜN BEDELİ SIFIR AMA SIZINTI GERÇEK» KALEMİ KAPATILDI — VE BEDELİ GERÇEKTEN SIFIR ÇIKTI. Zaman+kayn |
| T165 | BİR SEZGİNİN BİR EKSENDE İŞE YARAMASI, ÖTEKİ EKSENDE İŞE YARAYACAĞI ANLAMINA GELMEZ — ÖNERDİĞİM DÜZELTME ÖLÇÜL |
| T166 | KUSURLAR SAYILARIN ARASINDA DEĞİL, RAPORLARIN ARASINDA SAKLANIYORDU — VE TEK SAYFALIK BİR RAPOR İLK KOŞUSUNDA  |
| T167 | BİR EŞLEŞTİRMEYİ KATLAMAK, METNİ KATLAMAKLA AYNI ŞEY DEĞİLDİR — VE AYNI SAYIYA ÜÇ DENEMEDE ULAŞILDI, İLK İKİSİ |
| T168 | ALINTIDA EDAT DÜŞMESİ — MODEL TIRNAK İÇİNE ALIRKEN CÜMLENİN VURGUSUNU TAŞIYAN ÖGEYİ ATIYOR. Yayımlanmış sette  |
| T169 | ÖNCEDEN İLAN EDİLEN BİR ÖLÇÜT, DÜZELTMEYİ DOĞRULANABİLİR YAPAR — VE 16 ALINTI BİREBİR HÂLE GETİRİLDİ. T168 kus |
| T170 | BİR YANLIŞ POZİTİF SINIFINI AFFETMEK İLE ETİKETLEMEK AYNI ŞEY DEĞİLDİR — İLKİ KAPININ GÜCÜNÜ, İKİNCİSİ YALNIZ  |
| T171 | ELLE VERİLMİŞ BİR HÜKÜM, VERİLDİĞİ METNE BAĞLIDIR — VE BUNU SÖYLEYEN BİR ŞEY YOKSA OKUMA HER SÜRÜMDE SIFIRDAN  |
| T172 | BİR MEKANİZMAYI TEK KAPIYA YAZMAK, ÖTEKİ KAPILARDA AYNI EKSİĞİ BIRAKMAKTIR. T171'in okuma defteri yalnız yapıs |
| T179 | BİR ÖRNEKLEM KAYBININ «RASTGELE Mİ» OLDUĞU KAYDIN ÖZELLİKLERİNE BAKARAK ANLAŞILMAZ — KAYIP BORU HATTININ ÖZELL |
| T180 | YENİDEN KOŞULABİLİR BİR BETİKTE AD KİMLİKTİR, TARİH DEĞİL — K126 TEK SEFERLİK ÖLÇÜMLER İÇİN YAZILMIŞTI. K126 r |
| T190 | BİR KAPSAMA BOŞLUĞUNU KAPATMADAN ÖNCE ONU KİMİN AÇTIĞINI SORMAK GEREKİR. Veri üretimine dönülürken parti sıray |
| T191 | EK (üretimden önce yakalandı): ilk çözümde hedeflenen tohumlar parti BAŞINA yığılmıştı (rol_siniri blok1'de 12 |
| T195 | KAYIT KAYIT DENETİM, EKSİK KAYDI GÖREMEZ — VE BİR GEREKÇEYİ BETİĞE YAZMAK, ONU KAYDA YAZMAK DEĞİLDİR. v6-parti |
| T197 | BİR SINIFIN ADI DAVRANIŞI SÖYLER; BEN ADI TUTUP DAVRANIŞI TERSİNE ÇEVİRMİŞİM. baglam_davranisi beyanı ilk kez  |
| T198 | BİR HEDEF LİSTESİ ÖLÇÜMDEN TÜRETİLMİYORSA, ÖLÇÜM DEĞİŞTİĞİNDE DE AYNI KALIR VE KAPANMIŞ AÇIĞI KOVALAMAYA DEVAM |
| T203 | SABİT DIŞLAMASI OLAN BİR TÜRETME KURALI, AÇILAN AÇIĞI HİÇ GÖREMEZ — T198'İN DERSİNİN AYNADAKİ HÂLİ. T198 hedef |
| T204 | AYNI ŞEYİ GÖSTERDİĞİ VARSAYILAN İKİ ALAN HİÇ BİRLİKTE GÖRÜNMÜYORSA, İKİSİ AYNI ŞEYİ GÖSTERMİYORDUR. T199'un SE |
| T207 | TEK YÖNLÜ BİR AÇIK ÖLÇÜSÜ, DENGESİZLİĞİN YARISINI YAPISAL OLARAK GÖRMEZ — VE GÖRMEDİĞİ YARI, GÖRDÜĞÜNDEN BÜYÜK |
| T208 | BİR RAPORUN VARSAYILAN ETİKETİ BİR İDDİA TAŞIYORSA, O İDDİA HİÇ YAPILMAMIŞ OLABİLİR — VE DEVRALINAN ŞERH DEVRA |
| T209 | BİR KALIP KURALININ İHLALİ ANCAK İŞ BİTTİKTEN SONRA GÖRÜNÜYORSA, HATIRLATMA DEĞİL KAPI GEREKİR — VE İKİSİ AYNI |
| T210 | BİR ÖLÇÜT EŞİĞİNİ SÖYLEMİYORSA, EŞİĞİ UYGULAYAN KOYAR — VE ALTI KEZ ÜST ÜSTE AYNI YÖNE KARAR VERDİYSEM İŞLEYEN |
| T211 | BİR DÜZELTME KURALI DOĞRU YÖNDE OLABİLİR VE YİNE DE PRATİKTE ATIL OLABİLİR — YÖNÜ ÖLÇMEK YETMEZ, HIZINI DA ÖLÇ |
| T212 | BİR ELEME KARARI VERİYE YAZILMAZSA, KARARIN ÖMRÜ ONU VERENİN HAFIZASI KADARDIR — VE BUNU BİR TEKRAR GÖSTERDİ.  |
| T213 | BİR ÖN TARAMA YALNIZ İŞARETLEDİĞİ SATIRI OKUTUR; İŞARETLEMEDİĞİ SATIR ÜRETİM ANINA KADAR HİÇ OKUNMAZ — VE PART |
| T214 | is_negative PLANDA DONAR, RET İSE İÇERİKTEN DOĞAR — IZGARA HÜCRESİ TOHUMUN NE İSTEYECEĞİNİ BİLEMEZ. Plan v6-pa |
| T215 | BİR DOZ KAPISI BİRİMİ GÖRÜR, ADEDİ GÖRMEZ — VE ADET BİÇİMİ BULUNDURMA İLE ALMAYI AYNI CÜMLEYLE YAZAR. DOZ_SAYI |
| T216 | BİR DÜZELTME DOĞRU DOSYAYA YAZILABİLİR VE YİNE DE KORPUSA HİÇ ULAŞMAZ — ARADA YALNIZCA BİR SIRA VARDI VE O SIR |
| T218 | BİR ÖLÇÜMÜN DEĞERİ BULDUĞU ŞEYDE DEĞİL, NE ZAMAN BULDUĞUNDADIR — AYNI KAPI, AYNI KUSURU, OTUZ KAYIT YERİNE ON  |
| T219 | ÇÜRÜDÜ (T224). Aşağıdaki iddianın dayanağı olan %6'lık örtüşme, kayıtların YANLIŞ tohumlarla karşılaştırılması |
| T225 | ALTI PARTİ SONRA UFUK KURALI SIFIR HEDEF ÜRETİYOR VE KALAN ALTI TAVANIN DÖRDÜ TEK BİR EKSENDEN GELİYOR — ÜSTEL |
| T231 | YAKIN-TEKRARIN TEHLİKELİ OLUP OLMADIĞINI ÖRTÜŞMENİN BÜYÜKLÜĞÜ DEĞİL YERİ SÖYLER. T224'ün açık kalemi kapatıldı |
| T233 | PARTİ BOYUNU İKİYE KATLAMAK ÜÇ AYRI YERDE SESSİZ SEYRELME ÜRETTİ — ÇÜNKÜ N ÜÇ MODÜLDE, ORANLAR İSE SABİT SAYI  |
| T234 | ÇÜRÜDÜ — ve çürüten şey üçüncü koşuydu. Özgün iddia: *«kendi kendine yeterli bir brif kaynağın yerine geçmedi; |
| T240 | slice ALANININ ANLAMI v5 İLE v6 ARASINDA SESSİZCE DEĞİŞTİ — VE YAYIMLANMIŞ BİR SAYIYI BOZMADAN HEMEN ÖNCE YAKA |
| T244 | BİR ŞABLONDAKİ BİR BEYANI TÜRETMEYE ÇEVİRMEK, KOMŞUSUNU DÜZELTMEZ — ve komşu 178 kayda yanlış tarih yazdı. T24 |

---
## 4. ⛔ Bu envanterin sınırı
| | |
|---|---|
| ⛔ **Kapsam ≠ sonuç** | bir kaydın kümeye girmesi tarandığını gösterir, *iddiasının tek tek sorulduğunu* değil; küme düzeyinde arandı |
| ⛔ **Eşleme tek okuyucunun** | kümeleri ben kurdum (K30); başka bir okuyucu başka kümeler kurar ve kapsam yüzdesi değişir |
| ⚠️ **«Taranmadı» ≠ «özgün değil»** | taranmayan kayıt hakkında hiçbir şey iddia edilmiyor — ne lehte ne aleyhte |
