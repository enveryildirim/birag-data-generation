"""Türkçe ifade bankası çıkarımı (plan.md §13 Faz 1, K20). Bkz. Kural 7.

Girdi: campaigns/ (2.240, DOĞRULANMAMIŞ — K26) + hf_ready_dataset_old.jsonl (273, K28)
Yöntem: KALIP düzeyinde (K20) — tam cevaplar "doğru yanıt" olarak değil, yalnızca
Türkçe terapötik REGISTER örneği olarak toplanır. Klinik onay taşımaz (Kural 1/6).

Kullanım: uv run python scripts/analiz/2026-09-12-turkce-ifade-bankasi.py
"""
from __future__ import annotations
import collections
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
CAMPAIGNS_DIR = Path("/Users/pc/projects/birag/birag-tubitak/agentic_dataset_generation/campaigns")
HF_READY_OLD = Path("/Users/pc/projects/birag/birag-tubitak/agentic_dataset_generation/hf_ready_dataset_old.jsonl")
OUT_PATH = ROOT / "reports" / "analiz" / "2026-09-12-turkce-ifade-bankasi.md"

_SENT = re.compile(r"(?<=[.!?…])\s+")

# Fonksiyon kategorileri — anahtar kelime -> örnek cümleler. Bkz. plan.md §4, §7, §15.
CATEGORIES = {
    "yansitma_dogrulama (EPITOME duygusal tepki / OARS Reflection)": [
        "anlıyorum", "anlaşılır", "duyuyorum", "zorlayıcı olmalı", "yorucu olmalı",
        "zor bir duygu", "ağır bir yük", "yıpratıcı",
    ],
    "cift_yonlu_yansitma (ambivalans, TIP 35)": [
        "bir yandan", "diğer yandan", "hem ", " hem de",
    ],
    "ozerklik_saygisi (K21 dalkavukluk savunması ile karışmasın — karar hep kullanıcıda)": [
        "senin kararın", "sana kalmış", "seçim senin", "karar sizin", "zorlamıyorum",
    ],
    "yargisizlik": [
        "yargılamıyorum", "yargılamadan", "yargı olmadan",
    ],
    "rol_siniri_yonlendirme (Sor-Sun-Sor + profesyonel yönlendirme)": [
        "profesyonel", "bir uzmana", "doktora", "bir doktor", "sağlık kuruluşu",
        "psikiyatrist", "danışmanı",
    ],
    "olcek_teknikleri (0-10 güven cetveli)": [
        "0 ile 10", "1 ile 10", "0'dan 10", "kaç puan", "10 üzerinden",
    ],
    "durtu_somutlastirma (Marlatt dürtü sörfü)": [
        "fiziksel bir his", "düşünce mi", "birkaç dakika sürer",
    ],
}


def load_completions() -> list[dict]:
    out = []
    for campaign, path in {
        "kimyasal_madde": CAMPAIGNS_DIR / "kimyasal_madde" / "total_output.jsonl",
        "dijital": CAMPAIGNS_DIR / "dijital" / "total_output.jsonl",
        "receteli_ilac": CAMPAIGNS_DIR / "receteli_ilac" / "total_output.jsonl",
        "davranissal": CAMPAIGNS_DIR / "davranissal" / "total_output.jsonl",
    }.items():
        for l in open(path):
            if not l.strip():
                continue
            r = json.loads(l)
            asst = next((m for m in r["messages"] if m["role"] == "assistant"), None)
            if asst and asst.get("content"):
                out.append({"source": f"campaigns/{campaign}", "content": asst["content"]})
    for l in open(HF_READY_OLD):
        if not l.strip():
            continue
        r = json.loads(l)
        if r.get("final"):
            out.append({"source": "hf_ready_old", "content": r["final"]})
    return out


def sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENT.split(text.strip()) if s.strip()]


def opener_ngrams(sents: list[str], n: int = 3) -> collections.Counter:
    c = collections.Counter()
    for s in sents:
        words = s.split()
        if len(words) >= n:
            c[" ".join(words[:n])] += 1
    return c


def main():
    docs = load_completions()
    all_sents = []
    for d in docs:
        all_sents.extend(sentences(d["content"]))

    input_hash = hashlib.sha256(
        "".join(sorted(d["content"] for d in docs)).encode()
    ).hexdigest()[:16]

    openers = opener_ngrams(all_sents, n=3)
    top_openers = openers.most_common(30)

    category_hits = {}
    for cat, keywords in CATEGORIES.items():
        matched = [s for s in all_sents if any(k.lower() in s.lower() for k in keywords)]
        # tekrar eden neredeyse-aynı cümleleri ele (ilk 40 karaktere göre dedup)
        seen, examples = set(), []
        for s in matched:
            key = s[:40].lower()
            if key in seen:
                continue
            seen.add(key)
            examples.append(s)
            if len(examples) >= 8:
                break
        category_hits[cat] = {"count": len(matched), "examples": examples}

    lines = [
        "# Türkçe ifade bankası — ham çıkarım (kalıp düzeyinde, K20)",
        "",
        f"**Girdi:** campaigns/ (4 dosya, 2.240 kayıt) + hf_ready_dataset_old.jsonl (273 kayıt) "
        f"(sha256 içerik özeti:{input_hash}) · **Betik:** "
        f"`scripts/analiz/2026-09-12-turkce-ifade-bankasi.py` · **Tarih:** 2026-09-12",
        "",
        "⚠️ Bu belge **klinik onay taşımaz** (K26 — korpus DOĞRULANMAMIŞ). Yalnızca Türkçe "
        "terapötik REGISTER örneğidir — hangi kalıbın hangi durumda klinik olarak DOĞRU "
        "olduğu değil. Faz 2 üretiminde stil referansı olarak kullanılır, birebir "
        "kopyalanmaz.",
        "",
        f"**Toplam tamamlama:** {len(docs)} · **Toplam cümle:** {len(all_sents)}",
        "",
        "## En sık cümle başlangıçları (3-gram)",
        "",
    ]
    for phrase, count in top_openers:
        lines.append(f"- ({count}) {phrase}…")

    lines.append("\n## Fonksiyon kategorileri\n")
    for cat, data in category_hits.items():
        lines.append(f"### {cat} — {data['count']} eşleşme\n")
        for ex in data["examples"]:
            lines.append(f"- {ex}")
        lines.append("")

    OUT_PATH.write_text("\n".join(lines))
    print(f"yazıldı: {OUT_PATH}")
    print(f"tamamlama: {len(docs)}  cümle: {len(all_sents)}")
    for cat, data in category_hits.items():
        print(f"  {cat}: {data['count']}")


if __name__ == "__main__":
    main()
