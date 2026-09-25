#!/usr/bin/env python3
"""v6-parti4 tasarım ızgarası — 60 kayıt. Üretimden ÖNCE yazılır, dondurulur.

⭐ Izgara çözücü ve hedefli sıralama PP1'den, azınlık dalı PP2'den, çoğunluk
dalı + bağlam dağıtımı + çıplak kriz işareti PP3'ten **çağrılır** (K97).

⛔⛔⛔ **PARTİ3'TEN YAPISAL FARK: KAÇINMA TERİMİ.** Kapsama envanteri dört
partidir `ph − pu ≥ ESIK` koşuluyla çalışıyordu — yani **yalnız EKSİK
temsili** görüyor. Eşik `-100`'e indirilip iki yöne bakılınca çıktı ki
59 eksen-değer çiftinin **24'ü FAZLA temsil ediliyor** ve en büyükleri kalan
eksiklerden büyük:

| fazla temsil | sette | havuzda | fark |
|---|---:|---:|---:|
| `profil=mavi_yakali` | %17.0 | %10.3 | **−6.7** |
| `evre=tolerans` | %52.7 | %46.4 | **−6.3** |
| `siddet_seviyesi=orta` | %68.7 | %63.6 | **−5.1** |
| `senaryo=belirsiz` | %28.2 | %23.7 | **−4.5** |
| `profil=beyaz_yakali` | %27.7 | %24.6 | **−3.2** |

➡️⭐⭐⭐ *Tek yönlü bir açık ölçüsü, dengesizliğin yarısını yapısal olarak
görmez — ve görmediği yarı, gördüğünden büyük olabilir.* T203 sabit bir
DIŞLAMANIN kör noktasını göstermişti; bu, ÖLÇÜNÜN kendisinin kör noktası.

⭐ Kaçınma: `fark ≤ −ESIK` olan sınıflar sıralamada **ceza** alır; ceza =
fazlalığın bu parti boyutundaki karşılığı (`|fark| × N/100` kayıt).
⛔ Izgara ekseni olanlar (`bagimlilik_turu`, `yas_grubu`) dışarıda: onları
kota ve ızgara zaten yönetiyor, ceza vermek ızgarayla çatışırdı.
⛔ Ceza AĞIRLIĞI seçimdir (fazlalığın kayıt karşılığı) — türetilmedi.

⭐ **Kalan tek eksik hedef `stres_tipi=yok` (+4.8, çoğunluk dalı → 45).**
`risk_seviyesi=orta` ve `profil=ev_kadini` parti3'ten sonra listeden düştü.

Girdi : reports/analiz/2026-09-20-kapsama-acigi-envanteri-parti1-3.json
        reports/analiz/2026-09-20-kapsama-acigi-envanteri-parti1-3-cift-yon.json
Çıktı : data/plan/v6-parti4.jsonl · reports/analiz/2026-09-20-v6-parti4-plan.md
"""
from __future__ import annotations

import json
import os
import random
from collections import Counter
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
N = 60
TOHUM = int(os.environ.get("BIRAG_PLAN_TOHUM", "20260923"))
CIKTI = KOK / "data/plan/v6-parti4.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-v6-parti4-plan.md"
ENVANTER = KOK / "reports/analiz/2026-09-20-kapsama-acigi-envanteri-parti1-3.json"
CIFT_YON = KOK / "reports/analiz/2026-09-20-kapsama-acigi-envanteri-parti1-3-cift-yon.json"
IZGARA_EKSENI = ("bagimlilik_turu", "yas_grubu")   # kota/ızgara yönetiyor


def _modul(ad: str, yol: str):
    sp = _iu.spec_from_file_location(ad, KOK / yol)
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


# ⛔⛔ MODÜL KİMLİĞİ TUZAĞI. İlk yazımda PP1/PP2'yi ayrıca yükledim; oysa PP3
# kendi içinde KENDİ PP1/PP2 örneğini yüklüyor. `PP2.ENVANTER = ...` benim
# kopyama yazdı, türetme PP3'ünkinden okudu ⇒ parti2 DÖNEMİNİN hedefleri
# (7 hedef) kullanıldı ve plan sorunsuzca üretildi.
# ➡️⭐ *Aynı betiği iki kez yüklemek iki ayrı DURUM yaratır; birine yazıp
#    ötekinden okumak sessizce eski değeri kullanır.*
# ⇒ Tek nesne grafiği: PP1 ve PP2, PP3'ün taşıdıkları.
PP3 = _modul("pp3", "scripts/analiz/2026-09-20-v6-parti3-plan.py")
PP1, PP2 = PP3.PP1, PP3.PP2
KRIZ = PP3.KRIZ

KACINMA: dict[tuple[str, str], float] = {}


