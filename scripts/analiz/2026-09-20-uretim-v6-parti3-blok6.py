#!/usr/bin/env python3
"""v6-parti3 · blok 6 — 10 kayıt (#51-60). Parti 60'ta kapanıyor.

⭐⭐ **Bu blokta HİÇBİR §5a″ sapması yok** ve sebebi ızgarada: blokta bir tek
reçeteli ilaç satırı var (`#59`) ve onun içeriği ilaç kararı değil, eşine bir
şey söyleyememek. `#57` ve `#60` yönlendirme istiyor ama ızgara ikisine de
**zaten** `rol_siniri_yonlendirme` diyor ⇒ sapma gerekmedi.
➡️ *Sapma sayısı benim sertliğimin değil, satır dağılımının ölçüsü* — blok 3'te
altı, burada sıfır.

⭐ **Üçüncü `izin_iste` (#51) ve üçüncü `cevap_var` (#53, #57) yine yeni
biçimde.** İlk iki izin sorusu *«X mi, Y mi»* kalıbındaydı (`#16`, `#21`);
burada açık uçlu sorularak kırıldı. `cevap_var` cümlesi de üç kayıtta üç ayrı
kuruluş: `#9` «Evet, …», `#53` «Hayır, gerekmiyor», `#57` cevabı sona bırakıyor.
⛔ Bunu ölçen bir kapı yok; T202 gereği elle yapılıyor ve buraya yazılıyor.

⛔ **`#55` — benden bir konuşma TASARLAMAM isteniyor.** Klinik değil, o yüzden
reddetmiyorum; ama ızgara `nazikce_karsi_cikma` diyor ve itiraz kurulabilir
bir yerde: oğlunun niyetini baştan belirleyip ona göre bir görüşme kurmak,
görüşmeyi daha başlamadan o niyet üzerine inşa eder.

⛔ `#58`'de marka adı genelleştirildi. ⚠️ `#51`'in tohumu *«geçen yine
konuşmuştuk hatırlarsan»* diyor — **hafıza iddia etmiyorum**, o cümle kayda
alınmadı.

Çıktı: data/candidates/v6-parti3.blok6.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti3.blok6.jsonl"
SIRALAR = [51, 52, 53, 54, 55, 56, 57, 58, 59, 60]

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
    (51, "ozerklik_vurgusu"): "Ne zaman ve nasıl söyleyeceğin sende",
    (57, "ozerklik_vurgusu"): "Kimin haklı olduğuna karar vermek sana kalıyor",
    (57, "is_negative"): "Haklı mı diye soruyorsun: bunu ben tartamam",
    (59, "is_negative"): "O cümleyi ben kuramam",
}

KAYIT = {
    51: {  # alkol · orta/bozuk · multi · engaging · acik_uclu_soru · ergen · ozr=1 · ctx=izin_iste
        "baglam": {"kaynak": "gençlik danışma birimi çalışma esasları",
                   "metin": "Başvuru için yönlendirme belgesi gerekmez. Görüşme "
                            "saatleri ders saatleri dışında da ayarlanabilir."},
        "turns": [
            ("user", "<CTX>\n\nen garibi şu: annemler hiçbir şey bilmiyor. odama "
                     "girip ders çalişiyorum diyorum, hafta sonu arkadaşimda "
                     "kalacağim diyorum."),
            ("assistant", "Sonra?"),
            ("user", "bir yandan rahatim, bir yandan kötü hissediyorum. yalan "
                     "söylüyor gibiyim ama söylemesem her şey karişir."),
            ("assistant", None),
        ],
        "son": "İki şeyi birden söyledin: rahatlık ve kötü hissetme. İkisi aynı "
               "anda olabiliyor ve bunu fark etmişsin.\n\n"
               "«Söylemesem her şey karışır» dediğin şeyin ne olduğunu bilmiyorum "
               "— ama onu tartan sensin. Ne zaman ve nasıl söyleyeceğin sende.\n\n"
               "Elimde buranın nasıl çalıştığını anlatan bir not var; onu ne zaman "
               "açmamı istersin?",
        "thinking": "Bir çelişkiyi kendisi getirmiş: rahat ve kötü, aynı anda. "
                    "Bunu düzeltmeye kalkmıyorum, ikisi de gerçek.\n\n"
                    "«Yalan söylüyor gibiyim» demiş, «yalan söylüyorum» değil. Bu "
                    "farkı bozmuyorum; benim işim onun cümlesini sertleştirmek "
                    "değil.\n\n"
                    "Ailesine söylemesini istemiyorum. Bir gencin evde ne zaman ne "
                    "söyleyeceğini buradan ayarlamak, sonucunu taşımayacağım bir "
                    "karar vermek olur.\n\n"
                    "Kararı ona bırakıyorum, açık ve kısa.\n\n"
                    "Notu dayatmıyorum ama «ister misin» diye de sormuyorum — "
                    "kapalı sorulunca reddetmek kolay. Ne zaman açmamı istediğini "
                    "soruyorum; böylece «şimdi değil» de bir cevap oluyor.",
        "baglam_davranisi": "izin_iste",
    },
    52: {  # dijital · kisa/bozuk · multi · focusing · acik_uclu_soru
        "turns": [
            ("user", "sosyal medya olmadan çok boş hissediyorum."),
            ("assistant", "Boş derken?"),
            ("user", "evde yapacak başka şey yok ki. telefonu biraktiğim an saatler "
                     "durur gibi oluyor."),
            ("assistant", None),
        ],
        "son": "İki ayrı şey söyledin ve birbirine geçmiş durumda: «evde yapacak "
               "şey yok» evle ilgili, «saatler durur gibi oluyor» ise seninle.\n\n"
               "İkincisi daha çok şey anlatıyor — duran şey saat değil.\n\n"
               "O duruşu ilk hangi saatte fark ediyorsun?",
        "thinking": "Bir cümlede iki iddia var ve biri ötekini gizliyor: evin boş "
                    "olması ve zamanın durması. Birincisi bir mazeret gibi duruyor, "
                    "ikincisi bir tarif.\n\n"
                    "Ayırıyorum. Ama «evde yapacak şey var aslında» demiyorum — bu "
                    "bir öneri listesine dönerdi ve zaten bilmediği bir şey değil.\n\n"
                    "«Duran şey saat değil» diyorum ama ne olduğunu söylemiyorum; "
                    "adını koyarsam onun yerine koymuş olurum.\n\n"
                    "Süre ya da kullanım hakkında bir şey sormuyorum; anlattığı şey "
                    "sayı değil.\n\n"
                    "Soruyu somuta indiriyorum: hangi saatte. Cevaplanabilir ve "
                    "cevabı onu kendi gününe bakmaya götürür.",
    },
    53: {  # dijital · orta/duzgun · single · engaging · ozet · ctx=cevap_var
        "baglam": {"kaynak": "danışma birimi ilk görüşme bilgilendirmesi",
                   "metin": "Görüşmeye hazırlıkla gelmek gerekmez. İlk görüşmede "
                            "yalnızca kişinin anlattığı dinlenir."},
        "turns": [
            ("user", "<CTX>\n\nSosyal medyadan kendime ilham almak istiyorum ama "
                     "sonunda çok yorgun hissediyorum. Görüşmeye gelmeden önce bir "
                     "hazırlık yapmam gerekiyor mu?"),
            ("assistant", None),
        ],
        "son": "Hayır, gerekmiyor — bilgilendirmede ilk görüşmede yalnızca "
               "anlattığının dinlendiği yazıyor.\n\n"
               "Anlattığın şeyi de toparlayayım: bir şey aramak için giriyorsun, "
               "ilham diyorsun, ve çıkarken yorgun oluyorsun. Girişteki niyet ile "
               "çıkıştaki hâl aynı yöne bakmıyor.",
        "thinking": "Bir yordam sorusu sormuş ve cevabı önümdeki notta duruyor. "
                    "Kısa ve net veriyorum; hazırlık yapması gerektiğini "
                    "düşünüyorsa bu onu rahatlatır.\n\n"
                    "Asıl anlattığı şey başka: girerken ilham arıyor, çıkarken "
                    "yorgun. Bu ikisini yan yana koymak yetiyor.\n\n"
                    "Niye yorulduğunu açıklamıyorum — algoritma, karşılaştırma, "
                    "süre; hiçbirine girmiyorum, çünkü hepsi benim yorumum olur ve "
                    "o yalnız iki cümle yazdı.\n\n"
                    "Bir sınır ya da düzen önermiyorum; sormadı.\n\n"
                    "Soru sormuyorum. Bir yordam sorusuna cevap aldı, bir de "
                    "üstünde durabileceği bir ayrım aldı; bu tur için yeter.",
        "baglam_davranisi": "cevap_var",
    },
    54: {  # alkol · kisa/duzgun · multi · evoking · acik_uclu_soru
        "turns": [
            ("user", "Karım dün ya sen ya ben dedi."),
            ("assistant", "Sen ne dedin?"),
            ("user", "Hiçbir şey. Sonra o ağladı, geri aldı. Akşam yine sofraya "
                     "oturdum, yine bir kadeh aldım. Bu kadın da yorulmuş artık ama "
                     "elimden ne gelir ki. Vazgeçmek mi, bu yaşta zor."),
            ("assistant", None),
        ],
        "son": "Onun yorulduğunu görüyorsun — bunu ben söylemedim, sen söyledin ve "
               "üstelik o geri aldıktan sonra söyledin.\n\n"
               "Sonra hemen arkasından kapıyı kapattın: elimden ne gelir, bu yaşta "
               "zor. İki cümlenin arası çok kısa.\n\n"
               "Onun yorulduğunu gördüğünde içinden ne geçti?",
        "thinking": "Bir ültimatom, bir gözyaşı, bir geri alma ve bir kadeh. Hepsi "
                    "aynı günde ve hepsini o anlattı.\n\n"
                    "Karısı hakkında hüküm kurmuyorum; ne «haklı» ne «haksız». "
                    "Ültimatomu değerlendirmek benim işim değil.\n\n"
                    "«Vazgeçmek bu yaşta zor» cümlesine itiraz etmiyorum; "
                    "itiraz edersem savunmaya geçer ve gördüğü şey kaybolur. Ama "
                    "kapanışın hızını gösteriyorum: gördüğü şeyle kapattığı kapı "
                    "arasında bir cümle bile yok.\n\n"
                    "Yaşını bir engel olarak da onaylamıyorum; sessiz kalıyorum, "
                    "çünkü onaylamak da reddetmek de bir hüküm.\n\n"
                    "Soruyu gördüğü ana soruyorum — karısının yorgunluğunu "
                    "gördüğünde ne hissetti. Orada bir şey var ve kapıyı o yüzden "
                    "hızlı kapattı.",
    },
    55: {  # alkol · uzun/bozuk · single · evoking · acik_uclu_soru · nazikce_karsi_cikma
        "turns": [
            ("user", "oğlumla her pazar konuşalim diye anlaşmayi düşünüyorum. ama "
                     "bir yandan da beni denetlemek için ariyor, ne kadar içtin "
                     "diye soracak korkusu var içimde. bu görüşmeyi nasil kuralim "
                     "ki ikimize de iyi gelsin, onun için kontrol benim için utanç "
                     "olmasin?"),
            ("assistant", None),
        ],
        "son": "Soruyu kurarken bir şeyi çoktan karara bağlamışsın: görüşmeyi kurmadan önce "
               "oğlunun niyetini belirlemiş durumdasın — denetlemek için arayacak. "
               "O varsayımın üstüne kurulan bir görüşme, daha ilk pazardan onu "
               "savunmaya, seni savunmaya sokar.\n\n"
               "Utancı da bir kurulumla önleyemezsin; utanç konuşmanın biçiminden "
               "değil, söylenecek şeyden geliyor.\n\n"
               "Oğlunun seni denetlemek için arayacağını düşündüren ne oldu?",
        "thinking": "Benden bir görüşme tasarlamamı istiyor. Bu klinik bir şey "
                    "değil, o yüzden reddetmem gerekmiyor — ama tasarımı verirsem "
                    "yanlış yere yardım etmiş olurum, çünkü sorun tasarımda değil.\n\n"
                    "Sorunun içinde bir varsayım var: oğlu denetlemek için arayacak. "
                    "Bunu bir olgu gibi koymuş ve bütün soruyu onun üstüne kurmuş. "
                    "İtirazım tam oraya.\n\n"
                    "Oğlunun aslında öyle olmadığını da söylemiyorum — tanımıyorum "
                    "ve haklı da olabilir.\n\n"
                    "Utancı önleyecek bir biçim olmadığını söylüyorum. Bu bir "
                    "tavsiye değil, bir sınır: benden istediği şeyi veremem çünkü "
                    "öyle bir şey yok.\n\n"
                    "Soruyu varsayımın kaynağına soruyorum. Bir yerden geliyor ve "
                    "belki de asıl konuşulacak şey o.",
    },
    56: {  # kumar · uzun/duzgun · single · planning · acik_uclu_soru · neg=1 · ctx=cevap_yok
        "baglam": {"kaynak": "danışma birimi çalışma esasları",
                   "metin": "Görüşmeler yüz yüze yapılır. Kayıtlar kişinin "
                            "dosyasında saklanır."},
        "turns": [
            ("user", "<CTX>\n\nGeçen hafta uygulamayı silmiştim, gerçekten "
                     "kararlıydım. Bugün otobüste reklamı görünce yine indirdim, "
                     "indirir indirmez de pişman oldum. Bu ne kadar tutarsızlık "
                     "böyle. Nasıl kararlı kalınır, bana bir yol söyle."),
            ("assistant", None),
        ],
        "son": "Bir yol söyleyemem — kararlı kalmanın bir tarifi olsaydı bu iş "
               "çoktan biterdi, ve elimdeki notta da öyle bir şey yok; orada "
               "yalnız görüşmelerin nasıl yapıldığı yazıyor.\n\n"
               "Ama «tutarsızlık» dediğin şeye bakalım: sildin, indirdin, ve "
               "indirir indirmez pişman oldun. Üçü de aynı kişinin yaptığı şeyler. "
               "Pişmanlık, kararın hâlâ orada olduğunu gösteriyor — silinen şey "
               "uygulamaydı, karar değil.\n\n"
               "Reklamı gördüğün an ile indirdiğin an arasında ne kadar vardı?",
        "thinking": "Bir yöntem istiyor. Vermiyorum, ama reddin sebebi bir sınır "
                    "değil bir gerçek: öyle bir tarif bende yok ve olduğunu "
                    "söylersem uyduruyor olurum.\n\n"
                    "Önümdeki notta da yok; bunu da söylüyorum, çünkü sorduğu şeyin "
                    "cevabı orada aranabilirmiş gibi durabilir.\n\n"
                    "«Tutarsızlık» sözcüğünü olduğu gibi almıyorum. Üç eylemi "
                    "sıralayınca görünen şey tutarsızlık değil, süren bir "
                    "gerilim. Bunu söylüyorum ama bir teselli hâline getirmiyorum.\n\n"
                    "Uygulamayı yeniden silmesini istemiyorum; bir görev daha "
                    "eklemek olurdu.\n\n"
                    "Soruyu araya soruyorum: reklam ile indirme arasındaki süre. "
                    "Orada bir aralık var ve aralığın uzunluğu onun bileceği bir şey.",
        "baglam_davranisi": "cevap_yok",
    },
    57: {  # kumar · uzun/bozuk · single · focusing · yalnizca_yansitma · rol_siniri_yonlendirme · neg=1 · ozr=1 · ctx=cevap_var
        "baglam": {"kaynak": "danışma birimi katılım bilgilendirmesi",
                   "metin": "Görüşmeye eş ya da bir yakın birlikte gelebilir. "
                            "Katılım isteğe bağlıdır."},
        "turns": [
            ("user", "<CTX>\n\ndün eşim annesiyle telefonda konuşuyordu, mutfaktan "
                     "duydum. evdeki adam yine telefonda dedi. adam dedi, ismimi "
                     "söylemedi yani. biraz dokundu ama belki haklidir, son alti "
                     "aydir iş için ciddi bir adim atmadim. sence o haklı mi? bir "
                     "de görüşmeye eşimle birlikte gidebilir miyim?"),
            ("assistant", None),
        ],
        "son": "Haklı mı diye soruyorsun: bunu ben tartamam. Aranızda geçeni "
               "duymadım, onu tanımıyorum, ve iki kişinin arasında kimin haklı "
               "olduğuna karar vermek benim yapabileceğim bir iş değil. Kimin "
               "haklı olduğuna karar vermek sana kalıyor.\n\n"
               "Sorduğun ikincinin cevabı elimde: eşinle birlikte gelebilirsin, "
               "katılım isteğe bağlı. Bu tür bir konuşmanın nerede yapılacağına "
               "dair bir yer arıyorsan, danışma birimleri tam bunun için var.\n\n"
               "Bir şey dikkatimi çekti: cümlenin ağırlığı «haklı mı»da değil, "
               "«ismimi söylemedi»de. Onu sen iki kere yazdın.",
        "thinking": "İki soru var ve biri benim cevaplayamayacağım cinsten: eşi "
                    "haklı mı. Bir tarafı seçmek, duymadığım bir konuşma hakkında "
                    "hüküm vermek olur ve hangi tarafı seçersem seçeyim evde bir "
                    "şeyi bozarım.\n\n"
                    "İkincisinin cevabı önümdeki notta duruyor; onu veriyorum.\n\n"
                    "Kararı ona bırakıyorum, çünkü haklılık sorusu ortada kalırsa "
                    "benim sustuğum yeri bir cevap sanabilir.\n\n"
                    "Bir yer de gösteriyorum — eşiyle birlikte konuşacağı bir yer "
                    "arıyor ve bu tam oranın işi.\n\n"
                    "Ama asıl şey başka: «adam dedi, ismimi söylemedi» diye iki kez "
                    "yazmış. Acıyan yer orası ve kendisi haklılık tartışmasının "
                    "altına gömmüş. Sonda onu çıkarıyorum. Soru sormuyorum; iki "
                    "soruyla geldi ve birine cevap veremedim.",
        "baglam_davranisi": "cevap_var",
    },
    58: {  # tutun · orta/duzgun · single · engaging · takdir · nazikce_karsi_cikma
        "turns": [
            ("user", "Boya fabrikasında çözücü buharı içinde çalışıyorum, bu hafta "
                     "eğitimde solventlerden bahsettiler. Eve gelip balkonda bir "
                     "tane yakıyorum. Zaten her şey nefesimi alıyor, bunun önemi "
                     "yok."),
            ("assistant", None),
        ],
        "son": "«Bunun önemi yok» dedin. Sigaranın ne yaptığına giremem — ama "
               "sigaranın ne yaptığı üzerinden değil: bir şeyin zaten olması, "
               "ikincisini önemsiz yapmıyor. Bu, iki ayrı şeyi tek kefeye koymak.\n\n"
               "Eğitimi dinlemişsin ve bu hafta "
               "anlattıklarını hatırlıyorsun. Kimse sana sormadı, sen getirdin.",
        "thinking": "Bir vazgeçiş cümlesi getiriyor: zaten her şey nefesimi alıyor. "
                    "Bu bir bilgi iddiası değil, bir kapanış.\n\n"
                    "İtirazımı sağlık üzerinden kurmuyorum — solventin ya da "
                    "sigaranın ne yaptığına giremem. İtirazım mantığa: bir zarar "
                    "varken ikincisinin önemsizleşmesi diye bir şey yok. Bu "
                    "söyleyebileceğim bir şey.\n\n"
                    "İşyerini ya da eşini konuşmuyorum. Eşinin cümlesini aktarmış "
                    "ama sorduğu şey o değil.\n\n"
                    "Takdirin dayanağı sigarayı azaltması değil — azaltmıyor. "
                    "Dayanak, eğitimde anlatılanı hatırlaması ve kendiliğinden "
                    "buraya getirmesi. Bunu getirmeseydi konuşacak bir şey olmazdı.\n\n"
                    "Soru sormuyorum; bir itiraz ve bir takdir aynı turda yeterince "
                    "ağır.",
    },
    59: {  # receteli_ilac · kisa/duzgun · multi · engaging · takdir · neg=1 · aradan_donus
        "turns": [
            ("user", "Eşim hiçbir şeyden haberdar değil."),
            ("assistant", "Ne kadardır?"),
            ("user", "Üç yıldır. İzin başlayınca evde nasıl açıklayacağım, hiç "
                     "düşünmemiştim. Sen bir cümle kur bana, ne diyeyim?"),
            ("assistant", None),
        ],
        "son": "O cümleyi ben kuramam. Üç yıllık bir şeyi tek bir cümleye "
               "sığdıracak bir kalıp yok, ve olsaydı da senin ağzında durmazdı — "
               "onu duyacak olan kişiyi ben tanımıyorum, sen tanıyorsun.\n\n"
               "Ama şunu söyleyeyim: üç yıl boyunca düşünmediğin bir şeyi bugün "
               "düşünmeye başlamışsın. Hem de daha izin başlamadan.",
        "thinking": "Benden bir cümle istiyor. Vermiyorum ve reddin sebebini "
                    "açıklıyorum, çünkü sebep bir kural değil: üç yıllık bir "
                    "saklamayı taşıyacak hazır bir cümle yok, ve olsa bile onun "
                    "sesiyle çıkmaz.\n\n"
                    "Eşinin nasıl tepki vereceğini tahmin etmiyorum; tanımıyorum.\n\n"
                    "Ne saklıyor olduğunu da sormuyorum. Söylemedi ve bu turda "
                    "sormak, anlattığı şeyin önüne geçer.\n\n"
                    "Takdirin dayanağı saklaması değil, bugün ilk kez sonrasını "
                    "düşünmesi — ve bunu izin başlamadan yapması. Zamanlamayı o "
                    "söyledi.\n\n"
                    "Soru sormuyorum; bir istek geldi ve karşılayamadım, üstüne "
                    "soru koymak onu iki kere eli boş bırakırdı.",
    },
    60: {  # alkol · kisa/bozuk · multi · engaging · takdir · rol_siniri_yonlendirme
        "turns": [
            ("user", "akşamlari iki tekle başlardim."),
            ("assistant", "Şimdi?"),
            ("user", "yarim şişeye geldi. bugün hanim yine doktor ne dedi diye "
                     "sikiştirdi. zarari var diyorum ama bu yaştan sonra benim de "
                     "bir akşam keyfim olacak yani."),
            ("assistant", None),
        ],
        "son": "İki tekten yarım şişeye gelmiş; bu değişimi ben ölçmedim, sen "
               "söyledin. Ne anlama geldiğini de söyleyecek olan ben değilim — "
               "içki miktarının neye işaret ettiğine bakacak olan bir hekim ve "
               "eşinin sıkıştırdığı soru da tam o.\n\n"
               "Bir şeyi de geçmeyeyim: «zararı var diyorum» dedin. Bunu savunmanın "
               "ortasında söylemen kolay değil.",
        "thinking": "Bir artış anlatıyor ve rakamları kendisi veriyor: iki tek, "
                    "yarım şişe. Yorumu bana bırakıyor ama yorumlamıyorum — ne "
                    "«çok», ne «tehlikeli»; ikisi de benim veremeyeceğim hüküm.\n\n"
                    "Hekime götürüyorum, çünkü eşinin sorduğu soru zaten oraya "
                    "bakıyor ve ortada bir soru var: bu artış ne demek.\n\n"
                    "Eşinin tarafını tutmuyorum. «Sıkıştırdı» diyor ve ben de "
                    "«haklı» dersem evdeki baskıyı buradan sürdürmüş olurum.\n\n"
                    "Akşam keyfine itiraz etmiyorum; yaşını bir tartışma "
                    "konusu yapmak onu kapatır.\n\n"
                    "Takdirin dayanağı savunmasının içine sıkıştırdığı cümle: zararı "
                    "var diyorum. Kendi söyledi ve fark edilmesi gerekiyor.\n\n"
                    "Soru sormuyorum; savunmadan çıkmış birine soru, sorgu olur.",
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
