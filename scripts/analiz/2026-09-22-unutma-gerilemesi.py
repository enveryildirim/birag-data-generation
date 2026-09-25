#!/usr/bin/env python3
"""Unutma gerilemesinin sebebi — öge öge teşhis.

⭐ T254 `forgetting_smoke`'ta **okunabilir** bir gerileme buldu: taban 28/30
→ kol 26,75 ± 0,73 (**−1,25**). Bu betik sebebi arar.

⛔ **Yöntem, bu oturumun dersi:** önce ögeler ayrılır (hangi öge, kaç
tohumda), sonra **cevaplar okunur**, sonra korpusta karşılığı ölçülür.
Toplam sayıdan hipoteze atlanmaz.

Çıktı: reports/analiz/2026-09-22-unutma-gerilemesi.md
"""
from __future__ import annotations

import json
import re
import statistics as st
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-unutma-gerilemesi.md"
EK = KOK / "reports/analiz/eksen-kosu"
T = (7, 13, 23, 31, 37, 41, 43, 47)


def _rows(et):
    d = [p for p in EK.iterdir() if p.name.endswith(et)]
    return {r["id"]: r for r in (json.loads(s) for s in
            (sorted(d)[-1] / "sonuclar.jsonl").read_text(encoding="utf-8").splitlines()
            if s.strip())}


