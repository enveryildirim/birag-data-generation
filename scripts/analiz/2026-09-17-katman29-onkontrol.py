#!/usr/bin/env python3
"""Katman 29 deneyinin ÖNKONTROLÜ — kapsam gerçekten istenen katmanlara mı iniyor?

⛔⛔ K49'un dersi: sessiz bir eşleşmezlik koşuyu düşürmez, **yanlış koşuyu doğru
sandırır**. Bu deney `mlx_lm`'in belgelenmemiş bir yolunu kullanıyor (tam modül
yolu + `num_layers: 0`) ⇒ önkontrol **zorunlu**.

⭐ Mekanizma (`linear_to_lora_layers` kaynağından okundu, tahmin değil):
    for l in model.layers[-max(num_layers,0):]:
        ... if k in keys          # k = KATMAN İÇİ göreli ad
    lora_modules = [... for k,m in model.named_modules() if k in keys]   # k = TAM yol
⇒ `num_layers: 0` ile göreli adlar eşleşmez; tam yollar ikinci geçişte eşleşir.
⚠️ `[-0:]` bütün katmanlar demektir — ama göreli ad `keys`te olmadığı için o
   geçiş hiçbir şey uygulamaz. Bu, **varsayım değil, ölçülen** bir davranış.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
MODEL = KOK / "models/gemma-4-E4B-it-bf16-train"
CIKTI = KOK / "reports/analiz/2026-09-17-katman29-onkontrol.md"


def katmanlar(num_layers: int, keys: list[str]) -> list[int]:
    from mlx_lm.utils import load
    from mlx_lm.tuner.utils import linear_to_lora_layers
    m, _ = load(str(MODEL))
    m.freeze()
    linear_to_lora_layers(m, num_layers, {"rank": 8, "scale": 20.0, "dropout": 0.0, "keys": keys})
    kat = set()
    for k, mod in m.named_modules():
        if type(mod).__name__.startswith("LoRA"):
            p = k.split(".layers.")
            if len(p) > 1:
                kat.add(int(p[1].split(".")[0]))
    return sorted(kat)


def main() -> int:
    import yaml
    sat = ["# Katman 29 deneyi — kapsam önkontrolü", "",
           "**Betik:** `scripts/analiz/2026-09-17-katman29-onkontrol.py` · "
           "**Tarih:** 2026-09-17", "",
           "⛔ Bu deney `mlx_lm`'in belgelenmemiş bir yolunu kullanıyor (tam modül yolu + "
           "`num_layers: 0`). K49: sessiz eşleşmezlik **yanlış koşuyu doğru sandırır** ⇒ "
           "kapsam koşudan ÖNCE ölçülür.", "",
           "| config | `num_layers` | **uygulanan katmanlar** | sayı | beklenen | |",
           "|---|---:|---|---:|---|---|"]
    hata = 0
    for ad, bek in (("u-k12", list(range(30, 42))), ("u-k13", list(range(29, 42))),
                    ("p-atla29", [28] + list(range(30, 42))),
                    ("p-sadece29", [29] + list(range(31, 42)))):
        y = KOK / f"configs/training/{ad}.yaml"
        if not y.exists():
            sat.append(f"| `{ad}` | — | ⛔ config yok | | | |")
            hata += 1
            continue
        c = yaml.safe_load(y.read_text(encoding="utf-8"))["mlx"]
        k = katmanlar(c["num_layers"], c["lora_parameters"]["keys"])
        ok = k == bek
        hata += 0 if ok else 1
        kisa = f"{k[0]}" + (f"–{k[-1]}" if k == list(range(k[0], k[-1] + 1)) else f", …{k}")
        sat.append(f"| `{ad}` | {c['num_layers']} | `{k}` | **{len(k)}** | "
                   f"`{bek[0]}`… | {'✅' if ok else '⛔ SAPMA'} |")
    sat += ["", "## ⭐ Deneyin tasarımı — kapasite ile KATMAN ayrılıyor", "",
            "| kol | katman | kapasite | soru |", "|---|---|---:|---|",
            "| `u-k12` | 30–41 | 12 | ölçüldü: **%46** |",
            "| `u-k13` | 29–41 | 13 | ölçüldü: **%8** |",
            "| ⭐ `p-atla29` | **28** + 30–41 | **13** | 13 katman ama **29 YOK** |",
            "| ⭐ `p-sadece29` | **29** + 31–41 | **12** | 12 katman ama **29 VAR** |", "",
            "➡️ *Kapasite (katman sayısı) ile kimliğin (hangi katman) etkisi ancak ikisi "
            "ÇAPRAZLANIRSA ayrılır: 13 katman 29'suz ve 12 katman 29'lu.*", "",
            "| sonuç | çıkarım |", "|---|---|",
            "| `p-atla29` ≈ %46 **ve** `p-sadece29` ≈ %8 | ⭐ **katman 29** |",
            "| `p-atla29` ≈ %8 **ve** `p-sadece29` ≈ %46 | ⭐ **kapasite**, katman değil |",
            "| ikisi de ≈ %46 ya da ikisi de ≈ %8 | ⛔ ikisi de değil — başka bir şey |",
            "| karışık | ⛔ tek yönlü okuma yok |", "", "⭐ **Tahmin koşudan ÖNCE yazıldı:** "
            "`p-atla29` ≈ %46, `p-sadece29` ≈ %8 (yani katman 29 hipotezi).", ""]
    CIKTI.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[5:]))
    print(f"→ {CIKTI.relative_to(KOK)}")
    return 1 if hata else 0


if __name__ == "__main__":
    raise SystemExit(main())
