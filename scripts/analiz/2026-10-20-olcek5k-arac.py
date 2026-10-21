#!/usr/bin/env python3
"""Ölçek-5k — üç aşamalı üretimin TEK aracı (ajanlar yalnız bunu çağırır).

Aşamalar (parça = 25 satır, `data/plan/olcek5k.jsonl`):
  A  (Haiku)  tohumdan KULLANICI tarafını yazar: kullanıcı turları, çok turluda
              kısa asistan açılışı, bağlam pasajı.        → olcek5k/A/parcaNNN.jsonl
  B  (Haiku)  SON CEVAP + thinking. ⛔ Tohumu GÖRMEZ — `b-girdi` tohumu vermez.
              v5 §3a′ *«mesaj yazılınca tohum kapatılır»* tek ajanda talimattı ve
              pilotta 60 kaydın 11'inde çiğnendi (2026-10-20-haiku-pilot-okuma.md);
              burada YAPI.                                  → olcek5k/B/parcaNNN.jsonl
  C  (Sonnet) hata avı: okur, düzeltir ya da düşürür.        → olcek5k/C/parcaNNN.jsonl
  `birlestir` A + (B|C) → kayıt, kapılar               → olcek5k/kayit/parcaNNN.jsonl

Komutlar:
  a-girdi N | a-kontrol N | b-girdi N | birlestir N B|C | c-girdi N | durum
Kapılar `haiku-pilot-birlestir` (← parti8 blok1) betiğinden içe aktarılır.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from checks import run_checks  # noqa: E402
from dilim import dilim  # noqa: E402
from kunye import betik_tarihi  # noqa: E402
import tohum_guvenlik as TG  # noqa: E402

_sp = _iu.spec_from_file_location("hpb", KOK / "scripts/analiz/2026-10-20-haiku-pilot-birlestir.py")
HPB = _iu.module_from_spec(_sp)
_sp.loader.exec_module(HPB)
B1 = HPB.B1

PLAN = KOK / "data/plan/olcek5k.jsonl"
# Tamamlama partisi (2026-10-21, v0.2.1): parça 201+, sıra 5001+ — ayrı dosya, v0.2.0'ın plan SHA'sı değişmesin.
PLAN_EK = KOK / "data/plan/olcek5k-ek.jsonl"
HAVUZ = KOK / "data/seeds.v2.jsonl"
DIZIN = KOK / "data/candidates/olcek5k"
PARTI = "olcek5k"
SORUSUZ = ("takdir", "ozet", "yalnizca_yansitma", "durur")
# Korpusun (v0.1.1 ve önceki partiler) tek sınır sözlüğü. B, güvenlik sapmasında bunun dışında
# serbest etiket yazabiliyor (hekim, acil_yonlendirme…): önceki partilerin sapma kayıtları gibi
# «rol_siniri_yonlendirme»ye eşlenir, B'nin etiketi gen_meta.sinir_tipi_b'de kalır.
SINIR = ("yok", "rol_siniri_yonlendirme", "yonlendirme_istegi", "yonlendirme_gereksiz", "sinir_cekme")

# ⛔ Pilotta ölçülen şablonlar (2026-10-20-haiku-pilot-sablon.md). Parça (25 kayıt)
#    başına TAVAN; aşan kayıtlar yeniden yazılır.
ACILIS_YASAK = re.compile(r"^\W*(dinliyorum|buradayım|anlat|devam et|seni dinliyorum)", re.I)
KALIP_TAVAN = [
    ("«… adım gibi duruyor / adım olabilir»", re.compile(r"adım (gibi duruyor|olabilir|olur)"), 2),
    ("«yazman / anlatman … önemli»", re.compile(r"(yazman|anlatman|söylemen|fark etmen)[^.?!]{0,40}önemli"), 1),
    ("«kolay olmamıştır / kolay olmaz»", re.compile(r"kolay olma(mış|z)"), 1),
    ("«… duyuyorum»", re.compile(r"duyuyorum"), 2),
    ("«karar sende / senin kararın»", re.compile(r"karar sende|senin kararın|karar(ı)? sana ait"), 3),
    ("«hüküm ver… / bana düşmez»", re.compile(r"hüküm (vermem|veremem|vermek|kurmak)|bana düşmez"), 3),
    ("«adlandırıyorum / adıyla anıyorum»", re.compile(r"adlandırıyorum|adıyla anıyorum"), 0),
]
# ⛔ HİTAP «sen». Kalibrasyonda (parça 1-2) 49 kaydın 14'ünde A'nın açılışı «siz»
#    diyordu, B «sen» diye sürdürüyordu. Örnek kayıtların hepsi «sen».
#    ⚠️ v0.1.1'in 1636 asistan turunda 62 vuruş — çoğu MEŞRU çoğul («ikinizin»,
#    çifte hitap) ⇒ açılışta SERT (tek kişiye ilk söz), son cevapta yalnız UYARI.
SIZ = re.compile(r"\b(siz|size|sizi|sizin|sizde|sizce|sizinle|sizden)\b|"
                 r"\w+(yorsunuz|siniz|sınız|sunuz|sünüz)\b|\w+(unuz|ünüz|ınız|iniz)(un|ün|ın|in|a|e|ı|i|da|de|u|ü)?\b", re.I)
DF_ESIK = 0.02   # sızıntı dedektörü: tohum havuzunda %2'den seyrek gövdeler (pilotta 7/11 yakalar)


def _c_model(n: int) -> str:
    """⛔ C'yi yapan model parçaya göre değişiyor (2026-10-21, kota): 1-13 Sonnet, gerisi Haiku."""
    f = DIZIN / "c_model.json"
    if not f.exists():
        return "claude-sonnet-5-5"
    m = json.loads(f.read_text(encoding="utf-8"))
    return "claude-sonnet-5-5" if n in m["sonnet"] else f"claude-{m['varsayilan']}-5-5"


