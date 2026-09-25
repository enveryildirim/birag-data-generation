#!/usr/bin/env python3
"""Alt ajan taslağını blok betiğinin `KAYIT` sözlüğüne çevirir (K260).

⛔⛔ **BU BETİK KAYIT ÜRETMEZ, BİÇİM ÇEVİRİR.** Taslağın içeriğini
değiştirmez, düzeltmez, denetlemez. Kapılar blok betiğinde; okuma ve
revizyon bende (K260: alt ajan taslak yazar, okuma devredilmez).

⭐ Çevirmeden ÖNCE mekanik bir ön denetim yapar ve bulduklarını LİSTELER —
bu bir kapı değil, okuma kuyruğu: hangi satırlara önce bakacağımı söyler.
  · eksik/fazla satır · `son` boş · soru sayısı ↔ `turn_ending`
  · ilk kullanıcı mesajının bandı ↔ `bicim`
  · thinking/cevap oranı · bağlam sınıfı ↔ plan

Kullanım: uv run python ... --parti=v6-parti8 --taslak=<json> [--cikti=<py>]
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
_ap = argparse.ArgumentParser()
_ap.add_argument("--parti", required=True)
_ap.add_argument("--taslak", required=True)
_ap.add_argument("--cikti", default=None)
A = _ap.parse_args()


def _bant(m: str) -> str:
    # ⛔⛔ `<CTX>` BİR YER TUTUCU ve ilk hâlim onu SÖZCÜK SAYIYORDU: yalnız
    #    `<context>…</context>` etiketini siliyordum. Sonuç, üç blokta da tam
    #    26 sözcüklük «bant ihlalleri» — hepsi 25 sözcüktü ve kusur bendeydi.
    #    ➡️ *Bu oturumda DÖRDÜNCÜ kez bir sezici ölçtüğünü değil biçimini
    #    yakaladı (T227, T228, `slim`/«teslim», ve şimdi bu).*
    n = len(re.sub(r"<context.*?</context>|<CTX>", " ", m, flags=re.S).split())
    return "kisa" if n <= 8 else "orta" if n <= 25 else "uzun"


def _py(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def main() -> int:
    plan = {json.loads(l)["sira"]: json.loads(l)
            for l in (KOK / f"data/plan/{A.parti}.jsonl").read_text(
                encoding="utf-8").splitlines() if l.strip()}
    tas = {o["sira"]: o for o in json.loads(Path(A.taslak).read_text(encoding="utf-8"))}

    uyari: list[str] = []
    for s, o in sorted(tas.items()):
        p = plan.get(s)
        if p is None:
            uyari.append(f"#{s} planda yok")
            continue
        son = (o.get("son") or "").strip()
        if not son:
            uyari.append(f"#{s} `son` boş")
            continue
        soru = son.count("?")
        bek = 1 if p["turn_ending"] == "acik_uclu_soru" else 0
        if soru != bek:
            uyari.append(f"#{s} soru {soru} ≠ {bek} (`{p['turn_ending']}`)")
        ilk = next((t[1] for t in o.get("turns", []) if t[0] == "user"), "")
        if _bant(ilk) != p["bicim"]:
            uyari.append(f"#{s} bant {_bant(ilk)} ≠ `{p['bicim']}` "
                         f"({len(ilk.split())} sözcük)")
        th = o.get("thinking") or ""
        if son and len(th) / len(son) > 2.20:
            uyari.append(f"#{s} thinking oranı {len(th)/len(son):.2f} > 2.20")
        if p["context"] and o.get("baglam_davranisi") != p.get("baglam_davranisi"):
            uyari.append(f"#{s} bağlam sınıfı {o.get('baglam_davranisi')} "
                         f"≠ `{p.get('baglam_davranisi')}`")
        if p["context"] and not o.get("baglam"):
            uyari.append(f"#{s} bağlam bloğu yok")
    eksik = sorted(set(plan) & set(range(min(tas), max(tas) + 1)) - set(tas))
    if eksik:
        uyari.append(f"eksik satır: {eksik}")

    sat = ["KAYIT = {"]
    for s, o in sorted(tas.items()):
        p = plan.get(s)
        if p is None:
            continue
        sat.append(f"    {s}: {{  # {p['tur']}/{p['yas']} · {p['bicim']}/"
                   f"{p['register']} · {p['turn_type']} · {p['mi_process']} · "
                   f"{p['turn_ending']}")
        if o.get("baglam"):
            sat.append(f'        "baglam": {{"kaynak": {_py(o["baglam"]["kaynak"])},')
            sat.append(f'                   "metin": {_py(o["baglam"]["metin"])}}},')
        sat.append('        "turns": [')
        for rol, met in o.get("turns", []):
            sat.append(f'            ({_py(rol)}, {_py(met)}),')
        sat.append('            ("assistant", None),')
        sat.append("        ],")
        sat.append(f'        "son": {_py(o["son"])},')
        sat.append(f'        "thinking": {_py(o.get("thinking") or "")},')
        if o.get("sapma"):
            sat.append(f'        "sapma": {_py(o["sapma"])},')
        if p["context"]:
            sat.append(f'        "baglam_davranisi": {_py(o.get("baglam_davranisi") or "")},')
        sat.append("    },")
    sat.append("}")

    y = Path(A.cikti) if A.cikti else Path(A.taslak).with_suffix(".kayit.py")
    y.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print(f"{len(tas)} satır çevrildi → {y}")
    print(f"⚠️ okuma kuyruğu ({len(uyari)}):")
    for u in uyari:
        print(f"   {u}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
