#!/usr/bin/env python3
"""Judge işlerini DOSYAYA yazar — subagent'lar kör okusun diye.

Neden dosya: Gemini kotası tükendi (K96), yerel qwen makineyi 2 saat meşgul
ediyor. Üçüncü yol Claude subagent'ları. Ama K45 iki Claude judge'ın bağımsız
ailelerden **+6/+11 puan** yüksek verdiğini ölçtü ve korpusu Claude yazdı —
yani bu yolun bilinen bir sapması var.

Sapmayı yönetmenin iki şartı bu betikte:

  1. **KÖRLÜK.** Dosyada yalnızca rubrik + konuşma var. Metni kimin yazdığı,
     hangi korpustan geldiği, neyle karşılaştırılacağı YAZMAZ. Subagent'a giden
     talimat da bunu söylemez. Gemini'ye giden prompt neyse bu da odur — tek
     fark hangi modelin okuduğu.

  2. **ÖLÇÜLEBİLİRLİK.** Aynı prompt'lar Gemini'ye de gitmişti; sonuçları
     `reports/analiz/golden-kosu/*-v6/` altında duruyor. Yani Claude'un sapması
     bu rubrikte SIFIR kotayla ölçülebilir ve her raporda yazılabilir.

Kullanım:
  # golden koşusunun cevaplarını (model çıktısı) judge işine çevir
  uv run python <betik> --golden reports/analiz/golden-kosu/20260914-214626-baseline
  # korpus kayıtlarını judge işine çevir
  uv run python <betik> --korpus data/candidates/v3-kumulatif.jsonl
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import filter as f  # noqa: E402

ISLER = Path("/private/tmp/claude-501/-Users-pc-projects-birag-data-finetuning"
             "/fe6477c2-8e5e-439e-875d-df2b5ed62d91/scratchpad/judge-isleri")


def prompt_kur(kayit: dict) -> str:
    """filter.judge_record ile BİREBİR aynı prompt — tek fark okuyan model."""
    asst = f._last_assistant(kayit)
    return (f"{f.JUDGE_PROMPT_PATH.read_text()}\n\n---\n\n## Değerlendirilecek konuşma\n\n"
            f"{f._render_conversation(kayit)}\n\n"
            f"(iç muhakeme — değerlendirme dışı, yalnızca bağlam için: "
            f"{(asst.get('thinking') or '')[:500]})")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--golden", help="golden koşu dizini (model cevapları puanlanır)")
    ap.add_argument("--korpus", help="candidates jsonl (elle yazılmış kayıtlar puanlanır)")
    ap.add_argument("--set", default="evals/golden.dev.jsonl")
    ap.add_argument("--etiket", required=True, help="iş kümesi adı, dizin olur")
    a = ap.parse_args()

    isler: list[tuple[str, dict]] = []
    if a.golden:
        d = KOK / a.golden if not Path(a.golden).is_absolute() else Path(a.golden)
        ogeler = {o["id"]: o for o in
                  (json.loads(l) for l in open(KOK / a.set) if l.strip())}
        for satir in open(d / "sonuclar.jsonl"):
            r = json.loads(satir)
            if not r["cevap"].strip():
                continue
            oge = ogeler[r["id"]]
            sahte = {"messages": [{"role": m["role"], "content": m["content"]}
                                  for m in oge["messages"]]
                     + [{"role": "assistant", "content": r["cevap"],
                         "thinking": r["thinking"] or None}]}
            isler.append((r["id"], sahte))
    elif a.korpus:
        for satir in open(KOK / a.korpus):
            r = json.loads(satir)
            if r.get("replay"):          # replay judge'a girmez (K89)
                continue
            isler.append((r["id"], r))
    else:
        ap.error("--golden ya da --korpus verilmeli")

    dizin = ISLER / a.etiket
    (dizin / "istek").mkdir(parents=True, exist_ok=True)
    (dizin / "sonuc").mkdir(parents=True, exist_ok=True)
    kimlikler = []
    for i, (kid, kayit) in enumerate(isler, 1):
        (dizin / "istek" / f"{i:03d}.txt").write_text(prompt_kur(kayit))
        kimlikler.append({"no": f"{i:03d}", "id": kid})
    (dizin / "kimlikler.json").write_text(json.dumps(kimlikler, ensure_ascii=False, indent=1))

    print(f"{len(isler)} iş yazıldı: {dizin}/istek/")
    print(f"sonuçlar buraya beklenecek: {dizin}/sonuc/<no>.json")
    print(f"rubrik: {f.JUDGE_PROMPT_VERSION}")


if __name__ == "__main__":
    main()
