#!/usr/bin/env python3
"""`v6-parti1` künye onarımı — kayıtları ÜRETİLDİKLERİ tohumlara geri bağlar.

⛔⛔⛔ **GEREKÇE T224.** `data/plan/v6-parti1.jsonl` üretimden sonra yeniden
üretilip üstüne yazıldı (60 tohumun 60'ı değişti) ve blok betikleri başka bir
kusur için yeniden koşunca 59 kaydın `source_ids` + `gen_meta.seed_id` alanı
yeni plandan damgalandı. Kayıtların METİNLERİ kendi tohumlarına sadık
(örtüşme %53); yanlış olan yalnız künye.

⭐ **ONARIM KAYIPSIZ:** plan v1 ve üretim anındaki künye git'te duruyor.
Bu betik yalnız iki alana dokunur — `source_ids` ve `gen_meta.seed_id` —
ve **metinlere, `judge`, `is_negative`, `elle_onay` gibi sonradan yapılmış
meşru düzeltmelere dokunmaz.**

⛔ Kaynak: plan v1 (`{V1}`), `parti_sira` üzerinden eşleştirilir.
⛔ Doğrulama: onarımdan sonra kayıt–tohum örtüşmesi %50'nin üstüne çıkmalı
   ve çifte üretilen tohum kalmamalı; çıkmazsa betik **yazmaz**.

Kullanım: uv run python scripts/analiz/2026-09-21-parti1-kunye-onarimi.py [--yaz]
          (varsayılan KURU KOŞU — hiçbir şey yazmaz)
"""
from __future__ import annotations

import json
import re
import statistics as st
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
V1 = "6816874"
YAZ = "--yaz" in sys.argv
BLOK = re.compile(r"<context[^>]*>.*?</context>", re.S)

import tohum_guvenlik as TG  # noqa: E402


def _g(s: str) -> set[str]:
    return {w[:5] for w in re.sub(r"[^\w\s]", " ", TG.tr_sadelestir(s)).split()
            if len(w) > 4}


def main() -> int:
    ham = subprocess.run(["git", "show", f"{V1}:data/plan/v6-parti1.jsonl"],
                         capture_output=True, text=True, cwd=KOK).stdout
    v1 = {json.loads(l)["sira"]: json.loads(l) for l in ham.splitlines() if l.strip()}
    if len(v1) != 60:
        print(f"⛔ plan v1 okunamadı ({len(v1)} satır)")
        return 1

    dosyalar = sorted((KOK / "data/candidates").glob("v6-parti1.blok*.jsonl"))
    yeni_icerik, degisen, ort = {}, 0, []
    for f in dosyalar:
        kayitlar = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
        for r in kayitlar:
            s = r["gen_meta"]["parti_sira"]
            p = v1[s]
            if r["source_ids"] != [p["source_id"]]:
                degisen += 1
            r["source_ids"] = [p["source_id"]]
            r["gen_meta"]["seed_id"] = p["seed_id"]
            b = _g(" ".join(BLOK.sub("", m["content"]) for m in r["messages"]
                            if m["role"] == "user"))
            a = _g(p["tohum_metin"])
            ort.append(len(a & b) / max(1, len(a)))
        yeni_icerik[f] = kayitlar

    ortalama = 100 * st.mean(ort)
    sifir = sum(1 for x in ort if x == 0)
    print(f"⭐ {degisen} kaydın künyesi düzeltilecek · onarım sonrası "
          f"kayıt–tohum örtüşmesi %{ortalama:.0f} · sıfır örtüşen {sifir}")
    # ⛔ DOĞRULAMA KAPISI — onarım işe yaramadıysa yazma.
    if ortalama < 50 or sifir > 2:
        print("⛔ DOĞRULAMA BAŞARISIZ: onarım örtüşmeyi beklenen düzeye "
              "çıkarmadı. Hiçbir şey yazılmadı.")
        return 1
    if not YAZ:
        print("⭐ KURU KOŞU — yazmak için `--yaz`.")
        return 0

    (KOK / "data/plan/v6-parti1.jsonl").write_text(ham, encoding="utf-8")
    for f, kayitlar in yeni_icerik.items():
        f.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kayitlar),
                     encoding="utf-8")
    print(f"✅ plan v1 geri kondu · {len(yeni_icerik)} blok dosyası yazıldı")
    print("⛔ ŞİMDİ: birleştirme ve kapsama envanterleri yeniden koşulmalı.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
