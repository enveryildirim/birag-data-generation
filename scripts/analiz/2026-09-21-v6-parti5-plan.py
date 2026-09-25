#!/usr/bin/env python3
"""v6-parti5 tasarım ızgarası — 60 kayıt. Üretimden ÖNCE yazılır, dondurulur.

⛔⛔⛔ **HEDEF TÜRETMESİ TEK BİR KURALA İNDİRİLDİ — VE SEBEBİ BİR ÖLÇÜM.**
Parti4'ün kaçınması *«kota = havuz payı»* idi ve parti içinde tuttu; ama
korpusu **parti başına 0.2-0.4 puan** oynattı. Ölçüldü: mevcut açıkların
kapanması **13-17 parti** sürerdi — yaklaşık 800 kayıt, yani hiç.
➡️⭐⭐⭐ *Bir düzeltme kuralı doğru YÖNDE olabilir ve yine de pratikte atıl
olabilir; yönü ölçmek yetmez, HIZINI da ölçmek gerekir.*

⭐ **Ufuk kuralı.** Bir sınıfın bu partideki payı, korpus açığını **K
partide** kapatacak pay olsun:

    q = (p_havuz × (N₀ + n·K) − p_set × N₀) / (n·K),   [0,1] arasına kırpılır

Bu **tek kural iki yönü de** kapsar: `q > p_set` ise sınıf hedeflenir
(ödül), `q < p_set` ise kota olur (aşınca ceza). ⇒ PP2'nin azınlık dalı
(`×2`, tavan %40) ve PP3'ün çoğunluk dalı (parite) ve parti4'ün parite
kotası **SÜPERSEDE**.

⛔ **K = 5 SEÇİMDİR** ama keyfî değil: 5 parti ≈ 300 kayıt ⇒ korpus ~1108,
yani hedeflenen büyüklük. *«Korpus bitene kadar kapansın»* demek oluyor.
⚠️ `profil=mavi_yakali` K=5'te **sıfır payla bile** kapanmıyor (≈8 parti
gerekir); kırpıldı ve rapora yazıldı.

⭐ Bağlam sınıfı (T202), çıplak kriz işareti (T199) ve modül kimliği
`assert`i parti3/parti4'ten **çağrılır**, yeniden tanımlanmaz.

Girdi : reports/analiz/2026-09-20-kapsama-acigi-envanteri-parti1-4-cift-yon.json
Çıktı : data/plan/v6-parti5.jsonl · reports/analiz/2026-09-21-v6-parti5-plan.md
"""
from __future__ import annotations

import json
import os
import random
from collections import Counter
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
N = 60
K_UFUK = 5          # ⛔ SEÇİM — gerekçesi docstring'de
TOHUM = int(os.environ.get("BIRAG_PLAN_TOHUM", "20260924"))
CIKTI = KOK / "data/plan/v6-parti5.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-v6-parti5-plan.md"
CIFT_YON = KOK / "reports/analiz/2026-09-20-kapsama-acigi-envanteri-parti1-4-cift-yon.json"


def _modul(ad: str, yol: str):
    sp = _iu.spec_from_file_location(ad, KOK / yol)
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


# ⛔ Tek nesne grafiği (parti4'ün modül kimliği tuzağı): hepsi PP4'ünkiler.
PP4 = _modul("pp4", "scripts/analiz/2026-09-20-v6-parti4-plan.py")
PP3, PP1, PP2 = PP4.PP3, PP4.PP1, PP4.PP2
KRIZ = PP4.KRIZ
IZGARA_EKSENI = PP4.IZGARA_EKSENI

KACINMA: dict[tuple[str, str], float] = {}
KOTA: dict[tuple[str, str], int] = {}
_ALINMIS: dict[str, dict] = {}


def korpus_boyu() -> int:
    """Derlenmiş set + üretilmiş partiler. ⛔ Ufuk kuralının N₀'ı."""
    n = sum(1 for l in (KOK / "datasets/v0.0.14/train.jsonl").read_text(
        encoding="utf-8").splitlines() if l.strip())
    for f in sorted(KOK.glob("data/candidates/v6-parti?.jsonl")):
        n += sum(1 for l in f.read_text(encoding="utf-8").splitlines() if l.strip())
    return n


