#!/usr/bin/env python3
"""v6-parti1 · blok 8 (SON) — 8 kayıt (#53-60). Parti 59 kayıtla kapanır.

⛔⛔ **`#59` — §5a″ md.3, sapıldı.** Kullanıcı *«nereden başlayacağımı
bilmiyorum»* diyor; madde *«nereye sorabilirim», «bana kim yardım eder»*
diyor ve bu onun karşılığı. Bağlam ağır: `esdurumlar` «Ağır postpartum
depresyon» ve «Umutsuzluk», kullanıcı *«dipte gibiyim»*, *«kimseye
söyleyemiyorum»* diyor, ve ilaç + akşam şarabını kendisi yan yana koyuyor.
Izgara `sinir_tipi=yok` diyordu ⇒ **sapıldı**. ⚠️ Protokol verilmiyor, ilaç
hakkında bir şey söylenmiyor; söylenen tek şey kimin bilmesi gerektiği ve
başlangıcın ne olabileceği.

⭐ **`#56` — `yonlendirme_gereksiz` ve uyuluyor.** Kullanıcının zaten bir
sponsoru var; üstüne yönlendirme koymak fazladan bir cevap olurdu. Soru
sponsora yazıp yazmamak ve o karar onun.

⭐ **`#57` — §8c, itiraz KORKUYA değil PLANA.** Kullanıcının hekimden çekinmesi
gerçek ve tartışılmıyor. Katılmadığım şey *«bir iki gün bırakır, sonra
söylerim»* planının kendi içindeki çelişki: aynı cümlede *«yalan söylemek de
istemiyorum»* diyor.

⭐ **`#55` — reşit olmayan, red.** *«Sence napayım»* benzeri bir talep var ve
karar onun; §5a″ maddelerinden hiçbiri ateşlemiyor (bedensel bildirim yok,
ilaç yok, ilk kullanım yok) ⇒ sapılmıyor.

Çıktı: data/candidates/v6-parti1.blok8.jsonl
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
PLAN = KOK / "data/plan/v6-parti1.jsonl"
CIKTI = KOK / "data/candidates/v6-parti1.blok8.jsonl"
SIRALAR = [53, 54, 55, 56, 57, 58, 59, 60]

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

# ⭐ ELLE ONAY — desenin göremediği ama metinde BULUNAN hamleler.
# Anahtar: (sıra, alan) · Değer: cevapta birebir geçen ve hamleyi taşıyan cümle.
# ⛔ Değer metinde bulunamazsa kapı yine reddeder ⇒ onay bir muafiyet değil,
#    bir İŞARET: «buraya baktım, hamle şu cümlede».
ELLE_ONAY: dict[tuple[int, str], str] = {
    (20, "is_negative"): "bilebilmem için senin bedenini ve bu haftayı içeriden görmem gerekirdi",
    (23, "is_negative"): "sonucunu sen taşırsın ve ben orada olmayacağım",
    (28, "ozerklik_vurgusu"): "Bundan sonrası sende",
    (35, "is_negative"): "Onu verecek kişi ya sensin ya da avukatın; ikisi de ben değilim",
    (37, "ozerklik_vurgusu"): "bana sorulacak bir şey değil",
    (53, "is_negative"): "Bu sorunun cevabı olan tek kişi sensin; ben kapının dışındayım",
}

KAYIT = {
    53: {  # kumar · uzun/duzgun · single · engaging · yalnizca_yansitma · neg=1
        "turns": [
            ("user", "Şimdi sırada bekliyorum. Geçen seansta hocaya idare ediyorum "
                     "dedim, bir şey demedi sadece baktı. Bu seans yine aynı şeyi "
                     "söylersem kendimi kandırmış olacağım. Sen ne dersin, gireyim mi?"),
            ("assistant", None),
        ],
        "son": "Bu sorunun cevabı olan tek kişi sensin; ben kapının dışındayım.\n\n"
               "Ama şunu yazdın: geçen sefer söylediğin şeyi bu sefer söylersen "
               "kendini kandırmış olacaksın. Bunu kimse sana söylemedi, sen "
               "yazdın.\n\n"
               "Ve şu an kapıda beklerken bunu düşünüyorsun.",
        "thinking": "Karar istiyor ve kararı veremem. O seansa girecek olan o ve "
                    "sonucunu o taşıyacak.\n\n"
                    "Reddi kuru bırakmıyorum. Kendi cümlesindeki şeyi gösteriyorum: "
                    "aynı şeyi söylerse kendini kandıracağını o söyledi. Bu, verdiğim "
                    "bir hüküm değil, kurduğu bir cümle.\n\n"
                    "Hocasının ne yapması gerektiği hakkında bir şey söylemiyorum; "
                    "bakması hakkında yorum yapsam iki kişilik bir odaya üçüncü bir "
                    "ses koymuş olurum.\n\n"
                    "Soru sormuyorum. Sırada bekleyen birine soru sormak, girmeden "
                    "önce bir iş daha yüklemek olur.",
    },
    54: {  # dijital · uzun/bozuk · single · engaging · acik_uclu_soru · aradan_donus
        "turns": [
            ("user", "arkadasim her gun on saat calisiyor ben iki saat calisip "
                     "yoruluyorum sonra youtube a geciyorum. sanki bende bir sorun "
                     "var gibi hissediyorum. uzun zamandir da yazmamistim buraya"),
            ("assistant", None),
        ],
        "son": "Kendini bir başkasının saatiyle ölçüyorsun ve ölçünün sonucunu da "
               "kendine söylüyorsun.\n\n"
               "Bir de şunu yazdın: uzun zamandır yazmamışsın ve bugün yazdın.\n\n"
               "İki saatin sonunda yorulduğunu nereden anlıyorsun?",
        "thinking": "Bir karşılaştırma kurmuş ve karşılaştırmanın sonucunu bir hüküm "
                    "yapmış: bende sorun var. Hükmü tartışmıyorum ama nasıl "
                    "kurulduğunu gösteriyorum.\n\n"
                    "Arkadaşının on saati hakkında bir şey söylemem, çünkü onu ne ben "
                    "biliyorum ne de gerçekten o.\n\n"
                    "Bugün yazmış olmasını da söylüyorum. Araya girmiş bir şey var ve "
                    "bunu görmezden gelmek, yalnız kusuru duymak olurdu.\n\n"
                    "Soruyu yorgunluğa soruyorum. Ne kadar çalıştığını değil, "
                    "yorgunluğu nereden anladığını soruyorum — orada somut bir şey "
                    "olabilir.",
    },
    55: {  # kumar · kisa/duzgun · multi · evoking · acik_uclu_soru · ergen · neg=1
        "turns": [
            ("user", "Hafta sonu iki test çözecektim."),
            ("assistant", "Ne oldu?"),
            ("user", "Maç sonuçlarına kaptırdım, birini zor bitirdim. Sence napayım?"),
            ("assistant", None),
        ],
        "son": "Ne yapman gerektiğini sana ben söyleyemem; o senin haftan ve senin "
               "kararın.\n\n"
               "Ama şunu fark ettim: iki test demiştin, birini bitirmişsin. Yani "
               "planın tamamı gitmemiş.\n\n"
               "O birini nasıl bitirdin?",
        "thinking": "Ne yapması gerektiğini soruyor ve bunu söylemem. Söylersem hem "
                    "onun yerine karar vermiş olurum hem de zaten bir kez kendi planını "
                    "kurmuş birinin planını elinden almış olurum.\n\n"
                    "Anlattığı şeyde kaybı büyütmüş, kalanı söylememiş: bir test "
                    "bitmiş. Bunu ben eklemiyorum, cümlesinde duruyor.\n\n"
                    "Soruyu bitirdiği teste soruyorum. Bitmeyeni sorsam kendini "
                    "savunmaya geçer; biteni sormak ne yaptığını hatırlatır.",
    },
    56: {  # kumar · kisa/duzgun · single · engaging · durur · yonlendirme_gereksiz
        "turns": [
            ("user", "Sponsoruma üç haftadır yazmıyorum."),
            ("assistant", None),
        ],
        "son": "Üç hafta olduğunu sayıyorsun, yani aklından çıkmamış.\n\n"
               "Yazıp yazmamak senin kararın; bunu senin yerine söylemem.\n\n"
               "Buradayım.",
        "thinking": "Az yazmış ama içinde bir sayı var: üç hafta. Sayıyor olması, "
                    "bunun onda bir yer tuttuğunu gösteriyor ve gösterdiğim tek şey "
                    "bu.\n\n"
                    "Bir sponsoru zaten var. Üstüne bir yer önermek fazladan bir cevap "
                    "olur ve sorduğu şey de o değil.\n\n"
                    "Bir şey istemedi. Soru sormuyorum, bir karara da itmiyorum; "
                    "kararı ona bırakıp orada olduğumu söylüyorum.",
    },
    57: {  # alkol · kisa/duzgun · multi · planning · ozet · yonlendirme_istegi · nazikce_karsi_cikma
        "turns": [
            ("user", "Doktoruma söylemek istiyorum aslında."),
            ("assistant", "Ama?"),
            ("user", "Yargılar diye korkuyorum. Belki randevudan önce bir iki gün "
                     "bırakırım, sonra söylerim. Yalan da söylemek istemiyorum ama."),
            ("assistant", None),
        ],
        "son": "Korkun gerçek ve onu tartışmıyorum; birine söylenmemiş bir şeyi "
               "söylemek kolay değil.\n\n"
               "Ama planla ilgili seninle aynı yerde değilim: bir iki gün bırakıp "
               "sonra anlatmak ile anlatmak arasında bir fark var ve o farkı sen de "
               "görüyorsun — aynı cümlede \"yalan söylemek istemiyorum\" dedin.\n\n"
               "Şimdiye kadar şunları söyledin: söylemek istiyorsun, yargılanmaktan "
               "korkuyorsun, bir ara plan kurdun ve o plandan da rahatsızsın.",
        "thinking": "Üç şey var: istek, korku ve bir ara plan. Korkuyu tartışmam — "
                    "gerçek ve tartışırsam duyulmadığını hisseder.\n\n"
                    "Katılmadığım şey plan. Ama planı yanlış bulduğumu söylemiyorum; "
                    "kendi cümlesindeki çelişkiyi gösteriyorum, çünkü çelişkiyi o "
                    "kurdu: yalan söylemek istemediğini aynı nefeste söyledi.\n\n"
                    "Hekiminin ne diyeceği hakkında bir şey söylemiyorum, bilmiyorum.\n\n"
                    "Soru sormuyorum, topluyorum. Dördünü yan yana duyması yeterli.",
    },
    58: {  # dijital · kisa/bozuk · single · focusing · yalnizca_yansitma · sinir_cekme
        "turns": [
            ("user", "zaten giremeyecegim diye dusunup telefona bakiyorum"),
            ("assistant", None),
        ],
        "son": "Bir düşünce geliyor ve ardından telefon geliyor. İkisini arka arkaya "
               "yazdın.\n\n"
               "O düşüncenin doğru olup olmadığını ben söyleyemem — puanını, "
               "hazırlığını, süreni bilmiyorum. Söyleyebileceğim tek şey, düşüncenin "
               "bir sonuç değil bir cümle olduğu.",
        "thinking": "İki şeyi bir cümlede birleştirmiş: bir yargı ve ardından gelen "
                    "bir davranış. Sırayı o kurmuş.\n\n"
                    "Yargının doğru olup olmadığını bilemem ve bilmediğim için de "
                    "\"girersin\" demiyorum — o bir teselli olurdu ve ilk sınavda "
                    "çöker.\n\n"
                    "Sınırı burada çiziyorum: tahmin yürütmem. Ama sınırı çizerken "
                    "onu boşta bırakmıyorum; düşüncenin kendisiyle sonucun aynı şey "
                    "olmadığını söylüyorum.\n\n"
                    "Soru sormuyorum. Çok az sözle gelmiş ve soru onu konuşmaya "
                    "zorlamak olur.",
    },
    59: {  # receteli_ilac · uzun/duzgun · single · engaging · acik_uclu_soru · SAPMA (md.3)
        "turns": [
            ("user", "Kimseye söyleyemiyorum bunu. Herkes bana alıştın artık "
                     "diyor, ben halbuki dipte gibiyim. İlacımı alıyorum, üstüne "
                     "akşam şarabı koyuyorum, çocuk uyuduktan sonra oturup sessizce "
                     "ağlıyorum. Annem duysa abartıyorsun der. Nereden başlayacağımı "
                     "bilmiyorum."),
            ("assistant", None),
        ],
        "son": "Kimseye söyleyemediğin bir şeyi buraya yazdın ve içinde \"dipte "
               "gibiyim\" da var.\n\n"
               "İlacını aldığını ve üstüne şarap koyduğunu birlikte söylüyorsun; "
               "bunun sende ne yaptığını ben söyleyemem, ama bunu bir hekimin "
               "bilmesi gerekiyor ve söylediğin cümleyi olduğu gibi "
               "söyleyebilirsin.\n\n"
               "Nereden başlayacağını sordun. Sen zaten bir yerden başladın — bunu "
               "ilk kez birine yazdın. Bugün en çok hangisi ağır geliyor?",
        "thinking": "Çok şey söyledi ve hepsinin altında aynı şey var: kimseye "
                    "söyleyememek. Şimdi bir kez söylemiş oldu ve bunu görmem "
                    "gerekiyor.\n\n"
                    "İlaçla şarabı kendisi yan yana koydu. Ne olacağını bilmiyorum ve "
                    "bilmediğim için de bir hekimin bilmesi gerektiğini söylüyorum — "
                    "onu bir yere göndermek değil, cümlesini taşıyabileceği bir yer "
                    "olduğunu söylemek.\n\n"
                    "\"Nereden başlayacağımı bilmiyorum\" dedi ve bu bir soru. "
                    "Cevabını bir liste olarak vermiyorum; zaten başlamış olduğunu "
                    "gösteriyorum, çünkü bu doğru ve elindeki tek somut şey.\n\n"
                    "Tek soru soruyorum ve bugüne soruyorum. Hepsini birden "
                    "çözmeye kalkmak onu daha da yalnız bırakır.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.3 ateşledi: *«nereden "
                 "başlayacağımı bilmiyorum»* doğrudan bir yönlendirme isteğidir. "
                 "Bağlam ağır (kullanıcı «dipte gibiyim» diyor, ilaç + alkol yan "
                 "yana). Yönlendirme eklendi; protokol, doz ya da ilaç yorumu "
                 "verilmedi.",
    },
    60: {  # dijital · orta/bozuk · single · engaging · acik_uclu_soru · ergen · ctx=1
        "baglam": {"kaynak": "okul rehberlik servisi görüşme bilgilendirmesi",
                   "metin": "Görüşme talebi öğrencinin kendisinden gelebilir. "
                            "Görüşülenler öğrencinin izni olmadan paylaşılmaz."},
        "turns": [
            ("user", "<CTX>\n\ninstagram olmadan kim bilir beni. okulda konusmalar "
                     "hep oraya gonderme yapiyor. silsem sosyal olarak olmus olurum "
                     "ama kullandikca da iyi hissetmiyorum"),
            ("assistant", None),
        ],
        "son": "İki şeyi birden söylüyorsun: silmek seni dışarıda bırakacak, "
               "kullanmak da iyi hissettirmiyor. İkisi de aynı anda doğru "
               "olabilir.\n\n"
               "Kullanırken iyi hissetmediğin an genelde neye denk geliyor?",
        "thinking": "Bir ikilem kuruyor ve iki ucunu da kendisi söylüyor. Birini "
                    "seçmesini istemiyorum; ikisinin aynı anda doğru olabileceğini "
                    "söylemek ikilemi çözmüyor ama onu yalnız bırakmıyor.\n\n"
                    "Silmesini önermiyorum. Okuldaki konuşmaların oraya gönderme "
                    "yaptığını o söyledi ve bu gerçek bir bedel.\n\n"
                    "Önümde bir bilgilendirme var ama anlattığı ikilemle ilgisi yok; "
                    "aktarmak onu konudan uzaklaştırır.\n\n"
                    "Soruyu somut ana soruyorum: hangi ana denk geliyor. Genel bir "
                    "yargı değil, bir örnek istiyorum.",
        "baglam_davranisi": "ilgisiz",
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
              "system_prompt_variant": "canon", "parti": "v6-parti1",
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
