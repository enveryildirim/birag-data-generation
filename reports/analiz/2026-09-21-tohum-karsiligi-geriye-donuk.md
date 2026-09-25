# Tohum karşılığı — v6 partilerinde geriye dönük tarama

**Betik:** `scripts/analiz/2026-09-21-tohum-karsiligi-geriye-donuk.py` · **Tarih:** 2026-09-21  
**Ölçüt:** T217'nin kapısı, aynen — `tr_sadelestir` + 5 harflik gövde öneki, marj ≥ 3 ya da kendi tohumuyla sıfır örtüşme

⛔⛔ **Gerekçe bir hatadır.** `v6-parti6 #15` ve `#19` başka satırların tohumundan yazılmıştı ve `source_ids` plandan geldiği için doğru görünüyordu. Kapı parti6'da kuruldu; T217'nin şerhi *«geriye dönük tarama yapılmadı»* diyordu. Bu rapor onu kapatıyor.

## 0. ⭐⭐⭐ Sonuç

⭐ **Karışma YOK.** İşaretlenen 33 satırın 33'ü okundu; hiçbiri başka bir satırın tohumundan yazılmamış. 32'si `v6-parti1`'de ve sebebi tek: **parti1 başka bir üretim rejiminde yazılmış** — tohum ızgara hücresini verdi, sahneyi ben yazdım. Ölçüldü: kendi tohumuyla sözcük örtüşmesi parti1'de ortalama **%6** (21 kayıtta sıfır), parti2'de %49, parti3-6'da %66-71. ➡️⭐⭐⭐ *Bir alanın ne anlama geldiği ilan edilmediyse, anlamı sessizce değişebilir: `source_ids` parti1'de «ızgarayı veren tohum», parti3-6'da «metni veren tohum» demek ve ikisi arasında yazılı bir sınır yok.*

⛔ Kalan 1 işaret (`v6-parti3#3`) tohuma sadık; kayıt `kisa` olduğu için örtüşme düşük çıktı (yanlış pozitif).

## 1. Parti parti

| parti | kayıt | ⛔ işaretli | kendi tohumuyla örtüşme (en az / medyan / en çok) | girdi SHA256-16 |
|---|---:|---:|---|---|
| `v6-parti1` | 59 | **32** | 0 / 1 / 5 | `bbdc8057636d46d5` |
| `v6-parti2` | 59 | **0** | 3 / 9 / 17 | `4f65ece0ba019105` |
| `v6-parti3` | 60 | **1** | 0 / 14 / 28 | `a82b8d16705373f4` |
| `v6-parti4` | 59 | **0** | 4 / 14 / 23 | `2bc2e7ec1336bdcd` |
| `v6-parti5` | 60 | **0** | 3 / 13 / 30 | `21a6a72faf0435fb` |
| `v6-parti6` | 58 | **0** | 2 / 14 / 30 | `23186319a6b008b1` |

⭐ **Toplam 355 kayıt tarandı, 33 satır işaretlendi.**

## 2. ⛔ İşaretli satırlar — hüküm elle verildi

