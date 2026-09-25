#!/usr/bin/env python3
"""`v6` partilerinin yargılanmamış 370 kaydı için KÖR judge işleri kurar.

⭐ **Kullanıcı kararı (2026-09-22): subagent judge.** ⛔ Bu K43/K45'i
çiğnemiyor — **K97 (09-15) judge'ı zaten Claude subagent'lara taşımıştı**,
aynı gerekçeyle (Gemini kotası) ve iki şartla. Şartlar burada da geçerli:

  1. **KÖRLÜK (K97).** İş dosyasında yalnızca konuşma var: parti, tohum,
     kimin yazdığı, neyle karşılaştırılacağı YAZMAZ. ⭐ İş numaraları
     ayrıca **karıştırılıyor** — yoksa ardışık numaralar partiyi ele verir.
  2. **ÖLÇÜLEBİLİRLİK.** İki ek küme koşuya katılıyor:
     · **EŞLİ (42):** `v6-parti3`'ün Gemini ile yargılanmış 42 kaydı ⇒ bu
       korpusta ilk kez Claude↔Gemini farkı **aynı kayıtlar üzerinde**
       ölçülebilir (K97'nin 48 kaydı başka bir korpustandı).
     · **TEKRAR (24):** aynı kayıt aynı dalgada **iki ayrı numarayla**,
       ayrı öbeklere düşerek soruluyor ⇒ bu dalganın kendi gürültü tabanı.
       ⛔⛔ Bu şart: K98 gürültü tabanını **v6 rubriğiyle** ölçtü, koşu
       **v9** ile gidiyor ⇒ eski taban bu koşu için geçerli DEĞİL, ve
       taban bilinmeden Claude↔Gemini farkı okunamaz.

⛔ **Prompt kopyalanmıyor, TÜRETİLİYOR (K103).** `prompt_kur` 09-15
betiğinden import edilir. ⭐ İş dosyası rubriği TAŞIMAZ (29 KB × 436 =
12 MB, her subagent aynı rubriği onlarca kez okurdu); rubriği ajan bir kez
okur. Bunun prompt'u değiştirmediği **bayt bayt** doğrulanır: betik
`rubrik + iş dosyası == prompt_kur(kayıt)` olmazsa DURUR.

⚠️ **Öbekleme bir bağımsızlık kaybıdır.** Gemini her kaydı ayrı çağrıda
gördü; bir subagent öbeğindeki 16 kayıt aynı bağlamda duruyor ⇒ sıra ve
çapa etkisi olabilir. Ölçülemez değil: TEKRAR kümesi çiftleri ayrı
öbeklere düşürüldüğü için bu etki gürültü tabanına dahil ölçülüyor.

Çıktı: <scratchpad>/judge-isleri/v6-kalan/istek/NNN.txt + kimlikler.json
"""
from __future__ import annotations

import json
import os
import random
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import filter as f  # noqa: E402

# ⭐ K103: prompt kurucu KOPYALANMIYOR, 09-15 betiğinden geliyor.
_yol = KOK / "scripts/analiz/2026-09-15-judge-isleri-hazirla.py"
_spec = _iu.spec_from_file_location("_hazirla15", _yol)
_h15 = _iu.module_from_spec(_spec)
sys.argv = [str(_yol)]          # argparse modül yüklenirken koşmaz ama garanti
_spec.loader.exec_module(_h15)
prompt_kur = _h15.prompt_kur

SCRATCH = Path(os.environ["BIRAG_SCRATCH"])
DIZIN = SCRATCH / "judge-isleri/v6-kalan"
TOHUM = 20260922
N_TEKRAR = 24
OBEK = 16

# (parti, yargılanmamışları mı yoksa hepsini mi)
KALAN = {"v6-parti3": "eksik", "v6-parti4": "hep", "v6-parti5": "hep",
         "v6-parti6": "hep", "v6-parti7": "hep", "v6-parti8": "hep"}


def main() -> int:
    rubrik = f.JUDGE_PROMPT_PATH.read_text()
    isler: list[tuple[str, str, str]] = []   # (id, parti, küme)
    kayitlar: dict[str, dict] = {}

    for parti, kip in KALAN.items():
        aday = {r["id"]: r for r in
                (json.loads(l) for l in open(KOK / f"data/candidates/{parti}.jsonl"))}
        yargili = set()
        yj = KOK / f"data/judged/{parti}.jsonl"
        if yj.exists():
            yargili = {json.loads(l)["id"] for l in open(yj) if json.loads(l).get("judge")}
        for kid, r in aday.items():
            if r.get("replay"):          # K89: replay judge'a girmez
                continue
            kume = "esli" if kid in yargili else "yeni"
            if kip == "eksik" or kume == "yeni":
                isler.append((kid, parti, kume))
                kayitlar[kid] = r

    rng = random.Random(TOHUM)
    # ⭐ TEKRAR kümesi: mevcut işlerden çekilir, ikinci bir numara alır.
    tekrar = rng.sample([i[0] for i in isler], N_TEKRAR)
    tum = [(k, p, q, False) for k, p, q in isler] + \
          [(k, "", "tekrar", True) for k in tekrar]
    rng.shuffle(tum)                     # ⛔ körlük: numara partiyi ele vermesin

    # ⛔ TEKRAR çifti aynı öbeğe düşmemeli — düşerse kaydır.
    yer = {}
    for idx, (kid, _, _, dup) in enumerate(tum):
        yer.setdefault(kid, []).append(idx)
    for kid, yerler in yer.items():
        if len(yerler) == 2 and yerler[0] // OBEK == yerler[1] // OBEK:
            a = yerler[1]
            b = next(j for j in range(len(tum)) if j // OBEK != yerler[0] // OBEK
                     and tum[j][0] not in (kid,) and len(yer[tum[j][0]]) == 1)
            tum[a], tum[b] = tum[b], tum[a]

    (DIZIN / "istek").mkdir(parents=True, exist_ok=True)
    (DIZIN / "sonuc").mkdir(parents=True, exist_ok=True)
    kimlikler = []
    ayrac = "\n\n---\n\n## Değerlendirilecek konuşma\n\n"
    for i, (kid, parti, kume, dup) in enumerate(tum, 1):
        tam = prompt_kur(kayitlar[kid])
        govde = tam[len(rubrik) + len(ayrac):]
        # ⛔⛔ BAYT BAYT: rubriği ayırmak prompt'u değiştirmiyor.
        if rubrik + ayrac + govde != tam:
            raise SystemExit(f"⛔ prompt ayrıştırması bayt uyumsuz: {kid}")
        (DIZIN / "istek" / f"{i:03d}.txt").write_text(govde, encoding="utf-8")
        kimlikler.append({"no": f"{i:03d}", "id": kid, "parti": parti,
                          "kume": kume, "tekrar": dup})
    (DIZIN / "kimlikler.json").write_text(
        json.dumps(kimlikler, ensure_ascii=False, indent=1), encoding="utf-8")

    n_yeni = sum(1 for k in kimlikler if k["kume"] == "yeni")
    n_esli = sum(1 for k in kimlikler if k["kume"] == "esli")
    print(f"⭐ {len(kimlikler)} iş · yeni {n_yeni} · eşli {n_esli} · tekrar {N_TEKRAR}")
    print(f"   öbek {OBEK} ⇒ {-(-len(kimlikler) // OBEK)} subagent")
    print(f"   rubrik {f.JUDGE_PROMPT_VERSION} ({len(rubrik)} bayt, ayrı okunur)")
    print(f"→ {DIZIN}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
