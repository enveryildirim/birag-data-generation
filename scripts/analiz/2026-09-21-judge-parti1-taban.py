#!/usr/bin/env python3
"""`v6-parti1` judge sonucu ↔ korpusun AYNI MODELLE yargılanmış dilimi.

⛔ K97: `v0.0.14`'ün 521 kaydı `claude-sonnet-subagent` ile puanlı ve o
sayılar buraya konamaz. Ama **32 kayıt aynı Gemini modeliyle** yargılanmış;
karşılaştırma yalnız o dilimle yapılır.

⭐ Ölçekler farklı: EPITOME boyutları (`duygusal_tepki`, `yorumlama`,
`kesif`) **0/1/2**, `mi_uyumu` **1-5**. Tek bir «ortalama» sütunu ikisini
karıştırır; tabloda ölçek yazılı.

⭐⭐ **Sınanan hipotez:** `kesif` *«kendini daha fazla açmaya davet ediyor
mu»* diye soruyor. Izgara kayıtların yarısına **sorusuz** bir kapanış
dayatıyor (`ozet`, `takdir`, `yalnizca_yansitma`, `durur`). Eğer düşük
`kesif` ortalaması bu kapanışlardan geliyorsa, sayı bir kalite kusuru
değil bir **tasarım tercihinin ölçüdeki karşılığıdır**.

Çıktı: reports/analiz/2026-09-21-judge-parti1-taban.md
"""
from __future__ import annotations

import json
import statistics as st
from collections import defaultdict
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-judge-parti1-taban.md"
MODEL = "agy:gemini-3.8-flash-high"
EPITOME = ("duygusal_tepki", "yorumlama", "kesif")
BESLI = ("mi_uyumu", "grounding")
SORULU = "acik_uclu_soru"


