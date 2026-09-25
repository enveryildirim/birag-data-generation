#!/usr/bin/env python3
"""Bir derleme girdisi kurar (varsayılan `v0.0.16`): v0.0.14 + bütün `v6` partileri.

⛔⛔ **KAPILAR TEK SÜRÜMDEN KOŞUYOR.** `v0.0.14.jsonl` kayıtları kendi
`_checks`'lerini 09-18'de aldı; o günden bu yana `checks.py` değişti.
İki ayrı denetim sürümünü aynı korpusa koymak, bu oturumun üç serisinin
de uyardığı şeydir (*«alan dolu ama iki dönem iki anlam»* — T240).
⇒ **`_checks` atılır ve 1107 kaydın tamamında BUGÜNKÜ `run_checks`
yeniden koşar.** Eskiden geçip şimdi düşen kayıt varsa RAPORLANIR.

⛔ **Judge karışıktır ve bu yazılı olmalıdır (K97).** `v6-parti1` ve
`v6-parti2` Gemini ile, `v6-parti3`–`parti8` Claude subagent ile puanlı;
`v0.0.14`'ün 577 kaydı kendi içinde zaten karışık (T176). Betik
`judge_model` dağılımını sayar ki veri kartına yazılabilsin.

⭐ `v6-parti3` için **`.claude.jsonl`** alınır: Gemini dosyasında 18 kayıt
`judge: null` ve `build.py` onları (haklı olarak, T121) eler. Claude
dosyasında 60/60 yargılı. Gemini dosyası YERİNDE KALIR.

⛔ Bu betik ELEME YAPMAZ; eleme `build.py`'nin işi.

Kullanım: uv run python <betik> [--surum=v0.0.16]
Çıktı: data/judged/<sürüm>.jsonl · reports/analiz/<tarih>-<sürüm>-girdi.md
"""
from __future__ import annotations

import collections
import hashlib
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from checks import run_checks  # noqa: E402
from dilim import dilim  # noqa: E402

TARIH = Path(__file__).name[:10]
# ⛔⛔ ÇIKTI PARAMETRELİ (T200: girdi parametreleşiyorsa çıktı da
# parametreleşmeli). `data/judged/v0.0.15.jsonl` `datasets/v0.0.15`'in
# kanıtıdır ve SHA256'sı manifest'te yazılı (Kural 7) ⇒ üzerine yazılmaz.
SURUM = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--surum=")),
             "v0.0.16")
CIKTI = KOK / f"data/judged/{SURUM}.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-{SURUM}-girdi.md"
KAYNAK = ["v0.0.14", "v6-parti1", "v6-parti2", "v6-parti3.claude",
          "v6-parti4.claude", "v6-parti5.claude", "v6-parti6.claude",
          "v6-parti7.claude", "v6-parti8.claude"]


