#!/usr/bin/env python3
"""Subagent judge sonuçlarını toplar, partilere yazar ve İKİ KALİBRASYON koşar.

⭐ **Türetme KOPYALANMIYOR (K103):** `turet()` 09-15 toplama betiğinden
import edilir — `anlasilirlik`/`dogallik`/`mi_uyumu`/`tuzak_ihlali` ve F
bölümünün bayrakları judge'dan GELMEZ, `filter.py` hesaplar. Aynı
fonksiyonlardan geçmezse Gemini karşılaştırması rubrik farkını değil
**hesap farkını** ölçer.

⛔⛔ **Çıktı dosyasının ADINDA judge var** (`.claude.jsonl`). Gemini
dosyaları YERİNDE KALIR, üzerine yazılmaz (Kural 7). ⭐ Bu, T236 serisinin
dersinin uygulanması: *değeri değil kaynağı denetle* — kaynak burada
dosya adında.

İki kalibrasyon:
  **A. GÜRÜLTÜ TABANI** — 24 kayıt aynı dalgada iki ayrı numarayla, ayrı
     öbeklerde soruldu. ⛔ K98 tabanı **v6** rubriğiyle ölçmüştü; bu koşu
     **v9** ⇒ eski taban geçerli değil.
  **B. CLAUDE ↔ GEMINI** — `v6-parti3`'ün 42 kaydı iki judge'ın ikisinde
     de var. ⛔⛔ Fark ancak **A'daki tabandan büyükse** okunabilir; K98
     tam bu yüzden K97'nin iki sapma sayısını geçersiz kılmıştı.

Kullanım: BIRAG_SCRATCH=... uv run python <betik>
Çıktı: data/judged/v6-partiN.claude.jsonl · reports/analiz/<tarih>-...md
"""
from __future__ import annotations

import collections
import json
import os
import statistics as st
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-v6-kalan-judge.md"

_yol = KOK / "scripts/analiz/2026-09-15-judge-sonuclari-topla.py"
_spec = _iu.spec_from_file_location("_topla15", _yol)
_t15 = _iu.module_from_spec(_spec)
sys.argv = [str(_yol)]
_spec.loader.exec_module(_t15)
_t15.JUDGE_ADI = "claude-sonnet-subagent"
_t15.RUBRIK = "judge-eksen1.v9"
turet = _t15.turet

DIZIN = Path(os.environ["BIRAG_SCRATCH"]) / "judge-isleri/v6-kalan"
BOYUT = ["duygusal_tepki", "yorumlama", "kesif", "mi_uyumu", "grounding",
         "anlasilirlik", "dogallik"]
# ⛔ K98'in v6 tabanı — yalnız KARŞILAŞTIRMA için, bu koşuya uygulanmaz.
K98_V6 = {"grounding": 100, "mi_uyumu": 100, "kesif": 91, "dogallik": 91,
          "duygusal_tepki": 70, "yorumlama": 65, "anlasilirlik": 43}


def oku(no: str):
    y = DIZIN / "sonuc" / f"{no}.json"
    if not y.exists():
        return None
    ham = y.read_text().strip()
    if ham.startswith("```"):
        ham = ham.split("```")[1].removeprefix("json").strip()
    try:
        return turet(json.loads(ham))
    except Exception as e:
        return {"_hata": f"{type(e).__name__}: {e}"[:140]}


