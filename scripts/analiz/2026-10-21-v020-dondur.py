#!/usr/bin/env python3
"""`datasets/v0.2.0`'ı dondurur — ölçek-5k (K279) adaylarından, dışlamalarla.

Girdi : data/candidates/olcek5k.jsonl · data/plan/olcek5k.jsonl · evals/*.jsonl ·
        data/plan/elenen-tohumlar.jsonl · data/eval-ref/olcek5k-ref.v1.jsonl
Çıktı : datasets/v0.2.0/{train.jsonl,manifest.json,CARD.md} · reports/analiz/2026-10-21-v020-dondur.md

Dışlama sırası (bir kayıt İLK tutan sebeple sayılır):
  1. `sizinti_supheli`    — tohum sızıntısı şüphesi C'den sonra da kaldı (👤 2026-10-21: «131 şüpheliyi çıkar»)
  2. `eval_tohumu`        — kaydın tohumu bir eval öğesinin `kaynak.seed_id`'si (K91 bölmesi, K31 mühür)
  3. `eval_metni`         — tohum ya da kullanıcı turu bir eval kullanıcı mesajıyla iki yönlü 60 karakter
                            önekle çakışıyor (K111: `kaynak.tip: elle` öğeler seed_id taşımaz)
  4. `elenen_tohum`       — `data/plan/elenen-tohumlar.jsonl` kalıcı eleme defteri (Kural 3)
  5. `eval_ref`           — BLEU/ROUGE referans setinin kaydı ya da aynı ilk kullanıcı mesajı

⛔ 2-4 ölçek-5k planında (`2026-10-20-olcek5k-plan.py`) UYGULANMAMIŞTI — benim kusurum; önceki
partilerin hepsi uyguluyordu. Bu betik onu donmadan önce kapatır. `datasets/v0.2.0` varsa DURUR.

Kullanım: uv run python scripts/analiz/2026-10-21-v020-dondur.py
"""
from __future__ import annotations

import collections
import glob
import hashlib
import json
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from checks import run_checks  # noqa: E402
import tohum_guvenlik as TG  # noqa: E402

ADAY = KOK / "data/candidates/olcek5k.jsonl"
PLAN = KOK / "data/plan/olcek5k.jsonl"
ELEME = KOK / "data/plan/elenen-tohumlar.jsonl"
REF = KOK / "data/eval-ref/olcek5k-ref.v1.jsonl"
V011 = KOK / "datasets/v0.1.1/train.jsonl"
HEDEF = KOK / "datasets/v0.2.0"
RAPOR = KOK / "reports/analiz/2026-10-21-v020-dondur.md"
EVAL_MIN_KARAKTER = 40   # v4-parti1-plan ile aynı eşik (iki harflik turlar havuzu çökertiyordu)


def _sha16(y: Path) -> str:
    return hashlib.sha256(y.read_bytes()).hexdigest()[:16]


def _jl(p: Path) -> list[dict]:
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def _eval() -> tuple[set[str], list[str], list[str]]:
    tohum, metin, dosya = set(), [], []
    for p in sorted(glob.glob(str(KOK / "evals/*.jsonl"))):
        dosya.append(Path(p).name)
        for o in _jl(Path(p)):
            if isinstance(o.get("kaynak"), dict) and o["kaynak"].get("seed_id"):
                tohum.add(o["kaynak"]["seed_id"])
            metin += [TG.tr_fold(m["content"]).strip() for m in o.get("messages", []) if m.get("role") == "user"]
    return tohum, [m for m in metin if len(m) >= EVAL_MIN_KARAKTER], dosya


