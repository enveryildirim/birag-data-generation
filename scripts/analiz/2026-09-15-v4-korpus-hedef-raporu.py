#!/usr/bin/env python3
"""uretim-v4 korpus hedef raporu. §9a: "Rapor olmadan hedef tuttu denemez."

⚠️ Bu betik `2026-09-14-korpus-hedef-raporu.py`'nin YERİNE geçmez, onun yanına
yazılır. Eski betik v3 eksenlerini biliyor ve çıktısı `reports/analiz/` altında
kayıtlı (Kural 7); değiştirilmiyor. v4 dört eksen ekledi — `bicim`, `register`,
`turn_type` ve `sinir_tipi` — ve eski betik onları **sessizce atlar** (T25).

⛔ `sinir_tipi` ekseninde bu betik TERİM SAYMAZ. §8b'nin bulgusu tam olarak
şudur: aynı terim listesi *sınır çekme* ile *yönlendirme*yi ayıramıyor (T29).
Betik yalnızca **aday** üretir; sınıflandırmayı insan yapar ve kararı §8b'nin
üretimden önce yazılmış dört maddelik ölçütüne göre verir.

Kullanım: uv run python scripts/analiz/2026-09-15-v4-korpus-hedef-raporu.py <parti.jsonl>
"""
from __future__ import annotations

import hashlib
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).parent.parent.parent

HEDEF = {
    "bicim":          {"kisa": 40, "orta": 35, "uzun": 25},
    "register":       {"bozuk": 25, "duzgun": 75},
    "konusma_durumu": {"tetikleyici_an": 35, "suregiden_durum": 20, "iyi_giden_paylasim": 15,
                       "plan_yapma": 15, "merak_sorusu": 10, "aradan_donus": 5},
    "turn_ending":    {"acik_uclu_soru": 50, "takdir": 15, "ozet": 15,
                       "yalnizca_yansitma": 15, "durur": 5},
    "mi_process":     {"engaging": 40, "focusing": 20, "evoking": 25, "planning": 15},
    "turn_type":      {"multi": 40, "single": 60},
    "sinir_tipi":     {"yonlendirme_istegi": 6, "rol_siniri_yonlendirme": 8,
                       "yonlendirme_gereksiz": 5},
}
BICIM_BANT = {"kisa": (1, 8), "orta": (9, 25), "uzun": (26, 10**6)}

# §8b aday taraması. ⚠️ Bunlar KARAR DEĞİL, okuma listesi: terim geçen her kayıt
# elle okunup `sinir_cekme` mi `yonlendirme` mi olduğuna bakılır.
TERIMLER = ["uzman", "profesyonel", "hekim", "doktor", "acil", "destek hattı",
            "danışma hattı", "yardım hattı", "sağlık", "amatem", "yedam", "başvur",
            "yanında biri", "yanında birileri", "birine ulaş", "güvende",
            "danışmanlık", "merkez", "birim", "avukat", "müdürlük"]
# K18: model bu özel adları KENDİSİ ortaya atamaz; kullanıcı andıysa yansıtabilir.
OZEL_AD = ["AMATEM", "ÇEMATEM", "YEDAM", "ALO 191", "Yeşilay", "SHÇEK"]
RAKAM = re.compile(r"\d")



# ─── §8b düzeltme ölçütü 1 ve 2 · ELLE KARAR ───
# Aday listesi makineden, KARAR buradan. Aynı desen: 2026-09-15-v002-yonlendirme-
# envanteri.py. Ölçüt 1: `yonlendirme_istegi` ve `rol_siniri_yonlendirme`
# kayıtlarının HEPSİNDE kaynağın türünü adlandıran ve bir ADIM gösteren cümle
# olmalı. Ölçüt 2: `yonlendirme_gereksiz` kayıtlarının HİÇBİRİNDE yönlendirme
# cümlesi olmamalı.
# ⚠️ [3]'ün adım cümlesinde hiçbir terim geçmiyor — aday listesi onu göstermiyor.
# Bu, §8b'nin kendi iddiasının parti üstünde tekrarı: terim taraması hamleyi ölçmez.
ELLE_KARAR = {
    1:  ("GECTI", "«iki tür yere gidiliyor: … danışmanlık veren merkezler … bağımlılık birimleri» — tür + adım"),
    2:  ("GECTI", "«Böyle yerler var — … danışmanlık veren merkezler» — doğrudan soruya cevap, tür + adım"),
    3:  ("GECTI", "adım cümlesi TERİMSİZ: «bir sonraki görüşmede bunu olduğu gibi anlatmak, buradan atılabilecek en yakın adım»"),
    4:  ("GECTI", "«bu soruyu soracak kişi bu sabah zaten karşında oturuyordu … ilk cümlen o olabilir» — tür + adım"),
    5:  ("GECTI", "«yükümlülüğünü takip eden müdürlük, bir de bir avukat» — tür (özel ad yok) + adım"),
    6:  ("GECTI", "yönlendirme cümlesi yok; kullanıcı «bir şey sormayacağım» dedi ve tırmandırma yapılmadı"),
    7:  ("GECTI", "yönlendirme cümlesi yok; «kafayı yiyecem» mecazı kriz sayılmadı"),
}


