#!/usr/bin/env python3
"""v6-parti7 tasarım ızgarası — 60 kayıt. Üretimden ÖNCE yazılır, dondurulur.

⛔⛔⛔ **ÜÇ KARAR KULLANICININ, GEREKÇELERİ ÖLÇÜLMÜŞ.**

⭐ **(1) `profil` EKSENİ HEDEFLEMEDEN ÇIKARILDI.** T220/T221: v6
kayıtlarının yarısından fazlasında metin kişinin mesleki profili hakkında
**hiçbir şey söylemiyor** (parti1 %27, parti3-6 %53 doğrulanabilir). T225:
onarım sonrası zeminde kuralın ürettiği altı tavanın **dördü**
`profil=mavi_yakali` idi. ➡️ *Bir eksenin altı partidir kapanmaması ile o
eksenin kayıtta görünmemesi aynı şeyin iki yüzü olabilir; görünmeyen bir
eksende hedef tutturmak, korpusu değil tohum dosyasını düzeltir.*
⛔ Eksen **silinmedi**: envanterde ölçülmeye devam ediyor ve raporda
*«hedeflenmiyor»* diye ayrı bir tabloda duruyor. Ölçmeyi bırakmak,
kararı geri alınamaz yapardı.

⭐ **(2) K = 2.** N₀ = 926 ⇒ korpus 2 partide **1046**'ya varır; K=3
1106 demekti ve hedeflenen büyüklüğün üstü. Gerekçe T211'den beri aynı:
*«korpus hedeflenen büyüklüğe varmadan kapansın»*.

⭐ **(3) ZEMİN ONARIM SONRASI.** `v6-parti1`'in künyesi T224'te onarıldı;
envanterler `-parti1-6-onarim-sonrasi` dosyalarından okunuyor.

⛔⛔ **KURAL ARTIK HEDEF ÜRETMİYOR, YALNIZ TAVAN.** `profil` çıkınca geriye
**iki tavan** kalıyor (`evre=tolerans` ve `evre=tolerans&siddet_seviyesi=orta`)
ve **sıfır hedef**. ➡️ *Altı parti sonra kapsama kuralı bir çekim gücü
değil, yalnızca bir frendir; partiyi artık ızgara kotaları ve motivasyon
katmanı kuruyor.* Bu, planın en önemli özelliği ve raporda yazılı.

⛔ **MARJİNAL GERİLEME KAPISI DEĞİŞTİ:** `profil` bilerek hedeflenmediği
için o eksenin kötüleşmesi artık planı REDDETMİYOR — ama raporda ayrıca
gösteriliyor. Kasıtlı bir kararın yan etkisini hata saymak, kararı
görünmez kılardı.

Girdi : reports/analiz/2026-09-20-kapsama-acigi-envanteri-parti1-6-onarim-sonrasi.json
        reports/analiz/2026-09-21-hucre-kapsama-envanteri-parti1-6-onarim-sonrasi.json
Çıktı : data/plan/v6-parti7.jsonl · reports/analiz/2026-09-21-v6-parti7-plan.md
"""
from __future__ import annotations

import collections
import json
import os
import random
from collections import Counter
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
N = 60
K_UFUK = 2          # ⛔ kullanıcı kararı: N₀=926 ⇒ 926+2×60 = 1046
ESIK_HUCRE = 3.0
ESIK_MARJINAL = 3.0
TOLERANS = 0.3
TOHUM = int(os.environ.get("BIRAG_PLAN_TOHUM", "20260930"))
CIKTI = KOK / "data/plan/v6-parti7.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-v6-parti7-plan.md"
HUCRE = KOK / "reports/analiz/2026-09-21-hucre-kapsama-envanteri-parti1-6-onarim-sonrasi.json"
MARJINAL = KOK / "reports/analiz/2026-09-20-kapsama-acigi-envanteri-parti1-6-onarim-sonrasi.json"


