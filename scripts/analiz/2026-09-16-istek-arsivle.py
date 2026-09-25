#!/usr/bin/env python3
"""Judge İŞ DOSYALARINI (`istek/*.txt`) arşivle — Kural 7'nin kayıp halkası.

Neden: `ham-judge/*.jsonl` yalnızca judge'ın NE DÖNDÜĞÜNÜ saklıyor; NE OKUDUĞUNU
saklamıyor. İkisi arasındaki fark, 2026-09-15 ve 09-16'da iki kez belirleyici oldu:
`korpus-v9-p2` ve `korpus-v8` kusurlarının «judge yanlış okudu» değil «sonuç yanlış
dosyaya YAZILDI» olduğunu ancak `istek/NNN.txt` gösterebildi (K123, K124).

⛔ İş dosyaları oturum scratchpad'inde duruyor ve Kural 8 oturum sonunda siliyor.
`korpus-v3-claude` ÇOKTAN kayboldu: ham sonuçları arşivde, iş dosyaları yok.
Bu betik kalanları repoya alır — 27 MB ham, gzip'le ~1 MB.

Girdi : <scratchpad>/judge-isleri/<aile>/istek/*.txt
Çıktı : reports/analiz/ham-judge/istek/<aile>.jsonl.gz  +  bu tarihli rapor
Kullanım: uv run python scripts/analiz/2026-09-16-istek-arsivle.py
"""
from __future__ import annotations

import gzip
import hashlib
import io
import json
import os
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]
ISLER = Path(os.environ.get(
    "BIRAG_JUDGE_ISLERI",
    "/private/tmp/claude-501/-Users-pc-projects-birag-data-finetuning"
    "/fe6477c2-8e5e-439e-875d-df2b5ed62d91/scratchpad/judge-isleri"))
ARSIV = KOK / "reports/analiz/ham-judge"
HEDEF = ARSIV / "istek"
RAPOR = KOK / f"reports/analiz/{TARIH}-istek-arsivle.md"


def yaz(yol: Path, satirlar: list[str]) -> int:
    """mtime=0 ile gzip — aynı girdi aynı baytı versin (yoksa arşiv her koşuda 'değişti')."""
    tampon = io.BytesIO()
    with gzip.GzipFile(fileobj=tampon, mode="wb", compresslevel=9, mtime=0) as g:
        g.write("".join(satirlar).encode("utf-8"))
    ham = tampon.getvalue()
    if yol.exists() and yol.read_bytes() == ham:
        return len(ham)
    yol.write_bytes(ham)
    return len(ham)


def ortak_onek(metinler: list[str]) -> int:
    """K103: aynı ailedeki iş dosyaları aynı rubrik önekini taşımalı."""
    if len(metinler) < 2:
        return len(metinler[0]) if metinler else 0
    a, b = min(metinler), max(metinler)
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


