"""MLX LoRA eğitimi (keşif ayağı). Bkz. plan.md §10, §13 Faz 2, Kural 4/5/7.

Yaptığı iş:
  1. configs/training/*.yaml okunur — TEK hiper-parametre kaynağı
  2. datasets/vX/train.jsonl -> mlx `messages` formatına çevrilir
     · thinking, son asistan turunda <|channel>thought ... <channel|> ile gömülür
     · thinking AÇIK kayıtlarda system içeriğine <|think|> önekleniyor (K44)
  3. `mlx_lm lora` alt süreç olarak koşulur
  4. Her şey runs/<ts>/ altına yazılır — asla silinmez (K35)

Kullanım: uv run python src/train.py configs/training/e4b.yaml
"""
from __future__ import annotations
import hashlib
import json
import os
import platform
import random
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
THINK_ON = "<|think|>\n"


def build_train_model_dir(repo: str, template_path: Path) -> Path:
    """Ağırlıkları kopyalamadan, yamalı chat template'li bir model dizini kurar.

    mlx_lm tokenizer'ı model dizininden yükler; resmi template thinking'i sildiği için
    (K44) eğitimde yamalı sürüm gerekiyor. Büyük dosyalar sembolik bağ, 16 GB kopyalanmaz.
    """
    from huggingface_hub import snapshot_download

    snap = Path(snapshot_download(repo))
    out = ROOT / "models" / (repo.split("/")[-1] + "-train")
    out.mkdir(parents=True, exist_ok=True)
    for f in snap.iterdir():
        hedef = out / f.name
        if f.name == "chat_template.jinja":
            continue
        if not hedef.exists():
            hedef.symlink_to(f.resolve())
    (out / "chat_template.jinja").write_text(template_path.read_text())
    return out


def _sysctl(anahtar: str) -> str:
    """macOS `sysctl -n`. Başka platformda ya da hata hâlinde boş döner."""
    try:
        r = subprocess.run(["sysctl", "-n", anahtar], capture_output=True, text=True, timeout=5)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def donanim() -> dict:
    """§3.2'nin `donanım` kalemi (T65 · `2026-09-16-kosu-kaydi-denetimi.md`).

    ⛔ 24 koşunun 0'ında donanım kaydı yoktu: kural ilan edilmiş, yazıcı hiç
    üretmemişti. ⚠️ Geçmişe yazılamaz (Kural 7); buradan itibaren yazılır.
    Alanların hepsi **ortamdan okunur**, elle girilmez.
    """
    mem = _sysctl("hw.memsize")
    def _surum(ad: str) -> str:
        try:
            from importlib.metadata import version
            return version(ad)
        except Exception:
            return ""
    try:
        import mlx.core as mx
        # ⚠️ `mx.metal.device_info` kullanımdan kalkıyor; yenisi varsa o kullanılır.
        bilgi = (mx.device_info() if hasattr(mx, "device_info") else mx.metal.device_info())
        bellek_sinir = bilgi.get("max_recommended_working_set_size")
    except Exception:
        bellek_sinir = None
    return {
        "platform": platform.platform(),
        "makine": platform.machine(),
        "islemci": _sysctl("machdep.cpu.brand_string") or platform.processor(),
        "cekirdek": os.cpu_count(),
        "bellek_gb": round(int(mem) / 1024**3, 1) if mem.isdigit() else None,
        "python": platform.python_version(),
        "mlx": _surum("mlx"),
        "mlx_lm": _surum("mlx-lm"),
        "metal_calisma_kumesi_gb": round(bellek_sinir / 1024**3, 1) if bellek_sinir else None,
    }


