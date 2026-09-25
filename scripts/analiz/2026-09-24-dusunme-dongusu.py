#!/usr/bin/env python3
"""Düşünme döngüsü ne kadar yaygın — taban · `d1` (v0.0.18) · `e3` (v0.1.0).

⭐ Soru demodan doğdu (2026-09-23): ince ayarlı model düşünmesinde aynı cümleyi
altı kez yazdı (*«Soruyu sormuyorum, bir soruya cevap veriyorum.»*). Tek bir
örnek mi, yaygın bir kusur mu? **Yeni koşu yok** — kayıtlı eksen koşularının
`thinking` alanı okunur: taban 6 eksen (`taban-0924-*`, T278) + iki kol × 8
tohum × 6 eksen (EK-1 hücreleri, T277).

⭐ **Ölçüt KOPYALANMIYOR (K103):** `src/dejenerasyon.denetle` (distinct-5,
eşik 0,5) olduğu gibi kullanılır. ⚠️ O eşik **ağır çöküşten** kalibre edildi
(`B-derin`, cevabı boş kalan kayıtlar, T82) ve demodaki gibi **seyrek** bir
döngüyü görmeyebilir ⇒ yanına **ikinci, betimleyici** bir ölçü konur:

  **cümle döngüsü** — düşünmede ≥ 4 sözcüklü aynı cümle (küçük harf,
  noktalamasız) **≥ 3 kez** geçiyorsa. ⛔ Bu eşik KALİBRE EDİLMEDİ; ölçü
  yalnız betimler, kapı değildir. Demo örneği bilinen pozitif olarak sınanır.

Çıktı: reports/analiz/2026-09-24-dusunme-dongusu.md
"""
from __future__ import annotations

import collections
import math
import re
import statistics as st
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import dejenerasyon as dj  # noqa: E402

TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-dusunme-dongusu.md"
EK = KOK / "reports/analiz/eksen-kosu"
ASGARI_SOZCUK, ASGARI_TEKRAR = 4, 3

_sp = _iu.spec_from_file_location(
    "_coz", KOK / "scripts/analiz/2026-09-23-onkayit-ek1-cozumleme.py")
C = _iu.module_from_spec(_sp)
_sp.loader.exec_module(C)

# ⭐ Bilinen pozitif — demodan (2026-09-23, `v0.0.18` t31), birebir
DEMO = """İki cümlelik bir giriş cümlesi var ve azaltma isteği belirtilmiş.
İtiraz yok, onay yok.
"Nereden başlayacağımı bilmiyorum" cümlesi bir soru ve bir soruya cevap vermeden önce bir soru sormak gerekiyor.
İzin isteme protokolü: "Bilgi vermeden önce izin ister, kısa ve tarafsız verir, sonra nasıl geldiğini sorar."
Soruyu sormuyorum, bir soruya cevap veriyorum ve bu cevap bir bilgiye dayanıyor.
Önce bir soru sormuyorum, bir soruya cevap veriyorum.
Azaltma isteği bir hedeftir.
Soruyu sormuyorum, bir soruya cevap veriyorum.
"Nereden başlayacağımı bilmiyorum" cümlesi bir soru.
İzin isteme: "Bilgi vermeden önce izin ister"
Bilgi vermeden önce bir soru sormuyorum.
Soruyu sormuyorum, bir soruya cevap veriyorum.
Soruyu sormuyorum, bir soruya cevap veriyorum.
Soruyu sormuyorum, bir soruya cevap veriyorum."""


def cumleler(t: str) -> list[str]:
    parca = re.split(r"(?<=[.!?:])\s+|\n+", t or "")
    temiz = [re.sub(r"[^\wçğıöşü ]", "", p.lower()).strip() for p in parca]
    return [re.sub(r"\s+", " ", p) for p in temiz if len(p.split()) >= ASGARI_SOZCUK]


def cumle_olcu(t: str) -> dict:
    c = cumleler(t)
    say = collections.Counter(c)
    en = max(say.values(), default=0)
    return {"cumle": len(c), "en_cok_tekrar": en,
            "tekrar_payi": 1 - len(say) / len(c) if c else 0.0,
            "dongu": en >= ASGARI_TEKRAR}


def satir_olc(r: dict) -> dict:
    d = dj.denetle(r.get("thinking"), r.get("cevap"))
    return {**d, **cumle_olcu(r.get("thinking") or ""), "kesildi": bool(r.get("kesildi"))}


def ort_se(x: list[float]) -> str:
    if len(x) < 2:
        return f"{x[0]:.1f}"
    return f"{st.mean(x):.1f} ± {2 * st.stdev(x) / math.sqrt(len(x)):.1f}"


