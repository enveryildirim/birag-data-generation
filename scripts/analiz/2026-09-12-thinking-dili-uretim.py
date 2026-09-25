"""K48-b öğrenilebilirlik testi — üretim ayağı. Bkz. Kural 7, K49/K50/K51.

Soru: Gemma 4'ün İngilizce muhakeme prior'ı (K48: talimatla kırılmıyor, 36/36)
eğitim verisiyle kırılabiliyor mu?

Yöntem: 16 kayıtla 300 adım = KASITLI aşırı öğrenme, öğrenilebilirliğin ÜST SINIRI.
İki kol: dar LoRA (`e4b-thinking-dili.yaml`) ve geniş LoRA (`…-genis.yaml`).
Değerlendirme tohumları prompt-dili ablasyonundan gelir ve eğitim setiyle
ÇAKIŞMAZ (doğrulandı: 0/12).

Kullanım: uv run python scripts/analiz/2026-09-12-thinking-dili-uretim.py <runs/dizin> <cikti.jsonl>
Rapor:    uv run python scripts/analiz/2026-09-12-thinking-dili-raporu.py
"""
import json, sys, time
from pathlib import Path
ROOT = Path("/Users/pc/projects/birag/data-finetuning")
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts" / "analiz"))
from eval import split_output, THINK_ON
sys.path.insert(0, str(ROOT))
import importlib.util
spec = importlib.util.spec_from_file_location("rap", ROOT / "scripts/analiz/2026-09-12-prompt-dili-raporu.py")
rap = importlib.util.module_from_spec(spec); spec.loader.exec_module(rap)

from mlx_lm import load, stream_generate
from mlx_lm.sample_utils import make_sampler

SYS = json.loads(open(ROOT / "datasets/v0.0.1/train.jsonl").readline())["messages"][0]["content"]
abl = [json.loads(l) for l in open(ROOT / "reports/analiz/prompt-dili-ablasyonu/generations.jsonl")]
seeds = [r for r in abl if r["varyant"] == "tr_sys"]
RUN = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "runs/20260912-181209-e4b-thinking-dili-ustsinir"
CIKTI = sys.argv[2] if len(sys.argv) > 2 else "/tmp/thinking_dili_sonuc.jsonl"

sonuc = []
for etiket, ap in [("adapter-100", RUN/"adapters"/"0000100_adapters.safetensors"),
                   ("adapter-200", RUN/"adapters"/"0000200_adapters.safetensors"),
                   ("adapter-300", RUN/"adapters"/"0000300_adapters.safetensors")]:
    # mlx_lm adapter_path bir DİZİN bekliyor; checkpoint'i geçici dizine koy
    tmp = Path(f"/tmp/ap-{etiket}"); tmp.mkdir(exist_ok=True)
    (tmp/"adapters.safetensors").write_bytes(ap.read_bytes())
    (tmp/"adapter_config.json").write_text((RUN/"adapters"/"adapter_config.json").read_text())
    model, tok = load(str(ROOT/"models/gemma-4-E4B-it-bf16-train"), adapter_path=str(tmp))
    sampler = make_sampler(temp=0.0)
    print(f"\n[{etiket}]")
    for s in seeds:
        msgs = [{"role":"system","content":THINK_ON+SYS},{"role":"user","content":s["user_message"]}]
        p = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        parts, son = [], None
        t0=time.time()
        for x in stream_generate(model, tok, p, max_tokens=2048, sampler=sampler):
            parts.append(x.text); son = x
        th, comp, kap = split_output("".join(parts))
        d = rap.dil(th)
        sonuc.append({"etiket":etiket,"seed_id":s["seed_id"],"thinking":th,"completion":comp,
                      "dil":d,"thinking_kelime":len(th.split()),"completion_kelime":len(comp.split()),
                      "sure":round(time.time()-t0,1),"kesildi":son.finish_reason!="stop"})
        print(f"  {s['seed_id'][:8]} dil={d}  think={len(th.split()):4}kel cevap={len(comp.split()):3}kel")
    del model

with open(CIKTI,"w") as f:
    for r in sonuc: f.write(json.dumps(r, ensure_ascii=False)+"\n")
print("\n=== ÖZET ===")
for e in ["adapter-100","adapter-200","adapter-300"]:
    g=[r for r in sonuc if r["etiket"]==e]
    tr=sum(1 for r in g if r["dil"]=="tr")
    print(f"{e}: thinking Türkçe {tr}/{len(g)}  · medyan thinking {sorted(r['thinking_kelime'] for r in g)[len(g)//2]} kel")
