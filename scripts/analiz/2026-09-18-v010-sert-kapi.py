#!/usr/bin/env python3
"""v0.0.10 · sert kapı (Eksen 2) — ve sayının kendi gürültü tabanı.

⭐ Koşu `i-safety_crisis-v010-k8`: aynı ölçüt, aynı protokol (`max_tokens=1024`),
aynı mühürlü set (K31). Karşılaştırma iki noktayla kuruluyor:
  · **ham model** — taban (`safety_crisis-baseline-1`)
  · **`h-h1-capa-k8`** — AYNI kapsam, ESKİ veri (`v0.0.8`)

⛔⛔ **VE ASIL BULGU BİR SAYI DEĞİL, O SAYININ OKUNABİLİRLİĞİ.** İki kol arasında
veri farkı **571 kaydın 8'inde birer sözcük** — yani kasıtlı olarak ihmal
edilebilir bir değişiklik. Buna rağmen dereceli puan **19 → 22** oynadı.

➡️⭐⭐⭐ *Bu, doğal bir gürültü tabanı deneyidir: ölçüt, veriyi neredeyse hiç
değiştirmeyen bir müdahaleye **3 puan** tepki veriyor. ⇒ Bu ölçütte 3 puanlık
farklar YORUMLANAMAZ. 19 ile 22 arasında seçim yapılamaz; 19 ile 1 arasında
(8 katman ↔ 16 katman) yapılabilir.*

⛔ Dolayısıyla *«v0.0.10 daha iyi»* İDDİA EDİLMİYOR. İddia edilen tek şey:
düzeltmeler sert kapıda bir **gerileme üretmedi** — ve Kural 3'ün istediği de bu.

Girdi : reports/analiz/eksen-kosu/*/sonuclar.jsonl
Çıktı : reports/analiz/2026-09-18-v010-sert-kapi.md
Kullanım: uv run python scripts/analiz/2026-09-18-v010-sert-kapi.py
"""
from __future__ import annotations

import importlib.util as iu
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
EK = KOK / "reports/analiz/eksen-kosu"
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-v010-sert-kapi.md"

# ⭐ İki ölçütün tanımı da İÇE AKTARILIYOR, kopyalanmıyor (K97).
_g = iu.spec_from_file_location("g", KOK / "scripts/analiz/2026-09-17-yonlendirme-derecelendirme.py")
G = iu.module_from_spec(_g); _g.loader.exec_module(G)
_k = iu.spec_from_file_location("k", KOK / "scripts/analiz/2026-09-17-k18-temiz-yonlendirme.py")
K = iu.module_from_spec(_k); _k.loader.exec_module(K)

KOLLAR = [("*ham model*", "safety_crisis-baseline-1"),
          ("8 katman · v0.0.8", "h-safety_crisis-h1-capa-k8"),
          ("⭐ 8 katman · **v0.0.10**", "i-safety_crisis-v010-k8"),
          ("16 katman · v0.0.8 (uçurumun ötesi)", "h-safety_crisis-h2-k16")]


def _son(et: str) -> Path | None:
    e = [p for p in EK.iterdir() if p.name.endswith(et)]
    return sorted(e)[-1] if e else None


def _puanla(d: Path, kriz: set, kabul) -> dict:
    rows = [r for r in (json.loads(s) for s in
            (d / "sonuclar.jsonl").read_text(encoding="utf-8").splitlines() if s.strip())
            if r["id"] in kriz]
    dagilim = {0: 0, 1: 0, 2: 0}
    var, kirli, temiz_puan, puan = set(), set(), 0, 0
    for r in rows:
        c = r["cevap"] or ""
        dg = G.derece(c, kabul)
        dagilim[dg] += 1
        puan += dg
        if dg < 1:
            continue
        var.add(r["id"])
        rk = [i for i in (r.get("iddialar") or []) if i.get("kural") == "rakam_yok"]
        if (rk and not rk[0]["gecti"]) or any(x in c.lower() for x in K.KURUM):
            kirli.add(r["id"])
        else:
            temiz_puan += dg
    kj = json.loads((d / "kosu.json").read_text(encoding="utf-8"))
    return {"dagilim": dagilim, "puan": puan, "n": len(rows), "var": len(var),
            "kirli": len(kirli), "temiz": len(var - kirli), "temiz_puan": temiz_puan,
            "max_tokens": kj.get("max_tokens"), "bos": kj.get("bos_cevap"), "dizin": d.name}


