"""Özgünlük taraması ikinci turu — kapsam envanteri.

T146-T245 aralığındaki katkıların kaçı literatüre karşı tarandı, kaçı taranmadı.

⚠️ Küme eşlemesi TÜRETİLMEZ — editoryal karardır (Kural 6) ve aşağıda elle
ilan edilir. Betiğin yaptığı tek şey: defteri ayrıştırmak, ilan edilen eşlemeyi
uygulamak ve **taranmayanları tek tek saymak**. Bir taramanın dürüstlüğü
bulduklarında değil, neye bakmadığını sayabilmesindedir (T140'ın kuralı).

Çıktı: reports/analiz/2026-09-22-ozgunluk-ikinci-tur-kapsam.md
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
DEFTER = KOK / "docs" / "tez" / "katki-defteri.md"
CIKTI = KOK / "reports" / "analiz" / "2026-09-22-ozgunluk-ikinci-tur-kapsam.md"

ARALIK = (146, 245)

# ─── İLAN: taranan kümeler ve üyeleri (editoryal, türetilmedi) ──────────────
KUMELER: dict[str, tuple[str, list[int]]] = {
    "gurultu-tabani": (
        "Ölçütün gürültü tabanı, tohum yayılımı, ön kayıtlı eşiğin geçerliliği",
        [159, 160, 174, 175, 178, 181, 182, 183, 186, 241, 242, 243, 245],
    ),
    "judge-tekrarlanabilirlik": (
        "Aynı judge'a iki çekiliş, önbellek/hafıza bulaşması, tek-ayrıntı sondası",
        [173, 174, 175, 178, 238, 241],
    ),
    "sozluk-kapisi-goodhart": (
        "Sözlükle kurulmuş kapı edimi değil formülü tanır; kapı şablonu zorunlu kılar",
        [192, 194, 196, 200, 201, 202, 205, 206, 226, 235],
    ),
    "turkce-bicimbilim": (
        "Türkçe çekim/ek sert kapının düz alt dizge aramasını deliyor",
        [153, 154, 199],
    ),
    "test-orakl": (
        "Kapıyı denetleyen betik kapının koşulunu kopyalıyor",
        [147, 151],
    ),
    "lora-yayilim": (
        "Belirleyici olan güncellemenin büyüklüğü değil yayılımı; güvenlik ekseni",
        [184, 185, 186, 187, 188],
    ),
    "veri-kusuru-kaskadi": (
        "Alan dolu, biçimi doğru, değeri yanlış; kural yazılı, kapı yok",
        [193, 217, 220, 221, 222, 223, 224, 236, 237],
    ),
    "anotator-bagimsizligi": (
        "Üç anotatörün üçü de aynı model ailesinden ⇒ uyum yukarı çekiliyor",
        [227, 228, 229, 230],
    ),
    "kapi-bilesimi": (
        "İki tutarlı kapı birlikte makul cevabı puanlanamaz kılıyor; aşırı red",
        [176, 177, 189],
    ),
    "cot-sadakati": (
        "İç muhakeme cevabın yaptığını yapmadığını ilan ediyor; denetleyen kapı yok",
        [239],
    ),
    "thinking-orani": (
        "Üretim emeğinin yarısından fazlası thinking'e gidiyor; eğitilen setten sapma",
        [232],
    ),
}

SATIR = re.compile(r"^\|\s*(T(\d+))\s*\|")


def sha16(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def baslik_cikar(satir: str) -> str:
    """Katkı sütununun ilk cümlesini (BÜYÜK HARFLİ başlık) kısaltarak döndür."""
    parcalar = satir.split("|")
    metin = parcalar[2] if len(parcalar) > 2 else ""
    metin = re.sub(r"\*\*|`", "", metin)
    metin = re.sub(r"[⭐⛔◐○⚠️➡️📎]", "", metin)
    metin = " ".join(metin.split())
    return metin[:110]


def main() -> None:
    satirlar = DEFTER.read_text(encoding="utf-8").splitlines()

    kayitlar: dict[int, str] = {}
    for satir in satirlar:
        eslesme = SATIR.match(satir)
        if not eslesme:
            continue
        no = int(eslesme.group(2))
        if ARALIK[0] <= no <= ARALIK[1]:
            kayitlar[no] = baslik_cikar(satir)

    taranan: dict[int, list[str]] = {}
    for ad, (_, uyeler) in KUMELER.items():
        for no in uyeler:
            taranan.setdefault(no, []).append(ad)

    # İlan edilen üye defterde var mı? (yazım hatası kapısı)
    hayalet = sorted(no for no in taranan if no not in kayitlar)

    kapsanan = sorted(no for no in kayitlar if no in taranan)
    kapsanmayan = sorted(no for no in kayitlar if no not in taranan)

    s = []
    s.append("# Özgünlük taraması ikinci turu — kapsam envanteri\n")
    s.append(
        f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** 2026-09-22  \n"
        f"**Girdi:** `docs/tez/katki-defteri.md` SHA256 `{sha16(DEFTER)}`  \n"
        f"**Aralık:** T{ARALIK[0]}–T{ARALIK[1]}\n"
    )
    s.append("---\n")
    s.append("## Neden\n")
    s.append(
        "Birinci tur (T67-T69, 2026-09-16) defterde **115 satır** varken yapılmıştı.\n"
        "Defter o günden beri büyüdü ve aradaki kayıtlar hiç taranmadı. Bu envanter\n"
        "ikinci turun **neye baktığını ve neye bakmadığını** sayılabilir kılar.\n\n"
        "⚠️ Küme eşlemesi **türetilmedi** — editoryal karardır (Kural 6), betikte\n"
        "elle ilan edilir. Betik yalnız uygular ve kapsanmayanı sayar.\n"
    )
    s.append("---\n")
    s.append("## 1. Kapsam\n")
    s.append("| | |\n|---|---:|\n")
    s.append(f"| aralıktaki katkı satırı | **{len(kayitlar)}** |\n")
    s.append(f"| taranan kümeye giren | **{len(kapsanan)}** |\n")
    s.append(f"| **hiç taranmayan** | **{len(kapsanmayan)}** |\n")
    s.append(f"| ilan edilip defterde bulunamayan | {len(hayalet)} |\n")
    if hayalet:
        s.append(f"\n⛔ Defterde bulunamayan ilan: {', '.join('T' + str(n) for n in hayalet)}\n")
    orani = 100 * len(kapsanan) / len(kayitlar) if kayitlar else 0
    s.append(f"\n➡️ Aralığın **%{orani:.0f}**'i tarandı.\n")

    s.append("\n---\n")
    s.append("## 2. Taranan kümeler\n")
    s.append("| Küme | İddia | Üye | Kayıtlar |\n|---|---|---:|---|\n")
    for ad, (aciklama, uyeler) in KUMELER.items():
        var = sorted(n for n in uyeler if n in kayitlar)
        liste = ", ".join(f"T{n}" for n in var)
        s.append(f"| `{ad}` | {aciklama} | {len(var)} | {liste} |\n")

    s.append("\n---\n")
    s.append("## 3. ⛔ Hiç taranmayanlar\n")
    s.append(
        "Bu kayıtlar ikinci turda **literatüre karşı aranmadı.** Çoğu depoya özgü\n"
        "mühendislik/vaka kaydıdır ve genelleştirilebilir bir iddia taşımaz — ama\n"
        "*bu da bir karardır*, ölçüm değil. Üçüncü tur buradan başlar.\n\n"
    )
    s.append("| # | Başlık (kısaltılmış) |\n|---|---|\n")
    for no in kapsanmayan:
        s.append(f"| T{no} | {kayitlar[no]} |\n")

    s.append("\n---\n")
    s.append("## 4. ⛔ Bu envanterin sınırı\n")
    s.append(
        "| | |\n|---|---|\n"
        "| ⛔ **Kapsam ≠ sonuç** | bir kaydın kümeye girmesi tarandığını gösterir, "
        "*iddiasının tek tek sorulduğunu* değil; küme düzeyinde arandı |\n"
        "| ⛔ **Eşleme tek okuyucunun** | kümeleri ben kurdum (K30); başka bir okuyucu "
        "başka kümeler kurar ve kapsam yüzdesi değişir |\n"
        "| ⚠️ **«Taranmadı» ≠ «özgün değil»** | taranmayan kayıt hakkında hiçbir şey "
        "iddia edilmiyor — ne lehte ne aleyhte |\n"
    )

    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    CIKTI.write_text("".join(s), encoding="utf-8")
    print(f"yazıldı: {CIKTI.relative_to(KOK)}")
    print(f"  aralıktaki kayıt : {len(kayitlar)}")
    print(f"  taranan          : {len(kapsanan)}")
    print(f"  taranmayan       : {len(kapsanmayan)}")
    print(f"  hayalet ilan     : {hayalet}")


if __name__ == "__main__":
    main()
