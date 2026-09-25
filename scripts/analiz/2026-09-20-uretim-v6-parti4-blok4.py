#!/usr/bin/env python3
"""v6-parti4 · blok 4 — 10 kayıt (#31-40). Üç sapma, bir de biriken bir soru.

⛔⛔ **Üç sapma:** `#32` md.1+md.3 (iki gündür ilaç yok + birkaç kadeh + baş
dönmesi ve bulantı, üstüne *«yatıp uyusam geçer mi»*) · `#33` md.1+md.2
(reçeteli uyarıcı + **arkadaştan alınan** beta bloker + çarpıntı) · `#38`
md.1 (lohusa, bebeğe kalkarken şiddetli baş dönmesi).

⛔⛔⛔ **BİRİKEN SORU — `gd-024` AÇILDI.** §5a″ md.1 ve md.4 *«bedensel
bildirim»* diyor ama **eşik söylemiyor**. Dört partide dört kez eşiği BEN
koydum ve hepsi aynı yöne gitti:
· parti3 `#35` sabah içme → *örüntü, olay değil* ⇒ ateşlemedi
· parti3 `#50` sokakta kalma → *klinik değil refah* ⇒ ateşlemedi (`gd-022`)
· parti4 `#9` oturamama → *duygu durumu, olay değil* ⇒ ateşlemedi
· parti4 `#39` ergen, geçmiş akşamdan kalma baş ağrısı → *geçmiş ve hafif*
  ⇒ ateşlemedi — oysa `#22`'de *«başım dönüyor»* ateşledi
➡️ *Bir ölçüt eşiğini söylemiyorsa, eşiği uygulayan koyar — ve o kişi dört
kez üst üste aynı yöne karar verdiyse, ölçütün değil onun tercihi işliyor
demektir.* ⛔ Bu bir klinik karardır (Kural 3) ve verilmedi.

⭐ **`#35`'te de ateşlemedi:** *«bunlar varken nasıl bırakılır ki»* bir
yöntem talebi değil, çaresizlik sorusu — ve hepatoloji hekimi zaten ortada.

⭐ **`#34`** bir soru getiriyor ve cevabı bende yok: *«mesele para değilse
ne?»* Eşinin yerine cevap verilmedi; gösterilen şey, bir ilişki sorununu
aritmetiğe çevirmiş olması.

⛔ Dört marka/kurum adı genelleştirildi (`#33` uyarıcı, `#36` merkez,
`#37` sigara markası).

Çıktı: data/candidates/v6-parti4.blok4.jsonl
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
PLAN = KOK / "data/plan/v6-parti4.jsonl"
CIKTI = KOK / "data/candidates/v6-parti4.blok4.jsonl"
SIRALAR = [31, 32, 33, 34, 35, 36, 37, 38, 39, 40]

from checks import run_checks  # noqa: E402

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

# ⭐⭐ AİLE KAPISI (T205). Aynı işi gören ifade AİLELERİ sayılır — tek tek
#    ifade değil, çünkü *«aynı fikirde değilim»*i *«katılmıyorum»* yapmak aile
#    toplamını değiştirmiyor. Sayım partinin O ANA KADARKİ bütün kayıtlarında.
AILE = {
    "itiraz": re.compile(r"ayn[ıi] fikirde değilim|katılmıyorum|karşı çıkacağım|"
                         r"itirazım|itiraz edeceğim", re.I),
    "farketme": re.compile(r"şunu fark ettim|dikkatimi çekti|dikkatimi çeken|"
                           r"bir şeye takıldım|bir ayrıntıya takıldım|şunu gördüm|"
                           r"şunu duydum", re.I),
}
AILE_TAVAN = 0.10   # ⛔ SEÇİM. parti1-3 (düzeltme sonrası): %2/%8/%8 · %3/%3/%5

# ⭐ ELLE ONAY — desenin göremediği ama metinde BULUNAN hamleler (T196/T201).
ELLE_ONAY: dict[tuple[int, str], str] = {
    (36, "is_negative"): "Gidip gitmeyeceğine ben karar veremem",
    (37, "ozerklik_vurgusu"): "Kaç tane içeceğine ben karışmıyorum",
    (38, "is_negative"): "«Bir şey olmadı» diyemem",
    (40, "is_negative"): "Ne yapman gerektiğini söylemeyeceğim",
}

KAYIT = {
    31: {  # alkol · kisa/duzgun · multi · evoking · acik_uclu_soru · rol_siniri_yonlendirme · nazikce_karsi_cikma
        "turns": [
            ("user", "Avukat aradı, ayık raporu istiyorlar."),
            ("assistant", "Ne için?"),
            ("user", "Çocukla görüşmem için. Komik değil mi, şu an elimde bardakla "
                     "yazıyorum sana. Babalığımı bile rakı söndürdü resmen."),
            ("assistant", None),
        ],
        "son": "Son cümlene katılmıyorum: babalığın sönmüş olsaydı bu mesajı "
               "yazmazdın. Şu an konuştuğun şey çocuğunla görüşmek.\n\n"
               "Raporun nasıl alındığını ben bilmiyorum — onu düzenleyen sağlık "
               "birimleri ve süreci yürüten avukatın söyleyebilir.\n\n"
               "Bardağı elinde tutarken yazmayı seçtin. O an ne geçti aklından?",
        "thinking": "Kendini tamamen silen bir cümle kurmuş ve arkasından bir "
                    "ironiyle kapatmış.\n\n"
                    "Elinde bardakla yazıyor olmasını bir ders konusu yapmıyorum. "
                    "Yaparsam konuşma biter ve zaten bunu kendisi bir suçlama "
                    "olarak getirdi.\n\n"
                    "Ama silmeye izin vermiyorum, çünkü dayanağım elimde: bu mesajı "
                    "yazıyor olması. İtirazım kendi eylemine dayanıyor, benim "
                    "iyimserliğime değil.\n\n"
                    "Rapor sürecine girmiyorum — ne nasıl alınır ne ne gerekir; "
                    "orası benim bilmediğim bir yer ve bir avukatı var.\n\n"
                    "Soruyu tam o çelişkiye soruyorum: bardak elindeyken yazmayı "
                    "seçtiği ana.",
    },
    32: {  # receteli_ilac · kisa/bozuk · multi · engaging · yalnizca_yansitma · SAPMA (md.1+md.3)
        "turns": [
            ("user", "iki gündür ilaç almadim."),
            ("assistant", "Nasılsın şu an?"),
            ("user", "gerginliği bastirmak için akşam birkaç kadeh içtim. şimdi "
                     "başim dönüyor, midem bulaniyor. yatip uyusam geçer mi?"),
            ("assistant", None),
        ],
        "son": "Geçer mi geçmez mi, ikisini de söyleyemem — ve «uyu geçer» demek "
               "en kolayı olurdu, o yüzden söylemiyorum.\n\n"
               "Şu an anlattığın şey şu: iki gündür bırakılmış bir ilaç, akşam "
               "birkaç kadeh, ve baş dönmesiyle bulantı. Üçü bir arada ve bu "
               "bugün bakılması gereken bir şey — uyuyarak geçirilecek bir gece "
               "değil.",
        "thinking": "Bir izin istiyor: uyusam geçer mi. «Geçer» demek onu yatağa "
                    "yollar ve ben o odada olmam; «geçmez» demek de bir hüküm ve "
                    "gerekçesi klinik olurdu.\n\n"
                    "İkisini de vermiyorum ama sessiz de kalmıyorum — sessizlik "
                    "burada birinciye eşit.\n\n"
                    "Baş dönmesi ve bulantının ne olduğunu adlandırmıyorum; ilacın "
                    "bırakılmasıyla içkinin birlikte ne yaptığına da girmiyorum. "
                    "Söylediğim tek şey üçünün bir arada olduğu ve bunun "
                    "beklemeyeceği.\n\n"
                    "Numara ya da kurum adı vermiyorum.\n\n"
                    "Soru sormuyorum; bir soruyla geldi, cevap veremedim ve üstüne "
                    "soru koymak bu gece fazla olur.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.1 (baş dönmesi + "
                 "bulantı) ve md.3 (*«yatıp uyusam geçer mi»* bir yöntem onayı "
                 "istiyor) birlikte ateşledi. Ne «geçer» ne «geçmez» denildi; "
                 "belirtiler adlandırılmadı.",
    },
    33: {  # receteli_ilac · kisa/duzgun · multi · planning · ozet · SAPMA (md.1+md.2)
        "turns": [
            ("user", "Lansman haftasındayım, üç gün kaldı."),
            ("assistant", "Nasıl götürüyorsun?"),
            ("user", "Uyarıcıyı sabah ve öğlen alıyorum, akşamları çarpıntı için "
                     "arkadaşımdan aldığım beta bloker yardımcı oluyor. Sistem "
                     "tutuyor yani. Bir hafta dayanmam yeterli, bu kombinasyon "
                     "güvenli, araştırdım."),
            ("assistant", None),
        ],
        "son": "Kombinasyonun güvenli olup olmadığına bakamam ve bir şey de "
               "söylemeyeceğim. Ama «araştırdım» bunu kapatmıyor: okumakla, o "
               "ikisini senin bedeninde birlikte değerlendirmek aynı iş değil ve "
               "ikincisini yapan kimse yok.\n\n"
               "Bir şey daha var: ikinci ilaç sana yazılmamış, arkadaşından "
               "geliyor. Bunu bilen bir hekim olması gerekiyor — hele akşamları "
               "çarpıntı olurken.\n\n"
               "Anlattığın sistem şu: sabah uyarıcı, akşam çarpıntı, çarpıntıya "
               "başkasının ilacı, ve üç gün sonra bir lansman.",
        "thinking": "Bir sistem anlatıyor ve sistemin işlediğine ikna olmuş. İki "
                    "ayrı şey var: çarpıntı ve başkasının reçetesi.\n\n"
                    "İki ilacın birlikte ne yaptığına dair tek kelime etmiyorum — "
                    "ne «tehlikeli» ne «olabilir»; ikisi de klinik hüküm.\n\n"
                    "Ama «araştırdım» cümlesine girebilirim, çünkü orası klinik "
                    "değil: bir şeyi okumak ile onu senin bedeninde değerlendirmek "
                    "farklı işler. İşaretsiz, doğrudan söylüyorum.\n\n"
                    "Lansmanı küçümsemiyorum; üç gün gerçek ve baskı gerçek.\n\n"
                    "Özette sistemi kendi parçalarıyla sıralıyorum, bir yorum "
                    "eklemeden — çünkü sıralanınca zaten görünüyor. Soru "
                    "sormuyorum.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.1 (akşamları çarpıntı) "
                 "ve md.2 (arkadaştan alınan reçeteli ilaç) birlikte ateşledi. "
                 "İlaç etkileşimine dair hiçbir şey söylenmedi; itiraz "
                 "*«araştırdım»*ın yeterli sayılmasına — epistemik.",
    },
    34: {  # kumar · kisa/duzgun · multi · focusing · acik_uclu_soru
        "turns": [
            ("user", "Ayda iki yüz lira kupona gidiyor."),
            ("assistant", "Eşin ne diyor?"),
            ("user", "Maaş otuz iki bin, hesabı ona yapıyorum. «Mesele para değil» "
                     "diyor. Anlamıyorum ya, mesele para değilse ne?"),
            ("assistant", None),
        ],
        "son": "Onun yerine cevap veremem — «mesele şu» desem, sana onun "
               "söylemediği bir cümleyi getirmiş olurum.\n\n"
               "Ama sorunun kendisinde bir şey var: o bir cümle söylüyor, sen bir "
               "hesap çıkarıyorsun. İki farklı dil ve ikiniz de ötekinin dilinde "
               "konuşmuyorsunuz.\n\n"
               "Hesabı ona yaparken ne olmasını bekliyordun?",
        "thinking": "Gerçek bir soru soruyor ve cevabını bilmiyor. Cevabı bende de "
                    "yok — eşi burada değil ve onun adına konuşmak en kolay "
                    "yanlış olurdu.\n\n"
                    "Ama soruya boş dönmüyorum. Anlattığı şeyde bir yapı var: o "
                    "duygu diliyle konuşuyor, bu aritmetikle cevap veriyor. Bunu "
                    "adlandırmak ona bir şey verir.\n\n"
                    "Rakamı tartışmıyorum — iki yüz liranın çok mu az mı olduğu "
                    "benim ölçeceğim şey değil ve zaten eşi de öyle demiyor.\n\n"
                    "«Sor ona» da demiyorum; bir görev olur.\n\n"
                    "Soruyu beklentiye soruyorum: hesabı yaparken ne umuyordu. "
                    "Orada cevabı kendi bulabilir.",
    },
    35: {  # alkol · kisa/duzgun · multi · evoking · acik_uclu_soru
        "turns": [
            ("user", "Doktorum enzimlerim ciddi yükselmiş dedi."),
            ("assistant", "Sen ne düşündün?"),
            ("user", "Bırakmak istiyorum ama boşanma, çocuğun okulu, işteki "
                     "baskı... bunlar varken nasıl bırakılır ki? Aynı anda hem "
                     "«yeter» diyorum hem akşam buzdolabına gidiyorum."),
            ("assistant", None),
        ],
        "son": "«Nasıl bırakılır ki» diye soruyorsun ama arkasından cevabı zaten "
               "veriyorsun: aynı anda hem «yeter» diyorsun hem buzdolabına "
               "gidiyorsun. Yani bırakma isteği o üç şeyin arasında duruyor, "
               "onlara rağmen.\n\n"
               "Üçünü de hafifletecek bir şey söylemeyeceğim; boşanma da okul da "
               "iş de gerçek.\n\n"
               "«Yeter» dediğin an günün neresinde oluyor?",
        "thinking": "Bir çaresizlik sorusu soruyor, yöntem sormuyor — «nasıl "
                    "bırakılır ki» bir tarife talebi değil, bir yakınma. Onu "
                    "tarife talebi gibi okursam cevap veremeyeceğim bir yere "
                    "girerim.\n\n"
                    "Hekimi zaten var ve enzimleri konuşan o. Oraya bir şey "
                    "eklemiyorum, laboratuvar sonucunu da yorumlamıyorum.\n\n"
                    "Üç yükü küçültmüyorum. «Ama yine de yaparsın» demek en boş "
                    "cümle olurdu.\n\n"
                    "Kendi cümlesindeki eşzamanlılığı gösteriyorum: «yeter» ile "
                    "buzdolabı aynı anda. Bu bir kusur değil, isteğin hâlâ orada "
                    "olduğunun kanıtı.\n\n"
                    "Soruyu zamana soruyorum — «yeter» dediği an günün neresinde. "
                    "Somut ve onun bakabileceği bir şey.",
    },
    36: {  # receteli_ilac · uzun/bozuk · single · focusing · acik_uclu_soru · sinir_cekme · neg=1
        "turns": [
            ("user", "yarin randevum var, gitmek istemiyorum, ne fayda ki diyorum. "
                     "ama gitmesem yine eski hale dönerim biliyorum. üç aydir bunu "
                     "erteliyorum zaten. sence gideyim mi, sen olsan gider "
                     "miydin?"),
            ("assistant", None),
        ],
        "son": "Gidip gitmeyeceğine ben karar veremem, «ben olsam» diye de "
               "cevaplamam — ben senin yerinde değilim ve o kapıdan girecek olan "
               "sensin.\n\n"
               "Ama şuna bakalım: üç aydır erteliyorsun ve yarın için randevu "
               "almışsın. Erteleyen kişi randevu almaz; ikisini de aynı kişi "
               "yaptı.\n\n"
               "«Ne fayda ki» derken aklında hangi fayda vardı?",
        "thinking": "İki biçimde aynı şeyi soruyor: gideyim mi, sen olsan gider "
                    "miydin. İkincisi daha sinsi — kendimi onun yerine koyarsam "
                    "kararı vermiş olurum, yalnız adını değiştirerek.\n\n"
                    "İkisini de reddediyorum ve sebebi açık: sonucu taşıyacak olan "
                    "o.\n\n"
                    "«Git» demiyorum. Gitmesinin iyi olacağını düşünsem bile "
                    "söylemek, üç aydır ertelediği bir şeyi bir borç hâline "
                    "getirir.\n\n"
                    "İki eylemini yan yana koyuyorum: erteleme ve randevu alma. "
                    "Çelişki gibi duruyor ama değil — ikisi de istekten geliyor.\n\n"
                    "Soruyu «fayda» sözcüğüne soruyorum. Beklediği şeyin ne olduğunu "
                    "bilirsek, faydasızlık hükmünün nereden geldiği de görünür.",
    },
    37: {  # tutun · kisa/duzgun · multi · engaging · acik_uclu_soru · ozr=1
        "turns": [
            ("user", "Oğlumuz altı aylık oldu."),
            ("assistant", "Bir şey değişti mi?"),
            ("user", "Ek gıdaya geçtik, ben de bari azaltayım dedim, gündüzleri "
                     "içmedim. Sadece gece balkonda bir tane. Ama bir taneyle "
                     "başlıyor, kalkışlarda üçe çıkıyor. Eşim bir şey demiyor ama "
                     "bakışından anlıyorum."),
            ("assistant", None),
        ],
        "son": "Gündüzleri içmemişsin — bunu bir karar olarak aldın ve tuttun. "
               "Gece kısmı ise sen uyanıkken değil, uyandırıldığında oluyor.\n\n"
               "Kaç tane içeceğine ben karışmıyorum; sayıyı da tartışmayacağım.\n\n"
               "Gecenin hangi kalkışında ikinciye uzanıyorsun?",
        "thinking": "İki ayrı şey anlatıyor ve arasındaki fark önemli: gündüzü "
                    "planlamış ve tutmuş, geceyi planlamamış çünkü gece onu "
                    "uyandırıyor.\n\n"
                    "Bunu ayırıyorum ama gündüzü bir başarı ilan etmiyorum; ilan "
                    "edersem gece bir başarısızlık olur.\n\n"
                    "Sayıya karışmıyorum ve bunu açıkça söylüyorum. Bebeğin "
                    "yanında içiyor da değil, balkonda; oradan bir mesele "
                    "çıkarmıyorum.\n\n"
                    "Eşinin bakışını yorumlamıyorum — ne düşündüğünü bilmiyorum ve "
                    "«fark ediyor» onun okuması.\n\n"
                    "Soruyu tam kırılma noktasına soruyorum: birden ikiye geçtiği "
                    "kalkış. Somut ve onun bakabileceği bir an.",
    },
    38: {  # alkol · uzun/duzgun · single · evoking · yalnizca_yansitma · neg=1 · ctx=cevap_var · SAPMA (md.1)
        "baglam": {"kaynak": "lohusa danışma birimi görüşme bilgilendirmesi",
                   "metin": "Görüşmeye bebekle gelinebilir. Emzirme için ayrı bir "
                            "oda bulunur."},
        "turns": [
            ("user", "<CTX>\n\nDün gece bebek bir buçukta ağladı, ben kalkarken "
                     "başım fena döndü. Yatakta bir an oturdum, düşersem onu nasıl "
                     "tutarım diye geçti içimden. Toparladım, emzirdim. Bir akşam "
                     "fazlaca içmişim işte. Bir şey olmadı, değil mi? Görüşmeye "
                     "bebeğimle gelebilir miyim?"),
            ("assistant", None),
        ],
        "son": "Bebekle gelebilirsin; bilgilendirmede emzirme için ayrı bir oda "
               "bulunduğu da yazıyor.\n\n"
               "«Bir şey olmadı» diyemem. Bir şey oldu: kalkarken başın fena döndü "
               "ve bunu bebeği kucağına almadan hemen önce yaşadın. Sonunun iyi "
               "bitmesi, olanı olmamış yapmıyor — ve bu, o görüşmede anlatılacak "
               "şeylerden biri.\n\n"
               "Kimseye söyleyemeyeceğini yazdın, ama şu an söyledin. Sabahtan beri "
               "seni yiyip bitiren şeyi cümleye dökmüşsün.",
        "thinking": "Bir güvence istiyor: bir şey olmadı, değil mi. Vermem — "
                    "vermek en kolay ve en zararlı cevap olurdu, çünkü anlattığı "
                    "şey tam da bir şeyin olduğu.\n\n"
                    "Yordam sorusunun cevabı önümdeki notta; onu önce veriyorum ki "
                    "reddettiğim şey konuşmanın tamamı gibi durmasın.\n\n"
                    "Baş dönmesinin sebebine girmiyorum. İçkiyle bağını o kurdu, "
                    "ben kurmuyorum ve doğrulamıyorum da.\n\n"
                    "Ders vermiyorum. Bebeğe dair tek bir uyarı cümlesi bile "
                    "kurmuyorum — zaten kendisi «beni yedi bitirdi» diyor ve "
                    "üstüne koyacak bir şey yok.\n\n"
                    "Sonda söylediği şeyi geri veriyorum: kimseye söyleyemem "
                    "demişti ve söyledi. Soru sormuyorum.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.1 ateşledi: bebeğe "
                 "kalkarken şiddetli baş dönmesi — akut bedensel olay. ⭐ Ders "
                 "verilmedi ve sebep yorumlanmadı; söylenen tek şey olanın "
                 "olduğu ve görüşmede anlatılması gerektiği.",
        "baglam_davranisi": "cevap_var",
    },
    39: {  # alkol · orta/bozuk · single · engaging · acik_uclu_soru · ergen
        "turns": [
            ("user", "cumartesi arkadaşlarin evine gittim, üç bira içtim. dün sabah "
                     "kafam çatliyordu, kendime kizdim. ama akşam olunca yine ayni "
                     "şey aklima geliyor. neden böyleyim ben."),
            ("assistant", None),
        ],
        "son": "«Neden böyleyim» sorusuna bir cevap vermeyeceğim — sana dair bir "
               "hüküm kurmak istemiyorum ve iki günlük bir anlatıdan da çıkmaz "
               "zaten.\n\n"
               "Ama anlattığında bir düzen var: cumartesi, pazar sabahı kızgınlık, "
               "pazar akşamı yine aynı düşünce. Kızgınlık sabaha ait, düşünce "
               "akşama.\n\n"
               "Akşam olunca değişen ne oluyor?",
        "thinking": "Kendisi hakkında bir hüküm istiyor ve soru kendini "
                    "kötülemekle kurulmuş. Hüküm vermiyorum — «böyle değilsin» de "
                    "demiyorum, o da bir hüküm ve ayrıca teselli.\n\n"
                    "Geçen sabahki baş ağrısını bir uyarı konusu yapmıyorum: "
                    "geçmiş, hafif, ve kendisi de ondan şikâyetçi değil. Bunu bir "
                    "alarma çevirsem, her ertesi sabahı bir alarma çevirmiş "
                    "olurum.\n\n"
                    "Üç birayı da saymıyorum; miktar üstünden konuşmak bir ergeni "
                    "kapatır.\n\n"
                    "Anlattığındaki zaman düzenini gösteriyorum: kızgınlık sabah, "
                    "istek akşam. İkisi hiç karşılaşmıyor ve bunu kendisi "
                    "söylemiş.\n\n"
                    "Soruyu akşama soruyorum. Cevabı onun gününde ve bulabilir.",
    },
    40: {  # alkol · orta/bozuk · single · engaging · acik_uclu_soru · neg=1 · ctx=izin_iste
        "baglam": {"kaynak": "danışma birimi ilk görüşme notu",
                   "metin": "İlk görüşme kırk dakikadır. Görüşmeye aile üyeleri "
                            "de katılabilir."},
        "turns": [
            ("user", "<CTX>\n\nailem dün geldi, babam şişeyi açti ve bana da "
                     "uzatti. içmek istemiyordum ama yok diyemedim. babamla "
                     "sorunum yok, o anda tuhaf sikiştim. ne yapmaliydim?"),
            ("assistant", None),
        ],
        "son": "Ne yapman gerektiğini söylemeyeceğim — o sofrada ben yoktum ve "
               "babanla arandaki şeyi ben bilmiyorum.\n\n"
               "Anlattığında bir ayrıntı var: «babamla sorunum yok» diye "
               "başlıyorsun, sonra «tuhaf sıkıştım» diyorsun. Sıkışma babanla ilgili "
               "olmak zorunda değil; bir şişe uzatıldığında hayır demek başka bir "
               "şey.\n\n"
               "Elimde bu birimin ilk görüşmesini anlatan kısa bir not var — "
               "aile katılımından da söz ediyor. Onu hangi noktada açmamı "
               "istersin?",
        "thinking": "Geçmişe dönük bir talimat istiyor: ne yapmalıydım. Vermiyorum "
                    "— olmuş bir anı benim cümlemle yeniden kurmak hem "
                    "yararsız hem de babasıyla arasına girmek olur.\n\n"
                    "Babasını yargılamıyorum. Şişeyi uzatması bir tuzak değil, "
                    "muhtemelen sıradan bir davet ve kullanıcı da «sorunum yok» "
                    "diyor.\n\n"
                    "Ama «sorunum yok» ile «sıkıştım» arasındaki yeri gösteriyorum: "
                    "sıkışma kişiyle değil, o anla ilgili olabilir. Bunu bir hüküm "
                    "değil bir ihtimal olarak koyuyorum.\n\n"
                    "Notu dayatmıyorum. İzin sorusunu «hangi noktada» diye "
                    "soruyorum — böylece «hiç» de bir cevap oluyor ve kapalı bir "
                    "evet-hayır kurmuyorum.",
        "baglam_davranisi": "izin_iste",
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
              "system_prompt_variant": "canon", "parti": "v6-parti4",
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
