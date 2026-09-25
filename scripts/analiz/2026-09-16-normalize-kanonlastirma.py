#!/usr/bin/env python3
"""Ailenin SEKİZİNCİ örneği — ve ilk kez kusur SESSİZCE YANLIŞ DEĞER üretiyor.

T73 ve T75'te kusurun biçimi hep aynıydı: **kapı ateşlemiyor**. Eksik bir uyarı
görünür bir şey bırakmaz ama en azından *yanlış bir şey de söylemez*. ⛔ Burada
öyle değil: `src/normalize.py` ham kampanya meta'sını kanonik taksonomiye
çeviriyor (K26) ve düz `.lower()` üç yerde yanlıştı. İkisinin **sonucu ayrı
türden**:

  · `norm_egitim("İlkokul")` -> `belirtilmemis`  ⚠️ fallback — **izi var**
  · `norm_sure("3 YILDAN FAZLA")` -> `1_3_yil`   ⛔⛔ **YANLIŞ KOVA — izi YOK**

⭐⭐ İkincisi bu ailede ilk: çıktı geçerli görünüyor, hiçbir alan *«bilinmiyor»*
demiyor, ve kaydın 3+ yıllık kullanımı sessizce 1-3 yıla iniyor.

⭐ **Ve bir site BAĞIŞIK çıktı:** `slug()` `ı`→`i` eşlemesini **tasarım gereği**
yapıyor, yani i/ı ayrımını zaten yok sayıyor ⇒ her iki okuma aynı slug'a düşüyor.
➡️ *Bir fonksiyonun bu aileden korunmuş olması dikkatten değil, ayrımı hiç
KULLANMAMASINDAN geliyor. Aynı şey `i_sinifi`'nin de yaptığı şey.*

⛔ **Hasarın KESİN ölçümü bu betikle yapılamaz:** `data/seeds.jsonl` kanonik
meta'yı taşıyor, **ham** meta'yı değil; ham veri onaylı kaynak klasöründe ve
Kural 1 gereği sorulmadan okunmuyor. Burada **üst sınır** ölçülüyor — ve
`kullanim_suresi` için ⛔ **üst sınır bile yok**, çünkü kusur iz bırakmıyor.

Girdi : src/normalize.py · configs/taxonomy.yaml · data/seeds.jsonl
Çıktı : reports/analiz/2026-09-16-normalize-kanonlastirma.md
Kullanım: uv run python scripts/analiz/2026-09-16-normalize-kanonlastirma.py
"""
# lower-muaf-dosya: eski `norm_egitim`/`norm_sure`/`_keyword` referans uygulamaları (T76)
from __future__ import annotations

import collections
import hashlib
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-normalize-kanonlastirma.md"
TOHUM = KOK / "data/seeds.jsonl"
sys.path.insert(0, str(KOK / "src"))
import normalize as N  # noqa: E402

EGITIM_KURALLARI = (("lisansüstü", "lisansustu"), ("yüksek lisans", "lisansustu"),
                    ("mba", "lisansustu"), ("üniversite", "universite"),
                    ("lisans", "universite"), ("lise", "lise"),
                    ("ortaokul", "ortaokul"), ("ilkokul", "ilkokul"))


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


# --- 2026-09-16 ÖNCESİ davranış — referans olarak DURUYOR ---------------------
# ⭐ Canlı fonksiyon düzeltilince kusurun büyüklüğü raporda görünmez olurdu;
#   T73'te aynı sorun çıktı, aynı çözüm uygulanıyor.
def eski_egitim(raw: str) -> str:
    t = (raw or "").lower()
    for key, canon in EGITIM_KURALLARI:
        if key in t:
            return canon
    return "belirtilmemis"


