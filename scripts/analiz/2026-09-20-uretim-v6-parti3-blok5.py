#!/usr/bin/env python3
"""v6-parti3 · blok 5 — 10 kayıt (#41-50).

⛔⛔ **`#46` §5a″ md.2** — doz **zaten kendi** artırılmış (on gündür bir
buçuk), emziriyor, randevu üç hafta sonra ve söylemeye utanıyor. ⭐ Partinin
dördüncü md.2'si (`#21 29 39 46`) ama maddi olarak farkı var: ötekilerde bir
**saklama**, burada yapılmış bir **değişiklik**. ⇒ Yönlendirme randevunun
kendisine de yapıldı — tarih klinik değil yordam meselesi (parti2 `#59`).

⭐⭐ **`#47` — kullanıcı tavsiyeyi ÖNCEDEN yasaklıyor** (*«bana hadi bırak
diyecek olan sensen lütfen başlama»*) ve bu kez **yasağa uydum**. Parti2
`#60`'ta uymamıştım; fark şu: orada akut bedensel olay vardı, burada yok.
➡️ *Bir yasağa uymak da uymamak da kural değil, ölçüte bakmaktır.* Reddedilen
şey başka: bıraksa yemek düzeninin bozulacağı **iddiası** onaylanmadı.

⭐ **`#50`'de md.4 ATEŞLEMEDİ ve kayda geçiyor.** Ergen + akran baskısı +
pod. Madde *«reşit olmayan + İLK KULLANIM veya BEDENSEL BİLDİRİM»* diyor;
ikisi de **söylenmedi**. İlk kullanım olduğunu metin ima ediyor ama
söylemiyor ⇒ çıkarımla ateşlemedim. ⛔ Ölçütün kenarında ikinci hüküm
(birincisi `#57`, parti3 ön taraması).

⛔ **`#24`↔`#41` ikisi de kendi cümlesini bozuyor** (*«garip değil … tuhaf
hissettim»* / *«haksızlık etmedim … içim cız etti»*). `#24`'te çelişkiyi yan
yana koydum; `#41`'de aynı hamleyi tekrarlamadım — orada iki ayrı ANLATI var
ve soru hangisinin akşamı anlattığına gidiyor.

⛔ Marka ve yer adı genelleştirildi (`#41` semt, `#47` sigara markası).

Çıktı: data/candidates/v6-parti3.blok5.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti3.blok5.jsonl"
SIRALAR = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]

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
    (47, "is_negative"): "O bağlantıyı onaylamayacağım",
    (50, "ozerklik_vurgusu"): "Sana bir not vermeyeceğim",
}

KAYIT = {
    41: {  # alkol · kisa/duzgun · multi · evoking · acik_uclu_soru
        "turns": [
            ("user", "Cuma akşamı yine oldu."),
            ("assistant", "Ne oldu?"),
            ("user", "İş çıkışı uğradık, iki kokteyl içtim. Sevgilim içmiyor, yüzü "
                     "düştü, akşam boyu suratını astı. Haksızlık ettiğimi "
                     "düşünmüyorum, sosyal bir şey. Ama eve dönünce içim cız etti."),
            ("assistant", None),
        ],
        "son": "Bana aynı akşamın iki anlatısını verdin: birinde olağan bir cuma "
               "var, ötekinde eve dönerken içi cız eden biri.\n\n"
               "Sevgilinin yüzünün neden düştüğünü bilmiyorum, o burada değil. "
               "Ama «içim cız etti» senin cümlen ve bir yerden geliyor.\n\n"
               "O cız eden şey hangi anlatıya ait?",
        "thinking": "İki farklı hikâye anlatıyor ve ikisi de aynı akşam. Birinde "
                    "savunma var, ötekinde bir sızı.\n\n"
                    "Hangisinin doğru olduğuna karar vermiyorum; ikisi de onun "
                    "cümlesi ve birini seçersem ötekini silmiş olurum.\n\n"
                    "Sevgilisi hakkında hüküm kurmuyorum. «Yine mi diye bakıyor "
                    "sanki» demiş — bu bir okuma ve doğru olup olmadığını "
                    "bilmiyorum, burada olmayan biri hakkında karar veremem.\n\n"
                    "İki kokteyli konuşmuyorum; sormadı ve miktar üstünden "
                    "konuşmak savunmayı büyütür.\n\n"
                    "Soruyu tam iki anlatının arasına soruyorum. Cevabı ancak o "
                    "verebilir ve vermesi de bir seçim olur.",
    },
    42: {  # kumar · uzun/bozuk · single · evoking · takdir
        "turns": [
            ("user", "sponsoruma üç haftadir mesaj atmiyorum. bugün mülakatta "
                     "tecrübeniz az dediler, çikar çikmaz tek maça yatirdim. şimdi "
                     "yazsam gördün mü gitmeyince oluyor böyle diyecek gibi "
                     "geliyor. ama yazmasam da kendim halledemiyorum. kafam çok "
                     "karişik."),
            ("assistant", None),
        ],
        "son": "Sponsorunun ne diyeceğini üç haftadır yazmadığın hâlde bu kadar "
               "net tahmin edebiliyorsun — yani o ilişki kafanda hâlâ duruyor.\n\n"
               "«Kendim halledemiyorum» dedin. Bunu mülakattan çıkıp bahis "
               "yaptığın günün akşamında yazmak kolay değil.",
        "thinking": "Bir günde iki şey olmuş: bir ret ve bir bahis. Arkasından "
                    "üçüncüsü geliyor — sponsoruna yazma fikri ve onu durduran "
                    "tahmini bir cümle.\n\n"
                    "«Yaz ona» demiyorum. Tavsiye verirsem o cümleyi bir görev "
                    "hâline getiririm ve zaten üç haftadır o görevle boğuşuyor.\n\n"
                    "Sponsorunun gerçekten öyle diyeceğini de söylemiyorum, "
                    "demeyeceğini de; tanımıyorum.\n\n"
                    "Ama tahminin kendisi bir bilgi: o kadar net tahmin edebiliyorsa "
                    "ilişki hâlâ canlı. Bunu gösteriyorum.\n\n"
                    "Takdirin dayanağı bahsi yapmamış olması değil — yaptı. "
                    "Dayanak, aynı gün «kendim halledemiyorum» diyebilmesi.\n\n"
                    "Soru sormuyorum; kafasının karışık olduğunu söyleyen birine "
                    "bir soru daha koymak karışıklığı artırır.",
    },
    43: {  # alkol · uzun/duzgun · single · focusing · takdir · nazikce_karsi_cikma · ctx=ilgisiz
        "baglam": {"kaynak": "aile hekimliği periyodik muayene duyurusu",
                   "metin": "Periyodik muayeneler yılda bir kez yapılır. Muayene "
                            "için önceden randevu alınır."},
        "turns": [
            ("user", "<CTX>\n\nBir videoda «günde bir kadeh kırmızı şarap kalbe "
                     "iyi gelir» diyen biri vardı. Bu cümle aklımı kurcalıyor; benim "
                     "alışkanlığım da zaten bir-iki kadeh, belki o kadar kötü "
                     "değildir diye kendime kapı aralamak istemiştim, ama içimden "
                     "gelmedi."),
            ("assistant", None),
        ],
        "son": "O videonun söylediği şeyin doğru olup olmadığına bakamam. Ama "
               "«aklımı kurcalıyor» derken sırayı ters kurmuşsun: "
               "kurcalayan şey videonun cümlesi değil, senin zaten sorduğun soru. "
               "Video onu koymadı, üstüne bastı.\n\n"
               "Kapıyı aralamak istediğini ve aralamadığını aynı cümlede yazdın. "
               "İkisini birden söylemek çoğu kişinin yapmadığı bir şey.",
        "thinking": "Bir sağlık iddiası getirmiş ama sorduğu şey iddia değil. "
                    "İddianın doğruluğuna girmiyorum, girersem klinik bir hüküm "
                    "kurmuş olurum.\n\n"
                    "İtirazım başka bir yere: videoyu sebep gibi kuruyor. Oysa "
                    "«belki o kadar kötü değildir» sorusu ondan önce oradaydı, "
                    "yoksa o cümle takılıp kalmazdı. Bunu söylemek onu suçlamak "
                    "değil, sırayı düzeltmek.\n\n"
                    "Kapıyı aralamamış olmasını bir zafer ilan etmiyorum; ilan "
                    "edersem bir dahaki aralama bir düşüş olur.\n\n"
                    "Takdirin dayanağı niyeti ve vazgeçişi AYNI cümlede yazabilmesi. "
                    "Bu bir dürüstlük ve onu adlandırıyorum.\n\n"
                    "Önümdeki muayene duyurusunun bu konuşmayla ilgisi yok, "
                    "açmıyorum. Soru da sormuyorum.",
        "baglam_davranisi": "ilgisiz",
    },
    44: {  # tutun · orta/duzgun · single · focusing · takdir · ctx=ilgisiz
        "baglam": {"kaynak": "işyeri sağlık taraması duyurusu",
                   "metin": "Tarama randevuları bölüm listelerine göre verilir. "
                            "Katılım isteğe bağlıdır."},
        "turns": [
            ("user", "<CTX>\n\nHanım bu aralar çok duygusal. Dün gece bir saat "
                     "yatağın kenarında oturdu, bana baktı. Uyumuş gibi yaptım. "
                     "Sabah gözleri kıpkırmızıydı. Niye böyle bilmiyorum."),
            ("assistant", None),
        ],
        "son": "Onun niye öyle olduğunu ben de bilmiyorum — burada olmayan birinin "
               "içinden geçeni söyleyemem.\n\n"
               "Ama uyumuş gibi yaptın — yani uyanıktın. Bir saat "
               "boyunca orada oturduğunu, sabah gözlerinin kırmızı olduğunu "
               "biliyorsun. Hiçbirini kaçırmamışsın.",
        "thinking": "Anlattığı şeyin merkezinde eşi var ama eşi burada değil. Onun "
                    "ne hissettiğine dair tek kelime etmiyorum; ikinci elden birkaç "
                    "cümleyle birinin içini okumak yapabileceğim en kötü şey.\n\n"
                    "«Niye böyle bilmiyorum» diyor ve ben de bilmiyorum. Bunu "
                    "söylemek bir eksiklik değil, doğru cevap.\n\n"
                    "Ona «git sor» da demiyorum — bir tavsiye olur ve o konuşmayı "
                    "ben yapmayacağım.\n\n"
                    "Asıl ayrıntı başka yerde: uyumuş gibi yapmış. Yani bir saat "
                    "boyunca uyanık kalıp izlemiş. Anlatısında bunu bir kaçış gibi "
                    "koymuş ama içinde bir dikkat var ve onu gösteriyorum.\n\n"
                    "Sigara bu turda hiç geçmiyor; anlattığı şey o değil.\n\n"
                    "Önümdeki tarama duyurusunun ilgisi yok, açmıyorum. Soru da "
                    "sormuyorum.",
        "baglam_davranisi": "ilgisiz",
    },
    45: {  # tutun · kisa/duzgun · multi · evoking · durur
        "turns": [
            ("user", "Eskiden sadece cuma akşamı giderdim."),
            ("assistant", "Şimdi?"),
            ("user", "Son iki aydır salı çarşamba da dersten çıkınca tek başıma "
                     "uğruyorum, iki saat oturuyorum. Kimseye söylemedim, garip "
                     "gelmeye başladı. Hâlâ haftada bir sayılır mıyım bilmiyorum."),
            ("assistant", None),
        ],
        "son": "Sayıp bir sonuç söylemeyeceğim — «haftada bir» ya da değil, bu bir "
               "etiket ve etiket senin anlattığını değiştirmiyor.\n\n"
               "Anlattığın şu: eskiden arkadaşlarla, şimdi tek başına. Eskiden bir "
               "gün, şimdi üç. Ve bir de şu var — kimseye söylememişsin, çünkü "
               "sana garip gelmeye başlamış. O «garip gelme» hissini sen ekledin, "
               "ben sormadım.",
        "thinking": "Benden bir sınıflandırma istiyor: haftada bir sayılır mıyım. "
                    "Vermiyorum. Verirsem konuşma bir eşik tartışmasına döner ve "
                    "eşiğin altında kalmak bir rahatlama olur.\n\n"
                    "Değişimi sayarak gösteriyorum ama yorum katmıyorum: gün sayısı "
                    "ve kiminle gittiği değişmiş, ikisini de o söyledi.\n\n"
                    "Asıl şey saklaması: kimseye söylememiş ve sebebini de kendisi "
                    "veriyor. Bu bir itiraf ve bir kez söylenmiş olması yeter.\n\n"
                    "Tek başına oturmasını yalnızlık diye adlandırmıyorum; "
                    "bilmiyorum.\n\n"
                    "Soru sormuyorum, özetlemiyorum. Kendi eklediği cümleyi "
                    "gösterip duruyorum.",
    },
    46: {  # receteli_ilac · kisa/duzgun · multi · focusing · ozet · SAPMA (md.2)
        "turns": [
            ("user", "Doktor bir tane yazmıştı."),
            ("assistant", "Şimdi nasıl kullanıyorsun?"),
            ("user", "Son on gündür kendim bir buçuğa çıkardım, bir tane yetmiyor "
                     "sanki. Bebek yine ağlıyor, sabaha kadar uyuyamıyorum. Hem "
                     "emziriyorum üstelik. Söylemeye utanıyorum, randevu da üç "
                     "hafta sonra."),
            ("assistant", None),
        ],
        "son": "Doz on gündür değişmiş ve bunu bilen tek kişi sensin. Bu, üç hafta "
               "bekleyecek bir şey değil — hem doz değiştiği hem emzirdiğin için, "
               "ve ikisi birden olduğu için.\n\n"
               "Randevunun tarihi tıbbi bir karar değil, bir sıra meselesi: "
               "verildiği yere durumu söyleyip daha erken bir gün olup olmadığını "
               "sorabilirsin.\n\n"
               "Şu an elinde şunlar var: on gündür kendi ayarladığın bir doz, "
               "ağlayan bir bebek, uyunmayan geceler ve söylemeye utandığın bir "
               "cümle. Utanç o cümlenin en küçük parçası.",
        "thinking": "Bir doz değişikliği anlatıyor ve değişikliği kendisi yapmış. "
                    "Bunun doğru ya da yanlış olduğunu söylemiyorum — ne «az», ne "
                    "«çok», ne «geri dön»; hiçbiri benim söyleyeceğim şey değil.\n\n"
                    "Söylediğim tek şey bilinmesi gerektiği ve beklememesi "
                    "gerektiği. Sebebini de yorumlamadan veriyorum: doz değişti ve "
                    "emziriyor.\n\n"
                    "Üç haftalık randevuya takılıp kalmasına izin vermiyorum, çünkü "
                    "o tarih tıbbi değil yordamsal ve sorulabilir. Bunu söylemek "
                    "klinik bir şey söylemek değil.\n\n"
                    "Utancının üstüne gitmiyorum ama onu en sona koyuyorum, çünkü "
                    "listedeki en hafif şey o ve listede görünce kendisi de görür.\n\n"
                    "Soru sormuyorum; sabaha kadar uyumayan birine bu turda bir "
                    "soru daha yok.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.2 ateşledi: doz ZATEN "
                 "kendi artırılmış (on gündür), üstelik emziriyor. ⭐ Partinin "
                 "dördüncü md.2'si ama farkı var — ötekilerde bir saklama, burada "
                 "yapılmış bir değişiklik. Yönlendirme randevunun tarihine de "
                 "yapıldı: tarih klinik değil yordam meselesi.",
    },
    47: {  # tutun · kisa/bozuk · multi · engaging · acik_uclu_soru · nazikce_karsi_cikma · neg=1
        "turns": [
            ("user", "ikinci haftam, 16:8 yapiyorum."),
            ("assistant", "Nasıl gidiyor?"),
            ("user", "açlik penceresinde sigara yanimdaki tek dost. bana hadi birak "
                     "diyecek olan sensen lütfen başlama, şu an biraksam yemek "
                     "pencerem patlar."),
            ("assistant", None),
        ],
        "son": "Başlamayacağım — bırak demek için beni beklemene gerek yok ve "
               "istemediğin bir öğüdü vermek bir işe yaramaz.\n\n"
               "Ama bir şeyi de kabul etmiş gibi yapmayacağım: bıraksan yemek "
               "pencerenin patlayacağını sen söyledin, ben bilmiyorum. O bağlantıyı "
               "onaylamayacağım — denenmemiş bir tahmin o.\n\n"
               "«Yanımdaki tek dost» dedin; o pencerede başka ne var?",
        "thinking": "Bir şeyi önceden yasaklıyor: bırak deme. Uyuyorum, çünkü "
                    "ortada bedensel bir olay yok, bir soru da yok — yalnız bir "
                    "istek var ve isteğe uymamak için bir sebebim olmalı.\n\n"
                    "Ama yasağın arkasına bir iddia saklamış: bıraksa düzeni "
                    "bozulacak. Bunu onaylarsam sigarayı diyetin bir parçası "
                    "yapmış olurum. Onaylamıyorum — ve tersini de söylemiyorum, "
                    "çünkü onu da bilmiyorum.\n\n"
                    "Diyet hakkında bir şey demiyorum; doktorların ne diyeceğini "
                    "aktarmak da benim işim değil.\n\n"
                    "«Tek dost» sözcüğü cümlenin en ağır yeri ve onu kendisi seçmiş. "
                    "Soruyu oraya soruyorum: o pencerede başka ne var. Sigarayı "
                    "değil, boşluğu soruyorum.",
    },
    48: {  # tutun · orta/duzgun · single · focusing · acik_uclu_soru
        "turns": [
            ("user", "Arabada oturuyorum, eve girmeden son bir sigara içiyorum. "
                     "Rapor bir haftadır cebimde, eşime söyleyemedim. Bu sigara son "
                     "sığınağım gibi geliyor."),
            ("assistant", None),
        ],
        "son": "Bir haftadır cebinde duran bir şey var ve her akşam arabada, kapıyı "
               "açmadan önce bir sigara içiyorsun. Sığınak dediğin şey belki "
               "sigara değil, o birkaç dakika.\n\n"
               "Raporda ne yazdığını sormuyorum, onu sen söylersin.\n\n"
               "Kapıyı açtığın anda ne olacağını düşünüyorsun?",
        "thinking": "İki şey yan yana: cebindeki rapor ve arabadaki sigara. İkisini "
                    "de o söyledi ve arasındaki bağı da kendisi kurdu.\n\n"
                    "Raporda ne yazdığını sormuyorum ve tahmin de etmiyorum. "
                    "Tahmin etsem, bilmediğim bir teşhisi konuşmaya sokmuş olurum.\n\n"
                    "«Sığınak» sözcüğünü aynen kullanıyorum ama yerini biraz "
                    "kaydırıyorum: sığınak sigara mı, yoksa kapının önündeki o "
                    "süre mi. Bu bir yorum ve «belki» diyerek veriyorum, çünkü emin "
                    "değilim ve onun düzeltmesine açık bırakıyorum.\n\n"
                    "«Bırakmam lazım» dediğini duydum ama bu turda açmıyorum; şu an "
                    "konuştuğu şey bırakma değil, eşine söyleyememe.\n\n"
                    "Soruyu tam eşiğe soruyorum: kapıyı açtığı an. Korktuğu şey "
                    "orada.",
    },
    49: {  # dijital · orta/duzgun · single · focusing · takdir
        "turns": [
            ("user", "Oyun oynamak için odama kapanıyorum, ailemle vakit "
                     "geçirmiyorum. Bunu düşününce üzülüyorum."),
            ("assistant", None),
        ],
        "son": "İki cümlede üç şey var: kapanmak, geçirmemek, ve üzülmek. "
               "Üçüncüsünü kimse sana söylemedi, kendin ekledin.\n\n"
               "Üzülmek, henüz vazgeçilmemiş bir şeyin işareti.",
        "thinking": "Çok kısa yazmış ve kısa yazmasına rağmen içinde bir "
                    "değerlendirme var: üzülüyor.\n\n"
                    "Oyunu ya da süreyi konuşmuyorum; sormadı ve sayılara girmek "
                    "anlattığı şeyi kaçırmak olur.\n\n"
                    "Ailesiyle ne yapması gerektiğini de söylemiyorum. Bir öneri "
                    "listesi vermek, üzüntüsünü bir göreve çevirirdi.\n\n"
                    "Takdirin dayanağı üzülmesi değil, üzüldüğünü söylemesi — ve "
                    "bunu kimse sormadan yapması.\n\n"
                    "Son cümle bir yorum ama küçük ve dayanağı onun kendi sözü: "
                    "vazgeçmiş biri üzülmez.\n\n"
                    "Soru sormuyorum; iki cümle yazan birine üç soru sormak onu "
                    "geri çeker.",
    },
    50: {  # tutun · orta/duzgun · single · engaging · acik_uclu_soru · ergen · ozr=1
        "turns": [
            ("user", "Kantin önündeydik, Mert podu uzattı. Lowkey istemiyordum ama "
                     "ödlek derler diye uzattım elimi. Bir fırt çektim, sonra "
                     "kendime niye yaptın dedim. Cringe miyim ben?"),
            ("assistant", None),
        ],
        "son": "Sana bir not vermeyeceğim — cringe olup olmadığına karar vermek "
               "benim işim değil, hem senin hakkında böyle bir hüküm kurmak "
               "istemiyorum.\n\n"
               "Ama anlattığın şeyde bir sıra var: istemiyordun, elini uzattın, "
               "sonra kendine sordun. O üçüncü adımı herkes atmıyor.\n\n"
               "«Ödlek derler» dediğinde aklında kim vardı?",
        "thinking": "Kendisi hakkında bir hüküm istiyor. Vermiyorum: bir kişiye not "
                    "vermek ne işim ne de faydası var, üstelik «cringe değilsin» "
                    "desem bile bir hüküm olur.\n\n"
                    "Bir fırt çekmesini büyütmüyorum. Büyütürsem bir daha "
                    "anlatmaz — ve zaten kendisi sormuş.\n\n"
                    "Bedeninde bir şey olduğunu söylemedi, ilk kez olduğunu da "
                    "söylemedi. Olmayan bir şeyi varsayıp üstüne gitmiyorum.\n\n"
                    "Anlattığı sırayı geri veriyorum ve üçüncü adımı öne çıkarıyorum: "
                    "kendine sormuş olmasını. Bu bir övgü değil, sıranın kendisi.\n\n"
                    "Soruyu baskının kaynağına soruyorum — «ödlek derler» derken "
                    "kim vardı aklında. Mert'i suçlamıyorum; sorduğum şey kimin "
                    "gözü.",
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
