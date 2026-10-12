#!/usr/bin/env python3
"""Taban ↔ ince ayar ön kaydına EK-2: T1 = Hugging Face'teki birleştirilmiş model (2026-10-12).

Neden: ön kayıt T1'i «aynı yüklü tabana PeftModel ile takılan LoRA adapter» diye tanımlıyordu. Kullanıcı ince
ayarlı modeli `yildirim34/birag-gemma4-26b` olarak paylaştı ve depoda adapter YOK: LoRA tabana birleştirilmiş,
bf16 (`model-0000{1,2}-of-00002.safetensors`, 51,6 GB) + GGUF'lar. Dağıtılacak olan da bu model ⇒ T1 bu olur.

Değişen: T1 ayrı yüklenir (T0 bellekten atılır; iki model 80 GB'a sığmaz). «Değişen tek şey adapter» artık
«değişen tek şey birleştirilmiş LoRA»dır; birleştirmenin bf16 yuvarlaması da farka dahildir.
Revizyon sabitlenir: depo sonradan güncellense de mühürlü sürüm kullanılır.
Hiçbir Colab çıktısı görülmedi. Setler, üretim ayarı, ölçüler ve karar kuralı DEĞİŞMEDİ.

Kullanım:  uv run python scripts/analiz/2026-10-12-taban-vs-ince-onkayit-ek2-yaz.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
ON_KAYIT = "configs/deney/2026-10-12-taban-vs-ince-on-kayit.json"
EK1 = "configs/deney/2026-10-12-taban-vs-ince-on-kayit-ek1.json"
DEFTER = "notebooks/taban-vs-ince-ayar-uretim.ipynb"
COZ = "scripts/analiz/2026-10-12-taban-vs-ince-cozumleme.py"
CIKTI = KOK / "configs/deney/2026-10-12-taban-vs-ince-on-kayit-ek2.json"


def sha16(p: str) -> str:
    return hashlib.sha256((KOK / p).read_bytes()).hexdigest()[:16]


def main() -> int:
    ek = {
        "tarih": "2026-10-12",
        "on_kayit": ON_KAYIT, "on_kayit_sha256_16": sha16(ON_KAYIT),
        "ek1": EK1, "ek1_sha256_16": sha16(EK1),
        "neden": "Kullanıcının ince ayarlı modeli HF'te birleştirilmiş bf16 model olarak duruyor; adapter yok. "
                 "T1 bu modeldir (dağıtılacak olan). Hiçbir Colab çıktısı görülmedi.",
        "t1": {
            "model": "yildirim34/birag-gemma4-26b",
            "revizyon": "2f4a8b48aa6c78e5bb685e0b1a1e5f5544afc0d3",
            "indirilecek": ["*.json", "*.safetensors", "*.jinja"],
            "gozlem_2026_10_12": "Gemma4ForConditionalGeneration · bf16 · 1013 tensör · 51,6 GB · LoRA anahtarı yok · "
                                 "chat_template.jinja resmi 26B şablonuyla bayt bayt aynı · README base_model "
                                 "unsloth/gemma-4-26b-a4b-it",
            "bilinmeyen": "eğitim tarifi ve verinin v0.1.1 olduğu kullanıcının beyanı; depoda kayıt yok",
        },
        "degisiklikler": [
            "T1 = birleştirilmiş model, ayrı yüklenir (PeftModel yok); T0 bellekten atılır",
            "ortam.json: adapter alanları yerine t1_model + t1_revizyon; sablon_sha256_16 eklendi",
            "çözümleme: T1 kimliği EK-2'deki model+revizyonla; iki kolda şablon SHA'sı aynı olmalı",
            "defter ve çözümleme yeniden mühürlendi (aşağıda); ön kayıttaki defter SHA'sının yerini alır",
        ],
        "muhurlu_dosyalar": {DEFTER: sha16(DEFTER), COZ: sha16(COZ)},
    }
    CIKTI.write_text(json.dumps(ek, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"✅ {CIKTI.relative_to(KOK)} · defter {ek['muhurlu_dosyalar'][DEFTER]} · çözümleme "
          f"{ek['muhurlu_dosyalar'][COZ]} · mühür {hashlib.sha256(CIKTI.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
