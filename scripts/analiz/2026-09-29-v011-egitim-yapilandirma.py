#!/usr/bin/env python3
"""`v0.1.1` kolunun 8 eğitim yapılandırması — `e3`'ünkilerden TÜRETİLİR (K277 · Faz 3).

⭐⭐ DEĞİŞEN TEK ŞEY VERİ: `ad` ve `dataset` dışında her alan `e3-celiskili-k8qo-v022-t*`
ile birebir (assert). `e3`'ün verisi `datasets/v0.0.22` = `datasets/v0.1.0` (bayt bayt,
SHA256-16 `6fcb6b1e16290575`) ⇒ iki kol arasındaki tek fark `v0.1.1`'in yeniden kurulmuş
düşünmesi ve 9 son cümledir.

⛔ `datasets/v0.1.1/train.jsonl` henüz YOK: Faz 4'ün ilk adımı hazırlık dosyasını
(`data/candidates/v011-derleme.jsonl`) ön kayıttaki SHA ile dondurmaktır.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

KOK = Path(__file__).resolve().parents[2]
TOHUM = [7, 13, 23, 31, 37, 41, 43, 47]
BASLIK = """# `v0.1.1` KOLU — ön kayıt: configs/deney/2026-09-29-v011-on-kayit.json (K277 · Faz 3)
#
# ⭐⭐ DEĞİŞEN TEK ŞEY VERİ. Bu dosya `configs/training/e3-celiskili-k8qo-v022-t{t}.yaml`'dan
# `scripts/analiz/2026-09-29-v011-egitim-yapilandirma.py` ile türetildi; `ad` ve `dataset`
# dışında her alan birebir (betik assert eder). Karşılaştırma kolu `e3` (= `v0.1.0`).
# ⛔ Elle düzenleme — betiği yeniden koş.
"""


def main() -> int:
    for t in TOHUM:
        kaynak = KOK / f"configs/training/e3-celiskili-k8qo-v022-t{t}.yaml"
        e3 = yaml.safe_load(kaynak.read_text(encoding="utf-8"))
        assert e3["dataset"] == "datasets/v0.0.22/train.jsonl" and e3["mlx"]["seed"] == t, kaynak
        yeni = {**e3, "ad": f"v011-k8qo-t{t}", "dataset": "datasets/v0.1.1/train.jsonl"}
        fark = {k for k in set(e3) | set(yeni) if e3.get(k) != yeni.get(k)}
        assert fark == {"ad", "dataset"}, fark
        hedef = KOK / f"configs/training/v011-k8qo-t{t}.yaml"
        hedef.write_text(BASLIK.format(t=t) + yaml.safe_dump(yeni, allow_unicode=True, sort_keys=False),
                         encoding="utf-8")
        assert yaml.safe_load(hedef.read_text(encoding="utf-8")) == yeni
    print(f"✅ {len(TOHUM)} yapılandırma · değişen alan yalnız ad + dataset")
    return 0


if __name__ == "__main__":
    sys.exit(main())
