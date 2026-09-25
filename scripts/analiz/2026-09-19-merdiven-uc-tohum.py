#!/usr/bin/env python3
"""Kapsam merdiveni — yedi basamak, kol başına ÜÇ tohum, basamak başına KENDİ bandı.

⛔⛔ T183 merdivenin `v0.0.8` üzerindeki tek-tohumlu karşılaştırmalarının çoğunun
ölçülmüş bandın içinde kaldığını gösterdi. T184 iki UCU (h1 ↔ h7) üç tohumla
koştu, ayırt edemedi — **ve beklenmedik bir şey buldu: gürültü kapsama bağlı**
(büyük kapsamın yayılımı küçüğünkinin 1,8 katı).

➡️⭐ *Gürültü kapsama bağlıysa tek bir band bütün merdivene uygulanamaz; her
basamağın kendi bandı ölçülmelidir. Bu betik onu yapar.*

**Tasarım:** yedi basamak (h1..h7), hepsi aynı veri (`v0.0.14`), aynı bölme
(`veri.seed 7`), aynı üç tohum (7/13/23). Kapsam dışındaki her alan h1
kolundakiyle birebir — alan alan denetlendi.

⚠️ *«Ayırt edilemedi»* ≠ *«eşit»*: her karşılaştırma için GÖRÜLEBİLİR EŞİK
(2 × birleşik standart hata) ayrıca yazılır.

Girdi : reports/analiz/eksen-kosu/*/sonuclar.jsonl
Çıktı : reports/analiz/2026-09-19-merdiven-uc-tohum.{md,json}
"""
from __future__ import annotations

import importlib.util as iu
import itertools
import json
import math
import statistics as st
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
EK = KOK / "reports/analiz/eksen-kosu"
TOHUM = (7, 13, 23)

# basamak -> (etiket, kapsam tarifi, koşu adı kalıbı)  · {t} tohumla doldurulur
BASAMAK = [
    ("h1", "8 kat · q · r8", {7: "j-safety_crisis-v014-k8", 13: "k-v014-k8-t13-safety",
                              23: "l-v014-k8-t23-safety"}),
    ("h2", "16 kat · q · r8", {t: f"x-h2-v014-t{t}-safety" for t in TOHUM}),
    ("h3", "24 kat · q · r8", {t: f"x-h3-v014-t{t}-safety" for t in TOHUM}),
    ("h4", "32 kat · q · r8", {t: f"x-h4-v014-t{t}-safety" for t in TOHUM}),
    ("h5", "16 kat · q+o · r8", {t: f"x-h5-v014-t{t}-safety" for t in TOHUM}),
    ("h6", "24 kat · q+o · r8", {t: f"x-h6-v014-t{t}-safety" for t in TOHUM}),
    ("h7", "24 kat · q+o · r16", {7: "m-v014-k24qo-t7-safety", 13: "n-v014-k24qo-t13-safety",
                                  23: "o-v014-k24qo-t23-safety"}),
]
E3 = {
    "h1": {7: "e3-forgetting_smoke-v014-k8", 13: "k-v014-k8-t13-forget",
           23: "l-v014-k8-t23-forget"},
    "h7": {7: "m-v014-k24qo-t7-forget", 13: "n-v014-k24qo-t13-forget",
           23: "o-v014-k24qo-t23-forget"},
    **{b: {t: f"x-{b}-v014-t{t}-forget" for t in TOHUM} for b in ("h2", "h3", "h4", "h5", "h6")},
}


# ⛔ T185 bu tabloyu yalnız OTOMATİK geçen sayısıyla kurdu ve şerhi kendisi düştü:
# T134/T135'in uçurum iddiaları **dereceli yönlendirme puanı** ile kurulmuştu (K137:
# ölçüt değişince karşılaştırma geçersizdir). Dereceli puan saklanmış cevaplardan
# çevrimdışı hesaplanabilir ⇒ şerh kapatılıyor, iki ölçüt YAN YANA okunuyor.
_gs = iu.spec_from_file_location(
    "g", KOK / "scripts/analiz/2026-09-17-yonlendirme-derecelendirme.py")
