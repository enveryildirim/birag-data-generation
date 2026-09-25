#!/usr/bin/env python3
"""qwen ↔ gemini uyumu, **v6 rubriğinde** — metriği kullanmadan önce metriği sınamak.

⛔⛔ **Neden.** Eksen 1'i koşmanın tek kotasız yolu `qwen3.8:27b-mlx` (T161). Ama
K45'in ölçtüğü *«iki bağımsız aile birbirinden yalnız %1,4 farklı»* sonucu **v1/v4
rubriğiyleydi**; aradan v5, v6, v7, v8, v9 geçti. ➡️ *Bir judge'ı değiştirmek
ÖLÇÜT değiştirmektir; yeni judge'ın eskisiyle uyumu ölçülmeden sayıları aynı
tabloda okunamaz (K97/K137).*

⭐ **Sıfır kotayla ölçülebilir** (K96'nın işaret ettiği yol): `baseline-v6`
koşusunun 48 cevabı gemini ile **zaten yargılanmış**. Aynı cevaplar qwen'e
verildi (`--yeniden-judge`) ⇒ üretim tekrarlanmadı, cevaplar bit bit aynı.

⚠️ **Ölçülen şey uyum, DOĞRULUK değil.** İki judge aynı yere düşerse ikisi de
aynı yönde yanılıyor olabilir. Uyum, qwen'i *«doğru»* yapmaz; yalnız gemini'nin
yerine geçip geçemeyeceğini söyler.

⛔ Metrik tanımı KOPYALANMIYOR: `2026-09-15-judge-claude-sapmasi.py`'den içe
aktarılıyor (K97) ⇒ çıkan sayı K45'in 0,825/0,814 çapalarıyla aynı hesaptan.

Girdi : reports/analiz/golden-kosu/*-baseline-v6 (gemini) · *-qwen-v6-uyum (qwen)
Çıktı : reports/analiz/2026-09-18-judge-uyum-v6.md
Kullanım: uv run python scripts/analiz/2026-09-18-judge-uyum-v6.py
"""
from __future__ import annotations

import importlib.util as iu
import json
import statistics as st
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
G = KOK / "reports/analiz/golden-kosu"
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-judge-uyum-v6.md"

_s = iu.spec_from_file_location("sap", KOK / "scripts/analiz/2026-09-15-judge-claude-sapmasi.py")
S = iu.module_from_spec(_s); _s.loader.exec_module(S)     # ⭐ metrik tanımı ORADAN


def _son(ek: str) -> Path | None:
    d = sorted([p for p in G.iterdir() if p.name.endswith(ek)])
    return d[-1] if d else None


