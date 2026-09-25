#!/usr/bin/env python3
"""v0.0.10 — sekiz düzeltme: yedi yapısal atıf + bir alıntı birebirliği.

⛔ **Neden bu sekiz.** İkisi de bu oturumda ÖLÇÜLDÜ ve v0.0.9'a yetişemedi:
  · **7 kayıt** (T155) — iddia *«aynı CÜMLEDE»* diyor ama iki öge kullanıcının
    aynı mesajındaki AYRI cümlelerinde. Elle okundu, her biri tek tek doğrulandı.
  · **1 kayıt** (T142) — alıntı birebir değil: kullanıcı *«her şeye karışıyorlar»*
    yazmış, cevap *«her şeye karışmak»* diye alıntılıyor.

⭐ **Düzeltme ilkesi: en az değişiklik.** Yedisinde yanlış olan iddianın İÇERİĞİ
değil **DÜZEYİ** ⇒ tek sözcük değişiyor (*«cümlede»* → *«mesajda»*). Retorik
nokta, cümle yapısı, uzunluk korunuyor.
⚠️ Biri çift kusurlu (`#23`): *«iki tane içtiğini»* kullanıcının sözü değil,
*«bir tane… sonra bir tane daha»*dan çıkarılmış bir SAYIM ⇒ orada kullanıcının
kendi sözü tırnak içinde kullanılıyor.

⛔⛔ **YARGI BAYATLIYOR VE BU İLAN EDİLİYOR.** Judge bu kayıtları YANLIŞ iddia
taşıyan metin üzerinde puanladı; `grounding` ve `alinti_dogrulama` gibi alanlar
doğrudan bu iddiaya bakıyor. Metin değişince yargı o metni tarif etmiyor.
➡️ *Bir yargı, kuyruğa girdiği andaki metni tarif eder* (K103'ün `metin_sha`
mekanizmasının kurulma sebebi). ⇒ Sekiz kaydın `judge` alanına `bayat: true`
ve gerekçe yazılıyor; puanları düşürülmüyor ama **hiçbir sayıda sessizce
kullanılamaz**. Yeniden yargılama ayrı bir iştir.

Girdi : data/judged/v0.0.9.jsonl
Çıktı : data/judged/v0.0.10.jsonl · reports/analiz/2026-09-18-v010-revizyon.md
Kullanım: uv run python scripts/analiz/2026-09-18-v010-yapisal-atif-revizyonu.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
GIRDI = KOK / "data/judged/v0.0.9.jsonl"
CIKTI = KOK / "data/judged/v0.0.10.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-v010-revizyon.md"

from checks import run_checks  # noqa: E402

# id öneki -> (eski dizge, yeni dizge, gerekçe)
# ⛔ `parti_sira` birleşik sette BENZERSİZ DEĞİL (v4-parti2 #41 ile v5-parti4 #41
# ayrı kayıtlar) ⇒ hedefleme `id` ile yapılıyor, sıra numarasıyla değil.
DUZELTME = {
    "34ee4b88cad58794": (
        "Öğle arası çıkıp yaktığını da aynı cümlede söyledin.",
        "Öğle arası çıkıp yaktığını da aynı mesajda söyledin.",
        "*«İnhaleri aldım, kullanmayı da öğrendim.»* ve *«Ama öğle arası çıkıp yine "
        "yaktım.»* iki AYRI cümle; ikisi de aynı mesajda"),
    "fc06767f8f119e4e": (
        "Üst kattaki oğlundan da aynı cümlede söz ettin.",
        "Üst kattaki oğlundan da aynı mesajda söz ettin.",
        "*«Ben de aynı koltuğa oturmuşum gibi hissettim.»* ve *«Üst katta oğlum uyuyor.»* "
        "iki AYRI cümle"),
    "e279f4f4412d0796": (
        "Kahvaltı etmediğini ve iki tane içtiğini aynı cümlede yazdın.",
        "Kahvaltı etmediğini ve \"sonra bir tane daha\" dediğini aynı mesajda yazdın.",
        "⭐ ÇİFT kusur: (1) iki AYRI cümle, (2) *«iki tane»* kullanıcının sözü değil, "
        "*«bir tane… sonra bir tane daha»*dan çıkarılmış bir SAYIM ⇒ kullanıcının kendi "
        "sözü tırnak içinde kullanılıyor"),
    "91b9b2115544382a": (
        "Ama ikisini aynı cümlede tutabilmek zaten bir şey.",
        "Ama ikisini aynı mesajda tutabilmek zaten bir şey.",
        "*«Hayatımın değişmesi gerektiğini biliyorum…»* ve *«Ama oyunu bırakmak "
        "istemiyorum…»* iki AYRI cümle"),
    "53d8896213919c0d": (
        "İki şeyi aynı cümlede söyledin: hesabı yapmaya korkuyorsun ve onsuz yol gitmiyor.",
        "İki şeyi aynı mesajda söyledin: hesabı yapmaya korkuyorsun ve onsuz yol gitmiyor.",
        "*«…hesabını yapmaya bile korkuyorum.»* ve *«Ama bu kahve bu sigara olmadan da yol "
        "gitmiyor…»* iki AYRI cümle"),
    "2df10702dd0ab93f": (
        "ama aynı cümlede tam rakamı eşinin bilmediğini söylüyorsun",
        "ama aynı mesajda tam rakamı eşinin bilmediğini söylüyorsun",
        "⭐ Kapının GÖREMEDİĞİ vaka: iddia tek alıntı taşıyor (*«net kazanmışım»*) ve kapı "
        "≥2 alıntı istiyor. *«…net kazanmışım.»* ile *«Bunu kimseye anlatmıyorum…»* iki "
        "AYRI cümle"),
    "935dfac08ec6ae71": (
        "Üç haftadır uyuyamadığını da aynı cümlede söylüyorsun",
        "Üç haftadır uyuyamadığını da aynı mesajda söylüyorsun",
        "*«son üç haftadır uyuyamıyorum.»* ve *«…gerçekten işe yarıyor.»* iki AYRI cümle"),
    "5bffdc87e0479adf": (
        "Ama arkadaşının sana taksi demesi \"her şeye karışmak\" mıydı, orası bana biraz "
        "başka göründü.",
        "Ama arkadaşının sana taksi demesi de \"her şeye karışıyorlar\" dediğin şeyin "
        "içinde miydi, orası bana biraz başka göründü.",
        "T142: alıntı birebir değil — kullanıcı *«her şeye karışıyorlar»* yazmış, cevap "
        "*«her şeye karışmak»* diye alıntılıyordu ⇒ kullanıcının KENDİ çekimi kullanılıyor"),
}
BAYAT_GEREKCE = ("metin bu kayıtta düzeltildi; yargı düzeltmeden ÖNCEKİ metne verildi "
                 "(yapısal atıf / alıntı birebirliği düzeltmesi, 2026-09-18)")


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]


def _metin_sha(r: dict) -> str:
    """Kaydın PUANLANAN metni — `thinking` hariç (K103 ile aynı tanım)."""
    return hashlib.sha256(json.dumps(
        [{"role": m.get("role"), "content": m.get("content")} for m in r["messages"]],
        ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def main() -> int:
    ham = GIRDI.read_bytes()
    kayitlar = [json.loads(s) for s in ham.decode("utf-8").splitlines() if s.strip()]
    rapor, hata = [], []
    for r in kayitlar:
        d = next(((k, v) for k, v in DUZELTME.items() if r["id"].startswith(k)), None)
        if not d:
            continue
        anahtar, (eski, yeni, gerekce) = d
        asst = [m for m in r["messages"] if m["role"] == "assistant"][-1]
        n = asst["content"].count(eski)
        if n != 1:
            hata.append(f"{anahtar}: eski dizge {n} kez geçiyor (1 bekleniyordu)")
            continue
        onceki_sha = _metin_sha(r)
        asst["content"] = asst["content"].replace(eski, yeni, 1)
        # ⛔ Düzeltme kapıdan geçmelidir: bir revizyon, deney kolunun geçtiği her
        # kapıdan geçmek zorunda (plasebo dersinin aynısı).
        c = run_checks(r)
        if not c.get("passed"):
            hata.append(f"{anahtar}: düzeltmeden sonra run_checks DÜŞÜRÜYOR: {c}")
            continue
        j = r.setdefault("judge", {}) or {}
        j["bayat"] = True
        j["bayat_gerekce"] = BAYAT_GEREKCE
        r["judge"] = j
        rapor.append({"id": r["id"], "parti": (r.get("gen_meta") or {}).get("parti"),
                      "sira": (r.get("gen_meta") or {}).get("parti_sira"),
                      "eski": eski, "yeni": yeni, "gerekce": gerekce,
                      "metin_sha_once": onceki_sha, "metin_sha_sonra": _metin_sha(r)})

    bulunamayan = [k for k in DUZELTME if not any(x["id"].startswith(k) for x in rapor)]
    if hata or bulunamayan:
        print("⛔ REVİZYON UYGULANMADI:")
        for h in hata:
            print("   ", h)
        for b in bulunamayan:
            print(f"    {b}: kayıt bulunamadı")
        return 1

    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kayitlar),
                     encoding="utf-8")
    sat = ["# v0.0.10 — sekiz düzeltme (yapısal atıf + alıntı birebirliği)", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Girdi:** `{GIRDI.relative_to(KOK)}` SHA256-16 `{_sha(ham)}` · "
           f"**{len(kayitlar)}** kayıt  ",
           f"**Çıktı:** `{CIKTI.relative_to(KOK)}` SHA256-16 `{_sha(CIKTI.read_bytes())}`", "",
           f"⭐ **{len(rapor)} kayıt düzeltildi**, öteki {len(kayitlar)-len(rapor)} kayıt "
           "bayt bayt aynı.", "",
           "⭐ **İlke: en az değişiklik.** Yedisinde yanlış olan iddianın İÇERİĞİ değil "
           "**DÜZEYİ** ⇒ tek sözcük (*«cümlede»* → *«mesajda»*); retorik nokta korunuyor.", "",
           "| kayıt | parti | eski → yeni | gerekçe |", "|---|---|---|---|"]
    for x in rapor:
        sat.append(f"| `{x['id'][:10]}` | {x['parti']} #{x['sira']} | "
                   f"*«{x['eski'][:58]}»* → *«{x['yeni'][:58]}»* | {x['gerekce']} |")
    sat += ["", "## ⛔⛔ Yargı bayatladı — ve bu ilan ediliyor", "",
            "Judge bu sekiz kaydı **yanlış iddia taşıyan** metin üzerinde puanladı ve",
            "`grounding` · `alinti_dogrulama` gibi alanlar doğrudan o iddiaya bakıyor.",
            "Metin değişince yargı artık o metni tarif etmiyor.", "",
            "➡️ *Bir yargı, kuyruğa girdiği andaki metni tarif eder* — K103'ün `metin_sha`",
            "mekanizmasının kurulma sebebi bu. ⇒ Sekiz kaydın `judge` alanına **`bayat: true`**",
            "ve gerekçe yazıldı. ⚠️ Puanlar **düşürülmedi** (veri kaybolmasın) ama artık",
            "hiçbir sayıda sessizce kullanılamazlar; yeniden yargılama **ayrı bir iştir**.", "",
            "| kayıt | metin SHA önce | sonra |", "|---|---|---|"]
    for x in rapor:
        sat.append(f"| `{x['id'][:10]}` | `{x['metin_sha_once']}` | `{x['metin_sha_sonra']}` |")
    sat += ["", "⭐ Her düzeltme uygulandıktan SONRA `run_checks` yeniden koşuldu ve sekizi de",
            "geçti — *bir revizyon, deney kolunun geçtiği her kapıdan geçmek zorundadır*.", ""]
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    (KOK / f"reports/analiz/{TARIH}-v010-revizyon.json").write_text(
        json.dumps({"tarih": TARIH, "girdi_sha256_16": _sha(ham),
                    "cikti_sha256_16": _sha(CIKTI.read_bytes()), "duzeltme": rapor},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n".join(sat))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
