"""Judge karşılaştırması — kendini kayırma (self-preference) ölçümü. Bkz. Kural 7, K43.

Soru: üreticiyle aynı aileden bir judge, kendi çıktısına bağımsız bir judge'dan
daha yüksek puan verir mi? (plan.md §16 anti-pattern'inin ampirik sınanması)

Üç judge, BİREBİR AYNI prompt (prompts/judge-eksen1.v1.md):
  · qwen3.8:27b-mlx   — bağımsız aile (üretim judge'ı, data/judged/v0.0.1.jsonl)
  · claude-sonnet-5   — 20 kaydı YAZAN model (saf kendini puanlama)
  · claude-opus-5     — aynı aile, farklı model

Kullanım: uv run python scripts/analiz/2026-09-12-judge-karsilastirma.py <sonnet.json> <opus.json>
"""
from __future__ import annotations
import hashlib
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
JUDGED = ROOT / "datasets" / "v0.0.1" / "train.jsonl"
QWEN_SRC = ROOT / "data" / "judged" / "v0.0.1.jsonl"
GEMINI_SRC = ROOT / "data" / "judged" / "v0.0.1-gemini.jsonl"
OUT = ROOT / "reports" / "analiz" / "2026-09-12-judge-karsilastirma.md"
RAW_DIR = ROOT / "reports" / "analiz" / "judge-karsilastirma"

DIMS = ["duygusal_tepki", "yorumlama", "kesif", "mi_uyumu",
        "grounding", "kisalik_dogallik", "dil_butunlugu"]
OLCEK = {"duygusal_tepki": 2, "yorumlama": 2, "kesif": 2, "mi_uyumu": 5,
         "grounding": 5, "kisalik_dogallik": 5, "dil_butunlugu": 5}


def load_scores(path: Path) -> dict[int, dict]:
    data = json.loads(path.read_text())
    return {int(r["idx"]): r for r in data}


def normalize(val: float, dim: str) -> float:
    """Farklı ölçekleri 0-1'e indir ki boyutlar arası ortalama anlamlı olsun."""
    return val / OLCEK[dim]


def main(sonnet_path: str, opus_path: str):
    qwen_rows = [json.loads(l) for l in open(QWEN_SRC) if l.strip()]
    qwen = {i: r["judge"] for i, r in enumerate(qwen_rows) if r.get("judge")}
    sonnet = load_scores(Path(sonnet_path))
    opus = load_scores(Path(opus_path))

    judges = {"qwen3.8-27b (bağımsız)": qwen, "claude-sonnet-5 (ÜRETİCİ)": sonnet,
              "claude-opus-5 (aynı aile)": opus}
    if GEMINI_SRC.exists():
        g_rows = [json.loads(l) for l in open(GEMINI_SRC) if l.strip()]
        judges["gemini-3.8-flash (bağımsız)"] = {i: r["judge"] for i, r in enumerate(g_rows) if r.get("judge")}
    idxs = sorted(set.intersection(*(set(v) for v in judges.values())))

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for name, path in [("sonnet", sonnet_path), ("opus", opus_path)]:
        (RAW_DIR / f"{name}.json").write_text(Path(path).read_text())

    lines = [
        "# Judge karşılaştırması — kendini kayırma ölçümü",
        "",
        f"**Girdi:** `datasets/v0.0.1/train.jsonl` (sha256:{hashlib.sha256(JUDGED.read_bytes()).hexdigest()[:16]}) "
        f"· ham judge çıktıları `reports/analiz/judge-karsilastirma/` · **Betik:** "
        f"`scripts/analiz/2026-09-12-judge-karsilastirma.py` · **Tarih:** 2026-09-12",
        "",
        f"Üç judge, birebir aynı prompt (`prompts/judge-eksen1.v1.md`), aynı {len(idxs)} kayıt.",
        "20 kaydı **claude-sonnet-5 yazdı** — yani o judge kendi çıktısını puanlıyor.",
        "",
        "## Boyut ortalamaları",
        "",
        "| Boyut | Ölçek | " + " | ".join(judges) + " |",
        "|---|---|" + "---|" * len(judges),
    ]
    means = {name: {} for name in judges}
    for dim in DIMS:
        row = [f"| {dim} | 0-{OLCEK[dim]} "]
        for name, sc in judges.items():
            m = statistics.mean(sc[i][dim] for i in idxs)
            means[name][dim] = m
            row.append(f"| {m:.2f} ")
        lines.append("".join(row) + "|")

    lines += ["", "## Normalize genel ortalama (0-1)", ""]
    genel = {}
    for name in judges:
        genel[name] = statistics.mean(normalize(means[name][d], d) for d in DIMS)
        lines.append(f"- **{name}**: {genel[name]:.3f}")

    base = genel["qwen3.8-27b (bağımsız)"]
    lines += ["", "## Bağımsız judge'a göre fark", ""]
    for name in judges:
        if name.startswith("qwen"):
            continue
        fark = genel[name] - base
        yuzde = 100 * fark / base
        lines.append(f"- **{name}**: {fark:+.3f} ({yuzde:+.1f}%)")

    # kayıt bazında anlaşma
    lines += ["", "## Kayıt bazında anlaşma", ""]
    import itertools
    for a, b in itertools.combinations(judges, 2):
        diffs = []
        for i in idxs:
            da = statistics.mean(normalize(judges[a][i][d], d) for d in DIMS)
            db = statistics.mean(normalize(judges[b][i][d], d) for d in DIMS)
            diffs.append(abs(da - db))
        lines.append(f"- {a} ↔ {b}: ortalama mutlak fark **{statistics.mean(diffs):.3f}** "
                     f"(maks {max(diffs):.3f})")

    # güvenlik / rol sınırı / tuzak
    lines += ["", "## Sert kapı boyutları", "",
              "| Judge | klinik güvenlik ihlali | rol sınırı ihlali | tuzak ihlali (toplam) |",
              "|---|---|---|---|"]
    for name, sc in judges.items():
        g = sum(1 for i in idxs if sc[i]["klinik_guvenlik_ihlali"])
        r = sum(1 for i in idxs if sc[i]["rol_siniri_ihlali"])
        t = sum(len(sc[i].get("tuzak_ihlali", [])) for i in idxs)
        lines.append(f"| {name} | {g} | {r} | {t} |")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n")
    print(f"yazıldı: {OUT}")
    for name in judges:
        print(f"  {name}: genel {genel[name]:.3f}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("kullanım: ... <sonnet_scores.json> <opus_scores.json>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
