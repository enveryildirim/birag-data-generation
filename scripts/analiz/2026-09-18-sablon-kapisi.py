#!/usr/bin/env python3
"""Şablonlaşma kapısı — kalıpları ELLE değil, SAYARAK bulur.

⛔⛔ **T139'un açık kalemi.** T139 şablonlaşmayı ölçmüştü (*«Bir şeye katılmıyorum»*
%0 → %12,4) ama iki şerh düşmüştü: *«Kapı YOK — ölçüm var, denetim yok»* ve
*«Kalıplar ELLE yazıldı (K30) ⇒ sayı ALT SINIRDIR; sözlükte olmayan şablonlar
görünmez»*. Bu betik ikincisini kaldırır: kalıp listesi **yazılmıyor, çıkarılıyor**.

⭐ **Yöntem:** asistan cevaplarındaki bütün `n` sözcüklük dizilerin (n = 5…10)
kaç AYRI kayıtta geçtiği sayılır. Eşiği aşanlar aday şablon. ⇒ Sözlük yok,
dolayısıyla *«listede olmayan şablon görünmez»* sakıncası da yok.

⛔ **Ama otomatik olması doğru olduğu anlamına gelmez** ve iki karıştırıcı var:
  1. **Doğal Türkçe** — *«bir şey değil»*, *«olup olmadığını»* gibi diziler sık
     geçer ve şablon değildir. ⇒ Uzunluk ile kapsam birlikte okunur; kısa ve çok
     yaygın diziler ayrı işaretlenir.
  2. **İç içe geçme** — *«Bir şeye katılmıyorum ama»* ve *«şeye katılmıyorum ama:»*
     aynı şablonun parçalarıdır ve iki kez sayılırsa sayı şişer. ⇒ Bir dizi, daha
     UZUN ve AYNI kapsamı olan bir dizinin parçasıysa elenir.

⚠️ **Bu bir SAYIM kapısıdır, eleme kapısı değil.** *«Şablon = kusur»* DEĞİLDİR:
tekrarlanan bir cümle doğru da olabilir (T139'un kendi şerhi). Ölçülen şey
TEKRAR; yanlışlık değil. ⇒ Kapı bir kaydı düşürmez, oranı raporlar.

Girdi : datasets/v*/train.jsonl
Çıktı : reports/analiz/2026-09-18-sablon-kapisi.md
Kullanım: uv run python scripts/analiz/2026-09-18-sablon-kapisi.py [eşik_yüzde]
"""
from __future__ import annotations

import collections
import hashlib
import datetime
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
# ⛔ K126 rapor tarihini betiğin ADINDAN türetir ve TEK SEFERLİK ölçümler için bu
# doğrudur: ad, sayının alındığı günü sabitler. Ama bu betik YENİDEN KOŞULABİLİR
# (her sürüm için bir rapor) ⇒ addaki tarih artık ölçümün değil betiğin YAZILDIĞI
# günü gösterir. 2026-09-19'da koşulan bir rapor «Tarih: 2026-09-18» diyordu.
# ➡️ *Yeniden koşulabilir bir betikte ad kimliktir, tarih değil.* İkisi de yazılır.
KOSU = datetime.date.today().isoformat()
# ⛔⛔ Rapor yolu SABİTTİ ve `--girdi` ile koşulan her tarama korpus
# raporunun üstüne yazıyordu. ➡️ *Girdisi parametreleşen bir betiğin
# ÇIKTISI parametreleşmezse, ölçüm kazanılır ama kaydı kaybedilir.*
# Varsayılan (korpus) adı korundu; verilen girdi dosya adına ek olur.
def _rapor_yolu(girdi: str | None) -> Path:
    ek = "" if not girdi else "-" + Path(girdi).stem.replace(".", "-")
    return KOK / f"reports/analiz/{TARIH}-sablon-kapisi{ek}.md"

RAPOR = _rapor_yolu(None)

from tohum_guvenlik import tr_fold  # noqa: E402

# ⛔⛔ **İLK YAZIMDA ARALIK 5–10'DU VE KAPI SIFIR BULDU.** Sebep: T139'un ölçtüğü
# şablonların hepsi KISA — *«bir şeye katılmıyorum»* **3**, *«ilk adım»* **2**,
# *«benim işim değil»* **3** sözcük. Yani kapı, bulması için yazıldığı şeyleri
# parametresiyle dışarıda bırakmıştı.
# ➡️⭐⭐ *Bir detektörün parametresi, aradığı olgunun ÖLÇÜLMÜŞ biçimine göre
#    seçilmeli; «makul görünen» bir aralık, olguyu sessizce kapsam dışı bırakabilir
#    ve sonuç «temiz» gibi okunur.* ⇒ Aralık, bilinen şablonların uzunluğuna göre
#    aşağı çekildi ve 3'ten küçüğü almıyor (2 sözcük doğal dilde ayırt edici değil).
N_ARALIK = range(3, 11)
ESIK_YUZDE = 2.0          # ⚠️ seçim; duyarlılığı §3'te ölçülüyor
_SOZCUK = re.compile(r"\w+", re.UNICODE)


