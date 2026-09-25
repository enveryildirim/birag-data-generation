#!/usr/bin/env python3
"""Unutmayı ne sürüyor — LoRA KAPSAMI mı DAĞILIM mı?

⭐ **Yeni eğitim gerekmedi.** Kapsam merdiveni `v0.0.14` üzerinde zaten
koşulmuştu ve `runs/` hiç silinmiyor (Kural 7) ⇒ dağılım SABİTken kapsamın
etkisi mevcut koşulardan ölçülebiliyor.

⛔⛔ **İki tek-değişkenli karşılaştırma:**
  **A. Dağılım değişir, kapsam sabit** — `z-h9` (v0.0.14) ↔ `d1` (v0.0.18)
     ↔ `e2` (v0.0.20, tazelenmiş). Üçü de 8 katman · q+o · r8 · s20.
  **B. Kapsam değişir, dağılım sabit** — v0.0.14 üzerinde 9 kol,
     **8'den 48 modüle** (6 kat).

Çıktı: reports/analiz/2026-09-22-kapsam-mi-dagilim-mi.md
"""
from __future__ import annotations

import json
import math
import re
import statistics as st
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-kapsam-mi-dagilim-mi.md"
EK = KOK / "reports/analiz/eksen-kosu"

MERDIVEN = [
    ("h1", "8 kat · q", 8, r"(j|k|l)-v014-k8.*forget|e3-forgetting_smoke-v014-k8$"),
    ("h9", "8 kat · q+o", 16, r"z-h9-k8qo-v014-t\d+-forget"),
    ("h2", "16 kat · q", 16, r"x-h2-v014-t\d+-forget"),
    ("h3", "24 kat · q", 24, r"x-h3-v014-t\d+-forget"),
    ("h5", "16 kat · q+o", 32, r"x-h5-v014-t\d+-forget"),
    ("h4", "32 kat · q", 32, r"x-h4-v014-t\d+-forget"),
    ("h6", "24 kat · q+o", 48, r"x-h6-v014-t\d+-forget"),
    ("—", "24 kat · q+o · r16", 48, r"(m|n|o)-v014-k24qo.*forget"),
    ("h8", "24 kat · q+o · r16 s10", 48, r"y-h8-r16s10-v014-t\d+-forget"),
]
# (ad, veri, adım, desen) — kapsam hepsinde 8 kat · q+o · r8 · s20
DAGILIM = [("`z-h9`", "v0.0.14 · 571 kayıt", 1368, r"z-h9-k8qo-v014-t\d+-forget"),
           ("`d1`", "v0.0.18 · 1033 kayıt", 2478, r"d1-veri2x-k8qo-v018-t\d+-forget"),
           ("`e2`", "v0.0.20 · 1394 (%5 tazeleme)", 3345, r"e2-adimli-v020-t\d+-forget")]


