#!/usr/bin/env python3
"""Kriz süzgecinin YANLIŞ NEGATİFLERİ — dolaylı ifadeler.

⛔⛔ **Neden var.** `2026-09-15-v4-parti1-plan.py::KRIZ_ANAHTAR` havuzdan kriz
tohumlarını eler ve **etik kurul kararı beklerken kriz malzemesini üretimden uzak
tutan TEK mekanizma** odur (K23, `uretim-v4` §8b'nin Kural 3 sınırı).

⛔ Desen yalnız **AÇIK** ifadeleri arıyor (*intihar*, *canıma kıy*,
*yaşamak istemiyorum*, *uyanmasam*). v5-parti4 planında `#18`'in tohumu şu
cümleyi taşıyor ve süzgeçten **geçmiş**:

    «Bazen düşünüyorum ben olmasam belki herkes daha rahat eder.»

Bu, *algılanan yük* (perceived burdensomeness) biçiminde **edilgen intihar
düşüncesi**dir ve literatürde en sık görülen dolaylı ifadelerden biridir.

⭐ Bu betik iki şeyi ölçer:
  1. havuzda dolaylı ifade taşıyan kaç tohum var ve kaçı `KRIZ_ANAHTAR`'dan geçiyor
  2. ⛔ bunlardan kaçı **zaten üretilmiş** bir kayda girmiş

⚠️ Dolaylı desen **elle yazıldı** ve tam değildir; bulunan sayı bir **ALT
SINIRDIR**. Yön Kural 3 açısından güvenli taraftadır: eksik yakalar, fazla değil.
"""
from __future__ import annotations
import glob, hashlib, json, re, sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
_sp = _iu.spec_from_file_location("p1", KOK / "scripts/analiz/2026-09-15-v4-parti1-plan.py")
P1 = _iu.module_from_spec(_sp); _sp.loader.exec_module(P1)

# ─── DOLAYLI ifadeler: edilgen düşünce · algılanan yük · varoluşsal bıkkınlık ──
DOLAYLI = re.compile(
    r"ben olmasa[mn]|olmasaydı[mn]|yokluğum|yok olsa[mn]"
    r"|herkes daha (rahat|iyi)|daha rahat eder|kurtulurlar"
    r"|yük oluyorum|yüküm ol|başlarına yük|kimseye fayda"
    r"|kaybolmak isti|yok olmak isti|silinmek isti"
    r"|uyanmak istemiyorum|uyanmak zorunda"
    r"|anlamı kalmadı|hiçbir şeyin anlamı|nefes almak bile"
    r"|devam etmek istemiyorum|artık dayanamıyorum"
    # ⛔⛔ İKİNCİ GENİŞLETME (2026-09-17, T116). v5-parti7'nin PLANINA
    # `27ecde0ae08f064c` girdi: *«Boş ver beni, yaşamak da istemiyorum zaten.»*
    # ÜÇ SÜZGEÇ DE KAÇIRDI — açık desen, dolaylı desen ve beyan kapısı (tohum
    # `persona` sınıfındaydı ve T107 o sınıfı bilerek bırakıyordu).
    # ➡️⭐ *«İstememek» fiilinin nesnesi sonsuz: yok olmak, devam etmek,
    # uyanmak, YAŞAMAK. Her yeni nesne ayrı bir kaçak demek ve sözlük bu
    # ailede yapısal olarak eksik kalıyor.*
    r"|yaşamak( da)? istemiyorum|yaşamak istemem|hayatta kalmak istemiyorum"
    r"|yaşamanın anlamı|yaşama hevesim|ölsem de|ölsem keşke|ölmek istiyorum"
    r"|bitse de kurtulsam|bitse artık|son bulsa"
    # ⛔⛔ ÜÇÜNCÜ GENİŞLETME (2026-09-20, v6-parti1 planı). `#29`
    # (`kimyasal_madde:st_001:1088`) PLANA girdi ve **dört kapının dördü de
    # kaçırdı**: *«İçimden 'belki herkesi rahatlatmak için ortadan çekilsem'
    # geçiyor»*. Tohum `risk_seviyesi: yuksek` (SERT eşiği `cok_yuksek`),
    # `esdurumlar`'da «Aktif intihar» yok, iki desen süzgeci de eşleşmedi.
    # ➡️⭐⭐ *Kaçağın sebebi yine SÖZLÜK: süzgeç «herkes daha rahat» (GEÇİŞSİZ)
    # arıyordu, tohumda «herkesi rahatlatmak» (GEÇİŞLİ) vardı; «yok olsam»
    # arıyordu, tohumda «ortadan çekilsem» vardı. Aynı düşünce, başka fiil —
    # ikinci genişletmenin kendi teşhisinin tekrarı.*
    # ⚠️ Çekilme fiilleri tek başına alınıyor (işaretli ifadeler), rahatlatma
    # ise ancak çekilmeyle BİRLİKTE — «herkesi rahatlatmak» tek başına zararsız.
    r"|ortadan çekil|ortadan kalksa[mn]|aradan çekil|aradan çıksa[mn]"
    r"|çekilip gitsem|silinip gitsem"
    r"|(rahatlat|rahatlas)\w*[^.!?]{0,40}(çekil|yok ol|gitsem|kalksam)"
    r"|(çekil|yok ol|gitsem|kalksam)\w*[^.!?]{0,40}(rahatlat|rahatlas)",
    re.I)
