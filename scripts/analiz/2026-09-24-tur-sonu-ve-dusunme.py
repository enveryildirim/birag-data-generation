#!/usr/bin/env python3
"""Tur sonu ve düşünme — «her cevap soruyla bitiyor» ve «düşünme dar» gözlemleri.

⭐ Soru demodan doğdu (2026-09-24, kullanıcı): ince ayarlı model cevaplarını hep
soruyla bitiriyor ve düşünmesi dar. Önerilen iki çare (tur sonunda takdir /
teşekkür; düşünmeye beş başlıklı bir şablon) değerlendirilmeden önce iki şey
ölçülür: **veri bunu mu öğretiyor, model veriden mi sapıyor?**

**Yeni koşu yok.** Girdiler:
  * `datasets/v0.1.0/train.jsonl` — son asistan turu (eğitim hedefi, `mask_prompt`)
  * kayıtlı eksen koşuları — taban (`taban-0924-*`, T278) + `d1`/`e3` × 8 tohum
    (EK-1 hücreleri, T277). `forget` dışarıda: genel yetenek soruları, orada tur
    sonu terapötik bir seçim değil.

⭐ Ölçüt KOPYALANMIYOR (K103): döngü tanımı ve cümle normalleştirmesi T279
betiğinden, hücreler EK-1 çözümlemesinden import edilir.

⛔ Bütün ölçüler BETİMLEYİCİDİR — eşik yok, kapı değil. Anahtar sözcük ölçüleri
vekildir (ör. «sormuyorum» bir karşıtlık cümlesinde de geçer: *«X'i sormuyorum,
Y'yi soruyorum»*). ⛔ Taban İngilizce düşünüyor (K46) ⇒ Türkçe anahtar sözcük
satırlarında taban sütunu dil farkını taşır, yalnız biçim satırı karşılaştırılır.

Çıktı: reports/analiz/2026-09-24-tur-sonu-ve-dusunme.md
"""
from __future__ import annotations

import collections
import hashlib
import json
import math
import re
import statistics as st
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from tohum_guvenlik import tr_fold  # noqa: E402

TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-tur-sonu-ve-dusunme.md"
VERI = KOK / "datasets/v0.1.0/train.jsonl"
VERI_SHA = "6fcb6b1e16290575"                # datasets/v0.1.0/CARD.md
EK = KOK / "reports/analiz/eksen-kosu"
BITIS = ("acik_uclu_soru", "takdir", "ozet", "yalnizca_yansitma", "durur")
KOLLAR = ("taban", "d1", "e3")

_sp = _iu.spec_from_file_location(
    "_dd", KOK / "scripts/analiz/2026-09-24-dusunme-dongusu.py")
D = _iu.module_from_spec(_sp)
_sp.loader.exec_module(D)
C = D.C                                      # EK-1 çözümlemesi (T277)

SORMUYORUM = re.compile(r"sormuyorum")
# (desen, tr_fold'lu metinde mi) — biçim ve işaret ham metinde aranır
VEKIL = {
    "madde / başlık biçimi (`**`, madde imi, numara)":
        (re.compile(r"\*\*|^\s*[*\-•]\s|^\s*\d+\.\s", re.M), False),
    "sistem kuralını anıyor (*tek seferde* · *kural* · *protokol*)":
        (re.compile(r"tek seferde|\bkural|protokol"), True),
    "«sormuyorum»": (SORMUYORUM, True),
    "⛔ / ⭐ işareti": (re.compile("⛔|⭐"), False),
}
OLUMSUZ = re.compile(r"\w+m[iuü]yorum\b|\w+m[ae]y[ae]c[ae][ğk]im\b")   # tr_fold'lu
KALIP_SOZCUK, KALIP_KAYIT = 3, 5


def soru_bitis(t: str | None) -> bool:
    return re.sub(r"[\s\"'»”)\]*_]+$", "", (t or "").strip()).endswith("?")


def cumle_bol(t: str | None) -> list[str]:
    return [s for s in re.split(r"(?<=[.!?])\s+|\n+", (t or "").strip()) if s.strip()]


def kalip_cumleler(t: str | None) -> list[tuple[str, str]]:
    """[(anahtar, ham cümle)] — korpus düzeyi kalıp sayımı için. ⚠️ T279'un döngü
    ölçüsü DEĞİL: orada eşik ≥ 4 sözcük; burada 3 — *«soru sormuyorum,
    özetlemiyorum»* gibi üç sözcüklük kalıplar dört sözcük eşiğinin altında kalıyor."""
    out = []
    for ham in cumle_bol(t):
        c = re.sub(r"\s+", " ", re.sub(r"[^\w ]", "", tr_fold(ham))).strip()
        if len(c.split()) >= KALIP_SOZCUK:
            out.append((c, ham.strip()))
    return out