def kacinmalari_turet() -> dict[tuple[str, str], float]:
    """Fazla temsil edilen sınıflar → ceza. ⛔ Ağırlık SEÇİMDİR.

    Ceza, fazlalığın **bu parti boyutundaki kayıt karşılığı**: bir sınıf
    havuzu 6.7 puan aşıyorsa, 60'lık bir partide 4 kayıt fazladan demektir.
    Böylece ceza ile ödül (kalan hedef sayısı) aynı birimde — ikisi de KAYIT.
    """
    env = json.loads(CIFT_YON.read_text(encoding="utf-8"))
    out: dict[tuple[str, str], float] = {}
    for anahtar, v in env["acik"].items():
        eksen, deger = anahtar.split("=", 1)
        if eksen in IZGARA_EKSENI or v["fark"] > -PP2.BUYUK_SINIF * 0 - 3.0:
            continue
        out[(eksen, deger)] = abs(v["fark"]) * N / 100
    return out


KOTA: dict[tuple[str, str], int] = {}
_ALINMIS: dict[str, dict] = {}


def _kota_kur() -> dict[tuple[str, str], int]:
    """Fazla temsil edilen sınıfın bu partideki TAVANI = havuz payı × N.

    ⛔⛔ İLK SÜRÜM SABİT CEZAYDI VE AŞIRI DÜZELTTİ. Ödül `kalan` ile azalıyor,
    ceza sabit kalıyordu ⇒ tek hedef tükenince ceza rakipsiz çalıştı ve
    `siddet_seviyesi=orta` havuzda %63.6 iken partide **%3** oldu, `tolerans`
    %46 iken %10. Yani set havuzu yansıtmıyor, TERSİNE çeviriyordu.
    ➡️⭐⭐ *Azalan bir ödüle sabit bir ceza eklemek, ceza küçük olsa bile
    sonunda tek başına karar verir; kaçınma bir YASAK değil bir TAVAN olmalı.*
    ⇒ Ceza yalnız kota AŞILDIKTAN sonra uygulanır.
    """
    cy = json.loads(CIFT_YON.read_text(encoding="utf-8"))
    return {k: round(cy["acik"][f"{k[0]}={k[1]}"]["havuz"] * N / 100) for k in KACINMA}


def _ihtiyac_sirasi(hav: list[dict], kalan: dict) -> list[dict]:
    """PP1'in sıralayıcısı + kota aşımına ceza. PP1 DEĞİŞTİRİLMEDİ (Kural 2)."""
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


