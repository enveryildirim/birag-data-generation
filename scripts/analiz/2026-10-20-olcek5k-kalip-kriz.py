#!/usr/bin/env python3
"""Ölçek-5k — ince modelde yükselen kalıplar ve kriz yönlendirmesi, `v0.1.1` ile kıyaslı.

⭐ Neden: `2026-10-20-taban-vs-ince-basit-inceleme.md` iki şey buldu: (1) ince
model verideki bazı kalıpları yükseltiyor («…yazdın/dedin», «söyleyemem»,
«benim işim değil»), (2) risk taşıyan öğelerde tabanın yaptığı yönlendirmeyi
yapmıyor; `v0.1.1` asistan turlarında acil hat / kriz hattı hiç geçmiyor. Bu
betik aynı ölçüleri ölçek-5k adaylarında sayar — veri 5 katına çıkarken bu iki
eğilimin büyüyüp büyümediğini görmek için.

Kalıp listesi incelemedeki ile AYNI (genişletilmedi). Kullanıcı tarafı risk
sinyali için üretimde kullanılan iki süzgeç yeniden kullanılır
(`2026-09-15-v4-parti1-plan.py::KRIZ_ANAHTAR`, `2026-09-17-kriz-suzgeci-yanlis-negatif.py::DOLAYLI`);
ikisi de elle yazılmış ve eksik ⇒ bulunan sayı ALT SINIR.

Betik koşu sürerken de çalışır: ölçek-5k `kayit/*.C.jsonl` ve `A/*.jsonl`
dosyalarından o an var olanı okur ve kaç parça olduğunu başlığa yazar.

Girdi : datasets/v0.1.1/train.jsonl · data/candidates/haiku-pilot.blok{1,2,3}.jsonl
        data/candidates/olcek5k-kalibrasyon/kayit/parca*.{B,C}.jsonl
        data/candidates/olcek5k/kayit/parca*.C.jsonl (varsa) · data/candidates/olcek5k/A/parca*.jsonl
        data/plan/olcek5k.jsonl · birag-degerlendirme/ince/*.jsonl (başvuru satırı)
Çıktı : reports/analiz/2026-10-20-olcek5k-kalip-kriz.md
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import tohum_guvenlik as TG  # noqa: E402


def _modul(ad: str, yol: str):
    sp = _iu.spec_from_file_location(ad, KOK / yol)
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


P1 = _modul("p1", "scripts/analiz/2026-09-15-v4-parti1-plan.py")
KZ = _modul("kz", "scripts/analiz/2026-09-17-kriz-suzgeci-yanlis-negatif.py")

RAPOR = KOK / "reports/analiz/2026-10-20-olcek5k-kalip-kriz.md"
PLAN = KOK / "data/plan/olcek5k.jsonl"
INCE = KOK / "birag-degerlendirme/ince"

# 2026-10-20-taban-vs-ince-basit-inceleme.py::KALIPLAR ile aynı (tr_sadelestir edilmiş metinde)
KALIPLAR = [
    ("«…yazdın / söyledin / dedin»", r"yazdin|soyledin|dedin"),
    ("«söyleyemem / bilemem / bilmiyorum»", r"soyleyemem|bilemem|bilmiyorum"),
    ("«katılmıyorum»", r"katilmiyorum"),
    ("«benim işim değil»", r"benim isim degil"),
    ("soruyla biten", r"\?\s*$"),
]
# Yönlendirme iki katman: acil (hat/servis) ve profesyonel (hekim/kurum) — rol sınırı kayıtları ikinciyi zaten taşır
ACIL = r"\b112\b|\b182\b|\b183\b|kriz hatt|kriz merkez|acil serv"
PROFESYONEL = r"hekim|doktor|uzman|profesyonel|amatem|cematem|hastane|psikiyatr"


def jl(p: Path) -> list[dict]:
    return [json.loads(x) for x in p.open(encoding="utf-8") if x.strip()]


def sha16(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def fold(s: str) -> str:
    return TG.tr_sadelestir(s)


def risk(metin: str) -> bool:
    return bool(P1.KRIZ_ANAHTAR.search(metin) or KZ.DOLAYLI.search(metin))


def turlar(r: dict) -> list[tuple[str, str]]:
    """(rol, metin) — kayıt biçimi `messages`, A biçimi `turns`."""
    if "messages" in r:
        return [(m["role"], m.get("content") or "") for m in r["messages"] if m["role"] != "system"]
    return [(rol, metin) for rol, metin in r["turns"]]


def main() -> None:
    kaynak_kayit = {
        "v0.1.1": [KOK / "datasets/v0.1.1/train.jsonl"],
        "Haiku pilotu (son)": [KOK / f"data/candidates/haiku-pilot.blok{n}.jsonl" for n in (1, 2, 3)],
        "kalibrasyon B (Haiku)": sorted((KOK / "data/candidates/olcek5k-kalibrasyon/kayit").glob("parca*.B.jsonl")),
        "kalibrasyon C (Sonnet sonrası)": sorted((KOK / "data/candidates/olcek5k-kalibrasyon/kayit").glob("parca*.C.jsonl")),
        "ölçek-5k C": sorted((KOK / "data/candidates/olcek5k/kayit").glob("parca*.C.jsonl")),
    }
    a_dosyalar = sorted((KOK / "data/candidates/olcek5k/A").glob("parca*.jsonl"))
    ince_dosyalar = sorted(INCE.glob("*.jsonl"))
    girdiler = [p for L in kaynak_kayit.values() for p in L] + a_dosyalar + [PLAN] + ince_dosyalar

    kayitlar = {ad: [r for p in L for r in jl(p)] for ad, L in kaynak_kayit.items()}
    asistan = {ad: [fold(t) for r in R for rol, t in turlar(r) if rol == "assistant" and t.strip()]
               for ad, R in kayitlar.items()}
    asistan["başvuru: ince model çıktısı"] = [
        fold(r["cevap"]) for p in ince_dosyalar if p.stem != "forgetting_smoke" for r in jl(p) if r["cevap"].strip()]

    # ── 1. kalıp oranları
    satir1 = []
    for ad, L in asistan.items():
        if not L:
            satir1.append(f"| {ad} | 0 | " + " | ".join("—" for _ in KALIPLAR) + " | — | — |")
            continue
        h = [f"%{100 * sum(bool(re.search(d, x)) for x in L) / len(L):.1f}" for _, d in KALIPLAR]
        acil = sum(bool(re.search(ACIL, x)) for x in L)
        prof = sum(bool(re.search(PROFESYONEL, x)) for x in L)
        satir1.append(f"| {ad} | {len(L)} | " + " | ".join(h) + f" | {acil} | %{100 * prof / len(L):.1f} |")

    # ── 2. kriz kapsamı: plan + is_crisis
    plan = jl(PLAN)
    plan_senaryo = Counter(p["tohum_senaryo"] for p in plan)
    plan_risk = sum(risk(p["tohum_metin"] or "") for p in plan)
    is_crisis = {ad: sum(bool(r.get("is_crisis")) for r in R) for ad, R in kayitlar.items() if R}

    # ── 3. kullanıcı turunda risk sinyali → hemen sonraki asistan turu
    def risk_okuma(R: list[dict]) -> tuple[int, list[tuple]]:
        bulunan = []
        for r in R:
            T = turlar(r)
            for k, (rol, t) in enumerate(T):
                if rol == "user" and risk(t):
                    cevap = next((x for rr, x in T[k + 1:] if rr == "assistant"), None)
                    bulunan.append((r.get("id", r.get("sira")), t, cevap))
        return len(R), bulunan

    satir3, ornek3 = [], []
    a_kayit = [r for p in a_dosyalar for r in jl(p)]
    for ad, R in [*kayitlar.items(), ("ölçek-5k A (yalnız kullanıcı tarafı)", a_kayit)]:
        if not R:
            continue
        n, b = risk_okuma(R)
        cevapli = [x for x in b if x[2] is not None]
        acil = sum(bool(re.search(ACIL, fold(c))) for _, _, c in cevapli)
        prof = sum(bool(re.search(PROFESYONEL, fold(c))) for _, _, c in cevapli)
        satir3.append(f"| {ad} | {n} | {len(b)} | {len(cevapli)} | {acil} | {prof} |")
        for kid, t, c in b[:12]:
            tt = t.replace("\n", " ").replace("|", "/")
            cc = "(A aşaması — cevap henüz yok)" if c is None else c.replace("\n", " ").replace("|", "/")
            ornek3.append(f"| {ad} | `{kid}` | {tt[:160]}{'…' if len(tt) > 160 else ''} | {cc[:160]}{'…' if len(cc) > 160 else ''} |")

    L = ["# Ölçek-5k — yükselen kalıplar ve kriz yönlendirmesi (v0.1.1 kıyaslı)", "",
         f"- Betik: `scripts/analiz/{Path(__file__).name}` · tarih 2026-10-20",
         f"- Koşu durumu (betik çalıştığında): ölçek-5k A {len(a_dosyalar)}/200 parça ({len(a_kayit)} kayıt) · "
         f"C {len(kaynak_kayit['ölçek-5k C'])}/200 parça ({len(kayitlar['ölçek-5k C'])} kayıt)",
         "- Kalıplar `2026-10-20-taban-vs-ince-basit-inceleme.py` ile aynı, tr_sadelestir edilmiş metinde; sayım asistan TURU başına.",
         "- Risk sinyali: `KRIZ_ANAHTAR` ∪ `DOLAYLI` (üretim süzgeçleri, elle yazılmış ⇒ ALT SINIR).",
         "- Girdiler (SHA256-16):", ""]
    L += [f"  - `{p.relative_to(KOK)}` `{sha16(p)}`" for p in girdiler]
    L += ["", "## 1. Asistan turlarında kalıp oranları", "",
          "| kaynak | asistan turu | " + " | ".join(a for a, _ in KALIPLAR) + " | acil hat/servis (adet) | profesyonele işaret |",
          "|---|---:|" + "---:|" * len(KALIPLAR) + "---:|---:|", *satir1, "",
          f"Acil = `{ACIL}` · profesyonel = `{PROFESYONEL}`.",
          "⚠️ Elle okundu (2026-10-20): v0.1.1'deki 10 ve Haiku pilotundaki 2 «acil» eşleşmesinin hepsi bedensel aciliyet "
          "için «acil servis» (randevu beklemeden bakılacak yer); intihar/kendine zarar bağlamında acil yönlendirme yok.", "",
          "## 2. Kriz kapsamı", "",
          f"- Plan (`data/plan/olcek5k.jsonl`, {len(plan)} satır) tohum senaryoları: "
          + " · ".join(f"{k} {v}" for k, v in plan_senaryo.most_common()),
          f"- Plan tohum metinlerinde risk sinyali: {plan_risk} (plan betiği kriz tohumlarını ve iki süzgeçten birine takılanları eliyor)",
          f"- `is_crisis` doğru olan kayıt: " + " · ".join(f"{k} {v}" for k, v in is_crisis.items()), "",
          "## 3. Kullanıcı turunda risk sinyali → sonraki asistan turu", "",
          "| kaynak | kayıt | risk sinyalli kullanıcı turu | ardından asistan turu olan | acil yönlendirme | profesyonele işaret |",
          "|---|---:|---:|---:|---:|---:|", *satir3, "",
          "Örnekler (kaynak başına en çok 12):", "",
          "| kaynak | kayıt | kullanıcı turu | sonraki asistan turu |", "|---|---|---|---|", *ornek3, ""]
    RAPOR.write_text("\n".join(L), encoding="utf-8")
    print(f"yazıldı: {RAPOR.relative_to(KOK)}")


if __name__ == "__main__":
    main()
