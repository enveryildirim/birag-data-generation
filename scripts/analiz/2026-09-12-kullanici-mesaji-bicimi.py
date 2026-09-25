"""Kullanıcı mesajı biçim analizi — uzunluk + yazım register'ı (plan.md §6, K42).

Soru: gerçek sohbet robotu kullanıcısı kısa yazar; tohum korpusumuz bunu temsil ediyor mu?
Girdi: data/seeds.jsonl (2.240) + datasets/v0.0.1/train.jsonl (20)

Kullanım: uv run python scripts/analiz/2026-09-12-kullanici-mesaji-bicimi.py
"""
from __future__ import annotations
import hashlib
import json
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
SEEDS = ROOT / "data" / "seeds.jsonl"
V001 = ROOT / "datasets" / "v0.0.1" / "train.jsonl"
OUT = ROOT / "reports" / "analiz" / "2026-09-12-kullanici-mesaji-bicimi.md"

_SENT = re.compile(r"(?<=[.!?…])\s+")
BUCKETS = [(1, 8, "kısa açılış (1-8 kelime)"), (9, 25, "orta (9-25)"),
           (26, 60, "uzun (26-60)"), (61, 10**6, "çok uzun (60+)")]


def profile(msgs: list[str]) -> dict:
    words = [len(m.split()) for m in msgs]
    sents = [len([x for x in _SENT.split(m.strip()) if x]) for m in msgs]
    n = len(msgs)
    return {
        "n": n,
        "kelime_medyan": statistics.median(words),
        "kelime_ort": round(statistics.mean(words), 1),
        "kelime_min": min(words),
        "kelime_maks": max(words),
        "cumle_medyan": statistics.median(sents),
        "kovalar": {lbl: round(100 * sum(1 for w in words if lo <= w <= hi) / n, 1)
                    for lo, hi, lbl in BUCKETS},
        "tek_cumle_yuzde": round(100 * sum(1 for s in sents if s == 1) / n, 1),
        "kucuk_harf_baslangic_yuzde": round(100 * sum(1 for m in msgs if m.strip()[0].islower()) / n, 1),
        "noktalama_ile_biten_yuzde": round(100 * sum(1 for m in msgs if m.strip()[-1] in ".!?…") / n, 1),
        "hic_noktalama_yok_yuzde": round(100 * sum(1 for m in msgs if not any(c in m for c in ".,!?")) / n, 1),
    }


def main():
    seeds = [json.loads(l)["user_message"] for l in open(SEEDS) if l.strip()]
    v001 = [next(m["content"] for m in json.loads(l)["messages"] if m["role"] == "user")
            for l in open(V001) if l.strip()]

    p_seeds, p_v001 = profile(seeds), profile(v001)
    seeds_hash = hashlib.sha256(SEEDS.read_bytes()).hexdigest()[:16]
    v001_hash = hashlib.sha256(V001.read_bytes()).hexdigest()[:16]

    lines = [
        "# Kullanıcı mesajı biçim analizi — uzunluk ve yazım register'ı",
        "",
        f"**Girdi:** `data/seeds.jsonl` (sha256:{seeds_hash}) · "
        f"`datasets/v0.0.1/train.jsonl` (sha256:{v001_hash}) · **Betik:** "
        f"`scripts/analiz/2026-09-12-kullanici-mesaji-bicimi.py` · **Tarih:** 2026-09-12",
        "",
        "Soru: gerçek sohbet robotu kullanıcısı uzun paragraf yazmaz. Korpusumuz bunu temsil ediyor mu?",
        "",
        "| Ölçüt | Tohum korpusu | v0.0.1 |",
        "|---|---|---|",
        f"| Kayıt | {p_seeds['n']} | {p_v001['n']} |",
        f"| Kelime medyanı | **{p_seeds['kelime_medyan']:.0f}** | **{p_v001['kelime_medyan']:.0f}** |",
        f"| Kelime ortalaması | {p_seeds['kelime_ort']} | {p_v001['kelime_ort']} |",
        f"| Kelime min–maks | {p_seeds['kelime_min']}–{p_seeds['kelime_maks']} | {p_v001['kelime_min']}–{p_v001['kelime_maks']} |",
        f"| Cümle medyanı | {p_seeds['cumle_medyan']:.0f} | {p_v001['cumle_medyan']:.0f} |",
        f"| Tek cümlelik mesaj | %{p_seeds['tek_cumle_yuzde']} | %{p_v001['tek_cumle_yuzde']} |",
    ]
    for _, _, lbl in BUCKETS:
        lines.append(f"| {lbl} | %{p_seeds['kovalar'][lbl]} | %{p_v001['kovalar'][lbl]} |")
    lines += [
        f"| Küçük harfle başlayan | %{p_seeds['kucuk_harf_baslangic_yuzde']} | %{p_v001['kucuk_harf_baslangic_yuzde']} |",
        f"| Noktalamayla biten | %{p_seeds['noktalama_ile_biten_yuzde']} | %{p_v001['noktalama_ile_biten_yuzde']} |",
        f"| Hiç noktalama yok | %{p_seeds['hic_noktalama_yok_yuzde']} | %{p_v001['hic_noktalama_yok_yuzde']} |",
        "",
        "## Yorum",
        "",
        "**1-8 kelimelik mesaj ve noktalamasız mesaj korpusta hiç yok.** Gerçek kullanımda en sık",
        "görülecek açılış biçimi (*\"bırakamıyorum ya\"*) eğitim verisinde %0 temsil ediliyor.",
        "",
        "⚠️ Bu medyan **kullanıcılar hakkında bir kanıt değil** — korpus sentetik üretim, yani",
        "bir LLM'e kullanıcı personası yazdırıldığında ne çıktığının kanıtı. Üretici artefaktı.",
        "",
        "**İkinci risk (daha tehlikeli):** veri \"zengin girdi → çok detaylı yansıtma\" eşleşmesi",
        "öğretiyor. Model bunu öğrenip karşısında iki kelime bulduğunda en olası başarısızlık",
        "**detay uydurmak**tır. v0.0.1'de grounding 4.95/5 çıktı ama yalnızca zengin girdilerde",
        "ölçüldü — metrik, riskin en yüksek olduğu yerde kör.",
        "",
        "Karar: **K42** (plan.md §6).",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines))
    print(f"yazıldı: {OUT}")
    print(f"tohum kelime medyanı: {p_seeds['kelime_medyan']:.0f}  kısa açılış: %{p_seeds['kovalar']['kısa açılış (1-8 kelime)']}")


if __name__ == "__main__":
    main()
