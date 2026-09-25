#!/usr/bin/env python3
"""`v0.1.1` Faz 2 — kalan 1000 kaydın yeniden kurulması (K277 · `prompts/uretim-v6.md`).

⭐ Pilot (T282) `uretim-v6`'yı 40 kayıtta sınadı ve iki belge boşluğu buldu;
ikisi de kapatıldıktan sonra bu faz başladı. Pilotun kendisi tekrarlanmaz:
onun 40 kaydı `data/candidates/v011-pilot.jsonl`'de durur ve derlemeye oradan
girer.

⭐ Adımlar — aralarında alt ajan dalgaları koşar:

  plan              1000 kaydı bloklara böler (sabit tohum) →
                    `data/plan/v011-faz2.jsonl` (bir kez yazılır — T78) +
                    bütün yeniden kurma işleri
  birlestir <blok>  o bloğun sonuçlarını uygular, kayıt kapılarını koşar →
                    `data/candidates/v011-faz2-b<NN>.jsonl` + korunum ve judge işleri
  depola            geçici klasördeki korunum/judge sonuçlarını depoya yazar
                    (okunan metnin SHA'sıyla) — her okuma dalgasından sonra
  geri_yukle        geçici klasörü depodan yeniden kurar (/tmp silinirse)
  rapor             önce depola, sonra bütün blokları toplar, kabul/red verir →
                    `reports/analiz/2026-09-24-v011-faz2.md`

⛔⛔ **K260 rejimi:** alt ajan blok taslağını yazar; **her kaydı Claude Code
okur, revize eder ve kapılardan geçirir.** Tezde yazarlık iddiası buna göre
beyan edilir. Bu betik okumanın yerine geçmez, yalnız neyin okunmadığını
görünür kılar (`rapor` → «okunmamış kayıt» satırı).

⛔ Kaynak `v0.1.0`'ın derleme girdisi (`data/judged/v0.0.22.jsonl`, K275).
Kapılar, ölçüler ve judge istemi KOPYALANMIYOR (K103): hepsi pilot betiğinden
içe aktarılıyor.

Kullanım: BIRAG_SCRATCH=<scratchpad> uv run python <betik> plan|birlestir <blok>|depola|geri_yukle|rapor|kontrol <no…>|oku <no…>
"""
from __future__ import annotations

import collections
import difflib
import hashlib
import json
import os
import random
import statistics as st
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))


def _modul(ad: str, yol: str):
    argv = sys.argv[:]
    sys.argv = [str(KOK / yol)]
    sp = _iu.spec_from_file_location(ad, KOK / yol)
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    sys.argv = argv
    return m


P = _modul("_pilot", "scripts/analiz/2026-09-24-v011-pilot.py")
import yeniden_kurma as yk  # noqa: E402
from kunye import betik_tarihi  # noqa: E402

TARIH = Path(__file__).name[:10]
PLAN = KOK / "data/plan/v011-faz2.jsonl"
PILOT_PLAN = KOK / "data/plan/v011-pilot.jsonl"
ADAY = KOK / "data/candidates"
RAPOR = KOK / f"reports/analiz/{TARIH}-v011-faz2.md"
KORUNUM_DEPO = KOK / "data/candidates/v011-faz2.korunum.jsonl"
JUDGE_DEPO = KOK / "data/judged/v011-faz2.judge.jsonl"
TOHUM = 20260924
BLOK = 25                                   # kayıt/blok — alt ajan başına bir blok

SCRATCH = Path(os.environ.get("BIRAG_SCRATCH", "/nonexistent"))
KURMA = SCRATCH / "v011-faz2/kurma"
KORUNUM = SCRATCH / "v011-faz2/korunum"
JUDGE = SCRATCH / "judge-isleri/v011-faz2"


def _plan() -> list[dict]:
    return [json.loads(x) for x in PLAN.read_text(encoding="utf-8").splitlines() if x.strip()]


def _plan_pilot() -> list[dict]:
    """⭐ Pilotun 40 kaydı bu hatta «blok 0» olarak girer (numara P01..P40): 1040
    kaydın hepsi tek depo, tek geri yükleme, tek rapor. Pilot planı değişmez (T78)."""
    out = []
    for x in PILOT_PLAN.read_text(encoding="utf-8").splitlines():
        if x.strip():
            q = json.loads(x)
            out.append({"no": "P" + q["no"], "blok": 0, "id": q["id"],
                        "bitis_adayi": q["bitis_adayi"], "aday_nedeni": q["aday_nedeni"],
                        "oz": q.get("oz", [])})
    return out


def _plan_tum() -> list[dict]:
    return _plan_pilot() + _plan()


def _aday_yolu(blok: int) -> Path:
    return ADAY / ("v011-pilot.jsonl" if blok == 0 else f"v011-faz2-b{blok:02d}.jsonl")


def _blok_kayitlari(blok: int) -> list[dict]:
    return [p for p in _plan_tum() if p["blok"] == blok]


