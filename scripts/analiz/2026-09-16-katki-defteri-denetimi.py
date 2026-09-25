#!/usr/bin/env python3
"""63 katkının kaçı TEZDE SAVUNULABİLİR — defterin kendisine Kural 7 uygulanıyor.

⛔ `docs/tez/katki-defteri.md` projenin en değerli tez artefaktı: özgün olabilecek
her iddia ortaya çıktığı anda kaydedildi. ⚠️ Ama defterin **kendisi** hiç
denetlenmedi. Tezde bir katkıyı savunmak üç şey ister ve üçü de makineyle
sınanabilir:

  1. **Kanıt var mı** — gösterilen dosya gerçekten duruyor mu?
  2. **Sayı bugün üretilebiliyor mu** — adı geçen betik yeniden üretilebilirlik
     denetiminden geçiyor mu (`2026-09-16-rapor-yeniden-uretilebilirlik.md`)?
  3. **Çapraz atıflar tutuyor mu** — `İlgili` sütunundaki T##/K## gerçekten var mı?

⭐ Üçü de *«sonra bakarız»* denebilecek şeyler ve tam bu yüzden ölçülüyor: tez
yazımı sırasında bir katkının kanıtının bulunamaması, o katkıyı **kaybetmek**
demektir (Kural 7'nin defterdeki karşılığı).

⚠️ Bu betik katkının **doğruluğunu** yargılamaz — yalnızca savunulabilirliğinin
MEKANİK koşullarını sayar. Bir iddianın güçlü olup olmadığı tez yazarının kararı.

Girdi : docs/tez/katki-defteri.md · PROJECT_MEMORY.md ·
        reports/analiz/2026-09-16-rapor-yeniden-uretilebilirlik.md
Çıktı : reports/analiz/2026-09-16-katki-defteri-denetimi.md
Kullanım: uv run python scripts/analiz/2026-09-16-katki-defteri-denetimi.py
"""
from __future__ import annotations

import collections
import hashlib
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]
DEFTER = KOK / "docs/tez/katki-defteri.md"
HAFIZA = KOK / "PROJECT_MEMORY.md"
YENIDEN = KOK / "reports/analiz/2026-09-16-rapor-yeniden-uretilebilirlik.md"
RAPOR = KOK / f"reports/analiz/{TARIH}-katki-defteri-denetimi.md"

# Efsanenin ilan ettiği `Durum` değerleri — defterin kendi başlığından.
DURUMLAR = {"iddia", "kanıtlı", "onaylı", "çürüdü"}
GUCLER = {"⭐", "◐", "○"}
UZANTI = r"(?:py|md|json|jsonl|bib|yaml|yml|txt|jinja)"
YOL = re.compile(rf"`([A-Za-z0-9_./*-]+/[A-Za-z0-9_.*-]+\.{UZANTI})`")
ATIF = re.compile(r"\b([TK])(\d{1,3})\b")


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def satirlar() -> list[list[str]]:
    """Defterin katkı tablosu — `| T## |` ile başlayan her satır."""
    out = []
    for s in DEFTER.read_text(encoding="utf-8").split("\n"):
        if re.match(r"^\|\s*T\d+\s*\|", s):
            out.append([h.strip() for h in s.strip().strip("|").split("|")])
    return out


