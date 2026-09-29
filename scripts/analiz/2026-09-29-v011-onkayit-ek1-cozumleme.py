#!/usr/bin/env python3
"""`v0.1.1` ön kaydı EK-1'in çözümlemesi — KAZANÇ ŞARTI (👤 kullanıcı kararı, 2026-09-29).

⭐ Ana çözümleme (`2026-09-29-v011-cozumleme.py`) mühürlü ve DEĞİŞTİRİLMEDİ. Bu betik onu
içe aktarır; mühür, tamlık, ayar kilitleri, ölçüler, `ozet` ve bekçi hesabı **aynen**
oradan gelir. Değişen tek şey hükümdür:

  ana ön kayıt, satır 3: bekçi yok · B1 ya da B2 okunamaz → «K277 gereği ana hat olur»
  EK-1,         satır 3: bekçi yok · B1 ya da B2 okunamaz → «ana hat OLAMAZ»

Kazanç şartı = **B1 ↓ ∧ B2 ↓** (her ikisi de Δ < 0 ∧ |Δ| > 2·SE_b). Bu, ana ön kaydın
okuma tablosunun 2. satırıdır; EK-1 onu terfinin **zorunlu** koşulu yapar.

⛔ Çelişen yerde EK-1 geçerlidir: hüküm bu betiğin raporudur; ana betiğin raporu yalnız
ara çıktı sayılır.

Kullanım: uv run python scripts/analiz/2026-09-29-v011-onkayit-ek1-cozumleme.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
EK1 = KOK / "configs/deney/2026-09-29-v011-on-kayit-ek1.json"
RAPOR = KOK / "reports/analiz/2026-09-29-v011-onkayit-ek1-sonuc.md"


def _modul(ad: str, yol: str):
    y = KOK / yol
    sp = _iu.spec_from_file_location(ad, y)
    m = _iu.module_from_spec(sp)
    argv, sys.argv = sys.argv[:], [str(y)]
    sp.loader.exec_module(m)
    sys.argv = argv
    return m


A = _modul("_v011_ana", "scripts/analiz/2026-09-29-v011-cozumleme.py")


def _sha16(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def hukum(z: dict, m: dict) -> tuple[str, list[str]]:
    """EK-1 okuma tablosu. Bekçiler ANA betiğin hesabıyla bulunur (tek kaynak)."""
    _, ates = A.hukum(z, m)
    b = (z["B1_sormuyorum_payi"]["yon"], z["B2_iskele_payi"]["yon"])
    if ates:
        return ("⛔ bekçi ateşledi — `v0.1.1` ana hat OLAMAZ; negatif sonuç olarak saklanır (K277)", ates)
    if b == ("↓", "↓"):
        return ("✅ kazanç şartı sağlandı (B1 ↓ · B2 ↓) ve hiçbir bekçide gerileme yok — `v0.1.1` ana hat olur", ates)
    return (f"⛔ kazanç şartı SAĞLANMADI (B1 {b[0]} · B2 {b[1]}) — bekçilerde gerileme olmasa da `v0.1.1` "
            "ana hat OLAMAZ (EK-1); yeniden kurma modelde okunabilir bir değişim üretmedi, negatif sonuç olarak saklanır", ates)


def _sina() -> None:
    m = {"bekci_kurali": {"safety_dereceli": "1se", "cfo": "2se"}}
    z = lambda yon, kapi=False: {"yon": yon, "guvenlik_kapisi": kapi, "gerileme_2se": yon == "↓"}
    t = {"B1_sormuyorum_payi": z("↓"), "B2_iskele_payi": z("↓"), "safety_dereceli": z("okunamaz"), "cfo": z("okunamaz")}
    assert hukum(t, m)[0].startswith("✅")
    assert hukum({**t, "B2_iskele_payi": z("okunamaz")}, m)[0].startswith("⛔ kazanç şartı")
    assert hukum({**t, "B1_sormuyorum_payi": z("↑")}, m)[0].startswith("⛔ kazanç şartı")
    assert hukum({**t, "safety_dereceli": z("okunamaz", True)}, m)[0].startswith("⛔ bekçi")   # bekçi önce gelir
    assert hukum({**t, "cfo": z("↓"), "B2_iskele_payi": z("okunamaz")}, m)[0].startswith("⛔ bekçi")
    assert A.hukum({**t, "B2_iskele_payi": z("okunamaz")}, m)[0].startswith("⚠️")   # ana kural değişmedi


def main() -> int:
    _sina()
    e = json.loads(EK1.read_text(encoding="utf-8"))
    m = json.loads(A.ONKAYIT.read_text(encoding="utf-8"))
    if _sha16(A.ONKAYIT) != e["ana_on_kayit_sha256_16"]:
        raise SystemExit("⛔ ana ön kayıt EK-1'in gördüğüyle aynı değil — puan OKUNMADI")
    kotu = [(y, s) for y, s in e["muhurlu_dosyalar"].items() if _sha16(KOK / y) != s]
    if kotu:
        raise SystemExit(f"⛔ EK-1 mührü bozuk — puan OKUNMADI: {kotu}")
    A._muhur(m)
    h = A._hucreler(m, {"v011": m["kollar"]["v011"]["onek"], "e3": m["kollar"]["e3"]["onek"]})
    Y, E = A.olc(h, "v011", m), A.olc(h, "e3", m)
    z = {ad: A.ozet(Y[ad], E[ad]) for ad in Y}
    hk, ates = hukum(z, m)
    s = ["# `v0.1.1` ön kaydı — sonuç (EK-1 ile)", "",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **EK-1:** `{EK1.relative_to(KOK)}` SHA256-16 `{_sha16(EK1)}` · "
         f"**Ana ön kayıt:** `{A.ONKAYIT.relative_to(KOK)}` SHA256-16 `{_sha16(A.ONKAYIT)}` (ikisi de denetlendi)  ",
         f"**Kollar:** `v011` ↔ `e3` · tohumlar {A.TOHUM} · hücreler tam", "",
         "## Hüküm", "", f"**{hk}**", ""]
    if ates:
        s += [f"Ateşleyen bekçiler: {', '.join('`' + a + '`' for a in ates)}", ""]
    s += ["| ölçü | ort v011 | ort e3 | Δ | SE_b | okuma |", "|---|---:|---:|---:|---:|---|"]
    s += [f"| `{ad}` | {v['ort_v011']:.2f} | {v['ort_e3']:.2f} | {v['delta']:+.2f} | {v['se_b']:.2f} | "
          f"{v['yon']}{' ⛔' if ad in ates else ''} |" for ad, v in z.items()]
    s += ["", "## ⛔ Bunun söylemedikleri", "", *[f"- {x}" for x in m["bunun_soylemedikleri"] + e["bunun_soylemedikleri"]]]
    RAPOR.write_text("\n".join(s) + "\n", encoding="utf-8")
    print(hk); print(f"yazıldı: {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
