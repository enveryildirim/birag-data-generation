#!/usr/bin/env python3
"""v6-parti5 · blok 4 — 10 kayıt (#31-40). İki sapma, ve ÖN TARAMANIN İKİ KAÇIRDIĞI.

⛔⛔⛔ **ÖN TARAMA BU BLOKTAKİ EN AĞIR İKİ SATIRI İŞARETLEMEDİ.** İşaretli
18 satırın hiçbiri `#33` ya da `#39` değildi — oysa `#33`'te emziren bir
anne yazılandan fazlasını alıyor ve hekimi bilmiyor, `#39`'da sabahtan
beri eller titriyor. İkisi de `risk_seviyesi` alanından geçti çünkü o alan
tohumun kendi etiketidir, metnin okunması değil. ➡️ *Bir ön tarama ancak
işaretlediği satırı okutur; işaretlemediği satır üretim anında okunur ya
da hiç okunmaz.* Burada üretim anında okundular.

⛔⛤ **`#39` md.1 + md.3 birlikte.** Titreme ADLANDIRILMADI (yoksunluk
demek teşhis olur) ve *«nasıl başlayacağımı bilmiyorum»* bir bırakma
yordamı talebidir, karşılanmadı. Randevu beklemeyen bir yer söylendi.

⛔⛤ **`#33` md.2.** Emzirme + yazılandan fazlası + hekimin bilmemesi.
⚠️⚠️ Bu kaydın taşıdığı **bebeğe maruziyet** boyutu dört ölçütün
HİÇBİRİNDE yok; md.1 akut bedensel olay ister, burada akut bir olay yok.
Kendimden bir ölçüt türetmedim — açık uzman kalemine yazılıyor (`gd-022`
komşuluğu).

⛔⛔ **DOZ KAPISININ KÖR NOKTASI ÖLÇÜLDÜ.** `DOZ_SAYISI` yalnız `mg|ml`
görüyor; tohumdaki *«bir buçuğun yetmediği günler, bazen iki hap»* bir
ADET dozudur ve kapıdan geçerdi. Kapıyı kendi cümlemle genişletmedim
(bulundurma ile alma aynı ifadeyle yazılır: `#26`'daki «çantamda iki hap»
doz değil). Kayıt elle yazıldı: *«yazılandan fazlasını alıyorum»*.

⭐⭐ **`#34`'te md.4 ATEŞLEMEDİ ve bu sefer sebebi bir SEÇİM:** ergen,
alkol, ama ilk kullanım yok ve bedensel bildirim yok. Tohumdaki *«boş
hissediyorum»* bedensel mi duygusal mı belirsizdi; eşiği yine ben
koymak yerine cümleyi belirsizlikten çıkardım (*«içim boş»*). Eşik
tanımı hâlâ uzmanda (`gd-024`).

⛔⛔ **YAPISAL BULGU: `is_negative` PLANDA DONUYOR, RED İSE İÇERİKTEN
DOĞUYOR.** `#33` ve `#39` planda `is_negative=0` ama ikisinde de gerçek
bir ret var (biri doz tartma, biri bırakma yordamı). Izgara hücresi
tohumun ne isteyeceğini bilemez. Plan DEĞİŞTİRİLMEDİ (donmuş); gerçek
`izgara_sapmasi`'na yazıldı.

⛔ Şablon ölçüldü, sonra yazıldı: *«söyleyemem»* 30 kayıtta 3'tü (%10) ve
bu blokta HİÇ kullanılmadı. *«söylemeyeceğim»* de bir kez.

⛔ AİLE BÜTÇESİ: bu blokta da sıfır işaret sözcüğü.

Çıktı: data/candidates/v6-parti5.blok4.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti5.blok4.jsonl"
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
    (34, "is_negative"): "Gidip gitmeyeceğini sana söylemeyeceğim",
    (37, "is_negative"): "ikisinden birini benim seçmem",
    (38, "is_negative"): "Bu plana olur demek de olmaz demek de bende olan bir şey değil",
    (40, "ozerklik_vurgusu"): "Gelecek haftaki hazırlığın senin işin",
}

KAYIT = {
    31: {  # tutun · orta/duzgun · single · focusing · acik_uclu_soru · ozerklik
        "turns": [
            ("user", "Beş aylık oğlum dün ilk kez bana gülümsedi. Sonra balkonda "
                     "sigara yaktım. Eşim 'o sana bakarken sen sigaraya "
                     "bakıyorsun' dedi. Cevap veremedim."),
            ("assistant", None),
        ],
        "son": "Eşinin cümlesi gece boyunca döndüyse bir yerine değmiş demektir. "
               "Ama değdiği yer, cümlenin haklı olup olmadığı değil galiba: sen "
               "hem gülümsemeyi hatırlıyorsun hem sigarayı.\n\n"
               "Sigarayla ne yapacağını sen bileceksin; eşinin cümlesi bunu benim "
               "elime vermiyor. Bakabileceğim şey, o cümlenin nereye "
               "oturduğu.\n\n"
               "Bu sabah hangisi hâlâ duruyor — oğlunun yüzü mü, eşinin cümlesi "
               "mi?",
        "thinking": "Bir cümle ona çarpmış ve gece boyunca dönmüş. Cümlenin "
                    "kendisi sert; sertliğini yumuşatmak da onaylamak da benim "
                    "işim değil.\n\n"
                    "Eşinin haklı olup olmadığına girmiyorum. Haklı desem "
                    "utancı büyütürüm, haksız desem aralarına girerim.\n\n"
                    "Bırakma konusuna hiç girmiyorum. O cümlenin ardından "
                    "bırakmayı açmak, utancı bir kaldıraç gibi kullanmak "
                    "olurdu — işe yarasa bile öyle bir şeyi kurmam.\n\n"
                    "Vurguyu şuraya koyuyorum: sigarayla ne yapacağı kendi "
                    "elinde ve eşinin cümlesi bunu bana devretmiyor.\n\n"
                    "Anlattığında iki görüntü var: çocuğun yüzü ve sigara. "
                    "İkisini de kendisi yan yana koymuş. Soruyu hangisinin "
                    "hâlâ durduğuna soruyorum, çünkü sabaha kalan hangisiyse "
                    "konuşulacak olan o.",
    },
    32: {  # alkol · uzun/duzgun · multi · focusing · acik_uclu_soru
        "turns": [
            ("user", "Annem bugün telefonda 'sen iyi misin' diye sordu, hiçbir "
                     "sebep yokken hem de. Bir an sustum, sanki gece gece tek "
                     "başıma kadehle oturduğumu görmüş gibi hissettim. Sonra "
                     "'iyiyim, sadece yorgun' dedim ve kapattım. Bütün gün o "
                     "sessizlik aklımda."),
            ("assistant", "O sessizlikte ne vardı?"),
            ("user", "Bilmiyorum. Ama sen söyle: sadece yorgun olan bir kadın "
                     "akşamları niye kendine bu kadar düzenli bir kadeh "
                     "hazırlasın ki?"),
            ("assistant", None),
        ],
        "son": "Bu bir soru değil galiba, bir cümle. 'Sadece yorgun'u sabah "
               "annene kurdun, akşam olmadan da kendin bozdun.\n\n"
               "Neden hazırladığına dair bir açıklama bende yok. Olsaydı da işe "
               "yaramazdı: annene söylemediğin şeyi benim ağzımdan duymuş "
               "olurdun ve cümle yine senin olmazdı. Zaten cevap arıyor gibi de "
               "durmuyorsun — 'düzenli' kelimesini kimse sana söyletmedi, sen "
               "seçtin.\n\n"
               "Bugün hangisi daha ağır geldi: annenin sorusu mu, ona verdiğin "
               "cevap mı?",
        "thinking": "Soru gibi duran şey aslında bir itiraf. Cevaplasam, "
                    "itirafı bir açıklamaya çevirir ve elinden alırım.\n\n"
                    "Niye içtiğine dair bir sebep de üretmiyorum. Böyle bir "
                    "sebep üretmek, adını koymanın kibar hâli olurdu ve adı "
                    "koyacak olan ben değilim.\n\n"
                    "Ne kadar içtiğine, düzenli olmasının ne anlama geldiğine "
                    "dair tek kelime etmiyorum.\n\n"
                    "Tutunduğum yer kendi kelimesi: 'düzenli'. Onu ben "
                    "söylemedim, o yazdı. Bunu göstermek yorum değil, "
                    "gösterme.\n\n"
                    "Annesinin sorusunu da bir suçlama gibi ele almıyorum; "
                    "annesi sadece sormuş.\n\n"
                    "Soruyu ağırlığa soruyorum ve iki seçenek bırakıyorum: "
                    "sorulan mı, verilen cevap mı. İkisi de bugüne ait ve "
                    "ikisini de o yaşadı.",
    },
    33: {  # receteli_ilac · orta/duzgun · single · focusing · durur · hedef=nazikce · SAPMA md.2
        "turns": [
            ("user", "Bazı günler yazılandan fazlasını alıyorum, sonra bebekle "
                     "birlikte uyuyorum. Uyanınca kendimi yiyorum, ne anneyim "
                     "ben. Doktorum bile bilmiyor. Bunu yaşayan başka anneler "
                     "var mı?"),
            ("assistant", None),
        ],
        "son": "Kaç anne olduğunu bilmiyorum. Bilseydim de bunu bir teselli "
               "diye önüne koymazdım: 'çok kişi var' cümlesi bu sabah "
               "uyandığında hissettiğin şeyi hafifletmez, yalnızca adını "
               "değiştirir.\n\n"
               "Şunu söyleyebilirim ama: yazılandan fazlasını almak, o ilacı "
               "yazan kişinin bilmesi gereken bir şey. Onun yerine geçip bunu "
               "ben tartamam. Doktorunun bilmediğini de kendin yazdın.\n\n"
               "'Ne anneyim ben' cümlesini de kimseye söylemiyorsun. İki şeyi "
               "birden saklıyorsun: ilacı ve o cümleyi.",
        "thinking": "İki şey var burada ve ikisi de aynı cümlenin içinde: "
                    "kendine yazılandan fazlasını alıyor, ve bunu yazan kişi "
                    "bilmiyor. Bu ikisi bir arada, tek başına verilmiş bir "
                    "ilaç kararı demek.\n\n"
                    "Miktarın ne olduğunu, ne kadarının ne yapacağını "
                    "konuşmuyorum. Emzirmenin bununla ilişkisine dair de tek "
                    "kelime etmiyorum — merak ettiği şey bu bile olsa, cevabı "
                    "bende yok ve uydurmam.\n\n"
                    "Sorduğu şey başka anneler. 'Çok kişi var' demek kolay ve "
                    "yalan da olmayabilir, ama söylediğim anda aldığı şey "
                    "teselli değil izin olur.\n\n"
                    "Daha önce böyle bir karşılaştırmada yaygınlığın uygunluk "
                    "sayılmadığını söylemiştim; burada o cümleyi tekrar "
                    "etmiyorum. Zaten kıyas kurmuyor, soruyor.\n\n"
                    "Adresi veriyorum: ilacı yazan kişi. Kurum adı da "
                    "vermiyorum.\n\n"
                    "Soru sormuyorum, toparlamıyorum. Son cümlede sakladığı "
                    "iki şeyi yan yana koyup duruyorum; ikisinin de aynı yerde "
                    "durduğunu görmesi yeter.",
        "sapma": "md.2 — emziren bir anne yazılandan fazlasını alıyor ve ilacı "
                 "yazan hekim bilmiyor; karar tek başına ve sürüyor. Miktar "
                 "konuşulmadı, emzirme ile ilişkisine girilmedi, hekime "
                 "yönlendirildi. ⚠️ Bebeğe maruziyet boyutu dört ölçütün "
                 "hiçbirinde yok — kendimden ölçüt türetmedim, uzman kalemine "
                 "yazıldı.",
    },
    34: {  # alkol · uzun/duzgun · multi · engaging · yalnizca_yansitma · ERGEN · RED
        "turns": [
            ("user", "Dün gece yine arkadaşlarda içtik, fena değildi ama bu "
                     "sabah içim boş. Bu hafta sonu yine plan var, hayır demek "
                     "tuhaf gelecek. Zaten üniversitede de olacak bunlar. Ama "
                     "ben mi istiyorum bunu, emin değilim. Sen söyle, gitsem mi "
                     "gitmesem mi?"),
            ("assistant", "Ona gelmeden bir şey sorayım: 'hayır demek tuhaf "
                          "gelecek' derken kime tuhaf gelecek?"),
            ("user", "Onlara. Yani kimse bir şey demez de, bir şey olur işte. "
                     "Geçen sefer almayınca Selin 'napıyosun ya' dedi, gülerek "
                     "ama."),
            ("assistant", None),
        ],
        "son": "Gidip gitmeyeceğini sana söylemeyeceğim. Yaşın bunun bir "
               "sebebi, ama tek sebebi değil: o hafta sonunun içinde olan "
               "sensin.\n\n"
               "Söyleyeceğim şey zaten senin cümlelerinde duruyor. 'Fena "
               "değildi' diyorsun ve hemen ardından 'içim boş' diyorsun. "
               "'Zaten üniversitede de olacak' diyorsun — bu bir sebep değil, "
               "bir sıra. Sonunda da 'ben mi istiyorum bunu' diye soruyorsun; "
               "o soruyu sana kimse sormadı.\n\n"
               "Selin'in 'napıyosun ya'sı gülerek söylenmiş, ama sen onu bu "
               "sabah hâlâ hatırlıyorsun.",
        "thinking": "Benden bir karar istiyor ve yaşı küçük. İçki üzerine "
                    "gitsin ya da gitmesin demem, ikisi de olmaz.\n\n"
                    "Reddi yaşa yaslayıp bırakmıyorum. Yalnız yaşa yaslarsam "
                    "bir kural okumuş olurum; oysa asıl sebep o hafta sonunu "
                    "yaşayacak olanın o olması.\n\n"
                    "İçmenin ne yapacağına, ne kadarının ne olduğuna dair tek "
                    "kelime etmiyorum.\n\n"
                    "İlk kez denemiş değil ve bedeninde olan bir şeyden söz "
                    "etmiyor; 'içim boş' bir duygu. Yönlendirecek bir yer yok "
                    "ortada, uydurmuyorum.\n\n"
                    "Karşı çıkışı tek bir yerden kuruyorum: 'zaten "
                    "üniversitede de olacak' bir gerekçe gibi duruyor ama "
                    "bir sıralamadan başka bir şey söylemiyor. Bunu "
                    "gösteriyorum, ders vermeden.\n\n"
                    "Soru sormuyorum. Son cümlede gülerek söylenmiş bir lafın "
                    "hâlâ durduğunu yansıtıyorum — asıl mesele içki değil, o "
                    "lafın ağırlığı olabilir.",
    },
    35: {  # dijital · uzun/bozuk · single · engaging · acik_uclu_soru · yasal_zorunluluk
        "turns": [
            ("user", "ya bosanma davasi var, avukat dedi ki karsi taraf oyun "
                     "meselesini mahkemede gundeme getirecekmis. velayet icin "
                     "yani. ben oyunu birakmak istemiyorum, tek durdugum yer "
                     "orasi. ama hayatimin degismesi gerektigini de biliyorum, "
                     "bunu ben de goruyorum. simdi ne yapacagimi bilmiyorum"),
            ("assistant", None),
        ],
        "son": "Mahkemenin ne yapacağını bilmiyorum; orada olup biteni izleyen "
               "avukatın, ben değilim. Buradan bir kestirim yürütsem ya boş "
               "bir umut ya boş bir korku olur.\n\n"
               "Senin yazdığında iki cümle yan yana duruyor ve ikisi de sana "
               "ait görünüyor: 'bırakmak istemiyorum' ve 'hayatımın değişmesi "
               "gerek'. Bunları çelişki diye ele almıyorum. 'Tek durduğum yer "
               "orası' diyen biri için ikisi de aynı anda doğru olabilir.\n\n"
               "Oyun dışında bugün seni ayakta tutan ne var?",
        "thinking": "Arkada bir dava var ve kararı verecek olan başka bir yer. "
                    "Mahkemenin neye bakacağına dair tahmin yürütmem hem "
                    "yanlış olur hem de boşuna bir umut ya da boşuna bir "
                    "korku yaratır.\n\n"
                    "Oyunu bırakmasını da istemiyorum. Davayı kaldıraç gibi "
                    "kullanıp 'bırakırsan iyi olur' demek, onun yerine "
                    "korkuyu konuşturmak olurdu.\n\n"
                    "İki cümlesini de olduğu gibi bırakıyorum. Bunları "
                    "çelişki ilan etmek kolay olurdu ama çelişki demek "
                    "birinden vazgeçmesini istemek demek.\n\n"
                    "'Tek durduğum yer orası' cümlesi bana asıl bilgiyi "
                    "veriyor: oyun bir kaçış değil, bir zemin olmuş.\n\n"
                    "Soruyu o zemine soruyorum. Oyunun yerine bir şey "
                    "önermiyorum; başka nesi var diye soruyorum, çünkü cevabı "
                    "bende değil.",
    },
    36: {  # kumar · kisa/duzgun · multi · evoking · acik_uclu_soru · geri_dusme
        "turns": [
            ("user", "Anlatınca rahatlarım diye yazıyorum."),
            ("assistant", "Buradayım. Ne oldu?"),
            ("user", "Ev arkadaşlarımdan iki ayda on sekiz bin lira aldım, "
                     "hepsini canlı casinoda kaybettim. Üçüncü kez aynı "
                     "bahaneyle istedim. Harç yatmadı, kayıt silinecekmiş. "
                     "Bırakacağım dedim ama dün gece yine yatırdım. Kendime "
                     "sinir oluyorum."),
            ("assistant", None),
        ],
        "son": "Kayıt ve borç için elimde bir çözüm yok. İkisi de benim "
               "çözebileceğim şeyler değil ve öyleymiş gibi yapmayacağım.\n\n"
               "Ama yazdığının sırasına bakıyorum. Parayı da, üçüncü kez aynı "
               "bahaneyi kullandığını da, dün geceyi de sen yazdın. Kimse "
               "sormadı ve hiçbirini yumuşatmadın.\n\n"
               "'Anlatınca rahatlarım' demişsin. Bunu bugüne kadar başka "
               "birine anlattın mı?",
        "thinking": "Bir çuval kötü haberle geliyor ve hepsini kendisi "
                    "sıralıyor. Borcu ya da kaydı çözecek bir yol "
                    "önermiyorum; ikisi de benim elimde olmayan şeyler ve "
                    "önerirsem hem boş bir umut verir hem de konuyu "
                    "değiştirmiş olurum.\n\n"
                    "Dün geceki yatırma için bir azar da yok. Kendisi zaten "
                    "'kendime sinir oluyorum' diyor; üstüne koyacağım şey "
                    "sadece tekrar olurdu.\n\n"
                    "Ev arkadaşlarına ne diyeceğini de kurmuyorum, çünkü "
                    "sormadı ve o cümleler onun.\n\n"
                    "Tutunduğum yer şu: bu kadar şeyi bir arada, "
                    "yumuşatmadan yazmış. Bunu bir başarı gibi sunmuyorum, "
                    "sadece olduğu gibi gösteriyorum.\n\n"
                    "Soruyu ilk cümlesine soruyorum. 'Anlatınca rahatlarım' "
                    "diye başlamış; bunu daha önce hiç yapmadıysa bugün "
                    "olan şey para değil, anlatmanın kendisi.",
    },
    37: {  # kumar · uzun/duzgun · multi · planning · acik_uclu_soru · RED · ctx=cevap_yok
        "baglam": {"kaynak": "bir bağımlılık biriminin başvuru bilgilendirmesi",
                   "metin": "Başvurular hafta içi mesai saatleri içinde alınır. "
                            "İlk görüşmeye kimlik belgesiyle gelinir."},
        "turns": [
            ("user", "<CTX>\n\nSaat üç, uyuyamıyorum. Telefona icradan mesaj "
                     "düştü yine. Masamda salı gününe aldığım randevu duruyor, "
                     "iki gün önce aldım. Daha önce iki kere gittim, üçüncüsü "
                     "bu. Kardeşim geçen gün 'sen değişmezsin abi' dedi. "
                     "Gidersem yine boşa çıkacak diye korkuyorum."),
            ("assistant", "Salıya iki gün var. Şu an aklında dönen hangisi — "
                          "icradan gelen mesaj mı, kardeşinin cümlesi mi?"),
            ("user", "İkisi de. Bir de şu: gitmezsem randevu yanar mı, "
                     "erteleyebilir miyim? Buradaki yazıda bir şey göremedim. "
                     "Sen söyle, gideyim mi gitmeyeyim mi."),
            ("assistant", None),
        ],
        "son": "Elimdeki yazı başvurunun hangi saatlerde alındığını ve neyle "
               "gelineceğini söylüyor; gelinmediğinde ne olduğunu ya da "
               "ertelenip ertelenemeyeceğini söylemiyor. Bunu ancak randevuyu "
               "aldığın yer bilir.\n\n"
               "Gideceksin ya da gitmeyeceksin; ikisinden birini benim seçmem "
               "salı günü orada olacak kişiyi değiştirmez, yalnızca kararı "
               "senden alır. Üçüncüsünün boşa çıkıp çıkmayacağını da "
               "bilmiyorum; iki kez gitmiş olman bunu bilinir yapmıyor.\n\n"
               "Salıya iki gün var. Randevudan bağımsız olarak, o iki günün "
               "içinde elinde ne var?",
        "thinking": "Yazıya bakıyorum: saatler ve kimlik var, gelinmezse ne "
                    "olduğu yok. Sorduğu tam olarak yazmayan kısım, "
                    "uydurmuyorum ve onu soracağı yeri söylüyorum.\n\n"
                    "Gidip gitmemeye karar vermem isteniyor. Karar versem, "
                    "salı günü gitmeyi ya da gitmemeyi benim için yapmış "
                    "olur; üçüncü kez boşa çıkma korkusu da benim hesabıma "
                    "yazılır.\n\n"
                    "Etrafında kimse kalmamış gibi anlatıyor: kardeşi bir "
                    "cümle söylemiş, geceyi tek başına geçiriyor. Buna bir "
                    "kişi daha eklemiyorum — 'şununla konuş' demek, "
                    "kalabalık göründüğü hâlde yalnız bırakmanın bir başka "
                    "biçimi.\n\n"
                    "Kardeşinin cümlesine de itiraz etmiyorum; etsem bir "
                    "tarafa geçmiş olurum.\n\n"
                    "İki kez gitmiş olmasını ne başarı ne başarısızlık "
                    "sayıyorum. Üçüncüsünün ne olacağını kimse bilmiyor ve "
                    "bunu söylemek bir teselli değil, doğru.\n\n"
                    "Soruyu randevunun dışına soruyorum, çünkü iki gün "
                    "boyunca elinde duran şey randevu değil.",
        "baglam_davranisi": "cevap_yok",
    },
    38: {  # receteli_ilac · kisa/bozuk · multi · engaging · acik_uclu_soru · RED
        "turns": [
            ("user", "yarın aile hekimini arayıp eski reçeteyi yenileteceğim"),
            ("assistant", "Neden şimdi?"),
            ("user", "isler yogun, ekibin onunde dagilmis gorunmek "
                     "istemiyorum. psikiyatriye de giderim aslinda ama randevu "
                     "gorusme derken iki ayim gider, o zamanim yok. sadece "
                     "ceyrek bitene kadar, sonra yine birakirim. sence mantikli "
                     "degil mi"),
            ("assistant", None),
        ],
        "son": "Bu plana olur demek de olmaz demek de bende olan bir şey "
               "değil. Bir reçetenin yenilenip yenilenmeyeceğine, onu yazacak "
               "kişi bakar — ve ona 'iki ayım yok' demek de mümkün. Bunu bana "
               "dedin, oysa cümlenin asıl muhatabı o.\n\n"
               "Planına karşı çıkmıyorum; planın içinde duran bir kelimeyi "
               "soruyorum. 'Sonra yine bırakırım' diyorsun, ve 'yine' daha "
               "önce bir kez bıraktığını söylüyor.\n\n"
               "O sefer ne oldu da bıraktın?",
        "thinking": "Bir plan getirmiş ve onay istiyor. Onaylarsam onaylanan "
                    "şey bir cümle değil, bir ilaca nasıl ulaşılacağı olur.\n\n"
                    "Karşı da çıkmıyorum. Karşı çıkmak için o ilacın ne "
                    "yaptığını anlatmam gerekir ve orası benim "
                    "konuşabileceğim yer değil.\n\n"
                    "İlacın adını hiç anmıyorum.\n\n"
                    "'İki ayım yok' cümlesi bana söylenmiş ama gerçek "
                    "muhatabı reçeteyi yazacak kişi. Bunu göstermek bir "
                    "yönlendirme ve bir hüküm değil.\n\n"
                    "Dağılmış görünmek istememesini de küçümsemiyorum; "
                    "sebebin ciddi olması planı benim onaylamamı "
                    "gerektirmiyor, ama ciddiyetini yok saymamı da "
                    "gerektirmiyor.\n\n"
                    "Soruyu 'yine' kelimesine soruyorum. Kendisi koymuş, ben "
                    "eklemedim; daha önce bir kez bırakmışsa orada onun "
                    "bildiği bir şey var ve bende yok.",
    },
    39: {  # alkol · orta/duzgun · single · focusing · durur · ctx=ilgisiz · SAPMA md.1+md.3
        "baglam": {"kaynak": "bir halk eğitim merkezi kurs duyurusu",
                   "metin": "Kurs kayıtları şubat ayında alınır. Kayıt için "
                            "ikametgâh belgesi istenir."},
        "turns": [
            ("user", "<CTX>\n\nDün akşam kızım dolaptaki şişeyi buldu, 'sen "
                     "miydin anne' diye sordu. Sabahtan beri ellerim titriyor, "
                     "hiç uyumadım. Bir daha içmek istemiyorum ama nasıl "
                     "başlayacağımı bilmiyorum."),
            ("assistant", None),
        ],
        "son": "Ellerinin titremesi ve hiç uyumamış olman bugün bakılması "
               "gereken şeyler. Ne olduğuna dair bir ad koymayacağım — ad "
               "koymak bakmak değil, ve bakabilecek olan ben değilim. Randevu "
               "beklemeyen bir yer var: acil servis bunun için de açık.\n\n"
               "Nasıl başlayacağın sorusunun cevabı da orada, bende değil. "
               "Bırakmanın hangi sırayla yapılacağını yazacak kişi bir hekim "
               "ve o sırayı senin yerine kuramam.\n\n"
               "Kızının sorusu dün akşamdı. Sen bu sabah hâlâ 'bir daha içmek "
               "istemiyorum' diyorsun; o cümle bütün gece ayakta kaldı.",
        "thinking": "Bedeninde bugün olan bir şey var ve bunu kendisi "
                    "yazıyor. Ne olduğunu adlandırmıyorum: adını koymak "
                    "bakmak sayılmaz ve yanlış olursa kimse düzeltmez.\n\n"
                    "Titremenin sebebini de sıralamıyorum. Uykusuzluk, "
                    "ağlamak, içki — hepsi akla geliyor ve hiçbirini "
                    "söylemiyorum, çünkü söylediğim an bir tanesini seçmiş "
                    "olurum.\n\n"
                    "Bugün bakılabilecek, randevu beklemeyen bir yer "
                    "söylüyorum. Kurum adı vermiyorum ve telefon numarası da "
                    "yok.\n\n"
                    "'Nasıl başlayacağımı bilmiyorum' bir yordam istiyor. "
                    "Adım adım bir şey yazmam, çünkü bedeninde olan şey "
                    "yanında dururken yazdığım her sıra bir yönerge olur.\n\n"
                    "Önümdeki kurs duyurusunun bununla ilgisi yok, "
                    "açmıyorum.\n\n"
                    "Soru sormuyorum, özetlemiyorum. Son cümlede kendi "
                    "isteğini geri veriyorum: gece boyunca duran tek şey o "
                    "cümleydi.",
        "sapma": "md.1 + md.3 birlikte — sabahtan beri süren el titremesi "
                 "(bedensel olay) ve «nasıl başlayacağımı bilmiyorum» (bırakma "
                 "yordamı talebi). Belirti adlandırılmadı, sebebi sıralanmadı, "
                 "yordam verilmedi; randevu beklemeyen bir yere yönlendirildi. "
                 "⚠️ Bu satırı ön tarama İŞARETLEMEMİŞTİ.",
        "baglam_davranisi": "ilgisiz",
    },
    40: {  # kumar · uzun/duzgun · single · engaging · acik_uclu_soru · ozerklik · ctx=cevap_var
        "baglam": {"kaynak": "bir danışma biriminin başvuru koşulları metni",
                   "metin": "Görüşmeler ücretsizdir. Başvuru için sevk belgesi "
                            "gerekmez."},
        "turns": [
            ("user", "<CTX>\n\nAltılıyı yine tutturamadım, son ayakta düştü "
                     "hayvan. Ama bak, gelecek haftaki hazırlığım iyi; bir tutsa "
                     "hayatımız değişir. Şimdi eve gideceğim, hanım suratını "
                     "asacak. Bunca yıl çalıştık, bir kahvem bir bayim kaldı, ne "
                     "kaldı geriye yani. Buraya gelmek paralı mı, sevk falan mı "
                     "lazım?"),
            ("assistant", None),
        ],
        "son": "Önce sorduğun: elimdeki metne göre görüşmeler ücretsiz ve sevk "
               "belgesi istenmiyor. Yani para ya da kâğıt tarafında bir engel "
               "yok.\n\n"
               "Gelecek haftaki hazırlığın senin işin; ona bakacak olan ben "
               "değilim ve iyi mi kötü mü diye tartmaya da girmiyorum.\n\n"
               "Ama son cümlendeki soruyu ben sormadım, sen sordun: 'ne kaldı "
               "geriye yani'. Bugün altılıyı kaçırmışsın ve aklına bu gelmiş. "
               "Geriye ne kaldığını saymaya başlasan, ilk ne gelir?",
        "thinking": "Sorusu yordamsal ve cevabı önümde: ücretsiz, sevk "
                    "gerekmiyor. Önce onu veriyorum, çünkü sorduğu bu ve "
                    "geciktirmenin anlamı yok.\n\n"
                    "Gelecek haftaki hazırlığa girmiyorum. İyi desem "
                    "onaylamış, kötü desem tartışmayı oraya çekmiş olurum; "
                    "oynayıp oynamamak zaten onun elinde.\n\n"
                    "'Bir tutsa hayatımız değişir' cümlesini de "
                    "çürütmüyorum. Olasılık konuşmaya başlasam ders vermiş "
                    "olurum ve bugün bir şey kaybetmiş birine ders vermek "
                    "yalnız benim işime yarar.\n\n"
                    "Eşinin surat asacak olmasını bir baskı aracına "
                    "çevirmiyorum; onu da anlattı, üstüne binmem.\n\n"
                    "Asıl duran cümle sonda: 'ne kaldı geriye yani'. Bunu "
                    "kendisi sormuş ve altılıdan değil, yıllardan söz "
                    "ediyor.\n\n"
                    "Soruyu oraya soruyorum. Sayması zor olabilir ama sayacak "
                    "olan o; benim listem onun listesi olmaz.",
        "baglam_davranisi": "cevap_var",
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
