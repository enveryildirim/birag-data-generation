#!/usr/bin/env python3
"""`celiskili` sınıfının judge sonuçlarını toplar ve iki şeyi ölçer.

⭐ **Türetme KOPYALANMIYOR (K103):** `turet()` 09-15 toplama betiğinden
import edilir; judge adı ve rubrik sürümü burada **açıkça** ayarlanır.

Ölçülen iki şey:

  **A. Bu dalganın gürültü tabanı.** Aynı kayıt iki ayrı numarayla, ayrı
  öbeklerde soruldu. Boyut başına *aynı notu verme* yüzdesi ve ortalama
  mutlak fark. ⛔ n küçük (4 çift) ⇒ taban **kaba**; başka bir dalganın
  tabanının yerine geçmez ve güven aralığı hesaplanmadı.

  **B. Sınıfın kendi iddiasının sınanması.** §7a″ `celiskili`, korpusun
  ölçülmüş en büyük kusuru olan **uydurmaya** (T238, %12) karşı
  tasarlandı. Rubriğin `grounding` türetmesi tam da bir **uydurma
  sondası**: `grounding == 2` ⇒ yargıç somut bir ayrıntının konuşmada
  karşılığı olmadığını söylüyor. ⇒ Bu sınıfta uydurma oranı, korpus
  tabanının **altında** olmalı. Değilse tasarım iddiası boşa düşer.
  ⛔⛔ Bu bir **karşılaştırma değil gözlemdir**: korpus tabanı başka bir
  dalgada, başka kayıtlarla ölçüldü; n=12 ile oran **kararsızdır** ve
  hiçbir anlamlılık sınaması yapılmadı.

⛔ Judge notu kaydın kalitesini değil, **yargıcın o kayda verdiği notu**
ölçer. Kapılardan geçmek ile iyi not almak aynı şey değildir.

Çıktı: data/judged/celiskili-{pilot,parti2}.claude.jsonl
       reports/analiz/2026-09-22-judge-celiskili.md
"""
from __future__ import annotations

import json
import os
import statistics as st
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from kunye import betik_tarihi  # noqa: E402

# ⛔⛔ 09-15 betiği modül düzeyinde `sys.argv`'i EZİYOR; kendi
#   argümanlarımız onun altında kalıyordu ve betik sessizce YANLIŞ
#   dalgayı topladı (bir kez topladı). Aynı kusur hazırlık betiğinde de
#   çıkmıştı — iki yerde de argv korunuyor.
_ARGV = sys.argv[:]
_yol = KOK / "scripts/analiz/2026-09-15-judge-sonuclari-topla.py"
_spec = _iu.spec_from_file_location("_topla15", _yol)
_t15 = _iu.module_from_spec(_spec)
sys.argv = [str(_yol)]
_spec.loader.exec_module(_t15)
sys.argv = _ARGV                     # ⭐ geri al
_t15.JUDGE_ADI = "claude-sonnet-subagent"
_t15.RUBRIK = "judge-eksen1.v9"
turet = _t15.turet

# ⭐ Parametreli (T200): hangi dalga toplanıyorsa o verilir.
_D = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--dizin=")),
          "celiskili")
DIZIN = Path(os.environ["BIRAG_SCRATCH"]) / f"judge-isleri/{_D}"
RAPOR = KOK / f"reports/analiz/2026-09-22-judge-{_D}.md"
BOYUT = ["duygusal_tepki", "yorumlama", "kesif", "mi_uyumu", "grounding",
         "anlasilirlik", "dogallik"]
_K = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--parti=")), "")
KAYNAK = ({k: f"data/candidates/{k}.jsonl" for k in _K.split(",") if k.strip()}
          or {"celiskili-pilot": "data/candidates/celiskili-pilot.jsonl",
              "celiskili-parti2": "data/candidates/celiskili-parti2.jsonl"})
# ⛔ Boyutlar AYNI ölçekte değil — ortalama tablosu bunu yazmazsa yanıltır.
OLCEK = {"duygusal_tepki": "0-2", "yorumlama": "0-2", "kesif": "0-2",
         "mi_uyumu": "1-5", "grounding": "2/5", "anlasilirlik": "1-5",
         "dogallik": "1-5"}
T238_KORPUS = 12          # % — başka dalga, aynı rubrik ailesi (bkz. şerh)


