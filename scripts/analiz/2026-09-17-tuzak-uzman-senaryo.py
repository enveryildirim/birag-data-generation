#!/usr/bin/env python3
"""`tuzak_uzman` bayrağı bir VERİ kusurunu mu, yoksa SENARYONUN kendisini mi ölçüyor?

⛔⛔ **Neden bu ölçüm.** Judge 300 kayıtta 29 kez `tuzak_uzman` dedi ve sayı
partiler boyunca büyüdü (0→14). İlk açıklamam «Bir şeye katılmıyorum» kalıbıydı;
2×2 tablo bunu **çürüttü** (bayrakların %59'unda kalıp yok, kalıbın %76'sı
bayraksız). ⇒ İkinci hipotez: bayrak, **itirazın beklendiği senaryolarda**
yoğunlaşıyor olabilir.

➡️ *Eğer bir bayrak, tasarımın KASITLI olarak istediği davranışta yoğunlaşıyorsa,
o bayrak bir kusur ölçüsü değil, tasarımla rubriğin ÇATIŞMASININ ölçüsüdür — ve
bu ikisini ayırmadan yapılacak her revizyon tasarımı bozar.*

⚠️ Judge Claude ailesinden (K43/K45) ⇒ sayılar metrik değil, sinyal.
⚠️ Tek koşu, k=1, rubrik v9 (SHA `4b78260a96d78311`) — K97/K137 kapsamında.
"""
from __future__ import annotations
import json, re
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / "reports/analiz/2026-09-17-tuzak-uzman-senaryo.md"
KALIP = re.compile(r"Bir şeye katılmıyorum")
YOLLAR = {
 "v5-parti4": "data/judged/v5-parti4.v3.v9.jsonl",
 "v5-parti5": "data/judged/v5-parti5.arinmis.v9.jsonl",
 "v5-parti6": "data/judged/v5-parti6.arinmis.v9.jsonl",
 "v5-parti7": "data/judged/v5-parti7.arinmis.v9.jsonl",
 "v5-parti8": "data/judged/v5-parti8.arinmis.v9.jsonl",
}
# ⭐ Tasarımca İTİRAZ BEKLENEN senaryolar — `prompts/uretim-v5.md` §8c ve
# senaryo tanımlarından; liste burada YAZILI, koşuya göre değişmez.
ITIRAZ_BEKLENEN = {"nazikce_karsi_cikma", "inkar"}


def main() -> int:
    toplam, bayrak, kalip_var, kalip_bayrak = Counter(), Counter(), Counter(), Counter()
    ikili = Counter()
    for p, y in YOLLAR.items():
        for s in (KOK / y).read_text(encoding="utf-8").splitlines():
            if not s.strip():
                continue
            r = json.loads(s)
            j = r.get("judge") or {}
            if not j:
                continue
            sen = r["scenario"]
            son = [m for m in r["messages"] if m["role"] == "assistant" and m.get("content")][-1]
            k = bool(KALIP.search(son["content"]))
            t = j.get("tuzak_uzman") is True
            toplam[sen] += 1
            if t:
                bayrak[sen] += 1
            if k:
                kalip_var[sen] += 1
                if t:
                    kalip_bayrak[sen] += 1
            ikili[(k, t)] += 1

    sat = ["# `tuzak_uzman` — kusur ölçüsü mü, senaryo ölçüsü mü",
           "",
           "**Betik:** `scripts/analiz/2026-09-17-tuzak-uzman-senaryo.py` · **Tarih:** 2026-09-17",
           "**Kaynak:** v5-parti4..8 · rubrik `judge-eksen1.v9` · k=1 · 300 kayıt",
           "",
           "⚠️ Judge Claude ailesinden (K43/K45) ⇒ **metrik değil**, veri revizyonu sinyali.",
           "",
           "## 1. Kalıp hipotezi — ÇÜRÜDÜ", "",
           "| | `tuzak_uzman`=doğru | =yanlış |", "|---|---:|---:|",
           f"| «Bir şeye katılmıyorum» var | **{ikili[(True,True)]}** | {ikili[(True,False)]} |",
           f"| yok | **{ikili[(False,True)]}** | {ikili[(False,False)]} |", ""]
    kt, kf = ikili[(True, True)], ikili[(True, False)]
    nt, nf = ikili[(False, True)], ikili[(False, False)]
    p_k = kt / (kt + kf) if kt + kf else 0
    p_n = nt / (nt + nf) if nt + nf else 0
    sat += [f"P(bayrak | kalıp) = **{p_k:.2f}** · P(bayrak | kalıp yok) = **{p_n:.2f}** "
            f"⇒ oran **{(p_k/p_n if p_n else float('inf')):.1f}×**", "",
            f"⛔ Ama bayrakların **{nt}/{kt+nt}**'ünde kalıp YOK ve kalıbın "
            f"**{kf}/{kt+kf}**'i bayraksız. ➡️ *Kalıp ne gerekli ne yeterli; "
            f"eşlik ediyor, sürüklemiyor.*", "",
            "## 2. Senaryo hipotezi", "",
            "| senaryo | kayıt | bayrak | **oran** | itiraz bekleniyor mu |",
            "|---|---:|---:|---:|:--:|"]
    for sen, n in sorted(toplam.items(), key=lambda x: -(bayrak[x[0]] / x[1])):
        o = bayrak[sen] / n
        sat.append(f"| `{sen}` | {n} | {bayrak[sen]} | **{o:.2f}** | "
                   f"{'⭐ evet' if sen in ITIRAZ_BEKLENEN else '—'} |")

    bek_n = sum(n for s, n in toplam.items() if s in ITIRAZ_BEKLENEN)
    bek_b = sum(b for s, b in bayrak.items() if s in ITIRAZ_BEKLENEN)
    dig_n = sum(n for s, n in toplam.items() if s not in ITIRAZ_BEKLENEN)
    dig_b = sum(b for s, b in bayrak.items() if s not in ITIRAZ_BEKLENEN)
    sat += ["", "## 3. ⭐ Karar sayısı", "",
            "| dilim | kayıt | bayrak | oran |", "|---|---:|---:|---:|",
            f"| itiraz **beklenen** (`nazikce_karsi_cikma`, `inkar`) | {bek_n} | {bek_b} | "
            f"**{bek_b/bek_n:.2f}** |",
            f"| ötekiler | {dig_n} | {dig_b} | **{dig_b/dig_n:.2f}** |", "",
            f"➡️ Oran farkı **{(bek_b/bek_n)/(dig_b/dig_n) if dig_b else float('inf'):.1f}×**.", "",
            "## ⛔ Bu ölçümün söylemedikleri", "",
            "| | |", "|---|---|",
            "| ⛔ **Nedensellik yok** | senaryo ile bayrak arasındaki ilişki gözlemsel; "
            "hangi senaryonun hangi tohumla eşleştiği rastgele değil, örneklem planından geliyor |",
            "| ⛔ **Judge doğruluğu ölçülmedi** | bayrağın kendisi doğru mu, bunu ancak uzman söyler "
            "(K58 dilimi 50/70'te kapandı) |",
            "| ⚠️ k=1 | tek okuma; judge'ın kendi içi tutarlılığı ölçülmedi |",
            "| ⚠️ `ITIRAZ_BEKLENEN` listesi **benim okumam** | senaryo tanımlarından türetildi, "
            "rubrikte böyle bir sınıf yok |", ""]
    CIKTI.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[sat.index("## 2. Senaryo hipotezi"):]))
    print(f"→ {CIKTI.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
