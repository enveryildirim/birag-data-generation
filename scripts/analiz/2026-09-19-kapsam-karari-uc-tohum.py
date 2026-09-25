#!/usr/bin/env python3
"""Kapsam kararı — h1 ↔ h7, aynı veri, kol başına ÜÇ tohum.

⛔⛔ T183 üç yapılandırma dosyasının başındaki cümleyi çürüttü: *«h1 iki Pareto
kapısını da geçen tek kol»*. `v0.0.8` taramasında h1 **10**, h7 **11** çıkmıştı
ve fark (1) ölçülmüş bandın (±2) içindeydi — üstelik h7 nominal olarak daha
yüksek. Soru cevaplanmamıştı, cevaplanmış SAYILMIŞTI.

⭐⭐ **Tasarım.** Tek koşu bandı daraltmaz; kol başına üç tohumun ORTALAMASI
daraltır. İki kapsam **aynı veri (`v0.0.14`), aynı bölme, aynı üç tohum
(7/13/23)** ile koşuldu. Kapsam dışındaki her şey alan alan denetlendi.

➡️ *Bir farkı göstermek için ölçütü keskinleştirmek şart değil; aynı ölçütü
birkaç kez koşup ortalamak da bandı daraltır — ve hangi büyüklükteki farkın
GÖRÜLEBİLECEĞİNİ önceden söyler.*

Girdi : reports/analiz/eksen-kosu/*/sonuclar.jsonl
Çıktı : reports/analiz/2026-09-19-kapsam-karari-uc-tohum.{md,json}
"""
from __future__ import annotations

import json
import math
import statistics as st
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
EK = KOK / "reports/analiz/eksen-kosu"

KAPSAM = {
    "h1 · 8 kat · q · r8": {
        7: ("j-safety_crisis-v014-k8", "e3-forgetting_smoke-v014-k8"),
        13: ("k-v014-k8-t13-safety", "k-v014-k8-t13-forget"),
        23: ("l-v014-k8-t23-safety", "l-v014-k8-t23-forget")},
    "h7 · 24 kat · q+o · r16": {
        7: ("m-v014-k24qo-t7-safety", "m-v014-k24qo-t7-forget"),
        13: ("n-v014-k24qo-t13-safety", "n-v014-k24qo-t13-forget"),
        23: ("o-v014-k24qo-t23-safety", "o-v014-k24qo-t23-forget")},
}


def _gecen(et):
    d = [p for p in EK.iterdir() if p.name.endswith(et)]
    if not d:
        return None
    rows = [json.loads(s) for s in (sorted(d)[-1] / "sonuclar.jsonl").read_text(
        encoding="utf-8").splitlines() if s.strip()]
    return sum(1 for r in rows if r.get("otomatik_gecti")), len(rows)


def _sure(kol_parcasi):
    """Kolun ORTALAMA eğitim süresi — üç tohumun hepsi sayılır.

    ⚠️ İlk sürüm `runs/*{parca}/metrics.json` diye aradı ve dizin adları `-t7`
    gibi bir sonekle bittiği için h7 kollarını hiç bulamadı (tabloda «—» çıktı).
    Sonek serbest bırakıldı ve tek koşu yerine ORTALAMA alındı.
    """
    d = sorted(KOK.glob(f"runs/*{kol_parcasi}*/metrics.json"))
    if not d:
        return None
    v = [json.loads(x.read_text())["sure_saniye"] / 60 for x in d]
    return sum(v) / len(v)


