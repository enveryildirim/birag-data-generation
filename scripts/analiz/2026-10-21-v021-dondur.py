#!/usr/bin/env python3
"""`datasets/v0.2.1`'i dondurur — `v0.2.0` + ölçek-5k tamamlama partisi (parça 201-228).

👤 2026-10-21: *«650 kayıt daha üret, v0.2.1 olarak dondur»*.

`v0.2.0/train.jsonl` satırları BAYT BAYT aynen alınır (sıra korunur); ardından tamamlama
kayıtları (`data/candidates/olcek5k.jsonl` içinde plan sırası ≥ 5001) `v0.2.0`'ın dışlama
kurallarından geçirilip eklenir. Dışlama yardımcıları `2026-10-21-v020-dondur.py`'den içe
aktarılır; sebep sırası onunla aynıdır. Tamamlama planı eval/eleme/referans tohumlarını zaten
dışladı (`2026-10-21-olcek5k-ek-plan.py`) — burada yeniden sınanır, beklenen 0.

Girdi : datasets/v0.2.0/train.jsonl · data/candidates/olcek5k.jsonl · data/plan/olcek5k-ek.jsonl
Çıktı : datasets/v0.2.1/{train.jsonl,manifest.json,CARD.md} · reports/analiz/2026-10-21-v021-dondur.md
`datasets/v0.2.1` varsa DURUR.
"""
from __future__ import annotations

import collections
import hashlib
import json
import subprocess
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
_sp = _iu.spec_from_file_location("don", KOK / "scripts/analiz/2026-10-21-v020-dondur.py")
DON = _iu.module_from_spec(_sp)
_sp.loader.exec_module(DON)

TABAN = KOK / "datasets/v0.2.0/train.jsonl"
ADAY = KOK / "data/candidates/olcek5k.jsonl"
PLAN_EK = KOK / "data/plan/olcek5k-ek.jsonl"
HEDEF = KOK / "datasets/v0.2.1"
RAPOR = KOK / "reports/analiz/2026-10-21-v021-dondur.md"
TABAN_SHA = "eabc85f7b97c96c1"


