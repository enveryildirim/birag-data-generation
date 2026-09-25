#!/usr/bin/env python3
"""v0.0.13 — zaman kapısının kalan 3 bulgusu düzeltiliyor.

⛔ Yayımlanmış sette zaman+kaynak kapısı 3 bulgu veriyordu ve hiçbiri elle
okunmamıştı. Üçü de okundu; üçü de **ılımlı ama gerçek** kusur:

| bulgu | neden kusur |
|---|---|
| *«hekimin planlayacağı bir şey»* | kullanıcı hiçbir hekim anmadı ⇒ BELİRLİ tamlama, var olmayan bir hekime gönderme yapıyor. §8b rol adlandırmayı ister ama **belirsiz** biçimde |
| *«dün gece ekranı en son kapatabildiğin an»* | kullanıcı bir ALIŞKANLIK anlattı (*«sabaha kadar oynuyorum»*), belirli bir geceyi değil ⇒ soru olmayan bir çıpayı varsayıyor |
| *«bir hafta önce bilmediğin bir şeyi»* | kullanıcı yalnız *«bu hafta»*yı çıpaladı; bir hafta öncesi hakkında hiçbir şey söylemedi |

⭐ Düzeltme ölçütü önceden: düzeltmeden sonra kapı bu kayıtlar için **0** demeli.

⚠️ Üçü de KÜÇÜK kusur ve üçü de aynı aileden: **cevabın, kullanıcının koymadığı
bir çıpayı koyması**. Ayrı ayrı bakınca önemsiz görünürler; birlikte bakınca
korpusun kullanıcıya kendi anlatmadığı bir zaman/kişi çerçevesi giydirme eğilimi.

Girdi : data/judged/v0.0.12.jsonl
Çıktı : data/judged/v0.0.13.jsonl · reports/analiz/2026-09-18-v013-revizyon.md
Kullanım: uv run python scripts/analiz/2026-09-18-v013-zaman-revizyonu.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
GIRDI = KOK / "data/judged/v0.0.12.jsonl"
CIKTI = KOK / "data/judged/v0.0.13.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-v013-revizyon.md"

from checks import run_checks  # noqa: E402

DUZELTME = [
    ("hekimin planlayacağı bir şey", "bir hekimin planlayacağı bir şey",
     "belirli → belirsiz: §8b rol adlandırmayı ister ama var olmayan bir hekime "
     "gönderme yapmadan"),
    ("dün gece ekranı en son kapatabildiğin an hangisiydi",
     "ekranı en son kapatabildiğin an hangisiydi",
     "kullanıcı ALIŞKANLIK anlattı, belirli bir geceyi değil ⇒ çıpa kaldırıldı"),
    ("bir hafta önce bilmediğin bir şeyi bu hafta öğrendin",
     "daha önce bilmediğin bir şeyi bu hafta öğrendin",
     "kullanıcı yalnız *«bu hafta»*yı çıpaladı ⇒ belirsiz geçmişe çevrildi"),
]
BAYAT = ("metin bu kayıtta düzeltildi; yargı düzeltmeden ÖNCEKİ metne verildi "
         "(zaman/kaynak çıpası, 2026-09-18)")


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]


def main() -> int:
    ham = GIRDI.read_bytes()
    kayitlar = [json.loads(s) for s in ham.decode("utf-8").splitlines() if s.strip()]
    rapor, hata = [], []
    for eski, yeni, gerekce in DUZELTME:
        hedef = [r for r in kayitlar if any(eski in (m.get("content") or "")
                                            for m in r["messages"] if m["role"] == "assistant")]
        if len(hedef) != 1:
            hata.append(f"«{eski[:44]}»: {len(hedef)} kayıtta (1 bekleniyordu)")
            continue
        r = hedef[0]
        for m in r["messages"]:
            if m["role"] == "assistant" and eski in m["content"]:
                m["content"] = m["content"].replace(eski, yeni, 1)
        if not run_checks(r).get("passed"):
            hata.append(f"«{eski[:44]}»: run_checks DÜŞÜRÜYOR")
            continue
        j = r.setdefault("judge", {}) or {}
        j["bayat"] = True
        j["bayat_gerekce"] = BAYAT
        r["judge"] = j
        rapor.append({"id": r["id"], "eski": eski, "yeni": yeni, "gerekce": gerekce,
                      "parti": (r.get("gen_meta") or {}).get("parti"),
                      "sira": (r.get("gen_meta") or {}).get("parti_sira")})
    if hata:
        print("⛔ REVİZYON UYGULANMADI:")
        for h in hata:
            print("   ", h)
        return 1
    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kayitlar),
                     encoding="utf-8")
    sat = ["# v0.0.13 — zaman/kaynak çıpası: 3 düzeltme", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Girdi:** `{GIRDI.relative_to(KOK)}` SHA256-16 `{_sha(ham)}`  ",
           f"**Çıktı:** `{CIKTI.relative_to(KOK)}` SHA256-16 `{_sha(CIKTI.read_bytes())}`", "",
           "| kayıt | eski | yeni | gerekçe |", "|---|---|---|---|"]
    for x in rapor:
        sat.append(f"| `{x['id'][:10]}` | {x['eski'][:44]} | {x['yeni'][:44]} | {x['gerekce']} |")
    sat += ["", "⚠️ Üçü de KÜÇÜK kusur ve üçü de aynı aileden: **cevabın, kullanıcının koymadığı",
            "bir çıpayı koyması**. Ayrı ayrı bakınca önemsiz görünürler; birlikte bakınca",
            "korpusun kullanıcıya kendi anlatmadığı bir zaman/kişi çerçevesi giydirme eğilimi.", "",
            "⛔⛔ Üç kaydın yargısı **BAYAT** ilan edildi; yeniden yargılama yapılmadı.", ""]
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    (KOK / f"reports/analiz/{TARIH}-v013-revizyon.json").write_text(
        json.dumps({"tarih": TARIH, "girdi_sha256_16": _sha(ham),
                    "cikti_sha256_16": _sha(CIKTI.read_bytes()), "duzeltme": rapor},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n".join(sat))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
