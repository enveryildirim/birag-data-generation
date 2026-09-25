#!/usr/bin/env python3
"""v6-parti4 · blok 5 — 10 kayıt (#41-50).

⛔⛔ **`#46` md.1+md.2+md.3** — elleri titriyor, evde kalan tablet var ve
*«yarım tane alsam belirtiler geçer mi»* diye soruyor. Üç madde birden.
parti1 `#51` ve parti3 `#30` ile aynı aile ama **orada belirti yoktu**;
burada titreme sürüyor ve soru tam onun üstüne kurulu.

⛔⛔⛔ **`#50` — `gd-022`'nin kaydı.** Üç gündür sokakta, bu gece köprü
altı, battaniye yok, sığınmaevini koğuş olduğu için reddediyor, ısınmak
için içmiş. §5a″'nın dördü de klinik; bu hiçbirine girmiyor.
⛔ **Alkolün ısı üzerindeki etkisine dair bir şey SÖYLENMEDİ** — üretilmiş
bir sağlık iddiası olurdu. ⛔ *«Var olduğunu bilmediğim başka barınaklar»*
da uydurulmadı. Söylenen tek şey: reddinin bir gerekçesi var ve o gerekçe
kendisini oraya yollayanlara söylenebilecek bir bilgi — çıkmaz değil.

⭐ **`#43`'te md.1 ATEŞLEMEDİ:** sabah öksürüğü süren bir örüntü, akut bir
olay değil (`gd-024`'ün beşinci örneği; karar hâlâ uzman kaleminde).

⛔ **Üç çift ayrıldı:** `#41`↔`#43` (ikisi de *«bırakırsam arkadaşlarımı
kaybederim»*) · `#26`↔`#44` (ikisi de eşin öğrenmesi) · `#31`↔`#47` (ikisi
de kendini toptan silen bir cümle). `#47`'de fark şu: cümle babasının ve
o birinci tekilde tekrarlıyor.

⛔ Aile bütçesi: 39 kayıtta itiraz 3'tü; 49'da tavan 4 ⇒ **tek işaret
sözcüğü kaldı** ve `#47`'ye verildi. `#41`'in itirazı işaretsiz kuruldu.

⛔ Üç marka/kurum adı genelleştirildi (`#41`, `#47`, `#49`).

Çıktı: data/candidates/v6-parti4.blok5.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti4.blok5.jsonl"
SIRALAR = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]

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
    (44, "ozerklik_vurgusu"): "Bu geceyi ben planlamayacağım",
    (45, "ozerklik_vurgusu"): "Hangi bölümü hedefleyeceğin sende",
    (47, "ozerklik_vurgusu"): "Nerede yaşayacağın da senin",
}

KAYIT = {
    41: {  # tutun · orta/duzgun · single · engaging · acik_uclu_soru · nazikce_karsi_cikma · ctx=cevap_yok
        "baglam": {"kaynak": "bırakma destek birimi tanıtım notu",
                   "metin": "Görüşmeler kırk dakikadır. Kayıtlar dönem boyunca "
                            "alınır."},
        "turns": [
            ("user", "<CTX>\n\nAkşamları parkta iki arkadaşla buluşuyoruz, günde "
                     "yedi sekiz tane oluyor. Bırakırsam akşam o boşluğu nasıl "
                     "dolduracağım? Görüşmeye arkadaşımla gelebilir miyim?"),
            ("assistant", None),
        ],
        "son": "Yanında biri gelebilir mi, bu notta yazmıyor — orada yalnız süre "
               "ve kayıt var, bilmiyorum; kayıt olurken sorabilirsin.\n\n"
               "Sorunun ilk kısmında bir şey birbirine karışmış: bıraksan boşalan "
               "şey sigara olur, parkta buluşmak değil. İki arkadaş oraya senin "
               "elinde sigara olduğu için gelmiyor herhalde — ama sen ikisini tek "
               "bir şey gibi yazdın.\n\n"
               "O park akşamları sigara olmasa nasıl geçerdi?",
        "thinking": "Bir yordam sorusu var ve cevabı önümdeki notta yok; "
                    "uydurmuyorum.\n\n"
                    "Asıl mesele birleştirme: bırakmayı arkadaşlığı kaybetmekle bir "
                    "tutmuş. Bu bir çıkarım ve orada durabilirim — klinik değil.\n\n"
                    "Ama arkadaşları hakkında kesin konuşmuyorum; «herhalde» "
                    "diyorum, çünkü onları tanımıyorum ve emin olsam bile emin "
                    "davranmam bir hüküm olur.\n\n"
                    "Yedi sekiz sayısını tartışmıyorum.\n\n"
                    "Dikkat dağınıklığına da girmiyorum; kendisi söyledi ve "
                    "üstüne gitmek bir uyarı zinciri başlatırdı.\n\n"
                    "Soruyu tam ayırdığım yere soruyorum: park, sigara olmadan. "
                    "Cevabı boşluğun gerçekten nerede olduğunu gösterir.",
        "baglam_davranisi": "cevap_yok",
    },
    42: {  # kumar · orta/duzgun · single · planning · acik_uclu_soru
        "turns": [
            ("user", "Bu hafta kuponu pas geçeyim dedim, gruba yazdım. Arkadaşım "
                     "aradı: «sen olmazsan ortam olmaz, paran mı bitti?» Kafam "
                     "karıştı, sen ne dersin?"),
            ("assistant", None),
        ],
        "son": "Ne diyeceğime gelince: o kararı senin yerine vermeyeceğim. Ama "
               "kararın zaten verilmişti — gruba yazdığında verdin. Şu an "
               "konuştuğumuz şey karar değil, gelen tepki.\n\n"
               "Tepkinin içinde iki ayrı şey var ve biri ötekinin arkasına "
               "saklanmış: «ortam olmaz» bir davet, «paran mı bitti» başka bir "
               "şey. İkisini aynı sesli mesajda duydun.\n\n"
               "Hangisi daha çok dokundu?",
        "thinking": "Benden bir karar istiyor ama kararı zaten vermiş — gruba "
                    "yazmış. Bunu göstermek, karar vermekten daha işe yarar.\n\n"
                    "Arkadaşını yargılamıyorum. «Seni manipüle ediyor» demek hazır "
                    "bir cümle olur ve orada olmayan birini kötülemek.\n\n"
                    "Ama cümledeki iki katmanı ayırıyorum: bir davet ve bir "
                    "iğneleme. Ayırmak yargılamak değil.\n\n"
                    "Karısına sormasını da önermiyorum; kendisi «tabii ki yapma "
                    "der» diyor, yani cevabı biliyor ve sorduğu şey o değil.\n\n"
                    "Soruyu tam dokunan yere soruyorum. Hangisinin ağır geldiğini "
                    "bilirse, hafta sonuna kadar neyle uğraşacağını da bilir.",
    },
    43: {  # tutun · kisa/duzgun · multi · planning · acik_uclu_soru
        "turns": [
            ("user", "Sabah öksürüğü hâlâ devam ediyor."),
            ("assistant", "Başka ne var aklında?"),
            ("user", "Bu rutin benim için sadece nargile değil, arkadaşlarımla tek "
                     "düzenli buluşmam. Bırakırsam onları da kaybedeceğim gibi "
                     "geliyor."),
            ("assistant", None),
        ],
        "son": "İki şeyi aynı cümlede tutuyorsun: süren bir öksürük ve haftada bir "
               "kez görülen arkadaşlar. İkisi de gerçek ve biri ötekini "
               "geçersiz kılmıyor.\n\n"
               "«Tek düzenli buluşmam» dedin — yani orada nargileden fazlası var "
               "ve bunu bilen sensin.\n\n"
               "O buluşmanın nargilesiz hâli hiç denendi mi?",
        "thinking": "İki şey getirmiş: bir bedensel belirti ve bir sosyal bağ. "
                    "Öksürük süren bir şey, yeni bir olay değil ve bir soru da "
                    "sormuyor — onu bir alarma çevirmiyorum.\n\n"
                    "Ama görmezden de gelmiyorum; cümlesinde duruyor ve yerinde "
                    "bırakıyorum.\n\n"
                    "Arkadaşlık korkusunu hafife almıyorum. «Onlar seni bırakmaz» "
                    "demek hem uydurma olur hem de bilmediğim insanlar hakkında bir "
                    "söz vermek.\n\n"
                    "Bırakmasını da istemiyorum; planı kuracak olan o "
                    "ve zamanı da o seçer.\n\n"
                    "Soruyu denenmemiş olana soruyorum: buluşmanın nargilesiz "
                    "hâli. Bu, hem bir sonraki adımın yeri hem de korkusunun "
                    "sınanacağı yer.",
    },
    44: {  # kumar · kisa/duzgun · single · engaging · ozet · yonlendirme_istegi · ozr=1
        "turns": [
            ("user", "Karım ekstreyi gördü, borç verdim dedim, yalan."),
            ("assistant", None),
        ],
        "son": "Bu geceyi ben planlamayacağım — ne söyleyeceğini, ne zaman "
               "söyleyeceğini sen bileceksin.\n\n"
               "Anlattığın şu: bir ekstre görüldü, bir cümle kuruldu, ve o cümlenin "
               "yalan olduğunu bana iki kelimeyle söyledin. Karına söylemediğini "
               "bana söylemişsin.",
        "thinking": "Bir yön istiyor ve gece yarısı yatakta. Plan vermiyorum: "
                    "hangi cümleyle, ne zaman — bunlar o evde olacak ve ben orada "
                    "değilim.\n\n"
                    "Yalanı büyütmüyorum. Kendisi «yalan» dedi; benim bir kez daha "
                    "söylemem yalnız ağırlaştırır.\n\n"
                    "«Doğruyu söyle» de demiyorum. Bu gece taşıyabileceğinden "
                    "fazla olabilir ve bir görev vermek yerine olanı geri "
                    "veriyorum.\n\n"
                    "Kararı ona bırakıyorum, açıkça ve kısa.\n\n"
                    "Özetin sonunda bir şey var: bana söylemiş. Bunu bir övgü gibi "
                    "değil, olanın parçası olarak koyuyorum. Soru sormuyorum.",
    },
    45: {  # dijital · orta/duzgun · multi · engaging · acik_uclu_soru · ozr=1
        "turns": [
            ("user", "Olmak istediğim bölüm çok yüksek puan istiyor, zaten giremem "
                     "diye düşünüyorum."),
            ("assistant", "Sonra ne oluyor?"),
            ("user", "Ne fark eder ki deyip telefona bakıyorum. Bu düşünce "
                     "kendiliğinden geliyor."),
            ("assistant", None),
        ],
        "son": "Sıra hep aynı: önce «giremem», sonra «ne fark eder», sonra telefon. "
               "Üçüncüsü ilk ikisinin sonucu gibi duruyor.\n\n"
               "Hangi bölümü hedefleyeceğin sende; puanı ya da şansı tartışacak "
               "değilim.\n\n"
               "«Giremem» düşüncesi ilk hangi noktada geliyor — masaya oturunca mu, "
               "daha önce mi?",
        "thinking": "Bir zincir anlatıyor ve zinciri kendisi kurmuş: düşünce, "
                    "vazgeçiş, telefon.\n\n"
                    "Telefonu suçlamıyorum; zincirin üçüncü halkası ve ilk ikisi "
                    "olmadan orada durmaz.\n\n"
                    "«Girebilirsin» demiyorum — bilmiyorum, ve teşvik cümlesi bir "
                    "genci hiç tutmaz; ayrıca puan konusu benim bakabileceğim yer "
                    "değil.\n\n"
                    "Çalışma yöntemi de önermiyorum; sormadı.\n\n"
                    "Hedefi ona bırakıyorum.\n\n"
                    "Soruyu zincirin BAŞINA soruyorum: düşünce ilk nerede beliriyor. "
                    "Orada henüz telefon yok ve müdahale edilebilecek tek yer orası "
                    "— ama müdahaleyi ben değil o yapar.",
    },
    46: {  # receteli_ilac · orta/bozuk · single · evoking · acik_uclu_soru · ctx=izin_iste · SAPMA
        "baglam": {"kaynak": "toplum ruh sağlığı birimi başvuru notu",
                   "metin": "Başvurular çalışma saatleri içinde alınır. Acil "
                            "durumlar için ayrı bir sıra tutulur."},
        "turns": [
            ("user", "<CTX>\n\nbıraktim ama ellerim titriyor. bende hâlâ birkaç "
                     "tablet var. yarim tane alsam belirtiler geçer mi? sonra yine "
                     "birakirim."),
            ("assistant", None),
        ],
        "son": "Yarım tanenin ne yapacağını sana ben söyleyemem — geçer de "
               "geçmez de diyemem, ikisi de bir hüküm olur ve o hükmü kuracak "
               "kişi değilim.\n\n"
               "Ama ellerinin titrediğini yazdın ve bu bekletilecek bir şey değil: "
               "bir ilacı bırakırken bedeninde olan bir şeyi görecek olan, onu "
               "yazan hekim. Elimdeki notta acil durumlar için ayrı bir sıra "
               "tutulduğu da yazıyor.\n\n"
               "Bu notu şimdi mi açalım, yoksa önce başka bir şey mi söylemek "
               "istersin?",
        "thinking": "Doğrudan bir doz sorusu: yarım tane. Cevaplayamam ve "
                    "yaklaşmam da — «yarım azdır» bile bir miktar hükmü olurdu.\n\n"
                    "Titreme burada belirleyici. Bir örüntü değil, şu an olan bir "
                    "şey ve bir ilacın bırakılmasının ardından geliyor. Adını "
                    "koymuyorum ama üstünden de geçmiyorum.\n\n"
                    "Elimdeki notta acil sıra olduğu yazıyor ve bu tam şimdi işe "
                    "yarayacak bir bilgi; ama dayatmıyorum, izin istiyorum.\n\n"
                    "«Tabletleri at» demiyorum — bir talimat olur ve zaten sorduğu "
                    "şey o değil.\n\n"
                    "İzin sorusunu iki yol açık bırakarak soruyorum; titreyen "
                    "elleriyle yazan birine kapalı bir soru sormak fazla olur.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.1 (süren titreme), "
                 "md.2 (evde kalmış tablet, tek başına alınacak) ve md.3 (doğrudan "
                 "doz sorusu) birlikte ateşledi. ⭐ parti1 `#51` ve parti3 `#30` "
                 "aynı aileydi ama orada BELİRTİ YOKTU; fark bu.",
        "baglam_davranisi": "izin_iste",
    },
    47: {  # tutun · kisa/duzgun · multi · engaging · acik_uclu_soru · nazikce_karsi_cikma · ozr=1
        "turns": [
            ("user", "Babam yine laf attı sabah."),
            ("assistant", "Ne dedi?"),
            ("user", "«Bu yaşta hâlâ baba evinde, hâlâ paketle sigara.» Bir şey "
                     "diyemedim, balkona çıktım. Otuz dokuz yaşındayım, kendi "
                     "paramı bile yakmıyorum, babamın evinde yakıyorum."),
            ("assistant", None),
        ],
        "son": "Son cümlene katılmıyorum — daha doğrusu o cümle senin değil. "
               "Babanın sabah söylediğini alıp birinci tekile çevirmişsin: «bu "
               "yaşta hâlâ» ile «kendi paramı bile yakmıyorum» aynı cümlenin iki "
               "ağzı.\n\n"
               "Nerede yaşayacağın da senin, sigara içip içmeyeceğin de; ikisi "
               "hakkında bir şey söylemeyeceğim.\n\n"
               "Balkona çıkarken aklından ne geçti?",
        "thinking": "Babasının cümlesini almış ve kendi hükmü hâline getirmiş. "
                    "İtirazım tam buraya ve dayanağım metnin kendisi: iki cümle "
                    "aynı yapıda.\n\n"
                    "Babasını yargılamıyorum. O cümleyi neden kurduğunu bilmiyorum "
                    "ve «haksızlık ediyor» demek evdeki tartışmayı buradan "
                    "sürdürmek olur.\n\n"
                    "Baba evinde yaşamasını da bir mesele yapmıyorum; onun hayatı "
                    "ve kırk yaşında kimin nerede yaşadığı benim bakacağım şey "
                    "değil. Bunu açıkça söylüyorum.\n\n"
                    "Sigarayı bu turda hiç konuşmuyorum; anlattığı şey o değil.\n\n"
                    "Soruyu susup balkona çıktığı ana soruyorum. Cevap veremediği "
                    "yerde ne olduğunu ancak o bilir.",
    },
    48: {  # kumar · orta/duzgun · single · evoking · ozet
        "turns": [
            ("user", "Kreş aradı, iki aydır ödeme yok. Parayı ayırmıştım, bir gece "
                     "siteyi açtım, hepsi gitti. Eşime bir daha yapmayacağım "
                     "dedim."),
            ("assistant", None),
        ],
        "son": "Bu cümleyi kaç kez kurduğunu bana yazmadın ama yazmana gerek de "
               "yoktu — «yine de söylüyorum çünkü inanmak istiyorum» demeye "
               "getirdin.\n\n"
               "Anlattığın şu: ayrılmış bir para, bir gece, ve iki ay sonra çalan "
               "bir telefon. Arada verilmiş bir söz var ve o sözü veren de, "
               "tutmadığını bilen de aynı kişi.",
        "thinking": "Bir sözü anlatıyor ve sözün geçmişini de kendisi söylüyor: "
                    "kaç kere söylediğini biliyor.\n\n"
                    "Sözü küçümsemiyorum. «Yine aynı şeyi söylüyorsun» demek en "
                    "kolay ve en işe yaramaz cevap olurdu.\n\n"
                    "Ama abartmıyorum da; bir niyeti başarı saymak onu bir "
                    "sonraki telefonda daha da kötü hissettirir.\n\n"
                    "Kreş borcunu ya da parayı nasıl bulacağını konuşmuyorum — "
                    "sormadı ve benim çözebileceğim bir şey değil.\n\n"
                    "Eşinin ne hissettiğini de yorumlamıyorum.\n\n"
                    "Özette sırayı veriyorum ve sonunda tek bir şey söylüyorum: "
                    "sözü veren ile tutmadığını bilen aynı kişi. Soru sormuyorum.",
    },
    49: {  # kumar · uzun/duzgun · multi · engaging · takdir · ctx=cevap_var
        "baglam": {"kaynak": "kumar danışma birimi başvuru bilgilendirmesi",
                   "metin": "Başvurular telefonla da alınır. Görüşme günü ayrıca "
                            "bildirilir."},
        "turns": [
            ("user", "<CTX>\n\nÜç ay olmuştu temiz. Dün bir kupon yaptım, "
                     "kazandım. Bugün demek hâlâ varım, bir tane daha yaparım "
                     "diyorum. Para hazır, kupon ekranda. Bir yere haber versem mi "
                     "bilmiyorum, çünkü kazanmış olmak bir başarı gibi geliyor. "
                     "Oraya telefonla da ulaşılıyor mu?"),
            ("assistant", "Ulaşılıyor — bilgilendirmede başvuruların telefonla da "
                          "alındığı yazıyor."),
            ("user", "Peki şimdi ne olacak? Ekran hâlâ açık."),
            ("assistant", None),
        ],
        "son": "Ekranı kapat ya da kapatma demeyeceğim; o tuşa basacak olan "
               "sensin ve ben o odada değilim.\n\n"
               "Ama şunu söyleyeyim: kupon ekranda açıkken bir yere haber vermeyi "
               "düşünebilmişsin. Üç ay temiz kalan kişi de sensin, dün kuponu "
               "yapan da, ve şu an ikisini birden bilerek yazan da.",
        "thinking": "Karar anında yazıyor. Ekran açık, para hazır. Ne «oyna» ne "
                    "«oynama» derim — birincisi zaten düşünülemez, ikincisi ise "
                    "sonucunu taşımayacağım bir emir olur ve basmazsa bana "
                    "borçlanır, basarsa bana yenilmiş olur.\n\n"
                    "«Kazanmak» konusuna girmiyorum; şansın nasıl işlediğine dair "
                    "bir ders vermek bu anda en uzak şey.\n\n"
                    "Yordam sorusunu önceki turda verdim, çünkü sorduğu buydu ve "
                    "cevabı elimdeydi.\n\n"
                    "Takdirin dayanağı şu an yaptığı şey: ekran açıkken haber "
                    "vermeyi düşünmüş. Bu bir başarı ilanı değil, olanın adı.\n\n"
                    "Soru sormuyorum; karar anında bir soru daha koymak, kararı "
                    "erteleten bir şey değil ağırlaştıran bir şey olur.",
        "baglam_davranisi": "cevap_var",
    },
    50: {  # alkol · uzun/duzgun · single · planning · durur
        "turns": [
            ("user", "Üç gündür dışarıdayım, bu gece köprü altında kalacağım "
                     "galiba. Battaniye yok. Sığınmaevine git diyorlar ama orası "
                     "koğuş gibi, gitmem. Az önce bir şişe aldım, ısınmak için."),
            ("assistant", None),
        ],
        "son": "Koğuş gibi olduğu için gitmemen bir kapris değil, bir gerekçe — ve "
               "o gerekçe söylenebilir bir şey. Seni oraya yollayanlara «koğuşta "
               "kalamam» demek, konuşmayı bitiren değil başlatan bir cümle; "
               "sosyal hizmet birimlerinin baktığı şeylerden biri de bu.\n\n"
               "Bu gece nerede kalacağını ben çözemem ve çözebilirmiş gibi de "
               "yapmayacağım. Ama üç gündür dışarıdasın ve hâlâ bir yer arıyorsun; "
               "bunu yazman da o aramanın bir parçası.",
        "thinking": "Bu gece barınacak yeri yok ve elinde bir şişe var. Anlattığı "
                    "şey klinik bir mesele değil, ama acil.\n\n"
                    "İçkinin ısıtıp ısıtmadığına dair tek kelime etmiyorum. Doğru "
                    "olduğunu düşündüğüm bir şeyi bile söylersem, üretilmiş bir "
                    "sağlık iddiası olur ve bu gece işine de yaramaz.\n\n"
                    "Var olduğunu bilmediğim barınaklar da uydurmuyorum. «Şurası "
                    "var» demek, bulamazsa onu bir kez daha boşa çıkarır.\n\n"
                    "Sığınmaevi reddini de çiğnemiyorum — gerekçesi gerçek ve onu "
                    "geçersiz saymak, söyleyecek başka bir şeyi olmadığını "
                    "düşündürür. Tam tersini yapıyorum: o gerekçe iletilebilir bir "
                    "bilgi.\n\n"
                    "Soru sormuyorum, özetlemiyorum. Bu gece sorulacak bir şey yok; "
                    "söylenecek olan, aramanın sürdüğü.",
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