def main() -> int:
    global KACINMA
    PP2.ENVANTER, PP2.N = ENVANTER, N
    PP3.ENVANTER, PP3.N = ENVANTER, N
    assert PP3.PP2 is PP2 and PP3.PP1 is PP1, "⛔ modül kimliği ayrıştı"
    hedef, cogunluk = PP3.hedefleri_turet()
    KACINMA = kacinmalari_turet()
    PP1.TOHUM_HEDEF.clear()
    PP1.TOHUM_HEDEF.update(hedef)
    global KOTA
    KOTA = _kota_kur()
    PP1._ihtiyac_sirasi = _ihtiyac_sirasi        # ⭐ tek enjeksiyon noktası
    # ⭐ Seçilenleri görmek için `P1.sec` sarmalanıyor: kota tüketimi ancak
    #    hangi tohumun alındığı bilinerek sayılabilir.
    _orij = PP1.P1.sec

    def _sec(s, h, alinmis):
        t = _orij(s, h, alinmis)
        if t is not None:
            _ALINMIS[t["seed_id"]] = t["meta"]
        return t
    PP1.P1.sec = _sec
    PP1._TURETILMIS = True
    PP1.CIKTI, PP1.RAPOR, PP1.TOHUM, PP1.N = CIKTI, RAPOR, TOHUM, N
    print(f"⭐ eksik hedefler ({len(hedef)}): " +
          ", ".join(f"{e}={d}→{n}" for (e, d), n in sorted(hedef.items(), key=lambda x: -x[1])))
    print(f"⛔ kaçınma ({len(KACINMA)}): " +
          ", ".join(f"{e}={d}→-{w:.1f}" for (e, d), w in
                    sorted(KACINMA.items(), key=lambda x: -x[1])))
    if (rc := PP1.main()):
        return rc

    # ── plana bağlam sınıfı ve çıplak kriz işareti (PP3'ün tanımlarıyla) ──
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

    # ── kaçınma tuttu mu: parti payı ↔ havuz payı ──
    cy = json.loads(CIFT_YON.read_text(encoding="utf-8"))
    ek = ["", "## ⛔⛔ Parti3'ten fark — KAÇINMA TERİMİ", "",
          "Kapsama envanteri dört partidir `ph − pu ≥ ESIK` ile çalışıyordu: **yalnız "
          "eksik temsili** görüyor. Eşik iki yöne açılınca 59 eksen-değer çiftinin "
          "**24'ü fazla temsil** çıktı ve en büyükleri kalan eksiklerden büyük.", "",
          "➡️⭐⭐⭐ *Tek yönlü bir açık ölçüsü, dengesizliğin yarısını yapısal olarak "
          "görmez — ve görmediği yarı, gördüğünden büyük olabilir.*", "",
          "| eksen = değer | havuz | set (önce) | **ceza** | **parti4 payı** |",
          "|---|---:|---:|---:|---:|"]
    ek[-2] = "| eksen = değer | havuz | set (önce) | **kota** | **parti4 payı** |"
    for (e, d), w in sorted(KACINMA.items(), key=lambda x: -x[1]):
        v = cy["acik"][f"{e}={d}"]
        pay = sum(1 for r in satir
                  if str((tohumlar.get(r["seed_id"], {}).get("meta") or {}).get(e)) == d)
        ek.append(f"| `{e}={d}` | %{v['havuz']} | %{v['sette']} | {KOTA[(e, d)]} | "
                  f"**{pay}** (%{100*pay/len(satir):.0f}) |")
    ek += ["", "⭐ Kaçınma bir **yasak değil tavan**: ceza yalnız kota aşıldıktan "
               "sonra uygulanır. ⛔⛔ İlk sürüm SABİT cezaydı ve aşırı düzeltti — "
               "`siddet_seviyesi=orta` havuzda %63.6 iken partide **%3**, `tolerans` "
               "%46 iken %10 olmuştu. ➡️ *Azalan bir ödüle sabit bir ceza eklemek, ceza "
               "küçük olsa bile sonunda tek başına karar verir.*", "",
           "⛔ **Kota ve ceza ağırlığı SEÇİMDİR:** kota = havuz payı × N; ceza = "
           f"`|fark| × {N}/100`. Ödül ile ceza aynı birimde (kayıt) olsun diye böyle "
           "kuruldu; yalnız YÖNLERİ türetildi.", "",
           "⛔ Izgara ekseni olanlar dışarıda tutuldu (`bagimlilik_turu`, `yas_grubu`): "
           "onları kota ve ızgara yönetiyor, ceza vermek ızgarayla çatışırdı.", "",
           "## ⭐ Bağlam sınıfı — plandan (T202)", "",
           "| sınıf | parti4 payı |", "|---|---:|"]
    for s in ("cevap_var", "cevap_yok", "izin_iste", "ilgisiz"):
        ek.append(f"| `{s}` | {dagitim.count(s)} |")
    ek += ["", f"⭐ Çıplak kriz beyanı işaretli satır: **{isaret}** (`gd-021` açık).", "",
           "## ⛔ ÜRETİM TALİMATI — bu kez KAPI olmalı, hatırlatma değil", "",
           "⛔⛔ **T205:** parti3'te ızgara sabitken (üç partide de 9 "
           "`nazikce_karsi_cikma` satırı) iki cümle ailesi patladı — itiraz %2→%8→%20, "
           "fark etme %3→%3→%18 — çünkü red ve özerklik biçimlerini çeşitlendirirken "
           "dikkatim oradaydı. ➡️ *Hatırlatma, dikkat kaymasına karşı işe yaramadı; "
           "parti3'ün talimatları da yazılıydı.* ⇒ Parti4'te aile sayımı **blok "
           "kapısına** girecek: her blok, o ana kadar üretilmiş bütün bloklardaki "
           "aile oranını ölçecek ve eşiği aşarsa **reddedecek**.", "",
           "⭐ **T206:** kapsama bir SÖZCÜK ölçüsü, şablon bir DİZİ ölçüsü. Kapsamanın "
           "yükselmesi tek başına şablonlaşma değil; karar dizi sayan kapıya ait.", "",
           "⭐ **T202:** `cevap_var`/`izin_iste` cümlelerinin biçimi kayıttan kayda "
           "değişecek; parti3'te bu elle yapıldı ve yazıldı.", "",
           "## ⛔ Bu planın söylemedikleri", "", "| | |", "|---|---|",
           "| ⛔⛔ **Kaçınma ağırlığı ve eşiği SEÇİLDİ** | yalnız yönü türetildi |",
           "| ⛔⛔ **T132 hâlâ geçerli** | daha çok veri güvenlik kapısını açacağına "
           "dair bir kanıt YOK |",
           "| ⛔ **Fazla temsilin KUSUR olduğu gösterilmedi** | envanterin varsayımı "
           "*«set havuzu yansıtmalı»*; havuzun kendisi bir tasarım ürünü ve onun "
           "doğruluğu ayrı bir soru |",
           "| ⛔ **`gd-021` KARARI VERİLMEDİ** | çıplak sınıf işaretlendi, "
           "sınıflandırılmadı |"]
    RAPOR.write_text(RAPOR.read_text(encoding="utf-8") + "\n".join(ek), encoding="utf-8")
    print("\n".join(ek[:22]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