| parti | # | kendi | en iyi | marj | rakip satır | hüküm |
|---|---:|---:|---:|---:|---|---|
| `v6-parti1` | 2 | 0 | 3 | 3 | [28] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 4 | 0 | 2 | 2 | [53] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 10 | 1 | 4 | 3 | [24, 56] | ⭐ karışma YOK — aynı durumun başka sahnesi |
| `v6-parti1` | 11 | 1 | 4 | 3 | [41] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 12 | 0 | 3 | 3 | [43, 60] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 16 | 0 | 2 | 2 | [14, 20] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 17 | 1 | 4 | 3 | [5] | ⭐ karışma YOK — aynı durumun başka sahnesi |
| `v6-parti1` | 18 | 0 | 4 | 4 | [8, 27] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 23 | 0 | 2 | 2 | [18, 41] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 24 | 1 | 4 | 3 | [10] | ⭐ karışma YOK — aynı durumun başka sahnesi |
| `v6-parti1` | 25 | 0 | 3 | 3 | [33] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 26 | 1 | 5 | 4 | [5] | ⭐ karışma YOK — aynı durumun başka sahnesi |
| `v6-parti1` | 27 | 0 | 4 | 4 | [12] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 28 | 0 | 5 | 5 | [33] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 30 | 2 | 6 | 4 | [47] | ⭐ karışma YOK — aynı durumun başka sahnesi |
| `v6-parti1` | 31 | 0 | 3 | 3 | [44] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 32 | 0 | 3 | 3 | [39] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 33 | 2 | 5 | 3 | [1] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 34 | 0 | 3 | 3 | [5, 10, 16] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 36 | 1 | 4 | 3 | [47] | ⭐ karışma YOK — aynı durumun başka sahnesi |
| `v6-parti1` | 37 | 0 | 1 | 1 | [2, 5, 10] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 38 | 0 | 3 | 3 | [15, 31, 41] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 42 | 0 | 3 | 3 | [2, 20] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 43 | 0 | 1 | 1 | [5, 11, 44] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 46 | 0 | 2 | 2 | [16] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 48 | 1 | 6 | 5 | [40] | ⭐ karışma YOK — aynı durumun başka sahnesi |
| `v6-parti1` | 51 | 0 | 1 | 1 | [14, 17, 22] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 52 | 0 | 3 | 3 | [42, 58] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 53 | 1 | 4 | 3 | [7, 24] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 54 | 1 | 4 | 3 | [21] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 55 | 0 | 1 | 1 | [3, 6, 7] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti1` | 56 | 0 | 1 | 1 | [3, 6, 7] | ⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi) |
| `v6-parti3` | 3 | 0 | 0 | 0 | [1, 2, 4] | ⭐ karışma YOK — tohuma sadık, kayıt `kisa` olduğu için örtüşme düşük (yanlış pozitif) |

⭐⭐ **İşaret ≠ karışma, ve farkı MUTLAK skor söylüyor.** parti6'daki iki gerçek karışmada rakip tohumun skoru yüksekti (5 ve 8) ve kayıt görünür biçimde O tohumun hikâyesini anlatıyordu. Buradaki 33 işarette rakip skorların tamamı 0-6 aralığında, yani gürültü düzeyinde: hiçbir kayıt başka bir satırın hikâyesini anlatmıyor. ➡️ *Kıyaslı bir ölçütte marj karışmayı işaret eder, ama karışmayı KANITLAYAN şey rakibin mutlak skorudur.*

### İşaretli satırların metinleri

**`v6-parti1#2`**  
· *tohum:* Ya ben aslında günde 1-2 saat falan bakıyorum o sitelere, akşamları sadece kafa dağıtmak için. Eşim büyütüyor …  
· *kayıt:* dun esim annesine evdeki adam yine telefonda dedi. ismimi soylemedi…

**`v6-parti1#4`**  
· *tohum:* Kardeşim de bu gece kapıyı yüzüme kapadı. Dönecek yerim yok. Siz de yardım edemezsiniz zaten, ne yazıyorum bil…  
· *kayıt:* yine numara verdin…

**`v6-parti1#10`**  
· *tohum:* Efexor üç yıldır kullanıyorum. Son bir yıldır şarap şişesini mutfak dolabının arkasına saklıyorum, eşim işteyk…  
· *kayıt:* 

Yarın psikiyatra gideceğim. Dozumu altı ayda iki kez artırdılar, hâlâ iyileşme yok diyor. Ona şarabı söyleye…

**`v6-parti1#11`**  
· *tohum:* Şu an AMATEM'de yatıyorum, ikinci günüm. Az önce eşim avukatı üzerinden boşanma dilekçesinin gittiğini yazdı. …  
· *kayıt:* dun gece kolonya ictim baska sey yoktu evde saat gecti dukkanlar kapaliydi. midem su an yaniyor resmen sabahta…

**`v6-parti1#12`**  
· *tohum:* Eşim dün gece tek bir mesaj attı: 'bütün borçların listesini istiyorum, hiçbir şey saklamadan.' Oturdum üç ban…  
· *kayıt:* 

Gündüz kendime bu gece açmayacağım diyorum ve gerçekten de istemiyorum. Gece üçte bebeği emzirip yatağa dönd…

