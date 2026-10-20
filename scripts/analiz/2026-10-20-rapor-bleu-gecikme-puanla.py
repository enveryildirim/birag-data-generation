#!/usr/bin/env python3
"""BLEU/ROUGE ve tek istek gecikmesi — `notebooks/rapor-bleu-gecikme.ipynb` çıktılarının puanlanması.

Colab yalnız üretir (cevap, süre) ve BERTScore'u hesaplar (model gerektiriyor); sözcük
örtüşmesi ölçüleri ve hüküm burada (makine kuralı: burada model yüklenmez).

Ölçüler (hepsi 0–100):
  BLEU    sacrebleu corpus BLEU, varsayılan 13a tokenizasyon
  chrF    sacrebleu chrF — karakter n-gram; Türkçe gibi eklemeli dilde BLEU'dan daha anlamlı
  ROUGE   rouge-score ROUGE-1/2/L F1 — Türkçe harfleri silen varsayılan tokenizer YERİNE tr_fold + \\w+
  F1      sözcük torbası F1 (SQuAD tarzı), cevap başına ortalama
  BERTScore F1, Colab'da (`bert-base-multilingual-cased`), cevap başına ortalama
Boş cevap boş dizgi olarak puanlanır (0). Güven aralıkları: 1000 bootstrap, tohum 20261020.

Gecikme: tek istek, akışla — ilk jeton · görünen cevabın başlaması · toplam. Form ölçütü
«ortalama yanıt süresi < 2 sn»; hangi anın «yanıt» sayılacağı raporda iki türlü verilir.

Girdi : birag-rapor-olcum/{taban,ince}/{referans.jsonl,bilgi.json} · birag-rapor-olcum/gecikme/*.jsonl
        birag-rapor-olcum/{bertscore.jsonl,bertscore_bilgi.json} · data/eval-ref/olcek5k-ref.v1.jsonl
Çıktı : reports/analiz/2026-10-20-rapor-bleu-gecikme.md

Kullanım: uv run --with sacrebleu --with rouge-score python scripts/analiz/2026-10-20-rapor-bleu-gecikme-puanla.py [girdi_klasörü]
(iki paket projeye eklenmez — yalnız bu ölçüm için, Kural 4)
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import statistics as st
import sys
from collections import Counter
from pathlib import Path

import sacrebleu
from rouge_score import rouge_scorer

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from tohum_guvenlik import tr_fold  # noqa: E402

D = Path(sys.argv[1]) if len(sys.argv) > 1 else KOK / "birag-rapor-olcum"
REF = KOK / "data/eval-ref/olcek5k-ref.v1.jsonl"
RAPOR = KOK / "reports/analiz/2026-10-20-rapor-bleu-gecikme.md"
MODELLER = ("taban", "ince")
TOHUM, BOOT = 20261020, 1000
HEDEF_SN = 2.0


def jl(p: Path) -> list[dict]:
    return [json.loads(x) for x in p.open(encoding="utf-8") if x.strip()]


def sha16(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def sozcukler(s: str) -> list[str]:
    return re.findall(r"\w+", tr_fold(s))


class TrTokenizer:
    """rouge-score'un varsayılanı [a-z0-9] dışını siler ⇒ ç, ğ, ı, ö, ş, ü kaybolur."""

    def tokenize(self, s: str) -> list[str]:
        return sozcukler(s)


ROUGE = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], tokenizer=TrTokenizer())


def f1(aday: str, ref: str) -> float:
    a, r = Counter(sozcukler(aday)), Counter(sozcukler(ref))
    ortak = sum((a & r).values())
    if not ortak:
        return 0.0
    p, rc = ortak / sum(a.values()), ortak / sum(r.values())
    return 100 * 2 * p * rc / (p + rc)


KORPUS = {"BLEU": sacrebleu.metrics.BLEU(), "chrF": sacrebleu.metrics.CHRF()}


