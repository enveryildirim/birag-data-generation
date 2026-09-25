#!/usr/bin/env python3
"""`v0.1.1` pilotu — 40 kayıtta yeniden kurma (K277 · `prompts/uretim-v6.md`).

⭐ Üç adım; aralarında alt ajan dalgaları koşar:

  orneklem   40 kaydı seçer (12 bitiş adayı + 28 yalnız düşünme; kapsama
             güdümlü, sabit tohum) → `data/plan/v011-pilot.jsonl` (bir kez
             yazılır, üzerine yazılmaz — T78) + yeniden kurma işleri
  birlestir  yeniden kurma sonuçlarını kayda uygular, kayıt kapılarını koşar →
             `data/candidates/v011-pilot.jsonl` + judge ve korunum işleri
  rapor      judge ve korunum sonuçlarını depoya taşır, kabul/red verir →
             `data/judged/v011-pilot.claude.jsonl` ·
             `data/candidates/v011-pilot.korunum.jsonl` ·
             `reports/analiz/2026-09-24-v011-pilot.md`

⛔ Kaynak `v0.1.0`'ın derleme girdisidir (`data/judged/v0.0.22.jsonl`, K275):
yeniden kurulan kayıt, `v0.1.1` derlemesinde onun yerine geçecek olan kayıttır.

⛔⛔ Bitişi değişen kaydın ESKİ ve YENİ cevabı **aynı** judge ile, **aynı**
dalgada, kör ve karışık sırayla yargılanır (K97): ilk yargının judge'ı
(Gemini ya da başka bir Claude dalgası) karşılaştırmaya giremez.

⭐ Kapılar ve ölçüler KOPYALANMIYOR (K103): `src/yeniden_kurma.py`,
`checks.run_checks`, judge istemi 09-15 hazırlama betiğinden, türetme 09-15
toplama betiğinden, olumsuz karar ve kalıp ölçüleri T281 betiğinden.

Kullanım: BIRAG_SCRATCH=<scratchpad> uv run python <betik> orneklem|birlestir|rapor
"""
from __future__ import annotations

import collections
import copy
import hashlib
import json
import os
import random
import re
import statistics as st
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import yeniden_kurma as yk  # noqa: E402
from checks import run_checks  # noqa: E402
from kunye import betik_tarihi  # noqa: E402
from tohum_guvenlik import tr_fold  # noqa: E402

TARIH = Path(__file__).name[:10]
KAYNAK = KOK / "data/judged/v0.0.22.jsonl"
KAYNAK_SHA = "fc1c117d3be48982"             # datasets/v0.1.0/manifest.json
V010 = KOK / "datasets/v0.1.0/train.jsonl"
V010_SHA = "6fcb6b1e16290575"
PLAN = KOK / "data/plan/v011-pilot.jsonl"
ADAY_YOL = KOK / "data/candidates/v011-pilot.jsonl"
KORUNUM_YOL = KOK / "data/candidates/v011-pilot.korunum.jsonl"
YARGI_YOL = KOK / "data/judged/v011-pilot.claude.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-v011-pilot.md"
ORNEK_ID = "833a3c51bbbd1adc139c7201"       # uretim-v6 §1e — pilot ve ölçüm dışı
TOHUM = 20260924
N_IYI, N_SERI, N_TOPLAM, N_OBEK = 6, 6, 40, 10
# ⛔⛔ K277 kurucuyu «claude-code-subagent:opus» diye yazmıştı; o yol KAPALI.
# Opus alt ajanları bu işte API düzeyinde bir güvenlik korumasına takılıyor
# (`reasoning_extraction`, invalid_request) ve daha ilk turda düşüyor — dört
# deneme, dördü de. Pilot bu yüzden alt ajan dalgasıyla değil, oturumun
# kendisinde yazıldı; kullanıcı kararı (2026-09-24): tek üretici, temiz künye.
KURUCU = "claude-code:opus-5"               # yeniden kuran: oturumun kendisi
DENETCI = "claude-sonnet-subagent"          # korunum okuması ve judge

SCRATCH = Path(os.environ.get("BIRAG_SCRATCH", "/nonexistent"))
KURMA = SCRATCH / "v011-pilot/kurma"
KORUNUM = SCRATCH / "v011-pilot/korunum"
JUDGE = SCRATCH / "judge-isleri/v011-pilot"


