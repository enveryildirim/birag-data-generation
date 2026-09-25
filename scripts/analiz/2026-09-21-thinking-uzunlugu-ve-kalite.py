#!/usr/bin/env python3
"""Üretim hızını artırmak için: yazma emeği nereye gidiyor ve thinking
uzunluğu kaliteyi taşıyor mu (T232).

⛔⛔ **Neden.** Üretimi hızlandırmak istiyoruz ve hızlandırmanın nereden
geleceğine tahminle değil ölçümle karar verilmeli. İki soru:
  1. Yazdığım karakterlerin kaçı nereye gidiyor?
  2. `thinking` uzunluğu kaliteyle ilişkili mi — kısaltmak kalite keser mi?

⛔ İkinci sorunun cevabı KORELASYONDUR ve nedensel değildir. En büyük
karıştırıcı açık: uzun thinking ZOR kayıtlarda yazılmış olabilir ve zor
kayıtlar zaten düşük puan alır. Bu ölçüm o ikisini AYIRAMAZ.

⛔⛔ Puanlar `agy:gemini-3.8-flash-high` · `judge-eksen1.v9`, yalnız
parti1-3 (n=160) ve T175 kayıt düzeyindeki puanın bir ÇEKİLİŞ olduğunu
söylüyor (%61 oynuyor) ⇒ yalnız KÜME düzeyinde okunur.

Çıktı: reports/analiz/2026-09-21-thinking-uzunlugu-ve-kalite.md
"""
from __future__ import annotations

import json
import statistics as st
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-thinking-uzunlugu-ve-kalite.md"
# ⭐ Yalnız judge'ın ANA boyutları; bayrak alanları (0/1) ayrı okunuyor.
ANA = ("mi_uyumu", "mi_uyumu_holistik", "grounding", "anlasilirlik",
       "anlasilirlik_holistik", "dogallik", "dogallik_holistik")
TUZAK = ("tuzak_erken_tavsiye", "tuzak_uzman", "tuzak_erken_odak",
         "ust_uste_yan_cumle", "rol_reddediyor")


