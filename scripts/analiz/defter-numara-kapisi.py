"""Katkı defteri ve karar kaydı için numara tahsis kapısı.

2026-09-22'de on dakika içinde **iki kez** aynı numara iki ayrı katkıya verildi
(`T246`, sonra `T247`): iki oturum aynı artefaktı aynı anda numaralandırdı ve
bunu hiçbir şey görmedi. Çakışma tez artefaktında yanlış çapraz atıf üretir —
ilkinde 31 şerh yanlış kaydı gösteriyordu.

T237'nin dersi: *«kural yazılı, kapı yok»* ⇒ çaresi kapıdır.
T180'in dersi: yeniden koşulabilir bir betikte **ad kimliktir, tarih değil** —
bu yüzden dosya adında tarih yok.

Kullanım:
    uv run python scripts/analiz/defter-numara-kapisi.py          # denetle
    uv run python scripts/analiz/defter-numara-kapisi.py --sonraki # boş numara

Çıkış kodu 1 = çakışma var.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]

KAYNAKLAR: list[tuple[str, Path, re.Pattern[str]]] = [
    ("T", KOK / "docs" / "tez" / "katki-defteri.md", re.compile(r"^\|\s*T(\d+)\s*\|")),
    ("K", KOK / "PROJECT_MEMORY.md", re.compile(r"^\|\s*K(\d+)\s*\|")),
]


def numaralari_oku(yol: Path, desen: re.Pattern[str]) -> list[int]:
    numaralar = []
    for satir in yol.read_text(encoding="utf-8").splitlines():
        m = desen.match(satir)
        if m:
            numaralar.append(int(m.group(1)))
    return numaralar


def main() -> int:
    sonraki_mi = "--sonraki" in sys.argv
    kusurlu = False

    for onek, yol, desen in KAYNAKLAR:
        numaralar = numaralari_oku(yol, desen)
        if not numaralar:
            print(f"⛔ {yol.name}: hiç {onek} satırı bulunamadı — desen bozulmuş olabilir")
            kusurlu = True
            continue

        sayac = Counter(numaralar)
        cakisan = sorted(n for n, adet in sayac.items() if adet > 1)
        en_buyuk = max(numaralar)

        if sonraki_mi:
            print(f"{onek}: en büyük {onek}{en_buyuk} · sıradaki boş → **{onek}{en_buyuk + 1}**")
            continue

        durum = "⛔ ÇAKIŞMA" if cakisan else "✅"
        print(
            f"{durum} {yol.relative_to(KOK)}: {len(numaralar)} satır, "
            f"tekil {len(sayac)}, en büyük {onek}{en_buyuk}"
        )
        if cakisan:
            kusurlu = True
            for n in cakisan:
                print(f"   ⛔ {onek}{n} × {sayac[n]} kez")

    if sonraki_mi:
        return 0

    if kusurlu:
        print(
            "\n⛔ Numara çakışması, tez artefaktında yanlış çapraz atıf demektir.\n"
            "   Çözüm kuralı (2026-09-22'de iki kez uygulandı): **taşınan**, "
            "deponun içinde\n   daha AZ atıf alan kayıttır; eşitlikte önce "
            "commit'lenen yerinde kalır."
        )
    return 1 if kusurlu else 0


if __name__ == "__main__":
    raise SystemExit(main())
