#!/usr/bin/env python3
"""`slice` alanını `src/dilim.py`'den TÜRETİP kayıtlara yazar (T240 onarımı).

⭐ Kullanıcı kararı (2026-09-22): *«slice'ı context'ten türet»*.

⛔ **DOKUNULMAYANLAR:**
  · `datasets/` — IMMUTABLE (Kural 4). `v0.0.15` eski etiketlerle kaldı.
  · `data/judged/v0.0.*.jsonl` — derleme girdisi anlık görüntüleri; SHA256'ları
    manifest'lerde yazılı (Kural 7). Bir sonraki derleme bunları okumaz,
    dilimi **birleştirme anında yeniden türetir**.
  · `data/seeds*.jsonl` — IMMUTABLE.

⭐ Dokunulanlar: `data/candidates/` konuşma taşıyan dosyalar ve
`data/judged/v6-parti*.jsonl` (canlı yargı katmanı).

Çıktı: reports/analiz/2026-09-22-slice-yeniden-etiketle.md
"""
from __future__ import annotations

import collections
import glob
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from dilim import dilim  # noqa: E402

TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-slice-yeniden-etiketle.md"


def main() -> int:
    hedefler = sorted(glob.glob(str(KOK / "data/candidates/*.jsonl"))) + \
        sorted(glob.glob(str(KOK / "data/judged/v6-parti*.jsonl")))
    degisim = collections.Counter()
    dosya_ozet, n_kayit, n_degisen = [], 0, 0

    for f in hedefler:
        satirlar = [json.loads(l) for l in open(f) if l.strip()]
        d = 0
        for r in satirlar:
            if "messages" not in r:
                continue
            n_kayit += 1
            yeni = dilim(r)
            if r.get("slice") != yeni:
                degisim[(r.get("slice"), yeni)] += 1
                r["slice"] = yeni
                d += 1
        if d:
            Path(f).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n"
                                       for r in satirlar), encoding="utf-8")
            dosya_ozet.append((Path(f).relative_to(KOK), len(satirlar), d))
            n_degisen += d

    sat = ["# `slice` yeniden etiketlendi — beyan yerine türetme", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Taranan:** {len(hedefler)} dosya, {n_kayit} kayıt · "
           f"**değişen: {n_degisen}**  ", "",
           "⭐ Kullanıcı kararı: *«slice'ı context'ten türet»* (T240). Alan "
           "artık `src/dilim.py`'de **tek bir yerden** türer: kip `context`'in "
           "doluluğundan, tur sayısı `messages`'taki `user` turlarından, "
           "`replay` ise kaydın kendi bayrağından.", "",
           "## Ne değişti", "", "| beyan | → türetilen | kayıt |", "|---|---|---:|"]
    for (a, b), v in sorted(degisim.items(), key=lambda x: -x[1]):
        sat.append(f"| `{a}` | `{b}` | {v} |")
    sat += ["", "⭐⭐ **En büyük iki kalem v6'nın sözlük kaymasıdır:** "
            "`rag_tek_tur` → `terapotik_tek_tur` ve `cok_tur` → "
            "`terapotik_cok_tur`. İkisi de aynı şeyi söylüyor: v6 kayıtları "
            "**bağlamı olmadığı hâlde RAG etiketi taşıyordu** ya da kipi hiç "
            "taşımıyordu.", "",
            "⭐ **Bir kalem v6'dan değil:** `terapotik_tek_tur` → "
            "`terapotik_cok_tur`, **1 kayıt** (`v4-parti1 / d001bc7a8f`). Bu "
            "**K69**'un belgelenmiş kusuru — `kayit()`'in varsayılanı çok "
            "turlu bir kaydı tek tur diye damgalamıştı. ⇒ Türetme, K69'u "
            "aramadan buldu.", "",
            "## Değişen dosyalar", "", "| dosya | kayıt | değişen |", "|---|---:|---:|"]
    sat += [f"| `{d}` | {n} | {k} |" for d, n, k in dosya_ozet]
    sat += ["", "## ⛔ Dokunulmayanlar", "", "| | |", "|---|---|",
            "| `datasets/` | IMMUTABLE (Kural 4) ⇒ **`v0.0.15` eski "
            "etiketlerle kaldı**; kartı zaten `slice` dağılımı yazmıyor ve "
            "nedenini açıklıyor |",
            "| `data/judged/v0.0.*.jsonl` | derleme girdisi anlık "
            "görüntüleri; SHA256'ları manifest'lerde yazılı (Kural 7) ⇒ bir "
            "sonraki derleme bunları okumaz, dilimi **birleştirme anında "
            "yeniden türetir** |",
            "| `data/seeds*.jsonl` | IMMUTABLE |", "",
            "## ⭐ Artık bir kapı var", "",
            "`src/checks.py` beyan ile türetileni karşılaştırır "
            "(`dilim_ok`) ve ayrışırsa kayıt **düşer**. ⛔ Bu, T237'nin "
            "dersinin uygulanmasıdır: *bir sınır yazıldığında aynı commit'te "
            "onu uygulayan kod da yazılır.* Kapı ancak biri dilimi **elle** "
            "yazarsa ateşler — çünkü üretim ve birleştirme artık türetiyor.", "",
            "## ⛔ Bunun söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **Yayımlanmış kartlar geriye dönük düzelmedi** | `v0.0.5`–"
            "`v0.0.11` v5 sözlüğüyle derlendi ve o sözlükte sayıları "
            "**doğruydu**; `v0.0.15` ise `slice` dağılımını hiç yazmıyor |",
            "| ⚠️ **Türetme bir TANIM seçimidir** | *«bağlamı olan kayıt "
            "RAG'dir»* denildi; bağlamı olup da cevabı bağlamı kullanmayan "
            "kayıt da RAG sayılır. Başka bir tanım (*«cevap bağlamı "
            "KULLANIYOR mu»*) ölçülmedi ve daha zordur |",
            "| ⚠️ **`cok_tur` bağlamlı 21 kayıt** | yeni sözlükte "
            "`rag_cok_tur` oldular; v6'da bu birleşim hiç adlandırılmamıştı |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print(f"{n_kayit} kayıt tarandı · {n_degisen} etiket değişti")
    for (a, b), v in sorted(degisim.items(), key=lambda x: -x[1]):
        print(f"  {a} → {b}: {v}")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
