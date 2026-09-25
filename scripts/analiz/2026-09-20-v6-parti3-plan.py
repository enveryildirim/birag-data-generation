#!/usr/bin/env python3
"""v6-parti3 tasarım ızgarası — 60 kayıt. Üretimden ÖNCE yazılır, dondurulur.

⭐ Izgara çözücü, hücre yasakları, kriz süzgeçleri ve hedefli tohum sıralaması
`2026-09-20-v6-parti1-plan.py` (PP1) üzerinden **çağrılır** (K97). Hedef türetme
kuralı parti2'den (PP2) devralınır — yeniden yazılmaz.

⛔⛔ **PARTİ2'DEN İKİ YAPISAL FARK:**

**1. `baglam_davranisi` artık PLANDA.** Parti2'de sınıf üretim anında kayıt
kayıt seçiliyordu ve 15 bağlam kaydının **13'ü `cevap_var`** çıktı (%87; hedef
%50) — T197'nin *«soruyu pasaja göre tasarla»* talimatını tek biçimde
uygulamışım (T202). ➡️ *Bir dağılım hedefi üretim anında kayıt kayıt
tutturulamaz; üretim anında görünen tek şey o kayıttır.*
⭐ Sınıflar **seçilmiyor, türetiliyor**: kümülatif korpusun (`v0.0.14` + parti1
+ parti2) §7a hedefine olan uzaklığını en çok azaltan dağıtım, açgözlü
ayrımla. Sayım `2026-09-20-v6-parti2-birlestir.baglam_sayimi()`ten gelir (K97).

**2. Çıplak kriz beyanı satır düzeyinde İŞARETLENİR.** T199 adsız bir sınıf
buldu: `esdurumlar`'da nitelenmemiş *«İntihar düşüncesi»* — SERT'e de
PERSONA'ya da girmiyor ve `gd-021` uzman kaleminde bekliyor. Parti1 bu sınıftan
3 kayıt üretti, parti2'de `#54` üretilmedi. ⛔ Ne sessizce üretilir ne sessizce
elenir: plana `beyan_ciplak_kriz` alanı yazılır ve üretim o satırın **mesajını
okumadan** yazmaz. ⭐ T199'un sayıları (SERT/PERSONA/ÇIPLAK) bu betikte ilk kez
**yeniden koşulabilir** hâle geliyor — ölçüm yapılmıştı, betiği yoktu (Kural 7).

Girdi : reports/analiz/2026-09-20-kapsama-acigi-envanteri-parti1-2.json
Çıktı : data/plan/v6-parti3.jsonl · reports/analiz/2026-09-20-v6-parti3-plan.md
"""
from __future__ import annotations

import json
import os
import random
import sys
from collections import Counter
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
sys.path.insert(0, str(KOK / "src"))
N = 60
TOHUM = int(os.environ.get("BIRAG_PLAN_TOHUM", "20260922"))
CIKTI = KOK / "data/plan/v6-parti3.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-v6-parti3-plan.md"
ENVANTER = KOK / "reports/analiz/2026-09-20-kapsama-acigi-envanteri-parti1-2.json"
# §7a hedef payları — v4 §7a (tasarım kararı, literatür değil).
HEDEF_CTX = {"cevap_var": 0.50, "cevap_yok": 0.25, "izin_iste": 0.12, "ilgisiz": 0.12}


def _modul(ad: str, yol: str):
    sp = _iu.spec_from_file_location(ad, KOK / yol)
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


PP1 = _modul("pp1", "scripts/analiz/2026-09-20-v6-parti1-plan.py")
PP2 = _modul("pp2", "scripts/analiz/2026-09-20-v6-parti2-plan.py")
BIR = _modul("bir", "scripts/analiz/2026-09-20-v6-parti2-birlestir.py")
KRIZ = _modul("kriz", "scripts/analiz/2026-09-17-tohum-beyan-kriz-kapisi.py")