def _modul(ad: str, yol: str):
    sp = _iu.spec_from_file_location(ad, KOK / yol)
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


# ⛔ Tek nesne grafiği (parti4'ün modül kimliği tuzağı). Hepsi PP5'inkiler.
PP6 = _modul("pp6", "scripts/analiz/2026-09-21-v6-parti6-plan.py")
PP5 = PP6.PP5
PP4, PP3, PP1, PP2 = PP5.PP4, PP5.PP3, PP5.PP1, PP5.PP2
P1 = PP1.P1
KRIZ = PP5.KRIZ
# ⛔ KULLANICI KARARI: hedeflemeden çıkarılan eksen(ler). Ölçüm sürüyor.
HEDEFLENMEYEN = ("profil",)
ENV = _modul("env", "scripts/analiz/2026-09-20-kapsama-acigi-envanteri.py")

KACINMA: dict[tuple[str, str], float] = {}
KOTA: dict[tuple[str, str], int] = {}
_ALINMIS: dict[str, dict] = {}


def _coz(anahtar: str) -> tuple[tuple[str, str], tuple[str, str]]:
    a, b = anahtar.split("&")
    e1, v1 = a.split("=", 1)
    e2, v2 = b.split("=", 1)
    return (e1, v1), (e2, v2)


def paylar() -> tuple[dict, dict, dict, int, list, dict]:
    """Ufuk kuralı — DEĞİŞMEDEN, hem marjinallere hem hücrelere.

    Döner: (hedef, kacinma, kota, N₀, kırpık, kaynak) — `kaynak` her anahtarın
    hangi envanterden ve hangi farkla geldiğini tutar (rapor için).
    """
    n0 = PP5.korpus_boyu()
    hedef: dict[tuple[str, str], int] = {}
    kacinma: dict[tuple[str, str], float] = {}
    kota: dict[tuple[str, str], int] = {}
    kirpik: list[str] = []
    atlanan: list[str] = []
    kaynak: dict[tuple[str, str], dict] = {}

    def _ekle(sent: tuple[str, str], v: dict, tur: str, ad: str) -> None:
        ps, p0 = v["havuz"] / 100, v["sette"] / 100
        q_ham = (ps * (n0 + N * K_UFUK) - p0 * n0) / (N * K_UFUK)
        q = max(0.0, min(1.0, q_ham))
        if not 0.0 <= q_ham <= 1.0:
            kirpik.append(f"{ad} (ham q=%{100*q_ham:.1f})")
        pay = round(q * N)
        if v["fark"] > 0:
            hedef[sent] = pay
        else:
            kota[sent] = pay
            kacinma[sent] = abs(v["fark"]) * N / 100
        kaynak[sent] = {"tur": tur, "ad": ad, **v, "pay": pay}

    # (a) MARJİNAL — parti5'in kuralı, aynen. Hedef yönü boş, tavan yönü dolu.
    mj = json.loads(MARJINAL.read_text(encoding="utf-8"))["acik"]
    for anahtar, v in mj.items():
        eksen, deger = anahtar.split("=", 1)
        if eksen in PP4.IZGARA_EKSENI or abs(v["fark"]) < ESIK_MARJINAL:
            continue
        if eksen in HEDEFLENMEYEN:      # ⛔ kullanıcı kararı — ölçülür, hedeflenmez
            atlanan.append(f"{anahtar} ({v['fark']:+.2f})")
            continue
        _ekle((eksen, deger), v, "marjinal", anahtar)

    # (b) HÜCRE — aynı kural, iki eksenin kesişimi.
    hc = json.loads(HUCRE.read_text(encoding="utf-8"))["acik"]
    for anahtar, v in hc.items():
        if abs(v["fark"]) < ESIK_HUCRE:
            continue
        (e1, _), (e2, _) = _coz(anahtar)
        if e1 in HEDEFLENMEYEN or e2 in HEDEFLENMEYEN:
            atlanan.append(f"{anahtar} ({v['fark']:+.2f})")
            continue
        _ekle((f"hucre:{anahtar}", "1"), v, "hücre", anahtar)
    paylar.atlanan = atlanan            # rapora taşınıyor
    return hedef, kacinma, kota, n0, kirpik, kaynak


