#!/usr/bin/env python3
"""`ozerklik_vurgusu` — `C` tabakasının TAM SAYIMI (T229).

⛔⛔ **Neden.** T228 `C` tabakasının (desen ateşlemedi + elle onay yok)
323 kaydından yalnız 26'sını okuyabilmişti ve korpus oranını **%22-%50**
gibi kullanılamayacak kadar geniş bir aralıkta bırakmıştı. Burada tabaka
tamamen okunuyor ⇒ aralık kalkıyor, yerine sayı geliyor.

⭐ **Tasarım T228'den iki noktada ayrılıyor:**
  1. **İki anotatör + hakem.** T228'de üç anotatör her kaydı okudu; burada
     `X` (Opus 5 alt ajanı) ve `Y` (Sonnet alt ajanı) her kaydı okuyor,
     AYRILDIKLARI kayıtlara ben bakıyorum. Gerekçe ölçülmüş: T228'de bu
     soruda uyum κ 0,85-0,97'ydi ⇒ üçüncü tam okuma, ayrışmayan kayıtlarda
     bilgi eklemiyor. ⛔ Bedeli de açık: ayrışmayan bir kaydın iki oyu var,
     üç değil.
  2. **Gizli tekrar testi.** T228'de okunan 26 kayıt listeye KARIŞTIRILDI
     ve anotatörlere söylenmedi. ⇒ Aynı soruya ikinci kez aynı cevabın
     verilip verilmediği ölçülüyor (test-tekrar güvenilirliği), ki T227 ve
     T228'in tamamı bu ölçülmeden duruyordu.

⛔ Tabaka ÜRETİM ANINDAKİ ölçütle yeniden kuruldu (desen + elle onay),
T228'in yazdığı alan değeriyle değil — yoksa T228'de düzeltilen 5 kayıt
tabakadan düşer ve tekrar testi imkânsız olurdu.

Kullanım: uv run python ...     → hakemlik gerekirse listeyi basar
          (hakem dosyası: scratchpad/cs-hakem.json)
Çıktı   : reports/analiz/2026-09-21-ozerklik-c-tabakasi-sayimi.md
"""
from __future__ import annotations

import json
import math
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
# Girdi: depodaki kalıcı kopya — T227-T230'un kanıt tabanı
# (bkz. data/anotasyon/OKU.md).
SP = KOK / "data/anotasyon"
RAPOR = KOK / f"reports/analiz/{TARIH}-ozerklik-c-tabakasi-sayimi.md"


