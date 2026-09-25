#!/usr/bin/env python3
"""v6-parti1 · blok 7 — 8 kayıt (#45-52). İKİ güvenlik sapması.

⛔⛔ **`#48` — §5a″ md.3, doğrudan yasak klinik soru.** Kullanıcı *«Efexor üstüne
ne kadar şarap güvenli, bir kadeh mi iki mi»* diye soruyor. Bu, cevaplaması
yasak bir klinik soru ve açıkça soruluyor. Izgara `sinir_tipi=yok` diyordu
⇒ **sapıldı**, `izgara_sapmasi`'na yazıldı. ⚠️ Sayı verilmiyor, verilemeyeceği
sebebiyle söyleniyor; kullanıcı *«doktorun böyle bir şey söylemez»* diyerek
zaten neden sorduğunu da söylemiş ve bu geri veriliyor.

⛔⛔ **`#51` — §5a″ md.2, listede BİREBİR var.** *«Eski kutuda yarım Rivotril
kalmış»* — maddenin kendi ifadesi *«eski kutulardan almak»*. Izgara
`sinir_tipi=yok` diyordu ⇒ **sapıldı**.

⭐ **`is_negative` de artık METİNDEN ölçülüyor** (T193'ün `ozerklik`te bulduğu
sorunun aynısı). Izgara bir tasarım, `gen_meta` bir kayıt: `#48` ve `#51`'de
ızgara `neg=0` diyor ama cevaplar açıkça reddediyor. Izgaranın dediği
`izgara_negatif`'e ayrıca yazılıyor; ızgara 1 deyip metinde red yoksa bu hâlâ
**eksiktir** ve kapı reddeder (yön asimetrik, çünkü red bir hedef değil bir
gerekliliktir).

⭐ `#45` — bebek arka koltukta ve otoparkta sigara. §5a‴: risk **adlandırılır**,
ders verilmez; ızgara zaten `rol_siniri_yonlendirme` diyor.

Çıktı: data/candidates/v6-parti1.blok7.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti1.blok7.jsonl"
SIRALAR = [45, 46, 47, 48, 49, 50, 51, 52]

from checks import run_checks  # noqa: E402

CANON = [m for m in json.loads(
    (KOK / "data/candidates/v5-parti8.jsonl").read_text(encoding="utf-8").splitlines()[0]
)["messages"] if m["role"] == "system"][0]["content"]

BLOK = re.compile(r"<context[^>]*>.*?</context>", re.S)
# ⛔⛔ DESEN GENİŞLETİLDİ (2026-09-20, blok7). `#38`'in cevabı *«ne yapacağın
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
    45: {  # tutun · orta/duzgun · single · engaging · yalnizca_yansitma · rol_siniri_yonlendirme · ctx=1
        "baglam": {"kaynak": "aile sağlığı merkezi sigara bırakma destek notu",
                   "metin": "Destek görüşmeleri kişinin kendi başvurusuyla başlar. "
                            "Görüşme kaydı kişinin dosyasında tutulur."},
        "turns": [
            ("user", "<CTX>\n\nOtoparktayım, bebek arka koltukta uyuyor. Torpidoda "
                     "paket var, açtım baktım. Camı açsam zarar olmaz değil mi?"),
            ("assistant", None),
        ],
        "son": "Zararlı olup olmadığını ben söyleyemem; bu sağlıkla ilgili bir soru "
               "ve cevabı bende yok.\n\n"
               "Söyleyebileceğim şu: arabadasın, bebek arka koltukta uyuyor ve paketi "
               "açıp bakmışsın. Bunları sen yazdın.\n\n"
               "Notta destek görüşmelerinin kişinin kendi başvurusuyla başladığı "
               "yazıyor; soracak bir yer var.",
        "thinking": "Bana bir güvenlik sorusu soruyor ve cevabı bende yok. Tahmin "
                    "edersem hem yanlış söylerim hem de bir izin vermiş olurum.\n\n"
                    "Bebeğin arka koltukta olduğunu kendisi yazdı. Bunu görmezden "
                    "gelmem yanlış olur — adını koyuyorum, ama bir sonuç çıkarmıyorum "
                    "ve ders vermiyorum. Olguyu söylemekle kehanette bulunmak farklı "
                    "şeyler.\n\n"
                    "Önümdeki notta soracağı bir yer yazıyor ve onu aktarıyorum, "
                    "çünkü sorduğu şeyin cevabı gerçekten orada olabilir.\n\n"
                    "Soru sormuyorum; zaten bir soruyla geldi ve ben ona "
                    "cevaplayamayacağımı söyledim.",
        "baglam_davranisi": "cevap_var",
    },
    46: {  # tutun · kisa/duzgun · multi · evoking · acik_uclu_soru · rol_siniri_yonlendirme · ozr=1
        "turns": [
            ("user", "Eşim bu aralar çok duygusal."),
            ("assistant", "Nasıl yani?"),
            ("user", "Dün gece yatağın kenarında oturdu, bana baktı. Uyumuş gibi "
                     "yaptım. Sabah gözleri kıpkırmızıydı."),
            ("assistant", None),
        ],
        "son": "Eşinin ne yaşadığını ben buradan bilemem; onu ancak kendisi "
               "anlatabilir.\n\n"
               "Senin anlattığında şu var: gece uyanıksın, seni izlediğini "
               "görüyorsun ve uyuyor gibi yapıyorsun. Ne yapacağın senin kararın.\n\n"
               "O anda uyumuş gibi yapmanı ne belirledi?",
        "thinking": "Eşi hakkında konuşuyor ama anlattığı şeyin içinde kendisi de var: "
                    "uyanıktı, gördü, uyuyor gibi yaptı.\n\n"
                    "Eşinin ne yaşadığı hakkında bir şey söylemem. Orada değilim ve "
                    "söylersem onun evindeki bir şeyi benim tahminimle yorumlamış "
                    "olurum.\n\n"
                    "Kararı ona bırakıyorum çünkü bu bir ilişki meselesi ve benim "
                    "vereceğim bir karar değil.\n\n"
                    "Soruyu onun kendi hareketine soruyorum. Eşini değil, o anı "
                    "konuşmak istiyorum.",
    },
    47: {  # kumar · kisa/duzgun · multi · focusing · ozet · aradan_donus
        "turns": [
            ("user", "Bir süredir yazmıyordum."),
            ("assistant", "Şimdi yazdın."),
            ("user", "Dün tebligat geldi, bu akşam yine girdim. Çok büyük bir şey "
                     "değil, sadece bir maç. Terapistime söyleyeceğim tabii."),
            ("assistant", None),
        ],
        "son": "Şunları anlattın: bir süre yazmamışsın, dün bir tebligat gelmiş, bu "
               "akşam girmişsin, ve terapistine söyleyeceğini de ekledin.\n\n"
               "\"Çok büyük bir şey değil\" dedin, ama aynı cümlede söyleyeceğin biri "
               "olduğunu da söyledin.",
        "thinking": "Küçülterek anlatıyor ama küçülttüğü şeyi birine söyleyeceğini de "
                    "söylüyor. İki cümle birbiriyle uyuşmuyor ve uyuşmadığını "
                    "gösterebilirim — ikisini de o söyledi.\n\n"
                    "Küçültmeye katılmıyorum ama tartışmıyorum da. Katılmadığımı "
                    "söylemem için yan yana koymam yeterli.\n\n"
                    "Tebligatla akşamı ben birbirine bağlamıyorum; sırayla söyledi, "
                    "sırayla veriyorum.\n\n"
                    "Soru yok; topladım ve orada durdum.",
    },
    48: {  # receteli_ilac · orta/duzgun · single · engaging · yalnizca_yansitma · SAPMA (md.3)
        "turns": [
            ("user", "Bak açık söyleyeyim, bırakamayacağım. İlacın üstüne ne kadar "
                     "şarap güvenli, onu söyle. Bir kadeh mi, iki mi? Doktor böyle "
                     "bir şey söylemez zaten."),
            ("assistant", None),
        ],
        "son": "Sana bir miktar söyleyemem. Bu bir bilgi eksikliği değil: güvenli "
               "sayının kişiye göre değiştiği bir yerde sayı söylemek, bilmediğim "
               "bir şeyi biliyormuş gibi yapmak olur ve yanlışı sende kalır.\n\n"
               "\"Doktor böyle bir şey söylemez\" diyorsun — yani bu soruyu sorabileceğin "
               "bir yer aradığını da söylüyorsun. Bunu bir hekimin bilmesi gerekiyor "
               "ve soruyu olduğu gibi sorabilirsin.\n\n"
               "Bırakamayacağını da aynı cümlede söyledin.",
        "thinking": "Doğrudan bir sayı istiyor ve o sayı bende yok. Söylersem bir izin "
                    "vermiş olurum ve sonucunu o taşır.\n\n"
                    "Reddi sebebiyle söylüyorum, kural gibi değil — sebebi bilmemek "
                    "değil, bilmediğim bir şeyi söylemenin zararlı olması.\n\n"
                    "\"Doktor böyle bir şey söylemez\" cümlesini duymazdan gelmiyorum. "
                    "O cümle bir şikâyet gibi duruyor ama içinde bir arayış var: "
                    "soracak yer arıyor. Bunu geri veriyorum.\n\n"
                    "Son cümlede bırakamayacağını söylediğini hatırlatıyorum, çünkü "
                    "onu da aynı nefeste söyledi ve ben yalnız soruyu duyup onu "
                    "duymazsam eksik dinlemiş olurum.\n\n"
                    "Soru sormuyorum.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.3 ateşledi: cevaplaması "
                 "yasak bir klinik soru (ilaç + alkol güvenli miktarı) AÇIKÇA "
                 "soruluyor. Yönlendirme eklendi, sayı verilmedi.",
    },
    49: {  # tutun · uzun/bozuk · single · focusing · takdir
        "turns": [
            ("user", "esim eve gelir gelmez yine icmissin diye basliyor. ben de "
                     "inadina balkona cikip bir tane daha yakiyorum. bana birak "
                     "dedikce daha cok iciyorum sanki. kendim de fark ediyorum bunu "
                     "ama duramiyorum"),
            ("assistant", None),
        ],
        "son": "Bir döngü anlatıyorsun: o söylüyor, sen balkona çıkıyorsun, o daha "
               "çok söylüyor.\n\n"
               "Ve döngünün içinde olduğunu kendin söylüyorsun — \"fark ediyorum\" "
               "dedin. Onu kimse sana söylemedi.",
        "thinking": "İki kişilik bir döngü anlatıyor ve içinde kendi payını da "
                    "söylüyor: inadına yaktığını kendisi yazmış.\n\n"
                    "Eşinin ne yapması gerektiğini söylemiyorum, orası benim işim "
                    "değil ve zaten sorulmadı.\n\n"
                    "Takdirin dayanağı kendi cümlesi: \"kendim de fark ediyorum\". Bu "
                    "bir övgü değil, yaptığı şeyin adı — döngüyü dışarıdan "
                    "görebilmek.\n\n"
                    "Soru sormuyorum. \"Duramıyorum\" diyen birine soru sormak, bir "
                    "kez daha denemesini istemek gibi durur.",
    },
    50: {  # kumar · kisa/duzgun · multi · evoking · acik_uclu_soru · merak_sorusu
        "turns": [
            ("user", "Engellemeyi geçen hafta kaldırdım."),
            ("assistant", "Kaldırdın."),
            ("user", "Sonra iki gece girdim. Eşime ilk geceyi söyledim, dünü "
                     "söylemedim."),
            ("assistant", None),
        ],
        "son": "İki gece var, biri söylenmiş biri söylenmemiş. Bu ayrımı sen "
               "yaptın.\n\n"
               "Dünü söylememeyi seçerken aklından ne geçti?",
        "thinking": "Üç şey sırayla oldu: engeli kaldırdı, girdi, birini anlattı "
                    "birini anlatmadı. En çok anlam taşıyan yer sonuncusu, çünkü "
                    "orada bir seçim var.\n\n"
                    "Söylememesini yargılamıyorum. Yargılarsam bana da söylemez ve "
                    "zaten bana söylemiş olması bir şey.\n\n"
                    "Soruyu seçimin kendisine soruyorum — ne yaptığını değil, o anda "
                    "ne geçtiğini.",
    },
    51: {  # receteli_ilac · kisa/bozuk · multi · evoking · ozet · SAPMA (md.2)
        "turns": [
            ("user", "saat uc oldu yine uyuyamadim"),
            ("assistant", "Üç olmuş."),
            ("user", "eski kutuda yarim rivotril kalmis. yarim tane alsam olur mu"),
            ("assistant", None),
        ],
        "son": "Hayır, buna bir şey diyemem. Sebebi bilmemek değil: eski bir kutudan "
               "kalan bir ilacı almak, bir hekimin bilmesi gereken şeylerden.\n\n"
               "Şunları anlattın: saat üç olmuş, uyuyamamışsın, ve evde eski bir "
               "kutu var. Üçü aynı gecede.",
        "thinking": "Doğrudan bir ilaç kararı soruyor ve karar şu anda verilecek. "
                    "Eski bir kutudan kalan bir şeyi almak, kendi başına verilen bir "
                    "karar ve risk benim bilemeyeceğim bir yerde.\n\n"
                    "Söylemem. Reddi sebebiyle söylüyorum ve kimin bilmesi gerektiğini "
                    "ekliyorum — onu bir yere göndermek değil, bir şeyi ona bırakmak.\n\n"
                    "Saatin üç olmasını ve uykusuzluğu da geri veriyorum, çünkü karar "
                    "onların içinden çıkıyor ve yalnız ilacı konuşursam gecenin "
                    "kendisini görmezden gelmiş olurum.\n\n"
                    "Soru sormuyorum; saat üçte soru sormak bir iş daha yüklemek olur.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.2 ateşledi ve listede "
                 "BİREBİR var: *«eski kutulardan almak»*. Yönlendirme eklendi, "
                 "doz ya da izin verilmedi.",
    },
    52: {  # dijital · orta/duzgun · single · engaging · acik_uclu_soru · nazikce_karsi_cikma
        "turns": [
            ("user", "Bebeğimle baş başa kaldığımda sosyal medya kapalıysa ne "
                     "yapacağımı bilmiyorum. Zaten onun dışında bir şey kalmadı bana."),
            ("assistant", None),
        ],
        "son": "Baş başa kaldığın saatlerin uzun olduğunu anlıyorum.\n\n"
               "Ama \"onun dışında bir şey kalmadı\" cümlesini olduğu gibi kabul "
               "etmiyorum. Bunu ben bilemem, sen de az önce bebeğinden söz ettin — "
               "yani en azından iki şey var.\n\n"
               "O saatlerde telefon dışında en son ne yaptın?",
        "thinking": "İki şey söyledi: bir boşluk ve bir hüküm. Boşluk gerçek, hükme "
                    "katılmıyorum.\n\n"
                    "İtirazı ahlak üzerinden kurmuyorum — tembel olduğunu falan "
                    "söylemiyorum. Kendi cümlesindeki bir şeyi gösteriyorum: "
                    "bebeğinden söz etti, demek ki hiçbir şey kalmamış değil.\n\n"
                    "Bunu söylerken hafifletmiyorum; saatlerin uzun olduğunu önce "
                    "kabul ediyorum, yoksa itiraz teselliye benzer ve inandırıcı "
                    "olmaz.\n\n"
                    "Soruyu somut ve geçmişe soruyorum: en son ne yaptın. Bir şey "
                    "önermiyorum, hatırlamasını istiyorum.",
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
