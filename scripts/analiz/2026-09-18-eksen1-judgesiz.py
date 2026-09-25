#!/usr/bin/env python3
"""Eksen 1'in JUDGE GEREKTİRMEYEN yarısı — ve neden öteki yarısı koşulamadı.

⛔⛔ **Eksen 1 bu projede bir metrik olarak hiç koşulmadı ve sebebi ölçüldü.**
Golden koşularının hepsi diskte duruyor ama **ince ayar kollarının hiçbiri
yargılanmamış** (`judge_model: None`, 48/48). Yargılanmış olan yalnız TABANLAR,
o da **v4/v5/v6** rubrikleriyle; güncel rubrik **v9** ve K137 gereği sürümler
arası karşılaştırma geçersiz.

⛔ **Puanlayan judge üç yoldan da kapalı ya da pahalı:**
  · **Gemini** (`agy:gemini-3.8-flash-high`) — yapılandırılmış judge, **kotası
    tükendi** (K96)
  · **Claude** — K43/K45 gereği puanlayan olamaz; ölçülmüş öz-şişirme
    (bağımsız aile 0,825 ↔ Claude 0,878/0,924, sapma ÖZNEL boyutlarda)
  · **`qwen3.8:27b-mlx`** — kotasız ve çalışıyor; bu betikle **ölçüldü:
    164 sn/kayıt** (v9 rubriği, yerel)

⭐ Ama üretim ucuz ve yapıldı: `gd-v010-k8` (48 öğe, 6,7 dk). Cevaplar sabit
olduğu için judge sonradan koşulabilir (`--yeniden-judge`) ⇒ bu rapor **judge
gerektirmeyen** sinyalleri karşılaştırır ve öteki yarının maliyetini yazar.

⚠️ *«Otomatik iddialar geçti»* **kalite demek değildir**: bunlar biçim kapıları
(soru sayısı, uydurma yok, uzunluk). Terapötik kalite EPITOME/MI boyutlarında
ölçülür ve onlar judge ister.

Girdi : reports/analiz/golden-kosu/*/sonuclar.jsonl
Çıktı : reports/analiz/2026-09-18-eksen1-judgesiz.md
Kullanım: uv run python scripts/analiz/2026-09-18-eksen1-judgesiz.py
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
G = KOK / "reports/analiz/golden-kosu"
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-eksen1-judgesiz.md"

KOLLAR = [("*ham model* (taban)", "-baseline-v6"),
          ("8 katman · v0.0.5 (eski tarama)", "gd2-A-dar"),
          ("⭐ 8 katman · **v0.0.10**", "gd-v010-k8")]
QWEN_SN = 164          # ⭐ bu oturumda ÖLÇÜLDÜ (v9 rubriği, yerel qwen)


def _oku(ad: str):
    d = sorted([p for p in G.iterdir() if p.name.endswith(ad)])
    if not d:
        return None, []
    return d[-1], [json.loads(s) for s in
                   (d[-1] / "sonuclar.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]


def main() -> int:
    veri = {}
    for ad, et in KOLLAR:
        d, rs = _oku(et)
        if not d:
            continue
        oto = collections.Counter()
        otot = collections.Counter()
        for r in rs:
            for i in (r.get("denetim") or []):
                if i.get("tip") != "otomatik":
                    continue
                otot[i["ad"]] += 1
                oto[i["ad"]] += bool(i.get("gecti"))
        veri[ad] = {
            "dizin": d.name, "n": len(rs),
            "bos": sum(1 for r in rs if not (r.get("cevap") or "").strip()),
            "kesildi": sum(1 for r in rs if r.get("kesildi")),
            "dejenere": sum(1 for r in rs if (r.get("dejenerasyon") or {}).get("dejenere")),
            "token": sum(r.get("uretim_token") or 0 for r in rs) / max(1, len(rs)),
            "oto": dict(oto), "otot": dict(otot),
            "yargili": sum(1 for r in rs if (r.get("judge") or {}).get("judge_model")),
        }

    kurallar = sorted({k for v in veri.values() for k in v["otot"]})
    sat = ["# Eksen 1'in judge gerektirmeyen yarısı", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           "**Set:** `evals/golden.dev.jsonl` (48 öğe) — mühürlü, değiştirilmedi", "",
           "⛔⛔ **Eksen 1 bu projede bir METRİK olarak hiç koşulmadı.** Golden koşuları",
           "diskte duruyor ama **ince ayar kollarının hiçbiri yargılanmamış**; yargılanmış",
           "olan yalnız tabanlar, o da **v4/v5/v6** rubrikleriyle. Güncel rubrik **v9** ve",
           "K137 gereği sürümler arası karşılaştırma geçersiz.", "",
           "## 1. Üretim ve judge durumu", "",
           "| kol | öğe | ⛔ yargılanmış | boş | kesilen | dejenere | ort. token |",
           "|---|---:|---:|---:|---:|---:|---:|"]
    for ad, _ in KOLLAR:
        v = veri.get(ad)
        if not v:
            sat.append(f"| {ad} | ⛔ koşu yok | | | | | |")
            continue
        sat.append(f"| {ad} | {v['n']} | **{v['yargili']}**/{v['n']} | {v['bos']} | "
                   f"{v['kesildi']} | {v['dejenere']} | {v['token']:.0f} |")
    sat += ["", "## 2. ⭐ Otomatik iddialar (judge'sız)", "",
            "| kural | " + " | ".join(ad for ad, _ in KOLLAR if ad in veri) + " |",
            "|---|" + "---:|" * len(veri)]
    for k in kurallar:
        h = [f"{veri[ad]['oto'].get(k,0)}/{veri[ad]['otot'].get(k,0)}"
             for ad, _ in KOLLAR if ad in veri]
        sat.append(f"| `{k}` | " + " | ".join(h) + " |")
    sat += ["", "⚠️ *«Otomatik iddialar geçti»* **kalite demek değildir**: bunlar biçim",
            "kapıları (soru sayısı, uydurma yok, uzunluk). **Terapötik kalite** EPITOME ve MI",
            "boyutlarında ölçülür — duygusal tepki, yorumlama, keşif, MI uyumu — ve o boyutlar",
            "**yalnız judge ile** ölçülebilir.", "",
            "## 3. ⛔⛔ Öteki yarı neden koşulmadı — ve maliyeti", "",
            "| yol | durum | maliyet |", "|---|---|---|",
            "| `agy:gemini-3.8-flash-high` (yapılandırılmış judge) | ⛔ **kota tükendi** (K96) | — |",
            "| Claude subagent | ⛔ **puanlayan olamaz** (K43/K45) | — |",
            f"| `qwen3.8:27b-mlx` (yerel, kotasız) | ⭐ çalışıyor | **{QWEN_SN} sn/kayıt** "
            f"(bu oturumda ölçüldü, v9) |", "",
            f"⭐ **Ölçülen maliyet:** 48 öğe × {QWEN_SN} sn = **{48*QWEN_SN/3600:.1f} saat/kol**.",
            "⛔ Ve **en az iki kol** gerekir: v9 rubriğiyle yargılanmış bir TABAN yok, yani",
            f"taban + v0.0.10 = **{2*48*QWEN_SN/3600:.1f} saat**.", "",
            "⛔⛔ **Üstelik bir soru daha açık:** K45 qwen↔gemini uyumunu **%1,4** ölçmüştü ama",
            "o ölçüm **v1/v4 rubriğiyleydi**; v9'da uyum **ölçülmedi**. qwen'i metrik yapmak,",
            "ölçülmemiş bir uyuma dayanmak demek. ➡️ *Bir judge'ı değiştirmek, ölçüt değiştirmektir;",
            "yeni judge'ın eskisiyle uyumu ÖLÇÜLMEDEN sayıları aynı tabloda okunamaz (K97/K137).*", "",
            "⭐ **Ama cevaplar sabit ve kayıtlı** ⇒ judge sonradan koşulabilir",
            "(`--yeniden-judge`) ve üretim tekrarlanmaz. Bu raporun ölçtüğü şey kaybolmaz.", "",
            "## ⛔ Bu raporun söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Bu bir Eksen 1 SONUCU DEĞİL** | Pareto'nun üçüncü adımı hâlâ açık; "
            "burada ölçülen şey biçim kapıları ve üretim sağlığı |",
            "| ⛔ **Kollar farklı veriden** | `gd2-A-dar` v0.0.5 korpusundan; v0.0.10 ile "
            "aynı tabloda yalnız ÜRETİM SAĞLIĞI için okunabilir, kalite için değil |",
            "| ⚠️ **164 sn/kayıt tek kayıttan** | n=1 sonda; ortalama değil, büyüklük sırası |",
            "| ⚠️ Ortalama token düşüyor (555 → 373) | bu bir kalite işareti DEĞİL; "
            "kısalık hem iyi hem kötü olabilir ve hangisi olduğunu judge söyler |", ""]

    (KOK / f"reports/analiz/{TARIH}-eksen1-judgesiz.json").write_text(
        json.dumps({"tarih": TARIH, "veri": veri, "qwen_sn_kayit": QWEN_SN},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[8:]))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