**`v6-parti1#16`**  
· *tohum:* Sabah karyoladan kalkarken bir an dünyam karardı, kenara tutundum da düşmedim. Dün akşam yine bir kadeh içmişt…  
· *kayıt:* Bizim masa eski, on iki yıldır aynı günler toplanırız. Bir arkadaşımız rahatsızlandı, artık gelemiyor. Eşim de…

**`v6-parti1#17`**  
· *tohum:* Doktor diz protezi diyor ama bir türlü cesaret edemedim. Geceleri dizim öyle bir sızlıyor ki, ağrı kesicimi al…  
· *kayıt:* Eşim öleli üç yıl oldu.…

**`v6-parti1#18`**  
· *tohum:* Bu sefer de tansiyon ilacı eklendi ama eczacı 'şu eski hapınızla beraber alırken dikkat edin, baş döndürebilir…  
· *kayıt:* esim hicbir seyden haberdar degil uc yildir. izin baslayinca evde nasil aciklayacagim bunu hic dusunmemistim a…

**`v6-parti1#23`**  
· *tohum:* selam ya bu cumartesi Burak'ın doğum günü var, evde toplanacağız. WhatsApp'taki grupta vodka-cola ayarlamışlar…  
· *kayıt:* Bir bardak içtim, başım dönüyor. Ne yapayım?…

**`v6-parti1#24`**  
· *tohum:* Geçen sefer 'doktoruna söylemeyi düşünebilirsin' demiştin. Denedim. İki gün önce muayenedeydim, ağzımı bile aç…  
· *kayıt:* Dozu iki ay önce artırdılar.…

**`v6-parti1#25`**  
· *tohum:* Saat akşam yedi oldu, eskiden bu saat şarabı açtığım saat. Mutfakta hâlâ iki şişe duruyor. Eşim 'ben akşamları…  
· *kayıt:* oglumla her pazar konusalim diye anlasmayi dusunuyorum ama icimde beni denetlemek icin ariyor korkusu var…

**`v6-parti1#26`**  
· *tohum:* Geçen gece tuvalete kalkarken duvara çarptım, kolum mosmor oldu. Akşam yemekte bir kadeh şarap içmiştim, sonra…  
· *kayıt:* Belim yıllardır tutuyor.…

**`v6-parti1#27`**  
· *tohum:* kayıt parasını bahse yatırdım, kupon tutarsa hem ödeyeceğim hem rahatlayacağız diye düşündüm. kaybettim. karım…  
· *kayıt:* Neredeyse bir yıl olmuştu.…

**`v6-parti1#28`**  
· *tohum:* Bu günlerde sürekli geriye dönüp düşünüyorum. Belki de yıllarca şarap içmemin sebebi evliliğimdeki mutsuzluk, …  
· *kayıt:* Alt komşumla akşamları beraber yiyoruz.…

**`v6-parti1#30`**  
· *tohum:* üç haftadır oynuyorum yine. iş yok, kafam dağınık, eve oturunca duramıyorum. tazminatın iyi bir kısmı gitti, e…  
· *kayıt:* 

Bir yıllık temizlikten sonra bu hafta iki defa girdim. Nafaka tartışması kafamı bitiriyor, avukat parası laz…

**`v6-parti1#31`**  
· *tohum:* Annem sonunda AMATEM'e yattı, bugün ikinci günü. Mide tedavisi devam ediyor, titremesi azalmış. Ben rahatladım…  
· *kayıt:* 

Hekime sersemlikten bahsettim, dönem öyle olur dedi. Bizimki de ikisini birlikte alma, tekrar sor diyor. Sen…

**`v6-parti1#32`**  
· *tohum:* Şu an etüt arasındayım, on dakikam var. Sabahtan beri matematik çözüyorum, kafam o kadar yorgun ki nefes alamı…  
· *kayıt:* babam bugun garip bir sey dedi. sacmalik varsa simdi soyle dedi. ben soylesem ne olur ki gercekten…

**`v6-parti1#33`**  
· *tohum:* Az önce oğlumla görüntülü konuştuk, Hollanda'dan arıyor. Senin sesin tuhaf çıkıyor anne, içtin mi yine dedi. A…  
· *kayıt:* 

Kızım az önce aradı, bu bayram da gelemeyecekmiş, torun çok küçükmüş diye. Telefonu kapattım, sofrayı kurark…

