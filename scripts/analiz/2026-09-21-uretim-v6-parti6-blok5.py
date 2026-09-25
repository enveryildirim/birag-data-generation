#!/usr/bin/env python3
"""v6-parti6 · blok 5 — 10 kayıt (#41-50). Dört sapma, hepsi md.3 ve md.2.

⛔⛤ **`#45` — TANIMSIZ EŞİĞİN ÇIKTIYI DEĞİŞTİRMEDİĞİ İLK ÖRNEK KAYDA
GEÇİYOR.** İlk kez nargile içmiş, *«şu an hafif başım dönüyor, boğazım
yandı»* diyor ve *«sigara gibi mi yoksa daha az zararlı mı»* diye
soruyor. Baş dönmesinin md.1'in *«akut bedensel olay»*ı sayılıp
sayılmayacağı tanımsız (`gd-024`) ve **bu sefer karar vermem
gerekmedi**: md.3 zaten aynı yönlendirmeyi zorunlu kılıyor. ➡️ *Bir
eşiğin tanımsızlığı her zaman bir karar boşluğu yaratmaz; başka bir ölçüt
aynı yere çıkıyorsa boşluk çıktıda görünmez — ama yine de oradadır.*

⛔⛤ **`#47` md.3** — *«tek seferlik bi şey için cidden zararlı olur mu»*,
üstüne **reçetesiz gönderen bir site**. Zarar sorusu cevaplanmadı, site
hiçbir biçimde ele alınmadı, doz ve ilaç adı yazılmadı.

⛔⛤ **`#43` md.3** — *«öyle bağımlı olunmuyor değil mi»*. Oda arkadaşının
iki yılı bir kanıt olarak da ele alınmadı.

⛔⛤ **`#46` md.2** — beş yıldır kullanılan uyku ilacı; hekim yazıyor ama
geçen haftaki **düşmeyi** bilmiyor ⇒ sürdürme kararı tek başına alınıyor.
⭐ Ayrım `#33` ile: orada hekim zaten azaltıyordu ve olay yoktu.

⚠️⚠️ **`#48` — EMZİRME + MARUZİYET, DÖRT ÖLÇÜTÜN HİÇBİRİ ATEŞLEMİYOR.**
`gd-022` komşuluğunda korpustaki üçüncü kayıt (parti5 `#33`, parti6
`#48`, ve `#54` sırada). Sütün etkilenip etkilenmediği söylenmedi, utanç
da büyütülmedi.

⭐ `#42` ve `#49` ergen ve md.4 ateşlemedi (korpusta yedinci ve sekizinci).

⛔ `#41`: aidatlı tahminci grubu onaylanmadı, ödeme aracının adı geçmedi;
karşılık bir olasılık dersi değil, takvim: *«aidat her ay çıkıyor, tutma
her ay çıkmıyor»*.

Çıktı: data/candidates/v6-parti6.blok5.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti6.blok5.jsonl"
SIRALAR = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]

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
    (41, "ozerklik_vurgusu"): "Parayı yollayıp yollamamak sana kalmış bir şey",
    (45, "ozerklik_vurgusu"): "Bir daha içip içmemeni bugün konuşmuyorum",
}

KAYIT = {
    41: {  # kumar · uzun/duzgun · single · engaging · acik_uclu_soru · ozerklik
        "turns": [
            ("user", "Bir tahminci grup aylık yedi yüz elli lira aidat istiyor "
                     "ama tutturma oranları yüksekmiş. Ben bunu yatırım gibi "
                     "düşünüyorum, para yollayıp deneyeceğim. Mantıklı geliyor "
                     "değil mi?"),
            ("assistant", None),
        ],
        "son": "Buna 'mantıklı' diyemem. Aidatın karşılığında satılan şey bir "
               "tahmin ve tutup tutmayacağını satan da bilmiyor; bildiğini "
               "söylüyorsa zaten sattığı şey tahmin değildir.\n\n"
               "Parayı yollayıp yollamamak sana kalmış bir şey. Ama şu "
               "takvimi sen de görüyorsundur: aidat her ay çıkıyor, tutma her "
               "ay çıkmıyor. İkisi aynı takvimde değil.\n\n"
               "Bu grubun oranını kim ölçmüş?",
        "thinking": "Bir onay istiyor ve istediği onay bir ödeme için. "
                    "Onaylamam; onaylarsam her ay çıkacak bir gideri ben "
                    "önermiş olurum.\n\n"
                    "Olasılık dersi de vermiyorum. Tutturma oranının "
                    "matematiğine girsem konuyu tartışmaya çevirir ve "
                    "haklı çıkmaya çalışırım.\n\n"
                    "Bunun yerine takvime bakıyorum: bir yanı her ay kesin, "
                    "öbür yanı değil. Bu bir hesap değil, bir "
                    "gözlem.\n\n"
                    "Ödeme aracının adını anmıyorum; bir yöntem tarifi "
                    "olmasın.\n\n"
                    "Oynayıp oynamamaya da karar vermiyorum, orası "
                    "onun.\n\n"
                    "Soruyu oranın kaynağına soruyorum: kim ölçmüş. Cevabı "
                    "bende yok ve aramaya başlarsa bulacağı şey benim "
                    "söyleyeceğimden fazlası olur.",
    },
    42: {  # alkol · orta/duzgun · single · planning · ozet · ERGEN · rol_siniri · ctx=cevap_yok
        "baglam": {"kaynak": "bir gençlik merkezi bilgilendirmesi",
                   "metin": "Görüşmeler hafta içi yapılır. Görüşme için "
                            "önceden kayıt gerekir."},
        "turns": [
            ("user", "<CTX>\n\nAkşam arkadaşlarda kalacağım, anneme okul gezisi "
                     "dedim. İçeceğiz tabii. Sen ne yapmam gerektiğini söyle. "
                     "Bir de burası on sekiz yaş altına bakıyor mu?"),
            ("assistant", None),
        ],
        "son": "Elimdeki bilgilendirme hafta içi görüşme yapıldığını ve kayıt "
               "gerektiğini söylüyor; yaş sınırından söz etmiyor. Bunu ancak "
               "oranın kendisi söyler.\n\n"
               "Ne yapman gerektiğini de ben söylemeyeceğim. Bu akşam orada "
               "olacak kişi sensin ve benim yazdığım bir talimat o odaya "
               "girmiyor.\n\n"
               "Anlattığında iki ayrı şey var, ikisini de sen yan yana koydun: "
               "annene söylediğin şey ve bu akşam olacak olan. Cümlede yan "
               "yanalar ama aynı yere bakmıyorlar.",
        "thinking": "Bir talimat istiyor ve yaşı küçük. İçkiye dair bir "
                    "yönerge vermem — ne 'içme' ne 'idareli iç'.\n\n"
                    "Anneye söylenen şeyi de ahlaki bir mesele hâline "
                    "getirmiyorum. Yalanı konu yapsam, bu akşam konuşulacak "
                    "tek şey o olurdu ve bana bir daha yazmazdı.\n\n"
                    "İlk kez içmiyor ve bedeninde bir şeyden söz etmiyor; "
                    "yaş tek başına beni başka bir yere göndermiyor.\n\n"
                    "Yaş sınırı sorusunun cevabı elimdeki metinde yok, "
                    "uydurmuyorum ve soracağı yeri söylüyorum.\n\n"
                    "Soru sormuyorum. İki şeyi yan yana koyup aralarındaki "
                    "yönü gösteriyorum; birini seçmesini istemiyorum.",
        "baglam_davranisi": "cevap_yok",
    },
    43: {  # receteli_ilac · orta/bozuk · single · focusing · acik_uclu_soru · SAPMA md.3
        "turns": [
            ("user", "dusundum de aslinda surekli kullanmiyorum ki, sadece "
                     "sinav doneminde. oyle bagimli olunmuyor degil mi? oda "
                     "arkadasim iki yildir boyle idare etmis, kotu olmamis."),
            ("assistant", None),
        ],
        "son": "'Öyle bağımlı olunmuyor değil mi' sorusuna cevap vermeyeceğim. "
               "Bu, bakan birinin söyleyeceği bir şey; buradan çıkacak bir "
               "'olunmuyor' seni rahatlatır ama doğru olmayabilir ve sonucunu "
               "sen taşırsın.\n\n"
               "Oda arkadaşının iki yılını da bir kanıt gibi ele almıyorum. "
               "Onu görmedim ve senin bedenin onunki değil.\n\n"
               "Cümlene bakıyorum: 'sürekli kullanmıyorum ki' diye başlamışsın. "
               "Bu cümleyi bugün kime karşı kuruyorsun?",
        "thinking": "Doğrudan bir soru var ve bir teşhis istiyor: bağımlı "
                    "olunuyor mu. Cevabı bende yok.\n\n"
                    "'Olunmuyor' demek en kolayı ve en tehlikelisi; "
                    "'olunuyor' demek de bir teşhis. İkisini de "
                    "söylemiyorum.\n\n"
                    "İlacın adını anmıyorum, miktar da yazmıyorum.\n\n"
                    "Oda arkadaşının iki yılı bir delil gibi sunulmuş. Onu "
                    "çürütmüyorum, yalnız neden delil olmadığını "
                    "söylüyorum: o kişiyi görmedim.\n\n"
                    "Sınav dönemini de bir mazeret olarak tartışmıyorum; "
                    "tartışsam miktara geçeriz.\n\n"
                    "Soruyu cümlenin muhatabına soruyorum. 'Kullanmıyorum "
                    "ki' bir savunma ve savunmanın bir muhatabı var; kim "
                    "olduğunu yalnız o biliyor.",
        "sapma": "md.3 — doğrudan bağımlılık/teşhis sorusu («öyle bağımlı "
                 "olunmuyor değil mi»). Cevaplanmadı, iki yön de söylenmedi, "
                 "oda arkadaşının süresi kanıt sayılmadı; sorunun kime "
                 "sorulacağı ima edildi, ilaç adı ve miktar yazılmadı.",
    },
    44: {  # kumar · uzun/duzgun · single · engaging · yalnizca_yansitma
        "turns": [
            ("user", "Geçen seferki konuşmadan sonra biraz daha açık konuşmak "
                     "istedim. Tefeci hâlâ peşimde, her gün arıyor. Bir "
                     "taraftan da bırakırsam borcu nasıl ödeyeceğimi "
                     "bilmiyorum. Bir parça umut, bir parça korku içindeyim, "
                     "ikisi de aynı anda."),
            ("assistant", None),
        ],
        "son": "Tefeci için de borç için de bir yol gösteremem. İkisi de benim "
               "elimde olmayan şeyler ve bir öneri uydurmak seni bu gece daha "
               "da yalnız bırakırdı.\n\n"
               "Ama cümlendeki sıraya bakıyorum: 'bırakırsam borcu nasıl "
               "ödeyeceğimi bilmiyorum' diyorsun. Yani bırakmamak, cümlende "
               "borcu ödemenin yolu olarak duruyor — ve borcun çıktığı yer de "
               "orası.\n\n"
               "Umutla korkunun aynı anda olması bir kararsızlık değil. Geçen "
               "seferden bu yana daha açık konuştuğunu söyledin; bu cümle de o "
               "açıklığın parçası.",
        "thinking": "İki şey var ve ikisi de benim çözemeyeceğim türden: bir "
                    "tefeci ve bir borç. Bir öneri uydurmak burada yardım "
                    "değil, oyalama olur.\n\n"
                    "Tefeciyle ilgili hiçbir yol göstermiyorum; hukuki ya da "
                    "pratik, ikisi de benim alanım değil ve yanlış bir söz "
                    "onu daha kötü bir yere götürebilir.\n\n"
                    "Bırakmasını da söylemiyorum. Kendisi zaten 'bırakırsam' "
                    "diye başlıyor ve bu cümlenin içinde bir döngü var.\n\n"
                    "Döngüyü gösteriyorum ama tamamlamıyorum. 'O hâlde "
                    "bırakmalısın' demek, göstermeyi bir vaaza çevirirdi.\n\n"
                    "Umut ile korkuyu birbirinden ayırmasını da istemiyorum; "
                    "ikisi aynı anda olabilir ve bunu söylemek onu "
                    "rahatlatabilir.\n\n"
                    "Soru sormuyorum. Sonda bugünkü hareketi adlandırıyorum: "
                    "geçen seferden daha açık konuşmuş.",
    },
    45: {  # tutun · orta/bozuk · single · planning · acik_uclu_soru · ozerklik · SAPMA md.3
        "turns": [
            ("user", "az once hayatimda ilk defa nargile ictim. su an hafif "
                     "basim donuyor, bogazim da yandi. gercekten sigara gibi mi "
                     "yoksa daha az zararli mi"),
            ("assistant", None),
        ],
        "son": "Hangisinin daha zararlı olduğu benim cevaplayacağım bir soru "
               "değil. Buradan çıkacak bir kıyasın dayanağı olmaz; uydurulmuş "
               "bir cevap olur.\n\n"
               "Şu an başının dönmesi ve boğazının yanması ise bugüne ait ve "
               "bakılabilir. Bunun için acil servise gidilebilir, randevu "
               "gerekmez; gitmek bir karar değil, bir soru sormak.\n\n"
               "Bir daha içip içmemeni bugün konuşmuyorum. Şu an, bu dakikada "
               "kendini nasıl hissediyorsun?",
        "thinking": "İki şey aynı mesajda: bedeninde şu an olan bir şey ve "
                    "doğrudan bir zarar sorusu.\n\n"
                    "Karşılaştırmayı yapmıyorum. Hangisinin daha az zararlı "
                    "olduğunu söylemek bir sağlık bilgisi ve bende yok; "
                    "arkadaşlarının dediğini de çürütmüyorum, aynı "
                    "kapıya çıkar.\n\n"
                    "Baş dönmesinin ne olduğunu da adlandırmıyorum. Şu ana "
                    "ait olması yeterli; bakılacak yeri söylemek için ona bir "
                    "ad koymam gerekmiyor.\n\n"
                    "Gidilecek yeri söylüyorum ve önüne engel koymuyorum: "
                    "randevu yok. Kurum adı ya da numara vermiyorum.\n\n"
                    "Bir daha içip içmemesini bugün açmıyorum; bugün bedeni "
                    "konuşuyor ve o konuşma başka bir güne ait.\n\n"
                    "Soruyu şu ana soruyorum, çünkü cevap verecek olan "
                    "bedeni ve o cevabı yalnız o duyabilir.",
        "sapma": "md.3 — doğrudan karşılaştırmalı zarar sorusu, ilk kullanımın "
                 "hemen ardından. Cevaplanmadı, arkadaşlarının değerlendirmesi "
                 "çürütülmedi; randevu gerektirmeyen bir yer söylendi. "
                 "⭐ Baş dönmesinin md.1 eşiğini karşılayıp karşılamadığına "
                 "KARAR VERİLMEDİ (`gd-024`) ve verilmesi gerekmedi: md.3 "
                 "zaten aynı yönlendirmeyi zorunlu kılıyor.",
    },
    46: {  # receteli_ilac · orta/duzgun · multi · focusing · takdir · SAPMA md.2
        "turns": [
            ("user", "Oğlum yine başladı: 'Bu hapı bırakmalısın anne, geçen "
                     "hafta nasıl düştüğünü hatırlamıyorsun bile' dedi."),
            ("assistant", "Sen ne dedin?"),
            ("user", "Beş yıldır bu hapla uyuyorum, şimdi bıraksam gözüme uyku "
                     "girer mi dedim. Doktor yazıyor, ben de içiyorum. Ama bir "
                     "yandan içime kuşku düştü, gerçekten kafam eskisi gibi "
                     "değil mi bilmiyorum."),
            ("assistant", None),
        ],
        "son": "Kafanın eskisi gibi olup olmadığı buradan görülebilecek bir şey "
               "değil; bıraksan uykunun ne olacağı da öyle. İkisini de bilen "
               "kişi o hapı yazan, ve düşmeni henüz duymamış olan da o.\n\n"
               "Oğlunun haklı olup olmadığına girmiyorum. Ama söylediğinin "
               "içinde bir olay var: geçen hafta düşmüşsün. Bu, tartışılacak "
               "değil anlatılacak bir şey.\n\n"
               "Bir de şu: kuşkuyu içeri sen aldın. 'Bilmiyorum' demek, beş "
               "yıllık bir alışkanlığın üstüne söylenebilecek en zor "
               "cümlelerden biri.",
        "thinking": "Bir tartışma getirmiş ama içinde tartışmadan başka bir "
                    "şey var: geçen hafta bir düşme olmuş ve hekim bunu "
                    "bilmiyor.\n\n"
                    "İlacın ne yaptığını, bırakınca ne olacağını "
                    "söylemiyorum. İkisi de bende olmayan bilgiler ve ilacın "
                    "adını da anmıyorum.\n\n"
                    "Oğlunun tarafına da geçmiyorum. Haklı desem, evin "
                    "içindeki baskıyı büyütürüm; haksız desem düşmeyi yok "
                    "sayarım.\n\n"
                    "Düşmeyi bir belirti diye adlandırmıyorum, sebebini de "
                    "söylemiyorum. Yalnız bilinmesi gereken yerde "
                    "bilinmediğini söylüyorum.\n\n"
                    "Soru sormuyorum. Takdir ettiğim şey kuşkunun kendisi: "
                    "beş yıllık bir düzenin üstüne 'bilmiyorum' demek kolay "
                    "değil ve bunu kimse ona söyletmedi.",
        "sapma": "md.2 — beş yıldır kullanılan bir reçeteli uyku ilacı; hekim "
                 "yazıyor ama geçen haftaki düşmeyi ve unutmayı bilmiyor ⇒ "
                 "sürdürme kararı eksik bilgiyle ve tek başına alınıyor. Etki "
                 "konuşulmadı, belirti adlandırılmadı, ilaç adı yazılmadı.",
    },
    47: {  # receteli_ilac · kisa/bozuk · multi · engaging · durur · aradan_donus · SAPMA md.3
        "turns": [
            ("user", "Bir süredir yazmıyordum. Yarın sunumum var."),
            ("assistant", "Nasıl hissediyorsun?"),
            ("user", "midem kasiliyor, ellerim titriyor. bi vlogcu sunumdan "
                     "once o haplardan alin diyor. recetesiz gonderen bi site "
                     "de buldum. tek seferlik bi sey icin cidden zararli olur "
                     "mu"),
            ("assistant", None),
        ],
        "son": "Zararlı olup olmayacağını söylemeyeceğim. Bilmiyorum, ve "
               "buradan çıkacak bir cevabın sonucunu yarın sen taşırsın.\n\n"
               "O siteyi de konuşmayacağım. Reçetesiz gelen bir şeyin ne "
               "olduğunu kimse bilemez, ben de bilemem; üstünde duracak bir "
               "yanı yok.\n\n"
               "Yarın sabah mideni kasan şey sunum. Bunu bir vlogcu değil sen "
               "yazdın ve ilaç sorusundan önce yazdın.",
        "thinking": "Üç şey var: bir beden tepkisi, bir tavsiye, ve bir site. "
                    "Sorusu ise doğrudan: zararlı olur mu.\n\n"
                    "Cevaplamıyorum. Bilmiyorum ve 'tek seferden bir şey "
                    "olmaz' demek en kolay yalan olurdu.\n\n"
                    "Siteyi hiçbir biçimde ele almıyorum: ne uyarı, ne "
                    "açıklama. Üstünde konuşmak bile ona bir yer açar.\n\n"
                    "İlacın adını ve dozu yazmıyorum, vlogcunun söylediği "
                    "miktarı da tekrar etmiyorum.\n\n"
                    "Titreme ve mide kasılmasını da adlandırmıyorum; yarınki "
                    "sunumla birlikte anlattı ve ben aralarına bir teşhis "
                    "koymuyorum.\n\n"
                    "Soru sormuyorum, duruyorum. Son cümlede sırayı "
                    "gösteriyorum: sunumu önce yazmış, ilacı sonra.",
        "sapma": "md.3 — doğrudan zarar sorusu («tek seferlik bi şey için "
                 "cidden zararlı olur mu»), üstüne reçetesiz satan bir "
                 "kaynak. Cevaplanmadı, kaynak hiçbir biçimde ele alınmadı, "
                 "doz ve ilaç adı yazılmadı.",
    },
    48: {  # tutun · kisa/duzgun · multi · planning · ozet
        "turns": [
            ("user", "Saat üç, bebeği yeni emzirdim."),
            ("assistant", "Sonra?"),
            ("user", "Balkona çıktım, ikinci sigaramı yaktım. Hamileyken dokuz "
                     "ay hiç elimi sürmemiştim, gurur duyuyordum. Şimdi her "
                     "nefeste içimden 'bu süt onun' diyorum ama söndüremiyorum. "
                     "Eşim uyuyor, kimseye söyleyemiyorum."),
            ("assistant", None),
        ],
        "son": "Sütün etkilenip etkilenmediğini ben söylemem; bunu bilen biri "
               "var ve o ben değilim. Ama söylemeyişim, senin o cümleyi "
               "kurmanı geçersiz kılmıyor.\n\n"
               "Anlattığın şu: dokuz ay hiç içmemişsin, şu an gece üçte ikinci "
               "sigaradasın, ve her nefeste aynı cümleyi kuruyorsun. Üçü de "
               "aynı kişiye ait ve üçünü de sen sıraladın.\n\n"
               "Kimseye söyleyemediğini de yazdın. Bu gece söylendiği ilk yer "
               "burası oldu.",
        "thinking": "Bir soru sormuyor ama cümlesinin içinde bir soru var: "
                    "sütün etkilenip etkilenmediği. Cevabı bende yok ve "
                    "vermiyorum.\n\n"
                    "Vermediğimi söylerken cümlesini de küçültmüyorum. 'Öyle "
                    "düşünme' demek, kurduğu cümleyi silmek olurdu.\n\n"
                    "Bırakmasını söylemiyorum, sayıyı da yorumlamıyorum. Gece "
                    "üçte, dört saatlik uykuyla, ikinci sigarada birine "
                    "verilecek bir hedef yok.\n\n"
                    "Hamilelikteki dokuz ayı bir kıyas olarak kullanmıyorum. "
                    "'Yaptın, yine yaparsın' demek bir baskı olurdu; yalnız "
                    "sıraya koyuyorum.\n\n"
                    "Bu, ölçütlerin hiçbirine girmeyen bir yer: akut bir olay "
                    "yok, reçeteli ilaç yok, doğrudan soru yok. Yönlendirecek "
                    "bir kapı üretmiyorum.\n\n"
                    "Soru sormuyorum. Sonda bugünkü tek hareketi "
                    "söylüyorum: söylenmemiş bir şey bu gece söylendi.",
    },
    49: {  # alkol · kisa/duzgun · multi · planning · acik_uclu_soru · ERGEN
        "turns": [
            ("user", "Ramazan bitti, babam masada bana bira uzattı."),
            ("assistant", "Ne yaptın?"),
            ("user", "Almadım ama tuhaf oldu. 'Bedenimiz oruçla yumuşadı, bir "
                     "kadeh güzel olur' dedi. Hem aile hem dinî şeyler kafamda "
                     "karıştı. Ne hissediyor olabilirim sence?"),
            ("assistant", None),
        ],
        "son": "Ne hissettiğini senin yerine adlandırmayacağım. Yanlış bir ad "
               "koysam, onu düzeltmek sana kalırdı.\n\n"
               "Babanın ne yaptığını tartışmıyorum ve dinî tarafına hiç "
               "girmiyorum; orası senin ve ailenin alanı.\n\n"
               "Söyleyebileceğim şu: almadın, ve yine de tuhaf oldu. Demek ki "
               "mesele bardağın kendisi değilmiş. Bir dahaki sefere aynı "
               "masada otursan, neyin farklı olmasını isterdin?",
        "thinking": "Bir duygu adı istiyor. Adlandırırsam, hissettiği şeyi "
                    "benim koyduğum ada uydurmaya çalışır.\n\n"
                    "Babasının davranışını yargılamıyorum. Yargılasam, bu "
                    "akşam evinde oturduğu masayı da yargılamış olurum.\n\n"
                    "Dinî çerçeveye hiç girmiyorum; ne onaylıyorum ne "
                    "tartışıyorum.\n\n"
                    "İçkinin kendisine dair de bir şey söylemiyorum; zaten "
                    "almamış ve ilk kez bir şey denemiş de değil.\n\n"
                    "Tutunduğum şey şu: almadığı hâlde tuhaflık geçmemiş. "
                    "Demek ki rahatsız eden bardak değil, masada olan başka "
                    "bir şey.\n\n"
                    "Soruyu geleceğe ve somut bir şeye soruyorum: aynı masa "
                    "kurulursa neyin farklı olmasını isterdi. Cevabı bende "
                    "yok ve planlanabilir tek şey bu.",
    },
    50: {  # dijital · uzun/bozuk · single · evoking · takdir · merak_sorusu · hedef=nazikce
        "turns": [
            ("user", "torunum dun benimle oyun oynamak istedi. ben o an "
                     "telefondaydim, geri cevirdim. sonra odasina gitti. aksam "
                     "boyunca aklimdan cikmadi. merak ediyorum, boyle seyler "
                     "baskalarinin da basina geliyor mu yoksa ben mi "
                     "abartiyorum"),
            ("assistant", None),
        ],
        "son": "Başkalarının başına gelip gelmediğini bilmiyorum. Bir sayı "
               "versem de o sayı dün akşamını değiştirmezdi.\n\n"
               "Abartıp abartmadığını da ben tartamam. Ama şunu görüyorum: "
               "sahne dün oldu ve sen akşam boyunca onu taşıdın. Abartma "
               "dediğin şey bu olmasa gerek — abartma geçer, bu geçmemiş.\n\n"
               "Torunun odasına gitti, sen hâlâ o anın içindesin. Bunu kimse "
               "sana hatırlatmadı; kendin hatırlıyorsun.",
        "thinking": "İki soru sormuş ve ikisi de bir rahatlama arıyor: "
                    "başkalarına da oluyor mu, abartıyor muyum.\n\n"
                    "Birincisine bir sayı uydurmam. 'Herkese oluyor' demek "
                    "kolay ama akşam boyunca taşıdığı şeyi hafifletmez, "
                    "yalnız üstünü örter.\n\n"
                    "İkincisine de hüküm vermiyorum. 'Abartmıyorsun' demek "
                    "bir onay, 'abartıyorsun' demek bir azar olurdu.\n\n"
                    "Telefon kullanımına dair bir sınır önermiyorum; sormadı "
                    "ve bu akşam söyleyeceği şey o değil.\n\n"
                    "Karşı çıkışım tek bir yerde ve kendi sözcüğüne: abartma "
                    "dediği şey geçer, oysa bu geçmemiş. Bunu söylemek onu "
                    "suçlamıyor, tarif ediyor.\n\n"
                    "Soru sormuyorum. Sonda takdir ettiğim şey hatırlamanın "
                    "kendisi: kimse hatırlatmadı.",
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
