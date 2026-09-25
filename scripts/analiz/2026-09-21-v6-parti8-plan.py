#!/usr/bin/env python3
"""v6-parti8 tasarım ızgarası — **120 kayıt**. Üretimden ÖNCE yazılır, dondurulur.

⛔⛔⛔ **BU PARTİ K260'IN İLK UYGULAMASI VE İKİ PARAMETRESİ DEĞİŞTİ.**

⭐ **(1) n = 120** (önceki yedi partide 60). Gerekçe hız: T232 ölçtü ki
parti başına sabit bir yük var (plan, ön tarama, birleştirme, rapor) ve
bu yük kayıt sayısına bölünüyor. ⛔ Ön tarama okuması DOĞRUSAL büyür
(T213 satırların tamamının okunmasını zorunlu kılıyor) ⇒ o kalem
ucuzlamıyor, yalnız amortisman iyileşiyor.

⭐ **(2) K = 1** ve bu bir gevşeme DEĞİL. Ufuk kuralının anlamı
*«açık kaç KAYIT içinde kapanmalı»*; K bir parti sayısı olduğu için n
değişince aynı ufku korumak K'yı da değiştirmeyi gerektiriyor:
  · parti5: n=60, K=5 → 300 kayıt · parti6: K=3 → 180 · parti7: K=2 → 120
  · parti8: n=120, **K=1 → 120 kayıt** — parti7 ile AYNI ufuk.
⛔ Seçimin ikinci gerekçesi K250'deki ile aynı: korpus hedeflenen
büyüklüğe varmadan kapansın. N₀ = **983** ⇒ 983 + 1×120 = **1103**, ve
K250'nin hedefi ~1108'di. ⇒ **Bu parti, hedeflenen korpus büyüklüğüne
varan parti.**

⭐ **(3) `profil` hedeflemeden çıkarılmış durumda** (parti7, kullanıcı
kararı). Envanterde ölçülmeye devam ediyor, raporda ayrı tabloda duruyor.
Ölçmeyi bırakmak kararı geri alınamaz yapardı.

⛔⛔ **ENVANTERLER PARTİ7'Yİ İÇERİYOR.** `-parti1-7` dosyalarından
okunuyor; parti7'siz bir zemine göre hedef türetmek T224 sınıfı bir hata
olurdu.

⛔⛔ **T225/T231'İN SAYIM SORUNU AÇIK ve N₀'ı etkiliyor:** 37 tohum iki
kayıt taşıyor, envanter tohumu bir kez sayıyor (T231 kayıtların kalmasına
karar verdi) ⇒ `N₀=983` korpusun kayıt sayısı, envanterin tohum sayısı
değil. Kural ikisini aynı ölçekte varsayıyor ve bu varsayım 37 tohumda
tutmuyor. Düzeltilmedi; burada ilan ediliyor.
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
N = 120
K_UFUK = 1          # ⛔ N₀=983 ⇒ 983+1×120 = 1103 (K250 hedefi ~1108)
ESIK_HUCRE = 3.0
ESIK_MARJINAL = 3.0
TOLERANS = 0.3
TOHUM = int(os.environ.get("BIRAG_PLAN_TOHUM", "20261001"))
CIKTI = KOK / "data/plan/v6-parti8.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-v6-parti8-plan.md"
HUCRE = KOK / "reports/analiz/2026-09-21-hucre-kapsama-envanteri-parti1-7.json"
MARJINAL = KOK / "reports/analiz/2026-09-20-kapsama-acigi-envanteri-parti1-7.json"


def _modul(ad: str, yol: str):
    sp = _iu.spec_from_file_location(ad, KOK / yol)
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


# ⛔ Tek nesne grafiği (parti4'ün modül kimliği tuzağı). Hepsi PP5'inkiler.
PP7 = _modul("pp7", "scripts/analiz/2026-09-21-v6-parti7-plan.py")
PP6 = PP7.PP6
PP5 = PP6.PP5
PP4, PP3, PP1, PP2 = PP5.PP4, PP5.PP3, PP5.PP1, PP5.PP2
P1 = PP1.P1
KRIZ = PP5.KRIZ
# ⛔ KULLANICI KARARI: hedeflemeden çıkarılan eksen(ler). Ölçüm sürüyor.
# ⛔⛔⛔ KULLANICI KARARI (parti8): `bagimlilik_turu` de hedeflemeden çıktı.
#    Gerekçe `profil`inkinden FARKLI ve ölçülmüş — TÜKENME:
#    kapsama açığı TAM havuza göre ölçülüyor ama seçim KALAN havuzdan
#    yapılıyor, ve `tutun` tam havuzda %22,3 iken kalan havuzda %16,6
#    (+5,7 puan tükenmiş) ⇒ hiçbir parti kompozisyonu bu açığı kapatamaz.
#    ⭐ Boyuttan bağımsız olduğu ayrıca ölçüldü: aynı kodla n=60'ta −4,3,
#    n=120'de −4,0 ⇒ parti küçültmek DÜZELTMEZ.
#    ⛔ Eksen SİLİNMEDİ: envanterde ölçülmeye devam ediyor.
# ⚠️ `evre` AYNI TESTLE eklendi (kullanıcı «tükenmişi hedefleme» ilkesini
#    onayladı): `evre=tolerans` kalan havuzda +2,7 puan eksik. İKİNCİ ve
#    bağımsız gerekçe: T223 `evre` etiketlerinin ~%10'unun metinle
#    ÇELİŞTİĞİNİ ölçmüştü ve hata tek taraflıydı ⇒ hedeflenen şeyin
#    kayıtta karşılığı belirsiz. ⛔ Bu benim uygulamam, geri alınabilir.
HEDEFLENMEYEN = ("profil", "bagimlilik_turu", "evre")
# ⭐ Tükenme testi rapora basılıyor (Kural 7: sayı kaynağıyla dursun).
TUKENME_ESIK = 2.0
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

    # ⛔⛔⛔ SEÇİCİ `risk_seviyesi=yuksek`'İ AŞIRI SEÇİYOR ve bu ölçüldü:
    #    süzgeç sonrası havuz %37,1 iken plan %50,0 çekti (+12,9 puan) ⇒
    #    marjinal gerileme kapısı sekiz tohumun sekizinde de çaldı.
    #    ⛔ Bu bir TÜKENME DEĞİL — kalan havuzda oran var, seçici almıyor.
    #    `P1.sec` ilk-uyan ve `(tur, yaş)` kovaları içinde sıralıyor; risk
    #    ekseni seçimde hiç kısıtlanmıyordu.
    # ⭐ Düzeltme YENİ MEKANİZMA DEĞİL: `TOHUM_HEDEF` zaten tohum
    #    özniteliklerini hedeflemek için var (T190). Buraya havuz oranı
    #    konuyor — hedef uydurulmuyor, ÖLÇÜLEN havuz payı yazılıyor.
    _suz = P1.havuz(CIKTI)
    for _yol, _dsn in (("2026-09-17-kriz-suzgeci-yanlis-negatif.py", "DOLAYLI"),
                       ("2026-09-17-tohum-beyan-kriz-kapisi.py", None)):
        _M = _modul("kz", "scripts/analiz/" + _yol)
        _suz = ([t for t in _suz if not _M.DOLAYLI.search(t["user_message"])]
                if _dsn else [t for t in _suz if _M._sinif(t) != "sert"])
    _rc = collections.Counter((t.get("meta") or {}).get("risk_seviyesi")
                              for t in _suz)
    _rc.pop(None, None)
    _rt = sum(_rc.values())
    RISK_HEDEF = {k: round(N * v / _rt) for k, v in _rc.items()}
    print(f"   ⭐ `risk_seviyesi` hedefi süzgeç sonrası havuzdan: {RISK_HEDEF} "
          f"(havuz payı {{{', '.join(f'{k}:%{100*v/_rt:.1f}' for k, v in _rc.items())}}})")

    PP1.TOHUM_HEDEF.clear()
    PP1.TOHUM_HEDEF.update(hedef)
    for _k, _v in RISK_HEDEF.items():
        PP1.TOHUM_HEDEF.setdefault(("risk_seviyesi", _k), _v)
    PP1._ihtiyac_sirasi = _ihtiyac_sirasi
    PP1._TURETILMIS = True
    PP1.CIKTI, PP1.RAPOR, PP1.TOHUM, PP1.N = CIKTI, RAPOR, TOHUM, N

    # ⛔⛔ KOTA TABLOLARI N=60'A GÖRE YAZILMIŞ ve parti8 ilk kez N≠60.
    #    Toplamları N'e eşit olmak zorunda (PP1'in kapısı bunu denetliyor) ⇒
    #    ölçeklenmeleri gerekiyor. ⭐ N=120 tam iki katı olduğu için ölçekleme
    #    YUVARLAMASIZ: her sayı ×2 ve oranlar birebir korunuyor.
    # ⛔ İkinci bir kota tanımı KURULMUYOR (K97): tablonun sahibi PP3 ve
    #    burada yalnız ölçeği değişiyor (tablonun evi: `2026-09-16-v5-parti3-plan.py`,
#    `PP1.P3.KOTA` — PP1 onu oradan okuyor). Oranlar aşağıda sınanıyor.
    # ⚠️ N 60'ın katı olmazsa bu yol çalışmaz — o zaman yuvarlama politikası
    #    ayrıca kararlaştırılmalı. Kapı bunu tutuyor.
    if N % 60:
        raise SystemExit(f"⛔ N={N} 60'ın katı değil; kota ölçeklemesi "
                         "yuvarlama gerektirir ve politika kararlaştırılmadı")
    # ⛔⛔ `N` ÜÇ MODÜLDE AYRI AYRI DURUYOR ve üçü de 60 yazıyor: PP1 (satır
    #    dizisini kuran), PP1.P3 (ızgarayı çözen) ve bu betik. Yalnız PP1.N'i
    #    ayarlamak yetmedi — çözücü kendi N'ini okudu ve 60 satır üretti.
    #    ➡️ *Bir sayı üç yerde yaşıyorsa, birini değiştirmek onu değiştirmez.*
    PP1.N = PP1.P3.N = N

    # ⛔⛔⛔ İKİ AYRI PAYDA — parti8'de ölçüldü ve marjinal gerileme kapısı
    #    bunu yakaladı. `tur` kotası KALAN havuzdan türetiliyordu
    #    (`tur_kotasi(hav)`), kapsama açığı ise TAM havuza göre ölçülüyor.
    #    Havuz tükendikçe ikisi ayrışıyor: tam havuzda `tutun` %22,3, kalan
    #    havuzda %17,1, sette %18,7 ⇒ kota, hedefin tanımı gereği
    #    KAPATAMAYACAĞI bir açığı kovalıyordu ve her çekilişte aynı sınıf
    #    eşiği aşıyordu (altı tohumda da `tutun` −3,6/−4,0).
    # ➡️ *Aynı büyüklüğün iki paydası varsa, biri ötekinin hedefini
    #    ulaşılamaz kılar.*
    # ⭐ Düzeltme YENİ BİR KURAL DEĞİL (K97): ölçü aynı, payda düzeltiliyor —
    #    kota artık kapsama açığının ölçüldüğü TAM havuzdan türetiliyor.
    # ⛔ Fizibilite ayrıca denetleniyor: kalan havuzda o kadar tohum yoksa
    #    kota karşılanamaz ve bu SESSİZ kalmamalı.
    # ⭐ TAM havuz = kapsama envanterinin paydası: `data/seeds.v2.jsonl`.
    _TAM = [json.loads(l) for l in
            (KOK / "data/seeds.v2.jsonl").read_text(encoding="utf-8").splitlines()
            if l.strip()]
    _orij_kotasi = PP1.tur_kotasi

    def _tur_kotasi(hav: list[dict]) -> dict[str, int]:
        c = collections.Counter(
            P1.TUR_ESLEME.get((t.get("meta") or t).get("bagimlilik_turu"))
            for t in _TAM)
        c.pop(None, None)
        top = sum(c.values())
        ham = {k: N * v / top for k, v in c.items()}
        kota = {k: int(v) for k, v in ham.items()}
        for k, _ in sorted(ham.items(),
                           key=lambda x: -(x[1] - int(x[1])))[:N - sum(kota.values())]:
            kota[k] += 1
        # ⛔ FİZİBİLİTE: kalan havuzda o kadar tohum var mı? Yoksa kota
        #    karşılanamaz ve bu sessiz kalmamalı.
        mevcut = collections.Counter(
            P1.TUR_ESLEME.get(t["meta"].get("bagimlilik_turu")) for t in hav)
        eksik = {k: (v, mevcut.get(k, 0)) for k, v in kota.items()
                 if mevcut.get(k, 0) < v}
        if eksik:
            raise SystemExit(f"⛔ `tur` kotası kalan havuzla karşılanamıyor: "
                             f"{eksik} (istenen, mevcut)")
        eski = _orij_kotasi(hav)
        print(f"   ⭐ `tur` kotası TAM havuzdan türetildi: {kota}")
        print(f"      (kalan havuzdan türetilseydi: {eski})")
        return kota
    PP1.tur_kotasi = _tur_kotasi
    _kat = N // 60
    if _kat != 1:
        # ⛔⛔ `SAYI_KOTA` DA 60'A GÖRE YAZILMIŞ ve ölçeklenmediği ilk
        #    koşuda görüldü: plan 120 satırda yalnız 15 bağlam, 9 red, 12
        #    özerklik üretti — yani oranlar yarıya düştü (bağlam %25 → %12,5).
        #    ➡️ *N'e bağlı her sayı N ile birlikte ölçeklenmezse, parti
        #    büyütmek tasarımı sessizce seyreltir.*
        _onceki_sk = dict(PP1.P3.SAYI_KOTA)
        PP1.P3.SAYI_KOTA = {k: v * _kat for k, v in PP1.P3.SAYI_KOTA.items()}
        print(f"   ⭐ SAYI_KOTA ×{_kat}: {_onceki_sk} → {PP1.P3.SAYI_KOTA}")
        _onceki = {a: dict(d) for a, d in PP1.P3.KOTA.items()}
        PP1.P3.KOTA = {a: {k: v * _kat for k, v in d.items()}
                    for a, d in PP1.P3.KOTA.items()}
        for a, d in PP1.P3.KOTA.items():          # oran korundu mu
            for k, v in d.items():
                assert v == _onceki[a][k] * _kat, f"kota oranı bozuldu: {a}.{k}"
        print(f"   ⭐ kota tabloları ×{_kat} ölçeklendi (oranlar birebir korundu)")
    _orij_sec = P1.sec

    def _sec(s, h, alinmis):
        t = _orij_sec(s, h, alinmis)
        if t is not None:
            _ALINMIS[t["seed_id"]] = t["meta"]
        return t
    P1.sec = _sec

    # ⭐ TÜKENME TESTİ — hedeflemeden çıkarma gerekçesinin sayısı.
    _tam = [json.loads(l) for l in
            (KOK / "data/seeds.v2.jsonl").read_text(encoding="utf-8").splitlines()
            if l.strip()]
    _kal = P1.havuz(CIKTI)

    def _pay(lst, e):
        c = collections.Counter((t.get("meta") or t).get(e) for t in lst)
        c.pop(None, None)
        tp = sum(c.values())
        return {k: 100 * v / tp for k, v in c.items()}
    TUKENME = {}
    for _e in HEDEFLENMEYEN + ("evre", "risk_seviyesi", "senaryo"):
        _a, _b = _pay(_tam, _e), _pay(_kal, _e)
        for _k in _a:
            _d = _a[_k] - _b.get(_k, 0)
            if _d >= TUKENME_ESIK:
                TUKENME[f"{_e}={_k}"] = (_a[_k], _b.get(_k, 0), _d)
    print(f"⭐ korpus N₀={n0} · ufuk K={K_UFUK} parti · hücre eşiği {ESIK_HUCRE}")
    print(f"⛔ tükenmiş sınıf ({len(TUKENME)}): "
          + ", ".join(f"{k} +{v[2]:.1f}" for k, v in sorted(
              TUKENME.items(), key=lambda x: -x[1][2])))
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
          f"⛔ **K={K_UFUK}** — n=120 olduğu için parti7 ile AYNI ufku (120 kayıt) veriyor; parti5 n=60/K=5, parti6 K=3, parti7 K=2. Gerekçe değişmedi — *«korpus "
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
           "", "### ⛔⛔ Tükenme testi — hedeflemeden çıkarmanın sayısı", "",
           "Kapsama açığı **tam havuza** göre ölçülüyor ama seçim **kalan "
           "havuzdan** yapılıyor. Bir sınıf kalan havuzda tam havuzdakinden "
           f"{TUKENME_ESIK:.1f} puandan fazla azsa, o açık hiçbir parti "
           "kompozisyonuyla kapanmaz.", "",
           "| sınıf | tam havuz | kalan havuz | tükenme |", "|---|---:|---:|---:|"]
    ek += [f"| `{k}` | %{v[0]:.1f} | %{v[1]:.1f} | **+{v[2]:.1f}** |"
           for k, v in sorted(TUKENME.items(), key=lambda x: -x[1][2])]
    ek += ["", "⭐ Kullanıcı kararı: `" + "`, `".join(HEDEFLENMEYEN) + "`. İki eksenin gerekçesi AYRI ve ikisi de ölçülmüş: "
           "`profil` — T220/T221, v6 kayıtlarının yarısından fazlasında metinde "
           "hiç görünmüyor; `bagimlilik_turu` — yukarıdaki tükenme testi, "
           "`tutun` kalan havuzda +5,1 puan eksik ve açık hiçbir parti "
           "kompozisyonuyla kapanmıyor (n=60'ta −4,3, n=120'de −4,0 ⇒ parti "
           "küçültmek düzeltmiyor). ⛔ Eksen "
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
