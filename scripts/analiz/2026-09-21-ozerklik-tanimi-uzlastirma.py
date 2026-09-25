#!/usr/bin/env python3
"""`ozerklik_vurgusu` — T227'nin yöntemi bu alana uygulandı.

⛔⛔ **Neden.** T227 `is_negative`'i ölçümden beyana çevirdi ve şerhinde
*«`ozerklik_vurgusu` aynı yapıyı taşıyor ama ölçülmedi»* yazıyordu. Burada
ölçülüyor. ⛔ Yapı AYNI DEĞİL ve fark önemli: özerklikte iki rakip tanım yok,
**bir desen ve bir kaçamak** var —
    `ozerklik_vurgusu = OZERKLIK_deseni(son)  VEYA  elle_onay`
⇒ Üç tabaka doğuyor ve üçü ayrı şey soruyor:

  · **A — yalnız desen** (24 kayıt, TAMAMI alındı): desen ateşledi, elle onay
    yok. *Desen FAZLA mı sayıyor?*
  · **B — yalnız elle onay** (65 kayıt, 20'si alındı): desen görmedi, ben
    onayladım. *Kendi onaylarım tutuyor mu?* (K30: bu benim hükmümdü)
  · **C — hiçbiri** (323 kayıt, 26'sı alındı): *Desen AZ mı sayıyor?*

⭐ İki soru soruldu: `karar_var` (ortada kullanıcının vereceği bir karar var
mı — özerklik vurgusunun ön şartı) ve `ozerklik` (son mesaj kararı açıkça
kullanıcıya bırakıyor mu). Talimatta *«sözcük aramıyorsun»* açıkça yazıldı.

⛔ Anotatörler tabakaları BİLMİYOR; 70 öğe karıştırılmış tek liste olarak
verildi.

Girdi : scratchpad/oz-{A,B,C-benim}.json + oz-anahtar.json
Çıktı : reports/analiz/2026-09-21-ozerklik-tanimi-uzlastirma.md
"""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
# Girdi: depodaki kalıcı kopya — T227-T230'un kanıt tabanı
# (bkz. data/anotasyon/OKU.md).
SP = KOK / "data/anotasyon"
RAPOR = KOK / f"reports/analiz/{TARIH}-ozerklik-tanimi-uzlastirma.md"
ANOT = {"A": "oz-A.json", "B": "oz-B.json", "C": "oz-C-benim.json"}
ETIKET = {"A": "Claude Opus 5 alt ajanı", "B": "Claude Sonnet alt ajanı",
          "C": "ben (Claude Code, Opus 5)"}
EVREN = {"A": 24, "B": 65, "C": 323}      # tabakaların korpustaki gerçek boyu


