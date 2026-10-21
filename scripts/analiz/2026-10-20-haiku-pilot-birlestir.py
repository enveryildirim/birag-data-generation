#!/usr/bin/env python3
"""Haiku pilotu — taslakları kayda çevirir ve kapılardan geçirir.

Girdi : data/candidates/haiku-pilot.taslak.blok<N>.jsonl  (Haiku alt ajanının taslağı)
Plan  : data/plan/haiku-pilot.jsonl
Çıktı : data/candidates/haiku-pilot.blok<N>.jsonl         (yalnız kapıyı GEÇEN kayıtlar)

Kullanım: uv run python scripts/analiz/2026-10-20-haiku-pilot-birlestir.py <N> [<N> ...]

⭐ Kapılar `v6-parti8 blok1` betiğinden İÇE AKTARILIR, kopyalanmaz (aynı kural
iki yerde yazılınca hangisinin doğru olduğu sorulamaz — T70). Farkları:
  · ELLE_ONAY yok: `is_negative`/`ozerklik` deseni görmezse kayıt düşmez,
    OKUMA KUYRUĞUNA yazılır (pilotta onayı ben okuyarak vereceğim).
  · Kapı reddi bütün bloğu durdurmaz: her kayıt kendi hatasını taşır, geçenler
    yazılır. Pilotun ölçtüğü şey tam olarak bu ret oranıdır.
  · `generator_model` = claude-haiku-5-5, `prompt_version` = haiku-taslak-brifi.v1.
"""
from __future__ import annotations

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

_sp = _iu.spec_from_file_location("b1", KOK / "scripts/analiz/2026-09-22-uretim-v6-parti8-blok1.py")
B1 = _iu.module_from_spec(_sp)
_sp.loader.exec_module(B1)

PLAN = KOK / "data/plan/haiku-pilot.jsonl"
PARTI = "haiku-pilot"
TH_HEDEF, TH_TOLERANS, TH_TAVAN = 1.20, 0.20, 2.20
ISKELE = re.compile(r"ızgara|kota|beyan|§\d|K\d{1,3}\b|T\d{2,3}\b|Kural \d|parti\d|brif|"
                    r"turn_ending|sinir_tipi|mi_process|is_negative|ozerklik", re.I)