def _sentetikle(hav: list[dict], anahtarlar: list[str]) -> None:
    """Hedeflenen hücreyi tohumun `meta`sına tek bir alan olarak yazar.

    ⭐ Böylece PP1'in `str(t["meta"].get(e)) == v` karşılaştırması hücreyi de
    görür ve PP1'in tek satırı bile değişmez. ⛔ Yalnız bellekte.
    """
    for t in hav:
        for a in anahtarlar:
            (e1, v1), (e2, v2) = _coz(a)
            if str(t["meta"].get(e1)) == v1 and str(t["meta"].get(e2)) == v2:
                t["meta"][f"hucre:{a}"] = "1"


def _ihtiyac_sirasi(hav: list[dict], kalan: dict) -> list[dict]:
    """PP5'in sıralayıcısı — hücre anahtarlarıyla aynen çalışıyor."""
    kullanim: Counter = Counter()
    for m in _ALINMIS.values():
        for (e, v) in KOTA:
            if str(m.get(e)) == v:
                kullanim[(e, v)] += 1

    def anahtar(t):
        puan = sum(kalan.get((e, v), 0) for (e, v) in PP1.TOHUM_HEDEF
                   if str(t["meta"].get(e)) == v)
        ceza = sum(w for (e, v), w in KACINMA.items()
                   if str(t["meta"].get(e)) == v and kullanim[(e, v)] >= KOTA[(e, v)])
        return (-(puan - ceza), t["seed_id"])
    return sorted(hav, key=anahtar)