def yeniden_durumu() -> dict[str, str]:
    """betik adı → yeniden üretilebilirlik sınıfı (`✅ aynı`, `⛔ kaydı`, …)."""
    if not YENIDEN.exists():
        return {}
    out = {}
    for s in YENIDEN.read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^\|\s*`([^`]+\.py)`\s*\|\s*`?([^`|]*)`?\s*\|\s*([^|]+?)\s*\|", s)
        if m:
            out[m.group(1)] = m.group(3).strip()
    return out


def betik_sinifi(betik: str, yen: dict[str, str]) -> str:
    """Bir betiğin yeniden üretilebilirlik sınıfı — DÖRT ayrı şey, tek torbada değil.

    ⛔ *«Denetimde yok»* tek başına bir kusur değildir: yeniden üretilebilirlik
    denetimi yalnızca `reports/analiz/*.md` ÜRETEN betikleri kapsar. Bir koşu
    başlatıcısı (`*-kosu.py`) ya da veri üreticisi rapor yazmaz ve kapsam dışıdır.
    ⭐ Ama raporu OLDUĞU hâlde denetimde görünmeyen betik gerçek bir açıktır —
    ikisi ayrı sayılıyor.
    """
    if betik in yen:
        return yen[betik]
    stem = betik[:-3]
    raporu_var = (KOK / f"reports/analiz/{stem}.md").exists()
    return "❓ raporu var ama DENETİMDE YOK" if raporu_var else "⚪ rapor üretmiyor (kapsam dışı)"


def ozet_sinif(durumlar: list[str]) -> str:
    if any(d.startswith("⛔") for d in durumlar):
        return "⛔ en az biri SAPIYOR"
    if any(d.startswith("❓") for d in durumlar):
        return "❓ raporu var ama denetimde yok"
    if any(d.startswith("⏭️") for d in durumlar):
        return "⏭️ model çağırıyor (beyanlı)"
    if all(d.startswith("⚪") for d in durumlar):
        return "⚪ rapor üretmiyor (kapsam dışı)"
    return "✅ hepsi aynı"


def var_mi(yol: str) -> bool:
    """Glob da kabul edilir: bazı satırlar `ham-judge/v9-*.jsonl` gibi küme gösteriyor."""
    if "*" in yol:
        return bool(list(KOK.glob(yol)))
    return (KOK / yol).exists()


def main() -> int:
    ROW = satirlar()
    YEN = yeniden_durumu()
    hafiza = HAFIZA.read_text(encoding="utf-8")
    K_VAR = {f"K{m}" for m in re.findall(r"^\|\s*K(\d+)\s*\|", hafiza, re.M)}
    T_VAR = {r[0] for r in ROW}

    L = ["# Katkı defteri denetimi — 63 katkının kaçı tezde savunulabilir?", "",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
         f"**Girdi:** `docs/tez/katki-defteri.md` SHA256 `{sha(DEFTER)}`  ",
         f"**Girdi:** `PROJECT_MEMORY.md` SHA256 `{sha(HAFIZA)}`  ",
         f"**Girdi:** `reports/analiz/2026-09-16-rapor-yeniden-uretilebilirlik.md` "
         f"SHA256 `{sha(YENIDEN)}`", "", "---", "",
         "## Neden", "",
         "Defter projenin en değerli tez artefaktı — ama **kendisi hiç denetlenmedi**.",
         "Bir katkıyı tezde savunmak üç mekanik koşul ister ve üçü de sınanabilir:",
         "**(1)** gösterilen kanıt dosyası duruyor mu · **(2)** adı geçen betik bugün",
         "hâlâ aynı sayıyı üretiyor mu · **(3)** çapraz atıflar tutuyor mu.", "",
         "⚠️ Katkının **doğruluğu** yargılanmıyor; yalnızca savunulabilirliğin mekanik",
         "koşulları sayılıyor. Bir iddianın güçlü olup olmadığı tez yazarının kararı.", "",
         f"**Tabloda {len(ROW)} katkı satırı bulundu.**", ""]

    # --- 1. sütun disiplini ---------------------------------------------------
    sutun_say = collections.Counter(len(r) for r in ROW)
    guc = collections.Counter(r[2] if len(r) > 2 else "?" for r in ROW)
    durum_uyan = sum(1 for r in ROW if len(r) > 3 and r[3].strip("*` ").lower() in DURUMLAR)  # lower-muaf: DURUMLAR küçük harfli Türkçe ama i/ı taşımıyor: iddia/kanıtlı/onaylı/çürüdü
    L += ["## 1. ⛔ Sütun disiplini — başlık satırların gerçeğini anlatıyor mu", "",
          "Defterin başlığı: `| # | Katkı | Güç | Durum | Kanıt / kanıt için gereken | İlgili |`",
          "", "| | |", "|---|---:|",
          f"| satır | {len(ROW)} |",
          f"| sütun sayısı dağılımı | " + ", ".join(f"{k}:{v}" for k, v in sorted(sutun_say.items())) + " |",
          f"| **`Durum` sütunu efsanedeki bir değeri taşıyan satır** | **{durum_uyan}/{len(ROW)}** |", ""]
    if durum_uyan < len(ROW) / 2:
        L += ["⛔⭐ **Başlık satırları ANLATMIYOR.** `Durum` sütununun efsanesi dört değer",
              "ilan ediyor (`iddia`/`kanıtlı`/`onaylı`/`çürüdü`) ama satırların",
              f"**{len(ROW)-durum_uyan}**'inde o sütun serbest metin (kanıt ve sınırlılık",
              "prozası) taşıyor; kanıt dosyaları da bir sağdaki sütuna kaymış.",
              "➡️ *Tez okuyucusu için bu sessiz bir hata: sütun adına göre okuyan kişi",
              "yanlış hücreyi okur. Düzeltme ya başlığı gerçeğe uydurmak ya satırları",
              "başlığa — ikisi de KARAR, bu yüzden burada yalnızca ölçülüyor.*", ""]
    L += ["| Güç imi | satır |", "|---|---:|"]
    for g, n in sorted(guc.items(), key=lambda t: (-t[1], t[0])):
        L.append(f"| {g or '_(boş)_'} | {n} |")
    L += ["", "⚠️ Efsane üç im tanımlıyor (⭐ · ◐ · ○); yukarıdaki dağılım ne kullanıldığını",
          "gösteriyor. Bileşik imler (`⭐⭐`) efsanede **tanımlı değil**.", ""]

    # --- 2. kanıt dosyaları ---------------------------------------------------
    kanitsiz, kirik, tum_yol = [], [], collections.Counter()
    for r in ROW:
        metin = " | ".join(r[3:])
        yollar = sorted(set(YOL.findall(metin)))
        if not yollar:
            kanitsiz.append(r[0])
            continue
        for y in yollar:
            tum_yol[y] += 1
            if not var_mi(y):
                kirik.append((r[0], y))
    L += ["## 2. Kanıt dosyaları duruyor mu", "", "| | |", "|---|---:|",
          f"| gösterilen ayrı dosya/küme | {len(tum_yol)} |",
          f"| ⛔ **bulunamayan** | **{len(kirik)}** |",
          f"| ⚠️ hiç dosya göstermeyen katkı | **{len(kanitsiz)}** |", ""]
    if kirik:
        L += ["| katkı | bulunamayan yol |", "|---|---|"]
        L += [f"| {t} | `{y}` |" for t, y in kirik]
        L += [""]
    else:
        L += ["✅ **Gösterilen her yol duruyor.**", ""]
    if kanitsiz:
        L += ["⚠️ **Hiç dosya göstermeyen katkılar:** "
              + ", ".join(f"**{t}**" for t in kanitsiz) + ".", "",
              "Bunların bir kısmı meşru: `iddia` durumundaki bir katkının henüz kanıtı",
              "olmayabilir. ⛔ Ama tez yazımında bu satırlar **kanıt aranacak** yer",
              "değil, **kanıt üretilecek** yerdir ve ayırt edilmeleri gerekir.", ""]

    # --- 3. sayı bugün üretilebiliyor mu -------------------------------------
    betikli, betiksiz, sinif = [], [], collections.Counter()
    for r in ROW:
        metin = " | ".join(r[3:])
        bet = sorted({Path(y).name for y in YOL.findall(metin)
                      if y.startswith("scripts/") and y.endswith(".py")})
        if not bet:
            betiksiz.append(r[0])
            continue
        durumlar = [betik_sinifi(b, YEN) for b in bet]
        betikli.append((r[0], bet, durumlar))
        sinif[ozet_sinif(durumlar)] += 1
    sapan = [(t, b, d) for t, b, d in betikli
             if any(x.startswith(("⛔", "❓")) for x in d)]
    kapsamdisi = [(t, b, d) for t, b, d in betikli
                  if all(x.startswith("⚪") for x in d)]
    L += ["## 3. ⭐ Sayı bugün üretilebiliyor mu", "",
          "Katkının gösterdiği `scripts/analiz/*.py` dosyaları yeniden üretilebilirlik",
          "denetiminden geçiyor mu (`⛔ kaydı` = yayımlanan sayı artık betiğin ürettiği",
          "sayı değil). ⚠️ Tezde bir sayı savunulacaksa bu sütun **✅** olmalı.", "",
          "| | katkı |", "|---|---:|"]
    for k, v in sorted(sinif.items()):
        L.append(f"| {k} | **{v}** |")
    L += [f"| ⚠️ betik göstermeyen | {len(betiksiz)} |", "",
          "⚪ **«rapor üretmiyor»** bir kusur değil: denetim yalnızca "
          "`reports/analiz/*.md` **üreten** betikleri kapsar; bir koşu başlatıcısı "
          f"({len(kapsamdisi)} katkıda) rapor yazmaz. ⭐ Raporu **olduğu hâlde** "
          "denetimde görünmeyen betik ise gerçek bir açıktır ve ayrı sayıldı.", ""]
    if sapan:
        L += ["| katkı | betik | yeniden üretilebilirlik |", "|---|---|---|"]
        for t, b, d in sapan:
            L.append(f"| {t} | " + ", ".join(f"`{x}`" for x in b) + " | "
                     + ", ".join(d) + " |")
        kendi = YENIDEN.stem + ".py"
        if any(kendi in b for _t, b, _d in sapan):
            L += ["", f"⚠️ `{kendi}` **denetimin KENDİSİ** ve kendini kapsamına almıyor —",
                  "bir betik kendi koşusunun içinde kendini yeniden koşamaz. Bu yapısal bir",
                  "dışlama, kusur değil; yine de gizlenmiyor: o betiğin ürettiği sayının",
                  "(Kural 7 yüzdesi) **kendi denetimi yok** ve tezde bu yazılmalı.", ""]
        L += ["", "⛔ Bu katkıların **sayıları** tezde ancak yanına *«şu tarihte şu girdiyle",
              "ölçüldü, bugün yeniden üretilemiyor»* notu düşülerek yazılabilir. Kural 7'nin",
              "kendi ölçütü bu.", ""]

    # --- 4. çapraz atıflar ----------------------------------------------------
    kirik_atif = []
    for r in ROW:
        for harf, no in ATIF.findall(r[-1] if len(r) > 5 else ""):
            ad = f"{harf}{no}"
            if harf == "T" and ad not in T_VAR:
                kirik_atif.append((r[0], ad))
            if harf == "K" and ad not in K_VAR:
                kirik_atif.append((r[0], ad))
    L += ["## 4. Çapraz atıflar tutuyor mu", "",
          f"`İlgili` sütunundaki her `T##` defterde, her `K##` `PROJECT_MEMORY.md`'de",
          f"aranıyor. Hafızada bulunan karar sayısı: **{len(K_VAR)}**.", ""]
    if kirik_atif:
        L += ["| katkı | bulunamayan atıf |", "|---|---|"]
        L += [f"| {t} | `{a}` |" for t, a in kirik_atif]
        L += [""]
    else:
        L += ["✅ **Kırık atıf yok** — defterdeki her `T##` ve `K##` karşılığını buluyor.", ""]

    # --- 5. kırık atfın ardındaki artefakt ------------------------------------
    if kirik_atif:
        eksik_k = sorted({a for _t, a in kirik_atif if a.startswith("K")})
        L += ["### ⭐ Kırık atıf bir BOŞLUĞU mu gösteriyor", "",
              "Bir atıf tutmuyorsa iki şey olabilir: yanlış numara yazılmış, ya da **karar",
              "hiç yazılmamış**. İkincisi tez için daha ağırdır: karar verilmiş, uygulanmış,",
              "başka kayıtlardan atıf almış — ama **gerekçesi hiçbir yerde yok**.", ""]
        for ad in eksik_k:
            nerede = [s2 for s2 in hafiza.split("\n") if ad in s2]
            satir_no = [re.match(r"^\|\s*(K\d+)\s*\|", x).group(1)
                        for x in nerede if re.match(r"^\|\s*K\d+\s*\|", x)]
            L += [f"**`{ad}`** — `PROJECT_MEMORY.md`'de **satırı yok**; buna karşılık "
                  f"**{len(nerede)}** yerde atıf alıyor"
                  + (f" (" + ", ".join(f"`{k}`" for k in satir_no) + " satırlarından)"
                     if satir_no else "") + ".", ""]
        kar = KOK / "data/guvenlik-karantinasi.jsonl"
        if kar.exists():
            n = sum(1 for _ in kar.open(encoding="utf-8"))
            L += [f"⛔⭐ **Ve artefaktı DURUYOR:** `data/guvenlik-karantinasi.jsonl` "
                  f"({n} kayıt, SHA256 `{sha(kar)}`). Yani karar uygulandı — klinik güvenlik "
                  "ihlali alan kayıtlar silinmeyip karantinaya alındı — ama **gerekçesi "
                  "yazılmadı**. ➡️ *Bir kararın izini artefakt taşıyorsa ve gerekçe defteri "
                  "taşımıyorsa, tezde savunulacak olan şey kaybolmuş demektir: ne yapıldığı "
                  "değil, NEDEN yapıldığı.* ⚠️ İçeriği burada uydurulmuyor — bu bir "
                  "**yürütücü kalemi** (Kural 3: klinik güvenlik kararı).", ""]

    # --- özet -------------------------------------------------------------------
    savunulabilir = sum(1 for t, b, d in betikli
                        if d and all(x.startswith(("✅", "⏭️", "⚪")) for x in d)
                        and any(x.startswith("✅") for x in d))
    L += ["## ⭐ Özet — tezde bugün savunulabilir olanlar", "", "| | |", "|---|---:|",
          f"| katkı | {len(ROW)} |",
          f"| ⭐ **kanıt dosyası + betiği yeniden üretiliyor** | **{savunulabilir}** |",
          f"| ⛔ betiği sapıyor ya da raporu denetim dışında | {len(sapan)} |",
          f"| ⚪ yalnızca koşu/üretim betiği gösteriyor (kapsam dışı) | {len(kapsamdisi)} |",
          f"| ⚠️ betik göstermiyor (ölçüm değil, argüman/tasarım katkısı olabilir) | {len(betiksiz)} |",
          f"| ⛔ hiç dosya göstermiyor | {len(kanitsiz)} |", "",
          "➡️ *Bu sayı bir kalite ölçüsü DEĞİL:* bir katkı betiksiz olabilir ve yine de",
          "güçlü olabilir (tasarım ilkesi, elenen alternatif, literatür boşluğu). Ölçülen",
          "şey **tezde hangi satırın yanına sayı yazılabileceği**.", "",
          "## ⛔ Bu denetimin söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ Katkının **doğruluğu** | yargılanmadı; yalnızca mekanik savunulabilirlik |",
          "| ⛔ Katkının **özgünlüğü** | literatür taraması bu betiğin işi değil (T1 hâlâ açık) |",
          "| ⚠️ Yol çıkarımı **dizgeye dayalı** | metinde geçen ``yol`` kalıbı aranıyor; "
          "düzyazıyla anlatılan bir kanıt görünmez (T57'nin sınıfı) |",
          "| ⚠️ `Durum` sütunu | efsaneye uymayan satırlarda sınıflandırma yapılmadı — "
          "hangi katkının `kanıtlı` hangisinin `iddia` olduğu makineyle okunamıyor |", ""]

    RAPOR.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print(f"   katkı {len(ROW)} · savunulabilir {savunulabilir} · sapan {len(sapan)} · "
          f"betiksiz {len(betiksiz)} · kanıtsız {len(kanitsiz)} · "
          f"kırık yol {len(kirik)} · kırık atıf {len(kirik_atif)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
