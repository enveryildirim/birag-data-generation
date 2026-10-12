"""26B model kartını eğitim kontrol noktasından doldurur ve (istenirse) Hugging Face'e yükler — Colab'da çalıştırılır.

Eğitim ayrıntıları elle yazılmaz: son kontrol noktasındaki `adapter_config.json` (LoRA), `trainer_state.json`
(adım, tur, kayıp) ve `training_args.bin`'den (öğrenme oranı, batch, optimizer…) okunur.

Colab'da bir hücreye yapıştırın, ilk üç değişkeni kontrol edin, çalıştırın. Önce `YUKLE = False` ile README.md'yi
okuyun; doğruysa `YUKLE = True` ile yeniden çalıştırın. Belirteç yalnız Colab gizlilerinden (`HF_TOKEN`) okunur.
"""
import glob
import json
import os
import string
import subprocess
from collections import Counter
from datetime import date

import torch

EGITIM_KLASORU = "/content/drive/MyDrive/birag-sohbet/ckpt-26"   # SFTConfig(output_dir=...) — checkpoint-* klasörlerinin olduğu yer
YUKLEME = "bf16"            # eğitimde load_in_4bit=True kullandıysanız: "4-bit (QLoRA)"
YUKLE = False               # True: README.md ve sistem_istemi.txt depoya yüklenir
REPO = "yildirim34/birag-gemma4-26b"
DEPO = "/content/birag"

if not os.path.exists(DEPO):
    subprocess.run(["git", "clone", "-q", "--depth", "1",
                    "https://github.com/enveryildirim/birag-data-generation.git", DEPO], check=True)

ckpt = sorted(glob.glob(f"{EGITIM_KLASORU}/checkpoint-*"), key=lambda p: int(p.rsplit("-", 1)[1]))
assert ckpt, f"⛔ {EGITIM_KLASORU} içinde checkpoint-* yok"
son = ckpt[-1]
lora = json.load(open(f"{son}/adapter_config.json"))
durum = json.load(open(f"{son}/trainer_state.json"))
args = torch.load(f"{son}/training_args.bin", weights_only=False)

hedef = lora["target_modules"]
hedef = f"`{hedef}`".replace("|", "\\|") if isinstance(hedef, str) else ", ".join(f"`{h}`" for h in sorted(hedef))
eval_kayip = [x["eval_loss"] for x in durum["log_history"] if "eval_loss" in x]
isinma = f"{args.warmup_steps} adım" if getattr(args, "warmup_steps", 0) else f"oran {getattr(args, 'warmup_ratio', 0)}"
max_len = getattr(args, "max_length", None) or getattr(args, "max_seq_length", None) or "—"

deger = {
    "yukleme": YUKLEME,
    "r": lora["r"], "lora_alpha": lora["lora_alpha"], "dropout": lora.get("lora_dropout", 0), "hedef": hedef,
    "optim": str(args.optim).split(".")[-1].lower(), "lr": f"{args.learning_rate:g}",
    "zamanlayici": str(args.lr_scheduler_type).split(".")[-1].lower(), "isinma": isinma, "wd": f"{args.weight_decay:g}",
    "etkin_batch": args.per_device_train_batch_size * args.gradient_accumulation_steps,
    "adim": durum["global_step"], "epoch": f"{durum['epoch']:.2f}", "max_len": max_len,
    "eval_loss": f"{eval_kayip[-1]:.4f} (adım {durum['global_step']})" if eval_kayip else "kaydedilmedi",
    "tarih": date.today().isoformat(),
}
kart = string.Template(open(f"{DEPO}/docs/hf/model-karti-26b.md", encoding="utf-8").read()).substitute(deger)

kayit = [json.loads(x) for x in open(f"{DEPO}/datasets/v0.1.1/train.jsonl", encoding="utf-8")]
sistem = Counter(r["messages"][0]["content"] for r in kayit if r["messages"][0]["role"] == "system").most_common(1)[0][0]
assert "<|think|>" not in sistem

os.makedirs("/content/birag-kart", exist_ok=True)
open("/content/birag-kart/README.md", "w", encoding="utf-8").write(kart)
open("/content/birag-kart/sistem_istemi.txt", "w", encoding="utf-8").write(sistem)
print(f"kontrol noktası: {os.path.basename(son)}")
print(json.dumps({k: v for k, v in deger.items() if k != "tarih"}, ensure_ascii=False, indent=1, default=str))
print("→ /content/birag-kart/README.md · sistem_istemi.txt")

if YUKLE:
    from google.colab import userdata
    from huggingface_hub import HfApi
    api = HfApi(token=userdata.get("HF_TOKEN"))
    for ad in ("README.md", "sistem_istemi.txt"):
        api.upload_file(path_or_fileobj=f"/content/birag-kart/{ad}", path_in_repo=ad, repo_id=REPO,
                        commit_message=f"{ad}: BıRAG model kartı / sistem istemi")
    print(f"✅ yüklendi: https://huggingface.co/{REPO}")