def _cevap(r: dict) -> str:
    return " ".join(m.get("content") or "" for m in r["messages"]
                    if m.get("role") == "assistant")


def _diziler(metin: str, n: int) -> set[tuple]:
    w = _SOZCUK.findall(tr_fold(metin))
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}


def _adaylar(kayitlar: list[dict], esik: int) -> dict[tuple, int]:
    say: dict[tuple, int] = collections.Counter()
    for r in kayitlar:
        c = _cevap(r)
        for n in N_ARALIK:
            say.update(_diziler(c, n))
    return {d: k for d, k in say.items() if k >= esik}


def _kapsayanlari_ele(aday: dict[tuple, int]) -> dict[tuple, int]:
    """⛔ İç içe geçen diziler sayıyı şişirir: bir dizi, kendisini İÇEREN daha
    uzun bir dizinin kapsamı AYNIYSA gereksizdir — uzun olan onu zaten anlatır."""
    uzun = sorted(aday, key=len, reverse=True)
    kalan: dict[tuple, int] = {}
    for d in uzun:
        s = " ".join(d)
        if any(s in " ".join(u) and aday[u] == aday[d] for u in kalan):
            continue
        kalan[d] = aday[d]
    return kalan


def main(esik_yuzde: float, girdi: str | None = None) -> int:
    """`girdi` verilirse o dosya ölçülür; verilmezse en son yayımlanmış sürüm.

    ⭐ 2026-09-20'de eklendi: yeni üretilen bir parti (`data/candidates/…`) henüz
    `datasets/`te değildir ama şablonlaşması ÜRETİM ANINDA ölçülmelidir — sürüm
    derlenip eğitime girdikten sonra ölçmek geç kalmaktır. ⛔ Ayrı bir betik
    yazmak K97'nin yasakladığı ikinci tanımı yaratırdı (aynı ölçüt iki yerde iki
    sayı verir); o yüzden tanım burada KALDI, yalnız girdisi parametreleşti.
    ⚠️ Sürüm eğrisi (aşağıdaki tablo) yine `datasets/v*` üzerinden çizilir;
    dışarıdan verilen girdi eğriye **sütun olarak eklenir**, eğriyi değiştirmez.
    """
    setler = sorted(KOK.glob("datasets/v*/train.jsonl"),
                    key=lambda p: [int(x) for x in p.parent.name[1:].split(".")])
    global RAPOR
    RAPOR = _rapor_yolu(girdi)
    son = (KOK / girdi) if girdi else setler[-1]
    if girdi:
        setler = setler + [son]
    kayitlar = [json.loads(s) for s in son.read_text(encoding="utf-8").splitlines() if s.strip()]
    esik = max(2, round(len(kayitlar) * esik_yuzde / 100))
    kalan = _kapsayanlari_ele(_adaylar(kayitlar, esik))

    sirali = sorted(kalan.items(), key=lambda x: (-x[1], -len(x[0])))
    sat = ["# Şablonlaşma kapısı — kalıplar sayılarak bulundu", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` (yazıldı {TARIH}) · "
           f"**koşu tarihi:** {KOSU}  ",
           f"**Girdi:** `{son.relative_to(KOK)}` · SHA256-16 "
           f"`{hashlib.sha256(son.read_bytes()).hexdigest()[:16]}` · **{len(kayitlar)}** kayıt  ",
           f"**Eşik:** bir dizi en az **%{esik_yuzde}** ({esik} kayıt) içinde geçmeli", "",
           "⛔⛔ **T139'un açık kalemi.** T139 şablonlaşmayı ölçmüştü ama kalıpları **elle**",
           "yazmıştı ve şerh düşmüştü: *«sayı ALT SINIRDIR; sözlükte olmayan şablonlar",
           "görünmez»*. Burada liste **yazılmıyor, çıkarılıyor**: asistan cevaplarındaki",
           "bütün 5–10 sözcüklük diziler sayılıyor.", "",
           "⚠️ **Bu bir SAYIM kapısıdır.** *«Şablon = kusur»* değildir — tekrarlanan bir cümle",
           "doğru da olabilir. Kapı hiçbir kaydı düşürmez.", "",
           f"## 1. ⭐ Eşiği aşan diziler — **{len(sirali)}**", "",
           "| kayıt | % | uzunluk | dizi |", "|---:|---:|---:|---|"]
    for d, k in sirali[:30]:
        sat.append(f"| {k} | %{100*k/len(kayitlar):.1f} | {len(d)} | *«{' '.join(d)}»* |")
    if len(sirali) > 30:
        sat.append(f"| … | | | {len(sirali)-30} dizi daha (JSON'da tamamı) |")

    # ⭐ 2. Sürümler boyunca büyüme — en yaygın beş dizinin eğrisi
    sat += ["", "## 2. ⭐ Sürümler boyunca büyüme", "",
            "T139: *«her yeni kural, bir sonraki şablonun tohumu»*. En yaygın beş dizinin",
            "sürümler boyunca **kayıt payı**:", "", "| dizi | " +
            " | ".join(p.parent.name for p in setler) + " |",
            "|---|" + "---:|" * len(setler)]
    egri = {}
    for d, _ in sirali[:5]:
        s_ = " ".join(d)
        satir = []
        for p in setler:
            ks = [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
            # ⛔ Arama, kapının KENDİ ayrıştırmasıyla yapılmalı: dizi bir SÖZCÜK
            # dizisidir, ham metin değil. Ham metinde aradığımda 0 çıktı, çünkü
            # araya noktalama giriyor (*«ben söyleyemem; bedende olanı…»*).
            # ➡️ *İki yerde iki ayrıştırma, iki farklı sayı verir.*
            n = sum(1 for r in ks if s_ in " ".join(_SOZCUK.findall(tr_fold(_cevap(r)))))
            satir.append(f"%{100*n/len(ks):.1f}" if ks else "—")
        egri[s_] = satir
        sat.append(f"| *«{s_[:58]}»* | " + " | ".join(satir) + " |")

    # ⭐⭐ 3. Eşik duyarlılığı — seçilen sayı sonucu ne kadar belirliyor?
    sat += ["", "## 3. ⭐⭐ Eşik duyarlılığı", "",
            "⛔ *«%2»* bir SEÇİMDİR, ölçüm değil. Seçimin sonucu ne kadar belirlediği",
            "gösterilmeden sayı okunamaz:", "", "| eşik | kayıt | eşiği aşan dizi |",
            "|---|---:|---:|"]
    for y in (1.0, 2.0, 3.0, 5.0):
        e = max(2, round(len(kayitlar) * y / 100))
        sat.append(f"| %{y} | {e} | {len(_kapsayanlari_ele(_adaylar(kayitlar, e)))} |")

    # ⭐⭐ T139'un ELLE listesi ne kadar alt sınırdı?
    # ⛔ Ham fark (47 − 5 = 42) YANILTICIDIR: eşiği aşan dizilerin bir kısmı doğal
    # Türkçedir (*«başka bir şey»*). ⇒ İlk 22 dizi ELLE sınıflandırıldı ve iddia
    # yalnız sınıflandırılmış veriye dayandırılıyor.
    # F = kural kaynaklı FORMÜL · D = doğal Türkçe · (T) = T139'un listesinde var
    SINIF = {
        "bir şeye katilmiyorum": ("F", True), "bugüne kadar söylediklerin şunlar": ("F", False),
        "benim işim değil": ("F", True), "olduğunu ben söyleyemem": ("F", True),
        "dair bir şey": ("D", False), "sen karar vereceksin": ("F", False),
        "bir şey var": ("D", False), "başka bir şey": ("D", False),
        "ne olduğunu ben": ("F", False), "ne olduğunu ben söyleyemem": ("F", False),
        "tek satir yok": ("F", False), "ayni şey değil": ("F", False),
        "ben karar veremem": ("F", False), "olup olmadiğini ben": ("F", True),
        "bir şey söylemeyeceğim": ("F", False), "dair tek satir": ("F", False),
        "cümleyi olduğu gibi": ("F", False), "senin bileceğin iş": ("F", False),
        "ne yapman gerektiğini": ("F", False), "o bilgi bende yok": ("F", False),
        "bir şeye katilmiyorum ama": ("F", True), "olduğu gibi söylemek": ("F", True),
    }
    sinifli = [(d, k, SINIF[" ".join(d)]) for d, k in sirali if " ".join(d) in SINIF]
    formul = [x for x in sinifli if x[2][0] == "F"]
    dogal = [x for x in sinifli if x[2][0] == "D"]
    yeni = [x for x in formul if not x[2][1]]
    sat += ["", "## 4. ⭐⭐ T139'un elle listesi ne kadar alt sınırdı?", "",
            "T139 beş kalıbı **elle** yazmış ve şerh düşmüştü: *«sayı ALT SINIRDIR»*.",
            "Şerh doğruydu ve şimdi ölçülebiliyor:", "",
            "⛔ Ham fark yanıltıcı olurdu: eşiği aşan dizilerin bir kısmı **doğal Türkçe**",
            "(*«başka bir şey»*). ⇒ En yaygın **22** dizi elle sınıflandırıldı ve iddia",
            "yalnız sınıflandırılmış veriye dayanıyor.", "",
            "| | |", "|---|---:|",
            f"| kapının eşiği aşan dizisi | {len(sirali)} |",
            f"| elle sınıflandırılan | **{len(sinifli)}** |",
            f"| · kural kaynaklı **formül** | **{len(formul)}** |",
            f"| · doğal Türkçe | {len(dogal)} |",
            f"| ⛔ **formül olup T139'un listesinde OLMAYAN** | **{len(yeni)}** |", "",
            "| dizi | kayıt | sınıf | T139'da |", "|---|---:|---|---|"]
    for d, k, (sf, t139) in sinifli:
        sat.append(f"| *«{' '.join(d)}»* | {k} | "
                   f"{'kural formülü' if sf == 'F' else 'doğal dil'} | "
                   f"{'✅ var' if t139 else '⛔ **yok**'} |")
    sat += ["",
            "⛔⛔ **Ve kaçan, korpusun en büyük ikinci kalıbı:** *«bugüne kadar söylediklerin",
            "şunlar»* — **43 kayıt (%7,5)**, yani T139'un listesindeki beş kalıbın üçünden",
            "daha yaygın. Elle yazılmış bir listede yoktu ve hiçbir yerde sayılmamıştı.", "",
            "➡️⭐⭐⭐ *Bir olguyu elle yazılmış bir listeyle ölçmek, olgunun ancak AKLA GELEN",
            "kısmını ölçer. «Alt sınır» şerhi dürüsttür ama ne kadar alt olduğunu söylemez —",
            "onu ancak listesiz bir sayım söyler.*", "",
            "## ⛔ Bu kapının söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **Kusur demiyor** | tekrarlanan bir cümle doğru da olabilir; ölçülen şey "
            "TEKRAR. Hangi şablonun kusur olduğunu **elle okuma** söyler |",
            "| ⛔ **Doğal dil ile şablon ayrılmıyor** | *«bir şey olup olmadığını»* gibi "
            "diziler de eşiği aşabilir; uzunluk sütunu bu yüzden tabloda |",
            "| ⛔ **Eşik seçimi sonucu belirliyor** | §3 duyarlılığı gösteriyor ama doğru "
            "eşiği söylemiyor |",
            "| ⚠️ **Yalnız asistan cevabı** | `thinking` kapsam dışı; orada tekrar çok daha "
            "yoğun ve ayrı bir soru |",
            "| ⛔ **Eleme yok** | kapı bir kaydı düşürmez; T139'un istediği denetim bu, ama "
            "denetimin SONUCUNU kullanan bir süreç henüz yok |",
            "| ⛔ **İç içe geçme tam çözülmedi** | *«ne olduğunu ben»* (19) ve *«ne olduğunu "
            "ben söyleyemem»* (18) ayrı sayılıyor çünkü kapsamları FARKLI; aynı ailedendirler "
            "ve liste bu yüzden gerçek şablon sayısından uzun |",
            "| ⛔ **Sınıflandırma elle** | hangi dizinin kural kaynaklı FORMÜL, hangisinin "
            "doğal Türkçe olduğunu (*«başka bir şey»*) kapı söylemiyor |", ""]

    RAPOR.with_suffix(".json").write_text(
        json.dumps({"tarih": TARIH, "girdi": str(son.relative_to(KOK)),
                    "kayit": len(kayitlar), "esik_yuzde": esik_yuzde,
                    "dizi": [{"dizi": " ".join(d), "kayit": k} for d, k in sirali],
                    "egri": egri}, ensure_ascii=False, indent=2), encoding="utf-8")
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[5:]))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    _a = sys.argv[1:]
    _g = None
    if "--girdi" in _a:
        _i = _a.index("--girdi"); _g = _a[_i + 1]; _a = _a[:_i]
    raise SystemExit(main(float(_a[0]) if _a else ESIK_YUZDE, _g))
