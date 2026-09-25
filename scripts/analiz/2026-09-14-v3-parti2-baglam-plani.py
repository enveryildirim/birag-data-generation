#!/usr/bin/env python3
"""v3 parti 2 — bağlam (RAG) dilimi planı, 8 satır.

⚠️ ÇIKTI DONDURULUR. Plan ELLE tasarlandı; betik tasarımı ÜRETMİYOR, DOĞRULUYOR.
Doğrulama düşerse plan yazılmaz.

Neden 8: plan.md §6 RAG dilimini %10 istiyor. Parti 1'de 0/40 vardı; 8/80 = %10,
yani iki parti birlikte hedefe oturuyor.

Davranış dağılımı `uretim-v3.md` §7a'dan (v2'nin dilimi bağlamı KULLANMAYI hiç
öğretmiyordu — envanter raporu §2b):
    cevapla   4/8   soruldu + cevap bağlamda VAR   ← v2'de 0 tane
    yetersiz  2/8   soruldu + cevap bağlamda YOK   (is_negative)
    izin_iste 1/8   sorulmadı + bilgi işe yarar    (K19'un asıl kapsamı)
    ilgisiz   1/8   bağlam gürültü                 → görmezden gel

Girdi : data/seeds.jsonl
Çıktı : data/plan/v3-parti2-baglam.jsonl + reports/analiz/2026-09-14-v3-parti2-baglam-plani.md
"""
from __future__ import annotations

import collections
import hashlib
import json
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
SEEDS = KOK / "data/seeds.jsonl"
KULLANILAN = [KOK / "data/candidates/expert-70.jsonl", KOK / "data/candidates/v3-parti1.jsonl"]
CIKTI_JSONL = KOK / "data/plan/v3-parti2-baglam.jsonl"
CIKTI_MD = KOK / "reports/analiz/2026-09-14-v3-parti2-baglam-plani.md"

# K17: tek format kullanılmaz. Sekiz satırda BEŞ ayrı varyant dolaşır.
FORMAT = {
    "xml":      '<context kaynak="{k}">\n{m}\n</context>\n\n',
    "koseli":   "[BAĞLAM]\nKaynak: {k}\n{m}\n[/BAĞLAM]\n\n",
    "tire":     "--- KAYNAK: {k} ---\n{m}\n---\n\n",
    "markdown": "### BAĞLAM\nKaynak: {k}\n\n{m}\n\n",
    "parantez": "BAĞLAM (kaynak: {k})\n{m}\n\n",
}

# Elle tasarlanan plan. Tohumlar okunarak seçildi (K65: okumadan plan dondurulmaz).
P = [
    # sira, davranis, seed10, senaryo, tur, yas, mi, durum, kapanis, sysvar, neg, format
    (1, "cevapla",   "1c99e9ad47", "ambivalans",          "alkol",         "yetiskin", "engaging", "merak_sorusu",    "acik_uclu_soru",    "canon",      0, "xml"),
    (2, "yetersiz",  "64d3439bcd", "ambivalans",          "alkol",         "yetiskin", "engaging", "merak_sorusu",    "acik_uclu_soru",    "canon",      1, "koseli"),
    (3, "cevapla",   "6037eb17cc", "nazikce_karsi_cikma", "receteli_ilac", "yetiskin", "focusing", "merak_sorusu",    "yalnizca_yansitma", "paraphrase", 0, "tire"),
    (4, "izin_iste", "05332da95d", "kayma_nuks",          "alkol",         "yetiskin", "engaging", "aradan_donus",    "acik_uclu_soru",    "canon",      0, "markdown"),
    (5, "ilgisiz",   "c5065b4746", "ambivalans",          "tutun",         "yetiskin", "evoking",  "suregiden_durum", "yalnizca_yansitma", "canon",      0, "parantez"),
    (6, "yetersiz",  "86681c5b2f", "rol_siniri",          "alkol",         "yetiskin", "focusing", "plan_yapma",      "acik_uclu_soru",    "canon",      1, "xml"),
    (7, "cevapla",   "ac2d9b7a28", "ambivalans",          "kumar",         "ergen",    "engaging", "merak_sorusu",    "acik_uclu_soru",    "canon",      0, "koseli"),
    (8, "cevapla",   "e5f3c4c0b4", "rol_siniri",          "alkol",         "yetiskin", "engaging", "merak_sorusu",    "durur",             "paraphrase", 0, "tire"),
]
HEDEF_DAVRANIS = {"cevapla": 4, "yetersiz": 2, "izin_iste": 1, "ilgisiz": 1}
# yas gevşetmesi: şema yalnızca yetiskin|ergen tanıyor (v3 §1); `yasli` → `yetiskin`.
YAS_ESLE = {"yasli": "yetiskin", "orta_yas": "yetiskin", "genc_yetiskin": "yetiskin"}


def dogrula(satirlar, tohumlar, kullanilan) -> list[str]:
    s = []
    if len(P) != 8:
        s.append(f"plan {len(P)} satır, 8 bekleniyordu")
    d = collections.Counter(r["davranis"] for r in satirlar)
    for k, v in HEDEF_DAVRANIS.items():
        if d.get(k, 0) != v:
            s.append(f"davranış `{k}`: {d.get(k,0)} satır, {v} bekleniyordu (§7a)")
    if len({r["format"] for r in satirlar}) < 5:
        s.append(f"format varyantı {len({r['format'] for r in satirlar})} < 5 (K17)")
    for r in satirlar:
        t = tohumlar.get(r["seed_id"])
        if t is None:
            s.append(f"#{r['sira']}: tohum bulunamadı ({r['seed10']})")
            continue
        if r["seed_id"] in kullanilan or t["source_id"] in kullanilan:
            s.append(f"#{r['sira']}: tohum zaten kullanılmış")
        m = t["meta"]
        if m.get("senaryo") == "kriz" or m.get("risk_seviyesi") == "cok_yuksek":
            s.append(f"#{r['sira']}: kriz/çok yüksek risk tohumu (Kural 3)")
        if (r["neg"] == 1) != (r["davranis"] == "yetersiz"):
            s.append(f"#{r['sira']}: is_negative ile davranış uyuşmuyor (§8)")
        ham = m.get("yas_grubu")
        if YAS_ESLE.get(ham, ham) != r["yas"]:
            s.append(f"#{r['sira']}: yaş uyuşmuyor — tohum `{ham}`, plan `{r['yas']}`")
    return s


