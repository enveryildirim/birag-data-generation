#!/usr/bin/env python3
"""T104'ün ALTINCI üyesi: **yapısal atıf** — «aynı cümlede» iddiası.

⛔⛔ **Judge bunu `v5-parti3 #37`'de gösterdi.** Cevap *«…ama meyhanede olduğunu
da AYNI CÜMLEDE söyledin»* diyor; oysa kullanıcı *«meyhanedeydik»*i **bir mesaj
önce** yazmış, *«alkolle alakası yok»*u ise sonraki turda. İki söz aynı cümlede
değil, aynı KONUŞMADA.

⭐ T104 kırpma kusurunun beş üyesi sayılmıştı: alıntı · zaman · kaynak atfı ·
mekân · örüntü. Bu altıncısı: **iki sözün BİRLİKTE söylendiği iddiası.**

➡️ *«Aynı cümlede» bir gözlem gibi durur ama bir İDDİADIR ve yanlış olabilir.
Üstelik yanlış olduğunda özellikle ikna edicidir: kullanıcıya kendi çelişkisini
gösteriyormuş gibi yaparken aslında iki ayrı anı birleştirir.*

⭐⭐ **Kapı iki kova üretir ve ikisini KARIŞTIRMAZ:**
  **(A) OTOMATİK** — cümlede **iki ya da daha çok alıntı** varsa iddia
     sınanabilir: hepsi TEK bir kullanıcı turunda geçiyor mu? Geçmiyorsa ⛔.
  **(B) ELLE** — alıntı yoksa iddia otomatik sınanamaz; kayıt elle okunmak
     üzere ayrı listelenir. ⛔ Bu kova bir BULGU DEĞİL, bir iş listesidir.

⚠️ Tek turlu kayıtlarda iddia zaten doğrudur (tek tur var) ⇒ taranmaz.
"""
from __future__ import annotations
import glob, hashlib, json, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
sys.path.insert(0, str(KOK / "scripts/analiz"))
import _muafiyet as MUAF  # noqa: E402  ⭐ T141: bağışlanan her öge sayılır
from tohum_guvenlik import tr_fold  # noqa: E402

# ⭐⭐ İDDİANIN DÜZEYİ ÖNEMLİ: «aynı cümlede» CÜMLE düzeyinde bir iddiadır,
# «aynı mesajda» TUR düzeyinde. İkisini tur düzeyinde sınamak, birincisini
# olduğundan zayıf sınamak demektir.
# ➡️ *Bir iddiayı sınarken onun kendi düzeyinde sınamak gerekir; daha kaba bir
#    düzeyde sınamak, iddiayı haksız yere aklar.*
IDDIA_CUMLE = re.compile(r"aynı (?:cümlede|cümlenin içinde|satırda|nefeste)", re.I)
IDDIA_TUR = re.compile(r"aynı (?:mesajda|paragrafta)", re.I)
IDDIA = re.compile(r"aynı (?:cümlede|mesajda|satırda|nefeste|paragrafta|cümlenin içinde)", re.I)
# ⛔⛔ OLUMSUZ/KİP BİÇİMLERİ İDDİA DEĞİLDİR. *«"X" ile "Y" aynı cümlede DURAMAZ»*
# ikisinin bir arada söylendiğini söylemiyor; söylemesi GEREKTİĞİNİ ya da
# olamayacağını söylüyor. Kapı ilk yazımında bunu ihlal saydı (`v5-parti7 #48`).
OLUMSUZ = re.compile(r"aynı (?:cümlede|mesajda|satırda|nefeste|paragrafta)\s+"
                     r"\w*(?:maz|mez|amaz|emez|madı|medi|değil)", re.I)
ALINTI = re.compile(r"[\"“”«»]([^\"“”«»]{3,})[\"“”«»]")
CIKTI = KOK / "reports/analiz/2026-09-17-yapisal-atif-kapisi.json"


def _cumleler(t: str) -> list[str]:
    return [c for c in re.split(r"(?<=[.!?])\s+|\n\n", t) if c.strip()]


def _var(alt: list[str], metinler: list[str]) -> bool:
    """Alıntıların HEPSİ tek bir metin biriminde geçiyor mu?

    ⛔ Karşılaştırma `tr_fold` ile: alıntı cümle BAŞINDA olduğunda büyük harfle
    başlar (*«"Bırakacağım" ile …»* ↔ kullanıcı *«bırakacağım diyorum»*) ve düz
    dizge karşılaştırması bunu farklı sayar. ⚠️ Alıntının BİREBİRLİĞİ ayrı bir
    kapının işi (T105); burada sorulan şey NEREDE geçtiği.
    """
    kat = [tr_fold(m) for m in metinler]
    return any(all(tr_fold(a) in t for a in alt) for t in kat)


