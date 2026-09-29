"""`v0.1.1` ön kaydının ölçüleri — TEK kaynak (K103). Ön kayıt bu dosyanın SHA'sını mühürler.

Hiçbir ölçü burada yeniden tanımlanmaz; hepsi ölçülmüş kaynaklarından İÇE AKTARILIR:
  soru_bitis · «sormuyorum» · ⛔/⭐  ← T281 (`scripts/analiz/2026-09-24-tur-sonu-ve-dusunme.py`)
  dejenerasyon                       ← T82  (`src/dejenerasyon.py`)
⇒ `v0.1.0`'ın T281'de ölçülmüş sayılarıyla aynı cetvelle karşılaştırılır.

⛔ Bu dosya ön kayıt mühürlendikten sonra DEĞİŞTİRİLMEZ; değişirse çözümleme mühürdeki
SHA ile karşılaştırıp durur.
"""
from __future__ import annotations

import statistics as st
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "src"))
import dejenerasyon as _dj  # noqa: E402
from tohum_guvenlik import tr_fold  # noqa: E402


def _modul(ad: str, yol: str):
    y = KOK / yol
    sp = _iu.spec_from_file_location(ad, y)
    m = _iu.module_from_spec(sp)
    argv, sys.argv = sys.argv[:], [str(y)]
    sp.loader.exec_module(m)
    sys.argv = argv
    return m


_T281 = _modul("_t281", "scripts/analiz/2026-09-24-tur-sonu-ve-dusunme.py")
_SORMUYORUM, _S_FOLD = _T281.VEKIL["«sormuyorum»"]
_ISKELE, _I_FOLD = _T281.VEKIL["⛔ / ⭐ işareti"]
assert _S_FOLD is True and _I_FOLD is False, "⛔ T281 vekil tanımı değişmiş"


def soru_bitis(cevap: str | None) -> bool:
    """Cevap soruyla mı bitiyor — T281'in vekili (son karakter)."""
    return _T281.soru_bitis(cevap)


def sormuyorum(thinking: str | None) -> bool:
    """Düşünmede «sormuyorum» — T281 vekili, tr_fold'lu metinde."""
    return bool(_SORMUYORUM.search(tr_fold(thinking or "")))


def iskele(thinking: str | None) -> bool:
    """Düşünmede ⛔ ya da ⭐ — T281 vekili, ham metinde."""
    return bool(_ISKELE.search(thinking or ""))


def dejenere(r: dict) -> bool:
    return _dj.denetle(r.get("thinking"), r.get("cevap"), r.get("thinking_kapandi"))["dejenere"]


def tek_tur_ozet(satirlar: list[dict]) -> dict:
    """Bir tohumun tek turlu eksen çıktıları (altı set birleşik) → baş/ikinci ölçüler.
    Paydalar: düşünme ölçüleri **düşünmesi dolu** üretimler; bitiş **cevabı dolu** üretimler
    (T281 §2a ile aynı)."""
    dol = [r for r in satirlar if (r.get("cevap") or "").strip()]
    # ⚠️ T281 §3 ile aynı payda: düşünmesi VE cevabı dolu üretimler. Cevabı boş
    #    (çoğu dejenere) üretimler burada sayılmaz; onları `dejenere_payi` ölçer.
    #    İlk sürümde payda yalnız «düşünmesi dolu» idi ve T281'i üretemedi (381/751 ↔ 364/709).
    # ⚠️ T281'in paydası bundan BİR kayıt geniş (709 ↔ 708): o, cevabı dolu ama düşünmesi
    #    BOŞ üretimi de sayar ve «sormuyorum yok» hanesine yazar. Burada bilerek sayılmaz —
    #    `thinking=False` koşuda daha seyrek düşünen bir model aksi hâlde bedavaya «temiz»
    #    görünürdü. Düşünme sıklığı ayrıca `dusunme_orani` olarak raporlanır.
    dus = [r for r in dol if (r.get("thinking") or "").strip()]
    return {
        "n": len(satirlar), "n_dusunme": len(dus), "n_cevap": len(dol),
        "dusunme_orani": 100 * len(dus) / max(len(dol), 1),
        "sormuyorum_payi": 100 * sum(sormuyorum(r["thinking"]) for r in dus) / max(len(dus), 1),
        "iskele_payi": 100 * sum(iskele(r["thinking"]) for r in dus) / max(len(dus), 1),
        "soru_bitis_payi": 100 * sum(soru_bitis(r["cevap"]) for r in dol) / max(len(dol), 1),
        "dejenere_payi": 100 * sum(dejenere(r) for r in satirlar) / max(len(satirlar), 1),
        "bos_cevap": len(satirlar) - len(dol),
        "dusunme_sozcuk_ortanca": st.median([len(r["thinking"].split()) for r in dus]) if dus else 0,
    }


def en_uzun_seri(bayraklar: list[bool]) -> int:
    en = cur = 0
    for b in bayraklar:
        cur = cur + 1 if b else 0
        en = max(en, cur)
    return en


def cok_tur_ozet(turlar: list[dict]) -> dict:
    """Bir tohumun çok turlu çıktıları (her satır bir asistan turu; `konusma`, `tur`)."""
    konus: dict[str, list[dict]] = {}
    for r in turlar:
        konus.setdefault(r["konusma"], []).append(r)
    for v in konus.values():
        v.sort(key=lambda r: r["tur"])
    dol = [r for r in turlar if (r.get("cevap") or "").strip()]
    dus = [r for r in dol if (r.get("thinking") or "").strip()]      # tek turla aynı payda
    sb = {k: [soru_bitis(r.get("cevap")) for r in v] for k, v in konus.items()}
    return {
        "n_konusma": len(konus), "n_tur": len(turlar), "n_cevap": len(dol),
        "dusunme_orani": 100 * len(dus) / max(len(dol), 1),
        "soru_bitis_payi": 100 * sum(soru_bitis(r["cevap"]) for r in dol) / max(len(dol), 1),
        # boş cevap soru sayılmaz ⇒ «hep soru» için dört turun dördü de DOLU ve soru olmalı
        "hep_soru_konusma": sum(all(v) and len(v) == 4 for v in sb.values()),
        "en_uzun_soru_serisi_ort": st.mean(en_uzun_seri(v) for v in sb.values()) if sb else 0,
        "sormuyorum_payi": 100 * sum(sormuyorum(r["thinking"]) for r in dus) / max(len(dus), 1),
        "iskele_payi": 100 * sum(iskele(r["thinking"]) for r in dus) / max(len(dus), 1),
        "dejenere_payi": 100 * sum(dejenere(r) for r in turlar) / max(len(turlar), 1),
        "bos_cevap": len(turlar) - len(dol),
    }
