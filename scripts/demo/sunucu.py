#!/usr/bin/env python3
"""BıRAG demo sunucusu — tek dosya, standart kütüphane + mlx_lm.

⛔⛔ **BU BİR ARAŞTIRMA PROTOTİPİDİR, DESTEK HİZMETİ DEĞİLDİR.** Model
ölçülmüş kusurlar taşıyor ve bunlar arayüzde de yazılı:
  · kriz yönlendirmesi **tabandan KÖTÜ** (T248: taban 21/30 → kol 5,12/30)
  · korpusta kriz kaydı **yok** (T247) — kriz dilimi uzman onayı bekliyor
  · uydurma oranı **%12** ve bu bir ALT SINIR (T238)

⭐ **Adaptör dürüstçe seçildi: ORTANCA tohum (t31), en iyi değil.** 8 tohumun
dereceli puanları 0–11 arası; en iyisini (t43) koymak demoyu modelin tipik
davranışından daha iyi gösterirdi. Seçim `--adapter` ile değiştirilebilir.

⭐ **Üretim yolu KOPYALANMIYOR (K103):** sohbet şablonu ve system prompt
`golden_eval`'in kullandığı yoldan gelir; demo ile ölçüm aynı metni görür.

Kullanım:
  uv run python scripts/demo/sunucu.py            # ortanca adaptör
  uv run python scripts/demo/sunucu.py --taban    # adaptersiz (karşılaştırma)
  uv run python scripts/demo/sunucu.py --adapter runs/<koşu>/adapters
"""
from __future__ import annotations

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))

VARSAYILAN_ADAPTER = "runs/20260922-*-d1-veri2x-k8qo-v018-t31/adapters"
MODEL_DIZIN = KOK / "models/gemma-4-E4B-it-bf16-train"
SAYFA = Path(__file__).parent / "index.html"

_model = _tok = None
SISTEM = ""


def _sistem_prompt() -> str:
    """Kanonik system prompt — EĞİTİM VERİSİNDEN okunur, elle yazılmaz."""
    for l in open(KOK / "datasets/v0.0.18/train.jsonl"):
        r = json.loads(l)
        if (r.get("gen_meta") or {}).get("system_prompt_variant") == "canon":
            for m in r["messages"]:
                if m["role"] == "system":
                    return m["content"]
    raise SystemExit("⛔ kanonik system prompt bulunamadı")


def _yukle(adapter: Path | None):
    global _model, _tok
    from mlx_lm import load
    print(f"model yükleniyor… adaptör: {adapter or '(YOK — taban)'}")
    _model, _tok = load(str(MODEL_DIZIN),
                        adapter_path=str(adapter) if adapter else None)
    print("hazır.")


def _uret(mesajlar: list[dict], max_tokens: int = 2048) -> str:
    from mlx_lm import generate
    from mlx_lm.sample_utils import make_sampler
    msgs = [{"role": "system", "content": SISTEM}] + mesajlar
    istem = _tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    return generate(_model, _tok, istem, max_tokens=max_tokens,
                    sampler=make_sampler(temp=0.0), verbose=False)


class Istek(BaseHTTPRequestHandler):
    def log_message(self, *a):         # sessiz
        pass

    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_error(404); return
        govde = SAYFA.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(govde)))
        self.end_headers()
        self.wfile.write(govde)

    def do_POST(self):
        if self.path != "/api/sohbet":
            self.send_error(404); return
        n = int(self.headers.get("Content-Length", 0))
        try:
            veri = json.loads(self.rfile.read(n) or b"{}")
            mesajlar = [m for m in veri.get("mesajlar", [])
                        if m.get("role") in ("user", "assistant") and m.get("content")]
            if not mesajlar:
                raise ValueError("mesaj yok")
            cevap = _uret(mesajlar[-12:])   # son 12 tur — bağlam sınırı
            govde = json.dumps({"cevap": cevap}, ensure_ascii=False).encode()
        except Exception as e:
            govde = json.dumps({"hata": f"{type(e).__name__}: {e}"},
                               ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(govde)))
        self.end_headers()
        self.wfile.write(govde)


def main() -> int:
    global SISTEM
    ap = argparse.ArgumentParser()
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--taban", action="store_true", help="adaptersiz koş")
    ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()

    if a.taban:
        adapter = None
    elif a.adapter:
        adapter = KOK / a.adapter
    else:
        bulunan = sorted(KOK.glob(VARSAYILAN_ADAPTER))
        if not bulunan:
            raise SystemExit(f"⛔ varsayılan adaptör yok: {VARSAYILAN_ADAPTER}")
        adapter = bulunan[-1]

    SISTEM = _sistem_prompt()
    _yukle(adapter)
    ad = "TABAN (ince ayarsız)" if adapter is None else adapter.parent.name
    print(f"\n⭐ http://localhost:{a.port}  ·  model: {ad}")
    print("⛔ Araştırma prototipi — destek hizmeti değildir.\n")
    # ⛔ TEK PARÇACIK: MLX GPU akışı iş parçacığına bağlıdır —
    #   ThreadingHTTPServer'da üretim «no Stream(gpu,1) in current
    #   thread» ile düşüyor. İstekler sıraya girer; demo için doğru.
    HTTPServer(("127.0.0.1", a.port), Istek).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
