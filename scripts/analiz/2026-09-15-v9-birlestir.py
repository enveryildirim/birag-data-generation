#!/usr/bin/env python3
"""v9 judge sonuçlarını toplar, KAYNAKLI türetir ve v8 ile eşleştirir.

⭐ v8'den tek yapısal fark: türetme `kaynak` ile çağrılır. v9'un doğrulama kapısı
kaynak metin olmadan **sessizce kapalı** çalışır (`alinti_dogrulama: kaynaksiz`);
bu betik kaynağı kurar ve her kayda doğrulamanın YAPILDIĞINI yazar.

Türetme `filter.py`'den İMPORT EDİLİR, kopyalanmaz — kopyalasaydım v8↔v9 farkı
rubrik farkı değil **hesap farkı** olurdu.

Çıktı:
  reports/analiz/eksen2-judge-v9/<kol>/sonuclar.jsonl
  reports/analiz/eksen2-judge-v9/ayrisma-kumesi.json    — --hakemlik ile

Kullanım:
  uv run python scripts/analiz/2026-09-15-v9-birlestir.py
  uv run python scripts/analiz/2026-09-15-v9-birlestir.py --hakemlik
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import filter as f  # noqa: E402
from schemas import JudgeResult  # noqa: E402

_sp = _iu.spec_from_file_location("plan9", KOK / "scripts/analiz/2026-09-15-v9-kosu-plan.py")
PLAN = _iu.module_from_spec(_sp)
_sp.loader.exec_module(PLAN)

ISLER = PLAN.ISLER
KOSU = KOK / "reports/analiz/eksen-kosu"
V8 = KOK / "reports/analiz/eksen2-judge-v8"
HEDEF = KOK / "reports/analiz/eksen2-judge-v9"
SET1 = KOK / "evals/safety_crisis.jsonl"
IKINCI = KOK / "reports/analiz/ikinci-set"

JUDGE_ADI = "claude-sonnet-subagent"
RUBRIK = "judge-eksen1.v9"
ALANLAR = ["rol_siniri_ihlali", "bos_guvence", "tuzak_suclama"]

HARITA = {
    "e2-5ae67873": ("taban",    "20260915-105829-safety_crisis-baseline-1"),
    "e2-b7584bec": ("A-dar",    "20260915-140907-sc2-A-dar"),
    "e2-220c3b5a": ("B-derin",  "20260915-141354-sc2-B-derin"),
    "e2-99b69ab4": ("C-dikkat", "20260915-141743-sc2-C-dikkat"),
    "e2-7ac7e984": ("D-tam",    "20260915-142010-sc2-D-tam"),
    "e2-ceef5655": ("E-genis",  "20260915-142308-sc2-E-genis"),
}
# v9'un ALAN listesi — Ö6 (doluluk) bunları sayıyor. v8'in dördü KALKTI.
V9_ALAN = ["teselli_islevi", "teselli_dayanak_alintisi", "rol_risk_olasilik_olarak",
           "rol_kaynak_turu", "kurum_yordam_en_yakin", "kurum_adi", "yordam_iddiasi",
           "yordam_baglamdan", "yordam_baglam_alintisi"]
# v9'da judge'ın YAZMAMASI gereken, v8'den kalkan alanlar (Ö6 — talimata uyum).
KALKAN = ["teselli_ozgu_oge", "teselli_kalip", "teselli_kullanici_alintisi",
          "kurum_adi_kullanicidan"]


def kaynak_kur(oge: dict, cevap: str, thinking: str) -> dict:
    """Doğrulamanın bakacağı metinler — eval öğesi + kayıtlı cevap."""
    rec = {"messages": list(oge["messages"]) +
           [{"role": "assistant", "content": cevap, "thinking": thinking or ""}],
           "context": oge.get("context")}
    return f.kaynak_metinleri(rec)


def turet(data: dict, kaynak: dict) -> dict:
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


def oku(dizin: Path, kaynaklar: dict) -> tuple[dict, list, list, dict, dict]:
    kimlikler = json.loads((dizin / "kimlikler.json").read_text())
    sonuc, eksik, bozuk, ham_alan, fazla = {}, [], [], {}, {}
    for k in kimlikler:
        yol = dizin / "sonuc" / f"{k['no']}.json"
        if not yol.exists():
            eksik.append(k["no"]); continue
        try:
            ham = yol.read_text().strip()
            if ham.startswith("```"):
                ham = ham.split("```")[1].removeprefix("json").strip()
            d = json.loads(ham)
            ham_alan[k["id"]] = {a: (a in d) for a in V9_ALAN}
            fazla[k["id"]] = [a for a in KALKAN if a in d]
            sonuc[k["id"]] = turet(d, kaynaklar[k["id"]])
        except Exception as e:
            bozuk.append((k["no"], f"{type(e).__name__}: {e}"[:120]))
    return sonuc, eksik, bozuk, ham_alan, fazla


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hakemlik", action="store_true")
    a = ap.parse_args()

    ogeler = {o["id"]: o for o in (json.loads(l) for l in open(SET1) if l.strip())}
    beklenen = {oid: [i["alan"] for i in o["iddialar"] if i.get("tip") == "judge"]
                for oid, o in ogeler.items()}

    HEDEF.mkdir(parents=True, exist_ok=True)
    ozet, ayrisan, tum, kimlik_kol = [], [], {}, {}
    for etiket, (kol, dizin) in HARITA.items():
        kosu = {r["id"]: r for r in
                (json.loads(l) for l in open(KOSU / dizin / "sonuclar.jsonl"))}
        kaynaklar = {oid: kaynak_kur(ogeler[oid], r["cevap"], r.get("thinking"))
                     for oid, r in kosu.items()}
        judge, eksik, bozuk, ham_alan, fazla = oku(ISLER / f"v9-{etiket}", kaynaklar)
        # ⚠️ Kontrol kümesinin ÇEKİLDİĞİ nüfus, tasarım belgesindekiyle BİREBİR aynı
        # olmalı: iş dizininin `kimlikler.json`'u (114 öğe). Koşu dizini 120 kayıt
        # taşıyor (6'sı boş cevap, iş dosyası kurulmadı); oradan çekmek tohumu aynı
        # tutsa bile BAŞKA bir örneklem verir ve ön kayıt anlamını yitirirdi.
        kimlik_kol[kol] = [k["id"] for k in json.loads(
            (ISLER / f"v9-{etiket}" / "kimlikler.json").read_text())]
        v8 = {json.loads(l)["id"]: json.loads(l)
              for l in open(V8 / kol / "sonuclar.jsonl")}
        oto2 = {r["kaynak_oge"]: r for r in
                (json.loads(l) for l in open(IKINCI / dizin / "sonuclar.jsonl"))}
        satirlar = []
        for oid, r in kosu.items():
            j = judge.get(oid)
            v8s = v8[oid]
            s = {"id": oid, "kutup": r.get("kutup"), "dilim": r.get("dilim"),
                 "cevap": r["cevap"], "judge_alanlari": beklenen[oid],
                 "otomatik_gecti_set1": r["otomatik_gecti"],
                 "otomatik_gecti_set2": oto2[oid]["otomatik_gecti"],
                 "judge_v9": j,
                 "v9_alan_dolu": ham_alan.get(oid),
                 "v9_fazla_alan": fazla.get(oid),
                 "v8_dusuren": v8s["v8_dusuren"],
                 "v8_gecti": v8s["v8_gecti"],
                 "v8_kurum_yordam_ihlali": v8s.get("kurum_yordam_ihlali")}
            if j is None:
                s["v9_dusuren"] = []
                s["v9_gecti"] = None if r["cevap"].strip() else False
                s["izler"] = None
            else:
                dus = [al for al in beklenen[oid] if j.get(al) is True]
                s["v9_dusuren"] = dus
                s["v9_gecti"] = not dus
                s["kurum_yordam_ihlali"] = j.get("kurum_yordam_ihlali")
                # ⭐ v9'un makine-okunur izleri (Ö2 atıf ölçümü bunları kullanır)
                dogrulanmadi = j.get("alinti_dogrulanmadi") or []
                s["izler"] = {
                    "alinti_dogrulama": j.get("alinti_dogrulama"),
                    "alinti_dogrulanmadi": dogrulanmadi,
                    "kapsam_disi": [x for x in dogrulanmadi if x.endswith(":ic_muhakeme")],
                    "bulunamadi": [x for x in dogrulanmadi if x.endswith(":bulunamadi")],
                    "teselli_dayanak_dogrulandi": j.get("teselli_dayanak_dogrulandi"),
                    "teselli_dayanak_alintisi": j.get("teselli_dayanak_alintisi"),
                    "v8_teselli_kalip": v8s.get("judge_v8", {}).get("teselli_kalip"),
                    "v8_teselli_ozgu_oge": v8s.get("judge_v8", {}).get("teselli_ozgu_oge"),
                }
            s["ayrisma"] = (j is not None
                            and set(s["v8_dusuren"]) != set(s["v9_dusuren"]))
            if s["ayrisma"]:
                ayrisan.append({"kol": kol, "id": oid, "rol": "ayrisan",
                                "v8": sorted(s["v8_dusuren"]),
                                "v9": sorted(s["v9_dusuren"])})
            satirlar.append(s)
        tum[kol] = {s["id"]: s for s in satirlar}
        d = HEDEF / kol
        d.mkdir(parents=True, exist_ok=True)
        (d / "sonuclar.jsonl").write_text(
            "".join(json.dumps(s, ensure_ascii=False) + "\n" for s in satirlar))
        (d / "kosu.json").write_text(json.dumps(
            {"kol": kol, "kaynak_kosu": dizin, "kor_etiket": f"v9-{etiket}",
             "judge_model": JUDGE_ADI, "judge_rubrik": RUBRIK, "k": 1,
             "judge_toplandi": len(judge), "eksik": eksik, "bozuk": bozuk,
             "dogrulama": "kaynakli",
             "karsilastirma": "reports/analiz/eksen2-judge-v8 (v8, aşama 1, k=1)",
             "tarih": datetime.now().isoformat(timespec="seconds")},
            ensure_ascii=False, indent=1))
        ozet.append((kol, len(judge), len(eksik), len(bozuk),
                     sum(1 for v in fazla.values() if v)))

    print(f"{'kol':10} {'toplandı':>8} {'eksik':>6} {'bozuk':>6} {'kalkan alan yazan':>18}")
    for kol, n, e, b, fz in ozet:
        print(f"{kol:10} {n:>8} {e:>6} {b:>6} {fz:>18}")
    print(f"\nv8 ile AYRIŞAN öğe: {len(ayrisan)}")

    if a.hakemlik:
        # ⭐ Ö3 — kontrol kümesi TOHUMLA çekildi, ayrışmadan BAĞIMSIZ (tasarımda yazılı).
        kontrol = PLAN.kontrol_kumesi(kimlik_kol)
        kume, secilen = [], set()
        for x in ayrisan:
            kume.append(x); secilen.add((x["kol"], x["id"]))
        kesisim = 0
        for kol, oid in kontrol:
            s = tum[kol].get(oid)
            if s is None or s["judge_v9"] is None:
                continue
            if (kol, oid) in secilen:
                kesisim += 1
                for x in kume:
                    if x["kol"] == kol and x["id"] == oid:
                        x["rol"] = "ayrisan+kontrol"
                continue
            kume.append({"kol": kol, "id": oid, "rol": "kontrol",
                         "v8": sorted(s["v8_dusuren"]), "v9": sorted(s["v9_dusuren"])})
            secilen.add((kol, oid))
        (HEDEF / "ayrisma-kumesi.json").write_text(
            json.dumps(kume, ensure_ascii=False, indent=1))
        n_a = sum(1 for x in kume if x["rol"].startswith("ayrisan"))
        n_k = sum(1 for x in kume if "kontrol" in x["rol"])
        print(f"hakemlik kümesi: {n_a} ayrışan + {n_k} kontrol "
              f"(kesişim {kesisim}) = {len(kume)} öğe "
              f"→ {(HEDEF / 'ayrisma-kumesi.json').relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
