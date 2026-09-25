#!/usr/bin/env python3
"""T230'un `B` tabakası sayımını kayıtlara işler.

⛔ Yalnız `B` tabakasına dokunur. `A` T228'den, `C` T229'dan geliyor.
⭐ Bu adımdan sonra korpusun `ozerklik_vurgusu` sayısında KESTİRİM
bileşeni kalmıyor: üç tabakanın üçü de tam sayıldı.

Kullanım: uv run python ... [--yaz]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
# Girdi: depodaki kalıcı kopya (bkz. data/anotasyon/OKU.md).
SP = KOK / "data/anotasyon"
RAPOR = KOK / f"reports/analiz/{TARIH}-ozerklik-b-sayimini-isle.md"
YAZ = "--yaz" in sys.argv


def main() -> int:
    karar = json.loads((SP / "bs-karar.json").read_text(encoding="utf-8"))
    anah = json.loads((SP / "bs-anahtar.json").read_text(encoding="utf-8"))
    kid = {v["kimlik"]: k for k, v in anah.items()}
    hakem = json.loads((SP / "bs-hakem.json").read_text(encoding="utf-8"))
    hakem.pop("_ilke", None)
    oy = {k: {o["id"]: o["ozerklik"]
              for o in json.loads((SP / f"bs-{k}.json").read_text(encoding="utf-8"))}
          for k in ("X", "Y")}

    degisen, dokunulan, tutarsiz = [], 0, []
    for parti in sorted({k.split("#")[0] for k in karar}):
        for y in [KOK / f"data/candidates/{parti}.jsonl"] + \
                 sorted(KOK.glob(f"data/candidates/{parti}.blok*.jsonl")):
            if not y.exists():
                continue
            kay = [json.loads(l) for l in y.read_text(encoding="utf-8").splitlines() if l.strip()]
            deg = False
            for r in kay:
                kim = f"{parti}#{r['gen_meta']['parti_sira']}"
                if kim not in karar:
                    continue
                dokunulan += 1
                yeni = karar[kim] == "evet"
                if r["gen_meta"].get("ozerklik_vurgusu") != yeni:
                    degisen.append((kim, y.name, r["gen_meta"].get("ozerklik_vurgusu"), yeni))
                r["gen_meta"]["ozerklik_vurgusu"] = yeni
                i_ = kid[kim]
                oylar = {"X": oy["X"][i_], "Y": oy["Y"][i_]}
                if i_ in hakem:
                    oylar["H"] = hakem[i_]
                r["gen_meta"]["ozerklik_kaynak"] = "T230-sayim-2026-09-21"
                r["gen_meta"]["ozerklik_oylar"] = oylar
                deg = True
            if deg and YAZ:
                y.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kay),
                             encoding="utf-8")
    top = kayit = 0
    if YAZ:
        for parti in sorted({k.split("#")[0] for k in karar}):
            bir = {json.loads(l)["gen_meta"]["parti_sira"]:
                   json.loads(l)["gen_meta"]["ozerklik_vurgusu"]
                   for l in (KOK / f"data/candidates/{parti}.jsonl").read_text(
                       encoding="utf-8").splitlines() if l.strip()}
            for b in sorted(KOK.glob(f"data/candidates/{parti}.blok*.jsonl")):
                for l in b.read_text(encoding="utf-8").splitlines():
                    if l.strip():
                        r = json.loads(l)
                        s = r["gen_meta"]["parti_sira"]
                        if s in bir and bir[s] != r["gen_meta"]["ozerklik_vurgusu"]:
                            tutarsiz.append(f"{parti}#{s}")
        for i in range(1, 8):
            for l in (KOK / f"data/candidates/v6-parti{i}.jsonl").read_text(
                    encoding="utf-8").splitlines():
                if l.strip():
                    kayit += 1
                    top += json.loads(l)["gen_meta"]["ozerklik_vurgusu"]

    sat = ["# T230 sayımının kayıtlara işlenmesi", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Kip:** {'YAZILDI' if YAZ else 'kuru koşu'}  ", "",
           f"Dokunulan kayıt örneği: **{dokunulan}** · değeri değişen: "
           f"**{len(degisen)}** ({len(degisen)//2} kayıt)", ""]
    if degisen:
        sat += ["| kayıt | dosya | eski | **yeni** |", "|---|---|:-:|:-:|"]
        sat += [f"| `{k}` | `{d}` | {'var' if e else '—'} | **{'var' if n else '—'}** |"
                for k, d, e, n in sorted(degisen)]
    sat += ["", f"⭐ Blok ↔ birleşik tutarsızlığı: **{len(tutarsiz)}**"
                + (f" — {tutarsiz}" if tutarsiz else "")]
    if YAZ:
        sat += [f"  ·  korpus özerklik beyanı: **{top}/{kayit} "
                f"(%{round(100*top/kayit)})**"]
    sat += ["", "## ⛔ Bu adımın söylemedikleri", "", "| | |", "|---|---|",
            "| ⭐ **Kestirim bileşeni kalmadı** | `A`(24) + `B`(65) + `C`(323) = 412, "
            "üçü de tam sayıldı |",
            "| ⛔⛔ **Hakem denetlenen onayların sahibi** | `B` tabakasında ayrışan "
            "7 kayıtta kendi onayımı üçüncü kez değerlendirdim |",
            "| ⛔ **Üçü de Claude** | T227'den beri süren şerh |"]
    if YAZ:
        RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat))
    return 1 if tutarsiz else 0


if __name__ == "__main__":
    raise SystemExit(main())
