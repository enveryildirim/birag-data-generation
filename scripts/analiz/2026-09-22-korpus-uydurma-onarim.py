#!/usr/bin/env python3
"""`yansitma_ok` kapısının tuttuğu eski kopyaları KANONİK metinle tazeler.

⛔⛔⛔ **ÖNCE BİR DÜZELTME (T266'nın hükmü yanlıştı).** T266'da *«kapı
korpusta iki YENİ uydurma buldu, daha önce bilinmiyordu»* yazmıştım.
**Yanlış.** Ölçüldü: `data/judged/v0.0.8` … `v0.0.20` **girdilerinin
hepsi** ve `datasets/v0.0.8` … `v0.0.20` **train dosyalarının hepsi** bu
iki kayıt için **temiz metni** taşıyor. Uydurma yalnız **eski aday
anlık görüntülerinde** duruyor; sonraki parti sürümleri (`v5-parti4.v3`
ve sonrası, `v5-parti7.v4` ve sonrası) onu **zaten düzeltmiş**.

➡️ *Kapı yeni bir kusur bulmadı; **düzeltmenin geriye taşınmadığı eski
kopyaları** buldu. Bu daha küçük ama gerçek bir bulgudur: aynı kaydın
depoda hem kusurlu hem düzeltilmiş hâli duruyor ve hangisini okuduğun
dosyaya bağlı.*

⭐ **Bu yüzden bu betik metin UYDURMAZ.** Kanonik metni ana hat derleme
girdisinden (`data/judged/v0.0.18.jsonl` — yayımlanmış hâl) okur ve
kapıdan düşen kopyalara **birebir** taşır. ⇒ Onarımın yazarı ben
değilim, önceki turun düzeltmesidir.

⛔ `datasets/` DOKUNULMAZ (Kural 7) — zaten temiz.

Çıktı: kapıdan düşen kopyalar (yerinde)
       reports/analiz/2026-09-22-korpus-uydurma-onarim.md
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from checks import run_checks  # noqa: E402
from kunye import betik_tarihi  # noqa: E402
from yansitma import alinti_ihlalleri  # noqa: E402

RAPOR = KOK / "reports/analiz/2026-09-22-korpus-uydurma-onarim.md"
# ⭐ Kanonik kaynak: ANA HAT derleme girdisi. `v0.0.19`/`v0.0.20` deney
#   kollarıdır (CARD: «korpusun ilerleyişi değildir») ⇒ ana hat `v0.0.18`.
KANONIK = KOK / "data/judged/v0.0.18.jsonl"
HEDEF_GLOB = ["data/candidates/*.jsonl", "data/judged/v5-*.jsonl",
              "data/judged/v6-*.jsonl", "data/judged/v4-*.jsonl"]


def main() -> int:
    # 1) kanonik metinleri topla
    kanon = {}
    for l in open(KANONIK):
        r = json.loads(l)
        if r.get("id"):
            kanon[r["id"]] = r["messages"][-1]
    print(f"kanonik kaynak: {KANONIK.relative_to(KOK)} · {len(kanon)} kayıt")

    dosyalar = sorted({f for g in HEDEF_GLOB for f in glob.glob(str(KOK / g))})
    dokunulan, onarilan, kanonsuz = [], [], []
    for f in dosyalar:
        kayitlar = [json.loads(l) for l in open(f)]
        degisti = False
        for r in kayitlar:
            if not alinti_ihlalleri(r):
                continue
            kid = r.get("id")
            k = kanon.get(kid)
            if k is None:
                # ⛔ Kanonik hâli YOK ⇒ bu betik onu onaramaz. Uydurmak
                #   yerine RAPORLANIR (bir sonraki tur kararı).
                kanonsuz.append((Path(f).name, str(kid)[:10]))
                continue
            eski = r["messages"][-1]["content"]
            r["messages"][-1]["content"] = k["content"]
            if k.get("thinking"):
                r["messages"][-1]["thinking"] = k["thinking"]
            if alinti_ihlalleri(r):
                raise SystemExit(f"⛔ {Path(f).name}/{kid[:10]}: kanonik metin "
                                 "de ihlal taşıyor — HİÇBİR ŞEY yazılmadı")
            chk = run_checks(r)
            if not chk["passed"]:
                raise SystemExit(
                    f"⛔ {Path(f).name}/{kid[:10]} kanonikle kapıdan geçmiyor: "
                    + str([f"{a}={v}" for a, v in chk.items()
                           if a.endswith("_error") and v][:3]))
            # ⛔⛔ Yargı ESKİ metne ait — işaretlenir, SİLİNMEZ (T121:
            #   `judge: null` kaydı derlemeden eler).
            if r.get("judge") and not r["judge"].get("_metin_tazelendi"):
                r["judge"]["_metin_tazelendi"] = betik_tarihi(__file__)
            onarilan.append((Path(f).name, kid[:10], eski.split("\n")[0][:60]))
            degisti = True
        if degisti:
            Path(f).write_text("".join(json.dumps(x, ensure_ascii=False) + "\n"
                                       for x in kayitlar), encoding="utf-8")
            dokunulan.append(str(Path(f).relative_to(KOK)))

    # 2) kalan
    kalan = []
    for f in dosyalar:
        for l in open(f):
            r = json.loads(l)
            if alinti_ihlalleri(r):
                kalan.append((Path(f).name, str(r.get("id"))[:10]))

    kimlikler = sorted({k for _, k, _ in onarilan})
    s = [f"# Kapıdan düşen eski kopyalar kanonik metinle tazelendi", "",
         f"**Betik:** `{Path(__file__).relative_to(KOK)}` · "
         f"**Tarih:** {betik_tarihi(__file__)}  ",
         f"**Kanonik kaynak:** `{KANONIK.relative_to(KOK)}` (ana hat)  ",
         f"**Tazelenen satır:** {len(onarilan)} · "
         f"**kayıt:** {len(kimlikler)} · **dosya:** {len(dokunulan)}  ", "",
         "## ⛔⛔⛔ T266'nın bir hükmü GERİ ALINDI", "",
         "T266'da *«kapı korpusta iki YENİ uydurma buldu, daha önce "
         "bilinmiyordu»* yazmıştım. **Yanlış.** Ölçüldü: `data/judged/v0.0.8` "
         "… `v0.0.20` girdilerinin **hepsi** ve `datasets/v0.0.8` … "
         "`v0.0.20` train dosyalarının **hepsi** bu kayıtlar için **temiz "
         "metni** taşıyor. Sonraki parti sürümleri (`v5-parti4.v3`+, "
         "`v5-parti7.v4`+) düzeltmeyi **zaten yapmış**.", "",
         "➡️ **Gerçek bulgu daha küçük ama gerçek:** kapı yeni bir kusur "
         "değil, **düzeltmenin geriye taşınmadığı eski kopyaları** buldu. "
         "Aynı kaydın depoda hem kusurlu hem düzeltilmiş hâli duruyor ve "
         "**hangisini okuduğun dosyaya bağlı**.", "",
         "⭐ Bu yüzden onarım metni **uydurulmadı**: kanonik hâl ana hat "
         "derleme girdisinden birebir taşındı.", "",
         "## Tazelenen satırlar", "", "| dosya | id | eski ilk satır |",
         "|---|---|---|"]
    s += [f"| `{a}` | `{b}` | {c}… |" for a, b, c in onarilan]
    if kanonsuz:
        s += ["", "⛔⛔ **Kanonik hâli olmayan, bu yüzden ONARILMAYAN:**", ""]
        s += [f"- `{a}` / `{b}` — ana hat girdisinde yok" for a, b in kanonsuz]
        s += ["", "⚠️ Bunlar ana hatta hiç derlenmemiş kayıtlar; metni "
              "uydurmak yerine bırakıldı. Kapı onları tutmaya devam eder.", ""]
    s += ["", "## Kapı artık ne tutuyor", ""]
    s += ([f"⛔ {len(kalan)} satır: " + " · ".join(f"`{a}`/`{b}`"
                                                  for a, b in kalan[:8]), ""]
          if kalan else ["⭐ Taranan dosyalarda **hiçbir satır** tutulmuyor.", ""])
    s += ["## ⛔ Bunun söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔⛔ **Yargı eski metne ait** | tazelenen satırların `judge` "
          "alanına `_metin_tazelendi` işareti kondu; yargı **silinmedi** "
          "çünkü `judge: null` kaydı derlemeden eler (T121). Ama not: "
          "kanonik metin **zaten ana hatta yargılanmış** metindir ⇒ "
          "`v0.0.18` girdisindeki yargı ona aittir |",
          "| ⛔ **`datasets/` dokunulmadı** | Kural 7 — ve zaten temizdi |",
          "| ⛔ **Kapı dar** | `yansitma_ok` yalnız alıntıyla atfa bakar "
          "(kesinlik %100, duyarlılık %1) ⇒ eski kopyalarda **alıntısız** "
          "parafraz uydurması olabilir, bu tarama onu göstermez |",
          "| ⛔ **Eski kopyalar neden duruyor** | `data/candidates/` altında "
          "aynı kaydın parti sürümleri yan yana duruyor ve hangisinin "
          "güncel olduğunu söyleyen bir alan **yok**. Bu tazeleme o sorunu "
          "**çözmez**, yalnız bir örneğini kapatır |"]

    RAPOR.write_text("\n".join(s) + "\n", encoding="utf-8")
    assert RAPOR.exists()
    print(f"⭐ {len(onarilan)} satır tazelendi · {len(kimlikler)} kayıt · "
          f"{len(dokunulan)} dosya")
    for a, b, c in onarilan:
        print(f"   {a:32} {b}")
    if kanonsuz:
        print(f"⛔ kanoniği olmayan (onarılmadı): {kanonsuz}")
    print(f"⛔ kapının hâlâ tuttuğu satır: {len(kalan)}")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
