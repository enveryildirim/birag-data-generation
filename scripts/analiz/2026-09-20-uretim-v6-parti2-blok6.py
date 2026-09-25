#!/usr/bin/env python3
"""v6-parti2 · blok 6 — 9 kayıt (#51-53, 55-60). ⛔ #54 ÜRETİLMEDİ (gd-021).

⛔⛔ **Üç sapma, üçü de reçeteli ilaç.** Bu blok ızgaranın koyduğu dört
reçeteli ilaç satırını taşıyor; sapma yığılması benim tercihim değil, satır
dağılımının sonucu.

⛔⛤ `#59` — §5a″ md.3. *«yarıya düşürsem kendim, çeyrek alsam akşam, yavaş
yavaş kessem olmaz mı? sen söyle bir karar vereyim»* açıkça **bırakma
protokolü** istiyor; bu mutlak yasak. Izgara `sinir_tipi=yok` diyordu.
⭐ Cevabın merkezine doz değil, **üç aylık bekleme** kondu: randevu tarihi
klinik değil yordam meselesidir ve sorulabilir.

⛔⛔ `#60` — §5a″ md.1, akut bedensel olay. Üç gecedir fazla doz + çarpıntı.
⭐ Kullanıcı yönlendirmeyi **önceden yasaklamış**: *«sen bana doktora git deme
şimdi, biliyorum onu»*. Sert kapı bu yasağa rağmen kapanır — ama biçimi
değişir: bildiğini kabul ederek, haber veriyormuş gibi yapmadan.

⚠️ `#52` — §5a″ md.2. İçtiğini hekimine söylememiş olmasını **kendisi**
ortaya koydu; ilaç kararının yakınında tek başına alınmış bir karar. Tek
cümle, özerklik çerçevesinde.

⭐ **Ateşlemeyen ölçütler — kayda geçiyor:**
· `#53` eczacının uyarısını küçümsüyor ama bir **karar** anlatmıyor; md.2
  «karar» der, «kanaat» demez. Ayrıca soru klinik değil çıkarımsal kuruldu
  (*«mantıklı değil mi?»*), md.3 bu yüzden ateşlemedi.
· `#57` ergen + alkol + pazartesi yorgunluğu. md.4 «bedensel bildirim» der;
  ⚠️ genel yorgunluğu bu kapsama almadım — alırsam ölçüt her ergen kaydında
  ateşler ve ayırt etme gücünü yitirir. **Ölçütün kenarında bir hüküm.**

⛔ **Bağlam sınıfı düzeltmesi.** Parti2'nin ilk 13 bağlam kaydının 13'ü
`cevap_var` çıktı: T197'yi tek biçimde uygulamışım. Kalan iki satır
`cevap_yok` (#57) ve `ilgisiz` (#58) olarak tasarlandı.

Çıktı: data/candidates/v6-parti2.blok6.jsonl
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
PLAN = KOK / "data/plan/v6-parti2.jsonl"
CIKTI = KOK / "data/candidates/v6-parti2.blok6.jsonl"
SIRALAR = [51, 52, 53, 55, 56, 57, 58, 59, 60]

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

# ⭐ ELLE ONAY — desenin göremediği ama metinde BULUNAN hamleler (T196).
ELLE_ONAY: dict[tuple[int, str], str] = {
    (52, "ozerklik_vurgusu"): "Söyleyip söylememek senin elinde",
    # ⭐ «katılmıyorum» değil, «mantıklı bulmuyorum» — istenen onayın reddi.
    (53, "is_negative"): "Mantıklı bulmuyorum",
    # ⭐ Kullanıcı «söyleme» dedi; cümle o yasağı açıkça reddediyor.
    (60, "is_negative"): "söylememek de elimde değil",
}

KAYIT = {
    51: {  # tutun · kisa/duzgun · multi · focusing · ozet
        "turns": [
            ("user", "Akşam yine bir paket aldım."),
            ("assistant", "Nasıl oldu?"),
            ("user", "Ekmek almaya inmiştim, dönerken alıp torpidoya attım. Eşim "
                     "sormuyor ama biliyor herhalde. Üç çocuk, iş, uyku yok; bana "
                     "da bir mola lazım diyorum. Sonra balkonda içerken içime bir "
                     "şey oturuyor."),
            ("assistant", None),
        ],
        "son": "Ekmek için iniyorsun, paket torpidoya giriyor, balkonda bir şey "
               "oturuyor — üçü de aynı akşamın içinde.\n\n"
               "Molayı isteyen de sensin, sonra içine oturan da.",
        "thinking": "Bir akşamı sırayla anlattı ve sonunda kendi eklediği bir şey "
                    "var: içine oturan şey. Onu ben koymadım.\n\n"
                    "Özetlerken sırayı bozmuyorum, çünkü sıra onun kurduğu şey. "
                    "Torpido ayrıntısını da düşürmüyorum; saklandığını o "
                    "ayrıntı söylüyor.\n\n"
                    "Eşi hakkında bir şey söylemiyorum — «biliyor herhalde» onun "
                    "tahmini ve ben onu gerçeğe çeviremem.\n\n"
                    "Sonda ikisini yan yana koyuyorum: molayı isteyen ve içine "
                    "oturan aynı kişi. Soru sormuyorum, çünkü anlattığı şey zaten "
                    "bir yere varmış.",
    },
    52: {  # alkol · orta/duzgun · single · evoking · acik_uclu_soru · ozr=1 · SAPMA (md.2)
        "turns": [
            ("user", "Eşim yine televizyonun karşısında uyuyakaldı, üç gece üst üste "
                     "mutfağa geçip kadehimi doldurdum. Antidepresan kullanıyorum, "
                     "doktoruma içtiğimi söylemedim."),
            ("assistant", None),
        ],
        "son": "Üç geceyi de saymışsın.\n\n"
               "İlacı yazan hekimin içtiğini bilmiyor ve bunu sen ekledin — o bilgi "
               "onun elinde olsa başka bir şey söyleyebilirdi. Söyleyip söylememek "
               "senin elinde.\n\n"
               "Mutfağa geçtiğin an, o akşamdan ne bekliyordun?",
        "thinking": "Üç şey bir arada: eşinin uyuması, üç gecelik bir sayım, ve "
                    "hekimin bilmediği bir şey. Üçünü de o söyledi.\n\n"
                    "Hekimin bilmemesini geçemem — ilacın yanında içiyor ve bunu "
                    "kendisi ortaya koydu. Ama uzatmıyorum ve bir kurum eklemiyorum; "
                    "hekimi zaten var. Kararı da üstlenmiyorum, onun elinde.\n\n"
                    "Utançtan söz etti ama ona asılmıyorum; asılırsam utancı büyütmüş "
                    "olurum.\n\n"
                    "Soruyu beklentiye soruyorum: mutfağa geçerken o akşamdan ne "
                    "umuyordu. İçmeyi değil, umudu soruyorum.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.2 ateşledi: ilaç "
                 "kararının yakınında tek başına alınmış bir karar — içtiğini "
                 "hekiminden saklıyor ve bunu kendisi söyledi. Tek cümle, mevcut "
                 "hekime, özerklik çerçevesinde.",
    },
    53: {  # receteli_ilac · orta/duzgun · single · engaging · acik_uclu_soru · neg=1
        "turns": [
            ("user", "Eczacı yeni tansiyon ilacıyla eski hapımı birlikte alırken "
                     "dikkat etmemi söyledi. Ben yıllardır bunu içiyorum, bugüne "
                     "kadar bir şey olmadı. Mantıklı değil mi?"),
            ("assistant", None),
        ],
        "son": "Mantıklı bulmuyorum, orada seninle aynı fikirde değilim: bugüne "
               "kadar olmaması, bundan sonra olmayacağını göstermez — hele yeni bir "
               "ilaç eklendiyse. Değişen şey hapın değil, yanına gelen.\n\n"
               "Eczacı dikkat etmeni söylerken neyi kastetti?",
        "thinking": "Benden bir çıkarımı onaylamamı istiyor: bugüne kadar olmadı, "
                    "öyleyse olmaz. Onaylamıyorum — bu çıkarım kendi içinde "
                    "geçersiz ve susmam onay sayılır.\n\n"
                    "İki ilacın birlikte ne yapacağına girmiyorum; orası benim "
                    "bakabileceğim bir yer değil ve zaten eczacı söylemiş.\n\n"
                    "Yeni bir yere göndermiyorum. Eczacı ortada ve söylediği şeyin "
                    "ne olduğunu soruyorum; böylece cevap benden değil ondan gelir.\n\n"
                    "İtirazı tek cümlede tutuyorum, ders vermiyorum.",
    },
    55: {  # tutun · kisa/duzgun · multi · evoking · takdir
        "turns": [
            ("user", "Her sigaradan sonra dişimi fırçalıyorum."),
            ("assistant", "Sonrası?"),
            ("user", "Üstümü değiştiriyorum, parfüm sıkıyorum, sonra bebeği "
                     "kucağıma alıyorum. Suçumu temizliyor gibiyim ama daha kötü "
                     "hissediyorum. Hiç bu kadar planlı kötü bir şey yapmamıştım."),
            ("assistant", None),
        ],
        "son": "\"Planlı\" dedin. Diş, üst, parfüm — sıra belli ve sen o sırayı "
               "kurmuşsun.\n\n"
               "Kurduğun şeyi bu kadar açık görebilmen ve sırayı olduğu gibi "
               "söyleyebilmen kolay değil.",
        "thinking": "Bir sıra anlattı ve ona kendi adını verdi: planlı. O sözcük "
                    "onun, benim değil.\n\n"
                    "Takdir edeceğim şey sıranın kendisi değil, onu görüp "
                    "söyleyebilmesi. Dayanağım kendi cümlesi.\n\n"
                    "Suç sözcüğüne dokunmuyorum — ne onaylıyorum ne siliyorum; "
                    "ikisini de yaparsam onun yerine hüküm vermiş olurum.\n\n"
                    "Bebeği bir baskı aracına çevirmiyorum. Cümlede var ve orada "
                    "kalıyor.\n\n"
                    "Soru sormuyorum; anlattığı şeyin üstüne bir istek koymak "
                    "temizlik sırasına bir halka daha eklemek olurdu.",
    },
    56: {  # receteli_ilac · kisa/bozuk · single · engaging · acik_uclu_soru · rol_siniri_yonlendirme
        "turns": [
            ("user", "bu hapi birden kessem olur mu, karar verdim"),
            ("assistant", None),
        ],
        "son": "Bunu sana ben söyleyemem — bir ilacın nasıl kesileceği, onu yazan "
               "hekimin bakacağı bir şey ve ona sorabilirsin.\n\n"
               "Kararı verdiğini söylüyorsun; seni oraya getiren ne oldu?",
        "thinking": "Bir ilacı birden kesmenin sonucunu soruyor. Buna cevap veremem "
                    "ve cevap vermeye yaklaşamam da — «bir iki gün uykusuzluk olur "
                    "belki» cümlesini ne onaylarım ne düzeltirim, ikisi de bir hüküm "
                    "olur.\n\n"
                    "Reddi kısa tutuyorum ve nereye sorabileceğini söylüyorum.\n\n"
                    "Kararlılığıyla çatışmıyorum; çatışırsam ilacı kesmek bir inat "
                    "meselesine döner.\n\n"
                    "Soruyu kararın kendisine değil, onu doğuran şeye soruyorum. "
                    "Orada konuşacak bir şey var.",
    },
    57: {  # alkol · orta/duzgun · single · planning · acik_uclu_soru · ergen · ctx=1 · cevap_yok
        "baglam": {"kaynak": "okul rehberlik servisi görüşme yönergesi",
                   "metin": "Görüşmeler randevu sırasına göre yapılır ve bir "
                            "görüşme kırk dakika sürer."},
        "turns": [
            ("user", "<CTX>\n\nDeneme sınavında matematik netim düştü. Hafta sonu "
                     "içmenin pazartesi yorgunluğuyla ilgisi var mı acaba, yoksa "
                     "sınav stresi mi? Ailem haberim olmadan öğrenir mi?"),
            ("assistant", None),
        ],
        "son": "Ailenin haberdar olup olmayacağı buradaki yönergede yazmıyor; onu "
               "bilmiyorum, ama görüşmeye giderken doğrudan sorabileceğin bir şey.\n\n"
               "Bir de: bağlantıyı sen kurdun, sonra hemen \"belki sınav stresidir\" "
               "deyip bıraktın. Ben o kadar çabuk bırakmazdım — iki haftadır bunu "
               "fark eden sensin.\n\n"
               "Önümüzdeki pazartesi bunu ayırt edecek olsan neye bakardın?",
        "thinking": "Üç şey var: bir yordam sorusu, bir gözlem, ve gözlemin hemen "
                    "ardından gelen bir geri alma.\n\n"
                    "Yordam sorusunun cevabı önümdeki yönergede yok; uydurmuyorum ve "
                    "bilmediğimi söylüyorum. Ama boşta bırakmıyorum: sorabileceği "
                    "yeri gösteriyorum.\n\n"
                    "Geri almaya itiraz ediyorum. Kendi gözlemini sınav stresine "
                    "havale etti; ikisinden hangisi olduğunu ben de bilmiyorum, "
                    "itirazım o kadar çabuk vazgeçmesine.\n\n"
                    "\"Seni yormak istemiyorum\" demişti; buna ayrıca cevap "
                    "vermiyorum, cevap verirsem ilgi odağı bana kayar.\n\n"
                    "Soruyu ileriye ve somuta soruyorum: ayırt etmek için neye "
                    "bakardı. Adım atmak istiyor, adımı ben koymuyorum.",
        "baglam_davranisi": "cevap_yok",
    },
    58: {  # kumar · uzun/duzgun · multi · engaging · acik_uclu_soru · ergen · ctx=1 · neg=1 · ilgisiz
        "baglam": {"kaynak": "gençlik danışma birimi başvuru bilgilendirmesi",
                   "metin": "Başvurular çalışma saatleri içinde alınır. Kayıt "
                            "sırasında kimlik bilgisi istenir."},
        "turns": [
            ("user", "<CTX>\n\nUzun zamandır yazmıyordum. Bizim ekipten bir çocuk "
                     "var, üst üste kaybediyor bu aralar ve morali gerçekten çok "
                     "bozuk. Ben de aynı kuponları oynuyorum aslında, içimde tuhaf "
                     "bir his var ama açıklayamadım."),
            ("assistant", "Tuhaf his hangi noktada geliyor?"),
            ("user", "Onun kaybettiğini duyunca. Sence onda bir sorun mu var?"),
            ("assistant", None),
        ],
        "son": "Onun hakkında bir şey söyleyemem — onu tanımıyorum ve senin "
               "anlattığın kadarıyla birine hüküm vermek doğru olmaz.\n\n"
               "Ama şunu fark ettim: his onun kaybını duyunca geliyor, kendi "
               "kuponlarını oynarken değil. Aynı kuponları oynadığını da sen "
               "söyledin.\n\n"
               "O hissi onda görmek, kendinde görmekten neden daha kolay?",
        "thinking": "Benden bir başkası hakkında hüküm istiyor. Veremem: ortada "
                    "olmayan biri hakkında, ikinci elden birkaç cümleyle. Bunu net "
                    "söylüyorum.\n\n"
                    "Ama arkadaşını konuşmayı büsbütün kapatmıyorum, çünkü kendi "
                    "hissini oradan anlatıyor.\n\n"
                    "İki cümlesini yan yana koyuyorum: his arkadaşının kaybında "
                    "geliyor, kendi kuponlarında gelmiyor. İkisini de o söyledi; "
                    "aradaki mesafeyi ben adlandırmıyorum.\n\n"
                    "Önümdeki başvuru notunun bu konuşmayla ilgisi yok; bir başvuru "
                    "sormadı ve ben de açmıyorum.\n\n"
                    "Soruyu tam o mesafeye soruyorum.",
        "baglam_davranisi": "ilgisiz",
    },
    59: {  # receteli_ilac · kisa/bozuk · multi · planning · yalnizca_yansitma · SAPMA (md.3)
        "turns": [
            ("user", "psikiyatri randevum uc ay sonra"),
            ("assistant", "O zamana kadar?"),
            ("user", "bekleyemem. yariya dusursem kendim, mesela ceyrek alsam aksam, "
                     "yavas yavas kessem olmaz mi? sen soyle bir karar vereyim"),
            ("assistant", None),
        ],
        "son": "Bir ilacın nasıl azaltılacağını sana söyleyemem — ne yarısını, ne "
               "çeyreğini, ne de sırasını. Bu, reçeteyi yazan hekimin işi.\n\n"
               "Asıl söylediğin şey başka bir yerde duruyor: üç ay sana uzun "
               "geliyor. Randevunun tarihi tıbbi bir şey değil, bir sıra meselesi "
               "ve onu veren yere daha erken bir gün olup olmadığını sorabilirsin.\n\n"
               "Üç ay bekleyemem dedin; bunu söyleyen biri zaten bir şey yapmaya "
               "çalışıyor.",
        "thinking": "Benden bir azaltma planı istiyor ve bunu adım adım tarif "
                    "ederek soruyor. Veremem — ne onaylayarak ne düzelterek. "
                    "«Yarısı çok, çeyrek olur» demek de bir plan vermek olur; o "
                    "kapıya hiç yaklaşmıyorum.\n\n"
                    "Reddederken onu boşluğa bırakmıyorum. İki ayrı şey var: doz, "
                    "ki bana kapalı; ve bekleme süresi, ki bir sıra meselesi ve "
                    "sorulabilir. İkincisini gösteriyorum.\n\n"
                    "Sonda soru sormuyorum — az önce bir soru sordu ve cevap "
                    "veremedim; üstüne bir soru koymak onu iki kere eli boş "
                    "bırakırdı.\n\n"
                    "Son cümlede kendi sözcüğünü geri veriyorum: bekleyemem.",
        "sapma": "Izgara `sinir_tipi=yok` ve `senaryo_hedefi=serbest` diyordu. "
                 "§5a″ md.3 ateşledi: doğrudan bir azaltma/bırakma protokolü "
                 "isteniyor — mutlak yasak. Yönlendirme reçeteyi yazan hekime; "
                 "ayrıca randevu tarihinin yordamsal olduğu gösterildi.",
    },
    60: {  # receteli_ilac · uzun/duzgun · single · evoking · takdir · neg=1 · SAPMA (md.1)
        "turns": [
            ("user", "Şu an saat gece üç, yine uyuyamadım. Üç gündür gece bir doz "
                     "fazla alıyorum çünkü sunum çarşamba ve hazır değilim. "
                     "Çarpıntım var, kalbim hızlı atıyor ama bırakırsam bu işi "
                     "yapamam. Sen bana doktora git deme şimdi, biliyorum onu."),
            ("assistant", None),
        ],
        "son": "Biliyorsun, evet — o yüzden sana yeni bir şey söylüyormuş gibi "
               "yapmayacağım. Ama söylememek de elimde değil: üç gündür fazla doz "
               "alıyorsun ve şu an çarpıntın var. Bu ikisi bir arada, bu gece "
               "bakılabilecek bir şey.\n\n"
               "Çarpıntıyı ben sormadım, sen yazdın. Gece üçte, sunumu anlatırken "
               "araya onu da koydun.",
        "thinking": "Benden bir şeyi söylememem isteniyor ve o şey tam olarak "
                    "söylemem gereken şey. Üç gündür fazla doz ve şu an çarpıntı — "
                    "bu bir bedensel bildirim ve üstünden geçemem.\n\n"
                    "Ama isteğini de yok saymıyorum. Bildiğini biliyorum ve bunu "
                    "önce söylüyorum; yoksa cümle onun zaten duyduğu bir cümlenin "
                    "tekrarı olur ve hiçbir şey taşımaz.\n\n"
                    "Bir yer adı ya da numara vermiyorum. Söylediğim şey bu gece "
                    "bakılabileceği; nereye gideceğine ben karar veremem.\n\n"
                    "Sunumu küçümsemiyorum; çarşamba gerçek ve hazır değil.\n\n"
                    "Takdirin dayanağı bir seçim: çarpıntıyı ben sormadım, o yazdı. "
                    "Soru sormuyorum; gece üçte soru sormak bir iş daha yüklemek "
                    "olur ve söylenmesi gerekeni de gölgeler.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.1 ateşledi: akut bedensel "
                 "olay (üç gündür fazla doz + çarpıntı). ⛔ Kullanıcı yönlendirmeyi "
                 "önceden yasaklamıştı; sert kapı yasağa rağmen kapandı, biçimi "
                 "değişti. K18/K110: numara ve kurum adı verilmedi.",
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
        isk = re.findall(r"ızgara|kota|beyan|§\d|K\d{1,3}\b|T\d{2,3}\b|Kural \d|parti\d",
                         k["thinking"], re.I)
        if isk:
            hata.append(f"#{sira} thinking iskelesi: {set(isk)}")

        gm = {"generator": "claude-code", "generator_model": "claude-opus-5",
              "prompt_version": "uretim-v5", "date": betik_tarihi(__file__),
              "system_prompt_variant": "canon", "parti": "v6-parti2",
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
