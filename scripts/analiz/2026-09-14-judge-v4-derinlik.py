#!/usr/bin/env python3
"""Derin çok turlu kayıtlar tek turlulardan farklı puan alıyor mu? — KORPUS İÇİ.

Neden bu analiz: K79 tek partilik judge farklarının bulgu sayılamayacağını gösterdi
(n=40'ta %95 aralıklar ±15 puan ve parti 1'in iki bulgusu parti 2'de doğrulanmadı).
Korpuslar ARASI karşılaştırma zaten kontrollü değil — tohum, senaryo karışımı ve
yazım oturumu birlikte değişiyor.

Bu analiz farklı: **aynı korpusun içinde** derin çok turlu (3-5 kullanıcı turu) ile
tek turlu kayıtları karşılaştırıyor. Talimat, yazar, gün ve tohum havuzu aynı;
değişen tek şey kaydın derinliği. Yine de kontrollü bir deney değil — derin kayıtlar
ZENGİN tohumlara atandı (≥30 kelime), yani tohumlar da farklı.

Çıktı: reports/analiz/2026-09-14-judge-v4-derinlik.md
"""
from __future__ import annotations

import hashlib
import json
import statistics as st
import sys
from datetime import date
from pathlib import Path

from scipy.stats import fisher_exact, mannwhitneyu

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
sys.path.insert(0, str(KOK / "src"))
from filter import ANLASILIRLIK_BAYRAKLARI, anlasilirlik_hesapla  # noqa: E402

GIRDILER = [KOK / "data/judged/v3-parti1.jsonl", KOK / "data/judged/v3-parti2-tam.jsonl",
            KOK / "data/judged/v3-parti3.jsonl"]
CIKTI = KOK / "reports/analiz/2026-09-14-judge-v4-derinlik.md"
BAYRAK_ADI = {
    "kurulmamis_mecaz": "kullanıcının kurmadığı mecaz",
    "belirsiz_gonderge": "belirsiz gönderge",
    "ust_uste_yan_cumle": "üst üste binen yan cümle",
    "devrik_eksiltili": "devrik / eksiltili cümle",
    "soyut_adlastirma": "soyut adlaştırma",
}


def puan(j):
    v = j.get("anlasilirlik")
    return v if v is not None else anlasilirlik_hesapla(j)


def main() -> None:
    rows = []
    for g in GIRDILER:
        rows += [json.loads(l) for l in open(g) if l.strip()]
    rows = [r for r in rows if r.get("judge")]
    derin = [r for r in rows if sum(1 for m in r["messages"] if m["role"] == "user") >= 3]
    tek = [r for r in rows if sum(1 for m in r["messages"] if m["role"] == "user") == 1]
    iki = [r for r in rows if sum(1 for m in r["messages"] if m["role"] == "user") == 2]
    pd_, pt = [puan(r["judge"]) for r in derin], [puan(r["judge"]) for r in tek]
    pd_ = [x for x in pd_ if x is not None]
    pt = [x for x in pt if x is not None]
    u = mannwhitneyu(pd_, pt, alternative="two-sided") if pd_ and pt else None

    L = [f"# judge v4 — derin çok turlu ↔ tek turlu (korpus içi)", "",
         "**Girdi:** " + " · ".join(
             f"`{g.relative_to(KOK)}` (`{hashlib.sha256(g.read_bytes()).hexdigest()[:12]}…`)"
             for g in GIRDILER) + "  ",
         f"**Betik:** `{Path(__file__).resolve().relative_to(KOK)}` · "
         f"**Tarih:** {TARIH} · **Kayıt:** {len(rows)}", "", "---", "",
         "## Neden bu analiz", "",
         "K79 tek partilik judge farklarının bulgu sayılamayacağını gösterdi ve korpuslar "
         "**arası** karşılaştırma zaten kontrollü değil (tohum, senaryo karışımı ve yazım "
         "oturumu birlikte değişiyor). Bu analiz **aynı korpusun içinde** kalıyor: talimat, "
         "yazar, gün ve tohum havuzu aynı, değişen tek şey kaydın derinliği.", "",
         "> ⚠️ Yine de kontrollü değil: derin kayıtlar **zengin tohumlara** atandı "
         "(≥30 kelime), yani tohumlar da farklı. Fark derinliğe atfedilemez.", "",
         "## 1. `anlasilirlik`", "",
         "| Grup | n | ortalama | medyan | kusursuz (=5) |", "|---|---:|---:|---:|---:|"]
    for ad, grup in [("derin çok turlu (3-5 tur)", pd_), ("tek turlu", pt)]:
        if grup:
            L.append(f"| {ad} | {len(grup)} | {st.mean(grup):.2f} | {st.median(grup):.0f} | "
                     f"{sum(1 for v in grup if v == 5)} (%{sum(1 for v in grup if v==5)/len(grup)*100:.0f}) |")
    L.append(f"| iki turlu | {len(iki)} | "
             f"{st.mean([puan(r['judge']) for r in iki]):.2f} | "
             f"{st.median([puan(r['judge']) for r in iki]):.0f} | "
             f"{sum(1 for r in iki if puan(r['judge'])==5)} |")
    if u:
        L += ["", f"Mann-Whitney (derin ↔ tek turlu): **p = {u.pvalue:.4f}** — "
              + ("anlamlı fark." if u.pvalue < 0.05 else
                 "anlamlı fark yok; bu, grupların aynı olduğu anlamına gelmez, "
                 f"n = {len(pd_)} ve n = {len(pt)} ile ayırt edilemiyor demektir."), ""]
    L += ["## 2. Kusur bayrakları", "",
          "| Kusur | derin | tek turlu | Fisher p |", "|---|---:|---:|---:|"]
    for b in ANLASILIRLIK_BAYRAKLARI:
        a = sum(1 for r in derin if r["judge"].get(b) is True)
        c = sum(1 for r in tek if r["judge"].get(b) is True)
        p = fisher_exact([[a, len(derin) - a], [c, len(tek) - c]])[1]
        L.append(f"| {BAYRAK_ADI[b]} | {a}/{len(derin)} (%{a/len(derin)*100:.0f}) | "
                 f"{c}/{len(tek)} (%{c/len(tek)*100:.0f}) | {p:.3f} |")
    L += ["", "## 3. Güvenlik", "",
          "| Ölçüm | derin | tek turlu |", "|---|---:|---:|"]
    for ad, alan in [("klinik güvenlik ihlali", "klinik_guvenlik_ihlali"),
                     ("rol sınırı ihlali", "rol_siniri_ihlali"),
                     ("cevapsız soru", "cevapsiz_soru")]:
        L.append(f"| {ad} | {sum(1 for r in derin if r['judge'].get(alan))}/{len(derin)} | "
                 f"{sum(1 for r in tek if r['judge'].get(alan))}/{len(tek)} |")
    L += ["", "> Bu bayrakların ayrım gücü hiç ölçülmedi (K61); yokluk kanıt değildir.", ""]
    CIKTI.write_text("\n".join(L) + "\n")
    print(f"yazıldı: {CIKTI.relative_to(KOK)} (derin {len(derin)} · iki turlu {len(iki)} · tek {len(tek)})")


if __name__ == "__main__":
    main()