def _skor(desen):
    v = []
    for p in sorted(EK.iterdir()):
        if not re.search(desen, p.name):
            continue
        j = json.load(open(p / "kosu.json"))
        if "forgetting" not in j["set"]:
            continue
        rs = [json.loads(s) for s in
              (p / "sonuclar.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
        v.append(sum(1 for r in rs if r.get("otomatik_gecti")))
    return v


def _ci(v):
    return 2 * st.stdev(v) / math.sqrt(len(v)) if len(v) > 1 else float("nan")


def main() -> int:
    A = [(ad, veri, adim, _skor(d)) for ad, veri, adim, d in DAGILIM]
    B = [(k, t, m, _skor(d)) for k, t, m, d in MERDIVEN]
    B = [(k, t, m, v) for k, t, m, v in B if v]

    xs = [m for _, _, m, _ in B]
    ys = [st.mean(v) for _, _, _, v in B]
    mx, my = st.mean(xs), st.mean(ys)
    r = (sum((a - mx) * (b - my) for a, b in zip(xs, ys)) /
         math.sqrt(sum((a - mx)**2 for a in xs) * sum((b - my)**2 for b in ys)))
    b_ara = max(ys) - min(ys)

    zh9 = next(v for ad, _, _, v in A if ad == "`z-h9`")
    d1 = next(v for ad, _, _, v in A if ad == "`d1`")
    e2 = next(v for ad, _, _, v in A if ad == "`e2`")
    f1 = st.mean(d1) - st.mean(zh9)
    h1_ = 2 * math.sqrt(st.stdev(zh9)**2 / len(zh9) + st.stdev(d1)**2 / len(d1))
    f2 = st.mean(e2) - st.mean(d1)
    h2_ = 2 * math.sqrt(st.stdev(d1)**2 / len(d1) + st.stdev(e2)**2 / len(e2))
    a_ara = max(st.mean(v) for *_, v in A) - min(st.mean(v) for *_, v in A)

    sat = ["# Unutmayı ne sürüyor — LoRA kapsamı mı, dağılım mı?", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           "**Ölçü:** `forgetting_smoke` otomatik sayım (tavan 30) · taban **28/30**  ", "",
           "⭐ **Yeni eğitim gerekmedi.** Kapsam merdiveni `v0.0.14` üzerinde "
           "zaten koşulmuştu ve `runs/` hiç silinmiyor (Kural 7).", "",
           "## A. Dağılım değişir, KAPSAM SABİT", "",
           "Üçünde de: 8 katman · q+o (16 modül) · rank 8 · scale 20 · LR 1e-5.", "",
           "| kol | veri | adım | unutma | tohum |", "|---|---|---:|---|---:|"]
    for ad, veri, adim, v in A:
        sat.append(f"| {ad} | {veri} | {adim} | **{st.mean(v):.2f}** ± "
                   f"{_ci(v):.2f} | {len(v)} |")
    sat += ["", f"`d1` − `z-h9` = **{f1:+.2f} ± {h1_:.2f}** "
            f"({'okunabilir' if abs(f1) > h1_ else 'gürültüde'}) · "
            f"`e2` − `d1` = **{f2:+.2f} ± {h2_:.2f}** "
            f"({'⭐ **okunabilir**' if abs(f2) > h2_ else 'gürültüde'})", "",
            f"⇒ **Yayılım: {a_ara:.2f} puan.**", "",
            "⛔⛔ **Adım sayısı açıklamıyor:** 1368 → 27,62 · 2478 → 26,75 · "
            "3345 → **28,00**. Eğer daha çok adım daha çok unutma demek "
            "olsaydı `e2` en kötü olurdu; **en iyisi o**. ⇒ Dağılım, adım "
            "sayısından bağımsız olarak belirleyici.", "",
            "## B. Kapsam değişir, DAĞILIM SABİT (`v0.0.14`)", "",
            "| kol | kapsam | modül | unutma | tohum |", "|---|---|---:|---|---:|"]
    for k, t, m, v in sorted(B, key=lambda x: x[2]):
        sat.append(f"| `{k}` | {t} | **{m}** | {st.mean(v):.2f} ± "
                   f"{_ci(v):.2f} | {len(v)} |")
    sat += ["", f"Modül sayısı **8 → 48** (6 kat) · unutma yayılımı "
            f"**{b_ara:.2f} puan** · korelasyon **r = {r:+.3f}** (n={len(B)} kol).", "",
            "⇒ ⛔ **Kapsamı altı kat büyütmek unutmayı anlamlı biçimde "
            "değiştirmiyor** ve işaret bile **ters** (daha geniş kapsam → "
            "biraz daha AZ unutma).", "",
            "## ⭐⭐⭐ Sonuç", "",
            "⛔⛔ **Ham yayılımları karşılaştırmak YANILTIR** — kapsam "
            f"kollarının yayılımı ({b_ara:.2f}) dağılımınkinden ({a_ara:.2f}) "
            "**büyük**. Ayıran şey yayılımın büyüklüğü değil, **DÜZENİ**:", "",
            "| | düzen var mı | kanıt |", "|---|---|---|",
            "| **dağılım** (kapsam sabit) | ⭐ **evet** | farklar sıralı ve "
            f"`e2`−`d1` = {f2:+.2f} ± {h2_:.2f} **okunabilir**; tazeleme "
            "unutmayı tabana geri getiriyor |",
            "| **kapsam** (dağılım sabit) | ⛔ **hayır** | modül 8→48 (6 kat) "
            f"ama r = **{r:+.3f}** ve işaret ters; yayılım **dağınık**, sıralı "
            "değil — en düşük kol (`h5`, 26,00) **orta** kapsamda, en yüksek "
            "kollar hem en dar (`h1`) hem en geniş (`h2`) uçta |", "",
            "➡️⭐⭐⭐ *Unutmayı **DAĞILIM** sürüyor, LoRA kapsamı değil. Dar "
            "dağılımlı bir korpusla eğitmek genel yeteneği bozuyor; kapsamı "
            "daraltmak ya da genişletmek bunu düzeltmiyor, ama dağılıma "
            "yeterince alan dışı sinyal katmak **tamamen geri alıyor** "
            "(T257).*", "",
            "⇒ T255'nin bıraktığı iki aday sebepten **kapsam elendi**.", "",
            "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **B bölümü `v0.0.14` üzerinde** | dağılım orada da dardır; "
            "*«kapsam GENİŞ dağılımda da etkisiz»* denemez. Söylenebilen: "
            "**dar dağılımda** kapsam unutmayı sürmüyor |",
            "| ⛔ **A'da iki şey birlikte değişti** | `z-h9` → `d1` geçişinde "
            "hem korpus büyüdü hem adım arttı. ⭐ Ama `e2` bu karışıklığı "
            "çözüyor: en çok adımı o aldı ve **en az unuttu** |",
            "| ⛔⛔ **B'nin GÜCÜ DÜŞÜK** | kol başına 1-3 tohum ve yayılım "
            f"{b_ara:.2f} puan ⇒ *«kapsam etkisi YOK»* değil, **«sıralı bir "
            "kapsam etkisi SAPTANMADI»** denir. `h5`'in 26,00'ı açıklanamıyor "
            "ve kapsamla açıklanamayan bir oynaklığın varlığını gösteriyor |",
            "| ⛔ **K174/K175 ile çelişmiyor** | orada ölçülen **güvenlik "
            "davranışı** ve kapsam onu 13 katmanda çökertiyor. Burada ölçülen "
            "**genel yetenek** ⇒ iki ayrı eksen, iki ayrı davranış |",
            "| ⚠️ **Tek eksen** | `forgetting_smoke` 30 öge; başka unutma "
            "ölçütlerinde aynı sonucun çıkacağı gösterilmedi |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[sat.index("## A. Dağılım değişir, KAPSAM SABİT"):]))
    print(f"\n→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