def main() -> int:
    if HEDEF.exists():
        raise SystemExit(f"⛔ {HEDEF.relative_to(KOK)} zaten var — IMMUTABLE, üzerine yazılmaz")
    aday = _jl(ADAY)
    plan = {hashlib.sha256(f"olcek5k-{r['sira']}".encode()).hexdigest()[:24]: r for r in _jl(PLAN)}
    ev_tohum, ev_metin, ev_dosya = _eval()
    elenen = {d["seed_id"] for d in _jl(ELEME)} if ELEME.exists() else set()
    ref = _jl(REF)
    ref_id = {r["id"] for r in ref}
    ref_user = {r["messages"][1]["content"] for r in ref}
    ref_tohum = {r["seed_id"] for r in ref}

    def carpisir(t: str) -> bool:
        d = TG.tr_fold(t).strip()
        return len(d) >= EVAL_MIN_KARAKTER and any(e[:60] in d or d[:60] in e for e in ev_metin)

    def sebep(r: dict) -> str | None:
        g, p = r["gen_meta"], plan[r["id"]]
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
    kalan = []
    for r in aday:
        s = sebep(r)
        say[s or "kaldi"] += 1
        if s is None:
            kalan.append(r)
    assert all(run_checks(r)["passed"] for r in kalan)
    v011_id = {r["id"] for r in _jl(V011)}
    assert not (v011_id & {r["id"] for r in kalan}), "v0.1.1 ile id çakışması"
    kardes = sum(1 for r in kalan if r["gen_meta"].get("seed_id") in ref_tohum)

    HEDEF.mkdir(parents=True)
    cikti = HEDEF / "train.jsonl"
    cikti.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kalan), encoding="utf-8")
    sayac = lambda f: dict(collections.Counter(f(r) for r in kalan).most_common())
    cmodel = lambda r: r["gen_meta"]["generator_model"].split("C: ")[1]
    rev = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=KOK, capture_output=True, text=True).stdout.strip()
    manifest = {
        "version": "v0.2.0", "date": "2026-10-21", "git_rev": rev, "karar": "K279 (+ K281 dondurma)",
        "input_file": str(ADAY.relative_to(KOK)), "input_sha256_16": _sha16(ADAY),
        "plan_file": str(PLAN.relative_to(KOK)), "plan_sha256_16": _sha16(PLAN),
        "eval_ref": str(REF.relative_to(KOK)), "eval_ref_sha256_16": _sha16(REF),
        "eleme_defteri_sha256_16": _sha16(ELEME) if ELEME.exists() else None,
        "eval_dosyalari": ev_dosya, "eval_tohum_sayisi": len(ev_tohum),
        "build_script": "scripts/analiz/2026-10-20-olcek5k-toplu.py",
        "freeze_script": f"scripts/analiz/{Path(__file__).name}",
        "output_sha256_16": _sha16(cikti),
        "n_aday": len(aday), "n_total": len(kalan), "dislama": {k: v for k, v in say.items() if k != "kaldi"},
        "n_eval_ref_kardes_tohum": kardes,
        "v011_ile_birlesik": False,
        "c_model_counts": sayac(cmodel), "c_karar_counts": sayac(lambda r: r["gen_meta"].get("c_karar")),
        "addiction_type_counts": sayac(lambda r: r["addiction_type"]), "age_group_counts": sayac(lambda r: r["age_group"]),
        "slice_counts": sayac(lambda r: r["slice"]), "turn_type_counts": sayac(lambda r: r["turn_type"]),
        "sinir_tipi_counts": sayac(lambda r: r["gen_meta"]["sinir_tipi"]),
        "turn_ending_counts": sayac(lambda r: r["gen_meta"]["turn_ending"]),
    }
    (HEDEF / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    d = manifest["dislama"]
    tablo = lambda c: " · ".join(f"{k} {v}" for k, v in c.items())
    kart = f"""# BıRAG veri kümesi — v0.2.0

**Tarih:** 2026-10-21 · **Kaynak:** ölçek-5k (K279), `{manifest['input_file']}` `{manifest['input_sha256_16']}`
**Çıktı:** `train.jsonl` SHA256-16 **`{manifest['output_sha256_16']}`** · **{len(kalan)} kayıt**
**Durum:** ⭐ araştırma sürümü · ⛔ `v0.1.1` ile **birleşik DEĞİL** (yalnız ölçek-5k kayıtları; birlikte eğitilecekse iki dosya ayrıca birleştirilir) · ⛔ kriz dilimi hariç (tasarım gereği)

## 1. Nasıl üretildi

Üç aşama, kayıt başına: **A** (Haiku) tohumdan kullanıcı tarafı · **B** (Haiku) son cevap + thinking, **tohumu görmeden** · **C** hata avı — düzelt / düşür (K43: puan değil). Mekanik kapılar her aşamada (`scripts/analiz/2026-10-20-olcek5k-arac.py`). Briefler `prompts/olcek5k-{{A,B,C}}.v1.md`.

| C modeli | kayıt |
|---|---:|
""" + "\n".join(f"| {k} | {v} |" for k, v in manifest["c_model_counts"].items()) + f"""

C kararları: {tablo(manifest['c_karar_counts'])}. Düzeltme+düşürme oranı Sonnet'te %62,5, Haiku'da %28,3 — **Haiku kusurların bir kısmını kaçırıyor** (`reports/analiz/2026-10-20-olcek5k-sonuc.md`).

## 2. Dışlananlar ({len(aday)} aday → {len(kalan)})

| sebep | kayıt |
|---|---:|
| tohum sızıntısı şüphesi (`gen_meta.sizinti_supheli`) | {d.get('sizinti_supheli', 0)} |
| eval tohumu (`evals/*` `kaynak.seed_id`) | {d.get('eval_tohumu', 0)} |
| eval metni çakışması (60 karakter önek) | {d.get('eval_metni', 0)} |
| kalıcı eleme defteri | {d.get('elenen_tohum', 0)} |
| BLEU/ROUGE referans seti (`olcek5k-ref.v1`) | {d.get('eval_ref', 0)} |

⛔ Eval dışlamaları ölçek-5k planında uygulanmamıştı (önceki partilerin hepsinde vardı); donmadan önce bu betikle kapatıldı.

## 3. Dağılım

| alan | dağılım |
|---|---|
| tür | {tablo(manifest['addiction_type_counts'])} |
| yaş | {tablo(manifest['age_group_counts'])} |
| dilim | {tablo(manifest['slice_counts'])} |
| tur | {tablo(manifest['turn_type_counts'])} |
| sınır tipi | {tablo(manifest['sinir_tipi_counts'])} |
| bitiş | {tablo(manifest['turn_ending_counts'])} |

## 4. ⛔ Bilinen kusurlar ve açık maddeler

| | |
|---|---|
| ⛔⛔ **Kayıt kayıt okunmadı** | K260 bu üretim için askıda (K279). Örneklem okuması 20 kayıt: Haiku-C 14'te 2 ciddi + 2 küçük, Sonnet-C 6'da 0 ciddi + 1 küçük (`reports/analiz/2026-10-21-olcek5k-okuma.md`) |
| ⛔ **Açılış sızıntısı** | çok turlu kayıtların ~%1-2'sinde asistan açılışı ikinci kullanıcı mesajındaki bir ayrıntıyı anıyor (kaba tarama, kapı değil) |
| ⛔ **Tohumlar yeniden kullanıldı** | 5000 satırın tamamı `v0.1.1` / eski partilerde kullanılmış tohumlardan (2153 tohum × 2-3); kullanıcı metni yeni, senaryo tohumu ortak |
| ⚠️ **BLEU referans seti kardeşleri** | referans setinin tohumlarından üretilmiş {kardes} kayıt eğitimde kaldı (aynı kayıt / aynı ilk mesaj çıkarıldı). Referans set zaten tohumu `v0.1.1` ile paylaşıyor (`2026-10-20-rapor-referans-seti.py` sınırları) |
| ⚠️ **`sinir_tipi` normalleştirildi** | B'nin güvenlik sapmasında yazdığı serbest etiketler korpus sözlüğüne bağlandı; özgün etiket `gen_meta.sinir_tipi_b` |
| ⛔ **Jeton uzunluğu doğrulanmadı** | bu makinede tokenizer yok; eğitim ortamında ≤ 2048 denetlenmeli |
| ⚠️ **Yazarlık** | *Haiku taslakladı (A, B), Sonnet (parça 1-13) / Haiku (14-200) hata avı yaptı, Claude Code tasarladı ve örnekledi* |
| ⛔ **Kriz dilimi yok** | tasarım gereği; T311'in gerilemesini (kriz/yönlendirme) bu sürüm onaramaz |
"""
    (HEDEF / "CARD.md").write_text(kart, encoding="utf-8")

    sat = ["# v0.2.0 dondurma\n", f"- Betik: `scripts/analiz/{Path(__file__).name}` · tarih 2026-10-21 · git `{rev}`",
           f"- Girdi: `{manifest['input_file']}` `{manifest['input_sha256_16']}` · plan `{manifest['plan_sha256_16']}` · "
           f"eval-ref `{manifest['eval_ref_sha256_16']}` · eval tohumu {len(ev_tohum)} ({len(ev_dosya)} dosya)",
           f"- Çıktı: `datasets/v0.2.0/train.jsonl` `{manifest['output_sha256_16']}` — **{len(kalan)} kayıt**\n",
           "| sebep | kayıt |", "|---|---:|"] + [f"| {k} | {v} |" for k, v in say.items()]
    sat.append(f"\nReferans seti tohumlarından kalan kardeş kayıt: {kardes}")
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat))
    return 0


if __name__ == "__main__":
    sys.exit(main())
