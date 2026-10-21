#!/usr/bin/env python3
"""Haiku pilotu tasarım ızgarası — **60 kayıt**. Üretimden ÖNCE yazılır, dondurulur.

⭐ Amaç ölçek değil ÖLÇÜM: taslak yazarı Opus yerine Haiku olduğunda K260
rejiminin (alt ajan taslak, Claude Code okur ve kapılardan geçirir) kusur
oranı ne olur. Hacim 5-10 bine çıkarılacaksa önce bu sayı gerekir.

⛔ Bu ızgara kapsama-açığı hedeflemesi YAPMAZ (parti8 planının zinciri
kurulmadı). Tasarım sütunları `v6-parti8` ızgarasından 60 satırlık rastgele
örneklemle alınır ⇒ dağılım, kıyas zemini olan partiyle aynı ailedendir.
Tohum, satırın `tur` + `yas` değerini taşıyan ve HİÇ kullanılmamış
(`data/plan/*`, `data/candidates/*`, `datasets/v0.1.1`) bir tohumdur.
`bicim` tohum boyuna uymuyorsa (kırpma uzatamaz) satır bir alt banda iner
ve bu `izgara_sapmasi` olarak yazılır.

Çıktı: data/plan/haiku-pilot.jsonl · reports/analiz/2026-10-20-haiku-pilot-plan.md
"""
from __future__ import annotations

import collections
import glob
import hashlib
import json
import random
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
N = 60
TOHUM = 20261020
KAYNAK_PLAN = KOK / "data/plan/v6-parti8.jsonl"
HAVUZ = KOK / "data/seeds.v2.jsonl"
CIKTI = KOK / "data/plan/haiku-pilot.jsonl"
RAPOR = KOK / "reports/analiz/2026-10-20-haiku-pilot-plan.md"

# uretim-v5 §1c
MOTIVASYON = {"ic_motivasyon": "ic", "aile_baskisi": "aile_baskisi",
              "yasal_zorunluluk": "yasal_zorunluluk",
              "tetikleyici_olay": "ic", "duygusal_regulasyon": "ic"}
TASARIM = ("bicim", "register", "turn_ending", "mi_process", "turn_type",
           "konusma_durumu", "sinir_tipi", "senaryo_hedefi", "is_negative",
           "ozerklik", "context", "baglam_davranisi")
BANT_MIN = {"kisa": 1, "orta": 9, "uzun": 26}
ALT = {"uzun": "orta", "orta": "kisa"}


def _modul(ad: str, yol: str):
    sp = _iu.spec_from_file_location(ad, KOK / yol)
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def _kullanilmis() -> set[str]:
    s: set[str] = set()
    for f in glob.glob(str(KOK / "data/plan/*.jsonl")) + glob.glob(str(KOK / "data/candidates/*.jsonl")):
        if Path(f).name.startswith("haiku-pilot"):
            continue
        for l in open(f, encoding="utf-8"):
            if not l.strip():
                continue
            r = json.loads(l)
            for k in (r.get("seed_id"), (r.get("gen_meta") or {}).get("seed_id")):
                if k:
                    s.add(k)
    for l in open(KOK / "datasets/v0.1.1/train.jsonl", encoding="utf-8"):
        k = (json.loads(l).get("gen_meta") or {}).get("seed_id")
        if k:
            s.add(k)
    return s


