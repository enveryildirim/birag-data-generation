#!/usr/bin/env python3
"""Ölçek eğrisinin ilk noktası: v0.0.5 (155) -> v0.0.6 (214).

Üç kol, `evals/golden.dev.jsonl` (48 öğe) üzerinde, `--judge-atla` ile:
  · v005-referans   : v0.0.5, 372 adım   (mevcut `f4c-doz25-A-dar` adaptörü)
  · v006-adimsabit  : v0.0.6, 372 adım   ⇒ v005 ile tek fark VERİ
  · v006-3epoch     : v0.0.6, 513 adım   ⇒ adimsabit ile tek fark ADIM
LoRA kapsamı, LR, tohum, template üçünde de BİREBİR aynı (K113'ün kontrol kolu).

⛔⛔ **VAL LOSS ÜÇ KOL ARASINDA OKUNAMAZ.** Doğrulama kümesi datasetin kendi
%20'si; v0.0.5 ile v0.0.6 farklı kümelerle doğruluyor. Val loss yalnızca
`3epoch` ↔ `adimsabit` arasında anlamlı (aynı dataset, aynı tohum).
⇒ Veri etkisi yalnızca SABİT eval setinden okunur.

⛔ Judge atlandı (K96/K97) ⇒ `golden.dev`in 203 iddiasının **141'i judge tipi** ve
`denetlenemedi` kaldı. Öğe düzeyinde üç kol da **0/48**; okunabilen tek şey
**60 otomatik iddia**. ➡️ *Bir eval setinin «kaç öğe geçti» sayısı, o setin
iddialarının hangi tipte olduğu yazılmadan okunamaz.*
"""
from __future__ import annotations
import json, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
KOSU = {"v005-referans": "20260916-204027-g1-v005-referans",
        "v006-adimsabit": "20260916-203111-g1-v006-adimsabit",
        "v006-3epoch": "20260916-202237-g1-v006-3epoch"}
CIKTI = KOK / "reports/analiz/2026-09-16-olcek-egrisi-ilk-nokta.json"


def main() -> int:
    detay, ozet = {}, {}
    for ad, d in KOSU.items():
        yol = KOK / "reports/analiz/golden-kosu" / d / "sonuclar.jsonl"
        rows = [json.loads(s) for s in yol.read_text(encoding="utf-8").splitlines() if s.strip()]
        per = {(r["id"], it["ad"]): it["gecti"]
               for r in rows for it in (r.get("denetim") or []) if it["tip"] == "otomatik"}
        detay[ad] = per
        ozet[ad] = {
            "kosu": d,
            "otomatik_gecen": sum(1 for v in per.values() if v is True),
            "otomatik_toplam": len(per),
            "dejenere": sum(1 for r in rows if (r.get("dejenerasyon") or {}).get("dejenere")),
            "bos_cevap": sum(1 for r in rows if not (r.get("cevap") or "").strip()),
            "kesildi": sum(1 for r in rows if r.get("kesildi")),
            "ort_cevap_kelime": round(sum(len((r.get("cevap") or "").split()) for r in rows) / len(rows), 1),
            "ort_thinking_kelime": round(sum(len((r.get("thinking") or "").split()) for r in rows) / len(rows), 1),
        }

    def kiyas(x, y):
        a, b = detay[x], detay[y]; ortak = set(a) & set(b)
        return {"ortak_iddia": len(ortak),
                f"{y}_lehine": sorted(f"{i}/{k}" for i, k in ortak if b[(i, k)] is True and a[(i, k)] is not True),
                f"{x}_lehine": sorted(f"{i}/{k}" for i, k in ortak if a[(i, k)] is True and b[(i, k)] is not True)}

    # ⭐ Hangi iddia adları HİÇ ayrışmıyor — tavan etkisi görünür olsun diye.
    adlar = {k[1] for k in detay["v006-3epoch"]}
    tavan = [a for a in sorted(adlar)
             if all(v is True for kol in detay.values() for k, v in kol.items() if k[1] == a)]

    rapor = {"tarih": "2026-09-16",
             "betik": "scripts/analiz/2026-09-16-olcek-egrisi-ilk-nokta.py",
             "eval_seti": "evals/golden.dev.jsonl", "judge": "ATLANDI (K96/K97)",
             "kollar": ozet,
             "veri_etkisi_adim_sabit": kiyas("v005-referans", "v006-adimsabit"),
             "adim_etkisi_veri_sabit": kiyas("v006-adimsabit", "v006-3epoch"),
             "hic_ayrismayan_iddia": tavan,
             "val_loss": {"v006-3epoch": 2.780, "v006-adimsabit": 2.823,
                          "v005-referans": 2.874,
                          "not": "v005 BAŞKA doğrulama kümesi — kıyaslanamaz"}}
    CIKTI.write_text(json.dumps(rapor, ensure_ascii=False, indent=2), encoding="utf-8")
    for ad, o in ozet.items():
        print(f"  {ad:15s} {o['otomatik_gecen']:>2}/{o['otomatik_toplam']} "
              f"({100*o['otomatik_gecen']/o['otomatik_toplam']:.1f}%) · dejenere {o['dejenere']} "
              f"· cevap {o['ort_cevap_kelime']} kel · thinking {o['ort_thinking_kelime']} kel")
    print(f"\n⭐ hiç ayrışmayan (tavanda) iddia: {tavan}")
    print(f"→ {CIKTI.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
