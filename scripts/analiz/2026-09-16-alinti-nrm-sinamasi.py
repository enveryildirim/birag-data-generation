#!/usr/bin/env python3
"""⭐⭐ Aynı düzeltme, TERS YÖN: burada i-sınıfı kapıyı GÜÇLENDİRMEZ, ZAYIFLATIR.

T73-T76'da düz `.lower()`'ın Türkçe kusuru hep aynı sonucu doğurdu: kapı
ateşlemiyordu, yani ihlal kaçıyordu ⇒ `i_sinifi` **güvenli yönde** genişletti.
⛔ `filter.alinti_nrm` bu ailenin son üyesi ama **işi farklı**: judge'ın
alıntısının kaynakta GERÇEKTEN bulunduğunu doğruluyor, yani **reddetmek** için
var (T43/T51). ⇒ Eşleştiriciyi genişletmek daha çok ihlal yakalamaz;
**uydurma alıntının geçmesini kolaylaştırır**.

⭐ İkinci fark: normalizasyon **iki tarafa da** uygulanıyor (alıntıya ve
kaynağa). ⇒ Kusur kapıyı **kör etmez**, **fazladan ateşletir** — gerçek bir
alıntı *«doğrulanamadı»* sayılır. Kapının kendi şerhi bunu *daha pahalı* hata
sayıyor (*«kanıtı yok eder»*).

⇒ Bu betik üç şey ölçüyor: **(1)** hangi yazım vektörü kusur üretiyor,
**(2)** yön gerçekten *«fazladan ateşleme»* mi, **(3)** i-sınıfı arşivlenmiş
**1735 alıntıda** kaç hükmü çevirirdi — ve çevirdiklerinin yönü ne.

Girdi : reports/analiz/ham-judge/*.jsonl (arşiv, yeniden puanlama YOK) ·
        src/filter.py · scripts/analiz/2026-09-15-v9-kapi-denetimi.py
Çıktı : reports/analiz/2026-09-16-alinti-nrm-sinamasi.md
Kullanım: uv run python scripts/analiz/2026-09-16-alinti-nrm-sinamasi.py
"""
# lower-muaf-dosya: `alinti_nrm`'in eski/yeni hâllerini karşılaştırıyor (T80)
from __future__ import annotations

import hashlib
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-alinti-nrm-sinamasi.md"
sys.path.insert(0, str(KOK / "src"))
import filter as f  # noqa: E402
from tohum_guvenlik import i_sinifi  # noqa: E402

_sp = _iu.spec_from_file_location("k9", KOK / "scripts/analiz/2026-09-15-v9-kapi-denetimi.py")
K9 = _iu.module_from_spec(_sp)
sys.argv = [sys.argv[0]]
_sp.loader.exec_module(K9)

ORIJINAL = f.alinti_nrm


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def sertlestirilmis(s: str | None) -> str:
    """⭐ Var olan normalizasyonun ÜSTÜNE i-sınıfı — mantık kopyalanmıyor."""
    return i_sinifi(ORIJINAL(s))


def tarama(patch: bool) -> tuple[int, int, int, list]:
    """Arşivin tamamını tarar. `patch` ise `alinti_nrm` sertleştirilmiş sürüm olur.

    ⚠️ Kaynak metinleri de `alinti_nrm`'den geçiyor; bu yüzden kaynaklar her
    varyantta **yeniden kuruluyor** — tek taraflı yama iki tarafı ayırırdı.
    """
    f.alinti_nrm = sertlestirilmis if patch else ORIJINAL
    try:
        e2 = K9.eksen2_kaynaklari()
        kor = K9.korpus_kaynaklari()
        n = alinti = ates = 0
        vaka = []
        for yol in sorted(K9.HAM.glob("*.jsonl")):
            ad = yol.stem
            if ad.startswith("e2-") or ad.startswith("v9-") or ad.startswith("v8-") \
               or ad.startswith("v7-"):
                kol = K9.B9.HARITA.get(ad, (None, None))[0] if hasattr(K9.B9, "HARITA") else None
                bul = (lambda r, _k=kol: e2.get((_k, r.get("id")))) if kol else \
                      (lambda r: kor.get(r.get("id")))
            else:
                bul = lambda r: kor.get(r.get("id"))
            try:
                a, b, _m, c, v = K9.tara(yol, bul)
            except Exception:
                continue
            n += a
            alinti += b
            ates += c
            vaka += v
        return n, alinti, ates, vaka
    finally:
        f.alinti_nrm = ORIJINAL


