#!/usr/bin/env python3
"""Tohumun KENDİ BEYANINA göre kriz tohumu üretime girmiş mi.

⛔⛔ **Neden var.** `2026-09-17-kriz-suzgeci-yanlis-negatif` tohumun **mesaj
metnini** tarıyor ve dolaylı ifadeleri kaçırıyordu. Genişletilmiş hâli
`ce39d82bf868e5f2`'yi yakaladı — ve o tohumun `meta.notlar.esdurumlar` alanı
zaten **«Aktif intihar düşüncesi»** yazıyordu. ⇒ Regex'le aradığımız şeyi tohum
korpusu BEYAN EDİYORMUŞ. Beyan okumak desen aramaktan hem daha ucuz hem daha
güvenilir; desen süzgeci yerine geçmez, ÖNÜNE geçer.

⭐⭐ **İki sınıf, tek alan — ve ayrım üretim kararını değiştiriyor:**

  1. **SERT** — `esdurumlar`'da *«Aktif intihar …»* ya da
     `risk_seviyesi == "cok_yuksek"`. Tohumun kendisi mevcut bir kriz beyan
     ediyor. Kural 3: kriz davranışı **etik kurul + uzman onayı** ister.
     ⇒ Üretime giremez; bu kapı ateşlerse çıkış kodu 1.

  2. **PERSONA** — *«İntihar düşüncesi olası»*, *«… sinyali»*. ⚠️ ÖLÇÜLDÜ:
     üretilmiş 11 tohumun **7'si aynı `esdurumlar` listesini paylaşıyor**
     (tefeci-haciz personası). Yani bu alan TURU değil PERSONAYI anlatıyor:
     kişi risk taşıyor, çekilen mesaj kriz ifade etmiyor olabilir.
     ⇒ Bu sınıfı üretimden ELEMEK borç/tefeci eksenini tamamen kaybettirir —
     ki §8b yönlendirme davranışının en çok önem taşıdığı eksen odur.
     ⇒ Rapor edilir, **elenmez**; çıkış kodunu etkilemez.

⛔ **Bu kapının kurmadığı hüküm.** PERSONA sınıfının üretilebilir olup olmadığı
bir ETİK KARARDIR ve burada verilmemiştir; kapı yalnızca sayıyı görünür kılar.

Kullanım: uv run python scripts/analiz/2026-09-17-tohum-beyan-kriz-kapisi.py [kayitlar.jsonl ...]
          (argümansız: data/candidates/*.jsonl + datasets/v*/train.jsonl)
"""
from __future__ import annotations
import glob, hashlib, json, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]

SERT = re.compile(r"aktif\s+intihar|aktif\s+özkıyım|intihar\s+girişim|planlı\s+intihar", re.I)
PERSONA = re.compile(r"intihar|özkıyım|kendine zarar|ölüm düşünce", re.I)


def _tohumlar() -> dict:
    t = {}
    for f in sorted(glob.glob(str(KOK / "data/seeds*.jsonl"))):
        for s in Path(f).read_text(encoding="utf-8").splitlines():
            if s.strip():
                d = json.loads(s)
                t[d["seed_id"]] = d
    return t


def _sinif(d: dict) -> str | None:
    meta = d.get("meta", {}) or {}
    es = (meta.get("notlar", {}) or {}).get("esdurumlar") or []
    if any(SERT.search(e) for e in es) or meta.get("risk_seviyesi") == "cok_yuksek":
        return "sert"
    if any(PERSONA.search(e) for e in es):
        return "persona"
    return None


def main(yollar: list[str]) -> int:
    tohum = _tohumlar()
    sinif = {sid: s for sid, d in tohum.items() if (s := _sinif(d))}
    if not yollar:
        yollar = sorted(glob.glob(str(KOK / "data/candidates/*.jsonl"))) + \
                 sorted(glob.glob(str(KOK / "datasets/v*/train.jsonl")))
    bulgu: dict[str, dict] = {}
    for f in yollar:
        p = Path(f) if Path(f).is_absolute() else KOK / f
        for s in p.read_text(encoding="utf-8").splitlines():
            if not s.strip():
                continue
            sid = (json.loads(s).get("gen_meta") or {}).get("seed_id")
            if sid in sinif:
                b = bulgu.setdefault(sid, {"seed_id": sid, "sinif": sinif[sid],
                                           "dosyalar": [], "yayimlandi": False})
                ad = str(p.relative_to(KOK))
                if ad not in b["dosyalar"]:
                    b["dosyalar"].append(ad)
                b["yayimlandi"] |= ad.startswith("datasets/")
    sert = [b for b in bulgu.values() if b["sinif"] == "sert"]
    pers = [b for b in bulgu.values() if b["sinif"] == "persona"]
    for b in bulgu.values():
        n = (tohum[b["seed_id"]]["meta"].get("notlar", {}) or {})
        b["esdurumlar"] = n.get("esdurumlar")
        b["risk_seviyesi"] = tohum[b["seed_id"]]["meta"].get("risk_seviyesi")
    ozet = {"tarih": "2026-09-17",
            "betik": "scripts/analiz/2026-09-17-tohum-beyan-kriz-kapisi.py",
            "tohum": len(tohum),
            "tohum_sha256_16": {Path(f).name: hashlib.sha256(Path(f).read_bytes()).hexdigest()[:16]
                                for f in sorted(glob.glob(str(KOK / "data/seeds*.jsonl")))},
            "beyanla_sert": sum(1 for v in sinif.values() if v == "sert"),
            "beyanla_persona": sum(1 for v in sinif.values() if v == "persona"),
            "taranan_dosya": len(yollar),
            "uretilmis_sert": sorted(b["seed_id"] for b in sert),
            "uretilmis_persona": sorted(b["seed_id"] for b in pers),
            "bulgu": sorted(bulgu.values(), key=lambda b: (b["sinif"], b["seed_id"]))}
    # ⛔ ÇIKTI ADI GİRDİDEN BAĞIMSIZDI ve tek bir partiye koşulunca tam korpus
    # raporunu EZDİ — T108'in aynı sınıfı, bu kez kendi kapımda. ⇒ Kapsam ada
    # giriyor: argümansız koşu "tam", tek dosya koşusu dosyanın adını alır.
    etiket = "tam" if len(sys.argv) <= 1 else "-".join(Path(y).stem for y in sys.argv[1:])[:60]
    cikti = KOK / f"reports/analiz/2026-09-17-tohum-beyan-kriz-kapisi-{etiket}.json"
    cikti.write_text(json.dumps(ozet, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"tohum {len(tohum)} · beyanla SERT {ozet['beyanla_sert']} · "
          f"beyanla PERSONA {ozet['beyanla_persona']}")
    print(f"⛔ SERT olup ÜRETİLMİŞ: {len(sert)}")
    for b in sert:
        y = " · ⛔ YAYIMLANMIŞ" if b["yayimlandi"] else ""
        print(f"   {b['seed_id']}  {b['dosyalar']}{y}")
    print(f"⚠️ PERSONA olup üretilmiş: {len(pers)} "
          f"(yayımlanmış {sum(1 for b in pers if b['yayimlandi'])}) — elenmez, KARAR DIŞARIDA")
    for b in pers:
        y = " · yayımlanmış" if b["yayimlandi"] else ""
        print(f"   {b['seed_id']}{y}")
    print(f"→ {cikti.relative_to(KOK)}")
    return 1 if sert else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
