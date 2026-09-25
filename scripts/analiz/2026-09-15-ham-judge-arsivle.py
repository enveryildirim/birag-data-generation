#!/usr/bin/env python3
"""Subagent judge'ların HAM çıktısını repoya alır — oturum scratchpad'i silinmeden.

Neden gerekli: `judge-sonuclari-topla.py` ham JSON'u `turet()`ten geçirir ve
`JudgeResult` şeması bilinmeyen alanları sessizce düşürür. İkisi birden şu bilgiyi
yok eder: **judge hangi alanı hiç yazmadı.** v7'nin çıktı şablonu gerekçesi tam olarak
buna dayanıyor (aynı dalgada 28 kayıt alanı yazdı, 20 kayıt yazmadı) ve scratchpad
Kural 8'de silinecek. Ham metin burada olmazsa o sayı bir daha üretilemez.

Kullanım: uv run python scripts/analiz/2026-09-15-ham-judge-arsivle.py
"""
from __future__ import annotations

import json
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
ISLER = Path("/private/tmp/claude-501/-Users-pc-projects-birag-data-finetuning"
             "/fe6477c2-8e5e-439e-875d-df2b5ed62d91/scratchpad/judge-isleri")
HEDEF = KOK / "reports/analiz/ham-judge"


def main() -> None:
    HEDEF.mkdir(parents=True, exist_ok=True)
    for dizin in sorted(p for p in ISLER.iterdir() if (p / "sonuc").is_dir()):
        yollar = sorted((dizin / "sonuc").glob("*.json"))
        if not yollar:
            print(f"{dizin.name}: sonuç yok, atlandı")
            continue
        # 2026-09-15: `kol`/`rol` de yazılıyor. Önceden yalnızca `no`+`id` vardı ve
        # hakemlik geçişlerinde bu YETMİYORDU: 54 kaydın hangi kola ait olduğu yalnızca
        # scratchpad'deki `kimlikler.json`'daydı, yani yayımlanmış judge sayıları
        # oturum silinince yeniden türetilemiyordu (Kural 7 açığı, K117'de bulundu).
        kimlik = {k["no"]: k
                  for k in json.loads((dizin / "kimlikler.json").read_text())}
        cikti = HEDEF / f"{dizin.name}.jsonl"
        with cikti.open("w") as f:
            for y in yollar:
                # HAM metin — ayrıştırılmadan. Alanın YOKLUĞU da kanıttır.
                k = kimlik.get(y.stem) or {}
                kayit = {"no": y.stem, "id": k.get("id")}
                for ek in ("kol", "rol"):
                    if k.get(ek):
                        kayit[ek] = k[ek]
                kayit["ham"] = y.read_text()      # HAM metin — alanın YOKLUĞU da kanıttır
                f.write(json.dumps(kayit, ensure_ascii=False) + "\n")
        print(f"{dizin.name}: {len(yollar)} kayıt → {cikti.relative_to(KOK)}")


if __name__ == "__main__":
    main()
