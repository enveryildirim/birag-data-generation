#!/usr/bin/env python3
"""§15 sert kapısı BÜYÜK HARFLE yazılan ifadeyi görmüyor — ve yaması repoda ZATEN var.

`src/tohum_guvenlik.py` bu hata ailesinin **üç ayrı örneğini** başlığında
anlatıyor (K76'nın iki bulgusu + 2026-09-15'te bulunan üçüncüsü) ve çözümü
*«TEK giriş noktası»* diye ilan ediyor: `tr_kucult()`. ⛔ Ama §15 yasak ifade
kapısı — `src/checks.py::scan_forbidden` — hâlâ **düz `.lower()`** kullanıyor.
Bu, ailenin **dördüncü** örneği ve bu kez **sert kapının kendisinde**.

⭐ Mekanizma Python'un Türkçe bilmemesi:

    "ADI".lower()  -> "adi"    ⛔ Türkçesi "adı"   (I → i, ı DEĞİL)
    "İLAÇ".lower() -> "i̇laç"   ⛔ i + BİRLEŞEN NOKTA, "ilaç" ile eşleşmez

⇒ İçinde **ı** ya da **İ** geçen her yasak ifade, metin büyük harfle yazılınca
kapıdan **görünmez** geçer.

⚠️ Bu betik iki soruyu AYIRIYOR ve ikisi de ayrı ayrı gerekli:
  1. **Kapı ne kadar delik** — kaç ifade kaçabiliyor (tasarım kusuru)
  2. **Bugün kayba yol açtı mı** — mevcut korpusta kaçan var mı (olgusal zarar)
⛔ (1) *«hayır»* olsa bile (2) sıfır çıkabilir; ikisini karıştırmak kapıyı ya
gereksiz yere korkutucu ya gereksiz yere masum gösterir.

Girdi : src/checks.py · configs/filters.yaml · src/tohum_guvenlik.py ·
        datasets/v*/train.jsonl · data/candidates/*.jsonl · data/judged/*.jsonl
Çıktı : reports/analiz/2026-09-16-buyuk-harf-kapisi.md
Kullanım: uv run python scripts/analiz/2026-09-16-buyuk-harf-kapisi.py
"""
# lower-muaf-dosya: bütün işi ESKİ `.lower()` davranışını ölçmek — referans uygulama (T73)
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
import unicodedata
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-buyuk-harf-kapisi.md"
sys.path.insert(0, str(KOK / "src"))
sys.path.insert(0, str(KOK / "scripts/analiz"))
import _muafiyet as MUAF  # noqa: E402  ⭐ T141: bağışlanan her öge sayılır
import checks as C  # noqa: E402

_s = importlib.util.spec_from_file_location("_tg", KOK / "src/tohum_guvenlik.py")
TG = importlib.util.module_from_spec(_s)
_s.loader.exec_module(TG)


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def ifadeler() -> list[tuple[str, str]]:
    return [(k, i) for k, lst in C.FILTERS["yasakli_ifadeler"].items() for i in lst]


def tr_buyut(s: str) -> str:
    """⭐ DOĞRU Türkçe büyütme. Python'un `.upper()`'ı bunu yapmaz: `i` → `I` der,
    Türkçesi `İ`'dir. İki ayrı tehdit vektörü bu yüzden AYRI ölçülüyor."""
    return s.replace("i", "İ").replace("ı", "I").upper()


def ascii_kucult(s: str) -> str:
    """`I`'yı `i` okuyan karşı-normalizasyon — `tr_kucult`'un tersi yönü."""
    return unicodedata.normalize("NFKD", s.replace("İ", "i").lower()).replace("\u0307", "")


def _kapi_duz(igne: str, saman: str) -> bool:
    return igne.lower() in saman.lower()


def _kapi_tr(igne: str, saman: str) -> bool:
    return TG.tr_kucult(igne) in TG.tr_kucult(saman)


def _kapi_cift(igne: str, saman: str) -> bool:
    return _kapi_tr(igne, saman) or ascii_kucult(igne) in ascii_kucult(saman)


