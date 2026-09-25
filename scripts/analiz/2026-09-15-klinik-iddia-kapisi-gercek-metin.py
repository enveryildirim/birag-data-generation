#!/usr/bin/env python3
"""`context_ok`'un klinik-iddia kapısı GERÇEK kurumsal metni eliyor mu?

Bağlam: `uretim-v3` §7b-2 pasajın klinik iddia taşımasını yasaklıyor ve
`src/checks.py::KLINIK_IDDIA` bunu anahtar kelimeyle denetliyor. Kural SENTETİK
pasaj için yazıldı (K74) ve orada işini yapıyor. Ama A katmanı korpusu (yordam /
erişim / kurum metinleri) devreye girdiğinde aynı kapı GERÇEK belgelere de
uygulanacak — `run_checks` kapıyı `sentetik` bayrağına göre ayırmıyor, yalnızca
§7b-1 (kaynak adı büyük harf) ayrılmış durumda.

Soru: gerçek kurumsal/yordamsal Türkçe metin bu kapıdan geçer mi?

Vekil girdi: `docs/arastirma-notlari.md` BÖLÜM K (Türkiye'nin tedavi ve yönlendirme
sistemi) — repoda elimizdeki, A katmanına en yakın gerçek metin. Kurum adları,
başvuru yordamı, TCK 191/3 yükümlülükleri.

⚠️ SINIR: bu bir vekil ölçümdür. Girdi markdown tablo satırı, gerçek bir kurum
belgesinin paragrafı değil; oran gerçek korpusa birebir taşınmaz. Ölçtüğü şey
kapının HANGİ SÖZCÜKTEN ateşlediği — o sözcükler gerçek belgede de aynı.

Girdi : docs/arastirma-notlari.md (BÖLÜM K)
Çıktı : reports/analiz/2026-09-15-klinik-iddia-kapisi-gercek-metin.md
"""
from __future__ import annotations

import hashlib
import sys
from collections import Counter
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
sys.path.insert(0, str(KOK / "src"))

from checks import KLINIK_IDDIA  # noqa: E402

GIRDI = KOK / "docs/arastirma-notlari.md"
CIKTI = KOK / "reports/analiz/2026-09-15-klinik-iddia-kapisi-gercek-metin.md"
BOLUM_BAS = "# BÖLÜM K — Türkiye'nin tedavi ve yönlendirme sistemi"
BOLUM_SON = "# BÖLÜM L —"


def bolum_metni(ham: str) -> list[str]:
    """BÖLÜM K'nin içerik satırları — başlık, alıntı ve kod çiti dışarıda."""
    bas = ham.index(BOLUM_BAS)
    son = ham.index(BOLUM_SON, bas)
    satirlar = []
    for s in ham[bas:son].split("\n"):
        s = s.strip()
        if not s or s.startswith(("#", ">", "```", "---", "| ---", "|---")):
            continue
        satirlar.append(s)
    return satirlar


def main() -> None:
    ham = GIRDI.read_text(encoding="utf-8")
    sha = hashlib.sha256(ham.encode("utf-8")).hexdigest()
    satirlar = bolum_metni(ham)

    vurus = []
    for s in satirlar:
        bulunan = sorted({m.group(0).lower() for m in KLINIK_IDDIA.finditer(s.lower())})
        if bulunan:
            vurus.append((bulunan, s))

    sayac = Counter(k for b, _ in vurus for k in b)
    oran = round(100 * len(vurus) / len(satirlar)) if satirlar else 0

    sat = [
        "# Klinik-iddia kapısı gerçek kurumsal metne uygulanınca ne oluyor?",
        "",
        f"**Girdi:** `docs/arastirma-notlari.md` (BÖLÜM K) · SHA256 `{sha}`  ",
        f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}",
        "",
        "---",
        "",
        "## 1. Soru",
        "",
        "`uretim-v3` §7b-2 *\"pasaj klinik iddia taşımaz\"* diyor; `src/checks.py::KLINIK_IDDIA`",
        "bunu anahtar kelimeyle denetliyor. Kural **sentetik** pasaj için yazıldı (K74).",
        "A katmanı korpusu geldiğinde aynı kapı **gerçek** kurum belgelerine de uygulanacak:",
        "`context_ok` yalnızca §7b-1'i (kaynak adı büyük harf) `sentetik` bayrağına göre ayırıyor,",
        "§7b-2'yi **her bağlam girdisine** uyguluyor.",
        "",
        "## 2. Ölçüm",
        "",
        f"- İncelenen içerik satırı: **{len(satirlar)}**",
        f"- Kapıya takılan: **{len(vurus)}** (%{oran})",
        "",
        "| eşleşen sözcük | kaç satırda |",
        "|---|---|",
        *[f"| `{k}` | {n} |" for k, n in sayac.most_common()],
        "",
        "### Takılan satırlar",
        "",
        "| eşleşen | satır |",
        "|---|---|",
        *[f"| `{', '.join(b)}` | {s.replace('|', '\\|')[:110]} |" for b, s in vurus],
        "",
        "## 3. Okuma",
        "",
        "Eşleşmelerin çoğu **klinik iddia değil**; kapının K65 ailesinden bir yanlış pozitifi:",
        "",
        "- `tedavi` — kurumun **kendi adının** içinde geçiyor (*Alkol ve Madde Bağımlıları",
        "  **Tedavi** Merkezi*). A katmanının her belgesi bu adı taşır.",
        "- `tanı` — *\"kaygıyı **tanı**\"* buyruk kipi; teşhis değil, eşsesli.",
        "- `iyileşme` — davranış tarifinde geçiyor (*performatif iyileşme*), iddia olarak değil.",
        "",
        "## 4. Sonuç",
        "",
        "Kapı **sentetik pasaj için doğru, gerçek belge için fazla geniş.** A katmanı",
        "korpusu bugünkü hâliyle `context_ok`'tan geçirilirse kurum adı taşıyan her pasaj",
        "elenir. Düzeltme yönü §7b-1'in deseniyle aynı: kapı `sentetik` bayrağına göre",
        "ayrılmalı ve gerçek pasajda **iddia cümlesi** aranmalı (sözcük varlığı değil).",
        "",
        "⚠️ **Sınır:** vekil ölçüm. Girdi markdown tablo satırı, kurum belgesi paragrafı",
        "değil; **oran** gerçek korpusa taşınmaz. Taşınan şey kapının hangi sözcükten",
        "ateşlediği. Gerçek oran, A katmanı pilotunun ilk partisinde ölçülmeli.",
        "",
    ]
    CIKTI.write_text("\n".join(sat), encoding="utf-8")
    print(f"{len(vurus)}/{len(satirlar)} (%{oran}) · {CIKTI.relative_to(KOK)}")


if __name__ == "__main__":
    main()