def _modul(ad: str, yol: str):
    argv = sys.argv[:]
    sys.argv = [str(KOK / yol)]
    sp = _iu.spec_from_file_location(ad, KOK / yol)
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    sys.argv = argv
    return m


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def _son(r: dict) -> dict:
    return [m for m in r["messages"] if m["role"] == "assistant"][-1]


def soru_bitis(t: str | None) -> bool:
    return re.sub(r"[\s\"'»”)\]*_]+$", "", (t or "").strip()).endswith("?")


def _json_oku(y: Path):
    if not y.exists():
        return None
    h = y.read_text(encoding="utf-8").strip()
    if h.startswith("```"):
        h = h.split("```")[1].removeprefix("json").strip()
    return json.loads(h)


def _kaynak() -> dict[str, dict]:
    """`v0.1.0`'a giren judged kayıtlar, id → kayıt (`_checks` sökülmüş)."""
    for p, s in ((KAYNAK, KAYNAK_SHA), (V010, V010_SHA)):
        if _sha(p) != s:
            raise SystemExit(f"⛔ {p.relative_to(KOK)} değişmiş: {_sha(p)} ≠ {s}")
    giren = {json.loads(x)["id"] for x in V010.read_text(encoding="utf-8").splitlines() if x}
    out = {}
    for x in KAYNAK.read_text(encoding="utf-8").splitlines():
        if x.strip():
            r = json.loads(x)
            if r["id"] in giren:
                r.pop("_checks", None)
                out[r["id"]] = r
    if len(out) != len(giren):
        raise SystemExit(f"⛔ v0.1.0 kayıtlarının {len(giren) - len(out)}'i kaynakta yok")
    return out


def ozellikler(r: dict) -> tuple[set, str | None]:
    """(tabaka özellikleri, bitiş adaylığı nedeni ya da None)."""
    gm, th = r["gen_meta"], _son(r).get("thinking") or ""
    a = [m for m in r["messages"] if m["role"] == "assistant"]
    oz = {f"te:{gm.get('turn_ending')}", f"kd:{gm.get('konusma_durumu')}",
          f"slice:{r['slice']}", f"bicim:{gm.get('bicim')}", f"yas:{r['age_group']}",
          f"madde:{r['addiction_type']}"}
    if gm.get("baglam_davranisi"):
        oz.add(f"baglam:{gm['baglam_davranisi']}")
    if "gemini" in ((r.get("judge") or {}).get("judge_model") or ""):
        oz.add("judge:gemini")
    if yk.ISARET.search(th):
        oz.add("isaret")
    if "sormuyorum" in tr_fold(th):
        oz.add("sormuyorum")
    sert, _ = yk.dusunme_temizligi(th, r)
    if any("iskele" in x for x in sert):
        oz.add("iskele")
    neden = None
    if soru_bitis(a[-1]["content"]):
        if gm.get("konusma_durumu") == "iyi_giden_paylasim":
            neden = "iyi_giden_paylasim"
        elif len(a) >= 2 and soru_bitis(a[-2]["content"]):
            neden = "onceki_tur_soru"
    return oz, neden


ASGARI = [("te:acik_uclu_soru", 5), ("te:takdir", 4), ("te:ozet", 4),
          ("te:yalnizca_yansitma", 4), ("te:durur", 3),
          ("kd:tetikleyici_an", 4), ("kd:suregiden_durum", 4), ("kd:iyi_giden_paylasim", 4),
          ("kd:plan_yapma", 4), ("kd:merak_sorusu", 3), ("kd:aradan_donus", 3),
          ("slice:terapotik_tek_tur", 8), ("slice:terapotik_cok_tur", 6),
          ("slice:rag_tek_tur", 5), ("slice:rag_cok_tur", 2),
          ("bicim:kisa", 8), ("bicim:orta", 8), ("bicim:uzun", 8),
          ("isaret", 8), ("sormuyorum", 8), ("iskele", 3),
          ("baglam:cevap_var", 1), ("baglam:cevap_yok", 1), ("baglam:ilgisiz", 1),
          ("baglam:izin_iste", 1), ("baglam:celiskili", 1),
          ("yas:ergen", 3), ("judge:gemini", 4),
          ("madde:alkol", 2), ("madde:tutun", 2), ("madde:kumar", 2),
          ("madde:receteli_ilac", 2), ("madde:dijital", 1)]


