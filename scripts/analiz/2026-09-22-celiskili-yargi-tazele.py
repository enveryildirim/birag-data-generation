#!/usr/bin/env python3
"""`celiskili` yargı dosyalarını ONARILMIŞ metin + TAZE yargıyla tazeler.

⛔⛔ **Neden gerekli.** `data/judged/celiskili-*.claude.jsonl` ilk yargı
koşusunun çıktısıdır ve **onarımdan önceki** metni taşır (T265). Üç kayıt
(#1, #6, #11) onarıldı ve **yeniden yargılandı** (T267); bu betik
onarılmış metni adaylardan, taze yargıyı da yeniden yargı koşularından
alıp yargı dosyasını **tutarlı** hâle getirir.

⛔ **Yargı seçimi açıktır:** bir kaydın birden çok yeniden yargısı varsa
**en son tur** alınır (#6 üç tur sürdü). Hangi turun alındığı rapora
yazılır — *«hangi sayıyı kullandığın yazılı olmalı»* (Kural 5).

⚠️ Yeniden yargı sonuçları **scratchpad**'de duruyor ve kalıcı değil;
bu betik onları **depoya** taşır. Bir daha koşulduğunda scratchpad boşsa
mevcut yargı korunur (bozmaz).

⛔ Bu betik ELEME YAPMAZ; eleme `build.py`'nin işi.

Çıktı: data/judged/celiskili-{pilot,parti2}.claude.jsonl (yerinde)
       reports/analiz/2026-09-22-celiskili-yargi-tazele.md
"""
from __future__ import annotations

import json
import os
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from checks import run_checks  # noqa: E402
from kunye import betik_tarihi  # noqa: E402

# ⭐ Parametreli (T200): hangi parti tazeleniyorsa o verilir.
_P = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--parti=")), "")
_T = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--turlar=")), "")
_AD = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--ad=")),
           "celiskili")
RAPOR = KOK / f"reports/analiz/2026-09-22-{_AD}-yargi-tazele.md"
CIFT = ([(f"data/candidates/{k}.jsonl", f"data/judged/{k}.claude.jsonl")
         for k in _P.split(",") if k.strip()]
        or [("data/candidates/celiskili-pilot.jsonl",
             "data/judged/celiskili-pilot.claude.jsonl"),
            ("data/candidates/celiskili-parti2.jsonl",
             "data/judged/celiskili-parti2.claude.jsonl")])
# ⭐ Sıra ÖNEMLİ: sonraki tur öncekini ezer.
TURLAR = ([x.strip() for x in _T.split(",") if x.strip()]
          or ["celiskili-onarim", "celiskili-onarim2", "celiskili-onarim3"])


def _turet():
    _argv0 = sys.argv[:]
    _y = KOK / "scripts/analiz/2026-09-15-judge-sonuclari-topla.py"
    sp = _iu.spec_from_file_location("_t15t", _y)
    mm = _iu.module_from_spec(sp)
    argv = sys.argv[:]
    sys.argv = [str(_y)]
    sp.loader.exec_module(mm)
    sys.argv = _argv0                # ⭐ argv korunur (iki kez ezilmişti)
    mm.JUDGE_ADI, mm.RUBRIK = "claude-sonnet-subagent", "judge-eksen1.v9"
    return mm.turet