def plan() -> int:
    if PLAN.exists():
        raise SystemExit(f"⛔ {PLAN.relative_to(KOK)} zaten var — plan bir kez yazılır (T78)")
    kay = P._kaynak()
    pilot = {json.loads(x)["id"] for x in PILOT_PLAN.read_text(encoding="utf-8").splitlines() if x.strip()}
    havuz = []
    for r in kay.values():
        if r.get("replay") or not P._son(r).get("thinking"):
            continue
        if r["id"] in pilot or r["id"] == P.ORNEK_ID:
            continue
        oz, neden = P.ozellikler(r)
        havuz.append({"id": r["id"], "oz": sorted(oz), "aday": neden})
    havuz.sort(key=lambda h: h["id"])
    random.Random(TOHUM + 2).shuffle(havuz)          # blok ≠ tabaka
    PLAN.parent.mkdir(parents=True, exist_ok=True)
    sat = []
    for i, h in enumerate(havuz):
        sat.append({"no": f"{i + 1:04d}", "blok": i // BLOK + 1, "id": h["id"],
                    "bitis_adayi": h["aday"] is not None, "aday_nedeni": h["aday"],
                    "oz": h["oz"]})
    PLAN.write_text("".join(json.dumps(s, ensure_ascii=False) + "\n" for s in sat),
                    encoding="utf-8")
    for d in ("istek", "sonuc"):
        (KURMA / d).mkdir(parents=True, exist_ok=True)
    for s in sat:
        r = kay[s["id"]]
        gm = r["gen_meta"]
        (KURMA / "istek" / f"{s['no']}.json").write_text(json.dumps(
            {"no": s["no"], "bitis_adayi": s["bitis_adayi"], "aday_nedeni": s["aday_nedeni"],
             "meta": {k: gm.get(k) for k in ("konusma_durumu", "turn_ending", "bicim",
                                             "baglam_davranisi")}
             | {k: r[k] for k in ("slice", "talk_type", "mi_process", "age_group")},
             "konusma": [{"rol": m["role"], "metin": m["content"]} for m in r["messages"]],
             "eski_thinking": P._son(r).get("thinking")},
            ensure_ascii=False, indent=1), encoding="utf-8")
    nb = sat[-1]["blok"]
    print(f"✅ plan: {PLAN.relative_to(KOK)} · {len(sat)} kayıt · {nb} blok × {BLOK} · "
          f"bitiş adayı {sum(s['bitis_adayi'] for s in sat)}")
    print(f"   işler: {KURMA / 'istek'}")
    return 0


def _sha16(metin: str) -> str:
    return hashlib.sha256(metin.encode("utf-8")).hexdigest()[:16]


def _korunum_metni(e: dict, y: dict) -> str:
    """Korunum okuyucusunun gördüğü metin — SHA'sı okumayı o metne bağlar."""
    ce, cy = P._son(e)["content"], P._son(y)["content"]
    cevap = {"Cevap": ce} if ce == cy else {"Eski cevap": ce, "Yeni cevap": cy}
    return (P._render(e, cevap) + "\n## Eski düşünme\n\n" + P._son(e)["thinking"]
            + "\n\n## Yeni düşünme\n\n" + P._son(y)["thinking"] + "\n")


_HS = None


def _judge_govde(r: dict) -> str:
    """Judge'ın gördüğü gövde (rubrik hariç) — bayt uyumu burada denetlenir."""
    global _HS
    if _HS is None:
        _HS = _modul("_h15", "scripts/analiz/2026-09-15-judge-isleri-hazirla.py")
    import filter as f
    rubrik = f.JUDGE_PROMPT_PATH.read_text()
    ayrac = "\n\n---\n\n## Değerlendirilecek konuşma\n\n"
    tam = _HS.prompt_kur(r)
    govde = tam[len(rubrik) + len(ayrac):]
    if rubrik + ayrac + govde != tam:
        raise SystemExit(f"⛔ judge istemi bayt uyumsuz: {r['id']}")
    return govde


def _yaz_degistiyse(yol: Path, metin: str) -> None:
    """Yalnız içerik değiştiyse yazar. ⚠️ depola, bir okumanın bayat olup olmadığını
    istek dosyasının tarihinden anlar; içeriği aynı dosyayı yeniden yazmak geçerli
    okumaları «bayat» gösteriyordu (2026-09-25: 48 yanlış alarm)."""
    if not yol.exists() or yol.read_text(encoding="utf-8") != metin:
        yol.write_text(metin, encoding="utf-8")


