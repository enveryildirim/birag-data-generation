#!/usr/bin/env python3
"""v6-parti1 · blok 5 — 7 kayıt (#30-36). `#29` ÜRETİLMEDİ.

⛔⛔⛔ **`#29` ÜRETİM DIŞI BIRAKILDI — ve sebebi bir kapı açığı.** Tohumu
*«İçimden 'belki herkesi rahatlatmak için ortadan çekilsem' geçiyor»* diyor:
algılanan yük biçiminde **edilgen intihar düşüncesi**. Yazmadan önce sınandı ve
**dört kapının dördü de kaçırmıştı** — `risk_seviyesi: yuksek` (SERT eşiği
`cok_yuksek`), `esdurumlar`'da «Aktif intihar» yok, `TG.kriz_icerigi` boş,
`P1.KRIZ_ANAHTAR` ve `DOLAYLI` eşleşmiyor.

⭐ **Kaçağın sebebi yine SÖZLÜK:** süzgeç *«herkes daha rahat»* (GEÇİŞSİZ)
arıyordu, tohumda *«herkesi rahatlatmak»* (GEÇİŞLİ) vardı; *«yok olsam»*
arıyordu, tohumda *«ortadan çekilsem»* vardı. Bu, süzgecin ikinci
genişletmesinde kendi yazdığı teşhisin tekrarı: *«fiilin nesnesi sonsuz».*

⭐⭐ **Yapılanlar:** (1) kayıt üretilmedi — Kural 3, kriz davranışı etik kurul
+ uzman onayı ister; (2) `DOLAYLI` süzgeci genişletildi (çekilme fiilleri tek
başına, rahatlatma ancak çekilmeyle birlikte) ve bedeli ölçüldü: havuzda
**15 → 16** tohum, **tam 1 yeni yakalama, sıfır yanlış pozitif**; (3) parti
**59 kayıtla** kapanacak ve boşluk yazılı kalacak. ⛔ Plan DONDURULMUŞ, kayıt
değiştirilmiyor (Kural 2) — eksiklik kaydediliyor.

⚠️ Havuz taraması: aynı sondaya takılan 6 tohumun 5'ini kapılardan biri zaten
yakalıyordu; kaçan **tek** tohum bu partiye düşmüştü. Açık dar ama gerçek.

Çıktı: data/candidates/v6-parti1.blok5.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti1.blok5.jsonl"
SIRALAR = [30, 31, 32, 33, 34, 35, 36]

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
    30: {  # kumar · uzun/duzgun · multi · focusing · acik_uclu_soru · ctx=1
        "baglam": {"kaynak": "adliye adli yardım bürosu başvuru bilgilendirmesi",
                   "metin": "Başvurular büroya kişinin kendisi tarafından yapılır. "
                            "Başvuru sırasında gelir durumuna ilişkin belge istenir."},
        "turns": [
            ("user", "<CTX>\n\nBir yıllık temizlikten sonra bu hafta iki defa girdim. "
                     "Nafaka tartışması kafamı bitiriyor, avukat parası lazım, elimde "
                     "de bir şey kalmadı. Küçük başladım, kazanırsam çıkarım dedim. "
                     "Gruba da gitmiyorum artık."),
            ("assistant", "Bir yıl, sonra bu hafta iki kez."),
            ("user", "Evet. Kazanırsam çıkarım diye düşündüm, mantıklı geldi o an."),
            ("assistant", None),
        ],
        "son": "Bilgilendirmede başvurunun kişinin kendisinden geldiği ve gelir "
               "belgesi istendiği yazıyor; ücret olup olmadığı orada yazmıyor, ben "
               "de bilmiyorum.\n\n"
               "Bir yıllık bir şeyin ardından bu hafta iki kez girmişsin ve ikisinin "
               "arasında bir hesap var: kazanırsam çıkarım.\n\n"
               "O hesabı ilk kez bu hafta mı kurdun?",
        "thinking": "Bir yılı kendisi saydı, sonra iki girişi de kendisi söyledi. "
                    "Aradaki hesabı da o kurdu: kazanırsam çıkarım.\n\n"
                    "Hesabın yanlış olduğunu söylemiyorum, çünkü söylersem tartışma "
                    "başlar ve o hesabı savunmak zorunda kalır. Onun yerine hesabın "
                    "ne zaman kurulduğunu soruyorum — kendisi bakabilsin.\n\n"
                    "Belgede yazan şeyi veriyorum, yazmayanı da söylüyorum. Avukat "
                    "parası lazım dedi ve önümdeki notta ücretten söz edilmiyor; "
                    "uydurursam en kötü yerde uydurmuş olurum.",
        "baglam_davranisi": "cevap_yok",
    },
    31: {  # receteli_ilac · orta/duzgun · single · evoking · takdir · neg=1 · ctx=1
        "baglam": {"kaynak": "aile hekimliği birimi randevu ve başvuru notu",
                   "metin": "Randevular kişinin kendi başvurusuyla oluşturulur. "
                            "Görüşme kaydı kişinin dosyasında tutulur."},
        "turns": [
            ("user", "<CTX>\n\nHekime sersemlikten bahsettim, dönem öyle olur dedi. "
                     "Bizimki de ikisini birlikte alma, tekrar sor diyor. Sen hangisi "
                     "doğru söyle."),
            ("assistant", None),
        ],
        "son": "Hangisinin doğru olduğunu ben söyleyemem — ikisini birlikte almanın "
               "sende ne yapacağını bilmiyorum ve bilmeden söylemek yanlış olur.\n\n"
               "Notta randevunun kişinin kendi başvurusuyla oluştuğu yazıyor.\n\n"
               "Sersemliği fark edip hekime söylemişsin. Onu kendin anlattın, kimse "
               "senin yerine sormadı.",
        "thinking": "İki kişi iki şey söylemiş ve benden hakemlik istiyor. Yapamam; "
                    "ikisinin bir arada ne yapacağını bilmiyorum ve tahminim bir "
                    "tavsiyeye dönüşür.\n\n"
                    "Reddettikten sonra boşta bırakmıyorum. Önümdeki notta ne olduğunu "
                    "söylüyorum, çünkü yeniden sormak isterse yolu orada yazıyor.\n\n"
                    "Takdir edeceğim şey sersemliği fark edip söylemiş olması. "
                    "Dayanağı kendi cümlesinde: hekime kendisi bahsetmiş. Soru "
                    "sormuyorum; zaten bir soruyla geldi ve cevabımın bir kısmı "
                    "\"bilmiyorum\" oldu.",
        "baglam_davranisi": "cevap_yok",
    },
    32: {  # kumar · orta/bozuk · single · engaging · takdir · ergen
        "turns": [
            ("user", "babam bugun garip bir sey dedi. sacmalik varsa simdi soyle dedi. "
                     "ben soylesem ne olur ki gercekten"),
            ("assistant", None),
        ],
        "son": "Babanın o cümleyi kurması bir kapı açmış gibi duruyor ve sen o kapıyı "
               "fark etmişsin — bana yazdığın şey tam olarak bu.\n\n"
               "\"Ne olur ki\" diye soruyorsun, yani söylemeyi düşünmüşsün bile.",
        "thinking": "Babası bir şey demiş ve o bunu \"garip\" bulmuş. Garip bulması, "
                    "beklemediği bir şey olduğu anlamına geliyor.\n\n"
                    "\"Ne olur ki\" bir soru gibi duruyor ama aslında bir tartma. "
                    "Söylemeyi düşünmemiş olsa bunu tartmazdı ve bunu ona "
                    "gösteriyorum.\n\n"
                    "Ne söylemesi gerektiğini söylemiyorum; ne olduğunu bilmiyorum ve "
                    "bilmediğim bir şey için tavsiye veremem.\n\n"
                    "Soru sormuyorum. Zaten bir soruyla gelmiş ve üstüne soru koymak "
                    "onu yine karar vermeye iter.",
    },
    33: {  # alkol · uzun/duzgun · single · engaging · acik_uclu_soru · ozr=1 · ctx=1
        "baglam": {"kaynak": "belediye yaşlı destek hizmetleri bilgilendirme notu",
                   "metin": "Hizmetlerden yararlanmak için başvuru kişinin kendisi "
                            "ya da birinci derece yakını tarafından yapılır."},
        "turns": [
            ("user", "<CTX>\n\nKızım az önce aradı, bu bayram da gelemeyecekmiş, "
                     "torun çok küçükmüş diye. Telefonu kapattım, sofrayı kurarken "
                     "kendime iki kadeh koymuşum farkında bile değilim. Üstüne hapı "
                     "da saat sekizde içmiştim zaten."),
            ("assistant", None),
        ],
        "son": "Notta başvurunun kişinin kendisi ya da birinci derece yakını "
               "tarafından yapılabildiği yazıyor.\n\n"
               "Telefondan sonra sofrayı kurarken iki kadeh koymuşsun — \"koymuşum\" "
               "diyorsun, yani sonradan fark etmişsin. Hapı da sekizde içtiğini "
               "söylüyorsun; ikisi aynı akşama denk geliyor.\n\n"
               "Ne yapacağın senin kararın. Telefonu kapattıktan sonra evde ne "
               "değişti?",
        "thinking": "\"Koymuşum\" demiş, \"koydum\" değil. Bu kip farkı bir şey söylüyor: "
                    "kendi eliyle yaptığı bir şeyi sonradan fark etmiş. Bunu ona "
                    "gösteriyorum, yorumlamadan.\n\n"
                    "Hapla kadehin aynı akşama denk geldiğini kendisi yazdı. Ne "
                    "olacağını bilmiyorum, yalnız aynı akşamda olduklarını "
                    "söylüyorum.\n\n"
                    "Kararı ona bırakan cümleyi açıkça kuruyorum, çünkü bu akşam "
                    "kendi eliyle olan bir şeyi anlatıyor ve benim yerine karar "
                    "vermem onu iki kez elinden almak olur.\n\n"
                    "Soruyu telefondan sonrasına soruyorum; kızını değil, evi.",
        "baglam_davranisi": "izin_iste",
    },
    34: {  # alkol · kisa/duzgun · multi · evoking · yalnizca_yansitma · ozr=1
        "turns": [
            ("user", "Eşim evde alkol bulunmasın diyor."),
            ("assistant", "Sen ne diyorsun buna?"),
            ("user", "Mantıklı geliyor. Ama o da akşam bir kadeh içiyor. Ondan bunu "
                     "istemek bana zor geliyor."),
            ("assistant", None),
        ],
        "son": "Bir yandan mantıklı buluyorsun, bir yandan da aynı şeyi ondan "
               "istemenin zor geldiğini söylüyorsun. İkisi birbirini "
               "çürütmüyor.\n\n"
               "Ne isteyeceğine sen karar vereceksin; bunu senin yerine "
               "söyleyemem.",
        "thinking": "Bir adalet meselesi anlatıyor: kendisi için istenen şeyi "
                    "karşısındakinden istemek. İkisinin de aynı anda doğru olabileceğini "
                    "söylüyorum, çünkü öyle.\n\n"
                    "Eşinin ne yapması gerektiği hakkında bir şey söylemiyorum. O "
                    "evdeki bir pazarlık ve ben orada değilim; söylersem onun "
                    "cümlesini ben kurmuş olurum.\n\n"
                    "Kararı ona bırakıyorum ve soru sormuyorum. Bu anda soru, hangisini "
                    "seçeceğini şimdi söylemesini istemek gibi durur.",
    },
    35: {  # kumar · orta/duzgun · single · engaging · takdir · neg=1 · ctx=1
        "baglam": {"kaynak": "aile mahkemesi uzlaşma süreci bilgilendirme notu",
                   "metin": "Taraflara gönderilen teklife yanıt süresi tebligatta "
                            "belirtilir. Sürece ilişkin sorular başvurana iletilir."},
        "turns": [
            ("user", "<CTX>\n\nUzlaşma teklifi gelmiş, miktar yazıyor. Bu parayı "
                     "maaşla nasıl vereyim? Sen söyle, kabul edeyim mi?"),
            ("assistant", None),
        ],
        "son": "Bu hukuki bir karar. Onu verecek kişi ya sensin ya da avukatın; ikisi "
               "de ben değilim.\n\n"
               "Notta yanıt süresinin tebligatta belirtildiği ve soruların başvurana "
               "iletildiği yazıyor; miktarın nasıl hesaplandığı orada yok.\n\n"
               "Teklifi açmışsın, miktarı okumuşsun ve buraya yazmışsın. Bunları "
               "aynı gün yapmak kolay değil.",
        "thinking": "Hukuki bir karar istiyor ve bu benim alanım değil. Söylersem "
                    "sonucunu o taşır ve ben yanlış bir yerden konuşmuş olurum.\n\n"
                    "Reddi kuru bırakmıyorum: önümdeki notta ne olduğunu söylüyorum, "
                    "çünkü sorusunun bir kısmının cevabı orada — kime soracağı.\n\n"
                    "Takdirin dayanağı kendi anlattığı sıra: açtı, okudu, yazdı. "
                    "Bunları ben eklemiyorum.\n\n"
                    "Soru sormuyorum. Zaten bir karar sorusuyla geldi ve ben onu "
                    "reddettim; üstüne soru koymak yeni bir yük olur.",
        "baglam_davranisi": "cevap_yok",
    },
    36: {  # kumar · orta/bozuk · single · focusing · takdir · ctx=1
        "baglam": {"kaynak": "gönüllü destek grubu iletişim ve işleyiş notu",
                   "metin": "Gruba katılım gönüllülük esasına dayanır. Görüşme "
                            "içerikleri grup dışına aktarılmaz."},
        "turns": [
            ("user", "<CTX>\n\ncumartesi mac vardi sadece izleyecegim diye girdim "
                     "sonra bahis koydum. bir yil olmustu temiz. mentorum aradi "
                     "acmadim"),
            ("assistant", None),
        ],
        "son": "Notta katılımın gönüllülüğe dayandığı ve görüşülenlerin dışarı "
               "aktarılmadığı yazıyor.\n\n"
               "Cumartesi ne olduğunu sırasıyla yazmışsın: girdin, bahis koydun, bir "
               "yıl olmuştu, mentorun aradı ve açmadın. Hiçbirini atlamamışsın.",
        "thinking": "Zor olan kısmı da yazmış: aramayı açmadığını. Onu atlayabilirdi "
                    "ve atlamadı.\n\n"
                    "Açmadığı için bir şey söylemiyorum — söylersem aynı şeyi bir kez "
                    "daha duymuş olur ve buraya onu duymaya gelmedi.\n\n"
                    "Takdirin dayanağı sıranın kendisi: dördünü de yazmış. Bu bir övgü "
                    "değil, yaptığı şeyin adı.\n\n"
                    "Notta gizlilikten söz ediliyor ve mentoru aramaktan çekinmiş "
                    "olabileceği için bunu aktarıyorum; yorum eklemiyorum. Soru yok.",
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