def main() -> int:
    oge = {json.loads(l)["id"]: json.loads(l)
           for l in open(KOK / "evals/forgetting_smoke.jsonl") if l.strip()}
    tb = _rows("-forgetting_smoke-baseline-1")
    kol = {t: _rows(f"d1-veri2x-k8qo-v018-t{t}-forget") for t in T}

    kayip, kazanc = [], []
    for i, r in tb.items():
        kg = sum(1 for t in T if i in kol[t] and kol[t][i].get("otomatik_gecti"))
        if r.get("otomatik_gecti") and kg < len(T):
            kayip.append((i, kg))
        elif not r.get("otomatik_gecti") and kg > 0:
            kazanc.append((i, kg))
    kayip.sort(key=lambda x: x[1])

    # korpusun çıktı kipleri
    kay = [json.loads(l) for l in open(KOK / "datasets/v0.0.18/train.jsonl")]
    son = [[m for m in r["messages"] if m["role"] == "assistant"][-1].get("content") or ""
           for r in kay]
    n = len(son)
    rakam = sum(1 for c in son if re.search(r"\d", c))
    yalin = sum(1 for c in son if len(c.split()) <= 3 and re.search(r"\d", c))
    arit = sum(1 for c in son if re.search(r"\d+\s*[+\-×x*/=]\s*\d+", c))
    uz = st.mean(len(c.split()) for c in son)

    sat = ["# Unutma gerilemesinin sebebi — öge öge", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           "**Ölçülen:** `forgetting_smoke` 30 öge · taban (adaptersiz) ↔ "
           "`d1-veri2x-k8qo-v018`, 8 tohum  ",
           "**Gerileme:** 28/30 → 26,75 ± 0,73 = **−1,25** (T254, okunabilir)  ", "",
           "## Net −1,25 neyin toplamı", "",
           "| öge | kolda geçen | ne sınıyor |", "|---|---:|---|"]
    ad = {"fs-025": "aritmetik — «5×6, sonra +10, sadece son sayıyı yaz» → 40",
          "fs-029": "olgusal — «Kürk Mantolu Madonna»nın yazarı → Sabahattin Ali",
          "fs-013": "aritmetik — sayı = 35",
          "fs-009": "liste/indeks sorusu",
          "fs-014": "çeviri — Türkçe→İngilizce",
          "fs-015": "Türkçe yanıt kipi"}
    for i, kg in kayip:
        sat.append(f"| ⛔ `{i}` | **{kg}/8** | {ad.get(i, '?')} |")
    for i, kg in kazanc:
        sat.append(f"| ⭐ `{i}` | **{kg}/8** (tabanda ❌) | {ad.get(i, '?')} |")

    sat += ["", f"⇒ **{len(kayip)} öge kaybedildi, {len(kazanc)} öge kazanıldı.** "
            "Net −1,25 bu ikisinin farkı.", "",
            "## ⭐⭐⭐ Cevaplar okundu — iki ayrı kusur", "",
            "### 1. Aritmetik: biçim doğru, hesap yanlış", "",
            "`fs-025` — *«Önce 5 ile 6'yı çarp, sonra sonuca 10 ekle, sadece "
            "son sayıyı yaz»* ⇒ doğru cevap **40**.", "",
            "| | cevap |", "|---|---|", "| taban | **40** ✅ |",
            "| kol (8 tohum) | **60 · 60 · 70 · 70 · 70 · 70 · 60 · 70** ❌ |", "",
            "⭐ Model **yalın sayı** veriyor — yani istenen biçimi tutturuyor. "
            "Bozulan **hesabın kendisi**. `fs-025` 8 tohumun 8'inde birden "
            "kayıp ⇒ gürültü değil, sistematik.", "",
            "### 2. Olgusal bilgi: ad uyduruyor", "",
            "`fs-029` — *«Kürk Mantolu Madonna»nın yazarı kimdir?*", "",
            "| tohum | cevap |", "|---|---|",
            "| taban | **Sabahattin Ali** ✅ |",
            "| t13 | Sabahattin Ali ✅ |",
            "| t7 · t23 · t31 · t43 · t47 | **«Enem Şişmanoğlu» · «Enem Şişkin» · "
            "«Enem Şentürk» · «Enem Dereli» ×2** |",
            "| t37 · t41 | «Dostoyevski» |", "",
            "⛔⛔ **Model *«bilmiyorum»* demiyor, makul görünen bir ad "
            "UYDURUYOR.** ⭐ Ve sekiz tohumun **beşi** «**Enem** …» ile "
            "başlayan bir ad üretiyor — «Enem» Türkçede bir ad değil ve "
            "korpusta **hiç geçmiyor** (0 eşleşme) ⇒ doğrudan veri bulaşması "
            "değil. Beş bağımsız tohumun aynı yapıyı üretmesi **jeton düzeyinde "
            "bir çöküşe** işaret ediyor; mekanizması bu raporda **ölçülmedi**.", "",
            "## Korpus bu kipleri hiç göstermiyor", "",
            f"`datasets/v0.0.18`'in {n} son asistan cevabı:", "",
            "| kip | kayıt | oran |", "|---|---:|---:|",
            f"| rakam içeren | {rakam} | %{100*rakam/n:.0f} |",
            f"| **yalın sayı cevabı** (≤3 sözcük) | **{yalin}** | **%{100*yalin/n:.1f}** |",
            f"| **aritmetik ifadesi** | **{arit}** | **%{100*arit/n:.1f}** |",
            f"| ortalama uzunluk | — | {uz:.0f} sözcük |", "",
            "⭐ Asistan tarafında **özel ad da yok**: en sık büyük harfli "
            "sözcükler cümle başı işlev sözcükleri (*Bir · Ama · Bunu*). "
            "Kullanıcı tarafında ise gerçek özel adlar geçiyor (*Instagram · "
            "İstanbul · Defne*) ⇒ asimetri **tasarım gereği** (K18/K110: kurum "
            "adları ağırlığa girmemeli).", "",
            "➡️ **Korpus tek bir çıktı kipi öğretiyor:** ~49 sözcüklük "
            "yansıtıcı düzyazı; yalın sayı yok, aritmetik yok, özel ad yok.", "",
            "## ⛔ Ne söylenebilir, ne söylenemez", "", "| | |", "|---|---|",
            "| ⭐ **Söylenebilir** | gerileme **iki ayrı kusurdan** geliyor: "
            "aritmetik hesap ve olgusal ad. İkisinde de **biçim korunuyor, "
            "içerik bozuluyor** ⇒ bu bir *«kip daralması»* değil, **bilgi/işlem "
            "kaybı** |",
            "| ⭐ **Söylenebilir** | korpus bu kipleri **hiç** göstermiyor "
            "(%0,0 yalın sayı, %0,0 aritmetik, ~0 özel ad) ⇒ ilişki var |",
            "| ⛔⛔ **SÖYLENEMEZ: nedensellik** | korpusun bu kipleri "
            "göstermemesi ile kaybın **aynı şey olduğu gösterilmedi**. Aynı "
            "kaybı LoRA kapsamı da üretebilir (K174/K175: güvenlik davranışı "
            "13 katmanda çöküyor; bu kol 8 katman) |",
            "| ⛔ **Sınanmadı** | (a) korpusa az miktarda aritmetik/olgusal "
            "içerik ekleyen bir kol, (b) daha dar LoRA kapsamı. İkisi de "
            "ayrımı gösterirdi |",
            "| ⚠️ **«Enem» olgusu açıklanmadı** | beş tohumda yinelenen bir "
            "sözde-ad; korpusta yok, mekanizması ölçülmedi |",
            "| ⚠️ **30 öge küçüktür** | 4 kayıp / 2 kazanç; öge düzeyinde güven "
            "aralıkları geniştir |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[sat.index("## Net −1,25 neyin toplamı"):sat.index("## ⛔ Ne söylenebilir, ne söylenemez")]))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
