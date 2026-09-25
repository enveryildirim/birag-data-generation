#!/usr/bin/env python3
"""`celiskili-parti3`'ün iki güvenlik bayrağını onarır.

⛔⛔ **Bulgu deseni ve bu kalemin asıl değeri.** 13 kaydın **2'si**
`klinik_guvenlik_ihlali` aldı ve ikisi de `guvenlik_tipi: riski_atlama`.
⭐⭐ **İkisi de `turn_ending = takdir`** — ve partideki `takdir`
kayıtlarının **ikisi de** ateşledi (2/2). ⇒ *Açıklığı övmek, sinyali
atlamanın kapısı oluyor: «yazacak kadar açık yazmışsın» kapanışı, aynı
mesajdaki risk işaretini **yerine geçerek** susturuyor.*

  · **#15** — kullanıcı üç hafta önceki kazancından beri **her gece
    oranlara baktığını** yazıyor; cevap bunu yalnız «açık yazmışsın»
    diye övüyor.
  · **#24** — kullanıcı eve varmadan şişeyi düşünüp **kendinden
    korktuğunu** yazıyor; cevap yine yalnız övüyor ve dil sorusuna
    geçiyor.

⛔ **Kural 3: güvenlik ekseninde gerileme «kabul edilebilir» değildir.**
Bu kayıtlar onarılmadan derlemeye giremez — üstelik `build.py` onları
`judge_safety_violation` ile **zaten elerdi** ve kota 11'e düşerdi.

⭐ **Onarım deseni T267'nin üçüncü turundan alındı** (orada ölçülmüştü):
sinyali **adlandır**, rol sınırını **koru**, kararı **kullanıcıya bırak**
(izin sor). Tanı yok, miktar yorumu yok, protokol yok.

⛔ `turn_ending` beyanı da metinle birlikte değişir (T263): kapanış artık
takdir değil, açık uçlu soru.

⛔⛔ Yargı ESKİ metne aittir; onarılan metin **yeniden yargılanmalıdır**
ve bu betik yeniden yargıyı koşmaz.

Çıktı: data/candidates/celiskili-parti3.jsonl (yerinde)
       reports/analiz/2026-09-22-celiskili-p3-guvenlik-onarim.md
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from checks import run_checks  # noqa: E402
from kunye import betik_tarihi  # noqa: E402
from yansitma import alinti_ihlalleri  # noqa: E402

HEDEF = KOK / "data/candidates/celiskili-parti3.jsonl"
RAPOR = KOK / "reports/analiz/2026-09-22-celiskili-p3-guvenlik-onarim.md"

ONARIM = {
 15: dict(
    sinyal="üç hafta önceki kazançtan beri her gece oranlara bakma",
    eski=("Şunu da söyleyeyim: o günden beri her gece oranlara baktığını "
          "yazacak kadar açık yazmışsın."),
    yeni=("Şunu da söyleyeyim: o günden beri her gece oranlara baktığını sen "
          "yazdın. Onu burada konuşmak ister misin, yoksa görüşmeye mi "
          "bırakalım? Nasıl istersen."),
    eski_thk=("Açık yazmasını takdir edip bırakıyorum, soru sormuyorum."),
    yeni_thk=("Her gece oranlara bakmasını övgüyle kapatıp geçmiyorum — "
              "adlandırıyorum. Ama ne anlama geldiğini söylemiyorum ve ne "
              "yapacağını ben belirlemiyorum: izin soruyorum, kararı ona "
              "bırakıyorum."),
    ust={"turn_ending": "acik_uclu_soru"}),

 24: dict(
    sinyal="eve varmadan şişeyi düşünme ve kendinden korkma",
    eski=("Şunu da söyleyeyim: «O an korktum kendimden» diye yazacak kadar "
          "açık yazmışsın."),
    yeni=("«O an korktum kendimden» diye yazmışsın. Şu an nasılsın — o korku "
          "hâlâ duruyor mu?"),
    eski_thk=("Açık yazmasını takdir edip bırakıyorum."),
    yeni_thk=("Korkusunu övgüyle kapatıp dil sorusuna geçmiyorum — şu anki "
              "hâlini soruyorum. Tanı koymuyorum, «geçer» demiyorum, hiçbir "
              "protokol vermiyorum; yalnız kendi sözcüğünü alıp şimdiye "
              "getiriyorum."),
    ust={"turn_ending": "acik_uclu_soru"}),
}


def main() -> int:
    kayitlar = [json.loads(l) for l in open(HEDEF)]
    degisen, degisti = [], False
    for r in kayitlar:
        no = r["gen_meta"].get("celiskili_banka_no")
        o = ONARIM.get(no)
        if not o:
            continue
        cev = r["messages"][2]
        zaten = o["yeni"] in cev["content"]
        if not zaten:
            if o["eski"] not in cev["content"]:
                raise SystemExit(f"⛔ #{no}: onarılacak kapanış bulunamadı — "
                                 "HİÇBİR ŞEY yazılmadı")
            cev["content"] = cev["content"].replace(o["eski"], o["yeni"])
            if o["eski_thk"] not in cev["thinking"]:
                raise SystemExit(f"⛔ #{no}: thinking bulunamadı")
            cev["thinking"] = cev["thinking"].replace(o["eski_thk"],
                                                      o["yeni_thk"])
            degisti = True
        for a, v in (o.get("ust") or {}).items():
            if r["gen_meta"].get(a) != v:
                r["gen_meta"][a] = v
                degisti = True
        # ⛔ Yargı eski metne ait — işaretlenir, silinmez (T121).
        if r.get("judge") and not r["judge"].get("_yeniden_yargi_gerekli"):
            r["judge"]["_yeniden_yargi_gerekli"] = betik_tarihi(__file__)
            degisti = True
        chk = run_checks(r)
        if not chk["passed"]:
            raise SystemExit(f"⛔ #{no} onarımdan sonra kapıdan geçmiyor: "
                             + str([f"{a}={v}" for a, v in chk.items()
                                    if a.endswith("_error") and v][:3]))
        if alinti_ihlalleri(r):
            raise SystemExit(f"⛔ #{no} alıntı ihlali taşıyor")
        degisen.append((no, o["sinyal"], r["gen_meta"]["turn_ending"]))

    if len(degisen) != len(ONARIM):
        raise SystemExit(f"⛔ {len(degisen)}/{len(ONARIM)} onarıldı — eksik")
    if degisti:
        HEDEF.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n"
                                 for r in kayitlar), encoding="utf-8")
        assert HEDEF.exists()

    import collections
    te = collections.Counter(r["gen_meta"]["turn_ending"] for r in kayitlar)

    s = [f"# `celiskili-parti3` — iki güvenlik bayrağı onarıldı", "",
         f"**Betik:** `{Path(__file__).relative_to(KOK)}` · "
         f"**Tarih:** {betik_tarihi(__file__)}  ",
         f"**Onarılan:** {len(degisen)}/13 kayıt  ", "",
         "## ⭐⭐ Bulgu deseni — bu kalemin asıl değeri", "",
         "13 kaydın **2'si** `klinik_guvenlik_ihlali` aldı ve ikisi de "
         "`guvenlik_tipi: riski_atlama`. **İkisi de `turn_ending = takdir`** "
         "— ve partideki `takdir` kayıtlarının **ikisi de** ateşledi (**2/2**).",
         "",
         "➡️ *Açıklığı övmek, sinyali atlamanın kapısı oluyor: «yazacak kadar "
         "açık yazmışsın» kapanışı, aynı mesajdaki risk işaretinin **yerine "
         "geçerek** onu susturuyor.*", "",
         "⛔⛔ **Bu bir ORAN DEĞİL, iki vakadır** (T252'nin dersi): "
         "`takdir` 2/2 ateşledi ama payda **2**. Bir eğilim iddiası için "
         "başka partilerdeki `takdir` kayıtları ayrıca sayılmalı — "
         "**sayılmadı**.", "",
         "## Onarılanlar", "", "| banka | atlanan sinyal | yeni `turn_ending` |",
         "|---:|---|---|"]
    s += [f"| #{n} | {sg} | `{te_}` |" for n, sg, te_ in sorted(degisen)]
    s += ["", "⭐ **Onarım deseni T267'nin üçüncü turundan alındı** (orada "
          "ölçülmüştü): sinyali **adlandır**, rol sınırını **koru**, kararı "
          "**kullanıcıya bırak**. Tanı yok, miktar yorumu yok, protokol yok.",
          "", f"⭐ Partinin `turn_ending` dağılımı artık: "
          + " · ".join(f"`{k}` {v}" for k, v in te.most_common()), "",
          "## ⛔ Bunun söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔⛔ **Yargı eski metne ait** | iki kaydın `judge` alanına "
          "`_yeniden_yargi_gerekli` işareti kondu; yargı **silinmedi** "
          "(T121: `judge: null` kaydı eler). Yeniden yargı ayrı koşudur |",
          "| ⛔ **Onarımın işe yaradığı HENÜZ ölçülmedi** | T267'de aynı "
          "desen ikinci turda `mi_uyumu`'yu düşürmüştü; burada da başka bir "
          "ekseni bozabilir |",
          "| ⛔ **`takdir` kusurlu demiyorum** | kusurlu olan, risk sinyali "
          "taşıyan bir mesajı **yalnız** takdirle kapatmak; takdirin kendisi "
          "değil |",
          "| ⛔ **Onarımı ben yazdım** | K30/K260 |"]

    RAPOR.write_text("\n".join(s) + "\n", encoding="utf-8")
    assert RAPOR.exists()
    print(f"⭐ {len(degisen)} kayıt onarıldı, hepsi kapılardan geçti")
    for n, sg, te_ in sorted(degisen):
        print(f"   #{n:2} {sg[:52]:54} → {te_}")
    print(f"   turn_ending: {dict(te)}")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
