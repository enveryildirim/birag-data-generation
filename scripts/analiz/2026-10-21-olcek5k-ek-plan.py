#!/usr/bin/env python3
"""Ölçek-5k tamamlama ızgarası — **700 satır, parça 201-228 × 25, sıra 5001-5700** (v0.2.1).

👤 2026-10-21: *«650 kayıt daha üret, v0.2.1 olarak dondur»*. `v0.2.0` 4334 kayıt; 5000'e
666 eksik ⇒ ~%3 kayıp (sızıntı şüphesi + C düşürmesi) için 700 satır.

⛔⛔ K281 dersi: ölçek-5k planı eval tohumlarını ve eleme defterini uygulamamıştı. Bu betik
dışlamaları YENİDEN TÜRETMEZ, `2026-10-21-v020-dondur.py`'den İÇE AKTARIR:
  eval `kaynak.seed_id` · eval kullanıcı metni (60 karakter önek) · kalıcı eleme defteri ·
  BLEU referans setinin tohumları (kardeş kayıt üretmemek için) · kriz süzgeçleri (ölçek-5k ile aynı).
Tohum seçimi: ölçek-5k planında EN AZ kullanılmış tohum önce; aynı (tohum, turn_type, bicim,
turn_ending) hücresi ölçek-5k'da varsa alınmaz. Tasarım sütunları ölçek-5k ile aynı kaynaktan.

Çıktı: data/plan/olcek5k-ek.jsonl · reports/analiz/2026-10-21-olcek5k-ek-plan.md
"""
from __future__ import annotations

import collections
import hashlib
import json
import random
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
N, PARCA, ILK_PARCA, ILK_SIRA = 700, 25, 201, 5001
TOHUM = 20261022
KAYNAK_PLAN = KOK / "data/plan/v6-parti8.jsonl"
HAVUZ = KOK / "data/seeds.v2.jsonl"
ANA_PLAN = KOK / "data/plan/olcek5k.jsonl"
CIKTI = KOK / "data/plan/olcek5k-ek.jsonl"
RAPOR = KOK / "reports/analiz/2026-10-21-olcek5k-ek-plan.md"


def _modul(ad: str, yol: str):
    sp = _iu.spec_from_file_location(ad, KOK / yol)
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