def main() -> int:
    # ── bilinen pozitif ──
    demo_d5 = dj.distinct_n(DEMO)
    demo_c = cumle_olcu(DEMO)
    assert demo_c["dongu"], "⛔ cümle ölçüsü demo örneğini yakalamıyor"

    h = C._hucreler()
    kollar = {"taban": {0: {k: sorted(EK.glob(f"*-taban-0924-{k}"))[-1]
                            for k, _ in C._ek.EKSEN}}}
    for kol in ("d1", "e3"):
        kollar[kol] = {t: {k: h[(kol, t, k)] for k, _ in C._ek.EKSEN} for t in C._ek.TOHUM}

    O = {}          # kol → tohum → eksen → [ölçü]
    for kol, tohumlar in kollar.items():
        O[kol] = {t: {k: [satir_olc(r) for r in C._satirlar(d)] for k, d in e.items()}
                  for t, e in tohumlar.items()}

    def oran(kol, anahtar, eksen=None):
        """tohum başına yüzde"""
        out = []
        for t, e in O[kol].items():
            rs = [x for k, v in e.items() if eksen in (None, k) for x in v]
            out.append(100 * sum(1 for x in rs if x[anahtar]) / len(rs))
        return out

    n_oge = {kol: sum(len(v) for v in next(iter(O[kol].values())).values()) for kol in O}
    s = ["# Düşünme döngüsü ne kadar yaygın", "",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
         "**Veri:** kayıtlı eksen koşularının `thinking` alanı — yeni koşu yok. Taban tek "
         f"koşu ({n_oge['taban']} öge), `d1`/`e3` 8 tohum × {n_oge['d1']} öge. "
         "Değerler tohum başına yüzde, ort ± 2·SE.", "",
         "## Bilinen pozitif — demo örneği", "",
         f"| ölçü | değer | yakaladı mı |", "|---|---:|---|",
         f"| distinct-5 (eşik {dj.TEKRAR_ESIGI}) | {demo_d5:.3f} | "
         f"{'✓' if demo_d5 < dj.TEKRAR_ESIGI else '⛔ HAYIR'} |",
         f"| cümle döngüsü (≥{ASGARI_SOZCUK} sözcük, ≥{ASGARI_TEKRAR} kez) | en çok "
         f"{demo_c['en_cok_tekrar']} kez | ✓ |", "",
         "## Kollara göre", "",
         "| ölçü | taban | `d1` (v0.0.18) | `e3` (v0.1.0) |", "|---|---:|---:|---:|"]
    for ad, an in (("cümle döngüsü", "dongu"), ("distinct-5 < 0,5 (mevcut kapı)", "tekrar"),
                   ("boş cevap", "bos_cevap"), ("üretim yok", "uretim_yok"),
                   ("bütçe kesildi (1024 jeton)", "kesildi"), ("herhangi dejenerasyon", "dejenere")):
        s.append(f"| {ad} | " + " | ".join(ort_se(oran(k, an)) for k in ("taban", "d1", "e3"))
                 + " |")
    medyan = {k: st.median(x["thinking_kelime"] for e in O[k].values() for v in e.values()
                           for x in v) for k in O}
    s.append("| düşünme uzunluğu, ortanca sözcük | "
             + " | ".join(f"{medyan[k]:.0f}" for k in ("taban", "d1", "e3")) + " |")
    s += ["", "## Eksene göre — cümle döngüsü", "",
          "| eksen | taban | `d1` | `e3` |", "|---|---:|---:|---:|"]
    for k, _ in C._ek.EKSEN:
        s.append(f"| `{k}` | " + " | ".join(ort_se(oran(kol, "dongu", k))
                                          for kol in ("taban", "d1", "e3")) + " |")

    # döngü ile boş cevap birlikte mi
    s += ["", "## Döngü cevabı bozuyor mu", "",
          "| kol | döngülü öge | bunların boş cevaplı olanı | döngüsüz ögelerde boş cevap |",
          "|---|---:|---:|---:|"]
    for kol in ("taban", "d1", "e3"):
        rs = [x for e in O[kol].values() for v in e.values() for x in v]
        dg = [x for x in rs if x["dongu"]]
        dz = [x for x in rs if not x["dongu"]]
        pay = lambda z: f"{100 * sum(1 for x in z if x['bos_cevap'] or x['uretim_yok']) / len(z):.0f}%" if z else "—"
        s.append(f"| `{kol}` | {len(dg)} / {len(rs)} | {pay(dg)} | {pay(dz)} |")

    s += ["", "## ⛔ Bunun söylemedikleri", "", "| | |", "|---|---|",
          f"| ⛔ **Cümle eşiği kalibre edilmedi** | ≥{ASGARI_TEKRAR} tekrar bir seçim; yalnız "
          "demo örneğiyle sınandı. Betimleyicidir, eleme ya da sürüm kapısı değildir |",
          "| ⚠️ **Eval koşuları demo koşulu değil** | eval `max_tokens` 1024 ve ögenin kendi "
          "istemi; demo 2048 jeton ve kanonik system prompt |",
          "| ⚠️ **Taban tek koşu** | tohum yok; yüzdesi bir ölçüm, dağılım değil |",
          "| ⚠️ **Cevabın içi ölçülmedi** | yalnız `thinking` alanı; cevaptaki tekrar ayrı konu |"]
    RAPOR.write_text("\n".join(s) + "\n", encoding="utf-8")
    print("\n".join(s[8:32]))
    print(f"\nyazıldı: {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
