#!/usr/bin/env python3
"""Alıntıda edat düşmesi — yayımlanmış setteki 21 bulgu elle okundu.

⛔ **Neden.** Alıntı birebirlik kapısı `datasets/v0.0.11`de **21 bulgu** veriyordu
ve hiçbiri elle okunmamıştı — T155'in *«%26 kusur»* çıkardığı yığınla aynı biçim.

⭐ **Okundu ve ikiye ayrıldı.** Her bulgu için kullanıcının metnindeki EN YAKIN
parça `difflib` ile bulundu; benzerlik oranı sınıfı verdi:

  · **5 vuruş yanlış pozitifti** — üçü yeni ANMA çerçevesi, kapıya eklendi:
    olumsuz yeterlilik (*«ben "olur" DİYEMEM»*) · ulaç (*«"iyi olur" DİYEREK …
    almayacağım»*) · karşılaştırma (*«"Bir şey olmadı" İLE "olmaz" AYNI ŞEY
    DEĞİL»*). ⇒ 21 → **16**.
  · **Kalan 16'sı tek bir örüntü:** model alıntılarken Türkçenin **«de/da»
    edatını** ve hedge öbeklerini (*«biraz»*, *«aslında»*, *«bunu»*, *«ben»*)
    **düşürüyor**.

➡️⭐⭐⭐ *Bu bir «yanlış alıntı» değil, bir ÜSLUP: alıntı kısaltılırken cümlenin
vurgusunu taşıyan öge atılıyor. «içim DE bir tuhaf» ile «içim bir tuhaf» aynı şeyi
söylemez — «de» başka bir şeyin daha olduğunu ima eder ve alıntıdan silinince
kullanıcının söylediğinden BAŞKA bir cümle tırnak içine alınmış olur.*

⛔⛔ Biri daha ağır: *«icra dosyasına bir nefes olur, kimsenin haberi olmaz»* —
kullanıcı *«…bir nefes olur, EŞİM DUYMAZ, kimsenin haberi…»* yazmış ⇒ alıntı
**ortadaki bir yan cümleyi atıp iki ucu bitiştiriyor**. T104'ün özgün kırpma
kusuru.

Girdi : datasets/v0.0.11/train.jsonl
Çıktı : reports/analiz/2026-09-18-alinti-edat-dusmesi.md
Kullanım: uv run python scripts/analiz/2026-09-18-alinti-edat-dusmesi.py
"""
from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-alinti-edat-dusmesi.md"
SET = KOK / "datasets/v0.0.11/train.jsonl"
BULGU = KOK / "reports/analiz/2026-09-17-alinti-birebirlik-v0.0.11-train.json"

from tohum_guvenlik import tr_fold  # noqa: E402

BLOK = r"\[BAĞLAM.*?(?=\n|$)|---\s*KAYNAK.*?KAYNAK SONU\s*---"


def main() -> int:
    d = json.loads(BULGU.read_text(encoding="utf-8"))
    kayitlar = [json.loads(s) for s in SET.read_text(encoding="utf-8").splitlines() if s.strip()]
    satirlar = []
    for b in d["bulgu"]:
        al = b["alinti"]
        for r in kayitlar:
            cev = " ".join(m.get("content") or "" for m in r["messages"] if m["role"] == "assistant")
            if ('"' + al + '"') not in cev:
                continue
            kul = re.sub(BLOK, " ", " ".join(m.get("content") or "" for m in r["messages"]
                                             if m["role"] == "user"), flags=re.S)
            n = len(al.split())
            w = kul.split()
            aday = [" ".join(w[i:i + n + 2]) for i in range(max(1, len(w) - n))]
            en = max(aday, key=lambda x: difflib.SequenceMatcher(
                None, tr_fold(al), tr_fold(x)).ratio()) if aday else ""
            oran = difflib.SequenceMatcher(None, tr_fold(al), tr_fold(en)).ratio()
            # düşen sözcükler
            a_k, e_k = tr_fold(al).split(), tr_fold(en).split()
            dusen = [x for x in e_k if x not in a_k]
            satirlar.append({"id": r["id"], "alinti": al, "kullanici": en,
                             "oran": round(oran, 2), "dusen": dusen})
            break

    sat = ["# Alıntıda edat düşmesi — 21 bulgu elle okundu", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Girdi:** `{SET.relative_to(KOK)}` · bulgu **{len(d['bulgu'])}**", "",
           "⭐ Üç yeni ANMA çerçevesi kapıya eklendikten sonra 21 → **16**; kalan 16'sı",
           "tek bir örüntü. Her bulgu için kullanıcının en yakın parçası `difflib` ile",
           "bulundu.", "",
           "| benzerlik | alıntı | kullanıcının yazdığı | düşen |",
           "|---:|---|---|---|"]
    for x in sorted(satirlar, key=lambda y: -y["oran"]):
        sat.append(f"| {x['oran']:.2f} | *«{x['alinti'][:42]}»* | "
                   f"*«{x['kullanici'][:48]}»* | `{', '.join(x['dusen'][:4]) or '—'}` |")
    edat = [x for x in satirlar if any(t in ("de", "da") for t in x["dusen"])]
    sat += ["", f"⭐⭐ **{len(edat)} bulguda düşen şey Türkçenin «de/da» edatı.**", "",
            "➡️⭐⭐⭐ *Bu bir «yanlış alıntı» değil, bir ÜSLUP: alıntı kısaltılırken cümlenin",
            "vurgusunu taşıyan öge atılıyor. «içim DE bir tuhaf» ile «içim bir tuhaf» aynı şeyi",
            "söylemez — «de» başka bir şeyin daha olduğunu ima eder ve alıntıdan silinince",
            "kullanıcının söylediğinden BAŞKA bir cümle tırnak içine alınmış olur.*", "",
            "## ⛔⛔ Biri daha ağır — yan cümle elenmiş", "",
            "*«icra dosyasına bir nefes olur, kimsenin haberi olmaz»* — kullanıcı",
            "*«…bir nefes olur, **eşim duymaz**, kimsenin haberi…»* yazmış ⇒ alıntı ortadaki",
            "yan cümleyi atıp iki ucu **bitiştiriyor**. Bu T104'ün özgün kırpma kusurudur ve",
            "öteki on beşten farklı bir sınıftır.", "",
            "## ⛔ Bu okumanın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **Hiçbiri düzeltilmedi** | `datasets/` IMMUTABLE ⇒ 16 kayıt bir sonraki "
            "derlemenin kalemi. Düzeltme ölçütü verilebilir: düzeltmeden sonra kapı o kayıtlar "
            "için **0** demeli |",
            "| ⛔ **Benzerlik bir SINIF değil** | `difflib` oranı bir sezgidir; hangi düşmenin "
            "anlamı değiştirdiğine **elle okuma** karar verdi |",
            "| ⛔ **Anma çerçevesi listesi kapanmıyor** | üç biçim daha eklendi ve her biri "
            "ancak elle okumayla görüldü ⇒ kapı bu sınıfta hep bir adım geride |",
            "| ⚠️ Kullanıcının «en yakın parçası» pencere kaydırarak bulundu | yanlış hizalama "
            "olabilir; oran düşükse tablo yanıltır |", ""]
    (KOK / f"reports/analiz/{TARIH}-alinti-edat-dusmesi.json").write_text(
        json.dumps({"tarih": TARIH, "bulgu": satirlar, "edat_dusen": len(edat)},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[4:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