def soru_payi(t: str) -> float:
    c = cumle_bol(t)
    return sum(1 for s in c if soru_bitis(s)) / len(c) if c else 0.0


def ort_se(x: list[float], ond: int = 1) -> str:
    if len(x) < 2:
        return f"{x[0]:.{ond}f}"
    return f"{st.mean(x):.{ond}f} ± {2 * st.stdev(x) / math.sqrt(len(x)):.{ond}f}"


def yuzde(k: int, n: int) -> str:
    return f"{k}/{n} ({100 * k / n:.0f}%)" if n else "—"


def son_asistan(r: dict) -> dict:
    return [m for m in r["messages"] if m["role"] == "assistant"][-1]


def _veri() -> list[dict]:
    s = hashlib.sha256(VERI.read_bytes()).hexdigest()[:16]
    if s != VERI_SHA:
        raise SystemExit(f"⛔ v0.1.0 değişmiş: {s} ≠ {VERI_SHA}")
    return [json.loads(x) for x in VERI.read_text(encoding="utf-8").splitlines() if x.strip()]


def _model() -> dict:
    """kol → tohum → [satır] (forget hariç eksenler birleşik)."""
    eksen = [k for k, _ in C._ek.EKSEN if k != "forget"]
    h = C._hucreler()
    out = {"taban": {0: {k: C._satirlar(sorted(EK.glob(f"*-taban-0924-{k}"))[-1])
                         for k in eksen}}}
    for kol in ("d1", "e3"):
        out[kol] = {t: {k: C._satirlar(h[(kol, t, k)]) for k in eksen} for t in C._ek.TOHUM}
    return out


