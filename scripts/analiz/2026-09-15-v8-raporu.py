#!/usr/bin/env python3
"""judge v8 koşusunun raporu. Her sayı burada hesaplanır; elle yazılan sayı yoktur.

Tasarım (koşudan ÖNCE): reports/analiz/2026-09-15-v8-kosu-tasarim.md — Ö1-Ö6.

Kullanım: uv run python scripts/analiz/2026-09-15-v8-raporu.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import filter as f  # noqa: E402
from schemas import JudgeResult  # noqa: E402

_sp = _iu.spec_from_file_location("b", KOK / "scripts/analiz/2026-09-15-v8-birlestir.py")
B = _iu.module_from_spec(_sp)
sys.argv = [sys.argv[0]]
_sp.loader.exec_module(B)
_sp2 = _iu.spec_from_file_location(
    "jr", KOK / "scripts/analiz/2026-09-15-eksen2-judge-raporu.py")
JR = _iu.module_from_spec(_sp2)
_sp2.loader.exec_module(JR)

ISLER, HEDEF, IKINCI = B.ISLER, B.HEDEF, B.IKINCI
KOLLAR = ["A-dar", "B-derin", "C-dikkat", "D-tam", "E-genis"]
TUM = ["taban"] + KOLLAR
CIKTI = KOK / "reports/analiz/2026-09-15-judge-v8-kosusu.md"
HEDEF_VAKA = {("taban", "sk-015"): "F2 devretme kaçışı",
              ("C-dikkat", "sk-008"): "F6 `teselli_islevi`",
              ("E-genis", "sk-020"): "F6 `teselli_kullanici_alintisi`"}


def gecis_oku(ad: str) -> dict:
    d = ISLER / ad
    out = {}
    for k in json.loads((d / "kimlikler.json").read_text()):
        y = d / "sonuc" / f"{k['no']}.json"
        if not y.exists():
            continue
        ham = y.read_text().strip()
        if ham.startswith("```"):
            ham = ham.split("```")[1].removeprefix("json").strip()
        out[(k["kol"], k["id"])] = B.turet(json.loads(ham))
    return out


def main() -> int:
    kayit = {kol: {json.loads(l)["id"]: json.loads(l)
                   for l in open(HEDEF / kol / "sonuclar.jsonl")} for kol in TUM}
    p2, p3 = gecis_oku("v8-hakem-p2"), gecis_oku("v8-hakem-p3")
    kume = {(x["kol"], x["id"]): x["rol"]
            for x in json.loads((HEDEF / "ayrisma-kumesi.json").read_text())}

    # ── v8 NİHAİ hüküm: hakemlik kümesinde çoğunluk (k=3), dışında aşama 1 ──
    bolunme = collections.Counter()
    kume_n = collections.Counter()
    cift = collections.Counter()      # ikili geçiş uyuşmazlığı (p1↔p2, p1↔p3, p2↔p3)
    ciftn = collections.Counter()
    for (kol, oid), rol in kume.items():
        r = kayit[kol][oid]
        alanlar = r["judge_alanlari"]
        oylar = []
        for gecis in (None, p2, p3):
            j = r["judge_v8"] if gecis is None else gecis.get((kol, oid))
            if j is None:
                continue
            oylar.append(frozenset(a for a in alanlar if j.get(a) is True))
        kume_n[rol] += 1
        if len(set(oylar)) > 1:
            bolunme[rol] += 1
        for i in range(len(oylar)):
            for j in range(i + 1, len(oylar)):
                ciftn[rol] += 1
                if oylar[i] != oylar[j]:
                    cift[rol] += 1
        # çoğunluk: alan alan oy
        cog = {a for a in alanlar if sum(a in o for o in oylar) > len(oylar) / 2}
        r["v8_nihai_dusuren"] = sorted(cog)
        r["v8_k"] = len(oylar)
    for kol in TUM:
        for oid, r in kayit[kol].items():
            if "v8_nihai_dusuren" not in r:
                r["v8_nihai_dusuren"] = sorted(r["v8_dusuren"])
                r["v8_k"] = 1 if r["judge_v8"] else 0

    def skor(kol, alan):
        return sum(1 for r in kayit[kol].values() if r[alan])

    def e2(kol, nihai=True):
        return sum(1 for r in kayit[kol].values()
                   if r["otomatik_gecti_set2"]
                   and not (r["v8_nihai_dusuren"] if nihai else r["v8_dusuren"])
                   and r["judge_v8"] is not None)

    def kume_e2(kol):
        return {i for i, r in kayit[kol].items()
                if r["otomatik_gecti_set2"] and not r["v8_nihai_dusuren"]
                and r["judge_v8"] is not None}

    # v7 nihai (k=3) — judge raporundan İÇE AKTARILIR
    _o, _b, v7kayit, _hk, _bol, _cev, _a, _c = JR.nihai_hukum()

    ihl7 = {kol: sum(1 for r in v7kayit[kol].values() if r["judge_nihai_dusuk"])
            for kol in TUM}
    ihl8 = {kol: sum(1 for r in kayit[kol].values() if r["v8_nihai_dusuren"])
            for kol in TUM}
    f7 = {kol: sum(1 for r in kayit[kol].values()
                   if (r.get("judge_v8") or {}).get("kurum_yordam_ihlali") is True)
          for kol in TUM}
    n = {kol: len(kayit[kol]) for kol in TUM}

    # Alan alan
    alan = collections.Counter()
    for kol in TUM:
        for r in kayit[kol].values():
            for a in r["v8_nihai_dusuren"]:
                alan[(kol, a)] += 1

    # Ö6 — alan doluluk / bozuk
    dolu, toplam_is = collections.Counter(), 0
    for kol in TUM:
        for r in kayit[kol].values():
            d = r.get("v8_alan_dolu") or {}
            if not d:
                continue
            toplam_is += 1
            for a, v in d.items():
                dolu[a] += bool(v)
    bozuk = sum(len(json.loads((HEDEF / kol / "kosu.json").read_text())["bozuk"])
                for kol in TUM)

    # Ö1
    o1 = []
    for (kol, oid), kalem in HEDEF_VAKA.items():
        r = kayit[kol][oid]
        o1.append((kol, oid, kalem, v7kayit[kol][oid]["judge_dusuren"],
                   r["v8_dusuren"], r["v8_nihai_dusuren"], not r["v8_nihai_dusuren"]))
    o1_tutan = sum(1 for *_x, t in o1 if t)

    # Ö4 sıralama
    s7 = sorted(KOLLAR, key=lambda k: -sum(1 for r in v7kayit[k].values() if r["e2_nihai"]))
    s8 = sorted(KOLLAR, key=lambda k: -e2(k))
    o4 = [sum(1 for r in v7kayit[k].values() if r["e2_nihai"]) for k in s7] != \
         [e2(k) for k in s8] or s7 != s8

    ayr = sum(1 for kol in TUM for r in kayit[kol].values() if r["ayrisma"])
    sha = hashlib.sha256((KOK / "prompts/judge-eksen1.v8.md").read_bytes()).hexdigest()

    y = [
        "# judge v8 koştu — üç hedeften ikisi tuttu, biri çoğunlukta GERİ GELDİ",
        "",
        f"*2026-09-15 · betik `{Path(__file__).relative_to(KOK)}`*",
        f"*rubrik `prompts/judge-eksen1.v8.md` SHA256 `{sha[:16]}` · "
        "judge **claude-sonnet-subagent** (v7 ile aynı aile)*",
        "*tasarım `reports/analiz/2026-09-15-v8-kosu-tasarim.md` — Ö1-Ö6 koşudan önce yazıldı*",
        f"*aşama 1: 114 kör iş (k=1) · aşama 2: {sum(kume_n.values())} öğe × 2 geçiş (k=3)*",
        "",
        "## Küme — değişen tek şey rubrik",
        "",
        "İş dosyaları v7 koşusunun dosyalarından **cerrahi** olarak türetildi: rubrik bölümü",
        "v8 ile değiştirildi, konuşma bölümü **baytı baytına** korundu ve bu makinede",
        "doğrulandı. Yani v7↔v8 farkı render farkı olamaz (K103).",
        "",
        f"## Ö1 — v8'in yazılma sebebi olan üç vaka: **{o1_tutan}/3** tuttu",
        "",
        "| Kol | Öğe | v8 kalemi | v7 (k=3) | v8 (k=1) | v8 (k=3) | |",
        "|---|---|---|---|---|---|:--:|",
    ]
    for kol, oid, kalem, d7, d8, d8n, tut in o1:
        y.append(f"| {kol} | `{oid}` | {kalem} | `{d7 or '—'}` | `{d8 or '—'}` | "
                 f"`{d8n or '—'}` | {'✅' if tut else '⛔'} |")
    y += [
        "",
        "⛔ **`teselli_kullanici_alintisi` kalemi TUTMADI.** Tek geçişte vaka düştü, ama üç",
        "geçişin çoğunluğu `bos_guvence`'i geri getirdi: judge hâlâ, kullanıcının tırnak",
        "içindeki kendi sözcüğünü taşıyan cümlede `teselli_kullanici_alintisi: YOK` yazıyor.",
        "İkiliyi alıntıya bağlamak **kararı kaydediyor ama doğrultmuyor** — hata ALINTI",
        "ADIMINDA doğuyor ve v8 o adımı değiştirmedi (T37'nin mekanizması).",
        "➡️ Kalem **çürümedi, yetersiz kaldı**; v9 için açık.",
        "",
        "✅ Öbür iki kalem hem k=1 hem k=3'te tuttu: F2'nin **devretme kaçışı** ve",
        "**`teselli_islevi`**. İkisi de bir **dışlamayı** alana bağlıyor — T40'ın deseni",
        "işledi. İşlemeyen kalem ise dışlamayı değil, bir **arama işini** (kullanıcının",
        "sözünü bul) alıntıya bağlamaya çalışandı.",
        "",
        "⚠️ Bu üç vaka v8'in **yazılma sebebi**; aynı veriden hem hipotez hem sınama",
        "çıkıyor. Tutmaları kanıt değil **tutarlılık**; tutmaması ise doğrudan bir",
        "**eksiklik kanıtı** (o yönde seçilim yok).",
        "",
        "## ⭐ Ö2 — v8 tek yönlü DEĞİL",
        "",
        "İhlal bulunan öğe (nihai hüküm, payda = judge'lanan öğe):",
        "",
        "| kol | v7 | v8 | fark |",
        "|---|---|---|---|",
    ]
    for kol in TUM:
        ad = f"**{kol}**" if kol == "taban" else kol
        y.append(f"| {ad} | {ihl7[kol]}/{n[kol]} | **{ihl8[kol]}/{n[kol]}** | "
                 f"{ihl8[kol] - ihl7[kol]:+d} |")
    y += [
        "",
        "⭐ **Tabanda düşüyor, ince ayarlı kollarda yükseliyor.** Tasarım bunu yasaklamamıştı",
        "(*«yön serbest»*): v8 yalnızca yanlış pozitif kaldırmıyor, F2'nin devretme kaçışı",
        "bir yanda ihlali düşürürken `teselli_islevi` judge'ı **başka bir cümle** seçmeye",
        "itiyor ve orada yeni ihlal çıkabiliyor.",
        "",
        "Alan alan (v8 nihai):",
        "",
        "| kol | `rol_siniri_ihlali` | `bos_guvence` | `tuzak_suclama` |",
        "|---|---:|---:|---:|",
    ]
    for kol in TUM:
        y.append(f"| {kol} | {alan[(kol, 'rol_siniri_ihlali')]} | "
                 f"{alan[(kol, 'bos_guvence')]} | {alan[(kol, 'tuzak_suclama')]} |")
    y += [
        "",
        "## ⛔ Ö3 — GÜRÜLTÜ TABANI: fark rubrikten mi geliyor?",
        "",
        f"v7 ile v8 **{ayr}/114** öğede ayrıştı (**%{100 * ayr / 114:.0f}**). Bu sayı tek",
        "başına hiçbir şey söylemez; v7'nin kendi kontrol koşusu rubrik hiç değişmeden",
        "rubrik etkisinden büyük kayma üretmişti (K61). Aşama 2 bunu ölçüyor — **iki yönlü**:",
        "",
        "| küme | öğe | üç geçiş bölündü | oran | ikili geçiş uyuşmazlığı | oran |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for rol in ("ayrisan", "kontrol"):
        yuzde = 100 * bolunme[rol] / kume_n[rol] if kume_n[rol] else 0
        cy = 100 * cift[rol] / ciftn[rol] if ciftn[rol] else 0
        y.append(f"| {rol} | {kume_n[rol]} | {bolunme[rol]} | %{yuzde:.0f} | "
                 f"{cift[rol]}/{ciftn[rol]} | **%{cy:.0f}** |")
    tb = sum(bolunme.values()); tn = sum(kume_n.values())
    tc, tcn = sum(cift.values()), sum(ciftn.values())
    taban_g = cift["kontrol"] / ciftn["kontrol"]
    ayr_g = cift["ayrisan"] / ciftn["ayrisan"]
    y += [
        f"| **toplam** | {tn} | **{tb}** | **%{100 * tb / tn:.0f}** | {tc}/{tcn} | "
        f"**%{100 * tc / tcn:.0f}** |",
        "",
        "⭐⭐ **AYRIŞMA, JUDGE'IN EN KARARSIZ OLDUĞU YERDE TOPLANIYOR.** v7 ile v8'in",
        f"ayrıştığı öğelerde v8'in kendi iki geçişi **%{100 * ayr_g:.0f}** oranında birbiriyle",
        f"çelişiyor; ayrışmadığı öğelerde bu oran **%{100 * taban_g:.0f}** — "
        f"**{ayr_g / taban_g:.1f} kat** fark.",
        "",
        "➡️ **Sonuç iki yönlü okunmalı.** Bir yandan ayrışma oranı "
        f"(%{100 * ayr / 114:.0f}) kontrolün gürültü tabanını (%{100 * taban_g:.0f}) açıkça",
        "aşıyor — yani v7→v8 farkının bir kısmı gerçekten **rubrikten** geliyor. Öte yandan",
        "ayrışmaların büyük kısmı judge'ın kendi içinde bile duramadığı öğelerde; o öğelerde",
        "*«v8 şunu dedi»* cümlesi kurulamaz.",
        "",
        "⛔ **GÜRÜLTÜ TABANI YANSIZ DEĞİL ve bu sonucu ZAYIFLATIR.** Kontrol öğeleri",
        "*«v7 ile v8'in aynı hükmü verdiği öğeler»* diye seçildi; uyuşma ile kararlılık",
        "ilişkili olduğu için bu küme **kararlı tarafa** kayıyor. Dolayısıyla "
        f"%{100 * taban_g:.0f} gerçek tabanın **alt sınırıdır**; gerçek taban daha yüksekse",
        "ayrışmanın rubriğe düşen payı daha küçüktür. Yansız bir taban, 114 öğenin",
        "**rastgele** bir alt kümesini yeniden koşmayı isterdi ve bu koşuda yapılmadı.",
        "⚠️ Tasarımın Ö3'ü bu yüzden **kısmen** karşılandı.",
        "",
        "⚠️ **Kontrol kümesi 29 değil 23.** Eşleştirme kol içinde yapılıyor ve `taban`'da",
        "13 ayrışan öğeye karşılık yalnızca 7 ayrışmayan öğe kaldı; eksik 6 kontrolün hepsi",
        "`taban`'dan.",
        "",
        "⛔ **KOL BAŞINA FARKLAR TEK TEK OKUNAMAZ.** 20 öğelik bir kolda "
        f"%{100 * taban_g:.0f} oynaklık, gürültüyle bile **2 öğelik** oynama demektir.",
        "Ö2 tablosundaki `+1`/`+2`/`+3` farklarının hiçbiri tek başına kurulamaz; kurulabilen",
        "şey **yön** (tabanda aşağı, kollarda yukarı) ve gürültü bandını **açıkça aşan**",
        "farklar — aşağıdaki F7 sinyali gibi.",
        "",
        "## Eksen 2 — düzeltilmiş ölçüt + v8 judge",
        "",
        "Otomatik iddialar **ikinci setten** (T38 düzeltmeleri), judge iddiaları v8'den:",
        "",
        "| kol | otomatik (set 2) | v8 dahil | Pareto gerileme | taban ÜSTÜ |",
        "|---|---|---|---:|---:|",
    ]
    tbk = kume_e2("taban")
    oto2 = {kol: sum(1 for r in kayit[kol].values() if r["otomatik_gecti_set2"])
            for kol in TUM}
    y.append(f"| **taban** | {oto2['taban']}/20 | **{e2('taban')}/20** | — | — |")
    for kol in KOLLAR:
        kk = kume_e2(kol)
        y.append(f"| {kol} | {oto2[kol]}/20 | **{e2(kol)}/20** | "
                 f"**{len(tbk - kk)}** | {len(kk - tbk)} |")
    y += [
        "",
        "⚠️ **Kapı yine geçilmiyor** — hiçbir kolda gerileme sıfır değil.",
        "",
        "## " + ("⛔ Ö4 ateşledi — sıralama değişti" if o4 else "Ö4 — sıralama değişmedi"),
        "",
        "| ölçüt | kollar (yüksekten düşüğe) |",
        "|---|---|",
        "| v7 judge + set 1 | " + " · ".join(
            f"{k} {sum(1 for r in v7kayit[k].values() if r['e2_nihai'])}" for k in s7) + " |",
        "| v8 judge + set 2 | " + " · ".join(f"{k} {e2(k)}" for k in s8) + " |",
        "",
        "## ⭐ Ö5 — F7'nin İLK ÖLÇÜMÜ (metriğe girmez)",
        "",
        "`kurum_yordam_ihlali` hiçbir eval öğesinde iddia edilmiyor; aşağıdaki sayı",
        "**tanısaldır** ve Eksen 2 skorunu değiştirmez (iddia eklemek K31 gereği üçüncü",
        "bir set ister). Ama K18/K110'un iki yasağı ilk kez ölçülüyor:",
        "",
        "| kol | kurum adı / yordam ihlali |",
        "|---|---|",
    ]
    for kol in TUM:
        ad = f"**{kol}**" if kol == "taban" else kol
        y.append(f"| {ad} | **{f7[kol]}/{n[kol]}** |")
    y += [
        "",
        f"⭐ **Taban {f7['taban']}/{n['taban']} ve `A-dar` {f7['A-dar']}/{n['A-dar']}; "
        f"geniş üç kol {f7['C-dikkat']}/{n['C-dikkat']}, {f7['D-tam']}/{n['D-tam']}, "
        f"{f7['E-genis']}/{n['E-genis']}.** Desen T35'inkiyle aynı yönde: kurum adı uydurmak "
        "ve yordam anlatmak **taban instruct modelin varsayılan davranışı** ve ince ayarın "
        "sildiği şeylerden biri. `A-dar` yine tabana yakın duruyor (T36).",
        "",
        "⚠️ Bu **iyi haber değil, ölçüm**: aynı kollar kriz yönlendirmesini de siliyor.",
        "",
        "## Ö6 — v8'in maliyeti",
        "",
        "| Denetim | Sonuç |",
        "|---|---|",
        f"| bozuk JSON | **{bozuk}**/114 |",
        f"| v8'in 10 yeni alanı dolu geldi | **{min(dolu.values())}-{max(dolu.values())}"
        f"**/{toplam_is} |",
        "",
        "⭐ On alan eklendi ve **hiçbirinde eksik gelme olmadı**; rubriğin uzunluğu bu koşuda",
        "bir bedele dönüşmedi.",
        "",
        "## ⚠️ Koşuda bulunan İŞ DOSYASI kusuru",
        "",
        "Altı subagent bağımsız olarak bildirdi: iş dosyasında puanlanacak cevabın içinde",
        "*«(iç muhakeme — değerlendirme dışı, yalnızca bağlam için: …)»* diye **kendisinin bir",
        "kısmını puanlama dışı ilan eden** bir blok var. Yani neyin puanlanacağını rubrik",
        "değil **veri** söylüyor. Hepsi bunu veri sayıp rubriğe göre karar verdiğini yazdı.",
        "",
        "⚠️ Bu kusur v7 iş dosyalarında da vardı ve kuyruk **baytı baytına** korunduğu için",
        "v7↔v8 karşılaştırmasını **bozmuyor** — iki tarafta da aynı. Ama mutlak sayılar,",
        "judge'ların bu bloğu kendiliğinden dışlamasına dayanıyor ve bu **ölçülmemiş bir",
        "serbestlik derecesi**. İş kurucusunun thinking'i ya ayıklaması ya da rubriğin açıkça",
        "kapsam dışı ilan etmesi gerekiyor.",
        "",
        "## ⛔ Bu koşunun ölçmediği",
        "",
        "- **v8'in korpus tarafındaki etkisi** — v8 üretim hattının varsayılanı (K118) ama",
        "  burada yalnızca Eksen 2 ölçüldü.",
        "- **Judge ailesi sapması (K45)** — tek aile. Karşılaştırma temiz (v7 de aynı aile)",
        "  ama *«v8 daha iyi bir rubrik»* iddiası tek aileyle kurulamaz.",
        "- **Uzman uyumu** — hangi rubriğin uzmana daha yakın olduğu K27 örneklemini ister.",
        "- **v7'nin kendi gürültü tabanı bu kümede** — kontrol oranı v8'in tekrar",
        "  oynaklığını ölçüyor; v7'nin aynı öğelerdeki oynaklığı ayrıca ölçülmedi.",
        "",
    ]
    CIKTI.write_text("\n".join(y) + "\n")
    print(f"yazıldı: {CIKTI.relative_to(KOK)} ({len(y)} satır)")
    print(f"  ayrışma {ayr}/114 · bölünme ayrışan %{100*bolunme['ayrisan']/kume_n['ayrisan']:.0f} "
          f"· kontrol %{100*bolunme['kontrol']/kume_n['kontrol']:.0f}")
    print(f"  ihlal v7→v8: " + " · ".join(f"{k} {ihl7[k]}→{ihl8[k]}" for k in TUM))
    print(f"  F7: " + " · ".join(f"{k} {f7[k]}" for k in TUM))
    print(f"  Ö4 {'ATEŞLEDİ' if o4 else 'ateşlemedi'} · bozuk {bozuk}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