def _oku(p: Path) -> list[dict]:
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def _plan_hepsi() -> list[dict]:
    return _oku(PLAN) + _oku(PLAN_EK)


def _plan(n: int) -> list[dict]:
    return [r for r in _plan_hepsi() if r["parca"] == n]


def _yol(asama: str, n: int) -> Path:
    return DIZIN / asama / f"parca{n:03d}.jsonl"


def _govde(s: str) -> set[str]:
    return {w[:5] for w in re.sub(r"[^\w\s]", " ", TG.tr_sadelestir(s)).split() if len(w) > 4}


_DF: collections.Counter | None = None


def _df() -> tuple[collections.Counter, int]:
    global _DF
    h = _oku(HAVUZ)
    if _DF is None:
        _DF = collections.Counter(g for t in h for g in _govde(t["user_message"]))
    return _DF, len(h)


# ───────────────────────── A ─────────────────────────
A_ALAN = ("sira", "tur", "yas", "bicim", "register", "turn_type", "konusma_durumu",
          "context", "baglam_davranisi", "sinir_tipi", "senaryo_hedefi", "tohum_metin", "tohum_baglam")


def a_girdi(n: int) -> int:
    for r in _plan(n):
        print(json.dumps({k: r.get(k) for k in A_ALAN}, ensure_ascii=False))
    return 0


