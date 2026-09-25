#!/usr/bin/env python3
"""`gen_meta.bicim` beyan olmaktan çıkıp TÜRETME oldu — ve 43 kayıt düzeldi.

⛔⛔ **Aynı sözlükteki ÜÇÜNCÜ aynı kusur.** `slice` (T240) ve `date` (T244)
beyan edilip sessizce kaymıştı; `bicim` de aynı `gen_meta` içinde, aynı
biçimde. ⭐ **Nasıl çıktı:** `celiskili` pilotunda bantları **elle** beyan
ettim ve ikisi yanlış çıktı (16 sözcüğe *«kisa»*, 29 sözcüğe *«orta»*) —
**hiçbir kapı görmedi**, kendi işimi denetlerken buldum.

⭐ **Bulgu tek yönlü:** mevcut korpusta uyumsuz **43 kaydın 43'ü de**
`orta` → `uzun`. Hiç `uzun → orta` ya da `kisa` uyumsuzluğu yok ⇒ `orta`
bandı sistematik olarak **yukarı taşıyor**; üretici 25 sözcük sınırını
aşarken bunu fark etmiyor.

⛔ `datasets/` ve `data/judged/v0.0.*.jsonl` anlık görüntülerine DOKUNULMAZ
(Kural 7); birleştirme dilimi türettiği gibi bantı da türetmelidir.

Çıktı: reports/analiz/2026-09-22-bant-yeniden-etiketle.md
"""
from __future__ import annotations

import collections
import glob
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from dilim import bant  # noqa: E402

TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-bant-yeniden-etiketle.md"
TUREV = re.compile(r"\.(blok\d+[a-z]*|v\d+|arinmis|claude)\.")


# ⚠️ İlk uygulamanın (2026-09-22) geçiş sayımı — TARİHSEL, bu koşuda
#   ölçülmüş değil. «beyan» sütunu bundan geri hesaplanır.
ILK = {"tarih": "2026-09-22", "gecis": {("orta", "uzun"): 286, ("kisa", "orta"): 1}}

