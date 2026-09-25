#!/usr/bin/env python3
"""v0.0.12 — 16 alıntı birebir hâline getiriliyor (T168).

⛔ **Neden.** T168: model alıntılarken Türkçenin **«de/da» edatını** ve hedge
öbeklerini (*«biraz»*, *«aslında»*, *«bunu»*, *«ben»*) düşürüyor. *«içim DE bir
tuhaf»* ile *«içim bir tuhaf»* aynı şeyi söylemez — *«de»* başka bir şeyin daha
olduğunu ima eder ve alıntıdan silinince kullanıcının söylediğinden **başka bir
cümle** tırnak içine alınmış olur.

⭐ **Düzeltme ölçütü ÖNCEDEN yazıldı ve doğrulanabilir:** düzeltmeden sonra alıntı
kapısı bu kayıtlar için **0** demeli. Betik bunu kendisi sınar.

⚠️ Üç düzeltmede **noktalama dışarı taşındı**: kullanıcı o cümleyi noktayla
bitirmemiş (*«…onlar bilmiyor, o kötü geliyor»*) ⇒ nokta tırnağın içinde kalırsa
alıntı birebir olmaz. ➡️ *Birebirlik noktalamayı da kapsar; bir nokta eklemek
cümleyi bitirmek demektir ve kullanıcı onu bitirmemiş olabilir.*

⛔ Biri ötekilerden farklı sınıftan: *«Babam da idare etti»* bir alıntı değil
**sentez**di — kullanıcı *«babamda da olurdu böyle şeyler, hiç doktora gitmedi,
idare etti»* yazmış. ⇒ Kullanıcının kendi ardışık sözü tırnağa alındı.
Ve *«icra dosyasına…»* alıntısı ortadaki yan cümleyi atıp iki ucu bitiştiriyordu
(T104 kırpma) ⇒ alıntı **kısaltıldı**, bitişik olan kısımla sınırlandı.

Girdi : data/judged/v0.0.11.jsonl
Çıktı : data/judged/v0.0.12.jsonl · reports/analiz/2026-09-18-v012-revizyon.md
Kullanım: uv run python scripts/analiz/2026-09-18-v012-alinti-revizyonu.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
GIRDI = KOK / "data/judged/v0.0.11.jsonl"
CIKTI = KOK / "data/judged/v0.0.12.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-v012-revizyon.md"

from checks import run_checks  # noqa: E402
from tohum_guvenlik import tr_fold  # noqa: E402

# (eski dizge, yeni dizge, sınıf) — tırnaklar DAHİL, noktalama denetimi için
DUZELTME = [
    ('"hiçbir işe yaramıyor"', '"hiç bir işe yaramıyor"', "yazım"),
    ('"yanlış mı bilmiyorum, garip hissediyorum"',
     '"Yanlış mı bilmiyorum, biraz garip hissediyorum"', "hedge düştü: «biraz»"),
    ('"icra dosyasına bir nefes olur, kimsenin haberi olmaz"',
     '"icra dosyasına bir nefes olur"', "⛔ yan cümle elenmişti (T104) ⇒ alıntı kısaltıldı"),
    ('"ben de katılıyorum"', '"ben de aslında buna katılıyorum"', "hedge düştü: «aslında buna»"),
    ('"Kumardan diyemezsin di mi"', '"kumardan diyemezsin ki di mi"', "edat düştü: «ki»"),
    ('"niye hep yalnızım"', '"niye ben hep yalnızım"', "özne düştü: «ben»"),
    ('"Gerçeği söylemek mümkün değil"', '"gerçeği söylemek de mümkün değil"', "edat düştü: «de»"),
    ('"İçim buna razı değil"', '"içim de buna razı değil"', "edat düştü: «de»"),
    ('"Hak ettim galiba"', '"Hak ettim bunu galiba"', "hedge düştü: «bunu»"),
    ('"nasıl uzak dururum"', '"nasıl uzak durabilirim"', "fiil değiştirilmişti"),
    ('"İçim bir tuhaf"', '"içim de bir tuhaf"', "edat düştü: «de»"),
    ('"Ortada büyük bir şey yok"', '"ortada büyük bir şey de yok"', "edat düştü: «de»"),
    ('"eşim bilse zaten anlamaz."', '"eşim de bilse zaten anlamaz."', "edat düştü: «de»"),
    ('"Benim bildiğim bir şey var ki onlar bilmiyor."',
     '"Benim bildiğim bir şey var ki onlar bilmiyor".', "⚠️ nokta dışarı: kullanıcı bitirmemiş"),
    ('"hak etmiyorum bu cümleyi."', '"hak etmiyorum bu cümleyi".',
     "⚠️ nokta dışarı: kullanıcı bitirmemiş"),
    ('"Babam da idare etti"', '"hiç doktora gitmedi, idare etti"',
     "⛔ alıntı değil SENTEZdi ⇒ kullanıcının kendi ardışık sözü"),
]
BAYAT = ("metin bu kayıtta düzeltildi; yargı düzeltmeden ÖNCEKİ metne verildi "
         "(alıntı birebirliği, 2026-09-18)")


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]


def _kaynak(r: dict) -> str:
    p = [m.get("content", "") for m in r["messages"] if m.get("role") == "user"]
    p += [c.get("metin", "") for c in (r.get("context") or [])]
    return tr_fold(" \n ".join(p))


def main() -> int:
    ham = GIRDI.read_bytes()
    kayitlar = [json.loads(s) for s in ham.decode("utf-8").splitlines() if s.strip()]
    rapor, hata = [], []
    for eski, yeni, sinif in DUZELTME:
        hedef = [r for r in kayitlar
                 if any(eski in (m.get("content") or "") for m in r["messages"]
                        if m["role"] == "assistant")]
        if len(hedef) != 1:
            hata.append(f"«{eski[:40]}»: {len(hedef)} kayıtta geçiyor (1 bekleniyordu)")
            continue
        r = hedef[0]
        for m in r["messages"]:
            if m["role"] == "assistant" and eski in m["content"]:
                m["content"] = m["content"].replace(eski, yeni, 1)
        # ⭐ ÖLÇÜT: yeni alıntı kullanıcının metninde BİREBİR bulunmalı
        ic = yeni.strip('"').rstrip('".')
        if tr_fold(ic) not in _kaynak(r):
            hata.append(f"«{ic[:44]}»: düzeltmeden sonra kaynakta BULUNAMADI")
            continue
        if not run_checks(r).get("passed"):
            hata.append(f"«{eski[:40]}»: run_checks DÜŞÜRÜYOR")
            continue
        j = r.setdefault("judge", {}) or {}
        j["bayat"] = True
        j["bayat_gerekce"] = BAYAT
        r["judge"] = j
        rapor.append({"id": r["id"], "eski": eski, "yeni": yeni, "sinif": sinif,
                      "parti": (r.get("gen_meta") or {}).get("parti"),
                      "sira": (r.get("gen_meta") or {}).get("parti_sira")})

    if hata:
        print("⛔ REVİZYON UYGULANMADI:")
        for h in hata:
            print("   ", h)
        return 1

    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kayitlar),
                     encoding="utf-8")
    sat = ["# v0.0.12 — 16 alıntı birebir hâline getirildi", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Girdi:** `{GIRDI.relative_to(KOK)}` SHA256-16 `{_sha(ham)}` · "
           f"**{len(kayitlar)}** kayıt  ",
           f"**Çıktı:** `{CIKTI.relative_to(KOK)}` SHA256-16 `{_sha(CIKTI.read_bytes())}`", "",
           f"⭐ **{len(rapor)} düzeltme** · her biri için ölçüt betikte sınandı: yeni alıntı",
           "kullanıcının metninde **birebir** bulunmalı ve `run_checks` geçmeli.", "",
           "| kayıt | eski | yeni | sınıf |", "|---|---|---|---|"]
    for x in rapor:
        sat.append(f"| `{x['id'][:10]}` | {x['eski'][:46]} | {x['yeni'][:46]} | {x['sinif']} |")
    sat += ["", "## ⚠️ Üç düzeltmede noktalama dışarı taşındı", "",
            "Kullanıcı o cümleyi noktayla bitirmemiş (*«…onlar bilmiyor, o kötü geliyor»*) ⇒",
            "nokta tırnağın içinde kalırsa alıntı birebir olmaz.", "",
            "➡️⭐⭐ *Birebirlik noktalamayı da kapsar: bir nokta eklemek cümleyi BİTİRMEK",
            "demektir ve kullanıcı onu bitirmemiş olabilir.*", "",
            "## ⛔ İki düzeltme farklı sınıftan", "",
            "| kayıt | neden farklı |", "|---|---|",
            "| *«icra dosyasına…»* | alıntı ortadaki yan cümleyi (*«eşim duymaz»*) atıp iki ucu "
            "bitiştiriyordu — T104'ün özgün kırpma kusuru ⇒ alıntı **kısaltıldı** |",
            "| *«Babam da idare etti»* | bir alıntı değil **sentez**di; kullanıcı *«babamda da "
            "olurdu böyle şeyler, hiç doktora gitmedi, idare etti»* yazmış ⇒ kendi ardışık sözü |",
            "", "## ⛔⛔ On altı kaydın yargısı BAYAT", "",
            "Judge bu kayıtları düzeltmeden **önceki** metin üzerinde puanladı ⇒ "
            "`judge.bayat: true`. Puanlar düşürülmedi ama hiçbir sayıda sessizce kullanılamaz.", ""]
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    (KOK / f"reports/analiz/{TARIH}-v012-revizyon.json").write_text(
        json.dumps({"tarih": TARIH, "girdi_sha256_16": _sha(ham),
                    "cikti_sha256_16": _sha(CIKTI.read_bytes()), "duzeltme": rapor},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n".join(sat[:9]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
