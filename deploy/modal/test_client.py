"""
birag API test istemcisi.

Sistem promptu ve düşünme modu artık SUNUCU tarafında uygulanıyor (bkz. birag_modal.py):
istekte system mesajı yoksa kanonik BıRAG promptu eklenir, düşünme varsayılan açıktır.

Kullanım:
    export BIRAG_URL="https://yildirim-developer34--birag-api-serve.modal.run"
    export BIRAG_KEY="<API key>"

    uv run --with openai deploy/modal/test_client.py                          # varsayılan soru
    uv run --with openai deploy/modal/test_client.py "Sorun buraya"           # kendi sorun
    uv run --with openai deploy/modal/test_client.py "Soru" --no-think        # düşünme kapalı
    uv run --with openai deploy/modal/test_client.py "Soru" --raw             # sunucu hiçbir şey eklemez (taban davranış)
    uv run --with openai deploy/modal/test_client.py "Soru" --system "Sen ..."   # özel sistem promptu

İlk istek soğuk başlangıç yüzünden 1-3 dk sürebilir.
"""
import argparse
import os
import sys
import time

from openai import OpenAI

parser = argparse.ArgumentParser()
parser.add_argument("prompt", nargs="?", default="Sigarayı bırakmak için 5 öneri ver.")
parser.add_argument("--system", default=None, help="Özel sistem promptu (varsayılan: sunucudaki kanonik prompt)")
parser.add_argument("--raw", action="store_true", help="Sunucu system prompt / düşünme eklemesin")
parser.add_argument("--no-think", action="store_true", help="Bu istekte düşünme modunu kapat")
parser.add_argument("--max-tokens", type=int, default=None, help="Verilmezse sunucu 8192 kullanır")
parser.add_argument("--temperature", type=float, default=None)
args = parser.parse_args()

url = os.environ.get("BIRAG_URL")
key = os.environ.get("BIRAG_KEY")
if not url or not key:
    sys.exit("HATA: Önce BIRAG_URL ve BIRAG_KEY ortam değişkenlerini export et.")

client = OpenAI(base_url=url.rstrip("/") + "/v1", api_key=key, timeout=900)

messages = []
if args.system:
    messages.append({"role": "system", "content": args.system})
messages.append({"role": "user", "content": args.prompt})

kwargs = {}
if args.max_tokens is not None:
    kwargs["max_tokens"] = args.max_tokens
if args.temperature is not None:
    kwargs["temperature"] = args.temperature
if args.no_think:
    kwargs["extra_body"] = {"chat_template_kwargs": {"enable_thinking": False}}
if args.raw:
    kwargs["extra_headers"] = {"X-Birag-Raw": "1"}

system_info = "özel (--system)" if args.system else ("yok (--raw)" if args.raw else "kanonik (sunucu ekliyor)")
thinking_info = "kapalı" if args.no_think else ("şablon varsayılanı (kapalı)" if args.raw else "açık")
print(f"Sistem promptu: {system_info} | düşünme: {thinking_info}")
print("İstek gönderiliyor...", flush=True)

t0 = time.time()
resp = client.chat.completions.create(model="birag", messages=messages, **kwargs)
elapsed = time.time() - t0

choice = resp.choices[0]
reasoning = getattr(choice.message, "reasoning_content", None)
content = choice.message.content or ""

if reasoning:
    print("\n===== DÜŞÜNME =====")
    print(reasoning.strip())
elif "<|channel>thought" in content:
    print("\n(Not: Düşünme metni ayrıştırılmadı, cevabın içinde etiketlerle geliyor.)")

print("\n===== CEVAP =====")
print(content.strip() or "(boş — max_tokens düşünmeye yetmemiş olabilir)")

u = resp.usage
print("\n===== BİLGİ =====")
print(f"Süre: {elapsed:.1f} sn | bitiş nedeni: {choice.finish_reason}")
if u:
    tps = u.completion_tokens / elapsed if elapsed > 0 else 0
    print(f"Token: girdi {u.prompt_tokens}, çıktı {u.completion_tokens} (~{tps:.0f} token/sn, soğuk başlangıç dahil)")
if choice.finish_reason == "length":
    print("UYARI: Cevap max_tokens sınırına (veya bağlam sınırına) takıldı.")