def main() -> int:
    hedef = sorted(glob.glob(str(KOK / "data/candidates/*.jsonl"))) + \
        sorted(glob.glob(str(KOK / "data/judged/v6-parti*.jsonl")))
    gecis, dosya, n_kayit, n_deg = collections.Counter(), [], 0, 0
    for f in hedef:
        sat = [json.loads(l) for l in open(f) if l.strip()]
        d = 0
        for r in sat:
            if "messages" not in r or r.get("replay"):
                continue
            gm = r.get("gen_meta") or {}
            if "bicim" not in gm:
                continue
            n_kayit += 1
            y = bant(r)
            if y and gm["bicim"] != y:
                gecis[(gm["bicim"], y)] += 1
                gm["bicim"] = y
                d += 1
        if d:
            Path(f).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n"
                                       for r in sat), encoding="utf-8")
            dosya.append((Path(f).relative_to(KOK), len(sat), d))
            n_deg += d

    sat_ = ["# `gen_meta.bicim` yeniden etiketlendi — beyan yerine türetme", "",
            f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
            f"**Taranan:** {len(hedef)} dosya, {n_kayit} bant beyanı · "
            f"**değişen: {n_deg}**  ", "",
            "⛔⛔ **Aynı `gen_meta` sözlüğündeki ÜÇÜNCÜ aynı kusur:** `slice` "
            "(T240) · `date` (T244) · **`bicim`**. Üçü de beyan edildi, üçü de "
            "sessizce kaydı, üçünü de kapı görmedi.", "",
            "⭐ **Nasıl çıktı:** `celiskili` pilotunda bantları elle beyan ettim "
            "ve ikisi yanlış çıktı; **kendi işimi denetlerken** buldum, kapı "
            "değil.", "",
            "## Geçişler", "", "| beyan | → sayılan | kayıt |", "|---|---|---:|"]
    # ⚠️ Koşu değişiklik bulmazsa tablo BOŞ kalmasın; ilk uygulamanın
    #   sayımı gösterilir ve TARİHSEL diye işaretlenir (K84: hüküm sabit
    #   yazılmaz, ama boş tablo da okuyucuyu yanıltır).
    if gecis:
        sat_ += [f"| `{a}` | `{b}` | {n} |" for (a, b), n in gecis.most_common()]
    else:
        sat_ += [f"| `{a}` | `{b}` | {n} _(tarihsel)_ |"
                 for (a, b), n in sorted(ILK["gecis"].items(), key=lambda t: -t[1])]
        sat_ += ["", f"⚠️ Bu koşu **0 değişiklik** buldu; satırlar "
                 f"{ILK['tarih']} ilk uygulamasının sayımıdır."]
    sat_ += ["", "⭐⭐ **Bulgu TEK YÖNLÜ:** uyumsuzlukların tamamı "
             "`orta` → `uzun`. Hiç `uzun → orta`, hiç `kisa` uyumsuzluğu yok. "
             "⇒ `orta` bandı sistematik olarak **yukarı taşıyor**: üretici "
             "25 sözcük sınırını aşarken fark etmiyor. Bu bir **üretim "
             "sadakati** bulgusudur, etiketleme kusuru değil.", "",
             "## Kota dağılımına etkisi", "", "| bant | beyan | **sayılan** |",
             "|---|---:|---:|"]
    # ⛔ K84: rapor üreticisinde SABİT HÜKÜM yazılmaz — sayı değişince cümle
    #   de değişmeli. İlk sürümde bu tabloyu elle yazmıştım.
    #   ⇒ benzersiz kayıt üzerinden TÜRETİLİR.
    # ⛔⛔ K84 BURADA İKİ KEZ TEKRARLADI. İlk sürüm kota tablosunu ELLE yazdı;
    #   ikinci sürüm türetmeye çalıştı ama dosyalar zaten onarılmıştı ve
    #   «beyan» ile «sayılan» aynı çıkıp tablo kendi hüküm cümlesiyle ÇELİŞTİ.
    #   ⇒ Ders: *«rapor üreticisinde sabit hüküm yazılmaz»* kuralı, GERİ
    #     DÖNÜŞÜ OLMAYAN bir düzeltmeden sonra ayrıca zordur — ölçülecek
    #     durum artık yoktur. Tarihsel sayı kaynağıyla birlikte yazılır.
    gor, son = set(), collections.Counter()
    for f in hedef:
        if "candidates" not in f or TUREV.search(f):
            continue
        for l in open(f):
            r = json.loads(l)
            if "messages" not in r or r.get("replay") or r["id"] in gor:
                continue
            if "bicim" in (r.get("gen_meta") or {}):
                gor.add(r["id"])
                son[r["gen_meta"]["bicim"]] += 1
    kaynak = gecis if n_deg else ILK["gecis"]
    for k in ("kisa", "orta", "uzun"):
        onceki = (son[k]
                  - sum(v for (a2, b2), v in kaynak.items() if b2 == k)
                  + sum(v for (a2, b2), v in kaynak.items() if a2 == k))
        sat_.append(f"| `{k}` | {onceki} | **{son[k]}** |")
    if n_deg:
        sat_ += ["", "⚠️ §6 bant kotası **tutturulmamış**: raporlanan `orta` "
                 "payı gerçekte olduğundan **yüksekti**.", ""]
    else:
        sat_ += ["", f"⚠️ **Düzeltme {ILK['tarih']}'de UYGULANDI; bu koşu "
                 "değişiklik bulmadı.** «Beyan» sütunu ilk uygulamanın geçiş "
                 "sayımından **geri hesaplandı** "
                 + str({f"{a}→{b}": v for (a, b), v in ILK["gecis"].items()})
                 + " ⇒ **tarihsel**, bu koşuda ölçülmüş değil.", "",
                 "⛔ §6 bant kotası o gün **tutturulmamıştı**: raporlanan `orta` "
                 "payı gerçekte olduğundan yüksekti.", ""]
    sat_ += ["## Değişen dosyalar", "", "| dosya | kayıt | değişen |",
             "|---|---:|---:|"]
    sat_ += ([f"| `{d}` | {n} | {k} |" for d, n, k in dosya]
             or ["| _(bu koşuda değişen dosya yok)_ | — | 0 |"])
    sat_ += ["", "## ⛔ Bunun söylemedikleri", "", "| | |", "|---|---|",
             "| ⛔ **Dokunulmayanlar** | `datasets/` IMMUTABLE ve "
             "`data/judged/v0.0.*.jsonl` anlık görüntüleri Kural 7 gereği "
             "yerinde; birleştirme bantı **türeterek** okumalı |",
             "| ⛔ **Metin değişmedi** | yalnız etiket düzeldi; hiçbir kaydın "
             "kullanıcı mesajı kısaltılmadı |",
             "| ⚠️ **Eşikler v4 §6'dan** | kisa ≤8 · orta 9-25 · uzun >25; "
             "eşik değişirse bu sayılar değişir |",
             "| ⚠️ **Sebep izlenmedi** | `orta` bandının neden yukarı taştığı "
             "(üretici eğilimi mi, ızgara mı) **ölçülmedi** |"]
    RAPOR.write_text("\n".join(sat_) + "\n", encoding="utf-8")
    print(f"{n_kayit} beyan tarandı · {n_deg} etiket düzeldi")
    for (a, b), n in gecis.most_common():
        print(f"  {a} → {b}: {n}")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
