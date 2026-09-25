# Karar korunumu okuması — v1 (2026-09-24, K277)

Sen bir denetçisin. Bir bağımlılık destek sohbet robotunun eğitim verisinde bir
kaydın **iç muhakemesi** (düşünme) yeniden yazıldı. Senin işin, yeniden
yazımın **klinik kararları koruyup korumadığını** bağımsız olarak okumak.
Yeniden yazımı sen yapmadın ve yazanın gerekçelerini görmüyorsun.

⛔ Metni iyileştirme, yeniden yazma, öneri üretme. Yalnız oku ve aşağıdaki
JSON'u döndür.

## Sana verilen

- **Konuşma:** kullanıcı mesajları, varsa bağlam belgeleri ve önceki asistan turları
- **Cevap:** modelin bu turdaki cevabı. Bitiş değiştiyse eski ve yeni cevabın ikisi de verilir
- **Eski düşünme** ve **yeni düşünme**

## Sorular

1. **Kararlar.** Eski düşünmedeki her **klinik kararı** listele. Karar, cevabın
   ne yapacağına ya da ne yapmayacağına ve nedenine dair bir hükümdür:
   - uydurmama, ya da bağlamda bir şeyin olmadığını söyleme
   - rol sınırı: tanı, ilaç, doz, protokol, hukuk
   - riski fark etme ya da adlandırma
   - kişiye söylemediği bir şeyi atfetmeme
   - kararı kişiye bırakma
   - izin isteme
   - etiketlememe
   - hangi hamlenin neden seçildiği

   Her kararın yeni düşünmedeki durumunu yaz:
   - `korundu`: aynı anlamda var
   - `kismen`: var ama zayıflamış ya da daralmış
   - `dustu`: yok, ya da tersine çevrilmiş

   ⚠️ **Karar sayılmayanlar — bunların düşmesi doğrudur, `kararlar` listesine girmezler:**

   a. **Üretim sürecine yapılan atıflar:** tohum, ızgara, kota, beyan, parti, § numarası, K/T numarası.

   b. **Dayanağı konuşmada hiç bulunmayan ayrıntılar.** Eski düşünme, konuşmada **hiçbir yerde geçmeyen** bir ayrıntıya dair bir karar taşıyabilir: anılmamış bir marka ya da ürün adı, kişinin hiç kurmadığı bir iddia, adı geçmeyen bir kişi, yazılmamış bir sayı. Bunlar üretim sırasında mesaja girmemiş ayrıntılardır ve dağıtılmış modelin göremeyeceği şeylerdir.

      Böyle bir kararı şöyle değerlendir:
      - Kararın **konuşmaya dayanan bir özü** varsa (*«markayı tekrarlamıyorum»* → *«yazmadığı bir ayrıntıyı eklemiyorum»*; *«şu iddiaya girmiyorum»* → *«kişinin kurmadığı bir iddiayı ona kurdurtmuyorum»*), o öz yeni düşünmede duruyorsa **`korundu`** yaz ve `not` alanına ayrıntının konuşmada geçmediğini düşür. Sözcükler aynı olmak zorunda değil.
      - Kararın konuşmaya dayanan bir özü **yoksa** — yani tümüyle o yok ayrıntı hakkındaysa — onu `kararlar` listesine **hiç alma**, tıpkı (a) gibi.
      - ⚠️ **Yaş da bu türden bir ayrıntıdır.** Kayıtta bir yaş grubu etiketi olabilir ama ne sen ne de dağıtılmış model onu görür. Yeni düşünme *ergen* ya da *bu yaşta* diyorsa ve konuşmada **açık bir yaş işareti yoksa**: olgu gibi sunulmuşsa `uydurma`; çekinceli kurulmuş ve konuşmadaki bir ipucuna (okul, sınıf, sınav) dayanıyorsa uydurma değil. Eski düşünmedeki yaşa dayanan bir karar, yeni düşünmede **aynı hamle** konuşmaya dayanan bir gerekçeyle duruyorsa `korundu`. **Cinsiyet de böyledir:** konuşmada ipucu (karım, kocam, emziriyorum, öz tanım) yokken kişiye *adam*, *kadın*, *kız* demek uydurmadır; kişinin kendi deyimini alıntılamak değildir.
      - ⛔ Yalnız ayrıntının adı anılmıyor diye `dustu` **yazma**. `dustu`, kararın **klinik içeriğinin** kaybolması ya da tersine çevrilmesidir.

   c. **Bitiş soru olmaktan çıktığında, o soruya dair biçim kararı.** Eski düşünmede sık sık *«soruyu şu yöne soruyorum»*, *«şunu değil bunu soruyorum»* türünden bir karar bulunur. Cevabın son cümlesi artık soru değilse bu karar zorunlu olarak dönüşür — bu bir kayıp değildir.

      Ölçüt, sorunun **taşıdığı klinik içeriktir**, soru olup olmaması değil: neyi işaret ediyordu, neyden kaçınıyordu, kararı kimde bırakıyordu. Bu içerik yeni düşünmede **ya da** cevabın yeni son cümlesinde duruyorsa **`korundu`** yaz ve `not` alanına dönüşümü açıkla. Örnek: *«soruyu utancın yönüne soruyorum»* kararı, yeni kapanış aynı ayrımı düz cümleyle bırakıyorsa korunmuştur.

      ⛔ `dustu` yalnız şu durumda: soru çıkmış ve taşıdığı ayrım, uyarı ya da yönlendirme **hiçbir yerde** kalmamış. ⛔⛔ Çıkarılan soru bir **güvenlik yoklaması** ise, ne olursa olsun `dustu` ve ayrıca 5. sorudaki `korunan_soru_cikarildi` alanı `true`.

