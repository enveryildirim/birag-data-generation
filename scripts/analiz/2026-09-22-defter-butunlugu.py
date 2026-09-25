#!/usr/bin/env python3
"""Katkı defteri bütünlük denetimi — beş ayrı kopukluk arar.

⛔⛔ **Neden (bugün üç kez oldu).** Bir yama betiği düştü, `write_text` hiç
koşmadı, ama commit *«T261 yazıldı»* diyordu. Üç kez. ⇒ K66/T237 ailesi:
kural yazılı (*«her iddia deftere»*) ama **onu denetleyen hiçbir şey yok**.

⭐ Ayrıca bugün numaralar paralel bir oturumla **çakıştı** ve elle yeniden
numaralandı (K271); yeniden numaralamanın atıfları bozup bozmadığını da
yalnız böyle bir denetim gösterebilir.

Aranan beş kopukluk:
  1. **çakışan numara** — aynı `Tn` iki kez
  2. **kopuk 📎** — kalemin işaret ettiği betik/rapor dosyada yok
  3. **ölü atıf** — kalem içinde geçen `Txxx` defterde yok
  4. **defterе girmemiş rapor** — `reports/analiz/` altında olup hiçbir
     kalemin işaret etmediği rapor (Kural 7'nin tersi yönü)
  5. **commit ↔ defter kopukluğu** — commit iletisi `Tn:` diyor ama `Tn`
     defterde yok (bugünün kusuru tam bu)

⛔ Bu betik **hiçbir şeyi düzeltmez**, yalnız sayar ve listeler.

Kullanım: uv run python <betik> [--gun 2026-09-22]
Çıktı: reports/analiz/2026-09-22-defter-butunlugu.md
"""
from __future__ import annotations

import collections
import re
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-defter-butunlugu.md"
DEFTER = KOK / "docs/tez/katki-defteri.md"
GUN = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--gun=")), TARIH)
YOL = re.compile(r"`((?:scripts|reports|src|docs|datasets|data|configs|evals|prompts)/[^`\s]+)`")
ATIF = re.compile(r"\bT(\d{1,3})\b")


