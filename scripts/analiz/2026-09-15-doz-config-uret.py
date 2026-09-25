#!/usr/bin/env python3
"""Doz-yanıt koşu config'lerini `f4b` ailesinden türetir.

⭐ Bu betiğin asıl işi config yazmak DEĞİL, tasarımın merkezî iddiasını DOĞRULAMAK:
«korpus boyu sabit tutulduğu için adım sayısı değişmek zorunda değil.»

K113'ün kontrol kolu adımın metriği veriden daha çok oynattığını ölçmüştü. Doz eğrisi
ancak adım sabitse okunabilir. N = 155 sabit olduğu için valid bölmesi (124/31) de,
`iters` (372) de, `steps_per_eval`, `save_every`, LR ve seed de aynen kalıyor.

Betik bunu iddia etmiyor, DENETLİYOR: üretilen her config `f4b` karşılığıyla satır satır
karşılaştırılır ve `ad` + `dataset` DIŞINDA bir fark bulunursa DURUR.
"""
from __future__ import annotations

import difflib
import re
from pathlib import Path

KOK = Path(__file__).parent.parent.parent
CFG = KOK / "configs/training"
KOLLAR = ["A-dar", "B-derin", "C-dikkat", "D-tam", "E-genis"]
DOZLAR = {"doz10": ("v0.0.4", "%10,2"), "doz25": ("v0.0.5", "%24,1")}

BASLIK = """# Faz 4 · T30 DOZ-YANIT EĞRİSİ — kol "{kol}" · korpus {surum} (yönlendirme {oran})
#
# ⛔ `f4-kapsam-*.yaml` (birinci koşu, v0.0.2) ve `f4b-kapsam-*.yaml` (ikinci koşu,
# v0.0.3) DEĞİŞTİRİLMEDİ — Kural 7. Bu üçüncü aile ayrı yazıldı.
#
# NEDEN: T30 negatif çıktı — yönlendirmeyi %5,1 dozunda geri koymak refleksi geri
# getirmedi. İki açıklama ayırt edilemedi: (a) doz yetersiz, (b) ilişki asimetrik.
# Doz-yanıt eğrisi bunu ayıran tek deney. Ölçülü noktalar: %2,0 · %5,1. Bu aile
# %10,2 ve %24,1 noktalarını ekliyor.
#
# ⭐ TEK DEĞİŞKEN: `dataset`. Adım sayısı, LR, tohum, LoRA kapsamı, valid bölmesi —
# hepsi `f4b-kapsam-{kol}.yaml` ile BİREBİR aynı. Korpus boyu {n} kayıtta sabit
# tutulduğu için §9'un 3-epoch kuralı adımı oynatmıyor: 124 eğitim kaydı, 372 adım.
# K113'te iki değişken birden oynamıştı (veri + adım) ve kontrol kolu gerekmişti;
# bu ailede o karışma YOK.
"""


def main() -> None:
    n = sum(1 for _ in (KOK / "datasets/v0.0.3/train.jsonl").open())
    hata, yazilan = [], []
    for kol in KOLLAR:
        kaynak = CFG / f"f4b-kapsam-{kol}.yaml"
        if not kaynak.exists():
            raise SystemExit(f"⛔ kaynak config yok: {kaynak.relative_to(KOK)}")
        ham = kaynak.read_text()
        govde = ham[ham.index("ad: "):]          # başlık yorumlarını at
        for etiket, (surum, oran) in DOZLAR.items():
            yeni_ad = f"f4c-{etiket}-{kol}"
            g = re.sub(r"^ad: .*$", f"ad: {yeni_ad}", govde, count=1, flags=re.M)
            g = re.sub(r"^dataset: .*$",
                       f"dataset: datasets/{surum}/train.jsonl"
                       f"         # {n} kayıt — v0.0.3 ile AYNI boy, yönlendirme {oran}",
                       g, count=1, flags=re.M)
            metin = BASLIK.format(kol=kol, surum=surum, oran=oran, n=n) + "\n" + g
            yol = CFG / f"{yeni_ad}.yaml"
            yol.write_text(metin, encoding="utf-8")
            yazilan.append(yol.name)

            # ─── DOĞRULAMA: `ad` + `dataset` dışında fark olmamalı ───────────
            a = [l for l in govde.splitlines()]
            b = [l for l in g.splitlines()]
            farklar = [l for l in difflib.unified_diff(a, b, lineterm="", n=0)
                       if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]
            izinli = [l for l in farklar
                      if re.match(r"^[+-](ad: |dataset: )", l)]
            if len(farklar) != len(izinli):
                hata.append(f"{yeni_ad}: izinsiz fark → "
                            + " | ".join(l for l in farklar if l not in izinli))
    if hata:
        raise SystemExit("⛔ TEK DEĞİŞKEN İLKESİ BOZULDU:\n" + "\n".join(f"  - {h}" for h in hata))
    print(f"{len(yazilan)} config yazıldı, hepsi `f4b` karşılığından YALNIZCA "
          f"`ad` ve `dataset` satırında farklı:")
    for ad in yazilan:
        print(f"  configs/training/{ad}")
    print(f"\n⭐ adım sayısı DEĞİŞMEDİ (372) — korpus boyu {n}'te sabit tutulduğu için "
          f"K113'ün veri↔adım karışması bu ailede yok.")


if __name__ == "__main__":
    main()
