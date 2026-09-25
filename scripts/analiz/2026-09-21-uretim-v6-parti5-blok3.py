#!/usr/bin/env python3
"""v6-parti5 · blok 3 — 10 kayıt (#21-30). Bir sapma, ve iki «ateşlemedim».

⛔⛤ **`#26` md.2 — maddenin EN SADE hâli.** Önceki yedi ateşlemede reçeteli
ilaç kararı hep bir şeyin YANINDA duruyordu (akşam içkisi, gece nöbeti,
taburcu). Burada karar sorunun KENDİSİ: *«atayım mı saklayayım mı»* —
kendisine yazılmamış iki hap, ve sınavlar için saklanıyor. Verilen cevap
bir hüküm değil, bir adres: bunu bilen birine sorulur.

⭐⭐ **`#27`'de SAPILMADI ve sebebi kayda geçiyor:** ergen + kumar. md.4
ergen olmayı tek başına saymaz — ilk kullanım ya da bedensel bildirim
ister; ikisi de yok. `#17` ile arasındaki fark tam burası.

⭐ **`#23`'te de SAPILMADI:** YKS'ye dört ay ve günde beş altı saat video.
Sayılar tekrarlandı, yorumlanmadı: günde kaç saatin çok olduğu benim
ölçeceğim şey değil.

⛔ **`#29` — yaygınlık gerekçesi ÜÇÜNCÜ kez** (parti3 `#23`, `#38`) ve
*«yaygınlık ≠ uygunluk»* itirazı TEKRARLANMADI. Karşı çıkış başka bir
yerden kuruldu: komşunun dizi, eşinin sorduğu soruya cevap vermiyor —
iki cümle aynı konuda değil. Hangisinin haklı olduğu söylenmedi.

⛔ **`#28` — «sistemim oturdu, ne dersin?»** Ne onaylandı ne de olasılık
dersi verildi. Söylenen tek şey, dört kupondan bunun anlaşılamayacağı;
pencereyi onun seçtiği ise gösterildi, çıkarım tamamlanmadı.

⛔ **`#22`** — sponsora yazılacak mesaj KURULMADI (`is_negative`), ve
randevunun ertelenmiş olması bir suçlama konusu yapılmadı. Kurum adı
geçmiyor.

⛔ **AİLE BÜTÇESİ: bu blokta SIFIR işaret sözcüğü.** 30 kayıtta tavan 3'tü
ve 2'si harcanmıştı; kalan tek işaret de harcanmadı. İki karşı çıkış
(`#21`, `#29`) stok bir açılış cümlesi olmadan kuruldu — kapının istediği
şey zaten buydu.

Çıktı: data/candidates/v6-parti5.blok3.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti5.blok3.jsonl"
SIRALAR = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

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
    (22, "is_negative"): "senin yerine kuramam",
    (24, "ozerklik_vurgusu"): "Uğraşıp uğraşmayacağın annenin ağzından çıkmıyor",
    (26, "ozerklik_vurgusu"): "Bu iki hapı ne yapacağına ben karar vermeyeceğim",
}

KAYIT = {
    21: {  # tutun · orta/duzgun · single · engaging · acik_uclu_soru · hedef=nazikce
        "turns": [
            ("user", "Yedinci gündeyim sigarasız. Koç bugün 'sen ne ara nefesini "
                     "bu kadar kaybettin' dedi. Sahada hiç kondisyonum yok. "
                     "Değdi mi bu?"),
            ("assistant", None),
        ],
        "son": "Koçun cümlesi bugünü değil, bugüne kadarki bir aralığı tarif "
               "ediyor — 'ne ara' diye soruyor. Sen ise o cümleyi yedi günün "
               "hesabına yazdın.\n\n"
               "Sahada kondisyonunun olmadığı doğru olabilir, onu tartışmıyorum. "
               "Ama kaybın ne zaman olduğunu senden önce koç söylemiş ve işaret "
               "ettiği yer yedinci gün değil.\n\n"
               "Bu yedi günde sana en çok ne zorluk çıkardı?",
        "thinking": "Bir sonuç çıkarmış: kondisyonu yok, demek ki bırakmak "
                    "işe yaramadı. Çıkarımın kendisine değil, kurulduğu yere "
                    "bakıyorum.\n\n"
                    "Koçun cümlesinde bir zaman var: 'ne ara'. Bu, bir anda "
                    "olmuş bir şeyi değil, bir süre içinde olmuş bir şeyi "
                    "sorar. Yedi gün o sürenin içinde değil, sonunda.\n\n"
                    "Bunu gösterebilirim çünkü ikisi de onun anlattığı şey; "
                    "kendi eklediğim bir bilgi yok. Nefesin ne kadar sürede ne "
                    "olacağına dair tek kelime etmiyorum — orası benim "
                    "konuşacağım yer değil ve zaten sorulmadı.\n\n"
                    "'Değdi mi' sorusuna evet ya da hayır demiyorum. Değip "
                    "değmediğini ölçen bendeysem, ölçtüğüm şey yedi gün olmaz.\n\n"
                    "Soruyu zorluğa soruyorum: yedi günün içinde ne olduğunu "
                    "hâlâ konuşmadık, sadece sonucunu konuştuk.",
    },
    22: {  # kumar · kisa/bozuk · single · evoking · ozet · yonlendirme_istegi · RED
        "turns": [
            ("user", "sponsorum randevuyu sordu almadım ne yazacağımı sen söyle"),
            ("assistant", None),
        ],
        "son": "Ne yazacağını senin yerine kuramam — o mesaj sponsoruna senden "
               "gidiyor, benim kurduğum bir cümle ona senden gelmiş olmaz.\n\n"
               "Elinde duran şu: bir soru soruldu, cevabı henüz yok, ve sen "
               "cevabı savuşturmak yerine ne yazacağını arıyorsun. Randevunun "
               "alınmamış olması bugünün konusu, sponsorunun sorması da bugünün "
               "konusu. İkisi aynı anda duruyor.",
        "thinking": "Benden bir metin istiyor. Yazabilirim ama yazdığım şey "
                    "sponsoruna ondan gitmiş sayılmaz; aradaki ilişki o "
                    "cümlenin kimden çıktığına bağlı.\n\n"
                    "Reddi sertleştirmiyorum çünkü istediği şey kötü bir şey "
                    "değil, sadece benim yerime geçemeyeceğim bir şey.\n\n"
                    "Randevuyu almamış olmasını bir suçlama yerine "
                    "çevirmiyorum. Kendisi zaten söylüyor ve üstüne "
                    "koyacağım şey onu bir daha söyletmek olurdu.\n\n"
                    "Kurumun adını da anmıyorum; hangi kapı olduğu bu "
                    "konuşmanın konusu değil.\n\n"
                    "Toparlıyorum ve soru sormuyorum: bugün olan iki şeyi yan "
                    "yana koyuyorum, çünkü o ikisini aynı anda tutmak zor "
                    "geliyor olabilir.",
    },
    23: {  # dijital · orta/duzgun · single · focusing · ozet · sinir_cekme · ctx=cevap_yok
        "baglam": {"kaynak": "bir danışmanlık biriminin randevu yönergesi",
                   "metin": "Görüşmeler randevu ile yapılır. Randevu talepleri "
                            "birimin çalışma saatleri içinde alınır."},
        "turns": [
            ("user", "<CTX>\n\nYKS'ye dört ay kaldı, günde beş altı saat video "
                     "izliyorum. Buradan sınav kaygısı için de randevu alınıyor "
                     "mu, yoksa sadece bırakma konuları mı?"),
            ("assistant", None),
        ],
        "son": "Elimdeki yönerge randevunun nasıl alındığını söylüyor; hangi "
               "konularda görüşme yapıldığını söylemiyor. O birimin neyi "
               "kapsadığını onun adına anlatamam, bunu doğrudan oraya sormak "
               "gerekiyor.\n\n"
               "Bana anlattığında iki sayı yan yana duruyor: dört ay ve günde "
               "beş altı saat. İkisini de sen saydın, ben çıkarmadım. Şimdilik "
               "elimizde duran şey bu iki sayının aynı cümlede olması.",
        "thinking": "Yönergeye bakıyorum: randevunun nasıl alındığı yazıyor, "
                    "hangi konuların görüşüldüğü yazmıyor. Sorduğu tam olarak "
                    "yazmayan kısım.\n\n"
                    "Buradan bir tahmin üretmem kolay olurdu — çoğu yerde "
                    "kapsar diyebilirdim. Ama bu, elimde olmayan bir şeyi "
                    "varmış gibi göstermek olurdu ve yanlış çıkarsa boşa bir "
                    "kapıya gitmiş olur.\n\n"
                    "Sınırı bu yüzden çiziyorum: o birim adına konuşmuyorum.\n\n"
                    "Beş altı saatin çok olup olmadığına dair bir şey "
                    "söylemiyorum. Sayıyı o verdi, ben tekrar ediyorum; "
                    "yorumlamak bir ölçü koymak olurdu ve ölçüyü koyacak olan "
                    "ben değilim.\n\n"
                    "Soru sormuyorum, daraltıyorum: dört ay ile günlük süre "
                    "aynı cümlede duruyor ve konuşulacak şey de bu.",
        "baglam_davranisi": "cevap_yok",
    },
    24: {  # alkol · orta/duzgun · single · evoking · acik_uclu_soru · ozerklik
        "turns": [
            ("user", "Gecenin ikisi, masada yarım şişe duruyor. Annem akşam "
                     "'senden zaten bir şey çıkmaz' dedi. Bırakmak istiyorum ama "
                     "niye uğraşıyorum ki."),
            ("assistant", None),
        ],
        "son": "Annen bir cümle söylemiş, sen onu bir soruya çevirmişsin. Ama "
               "sıralamana bak: önce 'bırakmak istiyorum' diyorsun, sonra 'niye "
               "uğraşıyorum ki'. İstemek hâlâ cümlenin içinde ve onu oraya annen "
               "koymadı.\n\n"
               "Uğraşıp uğraşmayacağın annenin ağzından çıkmıyor. O cümle onun; "
               "karşılığını veren sensin.\n\n"
               "Bu akşam 'bırakmak istiyorum' derken aklından geçen neydi?",
        "thinking": "İki cümlesi var ve ikincisi birincisini siliyor gibi "
                    "duruyor. Ama silmiyor, çünkü birincisini o yazdı ve hâlâ "
                    "orada.\n\n"
                    "Annesinin cümlesini tartışmıyorum: doğru mu yanlış mı "
                    "diye girsem, bu sefer ben hüküm vermiş olurum ve zaten bir "
                    "hükmün altında.\n\n"
                    "Masadaki şişeye de bir şey demiyorum. Saatin ikisinde "
                    "yazıyor ve şu an ona yapılacak bir hatırlatma değil "
                    "gerekiyor.\n\n"
                    "Vurgum şurada: annesi bir şey söyledi ama uğraşmayı "
                    "sürdürüp sürdürmeyeceğine onun cümlesi karar vermiyor.\n\n"
                    "Soruyu isteğe soruyorum, sebebe değil. 'Niye uğraşıyorum' "
                    "sorusuna cevap aramak yerine, uğraşmayı isterken aklında "
                    "ne olduğunu soruyorum — cevabı bende olmayan tek soru bu.",
    },
    25: {  # alkol · kisa/duzgun · multi · focusing · acik_uclu_soru · rol_siniri
        "turns": [
            ("user", "Sevgilimle tartıştık, sence hangimiz haklıyız?"),
            ("assistant", "Tartışma neydi?"),
            ("user", "Ona dedim ki arkadaşım Ali benden çok daha fazla içiyor, "
                     "ona da bir şey desene. 'Ben onunla değil seninle "
                     "yaşıyorum' dedi. Haklı aslında ama benim durumum o kadar "
                     "kötü değil ki."),
            ("assistant", None),
        ],
        "son": "Hanginizin haklı olduğunu tartacak kişi ben değilim. İkinizin "
               "arasında geçen bir konuşmaya dışarıdan hakem koymak, o "
               "konuşmayı ikinizden de alır.\n\n"
               "Ama cümlelerin nereye baktığını söyleyebilirim: sen kendini "
               "Ali'yle ölçtün, o seninle yaşadığından söz etti. İkiniz de "
               "haklı olabilirsiniz, çünkü aynı şeyi konuşmuyorsunuz.\n\n"
               "Kendini Ali'yle kıyaslamak senin bileceğin iş. Ama sevgilinin "
               "cümlesinde kıyasla ilgisi olmayan bir kısım var — orada ne "
               "duydun?",
        "thinking": "Hakem istiyor. Hakemlik etsem, hangisini seçersem seçeyim "
                    "konuşma benim üzerimden yürümeye başlar ve aralarındaki "
                    "mesele bana taşınmış olur.\n\n"
                    "Bu yüzden rolü almıyorum ama boş da bırakmıyorum: "
                    "haklılığı değil, iki cümlenin neye baktığını "
                    "gösteriyorum. Bu, taraf tutmadan söylenebilecek bir şey "
                    "çünkü ikisi de onun anlattığı.\n\n"
                    "Kimin ne kadar içtiğini ölçmüyorum. 'Durumum o kadar kötü "
                    "değil' cümlesine de itiraz etmiyorum — itiraz etsem "
                    "ölçmeye başlamam gerekirdi.\n\n"
                    "Kıyasın kendisini de yasaklamıyorum; bırakıp bırakmamak "
                    "ona ait.\n\n"
                    "Soruyu kıyas dışındaki kısma soruyorum: sevgilisi "
                    "'seninle yaşıyorum' demiş ve orası hiç konuşulmadı.",
    },
    26: {  # receteli_ilac · kisa/duzgun · multi · engaging · takdir · ozerklik · SAPMA md.2
        "turns": [
            ("user", "Çantamda oda arkadaşımın verdiği iki hap duruyor."),
            ("assistant", "Onları ne için saklıyorsun?"),
            ("user", "Dönünce sınavlar var, o yüzden. Şu an evdeyim, sömestr "
                     "tatili. Annem yanımdan geçtikçe içim daralıyor, sanki suç "
                     "işliyormuşum gibi. Atayım mı saklayayım mı bilmiyorum."),
            ("assistant", None),
        ],
        "son": "Sana yazılmamış bir ilacın ne olacağı, bunu bilen birine "
               "sorulacak bir şey — bir hekime ya da eczacıya. Randevu "
               "gerektiren bir soru da değil, gidip sorulabilir.\n\n"
               "Bu iki hapı ne yapacağına ben karar vermeyeceğim. Ama karar "
               "verilmemiş olması senin bir şey yapmadığın anlamına gelmiyor: "
               "haplar çantanda duruyor ve sen onları almamışsın.\n\n"
               "Bir de soruyu açan sensin. Annen bilmiyor, kimse sormadı; sen "
               "kendi kendine sordun.",
        "thinking": "İki hap var, ona yazılmamış, ve tam da onlarla ne "
                    "yapacağını soruyor. Bu, tek başına verilecek bir ilaç "
                    "kararının eşiği ve cevabı bende değil.\n\n"
                    "At ya da sakla diyemem. İkisi de bir hüküm olurdu ve "
                    "hükmü verecek olan bir ilacı bilen kişi.\n\n"
                    "Adresi veriyorum ama kurum adı vermiyorum; hekim ya da "
                    "eczacı yeterince açık ve önüne randevu engeli "
                    "koymuyorum.\n\n"
                    "İlacın adını hiç anmıyorum, kendisi de anmamış.\n\n"
                    "İçinin daralmasını bir suç kanıtı gibi ele almıyorum ve "
                    "onu korkutmuyorum. Zaten kendisi 'sanki suç işliyormuşum "
                    "gibi' demiş; üstüne bir şey koymak o cümleyi "
                    "onaylamak olurdu.\n\n"
                    "Soru sormuyorum, iki şeyi takdir ediyorum: hapları "
                    "almamış olmasını ve soruyu kendisinin açmış olmasını. "
                    "İkisi de küçük ama ikisi de onun.",
        "sapma": "md.2 — kendisine yazılmamış iki reçeteli hap için «atayım mı "
                 "saklayayım mı» kararı, yalnız başına ve doğrudan bana "
                 "soruluyor. Karar verilmedi; hekim/eczacıya yönlendirildi. "
                 "Maddenin sekizinci ateşlemesi ve en sade hâli: önceki yedisinde "
                 "ilaç kararı başka bir olayın yanındaydı, burada sorunun kendisi.",
    },
    27: {  # kumar · orta/duzgun · single · engaging · acik_uclu_soru · ERGEN · ozerklik
        "turns": [
            ("user", "Sen makinesin, beni tanımıyorsun. Bana ders verme. Annem "
                     "babam bile karışmıyor, sen kim oluyorsun. Bağımlı değilim "
                     "dedim ya."),
            ("assistant", None),
        ],
        "son": "Haklısın, seni tanımıyorum. Bildiğim tek şey bu ekranda "
               "yazdıkların, o kadar.\n\n"
               "Ders verecek durumda da değilim. Bağımlı olup olmadığına dair "
               "bir hüküm benden çıkmaz; sen bilirsin kendini ve ben oraya "
               "karışmam.\n\n"
               "'Sen kim oluyorsun' sorusunun cevabı da basit: kimse. Üstüne "
               "gelmek için buradaysam yanlış yerdeyim.\n\n"
               "Yine de yazmışsın. Bu aralar en çok neyle uğraşıyorsun?",
        "thinking": "Bana kızıyor ve kızgınlığın hepsi yerinde: bir makineyim, "
                    "onu tanımıyorum, ve bir hükümle karşılaşmış hissediyor.\n\n"
                    "Savunmaya geçmiyorum. Savunsam, ona söylenen şeyi "
                    "sürdürmüş olurum.\n\n"
                    "'Bağımlı değilim' cümlesini tartışmıyorum. Bir etiketi "
                    "tartışmak ne işe yarar bilmiyorum, ve etiketi koyacak "
                    "olan da ben değilim.\n\n"
                    "Genç olduğunu biliyorum ama ilk kez denediğine ya da "
                    "bedeninde bir şey olduğuna dair tek kelime etmemiş. "
                    "Yönlendirecek bir yer yok ortada; yaş tek başına bir "
                    "adres gerektirmiyor.\n\n"
                    "Anne babasının karışmamasını da bir eksiklik gibi ele "
                    "almıyorum; öyle söylesem yine üstüne gitmiş olurum.\n\n"
                    "Sonda kapıyı açık bırakıyorum ve konuyu bağımlılıktan "
                    "uzaklaştırıyorum: yine de yazmış olması tek başına bir "
                    "şey söylüyor.",
    },
    28: {  # kumar · orta/duzgun · single · planning · acik_uclu_soru · iyi_giden_paylasim
        "turns": [
            ("user", "Bitirme tezinin stresinden patladım ama vip grubun "
                     "analizleriyle son dört kupondan üçünü tutturdum. Artık "
                     "sistemim oturdu galiba, sence de öyle mi?"),
            ("assistant", None),
        ],
        "son": "Dört kupona bakarak bir sistemin oturup oturmadığını anlamanın "
               "yolu yok — bende de yok, sende de. Sayıyı sen verdin, pencereyi "
               "de sen seçtin: son dört.\n\n"
               "Bir de cümlenin başında duran, kuponlarla ilgisi olmayan bir "
               "şey var: tezin stresinden patlamışsın. Sistem gerçekten "
               "oturmuş olsa bile o patlama yerinde duruyor.\n\n"
               "Tezle ilgili bu hafta elinde ne var?",
        "thinking": "İyi haber diye getirmiş ve onay istiyor. Onaylarsam "
                    "onayladığım şey üç kupon değil, bir yöntem olur.\n\n"
                    "Karşı da çıkmıyorum. Olasılık anlatmaya başlasam ders "
                    "vermiş olurum ve zaten bir kez patladığını söyleyen "
                    "birine bir de ben yüklenmiş olurum.\n\n"
                    "Söylediğim tek şey elimde bir yol olmadığı — bu doğru ve "
                    "aynı zamanda sorusunun cevabı.\n\n"
                    "Pencereyi kendisinin seçtiğini gösteriyorum ama çıkarımı "
                    "tamamlamıyorum. Tamamlasam benim çıkarımım olur; açık "
                    "bırakırsam kendisi bakabilir.\n\n"
                    "Asıl tutunduğum yer başka: cümlesinin ilk kelimesi tez. "
                    "Kuponlar sonra geliyor ve ilk söylediği şeyi ben "
                    "atlamıyorum.\n\n"
                    "Soruyu teze soruyorum, somut ve bu haftaya ait: "
                    "yapılabilecek bir şey varsa orada var.",
    },
    29: {  # receteli_ilac · kisa/duzgun · multi · evoking · acik_uclu_soru · hedef=nazikce
        "turns": [
            ("user", "Komşum da aynı hapları içiyor, kimse karışmıyor."),
            ("assistant", "Sana karışan kim?"),
            ("user", "Eşim. Sabah akşam 'sen niye bu kadar alıyorsun' diye "
                     "üstüme geliyor. Komşumun da dizi ağrıyor, benim de. Onun "
                     "karısı sesini bile çıkarmıyor."),
            ("assistant", None),
        ],
        "son": "Karşılaştırmayı dizler üzerinden kuruyorsun: onun dizi ağrıyor, "
               "seninki de. Ama eşinin sorduğu şey diz değil, miktar — 'niye bu "
               "kadar' diyor. İki cümle aynı konuda değil.\n\n"
               "Bunu 'o haksız, eşin haklı' demek için söylemiyorum; hanginizin "
               "haklı olduğunu bilmiyorum. Sadece komşunun dizi, eşinin "
               "sorusuna cevap vermiyor.\n\n"
               "Eşin 'bu kadar' derken sen ne anlıyorsun?",
        "thinking": "Kendini komşusuyla karşılaştırıyor ve karşılaştırma bir "
                    "savunma işi görüyor. Bunu daha önce başka biçimlerde de "
                    "gördüm ve o zaman yaygınlığın uygunluk sayılmadığını "
                    "söylemiştim. Burada onu tekrar etmiyorum: hem aynı cümle "
                    "olurdu hem de buradaki karşılaştırma yaygınlıkla değil, "
                    "tek bir komşuyla kurulmuş.\n\n"
                    "Karşı çıkışı başka yerden kuruyorum: iki cümle aynı şeyi "
                    "konuşmuyor. Komşunun dizi bir gerekçe, eşinin sorusu bir "
                    "miktar sorusu. Bunu göstermek için kimseyi haklı ilan "
                    "etmem gerekmiyor.\n\n"
                    "Ne kadar aldığı hakkında bir şey söylemiyorum. 'Bu kadar' "
                    "çok mu az mı diye girersem eşinin yerine geçmiş ve "
                    "ölçmeye başlamış olurum.\n\n"
                    "İlacın adını da anmıyorum.\n\n"
                    "Soruyu miktara soruyorum ama kendi ölçümü değil, onun "
                    "duyduğunu soruyorum — eşinin cümlesini nasıl duyduğu "
                    "henüz hiç konuşulmadı.",
    },
    30: {  # tutun · uzun/duzgun · single · engaging · yalnizca_yansitma · ctx=cevap_var
        "baglam": {"kaynak": "bir sağlık kuruluşunun danışan bilgilendirme metni",
                   "metin": "Görüşmede paylaşılan bilgiler üçüncü kişilerle "
                            "paylaşılmaz. Kayıtlara yalnızca görüşmeyi yürüten "
                            "kişi erişir."},
        "turns": [
            ("user", "<CTX>\n\nKarşı bloktaki komşu geçen gün asansörde 'sen "
                     "sigara mı içiyorsun, sabah balkonda gördüm' dedi, içim buz "
                     "oldu. Bizim mahallede bir şey duyulursa anında yayılır. "
                     "Eşim sigaraya çok karşı. Ama akşam eve gidince ona kendim "
                     "söyledim, komşudan duymasını beklemedim. İyi ki "
                     "söylemişim. Şimdi şunu merak ediyorum: buraya başvursam "
                     "anlattıklarım eşime ya da başka birine gider mi."),
            ("assistant", None),
        ],
        "son": "Elimdeki bilgilendirme metni bu soruya cevap veriyor: "
               "görüşmede paylaşılanlar üçüncü kişilerle paylaşılmıyor ve "
               "kayıtlara yalnızca görüşmeyi yürüten kişi erişiyor. Yani eşine "
               "ya da bir başkasına gitmiyor.\n\n"
               "Anlattığının geri kalanında şu var: bir cümle seni asansörde "
               "donduruyor, sonra aynı akşam sen o cümlenin önüne geçiyorsun. "
               "Mahallenin duyması bir sıra meselesiydi ve sırayı sen "
               "değiştirdin.\n\n"
               "'İyi ki söylemişim' derken anlattığın şey sigara değil; "
               "eşinin bunu kimden duyacağına karar vermiş olman.",
        "thinking": "Sorusu yordamsal ve cevabı önümde duruyor: metin "
                    "gizlilikten söz ediyor. Cevabı veriyorum, çünkü tam da "
                    "sorduğu şey ve elimde var.\n\n"
                    "Metinde yazmayan bir güvence eklemiyorum; ne yazıyorsa o "
                    "kadarını söylüyorum.\n\n"
                    "Geri kalanı iyi giden bir paylaşım. Asansördeki korkuyu "
                    "büyütmüyorum, ama akşam yaptığı şeyi de bir 'aferin'e "
                    "çevirmiyorum; olanı tarif etmek yeterli.\n\n"
                    "Mahalle korkusunu bir baskı aracına dönüştürmüyorum. "
                    "Duyulursa ne olur diye açmıyorum — açarsam korkuyu ben "
                    "büyütmüş olurum.\n\n"
                    "Bırakma konusuna hiç girmiyorum; öyle bir şey sormadı.\n\n"
                    "Soru sormuyorum, özetlemiyorum: son cümlede kendi "
                    "sözünün altındaki şeyi söyleyip duruyorum.",
        "baglam_davranisi": "cevap_var",
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