def main() -> int:
    metin = DEFTER.read_text(encoding="utf-8")
    satir = {}
    for l in metin.splitlines():
        m = re.match(r"^\| (T\d+) \|", l)
        if m:
            satir.setdefault(m.group(1), []).append(l)

    # 1) çakışan numara
    cakisan = {k: len(v) for k, v in satir.items() if len(v) > 1}

    # 2) kopuk 📎 — yalnız 📎'den SONRAKİ yollar (gövdedeki örnek yollar değil)
    kopuk = []
    for k, ls in satir.items():
        for l in ls:
            if "📎" not in l:
                continue
            for y in YOL.findall(l.split("📎", 1)[1]):
                # ⛔ `…-t{7,13,23}.yaml` bir yol DEĞİL, kısaltma yazımıdır.
                #   İlk sürüm bunları kopuk sandı — kapının kendi yanlış
                #   pozitifi, okuyarak bulundu.
                if "{" in y:
                    import itertools
                    govde = re.split(r"\{([^}]*)\}", y)
                    parcalar = [[x] if i % 2 == 0 else x.split(",")
                                for i, x in enumerate(govde)]
                    if all((KOK / "".join(c)).exists()
                           for c in itertools.product(*parcalar)):
                        continue
                    kopuk.append((k, y + " ⚠️ kısaltma açılımı eksik"))
                elif "::" in y:
                    # ⛔ `dosya.py::sembol` bir yol DEĞİL — kapının İKİNCİ
                    #   yanlış pozitif ailesi, yine okuyarak bulundu (T263).
                    #   Susturmak yerine kapı GÜÇLENDİRİLİR: dosya var mı VE
                    #   sembol o dosyada tanımlı mı?
                    d, _, sem = y.partition("::")
                    f = KOK / d
                    if not f.exists():
                        kopuk.append((k, d))
                    elif not re.search(rf"^\s*(def|class)\s+{re.escape(sem)}\b",
                                       f.read_text(encoding="utf-8"), re.M):
                        kopuk.append((k, y + " ⚠️ dosya var, sembol tanımlı değil"))
                elif not (KOK / y).exists():
                    kopuk.append((k, y))

    # 3) ölü atıf
    var = set(satir)
    olu = []
    for k, ls in satir.items():
        for l in ls:
            for n in set(ATIF.findall(l)):
                if f"T{n}" != k and f"T{n}" not in var:
                    olu.append((k, f"T{n}"))

    # 4) deftere girmemiş rapor (yalnız GUN tarihli olanlar)
    anilan = set(YOL.findall(metin))
    girmemis = sorted(
        str(p.relative_to(KOK)) for p in (KOK / "reports/analiz").glob(f"{GUN}-*.md")
        if str(p.relative_to(KOK)) not in anilan)

    # 5) commit ↔ defter
    try:
        log = subprocess.run(["git", "log", f"--since={GUN} 00:00", "--format=%h%x09%s"],
                             cwd=KOK, capture_output=True, text=True, check=True).stdout
    except Exception:
        log = ""
    commit_kopuk = []
    for l in log.splitlines():
        if "\t" not in l:
            continue
        h, s = l.split("\t", 1)
        m = re.match(r"^(T\d+)\s*[:：]", s)
        if m and m.group(1) not in var:
            commit_kopuk.append((h, m.group(1), s[:60]))

    toplam = (len(cakisan) + len(kopuk) + len(olu) + len(girmemis) + len(commit_kopuk))
    sat = ["# Katkı defteri bütünlük denetimi", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Defter:** {len(satir)} kalem · **gün süzgeci:** {GUN}  ",
           f"**Bulgu:** {'⭐ **kopukluk yok**' if not toplam else f'⛔ **{toplam} kopukluk**'}  ", "",
           "⛔⛔ **Neden var:** bugün üç kez bir yama betiği düştü, `write_text` "
           "hiç koşmadı, ama commit *«kalem yazıldı»* dedi. K66/T237 ailesi — "
           "kural yazılı, kapı yok. Bu betik o kapıdır (ölçen türden).", "",
           "## Sonuç", "", "| kopukluk | sayı |", "|---|---:|",
           f"| 1. çakışan numara | {len(cakisan)} |",
           f"| 2. kopuk 📎 (dosya yok) | {len(kopuk)} |",
           f"| 3. ölü atıf (kalem yok) | {len(olu)} |",
           f"| 4. deftere girmemiş rapor ({GUN}) | {len(girmemis)} |",
           f"| 5. commit ↔ defter kopukluğu | {len(commit_kopuk)} |", ""]
    for ad, veri, bicim in (
            ("1. Çakışan numaralar", cakisan, lambda x: f"`{x}` ({cakisan[x]} kez)"),
            ("2. Kopuk 📎", kopuk, lambda x: f"`{x[0]}` → `{x[1]}`"),
            ("3. Ölü atıflar", olu, lambda x: f"`{x[0]}` → **{x[1]}** (yok)"),
            ("4. Deftere girmemiş raporlar", girmemis, lambda x: f"`{x}`"),
            ("5. Commit ↔ defter", commit_kopuk,
             lambda x: f"`{x[0]}` **{x[1]}** — *«{x[2]}»*")):
        if not veri:
            continue
        sat += [f"### ⛔ {ad}", ""]
        sat += [f"- {bicim(x)}" for x in (veri if not isinstance(veri, dict) else veri)]
        sat += [""]
    sat += ["## ⛔ Bu denetimin söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **İçeriği denetlemez** | bir kalemin **yazılmış** olduğunu "
            "gösterir, **doğru** olduğunu değil |",
            "| ⛔ **4. madde yalnız bir günü tarar** | `--gun` ile değişir; "
            "bütün geçmiş taranmıyor çünkü eski raporların bir kısmı bilerek "
            "kalemsizdir |",
            "| ⛔ **5. madde commit iletisi biçimine bağlı** | yalnız `Tn:` ile "
            "**başlayan** iletiler denetlenir; başka biçimde anılan kalemler "
            "görünmez |",
            "| ⛔ **Kapının kendi yanlış pozitifi vardı** | ilk sürüm `…-t{7,13,23}.yaml` kısaltma yazımını kopuk yol sandı; **okuyarak** bulundu ve açılım eklendi — T22 ailesinin biçimi |",
            "| ⚠️ **2. madde yalnız 📎'den sonrasına bakar** | gövde içinde "
            "örnek olarak geçen yollar denetlenmez, yoksa yanlış pozitif olur |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[sat.index("## Sonuç"):]))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
