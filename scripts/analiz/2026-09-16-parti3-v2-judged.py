#!/usr/bin/env python3
"""v5-parti3 **v2** (düzeltilmiş) için judged dosyasını kurar.

⭐ Revizyon dalgaları `kimlikler.json`dan OKUNUR, elle eşlenmez — iş numarası ile
`parti_sira` arasındaki eşleme korpus sırasına bağlı ve elle yazılırsa ilk sıra
değişikliğinde sessizce kayar.

⛔ İlk dalganın çıktısı (`data/judged/v5-parti3.v9.jsonl`) SİLİNMEZ (Kural 7).
⛔ Türetme KAYNAKLI (v9 şartı) ve `filter`ten çağrılır.
"""
from __future__ import annotations
import hashlib, json, sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import filter as f  # noqa: E402
from checks import run_checks  # noqa: E402

_sp = _iu.spec_from_file_location("bl", KOK / "scripts/analiz/2026-09-16-parti2-judge-birlestir.py")
BL = _iu.module_from_spec(_sp); _sp.loader.exec_module(BL)

KORPUS = KOK / "data/candidates/v5-parti3.v2.jsonl"
ILK = KOK / "data/judged/v5-parti3.v9.jsonl"
CIKTI = KOK / "data/judged/v5-parti3.v2.v9.jsonl"
# sonra gelen dalga öncekini EZER (rev2, rev'i ezer)
DALGALAR = ["parti3-v9-rev", "parti3-v9-rev2"]


def main() -> int:
    kayit = {r["gen_meta"]["parti_sira"]: r for r in
             (json.loads(s) for s in KORPUS.read_text(encoding="utf-8").splitlines() if s.strip())}
    kimlik_sira = {r["id"]: r["gen_meta"]["parti_sira"] for r in kayit.values()}
    ilk = {r["gen_meta"]["parti_sira"]: (r.get("judge") or None) for r in
           (json.loads(s) for s in ILK.read_text(encoding="utf-8").splitlines() if s.strip())}

    yeniden = {}
    for etiket in DALGALAR:
        d = BL.HZ.ISLER / etiket
        for k in json.loads((d / "kimlikler.json").read_text(encoding="utf-8")):
            yol = d / "sonuc" / f"{k['no']}.json"
            if not yol.exists():
                print(f"  ⚠️ {etiket}/{k['no']} sonucu yok, atlanıyor"); continue
            ham = yol.read_text(encoding="utf-8").strip()
            if ham.startswith("```"):
                ham = ham.split("```")[1].removeprefix("json").strip()
            sira = kimlik_sira[k["id"]]
            yeniden[sira] = BL.turet(json.loads(ham), f.kaynak_metinleri(kayit[sira]))

    satirlar = []
    for sira in sorted(kayit):
        r = kayit[sira]
        r["_checks"] = run_checks(r)
        r["judge"] = yeniden.get(sira, ilk.get(sira))
        if sira in yeniden:
            r["gen_meta"]["judge_dalgasi"] = "revizyon"
        satirlar.append(r)
    CIKTI.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in satirlar),
                     encoding="utf-8")

    j = lambda r: (r.get("judge") or {})
    dolu = [r for r in satirlar if j(r).get("en_somut_ayrinti") not in (None, "YOK")]
    uyd = [r["gen_meta"]["parti_sira"] for r in dolu if j(r).get("ayrinti_konusmada_var") is False]
    print(f"{len(satirlar)} kayıt · yeniden puanlanan {sorted(yeniden)}")
    print(f"⛔ klinik güvenlik ihlali: {[r['gen_meta']['parti_sira'] for r in satirlar if j(r).get('klinik_guvenlik_ihlali')]}")
    print(f"⛔ kurum_yordam_ihlali  : {[r['gen_meta']['parti_sira'] for r in satirlar if j(r).get('kurum_yordam_ihlali')]}")
    print(f"⛔ uydurma ayrıntı      : {uyd} ({len(uyd)}/{len(dolu)})   — v1'de 6/58")
    print(f"   grounding==2         : {[r['gen_meta']['parti_sira'] for r in satirlar if j(r).get('grounding')==2]}")
    print(f"→ {CIKTI.relative_to(KOK)} sha {hashlib.sha256(CIKTI.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