def _sec(havuz: list[dict], n: int, rng: random.Random, secili: list[dict]) -> list[dict]:
    """Kapsama güdümlü açgözlü seçim: en çok eksik tabakayı kapatan kayıt."""
    secili = list(secili)
    while len(secili) < n:
        alinan = {s["id"] for s in secili}
        eksik = [oz for oz, k in ASGARI if sum(oz in s["oz"] for s in secili) < k]
        kalan = sorted((r for r in havuz if r["id"] not in alinan), key=lambda r: r["id"])
        if eksik:
            puan = {r["id"]: sum(oz in r["oz"] for oz in eksik) for r in kalan}
            en = max(puan.values())
            kalan = [r for r in kalan if puan[r["id"]] == en]
        secili.append(rng.choice(kalan))
    return secili


def orneklem() -> int:
    if PLAN.exists():
        raise SystemExit(f"⛔ {PLAN.relative_to(KOK)} zaten var — plan bir kez yazılır (T78)")
    kay = _kaynak()
    havuz = []
    for r in kay.values():
        if r.get("replay") or not _son(r).get("thinking") or r["id"] == ORNEK_ID:
            continue
        oz, neden = ozellikler(r)
        havuz.append({"id": r["id"], "oz": oz, "aday": neden})
    rng = random.Random(TOHUM)
    sec = []
    for neden, n in (("iyi_giden_paylasim", N_IYI), ("onceki_tur_soru", N_SERI)):
        sec += rng.sample(sorted((h for h in havuz if h["aday"] == neden),
                                 key=lambda h: h["id"]), n)
    sec = _sec([h for h in havuz if h["aday"] is None], N_TOPLAM, rng, sec)
    rng.shuffle(sec)                          # iş numarası tabakayı ele vermesin
    PLAN.parent.mkdir(parents=True, exist_ok=True)
    PLAN.write_text("".join(json.dumps({"no": f"{i:02d}", "id": h["id"],
                                        "bitis_adayi": h["aday"] is not None,
                                        "aday_nedeni": h["aday"], "oz": sorted(h["oz"])},
                                       ensure_ascii=False) + "\n"
                            for i, h in enumerate(sec, 1)), encoding="utf-8")
    (KURMA / "istek").mkdir(parents=True, exist_ok=True)
    (KURMA / "sonuc").mkdir(parents=True, exist_ok=True)
    for i, h in enumerate(sec, 1):
        r = kay[h["id"]]
        gm = r["gen_meta"]
        is_ = {"no": f"{i:02d}", "bitis_adayi": h["aday"] is not None,
               "aday_nedeni": h["aday"],
               "meta": {k: gm.get(k) for k in ("konusma_durumu", "turn_ending", "bicim",
                                                "baglam_davranisi")}
               | {k: r[k] for k in ("slice", "talk_type", "mi_process", "age_group")},
               "konusma": [{"rol": m["role"], "metin": m["content"]} for m in r["messages"]],
               "eski_thinking": _son(r).get("thinking")}
        (KURMA / "istek" / f"{i:02d}.json").write_text(
            json.dumps(is_, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"✅ plan: {PLAN.relative_to(KOK)} ({len(sec)} kayıt) · işler: {KURMA / 'istek'}")
    print("kapsama:", {oz: sum(oz in h["oz"] for h in sec) for oz, _ in ASGARI})
    print("aday:", collections.Counter(h["aday"] for h in sec))
    return 0


def _plan() -> list[dict]:
    return [json.loads(x) for x in PLAN.read_text(encoding="utf-8").splitlines() if x]


def uygula(eski: dict, s: dict) -> dict:
    """Yeniden kurma sonucunu kayda uygular — başka hiçbir şeye dokunmaz."""
    yeni = copy.deepcopy(eski)
    son = _son(yeni)
    son["thinking"] = s["thinking"]
    kurma = {"talimat": "uretim-v6", "tarih": TARIH, "model": KURUCU, "kaynak": "v0.1.0",
             "bitis_karari": s.get("bitis_karari"), "bitis_gerekcesi": s.get("bitis_gerekcesi"),
             "korunan_soru_turu": s.get("korunan_soru_turu"),
             "onceki_turn_ending": eski["gen_meta"].get("turn_ending"),
             "korunan_kararlar": s.get("korunan_kararlar")}
    if s.get("bitis_karari") == "degisti" and s.get("son_cumle"):
        son["content"] = yk.son_cumle_uygula(son["content"], s["son_cumle"])
        kurma["son_cumle"] = s["son_cumle"]
        yeni["gen_meta"]["turn_ending"] = s.get("turn_ending")
    yeni["gen_meta"]["yeniden_kurma"] = kurma
    return yeni


def kayit_kapilari(eski: dict, yeni: dict, p: dict, s: dict) -> tuple[list, list]:
    """(sert, incelenecek) — betik kapıları; judge ve korunum okuması hariç."""
    sert, inc = [], []
    sert += [f"zarf: {x}" for x in yk.zarf(eski, yeni)]
    th_s, th_i = yk.dusunme_temizligi(_son(yeni)["thinking"], yeni, _son(eski)["thinking"])
    sert += [f"temizlik: {x}" for x in th_s]
    inc += th_i
    chk = run_checks(copy.deepcopy(yeni))
    if not chk["passed"]:
        sert += [f"run_checks: {k}={v}" for k, v in chk.items() if k.endswith("error") and v][:2] \
            or ["run_checks: geçmedi"]
    sert += [f"eşleme: {x}" for x in yk.karar_eslemesi(
        s.get("korunan_kararlar") or [], _son(eski)["thinking"], _son(yeni)["thinking"])]
    bk = s.get("bitis_karari")
    if bk not in yk.BITIS_KARARI:
        sert.append(f"bitiş: bilinmeyen karar «{bk}»")
    elif not p["bitis_adayi"]:
        if bk != "aday_degil" or s.get("son_cumle"):
            sert.append("bitiş: aday olmayan kayıtta bitiş kararı verilmiş")
    else:
        if bk == "aday_degil":
            sert.append("bitiş: aday kayıt «aday_degil» dönmüş")
        if bk == "degisti":
            if soru_bitis(_son(yeni)["content"]) or "?" in (s.get("son_cumle") or {}).get("yeni", "?"):
                sert.append("bitiş: yeni bitiş soru içeriyor")
            if yeni["gen_meta"].get("turn_ending") not in ("takdir", "ozet", "yalnizca_yansitma", "durur"):
                sert.append("bitiş: turn_ending sorusuz bir hamle değil")
        if bk == "korunan_soru" and s.get("korunan_soru_turu") not in yk.KORUNAN_SORU:
            sert.append("bitiş: korunan soru türü eksik")
    return sert, inc


def _render(r: dict, cevap: dict[str, str]) -> str:
    s = ["## Konuşma", ""]
    msj = [m for m in r["messages"] if m["role"] != "system"]
    for m in msj[:-1]:
        s += [f"**{'Kullanıcı' if m['role'] == 'user' else 'Asistan'}:** {m['content']}", ""]
    s += ["## Cevap", ""]
    for ad, c in cevap.items():
        s += ([f"### {ad}", ""] if len(cevap) > 1 else []) + [c, ""]
    return "\n".join(s)


def birlestir() -> int:
    kay, plan = _kaynak(), _plan()
    hs = _modul("_h15", "scripts/analiz/2026-09-15-judge-isleri-hazirla.py")
    import filter as f
    rubrik = f.JUDGE_PROMPT_PATH.read_text()
    ayrac = "\n\n---\n\n## Değerlendirilecek konuşma\n\n"
    yeniler, eksik, dusen, degisen = [], [], [], []
    for p in plan:
        s = _json_oku(KURMA / "sonuc" / f"{p['no']}.json")
        if s is None:
            eksik.append(p["no"])
            continue
        eski = kay[p["id"]]
        try:
            yeni = uygula(eski, s)
        except (ValueError, KeyError) as e:
            dusen.append((p["no"], f"uygulanamadı: {e}"))
            continue
        sert, _ = kayit_kapilari(eski, yeni, p, s)
        if sert:
            dusen.append((p["no"], sert[0]))
        if s.get("bitis_karari") == "degisti":
            degisen.append((eski, yeni))
        yeniler.append(yeni)
    if eksik:
        raise SystemExit(f"⛔ sonucu olmayan iş: {eksik}")
    ADAY_YOL.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in yeniler),
                        encoding="utf-8")

    # ── judge işleri: bitişi değişenin eski ve yeni cevabı, kör ve karışık ──
    rng = random.Random(TOHUM + 1)
    isler = [(e["id"], "eski", e) for e, _ in degisen] + [(y["id"], "yeni", y) for _, y in degisen]
    rng.shuffle(isler)
    for d in ("istek", "sonuc"):
        (JUDGE / d).mkdir(parents=True, exist_ok=True)
    kim = []
    for i, (kid, surum, r) in enumerate(isler, 1):
        tam = hs.prompt_kur(r)
        govde = tam[len(rubrik) + len(ayrac):]
        if rubrik + ayrac + govde != tam:
            raise SystemExit(f"⛔ judge istemi bayt uyumsuz: {kid}")
        (JUDGE / "istek" / f"{i:03d}.txt").write_text(govde, encoding="utf-8")
        kim.append({"no": f"{i:03d}", "id": kid, "surum": surum})
    (JUDGE / "kimlikler.json").write_text(json.dumps(kim, ensure_ascii=False, indent=1),
                                          encoding="utf-8")

    # ── korunum işleri: her kayıt, eski ↔ yeni düşünme ──
    for d in ("istek", "sonuc"):
        (KORUNUM / d).mkdir(parents=True, exist_ok=True)
    sira = list(range(len(yeniler)))
    rng.shuffle(sira)
    kimk = []
    for i, j in enumerate(sira, 1):
        y = yeniler[j]
        e = kay[y["id"]]
        ce, cy = _son(e)["content"], _son(y)["content"]
        cevap = {"Cevap": ce} if ce == cy else {"Eski cevap": ce, "Yeni cevap": cy}
        metin = (_render(e, cevap) + "\n## Eski düşünme\n\n" + _son(e)["thinking"]
                 + "\n\n## Yeni düşünme\n\n" + _son(y)["thinking"] + "\n")
        (KORUNUM / "istek" / f"{i:02d}.txt").write_text(metin, encoding="utf-8")
        kimk.append({"no": f"{i:02d}", "id": y["id"]})
    (KORUNUM / "kimlikler.json").write_text(json.dumps(kimk, ensure_ascii=False, indent=1),
                                            encoding="utf-8")
    print(f"✅ {ADAY_YOL.relative_to(KOK)}: {len(yeniler)} kayıt · betik kapısından düşen "
          f"{len(dusen)} · bitişi değişen {len(degisen)} → judge işi {len(isler)} · "
          f"korunum işi {len(kimk)}")
    for no, neden in dusen:
        print(f"   ⛔ #{no}: {neden}")
    return 0


