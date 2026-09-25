#!/usr/bin/env python3
"""`gen_meta.date` betik adından mı geliyor — denetler ve `--duzelt` ile onarır.

⛔⛔ **Bulgu (T243).** Tarih üretim betiklerinde **elle yazılıyordu** ve bir
partiden ötekine kopyalanıyordu ⇒ `v6-parti5` (60 kayıt) ve `v6-parti8`
(118 kayıt) kendilerini üreten betiğin adındaki tarihten **bir gün önceyi**
taşıyor. Toplam **178 kayıt**.

⭐ **Kural yeni değil:** K126 raporlar için *«tarih betik ADINDAN»* diyor.
`src/kunye.py::betik_tarihi` aynı kuralı künyeye uyguluyor ve 48 üretim
betiği ona bağlandı ⇒ **kaynak kapatıldı**.

⭐ **Bu betik kalan yarıdır (K66):** *bir sınır yazıldığında ya onu uygulayan
kod ya da onu ÖLÇEN rapor satırı yazılır.* Kod yazıldı; bu, ölçendir. Geriye
dönük kayıtları da `--duzelt` ile onarır.

⛔ Denetim `checks.py`'ye KAPI olarak konulamaz: bir kaydın hangi betikten
geldiği kayıtta yazmıyor, yalnız **blok dosyası adından** çıkarılabiliyor
(`v6-parti8.blok1.jsonl` ↔ `2026-09-22-uretim-v6-parti8-blok1.py`).
⇒ Bu bağ boru hattı düzeyindedir, kayıt düzeyinde değil.

Kullanım: uv run python <betik> [--duzelt]
Çıktı: reports/analiz/2026-09-22-kunye-tarihi-denetimi.md
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-kunye-tarihi-denetimi.md"
DUZELT = "--duzelt" in sys.argv
BETIK = re.compile(r"^(\d{4}-\d{2}-\d{2})-uretim-(v\d+-parti\d+)-(blok\d+[a-z]*)")


def main() -> int:
    # blok -> betiğin adındaki tarih
    dogru = {}
    for s in sorted((KOK / "scripts/analiz").glob("*uretim-v*-parti*.py")):
        m = BETIK.match(s.name)
        if m:
            dogru[(m.group(2), m.group(3))] = m.group(1)

    # kayıt id -> doğru tarih
    id_tarih, blok_ozet = {}, []
    for (parti, blok), t in sorted(dogru.items()):
        f = KOK / f"data/candidates/{parti}.{blok}.jsonl"
        if not f.exists():
            continue
        c = collections.Counter()
        for l in open(f):
            r = json.loads(l)
            kd = (r.get("gen_meta") or {}).get("date")
            c[kd] += 1
            if kd != t:
                id_tarih[r["id"]] = t
        for kd, n in c.items():
            if kd != t:
                blok_ozet.append((parti, blok, t, kd, n))

    duzeltilen = 0
    if DUZELT and id_tarih:
        hedefler = sorted((KOK / "data/candidates").glob("*.jsonl")) + \
            sorted((KOK / "data/judged").glob("v*-parti*.jsonl"))
        for f in hedefler:
            satir = [json.loads(l) for l in open(f) if l.strip()]
            d = 0
            for r in satir:
                if r.get("id") in id_tarih and (r.get("gen_meta") or {}).get("date") \
                        != id_tarih[r["id"]]:
                    r["gen_meta"]["date"] = id_tarih[r["id"]]
                    d += 1
            if d:
                f.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n"
                                     for r in satir), encoding="utf-8")
                duzeltilen += d

    sat = ["# Künye tarihi denetimi — `gen_meta.date` betik adından mı", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Eşleşen blok:** {len(dogru)} · **uyuşmayan kayıt (benzersiz):** "
           f"{len(id_tarih)}  ",
           f"**Kip:** {'⭐ DÜZELTME' if DUZELT else 'yalnız denetim'}"
           + (f" — {duzeltilen} satır yazıldı  " if DUZELT else "  "), "",
           "⭐ Ölçüt: kaydın `gen_meta.date`'i, onu üreten blok betiğinin "
           "**adındaki** tarihe eşit olmalı (K126'nın künyeye uygulanışı).", ""]
    if blok_ozet:
        sat += ["## ⛔ Uyuşmayan bloklar", "",
                "| parti | blok | betik adı | kayıtta yazan | kayıt |",
                "|---|---|---|---|---:|"]
        sat += [f"| `{p}` | `{b}` | {t} | **{kd}** | {n} |"
                for p, b, t, kd, n in blok_ozet]
        sat += ["", "⭐⭐ **Mekanizma:** tarih blok betiğinde sabit yazılıydı ve "
                "bir sonraki partiye **kopyalandı**. Aynı sözlükte `parti` alanı "
                "da sabit yazılıydı, aynı kusuru üretti, yakalandı ve türetilir "
                "yapıldı; `date` **yanı başındaydı** ve düzeltilmedi. "
                "➡️ *Bir şablondaki bir beyanı türetmeye çevirmek, komşusunu "
                "düzeltmez.*", ""]
    else:
        sat += ["⭐ **Uyuşmazlık yok.** Bütün kayıtların künye tarihi, kendilerini "
                "üreten betiğin adıyla eşleşiyor.", ""]
    sat += ["## ⛔ Bu denetimin söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **Kapı DEĞİL, denetimdir** | bir kaydın hangi betikten geldiği "
            "kayıtta yazmıyor; bağ yalnız blok dosyası adından kuruluyor ⇒ "
            "`checks.py`'ye kayıt düzeyli kapı olarak konulamaz |",
            "| ⛔ **Betik adı da bir BEYANDIR** | yalnız daha dayanıklı bir "
            "beyan: dosya adı commit'te görünür ve K126 onu zaten ölçüt "
            "saymıştı. Gerçek üretim anını ölçen şey **git zaman damgasıdır** "
            "ve bu denetim onu kullanmıyor |",
            "| ⚠️ **`datasets/` düzeltilmez** | IMMUTABLE; `v0.0.15` ve "
            "`v0.0.16` eski tarihleri taşımayı sürdürür |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print(f"uyuşmayan benzersiz kayıt: {len(id_tarih)}"
          + (f" · düzeltilen satır: {duzeltilen}" if DUZELT else ""))
    for p, b, t, kd, n in blok_ozet:
        print(f"  {p}.{b}: betik {t} · kayıt {kd} ({n})")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