def elle_karar_yaz(kay) -> None:
    print("\n### §8b düzeltme ölçütü 1 ve 2 — ELLE KARAR")
    kapsam = {k["gen_meta"]["parti_sira"] for k in kay
              if k["gen_meta"].get("sinir_tipi") in
              ("yonlendirme_istegi", "rol_siniri_yonlendirme", "yonlendirme_gereksiz")}
    eksik = sorted(kapsam - set(ELLE_KARAR))
    fazla = sorted(set(ELLE_KARAR) - kapsam)
    if eksik or fazla:
        print(f"  ⛔ elle karar tablosu kayıtlarla örtüşmüyor — tabloda yok: {eksik} · kayıtta yok: {fazla}")
        return
    for sira in sorted(ELLE_KARAR):
        karar, gerekce = ELLE_KARAR[sira]
        print(f"  [{sira:2d}] {karar}  {gerekce}")
    kaldi = [s for s, (k, _) in ELLE_KARAR.items() if k != "GECTI"]
    print(f"  → ölçüt 1 ve 2: {'TUTTU ✅' if not kaldi else f'TUTMADI ⛔ {kaldi}'}")


def son(k): return next(m for m in reversed(k["messages"]) if m["role"] == "assistant")
def kullanici_metni(k): return " ".join(m["content"] for m in k["messages"] if m["role"] == "user")
def ilk_kullanici(k): return next(m["content"] for m in k["messages"] if m["role"] == "user")


def dagilim(kay, alan, yuzde_hedef):
    n = len(kay)
    c = Counter(k["gen_meta"].get(alan) or k.get(alan) for k in kay)
    satir = []
    for deger, hedef in yuzde_hedef.items():
        adet = c.get(deger, 0)
        ger = 100 * adet / n
        satir.append((deger, adet, round(ger, 1), hedef, round(ger - hedef, 1)))
    for deger, adet in c.items():
        if deger not in yuzde_hedef:
            satir.append((str(deger), adet, round(100 * adet / n, 1), None, None))
    return satir


def yaz_tablo(baslik, satirlar):
    print(f"\n### {baslik}")
    print(f"{'değer':22s} {'adet':>4s} {'%':>6s} {'hedef':>6s} {'fark':>6s}")
    for d, a, g, h, f in satirlar:
        print(f"{d:22s} {a:4d} {g:6.1f} {'—' if h is None else f'{h:6.1f}'} {'—' if f is None else f'{f:+6.1f}'}")