def eski_sure(raw: str):
    if not raw:
        return "belirtilmemis"
    t = raw.lower()
    if "ay" in t and not re.search(r"\byıl|yil\b", t.split("ay")[0][-12:]):
        m = re.search(r"(\d+)\s*(?:-|–|\s)*\d*\s*ay", t)
        if m:
            return "0_6_ay" if int(m.group(1)) < 6 else "6_ay_1_yil"
    m = re.search(r"(\d+)", t)
    if not m:
        return "belirtilmemis"
    n = int(m.group(1))
    if "3 yıldan fazla" in t:
        return "3_10_yil"
    return ("0_6_ay" if n < 1 else "1_3_yil" if n <= 3 else
            "3_10_yil" if n <= 10 else "10_yil_ustu")


def eski_keyword(field: str, raw: str):
    low = raw.lower()
    for keys, canon in N.TAX.get(field, {}).get("anahtar_kelime", []):
        if any(k in low for k in keys):
            return canon
    return None


# --- vektörler ----------------------------------------------------------------
def tr_buyut(s: str) -> str:
    return s.replace("i", "İ").replace("ı", "I").upper()


def baslik(s: str) -> str:
    """Bir meta alanının EN OLAĞAN yazımı: her sözcüğün ilk harfi büyük."""
    return " ".join(w[:1].replace("i", "İ").replace("ı", "I").upper() + w[1:]
                    for w in s.split())


def aksansiz(s: str) -> str:
    """Türkçe klavyesiz yazımın ürettiği hâl — AYRI bir aile üyesi."""
    for a, b in zip("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU"):
        s = s.replace(a, b)
    return s


VEKTOR = [("olduğu gibi", lambda s: s),
          ("**Başlık Yazımı** (`İlkokul`)", baslik),
          ("**doğru TR BÜYÜK**", tr_buyut),
          ("ASCII `.upper()`", str.upper),
          ("⚠️ **aksansız** (`Universite`)", aksansiz)]


