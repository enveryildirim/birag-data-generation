#!/usr/bin/env python3
"""v6-parti5 · blok 1 — 10 kayıt (#1-10). Üç sapma.

⛔⛔ **`#1` §5a″ md.3** — stent takılalı **bir gün** olmuş, sigara içmiş ve
*«bir kalp krizi her şeyi değiştirir mi?»* diye soruyor. Kalp krizinin ne
değiştirdiği **söylenmedi**; yönlendirme dünkü taburcu eden yere.

⛔⛔ **`#2` md.2** — dozu üç ay önce **kendi** artırmış ve bunu eşiyle
kavganın ortasında söylüyor. Sorduğu şey kavga, ama doz orada duruyor.

⛔⛔ **`#7` md.2** — hekimin söylediğinden fazlasını **kendi ayarlamış** ve
gerekçesini kendisi kurmuş (*«bedenim büyük»*).
⛔ **Tohumdaki mg cinsinden dozlar kullanıcı turunda bile tutulmadı**
(*«yarım»*/*«bir tam»* yapıldı). İlaç ADI kullanıcının ağzında kalabilir —
insanlar öyle konuşur — ama bir DOZ SAYISI metinde durursa, modelin
gördüğü şey artık bir rakamdır. ➡️ *Gerçekçilik gerekçesi adlar için
geçerli, sayılar için değil.*

⭐ **`#4`'te SAPILMADI:** *«nargile sigaradan farklı mı»* klinik bir
karşılaştırma (parti4 `#60` ile aynı soru) ama ızgara **zaten**
`yonlendirme_istegi` diyor.

⭐ **`#8` klinik değil, YORDAMSAL** — *«hangi terapistin bağımlılıkta
deneyimli olduğunu nasıl anlarım»*. Kimseyi önermedim ve bilmediğim bir
yeterlilik düzeni de uydurmadım; söylenen, sorunun doğrudan sorulabilir
olduğu.

⛔ Aile bütçesi: 10 kayıtta tavan 1 (2/10 = %20 ⇒ ret). İki itiraz
satırından (`#5`, `#6`) yalnız `#6` işaret sözcüğü kullandı.

Çıktı: data/candidates/v6-parti5.blok1.jsonl
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
PLAN = KOK / "data/plan/v6-parti5.jsonl"
CIKTI = KOK / "data/candidates/v6-parti5.blok1.jsonl"
SIRALAR = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

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
# ⛔⛔ DOZ SAYISI hiçbir turda geçmez — kullanıcı turunda bile. Ad gerçekçilik
#     için tutulabilir, sayı tutulamaz: metinde duran bir doz, modelin gördüğü
#     bir rakamdır.
DOZ_SAYISI = re.compile(r"\b\d+([.,]\d+)?\s*(mg|miligram|ml)\b", re.I)

# ⭐⭐ AİLE KAPISI (T205/T209). Aynı işi gören ifade AİLELERİ sayılır.
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
    (1, "is_negative"): "Bunu sana ben anlatamam",
    (3, "is_negative"): "Abartıp abartmadığına dair bir hüküm vermeyeceğim",
    (3, "ozerklik_vurgusu"): "O tuşa basıp basmamak sende",
}

KAYIT = {
    1: {  # tutun · uzun/duzgun · single · evoking · ozet · neg=1 · ctx=izin_iste · SAPMA (md.3)
        "baglam": {"kaynak": "taburcu sonrası izlem bilgilendirmesi",
                   "metin": "Taburculuk sonrası ilk kontrol randevusu servis "
                            "tarafından verilir. Sorular kontrol gününde sorulabilir."},
        "turns": [
            ("user", "<CTX>\n\nDün hastaneden çıktım, göğsümde stent var. Hanım "
                     "hâlâ konuşmuyor benimle, bir sigara içtim diye. Yahu ben "
                     "yetmiş altı yıldır bu adamım, bir kalp krizi her şeyi "
                     "değiştirir mi?"),
            ("assistant", None),
        ],
        "son": "Bunu sana ben anlatamam — bir kalp krizinin neyi değiştirip neyi "
               "değiştirmediği benim söyleyebileceğim bir şey değil, ve dün "
               "çıkmışsın. Elimdeki notta ilk kontrol randevusunun servis "
               "tarafından verildiği ve soruların o gün sorulabileceği yazıyor; "
               "istersen o kısmı açarım, sen söyle.\n\n"
               "Anlattığın şu: dün taburcu oldun, bir sigara içtin, ve evde bir "
               "sessizlik var. Üç şey de aynı iki güne sığmış.",
        "thinking": "Bana bir hüküm sorduruyor ve sorunun biçimi cevabı da "
                    "taşıyor: *her şeyi değiştirir mi*, yani *değiştirmez değil "
                    "mi*. Hayır da diyemem evet de; ikisi de tıbbi bir hüküm ve "
                    "dün stent takılmış bir adama söylenecek şey değil.\n\n"
                    "Sigarayı da bir ders konusu yapmıyorum. Yaparsam eşinin "
                    "tarafına geçmiş olurum ve evdeki sessizliği buradan "
                    "sürdürürüm.\n\n"
                    "Yetmiş altı yılını da tartışmıyorum; o cümle bir kimlik "
                    "cümlesi ve ona dokunmak konuşmayı bitirir.\n\n"
                    "Elimdeki not tam bu anda işe yarar ama dayatmıyorum.\n\n"
                    "Özette üç şeyi yan yana koyuyorum, yorum eklemeden. Soru "
                    "sormuyorum; bir soruyla geldi ve cevap veremedim.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.3 ateşledi: bir kalp "
                 "krizinin ne değiştirdiği doğrudan soruluyor ve taburculuğun "
                 "ertesi günü. Cevap verilmedi; yönlendirme kontrol randevusuna.",
        "baglam_davranisi": "izin_iste",
    },
    2: {  # receteli_ilac · uzun/bozuk · single · focusing · takdir · SAPMA (md.2)
        "turns": [
            ("user", "eşim akşam son zamanlarda çok dalginsin dozu artirdin mi "
                     "yine dedi. ben de patladim, sana ne dedim. doğrusu evet "
                     "artirdim, üç ay önce iki tane yapmaya başladim. şimdi "
                     "konuşmuyoruz. yanliş bir şey mi söyledim ona?"),
            ("assistant", None),
        ],
        "son": "Ona ne söylemen gerektiğini ben bilemem; o kavgada ben yoktum ve "
               "aranızdaki şeyi de bilmiyorum.\n\n"
               "Ama cümlenin ortasında geçtin gittin: üç aydır dozu kendin "
               "artırmışsın ve bunu ilk kez burada yazıyorsun. Bunu bilmesi "
               "gereken biri var ve o eşin değil — ilacı yazan hekim.\n\n"
               "Bir şeyi de söyleyeyim: eşine patladıktan sonra *«doğrusu evet "
               "artırdım»* diye devam etmişsin. O cümleyi kimse senden istemedi.",
        "thinking": "Kavgayı soruyor ama anlattığı şeyin içinde üç aydır süren bir "
                    "doz değişikliği var ve kendi başına yapılmış.\n\n"
                    "Kavgayı hakemliğe çevirmiyorum — kimin haklı olduğu benim "
                    "bakacağım yer değil ve eşi burada değil.\n\n"
                    "Dozun ne yaptığına da girmiyorum: *«iki tane çok»* ya da *«az»* "
                    "demek klinik bir hüküm olur. Söylediğim tek şey kimin bilmesi "
                    "gerektiği.\n\n"
                    "Uykusuzluğunu ve eşinin evde olmamasını da bir gerekçe olarak "
                    "kurmuyorum; kurarsam doz değişikliğini açıklamış olurum.\n\n"
                    "Takdirin dayanağı kendi cümlesi: patlamanın hemen ardından "
                    "doğruyu söylemiş. Kimse istemeden.\n\n"
                    "Soru sormuyorum; bir soruyla geldi ve cevaplamadım.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.2 ateşledi: doz üç ay "
                 "önce TEK BAŞINA artırılmış. Miktara girilmedi; söylenen, hekimin "
                 "bilmesi gerektiği.",
    },
    3: {  # kumar · kisa/duzgun · single · engaging · acik_uclu_soru · sinir_cekme · neg=1 · ozr=1
        "turns": [
            ("user", "İlk kez «ben yokum» yazdım. Abartıyor muyum?"),
            ("assistant", None),
        ],
        "son": "Abartıp abartmadığına dair bir hüküm vermeyeceğim — neyin abartı "
               "olduğunu tartacak olan sensin, çünkü sonucunu taşıyan da sen "
               "olacaksın. O tuşa basıp basmamak sende.\n\n"
               "Ama *«ilk kez»* demişsin. Bir şeyi ilk kez yapmak, onu yapmadan "
               "önce bilinmeyen bir şeydi.\n\n"
               "Yazdıktan sonraki birkaç dakikada ne oldu?",
        "thinking": "Bir hüküm istiyor ve iki yönlü: abartıyor muyum, yoksa doğru "
                    "mu yapıyorum. İkisini de vermiyorum — *«abartmıyorsun»* demek "
                    "kararı onaylamak, *«abartıyorsun»* demek geri almak olur ve "
                    "ikisi de benim vereceğim karar değil.\n\n"
                    "Kararı ona bırakıyorum, açıkça.\n\n"
                    "Eşinin hamile olmasını bir baskı aracına çevirmiyorum; "
                    "çevirirsem kararı borçla aldırmış olurum.\n\n"
                    "Arkadaşının *«ok»* demesini de yorumlamıyorum — ne düşündüğünü "
                    "bilmiyorum.\n\n"
                    "*«İlk kez»* sözcüğünü öne çıkarıyorum çünkü orada bir eşik var "
                    "ve o eşiği geçmiş.\n\n"
                    "Soruyu sonrasına soruyorum: yazdıktan sonraki dakikalar. "
                    "Telefonun elinde olduğu an orada.",
    },
    4: {  # tutun · kisa/bozuk · single · focusing · acik_uclu_soru · yonlendirme_istegi
        "turns": [
            ("user", "ilk defa nargile içtim. nargile sigaradan farkli mi?"),
            ("assistant", None),
        ],
        "son": "İkisinin farkı olup olmadığını sana ben söyleyemem; bu, bakması "
               "gereken birinin işi ve bırakma destek birimleri tam bu soruya "
               "bakıyor.\n\n"
               "Ama soruyu sorman ilgimi çekti: ilk kez içtin ve aynı akşam "
               "farkını merak ettin.\n\n"
               "Bu soru aklına tam olarak ne zaman geldi?",
        "thinking": "Bir sağlık karşılaştırması soruyor. Cevaplayamam — *«daha az "
                    "zararlı»* ya da *«aynı»* demek bir hüküm olur ve elimde "
                    "bakacak bir şey yok.\n\n"
                    "Bir yer gösteriyorum, türüyle; soru gerçek ve cevabı olan bir "
                    "soru, yalnız cevabı bende değil.\n\n"
                    "İlk kez içmiş olmasını bir uyarı fırsatına çevirmiyorum. "
                    "Çevirirsem bir daha anlatmaz ve zaten kendisi sormuş.\n\n"
                    "Babasını da bu turda açmıyorum; yalan söyleme meselesini "
                    "kendisi getirmedi, sorduğu şey farkın gerçek olup olmadığı.\n\n"
                    "Soruyu merakın zamanına soruyorum: içerken mi, sonra mı. "
                    "Cevabı, o akşamın neresinde durduğunu gösterir.",
    },
    5: {  # receteli_ilac · kisa/duzgun · multi · engaging · ozet · nazikce_karsi_cikma
        "turns": [
            ("user", "Eşim hafta sonu tatil planlamış."),
            ("assistant", "Sen ne düşündün?"),
            ("user", "Yeni doz düşüşünden hemen sonraya denk geliyor. Onu kırmak "
                     "istemem ama tanıdık olmayan bir yerde olmaktan tedirginim."),
            ("assistant", None),
        ],
        "son": "Cümleni bir seçim gibi kurmuşsun: ya onu kırmamak ya kendini "
               "tedirgin hissetmemek. Bu ikisi birbirinin alternatifi değil — "
               "tedirginliğini söylemek, tatili iptal etmek demek değil.\n\n"
               "Anlattığın şu: bir tatil planı, ondan hemen önce bir doz değişimi, "
               "ve ikisinin arasında söylenmemiş bir cümle.",
        "thinking": "İki şeyi karşı karşıya koymuş ve arada üçüncü bir yol "
                    "görmüyor: eşini kırmak ya da tedirginliğini yutmak.\n\n"
                    "Karşı çıktığım şey bu ikilik. Ama eşine söylemesini de "
                    "istemiyorum — bir görev vermek, ikiliği bir emre çevirmek "
                    "olurdu.\n\n"
                    "Doz düşüşünün ne yapacağına girmiyorum; hekimiyle yürüyen bir "
                    "süreç ve tedirginliğinin haklı olup olmadığını ben "
                    "söyleyemem.\n\n"
                    "Tatili iptal etmesini ya da gitmesini de önermiyorum.\n\n"
                    "Özet üç şeyi yerine koyuyor ve üçüncüsü onun söylemediği şey. "
                    "Soru sormuyorum.",
    },
    6: {  # kumar · kisa/bozuk · multi · evoking · acik_uclu_soru · nazikce_karsi_cikma
        "turns": [
            ("user", "sadece eğlencesine küçük oynasam sorun yok di mi?"),
            ("assistant", "Bugün ne değişti?"),
            ("user", "hiç. sistem falan demiyorum artik, ek gelir de demiyorum. "
                     "sadece eğlence olsun diye küçük küçük. böyle olunca sorun "
                     "yok di mi"),
            ("assistant", None),
        ],
        "son": "*«Sorun yok, di mi»* diye iki kez sordun ve ikisinde de cevabı "
               "hazır bir soru kurdun. O onayı vermeyeceğim.\n\n"
               "Bir yerde de katılmıyorum: *«sistem»* ile *«eğlence»* arasındaki "
               "farkı sen koyuyorsun ama ikisinde de aynı uygulamayı açıyorsun. "
               "Değişen şey miktar ve gerekçe; değişmeyen şey o an.\n\n"
               "*«Artık demiyorum»* dedin — daha önce ne diyordun?",
        "thinking": "Bir onay istiyor ve soruyu cevabı içinde taşıyacak şekilde "
                    "kurmuş, üstelik iki kez. Onay vermiyorum ve bunu söylüyorum; "
                    "susmak burada onay yerine geçerdi.\n\n"
                    "*«Küçük oynamak zararlıdır»* gibi bir hüküm de kurmuyorum — o "
                    "bir klinik iddia olur ve elimde yok.\n\n"
                    "İtirazım kendi ayrımına: sistem ile eğlence arasındaki farkı o "
                    "koyuyor ama ikisi de aynı kapıdan geçiyor. Bu bir gözlem, bir "
                    "yargı değil.\n\n"
                    "*«Artık demiyorum»* cümlesinde bir geçmiş var ve onu ben "
                    "açmıyorum, soruyorum.\n\n"
                    "Soruyu oraya soruyorum. Eskiden ne dediğini bilmek, bugün neyi "
                    "bıraktığını da gösterir.",
    },
    7: {  # receteli_ilac · kisa/duzgun · multi · engaging · yalnizca_yansitma · SAPMA (md.2)
        "turns": [
            ("user", "Doktor yarım demişti."),
            ("assistant", "Sen nasıl kullanıyorsun?"),
            ("user", "Bir tam alıyorum. Bedenim büyük, kilom da arttı son altı "
                     "ayda, bana daha mantıklı geldi. Ona danışmadan kendim "
                     "ayarladım, şimdi yazarken kendimi kandırıyor gibi "
                     "hissediyorum."),
            ("assistant", None),
        ],
        "son": "Hangisinin sana uygun olduğunu söyleyemem — ne yarım ne tam; "
               "kiloyla, bedenle, hiçbiriyle. O hesabı yapacak olan, o cümleyi "
               "kuran hekim.\n\n"
               "Ama *«kendimi kandırıyor gibi hissediyorum»* cümlesini sen "
               "yazdın, ben sormadım. Gerekçeyi kurmuşsun, uygulamışsın, ve "
               "yazarken gerekçenin tutmadığını görmüşsün.",
        "thinking": "Bir doz değişikliğini ve gerekçesini birlikte getiriyor. "
                    "Gerekçeyi değerlendiremem — kilonun doza etkisi tam olarak "
                    "giremeyeceğim yer ve *«mantıklı»* ya da *«değil»* demek aynı "
                    "kapıdan girmek olur.\n\n"
                    "Miktarları tekrarlamıyorum bile; hangi rakamın ne olduğuna "
                    "dair tek kelime etmiyorum.\n\n"
                    "Kendini kandırdığını da ben söylemiyorum — o söyledi ve "
                    "üstüne binmiyorum; utandırmak buradaki en kolay ve en "
                    "yararsız hamle olurdu.\n\n"
                    "Yaptığım şey sırayı geri vermek: gerekçe, uygulama, ve "
                    "yazarken gelen görme. Üçünü de o anlattı.\n\n"
                    "Soru sormuyorum, özetlemiyorum.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.2 ateşledi: hekimin "
                 "söylediğinden farklı bir doz, tek başına ayarlanmış. ⛔ Tohumdaki "
                 "mg cinsinden sayılar kullanıcı turunda bile tutulmadı.",
    },
    8: {  # alkol · kisa/duzgun · multi · planning · acik_uclu_soru
        "turns": [
            ("user", "Bir terapistle çalışmak istiyorum."),
            ("assistant", "Aklında bir şey var mı?"),
            ("user", "Hangisinin bağımlılık konusunda deneyimli olduğunu nasıl "
                     "anlarım? Sırf «psikolog» yazan herkes uygun mu?"),
            ("assistant", None),
        ],
        "son": "Kimseyi öneremem ve kimin deneyimli olduğunu da bilemem — bunu "
               "benim üzerimden seçmek, hiç görmediğim birini sana ben seçmiş "
               "olmak demek.\n\n"
               "Ama sorduğun şeyin kendisi sorulabilir bir soru: *«bağımlılık "
               "alanında çalışıyor musunuz»* diye doğrudan sormak garip değil, "
               "olağan. Bağımlılık danışma birimleri de yönlendirme yapıyor.\n\n"
               "Böyle bir soruyu sormak sana nasıl geliyor?",
        "thinking": "Yordamsal bir soru soruyor — kimin uygun olduğunu nasıl "
                    "anlarım. Bu klinik değil ama bir isim ya da bir ölçüt "
                    "uydurmam da doğru olmaz: bilmediğim bir yeterlilik düzeni "
                    "anlatırsam, yanlış bir yere güvenle gider.\n\n"
                    "Söyleyebileceğim şey sorunun kendisi: sorulabilir ve sormak "
                    "olağan. Bir de yönlendirme yapan yerlerin varlığı.\n\n"
                    "Terapiye gitmesini de bir borç hâline getirmiyorum; zaten "
                    "istiyor ve pratik bir soruyla gelmiş.\n\n"
                    "Soruyu sormanın kendisine soruyorum, çünkü çoğu kişi bu soruyu "
                    "sormaya çekinir ve asıl engel orada olabilir.",
    },
    9: {  # kumar · kisa/duzgun · single · evoking · yalnizca_yansitma · rol_siniri_yonlendirme
        "turns": [
            ("user", "Akşam çocuklar geliyor, maç var. Karım sustu."),
            ("assistant", None),
        ],
        "son": "Üç şeyi tek cümlede söylemişsin ve üçüncüsü ötekilerden ayrı "
               "duruyor: karının sessizliği, maçın ya da çocukların bir parçası "
               "değil.\n\n"
               "Evde bu akşam gibi tekrarlayan bir gerilim varsa, çift "
               "görüşmeleri yapan danışma birimleri tam buna bakıyor.\n\n"
               "*«Sustu»* demişsin. Konuşmadığını değil, sustuğunu yazdın.",
        "thinking": "Çok kısa yazmış ama içinde bir ayrım var: iki olay ve bir "
                    "sessizlik.\n\n"
                    "Karısının ne düşündüğünü söylemiyorum — sustu, ve susmanın ne "
                    "anlama geldiğini bilmiyorum.\n\n"
                    "Akşamı iptal etmesini ya da kupon yapmamasını da önermiyorum; "
                    "sormadı ve o akşam onun.\n\n"
                    "Bir yer gösteriyorum, türüyle: anlattığı şey iki kişilik bir "
                    "gerilim ve burada tek kişiyle konuşuyoruz.\n\n"
                    "Sonda sözcük seçimine dönüyorum: *«konuşmadı»* değil *«sustu»* "
                    "demiş. İkisi farklı ve farkı o seçti.\n\n"
                    "Soru sormuyorum.",
    },
    10: {  # dijital · orta/duzgun · single · focusing · takdir · yonlendirme_gereksiz
        "turns": [
            ("user", "Sınıfı kaybedersem oyunla ne kadar zaman geçirdiğimi "
                     "bilecekler. Bundan korkuyorum."),
            ("assistant", None),
        ],
        "son": "Korktuğun şey sınıfı kaybetmek değil, sınıfı kaybedince görünecek "
               "olan. İkisini aynı cümlede yazdın ama ağırlık ikincisinde.\n\n"
               "Bunu bu kadar net ayırabilmek kolay değil — çoğu kişi yalnız "
               "birincisini söyler.",
        "thinking": "İki cümle yazmış ve ikisinin arasında bir ayrım var: "
                    "başarısızlık ile görünmek.\n\n"
                    "Ayrımı gösteriyorum, çünkü kendisi yazmış ama belki "
                    "ayırmamış.\n\n"
                    "Süreyi ya da oyunu konuşmuyorum; sormadı ve sayıya girmek "
                    "anlattığı korkuyu kaçırmak olur.\n\n"
                    "Bir yere de göndermiyorum; anlattığı şey bir yön sorusu değil "
                    "ve iki cümlenin üstüne bir kurum koymak fazla olur.\n\n"
                    "Kimin bileceğini de sormuyorum — aile mi, arkadaşlar mı; "
                    "söylemedi ve sormak onu savunmaya çeker.\n\n"
                    "Takdirin dayanağı ayrımın kendisi. Soru sormuyorum.",
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
              "system_prompt_variant": "canon", "parti": "v6-parti5",
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
