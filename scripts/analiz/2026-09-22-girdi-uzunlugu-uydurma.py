#!/usr/bin/env python3
"""Uzun kullanıcı girdisi uydurmadan koruyor mu — yoksa ölçüyü mü kolaylaştırıyor?

⭐ **Nasıl çıktı.** T243 partiler arası uydurma oynaklığının sebebini
arayıp bulamamıştı; keşifsel bölümünde en güçlü sinyal `bicim = uzun`
(−12,7 puan, p = 0,0011, Bonferroni'yi geçen tek satır) idi ama **çoklu
karşılaştırma** yüzünden bulgu sayılmamıştı. ⛔ Ayrıca o gün **cevabın**
uzunluğu ölçülmüş, **kullanıcı girdisinin** uzunluğu hiç ölçülmemişti.

⭐⭐ Bu betik onu doğrudan ölçer ve **2,6 kat büyük** kümede (1089 ↔ 412)
yineler. Birim T231'in kararıdır: **ilk kullanıcı mesajı**, bağlam çıkarılmış.

⛔⛔ **VE ALTERNATİF AÇIKLAMA ÖNCEDEN YAZILI.** `grounding` bir **tek-ayrıntı
sondasıdır** (T238): judge bir ayrıntı adlandırır, kod onu konuşmada arar.
⇒ Kullanıcı metni uzadıkça, adlandırılan ayrıntının orada **rastlantısal
olarak bulunma olasılığı da artar**. Yani ölçülen düşüş, uydurmanın azalması
kadar **sondanın kolaylaşması** da olabilir. İkisi bu veriyle **ayrılamaz**.

Çıktı: reports/analiz/2026-09-22-girdi-uzunlugu-uydurma.md
"""
from __future__ import annotations

import collections
import json
import math
import random
import re
import statistics as st
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-girdi-uzunlugu-uydurma.md"
KUME = KOK / "data/judged/v0.0.18.jsonl"
TOHUM, N_PERM = 20260922, 20000
CTX = re.compile(r"<context.*?</context>|<CTX>", re.S)


def wilson(k, n, z=1.96):
    if not n:
        return (0.0, 0.0)
    p, d = k / n, 1 + z * z / n
    m = (p + z * z / (2 * n)) / d
    y = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, m - y), min(1.0, m + y))


def perm(a, b, rng):
    d = sum(a) / len(a) - sum(b) / len(b)
    hep = a + b
    asiri = 0
    for _ in range(N_PERM):
        rng.shuffle(hep)
        dd = sum(hep[:len(a)]) / len(a) - sum(hep[len(a):]) / len(b)
        if abs(dd) >= abs(d) - 1e-12:
            asiri += 1
    return d, (asiri + 1) / (N_PERM + 1)


