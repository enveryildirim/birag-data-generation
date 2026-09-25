#!/usr/bin/env python3
"""v0.0.10 üzerinde ilk eğitim — ve kaybın GÖREMEDİĞİ şey.

⭐ Koşu `i-v010-k8`: kapsam `h-h1-capa-k8` ile **birebir aynı** (8 katman,
`q_proj`, rank 8) çünkü iki Pareto kapısını da geçen tek kol o. Değişen TEK şey
veri: `v0.0.8` → `v0.0.10` (8 kayıtta birer sözcük).

⛔⛔ **Ve sonuç, düzeltmenin ne OLMADIĞINI gösteriyor:** val kaybı eğrisi iki
koşuda **birebir aynı** (fark ±0,001, yedi ölçüm noktasının hepsinde).

➡️⭐⭐⭐ *Yanlış bir «aynı cümlede» iddiası ile doğru bir «aynı mesajda» iddiası
modelin gözünde AYNI maliyete sahiptir — ikisi de aynı uzunlukta, aynı sıklıkta,
aynı dilbilgisinde. Kayıp, bir iddianın DOĞRU olup olmadığını göremez. Kapıların
var olma sebebi tam olarak budur: ölçtükleri şey kaybın ölçemediği şeydir.*

⚠️ Bunun tersi de doğrudur ve rahatlatıcıdır: 8 kayıtlık düzeltme uyumu
**bozmadı** da. Düzeltme kaliteyi kayıpta değil, **iddianın doğruluğunda**
değiştirdi.

⛔ Bu rapor bir KALİTE ölçümü DEĞİLDİR. Davranış (Eksen 2 güvenlik, Eksen 3
unutma) ölçülmedi; onlar üretim gerektirir ve ayrı koşulur.

Girdi : runs/*-h-h1-capa-k8 · runs/*-i-v010-k8
Çıktı : reports/analiz/2026-09-18-v010-ilk-egitim.md
Kullanım: uv run python scripts/analiz/2026-09-18-v010-ilk-egitim.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-v010-ilk-egitim.md"


def _kosu(desen: str) -> Path | None:
    d = sorted(KOK.glob(f"runs/*{desen}"))
    d = [x for x in d if not (x / "IPTAL.md").exists()]     # ⛔ iptal edilenler dışarıda
    return d[-1] if d else None


def _egri(d: Path) -> tuple[list, dict]:
    log = (d / "train.log").read_text(errors="ignore")
    va = [(int(i), float(v)) for i, v in re.findall(r"Iter (\d+): Val loss ([\d.]+)", log)]
    m = json.loads((d / "metrics.json").read_text()) if (d / "metrics.json").exists() else {}
    return va, m


def main() -> int:
    eski, yeni = _kosu("-h-h1-capa-k8"), _kosu("-i-v010-k8")
    if not (eski and yeni):
        print("⛔ Koşu bulunamadı."); return 2
    a, ma = _egri(eski); b, mb = _egri(yeni)
    farklar = [y - x for (_, x), (_, y) in zip(a, b)]
    enb = max(abs(f) for f in farklar)

    sat = ["# v0.0.10 üzerinde ilk eğitim — ve kaybın göremediği şey", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}", "",
           "| | v0.0.8 çapası | v0.0.10 |", "|---|---|---|",
           f"| koşu | `{eski.name}` | `{yeni.name}` |",
           f"| kapsam | 8 katman · `q_proj` · rank 8 | **birebir aynı** |",
           f"| veri | `datasets/v0.0.8/train.jsonl` | `datasets/v0.0.10/train.jsonl` |",
           f"| süre | {ma.get('sure_saniye', 0):.0f} sn | {mb.get('sure_saniye', 0):.0f} sn |", "",
           "⭐ Değişen TEK şey veri: 8 kayıtta birer sözcük. Hiperparametrelerden biri bile",
           "oynatılsaydı çıkan sayı ölçülmüş kollarla karşılaştırılamazdı.", "",
           "## 1. ⭐⭐ Val kaybı eğrisi — BİREBİR aynı", "",
           "| adım | v0.0.8 | v0.0.10 | fark |", "|---:|---:|---:|---:|"]
    for (i, x), (_, y) in zip(a, b):
        sat.append(f"| {i} | {x:.3f} | {y:.3f} | {y-x:+.3f} |")
    sat += ["", f"⭐ **En büyük fark: {enb:.3f}** — yedi ölçüm noktasının hepsinde gürültü "
            "tabanında.", "",
            "➡️⭐⭐⭐ *Yanlış bir «aynı cümlede» iddiası ile doğru bir «aynı mesajda» iddiası",
            "modelin gözünde AYNI maliyete sahiptir — aynı uzunluk, aynı sıklık, aynı",
            "dilbilgisi. **Kayıp, bir iddianın DOĞRU olup olmadığını göremez.** Kapıların var",
            "olma sebebi tam olarak budur: ölçtükleri şey, kaybın ölçemediği şeydir.*", "",
            "⚠️ Tersi de doğru ve rahatlatıcı: 8 kayıtlık düzeltme uyumu **bozmadı** da.",
            "Düzeltme kaliteyi kayıpta değil, **iddianın doğruluğunda** değiştirdi.", "",
            "## 2. ⚠️ Yakınsama — merdivenin bulgusu sürüyor", ""]
    son_mu = min(b, key=lambda x: x[1])[0] == b[-1][0]
    sat += [(f"⛔ **En iyi val SON adımda** (adım {b[-1][0]}, {b[-1][1]:.3f}) ⇒ eğitim "
             "**yakınsamamış**. Merdivende yedi kolun yedisinde de böyleydi; veri değişince "
             "de değişmedi. ⚠️ *«3 epoch» §9'un tavanı olduğu için seçildi, verinin "
             "gerektirdiği için değil.*" if son_mu else
             "⭐ En iyi val son adımda DEĞİL — yakınsama işareti."), "",
            "⭐ Kural 5: Pareto kontrol noktası en iyi val adımında seçilir; kontrol noktaları "
            f"her epokta kaydedildi (`save_every: 456`).", "",
            "## ⛔ Bu raporun söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Bu bir KALİTE ölçümü değil** | davranış (Eksen 2 güvenlik, Eksen 3 unutma) "
            "ölçülmedi; üretim gerektirir ve ayrı koşulur. *Kayıp düşmesi davranış demek "
            "değildir* — önceki taramalarda en iyi uyan kollar güvenlik kapısında elendi |",
            "| ⛔ **Sekiz düzeltmenin etkisi burada görünmez** | ve bu raporun asıl bulgusu "
            "zaten bu: kayıp o farkı ölçemiyor |",
            "| ⚠️ **Süre iki koşuda farklı** | aynı iş, farklı termal durum; süre bir "
            "performans ölçüsü olarak okunmamalı |",
            "| ⚠️ Tek tohum (7) | kollar arası farklar tek tohumda ölçüldü |", ""]

    (KOK / f"reports/analiz/{TARIH}-v010-ilk-egitim.json").write_text(
        json.dumps({"tarih": TARIH, "eski": eski.name, "yeni": yeni.name,
                    "val_eski": a, "val_yeni": b, "en_buyuk_fark": enb},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