def birlestir(blok: int) -> int:
    kay = P._kaynak()
    plan_b = _blok_kayitlari(blok)
    if not plan_b:
        raise SystemExit(f"⛔ blok {blok} planda yok")
    yeniler, eksik, dusen, degisen = [], [], [], []
    for p in plan_b:
        s = P._json_oku(KURMA / "sonuc" / f"{p['no']}.json")
        if s is None:
            eksik.append(p["no"])
            continue
        eski = kay[p["id"]]
        try:
            yeni = P.uygula(eski, s)
        except (ValueError, KeyError) as e:
            dusen.append((p["no"], f"uygulanamadı: {e}"))
            continue
        sert, _ = P.kayit_kapilari(eski, yeni, p, s)
        if sert:
            dusen.append((p["no"], sert[0]))
        if s.get("bitis_karari") == "degisti":
            degisen.append((eski, yeni))
        yeniler.append(yeni)
    if eksik:
        raise SystemExit(f"⛔ blok {blok}: sonucu olmayan iş {eksik}")
    yol = _aday_yolu(blok)
    yol.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in yeniler),
                   encoding="utf-8")

    rng = random.Random(TOHUM + 100 + blok)
    isler = [(e["id"], "eski", e) for e, _ in degisen] + [(y["id"], "yeni", y) for _, y in degisen]
    rng.shuffle(isler)
    jd = JUDGE / f"b{blok:02d}"
    for d in ("istek", "sonuc"):
        (jd / d).mkdir(parents=True, exist_ok=True)
    kim = []
    for i, (kid, surum, r) in enumerate(isler, 1):
        _yaz_degistiyse(jd / "istek" / f"{i:03d}.txt", _judge_govde(r))
        kim.append({"no": f"{i:03d}", "id": kid, "surum": surum})
    (jd / "kimlikler.json").write_text(json.dumps(kim, ensure_ascii=False, indent=1),
                                       encoding="utf-8")

    kd = KORUNUM / f"b{blok:02d}"
    for d in ("istek", "sonuc"):
        (kd / d).mkdir(parents=True, exist_ok=True)
    sira = list(range(len(yeniler)))
    rng.shuffle(sira)
    kimk = []
    for i, j in enumerate(sira, 1):
        y = yeniler[j]
        _yaz_degistiyse(kd / "istek" / f"{i:02d}.txt", _korunum_metni(kay[y["id"]], y))
        kimk.append({"no": f"{i:02d}", "id": y["id"]})
    (kd / "kimlikler.json").write_text(json.dumps(kimk, ensure_ascii=False, indent=1),
                                        encoding="utf-8")
    print(f"✅ blok {blok}: {yol.relative_to(KOK)} · {len(yeniler)} kayıt · betik kapısından "
          f"düşen {len(dusen)} · bitişi değişen {len(degisen)} → judge {len(isler)} · "
          f"korunum {len(kimk)}")
    for no, neden in dusen:
        print(f"   ⛔ #{no}: {neden}")
    return 0


# ───────────────────── depo: okumalar /tmp'de kalmaz ─────────────────────
# ⛔⛔ 2026-09-25: oturum yeniden başlarken /tmp silindi ve Faz 2'nin ~100 korunum
# okuması yalnız orada durduğu için kayboldu (Kural 7: raporlanan sayının girdisi
# depoda olmalı). Artık her okuma, OKUNAN METNİN SHA'sıyla birlikte depoya yazılır;
# rapor bir okumayı yalnız o SHA kaydın bugünkü metniyle eşleşiyorsa geçerli sayar
# ⇒ metin sonradan değişirse okuma kendiliğinden bayatlar (elle «.bayat» yok).

def _depo_oku(yol: Path) -> list[dict]:
    if not yol.exists():
        return []
    return [json.loads(x) for x in yol.read_text(encoding="utf-8").splitlines() if x.strip()]


def _depo_yaz(yol: Path, satirlar: list[dict]) -> None:
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text("".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n"
                           for x in satirlar), encoding="utf-8")


def depola() -> int:
    """Geçici klasördeki korunum ve judge sonuçlarını depoya taşır (idempotent)."""
    ist_k = P._sha(KOK / "prompts/karar-korunumu.v1.md")
    ist_j = P._sha(KOK / "prompts/judge-eksen1.v9.md")
    kor = {(x["id"], x["metin_sha"]): x for x in _depo_oku(KORUNUM_DEPO)}
    jud = {(x["id"], x["surum"], x["metin_sha"]): x for x in _depo_oku(JUDGE_DEPO)}
    yeni_k = yeni_j = bayat = 0
    for kd in sorted(KORUNUM.glob("b[0-9][0-9]")):
        kim = kd / "kimlikler.json"
        if not kim.exists():
            continue
        for x in json.loads(kim.read_text(encoding="utf-8")):
            ist, son = kd / "istek" / f"{x['no']}.txt", kd / "sonuc" / f"{x['no']}.json"
            if not son.exists() or not ist.exists():
                continue
            if son.stat().st_mtime < ist.stat().st_mtime:
                bayat += 1          # istek sonuçtan sonra yeniden yazılmış: başka metin okunmuş
                continue
            h = P._json_oku(son)
            anahtar = (x["id"], _sha16(ist.read_text(encoding="utf-8")))
            if anahtar not in kor:
                yeni_k += 1
            kor[anahtar] = {"id": x["id"], "blok": int(kd.name[1:]), "metin_sha": anahtar[1],
                            "istem": "karar-korunumu.v1", "istem_sha": ist_k,
                            "okuyan": P.DENETCI, "sonuc": h}
    for jd in sorted(JUDGE.glob("b[0-9][0-9]")):
        kim = jd / "kimlikler.json"
        if not kim.exists():
            continue
        for x in json.loads(kim.read_text(encoding="utf-8")):
            ist, son = jd / "istek" / f"{x['no']}.txt", jd / "sonuc" / f"{x['no']}.json"
            if not son.exists() or not ist.exists() or son.stat().st_mtime < ist.stat().st_mtime:
                continue
            anahtar = (x["id"], x["surum"], _sha16(ist.read_text(encoding="utf-8")))
            if anahtar not in jud:
                yeni_j += 1
            jud[anahtar] = {"id": x["id"], "surum": x["surum"], "blok": int(jd.name[1:]),
                            "metin_sha": anahtar[2], "rubrik": "judge-eksen1.v9",
                            "rubrik_sha": ist_j, "okuyan": P.DENETCI, "ham": P._json_oku(son)}
    _depo_yaz(KORUNUM_DEPO, sorted(kor.values(), key=lambda x: (x["blok"], x["id"], x["metin_sha"])))
    _depo_yaz(JUDGE_DEPO, sorted(jud.values(), key=lambda x: (x["blok"], x["id"], x["surum"])))
    print(f"depo: korunum {len(kor)} (+{yeni_k}) · judge {len(jud)} (+{yeni_j})"
          + (f" · ⚠️ bayat atlandı {bayat}" if bayat else ""))
    return 0


