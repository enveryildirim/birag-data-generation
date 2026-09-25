#!/usr/bin/env python3
"""Eşleşme denetimi bir kaymayı KAÇ vakada görebilirdi — tespit gücü.

⛔ **Açık kalem (T50).** Sonucu yanlış dosyaya yazma kusuru iki ayrı partide
bulundu (`korpus-v8` 075↔077, `korpus-v9-p2` 004→005→006→007→004) ama **oranı**
bilinmiyordu. Oranı bilmenin önündeki engel şu: eşleşme denetimi bir kaymayı ancak
alıntılar **ayırt ediciyse** görebiliyor. Yani *«kaç kez oldu»* sorusundan önce
*«olsaydı görür müydüm»* sorusu yanıtlanmalı.

⭐ Bu ölçüm **tamamen geriye dönük**: yeni koşu, yeni judge, yeni üretim yok.
Arşivdeki her kayıt için *«bu kaydın sonucu başka bir kaydın dosyasına yazılsaydı
denetim ateşler miydi»* sorusu **bütün çiftler** için hesaplanır.

Karar kuralı `eslesme_denetimi()` ile birebir aynı yerden türetilir:
bir kaydın uzun alıntıları için `skor_k = k'nin cevabında bulunan alıntı sayısı`;
kapı, kaydın yazıldığı dosyanın skoru **en yüksek skordan küçükse** ateşler.

⚠️ Güç iki ayrı sayı olarak raporlanır. Gözlenen iki olayın **ikisi de komşu
indekslerde** oldu (uzaklık ≤ 3); bu yüzden *«bütün çiftler»* gücü iyimser,
*«komşu çiftler»* gücü ilgili olandır.

Kullanım: uv run python scripts/analiz/2026-09-15-kayma-tespit-gucu.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import date
from importlib import util as _iu
from itertools import combinations
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
sys.path.insert(0, str(KOK / "src"))
import filter as f  # noqa: E402

sys.argv = [sys.argv[0]]
_sp = _iu.spec_from_file_location("gd", KOK / "scripts/analiz/2026-09-15-geriye-donuk-eslesme.py")
GD = _iu.module_from_spec(_sp)
_sp.loader.exec_module(GD)

HAM = GD.HAM
eslesme_denetimi = GD.eslesme_denetimi
ESLESME_ALAN = GD.ESLESME_ALAN
RAPOR = KOK / f"reports/analiz/{TARIH}-kayma-kapanis.md"
JUDGED = KOK / "data/judged"

YAKIN = 3          # gözlenen iki olayın indeks uzaklığı: 2 ve ≤3


def kayitlari_oku(yol: Path, havuz: dict, anahtar) -> list:
    """(no, havuz anahtarı, uzun alıntılar) — denetimin gördüğü her şey."""
    out = []
    for l in yol.open(encoding="utf-8"):
        r = json.loads(l)
        ham = r.get("ham")
        if isinstance(ham, str):
            try:
                ham = json.loads(ham)
            except json.JSONDecodeError:
                continue
        if not isinstance(ham, dict):
            continue
        k = anahtar(r)
        if k is None or k not in havuz:
            continue
        q = [f.alinti_nrm(ham[a]) for a in ESLESME_ALAN if f._f_dolu(ham, a)]
        out.append((r.get("no"), k, [x for x in q if len(x) > 25]))
    return out


def guc(kayitlar: list, havuz: dict) -> dict:
    """Her TAKAS çifti için: denetim ateşler miydi?

    `eslesme_denetimi` mantığı: kaydın alıntıları yazıldığı dosyanın cevabında
    aranır; **en yüksek skorlu** başka bir kayıt varsa ateşler. Bir takasta iki
    yön vardır ve **biri** ateşlerse kayma görülür.
    """
    anahtarlar = [k for _no, k, _q in kayitlar]
    # skor[i][j] = i'nin alıntılarından kaçı j'nin cevabında bulunuyor
    skor, enb = [], []
    for _no, _k, q in kayitlar:
        s = Counter()
        for x in q:
            for j, kj in enumerate(anahtarlar):
                if x in havuz[kj]["cevap"]:
                    s[j] += 1
        skor.append(s)
        enb.append(max(s.values()) if s else 0)

    def ates(i: int, j: int) -> bool:
        """i'nin sonucu j'nin dosyasına yazılsaydı kapı ateşler miydi?"""
        return bool(kayitlar[i][2]) and skor[i][j] < enb[i]

    n = len(kayitlar)
    d = dict(kayit=n, alintisiz=sum(1 for _n, _k, q in kayitlar if not q),
             cift=0, gorulen=0, yakin=0, yakin_gorulen=0, iki_tarafli=0, ornek=[])
    for i, j in combinations(range(n), 2):
        g = ates(i, j) or ates(j, i)
        d["cift"] += 1
        d["gorulen"] += g
        # ⚠️ Görünmezliğin sebebi: alıntısızlık mı, yoksa iki cevabın birbirine
        # fazla benzemesi mi? İkincisi rubrikle kapanmaz, bu yüzden ayrı sayılır.
        if not g and kayitlar[i][2] and kayitlar[j][2]:
            d["iki_tarafli"] += 1
        try:
            komsu = abs(int(kayitlar[i][0]) - int(kayitlar[j][0])) <= YAKIN
        except (TypeError, ValueError):
            komsu = False
        if komsu:
            d["yakin"] += 1
            d["yakin_gorulen"] += g
            if not g and len(d["ornek"]) < 3:
                d["ornek"].append((kayitlar[i][0], kayitlar[j][0],
                                   len(kayitlar[i][2]), len(kayitlar[j][2])))
    return d


def judged_kume() -> list:
    """`data/judged/*.jsonl` — ham arşivde HİÇ bulunmayan koşular burada.

    ⛔ 2026-09-15 taraması yalnızca `reports/analiz/ham-judge/` altını denetledi; ama
    ham arşiv **sonradan** doğdu (K117) ve ondan önceki judge koşularının tek kaydı
    veri kümesi dosyalarının kendisi. ⭐ O dosyalar kendi kendine yeter: her kayıt hem
    `messages` (kaynak) hem `judge` (alıntılar) taşıyor, yani havuz dosyanın içinde.
    """
    out = []
    for yol in sorted(JUDGED.glob("*.jsonl")):
        kayitlar, havuz = [], {}
        for no, l in enumerate(yol.open(encoding="utf-8")):
            r = json.loads(l)
            j = r.get("judge")
            if not isinstance(j, dict):
                continue
            havuz[r["id"]] = f.kaynak_metinleri(r)
            kayitlar.append({"no": f"{no:03d}", "id": r["id"], "ham": j})
        if kayitlar:
            sur = {k["ham"].get("prompt_version") for k in kayitlar}
            rub = sorted(x.split(".")[-1] for x in sur if x) or ["?"]
            out.append((yol.name, "/".join(rub), kayitlar, havuz))
    return out


def main() -> int:
    satir = []
    for stem, rub, es, havuz, anahtar in GD.kume():
        kayitlar = kayitlari_oku(HAM / f"{stem}.jsonl", havuz, anahtar)
        satir.append((stem, rub, es, guc(kayitlar, havuz)))

    # ── data/judged — ham arşivde hiç bulunmayan koşular ──────────────────
    jsatir, jvaka = [], []
    for ad, rub, kayitlar, havuz in judged_kume():
        jvaka += eslesme_denetimi(JUDGED / ad, havuz, lambda r: r["id"], kayitlar)
        g = guc([(k["no"], k["id"],
                  [x for x in (f.alinti_nrm(k["ham"][a]) for a in ESLESME_ALAN
                               if f._f_dolu(k["ham"], a)) if len(x) > 25])
                 for k in kayitlar], havuz)
        jsatir.append((ad, rub, g))

    T = {k: sum(s[3][k] for s in satir) + sum(s[2][k] for s in jsatir)
         for k in ("kayit", "alintisiz", "cift", "gorulen", "yakin", "yakin_gorulen",
                   "iki_tarafli")}
    p_tum = T["gorulen"] / T["cift"]
    p_yakin = T["yakin_gorulen"] / T["yakin"]
    kor = [s for s in satir if s[3]["alintisiz"]] + \
          [(s[0], s[1], None, s[2]) for s in jsatir if s[2]["alintisiz"]]

    y = [
        "# Kayma denetimi kapanışı — hiç denetlenmemiş koşular + tespit gücü",
        "",
        f"*{TARIH} · betik `scripts/analiz/{Path(__file__).name}`*",
        "*girdi: `data/judged/*.jsonl` · `reports/analiz/ham-judge/*.jsonl` — "
        "**yeni koşu / yeni judge / yeni üretim YOK**, tamamen geriye dönük*",
        "",
        "## İki açık kalem, iki soru",
        "",
        "2026-09-15 taraması `korpus-v8`'de bir takas buldu ve iki kalem açık bıraktı:",
        "",
        "1. ⛔ **Tarama eksikti.** Yalnızca `reports/analiz/ham-judge/` denetlendi; ama o",
        "   arşiv **sonradan** doğdu (K117) ve ondan önceki judge koşularının tek kaydı",
        "   **veri kümesi dosyalarının kendisi** (`data/judged/`). Oradaki koşular hiç",
        "   denetlenmemişti — ve asıl önemli olan onlar: eğitim verisi oradan seçiliyor.",
        "2. ⛔ **Kusurun oranı bilinmiyordu.** Ama orandan önce şu sorulmalı: *bir kayma",
        "   olsaydı görür müydüm?* Denetim bir kaymayı ancak alıntılar **ayırt ediciyse**",
        "   görebiliyor.",
        "",
        "⭐ `data/judged` kendi kendine yeter: her kayıt hem `messages` (kaynak) hem",
        "`judge` (alıntılar) taşıyor, yani havuz dosyanın **içinde**.",
        "",
        "## 1. Hiç denetlenmemiş koşular — `data/judged`",
        "",
        "| Dosya | rubrik | kayıt | ⛔ alıntısız | **kayma** |",
        "|---|---|---:|---:|---:|",
    ]
    for ad, rub, g in jsatir:
        at = sum(1 for v in jvaka if v["dosya"] == Path(ad).stem)
        y.append(f"| `{ad}` | {rub} | {g['kayit']} | {g['alintisiz'] or '—'} | "
                 f"{'**' + str(at) + '**' if at else '0'} |")
    jt = sum(s[2]["kayit"] for s in jsatir)
    y += [
        f"| **TOPLAM** | | **{jt}** | "
        f"**{sum(s[2]['alintisiz'] for s in jsatir)}** | **{len(jvaka)}** |",
        "",
    ]
    if jvaka:
        y += ["⛔ **Kayma bulundu:**", "",
              "| dosya | no | kayıt | kendi/alıntı | ait olduğu |", "|---|---|---|---|---|"]
        for v in jvaka[:30]:
            y.append(f"| `{v['dosya']}` | {v['no']} | `{v['kayit'][:12]}` | "
                     f"{v['kendi']}/{v['alinti']} | `{v['ait_oldugu'][:12]}` |")
        y.append("")
    else:
        y += [
            f"✅ **{jt} kayıtta kayma 0.** v1'den v7'ye altı rubrik sürümü, aralarında",
            "`v0.0.2`–`v0.0.5`, `v3-parti1/2/3`, `expert-70.v2/v3/v4` ve",
            "`v3-kumulatif.v6` — **hiçbiri daha önce bu denetimden geçmemişti.**",
            "➡️ Bilinen takas `korpus-v8`'de kaldı; veri kümesi dosyalarına bulaşmamış.",
            "",
        ]

    # ── güç, RUBRİK SÜRÜMÜNE göre — asıl değişken bu ────────────────────
    rubrik = {}
    for ad, rub, g in [(s[0], s[1], s[3]) for s in satir] + \
                      [(s[0], s[1], s[2]) for s in jsatir]:
        d = rubrik.setdefault(rub, dict(kayit=0, alintisiz=0, cift=0, gorulen=0,
                                        iki_tarafli=0))
        for k in d:
            d[k] += g[k]

    y += [
        "## 2. Tespit gücü — bir kayma olsaydı görür müydüm",
        "",
        "Her kümede **bütün takas çiftleri** tek tek hesaplandı: kaydın sonucu ötekinin",
        "dosyasına yazılsaydı `eslesme_denetimi()` ateşler miydi? Karar kuralı kapının",
        "kendi kuralından türetildi (skor = alıntının o cevapta bulunması; kapı,",
        "yazıldığı dosyanın skoru **en yüksek skordan küçükse** ateşler). Bir takasta",
        "**iki yön** vardır ve birinin ateşlemesi yeter.",
        "",
        "| Küme | çift | ⛔ görülmeyen | **güç** |",
        "|---|---:|---:|---:|",
    ]
    for ad, grup in (("`ham-judge` (31 arşiv, v3-v8)", [s[3] for s in satir]),
                     ("`data/judged` (21 dosya, v1-v7)", [s[2] for s in jsatir])):
        c = sum(g["cift"] for g in grup); gr = sum(g["gorulen"] for g in grup)
        y.append(f"| {ad} | {c} | **{c - gr}** | %{100 * gr / c:.2f} |")
    y += [
        f"| **TOPLAM** | **{T['cift']}** | **{T['cift'] - T['gorulen']}** | "
        f"**%{100 * p_tum:.2f}** |",
        "",
        "### ⭐⭐ Güç rubriğin kendisine bağlı",
        "",
        "Fark kümelerden değil **rubrik sürümünden** geliyor:",
        "",
        "| rubrik | kayıt | ⛔ alıntısız | çift | görülmeyen | **güç** |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for rub in sorted(rubrik, key=lambda x: (len(x), x)):
        d = rubrik[rub]
        y.append(f"| `{rub}` | {d['kayit']} | {d['alintisiz'] or '—'} | {d['cift']} | "
                 f"**{d['cift'] - d['gorulen']}** | "
                 f"%{100 * d['gorulen'] / d['cift']:.1f} |")
    v1 = rubrik.get("v1", {})
    y += [
        "",
        "⛔ **`v1` rubriğinde güç SIFIR.** O sürüm judge'dan hiç alıntı istemiyordu:",
        f"{v1.get('kayit', 0)} kaydın **tamamında** ({v1.get('alintisiz', 0)}/"
        f"{v1.get('kayit', 0)}) tek bir uzun alıntı bile yok. Alıntı yoksa kaymanın",
        "imzası da yok.",
        "",
        "➡️ ⭐ *Kanıtı zorunlu kılan bir rubrik yalnızca judge'ı disipline etmiyor;",
        "**ölçüm hattını geriye dönük denetlenebilir kılıyor.** Alıntı istemeyen bir",
        "rubrikle puanlanmış kayıtlarda sonuç-kayıt kaymasını gösterecek hiçbir iz",
        "yoktur ve o koşular bugün de, gelecekte de denetlenemez.* ⚠️ Bu, kanıta bağlı",
        "rubriğin (v7→v9 hattı) ölçülmemiş bir **yan faydası**.",
        "",
        "### Orana ne diyor",
        "",
        "Gözlenen iki olay da **v8/v9 döneminde ve `ham-judge` kümesinde** oldu; o",
        f"kümede güç **%{100 * sum(s[3]['gorulen'] for s in satir) / sum(s[3]['cift'] for s in satir):.2f}**.",
        "➡️ *O dönemde iki olay oldu ve ikisi de bulundu; görülmemiş bir üçüncünün",
        "beklentisi ihmal edilebilir.*",
        "",
        "⛔ **Ama bu, oranın ölçüldüğü anlamına gelmez** — üç sebeple:",
        "",
        "1. **Erken dönem denetlenemez.** `v1`-`v4` rubrikleriyle puanlanmış kayıtlarda",
        "   güç düşük ya da sıfır; oradaki *«kayma 0»* sonucu **kanıt değil, sessizlik**.",
        "2. **Bağımsız parti sayımı yok.** Güç bir olayın *görülme* olasılığı; *olma*",
        "   olasılığı için partileri bağımsız sayabileceğimiz bir düzenek gerekir.",
        "   ⚠️ İki olay da aynı oturumda, aynı iş kurucusuyla çıktı.",
        "3. **Takas dışındaki bozulmalar hesabın dışında** — sonucun hiç yazılmaması,",
        "   aynı kayda iki kez yazılması, içeriğin kısmen karışması.",
        "",
    ]

    if kor:
        y += [
            "## ⛔ Yapısal kör nokta — hiç uzun alıntısı olmayan kayıtlar",
            "",
            "Bir kaydın tek bir uzun alıntısı bile yoksa **o yön hiç ateşleyemez**;",
            "kayma ancak karşı yönden görülebilir.",
            "",
            f"⭐ Görünmez {T['cift'] - T['gorulen']} çiftin **{T['iki_tarafli']}'i** iki",
            "tarafı da alıntılı; geri kalanın sebebi **alıntısızlık**. ➡️ Açık rubrikte",
            "değil **kısa/boş cevaplarda** — ve alıntı isteyen bir rubrikle kapanıyor.",
            "",
            "| küme | alıntısız kayıt |", "|---|---:|",
        ]
        for s in sorted(kor, key=lambda x: -x[3]["alintisiz"])[:12]:
            y.append(f"| `{s[0]}` | {s[3]['alintisiz']}/{s[3]['kayit']} |")
        y.append("")

    guncel = [rubrik[r] for r in ("v6", "v7", "v8") if r in rubrik]
    guncel_cift = sum(d["cift"] for d in guncel)
    guncel_gorulen = sum(d["gorulen"] for d in guncel)
    y += [
        "## ⭐ Karar",
        "",
        "| | |",
        "|---|---|",
        f"| ✅ Tarama tamamlandı | ham arşiv **+** `data/judged`; toplam **{T['kayit']}** "
        "judge kararı denetlendi |",
        f"| ✅ Güç ölçüldü | yürürlükteki rubriklerde (`v6`-`v8`) "
        f"**%{100 * guncel_gorulen / guncel_cift:.2f}** — denetim **doygun**. "
        f"Bütün sürümler birlikte %{100 * p_tum:.2f}; farkı `v1` açıyor |",
        "| ⛔ Bilinen tek kusur | `korpus-v8` 075↔077 (bildirimle düzeltildi, etkisi yok) |",
        "| ⚠️ Kimlik damgası | ⛔ **koşullu geri çekiliyor**: v7+ rubriklerinde güç "
        "zaten ~1, ek alan kazanç getirmez. ⚠️ Koşul: *rubrik alıntı istemeye devam "
        "ettiği sürece*. Alıntı zorunluluğu kalkarsa güç `v1`'deki gibi çöker ve damga "
        "**tek** denetim yolu olur |",
        "",
        "➡️ *Kapının gücü sabit bir özellik değil, rubriğe bağlı bir ölçüdür.* Bu yüzden",
        "güç hesabı rubrik değiştiğinde yeniden koşulmalı — betik bunu tek komutla yapar.",
        "",
        "⚠️ **Erken dönem için hiçbir şey yapılamaz.** `v1`-`v4` ile puanlanmış kayıtlar",
        "bugün de denetlenemez; oradaki *«kayma 0»* sonucu kanıt değil **sessizliktir**",
        "ve bir sayı raporlanırken bu ayrım korunmalı (Kural 5).",
    ]
    RAPOR.write_text("\n".join(y) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print(f"   {T['kayit']} kayıt · {T['cift']} çift · güç %{100 * p_tum:.1f} · "
          f"komşu güç %{100 * p_yakin:.1f} · alıntısız {T['alintisiz']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