def main() -> int:
    rng = random.Random(TOHUM)
    kaynak = [json.loads(l) for l in KAYNAK_PLAN.read_text(encoding="utf-8").splitlines() if l.strip()]
    satirlar = rng.sample(kaynak, N)
    kullanilmis = _kullanilmis()
    havuz = [json.loads(l) for l in HAVUZ.read_text(encoding="utf-8").splitlines() if l.strip()]
    serbest = [t for t in havuz if t["seed_id"] not in kullanilmis and t.get("turn_count", 1) == 1]
    # ⛔ KRİZ SÜZGEÇLERİ (K23, Kural 3) — v5 planlarının üçü, aynı sırayla:
    #    açık ifade (P1) · dolaylı ifade (KZ) · tohumun kendi beyanı (BK).
    #    Ek olarak `senaryo: kriz` beyanlı tohum hiç alınmaz.
    P1 = _modul("p1", "scripts/analiz/2026-09-15-v4-parti1-plan.py")
    KZ = _modul("kz", "scripts/analiz/2026-09-17-kriz-suzgeci-yanlis-negatif.py")
    BK = _modul("bk", "scripts/analiz/2026-09-17-tohum-beyan-kriz-kapisi.py")
    _once = len(serbest)
    serbest = [t for t in serbest if t["meta"].get("senaryo") != "kriz"
               and not P1.KRIZ_ANAHTAR.search(t["user_message"])
               and not KZ.DOLAYLI.search(t["user_message"]) and BK._sinif(t) != "sert"]
    kriz_elenen = _once - len(serbest)
    rng.shuffle(serbest)

    plan, alinan, sapma = [], set(), 0
    for i, s in enumerate(satirlar, 1):
        aday = [t for t in serbest if t["seed_id"] not in alinan
                and t["meta"]["bagimlilik_turu"] == s["tur"] and t["meta"]["yas_grubu"] == s["yas"]]
        if not aday:
            raise SystemExit(f"#{i}: {s['tur']}/{s['yas']} için serbest tohum kalmadı")
        t = max(aday[:5], key=lambda x: len(x["user_message"].split()))
        alinan.add(t["seed_id"])
        satir = {"sira": i, **{k: s.get(k) for k in TASARIM},
                 "tur": s["tur"], "yas": s["yas"], "havuz": None,
                 "seed_id": t["seed_id"], "source_id": t["source_id"],
                 "tohum_senaryo": t["meta"]["senaryo"],
                 "tohum_kelime": len(t["user_message"].split()),
                 "tohum_metin": t["user_message"],
                 "tohum_baglam": t.get("scenario_context"),
                 "motivasyon": MOTIVASYON.get(t["meta"]["motivasyon"], "ic"),
                 "motivasyon_tohum": t["meta"]["motivasyon"],
                 "motivasyon_geri_dusme": t["meta"]["motivasyon"] in ("tetikleyici_olay", "duygusal_regulasyon"),
                 "kaynak_parti8_sira": s["sira"]}
        while satir["tohum_kelime"] < BANT_MIN[satir["bicim"]]:
            eski = satir["bicim"]
            satir["bicim"] = ALT[eski]
            satir["izgara_sapmasi"] = f"bicim {eski}→{satir['bicim']}: tohum {satir['tohum_kelime']} kelime"
            sapma += 1
        plan.append(satir)

    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in plan), encoding="utf-8")

    sat = [f"# Haiku pilotu — tasarım ızgarası ({N} kayıt)\n",
           f"- Betik: `scripts/analiz/{Path(__file__).name}` · tohum `{TOHUM}`",
           f"- Girdi: `{KAYNAK_PLAN.relative_to(KOK)}` SHA256/16 `{_sha(KAYNAK_PLAN)}` · "
           f"`{HAVUZ.relative_to(KOK)}` `{_sha(HAVUZ)}`",
           f"- Çıktı: `{CIKTI.relative_to(KOK)}` `{_sha(CIKTI)}`",
           f"- Serbest tohum (tek turlu, hiç kullanılmamış, kriz süzgeçlerinden geçmiş): "
           f"**{len(serbest)}** / {len(havuz)} · süzgeçlerin elediği {kriz_elenen}",
           f"- `bicim` sapması (tohum kısa): {sapma}\n", "| sütun | dağılım |", "|---|---|"]
    for k in TASARIM + ("tur", "yas", "tohum_senaryo"):
        c = collections.Counter(str(r.get(k)) for r in plan)
        sat.append(f"| `{k}` | " + " · ".join(f"{a} {b}" for a, b in c.most_common()) + " |")
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
