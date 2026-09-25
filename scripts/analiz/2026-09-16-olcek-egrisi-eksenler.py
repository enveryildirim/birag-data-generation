#!/usr/bin/env python3
"""Ölçek eğrisi ilk noktası — DÖRT eksen setinde, üç kol + taban.

Kollar (LoRA kapsamı/LR/tohum/template BİREBİR aynı, K113'ün kontrol kolu):
  · TABAN         : adaptörsüz ham model (yalnız `safety_crisis`te mevcut)
  · v005-referans : v0.0.5, 372 adım
  · v006-adimsabit: v0.0.6, 372 adım  ⇒ v005 ile tek fark VERİ
  · v006-3epoch   : v0.0.6, 513 adım  ⇒ adimsabit ile tek fark ADIM

⛔ Judge YOK (`eksen_eval` deterministik; judge iddiaları `denetlenemedi`).
⛔ n küçük (set başına 15-30 öğe); tek öğe oynaması bu tabloda **1 puan**.
"""
from __future__ import annotations
import json, sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
EK = KOK / "reports/analiz/eksen-kosu"
CIKTI = KOK / "reports/analiz/2026-09-16-olcek-egrisi-eksenler.json"
KOL = ["TABAN", "v005-referans", "v006-adimsabit", "v006-3epoch"]
TABAN = {"safety_crisis": "20260915-105829-safety_crisis-baseline-1"}


def _dizin(set_ad: str, kol: str) -> Path | None:
    if kol == "TABAN":
        return EK / TABAN[set_ad] if set_ad in TABAN else None
    e = [p for p in EK.iterdir() if p.name.endswith(f"g1-{set_ad}-{kol}")]
    return e[0] if e else None


def _oku(d: Path) -> list[dict]:
    return [json.loads(s) for s in (d / "sonuclar.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]


def _iddialar(rows: list[dict]) -> dict:
    p = {}
    for r in rows:
        for i, it in enumerate(r.get("iddialar") or []):
            ad = it.get("kural") or it.get("alan") or it.get("ad") or f"i{i}"
            p[(r["id"], f"{ad}#{i}")] = it.get("gecti")
    return p


def main() -> int:
    rapor = {"tarih": "2026-09-16",
             "betik": "scripts/analiz/2026-09-16-olcek-egrisi-eksenler.py",
             "judge": "YOK — eksen_eval deterministik", "setler": {}}
    for set_ad in ("safety_crisis", "context_fidelity", "forgetting_smoke", "sycophancy"):
        s = {"kollar": {}, "kural_bazinda": {}}
        per = {}
        for kol in KOL:
            d = _dizin(set_ad, kol)
            if d is None:
                continue
            rows = _oku(d)
            p = _iddialar(rows)
            per[kol] = p
            g = sum(1 for v in p.values() if v is True)
            s["kollar"][kol] = {
                "kosu": d.name, "oge": len(rows),
                "iddia_gecen": g, "iddia_toplam": len(p),
                "oge_tam_gecen": sum(1 for r in rows if r.get("otomatik_gecti") is True),
                "kesildi": sum(1 for r in rows if r.get("kesildi")),
                "ort_cevap_kelime": round(sum(len((r.get("cevap") or "").split()) for r in rows) / len(rows), 1),
            }
        # kural bazında: hangi kural ayrışıyor, hangisi tavanda
        kurallar = {k[1].split("#")[0] for p in per.values() for k in p}
        for kural in sorted(kurallar):
            sat = {kol: sum(1 for k, v in p.items() if k[1].startswith(kural + "#") and v is True)
                   for kol, p in per.items()}
            tot = {kol: sum(1 for k in p if k[1].startswith(kural + "#")) for kol, p in per.items()}
            if len(set(sat.values())) > 1:      # yalnız AYRIŞAN kurallar
                s["kural_bazinda"][kural] = {"gecen": sat, "toplam": tot}
        # kontrollü kıyaslar
        def kiyas(x, y):
            if x not in per or y not in per:
                return None
            a, b = per[x], per[y]; o = set(a) & set(b)
            return {"ortak": len(o),
                    f"{y}_lehine": sorted(f"{i}/{k}" for i, k in o if b[(i, k)] is True and a[(i, k)] is not True),
                    f"{x}_lehine": sorted(f"{i}/{k}" for i, k in o if a[(i, k)] is True and b[(i, k)] is not True)}
        s["veri_etkisi"] = kiyas("v005-referans", "v006-adimsabit")
        s["adim_etkisi"] = kiyas("v006-adimsabit", "v006-3epoch")
        s["egitim_etkisi"] = kiyas("TABAN", "v006-3epoch")
        rapor["setler"][set_ad] = s
    CIKTI.write_text(json.dumps(rapor, ensure_ascii=False, indent=2), encoding="utf-8")

    for set_ad, s in rapor["setler"].items():
        print(f"\n=== {set_ad} ===")
        for kol, k in s["kollar"].items():
            print(f"  {kol:16s} iddia {k['iddia_gecen']:>3}/{k['iddia_toplam']:<4} "
                  f"({100*k['iddia_gecen']/k['iddia_toplam']:>5.1f}%) · öğe tam "
                  f"{k['oge_tam_gecen']:>2}/{k['oge']} · cevap {k['ort_cevap_kelime']} kel")
        if s["kural_bazinda"]:
            print("  ayrışan kurallar:")
            for kural, d in s["kural_bazinda"].items():
                print(f"    {kural:22s} " + " · ".join(f"{k}:{v}" for k, v in d['gecen'].items()))
        else:
            print("  ⚠️ hiçbir kural ayrışmıyor (hepsi tavanda ya da hepsi düşük)")
        for ad, key in (("VERİ", "veri_etkisi"), ("ADIM", "adim_etkisi"), ("EĞİTİM", "egitim_etkisi")):
            v = s.get(key)
            if v:
                art = [k for k in v if k.endswith("_lehine")]
                print(f"    {ad:6s}: " + " · ".join(f"{k.replace('_lehine','')} +{len(v[k])}" for k in art))
    print(f"\n→ {CIKTI.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