def hazirla(aday: list[str], ref: list[str], bert: list[float]) -> dict:
    """Bir kez hesaplanır: korpus ölçüleri için cümle başına yeterli istatistik, ötekiler için cümle puanı.
    Bootstrap yalnız bunları yeniden örnekler (ROUGE'u her örneklemde baştan koşmak dakikalar sürüyordu)."""
    rg = [ROUGE.score(r, a) for a, r in zip(aday, ref)]
    return {"korpus": {k: [list(x) for x in m._extract_corpus_statistics(aday, [ref])] for k, m in KORPUS.items()},
            "cumle": {"ROUGE-1": [100 * x["rouge1"].fmeasure for x in rg],
                      "ROUGE-2": [100 * x["rouge2"].fmeasure for x in rg],
                      "ROUGE-L": [100 * x["rougeL"].fmeasure for x in rg],
                      "F1": [f1(a, r) for a, r in zip(aday, ref)],
                      "BERTScore": [100 * b for b in bert]}}


def olcu(h: dict, ix: list[int]) -> dict[str, float]:
    out = {}
    for k, m in KORPUS.items():
        top = [sum(col) for col in zip(*(h["korpus"][k][i] for i in ix))]
        out[k] = m._compute_score_from_stats(top).score
    out.update({k: st.mean(v[i] for i in ix) for k, v in h["cumle"].items()})
    return out


def bootstrap(h: dict, n: int) -> dict[str, tuple[float, float]]:
    rng = random.Random(TOHUM)
    orn = [olcu(h, [rng.randrange(n) for _ in range(n)]) for _ in range(BOOT)]
    return {k: (sorted(o[k] for o in orn)[int(.025 * BOOT)], sorted(o[k] for o in orn)[int(.975 * BOOT) - 1])
            for k in orn[0]}


