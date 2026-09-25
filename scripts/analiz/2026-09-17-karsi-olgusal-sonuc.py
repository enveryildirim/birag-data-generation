#!/usr/bin/env python3
"""Karşı olgusal koşunun SONUCU — ön kayıtla yüzleştirilir.

⛔ Ön kayıt koşudan ÖNCE yazıldı: `reports/analiz/2026-09-17-karsi-olgusal-onkayit.md`
⭐ Tahmin: **A kolunda yönlendirme-yok 4 → ≤3; P kolunda 4 (±1).**

⛔⛔ **Ön kayıtta yazılı olan ve burada TEKRARLANAN uyarı:** hipotezin suçladığı
şeyin büyük kısmı (`ret_bilgi`, 139 kayıt) Kural 3'ün ZORUNLU kıldığı şeyle
aynı. Ablasyon yalnız azınlığa dokunabildi (%32,2 → %24,5) ⇒ **negatif sonuç
«hipotez yanlış» demek DEĞİLDİR**, «bu manipülasyon zayıftı» demek olabilir.
Bu cümle sonuç görülmeden yazıldı ve sonuç ne çıkarsa çıksın geçerlidir.
"""
from __future__ import annotations
import json
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
EK = KOK / "reports/analiz/eksen-kosu"
CIKTI = KOK / "reports/analiz/2026-09-17-karsi-olgusal-sonuc.md"

TABAN_ETIKET = "h-safety_crisis-h1-capa-k8"     # zaten koşmuş taban kol
KOLLAR = [("TABAN", TABAN_ETIKET, "datasets/v0.0.8"),
          ("A (ilan seyreltilmiş)", "ka-safety_crisis-ka-A-ilan-seyreltilmis",
           "data/ablasyon/…A-ilan-seyreltilmis"),
          ("P (plasebo)", "ka-safety_crisis-ka-P-plasebo",
           "data/ablasyon/…P-plasebo")]
TABAN_YY = 1          # Faz 3 tabanı (adaptörsüz ham model), K105/K106
TAHMIN_A, TAHMIN_P = 3, 4


def _dizin(etiket: str) -> Path | None:
    e = [p for p in EK.iterdir() if p.name.endswith(etiket)]
    return sorted(e)[-1] if e else None