HP = _modul("hp", "scripts/analiz/2026-10-20-haiku-pilot-plan.py")
DON = _modul("don", "scripts/analiz/2026-10-21-v020-dondur.py")


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def main() -> int:
    if CIKTI.exists():
        raise SystemExit(f"⛔ {CIKTI.relative_to(KOK)} zaten var — plan üretimden önce dondurulur")
    rng = random.Random(TOHUM)
    kaynak = DON._jl(KAYNAK_PLAN)
    havuz = DON._jl(HAVUZ)
    ana = DON._jl(ANA_PLAN)
    kullanilmis = HP._kullanilmis()
    ev_tohum, ev_metin, _ = DON._eval()
    elenen = {d["seed_id"] for d in DON._jl(DON.ELEME)}
    ref_tohum = {r["seed_id"] for r in DON._jl(DON.REF)}

    def eval_carpisir(t: str) -> bool:
        d = DON.TG.tr_fold(t).strip()
        return len(d) >= DON.EVAL_MIN_KARAKTER and any(e[:60] in d or d[:60] in e for e in ev_metin)

    P1 = HP._modul("p1", "scripts/analiz/2026-09-15-v4-parti1-plan.py")
    KZ = HP._modul("kz", "scripts/analiz/2026-09-17-kriz-suzgeci-yanlis-negatif.py")
    BK = HP._modul("bk", "scripts/analiz/2026-09-17-tohum-beyan-kriz-kapisi.py")
    elenme = collections.Counter()
    uygun = []
    for t in havuz:
        if t.get("turn_count", 1) != 1:
            continue
        if (t["meta"].get("senaryo") == "kriz" or P1.KRIZ_ANAHTAR.search(t["user_message"])
                or KZ.DOLAYLI.search(t["user_message"]) or BK._sinif(t) == "sert"):
            elenme["kriz süzgeci"] += 1
        elif t["seed_id"] in ev_tohum or t["source_id"] in ev_tohum:
            elenme["eval tohumu"] += 1
        elif eval_carpisir(t["user_message"]):
            elenme["eval metni"] += 1
        elif t["seed_id"] in elenen or t["source_id"] in elenen:
            elenme["eleme defteri"] += 1
        elif t["seed_id"] in ref_tohum:
            elenme["BLEU referans tohumu"] += 1
        else:
            uygun.append(t)

    ana_kul = collections.Counter(r["seed_id"] for r in ana)
    hucre = {(r["seed_id"], r["turn_type"], r["bicim"], r["turn_ending"]) for r in ana}
    rng.shuffle(uygun)
    uygun.sort(key=lambda t: ana_kul[t["seed_id"]])   # kararlı: ölçek-5k'da en az kullanılan önce
    kullanim: collections.Counter = collections.Counter()
    plan, sapma, atlanan = [], 0, 0
    while len(plan) < N:
        for t in uygun:
            if len(plan) >= N:
                break
            for _ in range(20):
                s = rng.choice(kaynak)
                bicim = s["bicim"]
                kelime = len(t["user_message"].split())
                while kelime < HP.BANT_MIN[bicim]:
                    bicim = HP.ALT[bicim]
                if (t["seed_id"], s["turn_type"], bicim, s["turn_ending"]) not in hucre:
                    break
            else:
                atlanan += 1
                continue
            satir = {"sira": 0, "parca": 0,
                     **{k: s.get(k) for k in HP.TASARIM}, "bicim": bicim,
                     "tur": t["meta"]["bagimlilik_turu"],
                     "yas": "ergen" if t["meta"]["yas_grubu"] == "ergen" else "yetiskin",
                     "yas_tohum": t["meta"]["yas_grubu"], "havuz": None,
                     "seed_id": t["seed_id"], "source_id": t["source_id"],
                     "tohum_senaryo": t["meta"]["senaryo"],
                     "tohum_kelime": len(t["user_message"].split()),
                     "tohum_metin": t["user_message"],
                     "tohum_baglam": t.get("scenario_context"),
                     "motivasyon": HP.MOTIVASYON.get(t["meta"]["motivasyon"], "ic"),
                     "motivasyon_tohum": t["meta"]["motivasyon"],
                     "tohum_onceden_kullanildi": t["seed_id"] in kullanilmis,
                     "tohum_bu_plandaki_kullanim": kullanim[t["seed_id"]] + 1}
            if bicim != s["bicim"]:
                satir["izgara_sapmasi"] = f"bicim {s['bicim']}→{bicim}: tohum {satir['tohum_kelime']} kelime"
                sapma += 1
            hucre.add((t["seed_id"], s["turn_type"], bicim, s["turn_ending"]))
            kullanim[t["seed_id"]] += 1
            plan.append(satir)
    rng.shuffle(plan)
    for i, r in enumerate(plan):
        r["sira"], r["parca"] = ILK_SIRA + i, ILK_PARCA + i // PARCA
    assert not {r["sira"] for r in plan} & {r["sira"] for r in ana}

    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in plan), encoding="utf-8")
    toplam_kul = collections.Counter(ana_kul[t] + kullanim[t] for t in kullanim)
    sat = [f"# Ölçek-5k tamamlama ızgarası ({N} satır, parça {ILK_PARCA}-{plan[-1]['parca']})\n",
           f"- Betik: `scripts/analiz/{Path(__file__).name}` · tohum `{TOHUM}` · tarih 2026-10-21",
           f"- Girdi: `{KAYNAK_PLAN.relative_to(KOK)}` `{_sha(KAYNAK_PLAN)}` · `{HAVUZ.relative_to(KOK)}` `{_sha(HAVUZ)}` · "
           f"`{ANA_PLAN.relative_to(KOK)}` `{_sha(ANA_PLAN)}` · eval-ref `{_sha(DON.REF)}` · eleme `{_sha(DON.ELEME)}`",
           f"- Çıktı: `{CIKTI.relative_to(KOK)}` `{_sha(CIKTI)}`",
           f"- Uygun tohum: **{len(uygun)}**; elenen: " + " · ".join(f"{k} {v}" for k, v in elenme.most_common()),
           f"- Bu planda farklı tohum **{len(kullanim)}** · ölçek-5k + bu plan toplam kullanım: "
           + " · ".join(f"{k}×: {v}" for k, v in sorted(toplam_kul.items())),
           f"- `bicim` sapması {sapma} · atlanan çekiliş {atlanan}\n",
           "| sütun | dağılım |", "|---|---|"]
    for k in HP.TASARIM + ("tur", "yas", "tohum_senaryo"):
        c = collections.Counter(str(r.get(k)) for r in plan)
        sat.append(f"| `{k}` | " + " · ".join(f"{a} {b}" for a, b in c.most_common()) + " |")
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
