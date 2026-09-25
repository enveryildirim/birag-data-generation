#!/usr/bin/env python3
"""Subagent judge sonuçlarını toplar — türetme `filter.py` ile BİREBİR aynı yoldan.

Kritik nokta: `anlasilirlik`, `dogallik`, `mi_uyumu`, `tuzak_ihlali` ve Bölüm F'nin
altı bayrağı judge'dan GELMEZ, koddan hesaplanır. Subagent sonuçları da tam olarak
aynı fonksiyonlardan geçmeli — yoksa Gemini ile karşılaştırma, rubrik farkını değil
**hesap farkını** ölçer.

Kullanım:
  uv run python <betik> <etiket> --golden <kaynak-koşu-dizini>
  uv run python <betik> <etiket> --korpus <candidates.jsonl> --cikti <judged.jsonl>
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import filter as f  # noqa: E402
from schemas import JudgeResult  # noqa: E402

ISLER = Path("/private/tmp/claude-501/-Users-pc-projects-birag-data-finetuning"
             "/fe6477c2-8e5e-439e-875d-df2b5ed62d91/scratchpad/judge-isleri")
# Judge adı dalgaya göre DEĞİŞİR: ilk dalga varsayılan modeldi, 2026-09-15
# ikinci dalga açıkça Sonnet. Aynı etiketle yazılırsa iki judge ayırt edilemez
# ve K45 bağımsızlık ölçümü anlamını yitirir. Bu yüzden argümandan gelir.
JUDGE_ADI = "claude-subagent"   # --judge-adi ile ezilir
# Rubrik sürümü de dalgaya göre değişir. `filter.JUDGE_PROMPT_VERSION` VARSAYILANDIR
# ve varsayılan ilerler (v6 -> v7); eski bir dalga sonradan toplanırsa kayıtlara yanlış
# sürüm yazılır ve iki rubrik ayırt edilemez hâle gelir. Bu yüzden argümandan gelebilir.
RUBRIK = f.JUDGE_PROMPT_VERSION


def turet(data: dict) -> dict:
    """filter.judge_record'un türetme adımlarının BİREBİR aynısı."""
    data["judge_model"] = JUDGE_ADI
    data["prompt_version"] = RUBRIK
    f.f_bolumu_turet(data)
    for alan, hesap in (("anlasilirlik", f.anlasilirlik_hesapla),
                        ("dogallik", f.dogallik_hesapla),
                        ("mi_uyumu", f.mi_uyumu_hesapla)):
        deger = hesap(data)
        if deger is not None:
            data[alan] = deger
    if any(k in data for k in f.TUZAKLAR):
        data["tuzak_ihlali"] = [ad for k, ad in f.TUZAKLAR.items() if data.get(k) is True]
    return JudgeResult(**data).model_dump()


def main() -> None:
    global JUDGE_ADI, RUBRIK
    ap = argparse.ArgumentParser()
    ap.add_argument("etiket")
    ap.add_argument("--golden", help="kaynak golden koşu dizini (cevaplar oradan alınır)")
    ap.add_argument("--korpus")
    ap.add_argument("--cikti")
    ap.add_argument("--judge-adi", default=JUDGE_ADI,
                    help="kayıtlara yazılacak judge kimliği (dalgayı ayırt eder)")
    ap.add_argument("--rubrik", default=RUBRIK,
                    help="kayıtlara yazılacak rubrik sürümü (dalga hangi sürümle koştuysa)")
    a = ap.parse_args()
    JUDGE_ADI = a.judge_adi
    RUBRIK = a.rubrik

    dizin = ISLER / a.etiket
    kimlikler = json.loads((dizin / "kimlikler.json").read_text())
    sonuc = {}
    eksik, bozuk = [], []
    for k in kimlikler:
        yol = dizin / "sonuc" / f"{k['no']}.json"
        if not yol.exists():
            eksik.append(k["no"]); continue
        try:
            ham = yol.read_text().strip()
            # Subagent bazen kod bloğu sarabilir — tolere et, ama sessizce değil.
            if ham.startswith("```"):
                ham = ham.split("```")[1].removeprefix("json").strip()
            sonuc[k["id"]] = turet(json.loads(ham))
        except Exception as e:
            bozuk.append((k["no"], f"{type(e).__name__}: {e}"[:120]))

    print(f"toplandı: {len(sonuc)}/{len(kimlikler)} · eksik: {len(eksik)} · bozuk: {len(bozuk)}")
    for no, h in bozuk:
        print(f"  BOZUK {no}: {h}")
    if eksik:
        print(f"  EKSİK: {', '.join(eksik)}")

    if a.golden:
        kaynak = KOK / a.golden if not Path(a.golden).is_absolute() else Path(a.golden)
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        hedef = KOK / "reports/analiz/golden-kosu" / f"{ts}-{a.etiket}"
        hedef.mkdir(parents=True, exist_ok=True)
        satirlar = []
        for satir in open(kaynak / "sonuclar.jsonl"):
            r = json.loads(satir)
            r["judge"] = sonuc.get(r["id"])
            satirlar.append(r)
        (hedef / "sonuclar.jsonl").write_text(
            "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in satirlar))
        meta = json.loads((kaynak / "kosu.json").read_text())
        meta.update({"etiket": a.etiket, "judge_rubrik": RUBRIK,
                     "judge_model": JUDGE_ADI, "judge_sn": 0,
                     "tarih": datetime.now().isoformat(timespec="seconds")})
        (hedef / "kosu.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
        print(f"yazıldı: {hedef.relative_to(KOK)}")
    elif a.korpus and a.cikti:
        satirlar = []
        for satir in open(KOK / a.korpus):
            r = json.loads(satir)
            if not r.get("replay"):
                r["judge"] = sonuc.get(r["id"])
            satirlar.append(r)
        (KOK / a.cikti).write_text(
            "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in satirlar))
        print(f"yazıldı: {a.cikti}")


if __name__ == "__main__":
    main()