def _olc(d: Path) -> tuple[int, list[str]]:
    rows = [json.loads(s) for s in (d / "sonuclar.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
    g = sum(1 for r in rows if r["otomatik_gecti"])
    yy = [r["id"] for r in rows
          if any(i.get("kural") == "herhangi_biri" and not i["gecti"]
                 for i in (r.get("iddialar") or []))]
    return g, yy


def main() -> int:
    veri = {}
    eksik = []
    for ad, et, korpus in KOLLAR:
        d = _dizin(et)
        if d is None:
            eksik.append(ad)
            continue
        g, yy = _olc(d)
        veri[ad] = {"gecen": g, "yonlendirme_yok": yy, "korpus": korpus, "dizin": d.name}
    if eksik:
        print("⛔ Henüz koşmamış kol:", ", ".join(eksik))
        return 2

    a, p, t = veri["A (ilan seyreltilmiş)"], veri["P (plasebo)"], veri["TABAN"]
    na, np_, nt = len(a["yonlendirme_yok"]), len(p["yonlendirme_yok"]), len(t["yonlendirme_yok"])

    sat = ["# Karşı olgusal — SONUÇ", "",
           "**Betik:** `scripts/analiz/2026-09-17-karsi-olgusal-sonuc.py` · **Tarih:** 2026-09-17",
           "**Ön kayıt:** `reports/analiz/2026-09-17-karsi-olgusal-onkayit.md` "
           "(koşudan ÖNCE yazıldı)", "",
           "Üç kol da **birebir aynı kapsamla** eğitildi (8 katman · `q_proj` · rank 8 · "
           "1368 adım · aynı tohum). Değişen tek şey korpus.", "",
           "| kol | korpus | E2 geçen | **yönlendirme-yok** | tabana fark |",
           "|---|---|---:|---:|---:|",
           f"| *ham model* | — | 11/20 | **{TABAN_YY}** | — |"]
    for ad in ("TABAN", "A (ilan seyreltilmiş)", "P (plasebo)"):
        v = veri[ad]
        n = len(v["yonlendirme_yok"])
        sat.append(f"| **{ad}** | `{v['korpus']}` | {v['gecen']}/20 | **{n}** | +{n-TABAN_YY} |")

    sat += ["", "## ⭐ Tahmin tuttu mu", "",
            f"| tahmin | beklenen | çıkan | |", "|---|---|---|---|",
            f"| A ≤ {TAHMIN_A} | ≤{TAHMIN_A} | **{na}** | "
            f"{'✅ **TUTTU**' if na <= TAHMIN_A else '⛔ **TUTMADI**'} |",
            f"| P = {TAHMIN_P} (±1) | {TAHMIN_P-1}–{TAHMIN_P+1} | **{np_}** | "
            f"{'✅ **TUTTU**' if abs(np_-TAHMIN_P) <= 1 else '⛔ **TUTMADI**'} |", ""]

    # ⭐ Asıl karşılaştırma A ↔ P: ikisi de aynı sayıda cümle kaybetti.
    fark = np_ - na
    sat += ["## ⭐⭐ Asıl karşılaştırma: A ↔ P", "",
            "İki kol da **aynı sayıda cümle** kaybetti (63); tek fark **hangi** cümleler.", "",
            f"| | yönlendirme-yok |", "|---|---:|",
            f"| A (hedef cümleler silindi) | **{na}** |",
            f"| P (hedef DIŞI cümleler silindi) | **{np_}** |",
            f"| **fark (P − A)** | **{fark:+d}** |", ""]
    if fark > 0 and na < nt:
        sat += [f"⭐ A, hem tabandan ({nt}) hem plasebodan ({np_}) **daha az** hasarlı. "
                "➡️ *Hasarın bir kısmı «yönlendirmeme ilanları»na atfedilebilir — "
                "silmenin kendisine değil, NEYİN silindiğine.*", "",
                f"⛔ Ama fark **{fark} öğe** ve n=20. Tek öğe bir puandır; bu fark "
                "gürültüden ayrılamaz. ⇒ **Yön var, kanıt yok.**"]
    elif na >= nt and np_ >= nt:
        sat += ["⛔⛔ **Hiçbir kol tabandan iyi değil.** Hedef cümleleri silmek de, "
                "rastgele cümle silmek de hasarı azaltmadı.", "",
                "➡️ Ön kayıtta yazıldığı gibi: bu **«hipotez yanlış» demek değil**. "
                "Ablasyon yalnız azınlığa dokunabildi (%32,2 → %24,5) çünkü kalanı "
                "Kural 3'ün zorunlu kıldığı `ret_bilgi`. ⇒ Söylenebilen tek şey: "
                "*bu güçte bir manipülasyon hasarı oynatmıyor.*"]
    else:
        sat += [f"⛔⛔ **TAHMİN TUTMADI VE TERS YÖNDE TUTMADI.** Hedef cümleleri silmek "
                f"hasarı azaltmadı, **artırdı** ({nt} → {na}); rastgele cümle silmek ise "
                f"**azalttı** ({nt} → {np_}).", "",
                "➡️⭐⭐ *Plasebo, deney kolundan daha çok «işe yaradı». Bu, bir etkinin "
                "yokluğunun klasik imzasıdır: fark, müdahalenin yönünü değil ÖLÇÜMÜN "
                "oynaklığını izliyor.*"]

    # ⭐⭐ GÜRÜLTÜ TABANI — bu koşunun asıl kazancı
    cekirdek = set(a["yonlendirme_yok"]) & set(p["yonlendirme_yok"]) & set(t["yonlendirme_yok"])
    hepsi = set(a["yonlendirme_yok"]) | set(p["yonlendirme_yok"]) | set(t["yonlendirme_yok"])
    oynak = hepsi - cekirdek
    sat += ["", "## ⭐⭐⭐ Bu koşunun ASIL kazancı: gürültü tabanı ölçüldü", "",
            "Üç korpus birbirinden **63 cümle** farkla ayrılıyor ve hepsi aynı kapsamla, "
            "aynı tohumla, aynı adımda eğitildi. Sonuç:", "",
            f"| | öğe |", "|---|---:|",
            f"| **her üç kolda da düşen** (çekirdek) | **{len(cekirdek)}** |",
            f"| kollar arasında oynayan | **{len(oynak)}** |",
            f"| aralık | **{min(nt,na,np_)}–{max(nt,na,np_)}** |",
            f"| **yayılım** | **{max(nt,na,np_)-min(nt,na,np_)}** |", "",
            f"➡️⭐⭐⭐ *Korpusu 63 cümle değiştirmek sonucu {min(nt,na,np_)} ile "
            f"{max(nt,na,np_)} arasında gezdiriyor — **{max(nt,na,np_)-min(nt,na,np_)} "
            f"öğelik bir yayılım** — ve yön müdahaleyi izlemiyor. ⇒ Bu ölçütte "
            f"**{max(nt,na,np_)-min(nt,na,np_)} öğeden küçük hiçbir fark okunamaz.*", "",
            f"⚠️ İki sayı KARIŞTIRILMAMALI: kollar arasında oynayan öğe **{len(oynak)}** "
            f"(`{'`, `'.join(sorted(oynak))}`), ama toplam yayılım **{max(nt,na,np_)-min(nt,na,np_)}** "
            "— çünkü aynı anda bir öğe düşerken başka biri düzeliyor.", "",
            "⭐ **Bu, kapsam merdivenini GERİYE DÖNÜK niteliyor:** merdivenin aralığı "
            "4–14'tü. Uçlar (4 ↔ 14) gürültü tabanının **çok üstünde** ⇒ o fark gerçek. "
            "Ama 2 öğeden küçük farklar **okunamaz** ⇒ merdivende «en dar kol (4) en "
            "geniş koldan (14) az hasarlı» demek meşru; «h7 (8), h6'dan (10) iyi» "
            "demek **değil**.", "",
            f"⛔ Çekirdek {len(cekirdek)} öğe (`{'`, `'.join(sorted(cekirdek))}`) "
            "**korpustan bağımsız** düşüyor: hangi veriyle eğitilirse eğitilsin bu "
            "öğelerde yönlendirme kayboluyor. ⇒ Asıl hasar burada ve korpus "
            "değişiklikleriyle oynatılamıyor.", "",
            "## Öğe düzeyinde"]

    # Öğe düzeyinde: hangi öğeler oynadı
    sat += ["", "| kol | yönlendirme-yok öğeler |", "|---|---|"]
    for ad in ("TABAN", "A (ilan seyreltilmiş)", "P (plasebo)"):
        sat.append(f"| {ad} | `{'`, `'.join(veri[ad]['yonlendirme_yok']) or '—'}` |")
    sat += ["",
            "## ⛔ Bu koşunun söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Negatif sonuç hipotezi çürütmez** | ablasyon, hipotezin suçladığı şeyin yalnız azınlığına dokunabildi; kalanı Kural 3 zorunlu kılıyor (ön kayıtta yazılı) |",
            "| ⛔ **n = 20 öğe** | oynama alanı 3; tek öğe bir puandır |",
            "| ⛔ **Tek tohum** | üretim deterministik (K105) ama tohum tek |",
            "| ⛔ **Yakınsama yok** | üç kol da 3 epoch'ta yakınsamadı (en iyi val son adımda) |",
            "| ⛔ **Eksen 3 ve Eksen 1 koşulmadı** | Pareto sırası + makine ısınması |",
            "| ⚠️ **Kelime dengesizliği** | A −501, P −388 kelime (fark korpusun %0,36'sı) |",
            "| ⚠️ **Ablasyon korpusu yayımlanamaz** | MI ekseninde daha kötü; `datasets/` altında değil |", ""]
    CIKTI.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[5:]))
    print(f"→ {CIKTI.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
