#!/usr/bin/env python3
"""`yansitma.py`'nin iki kuralını YARGIÇ ETİKETİNE karşı ölçer.

⛔⛔ **Neden ölçülüyor.** T265'te eksik kapıyı buldum; kapıyı yazmak
kolay, **işe yaradığını söylemek** ölçüm ister. Bu proje kapıyı ölçmeden
kurmuyor (T237) ve gevşetme kararını sayıya bağlıyor (K40).

**Altın etiket:** yargıcın `ayrinti_konusmada_var == False` alanı —
*«cevaptaki en somut ayrıntının konuşmada karşılığı yok»*.

⛔⛔ **Altın etiket ALTIN DEĞİL, bir yargıcın kanısıdır:** tek yargıç
ailesi (Claude + bir bölümü Gemini), ikinci anotatör yok, ve etiket
**tek ayrıntı** sondasıdır (`en_somut_ayrinti`) ⇒ kayıtta başka bir
uydurma varsa etiket onu görmez. Dolayısıyla burada ölçülen «duyarlılık»
kapının gerçek duyarlılığı değil, **yargıcın işaretlediği ayrıntıyı
yakalama oranıdır**.

⚠️ Kayıt kümesi `data/judged/*.jsonl` içindeki **tekil** kayıtlardır;
aynı kayıt birden çok sürüm anlık görüntüsünde geçtiği için ilk görülen
alınır (hepsi aynı yargıyı taşır).

Çıktı: reports/analiz/2026-09-22-yansitma-kalibrasyon.md
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from kunye import betik_tarihi  # noqa: E402
from yansitma import alinti_ihlalleri, yansitma_yeni  # noqa: E402

RAPOR = KOK / "reports/analiz/2026-09-22-yansitma-kalibrasyon.md"


def dortlu(kayit, kapi):
    """(dogru_pozitif, yanlis_pozitif, yanlis_negatif, dogru_negatif)"""
    dp = yp = yn = dn = 0
    for r in kayit:
        gercek = r["judge"]["ayrinti_konusmada_var"] is False
        tahmin = kapi(r)
        dp += gercek and tahmin
        yp += (not gercek) and tahmin
        yn += gercek and (not tahmin)
        dn += (not gercek) and (not tahmin)
    return dp, yp, yn, dn


def olcu(dp, yp, yn, dn):
    kesinlik = dp / (dp + yp) if dp + yp else 0.0
    duyar = dp / (dp + yn) if dp + yn else 0.0
    f1 = 2 * kesinlik * duyar / (kesinlik + duyar) if kesinlik + duyar else 0.0
    return round(100 * kesinlik), round(100 * duyar), round(100 * f1)


def main() -> int:
    tek = {}
    for f in sorted(glob.glob(str(KOK / "data/judged/*.jsonl"))):
        for l in open(f):
            r = json.loads(l)
            j = r.get("judge")
            if not j or not j.get("en_somut_ayrinti"):
                continue
            if "ayrinti_konusmada_var" not in j:
                continue
            tek.setdefault(r["id"], r)
    kayit = list(tek.values())
    poz = sum(1 for r in kayit if r["judge"]["ayrinti_konusmada_var"] is False)

    kurallar = {
        "A — alıntı (kapı adayı)": lambda r: bool(alinti_ihlalleri(r)),
        "B — yansıtma, ≥1 yeni kök": lambda r: bool(yansitma_yeni(r)),
        "B′ — yansıtma, ≥2 yeni kök": lambda r: any(
            len(y) >= 2 for _, y in yansitma_yeni(r)),
        "B″ — yansıtma, ≥3 yeni kök": lambda r: any(
            len(y) >= 3 for _, y in yansitma_yeni(r)),
        "A ∪ B″": lambda r: bool(alinti_ihlalleri(r)) or any(
            len(y) >= 3 for _, y in yansitma_yeni(r)),
    }
    sonuc = {}
    for ad, k in kurallar.items():
        dp, yp, yn, dn = dortlu(kayit, k)
        sonuc[ad] = (dp, yp, yn, dn) + olcu(dp, yp, yn, dn)

    s = [f"# `yansitma` kurallarının kalibrasyonu — {len(kayit)} etiketli kayıt",
         "",
         f"**Betik:** `{Path(__file__).relative_to(KOK)}` · "
         f"**Tarih:** {betik_tarihi(__file__)}  ",
         f"**Girdi:** `data/judged/*.jsonl` tekilleştirilmiş  ",
         f"**Altın etiket:** yargıcın `ayrinti_konusmada_var == False`  ",
         f"**Pozitif:** {poz}/{len(kayit)} (%{round(100*poz/len(kayit))})  ", "",
         "⛔⛔ **Altın etiket altın değil** — bir yargıcın kanısı, tek "
         "anotatör, ve **tek ayrıntı** sondası. Aşağıdaki «duyarlılık», "
         "kapının gerçek duyarlılığı değil **yargıcın işaretlediği ayrıntıyı "
         "yakalama oranıdır**.", "",
         "## Sonuç", "",
         "| kural | DP | YP | YN | kesinlik | duyarlılık | F1 |",
         "|---|---:|---:|---:|---:|---:|---:|"]
    for ad, (dp, yp, yn, dn, ke, du, f1) in sonuc.items():
        s.append(f"| {ad} | {dp} | {yp} | {yn} | %{ke} | %{du} | {f1} |")

    a = sonuc["A — alıntı (kapı adayı)"]
    s += ["", "## Hüküm", ""]
    if a[4] >= 80:
        s += [f"⭐ **A kuralı KAPI olabilir:** kesinlik %{a[4]} "
              f"({a[0]} doğru / {a[1]} yanlış pozitif). Alıntıyla atıf en sert "
              "iddiadır ve parafraz riski taşımaz.", ""]
    else:
        s += [f"⛔ **A kuralı kapı olamaz:** kesinlik %{a[4]} — "
              f"{a[1]} yanlış pozitif. Rapora indirilmeli (K40 emsali).", ""]
    b = sonuc["B — yansıtma, ≥1 yeni kök"]
    s += [f"⛔ **B kuralı RAPOR kalır:** kesinlik %{b[4]}, {b[1]} yanlış "
          "pozitif. Parafrazı yeniden ifade olarak tanıyamıyor — "
          "*«içmeye başlamışsın»* ile *«alıyorum»* aynı şeydir ama kök "
          "eşlemesi bunu göremez.", "",
          "⭐ Eşik yükseltmek kesinliği artırıyor ama duyarlılığı düşürüyor; "
          "tablodaki B/B′/B″ satırları bu takası gösteriyor.", "",
          "## ⛔ Bunun söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔⛔ **Duyarlılık yanıltıcı** | altın etiket tek ayrıntıya "
          "bakıyor; kapı başka bir uydurmayı yakalarsa **yanlış pozitif** "
          "sayılıyor ⇒ gerçek kesinlik ölçülenden **yüksek** olabilir |",
          "| ⛔ **Kök eşleme 5 harf** | Türkçe ek sorununun kaba çözümü; "
          "`güven`/`güvenlik` ayrımı yapılamaz |",
          "| ⛔ **Durak listesi elle** | listeye eklenen her sözcük ölçümü "
          "daraltır; liste `src/yansitma.py` içinde açık yazılı |",
          "| ⛔ **Tek yargıç ailesi** | etiketlerin bir bölümü Gemini'den, "
          "çoğu Claude'dan; K97 gereği iki yargıcın notu aynı tabloda "
          "birleştirilmedi ama **etiket olarak** birlikte kullanıldı — bu "
          "bir gevşemedir ve burada yazılıdır |"]

    RAPOR.write_text("\n".join(s) + "\n", encoding="utf-8")
    assert RAPOR.exists()
    for ad, v in sonuc.items():
        print(f"  {ad:28} DP={v[0]:3} YP={v[1]:4} YN={v[2]:3} "
              f"kesinlik %{v[4]:3} duyarlılık %{v[5]:3} F1 {v[6]}")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