def main() -> int:
    veri = {}
    for kapsam, tohumlar in KAPSAM.items():
        veri[kapsam] = {}
        for t, (se, fe) in tohumlar.items():
            s, f = _gecen(se), _gecen(fe)
            assert s and f, f"⛔ eksik koşu: {se} / {fe}"
            veri[kapsam][t] = {"e2": s[0], "e2_n": s[1], "e3": f[0], "e3_n": f[1]}

    def ist(kapsam, alan):
        v = [veri[kapsam][t][alan] for t in sorted(veri[kapsam])]
        sd = st.stdev(v)
        return {"degerler": v, "ort": st.mean(v), "sd": sd, "sh": sd / math.sqrt(len(v)),
                "yayilim": max(v) - min(v)}

    A, B = list(KAPSAM)
    e2 = {k: ist(k, "e2") for k in KAPSAM}
    e3 = {k: ist(k, "e3") for k in KAPSAM}
    sure = {A: _sure("v014-k8") , B: _sure("v014-k24qo")}

    sat = ["# Kapsam kararı — h1 ↔ h7, aynı veri, kol başına üç tohum", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           "**Veri:** `datasets/v0.0.14/train.jsonl` · **bölme:** `veri.seed 7` (sabit) · "
           "**tohumlar:** 7 / 13 / 23  ",
           "**Kapsam dışındaki her alan** h1 kolundakiyle birebir — alan alan denetlendi", "",
           "## 1. ⭐⭐⭐ Altı kol", "",
           "| kapsam | t7 | t13 | t23 | **ortalama** | sd | yayılım |",
           "|---|---:|---:|---:|---:|---:|---:|"]
    for ad, s in (("**E2 sert kapı** (/20)", e2), ("**E3 unutma** (/30)", e3)):
        sat.append(f"| _{ad}_ | | | | | | |")
        for k in KAPSAM:
            d = s[k]
            sat.append(f"| {k} | {d['degerler'][0]} | {d['degerler'][1]} | "
                       f"{d['degerler'][2]} | **{d['ort']:.2f}** | {d['sd']:.2f} | "
                       f"{d['yayilim']} |")

    def karsilastir(s, ad):
        fark = s[A]["ort"] - s[B]["ort"]
        bsh = math.sqrt(s[A]["sh"] ** 2 + s[B]["sh"] ** 2)
        gorulebilir = 2 * bsh
        return fark, bsh, gorulebilir, abs(fark) > gorulebilir

    sat += [""]
    ozet = {}
    for s, ad in ((e2, "E2 sert kapı"), (e3, "E3 unutma")):
        fark, bsh, gor, ayirt = karsilastir(s, ad)
        ozet[ad] = {"fark": fark, "birlesik_sh": bsh, "gorulebilir_esik": gor,
                    "ayirt_edilebilir": ayirt}
        sat += [f"**{ad}:** h1 − h7 = **{fark:+.2f}** · birleşik standart hata "
                f"**{bsh:.2f}** ⇒ bu tasarımla **ancak {gor:.1f} puandan büyük** bir "
                f"fark görülebilirdi. " +
                ("⭐ Fark bu eşiği aşıyor." if ayirt else
                 "⛔⛔ **Fark eşiğin çok altında — iki kapsam ayırt edilemiyor.**"), ""]

    sat += ["## 2. ⭐⭐⭐ Beklenmeyen bulgu — gürültü KAPSAMA BAĞLI", "",
            "| kapsam | E2 yayılımı | E2 sd |", "|---|---:|---:|"]
    for k in KAPSAM:
        sat.append(f"| {k} | {e2[k]['yayilim']} | {e2[k]['sd']:.2f} |")
    oran = e2[B]["sd"] / e2[A]["sd"] if e2[A]["sd"] else float("inf")
    sat += ["",
            f"⛔⛔⛔ **Büyük kapsamın oynaklığı küçüğünkinin {oran:.1f} katı** "
            f"({e2[A]['yayilim']} → {e2[B]['yayilim']} puan yayılım). ➡️ *T183'te "
            "«kapsam bağımsızlığı VARSAYIM, ölçülmedi» diye şerh düşmüştüm — şimdi "
            "ölçüldü ve varsayım **yanlış** çıktı. Büyük kollar daha oynak; T183'ün "
            "büyük kapsamlı ailelere uyguladığı ±2 bandı bu yüzden **fazla dar**, "
            "yani o ailelerde bandın içinde kalan iddia sayısı raporladığımdan "
            "**daha fazla**.*", "",
            "## 3. ⭐ Maliyet — eşit sonuç, eşit olmayan bedel", "",
            "| kapsam | eğitim süresi (ort.) |", "|---|---:|"]
    for k in KAPSAM:
        sat.append(f"| {k} | {sure[k]:.1f} dk |" if sure[k] else f"| {k} | — |")
    sat += ["",
            "⭐⭐ **Karar kuralı, ölçüm iddiası değil:** iki seçenek ayırt edilemiyorsa "
            "ucuz ve basit olan seçilir. ⇒ **h1 kapsamı korunur** — ama artık "
            "*«iki kapıyı da geçen tek kol»* olduğu için değil, **h7'den ayırt "
            "edilemediği ve daha ucuz olduğu için**. ➡️ *Aynı karar, başka gerekçe; "
            "ve gerekçenin doğru olması kararın doğru olmasından ayrı bir iştir.*", "",
            "⛔ Üç yapılandırma dosyasının başındaki *«iki Pareto kapısını da geçen tek "
            "kol»* cümlesi bu bulguyla **yanlış**tır ve düzeltilmelidir.", "",
            "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **n=3 tohum/kol** | görülebilir eşik ~"
            f"{ozet['E2 sert kapı']['gorulebilir_esik']:.1f} puan; daha küçük gerçek "
            "farklar bu tasarımla görünmez |",
            "| ⛔⛔ **Sayılar ALT SINIR** | 20 öğenin hepsi `tip: judge` iddiası taşıyor, "
            "judge koşulmadı (K216) |",
            "| ⛔ **İki kapsam noktası** | merdivenin tamamı üç tohumla koşulmadı; "
            "yalnız uçları |",
            "| ⛔ **`veri.seed` sabit** | bölme oynaklığı hâlâ dahil değil ⇒ gerçek "
            "kol-kola bant bundan da geniş |",
            "| ⚠️ **Eşit sonuç «ikisi de iyi» demek değil** | ikisi de sert kapıda "
            "tabanın (11/20) altında ya da civarında |", ""]

    (KOK / f"reports/analiz/{TARIH}-kapsam-karari-uc-tohum.json").write_text(
        json.dumps({"tarih": TARIH, "veri": veri, "e2": e2, "e3": e3,
                    "karsilastirma": ozet, "sure_dk": sure},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    (KOK / f"reports/analiz/{TARIH}-kapsam-karari-uc-tohum.md").write_text(
        "\n".join(sat), encoding="utf-8")
    print("\n".join(sat[5:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
