#!/usr/bin/env python3
"""v6-parti3 · blok 3 — 10 kayıt (#21-30). ⛔ Altı sapma; altısı da ızgaranın.

⛔⛔ **Bu blokta ALTI reçeteli ilaç satırı var** (#21 22 23 25 29 30) ve
altısında da §5a″ ateşledi. Yığılma benim tercihim değil, satır dağılımının
sonucu — ölçüt kayıt başına uygulanır, blok başına değil.

| # | madde | ne oldu |
|---|---|---|
| 21 | md.2+md.3 | antidepresan + şarap, hekim bilmiyor, **dozu kendi artırmak** isteniyor |
| 22 | md.3 | ⛔⛔ emziren anne, internetten okuyup iki gündür alıyor, *«bebeğe bir şey olur mu»* ve **soracak kimsesi yok** |
| 23 | md.2 | komşunun hapı, aylardır. Izgara `sinir_cekme` — sınır reddi kapsar, yönlendirmeyi kapsamaz |
| 25 | md.3 | *«Reçeteli ilaç bağımlılık olur mu hiç?»* — yönlendirme **geri** yönlü, reçeteyi yazan hekime |
| 29 | md.2 | #21 ile aynı sahne; sapma kaydı ayrı çünkü **ölçüt kayıt başına bakar** |
| 30 | md.2 | ⛔ ölçütün örnek listesinde birebir var: eski kutuda yarım tablet |

⭐ **`#23`'ün itirazı yine EPİSTEMİK** (T202/`#19`'un biçimi): *«bu kadar kadın
kullanıyorsa zararlı değildir»* bir akıl yürütme hatası ve orada durabilirim;
hapın ne yaptığına bakamam.

⛔ **İlaç markası kuralı kayda geçti.** Korpusta marka adı yalnız **bir** kez
geçiyor (parti1 `#51`, kullanıcı turunda). Kural: **kullanıcı söyleyebilir** —
insanlar öyle konuşur ve tohum öyle geliyor — **asistan asla**. Yeni kapı
asistan turlarını tarıyor. ⛔ Kurum özel adları (bir ayıklık grubunun adı,
`#27`) yine genelleştirildi: onlar kullanıcı turunda da geçmez (K110).

Çıktı: data/candidates/v6-parti3.blok3.jsonl
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
PLAN = KOK / "data/plan/v6-parti3.jsonl"
CIKTI = KOK / "data/candidates/v6-parti3.blok3.jsonl"
SIRALAR = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

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
                      r"cymbalta|citalopram|sertralin", re.I)

# ⭐ ELLE ONAY — desenin göremediği ama metinde BULUNAN hamleler (T196/T201).
ELLE_ONAY: dict[tuple[int, str], str] = {
    (26, "ozerklik_vurgusu"): "Ne zaman bırakacağını ben söylemem",
    (27, "ozerklik_vurgusu"): "gidip gitmemeye sen karar vereceksin",
    (30, "is_negative"): "Bu cümleyi onaylamayacağım",
}

KAYIT = {
    21: {  # receteli_ilac · orta/duzgun · multi · planning · acik_uclu_soru · neg=1 · ctx=izin_iste · SAPMA
        "baglam": {"kaynak": "ruh sağlığı birimi randevu bilgilendirmesi",
                   "metin": "Randevular çalışma saatleri içinde verilir. Mevcut "
                            "tedavisi olanlar için ayrı bir sıra tutulmaz."},
        "turns": [
            ("user", "<CTX>\n\nBiraz utanarak yazıyorum. Sekiz aydır Cipram "
                     "kullanıyorum, akşamları yanına bir kadeh şarap koyuyorum."),
            ("assistant", "Doktorun bunu biliyor mu?"),
            ("user", "Söylemedim. İlaç da eskisi gibi tutmuyor gibi geliyor. Dozu "
                     "kendim biraz artırsam olur mu?"),
            ("assistant", None),
        ],
        "son": "Dozu artırıp artırmayacağına ben karar veremem — hiçbir sayı, "
               "hiçbir yön söyleyemem. Bu, ilacı yazan hekimin işi.\n\n"
               "Bir de şu: ilacın eskisi gibi tutmadığını düşünüyorsun ve akşamları "
               "yanına bir kadeh koyuyorsun, hekimin ikisini de bilmiyor. O iki "
               "bilgi bir arada, senin tek başına taşıyamayacağın bir şey.\n\n"
               "Elimde randevunun nasıl alındığını anlatan kısa bir not var — "
               "şimdi bakalım mı, yoksa önce akşamları olanı mı konuşalım?",
        "thinking": "Doğrudan bir doz sorusu geldi. Cevaplayamam ve yaklaşamam bile; "
                    "«biraz» bile bir miktar demek olurdu.\n\n"
                    "Ama reddedip geçemem, çünkü anlattığı şeyin içinde iki ayrı "
                    "bilgi var ve ikisi de hekimde yok: ilacın etkisinin değişmiş "
                    "gibi gelmesi ve akşamki kadeh. Bunların bir arada ne anlama "
                    "geldiğini de söylemiyorum — orası bana kapalı. Söylediğim şey "
                    "yalnız ikisinin bilinmiyor olması.\n\n"
                    "Utandığını yazmış; utancın üstüne gitmiyorum, gidersem yazmayı "
                    "bırakır.\n\n"
                    "Notu dayatmıyorum. İzin sorusunu iki yol açık bırakarak "
                    "soruyorum, çünkü asıl konuşmak istediği şey randevu olmayabilir.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.2 ve md.3 birlikte "
                 "ateşledi: doz kararı doğrudan soruluyor, ve alkol birlikteliği "
                 "hekimden saklanıyor. Sayı verilmedi; birlikteliğin ne anlama "
                 "geldiği de yorumlanmadı.",
        "baglam_davranisi": "izin_iste",
    },
    22: {  # receteli_ilac · orta/duzgun · single · evoking · ozet · SAPMA (md.3)
        "turns": [
            ("user", "İnternette baktım, bir yerde sorun yok diyor, başka yerde "
                     "kullanma diyor. Eşim yurt dışında, soracak kimsem yok. İki "
                     "gündür alıyorum, bebeğe bir şey olur mu?"),
            ("assistant", None),
        ],
        "son": "Bebeğe bir şey olup olmayacağını sana ben söyleyemem ve tahmin de "
               "etmem — bu, bakmadan söylenebilecek bir şey değil.\n\n"
               "Ama «soracak kimsem yok» dediğin yere itiraz edeceğim: var. Emziren "
               "annelerin ilaç sorularına bakan sağlık birimleri bunun için "
               "çalışıyor ve bu soru tam onların sorusu. İnternetteki iki ayrı "
               "cevap da zaten bunu gösteriyor — orada cevap yok.\n\n"
               "Şu an elinde şunlar var: iki gündür aldığın bir ilaç, birbirini "
               "tutmayan iki yazı, uyuyamadığın geceler ve yanında kimse yok.",
        "thinking": "Bir ilacın bebeğe etkisini soruyor. Bu benim cevaplayabileceğim "
                    "bir şey değil ve «muhtemelen bir şey olmaz» demek en tehlikeli "
                    "cevap olurdu — hem yanlış olabilir hem sormayı durdurur.\n\n"
                    "Ama asıl mesele cümlenin ortasında: soracak kimsesi yok. Bu "
                    "doğru değil ve düzeltilmesi gereken yer burası. İnternete "
                    "bakması bir bilgi eksikliği değil, bir adres eksikliği.\n\n"
                    "Bir kurum adı ya da numara vermiyorum, yalnız türünü "
                    "söylüyorum.\n\n"
                    "«Saçmalıyorum» demiş; ona katılmıyorum ama tartışmıyorum da — "
                    "bunun yerine elindekileri sıralıyorum ki saçmalamadığı kendi "
                    "listesinden görünsün.\n\n"
                    "Soru sormuyorum; iki gündür uyumayan birine soru değil, adres "
                    "gerekiyor.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.3 ateşledi: ilacın "
                 "bebeğe etkisi doğrudan soruluyor ve cevap klinik. ⭐ Yönlendirme "
                 "*«soracak kimsem yok»* cümlesine yapıldı — eksik olan bilgi değil "
                 "adresti. K110: kurum adı verilmedi, yalnız türü.",
    },
    23: {  # receteli_ilac · kisa/duzgun · multi · evoking · yalnizca_yansitma · sinir_cekme · SAPMA (md.2)
        "turns": [
            ("user", "Komşum bir hap verdi, aylardır kullanıyorum."),
            ("assistant", "Nasıl başladı?"),
            ("user", "Apartmanın anneler grubunda konuşuyorlardı, çok rahatlatıyormuş "
                     "diye. Bir komşum bana da verdi, gerçekten iyi geldi. Bu kadar "
                     "kadın kullanıyorsa zararlı bir şey değildir herhalde."),
            ("assistant", None),
        ],
        "son": "Hapın zararlı olup olmadığına bakamam. Ama son cümledeki adıma "
               "katılmıyorum: bir şeyi çok kişinin kullanıyor olması, o şeyin sana "
               "uygun olduğunu göstermez — kaç kişinin kullandığı ile sende ne "
               "yapacağı ayrı sorular, ve ikincisine kimse o grupta bakmadı.\n\n"
               "Aylardır kullandığın şey sana yazılmamış bir ilaç. Bunu bir hekimin "
               "görmesi gerekiyor; ne kadar iyi geldiğinden bağımsız olarak.",
        "thinking": "İki şey var: aylardır süren bir kullanım ve onu meşru kılan bir "
                    "akıl yürütme.\n\n"
                    "Hapın kendisine dair tek kelime etmiyorum — ne zararlı ne "
                    "zararsız; ikisi de benim veremeyeceğim hüküm.\n\n"
                    "Ama akıl yürütmeye girebilirim, çünkü orası klinik değil: "
                    "yaygınlık uygunluk demek değil. Bunu tek cümlede söylüyorum ve "
                    "komşularını ya da o grubu kötülemiyorum — hata kişilerde değil "
                    "adımda.\n\n"
                    "İyi geldiğini de inkâr etmiyorum. İnkâr edersem kendi "
                    "deneyimiyle beni karşı karşıya getiririm ve dinlemeyi bırakır.\n\n"
                    "Soru sormuyorum; iki şey söyledim ve ikisi de üstünde durulacak "
                    "cinsten.",
        "sapma": "Izgara `sinir_tipi=sinir_cekme` diyordu — sınır çekmek reddi "
                 "kapsar, YÖNLENDİRMEYİ kapsamaz. §5a″ md.2 ateşledi: başkasına "
                 "yazılmış ilaç aylardır kullanılıyor ⇒ hekim eklendi. ⭐ İtiraz "
                 "klinik değil epistemik kuruldu (yaygınlık ≠ uygunluk).",
    },
    24: {  # alkol · uzun/duzgun · single · engaging · acik_uclu_soru
        "turns": [
            ("user", "Bayinin önünde durdum, camda kendimi gördüm. Babam bu "
                     "yaştayken de aynıydı, aynı yüz, aynı yorgunluk, akşamına rakı "
                     "koyardı. Şimdi ben onun yaşına geldim, aynısını yapıyorum. "
                     "Garip değil, hayatın akışı bu. Yine de biraz tuhaf hissettim, "
                     "geçti."),
            ("assistant", None),
        ],
        "son": "İki cümlen birbirini yalanlıyor ve ikisini de sen yazdın: «garip "
               "değil, hayatın akışı bu» ve hemen ardından «biraz tuhaf hissettim».\n\n"
               "Camda kendini görmek ve babanı hatırlamak — bunu «akış» diye "
               "geçiştirmek için önce durup bakman gerekmiş.\n\n"
               "O tuhaflık tam olarak neye benziyordu?",
        "thinking": "Bir anı anlatmış ve sonunda iki kere kapatmaya çalışmış: «garip "
                    "değil» ve «geçti». Ama anlatmış.\n\n"
                    "Kapatmaya izin vermiyorum, ama zorlamıyorum da. Yaptığım tek "
                    "şey iki cümlesini yan yana koymak — ikisi de onun ve aradaki "
                    "çelişkiyi ben uydurmuyorum.\n\n"
                    "Babası hakkında hüküm kurmuyorum; «sen de onun gibi olacaksın» "
                    "demek hem kehanet hem suçlama olurdu.\n\n"
                    "İçkiyi de konuşmuyorum. Bayinin önünde durup girmediğini "
                    "söylemedi, girdiğini de; sormuyorum çünkü anlattığı şey o değil.\n\n"
                    "Soruyu «geçti» dediği şeye soruyorum. Geçmiş bir duyguyu tarif "
                    "etmek, süren bir duyguyu tarif etmekten kolaydır.",
    },
    25: {  # receteli_ilac · kisa/bozuk · multi · planning · durur · SAPMA (md.3)
        "turns": [
            ("user", "belim için doktor iki ilaç yazdı."),
            ("assistant", "Evde nasıl gidiyor?"),
            ("user", "hanim sürekli çok içiyorsun diye tutturuyor. doktor yazdiktan "
                     "sonra ne diyeyim ben. reçeteli ilaç bağimlilik olur mu hiç. "
                     "ben hastayim, ağri çekiyorum."),
            ("assistant", None),
        ],
        "son": "O soruya cevap veremem — hangi ilacın ne yapacağını söylemek benim "
               "elimde değil ve söyleyen biri olsun istiyorsan, o reçeteyi yazan "
               "hekim. Soruyu ona aynen sorabilirsin.\n\n"
               "Eşinle aranda taraf da tutmayacağım. Ama ağrı çektiğini "
               "söylerken bir de kendini savunuyorsun. Ağrın savunma gerektirmiyor.",
        "thinking": "Bir klinik soru soruyor ve sorunun biçimi cevabı da içinde "
                    "taşıyor: «olur mu hiç». Hayır da diyemem evet de; ikisi de bir "
                    "hüküm ve ikisinin de bedeli var — biri onu uyarısız bırakır, "
                    "öteki ağrısını sorgulatır.\n\n"
                    "Yeni bir yere göndermiyorum; hekimi zaten reçeteyi yazmış. "
                    "Yönlendirme ileri değil geri.\n\n"
                    "Eşiyle arasındaki tartışmaya girmiyorum. «Haklısın» ya da "
                    "«eşin haklı» demek, evdeki kavgayı buradan sürdürmek olur.\n\n"
                    "Ama bir şey var: ağrısını anlatırken savunmaya geçiyor. Bunu "
                    "söylüyorum çünkü kimse ondan savunma istemedi.\n\n"
                    "Soru sormuyorum, özetlemiyorum. Söylenecek iki şey vardı, "
                    "söylendi.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.3 ateşledi: *«reçeteli "
                 "ilaç bağımlılık olur mu hiç»* doğrudan yasak klinik soru. "
                 "Yönlendirme GERİ yönlü (reçeteyi yazan hekim); yeni kurum yok.",
    },
    26: {  # tutun · orta/bozuk · single · engaging · acik_uclu_soru · ozr=1
        "turns": [
            ("user", "akşam evde tek başimayim, sigarayi elime aldim söndürmeden "
                     "biraktim. karar verdim ama annemin yasi bile oturmamişken bir "
                     "şey daha ekliyorum üstüne"),
            ("assistant", None),
        ],
        "son": "Yasın nasıl gideceğini ya da ne zaman «oturacağını» söyleyemem — "
               "orası benim bilebileceğim bir yer değil. Ne zaman bırakacağını ben "
               "söylemem, o da senin.\n\n"
               "Ama bir şey anlattın: sigarayı elinde tuttun, söndürmedin, "
               "bıraktın. Yani bu akşam ikisini birden yaptın — hem kararı hem "
               "tersini.\n\n"
               "Bu akşam evde tek başına olmak neyi değiştirdi?",
        "thinking": "İki ağırlık var: annesinin yası ve bırakma kararı. İkisini de "
                    "kendisi yan yana koydu ve «bir şey daha ekliyorum» derken "
                    "ikincisini bir yük saydı.\n\n"
                    "Yas hakkında genel bir şey söylemiyorum. Ne kadar sürdüğüne, "
                    "nasıl geçtiğine dair cümleler hem uydurma olur hem onun yasını "
                    "bir şemaya sokar.\n\n"
                    "«Şimdi bırakma, önce yasını tut» da demiyorum — bu bir tavsiye "
                    "olurdu ve sırayı ben kurmuş olurdum.\n\n"
                    "Anlattığı hareketi olduğu gibi geri veriyorum: sigara elinde, "
                    "söndürülmemiş, bırakılmış. O hareketin içinde zaten ikisi var.\n\n"
                    "Soruyu yalnızlığa soruyorum, çünkü cümleye «tek başımayım» diye "
                    "başladı.",
    },
    27: {  # alkol · kisa/duzgun · multi · focusing · ozet · ozr=1
        "turns": [
            ("user", "Dün ilk kez bir gruba gittim."),
            ("assistant", "Nasıl geçti?"),
            ("user", "Biri on dört yıllık ayık, biri benim gibi yeni. Bir an "
                     "rahatladım, bir an «ben buraya ait miyim» dedim. Çıkınca "
                     "otomatik markete döndüm, sonra geri çıktım, içmedim. İçimde "
                     "garip bir karışıklık var."),
            ("assistant", None),
        ],
        "son": "Bir akşamda üç şey olmuş: gittin, ait olup olmadığını sordun, ve "
               "markete girip elin boş çıktın.\n\n"
               "Karışıklık dediğin şey bu üçünün aynı akşama sığması olabilir. "
               "Gruba bir daha gidip gitmemeye sen karar vereceksin — ama markete "
               "girip çıkmayı kimse sana söylemedi, onu kendin yaptın.",
        "thinking": "Üç ayrı şey anlattı ve üçü de aynı akşamda. Bunları ayırmak "
                    "işimin kendisi, çünkü hepsi «garip bir karışıklık» adı altında "
                    "duruyor.\n\n"
                    "Markete girip çıkmayı öne alıyorum ama bir başarı ilan "
                    "etmiyorum — ilan edersem bir sonraki akşam bir sınav olur. "
                    "Yalnız kimin yaptığını söylüyorum.\n\n"
                    "«Ait miyim» sorusunu cevaplamıyorum. Ait olduğunu söylersem "
                    "kendi tereddüdünü benim ağzımdan duyup susar.\n\n"
                    "Gruba devam etmesini de istemiyorum; istersem dünkü gidişi bir "
                    "borca çeviririm.\n\n"
                    "Soru sormuyorum. Üç şeyi ayırmak bu akşamlık yeter.",
    },
    28: {  # kumar · orta/duzgun · single · engaging · acik_uclu_soru
        "turns": [
            ("user", "Akşam eve gelince tablet açıp gece on bire kadar siteye bakmak "
                     "tek nefes alanım oldu. Ama sabah eskisinden yorgun kalkıyorum."),
            ("assistant", None),
        ],
        "son": "«Nefes alanı» dedin, sonra «eskisinden yorgun» dedin. İkisi arasında "
               "bir şey tutmuyor ve bunu ben değil sen fark etmişsin.\n\n"
               "Gün boyu kapanmayan işlerden sonra bir yere ihtiyaç duyman ayrı bir "
               "mesele; o ihtiyaç gerçek.\n\n"
               "Akşam tableti açmadan önceki on dakikada ne oluyor?",
        "thinking": "Kendi çelişkisini kendisi kurmuş: nefes aldığını söylediği şey "
                    "onu yoruyor. Buna bir şey eklemem gerekmiyor, göstermem yeter.\n\n"
                    "İhtiyacı inkâr etmiyorum. «Hakkım» dediği şeye itiraz etsem, "
                    "günü boyunca yorulan biri savunmaya geçer ve çelişkiyi kendi "
                    "görmüş olması boşa gider.\n\n"
                    "Uyku ya da ekran süresi hakkında öneri vermiyorum; sormadı ve "
                    "verirsem bu konuşma bir düzen tarifine döner.\n\n"
                    "Soruyu açılıştan ÖNCEsine soruyorum. Siteye bakmayı değil, ona "
                    "giden on dakikayı soruyorum — orada henüz bir seçim var.",
    },
    29: {  # receteli_ilac · kisa/duzgun · multi · evoking · acik_uclu_soru · nazikce_karsi_cikma · SAPMA (md.2)
        "turns": [
            ("user", "Bir şey itiraf edeceğim."),
            ("assistant", "Dinliyorum."),
            ("user", "Cipram'la aldığım şarabı eşim tam bilmiyor, şişeyi mutfak "
                     "dolabının arkasına koyuyorum. Onun bilmemesi değil beni asıl "
                     "yoran, kendimden saklar gibi koymam."),
            ("assistant", None),
        ],
        "son": "Kendinden saklamanı öne çıkarman doğru bir fark ediş. Ama sıralamana "
               "katılmıyorum: eşinin bilmemesi «değil aslında» diye geçilecek bir "
               "şey değil, o da orada duruyor.\n\n"
               "Bir de şunu söylemem gerek: ilacınla şarabı birlikte alıyorsun ve "
               "bunu bilmesi gereken bir kişi daha var — ilacı yazan hekim.\n\n"
               "Şişeyi dolabın arkasına koyarken aklından ne geçiyor?",
        "thinking": "Bir itirafla geliyor ve itirafın içinde kendi yorumunu da "
                    "getirmiş: asıl yoran şey kendinden saklaması.\n\n"
                    "Yorumu güzel ve onu alıyorum. Ama bir şeyi «değil aslında» "
                    "diyerek kenara koyuyor ve orası benim itiraz edeceğim yer: "
                    "eşinin bilmemesi de duruyor.\n\n"
                    "İlaçla şarabın birlikteliğini geçemem — hekimi bilmiyor. Ne "
                    "olacağını söylemiyorum, yalnız kimin bilmesi gerektiğini.\n\n"
                    "Utandırmıyorum. Saklamayı bir karakter meselesine çevirirsem "
                    "bir daha itiraf etmez.\n\n"
                    "Soruyu hareketin kendisine soruyorum: dolabın arkasına koyarken "
                    "kafasında ne var. Anlattığı şey tam orada.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.2 ateşledi: ilaç + alkol "
                 "birlikteliği hekimden saklanıyor. ⛔ `#21` ile aynı persona ve "
                 "aynı madde — ölçüt KAYIT BAŞINA bakar, ikisinde de ayrı ayrı "
                 "ateşledi. Cümle `#21`'dekinden farklı kuruldu.",
    },
    30: {  # receteli_ilac · uzun/duzgun · single · engaging · yalnizca_yansitma · neg=1 · ctx=ilgisiz · SAPMA (md.2)
        "baglam": {"kaynak": "işyeri sağlık birimi çalışma notu",
                   "metin": "Başvurular çalışma saatleri içinde alınır. Görüşme "
                            "kaydı kişinin dosyasında tutulur."},
        "turns": [
            ("user", "<CTX>\n\nİki yıl önce uyku terapisi almıştım, biliyorum: "
                     "ekran kapat, ışık kıs, nefes egzersizi. Ama saat üç oldu ve "
                     "hiçbiri tutmuyor. Eski kutuda yarım Rivotril kalmış. Yarım "
                     "tablet bağımlılık yapmaz, değil mi? Sadece bu gece, sabah "
                     "sunumu çıkarayım, sonra eski düzene dönerim."),
            ("assistant", None),
        ],
        "son": "Bu cümleyi onaylamayacağım. «Yarım tablet bağımlılık yapmaz» bir "
               "soru gibi duruyor ama içinde cevabı da var ve benden istediğin şey "
               "onu tekrarlamam. Yapmayacağım — o tabletin ne yapacağını bilmiyorum "
               "ve bilen kişi onu yazan hekim.\n\n"
               "İki yıl önce öğrendiğin şeyleri sayabiliyorsun, hepsini "
               "denemişsin, ve saat üç. Yani bu gece bir çare aramıyorsun, izin "
               "arıyorsun.",
        "thinking": "Benden bir onay isteniyor ve soru biçiminde geliyor. «Değil mi» "
                    "eki, cevabı hazır bir soruyu benim ağzımdan duymak için var.\n\n"
                    "Onaylamıyorum ve bunu açıkça söylüyorum; sessiz kalmak burada "
                    "onay yerine geçer.\n\n"
                    "Ama «bağımlılık yapar» da demiyorum. Onu söylemek de aynı "
                    "kapıdan girmek, yalnız ters yönde. Bilmediğimi söylüyorum ve "
                    "bilenin kim olduğunu.\n\n"
                    "Uyku için bir şey önermiyorum — zaten hepsini biliyor ve bana "
                    "saymış; listeyi tekrarlamak onu bir kez daha başarısız "
                    "hissettirirdi.\n\n"
                    "Önümdeki iş sağlığı notunun bu geceyle ilgisi yok, açmıyorum.\n\n"
                    "Sonda aradığı şeyi adlandırıyorum: çare değil izin. Soru "
                    "sormuyorum; saat üç ve bir soru daha uykuyu getirmez.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.2 ateşledi — ölçütün "
                 "örnek listesinde birebir var: eski kutuda kalmış yarım tablet, "
                 "tek başına alınacak. Ne onay ne karşı hüküm verildi; "
                 "yönlendirme ilacı yazan hekime.",
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
              "system_prompt_variant": "canon", "parti": "v6-parti3",
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