def _kayit(p: dict, k: dict) -> tuple[dict, list[str], list[str]]:
    sira, hata, kuyruk = p["sira"], [], []
    ctx, blok = [], ""
    if k.get("baglam"):
        b = k["baglam"]
        blok = f'<context kaynak="{b["kaynak"]}">\n{b["metin"]}\n</context>'
        ctx = [{"kaynak": b["kaynak"], "metin": b["metin"], "sentetik": True}]
    msgs = [{"role": "system", "content": B1.CANON}]
    ilk_user = True
    for rol, icerik in k["turns"]:
        if rol == "user" and ilk_user and blok:
            icerik = f"{blok}\n\n{icerik}"
        if rol == "user":
            ilk_user = False
        msgs.append({"role": rol, "content": icerik})
    msgs.append({"role": "assistant", "content": k["son"], "thinking": k["thinking"]})
    son, th = k["son"], k["thinking"] or ""
    ilk = next(m["content"] for m in msgs if m["role"] == "user")

    rollar = [m["role"] for m in msgs[1:]]
    beklenen = ["user", "assistant"] if p["turn_type"] == "single" else ["user", "assistant", "user", "assistant"]
    if rollar != beklenen:
        hata.append(f"tur yapısı {rollar} ≠ {beklenen} ({p['turn_type']})")
    if (b2 := B1._bant(ilk)) != p["bicim"]:
        hata.append(f"bicim plan {p['bicim']} ↔ ölçülen {b2} ({len(B1._serbest(ilk).split())} kelime)")
    if bool(ctx) != bool(p["context"]):
        hata.append(f"context plan {p['context']} ↔ taslak {bool(ctx)}")
    if ctx and k.get("baglam_davranisi") != p.get("baglam_davranisi"):
        hata.append(f"bağlam sınıfı plan {p.get('baglam_davranisi')} ↔ taslak {k.get('baglam_davranisi')}")
    soru = son.count("?")
    if soru > 1:
        hata.append(f"soru {soru} > 1")
    if p["turn_ending"] == "acik_uclu_soru" and soru != 1:
        hata.append(f"`acik_uclu_soru` ama soru {soru}")
    if p["turn_ending"] in ("takdir", "ozet", "yalnizca_yansitma", "durur") and soru:
        hata.append(f"`{p['turn_ending']}` sorusuz olmalı, soru {soru}")
    for alan, desen, ad in ((p["ozerklik"], B1.OZERKLIK, "ozerklik_vurgusu"),
                            (p["is_negative"], B1.RED, "is_negative")):
        if alan and not desen.search(son):
            kuyruk.append(f"`{ad}` planlı, desen görmedi — okumada bakılacak")
    o = len(th) / max(1, len(son))
    if o > TH_TAVAN:
        hata.append(f"thinking kaçak tavanı {o:.2f} > {TH_TAVAN}")
    for m in msgs[1:]:
        if B1.DOZ_SAYISI.search(m["content"]):
            hata.append(f"doz sayısı ({m['role']}): {B1.DOZ_SAYISI.findall(m['content'])}")
        if m["role"] == "assistant" and B1.ILAC_ADI.search(m["content"]):
            hata.append(f"asistan turunda ilaç adı: {B1.ILAC_ADI.findall(m['content'])}")
    if isk := ISKELE.findall(th):
        hata.append(f"thinking iskelesi: {sorted(set(isk))}")

    gm = {"generator": "claude-code-subagent", "generator_model": "claude-haiku-5-5",
          "prompt_version": "haiku-taslak-brifi.v1", "date": betik_tarihi(__file__),
          "system_prompt_variant": "canon", "parti": PARTI, "parti_sira": sira,
          "seed_id": p["seed_id"], "turn_ending": p["turn_ending"],
          "konusma_durumu": p["konusma_durumu"], "bicim": p["bicim"],
          "register": p["register"], "sinir_tipi": p["sinir_tipi"],
          "senaryo_hedefi": p["senaryo_hedefi"], "ozerklik_vurgusu": bool(p["ozerklik"]),
          "tohum_havuzu": "seeds.v2", "motivasyon_tohum": p["motivasyon_tohum"]}
    if ctx:
        gm["baglam_davranisi"] = k.get("baglam_davranisi")
        gm["baglam_bicimi"] = "v1"
    sapma = "; ".join(x for x in (p.get("izgara_sapmasi"), k.get("sapma")) if x)
    if sapma:
        gm["izgara_sapmasi"] = sapma
    if kuyruk:
        gm["okuma_kuyrugu"] = kuyruk
    rec = {"id": hashlib.sha256(f"{PARTI}-{sira}".encode()).hexdigest()[:24],
           "slice": None,  # T240: türetilir, beyan edilmez
           "scenario": p["tohum_senaryo"], "addiction_type": p["tur"],
           "motivation": p["motivasyon"], "mi_process": p["mi_process"],
           "talk_type": "change" if p["senaryo_hedefi"] == "serbest" else "sustain",
           "age_group": p["yas"], "turn_type": p["turn_type"], "messages": msgs,
           "context": ctx, "source_ids": [p["source_id"]], "is_crisis": False,
           "is_negative": bool(p["is_negative"]), "has_thinking": True,
           "judge": None, "replay": False, "gen_meta": gm}
    rec["slice"] = dilim(rec)
    if not hata:
        c = run_checks(rec)
        if not c.get("passed"):
            hata.append(f"run_checks: {json.dumps({a: v for a, v in c.items() if v not in (None, True, [], {})}, ensure_ascii=False)[:300]}")
    return rec, hata, kuyruk


def _govde(s: str) -> set[str]:
    return {w[:5] for w in re.sub(r"[^\w\s]", " ", TG.tr_sadelestir(s)).split() if len(w) > 4}


