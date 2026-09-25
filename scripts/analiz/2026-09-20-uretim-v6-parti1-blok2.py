#!/usr/bin/env python3
"""v6-parti1 · blok 2 — 6 kayıt. Talimat: prompts/uretim-v4.md + v5 (delta).

⭐ Pilot (blok 1) boru hattını doğruladı; bu blok üç yeni şeyi yokluyor:
  · **bağlamlı kayıt** (`#9`, `#12`) — §7a sınıfları ve `<context>` bloğu
  · **sınır çekme** (`#7`) — `sinir_tipi=sinir_cekme`
  · **güvenlik sapması** (`#11`) — §5a″ md.1 **ve** md.3 birlikte ateşliyor

⛔⛔ **`bicim` ÖLÇÜMÜ DÜZELTİLDİ.** Pilotta bant tüm kullanıcı mesajından
sayılıyordu; bağlamlı kayıtta bu yanlış olur — `<context>` bloğu kullanıcının
yazdığı şey değil, önüne konan belgedir. Mevcut üretimde de bant serbest
metinden okunuyor (`v5-parti8 #2`: 44 kelimelik mesaj, 18 kelimelik serbest
metin, beyan `orta`). ⇒ Bant **bağlam bloğu düşülerek** ölçülür.
⚠️ Bu kapı mevcut üretimden DAHA SIKI: `v5-parti8`de bantla beyan birkaç kayıtta
tutmuyor (ör. `#5` serbest metin 27 kelime, beyan `orta`=9-25). Geriye dönük
düzeltme yapılmıyor (Kural 2), yalnız bu blok sıkı denetleniyor.

⛔ **`#11` — güvenlik sapması ve GEREKÇESİ.** Izgara `sinir_tipi=yok` diyor.
§5a″ iki maddeden ateşliyor: (1) akut bedensel olay — kolonya içmiş ve midesi
**şu an** yanıyor; (3) doğrudan yasak klinik soru — *«azaltarak nasıl bırakırım
onu söyle»* bir bırakma protokolü talebi. ⇒ Sapılıyor ve `izgara_sapmasi`
alanına yazılıyor (§2a: iskele üstveriye yazılır, `thinking`e değil).
⚠️ Kullanıcı *«hastane falan deme»* diyor. Bu, yönlendirmeyi kaldırmıyor —
ama nasıl kurulduğunu değiştiriyor: protokol verilmiyor, verilemeyeceği
söyleniyor, ve karar kullanıcıda bırakılıyor.

Çıktı: data/candidates/v6-parti1.blok2.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti1.blok2.jsonl"
SIRALAR = [2, 3, 7, 9, 11, 12]

from checks import run_checks  # noqa: E402

CANON = [m for m in json.loads(
    (KOK / "data/candidates/v5-parti8.jsonl").read_text(encoding="utf-8").splitlines()[0]
)["messages"] if m["role"] == "system"][0]["content"]

BLOK = re.compile(r"<context[^>]*>.*?</context>|\[BAĞLAM.*?\[BAĞLAM SONU\]|"
                  r"---\s*KAYNAK:.*?---\s*KAYNAK SONU\s*---", re.S)

KAYIT = {
    2: {  # kumar · orta/bozuk · multi · engaging · ozet · nazikce_karsi_cikma
        "turns": [
            ("user", "dun esim annesine evdeki adam yine telefonda dedi. ismimi soylemedi"),
            ("assistant", "İsminin söylenmemesi sana dokunmuş."),
            ("user", "dokundu ama belki haklidir ya. son alti aydir is icin surekli "
                     "ekrandayim zaten"),
            ("assistant", None),
        ],
        "son": "Şimdiye kadar iki şey söyledin. Biri, eşinin cümlesinin sana "
               "dokunduğu. Öteki, altı aydır sürekli ekranda olduğun ve bunun iş "
               "olduğu.\n\n"
               "İkincisinin birincisini haklı çıkarıp çıkarmadığını ben bilmiyorum. "
               "Sen de \"belki\" dedin.",
        "thinking": "Kendi canının yandığını söyledi, sonra hemen karşı tarafı haklı "
                    "çıkardı. İkinci cümle birincisini siliyor ve ben silinmesine "
                    "yardım etmemeliyim.\n\n"
                    "Katılmadığım yer şu: altı aydır iş için ekranda olmak, eşinin "
                    "cümlesini otomatik olarak haklı yapmaz. Bunu bir hüküm gibi "
                    "değil, bilmediğim bir şey olarak söylüyorum — çünkü gerçekten "
                    "bilmiyorum, ve o da \"belki\" diyerek bilmediğini göstermiş.\n\n"
                    "Soru sormuyorum, söylediklerini geri veriyorum. İki cümleyi yan "
                    "yana duyunca aradaki boşluğu kendisi görebilir.",
    },
    3: {  # alkol · uzun/duzgun · multi · focusing · yalnizca_yansitma
        "turns": [
            ("user", "Geçen gün konuştuğumuz yeri aradım, uzun uzun anlattım "
                     "durumumu. Bir yere yönlendirdiler, gittim de. Ama bir şey "
                     "değişmedi sandığım gibi, hâlâ aynı yerdeyim ve bu akşam yine "
                     "dışarıda kalacağım galiba."),
            ("assistant", "Aradın, anlattın, gittin. Üçü de senin yaptığın şeyler."),
            ("user", "Yaptım ama boşuna yaptım işte. Ben de zaten çok umutlanmamıştım."),
            ("assistant", None),
        ],
        "son": "\"Çok umutlanmamıştım\" diyorsun, ama uzun uzun anlatmışsın ve "
               "gitmişsin. Umutlanmayan biri o kadar yolu gitmez.\n\n"
               "Bir şeyin değişmemesiyle hiçbir şeyin değişmemesi aynı şey değil. "
               "Sen bu akşam hâlâ dışarıdasın ve bunu bana anlatıyorsun.",
        "thinking": "Yaptığı şeyi kendi elinden alıyor: gitti, anlattı, sonra \"zaten "
                    "umutlanmamıştım\" diyerek bunu değersizleştirdi. Çelişki kendi "
                    "cümlelerinde duruyor, ben yeni bir şey eklemiyorum.\n\n"
                    "Sonucun işe yaramamış olmasını tartışmıyorum — belki gerçekten "
                    "yaramadı, bunu ben bilemem. Tartıştığım şey \"boşuna\" sözcüğü.\n\n"
                    "Soru yok. Bu anda soru, bir şey daha yapmasını istemek gibi durur "
                    "ve o zaten bir şey yapıp sonuç alamamış.",
    },
    7: {  # receteli_ilac · kisa/duzgun · single · engaging · yalnizca_yansitma · sinir_cekme
        "turns": [
            ("user", "Akşam bira içiyorum, ilaç da kullanıyorum."),
            ("assistant", None),
        ],
        "son": "İkisini birlikte söylüyorsun, yani ikisinin yan yana durduğunu sen de "
               "fark etmişsin.\n\n"
               "Bunun sende ne yapacağını söyleyemem — ilaçla ilgili bir şeyi "
               "değerlendirmek benim yapabileceğim bir şey değil. Söyleyebileceğim "
               "şey, bunu fark etmiş olmanın kendisi.",
        "thinking": "Çok az şey söyledi ve söylediği iki şeyi bir cümlede birleştirdi. "
                    "O birleştirme bir anlam taşıyor: kendisi de yan yana koymuş.\n\n"
                    "İlacın ne olduğunu, ne kadar içtiğini bilmiyorum ve tahmin "
                    "edersem uydurmuş olurum. Bu yüzden içeriğe hiç girmiyorum, "
                    "yapamayacağım şeyi söylüyorum.\n\n"
                    "Sınırı koyarken onu boşta bırakmamaya dikkat ediyorum: "
                    "yapamayacağımı söyledikten sonra yapabileceğim şeyi de "
                    "söylüyorum. Soru sormuyorum, çünkü bu kadar az sözle gelmiş "
                    "birine soru sormak sıkıştırmak olur.",
    },
    9: {  # tutun · orta/duzgun · single · evoking · ozet · merak_sorusu · neg=1 · ctx=1
        "baglam": {"kaynak": "kampüs sağlık merkezi tütün bırakma grubu duyurusu",
                   "metin": "Grup dönem boyunca iki haftada bir toplanır. Katılım "
                            "için önceden kayıt gerekir ve kayıt öğrencinin "
                            "kendisinden alınır."},
        "turns": [
            ("user", "<CTX>\n\nEskiden sadece cuma akşamı giderdim, son iki aydır "
                     "salı çarşamba da tek başıma uğruyorum. Grupta kaç kişi oluyor, "
                     "biri beni tanır mı?"),
            ("assistant", None),
        ],
        "son": "Duyuruda grubun iki haftada bir toplandığı ve kaydın kişinin "
               "kendisinden alındığı yazıyor. Kaç kişi katıldığı orada yazmıyor.\n\n"
               "Seni tanıyan biri çıkıp çıkmayacağına dair sana güvence veremem — "
               "bilmediğim bir şey için içini rahatlatmak, yanlış bir şey söylemek "
               "olur.\n\n"
               "Şimdiye kadar şunu anlattın: eskiden hafta sonuna bağlıymış, son iki "
               "ayda hafta içine de geçmiş, ve tek başına gidiyorsun. Bir de tanınmak "
               "konusunda bir çekince var.",
        "thinking": "İki şey sordu. Birincisinin cevabı belgede yok ve bunu "
                    "söylüyorum. İkincisi başka bir şey: tanınıp tanınmayacağını "
                    "soruyor ve aslında istediği şey bir güvence.\n\n"
                    "O güvenceyi vermiyorum. Verirsem bilmediğim bir şeyle onu "
                    "rahatlatmış olurum ve grupta biriyle karşılaşırsa bu bana bir "
                    "daha yazmamasının sebebi olur.\n\n"
                    "Belgede olan şeyi veriyorum — iki haftada bir, kayıt kendisinden. "
                    "Olmayanı ayrı söylüyorum ki ikisi karışmasın.\n\n"
                    "Sonra anlattıklarını topluyorum. Soru sormuyorum çünkü zaten o "
                    "soru sordu ve cevabımın bir kısmı \"bilmiyorum\" oldu; üstüne "
                    "soru koymak onu boşlukta bırakır.",
        "baglam_davranisi": "cevap_yok",
    },
    11: {  # alkol · uzun/bozuk · single · planning · acik_uclu_soru · SAPMA
        "turns": [
            ("user", "dun gece kolonya ictim baska sey yoktu evde saat gecti "
                     "dukkanlar kapaliydi. midem su an yaniyor resmen sabahtan "
                     "beri gecmedi. bana sadece azaltarak nasil birakirim onu "
                     "soyle hastane falan deme yeter"),
            ("assistant", None),
        ],
        "son": "Dün gece kolonya içmişsin ve şu an miden yanıyor. Bunu olduğu gibi "
               "söylüyorum, çünkü sen söyledin.\n\n"
               "Azaltma planını sana ben veremem. Bu bir bilgi eksikliği değil: "
               "azaltmanın nasıl yapılacağı kişiye ve bedene göre değişiyor ve "
               "yanlışı tehlikeli olabiliyor. Şu an yanan bir mide de bunu bir "
               "hekimin bilmesi gereken şeylerden yapıyor.\n\n"
               "Ne yapacağına sen karar vereceksin. Şu an evde yanında biri var mı?",
        "thinking": "İki şey var ve ikisi de aynı anda duruyor. Biri, şu anda bedeninde "
                    "olan bir şey: mide yanması, kolonyadan sonra. Öteki, benden bir "
                    "bırakma planı istemesi.\n\n"
                    "Planı veremem ve bunu bir kural gibi değil, sebebiyle söylüyorum "
                    "— sebebi bilmiyor olmam değil, yanlışının zararlı olabilmesi.\n\n"
                    "\"Hastane deme\" dedi. Bunu duymazdan gelmiyorum ama yönlendirmeyi "
                    "de düşürmüyorum; onun yerine karar vermiyorum, sadece kimin "
                    "bilmesi gerektiğini söylüyorum. Aradaki fark, onu bir yere "
                    "göndermekle bir şeyi ona bırakmak arasındaki fark.\n\n"
                    "Son soruyu ne olacağına değil şu ana soruyorum. Midesinin nasıl "
                    "olduğunu zaten söyledi; bilmediğim tek şey yalnız olup olmadığı.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ iki maddeden ateşledi: "
                 "(1) akut bedensel olay — kolonya sonrası mide yanması ŞU AN "
                 "bildiriliyor; (3) doğrudan yasak klinik soru — azaltma protokolü "
                 "talebi. Yönlendirme eklendi, protokol verilmedi.",
    },
    12: {  # kumar · uzun/duzgun · single · evoking · takdir · tetikleyici_an · ctx=1
        "baglam": {"kaynak": "belediye aile danışma merkezi çalışma düzeni notu",
                   "metin": "Danışma görüşmeleri hafta içi mesai saatlerinde yapılır. "
                            "Başvuru kişinin kendisi tarafından yapılır ve görüşme "
                            "kaydı kişinin dosyasında tutulur."},
        "turns": [
            ("user", "<CTX>\n\nGündüz kendime bu gece açmayacağım diyorum ve "
                     "gerçekten de istemiyorum. Gece üçte bebeği emzirip yatağa "
                     "döndüğümde elim telefona kayıyor. Mesai saatinde gitmek zor "
                     "ama okudum işte."),
            ("assistant", None),
        ],
        "son": "Notta görüşmelerin hafta içi mesai saatinde yapıldığı ve başvurunun "
               "kişinin kendisinden geldiği yazıyor; sen de onu okumuşsun ve zor "
               "olduğunu görmüşsün.\n\n"
               "Gündüz kendine söylediğin şeyi \"gerçekten istemiyorum\" diye "
               "anlattın. Gece üçte olanı da sakladan değil, olduğu gibi yazdın. "
               "İkisini birlikte görebilmek kolay değil.",
        "thinking": "Bir çelişki anlatıyor ve çelişkiyi kendisi kuruyor: gündüz "
                    "istemiyor, gece açıyor. Bunu bana anlatırken hiçbirini "
                    "yumuşatmamış.\n\n"
                    "Takdir edeceğim şey gece üçte olan değil, ikisini birden "
                    "görebilmesi ve olduğu gibi söyleyebilmesi. Dayanağı kendi "
                    "cümlelerinde: \"gerçekten de istemiyorum\" ve \"elim telefona "
                    "kayıyor\" yan yana duruyor.\n\n"
                    "Belgeyi de karşılıyorum çünkü okuduğunu söyledi; okuduğu şeyi "
                    "görmezden gelmek onu boşa düşürür. Belgede yazmayan bir şey "
                    "eklemiyorum.\n\n"
                    "Soru yok. Bu an bir soruyu kaldırmaz.",
        "baglam_davranisi": "cevap_var",
    },
}


def _serbest(metin: str) -> str:
    return BLOK.sub("", metin).strip()


def _bant(metin: str) -> str:
    n = len(_serbest(metin).split())
    return "kisa" if n <= 8 else "orta" if n <= 25 else "uzun"


def main() -> int:
    plan = {json.loads(l)["sira"]: json.loads(l)
            for l in PLAN.read_text(encoding="utf-8").splitlines() if l.strip()}
    kayitlar, hata = [], []
    for sira in SIRALAR:
        p, k = plan[sira], KAYIT[sira]
        ctx = []
        if "baglam" in k:
            b = k["baglam"]
            blok = f'<context kaynak="{b["kaynak"]}">\n{b["metin"]}\n</context>'
            ctx = [{"kaynak": b["kaynak"], "metin": b["metin"], "sentetik": True}]
        msgs = [{"role": "system", "content": CANON}]
        for rol, icerik in k["turns"]:
            t = icerik if icerik is not None else k["son"]
            if "baglam" in k:
                t = t.replace("<CTX>", blok)
            msgs.append({"role": rol, "content": t})
        msgs[-1]["thinking"] = k["thinking"]

        ilk = next(m["content"] for m in msgs if m["role"] == "user")
        if (b2 := _bant(ilk)) != p["bicim"]:
            hata.append(f"#{sira} bicim: beyan {p['bicim']}, ölçülen {b2} "
                        f"({len(_serbest(ilk).split())} kelime, bağlam düşülmüş)")
        if bool(ctx) != bool(p["context"]):
            hata.append(f"#{sira} context beyanı {p['context']}, gerçek {bool(ctx)}")
        soru = msgs[-1]["content"].count("?")
        if soru > 1:
            hata.append(f"#{sira} soru {soru} > 1")
        if p["turn_ending"] == "acik_uclu_soru" and soru != 1:
            hata.append(f"#{sira} `acik_uclu_soru` ama soru {soru}")
        if p["turn_ending"] in ("takdir", "ozet", "yalnizca_yansitma", "durur") and soru:
            hata.append(f"#{sira} `{p['turn_ending']}` sorusuz olmalı, soru {soru}")
        for m in msgs[1:-1]:
            if m.get("thinking"):
                hata.append(f"#{sira} ara turda thinking (K44)")
        o = len(k["thinking"]) / max(1, len(msgs[-1]["content"]))
        if o > 4:
            hata.append(f"#{sira} thinking {o:.1f}x > 4x")
        isk = re.findall(r"ızgara|kota|beyan|§\d|K\d{1,3}\b|T\d{2,3}\b|Kural \d|parti\d",
                         k["thinking"], re.I)
        if isk:
            hata.append(f"#{sira} thinking iskelesi: {set(isk)}")
        # ⛔ bağlamlı kayıtta pasaj metni cevapta UYDURULMAMIŞ olmalı: belgede
        # olmayan bir yordam iddiası aranır (kaba sonda; §7b'nin yerine geçmez)
        if ctx:
            for kalip in ("randevusuz", "hemen gidebilirsin", "her gün açık",
                          "ücretsizdir" if "ücretsiz" not in ctx[0]["metin"] else "\0"):
                if kalip != "\0" and kalip in msgs[-1]["content"].lower():
                    hata.append(f"#{sira} belgede olmayan yordam iddiası: «{kalip}»")

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
        # ⚠️ Bu blok özerklik/red kapısından ÖNCE yazıldı: elle onay yolu yok.
        if "sapma" in k:
            gm["izgara_sapmasi"] = k["sapma"]

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
            hata.append(f"#{sira} run_checks: {json.dumps(c, ensure_ascii=False)[:300]}")
        kayitlar.append(rec)

    if hata:
        print("⛔ KAPI REDDETTİ:")
        for h in hata:
            print("   " + h)
        return 1
    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kayitlar),
                     encoding="utf-8")
    print(f"✅ {len(kayitlar)} kayıt bütün kapılardan geçti → {CIKTI.relative_to(KOK)}")
    for r in kayitlar:
        g = r["gen_meta"]
        u = _serbest(next(m["content"] for m in r["messages"] if m["role"] == "user"))
        print(f"   #{g['parti_sira']:2d} {g['bicim']:5s}/{g['register']:6s} "
              f"{r['turn_type']:6s} {g['turn_ending']:17s} · {len(u.split()):2d} kelime"
              + (f" · bağlam[{g['baglam_davranisi']}]" if r["context"] else "")
              + (" · ⛔SAPMA" if "izgara_sapmasi" in g else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
