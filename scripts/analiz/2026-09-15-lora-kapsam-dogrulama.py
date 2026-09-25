#!/usr/bin/env python3
"""LoRA kapsam merdiveninin KOŞU ÖNCESİ doğrulaması — K49'un gereği.

Neden var: `mlx_lm` eşleşmeyen bir `lora_parameters.keys` girdisi için **uyarı
vermez**. Faz 2'nin bütün koşuları bu yüzden sanılanın yarısı kapsamla yapıldı
(K49). Bu yüzden Faz 4 kapsam taramasının her kolu, eğitim başlamadan önce
"kaç modül, kaç parametre" diye ölçülür; sayılar rapora bu betikten girer.

⚠️ Bu betik K49'un olgusal ifadesini DÜZELTİR. K49 "bu modelde v_proj/k_proj
YOK" diyor. Ölçüm: **katman 0-23'te varlar, 24-41'de yoklar** (Gemma 4'ün üst
yarıda KV paylaşımı). K49'un pratik sonucu yine de doğru — `num_layers: 8`
SON 8 katmanı (34-41) seçer ve orada gerçekten yokturlar, o yüzden eski
config'in `self_antn.v_proj` anahtarı hiçbir şeyle eşleşmiyordu. Ama kapsam
`num_layers: 42`'ye açılırsa bu anahtarlar **24 modül** eşleşir; yani ifadenin
yanlış hali Faz 4'te yanlış karara götürürdü.

Kullanım: uv run python scripts/analiz/2026-09-15-lora-kapsam-dogrulama.py
"""
from __future__ import annotations

import json
from pathlib import Path

KOK = Path(__file__).parent.parent.parent
MODEL = KOK / "models" / "gemma-4-E4B-it-bf16-train"

ATT = ["self_attn.q_proj", "self_attn.o_proj"]
MLP = ["mlp.gate_proj", "mlp.up_proj", "mlp.down_proj"]

# Merdiven: her basamak bir öncekinden TEK bir eksende ayrılsın ki fark
# atfedilebilir olsun. K50'nin dar↔geniş karşılaştırması kapsamı ve rank'ı
# AYNI ANDA değiştiriyordu (8→32); hangisinin dili çevirdiği oradan okunamaz.
KOLLAR = [
    ("A-dar",      8, 8,  ["self_attn.q_proj"],  "Faz 2 config'i — değişmeyen taban"),
    ("B-derin",   42, 8,  ["self_attn.q_proj"],  "A + bütün katmanlar (tek fark: derinlik)"),
    ("C-dikkat",  42, 8,  ATT,                   "B + o_proj (tek fark: dikkat çıkışı)"),
    ("D-tam",     42, 8,  ATT + MLP,             "C + mlp (tek fark: ileri besleme)"),
    ("E-genis",   42, 32, ATT + MLP,             "D + rank 32 (tek fark: rank) = K50 geniş kolu"),
]


def olc(num_layers: int, rank: int, keys: list[str]) -> dict:
    from mlx_lm import load
    from mlx_lm.tuner.utils import linear_to_lora_layers

    model, _ = load(str(MODEL))
    model.freeze()
    linear_to_lora_layers(model, num_layers,
                          {"rank": rank, "scale": 20.0, "dropout": 0.0, "keys": keys})
    # trainable_parameters() iç içe sözlük döner; düzleştirerek say.
    from mlx.utils import tree_flatten
    duz = tree_flatten(model.trainable_parameters())
    egitilebilir = sum(v.size for _, v in duz)
    toplam = sum(v.size for _, v in tree_flatten(model.parameters()))
    modul = len({ad.rsplit(".", 1)[0] for ad, _ in duz})
    del model
    return {"modul": modul, "egitilebilir": egitilebilir, "toplam": toplam,
            "oran_yuzde": round(100 * egitilebilir / toplam, 4)}


def main() -> int:
    print(f"model: {MODEL.relative_to(KOK)}\n")
    satir = []
    for ad, nl, rank, keys, not_ in KOLLAR:
        o = olc(nl, rank, keys)
        satir.append({"kol": ad, "num_layers": nl, "rank": rank, "keys": keys,
                      "not": not_, **o})
        print(f"{ad:10} katman={nl:>2} rank={rank:>2} anahtar={len(keys)} | "
              f"modül {o['modul']:>4} | eğitilebilir {o['egitilebilir']:>12,} "
              f"({o['oran_yuzde']:>6.3f}%) | {not_}")

    cikti = KOK / "reports/analiz/2026-09-15-lora-kapsam-dogrulama.json"
    cikti.write_text(json.dumps(
        {"model": str(MODEL.relative_to(KOK)), "kollar": satir}, ensure_ascii=False, indent=1))
    print(f"\nyazıldı: {cikti.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