def main() -> int:
    if HEDEF.exists():
        raise SystemExit(f"⛔ {HEDEF.relative_to(KOK)} zaten var — IMMUTABLE, üzerine yazılmaz")
    assert DON._sha16(TABAN) == TABAN_SHA, "v0.2.0 değişmiş"
    taban_sat = [x for x in TABAN.read_text(encoding="utf-8").splitlines() if x.strip()]
    taban_id = {json.loads(x)["id"] for x in taban_sat}

    ek_plan = {hashlib.sha256(f"olcek5k-{r['sira']}".encode()).hexdigest()[:24]: r for r in DON._jl(PLAN_EK)}
    aday = [r for r in DON._jl(ADAY) if r["id"] in ek_plan]
    eksik_parca = sorted({p["parca"] for p in ek_plan.values()}
                         - {ek_plan[r["id"]]["parca"] for r in aday})
    ev_tohum, ev_metin, ev_dosya = DON._eval()
    elenen = {d["seed_id"] for d in DON._jl(DON.ELEME)}
    ref = DON._jl(DON.REF)
    ref_id, ref_user = {r["id"] for r in ref}, {r["messages"][1]["content"] for r in ref}

    def carpisir(t: str) -> bool:
        d = DON.TG.tr_fold(t).strip()
        return len(d) >= DON.EVAL_MIN_KARAKTER and any(e[:60] in d or d[:60] in e for e in ev_metin)

    def sebep(r: dict) -> str | None:   # v0.2.0 ile aynı sıra
        g, p = r["gen_meta"], ek_plan[r["id"]]
        if g.get("sizinti_supheli"):
            return "sizinti_supheli"
        if g.get("seed_id") in ev_tohum or p.get("source_id") in ev_tohum:
            return "eval_tohumu"
        if carpisir(p["tohum_metin"]) or any(carpisir(m["content"]) for m in r["messages"] if m["role"] == "user"):
            return "eval_metni"
        if g.get("seed_id") in elenen or p.get("source_id") in elenen:
            return "elenen_tohum"
        if r["id"] in ref_id or r["messages"][1]["content"] in ref_user:
            return "eval_ref"
        return None

    say = collections.Counter()
    yeni = []
    for r in aday:
        s = sebep(r)
        say[s or "kaldi"] += 1
        if s is None:
            yeni.append(r)
    assert all(DON.run_checks(r)["passed"] for r in yeni)
    assert not taban_id & {r["id"] for r in yeni}
    plan_say = len(ek_plan)
    c_dusen = plan_say - len(aday)

    HEDEF.mkdir(parents=True)
    cikti = HEDEF / "train.jsonl"
    cikti.write_text("".join(x + "\n" for x in taban_sat)
                     + "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in yeni), encoding="utf-8")
    hepsi = DON._jl(cikti)
    assert [json.dumps(r, ensure_ascii=False) for r in hepsi[:len(taban_sat)]] == taban_sat
    sayac = lambda xs, f: dict(collections.Counter(f(r) for r in xs).most_common())
    rev = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=KOK, capture_output=True, text=True).stdout.strip()
    manifest = {
        "version": "v0.2.1", "date": "2026-10-21", "git_rev": rev, "karar": "K279 · K281 · K282",
        "base_dataset": str(TABAN.relative_to(KOK)), "base_sha256_16": TABAN_SHA, "n_base": len(taban_sat),
        "input_file": str(ADAY.relative_to(KOK)), "input_sha256_16": DON._sha16(ADAY),
        "plan_ek": str(PLAN_EK.relative_to(KOK)), "plan_ek_sha256_16": DON._sha16(PLAN_EK),
        "plan_script": "scripts/analiz/2026-10-21-olcek5k-ek-plan.py",
        "freeze_script": f"scripts/analiz/{Path(__file__).name}",
        "output_sha256_16": DON._sha16(cikti),
        "n_ek_plan": plan_say, "n_ek_c_dusen_ya_da_eksik": c_dusen, "eksik_parca": eksik_parca,
        "n_ek": len(yeni), "n_total": len(hepsi),
        "ek_dislama": {k: v for k, v in say.items() if k != "kaldi"},
        "v011_ile_birlesik": False,
        "ek_c_karar_counts": sayac(yeni, lambda r: r["gen_meta"].get("c_karar")),
        "c_model_counts": sayac(hepsi, lambda r: r["gen_meta"]["generator_model"].split("C: ")[1]),
        "addiction_type_counts": sayac(hepsi, lambda r: r["addiction_type"]),
        "age_group_counts": sayac(hepsi, lambda r: r["age_group"]),
        "slice_counts": sayac(hepsi, lambda r: r["slice"]),
        "turn_type_counts": sayac(hepsi, lambda r: r["turn_type"]),
        "sinir_tipi_counts": sayac(hepsi, lambda r: r["gen_meta"]["sinir_tipi"]),
        "turn_ending_counts": sayac(hepsi, lambda r: r["gen_meta"]["turn_ending"]),
    }
    (HEDEF / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    tablo = lambda c: " · ".join(f"{k} {v}" for k, v in c.items())
    kart = f"""# BıRAG veri kümesi — v0.2.1

**Tarih:** 2026-10-21 · **Taban:** `datasets/v0.2.0/train.jsonl` `{TABAN_SHA}` ({len(taban_sat)} kayıt, bayt bayt aynen, sıra korunur)
**Çıktı:** `train.jsonl` SHA256-16 **`{manifest['output_sha256_16']}`** · **{len(hepsi)} kayıt** (= {len(taban_sat)} + {len(yeni)} tamamlama)
**Durum:** ⭐ araştırma sürümü · ⛔ `v0.1.1` ile **birleşik DEĞİL** · ⛔ kriz dilimi hariç (tasarım gereği)

## 1. Tamamlama partisi

`v0.2.0`'ı 5000'e yaklaştırmak için {plan_say} satırlık ızgara (`{manifest['plan_ek']}` `{manifest['plan_ek_sha256_16']}`, parça 201-{max(p['parca'] for p in ek_plan.values())}). Üretim `v0.2.0` ile aynı: A (Haiku) → B (Haiku, tohumsuz) → C (Haiku, hata avı). Fark: eval tohumu, eval metni, kalıcı eleme defteri ve BLEU referans seti tohumları **planda** dışlandı (K281 dersi).

| | kayıt |
|---|---:|
| planlanan | {plan_say} |
| C düşürdü / birleştirmeye girmedi | {c_dusen} |
| dışlandı (sızıntı şüphesi vb.) | {sum(v for k, v in say.items() if k != 'kaldi')} — {tablo(manifest['ek_dislama']) or '—'} |
| **eklendi** | **{len(yeni)}** |

Tamamlama C kararları: {tablo(manifest['ek_c_karar_counts'])}.

## 2. Dağılım (bütün sürüm)

| alan | dağılım |
|---|---|
| C modeli | {tablo(manifest['c_model_counts'])} |
| tür | {tablo(manifest['addiction_type_counts'])} |
| yaş | {tablo(manifest['age_group_counts'])} |
| dilim | {tablo(manifest['slice_counts'])} |
| tur | {tablo(manifest['turn_type_counts'])} |
| sınır tipi | {tablo(manifest['sinir_tipi_counts'])} |
| bitiş | {tablo(manifest['turn_ending_counts'])} |

## 3. ⛔ Bilinen kusurlar

`datasets/v0.2.0/CARD.md` §4'tekilerin hepsi geçerli (kayıt kayıt okunmadı, Haiku-C kaçırma payı, açılış sızıntısı ~%1-2, tohumlar yeniden kullanıldı, jeton uzunluğu doğrulanmadı, kriz dilimi yok). Ek: tamamlama partisinin tohumları ölçek-5k'da zaten 2 kez kullanılmıştı ⇒ bu 700 tohum artık **3×**.
"""
    (HEDEF / "CARD.md").write_text(kart, encoding="utf-8")
    sat = ["# v0.2.1 dondurma\n", f"- Betik: `scripts/analiz/{Path(__file__).name}` · tarih 2026-10-21 · git `{rev}`",
           f"- Girdi: taban `{TABAN_SHA}` · aday `{manifest['input_sha256_16']}` · plan-ek `{manifest['plan_ek_sha256_16']}`",
           f"- Çıktı: `datasets/v0.2.1/train.jsonl` `{manifest['output_sha256_16']}` — **{len(hepsi)} kayıt** "
           f"({len(taban_sat)} + {len(yeni)})\n",
           f"- Tamamlama: plan {plan_say} · C düşürdü/eksik {c_dusen} · eksik parça {eksik_parca or 'yok'}",
           "", "| sebep | kayıt |", "|---|---:|"] + [f"| {k} | {v} |" for k, v in say.items()]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat))
    return 0


if __name__ == "__main__":
    sys.exit(main())