def _a_hatalari(n: int) -> dict[int, list[str]]:
    plan = {r["sira"]: r for r in _plan(n)}
    a = _oku(_yol("A", n))
    hata: dict[int, list[str]] = collections.defaultdict(list)
    gorulen = set()
    tohum = {s: _govde(p["tohum_metin"]) for s, p in plan.items()}
    acilislar = collections.Counter()
    for k in a:
        s = k.get("sira")
        if s not in plan:
            hata[s or 0].append("plan dışı sira")
            continue
        gorulen.add(s)
        p = plan[s]
        try:
            turns = k["turns"]
            rollar = [r for r, _ in turns]
        except (KeyError, TypeError, ValueError):
            hata[s].append("`turns` biçimi bozuk")
            continue
        bek = ["user"] if p["turn_type"] == "single" else ["user", "assistant", "user"]
        if rollar != bek:
            hata[s].append(f"tur yapısı {rollar} ≠ {bek}")
            continue
        ilk = turns[0][1]
        if "<context" in ilk:
            hata[s].append("bağlam bloğunu kullanıcı mesajına yazma, `baglam` alanına yaz")
        if (b := B1._bant(ilk)) != p["bicim"]:
            hata[s].append(f"bicim {p['bicim']} ↔ ilk mesaj {b} ({len(ilk.split())} kelime; kisa ≤8 · orta 9–25 · uzun ≥26)")
        if bool(k.get("baglam")) != bool(p["context"]):
            hata[s].append(f"context {p['context']} ama baglam {'var' if k.get('baglam') else 'yok'}")
        if k.get("baglam"):
            kb = k["baglam"]
            if not isinstance(kb, dict) or not kb.get("kaynak") or not kb.get("metin"):
                hata[s].append("baglam {kaynak, metin} olmalı")
            elif kb["kaynak"][:1] != TG.tr_fold(kb["kaynak"][:1]):
                hata[s].append("baglam.kaynak küçük harfle başlamalı (kategori, özel ad değil)")
        if p["turn_type"] == "multi":
            ac = turns[1][1]
            if ACILIS_YASAK.search(TG.tr_fold(ac)):
                hata[s].append(f"asistan açılışı yasaklı kalıp: «{ac[:40]}» — açılış kullanıcının ilk mesajına özgü olmalı")
            if SIZ.search(ac):
                hata[s].append(f"asistan açılışında «siz» hitabı — BıRAG «sen» der: «{ac[:50]}»")
            if ac.count("?") > 1:
                hata[s].append("asistan açılışında en fazla 1 soru")
            acilislar[TG.tr_fold(ac).strip()] += 1
        for m in (c for _, c in turns):
            if B1.DOZ_SAYISI.search(m):
                hata[s].append(f"doz sayısı: {B1.DOZ_SAYISI.findall(m)}")
        b_ = _govde(" ".join(c for r, c in turns if r == "user"))
        skor = {t: len(a_ & b_) for t, a_ in tohum.items()}
        if skor[s] == 0 or max(skor.values()) - skor[s] >= 3:
            hata[s].append(f"TOHUM KARŞILIĞI zayıf (kendi {skor[s]}, en iyi {max(skor.values())}) — başka satırın tohumu mu?")
    for s in plan:
        if s not in gorulen:
            hata[s].append("satır yazılmamış")
    for ac, c in acilislar.items():
        if c > 1:
            hata[0].append(f"aynı asistan açılışı {c} kez: «{ac[:40]}»")
    return {k: v for k, v in hata.items() if v}


def a_kontrol(n: int) -> int:
    h = _a_hatalari(n)
    for s, v in sorted(h.items()):
        print(f"⛔ #{s}: " + " | ".join(v))
    print(f"A parca{n:03d}: {len(_oku(_yol('A', n)))} satır · {'GEÇTİ' if not h else f'{len(h)} satırda hata'}")
    return 1 if h else 0


# ───────────────────────── B ─────────────────────────
B_ALAN = ("sira", "tur", "yas", "register", "turn_type", "turn_ending", "mi_process",
          "konusma_durumu", "sinir_tipi", "senaryo_hedefi", "is_negative", "ozerklik", "baglam_davranisi")


def b_girdi(n: int) -> int:
    """⛔ TOHUM YOK — B yalnız yazılmış konuşmayı görür."""
    a = {k["sira"]: k for k in _oku(_yol("A", n))}
    for r in _plan(n):
        k = a.get(r["sira"])
        if k is None:
            continue
        print(json.dumps({**{x: r.get(x) for x in B_ALAN}, "turns": k["turns"],
                          "baglam": k.get("baglam")}, ensure_ascii=False))
    return 0


