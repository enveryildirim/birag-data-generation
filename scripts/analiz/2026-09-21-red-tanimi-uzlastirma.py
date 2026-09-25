#!/usr/bin/env python3
"""`is_negative`'in iki canlı tanımının ayrıştığı 26 kayıt — üç anotatörle
karara bağlama.

⛔⛔ **Nereden çıktı.** T226: (a) blok kapısı yalnız son asistan turundaki red
desenine bakıyor, (b) `beyan-metin-uyumu` ayrıca kullanıcı turunda bir TALEP
işareti arıyor. İkisi, (a)'nın ateşlediği 70 kaydın 26'sında ayrılıyor.
Ayrışmanın İKİ ayrı sebebi olabilir ve karar ikisinde TERS yöne gider:
  · sezici gerçek bir talebi kaçırdıysa ⇒ **(b) onarılmalı**, kayıt red'dir;
  · gerçekten talep yoksa ⇒ **(a) fazla sayıyor**, kayıt red DEĞİLDİR.
⇒ Ayrımı desen yapamaz, okuma yapar.

⭐ **Üç anotatör** (kullanıcı isteğiyle Claude kullanıldı):
  · `A` — Claude Opus 5 alt ajanı, bağımsız bağlam
  · `B` — Claude Sonnet alt ajanı, bağımsız bağlam
  · `C` — ben (Claude Code, Opus 5). ⛔ K30: bu bir İNSAN kararı değil;
    hiçbiri uzman değil ve üçü de aynı model ailesinden. Uyum yüksek çıksa
    bile bu **anotatör bağımsızlığı kanıtı sayılmaz** — aynı ailenin ortak
    yanlılığı uyumu yukarı çeker.

⭐ **İki soru soruldu, biri ötekinin vekili:**
  · `talep` — kullanıcı asistandan bir şey istiyor mu (= (b)'nin şartı)
  · `red`   — asistan istenen bir şeyi geri çeviriyor mu (= ölçülmek İSTENEN)
⇒ Vekilin hedefi ne kadar izlediği de ölçülüyor.

⛔ **15 KONTROL ÖĞESİ karıştırıldı** (8'i iki tanımın da «red» dediği, 7'si
(a)'nın red demediği kayıtlar) ve anotatörlere hangi öğenin hangi grupta
olduğu SÖYLENMEDİ. Kontroller olmadan *«hepsi sorunlu»* çıpası kurulurdu.

Girdi : scratchpad/anot-{A,B,C-benim}.json + anot-anahtar.json
Çıktı : reports/analiz/2026-09-21-red-tanimi-uzlastirma.md
"""
from __future__ import annotations

import json
import sys
from itertools import combinations
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
# Girdi dizini: depodaki kalıcı kopya (T227-T230'un kanıt tabanı,
# bkz. data/anotasyon/OKU.md). Argümanla başka bir dizin verilebilir.
SP = Path(sys.argv[1]) if len(sys.argv) > 1 else KOK / "data/anotasyon"
RAPOR = KOK / f"reports/analiz/{TARIH}-red-tanimi-uzlastirma.md"

ANOT = {"A": "anot-A.json", "B": "anot-B.json", "C": "anot-C-benim.json"}
ETIKET = {"A": "Claude Opus 5 alt ajanı", "B": "Claude Sonnet alt ajanı",
          "C": "ben (Claude Code, Opus 5)"}