def main() -> None:
    yol = Path(sys.argv[1]) if len(sys.argv) > 1 else KOK / "data/candidates/v4-parti1.jsonl"
    ham = yol.read_bytes()
    kay = [json.loads(s) for s in ham.decode().splitlines() if s.strip()]
    kay = [k for k in kay if not k.get("replay")]

    print(f"# uretim-v4 korpus hedef raporu · {yol.name}")
    print(f"girdi sha256: {hashlib.sha256(ham).hexdigest()[:16]} · kayıt: {len(kay)}")
    print(f"betik: scripts/analiz/{Path(__file__).name}")

    for alan, hedef in HEDEF.items():
        if alan == "sinir_tipi":
            continue
        yaz_tablo(f"{alan} (§ hedefi)", dagilim(kay, alan, hedef))

    # ─── beyan ↔ metin tutarlılığı ───
    print("\n### beyan ↔ metin tutarsızlıkları")
    sorun = []
    for k in kay:
        s = k["gen_meta"]["parti_sira"]; c = son(k)["content"]
        te = k["gen_meta"]["turn_ending"]
        soru = c.count("?")
        if te in {"takdir", "ozet", "yalnizca_yansitma", "durur"} and soru:
            sorun.append(f"{s}: `{te}` beyan edildi ama cevap {soru} soru içeriyor")
        if te == "acik_uclu_soru" and soru == 0:
            sorun.append(f"{s}: `acik_uclu_soru` beyan edildi ama soru yok")
        alt, ust = BICIM_BANT[k["gen_meta"]["bicim"]]
        kel = len(ilk_kullanici(k).split("\n")[-1].split()) if k.get("context") else len(ilk_kullanici(k).split())
        if not (alt <= kel <= ust):
            sorun.append(f"{s}: `{k['gen_meta']['bicim']}` beyan edildi ama ilk mesaj {kel} kelime ({alt}-{ust} bekleniyor)")
    print("\n".join(f"  ⚠️ {x}" for x in sorun) if sorun else "  yok ✅")

    # ─── §8b: ADAY listesi (karar elle) ───
    print("\n### §8b · sinir_tipi beyanları")
    c = Counter(k["gen_meta"].get("sinir_tipi") for k in kay)
    for d, hedef in HEDEF["sinir_tipi"].items():
        a = c.get(d, 0)
        print(f"  {d:24s} {a:3d}  %{100*a/len(kay):4.1f}  (hedef ~%{hedef})")
    for d, a in c.items():
        if d not in HEDEF["sinir_tipi"]:
            print(f"  {d:24s} {a:3d}  %{100*a/len(kay):4.1f}  (kota yok)")

    print("\n### §8b düzeltme ölçütü — ÖLÇÜT 1/2 için ADAY listesi (karar elle okunur)")
    for k in kay:
        st = k["gen_meta"].get("sinir_tipi")
        if st in (None, "yok"):
            continue
        c = son(k)["content"]
        bulunan = [t for t in TERIMLER if t in c.lower()]
        cum = [x.strip() for x in re.split(r"(?<=[.!?])\s+", c) if any(t in x.lower() for t in TERIMLER)]
        print(f"\n  [{k['gen_meta']['parti_sira']:2d}] {st}  terim={bulunan or '—'}")
        for x in cum:
            print(f"       · {x[:150]}")
        if not cum:
            print("       · (yönlendirme/sınır cümlesi yok)")

    elle_karar_yaz(kay)

    # ─── ÖLÇÜT 3: makine denetlenebilir ───
    print("\n### §8b düzeltme ölçütü 3 — rakam ve kurum özel adı (makine)")
    ihlal = []
    for k in kay:
        s = k["gen_meta"]["parti_sira"]
        for m in k["messages"]:
            if m["role"] != "assistant":
                continue
            if RAKAM.search(m["content"]):
                ihlal.append(f"{s}: asistan cevabında rakam — {RAKAM.search(m['content']).group()}")
        kul = kullanici_metni(k)
        for ad in OZEL_AD:
            if ad.lower() in son(k)["content"].lower() and ad.lower() not in kul.lower():
                ihlal.append(f"{s}: kurum özel adı «{ad}» modelden çıkıyor, kullanıcı anmamış (K18)")
    print("\n".join(f"  ⚠️ {x}" for x in ihlal) if ihlal else "  ihlal yok ✅")

    # ─── K31: eval metniyle çakışma ───
    print("\n### K31 · eval metniyle çakışma (üretim tarafı denetimi)")
    ev = []
    for p in sorted((KOK / "evals").glob("*.jsonl")):
        for l in open(p, encoding="utf-8"):
            r = json.loads(l)
            ev += [(p.name, r["id"], m["content"].strip().lower())
                   for m in r.get("messages", []) if m["role"] == "user"
                   and len(m["content"].strip()) >= 40]
    carp = []
    for k in kay:
        for m in k["messages"]:
            if m["role"] != "user":
                continue
            d = m["content"].strip().lower()
            if len(d) < 40:
                continue
            for dn, eid, e in ev:
                if e[:60] in d or d[:60] in e:
                    carp.append(f"{k['gen_meta']['parti_sira']}: {dn} {eid}")
    print("\n".join(f"  ⚠️ {x}" for x in sorted(set(carp))) if carp else "  çakışma yok ✅")

    # ─── uzunluk / oran ───
    cw = [len(son(k)["content"].split()) for k in kay]
    tw = [len((son(k).get("thinking") or "").split()) for k in kay]
    orn = [len(son(k).get("thinking") or "") / max(len(son(k)["content"]), 1) for k in kay]
    print(f"\n### uzunluk\ncompletion ortanca {statistics.median(cw)} kelime · "
          f"thinking ortanca {statistics.median(tw)} kelime · "
          f"thinking:completion (karakter) ortanca {statistics.median(orn):.2f}x, maks {max(orn):.2f}x (tavan 4x)")
    print(f"system promptu: {dict(Counter(k['gen_meta']['system_prompt_variant'] for k in kay))}")
    print(f"özerklik vurgusu: {sum(1 for k in kay if k['gen_meta'].get('ozerklik_vurgusu'))}/{len(kay)}")
    print(f"bağlam (RAG): {sum(1 for k in kay if k.get('context'))}/{len(kay)} · "
          f"is_negative: {sum(1 for k in kay if k['is_negative'])}/{len(kay)}")
    print(f"bağımlılık türü: {dict(Counter(k['addiction_type'] for k in kay))}")
    print(f"yaş: {dict(Counter(k['age_group'] for k in kay))} · "
          f"motivasyon: {dict(Counter(k['motivation'] for k in kay))}")
    print(f"senaryo: {dict(Counter(k['scenario'] for k in kay).most_common())}")


if __name__ == "__main__":
    main()
