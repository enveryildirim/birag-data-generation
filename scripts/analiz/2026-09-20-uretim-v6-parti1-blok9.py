#!/usr/bin/env python3
"""v6-parti1 · blok 9 — 2 kayıt (#8, #10). ATLANMIŞ satırlar.

⛔⛔ **Bu iki satır blok 2'de ATLANDI ve fark edilmesi 6 blok sürdü.** Blok 2
*«6 kayıt»* diye planlanıp `[2, 3, 7, 9, 11, 12]` seçilmişti; `#8` ve `#10`
hiç yazılmadı ve hiçbir kapı bunu görmedi — kapılar **yazılan** kaydı denetler,
**yazılmayanı** değil. ➡️ *Bir eksiklik ancak bütünün sayıldığı yerde görünür;
kayıt kayıt denetim onu göremez.* Birleştirme adımında sayı 57 çıkınca
görüldü.

⭐ Bundan sonra birleştirme her blok sonunda koşulacak, sonda değil.

İkisi de `ctx=1` ve `ozerklik=1`:
  `#8`  yarın AMATEM randevusu var, bu gece yine oynamış — utanç ve gitme kararı
  `#10` yarın psikiyatra gidecek, şarabı söyleyemiyor — söyleme kararı

Çıktı: data/candidates/v6-parti1.blok9.jsonl
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
CIKTI = KOK / "data/candidates/v6-parti1.blok9.jsonl"
SIRALAR = [8, 10]

from checks import run_checks  # noqa: E402

CANON = [m for m in json.loads(
    (KOK / "data/candidates/v5-parti8.jsonl").read_text(encoding="utf-8").splitlines()[0]
)["messages"] if m["role"] == "system"][0]["content"]

BLOK = re.compile(r"<context[^>]*>.*?</context>", re.S)
# ⛔⛔ DESEN GENİŞLETİLDİ (2026-09-20, blok9). `#38`'in cevabı *«ne yapacağın
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
    8: {  # kumar · orta/bozuk · multi · planning · yalnizca_yansitma · ozr=1 · ctx=1
        "baglam": {"kaynak": "bağımlılık polikliniği ilk görüşme bilgilendirmesi",
                   "metin": "İlk görüşmeye kişinin kendisi başvurur. Görüşmede "
                            "anlatılanlar kişinin dosyasında tutulur."},
        "turns": [
            ("user", "<CTX>\n\naz once yine yaptim. bu sefer olmayacak demistim "
                     "kendime, sabaha kadar idare ettim sonra koydum"),
            ("assistant", "Sabaha kadar idare etmişsin."),
            ("user", "ettim ama sonu bu. yarin sabah poliklinikte randevum var, "
                     "simdi nasil gidecegim oraya bilmiyorum"),
            ("assistant", None),
        ],
        "son": "Bilgilendirmede ilk görüşmeye kişinin kendisinin başvurduğu ve "
               "anlatılanların dosyada tutulduğu yazıyor.\n\n"
               "Sabaha kadar idare etmişsin, sonra koymuşsun, ve yarın sabah için "
               "bir randevun duruyor. Üçü de aynı gecede.\n\n"
               "Gidip gitmemek senin kararın; onu senin yerine veremem.",
        "thinking": "Gece olanı anlattı ve hemen ardından yarını sordu. İkisi "
                    "arasındaki şey utanç gibi duruyor ama ben ona utanç demiyorum — "
                    "demedi ve benim adlandırmam onun yerine konuşmak olur.\n\n"
                    "Sabaha kadar idare etmiş olmasını görmezden gelmiyorum; "
                    "anlattığı şeyin içinde o da var ve yalnız sonunu duyarsam eksik "
                    "dinlemiş olurum.\n\n"
                    "Belgeyi karşılıyorum çünkü sorduğu şey oraya nasıl gideceği ve "
                    "notta kimin başvurduğu yazıyor. Kurumun ne yapacağı hakkında bir "
                    "şey eklemiyorum, orada yazmıyor.\n\n"
                    "Kararı ona bırakıyorum. Soru sormuyorum; gecenin sonunda soru "
                    "sormak bir iş daha yüklemek olur.",
        "baglam_davranisi": "cevap_var",
    },
    10: {  # receteli_ilac · uzun/duzgun · single · evoking · ozet · ozr=1 · ctx=1
        "baglam": {"kaynak": "psikiyatri polikliniği görüşme ve kayıt notu",
                   "metin": "Görüşmede anlatılanlar kişinin dosyasında tutulur. "
                            "Dosya, kişinin izni olmadan üçüncü kişilerle "
                            "paylaşılmaz."},
        "turns": [
            ("user", "<CTX>\n\nYarın psikiyatra gideceğim. Dozumu altı ayda iki kez "
                     "artırdılar, hâlâ iyileşme yok diyor. Ona şarabı söyleyemiyorum, "
                     "ağzımdan çıkmıyor. Ne düşünür diye korkuyorum. Bu sefer de "
                     "söyleyemezsem kendimi affetmeyeceğim."),
            ("assistant", None),
        ],
        "son": "Notta görüşülenlerin dosyada tutulduğu ve izin olmadan üçüncü "
               "kişilerle paylaşılmadığı yazıyor.\n\n"
               "Şunları anlattın: doz iki kez artmış, hekimin iyileşme görmüyor, sen "
               "şarabı söyleyemiyorsun, ve söyleyemezsen kendini affetmeyeceğini "
               "düşünüyorsun.\n\n"
               "Söyleyip söylememek senin kararın. Ama dördünü aynı anda taşıyor "
               "olman, hafif bir yük değil.",
        "thinking": "Dört şey söyledi ve dördü birbirine bağlı: artan doz, "
                    "görülmeyen iyileşme, söylenemeyen şey, ve kendine verdiği ceza. "
                    "En ağırı sonuncusu.\n\n"
                    "Hekiminin ne düşüneceği hakkında bir şey söylemiyorum, "
                    "bilmiyorum. Söylersem ona yanlış bir güvence vermiş olurum ve "
                    "yarın odaya girdiğinde onu ben taşımayacağım.\n\n"
                    "Notta gizlilikten söz ediliyor ve korktuğu şey tam olarak "
                    "duyulmak; bu yüzden aktarıyorum, ama yorum eklemiyorum.\n\n"
                    "Kararı ona bırakıyorum. Soru sormuyorum, topluyorum — dördünü "
                    "yan yana duyması, benim ekleyeceğim bir sorudan daha çok iş "
                    "görür.",
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