**`v6-parti1#34`**  
· *tohum:* Geçen hafta hastanede yoksunluktan kıvrandım, çıkarken AMATEM dediler ama benim için artık çok geç bence. Şu a…  
· *kayıt:* Eşim evde alkol bulunmasın diyor.…

**`v6-parti1#36`**  
· *tohum:* üç gece üst üste oynadım. iş yok, eşim de hasta. bir yıl temizdim. terapisti aramak şu an bana çözüm değil, sı…  
· *kayıt:* 

cumartesi mac vardi sadece izleyecegim diye girdim sonra bahis koydum. bir yil olmustu temiz. mentorum aradi…

**`v6-parti1#37`**  
· *tohum:* abi şu family link mi ne açmışlar telefondan, artık bi şey indirsem görüyor. ama grup deli, kombine atıyolar. …  
· *kayıt:* Deneme kötü geçti. Bu akşam maç var.…

**`v6-parti1#38`**  
· *tohum:* Bugün üçüncü seanstaydım. İlk iki seans 'mecburiyet' gibi geçmişti, bugün ilk kez kendi adıma bir şey fark ett…  
· *kayıt:* İkinci test de bitti, temiz çıkacak. Ama dönerken çok yorgun hissettim. İlk başlarda bir öfke vardı, şimdi onu…

**`v6-parti1#42`**  
· *tohum:* Geçen ay bir hafta sosyal medyasız yaşadım. Çok iyi hissettim, çok şey yaptım. Ama sonra bir ara açtım ve yine…  
· *kayıt:* 

Sınava dört ay kaldı. Her gün çalışacağım diyorum ama kapatamıyorum, günde beş altı saat izliyorum. Kendime …

**`v6-parti1#43`**  
· *tohum:* Kayınvalidem üç gündür bizde. Hep iyi anne mi olduğumu test ediyormuş gibi hissediyorum. Balkona her on dakika…  
· *kayıt:* Hekim bant yazdı, sevk de verdi.…

**`v6-parti1#46`**  
· *tohum:* Aile hekimi yine ahkâm kesti, e-Nabız'a bakıp 'durum ciddi' diyor. Yahu bu çocuk benim torunum yaşında, daha d…  
· *kayıt:* Eşim bu aralar çok duygusal.…

**`v6-parti1#48`**  
· *tohum:* düşündüm dediklerini. iki gündür şarap içmedim. ama bu sefer cipram'ı sabah iki tane almaya başladım, tek tane…  
· *kayıt:* Bak açık söyleyeyim, bırakamayacağım. İlacın üstüne ne kadar şarap güvenli, onu söyle. Bir kadeh mi, iki mi? D…

**`v6-parti1#51`**  
· *tohum:* Gelinim bu sabah dedi ki, 'anne biz sizi kaybedeceğiz diye korkuyoruz.' O cümle hâlâ kulağımda. Bir yanım onla…  
· *kayıt:* saat uc oldu yine uyuyamadim…

**`v6-parti1#52`**  
· *tohum:* Telefonumun ekran süresine baktım, günde ortalama 7 saat çıkıyor. Bunun 4.5 saati TikTok. Bunu görünce içim sı…  
· *kayıt:* Bebeğimle baş başa kaldığımda sosyal medya kapalıysa ne yapacağımı bilmiyorum. Zaten onun dışında bir şey kalm…

**`v6-parti1#53`**  
· *tohum:* Eşim 7 aylık hamile, ben servis şoförüyüm, sabah 5'te kalkıp gece 10'da geliyorum. 80 bin lira ceza, hayatımı …  
· *kayıt:* Şimdi sırada bekliyorum. Geçen seansta hocaya idare ediyorum dedim, bir şey demedi sadece baktı. Bu seans yine…

**`v6-parti1#54`**  
· *tohum:* Kocam eve gelince akşamları film izleriz. Ama ondan önce de TikTok, sonra da TikTok. Gündüzüm kayıyor.…  
· *kayıt:* arkadasim her gun on saat calisiyor ben iki saat calisip yoruluyorum sonra youtube a geciyorum. sanki bende bi…

