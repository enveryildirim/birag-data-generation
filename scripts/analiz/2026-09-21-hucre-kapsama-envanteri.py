#!/usr/bin/env python3
"""Hücre düzeyi kapsama — marjinaller kapandı, birlikte dağılım hiç bakılmadı.

⛔⛔⛔ **BU BİR AÇIK KALEMİN KAPATILMASI, BENİM FİKRİM DEĞİL.** Kapsama
envanterinin kendi şerhi şunu diyor: *«Eksenler bağımsız sayıldı; birlikte
dağılım (hücre düzeyi) bakılmadı; T94 tam bunun bedelini ölçmüştü ⇒ parti
planı ızgarayı kısıtla kurmalı, marjinalleri ayrı ayrı değil.»* Beş parti
sonra marjinal açıkların tamamı 3 puanın altına indi (en büyüğü +2,7) ⇒
marjinal ölçüt artık hiçbir şey söylemiyor ve hedef üretmiyor.

⭐ **Ölçü DEĞİŞMİYOR, ölçülen BİRİM değişiyor** (K97). Aynı fark tanımı —
`havuz% − set%` — tek eksen değerine değil, iki eksenin KESİŞİMİNE
uygulanıyor. Ufuk kuralı (T211) da olduğu gibi kalıyor.

⛔ **ASGARİ HAVUZ SAYISI bir SEÇİMDİR.** Seyrek hücrelerde yüzde farkı
gürültüdür: havuzda 3 tohumu olan bir hücre tek kayıtla %100 oynar. Eşik
`--asgari` ile verilir, varsayılan **20 tohum** (havuzun ~%1,5'i) — bu
benim önerim, türetilmedi.

⛔ Izgaranın kendi yönettiği eksenler (`bagimlilik_turu`, `yas_grubu`)
hücre çiftlerinde de DIŞARIDA: onları tohum seçimi değil plan belirliyor.

Çıktı: reports/analiz/2026-09-21-hucre-kapsama-envanteri[-EK].{md,json}
Kullanım: uv run python scripts/analiz/2026-09-21-hucre-kapsama-envanteri.py \
          [--ek=parti1-5] [--asgari=20] [--ust=40]
"""
from __future__ import annotations

