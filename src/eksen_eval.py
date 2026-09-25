#!/usr/bin/env python3
"""Eksen 2/3/4/5 koşucusu — üretim + DETERMİNİSTİK iddia denetimi.

`golden_eval.py` Eksen 1 içindir ve kendi iddia sözlüğünü kullanır. Bu eksenlerin
iddiaları `src/smoke_checks.py`'de ve çoğu deterministik; bu yüzden ayrı ama
**üretim yolunu paylaşan** bir koşucu gerekiyor (aynı `uret`, aynı prompt kurulumu —
yoksa iki eksen arasındaki fark modelin değil koşucunun farkı olur).

Judge tipindeki iddialar burada **denetlenemedi** kalır: Gemini kotası tükendi (K96)
ve judge Claude subagent'larla ayrı yürütülüyor (K97). Geçti SAYILMAZ.

Kullanım:
  uv run python src/eksen_eval.py evals/forgetting_smoke.jsonl --etiket fs-baseline
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
import time
from datetime import datetime
from pathlib import Path

KOK = Path(__file__).parent.parent
sys.path.insert(0, str(KOK / "src"))
import smoke_checks as sc  # noqa: E402
from golden_eval import uret  # noqa: E402  (aynı üretim yolu — bilerek)

import yaml  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("set_yolu")
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--etiket", default=None)
    ap.add_argument("--max-tokens", type=int, default=1024)
    ap.add_argument("--thinking", action="store_true")
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--yeniden", default=None,
                    help="kayıtlı koşu dizininden iddiaları YENİDEN denetle — "
                         "üretim tekrar koşulmaz. Denetleyici kusuru düzeltildiğinde "
                         "kullanılır; cevaplar sabit kaldığı için düzeltmenin etkisi "
                         "modelin oynaklığından AYRIŞIR (golden_eval --yeniden ile aynı gerekçe).")
    a = ap.parse_args()

    cfg = yaml.safe_load((KOK / "configs/training/e4b.yaml").read_text())
    model_dir = KOK / "models" / (cfg["model"].split("/")[-1] + "-train")
    if not model_dir.exists():
        model_dir = Path(cfg["model"])

    ogeler = [json.loads(l) for l in open(KOK / a.set_yolu) if l.strip()]
    if a.n:
        ogeler = ogeler[:a.n]
    etiket = a.etiket or Path(a.set_yolu).stem
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    cikti_dir = KOK / "reports/analiz/eksen-kosu" / f"{ts}-{etiket}"

    if a.yeniden:
        eski_dir = KOK / a.yeniden if not Path(a.yeniden).is_absolute() else Path(a.yeniden)
        eski = {json.loads(l)["id"]: json.loads(l)
                for l in open(eski_dir / "sonuclar.jsonl")}
        ogeler = [o for o in ogeler if o["id"] in eski]
        ciktilar = [{"id": o["id"], "cevap": eski[o["id"]]["cevap"],
                     "thinking": eski[o["id"]]["thinking"],
                     "sure_sn": eski[o["id"]]["sure_sn"],
                     "kesildi": eski[o["id"]]["kesildi"]} for o in ogeler]
        uretim_sn = json.loads((eski_dir / "kosu.json").read_text())["uretim_sn"]
        cikti_dir = eski_dir
        print(f"kayıtlı koşudan yeniden denetim: {len(ogeler)} öğe — üretim koşulmadı")
    else:
        print(f"eksen koşu · {len(ogeler)} öğe · {etiket} · "
              f"thinking={'açık' if a.thinking else 'kapalı'}")
        t0 = time.time()
        ciktilar = uret(model_dir, Path(a.adapter) if a.adapter else None,
                        ogeler, a.max_tokens, a.thinking)
        uretim_sn = time.time() - t0

    return degerlendir_yaz(ogeler, ciktilar, uretim_sn, cikti_dir, etiket, a.set_yolu,
                           a.adapter, model_dir, a.thinking, a.max_tokens)


def degerlendir_yaz(ogeler: list[dict], ciktilar: list[dict], uretim_sn: float,
                    cikti_dir: Path, etiket: str, set_yolu: str, adapter: str | None,
                    model_dir: Path, thinking: bool, max_tokens: int) -> int:
    """İddia denetimi + diske yazma. `main` ve toplu koşucu (EK-1 ölçümü) AYNI
    fonksiyonu çağırır — iki ayrı «koşu çıktısı» tanımı doğmasın (K103)."""
    sonuclar, gecen, dusen, denetlenemeyen = [], 0, 0, 0
    for oge, cikti in zip(ogeler, ciktilar):
        cevap = cikti["cevap"]
        iddia_sonuc, oge_gecti, oge_judge = [], True, 0
        # ⚠️ ÖN KOŞUL (golden_eval ile aynı gerekçe): BOŞ cevap bütün yokluk
        # iddialarını kendiliğinden geçer. Cevap yoksa öğe kalır.
        if not cevap.strip():
            oge_gecti = False
            iddia_sonuc.append({"kural": "_on_kosul", "gecti": False,
                                "kanit": "cevap boş"})
        else:
            for i in oge["iddialar"]:
                if i.get("tip", "otomatik") == "judge":
                    oge_judge += 1
                    iddia_sonuc.append({"tip": "judge", "alan": i.get("alan"),
                                        "gecti": None, "kanit": "denetlenemedi (judge ayrı koşuyor)"})
                    continue
                g, k = sc.denetle(i, cevap)
                iddia_sonuc.append({"kural": i["kural"], "deger": i.get("deger"),
                                    "gecti": g, "kanit": k})
                oge_gecti = oge_gecti and g
        if not cevap.strip():
            dusen += 1
        elif oge_gecti:
            gecen += 1
        if oge_judge:
            denetlenemeyen += 1
        sonuclar.append({**{k: oge[k] for k in ("id", "eksen", "sonda") if k in oge},
                         "kategori": oge.get("kategori"), "kutup": oge.get("kutup"),
                         "dilim": oge.get("dilim"), "bicim": oge.get("bicim"),
                         "cevap": cevap, "thinking": cikti["thinking"],
                         "sure_sn": cikti["sure_sn"], "kesildi": cikti["kesildi"],
                         "otomatik_gecti": oge_gecti if cevap.strip() else False,
                         "iddialar": iddia_sonuc})

    cikti_dir.mkdir(parents=True, exist_ok=True)
    (cikti_dir / "sonuclar.jsonl").write_text(
        "".join(json.dumps(s, ensure_ascii=False) + "\n" for s in sonuclar))
    (cikti_dir / "kosu.json").write_text(json.dumps(
        {"etiket": etiket, "set": set_yolu, "adapter": adapter,
         "model": str(model_dir), "thinking": thinking, "max_tokens": max_tokens,
         "oge": len(ogeler), "uretim_sn": round(uretim_sn),
         "otomatik_gecen": gecen, "bos_cevap": dusen,
         "judge_bekleyen_oge": denetlenemeyen,
         "tarih": datetime.now().isoformat(timespec="seconds")},
        ensure_ascii=False, indent=1))

    print(f"\n**otomatik iddialar:** {gecen}/{len(ogeler)} geçti · "
          f"{dusen} boş cevap · {denetlenemeyen} öğede judge iddiası bekliyor")
    grup = collections.Counter()
    for s in sonuclar:
        anahtar = s.get("kutup") or s.get("dilim") or s.get("kategori") or "—"
        if s["otomatik_gecti"]:
            grup[anahtar] += 1
    toplam = collections.Counter(
        (s.get("kutup") or s.get("dilim") or s.get("kategori") or "—") for s in sonuclar)
    for k in sorted(toplam):
        print(f"  {k:18} {grup.get(k,0):>3}/{toplam[k]}")
    print(f"üretim {uretim_sn/60:.1f} dk · yazıldı: {cikti_dir.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