def main(yollar: list[str]) -> int:
    if not yollar:
        yollar = sorted(glob.glob(str(KOK / "data/candidates/v5-parti*.v4.jsonl")))
    otomatik, elle, sinanan = [], [], 0
    for y in yollar:
        p = Path(y) if Path(y).is_absolute() else KOK / y
        for s in p.read_text(encoding="utf-8").splitlines():
            if not s.strip():
                continue
            r = json.loads(s)
            turlar = [m["content"] for m in r["messages"] if m["role"] == "user"]
            # ⛔⛔ **MUAFİYET KAPININ KENDİ AYRIMINI ÇİĞNİYORDU.** İlk yazımda
            # `len(turlar) < 2 → atla` vardı, gerekçesi *«tek tur: iddia zaten
            # doğru»*. Bu *«aynı MESAJDA»* için doğru, *«aynı CÜMLEDE»* için
            # **yanlış**: tek bir tur birden çok cümle taşır. Judge, kapının
            # atladığı bir kayıtta (`v5-parti8 #13`, tek turlu) tam bu kusuru
            # buldu: iki alıntı kullanıcının İKİ AYRI cümlesinde.
            # ➡️ *Kapıyı cümle ile turu ayırmak için yazdım, sonra muafiyetle o
            #    ayrımı yok ettim. Bir muafiyet, kapının kendi ayrımını
            #    korumalıdır — yoksa kapı kendi sorusunu sormaz.*
            # ⇒ Tek turlu kayıtta yalnız TUR düzeyi iddia atlanır; CÜMLE düzeyi
            #   iddia sınanır.
            tek_tur = len(turlar) < 2
            kul_cumle = [c for t in turlar for c in _cumleler(t)]
            for m in r["messages"]:
                if m["role"] != "assistant" or not m.get("content"):
                    continue
                for c in _cumleler(m["content"]):
                    if not IDDIA.search(c):
                        continue
                    if OLUMSUZ.search(c):
                        # ⛔ olumsuz/kip: iddia değil. ⭐ NET BAĞIŞ: iki alıntı varsa
                        # ve birlikte durmuyorlarsa bu muafiyet GERÇEK bir otomatik
                        # bulguyu düşürüyor demektir; ayrı işaretlenir.
                        _a = ALINTI.findall(c)
                        _d = "cümle" if IDDIA_CUMLE.search(c) else "tur"
                        _net = (len(_a) >= 2
                                and not _var(_a, kul_cumle if _d == "cümle" else turlar))
                        MUAF.yaz("olumsuz_kip" + ("" if _net else " [ZATEN YERDE]"),
                                 r, _a or c.strip()[:60], c.strip())
                        continue
                    sinanan += 1
                    alt = ALINTI.findall(c)
                    duzey = "cümle" if IDDIA_CUMLE.search(c) else "tur"
                    if tek_tur and duzey == "tur":
                        # tek turda «aynı mesajda» zaten doğru — T140'ın daraltılmış
                        # hâli: yalnız TUR düzeyi iddia atlanır, cümle düzeyi sınanır.
                        MUAF.yaz("tek_tur_mesaj_duzeyi", r, alt or c.strip()[:60], c.strip())
                        continue
                    kayit = {"korpus": p.stem.split(".")[0], "duzey": duzey,
                             "sira": r["gen_meta"]["parti_sira"], "cumle": c.strip()[:150]}
                    if len(alt) >= 2:
                        hedef = kul_cumle if duzey == "cümle" else turlar
                        if not _var(alt, hedef):
                            kayit["alintilar"] = alt
                            otomatik.append(kayit)
                    else:
                        elle.append(kayit)

    CIKTI.write_text(json.dumps(
        {"tarih": "2026-09-17", "betik": "scripts/analiz/2026-09-17-yapisal-atif-kapisi.py",
         "taranan_dosya": len(yollar),
         # ⛔ Kural 7: rapor yalnız DOSYA SAYISINI yazıyordu ⇒ aynı betiğin iki
         # koşusu farklı korpuslardan gelince fark «davranış değişti» sanıldı.
         # ⇒ Girdi adları ve SHA256'ları raporun içinde.
         "girdiler": [{"dosya": str(Path(y).name),
                       "sha256_16": hashlib.sha256(
                           (Path(y) if Path(y).is_absolute() else KOK / y).read_bytes()
                       ).hexdigest()[:16]} for y in yollar],
         "sinanan_iddia": sinanan,
         "otomatik_ihlal": otomatik, "elle_okunacak": elle,
         "muafiyet_ozeti": MUAF.ozet(), "muafiyet": list(MUAF.DEFTER)}, ensure_ascii=False, indent=2),
        encoding="utf-8")

    print(f"{len(yollar)} dosya · çok turlu kayıtlarda {sinanan} «aynı cümlede» iddiası")
    print(f"⛔ OTOMATİK ihlal (≥2 alıntı, tek turda değil): {len(otomatik)}")
    for b in otomatik:
        print(f"   {b['korpus']:<12} #{b['sira']:<3} [{b['duzey']}] {b['alintilar']}")
        print(f"       «{b['cumle'][:110]}»")
    print(f"⚠️ ELLE okunacak (alıntısız iddia): {len(elle)}")
    for b in elle:
        print(f"   {b['korpus']:<12} #{b['sira']:<3} «{b['cumle'][:100]}»")
    print(f"→ {CIKTI.relative_to(KOK)}")
    return 1 if otomatik else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
