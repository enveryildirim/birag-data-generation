#!/usr/bin/env python3
"""Tazeleme kolu sonucu — ve neden bu deney hipotezi SINAMADI.

⭐ T255 iki aday sebep bırakmıştı: (a) korpusun kipi hiç göstermemesi,
(b) LoRA kapsamı. Ayırıcı kol kuruldu (`v0.0.19` = `v0.0.18` + 40 aritmetik
tazeleme kaydı) ve üç öngörü **koşudan önce** yazıldı.

⛔⛔⛔ **SONUÇ: hiçbir öge düzelmedi** — ve ön kayda göre bu *«sebep LoRA
kapsamı»* demek olurdu. ⭐ **AMA ÖYLE OKUNAMAZ,** çünkü koşudan sonra
ölçülen bir şey deneyi geçersiz kılıyor: tazeleme kayıtları eğitim
sinyalinin **%0,034'ü**.

➡️⭐⭐⭐ *`mask_prompt: true` kaybı yalnız CEVAP jetonlarına uyguluyor.
Tazeleme cevapları yalın sayı, yani ortalama **2,1 jeton**; korpus cevapları
ortalama **241**. ⇒ Kayıtların %3,7'si olan bir küme, gradyanın %0,034'ü
oluyor — **114 kat fark**. Kayıt saymak sinyal saymak değildir.*

⇒ Bu kol *«tazeleme işe yaramaz»*ı değil, *«%0,034 sinyal hiçbir şeyi
değiştirmez»*i gösterdi. Hipotez **hâlâ açık**.

Çıktı: reports/analiz/2026-09-22-tazeleme-kolu-sonuc.md
"""
from __future__ import annotations

import json
import math
import statistics as st
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-tazeleme-kolu-sonuc.md"
EK = KOK / "reports/analiz/eksen-kosu"
T8 = (7, 13, 23, 31, 37, 41, 43, 47)
T3 = (7, 13, 23)
# ölçüldü: scripts/analiz/2026-09-22-tazeleme-seti.py + tokenizer sayımı
JETON = {"korpus": (1033, 249423), "tazeleme": (40, 84)}


def _rows(et):
    d = [p for p in EK.iterdir() if p.name.endswith(et)]
    return {r["id"]: r for r in (json.loads(s) for s in
            (sorted(d)[-1] / "sonuclar.jsonl").read_text(encoding="utf-8").splitlines()
            if s.strip())} if d else None