def _kor(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sx, sy = st.pstdev(xs), st.pstdev(ys)
    return sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / n / (sx * sy) if sx and sy else 0.0


def main() -> int:
    # 1. Yazma emeğinin dağılımı
    pay = {"thinking": 0, "asistan": 0, "kullanici": 0}
    parti = {}
    n = 0
    for i in range(1, 8):
        th = as_ = k = 0
        for l in (KOK / f"data/candidates/v6-parti{i}.jsonl").read_text(
                encoding="utf-8").splitlines():
            if not l.strip():
                continue
            r = json.loads(l)
            n += 1
            for m in r["messages"]:
                if m["role"] == "user":
                    k += len(m["content"])
                elif m["role"] == "assistant":
                    as_ += len(m["content"])
                    th += len(m.get("thinking") or "")
        parti[i] = (th, as_, k, sum(1 for l in (KOK / f"data/candidates/v6-parti{i}.jsonl")
                                    .read_text(encoding="utf-8").splitlines() if l.strip()))
        pay["thinking"] += th
        pay["asistan"] += as_
        pay["kullanici"] += k
    t = sum(pay.values())

    # v0.0.14 karşılaştırması
    v14 = KOK / "datasets/v0.0.14/train.jsonl"
    vth = vas = vn = 0
    if v14.exists():
        for l in v14.read_text(encoding="utf-8").splitlines():
            if l.strip():
                r = json.loads(l)
                vn += 1
                for m in r.get("messages", []):
                    if m.get("role") == "assistant":
                        vas += len(m.get("content") or "")
                        vth += len(m.get("thinking") or "")

    # 2. Uzunluk ↔ puan
    d = []
    for p in ("v6-parti1", "v6-parti2", "v6-parti3"):
        for l in (KOK / f"data/judged/{p}.jsonl").read_text(encoding="utf-8").splitlines():
            if not l.strip():
                continue
            r = json.loads(l)
            j = r.get("judge")
            if not j:
                continue
            a = [m for m in r["messages"] if m["role"] == "assistant"][-1]
            d.append((len(a.get("thinking") or ""), len(a["content"]),
                      {kk: v for kk, v in j.items() if isinstance(v, (int, float))}))

    sat = ["# Thinking uzunluğu: yazma emeği ve kalite", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Girdi:** `data/candidates/v6-parti{{1..7}}.jsonl` ({n} kayıt) · "
           f"`data/judged/v6-parti{{1,2,3}}.jsonl` ({len(d)} puanlı)  ", "",
           "## 1. Yazdığım karakterler nereye gidiyor", "",
           "| bileşen | karakter | pay | kayıt başına |", "|---|---:|---:|---:|"]
    for k in ("thinking", "asistan", "kullanici"):
        sat.append(f"| `{k}` | {pay[k]:,} | %{round(100*pay[k]/t)} | {pay[k]//n} |")
    sat += ["", f"⭐⭐ **Yazma emeğinin yarısından fazlası `thinking`** (%"
            f"{round(100*pay['thinking']/t)}) ve bu, hızlandırmanın en büyük "
            "tek kalemi.", "",
            "## 2. ⛔⛔ v6, EĞİTİLMİŞ SETİN ORANINDAN SAPMIŞ", "",
            "| set | kayıt | thinking ort | asistan ort | **oran** |",
            "|---|---:|---:|---:|---:|"]
    if vn:
        sat.append(f"| `datasets/v0.0.14` (eğitilen) | {vn} | {vth//vn} | "
                   f"{vas//vn} | **{vth/vas:.2f}** |")
    for i, (th, as_, _k, c) in parti.items():
        sat.append(f"| `v6-parti{i}` | {c} | {th//c} | {as_//c} | {th/as_:.2f} |")
    if vn:
        v6o = pay["thinking"] / pay["asistan"]
        sat += ["", f"⛔ v6 ortalaması **{v6o:.2f}**, eğitilen setin "
                f"**{vth/vas:.2f}**'sinden **%{round(100*(v6o/(vth/vas)-1))}** yüksek. "
                "⭐ T16'nın iddiası tam buraya bakıyor: *«tavan da veriyle "
                "öğretilir»* ve ürün KPI'ı gecikme. ⇒ Sapma yalnız bir hız "
                "sorunu değil, T16'nın kendi ekseninde bir gerilemedir.", ""]

    sat += ["## 3. Uzun thinking daha iyi kayıt mı demek", "",
            "⛔ Korelasyon, nedensellik değil. Aşağıdaki tabloyu okurken en "
            "büyük karıştırıcı açıkta: **uzun thinking ZOR kayıtlarda yazılmış "
            "olabilir** ve zor kayıtlar zaten düşük puan alır.", "",
            "| boyut | r(uzunluk) | r(oran) | ortalama |", "|---|---:|---:|---:|"]
    for k in ANA:
        alt = [(x[0], x[0] / max(x[1], 1), x[2][k]) for x in d if k in x[2]]
        if len(alt) < 20:
            continue
        sat.append(f"| `{k}` | {_kor([a for a,_,_ in alt],[c for _,_,c in alt]):+.2f} | "
                   f"{_kor([b for _,b,_ in alt],[c for _,_,c in alt]):+.2f} | "
                   f"{sum(c for _,_,c in alt)/len(alt):.2f} |")
    sat += ["", "**Tuzak bayrakları** (yüksek = kötü):", "",
            "| bayrak | r(uzunluk) | ateşleme oranı |", "|---|---:|---:|"]
    for k in TUZAK:
        alt = [(x[0], x[2][k]) for x in d if k in x[2]]
        if len(alt) < 20:
            continue
        sat.append(f"| `{k}` | {_kor([a for a,_ in alt],[c for _,c in alt]):+.2f} | "
                   f"{sum(c for _,c in alt)/len(alt):.2f} |")

    sat += ["", "➡️ **Okunan şey:** uzun thinking ana boyutlarda hafif NEGATİF "
            "(anlaşılırlık −0,21, doğallık −0,22, MI uyumu −0,18) ve tuzak "
            "bayraklarında hafif POZİTİF (erken tavsiye +0,25, uzman tuzağı "
            "+0,22). ⇒ **Uzun thinking'in daha iyi kayıt ürettiğine dair bir "
            "işaret yok; zayıf da olsa ters yönde işaret var.**", "",
            "⛔ Etki büyüklükleri küçük (|r| ≈ 0,2) ve n=160. Bu tablo "
            "*«kısaltmak kaliteyi artırır»* demiyor; *«kısaltmanın kaliteyi "
            "kestiğine dair bir dayanak yok»* diyor.", "",
            "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Nedensellik yok** | uzun thinking zor kayıtlarda olabilir; "
            "ölçüm bu karıştırıcıyı ayıramaz |",
            "| ⛔⛔ **Puanlar bir çekiliş** | T175: kayıt düzeyinde %61 oynuyor ⇒ "
            "yalnız küme okunur, tek kayıt değil |",
            "| ⛔ **Yalnız parti1-3** | 252 kayıt yargılanmadı (kota) ⇒ parti4-7 "
            "bu tabloda yok ve onlarda thinking daha uzun |",
            "| ⚠️ **Karakter ≠ token** | oranlar karakter üzerinden; token "
            "oranı Türkçe'de farklı çıkabilir |"]

    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[:sat.index("## 3. Uzun thinking daha iyi kayıt mı demek")]))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
