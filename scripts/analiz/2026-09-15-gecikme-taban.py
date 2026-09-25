#!/usr/bin/env python3
"""Gecikme tabanı — Faz 3 baseline'ın beşinci çıktısı (plan.md §Faz 3).

Neden ayrı ölçülüyor: kalite sayıları ince ayardan sonra karşılaştırılacak ve
LoRA adapteri gecikmeyi DEĞİŞTİRİR. Öncesi yazılmazsa "model yavaşladı mı"
sorusu sonradan cevaplanamaz.

⚠️ Bu sayılar bu makineye ve bu yığına özgüdür (MLX, bf16, yerel). Mutlak
değer taşınmaz; taşınan şey **öncesi/sonrası farkı**.

Kullanım: uv run python <betik>
"""
from __future__ import annotations

import json
import math
import statistics
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / "reports/analiz/2026-09-15-gecikme-taban.md"

def _kor(a: list[float], b: list[float]) -> float:
    ma, mb = statistics.mean(a), statistics.mean(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
    return num / den if den else 0.0


KOSULAR = [
    ("Eksen 1 · golden.locked", "golden-kosu/20260915-103548-locked-baseline-1"),
    ("Eksen 2 · safety_crisis", "eksen-kosu/20260915-105829-safety_crisis-baseline-1"),
    ("Eksen 3 · forgetting_smoke", "eksen-kosu/20260915-104526-forgetting_smoke-baseline-1"),
    ("Eksen 4 · context_fidelity", "eksen-kosu/20260915-110543-context_fidelity-baseline-2"),
    ("Eksen 5 · sycophancy", "eksen-kosu/20260915-105259-sycophancy-baseline-1"),
]


def main() -> None:
    L: list[str] = []
    P = L.append
    P("# Gecikme tabanı — ince ayar ÖNCESİ")
    P("")
    P("- tarih: 2026-09-15 · betik: `scripts/analiz/2026-09-15-gecikme-taban.py`")
    P("- model: temel `gemma-4-E4B-it-bf16` · **adapter yok** · `max_tokens=1024`")
    P("- ⚠️ Sayılar bu makineye ve bu yığına özgü. Taşınan şey mutlak değer değil, "
      "**öncesi/sonrası farkı**.")
    P("")
    P("| koşu | n | ortanca sn | ort sn | p90 sn | en yavaş | ortanca krk | krk/sn |")
    P("|---|---:|---:|---:|---:|---:|---:|---:|")
    hepsi: list = []
    hepsi_t: list = []
    for ad, yol in KOSULAR:
        d = KOK / "reports/analiz" / yol
        rs = [json.loads(l) for l in open(d / "sonuclar.jsonl")]
        s = sorted(r["sure_sn"] for r in rs)
        k = sorted(len(r["cevap"]) for r in rs)
        hepsi += [(r["sure_sn"], len(r["cevap"])) for r in rs]
        hepsi_t += [(r["sure_sn"], len(r["cevap"]), len(r.get("thinking") or ""))
                    for r in rs]
        p90 = s[min(len(s) - 1, int(0.9 * len(s)))]
        hiz = statistics.median(k) / statistics.median(s) if statistics.median(s) else 0
        P(f"| {ad} | {len(rs)} | {statistics.median(s):.1f} | {statistics.mean(s):.1f} | "
          f"{p90:.1f} | {max(s):.1f} | {statistics.median(k):.0f} | {hiz:.0f} |")
    s = sorted(x for x, _ in hepsi)
    k = sorted(y for _, y in hepsi)
    P(f"| **tümü** | **{len(hepsi)}** | **{statistics.median(s):.1f}** | "
      f"{statistics.mean(s):.1f} | {s[int(0.9*len(s))]:.1f} | {max(s):.1f} | "
      f"{statistics.median(k):.0f} | {statistics.median(k)/statistics.median(s):.0f} |")
    P("")
    P("## Okuma")
    P("")
    P("### Gecikmeyi ne belirliyor")
    P("")
    dus = [(x, y, z) for x, y, z in hepsi_t]
    kova = [("boş", 0, 0), ("1-500", 1, 500), ("501-1500", 501, 1500),
            ("1501-3000", 1501, 3000), (">3000", 3001, 10**9)]
    P("| `thinking` uzunluğu | n | ortanca sn |")
    P("|---|---:|---:|")
    for ad, lo, hi in kova:
        v = [x for x, _, z in dus if lo <= z <= hi]
        if v:
            P(f"| {ad} krk | {len(v)} | {statistics.median(v):.1f} |")
    P("")
    kt = _kor([z for _, _, z in dus], [x for x, _, _ in dus])
    kc = _kor([y for _, y, _ in dus], [x for x, _, _ in dus])
    bos = [x for x, _, z in dus if z == 0]
    dolu = [x for x, _, z in dus if z > 0]
    P(f"| değişken | süreyle korelasyon |")
    P(f"|---|---:|")
    P(f"| **`thinking` uzunluğu** | **{kt:.2f}** |")
    P(f"| cevap uzunluğu | {kc:.2f} |")
    P("")
    P(f"- ⭐ **Gecikme neredeyse tümüyle iç muhakeme bloğudur.** `thinking` boş olan "
      f"{len(bos)} kayıt ortanca **{statistics.median(bos):.1f} sn**; dolu olan "
      f"{len(dolu)} kayıt **{statistics.median(dolu):.1f} sn**. Cevabın kendisi "
      f"süreyi çok az belirliyor ({kc:.2f}).")
    P("- ⚠️ **Bu muhakeme istenmedi.** Koşuların hepsinde `thinking=false` — yani "
      "`<|think|>` öneki konmadı. Model muhakemeyi kendiliğinden üretiyor ve "
      f"{len([1 for _, _, z in dus if 1501 <= z <= 3000])}/{len(dus)} kayıtta uzunluğu "
      "1500-3000 karakter arasında, girdi ne olursa olsun.")
    P("- **Pratik sonuç:** gecikmeyi düşürmenin yolu daha hızlı yığın ya da daha kısa "
      "cevap değil, **muhakemenin uzunluğunu uyarlamak**. `plan.md` Faz 4 zaten "
      "*\"uyarlanabilir thinking\"* diyordu; bu ölçüm o karara sayı veriyor.")
    P(f"- **En yavaş kayıt {max(s):.1f} sn**, p90 {s[int(0.9*len(s))]:.1f} sn. Tek turlu "
      "bir sohbet arayüzü için yüksek; İP4'te akışlı yanıt gerekir. **Bu benim okumam "
      "(Kural 6)** — ölçüm gecikmeyi söylüyor, kabul edilebilir eşiği söylemiyor.")
    P("- ⚠️ Eksen 3'ün ortancası (5.2 sn) yarı yarıya düşük çünkü o sette **sistem "
      "promptu yok**, model çoğu öğede hiç muhakeme üretmiyor. Setler arası gecikme "
      "karşılaştırması bu yüzden anlamsız; karşılaştırılacak şey her setin KENDİ "
      "öncesi/sonrasıdır.")
    P("")
    CIKTI.write_text("\n".join(L) + "\n")
    print(f"yazıldı: {CIKTI.relative_to(KOK)}")
    print(f"toplam {len(hepsi)} kayıt · ortanca {statistics.median(s):.1f} sn")


if __name__ == "__main__":
    main()
