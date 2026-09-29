#!/usr/bin/env python3
"""`datasets/v0.1.1`'i dondurur — ön kaydın Faz 4 adım 1'i (K277).

Hazırlık dosyası (`data/candidates/v011-derleme.jsonl`) ön kayıttaki SHA ile **aynıysa**
bayt bayt kopyalanır; değilse DURUR. `datasets/v0.1.1` varsa DURUR (IMMUTABLE, Kural 4).

⛔ Ön kaydın adım 2'si (gerçek tokenizer ile ≤ 2048 jeton) BU MAKİNEDE yapılamaz: model ve
tokenizer yok (👤 2026-09-29: bu makine yalnız veri üretimi). Kartta açık madde olarak durur.

Kullanım: uv run python scripts/analiz/2026-09-29-v011-dondur.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
ONKAYIT = KOK / "configs/deney/2026-09-29-v011-on-kayit.json"
EK1 = KOK / "configs/deney/2026-09-29-v011-on-kayit-ek1.json"
HAZIRLIK = KOK / "data/candidates/v011-derleme.jsonl"
KAYNAK = KOK / "datasets/v0.1.0/train.jsonl"
HEDEF = KOK / "datasets/v0.1.1"
ORNEK_ID = "833a3c51bbbd1adc139c7201"


def _sha16(y: Path) -> str:
    return hashlib.sha256(y.read_bytes()).hexdigest()[:16]


def main() -> int:
    if HEDEF.exists():
        raise SystemExit(f"⛔ {HEDEF.relative_to(KOK)} zaten var — IMMUTABLE, üzerine yazılmaz")
    m = json.loads(ONKAYIT.read_text(encoding="utf-8"))
    beklenen = m["kollar"]["v011"]["hazirlik_sha256_16"]
    if _sha16(HAZIRLIK) != beklenen:
        raise SystemExit(f"⛔ hazırlık SHA'sı {_sha16(HAZIRLIK)} ≠ ön kayıttaki {beklenen} — DONDURULMADI")
    assert _sha16(KAYNAK) == "6fcb6b1e16290575"

    HEDEF.mkdir(parents=True)
    shutil.copyfile(HAZIRLIK, HEDEF / "train.jsonl")
    assert _sha16(HEDEF / "train.jsonl") == beklenen

    yeni = [json.loads(x) for x in (HEDEF / "train.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    eski = [json.loads(x) for x in KAYNAK.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert [r["id"] for r in yeni] == [r["id"] for r in eski]
    kuruldu = [r for r in yeni if "yeniden_kurma" in (r.get("gen_meta") or {})]
    eski_hal = [r["id"] for r in yeni if "yeniden_kurma" not in (r.get("gen_meta") or {}) and not r.get("replay")]
    son_degisen = sum(a["messages"][-1]["content"] != b["messages"][-1]["content"] for a, b in zip(eski, yeni))
    rev = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=KOK, capture_output=True, text=True).stdout.strip()
    say = lambda k: dict(collections.Counter(r.get(k) for r in yeni))

    manifest = {
        "version": "v0.1.1", "date": "2026-09-29", "git_rev": rev,
        "base_dataset": "datasets/v0.1.0/train.jsonl", "base_sha256_16": _sha16(KAYNAK),
        "input_file": str(HAZIRLIK.relative_to(KOK)), "input_sha256_16": _sha16(HAZIRLIK),
        "output_sha256_16": _sha16(HEDEF / "train.jsonl"),
        "build_script": "scripts/analiz/2026-09-29-v011-derleme.py",
        "on_kayit": {"ana": str(ONKAYIT.relative_to(KOK)), "ana_sha256_16": _sha16(ONKAYIT),
                     "ek1": str(EK1.relative_to(KOK)), "ek1_sha256_16": _sha16(EK1)},
        "n_total": len(yeni), "n_yeniden_kurulan": len(kuruldu), "n_son_cumle_degisen": son_degisen,
        "n_replay": sum(bool(r.get("replay")) for r in yeni),
        "v010_hali_kalan": {"ids": eski_hal, "neden": "3 red (korunum/temizlik) + uretim-v6 §1e örneği (denetlenmedi)"},
        "degisen_alanlar": "yalnız son asistan turu (thinking; 9 kayıtta content'in son cümlesi) ve gen_meta",
        "scenario_counts": say("scenario"), "addiction_type_counts": say("addiction_type"), "age_group_counts": say("age_group"),
    }
    (HEDEF / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    kart = f"""# BıRAG veri kümesi — v0.1.1

