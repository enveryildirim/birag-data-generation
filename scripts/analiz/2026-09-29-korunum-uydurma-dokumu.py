#!/usr/bin/env python3
"""Korunum okumalarında `uydurma` dökümü — T302/T303'ün sayılarını raporlanır kılar.

T302 *«1144 okumanın yalnız 6'sında uydurma var, 2'si gerekçesinde cevabı anıyor»* ve
*«#0920'nin aynı paragrafına iki karşıt hüküm»* diyordu; ikisi de sohbette hesaplanmıştı
(Kural 7: tezde kullanılamaz). Bu betik ikisini depodan ve git geçmişinden yeniden üretir.

Kullanım: uv run python scripts/analiz/2026-09-29-korunum-uydurma-dokumu.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from kunye import betik_tarihi  # noqa: E402

DEPO = KOK / "data/candidates/v011-faz2.korunum.jsonl"
RAPOR = KOK / "reports/analiz/2026-09-29-korunum-uydurma-dokumu.md"
ID_0920 = "cb97048d226ea882ae9f6dfe"
ONCE, SONRA = "7aa5f57", "87a7b34"         # #0920 onarımından önce · sonra (blok 37 yeniden açıldı)


def _git_kayit(rev: str, kid: str) -> dict:
    out = subprocess.run(["git", "show", f"{rev}:data/candidates/v011-faz2-b37.jsonl"], cwd=KOK,
                         capture_output=True, text=True, check=True).stdout
    return next(json.loads(x) for x in out.splitlines() if x.strip() and json.loads(x)["id"] == kid)


def main() -> int:
    satir = [json.loads(x) for x in DEPO.read_text(encoding="utf-8").splitlines() if x.strip()]
    plan = {json.loads(x)["id"]: json.loads(x)["no"] for f in ("data/plan/v011-faz2.jsonl", "data/plan/v011-pilot.jsonl")
            for x in (KOK / f).read_text(encoding="utf-8").splitlines() if x.strip()}
    rub = collections.Counter(r["istem"] for r in satir)
    tablo = []
    for r in satir:
        u = r["sonuc"].get("uydurma") or []
        if u:
            neden = " ".join(i.get("neden") or "" for i in u)
            tablo.append((plan.get(r["id"], "?"), r["istem"], r["metin_sha"], bool(re.search(r"[Cc]evap", neden)),
                          (u[0].get("parca") or "")[:70]))
    v1 = [t for t in tablo if t[1] == "karar-korunumu.v1"]
    n_v1 = rub["karar-korunumu.v1"]

    # #0920: iki okuma, iki metin — işaretlenen 1. paragraf iki sürümde aynı mı?
    once, sonra = _git_kayit(ONCE, ID_0920), _git_kayit(SONRA, ID_0920)
    p_once = once["messages"][-1]["thinking"].split("\n\n")
    p_sonra = sonra["messages"][-1]["thinking"].split("\n\n")
    ayni = [i + 1 for i, (a, b) in enumerate(zip(p_once, p_sonra)) if a == b]
    ok = {r["metin_sha"]: r for r in satir if r["id"] == ID_0920 and r["istem"] == "karar-korunumu.v1"}

    s = ["# Korunum okumalarında `uydurma` dökümü (T302 · T303)", "",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {betik_tarihi(__file__)}  ",
         f"**Girdi:** `{DEPO.relative_to(KOK)}` SHA256-16 `{hashlib.sha256(DEPO.read_bytes()).hexdigest()[:16]}` · "
         f"{len(satir)} okuma satırı ({', '.join(f'`{k}` {v}' for k, v in sorted(rub.items()))})  ",
         "⚠️ Depo, metni sonradan değişen kayıtların **eski** okumalarını da saklar (bayat okumalar silinmez); sayılar okuma satırıdır, kayıt değil.", "",
         "## 1. `uydurma` işaretli okumalar", "",
         f"`karar-korunumu.v1`: **{len(v1)}/{n_v1}** okuma `uydurma` taşıyor · gerekçesinde **cevabı** anan: **{sum(t[3] for t in v1)}**", "",
         "| no | rubrik | metin SHA | gerekçe cevabı anıyor | işaretlenen parça |", "|---|---|---|---|---|"]
    s += [f"| {n} | `{i}` | `{m}` | {'✅' if c else '—'} | {p} |" for n, i, m, c, p in sorted(tablo)]
    s += ["", "## 2. #0920 — aynı paragrafa iki karşıt hüküm", "",
          f"Onarımdan önce (`{ONCE}`) ve sonra (`{SONRA}`) yeni düşünmenin paragrafları; **iki sürümde birebir aynı paragraflar: {ayni}**.", "",
          "| okuma (metin SHA) | `uydurma` |", "|---|---:|"]
    s += [f"| `{sha}` | {len(r['sonuc'].get('uydurma') or [])} |" for sha, r in sorted(ok.items())]
    s += ["", "⇒ `uydurma` işaretlenen 1. paragraf iki sürümde de aynıysa, iki okuma **aynı metne** zıt sert-kapı hükmü vermiştir "
          "(onarım yalnız 2. ve 4. paragrafa dokundu).", "",
          "## ⛔ Bunun söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ **Gürültü tabanı ölçülmedi** | tek bir kayıtta iki okuma; tasarlanmış bir iki-kör-okuyucu deneyi değil |",
          "| ⚠️ **«Cevabı anıyor» sözcük eşlemesi** | gerekçede *cevap* sözcüğü aranır; okuyucunun cevabı dayanak saydığını değil, andığını gösterir |"]
    RAPOR.write_text("\n".join(s) + "\n", encoding="utf-8")
    print(f"v1: {len(v1)}/{n_v1} uydurma · cevabı anan {sum(t[3] for t in v1)} · #0920 aynı paragraflar {ayni} · okumalar {[(k, len(v['sonuc'].get('uydurma') or [])) for k, v in ok.items()]}")
    print(f"yazıldı: {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
