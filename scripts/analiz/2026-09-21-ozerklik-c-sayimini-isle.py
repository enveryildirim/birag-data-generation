#!/usr/bin/env python3
"""T229'un `C` tabakası sayımını kayıtlara işler.

⛔ Yalnız `C` tabakasına dokunur. `A` ve `B` tabakalarının hükmü T228'den
geliyor ve değişmiyor.

⭐ Kaynak kayda yazılıyor: `ozerklik_kaynak = T229-sayim-2026-09-21` ve
`ozerklik_oylar` içinde `X`, `Y` ve gerekiyorsa hakem oyu duruyor.
⛔ T228'de okunan 26 kaydın kaynağı `T228`de kalıyor (hükümleri değişmedi,
%100 tekrar uyumu) — hangi turun yazdığı ayırt edilebilsin diye.

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
RAPOR = KOK / f"reports/analiz/{TARIH}-ozerklik-c-sayimini-isle.md"
YAZ = "--yaz" in sys.argv


def main() -> int:
    karar = json.loads((SP / "cs-karar.json").read_text(encoding="utf-8"))
    anah = json.loads((SP / "cs-anahtar.json").read_text(encoding="utf-8"))
    kid = {v["kimlik"]: k for k, v in anah.items()}
    tekrar = {v["kimlik"] for v in anah.values() if v["tekrar"]}
    hakem = json.loads((SP / "cs-hakem.json").read_text(encoding="utf-8"))
    oy = {}
    for kod in ("X", "Y"):
        oy[kod] = {}
        for b in range(1, 5):
            for o in json.loads((SP / f"cs-{kod}-{b}.json").read_text(encoding="utf-8")):
                oy[kod][o["id"]] = o["ozerklik"]

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
                if kim in tekrar:
                    # ⛔ Bu kayıt T228'de de okunmuştu ve iki tur AYNI hükme
                    #    vardı; kaynağı değiştirmiyorum, oyları birleştiriyorum.
                    r["gen_meta"].setdefault("ozerklik_oylar", {}).update(
                        {f"T229-{k}": v for k, v in oylar.items()})
                else:
                    r["gen_meta"]["ozerklik_kaynak"] = "T229-sayim-2026-09-21"
                    r["gen_meta"]["ozerklik_oylar"] = oylar
                deg = True
            if deg and YAZ:
                y.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kay),
                             encoding="utf-8")

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

    top = 0
    if YAZ:
        for i in range(1, 8):
            top += sum(1 for l in (KOK / f"data/candidates/v6-parti{i}.jsonl").read_text(
                encoding="utf-8").splitlines() if l.strip()
                and json.loads(l)["gen_meta"]["ozerklik_vurgusu"])

    sat = ["# T229 sayımının kayıtlara işlenmesi", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Kip:** {'YAZILDI' if YAZ else 'kuru koşu'}  ", "",
           f"Dokunulan kayıt örneği: **{dokunulan}** · değeri değişen: "
           f"**{len(degisen)}** ({len(degisen)//2} kayıt)", ""]
    if degisen:
        sat += ["| kayıt | dosya | eski | **yeni** |", "|---|---|:-:|:-:|"]
        sat += [f"| `{k}` | `{d}` | {'var' if e else '—'} | **{'var' if n else '—'}** |"
                for k, d, e, n in sorted(degisen)]
    sat += ["", f"⭐ Blok ↔ birleşik tutarsızlığı: **{len(tutarsiz)}**"
                + (f" — {tutarsiz}" if tutarsiz else ""),
            f"  ·  korpus özerklik beyanı: **{top}/412**" if YAZ else "", "",
            "## ⛔ Bu adımın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **`B` tabakası hâlâ örneklem** | 65 kaydın 20'si okundu (T228) ⇒ "
            "korpus sayısının o bileşeni bir kestirim olarak kalıyor |",
            "| ⛔ **İki anotatör + hakem** | ayrışmayan kayıtların iki oyu var, üç değil |",
            "| ⛔ **Üçü de Claude** | T227'den beri süren şerh |"]
    if YAZ:
        RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[:8]))
    print("\n".join(sat[-9:]))
    return 1 if tutarsiz else 0


if __name__ == "__main__":
    raise SystemExit(main())