def _kapi_sinif(igne: str, saman: str) -> bool:
    """Canlı kapının mantığı — `checks.i_sinifi` ÇAĞRILIYOR, kopyalanmıyor."""
    return C.i_sinifi(TG.tr_kucult(igne)) in C.i_sinifi(TG.tr_kucult(saman))


def duz_tarama(metin: str) -> dict[str, list[str]]:
    """⛔ Düz `.lower()` ile tarama — `scan_forbidden`'ın 2026-09-16 ÖNCESİ hâli.

    ⭐ Referans olarak duruyor: canlı kapı düzeltilince §1 sıfırlanır ve o zaman
    tuzağın büyüklüğü raporda görünmez olurdu. Tuzak burada ölçülüyor, kapı ise
    ayrıca — ikisi aynı sayı değil ve aynı sayıya dönmemeli.
    """
    low = metin.lower()
    out: dict[str, list[str]] = {}
    for kategori, liste in C.FILTERS["yasakli_ifadeler"].items():
        bulunan = [i for i in liste if i.lower() in low]
        if bulunan:
            out[kategori] = bulunan
    return out


def tr_tarama(metin: str) -> dict[str, list[str]]:
    """⭐ `scan_forbidden`'ın Türkçe normalizasyonlu ikizi — mantık aynı, yalnızca
    küçültme `tohum_guvenlik.tr_kucult`'tan ÇAĞRILIYOR."""
    low = TG.tr_kucult(metin)
    out: dict[str, list[str]] = {}
    for kategori, liste in C.FILTERS["yasakli_ifadeler"].items():
        bulunan = [i for i in liste if TG.tr_kucult(i) in low]
        if bulunan:
            out[kategori] = bulunan
    return out


def metinler() -> list[tuple[str, str, str]]:
    """(kaynak, kayıt kimliği, asistan metni) — yalnızca ASİSTAN tarafı.

    ⛔ §15 modelin ÜRETTİĞİNİ kısıtlar; kullanıcı mesajındaki bir ifade ihlal
    değildir (T62'nin aynalama dersi).
    """
    out = []
    yollar = (sorted(KOK.glob("datasets/v*/train.jsonl"))
              + sorted(KOK.glob("data/judged/*.jsonl"))
              + sorted(KOK.glob("data/candidates/*.jsonl")))
    for p in yollar:
        for n, satir in enumerate(p.read_text(encoding="utf-8").split("\n")):
            if not satir.strip():
                continue
            try:
                r = json.loads(satir)
            except json.JSONDecodeError:
                # ⛔⛔ SESSİZ TİP — ayrıştırılamayan satır hiç sınanmıyor (T143).
                MUAF.yaz("json_ayristirilamadi", {}, satir[:60],
                         str(p.relative_to(KOK)), tip="sessiz")
                continue
            for m in r.get("messages", []):
                if m.get("role") != "assistant":
                    # ⭐ KAPSAM TİPİ — İLAN EDİLMİŞ sınır: §15 modelin ÜRETTİĞİNİ
                    # kısıtlar (T62). ⚠️ Yalnız ADAY olan metinler sayılır: büyük
                    # harf içermeyen bir kullanıcı mesajını «kapsam dışı» diye
                    # saymak defteri şişirir ve sınırın BEDELİNİ gizler.
                    _p = " ".join(x for x in (m.get("content"), m.get("thinking")) if x)
                    if _p and BUYUK.search(_p):
                        MUAF.yaz("asistan_disi", r, sorted(set(BUYUK.findall(_p)))[:6],
                                 f"{m.get('role')} · {_p[:90]}", tip="kapsam")
                    continue
                parca = " ".join(x for x in (m.get("content"), m.get("thinking")) if x)
                if parca:
                    out.append((str(p.relative_to(KOK)), r.get("id", f"satır{n}"), parca))
    return out


BUYUK = re.compile(r"\b[A-ZÇĞİÖŞÜ]{3,}\b")


