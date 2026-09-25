#!/usr/bin/env python3
"""Doz-yanıt korpuslarını judge karneleriyle birleştirir → data/judged/v0.0.4|v0.0.5.

Karne mantığı
-------------
v0.0.3'ün 155 kaydının hepsi K112'de puanlanmıştı. Bu turda yalnızca 26 kaydın SON
ASİSTAN CEVABI değişti (tek cümle eklendi) — o 26'nın karnesi artık kayda ait değil
ve yeniden puanlandı. Kalan 111 terapötik kaydın karnesi aynen taşınır, çünkü metinleri
BAYT BAYT aynı (yamalama betiğinin I2 değişmezi bunu garanti ediyor).

⛔ YAMASI GÜVENLİK İHLALİ ALAN KAYIT KARANTİNAYA ALINMAZ, YAMASI GERİ ALINIR
---------------------------------------------------------------------------
Kayıt zaten K112'de temiz geçmişti; yeni bir ihlal ancak EKLENEN CÜMLEDEN gelebilir.
Doğru karşılık kaydı atmak değil, yanlış olan eklemeyi geri almaktır: korpus boyu
sabit kalır (deneyin tek değişkenli olmasının şartı), doz bir azalır ve bu RAPORLANIR.
Kaydı atmak N'i oynatırdı ve K113'ün ölçtüğü adım karışması geri gelirdi.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import date
from pathlib import Path

KOK = Path(__file__).parent.parent.parent
KAYNAK = KOK / "datasets/v0.0.3/train.jsonl"
YENI_KARNE = KOK / "data/judged/doz-yama.v7.jsonl"
SETLER = [("v0.0.4", "data/candidates/v0.0.4-doz10.jsonl"),
          ("v0.0.5", "data/candidates/v0.0.5-doz25.jsonl")]


def main() -> None:
    if not YENI_KARNE.exists():
        raise SystemExit(f"⛔ yeni karneler yok: {YENI_KARNE.relative_to(KOK)}")
    karne = {r["id"]: r["judge"] for r in
             (json.loads(l) for l in YENI_KARNE.open())}
    asil = {r["id"]: r for r in (json.loads(l) for l in KAYNAK.open())}
    yamali = {y["id_16"] for y in
              (json.loads(l) for l in (KOK / "data/candidates/doz-yonlendirme-ekleri.jsonl").open())}

    ihlal: list[str] = []
    for kid, j in karne.items():
        if j.get("klinik_guvenlik_ihlali") or j.get("rol_siniri_ihlali"):
            ihlal.append(kid)

    ozet = {"tarih": date.today().isoformat(),
            "betik": "scripts/analiz/2026-09-15-doz-yanit-derleme.py",
            "yeni_karne": {"dosya": str(YENI_KARNE.relative_to(KOK)),
                           "kayit": len(karne),
                           "judge_model": sorted({j.get("judge_model") for j in karne.values()}),
                           "rubrik": sorted({j.get("prompt_version") for j in karne.values()})},
            "yamasi_geri_alinan": sorted(ihlal),
            "setler": {}}

    for surum, aday_yolu in SETLER:
        kayitlar = [json.loads(l) for l in (KOK / aday_yolu).open()]
        cikti, geri_alinan, yonlendirme = [], [], 0
        for r in kayitlar:
            kid = r["id"]
            yamalandi = kid[:16] in yamali and "doz_yamasi" in (r.get("gen_meta") or {})
            if yamalandi and kid in ihlal:
                r = json.loads(json.dumps(asil[kid]))     # yamasız asıl kayıt
                geri_alinan.append(kid)
                yamalandi = False
            if yamalandi:
                if kid not in karne:
                    raise SystemExit(f"⛔ {kid}: yamalı ama yeni karnesi yok")
                r["judge"] = karne[kid]
            if not r.get("replay") and not r.get("judge"):
                raise SystemExit(f"⛔ {kid}: terapötik kayıt karnesiz (K76/K112)")
            gm = r.get("gen_meta") or {}
            if gm.get("sinir_tipi") in ("yonlendirme_istegi", "rol_siniri_yonlendirme"):
                yonlendirme += 1
            cikti.append(r)

        # v0.0.3'ten gelen 7 yönlendirme kaydının ikisi (hukuki) sinir_tipi beyanı
        # taşımıyor — geniş tarama betiğiyle elle saptandılar, sayıya elle eklenir.
        yonlendirme += 2
        yol = KOK / f"data/judged/{surum}.jsonl"
        with yol.open("w", encoding="utf-8") as f:
            for r in cikti:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        ter = [r for r in cikti if not r.get("replay")]
        ozet["setler"][surum] = {
            "dosya": str(yol.relative_to(KOK)), "kayit": len(cikti), "terapotik": len(ter),
            "yonlendirme": yonlendirme, "oran": round(100 * yonlendirme / len(ter), 1),
            "yamasi_geri_alinan": geri_alinan,
            "sha256_16": hashlib.sha256(yol.read_bytes()).hexdigest()[:16],
        }

    cikti_yolu = KOK / "reports/analiz/2026-09-15-doz-yanit-derleme.json"
    cikti_yolu.write_text(json.dumps(ozet, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"yeni karne: {len(karne)} kayıt · judge {ozet['yeni_karne']['judge_model']} "
          f"· rubrik {ozet['yeni_karne']['rubrik']}")
    if ihlal:
        print(f"⛔ YAMASI GERİ ALINAN: {len(ihlal)} — {ihlal}")
    else:
        print("güvenlik/rol ihlali: 0/26 ✅")
    print()
    for s, o in ozet["setler"].items():
        print(f"{s}  {o['kayit']} kayıt · terapötik {o['terapotik']} · "
              f"yönlendirme {o['yonlendirme']} (%{o['oran']})  sha {o['sha256_16']}")
    print(f"\nyazıldı: {cikti_yolu.relative_to(KOK)}")


if __name__ == "__main__":
    main()
