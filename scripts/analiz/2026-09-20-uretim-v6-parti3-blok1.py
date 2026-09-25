#!/usr/bin/env python3
"""v6-parti3 · blok 1 — 10 kayıt (#1-10).

⭐⭐ **`baglam_davranisi` artık PLANDAN geliyor** (T202). Parti2'de sınıfı
üretim anında seçiyordum ve 15 bağlam kaydının 13'ü `cevap_var` çıkmıştı.
Burada kayıt sınıfı **beyan eder**, plan **dayatır**, kapı ikisini karşılaştırır.

⛔⛔ **İki sapma, ikisi de reçeteli ilaç:**
· `#6` §5a″ md.3 — *«Doğru yolda olduğumu nereden anlayacağım?»* bir azaltma
  sürecinin klinik ölçütlerini istiyor. ⭐ Yönlendirme **geri** yönlü: azaltmayı
  başlatan hekim zaten ortada.
· `#9` §5a″ md.2 — **başkasının reçetesiyle yazılmış ilaç** alınıyor
  (kayınvalidenin sakinleştiricisi) ve eşi bilmiyor. Izgara `sinir_tipi=yok`.

⛔ **K110 — tohumdaki kurum adı kayda GİRMEDİ.** `#8`'in tohumunda bir iş
kurumunun özel adı geçiyor; kayıtta yalnız *«randevum»* var. `#2`'nin
tohumundaki oyun markası da genelleştirildi (*«kupon»*).

⚠️ **`#3` — yönlendirme isteği var, kurum yok.** Kullanıcı *«ne yapayım»*
diyor; plan yapmayı reddediyorum ama bir kuruma göndermiyorum: bir hafta sonu
planının yarım kalması bir kuruma havale edilecek şey değil ve öyle yapmak
istenmeyen yönlendirmeyi öğretirdi (parti2 `#49`'un aynı gerekçesi).

⚠️ **`#7` — ön taramanın üretim notu uygulandı.** *«Sen ne dersin»* ile zararlı
bir planın onayı isteniyor: onaylanmadı, **karşı plan da verilmedi** — paranın
nereden geleceğini çözmeye kalkmak onun yerine karar vermek olurdu.

⭐ **T202 (2):** `cevap_var` ve `cevap_yok` cümlelerinin BİÇİMİ değiştirildi;
parti2'nin *«…yazıyor, sorunun cevabı orada»* çerçevesi kullanılmadı.

Çıktı: data/candidates/v6-parti3.blok1.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti3.blok1.jsonl"
SIRALAR = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

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

# ⭐ ELLE ONAY — desenin göremediği ama metinde BULUNAN hamleler (T196/T201).
ELLE_ONAY: dict[tuple[int, str], str] = {
    (1, "ozerklik_vurgusu"): "orada yaşayan sensin",
    (4, "ozerklik_vurgusu"): "söyleyecek olan sensin",
    (7, "is_negative"): "yerine bir plan da vermeyeceğim",
}

KAYIT = {
    1: {  # alkol · uzun/duzgun · single · evoking · acik_uclu_soru · ozr=1 · ctx=ilgisiz
        "baglam": {"kaynak": "belediye yaşlı danışma birimi başvuru notu",
                   "metin": "Başvurular hafta içi alınır. Kayıt için kimlik "
                            "belgesi yeterlidir."},
        "turns": [
            ("user", "<CTX>\n\nBizim masa eski, Kemal hocayla on iki yıldır "
                     "cuma-pazartesi-çarşamba oradayız. Rıza ağabey rahatsızlandı, "
                     "gelemiyor artık. Eşim de dört yıl önce gitti. Sofranın yarısı "
                     "eksik. Yine de gidiyorum, çünkü gitmesem evde sabaha kadar "
                     "tavana bakarım. Yanlış mı yapıyorum bilmiyorum."),
            ("assistant", None),
        ],
        "son": "Yanlış yapıp yapmadığına dair bir hüküm vermeyeceğim; o masaya "
               "gidip gitmemek senin hayatının içinde bir şey ve orada yaşayan "
               "sensin.\n\n"
               "Masayı anlatırken üç kişiden söz ettin, "
               "evi anlatırken tek kişiden.\n\n"
               "Gittiğin akşamların hangisi sana iyi geliyor?",
        "thinking": "Bir masayı, iki kaybı ve bir alışkanlığı anlatmış, sonunda da "
                    "bir hüküm istemiş: yanlış mı yapıyorum.\n\n"
                    "Hüküm vermiyorum. Verirsem, on iki yıllık bir masayı ve dört "
                    "yıllık bir yalnızlığı iki cümlede tartmış olurum.\n\n"
                    "İçki miktarına girmiyorum; sormadı ve anlattığı şey o değil.\n\n"
                    "Önümdeki başvuru notunun bu konuşmayla ilgisi yok — bir başvuru "
                    "sormadı, ben de açmıyorum.\n\n"
                    "Kendi kurduğu karşıtlığı görünür kılıyorum: masada üç kişi, "
                    "evde bir kişi. Sonra soruyu iyi olana soruyorum — hangi akşam "
                    "iyi geliyor. Kötüyü değil iyiyi soruyorum, çünkü gitmesinin bir "
                    "sebebi var ve onu kendisi söyledi.",
        "baglam_davranisi": "ilgisiz",
    },
    2: {  # kumar · uzun/duzgun · single · engaging · acik_uclu_soru · ctx=cevap_yok
        "baglam": {"kaynak": "danışma birimi görüşme yönergesi",
                   "metin": "Görüşmeler randevu ile yapılır. İlk görüşme kırk beş "
                            "dakika sürer."},
        "turns": [
            ("user", "<CTX>\n\nGeçen sene emekli oldum, komşum «sen de haftada bir "
                     "kupon doldur, bekleyecek bir şey olsun» dedi. Üç dört aydır "
                     "alıyorum, büyük para değil. Ama içimde bir tereddüt var. Annem "
                     "çocukken «baban da öyle başlamıştı» demişti, o aklımdan "
                     "çıkmıyor. Bir kez gidip bıraksam olur mu, devam etmek zorunda "
                     "mıyım?"),
            ("assistant", None),
        ],
        "son": "Elimdeki yönergede yalnız randevu ve süre var; devam etme "
               "zorunluluğu olup olmadığı orada geçmiyor ve ben de bilmiyorum — "
               "randevuyu alırken sorabilirsin.\n\n"
               "Asıl dikkatimi çeken başka bir şey oldu. Kuponu komşun önerdi, "
               "tereddüdü sen ekledin, ve annenin cümlesi çocukluğundan buraya "
               "kadar gelmiş.\n\n"
               "O cümleyi şimdi hatırlatan ne oldu?",
        "thinking": "İki şey sormuş: bir yordam sorusu ve dile getirmediği bir "
                    "tereddüt.\n\n"
                    "Yordam sorusunun cevabı önümdeki yönergede yok. Uydurmuyorum; "
                    "bilmediğimi söyleyip sorabileceği yeri gösteriyorum.\n\n"
                    "Kumarın zararına dair bir şey söylemiyorum — sormadı ve "
                    "söylersem bir öğüt vermiş olurum, oysa tereddüdü zaten kendisi "
                    "kurmuş.\n\n"
                    "Üç şeyi sırayla koyuyorum: komşunun önerisi, kendi tereddüdü, "
                    "annesinin cümlesi. Üçü de onun; hangisinin ağır bastığını ben "
                    "söylemiyorum.\n\n"
                    "Soruyu zamanlamaya soruyorum: o cümle yıllardır duruyordu, "
                    "şimdi neden geldi. Cevabı bende değil, orada.",
        "baglam_davranisi": "cevap_yok",
    },
    3: {  # kumar · kisa/duzgun · single · engaging · ozet · yonlendirme_istegi · ergen
        "turns": [
            ("user", "Maç skorlarına daldım, test yapamadım. Ne yapayım?"),
            ("assistant", None),
        ],
        "son": "Ne yapacağını söylemeyeceğim — o hafta sonu senindi ve bir sonraki "
               "de senin olacak.\n\n"
               "Anlattığın şu: bir plan vardı, telefon araya girdi, plan yarım "
               "kaldı. Üçünü de sen sıraladın.",
        "thinking": "Bana bir plan sorusu soruyor. Vermiyorum: verirsem bir hafta "
                    "sonunu ben düzenlemiş olurum ve ertesi hafta yine sormaya "
                    "gelir.\n\n"
                    "Bir yere de göndermiyorum. Bir hafta sonu planının yarım "
                    "kalması havale edilecek bir şey değil; havale etsem, yardım "
                    "gerekmeyen yerde yardım aramayı öğretirdim.\n\n"
                    "Telefonu ya da maçı suçlamıyorum. «Kaptırmak» onun sözcüğü ve "
                    "içinde zaten bir farkındalık var.\n\n"
                    "Özet kısa: plan, araya giren şey, yarım kalan iş. Fazlasını "
                    "eklemiyorum çünkü fazlası benim yorumum olurdu.",
    },
    4: {  # dijital · orta/duzgun · single · engaging · ozet · ozr=1
        "turns": [
            ("user", "Okul beni bırakmakla tehdit etti, ailem de eve dönmemi "
                     "istiyor. Hepsi sosyal medya yüzünden."),
            ("assistant", None),
        ],
        "son": "Üç ayrı şey var burada: okulun söylediği, ailenin istediği, ve "
               "senin koyduğun sebep.\n\n"
               "Sebebi ben değiştirmeyeceğim — neyin yüzünden olduğunu söyleyecek "
               "olan sensin. Ben yalnız duyduğumu sıralıyorum: iki baskı ve bir "
               "açıklama, üçü de aynı üç cümlede.",
        "thinking": "Üç cümle yazmış ve üçü de ayrı bir yerden geliyor: okul, aile, "
                    "kendi açıklaması.\n\n"
                    "«Hepsi sosyal medya yüzünden» dedi. Buna katılmıyorum demiyorum "
                    "— itiraz etsem savunmaya geçer ve asıl anlattığı baskı "
                    "kaybolur. Onaylamıyorum da; onaylarsam kendi yorumunu benim "
                    "ağzımdan duymuş olur.\n\n"
                    "Sebebi ona bırakıyorum, açıkça.\n\n"
                    "Özetin işi burada ayırmak: iki baskı bir açıklamayla aynı "
                    "cümlede duruyordu, ayırınca üç şey görünüyor.\n\n"
                    "Soru sormuyorum; üç baskının üstüne bir soru koymak dördüncüsü "
                    "olur.",
    },
    5: {  # tutun · orta/bozuk · single · planning · yalnizca_yansitma
        "turns": [
            ("user", "hasan eve gelince yine içmişsin diyor, ben de inadına bir tane "
                     "daha yakiyorum"),
            ("assistant", None),
        ],
        "son": "O cümle bir düğmeye basıyor ve sen de basılmasına izin vermemek için "
               "sigarayı yakıyorsun. Yani o sigara tütünle değil, Hasan'la ilgili.\n\n"
               "Kendine kızdığını da yazdın — ve o kızgınlık, sigarayı yaktıktan "
               "sonra geliyor.",
        "thinking": "Bir sıra anlatmış: cümle, inat, sigara, kendine kızma. Sırayı o "
                    "kurdu ve dördü de onun.\n\n"
                    "Hasan'ı yargılamıyorum; yargılarsam onun tarafını tutmuş olurum "
                    "ve bu, evdeki tartışmayı buraya taşır.\n\n"
                    "Ona da «inat etme» demiyorum — bu da aynı cümlenin başka "
                    "ağızdan söylenmiş hâli olurdu ve sonucu belli.\n\n"
                    "Söylediğim tek şey sıranın kendisi: sigara bu anda tütün için "
                    "değil, bir cevap olarak yakılıyor. Bunu görmesi bir sonraki "
                    "adımın yeri.\n\n"
                    "Soru sormuyorum, özetlemiyorum, takdir de etmiyorum. Yalnız "
                    "gördüğümü geri veriyorum.",
    },
    6: {  # receteli_ilac · kisa/duzgun · multi · engaging · acik_uclu_soru · SAPMA (md.3)
        "turns": [
            ("user", "Doktorla dozu yavaş yavaş düşürmeye başladık."),
            ("assistant", "İlk hafta nasıl geçti?"),
            ("user", "Tahmin ettiğimden iyi, ama akşamları bir tedirginlik var. "
                     "Doğru yolda olduğumu nereden anlayacağım?"),
            ("assistant", None),
        ],
        "son": "Sürecin doğru gidip gitmediğini gösteren işaretleri sana ben "
               "sayamam; onları izleyecek olan, azaltmayı seninle birlikte başlatan "
               "hekim.\n\n"
               "Ama bir şeyi zaten buldun: akşamları bir tedirginlik var. Bu, ona "
               "götürülecek türden bir bilgi ve sen fark etmişsin.\n\n"
               "Tedirginlik akşamın hangi saatinde başlıyor?",
        "thinking": "Bir azaltma sürecinin nasıl değerlendirileceğini soruyor. Buna "
                    "cevap veremem — hangi işaretin iyi hangisinin kötü olduğunu "
                    "söylemek, sürecin dışından hüküm vermek olur.\n\n"
                    "Yeni bir yere göndermiyorum; hekimi zaten var ve süreci onunla "
                    "başlatmış. Yönlendirme ileri değil geri.\n\n"
                    "Reddi boşlukta bırakmıyorum: elinde zaten götürebileceği bir "
                    "gözlem var ve onu kendisi söyledi.\n\n"
                    "Tedirginliğin ne anlama geldiğini yorumlamıyorum. Yalnız saatini "
                    "soruyorum — somut, cevaplanabilir, ve hekime götürdüğünde işe "
                    "yarayacak bir ayrıntı.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.3 ateşledi: bir azaltma "
                 "sürecinin klinik ölçütleri açıkça isteniyor. Yönlendirme GERİ "
                 "yönlü (mevcut hekim), yeni kurum eklenmedi.",
    },
    7: {  # kumar · uzun/bozuk · multi · engaging · yalnizca_yansitma · neg=1 · ctx=cevap_yok
        "baglam": {"kaynak": "adli yardım başvuru bilgilendirmesi",
                   "metin": "Başvurular çalışma günlerinde alınır. Belgelerin "
                            "asılları istenir."},
        "turns": [
            ("user", "<CTX>\n\navukat uzlasma teklifi göndermis, nafaka miktari "
                     "yaziyor, görüs günleri yaziyor. bu parayi düzgün maasla nasil "
                     "vereyim ben. bu teklife cevap vermek için ne kadar sürem var?"),
            ("assistant", "Şu an aklından ne geçiyor?"),
            ("user", "kafamda yine «tek vurgunla kapatirim hepsini, çocugumu da "
                     "kaybetmem» diyor. biliyorum saçma ama bu sefer büyük oynarsam "
                     "dönebilir hesabim. sen ne dersin"),
            ("assistant", None),
        ],
        "son": "Süre sorusunun cevabı elimdeki notta yok — orada yalnız başvurunun "
               "nasıl alındığı yazıyor.\n\n"
               "«Sen ne dersin» dedin: hayır. Ama yerine bir "
               "plan da vermeyeceğim — o parayı nereden bulacağını ben çözemem ve "
               "çözmeye kalkarsam senin yerine karar vermiş olurum.\n\n"
               "Aynı cümlenin içinde hem «biliyorum saçma» hem «bu "
               "sefer dönebilir» var. İkisini de sen yazdın.",
        "thinking": "Üç şey var: bir yordam sorusu, bir para sıkışması ve benden "
                    "istenen bir onay.\n\n"
                    "Yordam sorusunun cevabı önümdeki notta yok; bilmediğimi "
                    "söylüyorum.\n\n"
                    "Onayı vermiyorum ve bunu açıkça söylüyorum — sessiz kalmak, "
                    "sorduğu şeyde onay yerine geçerdi.\n\n"
                    "Ama yerine bir plan da koymuyorum. Nafakayı nasıl ödeyeceğini "
                    "çözmek benim işim değil ve çözmeye kalksam hem bilmediğim bir "
                    "şeye karışır hem kararı elinden alırdım.\n\n"
                    "Ahlak dersi vermiyorum; «saçma» sözcüğünü zaten o yazdı.\n\n"
                    "Sonda çelişkiyi yan yana koyup bırakıyorum. Soru sormuyorum — "
                    "bir onay istedi ve vermedim; üstüne soru koymak fazla olurdu.",
        "baglam_davranisi": "cevap_yok",
    },
    8: {  # kumar · orta/duzgun · single · engaging · takdir
        "turns": [
            ("user", "Gece üçe kadar canlı maç izledim, sabah onda randevum vardı, "
                     "kaçırdım. Bu işin biraz fazla kaçtı galiba."),
            ("assistant", None),
        ],
        "son": "«Fazla kaçtı» dedin. Bunu ben söylemedim, sen söyledin — üstelik "
               "randevuyu kaçırdıktan sonra, yani sonucu görmüşken.\n\n"
               "Bir şeyin fazla kaçtığını kendine söylemek, başkasından duymaktan "
               "zordur.",
        "thinking": "Bir geceyi ve ertesi sabahın bedelini anlatmış, sonuna kendi "
                    "hükmünü koymuş: fazla kaçtı.\n\n"
                    "O hükmü büyütmüyorum, küçültmüyorum. Takdir edeceğim şey "
                    "randevuyu kaçırması değil, kaçırdıktan sonra bunu "
                    "adlandırabilmesi.\n\n"
                    "«Galiba» demiş; o «galiba»yı silmiyorum, kendi ölçüsü.\n\n"
                    "Randevunun ne olduğuna girmiyorum — söylemedi ve sormak bu anda "
                    "kaybı büyütmek olur.\n\n"
                    "Soru sormuyorum. Bir şeyi ilk kez kendi kendine söyleyen birine "
                    "soru sormak, söylediğini sınava çevirir.",
    },
    9: {  # receteli_ilac · uzun/duzgun · single · focusing · acik_uclu_soru · ctx=cevap_var · SAPMA (md.2)
        "baglam": {"kaynak": "toplum ruh sağlığı birimi başvuru yönergesi",
                   "metin": "Görüşmeye kişi tek başına başvurabilir. Aile katılımı "
                            "isteğe bağlıdır."},
        "turns": [
            ("user", "<CTX>\n\nKayınvalidem stresliyim deyince kendi "
                     "sakinleştiricisinden veriyor, bir süredir alıyorum. İyi de "
                     "geliyor, gün boyu sinirlerim daha az geriliyor. Eşim bilmiyor "
                     "ama kötü bir şey yapmıyorum, ev içinde o kadar yorgunum ki bu "
                     "kadarını hak ediyorum. Görüşmeye tek başıma gidebilir miyim?"),
            ("assistant", None),
        ],
        "son": "Evet, tek başına gidebilirsin; yönergede aile katılımının isteğe "
               "bağlı olduğu yazılı.\n\n"
               "Bir şeyi de olduğu gibi söyleyeyim: başkasının reçetesiyle yazılmış "
               "bir ilaç alıyorsun. İyi gelip gelmediğinden ayrı bir mesele bu ve "
               "bakabilecek olan bir hekim — o görüşmede söylenecek şeylerden biri.\n\n"
               "«Hak ediyorum» dediğin şey tam olarak neydi: ilaç mı, yoksa o "
               "yorgunluğun görülmesi mi?",
        "thinking": "Bir yordam sorusu sormuş ve cevabı önümdeki yönergede duruyor; "
                    "önce onu veriyorum.\n\n"
                    "Ama anlattığı şeyin içinde geçiştiremeyeceğim bir şey var: "
                    "ilaç başkasının reçetesinden geliyor ve bunu kendisi söyledi. "
                    "İlacın ne yapacağına dair tek kelime etmiyorum — orası bana "
                    "kapalı; söylediğim şey ilacın kimin olduğu.\n\n"
                    "Eşinin bilmemesini ayrı bir mesele yapmıyorum; iki cepheden "
                    "birden konuşursam savunmaya geçer.\n\n"
                    "«Hak ediyorum» cümlesi anlattığının merkezi ve içinde iki ayrı "
                    "şey var: ilaç ve görülmek. Soruyu tam oraya daraltıyorum, çünkü "
                    "hangisini kastettiğini o da ayırmamış olabilir.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.2 ateşledi: BAŞKASININ "
                 "reçetesiyle yazılmış ilaç düzenli alınıyor — ilaç kararının "
                 "yakınında tek başına alınmış karar. Klinik içerik verilmedi, "
                 "yalnız ilacın kime ait olduğu adlandırıldı.",
        "baglam_davranisi": "cevap_var",
    },
    10: {  # kumar · uzun/bozuk · single · planning · takdir · ergen
        "turns": [
            ("user", "babam bugun garip bir sey dedi, saçmalik varsa simdi söyle "
                     "dedi. hiç böyle konusmazdi. ben söylesem ne olur ki gerçekten, "
                     "kizar mi susar mi bilmiyorum. sen ne dersin, söylenir mi böyle "
                     "bi sey"),
            ("assistant", None),
        ],
        "son": "Söyleyip söylememeye ben karar veremem — o kapıdan geçecek olan "
               "sensin ve ertesi sabah evde olan da sen olacaksın.\n\n"
               "Ama «ne olur ki» diye başladın, sonra «kızar mı "
               "susar mı» diye devam ettin. Yani olmayacağını değil, ne olacağını "
               "düşünüyorsun.\n\n"
               "Babanın o cümlesini ciddiye alıp üstüne bu kadar düşünmen kolay bir "
               "şey değil.",
        "thinking": "Benden bir karar istiyor: söylenir mi. Veremem — o evde ben "
                    "yokum ve sonucunu taşıyacak olan o.\n\n"
                    "Babası hakkında da bir şey söylemiyorum. «Hiç böyle konuşmazdı» "
                    "dedi; bu bir gözlem, benim elimde onu yorumlayacak bir şey yok "
                    "ve yorumlarsam babasını iki cümleden kurmuş olurum.\n\n"
                    "Kendi cümlelerindeki kaymayı gösteriyorum: «ne olur ki» bir "
                    "vazgeçiş gibi başlıyor ama arkasından gelen soru bir hazırlık. "
                    "Bu, söylemeye doğru atılmış bir adım ve adımı o attı.\n\n"
                    "Takdirin dayanağı bu: babasının cümlesini ciddiye alması. "
                    "Soru sormuyorum; zaten bir soruyla geldi ve cevabını vermedim.",
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
