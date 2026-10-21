"""`datasets/v*` sürümlerini Hugging Face veri deposuna yükler — her sürüm bir commit + bir git etiketi.

Sürümler sırayla commit'lenir (v0.0.1 → … → en son), her commit sürümün adıyla etiketlenir; `main` en son sürümde kalır.
Her revizyonda: `README.md` (`docs/hf/veri-karti.md`'den, sayılar o sürümün `train.jsonl`'inden okunur) · `data/train.jsonl`
· `CARD.md` · `manifest.json`. Depoda zaten var olan etiketler atlanır (yarıda kalan yükleme kaldığı yerden sürer).

Kullanım:
  uv run python scripts/analiz/2026-10-21-hf-veri-yukle.py            # kuru koşu: README'ler scratch'e yazılır
  uv run python scripts/analiz/2026-10-21-hf-veri-yukle.py --yukle    # yükler (önce: uv run hf auth login)
  ... --haric v0.2.0                                                     # bu sürüm yüklenmez, sürüm tablosunda da yer almaz
"""

import argparse
import hashlib
import json
import re
import string
import tempfile
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
SABLON = KOK / "docs/hf/veri-karti.md"
EPOSTA = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")


def surum_anahtari(p):
    return tuple(int(x) for x in p.name.lstrip("v").split("."))


def say(c):
    return " · ".join(f"`{k}` {v}" for k, v in c.most_common())


def eposta_sil(metin):
    """Herkese açık kopyada e-posta kalmaz — yerel `CARD.md` IMMUTABLE, yalnız yüklenen kopya değişir."""
    metin = re.sub(r"\s*\(\s*[\w.+-]+@[\w-]+\.[\w.]+\s*\)", "", metin)
    assert not EPOSTA.search(metin), "⛔ kartta e-posta kaldı"
    return metin


def boyut(n):
    return "n<1K" if n < 1000 else "1K<n<10K" if n < 10_000 else "10K<n<100K"


def kart_degerleri(klasor, surumler, repo, lisans):
    ham = (klasor / "train.jsonl").read_bytes()
    kayit = [json.loads(x) for x in ham.decode("utf-8").splitlines() if x.strip()]
    assert not any(r["is_crisis"] for r in kayit), f"⛔ {klasor.name}: kriz kaydı var, kart 'kriz yok' diyor"
    manifest = json.loads((klasor / "manifest.json").read_text(encoding="utf-8"))
    return {
        "surum": klasor.name, "tarih": manifest["date"], "repo": repo, "lisans": lisans, "son_surum": surumler[-1]["surum"],
        "sha": hashlib.sha256(ham).hexdigest()[:16], "n": len(kayit), "boyut": boyut(len(kayit)),
        "tek": sum(r["turn_type"] == "single" for r in kayit), "cok": sum(r["turn_type"] == "multi" for r in kayit),
        "dusunce": sum(r["has_thinking"] for r in kayit), "replay": sum(r["replay"] for r in kayit),
        "baglam": sum(bool(r["context"]) for r in kayit),   # boş liste bağlam değil
        "dilimler": say(Counter(r["slice"] for r in kayit)),
        "turler": say(Counter(r["addiction_type"] for r in kayit)),
        "yas": say(Counter(r["age_group"] for r in kayit)),
        "surumler": "\n".join(f"| `{s['surum']}` | {s['tarih']} | {s['n']} | `{s['sha']}` |" for s in surumler),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="yildirim34/birag-dataset")
    ap.add_argument("--lisans", default="cc-by-4.0")
    ap.add_argument("--ozel", action="store_true", help="depo yoksa özel oluşturulur")
    ap.add_argument("--yukle", action="store_true")
    ap.add_argument("--haric", action="append", default=[], help="yüklenmeyecek sürüm (tekrarlanabilir)")
    ap.add_argument("--cikti", default=tempfile.gettempdir() + "/birag-hf-kart")
    a = ap.parse_args()

    klasorler = sorted((k for k in (KOK / "datasets").glob("v*.*.*") if k.name not in a.haric), key=surum_anahtari)
    ozet = []
    for k in klasorler:
        ham = (k / "train.jsonl").read_bytes()
        ozet.append({"surum": k.name, "tarih": json.loads((k / "manifest.json").read_text())["date"],
                     "n": sum(1 for x in ham.splitlines() if x.strip()), "sha": hashlib.sha256(ham).hexdigest()[:16]})
    sablon = string.Template(SABLON.read_text(encoding="utf-8"))
    cikti = Path(a.cikti)
    cikti.mkdir(parents=True, exist_ok=True)
    kartlar, surum_kartlari = {}, {}
    for i, k in enumerate(klasorler):
        kartlar[k.name] = sablon.substitute(kart_degerleri(k, ozet[: i + 1], a.repo, a.lisans))
        surum_kartlari[k.name] = eposta_sil((k / "CARD.md").read_text(encoding="utf-8"))
        assert not EPOSTA.search(kartlar[k.name] + (k / "manifest.json").read_text(encoding="utf-8"))
        (cikti / f"README.{k.name}.md").write_text(kartlar[k.name], encoding="utf-8")
    print(f"{len(klasorler)} sürüm: {klasorler[0].name} … {klasorler[-1].name} → README'ler {cikti}")

    if not a.yukle:
        return
    from huggingface_hub import CommitOperationAdd, HfApi

    api = HfApi()
    print(f"kullanıcı: {api.whoami()['name']}")
    api.create_repo(a.repo, repo_type="dataset", private=a.ozel, exist_ok=True)
    var = {t.name for t in api.list_repo_refs(a.repo, repo_type="dataset").tags}
    for k in klasorler:
        if k.name in var:
            print(f"  {k.name}: etiket var, atlandı")
            continue
        islem = [CommitOperationAdd("README.md", kartlar[k.name].encode("utf-8")),
                 CommitOperationAdd("data/train.jsonl", str(k / "train.jsonl")),
                 CommitOperationAdd("CARD.md", surum_kartlari[k.name].encode("utf-8")),
                 CommitOperationAdd("manifest.json", str(k / "manifest.json"))]
        c = api.create_commit(a.repo, operations=islem, repo_type="dataset",
                              commit_message=f"{k.name}: BıRAG veri kümesi")
        api.create_tag(a.repo, tag=k.name, revision=c.oid, repo_type="dataset", tag_message=k.name)
        print(f"  {k.name}: {c.oid[:8]} etiketlendi")
    print(f"✅ https://huggingface.co/datasets/{a.repo}")


if __name__ == "__main__":
    main()
