#!/usr/bin/env python3
"""T228 kararını kayıtlara işler — `ozerklik_vurgusu`.

⛔ **Yalnız OKUNAN 70 kayda dokunur.** `C` tabakasının okunmamış 297 kaydı
olduğu gibi kalır ve bu bir eksiklik olarak raporda durur: alanın %22'si
ölçülmüş bir ALT SINIR (T228, kestirim ~%34, %95 aralık %22-%50).

⛔ `is_negative`'den farklı olarak desen KALDIRILMIYOR: `A` tabakasının
tamamı okundu ve 24 kaydın 23'ü doğrulandı (%96) ⇒ özerklik deseni
fazla saymıyor, yalnız az sayıyor. Kaldırmak, işleyen bir hatırlatıcıyı
atmak olurdu.

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
RAPOR = KOK / f"reports/analiz/{TARIH}-ozerklik-beyani-uzlasmaya-gore.md"
YAZ = "--yaz" in sys.argv


def main() -> int:
    uz = json.loads((SP / "oz-uzlasma.json").read_text(encoding="utf-8"))
    anah = json.loads((SP / "oz-anahtar.json").read_text(encoding="utf-8"))
    kid = {v["kimlik"]: k for k, v in anah.items()}
    oy = {k: {o["id"]: o["ozerklik"] for o in json.loads((SP / a).read_text(encoding="utf-8"))}
          for k, a in (("A", "oz-A.json"), ("B", "oz-B.json"), ("C", "oz-C-benim.json"))}

    degisen, dokunulan, tutarsiz = [], 0, []
    for parti in sorted({k.split("#")[0] for k in uz}):
        for y in [KOK / f"data/candidates/{parti}.jsonl"] + \
                 sorted(KOK.glob(f"data/candidates/{parti}.blok*.jsonl")):
            if not y.exists():
                continue
            kay = [json.loads(l) for l in y.read_text(encoding="utf-8").splitlines() if l.strip()]
            deg = False
            for r in kay:
                kim = f"{parti}#{r['gen_meta']['parti_sira']}"
                if kim not in uz:
                    continue
                dokunulan += 1
                yeni = uz[kim]["karar"] == "evet"
                if r["gen_meta"].get("ozerklik_vurgusu") != yeni:
                    degisen.append((kim, y.name, uz[kim]["tabaka"],
                                    r["gen_meta"].get("ozerklik_vurgusu"), yeni))
                r["gen_meta"]["ozerklik_vurgusu"] = yeni
                r["gen_meta"]["ozerklik_kaynak"] = "T228-uzlastirma-2026-09-21"
                r["gen_meta"]["ozerklik_oylar"] = {k: oy[k][kid[kim]] for k in oy}
                deg = True
            if deg and YAZ:
                y.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kay),
                             encoding="utf-8")
    if YAZ:
        for parti in sorted({k.split("#")[0] for k in uz}):
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

    sat = ["# T228 kararının kayıtlara işlenmesi", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Kip:** {'YAZILDI' if YAZ else 'kuru koşu'}  ", "",
           f"Dokunulan kayıt örneği: **{dokunulan}** · değeri değişen: "
           f"**{len(degisen)}**", ""]
    if degisen:
        sat += ["| kayıt | dosya | tabaka | eski | **yeni** |", "|---|---|:-:|:-:|:-:|"]
        sat += [f"| `{k}` | `{d}` | {t} | {'var' if e else '—'} | "
                f"**{'var' if n else '—'}** |" for k, d, t, e, n in sorted(degisen)]
    sat += ["", f"⭐ Blok ↔ birleşik tutarsızlığı: **{len(tutarsiz)}**"
                + (f" — {tutarsiz}" if tutarsiz else ""), "",
            "## ⛔ Bu adımın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **297 kayıt OKUNMADI** | `C` tabakasının 323'ünden yalnız 26'sı "
            "okundu; alanın sayısı ölçülmüş bir ALT SINIR olarak kalıyor |",
            "| ⛔ **Üç anotatör de Claude** | T227'nin şerhi aynen geçerli |",
            "| ⛔ **`B` tabakası benim onaylarımdı ve `C` anotatörü de benim** | "
            "o sütunda kendi kararımı ikinci kez verdim |"]
    if YAZ:
        RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat))
    return 1 if tutarsiz else 0


if __name__ == "__main__":
    raise SystemExit(main())
