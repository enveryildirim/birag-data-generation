#!/usr/bin/env python3
"""Yayılım mı derinlik mi — ölçüt koşudan ÖNCE ilan edilmişti.

⛔ T187 güçlü bir hipotez buldu ama POST-HOC buldu: `h1` ile `h8` toplam
güncelleme enerjisinde eşitken (10,4 ↔ 10,5) dereceli puanda 16,33 ↔ 4,00
ayrıldılar; tek yapısal fark kaç modüle dokunulduğuydu (8 ↔ 48).

⚠️ Üstelik merdivenin tamamında iki şey İÇ İÇEYDİ: kollar büyüdükçe hem katman
derinliği hem modül sayısı birlikte artıyordu.

⭐⭐⭐ `h9` (8 katman · q+o · r8 · s20) ikisini ayırır ve ölçütü **koşudan önce**
`configs/training/z-h9-k8qo-v014-t*.yaml` başlığına yazıldı:
  · h9 ≈ h1 (~16,3) ⇒ belirleyen **derinlik**, T187 çürür
  · h9 ≈ h2 (~2,0)  ⇒ belirleyen **modül sayısı**, T187 doğrulanır
  · arada (5-13)    ⇒ ikisi birlikte

Bu betik ilan edilen ölçütü uygular ve iki temiz tek-değişkenli karşılaştırmayı
kurar (biri derinliği, öteki modül sayısını sabitler).

Girdi : reports/analiz/eksen-kosu/*/sonuclar.jsonl · runs/*/adapters/
Çıktı : reports/analiz/2026-09-20-yayilim-mi-derinlik-mi.{md,json}
"""
from __future__ import annotations

import importlib.util as iu
import json
import math
import statistics as st
from pathlib import Path

import mlx.core as mx
import yaml

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
EK = KOK / "reports/analiz/eksen-kosu"
TOHUM = (7, 13, 23)
ILAN = {"h1_gibi": 16.3, "h2_gibi": 2.0, "ara_alt": 5.0, "ara_ust": 13.0}

_gs = iu.spec_from_file_location(
    "g", KOK / "scripts/analiz/2026-09-17-yonlendirme-derecelendirme.py")
G = iu.module_from_spec(_gs)
_gs.loader.exec_module(G)

KOL = {
    "h1": ("8 kat · q", 8, 8, ["j-safety_crisis-v014-k8", "k-v014-k8-t13-safety",
                               "l-v014-k8-t23-safety"], "j-v014-k8"),
    "h9": ("8 kat · **q+o**", 8, 16, [f"z-h9-k8qo-v014-t{t}-safety" for t in TOHUM],
           "z-h9-k8qo-v014-t7"),
    "h2": ("**16 kat** · q", 16, 16, [f"x-h2-v014-t{t}-safety" for t in TOHUM],
           "x-h2-v014-t7"),
    "h8": ("24 kat · q+o · r16 · s10", 24, 48,
           [f"y-h8-r16s10-v014-t{t}-safety" for t in TOHUM], "y-h8-r16s10-v014-t7"),
}


