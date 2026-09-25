# Faz 4'ü bitirmek için ne kaldı — `plan.md`'den türetildi

**Betik:** `scripts/analiz/2026-09-16-faz4-kapanis-listesi.py` · **Tarih:** 2026-09-16  
**Girdi:** `plan.md` SHA256 `03890b9dc3e204b3` — Faz 4 bölümü

---

## Neden türetiliyor

⛔ T65'in dersi: *elle tutulan bir durum tablosu iki ayrı yalan söyleyebilir —
durum **bayatlar**, ve hiç uygulanmamış bir madde yıllarca **işaretsiz** durur.*
⇒ Faz 4'ün kalan işi elle özetlenmiyor; bölümdeki **her** açık madde okunup
**engel türüne** göre sınıflanıyor.

⭐⭐ **Asıl ayrım kalemlerin sayısı değil, KİMİN ELİNDE olduğu.**

| | |
|---|---:|
| Faz 4 maddesi (toplam) | **128** |
| ✅ kapalı | **67** |
| açık | **61** |

---

## Açık maddeler — engel türüne göre

| engel | madde | ben ilerletebilir miyim |
|---|---:|---|
| **onay** | **13** | ⛔ **hayır** — etik kurul · uzman · yürütücü · hukukçu |
| **mühür** | **6** | ⛔ **hayır** — `K31` mührü açılmadan karar verilemez |
| **ölçüm** | **10** | ✅ **evet** — yalnız zaman ister |
| **şerh** | **5** | ⚠️ kapanacak iş **değil** — tezde yazılacak sınırlılık |
| **çıkış** | **2** | 🎯 iş **değil** — Faz 4'ün HEDEFİ |
| **?** | **25** | ❓ **mekanik olarak sınıflandırılamadı** — elle okundu, aşağıda |

⚠️ **Sıra önemli:** bir madde hem *«uzman»* hem *«ölçülmeli»* sözcüğü
taşıyabilir; o zaman **onay baskındır**, çünkü onay gelmeden ölçüm yapılamaz.
Eşleme aşağıda ilan ediliyor ve sınıflandırılamayan madde `?` olarak
**görünür kalır**.

---

### onay — 13 madde

· TARAMANIN İKİNCİ TURU — ÜNİVERSİTE ERİŞİMİ GEREKİYOR (T66).  
· JUDGE'IN YANLIŞ POZİTİF ORANI UZMANA KARŞI HİÇ ÖLÇÜLMEDİ (T68) — ASİMETRİYİ SAVUNMAK İÇİN GEREKL…  
· HUKUKÇU ONAYI GEREKİYOR (T69) — YÜRÜTÜCÜ KALEMİ.  
· K76 YAZILMAMIŞ — YÜRÜTÜCÜ KALEMİ (T64), ama MALZEMESİ HAZIR (K162 · T89).  
· KATKI DEFTERİNİN BAŞLIĞI SATIRLARINI ANLATMIYOR (T64) — KARAR GEREKİYOR.  
· HANGİ TOHUM HAVUZU KULLANILACAK — KARAR AÇIK ama ÖN KOŞULU KALKTI (K161 · T88).  
· AMA DENEY KENDİ SORUSUNU DEĞİŞTİRDİ (T34).  
· ROL SINIRI BAYRAĞI İÇİN YEM ÖĞESİ GEREKİYOR (T59).  
· gd-024 UZMAN KALEMİ (Kural 3).  
· KURAL 8'İN MUAFİYET LİSTESİ EKSİK — judge iş dizini (istek/) oturum sonunda siliniyor ve o dosya…  
· GOLDEN SETİ RUBRİĞİN ÜÇTE BİRİNİ SINIYOR (K129 · T55).  
· KAPININ ANLAM EKSENİ ÖLÇÜLEMEDİ (T58).  
· rol-sınırı/yönlendirme (talimat ✅ K110, ilk parti ✅ K111)  

### mühür — 6 madde

