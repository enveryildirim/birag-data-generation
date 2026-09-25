#!/usr/bin/env python3
"""Muafiyet kapısı 0/162 ateşledi — ateşleseydi GÖRÜR MÜYDÜ?

⛔ Açık kalem (T46): v9'un muafiyet doğrulama kapısı üretimde **hiç ateşlemedi**.
T46 sebebini de gösterdi — kapı rubrikte ilan edildiği için judge uydurma dayanak
yazmayı bıraktı; kapı ÖNLEYEREK çalışıyor, YAKALAYARAK sınanmamış kalıyor. Plan iki
kabul edilebilir yol bırakmıştı: ateşleyecek bir vaka bulmak, ya da her koşuda
*«sınanmadı»* diye raporlamak — sessizlik değil. ⭐ Üçüncü bir yol var: **kusuru
ÜRETİP kapının görüp görmediğini ölçmek**. Yöntem T51'in kayma denetimine
uyguladığının aynısı: tespit gücü.

⚠️ Ölçülen şey kapının **duyarlılığı**, judge'ın uydurma ORANI değil. Üretimde oran
0 gözlendi; burada o 0'ın *«kusur yok»* mu *«kapı kör»* mü olduğu ayrılıyor.

Bozma kipleri GÖZLENMİŞ kusurlardan alındı — uydurulmadı:
  · `ic_muhakeme`  — alıntı cevapta değil iç muhakemede (v8 Eksen 2'de 33 vaka, T45/T50)
  · `birlestirme`  — iki cümlenin başı ve gövdesi birleşmiş (T49'un tek gerçek hatası)
  · `baska_kayit`  — dayanak başka bir kaydın kaynağından (T50'nin takas imzası)
  · `kelime_dusur` — gerçek alıntıdan tek iç kelime düşmüş (en hafif bozulma)

⭐ Nüfus ve karar kuralı `2026-09-15-v9-kapi-denetimi.py`'den **import edilir**,
kopyalanmaz: iki yerde iki tanım olursa güç de ikiye bölünür (K97 dersi).

Girdi : v9 kapı denetiminin kendi kaynak kurucuları + ham-judge arşivi
Çıktı : reports/analiz/2026-09-16-muafiyet-kapisi-gucu.md
Kullanım: uv run python scripts/analiz/2026-09-16-muafiyet-kapisi-gucu.py
"""
from __future__ import annotations

import collections
import importlib.util
import json
import random
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-muafiyet-kapisi-gucu.md"

import filter as f  # noqa: E402

_s = importlib.util.spec_from_file_location(
    "kd", KOK / "scripts/analiz/2026-09-15-v9-kapi-denetimi.py")
KD = importlib.util.module_from_spec(_s)
_s.loader.exec_module(KD)          # ⭐ MUAFIYET eşlemesi ve kaynak kurucuları buradan

RASTGELE = random.Random(97)       # ⛔ tohum sabit — bozma seçimleri koşular arası aynı
KIPLER = ["yanlis_bolum", "ic_muhakeme", "birlestirme", "baska_kayit", "kelime_dusur"]
ACIKLAMA = {"yanlis_bolum": "⭐ **dizge GERÇEK, yeri yanlış** — BıRAG'ın kendi cümlesi",
            "ic_muhakeme": "v8 Eksen 2'de **33 vaka** (T45/T50)",
            "birlestirme": "T49'un tek gerçek judge hatası",
            "baska_kayit": "T50'nin takas imzası",
            "kelime_dusur": "en hafif bozulma — eşleştiricinin sertliği"}


def cumleler(metin: str) -> list[str]:
    return [c.strip() for c in re.split(r"(?<=[.!?…])\s+", metin or "") if len(c.strip()) > 20]


def kapi(alan: str, deger: str, kaynak: dict, nerede: str) -> bool:
    """⭐ Kapının KENDİSİ çağrılır — kural burada yeniden yazılmaz."""
    return f._dogrula({alan: deger}, alan, kaynak, nerede, zorunlu=True)


