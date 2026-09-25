#!/usr/bin/env python3
"""Raporların İLAN ETTİĞİ SHA256 gerçekten o dosyanın mı — Kural 7'nin sağlaması.

⛔ Nasıl bulundu: üç eval raporunun ilan ettiği SHA, adını verdiği mühürlü
dosyanınki DEĞİLDİ (K130). Sebep üretici-raporlayıcı bitişikliği: rapor, zincirin
BİRİNCİ adımının ürettiği öğeleri anlatıyordu; mühürlenen dosya ise İKİNCİ adımın
çıktısıydı. İki ayrı nesne, tek rapor. `**Kapı:** 16/20` yazıyordu, mühürlü set
20/20 geçiyor — rapor kendi setini kötü gösteriyordu.

➡️ *Bir rapor girdi/çıktı dosyasının SHA'sını yazıyorsa o SHA SAĞLANABİLİR bir
iddiadır. Sağlanmadığı sürece, raporun anlattığı nesnenin adını verdiği nesne
olduğunun güvencesi yoktur.*

Girdi : reports/analiz/*.md (ilan edilen her `dosya` + SHA256 çifti)
Çıktı : reports/analiz/2026-09-16-ilan-edilen-sha-denetimi.md
Çıkış kodu: tutmayan varsa 1 — kapı olarak koşulabilir.
Kullanım: uv run python scripts/analiz/2026-09-16-ilan-edilen-sha-denetimi.py
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-ilan-edilen-sha-denetimi.md"

# `yol.uzantı` … SHA256 … `hex` — araya "·", "**", boşluk girebilir; kısaltılmış
# (16 karakter + "…") ilanlar da yakalanır ve ÖNEK olarak sağlanır.
DESEN = re.compile(
    r"`([^`\s]+\.(?:jsonl|json|md|py|txt|yaml|yml))`[^`\n]{0,80}?"
    r"SHA256[^`\n]{0,12}`([0-9a-f]{16,64})", re.I)  # lower-muaf: onaltılık hash — ASCII


def main() -> int:
    tutan, kayan, yok, disari = 0, [], [], []
    for p in sorted((KOK / "reports/analiz").glob("*.md")):
        if p.name == RAPOR.name:
            continue
        for satir in p.read_text(encoding="utf-8", errors="ignore").split("\n"):
          for yol, ilan in DESEN.findall(satir):
            # ⧉ = repo DIŞI girdi: SHA kayıtlı ama buradan doğrulanamaz. ⛔ Bunu
            # «dosya yok» saymak yanlış olurdu (kusur değil), sessizce atlamak da
            # (o zaman raporun dış bağımlılığı görünmez olurdu).
            if "⧉" in satir:
                disari.append((p.name, yol, ilan[:16]))
                continue
            h = KOK / yol
            if not h.exists():
                yok.append((p.name, yol))
                continue
            ger = hashlib.sha256(h.read_bytes()).hexdigest()
            if ger.startswith(ilan.rstrip("…")):
                tutan += 1
            else:
                kayan.append((p.name, yol, ilan[:16], ger[:16]))

    L = [f"# Raporların ilan ettiği SHA256 tutuyor mu", "",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
         f"**Kapsam:** `reports/analiz/*.md` içindeki her ``dosya`` + `SHA256` çifti",
         "", "---", "",
         "## Neden", "",
         "Bir rapor girdi ya da çıktı dosyasının SHA'sını yazıyorsa o SHA",
         "**sağlanabilir** bir iddiadır — ve sağlanmadığı sürece raporun anlattığı",
         "nesnenin, adını verdiği nesne olduğunun güvencesi yoktur.", "",
         "⛔ İlk koşuda üç eval raporu tutmadı: rapor zincirin **birinci** adımının",
         "öğelerini anlatıyor, mühürlenen dosya **ikinci** adımın çıktısıydı (K130).",
         "", "## Sonuç", "", "| | sayı |", "|---|---:|",
         f"| ✅ tutuyor | **{tutan}** |",
         f"| ⛔ tutmuyor | **{len(kayan)}** |",
         f"| ⚠️ adı geçen dosya yok | {len(yok)} |",
         f"| ⧉ repo DIŞI ilan (SHA kayıtlı, buradan doğrulanamaz) | {len(disari)} |",
         f"| **toplam ilan** | **{tutan + len(kayan) + len(yok)}** |", ""]
    if kayan:
        L += ["## ⛔ Tutmayanlar", "", "| Rapor | İlan edilen dosya | ilan | gerçek |",
              "|---|---|---|---|"]
        L += [f"| `{r}` | `{y}` | `{i}` | `{g}` |" for r, y, i, g in kayan]
        L += [""]
    if yok:
        L += ["## ⚠️ Adı geçen dosya yok", "", "| Rapor | Dosya |", "|---|---|"]
        L += [f"| `{r}` | `{y}` |" for r, y in yok] + [""]
    L += ["## ⭐ Karar", "", "| | |", "|---|---|",
          f"| {'✅' if not kayan else '⛔'} Durum | "
          f"{'her ilan sağlandı' if not kayan else f'{len(kayan)} ilan tutmuyor'} |",
          "| ➡️ Kapı | tutmayan varsa **çıkış kodu 1** — oturum sonu yordamına konabilir |",
          "| ⚠️ Kapsam | yalnızca SHA yazılmış ilanlar sağlanır; SHA **yazmayan** bir "
          "rapor bu denetimden sessizce geçer |", ""]

    RAPOR.write_text("\n".join(L), encoding="utf-8")
    print(f"✅ tutan {tutan} · ⛔ tutmayan {len(kayan)} · ⚠️ dosya yok {len(yok)} "
          f"· ⧉ repo dışı {len(disari)} "
          f"→ {RAPOR.relative_to(KOK)}")
    for r, y, i, g in kayan:
        print(f"  ⛔ {r} · {y} · ilan {i} gerçek {g}")
    return 1 if kayan else 0


if __name__ == "__main__":
    sys.exit(main())
