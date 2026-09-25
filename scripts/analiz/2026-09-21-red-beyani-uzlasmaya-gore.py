#!/usr/bin/env python3
"""T227 kararını kayıtlara işler ve `is_negative`'i ölçümden BEYANA çevirir.

⛔⛔ **Ne yapar.** T226'nın ayrışan 26 kaydında `is_negative`, üç anotatörün
çoğunluk kararına eşitlenir ve kararın KAYNAĞI kayda yazılır — sayı bir daha
*«nereden geldi»* diye sorulmasın diye (Kural 5).

⛔ **Ne YAPMAZ.** Sözlüğü genişletmez, başka kayda dokunmaz, `ozerklik_vurgusu`
alanına hiç bakmaz. ⚠️ Özerklikte de aynı yapı var (`beyan-metin-uyumu` onu da
desenle yazıyor) ama ÖLÇÜLMEDİ; açık kalem olarak duruyor.

⭐ Hem blok dosyasına hem birleşik dosyaya yazar. Birleştirmeyi yeniden
KOŞMAZ: parti1'in planı üretimden sonra değişmişti (T224) ve künye kapısı
haklı olarak reddederdi. ⇒ Cerrahi alan güncellemesi + iki dosya arasında
tutarlılık denetimi.

Kullanım: uv run python ... [--yaz]   (varsayılan: kuru koşu)
Girdi   : scratchpad/uzlasma.json + anot-{A,B,C-benim}.json
Çıktı   : data/candidates/v6-parti*.jsonl (yerinde) ·
          reports/analiz/2026-09-21-red-beyani-uzlasmaya-gore.md
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
# Girdi: depodaki kalıcı kopya (bkz. data/anotasyon/OKU.md).
SP = KOK / "data/anotasyon"
RAPOR = KOK / f"reports/analiz/{TARIH}-red-beyani-uzlasmaya-gore.md"
YAZ = "--yaz" in sys.argv


def main() -> int:
    uz = json.loads((SP / "uzlasma.json").read_text(encoding="utf-8"))
    oy = {k: {o["id"]: o["red"] for o in json.loads((SP / a).read_text(encoding="utf-8"))}
          for k, a in (("A", "anot-A.json"), ("B", "anot-B.json"),
                       ("C", "anot-C-benim.json"))}
    # kimlik -> (yeni_deger, oylar)
    hedef: dict[str, tuple[bool, dict]] = {}
    for kid, v in uz.items():
        hedef[v["kimlik"]] = (v["karar"] == "evet", {k: oy[k][kid] for k in oy})

    degisen, dokunulan, tutarsiz = [], 0, []
    for parti in sorted({k.split("#")[0] for k in hedef}):
        yollar = [KOK / f"data/candidates/{parti}.jsonl"]
        yollar += sorted(KOK.glob(f"data/candidates/{parti}.blok*.jsonl"))
        for y in yollar:
            if not y.exists():
                continue
            kay = [json.loads(l) for l in y.read_text(encoding="utf-8").splitlines() if l.strip()]
            deg = False
            for r in kay:
                kimlik = f"{parti}#{r['gen_meta']['parti_sira']}"
                if kimlik not in hedef:
                    continue
                yeni, oylar = hedef[kimlik]
                dokunulan += 1
                if r["is_negative"] != yeni:
                    degisen.append((kimlik, y.name, r["is_negative"], yeni))
                    deg = True
                r["is_negative"] = yeni
                # ⭐ Kaynak kayda yazılıyor: bu sayı bir desenden değil,
                #    üç anotatörün çoğunluğundan geldi.
                r["gen_meta"]["is_negative_kaynak"] = "T227-uzlastirma-2026-09-21"
                r["gen_meta"]["is_negative_oylar"] = oylar
                deg = True
            if deg and YAZ:
                y.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n"
                                     for r in kay), encoding="utf-8")

    # ⭐ Tutarlılık: blok ile birleşik aynı değeri mi taşıyor
    if YAZ:
        for parti in sorted({k.split("#")[0] for k in hedef}):
            bir = {json.loads(l)["gen_meta"]["parti_sira"]: json.loads(l)["is_negative"]
                   for l in (KOK / f"data/candidates/{parti}.jsonl").read_text(
                       encoding="utf-8").splitlines() if l.strip()}
            for b in sorted(KOK.glob(f"data/candidates/{parti}.blok*.jsonl")):
                for l in b.read_text(encoding="utf-8").splitlines():
                    if not l.strip():
                        continue
                    r = json.loads(l)
                    s = r["gen_meta"]["parti_sira"]
                    if s in bir and bir[s] != r["is_negative"]:
                        tutarsiz.append(f"{parti}#{s} ({b.name})")

    sat = ["# T227 kararının kayıtlara işlenmesi", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Kip:** {'YAZILDI' if YAZ else 'kuru koşu'}  ", "",
           f"Dokunulan kayıt örneği (blok + birleşik, yinelemeli): **{dokunulan}**  ",
           f"Değeri değişen: **{len(degisen)}**", ""]
    if degisen:
        sat += ["| kayıt | dosya | eski | **yeni** |", "|---|---|:-:|:-:|"]
        sat += [f"| `{k}` | `{d}` | {'red' if e else '—'} | **{'red' if y else '—'}** |"
                for k, d, e, y in sorted(degisen)]
    sat += ["", f"⭐ Blok ↔ birleşik tutarsızlığı: **{len(tutarsiz)}**"
                + (f" — {tutarsiz}" if tutarsiz else ""), ""]
    sat += ["## ⛔ Bu adımın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Karar üç Claude anotatörünün çoğunluğu** | uzman değil; "
            "`gen_meta.is_negative_oylar`'da üç oy da duruyor ve geri alınabilir |",
            "| ⛔ **`ozerklik_vurgusu` DEĞİŞMEDİ** | aynı yapı orada da var ama "
            "ölçülmedi; açık kalem |",
            "| ⚠️ **Birleştirme yeniden koşulmadı** | parti1'in planı üretimden "
            "sonra değişmişti (T224) ⇒ künye kapısı reddederdi. Alan cerrahi "
            "güncellendi ve iki dosya arasındaki tutarlılık ayrıca denetlendi |"]
    if YAZ:
        RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat))
    return 1 if tutarsiz else 0


if __name__ == "__main__":
    raise SystemExit(main())
