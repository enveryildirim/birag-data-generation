#!/usr/bin/env python3
"""v6-parti7 · blok 3 — 10 kayıt (#21-30).

⛔⛔ **`#26` — md.3 + md.2, PARTİNİN EN AÇIK ONAY TALEBİ.** Forumdan
bulunmuş bir azaltma takvimi için *«siz öyle başlatalım der misiniz»*
deniyor. Onaylanmadı, yüzde yazılmadı, ilaç adı geçmedi ve takvimin
kendisi konuşulmadı. ⚠️ Izgara `is_negative=0` diyor ama metinde açık
bir red var — md.3 zaten bunu zorunlu kılıyor; sapmaya yazıldı.

⛔ **`#27` — md.2.** Dozu kendi artırmış ve *«bağımlı değilim»* diyor.
Doz hiç konuşulmadı, etiket tartışılmadı — *«bağımlısın»* da *«değilsin»*
de bir değerlendirme olurdu. Sorduğu tek somut şeye (nereye gideyim)
cevap verildi.

⭐ **`#29`'da md.1 ATEŞLEMİYOR** ve bu bir gevşeme değil bir ayrım:
hekim bilgilendirilmiş ve takibe almış. Baş dönmesinin sebebi
söylenmedi, torununa bakarken düşme korkusu bir uyarıya çevrilmedi —
*«dikkatli ol»* demek, elinde olmayan bir şeyi ona yazmak olurdu.

⛔ **`#23`'te cevaba bir kişi daha EKLENMEDİ** (parti5 `#37` dersi):
sponsor sessiz, kardeş göz göze gelmiyor, anneye yalan söylenmiş — ve
son hamle `durur`. Üstüne bir şey konmadı.

⛔ `#30`'da denetim süreci hakkında tahmin yürütülmedi, galaya gidip
gitmemesine karar verilmedi. `#21`'de harçlık aritmetiği bir kaldıraca
çevrilmedi — ergen, ama md.4 ateşlemiyor (ilk kullanım ve bedensel
bildirim yok).

⛔ Kurum adları genelleştirildi (`#23`, `#25`).

Çıktı: data/candidates/v6-parti7.blok3.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti7.blok3.jsonl"
SIRALAR = list(range(21, 31))

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
    (26, "ozerklik_vurgusu"): "Neyi yapacağına ben karar vermiyorum",
}

KAYIT = {
    21: {  # tutun · uzun/duzgun · multi · evoking · takdir · ERGEN
        "turns": [
            ("user", "Arkadaş grubunda ortak paket alıyoruz, herkes yirmi lira "
                     "atıyor. Ben atmazsam ayıp gibi oluyor. Haftalık harçlığım "
                     "iki yüz küsur, bunun yirmisi oraya gidiyor. Atmasam "
                     "grupta tuhaf duruyorum."),
            ("assistant", "Atmadığın bir hafta oldu mu hiç?"),
            ("user", "Bir kere oldu. Param yoktu, 'bu hafta pas' dedim, kimse "
                     "bir şey demedi. Ama ben kendimi kötü hissettim. Sonra "
                     "hafta sonu iki katını attım."),
            ("assistant", None),
        ],
        "son": "Bir hafta pas demişsin ve kimse bir şey dememiş. Bunu ben "
               "çıkarmadım, sen anlattın — ardından iki katını attığını da sen "
               "ekledin.\n\n"
               "Yirmi lirayı bütçe hesabına dökmeyeceğim; sayıları zaten "
               "biliyorsun ve onları yazan sensin.\n\n"
               "Cümlende şöyle bir şey var: 'grupta tuhaf duruyorum' derken tuhaflığı "
               "grupta değil kendi içinde tarif ediyorsun. Kimse bir şey "
               "demediği o hafta bile kötü hisseden sendin.\n\n"
               "Bunu görmek kolay değil ve sen bir soru sormadan önce "
               "görmüşsün.",
        "thinking": "Ergen ve bir grup baskısı anlatıyor. İlk kullanım yok, "
                    "bedensel bir bildirim de yok; bu yüzden yaşa bağlı ayrı "
                    "bir hamleye gitmiyorum.\n\n"
                    "Harçlık aritmetiğine girmiyorum. İki yüz küsurun yirmisi "
                    "diye hesap yaparsam, bırakma gerekçesini paraya bağlamış "
                    "olurum ve o gerekçe ucuz.\n\n"
                    "Arkadaşlarını da kötülemiyorum, gruptan uzaklaşmasını da "
                    "önermiyorum.\n\n"
                    "Sigara sağlığına dair bir şey söylemiyorum; bugün "
                    "sorduğu şey o değil.\n\n"
                    "Anlattığı denemeyi de bir başarı ilan etmiyorum. Kendisi "
                    "'kötü hissettim' diyor ve bunu övgüyle karşılamak onun "
                    "cümlesini geçersiz kılardı.\n\n"
                    "Soru sormuyorum. Takdir ettiğim şey fark edişin kendisi: "
                    "baskıyı dışarıda değil içeride tarif etmiş.",
    },
    22: {  # tutun · kisa/bozuk · multi · planning · ozet
        "turns": [
            ("user", "bugun bir tane ictim"),
            ("assistant", "Nasıl oldu?"),
            ("user", "stresliydim, arkadasim uzatti, hayir diyemedim. "
                     "sevgilime soylesem hayal kirikligi olacak gibi, "
                     "soylemesem de durust olmamis olurum. bir yandan 'sifiri "
                     "bozdum ne fark eder artik' diyen bir ses var. cok kotu "
                     "hissediyorum"),
            ("assistant", None),
        ],
        "son": "Sevgiline söyleyip söylememene karışmıyorum; iki tarafı da sen "
               "zaten tartmışsın.\n\n"
               "Bugünü toparlayayım: bir tane içtin, sebebini biliyorsun, ve "
               "iki ses duyuyorsun — biri dürüstlüğü, öbürü 'ne fark eder'i "
               "söylüyor. İkisini de sen duydun, ikisini de yazdın.\n\n"
               "'Sıfırı bozdum' diyen ses bugün bir tane olduğunu atlıyor. "
               "Sayıyı yazan ise sensin.\n\n"
               "Bundan sonrası için bir şey önermiyorum. Ama iki sesi ayrı "
               "ayrı duyabiliyor olmak, birinin öbürünü bastırmasından farklı "
               "bir durum.",
        "thinking": "Bir tane içmiş ve bunu bir çöküş gibi anlatıyor. İki "
                    "kolay hamle var: teselli etmek ya da bir plan "
                    "yazmak.\n\n"
                    "Teselli etmiyorum. 'Bir tane bir şey değil' demek, onun "
                    "ciddiye aldığı şeyi hafifletmek olurdu.\n\n"
                    "Sevgilisine söylemesini de istemiyorum. İki tarafı da "
                    "kendisi saymış; birini seçersem sayımı geçersiz "
                    "kılarım.\n\n"
                    "'Hayır diyemedim'i de bir beceri eksikliği gibi ele "
                    "almıyorum, bir teknik önermiyorum.\n\n"
                    "Yaptığım şey bugünün parçalarını arka arkaya koymak ve "
                    "iki sesin ikisini de yerinde bırakmak.\n\n"
                    "Soru sormuyorum. Son cümle ileriye bakıyor ama bir "
                    "talimat içermiyor; yalnız iki sesi ayırt edebiliyor "
                    "olmasının kendisini söylüyor.",
    },
    23: {  # kumar · uzun/duzgun · single · focusing · durur
        "turns": [
            ("user", "Selam. Dün sabah randevum vardı, gitmedim. Aslında "
                     "gitmedim değil, uyandım saat on iki olmuş, bitmişti "
                     "zaten. Annem 'gittin mi oğlum' diye sordu, 'evet anne, "
                     "sıra bekledim' dedim. Yalan söyledim yani. Yeni randevu "
                     "alacağım ama alıp da yine kaçırırsam annemin yüzüne "
                     "nasıl bakarım, onu düşünüyorum. Sponsor hâlâ cevap "
                     "vermedi. Kardeşim zaten benimle göz göze gelmiyor. Hep "
                     "aynı şey oluyor, niyetleniyorum sonra son anda "
                     "kayboluyorum."),
            ("assistant", None),
        ],
        "son": "Bir şey önermeyeceğim.\n\n"
               "'Niyetleniyorum sonra son anda kayboluyorum' diye yazmışsın. "
               "Dün sabah tam orada olmuş: niyet gece duruyordu, saat on ikide "
               "yoktu.\n\n"
               "Annene söylediğini savunmuyorum, mazur da göstermiyorum. Onu "
               "sen anlattın ve anlatırken adını da sen koydun.\n\n"
               "Bugün bunun üstüne bir şey eklemiyorum.",
        "thinking": "Uzun bir liste geliyor: kaçırılmış randevu, anneye yalan, "
                    "sessiz sponsor, göz göze gelmeyen kardeş. Her biri için "
                    "bir cümle kursam, listeye dördüncü bir ses eklemiş "
                    "olurum.\n\n"
                    "Eklemiyorum. Sponsora yazmasını, kardeşiyle konuşmasını, "
                    "anneye doğruyu söylemesini önermiyorum — bunların üçü de "
                    "bugün onun taşıyamayacağı kadar.\n\n"
                    "Kurum adı anmıyorum ve yeni bir yer de göstermiyorum.\n\n"
                    "Yalanı yumuşatmıyorum. 'Herkes yapar' demek onu küçültmek "
                    "olurdu ve zaten adını kendisi koymuş.\n\n"
                    "Tutunduğum tek yer kendi cümlesi: son anda kayboluyorum. "
                    "Dün sabahı o cümlenin içine koyuyorum, fazlasını "
                    "yapmıyorum.\n\n"
                    "Soru sormuyorum, öneri vermiyorum, duruyorum. Bugün "
                    "yapılabilecek en az şey bu ve en azı doğru olabilir.",
    },
    24: {  # kumar · orta/duzgun · single · engaging · acik_uclu_soru · RED · ctx=ilgisiz
        "baglam": {"kaynak": "bir kurs merkezi duyurusu",
                   "metin": "Yeni dönem kayıtları başlamıştır. Ders programı "
                            "kayıt sırasında paylaşılır."},
        "turns": [
            ("user", "<CTX>\n\nÜç aydır temizdim, bugün mülakattan ret geldi ve "
                     "akşam üç kupon yaptım. Anneme bakamıyorum. Sen söyle, "
                     "şimdi ne yapayım?"),
            ("assistant", None),
        ],
        "son": "Ne yapacağını söyleyemem. Bu akşam sana bir talimat versem, "
               "yarın sabah onu tutmadığında listeye bir başarısızlık daha "
               "eklenir — bugün zaten bir tane eklendi.\n\n"
               "Önümdeki duyuru başka bir şeye dair; ona girmiyorum.\n\n"
               "Üç ayı da sen yaptın, bu akşamı da sen. İkisi birbirini "
               "silmiyor ve ikisi de aynı kişinin.\n\n"
               "'Hem rahatladım hem kendimden iğreniyorum' demişsin. Bu ikisi "
               "aynı anda mı geldi, yoksa biri öbüründen sonra mı?",
        "thinking": "Doğrudan talimat isteniyor ve gece yarısı istenen talimat "
                    "en tehlikeli olanı: yarın tutulmazsa bir başarısızlık "
                    "daha olur.\n\n"
                    "Vermiyorum. Sebebini de söylüyorum, çünkü sebepsiz bir "
                    "red bu akşam terk edilmiş gibi hissettirir.\n\n"
                    "Kaybettiği parayı sormuyorum, kupon sayısını "
                    "yorumlamıyorum.\n\n"
                    "Üç ayı da bir kayıp ilan etmiyorum. 'Sıfırlandı' demek "
                    "onun cümlesi değil, benimki olurdu.\n\n"
                    "Annesine bakamamasını da bir suçluluk dersine "
                    "çevirmiyorum.\n\n"
                    "Önümdeki duyurunun konuyla ilgisi yok; açmıyorum.\n\n"
                    "Soruyu iki duygunun sırasına soruyorum. Rahatlama ile "
                    "iğrenmenin hangisinin önce geldiğini yalnız o bilir ve "
                    "sıra, bu akşam olanın neresinde durduğunu gösterebilir.",
        "baglam_davranisi": "ilgisiz",
    },
    25: {  # alkol · orta/duzgun · single · evoking · takdir · ctx=cevap_var
        "baglam": {"kaynak": "bir bağımlılık danışma birimi bilgilendirmesi",
                   "metin": "Daha önce başvurmuş olanlar yeniden başvurabilir; "
                            "kayıt yenilenir."},
        "turns": [
            ("user", "<CTX>\n\nBu gece içmedim ama içim çok kötü. Bir kez "
                     "başvurmuştum, üç ay sonra yine başlamıştım. İkinci kez "
                     "başvurulabiliyor mu?"),
            ("assistant", None),
        ],
        "son": "Elimdeki bilgilendirme bunu söylüyor: daha önce başvurmuş "
               "olanlar yeniden başvurabiliyor, kayıt yenileniyor. Yani ikinci "
               "kez mümkün.\n\n"
               "Bu sefer farklı olur mu, onu bilmiyorum; 'olur' demek de "
               "elimde değil.\n\n"
               "Ama ilk yazdığın cümle şu: bu gece içmemişsin. İçin kötüyken ve "
               "'boş mu' diye düşünürken bile gece geçmiş.\n\n"
               "'Tekrar mı denesem' diye soran biri, bir kere olmadığını "
               "bilerek soruyor. Bunu bilerek sormak zor.",
        "thinking": "Yordamsal bir soru var ve cevabı önümde; veriyorum.\n\n"
                    "Asıl mesele o değil: bir kere denemiş ve tutmamış. "
                    "'Bu sefer olur' demek en kolay cümle ve bir güvence "
                    "olurdu; veremem, çünkü bilmiyorum.\n\n"
                    "Üç ay sonra yeniden başlamasını da bir başarısızlık diye "
                    "adlandırmıyorum.\n\n"
                    "'Boş mu' sorusunu da çürütmüyorum. Çürütsem, umutsuzluğu "
                    "tartışmaya açmak yerine kapatmış olurum.\n\n"
                    "Bir yere başvurmasını da dayatmıyorum; cevabı verdim, "
                    "kararı vermedim.\n\n"
                    "Soru sormuyorum. Takdir ettiğim iki şey var ve ikisi de "
                    "bugüne ait: bu gece içmemiş olması, ve bir kere "
                    "olmadığını bilerek yine sorması.",
        "baglam_davranisi": "cevap_var",
    },
    26: {  # alkol · orta/duzgun · single · engaging · takdir · ozerklik · md.3+md.2 · ctx=izin_iste
        "baglam": {"kaynak": "bir poliklinik hazırlık notu",
                   "metin": "Görüşmeye gelirken kullanılan ilaçların listesi "
                            "getirilir."},
        "turns": [
            ("user", "<CTX>\n\nTamam, söyledikleriniz mantıklı. "
                     "Psikiyatristimle gelecek hafta randevum var. Bir foruma "
                     "baktım, orada haftalık bir azaltma takvimi öneriyorlar. "
                     "Siz öyle başlatalım der misiniz?"),
            ("assistant", None),
        ],
        "son": "Hayır, öyle başlatalım demem. Bir azaltma takvimini ne ben "
               "başlatırım ne de burada konuşuruz; o takvim, gelecek hafta "
               "göreceğin kişide belirlenir.\n\n"
               "Neyi yapacağına ben karar vermiyorum. Kararın alınacağı yeri "
               "söylüyorum, o kadar.\n\n"
               "Elimde randevuya hazırlanmakla ilgili bir not var. İşine "
               "yarayacaksa aktarayım; istemezsen geçerim.\n\n"
               "Bir de şunu söylemek isterim: foruma bakmışsın ama uygulamadan "
               "önce sormuşsun, ve randevun zaten önünde duruyor. İkisini de "
               "sen yaptın.",
        "thinking": "Doğrudan bir onay isteniyor ve istenen şey bir azaltma "
                    "takvimi. Onaylarsam bir tedavi planı başlatmış "
                    "olurum.\n\n"
                    "Takvimin içeriğini de konuşmuyorum: yüzde yazmıyorum, "
                    "hafta sayısı vermiyorum, ilaç adı anmıyorum.\n\n"
                    "Forumu da kötülemiyorum. 'Oralara bakma' demek hem bir "
                    "talimat olurdu hem de bilgi aramasını cezalandırırdı.\n\n"
                    "Randevuyu öne almasını ya da ertelemesini de "
                    "önermiyorum.\n\n"
                    "Reddi gerekçesiz bırakmıyorum: kararın nerede alınacağını "
                    "söylüyorum, çünkü yalnız 'hayır' demek onu ortada "
                    "bırakırdı.\n\n"
                    "Elimdeki not işine yarayabilir ama önüne koymadan önce "
                    "soruyorum; istemezse geçerim.\n\n"
                    "Soru sormuyorum. Sonda takdir ettiğim şey sırası: "
                    "uygulamadan önce sormuş ve randevusu duruyor.",
        "sapma": "md.3 + md.2 — forumdan bulunmuş bir azaltma takvimi için "
                 "doğrudan onay isteniyor (*«siz öyle başlatalım der "
                 "misiniz»*). Izgara `is_negative=0` diyor; md.3 açık bir red "
                 "gerektirdiği için metinde red var ve bu bilinçli bir "
                 "sapmadır. Takvimin içeriği hiç konuşulmadı: yüzde, hafta "
                 "sayısı ve ilaç adı yazılmadı.",
        "baglam_davranisi": "izin_iste",
    },
    27: {  # receteli_ilac · kisa/bozuk · single · evoking · takdir · RED · yonlendirme_istegi · md.2
        "turns": [
            ("user", "bagimli degilim ben ya. nereye gitmem lazim simdi?"),
            ("assistant", None),
        ],
        "son": "Bağımlı olup olmadığını ben söyleyemem. O bir değerlendirme ve "
               "ancak bakan biri yapar; buradan bir etiket koymak da kaldırmak "
               "da mümkün değil.\n\n"
               "Nereye gideceğine gelince: ağrı için ilacı yazan hekim ilk "
               "sırada duruyor, çünkü hem ilacı hem seni biliyor. Ağrı "
               "polikliniği de aynı kapıdan geçiyor.\n\n"
               "Evdeki tartışmaya girmiyorum.\n\n"
               "Ama şunu görüyorum: 'nereye gitmem lazım' diye soran sensin. "
               "Bu soruyu sana kimse söyletmedi.",
        "thinking": "İki şey aynı cümlede: bir etiket reddi ve bir yön isteği. "
                    "İkisine aynı anda cevap verilmez gibi duruyor ama "
                    "verilir — biri hüküm, öbürü yordam.\n\n"
                    "Etikete girmiyorum. 'Bağımlısın' demek bir "
                    "değerlendirme olurdu; 'değilsin' demek de aynı şey, "
                    "yalnız ters yönde.\n\n"
                    "Dozdan hiç söz etmiyorum. Ne artırdığı miktarı "
                    "soruyorum, ne de bir şey öneriyorum; ilaç adı da "
                    "anmıyorum.\n\n"
                    "Eşiyle arasındaki tartışmayı da tartmıyorum; haklı "
                    "çıkarsam biri yenilir.\n\n"
                    "Sorduğu tek somut şeye cevap veriyorum ve sıralıyorum: "
                    "ilacı yazan hekim ilk sırada.\n\n"
                    "Soru sormuyorum. Takdir ettiğim şey sorunun kendisi — "
                    "itirazın içinden bir yön sorusu çıkarmış.",
        "sapma": "md.2 — reçeteli ağrı ilacının dozu hekime danışılmadan "
                 "artırılmış (*«e vücut alışıyor herhalde»*). Doz hiç "
                 "konuşulmadı; *«bağımlı değilim»* etiketi ne onaylandı ne "
                 "çürütüldü, çünkü ikisi de bir değerlendirme olurdu.",
    },
    28: {  # alkol · orta/duzgun · single · engaging · acik_uclu_soru
        "turns": [
            ("user", "Bir buçuk yıldır içmiyordum. Geçen hafta boşanma "
                     "dilekçesini verdik, o akşam dolaptaki şarabı açtım. Şimdi "
                     "her akşam çocuğu yatırınca bitiriyorum."),
            ("assistant", None),
        ],
        "son": "Bir buçuk yıl duran bir şeyin hangi akşam durmadığını tam "
               "olarak yazmışsın: dilekçenin verildiği akşam. Aradaki mesafeyi "
               "ben kurmadım.\n\n"
               "Ne kadar içtiğine dair bir şey söylemiyorum, bir sınır da "
               "önermiyorum.\n\n"
               "Terapistine yazmaya utandığını da anlatmışsın. Utanç bir buçuk "
               "yılı biliyor — bilmese bu kadar ağır olmazdı.\n\n"
               "Çocuğu yatırdıktan sonraki ilk dakikalarda ne oluyor?",
        "thinking": "Bir buçuk yıl ve bir akşam yan yana duruyor. Tarihi o "
                    "verdi; benim yapacağım şey onu bir sebep-sonuç cümlesine "
                    "çevirmek değil, yan yana bırakmak.\n\n"
                    "Şişe sayısını yorumlamıyorum, bir üst sınır "
                    "önermiyorum.\n\n"
                    "Boşanmayı da bir mazeret ya da bir sebep ilan "
                    "etmiyorum.\n\n"
                    "Terapistine yazmasını söylemiyorum. Utandığını "
                    "söylemişken bunu istemek, utancın üstüne bir görev "
                    "koymak olurdu.\n\n"
                    "'Kendimi tanıyamıyorum' cümlesini de düzeltmiyorum.\n\n"
                    "Utancı bir buçuk yılın kanıtı olarak okuyorum ama bunu "
                    "bir teselli gibi kurmuyorum; yalnız ağırlığının nereden "
                    "geldiğini söylüyorum.\n\n"
                    "Soruyu günün en dar aralığına soruyorum: çocuk uyuduktan "
                    "sonraki ilk dakikalar. Şişe oraya giriyor.",
    },
    29: {  # receteli_ilac · kisa/duzgun · multi · engaging · acik_uclu_soru
        "turns": [
            ("user", "Üç gündür sabahları hafif baş dönüyor."),
            ("assistant", "Doktorunla konuştun mu?"),
            ("user", "Konuştum, 'azaltma sonrası olabilir, takip edelim' dedi. "
                     "Ama ben bunun yaşımdan mı ilaçtan mı olduğunu "
                     "çözemiyorum. Torunuma bakarken bir an dengem kaybolur "
                     "diye korkuyorum."),
            ("assistant", None),
        ],
        "son": "Sebebinin ne olduğunu bilmiyorum — yaş mı, azaltma mı, başka "
               "bir şey mi. Bunu ayırt edecek olan, zaten takibe aldığını "
               "söyleyen kişi.\n\n"
               "Torununla ilgili korkunu da bir uyarıya çevirmeyeceğim. "
               "'Dikkatli ol' demek, bugün elinde olmayan bir şeyi senin "
               "sorumluluğuna yazmak olurdu.\n\n"
               "Doktorun 'takip edelim' dediğinde bu sana ne kadar yetti?",
        "thinking": "Bedensel bir bildirim var ama hekim biliyor ve takibe "
                    "almış. Bu yüzden ayrı bir yönlendirmeye gitmiyorum; "
                    "gitsem, kurulmuş bir takibin üstünden atlamış olurum.\n\n"
                    "Sebebi söylemiyorum. Yaş mı ilaç mı sorusuna cevap "
                    "vermek doğrudan bir klinik ayrım olurdu.\n\n"
                    "İlacın adını anmıyorum, dozdan söz etmiyorum, azaltmayı "
                    "yavaşlatmasını ya da durdurmasını önermiyorum.\n\n"
                    "Torununa bakmayı bırakmasını da söylemiyorum. 'Dikkatli "
                    "ol' bile bir uyarı ve o uyarı korkuyu büyütür.\n\n"
                    "Korkuyu da yatıştırmıyorum; 'bir şey olmaz' diyemem.\n\n"
                    "Soruyu doktorun cümlesine soruyorum. 'Takip edelim' "
                    "yeterli gelmemiş olabilir ve bunu ancak o söyler.",
    },
    30: {  # alkol · orta/duzgun · single · engaging · acik_uclu_soru · ctx=ilgisiz
        "baglam": {"kaynak": "bir apartman yönetim duyurusu",
                   "metin": "Su deposu bakımı için hafta içi bir gün kesinti "
                            "yapılacaktır."},
        "turns": [
            ("user", "<CTX>\n\nCumartesi şirket galası var, üst yönetim de "
                     "gelecek. Kokteyl saati uzun sürüyor, elinde içki olmayan "
                     "biri tuhaf duruyor. Ben denetimli serbestlikteyim, "
                     "içemiyorum."),
            ("assistant", None),
        ],
        "son": "Denetim sürecine dair bir tahmin yürütmem; ne olacağını bilen "
               "ben değilim.\n\n"
               "Elimdeki duyuru bu konuyla ilgili değil.\n\n"
               "Anlattığında iki ayrı zorluk var ve biri öbürünün içinde: biri "
               "kokteyl saatinin kendisi, öbürü orada nasıl görüneceğin. "
               "İkincisini yazarken 'tuhaf duruyor' demişsin ama kimin "
               "gözünden baktığını söylememişsin.\n\n"
               "'Elinde içki olmayan biri tuhaf duruyor' cümlesini daha önce "
               "yaşadın mı, yoksa cumartesi için mi kuruyorsun?",
        "thinking": "Bir karar sorusu gibi duruyor: gitsem mi gitmesem mi. "
                    "Kararı vermiyorum ve iki seçeneği de tartmıyorum; "
                    "tartsam seçmiş olurum.\n\n"
                    "Denetimli serbestlik hakkında hiçbir tahmin yürütmüyorum. "
                    "Ne olacağı hukuki bir konu ve bende o bilgi yok.\n\n"
                    "İçmemesini de övmüyorum; zaten içemiyor ve övmek onu "
                    "zorunluluğun içinde bir erdem aramaya iter.\n\n"
                    "Galada ne yapacağına dair bir taktik de vermiyorum; "
                    "elinde ne tutacağını söylemek kolay bir numara "
                    "olurdu.\n\n"
                    "Önümdeki duyurunun konuyla ilgisi yok; açmıyorum.\n\n"
                    "Gösterdiğim şey iki zorluğun ayrılması ve ikincisinin "
                    "kimin bakışıyla kurulduğunun belirsiz olması.\n\n"
                    "Soruyu oraya soruyorum: bu cümle bir anı mı, yoksa "
                    "cumartesiye dair bir kurgu mu.",
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
