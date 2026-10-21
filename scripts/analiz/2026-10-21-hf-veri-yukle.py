"""`datasets/v*` sürümlerini Hugging Face veri deposuna yükler — her sürüm bir commit + bir git etiketi.

Sürümler sırayla commit'lenir (v0.0.1 → … → en son), her commit sürümün adıyla etiketlenir; `main` en son sürümde kalır.
Her revizyonda: `README.md` (`docs/hf/veri-karti.md`'den, sayılar o sürümün `train.jsonl`'inden okunur) · `data/train.jsonl`
· `CARD.md` · `manifest.json`. Depoda zaten var olan etiketler atlanır (yarıda kalan yükleme kaldığı yerden sürer).

Seriler (👤 2026-10-21): `refined` = v0.0.1 … v0.1.x · `raw` = v0.2.x (ölçek-5k). Her yeni sürüme seri önekli eş etiket
(`raw-v0.2.1`) aynı commit'te konur ve serinin dalı (`refined` / `raw`) o commit'e taşınır.

Kullanım:
  uv run python scripts/analiz/2026-10-21-hf-veri-yukle.py            # kuru koşu: README'ler scratch'e yazılır
  uv run python scripts/analiz/2026-10-21-hf-veri-yukle.py --yukle    # yükler (önce: uv run hf auth login)
  ... --kart --yukle                                                     # yalnız README: main + seri dalları (etiketler değişmez)
  ... --haric vX                                                         # bu sürüm yüklenmez, tablolarda da yer almaz
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
# 👤 «HF'ye v0.2.1 olarak yükle» (K282): v0.2.0 yüklenmedi. Varsayılan dışlama — yoksa sonraki koşu v0.2.0'ı main'e,
# v0.2.1'in ÜSTÜNE commit'lerdi.
YUKLENMEYEN = ["v0.2.0"]


def surum_anahtari(p):
    return tuple(int(x) for x in p.name.lstrip("v").split("."))


def seri(surum):
    return "raw" if tuple(int(x) for x in surum.lstrip("v").split("."))[:2] >= (0, 2) else "refined"


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
    degerler = {
        "surum": klasor.name, "seri": seri(klasor.name), "tarih": manifest["date"], "repo": repo, "lisans": lisans,
        "son_surum": surumler[-1]["surum"],
        "sha": hashlib.sha256(ham).hexdigest()[:16], "n": len(kayit), "boyut": boyut(len(kayit)),
        "tek": sum(r["turn_type"] == "single" for r in kayit), "cok": sum(r["turn_type"] == "multi" for r in kayit),
        "dusunce": sum(r["has_thinking"] for r in kayit), "replay": sum(r["replay"] for r in kayit),
        "baglam": sum(bool(r["context"]) for r in kayit),   # boş liste bağlam değil
        "dilimler": say(Counter(r["slice"] for r in kayit)),
        "turler": say(Counter(r["addiction_type"] for r in kayit)),
        "yas": say(Counter(r["age_group"] for r in kayit)),
        "surumler": "\n".join(f"| `{s['surum']}` | `{s['seri']}` | {s['tarih']} | {s['n']} | `{s['sha']}` |" for s in surumler),
    }
    for sr in ("refined", "raw"):
        ss = [s["surum"] for s in surumler if s["seri"] == sr]
        degerler[f"{sr}_surumler"] = f"`{ss[0]}` … `{ss[-1]}`" if len(ss) > 1 else f"`{ss[0]}`" if ss else "—"
        degerler[f"{sr}_son"] = ss[-1] if ss else "—"
    return degerler


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="yildirim34/birag-dataset")
    ap.add_argument("--lisans", default="cc-by-4.0")
    ap.add_argument("--ozel", action="store_true", help="depo yoksa özel oluşturulur")
    ap.add_argument("--yukle", action="store_true")
    ap.add_argument("--kart", action="store_true", help="yalnız README'yi main ve seri dallarında güncelle")
    ap.add_argument("--haric", action="append", default=list(YUKLENMEYEN), help="yüklenmeyecek sürüm (tekrarlanabilir)")
    ap.add_argument("--cikti", default=tempfile.gettempdir() + "/birag-hf-kart")
    a = ap.parse_args()

    klasorler = sorted((k for k in (KOK / "datasets").glob("v*.*.*") if k.name not in a.haric), key=surum_anahtari)
    ozet = []
    for k in klasorler:
        ham = (k / "train.jsonl").read_bytes()
        ozet.append({"surum": k.name, "seri": seri(k.name), "tarih": json.loads((k / "manifest.json").read_text())["date"],
                     "n": sum(1 for x in ham.splitlines() if x.strip()), "sha": hashlib.sha256(ham).hexdigest()[:16]})
    sablon = string.Template(SABLON.read_text(encoding="utf-8"))
    cikti = Path(a.cikti)
    cikti.mkdir(parents=True, exist_ok=True)

    if a.kart:
        # dal → kartı yazılacak sürüm: main en son sürüm, seri dalı serisinin son sürümü; tablolar bütün sürümleri gösterir
        son = {"main": klasorler[-1]}
        son.update({seri(k.name): k for k in klasorler})
        kartlar = {}
        for dal, k in son.items():
            kartlar[dal] = sablon.substitute(kart_degerleri(k, ozet, a.repo, a.lisans))
            assert not EPOSTA.search(kartlar[dal])
            (cikti / f"README.{dal}.md").write_text(kartlar[dal], encoding="utf-8")
            print(f"  {dal}: {k.name}")
        print(f"README'ler → {cikti}")
        if not a.yukle:
            return
        from huggingface_hub import CommitOperationAdd, HfApi

        api = HfApi()
        for dal, metin in kartlar.items():
            c = api.create_commit(a.repo, operations=[CommitOperationAdd("README.md", metin.encode("utf-8"))],
                                  repo_type="dataset", revision=dal,
                                  commit_message=f"README: seriler (refined/raw) · {son[dal].name}")
            print(f"  {dal}: {c.oid[:8]}")
        print(f"✅ https://huggingface.co/datasets/{a.repo}")
        return

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
    refs = api.list_repo_refs(a.repo, repo_type="dataset")
    var = {t.name for t in refs.tags}
    dallar = {b.name for b in refs.branches}
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
        sr = seri(k.name)
        # ⛔ revision = commit oid; list_repo_refs().tags[].target_commit etiket NESNESİDİR (dal oluşturma 500 verir)
        for etiket in (k.name, f"{sr}-{k.name}"):
            api.create_tag(a.repo, tag=etiket, revision=c.oid, repo_type="dataset", tag_message=etiket)
        if sr in dallar:
            api.delete_branch(a.repo, branch=sr, repo_type="dataset")
        api.create_branch(a.repo, branch=sr, revision=c.oid, repo_type="dataset")
        dallar.add(sr)
        print(f"  {k.name}: {c.oid[:8]} etiketlendi ({sr}-{k.name}), dal {sr} taşındı")
    print(f"✅ https://huggingface.co/datasets/{a.repo}")


if __name__ == "__main__":
    main()
