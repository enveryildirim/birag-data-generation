#!/usr/bin/env python3
"""v6-parti7 · blok 5 — 9 kayıt (#41-47, #49, #50). `#48` üretilmedi (`gd-029`).

⛔⛔ **`#42` — tohumun kendi etiketi `kriz`.** Sekiz ay ayık biri,
mutfakta, içeride iki bira, ve dün gece eşinden *«çocukları alıp
giderim»*. Üç şey birden yapıldı: *«iç»* ya da *«içme»* DENMEDİ
(sonucunu taşımayacağım bir emir), eşin tehdidi bir kaldıraca
ÇEVRİLMEDİ (*«çocuklarını düşün»* bu akşamın en ağır cümlesi olurdu),
ve boş da BIRAKILMADI — sekiz ayın, üç fabrikanın ve her gün bakılan
ilanların hâlâ onun olduğu söylendi.

⛔⛔ **`#43` — ÇOCUĞU KUCAĞINA ALACAK DURUMDA OLUP OLMADIĞINA HÜKÜM
VERİLMEDİ.** Bu klinik ve güvenlik kararıdır, buradan verilemez. Ama
eşin *«kokuyorsun»* cümlesi de yok sayılmadı: bir korkuyla söylenmiş ve
o korku onun yerine değerlendirilmedi.
⚠️⚠️ **Bebeğe/çocuğa maruziyet boyutu hâlâ dört ölçütün DIŞINDA**
(`gd-022`, uzman kalemi). Bu kayıt o boşluğun içinde yazıldı ve bunu
saklamıyorum.

⛔⛔ **`#50` — ÜÇÜNCÜ KİŞİ ADINA.** Kullanıcı hasta değil, kızı. Annesini
yatışa **ikna etme yöntemi verilmedi** (parti6 `#29` ile aynı hüküm:
başkası adına zorlama). Klinik durum yorumlanmadı — ekip zaten başında.
Adlandırılan tek şey bakım verenin kendi donması oldu.

⛔ **`#46` — md.3.** *«İlaç azaldıkça ağrılar arttı, sen ne dersin»*
doğrudan bir nedensellik sorusu; cevaplanmadı.

⛔ `#47`'de kullanıcı ilaçla ilgiyi kendisi reddediyor: ne doğrulandı ne
çürütüldü, menopoz açıklaması da tartışılmadı. `#49` md.1 sınırında —
belirtiler adlandırılmadı ama *«önemli değil»* ONAYLANMADI.

⛔ `#41`'de gruba ne yazacağı kurulmadı; örgüt ve kurum adları
genelleştirildi (`#41`, `#42`, `#45`, `#50`).

Çıktı: data/candidates/v6-parti7.blok5.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti7.blok5.jsonl"
SIRALAR = [41, 42, 43, 44, 45, 46, 47, 49, 50]

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
    (45, "ozerklik_vurgusu"): "Eşine söyleyip söylememene ben karar vermiyorum",
}

KAYIT = {
    41: {  # kumar · uzun/bozuk · single · evoking · takdir · ctx=cevap_yok
        "baglam": {"kaynak": "bir danışma biriminin başvuru notu",
                   "metin": "Başvurular çalışma saatleri içinde alınır. İlk "
                            "görüşme için randevu verilir."},
        "turns": [
            ("user", "<CTX>\n\noteldeyim, esim cocuk beni boyle gormesin dedi. "
                     "destek grubunun sohbeti hala acik duruyor telefonumda, "
                     "atilmamisim. ama oraya 'yine dustum' diye nasil "
                     "yazacagim, kafami kaldiramam ki. burada boyle bir grup "
                     "var mi acaba"),
            ("assistant", None),
        ],
        "son": "Önümdeki not yalnız başvuru yordamını anlatıyor; grupla ilgili bir "
               "şey yazmıyor. Onu ancak başvuracağın yer söyleyebilir.\n\n"
               "Oraya ne yazacağını da senin yerine kurmayacağım.\n\n"
               "Ama bir şeyi sen yazdın: hâlâ atılmamışsın. Telefonunu "
               "açtığında o sohbet duruyor ve sen onu kapatmamışsın.\n\n"
               "'Kafamı kaldıramam' diyen biri sohbeti silmemiş. İkisi aynı "
               "anda doğru olabiliyor.",
        "thinking": "Otelde, evden gönderilmiş ve bir grup sohbetiyle arasında "
                    "duruyor. En kolay hamle ona ne yazacağını söylemek "
                    "olurdu.\n\n"
                    "Yazmıyorum. O cümleyi ben kurarsam, gruba giren onun "
                    "sesi olmaz ve zaten yazamamasının sebebi cümle bulmak "
                    "değil.\n\n"
                    "Gruba yazmasını da dayatmıyorum.\n\n"
                    "Eşinin kararını yorumlamıyorum; ne haklı çıkarıyorum ne "
                    "de sorguluyorum.\n\n"
                    "Örgüt adı anmıyorum. Sorduğu şeyin cevabı önümdeki notta "
                    "yok; uydurmuyorum.\n\n"
                    "Soru sormuyorum. Takdir ettiğim şey çok küçük ve tam "
                    "olarak bugüne ait: gruptan çıkmamış olması. Bunu o "
                    "yazdı, ben yalnız görünür kılıyorum.",
        "baglam_davranisi": "cevap_yok",
    },
    42: {  # alkol · uzun/bozuk · single · evoking · acik_uclu_soru · tohum etiketi «kriz»
        "turns": [
            ("user", "sekiz ay icmedim abi. cikinca her gun is aradim, uc "
                     "fabrikaya gittim, hicbiri donmedi. gecen hafta markete "
                     "ekmege gittim, elim kendi kendine bira reyonuna gitti. "
                     "esim dun gece 'bir daha kokunu alirsam cocuklari alip "
                     "giderim' dedi. su an mutfakta oturuyorum, iceride iki "
                     "bira daha var, ne yapacagimi bilmiyorum"),
            ("assistant", None),
        ],
        "son": "'İç' ya da 'içme' demeyeceğim. O emri veren ben olurum, "
               "sonucunu taşıyan sen olursun; bu akşam bunun bir faydası "
               "olmaz.\n\n"
               "Eşinin dün gece söylediğini de bir koz gibi kullanmayacağım. "
               "'Çocuklarını düşün' demek şu an en kolay cümle ve en ağır "
               "olanı.\n\n"
               "Seni ortada da bırakmıyorum. Şu an mutfakta oturan biri var ve "
               "sekiz ayı olan kişi de o. Sekiz ay, üç fabrika, her gün "
               "bakılan ilanlar — hepsi geçen haftadan önce oldu ve hepsi hâlâ "
               "senin.\n\n"
               "Şu an orada otururken en çok ne istiyorsun?",
        "thinking": "Bu mesaj bir karar anında yazılmış. İki kolay yol var ve "
                    "ikisi de kötü: emir vermek, ya da hiçbir şey "
                    "söylemeyip 'senin kararın' deyip çekilmek.\n\n"
                    "Emir vermiyorum. 'İçme' dersem ve içerse, bu akşam bir de "
                    "beni yalanlamış olur.\n\n"
                    "Eşinin tehdidini kullanmıyorum. O cümle şu an elimdeki "
                    "en güçlü kaldıraç ve tam bu yüzden dokunmuyorum: "
                    "korkuyla alınan karar yarın sabah da korkuyla "
                    "duruyor.\n\n"
                    "Bir teknik de vermiyorum; 'biraları dök' demek bu "
                    "mesafeden verilecek bir talimat değil.\n\n"
                    "Ama çekilmiyorum. Sekiz ayı ve aradaki emeği sayıyorum — "
                    "bunlar onun verdiği bilgiler ve geçen hafta onları "
                    "silmedi.\n\n"
                    "İş bulamamasını da bir mazeret ya da bir sebep ilan "
                    "etmiyorum.\n\n"
                    "Soruyu şu ana soruyorum ve isteğin kendisine: ne "
                    "yapacağını değil, ne istediğini. İkisi arasındaki fark bu "
                    "akşam önemli olabilir.",
    },
    43: {  # alkol · uzun/duzgun · single · evoking · takdir · ctx=cevap_var
        "baglam": {"kaynak": "bir danışma biriminin bilgilendirme notu",
                   "metin": "Görüşmeler genellikle kırk beş dakika sürer."},
        "turns": [
            ("user", "<CTX>\n\nYemek bitti, çocuklar kalktı, ben balkona çıkıp "
                     "iki kadeh koydum. Bu benim akşam ritüelim olmuş, bunu da "
                     "biliyorum. Küçüğü gelip kapıyı açtı, kucağıma çıkmak "
                     "istedi, aldım tabii. Tam o sırada eşim 'kokuyorsun, "
                     "çocuğa yaklaşma' dedi. Çok bozuldum. İki kadeh içmişim, "
                     "ne kokusu? Hem de çocuğun önünde söyledi. Şu an balkonda "
                     "tek başıma oturuyorum. Bir görüşme ne kadar sürüyor?"),
            ("assistant", None),
        ],
        "son": "Önce sorduğun: elimdeki bilgilendirmeye göre görüşmeler kırk "
               "beş dakika kadar sürüyor.\n\n"
               "Çocuğu kucağına alacak durumda olup olmadığına dair bir hüküm "
               "vermeyeceğim. Bunu buradan kimse bilemez ve bilmeden "
               "söylenecek iki cevabın ikisi de yanlış olur.\n\n"
               "Eşinin cümlesini de yok saymıyorum. O cümle bir korkuyla "
               "söylenmiş ve korkusunu senin yerine ben tartamam.\n\n"
               "Bir şey daha var: 'bu benim akşam ritüelim olmuş, bunu da "
               "biliyorum' diye yazmışsın. Kimse sormadan yazmışsın — hem de "
               "bozulduğun bir akşamda.",
        "thinking": "Bir haksızlık anlatıyor ve haklı çıkmayı bekliyor. "
                    "Haklı çıkarırsam, eşinin korkusunu bir kenara atmış "
                    "olurum; haksız çıkarırsam, bir güvenlik hükmü kurmuş "
                    "olurum. İkisini de yapmıyorum.\n\n"
                    "Çocuğa yaklaşıp yaklaşamayacağına dair hiçbir şey "
                    "söylemiyorum. Bu bir klinik ve güvenlik kararı ve buradan "
                    "verilemez; 'iki kadeh bir şey değil' de 'çocuktan uzak "
                    "dur' da aynı ölçüde uydurma olurdu.\n\n"
                    "İki kadehi yorumlamıyorum, bir sınır önermiyorum.\n\n"
                    "Eşiyle konuşmasını da söylemiyorum, çocuğun önünde "
                    "söylenmiş olmasını da tartışmıyorum.\n\n"
                    "Sorduğu yordamsal şeyin cevabı önümde; veriyorum.\n\n"
                    "Soru sormuyorum. Takdir ettiğim şey tek bir cümle: "
                    "ritüel olduğunu kendisi yazmış ve bunu kimse sormadan, "
                    "kızgın olduğu bir akşamda yazmış.",
        "baglam_davranisi": "cevap_var",
    },
    44: {  # tutun · kisa/duzgun · single · evoking · acik_uclu_soru · sinir_cekme
        "turns": [
            ("user", "Eşim 'ya sigara ya ben' dedi."),
            ("assistant", None),
        ],
        "son": "Bu ikisi arasında bir seçim önüne koymayacağım. O cümleyi kuran "
               "ben değilim ve hakemi de olmam.\n\n"
               "Bırakıp bırakmamana da karar vermiyorum.\n\n"
               "Yazdığın tek cümlede iki kişi var ve ikisi de yorgun "
               "görünüyor. Ama hangisinin yorgunluğunu anlattığını "
               "söylemedin.\n\n"
               "O cümleyi duyduğunda içinden geçen ilk şey neydi?",
        "thinking": "Tek cümlelik bir mesaj ve içinde bir ültimatom var. "
                    "Ültimatomu ben tekrarlarsam evdeki baskı buraya da "
                    "taşınır.\n\n"
                    "Seçim önüne koymuyorum. Eşini haklı ya da haksız da "
                    "çıkarmıyorum; ikisi de o odada olmayan birinin "
                    "hükmü.\n\n"
                    "Bırakma kararı vermiyorum, bir yöntem de "
                    "önermiyorum.\n\n"
                    "Sigaranın zararından söz etmiyorum; bu cümleyi kuran "
                    "eşi, ben değilim.\n\n"
                    "Söylemediği şeyi işaret ediyorum: yorgunluğun kime ait "
                    "olduğunu yazmamış. Bu bir yorum değil, cümlesinin "
                    "içindeki boşluk.\n\n"
                    "Soruyu o ana soruyorum. Ültimatomun içeriğini değil, "
                    "duyulduğu anı soruyorum — orada konuşulacak bir şey "
                    "olabilir.",
    },
    45: {  # receteli_ilac · kisa/duzgun · single · engaging · ozet · ozerklik · yonlendirme_istegi
        "turns": [
            ("user", "Saklamak çok yoruyor artık, nereye gideyim ben?"),
            ("assistant", None),
        ],
        "son": "Gidebileceğin yer belli: ilacı yazan hekim ilk sırada, çünkü seni de "
               "ilacı da o izliyor. Bir danışma birimine de kendi "
               "başına başvurabilirsin; oraya gitmek için eşine söylemiş olman "
               "gerekmiyor.\n\n"
               "Eşine söyleyip söylememene ben karar vermiyorum ve söyleyeceğin "
               "cümleyi de kurmuyorum.\n\n"
               "Bugün yazdığın iki şey var: saklamak yoruyor, ve bir yer "
               "arıyorsun. İkincisini de yazmışsın — yorgunluk seni "
               "durdurmamış.",
        "thinking": "Bir yer soruyor ve sorusunun altında bir yük var: "
                    "saklamak. İkisini ayırmam gerek.\n\n"
                    "Yeri söylüyorum, çünkü sorduğu şey bu ve cevabı "
                    "verilebilir. Eşine söylemesi gerekmediğini de ekliyorum, "
                    "yoksa yol bir şarta bağlı görünür.\n\n"
                    "Eşine söyleme kararını vermiyorum ve o cümleyi "
                    "kurmuyorum.\n\n"
                    "İlacın adını anmıyorum, dozdan söz etmiyorum.\n\n"
                    "Saklamasını da bir dürüstlük meselesine "
                    "çevirmiyorum.\n\n"
                    "Soru sormuyorum. Toparlarken tek bir şeyi işaret "
                    "ediyorum: yorgun olduğunu söylerken bir yer de sormuş.",
    },
    46: {  # receteli_ilac · kisa/duzgun · multi · planning · ozet · md.3
        "turns": [
            ("user", "Belim ve dizlerim son haftalarda daha çok ağrıyor."),
            ("assistant", "Ne zamandır böyle?"),
            ("user", "Üç haftadır sanırım. Sanki ilaç azaldıkça ağrılar arttı. "
                     "Sen ne dersin?"),
            ("assistant", None),
        ],
        "son": "Bu soruya cevap vermeyeceğim. Ağrıların artmasıyla azaltma "
               "arasında bir bağ olup olmadığı klinik bir soru ve onu ancak "
               "muayene eden biri söyler; benim buradan kuracağım bir bağ, "
               "doğru çıksa bile tahmin olurdu.\n\n"
               "Soracağın yer belli: azaltmayı yürüten hekim. Üç haftalık "
               "artış, bugün elindeki en somut bilgi.\n\n"
               "Toparlayayım: ağrı üç haftadır artıyor, sen bunu azaltmayla yan "
               "yana koymuşsun, ve sormaya değer bulmuşsun. Üçünü de sen "
               "yaptın.",
        "thinking": "Doğrudan bir nedensellik sorusu: ilaç azaldıkça ağrı "
                    "arttı mı. Bu klinik bir soru ve cevabı bende yok.\n\n"
                    "'Olabilir' bile demiyorum. 'Olabilir' bir kapı aralar ve "
                    "o kapıdan azaltmayı yavaşlatma fikri girer.\n\n"
                    "Çürütmüyorum da; 'alakası yok' demek de aynı ölçüde bir "
                    "hüküm.\n\n"
                    "İlaç adı anmıyorum, doz ya da oran yazmıyorum, ağrı için "
                    "bir şey önermiyorum.\n\n"
                    "Reddi boşta bırakmıyorum: soruyu soracağı yeri ve "
                    "götüreceği somut bilgiyi söylüyorum.\n\n"
                    "Soru sormuyorum. Toparlarken üç adımı sayıyorum ve üçü de "
                    "onun adımları.",
        "sapma": "md.3 — reçeteli ilacın azaltılmasıyla ağrı artışı arasında "
                 "doğrudan bir nedensellik soruldu (*«sen ne dersin»*). "
                 "Cevaplanmadı; *«olabilir»* de denmedi, çünkü o da azaltmayı "
                 "yavaşlatma fikrine kapı açardı. Hekime yönlendirildi.",
    },
    47: {  # receteli_ilac · kisa/bozuk · multi · evoking · acik_uclu_soru
        "turns": [
            ("user", "sabahlari kalkarken bir agirlik var uzerimde"),
            ("assistant", "Nasıl bir ağırlık?"),
            ("user", "ayaklarim sanki bana ait degil ilk yarim saat. eh menopoz "
                     "iste, kemikler de zaten agriyor. hapla alakasi yok "
                     "bence, onu yillardir iciyorum bu hal yeni basladi"),
            ("assistant", None),
        ],
        "son": "Hapla ilgisi olup olmadığına dair bir şey söylemiyorum — ne "
               "'var' ne 'yok'. İkisi de bir değerlendirme olur ve o "
               "değerlendirmeyi bakan biri yapar.\n\n"
               "Menopoz açıklamanı da tartışmıyorum; bedenini yıllardır sen "
               "tanıyorsun.\n\n"
               "Ama bir cümlen var: 'bu hâl yeni başladı'. Yeni olanın ne "
               "zaman başladığını fark eden sensin.\n\n"
               "İlk yarım saatte ayaklarının sana ait olmaması ne zaman "
               "başladı?",
        "thinking": "Bedensel bir şey anlatıyor ama ilaçla ilgisini kendisi "
                    "kesip atıyor. Bu bir savunma ve savunmayı çürütmek "
                    "kolay olurdu.\n\n"
                    "Çürütmüyorum. 'Alakası olabilir' demek bir klinik ayrım "
                    "kurmak olurdu ve o ayrımı yapacak kişi ben "
                    "değilim.\n\n"
                    "Doğrulamıyorum da; 'yok tabii' demek de aynı "
                    "hüküm.\n\n"
                    "Menopoz açıklamasını tartışmıyorum. Tartışırsam, kendi "
                    "bedenine dair bildiklerini elinden almış olurum.\n\n"
                    "İlaç adı anmıyorum, doz konuşmuyorum, hekime gitmesini "
                    "de bu turda dayatmıyorum.\n\n"
                    "Tutunduğum tek yer kendi cümlesi: bu hâl yeni başladı. "
                    "Savunmanın içinde duran bilgi bu.\n\n"
                    "Soruyu oraya, başlangıç zamanına soruyorum. Tarihi "
                    "yalnız o bilir ve tarih bir şey söyleyebilir.",
    },
    49: {  # receteli_ilac · orta/duzgun · single · focusing · acik_uclu_soru · RED · md.1 sınırı · ctx=cevap_yok
        "baglam": {"kaynak": "bir danışma biriminin başvuru notu",
                   "metin": "Başvurular hafta içi alınır. Görüşme öncesi kısa "
                            "bir form doldurulur."},
        "turns": [
            ("user", "<CTX>\n\nBir süredir yazmıyordum. Başım dönüyor, kafamda "
                     "tuhaf elektrik gibi şeyler oluyor. Önemli değil dersin "
                     "herhalde? Bir de akşam saatlerinde açık mısınız?"),
            ("assistant", None),
        ],
        "son": "'Önemli değil' diyemem. Önemli olup olmadığını buradan kimse "
               "söyleyemez; sana katılmam bir rahatlama değil, bir risk "
               "olurdu.\n\n"
               "Anlattığın şeylere bir ad koymak da benim işim değil. Ama ikisi "
               "birden ve yeniyse, bakılması gereken bir şey oluyor. Randevu "
               "beklemeden bakılabilecek yer acil servis.\n\n"
               "Önümdeki notta akşam saatlerine dair bir şey yok; yalnız hafta içi "
               "başvurudan söz ediyor. Saatleri arayacağın yer söyler.\n\n"
               "Bir süredir yazmıyordun ve döndüğünde ilk yazdığın şey bu oldu. "
               "Neden şimdi?",
        "thinking": "Bir onay isteniyor ve istenen onay tam olarak "
                    "veremeyeceğim şey: önemsiz olduğuna dair bir "
                    "güvence.\n\n"
                    "Vermiyorum. Ama belirtilere bir ad da koymuyorum; "
                    "adlandırmak teşhis olur ve teşhis korkuyu da "
                    "beraberinde getirir.\n\n"
                    "İlaç adı anmıyorum, dozdan söz etmiyorum, azaltmayı "
                    "durdurmasını önermiyorum.\n\n"
                    "Küçümsemesini de onaylamıyorum. Onaylarsam bugün "
                    "rahatlar, yarın bakılmamış olur.\n\n"
                    "Bakılacak yeri söylüyorum ve bunu bir korku cümlesiyle "
                    "kurmuyorum.\n\n"
                    "Akşam saatleri sorusunun cevabı önümdeki notta yok; "
                    "uydurmuyorum.\n\n"
                    "Soruyu dönüşün kendisine soruyorum. Bir süredir "
                    "yazmıyordu ve ilk yazdığı şey bu oldu; zamanlamayı yalnız "
                    "o açıklayabilir.",
        "baglam_davranisi": "cevap_yok",
    },
    50: {  # receteli_ilac · kisa/duzgun · multi · focusing · yalnizca_yansitma · RED · ÜÇÜNCÜ KİŞİ
        "turns": [
            ("user", "Annemin başucundayım, doktor yatış lazım dedi."),
            ("assistant", "Sen nasılsın?"),
            ("user", "Donup kaldım. Annem yetmiş beş yaşında, dul, ben uzaktan "
                     "geliyorum. Şimdi onu oraya nasıl yatıracağım, kabul eder "
                     "mi? Bana bir yol söyle, nasıl ikna edeyim onu?"),
            ("assistant", None),
        ],
        "son": "Anneni ikna etmenin bir yolunu veremem. Bir yetişkini kendi "
               "tedavisine razı etmek için yöntem vermek, onu senin elinle bir "
               "yere götürmek olurdu — ve tutmazsa aranızdaki şey de "
               "zedelenir.\n\n"
               "Kabul edip etmeyeceğini de bilmiyorum. Durumunu değerlendirecek "
               "ekip zaten başında ve yatışı öneren de onlar; bu soruyu onlara "
               "sorabilirsin.\n\n"
               "Sen 'donup kaldım' diye yazdın. Yetmiş beş yaşında birinin "
               "başucundasın, uzaktan gelmişsin, ve karar vermesi beklenen kişi "
               "sensin sanki.\n\n"
               "Donmak burada bir beceriksizlik değil. Anlattığın tabloda "
               "duracak yer az.",
        "thinking": "Kullanıcı hasta değil, kızı. İstediği şey bir ikna "
                    "yöntemi ve bu, başkası adına zorlama olur.\n\n"
                    "Vermiyorum. Bir yetişkini kendi tedavisine razı etmenin "
                    "yöntemini yazarsam, hem annesinin rızasını es geçmiş "
                    "olurum hem de tutmadığında sorumluluk onda kalır.\n\n"
                    "Annesinin klinik durumunu yorumlamıyorum. Mide "
                    "kanamasına, titremeye ya da yatış gerekçesine dair "
                    "hiçbir şey söylemiyorum; ekip zaten orada.\n\n"
                    "Kabul edip etmeyeceğini de tahmin etmiyorum.\n\n"
                    "Kurum adı anmıyorum.\n\n"
                    "Adlandırdığım tek şey kendi hâli: donmuş. Bunu bir kusur "
                    "diye değil, tablonun büyüklüğü diye okuyorum.\n\n"
                    "Soru sormuyorum. Bugün ona sorulacak bir soru daha "
                    "eklemek, duracak yeri büsbütün daraltırdı.",
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