CIKTI = KOK / "reports/analiz/2026-09-17-kriz-suzgeci-yanlis-negatif.json"


def main() -> int:
    tohumlar = [json.loads(s) for s in
                (KOK / "data/seeds.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
    # üretilmiş kayıtların tohum kimlikleri
    uretilmis: dict[str, list[str]] = {}
    for f in sorted(glob.glob(str(KOK / "data/candidates/*.jsonl"))):
        for s in Path(f).read_text(encoding="utf-8").splitlines():
            if not s.strip():
                continue
            r = json.loads(s)
            sid = (r.get("gen_meta") or {}).get("seed_id")
            if sid:
                uretilmis.setdefault(sid, []).append(Path(f).name)

    dolayli, acik, kacan, uretilen = [], [], [], []
    for t in tohumlar:
        m = t["user_message"]
        d = bool(DOLAYLI.search(m))
        a = bool(P1.KRIZ_ANAHTAR.search(m))
        if d:
            dolayli.append(t)
        if a:
            acik.append(t)
        if d and not a:                      # ⛔ süzgecin kaçırdığı
            kayit = {"seed_id": t["seed_id"], "source_id": t["source_id"],
                     "eslesen": DOLAYLI.search(m).group(0),
                     "metin": m[:180]}
            kacan.append(kayit)
            if t["seed_id"] in uretilmis:
                kayit["uretildi"] = uretilmis[t["seed_id"]]
                uretilen.append(kayit)

    ozet = {"tarih": "2026-09-17",
            "betik": "scripts/analiz/2026-09-17-kriz-suzgeci-yanlis-negatif.py",
            "tohum": len(tohumlar),
            "acik_desen_yakaladigi": len(acik),
            "dolayli_desen_yakaladigi": len(dolayli),
            "⛔ suzgecin_kacirdigi": len(kacan),
            "⛔⛔ kacirilip_URETILEN": len(uretilen),
            "uretilen_kayitlar": uretilen,
            "kacan_ornekler": kacan[:25]}
    CIKTI.write_text(json.dumps(ozet, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"tohum {len(tohumlar)} · açık desen {len(acik)} · dolaylı desen {len(dolayli)}")
    print(f"⛔ süzgecin kaçırdığı: {len(kacan)}")
    print(f"⛔⛔ kaçırılıp ÜRETİLEN: {len(uretilen)}")
    for u in uretilen:
        print(f"   {u['seed_id']} «{u['eslesen']}» → {u['uretildi']}")
    print(f"\nörnekler:")
    for k in kacan[:6]:
        print(f"   «{k['eslesen']}» — {k['metin'][:120]}")
    print(f"→ {CIKTI.relative_to(KOK)}")
    return 1 if uretilen else 0


if __name__ == "__main__":
    raise SystemExit(main())
