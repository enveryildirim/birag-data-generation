#!/usr/bin/env python3
"""Sıradaki parti neyi kapatmalı — tohum havuzunun kapsama açığı.

⛔⛔ **Neden sırayla değil kanıtla seçiliyor.** T132 ölçmüştü: *«veriyi 3,7 kat,
yönlendirme kaydını 3,2 kat büyütmek aynı kapsamda HİÇBİR ŞEYİ değiştirmedi»*.
⇒ Aynı türden 430 kayıt daha üretmek tıkanan şeyi açmıyor. Parti, havuzun hangi
bölgesinin **eksik kaldığı** ölçülerek seçilmeli.

⭐ **Ölçüm:** üretilmiş 559 tohumun her eksendeki payı, havuzun 2240'taki payıyla
karşılaştırılır. Fark ≥ 3 puan olan değerler «açık» sayılır (eşik ilan edilmiştir,
türetilmemiştir — bu benim önerim).

⛔⛔⛔ **VE «HİÇ ÜRETİLMEMİŞ» DEĞERLER BİR İHMAL DEĞİL.** Tarama iki değerin
sıfır olduğunu buldu (`senaryo=kayma_nuks`, `risk_seviyesi=cok_yuksek`) ve
bakılınca ikisi **aynı 20 tohum** çıktı: `cok_yuksek`'in 10'u `kriz`, 10'u
`kayma_nuks`; `kayma_nuks`'un **10'u da** `cok_yuksek`. Bunlar
`2026-09-17-tohum-beyan-kriz-kapisi.py`'nin **SERT** sınıfı ⇒ Kural 3 gereği
etik kurul + uzman onayı olmadan üretime giremez. ➡️ *Kapsama açığı diye
görünen şey kapının ÇALIŞMASIYDI; bir boşluğu kapatmadan önce onu kimin
açtığını sormak gerekiyor.*

Girdi : data/seeds.v2.jsonl · data/judged/v0.0.14.jsonl
Çıktı : reports/analiz/2026-09-20-kapsama-acigi-envanteri.{md,json}
"""
from __future__ import annotations

import collections
import json
from importlib import util as _iu
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]

# ⛔⛔ Bu envanter HAREKETLİ bir korpusun anlık görüntüsüdür: yeniden
# koşmak, bir önceki partinin hedeflerinin TÜRETİLDİĞİ görüntüyü siler.
# ➡️ *Anlık görüntü alan bir ölçümün çıktı adı sabitse, ölçüm her koşuda
#    kendi geçmişini yok eder* (T200). ⭐ `--ek=` ile etiketlenir;
# varsayılan boş, yani parti2 döneminin dosyası yerinde kalır.
# ⚠️ Etiket ELLE verilir; doğruluğunu raporun kendi sayıları denetler.
import sys as _sys
_EK = next((a.split("=", 1)[1] for a in _sys.argv if a.startswith("--ek=")), "")
_AD = f"{TARIH}-kapsama-acigi-envanteri" + (f"-{_EK}" if _EK else "")
# ⭐ Eşik parametre oldu: `--esik=0` eşik ALTINI da gösterir. Gerekçesi bir
# K97 çarpışması — parti4 planlanırken `stres_tipi` dağılımını kendi
# sayımımla çıkarmıştım ve farklı payda kullandığım için başka sayılar
# verdi. ➡️ *Eşik altını görmek istiyorsan ölçütü yeniden yazma, eşiği düşür.*
ESIK = float(next((a.split("=", 1)[1] for a in _sys.argv
                   if a.startswith("--esik=")), "3.0"))
EKSEN = ["senaryo", "risk_seviyesi", "motivasyon_evresi", "evre", "profil",
         "yas_grubu", "bagimlilik_turu", "siddet_seviyesi", "stres_tipi"]

import tohum_guvenlik as TG  # noqa: E402