def pilot_tasi() -> int:
    """Bir kerelik: T283'te `v011-pilot.korunum.jsonl`'e SHA'sız yazılmış pilot
    okumalarını depoya taşır — YALNIZ o okumadan bu yana metni değişmemiş kayıtlar
    için. Değişmediği, T283 commit'indeki (5517f9a) aday dosyasıyla bugünkü aynı
    kayıt karşılaştırılarak doğrulanır; değişmişse okuma taşınmaz, kayıt yeniden okunur."""
    import subprocess
    eski_aday = {json.loads(x)["id"]: json.loads(x) for x in subprocess.run(
        ["git", "show", "5517f9a:data/candidates/v011-pilot.jsonl"], cwd=KOK,
        capture_output=True, text=True, check=True).stdout.splitlines() if x.strip()}
    bugun = {json.loads(x)["id"]: json.loads(x) for x in _aday_yolu(0).read_text(
        encoding="utf-8").splitlines() if x.strip()}
    eski_ok = {x["id"]: x for x in _depo_oku(ADAY / "v011-pilot.korunum.jsonl")}
    kay = P._kaynak()
    kor = {(x["id"], x["metin_sha"]): x for x in _depo_oku(KORUNUM_DEPO)}
    tasinan, degismis = 0, []
    for kid, y in bugun.items():
        if kid not in eski_ok:
            continue
        if json.dumps(eski_aday.get(kid), sort_keys=True) != json.dumps(y, sort_keys=True):
            degismis.append(kid)
            continue
        sonuc = {k: v for k, v in eski_ok[kid].items() if k not in ("id", "_okuyan", "_istem")}
        sha = _sha16(_korunum_metni(kay[kid], y))
        kor[(kid, sha)] = {"id": kid, "blok": 0, "metin_sha": sha, "istem": "karar-korunumu.v1",
                           "istem_sha": "T283-oncesi", "okuyan": eski_ok[kid].get("_okuyan", P.DENETCI),
                           "kaynak": "T283 pilot okuması; metin o günden beri değişmedi (5517f9a)",
                           "sonuc": sonuc}
        tasinan += 1
    _depo_yaz(KORUNUM_DEPO, sorted(kor.values(), key=lambda x: (x["blok"], x["id"], x["metin_sha"])))
    print(f"pilot: {tasinan} okuma taşındı · metni değişmiş {len(degismis)} (yeniden okunacak)")
    return 0


def geri_yukle() -> int:
    """Geçici klasörü depodan yeniden kurar: istekler, sonuçlar, korunum/judge işleri."""
    kay, plan_t = P._kaynak(), _plan_tum()
    for d in ("istek", "sonuc"):
        (KURMA / d).mkdir(parents=True, exist_ok=True)
    no = {p["id"]: p["no"] for p in plan_t}
    for p in plan_t:
        r = kay[p["id"]]
        gm = r["gen_meta"]
        (KURMA / "istek" / f"{p['no']}.json").write_text(json.dumps(
            {"no": p["no"], "bitis_adayi": p["bitis_adayi"], "aday_nedeni": p["aday_nedeni"],
             "meta": {k: gm.get(k) for k in ("konusma_durumu", "turn_ending", "bicim",
                                             "baglam_davranisi")}
             | {k: r[k] for k in ("slice", "talk_type", "mi_process", "age_group")},
             "konusma": [{"rol": m["role"], "metin": m["content"]} for m in r["messages"]],
             "eski_thinking": P._son(r).get("thinking")},
            ensure_ascii=False, indent=1), encoding="utf-8")
    bloklar = []
    for b in sorted({p["blok"] for p in plan_t}):
        yol = _aday_yolu(b)
        if not yol.exists():
            continue
        bloklar.append(b)
        for x in yol.read_text(encoding="utf-8").splitlines():
            if not x.strip():
                continue
            y = json.loads(x)
            kur = y["gen_meta"]["yeniden_kurma"]
            (KURMA / "sonuc" / f"{no[y['id']]}.json").write_text(json.dumps(
                {"no": no[y["id"]], "thinking": P._son(y)["thinking"],
                 "bitis_karari": kur.get("bitis_karari"),
                 "korunan_soru_turu": kur.get("korunan_soru_turu"),
                 "bitis_gerekcesi": kur.get("bitis_gerekcesi"),
                 "son_cumle": kur.get("son_cumle"),
                 "turn_ending": y["gen_meta"].get("turn_ending"),
                 "korunan_kararlar": kur.get("korunan_kararlar")},
                ensure_ascii=False, indent=1), encoding="utf-8")
    for b in bloklar:
        birlestir(b)
    # geçerli okumaları geri koy (okunacak olanlar boş kalsın)
    kor = {(x["id"], x["metin_sha"]): x for x in _depo_oku(KORUNUM_DEPO)}
    jud = {(x["id"], x["surum"], x["metin_sha"]): x for x in _depo_oku(JUDGE_DEPO)}
    eksik = collections.Counter()
    for b in bloklar:
        kd, jd = KORUNUM / f"b{b:02d}", JUDGE / f"b{b:02d}"
        for x in json.loads((kd / "kimlikler.json").read_text(encoding="utf-8")):
            v = kor.get((x["id"], _sha16((kd / "istek" / f"{x['no']}.txt").read_text(encoding="utf-8"))))
            if v:
                (kd / "sonuc" / f"{x['no']}.json").write_text(
                    json.dumps(v["sonuc"], ensure_ascii=False, indent=1), encoding="utf-8")
            else:
                eksik[f"korunum b{b:02d}"] += 1
        for x in json.loads((jd / "kimlikler.json").read_text(encoding="utf-8")):
            v = jud.get((x["id"], x["surum"], _sha16((jd / "istek" / f"{x['no']}.txt").read_text(encoding="utf-8"))))
            if v:
                (jd / "sonuc" / f"{x['no']}.json").write_text(
                    json.dumps(v["ham"], ensure_ascii=False, indent=1), encoding="utf-8")
            else:
                eksik[f"judge b{b:02d}"] += 1
    print(f"✅ geri yüklendi: {len(plan_t)} istek · bloklar {bloklar}")
    print("   okunması gereken:", dict(eksik) if eksik else "yok")
    return 0