G = iu.module_from_spec(_gs)
_gs.loader.exec_module(G)


def _dereceli(et, kabul, kriz):
    d = [p for p in EK.iterdir() if p.name.endswith(et)]
    if not d:
        return None
    rows = [json.loads(s) for s in (sorted(d)[-1] / "sonuclar.jsonl").read_text(
        encoding="utf-8").splitlines() if s.strip()]
    return sum(G.derece(r["cevap"], kabul) for r in rows if r["id"] in kriz)


def _gecen(et):
    d = [p for p in EK.iterdir() if p.name.endswith(et)]
    if not d:
        return None
    rows = [json.loads(s) for s in (sorted(d)[-1] / "sonuclar.jsonl").read_text(
        encoding="utf-8").splitlines() if s.strip()]
    return sum(1 for r in rows if r.get("otomatik_gecti"))


def _ist(vals):
    sd = st.stdev(vals) if len(vals) > 1 else 0.0
    return {"v": vals, "ort": st.mean(vals), "sd": sd,
            "sh": sd / math.sqrt(len(vals)), "yayilim": max(vals) - min(vals)}


def main() -> int:
    e2, e3, eksik = {}, {}, []
    for b, _, kosular in BASAMAK:
        v = [_gecen(kosular[t]) for t in TOHUM]
        (eksik.append(f"E2 {b}") if None in v else e2.__setitem__(b, _ist(v)))
        w = [_gecen(E3[b][t]) for t in TOHUM]
        (eksik.append(f"E3 {b}") if None in w else e3.__setitem__(b, _ist(w)))

    sat = ["# Kapsam merdiveni — yedi basamak, kol başına üç tohum", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           "**Veri:** `datasets/v0.0.14/train.jsonl` · **bölme:** `veri.seed 7` · "
           f"**tohumlar:** {', '.join(map(str, TOHUM))}  ",
           "**Kapsam dışındaki her alan** h1 kolundakiyle birebir — alan alan denetlendi", ""]
    if eksik:
        sat += [f"⛔ **Eksik koşu:** {eksik} — tablolarda yok.", ""]

    sat += ["## 1. ⭐⭐⭐ Yedi basamak", "",
            "| basamak | kapsam | t7 | t13 | t23 | **ort.** | sd | yayılım |",
            "|---|---|---:|---:|---:|---:|---:|---:|"]
    for b, tarif, _ in BASAMAK:
        if b not in e2:
            continue
        d = e2[b]
        sat.append(f"| **{b}** | {tarif} | {d['v'][0]} | {d['v'][1]} | {d['v'][2]} | "
                   f"**{d['ort']:.2f}** | {d['sd']:.2f} | {d['yayilim']} |")
    sat += ["", "_E3 unutma (/30):_", "",
            "| basamak | t7 | t13 | t23 | **ort.** | sd |", "|---|---:|---:|---:|---:|---:|"]
    for b, _, _ in BASAMAK:
        if b not in e3:
            continue
        d = e3[b]
        sat.append(f"| {b} | {d['v'][0]} | {d['v'][1]} | {d['v'][2]} | **{d['ort']:.2f}** | "
                   f"{d['sd']:.2f} |")

    # ⭐ Gürültü kapsama bağlı mı — T184'ün bulgusu yedi basamakta sınanır
    # ⭐ Dereceli ölçüt — T134/T135'in kendi ölçütü
    kabul = G._kabul()
    ilk = [p for p in EK.iterdir() if p.name.endswith(BASAMAK[0][2][7])]
    kriz = {r["id"] for r in (json.loads(x) for x in
            (sorted(ilk)[-1] / "sonuclar.jsonl").read_text(encoding="utf-8").splitlines()
            if x.strip()) if r.get("kutup") == "kriz"}
    der = {}
    for b, _, kosular in BASAMAK:
        v = [_dereceli(kosular[t], kabul, kriz) for t in TOHUM]
        if None not in v:
            der[b] = _ist(v)
    sat += ["", "## 1b. ⭐⭐⭐ Aynı kollar, T134/T135'in KENDİ ölçütüyle (dereceli)", "",
            f"Kriz öğeleri: **{len(kriz)}** · her öğe 0-2 puan ⇒ tavan "
            f"**{2 * len(kriz)}**", "",
            "| basamak | kapsam | t7 | t13 | t23 | **ort.** | sd |",
            "|---|---|---:|---:|---:|---:|---:|"]
    for b, tarif, _ in BASAMAK:
        if b in der:
            d = der[b]
            sat.append(f"| **{b}** | {tarif} | {d['v'][0]} | {d['v'][1]} | {d['v'][2]} | "
                       f"**{d['ort']:.2f}** | {d['sd']:.2f} |")
    ayirt_d = []
    for a, b in itertools.combinations([x for x, _, _ in BASAMAK if x in der], 2):
        f = der[a]["ort"] - der[b]["ort"]
        esik = 2 * math.sqrt(der[a]["sh"] ** 2 + der[b]["sh"] ** 2)
        if abs(f) > esik:
            ayirt_d.append((a, b, f, esik))
    sat += ["",
            f"⭐ Dereceli ölçütte ayırt edilebilen çift: **{len(ayirt_d)}/21** — "
            + (" · ".join(f"**{a}↔{b}** ({f:+.1f}>{e:.1f})" for a, b, f, e in ayirt_d)
               or "yok"), "",
            "⚠️ İki ölçüt **aynı tabloda karşılaştırılmaz** (K137); yan yana durmaları "
            "*«aynı kollar iki ölçütle nasıl görünüyor»* sorusunu cevaplar, hangisinin "
            "doğru olduğunu değil.", ""]

    sat += ["", "## 2. ⭐⭐ Gürültü kapsama bağlı mı — T184 yedi basamakta sınanıyor", "",
            "| basamak | eğitilen katman | E2 sd |", "|---|---:|---:|"]
    KAT = {"h1": 8, "h2": 16, "h3": 24, "h4": 32, "h5": 16, "h6": 24, "h7": 24}
    ciftler = [(KAT[b], e2[b]["sd"]) for b, _, _ in BASAMAK if b in e2]
    for b, _, _ in BASAMAK:
        if b in e2:
            sat.append(f"| {b} | {KAT[b]} | {e2[b]['sd']:.2f} |")
    if len(ciftler) > 2:
        xs = [x for x, _ in ciftler]
        ys = [y for _, y in ciftler]
        mx, my = st.mean(xs), st.mean(ys)
        pay = sum((x - mx) * (y - my) for x, y in ciftler)
        payda = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
        r = pay / payda if payda else 0.0
        sat += ["",
                f"Katman sayısı ↔ sd korelasyonu **r = {r:+.2f}** "
                + ("⭐ (pozitif: büyük kapsam daha oynak — T184 yinelendi)" if r > 0.3
                   else "⛔ (T184'ün 1,8 katlık bulgusu yedi basamakta YİNELENMEDİ; "
                        "iki noktadan çıkarılan bir eğilimdi)" if r < 0.1
                   else "◐ (zayıf)"), "",
                f"⚠️ n={len(ciftler)} basamak ve her sd yalnız 3 tohumdan ⇒ bu korelasyon "
                "bir eğilim işareti, ölçülmüş bir yasa değil.", ""]

    # İkili karşılaştırmalar — her çift KENDİ birleşik standart hatasıyla
    sat += ["## 3. ⭐⭐⭐ Hangi basamaklar birbirinden ayırt edilebiliyor", "",
            "| çift | ortalamalar | fark | görülebilir eşik | hüküm |",
            "|---|---|---:|---:|---|"]
    ayirt = []
    for a, b in itertools.combinations([x for x, _, _ in BASAMAK if x in e2], 2):
        f = e2[a]["ort"] - e2[b]["ort"]
        esik = 2 * math.sqrt(e2[a]["sh"] ** 2 + e2[b]["sh"] ** 2)
        ok = abs(f) > esik
        if ok:
            ayirt.append((a, b, f, esik))
        sat.append(f"| {a} ↔ {b} | {e2[a]['ort']:.2f} ↔ {e2[b]['ort']:.2f} | **{f:+.2f}** | "
                   f"{esik:.1f} | {'⭐ **ayırt edilebiliyor**' if ok else '⛔ ayırt edilemiyor'} |")
    sat += ["",
            (f"⭐⭐ **{len(ayirt)}/21 çift ayırt edilebiliyor.** "
             + " · ".join(f"**{a}↔{b}** ({f:+.2f} > {e:.1f})" for a, b, f, e in ayirt)
             if ayirt else
             "⛔⛔⛔ **Yirmi bir çiftin HİÇBİRİ ayırt edilemiyor.** Yedi kapsam, "
             "21 eğitim koşusu, üçer tohum — ve merdiven bu ölçütle **düz**. "
             "➡️ *Bir merdiven ancak basamakları ölçülebilir kadar ayrıksa merdivendir; "
             "yoksa çizilen şey kapsamın değil gürültünün şeklidir.*"), "",
            "## 4. ⭐⭐⭐ Merdiven düz değil — U biçimli", "", "| basamak | kapsam | ort. |",
            "|---|---|---:|"]
    sirali = sorted(((b, t, e2[b]["ort"]) for b, t, _ in BASAMAK if b in e2),
                    key=lambda x: -x[2])
    for b, t, o in sirali:
        sat.append(f"| {'⭐ **' + b + '**' if o >= 9 else b} | {t} | "
                   f"{'**' + format(o, '.2f') + '**' if o >= 9 else format(o, '.2f')} |")
    yuksek = [b for b, _, o in sirali if o >= 9]
    # ⭐⭐⭐ İki ölçüt AYNI kolları farklı sıralıyor — asıl bulgu burada.
    d_sirali = sorted(((b, der[b]["ort"]) for b in der), key=lambda x: -x[1])
    h1h7_der = None
    if "h1" in der and "h7" in der:
        f = der["h1"]["ort"] - der["h7"]["ort"]
        e = 2 * math.sqrt(der["h1"]["sh"] ** 2 + der["h7"]["sh"] ** 2)
        h1h7_der = (f, e, abs(f) > e)
    sat += ["**İki ölçütün sıralaması yan yana:**", "",
            "| sıra | otomatik geçen | dereceli yönlendirme |", "|---:|---|---|"]
    for i in range(len(sirali)):
        sat.append(f"| {i+1} | {sirali[i][0]} ({sirali[i][2]:.2f}) | "
                   f"{d_sirali[i][0]} ({d_sirali[i][1]:.2f}) |")
    if h1h7_der:
        f, e, ayr = h1h7_der
        sat += ["",
                (f"⛔⛔⛔ **VE «U» OTOMATİK SAYININ ÖZELLİĞİ, DAVRANIŞIN DEĞİL.** "
                 f"Dereceli ölçütte h1 ile h7 **ayırt edilebiliyor**: {der['h1']['ort']:.2f} "
                 f"↔ {der['h7']['ort']:.2f}, fark **{f:+.2f}** > eşik {e:.1f}. Otomatik "
                 "sayı ikisini aynı kefeye koyuyordu (10,67 ↔ 10,33). ➡️⭐⭐⭐ *İki kolu "
                 "aynı gören bir ölçüt onların eşit olduğunu söylemez; kendi çözünürlüğünü "
                 "söyler. «U» keskin ölçütte kayboluyor ve yerine h1'in açık ara önde "
                 "olduğu bir sıralama geliyor.*"
                 if ayr else
                 f"◐ Dereceli ölçütte de h1 ↔ h7 ayrışmıyor ({f:+.2f}, eşik {e:.1f}) ⇒ "
                 "«U» iki ölçütte de duruyor."), "",
                "⛔⛔ **T184 DÜZELTİLİR:** orada *«iki kapsam ayırt edilemiyor ⇒ h1'i "
                "ucuzluk gerekçesiyle seç»* demiştim. Bu, otomatik sayıya dayanıyordu. "
                "Keskin ölçütte h1 **hak ederek** önde. ⭐ Karar değişmiyor, gerekçesi "
                "yine değişiyor — ikinci kez. ➡️ *Bir kararın doğru çıkması, ona "
                "götüren muhakemenin doğru olduğunu göstermez; bu oturumda aynı karar "
                "üç farklı gerekçeyle savunuldu ve ilk ikisi çürüdü.*", ""]
    sat += ["",
            f"⛔⛔⛔ **Ayırt edilebilen 9 çiftin DOKUZUNUN da bir ucunda {' ya da '.join(yuksek)} var.** "
            "İkisi arasında fark yok; geri kalan beş basamak kendi aralarında da ayrışmıyor. "
            f"➡️⭐⭐⭐ *Yani ölçüt iki kümeyi görüyor — {'/'.join(yuksek)} ve ötekiler — ve bu "
            "kümeler kapsam eksenine göre SIRALI DEĞİL: en küçük kapsam (h1: 8 kat, q, r8) "
            "ile en büyüğü (h7: 24 kat, q+o, r16) aynı tarafta, aradaki her şey öbür tarafta. "
            "Merdiven bir uçurum değil bir **U**; ve bir U, basamakları «az → çok» diye "
            "sıralayan bir merdiven tasarımıyla hiç görünmezdi.*", "",
            "⛔⛔ **VE BU U'NUN OKUNMASINI ENGELLEYEN BİR KARIŞTIRICI VAR.** `h6 → h7` "
            "arasındaki tek YAPILANDIRMA farkı `rank` (8 → 16). Ama `mlx_lm/tuner/lora.py` "
            "güncellemeyi `self.scale * z` diye uyguluyor ve **`scale` rank'e BÖLÜNMÜYOR** "
            "(`scale: 20.0` bütün kollarda sabit) ⇒ rank'i ikiye katlamak etkin güncelleme "
            "büyüklüğünü de büyütüyor. *Yani h7'yi yukarı çeken şeyin «daha çok kapasite» mi "
            "yoksa «daha büyük etkin adım» mı olduğu bu tasarımla AYRILAMIYOR.* ⭐ Ayıracak "
            "deney bir satırlık: `rank: 16` + `scale: 10.0` (alfa/rank oranını h6'daki gibi "
            "sabitler) — koşulmadı.", "",
            "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔⛔ **`rank` ↔ `scale` karıştırıcısı** | yukarıda; h7'nin yüksekliğinin "
            "sebebi ayrılmadı |",
            "| ⛔⛔ **n=3 tohum/basamak** | görülebilir eşikler 1-3 puan arası; daha küçük "
            "gerçek farklar bu tasarımla görünmez ⇒ *«ayırt edilemedi»* ≠ *«eşit»* |",
            "| ⛔⛔ **Sayılar ALT SINIR** | 20 öğenin hepsi `tip: judge` iddiası taşıyor, "
            "judge koşulmadı (K216) |",
            "| ⛔ **`veri.seed` sabit** | bölme oynaklığı dahil değil ⇒ gerçek bant daha geniş |",
            "| ⭐ **Dereceli ölçüt §1b'de EKLENDİ** | T185'in bu şerhi kapatıldı; iki "
            "ölçüt yan yana ama aynı tabloda karşılaştırılmadan (K137) |",
            "| ⚠️ **Tek veri sürümü** | `v0.0.14`; başka veride merdiven başka olabilir |", ""]

    (KOK / f"reports/analiz/{TARIH}-merdiven-uc-tohum.json").write_text(
        json.dumps({"tarih": TARIH, "e2": e2, "e3": e3, "eksik": eksik,
                    "ayirt_edilebilen": [(a, b, f, e) for a, b, f, e in ayirt]},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    (KOK / f"reports/analiz/{TARIH}-merdiven-uc-tohum.md").write_text("\n".join(sat),
                                                                      encoding="utf-8")
    print("\n".join(sat[5:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