def main() -> int:
    tohum = [json.loads(l) for l in
             (KOK / "data/seeds.v2.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    # ⛔⛔ İLK SÜRÜM «kullanılmış»ı KENDİ tanımıyla hesaplıyordu (`v0.0.14`'ün
    # `source_ids`'leri) — oysa planlayıcı `P1.kullanilmis()` kullanıyor ve o
    # `data/candidates/*` de tarıyor. İki tanım iki sayı demektir (K97) ve fark
    # somut: `v6-parti1`'in 59 kaydı üretildi ama henüz `judged/`te değil ⇒
    # envanter onları «kullanılmamış» sayar ve aynı tohumları yeniden hedefler.
    # ⇒ Tek kaynak: planlayıcının tanımı.
    _sp = _iu.spec_from_file_location(
        "p1", KOK / "scripts/analiz/2026-09-15-v4-parti1-plan.py")
    _P1 = _iu.module_from_spec(_sp)
    _sp.loader.exec_module(_P1)
    # ⭐ «Kullanılmış» kümesi dışarıdan verilebilir (`--kullanilmis=<json>`):
    # T211'in hedefleri onarım ÖNCESİ ve SONRASI zeminlerde karşılaştırılabilsin
    # diye. ⛔ Ölçünün tanımı değişmiyor, yalnız girdisi (K97).
    _kj = next((a.split("=", 1)[1] for a in sys.argv
                if a.startswith("--kullanilmis=")), None)
    kullanilan = _P1.kullanilmis()
    if _kj:
        kullanilan = set(json.loads(Path(_kj).read_text(encoding="utf-8")))
        print(f"⚠️ kullanılmış kümesi dışarıdan: {_kj} ({len(kullanilan)})")
    U = [t for t in tohum if t["source_id"] in kullanilan]
    kalan = [t for t in tohum if t["source_id"] not in kullanilan]

    # ⛔ SERT kriz sınıfı — Kural 3, üretime giremez
    def sert(t):
        if t["meta"].get("risk_seviyesi") == "cok_yuksek":
            return "risk_seviyesi=cok_yuksek"
        for e in t["meta"].get("notlar", {}).get("esdurumlar", []):
            if "aktif intihar" in TG.tr_kucult(e):
                return f"esdurum: {e}"
        return None

    sert_kalan = [(t, sert(t)) for t in kalan if sert(t)]
    uygun = [t for t in kalan if not sert(t)]
    krizli = [(t, TG.kriz_icerigi(t)) for t in uygun if TG.kriz_icerigi(t)]

    acik = {}
    for e in EKSEN:
        cu = collections.Counter(t["meta"].get(e) for t in U)
        ch = collections.Counter(t["meta"].get(e) for t in tohum)
        for v, n in ch.items():
            pu, ph = 100 * cu.get(v, 0) / len(U), 100 * n / len(tohum)
            if ph - pu >= ESIK:
                kalan_n = sum(1 for t in uygun if t["meta"].get(e) == v)
                acik[f"{e}={v}"] = {"sette": round(pu, 1), "havuz": round(ph, 1),
                                    "fark": round(ph - pu, 1), "uretilebilir_kalan": kalan_n}
    hic = {}
    for e in EKSEN:
        cu = {t["meta"].get(e) for t in U}
        for v in {t["meta"].get(e) for t in tohum} - cu:
            hic[f"{e}={v}"] = sum(1 for t in tohum if t["meta"].get(e) == v)

    sat = ["# Sıradaki parti neyi kapatmalı — kapsama açığı envanteri", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Havuz:** `data/seeds.v2.jsonl` **{len(tohum)}** tohum · üretilmiş "
           f"**{len(U)}** (%{100*len(U)/len(tohum):.0f}) · kalan **{len(kalan)}**", "",
           "⛔⛔ **Parti sırayla değil kanıtla seçiliyor.** T132: *«veriyi 3,7 kat, "
           "yönlendirme kaydını 3,2 kat büyütmek aynı kapsamda hiçbir şeyi değiştirmedi»* "
           "⇒ aynı türden üretmek tıkanan şeyi açmaz.", "",
           "## 1. ⛔⛔⛔ «Hiç üretilmemiş» değerler bir ihmal değil", "",
           "| değer | havuzdaki tohum | bunlardan SERT | durum |",
           "|---|---:|---:|---|"]
    sert_sid = {t["source_id"] for t, _ in sert_kalan}
    # ⛔ İlk sürümde bu cümle ELLE yazılmıştı («iki etiket, aynı 20 tohum») ve
    # YANLIŞTI: tablo üç değer listeliyordu ve SERT sayısı 40'tı — `esdurumlar`
    # kontrolü `cok_yuksek`'in ötesinde tohum yakalıyor. ⇒ Hesaplatılıyor.
    for k, v in sorted(hic.items()):
        e, d = k.split("=", 1)
        ilgili = {t["source_id"] for t in tohum if str(t["meta"].get(e)) == d}
        kapali = len(ilgili & sert_sid)
        sat.append(f"| `{k}` | {v} | {kapali} | "
                   + ("⛔ tamamı SERT" if kapali == len(ilgili)
                      else "◐ kısmen SERT" if kapali else "⚠️ **SERT değil — başka sebep**")
                   + " |")
    hic_sert = sum(1 for k in hic
                   if {t["source_id"] for t in tohum
                       if str(t["meta"].get(k.split("=", 1)[0])) == k.split("=", 1)[1]}
                   <= sert_sid)
    sat += ["",
            f"Hiç üretilmemiş **{len(hic)}** değerin **{hic_sert}**'i tamamen **SERT** "
            f"sınıfın içinde (`2026-09-17-tohum-beyan-kriz-kapisi.py`) ⇒ Kural 3 gereği "
            "etik kurul + uzman onayı olmadan üretime giremezler. Kalanı başka bir "
            "sebeple boş kalmış ve **üretilebilir**.", "",
            "➡️⭐⭐ *Kapsama açığı diye görünen şey kapının ÇALIŞMASIYDI. Bir boşluğu "
            "kapatmadan önce onu kimin açtığını sormak gerekiyor — yoksa «eksik» diye "
            "kapatılan şey, bilerek konmuş bir sınır olabilir.*", "",
            "## 2. ⭐ Gerçek açıklar — üretilebilir bölgede", "",
            f"Eşik: sette payı havuzdakinden **≥ {ESIK:.0f} puan** düşük olan değerler. "
            "«Üretilebilir kalan» SERT sınıf düşüldükten sonradır.", "",
            "| eksen = değer | sette | havuz | fark | üretilebilir kalan |",
            "|---|---:|---:|---:|---:|"]
    for k, v in sorted(acik.items(), key=lambda x: -x[1]["fark"]):
        sat.append(f"| `{k}` | %{v['sette']} | %{v['havuz']} | **{v['fark']:+.1f}** | "
                   f"{v['uretilebilir_kalan']} |")
    buyuk = [k for k, v in acik.items() if v["havuz"] >= 40]
    sat += ["",
            (f"⚠️ **{len(buyuk)} satır ÇOĞUNLUK sınıfı** ({', '.join('`'+k+'`' for k in buyuk)}): "
             "havuz payı %40'ın üstünde olan bir değerde 3-7 puanlık fark oransal olarak "
             "küçüktür ve hedeflemeye değmez. ➡️ *Mutlak puan eşiği büyük sınıflarda "
             "yanıltır; eylenebilir açıklar AZINLIK sınıflarındakilerdir.*" if buyuk else ""),
            "", "## 3. ⚠️ Üretilebilir havuzun kriz içeriği", "", "| | |", "|---|---:|",
            f"| kalan tohum | {len(kalan)} |",
            f"| ⛔ SERT (üretime giremez) | **{len(sert_kalan)}** |",
            f"| üretilebilir | **{len(uygun)}** |",
            f"| ⚠️ bunlardan kriz İÇERİĞİ işareti taşıyan | **{len(krizli)}** "
            f"(%{100*len(krizli)/max(1,len(uygun)):.1f}) |", "",
            "⚠️ K52: *«kriz içeriği etikete güvenilerek elenemez»* ⇒ içerik taraması "
            "SERT sınıftan sonra da koşuluyor. Bu işaretler **elenmez, raporlanır** "
            "(PERSONA ayrımı, `tohum-beyan-kriz-kapisi` §2): eleme borç/tefeci eksenini "
            "tamamen kaybettirirdi ve §8b yönlendirmesi en çok orada önem taşıyor.", "",
            "## ⛔ Bu envanterin söylemedikleri", "", "| | |", "|---|---|",
            f"| ⛔ **{ESIK:.0f} puanlık eşik SEÇİLDİ** | türetilmedi; bu benim önerim |",
            "| ⛔⛔ **Kapsama ≠ kalite** | bir eksenin payını havuza eşitlemek o "
            "eksende iyi kayıt üretileceğini göstermez |",
            "| ⛔⛔ **T132 hâlâ geçerli** | kapsama açığını kapatmak da «daha çok veri»dir; "
            "güvenlik kapısını açacağına dair bir kanıt YOK |",
            "| ⛔ **Eksenler bağımsız sayıldı** | birlikte dağılım (hücre düzeyi) "
            "bakılmadı; T94 tam bunun bedelini ölçmüştü ⇒ parti planı ızgarayı "
            "kısıtla kurmalı, marjinalleri ayrı ayrı değil |", ""]

    (KOK / f"reports/analiz/{_AD}.json").write_text(
        json.dumps({"tarih": TARIH, "havuz": len(tohum), "uretilmis": len(U),
                    "kalan": len(kalan), "sert": len(sert_kalan), "uygun": len(uygun),
                    "kriz_icerigi": len(krizli), "esik": ESIK,
                    "hic_uretilmemis": hic, "acik": acik}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    (KOK / f"reports/analiz/{_AD}.md").write_text(
        "\n".join(sat), encoding="utf-8")
    print("\n".join(sat[4:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
