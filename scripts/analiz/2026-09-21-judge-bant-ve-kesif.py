#!/usr/bin/env python3
"""İki soru, sıfır servis çağrısı — ikisi de parti1 judge koşusundan çıktı.

## Soru 1 — `kesif` rubriğin mi, bu judge'ın mı?
parti1'de `kesif` sorulu kapanışta **1.45**, sorusuzda **0.03** çıktı: bir
kalite boyutundan çok bir **kapanış dedektörü**. ⛔ Bu, judge'ın bir tuhaflığı
mı yoksa rubriğin tanımı gereği mi? Korpusun **Claude ile** yargılanmış 521
kaydında aynı ayrım koşuluyor.
⛔ K97 ihlali DEĞİL: iki modelin PUAN DÜZEYLERİ aynı tabloya konmuyor.
Sorulan şey her modelin **kendi içindeki** kapanış etkisi — yapısal bir soru.

## Soru 2 — ortalama farkının örnekleme bandı
parti1 ile korpusun Gemini dilimi arasında üç EPITOME boyutunda 0.15-0.20
fark var ve rapor *«bant yok»* diyor. ⛔ Judge'ın yeniden çekiliş oynaklığı
(T175) için hâlâ bant yok ve o servis ister. Ama **örnekleme** bileşeni
elde var: gruplar içi dağılımdan önyükleme ile hesaplanır.
➡️ *Toplam belirsizlik EN AZ bu kadardır; bu bant bir alt sınırdır.*

Çıktı: reports/analiz/2026-09-21-judge-bant-ve-kesif.md
"""
from __future__ import annotations

import json
import random
import statistics as st
from collections import defaultdict
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-judge-bant-ve-kesif.md"
GEMINI, CLAUDE = "agy:gemini-3.8-flash-high", "claude-sonnet-subagent"
EPITOME = ("duygusal_tepki", "yorumlama", "kesif")
SORULU = "acik_uclu_soru"
B = 10000
TOHUM = 20260921


def _yukle(yol: Path) -> list[dict]:
    return [json.loads(l) for l in yol.read_text(encoding="utf-8").splitlines() if l.strip()]


def _puan(kay, d):
    return [r["judge"][d] for r in kay
            if isinstance((r.get("judge") or {}).get(d), (int, float))]


def onyukleme(a: list[float], b: list[float]) -> tuple[float, float, float]:
    """(fark, %2.5, %97.5) — grup içi dağılımdan, yerine koyarak."""
    rng = random.Random(TOHUM)
    fark = st.mean(b) - st.mean(a)
    d = []
    for _ in range(B):
        ea = [a[rng.randrange(len(a))] for _ in a]
        eb = [b[rng.randrange(len(b))] for _ in b]
        d.append(st.mean(eb) - st.mean(ea))
    d.sort()
    return fark, d[int(0.025 * B)], d[int(0.975 * B)]


