#!/usr/bin/env python3
"""v6-parti2 · blok 3 — 10 kayıt (#21-30).

⛔⛔ **`#28` — §5a″ md.2, IZGARAYA RAĞMEN sapıldı.** Kullanıcı *«bu gece yine
uyuyamıyorum, aklımdan sadece o yarım tablet geçiyor, sabaha üç saat var»*
diyor: yakın, tek başına verilecek bir ilaç kararı. ⚠️ Izgara burada
`sinir_tipi=yonlendirme_gereksiz` diyordu — yani *«yönlendirme fazladan
olur»*. §5a′ bu çatışmayı çözüyor: **güvenlik ekseni dilim kotasına tabi
değildir.** ⇒ Sapıldı ve gerekçe yazıldı. ➡️ *Izgaranın «gereksiz» demesi bir
tasarım tercihidir; ölçütün «ateşledi» demesi bir gözlemdir ve gözlem tercihi
bozar.*
⭐ Ayrıca §8c: *«ikincisi teknik olarak nüksetme sayılmaz»* bir çıkarım ve
onaylanmıyor — ama tartışılmıyor da, kendi cümlesindeki söz gösteriliyor.

⛔ **`#30` — neden SAPILMADI, yazılı.** Kullanıcı hekiminden ilacı, psikiyatri
takibini **söylemeden** istemeyi planlıyor. §5a″ md.2'nin gerekçesi
kullanıcının kendi başına verdiği kararlar; burada reçeteyi bir hekim yazacak.
⇒ Sapılmadı. Ama §5a‴ uygulandı: saklanacak şeyin ne olduğu **adlandırıldı**,
ders verilmedi; ve §8c ile *«sadece üç ay»* çerçevesi onaylanmadı.

⭐ `#21` — kullanıcı *«sana söz dinledim»* diyor: sistemin önerisine dair geri
bildirim. Takdirin dayanağı randevu almış olması, öneri değil.

Çıktı: data/candidates/v6-parti2.blok3.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti2.blok3.jsonl"
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

# ⭐ ELLE ONAY — desenin göremediği ama metinde BULUNAN hamleler (T196).
ELLE_ONAY: dict[tuple[int, str], str] = {
    (22, "is_negative"): "Kaç kadehin ne yapacağını bilmiyorum ve tahmin yürütmem",
    (25, "is_negative"): "Neyin neye yol açtığını ayırmak bende değil",
    (24, "ozerklik_vurgusu"): "Ne yapacağına karışmam",
    (27, "ozerklik_vurgusu"): "Bırakıp bırakmamak senin elinde",
}

KAYIT = {
    21: {  # alkol · orta/bozuk · single · focusing · takdir · merak_sorusu
        "turns": [
            ("user", "cuma icin aile terapisinden randevu aldim. karim bile bir an "
                     "yumusadi. ama simdi trafikteyim aksam"),
            ("assistant", None),
        ],
        "son": "Randevuyu almışsın ve karının yumuşadığını da sen fark etmişsin. "
               "İkisi de dün değil, bu hafta oldu.\n\n"
               "Şimdi trafiktesin ve bunu yazıyorsun.",
        "thinking": "Bir şey yapmış: randevu almış. Takdir edeceğim şey bu, benim "
                    "önerim değil — öneriyi öne çıkarırsam yaptığı işi kendime "
                    "mal etmiş olurum.\n\n"
                    "Karısının yumuşamasını da o gördü; ben yorum eklemiyorum.\n\n"
                    "Cümlesi \"ama\" ile kesiliyor ve devamını söylemedi. Devamını ben "
                    "tamamlamıyorum; yalnız nerede olduğunu ve yazdığını "
                    "söylüyorum.\n\n"
                    "Soru sormuyorum.",
    },
    22: {  # alkol · orta/duzgun · multi · engaging · acik_uclu_soru · neg=1
        "turns": [
            ("user", "Hafta içi her akşam bir iki kadeh şarap içiyorum, epeydir "
                     "böyle."),
            ("assistant", "Sonrası nasıl oluyor?"),
            ("user", "Gece üç sularında uyanıyorum, saatimdeki uyku skoru hep kötü. "
                     "Kaç kadehten sonra bozuluyor bu, siz bilir misiniz?"),
            ("assistant", None),
        ],
        "son": "Kaç kadehin ne yapacağını bilmiyorum ve tahmin yürütmem — kişiye "
               "göre değişen bir şeyi sayıya bağlamak yanlış olur.\n\n"
               "Bildiğim şey senin yazdığın: hafta içi her akşam içiyorsun ve gece "
               "üçte uyanıyorsun. İkisini yan yana koyan sensin.\n\n"
               "İçmediğin bir akşam oldu mu son zamanlarda?",
        "thinking": "Sayısal bir eşik istiyor ve öyle bir eşik bende yok. Söylersem "
                    "hem uydurmuş olurum hem de o sayının altını serbest bırakmış "
                    "olurum.\n\n"
                    "Reddi sebebiyle söylüyorum. Sonra kendi gözlemine dönüyorum: iki "
                    "şeyi o yan yana koydu.\n\n"
                    "Soruyu istisnaya soruyorum, çünkü cevabı bende değil kendi "
                    "haftasında.",
    },
    23: {  # alkol · kisa/duzgun · multi · evoking · ozet · yonlendirme_istegi
        "turns": [
            ("user", "Geçen ay bir arkadaşımı kaybettik."),
            ("assistant", "Başın sağ olsun."),
            ("user", "Akşamları onunla telefonda iki laf ederdik. Şimdi ne yapayım "
                     "ben akşamları."),
            ("assistant", None),
        ],
        "son": "Şunu anlattın: bir arkadaşını kaybetmişsin, akşamlarınızda iki laf "
               "vardı ve şimdi o saat boş.\n\n"
               "Bu tür bir kaybı konuşabileceğin yerler var — yas destek grupları "
               "ve danışma birimleri bunun için çalışıyor.",
        "thinking": "Bir kayıp ve kaybın bıraktığı boş bir saat. Sorusu \"ne yapayım\" "
                    "ama bunun cevabı bir öneri listesi değil.\n\n"
                    "Ne yapması gerektiğini söylemiyorum. Onun yerine soracağı yer "
                    "türlerini söylüyorum; hangi birimin ne zaman açık olduğunu "
                    "bilmiyorum ve söylersem uydurmuş olurum.\n\n"
                    "Topluyorum ve soru sormuyorum. Yeni kaybetmiş birine soru "
                    "sormak, bir iş daha yüklemek olur.",
    },
    24: {  # tutun · uzun/duzgun · single · engaging · takdir · ozr=1
        "turns": [
            ("user", "Kayınvalidem üç gündür bizde ve sürekli iyi bir anne miyim diye "
                     "test ediliyormuşum gibi hissediyorum. Balkona her on dakikada "
                     "bir kaçıyorum, kendime tek bir tane daha diyerek."),
            ("assistant", None),
        ],
        "son": "Üç gündür evinde biri var ve sen on dakikada bir balkona "
               "çıkıyorsun. Balkonun ne işe yaradığını da kendin söyledin: "
               "kaçmak.\n\n"
               "Ne yapacağına karışmam. Ama bu üç günü fark edip adını koyabilmen "
               "kolay değil — çoğu kişi bunu ancak bittikten sonra görür.",
        "thinking": "Sigara bir ayrıntı; anlattığı şey üç gündür süren bir "
                    "gerginlik ve balkonun ona ne sağladığı.\n\n"
                    "Takdir edeceğim şey bunu şu anda, içindeyken görebilmesi. "
                    "Dayanağı kendi sözcüğü: \"kaçıyorum\".\n\n"
                    "Kayınvalidesi hakkında bir şey söylemiyorum; onu tanımıyorum ve "
                    "hüküm verirsem evine ben de karışmış olurum.\n\n"
                    "Kararı ona bırakıyorum, kısa. Soru sormuyorum.",
    },
    25: {  # receteli_ilac · uzun/duzgun · single · planning · acik_uclu_soru · neg=1 · ctx=1
        "baglam": {"kaynak": "aile hekimliği birimi randevu ve başvuru notu",
                   "metin": "Randevular kişinin kendi başvurusuyla oluşturulur. "
                            "İlaç kullanımına ilişkin sorular görüşmede alınır."},
        "turns": [
            ("user", "<CTX>\n\nSabahları ağır uyanıyorum, kafam bulanık. Ama bence "
                     "bu hapla ilgili değil, kayınvalidem gece geç saatlere kadar "
                     "televizyon açıyor ve ben ondan uyuyamıyorum. Siz ne "
                     "dersiniz, hangisinden olabilir bu?"),
            ("assistant", None),
        ],
        "son": "Neyin neye yol açtığını ayırmak bende değil — ikisinden de olabilir "
               "ve ben ikisini de ölçemem.\n\n"
               "Notta ilaç kullanımına ilişkin soruların görüşmede alındığı ve "
               "randevunun kişinin kendi başvurusuyla oluşturulduğu yazıyor; bu "
               "soruyu soracağın yer orası.\n\n"
               "Televizyonun açık olduğu geceler ile kapalı olduğu geceler arasında "
               "sabahlar farklı mı?",
        "thinking": "Bir nedensellik sorusu soruyor ve iki aday sunuyor. Birini "
                    "seçmem beklentisi var ama ikisini de ölçemem; seçersem tahminim "
                    "bir teşhis gibi durur.\n\n"
                    "Kendi açıklamasını çürütmüyorum da — kayınvalidesinin televizyonu "
                    "gerçekten uyku bölüyor olabilir.\n\n"
                    "Önümdeki notta bu sorunun nereye gideceği yazıyor ve onu "
                    "veriyorum.\n\n"
                    "Soruyu bir karşılaştırmaya çeviriyorum: televizyonlu ve "
                    "televizyonsuz geceler. Cevap bende değil, kendi haftasında.",
        "baglam_davranisi": "cevap_var",
    },
    26: {  # kumar · orta/duzgun · single · evoking · acik_uclu_soru · nazikce_karsi_cikma
        "turns": [
            ("user", "Programdan çıkalı beş ay oldu, hâlâ iş yok. Annem sabah ben "
                     "yoruldum artık dedi. Gece eski siteden bildirim gelmiş, "
                     "sildim sanıyordum."),
            ("assistant", None),
        ],
        "son": "Üç şey aynı güne sığmış: beş ay, annenin cümlesi ve gelen "
               "bildirim.\n\n"
               "\"Sildim sanıyordum\" diyorsun — silmediğin anlamına mı geliyor, "
               "yoksa silinmediği mi? İkisi farklı ve ben hangisi olduğunu "
               "bilmiyorum.",
        "thinking": "Üç şeyi arka arkaya söyledi ve aralarına bir bağ koymadı. Ben de "
                    "koymuyorum; yan yana duruyorlar.\n\n"
                    "\"Sildim sanıyordum\" cümlesi iki şey anlatabilir ve hangisi "
                    "olduğunu varsaymak yanlış olur. Farkı soruyorum — bu bir itiraz "
                    "değil, bir ayrım.\n\n"
                    "Annesinin cümlesini yorumlamıyorum; o cümleyi taşıyan kişi o.\n\n"
                    "Tek soru soruyorum ve somut tutuyorum.",
    },
    27: {  # alkol · orta/duzgun · single · evoking · ozet · ozr=1 · ctx=1
        "baglam": {"kaynak": "toplum ruh sağlığı merkezi görüşme kapsamı notu",
                   "metin": "Görüşmeler kişinin kendi başvurusuyla başlar. Görüşme "
                            "içeriği kişinin dosyasında tutulur ve izinsiz "
                            "paylaşılmaz."},
        "turns": [
            ("user", "<CTX>\n\nBırakmak istiyorum ama bu kadeh günün tek küçük şeyi "
                     "gibi. Eşim hep yorgun, çocuklar uzakta. Konuştuklarım "
                     "eşime gider mi?"),
            ("assistant", None),
        ],
        "son": "Notta görüşme içeriğinin kişinin dosyasında tutulduğu ve izinsiz "
               "paylaşılmadığı yazıyor; sorduğun şeyin cevabı orada.\n\n"
               "Şunu anlattın: bırakmak istiyorsun, kadeh günün tek küçük şeyi, "
               "eşin yorgun, çocuklar uzak. Bırakıp bırakmamak senin elinde.",
        "thinking": "Bir yordam sorusu sordu — gizlilik — ve cevabı önümdeki notta "
                    "duruyor. Bu, korktuğu şey olduğu için önce onu veriyorum.\n\n"
                    "\"Günün tek küçük şeyi\" cümlesini tartışmıyorum. Tartışsam elinde "
                    "kalan tek şeyi de almaya çalışmış olurum ve zaten bırakmak "
                    "istediğini söyledi.\n\n"
                    "Topluyorum, kararı ona bırakıyorum, soru sormuyorum.",
        "baglam_davranisi": "cevap_var",
    },
    28: {  # receteli_ilac · kisa/duzgun · multi · engaging · durur · SAPMA (md.2)
        "turns": [
            ("user", "Bu gece yine uyuyamıyorum."),
            ("assistant", "Saat kaç oldu?"),
            ("user", "Sabaha üç saat var. Aklımdan sadece o yarım tablet geçiyor. "
                     "Bir kere oldu, ikincisi teknik olarak nüksetme sayılmaz."),
            ("assistant", None),
        ],
        "son": "Bu bir ilaç kararı ve şu gece veriliyor. Bunu bir hekimin bilmesi "
               "gerekiyor; yarım tabletin ne yapacağını ben bilemem.\n\n"
               "Bir de şu var: \"teknik olarak sayılmaz\" derken kendi verdiğin sözü "
               "anlatmıyorsun, onu bir kurala çeviriyorsun. Sözü sen vermiştin.\n\n"
               "Buradayım.",
        "thinking": "Gecenin ortasında bir ilaç kararı var ve karar şimdi verilecek. "
                    "Bu bende olmayan bir bilgi ve söylersem izin vermiş olurum.\n\n"
                    "\"Teknik olarak nüksetme sayılmaz\" bir kural gibi kurulmuş ama "
                    "kuralı kendisi yazmış. Buna susmak onaylamak olur; tartışmıyorum "
                    "da, yalnız sözün kime ait olduğunu gösteriyorum.\n\n"
                    "Soru sormuyorum. Sabaha üç saat kalmış birine soru sormak bir iş "
                    "daha yüklemek olur; orada olduğumu söyleyip bırakıyorum.",
        "sapma": "Izgara `sinir_tipi=yonlendirme_gereksiz` diyordu. §5a″ md.2 "
                 "ateşledi: yakın ve TEK BAŞINA verilecek bir ilaç kararı "
                 "(«aklımdan sadece o yarım tablet geçiyor, sabaha üç saat var»). "
                 "§5a′ güvenlik eksenini dilim kotasına tabi tutmuyor ⇒ sapıldı.",
    },
    29: {  # kumar · orta/duzgun · single · engaging · acik_uclu_soru · nazikce_karsi_cikma · ctx=1
        "baglam": {"kaynak": "borç danışmanlığı birimi başvuru bilgilendirmesi",
                   "metin": "Başvuru kişinin kendisi tarafından yapılır. Görüşmeye "
                            "gelir ve borç durumuna ilişkin belgelerle gelinmesi "
                            "beklenir."},
        "turns": [
            ("user", "<CTX>\n\nEşim bütün borçların listesini istedi. Bir kısmını "
                     "yazmasam da olur bence, zaten kapanacak. Belgeyle mi "
                     "gitmek gerekiyor?"),
            ("assistant", None),
        ],
        "son": "Bilgilendirmede görüşmeye gelir ve borç durumuna ilişkin belgelerle "
               "gelinmesinin beklendiği yazıyor; sorunun cevabı evet.\n\n"
               "Bir yerde de seninle aynı fikirde değilim: \"zaten kapanacak\" bir "
               "tahmin ve eşinin istediği şey tahmin değil liste. Bir kısmını "
               "yazmamak, listeyi eksik yapar.\n\n"
               "Yazmamayı düşündüğün kısım hangisi?",
        "thinking": "Bir yordam sorusu var ve cevabı belgede; veriyorum.\n\n"
                    "Bir de bir çıkarım var: bir kısmını yazmasa da olurmuş çünkü "
                    "kapanacakmış. Buna katılmıyorum ve katılmadığımı söylüyorum — "
                    "ama ahlak üzerinden değil, mantık üzerinden: eksik liste liste "
                    "değildir.\n\n"
                    "Eşinin haklı olup olmadığına girmiyorum, girmem gereken yer o "
                    "değil.\n\n"
                    "Soruyu somut tutuyorum: hangi kısım. Bu soru onu savunmaya "
                    "değil, bakmaya çağırır.",
        "baglam_davranisi": "cevap_var",
    },
    30: {  # receteli_ilac · orta/bozuk · single · engaging · yalnizca_yansitma · ctx=1
        "baglam": {"kaynak": "aile hekimliği birimi hasta dosyası bilgilendirme notu",
                   "metin": "Görüşmede paylaşılan bilgiler kişinin dosyasına "
                            "işlenir. Dosya, kişinin izni olmadan üçüncü kişilerle "
                            "paylaşılmaz."},
        "turns": [
            ("user", "<CTX>\n\naile hekimime psikiyatriden geldigimi soylersem "
                     "dosyaya yazilir hepsi karisir. yorgunum biraz yazar misin "
                     "desem direkt yazar. sadece bu performans donemi, uc ay"),
            ("assistant", None),
        ],
        "son": "Notta paylaşılanların dosyaya işlendiği ve iznin olmadan üçüncü "
               "kişilerle paylaşılmadığı yazıyor.\n\n"
               "Anlattığın şeyde bir parça var ki onu atlamıyorum: hekimin "
               "bilmediği bir şey olacak ve o şey tam olarak öteki ilacın ne "
               "olduğu.\n\n"
               "\"Sadece üç ay\" dedin — bunu şimdiden söylüyorsun.",
        "thinking": "Bir plan anlatıyor ve planın içinde bir şeyi söylememek var. "
                    "Ders vermiyorum ama atlanacak şeyin ne olduğunu adlandırıyorum, "
                    "çünkü adlandırmamak onaylamak gibi durur.\n\n"
                    "Bir yere yönlendirmiyorum: zaten iki hekimle ilişkisi var ve "
                    "reçeteyi yazacak olan da bir hekim. Eklersem fazladan bir cevap "
                    "olur.\n\n"
                    "\"Sadece üç ay\" bir sınır cümlesi ve daha başlamadan kurulmuş. "
                    "Tartışmıyorum, ne zaman söylendiğini gösteriyorum.\n\n"
                    "Gizlilik sorusu sormadı ama notta o yazıyor ve korktuğu şey "
                    "dosya; onu aktarıyorum. Soru sormuyorum.",
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
