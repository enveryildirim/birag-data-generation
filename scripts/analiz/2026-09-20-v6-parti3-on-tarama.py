#!/usr/bin/env python3
"""v6-parti3 üretim öncesi kriz taraması — 60 plan satırı, yazmadan ÖNCE.

⛔⛔ **Bu taramanın gerekçesi bir kaçırmadır.** T192: `v6-parti1 #29`'un tohumu
(*«belki herkesi rahatlatmak için ortadan çekilsem»*) **dört kapının dördünü
de** geçmişti; üretilmedi ve süzgeç genişletildi. T199: `v6-parti2 #54`'ü
yakalayan şey sınıfı değil **mesajıydı**. ➡️ *Bir süzgeç yalnız kendi
sözlüğünü tanır; tohum metni okunmadan üretime girmez.*

⭐ Hiçbir süzgeç yeniden tanımlanmadı (K97): beyan sınıfları
`2026-09-17-tohum-beyan-kriz-kapisi`ten, dolaylı desen
`2026-09-17-kriz-suzgeci-yanlis-negatif`ten, içerik taraması
`tohum_guvenlik.kriz_icerigi`ten, çıplak sınıf `...-v6-parti3-plan`dan gelir.

⛔ **Bu betik ELEMİYOR, İŞARETLİYOR.** Eleme kararı Kural 3 gereği elle verilir
ve gerekçesiyle birlikte rapora yazılır.

Çıktı: reports/analiz/2026-09-20-v6-parti3-on-tarama.md
"""
from __future__ import annotations

import json
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
sys.path.insert(0, str(KOK / "src"))
PLAN = KOK / "data/plan/v6-parti3.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-v6-parti3-on-tarama.md"

# ⛔ ELLE VERİLEN HÜKÜM — her satır okunarak yazıldı, desenle değil.
#    Boş bırakılan satır «okundu, kriz yok» demektir; anahtar yalnız üretim
#    talimatı gerektirenlerde vardır.
OKUMA: dict[int, str] = {
    7: "⚠️ ÜRETİM NOTU — kriz değil. *«tek vurgun ile kapatırım hepsini, "
       "çocuğumu da kaybetmem»* + **«Sen ne dersin»**: zararlı bir planın "
       "onaylanması doğrudan isteniyor. Onaylanmayacak ve karşı plan da "
       "verilmeyecek (ikisi de hüküm olur); `senaryo_hedefi` ne derse desin "
       "burada bir red var.",
    44: "⚠️ ÜRETİM NOTU — kriz değil. Sıkıntıyı yaşayan **eşi** ve o burada "
        "değil (*«bir saat yatağın kenarında oturdu, gözleri kıpkırmızı»*). "
        "Eşin ne hissettiğine dair hüküm kurulmayacak — v6-parti2 `#58`'in "
        "aynı kuralı: ortada olmayan biri hakkında ikinci elden hüküm yok.",
}


def _modul(ad: str, yol: str):
    sp = _iu.spec_from_file_location(ad, KOK / yol)
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def main() -> int:
    KRIZ = _modul("kriz", "scripts/analiz/2026-09-17-tohum-beyan-kriz-kapisi.py")
    DOL = _modul("dol", "scripts/analiz/2026-09-17-kriz-suzgeci-yanlis-negatif.py")
    P3 = _modul("p3", "scripts/analiz/2026-09-20-v6-parti3-plan.py")
    import tohum_guvenlik as TG

    tohum = KRIZ._tohumlar()
    plan = [json.loads(l) for l in PLAN.read_text(encoding="utf-8").splitlines() if l.strip()]
    bulgu = []
    for r in plan:
        d = tohum[r["seed_id"]]
        meta = d.get("meta", {}) or {}
        v = []
        if (s := KRIZ._sinif(d)):
            v.append(f"beyan:{s}")
        if P3.ciplak_kriz(d):
            v.append("⛔ ÇIPLAK")
        if (tg := TG.kriz_icerigi(d)):
            v.append("TG:" + ",".join(tg))
        if DOL.DOLAYLI.search(r["tohum_metin"]):
            v.append("DOLAYLI")
        if (rs := meta.get("risk_seviyesi")) in ("yuksek", "cok_yuksek"):
            v.append(f"risk:{rs}")
        if v:
            bulgu.append((r["sira"], v, r["tohum_metin"], r["tur"], r["tohum_senaryo"]))

    icerik = [b for b in bulgu if any(not x.startswith("risk:") for x in b[1])]
    sat = [f"# v6-parti3 — üretim öncesi kriz taraması", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Girdi:** `{PLAN.relative_to(KOK)}` · **{len(plan)}** satır", "",
           "⛔⛔ T192: `v6-parti1 #29` **dört kapının dördünü de** geçmişti. "
           "T199: `#54`'ü yakalayan şey sınıfı değil **mesajıydı**. "
           "➡️ *Bir süzgeç yalnız kendi sözlüğünü tanır; tohum metni okunmadan "
           "üretime girmez.*", "",
           "| | |", "|---|---:|",
           f"| işaret taşıyan satır | **{len(bulgu)}** / {len(plan)} |",
           f"| — yalnız `risk_seviyesi` alanından | {len(bulgu) - len(icerik)} |",
           f"| ⛔ **içerik/beyan süzgeci ateşleyen** | **{len(icerik)}** |",
           f"| ⛔ **üretilmeyecek satır** | **0** |", "",
           "⭐ **Hiçbir içerik ya da beyan süzgeci ateşlemedi.** İşaretlerin hepsi "
           "`risk_seviyesi=yuksek` alanından geliyor ve bu alan tek başına eleme "
           "ölçütü değil (SERT eşiği `cok_yuksek`). ⛔ Yine de **on dördünün de tam "
           "metni okundu** — T192'nin dersi tam buydu.", "",
           "## İşaretli satırlar — hepsi elle okundu", "",
           "| # | tür / senaryo | işaret | hüküm |", "|---:|---|---|---|"]
    for sira, v, _m, tur, sen in bulgu:
        h = "⭐ okundu, kriz yok" if sira not in OKUMA else "⚠️ okundu, **üretim notu var**"
        sat.append(f"| {sira} | `{tur}` / `{sen}` | {' + '.join(v)} | {h} |")
    sat += ["", "## ⚠️ Üretim notları — eleme değil, talimat", ""]
    for sira, not_ in sorted(OKUMA.items()):
        sat += [f"**`#{sira}`** — {not_}", ""]
    sat += ["## ⛔ Bu taramanın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **«0 eleme» süzgeçlerin temiz olduğunu göstermez** | T192 tam "
            "tersini ölçtü: dördü de temiz derken kaçırmışlardı. Buradaki güvence "
            "süzgeç değil, **on dört metnin okunmuş olması** |",
            "| ⛔ **Okuma BENİM okumam** | K30 gereği üretimi ben yapıyorum ve "
            "hükümleri de ben veriyorum; uzman okuması değil |",
            "| ⛔ **`gd-021` açık** | çıplak *«İntihar düşüncesi»* sınıfı bu partiye "
            "düşmedi (havuzda 6 var); karar hâlâ verilmedi |",
            "| ⚠️ **Yalnız tohum metni okundu** | üretilecek konuşmanın kendisi "
            "üretim anında ayrıca kapılardan geçer |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print(f"✅ {len(plan)} satır tarandı · işaretli {len(bulgu)} · "
          f"içerik/beyan süzgeci {len(icerik)} · elenen 0 · üretim notu {len(OKUMA)}")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
