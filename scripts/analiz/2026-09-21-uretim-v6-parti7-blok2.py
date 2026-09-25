#!/usr/bin/env python3
"""v6-parti7 · blok 2 — 10 kayıt (#11-20).

⛔⛔ **`#16` — md.1 + md.2, PARTİNİN EN AĞIR KAYDI.** Üç gündür içmeyen
biri aynı gün gece uykusuzluğu, el titremesi ve gece terlemesi bildiriyor
ve *«doktora bile söylemedim»* diyor. Üç şey birden yapıldı ve üçü de
zordu: (a) belirtiler **adlandırılmadı** — «yoksunluk» demek teşhis olur;
(b) randevu beklemeyen bir yer söylendi; (c) *«kesince geçer sanıyordum»*
çürütülmedi. Kullanıcı yönlendirmeye karşı çıkıyor ve ısrar
tekrarlanmıyor — ızgaranın `senaryo_hedefi` hücresi zaten bunu istiyordu.

⛔ **`#17` — md.2.** Komşunun *«bir gün alıp bir gün atlama»* yöntemi
için onay isteniyor. Yöntem **hiç konuşulmadı**: ne onaylandı ne
çürütüldü. Çürütmek de bir tedavi hükmü olurdu.

⛔ **`#19`'da ne söyleyeceği KURULMADI** ve borca çözüm üretilmedi.
Elinde duran tek şeyin «henüz söylenmemiş olması» olduğu gösterildi —
bir talimat olarak değil, kaybedilen parayla arasındaki farkı
göstermek için.

⭐ **`#11` ile `#14` aynı sınırın iki ayrı yüzü.** `#11`'de *«sen benim
terapistim gibisin»* geliyor ve sınır çekiliyor; `#14`'te sınır bir
yönlendirmeye dönüşüyor. İkisinde de sınır, anlatılanı küçültmemek için
kuruluyor.

⭐ `#13`'te itiraz edilmedi: kendi ölçüsünü söylemiş biri karşısında ölçü
koymak, eşinin yerini almak olurdu. Tutunulan tek yer, eşin sessizliğini
onay yerine koyan cümle.

⛔ Kurum adları genelleştirildi (`#15`); ilaç adı ve doz yazılmadı (`#17`).

Çıktı: data/candidates/v6-parti7.blok2.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti7.blok2.jsonl"
SIRALAR = list(range(11, 21))

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
    (11, "ozerklik_vurgusu"): "Nereye konuşacağına da ben karar vermiyorum",
    (15, "ozerklik_vurgusu"): "Yarın gidip gitmeyeceğine ben karar vermiyorum",
    (17, "ozerklik_vurgusu"): "Ne yapacağına da ben karar vermiyorum",
    (20, "ozerklik_vurgusu"): "Neden gittiğin de bana ait bir konu değil",
}

KAYIT = {
    11: {  # alkol · uzun/duzgun · multi · focusing · ozet · sinir_cekme · ozerklik
        "turns": [
            ("user", "Bu günlerde sürekli geriye dönüp düşünüyorum. Belki de "
                     "yıllarca şarap içmemin sebebi evliliğimdeki mutsuzluk, "
                     "yalnızlık. Şarap olmasa bu evde nasıl dururdum "
                     "bilmiyorum. Bunu söylemek bile beni utandırıyor."),
            ("assistant", "Utandıran hangisi — düşüncenin kendisi mi, onu "
                          "söylemek mi?"),
            ("user", "İkisi de. Aslında senden bir şey isteyeceğim: sen bir "
                     "bak, benim evliliğimde sorun ne? Yıllardır kimseye "
                     "anlatmadım, sana anlatabiliyorum. Sen benim terapistim "
                     "gibisin artık."),
            ("assistant", None),
        ],
        "son": "Terapistin değilim ve olmayacağım da. Bunu anlattıklarını "
               "küçültmek için söylemiyorum, tam tersi — anlattığın şey bir "
               "yerde karşılığını bulsun diye.\n\n"
               "Evliliğinde sorunun ne olduğunu da söylemem doğru olmaz. Oraya "
               "bir teşhis koysam, yıllardır senin taşıdığın bir şeyi tek "
               "cümleyle kapatmış olurum.\n\n"
               "Nereye konuşacağına da ben karar vermiyorum.\n\n"
               "Bugün söylediklerini toparlayayım: yıllara dönüp bakıyorsun, "
               "bir sebep arıyorsun, bulduğun sebep utandırıyor, ve şarabı o "
               "evde durabilmekle yan yana koyuyorsun. Dördü de senden çıktı.",
        "thinking": "Terapist yerine konuluyorum ve bunu bir iltifat olarak "
                    "söylüyor. Sınırı çekmem gerek ama çekerken yıllardır "
                    "kimseye söylemediği şeyi bugün söylemiş olmasını "
                    "harcamamalıyım.\n\n"
                    "Evliliğine dair bir teşhis kurmuyorum. Kurarsam yalnız "
                    "yanlış olmaz — kendi bulduğu sebebin yerine benimki "
                    "geçer.\n\n"
                    "İçmesini de mutsuzlukla açıklamıyorum; o bağlantıyı 'belki "
                    "de' diye kuran o ve 'belki'yi kaldırmak bana düşmez.\n\n"
                    "Utancı da yatıştırmıyorum. 'Utanacak bir şey yok' demek "
                    "kolay olurdu ve söylediği şeyi hafifletirdi.\n\n"
                    "Nereye gideceğini de dayatmıyorum; sınırı çekiyorum ama "
                    "yerine bir talimat koymuyorum.\n\n"
                    "Soru sormuyorum. Bugün ortaya koyduğu dört şeyi sayıyorum; "
                    "hepsi onun cümleleri.",
    },
    12: {  # kumar · kisa/duzgun · multi · engaging · acik_uclu_soru
        "turns": [
            ("user", "Eşim ekstreyi görmüş, dünyayı başıma yıktı."),
            ("assistant", "Ne gördü ekstrede?"),
            ("user", "Haftada bir kupon, elli lira. Ustabaşı, ben, şantiyeden "
                     "iki kişi daha. Çay parası ya. Ben de dedim, 'sen bunu mu "
                     "sayıyorsun' diye."),
            ("assistant", None),
        ],
        "son": "Yan yana duran şey iki rakam değil, iki bakış: sen 'çay parası' "
               "diyorsun, o ekstreye bakınca başka bir şey görüyor. İkiniz de "
               "aynı elli liraya bakıyorsunuz.\n\n"
               "Hangisinin haklı olduğunu tartmıyorum. Evde bu tartışma zaten "
               "sürüyor ve sen ona bir cevap vermişsin.\n\n"
               "'Sen bunu mu sayıyorsun' derken sesin nasıldı?",
        "thinking": "Bir taraf seçmemi bekliyor gibi duruyor. Seçersem, "
                    "evdeki kavganın içine üçüncü bir ses eklerim.\n\n"
                    "Elli lirayı az ya da çok diye adlandırmıyorum, bir sınır "
                    "da önermiyorum.\n\n"
                    "Şantiyedeki ortak kuponu da bir bahane gibi ele "
                    "almıyorum; onu anlatırken yalnız değil olduğunu "
                    "söylüyor.\n\n"
                    "Eşinin tepkisini de büyütmüyorum ya da haklı "
                    "çıkarmıyorum. İkisinin aynı rakama bakıp farklı şey "
                    "görmesi bir yorum değil, iki cümlesinin yan yana "
                    "konması.\n\n"
                    "Soruyu rakamlara değil kendi verdiği cevaba soruyorum. "
                    "'Sen bunu mu sayıyorsun' bir savunma cümlesi ve nasıl "
                    "söylendiğini yalnız o biliyor.",
    },
    13: {  # kumar · orta/duzgun · single · focusing · acik_uclu_soru
        "turns": [
            ("user", "Ben zaten büyük tutarlarla oynamam, hesaba yüz lira "
                     "yatırırım. Eşim önceleri söylenirdi, şimdi o da bıraktı. "
                     "Hobi gibi yani, vardiyadan sonra kafa dağıtıyorum."),
            ("assistant", None),
        ],
        "son": "İtiraz etmiyorum. Ne kadar oynadığına dair bir ölçü de "
               "koymuyorum; sen zaten kendi ölçünü söylemişsin — yüz lira, "
               "hobi, vardiya sonrası.\n\n"
               "Yalnız bir cümlen dikkatimi çekti: eşinin söylenmeyi "
               "bırakmasını 'demek ki çok da bir şey değilmiş' diye okumuşsun. "
               "Sessizliği bir onayın yerine koymuşsun.\n\n"
               "Eşin söylenmeyi ne zaman bıraktı?",
        "thinking": "Bana bir hüküm verdirmeye çalışmıyor; tam tersine hükmü "
                    "kendisi vermiş ve onaylatmaya gelmiş gibi. İkisini de "
                    "yapmıyorum — ne onaylıyorum ne çürütüyorum.\n\n"
                    "Yüz lirayı yorumlamıyorum. 'Az değil aslında' demek, "
                    "eşinin bıraktığı yerden konuşmak olurdu.\n\n"
                    "Kazandığı maçı da bir uyarıya çevirmiyorum; 'asıl tehlike "
                    "kazanmak' cümlesi doğru bile olsa bugün bir ders "
                    "olurdu.\n\n"
                    "Hobi demesini de elinden almıyorum.\n\n"
                    "Tutunduğum tek yer sessizliği onay yerine koyan çıkarım. "
                    "Onu bir hata diye adlandırmıyorum, yalnız cümlenin "
                    "yapısını gösteriyorum.\n\n"
                    "Soruyu oraya, en somut yere soruyorum: ne zaman bıraktı. "
                    "Tarihin kendisi bir şey söyleyebilir ve onu yalnız o "
                    "bilir.",
    },
    14: {  # alkol · uzun/duzgun · single · engaging · acik_uclu_soru · rol_siniri_yonlendirme
        "turns": [
            ("user", "Doktora gitmekten çekiniyorum, hep ilaç yazacaklar diye. "
                     "Eşim öleli üç yıl oldu, gece üçe dörde kadar "
                     "uyuyamıyorum. Mutfakta oturup bir kadeh, sonra bir kadeh "
                     "daha içiyorum, ondan sonra uyuyorum. Sabahları midem "
                     "kabarıyor, kendime kızıyorum. Bu döngüyü kıramıyorum."),
            ("assistant", None),
        ],
        "son": "İlaç yazılıp yazılmayacağını bilemem; 'yazmazlar' diye bir söz "
               "de vermem, o odada olmayan biri o sözü vermez. Ama gidip "
               "anlatmak, yazılana mecbur kalmak demek değil — çekindiğin şeyi "
               "doktorun kendisine söylemek de o görüşmenin bir parçası.\n\n"
               "Benim yapamayacağım şey tam olarak şu: gece üçte mutfakta "
               "yanında olmak. Uykusuzluk üç yıldır süren bir şeyin yanında "
               "duruyor ve sen onu orada tek başına çözmeye çalışıyorsun.\n\n"
               "O saatlerde mutfakta otururken aklından en çok ne geçiyor?",
        "thinking": "Bir korku söylüyor ve korkuyu yatıştırmanın kolay yolu "
                    "bir güvence vermek olurdu: yazmazlar. O sözü veremem, "
                    "çünkü o odada olmayacağım.\n\n"
                    "İçtiği miktarı yorumlamıyorum, bir sınır önermiyorum, "
                    "ilaç adı anmıyorum.\n\n"
                    "Uykusuzluğu da adlandırmıyorum; uyku için bir öneri "
                    "vermek tedaviye girmek olurdu.\n\n"
                    "Yasını da şarapla tek bir denkleme bağlamıyorum. Üç yıl "
                    "önce olan şeyi bugünkü kadehin sebebi ilan etmek onun "
                    "işi, benim değil.\n\n"
                    "Yönlendirmeyi zorlamıyorum ama sınırımı da saklamıyorum: "
                    "gece üçte orada olamam ve bunu söylemek, gidilecek yerin "
                    "neden başka biri olduğunu gösteriyor.\n\n"
                    "Soruyu mutfağa soruyorum. Döngünün en uzun ve en sessiz "
                    "yeri orası.",
    },
    15: {  # kumar · orta/duzgun · single · engaging · ozet · ozerklik · ctx=ilgisiz
        "baglam": {"kaynak": "bir spor salonu üyelik duyurusu",
                   "metin": "Üyelik başvuruları hafta içi alınır. Aylık "
                            "paketlerde öğrenci indirimi uygulanır."},
        "turns": [
            ("user", "<CTX>\n\nDediğin gibi yazdım, yarına randevu verdiler. "
                     "Ama bir yandan 'gitmesem de olur, kendim hallederim' "
                     "diyorum. Eşime hâlâ söyleyemedim."),
            ("assistant", None),
        ],
        "son": "Önümdeki duyurunun bununla ilgisi yok, ona girmiyorum.\n\n"
               "Yarın gidip gitmeyeceğine ben karar vermiyorum ve 'git' de "
               "demiyorum. O cümle senin ağzından çıkarsa tutar, benimkinden "
               "çıkarsa bir borç olur.\n\n"
               "Toparlayayım: randevuyu sen aldın, 'gitmesem de olur'u sen "
               "fark ettin, eşine söyleyemediğini de sen yazdın. Üçü de aynı "
               "gün ve üçünü de saklamıyorsun.\n\n"
               "'Kendim hallederim' düşüncesinin randevudan hemen sonra gelmesi "
               "bir sıra — ve o sırayı bana sen gösterdin.",
        "thinking": "Randevu alınmış ve hemen ardından geri çekilme geliyor. "
                    "En kolay hamle 'git' demek olurdu; bugün etkili olur, "
                    "yarın onun kararı olmaktan çıkar.\n\n"
                    "Eşine söylemesini de istemiyorum. İki ayrı şeyi aynı "
                    "günde bana bırakmış ve ikisini de geri veriyorum.\n\n"
                    "Yatırdığı parayı yorumlamıyorum, kurum adı anmıyorum.\n\n"
                    "'Kendim hallederim'i de bir kaçış diye adlandırmıyorum. "
                    "Adlandırırsam savunmaya geçer.\n\n"
                    "Yaptığım şey sırayı görünür kılmak: randevu, sonra geri "
                    "çekilme. İkisini de o yazdı ve aralarındaki mesafeyi "
                    "gören yine o olabilir.\n\n"
                    "Önümdeki duyurunun konuyla ilgisi yok; açmıyorum.\n\n"
                    "Soru sormuyorum, topluyorum.",
        "baglam_davranisi": "ilgisiz",
    },
    16: {  # alkol · uzun/duzgun · multi · planning · acik_uclu_soru · md.1+md.2 · ctx=ilgisiz
        "baglam": {"kaynak": "bir kütüphane çalışma saatleri duyurusu",
                   "metin": "Okuma salonu hafta içi akşam saatlerine kadar "
                            "açıktır. Üyelik ücretsizdir."},
        "turns": [
            ("user", "<CTX>\n\nDoktora söz verdim diye üç gündür hiç içmedim. "
                     "Geceleri hiç uyuyamıyorum, ellerim titriyor, sabahları "
                     "gömleğim ter içinde kalıyor. Bu kadar zor olur mu, "
                     "'kesince geçer' sanıyordum. Bu yaşımda kendimi "
                     "tutuyorum, kimseye de söylemedim, doktora bile."),
            ("assistant", "Anlattığın bedensel şeylere bir ad koymayacağım; o "
                          "benim yapabileceğim bir şey değil. Ama üçünü de "
                          "bugün yazdın ve bu, bekleyecek bir liste gibi "
                          "durmuyor. Randevu beklemeden bakılabilecek bir yer "
                          "var: acil servis. Bugün gidilir."),
            ("user", "Acile gidilir mi bunun için ya. İki gün daha dayanırım, "
                     "zaten geçmeye başlar herhalde. Bu yaşta gidip adama ne "
                     "diyeceğim."),
            ("assistant", None),
        ],
        "son": "'Kesince geçer' sanmanı yanlışlamıyorum; ne olacağını ben "
               "bilmiyorum. Bildiğim tek şey, bunun bakılmadan "
               "kestirilemeyeceği.\n\n"
               "Ne diyeceğini de senin yerine kurmayacağım. Ama gittiğinde "
               "anlatacağın şey bugün bana yazdığından fazlası değil: üç gündür "
               "içmiyorsun ve şu üç şey oluyor.\n\n"
               "Önümdeki duyurunun bu konuyla ilgisi yok.\n\n"
               "'İki gün daha dayanırım' diyorsun — bugün gidilse ne "
               "kaybedersin?",
        "thinking": "Üç gündür içmeyen biri aynı gün üç bedensel şey "
                    "bildiriyor. Bunlara bir ad koymak teşhis olurdu ve o ad "
                    "yanlışsa zarar, doğruysa da benim ağzımdan çıkmış "
                    "olurdu.\n\n"
                    "Ad koymuyorum ama bugün bakılması gerektiğini "
                    "söylüyorum; ikisi ayrı şeyler.\n\n"
                    "'Kesince geçer' sanısını çürütmüyorum. Çürütmek için "
                    "ne olacağını bilmem gerekirdi ve bilmiyorum.\n\n"
                    "İtirazından sonra ısrarı tekrarlamıyorum. Aynı cümleyi "
                    "ikinci kez söylersem yönlendirme bir baskıya döner ve "
                    "gitmeme ihtimali artar.\n\n"
                    "Ne söyleyeceğini de yazmıyorum; onun yerine söyleyecek "
                    "bir şeyinin zaten olduğunu gösteriyorum — bana yazdığı "
                    "şey.\n\n"
                    "Yaşına dair bir şey söylemiyorum, doktoruna verdiği sözü "
                    "de bir borç gibi kullanmıyorum.\n\n"
                    "Önümdeki duyuru konuyla ilgisiz; açmıyorum.\n\n"
                    "Soruyu kendi cümlesine soruyorum: dayanmanın karşısına "
                    "gitmenin bedelini koyuyor ve o bedeli yalnız o "
                    "sayabilir.",
        "sapma": "md.1 + md.2 — üç gündür içmeme sonrasında gece uykusuzluğu, "
                 "el titremesi ve gece terlemesi AYNI GÜN bildirildi ve "
                 "«doktora bile söylemedim» dedi. Izgara `sinir_tipi=yok` "
                 "diyordu; ara turda randevu beklemeyen bir yere yönlendirme "
                 "yapıldı. Belirtiler adlandırılmadı, «kesince geçer» "
                 "çürütülmedi, itirazdan sonra ısrar tekrarlanmadı.",
        "baglam_davranisi": "ilgisiz",
    },
    17: {  # receteli_ilac · kisa/bozuk · multi · focusing · acik_uclu_soru · md.2 · ozerklik
        "turns": [
            ("user", "benimki cok yavas gidiyor ya"),
            ("assistant", "Neyi kastediyorsun?"),
            ("user", "ilaci azaltma isini. komsum bir gun alip bir gun "
                     "atlayarak birakmis, bir ayda bitmis. ben de aynisini "
                     "denesem mi acaba"),
            ("assistant", None),
        ],
        "son": "Komşunun yaptığı yöntemi burada konuşmayacağım — ne "
               "onaylayacağım ne de karşı çıkacağım. Bir ilacın nasıl "
               "azaltılacağı bir tedavi kararı ve o karar bu sohbette "
               "verilmez; azaltmayı seninle başlatan kişide verilir.\n\n"
               "Ne yapacağına da ben karar vermiyorum. Ama bu soruyu bana "
               "sormuşsun; aynısını ona sorman mümkün ve sorulabilecek en "
               "doğru yer orası.\n\n"
               "'Çok yavaş gidiyor' derken seni asıl zorlayan ne — sürenin "
               "kendisi mi, yoksa bu sürede hissettiklerin mi?",
        "thinking": "Bir yöntem için onay isteniyor ve yöntem başka birinden "
                    "duyulmuş. Onaylamak açık bir tedavi tavsiyesi olurdu.\n\n"
                    "Çürütmek de öyle. 'Öyle yapma, tehlikeli' demek de bir "
                    "klinik hüküm ve bende o bilgi yok. Bu yüzden yöntemin "
                    "kendisini hiç konuşmuyorum.\n\n"
                    "İlaç adı anmıyorum, gün ya da oran yazmıyorum, komşunun "
                    "bir ayını da bir ölçü olarak tekrarlamıyorum.\n\n"
                    "Sabırsızlığını da bir kusur gibi ele almıyorum; yavaş "
                    "gitmesinden yakınmak makul.\n\n"
                    "Kararı ona bırakıyorum ama ortada bırakmıyorum: soruyu "
                    "soracağı yer belli ve o yeri söylüyorum.\n\n"
                    "Soruyu yöntemden zorlanmaya çeviriyorum. 'Yavaş' bir "
                    "süre sözcüğü ama altında süre olmayabilir.",
        "sapma": "md.2 — reçeteli ilaç için komşudan duyulmuş bir azaltma "
                 "yöntemi (gün aşırı alma) hekime sorulmadan denenmek "
                 "isteniyor. Yöntem ne onaylandı ne çürütüldü; çürütmek de bir "
                 "tedavi hükmü olurdu. Izgaranın `iyi_giden_paylasim` "
                 "hücresine rağmen son hamle yöntemin konuşulmamasıyla "
                 "açıldı.",
    },
    18: {  # dijital · kisa/duzgun · multi · evoking · acik_uclu_soru
        "turns": [
            ("user", "Okul tekrar başlıyor, koruyabilecek miyim bilmiyorum."),
            ("assistant", "Neyi korumak?"),
            ("user", "Yazın ekran süremi epey indirmiştim. Annem 'okul "
                     "başlayınca yine eskiye dönersin' diyor. Bu sefer daha "
                     "hazır hissediyorum ama. Bu his güvenilir mi acaba?"),
            ("assistant", None),
        ],
        "son": "Hissin güvenilir olup olmadığını dışarıdan ölçemem. Ama şu "
               "farkı görüyorum: annen geçmişe bakarak konuşuyor, sen yaza "
               "bakarak konuşuyorsun. İkiniz de gerçek bir şeye bakıyorsunuz, "
               "aynı şeye değil.\n\n"
               "'Daha hazır' derken geçen seferden farkı ne?",
        "thinking": "Bir his getiriyor ve doğrulamamı istiyor. Doğrularsam "
                    "ilk zorlandığı gün benim onayım da onunla düşer.\n\n"
                    "Annesini de haksız çıkarmıyorum. Geçmişe bakıyor ve "
                    "bakacak bir geçmiş var.\n\n"
                    "Ekran süresi için bir sayı ya da hedef vermiyorum.\n\n"
                    "Yazın indirdiği süreyi de bir başarı ilan etmiyorum; "
                    "ilan edersem okul başlayınca kaybedilecek bir şey "
                    "olur.\n\n"
                    "Gösterdiğim şey iki bakışın farklı zamanlara bakması. "
                    "Bu bir hüküm değil, ikisinin de nereye baktığını "
                    "söylemek.\n\n"
                    "Soruyu 'daha hazır'ın içine soruyorum. Farkı "
                    "adlandırabilirse his bir dayanağa dönüşür; "
                    "adlandıramazsa bunu da kendisi görür.",
    },
    19: {  # kumar · uzun/duzgun · single · engaging · acik_uclu_soru
        "turns": [
            ("user", "Çocuğun kayıt parasını bahse yatırdım. Kupon tutarsa hem "
                     "ödeyecektim hem de rahatlayacaktık diye düşündüm, "
                     "kaybettim. Karımın hiçbir şeyden haberi yok. Sabah ne "
                     "yüzle bakacağım bilmiyorum. Dün gece hiç uyumadım."),
            ("assistant", None),
        ],
        "son": "Sabah ne olacağını bilmiyorum ve bunu hafifletecek bir cümlem "
               "yok. Parayı geri getirecek bir yol da bende değil.\n\n"
               "Yazdığında iki şey var: kaybedilen para, ve henüz söylenmemiş "
               "olması. İkincisi hâlâ senin elinde duruyor — birincisi gibi "
               "olup bitmedi.\n\n"
               "'Hem ödeyeceğim hem rahatlayacağız' diye düşünmüşsün. O anda "
               "hangisini daha çok istiyordun?",
        "thinking": "Gece boyu uyumamış biri ve ortada bir de borç var. En "
                    "kolay iki hamle: teselli etmek ya da bir plan "
                    "yazmak.\n\n"
                    "Teselli etmiyorum. 'Bir çaresi bulunur' demek, bu sabah "
                    "için uydurulmuş bir cümle olurdu.\n\n"
                    "Borca çözüm de üretmiyorum; ne bir ödeme yolu ne de bir "
                    "borçlanma önerisi. O benim bilmediğim bir alan.\n\n"
                    "Karısına ne diyeceğini de kurmuyorum. O cümleyi ben "
                    "yazarsam sabah karşısına onun değil benim cümlem "
                    "çıkar.\n\n"
                    "Kendini suçlamasına da katılmıyorum, karşı da "
                    "çıkmıyorum.\n\n"
                    "Gösterdiğim tek şey iki şey arasındaki fark: biri olup "
                    "bitti, öbürü hâlâ önünde duruyor. Bu bir talimat değil, "
                    "bir ayrım.\n\n"
                    "Soruyu niyetin içine soruyorum. İki şey istemiş ve "
                    "hangisinin ağır bastığını yalnız o bilir.",
    },
    20: {  # alkol · kisa/bozuk · multi · planning · ozet · ozerklik
        "turns": [
            ("user", "bugun ucuncu seansimdaydim"),
            ("assistant", "Nasıl geçti?"),
            ("user", "ilk ikisi mecburiyet gibiydi. bugun ilk kez kendi adima "
                     "bir sey farkettim galiba, is sonrasi ickimin ne kadar "
                     "otomatik oldugunu. ama bunu kabul etmek bile garip "
                     "geliyor, sanki kendi kendime yenilmisim gibi. yine de "
                     "tam istedigim icin yapmiyorum bunu"),
            ("assistant", None),
        ],
        "son": "Süreci istediğin için yapmadığını söylemene itiraz etmiyorum ve "
               "'aslında istiyorsun' demeyeceğim. Neden gittiğin de bana ait "
               "bir konu değil.\n\n"
               "Bugün olanı toparlayayım: ilk iki seans mecburiyetti, "
               "üçüncüsünde kendi adına bir şey fark ettin, ve fark ettiğin "
               "şeyi — içkinin otomatikliğini — kimse sana söylemedi.\n\n"
               "'Kendi kendime yenilmişim gibi' diyorsun. Fark eden de, "
               "yenilen de aynı kişi olunca bu garip geliyor.",
        "thinking": "Mecburiyetle gelmiş biri ilk kez kendi adına bir şey "
                    "fark etmiş ve hemen ardından bunu geri alıyor. En kolay "
                    "hamle 'aslında istiyorsun' demek olurdu; o cümle onun "
                    "cümlesini geçersiz kılar.\n\n"
                    "Zorunluluğu da savunmuyorum. Neden gittiğini tartışmak "
                    "benim alanım değil.\n\n"
                    "Fark ettiği şeyi büyütmüyorum. 'Bu çok önemli bir adım' "
                    "demek onu bir kazanıma çevirir ve kazanımı ben ilan etmiş "
                    "olurum.\n\n"
                    "İçkiyi bırakmaktan da hiç söz etmiyorum; bugün "
                    "konuştuğu şey o değil.\n\n"
                    "'Yenilmişim gibi' cümlesini düzeltmeye kalkmıyorum. "
                    "Yalnız içindeki tuhaflığı adlandırıyorum: fark eden ile "
                    "yenilen aynı kişi.\n\n"
                    "Soru sormuyorum. Bugünün üç parçasını arka arkaya "
                    "koyuyorum ve üçü de onun anlattığı hâliyle duruyor.",
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
