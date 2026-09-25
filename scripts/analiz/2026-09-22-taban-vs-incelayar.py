#!/usr/bin/env python3
"""Taban ↔ ince ayarlı model — JUDGE GEREKTİRMEYEN metrikler.

⛔ **Neden judge yok.** Gemini kotası kapalı ve Claude üreticiyle aynı aile
(K45: +6/+11 öz-şişirme). ⇒ Rubrik boyutları bu raporda **yok**. Buradaki
her sayı ya deterministik bir iddia denetiminden ya da metnin kendisinden
geliyor.

⭐ **Ve bu bir kayıp değil, kısmen bir kazanç:** deterministik sayımların
tohum oynaklığı dereceli puandan çok daha düşük ölçüldü
(`forget` sd **0,52** ↔ dereceli sd **3,0**) ⇒ 3 tohumla okunabilir.

⛔⛔ **T248'in şartı uygulanır:** her eksen puanının yanında **boş cevap**,
**ortalama uzunluk** ve **kesilme** verilir. Bunlar olmadan davranış sanılan
şeyin ne kadarının ağzını açmamaktan geldiği bilinemez.

⛔ **Taban tek koşudur** (adaptersiz, üretim deterministik ⇒ tohum kavramı
yok). İnce ayarlı kol 3 ya da 8 tohum; hata payı yalnız onun için verilir.

Çıktı: reports/analiz/2026-09-22-taban-vs-incelayar.md
"""
from __future__ import annotations

import collections
import json
import math
import re
import statistics as st
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-taban-vs-incelayar.md"
EK = KOK / "reports/analiz/eksen-kosu"
GK = KOK / "reports/analiz/golden-kosu"

# (eksen, taban etiketi, ince ayar etiket deseni, tohumlar, tavan)
EKSEN = [
    ("safety_crisis", "-safety_crisis-baseline-1",
     "d1-veri2x-k8qo-v018-t{t}-safety", (7, 13, 23, 31, 37, 41, 43, 47), 20),
    ("forgetting_smoke", "-forgetting_smoke-baseline-1",
     "d1-veri2x-k8qo-v018-t{t}-forget", (7, 13, 23, 31, 37, 41, 43, 47), 30),
    ("context_fidelity", "-context_fidelity-baseline-1",
     "d1-v018-t{t}-context_fidelity", (7, 13, 23), 20),
    ("sycophancy", "-sycophancy", "d1-v018-t{t}-sycophancy", (7, 13, 23), 24),
    ("context_fidelity.real", "-cf-gercek", "d1-v018-t{t}-cfreal", (7, 13, 23), 15),
]


def _son(desen: str, kok: Path = EK):
    d = [p for p in kok.iterdir() if p.name.endswith(desen)]
    if not d:
        return None
    return [json.loads(s) for s in
            (sorted(d)[-1] / "sonuclar.jsonl").read_text(encoding="utf-8").splitlines()
            if s.strip()]


def _profil(rs):
    """T248'in üç zorunlu yan sütunu + geçen sayısı."""
    gec = sum(1 for r in rs if r.get("otomatik_gecti"))
    metin = [(r.get("cevap") or "") for r in rs]
    bos = sum(1 for c in metin if not c.strip())
    dolu = [c for c in metin if c.strip()]
    kes = sum(1 for c in dolu if c.strip()[-1] not in ".!?…\"'»)")
    uz = st.mean(len(c.split()) for c in dolu) if dolu else 0
    return gec, bos, kes, uz


def _cesitlilik(metinler):
    """distinct-1/2 ve tekrar oranı — judge gerektirmez."""
    tk = [re.findall(r"\w+", m.lower()) for m in metinler if m.strip()]
    t1 = [w for s in tk for w in s]
    t2 = [tuple(s[i:i+2]) for s in tk for i in range(len(s) - 1)]
    d1 = len(set(t1)) / len(t1) if t1 else 0
    d2 = len(set(t2)) / len(t2) if t2 else 0
    # aynı cümlenin birden çok cevapta geçmesi
    cum = [c.strip() for m in metinler for c in re.split(r"(?<=[.!?])\s+", m)
           if len(c.split()) >= 5]
    yin = 1 - len(set(cum)) / len(cum) if cum else 0
    return d1, d2, yin


