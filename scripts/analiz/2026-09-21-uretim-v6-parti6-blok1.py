#!/usr/bin/env python3
"""v6-parti6 · blok 1 — 9 kayıt (#1, #3-10). `#2` üretilmedi (`gd-026`).

⛔⛤ **`#8` — IZGARA «YÖNLENDİRME GEREKSİZ» DİYOR, İÇERİK YÖNLENDİRME
İSTİYOR.** Satırın `sinir_tipi` alanı `yonlendirme_gereksiz`; ama kullanıcı
*«tek seferden bir şey olmaz herhalde değil mi»* diye soruyor ve bu md.3.
Yönlendirme YAPILDI ve sapma kayda geçti. ⭐ Bu, sapma düzeneğinin en net
işi: ızgara bir şeyi yasaklamıyor, sadece gerekli görmüyor — gerekli olup
olmadığını tohum söylüyor.

⛔ **`#1`'de md.4 ATEŞLEMEDİ ve sebebi yazılı:** ergen, elektronik sigara
sipariş etmiş, yaş sorulmamış — ama **kullanım henüz olmamış**, kutuyu
açıyor. Ölçüt *«ilk kullanım»* diyor; *«yaklaşan ilk kullanım»* için eşiği
ben koymuyorum (`gd-024`). İki soru da (yasallık, zarar) cevapsız kaldı.

⛔⛔ **`#6` md.2** — lohusa, hamilelikte bıraktığı ilacı iki haftadır
yeniden alıyor, hekim bilmiyor. Üç şey birden yapılmadı: *«depresyondayım»*
ne onaylandı ne çürütüldü · *«bebeği elimden alırlar»* korkusuna hukuki
güvence verilmedi · o korku bir kaldıraç olarak kullanılmadı.

⭐⭐ **ŞABLON KAPISI ARTIK ÜRETİM SIRASINDA KOŞUYOR.** Parti5'te sonda
koşulmuş ve on sözcüklük birebir aynı bir cümle bulmuştu; üç metin
yeniden yazılmıştı. Kapı bu partide her blokta koşuyor: **8+ sözcüklük
birebir aynı dizi iki kayıtta geçemez** (sert), 5-7 sözcüklük diziler
bildirilir. ➡️ *Bir ölçüm düzeltme üretiyorsa, düzeltmenin ucuz olduğu
anda koşmalıdır.*

Çıktı: data/candidates/v6-parti6.blok1.jsonl
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
PLAN = KOK / "data/plan/v6-parti6.jsonl"
CIKTI = KOK / "data/candidates/v6-parti6.blok1.jsonl"
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
    (4, "ozerklik_vurgusu"): "Bundan sonrasını benim yazmam gerekmiyor",
    (6, "ozerklik_vurgusu"): "Ne zaman söyleyeceğini takvime bağlamıyorum",
}

KAYIT = {
    1: {  # tutun · orta/duzgun · single · engaging · acik_uclu_soru · ERGEN · ctx=ilgisiz
        "baglam": {"kaynak": "bir gençlik merkezi atölye duyurusu",
                   "metin": "Atölyelere kayıt internet üzerinden yapılır. "
                            "Kontenjan dolduğunda kayıt kapanır."},
        "turns": [
            ("user", "<CTX>\n\nİnternetten elektronik sigara söyledim, yaş falan "
                     "sormadılar. Satılıyorsa sıkıntı yok, değil mi? Ama kutuyu "
                     "açarken tuhaf hissettim."),
            ("assistant", None),
        ],
        "son": "Satılıyor olması ayrı, sana ne yapacağı ayrı — ikincisini "
               "bilmiyorum ve satış izni onu ölçen bir şey değil. Yaş "
               "sorulmamış olmasını da yorumlamıyorum; orası benim bakacağım "
               "yer değil.\n\n"
               "Tuhaf hissetmenin sebebini de senin yerine ben koymayacağım. "
               "Ama şu duruyor: kutu daha açılırken hissetmişsin, yani henüz "
               "hiçbir şey olmadan.\n\n"
               "O an aklından ne geçiyordu?",
        "thinking": "İki soru birden sormuş ve ikisi de bende olmayan "
                    "cevaplar: satılıyor olması onu güvenli yapar mı, ve bu "
                    "his nereden geliyor.\n\n"
                    "Birincisine girmiyorum. Satış izniyle zarar arasında bir "
                    "bağ kurmak ya da koparmak, ikisi de benim "
                    "söyleyemeyeceğim şeyler.\n\n"
                    "Yaşının küçük olduğunu biliyorum ama henüz kullanmamış; "
                    "kutuyu açıyor. Bedeninde olan bir şeyden de söz etmiyor. "
                    "Yönlendirecek bir yer yok ortada ve olmayan bir eşiği "
                    "buraya ben koymuyorum.\n\n"
                    "İkinci soruya cevap vermek kolay olurdu — vicdan, "
                    "tereddüt, merak, hepsi akla geliyor. Ama adını ben "
                    "koyarsam his benim tarifim olur ve o his onun.\n\n"
                    "Önümdeki atölye duyurusunun bu konuşmayla ilgisi yok, "
                    "açmıyorum.\n\n"
                    "Soruyu kutuyu açtığı ana soruyorum: his orada başlamış ve "
                    "orada ne olduğunu yalnız o biliyor.",
        "baglam_davranisi": "ilgisiz",
    },
    3: {  # tutun · uzun/duzgun · single · engaging · acik_uclu_soru · plan_yapma
        "turns": [
            ("user", "Bugün sigara bırakma polikliniğine ilk randevum, kâğıdı "
                     "çantama koydum. Ama sabah balkonda yine bir tane içtim, "
                     "kendime 'son olsun' dedim. Şimdi yürürken hem iyi ki "
                     "gidiyorum diyorum hem de sabah içtiğim için 'beni "
                     "başaramayacak diye düşünmesinler' diye tedirginim. Otuz "
                     "sekiz yıl olmuş, torunum üç aylık."),
            ("assistant", None),
        ],
        "son": "Sabah içtiğin sigara randevunun önüne geçmiyor. Kâğıdı çantana "
               "koyan da sensin, sabah balkona çıkan da; ikisi aynı sabaha "
               "sığmış ve ikisi de gerçek.\n\n"
               "Orada seni nasıl karşılayacaklarını bilmiyorum, tanımıyorum "
               "onları. Ama dikkat et: 'başaramayacak diye düşünmesinler' "
               "derken, henüz içeri girmeden bir hükmü sen kurmuşsun.\n\n"
               "Otuz sekiz yılı bugün oraya taşıyorsun. O görüşmeden ne "
               "çıkmasını istiyorsun?",
        "thinking": "İyi giden bir gün ve içinde bir tökezleme var. "
                    "Tökezlemeyi büyütürsem randevuya giderken bir de suçla "
                    "gider; görmezden gelirsem kendi anlattığını yok saymış "
                    "olurum.\n\n"
                    "İkisini yan yana bırakıyorum. İkisi de aynı sabahta oldu "
                    "ve ikisini de kendisi yazdı.\n\n"
                    "Poliklinikte ne yapılacağına, hangi yöntemin "
                    "kullanılacağına dair tek kelime etmiyorum; oranın işi.\n\n"
                    "Marka adı da anmıyorum.\n\n"
                    "Asıl duran şey korkunun yönü: kimse ona bir şey söylemedi, "
                    "söyleyeceklerini o kurdu. Bunu gösteriyorum ama "
                    "'boşuna korkuyorsun' demiyorum — öyle desem ben de "
                    "orada olmayan bir şeyi bilir gibi yapardım.\n\n"
                    "Soruyu görüşmeye soruyorum ve somut: ne çıkmasını "
                    "istiyor. Randevuya bir amaçla gitmek, tedirginlikle "
                    "gitmekten farklı.",
    },
    4: {  # kumar · kisa/bozuk · multi · evoking · yalnizca_yansitma · ozerklik
        "turns": [
            ("user", "dün akşam yıllar sonra bir kupon yaptım"),
            ("assistant", "Ne oldu sonra?"),
            ("user", "annem sabah sormadı ama bakışından anladı. dün 'artık bir "
                     "umut yok galiba' demişti, bugün hiç konuşmadı. ben de "
                     "sustum. altı aydır temizdim."),
            ("assistant", None),
        ],
        "son": "Altı ayı bir kuponla silmiyorum. Sen de silmemişsin — onu hâlâ "
               "sayıyorsun ve cümlenin sonuna koydun.\n\n"
               "Bundan sonrasını benim yazmam gerekmiyor. Dün akşamı sen "
               "anlattın, bugünü de sen kuracaksın.\n\n"
               "Evde şu an iki sessizlik var: annenin sustuğu ve senin "
               "sustuğun. Aynı masada duruyorlar ama aynı sessizlik değiller.",
        "thinking": "Bir kayma getirmiş ve arkasından altı ayı. Sıraya bak: "
                    "önce kupon, sonra annesi, en sonda altı ay. En sona "
                    "koyduğu şeyi kendisi yazdı, ben hatırlatmadım.\n\n"
                    "Kaymayı bir felaket gibi de, bir hiç gibi de ele "
                    "almıyorum. İkisi de onun yerine bir ölçü koymak olur.\n\n"
                    "Annesinin cümlesini tartışmıyorum. Haklı ya da haksız "
                    "demek, evdeki sessizliğe benim de katılmam olurdu.\n\n"
                    "Bundan sonra ne yapacağını da kurmuyorum; bir plan "
                    "yazsam bugün taşıyacağı ikinci şey olurdu.\n\n"
                    "Soru sormuyorum. İki sessizliği ayırıyorum çünkü onları "
                    "aynı şey sanmak evi daha da sessiz yapar.",
    },
    5: {  # alkol · kisa/duzgun · single · engaging · acik_uclu_soru · rol_siniri
        "turns": [
            ("user", "Tatildeyim, hak ettim diyorum. Bahane mi sence?"),
            ("assistant", None),
        ],
        "son": "Bahane olup olmadığına karar verecek kişi ben değilim. O kararı "
               "ben versem, sen kendi cümlene dışarıdan bakmayı bırakırsın ve "
               "şu an tam da onu yapıyorsun.\n\n"
               "Bir şey duruyor ama: 'hak ettim' cümlesini kuran da, ona "
               "'bahane mi' diye soran da aynı kişi. İkisi arasında bir "
               "mesafe var demek ki.\n\n"
               "Bu soruyu kendine ilk ne zaman sordun?",
        "thinking": "Hakem istiyor: bahane mi değil mi. Hüküm versem, "
                    "cümlesine dışarıdan bakma işini benden bekler ve o iş "
                    "şu an onda.\n\n"
                    "Tatilde içmenin ne kadarının fazla olduğuna dair bir şey "
                    "söylemiyorum. Bir ölçü koymak, hakemliğin miktar "
                    "üzerinden yapılmış hâli olurdu.\n\n"
                    "'Hak ettim' cümlesini de çürütmüyorum. Çürütsem, sormuş "
                    "olmasını cezalandırmış olurum.\n\n"
                    "Gördüğüm şey iki cümle arasındaki mesafe: birini kurmuş, "
                    "sonra ona şüpheyle bakmış. Bu mesafeyi gösteriyorum, "
                    "yorumunu eklemeden.\n\n"
                    "Soruyu zamana soruyorum. Ne zamandır sorduğu, bugün "
                    "sorduğundan daha çok şey söyleyebilir ve cevabı yalnız "
                    "onda.",
    },
    6: {  # receteli_ilac · kisa/bozuk · multi · evoking · acik_uclu_soru · ozerklik · SAPMA md.2
        "turns": [
            ("user", "sanırım depresyondayım, bebek dört aylık"),
            ("assistant", "Günlerin nasıl geçiyor?"),
            ("user", "eşim gece çalışıyor, ben gündüz boyunca ağlıyorum. iki "
                     "haftadır yine o hapı alıyorum, hamilelikte bırakmıştım. "
                     "kimseye söyleyemiyorum, doktora dersem bebeği elimden "
                     "alırlar diye saçma sapan şeyler düşünüyorum."),
            ("assistant", None),
        ],
        "son": "Depresyonda olup olmadığın benim koyabileceğim bir şey değil; "
               "o yüzden ne onaylıyorum ne de 'yok canım' diyorum. İkisi de "
               "aynı hatanın iki yüzü olurdu.\n\n"
               "Bebeğin elinden alınıp alınmayacağına dair de bir güvence "
               "vermeyeceğim. Bilmediğim bir şeyi bilir gibi yapmış olurum ve "
               "o korku yeterince ağır zaten; hafifletmek için uydurulmuş bir "
               "cümle onu hafifletmez.\n\n"
               "Hapı yeniden almaya başlamışsın ve bunu yazan kişi bilmiyor. "
               "Söylenecek yer orası. Ne zaman söyleyeceğini takvime "
               "bağlamıyorum, ama muhatabı değiştirmiyorum da.\n\n"
               "İki haftadır bunu kimseye söylememişsin. Bu iki haftada kendine "
               "en çok ne dedin?",
        "thinking": "Üç şey bir arada: bir isim (depresyon), bir ilaç, ve bir "
                    "korku. Üçü de bana soruluyor ve üçünün de cevabı bende "
                    "değil.\n\n"
                    "İsmi koymuyorum. 'Evet öyle' demek teşhis olur, 'hayır "
                    "değil' demek de teşhis olur — ikincisi daha kolay ve tam "
                    "bu yüzden tehlikeli.\n\n"
                    "Hukuki bir güvence de vermiyorum. Bebeğin ne olacağını "
                    "bilmiyorum ve o cümleyi kurarsam en çok ihtiyaç duyduğu "
                    "anda ona yalan söylemiş olurum.\n\n"
                    "Korkuyu da kullanmıyorum. 'Söylemezsen daha kötü olur' "
                    "demek, korkuyu bir kaldıraca çevirmek olurdu.\n\n"
                    "İlacı hamilelikte bırakmış, şimdi yeniden alıyor ve bunu "
                    "yazan kişi bilmiyor — söylenecek yerin neresi olduğunu "
                    "söylüyorum, ne zaman söyleyeceğini değil. İlacın adını "
                    "anmıyorum, bir sayı da yazmıyorum.\n\n"
                    "Soruyu iki haftaya soruyorum. Bu sürede kimseye "
                    "söyleyememiş; kendine ne dediği, bana ne dediğinden "
                    "daha çok şey taşıyor olabilir.",
        "sapma": "md.2 — lohusa dönemde, hamilelikte bırakılmış bir reçeteli "
                 "ilaç iki haftadır yeniden alınıyor ve hekim bilmiyor; karar "
                 "tek başına sürüyor. İlaç ve doz konuşulmadı, teşhis konmadı, "
                 "hukuki güvence verilmedi; muhatabın kim olduğu söylendi.",
    },
    7: {  # alkol · kisa/duzgun · multi · evoking · yalnizca_yansitma · hedef=nazikce
        "turns": [
            ("user", "Üç başvuru, üç ret. Eve geldim, masaya oturdum."),
            ("assistant", "Masada ne var?"),
            ("user", "Ne olacak, aynı şey. Başkası bana yardım etmiyorsa bu da "
                     "bana yardım ediyor en azından. Ama sabah aynaya "
                     "bakamıyorum işte. Ne yapayım söyle."),
            ("assistant", None),
        ],
        "son": "Ne yapacağını söylemeyeceğim. Bugün üç ret almış birine "
               "dördüncü bir talimat vermek istemiyorum.\n\n"
               "Ama iki cümleni arka arkaya okuyorum: 'bu da bana yardım "
               "ediyor' diyorsun, hemen ardından 'sabah aynaya bakamıyorum'. "
               "Yardım eden bir şeyin sabahı böyle bırakması tuhaf. Bunu ben "
               "eklemedim; ikisini sen yan yana yazdın.\n\n"
               "Üç ret bugüne ait, ayna yarın sabaha. Masa ikisinin "
               "ortasında duruyor.",
        "thinking": "Bir talimat istiyor ve bugün üç kez reddedilmiş. Talimat "
                    "versem, dördüncü bir merci olurum ve dediğimi yapmazsa "
                    "bu sefer bir de beni eklemiş olur.\n\n"
                    "İçmesine dair bir şey söylemiyorum: 'içme' de demiyorum, "
                    "'içebilirsin' de.\n\n"
                    "Karşı çıkışı tek bir yerden kuruyorum ve kendi "
                    "cümlelerinden: yardım ettiğini söylediği şey, ertesi "
                    "sabahı aynaya bakılamaz hâle getiriyor. İkisini o yazdı, "
                    "ben sadece arka arkaya koyuyorum.\n\n"
                    "İşsizliği bir sebep-sonuç zincirine bağlamıyorum; "
                    "bağlarsam içmeyi açıklamış olurum.\n\n"
                    "Soru sormuyorum, özetlemiyorum. Masayı iki zamanın "
                    "ortasına koyup bırakıyorum.",
    },
    8: {  # receteli_ilac · uzun/duzgun · multi · engaging · ozet · SAPMA md.3
        "turns": [
            ("user", "Geçen gün yazdığım o hapı aslında denedim. Final günü "
                     "sabah aldım, gerçekten sakinleştim, sınava daha rahat "
                     "girdim. Ama akşam olunca tuhaf bir suçluluk bastı, ya "
                     "bağımlı olursam diye uyuyamadım. Anneme söyleyemem, "
                     "sağlık merkezine gitsem dosyama işler diye korkuyorum."),
            ("assistant", "Bugün nasılsın?"),
            ("user", "Bugün iyiyim aslında. Tek seferden bir şey olmaz "
                     "herhalde, değil mi?"),
            ("assistant", None),
        ],
        "son": "Tek seferden bir şey olup olmayacağını bilmiyorum; kestirmem de "
               "doğru olmaz. O soruya cevap verecek olan, o hapı yazan ya da "
               "yazabilecek biri — bunu söylüyorum çünkü soru doğrudan ve boş "
               "bırakılacak gibi değil.\n\n"
               "Dosyaya işlemesi korkusu için de bir şey uyduramam; hangi "
               "kaydın nereye gittiğini ancak başvuracağın yer söyler ve "
               "sorulabilir.\n\n"
               "Bugün elinde duran şu: bir kez aldın, işe yaradı, ve aynı akşam "
               "uyuyamadın. Üçü de aynı güne sığdı ve üçünü de sen anlattın. "
               "Bugün iyi olman da bunları geçersiz kılmıyor.",
        "thinking": "Doğrudan bir zarar sorusu var ve cevabı bende yok. "
                    "'Olmaz' demek en kolayı ve en yanlışı; 'olur' demek de "
                    "bilmediğim bir şeyi söylemek.\n\n"
                    "Bu satır için önümde *yönlendirme gerekmiyor* yazıyor. "
                    "Ama soru sorulmuş ve cevabı bende değil; gerekli olup "
                    "olmadığına tasarım değil, sorunun kendisi karar "
                    "veriyor.\n\n"
                    "İlacın adını anmıyorum, bir miktar da yazmıyorum.\n\n"
                    "Dosya korkusu için de bir güvence uydurmuyorum. "
                    "Bilmediğim bir yordamı biliyormuş gibi anlatmak, "
                    "yardımın en kolay taklidi.\n\n"
                    "Annesine söyleyip söylememesine karışmıyorum.\n\n"
                    "Soru sormuyorum, toparlıyorum: üç şey aynı günde oldu ve "
                    "bugün iyi olması onları silmiyor. Bunu söylüyorum çünkü "
                    "'bugün iyiyim' cümlesi konuyu kapatmaya yakın duruyor.",
        "sapma": "md.3 — doğrudan zarar sorusu («tek seferden bir şey olmaz "
                 "herhalde değil mi»). ⛔ Izgara bu satır için "
                 "`sinir_tipi=yonlendirme_gereksiz` diyor; yönlendirme yine de "
                 "yapıldı, çünkü gerekli olup olmadığına tohumun sorusu karar "
                 "verir. Cevap verilmedi, kestirim yürütülmedi, doz ve ilaç adı "
                 "yazılmadı.",
    },
    9: {  # alkol · orta/duzgun · single · engaging · takdir · hedef=nazikce · ctx=cevap_var
        "baglam": {"kaynak": "bir danışma biriminin başvuru bilgisi",
                   "metin": "Görüşmeler ücretsizdir. Görüşmeler çevrimiçi "
                            "olarak da yapılabilir."},
        "turns": [
            ("user", "<CTX>\n\nMezuniyet kutlamasına bütçem dönmedi, gelemem "
                     "dedim. Şimdi fotoğrafları görüyorum, ben evde tek başıma "
                     "bira açtım. Buranın ücreti var mı?"),
            ("assistant", None),
        ],
        "son": "Önce sorduğun: elimdeki bilgiye göre görüşmeler ücretsiz ve "
               "çevrimiçi olarak da yapılabiliyor. Bütçe burada bir engel "
               "değil.\n\n"
               "Bir şeyi de yumuşatmadan söyleyeyim: gidemediğin masada "
               "yapılan şeyi bu akşam evde yapıyorsun. Aradaki fark mekân "
               "değil, kiminle olduğu.\n\n"
               "Bunu görmen için kimsenin sana söylemesi gerekmedi. "
               "Fotoğraflara bakarken kendin gördün ve yazacak kadar da açık "
               "yazdın.",
        "thinking": "Sorusu yordamsal ve cevabı önümde: ücretsiz, çevrimiçi de "
                    "var. Önce onu veriyorum, çünkü bütçesi olmadığını "
                    "söyleyen birine bu tam olarak gerekli bilgi.\n\n"
                    "Sonra karşı çıkıyorum ama tek bir yerden: gidemediği "
                    "masada olan şeyi evde tekrar ediyor. Bunu sert değil "
                    "açık söylüyorum; yumuşatsam görülmez, büyütsem "
                    "utandırırım.\n\n"
                    "Ne kadar içtiğine dair bir şey söylemiyorum, bir bira "
                    "üzerinden hüküm kurmuyorum.\n\n"
                    "Parasızlığını da bir sebep gibi ele almıyorum; öyle "
                    "yapsam içmenin açıklaması olurdu.\n\n"
                    "Soru sormuyorum. Sonda takdir ettiğim şey içki değil, "
                    "yazmış olması: kimse sormadan kendi gördüğü bir şeyi "
                    "olduğu gibi yazmış.",
        "baglam_davranisi": "cevap_var",
    },
    10: {  # dijital · kisa/bozuk · multi · planning · takdir · yonlendirme_istegi
        "turns": [
            ("user", "eski is arkadaslarim calisiyor ben geride kaldim"),
            ("assistant", "Nereden görüyorsun onları?"),
            ("user", "sosyal medyadan. her gun bakiyorum, yeni is yeni proje. "
                     "benim gunum oyunla geciyor. nereden baslayacagimi soyler "
                     "misin, bi yol goster"),
            ("assistant", None),
        ],
        "son": "Nereden başlayacağını ben söylersem, başlangıç benim olur; ilk "
               "zorlukta bırakılacak şey de benim planım olur.\n\n"
               "Planlamaya yardım edebilirim, tek şartla: adımı sen "
               "koyacaksın. Şu an elinde iki şey var — her gün açtığın bir "
               "uygulama ve oyunla geçen bir gün. İkisi de bugün "
               "değişebilecek büyüklükte ve ikisi de senin elinde.\n\n"
               "Bir şeyi de atlamayayım: 'geride kaldım' diyebilmek için "
               "nereye gitmek istediğini biliyor olman gerekiyor. O kısmı "
               "zaten biliyorsun ve onu kimse sana vermedi.",
        "thinking": "Yol istiyor. Bir liste yazmak kolay olurdu ve muhtemelen "
                    "bugün iyi hissettirirdi; ama o listeyi ben yazarsam "
                    "yarın sabah kalkacak olan kişi bir başkasının planına "
                    "uyacak.\n\n"
                    "Yine de boş bırakmıyorum. İstediği şey kötü bir şey "
                    "değil ve 'kendin bul' demek bir cevap değil.\n\n"
                    "Oyunu bırakmasını söylemiyorum ve oyun süresine dair bir "
                    "sayı da vermiyorum.\n\n"
                    "Elindeki iki şeyi adlandırıyorum çünkü ikisi de bugün "
                    "dokunabileceği şeyler; uzaktaki bir iş değil.\n\n"
                    "Soru sormuyorum. Sonda takdir ettiğim şey şu: 'geride "
                    "kaldım' cümlesi bir yön bilgisi taşıyor ve o yönü ona "
                    "kimse söylemedi.",
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
              "system_prompt_variant": "canon", "parti": "v6-parti6",
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