def _kappa(x, y):
    n = len(x)
    po = sum(a == b for a, b in zip(x, y)) / n
    pe = sum((x.count(s) / n) * (y.count(s) / n) for s in set(x) | set(y))
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def main() -> int:
    anah = json.loads((SP / "cs-anahtar.json").read_text(encoding="utf-8"))
    oy = {}
    for kod in ("X", "Y"):
        d = {}
        for b in range(1, 5):
            y = SP / f"cs-{kod}-{b}.json"
            if not y.exists():
                print(f"⛔ {y.name} yok — anotatör bitmedi.")
                return 1
            for o in json.loads(y.read_text(encoding="utf-8")):
                d[o["id"]] = o["ozerklik"]
        eksik = set(anah) - set(d)
        if eksik:
            print(f"⛔ {kod} eksik {len(eksik)}: {sorted(eksik)[:10]}")
            return 1
        oy[kod] = d

    idler = sorted(anah)
    ayri = [i for i in idler if oy["X"][i] != oy["Y"][i]]
    hakem_y = SP / "cs-hakem.json"
    hakem = json.loads(hakem_y.read_text(encoding="utf-8")) if hakem_y.exists() else {}
    ilke = hakem.pop("_ilke", "")
    kalan = [i for i in ayri if i not in hakem]
    if kalan:
        print(f"⛔ HAKEMLİK GEREKİYOR — {len(ayri)} ayrışmanın {len(kalan)}'i karara "
              f"bağlanmamış.\n   Dosya: {hakem_y}\n")
        for i in kalan:
            print(f"{i}  ({anah[i]['kimlik']})  X={oy['X'][i]}  Y={oy['Y'][i]}")
        return 1

    karar = {i: (hakem[i] if i in hakem else oy["X"][i]) for i in idler}
    evet = [i for i in idler if karar[i] == "evet"]

    # ⭐ Gizli tekrar testi
    onc = json.loads((SP / "oz-uzlasma.json").read_text(encoding="utf-8"))
    tek = [i for i in idler if anah[i]["tekrar"]]
    ayni = [i for i in tek if onc[anah[i]["kimlik"]]["karar"] == karar[i]]

    def _wilson(k, n, z=1.96):
        p = k / n
        d = 1 + z * z / n
        m = (p + z * z / (2 * n)) / d
        r = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
        return max(0, m - r), min(1, m + r)

    sat = ["# `ozerklik_vurgusu` — `C` tabakasının tam sayımı", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Kapsam:** `C` tabakasının **{len(idler)}** kaydının tamamı "
           "(T228'de 26'sı okunmuştu)  ", "",
           "| anotatör | kim | rol |", "|---|---|---|",
           "| `X` | Claude Opus 5 alt ajanı | tam okuma |",
           "| `Y` | Claude Sonnet alt ajanı | tam okuma |",
           "| `H` | ben (Claude Code, Opus 5) | yalnız ayrışmalarda hakem |", "",
           "## 1. İki anotatör ne kadar uyuştu", "", "| | |", "|---|---:|",
           f"| kayıt | {len(idler)} |",
           f"| ham uyum | %{round(100*(len(idler)-len(ayri))/len(idler))} |",
           f"| κ | {_kappa([oy['X'][i] for i in idler], [oy['Y'][i] for i in idler]):.2f} |",
           f"| ⛔ hakeme düşen | **{len(ayri)}** |", "",
           f"⛔⛔ **Ayrışmalar RASTGELE DEĞİL, tek bir sınırda toplanıyor.** "
           f"{sum(1 for i in ayri if oy['X'][i] == 'evet')}/{len(ayri)}'inde `X` "
           "*«evet»*, `Y` *«hayır»* dedi — yani `X` (Opus) daha geniş okuyor. "
           "Hakemin uyguladığı ilke:", "",
           f"> {ilke}", "",
           f"⇒ Hakem bir tarafa yaslanmadı: `X` ile "
           f"{sum(1 for i in ayri if hakem[i] == oy['X'][i])}/{len(ayri)}, `Y` ile "
           f"{sum(1 for i in ayri if hakem[i] == oy['Y'][i])}/{len(ayri)} kayıtta "
           "aynı fikirde.", "",
           "## 2. ⭐⭐ Gizli tekrar testi", "",
           "⛔ T228'de okunmuş 26 kayıt listeye karıştırıldı ve anotatörlere "
           "söylenmedi. Aynı soruya ikinci kez aynı cevap veriliyor mu?", "",
           "| | |", "|---|---:|",
           f"| tekrar edilen kayıt | {len(tek)} |",
           f"| ⭐ aynı hükme varılan | **{len(ayni)}/{len(tek)}** "
           f"(%{round(100*len(ayni)/max(1,len(tek)))}) |", ""]
    fark = [i for i in tek if i not in ayni]
    if fark:
        sat += ["| kayıt | T228 | **şimdi** |", "|---|:-:|:-:|"]
        sat += [f"| `{anah[i]['kimlik']}` | {onc[anah[i]['kimlik']]['karar']} | "
                f"**{karar[i]}** |" for i in fark]
        sat += [""]
    sat += [f"➡️ *Test-tekrar güvenilirliği %{round(100*len(ayni)/max(1,len(tek)))}; "
            "T227 ve T228'in bütün sayıları bu ölçülmeden duruyordu.*", ""]

    a, b = _wilson(5, 26)
    sat += ["## 3. Tabakanın gerçek oranı — kestirim yerine SAYIM", "",
            "| | |", "|---|---:|",
            f"| `C` tabakası | {len(idler)} |",
            f"| ⭐ özerklik taşıyan | **{len(evet)}** (%{round(100*len(evet)/len(idler))}) |",
            f"| T228'in 26 kayıtlık kestirimi | %19, %95 aralık "
            f"%{round(100*a)}-%{round(100*b)} ({a*323:.0f}-{b*323:.0f} kayıt) |",
            f"| ⇒ kestirim tuttu mu | "
            f"{'⭐ **evet**, sayım aralığın içinde' if a*323 <= len(evet) <= b*323 else '⛔ **hayır**, sayım aralığın DIŞINDA'} |", ""]

    return _rapor_bitir(sat, anah, karar, evet, idler)


def _rapor_bitir(sat, anah, karar, evet, idler):
    onceki_alan = 90    # T228 sonrası korpus beyanı
    # ⛔ T228'de C'den 5 kayıt zaten «var»a çevrilmişti; onları iki kez sayma.
    onc = json.loads((SP / "oz-uzlasma.json").read_text(encoding="utf-8"))
    zaten = {anah[i]["kimlik"] for i in idler
             if anah[i]["tekrar"] and onc[anah[i]["kimlik"]]["karar"] == "evet"}
    yeni = [i for i in evet if anah[i]["kimlik"] not in zaten]
    toplam = onceki_alan + len(yeni)
    sat += ["## 4. Korpus", "", "| | |", "|---|---:|",
            f"| T228 sonrası beyan | {onceki_alan}/412 (%{round(100*onceki_alan/412)}) |",
            f"| ⭐ bu sayımla eklenen | **+{len(yeni)}** |",
            f"| ⭐⭐ **yeni toplam** | **{toplam}/412 "
            f"(%{round(100*toplam/412)})** |",
            f"| T228 kestirimi | ~140 (%34), aralık 92-207 |", "",
            "## ⛔ Bu sayımın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Ayrışmayan kayıtların İKİ oyu var, üç değil** | üçüncü tam "
            "okuma yapılmadı; gerekçesi T228'de ölçülen κ 0,85-0,97 ama bu bir "
            "gerekçe, kanıt değil |",
            "| ⛔⛔ **Anotatörlerin ikisi de Claude, hakem de ben** | T227'den "
            "beri süren şerh: ortak yanlılık uyumu yukarı çeker |",
            "| ⛔ **`A` ve `B` tabakaları yeniden okunmadı** | onların oranları "
            "T228'den geliyor (`A` sayımdı, `B` 20/65 örneklem) ⇒ korpus sayısının "
            "`B`'den gelen bileşeni hâlâ bir kestirim |",
            "| ⚠️ **Karar kayda yazılmadı** | bu betik hiçbir kayda dokunmaz |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    (SP / "cs-karar.json").write_text(json.dumps(
        {anah[i]["kimlik"]: karar[i] for i in idler}, ensure_ascii=False, indent=1),
        encoding="utf-8")
    print("\n".join(sat))
    print(f"\n→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