def hedefleri_turet() -> dict[tuple[str, str], int]:
    """PP2'nin kuralı + **çoğunluk dalı**. Kural yeniden yazılmadı, TAMAMLANDI.

    ⛔⛔ PP2'nin kuralı `min(havuz_payı × 2, %40) × N` ve çoğunluk sınıflarını
    (`havuz ≥ %40`) **atlıyor**. Atlama yerindeydi: %75'lik bir sınıfa %40 hedef
    koymak onu YÜKSELTMEZ, düşürür — formül orada tanımsız. Ama iki parti sonra
    azınlık açıkları kapandı ve geriye **yalnız çoğunluk açıkları** kaldı:
    `stres_tipi=yok` +6.0 · `risk_seviyesi=orta` +4.4 (üstelik +4.0'dan BÜYÜDÜ).
    ⇒ Kural, kalan tek açık türünü yapısal olarak göremiyordu.

    ➡️⭐ *T198'in dersinin aynadaki hâli: ölçümden türetilmeyen bir hedef listesi
    kapanmış açığı kovalar; SABİT DIŞLAMASI olan bir türetme kuralı da açılan
    açığı hiç görmez.*

    ⭐ Çoğunluk dalı: hedef = `havuz_payı × N` (**parite**) — çarpan yok, tavan
    yok; ikisi de azınlığı yukarı çekmek için vardı ve burada ters çalışır.
    ⛔ Bu dal SEÇİMDİR, türetilmemiştir — PP2'nin çarpanı ve tavanı gibi.
    """
    hedef = PP2.hedefleri_turet()          # azınlık dalı — DEĞİŞMEDİ
    env = json.loads(ENVANTER.read_text(encoding="utf-8"))
    cogunluk: dict[tuple[str, str], int] = {}
    for anahtar, v in env["acik"].items():
        eksen, deger = anahtar.split("=", 1)
        if eksen == "bagimlilik_turu" or v["havuz"] < PP2.BUYUK_SINIF:
            continue
        cogunluk[(eksen, deger)] = round(N * v["havuz"] / 100)
    hedef.update(cogunluk)
    return hedef, cogunluk


def ciplak_kriz(d: dict) -> bool:
    """T199'un adsız sınıfı: PERSONA deseni tutuyor ama nitelenmemiş.

    ⛔ Bu bir SINIFLANDIRMA değil, bir İŞARET. Hangi sınıfa ait olduğu
    (`gd-021`) klinik/etik bir karardır ve verilmedi (Kural 3).
    ⭐ SERT ve PERSONA tanımları kapının kendisinden gelir (K97).
    """
    if KRIZ._sinif(d) != "persona":
        return False
    es = ((d.get("meta", {}) or {}).get("notlar", {}) or {}).get("esdurumlar") or []
    # nitelenmiş olanlar («… olası», «… sinyali») çıplak DEĞİLDİR
    return any(KRIZ.PERSONA.search(e) and not any(
        k in e.lower() for k in ("olası", "olasi", "sinyal", "riski")) for e in es)


def baglam_paylari(n_ctx: int) -> list[str]:
    """§7a sınıflarını kümülatif açığa göre dağıt — SEÇİM DEĞİL, TÜRETME.

    Her adımda, o sınıfa bir kayıt daha eklendiğinde kümülatif oranı hedefe en
    çok yaklaştıran sınıf seçilir. ⛔ Sınıf dışı değerler (`cevapla`,
    `yetersiz`) hedefsizdir ve paydaya girmez.
    """
    sayim = BIR.baglam_sayimi()
    var = Counter()
    for c in sayim.values():
        var += Counter({k: v for k, v in c.items() if k in HEDEF_CTX})
    toplam = sum(var.values())
    dagitim: list[str] = []
    for i in range(n_ctx):
        t = toplam + i + 1
        # en büyük eksiği olan sınıf: hedefin gerektirdiği sayı eksi eldeki
        sinif = max(HEDEF_CTX, key=lambda s: (HEDEF_CTX[s] * t - var[s], s))
        var[sinif] += 1
        dagitim.append(sinif)
    return dagitim


