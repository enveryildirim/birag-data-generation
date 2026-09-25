#!/usr/bin/env python3
"""Tohum oynaklığı — sert kapının kendi gürültü tabanı, VERİ SABİTKEN.

⛔ T181'de `v0.0.10` → `v0.0.14` geçişinde sert kapıda öğe düzeyinde **3 gerileyen /
3 yükselen** çıktı, toplam oynamadı ve veri farkı **%0,014**'tü. O oynamanın ne
kadarı veriden, ne kadarı eğitimin kendi rastgeleliğinden geliyor bilinmiyordu.

⭐⭐ **Deney:** aynı veri (`v0.0.14`), aynı bölme (`veri.seed: 7`), aynı kapsam,
aynı LR/adım/batch — **yalnız `mlx.seed`** 7 / 13 / 23. Üç nokta ⇒ üç ikili
karşılaştırma. Yapılandırmalar alan alan denetlendi: fark yalnız `ad` + `mlx.seed`.

➡️ *Bir ölçütün gürültü tabanı, o ölçütün hiçbir şey değişmediğinde ne kadar
oynadığıdır. Burada «hiçbir şey» = veri; oynayan tek şey eğitimin kendi kurası.*

⚠️ Bu bir ALT SINIRDIR: bölme değişimini içermiyor, gerçek kol-kola oynaklık
bundan büyük olabilir, küçük olamaz.

Girdi : reports/analiz/eksen-kosu/*/sonuclar.jsonl
Çıktı : reports/analiz/2026-09-19-tohum-oynakligi.{md,json}
"""
from __future__ import annotations

import collections
import itertools
import json
import statistics as st
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
KOSU = KOK / "reports/analiz/eksen-kosu"

TOHUM = {7: "j-safety_crisis-v014-k8", 13: "k-v014-k8-t13-safety", 23: "l-v014-k8-t23-safety"}
UNUTMA = {7: "e3-forgetting_smoke-v014-k8", 13: "k-v014-k8-t13-forget",
          23: "l-v014-k8-t23-forget"}
VERI = {"v0.0.10": "i-safety_crisis-v010-k8", "v0.0.14": "j-safety_crisis-v014-k8"}


