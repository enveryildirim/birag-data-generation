#!/usr/bin/env python3
"""EK-1'in mühürlü ölçüm planını koşturur — KALDIĞI YERDEN.

⭐ Plan `configs/deney/2026-09-23-v0022-on-kayit-ek1.json` içindedir ve bu
betik onu **değiştirmez**, yalnız okur. Her (kol, tohum, eksen) için
tamamlanmış bir koşu dizini varsa (satır sayısı = setin öge sayısı)
**atlanır**. Tamlık denetimi kopyalanmadı, ek betiğinden import edildi
(K103) — iki ayrı «bitmiş» tanımı doğmasın.

⛔ Bu betik ÇÖZÜMLEME YAPMAZ. Ön kaydın şartı: ölçüm bitmeden çıktılar
okunmaz. Yalnız koşu ve boş cevap sayısı basılır.

⚡ Hızlandırma (plan DEĞİŞMEDİ — yalnız yürütme): (1) model (kol, tohum)
başına bir kez yüklenir, o adapterin eksenleri art arda koşulur; (2) koşular
iki geçişe ayrılır — önce hükmün dayandığı B1 `cfo`, B2 `context_fidelity`
ve sert kapı `safety`, sonra `cfreal` · `forget` · `sycophancy`; (3) `--isci
i/n` ile n süreç paralel koşar. Atama tahmini süreye göre açgözlüdür ve
deterministiktir: her süreç aynı listeyi hesaplar, yalnız kendi payını alır.
Üretim yolu, `max_tokens` ve sıralı greedy üretim aynı — batch YOK (padding
greedy çıktıyı `d1`'in kayıtlı koşularından saptırabilir).

Kullanım:  uv run python scripts/analiz/2026-09-23-onkayit-ek1-olcum.py [--kuru] [--isci 1/2]
"""
from __future__ import annotations

import json
import sys
import time
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
MUHUR = KOK / "configs/deney/2026-09-23-v0022-on-kayit-ek1.json"

_y = KOK / "scripts/analiz/2026-09-23-onkayit-ek1-yaz.py"
_sp = _iu.spec_from_file_location("_ek1", _y)
_ek = _iu.module_from_spec(_sp)
_argv = sys.argv[:]
sys.argv = [str(_y)]
_sp.loader.exec_module(_ek)
sys.argv = _argv


SURE_DK = {"cfo": 3.5, "cfreal": 2.3, "context_fidelity": 2.3,   # EK-1 raporundaki
           "sycophancy": 3.0, "forget": 1.4, "safety": 4.0}          # kayıtlı ortalamalar
KARAR = ("cfo", "context_fidelity", "safety")                         # 1. geçiş
SIRA = KARAR + ("cfreal", "forget", "sycophancy")


def gruplar(kalan: list[dict]) -> list[list[dict]]:
    """(geçiş, kol, tohum) grupları — model grup başına bir kez yüklenir."""
    g: dict[tuple, list[dict]] = {}
    for p in kalan:
        gecis = 0 if p["eksen"] in KARAR else 1
        g.setdefault((gecis, p["kol"], p["tohum"]), []).append(p)
    return [sorted(v, key=lambda p: SIRA.index(p["eksen"])) for _, v in sorted(g.items())]


def ata(gs: list[list[dict]], n: int) -> list[list[list[dict]]]:
    """Açgözlü, deterministik: sıradaki grup en az yüklü işçiye."""
    yuk, pay = [0.0] * n, [[] for _ in range(n)]
    for grup in gs:
        k = min(range(n), key=lambda j: (yuk[j], j))
        pay[k].append(grup)
        yuk[k] += sum(SURE_DK[p["eksen"]] for p in grup)
    return pay


def main() -> int:
    kuru = "--kuru" in sys.argv
    isci, n_isci = 1, 1
    if "--isci" in sys.argv:
        isci, n_isci = map(int, sys.argv[sys.argv.index("--isci") + 1].split("/"))
    plan = json.loads(MUHUR.read_text())["olcum_plani"]
    kalan, atla = [], 0
    for p in plan:
        if _ek.bitmis(p["kol"], p["tohum"], p["eksen"], _ek.satir_say(p["set"])):
            atla += 1
        else:
            kalan.append(p)
    pay = ata(gruplar(kalan), n_isci)
    benim = pay[isci - 1]
    dk = sum(SURE_DK[p["eksen"]] for g in benim for p in g)
    print(f"plan {len(plan)} · önceden bitmiş {atla} · koşulacak {len(kalan)} · "
          f"işçi {isci}/{n_isci}: {sum(map(len, benim))} koşu, {len(benim)} yükleme, "
          f"~{dk:.0f} dk (tek başına tahmin)")
    if kuru:
        for g in benim:
            print(f"   {g[0]['kol']} t{g[0]['tohum']:<2} " + " · ".join(p["eksen"] for p in g))
        return 0

    sys.path.insert(0, str(KOK / "src"))
    from datetime import datetime
    import yaml
    from mlx_lm import load
    from golden_eval import uret_yuklu
    from eksen_eval import degerlendir_yaz

    cfg = yaml.safe_load((KOK / "configs/training/e4b.yaml").read_text())
    model_dir = KOK / "models" / (cfg["model"].split("/")[-1] + "-train")
    if not model_dir.exists():
        model_dir = Path(cfg["model"])

    hata, n = [], 0
    for grup in benim:
        adapter = sorted(KOK.glob(grup[0]["adapter"]))
        if not adapter:
            hata += [(p["etiket"], "adapter yok") for p in grup]
            continue
        ad = adapter[0].relative_to(KOK)
        t0 = time.time()
        model, tokenizer = load(str(model_dir), adapter_path=str(KOK / ad))
        print(f"── yüklendi {ad} · {time.time()-t0:.1f} sn", flush=True)
        for p in grup:
            n += 1
            print(f"── [{n}/{sum(map(len, benim))}] {p['etiket']} "
                  f"{time.strftime('%H:%M:%S')}", flush=True)
            try:
                ogeler = [json.loads(l) for l in open(KOK / p["set"]) if l.strip()]
                t1 = time.time()
                ciktilar = uret_yuklu(model, tokenizer, ogeler, 1024, False)
                ts = datetime.now().strftime("%Y%m%d-%H%M%S")
                cikti_dir = KOK / "reports/analiz/eksen-kosu" / f"{ts}-{p['etiket']}"
                # ⛔ çözümleme yok: degerlendir_yaz'ın özet çıktısı yutulur
                import contextlib, io
                with contextlib.redirect_stdout(io.StringIO()):
                    degerlendir_yaz(ogeler, ciktilar, time.time() - t1, cikti_dir,
                                    p["etiket"], p["set"], str(ad), model_dir, False, 1024)
                bos = sum(1 for c in ciktilar if not c["cevap"].strip())
                print(f"   {bos} boş cevap · yazıldı: {cikti_dir.relative_to(KOK)}",
                      flush=True)
            except Exception as e:
                hata.append((p["etiket"], f"{type(e).__name__}: {e}"[:200]))
        del model
    print(f"EK-1 ÖLÇÜMÜ BİTTİ (işçi {isci}/{n_isci}) {time.strftime('%H:%M:%S')} · "
          f"hata {len(hata)}")
    for e, h in hata:
        print(f"   ⛔ {e}: {h}")
    return 1 if hata else 0


if __name__ == "__main__":
    raise SystemExit(main())