def _kappa(x: list[str], y: list[str]) -> float:
    n = len(x)
    po = sum(a == b for a, b in zip(x, y)) / n
    pe = sum((x.count(s) / n) * (y.count(s) / n) for s in set(x) | set(y))
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def main() -> int:
    anah = json.loads((SP / "oz-anahtar.json").read_text(encoding="utf-8"))
    hük = {}
    for k, ad in ANOT.items():
        y = SP / ad
        if not y.exists():
            print(f"⛔ {ad} yok — anotatör bitmedi.")
            return 1
        hük[k] = {o["id"]: o for o in json.loads(y.read_text(encoding="utf-8"))}
        if set(anah) - set(hük[k]):
            print(f"⛔ {k} eksik: {sorted(set(anah) - set(hük[k]))}")
            return 1

    idler = sorted(anah)
    tab = {t: [i for i in idler if anah[i]["tabaka"] == t] for t in "ABC"}
    coguk = {i: ("evet" if [hük[k][i]["ozerklik"] for k in ANOT].count("evet") >= 2
                 else "hayir") for i in idler}

    sat = ["# `ozerklik_vurgusu`'nun karara bağlanması", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           "**Girdi:** 70 öğe — A tabakasının tamamı (24), B'den 20/65, C'den "
           "26/323; karıştırılmış, tabaka bilgisi verilmedi  ", "",
           "| anotatör | kim |", "|---|---|"]
    sat += [f"| `{k}` | {ETIKET[k]} |" for k in ANOT]

    sat += ["", "## 1. Anotatörler arası uyum", "",
            "| soru | çift | ham uyum | κ |", "|---|---|---:|---:|"]
    for soru in ("karar_var", "ozerklik"):
        for a, b in combinations(ANOT, 2):
            x = [hük[a][i][soru] for i in idler]
            y = [hük[b][i][soru] for i in idler]
            sat.append(f"| `{soru}` | {a}–{b} | "
                       f"%{round(100*sum(p==q for p,q in zip(x,y))/len(x))} | "
                       f"{_kappa(x, y):.2f} |")

    sat += ["", "## 2. Tabaka tabaka — alan ne diyor, anotatörler ne diyor", "",
            "| tabaka | alan | örneklem | çoğunluk `ozerklik`=evet | ⇒ |",
            "|---|:-:|---:|---:|---|"]
    ozet = {}
    for t, ad, alan in (("A", "yalnız desen", "evet"),
                        ("B", "yalnız elle onay", "evet"),
                        ("C", "hiçbiri", "hayır")):
        e = sum(1 for i in tab[t] if coguk[i] == "evet")
        n = len(tab[t])
        ozet[t] = (e, n)
        yorum = ("⛔ desen FAZLA saymış" if t == "A" and e < n else
                 "⭐ desen doğru saymış" if t == "A" else
                 "⛔ onaylarım FAZLA saymış" if t == "B" and e < n else
                 "⭐ onaylarım tutuyor" if t == "B" else
                 "⛔ alan AZ saymış" if e else "⭐ alan doğru")
        sat.append(f"| `{t}` ({ad}) | {alan} | {n} | {e}/{n} (%{round(100*e/n)}) | {yorum} |")

    # ⭐ Korpusa taşıma. ⛔ A tabakası sayım (n=24=evren), B ve C örneklem.
    # ⛔⛔ ÖRNEKLEMDEN EVRENE TAŞINAN HER SAYI BİR ARALIKTIR. Wilson skor
    # aralığı kullanılıyor (küçük n ve uç orana normal yaklaşımdan dayanıklı).
    import math

    def _wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
        if n == 0:
            return (0.0, 1.0)
        p = k / n
        d = 1 + z * z / n
        m = (p + z * z / (2 * n)) / d
        r = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
        return (max(0.0, m - r), min(1.0, m + r))

    tah = sum(ozet[t][0] / ozet[t][1] * EVREN[t] for t in "ABC")
    alt = sum((ozet[t][0] / ozet[t][1] if t == "A" else _wilson(*ozet[t])[0]) * EVREN[t]
              for t in "ABC")
    ust = sum((ozet[t][0] / ozet[t][1] if t == "A" else _wilson(*ozet[t])[1]) * EVREN[t]
              for t in "ABC")
    mevcut = EVREN["A"] + EVREN["B"]
    cw = _wilson(*ozet["C"])
    sat += ["", "## 3. Korpusa taşıma", "",
            f"Alanın şu an *«özerklik var»* dediği: **{mevcut}/412** "
            f"(%{round(100*mevcut/412)}).  ",
            f"Tabaka oranları evrene taşınınca kestirim: **~{tah:.0f}/412** "
            f"(%{round(100*tah/412)}), %95 aralık **{alt:.0f}-{ust:.0f}** "
            f"(%{round(100*alt/412)}-%{round(100*ust/412)}).", "",
            f"⛔ `A` bir SAYIM (24 kaydın tamamı okundu); `B` ve `C` ÖRNEKLEM. "
            f"Aralığı açan bileşen `C`: 26 kayıtta {ozet['C'][0]} ⇒ oran "
            f"%{round(100*ozet['C'][0]/ozet['C'][1])}, Wilson aralığı "
            f"%{round(100*cw[0])}-%{round(100*cw[1])} ve bu 323 kayda "
            f"çarpılıyor ({cw[0]*323:.0f}-{cw[1]*323:.0f} kayıt).", "",
            "⇒ **Kestirim, alanın %22'sinin bir ALT SINIR olduğunu söylüyor; "
            "kaç puan alt sınır olduğunu söylemiyor.** Aralığın alt ucu bile "
            f"mevcut sayının üstünde ({alt:.0f} > {mevcut}), yani AZ SAYMA "
            "yönü aralıktan bağımsız.", ""]

    sat += ["## 4. Ön şart tutuyor mu — `karar_var`", "",
            "⛔⛔ **BU BÖLÜMÜN SAYISINA GÜVENİLEMEZ VE SEBEBİ YUKARIDA:** "
            "`karar_var`'da anotatör uyumu κ **0,16-0,52** çıktı (`ozerklik`'te "
            "0,85-0,97). ➡️ *T227'de `talep` ön şartı güvenilir biçimde "
            "etiketlenebiliyordu; «ortada bir karar var mı» etiketlenemiyor.* "
            "⇒ Özerklik için T227'deki gibi bir ön şart kurulamaz — aşağıdaki "
            "sayı yalnız kayda geçsin diye duruyor.", "",
            "| | |", "|---|---:|"]
    bos = [i for i in idler if coguk[i] == "evet"
           and [hük[k][i]["karar_var"] for k in ANOT].count("evet") < 2]
    sat += [f"| çoğunluk `ozerklik`=evet | {sum(1 for i in idler if coguk[i]=='evet')} |",
            f"| ⛔ — bunların kararı olmayanı | **{len(bos)}** "
            + (f"({', '.join(anah[i]['kimlik'] for i in bos)})" if bos else "") + " |", ""]

    sat += ["## 5. Kayıt kayıt karar", "",
            "| # | kayıt | tabaka | A | B | C | **karar** | alan | değişir mi |",
            "|---|---|:-:|:-:|:-:|:-:|:-:|:-:|---|"]
    degis = {}
    for i in idler:
        t = anah[i]["tabaka"]
        alan = t in ("A", "B")
        oy = [hük[k][i]["ozerklik"][0].upper() for k in ANOT]
        yeni = coguk[i] == "evet"
        if yeni != alan:
            degis[anah[i]["kimlik"]] = yeni
        sat.append(f"| {i} | `{anah[i]['kimlik']}` | {t} | {oy[0]} | {oy[1]} | "
                   f"{oy[2]} | **{coguk[i]}** | {'evet' if alan else 'hayır'} | "
                   f"{'⛔ **' + ('evet' if yeni else 'hayır') + '**' if yeni != alan else '—'} |")

    tam = sum(1 for i in idler if len({hük[k][i]["ozerklik"] for k in ANOT}) == 1)
    sat += ["", f"⭐ Üç anotatörün tamamı aynı fikirde: **{tam}/{len(idler)}**. "
                f"Alanla ayrışan: **{len(degis)}/{len(idler)}**.", ""]

    sat += ["## ⛔ Bu kararın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Üç anotatör de Claude** | T227'nin şerhi aynen geçerli: ortak "
            "yanlılık uyumu yukarı çeker, bu bir bağımsızlık kanıtı değildir |",
            "| ⛔⛔ **`C` tabakası ÖRNEKLEM** | 323 kaydın 26'sı okundu; korpus "
            "kestirimi bu orana çok duyarlı ve güven aralığı hesaplanmadı |",
            "| ⛔ **`B` tabakası benim kendi onaylarım** | anotatör `C` de benim ⇒ "
            "o sütunda kendi kararımı ikinci kez veriyorum, bağımsız değil |",
            "| ⚠️ **Karar kayda yazılmadı** | bu betik hiçbir kayda dokunmaz |"]

    (SP / "oz-uzlasma.json").write_text(json.dumps(
        {anah[i]["kimlik"]: {"tabaka": anah[i]["tabaka"], "karar": coguk[i]}
         for i in idler}, ensure_ascii=False, indent=1), encoding="utf-8")
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[:sat.index("## 5. Kayıt kayıt karar")]))
    print(f"\n… (kayıt tablosu raporda)\n→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
