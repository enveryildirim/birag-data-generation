#!/usr/bin/env python3
"""v5-parti4..8 judge sonuçlarını partiler arası karşılaştırır.

⛔⛔ **K97 UYARISI KAPSAM İÇİNDE.** Bu tablo yalnız **aynı rubrik (v9), aynı
judge kurulumu ve aynı koşu** içinde üretilmiş beş partiyi karşılaştırır.
`2026-09-15-korpus-v9-kosusu` ya da `v0.0.x` sayıları bu tabloya **girmez**:
farklı koşu, farklı korpus. ⚠️ Judge Claude ailesinden (K43/K45) ⇒ bu sayılar
**metrik değil**, veri revizyonu sinyalidir.

⭐ Amaç: tek bir partinin bulgusunun mu, yoksa korpus boyunca süren bir
EĞİLİMİN mi söz konusu olduğunu ayırmak.
"""
from __future__ import annotations
import json, statistics as st, sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
SAYISAL = ["anlasilirlik_holistik", "dogallik_holistik", "mi_uyumu_holistik",
           "duygusal_tepki", "yorumlama", "kesif",
           "anlasilirlik", "dogallik", "mi_uyumu", "grounding"]
BAYRAK = ["belirsiz_gonderge", "ust_uste_yan_cumle", "kurulmamis_mecaz", "soyut_adlastirma",
          "siz_kaymasi", "klise_acilis", "terapi_jargonu", "ovgu_tonu",
          "tuzak_uzman", "tuzak_soru_cevap", "tuzak_erken_odak", "tuzak_erken_tavsiye",
          "kusur_kullanicida_ima", "utanc_buyutuyor",
          "yansitma_var", "karmasik_yansitma", "takdir_var", "ozet_var", "ozerklik_vurgusu"]


def yukle(yol: Path) -> list[dict]:
    return [x["judge"] for x in
            (json.loads(s) for s in yol.read_text(encoding="utf-8").splitlines() if s.strip())
            if x.get("judge")]


def main(yollar: list[str]) -> int:
    if not yollar:
        yollar = sorted(glob_ := [str(p) for p in (KOK / "data/judged").glob("v5-parti*.arinmis.v9.jsonl")])
    veri = {Path(y).name.split(".")[0]: yukle(Path(y) if Path(y).is_absolute() else KOK / y)
            for y in yollar}
    ad = list(veri)
    print(f"{'ölçüm':<26}" + "".join(f"{a.replace('v5-',''):>10}" for a in ad))
    print("─" * (26 + 10 * len(ad)))
    for k in SAYISAL:
        sat = []
        for a in ad:
            v = [x[k] for x in veri[a] if isinstance(x.get(k), (int, float))]
            sat.append(f"{st.mean(v):>10.2f}" if v else f"{'—':>10}")
        print(f"{k:<26}" + "".join(sat))
    print()
    print(f"{'bayrak (true sayısı)':<26}" + "".join(f"{a.replace('v5-',''):>10}" for a in ad))
    print("─" * (26 + 10 * len(ad)))
    for k in BAYRAK:
        sat = [f"{sum(1 for x in veri[a] if x.get(k) is True):>10}" for a in ad]
        if any(int(x) for x in sat):
            print(f"{k:<26}" + "".join(sat))
    print()
    print(f"{'F-bayrakları':<26}" + "".join(f"{a.replace('v5-',''):>10}" for a in ad))
    print("─" * (26 + 10 * len(ad)))
    for etiket, f in (("ayrinti_konusmada_var=F", lambda x: x.get("ayrinti_konusmada_var") is False),
                      ("teselli_dayanak=YOK",     lambda x: x.get("teselli_dayanak_alintisi") == "YOK"
                                                            and x.get("teselli_islevi") == "rahatlatma"),
                      ("guvenlik_tipi != yok",    lambda x: x.get("guvenlik_tipi") not in (None, "yok")),
                      ("rol_alani != yok",        lambda x: x.get("rol_alani") not in (None, "yok")),
                      ("yordam_baglamdan=F",      lambda x: x.get("yordam_iddiasi") not in (None, "YOK", "")
                                                            and x.get("yordam_baglamdan") is False)):
        print(f"{etiket:<26}" + "".join(f"{sum(1 for x in veri[a] if f(x)):>10}" for a in ad))
    print()
    print(f"{'kayıt':<26}" + "".join(f"{len(veri[a]):>10}" for a in ad))
    return 0


if __name__ == "__main__":
    import glob
    raise SystemExit(main(sys.argv[1:]))
