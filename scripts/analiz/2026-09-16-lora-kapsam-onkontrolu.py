#!/usr/bin/env python3
"""LoRA anahtarları GERÇEKTEN eşleşiyor mu — K49'un tuzağı için önkontrol (T85).

K49: *«Gemma 4 E4B'de `v_proj`/`k_proj` YOK (K/V paylaşımlı attention); katmanda
yalnızca q_proj ve o_proj var. Eskiden burada yazan `self_attn.v_proj` hiçbir
şeyle eşleşmiyordu ve mlx-lm uyarı vermiyordu -> koşular sanılanın yarısı
kapsamla yapıldı.»*

⭐⭐ **Gözlem doğruydu, MEKANİZMA yanlış — ve fark önemli.** mlx-lm'in kendi modül
ağacı okundu: `v_proj`/`k_proj` **katman 0-23'te VAR**, 24-41'de yok (42 katmanın
24'ü). `mlx_lm` `num_layers: N` **ÜSTTEN** N katman alır ⇒

    num_layers= 8 -> katman 34..41 -> v_proj  0/8   ⛔ ölü
    num_layers=24 -> katman 18..41 -> v_proj  6/24
    num_layers=42 -> katman  0..41 -> v_proj 24/42  ✅ canlı

➡️ *Yani anahtar «modelde yok» değil, **seçilen DİLİMDE yok**. Aynı anahtar
`num_layers` büyüyünce sessizce CANLANIR. ⇒ «Bu anahtar ölü mü» sorusunun cevabı
modele değil, **config'in kendisine** bağlıdır ve her config için ayrı sorulmalıdır.*

⛔ **Bu betiğin repo dışı bir bağımlılığı var:** modelin lokalde olması gerekiyor.
Yoksa rapor bunu **yazar** ve sayı üretmez — sessizce geçmez.

Girdi : configs/training/*.yaml · mlx_lm modül ağacı (model lokalde olmalı)
Çıktı : reports/analiz/2026-09-16-lora-kapsam-onkontrolu.md
Kullanım: uv run python scripts/analiz/2026-09-16-lora-kapsam-onkontrolu.py
"""
from __future__ import annotations

import collections
import hashlib
import re
import sys
from pathlib import Path

import yaml

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-lora-kapsam-onkontrolu.md"
CONFIG = KOK / "configs/training"
KATMAN = re.compile(r"^language_model\.model\.layers\.(\d+)\.(.+)$")


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def modul_agaci(model_dizini: Path) -> dict[int, set[str]] | None:
    """{katman indeksi: {modül son eki}} — mlx-lm'in KENDİ ağacından.

    ⚠️ HF `safetensors.index.json` yeterli DEĞİL: mlx-lm dönüştürme sırasında
    modülleri yeniden adlandırabilir/kaynaştırabilir ve LoRA hedefi runtime
    ağacıdır. Bu yüzden model **yükleniyor** (tembel yükleme, ~3 sn).
    """
    if not model_dizini.exists():
        return None
    try:
        import mlx.nn as nn
        from mlx_lm.utils import load
    except Exception:
        return None
    model, _ = load(str(model_dizini))
    out: dict[int, set[str]] = collections.defaultdict(set)
    for ad, m in model.named_modules():
        mm = KATMAN.match(ad or "")
        if mm and isinstance(m, nn.Linear):
            out[int(mm.group(1))].add(mm.group(2))
    return dict(out)


def yerel_dizin(repo: str) -> Path:
    return KOK / "models" / (repo.split("/")[-1] + "-train")


