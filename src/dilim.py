"""`slice` alanının TEK evi — beyan edilmez, TÜRETİLİR.

⛔⛔ **Neden (T240).** Alanın anlamı v5 ile v6 arasında **sessizce değişti**:
v4/v5'te `rag_*` kayıtların %100'ünde bağlam belgesi vardı ve `terapotik_*`
kayıtların %0'ında — alan tam bilgi taşıyordu. v6'da sözlük iki değere düştü
(`rag_tek_tur`, `cok_tur`), `terapotik_*` kayboldu, ve `rag_tek_tur`
kayıtların yalnız %35'inde bağlam kaldı. Aynı ad, iki anlam, iki dönem aynı
korpusun içinde. Dört katman da kördü: `schemas.py`'de alan `slice: str`
(`Literal` değil), `checks.py`'de denetim yok, birleştirme raporu saymıyor,
judge görmüyor.

⭐ **Çözüm beyanı düzeltmek değil, beyanı KALDIRMAK.** Dilim iki bağımsız
eksenden oluşur ve ikisi de kaydın içinde zaten yazılıdır:

  · **kip** — `context` DOLU mu? → `rag` : `terapotik`
  · **tur** — kaç `user` turu var? → `cok_tur` (>1) : `tek_tur`

⇒ Alan kendisiyle çelişemez hâle gelir. ⛔ `replay` dilimi bir ÜÇÜNCÜ şeydir
(§9, genel amaçlı talimat-cevap) ve iki eksenle anlatılamaz; kayıt
`replay=True` taşıyorsa dilim `replay`'dir.

⭐ **Kural v4/v5'e karşı sınandı: 460 kaydın 459'unda beyanı birebir yeniden
üretiyor.** Tek uyuşmazlık `v4-parti1 / d001bc7a8f` — ve o zaten **K69**'un
belgelenmiş kusuru: `kayit()`'in `slice_="terapotik_tek_tur"` varsayılanı
çok turlu bir kaydı tek tur diye damgalamıştı. ⇒ Türetme, beyanı yeniden
üretmekle kalmıyor, beyanın **yanlış olduğu tek yeri de gösteriyor**.
"""
from __future__ import annotations

import re

DILIMLER = ("terapotik_tek_tur", "terapotik_cok_tur",
            "rag_tek_tur", "rag_cok_tur", "replay")


def dilim(record: dict) -> str:
    """⛔ KARAR VERMEZ, OKUR. Kaydın kendi alanlarından dilimi türetir."""
    if record.get("replay"):
        return "replay"
    kip = "rag" if record.get("context") else "terapotik"
    n_user = sum(1 for m in record.get("messages", []) if m.get("role") == "user")
    return f"{kip}_{'cok_tur' if n_user > 1 else 'tek_tur'}"


def dilim_tutarli(record: dict) -> tuple[bool, str | None]:
    """Beyan edilen `slice` türetilenle uyuşuyor mu?

    ⭐ Kapı, T237'nin dersinin uygulanması: *bir sınır yazıldığında aynı
    commit'te onu uygulayan kod da yazılır.* Alan türetilebilir olduğu hâlde
    kayıtta saklanmayı sürdürüyor (geriye dönük okunabilirlik için) ⇒ ikisinin
    ayrışması sessiz kalmamalı.
    """
    beklenen = dilim(record)
    var = record.get("slice")
    if var is None:
        return True, None                  # alan yoksa denetlenecek bir şey yok
    if var == beklenen:
        return True, None
    return False, f"slice beyanı '{var}', türetilen '{beklenen}'"


# ⛔⛔ ÜÇÜNCÜ AYNI KUSUR. `slice` (T240) ve `gen_meta.date` (T244) beyan
#   edilip sessizce kaymıştı; `gen_meta.bicim` de aynı sözlükte ve aynı
#   biçimde. `celiskili` pilotunda **elle beyan ettiğim iki bant yanlış
#   çıktı** (16 sözcüğe «kisa», 29 sözcüğe «orta») ve **hiçbir kapı
#   görmedi** — okuyarak buldum.
# ⭐ Eşikler v4 §6'dan: kisa ≤8 · orta 9-25 · uzun >25. Bağlam pasajı
#   çıkarılır (T233: `<CTX>` yer tutucusu sözcük sayılıp sahte bant ihlali
#   üretmişti).
_CTX = re.compile(r"<context.*?</context>|<CTX>", re.S)


def bant(record: dict) -> str | None:
    """İLK kullanıcı mesajının bandı. ⛔ KARAR VERMEZ, SAYAR."""
    u = [m for m in record.get("messages", []) if m.get("role") == "user"]
    if not u:
        return None
    n = len(_CTX.sub(" ", u[0].get("content") or "").split())
    return "kisa" if n <= 8 else "orta" if n <= 25 else "uzun"


def bant_tutarli(record: dict) -> tuple[bool, str | None]:
    """Beyan edilen `gen_meta.bicim` sayılanla uyuşuyor mu?"""
    var = (record.get("gen_meta") or {}).get("bicim")
    if var is None or record.get("replay"):
        return True, None
    bek = bant(record)
    if bek is None or var == bek:
        return True, None
    return False, f"bicim beyanı '{var}', sayılan '{bek}'"