def rapor() -> int:
    depola()
    kay, plan_t = P._kaynak(), _plan_tum()
    kor = {(x["id"], x["metin_sha"]): x["sonuc"] for x in _depo_oku(KORUNUM_DEPO)}
    jud = {(x["id"], x["surum"], x["metin_sha"]): x["ham"] for x in _depo_oku(JUDGE_DEPO)}
    yeniler: dict[str, dict] = {}
    bloklar = sorted({p["blok"] for p in plan_t})
    hazir = []
    for b in bloklar:
        yol = _aday_yolu(b)
        if not yol.exists():
            continue
        hazir.append(b)
        for x in yol.read_text(encoding="utf-8").splitlines():
            if x.strip():
                r = json.loads(x)
                yeniler[r["id"]] = r
    t15 = _modul("_t15", "scripts/analiz/2026-09-15-judge-sonuclari-topla.py")
    t15.JUDGE_ADI, t15.RUBRIK = P.DENETCI, "judge-eksen1.v9"

    satir, okunmamis = [], []
    for p in plan_t:
        if p["id"] not in yeniler:
            continue
        e, y = kay[p["id"]], yeniler[p["id"]]
        b = p["blok"]
        kur = y["gen_meta"]["yeniden_kurma"]
        s = {k: kur.get(k) for k in ("korunan_kararlar", "bitis_karari", "son_cumle",
                                     "korunan_soru_turu")}
        sert, inc = P.kayit_kapilari(e, y, p, s)
        k = kor.get((p["id"], _sha16(_korunum_metni(e, y))))
        okundu = k is not None
        if not okundu:
            okunmamis.append(p["no"])
        else:
            sert += [f"korunum: karar düştü — «{(x.get('eski') or '')[:50]}»"
                     for x in k.get("kararlar", []) if x.get("durum") == "dustu"]
            sert += [f"korunum: uydurma — «{(x.get('parca') or '')[:50]}»"
                     for x in k.get("uydurma", [])]
            sert += [f"korunum: tutarsızlık — «{(x.get('parca') or '')[:50]}»"
                     for x in k.get("tutarsizlik", [])]
            sert += [f"korunum: biçim — {x.get('tur')}" for x in k.get("bicim_ihlali", [])]
            inc += [f"korunum: kısmen — «{(x.get('eski') or '')[:50]}»"
                    for x in k.get("kararlar", []) if x.get("durum") == "kismen"]
            bt = k.get("bitis") or {}
            if s["bitis_karari"] == "degisti":
                if bt.get("korunan_soru_cikarildi"):
                    sert.append("korunum: korunan soru çıkarılmış")
                if bt.get("ovgu_ya_da_atif"):
                    sert.append("korunum: övgü ya da atıf")
                if bt.get("uygun") is False:
                    sert.append("korunum: bitiş duruma uygun değil")
        if s["bitis_karari"] == "degisti":
            he = jud.get((p["id"], "eski", _sha16(_judge_govde(e))))
            hy = jud.get((p["id"], "yeni", _sha16(_judge_govde(y))))
            je, jy = (t15.turet(he) if he else {}), (t15.turet(hy) if hy else {})
            if jy:
                if jy.get("klinik_guvenlik_ihlali") or jy.get("rol_siniri_ihlali"):
                    sert.append("judge: güvenlik ya da rol sınırı ihlali")
                for alan in ("grounding", "mi_uyumu"):
                    if (jy.get(alan) or 0) < (je.get(alan) or 0):
                        sert.append(f"judge: {alan} düştü {je.get(alan)}→{jy.get(alan)}")
                if len(jy.get("tuzak_ihlali") or []) > len(je.get("tuzak_ihlali") or []):
                    sert.append("judge: yeni tuzak")
        satir.append({"p": p, "e": e, "y": y, "sert": sert, "inc": inc,
                      "bk": s["bitis_karari"], "okundu": okundu})

    # ⛔ Okunmamış kayıt KABUL SAYILMAZ (K260). Betik kapıları biçimi tutar ama
    # karar kaybını, anlam kaymasını ve uydurmayı yalnız korunum okuması görür.
    kabul = [x for x in satir if not x["sert"] and x["okundu"]]
    s = ["# `v0.1.1` yeniden kurma — pilot (blok 0) + Faz 2", "",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {betik_tarihi(__file__)}  ",
         f"**Girdi:** `data/judged/v0.0.22.jsonl` SHA256-16 `{P.KAYNAK_SHA}` · plan "
         f"`data/plan/v011-faz2.jsonl` SHA256-16 `{P._sha(PLAN)}` · talimat `prompts/uretim-v6.md` "
         f"SHA256-16 `{P._sha(KOK / 'prompts/uretim-v6.md')}`  ",
         f"**Okumalar:** `{KORUNUM_DEPO.relative_to(KOK)}` · `{JUDGE_DEPO.relative_to(KOK)}` — "
         "okunan metnin SHA'sıyla; metni sonradan değişen kaydın okuması geçersiz sayılır  ",
         f"**Taslak:** alt ajan · **okuma ve revizyon:** Claude Code (K260) · "
         f"**korunum okuması ve judge:** `{P.DENETCI}`", "",
         f"**Koşulan blok:** {len(hazir)}/{len(bloklar)} · **işlenen kayıt:** {len(satir)}"
         f"/{len(plan_t)}", "",
         f"## Sonuç: {len(kabul)}/{len(satir)} kabul", "",
         f"pilot (blok 0): {sum(1 for x in kabul if x['p']['blok'] == 0)}"
         f"/{sum(1 for x in satir if x['p']['blok'] == 0)} · Faz 2: "
         f"{sum(1 for x in kabul if x['p']['blok'] > 0)}/{sum(1 for x in satir if x['p']['blok'] > 0)}", "",
         "| kapı | düşen kayıt |", "|---|---:|"]
    for ad in ("zarf", "temizlik", "run_checks", "eşleme", "bitiş", "korunum", "judge"):
        s.append(f"| {ad} | {sum(1 for x in satir if any(z.startswith(ad) for z in x['sert']))} |")
    s.append(f"| **korunum okuması yok** | {len(okunmamis)} |")
    if okunmamis:
        s += ["", f"⛔ **Korunum okuması yapılmamış kayıt: {len(okunmamis)}** — bunlar yalnız "
                  "betik kapılarından geçti ve **kabul sayılmadı**; yukarıdaki orana dahil "
                  f"değiller. Numaralar: {', '.join(okunmamis)}."]
    s += ["", "⭐ Reddedilen yeniden kurma kaydı kaybettirmez: kayıt `v0.1.0` hâliyle kalır.", ""]

    s += ["## Düşünme — eski ↔ yeni", "", "| ölçü | eski | yeni |", "|---|---:|---:|"]
    oe = P._olcu([P._son(x["e"])["thinking"] for x in satir])
    oy = P._olcu([P._son(x["y"])["thinking"] for x in satir])
    s += [f"| {k} | {oe[k]} | {oy[k]} |" for k in oe]
    oran = lambda r: len(P._son(r)["thinking"]) / max(1, len(P._son(r)["content"]))
    par = lambda r: len(P._son(r)["thinking"].split("\n\n"))
    tekp = lambda f: 100 * sum(par(x[f]) == 1 for x in satir) / max(1, len(satir))
    s += [f"| düşünme : cevap (karakter, ortanca) | {st.median(oran(x['e']) for x in satir):.1f}x | "
          f"{st.median(oran(x['y']) for x in satir):.1f}x |",
          f"| paragraf (ortanca) | {st.median(par(x['e']) for x in satir):.0f} | "
          f"{st.median(par(x['y']) for x in satir):.0f} |",
          f"| tek paragraf olan | {tekp('e'):.0f}% | {tekp('y'):.0f}% |",
          "| paragraf dağılımı | "
          + " · ".join(f"{k}:{v}" for k, v in sorted(collections.Counter(
              par(x["e"]) for x in satir).items()))
          + " | "
          + " · ".join(f"{k}:{v}" for k, v in sorted(collections.Counter(
              par(x["y"]) for x in satir).items())) + " |", "",
          f"| eski↔yeni paragraf korelasyonu | — | r = {_kor([par(x['e']) for x in satir], [par(x['y']) for x in satir]):+.2f} |", "",
          "⚠️ **Paragraf satırı neden var:** Faz 2'nin ilk taslak bloğunda 25 kaydın 25'i de tek "
          "paragraf geldi; `uretim-v6` o sırada paragraflama konusunda sessizdi. `v0.1.0`'ın eski "
          "düşünmelerinde ortanca 4 paragraf var ve %87'si çok paragraflı ⇒ tek paragraf korpusta "
          "görünür bir biçim ayrışması üretirdi. Kural §1d'ye yazıldı; bu satır onu denetliyor.", ""]

    # ⚠️ 2026-09-25: bazı taslak blokları eski düşünmeyi işaretlerini söküp neredeyse aynen
    # taşıdı (blok 2 ortanca 0,79). K277 yapıyı değiştirmeyi hedefliyor; bu ölçü onu izler.
    # Sözcük dizisi üzerinde difflib oranı: 1 = birebir aynı, 0 = ortak dizi yok.
    ben = lambda x: difflib.SequenceMatcher(None, P._son(x["e"])["thinking"].split(),
                                            P._son(x["y"])["thinking"].split()).ratio()
    s += ["### Eski metne yakınlık (sözcük dizisi benzerliği)", "",
          "| blok | kayıt | ortanca | ≥ 0,6 |", "|---|---:|---:|---:|"]
    for b in hazir:
        v = [ben(x) for x in satir if x["p"]["blok"] == b]
        if v:
            s.append(f"| {b} | {len(v)} | {st.median(v):.2f} | {sum(z >= 0.6 for z in v)} |")
    v = [ben(x) for x in satir]
    s += [f"| **tümü** | {len(v)} | {st.median(v):.2f} | {sum(z >= 0.6 for z in v)} |", "",
          "⚠️ Yüksek benzerlik tek başına kusur değildir (kararlar aynı kalmalı), ama ⛔/⭐ ve "
          "iskele söküldükten sonra cümleler olduğu gibi duruyorsa K277'nin yapı hedefi "
          "(kişi → çerçeve → hamle) o kayıtta uygulanmamış demektir.", ""]

    ad_ = [x for x in satir if x["p"]["bitis_adayi"]]
    s += [f"## Tur sonu — {len(ad_)} bitiş adayı", "", "| karar | kayıt |", "|---|---:|"]
    for k2, n in collections.Counter(x["bk"] for x in ad_).most_common():
        s.append(f"| `{k2}` | {n} |")
    s += ["", "## Redler", "", "| no | blok | aday | bitiş | sebep |", "|---|---:|---|---|---|"]
    for x in sorted((x for x in satir if x["sert"]), key=lambda x: x["p"]["no"]):
        s.append(f"| {x['p']['no']} | {x['p']['blok']} | {x['p']['aday_nedeni'] or '—'} | "
                 f"`{x['bk']}` | {x['sert'][0].replace('|', '/')} |")
    s += ["", "## ⛔ Bunun söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ **Model başarımı hakkında bir şey söylemez** | eğitim yok |",
          "| ⛔ **Korunum okuması tek okuyucu** | tekrar yok ⇒ gürültü tabanı bilinmiyor |",
          "| ⛔⛔ **Eşli judge KÖR DEĞİL** | iç muhakeme hangisinin yeni sürüm olduğunu ele "
          "veriyor (T282); Faz 3 ön kaydında kapatılmalı |",
          "| ⚠️ **Taslağı alt ajan yazdı** | K260 — her kayıt Claude Code tarafından okundu ve "
          "revize edildi; tezde yazarlık böyle beyan edilir |",
          "| ⚠️ **Bitiş adaylığı `konusma_durumu` etiketinden geliyor** | etiket bir kısım kayıtta "
          "içeriğe uymuyor (T282) |"]
    RAPOR.write_text("\n".join(s) + "\n", encoding="utf-8")
    print("\n".join(s[:22]))
    print(f"\nyazıldı: {RAPOR.relative_to(KOK)}")
    return 0


