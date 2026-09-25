#!/usr/bin/env python3
"""Ölçülmüş EĞİTİM gürültüsünü geçmiş kol karşılaştırmalarına uygulamak.

⛔ T182 eğitim gürültüsünü ilk kez doğrudan ölçtü (aynı veri, tohum 7/13/23).
Geçmişteki kol karşılaştırmaları bu taban yokken okundu ⇒ hangi sonuçların
bandın İÇİNDE kaldığı hiç sorulmadı. Bu betik onu sorar.

⛔⛔ **İki ölçüt karıştırılmaz.** T182'nin 2 puanı **otomatik geçen sayısı**
üzerindeydi; oysa T134/T135'in uçurum iddiaları **dereceli yönlendirme puanı**
ile kurulmuştu. Bir ölçütün tabanını başka bir ölçüde uygulamak, bu depoda
defalarca yakalanan hatanın ta kendisidir (K137, K97). ⇒ Taban **her iki ölçüt
için ayrı** hesaplanır ve her geçmiş karşılaştırmaya KENDİ ölçütünün bandı
uygulanır.

⛔⛔⛔ **KAPSAM BAĞIMSIZLIĞI VARSAYIMI — ölçülmedi.** Taban 8 katman / q_proj /
rank 8 kolunda ölçüldü. 16/24/32 katmanlı kolların eğitim gürültüsü daha BÜYÜK
olabilir (daha çok parametre, daha çok rastgelelik). Bu betik bandı yine de
uygular çünkü elde başka taban yok — ama sonuç *«en iyimser bant»* diye okunmalı:
gerçek bant daha genişse, bandın içinde kalan karşılaştırma sayısı ARTAR.

Girdi : reports/analiz/eksen-kosu/*/sonuclar.jsonl
Çıktı : reports/analiz/2026-09-19-gecmis-kollar-bant.{md,json}
"""
from __future__ import annotations

import importlib.util as iu
import itertools
import json
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
EK = KOK / "reports/analiz/eksen-kosu"
_sp = iu.spec_from_file_location("g", KOK / "scripts/analiz/2026-09-17-yonlendirme-derecelendirme.py")
G = iu.module_from_spec(_sp)
_sp.loader.exec_module(G)

TOHUM = {7: "j-safety_crisis-v014-k8", 13: "k-v014-k8-t13-safety", 23: "l-v014-k8-t23-safety"}
TOHUM_E3 = {7: "e3-forgetting_smoke-v014-k8", 13: "k-v014-k8-t13-forget",
            23: "l-v014-k8-t23-forget"}

# Geçmiş aileler — her biri KENDİ İÇİNDE karşılaştırılmıştı
AILE = {
    "kapsam merdiveni (h · 09-17)": [
        ("h1 · 8 kat q", "h-safety_crisis-h1-capa-k8"),
        ("h2 · 16 kat q", "h-safety_crisis-h2-k16"),
        ("h3 · 24 kat q", "h-safety_crisis-h3-k24"),
        ("h4 · 32 kat q", "h-safety_crisis-h4-k32"),
        ("h5 · 16 kat q+o", "h-safety_crisis-h5-k16-qo"),
        ("h6 · 24 kat q+o", "h-safety_crisis-h6-k24-qo"),
        ("h7 · 24 kat q+o r16", "h-safety_crisis-h7-k24-qo-r16")],
    "uçurum (u · 09-17)": [
        ("8 katman", "h-safety_crisis-h1-capa-k8"),
        ("10 katman", "u-safety_crisis-u-k10"),
        ("12 katman", "u-safety_crisis-u-k12"),
        ("13 katman", "u-safety_crisis-u-k13"),
        ("14 katman", "u-safety_crisis-u-k14"),
        ("16 katman", "h-safety_crisis-h2-k16")],
    "katman 29 (p · 09-17)": [
        ("13 kat · 29 YOK", "p-safety_crisis-p-atla29"),
        ("12 kat · 29 VAR", "p-safety_crisis-p-sadece29")],
    "ilan seyreltme (ka · 09-17)": [
        ("A · ilan seyreltilmiş", "ka-safety_crisis-ka-A-ilan-seyreltilmis"),
        ("P · plasebo", "ka-safety_crisis-ka-P-plasebo")],
    "epok/adım (g1 · 09-16)": [
        ("v006 3 epok", "g1-safety_crisis-v006-3epoch"),
        ("v006 adım sabit", "g1-safety_crisis-v006-adimsabit"),
        ("v005 referans", "g1-safety_crisis-v005-referans")],
    "veri sürümü (09-18/19)": [
        ("v0.0.8 (h1)", "h-safety_crisis-h1-capa-k8"),
        ("v0.0.10", "i-safety_crisis-v010-k8"),
        ("v0.0.14", "j-safety_crisis-v014-k8")],
}


