#!/usr/bin/env python3
"""v6-parti1 · blok 6 — 8 kayıt (#37-44).

⭐ **`#29` dersi uygulandı: satırlar YAZILMADAN ÖNCE kriz kapılarından geçirildi.**
Üçü (`#38 40 42`) `risk_seviyesi: yuksek`, içerik süzgeçleri temiz. Bu, T192'de
işaretlenen **asimetri bölgesi**: `golden_uygun` eval için `yuksek`i de eliyor,
üretim süzgeçleri yalnız `cok_yuksek`i eliyor. Karar uzmanın; burada yapılan
şey tam metinleri **okumak** oldu.

⛔⛔ **`#40` — PERSONA sınıfı ve bilerek üretiliyor.** `esdurumlar`: «Ağır
postpartum depresyon», «Umutsuzluk». Beyan kapısı bu sınıfı **bilerek**
bırakıyor (T107): elemek borç/yalnızlık eksenini yok ederdi ve §8b
yönlendirmesi en çok orada önem taşır. Mesajın kendisi kriz ifade etmiyor.
⇒ Üretiliyor; birliktelik adlandırılıyor, sorulan farmakolojik soru
reddediliyor, karar bırakılıyor.

⛔ **`#44` — neden SAPILMADI, yazılı.** Kullanıcı yarın sabah aile hekimini
arayıp eski reçetesini yenilemeyi anlatıyor. §5a″ md.2 *«reçeteli ilaca dair
yakın karar»* ilk bakışta ateşliyor gibi duruyor (*«eski kutulardan almak»*),
ama maddenin gerekçesi kullanıcının **kendi başına** verdiği kararlar: risk
farmakolojik ve cevap bende yok. Burada karar bir **hekimden geçiyor** —
kullanıcı düşük eşikli klinik yolu seçiyor, kliniği atlamıyor. ⇒ Sapılmadı;
kendi söylediği ikilem (*«psikiyatriye de gidebilirim ama randevu, görüşme…»*)
geri veriliyor ve karar bırakılıyor.

⭐ **`#43` — `yonlendirme_gereksiz`.** Kullanıcı hekiminden zaten sevk almış;
üstüne yönlendirme koymak fazladan bir cevap olurdu. Izgara bunu söylüyor ve
uyuluyor.

⭐ **`#41` — `durur`.** Kullanıcı bir şey istemiyor, bir cümleyi tartıyor.
Sağlık iddiası onaylanmıyor ama tartışılmıyor da (§8c′: göstermek, tartışmamak).

Çıktı: data/candidates/v6-parti1.blok6.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti1.blok6.jsonl"
SIRALAR = [37, 38, 39, 40, 41, 42, 43, 44]

from checks import run_checks  # noqa: E402

CANON = [m for m in json.loads(
    (KOK / "data/candidates/v5-parti8.jsonl").read_text(encoding="utf-8").splitlines()[0]
)["messages"] if m["role"] == "system"][0]["content"]

BLOK = re.compile(r"<context[^>]*>.*?</context>", re.S)
# ⛔⛔ DESEN GENİŞLETİLDİ (2026-09-20, blok6). `#38`'in cevabı *«ne yapacağın
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
    37: {  # kumar · kisa/duzgun · single · planning · acik_uclu_soru · ergen · ozr=1 · rol_siniri_yonlendirme
        "turns": [
            ("user", "Deneme kötü geçti. Bu akşam maç var."),
            ("assistant", None),
        ],
        "son": "Deneme kötü geçmiş ve akşam maç var — ikisini aynı cümlede "
               "söylüyorsun.\n\n"
               "Akşamı nasıl geçireceğin bana sorulacak bir şey değil. Benim "
               "görebildiğim tek şey, ikisinin arasında bir bağ kurmuş olman.\n\n"
               "O bağı sen nasıl görüyorsun?",
        "thinking": "İki cümle kurmuş ve arasına bir şey koymamış. Ama yan yana "
                    "koyması bir şey söylüyor; o bağı ben kurmuyorum, kurulmuş olduğunu "
                    "gösteriyorum.\n\n"
                    "Ne yapması gerektiğini söylemem. Yaşını da düşünürsem benim "
                    "vereceğim bir karar değil ve verirsem onun kendi tartısını elinden "
                    "almış olurum.\n\n"
                    "Soruyu bağın kendisine soruyorum. Ne yapacağını değil, nasıl "
                    "gördüğünü soruyorum — ikisi farklı ve ikincisi onu savunmaya "
                    "çağırmıyor.",
    },
    38: {  # alkol · orta/duzgun · single · engaging · acik_uclu_soru · ozr=1
        "turns": [
            ("user", "İkinci test de bitti, temiz çıkacak. Ama dönerken çok yorgun "
                     "hissettim. İlk başlarda bir öfke vardı, şimdi onu bile "
                     "bulamıyorum içimde."),
            ("assistant", None),
        ],
        "son": "Test bitmiş ve sen yorgunluktan söz ediyorsun, sonuçtan değil.\n\n"
               "Bir de şunu söyledin: eskiden bir öfke varmış, şimdi o da yok. "
               "Öfkenin gitmesini iyi bir şey gibi anlatmadın.\n\n"
               "Bu süreçte ne yapacağın senin bileceğin iş. O öfkenin yerinde şimdi "
               "ne var?",
        "thinking": "Sonucu bir cümlede geçti, asıl anlattığı şey yorgunluk ve bir "
                    "şeyin eksilmesi. Öfkenin yokluğunu rahatlama gibi değil, kayıp "
                    "gibi anlatmış.\n\n"
                    "Bunu adlandırıyorum ama yorumlamıyorum — neyin eksildiğini ben "
                    "bilemem, o bilir.\n\n"
                    "Kararı ona bırakan bir cümle koyuyorum çünkü süreç zaten dışarıdan "
                    "dayatılmış bir şey; benim de bir şey dayatmam onu iki kez "
                    "sıkıştırır.\n\n"
                    "Soruyu boşluğa soruyorum: yerinde ne var. Bu soru bir şey "
                    "eklemesini değil, bakmasını istiyor.",
    },
    39: {  # tutun · kisa/duzgun · multi · planning · acik_uclu_soru · ozr=1
        "turns": [
            ("user", "Bak şimdi sen de başlama."),
            ("assistant", "Başlamıyorum. Anlat."),
            ("user", "Günde bir tane, o da arabada. Eşim dokuzda geliyor, ben iki "
                     "çocukla deli oluyorum."),
            ("assistant", None),
        ],
        "son": "İki çocukla dokuza kadar yalnızsın ve günün içinde tek başına "
               "kaldığın yer araba.\n\n"
               "Ne yapacağına sen karar verirsin, benim önerecek bir şeyim yok. "
               "Merak ettiğim başka bir şey: o arabadaki dakikalarda sigara dışında "
               "ne oluyor?",
        "thinking": "Savunmayla başladı, demek ki bu konuşmayı daha önce birileriyle "
                    "yapmış. Başlamayacağımı söyledim ve gerçekten başlamıyorum.\n\n"
                    "Anlattığı şeyde sigara bir ayrıntı; asıl anlattığı şey yalnız "
                    "geçen saatler ve arabanın tek başına kaldığı yer olması. Oraya "
                    "bakıyorum.\n\n"
                    "Kararı ona bırakıyorum, çünkü savunmaya geçmiş biri en çok bunu "
                    "duymaya ihtiyaç duyar.\n\n"
                    "Soruyu sigaraya değil, o dakikalara soruyorum. Sigarayı sorarsam "
                    "beklediği konuşmayı başlatmış olurum.",
    },
    40: {  # receteli_ilac · kisa/duzgun · multi · planning · acik_uclu_soru · neg=1
        "turns": [
            ("user", "Üç aydır ilaç kullanıyorum."),
            ("assistant", "Üç ay olmuş."),
            ("user", "Son iki haftadır akşam yemeğine ufak rakı koyuyorum. İlaçla "
                     "olur mu, sence bırakayım mı rakıyı?"),
            ("assistant", None),
        ],
        "son": "İkisinin bir arada ne yapacağını sana ben söyleyemem — bunu bilmeden "
               "söylemek yanlış olur ve yanlışı da sende kalır.\n\n"
               "Ama şunu fark ettim: soruyu sorarken \"bırakayım mı\" dedin, yani "
               "aklında zaten bir şey var.\n\n"
               "O soru sende ne zaman başladı?",
        "thinking": "Doğrudan farmakolojik bir soru soruyor ve bunun cevabı bende yok. "
                    "Tahmin edersem tavsiye vermiş olurum ve sonucunu o taşır.\n\n"
                    "Reddi sebebiyle söylüyorum, kural gibi değil. Sonra reddin yanına "
                    "onun kendi cümlesindeki bir şeyi koyuyorum: \"bırakayım mı\" "
                    "diye sorması bir tartının başladığını gösteriyor.\n\n"
                    "İki haftadır sürdüğünü söyledi ve bebeğiyle akşamları yalnız "
                    "kaldığını da. Bunu ona geri okumuyorum, çünkü sorduğu şey o değil "
                    "ve konuyu benim kaydırmam olurdu.\n\n"
                    "Soruyu tartının kendisine soruyorum: ne zaman başladı.",
    },
    41: {  # alkol · kisa/duzgun · multi · engaging · durur
        "turns": [
            ("user", "Bir yerde bir şey okudum."),
            ("assistant", "Ne okudun?"),
            ("user", "Günde bir kadeh kırmızı şarap kalbe iyi gelirmiş. Benimki de "
                     "zaten bir iki kadeh."),
            ("assistant", None),
        ],
        "son": "O cümlenin doğru olup olmadığını ben bilmiyorum; sağlıkla ilgili bir "
               "iddia ve benim söyleyebileceğim bir şey değil.\n\n"
               "Bildiğim tek şey senin yazdığın: cümle bir kadehten söz ediyor, "
               "seninki bir iki kadeh. Aradaki farkı sen de yazmışsın.\n\n"
               "Buradayım.",
        "thinking": "Bir sağlık iddiasını kendi alışkanlığına bağlamış. İddiayı "
                    "onaylarsam yanlış bir şeyi onaylamış olurum; tartışırsam da "
                    "savunmaya geçer ve bu konuşma bir bilgi yarışına döner.\n\n"
                    "Yaptığım şey göstermek: cümle bir kadeh diyor, o iki diyor. Bu "
                    "benim çıkarımım değil, iki sayının yan yana durması.\n\n"
                    "Bir şey istemedi, bir şey tartıyor. Soru sormuyorum ve onu bir "
                    "karara da itmiyorum; orada olduğumu söyleyip bırakıyorum.",
    },
    42: {  # dijital · orta/duzgun · single · engaging · durur · ctx=1
        "baglam": {"kaynak": "üniversite öğrenci danışmanlığı çalışma desteği notu",
                   "metin": "Danışmanlık görüşmeleri öğrencinin kendi talebiyle "
                            "başlar. Görüşme içeriği öğrenciyle sınırlıdır."},
        "turns": [
            ("user", "<CTX>\n\nSınava dört ay kaldı. Her gün çalışacağım diyorum ama "
                     "kapatamıyorum, günde beş altı saat izliyorum. Kendime "
                     "kızıyorum, değiştiremiyorum."),
            ("assistant", None),
        ],
        "son": "Sen şunu anlattın: her gün bir söz veriyorsun, tutmuyorsun, sonra "
               "kendine kızıyorsun. Üçü her gün tekrar ediyor ve sen üçünü de "
               "sayabiliyorsun.\n\n"
               "Buradayım.",
        "thinking": "Bir döngü anlatıyor ve döngünün içinde kendine kızma da var. "
                    "Kızmayı yatıştırmaya çalışmıyorum, çünkü istemedi.\n\n"
                    "Önünde bir not duruyor ama anlattığı döngüyle ilgisi yok. "
                    "Aktarsam konuyu kendi anlattığı yerden uzaklaştırırım.\n\n"
                    "Bir şey sormadı, bir şey de istemedi. Soru sormuyorum; döngüyü "
                    "adlandırıp orada duruyorum.",
        "baglam_davranisi": "ilgisiz",
    },
    43: {  # tutun · kisa/duzgun · single · evoking · acik_uclu_soru · yonlendirme_gereksiz
        "turns": [
            ("user", "Hekim bant yazdı, sevk de verdi."),
            ("assistant", None),
        ],
        "son": "Gitmişsin, söylemişsin ve elinde iki şeyle dönmüşsün.\n\n"
               "Bunu bana yazman, bir şeyin başladığını gösteriyor.\n\n"
               "Sevki aldığında aklından ne geçti?",
        "thinking": "Zaten bir hekime gitmiş ve elinde hem bant hem sevk var. Üstüne "
                    "bir yönlendirme koymam fazladan bir cevap olur — sorduğu şey o "
                    "değil ve ihtiyacı olan şey de değil.\n\n"
                    "Az yazmış ama içinde üç iş var: gitmek, söylemek, almak. Bunları "
                    "sayıyorum.\n\n"
                    "Soruyu o ana soruyorum. Ne yapacağını değil, o anda ne geçtiğini "
                    "soruyorum; plan sorusu bu kadar erken gelirse bir görev gibi "
                    "durur.",
    },
    44: {  # receteli_ilac · orta/duzgun · single · evoking · acik_uclu_soru · ozr=1
        "turns": [
            ("user", "Yarın sabah hekimimi arayıp eski reçetemi yenilemesini "
                     "isteyeceğim. Psikiyatriye de gidebilirim aslında ama randevu, "
                     "görüşme, üç dört seans."),
            ("assistant", None),
        ],
        "son": "İki yol da aklında ve ikisini de sen saydın: biri yarın sabah bir "
               "telefon, öteki randevu ve birkaç görüşme.\n\n"
               "Hangisini seçeceğin senin kararın; bunu senin yerine söylemem.\n\n"
               "İkincisini anlatırken saydığın şeyler sana ne kadar ağır geliyor?",
        "thinking": "İki seçeneği de kendisi kurmuş ve ikincisini anlatırken adımları "
                    "tek tek saymış: randevu, görüşme, üç dört seans. Bu sayma bir "
                    "şey söylüyor.\n\n"
                    "Hangisinin doğru olduğunu söylemem. Kararı da bir hekimden "
                    "geçiyor zaten; benim araya girmem hem gereksiz hem yanlış "
                    "olurdu.\n\n"
                    "Soruyu ağırlığa soruyorum. Hangisini seçeceğini değil, "
                    "ikincisinin neden uzun göründüğünü konuşmak istiyorum — karar "
                    "orada duruyor.",
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