def main() -> None:
    HEDEF.mkdir(parents=True, exist_ok=True)
    arsivli = sorted(p.stem for p in ARSIV.glob("*.jsonl"))
    satir_aile, toplam_ham, toplam_gz = [], 0, 0

    for aile in sorted(d.name for d in ISLER.iterdir() if (d / "istek").is_dir()) \
            if ISLER.is_dir() else []:
        dosyalar = sorted((ISLER / aile / "istek").glob("*.txt"))
        if not dosyalar:
            continue
        metinler, satirlar, ham = [], [], 0
        for p in dosyalar:
            m = p.read_text(encoding="utf-8")
            metinler.append(m)
            ham += len(m.encode("utf-8"))
            satirlar.append(json.dumps({
                "no": p.stem,
                "sha256": hashlib.sha256(m.encode("utf-8")).hexdigest(),
                "bayt": len(m.encode("utf-8")),
                "istek": m,
            }, ensure_ascii=False) + "\n")
        gz = yaz(HEDEF / f"{aile}.jsonl.gz", satirlar)
        onek = ortak_onek(metinler)
        toplam_ham += ham
        toplam_gz += gz
        satir_aile.append((aile, len(dosyalar), ham, gz, onek,
                           aile in arsivli))

    # ham sonucu arşivde olup iş dosyası KURTARILAMAYAN aileler
    kurtarilan = {a for a, *_ in satir_aile}
    kayip = [a for a in arsivli if a not in kurtarilan]

    L = [f"# Judge iş dosyaları arşivi — `ham-judge` neyi saklamıyordu", "",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
         f"**Kaynak:** oturum scratchpad'i `judge-isleri/<aile>/istek/` "
         f"(⛔ Kural 8 oturum sonunda siler)  ",
         f"**Çıktı:** `reports/analiz/ham-judge/istek/<aile>.jsonl.gz`", "", "---", "",
         "## Neden",
         "",
         "`ham-judge/*.jsonl` judge'ın **ne döndüğünü** saklıyor; **ne okuduğunu**",
         "saklamıyor. İki kusur vakasında (K123 `korpus-v9-p2`, K124 `korpus-v8`)",
         "*«judge yanlış okudu»* ile *«sonuç yanlış dosyaya yazıldı»* ayrımını yapan",
         "tek kanıt `istek/NNN.txt` oldu. O dosyalar repoda değildi.", "",
         f"## Arşivlenen — {len(satir_aile)} aile · "
         f"{sum(s[1] for s in satir_aile)} iş dosyası", "",
         "| Aile | dosya | ham | gzip | ortak önek (K103) | ham sonuç arşivde |",
         "|---|---:|---:|---:|---:|:--:|"]
    for aile, n, ham, gz, onek, var in satir_aile:
        L.append(f"| `{aile}` | {n} | {ham/1024:.0f} KB | {gz/1024:.0f} KB | "
                 f"{onek} krk | {'✅' if var else '⚠️'} |")
    L += [f"| **TOPLAM** | **{sum(s[1] for s in satir_aile)}** | "
          f"**{toplam_ham/1048576:.1f} MB** | **{toplam_gz/1048576:.2f} MB** | | |", "",
          f"➡️ Sıkıştırma **{toplam_ham/max(toplam_gz,1):.0f}×** — iş dosyalarının",
          "büyük kısmı ailede ortak olan rubrik öneki (K103: kuyruklar bayt-aynı).", ""]

    L += ["## ⛔ Kurtarılamayan — ham sonucu var, iş dosyası yok", ""]
    if kayip:
        L += [f"**{len(kayip)} aile:** " + " · ".join(f"`{a}`" for a in kayip), "",
              "Bu ailelerde bir sonuç-kayıt kayması bulunursa **judge kusuru mu yazma",
              "kusuru mu** olduğu gösterilemez. Ham sonuç arşivde olduğu için",
              "`eslesme_denetimi()` yine koşar — ama ayrımı yapamaz.", ""]
    else:
        L += ["_Yok._", ""]

    L += ["## ⭐ Karar", "",
          "| | |", "|---|---|",
          f"| ✅ Arşivlendi | {len(satir_aile)} aile · "
          f"{sum(s[1] for s in satir_aile)} iş dosyası · {toplam_gz/1048576:.2f} MB |",
          f"| ⛔ Geri alınamaz | {len(kayip)} aile — iş dosyaları oturumla birlikte gitti |",
          "| ➡️ Kural 8 | judge iş dizini artık **silinmeden önce arşivlenir**; "
          "bu betik oturum sonu yordamının parçası |", ""]

    RAPOR.write_text("\n".join(L), encoding="utf-8")
    print(f"{len(satir_aile)} aile arşivlendi · {toplam_gz/1048576:.2f} MB · "
          f"kurtarılamayan {len(kayip)} · yazıldı: {RAPOR.relative_to(KOK)}")


if __name__ == "__main__":
    main()