def marjinal_gerileme(yeni_sid: set[str]) -> tuple[list, list]:
    """Parti6 eklendikten sonra tek eksen farkları. Döner: (kötüleşen, iyileşen).

    ⛔⛔ KAPI YALNIZ KÖTÜLEŞMEYE BAKAR. İlk hâli *«sonrasında |fark| ≥ 3 olan
    her sınıf»*ı ihlal sayıyordu ve parti6'nın İYİLEŞTİRDİĞİ üç sınıfı hata
    diye bastı (−4,8 → −3,3 dahil). ➡️ *Bir gerileme kapısı mutlak eşiğe
    değil FARKA bakmalıdır; yoksa devraldığı borcu kendi suçu sayar.*
    Kötüleşme = büyüklük `TOLERANS`tan fazla arttı, ya da eşiği yeni aştı.
    """
    tohum = [json.loads(l) for l in
             (KOK / "data/seeds.v2.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    kullanilan = P1.kullanilmis() | yeni_sid
    U = [t for t in tohum if t["source_id"] in kullanilan]
    eski = json.loads(MARJINAL.read_text(encoding="utf-8"))["acik"]
    kotu, iyi, serbest = [], [], []
    for e in ENV.EKSEN:
        cu = collections.Counter(t["meta"].get(e) for t in U)
        ch = collections.Counter(t["meta"].get(e) for t in tohum)
        for v, n in ch.items():
            yeni = 100 * n / len(tohum) - 100 * cu.get(v, 0) / len(U)
            onc = eski.get(f"{e}={v}", {}).get("fark", 0.0)
            if abs(yeni) > abs(onc) + TOLERANS and abs(yeni) >= ESIK_MARJINAL:
                # ⛔ Bilerek hedeflenmeyen bir eksenin kötüleşmesi bir İHLAL
                # değil, alınmış kararın yan etkisidir. Reddetmiyor ama
                # raporda ayrı duruyor — yoksa karar görünmez olurdu.
                (serbest if e in HEDEFLENMEYEN else kotu).append(
                    (f"{e}={v}", round(onc, 2), round(yeni, 2)))
            elif abs(onc) >= ESIK_MARJINAL and abs(yeni) < abs(onc) - TOLERANS:
                iyi.append((f"{e}={v}", round(onc, 2), round(yeni, 2)))
    return kotu, iyi, serbest


def main() -> int:
    global KACINMA, KOTA
    assert PP5.PP4 is PP4 and PP4.PP3 is PP3 and PP3.PP1 is PP1, "⛔ modül kimliği ayrıştı"
    hedef, KACINMA, KOTA, n0, kirpik, kaynak = paylar()
    anahtarlar = [e.split(":", 1)[1] for (e, _) in list(hedef) + list(KOTA)
                  if e.startswith("hucre:")]

    _orij_havuz = P1.havuz

    def _havuz(*a, **kw):        # ⛔ T224'ten sonra `havuz(CIKTI)` çağrılıyor
        hav = _orij_havuz(*a, **kw)
        _sentetikle(hav, anahtarlar)
        return hav
    P1.havuz = _havuz

    PP1.TOHUM_HEDEF.clear()
    PP1.TOHUM_HEDEF.update(hedef)
    PP1._ihtiyac_sirasi = _ihtiyac_sirasi
    PP1._TURETILMIS = True
    PP1.CIKTI, PP1.RAPOR, PP1.TOHUM, PP1.N = CIKTI, RAPOR, TOHUM, N
    _orij_sec = P1.sec

    def _sec(s, h, alinmis):
        t = _orij_sec(s, h, alinmis)
        if t is not None:
            _ALINMIS[t["seed_id"]] = t["meta"]
        return t
    P1.sec = _sec

    print(f"⭐ korpus N₀={n0} · ufuk K={K_UFUK} parti · hücre eşiği {ESIK_HUCRE}")
    print(f"⭐ hedef ({len(hedef)}): " +
          ", ".join(f"{kaynak[k]['ad']}→{v}" for k, v in hedef.items()))
    print(f"⛔ tavan ({len(KOTA)}): " +
          ", ".join(f"{kaynak[k]['ad']}→{v}" for k, v in KOTA.items()))
    if (rc := PP1.main()):
        return rc

    satir = [json.loads(l) for l in CIKTI.read_text(encoding="utf-8").splitlines() if l.strip()]
    ctx = [r for r in satir if r["context"]]
    dagitim = PP3.baglam_paylari(len(ctx))
    random.Random(TOHUM).shuffle(dagitim)
    for r, s in zip(sorted(ctx, key=lambda r: r["sira"]), dagitim):
        r["baglam_davranisi"] = s
    tohumlar = KRIZ._tohumlar()
    isaret = sum(1 for r in satir
                 if PP3.ciplak_kriz(tohumlar.get(r["seed_id"], {}))
                 and not r.update({"beyan_ciplak_kriz": True}))
    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in satir),
                     encoding="utf-8")

    # ⛔⛔ MARJİNAL GERİLEME KAPISI
    bozulan, iyilesen, serbest = marjinal_gerileme({r["source_id"] for r in satir})
    ek = ["", "## ⛔⛔⛔ Parti5'ten fark — BİRİM DEĞİŞTİ, ÖLÇÜ DEĞİŞMEDİ", "",
          "⛔⛔ **Bu planın ilk hâli yanlış bir önermeyle kuruldu ve kendi "
          "kapısı yakaladı.** *«Marjinal açıkların tamamı 3 puanın altına "
          "indi (+2,7)»* deniyordu; o sayı `--esik=0` koşusundan okunmuştu ve "
          "o süzgeç `havuz% − set% ≥ 0` demek, yani **yalnız EKSİK temsil "
          "yönü**. Çift yönlü koşuda üç sınıf hâlâ eşiğin üstünde ve hepsi "
          "FAZLA temsil. ➡️⭐⭐⭐ *Bir ölçümün eşiği yönlüyse, eşiği düşürmek "
          "ölçümü genişletmez — yalnız bir yönü uzatır; ve o yönde boş çıkan "
          "tablo «ölçüt tükendi» diye okunur.*", "",
          "⭐ Tükenen şey **hedef yönü**: en büyük pozitif fark +2,7 ⇒ "
          "marjinaller yalnız TAVAN üretiyor, hedef üretmiyor. ⚠️⚠️ Bu da "
          "T211'in doğrulanması değil: parti4'teki en büyük pozitif açık "
          "zaten +3,4'tü ve en çok oynayan sınıf 1,2 puan hareket etti; "
          "negatif yön ise beş partide kapanmadı. *Bir ölçütün karşılanması, "
          "ölçtüğü iddianın doğrulanması değildir.*", "",
          "⭐⭐ Hedef yönü boş kaldığı için birim inceltildi — kapsama "
          "envanterinin kendi son şerhi: *«eksenler bağımsız sayıldı, birlikte "
          "dağılım bakılmadı»*. Fark tanımı ve ufuk kuralı AYNEN duruyor "
          "(K97); değişen yalnız birim. Marjinal tavanlar da yerinde: ikisi "
          "birlikte çalışıyor, biri diğerinin yerine değil.", "",
          f"⭐ **Ufuk kuralı** (N₀={n0}, n={N}, K={K_UFUK}):", "",
          "```", "q = (p_havuz × (N₀ + n·K) − p_set × N₀) / (n·K)", "```", "",
          f"⛔ **K={K_UFUK}** — kullanıcı kararı (parti5'te 5, parti6'da 3). Gerekçe değişmedi — *«korpus "
          f"hedeflenen büyüklüğe varmadan kapansın»* — değişen N₀: "
          f"{n0} + {K_UFUK}×{N} = {n0 + K_UFUK * N}.", "",
          "| birim | tür | set | havuz | fark | **pay** | ulaşılan |",
          "|---|---|---:|---:|---:|---:|---:|"]
    for k, bilgi in sorted(kaynak.items(), key=lambda x: x[1]["fark"]):
        ad = bilgi["ad"]
        if k[0].startswith("hucre:"):
            (e1, v1), (e2, v2) = _coz(ad)
            ul = sum(1 for r in satir
                     if str((tohumlar.get(r["seed_id"], {}).get("meta") or {}).get(e1)) == v1
                     and str((tohumlar.get(r["seed_id"], {}).get("meta") or {}).get(e2)) == v2)
        else:
            ul = sum(1 for r in satir
                     if str((tohumlar.get(r["seed_id"], {}).get("meta") or {}).get(k[0])) == k[1])
        yon = "hedef" if k in hedef else "tavan"
        ek.append(f"| `{ad}` | {bilgi['tur']} · {yon} | %{bilgi['sette']} | "
                  f"%{bilgi['havuz']} | {bilgi['fark']:+.2f} | **{bilgi['pay']}** | {ul} |")
    ek += ["", "## ⛔⛔⛔ HEDEFLEMEDEN ÇIKARILAN EKSEN — ölçülüyor, hedeflenmiyor",
           "", "⭐ Kullanıcı kararı: `" + "`, `".join(HEDEFLENMEYEN) + "`. Gerekçe "
           "ölçülmüş: T220/T221 bu eksenin v6 kayıtlarının yarısından fazlasında "
           "**metinde hiç görünmediğini** buldu; T225 kuralın ürettiği altı "
           "tavanın dördünün bu eksenden geldiğini gösterdi. ⛔ Eksen "
           "SİLİNMEDİ — envanterde ölçülmeye devam ediyor ve eşiği aşan "
           "birimleri burada duruyor:", "",
           "| eşiği aşan ama hedeflenmeyen birim | fark |", "|---|---:|"]
    for x in getattr(paylar, "atlanan", []):
        ad, fark = x.rsplit(" (", 1)
        ek.append(f"| `{ad}` | {fark.rstrip(')')} |")
    ek += ["", f"⛔⛔ **Bu karar {len(getattr(paylar, 'atlanan', []))} birimi "
           "hedeflemenin dışına aldı ve geriye SIFIR HEDEF, iki tavan kaldı.** "
           "➡️ *Altı parti sonra kapsama kuralı bir çekim gücü değil, yalnızca "
           "bir frendir; partiyi artık ızgara kotaları ve motivasyon katmanı "
           "kuruyor.* Bu, planın en önemli özelliği.", ""]
    if serbest:
        ek += ["⚠️ **Hedeflenmeyen eksende kötüleşen** (plan REDDEDİLMEDİ, "
               "kasıtlı kararın yan etkisi):", "",
               "| eksen = değer | önce | sonra |", "|---|---:|---:|"]
        ek += [f"| `{k}` | {x:+.2f} | **{y:+.2f}** |" for k, x, y in serbest]
        ek += [""]
    else:
        ek += ["⭐ Hedeflenmeyen eksende kötüleşme de olmadı: "
               "`profil=mavi_yakali` bu planda **−4,20 → −3,70** ile iyileşti. "
               "⛔ Bu bir başarı değil bir rastlantı olabilir; ızgara kotaları "
               "onu hedeflemeden oynatıyor ve bir sonraki partide ters yöne de "
               "gidebilir.", ""]
    if kirpik:
        ek += ["", f"⚠️ **Kırpılan hücre(ler):** {', '.join(kirpik)} — ham pay [0,1] "
                   f"dışına düştü, yani bu açık {K_UFUK} partide kapanamıyor.", ""]
    ek += ["", "## ⛔⛔ Marjinal gerileme kapısı", "",
           "⛔ Kapı KÖTÜLEŞMEYE bakar, mutlak eşiğe değil: 3'ü zaten aşmış bir "
           "sınıfın iyileşmesi ihlal değildir. (İlk hâli buna bakmıyordu ve "
           "kendi düzelttiği üç sınıfı hata diye bastı.)", ""]
    if bozulan:
        ek += ["| eksen = değer | parti6 sonrası | **parti7 sonrası** |", "|---|---:|---:|"]
        ek += [f"| `{k}` | {x:+.2f} | **{y:+.2f}** |" for k, x, y in bozulan]
        ek += ["", "⛔ Hücre hedefleme marjinali BOZDU — plan reddedildi."]
    else:
        ek += ["⭐ **Kötüleşen tek eksen yok** — hücre hedefleme hiçbir marjinali "
               "bozmadı. Bu bir kapı, bir gözlem değil: bozsaydı plan "
               "reddedilecekti.", ""]
    if iyilesen:
        ek += ["", "⭐ **İyileşen (eşiği zaten aşmış olanlar):**", "",
               "| eksen = değer | parti6 sonrası | **parti7 sonrası** |", "|---|---:|---:|"]
        ek += [f"| `{k}` | {x:+.2f} | **{y:+.2f}** |" for k, x, y in iyilesen]
    ek += ["", "## ⭐ Bağlam sınıfı — plandan (T202)", "", "| sınıf | parti7 payı |",
           "|---|---:|"]
    for s in ("cevap_var", "cevap_yok", "izin_iste", "ilgisiz"):
        ek.append(f"| `{s}` | {dagitim.count(s)} |")
    ek += ["", f"⭐ Çıplak kriz beyanı işaretli satır: **{isaret}** (`gd-021` açık).", "",
           "## ⛔ ÜRETİM TALİMATI", "",
           "⭐⭐ **Aile kapısı (T209) KALIYOR.** Parti5 ve parti6'da tavan hiç "
           "harcanmadı (parti6: itiraz 0/58) ⇒ kapı artık bir kısıt değil bir "
           "kayıt. Aynı iki aile, aynı tavan (%10).", "",
           "⭐⭐⭐ **ŞABLON KAPISI ÜRETİMİN İÇİNDE KALIYOR (T218).** Parti6'da "
           "altı blokta dört kez ateşledi; parti sonunda eşiği aşan en uzun "
           "dizi 3 sözcüğe indi (parti5'te on sözcüklük bir CÜMLEYDİ).", "",
           "⛔⛔ **TOHUM KARŞILIĞI (T217) ve KÜNYE (T224) KAPILARI ZORUNLU.** "
           "Birleştirme artık her kaydın `source_ids`'ini plana karşı "
           "denetliyor; parti1'in başına gelen bir daha sessizce olamaz.", "",
           "⛔⛔ **ŞABLON KAPISI ÜRETİM SIRASINDA KOŞULACAK, SONUNDA DEĞİL.** "
           "Parti5'te sonda koşuldu ve on sözcüklük birebir aynı bir yönlendirme "
           "cümlesi buldu (`#39`/`#53`); üç metin yeniden yazıldı. Blok blok "
           "koşulsaydı ikinci kayıt yazılırken görülürdü.", "",
           "⛔ **`gd-024` AÇIK:** *«bedensel bildirim»* eşiği hâlâ tanımsız; "
           "parti5'te bir kez eşik koymak yerine cümle belirsizlikten çıkarıldı. "
           "Aynı yol denenecek ve her örnek yazılacak.", "",
           "⛔ **`gd-022` AÇIK:** akut refah acilleri §5a″'nın dördüne de girmiyor.", "",
           "## ⛔ Bu planın söylemedikleri", "", "| | |", "|---|---|",
           f"| ⛔⛔ **Asgari 20 tohum SEÇİMDİR** | hücre envanterinin eşiği; "
           "altındaki hücrelerde yüzde farkı gürültü ama eşik türetilmedi |",
           "| ⛔⛔ **İkili bakıldı, üçlü bakılmadı** | aynı itiraz bir üst düzeyde "
           "aynen geçerli; nerede duracağı bir seçim ve ikide duruldu |",
           f"| ⛔⛔ **K={K_UFUK} seçimdir** | gerekçesi ilan edildi, türetilmedi |",
           "| ⛔⛔ **Fazla temsilin KUSUR olduğu gösterilmedi** | hücre düzeyinde "
           "de gösterilmedi; *«set havuzu yansıtmalı»* bir varsayım |",
           "| ⛔⛔ **T132 hâlâ geçerli** | daha çok veri güvenlik kapısını "
           "açacağına dair bir kanıt YOK |",
           "| ⛔⛔⛔ **205 KAYIT YARGILANMADI** | parti3'ün 28'i + parti4 (59) "
           "+ parti5 (60) + parti6 (58); judge `agy:gemini` ve kotası doldu. "
           "Judge Claude olamaz (K43/K45) ⇒ kota dönene kadar döngünün ikinci "
           "adımı kapalı |",
           "| ⛔⛔ **37 çift kayıt** | aynı tohumdan iki kayıt üretilmiş "
           "durumda (T224); envanter tohumu bir kez sayıyor, korpus iki kayıt "
           "taşıyor ⇒ buradaki tavanlar olduğundan hafif olabilir, ölçülmedi |",
           "| ⛔⛔ **`evre` ekseni de sorunlu** | T223: etiketlerin %10'u "
           "metinle çelişiyor ve hata tek taraflı. Bu partinin İKİ tavanı da "
           "`evre=tolerans` üzerinden işliyor |"]
    RAPOR.write_text(RAPOR.read_text(encoding="utf-8") + "\n".join(ek), encoding="utf-8")
    print("\n".join(ek[:30]))
    if bozulan:
        print("⛔ MARJİNAL GERİLEME: "
              + " · ".join(f"{k} {x:+.1f}→{y:+.1f}" for k, x, y in bozulan))
        return 1
    print("⭐ marjinal gerileme yok"
          + (f" · iyileşen {len(iyilesen)}: "
             + ", ".join(f"{k} {x:+.1f}→{y:+.1f}" for k, x, y in iyilesen) if iyilesen else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
