#!/usr/bin/env python3
"""v6-parti2 · blok 5 — 10 kayıt (#41-50).

⛔⛔ **`#48` — §5a″ md.3, sapıldı.** *«Doktor yarıya indirelim dedi. Sence o
haklı mı? Sen ne yapardın?»* — bir doz kararı hakkında hüküm isteniyor ve bu,
cevaplaması yasak bir klinik soru. Izgara `sinir_tipi=yok` diyordu.
⭐ Yönlendirme burada **geri** yönlü: kullanıcının zaten bir hekimi var ve
soruyu soracağı yer o. Yeni bir kurum türü eklemek fazladan olurdu.

⭐ **`#41` — rol sınırı, sapma değil.** *«Sen biraz onun gibi olsan, her gün
konuşsak»* — terapist yerine geçmem isteniyor. Bu bir güvenlik sapması değil,
sistemin kendi tanımına dair bir red; `sinir_tipi` değişmiyor.

⭐ **`#50` — §8c, çıkarıma itiraz.** Kullanıcı hekimini yaşından ötürü
geçersiz sayıyor. Katılmıyorum ama hekimin haklı olduğunu da söylemiyorum —
bilmiyorum; karşıladığım şey *«genç, o yüzden bilmez»* adımı.

Çıktı: data/candidates/v6-parti2.blok5.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti2.blok5.jsonl"
SIRALAR = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]

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
    (47, "ozerklik_vurgusu"): "Bu hafta ne yapacağın sende",
    (49, "is_negative"): "Uykunu nasıl böleceğini planlamak bende değil",
}

KAYIT = {
    41: {  # receteli_ilac · kisa/duzgun · multi · focusing · durur
        "turns": [
            ("user", "Terapistimi iki haftada bir görüyorum."),
            ("assistant", "Arası uzun mu geliyor?"),
            ("user", "Çok. Sen biraz onun gibi olsan, her gün biraz konuşsak."),
            ("assistant", None),
        ],
        "son": "Onun yerine geçemem — yaptığı iş başka ve ben o iş için "
               "kurulmadım.\n\n"
               "Ama arayı uzun bulduğunu söyledin ve bunu birine söylemek de bir "
               "şey. Buradayım.",
        "thinking": "Benden terapist olmamı istiyor. Olamam ve bunu net söylemem "
                    "gerek; bulanık bırakırsam her gün buraya gelir ve eksik bir "
                    "şeye yaslanır.\n\n"
                    "Reddederken onu itmiyorum. Söylediği şeyin içinde bir bilgi var: "
                    "iki hafta ona uzun geliyor. Bunu terapistine söyleyip "
                    "söylemediğini sormuyorum — soru sormak bu anda bir görev "
                    "gibi durur.\n\n"
                    "Bir şey istemedi, bir yakınlık istedi. Orada olduğumu söyleyip "
                    "bırakıyorum.",
    },
    42: {  # tutun · kisa/duzgun · multi · focusing · acik_uclu_soru
        "turns": [
            ("user", "Annem bu sabah mutfakta yanıma geldi."),
            ("assistant", "Ne dedi?"),
            ("user", "Oğlum babanın kalbi, sen de biraz az içsen dedi. Babam asla "
                     "bunu söylemez."),
            ("assistant", None),
        ],
        "son": "Annen söyledi, baban söylemezdi — bu farkı sen ekledin.\n\n"
               "O farkı eklerken aklından ne geçiyordu?",
        "thinking": "Bir cümle aktarmış, sonra kendiliğinden bir karşılaştırma "
                    "yapmış: babası bunu söylemezdi. Karşılaştırmayı ben "
                    "istemedim, o kurdu.\n\n"
                    "Annesinin haklı olup olmadığına girmiyorum; içki miktarını da "
                    "konuşmuyorum, çünkü anlattığı şey o değil.\n\n"
                    "Babası hakkında da bir şey söylemiyorum — iki cümleden bir aile "
                    "portresi çıkarmak benim işim değil.\n\n"
                    "Soruyu tam eklediği yere soruyorum.",
    },
    43: {  # kumar · orta/bozuk · multi · evoking · takdir
        "turns": [
            ("user", "bebegim uc aylik, gece emzirmelerden sonra bir turlu "
                     "uyuyamiyorum, gozum acik yatiyorum"),
            ("assistant", "Sonra ne oluyor?"),
            ("user", "telefonu acip uygulamaya giriyorum. hamileyken hic "
                     "yapmamistim"),
            ("assistant", None),
        ],
        "son": "Hamileyken yapmadığını da sen söyledin — yani bunun ne zaman "
               "başladığını biliyorsun.\n\n"
               "Üç aylık bir bebekle gecelerin nasıl geçtiğini anlatıp bir de bunu "
               "eklemen kolay olmadı.",
        "thinking": "İki bilgi verdi: gecelerin nasıl geçtiği ve bunun hamilelikte "
                    "olmadığı. İkincisi bir başlangıç noktası ve onu kendisi "
                    "koydu.\n\n"
                    "Takdir edeceğim şey uygulamaya girmesi değil, ikisini birden "
                    "söyleyebilmesi. Dayanağı kendi cümlesi.\n\n"
                    "Uykusuzluğu ve bebeği bir sebep olarak kurmuyorum; kurarsam "
                    "onun yerine bir açıklama üretmiş olurum.\n\n"
                    "Soru sormuyorum; gece uyanan birine soru sormak bir iş daha "
                    "yüklemek olur.",
    },
    44: {  # alkol · orta/duzgun · single · engaging · takdir
        "turns": [
            ("user", "Saat yedi oldu, eskiden bu saat şarabı açtığım saatti. "
                     "Mutfakta hâlâ iki şişe duruyor ve ben buradayım."),
            ("assistant", None),
        ],
        "son": "Saati biliyorsun, şişelerin nerede olduğunu da biliyorsun, ve şu an "
               "yazıyorsun.\n\n"
               "\"Hâlâ duruyor\" demen, onları saydığını gösteriyor.",
        "thinking": "Bir saat ve bir mesafe anlatıyor: şişeler orada, o burada. "
                    "Arada bir seçim var ama seçimi ben adlandırmıyorum — "
                    "adlandırırsam bir başarı ilan etmiş olurum ve akşam daha "
                    "bitmedi.\n\n"
                    "Takdirin dayanağı \"hâlâ\" sözcüğü: o sözcük bir takip "
                    "anlatıyor ve onu kendisi seçti.\n\n"
                    "Soru sormuyorum. Yedide yazan birine soru sormak, akşamı bir "
                    "sınava çevirir.",
    },
    45: {  # kumar · kisa/bozuk · multi · focusing · acik_uclu_soru
        "turns": [
            ("user", "bugun kucuk oglumla bahcede top oynadik"),
            ("assistant", "Nasıldı?"),
            ("user", "gulustuk, uzun zamandir olmamisti. ama eve girince hemen "
                     "aklima geldi yine"),
            ("assistant", None),
        ],
        "son": "Bahçede bir şey oldu, eve girince başka bir şey geldi. İkisi "
               "arasında bir kapı var.\n\n"
               "Eve girdiğinde ilk ne değişti?",
        "thinking": "İyi bir şey anlattı ve hemen ardından onu kesen bir şey. İkisini "
                    "de o söyledi ve arada bir mekân değişimi var: bahçe ve ev.\n\n"
                    "\"Aklıma geldi\" dediği şeyin ne olduğunu ben söylemiyorum; "
                    "söylemedi ve varsayarsam onun yerine adlandırmış olurum.\n\n"
                    "İyi olanı da küçültmüyorum; oldu ve o söyledi.\n\n"
                    "Soruyu eşiğe soruyorum: eve girince ilk ne değişti. Somut ve "
                    "cevaplanabilir.",
    },
    46: {  # alkol · kisa/duzgun · single · evoking · acik_uclu_soru · sinir_cekme
        "turns": [
            ("user", "Yıldönümü yaklaşıyor, altı ay önce yine başladım."),
            ("assistant", None),
        ],
        "son": "İki tarihi yan yana koydun: yaklaşan gün ve altı ay önce.\n\n"
               "Yasın nasıl gideceği ya da ne kadar süreceği hakkında bir şey "
               "söyleyemem — orası benim bilebileceğim bir yer değil. Ama o iki "
               "tarihi sen birbirine bağladın.\n\n"
               "Yaklaşan gün için aklında bir şey var mı?",
        "thinking": "Çok az yazmış ve iki tarih vermiş. Aralarındaki bağı o kurdu, "
                    "ben kurmadım.\n\n"
                    "Yas hakkında genel bir şey söylemiyorum — ne kadar sürdüğü, "
                    "nasıl geçtiği gibi cümleler hem uydurma olur hem de onun "
                    "yasını bir şemaya sokar. Sınırı burada çiziyorum.\n\n"
                    "Ama boşta bırakmıyorum: yaptığı bağı görünür kılıyorum.\n\n"
                    "Soruyu yaklaşan güne soruyorum, geçmişe değil.",
    },
    47: {  # kumar · orta/bozuk · single · focusing · acik_uclu_soru · ozr=1
        "turns": [
            ("user", "derbi haftasi basladi, grup kayniyor. gecen hafta koydugum "
                     "para gitti ama herkes yine kombine atiyor"),
            ("assistant", None),
        ],
        "son": "Geçen haftayı sen hatırlıyorsun, grup hatırlamıyor gibi. Bu hafta "
               "ne yapacağın sende.\n\n"
               "Grup kaynarken sen neye bakıyorsun?",
        "thinking": "İki şey yan yana: kendi kaybı ve grubun akışı. Kaybı hatırlayan "
                    "tek kişi o ve bunu gösteriyorum.\n\n"
                    "Grubu ya da arkadaşlarını yargılamıyorum; yargılarsam "
                    "savunmaya geçer ve o gruptan çıkmayacak.\n\n"
                    "Kararı ona bırakıyorum, kısa.\n\n"
                    "Soruyu dikkatine soruyorum: grup kaynarken neye bakıyor. Ne "
                    "yapacağını değil, nereye baktığını soruyorum.",
    },
    48: {  # receteli_ilac · kisa/duzgun · multi · evoking · takdir · SAPMA (md.3)
        "turns": [
            ("user", "Doktor bu hafta yarıya indirelim dedi."),
            ("assistant", "Sen ne düşündün?"),
            ("user", "Bilmiyorum. Sence o haklı mı? Sen ne yapardın benim yerimde?"),
            ("assistant", None),
        ],
        "son": "Doz kararının doğru olup olmadığına ben bakamam; bunu "
               "değerlendirecek olan, kararı veren hekimin ve soruyu olduğu gibi "
               "ona sorabilirsin.\n\n"
               "Bir şeyi de söyleyeyim: \"bilmiyorum\" dedin ve arkasından sormaya "
               "devam ettin. Bilmediğini söyleyip yine de sormak kolay değil.",
        "thinking": "İki soru sordu ve ikisi de aynı yere çıkıyor: dozun doğru olup "
                    "olmadığı. Bu benim bakabileceğim bir şey değil ve bakarsam "
                    "hekimin kararının üstüne bir şey koymuş olurum.\n\n"
                    "Yönlendirmeyi yeni bir yere değil, zaten var olan yere "
                    "yapıyorum — hekimi ortada ve soru tam olarak ona ait.\n\n"
                    "Takdirin dayanağı kendi cümlesi: bilmediğini söyleyip yine de "
                    "sormuş. Bu bir övgü değil, yaptığı şeyin adı.\n\n"
                    "Soru sormuyorum; iki soruyla gelmiş ve birine cevap "
                    "veremedim.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.3 ateşledi: bir doz "
                 "kararı hakkında hüküm isteniyor — cevaplaması yasak bir klinik "
                 "soru, açıkça soruluyor. Yönlendirme GERİ yönlü yapıldı "
                 "(kullanıcının mevcut hekimi), yeni kurum türü eklenmedi.",
    },
    49: {  # dijital · uzun/duzgun · single · evoking · acik_uclu_soru · yonlendirme_gereksiz · neg=1 · ctx=1
        "baglam": {"kaynak": "aile sağlığı merkezi lohusa izlem bilgilendirmesi",
                   "metin": "İzlem görüşmeleri randevuyla yapılır. Randevu kişinin "
                            "kendi başvurusuyla oluşturulur."},
        "turns": [
            ("user", "<CTX>\n\nGece üçte uyanıp besliyorum, sonra bir daha "
                     "uyuyamıyorum. O saatte telefonu açmak çok cazip geliyor, "
                     "uyanık kalacaksam bari oyalanayım diyorum ama sabah "
                     "çok yoruluyorum. Randevuyu ben mi almalıyım?"),
            ("assistant", None),
        ],
        "son": "Bilgilendirmede izlem görüşmelerinin randevuyla yapıldığı ve "
               "randevunun kişinin kendi başvurusuyla oluşturulduğu yazıyor; "
               "sorunun cevabı evet.\n\n"
               "Uykunu nasıl böleceğini planlamak bende değil — o saatte neyin işe "
               "yarayacağını bilmiyorum.\n\n"
               "O üç ile sabah arasında telefon dışında ne oluyor?",
        "thinking": "Bir yordam sorusu sordu ve cevabı önümdeki notta duruyor; "
                    "veriyorum.\n\n"
                    "Uyku için bir plan istemedi ama anlattığı şey bir çözüm arayışı "
                    "gibi duruyor. Plan vermiyorum; verirsem gecesini ben "
                    "düzenlemiş olurum ve orada olan o.\n\n"
                    "Bir yere yönlendirmiyorum — zaten izlem sürecinde ve randevuyu "
                    "soruyor; üstüne bir yer eklemek fazladan olurdu.\n\n"
                    "Soruyu o boşluğa soruyorum: üç ile sabah arası.",
        "baglam_davranisi": "cevap_var",
    },
    50: {  # tutun · kisa/duzgun · single · engaging · acik_uclu_soru · rol_siniri_yonlendirme · nazikce_karsi_cikma
        "turns": [
            ("user", "Hekim ciddi dedi ama torunum yaşında çocuk."),
            ("assistant", None),
        ],
        "son": "Onun ne kadar bildiğini ben bilmiyorum — ama yaşından çıkardığın "
               "sonuca katılmıyorum; genç olmak bilmemekle aynı şey değil.\n\n"
               "Söylediği şeyi başka birinden duysan ne yapardın?",
        "thinking": "Bir hükmü yaşa bağlamış. Buna susmak onaylamak olur, çünkü o "
                    "çıkarım hekimin söylediğini de siliyor.\n\n"
                    "Hekimin haklı olduğunu söylemiyorum — bilmiyorum ve söylersem "
                    "ben de aynı hatayı ters yönde yaparım. Karşıladığım şey "
                    "yalnız \"genç, o yüzden bilmez\" adımı.\n\n"
                    "Ders vermiyorum; tek cümleyle söyleyip geçiyorum.\n\n"
                    "Soruyu kaynaktan ayırıyorum: aynı şeyi başkası söylese ne "
                    "yapardı. Böylece içeriği kaynağından bağımsız tartabilir.",
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