· data/judged/* AYRICA MÜHÜRLÜ DEĞİL (T71).  
· AYNALAMA YÖNLENDİRME SAYILMAMALI — ama düzeltmesi İKİNCİ SET ister (T62).  
· Karşı kutbun bedeli kayda geçti (K110).  
· F7 bir eval iddiası olarak eklenecekse ÜÇÜNCÜ SET gerekir (K31).  
· kurum_yordam_ihlali hiçbir eval öğesinde İDDİA EDİLMİYOR.  
· K31 mühründe üretim tarafı açığı bulundu ve kapatıldı (K111).  

### ölçüm — 10 madde

· AMA KAYITTA HÂLÂ AÇIK — ilk gerçek koşuda doğrulanmalı (T70).  
· runs/*/eval/* KAYIT DİSİPLİNİ HİÇ SINANMADI (T70).  
· PLAN DÜZENLEMESİ ÜÇ KAPALI MADDEYİ SİLMİŞTİ (T80 turunda).  
· normalize._exact / _prefix / _contains HİÇ NORMALİZASYON KULLANMIYOR (T76).  
· A SİTESİNDE NFKD UYGULANMIYOR (T75).  
· D2 DOĞRULAMA KAPISI ÜRETİMDE SINANMADI (T46).  
· İç muhakemedeki rol ihlali kendi ekseninde ölçülmeli (T45).  
· RUBRİK KARŞILAŞTIRMASI KÜME SEÇİMİNE DUYARLI (T48).  
· DEJENERASYON EŞİĞİ TEK BİR KOLDAN KALİBRE EDİLDİ (T82).  
· 183 DEJENERE KAYDIN SEBEBİ BİLİNMİYOR (T82).  

### şerh — 5 madde

· KURAL 7 YÜZDESİNİN KENDİ DENETİMİ YOK (T64).  
· alinti_nrm'İN I↔ı AÇIĞI DURUYOR — KOŞULLU KALEM (T80).  
· alinti_dogrulanmadi kayıtları ELLE OKUNMALI.  
· DOZ EĞRİSİNİN OKUNMASINDA İKİ TUZAK — koşudan ÖNCE yazılı:  
· anlasilirlik ortancası 3  

### çıkış — 2 madde

· Çıkış kapısı: test eval'de plato + transfer korelasyonu sağlam  
· → datasets/v0.1.0/ + CARD.md + §8 rapor kanıtları  

### ? — 25 madde

· KAPSAM KARARI ASKIDA  
· KAPANIŞ SIRASI ARTIK BİR DÖNGÜ İÇERİYOR (T64).  
· SIRA BAĞIMLILIĞI — ilan-edilen-sha-denetimi EN SON koşmalı.  
· T51'İN NEGATİFİ İKİ SORGUYA DAYANIYOR (T67).  
· PLANDA motivasyon ADINDA BİR ANAHTAR VAR AMA TOHUMUNKİYLE AYNI DEĞİL (T79).  
· _keyword'DE iş → is ↔ isolation RİSKİ KAYIT ALTINDA, KAPALI DEĞİL (T84).  
· normalize._keyword KISA ANAHTARLARI YENİDEN GÖZDEN GEÇİRİLMELİ (T84).  
· i-SINIFININ YANLIŞ POZİTİF YÖNÜ ÖLÇÜLEMEZ (T73).  
· Eksen 3'ün aleti eksik (K108).  
· KAPSAM CÜMLESİ YENİDEN YAZILDI (T36).  
· Hakemlik geçerlilik filtresi de çıktı (T37)  
· KAPI SAYILARI JUDGE SÜRÜMLERİ ARASINDA KARŞILAŞTIRILAMAZ (T47).  
· Dört muafiyet hâlâ doğrulanamıyor  
· SIZINTININ SEBEBİ İÇİN NEDENSELLİK DENEYİ (T61) — YENİ JUDGE KOŞUSU İSTER.  
· (süperse edildi) GÜRÜLTÜ TABANI YANSIZ DEĞİL — Ö3 kısmen karşılandı.  
· KALAN 3 «KAYDI» BEYANLI AMA KAPANMADI  
· gd-024 ARTIK ÖLÜ DESEN VURUŞU VERİYOR  
· ERKEN DÖNEM KAYITLARI DENETLENEMEZ (T51).  
· İÇ MUHAKEMEDEN ALINTILAMA v8 EKSEN 2'DE 33 VAKA (T45 · T50).  
· Düzeltme ölçütün AİLESİNİ kapatmadı — kalıntı yansız değil (T38).  
· T34'ün tablosu düzeltilmeli — ÜÇÜNCÜ payda kusuru.  
· Adım kontrolü B/C/D/E'ye genişletilmeli  
· REPLAY SEYRELDİ — Eksen 3 bu koşuda tek başına yorumlanamaz.  
· Yönlendirme korpus düzeyinde yalnızca %3,6  
· tamamen yeniden üretilir  

⭐ **Elle okundu (Kural 6):** bu kovanın büyük çoğunluğu **kapanacak**
**iş değil, KAYIT** — ölçülmüş bir bulgunun şerhi ya da tezde
yazılacak bir sınırlılık (*«ERKEN DÖNEM KAYITLARI DENETLENEMEZ»*,
*«REPLAY SEYRELDİ»*, *«gürültü tabanı yansız değil»*). ⛔ İçlerinden
gerçekten **iş** olanlar: `T61`'in nedensellik deneyi (yeni judge
koşusu), `T34`'ün payda düzeltmesi, adım kontrolünün B/C/D/E'ye
genişletilmesi, `K108`'in Eksen 3 aleti ve dört doğrulanamayan
muafiyetin elle okunması.

⚠️ **Bu sayı mekanik değil, sınıflandırıcının SINIRIDIR ve öyle
bırakılıyor** — anahtar sözcük listesini bu 25 maddeye uydurmak
sınıflandırıcıyı kendi girdisine **aşırı uydurmak** olurdu ve
sonraki maddede yine tutmazdı.

---

## ⭐ Faz 4'ün çıkış kapısı

`plan.md`'nin kendi cümlesi: *«Çıkış kapısı: `test` eval'de plato + transfer korelasyonu sağlam»* → `datasets/v0.1.0/` + CARD.md +
§8 rapor kanıtları.

⛔⛔ **Kapı bugün açılamaz ve sebebi tek bir madde:** Pareto kapısının
**birinci** basamağı (Eksen 2 gerilemesi = 0) üç taramada da beş kolun beşini
eledi; kolları ayıracak tek şey **kriz dilimi** ve o **etik kurul**da.
➡️ *Yani Faz 4'ün kalan işi bir liste değil, bir **kilit**: ölçüm kalemlerinin
hepsi bitse bile kapı açılmıyor.*

## ⛔ Bu listenin söylemedikleri

| | |
|---|---|
| ⛔ **Engel eşlemesi bizim okumamızdır** (Kural 6) | anahtar sözcük araması; bir madde yanlış kovaya düşmüş olabilir. Eşleme yukarıda **ilan ediliyor** |
| ⛔ **Sıra/öncelik yok** | liste ne yapılacağını söylüyor, hangi sırayla değil |
| ⚠️ *«Ölçüm»* sınıfı **eşit büyüklükte değil** | bir satırlık şerh ile yeni bir judge koşusu aynı kovada |
| ⛔ Faz 4 **dışındaki** engeller kapsam dışı | Faz 3'ün kapanamayan kalemi (vahşi doğa dilimi) burada görünmüyor ama Faz 4'ü de bekletiyor |

