#!/usr/bin/env python3
"""Colab'ın şablon uygulamasını denetlemek için referans dizgeler — EK-2.

K44 sessiz bir şablon kusuruyla başladı (resmi şablon eğitim hedefinin düşünmesini
siliyordu). Colab'da tokenizer başka bir `transformers` sürümüyle gelir ⇒ eğitimden ÖNCE,
gerçek tokenizer'ın ürettiği dizgenin bu makinede üretilenle BİREBİR aynı olduğu
denetlenir (`colab_egitim.sablon_referansi_denetle`). Buradaki dizgeler tokenizer'sız,
HF'nin `apply_chat_template`'inin içte çağırdığı `render_jinja_template` ile üretilir.

Kapsam: iki kolun eğitim dizgeleri (tam + mask öneki; ilk 3 · çok turlu 3 · replay 2)
ve yedi setin üretim istemi (çok turluda 2. tur, sabit bir ara cevapla).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import transformers
from transformers.utils.chat_template_utils import render_jinja_template

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import colab_egitim as ce  # noqa: E402


class _Cizici:
    bos_token = "<bos>"          # Gemma'nın bos'u; Colab'da tok.bos_token bununla aynı olmak zorunda
    chat_template = None

    def apply_chat_template(self, msgs, tokenize=False, add_generation_prompt=False):
        assert tokenize is False
        return render_jinja_template(conversations=[msgs], chat_template=self.chat_template,
                                     add_generation_prompt=add_generation_prompt, bos_token=self.bos_token)[0][0]


def main() -> int:
    tok = ce.sablon_kur(_Cizici())
    d = ce.sablon_referansi_uret(tok)
    ref = {"bos_token": _Cizici.bos_token, "sablon": "configs/chat_template_train.jinja",
           "sablon_sha256_16": ce.sha16(ce.SABLON), "uretici": f"transformers {transformers.__version__} render_jinja_template",
           "dizgeler": d}
    ce.REFERANS.write_text(json.dumps(ref, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"✅ {ce.REFERANS.relative_to(KOK)} · {len(d)} dizge · şablon {ref['sablon_sha256_16']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
