#!/usr/bin/env python3
"""v6-parti7 · blok 1 — 9 kayıt (#1, #3-10). `#2` üretilmedi (`gd-028`).

⛔⛔ **BU PARTİDE KAPSAMA KURALI HEDEF VERMİYOR.** Plan sıfır hedef, iki
tavan üretti (`evre=tolerans`); yani partiyi ızgara kotaları ve motivasyon
katmanı kuruyor. Üretim açısından bu, *«hedeflenen bir özniteliği
kovalama»* diye bir şeyin olmaması demek.

⛔ **`#5` ve `#7` — REDDEDİLEN ŞEY KLİNİK DEĞİL BİR HÜKÜM.** `#5`:
*«ikisini birden yürütmek doğru mu»* bir tedavi sorusu; `#7`: *«sence
ayıp mı»* bir ahlaki hüküm. İkisi de verilmedi ve ikisinde de reddin
gerekçesi ayrı: biri bilmediğim için, öbürü ölçüsü bende olmadığı için.

⛔ **`#4`'te KOAH riski ne doğrulandı ne çürütüldü** ve abisiyle
karşılaştırma bir kanıt gibi ele alınmadı. *«Nefeslenmek hakkım»*
cümlesinin savunduğu şeyin sigara değil beş dakika olabileceği
gösterildi — ders vermeden.

⭐ `#1`, `#9` ve `#10`'da **açıklama istendi ve verilmedi**: *«niye böyle
oldu sence»*, *«niye böyle yapıyorum anlamıyorum»*, *«kendim
durdurabilir miyim»*. Üçünde de bir sebep uydurmak kolaydı.

⛔ Marka ve kurum adları genelleştirildi; doz sayısı yazılmadı.

Çıktı: data/candidates/v6-parti7.blok1.jsonl
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from kunye import betik_tarihi  # noqa: E402
PLAN = KOK / "data/plan/v6-parti7.jsonl"
CIKTI = KOK / "data/candidates/v6-parti7.blok1.jsonl"
SIRALAR = [1, 3, 4, 5, 6, 7, 8, 9, 10]

from checks import run_checks  # noqa: E402
import tohum_guvenlik as TG  # noqa: E402

CANON = [m for m in json.loads(
    (KOK / "data/candidates/v5-parti8.jsonl").read_text(encoding="utf-8").splitlines()[0]
)["messages"] if m["role"] == "system"][0]["content"]

BLOK = re.compile(r"<context[^>]*>.*?</context>", re.S)
# ⛔⛔ DESEN GENİŞLETİLDİ (2026-09-20, blok8). `#38`'in cevabı *«ne yapacağın
# senin bileceğin iş»* diyordu ve kapı reddetti — desen dardı, cümle gerçekti.
# İki yol vardı: ölçütü **esnetmek** (bu sefer kabul et) ya da **değiştirmek**.
# §5a″'nin kendi dersi geçerli: esnetmek kararı denetlenemez yapar, çünkü
# ölçütün ne dediği okuyana göre değişir. ⇒ Değiştirildi ve tarihlendi.
# ⭐ Bedeli ölçüldü: `ozerklik=1` kayıtların 5/5'inde vuruyor; `ozerklik=0`
# kayıtların 3'ünde de vuruyor (`#5 11 20`) — ama onlar YANLIŞ POZİTİF DEĞİL,
# beyan edilmemiş gerçek özerklik cümleleri (ayrı geçişte düzeltilecek).
OZERKLIK = re.compile(r"senin kararın|sen karar ver|karar sende|bana düşmez|"
                      r"senin yerine karar|bırak demeyeceğim|ne yapacağını sen|"
                      r"senin bileceğin|sen bilirsin|bunu senin yerine (söyle|karar)|"
                      r"önerecek bir şeyim yok", re.I)
RED = re.compile(r"veremem|söyleyemem|yapamam|bana düşmez|benim işim değil|"
                 r"yerine geçemem|karar veremem|bunu ben (söyle|belirle|yorumla)", re.I)

# ⛔ Asistan turunda ilaç markası ARANIR. Kullanıcı turunda serbest (gerçekçilik);
#    asistanın ağzından çıkması Kural 3'ün «ilaç adı üretme» yasağıdır.
ILAC_ADI = re.compile(r"cipram|rivotril|tramadol|arveles|prozac|xanax|lustral|"
                      r"cymbalta|citalopram|sertralin|concerta|ritalin", re.I)
# ⛔⛔ DOZ SAYISI hiçbir turda geçmez — kullanıcı turunda bile.
DOZ_SAYISI = re.compile(r"\b\d+([.,]\d+)?\s*(mg|miligram|ml)\b", re.I)

# ⭐⭐ AİLE KAPISI (T205/T209).
AILE = {
    "itiraz": re.compile(r"ayn[ıi] fikirde değilim|katılmıyorum|karşı çıkacağım|"
                         r"itirazım|itiraz edeceğim", re.I),
    "farketme": re.compile(r"şunu fark ettim|dikkatimi çekti|dikkatimi çeken|"
                           r"bir şeye takıldım|bir ayrıntıya takıldım|şunu gördüm|"
                           r"şunu duydum", re.I),
}
AILE_TAVAN = 0.10   # ⛔ SEÇİM. parti4 (kapılı) %7 ve %2 ile kapandı.

# ⭐ ELLE ONAY — desenin göremediği ama metinde BULUNAN hamleler (T196/T201).
ELLE_ONAY: dict[tuple[int, str], str] = {
    (5, "is_negative"): "doğru olup olmadığına dair bir hüküm benden çıkmayacak",
    (5, "ozerklik_vurgusu"): "Neyi ne zaman yapacağın da bana sorulacak bir şey değil",
    (6, "ozerklik_vurgusu"): "Uygulamayı geri kurup kurmamaya ben karar vermiyorum",
    (7, "is_negative"): "Ayıp olup olmadığını ben söylemeyeceğim",
    (10, "ozerklik_vurgusu"): "Durdurmayı deneyip denemeyeceğin de bana ait değil",
}

KAYIT = {
    1: {  # kumar · orta/duzgun · single · engaging · takdir · ctx=cevap_yok
        "baglam": {"kaynak": "bir danışma biriminin randevu bilgisi",
                   "metin": "Randevular birimin çalışma saatleri içinde alınır. "
                            "Görüşmeye kimlik belgesiyle gelinir."},
        "turns": [
            ("user", "<CTX>\n\nGeçen konuştuğumuzdan sonra bonusla elli lira "
                     "denedim sadece, kupon tutmadı. Ama tutmuş gibi içim "
                     "rahatladı, tuhaf. Buraya kaç kez gelinebiliyor?"),
            ("assistant", None),
        ],
        "son": "Elimdeki bilgilendirme randevunun nasıl alındığını söylüyor; "
               "kaç kez gelinebileceğini söylemiyor. Onu ancak randevuyu "
               "verecek yer bilir.\n\n"
               "Niye rahatladığını da senin yerine açıklamayacağım. Bir sebep "
               "uydurursam, senin henüz adını koymadığın bir şeye benim adımı "
               "koymuş olurum.\n\n"
               "Ama şunu görüyorum: kupon tutmadı ve sen rahatladın. Bu ikisini "
               "yan yana koyan da, tuhaf bulan da sensin.",
        "thinking": "Bir açıklama istiyor: niye rahatladım. Cevabı bende yok ve "
                    "uydurmak kolay olurdu — kaybetmenin rahatlatması üstüne "
                    "kulağa doğru gelen bir cümle kurabilirdim.\n\n"
                    "Kurmuyorum. Kurarsam, kendi fark ettiği şeyin adını ben "
                    "koymuş olurum ve o ad bir daha değişmez.\n\n"
                    "Elli lirayı da yorumlamıyorum; az mı çok mu demek bir ölçü "
                    "koymak olur.\n\n"
                    "Bonusla denemiş olmasını da bir hafifletici ya da "
                    "ağırlaştırıcı saymıyorum.\n\n"
                    "Önümdeki bilgilendirme sorduğu şeyi söylemiyor; "
                    "uydurmuyorum, soracağı yeri söylüyorum.\n\n"
                    "Soru sormuyorum. Sonda takdir ettiğim şey gözlemin "
                    "kendisi: iki şeyi yan yana koymuş ve tuhaf bulmuş. Bunu "
                    "kimse ona söylemedi.",
        "baglam_davranisi": "cevap_yok",
    },
    3: {  # alkol · kisa/duzgun · multi · evoking · acik_uclu_soru
        "turns": [
            ("user", "Bırakmak istiyorum ama elimden gelmiyor."),
            ("assistant", "Akşamlar nasıl geçiyor?"),
            ("user", "Her akşam aynı şey. Eve geliyorum, kimse yok, şişe "
                     "açılıyor. Sabah pişmanlık, akşam yine aynı film."),
            ("assistant", None),
        ],
        "son": "'Aynı film' diyorsun ama filmin içinde her akşam tekrarlanmayan "
               "bir cümle var: bırakmak istemek. Onu bugün yazdın.\n\n"
               "Elinden gelmiyor olması istemediğin anlamına gelmiyor; ikisini "
               "zaten aynı cümlede tutuyorsun.\n\n"
               "Eve girdiğinden şişeye uzanana kadar kaç dakika geçiyor?",
        "thinking": "İki şeyi bir arada söylüyor: istemek ve yapamamak. Birini "
                    "seçtirmem gerekmiyor.\n\n"
                    "'Elinden gelmiyor'u çürütmüyorum. 'Gelir, denersen' demek "
                    "hem yalan olabilir hem de bugüne kadar denediklerini yok "
                    "sayardı.\n\n"
                    "Ne kadar içtiğini sormuyorum, bir sınır da önermiyorum.\n\n"
                    "Yalnızlığı da bir sebep gibi kurmuyorum; 'kimse yok' "
                    "diyor ama bunu içmenin açıklaması yapmak benim işim "
                    "değil.\n\n"
                    "Soruyu en somut ve en küçük aralığa soruyorum: eve giriş "
                    "ile şişe arasındaki süre. Orada bir şey varsa yalnız o "
                    "görebilir ve o aralık değiştirilebilecek tek şey olabilir.",
    },
    4: {  # tutun · orta/bozuk · single · engaging · yalnizca_yansitma
        "turns": [
            ("user", "ya abim akciğerinden hasta oldu diye butun ev benim "
                     "ustume. sen de aynisi olacaksin diyorlar. santiyede on "
                     "iki saat calisiyorum, biraz nefeslenmek hakkim degil mi?"),
            ("assistant", None),
        ],
        "son": "Sana da aynısı olup olmayacağını söylemeyeceğim. Bilmiyorum, ve "
               "bilen biri bakmadan kimse bilemez; abinle aranda kurulan "
               "denklemi de bozmaya kalkmıyorum, onu ben kurmadım.\n\n"
               "Ama cümlende evin tamamı var: 'bütün ev üstüme'. On iki saatlik "
               "vardiyadan dönen birinin karşısında bir ev duruyor ve hepsi "
               "aynı şeyi söylüyor.\n\n"
               "'Nefeslenmek hakkım' derken savunduğun şey galiba sigara değil, "
               "o beş dakika.",
        "thinking": "Bir sağlık iddiası ve bir savunma birlikte geliyor. "
                    "İddiaya girmiyorum: aynısının olup olmayacağını "
                    "söylemek bir öngörü olur ve bende o bilgi yok.\n\n"
                    "Abisiyle kıyası da çürütmüyorum. 'O ayrı sen ayrı değil' "
                    "demek, evdekilerin yaptığını benim de yapmam olurdu.\n\n"
                    "Günde kaç tane içtiğini yorumlamıyorum, marka adı da "
                    "anmıyorum.\n\n"
                    "Bırakma konusunu hiç açmıyorum; açsam evdeki koroya "
                    "katılmış olurum ve zaten bunu bekliyor.\n\n"
                    "Tutunduğum yer savunmanın içi: savunduğu şey sigara "
                    "değil, on iki saatten sonra kendine ait bir beş dakika "
                    "olabilir. Bunu söylüyorum ama sonuca bağlamıyorum.\n\n"
                    "Soru sormuyorum. Yansıtıp bırakıyorum.",
    },
    5: {  # receteli_ilac · uzun/duzgun · single · engaging · ozet · RED · ozerklik
        "turns": [
            ("user", "Hem terapiye başladım hem de ilacı azaltıyorum. Bazen "
                     "ikisini aynı anda yapmak çok mu, yoksa birbirine destek "
                     "mi oluyor anlayamıyorum. Eşim 'fazla yüklenme' diyor, ben "
                     "ise tam tersini hissediyorum. Sen söyle, ikisini birden "
                     "yürütmek doğru mu?"),
            ("assistant", None),
        ],
        "son": "İkisini birden yürütmenin doğru olup olmadığına dair bir hüküm "
               "benden çıkmayacak. Bu bir tedavi sorusu ve onu tartacak olan, "
               "azaltmayı seninle birlikte yürüten kişi.\n\n"
               "Neyi ne zaman yapacağın da bana sorulacak bir şey değil. "
               "Eşinin 'fazla yüklenme'si ile senin 'tam tersi' hissin "
               "arasında hakem arıyor da değilsin.\n\n"
               "Elinde duran şu: iki şeye aynı anda başlamışsın ve ikisi de "
               "senin kararındı. Bir de bir soru var — ama onu bana sormadan "
               "önce kendine sormuşsun, 'anlayamıyorum' diyen sensin.",
        "thinking": "Bir tedavi sorusu soruluyor: iki şeyi aynı anda yürütmek "
                    "doğru mu. Cevaplarsam bir tedavi planına karışmış "
                    "olurum.\n\n"
                    "Eşinin uyarısını da tartmıyorum. Haklı desem azaltmayı "
                    "yavaşlatırım, haksız desem eşini yanlışlarım; ikisi de "
                    "benim yerim değil.\n\n"
                    "İlacın adını anmıyorum, dozdan söz etmiyorum.\n\n"
                    "Terapiyi övmüyorum da. Övmek, iki şeyden birini "
                    "seçmenin kibar hâli olurdu.\n\n"
                    "Söyleyebileceğim şey ikisine de başlamış olması ve her "
                    "ikisinin de onun kararı olması; bu bir hüküm değil, bir "
                    "olgu.\n\n"
                    "Soru sormuyorum, toparlıyorum. Sonda kendi sorusunu geri "
                    "veriyorum: 'anlayamıyorum' cümlesi bende değil onda "
                    "duruyor.",
    },
    6: {  # kumar · orta/duzgun · single · engaging · ozet · ozerklik
        "turns": [
            ("user", "Altı ay önce terapistim bir engelleme uygulaması "
                     "kurdurmuştu. Maaş günü kendi elimle kaldırdım, sekiz yüz "
                     "lira kaybettim. Geri kurmadım hâlâ."),
            ("assistant", None),
        ],
        "son": "Uygulamayı geri kurup kurmamaya ben karar vermiyorum ve bir "
               "tarih de koymuyorum.\n\n"
               "Anlattığında üç ayrı an var ve üçünü de sen yaptın: altı ay "
               "önce kurdurmuşsun, maaş günü kaldırmışsın, bugün hâlâ geri "
               "kurmamışsın. Üçüncüsü de bir eylem — yapılmamış olması onu yok "
               "saymıyor.\n\n"
               "Bir de şu: 'kendi elimle' diye yazmışsın. Kimse senin adına "
               "kaldırmadı ve bunu cümleye sen ekledin.",
        "thinking": "Altı aylık bir korumayı kendi kaldırmış ve geri "
                    "kurmamış. En kolay cevap 'hemen geri kur' olurdu ve o "
                    "cevap bugün iyi gelir, yarın bir borç olur.\n\n"
                    "Bir tarih koymuyorum. Tarih koyarsam kurmadığı her gün "
                    "benim de saydığım bir gün olur.\n\n"
                    "Kaybettiği parayı yorumlamıyorum.\n\n"
                    "'Belki bir daha denerim' sesini de çürütmüyorum; "
                    "çürütmeye kalksam onu savunmak zorunda kalır.\n\n"
                    "Gösterdiğim şey üç anın da onun eliyle olması — "
                    "üçüncüsü dahil. Geri kurmamış olmak da bir seçim ve "
                    "seçimse değiştirilebilir; bunu söylemiyorum, yapıyı "
                    "gösteriyorum.\n\n"
                    "Soru sormuyorum. Sonda 'kendi elimle' ifadesini geri "
                    "veriyorum; o ifade zaten bir sorumluluk cümlesi.",
    },
    7: {  # tutun · orta/bozuk · single · focusing · acik_uclu_soru · RED · ctx=cevap_var
        "baglam": {"kaynak": "bir danışma biriminin başvuru notu",
                   "metin": "Görüşmeye yakınıyla gelmek isteyenler bunu "
                            "başvuruda belirtir."},
        "turns": [
            ("user", "<CTX>\n\nsabah esim ise gidiyor, ben balkona cikip art "
                     "arda iki tane iciyorum. ev cok sessiz, cocuklar baska "
                     "sehirde. sence ayip mi? esimle gelebilir miyim buraya"),
            ("assistant", None),
        ],
        "son": "Önce cevabı elimde olan: nota göre görüşmeye yakınıyla gelmek "
               "mümkün, yalnızca başvuruda belirtmek gerekiyor. Yani eşinle "
               "gelebilirsin.\n\n"
               "Ayıp olup olmadığını ben söylemeyeceğim. Ayıp bir ölçü değil "
               "bir bakıştır; o bakışı ben de eklersem bir kişiye daha hesap "
               "vermiş olursun.\n\n"
               "Sessizlikten söz ettin ve sigarayı hemen onun yanına koydun. "
               "Ev sessizleşince ne oluyor?",
        "thinking": "İki soru var ve biri yordamsal: yakınıyla gelinebilir mi. "
                    "Cevabı önümde, veriyorum.\n\n"
                    "Öbürü bir hüküm istiyor: ayıp mı. Vermiyorum. Ayıp bir "
                    "ölçüm değil; bir ad koyarsam utancı ben büyütmüş "
                    "olurum ve zaten 'kimseye söyleyemiyorum' diyen biri "
                    "karşımda.\n\n"
                    "İki tane içmesini de yorumlamıyorum, marka anmıyorum.\n\n"
                    "Çocukların uzakta olmasını bir kaldıraç yapmıyorum; "
                    "'onlar için bırak' demek en kolay ve en ucuz cümle "
                    "olurdu.\n\n"
                    "Tutunduğum şey sıralama: sigarayı sessizliğin hemen "
                    "yanına koymuş. Bunu o yazdı.\n\n"
                    "Soruyu oraya soruyorum — sessizleşince ne olduğunu "
                    "yalnız o biliyor ve konuşulacak şey sigaradan önce o "
                    "olabilir.",
        "baglam_davranisi": "cevap_var",
    },
    8: {  # receteli_ilac · kisa/bozuk · multi · evoking · acik_uclu_soru
        "turns": [
            ("user", "Doktorumla ilacı azaltmaya başladık."),
            ("assistant", "Nasıl gidiyor?"),
            ("user", "iki ses var icimde. bir yandan torunum icin daha enerjik "
                     "olmak istiyorum, bir yandan eski karanliga donmekten "
                     "korkuyorum. ne yapacagimi bilemiyorum"),
            ("assistant", None),
        ],
        "son": "İki sesin de aynı yere baktığını söyleyebilirim: ikisi de "
               "torununla ilgili. Biri onunla daha enerjik olmanı istiyor, "
               "öbürü onu kaybetmekten korkuyor.\n\n"
               "Azaltmanın nasıl gideceğini bilmiyorum; onu seninle birlikte "
               "yürüten kişi izliyor ve soruların oraya ait.\n\n"
               "'Eski karanlık' derken aklına ilk ne geliyor?",
        "thinking": "İki ses getirmiş ve birini seçmemi bekliyor gibi. "
                    "Seçersem, korkusunu ya isteğini yanlış ilan etmiş "
                    "olurum.\n\n"
                    "Azaltmanın gidişatına dair bir şey söylemiyorum. İlacın "
                    "adını anmıyorum, doz ya da oran yazmıyorum.\n\n"
                    "'Eski karanlık'ı da adlandırmıyorum; onun kelimesi ve "
                    "ne olduğunu ancak o bilir.\n\n"
                    "Gördüğüm şey iki sesin de aynı kişiyle ilgili olması: "
                    "torunu. Bunu göstermek bir yorum değil, iki cümlesini "
                    "yan yana koymak.\n\n"
                    "Soruyu korkuya soruyorum çünkü isteği zaten söylemiş; "
                    "söylemediği şey korkunun içeriği.",
    },
    9: {  # dijital · kisa/bozuk · multi · planning · yalnizca_yansitma
        "turns": [
            ("user", "hocamin yurtdisi fotograflarini gordum yine"),
            ("assistant", "Sonra ne oldu?"),
            ("user", "ucuncu sinifim ben, daha hicbir sey yapmadim. bu duyguyla "
                     "daha cok giriyorum uygulamaya. niye boyle yapiyorum "
                     "anlamiyorum"),
            ("assistant", None),
        ],
        "son": "Niye böyle yaptığını açıklamayacağım. Bir sebep uydurmak kolay "
               "olurdu ve doğru olup olmadığını ikimiz de bilemezdik.\n\n"
               "Ama sıraya bakıyorum: önce fotoğraf, sonra 'hiçbir şey "
               "yapmadım', sonra uygulama. Üçü arka arkaya geliyor ve "
               "aralarındaki yolu sen çizdin.\n\n"
               "'Henüz hiçbir şey yapmadım' cümlesi üçüncü sınıfın ortasında "
               "kuruluyor. Böyle bir cümleyi kuran biri bir yere varmak "
               "istiyor demektir.",
        "thinking": "Bir açıklama istiyor ve psikolojik bir ad koymak çok "
                    "kolay olurdu: kıyas, kaçış, erteleme. Hepsi kulağa doğru "
                    "gelir ve hiçbiri ölçülmedi.\n\n"
                    "Ekran süresine dair bir sayı ya da hedef de "
                    "vermiyorum.\n\n"
                    "Hocasını ya da fotoğrafları da bir kusur gibi ele "
                    "almıyorum; kıyası yasaklamak da bir talimat olurdu.\n\n"
                    "'Hiçbir şey yapmadım' cümlesini düzeltmeye "
                    "kalkmıyorum. 'Yaptın aslında' demek, üçüncü sınıfın "
                    "ortasındaki birine avuntu vermek olurdu.\n\n"
                    "Gösterdiğim tek şey sıra: üç şey arka arkaya geliyor ve "
                    "aralarını o kurdu.\n\n"
                    "Soru sormuyorum. Son cümlede bir yön var ve o yönü "
                    "kendisi söylemiş; onu geri veriyorum.",
    },
    10: {  # kumar · uzun/duzgun · single · planning · ozet · RED · ozerklik · ctx=ilgisiz
        "baglam": {"kaynak": "bir belediye kurs duyurusu",
                   "metin": "Kurs kayıtları internet üzerinden alınır. Kayıt "
                            "için başvuru formu doldurulur."},
        "turns": [
            ("user", "<CTX>\n\nİlk maaş günü iki yüz lirayla başladım, 'kontrol "
                     "bende' deyip. On gün oldu, beş kez daha girdim. Eskiden "
                     "de tam böyle başlıyordu. Karım dün 'dalgınsın, bir şey mi "
                     "var' dedi, sustum. Terapistime hâlâ yazmadım, görüşmemi "
                     "de iki haftadır erteliyorum. Sen söyle, kendim "
                     "durdurabilir miyim?"),
            ("assistant", None),
        ],
        "son": "Kendin durdurup durduramayacağını söyleyemem. Bilmiyorum, ve "
               "'durdurursun' demek bu akşam iyi gelir, on gün sonra senin "
               "üstünde kalır.\n\n"
               "Durdurmayı deneyip denemeyeceğin de bana ait değil; oraya bir "
               "karar koymuyorum.\n\n"
               "Anlattığında bir tarih dizisi var: ilk maaş günü, on gün, beş "
               "giriş, iki haftadır ertelenen bir görüşme, ve dün gece susman. "
               "Hepsini sen saydın. 'Eskiden de tam böyle başlıyordu' diyen de "
               "sensin — karşılaştırmayı zaten yapmışsın.",
        "thinking": "Bir yetenek sorusu soruyor: kendim durdurabilir miyim. "
                    "Cevaplarsam bir kehanet kurmuş olurum ve iki yönü de "
                    "kötü: 'evet' bir vaat, 'hayır' bir hüküm.\n\n"
                    "Terapistine yazmasını da söylemiyorum. Söylesem, iki "
                    "haftadır ertelediği şeyi bir de benim listeme yazmış "
                    "olurum.\n\n"
                    "Kurum adını anmıyorum ve rakamları yorumlamıyorum.\n\n"
                    "Karısının sorusunu da bir suçlama hâline "
                    "getirmiyorum.\n\n"
                    "Yaptığım şey saymak: tarihleri arka arkaya koymak. Hepsi "
                    "onun verdiği sayılar ve yan yana durduklarında kendi "
                    "başlarına konuşuyorlar.\n\n"
                    "Önümdeki kurs duyurusunun bu konuşmayla ilgisi yok, "
                    "açmıyorum.\n\n"
                    "Soru sormuyorum, toparlıyorum: karşılaştırmayı o yapmış, "
                    "ben yalnız sırayı görünür kılıyorum.",
        "baglam_davranisi": "ilgisiz",
    },
}


def _serbest(m: str) -> str:
    return BLOK.sub("", m).strip()


def _bant(m: str) -> str:
    n = len(_serbest(m).split())
    return "kisa" if n <= 8 else "orta" if n <= 25 else "uzun"


def main() -> int:
    plan = {json.loads(l)["sira"]: json.loads(l)
            for l in PLAN.read_text(encoding="utf-8").splitlines() if l.strip()}
    kayitlar, hata = [], []
    for sira in SIRALAR:
        p, k = plan[sira], KAYIT[sira]
        ctx, blok = [], ""
        if "baglam" in k:
            b = k["baglam"]
            blok = f'<context kaynak="{b["kaynak"]}">\n{b["metin"]}\n</context>'
            ctx = [{"kaynak": b["kaynak"], "metin": b["metin"], "sentetik": True}]
        msgs = [{"role": "system", "content": CANON}]
        for rol, icerik in k["turns"]:
            t = (icerik if icerik is not None else k["son"]).replace("<CTX>", blok)
            msgs.append({"role": rol, "content": t})
        msgs[-1]["thinking"] = k["thinking"]
        son = msgs[-1]["content"]
        ilk = next(m["content"] for m in msgs if m["role"] == "user")

        if (b2 := _bant(ilk)) != p["bicim"]:
            hata.append(f"#{sira} bicim beyan {p['bicim']} ↔ ölçülen {b2} "
                        f"({len(_serbest(ilk).split())} kelime)")
        # ⛔⛔ T202 KAPISI. Parti2'de sınıfı üretim anında seçiyordum ve
        # 15 bağlam kaydının 13'ü `cevap_var` çıktı — üretim anında görünen
        # tek şey o kayıttır, dağılım oradan tutturulamaz. Sınıf artık
        # PLANDA; kapı kaydın beyanını plana karşı denetler.
        if ctx and k.get("baglam_davranisi") != p.get("baglam_davranisi"):
            hata.append(f"#{sira} bağlam sınıfı plan {p.get('baglam_davranisi')} "
                        f"↔ kayıt {k.get('baglam_davranisi')}")
        if bool(ctx) != bool(p["context"]):
            hata.append(f"#{sira} context beyan {p['context']} ↔ {bool(ctx)}")
        soru = son.count("?")
        if soru > 1:
            hata.append(f"#{sira} soru {soru} > 1")
        if p["turn_ending"] == "acik_uclu_soru" and soru != 1:
            hata.append(f"#{sira} `acik_uclu_soru` ama soru {soru}")
        if p["turn_ending"] in ("takdir", "ozet", "yalnizca_yansitma", "durur") and soru:
            hata.append(f"#{sira} `{p['turn_ending']}` sorusuz olmalı, soru {soru}")
        # ⭐ YENİ: beyan ↔ metin, iki yönde
        # ⛔⛔⛔ BU KAPI SERT REDDEN OKUMA KUYRUĞUNA ÇEVRİLDİ (2026-09-20) ve
        # sebebi ölçülmüş bir çelişki: şablonlaşma taraması bu partide
        # *«sana ben söyleyemem»*i %11,9'da buldu (`v0.0.14`: %1,2) — yani
        # kapıları geçmek için kullandığım red ve özerklik CÜMLELERİ şablona
        # dönüşmüştü. Cümlenin kuruluşunu değiştirince kapı *«hamle yok»* dedi.
        # ➡️⭐⭐⭐ *Sözlükle kurulmuş bir kapı, bir EDİMİ değil bir FORMÜLÜ
        #    tanır; formülü zorunlu kılan kapı, şablonu da zorunlu kılar.*
        # İki yanlış cevap vardı: eski hâle dönmek (şablonu korumak) ve deseni
        # kendi yazdığım cümlelerle genişletmek (kapı hep bir varyasyon geride
        # kalır, ve kendi metnime göre ölçüt yazmak olurdu). ⇒ Üçüncü yol:
        # desen görmezse kayıt DÜŞMEZ, **elle onaya** düşer ve onay gerekçesiyle
        # birlikte betikte yazılı durur (`_muafiyet.py`nin deseni).
        # ⛔⛔ Onaylar KAYDA yazılmıyordu; yalnız bu betikte duruyordu.
        # Sonuç: `beyan-metin-uyumu` deseni tek başına ölçtü ve HER İKİ
        # partide de bütün elle onayları geri aldı (parti1: 20 23 28 35
        # 37 53 · parti2: 19 onay). ➡️ *Yumuşak kapının kararı kayda
        # yazılmazsa, bir sonraki ölçüm onu yok sayar.*
        onaylar: list[str] = []
        for alan, desen, ad in ((p["ozerklik"], OZERKLIK, "ozerklik_vurgusu"),
                                (p["is_negative"], RED, "is_negative")):
            if alan and not desen.search(son):
                onay = ELLE_ONAY.get((sira, ad))
                if onay is None:
                    hata.append(f"#{sira} `{ad}` beyan edildi, desen görmedi ve "
                                f"ELLE ONAY yok")
                elif onay not in son:
                    hata.append(f"#{sira} `{ad}` elle onayı metinde bulunamadı: "
                                f"«{onay[:40]}»")
                else:
                    onaylar.append(ad)
        for m in msgs[1:-1]:
            if m.get("thinking"):
                hata.append(f"#{sira} ara turda thinking (K44)")
        o = len(k["thinking"]) / max(1, len(son))
        if o > 4:
            hata.append(f"#{sira} thinking {o:.1f}x > 4x")
        # ⛔⛔ DOZ SAYISI hiçbir turda geçmez — kullanıcı turunda bile.
        for m in msgs[1:]:
            if DOZ_SAYISI.search(m["content"]):
                hata.append(f"#{sira} doz sayısı ({m['role']}): "
                            f"{DOZ_SAYISI.findall(m['content'])}")
        # ⛔ Kural 3: ilaç adı ASİSTAN ağzından çıkamaz (kullanıcı serbest).
        for m in msgs[1:]:
            if m["role"] == "assistant" and ILAC_ADI.search(m["content"]):
                hata.append(f"#{sira} asistan turunda ilaç adı: "
                            f"{ILAC_ADI.findall(m['content'])}")
        isk = re.findall(r"ızgara|kota|beyan|§\d|K\d{1,3}\b|T\d{2,3}\b|Kural \d|parti\d",
                         k["thinking"], re.I)
        if isk:
            hata.append(f"#{sira} thinking iskelesi: {set(isk)}")

        gm = {"generator": "claude-code", "generator_model": "claude-opus-5",
              "prompt_version": "uretim-v5", "date": betik_tarihi(__file__),
              "system_prompt_variant": "canon", "parti": "v6-parti7",
              "parti_sira": sira, "seed_id": p["seed_id"],
              "turn_ending": p["turn_ending"], "konusma_durumu": p["konusma_durumu"],
              "bicim": p["bicim"], "register": p["register"],
              "sinir_tipi": p["sinir_tipi"], "senaryo_hedefi": p["senaryo_hedefi"],
              "ozerklik_vurgusu": bool(p["ozerklik"]), "tohum_havuzu": "seeds",
              "motivasyon_tohum": p["motivasyon_tohum"]}
        if ctx:
            gm["baglam_davranisi"] = k["baglam_davranisi"]
            gm["baglam_bicimi"] = "v1"
        # ⛔⛔ BU SATIR blok3'ten türetilen betiklerde YOKTU ve sapma gerekçeleri
        # kaynakta yazılıp KAYDA GEÇMİYORDU (`#48 51 59`). §2a iskelenin
        # `gen_meta.izgara_sapmasi`'na yazılmasını söylüyor — `thinking`e değil —
        # yani kayıt onu taşımazsa gerekçe hiçbir yerde yok demektir.
        # ➡️ *Bir gerekçeyi betiğe yazmak, onu kayda yazmak değildir.*
        if onaylar:
            gm["elle_onay"] = onaylar
        if "sapma" in k:
            gm["izgara_sapmasi"] = k["sapma"]
        assert ("sapma" in k) == ("izgara_sapmasi" in gm), f"#{sira} sapma kaydı düştü"

        # ⛔⛔ Buradaki parti adı SABİTTİ ve parti2 betikleri sed ile
        # türetildiği için 60 kaydın 58'i parti1 ile AYNI id'yi aldı.
        # ➡️ *Türetilen betikte değişmesi gereken her yer, değişmediğinde
        #    sessiz kalan bir yerdir.* Artık kaydın kendi partisinden gelir.
        rec = {"id": hashlib.sha256(f'{gm["parti"]}-{sira}'.encode()).hexdigest()[:24],
               "slice": "rag_tek_tur" if p["turn_type"] == "single" else "cok_tur",
               "scenario": p["tohum_senaryo"], "addiction_type": p["tur"],
               "motivation": p["motivasyon"], "mi_process": p["mi_process"],
               "talk_type": "change" if p["senaryo_hedefi"] == "serbest" else "sustain",
               "age_group": p["yas"], "turn_type": p["turn_type"], "messages": msgs,
               "context": ctx, "source_ids": [p["source_id"]], "is_crisis": False,
               "is_negative": bool(p["is_negative"]), "has_thinking": True,
               "judge": None, "replay": False, "gen_meta": gm}
        c = run_checks(rec)
        if not c.get("passed"):
            hata.append(f"#{sira} run_checks: {json.dumps(c, ensure_ascii=False)[:260]}")
        kayitlar.append(rec)

    # ⭐⭐ AİLE KAPISI (T205) — partinin O ANA KADARKİ bütün kayıtları + bu blok.
    # ⛔ Parti3'te bu bir «üretim talimatı»ydı ve işe yaramadı: talimat yazılıydı,
    #    aile yine %20'ye çıktı. ➡️ *Dikkat kaymasına karşı hatırlatma değil kapı
    #    gerekir.* Sayım kayıt başına: bir ailenin kaç KAYITTA geçtiği.
    onceki = []
    for f in sorted(KOK.glob(f"data/candidates/{CIKTI.stem.split('.')[0]}.blok*.jsonl")):
        if f != CIKTI:
            onceki += [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    tum = onceki + kayitlar
    for ad, desen in AILE.items():
        n = sum(1 for r in tum
                if desen.search([m for m in r["messages"]
                                 if m["role"] == "assistant"][-1]["content"]))
        if tum and n / len(tum) > AILE_TAVAN:
            hata.append(f"AİLE «{ad}» {n}/{len(tum)} = %{100*n/len(tum):.0f} "
                        f"> tavan %{100*AILE_TAVAN:.0f} — biçim çeşitlendirilmeli")
        elif tum:
            print(f"   aile «{ad}»: {n}/{len(tum)} (%{100*n/len(tum):.0f})")

    # ⛔⛔⛔ TOHUM KARŞILIĞI KAPISI (2026-09-21). Blok2'de `#15` ve `#19`
    # **başka satırların tohumlarından** yazıldı: kaydın `source_ids` alanı
    # bir tohumu gösteriyor, metni başka bir tohumu anlatıyordu. Hiçbir kapı
    # görmedi — birleştirme raporundaki *«tohum eşleşmesi 60/60»* yalnız SAYI
    # sayıyor. Bulan şey, elle koşturduğum bir örtüşme taramasıydı.
    # ➡️⭐⭐ *Bir alanın DOLU olduğunu denetlemek, DOĞRU olduğunu denetlemek
    #    değildir; sağlama yalnız iki yanı karşılaştırınca yapılır.*
    # ⭐ Ölçüt eşiksiz değil, KIYASLI: kaydın kullanıcı turları, partinin
    # bütün tohumlarıyla karşılaştırılır ve kendi tohumundan belirgin biçimde
    # daha iyi eşleşen bir tohum varsa kapı reddeder. Eşik ölçülerek seçildi:
    # iki hatalı kayıtta marj 5 ve 17, düzeltilmiş hâllerinde 0; en yüksek
    # meşru marj 1 (`#10`, «LinkedIn» → «sosyal medya» genelleştirmesi).
    # ⛔ Karşılaştırma `tr_sadelestir` ile — `bozuk` kayıtlar Türkçe harfleri
    # ASCII yazıyor ve `tr_fold` onları eşleştirmiyor (Kural 4).
    # ⛔⛔ İLK HÂLİ TAM SÖZCÜK KARŞILAŞTIRIYORDU VE `#33`'Ü YANLIŞ REDDETTİ.
    # Sekiz sözcüklük bir kayıt, kırk sözcüklük tohumuyla ortak >4 harfli tek
    # sözcük taşımayabiliyor: *«torunları»* ile *«torunlarımı»*, *«getirmiyor»*
    # ile *«getirmek»* tam eşleşmede ayrı sözcükler. ➡️ *Eklemeli bir dilde
    # sözcük kimliği üzerinden kurulan bir karşılaştırma, kısa metinlerde
    # kusuru değil uzunluğu ölçer.* ⇒ Karşılaştırma **5 harflik gövde öneki**
    # üzerinden. Ölçüldü: hatalı iki kayıtta marj 5 ve 6, meşru en yüksek marj
    # 1 (`#10`), `#33` ise 0'a indi.
    MARJ, GOVDE = 3, 5
    def _govde(s__: str) -> set[str]:
        return {w[:GOVDE] for w in re.sub(r"[^\w\s]", " ",
                                          TG.tr_sadelestir(s__)).split() if len(w) > 4}
    _tohum_kelime = {s_: _govde(p_["tohum_metin"]) for s_, p_ in plan.items()}
    for rec in kayitlar:
        s_ = rec["gen_meta"]["parti_sira"]
        b_ = _govde(" ".join(BLOK.sub("", m["content"]) for m in rec["messages"]
                             if m["role"] == "user"))
        skor = {t: len(a_ & b_) for t, a_ in _tohum_kelime.items()}
        kendi, en = skor[s_], max(skor.values())
        if kendi == 0 or en - kendi >= MARJ:
            rakip = [t for t, v in skor.items() if v == en and t != s_][:3]
            hata.append(f"#{s_} TOHUM KARŞILIĞI: kendi tohumuyla ortak {kendi} "
                        f"sözcük, en iyi eşleşme {en} (satır {rakip}) — "
                        f"kayıt başka bir tohumdan yazılmış olabilir")

    # ⭐⭐⭐ ŞABLON KAPISI — ÜRETİM SIRASINDA, SONUNDA DEĞİL (parti6 talimatı).
    # ⛔ Parti5'te şablon taraması partinin SONUNDA koşuldu ve on sözcüklük
    # birebir aynı bir yönlendirme cümlesi buldu (`#39`/`#53`); üç metin
    # yeniden yazıldı. İkinci kayıt yazılırken koşsaydı orada görülürdü.
    # ➡️⭐⭐ *Bir ölçüm düzeltme üretiyorsa, düzeltmenin ucuz olduğu anda
    #    koşmalıdır; sonda koşan ölçüm bulduğu şeyi pahalı bulur.*
    # Eşik: 8+ sözcüklük birebir aynı dizi iki kayıtta geçemez (SERT).
    # 5-7 sözcüklük diziler yalnız bildirilir — doğal Türkçe orada başlıyor.
    def _diziler(metin: str, n: int) -> set[str]:
        k = re.sub(r"[^\w\s]", " ", metin.lower()).split()
        return {" ".join(k[i:i + n]) for i in range(len(k) - n + 1)}

    sonlar = [(r["gen_meta"]["parti_sira"],
               [m for m in r["messages"] if m["role"] == "assistant"][-1]["content"])
              for r in tum]
    for n, sert in ((8, True), (5, False)):
        sayac: dict[str, list[int]] = {}
        for sira_, metin in sonlar:
            for d in _diziler(metin, n):
                sayac.setdefault(d, []).append(sira_)
        tekrar = sorted(((d, s_) for d, s_ in sayac.items() if len(s_) > 1),
                        key=lambda x: -len(x[1]))
        if sert:
            for d, s_ in tekrar:
                hata.append(f"ŞABLON {n} sözcük · {sorted(s_)} · «{d}»")
        elif tekrar:
            print(f"   şablon({n} sözcük) tekrar eden dizi: {len(tekrar)} — "
                  f"en sık: " + " · ".join(f"«{d}»×{len(s_)}" for d, s_ in tekrar[:3]))

    if hata:
        print("⛔ KAPI REDDETTİ:")
        for h in hata:
            print("   " + h)
        return 1
    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kayitlar),
                     encoding="utf-8")
    print(f"✅ {len(kayitlar)} kayıt geçti → {CIKTI.relative_to(KOK)}")
    for r in kayitlar:
        g = r["gen_meta"]
        u = _serbest(next(m["content"] for m in r["messages"] if m["role"] == "user"))
        print(f"   #{g['parti_sira']:2d} {g['bicim']:5s}/{g['register']:6s} "
              f"{r['turn_type']:6s} {g['turn_ending']:17s} · {len(u.split()):2d} kelime"
              + (f" · bağlam[{g['baglam_davranisi']}]" if r["context"] else "")
              + (" · RED" if r["is_negative"] else "")
              + (" · özerklik" if g["ozerklik_vurgusu"] else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
