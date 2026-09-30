#!/usr/bin/env python3
"""`v0.1.1` ön kaydı EK-3 çözümlemesi — koşucu değişti, tarif ve hüküm aynı (2026-09-30).

⭐ Zincir: bu betik → EK-2 çözümlemesi → EK-1 çözümlemesi → ana çözümleme. Hepsi mühürlü;
burada yalnız EK-3'ün eklediği iki denetim var, ikisi de puan OKUNMADAN önce:

  1. mühür      EK-3'ün mühürlediği dosyalar (basit defter + bu betik) bugünküyle aynı.
  2. koşucu     her Colab çıktı dizininin `ortam.json`'u `kosucu` = basit defter diyor VE
                kaydettiği `git_rev`'deki defter mühürlü defterle BİREBİR aynı ⇒ çıktı,
                mühürlü defterle üretilmiş. (`git_rev` bu depoda bulunmalı: Colab GitHub'dan
                klonladığı için her koşunun commit'i push edilmiş olmak zorunda.)

Sonra EK-2 çözümlemesi DEĞİŞTİRİLMEDEN koşar (ortam kilidi, tamlık, ölçüler, EK-1 hükmü).

Kullanım: önce `scripts/analiz/2026-09-29-v011-colab-puanla.py`, sonra bu betik.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
EK3 = KOK / "configs/deney/2026-09-30-v011-on-kayit-ek3.json"
DEFTER = "notebooks/v011-basit-egitim.ipynb"
KOLLAR = ("v010u", "v011u")


def _sha16(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]


def _modul(ad: str, yol: str):
    y = KOK / yol
    sp = _iu.spec_from_file_location(ad, y)
    m = _iu.module_from_spec(sp)
    argv, sys.argv = sys.argv[:], [str(y)]
    sp.loader.exec_module(m)
    sys.argv = argv
    return m


def muhur_denetle(e3: dict) -> None:
    kotu = [y for y, s in e3["muhurlu_dosyalar"].items()
            if not (KOK / y).exists() or _sha16((KOK / y).read_bytes()) != s]
    if kotu:
        raise SystemExit(f"⛔ EK-3 mührü bozuk — puan OKUNMADI: {kotu}")
    e2 = KOK / e3["ek2"]
    if _sha16(e2.read_bytes()) != e3["ek2_sha256_16"]:
        raise SystemExit("⛔ EK-2 EK-3'ün gördüğüyle aynı değil — puan OKUNMADI")


def kosucu_denetle(e3: dict, kok: Path = KOK / "reports/analiz") -> int:
    """Her Colab dizini mühürlü basit defterle mi üretilmiş. Denetlenen dizin sayısını döndürür."""
    beklenen = e3["muhurlu_dosyalar"][DEFTER]
    goruldu: dict[str, str] = {}
    n = 0
    for alt in ("eksen-kosu", "cok-turlu-kosu"):
        for kol in KOLLAR:
            for d in sorted((kok / alt).glob(f"*-{kol}-t*-*")):
                o = json.loads((d / "ortam.json").read_text(encoding="utf-8"))
                if o.get("kosucu") != DEFTER:
                    raise SystemExit(f"⛔ {d.name}: koşucu {o.get('kosucu')!r} ≠ {DEFTER} — puan OKUNMADI")
                rev = o["git_rev"]
                if rev not in goruldu:
                    r = subprocess.run(["git", "-C", str(KOK), "show", f"{rev}:{DEFTER}"], capture_output=True)
                    if r.returncode != 0:
                        raise SystemExit(f"⛔ {d.name}: git_rev {rev} bu depoda yok ya da defteri içermiyor — puan OKUNMADI")
                    goruldu[rev] = _sha16(r.stdout)
                if goruldu[rev] != beklenen:
                    raise SystemExit(f"⛔ {d.name}: {rev}'deki defter mühürlü defterden farklı "
                                     f"({goruldu[rev]} ≠ {beklenen}) — puan OKUNMADI")
                n += 1
    if n == 0:
        raise SystemExit("⛔ denetlenecek Colab dizini yok — önce paketi reports/analiz/ altına açın")
    return n


def main() -> int:
    e3 = json.loads(EK3.read_text(encoding="utf-8"))
    muhur_denetle(e3)
    n = kosucu_denetle(e3)
    print(f"✅ EK-3: mühür sağlam · {n} dizin mühürlü basit defterle üretilmiş")
    return _modul("_v011_ek2c", "scripts/analiz/2026-09-29-v011-onkayit-ek2-cozumleme.py").main()


if __name__ == "__main__":
    sys.exit(main())