def main() -> int:
    dg, dq = _son("-baseline-v6"), _son("-qwen-v6-uyum")
    if not (dg and dq):
        print(f"⛔ Koşu yok: gemini={dg} qwen={dq}"); return 2
    gj, qj = S.yukle(dg), S.yukle(dq)
    ortak = sorted(set(gj) & set(qj))
    if not ortak:
        print("⛔ Ortak kayıt yok."); return 2
    dims = S.mevcut_dims([gj[i] for i in ortak] + [qj[i] for i in ortak])
    eksik = [d for d in S.DIMS if d not in dims]

    sg = [S.k45_skoru(gj[i], dims) for i in ortak]
    sq = [S.k45_skoru(qj[i], dims) for i in ortak]
    cift = [(a, b) for a, b in zip(sg, sq) if a is not None and b is not None]
    mg, mq = st.mean([a for a, _ in cift]), st.mean([b for _, b in cift])

    sat = ["# qwen ↔ gemini uyumu — **v6 rubriğinde**", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**gemini:** `{dg.name}` · **qwen:** `{dq.name}` · ortak kayıt **{len(ortak)}**", "",
           "⛔⛔ **Neden bu ölçüm.** Eksen 1'i koşmanın tek kotasız yolu qwen (T161). Ama",
           "K45'in *«iki bağımsız aile %1,4 farklı»* sonucu **v1/v4 rubriğiyleydi**. ➡️ *Bir",
           "judge'ı değiştirmek ÖLÇÜT değiştirmektir.*", "",
           "⭐ **Sıfır kota:** aynı 48 cevap, üretim tekrarlanmadan iki judge'a verildi.", "",
           "## 1. ⭐ K45 bileşik puanı (aynı hesap, aynı çapalar)", "",
           "| judge | bileşik | K45 çapası |", "|---|---:|---|",
           f"| gemini (v6) | **{mg:.3f}** | 0,814 (v1/v4) |",
           f"| qwen (v6) | **{mq:.3f}** | 0,825 (v1/v4) |",
           f"| **fark** | **{mq-mg:+.3f}** | K45'te +0,011 |", "",
           (f"⚠️ **Boyut eksik:** {eksik} — v6 rubriği bunları üretmiyor; bileşik "
            f"{len(dims)} boyutla hesaplandı ⇒ K45 çapalarıyla **tam** karşılaştırılamaz."
            if eksik else "⭐ K45'in yedi boyutunun hepsi mevcut."), "",
           "## 2. Boyut boyut", "",
           "| boyut | gemini ort. | qwen ort. | fark |", "|---|---:|---:|---:|"]
    for d in dims:
        a = [gj[i][d] for i in ortak if gj[i].get(d) is not None]
        b = [qj[i][d] for i in ortak if qj[i].get(d) is not None]
        if a and b:
            sat.append(f"| `{d}` | {st.mean(a):.2f} | {st.mean(b):.2f} | "
                       f"**{st.mean(b)-st.mean(a):+.2f}** |")
    sat += ["", "## 3. İkili bayraklar — Cohen kappa", "",
            "⚠️ Ham uyum çarpık taban oranlarında yanıltır; kappa şansı düşer.", "",
            "| bayrak | gemini | qwen | ham uyum | kappa |", "|---|---:|---:|---:|---:|"]
    kappalar = []
    for f in S.IKILI:
        a = [bool(gj[i].get(f)) for i in ortak]
        b = [bool(qj[i].get(f)) for i in ortak]
        if sum(a) + sum(b) < S.SEYREK_ESIK:
            continue
        k = S.kappa(a, b)
        if k is not None:
            kappalar.append(k)
        ham = sum(1 for x, y in zip(a, b) if x == y) / len(a)
        sat.append(f"| `{f}` | {sum(a)} | {sum(b)} | %{100*ham:.0f} | "
                   f"{'—' if k is None else f'{k:+.2f}'} |")
    if kappalar:
        sat += ["", f"⭐ Ortanca kappa: **{st.median(kappalar):+.2f}** "
                f"({len(kappalar)} bayrak, seyrek olanlar hariç)."]

    sat += ["", "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Uyum ≠ doğruluk** | iki judge aynı yere düşerse ikisi de aynı yönde "
            "yanılıyor olabilir; uyum qwen'i *«doğru»* yapmaz, yalnız gemini'nin yerine "
            "geçip geçemeyeceğini söyler |",
            "| ⛔⛔ **Tek kol üzerinde ölçüldü** | uyum yalnız TABAN cevaplarında; metrik ise "
            "kolları SIRALAMAK için kullanılacak. *İki judge'ın aynı cevaba aynı puanı "
            "vermesi, iki KOLU aynı sırada dizecekleri anlamına gelmez* |",
            "| ⛔ **v9 uyumu hâlâ ölçülmedi** | bu ölçüm v6'da; güncel rubrik v9 ve K137 "
            "gereği sürümler karşılaştırılamaz ⇒ v9 için ayrı bir uyum ölçümü gerekir |",
            "| ⚠️ **48 öğe küçük** | kappa'lar geniş güven aralığı taşır |", ""]

    (KOK / f"reports/analiz/{TARIH}-judge-uyum-v6.json").write_text(
        json.dumps({"tarih": TARIH, "gemini": dg.name, "qwen": dq.name, "ortak": len(ortak),
                    "dims": dims, "eksik": eksik, "bilesik_gemini": mg, "bilesik_qwen": mq},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[8:]))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
