#!/usr/bin/env python3
"""v4-parti2 **v2** (düzeltilmiş) için judged dosyasını kurar.

⭐ Revizyon dalgası: `#25` ve `#38` düzeltildi ve YENİDEN puanlandı; kalan 58
kaydın cevabı değişmedi, ilk dalganın hükmü geçerli. `#18` ve `#34`'ün yalnızca
**thinking**'i düzeltildi — rubrik thinking'i kapsam dışı tuttuğu için (K120 §3)
hükümleri değişmez, ama kayıt metni değiştiği için judged dosyası v2'den kurulur.

⛔ Türetme yine KAYNAKLI (v9 şartı) ve `filter`ten çağrılır.
⛔ İlk dalganın çıktısı (`data/judged/v4-parti2.v9.jsonl`) **silinmez** — koşulmuş
bir ölçümün kaydı (Kural 7).
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

KORPUS = KOK / "data/candidates/v4-parti2.v2.jsonl"
ILK = KOK / "data/judged/v4-parti2.v9.jsonl"
CIKTI = KOK / "data/judged/v4-parti2.v2.v9.jsonl"
# revizyon dalgaları: etiket -> {iş no: parti_sira}
REV = {"parti2-v9-rev2": {"001": 25}, "parti2-v9-rev": {"002": 38}}


def main() -> int:
    kayit = {r["gen_meta"]["parti_sira"]: r for r in
             (json.loads(s) for s in KORPUS.read_text(encoding="utf-8").splitlines() if s.strip())}
    ilk = {r["gen_meta"]["parti_sira"]: (r.get("judge") or None) for r in
           (json.loads(s) for s in ILK.read_text(encoding="utf-8").splitlines() if s.strip())}

    yeniden = {}
    for etiket, harita in REV.items():
        d = BL.HZ.ISLER / etiket
        for no, sira in harita.items():
            ham = (d / "sonuc" / f"{no}.json").read_text(encoding="utf-8").strip()
            if ham.startswith("```"):
                ham = ham.split("```")[1].removeprefix("json").strip()
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

    guv = [r["gen_meta"]["parti_sira"] for r in satirlar
           if (r.get("judge") or {}).get("klinik_guvenlik_ihlali")]
    gr2 = [r["gen_meta"]["parti_sira"] for r in satirlar if (r.get("judge") or {}).get("grounding") == 2]
    print(f"{len(satirlar)} kayıt · yeniden puanlanan {sorted(yeniden)}")
    print(f"⛔ klinik güvenlik ihlali: {guv}")
    print(f"grounding==2: {gr2 or 'yok'}   (v1'de [25, 38] idi)")
    print(f"→ {CIKTI.relative_to(KOK)} sha {hashlib.sha256(CIKTI.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