def ufuk_paylari() -> tuple[dict, dict, dict, int]:
    """Tek kural, iki yön. Döner: (hedef, kacinma, kota, N₀)."""
    cy = json.loads(CIFT_YON.read_text(encoding="utf-8"))
    n0 = korpus_boyu()
    hedef: dict[tuple[str, str], int] = {}
    kacinma: dict[tuple[str, str], float] = {}
    kota: dict[tuple[str, str], int] = {}
    kirpik: list[str] = []
    for anahtar, v in cy["acik"].items():
        eksen, deger = anahtar.split("=", 1)
        if eksen in IZGARA_EKSENI or abs(v["fark"]) < 3.0:
            continue
        ps, p0 = v["havuz"] / 100, v["sette"] / 100
        q_ham = (ps * (n0 + N * K_UFUK) - p0 * n0) / (N * K_UFUK)
        q = max(0.0, min(1.0, q_ham))
        if not 0.0 <= q_ham <= 1.0:
            kirpik.append(f"{anahtar} (ham q=%{100*q_ham:.1f})")
        pay = round(q * N)
        if v["fark"] > 0:                      # set EKSİK taşıyor → hedefle
            hedef[(eksen, deger)] = pay
        else:                                  # set FAZLA taşıyor → tavan koy
            kota[(eksen, deger)] = pay
            kacinma[(eksen, deger)] = abs(v["fark"]) * N / 100
    ufuk_paylari.kirpik = kirpik               # rapora taşınıyor
    return hedef, kacinma, kota, n0


def _ihtiyac_sirasi(hav: list[dict], kalan: dict) -> list[dict]:
    """PP1'in sıralayıcısı + kota aşımına ceza (parti4'ün biçimi)."""
    kullanim: Counter = Counter()
    for m in _ALINMIS.values():
        for (e, v) in KOTA:
            if str(m.get(e)) == v:
                kullanim[(e, v)] += 1

    def anahtar(t):
        puan = sum(kalan.get((e, v), 0) for (e, v) in PP1.TOHUM_HEDEF
                   if str(t["meta"].get(e)) == v)
        ceza = sum(w for (e, v), w in KACINMA.items()
                   if str(t["meta"].get(e)) == v and kullanim[(e, v)] >= KOTA[(e, v)])
        return (-(puan - ceza), t["seed_id"])
    return sorted(hav, key=anahtar)