def boz(kip: str, gercek: str, kaynak: dict, yabanci: list[str],
        nerede_bl: str) -> str | None:
    havuz = cumleler(kaynak.get("konusma", "")) + cumleler(kaynak.get("cevap", ""))
    if kip == "yanlis_bolum":
        # ⭐ Tek NON-TRİVİAL kip: dizge kaynakta GERÇEKTEN var, ama kapının baktığı
        # bölümde değil. `filter.py` bunu açıkça istiyor — *«muafiyet KULLANICI
        # turunu ister: BıRAG'ın kendi önceki cümlesine dayanan teselli,
        # kullanıcının söylediği bir şeye dayanmıyor demektir»*. Öteki dört kip
        # metni DEĞİŞTİRİYOR ve kapı bir alt-dizge sınaması olduğu için onları
        # yakalaması yapı gereği neredeyse kesin; asıl soru bu kipte.
        ad = [c for c in cumleler(kaynak.get("cevap", ""))
              if f.alinti_nrm(c) not in kaynak.get(nerede_bl, "")]
        return RASTGELE.choice(ad) if ad else None
    if kip == "ic_muhakeme":
        ic = [c for c in cumleler(kaynak.get("ic_muhakeme", ""))
              if f.alinti_nrm(c) not in kaynak.get("konusma", "")
              and f.alinti_nrm(c) not in kaynak.get("baglam", "")]
        return RASTGELE.choice(ic) if ic else None
    if kip == "birlestirme":
        if len(havuz) < 2:
            return None
        a, b = RASTGELE.sample(havuz, 2)
        ap, bp = a.split(), b.split()
        return (" ".join(ap[:len(ap) // 2] + bp[len(bp) // 2:])
                if len(ap) >= 3 and len(bp) >= 3 else None)
    if kip == "baska_kayit":
        return RASTGELE.choice(yabanci) if yabanci else None
    if kip == "kelime_dusur":
        p = gercek.split()
        if len(p) < 4:
            return None
        i = RASTGELE.randrange(1, len(p) - 1)
        return " ".join(p[:i] + p[i + 1:])
    raise ValueError(kip)


def vakalari_topla(korpus_k: dict, eksen2_k: dict, aileler: list[Path]) -> list[tuple]:
    """Kapının GERÇEKTEN danıştığı muafiyet alıntıları — `_f_dolu` ile süzülür.

    ⛔ Eksen 2 kaynakları `(kol, id)` ile anahtarlanır: aynı öğe beş kolda birden
    var ve arşiv kaydı yalnızca `id` taşıyor. Kolu dosya adı söylüyor — eşleme
    `KD.BILINEN_KOL`'den gelir, burada yeniden kurulmaz.
    """
    out = []
    for yol in aileler:
        kol = KD.BILINEN_KOL.get(yol.stem)
        for satir in yol.open(encoding="utf-8"):
            r = json.loads(satir)
            ham = r.get("ham")
            if isinstance(ham, str):
                try:
                    ham = json.loads(ham)
                except Exception:
                    continue
            # Hakemlik dosyalarında kol KAYDIN içinde, aşama 1'de DOSYA ADINDA
            # (`bul()` ile birebir aynı sıra).
            kol_r = r.get("kol") or kol
            k = (eksen2_k.get((kol_r, r.get("id"))) if kol_r
                 else korpus_k.get(r.get("id")))
            if not isinstance(ham, dict) or k is None:
                continue
            for alan, nerede in KD.MUAFIYET.items():
                if f._f_dolu(ham, alan):
                    out.append((yol.stem, r.get("id"), alan, nerede, ham[alan], k))
    return out


def main() -> int:
    korpus_k, eksen2_k = KD.korpus_kaynaklari(), KD.eksen2_kaynaklari()
    aileler = sorted(p for p in (KOK / "reports/analiz/ham-judge").glob("*.jsonl")
                     if p.stem.startswith(("korpus-v9", "v9-hakem-"))
                     or p.stem in KD.BILINEN_KOL)
    vakalar = vakalari_topla(korpus_k, eksen2_k, aileler)

    yabanci_havuz = [c for k in list(korpus_k.values()) + list(eksen2_k.values())
                     for c in cumleler(k.get("cevap", ""))]
    ates, denenen = collections.Counter(), collections.Counter()
    gecerli, kacan = 0, []
    bant_sayi = collections.defaultdict(lambda: [0, 0])

    for aile, oid, alan, nerede, gercek, kaynak in vakalar:
        if kapi(alan, gercek, kaynak, nerede):
            gecerli += 1
        yabanci = [c for c in yabanci_havuz
                   if f.alinti_nrm(c) not in kaynak.get(nerede, "")]
        n = len(f.alinti_nrm(gercek))
        bant = "≤25" if n <= 25 else ("26-60" if n <= 60 else ">60")
        for kip in KIPLER:
            bozuk = boz(kip, gercek, kaynak, yabanci, nerede)
            if bozuk is None or f.alinti_nrm(bozuk) == f.alinti_nrm(gercek):
                continue
            denenen[kip] += 1
            bant_sayi[bant][1] += 1
            if not kapi(alan, bozuk, kaynak, nerede):
                ates[kip] += 1
                bant_sayi[bant][0] += 1
            else:
                kacan.append((aile, oid, alan, kip, bozuk[:70]))

    td, ta = sum(denenen.values()), sum(ates.values())
    guc = 100 * ta / td if td else 0.0
    L = [f"# Muafiyet kapısı 0/162 ateşledi — **ateşleseydi görür müydü**", "",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
         f"**Nüfus ve karar kuralı:** `scripts/analiz/2026-09-15-v9-kapi-denetimi.py` "
         f"**import edildi**, kopyalanmadı  ",
         f"**Kapı:** `src/filter.py::_dogrula` — **çağrıldı**, yeniden yazılmadı  ",
         f"**Arşiv:** {', '.join(f'`{p.stem}`' for p in aileler)}",
         "", "---", "",
         "## Soru", "",
         "T46 ölçtü: v9'un muafiyet kapısı üretimde **hiç ateşlemedi** ve sebebini de",
         "gösterdi — kapı ilan edildiği için judge uydurma dayanak yazmayı bıraktı.",
         "Kapı **önleyerek** çalışıyor, **yakalayarak** sınanmamış kalıyor.",
         "⛔ Bu, *«kapı çalışıyor»* demeye yetmez: bir uydurma dayanak GELSEYDİ kapı",
         "onu görür müydü? ⭐ Yöntem T51'in aynısı — **kusuru üret, kapıyı ölç**.", "",
         f"## Nüfus — {len(vakalar)} muafiyet alıntısı", "",
         "| Aile | vaka |", "|---|---:|"]
    L += [f"| `{a}` | {n} |" for a, n in
          sorted(collections.Counter(v[0] for v in vakalar).items())]
    L += [f"| **TOPLAM** | **{len(vakalar)}** |", "",
          f"✅ Gerçek alıntıların **{gecerli}/{len(vakalar)}**'i kapıdan geçiyor — "
          f"*«0/162 ateşleme»* sonucunun öteki yüzü: kapı **yanlış pozitif vermiyor**.", "",
          "## ⭐ Tespit gücü — bozma kipi başına", "",
          "| Kip | gözlenmiş kusur | denenen | yakalanan | **güç** |",
          "|---|---|---:|---:|---:|"]
    for kip in KIPLER:
        d, a = denenen[kip], ates[kip]
        L.append(f"| `{kip}` | {ACIKLAMA[kip]} | {d} | {a if d else '—'} | "
                 + (f"**%{100 * a / d:.1f}**" if d else "—") + " |")
    L += [f"| **TOPLAM** | | **{td}** | **{ta}** | **%{guc:.1f}** |", "",
          "## Alıntı uzunluğuna göre", "",
          "| Gerçek alıntı | denenen | yakalanan | güç |", "|---|---:|---:|---:|"]
    for bant in ("≤25", "26-60", ">60"):
        a, d = bant_sayi[bant]
        L.append(f"| {bant} karakter | {d} | {a} | "
                 + (f"**%{100 * a / d:.1f}**" if d else "—") + " |")
    L += ["", "## ⛔ Kaçanlar", ""]
    if kacan:
        L += [f"**{len(kacan)}** bozuk dayanak kapıdan GEÇTİ:", "",
              "| Aile | Kayıt | Alan | Kip | Bozuk dizge |", "|---|---|---|---|---|"]
        L += [f"| `{a}` | `{o}` | `{al}` | `{k}` | {b.replace('|', '/')}… |"
              for a, o, al, k, b in kacan[:25]]
        if len(kacan) > 25:
            L.append(f"| … | | | | _ve {len(kacan) - 25} tane daha_ |")
    else:
        L += ["_Yok — denenen her bozma yakalandı._"]
    L += ["", "## ⭐ Karar", "", "| | |", "|---|---|",
          f"| ✅ Yanlış pozitif | {len(vakalar) - gecerli}/{len(vakalar)} — "
          f"gerçek dayanaklar kapıdan geçiyor |",
          f"| {'✅' if guc > 95 else '⚠️'} Tespit gücü | **%{guc:.1f}** "
          f"({ta}/{td} bozma yakalandı) |",
          "| ➡️ T46 | *«0 ateşleme»* artık **sessizlik değil**: nüfusun tamamında "
          "üretilen kusurlar bu oranda görülüyor |",
          "| ⛔ Ölçmediği | judge'ın gerçek **uydurma oranı**. Bu bir duyarlılık ölçüsü; "
          "üretimde kusur gelmemesinin sebebi hâlâ **caydırıcılık** (T46) |",
          "| ⛔ Ölçmediği | *«kaynakta var ve doğru bölümde, ama muafiyeti HAK ETMEYEN»* "
          "alıntı. Kapı dizge arar, **anlam** denetlemez — bu sınır ölçülemedi |", "",
          "⚠️ **Dört kip yapı gereği kolaydır.** Kapı bir **alt-dizge** sınaması; metni",
          "değiştiren her bozmanın yakalanması neredeyse kesin ve bu sonucu ucuzlatır.",
          f"⭐ Asıl sınama `yanlis_bolum`: dizge kaynakta **gerçekten var**, yalnızca",
          "kapının baktığı bölümde değil (BıRAG'ın kendi cümlesine dayandırılmış bir",
          "teselli). Gücün anlamlı kısmı orada okunmalı.", ""]

    RAPOR.write_text("\n".join(L), encoding="utf-8")
    print(f"{len(vakalar)} muafiyet alıntısı · gerçek geçen {gecerli} · "
          f"bozma {td} · yakalanan {ta} (%{guc:.1f}) · kaçan {len(kacan)}")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
