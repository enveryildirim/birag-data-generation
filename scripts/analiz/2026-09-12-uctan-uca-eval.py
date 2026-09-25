"""Uçtan uca eval çözümlemesi — thinking dili, thinking:cevap oranı, gecikme bütçesi.
Bkz. Kural 7, plan.md §4 (thinking tasarımı), §8 (gecikme KPI), K38/T12.

Soru 1: Eğitilmemiş E4B çıkarımda thinking'i hangi dilde kuruyor? (T12 eğitim
        tarafında İngilizce bulmuştu — çıkarım tarafı ölçülmemişti)
Soru 2: thinking ne kadar uzun? Veri setimizdeki referans thinking'e göre nerede?
Soru 3: Cevap başına üretilen token kaçı kullanıcıya hiç gitmiyor? (gecikme bütçesi)

Kullanım: uv run python scripts/analiz/2026-09-12-uctan-uca-eval.py <eval_dizini>
"""
from __future__ import annotations
import hashlib
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.resolve()
DATASET = ROOT / "datasets" / "v0.0.1" / "train.jsonl"
OUT = ROOT / "reports" / "analiz" / "2026-09-12-uctan-uca-eval.md"

# Dil vekili — sözlük değil, ucuz ve şeffaf bir gösterge (yanılabilir, sayı değil işaret).
TR_KARAKTER = set("ğışçöüĞİŞÇÖÜ")
TR_KELIME = {"bir", "bu", "ve", "için", "ile", "ama", "değil", "kullanıcı", "soru",
             "cevap", "yani", "çünkü", "olarak", "var", "yok", "gibi"}
EN_KELIME = {"the", "a", "and", "to", "of", "is", "user", "response", "this", "that",
             "should", "not", "it", "for", "answer", "process", "thinking"}


def dil_isareti(metin: str) -> str:
    kelimeler = re.findall(r"[A-Za-zğışçöüĞİŞÇÖÜıİ]+", metin.lower())
    if not kelimeler:
        return "bos"
    tr = sum(w in TR_KELIME for w in kelimeler) + sum(c in TR_KARAKTER for c in metin) / 5
    en = sum(w in EN_KELIME for w in kelimeler)
    if tr == en == 0:
        return "belirsiz"
    return "tr" if tr > en else "en"