def main() -> None:
    tohumlar = {}
    for l in open(SEEDS):
        t = json.loads(l)
        tohumlar[t["seed_id"]] = t
    kisa = {k[:10]: k for k in tohumlar}
    kullanilan = set()
    for f in KULLANILAN:
        for l in open(f):
            r = json.loads(l)
            kullanilan.add(r["gen_meta"].get("seed_id") or "")
            kullanilan.update(r.get("source_ids") or [])

    alanlar = ("sira davranis seed10 senaryo tur yas mi konusma_durumu "
               "turn_ending sysvar neg format").split()
    satirlar = []
    for row in P:
        d = dict(zip(alanlar, row))
        d["seed_id"] = kisa.get(d["seed10"], d["seed10"])
        t = tohumlar.get(d["seed_id"])
        d["source_id"] = t["source_id"] if t else None
        d["user_message"] = t["user_message"] if t else None
        d["tohum_yas"] = t["meta"]["yas_grubu"] if t else None
        satirlar.append(d)

    sapma = dogrula(satirlar, tohumlar, kullanilan)
    if sapma:
        print("DOĞRULAMA DÜŞTÜ — plan yazılmadı:")
        for x in sapma:
            print("  ·", x)
        raise SystemExit(1)

    CIKTI_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with open(CIKTI_JSONL, "w") as f:
        for d in satirlar:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")

    gev = [d for d in satirlar if d["tohum_yas"] != d["yas"]]
    L = ["# v3 parti 2 — bağlam (RAG) dilimi planı", "",
         f"**Çıktı:** `data/plan/v3-parti2-baglam.jsonl` · SHA256 "
         f"`{hashlib.sha256(CIKTI_JSONL.read_bytes()).hexdigest()}`  ",
         f"**Betik:** `scripts/analiz/2026-09-14-v3-parti2-baglam-plani.py` · "
         f"**Tarih:** {TARIH}", "", "---", "",
         "## Neden 8 satır", "",
         "`plan.md` §6 RAG dilimini **%10** istiyor. Parti 1'de **0/40** vardı; "
         "**8/80 = %10**, iki parti birlikte hedefe oturuyor.", "",
         "## Davranış dağılımı (§7a)", "", "| Davranış | Satır | Hedef |", "|---|---:|---:|"]
    d = collections.Counter(r["davranis"] for r in satirlar)
    for k, v in HEDEF_DAVRANIS.items():
        L.append(f"| `{k}` | {d[k]} | {v} |")
    L += ["", "> `cevapla` v2'de **0/9**'du — dilimin ana işi o.", "",
          "## Satırlar", "",
          "| # | davranış | senaryo | tür | yaş | MI | durum | kapanış | sysvar | neg | format |",
          "|---:|---|---|---|---|---|---|---|---|:--:|---|"]
    for r in satirlar:
        L.append(f"| {r['sira']} | {r['davranis']} | {r['senaryo']} | {r['tur']} | "
                 f"{r['yas']} | {r['mi']} | {r['konusma_durumu']} | {r['turn_ending']} | "
                 f"{r['sysvar']} | {'✔' if r['neg'] else '—'} | `{r['format']}` |")
    L += ["", f"**Format varyantı: {len({r['format'] for r in satirlar})}** "
          f"({', '.join(sorted({r['format'] for r in satirlar}))}) — K17 4-5 istiyor.", ""]
    if gev:
        L += ["## ⚠️ Yaş gevşetmesi", "",
              "Şema yalnızca `yetiskin|ergen` tanıyor (v3 §1); tohumun kendi etiketi farklı:", ""]
        L += [f"- #{r['sira']}: tohum `{r['tohum_yas']}` → plan `{r['yas']}`" for r in gev]
        L += [""]
    L += ["## ⚠️ Bu dilimin bilinen sapması", "",
          f"Kapanış: {sum(1 for r in satirlar if r['turn_ending']=='acik_uclu_soru')}/8 "
          "soruyla bitiyor (%62), §5a hedefi %50. Sekiz satırlık bir dilimde bu **tek "
          "kayıtlık** bir oynama; parti 2'nin kalan 32 kaydı bunu dengelemek zorunda. "
          "Korpus raporu parti 2'nin tamamında denetleyecek.", "",
          "> ⚠️ **§5a'da açık:** #4 bir **izin sorusu** ile bitiyor (*\"paylaşmamı ister "
          "misin?\"*) — bu açık uçlu bir soru değil, ama §5a'nın beş kategorisinde izin "
          "sorusunun karşılığı yok. `acik_uclu_soru` beyan ediliyor çünkü kapı soru "
          "VARLIĞINA bakıyor; kategorinin dar kaldığı Oturum 3'e not edildi.", ""]
    CIKTI_MD.write_text("\n".join(L) + "\n")
    print(f"plan yazıldı: {CIKTI_JSONL.relative_to(KOK)} ({len(satirlar)} satır) · "
          f"rapor: {CIKTI_MD.relative_to(KOK)}")


if __name__ == "__main__":
    main()