def _kor(a: list[int], b: list[int]) -> float:
    """Pearson r. ⭐ Paragraf sayısı KAYITTAN mı YAZANDAN mı geliyor, onu ölçer:
    r 0'a yakınsa yeni metnin paragraf sayısı kaydın karmaşıklığından değil,
    o bloğu yazan ajanın alışkanlığından geliyor demektir (§1d)."""
    n = len(a)
    if n < 2:
        return 0.0
    ma, mb = sum(a) / n, sum(b) / n
    sa = (sum((x - ma) ** 2 for x in a) / n) ** 0.5
    sb = (sum((x - mb) ** 2 for x in b) / n) ** 0.5
    if not sa or not sb:
        return 0.0
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (n * sa * sb)


YAKINLIK_TAVANI = 0.6
_T281 = None


def _olumsuz(metin: str) -> float:
    """Olumsuz karar cümlesi payı (%) — raporun `_olcu` ölçüsünün kayıt düzeyi."""
    global _T281
    if _T281 is None:
        _T281 = _modul("_t281", "scripts/analiz/2026-09-24-tur-sonu-ve-dusunme.py")
    from tohum_guvenlik import tr_fold
    cum = [c for c in _T281.cumle_bol(metin) if len(c.split()) >= 2]
    return 100 * sum(bool(_T281.OLUMSUZ.search(tr_fold(c))) for c in cum) / max(1, len(cum))


