#!/usr/bin/env python3
"""Judge çıktısından parti başına REVİZYON LİSTESİ üretir — katmanlı.

⛔⛔ **Neden katmanlı.** Judge'ın işaretlediği her şey aynı ağırlıkta değil.
`build.py` yalnız iki bayrağı eler (klinik güvenlik, rol sınırı); ötekiler
veri setine GİRER. ⇒ «judge ne dedi» ile «hangi kayıt düzeltilmeli» aynı soru
değildir ve ikincisi yazılı bir ölçüt ister.

⭐ Katmanlar:
  **K1 — zorunlu.** `klinik_guvenlik_ihlali` ya da `rol_siniri_ihlali`.
     Düzeltilmezse kayıt elenir; eleme sessiz veri kaybıdır.
  **K2 — dayanaksız.** Cevabın somut ayrıntısı / tesellisi / yordam iddiası
     konuşmada YOK. ⇒ modele *uydurmayı* öğretir (K120 ekseni).
  **K3 — MI tuzağı.** `tuzak_*`, `kusur_kullanicida_ima`. Cevap doğru ama
     yöntem yanlış.

⚠️ Judge Claude ailesinden (K43/K45) ⇒ bu liste **veri revizyonu sinyali**,
metrik değil. ⚠️ `en_somut_ayrinti == "YOK"` uydurma DEĞİLDİR: ayrıntı yokluğu
başka bir kusurdur, K2'ye girmez.

Kullanım:
  uv run python scripts/analiz/2026-09-17-revizyon-listesi.py data/judged/*.jsonl
"""
from __future__ import annotations
import json, sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / "reports/analiz/2026-09-17-revizyon-listesi.json"

TUZAK = ["tuzak_uzman", "tuzak_etiketleme", "tuzak_soru_cevap",
         "tuzak_erken_odak", "tuzak_suclama", "tuzak_erken_tavsiye"]


def kusurlar(j: dict) -> list[str]:
    """Bir yargı kaydının kusur etiketleri. ⭐ Ölçüt burada, tek yerde."""
    out = []
    if j.get("klinik_guvenlik_ihlali"):
        out.append(f"K1:guvenlik={j.get('guvenlik_tipi')}")
    if j.get("rol_siniri_ihlali"):
        out.append(f"K1:rol={j.get('rol_alani')}")
    if (j.get("ayrinti_konusmada_var") is False
            and not j.get("ayrinti_hipotez_olarak_isaretli")
            and (j.get("en_somut_ayrinti") or "YOK") != "YOK"):
        out.append("K2:ayrinti_uydurma")
    # ⛔⛔ İLK YAZIMDA BU ÖLÇÜT HATALIYDI ve ölçümle yakalandı: `v5-parti3`'te
    # 15 «dayanaksız teselli» bayrağının **8'inde judge zaten «cevapta teselli
    # YOK» demişti**. Teselli olmayan bir cevabı «dayanaksız teselli» saymak,
    # olmayan bir şeyin dayanağını aramaktır.
    # ⭐ İkinci dışlama: *«Buradayım.»* gibi ASİSTANIN KENDİNE DAİR cümleleri.
    # Bunlar bir olgu iddiası taşımaz ⇒ dayanağı olamaz ve modele uydurma
    # öğretmez. Rubrik `teselli_dayanak_alintisi`ni ZORUNLU seçim yaptığı için
    # judge onları da dayanaksız işaretliyor; bu bir uydurma değil, zorunlu
    # seçimin yan ürünü (K2 revizyonunda ölçülüp yazıldı).
    # ➡️ *Bir kusur ölçütü, ölçtüğü şeyin var olduğunu önce doğrulamalı.*
    _t = (j.get("en_teselli_edici") or "YOK").strip()
    _KENDINE = {"buradayım.", "buradayım", "buradayim."}
    if (j.get("teselli_islevi") == "rahatlatma"
            and j.get("teselli_dayanak_dogrulandi") is False
            and _t not in ("YOK", "")
            and _t.lower() not in _KENDINE):
        out.append("K2:teselli_dayanaksiz")
    if (j.get("yordam_iddiasi") and j.get("yordam_iddiasi") != "YOK"
            and j.get("yordam_baglamdan") is False):
        out.append("K2:yordam_dayanaksiz")
    for t in TUZAK:
        if j.get(t) is True:
            out.append(f"K3:{t}")
    if j.get("kusur_kullanicida_ima") is True:
        out.append("K3:kusur_ima")
    return out


def main(yollar: list[str]) -> int:
    rapor, sayac = {}, Counter()
    for y in yollar:
        p = Path(y) if Path(y).is_absolute() else KOK / y
        parti = p.name.split(".")[0]
        kayit = {}
        for s in p.read_text(encoding="utf-8").splitlines():
            if not s.strip():
                continue
            r = json.loads(s)
            j = r.get("judge")
            if not j:
                continue
            k = kusurlar(j)
            if k:
                kayit[r["gen_meta"]["parti_sira"]] = k
                for x in k:
                    sayac[x.split("=")[0]] += 1
        kat = {n: sorted({x.split(":")[0] for x in v}) for n, v in kayit.items()}
        rapor[parti] = {
            "kaynak": str(p.relative_to(KOK)),
            "K1": sorted(n for n, v in kat.items() if "K1" in v),
            "K2": sorted(n for n, v in kat.items() if "K2" in v and "K1" not in v),
            "K3": sorted(n for n, v in kat.items() if v == ["K3"]),
            "ayrinti": {str(n): v for n, v in sorted(kayit.items())},
        }
    rapor["_toplam_kusur"] = dict(sayac.most_common())
    CIKTI.write_text(json.dumps(rapor, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{'parti':<10}{'K1':>5}{'K2':>5}{'K3':>5}{'toplam kayıt':>14}")
    print("─" * 39)
    for parti, d in rapor.items():
        if parti.startswith("_"):
            continue
        t = len(set(d["K1"]) | set(d["K2"]) | set(d["K3"]))
        print(f"{parti:<10}{len(d['K1']):>5}{len(d['K2']):>5}{len(d['K3']):>5}{t:>14}")
        if d["K1"]:
            print(f"    ⛔ K1: {d['K1']}")
        if d["K2"]:
            print(f"    ⚠️ K2: {d['K2']}")
        if d["K3"]:
            print(f"    · K3: {d['K3']}")
    print("\nkusur dağılımı:", rapor["_toplam_kusur"])
    print(f"→ {CIKTI.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