def main() -> int:
    cfgler = []
    for p in sorted(CONFIG.glob("*.yaml")):
        c = yaml.safe_load(p.read_text(encoding="utf-8"))
        if isinstance(c, dict) and "mlx" in c:
            cfgler.append((p, c))
    modeller = sorted({c["model"] for _, c in cfgler})

    L: list[str] = []
    L += ["# LoRA anahtarları gerçekten eşleşiyor mu — K49'un tuzağı için önkontrol", "",
          f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
          f"**Girdi:** `configs/training/*.yaml` — **{len(cfgler)}** eğitim config'i  ",
          f"**Girdi (repo DIŞI):** ⧉ mlx-lm modül ağacı — model **lokalde olmalı**",
          "", "---", "", "## Neden", "",
          "K49: *«Eskiden burada yazan `self_attn.v_proj` hiçbir şeyle eşleşmiyordu ve",
          "**mlx-lm uyarı vermiyordu** → koşular sanılanın yarısı kapsamla yapıldı.»*",
          "⛔ Sessiz kalan bir eşleşmezlik, koşuyu düşürmez — **yanlış koşuyu doğru**",
          "**sanmanıza** yol açar. ⇒ Koşudan **önce** sorulmalı.", "", "---", ""]

    agac = {}
    for repo in modeller:
        agac[repo] = modul_agaci(yerel_dizin(repo))

    L += ["## 1. Model modül ağacı", "", "| model | lokalde | katman | ölçülen |",
          "|---|---|---:|---|"]
    for repo, a in agac.items():
        if a is None:
            L.append(f"| `{repo}` | ⛔ **hayır** | — | ⛔ **önkontrol yapılamadı** |")
        else:
            L.append(f"| `{repo}` | ✅ evet | {len(a)} | ✅ mlx-lm modül ağacı |")
    canli = {r: a for r, a in agac.items() if a}
    if canli:
        repo, a = next(iter(canli.items()))
        ekler = collections.Counter(e for s in a.values() for e in s)
        L += ["", f"**`{repo}` — katman başına modüller:**", "",
              "| modül | katman sayısı | hangi katmanlar |", "|---|---:|---|"]
        for e, n in sorted(ekler.items()):
            idx = sorted(i for i, s in a.items() if e in s)
            aralik = (f"{idx[0]}–{idx[-1]}" if idx == list(range(idx[0], idx[-1] + 1))
                      else f"{len(idx)} katman")
            L.append(f"| `{e}` | **{n}**/{len(a)} | {aralik} |")
        L += ["",
              "⭐⭐ **K49'un mekanizması düzeltildi:** `v_proj`/`k_proj` modelde **var** —",
              "ama **alt** katmanlarda. `mlx_lm` `num_layers: N` **ÜSTTEN** N katman alır:", "",
              "| `num_layers` | seçilen dilim | `v_proj` canlı |", "|---:|---|---:|"]
        for n in (8, 16, 24, 42):
            dilim = sorted(a)[-n:]
            L.append(f"| {n} | {dilim[0]}–{dilim[-1]} | "
                     f"**{sum(1 for i in dilim if 'v_proj' in a[i])}**/{n} |")
        L += ["",
              "➡️⭐⭐ *Anahtar «modelde yok» değil, **seçilen DİLİMDE yok**. Aynı anahtar*",
              "*`num_layers` büyüyünce sessizce **canlanır**. ⇒ «Bu anahtar ölü mü»*",
              "*sorusunun cevabı modele değil **config'in kendisine** bağlıdır ve her*",
              "*config için ayrı sorulmalıdır. K49 doğru olguyu yanlış sebeple yazmıştı*",
              "*ve o sebep, kapsam taramasında `num_layers` değişince yanıltıcı olurdu.*",
              "", "---", ""]

    # --- §2 config başına ------------------------------------------------------
    L += ["## 2. Config başına — hangi anahtar kaç modüle değiyor", "",
          "| config | `num_layers` | anahtar | canlı modül | |", "|---|---:|---|---:|---|"]
    olu = []
    for p, c in cfgler:
        a = agac.get(c["model"])
        lp = c["mlx"].get("lora_parameters", {}) or {}
        anahtarlar = lp.get("keys")
        n = c["mlx"].get("num_layers")
        if a is None:
            L.append(f"| `{p.stem}` | {n} | "
                     + (", ".join(f"`{k}`" for k in anahtarlar) if anahtarlar else "*varsayılan*")
                     + " | — | ⛔ model yok |")
            continue
        dilim = sorted(a)[-n:] if n else sorted(a)
        if not anahtarlar:
            L.append(f"| `{p.stem}` | {n} | *varsayılan* | — | ⚠️ mlx-lm varsayılanı |")
            continue
        for k in anahtarlar:
            ek = k.split(".", 1)[-1] if "." in k else k
            c_say = sum(1 for i in dilim if any(e == ek or e.endswith("." + ek)
                                                or e == k for e in a[i]))
            if c_say == 0:
                olu.append((p.stem, k, n))
            L.append(f"| `{p.stem}` | {n} | `{k}` | **{c_say}**/{len(dilim)} | "
                     f"{'⛔ **ÖLÜ**' if c_say == 0 else '✅'} |")
    L += ["",
          (f"⛔ **{len(olu)} config-anahtar çifti ÖLÜ:** "
           + ", ".join(f"`{a}` → `{b}` (num_layers={c})" for a, b, c in olu)
           if olu else "✅ **Ölü anahtar yok.**"), "",
          "⚠️ *Varsayılan* satırlar: config `keys` yazmıyor ve mlx-lm kendi varsayılanını",
          "kullanıyor — ⛔ o varsayılanın ne olduğu **burada sınanmadı** ve bu bir açık.", "",
          "## ⛔ Bu önkontrolün söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ **Parametre sayısı** | kaç modüle değdiği sayılıyor, kaç **parametre** "
          "eğitileceği değil; `rank` ve modül boyutu hesaba katılmadı |",
          "| ⛔ mlx-lm **varsayılan** anahtar kümesi | `keys` yazmayan config'lerde ne "
          "hedeflendiği sınanmadı |",
          "| ⧉ **Repo dışı bağımlılık** | model lokalde olmalı; yoksa satır `⛔ model yok` "
          "der ve **sessizce geçmez** |",
          "| ⚠️ `num_layers` semantiği | *«üstten N»* varsayımı mlx-lm davranışıdır; "
          "sürüm değişirse bu betik de yanılır |", ""]

    RAPOR.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print(f"   config {len(cfgler)} · model {len(modeller)} · lokalde {len(canli)}")
    print(f"   ⛔ ölü config-anahtar çifti: {len(olu)}" +
          (" -> " + ", ".join(f"{a}:{b}" for a, b, _ in olu) if olu else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
