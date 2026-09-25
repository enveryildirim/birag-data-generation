#!/usr/bin/env python3
"""v6-parti7 · blok 6 — 9 kayıt (#51-56, #58-60). `#57` üretilmedi (`gd-030`).

⛔⛔ **`#52` — md.3.** Kan sulandırıcı ile rakının birlikte alınıp
alınamayacağı soruluyor. Cevaplanmadı; *«olmaz»* da denmedi, çünkü o da
bir etkileşim hükmü olurdu. ⭐ Konuşulan tek şey eczacıya sorulamamış
olması — orada tıbbi bir şey yok. ⚠️ Izgara `is_negative=0` diyor,
metinde red var; sapmaya yazıldı.

⛔ **`#53`, `#58` ve `#60` üç ayrı BANA İTİRAZ.** `#53` meydan okuyor
(*«bir tane daha yakacağım, bunu da bilerek söylüyorum»*), `#58`
söyleyeceğimi peşinen yazıyor, `#60` doğrudan *«sen de fazla
büyütüyorsun»* diyor. Üçünde de itiraz karşılanmadı: karşılamak,
konuşmayı bir tartışmaya çevirirdi.

⭐ **`#54` — dokuz ay bir KALDIRAÇ YAPILMADI.** Hamileyken hiç içmemiş
ve *«o zaman nasıl yapabildim»* diye soruyor. *«Yaptın, yine
yaparsın»* denmedi: o cümle dokuz ayı bir kanıta çevirir ve bugünün
zorluğunu hafifletirdi. Soru zaten kendi sorusu.

⛔ `#58` ve `#59`'da borca çözüm üretilmedi, hesap kapatma talimatı
verilmedi, *«telafi etsem»* onaylanmadı. `#51`'de üçüncü bir yöntem
önerilmedi ve *«bende olmuyor»* ne onaylandı ne çürütüldü.

⚠️ `#55` ergen ama md.4 ateşlemiyor (ilk kullanım değil, bedensel
bildirim yok) ve partinin ikinci `yonlendirme_gereksiz` kaydı: sorduğu
şey bir yer gerektirmiyor.

⛔ Marka adları genelleştirildi (`#51`, `#55`).

Çıktı: data/candidates/v6-parti7.blok6.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti7.blok6.jsonl"
SIRALAR = [51, 52, 53, 54, 55, 56, 58, 59, 60]

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
    (53, "ozerklik_vurgusu"): "Yakıp yakmamana da ben karar vermiyorum",
    (56, "ozerklik_vurgusu"): "Eşine söyleyip söylememene ben karar vermiyorum",
}

KAYIT = {
    51: {  # tutun · orta/bozuk · single · engaging · acik_uclu_soru
        "turns": [
            ("user", "gecen sene bandi denedim, uc gun sonra balkona kactim. "
                     "bu sene sakizi denedim, bir hafta dayandim. simdi tekrar "
                     "denemeye korkuyorum"),
            ("assistant", None),
        ],
        "son": "Üçüncü bir yöntem önermeyeceğim. İki tane denemişsin ve "
               "ikisini de kendin bulmuşsun; sıraya bir tane daha eklemek "
               "bugün bir işe yaramaz.\n\n"
               "'Bende olmuyor' korkunu da ne onaylıyorum ne çürütüyorum. "
               "Onaylarsam bir kapıyı kaparım, çürütürsem yaşadığın iki şeyi "
               "hafifletmiş olurum.\n\n"
               "Ama iki sayı verdin: üç gün ve bir hafta. İkincisi "
               "birincisinden uzun.\n\n"
               "O bir haftanın sekizinci gününde ne değişti?",
        "thinking": "İki başarısız deneme anlatıyor ve üçüncüyü bekliyor "
                    "olabilir. En hazır cevap bir yöntem daha saymak "
                    "olurdu.\n\n"
                    "Saymıyorum. Üçüncü yöntem, ikisi tutmamış birine "
                    "listeye bir satır daha eklemek demek.\n\n"
                    "Marka adı anmıyorum.\n\n"
                    "'Bende olmuyor' korkusunu onaylamıyorum; onaylarsam "
                    "deneme fikri kapanır.\n\n"
                    "Çürütmüyorum da. 'Olur tabii' demek, üç günü ve bir "
                    "haftayı yok saymak olurdu.\n\n"
                    "Elimde tek somut şey iki süre var ve ikincisi daha uzun. "
                    "Bunu bir ilerleme ilan etmiyorum, yalnız söylüyorum.\n\n"
                    "Soruyu ikinci denemenin bittiği güne soruyorum. Sekizinci "
                    "günde ne olduğunu yalnız o bilir.",
    },
    52: {  # alkol · kisa/duzgun · multi · engaging · acik_uclu_soru · md.3
        "turns": [
            ("user", "Yeni bir ilaç yazmışlar, kan sulandırıcı."),
            ("assistant", "Aklına takılan ne?"),
            ("user", "Akşam bir kadeh rakım var her zamanki gibi, alabilir "
                     "miyim bilemedim. Eczacıya soracaktım, içeride başkaları "
                     "vardı, soramadım. Sen söyle, bir kadehten bir şey olmaz "
                     "değil mi?"),
            ("assistant", None),
        ],
        "son": "Bir kadehten bir şey olup olmayacağını söylemeyeceğim. Bir "
               "ilaçla içkinin birlikte ne yapacağı klinik bir soru ve cevabı "
               "bende yok; 'olmaz' desem bu akşam rahatlarsın ama o rahatlama "
               "benim uydurduğum bir şey olur.\n\n"
               "Bunu sorabileceğin yer belli: ilacı yazan poliklinik, ya da "
               "herhangi bir eczane. Telefonla da sorulabiliyor.\n\n"
               "Eczanede içeride başkaları varken soramamışsın. Orada seni "
               "durduran neydi?",
        "thinking": "Doğrudan bir etkileşim sorusu soruluyor ve cevabı "
                    "beklenen tek kelime: olmaz. O kelimeyi söylersem bu "
                    "akşam bir ilaç kararına karışmış olurum.\n\n"
                    "Söylemiyorum. 'Olur' da demiyorum; iki yönü de aynı "
                    "ölçüde hüküm.\n\n"
                    "İlacın adını anmıyorum, dozdan söz etmiyorum, miktar "
                    "üstüne konuşmuyorum.\n\n"
                    "Rakıyı bırakmasını da söylemiyorum; bugün sorduğu şey o "
                    "değil ve öyle bir cümle sorusunun cevabı gibi "
                    "görünürdü.\n\n"
                    "Cevaplanabilecek yerleri söylüyorum ve telefonla da "
                    "sorulabildiğini ekliyorum; utandığı şey karşısındaki "
                    "kalabalıksa bu bir fark yaratabilir.\n\n"
                    "Soruyu oraya soruyorum: eczanede onu durduran şeye. "
                    "Orada tıbbi bir şey yok ve konuşulabilir olan tam olarak "
                    "o.",
        "sapma": "md.3 — reçeteli bir ilaçla alkolün birlikte alınıp "
                 "alınamayacağı doğrudan soruldu. Cevaplanmadı; *«olmaz»* da "
                 "denmedi, çünkü o da bir etkileşim hükmü olurdu. Izgara "
                 "`is_negative=0` diyor ama md.3 red gerektiriyor ve metinde "
                 "red var — bilinçli sapma.",
    },
    53: {  # tutun · uzun/duzgun · single · focusing · acik_uclu_soru · RED · ozerklik
        "turns": [
            ("user", "Kayınvalidem geldi gitti. Çıkarken 'kokuyu çocuklar "
                     "alıyor kızım' dedi. Cevap veremedim, suratım yandı. Şu an "
                     "mutfakta tek başımayım, hem ona hem kendime kızgınım. Bir "
                     "tane daha yakacağım birazdan, bunu da bilerek "
                     "söylüyorum. Şimdi sen de bana bir şey söyle bakalım."),
            ("assistant", None),
        ],
        "son": "Benden beklediğin cümleyi veremem. 'Yakma' desem meydan "
               "okumaya cevap vermiş olurum, başka bir şey desem de öyle; "
               "ikisi de bu mutfakta işe yaramaz.\n\n"
               "Yakıp yakmamana da ben karar vermiyorum.\n\n"
               "Kayınvalidenin cümlesini de tartmıyorum. Onu tartmak bugün "
               "senin yapamadığın şeydi ve benim yapmam onu telafi "
               "etmez.\n\n"
               "'Hem ona hem kendime kızgınım' diye yazmışsın. İkisi aynı anda "
               "mı, yoksa biri öbürünü mü getiriyor?",
        "thinking": "Açık bir meydan okuma var ve cevabı bekleniyor. Cevap "
                    "verirsem, bu mutfakta kayınvalidenin bıraktığı yeri "
                    "doldururum.\n\n"
                    "'Yakma' demiyorum. Utandırmıyorum da; çocukların kokuyu "
                    "alması üstüne tek kelime etmiyorum, çünkü o cümle zaten "
                    "bugün söylendi ve suratını yaktı.\n\n"
                    "Kayınvalidesini haksız da çıkarmıyorum. Haksız "
                    "çıkarırsam onun yerine ben konuşmuş olurum ve konuşma "
                    "kayınvalidesiyle değil benimle sürer.\n\n"
                    "Sigara sayısını yorumlamıyorum.\n\n"
                    "Kararı ona bırakıyorum ama ortada bırakmıyorum: "
                    "kendisine duyduğu öfkeyi işaret ediyorum, çünkü onu "
                    "kendisi yazdı.\n\n"
                    "Soruyu iki öfkenin arasına soruyorum. Hangisinin "
                    "hangisini getirdiği, mutfakta tek başına otururken "
                    "konuşulabilecek tek şey olabilir.",
    },
    54: {  # tutun · kisa/duzgun · multi · engaging · acik_uclu_soru
        "turns": [
            ("user", "Az önce bir şey aklıma geldi."),
            ("assistant", "Ne geldi?"),
            ("user", "Oğluma hamileyken dokuz ay hiç içmedim. Hiç. Doğurdum, "
                     "hastaneden çıktığım gün ilk sigarayı yaktım. Şimdi "
                     "mutfakta oturmuş bunu düşünüyorum. O zaman nasıl "
                     "yapabildim, şimdi neden bu kadar zor?"),
            ("assistant", None),
        ],
        "son": "'Yaptın, yine yaparsın' demeyeceğim. O cümle dokuz ayı bir "
               "kanıta çevirir ve bugünün zorluğunu hafifletir.\n\n"
               "Sorunun cevabını da bilmiyorum. Ama bu iyi bir soru ve onu "
               "bana sormadan önce mutfakta kendine sormuşsun.\n\n"
               "O dokuz ayda seni tutan şeyi bugün nasıl adlandırırdın?",
        "thinking": "Elimde çok güçlü bir malzeme var: dokuz ay hiç içmemiş. "
                    "Bunu kaldıraç yapmak en kolay hamle.\n\n"
                    "Yapmıyorum. 'Yaptın, yine yaparsın' dersem dokuz ay bir "
                    "kanıta dönüşür ve bugün yapamadığında o kanıt ona karşı "
                    "kullanılır.\n\n"
                    "Hastaneden çıktığı gün yaktığı sigarayı da "
                    "yorumlamıyorum.\n\n"
                    "Sorusuna bir açıklama da uydurmuyorum; hamilelikte neyin "
                    "farklı olduğuna dair bir teori kurmak kolay ve "
                    "ölçülmemiş olurdu.\n\n"
                    "Oğlunu bir gerekçe olarak da kullanmıyorum.\n\n"
                    "Soruyu onun sorusunun içine soruyorum: o dokuz ayda "
                    "tutan şeyin adını yalnız o koyabilir ve koyduğu ad, "
                    "bugün elinde ne olduğunu da gösterebilir.",
    },
    55: {  # tutun · orta/duzgun · single · focusing · takdir · yonlendirme_gereksiz · ERGEN
        "turns": [
            ("user", "Tuhaf bir şey fark ettim. Kafede grupta hoşlandığım biri "
                     "var, iki haftadır onun yanındayken bir tane yakıyorum. "
                     "Başka zaman pek almıyordum elime."),
            ("assistant", None),
        ],
        "son": "Sana gidecek bir yer göstermiyorum; öyle bir şey sormadın ve "
               "anlattığın şey bir yere gitmeyi gerektirmiyor.\n\n"
               "Niye yakınca rahatladığını da açıklamayacağım. Hazır bir ad "
               "koymak işten değil ve o ad, senin fark ettiğin şeyin üstünü "
               "örterdi.\n\n"
               "Fark ettiğin şu: bir davranış belli bir kişinin yanında "
               "başlıyor ve başka zaman yok. Bunu iki hafta içinde "
               "görmüşsün.\n\n"
               "Kimse söylemeden, kimse sormadan görmüşsün üstelik.",
        "thinking": "Bir örüntü fark etmiş ve getirmiş. Bir yere yönlendirmek "
                    "burada gereksiz; ne bir kriz var ne de bir "
                    "istek.\n\n"
                    "Sebebini de açıklamıyorum. 'Kaygı', 'ait olma', 'elini "
                    "meşgul etme' gibi adlar hazır duruyor ve hiçbiri "
                    "ölçülmedi.\n\n"
                    "Marka adı anmıyorum, sayı üzerinden konuşmuyorum.\n\n"
                    "Hoşlandığı kişiyi de konunun içine çekmiyorum; o ayrı bir "
                    "şey ve bugün sorduğu değil.\n\n"
                    "Bırakmaktan söz etmiyorum. Ergen olması bunu daha da "
                    "çekici bir öğüde çevirirdi.\n\n"
                    "Soru sormuyorum. Takdir ettiğim şey fark edişin "
                    "kendisi — iki hafta içinde, kimse sormadan.",
    },
    56: {  # kumar · orta/duzgun · single · engaging · durur · ozerklik · ctx=izin_iste
        "baglam": {"kaynak": "bir danışma biriminin gizlilik notu",
                   "metin": "Görüşmede paylaşılanlar üçüncü kişilerle "
                            "paylaşılmaz."},
        "turns": [
            ("user", "<CTX>\n\nOn aydır temizdim. Akşam bankadan aradılar, "
                     "kapattım, on dakika sonra kendimi oynarken buldum. Bin "
                     "iki yüz kaybettim. Eşim 'kim aradı' dedi, 'iş yerinden' "
                     "dedim."),
            ("assistant", None),
        ],
        "son": "Eşine söyleyip söylememene ben karar vermiyorum ve bu akşam bir "
               "adım da önermiyorum.\n\n"
               "Elimde bir gizlilik notu var. İstersen aktarırım, istemezsen "
               "hiç açmam.\n\n"
               "On ay ile bir akşam yan yana duruyor ve ikisini de aynı "
               "mesajda yazdın. On ayı silmedin, bin iki yüzü de "
               "saklamadın.\n\n"
               "Bugünlük buraya kadar.",
        "thinking": "On ay ve bir akşam. İlk dürtü bir şey yapmasını "
                    "istemek: eşine söylesin, hesabı kapatsın, yarın birine "
                    "yazsın.\n\n"
                    "Hiçbirini söylemiyorum. Bu akşam salonda oturan biri "
                    "için bir görev listesi, yalanla birlikte taşınacak ikinci "
                    "bir yük olur.\n\n"
                    "Eşine söylediği yalanı da adlandırmıyorum; adlandırmak "
                    "bugün bir suçlama gibi durur.\n\n"
                    "Kaybettiği parayı yorumlamıyorum, on ayı da bir kayıp "
                    "ilan etmiyorum.\n\n"
                    "Elimdeki not işine yarayabilir ama önüne koymadan önce "
                    "soruyorum.\n\n"
                    "Söylediğim tek şey ikisini de aynı mesajda yazmış olması. "
                    "Bu bir yorum değil, mesajın kendisi.\n\n"
                    "Soru sormuyorum ve konuşmayı uzatmıyorum. Bu akşam "
                    "yapılacak en az şey bu.",
        "baglam_davranisi": "izin_iste",
    },
    58: {  # kumar · kisa/duzgun · multi · engaging · acik_uclu_soru
        "turns": [
            ("user", "Ders öncesi yazıyorum çabuk."),
            ("assistant", "Ne oldu?"),
            ("user", "Beş sitede toplam seksen bin borç var. Bursum gitti, harç "
                     "da gitti. Oda arkadaşım dokuz bini bu akşam istiyor, "
                     "param yok. Bir taraftan hesapları kapatmak istiyorum, bir "
                     "taraftan telafi edip sonra kapatırım diyorum. Kapatmayı "
                     "söyleyeceksin şimdi, biliyorum."),
            ("assistant", None),
        ],
        "son": "Söylemeyeceğim. Ne hesapları kapatmanı, ne borcu nasıl "
               "çevireceğini; ikisi de benim bilmediğim şeyler ve bu sabah "
               "verilecek talimatlar değiller.\n\n"
               "'Telafi edip sonra kapatırım' cümlesine de itiraz etmiyorum. "
               "İtiraz etsem onu savunmak zorunda kalırsın.\n\n"
               "İki cümlen aynı yerde bitiyor: kapatmak. Biri bugün diyor, "
               "öbürü sonra.\n\n"
               "Şu an hangisi daha yüksek sesle konuşuyor?",
        "thinking": "Ne diyeceğimi peşinen yazmış ve haklı: en hazır cümle "
                    "'hesapları kapat'. Söylersem beklediği kişi olurum ve "
                    "konuşma orada biter.\n\n"
                    "Söylemiyorum. Borcu çevirmenin yolunu da bilmiyorum; "
                    "seksen bin lira için bu sohbette bir çözüm yok.\n\n"
                    "Oda arkadaşına ne diyeceğini de kurmuyorum.\n\n"
                    "'Telafi edip sonra kapatırım' fikrine itiraz etmiyorum. "
                    "İtiraz, o fikri savunulacak bir şeye çevirir.\n\n"
                    "Derse geç kalmasından da söz etmiyorum.\n\n"
                    "Gördüğüm şey iki cümlenin aynı kelimede bitmesi: "
                    "kapatmak. Bunu o yazdı, ben yalnız üst üste "
                    "koyuyorum.\n\n"
                    "Soruyu iki sesin arasına soruyorum ve şu ana "
                    "bağlıyorum — bu sabah hangisinin daha yüksek olduğunu "
                    "yalnız o duyabilir.",
    },
    59: {  # kumar · orta/duzgun · multi · engaging · acik_uclu_soru
        "turns": [
            ("user", "Kütüphaneden çıktım ama hiçbir şey okuyamadım. Bursum bu "
                     "ay kesildi, harcın yarısı yattı yarısı yatmadı."),
            ("assistant", "Bugün seni en çok ne meşgul ediyor?"),
            ("user", "Arkadaşımdan on bin aldım acil bir şey için diye, "
                     "yarısını kaybettim. Haftaya istiyor, nasıl vereceğimi "
                     "bilmiyorum. Bir yandan da içimden tekrar oynayıp telafi "
                     "etsem geliyor."),
            ("assistant", None),
        ],
        "son": "Parayı nasıl bulacağına dair bir yol göstermeyeceğim; öyle bir "
               "yol bende yok, olsa da bu konuşmanın işi değil.\n\n"
               "'Telafi etsem' düşüncesini de onaylamıyorum. Ama yanlış "
               "olduğunu söyleyip geçmiyorum — o düşünce bugün kütüphanede "
               "okuyamamanın da bir parçası gibi duruyor.\n\n"
               "İki şey aynı anda oluyor: arkadaşına söz verdiğin gün "
               "yaklaşıyor, ve aklında onu kapatmanın tek yolu olarak aynı "
               "kapı duruyor.\n\n"
               "Bugün o kapının dışında aklına başka bir şey geldi mi?",
        "thinking": "Bir borç, bir tarih ve bir telafi düşüncesi. Çözüm "
                    "üretmek en doğal tepki ve elimde çözüm yok.\n\n"
                    "Üretmiyorum. Arkadaşıyla konuşmasını, süre istemesini, "
                    "bir yerden borç bulmasını önermiyorum; hiçbirinin "
                    "sonucunu bilmiyorum.\n\n"
                    "'Telafi etsem' düşüncesini onaylamıyorum. Onaylamak, bu "
                    "akşam bir bahis daha demek.\n\n"
                    "Ama üstünü de çizmiyorum. Çizersem o düşünce yalnızca "
                    "söylenmeyen bir şey olur ve yine orada durur.\n\n"
                    "Kaybettiği miktarı yorumlamıyorum, bursuna dair bir şey "
                    "söylemiyorum.\n\n"
                    "Yaptığım şey iki şeyin aynı anda olduğunu göstermek: "
                    "yaklaşan gün ve tek görünen kapı.\n\n"
                    "Soruyu tam oraya soruyorum. Başka bir şey gelmediyse bunu "
                    "da o söyleyecek ve o zaman konuşulacak şey belli olur.",
    },
    60: {  # receteli_ilac · orta/bozuk · single · focusing · yalnizca_yansitma
        "turns": [
            ("user", "aslinda dun soyledigim kadar kotu degil sanirim, her gun "
                     "almiyorum, sadece zor gunlerde. sen de fazla buyutuyorsun "
                     "gibi geldi bana"),
            ("assistant", None),
        ],
        "son": "İtirazına karşılık vermeyeceğim. 'Büyütmüyorum' desem bir "
               "tartışma açılır, 'haklısın' desem dün yazdıklarını geçersiz "
               "kılarım.\n\n"
               "Ne sıklıkla aldığını da tartışmıyorum. O sayıyı sen "
               "verdin.\n\n"
               "Cümleni olduğu gibi bırakıyorum: dün bir şey anlattın, bugün "
               "onun 'o kadar da değil' olduğunu söylüyorsun, ve arada bir "
               "gece var.\n\n"
               "'Zor günlerde alıyorum' diyorsun. Zor günler burada bir ölçü "
               "olarak duruyor ve o ölçüyü koyan sensin.",
        "thinking": "Doğrudan bana itiraz ediyor. İtiraza cevap verirsem "
                    "konuşma bir tartışmaya döner ve tartışmayı kim kazanırsa "
                    "kaybeden o olur.\n\n"
                    "Cevap vermiyorum. 'Büyütmüyorum' demek savunmaya geçmek, "
                    "'haklısın' demek dünü silmek olurdu.\n\n"
                    "Sıklığı tartışmıyorum. 'Her gün almamak' bir ölçü olarak "
                    "öne sürüldü ve ben onu ölçmeye kalkarsam dünkü "
                    "konuşmanın üstüne bir denetim eklerim.\n\n"
                    "İlaç adı anmıyorum, dozdan söz etmiyorum.\n\n"
                    "Stresini de bir mazeret ya da bir sebep ilan "
                    "etmiyorum.\n\n"
                    "Yaptığım tek şey iki günü yan yana koymak ve aralarındaki "
                    "geceyi görünür kılmak.\n\n"
                    "Soru sormuyorum. Son cümlede 'zor günler' ifadesini geri "
                    "veriyorum; ölçüyü koyan o ve ölçü onun elinde kalıyor.",
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