def main() -> int:
    kim = json.loads((DIZIN / "kimlikler.json").read_text())
    birincil = [k for k in kim if not k["tekrar"]]
    tekrarlar = [k for k in kim if k["tekrar"]]

    yargi, bozuk, eksik = {}, [], []
    for k in birincil:
        r = oku(k["no"])
        if r is None:
            eksik.append(k["no"])
        elif "_hata" in r:
            bozuk.append((k["no"], r["_hata"]))
        else:
            yargi[k["id"]] = r

    # ── partilere yaz ───────────────────────────────────────────────
    parti_of = {k["id"]: k["parti"] for k in birincil}
    yazilan = {}
    for parti in sorted(set(parti_of.values())):
        aday = [json.loads(l) for l in open(KOK / f"data/candidates/{parti}.jsonl")]
        n = 0
        for r in aday:
            if not r.get("replay") and r["id"] in yargi:
                r["judge"] = yargi[r["id"]]
                n += 1
            else:
                r.setdefault("judge", None)
        hedef = KOK / f"data/judged/{parti}.claude.jsonl"
        hedef.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in aday),
                         encoding="utf-8")
        yazilan[parti] = (n, len(aday))

    # ── A. gürültü tabanı ───────────────────────────────────────────
    taban, tfark = {}, {}
    ciftler = []
    for k in tekrarlar:
        a, b = oku(k["no"]), yargi.get(k["id"])
        if a and "_hata" not in a and b:
            ciftler.append((a, b))
    for d in BOYUT:
        p = [(a[d], b[d]) for a, b in ciftler
             if a.get(d) is not None and b.get(d) is not None]
        if p:
            taban[d] = round(100 * sum(x == y for x, y in p) / len(p))
            tfark[d] = round(st.mean(abs(x - y) for x, y in p), 2)

    # ── B. Claude ↔ Gemini (eşli) ───────────────────────────────────
    gem = {}
    gy = KOK / "data/judged/v6-parti3.jsonl"
    if gy.exists():
        for l in open(gy):
            r = json.loads(l)
            if r.get("judge"):
                gem[r["id"]] = r["judge"]
    esli = [(yargi[i], gem[i]) for i in gem if i in yargi]
    fark, uyum, mutlak = {}, {}, {}
    for d in BOYUT:
        p = [(c[d], g[d]) for c, g in esli
             if c.get(d) is not None and g.get(d) is not None]
        if p:
            fark[d] = round(st.mean(c - g for c, g in p), 2)
            uyum[d] = round(100 * sum(c == g for c, g in p) / len(p))
            mutlak[d] = round(st.mean(abs(c - g) for c, g in p), 2)
    kg_c = sum(1 for c, _ in esli if c.get("klinik_guvenlik_ihlali"))
    kg_g = sum(1 for _, g in esli if g.get("klinik_guvenlik_ihlali"))

    sat = [f"# `v6` kalan partiler — subagent judge koşusu", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Judge:** `claude-sonnet-subagent` · **Rubrik:** `judge-eksen1.v9`  ",
           f"**Toplandı:** {len(yargi)}/{len(birincil)} · eksik {len(eksik)} · "
           f"bozuk {len(bozuk)}  ", "",
           "⛔ **Bu koşu K43/K45'i çiğnemiyor, K97'yi uyguluyor:** judge "
           "Claude subagent'lara **09-15'te kullanıcı kararıyla** taşınmıştı, "
           "aynı gerekçeyle (Gemini kotası) ve iki şartla — körlük ve "
           "ölçülebilirlik. İkisi de bu koşuda yerinde.", "",
           "## Partilere yazılanlar", "",
           "⛔ Gemini dosyaları **yerinde duruyor**; Claude yargıları ayrı "
           "dosyaya yazıldı ve judge **dosya adında**.", "",
           "| parti | yargılanan | dosya |", "|---|---:|---|"]
    for p, (n, t) in yazilan.items():
        sat.append(f"| `{p}` | {n}/{t} | `data/judged/{p}.claude.jsonl` |")

    sat += ["", "## ⭐ A. Bu dalganın gürültü tabanı (v9)", "",
            f"{len(ciftler)} kayıt aynı dalgada **iki ayrı numarayla**, ayrı "
            "öbeklerde soruldu. ⛔ K98'in tabanı **v6** rubriğiyle ölçülmüştü; "
            "aşağıdaki sütun yalnız karşılaştırma için.", "",
            "| boyut | birebir uyum | ort. \\|fark\\| | (K98, v6) |", "|---|---:|---:|---:|"]
    for d in BOYUT:
        if d in taban:
            sat.append(f"| `{d}` | %{taban[d]} | {tfark[d]} | %{K98_V6.get(d, '—')} |")

    sat += ["", "## ⭐⭐ B. Claude ↔ Gemini — aynı 42 kayıt", "",
            f"`v6-parti3`'ün **{len(esli)}** kaydı iki judge'ın ikisinde de "
            "var. ⛔⛔ Bir fark ancak **A'daki tabandan büyükse** okunabilir.", "",
            "⭐ **Ölçüt (K98):** judge KENDİSİYLE ne kadar anlaşıyorsa, iki "
            "judge arasındaki fark ancak ondan **daha büyükse** sapmadır. "
            "Kendiyle olan farktan küçük bir çapraz fark, sapma değil "
            "**oynaklık** ölçer — K98 K97'nin iki sayısını tam bunun için "
            "geçersiz kılmıştı.", "",
            r"| boyut | Claude−Gemini | çapraz \|fark\| | kendiyle \|fark\| (A) | okunabilir mi |",
            "|---|---:|---:|---:|---|"]
    for d in BOYUT:
        if d in fark:
            t = tfark.get(d)
            if t is None:
                ok = "⚠️ taban ölçülemedi"
            elif mutlak[d] > t:
                ok = "⭐ **evet** — çapraz fark tabanı aşıyor"
            else:
                ok = "⛔ **HAYIR** — fark gürültünün içinde"
            sat.append(f"| `{d}` | {fark[d]:+.2f} | {mutlak[d]} | "
                       f"{t if t is not None else '—'} | {ok} |")

    sat += ["", "### ⛔⛔ Klinik güvenlik bayrağı", "", "| judge | ateşleyen |",
            "|---|---:|", f"| `claude-sonnet-subagent` | {kg_c}/{len(esli)} |",
            f"| `agy:gemini-3.8-flash-high` | {kg_g}/{len(esli)} |", "",
            "⭐ T176 bu farkı korpus ölçeğinde ölçmüştü: Claude 85/7069 "
            "(%1,20), Gemini 0/430. ⛔ Bu bayrak `build.py`'nin **tek** "
            "otomatik klinik güvenlik kapısıdır (T121) ⇒ judge seçimi bir "
            "**güvenlik kararıdır**, yalnız bir ölçüm kararı değil.", ""]

    # ── C. korpus düzeyinde kapı bayrakları ─────────────────────────
    BAYRAK = ["klinik_guvenlik_ihlali", "rol_siniri_ihlali",
              "kurum_yordam_ihlali", "bos_guvence", "cevapsiz_soru"]
    pb = collections.defaultdict(collections.Counter)
    pn = collections.Counter()
    for k in birincil:
        j = yargi.get(k["id"])
        if not j:
            continue
        pn[k["parti"]] += 1
        if j.get("grounding") == 2:
            pb[k["parti"]]["grounding=2"] += 1
        for b in BAYRAK:
            if j.get(b):
                pb[k["parti"]][b] += 1
    partiler = sorted(pn)
    sat += ["## ⭐⭐⭐ C. Kapı bayrakları — bütün Claude yargıları", "",
            "⛔⛔ `klinik_guvenlik_ihlali` `build.py`'nin **tek** otomatik "
            "klinik güvenlik kapısıdır (T121) ⇒ o satır bir ölçüm değil bir "
            "**eleme listesidir**.", "",
            "| bayrak | " + " | ".join(f"`{p.replace('v6-', '')}`" for p in partiler)
            + " | **toplam** |",
            "|---|" + "---:|" * (len(partiler) + 1)]
    for b in ["grounding=2"] + BAYRAK:
        tot = sum(pb[p][b] for p in partiler)
        sat.append(f"| `{b}` | " + " | ".join(str(pb[p][b]) for p in partiler)
                   + f" | **{tot}** |")
    sat.append("| _yargılanan_ | " + " | ".join(str(pn[p]) for p in partiler)
               + f" | _{sum(pn.values())}_ |")
    g2 = {p: pb[p]["grounding=2"] for p in partiler}
    en = max(partiler, key=lambda p: g2[p] / pn[p])
    sat += ["", f"⛔ **`grounding` = 2 (uydurma) toplam {sum(g2.values())}/"
            f"{sum(pn.values())} = %{100*sum(g2.values())/sum(pn.values()):.0f}.** "
            f"En yüksek oran `{en}`: {g2[en]}/{pn[en]} = "
            f"**%{100*g2[en]/pn[en]:.0f}**.", "",
            "⚠️ **`v6-parti8` bu oturumda HIZLANDIRILMIŞ üretilen partidir** "
            "(K260/K261: alt ajan taslak, benim yazma turum 6'dan 3'e indi). "
            "Oranını öteki partilerle karşılaştırmak hızlanmanın bedelini "
            "sormanın doğal yolu — ⛔⛔ **ama bu rapor o karşılaştırmayı "
            "KURMUYOR:** partiler aynı tohum dağılımıyla üretilmedi (T233: "
            "parti8 planı %50 yüksek riskli tohum çekti, havuz %38,7) ve "
            "uydurma oranının risk düzeyinden bağımsız olduğu gösterilmedi. "
            "⇒ Ayrı ve tasarlanmış bir ölçüm gerekir.", "",
            "⭐⭐⭐ **T238 burada SAYIYLA doğrulandı:** `grounding`'in kendiyle "
            "farkı **0** (judge hep aynı ayrıntıyı seçiyor) ama Gemini'yle "
            "farkı **0.29** ⇒ %100 tekrar-test uyumu güvenilirlik DEĞİL, "
            "**paylaşılan seçim eğilimi**. T238 bunu öngörmüştü.", "",
            "## ⛔ Bu koşunun söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **K97: bu sayılar Gemini sayılarıyla AYNI TABLOYA konmaz** | "
            "`v6-parti1` ve `v6-parti2` Gemini ile puanlı; B bölümü bir "
            "**köprü** kurar ama tabloları birleştirmez |",
            "| ⛔⛔ **Öbekleme bir bağımsızlık kaybıdır** | Gemini her kaydı "
            "ayrı çağrıda gördü; bir subagent 16 kaydı aynı bağlamda gördü ⇒ "
            "sıra/çapa etkisi olabilir. A bölümü bu etkiyi tabana **dahil** "
            "ölçer, ondan **ayıramaz** |",
            "| ⛔ **Üretici ile judge aynı aileden** | K45 öz-şişirmeyi ölçtü "
            "(+6/+11); körlük bunu azaltır, sıfırlamaz |",
            "| ⚠️ **Judge kalite ölçmez, tarar** | K57'den beri geçerli |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[:14]))
    if bozuk:
        print("BOZUK:", bozuk[:5])
    if eksik:
        print(f"EKSİK {len(eksik)}: {', '.join(eksik[:20])}")
    print(f"\n→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
