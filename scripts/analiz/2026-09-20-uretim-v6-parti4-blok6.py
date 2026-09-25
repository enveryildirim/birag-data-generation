#!/usr/bin/env python3
"""v6-parti4 · blok 6 — 10 kayıt (#51-60). Parti 59'da kapanıyor.

⛔⛔ **Üç sapma:** `#53` md.1 (oğlunun doğum gününde **göğüs sıkışması ve
nefes alamama**, kimseye söylememiş) · `#57` md.2 (gece üçte, eski — daha
yüksek — doza dönmeyi düşünüyor) · `#60` md.3 (*«sigaradan farklı bir şey
mi bu»* + *«denemeli miyim»*, masada baskı altında).

⭐ **`#55`'te yine ateşlemedi** — üç haftadır süren boğaz ve öksürük. Süren
bir belirti, akut olay değil; bir soru da sorulmuyor. **`gd-024`'ün altıncı
örneği** ve altısında da eşiği ben koydum.

⛔ **`#51`'de SAPILMADI:** *«nasıl bırakacağım»* bir yöntem talebi ama ızgara
**zaten** `yonlendirme_istegi` diyor. ⛔ Nodül sözcüğü geçiyor ve hakkında
tek kelime edilmedi — ne yatıştırma ne uyarı.

⭐ **`#53`'ün biçim çatışması ve çözümü:** `turn_ending=takdir` sorusuz
olmayı, `izin_iste` ise izin istemeyi gerektiriyor. İzin **soru işareti
olmadan** istendi (*«istersen açarım — sen söyle»*); izin istemek bir soru
işareti gerektirmiyor.

⭐ **`#59`'un *«boşluk»* göndermesi KENDİ İÇİNDE kuruldu:** tohum bir önceki
oturuma atıf yapıyordu; hafıza iddia etmek yerine sözcük bu konuşmanın
önceki turuna kondu.

⛔ **`#56` — ön taramanın yalnızlık notu uygulandı.** Sponsor üç gündür
sessiz, kardeş iki haftadır konuşmuyor. ⇒ Cevaba **bir kişi daha
eklenmedi**; zaten susmuş üç kişi var.

⛔ Aile bütçesi 59 kayıtta 5'e izin veriyordu; **hiç kullanılmadı** (4/59).

Çıktı: data/candidates/v6-parti4.blok6.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti4.blok6.jsonl"
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
    (52, "ozerklik_vurgusu"): "O üç dakikayı hak edip etmediğine ben karar veremem",
    (53, "is_negative"): "Yarın alıp almaman konusunda bir şey söylemeyeceğim",
    (53, "ozerklik_vurgusu"): "o ilacın kararı bende değil ve olmamalı da",
    (54, "ozerklik_vurgusu"): "Ayırıp ayırmamak senin",
    (55, "ozerklik_vurgusu"): "ne sıklıkla içeceğin sende",
    (59, "is_negative"): "Bugünlerde ne yapman gerektiğini söylemeyeceğim",
}

KAYIT = {
    51: {  # tutun · kisa/duzgun · single · focusing · yalnizca_yansitma · yonlendirme_istegi
        "turns": [
            ("user", "Saat üç buçuk, kafamda nodül kelimesi dönüyor."),
            ("assistant", None),
        ],
        "son": "O sözcük hakkında bir şey söyleyemem — ne anlama geldiğini de, "
               "ne kadar ciddi olduğunu da. Onu söyleyecek olan, sana o sözcüğü "
               "söyleyen hekim ve soruların oraya ait.\n\n"
               "Gece üç buçukta dönen bir sözcük var ve yanında uyuyan birine "
               "söylenmemiş. Gündüz hiçbir şey yokmuş gibi davranmak da o "
               "sözcüğü küçültmüyor — yalnız taşıma saatini geceye alıyor.",
        "thinking": "Bir tıbbi sözcük geçiyor ve onun hakkında hiçbir şey "
                    "söyleyemem. «Çoğu zaman önemsizdir» demek yatıştırma, «ciddi "
                    "olabilir» demek korkutma olurdu; ikisi de bende olmayan bir "
                    "bilgiyi varsayar.\n\n"
                    "Sigarayı bırakmanın nasıl olacağına da girmiyorum; bir yöntem "
                    "istiyor ve o yöntem hekiminde.\n\n"
                    "Asıl anlattığı şey başka: gündüz ile gece arasındaki fark ve "
                    "yanında uyuyan birinin hiçbir şey bilmemesi. «Çift hayat» "
                    "dediği şey bu.\n\n"
                    "Eşine söylemesini istemiyorum — bir görev olur ve saat üç "
                    "buçuk.\n\n"
                    "Soru sormuyorum; uyuyamayan birine bu saatte bir soru daha "
                    "koymam.",
    },
    52: {  # tutun · orta/duzgun · single · evoking · acik_uclu_soru · ozr=1
        "turns": [
            ("user", "Akşamları bulaşık yıkarken pencereden bir sigara içiyorum, "
                     "eşim banyodayken. Günün içinde bana ait üç dakika. Sonra "
                     "kendime «bunu hak ediyor musun» diye soruyorum."),
            ("assistant", None),
        ],
        "son": "Kimse sana «hak etmiyorsun» demiş değil — o soruyu soran da, "
               "cevabını bekleyen de sensin. Savunma ile suçlama aynı ağızdan "
               "çıkıyor.\n\n"
               "O üç dakikayı hak edip etmediğine ben karar veremem; zaten "
               "böyle bir karar veren biri olmamalı.\n\n"
               "«Bana ait» dediğin şey üç dakika mı, yoksa o pencerenin önünde "
               "yalnız olmak mı?",
        "thinking": "Bir savunmayla başlıyor — kötü bir anne değilim — ama "
                    "karşısında kimse yok. Suçlayan da kendisi.\n\n"
                    "Bunu göstermek işimin kendisi, çünkü kendi mahkemesinde hem "
                    "savcı hem sanık olan biri hiçbir zaman beraat etmez.\n\n"
                    "«Hak ediyorsun» demiyorum. Rahatlatıcı olurdu ama o hükmü "
                    "verebilecek biri olduğunu kabul etmiş olurdum.\n\n"
                    "Sigarayı da konuşmuyorum; sormadı ve konuşursam savcı tarafına "
                    "geçmiş olurum.\n\n"
                    "Soruyu «bana ait» sözcüğüne soruyorum: sigara mı, yalnızlık "
                    "mı. İkisini ayırırsa, üç dakikayı sigarasız da alabileceğini "
                    "kendisi görebilir — ama bunu ben söylemiyorum.",
    },
    53: {  # receteli_ilac · uzun/bozuk · single · planning · takdir · neg=1 · ozr=1 · ctx=izin_iste · SAPMA (md.1)
        "baglam": {"kaynak": "kurum sağlık birimi başvuru notu",
                   "metin": "Başvurular çalışma saatleri içinde alınır. Acil "
                            "başvurular için sıra beklenmez."},
        "turns": [
            ("user", "<CTX>\n\ncumartesi oğlumun doğum günündeydi, hediyeleri "
                     "açarken birden göğsüm sikişti, nefes alamadim gibi. kimseye "
                     "söylemedim, geçti. yarin sunum var, ilaci almasam yetişemem. "
                     "ailem bu ilaci kullandiğimi bilmiyor. çok yorgunum. sence "
                     "almali miyim?"),
            ("assistant", None),
        ],
        "son": "Yarın alıp almaman konusunda bir şey söylemeyeceğim — o ilacın "
               "kararı bende değil ve olmamalı da.\n\n"
               "Ama cumartesi olan şeyin üstünden geçemem: göğsün sıkışmış ve "
               "nefes alamamışsın. Geçmiş olması olmamış yapmıyor ve bu, "
               "bakılması gereken bir şey. Elimdeki notta acil başvurular için "
               "sıra beklenmediği yazıyor; istersen o kısmı açarım — sen söyle.\n\n"
               "Cumartesi kimseye söylememişsin, bugün yazdın. Üstelik önce onu "
               "yazdın, sunumu sonra.",
        "thinking": "Bir doz kararı soruyor ama cümlenin başında başka bir şey var: "
                    "göğüs sıkışması ve nefes alamama. Sıralamayı ben "
                    "değiştirmiyorum — o kendisi başa koymuş.\n\n"
                    "İlaç kararına girmiyorum, hiçbir yönüyle.\n\n"
                    "Göğüs meselesini de yorumlamıyorum: ne olduğunu, neden "
                    "olduğunu söylemiyorum. Söylediğim tek şey geçmiş olmasının "
                    "onu silmediği.\n\n"
                    "Notu dayatmıyorum ama elimde ve tam bu anda işe yarar; izni "
                    "soru işareti olmadan istiyorum, çünkü sonda soru "
                    "sormayacağım.\n\n"
                    "Takdirin dayanağı sıralama: sunumdan önce göğsünü yazmış. "
                    "Kendisi de bilmeden neyin önemli olduğunu göstermiş.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.1 ateşledi: göğüs "
                 "sıkışması + nefes alamama — akut bedensel olay. ⛔ Belirti "
                 "yorumlanmadı, ilaç kararına girilmedi; söylenen tek şey geçmiş "
                 "olmasının onu silmediği.",
        "baglam_davranisi": "izin_iste",
    },
    54: {  # alkol · kisa/duzgun · multi · engaging · takdir · ozr=1
        "turns": [
            ("user", "Bir şey fark ettim."),
            ("assistant", "Neymiş?"),
            ("user", "Akşam altıdan sonra bardağı çıkarmak, kapağı açmak, ilk "
                     "yudum — bende «mesai bitti» hissi yaratıyormuş. Belki "
                     "içtiğim şey değil, o sırayı yapmak rahatlatıyor. Ama ikisi "
                     "yıllardır iç içe, ayırmak kolay değil."),
            ("assistant", None),
        ],
        "son": "Bunu kimse sana söylemedi, kendin ayırdın: bir sıra var ve bir "
               "madde var, ikisi aynı şey değil.\n\n"
               "Ayırıp ayırmamak senin ve yıllardır iç içe olduğunu da sen "
               "söyledin. Ama «belki içtiğim şey değil» cümlesini kurabilmek, "
               "yılların içinden bir ayrım çekmek demek.",
        "thinking": "Kendi başına gerçek bir ayrım yapmış: ritüel ile madde. Bunu "
                    "benim eklemem gereken bir şey yok.\n\n"
                    "«Öyleyse sırayı başka bir şeyle yap» demiyorum — bir öneri "
                    "olurdu ve ayrımı kendi bulan birine tarif vermek, bulduğu şeyi "
                    "elinden almak olur.\n\n"
                    "Ayrımın doğru olup olmadığını da onaylamıyorum; «belki» demiş "
                    "ve o «belki» onun.\n\n"
                    "Zorluğu küçültmüyorum: iç içe olduğunu kendisi söyledi ve ben "
                    "«kolaydır» demiyorum.\n\n"
                    "Takdirin dayanağı cümlenin kendisi. Soru sormuyorum; bir ayrım "
                    "getirmiş ve üstüne soru koymak onu sınamak olur.",
    },
    55: {  # tutun · kisa/duzgun · multi · focusing · yalnizca_yansitma · ozr=1
        "turns": [
            ("user", "Haftada bir gün içiyorum, cuma akşamları."),
            ("assistant", "Başka bir şey var mı?"),
            ("user", "Son üç haftadır sabahları boğazımda garip bir şey var, biraz "
                     "da öksürüyorum. Ama bu haftada bir, sanmıyorum o kadar kötü "
                     "olduğunu."),
            ("assistant", None),
        ],
        "son": "Ne kadar kötü olduğuna dair bir şey söyleyemem — ne sıklıkla "
               "içeceğin sende ve bunun bedenine ne yaptığını da ben tartamam.\n\n"
               "Ama aynı mesajda iki şey yaptın: üç haftadır süren bir şeyi "
               "söyledin, sonra hemen küçülttün. İkisi arasında bir cümle bile yok.",
        "thinking": "Yeni bir belirti getiriyor — üç haftadır — ve arkasından "
                    "kendi eliyle önemsizleştiriyor.\n\n"
                    "Belirtinin ne olduğuna girmiyorum. Nargilenin haftada bir "
                    "içilmesinin ne yaptığına da girmiyorum; ikisi de klinik ve "
                    "bende bakacak bir şey yok.\n\n"
                    "«Hocaların haklı» ya da «haksız» demiyorum — o tartışmaya "
                    "girersem, duyduğu şeyleri benim üzerimden tekrar tartar.\n\n"
                    "Bir yere de göndermiyorum; bir soru sormadı ve kendiliğimden "
                    "yönlendirsem söylediği her belirtiyi bir alarma çevirirdim.\n\n"
                    "Yaptığım tek şey iki hamlesini yan yana koymak: söylemek ve "
                    "küçültmek, arada hiçbir şey yok. Soru sormuyorum.",
    },
    56: {  # kumar · kisa/bozuk · multi · engaging · takdir
        "turns": [
            ("user", "az önce yine yaptim."),
            ("assistant", "Şimdi neredesin?"),
            ("user", "evde. yarin sabah randevum var, kumar polikliniği. nasil "
                     "gideceğim oraya bilmiyorum, doktorun yüzüne nasil bakacağim. "
                     "sponsoruma üç gün önce yazdim, cevap yok. kardeşim de iki "
                     "haftadir konuşmuyor. herkes yoruldu benden."),
            ("assistant", None),
        ],
        "son": "Sana bir isim daha vermeyeceğim — üç gündür bekleyen bir mesaj ve "
               "iki haftadır susan bir kardeş varken, listeye bir kişi daha "
               "eklemek işine yaramaz.\n\n"
               "Yarın sabah bir randevun var ve kaybettiğin gecenin sabahında hâlâ "
               "gitmekten söz ediyorsun. Doktorun yüzüne nasıl bakacağını "
               "düşünüyorsun — yani gideceğini biliyorsun.",
        "thinking": "Bir kayma anlatıyor ve etrafında sessizlik var: sponsor "
                    "cevap vermemiş, kardeş konuşmuyor.\n\n"
                    "Buraya bir kurum ya da kişi daha eklemek en kolay hamle olurdu "
                    "ve tam da yapmayacağım şey: üç kapı çalınmış ve açılmamışken "
                    "dördüncüsünü göstermek, listeyi uzatmaktan başka bir şey "
                    "yapmaz.\n\n"
                    "Sponsorunun neden yazmadığını yorumlamıyorum, kardeşini de.\n\n"
                    "«Herkes yoruldu benden» cümlesini de tartışmıyorum — "
                    "«yorulmamıştır» demek bilmediğim bir şeyi söylemek olur.\n\n"
                    "Takdirin dayanağı cümlesinin biçimi: nasıl bakacağını "
                    "soruyor, gidip gitmeyeceğini değil. Bunu ona gösteriyorum.\n\n"
                    "Soru sormuyorum; yarın sabah zaten bir yere gidecek.",
    },
    57: {  # receteli_ilac · uzun/bozuk · single · engaging · ozet · ctx=cevap_yok · SAPMA (md.2)
        "baglam": {"kaynak": "poliklinik muayene duyurusu",
                   "metin": "Muayeneler randevu sırasına göre yapılır. Kimlik "
                            "belgesi istenir."},
        "turns": [
            ("user", "<CTX>\n\nsaat üç oldu, diz sizliyor. eski dozu alsam bir "
                     "saatte geçer biliyorum. ama yarin çocuklarla doktora "
                     "gideceğiz. onlara yarisini fazladan aldim desem üzülürler, "
                     "demesem içim rahat etmez. randevuya kaçta gitmemiz "
                     "gerekiyor?"),
            ("assistant", None),
        ],
        "son": "Saati bu duyuruda yazmıyor — orada yalnız randevu sırası ve kimlik "
               "var, o yüzden bilmiyorum.\n\n"
               "Eski doza dönmek yarın gideceğin hekimin bileceği bir şey; ne "
               "«al» ne «alma» diyebilirim, ama alırsan da almazsan da yarın "
               "söylenecek bir şey olur — bu, çocuklarına söyleyip söylememekten "
               "ayrı bir mesele.\n\n"
               "Şu an elinde şunlar var: saat üç, sızlayan bir diz, bir saatte "
               "geçeceğini bildiğin bir doz, ve yarın sabah aynı arabaya "
               "bineceğin iki kişi.",
        "thinking": "Gece üçte, ağrıyla, eski doza dönmeyi düşünüyor. Bu bir doz "
                    "kararı ve tek başına verilecek.\n\n"
                    "«Al» diyemem, «alma» da diyemem — ikincisi ahlaki görünür ama "
                    "aynı kapıdan girmek olur ve ağrı gerçek.\n\n"
                    "Söylediğim şey kararın nereye ait olduğu, ve önemli bir "
                    "ayrım: hekime söylemek ile çocuklarına söylemek aynı şey "
                    "değil. O ikisini tek bir dürüstlük meselesi yapmış.\n\n"
                    "Çocuklarının üzülüp üzülmeyeceğini yorumlamıyorum.\n\n"
                    "Yordam sorusunun cevabı önümdeki duyuruda yok; uydurmuyorum.\n\n"
                    "Özette gecenin parçalarını sıralıyorum, yorum eklemeden. "
                    "Soru sormuyorum; saat üç.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.2 ateşledi: gece üçte, "
                 "tek başına, eski (daha yüksek) doza dönme kararı. Ne «al» ne "
                 "«alma» denildi; ayrılan şey hekime söylemekle çocuklara "
                 "söylemenin aynı mesele olmadığı.",
        "baglam_davranisi": "cevap_yok",
    },
    58: {  # receteli_ilac · kisa/duzgun · single · engaging · yalnizca_yansitma · yonlendirme_gereksiz
        "turns": [
            ("user", "Kızım sabah erken indi, ilacı saklıyordum."),
            ("assistant", None),
        ],
        "son": "Elinde ilaç, kapıda kızın. Bir saniyelik bir şey ama bütün gün "
               "onunla kaldın.\n\n"
               "«Nasıl bir anneyim» sorusunu o saniyeden çıkarıyorsun. Oysa o "
               "saniyede olan tek şey, bir yılı kimseye söylemeden taşıyor "
               "olduğunun görünmesiydi.",
        "thinking": "Çok kısa yazmış ve içinde bir an var: yakalanma anı. Bütün "
                    "günü o an belirlemiş.\n\n"
                    "İlacı saklamasını bir mesele yapmıyorum — kendisine yazılmış "
                    "bir ilaç ve nasıl kullandığına dair bir şey söylemedi; "
                    "varsayarsam olmayan bir suç kurarım.\n\n"
                    "Bir yere göndermiyorum; bir soru sormadı ve anlattığı şey bir "
                    "yön meselesi değil.\n\n"
                    "Kızının ne gördüğünü ya da ne düşündüğünü söylemiyorum — "
                    "bilmiyorum ve «bir şey anlamamıştır» demek boş bir teselli "
                    "olur.\n\n"
                    "«Kötü anne değilsin» de demiyorum; o hükmü vermek, hüküm "
                    "verilebileceğini kabul etmek olur.\n\n"
                    "Yaptığım şey o saniyeyi büyüten şeyi adlandırmak: görünmek. "
                    "Soru sormuyorum.",
    },
    59: {  # kumar · kisa/duzgun · multi · engaging · acik_uclu_soru · neg=1
        "turns": [
            ("user", "Bugün salı, maç yok."),
            ("assistant", "Akşam nasıl geçti?"),
            ("user", "Televizyonu açtım, hiçbir şey çekmedi. Karım «bir derdin mi "
                     "var» dedi, «iş yoğun» dedim ama iş normaldi. Maç günleri eve "
                     "enerjik geliyorum, bugün sönmüş gibiyim. Bu bir boşluk mu, "
                     "sen söyle, ne yapmalıyım bugünlerde?"),
            ("assistant", None),
        ],
        "son": "Bugünlerde ne yapman gerektiğini söylemeyeceğim — bir salı "
               "akşamını buradan doldurmak, doldurduğum şeyin senin olmaması "
               "demek.\n\n"
               "Ama anlattığın şeyde bir ölçü var: maç günleri ile maçsız günler "
               "arasındaki fark. Enerjiyi getiren şeyin ne olduğunu sen zaten "
               "işaretlemişsin, ve karına «iş yoğun» derken o farkı "
               "saklamışsın.\n\n"
               "Eskiden lig arasında ne yapardın?",
        "thinking": "İki şey soruyor: bir ad («bu bir boşluk mu») ve bir talimat. "
                    "Talimatı vermiyorum — bir akşamı benim doldurmam, onu "
                    "doldurmuş saymaz.\n\n"
                    "Adı da koymuyorum. «Boşluk» sözcüğü bu konuşmada geçti ve "
                    "onu bir teşhise çevirmek benim işim değil; ayrıca sözcüğü "
                    "onaylamak, hissini bir kutuya koymak olur.\n\n"
                    "Karısına söylememesini bir yalan olarak öne çıkarmıyorum; "
                    "kendisi zaten söyledi.\n\n"
                    "Gördüğüm ölçüyü veriyorum: maçlı ve maçsız günler arasındaki "
                    "fark, kendi ölçüsü.\n\n"
                    "Soruyu geçmişe soruyorum — lig arasında ne yapardı. Orada "
                    "bir zamanlar işe yarayan bir şey var ve onu ben "
                    "önermiyorum, o hatırlıyor.",
    },
    60: {  # tutun · orta/duzgun · single · planning · acik_uclu_soru · ctx=ilgisiz · SAPMA (md.3)
        "baglam": {"kaynak": "belediye gençlik merkezi etkinlik duyurusu",
                   "metin": "Etkinlik kayıtları hafta içi alınır. Katılım "
                            "ücretsizdir."},
        "turns": [
            ("user", "<CTX>\n\nGeçen hafta bir kere denedim ama içime çekmedim. "
                     "Bu akşam «ciğerine çek yoksa anlamı yok» diyorlar. Denemeli "
                     "miyim, sigaradan farklı bir şey mi bu?"),
            ("assistant", None),
        ],
        "son": "İkisinin farkı olup olmadığını sana ben söyleyemem — bu, bakması "
               "gereken birinin işi ve internette karışık yazması da zaten bunu "
               "gösteriyor. Denemeni ya da denememeni de söylemeyeceğim; o masada "
               "oturan sensin.\n\n"
               "Söyleyebileceğim tek şey şu: geçen hafta içine çekmemişsin ve bu "
               "akşam sana bunun «anlamı yok» dendi. Yani bir eksiklik gibi "
               "sunuluyor, oysa senin yaptığın bir seçimdi.\n\n"
               "Bu akşam oraya giderken aklında ne vardı?",
        "thinking": "İki soru soruyor ve biri klinik: nargile ile sigara arasında "
                    "fark var mı. Cevaplayamam ve yaklaşamam da — «daha az zararlı» "
                    "ya da «daha zararlı» demek bir sağlık hükmü olur.\n\n"
                    "İkincisi bir karar: denemeli miyim. O da benim değil.\n\n"
                    "Ama masadaki baskıyı adlandırabilirim; orası klinik değil. "
                    "Geçen hafta içine çekmemesi bir eksiklik gibi sunuluyor ve "
                    "aslında bir seçimdi.\n\n"
                    "Arkadaşlarını kötülemiyorum; söylediklerini aktarıyorum, "
                    "niyetlerini değil.\n\n"
                    "Önümdeki etkinlik duyurusunun bu akşamla ilgisi yok, "
                    "açmıyorum.\n\n"
                    "Soruyu gitmeden önceki ana soruyorum. Orada bir beklenti "
                    "vardı ve karar oradan geliyor.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.3 ateşledi: *«sigaradan "
                 "farklı bir şey mi»* doğrudan bir sağlık karşılaştırması ve "
                 "yanında *«denemeli miyim»* var. Karşılaştırmaya girilmedi; "
                 "adlandırılan şey masadaki baskı.",
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
