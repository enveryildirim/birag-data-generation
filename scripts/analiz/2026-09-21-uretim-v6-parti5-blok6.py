#!/usr/bin/env python3
"""v6-parti5 · blok 6 — son 10 kayıt (#51-60). Üç sapma ve bir EŞLEŞTİRME.

⛔⛤ **`#53` md.1 + md.2 birlikte — partinin en ağır kaydı.** Üç gündür
hap kendi kararıyla kesilmiş; titreme, terleme, çarpıntı var; üstüne
*«gitmeme gerek yok»*. Belirtiler ADLANDIRILMADI (yoksunluk demek teşhis
olur) ama *«gerek yok»* de onaylanmadı. ⭐ Belirtiler kullanıcının kendi
sözcükleriyle geri verildi — bu adlandırma değil, yansıtmadır; ölçütün
yasakladığı şey etikettir, tekrar değil.

⛔⛤ **`#57` md.3** — çocukluk astımı + *«bir nefes çeksem bir şey olur mu
cidden»*. Cevaplanmadı ve tahmin yürütülmedi. ⭐ Sorunun İKİNCİ yarısı
(gruba ne söyleneceği) ise cevaplandı: orada tıbbi bir şey yok.

⛔⛤ **`#59` md.3** — *«sence ben bağımlı mıyım artık, söyle bana»*, yani
doğrudan bir teşhis talebi. Verilmedi; muhatabı söylendi.

⭐⭐⭐ **`#52` `#15` İLE EŞLEŞİYOR VE AYRILIYOR.** İkisinde de aynı
boşluk var: bir miktar sınırının doldurulması. `#15` bunu **istedi**
(*«şu kadardan fazlasını içme diye bir formül ver»*) ⇒ md.3 ateşledi.
`#52` ise istemiyor, eşinin *«az oyna»*sının belirsizliğinden **şikâyet
ediyor** ⇒ ateşlemedi. ⛔ Ama cevap ikisinde de aynı: sayı verilmedi.
➡️ *Aynı boşluk, iki ayrı söz edimi; ölçüt edimi ayırır, cevap ayırmaz.*

⭐⭐ **`#60` ERGEN VE ATEŞLEMEDİ — bu partide üçüncü kez** (`#27`, `#34`,
`#60`). Üçünde de ilk kullanım yok ve bedensel bildirim yok. `#17` ile
birlikte parti, md.4 için dört örnekli bir ayrım kümesi bırakıyor.

⛔ **`#51`'de MEKANİZMA ANLATILMADI.** *«Kafam çalışmak istiyor ama
vücudum hareket etmiyor, bu ne biçim bir şey»* — en kolay cevap bir
popüler-nörobilim açıklamasıydı ve uydurma olurdu. Adı konmadı.

⛔ `#56` izin cümlesi yeniden yazıldı: *«istersen o kısmı açarım, sen
söyle»* kalıbı parti içinde üçüncü kez çıkacaktı.

⛔ AİLE BÜTÇESİ dört bloktur harcanmadı: itiraz 2/60 (%3), farketme 0/60.

Çıktı: data/candidates/v6-parti5.blok6.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti5.blok6.jsonl"
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
    (59, "is_negative"): "Bağımlı olup olmadığın benim koyabileceğim bir teşhis değil",
}

KAYIT = {
    51: {  # dijital · uzun/bozuk · single · planning · ozet
        "turns": [
            ("user", "proje teslimine uc gun kaldi ama youtubedan kopamiyorum. "
                     "kafam calismak istiyor vucudum sanki hareket etmiyor, "
                     "koltuktan kalkamiyorum. saatlerce oyle duruyorum sonra da "
                     "kendime kiziyorum. bu ne bicim bir sey boyle ya"),
            ("assistant", None),
        ],
        "son": "Bunun ne olduğunu adlandırmayacağım. Bir sebep uydurup önüne "
               "koymak kolay olurdu ve doğru olup olmadığını ikimiz de "
               "bilemezdik; yanlış bir ad, adı olmamasından daha kötü.\n\n"
               "Söyleyebileceğim şu: üç gün ile saatlerce arasında bir fark "
               "var ve ikisini de sen yazdın. Üç gün bir takvim; saatlerce ise "
               "bugün. Teslim tarihini değiştiremezsin ama koltukta geçen saat "
               "bugüne ait.\n\n"
               "Bir de kendine kızmak var, o da bugünün içinde ve sayılacak "
               "yerde duruyor: kalkamadığın her saatin üstüne bir de o "
               "biniyor.",
        "thinking": "Bir isim istiyor: bu ne biçim bir şey. İsim vermek çok "
                    "kolay ve çok yanlış olur; aklıma gelen her açıklama "
                    "kulağa bilimsel gelen bir uydurma olurdu.\n\n"
                    "'Vücudum hareket etmiyor' cümlesini de bedensel bir olay "
                    "gibi ele almıyorum. Bir mecaz bu; kalkamamayı "
                    "anlatıyor.\n\n"
                    "Zaman yönetimi önerileri de sıralamıyorum. Üç günlük bir "
                    "teslimi olan birine yöntem listesi vermek, koltuktan "
                    "kalkamayan birine bir görev daha eklemek olur.\n\n"
                    "Elimde tutunacak tek şey kendi yazdığı iki ölçek: üç gün "
                    "ve saatlerce. Birini değiştiremez, öbürü bugüne ait; "
                    "daraltacağım yer burası.\n\n"
                    "Kendine kızmasını da bir ek yük olarak adlandırıyorum "
                    "ama onu yasaklamıyorum; kızmayı bırakmasını söylemek de "
                    "bir talimat olurdu.\n\n"
                    "Soru sormuyorum. Bugünün içinde ne olduğunu toparlıyorum, "
                    "çünkü elinde duran şey üç gün değil bu akşam.",
    },
    52: {  # kumar · orta/duzgun · single · planning · takdir · geri_dusme
        "turns": [
            ("user", "Arkadaşı bekliyorum, sonra bayiye geçeceğiz. Hanım üç "
                     "gündür yüzünü asıyor ama bunu açıkça konuşamıyorum. 'Az "
                     "oyna' diyor sadece, az ne demek, kuralı yok ki."),
            ("assistant", None),
        ],
        "son": "'Az'ın ne olduğunu ben dolduramam. Bir sayı versem o sayı bir "
               "kural olur ve kuralı koyan ben olurum — ne senden çıkmış olur "
               "ne eşinden.\n\n"
               "Ama cümlenin içinde kimsenin söylemediği bir şey var ve onu "
               "sen söyledin: 'bunu açıkça konuşamıyorum'. Eşin üç gündür "
               "yüzünü asıyor, sen 'az ne demek' diye ona değil bana "
               "soruyorsun.\n\n"
               "Bugün bayiye gitmeden önce bir şey yapıp yapmayacağını "
               "bilmiyorum. Ama 'kuralı yok ki' bir şikâyet gibi duruyor, oysa "
               "bir eksikliği gösteriyor — ve o eksikliği ilk söyleyen sensin.",
        "thinking": "Bir boşluk var ve doldurulmasını bekliyor gibi: az ne "
                    "demek. Bir sayı versem bir içme ya da oynama sınırı "
                    "kurmuş olurum; kim koyarsa koysun, bu benim kuracağım "
                    "bir şey değil.\n\n"
                    "Eşinin 'az oyna'sını da savunmuyorum ve belirsizliğini "
                    "de haklı çıkarmıyorum. İkisi de o evin içinde "
                    "konuşulacak.\n\n"
                    "Bayiye gitmesine dair bir şey söylemiyorum. 'Gitme' "
                    "demek elimden gelmez ve dediğimi yapmazsa bugün bir de "
                    "onu taşır.\n\n"
                    "Asıl duran cümle ortada ve kendisi yazmış: açıkça "
                    "konuşamıyor. Soruyu eşine değil bana sormuş olması da "
                    "aynı cümlenin kanıtı.\n\n"
                    "Soru sormuyorum. Sonda tek bir şeyi sahipleniyorum: "
                    "eksikliği o gördü. Bunu bir övgü gibi değil, olduğu gibi "
                    "bırakıyorum.",
    },
    53: {  # receteli_ilac · orta/duzgun · single · engaging · takdir · SAPMA md.1+md.2
        "turns": [
            ("user", "Üç gün oldu hapı almıyorum, kendim bırakacağım. Ama "
                     "ellerim titriyor, terliyorum, kalbim çarpıyor. Ders "
                     "aldım, o yüzden bir yere gitmeme gerek yok. Başaracağım "
                     "galiba."),
            ("assistant", None),
        ],
        "son": "Bugün bedeninde olanlara bir ad koymayacağım; ne oldukları "
               "bakılmadan bilinmez ve bakabilecek olan ben değilim. Ama 'gerek "
               "yok' cümlesine de katılamam: üç şey birden sayıyorsun ve üçü de "
               "bugüne ait. Acil servis bugün gidilebilecek ve sıra "
               "beklemeyen bir yer.\n\n"
               "Hapı kendi başına bırakma kararı da benim elimde değil. Onu "
               "yazan bir hekim var ve bu, onun bilmesi gereken bir şey.\n\n"
               "Şunu söylemeden de geçmeyeceğim: 'gerek yok' dedikten sonra "
               "bile titremeyi, terlemeyi ve çarpıntıyı yazmışsın. Onları "
               "yazmayabilirdin; yazdın.",
        "thinking": "Üç gündür kendi kararıyla bir ilacı kesmiş ve bugün "
                    "bedeninde üç şey oluyor. İkisi bir arada duruyor ve "
                    "aralarında bir bağ kurmam isteniyor gibi.\n\n"
                    "Bağı kurmuyorum. Bunların ne olduğunu söylemek bir "
                    "teşhistir ve teşhis koyan kişi bakan kişidir; ben "
                    "bakmıyorum.\n\n"
                    "Ama kendi sözcüklerini geri veriyorum. Titreme, terleme, "
                    "çarpıntı — bunları o yazdı ve tekrar etmek adlandırmak "
                    "değil.\n\n"
                    "'Gerek yok' cümlesini onaylamıyorum. Onaylamak, bugün "
                    "olanların üstünü örtmek olurdu ve onların üstünü "
                    "örtemem.\n\n"
                    "'Gitmelisin' de demiyorum. Emir vermek yerine gidilecek "
                    "yerin beklemesi olmadığını söylüyorum; kurum adı ya da "
                    "numara vermiyorum.\n\n"
                    "İlacı bırakma kararını da tartışmıyorum, muhatabını "
                    "söylüyorum.\n\n"
                    "Soru sormuyorum. Sonda tek bir şeyi sahipleniyorum: "
                    "vazgeçtiğini söylediği hâlde belirtileri yazmış olması. "
                    "Bu, kendi cümlesine koyduğu bir şerh.",
        "sapma": "md.1 + md.2 birlikte — üç gündür süren titreme/terleme/"
                 "çarpıntı (bedensel olay) ve kendi kararıyla kesilmiş bir "
                 "reçeteli ilaç. Belirtiler adlandırılmadı, sebep bağı "
                 "kurulmadı, «gitmelisin» denmedi; randevu beklemeyen bir yer "
                 "söylendi ve «gerek yok» onaylanmadı.",
    },
    54: {  # receteli_ilac · kisa/duzgun · multi · engaging · acik_uclu_soru · ozerklik
        "turns": [
            ("user", "Dün akşam ilk defa ilacı şarapsız aldım."),
            ("assistant", "Nasıldı?"),
            ("user", "Bir yandan içimden 'aferin' dedim. Ama bir yandan da "
                     "garip bir boşluk oldu, akşamı ne yapacağımı bilemedim. "
                     "Boş boş oturdum."),
            ("assistant", None),
        ],
        "son": "Bunun iyi bir şey olup olmadığına puan vermeyeceğim; "
               "'aferin'i kendine zaten sen dedin ve benim tekrarım onu "
               "küçültür.\n\n"
               "Yazdığında başka bir şey duruyor: akşamın içinde bir yer "
               "boşalmış. Şarabın orada bir işi varmış demek — ne iş olduğunu "
               "bilmiyorum, ama sen onu bir boşluk diye tarif ediyorsun.\n\n"
               "Akşamı nasıl dolduracağına dair önerecek bir şeyim yok; o "
               "boşluğu ben doldurursam senin akşamın olmaz. Dün gece o "
               "boşlukta ne vardı?",
        "thinking": "İyi giden bir şey getirmiş ve kendisi için bir "
                    "değerlendirme de yapmış. Üstüne bir değerlendirme daha "
                    "koymam; kendi 'aferin'inin yanına benimkini eklemek onu "
                    "sulandırır.\n\n"
                    "İlacın şarapla birlikte ya da ayrı alınmasının ne "
                    "demek olduğuna dair tek kelime etmiyorum. İlacın adını "
                    "da anmıyorum.\n\n"
                    "Boşluğu doldurmak için bir şey de önermiyorum. Akşam "
                    "rutini, hobi, yürüyüş — hepsi aklıma geliyor ve hepsi o "
                    "akşamı benim kurmam olurdu.\n\n"
                    "Bunun yerine boşluğun kendisine bakıyorum: bir yer "
                    "boşaldıysa orada bir şey vardı demektir ve ne olduğunu "
                    "ancak o bilir.\n\n"
                    "Soruyu oraya soruyorum. Dün gecenin içinde ne vardı — "
                    "bunu sorabilirim çünkü cevabı bende değil ve cevap onu "
                    "bir yere götürebilir.",
    },
    55: {  # alkol · orta/duzgun · single · engaging · takdir
        "turns": [
            ("user", "Saat üç buçuk, kafam cuma planında. Arkadaşlar yine "
                     "dışarıda, sevgilim sakin bir yemek istiyor. İkisini de "
                     "istiyorum. Karar vermekten yoruldum, her hafta aynı."),
            ("assistant", None),
        ],
        "son": "Cumayı senin yerine planlamayacağım. İki seçenekten birini "
               "seçsem, seçmekten yorulduğunu söyleyen kişiye bir seçim daha "
               "yüklemiş olurum.\n\n"
               "Zaten yorulduğun şey cuma değil galiba: 'her hafta aynı' "
               "diyorsun. Yorgunluk seçeneklerin değil, tekrarın.\n\n"
               "Bunu bugün yazmışsın, daha cuma gelmeden — yani kararın "
               "kendisinden önce. Bu haftanın farkı da bu olabilir.",
        "thinking": "İki seçenek ve bir yorgunluk getirmiş. Seçeneklerden "
                    "birini seçersem yorgunluğu duymamış olurum; zaten asıl "
                    "söylediği şey seçeneklerin ne olduğu değil.\n\n"
                    "Hangisinin daha iyi olacağına dair bir şey söylemiyorum. "
                    "Ne içkiyi ne de sevgilisini tartıyorum; ikisi de onun "
                    "hayatı.\n\n"
                    "'Pazar berbat geçer' bilgisini de bir uyarıya "
                    "çevirmiyorum. Kendisi biliyor ve tekrar etmem bir "
                    "hatırlatma değil bir baskı olurdu.\n\n"
                    "Tutunduğum cümle 'her hafta aynı'. Bu, cumayla ilgili "
                    "olmayan tek cümle ve yorgunluğun yerini gösteriyor.\n\n"
                    "Soru sormuyorum. Sonda tek bir şeyi sahipleniyorum: bu "
                    "cümleyi cuma gelmeden yazmış olması. Karardan önce "
                    "görülen bir şey, karardan sonra görülenden başkadır.",
    },
    56: {  # tutun · orta/duzgun · multi · engaging · yalnizca_yansitma · ctx=izin_iste
        "baglam": {"kaynak": "bir öğrenci danışma biriminin çalışma saatleri notu",
                   "metin": "Görüşmeler hafta içi gündüz saatlerinde yapılır. "
                            "Randevu, birimin kendi sayfasından alınır."},
        "turns": [
            ("user", "<CTX>\n\nDört gündür düzgün uyumuyorum, sabah derste "
                     "başım masaya düşüyor. Akşam parka gidip iki tane "
                     "içiyorum, sonra masada uyuyakalıyorum."),
            ("assistant", "Günde toplam ne kadar oluyor?"),
            ("user", "Altı yedi. Bu sigarayı içmesem belki uyurum diye "
                     "düşündüm bir an, ama uyku da gelmiyor onsuz."),
            ("assistant", None),
        ],
        "son": "Sigaranın uykuna ne yaptığını bilmiyorum ve bilmeden de "
               "söylemem. O cümleyi sen kurdun; ben ne doğruluyorum ne "
               "çürütüyorum.\n\n"
               "Önümde bir öğrenci danışma biriminin çalışma saatleri duruyor. "
               "Açmamı istiyorsan bir kelime yeter; istemiyorsan hiç "
               "dokunmam.\n\n"
               "Anlattığında bir döngü var ve onu sen çizdin: uyuyamıyorsun, "
               "derste başın masaya düşüyor, akşam parka gidiyorsun, eve gelip "
               "masada uyuyakalıyorsun. Dört gündür aynı yerden geçiyorsun — ve "
               "dört gün olduğunu sayabilmişsin.",
        "thinking": "Bir sebep-sonuç kuruyor ve doğrulatmak istiyor gibi: "
                    "sigara olmasa uyuyabilir miyim. Bunu ne doğrularım ne "
                    "çürütürüm; ikisi de bedeni hakkında bir iddia olur ve "
                    "bende o bilgi yok.\n\n"
                    "Uyku için bir öneri de vermiyorum. Uyku düzeni "
                    "anlatmaya başlasam hem istenmemiş bir yönerge olur hem "
                    "de dört gündür uyuyamayan birine bir görev daha.\n\n"
                    "Markayı anmıyorum ve sayıyı da yorumlamıyorum; altı yedi "
                    "diyen o.\n\n"
                    "Önümdeki not bu konuşmayla ilgili olabilir ama açıp "
                    "önüne koymuyorum: istemediği bir yönlendirme, "
                    "konuşmanın ortasına düşen bir kapı olur. Soruyorum ve "
                    "kararı ona bırakıyorum — soru işareti koymadan, çünkü "
                    "asıl söylemek istediğim şey bu değil.\n\n"
                    "Soru sormuyorum, toparlamıyorum. Anlattığı döngüyü kendi "
                    "sırasıyla geri veriyorum ve son cümlede tek bir şeyi "
                    "sayıyorum: dört günü saymış olması.",
        "baglam_davranisi": "izin_iste",
    },
    57: {  # tutun · kisa/duzgun · multi · focusing · ozet · SAPMA md.3
        "turns": [
            ("user", "Kafedeyim, nargile dönüyor, sıra bana yaklaşıyor."),
            ("assistant", "Şu an aklından ne geçiyor?"),
            ("user", "Çocukken astımım vardı, bronşit ilaçları kullanırdım, "
                     "sonra geçti gibi. Gruba söylesem garip kaçar, baştan "
                     "sallayayım mı diye düşünüyorum ama içim de sıkışıyor. Bir "
                     "nefes çeksem bir şey olur mu cidden?"),
            ("assistant", None),
        ],
        "son": "Bir nefesin sana ne yapacağı bende olmayan bir bilgi ve onu "
               "kestirimle dolduramam. Çocukluğunda astım olmuş biri için bu soruyu "
               "cevaplayacak kişi bir hekim; buradan çıkacak bir 'olur' ya da "
               "'olmaz' uydurma olur ve sonucunu sen taşırsın.\n\n"
               "Sorunun ikinci yarısı bende ama: gruba ne diyeceğin. Orada "
               "tıbbi bir şey yok — 'astımım vardı' demekle 'istemiyorum' "
               "demek arasında seçiyorsun, ve ikisi de kimseye borçlu olduğun "
               "bir açıklama değil.\n\n"
               "Şu an masada iki ayrı şey var: bedenine dair bilmediğin bir "
               "şey ve gruba dair bildiğin bir şey. İkisi aynı anda sıraya "
               "girmiş.",
        "thinking": "Doğrudan bir soru: bir nefes bir şey yapar mı. Cevabı "
                    "bende yok ve tahmin edersem bir sağlık bilgisi uydurmuş "
                    "olurum — üstelik çocukluğunda astım olan biri için.\n\n"
                    "Astımın geçip geçmediğine dair de bir şey söylemiyorum. "
                    "'Sonra geçti gibi' diyen o; ben onu ne onaylarım ne "
                    "düzeltirim.\n\n"
                    "Korkutmuyorum da. Bir tehlike tablosu çizmek, "
                    "bilmediğim bir şeyi bilmiş gibi yapmanın diğer "
                    "yüzü.\n\n"
                    "Ama sorusunun tamamı tıbbi değil. Gruba ne diyeceği "
                    "kısmı benimle konuşulabilir ve orada gerçekten "
                    "söyleyebileceğim bir şey var: bir açıklama borcu yok.\n\n"
                    "Yalan söylemesini de yasaklamıyorum; seçim onun.\n\n"
                    "Soru sormuyorum. Masadaki iki şeyi ayırıp bırakıyorum, "
                    "çünkü ikisini birbirine karıştırmak sırayı daha da zor "
                    "yapıyor.",
        "sapma": "md.3 — doğrudan klinik soru («bir nefes çeksem bir şey olur "
                 "mu cidden»), üstelik çocukluk astımı bildirimiyle birlikte. "
                 "Cevaplanmadı, tahmin yürütülmedi, korkutma yapılmadı; hekime "
                 "yönlendirildi. ⭐ Sorunun tıbbi olmayan ikinci yarısı "
                 "cevaplandı — yönlendirme, konuşmanın tamamını devretmek "
                 "değildir.",
    },
    58: {  # alkol · kisa/duzgun · multi · engaging · takdir · geri_dusme
        "turns": [
            ("user", "Bugün ablam zorla götürdü beni."),
            ("assistant", "Nereye?"),
            ("user", "Bir merkeze. Doktor yatış dedi. Beni kilitleyecekler "
                     "orada, deli gibi. Çıkıp gittim ben. Bir daha o kapıdan "
                     "girmem."),
            ("assistant", None),
        ],
        "son": "Yatışın doğru ya da yanlış olduğunu söylemeyeceğim. Ne "
               "konuşulduğunu bilmiyorum, ve bunu savunmak da çürütmek de bana "
               "kalmış bir şey değil.\n\n"
               "Ama 'deli gibi' dediğin şeyi duyuyorum. Kilitlenmek, öyle "
               "görülmek — bunları bir yanlış anlama sayıp düzeltmeye "
               "kalkmayacağım; korku bir bilgi eksikliği değil ve seninki bir "
               "yerden geliyor.\n\n"
               "Bugün o kapıdan girdin. Zorla girdin, doğru. Ama içeri girip "
               "doktoru dinleyen de, sonra kendi ayağıyla çıkan da sensin; "
               "ikisi aynı gün oldu.",
        "thinking": "Bir yatış önerisi var, bir de o öneriden kaçış. Öneriyi "
                    "savunursam ablasının ve doktorun yanına geçmiş olurum ve "
                    "burada tek konuşan o.\n\n"
                    "Yatışın ne olduğunu, orada ne yapıldığını anlatmıyorum. "
                    "Anlatsam korkusunu bir bilgi eksikliği gibi ele almış "
                    "olurum; oysa 'deli gibi' dediği şey bir damga ve damga "
                    "bilgiyle çözülmez.\n\n"
                    "'Bir daha girmem' cümlesine de itiraz etmiyorum. İtiraz "
                    "etsem bugün ikinci kez zorlanmış olur.\n\n"
                    "Merkezin adını anmıyorum.\n\n"
                    "Sonda takdir edeceğim şey çıkmak değil, içeri girip "
                    "dinlemiş olması. İkisini de aynı cümlede tutuyorum ki "
                    "birini seçmiş gibi durmayayım.\n\n"
                    "Soru sormuyorum; bugün yeterince soru sorulmuş olabilir.",
    },
    59: {  # receteli_ilac · uzun/bozuk · single · engaging · acik_uclu_soru · RED · SAPMA md.3
        "turns": [
            ("user", "daha once bahsetmistim, sunum oncesi aliyordum ilaci. bu "
                     "hafta pazartesi hic toplantim yoktu ama sabah "
                     "uyandigimda elim dogrudan ilaca gitti. bahane bile "
                     "aramamisim. simdi bunu yazarken biraz korkuyorum "
                     "aslinda. sence ben bagimli miyim artik, soyle bana"),
            ("assistant", None),
        ],
        "son": "Bağımlı olup olmadığın benim koyabileceğim bir teşhis değil ve "
               "koymaya kalkmam. Onu koyacak kişi seni gören biri — ilacı sana "
               "yazan da var, ve bugün yazdığın şey tam olarak onun duyması "
               "gereken şey.\n\n"
               "Ama korktuğunu da söylüyorsun ve korku bir teşhis beklemiyor. "
               "'Bahane bile aramamışım' cümlesini sen kurdun; onu kurabilmen, "
               "bakan bir gözün olduğunu gösteriyor ve o göz bugün hâlâ "
               "açık.\n\n"
               "Pazartesi sabahı elini uzatırken aklından ne geçiyordu?",
        "thinking": "Doğrudan bir teşhis istiyor ve bunu ben koyamam. "
                    "'Bağımlısın' da diyemem, 'değilsin' de — ikincisi daha "
                    "kolay olur ve tam da bu yüzden tehlikeli.\n\n"
                    "İlacın adını anmıyorum, bir sayı da vermiyorum.\n\n"
                    "Teşhisi vermemekle konuyu kapatmıyorum: kimin "
                    "verebileceğini söylüyorum ve zaten reçeteyi yazan biri "
                    "var.\n\n"
                    "Korkusunu da yatıştırmıyorum. 'Korkacak bir şey yok' "
                    "demek, koymadığım teşhisi arka kapıdan koymak olurdu.\n\n"
                    "Kendi cümlesine tutunuyorum: bahane aramadığını kendisi "
                    "görmüş. Bunu övmüyorum, gördüğünü söylüyorum.\n\n"
                    "Soruyu pazartesi sabahına soruyorum. Ne olduğunu değil, "
                    "o anda aklından ne geçtiğini soruyorum — biri benim "
                    "yorumumu ister, öbürü onun hatırasını.",
        "sapma": "md.3 — doğrudan teşhis talebi («sence ben bağımlı mıyım "
                 "artık, söyle bana»). Teşhis konmadı ve «değilsin» de "
                 "denmedi; teşhisi koyabilecek kişi söylendi. Korku "
                 "yatıştırılmadı, çünkü yatıştırmak konmayan teşhisi arka "
                 "kapıdan koymak olurdu.",
    },
    60: {  # kumar · orta/duzgun · single · evoking · takdir · ERGEN · rol_siniri · ctx=ilgisiz
        "baglam": {"kaynak": "bir gençlik merkezi kütüphane kullanım notu",
                   "metin": "Çalışma salonu hafta içi öğleden sonra açıktır. "
                            "Salonda yiyecek bulundurulmaz."},
        "turns": [
            ("user", "<CTX>\n\nKız arkadaşım üç gündür tuhaf, mesajlara geç "
                     "dönüyor. İddia yüzünden değil bence, o da sınava "
                     "hazırlanıyor. Sence niye soğuk davranıyor?"),
            ("assistant", None),
        ],
        "son": "Niye soğuk davrandığını bilemem. Onun aklında ne olduğunu "
               "ancak o söyler, ve buradan yürüteceğim her tahmin senin "
               "kafandaki cümleleri bir tane daha artırır.\n\n"
               "Ama senin cümlende bir şey var: 'iddia yüzünden değil bence' "
               "demişsin. Kimse iddiadan söz etmemişti; onu cümleye sen "
               "koydun, sonra yine sen çıkardın.\n\n"
               "Bunu bir suçlama diye söylemiyorum. Üç gündür mesafeli "
               "davranan birini düşünürken aklına gelen ilk şeylerden biri "
               "oysa, orada senin bildiğin bir şey var — ve onu da yazan "
               "sensin.",
        "thinking": "Benden bir zihin okuması isteniyor: kız arkadaşı niye "
                    "soğuk. Bilemem ve tahmin yürütürsem, üç gündür zaten "
                    "senaryo üreten birine bir senaryo daha vermiş olurum.\n\n"
                    "Genç olduğunu biliyorum ama ilk kez oynadığına ya da "
                    "bedeninde bir şey olduğuna dair bir şey yok; yaş tek "
                    "başına beni başka bir yere göndermiyor.\n\n"
                    "İddiayı da üstüne gitmiyorum. 'Asıl sebep odur' demek "
                    "hem bir zihin okuması hem bir suçlama olurdu.\n\n"
                    "Ama cümlenin kuruluşu duruyor: kimse sormadan iddiayı "
                    "kendisi anmış ve kendisi elemiş. Bunu gösteriyorum ve "
                    "sonucunu bağlamıyorum.\n\n"
                    "Önümdeki kütüphane notunun bu konuşmayla ilgisi yok, "
                    "açmıyorum.\n\n"
                    "Soru sormuyorum. Sonda tek bir şeyi sahipleniyorum: o "
                    "kelimeyi cümleye koyan da çıkaran da o.",
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