# ─────────────────────────────── rapor ───────────────────────────────
def _olcu(ths: list[str]) -> dict:
    t = _modul("_t281", "scripts/analiz/2026-09-24-tur-sonu-ve-dusunme.py")
    cum = [c for x in ths for c in t.cumle_bol(x) if len(c.split()) >= 2]
    tekrar = collections.Counter(c for x in ths for c in {k for k, _ in t.kalip_cumleler(x)})
    return {"ortanca sözcük": f"{st.median(len(x.split()) for x in ths):.0f}",
            "⛔ / ⭐ işareti": f"{100 * sum(bool(yk.ISARET.search(x)) for x in ths) / len(ths):.0f}%",
            "«sormuyorum»": f"{100 * sum('sormuyorum' in tr_fold(x) for x in ths) / len(ths):.0f}%",
            "kural okuma (*tek seferde · kural · protokol*)":
                f"{100 * sum(bool(yk.KURAL_OKUMA.search(tr_fold(x))) for x in ths) / len(ths):.0f}%",
            "olumsuz karar cümlesi payı":
                f"{100 * sum(bool(t.OLUMSUZ.search(tr_fold(c))) for c in cum) / len(cum):.0f}%",
            "≥ 3 kayıtta birebir geçen cümle": str(sum(1 for n in tekrar.values() if n >= 3))}