**Tarih:** 2026-09-29 · **Taban:** `datasets/v0.1.0/train.jsonl` SHA256-16 `{_sha16(KAYNAK)}`  
**Çıktı:** `train.jsonl` SHA256-16 **`{_sha16(HEDEF / 'train.jsonl')}`** (ön kayıttaki hazırlık SHA'sıyla aynı — betik denetler)  
**Kayıt:** **{len(yeni)}** — kayıt kümesi ve sırası `v0.1.0` ile **birebir** (K277: yeni kayıt yok, silme yok)  
**Durum:** ⭐ araştırma sürümü, **ana hat DEĞİL** — ana hat olup olmayacağına ön kayıt karar verir (K277 · EK-1) · ⛔ kriz dilimi hariç (`v0.1.0` gibi)

## 1. Ne değişti

| | kayıt |
|---|---:|
| düşünmesi yeniden kurulan (`uretim-v6`, kararlar korunarak) | **{len(kuruldu)}** |
| cevabının **son cümlesi** değişen | **{son_degisen}** |
| `v0.1.0` hâliyle kalan (3 red + §1e örneği) | {len(eski_hal)} |
| replay (düşünmesi yok, dokunulmadı) | {manifest['n_replay']} |

⛔ **Dokunulmayanlar:** kullanıcı turları, bağlam, önceki turlar, cevabın gövdesi, klinik kararlar, üstveri.

| veri düzeyi | `v0.1.0` | `v0.1.1` |
|---|---:|---:|
| son tur soruyla biten | %50,3 | %49,4 |
| düşünmede «sormuyorum» | %30,6 | %3,1 |
| düşünmede ⛔ ya da ⭐ | %22,8 | %0,2 |
| düşünme ortanca sözcük | 72 | 112 |

Kaynak: `reports/analiz/2026-09-29-v011-derleme.md` · süreç: `reports/analiz/2026-09-24-v011-faz2.md`

## 2. Güvenceler

- Her yeniden kurma: zarf · temizlik · `run_checks` · karar eşlemesi · bağımsız karar korunumu okuması (1143 okuma `karar-korunumu.v1`, 4 okuma `v2`) · bitişi değişende eski↔yeni aynı judge.
- Ön kayıt: `configs/deney/2026-09-29-v011-on-kayit.json` (`{_sha16(ONKAYIT)}`) + EK-1 kazanç şartı (`{_sha16(EK1)}`).

## 3. ⛔ Bilinen kusurlar ve açık maddeler

| | |
|---|---|
| ⛔⛔ **Jeton uzunluğu doğrulanmadı** | ön kaydın adım 2'si: hiçbir kayıt `max_seq_length` 2048'i aşmamalı. Bu makinede tokenizer yok; en uzun kayıt 3359 karakter (~1100 jeton **tahmini**). **Eğitimden önce eğitim ortamında gerçek tokenizer ile denetlenmeli** — sessiz kırpma kıyası bozar |
| ⛔ **`v0.1.0` kusurları taşınıyor** | `data/candidates/v011-v010-kusurlari.jsonl` — 47 madde (cevap katmanı, `iyi_giden_paylasim` etiketi 9 kayıtta yanlış, biri güvenlikle ilgili: 0802) |
| ⚠️ **Düşünme %56 uzadı** | gecikme KPI'ı (K46) etkilenir |
| ⚠️ **İki rubrik sürümü** | korunum okumalarının 4'ü `karar-korunumu.v2` ile (T302-T304) |
| ⚠️ **Yazarlık** | 1039 yeniden kurmanın 206 taslağı Claude Code'a ait; hepsinin okuma ve revizyonu Claude Code (K260) |
| 👤 **İnsan okuması** | pilotun 40 kaydı henüz insan tarafından okunmadı (K277'nin ikinci güvence katmanı) |
"""
    (HEDEF / "CARD.md").write_text(kart, encoding="utf-8")
    print(f"✅ {HEDEF.relative_to(KOK)} donduruldu · train.jsonl {_sha16(HEDEF / 'train.jsonl')} · {len(yeni)} kayıt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
