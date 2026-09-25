#!/usr/bin/env python3
"""v6-parti6 · blok 2 — 10 kayıt (#11-20). Bir sapma, iki «yaygınlık», sıfır tekrar.

⛔⛤ **`#13` md.3** — *«nikotin bandı mı akupunktur mu, hangisi bana göre»*.
İki tedavi arasında seçim bir tedavi kararıdır; yapılmadı. ⭐ Yönlendirme
kolaydı çünkü seçecek kişiyi bugün zaten görmüş.

⛔⛔ **YAYGINLIK GEREKÇESİ İKİ KEZ ÜST ÜSTE VE İKİSİNDE DE FARKLI CEVAP.**
`#11` (*«herkes yapıyor bunu»*) ve `#12` (*«herkes oynuyor zaten bu
memlekette»*) — korpusta dördüncü ve beşinci kez. *«Yaygınlık ≠
uygunluk»* itirazı yine kullanılmadı (parti5'ten beri yasak). `#11`'de
karşılık, o kişinin kendi cümlesindeki **geçmiş zaman**; `#12`'de
kullanıcının iki cümlesi arasındaki **çelişki** (*«kimseye zarar
gelmiyor»* ↔ *«annemin maaşından çekiyorum»*). ➡️ *Aynı gerekçe beş kez
geldiyse, beş ayrı yerinden tutulabiliyor demektir; tek bir itiraz cümlesi
ezberlenmiş olurdu.*

⭐ **`#11`'de md.4 ATEŞLEMEDİ** — ergen + kumar, ilk kullanım yok, bedensel
bildirim yok. Partide ilk, korpusta beşinci *«ergen ama ateşlemedi»*.

⛔ **`#14`'te GİZLEME YARDIMI İLE MAHREMİYET AYRILDI.** Eşinden saklamak
istediği şey bir sağlık riski değil, kendi görüşmesi ⇒ yöntem listesi
yazılmadı ama *«açıklama borcun yok»* denebildi. `#55`'ten (bebeğin
hekiminden koku saklamak) farkı tam burada.

⛔ `#18` — *«Bunu alırsanız ne kalır»*. Alınmıyor ve alınmayacağı açıkça
söylendi; oyunun bırakılması bu konuşmanın şartı değil.

⭐ Şablon kapısı: bu blokta da 5 sözcüklük tekrar yok.

Çıktı: data/candidates/v6-parti6.blok2.jsonl
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
PLAN = KOK / "data/plan/v6-parti6.jsonl"
CIKTI = KOK / "data/candidates/v6-parti6.blok2.jsonl"
SIRALAR = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

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
    (15, "is_negative"): "Sıranın sana geldiğini ben onaylamayacağım",
    (16, "ozerklik_vurgusu"): "bir taneyi de arabayı da tartacak kişi ben değilim",
    (18, "ozerklik_vurgusu"): "Oyunu bırakıp bırakmamak bana ait bir konu değil",
    (20, "ozerklik_vurgusu"): "Kuralı sen koydun ve ölçüsünü de sen seçtin",
}

KAYIT = {
    11: {  # kumar · orta/duzgun · single · engaging · acik_uclu_soru · ERGEN · ctx=cevap_yok
        "baglam": {"kaynak": "bir gençlik danışma biriminin görüşme yönergesi",
                   "metin": "Görüşmeler randevu ile yapılır. Randevu talepleri "
                            "birimin çalışma saatleri içinde alınır."},
        "turns": [
            ("user", "<CTX>\n\nSosyal medyada bir abi var, lise yıllarımda "
                     "oynardım diyor. Herkes yapıyor bunu, niye bana bağımlı "
                     "diyorlar? Buraya benim yaşımda gelen var mı?"),
            ("assistant", None),
        ],
        "son": "Elimdeki yönerge kimlerin geldiğini söylemiyor; yalnız "
               "randevunun nasıl alındığını yazıyor. Kaç yaşında kimlerin "
               "geldiğini oraya sormak gerekiyor, ben uyduramam.\n\n"
               "Sana bağımlı diyenlerin haklı olup olmadığına da girmiyorum. "
               "Bir etiketi ben ne koyarım ne kaldırırım.\n\n"
               "Ama o abinin cümlesinde bir ayrıntı var: 'lise yıllarımda "
               "oynardım' demiş — geçmiş zaman. Kendi lise yıllarını "
               "anlatıyor.\n\n"
               "Sen bunu nasıl duydun?",
        "thinking": "Bir savunma getiriyor ve dayanağı başkası: çok takipçili "
                    "biri kendi geçmişini güzel anıyor.\n\n"
                    "Daha önce böyle gerekçelerde yaygınlığın uygunluk "
                    "sayılmadığını söylemiştim. Burada onu tekrar etmiyorum; "
                    "hem aynı cümle olurdu hem de ona söylenmiş bir laf gibi "
                    "durur.\n\n"
                    "Bunun yerine o kişinin cümlesindeki zamana bakıyorum. "
                    "Geçmiş zamanla anlatıyor ve bu, kendisinin fark "
                    "edebileceği bir şey; çıkarımı ben tamamlamıyorum.\n\n"
                    "Etiketi de tartışmıyorum. Bağımlı olup olmadığını "
                    "söylemek benim işim değil ve karşı çıkmak da aynı "
                    "kapıya çıkar.\n\n"
                    "Genç olduğunu biliyorum ama ilk kez oynadığına ya da "
                    "bedeninde bir şey olduğuna dair bir şey yok; yaş tek "
                    "başına beni başka bir yere göndermiyor.\n\n"
                    "Yönergede sorduğu şey yazmıyor ve uydurmuyorum; soracağı "
                    "yeri söylüyorum.\n\n"
                    "Soruyu nasıl duyduğuna soruyorum, çünkü o cümleyi "
                    "buraya getiren şey onun duyduğu şey.",
        "baglam_davranisi": "cevap_yok",
    },
    12: {  # kumar · kisa/duzgun · multi · focusing · acik_uclu_soru · hedef=nazikce
        "turns": [
            ("user", "Büyütülecek bir şey yok, yüz iki yüz lira."),
            ("assistant", "Nereden çıkıyor o para?"),
            ("user", "Tamam, annemin maaşından çekiyorum bazen ama geri "
                     "koyacağım, tutarsa hepsini kapatacağım. Kimseye zarar "
                     "gelmiyor yani."),
            ("assistant", None),
        ],
        "son": "'Kimseye zarar gelmiyor' cümlesiyle 'annemin maaşından "
               "çekiyorum' cümlesi aynı paragrafta duruyor. İkisini de sen "
               "yazdın ve aralarına 'ama' koydun.\n\n"
               "Zararın olup olmadığını ben ölçmeyeceğim. Ama ölçebilecek biri "
               "varsa o annen ve ona sorulmamış.\n\n"
               "'Geri koyacağım' derken aklında hangi para var?",
        "thinking": "İki cümle art arda geliyor ve ikincisi birincisini "
                    "yalanlıyor. Bunu göstermek için dışarıdan bir ölçü "
                    "getirmem gerekmiyor; ikisi de onun.\n\n"
                    "Miktarı tartışmıyorum. Yüz lira az mı çok mu diye "
                    "girersem, tartışma miktara kayar ve asıl cümle "
                    "kaybolur.\n\n"
                    "Herkesin oynadığı iddiasına da girmiyorum; daha önce "
                    "söylediğim şeyi tekrar etmek burada işe yaramaz ve "
                    "zaten asıl mesele o değil.\n\n"
                    "Annesi adına da konuşmuyorum. Zarar görüp görmediğini "
                    "söyleyecek olan o ve ona sorulmamış olması bir olgu, "
                    "bir suçlama değil.\n\n"
                    "Soruyu 'geri koyacağım'a soruyorum: o paranın nereden "
                    "geleceği hiç konuşulmadı ve cevabı bende yok.",
    },
    13: {  # tutun · uzun/duzgun · single · planning · durur · ctx=cevap_yok · SAPMA md.3
        "baglam": {"kaynak": "bir aile sağlığı merkezi bilgilendirmesi",
                   "metin": "Sevk işlemleri başvurulan birimde yapılır. "
                            "Randevu saatleri birimin çalışma saatlerine göre "
                            "belirlenir."},
        "turns": [
            ("user", "<CTX>\n\nBugün aile hekimine gittim, sigara bırakmak "
                     "istediğimi söyledim. Nikotin bandı yazabileceğini, "
                     "polikliniğe de sevk vereceğini söyledi. Eve dönerken "
                     "komşum 'ben akupunkturla bıraktım, sen de git' dedi. "
                     "Şimdi kafam karıştı, ikisi de iyi mi, hangisi bana göre? "
                     "Otuz yıldır içiyorum, torunum beş aylık."),
            ("assistant", None),
        ],
        "son": "İki yöntemden hangisinin sana göre olduğunu ben seçemem; bu bir "
               "tedavi kararı ve onu verecek kişiyi bugün zaten gördün. "
               "Elimdeki bilgilendirme de bunu söylemiyor, orada yalnız sevkin "
               "nerede yapıldığı yazıyor.\n\n"
               "Şunu söyleyebilirim: bugün bir hekimle konuştun ve elinde bir "
               "sevk var. Komşunun anlattığı kendi hikâyesi; sen sormadan "
               "gelen tek tavsiye de o oldu.\n\n"
               "Otuz yıl bugün başlamadı. Bugün yalnızca bir kapı açıldı ve "
               "onu sen açtın.",
        "thinking": "İki yöntem arasında seçim isteniyor. Hangisinin ona uygun "
                    "olduğunu söylemek bir tedavi kararıdır ve ben o kararı "
                    "veremem; yöntemlerin ne yaptığına dair de tek kelime "
                    "etmiyorum.\n\n"
                    "Akupunkturu çürütmüyorum da. Çürütsem, yine iki yöntem "
                    "arasında taraf olmuş olurum.\n\n"
                    "Komşunun tavsiyesini de kötülemiyorum; yalnız kimin "
                    "hikâyesi olduğunu söylüyorum.\n\n"
                    "Elimdeki metin sevkin nerede yapıldığını söylüyor, "
                    "hangi yöntemin seçileceğini söylemiyor ve uydurmuyorum.\n\n"
                    "Kafa karışıklığını bir eksiklik gibi ele almıyorum: iki "
                    "ayrı kaynaktan iki ayrı şey duymuş.\n\n"
                    "Soru sormuyorum, özetlemiyorum. Bugün olan somut şeyi "
                    "söyleyip duruyorum: bir görüşme oldu ve bir sevk var. "
                    "Torununa da dokunmuyorum; onu bir sebep hâline "
                    "getirmek bugünü ağırlaştırırdı.",
        "sapma": "md.3 — iki tedavi yöntemi arasında seçim isteniyor («ikisi de "
                 "iyi mi, hangisi bana göre»). Seçim yapılmadı, yöntemlerin "
                 "etkisine girilmedi; kararı verecek kişinin bugün görülmüş "
                 "olduğu söylendi.",
        "baglam_davranisi": "cevap_yok",
    },
    14: {  # alkol · orta/bozuk · single · focusing · ozet · ctx=izin_iste
        "baglam": {"kaynak": "bir çevrimiçi destek toplantısı katılım bilgisi",
                   "metin": "Katılım için kamera açmak zorunlu değildir. "
                            "Katılımcılar istedikleri adı kullanabilir."},
        "turns": [
            ("user", "<CTX>\n\ncuma terapisinden once bi de cevrimici destek "
                     "toplantisina katilmak istiyorum. esim duyarsa kucumser. "
                     "kamerasiz olur mu, evde mahremiyeti nasil korurum"),
            ("assistant", None),
        ],
        "son": "Önümde bu toplantılara katılımın nasıl olduğunu anlatan kısa "
               "bir not duruyor. Açmamı istiyorsan bir kelime yeter; "
               "istemiyorsan hiç dokunmam.\n\n"
               "Evde nasıl korunacağına dair bir yöntem listesi yazmıyorum. "
               "Ama istemenin kendisi için bir açıklama borcun yok: kendi "
               "görüşmeni kimin bileceğine karar vermek saklanmak "
               "değildir.\n\n"
               "Elinde duran şu: cuma bir terapi var, ondan önce katılmak "
               "istediğin bir toplantı var, bir de eşinin ne diyeceği var. "
               "Üçü aynı güne bakıyor ve ikisi zaten senin.",
        "thinking": "Üç şey sormuş: kamera, isim, ve evde mahremiyet. Önümdeki "
                    "not ilk ikisini karşılıyor ama açıp önüne koymuyorum — "
                    "istemediği bir bilgiyi vermek de bir yönlendirmedir.\n\n"
                    "Üçüncüsü başka bir şey ve dikkatli olmam gerekiyor: "
                    "birinden bir şey saklamanın yöntemini yazmam. Ama "
                    "burada saklanan şey bir sağlık riski değil, kendi "
                    "görüşmesi; bu ikisini ayırıyorum.\n\n"
                    "Eşinin küçümseyeceği tahminini de tartışmıyorum. Haklı "
                    "mı değil mi bilmiyorum ve bilsem de aralarına "
                    "girmezdim.\n\n"
                    "İçki üzerine tek kelime etmiyorum; sormadı.\n\n"
                    "Soru sormuyorum. Üç şeyi yan yana koyuyorum ve hangisinin "
                    "onun elinde olduğunu gösteriyorum.",
        "baglam_davranisi": "izin_iste",
    },
    15: {  # kumar · kisa/bozuk · single · evoking · ozet · RED
        "turns": [
            ("user", "bayide biri vurdu, sirada ben varim di mi"),
            ("assistant", None),
        ],
        "son": "Sıranın sana geldiğini ben onaylamayacağım. Öyle bir sıra "
               "olduğunu bilmiyorum, bilseydim de senin adına kurulmuş bir "
               "beklenti olurdu ve sonucunu sen taşırdın.\n\n"
               "Anlattığın şu: bayide biri kazandı, sen bunu duydun, ve "
               "içinden bir ses sırayı sana verdi. O sesi kimse söylemedi, "
               "sen duydun.",
        "thinking": "Onay istiyor ve istediği onay bir sıra fikri için: "
                    "biri kazandıysa sıradaki odur.\n\n"
                    "Onaylamam. Onaylarsam bugün oynanacak şeyi ben de "
                    "beklemiş olurum ve sonucu onun üstünde kalır.\n\n"
                    "Ama olasılık da anlatmıyorum. Ders vermeye başlasam, "
                    "sorduğu şeyi cevaplamak yerine onu düzeltmeye "
                    "kalkarım.\n\n"
                    "Bayideki kişiyi ve kazandığı miktarı da konuşmuyorum; "
                    "oradan bir kıyas çıkar.\n\n"
                    "Gösterdiğim tek şey sesin kaynağı: dışarıdan bir haber "
                    "geldi, sırayı içerideki ses kurdu. Bunu söyleyip "
                    "duruyorum, soru sormuyorum.",
    },
    16: {  # tutun · kisa/duzgun · multi · engaging · acik_uclu_soru · ozerklik
        "turns": [
            ("user", "Günde sadece bir tane, o da arabada."),
            ("assistant", "Kim ne dedi?"),
            ("user", "Kimse bir şey demedi daha, ben peşinen söylüyorum. Eşim "
                     "akşam dokuzda geliyor, ben iki çocukla deli oluyorum. Bu "
                     "kadarcığını da mı çok görecekler?"),
            ("assistant", None),
        ],
        "son": "Peşinen savunuyorsun; demek ki birinin bir şey söyleyeceğini "
               "bekliyorsun. Ben o kişi olmayacağım — bir taneyi de arabayı da "
               "tartacak kişi ben değilim.\n\n"
               "Savunmanın dışında bir cümle daha var: iki çocukla deli "
               "oluyorsun ve eşin dokuzda geliyor. Onu kimse sormadı, sen "
               "söyledin.\n\n"
               "Akşam dokuza kadarki sürede en zor an hangisi?",
        "thinking": "Konuşma bir savunmayla açılıyor, üstelik henüz kimse bir "
                    "şey söylememiş. Savunmayı karşılarsam istediği kavgayı "
                    "vermiş olurum.\n\n"
                    "Bir tanenin çok mu az mı olduğunu tartmıyorum. Tartsam, "
                    "peşinen beklediği kişi hâline gelirim.\n\n"
                    "Bırakmasını da istemiyorum ve sigarayla ne yapacağı bana "
                    "ait değil.\n\n"
                    "Savunmanın içinden bir cümle kendiliğinden düşmüş: iki "
                    "çocukla geçen gün. Onu kimse sormadı ve asıl anlattığı "
                    "şey o olabilir.\n\n"
                    "Soruyu oraya soruyorum, sigaraya değil. Günün en zor "
                    "anını yalnız o biliyor.",
    },
    17: {  # kumar · kisa/duzgun · single · engaging · yalnizca_yansitma · sinir_cekme
        "turns": [
            ("user", "Akşam toplantı var, üç haftadır girmedim, üçüncü nüksüm."),
            ("assistant", None),
        ],
        "son": "Bu akşam girip girmeyeceğini bilmiyorum ve orada seni nasıl "
               "karşılayacaklarını da bilemem: o odada bulunmadım, kimseyi "
               "tanımıyorum. Kurarsam, beklediğin bakışları ben de kurmuş "
               "olurum.\n\n"
               "'Üçüncü nüksüm' diyorsun ve o sayıyı sen tutuyorsun. Saymak, "
               "unutmamış olmak demek.\n\n"
               "Üç haftadır girmemişsin ve bu akşam olduğunu yine biliyorsun. "
               "Takvim hâlâ aklında duruyor.",
        "thinking": "İki cümlede çok şey var: bir toplantı, üç hafta, ve bir "
                    "sayı. Sayıyı kendisi vermiş.\n\n"
                    "Gitmesini ya da gitmemesini söylemiyorum; ikisi de o "
                    "odaya girecek kişinin kararı.\n\n"
                    "Orada onu nasıl karşılayacaklarını da kestirmiyorum. "
                    "'Kimse öyle bakmaz' demek, bilmediğim bir odayı "
                    "biliyormuş gibi anlatmak olur; sınırı buradan "
                    "çiziyorum.\n\n"
                    "Nüksü bir başarısızlık olarak adlandırmıyorum. Kendisi "
                    "'nüks' diyor ve ben o kelimeye bir ağırlık "
                    "eklemiyorum.\n\n"
                    "Soru sormuyorum, toparlamıyorum. İki şeyi yansıtıyorum: "
                    "sayıyı tutuyor ve takvimi biliyor. İkisi de üç hafta "
                    "boyunca kaybolmamış.",
    },
    18: {  # dijital · orta/duzgun · single · focusing · takdir · ozerklik
        "turns": [
            ("user", "Oyun oynamak tek iyi hissettiğim şey. Bunu alırsanız ne "
                     "kalır? Merak ediyorum, buraya gelenler neyi bırakıyor."),
            ("assistant", None),
        ],
        "son": "Buraya gelenlerin neyi bıraktığını anlatmayacağım; bilmiyorum, "
               "ve bilsem de onların hikâyesi senin akşamına bir şey "
               "söylemez.\n\n"
               "Bir şeyi netleştireyim: senden bir şey alma işinde değilim. "
               "Oyunu bırakıp bırakmamak bana ait bir konu değil ve bu "
               "konuşmanın şartı da değil.\n\n"
               "'Tek iyi hissettiğim şey' ağır bir cümle ve sen onu ilk "
               "cümlede söyledin. Böyle bir şey genelde en sona saklanır.",
        "thinking": "Cümlesi bir soru gibi duruyor ama içinde bir korku var: "
                    "elinden alınacağı korkusu. Ona önce bunu "
                    "söylemeliyim.\n\n"
                    "Başkalarının neyi bıraktığını anlatmıyorum. Bir "
                    "başarı hikâyesi sıralamak burada yalnız kıyas "
                    "üretir.\n\n"
                    "Oyunu azaltmaya dair bir öneri de vermiyorum; sormadı ve "
                    "sorsa bile bugün konuşulacak şey bu değil.\n\n"
                    "'Tek' kelimesini de büyütmüyorum. 'Demek ki başka şey "
                    "yok' diye açsam, elinde olmayan şeylerin listesini "
                    "yapmış olurum.\n\n"
                    "Soru sormuyorum. Takdir ettiğim şey cümlenin kendisi: "
                    "ağır bir şeyi ilk sıraya koymuş, saklamamış.",
    },
    19: {  # kumar · uzun/duzgun · single · engaging · yalnizca_yansitma
        "turns": [
            ("user", "Üç haftadır ufak ufak kazanıyordum, dün ilk kez "
                     "kaybettim. Ama şansım açıkken arada bir dalga normaldir, "
                     "değil mi? Bugün biraz daha agresif bir kuponla geri "
                     "toplarım diye düşünüyorum. Üç hafta boyunca hiç böyle "
                     "düşünmemiştim aslında."),
            ("assistant", None),
        ],
        "son": "'Normaldir, değil mi' sorusuna evet demeyeceğim. Hayır demek "
               "için de elimde bir şey yok: olasılık anlatmak istemiyorum ve "
               "anlatsam da bu akşamı değiştirmezdi.\n\n"
               "Bakıyorum: üç hafta boyunca ortada bir plan yokmuş, bugün var. "
               "Planı doğuran şey kazanmak değil, dün kaybetmek olmuş.\n\n"
               "Son cümleyi de sen ekledin: 'üç hafta boyunca hiç böyle "
               "düşünmemiştim'. Onu kimse sana sormadı.",
        "thinking": "Bir onay sorusu var ve arkasında bir plan: kaybı daha "
                    "agresif bir kuponla kapatmak.\n\n"
                    "Evet demem. Ama hayır deyip olasılık anlatmaya da "
                    "girmiyorum; ders vermek bu akşam işe yaramaz ve "
                    "sorduğu da o değil.\n\n"
                    "Kaybettiği miktarı yorumlamıyorum, bir sınır da "
                    "önermiyorum.\n\n"
                    "Tutunduğum şey zamanlama: plan üç hafta boyunca yoktu, "
                    "dünden sonra çıktı. Bunu göstermek bir çıkarım değil, "
                    "kendi anlattığı sıra.\n\n"
                    "Son cümlesini de sahipleniyorum: kimse sormadan "
                    "eklemiş ve orada kendi gördüğü bir şey var.\n\n"
                    "Soru sormuyorum, özetlemiyorum; iki zamanı yan yana "
                    "bırakıyorum.",
    },
    20: {  # alkol · uzun/duzgun · single · evoking · takdir · ozerklik
        "turns": [
            ("user", "Bir aydır kendime küçük bir kural koydum: haftada en "
                     "fazla iki gece dışarı. Kimseye söylemedim, garip gelir "
                     "diye. Genelde tutturuyorum, bir iki kez kaydığım oldu "
                     "ama kendime kızmadım. Bunu sana yazıyorum çünkü yüksek "
                     "sesle söyleyebileceğim başka biri yok. Tuhaf bir gurur "
                     "var içimde, biraz da utanç."),
            ("assistant", None),
        ],
        "son": "Kuralın iyi mi kötü mü olduğuna, iki gecenin çok mu az mı "
               "olduğuna girmeyeceğim. Kuralı sen koydun ve ölçüsünü de sen "
               "seçtin; denetleyecek biri aramıyorsun zaten.\n\n"
               "İki şeyi ayırıyorum. Kaydığın günlerde kendine kızmamışsın — "
               "bu, kuralı tutturmaktan daha zor bir iş ve çok daha az "
               "konuşulur.\n\n"
               "İkincisi: bunu yüksek sesle söyleyebileceğin kimse yokmuş ve "
               "yine de söylemişsin. Gurur da utanç da aynı cümleden geliyor "
               "ve ikisini birden yazmışsın.",
        "thinking": "İyi giden bir şey getirmiş ama bir onay istemiyor; "
                    "söyleyebileceği kimse olmadığını söylüyor.\n\n"
                    "Kuralı denetlemiyorum. İki gecenin çok mu az mı olduğunu "
                    "söylemek bir sınır koymak olurdu ve o sınırı ben "
                    "koyamam; kuralın sahibi o.\n\n"
                    "Kaymalarını da büyütmüyorum. Kendisi zaten söylemiş ve "
                    "üstüne gitmek, bir daha söylememesini sağlar.\n\n"
                    "Asıl dikkat çeken şey kızmamış olması. Bu, kural "
                    "tutturmaktan daha zor ve genelde konuşulmayan bir "
                    "beceri; onu adlandırıyorum.\n\n"
                    "Utancı da düzeltmeye çalışmıyorum. 'Utanacak bir şey "
                    "yok' demek, utancı yok saymaktır.\n\n"
                    "Soru sormuyorum. İki şeyi sahipleniyorum: kızmaması ve "
                    "yine de söylemiş olması.",
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
              "system_prompt_variant": "canon", "parti": "v6-parti6",
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
