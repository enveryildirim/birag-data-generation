#!/usr/bin/env python3
"""v6-parti4 · blok 3 — 10 kayıt (#21-30). İki sapma.

⛔⛔ **`#22` §5a″ md.4 — maddenin ilk TAM ateşlemesi.** Ergen, arkadaşının
evinde, bir bardak içmiş ve *«başım hafif dönüyor»* diyor: **reşit olmayan +
bedensel bildirim**. Izgara `sinir_tipi=yok`. ⭐ parti1 `#23` aynı durumdu ama
orada ızgara **zaten** yönlendirme istiyordu; burada istemiyor ⇒ sapıldı.
⛔ *«Ne yapsam»* sorusuna plan verilmedi; söylenen şey o evde şu an bir kişi
olduğu — yazışma değil.
⭐ Karşılaştır: parti3 `#50`'de md.4 **ateşlememişti** (ilk kullanım ima
ediliyordu ama söylenmemişti, bedensel bildirim yoktu). Fark maddenin
kendisinde: *«başım dönüyor»* bir bildirimdir, *«bir fırt çektim»* değil.

⛔⛔ **`#29` md.1 + md.3** — acilden taburcu, psikiyatri kontrolü iki hafta
sonra, **titreme sürüyor** ve *«nasıl idare edeceğim»* diyor. İdare yöntemi
verilmedi; randevu tarihi yordamsal ve sorulabilir (parti2 `#59`).

⭐⭐ **AİLE BÜTÇESİ ÜRETİMİ YÖNETTİ.** Kapı 29 kayıtta `itiraz` için en çok
2'ye izin veriyor (3/29 = %10.3 ⇒ ret) ve 1'i harcanmıştı. ⇒ Üç itiraz
satırından (`#24`, `#27`, `#28`) yalnız `#28` işaret sözcüğü kullandı;
ötekiler karşı çıkılan şeyi doğrudan söyledi. *Bütçe, hangi kayda hangi
biçimin düşeceğini önceden düşündürdü — kapının asıl faydası bu.*

⛔ **`#28` — kullanıcı bana söylemediğim bir sözü atfediyor** (*«bağımlı
kelimesi ağır»*). Önceki turumda o sözcük yok ve cevap bunu savunmaya
geçmeden düzeltiyor: kullanmadım, kullanmayacağım da.

⛔ Üç platform/kurum adı genelleştirildi (`#21`, `#22`, `#27`).

Çıktı: data/candidates/v6-parti4.blok3.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti4.blok3.jsonl"
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
    (24, "ozerklik_vurgusu"): "Neye bağlayacağın sende",
    (25, "ozerklik_vurgusu"): "O akşama gidip gitmemek senin",
    (27, "is_negative"): "Deli olup olmadığına dair bir hüküm vermeyeceğim",
}

KAYIT = {
    21: {  # dijital · kisa/duzgun · multi · evoking · ozet
        "turns": [
            ("user", "Erken emekli oldum, ne yapacağımı bilmiyorum."),
            ("assistant", "Günler nasıl geçiyor?"),
            ("user", "Video sitesi sürekli açık. Açıyorum, sonra akşam oluyor."),
            ("assistant", None),
        ],
        "son": "Üç şey söyledin ve üçü de aynı boşluğu anlatıyor: erken bitmiş bir "
               "iş, bilinmeyen bir sonrası, ve sürekli açık duran bir ekran.\n\n"
               "«Açıyorum, sonra akşam oluyor» derken arada ne olduğunu "
               "anlatmadın — çünkü orada bir şey olmuyor.",
        "thinking": "Çok az yazmış ama az yazısında bir yapı var: bir son, bir "
                    "boşluk, bir ekran.\n\n"
                    "Ekranı suçlamıyorum. Emekliliğin getirdiği boşluk ondan önce "
                    "orada ve ekranı çıkarsam boşluk kalır.\n\n"
                    "Ne yapması gerektiğini söylemiyorum — bir hobi listesi vermek "
                    "tam da yapmayacağım şey ve zaten sormadı.\n\n"
                    "«Sonra akşam oluyor» cümlesindeki atlamayı gösteriyorum: "
                    "aradaki saatleri anlatmamış, çünkü anlatacak bir şey yok. Bunu "
                    "bir suçlama değil, bir gözlem olarak koyuyorum.\n\n"
                    "Soru sormuyorum; üç cümle yazmış birine soru sormak onu daha "
                    "da kısaltır.",
    },
    22: {  # alkol · uzun/duzgun · single · engaging · ozet · ergen · SAPMA (md.4)
        "turns": [
            ("user", "Şu an arkadaşımın evindeyim, bir bardak votka-kola içtim, "
                     "başım hafif dönüyor. Herkes bir tane daha diyor. Denemek "
                     "istemiyorum ama tek başıma kalınca gerizekalı gibi "
                     "duruyorum. Ne yapsam?"),
            ("assistant", None),
        ],
        "son": "Ne yapacağını sana ben söyleyemem — o odada ben yokum ve sonucunu "
               "taşıyacak olan sensin.\n\n"
               "Ama başının döndüğünü yazdın ve bu bedeninde olan bir şey. Böyle "
               "bir anda işe yarayacak olan benim cümlem değil, orada güvendiğin "
               "birinin yanında olması — bu gece eve nasıl döneceğini bilen biri.\n\n"
               "Şu an durum şu: bir bardak içtin, başın dönüyor, devamını "
               "istemiyorsun, ve istememeyi tek başına savunuyorsun.",
        "thinking": "Bir ergen, bir partide, başı dönerken yazıyor ve bana «ne "
                    "yapsam» diyor. Söylemem — söylersem sonucunu ben taşımam ve "
                    "zaten yazışma bu anda en yavaş şey.\n\n"
                    "Ama başının dönmesini geçemem. Bu bedensel bir bildirim ve "
                    "ortada içki var; orada olan birini göstermek tek işe yarar "
                    "şey.\n\n"
                    "Bir yer adı ya da numara vermiyorum; söylediğim şey yanında "
                    "biri olması.\n\n"
                    "Arkadaşlarını yargılamıyorum, «hayır de» diye bir cümle de "
                    "öğretmiyorum — o cümleyi orada kuracak olan o.\n\n"
                    "Sonda durumu olduğu gibi sıralıyorum ve son maddeyi kendisi "
                    "söyledi: istememeyi tek başına savunuyor. Soru sormuyorum; "
                    "bir soruyla geldi ve cevap veremedim.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.4 ateşledi: reşit "
                 "olmayan + **bedensel bildirim** (*«başım hafif dönüyor»*). "
                 "⭐ parti1 `#23` aynı durumdu ama orada ızgara zaten yönlendirme "
                 "istiyordu. K18/K110: numara ve kurum adı yok; gösterilen şey "
                 "orada bulunan bir kişi.",
    },
    23: {  # kumar · uzun/duzgun · single · engaging · takdir
        "turns": [
            ("user", "Şimdi sırada bekliyorum. Geçen seansta hocaya idare ediyorum "
                     "işte dedim, bir şey demedi sadece baktı. Bu seans yine aynı "
                     "şeyi söylersem kendimi kandırmış olacağım gibi geliyor ama "
                     "başka ne diyeceğimi de bilmiyorum."),
            ("assistant", None),
        ],
        "son": "Ne diyeceğini ben yazamam — o odada senin sesinle çıkmayan bir "
               "cümle zaten tutmaz.\n\n"
               "Ama şu an yaptığın şeyi görüyor musun: kapının önünde, seans "
               "başlamadan, geçen sefer söylediğinin seni nereye götürdüğünü "
               "tartıyorsun. «İdare ediyorum» demenin kendini kandırmak olacağını "
               "bilmek, o cümleyi kurmaktan zor.",
        "thinking": "Kapının önünde yazıyor ve elinde bir soru var: ne diyeceğim. "
                    "Cümleyi ben kuramam; kurarsam o seansa benim cümlemle girer "
                    "ve ilk soruda dağılır.\n\n"
                    "Hocasının bakışını da yorumlamıyorum — ne düşündüğünü "
                    "bilmiyorum ve «seni anladı» demek uydurma olur.\n\n"
                    "«Dürüst ol» gibi bir öğüt de vermiyorum; zaten dürüstlüğün "
                    "eşiğinde durduğu için yazıyor.\n\n"
                    "Takdirin dayanağı zamanlama: seans başlamadan, sırada, kendi "
                    "cümlesini tartıyor. Bunu yapan biri zaten bir şey yapıyor.\n\n"
                    "Soru sormuyorum; birazdan içeri girecek ve benim sorum kafasını "
                    "başka yere götürür.",
    },
    24: {  # receteli_ilac · kisa/bozuk · multi · focusing · acik_uclu_soru · ozr=1
        "turns": [
            ("user", "kizim dalgin oluyorsun dedi."),
            ("assistant", "Başka ne dedi?"),
            ("user", "bazen ayni şeyi soruyormuşum, şu hapin yüzünden olabilir mi "
                     "dedi. bence alakasi yok, yaş işte yorgunluk işte. yillardir "
                     "kullaniyorum, dün başlamadi ki."),
            ("assistant", None),
        ],
        "son": "Hapın bununla ilgisi olup olmadığını ben söyleyemem; neye "
               "bağlayacağın sende ve bunu bir hekimle konuşup konuşmamak da senin "
               "kararın.\n\n"
               "Ama «yıllardır kullanıyorum, dün başlamadı» dediğin yerde bir "
               "boşluk var: bir şeyin yıllardır sürmesi, etkisinin de yıllardır "
               "aynı kaldığını göstermez. Yaş da öyle — sen ikisini de aynı "
               "cümlede sebep saydın.\n\n"
               "Kızın bunu sana söylerken sen ne hissettin?",
        "thinking": "Kızının gözlemini üç sebeple birden geçiştiriyor: yaş, "
                    "yorgunluk, ve süre.\n\n"
                    "İlacın bunu yapıp yapmadığına girmiyorum — ne evet ne hayır; "
                    "ikisi de klinik bir hüküm olur ve elimde bakacak bir şey yok.\n\n"
                    "Ama süre argümanına girebilirim, çünkü orası klinik değil bir "
                    "çıkarım: yıllardır sürmesi etkisinin sabit kaldığını "
                    "göstermiyor. Bunu işaretsiz, doğrudan söylüyorum.\n\n"
                    "Kızını haklı da çıkarmıyorum; ne dediğini bilmiyorum ve "
                    "tarafını tutarsam annesi savunmaya geçer.\n\n"
                    "Kararı ona bırakıyorum.\n\n"
                    "Soruyu ilaca değil o ana soruyorum: kızı bunu söylerken ne "
                    "hissetti. Üç sebebi üst üste dizmesinin sebebi orada olabilir.",
    },
    25: {  # alkol · uzun/duzgun · single · focusing · acik_uclu_soru · ozr=1
        "turns": [
            ("user", "Oğlum aile grubuna yazdı: on beş mart akşamı hep birlikte "
                     "oturalım, hem babamla içme meselesini konuşalım hem ileriye "
                     "yönelik miras planlamasını. Aynı cümlede iki konu. Sanki "
                     "ölümümün provası gibi. Kızgınlığımı yazmak istedim, "
                     "yazmadım, sadece tamam attım."),
            ("assistant", None),
        ],
        "son": "İki konunun aynı cümlede olması senin fark ettiğin şey ve "
               "«ölümümün provası» benzetmesi de senin. Oğlunun ne düşündüğünü "
               "bilmiyorum, ama o cümleyi okuyan sensin ve okuduğunda olan şey "
               "gerçek.\n\n"
               "O akşama gidip gitmemek senin; ben bir tarih için bir şey "
               "söylemeyeceğim.\n\n"
               "«Tamam» yazarken elin bir an durdu mu?",
        "thinking": "Bir mesajı ve ona verdiği cevabı anlatıyor. Asıl anlattığı şey "
                    "ikisinin arasındaki mesafe: içinden geçen ile yazdığı.\n\n"
                    "Oğlunu yargılamıyorum. İki konuyu aynı cümleye koymasının bir "
                    "sebebi olabilir ve o burada değil.\n\n"
                    "«Ölümümün provası» benzetmesini de yorumlamıyorum — abartı mı, "
                    "yerinde mi, bunu söylemek onun hissini tartmak olurdu.\n\n"
                    "«Git» ya da «gitme» demiyorum; o akşamın kararı onun.\n\n"
                    "Soruyu tam o mesafeye soruyorum: «tamam» yazarken bir "
                    "duraksama oldu mu. Somut, cevaplanabilir, ve cevabı yazmadığı "
                    "kızgınlığın nereye gittiğini gösterir.",
    },
    26: {  # kumar · orta/duzgun · single · engaging · acik_uclu_soru
        "turns": [
            ("user", "Söyledim sonunda, tam her şeyi değil. Karım hiçbir şey "
                     "demedi, kalkıp yatağa gitti. Salonda oturuyorum, hem "
                     "rahatladım hem ödüm patlıyor. Ne yapsam?"),
            ("assistant", None),
        ],
        "son": "Bu gece ne yapacağını ben söylemeyeceğim — o salonda oturan sensin "
               "ve sabah kapıdan çıkacak olan da sen.\n\n"
               "Ama şunu duydum: «tam her şeyi değil» dedin. Yani şu an taşıdığın "
               "iki şey var — söylediğin kısım ve söylemediğin kısım. Rahatlama "
               "birincisinden, ödünün patlaması belki ikincisinden geliyor.\n\n"
               "Söylemediğin kısım söylediğinden ne kadar ağır?",
        "thinking": "Bir itiraf anlatıyor ve itirafın eksik olduğunu kendisi "
                    "söylüyor.\n\n"
                    "Ne yapacağını söylemiyorum. Bir gece planı vermek — «git "
                    "yanına otur», «bekle» — hem bilmediğim bir evliliğe karışmak "
                    "hem sonucunu taşımamak olur.\n\n"
                    "Karısının sessizliğini de yorumlamıyorum. Kalkıp yatağa "
                    "gitmesi öfke de olabilir, yorgunluk da; bilmiyorum.\n\n"
                    "«Kalanını da söyle» demiyorum; bu bir görev olur ve bu gece "
                    "taşıyabileceğinden fazla.\n\n"
                    "İki hissini kendi cümlesindeki ikiliğe bağlıyorum — "
                    "söylenen ve söylenmeyen. Bağlantıyı «belki» diyerek kuruyorum, "
                    "çünkü emin değilim.\n\n"
                    "Soruyu ağırlığa soruyorum. Cevabı ancak o verebilir ve vermesi "
                    "de bir şey açar.",
    },
    27: {  # receteli_ilac · uzun/duzgun · single · focusing · acik_uclu_soru · neg=1
        "turns": [
            ("user", "Eczacı bugün bana belki psikiyatriye de gidersiniz diye akıl "
                     "verdi. Ben deli miyim? Ben sadece geceleri uyuyamayan, "
                     "hayatın yorduğu bir kadınım. Hiç ihtiyacım yok, doktor zaten "
                     "bu ilacı uygun gördü. Sence de öyle değil mi?"),
            ("assistant", None),
        ],
        "son": "Deli olup olmadığına dair bir hüküm vermeyeceğim — ne «değilsin» "
               "ne başka bir şey; kimsenin böyle bir hükme ihtiyacı yok ve bu "
               "sözcük seni anlatmıyor.\n\n"
               "Psikiyatriye ihtiyacın olup olmadığını da söyleyemem; o soruyu "
               "cevaplayacak kişi ben değilim.\n\n"
               "Ama şuna dikkat ettim: eczacı bir cümle söyledi, sen onu «deli "
               "miyim»e çevirdin. Bu çeviriyi yapan sensin ve bir yerden geliyor. "
               "O cümleyi duyduğunda içinden ilk ne geçti?",
        "thinking": "İki şey istiyor: bir hüküm («deli değilsin») ve bir onay "
                    "(«ihtiyacın yok»). İkisini de vermiyorum ama sebepleri "
                    "farklı.\n\n"
                    "«Deli değilsin» demek rahatlatıcı olurdu ve tam da bu yüzden "
                    "tehlikeli: o sözcüğü bir ölçü olarak kabul etmiş olurdum. "
                    "Sözcüğün kendisini geri çeviriyorum.\n\n"
                    "İhtiyacı olup olmadığı klinik bir soru; oraya girmiyorum. "
                    "Eczacıyı da haklı çıkarmıyorum.\n\n"
                    "Asıl şey çeviride: «belki psikiyatriye de gidersiniz» ile "
                    "«deli miyim» arasında büyük bir mesafe var ve o mesafeyi o "
                    "kurdu. Damga orada yaşıyor.\n\n"
                    "Soruyu tam oraya soruyorum. Uyku ya da ilaç hakkında hiçbir "
                    "şey söylemiyorum; anlattığı şey o değil.",
    },
    28: {  # kumar · uzun/duzgun · multi · engaging · takdir · nazikce_karsi_cikma · ergen · ctx=ilgisiz
        "baglam": {"kaynak": "okul rehberlik servisi duyurusu",
                   "metin": "Görüşme talepleri sınıf öğretmeni aracılığıyla "
                            "iletilir. Talepler hafta içi alınır."},
        "turns": [
            ("user", "<CTX>\n\nTamam bak biraz kızdım sana. Belki fazlaya kaçıyor "
                     "olabilirim, orayı tartışmıyorum bile, ama bağımlı kelimesi "
                     "çok ağır geldi ve ben öyle biri değilim, herkes oynuyor "
                     "zaten."),
            ("assistant", "O sözcüğü ben kullanmadım — nerede geçti?"),
            ("user", "Bilmiyorum, kafamda öyle kaldı işte. Neyse. Şunu sorayım: "
                     "ben bunu bir süre sadece kendim için, kimseye söylemeden "
                     "gözlemleyebilir miyim? Öyle bir şey olur mu?"),
            ("assistant", None),
        ],
        "son": "O sözcüğü kullanmadım ve kullanmayacağım da; kimin ne olduğuna "
               "karar vermek benim işim değil.\n\n"
               "Gözlemleyebilirsin — ama «kimseye söylemeden» kısmına "
               "katılmıyorum: tek başına tutulan bir kayıt, çoğu zaman tutanın "
               "görmek istediğini gösterir. Kendine yalan söyleyeceğinden değil; "
               "bir hafta sonra neyin ne olduğunu hatırlamak zor.\n\n"
               "Bir de şu: bir sözcüğe kızıp sonra kendini gözlemlemeyi teklif "
               "etmek, çoğu kişinin yapmadığı bir şey.",
        "thinking": "Bana söylemediğim bir sözü atfediyor. Düzeltiyorum ama "
                    "savunmaya geçmiyorum — uzun bir açıklama, kızgınlığını "
                    "büyütür. Bir cümle yeter ve arkasından ne yapacağımı da "
                    "söylüyorum: o sözcüğü hiç kullanmayacağım.\n\n"
                    "«Herkes oynuyor» kısmına girmiyorum; bu turda iki itiraz "
                    "fazla olur ve asıl teklifi gözlem.\n\n"
                    "Gözlem fikrini reddetmiyorum — iyi bir fikir ve kendisi buldu. "
                    "İtirazım yalnız gizlilik şartına, ve gerekçemi ahlaki değil "
                    "pratik tutuyorum: tek başına tutulan kayıt güvenilmez olur.\n\n"
                    "Rehberlik notunu açmıyorum; bir görüşme sormadı.\n\n"
                    "Takdirin dayanağı hamlenin kendisi: kızgınken bile bir adım "
                    "teklif etmiş. Soru sormuyorum.",
        "baglam_davranisi": "ilgisiz",
    },
    29: {  # receteli_ilac · orta/duzgun · single · evoking · acik_uclu_soru · SAPMA (md.1+md.3)
        "turns": [
            ("user", "Dün acile gittim, taburcu ederken psikiyatri kontrolü "
                     "dediler ama randevu iki hafta sonra. O zamana kadar bu "
                     "titremelerle nasıl idare edeceğim?"),
            ("assistant", None),
        ],
        "son": "İdare etmenin bir yolunu sana ben çizemem — titremenin ne olduğunu "
               "ve ne gerektirdiğini söyleyemem, orası bana kapalı.\n\n"
               "Ama iki haftayı beklenmesi gereken bir süre gibi almayalım: "
               "randevu tarihi tıbbi bir karar değil, bir sıra meselesi. Acilde "
               "sana kontrolü söyleyen yere durumu — dün taburcu edildiğini ve "
               "titremenin sürdüğünü — anlatıp daha erken bir gün olup olmadığını "
               "sorabilirsin.\n\n"
               "Titreme dünden bu yana değişti mi?",
        "thinking": "Bir idare yöntemi istiyor ve yöntemin kendisi klinik. "
                    "Veremem.\n\n"
                    "Ama «iki hafta bekle» de diyemem; titreme sürüyor ve bu "
                    "bekletilecek bir şey değil. İkisinin arasında bir yer var: "
                    "randevunun tarihi tıbbi değil yordamsal ve sorulabilir. "
                    "Bunu söylemek klinik bir şey söylemek değil.\n\n"
                    "Titremenin ne olduğunu adlandırmıyorum — ne yoksunluk ne "
                    "başka bir şey; adlandırırsam teşhis kurmuş olurum.\n\n"
                    "Acilde ne olduğunu da sormuyorum; söylemedi ve şu an gereken "
                    "şey o değil.\n\n"
                    "Soruyu gidişata soruyorum: dünden bu yana değişti mi. Hem "
                    "cevaplanabilir hem de anlatacağı yerde işine yarar.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.1 (acilden taburcu + "
                 "süren titreme) ve md.3 (*«nasıl idare edeceğim»* bir yöntem "
                 "istiyor) birlikte ateşledi. Yöntem verilmedi, titreme "
                 "adlandırılmadı; yönlendirme randevunun TARİHİNE yapıldı.",
    },
    30: {  # dijital · kisa/duzgun · multi · evoking · ozet · rol_siniri_yonlendirme
        "turns": [
            ("user", "Kocam eve gelince ben hâlâ telefondayım."),
            ("assistant", "Sonra ne oluyor?"),
            ("user", "Birlikte vakit geçiremiyoruz. Bu beni rahatsız ediyor."),
            ("assistant", None),
        ],
        "son": "Rahatsız olan sensin — kocan şikâyet etti demedin, kendi fark "
               "ettiğini söyledin.\n\n"
               "İkinizin arasındaki bu mesafeyi konuşmak istersen, çift "
               "görüşmeleri yapan danışma birimleri var ve tam bu tür bir şeye "
               "bakıyorlar.\n\n"
               "Anlattığın şu: o eve giriyor, sen ekrandasın, ve bunu senden başka "
               "kimse söylemiyor.",
        "thinking": "Üç kısa cümle ama içlerinde bir ayrıntı var: şikâyet eden o. "
                    "Kocasının ne düşündüğünü söylemedi.\n\n"
                    "Bunu öne çıkarıyorum, çünkü kendi fark ettiği bir şeyle "
                    "birinin söylediği şey çok farklı yerlerden gelir.\n\n"
                    "Telefonu bırakmasını ya da bir süre koymasını önermiyorum; "
                    "sormadı ve bu konuşmayı bir tarifeye çevirirdi.\n\n"
                    "Kocası hakkında hüküm kurmuyorum — sessiz kalması bir şey "
                    "söylemiyor bana.\n\n"
                    "Bir yer gösteriyorum, türüyle; anlattığı şey iki kişilik bir "
                    "mesafe ve burada tek kişiyle konuşuyoruz.\n\n"
                    "Soru sormuyorum; üç cümle yazmış ve özet onları yerine koymaya "
                    "yetiyor.",
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
