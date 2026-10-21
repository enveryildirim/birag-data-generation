#!/usr/bin/env python3
"""Haiku pilotu — şablon sıklığı, `v6-parti8` (v0.1.1 içindeki hâli) ile kıyaslı.

⭐ 8 sözcüklük kapı birebir diziyi görür; okumada fark edilen kalıplar ondan
kısa ve esnek. Burada okumada görülen kalıplar SAYILIR (kalıp listesi
okumadan çıktı, ölçümden önce yazıldı — sonradan genişletilmedi).

Girdi : data/candidates/haiku-pilot.taslak.blok{1,2,3}.jsonl · datasets/v0.1.1/train.jsonl
Çıktı : reports/analiz/2026-10-20-haiku-pilot-sablon.md
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import tohum_guvenlik as TG  # noqa: E402

TASLAK = [KOK / f"data/candidates/haiku-pilot.taslak.blok{n}.jsonl" for n in (1, 2, 3)]
ZEMIN = KOK / "datasets/v0.1.1/train.jsonl"
RAPOR = KOK / "reports/analiz/2026-10-20-haiku-pilot-sablon.md"

# (ad, desen, nereye) — nereye: "son" = son cevap, "acilis" = çok turlu kaydın ara asistan turu,
# "thinking" = son turun thinking'i
KALIPLAR = [
    ("«… adım gibi duruyor / adım olabilir»", r"adım (gibi duruyor|olabilir|olur)", "son"),
    ("«yazman önemli / anlatman önemli»", r"(yazman|anlatman|söylemen|fark etmen)[^.?!]{0,40}önemli", "son"),
    ("«kolay olmamıştır / kolay olmaz»", r"kolay olma(mış|z)", "son"),
    ("«… duyuyorum»", r"duyuyorum", "son"),
    ("«… karar sende / senin kararın»", r"karar sende|senin kararın|karar(ı)? sana ait", "son"),
    ("«hüküm ver… / … bana düşmez»", r"hüküm (vermem|veremem|vermek|kurmak)|bana düşmez", "son"),
    ("iskele sözcüğü «adlandırıyorum / adıyla anıyorum»", r"adlandırıyorum|adıyla anıyorum", "son"),
    ("açılış «Dinliyorum / Buradayım»", r"^(dinliyorum|buradayım|anlat, buradayım|anlatıyorsun, dinliyorum)", "acilis"),
]


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def _haiku() -> list[dict]:
    out = []
    for f in TASLAK:
        for l in f.read_text(encoding="utf-8").splitlines():
            if l.strip():
                k = json.loads(l)
                ara = [c for r, c in k["turns"] if r == "assistant"]
                out.append({"son": k["son"], "thinking": k["thinking"] or "", "acilis": ara[0] if ara else None})
    return out


def _zemin() -> list[dict]:
    out = []
    for l in ZEMIN.read_text(encoding="utf-8").splitlines():
        r = json.loads(l)
        if not (r.get("gen_meta") or {}).get("parti", "").startswith("v6-parti8"):
            continue
        a = [m for m in r["messages"] if m["role"] == "assistant"]
        out.append({"son": a[-1]["content"], "thinking": a[-1].get("thinking") or "",
                    "acilis": a[0]["content"] if len(a) > 1 else None})
    return out


def _say(kayitlar: list[dict], desen: str, yer: str) -> tuple[int, int]:
    rx = re.compile(desen)
    havuz = [k[yer] for k in kayitlar if k[yer] is not None]
    return sum(1 for t in havuz if rx.search(TG.tr_fold(t).strip())), len(havuz)


def main() -> int:
    h, z = _haiku(), _zemin()
    sat = ["# Haiku pilotu — şablon sıklığı\n",
           f"- Betik: `scripts/analiz/{Path(__file__).name}`",
           "- Girdi: " + " · ".join(f"`{f.relative_to(KOK)}` `{_sha(f)}`" for f in TASLAK),
           f"- Zemin: `{ZEMIN.relative_to(KOK)}` `{_sha(ZEMIN)}`, yalnız `gen_meta.parti = v6-parti8*` ({len(z)} kayıt)",
           "- Sayım KAYIT başına (bir kayıtta kaç kez geçtiği değil, geçip geçmediği). "
           "Desenler `tr_fold` edilmiş metinde aranır.\n",
           "| kalıp | yer | Haiku | parti8 (Opus taslak + revizyon) |", "|---|---|---:|---:|"]
    for ad, desen, yer in KALIPLAR:
        d = TG.tr_fold(desen)
        hn, ht = _say(h, d, yer)
        zn, zt = _say(z, d, yer)
        sat.append(f"| {ad} | {yer} | {hn}/{ht} (%{100 * hn / max(ht, 1):.0f}) | "
                   f"{zn}/{zt} (%{100 * zn / max(zt, 1):.0f}) |")
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
