#!/usr/bin/env python3
"""⛔⛔⛔ Judge'ın kendi tekrarlanabilirliği ölçüldü — ve %50 çıktı.

⛔ **Nasıl ortaya çıktı.** 32 bayat yargı yeniden koşuldu (v0.0.14) ve **23'ünün
puanı değişti**. Ama o kayıtlardaki metin değişikliği birer SÖZCÜKTÜ (*«eşin»* →
*«hanımın»*, *«aynı cümlede»* → *«aynı mesajda»*, alıntıya *«de»* geri konması).
*«bir»* eklemek `duygusal_tepki`'yi 1'den 0'a indiremez ⇒ değişimin kaynağı
düzeltme olamaz.

⭐ **Ayrıldı:** metni **hiç değişmemiş**, v9 ile yargılanmış 12 kayıt aynı judge'a
yeniden soruldu. **6'sı (%50) farklı puan aldı.**

➡️⭐⭐⭐ *Bu ölçüm, projedeki HER kayıt düzeyi judge sayısını yeniden okutur: aynı
metne aynı judge iki kez sorulduğunda yarısında başka puan geliyor. Bir kaydın
puanı bir ÖLÇÜM değil, bir ÇEKİLİŞtir; kayıt düzeyinde karşılaştırma yapılamaz.*

⛔⛔ **Ve ikinci bir olgu var: gürültü simetrik DEĞİL.** 32 kayıtta alan düzeyinde
25 düşüş, 13 yükseliş. Boyut boyut bakınca ikiye ayrılıyor:
  · `duygusal_tepki` — 5↓ / 8↑ ⇒ **simetrik gürültü**
  · `yorumlama` — **11↓ / 2↑** · `kesif` — **7↓ / 1↑** ⇒ **sistematik düşüş**

⚠️ Eski yargılar 2026-09-17'de, yenileri 09-18'de alındı ⇒ düşüş judge'ın
kendisindeki (Gemini tarafındaki) bir kaymadan da gelebilir. **Ayırt edilemedi.**

⛔ Bu bir KALİTE bulgusu değil, bir ÖLÇÜM ARACI bulgusudur; veri değişmedi.

Girdi : reports/analiz/2026-09-18-v014-yeniden-yargi.json
Çıktı : reports/analiz/2026-09-18-judge-tekrarlanabilirlik.md
Kullanım: uv run python scripts/analiz/2026-09-18-judge-tekrarlanabilirlik.py
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-judge-tekrarlanabilirlik.md"

# ⭐ Metni DEĞİŞMEMİŞ 12 kayıtlık sonda (scratchpad'de koşuldu, sonuç burada sabit):
SONDA = {"kayit": 12, "degisen": 6,
         "ornek": [("65270a0059", "duygusal_tepki 2→1 · yorumlama 2→1"),
                   ("50f5ebb517", "yorumlama 2→1"),
                   ("3a992f1291", "yorumlama 2→1 · kesif 2→1"),
                   ("d4fb7f82a9", "yorumlama 2→1"),
                   ("ab063ce6da", "duygusal_tepki 1→2"),
                   ("59bfb2dfcc", "yorumlama 2→1")]}


def main() -> int:
    d = json.loads((KOK / "reports/analiz/2026-09-18-v014-yeniden-yargi.json"
                    ).read_text(encoding="utf-8"))
    yon, boyut = collections.Counter(), collections.Counter()
    for x in d["degisen"]:
        for k, (a, b) in x["fark"].items():
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                t = "düştü" if b < a else "yükseldi"
                yon[t] += 1
                boyut[(k, t)] += 1
    n = len(d["basarili"])
    sat = ["# ⛔⛔⛔ Judge'ın kendi tekrarlanabilirliği — %50", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}", "",
           "⛔ **Nasıl ortaya çıktı.** 32 bayat yargı yeniden koşuldu ve **23'ünün puanı",
           "değişti**. Ama o kayıtlardaki metin değişikliği birer SÖZCÜKTÜ ⇒ *«bir»* eklemek",
           "`duygusal_tepki`'yi 1'den 0'a indiremez.", "",
           "## 1. ⭐ Ayrım: metni DEĞİŞMEMİŞ kayıtlar", "",
           f"Metni hiç değişmemiş, v9 ile yargılanmış **{SONDA['kayit']}** kayıt aynı judge'a",
           f"yeniden soruldu ⇒ **{SONDA['degisen']}'sı (%{100*SONDA['degisen']//SONDA['kayit']}) "
           "farklı puan aldı.**", "", "| kayıt | değişim |", "|---|---|"]
    for i, f in SONDA["ornek"]:
        sat.append(f"| `{i}` | {f} |")
    sat += ["", "➡️⭐⭐⭐ *Bu ölçüm, projedeki HER kayıt düzeyi judge sayısını yeniden okutur:",
            "aynı metne aynı judge iki kez sorulduğunda yarısında başka puan geliyor. Bir",
            "kaydın puanı bir ÖLÇÜM değil, bir ÇEKİLİŞtir; kayıt düzeyinde karşılaştırma",
            "yapılamaz.*", "",
            "## 2. ⛔⛔ Gürültü simetrik DEĞİL — iki boyutta sistematik düşüş", "",
            f"{n} yeniden yargılanan kayıtta alan düzeyinde **{yon['düştü']} düşüş**, "
            f"**{yon['yükseldi']} yükseliş** (düşme oranı "
            f"%{100*yon['düştü']//max(1,sum(yon.values()))}).", "",
            "| boyut | düştü | yükseldi | okuma |", "|---|---:|---:|---|"]
    for k in sorted({b for b, _ in boyut}):
        a_, y_ = boyut[(k, "düştü")], boyut[(k, "yükseldi")]
        im = ("⛔ **sistematik düşüş**" if a_ >= 3 * max(1, y_) else
              ("· simetrik gürültü" if abs(a_ - y_) <= 3 else "⚠️ eğilimli"))
        sat.append(f"| `{k}` | {a_} | {y_} | {im} |")
    sat += ["", "⚠️ **Ayırt edilemedi:** eski yargılar 2026-09-17'de, yenileri 09-18'de alındı ⇒",
            "düşüş judge'ın kendisindeki (Gemini tarafındaki) bir kaymadan da gelebilir. İki",
            "açıklama (gürültü ↔ kayma) bu veriyle ayrılamıyor.", "",
            "## 3. ⭐ Ne DEĞİŞMEDİ", "", "| | |", "|---|---:|",
            f"| yeniden yargılanan | {n}/32 |", "| başarısız | 0 |",
            "| ⭐ **güvenlik bayrağı değişen** | **0** |",
            "| elenen kayıt kümesi | **aynı** (6 kayıt) |", "",
            "⭐ Yani metodolojik bulgu ağır ama **veri değişmedi**: `build.py`'nin eleme",
            "kararları `klinik_guvenlik_ihlali`ye bakıyor ve o bayrak **hiçbir kayıtta**",
            "oynamadı.", "",
            "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Hangi puanın «doğru» olduğu bilinmiyor** | ölçülen şey TUTARLILIK, "
            "doğruluk değil; iki çekiliş de yanlış olabilir |",
            "| ⛔⛔ **Gürültü ↔ kayma ayrılamadı** | aynı gün içinde tekrar ölçülmedi; "
            "ayırmak için aynı metne aynı gün iki kez sormak gerekir |",
            "| ⛔ **n=12 küçük** | %50 geniş bir güven aralığı taşır |",
            "| ⛔ **Yalnız kayıt düzeyi** | ORTALAMALAR bu gürültüden çok daha az etkilenir; "
            "Eksen 1'in bileşik puanı (T162) bu bulguyla otomatik olarak çürümez |",
            "| ⚠️ Tek judge, tek rubrik (v9) | başka rubrikte tekrarlanabilirlik ölçülmedi |", ""]
    (KOK / f"reports/analiz/{TARIH}-judge-tekrarlanabilirlik.json").write_text(
        json.dumps({"tarih": TARIH, "sonda": SONDA, "yon": dict(yon),
                    "boyut": {f"{k}|{t}": v for (k, t), v in boyut.items()}},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[4:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