def main() -> int:
    tb = _rows("-forgetting_smoke-baseline-1")
    d1 = {t: _rows(f"d1-veri2x-k8qo-v018-t{t}-forget") for t in T8}
    e1 = {t: _rows(f"e1-tazeleme-v019-t{t}-forget") for t in T3}
    if any(v is None for v in e1.values()):
        raise SystemExit("⛔ tazeleme kolu koşusu eksik")

    d1_v = [sum(1 for r in d1[t].values() if r.get("otomatik_gecti")) for t in T8]
    e1_v = [sum(1 for r in e1[t].values() if r.get("otomatik_gecti")) for t in T3]
    tb_v = sum(1 for r in tb.values() if r.get("otomatik_gecti"))
    fark = st.mean(e1_v) - st.mean(d1_v)
    hata = 2 * math.sqrt(st.stdev(d1_v)**2 / len(d1_v) + st.stdev(e1_v)**2 / len(e1_v))

    nk, jk = JETON["korpus"]; nt, jt = JETON["tazeleme"]
    pay_kayit = 100 * nt / (nk + nt)
    pay_jeton = 100 * jt / (jk + jt)
    # %5 sinyal için gereken kayıt sayısı, iki tasarımda
    ger_yalin = math.ceil(0.05 * jk / (0.95 * (jt / nt)))
    ger_adimli = math.ceil(0.05 * jk / (0.95 * 40))      # ~40 jetonluk adımlı çözüm

    KIP = {"fs-025": ("ARİTMETİK", "⭐ tazelendi"),
           "fs-013": ("ARİTMETİK", "⭐ tazelendi"),
           "fs-029": ("olgusal ad", "⛔ tazelenMEDİ"),
           "fs-009": ("liste/indeks", "⛔ tazelenMEDİ")}

    sat = ["# Tazeleme kolu — sonuç ve deneyin geçersizliği", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           "**Kol:** `e1-tazeleme-k8qo-v019` (3 tohum) ↔ `d1-veri2x-k8qo-v018` "
           "(8 tohum) ↔ taban  ", "",
           "## Öngörüler koşudan önce yazılmıştı", "",
           "| sonuç | anlamı |", "|---|---|",
           "| aritmetik düzelir, olgusal düzelmez | kip yokluğu sebep |",
           "| ikisi de düzelir | tazeleme genel onarım yapıyor |",
           "| **ikisi de düzelmez** | **sebep LoRA kapsamı** |", "",
           "## Ölçüm", "",
           "| öge | taban | `d1` (tazelemesiz) | `e1` (tazelenmiş) | kip |",
           "|---|---|---:|---:|---|"]
    for i, (k, durum) in KIP.items():
        t = "✅" if tb[i].get("otomatik_gecti") else "❌"
        a = sum(1 for x in T8 if d1[x][i].get("otomatik_gecti"))
        b = sum(1 for x in T3 if e1[x][i].get("otomatik_gecti"))
        sat.append(f"| `{i}` | {t} | {a}/8 | **{b}/3** | {k} · {durum} |")
    sat += ["", "| kol | toplam | tohumlar |", "|---|---|---|",
            f"| taban | **{tb_v}/30** | (tek koşu) |",
            f"| `d1` tazelemesiz | {st.mean(d1_v):.2f}/30 | {d1_v} |",
            f"| `e1` tazelenmiş | {st.mean(e1_v):.2f}/30 | {e1_v} |", "",
            f"**Fark: {fark:+.2f} · hata payı ±{hata:.2f}** ⇒ ⛔ **hiçbir "
            "değişiklik yok.** `fs-025` tazelendiği hâlde **0/3**'te kaldı.", "",
            "## ⛔⛔⛔ Ama bu deney hipotezi SINAMADI", "",
            "Koşudan **sonra** ölçülen bir şey sonucu geçersiz kılıyor:", "",
            "| | kayıt | cevap jetonu | ortalama |", "|---|---:|---:|---:|",
            f"| korpus | {nk} | {jk:,} | {jk/nk:.0f} |",
            f"| tazeleme | {nt} | **{jt}** | **{jt/nt:.1f}** |", "",
            f"| tazelemenin payı | |", "|---|---:|",
            f"| **kayıt** sayısında | %{pay_kayit:.1f} |",
            f"| ⛔⛔ **kayıp sinyalinde** | **%{pay_jeton:.3f}** |", "",
            f"⇒ **{pay_kayit/pay_jeton:.0f} kat** fark.", "",
            "➡️⭐⭐⭐ *`mask_prompt: true` kaybı yalnız CEVAP jetonlarına "
            "uyguluyor. Tazeleme cevapları yalın sayı — ortalama 2,1 jeton; "
            "korpus cevapları 241. Kayıtların %3,7'si olan bir küme gradyanın "
            "%0,034'ü oluyor. **Kayıt saymak sinyal saymak değildir.***", "",
            "⇒ Bu kol *«tazeleme işe yaramaz»*ı göstermedi; *«%0,034 sinyal "
            "hiçbir şeyi değiştirmez»*i gösterdi. **Hipotez hâlâ açık ve iki "
            "aday sebep hâlâ ayrılmamış durumda.**", "",
            "## ⭐ Geçerli bir sınama ne ister", "",
            "Kayıp sinyalinin **%5'ine** ulaşmak için:", "",
            "| tasarım | gereken kayıt |", "|---|---:|",
            f"| yalın sayı cevabı (2,1 jeton) | **~{ger_yalin:,}** — korpustan büyük, saçma |",
            f"| ⭐ **adımlı çözüm** (~40 jeton) | **~{ger_adimli}** — yapılabilir |", "",
            "⇒ Doğru tasarım *«daha çok yalın cevap»* değil, **adımlarını "
            "yazan** aritmetik kayıtlarıdır: hem sinyal payı yeter hem de "
            "korpusun düzyazı kipine yakın durur. ⚠️ *Bu benim önerim*, "
            "ölçülmedi.", "",
            "## ⛔ Bu raporun söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Ön kayıtlı üçüncü sonuç UYGULANMADI** | *«ikisi de "
            "düzelmezse sebep LoRA kapsamı»* yazılmıştı; uygulanmadı çünkü "
            "müdahalenin **etkili olduğu varsayımı** çürüdü. Ön kayıt bir "
            "sonucu sabitler, müdahalenin gerçekten yapıldığını garanti etmez |",
            "| ⛔ **`e1` yalnız 3 tohum** | `d1` 8; fark ölçümü asimetrik |",
            "| ⛔ **LoRA kapsamı hipotezi hâlâ sınanmadı** | onu ayıracak kol "
            "(daha dar kapsam) koşulmadı |",
            "| ⚠️ **Jeton sayımı tokenizer'a bağlı** | `models/gemma-4-E4B-it-bf16-train`; "
            "başka bir tokenizer'da oranlar biraz oynar, büyüklük mertebesi değişmez |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[sat.index("## Ölçüm"):]))
    print(f"\n→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