def main() -> int:
    sat = ["# Taban ↔ ince ayarlı model — judge gerektirmeyen metrikler", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           "**İnce ayarlı kol:** `d1-veri2x-k8qo-v018` (`datasets/v0.0.18`, "
           "1033 kayıt) · **taban:** adaptersiz  ", "",
           "⛔ **Rubrik boyutları YOK:** judge kotası kapalı ve Claude "
           "üreticiyle aynı aile (K45) ⇒ buradaki her sayı deterministik bir "
           "iddia denetiminden ya da metnin kendisinden geliyor.", "",
           "⛔⛔ **T248 şartı:** her puanın yanında boş cevap, uzunluk ve "
           "kesilme verilir.", "",
           "## Eksenler", "",
           "| eksen | taban | ince ayar (ort ± 2·SE) | Δ | okunabilir mi | tohum |",
           "|---|---|---|---:|---|---:|"]
    detay = []
    for ad, tb_d, ia_d, tohumlar, tavan in EKSEN:
        tb = _son(tb_d)
        if tb is None:
            sat.append(f"| `{ad}` | ⛔ taban koşusu yok | — | — | — | — |")
            continue
        tg, tb_bos, tb_kes, tb_uz = _profil(tb)
        v, prof = [], []
        for t in tohumlar:
            rs = _son(ia_d.format(t=t))
            if rs is None:
                continue
            g, b, k, u = _profil(rs)
            v.append(g)
            prof.append((b, k, u))
        if not v:
            sat.append(f"| `{ad}` | {tg}/{tavan} | ⛔ kol koşusu yok | — | — | — |")
            continue
        ort = st.mean(v)
        hata = 2 * st.stdev(v) / math.sqrt(len(v)) if len(v) > 1 else float("nan")
        d = ort - tg
        ok = ("⚠️ tek tohum" if len(v) < 2 else
              "⭐ **evet**" if abs(d) > hata else "⛔ hayır — gürültüde")
        sat.append(f"| `{ad}` | {tg}/{tavan} | {ort:.2f} ± {hata:.2f} | "
                   f"**{d:+.2f}** | {ok} | {len(v)} |")
        detay.append((ad, tavan, (tb_bos, tb_kes, tb_uz),
                      (st.mean(p[0] for p in prof), st.mean(p[1] for p in prof),
                       st.mean(p[2] for p in prof))))

    sat += ["", "## ⛔⛔ T248 yan sütunları — puan bunlar olmadan okunmaz", "",
            "| eksen | boş cevap (taban → kol) | kesilme | ort. uzunluk (sözcük) |",
            "|---|---|---|---|"]
    for ad, tavan, tb, ia in detay:
        sat.append(f"| `{ad}` | {tb[0]:.0f} → **{ia[0]:.1f}** | "
                   f"{tb[1]:.0f} → {ia[1]:.1f} | {tb[2]:.0f} → **{ia[2]:.0f}** |")

    # ── çeşitlilik: golden.dev üretimleri ───────────────────────────
    tb_g = _son("-taban-v9", GK)
    sat += ["", "## Çeşitlilik ve uzunluk — `golden.dev` (48 öge)", ""]
    if tb_g is None:
        sat += ["⛔ taban golden koşusu bulunamadı."]
    else:
        satirlar = [("taban", [(r.get("cevap") or "") for r in tb_g])]
        for t in (7, 13, 23):
            rs = _son(f"-d1-v018-t{t}-golden", GK)
            if rs:
                satirlar.append((f"d1 · t{t}", [(r.get("cevap") or "") for r in rs]))
        sat += ["⭐ *«Bu benim önerim»* — çeşitlilik metrikleri diyalog üretimi "
                "literatüründe standarttır ve burada **ölçülmüş** bir olguyu "
                "hedefliyor: K193 korpusun ikinci büyük kalıbını 43 kayıtta "
                "(%7,5) bulmuştu.", "",
                "| model | distinct-1 | distinct-2 | yinelenen cümle | ort. uzunluk |",
                "|---|---:|---:|---:|---:|"]
        for ad, ms in satirlar:
            d1, d2, yin = _cesitlilik(ms)
            uz = st.mean(len(m.split()) for m in ms if m.strip()) if ms else 0
            sat.append(f"| {ad} | {d1:.3f} | {d2:.3f} | %{100*yin:.1f} | {uz:.0f} |")
        sat += ["", "⚠️ distinct-n **uzunluğa duyarlıdır**: kısa cevaplarda "
                "kendiliğinden yükselir. ⇒ Uzunluk sütunu olmadan okunamaz — "
                "bu, T248'in çeşitlilik metriğindeki karşılığıdır."]

    sat += ["", "## ⛔ Bu raporun söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Rubrik boyutları yok** | judge erişimi açılmadan "
            "`mi_uyumu`, EPITOME üçlüsü, `anlasilirlik` ölçülemez ⇒ bu rapor "
            "*«kalite arttı/azaldı»* demez |",
            "| ⛔⛔ **`safety_crisis` bu kolun etkisini ölçemez** | T247: "
            "korpusta `is_crisis` kaydı 0; eksen geçerli ama bu karşılaştırma "
            "için **yersiz** |",
            "| ⛔ **Taban tek koşu** | adaptersiz üretim deterministik ⇒ tohum "
            "yayılımı yok; hata payı yalnız ince ayar kolu için |",
            "| ⛔ **`otomatik_gecti` kapı sayımıdır, kalite değil** | K57; "
            "judge tipindeki iddialar bu koşucuda *«denetlenemedi»* kalır ve "
            "**geçti sayılmaz** |",
            "| ⚠️ **Çeşitlilik metrikleri yeni** | bu projede ilk kez "
            "hesaplanıyor, gürültü tabanı ölçülmedi |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[sat.index("## Eksenler"):]))
    print(f"\n→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
