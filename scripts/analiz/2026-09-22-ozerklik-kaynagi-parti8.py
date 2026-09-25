#!/usr/bin/env python3
"""`v6-parti8`'in `ozerklik_vurgusu` kaynağını kayda yazar (T235).

⛔⛔ **NEDEN.** T227-T230 `ozerklik_vurgusu`'nu parti1-7'nin 412 kaydında
uzlaştırmayla karara bağladı ve her kayda `gen_meta.ozerklik_kaynak`
yazdı. `v6-parti8` o turlardan SONRA üretildi; değerleri **desen + elle
onay** kuralından geliyor ve kaynak alanı BOŞ.

➡️⭐⭐ *Aynı alan, korpusun iki yarısında iki ayrı yoldan doldu ve bunu
söyleyen hiçbir şey yoktu. Bir alanın nereden geldiği kayıtta yazmıyorsa,
korpus büyüdükçe o alan sessizce iki anlama gelir.*

⭐ Bu betik parti8'in kayıtlarına kaynağını yazar. **Değerleri
DEĞİŞTİRMEZ** — yalnız nereden geldiklerini söyler.

⛔ Bu bir uzlaştırma DEĞİL: parti8 okunmadı, anotatöre verilmedi. Alanın
parti8'deki kesinliği parti1-7'dekiyle aynı DEĞİLDİR ve açık kalemdir.

Kullanım: uv run python ... [--yaz]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-ozerklik-kaynagi-parti8.md"
YAZ = "--yaz" in sys.argv
KAYNAK = "uretim-desen-veya-elle-onay"


def main() -> int:
    dosyalar = [KOK / "data/candidates/v6-parti8.jsonl"] + \
        sorted(KOK.glob("data/candidates/v6-parti8.blok*.jsonl"))
    n = yazilan = 0
    for y in dosyalar:
        kay = [json.loads(l) for l in y.read_text(encoding="utf-8").splitlines() if l.strip()]
        for r in kay:
            n += 1
            if not r["gen_meta"].get("ozerklik_kaynak"):
                r["gen_meta"]["ozerklik_kaynak"] = KAYNAK
                yazilan += 1
        if YAZ:
            y.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kay),
                         encoding="utf-8")

    # korpus dökümü
    dagilim: dict[str, int] = {}
    for i in range(1, 9):
        for l in (KOK / f"data/candidates/v6-parti{i}.jsonl").read_text(
                encoding="utf-8").splitlines():
            if l.strip():
                k = json.loads(l)["gen_meta"].get("ozerklik_kaynak") or "(boş)"
                dagilim[k] = dagilim.get(k, 0) + 1

    sat = ["# `ozerklik_vurgusu` alanının kaynağı — korpus dökümü", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Kip:** {'YAZILDI' if YAZ else 'kuru koşu'}  ", "",
           f"Dokunulan kayıt örneği: **{n}** · kaynağı yazılan: **{yazilan}**", "",
           "## Korpusta alan nereden geliyor", "", "| kaynak | kayıt |", "|---|---:|"]
    sat += [f"| `{k}` | {v} |" for k, v in sorted(dagilim.items(), key=lambda x: -x[1])]
    sat += ["", "⛔⛔ **İki kaynak AYNI KESİNLİKTE DEĞİL.** `T227`-`T230` kaynaklı "
            "412 kayıt iki ya da üç anotatörle okunup karara bağlandı; "
            f"`{KAYNAK}` kaynaklı 118 kayıt üretim kapısından geçti — desen "
            "gördü ya da ben elle onayladım, ama anotatöre verilmedi.", "",
            "⚠️ T228/T230'da ölçülmüştü: desen **fazla saymıyor** (%96 "
            "kesinlik) ama **az sayıyor** (işaretsiz kayıtların %16'sında "
            "özerklik vardı) ve elle onaylarımın %88'i tuttu. ⇒ parti8'in "
            "sayısı büyük olasılıkla bir **alt sınır**, tıpkı T228 öncesi "
            "parti1-7'nin olduğu gibi.", "",
            "## ⛔ Bu adımın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Bu bir uzlaştırma DEĞİL** | parti8 okunmadı, anotatöre "
            "verilmedi; yalnız alanın nereden geldiği yazıldı |",
            "| ⛔ **Değerler değişmedi** | tek yazılan şey `ozerklik_kaynak` |",
            "| ⚠️ **Açık kalem** | parti8 aynı yöntemle sayılırsa korpus oranı "
            "yeniden ölçülmeli |"]
    if YAZ:
        RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[:14]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