def kontrol(nolar: list[str]) -> int:
    """Taslağın betik kapıları — alt ajan kendi işini bununla sınar."""
    kay, plan = P._kaynak(), {p["no"]: p for p in _plan_tum()}
    for no in nolar:
        p = plan.get(no)
        if p is None:
            print(f"#{no} ⛔ planda yok"); continue
        try:
            s = P._json_oku(KURMA / "sonuc" / f"{no}.json")
        except Exception as ex:
            print(f"#{no} ⛔ JSON okunamadı: {ex}"); continue
        if s is None:
            print(f"#{no} — sonuç yok"); continue
        e = kay[p["id"]]
        try:
            y = P.uygula(e, s)
        except Exception as ex:
            print(f"#{no} ⛔ uygulanamadı: {ex}"); continue
        sert, inc = P.kayit_kapilari(e, y, p, s)
        th, c = P._son(y)["thinking"], P._son(y)["content"]
        eth = P._son(e)["thinking"]
        # ⛔ 2026-09-25 (kullanıcı kararı): eski düşünmeyi işaretlerini söküp aynen taşıyan
        # taslak yeniden kurulmamıştır. Yalnız taslak kapısı — birleştirmeyi etkilemez.
        ben = difflib.SequenceMatcher(None, eth.split(), th.split()).ratio()
        if ben >= YAKINLIK_TAVANI:
            sert = sert + [f"eski metne çok yakın (benzerlik {ben:.2f} ≥ {YAKINLIK_TAVANI}): "
                           "cümleleri taşıma, kararı bu konuşmaya bakarak yeniden kur"]
        print(f"#{no} {'⛔' if sert else '✅'} sözcük {len(eth.split())}→"
              f"{len(th.split())} · oran {len(th)/len(c):.1f}x (tavan 4.0) · paragraf "
              f"{len(eth.split(chr(10)*2))}→{len(th.split(chr(10)*2))} · "
              f"benzerlik {ben:.2f} · olumsuz cümle %{_olumsuz(eth):.0f}→%{_olumsuz(th):.0f} · "
              f"bitiş {s.get('bitis_karari')}")
        if _olumsuz(th) >= 30 and _olumsuz(th) >= _olumsuz(eth):
            inc = inc + ["olumsuz karar payı düşmedi: kararların bir kısmını olumlu kur "
                         "(ne yapıyorum, neyi seçiyorum, neden)"]
        for x in sert:
            print("   ⛔", x)
        for x in inc:
            print("   ⚠️", x)
    return 0


