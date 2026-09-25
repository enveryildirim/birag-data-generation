#!/usr/bin/env python3
"""Aynı judge'ın aynı kayda iki bağımsız geçişi ne kadar tutarlı? (K61 enstrüman doğrulama)

2026-09-15'te korpus judge'ı yanlışlıkla iki kez dağıtıldı: 03:35 ve 03:59 UTC
dalgalarının ikisi de `model='sonnet'`, aynı v6 rubriği, aynı girdi dosyaları.
İkinci dalga sürerken anlık görüntü alındı. Böylece **tekrar-test** örneklemi
bedavaya çıktı; ayırt etme ölçütü İÇERİKTİR, zaman damgası değil:
  · FARKLI  -> kopya o dosyanın üzerine yazılmasından ÖNCE alınmış;
               elimizde birinci ve ikinci geçiş ayrı ayrı var. GEÇERLİ ÇİFT.
  · AYNI    -> kopya o dosya zaten yeniden yazıldıktan SONRA alınmış; iki kopya da
               ikinci geçiş. Bağımsız iki LLM geçişinin serbest metin alıntılarını
               karakteri karakterine tekrarlaması olanaksız olduğundan bu tek
               açıklamadır. Çift değil, dışarıda bırakılır.

Bu tavan ölçümüdür: judge'ın kendisiyle uyuşmadığı yerde başka hiçbir
karşılaştırma (Sonnet-Gemini sapması, sürüm farkı) o eksende anlam taşımaz.

Kullanım:
  uv run python <betik> [--dizin korpus-v3-claude]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import filter as f  # noqa: E402

# ⛔ Rapor tarihi betiğin ADINDAN gelir. `datetime.now()` kullanılıyordu; tarih
# dönmesiyle değil, SAAT dönmesiyle her koşuda kayıyordu — bu betiği tek başına
# "kararsız" gösteren şey buydu (K126).
TARIH = Path(__file__).name[:10]

# ⛔⛔ GİRDİ OTURUM SCRATCHPAD'İNDE — ve `korpus-v3-claude` ARTIK YOK (2026-09-16'da
# bulundu). Bu rapor bugün yeniden türetilemez; ham sonuçların TEK dalgası
# `reports/analiz/ham-judge/korpus-v3-claude.jsonl`'de duruyor, tekrar-testin
# gerektirdiği İKİ dalga arşivlenmemişti. Kapı aşağıda: girdi yoksa betik boş
# rapor YAZMAZ, durur — yoksa yayımlanmış bulguyu sessizce siler.
ISLER = Path("/private/tmp/claude-501/-Users-pc-projects-birag-data-finetuning"
             "/fe6477c2-8e5e-439e-875d-df2b5ed62d91/scratchpad/judge-isleri")

SAYISAL = ["duygusal_tepki", "yorumlama", "kesif", "grounding", "kisalik_dogallik",
           "dil_butunlugu", "anlasilirlik", "dogallik", "mi_uyumu"]
IKILI = ["klinik_guvenlik_ihlali", "rol_siniri_ihlali", "cevapsiz_soru",
         "kurulmamis_mecaz", "belirsiz_gonderge", "ust_uste_yan_cumle",
         "devrik_eksiltili", "soyut_adlastirma", "siz_kaymasi", "klise_acilis",
         "terapi_jargonu", "bos_guvence", "ovgu_tonu", "yansitma_var",
         "karmasik_yansitma", "takdir_var", "ozet_var", "ozerklik_vurgusu",
         "tuzak_uzman", "tuzak_etiketleme", "tuzak_soru_cevap", "tuzak_erken_odak",
         "tuzak_suclama", "tuzak_erken_tavsiye"]


def turet(ham: dict) -> dict:
    """Toplayıcıyla BİREBİR aynı türetme — yoksa kod farkını rubrik farkı sanarız."""
    d = dict(ham)
    f.f_bolumu_turet(d)
    for alan, hesap in (("anlasilirlik", f.anlasilirlik_hesapla),
                        ("dogallik", f.dogallik_hesapla),
                        ("mi_uyumu", f.mi_uyumu_hesapla)):
        deger = hesap(d)
        if deger is not None:
            d[alan] = deger
    return d


def kappa(a: list[bool], b: list[bool]) -> float | None:
    """Cohen kappa. Her iki geçiş de tek sınıf verdiyse tanımsız -> None."""
    n = len(a)
    if n == 0:
        return None
    go = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    bek = pa * pb + (1 - pa) * (1 - pb)
    if abs(1 - bek) < 1e-12:
        return None
    return (go - bek) / (1 - bek)


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dizin", default="korpus-v3-claude")
    ap.add_argument("--ilk", default="sonuc-ilk-dalga")
    ap.add_argument("--ikinci", default="sonuc")
    a = ap.parse_args()

    kok = ISLER / a.dizin
    ciftler, ayni, tekil = [], 0, 0
    for yol1 in sorted((kok / a.ilk).glob("*.json")):
        yol2 = kok / a.ikinci / yol1.name
        if not yol2.exists():
            tekil += 1
            continue
        if sha(yol1) == sha(yol2):
            ayni += 1              # kopya üzerine yazmadan sonra alınmış — çift değil
            continue
        try:
            ciftler.append((yol1.stem, turet(json.loads(yol1.read_text())),
                            turet(json.loads(yol2.read_text()))))
        except Exception as e:
            print(f"  ATLANDI {yol1.stem}: {type(e).__name__}: {e}"[:110])

    n = len(ciftler)
    satir = [
        "# Judge tekrar-test: aynı Sonnet, aynı rubrik, iki bağımsız geçiş", "",
        f"- tarih: {TARIH}",
        f"- betik: `scripts/analiz/{Path(__file__).name}`",
        f"- rubrik: `{f.JUDGE_PROMPT_VERSION}` · judge: sonnet subagent (iki dalga)",
        f"- kaynak: `{a.dizin}/{a.ilk}` (03:35 UTC dalgası) ile "
        f"`{a.dizin}/{a.ikinci}` (03:59 UTC dalgası)",
        f"- iki bağımsız geçişi olan kayıt: **{n}** · "
        f"anlık görüntü geç kalmış (iki kopya da 2. geçiş): {ayni} · "
        f"karşılıksız: {tekil}", "",
    ]
    if n == 0:
        raise SystemExit(
            f"⛔ GİRDİ YOK: {kok} altında karşılaştırılacak çift bulunamadı.\n"
            f"   Rapor ÜZERİNE YAZILMADI. Oturum scratchpad'i silinmişse bu rapor\n"
            f"   yeniden türetilemez — yayımlanmış hâli tek kayıttır (Kural 7).")
        satir.append("Karşılaştırılacak çift yok.")
        (KOK / "reports/analiz/2026-09-15-judge-tekrar-test.md").write_text("\n".join(satir))
        print("çift yok"); return

    satir += ["## Sayısal eksenler", "",
              "| eksen | birebir uyum | ort. |fark| | yön (2.−1.) | ≥2 puan sapan |",
              "|---|---|---|---|---|"]
    for e in SAYISAL:
        p = [(x[e], y[e]) for _, x, y in ciftler if isinstance(x.get(e), int) and isinstance(y.get(e), int)]
        if not p:
            continue
        tam = sum(u == v for u, v in p) / len(p)
        mutlak = sum(abs(u - v) for u, v in p) / len(p)
        yon = sum(v - u for u, v in p) / len(p)
        buyuk = sum(abs(u - v) >= 2 for u, v in p)
        satir.append(f"| `{e}` | %{tam*100:.0f} | {mutlak:.2f} | {yon:+.2f} | {buyuk}/{len(p)} |")

    satir += ["", "## İkili boyutlar", "",
              "| boyut | uyum | kappa | 1. geçiş açık | 2. geçiş açık |",
              "|---|---|---|---|---|"]
    kararsiz = []
    for e in IKILI:
        p = [(bool(x.get(e)), bool(y.get(e))) for _, x, y in ciftler if e in x and e in y]
        if not p:
            continue
        u, v = [q[0] for q in p], [q[1] for q in p]
        uyum = sum(i == j for i, j in p) / len(p)
        k = kappa(u, v)
        ks = "—" if k is None else f"{k:.2f}"
        satir.append(f"| `{e}` | %{uyum*100:.0f} | {ks} | {sum(u)}/{len(p)} | {sum(v)}/{len(p)} |")
        if uyum < 0.85 or (k is not None and k < 0.4 and (sum(u) or sum(v))):
            kararsiz.append((e, uyum, k, sum(u), sum(v)))

    satir += ["", "## Kararsız boyutlar", ""]
    if kararsiz:
        satir.append("Judge kendisiyle bile anlaşamıyor — bu eksende Sonnet-Gemini "
                     "karşılaştırması yapmanın anlamı yok (K61):")
        satir.append("")
        for e, uyum, k, s1, s2 in sorted(kararsiz, key=lambda z: z[1]):
            ks = "tanımsız" if k is None else f"{k:.2f}"
            satir.append(f"- `{e}` — uyum %{uyum*100:.0f}, kappa {ks} "
                         f"(1. geçiş {s1}, 2. geçiş {s2})")
    else:
        satir.append("Yok: her ikili boyut %85 üzeri uyumda.")

    satir += ["", "## Kayıt başına toplam oynaklık", ""]
    oynak = sorted(((no, sum(abs(x[e] - y[e]) for e in SAYISAL
                             if isinstance(x.get(e), int) and isinstance(y.get(e), int)))
                    for no, x, y in ciftler), key=lambda z: -z[1])
    satir.append(f"Sayısal eksenlerde toplam |fark| ortalaması: "
                 f"**{sum(o[1] for o in oynak)/n:.1f}** puan/kayıt "
                 f"({len(SAYISAL)} eksen üzerinden)")
    satir.append("")
    satir.append("En oynak beş kayıt: " + ", ".join(f"`{no}` ({d})" for no, d in oynak[:5]))
    satir.append("En durağan beş kayıt: " + ", ".join(f"`{no}` ({d})" for no, d in oynak[-5:]))

    # --- gürültü tabanı: ölçülen "sapma" gürültüden ayırt edilebiliyor mu? ---
    sapma_yolu = KOK / "reports/analiz/2026-09-15-judge-claude-sapmasi.md"
    if sapma_yolu.exists():
        sapma = {}
        for st in sapma_yolu.read_text().splitlines():
            parca = [x.strip() for x in st.split("|")]
            if len(parca) == 8 and parca[1].startswith("`"):
                try:
                    sapma[parca[1].strip("`")] = (float(parca[5]), float(parca[6].lstrip("%")))
                except ValueError:
                    pass
        if sapma:
            satir += ["", "## Gürültü tabanı — ölçülen sapma gerçek mi?", "",
                      "Bir eksende judge KENDİSİYLE ne kadar anlaşmıyorsa, başka bir judge'la",
                      "olan farkın o kadarı zaten gürültüdür. Modeller arası fark bu tabanı",
                      "aşmıyorsa o eksende **sapma ölçülmemiştir**, oynaklık ölçülmüştür (K61).", "",
                      "⚠️ İki sütun FARKLI örneklemlerden: taban korpus v3 / Sonnet-Sonnet "
                      f"(n={n}), sapma golden dev / Gemini-Claude (n=48). Kalemler aynı "
                      "değil, bu yüzden bu bir **büyüklük karşılaştırması**, kesin bir "
                      "sınama değil.", "",
                      "| eksen | gürültü tabanı (ort.\\|fark\\|) | modeller arası fark | taban aşılıyor mu |",
                      "|---|---|---|---|"]
            for e in SAYISAL:
                if e not in sapma:
                    continue
                pr = [(x[e], y[e]) for _, x, y in ciftler
                      if isinstance(x.get(e), int) and isinstance(y.get(e), int)]
                if not pr:
                    continue
                taban = sum(abs(u - v) for u, v in pr) / len(pr)
                s_mutlak, _ = sapma[e]
                if taban == 0 and s_mutlak == 0:
                    karar = "ikisi de 0 — eksen sabit"
                elif s_mutlak > taban * 1.5:
                    karar = "**evet** — sapma gerçek"
                elif s_mutlak < taban:
                    karar = "**HAYIR** — judge kendisiyle daha az anlaşıyor"
                else:
                    karar = "sınırda — ayırt edilemez"
                satir.append(f"| `{e}` | {taban:.2f} | {s_mutlak:.2f} | {karar} |")

    hedef = KOK / "reports/analiz/2026-09-15-judge-tekrar-test.md"
    hedef.write_text("\n".join(satir) + "\n")
    print(f"{n} çift karşılaştırıldı · yazıldı: {hedef.relative_to(KOK)}")


if __name__ == "__main__":
    main()