def _son(et):
    e = [p for p in EK.iterdir() if p.name.endswith(et)]
    return sorted(e)[-1] if e else None


def _rows(et):
    d = _son(et)
    return None if d is None else [json.loads(s) for s in
        (d / "sonuclar.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]


def main() -> int:
    kabul = G._kabul()
    kriz = {r["id"] for r in _rows(TOHUM[7]) if r.get("kutup") == "kriz"}

    def otomatik(et):
        r = _rows(et)
        return None if r is None else sum(1 for x in r if x.get("otomatik_gecti"))

    def dereceli(et):
        r = _rows(et)
        if r is None:
            return None
        return sum(G.derece(x["cevap"], kabul) for x in r if x["id"] in kriz)

    t_oto = {t: otomatik(p) for t, p in TOHUM.items()}
    t_der = {t: dereceli(p) for t, p in TOHUM.items()}
    t_e3 = {t: otomatik(p) for t, p in TOHUM_E3.items()}
    B_OTO = max(t_oto.values()) - min(t_oto.values())
    B_DER = max(t_der.values()) - min(t_der.values())
    B_E3 = max(t_e3.values()) - min(t_e3.values())

    sat = ["# Geçmiş kol karşılaştırmaları, ölçülmüş eğitim gürültüsüne karşı", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           "**Taban:** aynı veri (`v0.0.14`), aynı bölme, yalnız `mlx.seed` 7/13/23 (T182)", "",
           "## 1. ⭐⭐ Üç ölçüt, üç ayrı bant", "",
           "| ölçüt | tohum 7 | 13 | 23 | **bant** |", "|---|---:|---:|---:|---:|",
           f"| E2 otomatik geçen (/20) | {t_oto[7]} | {t_oto[13]} | {t_oto[23]} | **±{B_OTO}** |",
           f"| E2 dereceli yönlendirme (kriz öğeleri) | {t_der[7]} | {t_der[13]} | {t_der[23]} | "
           f"**±{B_DER}** |",
           f"| E3 otomatik geçen (/30) | {t_e3[7]} | {t_e3[13]} | {t_e3[23]} | **±{B_E3}** |", "",
           "⛔⛔ **İki ölçüt karıştırılmaz.** T134/T135'in uçurum iddiaları **dereceli** "
           f"puanla kurulmuştu ⇒ onlara ±{B_DER} uygulanır, ±{B_OTO} değil.", "",
           "⛔⛔⛔ **Kapsam bağımsızlığı VARSAYIM:** taban 8 katman kolunda ölçüldü; "
           "16-32 katmanlı kolların gürültüsü daha büyük olabilir ⇒ bu **en iyimser "
           "bant**. Gerçek bant genişse, içinde kalan karşılaştırma sayısı **artar**.", ""]

    ozet = {}
    for aile, kollar in AILE.items():
        oto = {ad: otomatik(p) for ad, p in kollar}
        der = {ad: dereceli(p) for ad, p in kollar}
        var = [(a, b) for a, b in itertools.combinations([a for a, _ in kollar], 2)
               if oto[a] is not None and oto[b] is not None]
        icinde_o = [(a, b) for a, b in var if abs(oto[a] - oto[b]) <= B_OTO]
        icinde_d = [(a, b) for a, b in var if abs(der[a] - der[b]) <= B_DER]
        ozet[aile] = {"n_cift": len(var), "bant_ici_otomatik": len(icinde_o),
                      "bant_ici_dereceli": len(icinde_d),
                      "otomatik": oto, "dereceli": der}
        sat += [f"## {aile}", "", "| kol | otomatik /20 | dereceli (kriz) |", "|---|---:|---:|"]
        sat += [f"| {ad} | {oto[ad]} | {der[ad]} |" for ad, _ in kollar]
        sat += ["",
                f"İkili karşılaştırma **{len(var)}** · bandın İÇİNDE kalan: "
                f"otomatik **{len(icinde_o)}/{len(var)}** · dereceli "
                f"**{len(icinde_d)}/{len(var)}**", ""]
        ayirt_o = [(a, b) for a, b in var if abs(oto[a] - oto[b]) > B_OTO]
        if ayirt_o:
            sat += ["⭐ Otomatik ölçütte bandı AŞAN (yorumlanabilir) çiftler: "
                    + " · ".join(f"**{a}↔{b}** ({abs(oto[a]-oto[b])})" for a, b in ayirt_o), ""]
        else:
            sat += ["⛔⛔ **Bu ailede otomatik ölçütte bandı aşan TEK bir çift bile yok** ⇒ "
                    "kollar arası hiçbir sıralama bu ölçütle okunamaz.", ""]

    # ⭐ Asıl çıktı: hangi KAYITLI iddia ayakta kalıyor. Her satır bir defter/bellek
    # maddesinin dayandığı ÇİFTİ ve o çiftin farkını kendi ölçütünün bandına karşı
    # okur. ⛔ İddia metinleri elle eşleştirildi (Kural 7'nin zayıf halkası).
    IDDIA = [
        ("T135 · «uçurum 12 ile 14 katman arasında»", "uçurum (u · 09-17)",
         "12 katman", "13 katman", "dereceli", "fark"),
        ("T134/T135 · «8 ↔ 16 arasında çöküş»", "uçurum (u · 09-17)",
         "8 katman", "16 katman", "dereceli", "fark"),
        ("uçurum ara nokta · «10 ile 12 farklı»", "uçurum (u · 09-17)",
         "10 katman", "12 katman", "dereceli", "fark"),
        ("«h1 iki Pareto kapısını da geçen tek kol»", "kapsam merdiveni (h · 09-17)",
         "h1 · 8 kat q", "h7 · 24 kat q+o r16", "otomatik", "fark"),
        ("h-ailesi · «h6 h5'ten iyi»", "kapsam merdiveni (h · 09-17)",
         "h5 · 16 kat q+o", "h6 · 24 kat q+o", "otomatik", "fark"),
        ("T-katman29 · «29 atlamak 29'u tek başına almaktan iyi»", "katman 29 (p · 09-17)",
         "13 kat · 29 YOK", "12 kat · 29 VAR", "dereceli", "fark"),
        ("ka · «ilan seyreltmek plasebodan farklı»", "ilan seyreltme (ka · 09-17)",
         "A · ilan seyreltilmiş", "P · plasebo", "dereceli", "fark"),
        ("g1 · «3 epok adım-sabitten iyi»", "epok/adım (g1 · 09-16)",
         "v006 3 epok", "v006 adım sabit", "otomatik", "fark"),
        ("g1 · «v006 v005'ten iyi»", "epok/adım (g1 · 09-16)",
         "v006 3 epok", "v005 referans", "dereceli", "fark"),
        ("T181 · «v0.0.14 v0.0.10'a göre gerilemedi»", "veri sürümü (09-18/19)",
         "v0.0.10", "v0.0.14", "otomatik", "yokluk"),
    ]
    sat += ["## ⭐⭐⭐ Hangi kayıtlı iddia ayakta", "",
            "| iddia | tür | ölçüt | fark | bant | hüküm |",
            "|---|---|---|---:|---:|---|"]
    hukumler = {}
    # ⭐⭐ İki iddia TÜRÜ ayrılır ve bant ikisine TERS yönde uygulanır:
    #  · «fark» iddiası (X, Y'den iyi): bandın İÇİNDE kalırsa GÖSTERİLEMEZ.
    #  · «yokluk» iddiası (gerileme yok): bandın içinde kalması iddiayı ÇÜRÜTMEZ —
    #    onu destekler, ama bir TESPİT SINIRI ile: bant kadar bir gerileme
    #    var olabilir ve görünmezdi.
    # ➡️ *Aynı sayı, iddianın yönüne göre kanıt da olur sınır da.*
    for ad, aile, a, b, olcut, tip in IDDIA:
        o = ozet[aile]["otomatik" if olcut == "otomatik" else "dereceli"]
        bant = B_OTO if olcut == "otomatik" else B_DER
        if o.get(a) is None or o.get(b) is None:
            sat.append(f"| {ad} | {tip} | {olcut} | — | ±{bant} | ⛔ koşu eksik |")
            continue
        d = abs(o[a] - o[b])
        if tip == "yokluk":
            hk = (f"⭐ **ayakta** — ama tespit sınırı ±{bant}: bu kadar gerileme "
                  "var olabilir ve görünmezdi" if d <= bant else
                  "⛔⛔ **çürüdü** — bandı aşan bir fark var")
            tamam = d <= bant
        else:
            hk = ("⭐ **ayakta** — bandı aşıyor" if d > bant else
                  "⛔⛔ **gösterilemez** — bandın içinde")
            tamam = d > bant
        hukumler[ad] = {"tip": tip, "fark": d, "bant": bant, "ayakta": tamam}
        sat.append(f"| {ad} | {tip} | {olcut} | **{d}** | ±{bant} | {hk} |")
    ayakta = sum(1 for v in hukumler.values() if v["ayakta"])
    sat += ["",
            f"⭐⭐ **{ayakta}/{len(hukumler)} iddia ayakta kalıyor.** ➡️ *Bir ölçütün "
            "gürültü tabanı ölçülene kadar, ondan çıkarılan her sıralama bir iddia "
            "değil bir ihtimaldir — ve bu depoda o taban 09-19'a kadar ölçülmemişti.*", "",
            "⛔⛔ **«Okunamaz» ≠ «yanlış».** Bandın içinde kalan bir fark yanlış olduğunu "
            "değil, bu ölçütle **gösterilemediğini** söyler. Ayırt etmek için ya ölçüt "
            "keskinleştirilmeli ya kol başına birkaç tohum koşulmalı (ortalama bandı "
            "√n ile daraltır).", "",
            "⛔ **İddia metinleri elle eşleştirildi** — hangi defter maddesinin hangi "
            "çifte dayandığı otomatik çıkarılmadı (Kural 7'nin zayıf halkası).", ""]

    (KOK / f"reports/analiz/{TARIH}-gecmis-kollar-bant.json").write_text(
        json.dumps({"tarih": TARIH, "bant": {"otomatik": B_OTO, "dereceli": B_DER, "e3": B_E3},
                    "tohum": {"otomatik": t_oto, "dereceli": t_der, "e3": t_e3},
                    "aileler": ozet, "iddia_hukumleri": hukumler},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    (KOK / f"reports/analiz/{TARIH}-gecmis-kollar-bant.md").write_text("\n".join(sat),
                                                                       encoding="utf-8")
    print("\n".join(sat[4:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
