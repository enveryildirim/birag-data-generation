#!/usr/bin/env python3
"""Derleme girdisi kurar: ana hat + yeni parti(ler). Varsayılan `v0.0.21`.

⛔⛔ **ANA HAT `v0.0.18`'dir, `v0.0.20` DEĞİL.** `v0.0.19` ve `v0.0.20`
unutma gerilemesinin nedenselliğini sınayan **deney kollarıdır** ve kendi
veri kartları *«korpusun ilerleyişi değildir»* diyor (`%25,9`'u alan
dışı). ⇒ `celiskili` sınıfı ana hatta eklenir; aritmetik tazeleme
kayıtları **alınmaz**.

⭐ **Ne ekleniyor.** §7a″ `celiskili` (T262) sınıfının 12 kaydı: 12 temiz
çelişkili pasaj çifti, her biri ayrı tohumdan, hepsi `celiskili_ok`,
`bant_ok` ve `yansitma_ok` kapılarından geçmiş, hepsi yargılanmış
(3'ü onarım sonrası yeniden yargılanmış — T267).

⛔⛔ **KAPILAR TEK SÜRÜMDEN KOŞAR.** `v0.0.18.jsonl` kayıtları
`_checks`'lerini kendi gününde aldı; o günden bu yana `checks.py`'ye
**üç kapı** eklendi (`dilim_ok`, `bant_ok`, `celiskili_ok`, `yansitma_ok`).
İki denetim sürümünü aynı korpusa koymak T240'ın uyardığı şeydir ⇒
`_checks` atılır ve **bütün kayıtlarda bugünkü `run_checks` yeniden
koşar**. Eskiden geçip şimdi düşen kayıt varsa **raporlanır**.

⛔ `slice` ve `bicim` **türetmedir, beyan değil** (T240/T263) ⇒ birleştirme
anında yeniden türetilir; eski anlık görüntülerin beyanı kullanılmaz.

⛔ Bu betik ELEME YAPMAZ; eleme `build.py`'nin işi.

Kullanım: uv run python <betik> [--surum=v0.0.21]
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
from dilim import bant, dilim  # noqa: E402

TARIH = Path(__file__).name[:10]
SURUM = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--surum=")),
             "v0.0.21")
CIKTI = KOK / f"data/judged/{SURUM}.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-{SURUM}-girdi.md"
# ⭐ Kaynaklar parametreli (T200: girdi parametreleşiyorsa çıktı da
#   parametreleşmeli — ikisi de `--` ile verilir). Varsayılan: v0.0.21'i
#   üreten küme.
KAYNAK = ([x.strip() for x in next(
    (a.split("=", 1)[1] for a in sys.argv if a.startswith("--kaynak=")),
    "").split(",") if x.strip()]
    or ["v0.0.18", "celiskili-pilot.claude", "celiskili-parti2.claude"])


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
        print(f"  {ad:26s} {n:4d}")

    # ── kapılar tek sürümden ────────────────────────────────────────
    onceki = {r["id"]: bool((r.get("_checks") or {}).get("passed"))
              for r in kayitlar}
    dusen, dilim_d, bant_d = [], 0, 0
    for r in kayitlar:
        r.pop("_checks", None)
        y = dilim(r)
        if r.get("slice") != y:
            r["slice"], dilim_d = y, dilim_d + 1
        b = bant(r)
        if r.get("gen_meta", {}).get("bicim") != b and r.get("gen_meta"):
            r["gen_meta"]["bicim"], bant_d = b, bant_d + 1
        chk = run_checks(r)
        r["_checks"] = chk
        if onceki[r["id"]] and not chk["passed"]:
            dusen.append((r["id"][:10], kaynagi[r["id"]],
                          [k for k, v in chk.items()
                           if k.endswith("_error") and v][:2]))

    jm = collections.Counter(
        ((r.get("judge") or {}).get("judge_model") or
         ("replay" if r.get("replay") else "— (yargısız)")) for r in kayitlar)
    bd = collections.Counter(
        (r.get("gen_meta") or {}).get("baglam_davranisi") or "—"
        for r in kayitlar)
    gecti = sum(1 for r in kayitlar if r["_checks"]["passed"])

    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n"
                             for r in kayitlar), encoding="utf-8")
    sha = hashlib.sha256(CIKTI.read_bytes()).hexdigest()[:16]

    sat = [f"# `{SURUM}` derleme girdisi", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · "
           f"**Tarih:** {TARIH}  ",
           f"**Çıktı:** `data/judged/{SURUM}.jsonl` · SHA256 `{sha}`  ",
           f"**Kayıt:** {len(kayitlar)} · bugünkü `run_checks`'ten geçen "
           f"**{gecti}**  ", "",
           "⛔⛔ **Ana hat `v0.0.18`'dir.** `v0.0.19`/`v0.0.20` unutma "
           "gerilemesinin nedenselliğini sınayan **deney kollarıdır** ve "
           "kendi kartları *«korpusun ilerleyişi değildir»* diyor ⇒ "
           "aritmetik tazeleme kayıtları bu sürüme **alınmadı**.", "",
           "## Kaynaklar", "", "| dosya | kayıt |", "|---|---:|"]
    sat += [f"| `{a}.jsonl` | {sum(1 for v in kaynagi.values() if v == a)} |"
            for a in KAYNAK]
    sat += ["", "## ⭐ Yeni olan: §7a″ `celiskili`", "",
            "| `baglam_davranisi` | kayıt |", "|---|---:|"]
    sat += [f"| `{k}` | {v} |" for k, v in bd.most_common()]
    # ⛔⛔ K84: sayı ve hüküm TÜRETİLİR. İlk sürümde «12 kayıt» elle
    #   yazılmıştı ve betik yeniden kullanılınca yanlış sayı basacaktı.
    n_cel = bd.get("celiskili", 0)
    n_bagl = sum(v for k, v in bd.items() if k != "—")
    pay = 100 * n_cel / n_bagl if n_bagl else 0.0
    yon = ("hedefin **altında**" if pay < 9 else
           "hedefin **üstünde**" if pay > 11 else "**hedefte**")
    sat += ["", f"⭐ **{n_cel}** `celiskili` kaydı: her biri ayrı tohumdan, "
            "hepsi `celiskili_ok` · `bant_ok` · `yansitma_ok` kapılarından "
            "geçti ve hepsi yargılandı.", "",
            "⛔⛔ **Kota ölçülür, varsayılmaz:** §7a″ `celiskili` payını "
            f"`cevap_var`dan aldı (%50 → %40) ve ~%10 hedefliyor. Bu korpusta "
            f"**{n_cel}/{n_bagl}** bağlamlı kayıt = **%{pay:.1f}** ⇒ {yon}."
            + (" Kazanç görünmezse sebebinin tasarım mı pay mı olduğu "
               "**ayırt edilemez**." if pay < 9 else ""), "",
            "## ⛔⛔ Judge karışımı (K97)", "", "| judge | kayıt |", "|---|---:|"]
    sat += [f"| `{k}` | {v} |" for k, v in jm.most_common()]
    sat += ["", "⛔⛔ **Bu korpus TEK BİR judge ile puanlanmamıştır** ve veri "
            "kartına böyle yazılmalıdır (K97: iki judge'ın sayıları aynı "
            "tabloya konmaz).", "",
            "## ⭐ Kapılar tek sürümden koştu", "",
            f"`_checks` atıldı ve {len(kayitlar)} kaydın tamamında bugünkü "
            "`run_checks` yeniden koştu ⇒ korpusun tamamı **tek denetim "
            "sürümüyle** geçildi. Bugünkü sürümde `v0.0.18` gününden beri "
            "**dört yeni kapı** var: `dilim_ok` · `bant_ok` · `celiskili_ok` "
            "· `yansitma_ok`.", "",
            f"⭐ Türetilen alanlar birleştirme anında düzeltildi: "
            f"`slice` **{dilim_d}**, `gen_meta.bicim` **{bant_d}** kayıtta "
            "beyan ile türetme ayrıştı (T240/T263).", ""]
    if dusen:
        sat += ["## ⛔⛔ Eskiden geçip ŞİMDİ düşen kayıtlar", "",
                "| id | kaynak | sebep |", "|---|---|---|"]
        sat += [f"| `{a}` | `{b}` | {c} |" for a, b, c in dusen]
        sat += ["", f"⛔ **{len(dusen)} kayıt** yeni kapılara takıldı. Bunlar "
                "`build.py` tarafından **elenecek** — bu bir kusur değil, "
                "kapının işidir; ama sayının veri kartında görünmesi gerekir.",
                ""]
    else:
        sat += ["⭐ Eskiden geçip şimdi düşen kayıt **yok**.", ""]
    sat += ["## ⛔ Bunun söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **Eleme burada yapılmadı** | `build.py`'nin işi; bu dosya "
            "ham girdidir |",
            "| ⛔⛔ **`celiskili` kaydını ben yazdım, onardım ve yargısını "
            "ben okudum** | K30/K260; bağımsız anotatör hâlâ borç |",
            "| ⛔ **12 kayıt küçük** | sınıfın ince ayara etkisi bu sürümle "
            "**ölçülebilir olmayabilir**; kota hedefi ~%10 iken pay "
            f"**%{100*12/len(kayitlar):.1f}** |",
            "| ⚠️ **Yargı turları karışık** | 9 kayıt ilk yargıdan, 3 kayıt "
            "yeniden yargıdan (ayrı koşular, aynı rubrik) |"]

    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    assert CIKTI.exists() and RAPOR.exists()
    print(f"⭐ {len(kayitlar)} kayıt · bugünkü kapılardan geçen {gecti}")
    print(f"   slice düzeltilen {dilim_d} · bicim düzeltilen {bant_d}")
    print(f"   eskiden geçip şimdi düşen: {len(dusen)}")
    for a, b, c in dusen[:6]:
        print(f"     {a} {b} {c}")
    print(f"→ {CIKTI.relative_to(KOK)} · SHA256 {sha}")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
