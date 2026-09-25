"""Muafiyet defteri — bir kapının BAĞIŞLADIĞI her öge buraya yazılır.

⛔⛔ **Neden var (T140).** Yapısal atıf kapısında `len(turlar) < 2 → continue`
muafiyeti, *«aynı mesajda»* için doğru yazılmıştı ama *«aynı cümlede»* için de
ateşliyordu ve kapının kendi ayrımını yok ediyordu. Kusuru kapı değil **judge**
buldu; muafiyet düzeltilince elle okuma yükü 10'dan 26'ya çıktı, yani muafiyet
denetimin üçte ikisini sessizce siliyordu.

➡️⭐ *Bir kapının YAKALADIKLARI raporlanıyor ama BAĞIŞLADIKLARI raporlanmıyorsa,
muafiyetin ne kadar genişlediği sorulamaz. Bir muafiyet sayılmadıkça denetlenemez.*

⭐ **Sözleşme iki maddelik:**
  1. Her `continue` — yani «bu aday kusur değil» kararı — `yaz()` çağırır.
  2. Muafiyet ancak **ADAY** varken kaydedilir: deseni hiç eşleşmeyen bir cümleyi
     «muaf tuttum» diye saymak defteri şişirir ve denetimi yine kör eder.

⚠️ Defter kapının KARARINI değiştirmez; yalnız kararı görünür kılar. Bulgu sayısı
defter eklenmeden önce ve sonra aynı olmalıdır — `2026-09-17-muafiyet-denetimi.py`
bunu sınar.

⭐⭐ **ÜÇ TİP (2026-09-17, öteki beş kapı sayılırken ayrıldı).** İlk üç kapının
bağışları tek türdendi; beş kapıya bakınca tür ayrımı zorunlu oldu:

  · `muafiyet` — ADAY var, kapı *«kusur değil»* diyor. Bağışlanan bir kusur olabilir.
  · `kapsam`   — metin daha aday olmadan dışarıda; karar İLAN EDİLMİŞ ve gerekçeli
    (ör. §15 yalnız asistan tarafını kısıtlar, T62). Kusur saklayabilir ama
    sakladığı şey kapının ilan ettiği sınırın dışındadır.
  · `sessiz`   — metin dışarıda ve bunu kimse ilan etmemiş: ayrıştırılamayan satır,
    ölçülemez sayılan kısa metin, referansı olmadığı için hiç sınanmayan öge.
    ⛔⛔ **Tehlikeli tip budur:** T143'ün dersi tam burada genelleşiyor — *bir
    kapının sessizliği «kusur yok» değil, «o metne hiç bakmadım» demek olabilir.*

➡️ *Üçü aynı kefeye konursa sayı okunamaz: ilan edilmiş bir sınır ile sessizce
yutulmuş bir satır aynı şey değildir.*
"""
from __future__ import annotations

DEFTER: list[dict] = []


def sifirla() -> None:
    DEFTER.clear()


def yaz(ad: str, kayit: dict, oge, baglam: str = "", tip: str = "muafiyet") -> None:
    """Bir bağışın ateşlediğini kaydeder. `ad` bağışın adı, `oge` bağışlanan şey.

    `tip`: muafiyet / kapsam / sessiz — yukarıdaki üç tip.
    """
    assert tip in ("muafiyet", "kapsam", "sessiz"), tip
    kayit = kayit or {}
    DEFTER.append({
        "muafiyet": ad,
        "tip": tip,
        "parti_sira": (kayit.get("gen_meta") or {}).get("parti_sira"),
        "id": kayit.get("id"),
        "oge": oge if isinstance(oge, str) else list(oge),
        "baglam": (baglam or "")[:200],
    })


def ozet() -> dict[str, int]:
    s: dict[str, int] = {}
    for m in DEFTER:
        s[m["muafiyet"]] = s.get(m["muafiyet"], 0) + 1
    return s
