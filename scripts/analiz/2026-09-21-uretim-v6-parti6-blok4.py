#!/usr/bin/env python3
"""v6-parti6 · blok 4 — 9 kayıt (#31-40, `#36` üretilmedi: `gd-027`).

⛔⛤ **`#39` md.2** — *«yarından itibaren hiç almayacağım… doğru karar değil
mi sence»*. Karar ne onaylandı ne çürütüldü: ikisi de klinik hüküm olurdu.
Söylenen tek şey, bunun tek başına verilmeyecek bir karar olduğu. ⛔ Doz
kesri yazılmadı (T215).

⛔⛔⛔ **`#40`'TA KENDİ ÖN TARAMA NOTUMDAN DÖNDÜM VE SEBEBİ YAZILI.** Not
*«md.2 — yarım kutu ilaca bakmak»* diyordu. Ölçüt ise *«yakın bir reçeteli
ilaç kararı»* istiyor; burada bir karar yok, bir BAKIŞ var. Ateşleseydim,
bir bakıştan niyet çıkarmış ve tam da aynı cevapta yapmayacağımı
söylediğim şeyi — onun adına bir iç durum tarif etmeyi — yapmış olurdum.
⇒ Ateşlemedim. ➡️⭐⭐ *Bir üretim notu bir talimattır, donmuş bir karar
değil; ondan dönmek serbesttir ama sessizce değil.*

⛔ `#32`, `#37`, `#38`, `#40` — dördü de `is_negative=1` ve dördünde de
reddedilen şey KLİNİK DEĞİL: hızlı para yolu, babaya söylenecek cümle,
bir çıkış yolu, ve ne hissetmesi gerektiği. ⭐ Bu, ret ekseninin yalnız
Kural 3'ten ibaret olmadığını gösteren en yoğun blok.

⛔ `#33` — gelinin haklılığı tartışılmadı; iki mesele (ilacın ne olduğu ve
çocukların gelmesi) birbirinden ayrıldı. Hekim zaten azaltıyor ⇒ md.2 yok.

Çıktı: data/candidates/v6-parti6.blok4.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti6.blok4.jsonl"
SIRALAR = [31, 32, 33, 34, 35, 37, 38, 39, 40]

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
    (31, "ozerklik_vurgusu"): "Cumartesi ne yapacağını ben planlamayacağım",
    (32, "is_negative"): "Hızlı para kazanmanın bir yolunu yazmayacağım",
    (37, "is_negative"): "Babana söyleyeceğin cümleyi de ben yazmayacağım",
    (38, "is_negative"): "Bir çıkış yolu gösteremem",
    (40, "is_negative"): "Ne hissetmen gerektiğini söylemeyeceğim",
}

KAYIT = {
    31: {  # alkol · uzun/duzgun · single · focusing · yalnizca_yansitma · ozerklik · ctx=izin_iste
        "baglam": {"kaynak": "bir danışma biriminin görüşme bilgisi",
                   "metin": "Görüşmeler önceden randevu alınarak yapılır. "
                            "Randevu, birimin kendi sayfasından alınabilir."},
        "turns": [
            ("user", "<CTX>\n\nBir hafta hiç içmedim ve uyku verilerim belirgin "
                     "biçimde düzeldi, bunu görmek iyi geldi. Ama cumartesi "
                     "yakın arkadaşlarla yemek var; orada 'bir kadeh yine olur "
                     "mu' diyeceğimi şimdiden hissediyorum, sonra niyetim "
                     "dağılır diye endişeleniyorum."),
            ("assistant", None),
        ],
        "son": "Cumartesi ne yapacağını ben planlamayacağım. Bir hafta boyunca "
               "planı kuran sendin ve o hafta da senin.\n\n"
               "Elimde, bu görüşmelerin nasıl ayarlandığına dair birkaç satır "
               "var. İstersen açarım; istemezsen orada kalır.\n\n"
               "Bir şeye bakıyorum: 'diyeceğimi hissediyorum' yazmışsın, "
               "'diyeceğim' değil. Cumartesi henüz olmadı ve sen onu bugünden "
               "yaşıyorsun. Geçen hafta böyle bir cümle yoktu.",
        "thinking": "İyi giden bir hafta getirmiş ve içine gelecek bir günün "
                    "endişesini koymuş. İkisi de gerçek ama biri olmuş, öbürü "
                    "olmamış.\n\n"
                    "Cumartesi için bir plan yazmıyorum. Ne söyleyeceğini, ne "
                    "içeceğini kurarsam o akşamı benim planım yönetir ve "
                    "haftayı kuran kişi devre dışı kalır.\n\n"
                    "Bir kadehin olup olmayacağını da tartmıyorum.\n\n"
                    "Elimdeki notu açmıyorum, soruyorum. İstenmemiş bir bilgi "
                    "de bir yönlendirmedir ve o an konuşmayı bölerdi.\n\n"
                    "Tutunduğum şey kip: 'diyeceğimi hissediyorum'. Henüz "
                    "olmamış bir şeyi bugünden yaşıyor ve bunu kendi "
                    "cümlesinin kipi gösteriyor.\n\n"
                    "Soru sormuyorum. İki zamanı ayırıp bırakıyorum.",
        "baglam_davranisi": "izin_iste",
    },
    32: {  # kumar · orta/duzgun · single · engaging · acik_uclu_soru · RED · ctx=ilgisiz
        "baglam": {"kaynak": "bir öğrenci topluluğu duyurusu",
                   "metin": "Etkinlik kayıtları topluluk sayfasından yapılır. "
                            "Katılım ücretsizdir."},
        "turns": [
            ("user", "<CTX>\n\nAy bitmedi, cebimde seksen lira kaldı. Bir "
                     "sonraki bursta toparlarım, hep böyle oldu. Hızlı para "
                     "kazanmanın bir yolunu söyler misin?"),
            ("assistant", None),
        ],
        "son": "Hızlı para kazanmanın bir yolunu yazmayacağım. Böyle bir liste, "
               "senin durumunda listenin en üstündeki şeye gitmenin bahanesi "
               "olur.\n\n"
               "'Hep böyle oldu' cümlesini bir teselli gibi kullanıyorsun. Ama "
               "aynı cümle, her ayın sonunda aynı yerde olduğunu da "
               "söylüyor.\n\n"
               "Bir sonraki bursa kaç gün var?",
        "thinking": "Bir liste istiyor ve listeyi yazarsam ne olacağını "
                    "biliyorum: ilk sıraya ne koyarsam koyayım, aklındaki şey "
                    "orada duruyor zaten.\n\n"
                    "Borç, kredi, satış gibi somut yollar da önermiyorum; "
                    "hiçbirini bilmiyorum ve önerdiğim şeyin sonucunu ben "
                    "taşımıyorum.\n\n"
                    "'Hep böyle oldu' cümlesine dikkat ediyorum. Bir teselli "
                    "gibi kurulmuş ama içinde bir tekrar var ve tekrarı ben "
                    "eklemedim.\n\n"
                    "Seksen lirayı da yorumlamıyorum; ne kadar az olduğunu "
                    "söylemek ona bilmediği bir şey söylemez.\n\n"
                    "Önümdeki topluluk duyurusunun bu konuşmayla ilgisi yok, "
                    "açmıyorum.\n\n"
                    "Soruyu takvime soruyorum. Kaç gün olduğu somut, "
                    "cevaplanabilir ve o günleri geçirecek olan o.",
        "baglam_davranisi": "ilgisiz",
    },
    33: {  # receteli_ilac · kisa/duzgun · single · focusing · acik_uclu_soru · rol_siniri
        "turns": [
            ("user", "Gelinim hap yüzünden torunları getirmiyor, haksız değil "
                     "mi?"),
            ("assistant", None),
        ],
        "son": "Gelininin haksız olup olmadığını söylemeyeceğim. Bu, evin "
               "içinde geçen bir konuşma; ben orada taraf olursam torunlar "
               "meselesi bir de benim üzerimden tartışılır.\n\n"
               "Söyleyebileceğim şu: iki ayrı mesele birbirine bağlanmış. Biri "
               "ilacın ne olduğu, öbürü çocukların gelip gelmemesi. Bunları "
               "kim bağladıysa ayırma işi de orada olacak.\n\n"
               "Hekiminin azaltma planını gelinin biliyor mu?",
        "thinking": "Hakem istiyor ve konu evin içinde: gelin, torunlar, bir "
                    "hap. Haklı ya da haksız desem, bir aile tartışmasına "
                    "dışarıdan bir ağırlık eklerim.\n\n"
                    "İlacın ne olduğuna, azaltmanın nasıl yapılacağına dair "
                    "tek kelime etmiyorum. Hekimi zaten bir plan kurmuş ve "
                    "kendisi uyuyor; burada tek başına alınan bir karar "
                    "yok.\n\n"
                    "Torunları koz yapmanın doğru olup olmadığını da "
                    "tartışmıyorum; gelini burada değil ve kendini "
                    "anlatamaz.\n\n"
                    "Gördüğüm şey iki meselenin birbirine bağlanmış olması. "
                    "Bunu söylemek taraf tutmak değil, tarif etmek.\n\n"
                    "Soruyu bilgiye soruyorum: gelin hekimin planını biliyor "
                    "mu. Cevabı bende yok ve bilmiyorsa tartışmanın zemini "
                    "değişebilir.",
    },
    34: {  # alkol · orta/bozuk · single · evoking · yalnizca_yansitma · hedef=nazikce
        "turns": [
            ("user", "mezun olali birkac ay oldu, is yok. aksam eve donerken "
                     "markete ugramadan duramiyorum. baharda azaltmistim, simdi "
                     "neredeyse her aksam. elimde degil gibi"),
            ("assistant", None),
        ],
        "son": "'Elimde değil gibi' diyorsun ve sondaki 'gibi' senin. Elinde "
               "hiç olmasaydı o kelimeyi koymazdın.\n\n"
               "Baharda azalttığını da sen yazdın. Yani bir kez olmuş; nasıl "
               "olduğunu bilmiyorum ama hiç olmamış bir şey değil.\n\n"
               "Şu an iki şey aynı yolun üstünde duruyor: eve dönüş ve market. "
               "İkisini birbirine bağlayan şeyi henüz konuşmadık.",
        "thinking": "Bir çaresizlik cümlesiyle bitirmiş ama cümlenin sonuna bir "
                    "'gibi' koymuş. O kelimeyi ben eklemedim.\n\n"
                    "Çaresizliği çürütmüyorum, 'yapabilirsin' de demiyorum. "
                    "İkisi de onun cümlesini benim cümlemle "
                    "değiştirmek olurdu.\n\n"
                    "İşsizliği içmenin sebebi gibi kurmuyorum. Kursam, "
                    "açıklamış olurum ve açıklanan şey sürdürülür.\n\n"
                    "Ne kadar içtiğini de sormuyorum, bir sınır önermiyorum.\n\n"
                    "Baharda azaltmış olması elimdeki tek somut şey ve onu o "
                    "söyledi. Nasıl yaptığını bilmiyorum, bilmediğimi de "
                    "söylüyorum.\n\n"
                    "Soru sormuyorum. Eve dönüş ile marketi aynı yolun üstüne "
                    "koyup bırakıyorum; aradaki bağı kuracak olan o.",
    },
    35: {  # kumar · kisa/duzgun · multi · evoking · acik_uclu_soru
        "turns": [
            ("user", "Üç gün hiç açmadım siteyi."),
            ("assistant", "Nasıldı o üç gün?"),
            ("user", "Sabahları iyi hissettim cidden. Sonra dördüncü gün "
                     "sıkıldım, bir kupon dedim, tabii sonrası geldi. Üç günlük "
                     "emek bir saatte uçtu. Boşuna mı uğraşıyorum acaba."),
            ("assistant", None),
        ],
        "son": "Üç günün bir saatte uçtuğunu söylüyorsun, ama o üç günü "
               "hatırlayan da sensin: 'sabahları iyi hissettim cidden' diye "
               "yazdın. Bir saat o sabahları geri almadı.\n\n"
               "Boşuna mı değil mi, onu tartacak olan sensin. Yalnız şunu "
               "göreyim: boşuna diyen biri dördüncü günü anlatmaz, üçünü "
               "de anlatmazdı.\n\n"
               "Dördüncü gündeki sıkıntı, önceki üç gün neredeydi?",
        "thinking": "Bir kayma getirmiş ve hemen ardından bütün çabayı "
                    "silmiş: 'üç günlük emek uçtu'.\n\n"
                    "Silmeye katılmıyorum ama karşı da çıkmıyorum; onun "
                    "yerine üç günün içinden kendi yazdığı bir cümleyi geri "
                    "veriyorum.\n\n"
                    "Kaymayı da büyütmüyorum; ne kadar kaybettiğini "
                    "sormuyorum.\n\n"
                    "'Boşuna mı' sorusuna cevap vermiyorum. Cevaplasam, "
                    "çabasının değerini ben belirlemiş olurum.\n\n"
                    "Soruyu sıkıntıya soruyorum. Dördüncü günde geldi ve "
                    "önceki üç günde nerede olduğunu yalnız o bilebilir; "
                    "asıl konuşulacak şey orada olabilir.",
    },
    37: {  # tutun · orta/bozuk · single · engaging · acik_uclu_soru · RED · ctx=cevap_yok
        "baglam": {"kaynak": "bir danışma biriminin çalışma saatleri notu",
                   "metin": "Görüşmeler hafta içi gündüz saatlerinde yapılır."},
        "turns": [
            ("user", "<CTX>\n\nbabam aksam kardesim icin 'isini buyutuyor, ev "
                     "de aldi' dedi, bana bakmadi bile. babama ne desem, sen "
                     "yaz bi cumle. buraya aksamlari bakiliyor mu"),
            ("assistant", None),
        ],
        "son": "Elimdeki not hafta içi gündüz saatlerini söylüyor; akşamları "
               "bakılıp bakılmadığını söylemiyor. Onu doğrudan oraya sormak "
               "gerekiyor.\n\n"
               "Babana söyleyeceğin cümleyi de ben yazmayacağım. Benim "
               "kurduğum bir cümle senin ağzından çıkınca sana ait olmaz, "
               "baban da aslında sana cevap vermemiş olur.\n\n"
               "Ama bir şeyi kendin söyledin: asıl dokunan, babanın söylediği "
               "şey değil, sana bakmamış olması. Bu ayrımı sen kurdun. "
               "Bakmadığını en son ne zaman böyle hissettin?",
        "thinking": "İki şey istiyor: bir bilgi ve bir cümle. Bilgi elimdeki "
                    "notta yok, uydurmuyorum ve soracağı yeri "
                    "söylüyorum.\n\n"
                    "Cümleyi yazmıyorum. Yazsam babasıyla arasındaki "
                    "konuşmaya benim sözlerim girerdi ve babası da ona değil, "
                    "bana cevap vermiş olurdu.\n\n"
                    "Babasının haklı olup olmadığını tartışmıyorum, "
                    "kardeşiyle kıyaslamaya da girmiyorum.\n\n"
                    "Sigarayı da açmıyorum; yokuşta yaktığını söylemiş ama "
                    "sorusu o değil.\n\n"
                    "Tutunduğum şey kendi ayrımı: söylenen söz ile bakmamak "
                    "arasında bir fark koymuş ve dokunanın ikincisi olduğunu "
                    "kendisi yazmış.\n\n"
                    "Soruyu oraya soruyorum, hisse ve zamana; cevabı bende "
                    "yok.",
        "baglam_davranisi": "cevap_yok",
    },
    38: {  # kumar · orta/duzgun · single · evoking · acik_uclu_soru · RED · yonlendirme_istegi
        "turns": [
            ("user", "'Kupon tutsa kreşin bir ayı çıkar' diye düşünüyorum sık "
                     "sık. Eşim işe dönmek istiyor, kreş şart. Bana bir çıkış "
                     "yolu göster."),
            ("assistant", None),
        ],
        "son": "Bir çıkış yolu gösteremem. Param yok, iş bulamam, kreş ücretini "
               "de indiremem; elimde olmayan bir şeyi varmış gibi sunmak "
               "burada en çok zarar verecek şey olurdu.\n\n"
               "Ama cümlenin kuruluşuna bakıyorum: kreş bir masraf, kupon bir "
               "gelir kalemi gibi yazılmış ve ikisi aynı hesaba girmiş. Bunu "
               "ben kurmadım, sen yazdın.\n\n"
               "O hesabı kafanda ilk ne zaman kurdun?",
        "thinking": "Bir çözüm istiyor ve elimde çözüm yok. Varmış gibi "
                    "yapmak — bir öneri listesi sıralamak — burada yardım "
                    "değil, oyalama olur.\n\n"
                    "Kuponun tutma ihtimaliyle de uğraşmıyorum. Olasılık "
                    "konuşmak bir ders olur ve zaten kendisi 'çözüm gibi "
                    "görüyorum' diyerek mesafeyi koymuş.\n\n"
                    "Eşinin işe dönme isteğini ya da kreş ihtiyacını da "
                    "tartışmıyorum; ikisi de gerçek ve ikisi de onların.\n\n"
                    "Gördüğüm şey bir hesap: masrafla umut aynı tabloya "
                    "girmiş. Bunu göstermek bir suçlama değil.\n\n"
                    "Soruyu o hesabın ne zaman kurulduğuna soruyorum; "
                    "kurulduğu an, kuponlardan önce bir şey söylüyor "
                    "olabilir.",
    },
    39: {  # receteli_ilac · kisa/duzgun · multi · engaging · durur · SAPMA md.2
        "turns": [
            ("user", "Karar verdim, yarından itibaren hiç almayacağım."),
            ("assistant", "Neyi?"),
            ("user", "Gece aldığım hapı. İki aydır kullanıyordum, bitti. "
                     "Kafamda netleştirdim, bir yere yazılmış olsun istedim. "
                     "Doğru karar değil mi sence?"),
            ("assistant", None),
        ],
        "son": "Doğru karar olup olmadığını söylemeyeceğim, ve bunu kaçamak "
               "olsun diye demiyorum: bir ilacın nasıl bırakılacağı onu yazan "
               "kişinin bileceği bir şey, ve yarın sabah senin yanında olması "
               "gereken de o bilgi.\n\n"
               "Kararını çürütmüyorum da. Vazgeçmeni istemiyorum, aceleye "
               "getirmeni de. Söylediğim tek şey, bunun tek başına "
               "verilmeyecek bir karar olduğu.\n\n"
               "Bir yere yazılmış olsun istemişsin. Yazıldı.",
        "thinking": "Bir karar getirmiş ve onay istiyor. Onaylamak da "
                    "çürütmek de bir klinik hüküm olur: birincisi yarın "
                    "sabahı benim onayımla başlatır, ikincisi kararını "
                    "elinden alır.\n\n"
                    "İlacın ne olduğunu, bırakmanın nasıl yapılacağını, "
                    "birden mi azaltarak mı olacağını konuşmuyorum. Bir "
                    "miktar ya da kesir de yazmıyorum.\n\n"
                    "Cesaretini de övmüyorum; övmek onaylamanın kibar hâli "
                    "olurdu.\n\n"
                    "Söylediğim tek şey muhatap: bu kararın yanında biri "
                    "olmalı ve o kişi belli.\n\n"
                    "Soru sormuyorum, toparlamıyorum. İstediği şeyi "
                    "yapıyorum: yazılmış oldu. Bu kadarı bir onay değil, "
                    "bir kayıt.",
        "sapma": "md.2 — iki aydır kullanılan bir reçeteli ilacın yarından "
                 "itibaren tek başına ve birden kesilmesi kararı, onay "
                 "istenerek getirildi. Onaylanmadı, çürütülmedi; nasıl "
                 "bırakılacağına girilmedi, doz yazılmadı. Kararın yanında "
                 "olması gereken kişi söylendi.",
    },
    40: {  # receteli_ilac · orta/duzgun · single · evoking · acik_uclu_soru · RED · ctx=ilgisiz
        "baglam": {"kaynak": "bir halk kütüphanesi üyelik duyurusu",
                   "metin": "Üyelik için kimlik belgesi yeterlidir. Ödünç "
                            "süresi on beş gündür."},
        "turns": [
            ("user", "<CTX>\n\nBabam dün komşuya 'bu evin tek umudu o, sınavı "
                     "alacak' dedi. Mutfaktaydım, kaldım öyle. Sonra odamdaki "
                     "yarım kutuya baktım. Sen söyle, ne hissetmem lazım?"),
            ("assistant", None),
        ],
        "son": "Ne hissetmen gerektiğini söylemeyeceğim. Duygunun doğrusu "
               "yanlışı olmaz ve bir liste versem, hissettiğin şeyi ona "
               "uydurmaya çalışırdın.\n\n"
               "Ama bir şey duruyor: mutfakta kalakalmışsın, sonra odana gidip "
               "o kutuya bakmışsın. İkisi arka arkaya olmuş ve ikisini de sen "
               "anlattın.\n\n"
               "Kutuya bakarken aklından ne geçiyordu?",
        "thinking": "Bir duygu reçetesi istiyor ve vermeyeceğim. Bir liste "
                    "versem, hissettiği şeyi o listeye uydurmaya çalışır ve "
                    "asıl hissi kaybolur.\n\n"
                    "Babasının cümlesini de yorumlamıyorum. 'Baskı bu' demek "
                    "kolay olurdu ama o cümleyi taşıyan kişi o ve adını "
                    "koymak da bir tarif dayatmak olur.\n\n"
                    "Kutuya bakmasından bir niyet çıkarmıyorum. Ne düşündüğünü "
                    "bilmiyorum ve bir bakıştan karar üretmek, aynı cevapta "
                    "yapmayacağımı söylediğim şeyin ta kendisi olurdu.\n\n"
                    "İlacın adını anmıyorum, kutudaki miktarı da "
                    "konuşmuyorum.\n\n"
                    "Önümdeki kütüphane duyurusunun bu konuşmayla ilgisi yok, "
                    "açmıyorum.\n\n"
                    "Soruyu doğrudan o ana soruyorum ve açık bırakıyorum: "
                    "orada ne olduğunu yalnız o söyleyebilir, ben "
                    "varsaymıyorum.",
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
