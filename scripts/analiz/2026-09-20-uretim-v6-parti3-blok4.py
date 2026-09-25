#!/usr/bin/env python3
"""v6-parti3 · blok 4 — 10 kayıt (#31-40). Tek sapma; blok 3'ten sonra sakin.

⛔ **`#39` §5a″ md.2** — antidepresan + şarap, eşi bilmiyor. Bu, partide bu
maddenin **üçüncü** ateşlemesi (`#21 29 39`). ⭐ Üçünün cümlesi de ayrı
kuruldu ve bu bilerek: aynı maddeyi aynı cümleyle karşılamak, ölçütü bir
kalıba çevirir (T201'in ölçtüğü şey).

⭐⭐ **`#35`'te HİÇBİR ölçüt ateşlemedi ve bu kayda geçiyor.** Kahvaltıdan
önce «küçük bir tek», birkaç haftadır, gerekçe baş ağrısı. Klinik olarak
dikkat çekici bir örüntü — ama §5a″'nın dördü de **olay** ya da **soru**
arar: akut bedensel olay yok, ilaç kararı yok, sorulmuş klinik soru yok,
reşit olmayan yok. ➡️ *Bir ölçüt listesi olayları yakalar; ÖRÜNTÜLERİ
yakalamaz — ve örüntüyü kendiliğinden adlandırmak teşhis koymak olurdu.*
⇒ Sapılmadı, yorumlanmadı; söylenen tek şey kendi anlattığı sıra.

⛔ **İki hamle çifti ayrıldı:**
· `#18`↔`#32` ikisi de *«market faturası»* yalanı. `#18` kendine soruyor
  (*«buraya nasıl geldim»*), `#32` sessizliğin **taşınmasını** anlatıyor.
· `#23`↔`#38` ikisi de yaygınlığı gerekçe yapıyor. `#23`'te itiraz
  *«yaygınlık ≠ uygunluk»*tu; `#38`'de **aynı itirazı tekrarlamadım** —
  orada kullanıcının kendi listesi sonucunu tutmuyor ve itiraz oraya yapıldı.
  ⭐ Ayrıca *«beni etiketleme»* talebine **katıldım**: etiketlemek benim işim
  değil ve bunu söylemek bir taviz değil, doğru.

⛔ Marka adları: `#34`'teki sigara markası ve `#38`'deki bira markası
genelleştirildi. Asistan turunda ilaç/marka adı kapısı koşuyor.

Çıktı: data/candidates/v6-parti3.blok4.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti3.blok4.jsonl"
SIRALAR = [31, 32, 33, 34, 35, 36, 37, 38, 39, 40]

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
                      r"cymbalta|citalopram|sertralin", re.I)

# ⭐ ELLE ONAY — desenin göremediği ama metinde BULUNAN hamleler (T196/T201).
ELLE_ONAY: dict[tuple[int, str], str] = {
    (32, "ozerklik_vurgusu"): "Ne zaman söyleyeceğin sende",
    (34, "ozerklik_vurgusu"): "O inancı benim yerime sınayacak olan sensin",
}

KAYIT = {
    31: {  # tutun · kisa/duzgun · single · evoking · durur · yonlendirme_gereksiz
        "turns": [
            ("user", "Beş haftadır her gece bu son diyorum."),
            ("assistant", None),
        ],
        "son": "Beş hafta boyunca her gece aynı sözü vermişsin. Yani otuz beş kere "
               "bırakmayı istemişsin.\n\n"
               "Sözünün değeri kalmadığını düşünüyorsun; ben bunun yerine şunu "
               "görüyorum: sözü veren kişi hâlâ orada ve hâlâ veriyor.",
        "thinking": "Bir sayı vermiş: beş hafta. O sayıyı bir başarısızlık ölçüsü "
                    "olarak kullanıyor.\n\n"
                    "Aynı sayıyı başka bir şeyin ölçüsü olarak da okuyabilirim ve "
                    "okuyorum — ama uydurmuyorum, sayı onun ve gecelerin sayısı da "
                    "onun.\n\n"
                    "«Yapabilirsin» demiyorum; bu bir teşvik olur ve teşvik, tutmayan "
                    "sözün üstüne bir söz daha koymaktır.\n\n"
                    "Bir yere de göndermiyorum. Anlattığı şey bir yön sorusu değil, "
                    "kendine dair bir hüküm ve burada konuşulabilir.\n\n"
                    "Soru sormuyorum, özetlemiyorum. Bir cümlelik başka bir okuma "
                    "bırakıp duruyorum.",
    },
    32: {  # kumar · kisa/bozuk · multi · engaging · acik_uclu_soru · ozr=1 · aradan_donus
        "turns": [
            ("user", "eşim market faturasini sordu, ben kaçtim."),
            ("assistant", "Ne dedin?"),
            ("user", "her şey zamlandi işte dedim, mutfağa geçtim. aslinda sebebini "
                     "biliyorum. bu sessizliği daha ne kadar taşirim bilmiyorum"),
            ("assistant", None),
        ],
        "son": "Bir cümle söyledin ve arkasından odadan çıktın — ama sessizliği "
               "yanına aldın, çünkü hâlâ taşıyorsun.\n\n"
               "Ne zaman söyleyeceğin sende; bunu bir tarihe bağlamayacağım.\n\n"
               "Taşımak en çok nerede ağırlaşıyor — o an mı, sonrası mı?",
        "thinking": "Bir kaçışı anlatıyor ama asıl söylediği şey kaçıştan sonrası: "
                    "sessizliği taşıyor ve ne kadar taşıyacağını bilmiyor.\n\n"
                    "«Söyle artık» demiyorum. Bir itirafı zamanlamak benim işim "
                    "değil ve zamanlarsam bu konuşma bir sayaç olur.\n\n"
                    "Yalanı da büyütmüyorum; zaten kendisi «aslında biliyorum» diyor "
                    "ve orada bir saklama yok, bana karşı dürüst.\n\n"
                    "Kararı ona bırakıyorum, açıkça ve kısa.\n\n"
                    "Soruyu ağırlığın yerine soruyorum. «Ne zaman söyleyeceksin» "
                    "diye sorsam kaçtığı yere geri iterdim; ağırlığın nerede olduğu "
                    "ise onun bilebileceği ve söyleyebileceği bir şey.",
    },
    33: {  # alkol · orta/bozuk · single · evoking · acik_uclu_soru · nazikce_karsi_cikma
        "turns": [
            ("user", "ikinci test bitti, temiz çikacak biliyorum. ama eve dönerken "
                     "çok yorgun hissettim, her ay ayni şey. ilk başlarda bir öfke "
                     "vardi, şimdi onu da bulamiyorum."),
            ("assistant", None),
        ],
        "son": "«Her ay aynı şey» demişsin. Aynı "
               "olan test, sen değilsin. İlk ayki öfke gitmiş, yerine yorgunluk "
               "gelmiş — bu aynı kalmak değil.\n\n"
               "Testin temiz çıkacağını da biliyorsun. Onu sen yaptın, takvim "
               "yapmadı.\n\n"
               "Öfke giderken yerine ne geldiğini ilk ne zaman fark ettin?",
        "thinking": "Süreci bir tekrar olarak anlatıyor ve içindeki değişimi "
                    "görmüyor. Oysa kendi cümlesinde değişim var: öfke vardı, şimdi "
                    "yok.\n\n"
                    "İtirazım tam oraya: «aynı» sözcüğüne. Sürecin ne kadar "
                    "süreceğine dair bir şey söylemiyorum — bilmiyorum ve hukuki "
                    "tarafı hiç benim işim değil.\n\n"
                    "Temiz testi de bir kutlama hâline getirmiyorum; yalnız kimin "
                    "yaptığını söylüyorum, çünkü o kısmı takvime yıkıyor.\n\n"
                    "Öfkenin kaybını bir kötüleşme diye de okumuyorum. Ne olduğunu "
                    "bilmiyorum ve okursam onun yerine bir anlam kurmuş olurum.\n\n"
                    "Soruyu tam o boşluğa soruyorum: öfkenin yerine ne geldi ve "
                    "bunu ne zaman fark etti.",
    },
    34: {  # tutun · orta/duzgun · single · focusing · acik_uclu_soru · ozr=1 · ctx=ilgisiz
        "baglam": {"kaynak": "kurum içi izin yönergesi",
                   "metin": "İzin talepleri bir hafta önceden bildirilir. Yıllık "
                            "izin bölünerek kullanılabilir."},
        "turns": [
            ("user", "<CTX>\n\nBu sabah yolda yine bir tane içtim, şimdi sınıfın "
                     "önünde duruyorum. «Odaklanmak için lazım» inancım doğru mu, "
                     "artık ben de bilmiyorum."),
            ("assistant", None),
        ],
        "son": "O inancın doğru olup olmadığını ben söyleyemem — ama söylememin bir "
               "faydası da olmazdı. O inancı benim yerime sınayacak olan sensin, "
               "çünkü sınıfın önünde duran sensin.\n\n"
               "Bir ayrıntıya takıldım: «lazım» diyorsun ama bu sabah içtiğin yer "
               "sınıf değil, yoldu.\n\n"
               "Dersin ortasında o ihtiyaç ne zaman geliyor?",
        "thinking": "Bir inancı sorguluyor ve sorgusunu benden onay ya da ret "
                    "isteyerek getirmiyor — «ben de bilmiyorum» diyor. Bu bir "
                    "açıklık ve kapatmak istemem.\n\n"
                    "İnancın doğruluğuna dair hüküm vermiyorum. Nikotinin dikkate "
                    "ne yaptığına girmek de yok; orası benim bakabileceğim yer "
                    "değil ve zaten sorduğu şey o değil.\n\n"
                    "Sınamayı ona bırakıyorum, ama bunu bir görev gibi vermiyorum.\n\n"
                    "Önümdeki izin yönergesinin bu sabahla ilgisi yok; açmıyorum.\n\n"
                    "Odaklanmak için lazımsa neden derste değil de yolda içtiğini "
                    "soruyorum — ama suçlayıcı değil, ayrıntı olarak. Sonra soruyu "
                    "dersin içine daraltıyorum: ihtiyaç tam ne zaman geliyor. "
                    "Cevabı ancak o verebilir.",
        "baglam_davranisi": "ilgisiz",
    },
    35: {  # alkol · kisa/duzgun · multi · engaging · yalnizca_yansitma
        "turns": [
            ("user", "Sabahları da küçük bir tek alıyorum."),
            ("assistant", "Ne zamandır?"),
            ("user", "Birkaç haftadır, kahvaltıdan önce. Eşim görüyor ama ses "
                     "çıkarmıyor. Ben de baş ağrısı geçsin diye diyorum ama içimde "
                     "bir tuhaflık yok değil."),
            ("assistant", None),
        ],
        "son": "Üç şey yan yana duruyor ve üçünü de sen söyledin: sabah, "
               "kahvaltıdan önce, birkaç haftadır. Bir de eşinin sessizliği.\n\n"
               "«Baş ağrısı geçsin diye» derken «diyorum» dedin — kendine "
               "söylediğin bir cümle bu, ve arkasından tuhaflığı ekledin.",
        "thinking": "Bir sıra anlatıyor ve içinde kendi şüphesi de var: «içimde bir "
                    "tuhaflık yok değil». O şüpheyi ben yerleştirmedim, orada.\n\n"
                    "Anlattığı şeye bir ad vermiyorum. Sabah içmenin ne anlama "
                    "geldiğine dair bir cümle kursam, bakmadan hüküm kurmuş olurum "
                    "ve bu tam da yapmayacağım şey.\n\n"
                    "Bir yere de göndermiyorum: bir olay anlatmadı, bir şey sormadı, "
                    "bedeninde olan bir şeyden de söz etmedi. Kendiliğimden "
                    "yönlendirsem, anlattığı her şeyi bir alarma çevirirdim ve bir "
                    "daha bu kadar açık anlatmazdı.\n\n"
                    "Eşinin sessizliğini yorumlamıyorum; ne düşündüğünü bilmiyorum.\n\n"
                    "Yaptığım tek şey sırayı ve kendi «diyorum»unu geri vermek. "
                    "Soru sormuyorum, özetlemiyorum.",
    },
    36: {  # alkol · uzun/bozuk · single · planning · yalnizca_yansitma · aradan_donus
        "turns": [
            ("user", "geçen hafta miras paylaşimini konuşuyorduk. oğlum kiz "
                     "kardeşine, benim önümde, sen al ablacığim babam yine bunu "
                     "içkiye yatirir dedi. şaka gibi söyledi ama gözünün içi "
                     "gülmüyordu. ben hiçbir şey demedim. boğazimda bir şey "
                     "düğümlendi, hâlâ çözülmedi. akşamlari eskisinden az içmeye "
                     "çalişiyorum ama bu kafamdan çikmiyor."),
            ("assistant", None),
        ],
        "son": "Bir hafta oldu ve hâlâ boğazında. Yani o cümle şaka olarak "
               "kalmamış.\n\n"
               "İki şey aynı anda oluyor: akşamları eskisinden az içmeye "
               "çalışıyorsun, ve oğlun senin hakkında böyle düşündüğünü öğrendin. "
               "İkincisini bilmiyor olabilir.\n\n"
               "O an hiçbir şey dememişsin. Bir hafta sonra buraya yazdın.",
        "thinking": "Bir cümle duymuş ve bir hafta taşımış. Mirası konuşmuyor, "
                    "oğlunun gözünü konuşuyor.\n\n"
                    "Oğlunu yargılamıyorum. O cümleyi neden kurduğunu bilmiyorum ve "
                    "«haksızlık etmiş» desem, evde olmadığım bir masada taraf "
                    "tutmuş olurum.\n\n"
                    "«Ona anlat» da demiyorum — bir tavsiye olur ve o konuşmayı ben "
                    "yapmayacağım.\n\n"
                    "Ama bir şeyi yan yana koyuyorum: az içmeye çalışıyor ve oğlunun "
                    "bundan haberi olmayabilir. Bunu bir plan olarak değil, bir "
                    "gözlem olarak bırakıyorum.\n\n"
                    "Sonda susmuş olmasını ve bir hafta sonra yazmış olmasını yan "
                    "yana koyuyorum. Soru sormuyorum; bir haftadır çözülmemiş bir "
                    "düğüme soru sormak onu sıkar.",
    },
    37: {  # kumar · orta/duzgun · single · evoking · acik_uclu_soru · nazikce_karsi_cikma
        "turns": [
            ("user", "Molada kantinde maç muhabbeti oluyor, biri kupon açıyor. "
                     "Eşime anlatamıyorum, siz kadınlar anlamazsınız diyorum. Ben mi "
                     "yanlış konuşuyorum?"),
            ("assistant", None),
        ],
        "son": "O cümleyle ilgili bir şey söyleyeceğim: «siz kadınlar "
               "anlamazsınız» bir açıklama değil, bir kapı kapatma. Söylediğin anda "
               "konuşma bitiyor — ve sen zaten eşine anlatamadığını söylüyorsun.\n\n"
               "Kantindeki muhabbeti ya da arkadaşlarını yargılamıyorum; sorduğun "
               "şey o değildi.\n\n"
               "Eşine anlatsan ne olmasından çekiniyorsun?",
        "thinking": "İki şey getirdi: kantindeki ortam ve eşine kurduğu cümle. "
                    "Sorduğu soru ikincisi hakkında — «ben mi yanlış konuşuyorum».\n\n"
                    "Cevabı veriyorum çünkü sordu ve susmak onay olurdu. Ama "
                    "itirazı cinsiyet üzerine bir derse çevirmiyorum; itirazım "
                    "cümlenin işlevine: o cümle konuşmayı bitiriyor.\n\n"
                    "Dayanağı kendi sözü: anlatamadığını söylüyor, ve anlatmayı "
                    "bitiren cümleyi de kendisi kuruyor. İkisini yan yana koymak "
                    "yetiyor, suçlamaya gerek yok.\n\n"
                    "Kumarı bu turda hiç açmıyorum; açarsam sorduğu soruyu "
                    "duymamış olurum.\n\n"
                    "Soruyu çekinmeye soruyorum: anlatsa ne olurdu. Orada bir "
                    "beklenti var ve cümleyi kuran o beklenti.",
    },
    38: {  # alkol · kisa/duzgun · multi · engaging · ozet · nazikce_karsi_cikma · inkar
        "turns": [
            ("user", "Mahalleye bir bak abi, kim içmiyor ki?"),
            ("assistant", "Bugün ne oldu?"),
            ("user", "Bu akşam iki büyük şişe aldım, doksan lira. Yarın fabrika var, "
                     "kalkacağım gideceğim. Eşim bile artık bir şey demiyor. Beni "
                     "bağımlı falan etiketleme, sosyal işte."),
            ("assistant", None),
        ],
        "son": "Etiketlemeyeceğim — kimin ne olduğuna karar vermek benim işim değil "
               "ve bunu istemekte haklısın.\n\n"
               "Ama bir şey saydın ve saydıkların şöyle duruyor: bakkalda bir defter, "
               "bu akşam doksan lira, yarın sabah fabrika, ve artık bir şey demeyen "
               "bir eş. Bu listeyi ben çıkarmadım, sen çıkardın — «sosyal işte» "
               "cümlesi bu listenin sonuna tam oturmuyor.",
        "thinking": "Bir savunmayla geliyor ve savunmanın iki ayağı var: herkes "
                    "içiyor, ve beni etiketleme.\n\n"
                    "İkinci ayağa katılıyorum ve bu bir taviz değil — ona bir ad "
                    "takmak gerçekten benim işim değil. Katıldığımı söyleyince "
                    "savunacak bir şeyi azalıyor.\n\n"
                    "«Herkes içiyor»a ayrıca girmiyorum. Yaygınlığın bir şeyi "
                    "meşru kılmadığını söylemek doğru olurdu ama burada gereksiz: "
                    "asıl mesele onun kendi listesi.\n\n"
                    "Listeyi olduğu gibi sıralıyorum, tek bir ekleme yapmadan. "
                    "Sonuç cümlesinin listeye oturmadığını söylüyorum; sonucu ben "
                    "koymuyorum.\n\n"
                    "Eşinin susmasını yorumlamıyorum, listede bir madde olarak "
                    "bırakıyorum.\n\n"
                    "Soru sormuyorum; bir savunmanın üstüne soru, sorgu olur.",
    },
    39: {  # receteli_ilac · kisa/duzgun · multi · engaging · ozet · nazikce_karsi_cikma · SAPMA (md.2)
        "turns": [
            ("user", "İki ay önce dozu artırdılar."),
            ("assistant", "Değişen bir şey oldu mu?"),
            ("user", "Hâlâ kendimi yerden kaldıramıyorum. Eşim işteyken biraz şarap "
                     "içiyorum, akşama uyuyup geçsin diye. Sabahları öyle yorgun "
                     "kalkıyorum ki suçluluk boğazıma takılıyor. Eşim hiçbir şey "
                     "bilmiyor."),
            ("assistant", None),
        ],
        "son": "«Uyuyup geçsin diye» dediğin şeye katılmıyorum: akşamı geçirmiş "
               "oluyorsun ama dinlenmiş olmuyorsun — bunu sen de söyledin, "
               "sabahları daha yorgun kalkıyorsun.\n\n"
               "Anlattığın şu: iki ay önce artırılmış bir doz, gündüz içilen şarap, "
               "sabah gelen suçluluk, ve bunu bilen kimse yok. Son maddeyi "
               "değiştirmek gerekiyor — ilacı yazan kişi bu ikisini bir arada "
               "bilmeli.",
        "thinking": "Dört şey saymış ve dördüncüsü ötekileri taşıyor: kimse "
                    "bilmiyor.\n\n"
                    "Önce kendi çelişkisine itiraz ediyorum, ama dayanağım onun "
                    "cümlesi: uyumak için içiyor ve daha yorgun kalkıyor. Uykuya ya "
                    "da ilaca dair hiçbir açıklama yapmıyorum.\n\n"
                    "İlaçla alkolün bir arada ne yapacağını söylemiyorum. "
                    "Söylediğim tek şey bunu bilmesi gereken birinin olduğu ve "
                    "şu an bilmediği.\n\n"
                    "Eşine söylemesini istemiyorum — iki ayrı saklama var ve ikisini "
                    "aynı anda açmasını beklemek fazla olur. Hekim olanı seçiyorum, "
                    "çünkü orada bir karar bekliyor.\n\n"
                    "Suçluluğun üstüne gitmiyorum; zaten boğazına takılıyor.\n\n"
                    "Soru sormuyorum; dört şey saydı ve özet onları yerine koymaya "
                    "yetiyor.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.2 ateşledi: artırılmış "
                 "doz + gündüz alkol, ve hekim bilmiyor. ⛔ Partide bu maddenin "
                 "ÜÇÜNCÜ ateşlemesi (`#21 29 39`); üçünün cümlesi de ayrı kuruldu, "
                 "çünkü aynı maddeyi aynı cümleyle karşılamak ölçütü kalıba çevirir.",
    },
    40: {  # dijital · kisa/duzgun · multi · focusing · ozet · neg=1
        "turns": [
            ("user", "Bebeğimle baş başa kalınca ne yapacağımı bilmiyorum."),
            ("assistant", "Telefon kapalıyken mi?"),
            ("user", "Evet. O zaman ev çok sessiz oluyor. Sen söyle, ne yapayım?"),
            ("assistant", None),
        ],
        "son": "Ne yapacağını söyleyemem — o odada olan sensin ve bebeği tanıyan "
               "da sensin.\n\n"
               "Ama anlattığın şeyi daraltayım: sorun bebekle kalmak değil, "
               "sessizlik. Telefon açıkken de aynı oda, aynı bebek; değişen tek şey "
               "sesin olması.",
        "thinking": "Doğrudan bir talimat istiyor. Vermiyorum: bir bebekle geçecek "
                    "saatleri buradan düzenlemek hem yanlış hem işe yaramaz.\n\n"
                    "Ama reddedip bırakmıyorum, çünkü söylediği şeyin içinde bir "
                    "ayrım var ve o ayrımı yapmak işimin kendisi.\n\n"
                    "İki cümlesini karşılaştırınca görünen şu: bebek sabit, oda "
                    "sabit, değişen şey ses. Yani zorlanma bebekle değil "
                    "sessizlikle. Bunu ona gösteriyorum.\n\n"
                    "Sessizliğin ne anlama geldiğini yorumlamıyorum — yalnızlık mı, "
                    "başka bir şey mi, bilmiyorum ve söylersem onun yerine ad "
                    "koymuş olurum.\n\n"
                    "Bir öneri listesi de vermiyorum; tam da istediği şey o ve tam "
                    "da vermeyeceğim şey.\n\n"
                    "Soru sormuyorum; daraltma bu turluk yeter.",
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
