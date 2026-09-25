#!/usr/bin/env python3
"""v6-parti7 · blok 4 — 10 kayıt (#31-40).

⭐⭐ **BU BLOKTA DÖRT KAYIT AYNI ŞEYİ REDDETTİ: KOLAY CEVABI.** `#33`
eşin tutumuyla baş etme taktiği, `#35` elli bin liralık borca çözüm,
`#38` *«telefonu kaldır»*, `#40` bilimsel iddiaya hakemlik. Dördünde de
verilecek cevap hazırdı ve dördünde de verilmedi.

⛔ **`#35` — borca çözüm ÜRETİLMEDİ.** Bursu kesilmiş, harcı yatmamış,
elli bin borcu var ve aileye söylemeyi düşünüyor. Söyleme kararı
verilmedi, söylenecek cümle kurulmadı. Son hamle `durur`: yazdığı
sıranın en sonunda *«belki bir çıkış olur»* duruyor ve o cümle
yazılmış — üstüne bir şey konmadı.

⛔ **`#38` ve `#40` peşinen itiraz ediyor** (*«bana telefonu kaldır
diyeceksen boş»*, *«bunda ne var ki»*). İkisinde de itiraz doğrulandı
ama konuşma orada kapanmadı.

⛔ **`#40`'ta bilimsel iddia ne doğrulandı ne çürütüldü.** Ergen ama
md.4 ateşlemiyor: ilk kullanım ve bedensel bildirim yok.

⛔ `#32`'de annesinin ne yapacağı tahmin edilmedi, kurum adı
genelleştirildi. `#33`'te eşin tutumu yargılanmadı. `#36`'da *«oğlunla
konuş»* söylenmedi — kullanıcı bunu zaten bekliyordu.

⭐ `#33` partinin tek `yonlendirme_gereksiz` kaydı: yeri kendisi
bulmuş, gösterilecek bir yer yok.

Çıktı: data/candidates/v6-parti7.blok4.jsonl
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
PLAN = KOK / "data/plan/v6-parti7.jsonl"
CIKTI = KOK / "data/candidates/v6-parti7.blok4.jsonl"
SIRALAR = list(range(31, 41))

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
    (31, "ozerklik_vurgusu"): "Bakkala inip inmemene karışmıyorum",
}

KAYIT = {
    31: {  # tutun · uzun/duzgun · single · planning · yalnizca_yansitma · ozerklik · ctx=izin_iste
        "baglam": {"kaynak": "bir danışma biriminin gizlilik notu",
                   "metin": "Görüşme kayıtları yalnız danışanın izniyle "
                            "paylaşılır."},
        "turns": [
            ("user", "<CTX>\n\nPaket bitti. Az önce son sigarayı içtim, dizinin "
                     "bölümü daha bitmemişti bile. Şimdi otomatik olarak "
                     "çantamı alıp aşağı bakkala inmek üzereyim. Birdenbire "
                     "bunu görünce garip hissettim, sanki ben değilim de "
                     "alışkanlık beni yönetiyor."),
            ("assistant", None),
        ],
        "son": "Bakkala inip inmemene karışmıyorum ve 'inme' de demiyorum.\n\n"
               "Elimde bir gizlilik notu var; işine yarayacaksa aktarayım, "
               "gerek yoksa hiç açmam.\n\n"
               "Şu an olanı olduğu gibi bırakıyorum: paket bitti, çantanı "
               "aldın, kapıya doğru gidiyorsun — ve bunu yaparken kendini "
               "dışarıdan görüyorsun. Üçü aynı anda oluyor.\n\n"
               "'Sanki ben değilim' diyorsun. Ama o cümleyi kuran biri var ve "
               "o, kapıya doğru giden kişiyle aynı kişi.",
        "thinking": "Tam eylemin ortasında yazmış. Bu anda 'inme' demek en "
                    "güçlü müdahale gibi görünür ve en kırılgan olanı: "
                    "inerse hem sigarayı içer hem beni yalanlamış olur.\n\n"
                    "Demiyorum. Bir alternatif de önermiyorum; 'su iç, yürü' "
                    "türü bir taktik bu anı bir teknik sorusuna "
                    "çevirirdi.\n\n"
                    "Kaç sigara içtiğini sormuyorum, bırakmadan söz "
                    "etmiyorum.\n\n"
                    "Elimdeki not işine yarayabilir ama önüne koymadan önce "
                    "soruyorum.\n\n"
                    "'Alışkanlık beni yönetiyor' cümlesini de çürütmüyorum. "
                    "Çürütürsem, kendini dışarıdan görebilmiş olmasını "
                    "tartışmaya açarım.\n\n"
                    "Soru sormuyorum. Yalnız üç şeyin aynı anda olduğunu "
                    "söylüyorum ve son cümlede iki kişiyi tek kişiye "
                    "indiriyorum — bu bir yorum değil, cümlesinin içinde "
                    "duran şey.",
        "baglam_davranisi": "izin_iste",
    },
    32: {  # receteli_ilac · kisa/duzgun · multi · focusing · yalnizca_yansitma
        "turns": [
            ("user", "Annem sonunda yattı, bugün ikinci günü."),
            ("assistant", "Sen nasılsın?"),
            ("user", "Biraz rahatladım ama içim hâlâ tedirgin. Titremesi "
                     "azalmış, mide tedavisi sürüyor. Taburcu olunca eve döner "
                     "mi, bir daha mı başlar, evi nasıl hazırlayayım. Kime "
                     "danışayım taburculuk sonrası için?"),
            ("assistant", None),
        ],
        "son": "Taburculuk sonrasını en iyi bilecek yer, annenin şu an yattığı "
               "servis; taburculuk planını hazırlayan ekip de orada. Soruyu "
               "oraya sorabilirsin.\n\n"
               "Annenin bundan sonra ne yapacağını bilmiyorum ve bir tahmin de "
               "yürütmüyorum.\n\n"
               "Yazdıklarında dört soru var ve dördü de aynı yere bakıyor: "
               "eve. Annen henüz serviste ve sen çoktan evi düşünüyorsun.\n\n"
               "'Rahatladım ama içim tedirgin' demişsin. İkisi aynı cümlede "
               "duruyor — ve tedirginlik annenle değil, onu bekleyen evle "
               "ilgili gibi.",
        "thinking": "Yakını yatmış ve sorular taburculuk sonrasına dair. "
                    "Cevabı bende olmayan şeyleri ayırmam gerek.\n\n"
                    "Annesinin eve dönüp dönmeyeceğini, yeniden başlayıp "
                    "başlamayacağını söylemiyorum. Bunlar tahmin olurdu ve "
                    "tahminin iyi yönü bile bir vaat.\n\n"
                    "Kurum adı anmıyorum, evi nasıl hazırlayacağına dair bir "
                    "liste de vermiyorum; o liste onun değil, bir uzmanın "
                    "işi.\n\n"
                    "İlaç ya da tedavi hakkında hiçbir şey söylemiyorum.\n\n"
                    "Sorduğu tek yordamsal şeye cevap veriyorum: soruyu "
                    "soracağı yer belli.\n\n"
                    "Soru sormuyorum. Yansıttığım şey dört sorunun da eve "
                    "bakması; bunu o yazdı, ben yalnız sayıyorum.",
    },
    33: {  # alkol · kisa/duzgun · single · engaging · yalnizca_yansitma · yonlendirme_gereksiz
        "turns": [
            ("user", "Eşim 'sen ne ararsın orada' dedi, içime kapandım."),
            ("assistant", None),
        ],
        "son": "Sana bir yer göstermeyeceğim. Yeri zaten bulmuşsun ve neden "
               "orayı seçtiğini de biliyorsun.\n\n"
               "Eşinin tutumunu yargılamıyorum, onunla nasıl baş edeceğine "
               "dair bir yol da göstermiyorum.\n\n"
               "Cümleni olduğu gibi bırakıyorum: bir şey buldun, söyledin, ve "
               "söyledikten sonra içine kapandın. Üçüncüsü ilk ikisinin hemen "
               "ardından geldi.\n\n"
               "Kapanan şey senin fikrin değildi — konuşma kapandı.",
        "thinking": "Bir yer aramıyor; yeri kendisi bulmuş. Bu yüzden "
                    "yönlendirme gereksiz ve yapsam, onun yaptığı işi "
                    "görmezden gelmiş olurum.\n\n"
                    "Eşinin tutumunu yargılamıyorum. 'Böyle demesi doğru "
                    "değil' demek kolay olurdu ve bu akşam evde iki kişi "
                    "var.\n\n"
                    "Onunla nasıl konuşacağına dair bir taktik de vermiyorum. "
                    "Taktik verirsem, kapanan konuşmayı bir beceri sorununa "
                    "çeviririm.\n\n"
                    "İçkiden hiç söz etmiyorum; bugün anlattığı şey o "
                    "değil.\n\n"
                    "'İçime kapandım'ı da bir hata gibi ele almıyorum.\n\n"
                    "Soru sormuyorum. Üç adımı sırayla söylüyorum ve son "
                    "cümlede kapanan şeyin ne olduğunu ayırıyorum — fikri "
                    "değil, konuşmayı.",
    },
    34: {  # tutun · kisa/duzgun · multi · focusing · acik_uclu_soru · RED · ERGEN
        "turns": [
            ("user", "Bu yaşta bırakmaya çalışmak komik mi olur?"),
            ("assistant", "Bu soru nereden geldi?"),
            ("user", "Grupta biri 'bırakalım artık, paramız yetmiyor' dedi. "
                     "Öteki 'ne bırakacağız, sosyal bir şey bu' dedi. Ben ne "
                     "diyeceğimi bilemedim."),
            ("assistant", None),
        ],
        "son": "Komik olup olmayacağını söyleyemem. Komiklik bir ölçü değil, "
               "bir odadaki bakış — ve ben o odada değilim.\n\n"
               "İki arkadaşın iki ayrı şey söylemiş ve ikisi de kendi içinde "
               "tutarlı. Sen ikisine de katılmamışsın, 'bilemedim' "
               "demişsin.\n\n"
               "Ama o soruyu şimdi bana sordun. Grupta susan biri, burada "
               "sormuş.\n\n"
               "Sen orada ne demek istemiştin?",
        "thinking": "Bir hüküm isteniyor: komik mi. Vermem, çünkü komikliğin "
                    "ölçüsü o gruptaki bakışta ve ben orada değilim.\n\n"
                    "Bırakmasını da söylemiyorum. Ergen olması bunu daha da "
                    "kolay bir öğüde çevirirdi ve öğüt bugün sorduğu şey "
                    "değil.\n\n"
                    "Sigaranın zararından söz etmiyorum, harçlık hesabına "
                    "girmiyorum.\n\n"
                    "Arkadaşlarından birini haklı çıkarmıyorum; ikisi de "
                    "kendi içinde tutarlı ve tarafını seçmek bana "
                    "düşmez.\n\n"
                    "Tutunduğum yer suskunluğu: grupta bilememiş ama burada "
                    "sormuş. Bu farkı gösteriyorum.\n\n"
                    "Soruyu oraya soruyorum. 'Ne demek istemiştin' sorusu, "
                    "söyleyemediği cümleyi aramaya bir yer açıyor.",
    },
    35: {  # kumar · kisa/duzgun · multi · engaging · durur
        "turns": [
            ("user", "İlk kez aileme söylemeyi düşünüyorum."),
            ("assistant", "Şu an nasılsın?"),
            ("user", "Elim ayağım titriyor. Bursum kesildi, harç yatmadı, elli "
                     "bin borç oldu. Oda arkadaşımdan da altı bin var, o "
                     "biliyor ama hiç yüklenmiyor. Babam çok kızacak, annem "
                     "ağlar belki. Söylersem belki bir çıkış olur diye "
                     "düşünüyorum ama söyleyemiyorum işte."),
            ("assistant", None),
        ],
        "son": "Borca bir çözüm önermeyeceğim; öyle bir şey elimde yok.\n\n"
               "Aileye söyleyeceğin cümleyi de senin yerine kurmuyorum.\n\n"
               "Yazdığın sırada bir şey var: önce titreme, sonra rakamlar, "
               "sonra baban ve annen, en sonda 'belki bir çıkış olur'. O cümle "
               "en sona kalmış ama yazılmış.\n\n"
               "Şimdilik burada duruyorum.",
        "thinking": "Rakamlar ağır ve ilk dürtü bir çözüm aramak: yapılandırma, "
                    "ödeme planı, bir yere başvurma. Hiçbirini "
                    "bilmiyorum.\n\n"
                    "Aileye söylemesini de söylemiyorum, söylememesini de. "
                    "Kararı verirsem sonucunu da üstlenmem gerekir ve "
                    "üstlenemem.\n\n"
                    "Söyleyeceği cümleyi kurmuyorum. O cümleyi ben yazsam, "
                    "babasının karşısına çıkan onun sesi olmaz.\n\n"
                    "Babasının kızacağı, annesinin ağlayacağı tahminlerini de "
                    "yumuşatmıyorum; onları o biliyor.\n\n"
                    "Oda arkadaşının yüklenmemesini de bir kaldıraç "
                    "yapmıyorum.\n\n"
                    "Yaptığım tek şey yazdığı sırayı okumak: umut cümlesi en "
                    "sonda ama var.\n\n"
                    "Soru sormuyorum, öneri vermiyorum. Titreyen biri "
                    "karşımda ve bugün en az şeyi yapmak doğru olabilir.",
    },
    36: {  # alkol · uzun/duzgun · single · engaging · acik_uclu_soru
        "turns": [
            ("user", "Oğlum dün aradı, on dakika konuştuk. Sesimden anladı "
                     "sanırım; 'anne yine mi' demedi ama susması her şeyi "
                     "söyledi. Telefonu kapatınca yarım şişe daha içtim. Şimdi "
                     "bana onunla konuşmamı söyleyeceksin, biliyorum. "
                     "Komşulara bile görünmek istemiyorum ben."),
            ("assistant", None),
        ],
        "son": "Haklısın, onunla konuşmanı söylemeyeceğim. Bunu daha önce "
               "duymuşsun belli ki ve her duyduğunda bir şey eksilmiş.\n\n"
               "Ne kadar içtiğine dair de bir şey söylemiyorum.\n\n"
               "'Kadının içmesi başka konuşuluyor' diye yazmışsın. O cümle "
               "komşularla ilgili ama sen onu kendi üstünde taşıyorsun — "
               "oğlunun susması da aynı yere düşmüş gibi.\n\n"
               "Telefonu kapattığın anda ne hissettin?",
        "thinking": "Peşinen itiraz ediyor: bana ne söyleyeceğimi biliyor. "
                    "Bunu boşa çıkarmam gerek, ama boşa çıkarmanın yolu onu "
                    "yalanlamak değil, dediğini yapmamak.\n\n"
                    "Oğluyla konuşmasını söylemiyorum. Söylersem hem "
                    "tahminini doğrularım hem de daha önce işe yaramamış bir "
                    "cümleyi tekrarlarım.\n\n"
                    "Yarım şişeyi yorumlamıyorum, bir sınır önermiyorum.\n\n"
                    "Komşulara dair yargıyı da çürütmüyorum. 'Öyle "
                    "düşünmüyorlardır' demek, bildiği bir şeyi "
                    "yalanlamak.\n\n"
                    "Utancını da yatıştırmıyorum.\n\n"
                    "Gösterdiğim şey iki susmanın aynı yere düşmesi: "
                    "komşuların bakışı ve oğlunun sessizliği. Bu bir yorum "
                    "ama cümlelerinin yan yana durmasından çıkıyor.\n\n"
                    "Soruyu telefonu kapattığı ana soruyorum. Yarım şişe "
                    "oradan sonra geldi.",
    },
    37: {  # dijital · orta/duzgun · single · evoking · yalnizca_yansitma
        "turns": [
            ("user", "Sınava çalışıyorum ama hangi bölümü istediğimi "
                     "bilmiyorum. 'Ne için çalışıyorum ki' diye düşününce "
                     "motivasyon kayboluyor ve sosyal medyaya giriyorum."),
            ("assistant", None),
        ],
        "son": "Hangi bölümü isteyeceğini söylemeyeceğim ve bir hedef de "
               "koymayacağım.\n\n"
               "Yazdığın sıra şöyle: soru geliyor, motivasyon gidiyor, telefon "
               "açılıyor. Üçünü de bu sırayla sen dizdin.\n\n"
               "'Ne için çalışıyorum ki' bir erteleme cümlesi gibi duruyor ama "
               "içinde bir arayış var — bilmediğini bilen biri soruyor "
               "onu.\n\n"
               "Sosyal medya o sorunun cevabı değil; sorunun kesildiği yer.",
        "thinking": "Bir boşluk anlatıyor ve boşluğu doldurmak çok kolay "
                    "olurdu: bir hedef öner, bir bölüm say, bir yöntem "
                    "ver.\n\n"
                    "Hiçbirini yapmıyorum. Hedefi ben koyarsam, çalışmanın "
                    "sebebi de benim olur ve ilk zorlandığı gün düşer.\n\n"
                    "Ekran süresine dair bir sayı ya da kısıt "
                    "önermiyorum.\n\n"
                    "Motivasyon üstüne bir açıklama da kurmuyorum; "
                    "'kaçınma' gibi bir ad koymak bir yorum olurdu.\n\n"
                    "Sosyal medyayı da suçlamıyorum. Suçlarsam, asıl "
                    "söylediği şeyi — ne için çalıştığını bilmemeyi — "
                    "gölgelerim.\n\n"
                    "Soru sormuyorum. Yaptığım şey sırayı geri vermek ve "
                    "sorunun kesildiği yeri adlandırmak.",
    },
    38: {  # dijital · orta/duzgun · single · evoking · acik_uclu_soru · ERGEN
        "turns": [
            ("user", "Arada uygulamaya bakıyorum, durduramıyorum. Ama ailemi "
                     "hayal kırıklığına uğratmak istemiyorum. Bana da 'telefonu "
                     "kaldır' diyeceksen boş, onu herkes söylüyor."),
            ("assistant", None),
        ],
        "son": "Telefonu kaldır demeyeceğim. Zaten söyleyen çok ve işe "
               "yaramadığını sen görmüşsün.\n\n"
               "İki şey yan yana duruyor: durduramamak ve hayal kırıklığı "
               "yaratmamak. Birincisini elinde olmayan bir şey gibi "
               "anlatmışsın, ikincisini tamamen sana bağlıymış gibi.\n\n"
               "Aileni hayal kırıklığına uğratmak derken aklına gelen tam "
               "olarak ne?",
        "thinking": "Peşinen bir cümleyi kapatıyor ve haklı: o cümleyi herkes "
                    "söylemiş. Söylersem sıradaki kişi olurum.\n\n"
                    "Bir süre sınırı, bir uygulama ya da bir yöntem de "
                    "önermiyorum; hepsi aynı cümlenin başka kılıkları.\n\n"
                    "Ailesini de araya sokmuyorum. 'Onlar seni düşünüyor' "
                    "demek baskıyı artırırdı.\n\n"
                    "'Durduramıyorum'u da çürütmüyorum.\n\n"
                    "Gösterdiğim şey iki cümlenin farklı kurulması: biri "
                    "edilgen, öbürü tamamen kendi sorumluluğunda. Bu farkı "
                    "adlandırıyorum ama bir sonuç çıkarmıyorum.\n\n"
                    "Soruyu hayal kırıklığının içine soruyorum. Ergen biri "
                    "için o sözcüğün altında çoğu zaman somut bir sahne "
                    "vardır ve onu yalnız o görebilir.",
    },
    39: {  # dijital · orta/duzgun · single · evoking · acik_uclu_soru · ctx=cevap_yok
        "baglam": {"kaynak": "bir danışma biriminin başvuru notu",
                   "metin": "Başvurular çalışma saatleri içinde alınır. "
                            "Görüşme öncesi kısa bir form doldurulur."},
        "turns": [
            ("user", "<CTX>\n\nAilem benim için çok fedakârlık yapıyor. Bunu "
                     "düşündükçe daha çok baskı hissediyorum ve garip bir "
                     "şekilde daha çok giriyorum uygulamaya. Görüşmeler "
                     "ücretli mi?"),
            ("assistant", None),
        ],
        "son": "Elimdeki not başvurunun nasıl yapıldığını söylüyor ama ücretten "
               "söz etmiyor. Onu ancak başvuracağın yer söyleyebilir.\n\n"
               "Ücreti sormanın bugün anlattığınla bir ilgisi olabilir: "
               "ailenin fedakârlığını düşünürken bir masraf daha çıkarmak "
               "istemiyor olabilirsin. Bunu ben kurdum, yanlışsa "
               "düzeltebilirsin.\n\n"
               "'Garip bir şekilde daha çok giriyorum' demişsin. Baskı "
               "arttıkça oraya girmen sana neden garip geliyor?",
        "thinking": "İki şey var: bir yordam sorusu ve altında duran bir "
                    "ağırlık. Yordam sorusunun cevabı önümdeki notta yok; "
                    "uydurmuyorum.\n\n"
                    "Ücret hakkında bir rakam ya da tahmin de vermiyorum.\n\n"
                    "Ailesinin fedakârlığını bir borç gibi de ele almıyorum; "
                    "'onlar için yap' demek baskıyı ikiye katlardı.\n\n"
                    "Ekran süresine dair bir hedef koymuyorum.\n\n"
                    "İki şeyi birbirine bağlarken bunu bir tespit gibi "
                    "sunmuyorum: kurduğumu söylüyorum ve düzeltmesine yer "
                    "bırakıyorum.\n\n"
                    "Soruyu kendi 'garip' sözcüğüne soruyorum. Baskı ile "
                    "kaçış arasındaki bağı ben adlandırmıyorum; garipliğin "
                    "nerede olduğunu o söyleyecek.",
        "baglam_davranisi": "cevap_yok",
    },
    40: {  # kumar · uzun/bozuk · single · evoking · acik_uclu_soru · ERGEN
        "turns": [
            ("user", "saat gec biliyorum. aksam fizik calisiyordum, bir yandan "
                     "mac vardi, kupona goz attim arada. herkes telefonla "
                     "calisiyor zaten, bilim insanlari da diyor kucuk molalar "
                     "verin diye. bunda ne var ki ya"),
            ("assistant", None),
        ],
        "son": "Bilim insanlarının ne dediği konusunda bir şey "
               "söylemeyeceğim — ne doğrularım ne çürütürüm, orası benim "
               "bildiğim bir alan değil.\n\n"
               "'Bunda ne var ki' diye soruyorsun ama saatin geç olduğunu ilk "
               "cümlede yazan da sensin. İkisi aynı mesajda duruyor.\n\n"
               "Mola ile kupon arasında senin için bir fark var mı?",
        "thinking": "Bir savunma getiriyor ve savunmanın içinde bir bilimsel "
                    "iddia var. İddiayı çürütmek en kolay hamle ve en işe "
                    "yaramaz olanı: tartışmayı kaynaklara taşır.\n\n"
                    "Doğrulamıyorum da. Doğrularsam savunma tamamlanır ve "
                    "konuşacak bir şey kalmaz.\n\n"
                    "Kaç para yatırdığını sormuyorum, yaşına dair bir şey "
                    "söylemiyorum.\n\n"
                    "Ders çalışmasını da övmüyorum; övmek, kuponu görmezden "
                    "gelmek olurdu.\n\n"
                    "Saati de bir suçlamaya çevirmiyorum. Yalnız ilk "
                    "cümlesinde geçtiğini söylüyorum — onu yazan o.\n\n"
                    "Soruyu ayrımın kendisine soruyorum: mola ile kupon aynı "
                    "şey mi. Bu soruya kendi vereceği cevap, savunmanın "
                    "içindeki boşluğu ona gösterebilir.",
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
              "system_prompt_variant": "canon", "parti": "v6-parti7",
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