def _kappa(x: list[str], y: list[str]) -> float:
    """Cohen'in kappa'sı. ⛔ İki sınıflı ve dengesiz dağılımda kappa küçük
    görünebilir; ham uyumla BİRLİKTE okunur."""
    n = len(x)
    po = sum(a == b for a, b in zip(x, y)) / n
    sinif = set(x) | set(y)
    pe = sum((x.count(s) / n) * (y.count(s) / n) for s in sinif)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def main() -> int:
    anahtar = json.loads((SP / "anot-anahtar.json").read_text(encoding="utf-8"))
    hük: dict[str, dict[str, dict]] = {}
    for kod, ad in ANOT.items():
        y = SP / ad
        if not y.exists():
            print(f"⛔ {ad} yok — anotatör henüz bitmedi.")
            return 1
        hük[kod] = {o["id"]: o for o in json.loads(y.read_text(encoding="utf-8"))}
        eksik = set(anahtar) - set(hük[kod])
        if eksik:
            print(f"⛔ {kod} eksik öğe: {sorted(eksik)}")
            return 1

    idler = sorted(anahtar)
    ayr = [i for i in idler if anahtar[i]["grup"] == "ayrisan"]
    kon = [i for i in idler if anahtar[i]["grup"] == "kontrol"]

    sat = ["# `is_negative` ayrışmasının karara bağlanması", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           "**Girdi:** T226'nın ayrışan 26 kaydı + 15 kontrol (toplam 41), "
           "üç anotatör  ", ""]
    sat += ["| anotatör | kim |", "|---|---|"]
    sat += [f"| `{k}` | {ETIKET[k]} |" for k in ANOT]

    sat += ["", "## 1. Anotatörler arası uyum", "",
            "| soru | çift | ham uyum | κ |", "|---|---|---:|---:|"]
    for soru in ("talep", "red"):
        for a, b in combinations(ANOT, 2):
            x = [hük[a][i][soru] for i in idler]
            y = [hük[b][i][soru] for i in idler]
            ham = sum(p == q for p, q in zip(x, y)) / len(x)
            sat.append(f"| `{soru}` | {a}–{b} | %{round(100*ham)} | {_kappa(x, y):.2f} |")

    # ⭐ Kontroller: anotasyon görevinin kendisi geçerli mi?
    sat += ["", "## 2. Kontrol öğeleri — görev geçerli mi", "",
            "⛔ Kontrollerde iki tanım ZATEN aynı fikirde. Anotatörler burada da "
            "onlarla aynı fikirdeyse görev anlaşılmış demektir; ayrılıyorlarsa "
            "ayrışan gruptaki hükümleri de şüphelidir.", "",
            "| anotatör | `a&b: red` (8 öğe) | `a: red YOK` (7 öğe) |",
            "|---|---:|---:|"]
    # ⛔ Kontroller iki ALT TÜR: (i) iki tanımın da «red» dediği 8 kayıt,
    #    (ii) (a) desenin HİÇ ateşlemediği 7 kayıt. İkincisi bir yan ölçüm
    #    getiriyor: desen ateşlemediği yerde anotatör red görüyor mu?
    alt = {"var": [i for i in kon if anahtar[i].get("alt") == "a_var"],
           "yok": [i for i in kon if anahtar[i].get("alt") == "a_yok"]}
    for k in ANOT:
        v = sum(1 for i in alt["var"] if hük[k][i]["red"] == "evet")
        y = sum(1 for i in alt["yok"] if hük[k][i]["red"] == "evet")
        sat.append(f"| `{k}` | {v}/{len(alt['var'])} | {y}/{len(alt['yok'])} |")
    ort = sum(sum(1 for i in alt["yok"] if hük[k][i]["red"] == "evet")
              for k in ANOT) / 3
    sat += ["", f"⭐⭐ **İkinci sütun beklenmedik ve ayrı bir bulgu.** Desen (a) bu "
                f"7 kayıtta HİÇ ateşlemiyor, ama anotatörler ortalama "
                f"**{ort:.1f}/{len(alt['yok'])}**'sinde red görüyor. ⇒ Sözlük yalnız FAZLA "
                "saymıyor, AZ da sayıyor: *«söylemeyeceğim»*, *«vermeyeceğim»*, "
                "*«demem»* gibi kuruluşlar listede yok. ➡️ *Şablondan kaçınmak "
                "için red cümlesini her seferinde başka türlü kurmak, sözlüğü "
                "yapısal olarak geride bırakıyor.*", ""]

    # ⭐⭐ Uzlaştırma: çoğunluk
    sat += ["", "## 3. Ayrışan 26 kaydın kararı — çoğunluk", "",
            "| # | kayıt | A | B | C | **karar** | sonuç |",
            "|---|---|:-:|:-:|:-:|:-:|---|"]
    karar: dict[str, str] = {}
    for i in ayr:
        oy = [hük[k][i]["red"] for k in ANOT]
        c = "evet" if oy.count("evet") >= 2 else "hayir"
        karar[i] = c
        sonuc = ("⭐ (a) haklı — sezici talebi kaçırmış"
                 if c == "evet" else "⛔ (b) haklı — (a) fazla saymış")
        sat.append(f"| {i} | `{anahtar[i]['kimlik']}` | {oy[0][0].upper()} | "
                   f"{oy[1][0].upper()} | {oy[2][0].upper()} | **{c}** | {sonuc} |")

    e = sum(1 for i in ayr if karar[i] == "evet")
    h = len(ayr) - e
    tam = sum(1 for i in ayr if len({hük[k][i]["red"] for k in ANOT}) == 1)
    sat += ["", f"⭐ **{e}** kayıtta (a) haklı (sezici kaçırdı), **{h}** kayıtta "
                f"(b) haklı ((a) fazla saydı). Üç anotatörün TAMAMI aynı fikirde: "
                f"**{tam}/{len(ayr)}**.", ""]

    # ⭐ Vekil ne kadar izliyor
    sat += ["## 4. `talep` vekili `red` hedefini ne kadar izliyor", "",
            "| anotatör | `talep`≠`red` olan öğe |", "|---|---:|"]
    for k in ANOT:
        f = sum(1 for i in idler if (hük[k][i]["talep"] == "evet") != (hük[k][i]["red"] == "evet"))
        sat.append(f"| `{k}` | {f}/{len(idler)} |")

    sat += ["", "## ⛔ Bu kararın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Üç anotatör de Claude** | ikisi alt ajan, biri ben; üçü aynı "
            "model ailesinden. Yüksek uyum **bağımsızlık kanıtı değildir** — ortak "
            "yanlılık uyumu yukarı çeker. Uzman anotatör hâlâ açık kalem |",
            "| ⛔ **Çoğunluk bir doğruluk ölçütü değil** | 2/3 çoğunlukla karara "
            "bağlanan kayıtlar tablosunda ayrıca işaretli; tam uyum sayısı yukarıda |",
            "| ⚠️ **Karar kayda YAZILMADI** | bu betik hiçbir kayda dokunmaz; "
            "tanımın onarımı ve yeniden ölçüm ayrı adımdır |"]

    (SP / "uzlasma.json").write_text(
        json.dumps({i: {"kimlik": anahtar[i]["kimlik"], "karar": karar[i]}
                    for i in ayr}, ensure_ascii=False, indent=1), encoding="utf-8")
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat))
    print(f"\n→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