def main(eval_dir: str):
    ed = Path(eval_dir).resolve()
    rows = [json.loads(l) for l in open(ed / "generations.jsonl") if l.strip()]
    metrics = json.loads((ed / "metrics.json").read_text())

    # referans: veri setinde İNSAN/üretici tarafından yazılmış thinking
    ref = [json.loads(l) for l in open(DATASET) if l.strip()]
    ref_think = [m["thinking"] for r in ref for m in r["messages"]
                 if m["role"] == "assistant" and m.get("thinking")]
    ref_comp = [m["content"] for r in ref for m in r["messages"]
                if m["role"] == "assistant" and m.get("thinking")]

    lines = [
        "# Uçtan uca eval — thinking dili, uzunluk ve gecikme bütçesi",
        "",
        f"**Girdi:** `{ed.relative_to(ROOT)}/generations.jsonl` "
        f"(sha256:{hashlib.sha256((ed / 'generations.jsonl').read_bytes()).hexdigest()[:16]}) · "
        f"**Betik:** `scripts/analiz/2026-09-12-uctan-uca-eval.py` · **Tarih:** 2026-09-12",
        "",
        f"Koşu: `{metrics['run']}` · eval kümesi **{metrics['n_eval']} kayıt** (eğitimde görülmedi) · "
        f"max_tokens={metrics['max_tokens']} · judge `{metrics['judge_model']}`",
        "",
        "> **n=4.** Bu bir kalite ölçümü DEĞİL; borunun aktığını ve maliyetin ne olduğunu",
        "> gösteren bir duman testidir. Varyantlar arası puan farkları bu ölçekte gürültüdür.",
        "",
        "## 1. thinking dili (T12/K38'in çıkarım tarafı)",
        "",
        "| Varyant | thinking tr | thinking en | completion tr | completion en |",
        "|---|---|---|---|---|",
    ]
    for varyant in ("baseline", "lora"):
        v = [r for r in rows if r["varyant"] == varyant]
        td = [dil_isareti(r["thinking"]) for r in v]
        cd = [dil_isareti(r["completion"]) for r in v]
        lines.append(f"| {varyant} | {td.count('tr')}/{len(v)} | {td.count('en')}/{len(v)} | "
                     f"{cd.count('tr')}/{len(v)} | {cd.count('en')}/{len(v)} |")
    rt = [dil_isareti(t) for t in ref_think]
    lines.append(f"| *veri seti (referans)* | {rt.count('tr')}/{len(rt)} | {rt.count('en')}/{len(rt)} | — | — |")

    kalip = sum(r["thinking"].lstrip().startswith("Here's a thinking process") for r in rows)
    lines += ["",
              f"**{kalip}/{len(rows)}** üretim thinking'e birebir aynı İngilizce kalıpla başlıyor: "
              f"*\"Here's a thinking process that leads to the suggested response:\"* — "
              "bu Gemma'nın kendi post-training izi, bizim system prompt'umuzdan gelmiyor.",
              "",
              "## 2. thinking uzunluğu ve thinking:cevap oranı",
              "",
              "| Kaynak | thinking (kelime, medyan) | completion (kelime, medyan) | oran |",
              "|---|---|---|---|"]

    def satir(ad, ts, cs):
        mt, mc = statistics.median(ts), statistics.median(cs)
        return f"| {ad} | {mt:.0f} | {mc:.0f} | **{mt / mc:.0f}x** |"

    for varyant in ("baseline", "lora"):
        v = [r for r in rows if r["varyant"] == varyant]
        lines.append(satir(varyant, [len(r["thinking"].split()) for r in v],
                           [len(r["completion"].split()) for r in v]))
    lines.append(satir("*veri seti (referans)*", [len(t.split()) for t in ref_think],
                       [len(c.split()) for c in ref_comp]))

    lines += ["", "## 3. Gecikme bütçesi", "",
              "| Varyant | üretilen token (ort.) | tok/sn | cevap süresi (ort.) | kullanıcıya giden pay |",
              "|---|---|---|---|---|"]
    for varyant in ("baseline", "lora"):
        v = [r for r in rows if r["varyant"] == varyant]
        m = metrics["varyantlar"][varyant]
        pay = statistics.mean(len(r["completion"].split()) /
                              max(1, len(r["thinking"].split()) + len(r["completion"].split()))
                              for r in v)
        lines.append(f"| {varyant} | {m['uretim_token_ortalama']} | {m['uretim_tps_ortalama']} | "
                     f"**{m['uretim_sn_ortalama']} sn** | %{100 * pay:.0f} |")

    lines += ["", "## 4. Kapı ve judge sonuçları", "",
              "| Varyant | checks geçen | klinik güvenlik | rol sınırı | tuzak ihlali | judge süresi (ort.) |",
              "|---|---|---|---|---|---|"]
    for varyant in ("baseline", "lora"):
        m = metrics["varyantlar"][varyant]
        v = [r for r in rows if r["varyant"] == varyant]
        js = [r["judge_sn"] for r in v if r.get("judge_sn")]
        lines.append(f"| {varyant} | {m['checks_gecen']}/{metrics['n_eval']} | "
                     f"{m['klinik_guvenlik_ihlali']} | {m['rol_siniri_ihlali']} | "
                     f"{m['tuzak_ihlali_toplam']} | {statistics.mean(js):.0f} sn |")

    lines += ["", "### Judge rubriği (⚠️ n=4 — GÜRÜLTÜ, kalite okuması değil)", "",
              "Kayda geçiriliyor çünkü ölçüldü; **yorumlanmıyor** çünkü 4 kayıtla iki varyant ayrılamaz.",
              "",
              "| Boyut | baseline | lora |", "|---|---|---|"]
    for d in ["duygusal_tepki", "yorumlama", "kesif", "mi_uyumu",
              "grounding", "kisalik_dogallik", "dil_butunlugu"]:
        b = metrics["varyantlar"]["baseline"]["judge_ortalama"]
        l = metrics["varyantlar"]["lora"]["judge_ortalama"]
        lines.append(f"| {d} | {b[d]} | {l[d]} |")

    lines += ["", "### checks.py'nin elediği gerekçeler", ""]
    for r in rows:
        if not r["_checks"]["passed"]:
            neden = (r["_checks"].get("length_error")
                     or ("soru sayısı " + str(r["_checks"]["question_count"])))
            lines.append(f"- `{r['varyant']}` `{r['id'][:8]}` — {neden}")

    lines += ["", "## 5. Kayıt başına maliyet ve Faz 4 ekstrapolasyonu", ""]
    gen = statistics.mean(metrics["varyantlar"][v]["uretim_sn_ortalama"] for v in ("baseline", "lora"))
    jud = statistics.mean(r["judge_sn"] for r in rows if r.get("judge_sn"))
    lines += [
        f"- Üretim (yerel, E4B bf16, M5 Max): **{gen:.1f} sn/kayıt** · tepe bellek "
        f"{metrics['varyantlar']['lora']['tepe_bellek_gb']} GB · model yükleme ~1 sn",
        f"- Judge (`agy`, uzaktan): **{jud:.0f} sn/kayıt** — yani darboğaz üretim değil, **judge**",
        f"- Eğitim (50 adım, 16 kayıt): 23.4 sn",
        "",
        f"**v0.1.0 ölçeğine (≈1.000 kayıt) doğrusal ekstrapolasyon:** eval üretimi "
        f"~{1000 * gen / 3600:.1f} saat, judge ~{1000 * jud / 3600:.1f} saat. "
        "Judge paralelleştirilmezse Faz 4'te her tur bir iş günü sürer.",
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n")
    print(f"yazıldı: {OUT}")
    print("\n".join(lines[6:]))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("kullanım: ... <eval_dizini>")
        sys.exit(1)
    main(sys.argv[1])
