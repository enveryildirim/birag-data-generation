#!/usr/bin/env python3
"""Bir partinin yargısını, revizyon koşusuyla KAYNAŞTIRIR.

⛔⛔ **Neden ayrı bir araç.** Bir parti revize edildiğinde yalnız birkaç kayıt
değişir; kalanını yeniden yargılamak hem pahalı hem gereksizdir. Ama eski
yargıyı devralmanın **tek meşru koşulu** vardır: *devralınan kaydın puanlanan
metni birebir aynı olmalı.* Metin değiştiyse eski puan artık o metni tarif
etmez. ⇒ Bu betik devralmadan önce **asistan cevabını ve kullanıcı turlarını
karşılaştırır**; bir fark bulursa devralmayı reddeder ve kaydı `eksik` sayar.

➡️ *Yargıyı devralmak bir kolaylık değil, kanıtlanması gereken bir iddiadır.*

⭐ Türetme `filter`ten çağrılır (K120: doğrulama kaynağa bakar).

Kullanım (ortam değişkenleriyle):
  BIRAG_KAYNAS_KORPUS=data/candidates/v5-parti4.v3.jsonl \
  BIRAG_KAYNAS_TABAN=parti4-arinmis-v9 \
  BIRAG_KAYNAS_TABAN_KORPUS=data/candidates/v5-parti4.v2.arinmis.jsonl \
  BIRAG_KAYNAS_REV=parti4-v3-rev \
  BIRAG_KAYNAS_CIKTI=data/judged/v5-parti4.v3.v9.jsonl \
  BIRAG_KAYNAS_RAPOR=reports/analiz/2026-09-17-parti4-v3-judge.md \
  uv run python scripts/analiz/2026-09-17-judge-revizyon-kaynastir.py
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import filter as f            # noqa: E402
from checks import run_checks  # noqa: E402
from schemas import JudgeResult  # noqa: E402

_sp = _iu.spec_from_file_location("bl", KOK / "scripts/analiz/2026-09-16-parti2-judge-birlestir.py")
BL = _iu.module_from_spec(_sp)
_sp.loader.exec_module(BL)          # ⭐ `turet` kopyalanmaz, çağrılır

ISLER = Path("/private/tmp/claude-501/-Users-pc-projects-birag-data-finetuning"
             "/fe6477c2-8e5e-439e-875d-df2b5ed62d91/scratchpad/judge-isleri")

KORPUS = KOK / os.environ["BIRAG_KAYNAS_KORPUS"]
# ⭐ Taban iki biçimde verilebilir: bir İŞ DİZİNİ adı ya da doğrudan
# YARGILANMIŞ bir `.jsonl`. İkincisi eski katmanlar için gerekli — onların iş
# dizinleri farklı etiketlerle kurulmuştu ve yargı zaten dosyanın içinde duruyor.
_t = os.environ["BIRAG_KAYNAS_TABAN"]
TABAN_DOSYA = _t.endswith(".jsonl")
TABAN = (KOK / _t) if TABAN_DOSYA else (ISLER / _t)
TABAN_KORPUS = KOK / os.environ.get("BIRAG_KAYNAS_TABAN_KORPUS", _t)
REV = [ISLER / x for x in os.environ["BIRAG_KAYNAS_REV"].split(",") if x.strip()]
CIKTI = KOK / os.environ["BIRAG_KAYNAS_CIKTI"]
RAPOR = KOK / os.environ["BIRAG_KAYNAS_RAPOR"]
RUBRIK = BL.RUBRIK


def _puanlanan(r: dict) -> str:
    """Puanlanan metin: son asistan cevabı + bütün kullanıcı turları.

    ⛔ `thinking` DIŞARIDA: judge onu puanlamaz (T120), arındırma onu değiştirir
    ve bu, cevap aynıyken devralmayı haksız yere engellerdi.
    """
    par = []
    for m in r["messages"]:
        if m["role"] == "user":
            par.append("U:" + m["content"])
        elif m["role"] == "assistant":
            par.append("A:" + (m.get("content") or ""))
    return "\n".join(par)


def _sha(r: dict) -> str:
    import hashlib
    return hashlib.sha256(_puanlanan(r).encode("utf-8")).hexdigest()[:16]


def _oku(dizin: Path, kayitlar: dict, sonuc: dict, bozuk: list, dogrulanmadi: list,
         bayat: list | None = None) -> set[str]:
    """Bir iş dizininin sonuçlarını `sonuc`a yazar; işlenen id kümesini döner.

    ⛔⛔ **BAYAT SONUÇ DENETİMİ.** `kimlikler.json` artık kuyruğa girerken
    puanlanan metnin parmak izini taşıyor. Korpus o günden sonra değiştiyse
    sonuç BAŞKA bir metne aittir ⇒ alınmaz. (Bu delik gerçekten açıldı:
    `v5-parti8 #45`'in metni yargılandıktan sonra bir kez daha düzeltildi.)
    ⚠️ Parmak izi olmayan ESKİ iş dizinleri denetlenemez; rapora yazılır.
    """
    islenen = set()
    for k in json.loads((dizin / "kimlikler.json").read_text(encoding="utf-8")):
        yol = dizin / "sonuc" / f"{k['no']}.json"
        if not yol.exists():
            continue
        if k.get("metin_sha") and k["id"] in kayitlar:
            if _sha(kayitlar[k["id"]]) != k["metin_sha"]:
                if bayat is not None:
                    bayat.append({"kaynak": dizin.name, "no": k["no"], "id": k["id"][:16],
                                  "parti_sira": kayitlar[k["id"]]["gen_meta"]["parti_sira"]})
                continue
        try:
            ham = yol.read_text(encoding="utf-8").strip()
            if ham.startswith("```"):
                ham = ham.split("```")[1].removeprefix("json").strip()
            j = BL.turet(json.loads(ham), f.kaynak_metinleri(kayitlar[k["id"]]))
            if j.get("alinti_dogrulanmadi"):
                dogrulanmadi.append({"kaynak": dizin.name, "no": k["no"],
                                     "id": k["id"][:16], "alanlar": j["alinti_dogrulanmadi"]})
            sonuc[k["id"]] = j
            islenen.add(k["id"])
        except Exception as e:
            bozuk.append({"kaynak": dizin.name, "no": k["no"],
                          "hata": f"{type(e).__name__}: {e}"[:160]})
    return islenen


def main() -> int:
    kayitlar = {r["id"]: r for r in
                (json.loads(s) for s in KORPUS.read_text(encoding="utf-8").splitlines() if s.strip())}
    taban_kayitlar = {r["id"]: r for r in
                      (json.loads(s) for s in TABAN_KORPUS.read_text(encoding="utf-8").splitlines() if s.strip())}

    sonuc: dict[str, dict] = {}
    bozuk: list = []
    dogrulanmadi: list = []

    # 1) Revizyon koşuları önce: bunların metni YENİ korpusla aynı.
    revize = set()
    bayat: list = []
    denetlenemeyen = [d.name for d in REV
                      if not any("metin_sha" in x for x in
                                 json.loads((d / "kimlikler.json").read_text(encoding="utf-8")))]
    for d in REV:
        revize |= _oku(d, kayitlar, sonuc, bozuk, dogrulanmadi, bayat)

    # 2) Taban koşusu: yalnız metni DEĞİŞMEMİŞ kayıtlar devralabilir.
    reddedilen: list = []
    taban_aday: dict = {}
    if TABAN_DOSYA:
        # ⭐ Yargı zaten dosyada; yeniden türetilmez (türetme onu BOZABİLİR:
        # `f_bolumu_turet` kaynak metin ister ve o metin artık değişmiş olabilir).
        taban_aday = {r["id"]: r["judge"] for r in taban_kayitlar.values() if r.get("judge")}
    else:
        _oku(TABAN, taban_kayitlar, taban_aday, bozuk, dogrulanmadi)
    for kid, j in taban_aday.items():
        if kid in sonuc:
            continue                                   # revizyon kazanır
        yeni, eski = kayitlar.get(kid), taban_kayitlar.get(kid)
        if yeni is None:
            continue
        if _puanlanan(yeni) != _puanlanan(eski):
            reddedilen.append({"id": kid[:16],
                               "parti_sira": yeni["gen_meta"]["parti_sira"]})
            continue                                   # ⛔ metin değişmiş: devralınmaz
        sonuc[kid] = j

    satirlar = []
    for r in kayitlar.values():
        r["_checks"] = run_checks(r)
        if not r.get("replay"):
            r["judge"] = sonuc.get(r["id"])
        satirlar.append(r)
    CIKTI.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in satirlar),
                     encoding="utf-8")

    eksik = [r["gen_meta"]["parti_sira"] for r in satirlar
             if not r.get("replay") and not r.get("judge")]
    guvenlik = [r["gen_meta"]["parti_sira"] for r in satirlar
                if (r.get("judge") or {}).get("klinik_guvenlik_ihlali")]
    rol = [r["gen_meta"]["parti_sira"] for r in satirlar
           if (r.get("judge") or {}).get("rol_siniri_ihlali")]
    checks_elenen = [r["gen_meta"]["parti_sira"] for r in satirlar if not r["_checks"]["passed"]]
    rev_sira = sorted(r["gen_meta"]["parti_sira"] for r in satirlar if r["id"] in revize)

    rapor = {
        "tarih": "2026-09-17",
        "betik": "scripts/analiz/2026-09-17-judge-revizyon-kaynastir.py",
        "korpus": str(KORPUS.relative_to(KOK)),
        "korpus_sha256_16": hashlib.sha256(KORPUS.read_bytes()).hexdigest()[:16],
        "taban_korpus": str(TABAN_KORPUS.relative_to(KOK)),
        "taban_isi": TABAN.name,
        "taban_bicimi": "yargılanmış dosya" if TABAN_DOSYA else "iş dizini",
        "revizyon_isleri": [d.name for d in REV],
        "rubrik": RUBRIK,
        "rubrik_sha256_16": hashlib.sha256((KOK / f"prompts/{RUBRIK}.md").read_bytes()).hexdigest()[:16],
        "judge_model": BL.JUDGE_ADI,
        "k": 1,
        "kayit": len(satirlar),
        "revizyondan": rev_sira,
        "tabandan_devralinan": len(sonuc) - len(revize),
        "devralma_reddedilen": reddedilen,
        "bayat_revizyon_sonucu": bayat,
        "parmak_izi_olmayan_isler": denetlenemeyen,
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

    print(f"revizyondan {len(revize)} · tabandan {len(sonuc)-len(revize)} · toplam {len(sonuc)}/{len(satirlar)}")
    if reddedilen:
        print(f"  ⛔ DEVRALMA REDDEDİLDİ (metin değişmiş): {[x['parti_sira'] for x in reddedilen]}")
    if bayat:
        print(f"  ⛔ BAYAT REVİZYON SONUCU (yargıdan sonra metin değişti): "
              f"{[x['parti_sira'] for x in bayat]}")
    if denetlenemeyen:
        print(f"  ⚠️ parmak izi olmayan iş (denetlenemedi): {denetlenemeyen}")
    if eksik:
        print(f"  ⛔ EKSİK: {eksik}")
    for b in bozuk:
        print(f"  ⛔ BOZUK {b['kaynak']}/{b['no']}: {b['hata']}")
    print(f"checks elenen: {checks_elenen or 'yok'}")
    print(f"⛔ klinik güvenlik ihlali: {guvenlik or 'yok'}")
    print(f"⚠️ rol sınırı ihlali: {rol or 'yok'}")
    print(f"⚠️ alıntı doğrulanmadı: {len(dogrulanmadi)} kayıt")
    print(f"→ {CIKTI.relative_to(KOK)} · {RAPOR.relative_to(KOK)}")
    return 1 if (eksik or bozuk or reddedilen or bayat) else 0


if __name__ == "__main__":
    raise SystemExit(main())
