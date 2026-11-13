"""
birag-gemma4-26b (Q8_0 GGUF) -> Modal serverless API (llama.cpp, NVIDIA L40S)

Mimari (tek konteyner):
    istemci ──> FastAPI vekil (Modal web adresi) ──> llama-server (127.0.0.1:8081)

Vekil, eğitimdeki koşulları SUNUCU TARAFINDA uygular:
  · İstekte system mesajı yoksa KANONİK BıRAG system prompt'u eklenir
    (deploy anında eğitim verisinden okunur — K103: elle yazılmaz, veriden okunur).
  · chat_template_kwargs.enable_thinking verilmemişse True yapılır (eğitim verisinin tamamı düşünmeli).
  · max_tokens verilmemişse 8192 yapılır.
  · İstemci kendi system mesajını veya enable_thinking değerini gönderirse ona dokunulmaz.
  · "X-Birag-Raw: 1" başlığı gönderilirse hiçbir şey eklenmez (taban davranış karşılaştırması için).

- OpenAI uyumlu API: <URL>/v1/chat/completions , model adı: "birag"
- İstek yoksa GPU kapanır (scale-to-zero), saniye bazında ücretlendirilir.

Adımlar (proje klasöründe):
    modal run deploy/modal/birag_modal.py::download    # modeli bir kez volume'a indirir
    modal deploy deploy/modal/birag_modal.py           # API'yi yayınlar
"""

import base64
import json
import os
import subprocess
import time
from pathlib import Path

import modal

HF_REPO = "yildirim34/birag-gemma4-26b"
GGUF_FILE = "gemma-4-26b-a4b-it.Q8_0.gguf"   # 26.9 GB (Q4_K_M için: "gemma-4-26b-a4b-it.Q4_K_M.gguf")
MODEL_DIR = "/models"
GPU = "L40S"            # 48 GB VRAM (Q4_K_M için "L4" yeterli)
CTX_SIZE = 16384        # Bağlam uzunluğu
IDLE_SECONDS = 300      # Son istekten 5 dk sonra GPU kapanır
DEFAULT_MAX_TOKENS = 8192  # İstemci max_tokens göndermezse kullanılır (düşünme dahil)
LLAMA_PORT = 8081       # llama-server sadece konteyner içinden erişilir
URL_LABEL = "birag-api-serve"  # -> https://<kullanici>--birag-api-serve.modal.run (eski adresle aynı)


def _canonical_system_prompt() -> str:
    """En yeni veri sürümündeki kanonik system prompt (scripts/demo/sunucu.py ile aynı kural)."""
    root = Path(__file__).resolve().parents[2]

    def version_key(d: Path):
        return tuple(int(x) for x in d.name.lstrip("v").split("."))

    for d in sorted((root / "datasets").glob("v*"), key=version_key, reverse=True):
        f = d / "train.jsonl"
        if not f.exists():
            continue
        for line in open(f, encoding="utf-8"):
            r = json.loads(line)
            if (r.get("gen_meta") or {}).get("system_prompt_variant") == "canon":
                for m in r["messages"]:
                    if m["role"] == "system":
                        return m["content"]
    raise SystemExit("⛔ kanonik system prompt bulunamadı")


# Deploy anında (yerelde) veriden okunur, imaja ortam değişkeni olarak gömülür.
# Base64 ile kodlanır: prompt'taki tırnak (BıRAG'sın) ve satır sonları Dockerfile ENV satırını bozuyor.
if modal.is_local():
    SYSTEM_PROMPT = _canonical_system_prompt()
    SYSTEM_PROMPT_B64 = base64.b64encode(SYSTEM_PROMPT.encode("utf-8")).decode("ascii")
else:
    SYSTEM_PROMPT_B64 = os.environ.get("BIRAG_SYSTEM_B64", "")
    SYSTEM_PROMPT = base64.b64decode(SYSTEM_PROMPT_B64).decode("utf-8")

app = modal.App("birag-api")
models = modal.Volume.from_name("birag-models", create_if_missing=True)

# Modeli indirmek için hafif, GPU'suz imaj
download_image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("huggingface_hub")
    .env({"HF_XET_HIGH_PERFORMANCE": "1"})
)

# llama.cpp'nin resmi CUDA sunucu imajı + vekil için FastAPI/httpx
server_image = (
    modal.Image.from_registry("ghcr.io/ggml-org/llama.cpp:server-cuda", add_python="3.12")
    .entrypoint([])
    .pip_install("fastapi", "httpx")
    .env({"BIRAG_SYSTEM_B64": SYSTEM_PROMPT_B64})
)