def main() -> int:
    turet = _turet()
    scratch = os.environ.get("BIRAG_SCRATCH")
    taze: dict[str, tuple[str, dict]] = {}     # id → (tur adı, yargı)
    if scratch:
        B = Path(scratch) / "judge-isleri"
        for t in TURLAR:
            km = B / t / "kimlikler.json"
            if not km.exists():
                continue
            for k in json.loads(km.read_text()):
                if k.get("tekrar"):
                    continue
                y = B / t / "sonuc" / f"{k['no']}.json"
                if not y.exists():
                    continue
                h = y.read_text().strip()
                if h.startswith("```"):
                    h = h.split("```")[1].removeprefix("json").strip()
                taze[k["id"]] = (t, turet(json.loads(h)))

    satir, dusen = [], []
    for aday_yol, yargi_yol in CIFT:
        aday = [json.loads(l) for l in open(KOK / aday_yol)]
        eski = {}
        p_y = KOK / yargi_yol
        if p_y.exists():
            for l in open(p_y):
                r = json.loads(l)
                if r.get("judge"):
                    eski[r["id"]] = r["judge"]
        cikti = []
        for r in aday:
            no = r["gen_meta"].get("celiskili_banka_no")
            if r["id"] in taze:
                tur, j = taze[r["id"]]
            else:
                tur, j = "ilk yargı", eski.get(r["id"])
            r["judge"] = j
            # ⛔ Tazelenen metnin kapılardan geçtiği BURADA da doğrulanır.
            chk = run_checks(r)
            if not chk["passed"]:
                dusen.append((no, [f"{a}={v}" for a, v in chk.items()
                                   if a.endswith("_error") and v][:2]))
            cikti.append(r)
            satir.append((no, tur, (j or {}).get("grounding"),
                          (j or {}).get("klinik_guvenlik_ihlali"),
                          (j or {}).get("mi_uyumu")))
        if dusen:
            raise SystemExit(f"⛔ kapıdan düşen kayıt var, YAZILMADI: {dusen}")
        p_y.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n"
                               for x in cikti), encoding="utf-8")
        assert p_y.exists()

    n_ilk = sum(1 for _, t, _, _, _ in satir if t == "ilk yargı")
    yargisiz = [n for n, _, g, _, _ in satir if g is None]
    uydurma = [n for n, _, g, _, _ in satir if g == 2]
    kg = [n for n, _, _, k, _ in satir if k]

    s = [f"# `celiskili` yargı dosyaları tazelendi", "",
         f"**Betik:** `{Path(__file__).relative_to(KOK)}` · "
         f"**Tarih:** {betik_tarihi(__file__)}  ",
         f"**Kayıt:** {len(satir)} · yargısız {len(yargisiz)}  ", "",
         "⛔ Yargı dosyası ilk koşuda **onarımdan önceki** metni taşıyordu; "
         "bu betik onarılmış metni adaylardan, taze yargıyı yeniden yargı "
         "koşularından aldı.", "",
         "## Hangi kayıt hangi turdan", "",
         "| banka | yargı turu | `grounding` | `klinik_guvenlik_ihlali` | `mi_uyumu` |",
         "|---:|---|---:|---|---:|"]
    s += [f"| #{n} | {t} | {g} | {k} | {m} |"
          for n, t, g, k, m in sorted(satir)]
    s += ["", f"⭐ **`grounding == 2` (uydurma): {len(uydurma)}/{len(satir)}**"
          + (f" — #{uydurma}" if uydurma else " — sıfır"), "",
          f"⭐ **`klinik_guvenlik_ihlali`: {len(kg)}/{len(satir)}**"
          + (f" — #{kg}" if kg else " — sıfır (Kural 3 tarafı temiz)"), "",
          "⛔⛔ **Bu sayı T265'in %25'inin yerine GEÇMEZ.** T265 **onarımdan "
          "önceki** metni ölçtü ve o ölçüm korpus tasarımı hakkındaydı; bu "
          "tablo **onarılmış** metni gösterir. İkisini yan yana koyup "
          "*«uydurma %25'ten %0'a düştü»* demek **yanlış olur**: kayıtları "
          "uydurma bulunduğu için elle düzelttim, yani bu bir **müdahale "
          "sonrası** durumdur, üretimin kendi oranı değil.", "",
          "## ⛔ Bunun söylemedikleri", "", "| | |", "|---|---|",
          # ⛔⛔ K84: bu iki satır ELLE yazılmıştı («9 kayıt … 3 kayıt»,
          #   «#6 üç tur») ve betik başka bir partiye koşulunca yanlış
          #   basacaktı. Türetiliyor.
          f"| ⛔ **Turlar karışık** | {n_ilk} kayıt ilk yargıdan, "
          f"{len(satir)-n_ilk} kayıt yeniden yargıdan; aynı rubrik (v9) ve "
          "aynı yargıç ailesi ama **ayrı koşular** ⇒ koşular arası gürültü "
          "tabloya karışıyor |",
          f"| ⛔ **Birden çok tur** | bir kaydın birden çok yeniden yargısı "
          f"varsa **en son tur** alındı; bu koşuda taranan turlar: "
          f"{', '.join('`'+t+'`' for t in TURLAR)} |",
          "| ⛔ **Tek yargıç ailesi** | Gemini karşılaştırması yok (K97) |",
          "| ⛔ **Kayıtları ben yazdım, onarımı ben yaptım** | K30/K260 |"]

    RAPOR.write_text("\n".join(s) + "\n", encoding="utf-8")
    assert RAPOR.exists()
    print(f"⭐ {len(satir)} kayıt tazelendi · yargısız {len(yargisiz)}")
    print(f"   taze yargı alınan: {len(taze)} kayıt")
    print(f"   uydurma (grounding==2): {len(uydurma)} · klinik ihlal: {len(kg)}")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