def rapor() -> int:
    kay, plan = _kaynak(), _plan()
    yeniler = {json.loads(x)["id"]: json.loads(x)
               for x in ADAY_YOL.read_text(encoding="utf-8").splitlines() if x}
    t15 = _modul("_t15", "scripts/analiz/2026-09-15-judge-sonuclari-topla.py")
    t15.JUDGE_ADI, t15.RUBRIK = DENETCI, "judge-eksen1.v9"

    yargi: dict[tuple[str, str], dict] = {}
    for k in json.loads((JUDGE / "kimlikler.json").read_text()):
        h = _json_oku(JUDGE / "sonuc" / f"{k['no']}.json")
        if h is None:
            raise SystemExit(f"⛔ judge sonucu yok: {k['no']}")
        yargi[(k["id"], k["surum"])] = t15.turet(h)
    korunum = {}
    for k in json.loads((KORUNUM / "kimlikler.json").read_text()):
        h = _json_oku(KORUNUM / "sonuc" / f"{k['no']}.json")
        if h is None:
            raise SystemExit(f"⛔ korunum sonucu yok: {k['no']}")
        korunum[k["id"]] = h | {"_okuyan": DENETCI, "_istem": "karar-korunumu.v1"}

    # ── depoya taşı (Kural 7: raporlanan sayının girdisi depoda) ──
    KORUNUM_YOL.write_text("".join(json.dumps({"id": i} | v, ensure_ascii=False) + "\n"
                                   for i, v in korunum.items()), encoding="utf-8")
    yazilan = []
    for p in plan:
        r = copy.deepcopy(yeniler[p["id"]])
        if (p["id"], "yeni") in yargi:
            r["judge_v010"] = r["judge"]
            r["judge_esli_eski"] = yargi[(p["id"], "eski")]
            r["judge"] = yargi[(p["id"], "yeni")]
        yazilan.append(r)
    YARGI_YOL.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in yazilan),
                         encoding="utf-8")

    # ── karar ──
    satir = []
    for p in plan:
        e, y = kay[p["id"]], yeniler[p["id"]]
        s = {"korunan_kararlar": y["gen_meta"]["yeniden_kurma"].get("korunan_kararlar"),
             "bitis_karari": y["gen_meta"]["yeniden_kurma"].get("bitis_karari"),
             "son_cumle": y["gen_meta"]["yeniden_kurma"].get("son_cumle"),
             "korunan_soru_turu": y["gen_meta"]["yeniden_kurma"].get("korunan_soru_turu")}
        sert, inc = kayit_kapilari(e, y, p, s)
        k = korunum[p["id"]]
        dus = [x for x in k.get("kararlar", []) if x.get("durum") == "dustu"]
        kis = [x for x in k.get("kararlar", []) if x.get("durum") == "kismen"]
        sert += [f"korunum: karar düştü — «{(x.get('eski') or '')[:50]}»" for x in dus]
        sert += [f"korunum: uydurma — «{(x.get('parca') or '')[:50]}»" for x in k.get("uydurma", [])]
        sert += [f"korunum: tutarsızlık — «{(x.get('parca') or '')[:50]}»"
                 for x in k.get("tutarsizlik", [])]
        sert += [f"korunum: biçim — {x.get('tur')}" for x in k.get("bicim_ihlali", [])]
        inc += [f"korunum: kısmen — «{(x.get('eski') or '')[:50]}»" for x in kis]
        b = k.get("bitis") or {}
        jd = None
        if s["bitis_karari"] == "degisti":
            if b.get("korunan_soru_cikarildi"):
                sert.append("korunum: korunan soru çıkarılmış")
            if b.get("ovgu_ya_da_atif"):
                sert.append("korunum: övgü ya da atıf")
            if b.get("uygun") is False:
                sert.append("korunum: bitiş duruma uygun değil")
            je, jy = yargi[(p["id"], "eski")], yargi[(p["id"], "yeni")]
            jd = (je, jy)
            if jy.get("klinik_guvenlik_ihlali") or jy.get("rol_siniri_ihlali"):
                sert.append("judge: güvenlik ya da rol sınırı ihlali")
            for alan in ("grounding", "mi_uyumu"):
                if (jy.get(alan) or 0) < (je.get(alan) or 0):
                    sert.append(f"judge: {alan} düştü {je.get(alan)}→{jy.get(alan)}")
            if len(jy.get("tuzak_ihlali") or []) > len(je.get("tuzak_ihlali") or []):
                sert.append("judge: yeni tuzak")
        satir.append({"p": p, "e": e, "y": y, "sert": sert, "inc": inc, "jd": jd,
                      "bk": s["bitis_karari"], "kst": s["korunan_soru_turu"]})

    kabul = [x for x in satir if not x["sert"]]
    s = ["# `v0.1.1` pilotu — 40 kayıtta yeniden kurma", "",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {betik_tarihi(__file__)}  ",
         f"**Girdi:** `data/judged/v0.0.22.jsonl` SHA256-16 `{KAYNAK_SHA}` (v0.1.0'ın derleme "
         f"girdisi) · plan `data/plan/v011-pilot.jsonl` SHA256-16 `{_sha(PLAN)}` · "
         f"talimat `prompts/uretim-v6.md` SHA256-16 `{_sha(KOK / 'prompts/uretim-v6.md')}`  ",
         f"**Yeniden kuran:** `{KURUCU}` · **korunum okuması ve judge:** `{DENETCI}` "
         "(`karar-korunumu.v1` · `judge-eksen1.v9`)", "",
         f"## Sonuç: {len(kabul)}/{len(satir)} kabul", "",
         "| kapı | düşen kayıt |", "|---|---:|"]
    for ad in ("zarf", "temizlik", "run_checks", "eşleme", "bitiş", "korunum", "judge"):
        n = sum(1 for x in satir if any(z.startswith(ad) for z in x["sert"]))
        s.append(f"| {ad} | {n} |")
    s += ["", "⭐ Reddedilen yeniden kurma kaydı kaybettirmez: kayıt `v0.1.0` hâliyle kalır.", ""]

    s += ["## Düşünme — eski ↔ yeni (40 kayıt)", "", "| ölçü | eski | yeni |", "|---|---:|---:|"]
    oe = _olcu([_son(x["e"])["thinking"] for x in satir])
    oy = _olcu([_son(x["y"])["thinking"] for x in satir])
    s += [f"| {k} | {oe[k]} | {oy[k]} |" for k in oe]
    oran = lambda r: len(_son(r)["thinking"]) / max(1, len(_son(r)["content"]))
    s += [f"| düşünme : cevap (karakter, ortanca) | {st.median(oran(x['e']) for x in satir):.1f}x | "
          f"{st.median(oran(x['y']) for x in satir):.1f}x |", ""]

    s += ["## Tur sonu — 12 bitiş adayı", "", "| karar | kayıt |", "|---|---:|"]
    ad = [x for x in satir if x["p"]["bitis_adayi"]]
    for k, n in collections.Counter(
            x["bk"] + (f" · {x['kst']}" if x["kst"] else "") for x in ad).most_common():
        s.append(f"| `{k}` | {n} |")
    gecis = collections.Counter(
        f"`{x['e']['gen_meta'].get('turn_ending')}` → `{x['y']['gen_meta'].get('turn_ending')}`"
        for x in ad if x["bk"] == "degisti")
    if gecis:
        s += ["", "| geçiş | kayıt |", "|---|---:|"] + [f"| {k} | {n} |" for k, n in gecis.items()]
    jl = [x for x in ad if x["jd"]]
    if jl:
        s += ["", "### Bitişi değişenler — aynı judge, aynı dalga, eski ↔ yeni cevap", "",
              "| no | güvenlik ihlali | rol ihlali | `grounding` | `mi_uyumu` | `dogallik` | "
              "`takdir_var` | `ovgu_tonu` |", "|---|---|---|---:|---:|---:|---|---|"]
        for x in jl:
            je, jy = x["jd"]
            g = lambda a: f"{je.get(a)}→{jy.get(a)}"
            s.append(f"| {x['p']['no']} | {g('klinik_guvenlik_ihlali')} | {g('rol_siniri_ihlali')} | "
                     f"{g('grounding')} | {g('mi_uyumu')} | {g('dogallik')} | {g('takdir_var')} | "
                     f"{g('ovgu_tonu')} |")
    s += ["", "## Kayıt kayıt", "", "| no | aday | bitiş | durum | ilk sebep / inceleme |",
          "|---|---|---|---|---|"]
    for x in sorted(satir, key=lambda x: x["p"]["no"]):
        durum = "⛔ red" if x["sert"] else ("⚠️ incele" if x["inc"] else "✅ kabul")
        not_ = (x["sert"] or x["inc"] or [""])[0].replace("|", "/")
        s.append(f"| {x['p']['no']} | {x['p']['aday_nedeni'] or '—'} | `{x['bk']}` | {durum} | {not_} |")

    ornek = []
    for kosul in (lambda x: x["bk"] == "degisti", lambda x: x["bk"] == "korunan_soru",
                  lambda x: not x["p"]["bitis_adayi"] and "isaret" in x["p"]["oz"]):
        aday_ = [x for x in sorted(kabul, key=lambda x: x["p"]["no"]) if kosul(x)]
        if aday_:
            ornek.append(aday_[0])
    s += ["", "## Örnekler (kabul edilenlerden, kurala göre ilk)", ""]
    for x in ornek:
        u = [m for m in x["e"]["messages"] if m["role"] == "user"][-1]["content"]
        s += [f"### #{x['p']['no']} — `{x['bk']}`", "", f"**Kullanıcı (son):** {u}", "",
              "**Eski düşünme:**", "", "> " + _son(x["e"])["thinking"].replace("\n", "\n> "), "",
              "**Yeni düşünme:**", "", "> " + _son(x["y"])["thinking"].replace("\n", "\n> "), ""]
        if x["bk"] == "degisti":
            sc = x["y"]["gen_meta"]["yeniden_kurma"]["son_cumle"]
            s += [f"**Bitiş:** ~~{sc['eski']}~~ → {sc['yeni']}", ""]
    s += ["## ⛔ Bunun söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ **Model başarımı hakkında bir şey söylemez** | eğitim yok; bu, verinin "
          "kapılardan ve okumadan geçip geçmediğidir |",
          "| ⛔ **Korunum okuması tek bir okuyucu** | Sonnet alt ajanı, tekrar yok ⇒ gürültü "
          "tabanı bilinmiyor; pilot sonunda insan okuması şart |",
          "| ⚠️ **Judge eşleşmesi küçük** | bitişi değişen kayıt az; tekrar kümesi yok ⇒ puan "
          "farkları betimleyici, yalnız ikili ihlaller (güvenlik, rol) sert |",
          "| ⚠️ **Üretici ile denetçi aynı aileden** | K45 — körlük azaltır, sıfırlamaz |",
          "| ⛔⛔ **Judge körlüğü SIZDIRIYOR** | eşli işler kaydı tam hâliyle render ediyor, yani ESKİ sürümün iç "
          "muhakemesi ⛔/⭐ taşırken YENİ'ninki taşımıyor. Rubrik düşünmeyi değerlendirme dışı sayar ve "
          "puanlayıcı uyarıldı, ama hangisinin yeni olduğu biçimden okunabiliyor — puanlayıcı dalga özetinde "
          "eşleri kendiliğinden eşleştirdiğini yazdı. ⇒ Bu tablodaki eski↔yeni farkları **kör değil**. "
          "Faz 3'ün ön kaydında eşli yargı, iç muhakeme sökülerek ya da iki sürümde de aynı düşünmeyle "
          "koşulmalı |",
          "| ⛔ **Kurucu K277'den farklı** | K277 `claude-code-subagent:opus` diyordu; Opus alt ajanları bu işte "
          "API düzeyinde bir korumaya takılıyor (`reasoning_extraction`) ve ilk turda düşüyor. Pilot oturumun "
          "kendisinde yazıldı ⇒ **kurucu ile raporu yazan aynı**; kayıt kapıları betik, korunum okuması ve "
          "judge bağımsız, ama bitiş kararlarının gerekçesini yazan da veren de aynı taraf |",
          "| ⚠️ **Bitiş adaylığı etiketten geliyor** | üç kayıtta (13 · 21 · 32) `konusma_durumu` "
          "`iyi_giden_paylasim` beyan edilmiş ama paylaşılan şey iyi giden bir adım değil (yönlendirme "
          "sorusu · süren bedensel belirti · damga kaygısı). Aday havuzunu bu alan beslediği için tam "
          "geçişteki ~65 kayıtlık dilimin bir kısmı da yanlış etiketli olabilir |"]
    RAPOR.write_text("\n".join(s) + "\n", encoding="utf-8")
    print("\n".join(s[:20]))
    print(f"\nyazıldı: {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    adim = sys.argv[1] if len(sys.argv) > 1 else ""
    if adim not in ("orneklem", "birlestir", "rapor"):
        raise SystemExit("kullanım: <betik> orneklem|birlestir|rapor")
    if not SCRATCH.exists():
        raise SystemExit("⛔ BIRAG_SCRATCH tanımlı değil ya da yok")
    raise SystemExit({"orneklem": orneklem, "birlestir": birlestir, "rapor": rapor}[adim]())