def main() -> int:
    rs = _veri()
    M = _model()
    eksenler = list(next(iter(M["taban"].values())))
    s = ["# Tur sonu ve düşünme — «hep soru» ve «dar düşünme» ölçüldü", "",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
         f"**Girdi:** `datasets/v0.1.0/train.jsonl` SHA256-16 `{VERI_SHA}` ({len(rs)} kayıt; "
         "son asistan turu = eğitim hedefi, `mask_prompt`) · kayıtlı eksen koşuları: taban "
         "tek koşu, `d1` (v0.0.18) / `e3` (v0.1.0) 8 tohum, `forget` hariç "
         f"{len(eksenler)} eksen. **Yeni koşu yok.** Tohumlu değerler ort ± 2·SE.", ""]

    # ── 1. veri ──
    son = [son_asistan(r) for r in rs]
    beyan = collections.Counter(r["gen_meta"].get("turn_ending") for r in rs)
    tut = collections.defaultdict(collections.Counter)
    for r, a in zip(rs, son):
        tut[r["gen_meta"].get("turn_ending")][soru_bitis(a["content"])] += 1
    s += ["## 1. Veri tur sonunu nasıl öğretiyor", "",
          "### 1a. Beyan ve metin", "",
          "| beyan (`gen_meta.turn_ending`) | kayıt | metni `?` ile biten |", "|---|---:|---:|"]
    for b, n in beyan.most_common():
        s.append(f"| `{b}` | {n} ({100 * n / len(rs):.1f}%) | {tut[b][True]} |")
    q_son = sum(soru_bitis(a["content"]) for a in son)
    s += ["", f"Son tur soruyla biten: **{yuzde(q_son, len(rs))}**.", ""]

    ct = collections.defaultdict(collections.Counter)
    for r in rs:
        ct[r["gen_meta"].get("konusma_durumu")][r["gen_meta"].get("turn_ending")] += 1
    s += ["### 1b. Bitiş bağlama göre değişiyor mu — `konusma_durumu` × `turn_ending` (satır %)", "",
          "| bağlam | kayıt | " + " | ".join(f"`{b}`" for b in BITIS) + " | en sık |",
          "|---|---:|" + "---:|" * len(BITIS) + "---|"]
    mod_soru = 0
    baglamlar = [k for k in ct if k]
    for k in sorted(baglamlar, key=lambda x: -sum(ct[x].values())):
        v, n = ct[k], sum(ct[k].values())
        en = max(BITIS, key=lambda b: v[b])
        mod_soru += en == "acik_uclu_soru"
        s.append(f"| `{k}` | {n} | " + " | ".join(f"{100 * v[b] / n:.0f}" for b in BITIS)
                 + f" | `{en}` |")
    s += ["", f"En sık bitişin `acik_uclu_soru` olduğu bağlam: **{mod_soru} / {len(baglamlar)}**.", ""]

    seri = collections.defaultdict(collections.Counter)
    for r in rs:
        a = [m for m in r["messages"] if m["role"] == "assistant"]
        if len(a) < 2:
            continue
        ard = 0
        for m in reversed(a[:-1]):
            if not soru_bitis(m["content"]):
                break
            ard += 1
        seri[ard][soru_bitis(a[-1]["content"])] += 1
    s += ["### 1c. Çok turlu kayıtlar — geçmiş, son turun bitişini belirliyor mu", "",
          "| son turdan hemen önceki ardışık soru-sonu | kayıt | son tur soruyla biten |",
          "|---:|---:|---:|"]
    for k in sorted(seri):
        v = seri[k]
        s.append(f"| {k} | {sum(v.values())} | {yuzde(v[True], sum(v.values()))} |")
    s.append("")

    # ── 2. model ──
    def dolu(rows):
        return [r for r in rows if (r.get("cevap") or "").strip()]

    s += ["## 2. Model ne yapıyor — tek turlu eval ögeleri", "",
          "### 2a. Soruyla biten cevap (%, dolu cevaplar)", "",
          "| eksen | taban | `d1` | `e3` |", "|---|---:|---:|---:|"]
    for k in eksenler + [None]:
        hucre = []
        for kol in KOLLAR:
            x = []
            for e in M[kol].values():
                rows = dolu([r for kk, v in e.items() if k in (None, kk) for r in v])
                x.append(100 * sum(soru_bitis(r["cevap"]) for r in rows) / len(rows))
            hucre.append(ort_se(x))
        s.append(f"| {'**hepsi**' if k is None else f'`{k}`'} | " + " | ".join(hucre) + " |")
    s += ["", "### 2b. Cevabın şekli", "",
          "| | ortanca sözcük | ortanca cümle | soru cümlesi payı (ort.) |", "|---|---:|---:|---:|"]
    sekil = [("veri (son tur)", [a["content"] for a in son])]
    sekil += [(f"`{kol}`", [r["cevap"] for e in M[kol].values() for v in e.values()
                            for r in dolu(v)]) for kol in KOLLAR]
    for ad, cv in sekil:
        s.append(f"| {ad} | {st.median(len(c.split()) for c in cv):.0f} | "
                 f"{st.median(len(cumle_bol(c)) for c in cv):.0f} | "
                 f"{100 * st.mean(soru_payi(c) for c in cv):.0f}% |")
    s.append("")

    # ── 3. düşünme ↔ bitiş ──
    def bag(pairs):
        """[(düşünme, cevap)] → (sorm, sorm&soru, yok, yok&soru)"""
        a = b = c = d = 0
        for th, cv in pairs:
            if SORMUYORUM.search(tr_fold(th or "")):
                a += 1
                b += soru_bitis(cv)
            else:
                c += 1
                d += soru_bitis(cv)
        return a, b, c, d

    va, vb, vc, vd = bag([(a.get("thinking"), a["content"]) for a in son if a.get("thinking")])
    s += ["## 3. Düşünme tur sonunu belirliyor mu", "",
          "Düşünmede «sormuyorum» geçen ve geçmeyen dolu cevapların soruyla bitme payı.", "",
          "| | «sormuyorum» geçen düşünme | bunların soruyla biten cevabı | geçmeyenlerin "
          "soruyla biten cevabı | fark (puan) | okuma |", "|---|---:|---:|---:|---:|---|"]
    fark_v = 100 * vb / va - 100 * vd / vc
    s.append(f"| veri | {yuzde(va, va + vc)} | {yuzde(vb, va)} | {yuzde(vd, vc)} | "
             f"{fark_v:+.0f} | tek küme |")
    for kol in ("d1", "e3"):
        top, fark = [0, 0, 0, 0], []
        for e in M[kol].values():
            a, b, c, d = bag([(r.get("thinking"), r["cevap"]) for v in e.values() for r in dolu(v)])
            top = [x + y for x, y in zip(top, (a, b, c, d))]
            fark.append(100 * b / a - 100 * d / c)
        se2 = 2 * st.stdev(fark) / math.sqrt(len(fark))
        okuma = "sıfırdan ayrılıyor" if abs(st.mean(fark)) > se2 else "sıfırdan ayırt edilemiyor"
        s.append(f"| `{kol}` | {yuzde(top[0], top[0] + top[2])} | {yuzde(top[1], top[0])} | "
                 f"{yuzde(top[3], top[2])} | {ort_se(fark, 0)} | {okuma} |")
    s += ["", "Taban satırı yok: taban İngilizce düşünüyor, «sormuyorum» hiç geçmiyor.", ""]

    # ── 4. düşünmenin içeriği ──
    thv = [a["thinking"] for a in son if a.get("thinking")]
    thm = {kol: [r.get("thinking") or "" for e in M[kol].values() for v in e.values() for r in v]
           for kol in KOLLAR}
    s += ["## 4. Düşünmenin içeriği", "",
          "### 4a. Uzunluk ve biçim (% düşünme)", "",
          "| | veri | taban | `d1` | `e3` |", "|---|---:|---:|---:|---:|",
          "| ortanca sözcük | " + " | ".join(
              f"{st.median(len(t.split()) for t in x):.0f}" for x in [thv] + [thm[k] for k in KOLLAR])
          + " |"]
    for ad, (p, fold) in VEKIL.items():
        hucre = []
        for x in [thv] + [thm[k] for k in KOLLAR]:
            hucre.append(f"{100 * sum(1 for t in x if p.search(tr_fold(t) if fold else t)) / len(x):.0f}")
        s.append(f"| {ad} | " + " | ".join(hucre) + " |")
    s.append("")

    cum = [c for t in thv for c in cumle_bol(t) if len(c.split()) >= 2]
    olz = sum(1 for c in cum if OLUMSUZ.search(tr_fold(c)))
    per = [sum(1 for c in cumle_bol(t) if OLUMSUZ.search(tr_fold(c))) for t in thv]
    tekrar, ornek = collections.Counter(), {}
    for t in thv:
        for c, ham in kalip_cumleler(t):
            ornek.setdefault(c, ham)
        tekrar.update({c for c, _ in kalip_cumleler(t)})
    sik = [(ornek[c], n) for c, n in tekrar.most_common() if n >= KALIP_KAYIT]
    s += ["### 4b. Veride olumsuz karar cümleleri", "",
          f"* Olumsuz birinci tekil fiil (*-mıyorum*, *-mayacağım*) içeren düşünme cümlesi: "
          f"**{yuzde(olz, len(cum))}**",
          f"* Kayıt başına ortanca: **{st.median(per):.0f}** · hiç olmayan kayıt: "
          f"{yuzde(sum(1 for x in per if x == 0), len(per))}",
          f"* Korpusta **≥ {KALIP_KAYIT} kayıtta** birebir geçen düşünme cümlesi "
          f"(≥ {KALIP_SOZCUK} sözcük, noktalamasız): **{len(sik)}**", ""]
    if sik:
        s += ["| cümle | kayıt |", "|---|---:|"] + [f"| *{c}* | {n} |" for c, n in sik] + [""]

    s += ["### 4c. Modelin döngüleri neyin etrafında dönüyor", "",
          "| kol | döngülü düşünme (T279 tanımı) | en çok tekrarlanan cümlesinde «soru» geçen |",
          "|---|---:|---:|"]
    for kol in ("d1", "e3"):
        dg = [t for t in thm[kol] if D.cumle_olcu(t)["dongu"]]
        soru = sum(1 for t in dg if "soru" in collections.Counter(D.cumleler(t)).most_common(1)[0][0])
        s.append(f"| `{kol}` | {yuzde(len(dg), len(thm[kol]))} | {yuzde(soru, len(dg))} |")

    s += ["", "## ⛔ Bunun söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ **Anahtar sözcük vekildir** | «sormuyorum» karşıtlık cümlesinde de geçer "
          f"(veride bu kayıtların {vb}'i yine soruyla bitiyor); olumsuz fiil deseni yalnız "
          "iki kip yakalar; *kural* başka anlamda da geçebilir |",
          "| ⛔ **Nedeni ölçülmedi** | §3 bağın koptuğunu gösterir; neden koptuğunu (bağdaştırıcı "
          "kapasitesi, taban eğilimi, açgözlü çözme) ayırmaz |",
          "| ⚠️ **Eval ögeleri eğitim konuşması değil** | tek turlu, ögenin kendi istemi, 1024 "
          "jeton; demo çok turlu ve kanonik system prompt ⇒ demodaki «her cevap soru» "
          "izlenimi **çok turda ölçülmedi** |",
          "| ⚠️ **Bitiş = son karakter** | soru ortada, son cümle yansıtmaysa soru sayılmaz |",
          "| ⚠️ **Taban tek koşu ve İngilizce düşünüyor** | yüzdeleri dağılım değil; Türkçe "
          "vekil satırlarında taban karşılaştırılamaz |"]
    RAPOR.write_text("\n".join(s) + "\n", encoding="utf-8")
    print("\n".join(s))
    print(f"\nyazıldı: {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
