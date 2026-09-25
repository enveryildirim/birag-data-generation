"""Özgünlük taraması üçüncü turu — kapsam envanteri.

İkinci tur (T247) T146-T245'in **48**'ini taranmamış bırakmıştı ve listeledi.
Üçüncü tur o 48'in içinden genelleştirilebilir iddia taşıyanları arıyor.

⚠️ Küme eşlemesi TÜRETİLMEZ — editoryal karardır (Kural 6). Betik ikinci turun
raporundan **taranmayanlar listesini okur** (elle kopyalamaz), üçüncü turun
ilanını uygular ve **hâlâ taranmayanı** sayar.

Çıktı: reports/analiz/2026-09-22-ozgunluk-ucuncu-tur-kapsam.md
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
DEFTER = KOK / "docs" / "tez" / "katki-defteri.md"
IKINCI_TUR = KOK / "reports" / "analiz" / "2026-09-22-ozgunluk-ikinci-tur-kapsam.md"
CIKTI = KOK / "reports" / "analiz" / "2026-09-22-ozgunluk-ucuncu-tur-kapsam.md"

# ─── İLAN: üçüncü turda taranan kümeler (editoryal, türetilmedi) ────────────
KUMELER: dict[str, tuple[str, list[int]]] = {
    "distinct-n-tabani": (
        "Çeşitlilik ölçütünün kısa metinde göremediği taban («ölçülemez = temiz»)",
        [146],
    ),
    "etiket-bayatlamasi": (
        "Metin düzeltilince ona verilmiş yargı geçersizleşir; alanın anlamı sürümler arası kayar",
        [156, 171, 240],
    ),
    "kayip-mekanizmasi": (
        "Örneklem kaybının rastgeleliği kaydın özelliklerinden anlaşılmaz",
        [179],
    ),
    "erken-tespit": (
        "Bir ölçümün değeri bulduğu şeyde değil, NE ZAMAN bulduğunda",
        [218],
    ),
    "yakin-tekrar-yeri": (
        "Yakın-tekrarın tehlikesini örtüşmenin büyüklüğü değil YERİ söyler",
        [231],
    ),
    "alinti-sadakati-turkce": (
        "Alıntıda vurgu taşıyan ögenin düşmesi; önceden ilan edilen düzeltme ölçütü",
        [168, 169],
    ),
    "ortuk-esik-kayma": (
        "Ölçüt eşiğini söylemiyorsa uygulayan koyar; devralınan şerh sessizleşir",
        [208, 210],
    ),
    "okunmayan-sinyal": (
        "Okunmayan sinyal sinyal değildir; hatırlatma kapı değildir; denetim eksik kaydı görmez",
        [152, 195, 209, 213],
    ),
}

SATIR = re.compile(r"^\|\s*T(\d+)\s*\|")
RAPOR_SATIRI = re.compile(r"^\|\s*T(\d+)\s*\|", re.MULTILINE)


def sha16(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def ikinci_turun_taranmayanlari() -> list[int]:
    """İkinci turun raporundaki §3 listesini okur — elle kopyalanmaz."""
    metin = IKINCI_TUR.read_text(encoding="utf-8")
    bolum = metin.split("## 3. ⛔ Hiç taranmayanlar")[1].split("## 4.")[0]
    return [int(m.group(1)) for m in RAPOR_SATIRI.finditer(bolum)]


def baslik_cikar(satir: str) -> str:
    parcalar = satir.split("|")
    metin = parcalar[2] if len(parcalar) > 2 else ""
    metin = re.sub(r"\*\*|`", "", metin)
    metin = re.sub(r"[⭐⛔◐○⚠️➡️📎]", "", metin)
    return " ".join(metin.split())[:110]


def main() -> None:
    kalanlar = ikinci_turun_taranmayanlari()

    basliklar: dict[int, str] = {}
    for satir in DEFTER.read_text(encoding="utf-8").splitlines():
        m = SATIR.match(satir)
        if m and int(m.group(1)) in kalanlar:
            basliklar[int(m.group(1))] = baslik_cikar(satir)

    taranan: dict[int, list[str]] = {}
    for ad, (_, uyeler) in KUMELER.items():
        for no in uyeler:
            taranan.setdefault(no, []).append(ad)

    kapsam_disi = sorted(no for no in taranan if no not in kalanlar)
    kapsanan = sorted(no for no in kalanlar if no in taranan)
    hala_taranmayan = sorted(no for no in kalanlar if no not in taranan)

    s = []
    s.append("# Özgünlük taraması üçüncü turu — kapsam envanteri\n\n")
    s.append(
        f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** 2026-09-22  \n"
        f"**Girdi:** `docs/tez/katki-defteri.md` SHA256 `{sha16(DEFTER)}`  \n"
        f"**Girdi:** `reports/analiz/{IKINCI_TUR.name}` SHA256 `{sha16(IKINCI_TUR)}`  \n"
        f"**Evren:** ikinci turun **taranmamış** bıraktığı {len(kalanlar)} kayıt "
        f"(liste o rapordan **okundu**, elle kopyalanmadı)\n\n"
    )
    s.append("---\n\n## 1. Kapsam\n\n| | |\n|---|---:|\n")
    s.append(f"| ikinci turdan devralınan taranmamış kayıt | **{len(kalanlar)}** |\n")
    s.append(f"| üçüncü turda tarandı | **{len(kapsanan)}** |\n")
    s.append(f"| **hâlâ taranmadı** | **{len(hala_taranmayan)}** |\n")
    s.append(f"| ilan edilip evrende olmayan | {len(kapsam_disi)} |\n")
    if kapsam_disi:
        s.append(f"\n⛔ Evren dışı ilan: {', '.join('T' + str(n) for n in kapsam_disi)}\n")
    s.append(
        f"\n➡️ Devralınan kuyruğun **%{100 * len(kapsanan) / len(kalanlar):.0f}**'i "
        f"kapandı. T146-T245 aralığının toplam kapsamı: "
        f"**{100 * (100 - len(hala_taranmayan)) / 100:.0f}%** "
        f"(52 + {len(kapsanan)} = {52 + len(kapsanan)} / 100).\n"
    )

    s.append("\n---\n\n## 2. Üçüncü turda taranan kümeler\n\n")
    s.append("| Küme | İddia | Üye | Kayıtlar |\n|---|---|---:|---|\n")
    for ad, (aciklama, uyeler) in KUMELER.items():
        var = sorted(n for n in uyeler if n in kalanlar)
        s.append(
            f"| `{ad}` | {aciklama} | {len(var)} | "
            f"{', '.join('T' + str(n) for n in var)} |\n"
        )

    s.append("\n---\n\n## 3. ⛔ Hâlâ taranmayanlar\n\n")
    s.append(
        "İki tur sonra da literatüre karşı **aranmamış** kayıtlar. Okuyarak verilen "
        "hüküm: bunlar ağırlıkla **depoya özgü mühendislik ve vaka kayıtlarıdır** ve "
        "genelleştirilebilir bir özgünlük iddiası taşımazlar — ⚠️ ama bu bir **okuma**dır, "
        "ölçüm değil, ve yanılabilir.\n\n"
    )
    s.append("| # | Başlık (kısaltılmış) |\n|---|---|\n")
    for no in hala_taranmayan:
        s.append(f"| T{no} | {basliklar.get(no, '⛔ defterde bulunamadı')} |\n")

    s.append("\n---\n\n## 4. ⛔ Bu envanterin sınırı\n\n")
    s.append(
        "| | |\n|---|---|\n"
        "| ⛔ **Kapsam ≠ sonuç** | kümeye girmek tarandığını gösterir, iddiasının "
        "tek tek sorulduğunu değil |\n"
        "| ⛔ **Eşleme tek okuyucunun** | kümeleri ben kurdum (K30) |\n"
        "| ⚠️ **«Taranmadı» ≠ «özgün değil»** | §3 hakkında ne lehte ne aleyhte bir "
        "iddia var |\n"
        "| ⭐ **Evren türetildi** | §3'ün girdisi ikinci turun raporundan **okundu**; "
        "iki tur arasında elle kopyalama yok |\n"
    )

    CIKTI.write_text("".join(s), encoding="utf-8")
    print(f"yazıldı: {CIKTI.relative_to(KOK)}")
    print(f"  devralınan  : {len(kalanlar)}")
    print(f"  tarandı     : {len(kapsanan)}")
    print(f"  hâlâ kalan  : {len(hala_taranmayan)}")
    print(f"  evren dışı  : {kapsam_disi}")


if __name__ == "__main__":
    main()