def _yukle(parca):
    d = sorted(KOSU.glob(f"*{parca}"))
    if not d:
        return None
    return {r["id"]: r for r in (json.loads(l) for l in
            (d[-1] / "sonuclar.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}


def _churn(a, b):
    o = sorted(set(a) & set(b))
    d = [i for i in o if a[i].get("otomatik_gecti") and not b[i].get("otomatik_gecti")]
    u = [i for i in o if not a[i].get("otomatik_gecti") and b[i].get("otomatik_gecti")]
    return {"n": len(o), "dusen": d, "yukselen": u, "oynayan": len(d) + len(u)}


def main() -> int:
    S = {t: _yukle(p) for t, p in TOHUM.items()}
    F = {t: _yukle(p) for t, p in UNUTMA.items()}
    eksik = [t for t, v in S.items() if v is None]
    assert not eksik, f"⛔ eksik sert kapı koşusu: {eksik}"
    gecen = {t: sum(1 for r in J.values() if r.get("otomatik_gecti")) for t, J in S.items()}
    ikili = {f"{a}↔{b}": _churn(S[a], S[b]) for a, b in itertools.combinations(sorted(S), 2)}
    veri_churn = _churn(_yukload := _yukle(VERI["v0.0.10"]), S[7])

    bos = {t: [i for i, r in J.items() if not (r.get("cevap") or "").strip()]
           for t, J in S.items()}
    bos_gecen = {t: [i for i in ids if J[i].get("otomatik_gecti")]
                 for t, J in S.items() for tt, ids in [(t, bos[t])] if True}

    oynayanlar = [v["oynayan"] for v in ikili.values()]
    sat = [
        "# Tohum oynaklığı — sert kapının gürültü tabanı, veri sabitken", "",
        f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
        "**Kollar:** `j-v014-k8` (tohum 7) · `k-v014-k8-t13` · `l-v014-k8-t23` — "
        "veri, bölme, kapsam, LR, adım, batch **birebir aynı**; fark yalnız `mlx.seed`  ",
        "**Set:** `evals/safety_crisis.jsonl` (mühürlü, K31) · protokol `max_tokens=1024`", "",
        "## 1. ⭐⭐⭐ Toplam — aynı veri, üç tohum", "",
        "| tohum | otomatik geçen |", "|---|---:|"]
    sat += [f"| **{t}** | **{gecen[t]}**/{len(S[t])} |" for t in sorted(S)]
    yayilim = max(gecen.values()) - min(gecen.values())
    sat += ["",
            f"⛔⛔⛔ **Yalnız tohum değişince sert kapı {min(gecen.values())} ile "
            f"{max(gecen.values())} arasında oynuyor — yayılım {yayilim} puan.** Veri, "
            "bölme, hiperparametre: hepsi sabit. ➡️ *Bu ölçütün gürültü tabanı "
            f"**en az {yayilim} puan**; T159 bunu dolaylı bir deneyle 3 puan ölçmüştü, "
            "burada doğrudan ölçüldü.*", "",
            "## 2. ⭐⭐ Öğe düzeyinde — tohum oynaklığı ↔ veri değişimi", "",
            "| karşılaştırma | değişen | oynayan öğe | ↓ | ↑ |", "|---|---|---:|---:|---:|"]
    for ad, v in ikili.items():
        sat.append(f"| tohum {ad} | **yalnız tohum** | **{v['oynayan']}**/{v['n']} | "
                   f"{len(v['dusen'])} | {len(v['yukselen'])} |")
    sat.append(f"| veri v0.0.10↔v0.0.14 (tohum 7) | **yalnız veri (%0,014)** | "
               f"**{veri_churn['oynayan']}**/{veri_churn['n']} | "
               f"{len(veri_churn['dusen'])} | {len(veri_churn['yukselen'])} |")
    ort_tohum = st.mean(oynayanlar)
    sat += ["",
            (f"⛔⛔⛔ **Tohum tek başına ortalama {ort_tohum:.1f} öğe oynatıyor; veri "
             f"değişimi {veri_churn['oynayan']} öğe oynattı.** ➡️⭐⭐⭐ *T181'deki "
             "3↓/3↑ veriye atfedilemez: aynı büyüklükteki oynama hiç veri değişmeden "
             "de çıkıyor. «Düzeltmeler şu öğeyi bozdu» cümlesi bu ölçütle kurulamaz.*"
             if ort_tohum >= veri_churn["oynayan"] * 0.7 else
             f"◐ **Tohum ortalama {ort_tohum:.1f} öğe oynatıyor, veri değişimi "
             f"{veri_churn['oynayan']}.** Veri etkisi tohumdan belirgin büyük "
             "görünüyor; yine de n=3 tohum."), "",
            "## 3. ⚠️ Unutma ekseni aynı tohumlarda", "", "| tohum | otomatik geçen |",
            "|---|---:|"]
    for t in sorted(F):
        sat.append(f"| {t} | {'—' if F[t] is None else f'{sum(1 for r in F[t].values() if r.get(chr(111)+chr(116)+chr(111)+chr(109)+chr(97)+chr(116)+chr(105)+chr(107)+chr(95)+chr(103)+chr(101)+chr(99)+chr(116)+chr(105)))}/{len(F[t])}'} |")
    fg = {t: sum(1 for r in J.values() if r.get("otomatik_gecti"))
          for t, J in F.items() if J}
    f_yayilim = (max(fg.values()) - min(fg.values())) if fg else 0
    sat += ["",
            f"⛔⛔⛔ **Unutma da tohumla oynuyor — yayılım {f_yayilim} puan.** Ve bu, "
            "T160'ın *«bu ölçütte gürültü tabanı 0»* bulgusuyla ÇELİŞMİYOR; iki ayrı "
            "gürültüden söz ediliyor ve bu ayrım şimdiye kadar yazılı değildi:", "",
            "| gürültü kaynağı | nasıl ölçülür | ölçülen |", "|---|---|---:|",
            "| **üretim** — aynı adaptör yeniden koşulur | K105 determinist üretim | "
            "**0** (T160) |",
            f"| **eğitim** — aynı veri, farklı tohum | yeniden eğitilir | "
            f"**E2 {yayilim} · E3 {f_yayilim} puan** (burası) |", "",
            "➡️⭐⭐⭐ *Pareto kapısı KOLLARI karşılaştırır, aynı kolu değil ⇒ ilgili taban "
            "üretim gürültüsü değil **eğitim gürültüsüdür** ve o bugüne kadar hiç "
            "ölçülmemişti. Bu yüzden geçmiş raporlarda «29 ↔ 29» gibi eşitlikler TAM "
            "eşitlik gibi okundu; oysa o ölçüt de ±"
            f"{f_yayilim} oynuyor.* ⛔ T181'in *«T160'ta taban 0 ⇒ buradaki eşitlik "
            "gerçek»* cümlesi bu yüzden **yanlıştı** ve burada düzeltilir.", ""]

    bosluklu = {t: ids for t, ids in bos.items() if ids}
    if bosluklu:
        sat += ["## 4. ⛔⛔ Boş cevap — ve kapının onu nasıl gördüğü", "",
                "| tohum | boş cevap | bunlardan **kapıyı geçen** |", "|---|---|---:|"]
        for t, ids in bosluklu.items():
            gec = [i for i in ids if S[t][i].get("otomatik_gecti")]
            sat.append(f"| {t} | {', '.join('`'+i+'`' for i in ids)} | "
                       f"**{len(gec)}**{' ⛔ ' + ', '.join(gec) if gec else ''} |")
        hepsi_gec = [i for t, ids in bosluklu.items() for i in ids
                     if S[t][i].get("otomatik_gecti")]
        sat += ["",
                ("⛔⛔⛔ **BOŞ CEVAP KAPIYI GEÇTİ.** Hiçbir şey söylemeyen bir cevap "
                 "*«yasak ifade içermiyor»*, *«rakam yazmıyor»* olduğu için geçiyor ⇒ "
                 "kapı **suskunluğu** güvenli sayıyor. ➡️ *Bir güvenlik kapısı "
                 "yalnız YANLIŞ söyleneni denetliyorsa, HİÇ söylememek en güvenli "
                 "davranış olur — ölçüt suskunluğu ödüllendiriyor.*"
                 if hepsi_gec else
                 "⭐ Boş cevaplar kapıyı geçmedi (uzunluk kuralı yakaladı)."), ""]

    sat += ["## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **ALT SINIR** | `veri.seed` bilerek sabit tutuldu ⇒ bölme değişimi "
            "dahil değil; gerçek kol-kola oynaklık bundan **büyük** olabilir |",
            "| ⛔⛔ **n=3 tohum** | yayılım üç noktadan; güven aralığı geniş |",
            "| ⛔ **Sayılar ALT SINIR (ikinci anlamda)** | 20 öğenin hepsi `tip: judge` "
            "iddiası taşıyor ve judge koşulmadı (kota, K216) |",
            "| ⛔ **Hangi tohumun «doğru» olduğu bilinmiyor** | ölçülen oynaklık, "
            "doğruluk değil |", ""]

    (KOK / f"reports/analiz/{TARIH}-tohum-oynakligi.json").write_text(
        json.dumps({"tarih": TARIH, "gecen": gecen, "yayilim": yayilim,
                    "ikili_churn": ikili, "veri_churn": veri_churn,
                    "bos_cevap": bos}, ensure_ascii=False, indent=2), encoding="utf-8")
    (KOK / f"reports/analiz/{TARIH}-tohum-oynakligi.md").write_text("\n".join(sat),
                                                                    encoding="utf-8")
    print("\n".join(sat[4:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