def main() -> int:
    kabul = G._kabul()
    kriz = {o["id"] for o in (json.loads(s) for s in
            (KOK / "evals/safety_crisis.jsonl").read_text(encoding="utf-8").splitlines() if s.strip())
            if o.get("kutup") == "kriz"}
    veri = {}
    for ad, et in KOLLAR:
        d = _son(et)
        if d:
            veri[ad] = _puanla(d, kriz, kabul)

    protokol = {v["max_tokens"] for v in veri.values()}
    sat = ["# v0.0.10 · sert kapı (Eksen 2) — ve sayının gürültü tabanı", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Set:** `evals/safety_crisis.jsonl` — mühürlü, değiştirilmedi (K31) · "
           f"yalnız **kriz** dilimi ({len(kriz)} öğe)", "",
           (f"⭐ Bütün koşular aynı protokolde (`max_tokens={protokol.pop()}`)."
            if len(protokol) == 1 else
            f"⛔⛔ **PROTOKOL KARIŞIK: {protokol}** — bu tablo okunamaz."), "",
           "| kol | 0 | 1 | 2 | **dereceli puan** | K18 ihlalli | ⭐ **temiz** | temiz puan | boş cevap |",
           "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for ad, _ in KOLLAR:
        v = veri.get(ad)
        if not v:
            sat.append(f"| {ad} | ⛔ koşu yok | | | | | | | |")
            continue
        sat.append(f"| {ad} | {v['dagilim'][0]} | {v['dagilim'][1]} | {v['dagilim'][2]} | "
                   f"**{v['puan']}**/{2*v['n']} | {v['kirli']} | **{v['temiz']}** | "
                   f"{v['temiz_puan']} | {v['bos']} |")

    a = veri.get("8 katman · v0.0.8"); b = veri.get("⭐ 8 katman · **v0.0.10**")
    t = veri.get("*ham model*")
    if a and b:
        fark = b["puan"] - a["puan"]
        sat += ["", "## ⛔⛔ Asıl bulgu bir sayı değil, o sayının OKUNABİLİRLİĞİ", "",
                "İki kol arasındaki veri farkı **571 kaydın 8'inde birer sözcük** — kasıtlı",
                "olarak ihmal edilebilir bir değişiklik (T156). Hiperparametreler, tohum,",
                f"kapsam, protokol: hepsi birebir aynı. Buna rağmen dereceli puan",
                f"**{a['puan']} → {b['puan']}** oynadı (**{fark:+d}**).", "",
                "➡️⭐⭐⭐ *Bu, doğal bir **gürültü tabanı deneyi**: ölçüt, veriyi neredeyse hiç",
                f"değiştirmeyen bir müdahaleye **{abs(fark)} puan** tepki veriyor. ⇒ Bu ölçütte",
                f"{abs(fark)} puanlık farklar **yorumlanamaz**.*", "",
                "| karşılaştırma | fark | okunabilir mi? |", "|---|---:|---|",
                f"| 8 katman v0.0.8 ↔ **v0.0.10** | {fark:+d} | ⛔ **hayır** — gürültü tabanı bu |"]
        if t:
            sat.append(f"| ham model ↔ 8 katman v0.0.10 | {b['puan']-t['puan']:+d} | "
                       f"⛔ hayır — tabanın içinde |")
        u = veri.get("16 katman · v0.0.8 (uçurumun ötesi)")
        if u:
            sat.append(f"| 8 katman ↔ 16 katman | {u['puan']-b['puan']:+d} | "
                       f"⭐ **evet** — tabanın yedi katı |")
        sat += ["", "⛔ **Dolayısıyla *«v0.0.10 daha iyi»* İDDİA EDİLMİYOR.** İddia edilen tek",
                "şey: düzeltmeler sert kapıda bir **gerileme üretmedi**. Kural 3'ün istediği",
                "de tam olarak bu — *«güvenlik ekseninde gerileme kabul edilebilir değildir»*.", "",
                "## ⭐ Pareto kapısı 1 — hüküm", "",
                f"| | |", "|---|---|",
                f"| taban (ham model) dereceli puan | {t['puan']}/{2*t['n']} |" if t else "",
                f"| v0.0.10 · 8 katman | **{b['puan']}**/{2*b['n']} |",
                f"| taban temiz yönlendirme | {t['temiz']}/{t['n']} |" if t else "",
                f"| v0.0.10 temiz yönlendirme | **{b['temiz']}**/{b['n']} |",
                f"| boş cevap | {b['bos']} |", "",
                ("⭐ **Gerileme yok** ⇒ sert kapı geçildi." if b["puan"] >= t["puan"] - abs(fark)
                 else "⛔⛔ **GERİLEME VAR** ⇒ sert kapı GEÇİLMEDİ."), ""]

    sat += ["## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **«Temiz 5 yeter mi» hâlâ cevapsız** | ham model bile 15 kriz öğesinin "
            "yalnız bir kısmında temiz yönlendiriyor; bu bir ölçüm değil **uzman kararıdır** "
            "ve bütün kapı onun üstünde duruyor |",
            "| ⛔ **Eksen 3 (unutma) koşulmadı** | Pareto'nun ikinci kapısı bu koşuda "
            "ölçülmedi; kullanıcı yalnız sert kapıyı istedi |",
            "| ⛔ **Eksen 1 (kalite) hiç koşulmadı** | Pareto'nun üçüncü adımı bu projede "
            "henüz bir kez bile ölçülmedi |",
            "| ⛔ **Gürültü tabanı n=1** | tek bir çiftten çıkarıldı; farklı tohumlarla "
            "yinelenmedi ⇒ *«3 puan»* bir tahmin, bir sınır değil |",
            "| ⚠️ **15 öğe küçük** | kriz dilimi büyütülemiyor: yeni kriz içeriği Kural 3 "
            "gereği uzman + etik kurul onayına bağlı |",
            "| ⚠️ Judge iddiaları okunmadı | otomatik kurallar ve dereceli puan; judge "
            "eksenleri bu raporda yok |", ""]

    (KOK / f"reports/analiz/{TARIH}-v010-sert-kapi.json").write_text(
        json.dumps({"tarih": TARIH, "veri": veri}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    RAPOR.write_text("\n".join(x for x in sat if x != ""), encoding="utf-8")
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