# ⛔ Durak kökleri — `gibi`, `şimdi` gibi sözcükler HER metinde var; mekanizma
#   tablosunda sayılırlarsa «tohumda var» sayısını ŞİŞİRİRLER (ilk sürüm
#   şişirmişti). Elenerek ölçüm daraltılır, gevşetilmez.
DURAK_KOK = {w[:5] for w in """gibi şimdi yine ama için bunu şunu onun sonra
önce kadar daha çok bir bu şey olan olarak diye kendi ben sen biraz zaten
şöyle böyle hem söyle""".split()}


def _kok(metin: str, n: int = 5, durak: bool = True) -> set[str]:
    """Türkçe ek eşlemesi için kaba kök: ilk n harf. K40/T22 ailesinin dersi —
    tam dizge eşleme Türkçe'de yanlış negatif üretir."""
    import re as _re
    k = {w[:n] for w in _re.findall(r"\w{4,}", metin.lower())}
    return k - DURAK_KOK if durak else k


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

    # ── dosyalara yaz ───────────────────────────────────────────────
    yazilan = {}
    for parti, yol in KAYNAK.items():
        aday = [json.loads(l) for l in open(KOK / yol)]
        n = 0
        for r in aday:
            if not r.get("replay") and r["id"] in yargi:
                r["judge"] = yargi[r["id"]]
                n += 1
            else:
                r.setdefault("judge", None)
        hedef = KOK / f"data/judged/{parti}.claude.jsonl"
        hedef.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n"
                                 for x in aday), encoding="utf-8")
        assert hedef.exists()
        yazilan[parti] = (n, len(aday))

    # ── A. gürültü tabanı ───────────────────────────────────────────
    ciftler = []
    for k in tekrarlar:
        a, b = oku(k["no"]), yargi.get(k["id"])
        if a and "_hata" not in a and b:
            ciftler.append((a, b))
    taban, tfark = {}, {}
    for d in BOYUT:
        p = [(a[d], b[d]) for a, b in ciftler
             if a.get(d) is not None and b.get(d) is not None]
        if p:
            taban[d] = round(100 * sum(x == y for x, y in p) / len(p))
            tfark[d] = round(st.mean(abs(x - y) for x, y in p), 2)

    # ── B. uydurma sondası + not özeti ──────────────────────────────
    hepsi = list(yargi.values())
    ort = {d: round(st.mean([r[d] for r in hepsi if r.get(d) is not None]), 2)
           for d in BOYUT if any(r.get(d) is not None for r in hepsi)}
    uydurma = [i for i, r in yargi.items() if r.get("grounding") == 2]
    kg = [i for i, r in yargi.items() if r.get("klinik_guvenlik_ihlali")]

    # ── B2. MEKANİZMA: uydurulan ayrıntı TOHUMDA mı duruyor? ────────
    #   Hipotez: cevabı tohumdan yazdım, kullanıcı mesajı ise tohumun
    #   KISALTMASI ⇒ cevapta yansıttığım ayrıntı mesajda yok, tohumda var.
    #   ⛔ İddia edilmiyor, ÖLÇÜLÜYOR.
    tohumlar = {t["seed_id"]: t for t in
                (json.loads(l) for l in open(KOK / "data/seeds.v2.jsonl"))}
    kayit_of = {}
    for yol in KAYNAK.values():
        for l in open(KOK / yol):
            r = json.loads(l)
            kayit_of[r["id"]] = r
    mekanizma = []
    for kid in sorted(uydurma):
        r = kayit_of[kid]
        j = yargi[kid]
        ayrinti = j.get("en_somut_ayrinti") or ""
        kullanici = r["messages"][1]["content"].split("</context>")[-1]
        t = tohumlar.get(r["gen_meta"]["seed_id"], {})
        tohum_metin = (t.get("user_message", "") + " "
                       + (t.get("scenario_context") or ""))
        a = _kok(ayrinti)
        yok_mesajda = a - _kok(kullanici)     # mesajda YOK
        tohumda = yok_mesajda & _kok(tohum_metin)   # ama tohumda VAR
        mekanizma.append({
            "id": kid, "banka": r["gen_meta"]["celiskili_banka_no"],
            "ayrinti": ayrinti[:70], "eksik": len(yok_mesajda),
            "tohumda": len(tohumda),
            "ornek": sorted(tohumda)[:4]})

    # ── rapor ───────────────────────────────────────────────────────
    s = [f"# `celiskili` sınıfının ilk yargısı — {len(yargi)} kayıt", "",
         f"**Betik:** `{Path(__file__).relative_to(KOK)}` · "
         f"**Tarih:** {betik_tarihi(__file__)}  ",
         f"**Girdi:** {' · '.join(f'`{v}`' for v in KAYNAK.values())}  ",
         f"**Yargıç:** claude-sonnet-subagent · **rubrik:** judge-eksen1.v9  ",
         f"**Toplanan:** {len(yargi)}/{len(birincil)} · bozuk {len(bozuk)} · "
         f"eksik {len(eksik)}  ", ""]
    if bozuk or eksik:
        s += ["⛔ **Eksik/bozuk işler:** "
              + " · ".join([f"{n} ({h})" for n, h in bozuk] + eksik), ""]

    s += ["## Not ortalamaları", "",
          "| boyut | ortalama | ölçek |", "|---|---:|:--|"]
    s += [f"| `{d}` | {v} | {OLCEK.get(d, '?')} |"
          for d, v in sorted(ort.items(), key=lambda t: -t[1])]
    s += ["", "⛔⛔ **Boyutlar aynı ölçekte değil** — EPITOME üçlüsü "
          "(`duygusal_tepki`, `yorumlama`, `kesif`) **0-2**, ötekiler 1-5. "
          "Sütunu ölçeksiz okumak yanıltır.", "",
          "⚠️ `kesif` düşük (%.2f/2) ve bu **kısmen tasarımın sonucu**: bu "
          "sınıfta 12 cevabın 11'i `turn_ending ∈ {durur, ozet, "
          "yalnizca_yansitma, takdir}` ile bitiyor, yani açık uçlu soruyla "
          "davet etmiyor. ⛔ «Tasarım gereği» demek **savunma değildir**: "
          "kotanın bu boyutu bastırıp bastırmadığı ölçülmedi."
          % ort.get("kesif", 0), "",
          "⛔ Ortalama **karşılaştırmasız** bir sayıdır: bu kayıtların başka "
          "bir kümeyle kıyası yapılmadı ve n=12.", ""]

    s += ["## A. Bu dalganın gürültü tabanı", "",
          f"Tekrar çifti: **{len(ciftler)}** (aynı kayıt, iki numara, ayrı öbek)",
          "", "| boyut | aynı not % | ort. mutlak fark |", "|---|---:|---:|"]
    s += [f"| `{d}` | {taban[d]} | {tfark[d]} |"
          for d in sorted(taban, key=lambda d: -taban[d])]
    s += ["", "⛔⛔ **n=%d çift.** Taban kaba; güven aralığı hesaplanmadı ve "
          "başka bir dalganın tabanının yerine geçmez (K137: rubrik sürümü "
          "değişirse karşılaştırma geçersiz)." % len(ciftler), ""]

    oran = round(100 * len(uydurma) / len(yargi))
    yon = ("**ÜSTÜNDE**" if oran > T238_KORPUS else
           "**ALTINDA**" if oran < T238_KORPUS else "**eşit**")
    s += ["## B. Uydurma sondası — sınıfın kendi iddiası ÇÜRÜDÜ mü?", "",
          f"`grounding == 2` (yargıç: somut ayrıntının konuşmada karşılığı yok): "
          f"**{len(uydurma)}/{len(yargi)} = %{oran}**", "",
          f"⛔⛔ §7a″ bu sınıfı **uydurmaya karşı** tasarlamıştı. Ölçülen oran "
          f"korpus tabanının (T238: %{T238_KORPUS}) {yon}. ⇒ **Tasarım iddiası "
          f"bu ölçümde DESTEKLENMEDİ.**", "",
          f"`klinik_guvenlik_ihlali`: **{len(kg)}/{len(yargi)}**"
          + (f" — `{'`, `'.join(sorted(kg))}`" if kg else " (Kural 3 tarafı temiz)"),
          "", "### Mekanizma — iddia değil, ölçüm", "",
          "Hipotez: **cevabı tohumdan yazdım, kullanıcı mesajı ise tohumun "
          "kısaltması.** Yansıttığım ayrıntı mesajda yok, tohumda var. "
          "Sınama: uydurulan ayrıntının kökleri kullanıcı mesajında yok ama "
          "tohum metninde var mı?", "",
          "| banka | uydurulan ayrıntı | mesajda yok | **tohumda var** | örnek kök |",
          "|---:|---|---:|---:|---|"]
    s += [f"| #{m['banka']} | {m['ayrinti']} | {m['eksik']} | **{m['tohumda']}** | "
          f"{', '.join('`'+x+'`' for x in m['ornek']) or '—'} |"
          for m in mekanizma]
    tam = sum(1 for m in mekanizma if m["tohumda"] > 0)
    s += ["", f"⇒ **{tam}/{len(mekanizma)}** uydurmada, mesajda bulunmayan "
          "ayrıntı **tohumda duruyor**. Uydurma serbest değil, **tohumdan "
          "sızıyor**.", "",
          "⭐⭐⭐ **Eksik kapı, az önce yazdığım kapının AYNASI.** T264'te "
          "T217 kapısını yazdım: *«kullanıcı metni kendi tohumundan mı?»* "
          "Kimse tersini sormadı: ***«cevap yalnız kullanıcı metninden mi?»*** "
          "Tohum→mesaj kısaltması bilgiyi düşürüyor, cevap ise düşmeden önceki "
          "tohumu hatırlıyor. ⇒ Bu, kural yazılı-kapı yok ailesinin (T22) yeni "
          "bir üyesidir: `uretim-v5` uydurmayı **yasaklıyor**, hiçbir kapı "
          "**bakmıyor**.", "",
          f"⛔ **`celiskili_ok` {len(yargi)}/{len(yargi)} geçirdi** — çünkü o "
          "kapı yalnız çelişkinin adlandırılmasına ve iki pasaja atfa bakıyor; "
          "**yansıtma cümlesine bakmıyor**. Kapıdan geçmek temiz olmak "
          "değildir.", "",
          "⛔⛔ **Şerhler — bu sayı ne kadar sağlam:** "
          f"(1) n={len(yargi)} ⇒ bir kayıt oranı ~%{round(100/len(yargi))} "
          "oynatır, güven aralığı hesaplanmadı, anlamlılık sınanmadı · "
          f"(2) %{T238_KORPUS} **başka bir dalgada, başka kayıtlarla** "
          "ölçüldü ⇒ bu tam bir karşılaştırma değil, iki ayrı gözlemin yan "
          "yana konmasıdır · (3) `grounding` türetmesi **tek ayrıntı** "
          "sondasıdır (`en_somut_ayrinti`) ⇒ ölçülen oran bir **alt "
          "sınırdır**, gerçek uydurma bundan fazla olabilir · (4) tek yargıç "
          "ailesi, doğrulayan ikinci anotatör yok · (5) kök eşleme 5 harfe "
          "kısaltıyor ⇒ mekanizma tablosu yanlış pozitif verebilir.", ""]
    s += ["## Yazılan dosyalar", "", "| dosya | yargılanan | toplam |",
          "|---|---:|---:|"]
    s += [f"| `data/judged/{p}.claude.jsonl` | {n} | {t} |"
          for p, (n, t) in sorted(yazilan.items())]

    s += ["", "## ⛔ Bunun söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔⛔ **Körlük tam değil** | 12 kaydın hepsinde iki çelişkili "
          "`<context>` var ve cevapların hepsi çelişkiyi adlandırıyor ⇒ "
          "yargıç bunların **aynı sınıftan** olduğunu metinden anlayabilir. "
          "Numara karıştırma partiyi gizler, **sınıfı gizlemez** |",
          "| ⛔ **Öbekleme bağımsızlık kaybı** | bir subagent öbeğindeki 8 "
          "kayıt aynı bağlamda duruyor ⇒ sıra ve çapa etkisi olabilir; "
          "tekrar çiftleri ayrı öbeklere düşürülerek bu etki tabana dahil "
          "edildi, ama **ayrıştırılmadı** |",
          "| ⛔ **Tek yargıç ailesi** | yalnız Claude; bu kayıtlar için "
          "Gemini yargısı **yok** ⇒ K97'nin çapraz karşılaştırması burada "
          "yapılamadı |",
          "| ⛔ **Kapı ≠ not** | 12 kaydın 12'si `celiskili_ok`'tan geçti; "
          "bu, iyi not aldıkları anlamına gelmez |",
          "| ⚠️ **Kayıtları ben yazdım** | K30/K260: üretici de yargıyı "
          "okuyan da aynı taraf; bağımsız anotatör hâlâ borç |"]

    RAPOR.write_text("\n".join(s) + "\n", encoding="utf-8")
    assert RAPOR.exists()
    print(f"⭐ {len(yargi)}/{len(birincil)} toplandı · bozuk {len(bozuk)} · "
          f"eksik {len(eksik)}")
    print(f"   ortalamalar: {ort}")
    print(f"   gürültü tabanı ({len(ciftler)} çift): {taban}")
    print(f"   ⛔ uydurma (grounding==2): {len(uydurma)}/{len(yargi)} = "
          f"%{oran} · korpus tabanı %{T238_KORPUS} ⇒ {yon.strip('*')}")
    print(f"   mekanizma: {tam}/{len(mekanizma)} uydurmada ayrıntı TOHUMDA var")
    print(f"   klinik ihlal: {len(kg)}")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