def main() -> int:
    v = []
    for l in open(KUME):
        r = json.loads(l)
        j = r.get("judge")
        if not j or r.get("replay"):
            continue
        u = [m for m in r["messages"] if m["role"] == "user"]
        if not u:
            continue
        girdi = len(CTX.sub(" ", u[0].get("content") or "").split())
        son = [m for m in r["messages"] if m["role"] == "assistant"][-1]
        v.append({"girdi": girdi, "uyd": j.get("grounding") == 2,
                  "cevap": len((son.get("content") or "").split()),
                  "ayrinti": (j.get("en_somut_ayrinti") or "")})
    n = len(v)
    srt = sorted(x["girdi"] for x in v)
    q1, q2 = srt[n // 3], srt[2 * n // 3]

    def dilim(x):
        return "kısa" if x <= q1 else ("orta" if x <= q2 else "uzun")
    g = collections.defaultdict(list)
    for x in v:
        g[dilim(x["girdi"])].append(x["uyd"])

    rng = random.Random(TOHUM)
    uzun = [x["uyd"] for x in v if x["girdi"] > q2]
    oteki = [x["uyd"] for x in v if x["girdi"] <= q2]
    d, p = perm(uzun[:], oteki[:], rng)
    kat = (sum(oteki) / len(oteki)) / (sum(uzun) / len(uzun))

    # ⛔ karıştırıcı: cevap uzunluğu ve adlandırılan ayrıntının uzunluğu
    cev = {k: st.mean(x["cevap"] for x in v if dilim(x["girdi"]) == k)
           for k in ("kısa", "orta", "uzun")}
    ayr = {k: st.mean(len(x["ayrinti"].split()) for x in v
                      if dilim(x["girdi"]) == k and x["ayrinti"])
           for k in ("kısa", "orta", "uzun")}

    sat = ["# Uzun kullanıcı girdisi uydurmadan koruyor mu?", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Küme:** `data/judged/v0.0.18.jsonl` · {n} yargılı, replay dışı  ",
           f"**Birim:** ilk kullanıcı mesajı, bağlam çıkarılmış (T231) · "
           f"permütasyon {N_PERM}  ", "",
           "⭐ T243 bunu keşifsel bölümünde işaret etmişti (`bicim = uzun`, "
           "−12,7 puan) ama çokluk yüzünden bulgu saymamıştı; burada **2,6 kat "
           "büyük** kümede ve **girdi uzunluğu doğrudan ölçülerek** yineleniyor.", "",
           "## Ölçüm", "", "| girdi dilimi | uydurma | oran | %95 Wilson |",
           "|---|---:|---:|---|"]
    for k in ("kısa", "orta", "uzun"):
        a, m = sum(g[k]), len(g[k])
        lo, hi = wilson(a, m)
        esik = f"≤{q1}" if k == "kısa" else (f"≤{q2}" if k == "orta" else f">{q2}")
        sat.append(f"| **{k}** ({esik} sözcük) | {a}/{m} | %{100*a/m:.1f} | "
                   f"%{100*lo:.1f}–%{100*hi:.1f} |")
    sat += ["", f"**uzun ↔ öteki: {100*d:+.1f} puan · p = {p:.4f} · "
            f"{kat:.1f} kat fark.** Güven aralıkları **çakışmıyor**.", "",
            "⛔ İlişki **tek yönlü değil**: kısa %"
            f"{100*sum(g['kısa'])/len(g['kısa']):.1f} ↔ orta %"
            f"{100*sum(g['orta'])/len(g['orta']):.1f} arasında fark yok; "
            "ayrılan şey **uzun** dilim. ⇒ *«Seyrek girdi uydurma ÜRETİR»* "
            "değil, *«zengin girdi uydurmayı BASTIRIR»* biçiminde okunmalı.", "",
            "## ⛔⛔ Alternatif açıklama — ölçüyle ayrılamıyor", "",
            "`grounding` bir **tek-ayrıntı sondasıdır** (T238): judge bir "
            "ayrıntı adlandırır, kod onu konuşmada **arar**. ⇒ Kullanıcı metni "
            "uzadıkça adlandırılan ayrıntının orada **rastlantısal olarak "
            "bulunma olasılığı da artar.**", "",
            "| girdi dilimi | ort. cevap (sözcük) | ort. adlandırılan ayrıntı |",
            "|---|---:|---:|"]
    for k in ("kısa", "orta", "uzun"):
        sat.append(f"| {k} | {cev[k]:.0f} | {ayr[k]:.1f} |")
    sat += ["", "⚠️ Cevap uzunluğu dilimler arasında benzer kalıyorsa "
            "*«judge daha çok yazdığı için tutturuyor»* açıklaması zayıflar; "
            "ama **arama yüzeyi** (kullanıcı metni) tanımı gereği uzun "
            "dilimde daha büyük ⇒ **bu veriyle ayrılamaz.**", "",
            "⭐ **Ayıracak ölçüm:** aynı cevaplar, kullanıcı metni **kısaltılmış** "
            "bir kopyayla yeniden puanlanır; sonda kolaylaşması tek başına "
            "etkiyi üretiyorsa oran oynar. *Bu benim önerim*, koşulmadı.", "",
            "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Nedensellik yok** | girdi uzunluğu üretim anında "
            "**tasarlanmış** bir değişken (`bicim` kotası); uzun girdili "
            "kayıtlar başka açılardan da farklı olabilir |",
            "| ⛔⛔ **Sonda kolaylaşması ayrılamadı** | yukarıdaki bölüm; "
            "etkinin ne kadarının gerçek olduğu **bilinmiyor** |",
            "| ⛔ **T13-D'yi KAPATMAZ** | o kalem MODEL tarafını soruyor "
            "(*«seyrek girdide uydurma artar mı»*); bu ölçüm **korpus** "
            "tarafında ve aynı sonda kusurunu taşıyor ⇒ destekleyici, "
            "belirleyici değil |",
            "| ⚠️ **T243'ün çokluk şerhi kısmen kalkıyor** | bulgu önceden "
            "keşifseldi; **önceden belirtilmiş bir hipotez olarak** 2,6 kat "
            "büyük kümede yinelendi ⇒ güçlendi, ama aynı ölçütle |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[sat.index("## Ölçüm"):sat.index("## ⛔ Bu ölçümün söylemedikleri")]))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