VEKTOR = [
    ("olduğu gibi", "ilaç adı", "ilaç adı"),
    ("⭐ YALNIZ `İ` (dotsuz ı yok)", "İLAÇ", "ilaç"),
    ("⭐ YALNIZ `ı` (İ yok)", "ADI", "adı"),
    ("kaynak BÜYÜK (doğru TR)", "İLAÇ ADI", "ilaç adı"),
    ("alıntı BÜYÜK (doğru TR)", "ilaç adı", "İLAÇ ADI"),
    ("kaynak ASCII özensiz", "ILAÇ ADI", "ilaç adı"),
    ("alıntı ASCII özensiz", "ilaç adı", "ILAÇ ADI"),
    ("ikisi de BÜYÜK", "İLAÇ ADI", "İLAÇ ADI"),
    ("noktasız `ı` ↔ `I`", "BIRAKMALISIN", "bırakmalısın"),
]


def main() -> int:
    L: list[str] = []
    L += ["# `alinti_nrm` sınandı — aynı düzeltme, **ters yön**", "",
          f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
          f"**Girdi:** `src/filter.py` SHA256 `{sha(KOK/'src/filter.py')}` "
          f"(`alinti_nrm` **çağrılıyor**)  ",
          f"**Girdi:** `scripts/analiz/2026-09-15-v9-kapi-denetimi.py` SHA256 "
          f"`{sha(KOK/'scripts/analiz/2026-09-15-v9-kapi-denetimi.py')}` "
          f"(tarama **çağrılıyor**, kopyalanmıyor)  ",
          f"**Girdi:** `reports/analiz/ham-judge/*.jsonl` — "
          f"**{len(list(K9.HAM.glob('*.jsonl')))}** arşiv (yeniden puanlama **YOK**)",
          "", "---", "", "## 1. ⭐⭐ Neden bu üye ötekilerden farklı", "",
          "T73-T76'da düz `.lower()`'ın Türkçe kusuru hep aynı sonucu doğurdu: **kapı**",
          "**ateşlemiyordu**, ihlal kaçıyordu ⇒ `i_sinifi` **güvenli yönde** genişletti.",
          "⛔ `alinti_nrm`'in işi farklı: judge'ın alıntısının kaynakta **gerçekten**",
          "bulunduğunu doğruluyor, yani **reddetmek** için var (T43 · T51).", "",
          "| | `scan_forbidden` (T73) | `alinti_nrm` (burada) |", "|---|---|---|",
          "| kapının işi | ihlali **yakalamak** | uydurma alıntıyı **reddetmek** |",
          "| eşleştiriciyi genişletmek | ⭐ daha çok ihlal yakalar — **güvenli** | "
          "⛔ daha çok alıntıyı kabul eder — **zayıflatır** |",
          "| kusurun yönü | ihlal **kaçar** | gerçek alıntı **reddedilir** |", "",
          "⭐ İkinci fark: normalizasyon **iki tarafa da** uygulanıyor (alıntıya ve",
          "kaynağa). ⇒ Kusur kapıyı **kör etmez**, **fazladan ateşletir**. Kapının kendi",
          "şerhi bunu *daha pahalı* hata sayıyor: *«kanıtı yok eder»*.", "", "---", ""]

    # --- §2 vektör tablosu -----------------------------------------------------
    L += ["## 2. Hangi yazım vektörü kusur üretiyor", "",
          "Alıntı ve kaynak **ayrı ayrı** yazılıp eşleşme sınanıyor.", "",
          "| vektör | kaynak | alıntı | bugün | i-sınıflı |", "|---|---|---|---|---|"]
    bugun_kacan = sert_kacan = 0
    for ad, kaynak, alinti in VEKTOR:
        e = ORIJINAL(alinti) in ORIJINAL(kaynak)
        y = sertlestirilmis(alinti) in sertlestirilmis(kaynak)
        bugun_kacan += not e
        sert_kacan += not y
        L.append(f"| {ad} | `{kaynak}` | `{alinti}` | "
                 f"{'✅ eşleşti' if e else '⛔ **ateşler**'} | "
                 f"{'✅ eşleşti' if y else '⛔ ateşler'} |")
    L += ["",
          f"⛔ Bugün **{bugun_kacan}/{len(VEKTOR)}** vektörde **yanlış ateşleme** var; "
          f"i-sınıflı sürümde **{sert_kacan}**.", "",
          "⭐⭐ **İki mekanizma ayrı ayrı sınandı ve yalnızca BİRİ açık:**", "",
          "· `İLAÇ` ↔ `ilaç` **eşleşiyor** — çünkü `alinti_nrm` `.lower()`'dan sonra",
          "  `.replace(\"i̇\", \"i\")` yapıyor, yani **birleşen noktayı düşürüyor**. ⭐ Bu",
          "  yama K76'nın `İ` dersinden geliyor ve **işini görüyor**.  ",
          "· `ADI` ↔ `adı` **eşleşmiyor** — `\"ADI\".lower()` → `\"adi\"`, Türkçesi `\"adı\"`.",
          "  ⛔ **`I` ↔ `ı` vakası açık.**", "",
          "➡️ *Ötekiler bu ikisinin BİLEŞİMİ: `İLAÇ ADI` hem İ hem ı taşıdığı için*",
          "*ateşliyor, ama ateşlemenin sebebi `ı`. ⚠️ İlk vektör tablomda ikisini*",
          "*ayırmamıştım ve satır «doğru TR büyütme İ'yi kırıyor» der gibi okunuyordu —*",
          "*okunuşu düzeltmek için ayrı satırlar eklendi.*", "", "---", ""]

    # --- §3 gerçek veri --------------------------------------------------------
    n0, a0, t0, v0 = tarama(False)
    n1, a1, t1, v1 = tarama(True)
    k0, k1 = {(x[0], x[1], x[2]) for x in v0}, {(x[0], x[1], x[2]) for x in v1}
    yeni_gecen = k0 - k1
    yeni_ates = k1 - k0
    L += ["## 3. Arşivlenmiş alıntılarda etkisi", "",
          "⛔ Yeniden puanlama **yok**: arşiv okunuyor ve yalnızca eşleştirici",
          "değiştiriliyor. Kaynak metinleri de `alinti_nrm`'den geçtiği için her",
          "varyantta **yeniden kuruluyor**.", "",
          "| | bugün | i-sınıflı |", "|---|---:|---:|",
          f"| denetlenen kayıt | {n0} | {n1} |",
          f"| denetlenen alıntı | {a0} | {a1} |",
          f"| ateşleme | {t0} | {t1} |", "",
          "⛔⛔ **MUTLAK SAYILAR BU BETİKLE GÜVENİLİR DEĞİL ve kapı defteriyle**",
          f"**KARŞILAŞTIRILAMAZ.** `2026-09-15-v9-kapi-defteri.md` 1735 alıntıda **1**",
          f"ateşleme bildiriyor; burada {a0} alıntıda {t0}. Sebep: bu betik **46 arşivin**",
          "**tamamını** tarıyor (v7/v8/korpus dahil) ve hangi kaydın hangi kaynağa ait",
          "olduğunu **dosya adı önekinden kabaca** kuruyor — kapı defteri bunu koşu",
          "dizinlerinden **kesin** kuruyor. ⇒ Yanlış eşleşen kayıtlar sahte ateşleme",
          "üretiyor ve bu sayı bir kapı ölçüsü **değil**.", "",
          "⭐⭐ **Ama FARK güvenilir:** iki varyant **aynı** (kusurlu olabilen) eşlemeyi",
          "kullanıyor; eşleme hatası her iki tarafta **birebir aynı** olduğu için",
          "çıkarımda düşüyor. ➡️ *Bir ölçüm hatalı bir taban üzerinde bile GÜVENİLİR bir*",
          "*FARK verebilir — yeter ki hata iki kolda da aynı olsun. Mutlak sayıyı*",
          "*bildirmek ise bu durumda yanıltıcıdır ve bu yüzden burada **kalın**",
          "*yazılmıyor.*", "",
          f"| | |", "|---|---:|",
          f"| ⛔ i-sınıfıyla **yeni GEÇEN** (kapı zayıflar) | **{len(yeni_gecen)}** |",
          f"| ⭐ i-sınıfıyla **yeni ATEŞLEYEN** (kapı sıkılaşır) | **{len(yeni_ates)}** |", ""]
    if yeni_gecen:
        L += ["| koşu | kayıt | alan |", "|---|---|---|"]
        L += [f"| `{a}` | `{b}` | `{c}` |" for a, b, c in sorted(yeni_gecen)[:20]] + [""]
    if not yeni_gecen and not yeni_ates:
        L += ["✅ **Hiçbir hüküm değişmiyor.** ⇒ i-sınıfı bu kapıda bugün **ne fayda**",
              "**ne zarar** üretiyor.", "",
              "⭐⭐ **Ve bu, düzeltmeyi UYGULAMAMAK için yeterli sebep.** T73'te i-sınıfı",
              "*«bedeli 0, kazancı 26 ifade»* diye uygulandı. Burada kazanç **0** ve",
              "yön **zayıflatma**: eşleştirici genişledikçe uydurma bir alıntının",
              "kaynakta *«bulunmuş»* sayılma olasılığı artar. ➡️ *Aynı yamanın aynı repoda*",
              "*iki farklı kapıda iki farklı kararı olabilir; belirleyen şey yamanın*",
              "*kendisi değil, kapının HANGİ YÖNDE yanılmayı seçtiğidir (T69'un*",
              "*«yönü biz seçtik» cümlesinin koddaki karşılığı).*", ""]
    L += ["## ⛔ Bu sınamanın söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ **Mutlak ateşleme sayısı** | kaynak eşlemesi kabaca kuruldu; sayı bir "
          "kapı ölçüsü değil. ⭐ Yalnızca **fark** yorumlanabilir (§3) |",
          "| ⛔ **Yanlış negatif oranı** | kapı v9 defterinde 1735 alıntıda **1** kez "
          "ateşledi ve o elle okunup **gerçek judge hatası** çıktı ⇒ büyük-küçük harf "
          "kusurunun ürettiği yanlış ateşleme **0**; ama kaç uydurma alıntının "
          "**geçtiği** ölçülemez |",
          "| ⛔ Aksan/NFKD sınıfı | `alinti_nrm` NFKD uygulamıyor; ayrıştırılmış `ç`/`ş` "
          "taşıyan bir alıntı hâlâ eşleşmeyebilir ve bu **ölçülmedi** |",
          "| ⚠️ Vektör tablosu **kurgu** | gerçek judge çıktısında büyük harfli alıntı "
          "olup olmadığı ayrıca sayılmadı |",
          "| ⛔ Karar **uygulanmadı** | `alinti_nrm` DEĞİŞTİRİLMEDİ; gerekçe §3'te |", ""]

    RAPOR.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print(f"   vektör: bugün {bugun_kacan}/{len(VEKTOR)} yanlış ateşleme · "
          f"i-sınıflı {sert_kacan}")
    print(f"   arşiv (kaba eşleme, MUTLAK sayı güvenilir DEĞİL): kayıt {n0} · "
          f"alıntı {a0} · ateşleme {t0} → {t1}")
    print(f"   yeni geçen {len(yeni_gecen)} · yeni ateşleyen {len(yeni_ates)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