# ───────────────────────── birleştir ─────────────────────────
def _kayit(p: dict, a: dict, b: dict, asama: str) -> tuple[dict, list[str], list[str]]:
    """A (kullanıcı tarafı) + B/C (cevap) → kayıt. Sapma ile soruya çevrilen bitiş kabul edilir (v5 §5a′)."""
    te = p["turn_ending"]
    sapma_b = b.get("sapma")
    if b.get("turn_ending") and b["turn_ending"] != te:
        if sapma_b and b["turn_ending"] == "acik_uclu_soru" and te in SORUSUZ:
            te = "acik_uclu_soru"
        else:
            return {}, [f"turn_ending {te}→{b['turn_ending']} yalnız güvenlik sapmasıyla ve yalnız soruya çevrilebilir"], []
    p2 = {**p, "turn_ending": te}
    if b.get("sinir_tipi") and b["sinir_tipi"] != p["sinir_tipi"]:
        if not sapma_b:
            return {}, ["sinir_tipi değişikliği sapma gerekçesi ister"], []
        p2["sinir_tipi"] = b["sinir_tipi"] if b["sinir_tipi"] in SINIR else "rol_siniri_yonlendirme"
    taslak = {"turns": a["turns"], "baglam": a.get("baglam"),
              "baglam_davranisi": p["baglam_davranisi"] if a.get("baglam") else None,
              "son": b["son"], "thinking": b["thinking"], "sapma": sapma_b}
    rec, hata, kuyruk = HPB._kayit(p2, taslak)
    for m in rec["messages"]:
        if m["role"] == "assistant" and (x := SIZ.search(m["content"])):
            kuyruk.append(f"«siz» biçimi («{x.group(0)}») — tek kişiye hitapsa «sen»e çevir, çifte/aileye hitapsa kalabilir")
    # §3a′ İKİNCİ KATMAN — sızıntı dedektörü (rapor, kapı değil)
    df, nh = _df()
    konus = " ".join(c for _, c in a["turns"]) + " " + json.dumps(a.get("baglam") or {}, ensure_ascii=False)
    sizan = sorted(g for g in (_govde(b["son"] + " " + (b["thinking"] or "")) & _govde(p["tohum_metin"]))
                   - _govde(konus) if df[g] / nh < DF_ESIK)
    gm = rec["gen_meta"]
    gm.update({"generator": "claude-code-workflow", "parti": PARTI,
               "generator_model": f"A,B: claude-haiku-5-5 · C: {_c_model(p['parca'])}",
               "prompt_version": f"olcek5k-{asama}.v1", "date": betik_tarihi(__file__),
               "asama": asama, "tohum_onceden_kullanildi": p["tohum_onceden_kullanildi"],
               "yas_tohum": p.get("yas_tohum")})
    if p2["turn_ending"] != p["turn_ending"]:
        gm["turn_ending_plan"] = p["turn_ending"]
    if p2["sinir_tipi"] != p["sinir_tipi"]:
        gm["sinir_tipi_plan"] = p["sinir_tipi"]
    if b.get("sinir_tipi") and b["sinir_tipi"] not in SINIR:
        gm["sinir_tipi_b"] = b["sinir_tipi"]
    if b.get("c_karar"):
        gm["c_karar"], gm["c_neden"] = b["c_karar"], b.get("c_neden")
    if sizan:
        kuyruk.append(f"SIZINTI ŞÜPHESİ (konuşmada yok, tohumda var): {sizan}")
        gm["sizinti_supheli"] = sizan
    rec["id"] = hashlib.sha256(f"{PARTI}-{p['sira']}".encode()).hexdigest()[:24]
    return rec, hata, kuyruk


def birlestir(n: int, asama: str) -> int:
    plan = {r["sira"]: r for r in _plan(n)}
    a = {k["sira"]: k for k in _oku(_yol("A", n))}
    b = _oku(_yol(asama, n))
    if not b:
        print(f"⛔ {asama}/parca{n:03d}.jsonl yok ya da boş")
        return 1
    gecen, hatali, dusen = [], 0, 0
    sonlar = []
    for k in b:
        s = k.get("sira")
        if s not in plan or s not in a:
            print(f"⛔ #{s}: plan ya da A satırı yok")
            hatali += 1
            continue
        if k.get("c_karar") == "dusuruldu":
            dusen += 1
            continue
        try:
            rec, hata, kuyruk = _kayit(plan[s], a[s], k, asama)
        except (KeyError, TypeError, ValueError) as e:
            rec, hata, kuyruk = {}, [f"satır biçimi bozuk: {e!r}"], []
        if hata:
            hatali += 1
            print(f"⛔ #{s}: " + " | ".join(hata))
            continue
        if kuyruk:
            print(f"⚠️ #{s}: " + " | ".join(kuyruk))
        gecen.append(rec)
        sonlar.append((s, rec["messages"][-1]["content"]))
    # parça düzeyi: thinking oranı · kalıp tavanları · 8 sözcük
    blok = []
    o = [(len(r["messages"][-1].get("thinking") or ""), len(r["messages"][-1]["content"])) for r in gecen]
    if o:
        oran = sum(x for x, _ in o) / max(sum(y for _, y in o), 1)
        print(f"thinking/cevap oranı {oran:.2f} (hedef 1,20 ± 0,20)")
        if oran > 1.40:
            blok.append(f"THINKING parça oranı {oran:.2f} > 1,40 — thinking'leri kısalt")
    for ad, rx, tavan in KALIP_TAVAN:
        vuran = [s for s, t in sonlar if rx.search(TG.tr_fold(t))]
        if len(vuran) > tavan:
            blok.append(f"KALIP {ad}: {len(vuran)} kayıtta (tavan {tavan}) — {vuran}")
    sayac: dict[str, set] = collections.defaultdict(set)
    for s, t in sonlar:
        for d in HPB._diziler(t, 8):
            sayac[d].add(s)
    for d, ss in sayac.items():
        if len(ss) > 1:
            blok.append(f"ŞABLON 8 sözcük {sorted(ss)}: «{d}»")
    for x in blok:
        print(f"⛔ {x}")
    hedef = DIZIN / "kayit" / f"parca{n:03d}.{asama}.jsonl"
    hedef.parent.mkdir(parents=True, exist_ok=True)
    hedef.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in gecen), encoding="utf-8")
    print(f"{asama} parca{n:03d}: {len(b)} satır · {len(gecen)} geçti · {hatali} hatalı · {dusen} düşürüldü "
          f"· {len(blok)} parça uyarısı → {hedef.relative_to(KOK)}")
    return 1 if (hatali or blok) else 0