import collections
import itertools
import json
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
_EK = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--ek=")), "")
_AD = f"{TARIH}-hucre-kapsama-envanteri" + (f"-{_EK}" if _EK else "")
ASGARI = int(next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--asgari=")), "20"))
UST = int(next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--ust=")), "40"))
RAPOR = KOK / f"reports/analiz/{_AD}.md"
JSON = KOK / f"reports/analiz/{_AD}.json"

# ⛔ Envanterin eksen listesiyle AYNI olmalı; ayrılırsa iki tanım olur (K97).
_SP = _iu.spec_from_file_location(
    "env", KOK / "scripts/analiz/2026-09-20-kapsama-acigi-envanteri.py")
ENV = _iu.module_from_spec(_SP)
_SP.loader.exec_module(ENV)
IZGARA_EKSENI = ("bagimlilik_turu", "yas_grubu")
EKSEN = [e for e in ENV.EKSEN if e not in IZGARA_EKSENI]


def main() -> int:
    tohum = [json.loads(l) for l in
             (KOK / "data/seeds.v2.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    kullanilan = ENV._iu and None  # yer tutucu değil: aşağıda planlayıcıdan alınıyor
    sp = _iu.spec_from_file_location(
        "p1", KOK / "scripts/analiz/2026-09-15-v4-parti1-plan.py")
    p1 = _iu.module_from_spec(sp)
    sp.loader.exec_module(p1)
    # ⭐ «Kullanılmış» kümesi dışarıdan verilebilir (`--kullanilmis=<json>`):
    # T211'in hedefleri onarım ÖNCESİ ve SONRASI zeminlerde karşılaştırılabilsin
    # diye. ⛔ Ölçünün tanımı değişmiyor, yalnız girdisi (K97).
    _kj = next((a.split("=", 1)[1] for a in sys.argv
                if a.startswith("--kullanilmis=")), None)
    kullanilan = p1.kullanilmis()
    if _kj:
        kullanilan = set(json.loads(Path(_kj).read_text(encoding="utf-8")))
        print(f"⚠️ kullanılmış kümesi dışarıdan: {_kj} ({len(kullanilan)})")
    U = [t for t in tohum if t["source_id"] in kullanilan]

    hucre: dict[str, dict] = {}
    for e1, e2 in itertools.combinations(EKSEN, 2):
        ch = collections.Counter((t["meta"].get(e1), t["meta"].get(e2)) for t in tohum)
        cu = collections.Counter((t["meta"].get(e1), t["meta"].get(e2)) for t in U)
        for (v1, v2), n in ch.items():
            if n < ASGARI or v1 is None or v2 is None:
                continue
            ph = 100 * n / len(tohum)
            pu = 100 * cu.get((v1, v2), 0) / len(U)
            hucre[f"{e1}={v1}&{e2}={v2}"] = {
                "sette": round(pu, 2), "havuz": round(ph, 2),
                "fark": round(ph - pu, 2), "havuz_tohum": n,
                "set_tohum": cu.get((v1, v2), 0)}

    sirali = sorted(hucre.items(), key=lambda x: -abs(x[1]["fark"]))
    JSON.write_text(json.dumps(
        {"tarih": TARIH, "havuz": len(tohum), "uretilmis": len(U), "asgari": ASGARI,
         "hucre_sayisi": len(hucre), "acik": hucre}, ensure_ascii=False, indent=1),
        encoding="utf-8")

    art = [k for k, v in hucre.items() if v["fark"] >= 3.0]
    eks = [k for k, v in hucre.items() if v["fark"] <= -3.0]
    sat = [f"# Hücre düzeyi kapsama — marjinaller kapandıktan sonra", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Havuz:** **{len(tohum)}** tohum · üretilmiş **{len(U)}** · "
           f"asgari havuz sayısı **{ASGARI}**  ",
           f"**Bakılan hücre:** {len(hucre)} (eksen çifti: "
           f"{len(list(itertools.combinations(EKSEN, 2)))})", "",
           "⛔⛔ **Marjinal ölçüt tükendi.** Beş parti sonra tek eksen değerlerinin "
           "hiçbirinde |fark| ≥ 3 yok (en büyüğü +2,7) ⇒ ufuk kuralı hedef "
           "üretmiyor. Bu rapor, envanterin kendi son şerhini uyguluyor: "
           "*«eksenler bağımsız sayıldı; birlikte dağılım bakılmadı»*.", "",
           "⭐ Ölçü aynı (`havuz% − set%`), birim farklı: tek değer yerine iki "
           "eksenin kesişimi. Ufuk kuralı (T211) değişmiyor.", "",
           f"## 1. Eşiği aşan hücreler — eksik **{len(art)}**, fazla **{len(eks)}**", "",
           "| hücre | sette | havuz | fark | havuz tohum | set tohum |",
           "|---|---:|---:|---:|---:|---:|"]
    for k, v in sirali[:UST]:
        sat.append(f"| `{k}` | %{v['sette']} | %{v['havuz']} | {v['fark']:+.2f} | "
                   f"{v['havuz_tohum']} | {v['set_tohum']} |")
    sat += ["", "## ⛔ Bu envanterin söylemedikleri", "", "| | |", "|---|---|",
            f"| ⛔⛔ **Asgari {ASGARI} tohum SEÇİMDİR** | türetilmedi; altındaki "
            "hücrelerde yüzde farkı gürültüdür ama eşiğin nerede olduğu ölçülmedi |",
            "| ⛔⛔ **İkili bakıldı, üçlü bakılmadı** | aynı itiraz bir üst düzeyde "
            "aynen geçerli; nerede duracağı bir seçim ve burada ikide durdu |",
            "| ⛔⛔ **Hücre hedeflemek marjinali BOZABİLİR** | bir hücreyi doldurmak "
            "iki marjinali birden oynatır; planın bunu ölçmesi gerekir |",
            "| ⛔⛔ **Kapsama ≠ kalite** | envanterin şerhi burada da geçerli; "
            "hücre payını havuza eşitlemek o hücrede iyi kayıt üretileceğini "
            "göstermez |",
            "| ⛔ **Havuzun kendisi bir tasarım ürünü** | *«set havuzu yansıtmalı»* "
            "varsayımı hücre düzeyinde de kanıtlanmadı |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[:12 + min(UST, len(sirali))]))
    print(f"\n→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