def main() -> int:
    kor = _yukle(KOK / "datasets/v0.0.14/train.jsonl")
    p1 = _yukle(KOK / "data/judged/v6-parti1.jsonl")
    kor_g = [r for r in kor if (r.get("judge") or {}).get("judge_model") == GEMINI]
    kor_c = [r for r in kor if (r.get("judge") or {}).get("judge_model") == CLAUDE]

    sat = [f"# Judge — `kesif`in yapısı ve ortalama farkının örnekleme bandı", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Servis çağrısı:** 0 (yalnız kayıtlı puanlar okundu)", "",
           "## 1. ⭐⭐ `kesif` bir kapanış dedektörü mü — iki judge'da ayrı ayrı", "",
           "⛔ **K97 ihlali değil:** iki modelin puan DÜZEYLERİ aynı tabloya "
           "konmuyor. Sorulan şey her modelin **kendi içindeki** kapanış etkisi.", "",
           "| judge | n | sorulu kapanış | sorusuz kapanış | fark |",
           "|---|---:|---:|---:|---:|"]
    yapi = {}
    for ad, kay in (("Gemini (korpus dilimi)", kor_g), ("Gemini (parti1)", p1),
                    ("Claude (korpus)", kor_c)):
        so = [r for r in kay if (r.get("gen_meta") or {}).get("turn_ending") == SORULU]
        sz = [r for r in kay if (r.get("gen_meta") or {}).get("turn_ending") not in (SORULU, None)]
        a, b = _puan(so, "kesif"), _puan(sz, "kesif")
        if not a or not b:
            continue
        yapi[ad] = (st.mean(a), st.mean(b))
        sat.append(f"| {ad} | {len(a)}+{len(b)} | **{st.mean(a):.2f}** | "
                   f"**{st.mean(b):.2f}** | {st.mean(a)-st.mean(b):+.2f} |")
    sat += ["", "⭐⭐ Etki **her iki judge'da da** var ve ölçeğin (0-2) büyük "
                "kısmını kaplıyor ⇒ bu bir model tuhaflığı değil, **rubriğin "
                "`kesif` tanımının sonucu**: *«kendini daha fazla açmaya davet "
                "ediyor mu»* sorusu, sorusuz biten bir turda tanımı gereği "
                "hayırdır.", "",
           "➡️⭐⭐⭐ *Izgara kayıtların yarısına sorusuz kapanış dayatıyor; o yarı "
           "için `kesif` bir ÖLÇÜM değil, bir SABİT. Küme ortalamasını "
           "raporlamak, tasarım tercihini kalite puanı gibi göstermek olur.*", "",
           "## 2. ⭐ Ortalama farkının örnekleme bandı (önyükleme, B=10.000)", "",
           "⛔ Bu bant yalnız **örnekleme** belirsizliğini kapsar. Judge'ın "
           "yeniden çekiliş oynaklığı (T175: kayıt düzeyinde %61) **ayrıca** "
           "vardır ve servis gerektirdiği için ölçülmedi. "
           "➡️ *Toplam belirsizlik en az bu kadardır; bu bir ALT SINIRDIR.*", "",
           "| boyut | korpus dilimi | parti1 | fark | %95 bant | bandın dışında mı |",
           "|---|---:|---:|---:|---|---|"]
    for d in EPITOME:
        a, b = _puan(kor_g, d), _puan(p1, d)
        f, lo, hi = onyukleme(a, b)
        disar = "⭐ evet" if (lo > 0 or hi < 0) else "⛔ **hayır**"
        sat.append(f"| `{d}` | {st.mean(a):.2f} | {st.mean(b):.2f} | {f:+.2f} | "
                   f"[{lo:+.2f}, {hi:+.2f}] | {disar} |")

    # kapanış kovası içinde duygusal_tepki — karışımdan arınmış
    sat += ["", "⭐ `duygusal_tepki` kapanış karışımından arındırılmış hâliyle "
                "(yalnız sorulu kapanışlar, iki tarafta da en kalabalık kova):", "",
            "| | n | ortalama |", "|---|---:|---:|"]
    for ad, kay in (("korpus dilimi", kor_g), ("parti1", p1)):
        so = [r for r in kay if (r.get("gen_meta") or {}).get("turn_ending") == SORULU]
        v = _puan(so, "duygusal_tepki")
        sat.append(f"| {ad} | {len(v)} | {st.mean(v):.2f} |")
    a = _puan([r for r in kor_g if (r.get("gen_meta") or {}).get("turn_ending") == SORULU],
              "duygusal_tepki")
    b = _puan([r for r in p1 if (r.get("gen_meta") or {}).get("turn_ending") == SORULU],
              "duygusal_tepki")
    f, lo, hi = onyukleme(a, b)
    sat += ["", f"fark **{f:+.2f}**, %95 bant **[{lo:+.2f}, {hi:+.2f}]** ⇒ "
               + ("⭐ bandın dışında" if (lo > 0 or hi < 0) else
                  "⛔ **bandın içinde — bu farkı gösteremem**"), ""]

    sat += ["## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Judge oynaklığı KAPSANMADI** | T175 kayıt düzeyinde %61 "
            "oynaklık ölçtü; küme ortalaması için yeniden çekiliş gerekir ve kota "
            "kapalı. Gerçek bant buradan GENİŞ |",
            "| ⛔⛔ **Önyükleme bir kanıt üretmez, belirsizliği ölçer** | bandın "
            "dışında olmak farkın gerçek olduğunu değil, ÖRNEKLEMEYLE "
            "açıklanamadığını söyler |",
            "| ⛔ **Korpus dilimi n=32** | küçük bir grup geniş bant üretir; "
            "bandın genişliği bir bulgu değil, örneklem büyüklüğünün sonucu |",
            "| ⛔ **`kesif` bulgusu rubriği KUSURLU ilan etmez** | tanım gereği "
            "böyle davranıyor olabilir; karar `gd`-kalemi değil, **rubrik sahibinin** "
            "işi ve verilmedi |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[4:]))
    print(f"\n→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
