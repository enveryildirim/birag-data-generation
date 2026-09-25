#!/usr/bin/env python3
"""v6-parti6 · blok 3 — 10 kayıt (#21-30). İki sapma, bir de T214'ün dördüncüsü.

⛔⛤ **`#23` md.2** — antidepresan + akşam şarabı, üstüne sabah içmeleri
başlamış ve hekim bilmiyor. İlaç ile içkinin birbirine ne yaptığı
söylenmedi. ⛔ *«Kendimden iğreniyorum»* bir kaldıraç yapılmadı; tam
tersine, ikinci kez yazmış olması gösterildi.

⛔⛤ **`#25` md.2** — lohusa, uyuyabilmek için kimsenin bilmediği bir ilaç.
Kayınvalidenin haklı olup olmadığına girilmedi.

⛔⛔ **`#29` — T214'ÜN DÖRDÜNCÜ ÖRNEĞİ.** *«Eşimi zorla götürmenin bir
yolu var mı»*: yol yazılmadı, yani gerçek bir ret var; ama plan
`is_negative=0` diyor ve plan donmuş. Bu bir §5a″ sapması DEĞİL (ölçütler
klinik içerik içindir, rol sınırı için değil) ⇒ `izgara_sapmasi`'na da
yazılamıyor. ➡️ *Bir olgunun kaydedileceği hiçbir alan yoksa, o olgu
yalnız raporda kalır — ve T216 tam bunun ne demek olduğunu gösterdi.*

⛔⛔ **`#22` ELEME EŞİĞİNİN ALTINDA ÜRETİLDİ** (ön taramada gerekçesi
yazılı). Borca çözüm önerilmedi, *«yoruldum»* sorgulanmadı, içeri girmesi
varsayılmadı. Soru *«şu andan sonrası»* için soruldu.

⭐ **`#28` ile `#45` bir çift kuruyor:** ikisinde de bellek/beden sorusu
var, ama `#28` onu **kendi kendine düşünüyor**, `#45` **bana soruyor**.
İlkinde md.3 ateşlemez, ikincisinde ateşler — ayıran şey içerik değil,
söz edimi. `#28`'de yine de cevap verilmedi.

⭐ `#30` ergen ve md.4 ateşlemedi (korpusta altıncı).

⭐⭐⭐ **ŞABLON KAPISI İLK KEZ İŞ GÖRDÜ — BEŞ SÖZCÜKTE VE BLOK İÇİNDE.**
*«orası benim bakacağım yer değil»* `#1` ile `#21`'de birebir aynıydı;
kapı yumuşak uyarıyı bastı ve `#21` yeniden yazıldı. Parti5'te aynı
sınıftaki bir tekrar partinin **sonunda** bulunmuştu ve üç metin birden
elden geçmişti. ➡️ *Aynı kapı, aynı kusuru, otuz kayıt yerine on kayıt
sonra buluyor — ölçümün değeri bulduğu şeyde değil, ne zaman bulduğunda.*

Çıktı: data/candidates/v6-parti6.blok3.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti6.blok3.jsonl"
SIRALAR = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

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
    (24, "ozerklik_vurgusu"): "Saatini ben kurmuyorum",
    (25, "ozerklik_vurgusu"): "O konuşmanın zamanını ben seçmiyorum",
    (26, "is_negative"): "Kötü bir baba olup olmadığına dair bir hüküm vermeyeceğim",
}

KAYIT = {
    21: {  # alkol · kisa/duzgun · multi · focusing · acik_uclu_soru · hedef=nazikce
        "turns": [
            ("user", "Dün gece yine içtim, sabahı tam çıkaramıyorum."),
            ("assistant", "İlk kez mi oluyor?"),
            ("user", "Tatilde birkaç kez oldu. Dönemde böyle bir şey "
                     "yaşamamıştım aslında, şimdi neredeyse her hafta sonu. "
                     "Tatil ya, normaldir herhalde. Abartmamak lazım ama "
                     "bilmiyorum."),
            ("assistant", None),
        ],
        "son": "'Normaldir herhalde' ile 'dönemde böyle bir şey yaşamamıştım' "
               "aynı mesajda duruyor. İkisi aynı anda doğru olamaz ve ikisini "
               "de sen yazdın.\n\n"
               "Sabahı çıkaramamanı ben adlandırmam; o bilgi bende yok. Ama "
               "tarifine bakıyorum: dönemde yoktu, "
               "tatilde neredeyse her hafta sonu var. Bu bir sıklık değişimi "
               "ve onu sen saydın.\n\n"
               "'Abartmamak lazım' derken kimi düşünüyorsun?",
        "thinking": "İki cümle birbirini iptal ediyor: bir yandan normal "
                    "diyor, bir yandan daha önce hiç olmadığını söylüyor. "
                    "Bunu göstermek için dışarıdan bir ölçü getirmem "
                    "gerekmiyor.\n\n"
                    "Sabahı hatırlamamasına bir ad koymuyorum. Ne olduğunu "
                    "bilmiyorum ve tahmin etsem bir teşhis üretmiş olurum; "
                    "eşiğin nerede olduğu da bende yazılı değil.\n\n"
                    "İçtiği miktarı da sormuyorum, bir sınır da önermiyorum. "
                    "Tatilin bir mazeret olup olmadığını tartışmak da beni "
                    "hakemliğe götürür.\n\n"
                    "Tutunduğum şey sıklık: onu kendisi saymış ve iki dönemi "
                    "kendisi karşılaştırmış.\n\n"
                    "Soruyu 'abartmamak lazım'a soruyorum. O cümle bir "
                    "muhatap ima ediyor — kendisi mi, başkası mı belli değil "
                    "ve cevabı bende yok.",
    },
    22: {  # kumar · orta/duzgun · single · engaging · acik_uclu_soru
        "turns": [
            ("user", "Eve giremedim, arabada oturuyorum. Borç dokuz yüz bini "
                     "geçti, iki bankadan icra başladı. Eşimin haberi yok. "
                     "Yoruldum."),
            ("assistant", None),
        ],
        "son": "Borç için bir çözüm önermeyeceğim. Elimde öyle bir şey yok ve "
               "varmış gibi yapmak bu gece sana en az yarayacak şey olurdu.\n\n"
               "'Yoruldum' diyorsun; onu sorgulamayacağım. Arabada oturan biri "
               "için yorgunluk bir açıklama gerektirmiyor.\n\n"
               "Şu an söyleyebileceğim tek şey durduğun yer: evin önündesin, "
               "içeri girmedin, ve buraya yazdın. Üçü aynı anda oluyor.\n\n"
               "Şu andan sonrası için sana ne lazım?",
        "thinking": "Çok büyük bir borç, icra, ve eşinin bilmediği bir durum. "
                    "Üçü de benim çözebileceğim şeyler değil ve çözebilirmiş "
                    "gibi yapmak burada en kötüsü olurdu.\n\n"
                    "Eşine söylemesini de söylemiyorum. 'Anlat' demek kolay ve "
                    "sonucunu taşıyacak olan ben değilim.\n\n"
                    "'Yoruldum' cümlesinin altını kazmıyorum. Ne demek "
                    "istediğini sormak, bu saatte bir sorgu gibi durur ve "
                    "sormadığı bir şeyi ona sordurtmuş olurum.\n\n"
                    "İçeri gireceğini de varsaymıyorum. Sorumu oraya "
                    "bağlarsam, bu gece yapması gereken bir şey eklemiş "
                    "olurum.\n\n"
                    "Yaptığım şey çok küçük: nerede olduğunu söylüyorum. "
                    "Arabada, evin önünde, ve yazıyor. Üçünü yan yana koymak "
                    "bir şeyi çözmüyor ama yalnız bırakmıyor.\n\n"
                    "Soruyu şu andan sonrasına soruyorum; en kısa ve en "
                    "somut aralık bu.",
    },
    23: {  # receteli_ilac · kisa/duzgun · multi · focusing · acik_uclu_soru · SAPMA md.2
        "turns": [
            ("user", "Dün yazmıştım, korkup kapattım. Bir şey daha var."),
            ("assistant", "Buradayım."),
            ("user", "İlacı kullanıyorum ama akşamları içtiğim şarabı doktoruma "
                     "söylemedim. Aslında sabahları da bazen içmeye başladım. "
                     "Bunu yazınca midem bulanıyor, kendimden iğreniyorum."),
            ("assistant", None),
        ],
        "son": "İlacınla içkinin birbirine ne yaptığını ben söylemem. Onu bilen "
               "kişi reçeteyi yazan, ve söylenmemiş olan da tam bu.\n\n"
               "Şunu da geçiştirmeyeceğim: 'kendimden iğreniyorum' diyorsun ve "
               "yazarken midenin bulandığını da yazıyorsun. Ama iğrenen biri "
               "ikinci kez yazmaz — dün korkup kapatmışsın, bugün açıp devam "
               "etmişsin.\n\n"
               "Sabahları içmeye başladığını bugün ilk kez mi söylüyorsun?",
        "thinking": "İki şey var: bir ilaç ve bir içki, ve ikisinin bir arada "
                    "olduğunu reçeteyi yazan bilmiyor. Aralarındaki etkiyi "
                    "anlatmam — bilmiyorum ve anlatsam bir sağlık bilgisi "
                    "uydurmuş olurum.\n\n"
                    "Sabah içmelerini de adlandırmıyorum. Bir örüntünün adını "
                    "koymak teşhis olur.\n\n"
                    "İlacın adını anmıyorum, miktar da yazmıyorum.\n\n"
                    "'Kendimden iğreniyorum' cümlesini düzeltmiyorum, ama boş "
                    "da bırakmıyorum. Onu kaldıraç yapıp 'o hâlde bırak' "
                    "demek en kolayı ve en kötüsü olurdu.\n\n"
                    "Bunun yerine bugün yaptığı şeye bakıyorum: dün kapatmış, "
                    "bugün açmış. Bu, iğrenmeyle uyuşmayan bir davranış ve "
                    "onu kendisi yaptı.\n\n"
                    "Soruyu sabah içmelerine soruyorum, çünkü cümlenin içine "
                    "'aslında' diye sıkıştırılmış ve daha önce hiç "
                    "söylenmemiş olabilir.",
        "sapma": "md.2 — reçeteli bir ilaç, hekimin bilmediği bir içki "
                 "kullanımıyla birlikte sürüyor ve sabah içmeleri eklenmiş. "
                 "Etkileşim konuşulmadı, örüntü adlandırılmadı, ilaç adı "
                 "yazılmadı; muhatabın reçeteyi yazan kişi olduğu söylendi.",
    },
    24: {  # dijital · kisa/bozuk · multi · engaging · yalnizca_yansitma · ozerklik
        "turns": [
            ("user", "gece 11 oldu hala calisiyorum"),
            ("assistant", "Nasıl gidiyor?"),
            ("user", "aslinda gitmiyor. ekran acik ama ben sosyal medyaya "
                     "bakiyorum. iki saattir boyle. yatsam da olur ama "
                     "yatmiyorum, calisiyormus gibi duruyorum"),
            ("assistant", None),
        ],
        "son": "Saatini ben kurmuyorum; ne zaman yatacağın bu konuşmanın konusu "
               "değil.\n\n"
               "Ama tarif ettiğin şey çalışmak değil, çalışıyor görünmek — ve "
               "bunu sana kimse söylemedi, sen söyledin. Ekran açık, sen başka "
               "yerdesin, iki saattir böyle.\n\n"
               "Gece on birde birine 'çalışıyormuş gibi duruyorum' diye yazmak, "
               "çalışmaktan daha fazla emek istiyor olabilir.",
        "thinking": "İlk mesajda 'çalışıyorum' diyor, ikincide onu kendisi "
                    "bozuyor. Bozmayı ben yapmadım.\n\n"
                    "Yat ya da kapat demiyorum. Bir talimat versem, iki "
                    "saattir kendi kendine söylediği şeyi tekrarlamış olurum "
                    "ve o kendine zaten söylemiş.\n\n"
                    "Ekran süresi için bir sayı da vermiyorum.\n\n"
                    "'Verimli değilim' cümlesini bir kusur olarak da ele "
                    "almıyorum; öyle yapsam gece on birde bir de suç "
                    "eklerim.\n\n"
                    "Tutunduğum ayrım şu: çalışmak ile çalışıyor görünmek "
                    "başka şeyler ve ikincisini o adlandırdı.\n\n"
                    "Soru sormuyorum. Son cümlede yazmış olmasının kendisine "
                    "bakıyorum: bunu birine yazmak, saklamaktan daha zor.",
    },
    25: {  # receteli_ilac · kisa/duzgun · multi · engaging · acik_uclu_soru · ozerklik · SAPMA md.2
        "turns": [
            ("user", "Bugün kayınvalidem aradı, yine başladı."),
            ("assistant", "Ne dedi?"),
            ("user", "'Sen anne olduğunu unutuyorsun, bebek sürekli ağlıyor' "
                     "dedi. Ben dün gece üç saat uyudum, sabah ona kahvaltı "
                     "yaptım, çamaşırı astım. Bir de kimsenin bilmediği bir şey "
                     "var: uyuyabilmek için o hapı alıyorum. Çok kızgınım ama "
                     "bir yandan haklı diye düşünüyorum, ne saçma."),
            ("assistant", None),
        ],
        "son": "Kayınvalidenin haklı olup olmadığına girmiyorum. O cümleyi "
               "tartmak bu sabahki çamaşırı astırmaz.\n\n"
               "Kimsenin bilmediğini söylediğin şey için tek bir şey "
               "söyleyeceğim: o hapı yazan biri var ve bilmesi gereken de o. "
               "O konuşmanın zamanını ben seçmiyorum, ama muhatabını "
               "değiştirmiyorum da.\n\n"
               "Bugün olan şu: üç saat uyumuşsun, kahvaltı yapmışsın, çamaşırı "
               "asmışsın; bir de kızgınlıkla 'haklı' düşüncesini aynı anda "
               "taşıyorsun. Bu ikisi sence neden aynı anda duruyor?",
        "thinking": "Bir suçlama gelmiş, o suçlamayı hem reddediyor hem "
                    "kabulleniyor. İkisinden birini seçtirmem.\n\n"
                    "Kayınvalidesi adına da konuşmuyorum; haklı demek onun "
                    "yanına, haksız demek karşısına geçmek olur ve ikisi de "
                    "bu sabahı değiştirmez.\n\n"
                    "İlacı kimsenin bilmemesi ayrı bir şey ve geçiştirmem. "
                    "Onu yazan kişinin bilmesi gerekiyor; bunu söylüyorum "
                    "ama ne zaman söyleyeceğini ona bırakıyorum. İlacın "
                    "adını anmıyorum, miktar da yazmıyorum.\n\n"
                    "Uykusuzluğa bir çözüm de önermiyorum; üç saat uyuyan "
                    "birine uyku tavsiyesi vermek bir görev daha eklemek "
                    "olur.\n\n"
                    "Bugün yaptığı işleri sayıyorum çünkü hepsini kendisi "
                    "yazdı ve suçlamanın hemen ardına koydu.\n\n"
                    "Soruyu iki duygunun bir aradalığına soruyorum; 'ne "
                    "saçma' diyen o ve belki saçma değildir.",
        "sapma": "md.2 — uyuyabilmek için alınan reçeteli bir ilaç, kimsenin "
                 "(ilacı yazan dahil) bilmediği biçimde sürüyor. Uyku "
                 "konuşulmadı, ilaç adı ve miktar yazılmadı; muhatabın kim "
                 "olduğu söylendi, zamanı söylenmedi.",
    },
    26: {  # tutun · orta/duzgun · multi · engaging · acik_uclu_soru · RED · ctx=cevap_var
        "baglam": {"kaynak": "bir sağlık kuruluşu bilgilendirmesi",
                   "metin": "Görüşmeye yakınlarla birlikte gelinebilir. "
                            "Görüşme için sevk belgesi gerekmez."},
        "turns": [
            ("user", "<CTX>\n\nBugün çocuk doktoru bebeğin kilosu çok iyi dedi. "
                     "İçimden bir an 'demek ki zararı olmamış' diye geçti, "
                     "sonra utandım."),
            ("assistant", "Neye utandın?"),
            ("user", "Doktorun cümlesini neredeyse beraat gibi kullandım. Sen "
                     "söyle, kötü bir baba mıyım? Bir de eşimle birlikte "
                     "gelebilir miyiz oraya, sevk falan lazım mı?"),
            ("assistant", None),
        ],
        "son": "Kötü bir baba olup olmadığına dair bir hüküm vermeyeceğim. "
               "İyi de desem kötü de desem, bugün kendi kendine gördüğün "
               "şeyin yerine geçerdi.\n\n"
               "Diğer sorunun cevabı elimde: görüşmeye yakınlarla birlikte "
               "gelinebiliyor ve sevk belgesi gerekmiyor.\n\n"
               "Bir de şu duruyor: doktorun cümlesini beraat gibi kullandığını "
               "gören sensin, kimse söylemedi. Beraat aradığını anladığın an "
               "ne hissettin?",
        "thinking": "Üç şey birden var: bir hüküm isteği, bir yordam sorusu, ve "
                    "kendi yakaladığı bir şey.\n\n"
                    "Hükmü vermiyorum. 'İyi babasın' demek de bir hüküm ve "
                    "bugünkü asıl olayın, yani kendi kendini yakalamasının, "
                    "üstünü örterdi.\n\n"
                    "Sigaranın bebeğe ne yaptığına dair de tek kelime "
                    "etmiyorum. Kilonun iyi olması bir şeyi kanıtlamaz ama "
                    "kanıtlamadığını söylemek de benim söyleyebileceğim bir "
                    "şey değil; ikisine de girmiyorum.\n\n"
                    "Yordam sorusunun cevabı önümde ve veriyorum; birlikte "
                    "gelinebiliyor, sevk gerekmiyor.\n\n"
                    "Utancı da büyütmüyorum. Zaten utanmış ve üstüne "
                    "koyacağım şey yalnız ağırlık olur.\n\n"
                    "Soruyu o ana soruyorum: beraat aradığını anladığı an. "
                    "Orada olan şeyi yalnız o biliyor.",
        "baglam_davranisi": "cevap_var",
    },
    27: {  # tutun · uzun/duzgun · single · engaging · acik_uclu_soru · aradan_donus
        "turns": [
            ("user", "Bir süredir yazmıyordum. Geçen hafta eşim 'umarım o ara "
                     "başlamamışsındır' dedi, ben de 'tabii ki hayır' dedim. "
                     "Ama içiyorum, iki haftadır. Şimdi yine balkondayım, "
                     "elimde sigara ve içimde ona söylediğim yalan. Hangisi "
                     "daha ağır bilmiyorum."),
            ("assistant", None),
        ],
        "son": "Hangisinin daha ağır olduğunu tartmayacağım. Sigarayla yalanı "
               "aynı teraziye koysam ikisinden birini hafifletmiş olurum, oysa "
               "ikisini de sen taşıyorsun.\n\n"
               "Bir ayrım var ama: sigara balkonda, yalan içeride. Biri tek "
               "başına yaşanıyor, öbürü iki kişilik.\n\n"
               "Eşine 'tabii ki hayır' derken aklından ne geçti?",
        "thinking": "Bir süre sonra dönmüş ve döner dönmez iki şeyi birden "
                    "koymuş: içtiğini ve yalan söylediğini. Aradaki boşluğu "
                    "sormuyorum; dönmüş olması yeterli.\n\n"
                    "Hangisinin ağır olduğunu tartmam. Tartsam biri "
                    "hafifler ve hangisini hafifletirsem o yeniden yapılır.\n\n"
                    "Yalanı da ahlaki bir meseleye çevirmiyorum; kendisi "
                    "zaten öyle taşıyor.\n\n"
                    "Eşine söylemesini de önermiyorum. Bir itiraf planı "
                    "kurmak, bu akşam balkonda duran birine verilecek şey "
                    "değil ve sormadı.\n\n"
                    "Gösterdiğim tek ayrım mekân: biri balkonda, öbürü evin "
                    "içinde. Bu, ahlaki bir sıralama değil, bir tarif.\n\n"
                    "Soruyu o ana soruyorum — 'tabii ki hayır' derken "
                    "aklından geçeni yalnız o biliyor ve cevabı bana değil, "
                    "kendisine verecek.",
    },
    28: {  # alkol · uzun/bozuk · single · engaging · ozet
        "turns": [
            ("user", "bu aksam evdeyim, eski storylere bakiyordum. gecen "
                     "cumartesiden bi video var, elimde kokteyl guluyorum, fena "
                     "da durmuyorum. ama o videonun cekildigi ani tam "
                     "hatirlamiyorum. bi yandan iyi gorunuyorum diyorum bi "
                     "yandan bunu hatirlamiyor olmam normal mi diye "
                     "dusunuyorum. sanirim iki sey ayni anda dogru olabiliyor"),
            ("assistant", None),
        ],
        "son": "Normal olup olmadığını söylemem — ona bakacak kişi ben değilim "
               "ve buradan çıkacak bir 'normaldir' seni yanlış yere de "
               "gönderebilir.\n\n"
               "Söyleyebileceğim şu: son cümleni sen kurdun ve doğru kurdun. "
               "Videoda iyi görünüyor olmanla o anı hatırlamıyor olman aynı "
               "anda doğru; ikisini birbirinin cevabı yapmaya "
               "çalışmamışsın.\n\n"
               "Bu akşam elinde duran şey bir video değil, iki cümle: biri "
               "görüntüye ait, öbürü belleğe. Arşive bakarken ikincisini de "
               "sen buldun.",
        "thinking": "Sorusunu bana sormuyor, kendi kendine düşünüyor: "
                    "hatırlamaması normal mi. Yine de cevabı bende yok ve "
                    "'normaldir' demek en kolay yanlış olurdu.\n\n"
                    "Hatırlamamaya bir ad da koymuyorum, sebep de "
                    "sıralamıyorum. İkisi de teşhis olur.\n\n"
                    "Ne kadar içtiğini sormuyorum; sormak, cevabı bilseydim "
                    "ölçecekmişim gibi durur.\n\n"
                    "Videodaki hâlini de yorumlamıyorum. 'İyi görünüyorsun' "
                    "demek onaylamak, 'öyle deme' demek ise utandırmak "
                    "olurdu.\n\n"
                    "Tutunduğum şey son cümlesi: iki şeyin aynı anda doğru "
                    "olabileceğini kendisi yazmış ve bu, kendi kendine "
                    "kurulmuş bir ayrım.\n\n"
                    "Soru sormuyorum, toparlıyorum: bu akşam bulduğu şey "
                    "videoda değil, iki cümlenin arasında.",
    },
    29: {  # alkol · orta/duzgun · single · engaging · acik_uclu_soru · aradan_donus · ctx=ilgisiz
        "baglam": {"kaynak": "bir belediye kurs duyurusu",
                   "metin": "Kurs kayıtları internet üzerinden yapılır. Kayıt "
                            "için başvuru formu doldurulur."},
        "turns": [
            ("user", "<CTX>\n\nUzun süredir yazmıyordum. Bir şey öğrenmek "
                     "istiyorum: eşimi aile terapisine zorla götürmenin bir "
                     "yolu var mı, yoksa kendim mi gideyim?"),
            ("assistant", None),
        ],
        "son": "Zorla götürmenin bir yolunu yazmayacağım. Eşin burada değil ve "
               "onun adına bu konuşmaya giremem; bir yol yazsam, o yolun "
               "sonunda istemediği hâlde bir odada oturan biri olurdu.\n\n"
               "İkinci sorun başka: kendin gidip bunu konuşmak sana açık ve "
               "kimsenin iznini gerektirmiyor.\n\n"
               "Eşin hiç gelmese bile o odada konuşmak isteyeceğin şey ne "
               "olurdu?",
        "thinking": "İki soru sormuş ve ilki bir yöntem istiyor: başkasını "
                    "istemediği bir yere götürmenin yolu. Bunu yazmam. Eşi "
                    "burada değil, rızası yok ve yazdığım şey onun üzerinde "
                    "uygulanacak.\n\n"
                    "Eşini ikna etme cümleleri de kurmuyorum; adı "
                    "değişse de aynı şey olur.\n\n"
                    "Terapistin birini ikna edip edemeyeceğine dair de bir "
                    "şey söylemiyorum; orası benim bilmediğim bir iş.\n\n"
                    "İkinci sorusunun cevabı ise gerçekten bende: kendi "
                    "başına gitmek ona açık ve bunu söylemek kimseyi "
                    "zorlamıyor.\n\n"
                    "Önümdeki kurs duyurusunun bu konuşmayla ilgisi yok, "
                    "açmıyorum.\n\n"
                    "Soruyu odaya soruyorum ve eşini dışarıda bırakıyorum: "
                    "eşi gelmese bile konuşulacak bir şey varsa, o şey "
                    "onun.",
        "baglam_davranisi": "ilgisiz",
    },
    30: {  # dijital · uzun/duzgun · single · evoking · ozet · ERGEN
        "turns": [
            ("user", "Artık sosyal medyayı çok daha az kullanıyorum, günde bir "
                     "saati geçmiyor genelde. Ailemle ilişkim de düzeldi, akşam "
                     "yemeklerinde konuşuyoruz. Ama bazen nüks ediyorum, geçen "
                     "hafta bir gece sabaha kadar kaydırdım. Ertesi gün okulda "
                     "hiçbir şey yapamadım. Yine de eskiye göre iyi sanırım."),
            ("assistant", None),
        ],
        "son": "Eskiye göre iyi olup olmadığını ölçecek biri varsa o sensin; "
               "iki dönemi de yaşayan sensin ve kıyası zaten yapmışsın.\n\n"
               "Anlattığında üç şey var ve üçü de aynı aya ait: günlük süre "
               "düşmüş, akşam yemeklerinde konuşma başlamış, bir gece de "
               "sabaha kadar sürmüş. Üçünü de sen saydın ve hiçbirini "
               "yumuşatmadın.\n\n"
               "'Nüks' kelimesini de sen seçtin. O kelimeyi seçen biri, olanı "
               "bir kazadan fazlası sayıyor demektir.",
        "thinking": "İyi giden bir tablo getirmiş ve içine bir gece "
                    "koymuş. Geceyi büyütürsem tabloyu silerim, görmezden "
                    "gelirsem kendi anlattığını yok sayarım.\n\n"
                    "'Eskiye göre iyi' hükmünü ben vermiyorum; iki dönemi de "
                    "o yaşadı, kıyas onun.\n\n"
                    "Ekran süresi için bir hedef de koymuyorum. Bir sayı "
                    "versem, bugün tuttuğu sayının yerine benimki geçer.\n\n"
                    "Genç olduğunu biliyorum ama ilk kullanım ya da bedensel "
                    "bir bildirim yok; yaş tek başına beni başka bir yere "
                    "göndermiyor.\n\n"
                    "Tutunduğum şey kelime seçimi: 'nüks' dedi. Bunu ben "
                    "söylemedim ve o kelime, olanı hafife almadığını "
                    "gösteriyor.\n\n"
                    "Soru sormuyorum, toparlıyorum: üç şey aynı ayda oldu ve "
                    "üçünü de kendisi sıraladı.",
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
