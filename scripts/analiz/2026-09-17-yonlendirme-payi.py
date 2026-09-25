#!/usr/bin/env python3
"""Eğitim verisi, MODELİ ölçen aracın KENDİSİYLE ölçülür.

⛔⛔ **Neden.** İki kapsam taraması ince ayarlı modelin `safety_crisis`'te
yönlendirmeyi adlandırmayı bıraktığını gösterdi. Açıklama olarak *«veride
yönlendirme hamlesi az»* önerilmişti (K109/T26: v0.0.2'de **0** kayıt,
v0.0.3'te **5**). Ama o sayım **başka bir ölçütle** yapıldı.

➡️⭐ *Bir modelin bir davranışı yapmadığını X aracıyla ölçüp, verinin o
davranışı içerdiğini Y aracıyla ölçmek karşılaştırma değildir. Veri ile model
aynı terazide tartılmalı; yoksa «veride var ama model yapmıyor» cümlesi iki
farklı «var»ı karşılaştırır.*

⇒ Burada `evals/safety_crisis.duzeltilmis.jsonl`'in **kabul listesi** eğitim
verisinin asistan cevaplarına uygulanıyor — eval'in sorduğu soru birebir.

⚠️ Bu bir ÜST SINIRDIR: kabul listesi sözcük arar, hamlenin yerinde olup
olmadığını sormaz. ⚠️ Eval kriz bağlamında soruyor; eğitim verisinde kriz
dilimi YOK (Kural 3) ⇒ iki dağılım aynı değil ve bu fark kapatılamıyor.
"""
from __future__ import annotations
import json
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / "reports/analiz/2026-09-17-yonlendirme-payi.md"
SET2 = KOK / "evals/safety_crisis.duzeltilmis.jsonl"


def _kabul_listesi() -> list[str]:
    """Eval'in KENDİ kabul listesi — kopyalanmıyor, setten okunuyor."""
    for s in SET2.read_text(encoding="utf-8").splitlines():
        if not s.strip():
            continue
        for i in json.loads(s)["iddialar"]:
            if i.get("amac") == "yonlendirme" and i.get("kural") == "herhangi_biri":
                return i["deger"]
    raise SystemExit("⛔ kabul listesi bulunamadı")


def main() -> int:
    import sys
    sys.path.insert(0, str(KOK / "src"))
    import smoke_checks as sc
    kabul = _kabul_listesi()
    iddia = {"tip": "otomatik", "kural": "herhangi_biri", "deger": kabul}

    sat = ["# Yönlendirme payı — eğitim verisi, EVAL'İN ARACIYLA ölçüldü", "",
           "**Betik:** `scripts/analiz/2026-09-17-yonlendirme-payi.py` · **Tarih:** 2026-09-17", "",
           f"**Ölçüt:** `evals/safety_crisis.duzeltilmis.jsonl`'in kabul listesi "
           f"({len(kabul)} terim) — kopyalanmadı, **setten okundu**.", "",
           "| sürüm | kayıt | **yönlendirme adlandıran** | oran |", "|---|---:|---:|---:|"]
    veriler = {}
    for v in ("v0.0.2", "v0.0.3", "v0.0.5", "v0.0.6", "v0.0.7", "v0.0.8"):
        p = KOK / f"datasets/{v}/train.jsonl"
        if not p.exists():
            continue
        rs = [json.loads(s) for s in p.read_text(encoding="utf-8").splitlines() if s.strip()]
        n = 0
        for r in rs:
            son = [m for m in r["messages"] if m["role"] == "assistant" and m.get("content")]
            if son and sc.denetle(iddia, son[-1]["content"])[0]:
                n += 1
        veriler[v] = (len(rs), n)
        sat.append(f"| `{v}` | {len(rs)} | **{n}** | %{100*n/len(rs):.1f} |")

    a = veriler.get("v0.0.5"); b = veriler.get("v0.0.8")
    sat += ["", "## ⭐ Karşılaştırma noktası", ""]
    if a and b:
        sat += [f"Kapsam taraması `v0.0.5` üzerinde koştu: **{a[1]}/{a[0]}** kayıt "
                f"(%{100*a[1]/a[0]:.1f}) yönlendirmeyi adlandırıyordu.",
                f"Üçüncü tarama `v0.0.8` üzerinde: **{b[1]}/{b[0]}** (%{100*b[1]/b[0]:.1f}).", "",
                f"➡️ Mutlak sayı **{b[1]/a[1]:.1f} kat** arttı, oran "
                f"**%{100*a[1]/a[0]:.1f} → %{100*b[1]/b[0]:.1f}**.", "",
                "⭐ **Bu sayı üçüncü taramanın yorumunu belirler:** kollar yine elenirse, "
                "*«veride yönlendirme az»* açıklaması bu artışla birlikte **zayıflar** ve "
                "sıradaki aday veri MİKTARI değil, ya verinin BİÇİMİ ya da ölçütün kendisi olur."]
    v2 = veriler.get("v0.0.2")
    sat += ["", "## ⛔⛔ VE ÖLÇÜM KENDİ GEREKÇESİNİ DOĞRULADI: İKİ ARAÇ ÇELİŞİYOR", ""]
    if v2:
        sat += [f"K109/T26 şunu yazmıştı: *«v0.0.2'de yönlendirme HAMLESİ **0** kayıttaydı»*.",
                f"Eval'in kendi aracıyla aynı korpusta **{v2[1]} kayıt** (%{100*v2[1]/v2[0]:.1f}) çıkıyor.", "",
                "⛔ İki sayı da yanlış değil — **aynı şeyi ölçmüyorlar**. «Hamle» dar bir "
                "tanım (izin isteme + kaynak türü + ilk adım, §8b'nin biçimi); kabul listesi "
                "ise yalnız bir **kaynak türü sözcüğü** arıyor.", "",
                "➡️⭐⭐ *Ve ince ayarlı modeli eleyen kapı, dar tanımı değil GENİŞ olanı "
                "kullanıyor: `safety_crisis` bir kaynak türü sözcüğü arıyor. Yani "
                "«veride hamle yok» gerekçesi, modelin elendiği ölçütle hiç "
                "karşılaştırılmamış. Veri ile model üç taramadır **ayrı terazilerde** "
                "tartılıyor.*", "",
                "⚠️ Bu, önceki taramaların sonucunu geçersiz kılmaz — onlar modeli doğru "
                "ölçtü. Geçersiz olan, sonuca verilen **açıklama**."]
    sat += ["", "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **Üst sınır** | kabul listesi SÖZCÜK arar; hamlenin yerinde olup olmadığını sormaz |",
            "| ⛔ **Dağılım eşleşmiyor** | eval KRİZ bağlamında soruyor, eğitim verisinde kriz dilimi YOK (Kural 3) ⇒ iki dağılım aynı değil ve bu fark kapatılamıyor |",
            "| ⛔ **Nedensellik yok** | veride payın artması modelin davranışını açıklamaz; yalnız bir açıklamayı zayıflatır |",
            "| ⚠️ Yalnız SON asistan turu taranıyor | ara turlardaki yönlendirme sayılmıyor |",
            "| ⛔ **«Hamle» sayımı yeniden yapılmadı** | K109'un dar tanımıyla v0.0.8'de kaç kayıt olduğu ölçülmedi; burada yalnız İKİ ARACIN ayrıştığı gösterildi |", ""]
    CIKTI.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[4:]))
    print(f"→ {CIKTI.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
