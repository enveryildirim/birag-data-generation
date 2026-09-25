#!/usr/bin/env python3
"""v4-parti2 judge sonuçlarını toplar — rubrik **v9**, doğrulama KAYNAKLI.

⛔⛔ **Neden yeni bir toplayıcı gerekti.** Eski toplayıcı
`2026-09-15-judge-sonuclari-topla.py` türetmeyi `f.f_bolumu_turet(data)` diye,
yani **kaynak metin VERMEDEN** çağırıyor. v7 için doğruydu; v9'da doğrulama
kaynağa bakar (K120) ve kaynak yoksa **doğrulanamayan muafiyet DÜŞER** ⇒ eski
toplayıcıyla bir v9 koşusu sessizce **ihlal sayısını şişirir**. Yön Kural 3
açısından güvenli, ama sayı yanlış olur. ⇒ Burada `v9-birlestir.py`nin yaptığı
gibi `f.kaynak_metinleri(kayit)` verilir.
➡️ *Bir rubrik sürümü ilerlerken onu OKUYAN araçlar da ilerlemek zorundadır;
ilerlemeyen araç hatayı sessiz ve tek yönlü yapar.*

⭐ Türetme adımları `filter`ten **çağrılır**, kopyalanmaz.
⭐ `_checks` de `filter.main`in yaptığı gibi kaydedilir — `build.py` onu okuyor
ve yoksa BÜTÜN kayıtları eler.

Kullanım:
  uv run python scripts/analiz/2026-09-16-parti2-judge-birlestir.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import filter as f            # noqa: E402
from checks import run_checks  # noqa: E402
from schemas import JudgeResult  # noqa: E402

_sp = _iu.spec_from_file_location("hz", KOK / "scripts/analiz/2026-09-16-parti2-judge-hazirla.py")
HZ = _iu.module_from_spec(_sp)
_sp.loader.exec_module(HZ)

KORPUS = HZ.KORPUS
DIZIN = HZ.ISLER / HZ.ETIKET
# ⚠️ Varsayılanlar DEĞİŞMEDİ; ortam değişkeni sonraki partiler için ek giriş.
import os
CIKTI = KOK / os.environ.get("BIRAG_JUDGED_CIKTI", "data/judged/v4-parti2.v9.jsonl")
RAPOR = KOK / os.environ.get("BIRAG_JUDGED_RAPOR",
                             "reports/analiz/2026-09-16-parti2-judge-v9.json")
JUDGE_ADI = "claude-sonnet-subagent"
RUBRIK = "judge-eksen1.v9"


def turet(data: dict, kaynak: dict) -> dict:
    """`filter.judge_record`ün türetme adımlarının BİREBİR aynısı (kaynaklı)."""
    data["judge_model"] = JUDGE_ADI
    data["prompt_version"] = RUBRIK
    f.f_bolumu_turet(data, kaynak)
    for alan, hesap in (("anlasilirlik", f.anlasilirlik_hesapla),
                        ("dogallik", f.dogallik_hesapla),
                        ("mi_uyumu", f.mi_uyumu_hesapla)):
        d = hesap(data)
        if d is not None:
            data[alan] = d
    if any(k in data for k in f.TUZAKLAR):
        data["tuzak_ihlali"] = [ad for k, ad in f.TUZAKLAR.items() if data.get(k) is True]
    return JudgeResult(**data).model_dump()


def main() -> int:
    kayitlar = {r["id"]: r for r in
                (json.loads(s) for s in KORPUS.read_text(encoding="utf-8").splitlines() if s.strip())}
    kimlikler = json.loads((DIZIN / "kimlikler.json").read_text(encoding="utf-8"))

    sonuc, eksik, bozuk, dogrulanmadi = {}, [], [], []
    for k in kimlikler:
        yol = DIZIN / "sonuc" / f"{k['no']}.json"
        if not yol.exists():
            eksik.append(k["no"])
            continue
        try:
            ham = yol.read_text(encoding="utf-8").strip()
            if ham.startswith("```"):
                ham = ham.split("```")[1].removeprefix("json").strip()
            d = json.loads(ham)
            kaynak = f.kaynak_metinleri(kayitlar[k["id"]])
            j = turet(d, kaynak)
            if j.get("alinti_dogrulanmadi"):
                dogrulanmadi.append({"no": k["no"], "id": k["id"][:16],
                                     "alanlar": j["alinti_dogrulanmadi"]})
            sonuc[k["id"]] = j
        except Exception as e:
            bozuk.append({"no": k["no"], "hata": f"{type(e).__name__}: {e}"[:160]})

    # ⭐ `_checks` filter.main ile aynı biçimde; replay kaydı yok ama kural korunur.
    satirlar = []
    for r in kayitlar.values():
        r["_checks"] = run_checks(r)
        if not r.get("replay"):
            r["judge"] = sonuc.get(r["id"])
        satirlar.append(r)
    CIKTI.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in satirlar),
                     encoding="utf-8")

    guvenlik = [r["gen_meta"]["parti_sira"] for r in satirlar
                if (r.get("judge") or {}).get("klinik_guvenlik_ihlali")]
    rol = [r["gen_meta"]["parti_sira"] for r in satirlar
           if (r.get("judge") or {}).get("rol_siniri_ihlali")]
    checks_elenen = [r["gen_meta"]["parti_sira"] for r in satirlar if not r["_checks"]["passed"]]

    rapor = {
        "tarih": "2026-09-16",
        "betik": "scripts/analiz/2026-09-16-parti2-judge-birlestir.py",
        "korpus": str(KORPUS.relative_to(KOK)),
        "korpus_sha256_16": hashlib.sha256(KORPUS.read_bytes()).hexdigest()[:16],
        "rubrik": RUBRIK,
        "rubrik_sha256_16": hashlib.sha256((KOK / f"prompts/{RUBRIK}.md").read_bytes()).hexdigest()[:16],
        "judge_model": JUDGE_ADI,
        "k": 1,
        "kayit": len(satirlar),
        "toplanan": len(sonuc),
        "eksik": eksik,
        "bozuk": bozuk,
        "checks_elenen": checks_elenen,
        "klinik_guvenlik_ihlali": guvenlik,
        "rol_siniri_ihlali": rol,
        "alinti_dogrulanmadi": dogrulanmadi,
        "cikti": str(CIKTI.relative_to(KOK)),
        "cikti_sha256_16": hashlib.sha256(CIKTI.read_bytes()).hexdigest()[:16],
    }
    RAPOR.write_text(json.dumps(rapor, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"toplandı {len(sonuc)}/{len(kimlikler)} · eksik {len(eksik)} · bozuk {len(bozuk)}")
    for b in bozuk:
        print(f"  ⛔ BOZUK {b['no']}: {b['hata']}")
    if eksik:
        print(f"  ⛔ EKSİK: {', '.join(eksik)}")
    print(f"checks elenen: {checks_elenen or 'yok'}")
    print(f"⛔ klinik güvenlik ihlali: {guvenlik or 'yok'}")
    print(f"⚠️ rol sınırı ihlali: {rol or 'yok'}")
    print(f"⚠️ alıntı doğrulanmadı: {len(dogrulanmadi)} kayıt")
    print(f"→ {CIKTI.relative_to(KOK)} · {RAPOR.relative_to(KOK)}")
    return 1 if (eksik or bozuk) else 0


if __name__ == "__main__":
    raise SystemExit(main())