@app.function(image=download_image, volumes={MODEL_DIR: models}, timeout=60 * 60)
def download():
    from huggingface_hub import hf_hub_download

    path = hf_hub_download(repo_id=HF_REPO, filename=GGUF_FILE, local_dir=MODEL_DIR)
    models.commit()
    print(f"Model hazır: {path}")


def prepare_request(body: dict, system_prompt: str, raw: bool) -> dict:
    """Eğitim koşullarını isteğe uygular (system prompt + düşünme + max_tokens). Saf fonksiyon, test edilebilir."""
    # max_tokens yoksa varsayılanı koy (ham modda da: sınırsız üretim GPU'yu meşgul eder)
    if body.get("max_tokens") is None and body.get("max_completion_tokens") is None:
        body["max_tokens"] = DEFAULT_MAX_TOKENS
    if raw:
        return body
    messages = body.get("messages") or []
    if not any(m.get("role") == "system" for m in messages):
        body["messages"] = [{"role": "system", "content": system_prompt}] + messages
    kw = body.get("chat_template_kwargs") or {}
    kw.setdefault("enable_thinking", True)
    body["chat_template_kwargs"] = kw
    return body


@app.cls(
    image=server_image,
    gpu=GPU,
    volumes={MODEL_DIR: models},
    secrets=[modal.Secret.from_name("birag-api-key")],
    scaledown_window=IDLE_SECONDS,
    timeout=60 * 60,
    max_containers=1,   # Test amaçlı: aynı anda en fazla 1 GPU (maliyet kontrolü)
)
@modal.concurrent(max_inputs=8)
class Birag:
    @modal.enter()
    def start(self):
        import urllib.request

        self.proc = subprocess.Popen([
            "/app/llama-server",
            "--model", f"{MODEL_DIR}/{GGUF_FILE}",
            "--host", "127.0.0.1",
            "--port", str(LLAMA_PORT),
            "--n-gpu-layers", "999",
            "--ctx-size", str(CTX_SIZE),
            "--parallel", "1",
            "--alias", "birag",
            "--jinja",
            "--api-key", os.environ["API_KEY"],
        ])
        # Model tamamen yüklenene kadar bekle; istekler ancak bundan sonra kabul edilir.
        while True:
            if self.proc.poll() is not None:
                raise RuntimeError("llama-server beklenmedik şekilde kapandı (log'lara bak)")
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{LLAMA_PORT}/health", timeout=2) as r:
                    if r.status == 200:
                        break
            except Exception:
                pass
            time.sleep(1)
        print(f"llama-server hazır. Kanonik system prompt: {len(SYSTEM_PROMPT)} karakter")

    @modal.exit()
    def stop(self):
        self.proc.terminate()

    @modal.asgi_app(label=URL_LABEL)
    def api(self):
        return build_proxy_app(f"http://127.0.0.1:{LLAMA_PORT}", SYSTEM_PROMPT)


def build_proxy_app(upstream: str, system_prompt: str):
    """llama-server önündeki FastAPI vekili."""
    import httpx
    from fastapi import FastAPI, Request
    from fastapi.responses import Response, StreamingResponse
    from starlette.background import BackgroundTask

    web = FastAPI(title="BıRAG API")
    client = httpx.AsyncClient(base_url=upstream, timeout=None)
    forwarded_headers = ("authorization", "content-type", "accept")

    def forward_headers(req: Request) -> dict:
        return {k: v for k, v in req.headers.items() if k.lower() in forwarded_headers}

    @web.post("/v1/chat/completions")
    async def chat_completions(req: Request):
        body = prepare_request(await req.json(), system_prompt, req.headers.get("x-birag-raw") == "1")
        h = forward_headers(req)
        if body.get("stream"):
            resp = await client.send(
                client.build_request("POST", "/v1/chat/completions", json=body, headers=h),
                stream=True,
            )
            return StreamingResponse(
                resp.aiter_raw(),
                status_code=resp.status_code,
                media_type=resp.headers.get("content-type"),
                background=BackgroundTask(resp.aclose),
            )
        resp = await client.post("/v1/chat/completions", json=body, headers=h)
        return Response(resp.content, status_code=resp.status_code,
                        media_type=resp.headers.get("content-type"))

    # Diğer her şey (/v1/models, /health, web arayüzü...) olduğu gibi geçer
    @web.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    async def passthrough(path: str, req: Request):
        resp = await client.request(req.method, "/" + path, content=await req.body(),
                                      headers=forward_headers(req), params=req.query_params)
        return Response(resp.content, status_code=resp.status_code,
                        media_type=resp.headers.get("content-type"))

    return web
