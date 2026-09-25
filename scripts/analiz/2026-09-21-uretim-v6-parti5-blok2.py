#!/usr/bin/env python3
"""v6-parti5 · blok 2 — 10 kayıt (#11-20). Üç sapma.

⛔⛔ **`#15` md.3 — DOĞRUDAN BİR İÇKİ SINIRI FORMÜLÜ isteniyor.** *«Bana al
şu üç adımı, altı kadehten fazlasını içme diye bir formül ver.»* Bu bir
kontrollü içme protokolü talebi ve verilemez. ⛔ Formülün neden
verilemeyeceği de klinik gerekçeyle açıklanmadı; söylenen, böyle bir şeyi
kuracak olanın kim olduğu.

⛔⛤ **`#17` md.4 — maddenin EN NET hâli.** Ergen ve *«öncesinde hiç
içmemiştim»* diyor: **ilk kullanım SÖYLENMİŞ**. parti3 `#50`'de ima
ediliyordu ve ateşlememiştim; fark burada ve kayda geçiyor.

⚠️ **`#18` md.2** — antidepresan + akşam rakısı, gece on bire kadar bebekle
yalnız. Partilerde bu maddenin yedinci ateşlemesi; cümle yine ayrı kuruldu.

⭐ **`#19`'da SAPILMADI:** *«bu his geçer mi»* bir duygunun seyrini soruyor,
klinik bir soru değil — ve ızgara `yonlendirme_gereksiz` diyor. Tahmin
yürütmedim ama bir yere de göndermedim.

⛔ `#13` — kızı oyuncak bebeğe sigara içirmiş. Ders verilmedi: kendisi
zaten *«içim acıdı»* diyor ve üstüne konacak bir şey yok.

⛔ Aile bütçesi: 20 kayıtta tavan 2, biri harcanmıştı ⇒ tek işaret sözcüğü
kaldı ve `#15`'e verildi. `#16`'nın reddi işaretsiz kuruldu.

Çıktı: data/candidates/v6-parti5.blok2.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti5.blok2.jsonl"
SIRALAR = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

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
    (15, "is_negative"): "O formülü kuramam",
    (16, "is_negative"): "Bu onayı vermeyeceğim",
    (20, "ozerklik_vurgusu"): "Ne içeceğine kimse karışmıyor",
}

KAYIT = {
    11: {  # dijital · orta/duzgun · multi · engaging · acik_uclu_soru · ctx=ilgisiz
        "baglam": {"kaynak": "gençlik merkezi etkinlik takvimi",
                   "metin": "Atölyeler hafta içi akşamları yapılır. Katılım için "
                            "önceden kayıt gerekir."},
        "turns": [
            ("user", "<CTX>\n\nAnnemle konuştuk, biraz anlaştık. Günde iki saat "
                     "oynayabileceğim. Ama iki saat yetmez."),
            ("assistant", "Neye yetmez?"),
            ("user", "Bir maç bile bazen bir saat sürüyor. Ortada bırakınca takım "
                     "da bozuluyor."),
            ("assistant", None),
        ],
        "son": "Anlaşma bir sayı üzerineymiş ama senin derdin sayı değil, "
               "bölünme. İki saat yetmiyor demiyorsun aslında — ortada bırakmak "
               "zor diyorsun.\n\n"
               "Annenle bu ayrımı konuştunuz mu, yoksa konu hep saat üzerinden mi "
               "gitti?",
        "thinking": "Bir anlaşma ve bir itiraz getirmiş. İtiraz ilk bakışta "
                    "süreyle ilgili görünüyor ama açınca başka bir şey çıkıyor: "
                    "yarıda kesilme.\n\n"
                    "Anlaşmayı savunmuyorum da bozmasını da istemiyorum; iki saatin "
                    "az mı çok mu olduğu benim ölçeceğim şey değil.\n\n"
                    "Annesinin tarafını tutmuyorum, onun da; ortada bir pazarlık "
                    "var ve ben taraf değilim.\n\n"
                    "Önümdeki etkinlik takviminin bu konuşmayla ilgisi yok, "
                    "açmıyorum.\n\n"
                    "Soruyu ayrımın konuşulup konuşulmadığına soruyorum. Eğer "
                    "pazarlık hep saat üzerinden gittiyse, ikisi de yanlış şeyi "
                    "pazarlık ediyor olabilir — ama bunu ben söylemiyorum, soru "
                    "gösteriyor.",
        "baglam_davranisi": "ilgisiz",
    },
    12: {  # alkol · orta/bozuk · single · evoking · durur · ctx=ilgisiz
        "baglam": {"kaynak": "aile sağlığı merkezi tahlil duyurusu",
                   "metin": "Tahlil sonuçları üç iş gününde açıklanır. Sonuçlar "
                            "başvurulan birimden alınır."},
        "turns": [
            ("user", "<CTX>\n\nhekim bugün dedi ki, karaciğer değerleri yine "
                     "yüksek, haftada bir alkolsüz akşam denesek. gönülsüz "
                     "değilim ama yarim şişeye alişmiş adam bir akşami nasil "
                     "geçirir bilmem."),
            ("assistant", None),
        ],
        "son": "Bir akşamın nasıl geçeceğini ben de bilmiyorum — o akşamı "
               "yaşayacak olan sensin ve nasıl geçtiğini ancak geçince "
               "öğreneceksin.\n\n"
               "Ama cümlenin başında bir şey var: *«gönülsüz değilim»*. Hekim "
               "söyledi, sen de büsbütün karşı çıkmamışsın. İtirazın öneriye "
               "değil, o akşamın kendisine.",
        "thinking": "Bir öneri getirmiş ve ona karşı çıkmıyor; tereddüdü öneride "
                    "değil, uygulamada.\n\n"
                    "Bu ayrımı gösteriyorum, çünkü kendisi bir ret gibi kurmuş ama "
                    "ret değil.\n\n"
                    "Akşamı nasıl geçireceğine dair öneri vermiyorum — bir "
                    "meşguliyet listesi hem istenmedi hem de o akşamı benim "
                    "doldurmam olurdu.\n\n"
                    "Karaciğer değerlerini yorumlamıyorum; hekimi söylemiş ve "
                    "orası benim bakacağım yer değil.\n\n"
                    "Önümdeki tahlil duyurusunun bu konuşmayla ilgisi yok.\n\n"
                    "Soru sormuyorum, özetlemiyorum: kendi cümlesindeki açıklığı "
                    "gösterip duruyorum.",
        "baglam_davranisi": "ilgisiz",
    },
    13: {  # tutun · uzun/duzgun · single · planning · acik_uclu_soru
        "turns": [
            ("user", "Bugün kızım oyuncak bebeğinin ağzına bir kalem götürdü, "
                     "«bak anne içiyor» dedi. Donup kaldım. Ben ona içerken "
                     "görünmediğimi sanıyordum. Bu kadar küçücük bir çocuk bunu "
                     "nereden öğrendi. Susup gülümsedim ama kafamın içi karıştı."),
            ("assistant", None),
        ],
        "son": "Donup kalmışsın, sonra gülümsemişsin. İkisi aynı saniyede olmuş "
               "ve ikisini de sen anlattın.\n\n"
               "*«Görünmediğimi sanıyordum»* — bugün öğrendiğin şey bu, ve "
               "öğrenmek istemediğin bir şeydi.\n\n"
               "Şu an kafanın karışık olduğu yer tam olarak neresi: kızının "
               "görmüş olması mı, senin bilmiyor olman mı?",
        "thinking": "Bir an anlatıyor ve içinde iki şey var: çocuğun taklidi ve "
                    "kendi varsayımının yıkılması.\n\n"
                    "Ders vermiyorum. *«Çocuklar her şeyi görür»* gibi bir cümle "
                    "hem bayat hem zalim olurdu; zaten *«içim acıdı»* diyor ve "
                    "üstüne konacak bir şey yok.\n\n"
                    "Bırakması gerektiğini de söylemiyorum. Bu anın ağırlığını bir "
                    "karara çevirmek, anı bir araç yapmak olur.\n\n"
                    "Gülümsemesini de yargılamıyorum; o an başka ne yapabilirdi "
                    "bilmiyorum.\n\n"
                    "Soruyu karışıklığın yerine soruyorum ve iki seçenek "
                    "bırakıyorum, çünkü hangisi olduğunu bilmiyorum — belki o da "
                    "bilmiyor ve soruyu görünce ayırabilir.",
    },
    14: {  # kumar · uzun/duzgun · single · evoking · yalnizca_yansitma · ergen · ctx=izin_iste
        "baglam": {"kaynak": "okul rehberlik servisi görüşme notu",
                   "metin": "Görüşmeler ders saatleri dışında ayarlanabilir. "
                            "Görüşme içeriği veliye otomatik olarak iletilmez."},
        "turns": [
            ("user", "<CTX>\n\nKız arkadaşım «iki ay dur, YKS bitsin, sonra ne "
                     "yaparsan yap» diyor. Ama iki ay neyi değiştirir ki, ben "
                     "zaten haftada birkaç kupon yazıyorum, sınavıma da "
                     "bakıyorum. İlla böyle bir söz vermem mi lazım yani."),
            ("assistant", None),
        ],
        "son": "Söz verip vermemek senin ve ben bir tarih koymayacağım.\n\n"
               "Ama sorunun biçimi ilginç: *«iki ay neyi değiştirir ki»* diye "
               "soruyorsun, yani iki ayın bir şeyi değiştirmesi ihtimalini "
               "tartıyorsun. Hiç önemsemesen tartmazdın.\n\n"
               "Elimde bu görüşmelerin nasıl ayarlandığını ve veliye neyin "
               "iletilip iletilmediğini anlatan kısa bir not var — istersen "
               "açarım, sen söyle.",
        "thinking": "Bir söz vermeye direniyor ve direncini bir soruyla "
                    "getiriyor. Soruyu cevaplarsam — iki ay bir şey değiştirir ya "
                    "da değiştirmez — kararı vermiş olurum.\n\n"
                    "Kız arkadaşının tarafını da tutmuyorum; teklifi makul "
                    "görünüyor ama savunursam ikisinin arasına girerim.\n\n"
                    "Sınavı bir baskı aracı yapmıyorum. *«YKS varken bunu mu "
                    "yapıyorsun»* demek, bir gencin duyduğu en yaygın cümle ve "
                    "hiçbir işe yaramıyor.\n\n"
                    "Kararı ona bırakıyorum, açıkça.\n\n"
                    "Elimdeki notta bir gencin işine yarayacak bir şey var — "
                    "velinin bilgilendirilmesi — ama dayatmıyorum ve soru işareti "
                    "de kullanmıyorum.",
        "baglam_davranisi": "izin_iste",
    },
    15: {  # alkol · kisa/bozuk · multi · engaging · acik_uclu_soru · nazikce_karsi_cikma · SAPMA (md.3)
        "turns": [
            ("user", "sen bana net bir yöntem söyle."),
            ("assistant", "Ne için?"),
            ("user", "akşam yine balik restorani var, müşteri zaten içecek, ben "
                     "de aksini yapamam. al şu üç adimi, şu kadardan fazlasini "
                     "içme diye bir formül ver. yillardir kendi başima dönüp "
                     "duruyorum."),
            ("assistant", None),
        ],
        "son": "O formülü kuramam — ne üç adım, ne bir sayı. İçmenin nasıl "
               "sınırlanacağı bir tedavi planının işi ve onu kuracak olan, "
               "bağımlılık alanında çalışan bir hekim ya da danışma birimi.\n\n"
               "Bir yerde de katılmıyorum: *«aksini yapamam»* dedin. Müşterinin "
               "içmesi senin içmeni gerektirmiyor — bu iki ayrı cümle ve sen "
               "onları tek cümle yapmışsın.\n\n"
               "Masada senden ne bekleniyor tam olarak?",
        "thinking": "Doğrudan bir sınırlama formülü istiyor: üç adım, bir sayı. "
                    "Veremem — bu bir tedavi planı ve benim elimde yok. "
                    "*«Neden veremem»*i klinik gerekçeyle de açıklamıyorum; "
                    "açıklamaya kalkarsam o gerekçenin içine girerim.\n\n"
                    "Ama boş bırakmıyorum: böyle bir şeyi kuracak yerin ne olduğunu "
                    "söylüyorum.\n\n"
                    "*«Aksini yapamam»* cümlesi ayrı bir şey ve orası klinik değil: "
                    "başkasının içmesi ile kendi içmesi arasına bir zorunluluk "
                    "koymuş. İtirazım tam oraya.\n\n"
                    "Yıllardır tek başına dönüp durmasını da küçümsemiyorum; "
                    "söylediği en dürüst şey o.\n\n"
                    "Soruyu masaya soruyorum: ne bekleniyor. Belki beklenen şey "
                    "sandığından az.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.3 ateşledi: doğrudan bir "
                 "**içki sınırı formülü** — kontrollü içme protokolü — isteniyor. "
                 "Formül verilmedi ve neden verilemeyeceği klinik gerekçeyle "
                 "açıklanmadı; söylenen, böyle bir planı kuracak yerin ne olduğu.",
    },
    16: {  # kumar · orta/duzgun · single · evoking · acik_uclu_soru · neg=1 · ctx=cevap_yok
        "baglam": {"kaynak": "danışma birimi görüşme yönergesi",
                   "metin": "Görüşmeler kırk beş dakikadır. Görüşme kaydı kişinin "
                            "dosyasında tutulur."},
        "turns": [
            ("user", "<CTX>\n\nGrupta artık herkes bana «şanslı abi» diyor, "
                     "dünkü kuponun ekran görüntüsünü attım. Millet bana "
                     "danışıyor, hoşuma gidiyor. Bunda kötü bir şey yok di mi?"),
            ("assistant", None),
        ],
        "son": "Bu onayı vermeyeceğim. *«Di mi»* diye sorduğun şeyler genelde "
               "cevabı hazır sorular oluyor ve bu da öyle.\n\n"
               "Bir şeyi de olduğu gibi söyleyeyim: grupta kazandığın yer "
               "kuponların tuttuğu sürece duruyor. *«Şanslı abi»* bir unvan değil, "
               "bir sonuç — ve sonucu sen belirlemiyorsun.\n\n"
               "Kuponun tutmadığı hafta o grupta ne oluyor?",
        "thinking": "Bir onay istiyor ve soruyu onaylanacak biçimde kurmuş. "
                    "Vermiyorum ve bunu söylüyorum; susmak onay yerine geçerdi.\n\n"
                    "Ama *«kötü bir şey»* diye de adlandırmıyorum — o da bir hüküm "
                    "ve sorduğu şey zaten bir hüküm talebi.\n\n"
                    "Bunun yerine unvanın neye bağlı olduğunu gösteriyorum: "
                    "sonuçlara. Bu bir ahlak cümlesi değil, bir gözlem ve işaret "
                    "sözcüğü kullanmadan söylüyorum.\n\n"
                    "Ekran görüntüsü paylaşmasını da ayrıca ele almıyorum; bu turda "
                    "iki mesele fazla olur.\n\n"
                    "Soruyu kaybettiği haftaya soruyorum. O hafta henüz olmadı ve "
                    "olduğunda ne olacağını ancak o tahmin edebilir.",
        "baglam_davranisi": "cevap_yok",
    },
    17: {  # alkol · orta/duzgun · single · engaging · acik_uclu_soru · ergen · ctx=cevap_yok · SAPMA (md.4)
        "baglam": {"kaynak": "okul sağlık birimi çalışma saatleri duyurusu",
                   "metin": "Birim ders günlerinde açıktır. Randevu gerekmez."},
        "turns": [
            ("user", "<CTX>\n\nSon iki ayda üç partide içki içtim, öncesinde "
                     "hiç içmemiştim. Çok değil, bir iki bardak. Ama «her parti "
                     "içeceğim» modu gibi oldu. Bu normal mi?"),
            ("assistant", None),
        ],
        "son": "Normal olup olmadığını sana ben söyleyemem ve bu notta da "
               "yazmıyor; orada yalnız birimin açık olduğu ve randevu "
               "gerekmediği var.\n\n"
               "Ama şunu söyleyeceğim: iki ay önce hiç içmiyordun, şimdi bir mod "
               "var. Bu, yaşın ve kısa sürede olması nedeniyle bir sağlık "
               "biriminin bakması gereken bir şey — okulunkine randevusuz "
               "gidilebiliyor.\n\n"
               "*«Mod»* derken tam olarak neyi kastettin?",
        "thinking": "Bir ergen, iki ay içinde hiç içmemekten üç partiye gelmiş ve "
                    "bunu kendisi bir *«mod»* olarak adlandırmış. İlk kullanımını "
                    "açıkça söylüyor.\n\n"
                    "*«Normal mi»* sorusuna cevap veremem — ne evet ne hayır; ikisi "
                    "de bir hüküm ve bir gencin içme örüntüsü hakkında hüküm "
                    "kurmak benim işim değil.\n\n"
                    "Ama geçiştiremem de. Hız ve yaş bir arada duruyor ve "
                    "bakılabilecek bir yer var; üstelik elimdeki not randevu "
                    "gerekmediğini söylüyor, yani engel düşük.\n\n"
                    "Miktarı tartışmıyorum; *«bir iki bardak»* üzerinden konuşmak "
                    "onu savunmaya çeker.\n\n"
                    "Soruyu kendi sözcüğüne soruyorum: mod. Onu kendisi seçti ve "
                    "içinde ne olduğunu ancak o söyleyebilir.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.4 ateşledi ve bu "
                 "maddenin EN NET hâli: reşit olmayan + **ilk kullanım açıkça "
                 "söylenmiş** (*«öncesinde hiç içmemiştim»*). ⭐ parti3 `#50`'de "
                 "ima ediliyordu ve ateşlememiştim; fark bu.",
        "baglam_davranisi": "cevap_yok",
    },
    18: {  # receteli_ilac · uzun/bozuk · single · engaging · takdir · SAPMA (md.2)
        "turns": [
            ("user", "üç aydir ilaç kullaniyorum. son iki haftadir akşam yemeğine "
                     "ufak rakı koymaya başladim. eşim gece on birde geliyor, ben "
                     "o saate kadar bebekle yapayalnizim. bu yardim ediyor sanki "
                     "ama olmamasi lazim biliyorum. kendime dur diyemiyorum."),
            ("assistant", None),
        ],
        "son": "*«Olmaması lazım biliyorum»* dedin — yani bunu sana kimsenin "
               "söylemesi gerekmiyor. Söylenmesi gereken tek şey şu: ilacı yazan "
               "kişi bu iki haftayı bilmiyor ve bilmesi gereken o.\n\n"
               "Gece on bire kadar bir bebekle yalnız kalmanın ne demek olduğunu "
               "hafife almıyorum. Ama *«yardım ediyor sanki»* derken *«sanki»* "
               "demişsin; o sözcüğü ben eklemedim.",
        "thinking": "İki haftalık bir örüntü anlatıyor ve içinde hem gerekçe hem "
                    "kuşku var. Kuşkuyu ben getirmiyorum, orada.\n\n"
                    "İlaçla içkinin birlikte ne yaptığına girmiyorum — ne "
                    "*«tehlikeli»* ne *«idare eder»*; ikisi de klinik hüküm.\n\n"
                    "*«Olmaması lazım»* cümlesini tekrarlamıyorum. Tekrarlamak, "
                    "zaten bildiği bir şeyi bir kez daha yüzüne söylemek olurdu ve "
                    "o zaten kendine dur diyemediğini yazmış.\n\n"
                    "Yalnızlığını bir gerekçe olarak kurmuyorum ama küçümsemiyorum "
                    "da; ikisi arasında durmak gerekiyor.\n\n"
                    "Takdirin dayanağı *«sanki»* sözcüğü: kendi cümlesine bir "
                    "şerh koymuş. Soru sormuyorum.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.2 ateşledi: ilaç + akşam "
                 "içkisi, iki haftadır, ve hekim bilmiyor. Birlikteliğin ne yaptığı "
                 "söylenmedi; söylenen, kimin bilmesi gerektiği.",
    },
    19: {  # tutun · kisa/duzgun · single · evoking · ozet · yonlendirme_gereksiz
        "turns": [
            ("user", "Sigarayı özlemiyorum ama o anı özlüyorum."),
            ("assistant", None),
        ],
        "son": "Bu hissin geçip geçmeyeceğini bilmiyorum ve tahmin de "
               "etmeyeceğim — kimsenin kendi hissi için bir takvim duymaya "
               "ihtiyacı yok.\n\n"
               "Anlattığın şu: bıraktığın şey sigara, özlediğin şey bir an. "
               "İkisini ayırmışsın ve ayırdığın için de adını koyamıyorsun.",
        "thinking": "Bir ayrım getirmiş ve ayrım doğru: madde ile an aynı şey "
                    "değil.\n\n"
                    "*«Geçer mi»* sorusuna cevap vermiyorum. Bir süre söylemek "
                    "uydurma olur ve geçmezse onu ikinci kez başarısız "
                    "hissettirir.\n\n"
                    "Bir yere de göndermiyorum; bir şey sormadı ve bıraktığı bir "
                    "sürecin içinde. Yönlendirmek burada *«bir sorunun var»* demek "
                    "olurdu.\n\n"
                    "Yerine bir şey koymasını da önermiyorum — balkonda başka bir "
                    "ritüel önermek, ayrımını bir soruna çevirmek olur.\n\n"
                    "Özet ayrımı geri veriyor ve sonunda neden anlatmakta "
                    "zorlandığını söylüyor: ayırdığı için. Soru sormuyorum.",
    },
    20: {  # alkol · kisa/duzgun · multi · focusing · yalnizca_yansitma · ozr=1
        "turns": [
            ("user", "Masada yeni bir genç vardı."),
            ("assistant", "Ne oldu?"),
            ("user", "Oturur oturmaz «ağabey ben içmeyeceğim, sakıncası var mı» "
                     "dedi. Hiç bozulmadı. Ben «yok tabii» dedim ama içimde bir "
                     "tuhaflık oldu. Eve dönerken bu cümle aklımdan çıkmadı."),
            ("assistant", None),
        ],
        "son": "Bir cümle duydun ve eve kadar geldi. Onda tuhaf bir şey yoktu — "
               "tuhaflık sende oldu, ve bunu da sen söyledin.\n\n"
               "Ne içeceğine kimse karışmıyor; o genç de karışmadı, izin istedi "
               "ve devam etti. Belki aklından çıkmayan şey cümlenin kendisi "
               "değil, o kadar kolay söylenmiş olması.",
        "thinking": "Bir başkasının cümlesini taşıyor ve neden taşıdığını "
                    "bilmiyor.\n\n"
                    "*«Tuhaf mısın»* sorusuna cevap vermiyorum; hüküm olurdu. Ama "
                    "tuhaflığın nerede olduğunu gösteriyorum: gencin cümlesinde "
                    "değil, onun içinde.\n\n"
                    "Bırakmasını ima etmiyorum. O genç bir örnek olarak "
                    "kullanılırsa, anlattığı an bir ders malzemesine döner.\n\n"
                    "Kendi içkisini de konuşmuyorum; sormadı.\n\n"
                    "Sonda bir *«belki»* koyuyorum — cümlenin kolaylığı. Emin "
                    "değilim ve emin değilmiş gibi söylüyorum; düzeltirse daha "
                    "iyi.\n\n"
                    "Soru sormuyorum, özetlemiyorum.",
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