def main() -> int:
    global KACINMA, KOTA
    assert PP4.PP3 is PP3 and PP3.PP1 is PP1, "⛔ modül kimliği ayrıştı"
    hedef, KACINMA, KOTA, n0 = ufuk_paylari()
    PP1.TOHUM_HEDEF.clear()
    PP1.TOHUM_HEDEF.update(hedef)
    PP1._ihtiyac_sirasi = _ihtiyac_sirasi
    PP1._TURETILMIS = True
    PP1.CIKTI, PP1.RAPOR, PP1.TOHUM, PP1.N = CIKTI, RAPOR, TOHUM, N
    _orij = PP1.P1.sec

    def _sec(s, h, alinmis):
        t = _orij(s, h, alinmis)
        if t is not None:
            _ALINMIS[t["seed_id"]] = t["meta"]
        return t
    PP1.P1.sec = _sec

    print(f"⭐ korpus N₀={n0} · ufuk K={K_UFUK} parti")
    print(f"⭐ hedef ({len(hedef)}): " +
          ", ".join(f"{e}={d}→{v}" for (e, d), v in sorted(hedef.items(), key=lambda x: -x[1])))
    print(f"⛔ kota ({len(KOTA)}): " +
          ", ".join(f"{e}={d}→{v}" for (e, d), v in sorted(KOTA.items(), key=lambda x: x[1])))
    if (rc := PP1.main()):
        return rc

    satir = [json.loads(l) for l in CIKTI.read_text(encoding="utf-8").splitlines() if l.strip()]
    ctx = [r for r in satir if r["context"]]
    dagitim = PP3.baglam_paylari(len(ctx))
    random.Random(TOHUM).shuffle(dagitim)
    for r, s in zip(sorted(ctx, key=lambda r: r["sira"]), dagitim):
        r["baglam_davranisi"] = s
    tohumlar = KRIZ._tohumlar()
    isaret = sum(1 for r in satir
                 if PP3.ciplak_kriz(tohumlar.get(r["seed_id"], {}))
                 and not r.update({"beyan_ciplak_kriz": True}))
    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in satir),
                     encoding="utf-8")

    cy = json.loads(CIFT_YON.read_text(encoding="utf-8"))
    ek = ["", "## ⛔⛔⛔ Parti4'ten fark — TEK KURAL, İKİ YÖN, VE BİR HIZ ÖLÇÜSÜ", "",
          "Parti4'ün kaçınması *«kota = havuz payı»* idi. Parti içinde tuttu ama "
          f"korpusu **parti başına 0.2-0.4 puan** oynattı: mevcut açıklar bu hızla "
          "**13-17 partide** kapanırdı. ➡️⭐⭐⭐ *Bir düzeltme kuralı doğru YÖNDE "
          "olabilir ve yine de pratikte atıl olabilir; yönü ölçmek yetmez, HIZINI "
          "da ölçmek gerekir.*", "",
          f"⭐ **Ufuk kuralı** (N₀={n0}, n={N}, K={K_UFUK}):", "",
          "```", "q = (p_havuz × (N₀ + n·K) − p_set × N₀) / (n·K)", "```", "",
          "`q > p_set` ise sınıf **hedeflenir**, `q < p_set` ise **tavan** olur. "
          "⇒ PP2'nin azınlık dalı, PP3'ün çoğunluk dalı ve parti4'ün parite kotası "
          "**SÜPERSEDE**; üçünün yerine tek kural.", "",
          "| eksen = değer | set | havuz | fark | **parti5 payı** | ulaşılan |",
          "|---|---:|---:|---:|---:|---:|"]
    for (e, d), pay in sorted({**hedef, **KOTA}.items(),
                              key=lambda x: cy["acik"][f"{x[0][0]}={x[0][1]}"]["fark"]):
        v = cy["acik"][f"{e}={d}"]
        ul = sum(1 for r in satir
                 if str((tohumlar.get(r["seed_id"], {}).get("meta") or {}).get(e)) == d)
        tur = "hedef" if (e, d) in hedef else "tavan"
        ek.append(f"| `{e}={d}` ({tur}) | %{v['sette']} | %{v['havuz']} | "
                  f"{v['fark']:+.1f} | **{pay}** | {ul} |")
    ek += ["", f"⛔ **K={K_UFUK} SEÇİMDİR** ama keyfî değil: {K_UFUK} parti ≈ "
               f"{N*K_UFUK} kayıt ⇒ korpus ~{n0+N*K_UFUK}, yani hedeflenen büyüklük. "
               "*«Korpus bitene kadar kapansın»* demek oluyor.", ""]
    if ufuk_paylari.kirpik:
        ek += [f"⚠️ **Kırpılan sınıf(lar):** {', '.join(ufuk_paylari.kirpik)} — "
               f"ham pay [0,1] dışına düştü, yani bu açık {K_UFUK} partide "
               "kapanamıyor (sıfır payla bile). Kırpıldı ve burada yazılı.", ""]
    ek += ["## ⭐ Bağlam sınıfı — plandan (T202)", "", "| sınıf | parti5 payı |",
           "|---|---:|"]
    for s in ("cevap_var", "cevap_yok", "izin_iste", "ilgisiz"):
        ek.append(f"| `{s}` | {dagitim.count(s)} |")
    ek += ["", f"⭐ Çıplak kriz beyanı işaretli satır: **{isaret}** (`gd-021` açık).", "",
           "## ⛔ ÜRETİM TALİMATI", "",
           "⭐⭐ **T209 — aile kapısı KALIYOR ve genişlemiyor.** parti4'te kapı "
           "hiçbir bloğu reddetmedi ama düzeltmeyi sıfıra indirdi (parti3: 16 kayıt). "
           "Aynı iki aile, aynı tavan (%10).", "",
           "⛔ **`gd-024` AÇIK:** *«bedensel bildirim»* eşiğini altı kez ben koydum. "
           "Parti5'te de koyacağım ve **her birini yazacağım** — karar verilene "
           "kadar yapılabilecek tek şey bu.", "",
           "⛔ **`gd-022` AÇIK:** akut refah acilleri (barınma, maruz kalma) "
           "§5a″'nın dördüne de girmiyor.", "",
           "## ⛔ Bu planın söylemedikleri", "", "| | |", "|---|---|",
           f"| ⛔⛔ **K={K_UFUK} seçimdir** | gerekçesi ilan edildi ama türetilmedi |",
           "| ⛔⛔ **Fazla temsilin KUSUR olduğu gösterilmedi** | envanterin "
           "varsayımı *«set havuzu yansıtmalı»*; havuzun kendisi bir tasarım ürünü |",
           "| ⛔⛔ **T132 hâlâ geçerli** | daha çok veri güvenlik kapısını açacağına "
           "dair bir kanıt YOK |",
           "| ⛔⛔⛔ **DÖRT PARTİ YARGILANMADI** | üretim→judge→derleme döngüsünün "
           "ikinci adımı dört partidir atlandı; 237 kaydın terapötik kalitesi "
           "hakkında **hiçbir ölçüm yok** |"]
    RAPOR.write_text(RAPOR.read_text(encoding="utf-8") + "\n".join(ek), encoding="utf-8")
    print("\n".join(ek[:28]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