def main() -> int:
    if CIKTI.exists():
        raise SystemExit(f"⛔ {CIKTI.name} zaten var — üzerine yazılmaz "
                         "(Kural 7). --surum= ile başka bir sürüm ver.")
    kayitlar, kaynagi, gorulen = [], {}, set()
    for ad in KAYNAK:
        yol = KOK / f"data/judged/{ad}.jsonl"
        n = 0
        for l in open(yol):
            r = json.loads(l)
            if r["id"] in gorulen:          # ⛔ mükerrer kayıt korpusa girmez
                raise SystemExit(f"⛔ mükerrer id: {r['id']} ({ad})")
            gorulen.add(r["id"])
            kayitlar.append(r)
            kaynagi[r["id"]] = ad
            n += 1
        print(f"  {ad:20s} {n:4d}")

    # ── kapılar tek sürümden ────────────────────────────────────────
    onceki = {r["id"]: bool((r.get("_checks") or {}).get("passed"))
              for r in kayitlar}
    dusen, dilim_duzeltilen = [], 0
    for r in kayitlar:
        r.pop("_checks", None)
        # ⛔⛔ T240: `slice` BEYAN DEĞİL TÜRETMEDİR. Anlık görüntü dosyaları
        # (v0.0.14.jsonl) eski sözlüğü taşıyor ve onlara dokunulmuyor (Kural 7)
        # ⇒ dilim birleştirme anında yeniden türetilir. Böylece hiçbir derleme
        # iki sözlüğü aynı korpusa koyamaz.
        yeni = dilim(r)
        if r.get("slice") != yeni:
            r["slice"] = yeni
            dilim_duzeltilen += 1
        chk = run_checks(r)
        r["_checks"] = chk
        if onceki[r["id"]] and not chk["passed"]:
            dusen.append((r["id"][:10], kaynagi[r["id"]],
                          [k for k, v in chk.items() if k.endswith("_error") and v][:2]))

    jm = collections.Counter(
        ((r.get("judge") or {}).get("judge_model") or
         ("replay" if r.get("replay") else "— (yargısız)")) for r in kayitlar)
    gecti = sum(1 for r in kayitlar if r["_checks"]["passed"])

    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n"
                             for r in kayitlar), encoding="utf-8")
    sha = hashlib.sha256(CIKTI.read_bytes()).hexdigest()[:16]

    sat = [f"# `{SURUM}` derleme girdisi", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Çıktı:** `data/judged/{SURUM}.jsonl` · SHA256 `{sha}`  ",
           f"**Kayıt:** {len(kayitlar)} · bugünkü `run_checks`'ten geçen "
           f"**{gecti}**  ", "",
           "## Kaynaklar", "", "| dosya | kayıt |", "|---|---:|"]
    sat += [f"| `{a}.jsonl` | {sum(1 for v in kaynagi.values() if v == a)} |"
            for a in KAYNAK]
    sat += ["", "⭐ `v6-parti3` için **`.claude.jsonl`** alındı: Gemini "
            "dosyasında 18 kayıt `judge: null` ve `build.py` onları eler "
            "(T121'in onarılmış kapısı). Gemini dosyası yerinde duruyor.", "",
            "## ⛔⛔ Judge karışımı (K97)", "", "| judge | kayıt |", "|---|---:|"]
    sat += [f"| `{k}` | {v} |" for k, v in jm.most_common()]
    sat += ["", "⛔⛔ **Bu korpus TEK BİR judge ile puanlanmamıştır** ve veri "
            "kartına böyle yazılmalıdır. K97: iki judge'ın sayıları aynı "
            "tabloya konmaz. ⭐ Aralarındaki köprü ölçüldü: "
            "`reports/analiz/2026-09-22-v6-kalan-judge.md` §B — sapma **tek "
            "yönlü değil** (`anlasilirlik` −0.86, `yorumlama` +0.38) ve iki "
            "boyut gürültünün içinde kalıyor.", "",
            "## ⭐ Kapılar tek sürümden koştu", "",
            f"`_checks` atıldı ve {len(kayitlar)} kaydın tamamında bugünkü "
            "`run_checks` yeniden koştu ⇒ korpusun tamamı **tek denetim "
            "sürümüyle** geçildi.", ""]
    if dusen:
        sat += [f"⛔ **Eskiden geçip şimdi düşen: {len(dusen)}**", "",
                "| kayıt | kaynak | ilk hata |", "|---|---|---|"]
        sat += [f"| `{i}` | `{k}` | {h} |" for i, k, h in dusen]
    else:
        sat += ["⭐ **Eskiden geçip şimdi düşen kayıt yok** ⇒ `checks.py`'nin "
                "09-18'den bu yana değişimi eski kayıtları etkilemedi."]
    sat += ["", "## ⛔ Bu adımın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **Eleme burada YAPILMADI** | karantina, `checks` düşüşü ve "
            "`klinik_guvenlik_ihlali` elemesi `build.py`'nin işi |",
            "| ⭐ **`slice` birleştirme anında TÜRETİLDİ** | T240 onarıldı: "
            f"{dilim_duzeltilen} kaydın dilimi `src/dilim.py`'den yeniden "
            "yazıldı ⇒ anlık görüntü dosyalarına dokunulmadan (Kural 7) "
            "korpus tek sözlükten geçiyor; `checks.py`'nin `dilim_ok` kapısı "
            "ayrışmayı bundan sonra eler |",
            "| ⚠️ **Judge karışımı bir KUSUR DEĞİL, bir KAYITTIR** | ama "
            "kartta yazılmazsa kusura dönüşür |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print(f"\n⭐ {len(kayitlar)} kayıt · checks geçen {gecti} · "
          f"eskiden geçip düşen {len(dusen)} · dilim türetmeyle düzelen "
          f"{dilim_duzeltilen}")
    print("judge:", dict(jm))
    print(f"→ {CIKTI.relative_to(KOK)} (SHA256 {sha})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
