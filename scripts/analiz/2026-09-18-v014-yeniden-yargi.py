#!/usr/bin/env python3
"""v0.0.14 — bayat ilan edilen 32 yargı yeniden koşuluyor.

⛔ **Neden.** v0.0.10–v0.0.13 arasında 32 kaydın metni düzeltildi ve her birinin
`judge` alanı **bayat** ilan edildi: judge onları düzeltmeden ÖNCEKİ metin üzerinde
puanlamıştı ve `grounding` · `alinti_dogrulama` gibi alanlar doğrudan o metne
bakıyor. Puanlar saklandı ama *«hiçbir sayıda sessizce kullanılamaz»* diye işaretlendi.

⚠️⚠️ **BU KOŞU VERİYİ DEĞİŞTİREBİLİR.** `build.py`, `klinik_guvenlik_ihlali: true`
olan kaydı **eler**. Yeni bir yargı o bayrağı kaldırır ya da koyarsa yayımlanan
kayıt sayısı değişir ⇒ betik eleme farkını **ayrıca** raporlar.

⭐ Judge `filter.judge_record` ile çağrılıyor — kuyruk birebir aynı (K103) ve
model/rubrik yapılandırmadan geliyor (`agy:gemini-3.8-flash-high`, `judge-eksen1.v9`),
yani K43/K45 korunuyor: puanlayan Claude DEĞİL.

⛔ `agy` CLI'ın 280 sn sınırı bilinen bir kusur (T161: 48 öğede 5 ve 13 zaman aşımı).
Başarısız kayıtlarda **eski yargı ve bayat işareti DURUR** — yarım bir yargı yazmak,
bayat bir yargıdan daha kötüdür.

Girdi : data/judged/v0.0.13.jsonl
Çıktı : data/judged/v0.0.14.jsonl · reports/analiz/2026-09-18-v014-yeniden-yargi.md
Kullanım: uv run python scripts/analiz/2026-09-18-v014-yeniden-yargi.py
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
GIRDI = KOK / "data/judged/v0.0.13.jsonl"
CIKTI = KOK / "data/judged/v0.0.14.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-v014-yeniden-yargi.md"
PARALEL = 6

import filter as F  # noqa: E402

IKILI = ["klinik_guvenlik_ihlali", "rol_siniri_ihlali", "cevapsiz_soru"]
SAYISAL = ["duygusal_tepki", "yorumlama", "kesif", "mi_uyumu", "grounding"]


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]


def main() -> int:
    ham = GIRDI.read_bytes()
    kayitlar = [json.loads(s) for s in ham.decode("utf-8").splitlines() if s.strip()]
    bayat = [r for r in kayitlar if (r.get("judge") or {}).get("bayat")]
    print(f"bayat kayıt: {len(bayat)} · judge: {F.JUDGE_MODEL} · rubrik: {F.JUDGE_PROMPT_VERSION}",
          flush=True)

    def _yargila(r):
        t0 = time.time()
        try:
            return r, F.judge_record(r), None, time.time() - t0
        except Exception as e:                    # ⛔ yarım yargı YAZILMAZ
            return r, None, f"{type(e).__name__}: {str(e)[:110]}", time.time() - t0

    with ThreadPoolExecutor(max_workers=PARALEL) as h:
        sonuc = list(h.map(_yargila, bayat))

    basarili, basarisiz, degisen = [], [], []
    for r, yeni, hata, sn in sonuc:
        if hata:
            basarisiz.append({"id": r["id"], "hata": hata, "sn": round(sn)})
            continue
        eski = dict(r["judge"])
        y = dict(yeni)
        fark = {k: (eski.get(k), y.get(k)) for k in IKILI + SAYISAL
                if eski.get(k) != y.get(k)}
        y["yeniden_yargilandi"] = TARIH
        y["onceki_bayat_gerekce"] = eski.get("bayat_gerekce")
        r["judge"] = y                            # ⭐ bayat ve bayat_gerekce DÜŞÜYOR
        basarili.append({"id": r["id"], "sn": round(sn), "fark": fark})
        if fark:
            degisen.append({"id": r["id"], "fark": fark})

    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kayitlar),
                     encoding="utf-8")
    guv = [d for d in degisen if "klinik_guvenlik_ihlali" in d["fark"]]
    sat = ["# v0.0.14 — bayat yargılar yeniden koşuldu", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Girdi:** `{GIRDI.relative_to(KOK)}` SHA256-16 `{_sha(ham)}`  ",
           f"**Çıktı:** `{CIKTI.relative_to(KOK)}` SHA256-16 `{_sha(CIKTI.read_bytes())}`  ",
           f"**Judge:** `{F.JUDGE_MODEL}` · **rubrik:** `{F.JUDGE_PROMPT_VERSION}` · "
           f"paralel {PARALEL}", "",
           "⭐ Judge `filter.judge_record` ile çağrıldı ⇒ kuyruk birebir aynı (K103) ve",
           "puanlayan **Claude değil** (K43/K45).", "",
           "| | |", "|---|---:|",
           f"| bayat kayıt | **{len(bayat)}** |",
           f"| ⭐ yeniden yargılanan | **{len(basarili)}** |",
           f"| ⛔ başarısız (bayat KALDI) | **{len(basarisiz)}** |",
           f"| yargısı DEĞİŞEN | **{len(degisen)}** |",
           f"| ⛔⛔ güvenlik bayrağı değişen | **{len(guv)}** |", ""]
    if degisen:
        sat += ["## Yargısı değişen kayıtlar", "", "| kayıt | alan | eski → yeni |",
                "|---|---|---|"]
        for d in degisen:
            for k, (a, b) in d["fark"].items():
                sat.append(f"| `{d['id'][:10]}` | `{k}` | {a} → **{b}** |")
        sat.append("")
    if basarisiz:
        sat += ["## ⛔ Başarısız — eski yargı ve bayat işareti DURUYOR", "",
                "⚠️ *Yarım bir yargı yazmak, bayat bir yargıdan daha kötüdür.*", "",
                "| kayıt | hata | sn |", "|---|---|---:|"]
        for b in basarisiz:
            sat.append(f"| `{b['id'][:10]}` | {b['hata'][:70]} | {b['sn']} |")
        sat.append("")
    (KOK / f"reports/analiz/{TARIH}-v014-yeniden-yargi.json").write_text(
        json.dumps({"tarih": TARIH, "girdi_sha256_16": _sha(ham),
                    "cikti_sha256_16": _sha(CIKTI.read_bytes()),
                    "basarili": basarili, "basarisiz": basarisiz, "degisen": degisen},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[8:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