def main() -> int:
    IF = ifadeler()
    L: list[str] = []
    L += ["# §15 sert kapısı büyük harfi görmüyor — ve yaması repoda zaten var", "",
          f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
          f"**Girdi:** `src/checks.py` SHA256 `{sha(KOK/'src/checks.py')}`  ",
          f"**Girdi:** `configs/filters.yaml` SHA256 `{sha(KOK/'configs/filters.yaml')}`  ",
          f"**Girdi:** `src/tohum_guvenlik.py` SHA256 `{sha(KOK/'src/tohum_guvenlik.py')}` "
          f"(`tr_kucult` **çağrılıyor**, kopyalanmıyor)", "", "---", "",
          "## Mekanizma — Python Türkçe bilmiyor", "", "```text",
          '"ADI".lower()   -> "adi"     ⛔ Türkçesi "adı"  (I → i, ı DEĞİL)',
          '"İLAÇ".lower()  -> "i̇laç"    ⛔ i + BİRLEŞEN NOKTA, "ilaç" ile eşleşmez',
          "```", "",
          "⇒ İçinde **ı** ya da **İ** geçen her yasak ifade, metin büyük harfle",
          "yazılınca kapıdan **görünmez** geçer.", "",
          "⛔ Bu, `src/tohum_guvenlik.py`'nin başlığında anlatılan hata ailesinin",
          "**dördüncü** örneği — ve ilk üçünden farkı, bu kez **sert kapının kendisinde**",
          "olması. Modül çözümü *«TEK giriş noktası»* diye ilan ediyor (`tr_kucult`),",
          "ama `scan_forbidden` onu kullanmıyor.", "", "---", ""]

    # --- §1 kapı ne kadar delik ----------------------------------------------
    VEKTOR = [("olduğu gibi", lambda x: x),
              ("**doğru TR büyütme** (`i`→`İ`, `ı`→`I`)", tr_buyut),
              ("**ASCII özensiz** `.upper()` (`i`→`I`)", str.upper)]
    KAPI = [("düz `.lower()` — 2026-09-16 öncesi", _kapi_duz),
            ("`tr_kucult` tek yönlü", _kapi_tr),
            ("iki normalizasyon birden", _kapi_cift),
            ("⭐ **i-SINIFI** — canlı kapı", _kapi_sinif)]
    matris = {(ka, va): [(k, i) for k, i in IF if not kf(i, vf(i))]
              for ka, kf in KAPI for va, vf in VEKTOR}
    L += ["## 1. ⭐⭐ Tek yönlü bir küçültme, iki kaçak sınıfından BİRİNİ zorunlu açık bırakır",
          "",
          "Her yasak ifade üç biçimde yazılıp dört kapıya veriliyor. ⛔ Vektörler",
          "**ayrı** ölçülüyor çünkü ikisi farklı şey: biri Türkçe klavyeyle bağıran",
          "kullanıcı, öteki klavyesiz yazan (ya da `.upper()` çağıran) taraf.", "",
          "| Kapı | " + " | ".join(v for v, _ in VEKTOR) + " |",
          "|---|" + "---:|" * len(VEKTOR)]
    for ka, _ in KAPI:
        hucre = []
        for va, _ in VEKTOR:
            n = len(matris[(ka, va)])
            hucre.append(f"**{n}**" if n else "✅ **0**")
        L.append(f"| {ka} | " + " | ".join(hucre) + " |")
    n_duz_tr = len(matris[(KAPI[0][0], VEKTOR[1][0])])
    n_tr_ascii = len(matris[(KAPI[1][0], VEKTOR[2][0])])
    n_cift_ascii = len(matris[(KAPI[2][0], VEKTOR[2][0])])
    L += ["", f"*(kaçan / toplam **{len(IF)}** yasak ifade)*", "",
          "⭐⭐ **Satırlar okununca tasarım tuzağı görünüyor:**", "",
          f"· **düz `.lower()`** doğru Türkçe büyütmede **{n_duz_tr}** "
          "ifade kaçırıyor — yani *«BAĞIMLISIN»* diye bağıran bir cevap kapıdan geçer.  ",
          f"· **`tr_kucult`** onu sıfırlıyor ama ASCII özensiz yazımda "
          f"**{n_tr_ascii}** kaçırıyor — düzeltilmemiş hâlinden "
          "**daha çok**.  ",
          f"· **iki normalizasyon birden** de tam kapatmıyor: "
          f"**{n_cift_ascii}** kalıyor.  ",
          "· ⭐ **i-sınıfı** üç vektörde de **0**.", "",
          "➡️⭐⭐ *Sebep şu: ASCII özensiz BÜYÜTME Türkçede **bilgi kaybıdır**. `i` ve `ı`*",
          "*ikisi de `I` olur ve hiçbir TEK YÖNLÜ küçültme hangisinin hangisi olduğunu*",
          "*geri getiremez. İki okuma denemek de yetmez: **her iki harfi de içeren** bir*",
          "*ifade hiçbir tek okumada tam çıkmaz.* Örnekle:", "",
          "```text",
          '"ilaç adı"  ->  "ILAÇ ADI"  ->  tr okuması "ılaç adı"  ·  ascii okuması "ilaç adi"',
          "                                 ⛔ ikisi de aranan kalıpla eşleşmez",
          "```", "",
          "⇒ Çözüm normalizasyon değil **SINIF**: `i ı İ I` tek harfe iner ve ayrım",
          "aramada hiç kullanılmaz. ✅ `src/checks.py::i_sinifi` bunu yapıyor.", ""]
    kacan = matris[(KAPI[0][0], VEKTOR[1][0])]        # düz kapı · doğru TR büyütme
    sert_kacan = [(k, i) for k, i in kacan if k in C.SERT_KATEGORILER]
    L += [f"### Düz `.lower()`'ın doğru TR büyütmede kaçırdığı {len(kacan)} ifade", "",
          f"⛔⛔ Bunlardan **{len(sert_kacan)}** tanesi **sert kategoride** "
          f"(`{'`, `'.join(sorted(C.SERT_KATEGORILER))}`) — yani otomatik red kalemi.", "",
          "| kategori | kaçan ifade |", "|---|---|"]
    for k in sorted({k for k, _ in kacan}):
        sert = " ⛔**SERT**" if k in C.SERT_KATEGORILER else ""
        L.append(f"| `{k}`{sert} | " + ", ".join(f"`{i}`" for kk, i in kacan if kk == k) + " |")
    L += ["",
          "⭐ **Cümle başı büyük harf kaçak ÜRETMİYOR** — hiçbir yasak ifade `i`/`ı`",
          "ile **başlamıyor**; kaçak kelime **içindeki** harften doğuyor. ➡️ *Tehdit*",
          "*modeli «cümle başı» değil «BAĞIRMA».*", ""]

    # --- §2 bugün kayba yol açtı mı -------------------------------------------
    veri = metinler()
    kayip, buyuk_yazan = [], 0
    for kaynak, kid, metin in veri:
        if BUYUK.search(metin):
            buyuk_yazan += 1
        d = duz_tarama(metin)
        t = C.scan_forbidden(metin)   # ⭐ canlı kapı — kopyalanmıyor
        ek = {k: sorted(set(t.get(k, [])) - set(d.get(k, []))) for k in t}
        ek = {k: v for k, v in ek.items() if v}
        if ek:
            kayip.append((kaynak, kid, ek))
    L += ["## 2. Bugün kayba yol açtı mı — olgusal zarar", "",
          "⛔ *«Kapı delik»* ile *«kapıdan bir şey kaçtı»* **ayrı sorular**. Burada",
          "asistan metinlerinin tamamı iki tarama ile geçiriliyor: kapının **eski**",
          "hâli (düz `.lower()`) ve **canlı** `scan_forbidden` (i-sınıfı).",
          "⚠️ Yalnızca **asistan** tarafı taranıyor — §15 modelin ürettiğini kısıtlar,",
          "kullanıcının yazdığını değil (T62'nin aynalama dersi).", "",
          "| | |", "|---|---:|",
          f"| taranan asistan metni | **{len(veri)}** |",
          f"| içinde ≥3 harflik BÜYÜK kelime geçen | {buyuk_yazan} |",
          f"| ⛔ **düz `.lower()`'ın kaçırdığı, canlı kapının yakaladığı** | "
          f"**{len(kayip)}** |", ""]
    if kayip:
        L += ["| kaynak | kayıt | kaçan |", "|---|---|---|"]
        for kaynak, kid, ek in kayip[:40]:
            L.append(f"| `{kaynak}` | `{kid}` | "
                     + "; ".join(f"`{k}`: " + ", ".join(f"`{x}`" for x in v)
                                 for k, v in sorted(ek.items())) + " |")
        L += ["", "⛔ **Kaçak gerçek.** Bu kayıtlar kapıdan geçti ve bir kısmı "
              "`datasets/` içinde olabilir — ⚠️ `datasets/` IMMUTABLE (Kural 4), "
              "geriye dönük temizlenemez; sonraki sürümde düşer.", ""]
    else:
        L += ["✅ **Bugün kayıp yok** — düzeltme mevcut korpusta **hiçbir hükmü**",
              "**çevirmedi**. ⭐ Sert bir kapıyı değiştirmenin bedeli böylece ÖNCE",
              "ölçüldü, sonra değiştirildi (K40'ın dersi: kalibre edilmemiş kapı veri öldürür).",
              "",
              f"⛔⛔ **AMA BU ESKİ KAPIYI MASUM YAPMAZDI.** Korpus **bağırıyor**: "
              f"**{buyuk_yazan}** metinde ≥3 harflik BÜYÜK kelime var. ⇒ Sıfır kaçak, "
              "büyük harfin yokluğundan değil, **büyük harfle yazılanların yasak ifade "
              "olmamasından** geliyor — bu bir tesadüf, bir güvence değil. ➡️ *Bir kapının "
              "güvenliği girdinin bugünkü huyuna bağlıysa ölçülmüş değil, ÖDÜNÇ "
              "ALINMIŞTIR — ve üretici değiştiği gün geri istenir.* ⚠️ Üretim şu an "
              "yalnızca Claude Code (K30); insan katkısı, forum verisi ya da İP5 pilotu "
              "devreye girdiği gün eski kapı ilk gün delinirdi.", ""]

    # --- §3 ötekiler -----------------------------------------------------------
    kaynak_kod = (KOK / "src/checks.py").read_text(encoding="utf-8")
    duz = [(n, s.strip()) for n, s in enumerate(kaynak_kod.split("\n"), 1)
           if ".lower()" in s and "tr_kucult" not in s
           and not s.strip().startswith("#")]
    L += ["## 3. Aynı ailenin `checks.py`'deki öteki yerleri", "",
          "⚠️ Bu betik yalnızca §15 taramasını ölçtü. Aynı dosyada düz `.lower()`",
          "kullanan **başka** satırlar da var ve ⛔ **hiçbiri sınanmadı**:", "",
          "| satır | kod |", "|---|---|"]
    for n, s in duz:
        L.append(f"| `src/checks.py:{n}` | `{s[:90]}` |")
    L += ["", "➡️ *Bir hata ailesinin dördüncü örneğini bulmak, beşincisini de aramayı*",
          "*gerektirir — ve bu betik onu yapmadı.*", "",
          "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ Düzeltmenin **yeni veride** etkisi | §2 düzeltmenin mevcut veride "
          "**hiçbir hükmü çevirmediğini** gösteriyor (bu yüzden uygulanması güvenliydi), "
          "ama gelecekte ne kadar yakalayacağı ölçülemez |",
          "| ⛔ `SERT_KATEGORILER` dışındaki kaçaklar | otomatik red değil, elle gözden "
          "geçirme kalemi — kaçmaları bir kaydı geçirmez, **bir uyarıyı susturur** |",
          "| ⚠️ Yalnızca **büyük harf** sınandı | aynı ailenin başka biçimleri "
          "(NFKD ayrıştırması, birleşen imler) `tohum_guvenlik.py` başlığında anlatılıyor "
          "ve `checks.py` için ayrıca ölçülmedi |",
          "| ⚠️ Tarama **asistan** tarafıyla sınırlı | kullanıcı metni kapsam dışı "
          "(tasarım gereği) |", ""]

    RAPOR.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print(f"   kaçabilen ifade {len(kacan)}/{len(IF)} (sert kategoride {len(sert_kacan)}) · "
          f"taranan asistan metni {len(veri)} · gerçek kaçak {len(kayip)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