def main() -> None:
    ref = {o["id"]: o for o in jl(REF)}
    cev = {m: {r["id"]: r for r in jl(D / m / "referans.jsonl")} for m in MODELLER}
    bert = {(r["model"], r["id"]): r["F"] for r in jl(D / "bertscore.jsonl")}
    bilgi = {m: json.loads((D / m / "bilgi.json").read_text(encoding="utf-8")) for m in MODELLER}
    bbilgi = json.loads((D / "bertscore_bilgi.json").read_text(encoding="utf-8"))
    for m in MODELLER:
        assert set(cev[m]) == set(ref), f"⛔ {m}: referans setiyle aynı kayıtlar değil"
        assert bilgi[m].get("referans_sha16") == sha16(REF), f"⛔ {m}: Colab başka bir referans dosyası kullanmış"
    gec_dosya = sorted((D / "gecikme").glob("*.jsonl"))
    girdiler = [REF] + [D / m / f for m in MODELLER for f in ("referans.jsonl", "bilgi.json")] + \
               [D / "bertscore.jsonl", D / "bertscore_bilgi.json"] + gec_dosya

    ids = sorted(ref)
    gruplar = {"hepsi": ids, "tek tur": [i for i in ids if ref[i]["turn_type"] == "single"],
               "çok tur": [i for i in ids if ref[i]["turn_type"] == "multi"]}
    sonuc, aralik = {}, {}
    for m in MODELLER:
        for g, gi in gruplar.items():
            a = [cev[m][i]["cevap"] for i in gi]
            r = [ref[i]["referans"] for i in gi]
            b = [bert[(m, i)] for i in gi]
            h = hazirla(a, r, b)
            sonuc[(m, g)] = olcu(h, list(range(len(gi))))
            if g == "hepsi":
                aralik[m] = bootstrap(h, len(gi))
    olculer = list(sonuc[(MODELLER[0], "hepsi")])

    L = ["# BLEU/ROUGE ve tek istek gecikmesi — İP2 ölçütleri", "",
         f"- Betik: `scripts/analiz/{Path(__file__).name}` · tarih 2026-10-20",
         f"- Koşu: `notebooks/rapor-bleu-gecikme.ipynb` · " + " · ".join(
             f"{m} `{bilgi[m]['repo']}` rev `{bilgi[m]['revizyon'][:8]}` ({bilgi[m]['gpu']}, {bilgi[m]['tarih']})" for m in MODELLER),
         f"- BERTScore: `{bbilgi['bert_model']}` · bert-score {bbilgi['bert_score']}",
         f"- sacrebleu {sacrebleu.__version__} · güven aralığı %95, {BOOT} bootstrap",
         "- Girdiler (SHA256-16):", ""]
    L += [f"  - `{p.relative_to(KOK) if p.is_relative_to(KOK) else p}` `{sha16(p)}`" for p in girdiler]
    L += ["", "## 1. Referansa benzerlik — form hedefi: BLEU veya ROUGE > %80", "",
          f"Referanslı set: {len(ids)} kayıt, eğitimde görülmemiş (`reports/analiz/2026-10-20-rapor-referans-seti.md`).", "",
          "| ölçü | " + " | ".join(MODELLER) + " |", "|---|" + "---:|" * len(MODELLER)]
    for k in olculer:
        L.append(f"| {k} | " + " | ".join(
            f"**{sonuc[(m, 'hepsi')][k]:.1f}** ({aralik[m][k][0]:.1f}–{aralik[m][k][1]:.1f})" for m in MODELLER) + " |")
    L += ["", "Tek tur / çok tur:", "", "| ölçü | " + " | ".join(f"{m} · {g}" for m in MODELLER for g in ("tek tur", "çok tur")) + " |",
          "|---|" + "---:|" * (2 * len(MODELLER))]
    for k in olculer:
        L.append(f"| {k} | " + " | ".join(f"{sonuc[(m, g)][k]:.1f}" for m in MODELLER for g in ("tek tur", "çok tur")) + " |")
    bos = {m: sum(not cev[m][i]["cevap"].strip() for i in ids) for m in MODELLER}
    kes = {m: sum(cev[m][i]["kesildi"] for i in ids) for m in MODELLER}
    L += ["", f"- Boş cevap: " + " · ".join(f"{m} {bos[m]}" for m in MODELLER) +
          " · 2048'de kesilen: " + " · ".join(f"{m} {kes[m]}" for m in MODELLER),
          f"- Sözcük ortancası — referans {st.median(len(sozcukler(ref[i]['referans'])) for i in ids):.0f} · " +
          " · ".join(f"{m} {st.median(len(sozcukler(cev[m][i]['cevap'])) for i in ids):.0f}" for m in MODELLER), "",
          "## 2. Tek istek gecikmesi — form hedefi: ortalama < 2 sn", "",
          "| kol | n | ilk jeton ort / ortanca | görünen cevabın başlaması ort / ortanca | toplam ort / ortanca / p90 | toplam < 2 sn | jeton ortanca | kesilen |",
          "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for p in gec_dosya:
        R = jl(p)
        t = sorted(r["toplam_sn"] for r in R)
        L.append(f"| {p.stem} | {len(R)} "
                 f"| {st.mean(r['ilk_jeton_sn'] for r in R):.2f} / {st.median(r['ilk_jeton_sn'] for r in R):.2f} "
                 f"| {st.mean(r['cevap_bas_sn'] for r in R):.2f} / {st.median(r['cevap_bas_sn'] for r in R):.2f} "
                 f"| {st.mean(t):.2f} / {st.median(t):.2f} / {t[int(.9 * len(t)) - 1]:.2f} "
                 f"| {sum(x < HEDEF_SN for x in t)} / {len(t)} "
                 f"| {st.median(r['jeton'] for r in R):.0f} | {sum(r['kesildi'] for r in R)} |")
    L += ["", "- Ortam: Colab A100 80 GB, Hugging Face `generate` (Unsloth), bf16, açgözlü, parti 1, akışla. "
          "Üretim sunucusu (vLLM vb.) ve nicemleme bu sayıları değiştirir; burada ölçülen bu ortamdır.",
          "- «Görünen cevabın başlaması» kullanıcının ilk harfi gördüğü an: düşünme açıkken düşünce bitene kadar bekler.",
          "- Gecikme seti: `evals/golden.test.jsonl` (48 soru); ilk 2 istek ısınma, sayılmadı.", "",
          "## Okuma", "",
          "- BLEU/ROUGE «bu referansa sözcük benzerliği»dir; aynı duruma birçok doğru terapötik cevap verilebildiği için "
          "serbest diyalogda %80 beklenmez (K9). Rapor bu sayıları hedefle değil, iki modelin kıyasıyla ve BERTScore/chrF ile "
          "birlikte yorumlamalı.", ""]
    RAPOR.write_text("\n".join(L), encoding="utf-8")
    print(f"yazıldı: {RAPOR.relative_to(KOK)}")


if __name__ == "__main__":
    main()
