"""Üretim künyesinin türetilen alanları — tek ev.

⛔⛔ **Neden (T243).** `gen_meta.date` üretim betiklerinde **elle yazılıydı**
ve bir partiden ötekine **kopyalanıyordu**. Sonuç: `v6-parti5`'in 60 kaydı ve
`v6-parti8`'in 118 kaydı, kendilerini üreten betiğin adındaki tarihten **bir
gün önceyi** taşıyor — toplam **178 kayıt**.

⭐ **Mekanizma tanıdık ve dersi keskin.** Aynı sözlükte `parti` alanı da sabit
yazılıydı, aynı kusuru üretti, yakalandı ve **türetilir** yapıldı
(`CIKTI.stem`'den). `date` **yanı başındaydı** ve düzeltilmedi.
➡️ *Bir şablondaki bir beyanı türetmeye çevirmek, komşusunu düzeltmez.*

⭐ Kural yeni değil: **K126** raporlar için zaten *«tarih betik ADINDAN»*
diyor. Burada yapılan, aynı kuralı üretim künyesine de uygulamak.
"""
from __future__ import annotations

import re
from pathlib import Path

TARIH_DESENI = re.compile(r"^(\d{4}-\d{2}-\d{2})")


def betik_tarihi(dosya: str) -> str:
    """⛔ KARAR VERMEZ, OKUR. Betiğin ADINDAN tarihi alır (K126).

    `dosya` her zaman `__file__`'dir. Betik adı `YYYY-MM-DD-` ile
    başlamıyorsa **hata verir** — sessizce bugüne düşmez, çünkü o zaman alan
    yine beyan olurdu, yalnız beyan edeni değişirdi.
    """
    m = TARIH_DESENI.match(Path(dosya).name)
    if not m:
        raise ValueError(
            f"betik adı YYYY-MM-DD ile başlamıyor: {Path(dosya).name} — "
            "künye tarihi türetilemez (K126)")
    return m.group(1)