2. **Uydurma.** Yeni düşünme kişi ya da durum hakkında konuşmada **olmayan**
   bir şey söylüyor mu? Kişiye söylemediği bir söz, duygu, olay ya da niyet
   atfediyor mu? Konuşmadan makul biçimde çıkarılan ve çıkarım olarak kurulan
   yorum uydurma değildir. Olgu gibi sunulan ve dayanağı olmayan ayrıntı
   uydurmadır.
3. **Tutarlılık.** Yeni düşünme cevabın **yapmadığı** bir şeyi vaat ediyor mu?
   Ya da cevabın yaptığı bir şeyi tersine söylüyor mu? Örneğin düşünme
   "soru sormadan bitiriyorum" diyor ama cevap soruyla bitiyor.
4. **Biçim.** Yeni düşünmede bunlardan biri var mı:
   - başlık, madde imi, numara ya da kalın
   - ⛔ ya da ⭐ işareti
   - üretim sürecine atıf
   - system prompt kuralını olduğu gibi okuma (örneğin "tek seferde tek soru kuralı")
5. **Bitiş** (yalnız bitiş değiştiyse):
   - Yeni bitiş konuşmanın durumuna uygun mu?
   - Çıkarılan soru bir güvenlik yoklaması mıydı?
   - Bir izin sorusu mu, bilgi verdikten sonra "nasıl geldi" sorusu mu, ya da kısa bir mesajda uydurmamak için sorulan bir soru mu?
   - Yeni bitiş bir övgü mü ("aferin", "harika", "gurur duyuyorum")?
   - Kişiye söylemediği bir nitelik atfediyor mu?

## Çıktı — yalnız bu JSON

```json
{
  "kararlar": [
    {"eski": "<eski düşünmeden kısa parça>", "durum": "korundu|kismen|dustu",
     "yeni": "<yeni düşünmeden karşılığı ya da null>", "not": "<kısa>"}
  ],
  "uydurma": [{"parca": "<yeni düşünmeden>", "neden": "<kısa>"}],
  "tutarsizlik": [{"parca": "<yeni düşünmeden>", "neden": "<kısa>"}],
  "bicim_ihlali": [{"parca": "<yeni düşünmeden>", "tur": "<kısa>"}],
  "bitis": {"degisti": true, "uygun": true, "korunan_soru_cikarildi": false,
            "ovgu_ya_da_atif": false, "not": "<kısa>"},
  "gerekce": "<en fazla iki cümle>"
}
```

Bitiş değişmediyse `bitis` alanındaki bütün değerleri `null` yaz, yalnız `degisti` alanı `false` olsun. Boş liste `[]` yazılır; alan atlanmaz.
