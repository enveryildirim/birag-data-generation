#!/usr/bin/env python3
"""Ölçek-5k — bütün parçaları birleştirir, kapıları yeniden koşar, sonuç raporunu yazar.

Girdi : data/candidates/olcek5k/kayit/parca*.C.jsonl · B/ · C/ (denetim izi için)
Çıktı : data/candidates/olcek5k.jsonl · reports/analiz/2026-10-20-olcek5k-sonuc.md

⛔ Bu betik veri setini DONDURMAZ (`datasets/` ayrı adım, Kural 4).
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from checks import run_checks  # noqa: E402
import tohum_guvenlik as TG  # noqa: E402

_sp = _iu.spec_from_file_location("arac", KOK / "scripts/analiz/2026-10-20-olcek5k-arac.py")
AR = _iu.module_from_spec(_sp)
_sp.loader.exec_module(AR)

CIKTI = KOK / "data/candidates/olcek5k.jsonl"
RAPOR = KOK / "reports/analiz/2026-10-20-olcek5k-sonuc.md"


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def main() -> int:
    plan = AR._plan_hepsi()
    parcalar = sorted({r["parca"] for r in plan})
    kayit, red, eksik = [], 0, []
    c_karar = collections.Counter()
    c_grup: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    c_neden = collections.Counter()
    for n in parcalar:
        f = AR.DIZIN / "kayit" / f"parca{n:03d}.C.jsonl"
        if not f.exists():
            eksik.append(n)
            continue
        for k in AR._oku(AR._yol("C", n)):
            c_karar[k.get("c_karar") or "—"] += 1
            c_grup[AR._c_model(n)][k.get("c_karar") or "—"] += 1
            if k.get("c_neden"):
                c_neden[re.split(r"[:—\-]", k["c_neden"], 1)[0].strip()[:40]] += 1
        for r in AR._oku(f):
            if run_checks(r).get("passed"):
                kayit.append(r)
            else:
                red += 1
    gorulen: set[str] = set()
    kayit = [r for r in kayit if not (r["id"] in gorulen or gorulen.add(r["id"]))]
    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kayit), encoding="utf-8")

    sonlar = [r["messages"][-1]["content"] for r in kayit]
    sat = ["# Ölçek-5k — sonuç\n",
           f"- Betik: `scripts/analiz/{Path(__file__).name}` · plan `{AR.PLAN.relative_to(KOK)}` `{_sha(AR.PLAN)}`",
           f"- Çıktı: `{CIKTI.relative_to(KOK)}` `{_sha(CIKTI)}` — **{len(kayit)} kayıt**",
           f"- Planlanan {len(plan)} · C'si bitmemiş parça {len(eksik)}" + (f" ({eksik[:30]})" if eksik else ""),
           f"- Birleştirmede `run_checks` reddi: {red}\n",
           "## C kararları\n", "| karar | satır |", "|---|---:|"]
    sat += [f"| {k} | {v} |" for k, v in c_karar.most_common()]
    sat += ["\n### C modeline göre (Sonnet 1–13 · Haiku 14–228)\n", "| C modeli | parça | aynen | duzeltildi | dusuruldu | düzeltme+düşürme % |",
            "|---|---:|---:|---:|---:|---:|"]
    for m, c in sorted(c_grup.items()):
        t = sum(c.values())
        sat.append(f"| {m} | {t // 25} | {c['aynen']} | {c['duzeltildi']} | {c['dusuruldu']} | "
                   f"%{100 * (c['duzeltildi'] + c['dusuruldu']) / max(t, 1):.1f} |")
    sat += ["\n## C düzeltme / düşürme sebepleri (ilk sözcük öbeği)\n", "| sebep | n |", "|---|---:|"]
    sat += [f"| {k} | {v} |" for k, v in c_neden.most_common(25)]
    gm = [r["gen_meta"] for r in kayit]
    sat += ["\n## Dağılım\n", "| alan | dağılım |", "|---|---|"]
    for ad, f in [("turn_ending", lambda g, r: g["turn_ending"]), ("sinir_tipi", lambda g, r: g["sinir_tipi"]),
                  ("güvenlik sapması", lambda g, r: "var" if g.get("turn_ending_plan") or g.get("sinir_tipi_plan") else "yok"),
                  ("sızıntı şüphesi kaldı", lambda g, r: "evet" if g.get("sizinti_supheli") else "hayır"),
                  ("tur", lambda g, r: r["addiction_type"]), ("yas", lambda g, r: r["age_group"]),
                  ("turn_type", lambda g, r: r["turn_type"]), ("slice", lambda g, r: r["slice"]),
                  ("tohum önceden kullanılmış", lambda g, r: str(g.get("tohum_onceden_kullanildi")))]:
        c = collections.Counter(f(g, r) for g, r in zip(gm, kayit))
        sat.append(f"| {ad} | " + " · ".join(f"{a} {b}" for a, b in c.most_common()) + " |")
    sat += ["\n## Şablon (kayıt başına, bütün korpus)\n", "| kalıp | n | % |", "|---|---:|---:|"]
    for ad, rx, _ in AR.KALIP_TAVAN:
        n = sum(1 for t in sonlar if rx.search(TG.tr_fold(t)))
        sat.append(f"| {ad} | {n} | %{100 * n / max(len(sonlar), 1):.1f} |")
    acilis = collections.Counter(TG.tr_fold(r["messages"][2]["content"]).strip()
                                 for r in kayit if r["turn_type"] == "multi")
    sat.append(f"\nÇok turlu açılış: {sum(acilis.values())} kayıtta {len(acilis)} farklı açılış; "
               f"en sık: " + " · ".join(f"«{a[:30]}»×{b}" for a, b in acilis.most_common(5)))
    say8: dict[str, int] = collections.Counter()
    for t in sonlar:
        for d in AR.HPB._diziler(t, 8):
            say8[d] += 1
    tekrar = [(d, c) for d, c in say8.items() if c > 1]
    sat.append(f"\n8 sözcüklük dizi tekrarı (parçalar arası): {len(tekrar)} dizi; en sık: "
               + " · ".join(f"«{d}»×{c}" for d, c in sorted(tekrar, key=lambda x: -x[1])[:5]))
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