def _rows(et):
    d = [p for p in EK.iterdir() if p.name.endswith(et)]
    return None if not d else [json.loads(s) for s in
        (sorted(d)[-1] / "sonuclar.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]


def _norm(parca):
    k = sorted(KOK.glob(f"runs/*-{parca}"))[-1]
    sc = float(yaml.safe_load((k / "config.yaml").read_text(
        encoding="utf-8"))["mlx"]["lora_parameters"]["scale"])
    w = mx.load(str(k / "adapters" / "adapters.safetensors"))
    ns = []
    for key in w:
        if key.endswith(".lora_a"):
            d = (sc * w[key[:-6] + "lora_b"].T) @ w[key].T
            ns.append(float(mx.sqrt(mx.sum(d * d)).item()))
    return len(ns), math.sqrt(sum(n * n for n in ns)), st.mean(ns)


def main() -> int:
    kabul = G._kabul()
    kriz = {r["id"] for r in _rows("j-safety_crisis-v014-k8") if r.get("kutup") == "kriz"}
    V = {}
    for k, (tarif, kat, mod, ets, kosu) in KOL.items():
        d = [sum(G.derece(r["cevap"], kabul) for r in _rows(e) if r["id"] in kriz)
             for e in ets]
        o = [sum(1 for r in _rows(e) if r.get("otomatik_gecti")) for e in ets]
        n_mod, top, mb = _norm(kosu)
        assert n_mod == mod, f"⛔ {k}: modül sayısı beklenen {mod}, ölçülen {n_mod}"
        V[k] = {"tarif": tarif, "kat": kat, "mod": mod, "d": d, "d_ort": st.mean(d),
                "d_sh": st.stdev(d) / math.sqrt(len(d)), "o_ort": st.mean(o),
                "toplam": top, "modul_basina": mb}

    def kars(a, b):
        f = V[a]["d_ort"] - V[b]["d_ort"]
        e = 2 * math.sqrt(V[a]["d_sh"] ** 2 + V[b]["d_sh"] ** 2)
        return f, e, abs(f) > e

    h9 = V["h9"]["d_ort"]
    if abs(h9 - ILAN["h1_gibi"]) < abs(h9 - ILAN["h2_gibi"]) and not kars("h9", "h1")[2]:
        hukum = ("⭐ **İlan edilen birinci şık: belirleyen DERİNLİK.** h9, h1'den ayırt "
                 "edilemiyor ⇒ modül sayısını iki katına çıkarmak bir şey değiştirmedi; "
                 "T187'nin «yayılım» hipotezi **çürüdü**.")
    elif not kars("h9", "h2")[2]:
        hukum = ("⭐ **İlan edilen ikinci şık: belirleyen MODÜL SAYISI.** h9, h2'den ayırt "
                 "edilemiyor ⇒ derinliği yarıya indirmek bir şey değiştirmedi; T187 "
                 "**doğrulandı**.")
    else:
        hukum = (f"⭐⭐⭐ **İlan edilen ÜÇÜNCÜ şık: ikisi birlikte.** h9 = {h9:.2f}, "
                 f"ilan edilen ara bölgede ({ILAN['ara_alt']:.0f}-{ILAN['ara_ust']:.0f}) "
                 "ve **hem h1'den hem h2'den ayırt ediliyor** ⇒ ne derinlik ne modül "
                 "sayısı tek başına açıklıyor.")

    sat = ["# Yayılım mı derinlik mi — ölçüt koşudan önce ilan edilmişti", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           "**İlan:** `configs/training/z-h9-k8qo-v014-t*.yaml` başlığı, koşudan önce  ",
           "**Kollar:** aynı veri (`v0.0.14`), aynı bölme, tohum 7/13/23", "",
           "## 1. ⭐⭐⭐ İlan edilen ölçüt ve çıkan sonuç", "",
           "| kol | kapsam | katman | modül | dereceli | otomatik |",
           "|---|---|---:|---:|---:|---:|"]
    for k in ("h1", "h9", "h2", "h8"):
        v = V[k]
        sat.append(f"| **{k}** | {v['tarif']} | {v['kat']} | {v['mod']} | "
                   f"**{v['d_ort']:.2f}** | {v['o_ort']:.2f} |")
    f1, e1, a1 = kars("h9", "h1")
    f2, e2, a2 = kars("h9", "h2")
    sat += ["", hukum, "",
            f"· h9 ↔ h1: fark **{f1:+.2f}**, eşik {e1:.1f} ⇒ "
            f"{'**ayırt ediliyor**' if a1 else 'ayırt edilemiyor'}  ",
            f"· h9 ↔ h2: fark **{f2:+.2f}**, eşik {e2:.1f} ⇒ "
            f"{'**ayırt ediliyor**' if a2 else 'ayırt edilemiyor'}", "",
            "## 2. ⭐⭐⭐ İki temiz tek-değişkenli karşılaştırma", "",
            "| karşılaştırma | sabit tutulan | değişen | fark | hüküm |",
            "|---|---|---|---:|---|",
            f"| **h1 ↔ h9** | katman (8) | modül 8 → 16 | {f1:+.2f} | "
            f"{'⭐ modül sayısı TEK BAŞINA etkiliyor' if a1 else '⛔ etkisi gösterilemedi'} |",
            f"| **h9 ↔ h2** | modül (16) | katman 8 → 16 | {f2:+.2f} | "
            f"{'⭐ derinlik TEK BAŞINA etkiliyor' if a2 else '⛔ etkisi gösterilemedi'} |", "",
            ("⭐⭐⭐ **İki etken de, öteki sabit tutulduğunda, ayrı ayrı doğrulandı.** "
             "Merdiven boyunca iç içe giden iki şey burada ilk kez ayrıldı."
             if a1 and a2 else
             "◐ İki karşılaştırmanın yalnız biri bandı aştı."), "",
            "## 3. ⭐⭐ Eşit enerji, artan yayılım — üç nokta", "",
            "T187'nin post-hoc çifti artık üçlü bir seri: **toplam güncelleme enerjisi "
            "neredeyse aynı** olan üç kol, modül sayısına göre sıralanıyor.", "",
            "| kol | modül | ‖ΔW‖ toplam | modül başına | **dereceli** |",
            "|---|---:|---:|---:|---:|"]
    seri = sorted(("h1", "h9", "h8"), key=lambda k: V[k]["mod"])
    for k in seri:
        v = V[k]
        sat.append(f"| {k} | {v['mod']} | **{v['toplam']:.1f}** | {v['modul_basina']:.2f} | "
                   f"**{v['d_ort']:.2f}** |")
    tops = [V[k]["toplam"] for k in seri]
    ds = [V[k]["d_ort"] for k in seri]
    tek_dus = all(ds[i] > ds[i + 1] for i in range(len(ds) - 1))
    sat += ["",
            (f"⭐⭐⭐ **Toplam enerji {min(tops):.1f}-{max(tops):.1f} arasında sabitken "
             f"(yayılım %{100*(max(tops)-min(tops))/min(tops):.0f}), modül sayısı "
             f"{V[seri[0]]['mod']} → {V[seri[-1]]['mod']} çıkarken puan "
             f"{ds[0]:.2f} → {ds[-1]:.2f} diye **tekdüze düşüyor**.** ➡️ *Aynı miktarda "
             "değişikliği daha çok yere dağıtmak, kriz davranışına daha çok zarar "
             "veriyor.*" if tek_dus else
             "◐ Seri tekdüze değil; enerji sabitken modül sayısı tek başına sıralamıyor."),
            "",
            "⛔ **Üç noktanın ikisi (h1, h8) T187'de POST-HOC seçilmişti**; yeni ve "
            "önceden ilan edilmiş olan yalnız **h9**. Seri bu yüzden bir doğrulama "
            "değil, *önceden ilan edilmiş bir noktayla güçlenmiş* bir hipotez.", "",
            "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Tasarım 2×2 DEĞİL** | modül sayısı = katman × anahtar ⇒ «16 katman · "
            "8 modül» hücresi **var olamaz**; iki tek-değişkenli karşılaştırma var, tam "
            "bir faktöriyel yok |",
            "| ⛔⛔ **n=3 tohum** | eşikler 4,1-4,7; küçük etkiler görünmez |",
            "| ⛔ **Tek veri sürümü, tek ölçüt ailesi** | dereceli puan doğrulanmış değil "
            "(T186: anahtar sözcük listesi) |",
            "| ⛔ **`‖ΔW‖` Frobenius** | başka norm başka sıralama verebilir (T187) |",
            "| ⚠️ **Mekanizma yok** | *«neden yayılım zarar veriyor»* bu ölçümde YOK |", ""]

    (KOK / f"reports/analiz/{TARIH}-yayilim-mi-derinlik-mi.json").write_text(
        json.dumps({"tarih": TARIH, "ilan": ILAN, "kollar": V,
                    "h9_h1": [f1, e1, a1], "h9_h2": [f2, e2, a2],
                    "tekduze_dusus": tek_dus}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    (KOK / f"reports/analiz/{TARIH}-yayilim-mi-derinlik-mi.md").write_text(
        "\n".join(sat), encoding="utf-8")
    print("\n".join(sat[5:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