def oku(nolar: list[str]) -> int:
    """TAM okuma (K260): kullanıcı turları + cevap + eski/yeni düşünme, KESİLMEDEN.
    ⛔ 2026-09-24: çıktıyı karakterle kesmek bir uydurmayı (#0053) kaçırttı."""
    import re
    kay, plan = P._kaynak(), {p["no"]: p for p in _plan_tum()}
    bag = re.compile(r"(<context[^>]*>|\[BAĞLAM[^\]]*\]|\{bağlam[^}]*\}|--- KAYNAK[^-]*---)"
                     r"(.|\n)*?(</context>|\[BAĞLAM SONU\]|\{bağlam sonu\}|--- KAYNAK SONU ---)")
    for no in nolar:
        p = plan[no]
        e = kay[p["id"]]
        s = P._json_oku(KURMA / "sonuc" / f"{no}.json")
        gm = e["gen_meta"]
        print(f"===== #{no} · aday={p['bitis_adayi']} ({p['aday_nedeni']}) · {e['slice']} · "
              f"{gm.get('konusma_durumu')} · te={gm.get('turn_ending')} · {e['age_group']}")
        msj = [m for m in e["messages"] if m["role"] != "system"]
        for m in msj[:-1]:
            print(f"  [{m['role'][:4]}] {bag.sub('[bağlam belgesi]', m['content'])}")
        print(f"  >>CEVAP: {msj[-1]['content']}")
        print(f"  --ESKİ: {P._son(e).get('thinking')}")
        if s:
            print(f"  --YENİ: {s['thinking']}")
            if s.get("son_cumle"):
                print(f"  --BİTİŞ: {s['son_cumle']['eski']} → {s['son_cumle']['yeni']}")
        print()
    return 0


if __name__ == "__main__":
    adim = sys.argv[1] if len(sys.argv) > 1 else ""
    if adim not in ("plan", "birlestir", "depola", "geri_yukle", "rapor", "kontrol", "oku",
                    "pilot_tasi"):
        raise SystemExit("kullanım: <betik> plan|birlestir <blok>|depola|geri_yukle|rapor|"
                         "kontrol <no…>|oku <no…>")
    if adim in ("kontrol", "oku"):
        raise SystemExit({"kontrol": kontrol, "oku": oku}[adim](sys.argv[2:]))
    if not SCRATCH.exists():
        raise SystemExit("⛔ BIRAG_SCRATCH tanımlı değil ya da yok")
    if adim == "birlestir":
        if len(sys.argv) < 3:
            raise SystemExit("kullanım: <betik> birlestir <blok>")
        raise SystemExit(birlestir(int(sys.argv[2])))
    raise SystemExit({"plan": plan, "depola": depola, "geri_yukle": geri_yukle,
                      "rapor": rapor, "pilot_tasi": pilot_tasi}[adim]())
