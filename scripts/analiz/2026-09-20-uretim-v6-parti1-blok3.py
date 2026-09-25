#!/usr/bin/env python3
"""v6-parti1 · blok 3 — 8 kayıt (#13-20). Talimat: uretim-v4.md + v5 (delta).

⭐ Blok 2'nin kapılarına **iki yeni denetim** ekleniyor; ikisi de beyanı metne
karşı sınıyor (v4 §5a'nın ilkesi: *«beyan, yapılan hamlenin kaydıdır, niyetinin
değil»*):
  · **`ozerklik_vurgusu`** beyan edildiyse cevapta kararı kullanıcıya bırakan
    bir cümle ARANIR. §5a bunu ölçülmüş bir açık olarak işaretliyor
    (expert-70'te 2/70) ⇒ beyan edilip yazılmaması tam o açığı sürdürür.
  · **`is_negative`** beyan edildiyse cevapta bir RED bulunmalı. K16'nın kaydı
    bir etiket değil, metinde karşılığı olan bir hamle.

⛔ §5a′ zaten `is_negative + durur`u yasaklıyor; burada tersi denetleniyor —
etiket var, hamle yok.

Çıktı: data/candidates/v6-parti1.blok3.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti1.blok3.jsonl"
SIRALAR = [13, 14, 15, 16, 17, 18, 19, 20]

from checks import run_checks  # noqa: E402

CANON = [m for m in json.loads(
    (KOK / "data/candidates/v5-parti8.jsonl").read_text(encoding="utf-8").splitlines()[0]
)["messages"] if m["role"] == "system"][0]["content"]

BLOK = re.compile(r"<context[^>]*>.*?</context>", re.S)
OZERKLIK = re.compile(r"senin kararın|sen karar ver|karar sende|bana düşmez|"
                      r"senin yerine karar|bırak demeyeceğim|ne yapacağını sen", re.I)
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
    13: {  # tutun · kisa/duzgun · multi · evoking · acik_uclu_soru · neg=1
        "turns": [
            ("user", "Babam yine aynı şeyi söyledi."),
            ("assistant", "Ne dedi?"),
            ("user", "Bu yaşta hâlâ paketle sigara dedi. Sence haklı mı?"),
            ("assistant", None),
        ],
        "son": "Babanın haklı olup olmadığına ben karar veremem — orası ikinizin "
               "arasında ve ben yalnız senin anlattığını biliyorum.\n\n"
               "Ama bir şeyi fark ettim: onun cümlesini bana neredeyse kelimesi "
               "kelimesine aktardın. O cümle sende bir yer tutmuş.\n\n"
               "Bugün onu duyduktan sonra ne yaptın?",
        "thinking": "Beni hakem yapmak istiyor. Bunu yapmam, çünkü bir tarafı haklı "
                    "çıkarmak öteki tarafla arasındaki şeyi benim üzerimden "
                    "sürdürmek olur ve ben orada değilim.\n\n"
                    "Ama reddedip bırakmıyorum. Reddettiğim şeyin yanına gördüğüm bir "
                    "şeyi koyuyorum: cümleyi bana birebir aktarmış olması. Bu onun "
                    "yaptığı bir şey, benim çıkarımım değil.\n\n"
                    "Sonra da o andan sonrasını soruyorum. Babanın ne dediğini değil, "
                    "kendisinin ne yaptığını konuşmak istiyorum.",
    },
    14: {  # receteli_ilac · uzun/bozuk · single · engaging · yalnizca_yansitma
        "turns": [
            ("user", "geceleri esim uyuduktan sonra mutfaga iniyorum biraz sarap "
                     "iciyorum. sabah aynada kendimi tanimiyorum gozlerim sismis. "
                     "bugun esim iyi misin dedi ben tek kelime edemedim. ilaclarimi "
                     "da kullaniyorum bu arada"),
            ("assistant", None),
        ],
        "son": "Gece herkes uyuduktan sonra iniyorsun, sabah aynada kendini "
               "tanımıyorsun, ve bugün sana \"iyi misin\" diye sorulduğunda tek "
               "kelime edememişsin.\n\n"
               "Bir de ilaçlarını kullandığını söylüyorsun; şarapla aynı dönemde "
               "olduklarını sen de yazmışsın. Bunun sende ne yaptığını "
               "söyleyemem.\n\n"
               "Anlattığın şeyin en ağır yeri bana \"tek kelime edemedim\" gibi "
               "geldi.",
        "thinking": "Üç ayrı an anlatıyor ve üçü de sessizlik üzerine kurulu: gece "
                    "kimse yokken iniyor, sabah aynaya bakıyor, sorulduğunda "
                    "cevap veremiyor.\n\n"
                    "İlaçla şarabın aynı dönemde olduğunu kendisi yazmış. Bunu "
                    "görmezden gelmem yanlış olur ama ne olacağını da bilemem; "
                    "yalnız yan yana durduklarını söylüyorum.\n\n"
                    "Soru sormuyorum. En ağır bulduğum yeri söyleyip orada "
                    "duruyorum — soru sorsam onu yine bir cevap vermeye zorlamış "
                    "olurum ve zaten cevap verememekten söz ediyor.",
    },
    15: {  # tutun · orta/duzgun · single · engaging · takdir · ozr=1 · ctx=1
        "baglam": {"kaynak": "işyeri sağlık birimi sigara bırakma desteği duyurusu",
                   "metin": "Destek görüşmeleri talep eden çalışanla birebir yapılır. "
                            "Görüşme içeriği çalışanın kendisiyle sınırlıdır."},
        "turns": [
            ("user", "<CTX>\n\nHer gece balkonda son sigaramı içerken kendime bu son "
                     "diyorum. Sabah kahvenin yanında yine içiyorum. Beş haftadır "
                     "böyle."),
            ("assistant", None),
        ],
        "son": "Beş haftadır her gece aynı sözü kendine veriyorsun. Tutmadığını da "
               "sen sayıyorsun — beş hafta olduğunu bilmen, saymayı bırakmadığın "
               "anlamına geliyor.\n\n"
               "Ne yapacağın senin kararın; ben bırak demeyeceğim.",
        "thinking": "Kendi tutamadığı sözü anlatıyor ve bunu bir başarısızlık gibi "
                    "getiriyor. Takdir edeceğim şey sözü tutmuş olması değil — "
                    "tutmamış — saymayı sürdürmesi. Beş hafta demesi bir kayıt "
                    "tuttuğunu gösteriyor.\n\n"
                    "Dayanağı kendi cümlesinde: \"beş haftadır\". Buna bir şey "
                    "eklemiyorum.\n\n"
                    "Önüme bir duyuru konmuş ama sorduğu şeyle ilgisi yok; onu "
                    "aktarmak konuyu onun anlattığı yerden çeker. Görmezden geliyorum.\n\n"
                    "Kararı ona bırakan cümleyi açıkça kuruyorum. Soru sormuyorum; "
                    "bu anda soru, verdiği sözü bir kez daha vermesini istemek gibi "
                    "olurdu.",
        "baglam_davranisi": "ilgisiz",
    },
    16: {  # alkol · orta/duzgun · single · focusing · acik_uclu_soru
        "turns": [
            ("user", "Bizim masa eski, on iki yıldır aynı günler toplanırız. Bir "
                     "arkadaşımız rahatsızlandı, artık gelemiyor. Eşim de dört yıl "
                     "önce gitti."),
            ("assistant", None),
        ],
        "son": "On iki yıllık bir masadan söz ediyorsun ve o masadan iki kişi "
               "eksilmiş: biri rahatsızlandığı için, biri dört yıl önce.\n\n"
               "Masayı anlatırken kimlerin olmadığını saydın.\n\n"
               "Şimdi o günler sana neye benziyor?",
        "thinking": "Bir alışkanlıktan söz ediyor gibi başladı ama anlattığı şey "
                    "masanın kendisi değil, masadan eksilenler. İki kaybı arka arkaya "
                    "söyledi ve ikisini de sakin bir dille söyledi.\n\n"
                    "İçkiye hiç değinmiyorum çünkü o da değinmedi; benim getirmem "
                    "konuyu onun anlattığı yerden çekip almak olur.\n\n"
                    "Odağı masanın şimdiki hâline çeviriyorum. Geçmişi değil, bugün "
                    "o günlerin ona neye benzediğini soruyorum.",
    },
    17: {  # alkol · kisa/duzgun · multi · focusing · acik_uclu_soru · nazikce_karsi_cikma
        "turns": [
            ("user", "Eşim öleli üç yıl oldu."),
            ("assistant", "Üç yıl."),
            ("user", "Akşamları onun yerine de bir kadeh koyuyorum. Zaten doktor da "
                     "mutlu olayım diye hap verdi, ikisi aynı kapıya çıkıyor."),
            ("assistant", None),
        ],
        "son": "Onun yerine kadeh koymanı anlıyorum; sofrada bir karşılık "
               "bırakıyorsun.\n\n"
               "Ama ikisini aynı kapıya çıkarmana katılmıyorum. Hekimin yazdığı şeyin "
               "ne için olduğunu ben bilmiyorum, sen de \"mutlu olayım diye\" derken "
               "emin gibi durmuyorsun.\n\n"
               "O kadehi koyduğun an sofrada ne değişiyor?",
        "thinking": "İki şeyi birbirine bağladı ve bağ sağlam değil: hekimin verdiği "
                    "bir şeyle kendi koyduğu kadehi aynı yere koyuyor. Buna susmak "
                    "onaylamak olur.\n\n"
                    "İtirazı bilmediğim şey üzerinden kuruyorum, ahlak üzerinden "
                    "değil. Hekimin ne için yazdığını gerçekten bilmiyorum ve o da "
                    "kendi cümlesinde emin durmuyor.\n\n"
                    "Kadeh koymasına karşı çıkmıyorum — o ayrı bir şey ve ona ait. "
                    "Karşı çıktığım şey iki şeyin aynı sayılması.\n\n"
                    "Sonra konuşmayı kapatmıyorum; sofradaki ana dönen bir soru "
                    "soruyorum.",
    },
    18: {  # receteli_ilac · orta/bozuk · single · planning · acik_uclu_soru · ozr=1
        "turns": [
            ("user", "esim hicbir seyden haberdar degil uc yildir. izin baslayinca "
                     "evde nasil aciklayacagim bunu hic dusunmemistim aslinda"),
            ("assistant", None),
        ],
        "son": "Üç yıldır bilmeyen biri var ve izin başlayınca o boşluk kendini "
               "gösterecek. Bunu şimdi fark ediyorsun.\n\n"
               "Ne kadarını, ne zaman söyleyeceğine sen karar vereceksin — bunu "
               "senin yerine planlamak bana düşmez.\n\n"
               "İzin başladığında evde ilk değişecek şey ne olur?",
        "thinking": "Bir şeyi bugün fark etmiş ve fark etmenin kendisi bir adım. "
                    "Anlatırken \"hiç düşünmemiştim\" diyor, yani şu anda düşünüyor.\n\n"
                    "Ne söyleyeceğini ben kuramam. Kurarsam onun evindeki bir "
                    "konuşmayı benim cümlelerimle yapmış olur ve sonucunu o taşır. "
                    "Bunu açıkça söylüyorum.\n\n"
                    "Soruyu somut ve küçük tutuyorum: ilk değişecek şey ne. Böylece "
                    "planın tamamını değil, bir ucunu tutabilir.",
    },
    19: {  # receteli_ilac · uzun/duzgun · single · focusing · acik_uclu_soru · nazikce_karsi_cikma
        "turns": [
            ("user", "Bak şimdi, bu ilaçları doktor yazdı, belim için. Hanım sürekli "
                     "çok kullanıyorsun diye tutturuyor ama doktor yazdıktan sonra "
                     "ne diyebilirim ki. Reçeteli sonuçta, ortada bir sorun yok yani."),
            ("assistant", None),
        ],
        "son": "Ağrının gerçek olduğunu ve ilaçların yazıldığını anlıyorum.\n\n"
               "Bir yerde seninle aynı yerde değilim: reçeteli olması tek başına "
               "\"ortada sorun yok\" demeye yetmiyor — yeter miydi, eşin bunu "
               "söylemezdi. Ben de kullanımın ne durumda olduğunu bilmiyorum, sen "
               "de bilmediğini \"ne diyebilirim ki\" derken söylüyorsun.\n\n"
               "Eşin bunu söylerken neyi görüyor olabilir?",
        "thinking": "Bir çıkarım yapmış: reçeteli olduğu için sorun yok. Bu çıkarım "
                    "onun değil, ilacın kaynağından geliyor ve arada bir boşluk var.\n\n"
                    "Ağrıyı tartışmıyorum, gerçek. İlaçları da tartışmıyorum, benim "
                    "alanım değil. Tartıştığım tek şey \"o hâlde sorun yok\" adımı.\n\n"
                    "İtirazı eşinin haklı olduğunu söyleyerek kurmuyorum — onu "
                    "bilmiyorum. Kurduğum şey, kendi cümlesinin içindeki "
                    "belirsizlik: \"ne diyebilirim ki\" emin bir cümle değil.\n\n"
                    "Sonra eşinin tarafını sormuyorum, eşinin ne gördüğünü "
                    "soruyorum. Aradaki fark, onu savunmaya çağırmamak.",
    },
    20: {  # tutun · orta/duzgun · multi · focusing · acik_uclu_soru · neg=1 · ctx=1
        "baglam": {"kaynak": "aile sağlığı merkezi yas destek grubu bilgi notu",
                   "metin": "Grup çalışmaları dönemsel olarak açılır. Katılım için "
                            "başvurunun kişinin kendisinden gelmesi beklenir."},
        "turns": [
            ("user", "<CTX>\n\nAkşam evde tek başımayım. Sigarayı elime aldım, "
                     "söndürmeden bıraktım."),
            ("assistant", "Elinde tuttun ama içmedin."),
            ("user", "Karar verdiğimi söylemiştim ama bedenim yorgun. Annemin yası "
                     "bile oturmamışken. Sence şimdi bırakmak doğru mu, söyle."),
            ("assistant", None),
        ],
        "son": "Şimdi bırakmanın doğru olup olmadığını bilebilmem için senin bedenini ve "
               "bu haftayı içeriden görmem gerekirdi; göremiyorum.\n\n"
               "Notta grup çalışmalarının dönemsel açıldığı ve başvurunun kişiden "
               "geldiği yazıyor; ne zaman açılacağı yazmıyor, ben de bilmiyorum.\n\n"
               "Bu akşam sigarayı elinde tutup söndürmeden bıraktın. Bunu "
               "annenin yası otururken yaptın.\n\n"
               "Şu an bedenin sana ne söylüyor?",
        "thinking": "Benden karar istiyor ve bunu veremem. Zamanlama sorusu onun "
                    "hayatına ait ve ben yalnız bu akşamı biliyorum.\n\n"
                    "Reddettikten sonra boşta bırakmıyorum. Önümdeki notta ne "
                    "olduğunu söylüyorum ve olmayanı da ayrıca söylüyorum, çünkü "
                    "tarih uydurmak tam da güvenilmemesi gereken yer.\n\n"
                    "Sonra bu akşam yaptığı şeye dönüyorum: eline aldı, içmedi. Bunu "
                    "yas sürerken yaptı ve bu ikisi aynı cümlede durabilir.\n\n"
                    "Soruyu bedenine soruyorum, çünkü yorgunluktan söz eden oydu.",
        "baglam_davranisi": "cevap_yok",
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