def main() -> int:
    # ── 1. hedefler: PP2'nin türetme kuralı, YENİ envanterle ───────────────
    PP2.ENVANTER = ENVANTER
    PP2.N = N
    hedef, cogunluk = hedefleri_turet()
    PP1.TOHUM_HEDEF.clear()
    PP1.TOHUM_HEDEF.update(hedef)
    PP1._TURETILMIS = True
    PP1.CIKTI, PP1.RAPOR, PP1.TOHUM, PP1.N = CIKTI, RAPOR, TOHUM, N
    print(f"⭐ ölçümden türetilen hedefler ({len(hedef)}):")
    for (e, d), n in sorted(hedef.items(), key=lambda x: -x[1]):
        print(f"   {e}={d:18s} {n:2d}")
    if (rc := PP1.main()):
        return rc

    # ── 2. plana `baglam_davranisi` ve `beyan_ciplak_kriz` yaz ─────────────
    satir = [json.loads(l) for l in CIKTI.read_text(encoding="utf-8").splitlines() if l.strip()]
    ctx = [r for r in satir if r["context"]]
    dagitim = baglam_paylari(len(ctx))
    # ⭐ hangi satıra hangi sınıf: sıra etkisini kırmak için partinin tohumuyla
    # karıştırılır (PP1'in atama karıştırmasıyla aynı gerekçe).
    random.Random(TOHUM).shuffle(dagitim)
    for r, s in zip(sorted(ctx, key=lambda r: r["sira"]), dagitim):
        r["baglam_davranisi"] = s

    tohumlar = KRIZ._tohumlar()
    isaret = 0
    for r in satir:
        d = tohumlar.get(r["seed_id"])
        if d and ciplak_kriz(d):
            r["beyan_ciplak_kriz"] = True
            isaret += 1
    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in satir),
                     encoding="utf-8")

    # ── 3. T199'un sayıları — ilk kez yeniden koşulabilir ──────────────────
    # ⛔ `_sinif` SERT'i iki ayrı sinyalden kuruyor; T199'un «SERT 20»i yalnız
    # BEYAN sinyalini saymıştı. Tek sayı ikisini gizler ⇒ ayrıştırılıyor.
    sinif_sayim = Counter()
    for d in tohumlar.values():
        s = KRIZ._sinif(d)
        sinif_sayim["ciplak" if ciplak_kriz(d) else s or "yok"] += 1
    _es = lambda d: ((d.get("meta", {}) or {}).get("notlar", {}) or {}).get("esdurumlar") or []
    _beyan = {sid for sid, d in tohumlar.items() if any(KRIZ.SERT.search(e) for e in _es(d))}
    _risk = {sid for sid, d in tohumlar.items()
             if (d.get("meta", {}) or {}).get("risk_seviyesi") == "cok_yuksek"}
    havuz_ciplak = sum(1 for t in PP1.P1.havuz()
                       if ciplak_kriz(tohumlar.get(t["seed_id"], {})))

    # ── 4. rapor eki ───────────────────────────────────────────────────────
    sayim = BIR.baglam_sayimi()
    mev = Counter()
    for c in sayim.values():
        mev += Counter({k: v for k, v in c.items() if k in HEDEF_CTX})
    yeni = mev + Counter(dagitim)
    ek = ["", "## ⛔⛔ Parti2'den fark 0 — türetme kuralının ÇOĞUNLUK DALI", "",
          "İki hedefli partiden sonra azınlık açıkları kapandı ve geriye **yalnız "
          "çoğunluk açıkları** kaldı. PP2'nin kuralı (`min(havuz×2, %40)`) onları "
          "atlıyordu ve atlama yerindeydi — %75'lik bir sınıfa %40 hedef koymak onu "
          "düşürür. ⛔ Ama sonuç, kuralın **kalan tek açık türünü yapısal olarak "
          "görememesiydi**: bu envanterde yalnız `profil=ev_kadini` hedeflenebiliyordu.", "",
          "➡️⭐ *T198'in dersinin aynadaki hâli: ölçümden türetilmeyen bir hedef "
          "listesi kapanmış açığı kovalar; SABİT DIŞLAMASI olan bir türetme kuralı da "
          "açılan açığı hiç görmez.*", "",
          "⭐ Çoğunluk dalı: hedef = `havuz_payı × N` (**parite**) — çarpan ve tavan "
          "yok, ikisi de azınlığı yukarı çekmek içindi. ⛔ Bu dal **seçimdir**.", "",
          "| eksen = değer | havuz payı | set payı | fark | **hedef** |",
          "|---|---:|---:|---:|---:|"]
    _env = json.loads(ENVANTER.read_text(encoding="utf-8"))
    for (e, d), n in sorted(cogunluk.items(), key=lambda x: -x[1]):
        v = _env["acik"][f"{e}={d}"]
        ek.append(f"| `{e}={d}` | %{v['havuz']:.1f} | %{v['sette']:.1f} | "
                  f"+{v['fark']:.1f} | **{n}** |")
    ek += ["", "⚠️ **`stres_tipi=yok` için parite doğru amaç mı, ölçülmedi.** Envanterin varsayımı *«set havuzu yansıtmalı»*; ama adlandırılmış stres tipleri "
          "(`kronik_agri`, `yalnizlik`) daha zengin senaryolar olabilir ve setin onları "
          "havuzun üstünde taşıması bir kusur olmayabilir. Kural **tutarlı** "
          "uygulandı; itiraz buraya yazıldı.", ""]
    ek += ["", "## ⭐⭐ Parti2'den fark 1 — `baglam_davranisi` artık PLANDA", "",
          "⛔ Parti2'de sınıf üretim anında seçiliyordu: 15 bağlam kaydının **13'ü** "
          "`cevap_var` çıktı (%87, hedef %50). ➡️ *Bir dağılım hedefi üretim anında "
          "kayıt kayıt tutturulamaz; üretim anında görünen tek şey o kayıttır.* (T202)", "",
          f"⭐ **Seçilmedi, türetildi:** her slot, kümülatif oranı §7a hedefine en çok "
          f"yaklaştıran sınıfa verildi. Parti3'ün **{len(ctx)}** bağlam satırı:", "",
          "| sınıf | korpusta | **parti3 payı** | sonra | hedef |", "|---|---:|---:|---:|---:|"]
    t_mev, t_yeni = sum(mev.values()), sum(yeni.values())
    for s in ("cevap_var", "cevap_yok", "izin_iste", "ilgisiz"):
        ek.append(f"| `{s}` | {mev[s]} (%{100*mev[s]/t_mev:.0f}) | **{dagitim.count(s)}** "
                  f"| {yeni[s]} (%{100*yeni[s]/t_yeni:.0f}) | %{100*HEDEF_CTX[s]:.0f} |")
    ek += ["", "## ⛔⛔ Fark 2 — çıplak kriz beyanı satır düzeyinde işaretlendi", "",
           "T199 adsız bir sınıf bulmuştu: `esdurumlar`'da **nitelenmemiş** "
           "*«İntihar düşüncesi»* — ne SERT ne PERSONA. `gd-021` uzman kaleminde. "
           "⛔ Ne sessizce üretilir ne sessizce elenir.", "",
           "| tohum sınıfı | sayı |", "|---|---:|",
           f"| SERT — toplam (`_sinif`) | {sinif_sayim['sert']} |",
           f"| — `esdurumlar`'da *«Aktif intihar …»* | {len(_beyan)} |",
           f"| — `risk_seviyesi=cok_yuksek` | {len(_risk)} |",
           f"| ⛔⛔ — **ikisi birden** | **{len(_beyan & _risk)}** |",
           f"| PERSONA (nitelenmiş) | {sinif_sayim['persona']} |",
           f"| ⛔ **ÇIPLAK (adsız)** | **{sinif_sayim['ciplak']}** |", "",
           "⭐⭐ **Kesişim SIFIR.** Beyan metninde *«Aktif intihar»* yazan tohumların "
           f"hiçbiri `cok_yuksek` değil, {len(_risk)} `cok_yuksek` tohumun hiçbirinde de "
           "o metin yok. ➡️ *Aynı şeyi gösterdiği varsayılan iki alan hiç birlikte "
           "görünmüyorsa, ikisi aynı şeyi göstermiyordur — ve yalnız birine bakan bir "
           "kapı sınıfın yarısını kaçırır.* ⛔ `_sinif` ikisini VEYA ile birleştirdiği "
           "için kapı bu tuzağa düşmüyor; ama T199'un *«SERT 20»*i yalnız beyan "
           f"sinyalini saymıştı — bu tablodaki {sinif_sayim['sert']} onunla aynı sayı "
           "**değildir**, aynı şeyin iki parçasıdır.", "",
           f"⭐ Parti3 planında bu sınıftan **{isaret}** satır var. ⚠️ Havuzda "
           f"**{havuz_ciplak}** çıplak tohum bulunuyordu ve hiçbiri bu 60'lık çekilişe "
           "düşmedi ⇒ `beyan_ciplak_kriz` alanı **yazılı ama bu partide denenmemiş** "
           "durumda. ⛔ Düşselerdi: **üretim mesajı okumadan yazmayacaktı** — `#54`'te "
           "elenmeyi sağlayan şey sınıf değil mesajdı (*«dönecek yerim yok, siz de "
           "yardım edemezsiniz»*).", "",
           "⭐ T199 bu sayıları ölçmüştü ama **betiği yoktu**; burada ilk kez yeniden "
           "koşulabilir (Kural 7) — ve koşulunca beyan/risk ayrımı çıktı.", "",
           "## ⛔ ÜRETİM TALİMATI — plan kotası değil, hatırlatma", "",
           "⭐ **T202:** `cevap_var` kayıtlarının cevabı parti2'de kendi kalıbını kurdu "
           "(*«…yazıyor, sorunun cevabı…»* ×4). Pasajlar benzersizdi; tekrar **cevabın "
           "çerçevesinden** geldi. ⇒ Parti3'te pasaja dayanan cevabın **biçimi** "
           "kayıttan kayda değişecek.", "",
           "⭐ **T201:** özerklik ve red **sözlüğe uymak zorunda değil** — kapı okuma "
           "kuyruğu. Parti2'de desen 12 özerklikten yalnız 2'sini gördü ve bu bir "
           "kusur değil, çeşitlendirmenin ölçüsü. ⇒ Çeşitlendirme sürdürülecek.", "",
           "⭐ **T197:** `ilgisiz` sınıfı **görmezden gelinir** — pasaj aktarılmaz.", "",
           "## ⛔ Bu planın söylemedikleri", "", "| | |", "|---|---|",
           "| ⛔ **Çarpan ve tavan SEÇİLDİ** | hedef türetme kuralı PP2'den devralındı; "
           f"`min(havuz_payı × {PP2.CARPAN:g}, %{PP2.TAVAN*100:.0f}) × {N}` — çarpan ve "
           "tavan benim önerim |",
           "| ⛔⛔ **T132 hâlâ geçerli** | daha çok veri güvenlik kapısını açacağına "
           "dair bir kanıt YOK |",
           "| ⛔ **`baglam_davranisi` plana yazıldı, KALİTESİ garanti değil** | plan "
           "sınıfı söyler; sınıfın metinde tutup tutmadığını `beyan-metin-uyumu` ölçer |",
           "| ⛔ **`gd-021` KARARI VERİLMEDİ** | çıplak sınıf işaretlendi, "
           "sınıflandırılmadı |"]
    RAPOR.write_text(RAPOR.read_text(encoding="utf-8") + "\n".join(ek), encoding="utf-8")
    print("\n".join(ek))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