def main(bloklar: list[int]) -> int:
    plan = {json.loads(l)["sira"]: json.loads(l)
            for l in PLAN.read_text(encoding="utf-8").splitlines() if l.strip()}
    tohum = {s: _govde(p["tohum_metin"]) for s, p in plan.items()}
    toplam_hata = 0
    for n in bloklar:
        taslak = KOK / f"data/candidates/{PARTI}.taslak.blok{n}.jsonl"
        cikti = KOK / f"data/candidates/{PARTI}.blok{n}.jsonl"
        if not taslak.exists():
            print(f"⛔ blok{n}: taslak yok ({taslak.relative_to(KOK)})")
            toplam_hata += 1
            continue
        try:
            satirlar = [json.loads(l) for l in taslak.read_text(encoding="utf-8").splitlines() if l.strip()]
        except json.JSONDecodeError as e:
            print(f"⛔ blok{n}: JSON bozuk — {e}")
            toplam_hata += 1
            continue
        gecen, sonuc = [], []
        for k in satirlar:
            p = plan.get(k.get("sira"))
            if p is None:
                print(f"⛔ blok{n}: plan dışı sira {k.get('sira')}")
                toplam_hata += 1
                continue
            try:
                rec, hata, kuyruk = _kayit(p, k)
            except (KeyError, TypeError, ValueError) as e:
                sonuc.append((k.get("sira"), [f"taslak biçimi bozuk: {e!r}"], []))
                continue
            b_ = _govde(" ".join(B1.BLOK.sub("", m["content"]) for m in rec["messages"] if m["role"] == "user"))
            skor = {t: len(a & b_) for t, a in tohum.items()}
            if skor[p["sira"]] == 0 or max(skor.values()) - skor[p["sira"]] >= 3:
                hata.append(f"TOHUM KARŞILIĞI: kendi tohumuyla ortak {skor[p['sira']]}, en iyi {max(skor.values())}")
            sonuc.append((p["sira"], hata, kuyruk))
            if not hata:
                gecen.append(rec)

        # blok düzeyi: thinking oranı + şablon (8 sözcük, bloklar arası)
        _o = [(len(m.get("thinking") or ""), len(m["content"])) for r in gecen
              for m in r["messages"] if m["role"] == "assistant" and m.get("thinking")]
        blok_hata = []
        if _o:
            oran = sum(a for a, _ in _o) / max(sum(b for _, b in _o), 1)
            print(f"blok{n} thinking/cevap oranı: {oran:.2f} (hedef {TH_HEDEF} ±{TH_TOLERANS})")
            if oran > TH_HEDEF + TH_TOLERANS:
                blok_hata.append(f"THINKING blok oranı {oran:.2f} > {TH_HEDEF + TH_TOLERANS:.2f}")
        diger = []
        for f in sorted(KOK.glob(f"data/candidates/{PARTI}.blok*.jsonl")):
            if f != cikti:
                diger += [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
        sayac: dict[str, set[int]] = {}
        for r in diger + gecen:
            son = [m for m in r["messages"] if m["role"] == "assistant"][-1]["content"]
            for d in _diziler(son, 8):
                sayac.setdefault(d, set()).add(r["gen_meta"]["parti_sira"])
        for d, s in sayac.items():
            if len(s) > 1:
                blok_hata.append(f"ŞABLON 8 sözcük · {sorted(s)} · «{d}»")

        for sira, hata, kuyruk in sorted(sonuc, key=lambda x: x[0] or 0):
            if hata:
                print(f"  ⛔ #{sira}: " + " | ".join(hata))
            elif kuyruk:
                print(f"  ⚠️ #{sira}: " + " | ".join(kuyruk))
        for h in blok_hata:
            print(f"  ⛔ {h}")
        red = sum(1 for _, h, _ in sonuc if h)
        toplam_hata += red + len(blok_hata)
        cikti.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in gecen), encoding="utf-8")
        print(f"blok{n}: {len(satirlar)} taslak · {len(gecen)} geçti · {red} reddedildi "
              f"· {len(blok_hata)} blok uyarısı → {cikti.relative_to(KOK)}")
    return 1 if toplam_hata else 0


def _diziler(metin: str, n: int) -> set[str]:
    k = re.sub(r"[^\w\s]", " ", TG.tr_fold(metin)).split()  # Kural 4: str.lower() yasak
    return {" ".join(k[i:i + n]) for i in range(len(k) - n + 1)}


if __name__ == "__main__":
    raise SystemExit(main([int(a) for a in sys.argv[1:]] or [1, 2, 3]))
