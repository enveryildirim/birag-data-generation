#!/usr/bin/env python3
"""Ölçek-5k tasarım ızgarası — **5000 kayıt, 200 parça × 25**. Üretimden ÖNCE yazılır, dondurulur.

⭐ Kullanıcı kararı (2026-10-20): *«çok takılmadan 5000 civarı veri»*, sormadan
işleyen bir yapı. Gerekçe ve bedeli `reports/analiz/2026-10-20-olcek5k-plan.md`.

Tasarım sütunları `v6-parti8` ızgarasının dağılımından **yerine koyarak**
örneklenir (Haiku pilotuyla aynı aile). Kapsama-açığı hedeflemesi YAPILMAZ.

⛔⛔ TOHUM YETMİYOR ve bu bir karar: kriz süzgeçlerinden geçen tek turlu
tohum sayısı 5000'in çok altında ⇒ bir tohum birden fazla kayda gider.
Kural: (1) önce hiç kullanılmamış tohumlar, (2) en az kullanılmış tohum,
(3) aynı tohum aynı (turn_type, bicim, turn_ending) üçlüsünü iki kez almaz.
Tohum başına kullanım raporda dağılım olarak yazılır (T231'in sorunu
burada bilerek büyütülüyor — gizlenmiyor).

Çıktı: data/plan/olcek5k.jsonl · reports/analiz/2026-10-20-olcek5k-plan.md
"""
from __future__ import annotations

import collections
import hashlib
import json
import random
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
N, PARCA = 5000, 25
TOHUM = 20261021
KAYNAK_PLAN = KOK / "data/plan/v6-parti8.jsonl"
HAVUZ = KOK / "data/seeds.v2.jsonl"
CIKTI = KOK / "data/plan/olcek5k.jsonl"
RAPOR = KOK / "reports/analiz/2026-10-20-olcek5k-plan.md"

_sp = _iu.spec_from_file_location("hp", KOK / "scripts/analiz/2026-10-20-haiku-pilot-plan.py")
HP = _iu.module_from_spec(_sp)
_sp.loader.exec_module(HP)


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def main() -> int:
    rng = random.Random(TOHUM)
    kaynak = [json.loads(l) for l in KAYNAK_PLAN.read_text(encoding="utf-8").splitlines() if l.strip()]
    havuz = [json.loads(l) for l in HAVUZ.read_text(encoding="utf-8").splitlines() if l.strip()]
    kullanilmis = HP._kullanilmis()
    P1 = HP._modul("p1", "scripts/analiz/2026-09-15-v4-parti1-plan.py")
    KZ = HP._modul("kz", "scripts/analiz/2026-09-17-kriz-suzgeci-yanlis-negatif.py")
    BK = HP._modul("bk", "scripts/analiz/2026-09-17-tohum-beyan-kriz-kapisi.py")
    tek = [t for t in havuz if t.get("turn_count", 1) == 1]
    uygun = [t for t in tek if t["meta"].get("senaryo") != "kriz"
             and not P1.KRIZ_ANAHTAR.search(t["user_message"])
             and not KZ.DOLAYLI.search(t["user_message"]) and BK._sinif(t) != "sert"]
    # ⭐ TUR/YAŞ TOHUMDAN GELİR. İlk sürüm parti8 satırının tur/yaşına tohum
    #    arıyordu ve ölçüldü: 2153 uygun tohumun yalnız 1300'ü kullanıldı, bir
    #    kısmı 5-6 kez. ⇒ tohumlar sırayla dolaşılır (önce hiç kullanılmamışlar),
    #    tasarım sütunları parti8'den çekilir; tur dağılımı havuzunkidir.
    rng.shuffle(uygun)
    uygun.sort(key=lambda t: t["seed_id"] in kullanilmis)   # kararlı: serbestler önce
    kullanim: collections.Counter = collections.Counter()
    hucre: set[tuple] = set()
    plan, sapma, atlanan, tur_ = [], 0, 0, 0
    while len(plan) < N:
        tur_ += 1
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
            sira = len(plan) + 1
            satir = {"sira": sira, "parca": (sira - 1) // PARCA + 1,
                     **{k: s.get(k) for k in HP.TASARIM}, "bicim": bicim,
                     "tur": t["meta"]["bagimlilik_turu"],
                     # şema `age_group: Literal["yetiskin","ergen"]`; v4-parti1 eşlemesi
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
    # parçalar karışık olsun: aynı tohumun kayıtları aynı parçaya yığılmasın
    rng.shuffle(plan)
    for i, r in enumerate(plan, 1):
        r["sira"], r["parca"] = i, (i - 1) // PARCA + 1

    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in plan), encoding="utf-8")

    dag = collections.Counter(kullanim.values())
    onceden = sum(1 for r in plan if r["tohum_onceden_kullanildi"])
    sat = [f"# Ölçek-5k — tasarım ızgarası ({N} kayıt, {N // PARCA} parça × {PARCA})\n",
           f"- Betik: `scripts/analiz/{Path(__file__).name}` · tohum `{TOHUM}`",
           f"- Girdi: `{KAYNAK_PLAN.relative_to(KOK)}` `{_sha(KAYNAK_PLAN)}` · `{HAVUZ.relative_to(KOK)}` `{_sha(HAVUZ)}`",
           f"- Çıktı: `{CIKTI.relative_to(KOK)}` `{_sha(CIKTI)}`",
           f"- Uygun tohum (tek turlu, kriz süzgeçlerinden geçmiş): **{len(uygun)}** / {len(havuz)}; "
           f"bu planda kullanılan farklı tohum **{len(kullanim)}**",
           f"- ⛔ Önceden (v0.1.1 / eski partiler / pilot) kullanılmış tohumdan gelen satır: **{onceden}** / {N}",
           f"- Tohum başına kullanım dağılımı: " + " · ".join(f"{k}×: {v}" for k, v in sorted(dag.items())),
           f"- `bicim` sapması {sapma} · uygun tohum bulunamayıp atlanan çekiliş {atlanan}\n",
           "| sütun | dağılım |", "|---|---|"]
    for k in HP.TASARIM + ("tur", "yas", "tohum_senaryo"):
        c = collections.Counter(str(r.get(k)) for r in plan)
        sat.append(f"| `{k}` | " + " · ".join(f"{a} {b}" for a, b in c.most_common()) + " |")
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
