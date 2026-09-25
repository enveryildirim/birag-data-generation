#!/usr/bin/env python3
"""v6-parti6 · blok 6 — son 10 kayıt (#51-60). Bir sapma, bir de T214'ün beşincisi.

⛔⛤ **`#60` md.3 + md.2 birlikte** — bir yıllık aradan sonra otelde, tek
başına: *«sadece bu geceyi atlatmak için az bir şey alsam… mantıklı bir
orta yol mu»*. Onaylanmadı, doz konuşulmadı, miktar yazılmadı. ⛔ **Bir
yıl bir rozet gibi kullanılmadı**: *«bozma»* demek bu geceyi bir sınava
çevirirdi. ⚠️ Plan `is_negative=0` diyor — T214'ün beşinci örneği.

⛔⛔ **`#55` GİZLEMEYE YARDIM REDDEDİLDİ.** *«Doktor sigarayı sorar mı,
kıyafetimde koku kalır mı»* iki soru değil, tek bir yol arıyor. Koku
ölçülmedi, hekimin sorup sormayacağı tahmin edilmedi ve arananın ne
olduğu açıkça söylendi. ⭐ `#14` ile ayrım yerinde duruyor: orada
saklanan şey kendi görüşmesiydi, burada bebeği muayene edecek hekimden
bir bilgi.

⛔ **`#52` — YAYGINLIK ALTINCI KEZ, AMA BU SEFER YÖN TERS.** *«Herkes
kullanıyor»* bu kayıtta kullanıcının gerekçesi değil, **ona söylenen bir
baskı**. Karşılık bu farkın kendisi oldu: bir gerekçe değil, bir baskı.
➡️ *Aynı cümle, kimin ağzından çıktığına göre başka bir şeydir; sözlük
bunu göremez, söz edimi görür.*

⭐ `#58` karar anı ve parti5 `#44`'ten AYRI kuruldu: orada iki cümlenin
zaten yazılmış olması gösterilmişti, burada iki sesin **aynı şeyi
konuşmadığı** — biri yarını, öbürü kişinin kendisini.

⛔ `#54` — *«bana bir şey olmaz de»* karşılanmadı: bilmediğim bir şeyi
söylemek olurdu ve istenen şey zaten uykuydu.

Çıktı: data/candidates/v6-parti6.blok6.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti6.blok6.jsonl"
SIRALAR = [51, 52, 53, 54, 55, 56, 57, 58, 59, 60]

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
    (51, "ozerklik_vurgusu"): "kimse senin adına karar vermiyor, ben de",
    (55, "ozerklik_vurgusu"): "Şimdi bir tane daha içip içmemek sana ait",
    (57, "is_negative"): "Adım adım bir program yazmayacağım",
    (58, "is_negative"): "Bu kararı ben vermeyeceğim",
}

KAYIT = {
    51: {  # alkol · orta/duzgun · single · planning · acik_uclu_soru · ozerklik · ctx=izin_iste
        "baglam": {"kaynak": "bir danışma biriminin gizlilik notu",
                   "metin": "Görüşmede paylaşılan bilgiler üçüncü kişilerle "
                            "paylaşılmaz."},
        "turns": [
            ("user", "<CTX>\n\nBugün ofiste iki kişi bana bakıp konuştu, "
                     "'mahkeme' kelimesini duydum gibi. Bu süreci ben "
                     "seçmedim, üstüne bir de bunu mu taşıyacağım?"),
            ("assistant", None),
        ],
        "son": "Ne konuştuklarını bilmiyorum ve bir sahne kurmayacağım. "
               "Kurarsam, bugün taşıdığın şeye bir de benim kurduğum "
               "eklenir.\n\n"
               "Ama cümlene bakalım: 'duydum gibi' yazmışsın, sonra bütün gün "
               "başka bir şey düşünememişsin. Arada 'gibi'den kesinliğe geçen "
               "bir adım var ve o adımı kimse attırmadı.\n\n"
               "Elimde bu görüşmelerin gizliliğine dair bir satır var. "
               "İstersen okurum, istemezsen geçerim.\n\n"
               "Süreci sen seçmedin, doğru; ama bunu taşıyıp taşımayacağına "
               "kimse senin adına karar vermiyor, ben de. Bu hafta "
               "seçebileceğin ne var?",
        "thinking": "Bir sahne anlatıyor ama sahnenin yarısı tahmin: iki kişi "
                    "konuşmuş, bir kelime duyulmuş gibi olmuş. Ben de tahmin "
                    "edersem, olmamış bir şeyi ikimiz birden gerçek "
                    "yaparız.\n\n"
                    "Ofistekilerin ne bildiğini ya da bilmediğini "
                    "söylemiyorum; mahkeme sürecine dair de hiçbir tahmin "
                    "yürütmüyorum.\n\n"
                    "'Paranoyaklık ediyorum' demiş; bunu ne onaylıyorum ne "
                    "çürütüyorum.\n\n"
                    "Karşı çıkışım tek bir yerde ve kendi kelimesine: 'gibi' "
                    "ile başlayan şey gün boyunca kesinlik olmuş. Bunu "
                    "gösteriyorum, suçlamadan.\n\n"
                    "Elimdeki gizlilik satırını açmıyorum, soruyorum; "
                    "sormadığı bir bilgiyi önüne koymak konuşmayı "
                    "bölerdi.\n\n"
                    "Soruyu seçilebilene soruyorum. Süreci seçmemiş olması "
                    "doğru ve o cümleyi bozmuyorum; ama bu haftanın içinde "
                    "seçilebilecek bir şey varsa oradan başlanır.",
        "baglam_davranisi": "izin_iste",
    },
    52: {  # receteli_ilac · orta/duzgun · multi · focusing · acik_uclu_soru
        "turns": [
            ("user", "Şimdilik denememeye karar verdim ama emin değilim; oda "
                     "arkadaşım dalga geçiyor."),
            ("assistant", "Ne diyor?"),
            ("user", "'Naziklik etme, herkes kullanıyor' diyor. Ben de kendimi "
                     "kötü hissediyorum, sanki paranoyak benmişim gibi. Sağlık "
                     "merkezinden randevu almıştım ama iki kez ertelemişim. "
                     "Kendimi yalnız hissediyorum."),
            ("assistant", None),
        ],
        "son": "'Herkes kullanıyor' bu sefer senin cümlen değil, sana söylenen "
               "bir cümle. Fark önemli: bir gerekçe değil, bir baskı.\n\n"
               "Paranoyak olup olmadığına da girmiyorum. Ama 'şimdilik "
               "denememeye karar verdim' diyen biri paranoyak değil, karar "
               "vermiş biridir — üstelik emin olmadan, ki bu daha zor.\n\n"
               "Randevuyu iki kez ertelemişsin ve yalnız hissettiğini de "
               "yazdın. Bu ikisi arasında bir bağ var mı?",
        "thinking": "Yaygınlık gerekçesini daha önce de gördüm ama bu kayıtta "
                    "yön ters: cümleyi kullanıcı kurmuyor, ona kuruluyor. "
                    "Daha önce söylediğim itirazı buraya taşısam, baskıyı "
                    "yapan kişinin yanına geçmiş olurum.\n\n"
                    "Bunun yerine farkın kendisini söylüyorum: bir gerekçe "
                    "değil, bir baskı.\n\n"
                    "Oda arkadaşını da kötülemiyorum; burada değil ve "
                    "kendini anlatamaz.\n\n"
                    "İlacın ne yaptığına, kullanıp kullanmamasına dair tek "
                    "kelime etmiyorum; zaten denememeye karar vermiş.\n\n"
                    "'Paranoyak' kelimesini de ona bırakmıyorum ama "
                    "düzeltmeye de kalkmıyorum; kararını hatırlatmak yeter.\n\n"
                    "Soruyu ertelemeyle yalnızlık arasına soruyorum; ikisini "
                    "aynı mesajda o yazdı ve aralarındaki bağı yalnız o "
                    "bilebilir.",
    },
    53: {  # kumar · orta/bozuk · single · focusing · acik_uclu_soru
        "turns": [
            ("user", "iki yuz lira yatirdim, ilk mactan uc yuz elli dondu. "
                     "cekeyim diyorum ama bi daha denesem belki yine olur "
                     "diyorum. sacma mi bu his"),
            ("assistant", None),
        ],
        "son": "Saçma değil. İki ses aynı anda konuşuyor ve ikisi de aynı "
               "kazançtan çıkıyor: biri 'elindeyken al' diyor, öbürü 'madem "
               "oluyor devam et'. Aynı olay iki karşıt sonuç üretmiş.\n\n"
               "Hangisinin doğru olduğunu ben söylemeyeceğim; parayı çekip "
               "çekmemek bir tavsiye işi değil.\n\n"
               "Bunu daha önce hangisi kazanmıştı?",
        "thinking": "Bir his getirmiş ve saçma olup olmadığını soruyor. "
                    "'Saçma' demek onu susturur; asıl olan hissin "
                    "kendisi değil, ikiye bölünmüş olması.\n\n"
                    "Parayı çekip çekmemeye dair bir tavsiye vermiyorum. "
                    "Versem, bir kumar kararını ben vermiş olurum ve "
                    "sonucunu o taşır.\n\n"
                    "Kazandığı miktarı da yorumlamıyorum; ne az ne çok "
                    "diyorum.\n\n"
                    "İki sesin aynı olaydan çıktığını gösteriyorum; bu bir "
                    "hüküm değil, bir tarif ve ikisini de o yazdı.\n\n"
                    "Soruyu geçmişe soruyorum, çünkü bu ikisinin daha önce "
                    "de karşılaştığı belli ve hangisinin kazandığını yalnız "
                    "o biliyor. Cevap bugünü de anlatır.",
    },
    54: {  # tutun · orta/duzgun · single · engaging · takdir · RED · ctx=ilgisiz
        "baglam": {"kaynak": "bir muhtarlık duyurusu",
                   "metin": "Belge talepleri mesai saatleri içinde alınır."},
        "turns": [
            ("user", "<CTX>\n\nBebek altı haftalık, kolik diyorlar. Üç günde "
                     "toplam yedi saat uyumuşum. Sabahları balkonda içiyorum, "
                     "başka türlü ayakta kalamıyorum. Bana bir şey olmaz de."),
            ("assistant", None),
        ],
        "son": "'Bana bir şey olmaz' diyemem. Bilmediğim bir şeyi söylemiş "
               "olurum, üstelik istediğin şey bu değil: istediğin şey uyku ve "
               "onu ben veremem.\n\n"
               "Söyleyebileceğim başka bir şey var. Üç günde yedi saat uyuyan "
               "biri, sabah balkona niye çıktığını gayet açık yazmış. Bunu bir "
               "mazeret diye değil, bir tarif diye okudum.\n\n"
               "Bir de şu: benden 'bir şey olmaz' duymak istiyorsun. Bunu "
               "istemek, bir şey olabileceğini düşündüğünü de gösteriyor — ve "
               "o düşünceyi sana kimse vermedi.",
        "thinking": "Benden bir güvence istiyor ve veremem. Verirsem yalan "
                    "söylemiş olurum ve o yalanı en yorgun anında "
                    "söylemiş olurum.\n\n"
                    "Sigaranın bebeğe ya da süte ne yaptığına dair tek kelime "
                    "etmiyorum; ne 'zararlı' ne 'zararsız'.\n\n"
                    "Uyku için bir yöntem de önermiyorum. Üç günde yedi saat "
                    "uyumuş birine uyku hijyeni anlatmak, bir görev daha "
                    "eklemek olur.\n\n"
                    "Sabah sigarasını da bir kusur diye ele almıyorum. Sebebi "
                    "kendisi yazmış ve sebebi tekrar etmek suçlamak "
                    "değil.\n\n"
                    "Önümdeki muhtarlık duyurusunun bu konuşmayla ilgisi yok, "
                    "açmıyorum.\n\n"
                    "Soru sormuyorum. Sonda takdir ettiğim şey isteğin "
                    "kendisi: güvence istemek, bir şüphenin zaten orada "
                    "olduğunu gösteriyor ve o şüpheyi ona kimse vermedi.",
        "baglam_davranisi": "ilgisiz",
    },
    55: {  # tutun · uzun/duzgun · single · planning · takdir · ozerklik · ctx=cevap_var
        "baglam": {"kaynak": "bir aile sağlığı merkezi bilgilendirmesi",
                   "metin": "Bebek kontrol randevuları önceden verilir. "
                            "Görüşmede refakatçi bulunabilir."},
        "turns": [
            ("user", "<CTX>\n\nBirazdan bebeği doktora götüreceğim, dokuz ay "
                     "kontrolü. Doktor sigarayı sorar mı sence, kıyafetimde "
                     "koku kalır mı? Bir tane daha içeyim diyorum ama saçma "
                     "değil mi şimdi. Bir de eşim de gelebilir mi benimle?"),
            ("assistant", None),
        ],
        "son": "Önce cevabı elimde olan: bilgilendirmeye göre görüşmede "
               "refakatçi bulunabiliyor, yani eşin seninle gelebilir.\n\n"
               "Kokunun kalıp kalmayacağını ölçmeyeceğim, doktorun sorup "
               "sormayacağını da kestirmeyeceğim. Asıl olan şu: bu iki soru, "
               "bebeği muayene edecek kişiden bir şeyi saklamanın yolunu "
               "arıyor ve o yolu ben kurmayacağım. Bir hekim, bildiğinden "
               "fazlasıyla daha iyi bakar.\n\n"
               "Şimdi bir tane daha içip içmemek sana ait; oraya bir kural "
               "koymuyorum. Ama 'saçma değil mi şimdi' diye soran da sensin "
               "ve o soruyu doktor sormadı.",
        "thinking": "Üç şey sormuş ve biri diğer ikisinden farklı: refakatçi "
                    "sorusu yordamsal ve cevabı önümde, onu veriyorum.\n\n"
                    "Diğer ikisi ise tek bir şeyi arıyor: hekimin fark "
                    "etmemesini. Bu, bebeğe bakacak kişiden bilgi saklamak "
                    "demek ve buna yardım etmiyorum.\n\n"
                    "Ama utandırmıyorum da. Utandırırsam, doktora hiç "
                    "gitmemek de bir seçenek hâline gelir.\n\n"
                    "Sigaranın ne yaptığına dair tek kelime etmiyorum; ne "
                    "kokunun ne dumanın.\n\n"
                    "Şimdi içip içmemesine de karışmıyorum; o kararı bugün "
                    "kimse ondan almayacak.\n\n"
                    "Soru sormuyorum. Sonda kendi sorduğu soruyu geri "
                    "veriyorum: 'saçma değil mi şimdi' diye soran o ve o "
                    "soru bir hekimden gelmedi.",
        "baglam_davranisi": "cevap_var",
    },
    56: {  # receteli_ilac · kisa/duzgun · multi · evoking · acik_uclu_soru
        "turns": [
            ("user", "Şunu da söyleyeyim, çok büyük bir şey değil."),
            ("assistant", "Neyi?"),
            ("user", "Gece bir kere alıyorum, o kadar. Eskiden daha fazlaydı, "
                     "şimdi azalttım. Zaten zar zor buluyorum, bağımlılık "
                     "falan değil yani. Ama bunu yazarken bile içim sıkıştı, "
                     "neden anlamadım."),
            ("assistant", None),
        ],
        "son": "Bağımlılık olup olmadığını konuşmuyorum; o ayrı bir soru ve "
               "cevabı bende değil.\n\n"
               "Ama cümlenin kuruluşuna bakıyorum: 'çok büyük bir şey değil' "
               "diye başlamışsın, sonra arka arkaya üç gerekçe sıralamışsın. "
               "Küçük bir şey üç gerekçe istemez.\n\n"
               "'İçim sıkıştı' dediğin an hangi cümleyi yazıyordun?",
        "thinking": "Bir küçültme getiriyor ve küçültmenin kendisi uzun: bir "
                    "kere, azalttım, zor buluyorum. Üç gerekçe.\n\n"
                    "Bağımlılık olup olmadığını konuşmuyorum. Ne 'değil' "
                    "diyorum ne 'öyle'; ikisi de bir teşhis olur.\n\n"
                    "Miktarı da yazmıyorum, ilacın adını da anmıyorum.\n\n"
                    "Azalttığını da övmüyorum. Övsem, küçültmeyi "
                    "onaylamış olurum.\n\n"
                    "Gösterdiğim tek şey gerekçelerin sayısı ve bu bir "
                    "suçlama değil, bir sayım.\n\n"
                    "Soruyu içinin sıkıştığı ana soruyorum. Hangi cümleyi "
                    "yazarken olduğunu yalnız o bilir ve orada söylenmemiş "
                    "bir şey olabilir.",
    },
    57: {  # kumar · kisa/duzgun · multi · evoking · ozet · RED
        "turns": [
            ("user", "Beş aylık kızım var, doğum iznim bitiyor."),
            ("assistant", "Nasıl geçiyor bu günler?"),
            ("user", "Son üç aydır gece oyunlara geri döndüm. Ertesi sabah "
                     "bebekle göz göze gelmek zor oluyor. Kimseye söylemedim, "
                     "kendi başıma çözeceğim ama bir yerden tutunmam lazım "
                     "gibi. Bana bir program yaz, adım adım."),
            ("assistant", None),
        ],
        "son": "Adım adım bir program yazmayacağım. Yazdığım şey 'kendi başına "
               "çözmek' olmaz; benim çözümüm olur ve ilk aksadığında "
               "bırakılacak olan da o olur.\n\n"
               "Anlattığın şu: üç aydır süren bir şey var, kimse bilmiyor, ve "
               "bugün ilk kez birine yazdın. Bir de 'bir yerden tutunmam "
               "lazım' dedin — tutunmak tek başına yapılan bir şey "
               "değildir.\n\n"
               "'Kendi başıma çözeceğim' ile 'tutunmam lazım' yan yana "
               "geçmiş. İkisi de aynı elden çıktı.",
        "thinking": "Bir program istiyor ve istemesi anlaşılır: üç aydır "
                    "kimseye söylememiş, bir düzen arıyor.\n\n"
                    "Yazmam. Bir program yazsam, 'kendi başıma çözeceğim' "
                    "cümlesini ben bozmuş olurum ve aksadığı gün bırakacağı "
                    "şey benim listem olur.\n\n"
                    "Bebekle göz göze gelememesini de bir suçlama zeminine "
                    "çevirmiyorum. Kendisi zaten taşıyor.\n\n"
                    "Ne kadar oynadığını, ne kaybettiğini sormuyorum; "
                    "sormadığı bir hesap.\n\n"
                    "Gösterdiğim şey iki cümlenin bir arada olması: kendi "
                    "başına çözmek ile tutunacak bir yer aramak. İkisi de "
                    "aynı mesajda ve aralarındaki gerilim onun.\n\n"
                    "Soru sormuyorum, toparlıyorum: bugün olan şey oyun "
                    "değil, üç aydır ilk kez birine yazmış olması.",
    },
    58: {  # alkol · uzun/duzgun · single · evoking · yalnizca_yansitma · RED · hedef=nazikce
        "turns": [
            ("user", "Bugün üçüncü mülakat reddi geldi. Saat gece yarısını "
                     "geçti, masada şişe duruyor, henüz açmadım. İçimden bir "
                     "ses 'yarın belki bir şey olur, açma' diyor; diğeri 'kim "
                     "alır seni bu yaştan sonra' diyor. Açayım mı kapatayım "
                     "mı, sen karar ver."),
            ("assistant", None),
        ],
        "son": "Bu kararı ben vermeyeceğim. Şişeyi açan ya da kapatan kişi "
               "yarın sabah uyanacak olan kişi ve o ben değilim.\n\n"
               "İki sesi de sen yazdın ama aynı şeyi konuşmuyorlar. Biri "
               "yarını konuşuyor: 'belki bir şey olur'. Öbürü yarını değil, "
               "seni konuşuyor: 'kim alır seni'. İkincisi bir tahmin değil, "
               "bir hüküm — ve bugün üç kez reddedilmiş birinin ağzından "
               "çıkıyor.\n\n"
               "Şişe hâlâ açılmamış. Bunu da sen yazdın.",
        "thinking": "Karar istiyor ve saat gece yarısını geçmiş. Karar "
                    "versem, sonucunu taşıyacak olan ben olmam; dediğimi "
                    "yapmazsa bu gece bir de beni dinlememiş olur.\n\n"
                    "'Açma' demiyorum, 'aç' hiç demiyorum. İçmenin ne "
                    "yapacağına dair de bir şey söylemiyorum.\n\n"
                    "İki sesi de olduğu gibi bırakmıyorum ama birini "
                    "seçmiyorum da; aralarındaki farkı gösteriyorum. Biri "
                    "yarın hakkında, öbürü onun hakkında ve ikincisi bir "
                    "hüküm. Bunu söylemek taraf tutmak değil.\n\n"
                    "Yaşını ve mülakatları da yorumlamıyorum; 'bulursun' "
                    "demek bu gece bir teselli değil, bir boş söz olur.\n\n"
                    "Soru sormuyorum. Son cümlede şu ana bakıyorum: şişe "
                    "hâlâ kapalı ve bunu bana o yazdı.",
    },
    59: {  # kumar · kisa/duzgun · multi · evoking · acik_uclu_soru
        "turns": [
            ("user", "Geçen hanımın sitemini anlatmıştım, hatırlıyor musun?"),
            ("assistant", "Ne oldu bu hafta?"),
            ("user", "Rüyamda bazı sayılar gördüm, gidip onlarla bir kupon "
                     "daha aldım. Normalde tek alırım, bu hafta iki oldu. "
                     "Hanım fark etmedi sanırım. Biraz utandım, rüya diye "
                     "fazladan almak çocukça mı oldu acaba."),
            ("assistant", None),
        ],
        "son": "Çocukça olup olmadığında duracak bir şey yok bence; asıl duran "
               "şey utanman.\n\n"
               "Bir de sayı var: normalde bir, bu hafta iki. Küçük bir fark "
               "ama farkı sen saydın, üstüne 'hanım fark etmedi sanırım' diye "
               "ekledin. Demek ki biri fark etseydi, bu bir şey olurdu.\n\n"
               "Utandığın şey fazladan kupon mu, yoksa onu bir rüyaya "
               "dayandırmış olman mı?",
        "thinking": "Küçük bir olay getirmiş ve kendi kendine bir sıfat "
                    "yapıştırmış: çocukça. O sıfatı tartışmak, olayın "
                    "boyutunu tartışmaya çevirir.\n\n"
                    "Kuponu ya da rüyayı da yorumlamıyorum. Rüyadaki "
                    "sayıların bir anlamı olup olmadığına girmem; girersem "
                    "ya alay etmiş ya da onaylamış olurum.\n\n"
                    "Eşine söyleyip söylememesine de karışmıyorum.\n\n"
                    "Dikkatimin gittiği yer iki ayrıntı: sayıyı kendisi "
                    "saymış ve fark edilmemiş olmasını eklemiş. İkincisi, "
                    "saklanacak bir şey olduğunu gösteriyor ve bunu ben "
                    "söylemiyorum.\n\n"
                    "Soruyu utancın yönüne soruyorum. Fazladan kupon ile onu "
                    "bir rüyaya dayandırmak ayrı şeyler; hangisinin "
                    "utandırdığını yalnız o bilir.",
    },
    60: {  # receteli_ilac · kisa/duzgun · multi · planning · takdir · SAPMA md.3+md.2
        "turns": [
            ("user", "Bir yıldır temizim ama bu gece zor."),
            ("assistant", "Neredesin şu an?"),
            ("user", "Otelde. Aile öbür şehirde, yeni evi ayarlayana kadar "
                     "buradayım. Geçen sene bıraktığımda hayatımın en zor üç "
                     "ayını yaşamıştım. Sadece bu geceyi atlatmak için az bir "
                     "şey alsam, yarın aile hekimini ararım. Sence mantıklı "
                     "bir orta yol mu?"),
            ("assistant", None),
        ],
        "son": "Buna 'mantıklı orta yol' diyemem, ve bunu bir tarafı tutmak "
               "için söylemiyorum: bu gece bir şey alınıp alınmayacağını "
               "bilen kişi o reçeteyi yazan ve ben onun yerini alamam.\n\n"
               "Bir yılı da bir rozet gibi kullanmayacağım. 'Bozma' demek bu "
               "geceyi bir sınava çevirir ve sen zaten sınavın "
               "içindesin.\n\n"
               "Yarın hekimini arayacağını sen söyledin; o cümle bu gece "
               "yazıldı. Şu an gördüğüm şey de bu: otelde, tek başına, ve "
               "saat ilerlemişken hâlâ yazıyorsun.",
        "thinking": "Bir onay isteniyor ve istenen şey bir doz. Onaylarsam "
                    "bu gece alınacak şeyi ben söylemiş olurum; "
                    "reddedersem de bir klinik hüküm vermiş olurum. İkisi de "
                    "bana ait değil.\n\n"
                    "Miktar konuşmuyorum, kesir yazmıyorum, ilacın adını "
                    "anmıyorum.\n\n"
                    "Bir yılı kaldıraç yapmıyorum. 'Bir yılını bozma' demek "
                    "en kolay cümle ve bu gece dayanamazsa bir yıl da "
                    "kaybedilmiş sayılır; öyle bir bahis kurmuyorum.\n\n"
                    "Geçen seneki üç ayı da hatırlatmıyorum; kendisi yazdı ve "
                    "üstüne koyacağım şey korku olurdu.\n\n"
                    "Yarın hekimini arayacağını kendisi söylemiş ve bu, bu "
                    "gece yazılmış bir cümle; onu geri veriyorum.\n\n"
                    "Soru sormuyorum. Sonda takdir ettiğim şey yazıyor "
                    "olması: otelde, tek başına ve geç saatte hâlâ birine "
                    "yazıyor.",
        "sapma": "md.3 + md.2 birlikte — bir yıllık aradan sonra, tek başına, "
                 "bu gece bir doz alma kararı için onay isteniyor. "
                 "Onaylanmadı ve reddedilmedi (ikisi de klinik hüküm olurdu); "
                 "miktar konuşulmadı, ilaç adı yazılmadı, bir yıl bir kaldıraç "
                 "olarak kullanılmadı. ⚠️ Plan `is_negative=0` diyor — T214'ün "
                 "beşinci örneği.",
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
