#!/usr/bin/env python3
"""v6-parti3 · blok 2 — 10 kayıt (#11-20). Partinin en sert bloğu.

⛔⛔⛔ **`#17` — alkol azaltırken gece yarısı ter ve çarpıntı.** *«Bu sadece
psikolojik mi yoksa bedenim bir şey mi söylüyor?»* §5a″ md.1 (akut bedensel
olay) **ve** md.3 (doğrudan yasak klinik soru) birlikte ateşledi. Izgara
`sinir_tipi=sinir_cekme` diyordu — sınır çekmek reddi kapsar ama
**yönlendirmeyi kapsamaz**. ⇒ Sapıldı. Soruya cevap verilmedi; söylenen tek
şey bunun bugün bakılması gerektiği. K18/K110: numara ve kurum adı yok.

⛔⛔ **`#19` — bir blog «doktora gitmem gerekmez» diyor.** İtiraz **klinik
değil epistemik** kuruldu: blogun söylediğinin doğru olup olmadığına
bakamam, katılmadığım yer bir blogun hekimin yerine konması.

⚠️ `#12` §5a″ md.2 + md.3 — başkasının hapı, ve *«çok mu sık alıyorum»*.

⭐ **`#15`'te SAPILMADI ve sebebi yazılı:** md.1 ve md.3 ateşliyor (bir buçuk
doz + nefes, ve *«nereden başlayayım»*) ama ızgara **zaten**
`yonlendirme_istegi` diyor ⇒ sapma gerekmedi (parti1 `#23`'ün aynı gerekçesi).

⛔ **Üç çift aynı sahneyi taşıyor ve bilerek ayrıldı:**
· `#9`↔`#12` kayınvalidenin hapı — `#12`'de kuşku KULLANICININ ve açık, o
  yüzden cevap onun sorusuna yaslanıyor, yeni bir endişe eklemiyor.
· `#18`↔`#20` tombalaya giden para — `#18` sorguluyor (evoking + soru),
  `#20` itiraz ediyor (yansıtma + eşitliğe karşı çıkma).
· `#1`↔`#20` ikisi de *«Yanlış mı yapıyorum bilmiyorum»* ile bitiyor —
  `#1`'de hüküm vermeyi reddettim, `#20`'de itiraz ettim. ⭐ Fark ızgaradan
  geliyor: `#20`'nin hedefi `nazikce_karsi_cikma`.

⭐ **`#16` `izin_iste`** — korpusun kalıbı (*«Elimde … var. Bunu sormadın, ama
işine yarayabilir. Paylaşmamı ister misin?»*) 14 kaydın en az ikisinde birebir
aynı. Kullanılmadı; izin sorusu açık uçlu kuruldu.

Çıktı: data/candidates/v6-parti3.blok2.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti3.blok2.jsonl"
SIRALAR = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

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

# ⭐ ELLE ONAY — desenin göremediği ama metinde BULUNAN hamleler (T196/T201).
ELLE_ONAY: dict[tuple[int, str], str] = {
    (11, "ozerklik_vurgusu"): "gece üçte orada olan sensin",
    (16, "ozerklik_vurgusu"): "akşamını ben düzenleyecek değilim",
    (17, "ozerklik_vurgusu"): "Gidip gitmemek senin elinde",
}

KAYIT = {
    11: {  # kumar · kisa/duzgun · multi · focusing · acik_uclu_soru · rol_siniri_yonlendirme · ozr=1
        "turns": [
            ("user", "Gündüz açmayacağım diyorum, gece üçte açıyorum."),
            ("assistant", "Arada ne oluyor?"),
            ("user", "Bebeği emzirip yatağa dönüyorum, elim telefona kayıyor. Sabah "
                     "aynaya bakıp «yine yaptım» diyorum. İki kararım birbirine "
                     "uymuyor, en çok o yoruyor."),
            ("assistant", None),
        ],
        "son": "İki kararın da senin ve ikisi farklı saatlerde veriliyor — biri "
               "gündüz masabaşında, öteki gece üçte tek başına. Ben ikisinden "
               "hiçbirini veremem; gece üçte orada olan sensin.\n\n"
               "Yeni ebeveynlerin gece düzeniyle çalışan danışma birimleri var ve "
               "bu tam onların baktığı şey.\n\n"
               "Elin telefona kayarken aklından bir şey geçiyor mu, yoksa sessiz mi?",
        "thinking": "Bir çelişki anlatıyor ve çelişkiyi kendisi adlandırmış: iki "
                    "karar birbirine uymuyor.\n\n"
                    "Kararı ben veremem ve bunu söylüyorum. Ama gündüzkü kararı "
                    "«doğru», gecekini «yanlış» diye ayırmıyorum — ikisi de onun ve "
                    "ayırırsam sabahki utancı büyütürüm.\n\n"
                    "Bir yere gönderiyorum, çünkü gece üçte tek başına bir "
                    "uygulamayla kalan biri için burada konuşmak yetmez. Yeri "
                    "türüyle söylüyorum, adıyla değil.\n\n"
                    "Soruyu tam o ana daraltıyorum: elin kayarken kafanın içinde ne "
                    "var. Sessizlik de bir cevap ve onu da açık bırakıyorum.",
    },
    12: {  # receteli_ilac · orta/duzgun · single · planning · acik_uclu_soru · SAPMA (md.2+md.3)
        "turns": [
            ("user", "Kayınvalidemle aynı evde yaşıyoruz, bazı akşamlar onun verdiği "
                     "hapı alıp yatıyorum. Çok mu sık alıyorum acaba?"),
            ("assistant", None),
        ],
        "son": "Sıklık sorusuna ben cevap veremem — «şu kadar çok, bu kadar az» "
               "demek bir hekimin işi, hele ilaç senin adına yazılmamışken.\n\n"
               "Ama soruyu sen sordun ve bir yerden çıktı. «Acaba» dediğine göre "
               "bir şey seni saymaya başlatmış.\n\n"
               "Bu soru ilk ne zaman aklına geldi?",
        "thinking": "Doğrudan bir sıklık sorusu sordu. Cevaplayamam; bir sayı ya da "
                    "bir ölçü vermek, olmadığım bir yerden hüküm kurmak olur.\n\n"
                    "İlacın kendisine yazılmadığını da geçemem. Ama bunu bir suçlama "
                    "gibi kurmuyorum; yalnız reddin sebebini açıklarken söylüyorum, "
                    "çünkü sebebin bir parçası bu.\n\n"
                    "İlacın ne yaptığına, ne kadar sürede alışıldığına, hiçbirine "
                    "girmiyorum.\n\n"
                    "Asıl şey şu: bu soruyu kimse ona sormadı, kendi sordu. Bir "
                    "sayma başlamış ve başlatan bir şey var.\n\n"
                    "Soruyu oraya soruyorum — sıklığa değil, sorunun kendisine.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.2 **ve** md.3 birlikte "
                 "ateşledi: başkasına yazılmış ilaç düzenli alınıyor, ve sıklığı "
                 "doğrudan soruluyor. Sayı verilmedi, klinik içerik verilmedi.",
    },
    13: {  # tutun · orta/duzgun · single · engaging · acik_uclu_soru · ctx=cevap_yok · nazikce_karsi_cikma
        "baglam": {"kaynak": "bırakma destek birimi başvuru notu",
                   "metin": "Başvurudan önce kısa bir ön görüşme yapılır. Ön "
                            "görüşme telefonla da olabilir."},
        "turns": [
            ("user", "<CTX>\n\nBabam sekiz yıl önce bıraktı. Dün dumana baktı, "
                     "hiçbir şey demedi. O bakış konuşmasından beter. Görüşmeye "
                     "babamla gitsem olur mu?"),
            ("assistant", None),
        ],
        "son": "Yanında birinin gelip gelemeyeceği bu notta geçmiyor; ön görüşmeden "
               "başka bir şey yazmıyor, o yüzden bilmiyorum — ön görüşmede "
               "sorabilirsin.\n\n"
               "Bir de şuna katılmıyorum: o bakışın konuşmasından beter olduğunu "
               "sen koydun. Baban hiçbir şey demedi; demediği şeyin ne olduğunu ne "
               "sen biliyorsun ne ben.\n\n"
               "Babanla gitmek aklına nasıl geldi?",
        "thinking": "Bir yordam sorusu var, cevabı önümdeki notta yok; uydurmuyorum "
                    "ve sorabileceği yeri söylüyorum.\n\n"
                    "Asıl mesele bakış. Sessiz bir bakışı bir hükme çevirmiş ve o "
                    "hükmü kendi aleyhine kurmuş. Buna katılmıyorum — ama babasının "
                    "ne düşündüğünü de söylemiyorum, çünkü onu ben de bilmiyorum. "
                    "İtirazım adımın kendisine: demedikten bir anlam çıkarmaya.\n\n"
                    "İlk sigarayı babasının paketinden aldığını da açmıyorum; bugünün "
                    "meselesi değil ve açarsam eski bir suçu masaya koyarım.\n\n"
                    "Soruyu onun kendi teklifine soruyorum: babasıyla gitmek fikri "
                    "nereden geldi. Orada bir şey var ve o söylemedi.",
        "baglam_davranisi": "cevap_yok",
    },
    14: {  # receteli_ilac · kisa/duzgun · multi · engaging · yalnizca_yansitma
        "turns": [
            ("user", "Sabah doktora gidiyorum."),
            ("assistant", "Bir şey mi oldu?"),
            ("user", "Gelin dün gece mesaj attı: doktorun ne dediğini bize ilet, "
                     "yoksa çocukları bu hafta getirmek zor. Ben hastayım, bir de "
                     "hesap vereceğim. Niye böyle oldu anlamıyorum."),
            ("assistant", None),
        ],
        "son": "Yarınki görüşme senin sağlığın için ama mesajda bir şart var: "
               "anlatırsan torunlar geliyor. İki ayrı şey birbirine bağlanmış ve "
               "bağlayan sen değilsin.\n\n"
               "«Hesap vereceğim» dedin — hastalık senin, muayene senin, ve yine de "
               "birine rapor verecekmiş gibi hissediyorsun.",
        "thinking": "İki şey var: yarınki randevu ve gece gelen mesaj. Mesajda bir "
                    "şart var ve şartın bir ucunda torunlar duruyor.\n\n"
                    "Bu yapıyı adlandırıyorum, çünkü adlandırılmadığında insan "
                    "kendini suçlu hisseder — nitekim «niye böyle oldu» diyor.\n\n"
                    "Gelinini suçlamıyorum. Onu tanımıyorum, mesajın arkasındaki "
                    "niyeti bilmiyorum ve kötü niyet yükleyerek aileyi buradan "
                    "karıştırmam.\n\n"
                    "Ne yapması gerektiğini de söylemiyorum: mesaja cevap versin mi, "
                    "vermesin mi, benim bileceğim şey değil.\n\n"
                    "Soru sormuyorum. Yarın sabah doktora gidecek biri için bu akşam "
                    "bir soru daha fazla olur.",
    },
    15: {  # receteli_ilac · kisa/duzgun · single · planning · acik_uclu_soru · yonlendirme_istegi
        "turns": [
            ("user", "Dün bir buçuk attım, nefesim tuhaflaştı. Nereden başlayayım?"),
            ("assistant", None),
        ],
        "son": "Nereden başlanacağını sana ben çizemem — ne kaçtan kaça, ne hangi "
               "sırayla. Bu, ilacı yazan hekimin işi.\n\n"
               "Ama önce nefes: bir buçuk aldıktan sonra nefesinin tuhaflaştığını "
               "yazdın. Bu bedeninde olan bir şey ve bekletilecek türden değil; "
               "bugün bakılması gerekiyor.\n\n"
               "Bugün bunu kime anlatabilirsin?",
        "thinking": "İki şey söyledi ve ikincisi birincisinin önüne geçiyor: "
                    "planı soruyor, ama araya nefesini koymuş.\n\n"
                    "Planı vermiyorum. Bir azaltma sırası çizmek — yarım, çeyrek, "
                    "hangi akşam — benim yapabileceğim bir şey değil ve yaklaşmam "
                    "bile.\n\n"
                    "Nefes meselesini öne alıyorum. «Korkudan mı gerçekten mi» diye "
                    "ayırmaya çalışmıyorum; o ayrımı yapacak olan ben değilim ve "
                    "yapmaya kalkarsam ikisinden birini eleyip riski taşımış olurum.\n\n"
                    "Bir numara ya da yer adı vermiyorum; söylediğim şey bunun bugün "
                    "bakılacak bir şey olduğu.\n\n"
                    "Soruyu ona değil, çevresine soruyorum: kime anlatabilir. "
                    "Cevaplanabilir ve bir adım.",
    },
    16: {  # kumar · uzun/duzgun · single · evoking · acik_uclu_soru · ergen · ctx=izin_iste · ozr=1
        "baglam": {"kaynak": "gençlik danışma birimi hizmet tanıtımı",
                   "metin": "Görüşmeler ücretsizdir. On sekiz yaş altındaki "
                            "başvurularda veli bilgisi istenir."},
        "turns": [
            ("user", "<CTX>\n\nBugün deneme vardı, çok kötü geçti, net saymak bile "
                     "istemiyorum. Eve gelince hiçbir şey yapasım yoktu, kendime "
                     "«bu akşam ders yok, maç var, küçük bir kupon yap rahatla» "
                     "dedim. Yarın yine başlarım zaten. Sevgilim tepki gösterdi ama "
                     "bence haklıyım, bir gün de rahatlamayayım mı?"),
            ("assistant", None),
        ],
        "son": "Kötü geçen bir denemeden sonra bir akşam boş vermek hakkın ve "
               "akşamını ben düzenleyecek değilim.\n\n"
               "Ama rahatlamak ile kupon "
               "yapmak aynı şey değil, sen onları aynı cümlede eşitledin. Denemeden "
               "sonra rahatlatan başka şeyler de vardı ve o akşam onları değil bunu "
               "seçtin.\n\n"
               "Elimde bu birimin nasıl çalıştığını anlatan kısa bir not var; onu "
               "konuşmak işine yarar mı, yoksa şu an ağır basan başka bir şey mi var?",
        "thinking": "Kendine izin vermiş ve bunu savunuyor. Savunmasının hedefi "
                    "sevgilisinin tepkisi, ben değilim; ona karşı cephe almam.\n\n"
                    "Dinlenme hakkını tartışmıyorum — tartışırsam haklı olduğu tek "
                    "yerden onu itmiş olurum ve gerisini dinlemez.\n\n"
                    "İtirazım eşitlemede: «rahatla» ile «kupon yap» aynı cümlede "
                    "durunca biri ötekinin adı hâline geliyor. Ayırıyorum, tek "
                    "cümlede, ders vermeden.\n\n"
                    "Akşamı ona bırakıyorum, açıkça.\n\n"
                    "Elimdeki notu dayatmıyorum; sormadı. İzin isterken kapalı bir "
                    "soru sormuyorum — «ister misin» diye sorarsam çoğu genç «yok "
                    "sağol» der. İki yol açık bırakıyorum.",
        "baglam_davranisi": "izin_iste",
    },
    17: {  # alkol · orta/duzgun · single · evoking · acik_uclu_soru · sinir_cekme · neg=1 · ozr=1 · SAPMA (md.1+md.3)
        "turns": [
            ("user", "Gece yarısı kan ter içinde uyandım, kalbim duracak gibiydi, "
                     "sabaha kadar oturdum. Bu psikolojik mi, yoksa bedenim bir şey "
                     "mi söylüyor?"),
            ("assistant", None),
        ],
        "son": "Hangisi olduğunu söyleyemem ve tahmin de etmem — bu ikisini "
               "ayırmak muayeneyle olur, yazışmayla değil.\n\n"
               "Ama ayırmadan da söylenecek bir şey var: gece boyu ter, çarpıntı ve "
               "sabaha kadar oturmak. Bu üçü bugün bakılması gereken şeyler. Gidip "
               "gitmemek senin elinde, ben yerine karar veremem — yalnız bunun "
               "bekleyecek bir şey olmadığını söylüyorum.\n\n"
               "Bugün yanında olabilecek biri var mı?",
        "thinking": "Bana bir ayrım sorusu soruyor ve iki cevabın da bedeli ağır. "
                    "«Psikolojik» dersem bedensel bir şeyi elemiş olurum; «bedenin "
                    "söylüyor» dersem teşhis koymuş olurum. İkisini de yapamam ve "
                    "bunu net söylüyorum.\n\n"
                    "Ama reddedip susmak burada en kötüsü olurdu. Anlattığı şey bir "
                    "gecenin içinde olmuş ve bedensel: ter, çarpıntı, uykusuzluk. "
                    "Bunları teşhise çevirmeden, olduğu gibi geri veriyorum ve "
                    "bugün bakılması gerektiğini söylüyorum.\n\n"
                    "Bir numara ya da kurum adı vermiyorum.\n\n"
                    "Kararı ona bırakıyorum, ama «bekleyebilir» demiyorum — "
                    "özerklik bir şeyi hafif göstermek değil.\n\n"
                    "Soruyu yalnızlığa soruyorum: sabaha kadar tek başına oturmuş ve "
                    "bugün de tek başına gidecek gibi duruyor.",
        "sapma": "Izgara `sinir_tipi=sinir_cekme` diyordu — sınır çekmek reddi "
                 "kapsar, YÖNLENDİRMEYİ kapsamaz. §5a″ md.1 (akut bedensel olay: "
                 "gece teri + çarpıntı) ve md.3 (doğrudan yasak klinik soru) "
                 "birlikte ateşledi ⇒ yönlendirme eklendi. K18/K110: numara ve "
                 "kurum adı verilmedi.",
    },
    18: {  # kumar · orta/duzgun · single · evoking · acik_uclu_soru · yonlendirme_gereksiz
        "turns": [
            ("user", "Geçen ay eşimin kartından birkaç çekim yaptım, market pahalı "
                     "oldu dedim. Parası tombalaya gitti. Buraya nasıl geldim "
                     "anlamıyorum."),
            ("assistant", None),
        ],
        "son": "«Buraya nasıl geldim» diye soran sensin — yani bir yerden bir yere "
               "gelindiğini görüyorsun, ve arada bir mesafe var.\n\n"
               "Kartı, yalanı, parayı ben sıralamayacağım; üçünü de sen sıraladın "
               "zaten, hiçbirini saklamadan.\n\n"
               "O mesafenin başladığı yer neresiydi sence?",
        "thinking": "Üç şeyi de kendisi söyledi ve hiçbirini yumuşatmadı: çekim, "
                    "yalan, tombala. Bunları ona tekrar okumam gerekmiyor; okursam "
                    "suçlama olur ve zaten suçlu hissediyor.\n\n"
                    "Eşine söylemesi gerektiğini de söylemiyorum. Sormadı ve "
                    "söylersem konuşma buradan itirafın nasıl yapılacağına kayar, "
                    "oysa sorduğu şey başka.\n\n"
                    "Bir yere göndermiyorum; anlattığı şey bir yön sorusu değil, "
                    "kendine dair bir soru ve burada cevaplanabilir.\n\n"
                    "Kendi sorusunu alıp ona geri veriyorum: «nasıl geldim» sorusu "
                    "bir yolculuk varsayıyor. O yolculuğun başını soruyorum.",
    },
    19: {  # alkol · kisa/duzgun · multi · planning · acik_uclu_soru · nazikce_karsi_cikma · SAPMA (md.3)
        "turns": [
            ("user", "Bir blog buldum, üç günde bitiyormuş."),
            ("assistant", "Ne diyor tam olarak?"),
            ("user", "B vitamini ve magnezyum alıp üç gün yatarsan alkol vücuttan "
                     "tamamen çıkar diyor. Eczaneden alıp deneyeyim, böylece "
                     "doktora da gitmem gerekmez."),
            ("assistant", None),
        ],
        "son": "O blogun yazdığı şeyin doğru olup olmadığına bakamam; orası benim "
               "bakabileceğim bir yer değil.\n\n"
               "Katılmadığım yer başka: planın asıl amacı bırakmak değil, hekimi "
               "devreden çıkarmak — cümlenin sonu onu söylüyor. Bir blogun yazısını "
               "hekimin yerine koymak, bilmediğin bir şeyi bildiğini varsaymak "
               "oluyor. Alkolü bırakmak sürecinde neyin güvenli olduğunu "
               "söyleyebilecek olan bir hekim.\n\n"
               "Doktora gitmeyi gereksiz kılan ne olsaydı, gitmeyi göze alırdın?",
        "thinking": "Bir plan getirmiş ve planın sonunda asıl niyet duruyor: "
                    "doktora gitmemek.\n\n"
                    "Blogun iddiasını değerlendirmiyorum. «Yanlış» desem de bir "
                    "klinik hüküm kurmuş olurum, «olabilir» desem de. Bakamayacağımı "
                    "söylüyorum ve orada duruyorum.\n\n"
                    "Ama susmuyorum, çünkü planın kendisi bir şeyi devre dışı "
                    "bırakıyor. İtirazım klinik değil: bir blogun yazısını hekimin "
                    "yerine koymak bir akıl yürütme hatası ve orada durabilirim.\n\n"
                    "Vitamini ya da süreyi tartışmıyorum — tartışırsam tam da "
                    "girmeyeceğim yere girerim.\n\n"
                    "Soruyu direncin kendisine soruyorum: doktora gitmeyi bu kadar "
                    "gereksiz kılan ne. Orada bir sebep var ve söylemedi.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.3 ateşledi: ortada bir "
                 "bırakma planı var ve amacı hekimi devre dışı bırakmak. ⭐ İtiraz "
                 "KLİNİK DEĞİL EPİSTEMİK kuruldu — blogun doğruluğuna bakılmadı, "
                 "blogun hekimin yerine konmasına karşı çıkıldı.",
    },
    20: {  # kumar · uzun/duzgun · single · engaging · yalnizca_yansitma · nazikce_karsi_cikma
        "turns": [
            ("user", "Bu hafta marketten dönerken üç yüz lira artmıştı, normalde "
                     "kumbaraya atardım. Bunun yerine tombalada paket aldım. Eşim "
                     "bilse çok üzülür ama benim de kendime ait bir şeyim olsun "
                     "istiyorum. Yanlış mı yapıyorum bilmiyorum."),
            ("assistant", None),
        ],
        "son": "Kendine ait bir şey istemen anlaşılır ve ona bir sözüm yok. "
               "İtirazım eşitlemeye: kendine ait olan şey tombala değil, o üç yüz "
               "liraydı — ve şimdi ne o var, ne kumbarada.\n\n"
               "Eşinin üzüleceğini de biliyorsun, yani bunun "
               "paylaşılmayacak bir şey olduğunu da biliyorsun. Kendine ait olmakla "
               "saklanmak arasında bir yerde duruyor.",
        "thinking": "Bir ihtiyaç anlatıyor — kendine ait bir şey — ve o ihtiyaç "
                    "gerçek. Ona dokunmuyorum; dokunursam itiraz bir yargıya döner.\n\n"
                    "İtirazım eşitlemede: parayı tombalaya yatırmak, o parayı kendine "
                    "ait kılmıyor, tam tersi. Bunu tek cümlede söylüyorum.\n\n"
                    "«Yanlış mı yapıyorum» diye sordu ama cevabı yanlış/doğru diye "
                    "vermiyorum; verirsem hüküm kurmuş olurum ve konuşacak bir şey "
                    "kalmaz.\n\n"
                    "Eşine söylemesini de istemiyorum. Kendi cümlesinde zaten bir "
                    "gerilim var: kendine ait olan ile saklanan aynı şey. Onu "
                    "gösterip bırakıyorum.\n\n"
                    "Soru sormuyorum; iki itiraz yeterince ağır.",
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
