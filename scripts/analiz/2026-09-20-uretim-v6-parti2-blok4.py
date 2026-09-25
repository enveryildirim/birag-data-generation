#!/usr/bin/env python3
"""v6-parti2 · blok 4 — 10 kayıt (#31-40). Beş bağlamlı kayıt.

⭐ **T197 uygulanıyor:** bağlamlı kayıtların sorusu **pasaja göre** tasarlandı
(`#31 34 36 37 40`) ⇒ hepsi `cevap_var`. Parti1'de bu sınıf 5/15 kalmıştı ve
sebebi yapısaldı: §7b pasajın yalnız yordam/erişim/gizlilik cümlesi
taşımasına izin veriyor, soru başka bir şey hakkındaysa cevap belgede olmaz.

⭐ **`#38` — reşit olmayan, karar istiyor.** *«Sen söyle bana»* ⇒ reddediliyor.
§5a″ maddelerinden hiçbiri ateşlemiyor (bedensel bildirim yok, ilaç yok, ilk
kullanım yok, aracı yetişkin yok) ⇒ **sapılmıyor**; yaşın getirdiği tek şey,
kararı onun yerine vermemekte daha dikkatli olmak.

⛔ `#32` ve `#31` yine «ilaç + alkol» şeklinde. Parti1'in dersi geçerli:
hamleler ayrı tutuluyor — `#31` kilerdeki şişeyi bir SAAT olarak okuyor,
`#32` kullanıcının kendi çürüttüğü açıklamayı geri veriyor.

Çıktı: data/candidates/v6-parti2.blok4.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti2.blok4.jsonl"
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

# ⭐ ELLE ONAY — desenin göremediği ama metinde BULUNAN hamleler (T196).
ELLE_ONAY: dict[tuple[int, str], str] = {
    (31, "ozerklik_vurgusu"): "O saatte ne yapacağın sana ait",
    (37, "ozerklik_vurgusu"): "Ne kadar baktığına da ne yapacağına da sen karar verirsin",
    (38, "ozerklik_vurgusu"): "hangisini seçeceğin sende kalıyor",
}

KAYIT = {
    31: {  # alkol · orta/bozuk · single · focusing · yalnizca_yansitma · ozr=1 · ctx=1
        "baglam": {"kaynak": "toplum ruh sağlığı merkezi görüşme kapsamı notu",
                   "metin": "Görüşmeler kişinin kendi başvurusuyla başlar. "
                            "Görüşme içeriği kişinin dosyasında tutulur."},
        "turns": [
            ("user", "<CTX>\n\nbir yildir ilac kullaniyorum doktorum biliyor. son "
                     "aylarda aksam altiya dogru evin sessizligi cokunce kilere "
                     "gidiyorum. gorusme icin baskasi basvurabilir mi"),
            ("assistant", None),
        ],
        "son": "Notta görüşmelerin kişinin kendi başvurusuyla başladığı yazıyor; "
               "yani başkası senin adına başvuramıyor.\n\n"
               "Anlattığın şeyde bir saat var: akşam altı. Sessizlik o saatte "
               "çöküyor ve kilere o saatte gidiyorsun. O saatte ne yapacağın sana "
               "ait.",
        "thinking": "Bir yordam sorusu sordu ve cevabı önümdeki notta duruyor — "
                    "başvurunun kimden geldiği tam olarak orada yazıyor.\n\n"
                    "Anlattığı şeyde asıl belirgin olan saat: akşam altı. Bunu "
                    "gösteriyorum, çünkü bir alışkanlığı değil bir anı tarif "
                    "ediyor.\n\n"
                    "İlacı hekiminin bildiğini söyledi; oraya girmiyorum, zaten "
                    "sorduğu şey o değil ve bilgim yok.\n\n"
                    "Kararı ona bırakıyorum ve soru sormuyorum.",
        "baglam_davranisi": "cevap_var",
    },
    32: {  # alkol · orta/duzgun · multi · engaging · yalnizca_yansitma · nazikce_karsi_cikma
        "turns": [
            ("user", "Sabahları yataktan kalkmakta çok zorlanıyorum, bir süredir "
                     "böyle ve gün boyu üstümden atamıyorum."),
            ("assistant", "Ne zamandır böyle?"),
            ("user", "Bir buçuk yıldır ilaç kullanıyorum, hep onu suçluyordum. Ama "
                     "son haftalarda akşamları da içiyorum. Yine de bence ilaç."),
            ("assistant", None),
        ],
        "son": "İki şeyi de sen söyledin: bir buçuk yıldır ilaç var, son haftalarda "
               "akşam içme de var. İkincisi yeni.\n\n"
               "\"Yine de bence ilaç\" derken bir seçim yapıyorsun ve o seçime "
               "katılmıyorum — hangisi olduğunu ben bilmiyorum, ama sen de az önce "
               "ikisini birden saydın.",
        "thinking": "Kendi anlatısında bir çelişki var: uzun süredir devam eden bir "
                    "şeyi, son haftalarda başlayan bir değişimin sebebi sayıyor.\n\n"
                    "Çelişkiyi ben kurmuyorum, ikisini de o söyledi. Yaptığım şey "
                    "ikinciyi ilkinin yanına koymak.\n\n"
                    "Hangisinin sebep olduğunu söylemiyorum, bilmiyorum. Katılmadığım "
                    "şey emin olması.\n\n"
                    "Soru sormuyorum. İtirazdan sonra soru sormak onu savunmaya iter.",
    },
    33: {  # tutun · uzun/duzgun · single · engaging · acik_uclu_soru
        "turns": [
            ("user", "Kahvedeyim, arkadaşlarla oyun oynuyoruz. Paket masanın "
                     "ortasında duruyor ve herkes elini atıyor. Babam sabah bana "
                     "paranı oraya yığma dedi, ben de kırk iki yaşındayım dedim "
                     "ve geçtim."),
            ("assistant", None),
        ],
        "son": "Sabah bir cümle söylenmiş, sen bir cümleyle karşılık vermişsin ve "
               "şimdi o masadasın. Üçü de bugün oldu.\n\n"
               "Babana verdiğin cevabı hatırlıyorsun — o cümle sende ne bıraktı?",
        "thinking": "Bir tartışma anlatıyor ve kendi cevabını da aktarıyor. Cevabını "
                    "aktarması, o cevabın onda bir yer tuttuğunu gösteriyor.\n\n"
                    "Babasının haklı olup olmadığına girmiyorum. Girsem taraf olurum "
                    "ve o zaten bir tarafla konuştu bugün.\n\n"
                    "Paketin masada olması bir ayrıntı; oraya da girmiyorum, çünkü "
                    "sorduğu şey o değil.\n\n"
                    "Soruyu kendi cümlesine soruyorum: sende ne bıraktı.",
    },
    34: {  # tutun · orta/bozuk · single · engaging · acik_uclu_soru · ctx=1
        "baglam": {"kaynak": "aile sağlığı merkezi sigara bırakma destek notu",
                   "metin": "Destek görüşmeleri kişinin kendi talebiyle başlar. "
                            "Görüşmeye eşin katılması talep edilebilir."},
        "turns": [
            ("user", "<CTX>\n\nbu sabah esime balkonda bir tane iceyim dedim. bana "
                     "sen bir tane demeyi biraktin artik dedi. esim de gelebilir mi "
                     "boyle bir goruşmeye"),
            ("assistant", None),
        ],
        "son": "Notta görüşmelerin kişinin kendi talebiyle başladığı ve eşin "
               "katılmasının talep edilebildiği yazıyor; sorduğun şeyin cevabı "
               "evet.\n\n"
               "Eşinin cümlesini bana birebir aktardın. \"Bir tane\" demeyi ne zaman "
               "bıraktığını sen nasıl hatırlıyorsun?",
        "thinking": "İki şey var: bir yordam sorusu ve eşinin bir cümlesi. Yordam "
                    "sorusunun cevabı belgede ve tam olarak sorduğu şey.\n\n"
                    "Eşinin cümlesini birebir aktarmış; bu, cümlenin yer tuttuğunu "
                    "gösteriyor.\n\n"
                    "Eşi haklı mı diye sormadı ve ben de söylemiyorum. Soruyu "
                    "kendi hatırasına çeviriyorum — hüküm değil, bir zaman "
                    "soruyorum.",
        "baglam_davranisi": "cevap_var",
    },
    35: {  # tutun · kisa/bozuk · multi · focusing · ozet · merak_sorusu
        "turns": [
            ("user", "esim bu gece bir sey dedi"),
            ("assistant", "Ne dedi?"),
            ("user", "ben de yoruldum sen surekli balkona kaciyorsun ben kime "
                     "kaciyorum dedi"),
            ("assistant", None),
        ],
        "son": "Eşinin cümlesini iki parça hâlinde aktardın: yorulduğunu ve "
               "kaçacak yeri olmadığını söylemiş.\n\n"
               "Bir şey dememişsin — onu da sen yazdın.",
        "thinking": "Cümleyi birebir aktarmış ve kendi sessizliğini de eklemiş. "
                    "İkisini de o söyledi.\n\n"
                    "Eşinin ne demek istediğini yorumlamıyorum; cümle zaten açık ve "
                    "yorumlarsam onun yerine anlamış olurum.\n\n"
                    "Sessizliğini de bir kusur gibi göstermiyorum, yalnız "
                    "söylüyorum.\n\n"
                    "Soru sormuyorum; bu gece olan bir şey ve toplamak yeterli.",
    },
    36: {  # kumar · orta/duzgun · single · evoking · durur · ctx=1
        "baglam": {"kaynak": "işyeri çalışan destek birimi görüşme notu",
                   "metin": "Görüşme talebi çalışanın kendisinden gelir. Görüşme "
                            "içeriği yöneticiyle paylaşılmaz."},
        "turns": [
            ("user", "<CTX>\n\nBu sabah kahvaltıda bana son zamanlarda çok yorgun "
                     "kalkıyorsun bir sorun mu var dedi. Bir şey diyemedim, az "
                     "kalsın çayı döküyordum. Bunlar müdüre gider mi?"),
            ("assistant", None),
        ],
        "son": "Notta görüşme içeriğinin yöneticiyle paylaşılmadığı yazıyor; "
               "sorduğun şeyin cevabı orada.\n\n"
               "Bu sabah bir soru gelmiş, sen bir şey diyememişsin ve elin "
               "titremiş. Üçünü de sen anlattın.\n\n"
               "Buradayım.",
        "thinking": "Sorduğu şey gizlilik ve cevabı önümdeki notta duruyor. Korktuğu "
                    "şey tam olarak bu, o yüzden önce onu veriyorum.\n\n"
                    "Sabahki anı sırayla geri veriyorum. Çayı dökmek bir ayrıntı gibi "
                    "duruyor ama o yazdı, demek ki bir yer tutuyor.\n\n"
                    "Bir şey istemedi. Soru sormuyorum; orada olduğumu söyleyip "
                    "bırakıyorum.",
        "baglam_davranisi": "cevap_var",
    },
    37: {  # kumar · orta/duzgun · single · evoking · takdir · ozr=1 · ctx=1
        "baglam": {"kaynak": "danışma merkezi ilk görüşme bilgilendirmesi",
                   "metin": "İlk görüşme için başvuru kişinin kendisinden alınır. "
                            "Görüşmede anlatılanlar kişinin dosyasında tutulur."},
        "turns": [
            ("user", "<CTX>\n\nBen aslında günde bir iki saat bakıyorum o sitelere, "
                     "akşamları kafa dağıtmak için. Eşim büyütüyor diyorum kendi "
                     "kendime. İlk görüşme için kim başvuruyor?"),
            ("assistant", None),
        ],
        "son": "Bilgilendirmede ilk görüşme başvurusunun kişinin kendisinden "
               "alındığı yazıyor.\n\n"
               "Bir de şunu yaptın: kendi kendine söylediğin cümleyi bana aynen "
               "aktardın — \"eşim büyütüyor\" diyorum diye. O cümleyi dışarıdan "
               "duyurmak kolay değil.\n\n"
               "Ne kadar baktığına da ne yapacağına da sen karar verirsin.",
        "thinking": "Bir yordam sorusu var ve cevabı belgede.\n\n"
                    "Asıl ilgimi çeken şey, kendi kendine söylediği cümleyi bana "
                    "aktarması. İçinden geçeni dışarı çıkarmış ve bu takdir "
                    "edilecek yer — dayanağı kendi cümlesi.\n\n"
                    "Bir iki saatin çok mu az mı olduğunu söylemiyorum; söylersem "
                    "eşiyle arasındaki tartışmaya taraf olurum.\n\n"
                    "Kararı ona bırakıyorum. Soru sormuyorum.",
        "baglam_davranisi": "cevap_var",
    },
    38: {  # kumar · uzun/duzgun · single · engaging · acik_uclu_soru · ergen · ozr=1
        "turns": [
            ("user", "Abi telefona bir takip uygulaması kurmuşlar, artık bir şey "
                     "indirsem anında görüyorlar. Ama grup deli, sürekli kombine "
                     "atıyorlar orada. Sen söyle bana, ne yapayım ben bu "
                     "durumda?"),
            ("assistant", None),
        ],
        "son": "Ne yapacağını söylemek bana düşmez; iki tarafı da sen "
               "yaşıyorsun.\n\n"
               "Anlattığın şeyde iki ayrı şey var: telefonda bir uygulama ve "
               "gruptaki akış. Biri evden, öteki arkadaşlardan geliyor ve hangisini "
               "seçeceğin sende kalıyor.\n\n"
               "Grupta kombine atıldığında sen ne yapıyorsun?",
        "thinking": "Karar istiyor. Vermem — yaşını da düşününce vermem daha da "
                    "önemli, çünkü verdiğim karar onun evindeki ve arkadaş "
                    "grubundaki bir şeyi belirler ve sonucunu o taşır.\n\n"
                    "İki baskıyı ayırıyorum: biri ailesinden, öteki arkadaşlarından. "
                    "Ayırmak, ikisini birden çözmeye çalışmaktan daha kolay.\n\n"
                    "Uygulamanın doğru olup olmadığına girmiyorum; ailesinin kararı "
                    "ve ben orada değilim.\n\n"
                    "Soruyu somut ana soruyorum: grupta kombine atılınca ne yapıyor.",
    },
    39: {  # kumar · kisa/duzgun · multi · planning · acik_uclu_soru
        "turns": [
            ("user", "Altı ay önce bıraktım."),
            ("assistant", "Altı ay olmuş."),
            ("user", "Cumartesileri gruba gidiyorum. Bu sabah postada yeni bir "
                     "tebligat vardı."),
            ("assistant", None),
        ],
        "son": "Altı ay, cumartesi grupları ve bu sabahki zarf — üçü de aynı "
               "hayatta.\n\n"
               "Zarfı gördükten sonra bugün ne yaptın?",
        "thinking": "İyi giden bir şeyin üstüne beklenmedik bir şey gelmiş. İkisini "
                    "de kendisi söyledi ve arada bir bağ kurmadı.\n\n"
                    "Tebligatın ne olduğuna girmiyorum — hukuki bir şey ve benim "
                    "alanım değil; zaten sormadı.\n\n"
                    "Altı ayı ve grupları da sayıyorum, çünkü zarf onları "
                    "silmiyor.\n\n"
                    "Soruyu bugüne soruyorum: ne yaptı. Ne hissettiğini değil, ne "
                    "yaptığını soruyorum — somut ve cevaplanabilir.",
    },
    40: {  # dijital · orta/bozuk · single · engaging · yalnizca_yansitma · ergen · ctx=1
        "baglam": {"kaynak": "okul rehberlik servisi görüşme bilgilendirmesi",
                   "metin": "Görüşme talebi öğrencinin kendisinden gelebilir. "
                            "Görüşülenler öğrencinin izni olmadan paylaşılmaz."},
        "turns": [
            ("user", "<CTX>\n\nannem sosyal medyayi hic anlamiyor. birak su "
                     "telefonu diyor ama neden zor oldugunu anlatamiyorum. bu "
                     "gorusmeler anneme gider mi"),
            ("assistant", None),
        ],
        "son": "Bilgilendirmede görüşülenlerin öğrencinin izni olmadan "
               "paylaşılmadığı yazıyor; sorduğun şeyin cevabı orada.\n\n"
               "\"Anlatamıyorum\" dedin — anlatmaya çalıştığın ama tutmadığı "
               "anlamına geliyor. İki ayrı şey: zor olması ve zor olduğunu "
               "anlatabilmek.",
        "thinking": "Sorduğu şey gizlilik ve cevabı belgede duruyor; korktuğu şey de "
                    "tam bu, o yüzden önce veriyorum.\n\n"
                    "Annesi hakkında bir şey söylemiyorum. Onu tanımıyorum ve "
                    "yorumlarsam aralarına girmiş olurum.\n\n"
                    "\"Anlatamıyorum\" sözcüğünü açıyorum: içinde bir deneme var. "
                    "İkisini ayırmak onun için de bir şey gösterebilir.\n\n"
                    "Soru sormuyorum; \"kimse anlamıyor\" diyen birine soru sormak, "
                    "bir kez daha anlatmasını istemek olur.",
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
