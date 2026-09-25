#!/usr/bin/env python3
"""ÜÇÜNCÜ şablon ölçüldü — ve üçü de aynı biçimde büyüyor.

⛔⛔ Judge, çıkmaz revizyonunu okurken not düştü: *«…olup olmadığını ben
söyleyemem; … benim işim değil ve buradan uydurmayacağım»* kalıbı beş kayıtta
**neredeyse birebir** tekrarlanıyor ve hiçbir alan bunu yakalamıyor —
`klise_acilis` yalnız **kabul** cümlelerini soruyor.

⭐ Bu, aynı günün üçüncü şablon bulgusu:

| şablon | ne oldu |
|---|---|
| *«Bir şeye katılmıyorum»* | 300 kayıtta 50; judge 26 kez `tuzak_uzman` dedi |
| *«İlk adım … olabilir»* + kurum | §8b′ yazıldı, 16 kayıt düzeltildi |
| ⭐ *«…olup olmadığını ben söyleyemem»* | **bu ölçüm** |

➡️⭐⭐ *Üretici bir kuralı öğrendiğinde onu bir CÜMLEYE dönüştürüyor ve o cümle
korpusta üstel olarak büyüyor. Kural doğru, kalıp yanlış — ve kalıbı doğuran
şey kuralın kendisi. Her yeni kural, bir sonraki şablonun tohumu.*

⚠️ Kalıp elle yazıldı (K30) ⇒ sayı **alt sınır**. Bu bir kapı değil, bir ölçüm.
"""
from __future__ import annotations
import json, re
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / "reports/analiz/2026-09-17-sablon-buyumesi.md"
SABLON = {
 "«Bir şeye katılmıyorum»": re.compile(r"Bir şeye (de )?katılmıyorum", re.I),
 "«…olup olmadığını ben söyleyemem»": re.compile(r"olup olmadığını ben söyleyemem", re.I),
 "«buradan uydurmayacağım»": re.compile(r"buradan uydurmayacağım", re.I),
 "«benim işim değil»": re.compile(r"benim işim değil", re.I),
 "«İlk adım … olabilir»": re.compile(r"[İi]lk adım.{0,80}olabilir", re.I | re.S),
}
KORPUS = [("datasets/v0.0.2/train.jsonl", "v0.0.2"), ("datasets/v0.0.5/train.jsonl", "v0.0.5"),
          ("datasets/v0.0.6/train.jsonl", "v0.0.6"), ("datasets/v0.0.7/train.jsonl", "v0.0.7"),
          ("datasets/v0.0.8/train.jsonl", "v0.0.8")]


def main() -> int:
    sat = ["# Şablon büyümesi — her yeni kural, bir sonraki şablonun tohumu", "",
           "**Betik:** `scripts/analiz/2026-09-17-sablon-buyumesi.py` · **Tarih:** 2026-09-17", "",
           "⛔ Judge, çıkmaz revizyonunu okurken not düştü: bir ret kalıbı beş kayıtta "
           "**neredeyse birebir** tekrarlanıyor ve hiçbir alan yakalamıyor "
           "(`klise_acilis` yalnız **kabul** cümlelerini soruyor).", "",
           "| şablon | " + " | ".join(a for _, a in KORPUS) + " |",
           "|---|" + "---:|" * len(KORPUS)]
    veri = {}
    for ad, pat in SABLON.items():
        hucre = []
        for yol, sur in KORPUS:
            p = KOK / yol
            if not p.exists():
                hucre.append("—")
                continue
            rs = [json.loads(s) for s in p.read_text(encoding="utf-8").splitlines() if s.strip()]
            n = sum(1 for r in rs
                    if pat.search(" ".join(m.get("content") or "" for m in r["messages"]
                                           if m["role"] == "assistant")))
            hucre.append(f"**{n}** (%{100*n/len(rs):.1f})")
            veri.setdefault(ad, {})[sur] = n
        sat.append(f"| {ad} | " + " | ".join(hucre) + " |")
    sat += ["", "## ⭐⭐ Desen: üçü de aynı biçimde büyüyor", "",
            "➡️⭐⭐ *Üretici bir kuralı öğrendiğinde onu bir CÜMLEYE dönüştürüyor ve o "
            "cümle korpusta hızla büyüyor. Kural doğru, kalıp yanlış — ve kalıbı doğuran "
            "şey kuralın kendisi.* ⇒ **Her yeni kural, bir sonraki şablonun tohumu.**", "",
            "⭐ Bugün yazılan kurallar (§5a‴, §5a⁗, §8b′, §8c′, §8d′) bu riski taşıyor "
            "ve §8c′ bunu zaten bir kez gösterdi: «Bir şeye katılmıyorum» kalıbı §8c'nin "
            "kendi ürünüydü.", "",
            "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **Kapı YOK** | bu bir ölçüm; şablonlaşmayı yakalayan bir kapı yazılmadı |",
            "| ⛔ **Kalıplar elle** (K30) | sayı ALT SINIR; sözlükte olmayan şablonlar görünmez |",
            "| ⛔ **«Şablon = kusur» değil** | tekrarlanan bir cümle doğru da olabilir; ölçülen şey TEKRAR, yanlışlık değil |",
            "| ⚠️ Sürümler arası karşılaştırma | korpus büyüdükçe yeni partilerin payı artıyor; oran bunu düzeltir, mutlak sayı düzeltmez |", ""]
    CIKTI.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[4:]))
    print(f"→ {CIKTI.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