def sha16(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def yaz_samples(run_dir: Path, data_dir: Path, model_dir: Path, cfg: dict,
                dataset: Path, n: int = 3) -> None:
    """§3.2'nin `samples.md` kalemi — iki yerde ilan edildi, hiçbir yerde üretilmiyordu.

    ⭐ İçeriği §3.2 tanımlamıyor; **bu bizim kararımız**: modelin GÖRDÜĞÜ dizge
    yazılır, `tokenizer.apply_chat_template` ile (Kural 4 — şablon asla elle
    kurulmaz). Gerekçe K44: chat template thinking'i sessizce siliyordu ve hiçbir
    sayı bunu göstermiyordu. ⚠️ Şablonu ayrıca dosyaya basmak yetmez; kırılma
    şablonun METNİNDE değil, UYGULANMASINDA görünür.

    Örnekler **ilk n kayıt** — bölme zaten tohumla belirlendiği için seçim
    yeniden üretilebilir (ayrıca rastgelelik eklenmiyor).
    """
    satirlar = [l for l in (data_dir / "train.jsonl").read_text(encoding="utf-8").split("\n")
                if l.strip()][:n]
    L = [f"# Eğitim örnekleri — `{run_dir.name}`", "",
         f"**Dataset:** `{cfg['dataset']}` SHA256 `{sha16(dataset)}`  ",
         f"**Tohum:** `{cfg['veri']['seed']}` · **Şablon:** "
         f"`{cfg['veri']['chat_template']}` SHA256 `{sha16(ROOT / cfg['veri']['chat_template'])}`  ",
         f"**Model:** `{cfg['model']}`", "",
         "> ⭐ Aşağıdaki metin modelin **gördüğü dizgedir** — `apply_chat_template`",
         "> ile üretildi (Kural 4). K44'ün sessiz şablon kırılması tam burada görünürdü.", ""]
    try:
        from transformers import AutoTokenizer
        tok = AutoTokenizer.from_pretrained(str(model_dir))
        for i, ham in enumerate(satirlar, 1):
            msgs = json.loads(ham)["messages"]
            metin = tok.apply_chat_template(msgs, tokenize=False)
            L += [f"## Örnek {i}/{len(satirlar)} — {len(tok(metin)['input_ids'])} token", "",
                  "```text", metin, "```", ""]
    except Exception as e:  # ⚠️ örnek yazımı eğitimi DÜŞÜRMEZ, ama sessizce de geçmez
        L += [f"⛔ **Şablon uygulanamadı:** `{type(e).__name__}: {e}`", "",
              "⚠️ Ham `messages` kayıtları aşağıda; şablonlanmış hâli **yok**.", ""]
        for i, ham in enumerate(satirlar, 1):
            L += [f"## Örnek {i} (ham)", "", "```json", ham, "```", ""]
    (run_dir / "samples.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def to_mlx_messages(rec: dict) -> dict:
    """TrainRecord -> mlx `messages` formatı. thinking son asistan turuna gömülür."""
    msgs = []
    for m in rec["messages"]:
        rol = m["role"]
        icerik = m["content"]
        if rol == "system" and rec.get("has_thinking"):
            icerik = THINK_ON + icerik
        if rol == "assistant" and m.get("thinking"):
            icerik = f"<|channel>thought\n{m['thinking']}\n<channel|>{icerik}"
        msgs.append({"role": rol, "content": icerik})
    return {"messages": msgs}


def prepare_data(dataset: Path, out_dir: Path, valid_orani: float, seed: int) -> tuple[int, int]:
    kayitlar = [json.loads(l) for l in open(dataset) if l.strip()]
    random.Random(seed).shuffle(kayitlar)
    n_valid = max(1, round(len(kayitlar) * valid_orani))
    valid, train = kayitlar[:n_valid], kayitlar[n_valid:]

    out_dir.mkdir(parents=True, exist_ok=True)
    for ad, bolum in (("train", train), ("valid", valid)):
        with open(out_dir / f"{ad}.jsonl", "w") as f:
            for r in bolum:
                f.write(json.dumps(to_mlx_messages(r), ensure_ascii=False) + "\n")
    return len(train), len(valid)


def main(config_path: str):
    cfg = yaml.safe_load(Path(config_path).read_text())
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = ROOT / "runs" / f"{ts}-{cfg['ad']}"
    run_dir.mkdir(parents=True, exist_ok=True)

    # 1) yamalı template'li model dizini
    model_dir = build_train_model_dir(cfg["model"], ROOT / cfg["veri"]["chat_template"])

    # 2) veri
    data_dir = run_dir / "data"
    n_train, n_valid = prepare_data(
        ROOT / cfg["dataset"], data_dir, cfg["veri"]["valid_orani"], cfg["veri"]["seed"]
    )
    print(f"veri hazır: {n_train} eğitim / {n_valid} doğrulama -> {data_dir}")

    # 3) mlx_lm'in beklediği düz config
    mlx_cfg = dict(cfg["mlx"])
    mlx_cfg.update({"model": str(model_dir), "train": True, "data": str(data_dir),
                    "adapter_path": str(run_dir / "adapters")})
    mlx_cfg_path = run_dir / "mlx_config.yaml"
    mlx_cfg_path.write_text(yaml.safe_dump(mlx_cfg, allow_unicode=True, sort_keys=False))

    # 4) çalıştır
    (run_dir / "config.yaml").write_text(Path(config_path).read_text())
    log_path = run_dir / "train.log"
    t0 = time.time()
    with open(log_path, "w") as log:
        proc = subprocess.run(
            [sys.executable, "-m", "mlx_lm", "lora", "-c", str(mlx_cfg_path)],
            cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, text=True,
        )
    sure = time.time() - t0
    yaz_samples(run_dir, data_dir, model_dir, cfg, ROOT / cfg["dataset"])

    metrics = {
        "run": run_dir.name, "tarih": ts, "config": config_path,
        "model": cfg["model"], "dataset": cfg["dataset"],
        "n_train": n_train, "n_valid": n_valid,
        "dataset_sha256_16": sha16(ROOT / cfg["dataset"]),
        "seed": cfg["veri"]["seed"],
        "iters": cfg["mlx"]["iters"], "sure_saniye": round(sure, 1),
        "donus_kodu": proc.returncode,
        "donanim": donanim(),
        "git_rev": subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                                  capture_output=True, text=True).stdout.strip(),
    }
    (run_dir / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2))
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    print(f"log: {log_path}")
    return proc.returncode


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("kullanım: uv run python src/train.py configs/training/e4b.yaml")
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
