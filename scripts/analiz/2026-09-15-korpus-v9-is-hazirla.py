#!/usr/bin/env python3
"""Korpus judge işlerini kurar — v8 ve v9 için, KUYRUK ORTAK.

v7'nin korpus iş dosyaları Kural 8 gereği silinmiş; bu yüzden kuyruk kimliği
dosyadan değil **koddan** doğrulanıyor (tasarım belgesi: render işlevleri v7
commit'i ile birebir aynı). Burada ayrıca iki yeni küme arasında kuyruğun
**baytı baytına** aynı olduğu doğrulanır — v8↔v9 farkı render farkı olamasın.

⛔ Körlük (K97): dosyada yalnızca rubrik + konuşma var; kaydın nereden geldiği,
neyle karşılaştırılacağı yazmaz.

Kullanım: uv run python scripts/analiz/2026-09-15-korpus-v9-is-hazirla.py
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import filter as f  # noqa: E402

_sp = _iu.spec_from_file_location("kp", KOK / "scripts/analiz/2026-09-15-korpus-v9-plan.py")
PLAN = _iu.module_from_spec(_sp)
_sp.loader.exec_module(PLAN)

ISLER = Path("/private/tmp/claude-501/-Users-pc-projects-birag-data-finetuning"
             "/fe6477c2-8e5e-439e-875d-df2b5ed62d91/scratchpad/judge-isleri")


def kuyruk(kayit: dict) -> str:
    """`filter.judge_record` ve v7 iş kurucusuyla BİREBİR aynı kuyruk."""
    asst = f._last_assistant(kayit)
    return (f"\n\n---\n\n## Değerlendirilecek konuşma\n\n"
            f"{f._render_conversation(kayit)}\n\n"
            f"(iç muhakeme — değerlendirme dışı, yalnızca bağlam için: "
            f"{(asst.get('thinking') or '')[:500]})")


def main() -> int:
    kayitlar = [json.loads(l) for l in PLAN.KORPUS.open(encoding="utf-8")]
    kuyruklar = {r["id"]: kuyruk(r) for r in kayitlar}

    for surum in ("v8", "v9"):
        rub = PLAN.RUBRIKLER[surum].read_text(encoding="utf-8")
        d = ISLER / f"korpus-{surum}"
        if d.exists():
            shutil.rmtree(d)
        (d / "istek").mkdir(parents=True)
        (d / "sonuc").mkdir()
        kimlikler = []
        for i, r in enumerate(kayitlar, 1):
            no = f"{i:03d}"
            (d / "istek" / f"{no}.txt").write_text(rub + kuyruklar[r["id"]],
                                                   encoding="utf-8")
            kimlikler.append({"no": no, "id": r["id"]})
        (d / "kimlikler.json").write_text(json.dumps(kimlikler, ensure_ascii=False,
                                                     indent=1))
        print(f"{surum}: {len(kimlikler)} iş → {d.name}")

    # ── Kuyruk v8 ile v9 arasında BAYTI BAYTINA aynı mı ────────────────────
    r8 = PLAN.RUBRIKLER["v8"].read_text(encoding="utf-8")
    r9 = PLAN.RUBRIKLER["v9"].read_text(encoding="utf-8")
    kotu = 0
    for i in range(1, len(kayitlar) + 1):
        no = f"{i:03d}"
        t8 = (ISLER / "korpus-v8" / "istek" / f"{no}.txt").read_text(encoding="utf-8")[len(r8):]
        t9 = (ISLER / "korpus-v9" / "istek" / f"{no}.txt").read_text(encoding="utf-8")[len(r9):]
        if hashlib.sha256(t8.encode()).digest() != hashlib.sha256(t9.encode()).digest():
            kotu += 1
    if kotu:
        print(f"⛔ {kotu} dosyada kuyruk ayrıştı")
        return 1
    print(f"✅ kuyruk v8 ↔ v9 baytı baytına aynı ({len(kayitlar)} dosya, sha256)")

    # ── Aşama 2: tohumla çekilmiş kontrol kümesi, v9'un BİREBİR kopyası ────
    kontrol = PLAN.kontrol_kumesi([r["id"] for r in kayitlar])
    no_of = {k["id"]: k["no"] for k in
             json.loads((ISLER / "korpus-v9" / "kimlikler.json").read_text())}
    for gecis in ("p2", "p3"):
        d = ISLER / f"korpus-v9-{gecis}"
        if d.exists():
            shutil.rmtree(d)
        (d / "istek").mkdir(parents=True)
        (d / "sonuc").mkdir()
        kim = []
        for i, oid in enumerate(kontrol, 1):
            kaynak = ISLER / "korpus-v9" / "istek" / f"{no_of[oid]}.txt"
            hedef = d / "istek" / f"{i:03d}.txt"
            shutil.copyfile(kaynak, hedef)
            if hashlib.sha256(kaynak.read_bytes()).digest() != \
               hashlib.sha256(hedef.read_bytes()).digest():
                print(f"⛔ kopya birebir değil: {kaynak}")
                return 1
            kim.append({"no": f"{i:03d}", "id": oid, "rol": "kontrol"})
        (d / "kimlikler.json").write_text(json.dumps(kim, ensure_ascii=False, indent=1))
        print(f"{gecis}: {len(kim)} iş → {d.name} (aşama 1'in BİREBİR kopyası)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
