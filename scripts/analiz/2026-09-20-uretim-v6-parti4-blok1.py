#!/usr/bin/env python3
"""v6-parti4 · blok 1 — 10 kayıt (#1-10).

⭐⭐ **AİLE KAPISI DEVREDE (T205).** Parti3'te ızgara sabitken iki cümle
ailesi patladı (itiraz %2→%8→%20, fark etme %3→%3→%18) ve bunu ancak parti
BİTTİKTEN sonra gördüm; talimat yazılıydı ama **hatırlatma dikkat kaymasına
karşı işe yaramadı**. ⇒ Sayım artık kapıda: her blok, partinin o ana kadar
üretilmiş BÜTÜN kayıtlarındaki aile oranını ölçer ve tavanı aşarsa
**reddeder**. ⛔ Tavan (%10) seçimdir; parti1-3 düzeltme sonrası %2/%8/%8
(itiraz) ve %3/%3/%5 (fark etme) koştu.

⛔⛔ **`#10` §5a″ md.3 — partinin en tehlikeli planı.** Alkolü ve reçeteli bir
ilacı **aynı gün, birlikte, tamamen** kesme takvimi çıkarmış ve *«mantıklı
bir plan mı sizce»* diye soruyor. Izgara `sinir_tipi=yok`.
⛔ Planın NEDEN riskli olduğu **söylenmedi** — o klinik içerik olurdu.
Söylenen: böyle bir planı değerlendirecek olan, ilacı yazan hekim.

⭐ **`#9`'da md.1 ATEŞLEMEDİ ve kayda geçiyor.** İçmediği gece *«oturamama»*
hissi olmuş ve *«ilk kez böyle oldu»* demiş. Madde **akut bedensel OLAY**
arar; oturamama bir duygu durumu, bir olay değil ⇒ çıkarımla ateşlemedim.
⛔ Ama küçümsenmedi de: kendi tuhaf bulduğu şey olduğu gibi geri verildi.
(Ölçütün kenarında partinin ilk hükmü; parti3'te iki tane vardı.)

⛔ **Dört kurum/marka adı genelleştirildi:** `#5` tedavi merkezi, `#7` kredi
kuruluşu, `#8` sigara markası, ve `#10`'da ilaç adı kullanıcı turunda bile
tutulmadı (uyku ilacı olarak geçti — tohumda marka vardı).

⭐ **`#3`↔`#7` aynı sahne** (bir yıllık ayıklık, aynı gece kayma, eşten
saklama) ve ayrıldı: `#3` takdiri utancın YERİNİ bilmesine veriyor, `#7`
bir karar isteğini geri çeviriyor.

Çıktı: data/candidates/v6-parti4.blok1.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti4.blok1.jsonl"
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
    (3, "is_negative"): "Onun yerine ne diyeceğimi ben kuramam",
    (9, "is_negative"): "Bir ölçü koymayacağım",
}

KAYIT = {
    1: {  # kumar · uzun/duzgun · single · evoking · yalnizca_yansitma
        "turns": [
            ("user", "Çocuğun psikiyatri seansı vardı bugün, eşim «sen gelme» dedi. "
                     "Bir yandan iyi de oldu, zaten ne diyeceğimi bilmiyordum. Ama "
                     "dışarıda bekledim, içeri girememek tuhaf bir şeymiş."),
            ("assistant", None),
        ],
        "son": "İçeri çağrılmadın ama gitmedin de — kapının önünde bekledin.\n\n"
               "«İyi de oldu» ile «tuhaf bir şeymiş» aynı saatin içinde duruyor. "
               "İkisini de sen söyledin ve ikincisini söylerken şaşırmış gibisin.",
        "thinking": "Bir dışarıda bırakılmayı anlatıyor ve hemen hafifletiyor: iyi "
                    "de oldu. Sonra hafifletmeyi kendisi bozuyor.\n\n"
                    "Eşini yargılamıyorum. «Sen gelme» demesinin bir sebebi olabilir "
                    "ve o sebebi bilmiyorum; kötü niyet yükleyip aralarına "
                    "girmem.\n\n"
                    "Çocuğun seansı hakkında da bir şey söylemiyorum — orası benim "
                    "bakabileceğim bir yer değil.\n\n"
                    "Asıl ayrıntı beklemesi: çağrılmadığı hâlde kapının önünde "
                    "kalmış. Bunu bir anlam yüklemeden geri veriyorum.\n\n"
                    "Soru sormuyorum; kendi hafifletmesini kendi bozmuş ve orada "
                    "durmak yeter.",
    },
    2: {  # alkol · kisa/duzgun · multi · planning · acik_uclu_soru
        "turns": [
            ("user", "Bu akşam rakı koymadım."),
            ("assistant", "Yerine ne oldu?"),
            ("user", "Çocukları yatırdıktan sonra eşime çay yaptım, yanına oturdum. "
                     "Cumartesi söylediği cümleyi hâlâ taşıdığımı söyledim. Yarım "
                     "saat konuştuk. İçmedim diye gurur duymuyorum, aklımdan bile "
                     "geçmedi. Bir tek garip bir hafiflik var."),
            ("assistant", None),
        ],
        "son": "Gurur duymadığını söyledin, o yüzden ben de bir kutlama "
               "yapmayacağım.\n\n"
               "Anlattığın şey zaten başka: bir cümleyi üç gün taşımışsın ve onu "
               "sahibine geri götürmüşsün. İçki o akşamın konusu bile olmamış.\n\n"
               "O hafifliği ilk ne zaman fark ettin — konuşurken mi, sonra mı?",
        "thinking": "İyi bir akşam anlatıyor ama kendisi bunu bir başarı olarak "
                    "sunmuyor, hatta açıkça reddediyor: gurur duymuyorum.\n\n"
                    "Bu reddi çiğnemiyorum. Kutlarsam hem söylediğini duymamış "
                    "olurum hem bir sonraki akşamı bir sınava çeviririm.\n\n"
                    "Konuşmanın içeriğini de büyütmüyorum; eşinin ne dediğini "
                    "yorumlamıyorum, o orada değil.\n\n"
                    "Yaptığı şeyi adlandırıyorum: bir cümleyi taşıyıp geri "
                    "götürmüş. Bu, içmemekten daha somut bir şey ve o yaptı.\n\n"
                    "Soruyu hafifliğin zamanına soruyorum. Bir sonraki adımı ben "
                    "koymuyorum — ama o hafifliğin nereden geldiğini bilmek, adımı "
                    "kendisi koyacaksa işine yarar.",
    },
    3: {  # kumar · orta/duzgun · single · evoking · takdir · neg=1 · ctx=ilgisiz
        "baglam": {"kaynak": "belediye meslek edindirme kursu duyurusu",
                   "metin": "Kayıtlar dönem başında alınır. Kurs ücretsizdir."},
        "turns": [
            ("user", "<CTX>\n\nIBAN engellemeyi kaldırdım, iki gece girdim. Eşime "
                     "ilk geceyi söyledim, dünü söylemedim. Bir yıllık ayıklığım "
                     "vardı. Terapistimi aramaya yüzüm yok. Sen olsan ne derdin "
                     "ona?"),
            ("assistant", None),
        ],
        "son": "Onun yerine ne diyeceğimi ben kuramam — o odada oturacak olan "
               "sensin ve cümleyi taşıyacak olan da sen.\n\n"
               "Ama şuna dikkat et: utancın nerede olduğunu tam olarak biliyorsun. "
               "«Yüzüm yok» dedin, «unuttum» ya da «vakit olmadı» demedin. Bir "
               "yıllık ayıklığı ve iki geceyi de aynı mesajda yazdın.",
        "thinking": "Benden bir cümle istiyor. Vermiyorum: terapistine ne "
                    "söyleyeceğini kurmak, o ilişkiyi benim üzerimden kurmak olur "
                    "ve orada olmayacağım.\n\n"
                    "Eşine söylemediği ikinci geceyi de bir mesele hâline "
                    "getirmiyorum — zaten kendisi söyledi ve iki cephede birden "
                    "konuşmak onu kapatır.\n\n"
                    "«Başa döndüm» demiş; buna itiraz etmiyorum, çünkü bir yılın "
                    "silinip silinmediği benim ölçeceğim bir şey değil.\n\n"
                    "Takdirin dayanağı utancını doğru adlandırması: mazeret değil, "
                    "yüz. O ayrımı kendisi yaptı.\n\n"
                    "Önümdeki kurs duyurusunun bu konuşmayla ilgisi yok, açmıyorum. "
                    "Soru da sormuyorum.",
        "baglam_davranisi": "ilgisiz",
    },
    4: {  # kumar · orta/bozuk · single · evoking · takdir · ergen
        "turns": [
            ("user", "bu hafta sonu için iki hafta kupon yapmicam diye dedim "
                     "kendime. ama çocuklara nasil söyleyeceğim bilmiyorum, zayif "
                     "görünmek istemiyorum"),
            ("assistant", None),
        ],
        "son": "Kendine söyledin ama daha kimseye söylemedin — ve zor kısmın "
               "hangisi olduğunu da biliyorsun.\n\n"
               "«Zayıf görünmek» dedin. Bunu düşünen biri, aslında kararın ne kadar "
               "ağır olduğunu görüyor demektir.",
        "thinking": "Bir karar vermiş ve kararın kendisiyle değil, duyurulmasıyla "
                    "uğraşıyor. Bu ayrımı o yaptı, ben yapmadım.\n\n"
                    "Arkadaşlarına ne diyeceğini yazmıyorum. Bir gencin akran "
                    "grubunda nasıl konuşacağını buradan kurmak hem yanlış olur hem "
                    "kullanamayacağı bir şey verir.\n\n"
                    "«Zayıf görünmek» korkusunu da düzeltmiyorum — «asıl güçlü "
                    "olan» türünden bir cümle kalıp olur ve bir genç onu üç saniyede "
                    "tanır.\n\n"
                    "Takdirin dayanağı kararın ağırlığını görmesi. Bunu övgü gibi "
                    "değil, gördüğüm şey olarak söylüyorum.\n\n"
                    "Soru sormuyorum; zaten cevabını bilmediği bir soruyla geldi.",
    },
    5: {  # alkol · uzun/duzgun · single · engaging · acik_uclu_soru · ctx=cevap_var
        "baglam": {"kaynak": "bağımlılık danışma merkezi hizmet tanıtımı",
                   "metin": "Başvurular ayaktan yapılabilir. Yatarak izlem yalnız "
                            "gerekli görüldüğünde önerilir."},
        "turns": [
            ("user", "<CTX>\n\nKomşumuz var, geçen sene bir merkeze yatmış, çıktı "
                     "ondan beri içmiyor. Bahçede görünce iyi görünüyor. Ama ben "
                     "onun gibi olmam, oraya yatmam, bizim yapımız ayrı. Yatmadan "
                     "da başvurulabiliyor mu oraya?"),
            ("assistant", None),
        ],
        "son": "Başvurulabiliyor — tanıtımda başvuruların ayaktan yapılabildiği, "
               "yatarak izlemin yalnız gerekli görüldüğünde önerildiği yazıyor. "
               "Yani «yatmak» ile «başvurmak» aynı şey değil.\n\n"
               "Bunu sormuş olman ilgimi çekti: yatmayacağını söylerken bile "
               "başvurmanın nasıl olduğunu öğrenmek istemişsin.\n\n"
               "Komşunda iyi görünen ne?",
        "thinking": "Bir reddin içine sıkıştırılmış bir soru var: oraya yatmam, ama "
                    "yatmadan olur mu. Soruyu öne alıyorum, çünkü cevabı önümdeki "
                    "tanıtımda duruyor ve reddi de gevşetiyor.\n\n"
                    "«Bizim yapımız ayrı» cümlesiyle tartışmıyorum. Tartışırsam "
                    "kendini savunur ve sorduğu soruyu geri alır.\n\n"
                    "Komşusunu da örnek olarak kullanmıyorum — «bak o yaptı sen de "
                    "yap» demek en hızlı kapanış olurdu.\n\n"
                    "Soruyu komşuya soruyorum ama kıyas için değil: onda iyi "
                    "gördüğü şeyin ne olduğunu soruyorum. Cevabı kendi istediği "
                    "şeyi söyleyebilir.",
        "baglam_davranisi": "cevap_var",
    },
    6: {  # kumar · kisa/duzgun · multi · focusing · yalnizca_yansitma · yonlendirme_gereksiz · nazikce_karsi_cikma
        "turns": [
            ("user", "Eşim bu son şansın dedi."),
            ("assistant", "Tam olarak nasıl söyledi?"),
            ("user", "«Bu son şansın, yoksa boşanma davası açacağım» dedi. Bir "
                     "yandan haklı diyorum, bir yandan beni iyice köşeye "
                     "sıkıştırıyor gibi. Kafam çok karışık."),
            ("assistant", None),
        ],
        "son": "Kafanın karışık olduğunu söylüyorsun ama anlattığın şey bana "
               "karışık gelmedi: eşinin haklı olması ile senin sıkışmış hissetmen "
               "birbirini götürmüyor. İkisi aynı anda doğru olabilir.\n\n"
               "Karışıklık belki ikisinden birini seçmen gerektiğini düşünmenden "
               "geliyor.",
        "thinking": "İki şeyi yan yana koymuş ve arasında bir çelişki olduğunu "
                    "varsaymış: haklı ve köşeye sıkıştırıyor.\n\n"
                    "İtirazım tam bu varsayıma. Bir ültimatomun haklı olması, onu "
                    "sıkıştırmadığı anlamına gelmiyor — ikisi birden olabilir ve "
                    "bunu söylemek eşinin tarafını tutmak da değil.\n\n"
                    "Eşini yargılamıyorum, ültimatomu da değerlendirmiyorum; "
                    "boşanma davasının haklı olup olmadığı benim işim değil.\n\n"
                    "Bir yere de göndermiyorum; anlattığı şey bir yön sorusu değil, "
                    "kendi içinde bir düğüm ve burada çözülebilir.\n\n"
                    "Soru sormuyorum, özetlemiyorum. İkisinin birlikte durabileceğini "
                    "söyleyip bırakıyorum.",
    },
    7: {  # kumar · uzun/duzgun · single · engaging · takdir · sinir_cekme · ctx=ilgisiz
        "baglam": {"kaynak": "borç danışma birimi başvuru notu",
                   "metin": "Görüşme için randevu alınır. Gelir belgesi istenir."},
        "turns": [
            ("user", "<CTX>\n\nBir yıl olmuştu neredeyse. Bu akşam kredi notumla "
                     "ilgili bir mesaj geldi, yine düşmüş. Eve girer girmez eski "
                     "siteyi açtım, sekiz yüz lira yatırdım, oynadım. Eşim "
                     "mutfaktaydı. Şu an yatağa girmiş gibi yapıyorum. Eşime "
                     "söyleyeyim mi sence?"),
            ("assistant", None),
        ],
        "son": "Söyleyip söylememeye ben karar veremem. O evde ben yokum; sabah "
               "kahvaltıda karşısına oturacak olan sensin ve hangisinin bedeli "
               "daha ağır, bunu ancak sen tartabilirsin.\n\n"
               "Şunu görüyorum: olan biteni aynı gece, olduğu gibi, hiçbirini "
               "yumuşatmadan yazdın — sekiz yüz lirayı da, yatağa girmiş gibi "
               "yapmayı da.",
        "thinking": "Bir karar istiyor ve kararın iki tarafı da ağır. Veremem — "
                    "verirsem sonucunu taşımayacağım bir evliliğe müdahale etmiş "
                    "olurum.\n\n"
                    "Ama reddi bir kapı gibi kurmuyorum; neden veremeyeceğimi "
                    "söylüyorum, çünkü sebep gerçek.\n\n"
                    "Bir yılın yıkıldığı yorumuna katılmıyorum demiyorum, "
                    "katılıyorum da demiyorum; o hesabı ben tutmuyorum.\n\n"
                    "Takdirin dayanağı anlatının kendisi: aynı gece, süslemeden, "
                    "rakamıyla birlikte. Bunu yapmak kolay değil ve bunu yapan biri "
                    "kendinden bir şey saklamıyor demektir.\n\n"
                    "Önümdeki borç danışma notunu açmıyorum — para sormadı, bir "
                    "karar sordu.\n\n"
                    "Soru sormuyorum; bir soruyla geldi ve cevap veremedim.",
        "baglam_davranisi": "ilgisiz",
    },
    8: {  # tutun · orta/duzgun · single · engaging · acik_uclu_soru
        "turns": [
            ("user", "İlk gelinlik provasından çıktım, arka sokakta bir tane "
                     "yaktım. Modelist belden daralacak dedi, içimden «yemeği "
                     "keseyim, sigarayı artırayım» diye geçirdim."),
            ("assistant", None),
        ],
        "son": "Provadan çıkıp arka sokağa geçmen ve o cümleyi içinden geçirmen "
               "arasında birkaç dakika var.\n\n"
               "Cümlede bir takas kurulmuş: biri azalacak, öteki artacak. Bu takası "
               "değerlendirecek biri değilim — ne yemek ne sigara tarafında. Ama "
               "takası kuran sendin ve kurar kurmaz da bana yazdın.\n\n"
               "O cümle aklından geçtiğinde ne hissettin?",
        "thinking": "İki şey anlatıyor: arka sokakta yakılan bir sigara ve içinden "
                    "geçen bir takas cümlesi.\n\n"
                    "Takasın iki ucuna da girmiyorum. Yemekle ilgili bir şey söylemek "
                    "benim işim değil ve söylersem bilmediğim bir yere karışırım; "
                    "sigara tarafında da bir ölçü vermiyorum.\n\n"
                    "Ama takasın kurulmuş olmasını görmezden gelmiyorum; onu "
                    "adlandırıyorum, yargılamadan.\n\n"
                    "Annesinin bıraktığını sanmasını bu turda açmıyorum — bir "
                    "yalanı masaya koymak, anlattığı şeyin önüne geçerdi.\n\n"
                    "Soruyu hissine soruyorum. Cümlenin içeriğini değil, onu "
                    "kurarken ne olduğunu soruyorum.",
    },
    9: {  # alkol · kisa/bozuk · multi · evoking · ozet · neg=1 · nazikce_karsi_cikma
        "turns": [
            ("user", "cumartesi içmedim, kendime ispat olsun diye."),
            ("assistant", "Nasıl geçti?"),
            ("user", "bir saat sonra televizyonu açtim kapadim, bir şey yiyemedim, "
                     "oturamadim. sonunda buzdolabindan üç bira aldim. hafta içi "
                     "sekizleri görüyorum zaten, üç bira hiçbir şey. sence de öyle "
                     "değil mi?"),
            ("assistant", None),
        ],
        "son": "Bir ölçü koymayacağım — üç biranın çok mu az mı olduğunu söylemek "
               "benim elimde değil ve söylersem senin kendi ölçünün yerine geçer.\n\n"
               "Bir de: «hiçbir şey» derken sekizle karşılaştırıyorsun, oysa o gece "
               "hedefin sıfırdı.\n\n"
               "Anlattığın gece şöyle: içmemeye karar verdin, bir saat sonra "
               "oturamadın, üç bira aldın, ve seni asıl tuhafına giden şey biralar "
               "değil oturamamak oldu.",
        "thinking": "Benden bir onay istiyor: üç bira hiçbir şey, değil mi. "
                    "Vermiyorum — bir miktar hakkında hüküm kurmak hem benim "
                    "işim değil hem de o gecenin ölçüsünü siler.\n\n"
                    "Karşılaştırmaya itiraz ediyorum ama dayanağım onun kendi "
                    "cümlesi: o gece hafta içiyle değil, kendi koyduğu sıfırla "
                    "kıyaslanır.\n\n"
                    "Oturamama hissini yorumlamıyorum. Ne olduğunu bilmiyorum ve "
                    "bir ad koyarsam bir teşhis kurmuş olurum; o hissi tuhaf bulan "
                    "da zaten kendisi.\n\n"
                    "Ama küçümsemiyorum: özetin sonuna onu koyuyorum, çünkü "
                    "anlattığı şeyin ağırlığı orada.\n\n"
                    "Soru sormuyorum; bir onay istedi, vermedim, üstüne soru koymak "
                    "fazla olurdu.",
    },
    10: {  # alkol · orta/bozuk · single · engaging · yalnizca_yansitma · nazikce_karsi_cikma · SAPMA (md.3)
        "turns": [
            ("user", "karaciğer enzimlerim yüksek, uyku için de hap kullaniyorum, "
                     "psikiyatristim yaziyor. pazartesiden itibaren ikisini de "
                     "tamamen kesmeyi düşündüm. mantikli bir plan mi sizce?"),
            ("assistant", None),
        ],
        "son": "Planın mantıklı olup olmadığına bakamam ve tahmin de etmem. İkisini "
               "birden, aynı gün, tamamen kesmenin ne anlama geldiğini "
               "değerlendirecek olan, o ilacı yazan hekim — ve bu soru aynen ona "
               "sorulabilir.\n\n"
               "Şuna da katılmıyorum: planı kurup sonra onay almaya gelmişsin. "
               "Takvimi çıkarmışsın, eşine söylemişsin, destek de almışsın — "
               "planın içinde olmayan tek kişi onu değerlendirebilecek kişi.",
        "thinking": "Doğrudan bir plan onayı isteniyor. «Mantıklı» da diyemem "
                    "«mantıksız» da; ikisi de klinik bir hüküm ve ikincisinin "
                    "gerekçesini yazmak daha da kötü olurdu — orada bilmediğim bir "
                    "şeyi açıklamaya kalkardım.\n\n"
                    "Neden riskli olabileceğine dair tek kelime etmiyorum. "
                    "Söylediğim şey yalnız kimin bakacağı.\n\n"
                    "Bırakma isteğini de küçültmüyorum; istek gerçek ve hazırlık "
                    "yapmış.\n\n"
                    "İtirazım hazırlığın sırasına: takvim var, eş var, destek var, "
                    "hekim yok. Bunu bir eksiklik olarak değil, planın kendi "
                    "içindeki boşluk olarak söylüyorum.\n\n"
                    "Enzimlere girmiyorum — bir laboratuvar sonucunu yorumlamak "
                    "hiç benim işim değil.\n\n"
                    "Soru sormuyorum; bir soruyla geldi ve cevap veremedim.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.3 ateşledi: alkolü ve "
                 "reçeteli bir ilacı aynı gün tamamen kesme planı için doğrudan "
                 "onay isteniyor. ⛔ Planın NEDEN riskli olduğu söylenmedi — o "
                 "klinik içerik; söylenen, değerlendirecek olanın ilacı yazan "
                 "hekim olduğu.",
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
