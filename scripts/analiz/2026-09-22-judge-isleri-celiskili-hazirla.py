#!/usr/bin/env python3
"""`celiskili` sınıfının 12 kaydı için KÖR judge işleri kurar.

Pilot (6) + parti2 (6) = 12 kayıt; hiçbiri yargılanmadı. Bu koşu
§7a″'nın **ilk yargısıdır** — sınıfın kendi kapısından geçmesi ile
rubriğin ona verdiği notun aynı şey olmadığını görmek için.

⭐ **K97'nin iki şartı burada da geçerli:**

  1. **KÖRLÜK.** İş dosyasında yalnız konuşma var; parti, tohum, banka
     numarası, kimin yazdığı YAZMAZ. İş numaraları karıştırılıyor.
     ⚠️ ⛔ **Ama bu küme yapısı gereği tam kör DEĞİL:** 12 kaydın
     hepsinde iki çelişkili `<context>` var ve cevapların hepsi
     çelişkiyi adlandırıyor ⇒ yargıç kayıtların **aynı sınıftan**
     olduğunu metinden anlayabilir. Karıştırma partiyi gizler, sınıfı
     gizleyemez. Bu **ölçülemez bir sızıntıdır** ve notlar okunurken
     böyle okunmalı.
  2. **ÖLÇÜLEBİLİRLİK.** `N_TEKRAR` kayıt iki ayrı numarayla, ayrı
     öbeklere düşürülerek soruluyor ⇒ bu dalganın kendi gürültü tabanı.
     ⛔ n küçük (4 çift): taban **kaba**, güven aralığı geniş; başka bir
     dalganın tabanının yerine geçmez.

⛔ **Prompt kopyalanmıyor, TÜRETİLİYOR (K103):** `prompt_kur` 09-15
betiğinden import edilir ve `rubrik + ayrac + govde == prompt_kur(kayıt)`
bayt bayt doğrulanır; olmazsa betik DURUR.

Çıktı: <scratchpad>/judge-isleri/celiskili/istek/NN.txt + kimlikler.json
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import filter as f  # noqa: E402

# ⛔⛔ 09-15 betiği modül düzeyinde `sys.argv`'i EZİYOR; kendi argümanlarımız
#   onun altında kalıyordu (ilk koşuda --banka/--dizin sessizce yok sayıldı).
_ARGV = sys.argv[:]
_yol = KOK / "scripts/analiz/2026-09-15-judge-isleri-hazirla.py"
_spec = _iu.spec_from_file_location("_hazirla15", _yol)
_h15 = _iu.module_from_spec(_spec)
sys.argv = [str(_yol)]
_spec.loader.exec_module(_h15)
sys.argv = _ARGV                     # ⭐ geri al
prompt_kur = _h15.prompt_kur

SCRATCH = Path(os.environ["BIRAG_SCRATCH"])
TOHUM = 20260922
OBEK = 8
VARSAYILAN_KAYNAK = ["data/candidates/celiskili-pilot.jsonl",
                     "data/candidates/celiskili-parti2.jsonl"]


def main() -> int:
    # ⭐ Onarım sonrası yeniden yargı için parametreli: belirli banka
    #   numaraları, ayrı dizin, tekrar kümesiz.
    ap = argparse.ArgumentParser()
    ap.add_argument("--banka", default="", help="virgüllü banka no süzgeci")
    ap.add_argument("--dizin", default="celiskili")
    ap.add_argument("--tekrar", type=int, default=4)
    ap.add_argument("--kaynak", default="", help="virgüllü jsonl yolları")
    a = ap.parse_args()
    global DIZIN, N_TEKRAR
    DIZIN = SCRATCH / f"judge-isleri/{a.dizin}"
    N_TEKRAR = a.tekrar
    suzgec = {int(x) for x in a.banka.split(",") if x.strip()}
    KAYNAK = ([x.strip() for x in a.kaynak.split(",") if x.strip()]
              or VARSAYILAN_KAYNAK)

    rubrik = f.JUDGE_PROMPT_PATH.read_text()
    kayitlar: dict[str, dict] = {}
    for yol in KAYNAK:
        for l in open(KOK / yol):
            r = json.loads(l)
            if r.get("replay"):          # K89: replay judge'a girmez
                continue
            if suzgec and r["gen_meta"].get("celiskili_banka_no") not in suzgec:
                continue
            kayitlar[r["id"]] = r
    if not kayitlar:
        raise SystemExit("⛔ yargılanacak kayıt yok")

    rng = random.Random(TOHUM)
    isler = sorted(kayitlar)
    tekrar = rng.sample(isler, min(N_TEKRAR, len(isler))) if N_TEKRAR else []
    tum = [(k, False) for k in isler] + [(k, True) for k in tekrar]
    rng.shuffle(tum)                     # ⛔ körlük: numara sırayı ele vermesin

    # ⛔ TEKRAR çifti aynı öbeğe düşmemeli — düşerse tek numaralı bir işle takas.
    yer: dict[str, list[int]] = {}
    for idx, (kid, _) in enumerate(tum):
        yer.setdefault(kid, []).append(idx)
    for kid, yerler in yer.items():
        if len(yerler) == 2 and yerler[0] // OBEK == yerler[1] // OBEK:
            a = yerler[1]
            b = next(j for j in range(len(tum))
                     if j // OBEK != yerler[0] // OBEK and len(yer[tum[j][0]]) == 1)
            tum[a], tum[b] = tum[b], tum[a]
            yer[tum[a][0]], yer[tum[b][0]] = [a], [b]
    for kid, yerler in yer.items():
        if len(yerler) == 2 and yerler[0] // OBEK == yerler[1] // OBEK:
            raise SystemExit(f"⛔ tekrar çifti aynı öbekte kaldı: {kid}")

    (DIZIN / "istek").mkdir(parents=True, exist_ok=True)
    (DIZIN / "sonuc").mkdir(parents=True, exist_ok=True)
    kimlikler = []
    ayrac = "\n\n---\n\n## Değerlendirilecek konuşma\n\n"
    for i, (kid, dup) in enumerate(tum, 1):
        tam = prompt_kur(kayitlar[kid])
        govde = tam[len(rubrik) + len(ayrac):]
        if rubrik + ayrac + govde != tam:     # ⛔⛔ BAYT BAYT
            raise SystemExit(f"⛔ prompt ayrıştırması bayt uyumsuz: {kid}")
        (DIZIN / "istek" / f"{i:02d}.txt").write_text(govde, encoding="utf-8")
        kimlikler.append({"no": f"{i:02d}", "id": kid, "tekrar": dup})
    (DIZIN / "kimlikler.json").write_text(
        json.dumps(kimlikler, ensure_ascii=False, indent=1), encoding="utf-8")
    assert len(list((DIZIN / "istek").glob("*.txt"))) == len(tum)

    print(f"⭐ {len(kimlikler)} iş · kayıt {len(isler)} · tekrar {len(tekrar)}")
    print(f"   öbek {OBEK} ⇒ {-(-len(kimlikler) // OBEK)} subagent")
    print(f"   rubrik {f.JUDGE_PROMPT_VERSION} ({len(rubrik)} bayt, ayrı okunur)")
    print(f"→ {DIZIN}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
