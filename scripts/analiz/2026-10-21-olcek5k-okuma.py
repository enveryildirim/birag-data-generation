#!/usr/bin/env python3
"""Ölçek-5k — C sonrası örneklem okuması (Claude Code, K43: hata avı, puan değil).

Girdi : data/candidates/olcek5k.jsonl · data/plan/olcek5k.jsonl
Çıktı : reports/analiz/2026-10-21-olcek5k-okuma.md

Örneklem parça 191 HARİÇ çekilir (okuma, 191 üretilmeden önce yapıldı; 191 eklendiğinde
örneklem değişmesin diye). Okuma kararları aşağıdaki OKUMA sözlüğündedir.
"""
from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
GIRDI = KOK / "data/candidates/olcek5k.jsonl"
PLAN = KOK / "data/plan/olcek5k.jsonl"
RAPOR = KOK / "reports/analiz/2026-10-21-olcek5k-okuma.md"
TOHUM = 20261021

# id[:8] → (sınıf, not). sınıf: temiz · küçük · ciddi
OKUMA = {
    "c333c5c3": ("temiz", "ilgisiz bağlam kullanılmamış; özerklik cümlesi kalıba yakın"),
    "0a39bdfb": ("ciddi", "çok turlu yapı ters: ilk mesaj bütün anlatıyı taşıyor, ikinci mesaj onu tekrarlıyor; «zor olmuş olmalı» varsayımı"),
    "fd9fb625": ("temiz", "reçeteli ilaç → hekim; ders yok"),
    "e6fa12a5": ("temiz", ""),
    "efb9c8b0": ("ciddi", "A açılışı ilk mesajda olmayan «son» sözüne dayanıyor (ikinci mesajdan sızmış)"),
    "d1942eb0": ("temiz", ""),
    "b6f4d3bf": ("temiz", "kaynak türü doğru"),
    "420ee66b": ("temiz", "§5a″ sapması yerinde; izin_iste doğru"),
    "9b6fb9a7": ("temiz", ""),
    "1214e892": ("küçük", "nazikce_karsi_cikma hedefi için karşı çıkılacak iddia zayıf"),
    "64b2ded2": ("temiz", ""),
    "3ffaa85d": ("temiz", ""),
    "6d570a2a": ("küçük", "dil: «…sesin ise seni bırakmaya çektiğini söylüyor» özne bozuk"),
    "33c40c23": ("temiz", ""),
    "ef1a4ee8": ("küçük", "dil: «aileye söyleyemediğini ve utandığını» iki kez"),
    "b49bce77": ("temiz", ""),
    "edfaf9a4": ("temiz", "§8c′ göster-tartışma iyi"),
    "a91014f8": ("temiz", ""),
    "2ca6a84d": ("temiz", ""),
    "7e51f20d": ("temiz", "aldatma aracı reddi yerinde"),
}


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def main() -> int:
    parca = {hashlib.sha256(f"olcek5k-{r['sira']}".encode()).hexdigest()[:24]: r["parca"]
             for r in map(json.loads, PLAN.read_text(encoding="utf-8").splitlines())}
    R = [json.loads(x) for x in GIRDI.read_text(encoding="utf-8").splitlines()]
    R = [r for r in R if parca[r["id"]] != 191]
    random.seed(TOHUM)
    grup = lambda m: [r for r in R if m in r["gen_meta"]["generator_model"].split("C:")[1]]
    orneklem = [("haiku", r) for r in random.sample(grup("haiku"), 14)] + \
               [("sonnet", r) for r in random.sample(grup("sonnet"), 6)]
    sat = ["# Ölçek-5k — C sonrası örneklem okuması\n",
           f"- Betik: `scripts/analiz/{Path(__file__).name}` · tohum `{TOHUM}` · tarih 2026-10-21",
           f"- Girdi: `{GIRDI.relative_to(KOK)}` `{_sha(GIRDI)}` (parça 191 hariç {len(R)} kayıt)",
           "- Okuyan: Claude Code (K43 — hata avı; puan değil)\n",
           "| C modeli | n | temiz | küçük | ciddi |", "|---|---:|---:|---:|---:|"]
    for m in ("haiku", "sonnet"):
        s = [OKUMA[r["id"][:8]][0] for g, r in orneklem if g == m]
        sat.append(f"| {m} | {len(s)} | {s.count('temiz')} | {s.count('küçük')} | {s.count('ciddi')} |")
    sat += ["\n| id | C | slice | C kararı | sınıf | not |", "|---|---|---|---|---|---|"]
    for g, r in orneklem:
        k, n = OKUMA[r["id"][:8]]
        sat.append(f"| `{r['id'][:8]}` | {g} | {r['slice']} | {r['gen_meta'].get('c_karar')} | {k} | {n} |")
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
