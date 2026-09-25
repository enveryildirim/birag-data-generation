#!/usr/bin/env python3
"""Korpusun v4 ve v6 rubrikleriyle puanları — v6 bizim yazdığımızda ne buluyor?

golden koşusu **baseline modelin** cevaplarını puanlıyordu. Bu betik **bizim elle
yazdığımız** kayıtları puanlıyor ve soru farklı: korpusu tam da bu tuzaklardan
kaçınarak yazdık; v6 yine de bir şey buluyorsa bu bir **korpus bulgusudur**, judge
bulgusu değil.

⚠️ v4 ve v6 puanları karşılaştırılabilir DEĞİL (aynı kayda farklı sayı verirler).
Karşılaştırılan şey, v6'nın gördüğü ve v4'ün göremediği DAVRANIŞLAR.

Kullanım: uv run python scripts/analiz/2026-09-15-korpus-v4-v6.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import statistics as st
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
RAPOR = KOK / "reports/analiz/2026-09-15-korpus-v4-v6.md"

# (ad, v4 dosyaları, v6 dosyası)
KORPUSLAR = [
    ("BıRAG v3 (104)", ["data/judged/v3-parti1.jsonl", "data/judged/v3-parti2-tam.jsonl",
                        "data/judged/v3-parti3.jsonl"], "data/judged/v3-kumulatif.v6.jsonl"),
    ("expert-70", ["data/judged/expert-70.v4.jsonl"], "data/judged/expert-70.v6.jsonl"),
    ("v0.0.1 pilot", ["data/judged/v0.0.1.jsonl"], "data/judged/v0.0.1.v6.jsonl"),
]
HEDEF = ["klinik_guvenlik_ihlali", "bos_guvence", "rol_siniri_ihlali",
         "tuzak_suclama", "tuzak_etiketleme"]
ALINTI = {"klinik_guvenlik_ihlali": ("guvenlige_en_yakin", "guvenlik_tipi"),
          "bos_guvence": ("en_teselli_edici", "teselli_kalip"),
          "rol_siniri_ihlali": ("rol_sinirina_en_yakin", "rol_alani"),
          "tuzak_suclama": ("sorumluluga_en_yakin", "kusur_kullanicida_ima"),
          "tuzak_etiketleme": ("kisiye_dair_en_genel", "genelleme_kategori_mi")}


def yukle(yollar: list[str]) -> dict[str, dict]:
    kayit = {}
    for y in yollar:
        yol = KOK / y
        if not yol.exists():
            continue
        for l in open(yol):
            r = json.loads(l)
            if r.get("judge"):
                kayit[r["id"]] = r
    return kayit


def main() -> None:
    L = ["# Korpus: v4 → v6 rubriği", "",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}",
         "", "---", "",
         "## 0. Bu neden golden koşusundan farklı bir soru", "",
         "golden koşusu **baseline modelin** cevaplarını puanlıyordu; orada bir ihlal "
         "bulmak beklenir. Burada puanlanan kayıtlar **bizim elle yazdıklarımız** ve tam "
         "da bu tuzaklardan kaçınmak için yazıldılar. v6 yine de bir şey buluyorsa bu bir "
         "**korpus bulgusudur**, judge bulgusu değil.", "",
         "⚠️ v4 ve v6 puanları karşılaştırılabilir değil; karşılaştırılan şey v6'nın "
         "gördüğü ve v4'ün göremediği **davranışlar**.", ""]

    tum_yeni = []
    for ad, v4_yollar, v6_yol in KORPUSLAR:
        a, b = yukle(v4_yollar), yukle([v6_yol])
        ortak = sorted(set(a) & set(b))
        if not ortak:
            L += [f"## {ad}", "", "_v6 dosyası yok ya da ortak kayıt bulunamadı._", ""]
            continue
        sha = hashlib.sha256((KOK / v6_yol).read_bytes()).hexdigest()[:16]
        L += [f"## {ad}", "",
              f"**v6 çıktısı:** `{v6_yol}` · SHA256 `{sha}…` · **ortak kayıt:** {len(ortak)}", "",
              "| Boyut | v4 ateşleyen | v6 ateşleyen |", "|---|---:|---:|"]
        for alan in HEDEF:
            ka = sum(1 for i in ortak if a[i]["judge"].get(alan) is True)
            kb = sum(1 for i in ortak if b[i]["judge"].get(alan) is True)
            isaret = " ⚠️" if kb > ka else ""
            L.append(f"| `{alan}` | {ka} | {kb}{isaret} |")

        # türetilmiş puanlar
        L += ["", "| Türetilmiş puan | v4 ort | v6 ort |", "|---|---:|---:|"]
        for alan in ("anlasilirlik", "dogallik", "mi_uyumu", "grounding"):
            va = [a[i]["judge"][alan] for i in ortak if a[i]["judge"].get(alan) is not None]
            vb = [b[i]["judge"][alan] for i in ortak if b[i]["judge"].get(alan) is not None]
            if va and vb:
                L.append(f"| `{alan}` | {st.mean(va):.2f} | {st.mean(vb):.2f} |")

        # v6'nın yeni yakaladıkları — kanıtla
        yeni = []
        for i in ortak:
            for alan in HEDEF:
                if b[i]["judge"].get(alan) is True and a[i]["judge"].get(alan) is not True:
                    al_alan, karar_alan = ALINTI[alan]
                    yeni.append((i, alan, (b[i]["judge"].get(al_alan) or "")[:95],
                                 b[i]["judge"].get(karar_alan)))
        tum_yeni += [(ad, *y) for y in yeni]
        L += ["", f"### v6'nın yeni işaretledikleri — {len(yeni)} kayıt", ""]
        if yeni:
            L += ["> Bunlar **bizim yazdığımız** cümleler. Kanıt judge'ın çıkardığı metin; "
                  "klinik nitelikteki karar uzmana aittir (Kural 3).", "",
                  "| Kayıt | Boyut | Karar | Alıntı |", "|---|---|---|---|"]
            for i, alan, al, karar in yeni:
                L.append(f"| `{i[:12]}` | `{alan}` | `{karar}` | «{al.replace('|', '·')}» |")
        else:
            L += ["_Yok — v6 bu korpusta v4'ün kaçırdığı hiçbir ihlal bulmadı._"]
        L += [""]

    L += ["## Okuma", ""]
    if tum_yeni:
        sayim = collections.Counter(alan for _, _, alan, _, _ in tum_yeni)
        L += [f"- v6, üç korpusta toplam **{len(tum_yeni)}** yeni işaret koydu: "
              + ", ".join(f"`{k}`×{v}" for k, v in sayim.most_common()) + ".",
              "- Bunlar elle yazılmış kayıtlar; her işaret ya **gerçek bir korpus kusuru** "
              "ya da **judge'ın yanlış pozitifi**. Ayrımı yukarıdaki alıntılar gösterir ve "
              "klinik nitelikte olanlar uzmana gider.",
              "- ⚠️ Bir işaret doğrulanırsa ilgili kayıt **silinmez**, karantinaya alınır "
              "(K76 deseni): `data/guvenlik-karantinasi.jsonl`."]
    else:
        L += ["- v6 hiçbir korpusta yeni ihlal bulmadı. Bu, korpusun bu beş boyutta "
              "temiz yazıldığının kanıtıdır — ve golden koşusunda baseline modelin "
              "işaret aldığı yerlerde bizim kayıtlarımızın almaması **beklenen** sonuçtur."]
    L += [""]
    RAPOR.write_text("\n".join(L) + "\n")
    print(f"yeni işaret: {len(tum_yeni)} · yazıldı: {RAPOR.relative_to(KOK)}")


if __name__ == "__main__":
    main()
