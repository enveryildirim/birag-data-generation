#!/usr/bin/env python3
"""BLEU/ROUGE için referanslı test seti — ölçek-5k'nın eğitimde görülmemiş kayıtlarından.

Neden ayrı bir set: eval setleri (`evals/`) bilerek referanssız (K20-C, `src/golden_checks.py`);
başvuru formu İP2 ise «Türkçe testlerde BLEU veya ROUGE > %80» istiyor (K9 bu hedefi yeniden
tanımladı, yürütücü onayı bekliyor). Referanslı ölçüm için gereken iki şey ölçek-5k'da var:
son asistan turu bir referans cevap ve kayıtlar ince modelin eğitim verisinde (`v0.1.1`) YOK.

⚠️ Sınırlar (rapora yazılmalı):
  - Ölçek-5k'nın 5000 satırının tamamı daha önce kullanılmış tohumlardan geliyor (plan raporu):
    kullanıcı metni yeni, senaryo tohumu eğitimle ortak. Tam bağımsız değil.
  - Referansı başka bir model yazdı (Haiku; C aşaması varsa Sonnet denetiminden geçmiş).
    Ölçülen şey «referansa sözcük benzerliği», terapötik kalite değil.
  - Parçada C aşaması dosyası varsa o, yoksa B aşaması okunur; aşama dağılımı rapora yazılır.

Seçim: `run_checks` geçen, eval setlerinin tohumlarını kullanmayan kayıtlar; tek/çok tur ve
`bicim` katmanlarında havuzdaki oranla, sabit tohumla 200 kayıt.

Girdi : data/candidates/olcek5k/kayit/parca*.{B,C}.jsonl · evals/*.jsonl (tohum dışlama)
Çıktı : data/eval-ref/olcek5k-ref.v1.jsonl (IMMUTABLE — varsa yazmaz) · reports/analiz/2026-10-20-rapor-referans-seti.md
"""
from __future__ import annotations

import hashlib
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from checks import run_checks  # noqa: E402

KAYIT = KOK / "data/candidates/olcek5k/kayit"
CIKTI = KOK / "data/eval-ref/olcek5k-ref.v1.jsonl"
RAPOR = KOK / "reports/analiz/2026-10-20-rapor-referans-seti.md"
N = 200
TOHUM = 20261020


def jl(p: Path) -> list[dict]:
    return [json.loads(x) for x in p.open(encoding="utf-8") if x.strip()]


def sha16(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def eval_tohumlari() -> set[str]:
    tohum = set()
    for p in sorted((KOK / "evals").glob("*.jsonl")):
        for o in jl(p):
            if isinstance(o.get("kaynak"), dict) and o["kaynak"].get("seed_id"):
                tohum.add(o["kaynak"]["seed_id"])
    return tohum


def main() -> None:
    if CIKTI.exists():
        sys.exit(f"⛔ {CIKTI.relative_to(KOK)} zaten var (IMMUTABLE) — yeni sürüm için adı değiştirin")
    parcalar = sorted({p.name.split(".")[0] for p in KAYIT.glob("parca*.jsonl")})
    dosyalar = [KAYIT / f"{pc}.C.jsonl" if (KAYIT / f"{pc}.C.jsonl").exists() else KAYIT / f"{pc}.B.jsonl"
                for pc in parcalar]
    asama = Counter(p.name.split(".")[1] for p in dosyalar)
    dislanan = eval_tohumlari()

    havuz, elenen = [], Counter()
    for p in dosyalar:
        for r in jl(p):
            if not run_checks(r)["passed"]:
                elenen["run_checks"] += 1
            elif r["gen_meta"].get("seed_id") in dislanan:
                elenen["eval tohumu"] += 1
            elif r["messages"][-1]["role"] != "assistant" or not r["messages"][-1]["content"].strip():
                elenen["son tur asistan değil / boş"] += 1
            else:
                havuz.append((p.name, r))

    katman = defaultdict(list)
    for ad, r in havuz:
        katman[(r["turn_type"], r["gen_meta"].get("bicim"))].append((ad, r))
    rng = random.Random(TOHUM)
    kota = {k: round(N * len(v) / len(havuz)) for k, v in katman.items()}
    fark = N - sum(kota.values())                     # yuvarlama artığı en büyük katmana
    kota[max(katman, key=lambda k: len(katman[k]))] += fark
    secilen = [x for k in sorted(katman) for x in rng.sample(katman[k], kota[k])]

    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    with CIKTI.open("w", encoding="utf-8") as f:
        for ad, r in secilen:
            f.write(json.dumps({
                "id": r["id"], "turn_type": r["turn_type"], "bicim": r["gen_meta"].get("bicim"),
                "addiction_type": r["addiction_type"], "scenario": r["scenario"],
                "seed_id": r["gen_meta"].get("seed_id"), "kaynak_dosya": ad,
                # Notebook'la aynı biçim: yalnız rol + içerik; önceki asistan turlarında düşünce yok
                "messages": [{"role": m["role"], "content": m["content"]} for m in r["messages"][:-1]],
                "referans": r["messages"][-1]["content"],
            }, ensure_ascii=False) + "\n")

    L = ["# Referanslı test seti — ölçek-5k'dan 200 kayıt (BLEU/ROUGE için)", "",
         f"- Betik: `scripts/analiz/{Path(__file__).name}` · tarih 2026-10-20 · tohum {TOHUM}",
         f"- Girdi: `{KAYIT.relative_to(KOK)}/` — {len(dosyalar)} parça dosyası, aşama dağılımı {dict(asama)} "
         "(⚠️ koşu sürerken alındı; C = Sonnet denetiminden geçmiş, B = geçmemiş)",
         f"- Çıktı: `{CIKTI.relative_to(KOK)}` `{sha16(CIKTI)}` — **{len(secilen)}** kayıt", "",
         "## Havuz", "",
         f"- Uygun kayıt: {len(havuz)} · elenen: {dict(elenen)}",
         f"- Eval setlerinden dışlanan tohum sayısı: {len(dislanan)}", "",
         "## Bileşim", "", "| katman (tur · biçim) | havuz | seçilen |", "|---|---:|---:|"]
    L += [f"| {t} · {b} | {len(katman[(t, b)])} | {kota[(t, b)]} |" for t, b in sorted(katman)]
    L += ["", "| bağımlılık türü | seçilen |", "|---|---:|"]
    L += [f"| {k} | {n} |" for k, n in Counter(r["addiction_type"] for _, r in secilen).most_common()]
    L += ["", "## Sınırlar", "",
          "- Tohumlar eğitim verisiyle ortak (ölçek-5k'nın bütün satırları daha önce kullanılmış tohumlardan); kullanıcı metni ve referans yeni.",
          "- Referans başka bir modelin (Haiku) cevabı: BLEU/ROUGE «bu referansa sözcük benzerliği»ni ölçer, terapötik kaliteyi değil. "
          "Aynı duruma birçok doğru cevap verilebildiği için serbest diyalogda düşük skor beklenir (K9).", ""]
    RAPOR.write_text("\n".join(L), encoding="utf-8")
    print(f"yazıldı: {CIKTI.relative_to(KOK)} · {RAPOR.relative_to(KOK)}")


if __name__ == "__main__":
    main()