**`v6-parti1#55`**  
· *tohum:* abi bizim ekipten bi çocuk var, üst üste kaybediyo bu aralar ve cidden morali çok bozuk. ben de aynı kuponları…  
· *kayıt:* Hafta sonu iki test çözecektim.…

**`v6-parti1#56`**  
· *tohum:* YEDAM'dan çıkalı beş ay oldu, hâlâ iş yok. Anne sabah 'ben yoruldum artık' dedi. Gece eski siteden bildirim ge…  
· *kayıt:* Sponsoruma üç haftadır yazmıyorum.…

**`v6-parti3#3`**  
· *tohum:* abi şimdi hafta sonu plan yapmıştım iki test çözücem diye, ama maç sonuçlarına kaptırdım kendimi telefondan, b…  
· *kayıt:* Maç skorlarına daldım, test yapamadım. Ne yapayım?…

## 3. ⛔⛔ Çifte tahsis — bu tarama sırasında çıktı

Sorulan soru *«kayıt yanlış tohumdan mı yazıldı»* idi. Cevap hayır; ama aynı taramada başka bir şey göründü: **bir tohum iki plan satırına düşmüş olabiliyor.**

| | |
|---|---:|
| birden fazla plan satırına düşen tohum | **26** |
| ⛔ **iki kez ÜRETİLEN tohum** | **24** |
| toplam üretilmiş kayıt | 355 |
| benzersiz tohum | 331 |

⛔ Çifte üretimin tamamı **parti1 + parti2** çiftinde. ⭐ İki kayıt birbirinin kopyası DEĞİL: sözcük örtüşmesi (Jaccard) ortalama %2, en yüksek %7. ⇒ Eğitim verisinde tekrar yok; sorun **sayımda**: korpus 355 kayıt taşıyor ama 331 tohuma dayanıyor ve kapsama envanteri *«kullanılmış tohum»* üzerinden ölçüyor.

| tohum | kayıtlar | örtüşme |
|---|---|---:|
| — | `v6-parti1#44` ↔ `v6-parti2#30` | %7 |
| — | `v6-parti1#6` ↔ `v6-parti2#34` | %5 |
| — | `v6-parti1#50` ↔ `v6-parti2#8` | %5 |
| — | `v6-parti1#30` ↔ `v6-parti2#18` | %5 |
| — | `v6-parti1#60` ↔ `v6-parti2#40` | %4 |
| — | `v6-parti1#57` ↔ `v6-parti2#31` | %4 |

⛔⛔ **`gd-021`'in tohumu bunlardan biri.** `929466628ddb3207` hem `v6-parti1#4` hem `v6-parti2#54`'e düşmüş; parti1'de ÜRETİLMİŞ, parti2'de okunup elenmiştir. ⭐ Kriz metni korpusa girmedi çünkü parti1 rejiminde tohum metni kayda geçmiyor — yani bunu engelleyen şey bir kapı değil, o partinin üretim biçimiydi. ➡️ *Bir kaza, başka bir kazanın yan etkisiyle zararsız kalabilir; bu, ikisinin de kaza olmadığı anlamına gelmez.*

## ⛔ Bu taramanın söylemedikleri

| | |
|---|---|
| ⛔⛔ **Tarama PARTİ İÇİ** | bir kayıt başka bir PARTİNİN tohumundan yazıldıysa bu kural onu göremez; yalnız sıfır örtüşen satırlar o durumda da görünür |
| ⛔⛔ **İşaret hüküm değildir** | ölçüt sözcük örtüşmesi, anlam değil; ağır genelleştirme yapan (marka/kurum adı çıkaran) meşru bir kayıt da düşük skor alabilir. Hüküm okunarak verilir (K30) |
| ⛔ **Marj 3 bir SEÇİM** | parti6'daki iki gerçek hatayla kalibre edildi (marj 5 ve 6; meşru en yüksek 1), türetilmedi. Daha yumuşak bir karışma — aynı tür, benzer sözcükler — eşiğin altında kalabilir |
| ⛔ **Yalnız KULLANICI turlarına bakılıyor** | asistan cevabının tohuma uygunluğu ölçülmüyor |
| ⚠️ **v5 ve öncesi taranmadı** | `v0.0.14`'ün 571 kaydı bu taramanın dışında; onların planları farklı biçimde ve ayrı bir geçiş gerekir |