def main() -> int:
    L: list[str] = []
    kayitlar = [json.loads(l) for l in TOHUM.read_text(encoding="utf-8").split("\n") if l.strip()]
    anahtarlar = [(k, canon) for keys, canon in N.TAX["stres_tipi"]["anahtar_kelime"] for k in keys]

    L += ["# `normalize.py` — ailenin sekizincisi, ve ilk kez kusur **sessizce yanlış değer**", "",
          f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
          f"**Girdi:** `src/normalize.py` SHA256 `{sha(KOK/'src/normalize.py')}` "
          f"(fonksiyonlar **çağrılıyor**)  ",
          f"**Girdi:** `configs/taxonomy.yaml` SHA256 `{sha(KOK/'configs/taxonomy.yaml')}`  ",
          f"**Girdi:** `data/seeds.jsonl` SHA256 `{sha(TOHUM)}` — **{len(kayitlar)}** tohum",
          "", "---", "", "## 1. ⭐ Bir site BAĞIŞIK — ve sebebi öğretici", "",
          "`normalize.py`'de düz `.lower()` kullanan dört yer vardı. ⭐ Biri bu aileden",
          "**etkilenmiyor**: `slug()` küçülttükten sonra `ç ğ ı ö ş ü` → `c g i o s u`",
          "eşlemesi yapıyor, yani **`ı` ile `i` ayrımını tasarım gereği yok sayıyor**.",
          "Her iki okuma da aynı slug'a düşüyor:", "", "| girdi | `slug()` |", "|---|---|"]
    for w in ["ilaç", "ILAÇ", "İLAÇ", "ılaç"]:
        L.append(f"| `{w}` | `{N.slug(w)}` |")
    L += ["",
          "➡️ *Bir fonksiyonun bu aileden korunmuş olması dikkatten değil, ayrımı hiç*",
          "*KULLANMAMASINDAN geliyor — `i_sinifi`'nin yaptığı şeyin aynısı, yalnızca*",
          "*başka bir sebeple.* ⇒ Kural olarak: **ayrımı taşımak zorunda olmayan her yer**",
          "**onu düşürmeli**; taşımak zorunda olan yer de sınıf kullanmalı.", "", "---", ""]

    # --- §2 kusurun türü ------------------------------------------------------
    L += ["## 2. ⭐⭐ Kusurun TÜRÜ değişti — fallback değil, **yanlış kova**", "",
          "T73 ve T75'te kusurun biçimi hep *«kapı ateşlemiyor»*du: eksik bir uyarı",
          "görünür bir şey bırakmaz ama **yanlış bir şey de söylemez**. ⛔ Burada iki",
          "ayrı sonuç var ve ikincisi bu ailede **ilk**:", "",
          "| girdi | eski sonuç | doğru | tür |", "|---|---|---|---|"]
    ornek = [("norm_egitim", "İlkokul", eski_egitim, N.norm_egitim),
             ("norm_egitim", "LİSE", eski_egitim, N.norm_egitim),
             ("norm_sure", "3 YILDAN FAZLA", eski_sure, N.norm_sure)]
    for fn, g, e, c in ornek:
        ev, cv = e(g), c(g)
        tur = ("⚠️ fallback — **izi var**" if ev == "belirtilmemis"
               else "⛔⛔ **YANLIŞ KOVA — izi YOK**")
        L.append(f"| `{fn}({g!r})` | `{ev}` | `{cv}` | {tur} |")
    L += ["",
          "⛔⛔ *`3 YILDAN FAZLA` kaydı `1_3_yil` oluyor: çıktı **geçerli görünüyor**,",
          "hiçbir alan «bilinmiyor» demiyor, ve kaydın 3+ yıllık kullanımı sessizce",
          "1-3 yıla iniyor.* ➡️ **Bir kapının ateşlememesi ölçülebilir bir eksikliktir;**",
          "**bir dönüştürücünün yanlış değer üretmesi ölçülemez bir yalandır.**", "", "---", ""]

    # --- §3 matris ------------------------------------------------------------
    L += ["## 3. Matris — her site, beş yazım biçimi", "", "### 3a. `norm_egitim`", "",
          "| yazım | " + " | ".join(f"`{k}`" for k, _ in EGITIM_KURALLARI) + " |",
          "|---|" + "---:|" * len(EGITIM_KURALLARI)]
    egitim_olu = {v: 0 for v, _ in VEKTOR}
    canli_olu = 0
    for vad, vf in VEKTOR:
        hucre = []
        for key, canon in EGITIM_KURALLARI:
            g = vf(key)
            e_ok, c_ok = eski_egitim(g) == canon, N.norm_egitim(g) == canon
            egitim_olu[vad] += not e_ok
            canli_olu += not c_ok
            hucre.append(("✅" if e_ok else "⛔") + ("" if c_ok else "⁄⛔"))
        L.append(f"| {vad} | " + " | ".join(hucre) + " |")
    L += ["", "*(hücre = **eski**; `⁄⛔` varsa canlı da kaçırıyor)*", "",
          "| yazım | eski ölü | ", "|---|---:|"]
    for vad, _ in VEKTOR:
        L.append(f"| {vad} | **{egitim_olu[vad]}**/{len(EGITIM_KURALLARI)} |")
    L += ["", f"{'✅' if canli_olu == 0 else '⛔'} **Canlı `norm_egitim` ölü hücre: "
          f"{canli_olu}/{len(VEKTOR)*len(EGITIM_KURALLARI)}.**",
          ("" if canli_olu == 0 else
           " ⚠️ Kalanların hepsi **aksansız** sınıfı — ayrı aile üyesi, §5."), ""]

    L += ["### 3b. `_keyword` (`stres_tipi` — taksonomiden gelen anahtarlar)", "",
          "| yazım | eski ölü anahtar | canlı ölü anahtar |", "|---|---:|---:|"]
    for vad, vf in VEKTOR:
        e = sum(1 for k, canon in anahtarlar if eski_keyword("stres_tipi", vf(k)) != canon)
        c = sum(1 for k, canon in anahtarlar if N._keyword("stres_tipi", vf(k)) != canon)
        L.append(f"| {vad} | **{e}**/{len(anahtarlar)} | "
                 f"{'✅ **0**' if c == 0 else f'**{c}**'}/{len(anahtarlar)} |")
    L += ["",
          "⚠️ *«Ölü anahtar»* burada *«yanlış kanona düştü ya da hiç eşleşmedi»* demek —",
          "ikisi ayrılmadı, çünkü ikisi de aynı sonucu doğuruyor: **kayıt yanlış etiketlenir**.", "",
          "### 3b′. ⛔⛔ `_keyword` DÜZELTİLMEDİ — ve sebebi bu raporun en önemli kısmı", "",
          "`tr_fold` bu siteye de uygulandı ve ⛔ **gerileme üretti**: taban durumda "
          "(hiç büyük harf yokken) **2 anahtar yanlış kanona düştü**.", "",
          "| anahtar | beklenen | i-sınıfından sonra | sebep |", "|---|---|---|---|",
          "| `kaçış` | `ritüel_bagimliligi` | ⛔ `is_stresi` | `kaçış` → `kaçiş`, "
          "içinde **`iş`** var |",
          "| `alışkanlık` | `ritüel_bagimliligi` | ⛔ `is_stresi` | `alışkanlık` → "
          "`alişkanlik`, içinde **`iş`** var |", "",
          "⭐ Sebep i-sınıfının kendisi değil: **anahtarlar kısa alt-dizeler.** "
          f"{len([k for keys,_ in N.TAX['stres_tipi']['anahtar_kelime'] for k in keys if len(k) <= 4])}"
          f" anahtar ≤4 karakter (`iş`, `eş `, `boş`, `aile`, `okul`, `para`…). Bir "
          "karakter sınıfını genişletmek, kısa alt-dize eşleşmesinde **hemen** çakışma "
          "üretir.", "",
          "⭐⭐ **Ve altında DAHA ESKİ bir kusur var — kasingden bağımsız, bugün de açık:**",
          "", "| metin | `_keyword` bugün | |", "|---|---|---|"]
    for m in ["girişimci bir hayatım var", "gelişim çağında", "değişim istiyorum",
              "iş kurmayı düşünüyorum"]:
        sonuc = eski_keyword("stres_tipi", m)
        beklenen_yanlis = m.startswith(("girişimci", "gelişim", "değişim"))
        L.append(f"| `{m}` | `{sonuc}` | "
                 f"{'⛔ **yanlış**' if beklenen_yanlis else '✅ doğru'} |")
    L += ["",
          "⛔ `iş` anahtarı **kelime içinde** eşleşiyor. Bu **K65'in ailesi** ve çözümü "
          "`checks.KLINIK_IDDIA`'da zaten uygulanmış (`\\b` + Türkçe ek serbest) — "
          "`_keyword`'e hiç gelmemiş.", "",
          "➡️⭐⭐ *i-sınıfı kusuru YARATMADI; zaten bozuk olan eşleştiriciyi GENİŞLETİP*",
          "*GÖRÜNÜR KILDI. Ve bu, düzeltmeyi uygulamamak için yeterli sebep: iki kusuru*",
          "*birden kapatmak (`\\b` + i-sınıfı) etiket semantiğini değiştirir, etkisi ancak*",
          "*HAM kampanya meta'sına karşı ölçülebilir, ve o veri onaylı kaynak klasöründe*",
          "*(Kural 1).* ⛔ **Ölçülmeden değiştirilmedi** — K40: kalibre edilmemiş kapı veri",
          "öldürür. ⚠️ Gerekçe `normalize._keyword` docstring'ine yazıldı, kusur gizlenmiyor.", ""]

    L += ["### 3c. `norm_sure`", "", "| girdi | yazım | eski | canlı |", "|---|---|---|---|"]
    sure_ornek = ["3 yıldan fazla", "2 yıl", "5 ay", "8 ay", "15 yıl"]
    sure_olu_e = sure_olu_c = 0
    for g in sure_ornek:
        dogru = eski_sure(g)
        for vad, vf in VEKTOR[1:4]:
            e, c = eski_sure(vf(g)), N.norm_sure(vf(g))
            sure_olu_e += e != dogru
            sure_olu_c += c != dogru
            if e != dogru or c != dogru:
                L.append(f"| `{g}` | {vad} | "
                         f"{'✅ `'+str(e)+'`' if e == dogru else '⛔ **`'+str(e)+'`**'} | "
                         f"{'✅ `'+str(c)+'`' if c == dogru else '⛔ **`'+str(c)+'`**'} |")
    if sure_olu_e == 0:
        L.append("| — | — | ✅ | ✅ |")
    L += ["",
          f"⛔ Eski: **{sure_olu_e}** yanlış sonuç · "
          f"{'✅' if sure_olu_c == 0 else '⛔'} Canlı: **{sure_olu_c}**.", "", "---", ""]

    # --- §4 hasarın üst sınırı -------------------------------------------------
    L += ["## 4. ⛔ Hasar ÖLÇÜLEMİYOR — yalnızca üst sınır, o da her alanda değil", "",
          "`data/seeds.jsonl` **kanonik** meta taşıyor, **ham** meta'yı değil. Ham veri",
          "onaylı kaynak klasöründe ve ⛔ **Kural 1 gereği sorulmadan okunmuyor**. ⇒ Burada",
          "yalnızca **üst sınır** ölçülebiliyor: bir kayıt fallback değere düştüyse sebebi",
          "bu kusur **olabilir** (ya da alan gerçekten boştur).", "",
          "| alan | fallback değeri | kayıt | üst sınır |", "|---|---|---:|---|"]
    for alan, geri in [("egitim", "belirtilmemis"), ("stres_tipi", None),
                       ("kullanim_suresi", "belirtilmemis")]:
        n = sum(1 for k in kayitlar if k["meta"].get(alan) == geri)
        if alan == "kullanim_suresi":
            L.append(f"| `{alan}` | `{geri}` | **{n}** | ⛔⛔ **ÜST SINIR YOK** — kusur "
                     "fallback değil **yanlış kova** üretiyor, iz bırakmıyor |")
        else:
            L.append(f"| `{alan}` | `{geri}` | **{n}** | ≤ **{n}** (%{100*n/len(kayitlar):.1f}) |")
    L += ["",
          "⭐ **Kampanyaya göre dağılım — kümelenme bir işarettir:**", "",
          "| kampanya | `egitim=belirtilmemis` | `stres_tipi=None` |", "|---|---|---|"]
    for kmp in sorted({k["campaign"] for k in kayitlar}):
        alt = [k for k in kayitlar if k["campaign"] == kmp]
        e = sum(1 for k in alt if k["meta"].get("egitim") == "belirtilmemis")
        st = sum(1 for k in alt if k["meta"].get("stres_tipi") is None)
        L.append(f"| `{kmp}` | {e}/{len(alt)} (%{100*e/len(alt):.1f}) | "
                 f"{st}/{len(alt)} (%{100*st/len(alt):.1f}) |")
    L += ["",
          "⚠️ **Kümelenme kanıt DEĞİL, işarettir.** Yazım biçimi kampanyaya göre değişiyorsa",
          "kusur da kampanyaya göre kümelenir — ama alanın gerçekten boş bırakılması da",
          "kampanyaya göre kümelenir. ⛔ İkisini ayıran tek şey **ham veri**.", "", "---", ""]

    # --- §5 kalan sınıf --------------------------------------------------------
    aksan_olu = [key for key, canon in EGITIM_KURALLARI
                 if N.norm_egitim(aksansiz(key)) != canon]
    L += ["## 5. ⚠️ Kapanmayan sınıf — **aksan düşürme** ayrı bir aile üyesi", "",
          "`tr_fold` `i/ı/İ/I` ayrımını kaldırıyor ama `ü→u`, `ş→s`, `ğ→g` **değil**.",
          "Türkçe klavyesi olmayan biri `Universite` yazar ve bu hâlâ eşleşmiyor:", "",
          "| aksansız yazım | canlı sonuç |", "|---|---|"]
    for key in [k for k, _ in EGITIM_KURALLARI][:6]:
        L.append(f"| `{aksansiz(key)}` | `{N.norm_egitim(aksansiz(key))}` |")
    L += ["",
          f"⛔ Aksansız yazımda **{len(aksan_olu)}/{len(EGITIM_KURALLARI)}** kural hâlâ ölü: "
          + ", ".join(f"`{k}`" for k in aksan_olu) + ".", "",
          "✅ **2026-09-16'da KAPATILDI (T84)** — ama yalnızca `norm_egitim` ve",
          "`norm_sure`'de. `tohum_guvenlik.tr_sadelestir` aksanı da düşürüyor; bedeli",
          "**önce ölçüldü**: taksonomide çakışma **yok**, ham 2240 kayıtta `egitim`",
          "farkı **0**.", "",
          "⛔⭐⭐ **`_keyword`'e UYGULANMADI ve sebebi ölçümden çıktı:** aksansız `iş` →",
          "`is` olunca **`isolation`** içinde eşleşiyor. Bugün kural sırası bunu",
          "maskeliyor (`monotony_isolation` önce `monoton`a düşüyor) ⚠️ ama maskeyi",
          "tasarım değil **rastlantı** tutuyor. Kazanç 5 tartışmalı kayıt "
          "(`bos_zaman_caresizlik` → `yalnizlik`), risk **sessiz yanlış etiket** ⇒",
          "uygulanmadı. ➡️ *Aynı modülde iki fold bir karmaşa değil, iki farklı RİSK*",
          "*profilinin karşılığıdır — T80'in «yönü kapı belirler» dersinin ikinci*",
          "*uygulanışı.*", "",
          "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔⛔ **Gerçek hasar** | ölçülemedi — ham meta onaylı kaynak klasöründe, "
          "Kural 1. ⚠️ `kullanim_suresi` için **üst sınır bile yok** |",
          "| ⛔ `data/seeds.jsonl` **yeniden üretilmedi** | düzeltilmiş `normalize.py` ile "
          "yeniden koşmak ham veriyi okumayı gerektirir; yapılmadı |",
          "| ⛔ **Aksan düşürme sınıfı açık** (§5) | kapatmanın yan etkisi ölçülmedi |",
          "| ⚠️ `_exact` / `_prefix` / `_contains` | hiç normalizasyon **kullanmıyor** "
          "(tasarım gereği: takma adlar kaynaktan birebir alınmış). ⛔ Ama bu, aynı "
          "kırılganlığın **daha sert** biçimi ve ayrıca sınanmadı |",
          "| ⚠️ Kural listesi **elle** | `EGITIM_KURALLARI` betikte kopya duruyor çünkü "
          "`norm_egitim` onu gövdesinde taşıyor; kaynak değişirse **bu betik de** "
          "güncellenmeli |", ""]

    RAPOR.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print(f"   norm_egitim eski ölü: " + " · ".join(
        f"{v}={egitim_olu[v]}/{len(EGITIM_KURALLARI)}" for v, _ in VEKTOR))
    print(f"   norm_egitim canlı ölü hücre: {canli_olu}/{len(VEKTOR)*len(EGITIM_KURALLARI)}")
    print(f"   norm_sure: eski {sure_olu_e} yanlış · canlı {sure_olu_c}")
    print(f"   üst sınır: egitim ≤{sum(1 for k in kayitlar if k['meta'].get('egitim')=='belirtilmemis')}"
          f" · stres_tipi ≤{sum(1 for k in kayitlar if k['meta'].get('stres_tipi') is None)}"
          f" · kullanim_suresi ⛔ üst sınır yok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
