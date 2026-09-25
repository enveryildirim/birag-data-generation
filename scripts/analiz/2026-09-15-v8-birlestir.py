#!/usr/bin/env python3
"""v8 judge sonuçlarını toplar, TÜRETİR ve v7 ile eşleştirir.

Türetme `filter.py`'den İMPORT EDİLİR, kopyalanmaz — v7 birleştirmesiyle aynı gerekçe:
kopyalasaydım v7↔v8 farkı rubrik farkı değil **hesap farkı** olurdu.

Çıktı:
  reports/analiz/eksen2-judge-v8/<kol>/sonuclar.jsonl   — v8 + v7 aşama 1 yan yana
  reports/analiz/eksen2-judge-v8/ayrisma-kumesi.json    — --hakemlik ile

Kullanım:
  uv run python scripts/analiz/2026-09-15-v8-birlestir.py
  uv run python scripts/analiz/2026-09-15-v8-birlestir.py --hakemlik
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import filter as f  # noqa: E402
from schemas import JudgeResult  # noqa: E402

_sp = _iu.spec_from_file_location("plan", KOK / "scripts/analiz/2026-09-15-v8-kosu-plan.py")
PLAN = _iu.module_from_spec(_sp)
_sp.loader.exec_module(PLAN)

ISLER = PLAN.ISLER
KOSU = KOK / "reports/analiz/eksen-kosu"
V7 = KOK / "reports/analiz/eksen2-judge"
HEDEF = KOK / "reports/analiz/eksen2-judge-v8"
SET1 = KOK / "evals/safety_crisis.jsonl"
SET2 = KOK / "evals/safety_crisis.duzeltilmis.jsonl"
IKINCI = KOK / "reports/analiz/ikinci-set"

JUDGE_ADI = "claude-sonnet-subagent"
RUBRIK = "judge-eksen1.v8"
ALANLAR = ["rol_siniri_ihlali", "bos_guvence", "tuzak_suclama"]

HARITA = {
    "e2-5ae67873": ("taban",    "20260915-105829-safety_crisis-baseline-1"),
    "e2-b7584bec": ("A-dar",    "20260915-140907-sc2-A-dar"),
    "e2-220c3b5a": ("B-derin",  "20260915-141354-sc2-B-derin"),
    "e2-99b69ab4": ("C-dikkat", "20260915-141743-sc2-C-dikkat"),
    "e2-7ac7e984": ("D-tam",    "20260915-142010-sc2-D-tam"),
    "e2-ceef5655": ("E-genis",  "20260915-142308-sc2-E-genis"),
}
# v8'in EK alanları — Ö6 (doluluk oranı) bunları sayıyor.
V8_ALAN = ["rol_risk_olasilik_olarak", "rol_kaynak_turu", "teselli_islevi",
           "teselli_kullanici_alintisi", "kurum_yordam_en_yakin", "kurum_adi",
           "kurum_adi_kullanicidan", "yordam_iddiasi", "yordam_baglamdan",
           "yordam_baglam_alintisi"]


def turet(data: dict) -> dict:
    data["judge_model"] = JUDGE_ADI
    data["prompt_version"] = RUBRIK
    f.f_bolumu_turet(data)
    for alan, hesap in (("anlasilirlik", f.anlasilirlik_hesapla),
                        ("dogallik", f.dogallik_hesapla),
                        ("mi_uyumu", f.mi_uyumu_hesapla)):
        d = hesap(data)
        if d is not None:
            data[alan] = d
    if any(k in data for k in f.TUZAKLAR):
        data["tuzak_ihlali"] = [ad for k, ad in f.TUZAKLAR.items() if data.get(k) is True]
    return JudgeResult(**data).model_dump()


def oku(dizin: Path) -> tuple[dict, list, list, dict]:
    kimlikler = json.loads((dizin / "kimlikler.json").read_text())
    sonuc, eksik, bozuk, ham_alan = {}, [], [], {}
    for k in kimlikler:
        yol = dizin / "sonuc" / f"{k['no']}.json"
        if not yol.exists():
            eksik.append(k["no"]); continue
        try:
            ham = yol.read_text().strip()
            if ham.startswith("```"):
                ham = ham.split("```")[1].removeprefix("json").strip()
            d = json.loads(ham)
            ham_alan[k["id"]] = {a: (a in d) for a in V8_ALAN}
            sonuc[k["id"]] = turet(d)
        except Exception as e:
            bozuk.append((k["no"], f"{type(e).__name__}: {e}"[:120]))
    return sonuc, eksik, bozuk, ham_alan


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hakemlik", action="store_true")
    a = ap.parse_args()

    ogeler = {o["id"]: o for o in (json.loads(l) for l in open(SET1) if l.strip())}
    sira = list(ogeler)
    beklenen = {oid: [i["alan"] for i in o["iddialar"] if i.get("tip") == "judge"]
                for oid, o in ogeler.items()}
    set2 = {o["kaynak_oge"]: o for o in (json.loads(l) for l in open(SET2) if l.strip())}
    del set2

    HEDEF.mkdir(parents=True, exist_ok=True)
    ozet, ayrisan, tum = [], [], {}
    for etiket, (kol, dizin) in HARITA.items():
        judge, eksik, bozuk, ham_alan = oku(ISLER / f"v8-{etiket}")
        v7 = {json.loads(l)["id"]: json.loads(l)
              for l in open(V7 / kol / "sonuclar.jsonl")}
        oto2 = {r["kaynak_oge"]: r for r in
                (json.loads(l) for l in open(IKINCI / dizin / "sonuclar.jsonl"))}
        satirlar = []
        for r in (json.loads(l) for l in open(KOSU / dizin / "sonuclar.jsonl")):
            oid = r["id"]
            j = judge.get(oid)
            s = {"id": oid, "kutup": r.get("kutup"), "dilim": r.get("dilim"),
                 "cevap": r["cevap"], "judge_alanlari": beklenen[oid],
                 "otomatik_gecti_set1": r["otomatik_gecti"],
                 "otomatik_gecti_set2": oto2[oid]["otomatik_gecti"],
                 "judge_v8": j,
                 "v8_alan_dolu": ham_alan.get(oid),
                 "v7_dusuren": v7[oid]["judge_dusuren"],
                 "v7_gecti": v7[oid]["judge_gecti"]}
            if j is None:
                s["v8_dusuren"] = []
                s["v8_gecti"] = None if r["cevap"].strip() else False
            else:
                dus = [al for al in beklenen[oid] if j.get(al) is True]
                s["v8_dusuren"] = dus
                s["v8_gecti"] = not dus
                s["kurum_yordam_ihlali"] = j.get("kurum_yordam_ihlali")
            # v7 ile v8 AYRIŞIYOR mu — iddia edilen alanların herhangi birinde
            s["ayrisma"] = (j is not None
                            and set(s["v7_dusuren"]) != set(s["v8_dusuren"]))
            if s["ayrisma"]:
                ayrisan.append({"kol": kol, "id": oid, "rol": "ayrisan",
                                "v7": sorted(s["v7_dusuren"]),
                                "v8": sorted(s["v8_dusuren"])})
            satirlar.append(s)
        tum[kol] = {s["id"]: s for s in satirlar}
        d = HEDEF / kol
        d.mkdir(parents=True, exist_ok=True)
        (d / "sonuclar.jsonl").write_text(
            "".join(json.dumps(s, ensure_ascii=False) + "\n" for s in satirlar))
        (d / "kosu.json").write_text(json.dumps(
            {"kol": kol, "kaynak_kosu": dizin, "kor_etiket": f"v8-{etiket}",
             "judge_model": JUDGE_ADI, "judge_rubrik": RUBRIK, "k": 1,
             "judge_toplandi": len(judge), "eksik": eksik, "bozuk": bozuk,
             "karsilastirma": "reports/analiz/eksen2-judge (v7, aşama 1, k=1)",
             "tarih": datetime.now().isoformat(timespec="seconds")},
            ensure_ascii=False, indent=1))
        ozet.append((kol, len(judge), len(eksik), len(bozuk)))

    print(f"{'kol':10} {'toplandı':>8} {'eksik':>6} {'bozuk':>6}")
    for kol, n, e, b in ozet:
        print(f"{kol:10} {n:>8} {e:>6} {b:>6}")
    print(f"\nv7 ile AYRIŞAN öğe: {len(ayrisan)}")

    if a.hakemlik:
        # İki yönlü küme: ayrışan + eşit sayıda eşleştirilmiş AYRIŞMAYAN kontrol.
        # Kontrol, mühürlü set kimlik sırasında bir sonraki ayrışmayan öğe (sararak).
        kume, secilen = [], set()
        for x in ayrisan:
            kume.append(x)
            secilen.add((x["kol"], x["id"]))
        for x in ayrisan:
            kol = x["kol"]
            i = sira.index(x["id"])
            for adim in range(1, len(sira) + 1):
                aday = sira[(i + adim) % len(sira)]
                s = tum[kol].get(aday)
                if (s and not s["ayrisma"] and s["judge_v8"] is not None
                        and (kol, aday) not in secilen):
                    kume.append({"kol": kol, "id": aday, "rol": "kontrol",
                                 "v7": sorted(s["v7_dusuren"]),
                                 "v8": sorted(s["v8_dusuren"])})
                    secilen.add((kol, aday))
                    break
        (HEDEF / "ayrisma-kumesi.json").write_text(
            json.dumps(kume, ensure_ascii=False, indent=1))
        n_a = sum(1 for x in kume if x["rol"] == "ayrisan")
        n_k = sum(1 for x in kume if x["rol"] == "kontrol")
        print(f"hakemlik kümesi: {n_a} ayrışan + {n_k} kontrol = {len(kume)} öğe "
              f"→ {(HEDEF / 'ayrisma-kumesi.json').relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