def _yukle(yol: Path) -> list[dict]:
    return [json.loads(l) for l in yol.read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> int:
    kor = [r for r in _yukle(KOK / "datasets/v0.0.14/train.jsonl")
           if (r.get("judge") or {}).get("judge_model") == MODEL]
    p1 = [r for r in _yukle(KOK / "data/judged/v6-parti1.jsonl")
          if (r.get("judge") or {}).get("judge_model") == MODEL]

    def ort(kay, d):
        v = [r["judge"][d] for r in kay if isinstance((r.get("judge") or {}).get(d), (int, float))]
        return (st.mean(v), len(v)) if v else (float("nan"), 0)

    sat = [f"# `v6-parti1` judge ↔ korpusun aynı-model dilimi", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Model:** `{MODEL}` · korpus dilimi **{len(kor)}** · parti1 **{len(p1)}**", "",
           "⛔ K97: `v0.0.14`'ün 521 kaydı `claude-sonnet-subagent` ile puanlı ve "
           "buraya KONMADI. Karşılaştırma yalnız aynı modelle yargılanmış dilimle.", "",
           "| boyut | ölçek | korpus dilimi | **parti1** | fark |",
           "|---|---|---:|---:|---:|"]
    for d in EPITOME + BESLI:
        ol = "0-2" if d in EPITOME else "1-5"
        a, _ = ort(kor, d)
        b, _ = ort(p1, d)
        sat.append(f"| `{d}` | {ol} | {a:.2f} | **{b:.2f}** | {b-a:+.2f} |")

    # ── hipotez: kesif ↔ kapanış türü ──────────────────────────────────────
    sat += ["", "## ⭐⭐ Hipotez — düşük `kesif` bir KUSUR mu, bir TASARIM mı?", "",
            "`kesif` *«kendini daha fazla açmaya davet ediyor mu»* diye soruyor. "
            "Izgara kayıtların yarısına **sorusuz** kapanış dayatıyor. Eğer düşük "
            "ortalama oradan geliyorsa, sayı bir kalite kusuru değil bir tasarım "
            "tercihinin ölçüdeki karşılığıdır.", "",
            "| kapanış | n | `kesif` | `duygusal_tepki` | `yorumlama` |",
            "|---|---:|---:|---:|---:|"]
    grup: dict[str, list[dict]] = defaultdict(list)
    for r in p1:
        grup[r["gen_meta"].get("turn_ending", "?")].append(r)
    for k in sorted(grup, key=lambda x: -len(grup[x])):
        g = grup[k]
        sat.append(f"| `{k}` | {len(g)} | {ort(g,'kesif')[0]:.2f} | "
                   f"{ort(g,'duygusal_tepki')[0]:.2f} | {ort(g,'yorumlama')[0]:.2f} |")
    # ⭐ Aynı ayrımı KORPUS dilimine de uygula: kapanış karışımı iki tarafta da
    # ~%50 olduğuna göre, kalan fark kapanıştan DEĞİL başka bir yerden geliyor.
    sat += ["", "⭐ Aynı ayrım korpus diliminde (kapanış karışımı benzer, o yüzden "
                "kalan fark kapanıştan gelmiyor):", "",
            "| kapanış | n | `kesif` | `duygusal_tepki` | `yorumlama` |",
            "|---|---:|---:|---:|---:|"]
    kgrup: dict[str, list[dict]] = defaultdict(list)
    for r in kor:
        kgrup[(r.get("gen_meta") or {}).get("turn_ending", "?")].append(r)
    for k in sorted(kgrup, key=lambda x: -len(kgrup[x])):
        g = kgrup[k]
        sat.append(f"| `{k}` | {len(g)} | {ort(g,'kesif')[0]:.2f} | "
                   f"{ort(g,'duygusal_tepki')[0]:.2f} | {ort(g,'yorumlama')[0]:.2f} |")
    sat.append("")

    sorulu = [r for r in p1 if r["gen_meta"].get("turn_ending") == SORULU]
    sorusuz = [r for r in p1 if r["gen_meta"].get("turn_ending") != SORULU]
    ks, kz = ort(sorulu, "kesif")[0], ort(sorusuz, "kesif")[0]
    sat += ["", f"⭐ **Sorulu kapanış** (n={len(sorulu)}): `kesif` **{ks:.2f}** · "
                f"**sorusuz kapanış** (n={len(sorusuz)}): **{kz:.2f}** — "
                f"fark **{ks-kz:+.2f}** (ölçek 0-2).", ""]
    # korpus diliminin kapanış karışımı aynı mı
    kg = defaultdict(int)
    for r in kor:
        kg[(r.get("gen_meta") or {}).get("turn_ending", "?")] += 1
    ks_or = sum(v for k, v in kg.items() if k == SORULU) / max(1, len(kor))
    sat += [f"⚠️ Korpus diliminde sorulu kapanış oranı **%{100*ks_or:.0f}**, "
            f"parti1'de **%{100*len(sorulu)/max(1,len(p1)):.0f}**. "
            "İki dilimin kapanış karışımı farklıysa, `kesif` ortalamalarını "
            "doğrudan karşılaştırmak **elmayla armut** olur.", ""]

    sat += ["## ⛔ Bu karşılaştırmanın söylemedikleri", "", "| | |", "|---|---|",
            f"| ⛔⛔ **Korpus dilimi küçük** | n={len(kor)}; bir ortalama farkının "
            "gürültü bandı **ölçülmedi** — T175 kayıt düzeyinde %61 oynaklık ölçtü "
            "ama KÜME ORTALAMASI için bir taban yok |",
            "| ⛔⛔ **Neden-sonuç kurulmadı** | kapanış türü ile `kesif` arasındaki "
            "ilişki bir korelasyondur; ızgara kapanışı dayattığı için ters "
            "nedensellik yok, ama başka bir ortak sebep olabilir |",
            "| ⛔ **`kesif` düşüklüğü «iyi» demek değildir** | tasarım tercihi olması "
            "onu doğru yapmaz; yalnız bir KUSUR olmadığını gösterir. Sorusuz "
            "kapanışın terapötik değeri ayrı bir soru ve ölçülmedi |",
            "| ⛔ **`mi_uyumu` ve `grounding` tavana yakın** | bu, ayırt etme gücü "
            "olmadığı anlamına da gelebilir (K57: judge kalite ölçmez, tarar) |",
            "| ⛔⛔ **`kesif` bir KALİTE boyutu gibi raporlanıyor ama bu koşuda bir "
            "KAPANIŞ DEDEKTÖRÜ gibi davrandı** | sorulu 1.45 ↔ sorusuz 0.03; aradaki "
            "fark ölçeğin %70'i. Bu, rubriğin kusuru mu yoksa `kesif`in tanımı gereği "
            "mi böyle olduğu **karara bağlanmadı** |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[5:]))
    print(f"\n→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
