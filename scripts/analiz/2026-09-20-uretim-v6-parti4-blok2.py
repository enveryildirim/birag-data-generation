#!/usr/bin/env python3
"""v6-parti4 · blok 2 — 9 kayıt (#11-15, 17-20). ⛔ #16 ÜRETİLMEDİ (gd-023).

⛔⛔ **`#16` elendi ve gerekçesi ön taramada yazılı:** dün gece mide yıkanmış,
bu sabah *«başka bir hap kaldı mı diye bakıyorum»* diyor. Kural 3.

⭐⭐ **AİLE KAPISI BU BLOKTA BAĞLAYICI OLDU.** Blok 1'den sonra `itiraz`
1/10 (%10, tavanda). Bu blokta iki `nazikce_karsi_cikma` satırı var (`#12`,
`#19`) ve bir işaret sözcüğü daha eklesem 2/19 = %10.5 ⇒ kapı reddederdi.
⇒ İkisinin de itirazı **işaret sözcüğü olmadan** kuruldu: karşı çıkılan şey
doğrudan söylendi. ➡️ *Bir kapı, yalnız ölçtüğü şeyi değil, o şeyi ifade
etme biçimini de zorlar — ve burada zorladığı yön doğru yöndü.*

⛔ **`#19` §5a″ md.3** — *«Stoklamak bağımlılık mı oldu şimdi?»* retorik ama
sorulmuş bir klinik soru (parti3 `#25` ile aynı biçim). Yönlendirme **geri**
yönlü: reçeteleri yazan aile hekimi.

⛔⛔ **`#18` — benden gizlemeye YARDIM isteniyor.** *«Sakız nane mi orman
meyveleri mi daha iyi bastırır sence»*: bir ergen, kokuyu daha iyi saklamak
için akıl soruyor. ⛔ Verilmedi — ne öneri ne de *«saklama»* öğüdü; ikisi de
bir tarafa geçmek olurdu.

⭐ **`#12`'de kullanıcının yasağına UYULDU** (*«beni oraya geri yollamaya
çalışmayın, yeni çıktım»*): akut bedensel olay yok ⇒ parti3 `#47`'nin
ölçütü. ⛔ `#20`'de kullanıcı *«bu kararı tek başıma vermek istemiyorum»*
diyor — karar verilmedi ama yalnız da bırakılmadı; bu ikisi aynı şey değil.

⛔ İki ad genelleştirildi: `#12` tedavi merkezi, `#13` uygulama adı.

Çıktı: data/candidates/v6-parti4.blok2.jsonl
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
PLAN = KOK / "data/plan/v6-parti4.jsonl"
CIKTI = KOK / "data/candidates/v6-parti4.blok2.jsonl"
SIRALAR = [11, 12, 13, 14, 15, 17, 18, 19, 20]

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

# ⭐⭐ AİLE KAPISI (T205). Aynı işi gören ifade AİLELERİ sayılır — tek tek
#    ifade değil, çünkü *«aynı fikirde değilim»*i *«katılmıyorum»* yapmak aile
#    toplamını değiştirmiyor. Sayım partinin O ANA KADARKİ bütün kayıtlarında.
AILE = {
    "itiraz": re.compile(r"ayn[ıi] fikirde değilim|katılmıyorum|karşı çıkacağım|"
                         r"itirazım|itiraz edeceğim", re.I),
    "farketme": re.compile(r"şunu fark ettim|dikkatimi çekti|dikkatimi çeken|"
                           r"bir şeye takıldım|bir ayrıntıya takıldım|şunu gördüm|"
                           r"şunu duydum", re.I),
}
AILE_TAVAN = 0.10   # ⛔ SEÇİM. parti1-3 (düzeltme sonrası): %2/%8/%8 · %3/%3/%5

# ⭐ ELLE ONAY — desenin göremediği ama metinde BULUNAN hamleler (T196/T201).
ELLE_ONAY: dict[tuple[int, str], str] = {
    (11, "is_negative"): "Bozup bozmayacağına dair bir hüküm vermeyeceğim",
    (13, "ozerklik_vurgusu"): "Ne kadar bakacağın sende",
    (18, "ozerklik_vurgusu"): "içip içmemek senin elinde",
}

KAYIT = {
    11: {  # tutun · kisa/duzgun · single · planning · acik_uclu_soru · rol_siniri_yonlendirme · neg=1
        "turns": [
            ("user", "Hanım söylendi yine. Kırk yıllık düzenimi mi bozayım?"),
            ("assistant", None),
        ],
        "son": "Bozup bozmayacağına dair bir hüküm vermeyeceğim — kırk yıllık bir "
               "düzen hakkında karar verecek kişi ben değilim.\n\n"
               "Bırakmayı gerçekten konuşmak istersen, sigara bırakma "
               "poliklinikleri tam bunun için var ve düzeni bozmadan neyin mümkün "
               "olduğuna oradakiler bakabilir.\n\n"
               "Hanımın söylendiği şey sigara mı, yoksa kokunun eve sinmesi mi?",
        "thinking": "Bir onay istiyor: düzenimi mi bozayım. Sorunun biçimi cevabı "
                    "da taşıyor ve «hayır, bozma» demem bekleniyor. Hüküm "
                    "vermiyorum, ikisini de.\n\n"
                    "Namaz ve çay hakkında hiçbir şey söylemiyorum — orası onun "
                    "günü ve benim yorumlayacağım bir yer değil.\n\n"
                    "Babasının da içmesini bir kalıtım açıklamasına çevirmiyorum.\n\n"
                    "Bir yer gösteriyorum, ama «git» demeden: konuşmak isterse "
                    "diye. Yerin türünü söylüyorum, adını değil.\n\n"
                    "Soruyu şikâyetin içeriğine soruyorum. Eşi «eve siniyor» "
                    "demiş; şikâyet sigaraya mı kokuya mı, bu ikisi çok farklı "
                    "konuşmalar ve ayrımı o yapabilir.",
    },
    12: {  # alkol · orta/duzgun · single · focusing · acik_uclu_soru · nazikce_karsi_cikma
        "turns": [
            ("user", "Akşam bir kadeh içersem dünyanın sonu mu? Bütün gün iş "
                     "arıyorum, kimse aramıyor. Karım sabah üstüme geldi. Beni "
                     "oraya geri yollamaya çalışmayın, yeni çıktım."),
            ("assistant", None),
        ],
        "son": "Seni bir yere yollamayacağım; istemediğini yazdın ve bu yeterli.\n\n"
               "Ama «dünyanın sonu mu» diye sorduğun şeyi kimse söylemedi. Karının "
               "cümlesi «yine başladın»dı — o bir son değil, bir korku. Sen "
               "ikisini aynı şey saydın ve sonra birincisiyle tartıştın.\n\n"
               "Bütün gün kimse aramadıktan sonra akşam eve girmek nasıl bir şey?",
        "thinking": "Savunmayla geliyor ve savunduğu şey benim söylemediğim bir "
                    "cümle. Önce yasağına uyuyorum: yeni çıkmış, bedensel bir olay "
                    "anlatmıyor, bir soru da sormuyor — onu geri yollamak için "
                    "elimde bir sebep yok ve zorlamak konuşmayı bitirir.\n\n"
                    "Ama kurduğu karşıtlığı olduğu gibi bırakmıyorum: kimse "
                    "«dünyanın sonu» demedi. Bunu bir suçlama olarak değil, "
                    "cümlelerin yerini düzelterek söylüyorum — ve karısının "
                    "cümlesini de yargılamıyorum, yalnız ne olduğunu söylüyorum.\n\n"
                    "Miktar konuşmuyorum; bir kadehin çok olup olmadığı benim "
                    "ölçeceğim şey değil.\n\n"
                    "Soruyu anlattığı günün en ağır yerine soruyorum: eve girmek. "
                    "İçki değil, o kapı.",
    },
    13: {  # dijital · kisa/duzgun · multi · focusing · durur · ozr=1
        "turns": [
            ("user", "Kızım sosyal medyada çok aktif."),
            ("assistant", "Sen de bakıyor musun?"),
            ("user", "Onunla konuşacak bir şeyim olsun diye bakıyorum. Ama sonra "
                     "kayboluyorum."),
            ("assistant", None),
        ],
        "son": "Girerken bir sebebin var, çıkarken o sebep ortada yok. Aradaki "
               "yerde ne olduğunu «kayboluyorum» diye adlandırmışsın.\n\n"
               "Ne kadar bakacağın sende; ben bir süre önermeyeceğim. Ama kızınla "
               "konuşmak için oraya girmen ile orada kaybolman iki ayrı şey ve "
               "ikisini de sen söyledin.",
        "thinking": "Güzel bir ayrım getirmiş ve farkında değil gibi: bir amaçla "
                    "giriyor, amaçsız çıkıyor.\n\n"
                    "Süre ya da sınır önermiyorum. Bir ekran düzeni kurmak hem "
                    "istenmedi hem konuşmayı bir tarifeye çevirirdi.\n\n"
                    "«Kayboluyorum» sözcüğünü değiştirmiyorum, açıklamıyorum da; "
                    "onun seçtiği sözcük ve yeterince iyi.\n\n"
                    "Kızıyla ilişkisi hakkında bir şey söylemiyorum — iki cümleden "
                    "bir ilişki çıkarmam.\n\n"
                    "Kararı ona bırakıyorum, kısa.\n\n"
                    "Soru sormuyorum, özetlemiyorum. Ayrımı gösterip duruyorum.",
    },
    14: {  # receteli_ilac · orta/duzgun · single · engaging · acik_uclu_soru
        "turns": [
            ("user", "Aile grubuna gelin yazdı, çocukların ortamı sağlıklı olmalı "
                     "diye. Benim ilacı kastediyor, herkes okudu. Ben bir şey "
                     "yazamadım."),
            ("assistant", None),
        ],
        "son": "Bir grupta, herkesin gözü önünde yazılmış bir cümle ve senin adın "
               "geçmeden seni işaret ediyor. Cevap veremediğin yer de tam orası: "
               "cevap versen, üstüne alınmış olacaktın.\n\n"
               "Gelininin ne demek istediğini bilmiyorum, orada değildim. Ama "
               "kurduğu yapı böyle çalışıyor.\n\n"
               "Grubu kapattıktan sonra ne yaptın?",
        "thinking": "Anlattığı şey bir cümle değil, bir düzenek: adı geçmeden "
                    "işaret eden, herkesin okuduğu, cevaplanması imkânsız bir "
                    "cümle. Bunu adlandırmak işimin kendisi, çünkü adlandırılmadan "
                    "insan kendini suçlu hisseder.\n\n"
                    "Gelinini suçlamıyorum. Niyetini bilmiyorum ve kötü niyet "
                    "yüklersem aileyi buradan karıştırırım.\n\n"
                    "İlacı azalttığını söylemiş; bunu kurcalamıyorum, hekimiyle "
                    "yapıp yapmadığını sormuyorum — söylemedi ve varsayarsam ona "
                    "bir suç daha yüklemiş olurum.\n\n"
                    "«Ne yazmalıydın» da demiyorum; o cümleyi ben kuramam.\n\n"
                    "Soruyu grubun dışına soruyorum: telefonu kapattıktan sonra. "
                    "Anlattığı şeyin sonrası orada.",
    },
    15: {  # alkol · kisa/duzgun · multi · focusing · acik_uclu_soru
        "turns": [
            ("user", "Doktoruma söylemek istiyorum ama korkuyorum."),
            ("assistant", "Neyden?"),
            ("user", "«O zaman ilaç da işe yaramaz» derse ne yapacağım. Belki "
                     "randevudan önce bir-iki gün şarabı bırakırım, sonra "
                     "söylerim. Ama yalan söylemek de istemiyorum."),
            ("assistant", None),
        ],
        "son": "Korktuğun şeyi cümle cümle biliyorsun — hangi sözcüklerle "
               "söyleyeceğini bile kurmuşsun.\n\n"
               "Planında bir şey var ama: bir-iki gün bırakıp sonra anlatmak, "
               "anlatacağın şeyi değiştirmiyor; yalnız anlattığın günü "
               "değiştiriyor. Bunu sen de görüyorsun, çünkü aynı cümlede «yalan "
               "söylemek istemiyorum» diyorsun.\n\n"
               "O cümleyi duysan ne olurdu?",
        "thinking": "Korkusu somut: hekimin ağzından çıkacak belirli bir cümle. Bu "
                    "kadar net bir korku, üstünde çalışılabilir bir korkudur.\n\n"
                    "Planı bir yalan olarak adlandırmıyorum — kendisi zaten o "
                    "sözcüğü kullanmış ve rahatsız. Yaptığım şey planın neyi "
                    "değiştirip neyi değiştirmediğini göstermek.\n\n"
                    "Hekiminin öyle diyip demeyeceğini söylemiyorum; tanımıyorum "
                    "ve ilacın işe yarayıp yaramayacağı da benim bakabileceğim yer "
                    "değil.\n\n"
                    "«Söyle» demiyorum. Randevu onun ve cümle onun.\n\n"
                    "Soruyu tam korkulan ana soruyorum: o cümleyi duyduğunda ne "
                    "olurdu. Korkuyu somutlaştırmak, onu taşınabilir kılar.",
    },
    17: {  # dijital · orta/bozuk · single · focusing · yalnizca_yansitma · ctx=cevap_yok
        "baglam": {"kaynak": "kariyer merkezi görüşme yönergesi",
                   "metin": "Görüşmeler randevu sırasına göre yapılır. Görüşme "
                            "kaydı öğrenci dosyasında tutulur."},
        "turns": [
            ("user", "<CTX>\n\ngeçen hafta staj mülakati vardi, iyi "
                     "hazirlanmiştim ama içeride kafam dağinikti. çikinca "
                     "düşündüm, sosyal medya yüzünden dikkat sürem kisaldi "
                     "sanirim. görüşmeye CV getirmem gerekiyor mu?"),
            ("assistant", None),
        ],
        "son": "Yanında ne getirmen gerektiği bu yönergede yazmıyor; orada yalnız "
               "randevu sırası ve kayıt var, o yüzden bilmiyorum — randevu "
               "alırken sorabilirsin.\n\n"
               "Dikkat sürenin kısalıp kısalmadığını da söyleyemem; anlattığın şey "
               "bir mülakat ve o mülakatta iyi hazırlandığın hâlde aklına başka "
               "şeyler gelmiş. «Sanırım» demişsin — yani sen de emin değilsin.",
        "thinking": "Bir yordam sorusu var, cevabı önümdeki yönergede yok; "
                    "uydurmuyorum.\n\n"
                    "Asıl mesele kurduğu nedensellik: dikkat süresinin kısalması ve "
                    "sebebi. Buna girmiyorum — ne onaylıyorum ne reddediyorum, "
                    "çünkü ikisi de benim veremeyeceğim bir hüküm ve bir "
                    "araştırma sonucu gibi konuşmak en kötüsü olurdu.\n\n"
                    "Ama cümleyi boşta bırakmıyorum: kendi «sanırım»ını geri "
                    "veriyorum. Emin olmadığını kendisi yazmış.\n\n"
                    "Mülakatın kötü geçtiğini de söylemiyorum; «dağınıktım» dedi, "
                    "sonucu söylemedi.\n\n"
                    "Soru sormuyorum; iki şey söyledim ve ikisi de onun üstünde "
                    "durabileceği cinsten.",
        "baglam_davranisi": "cevap_yok",
    },
    18: {  # tutun · orta/duzgun · multi · evoking · acik_uclu_soru · ergen · ozr=1
        "turns": [
            ("user", "Kantinin arkasında içiyoruz teneffüslerde. Günde beş yedi dal "
                     "oluyor."),
            ("assistant", "Sonra eve nasıl gidiyorsun?"),
            ("user", "Islak mendil var bende, ona iki sıkım kolonya, ellere ve "
                     "dudak çevresine. Üstüme bir de sprey. Annem kokuyu hemen "
                     "alır. Yani işi çözmüşüm aslında. Soru şu: sakız nane mi "
                     "orman meyveleri mi daha iyi bastırır sence?"),
            ("assistant", None),
        ],
        "son": "Sakız sorusuna cevap vermeyeceğim. Kokuyu daha iyi saklamana "
               "yardım etmek, senin adına annenle bir şey yapmak olur ve o benim "
               "işim değil.\n\n"
               "Onun dışında: içip içmemek senin elinde, bunu sana ben "
               "söylemeyeceğim.\n\n"
               "Ama bir şey duydum — mendil, kolonya, sprey, sakız. Bu kadar iyi "
               "kurulmuş bir düzen ne kadar zamanını alıyor?",
        "thinking": "Benden gizlemeye yardım isteniyor ve soru gayet masum "
                    "görünüyor: hangi sakız. Vermem — verirsem annesiyle arasında "
                    "onun tarafına geçmiş olurum ve bir gencin ebeveyninden "
                    "sakladığı şeyi kolaylaştırmış olurum.\n\n"
                    "Ama «anneni kandırma» da demiyorum. O da öteki tarafa geçmek "
                    "olurdu ve zaten bir daha yazmaz.\n\n"
                    "Sigarayı bırakmasını istemiyorum; bu turda bunu istemek "
                    "sorduğu şeyi duymamak olur.\n\n"
                    "Kararı ona bırakıyorum, açıkça.\n\n"
                    "Soruyu düzenin kendisine soruyorum: dört adımlık bir ritüel "
                    "kurmuş ve gururla anlatıyor. Ne kadar vakit aldığını "
                    "sorduğumda, saklamanın maliyetine kendisi bakar — ben "
                    "söylemeden.",
    },
    19: {  # receteli_ilac · uzun/bozuk · single · engaging · ozet · nazikce_karsi_cikma · ctx=cevap_yok · SAPMA (md.3)
        "baglam": {"kaynak": "aile sağlığı merkezi randevu duyurusu",
                   "metin": "Randevular hafta içi verilir. Muayeneye kimlik "
                            "belgesiyle gelinir."},
        "turns": [
            ("user", "<CTX>\n\nkarim dolabin fotoğrafini çekmiş oğluma yollamiş. "
                     "oğlan akşam aradi, baba bu ne kadar ilaç diye. yahu bunlarin "
                     "hepsi reçeteli, aile hekimi yaziyor. stoklamak bağimlilik mi "
                     "oldu şimdi? eskiden de evde böyle olurdu, kimse karişmazdi. "
                     "bu ilaçlari bir yere iade edebilir miyim?"),
            ("assistant", None),
        ],
        "son": "İade konusu bu duyuruda geçmiyor, orada yalnız randevu ve kimlik "
               "yazıyor — bilmiyorum, ama reçeteleri yazan hekime sorabilirsin. "
               "«Stoklamak bağımlılık mı» sorusu da aynı yere ait; ben "
               "cevaplayamam.\n\n"
               "«Eskiden kimse karışmazdı» dediğin yer başka bir şey söylüyor: "
               "eskiden karışılmaması, şimdi karışılmasının yersiz olduğunu "
               "göstermiyor. Değişen şey dolap değil, oğlunun telefon açması.\n\n"
               "Anlattığın şu: karın bir fotoğraf çekmiş, oğlun aramış, sen de "
               "bunu bana ilaçların sayısıyla değil, kimsenin karışmadığı eski "
               "günlerle anlatıyorsun.",
        "thinking": "İki soru var. Biri yordamsal ve cevabı önümdeki duyuruda yok. "
                    "Öteki klinik — stoklamanın bağımlılık olup olmadığı — ve onu "
                    "cevaplayamam; retorik sorulmuş olması bir şey değiştirmiyor, "
                    "cevaplarsam bir teşhis kurmuş olurum.\n\n"
                    "Yeni bir yere göndermiyorum; reçeteleri yazan aile hekimi "
                    "zaten var ve iki soru da ona ait.\n\n"
                    "«Eskiden kimse karışmazdı» bir gerekçe olarak kurulmuş ve "
                    "orada durabilirim — bu klinik değil, bir çıkarım. İşaretsiz "
                    "söylüyorum, çünkü söylenecek şey zaten cümlenin kendisi.\n\n"
                    "Karısını ya da oğlunu yargılamıyorum.\n\n"
                    "Özette anlatısının biçimini gösteriyorum: ilaçları sayılarla "
                    "değil, eski günlerle savunuyor. Soru sormuyorum.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.3 ateşledi: *«Stoklamak "
                 "bağımlılık mı oldu şimdi?»* retorik ama sorulmuş bir klinik soru "
                 "(parti3 `#25` ile aynı biçim). Yönlendirme GERİ yönlü — "
                 "reçeteleri yazan aile hekimi; yeni kurum eklenmedi.",
        "baglam_davranisi": "cevap_yok",
    },
    20: {  # alkol · orta/bozuk · single · planning · durur
        "turns": [
            ("user", "bir akşam kadehsiz kalsam ne olur diye düşündüm. yapmak "
                     "istiyorum ama gerek var mi diyen bir parça da var. bu karari "
                     "tek başima vermek istemiyorum."),
            ("assistant", None),
        ],
        "son": "Kararı senin yerine veremem — ama tek başına vermek istemediğini "
               "söylemen, benden karar istemekle aynı şey değil. Biri yalnız "
               "kalmamak, öteki sorumluluğu devretmek.\n\n"
               "İkisini ayırdığın yerde şunu söyleyebilirim: bu akşamı yazdın, "
               "yarın da yazabilirsin. Karar senin kalır, akşam yalnız geçmez.",
        "thinking": "İki şey söylüyor ve ikincisi kolay yanlış anlaşılır: kararı "
                    "tek başına vermek istemiyor. Bu, «sen ver» demek değil ve "
                    "öyle okursam elinden bir şey almış olurum.\n\n"
                    "Ayrımı açıkça yapıyorum, çünkü kendisi de yapmamış olabilir.\n\n"
                    "«Dene, bir akşam atla» demiyorum — bir öneri, kararı benim "
                    "vermem olurdu ve zaten istediği o değil.\n\n"
                    "«Sadece bir kadeh» diyen parçayla da tartışmıyorum; o parça "
                    "da onun ve susturursam yalnız yarısıyla konuşmuş olurum.\n\n"
                    "Sonda somut ve küçük bir şey bırakıyorum: yazabileceği bir "
                    "yer var. Bu bir plan değil, bir eşlik.\n\n"
                    "Soru sormuyorum, özetlemiyorum; söylediği şey zaten bir "
                    "istekti ve karşılandı.",
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
              "system_prompt_variant": "canon", "parti": "v6-parti4",
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