# ───────────────────────── C ─────────────────────────
def c_girdi(n: int) -> int:
    """C'nin okuma görünümü: konuşma + cevap + şüpheler. Tohum yalnız SIZINTI denetimi için gösterilir."""
    plan = {r["sira"]: r for r in _plan(n)}
    a = {k["sira"]: k for k in _oku(_yol("A", n))}
    for k in _oku(_yol("B", n)):
        s = k["sira"]
        p = plan[s]
        try:
            _, hata, kuyruk = _kayit(p, a[s], k, "B")
        except (KeyError, TypeError, ValueError) as e:
            hata, kuyruk = [repr(e)], []
        print(f"══ #{s} · {p['tur']}/{p['yas']} · {p['turn_type']} · bitiş={k.get('turn_ending') or p['turn_ending']} "
              f"· sınır={k.get('sinir_tipi') or p['sinir_tipi']} · hedef={p['senaryo_hedefi']} "
              f"· red={p['is_negative']} · özerklik={p['ozerklik']} · bağlam={p['baglam_davranisi']}")
        if a[s].get("baglam"):
            print(f"  BAĞLAM [{a[s]['baglam']['kaynak']}]: {a[s]['baglam']['metin']}")
        for r, c in a[s]["turns"]:
            print(f"  {r.upper()}: {c}")
        print(f"  CEVAP: {k['son']}")
        print(f"  THINKING: {k['thinking']}")
        if k.get("sapma"):
            print(f"  SAPMA: {k['sapma']}")
        print(f"  [yalnız sızıntı denetimi için] TOHUM: {p['tohum_metin']}")
        for x in hata:
            print(f"  ⛔ {x}")
        for x in kuyruk:
            print(f"  ⚠️ {x}")
    return 0


def durum() -> int:
    parcalar = sorted({r["parca"] for r in _plan_hepsi()})
    say = collections.Counter()
    eksik = []
    for n in parcalar:
        for asama in ("A", "B", "C"):
            if _yol(asama, n).exists():
                say[asama] += 1
        k = DIZIN / "kayit" / f"parca{n:03d}.C.jsonl"
        if k.exists():
            say["kayit"] += sum(1 for l in k.read_text(encoding="utf-8").splitlines() if l.strip())
        else:
            eksik.append(n)
    print(f"parça {len(parcalar)} · A {say['A']} · B {say['B']} · C {say['C']} · son kayıt {say['kayit']}")
    print(f"C'si bitmemiş parça: {len(eksik)}" + (f" (ilk 20: {eksik[:20]})" if eksik else ""))
    return 0


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    k = argv[0]
    if k == "durum":
        return durum()
    n = int(argv[1])
    (DIZIN / "A").mkdir(parents=True, exist_ok=True)
    (DIZIN / "B").mkdir(parents=True, exist_ok=True)
    (DIZIN / "C").mkdir(parents=True, exist_ok=True)
    return {"a-girdi": lambda: a_girdi(n), "a-kontrol": lambda: a_kontrol(n),
            "b-girdi": lambda: b_girdi(n), "c-girdi": lambda: c_girdi(n),
            "birlestir": lambda: birlestir(n, argv[2])}[k]()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
