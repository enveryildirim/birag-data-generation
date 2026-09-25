#!/usr/bin/env python3
"""v6-parti2 — blokları birleştir ve bütün kapıları yeniden koş.

⛔ parti1 de yeniden birleştirilir: `data/candidates/v6-parti1.jsonl` bloklardan
ÖNCE üretilmişti (10:38 ↔ 11:03) ve `beyan-metin-uyumu`nun ölçtüğü değerleri
taşımıyordu. ➡️ *Birleşik dosya, parçaları değiştiğinde sessizce eskir.*

⭐ Hiçbir ölçüm yeniden tanımlanmadı (K97): `run_checks` `src/checks.py`ten,
özerklik/red kaydın kendi `gen_meta`sından okunur — bu betik SAYAR, ölçmez.

Çıktı: data/candidates/v6-parti{1,2}.jsonl · reports/analiz/2026-09-20-v6-parti2-birlestir.md
"""
from __future__ import annotations

import collections
import hashlib
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
sys.path.insert(0, str(KOK / "src"))
from checks import run_checks  # noqa: E402

# ⭐ Partiler parametre (T200: çıktı adı da girdiyle birlikte değişir).
# ⛔ Varsayılan parti1+parti2 — bu betiğin adındaki rapor yerinde kalır.
PARTILER = tuple((next((a.split("=", 1)[1] for a in sys.argv
                        if a.startswith("--partiler=")),
                       "v6-parti1,v6-parti2")).split(","))
_AD = "v6-parti2" if PARTILER == ("v6-parti1", "v6-parti2") else PARTILER[-1]
RAPOR = KOK / f"reports/analiz/{TARIH}-{_AD}-birlestir.md"
# §7a hedefleri — kaynak: v4 §7a (tasarım kararı, literatür değil).
HEDEF_CTX = {"cevap_var": 0.50, "cevap_yok": 0.25, "izin_iste": 0.12, "ilgisiz": 0.12}


def baglam_sayimi(partiler: tuple[str, ...] = ("v6-parti1", "v6-parti2"),
                  korpus: str = "datasets/v0.0.14/train.jsonl") -> dict:
    """§7a sınıf sayımı — **tek tanım** (K97); parti3 planlayıcısı bunu çağırır.

    Döner: {kaynak_adı: Counter}. Sınıf dışı değerler (`cevapla`, `yetersiz`)
    olduğu gibi sayılır; hedefle karşılaştıran taraf onları ayıklar.
    """
    kay = {korpus: [json.loads(l) for l in
                    (KOK / korpus).read_text(encoding="utf-8").splitlines() if l.strip()]}
    kay.update({p: _yukle(p) for p in partiler})
    return {ad: collections.Counter(
        r["gen_meta"]["baglam_davranisi"] for r in ks
        if r.get("gen_meta", {}).get("baglam_davranisi")) for ad, ks in kay.items()}


def _yukle(parti: str) -> list[dict]:
    kayit = []
    for f in sorted(KOK.glob(f"data/candidates/{parti}.blok*.jsonl")):
        kayit += [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    return sorted(kayit, key=lambda r: r["gen_meta"]["parti_sira"])


def main() -> int:
    sat = [f"# {' + '.join(PARTILER)} — birleştirme ve kapı denetimi", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}", ""]
    hepsi: dict[str, list[dict]] = {}
    hata: list[str] = []

    eksik_ad: list[str] = []
    for parti in PARTILER:
        kay = _yukle(parti)
        hepsi[parti] = kay
        plan = {json.loads(l)["sira"]: json.loads(l)
                for l in (KOK / f"data/plan/{parti}.jsonl").read_text(encoding="utf-8").splitlines()
                if l.strip()}
        # ⭐ tohum eşleşmesi: kayıt planın verdiği tohumu mu taşıyor
        for r in kay:
            s = r["gen_meta"]["parti_sira"]
            if r["gen_meta"]["seed_id"] != plan[s]["seed_id"]:
                hata.append(f"{parti} #{s} tohum uyuşmuyor")
            bek = hashlib.sha256(f"{parti}-{s}".encode()).hexdigest()[:24]
            if r["id"] != bek:
                hata.append(f"{parti} #{s} id beklenenden farklı")
        # ⛔ `run_checks` SONUÇ sözlüğü döndürür, hata listesi değil; sözlüğün
        # kendisi hep doğrudur. Süzgeç `passed` alanına bakar (blok kapısıyla
        # aynı kullanım). ➡️ *Dolu bir sözlük «sorun var» demek değildir.*
        dus = [(r["gen_meta"]["parti_sira"], run_checks(r)) for r in kay]
        dus = [(s, c) for s, c in dus if not c.get("passed")]
        if dus:
            hata += [f"{parti} #{s} run_checks: {json.dumps(c, ensure_ascii=False)[:160]}"
                     for s, c in dus]
        cikti = KOK / f"data/candidates/{parti}.jsonl"
        cikti.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kay),
                         encoding="utf-8")
        # ⛔⛔⛔ KÜNYE KAPISI (T224). `v6-parti1`'in planı üretimden SONRA
        # yeniden üretildi ve blok betikleri yeniden koşunca 59 kaydın
        # `source_ids`'i yeni plandan damgalandı — kayıtlar kendi tohumlarını
        # kaybetti. Hiçbir kapı görmedi; bu satır *«tohum eşleşmesi N/N»* diye
        # yalnız SAYI basıyordu. ➡️ *Bir sayım, sayılan şeyin doğru olduğunu
        # göstermez; künye ancak iki yan karşılaştırılırsa denetlenir.*
        for r in kay:
            s_ = r["gen_meta"]["parti_sira"]
            if s_ not in plan:
                continue
            if r["source_ids"] != [plan[s_]["source_id"]]:
                hata.append(f"{parti} #{s_} KÜNYE: kayıt {r['source_ids']} ↔ "
                            f"plan [{plan[s_]['source_id']}] — plan üretimden "
                            f"sonra değişmiş olabilir")
            if r["gen_meta"].get("seed_id") != plan[s_]["seed_id"]:
                hata.append(f"{parti} #{s_} KÜNYE: seed_id kayıtta "
                            f"{r['gen_meta'].get('seed_id')} ↔ planda "
                            f"{plan[s_]['seed_id']}")
        uretilmeyen = sorted(set(plan) - {r["gen_meta"]["parti_sira"] for r in kay})
        eksik_ad += [f"{parti}#{s}" for s in uretilmeyen]
        sat += [f"## `{parti}`", "", "| | |", "|---|---:|",
                f"| plan satırı | {len(plan)} |", f"| ⭐ üretilen kayıt | **{len(kay)}** |",
                f"| ⛔ üretilmeyen | {uretilmeyen or '—'} |",
                f"| ⭐ `run_checks` geçen | **{len(kay) - len(dus)}/{len(kay)}** |",
                f"| tohum eşleşmesi | {len(kay)}/{len(kay)} |", ""]

    # ⛔ id çakışması — iki parti arası
    tum = [(p, r) for p, ks in hepsi.items() for r in ks]
    sayac = collections.Counter(r["id"] for _, r in tum)
    cak = [i for i, n in sayac.items() if n > 1]
    if cak:
        hata.append(f"⛔ {len(cak)} id çakışması")

    # ── bağlam sınıfı dağılımı ────────────────────────────────────────────
    sat += ["## Bağlam sınıfı dağılımı (§7a)", "",
            "⛔ Parti2'nin ilk 13 bağlam kaydının 13'ü `cevap_var` çıktı: T197'yi "
            "(*«soruyu pasaja uyacak şekilde tasarla»*) tek biçimde uygulamışım. "
            "⭐ Bütünde hedefe yakın durulması iki partinin TERS yönde sapmasının "
            "sonucudur, tasarımın değil.", "",
            "| sınıf | " + " | ".join(["v0.0.14"] + list(PARTILER))
            + " | **bütün** | hedef |",
            "|---" + "|---:" * (len(PARTILER) + 3) + "|"]
    _s = baglam_sayimi(PARTILER)
    kum = {"v0.0.14": _s["datasets/v0.0.14/train.jsonl"],
           **{p: _s[p] for p in PARTILER}}
    top = collections.Counter()
    for c in kum.values():
        top += c
    n_top = sum(top.values())
    for sinif in ("cevap_var", "cevap_yok", "izin_iste", "ilgisiz"):
        hucre = " | ".join(f"{kum[a][sinif]} (%{100*kum[a][sinif]/max(1,sum(kum[a].values())):.0f})"
                           for a in ["v0.0.14", *PARTILER])
        sat.append(f"| `{sinif}` | {hucre} | **{top[sinif]} (%{100*top[sinif]/n_top:.0f})** "
                   f"| %{100*HEDEF_CTX[sinif]:.0f} |")
    sat += ["", f"⚠️ v0.0.14'te ayrıca sınıf dışı {sum(v for k, v in kum['v0.0.14'].items() if k not in HEDEF_CTX)} "
                "kayıt var (`cevapla`, `yetersiz`); toplam sütununa dahil değiller.", ""]

    # ── sapma ve elle onay envanteri ──────────────────────────────────────
    sap = [(p, r["gen_meta"]["parti_sira"]) for p, r in tum if "izgara_sapmasi" in r["gen_meta"]]
    onay = collections.Counter(a for _, r in tum for a in r["gen_meta"].get("elle_onay", []))
    sat += ["## §5a″ sapmaları ve elle onaylar", "", "| | |", "|---|---:|",
            f"| ızgaradan sapan kayıt | **{len(sap)}** / {len(tum)} |",
            *[f"| — {p} | {sum(1 for q, _ in sap if q == p)} |" for p in PARTILER],
            f"| elle onaylı `ozerklik_vurgusu` | {onay['ozerklik_vurgusu']} |",
            f"| elle onaylı `is_negative` | {onay['is_negative']} |", "",
            f"⭐ Sapan satırlar: {', '.join(f'{p[-6:]}#{s}' for p, s in sap)}", ""]

    # ── ⭐ desenin gördüğü oran: partiler arası ────────────────────────────
    sat += ["## ⭐⭐ Desen kapsaması — partiler arası", "",
            "Bir kaydın özerklik/red taşıdığı iki yoldan biriyle saptanıyor: **sözlük "
            "deseni** ya da **elle onay**. Desenin tek başına yakaladığı oran:", "",
            "| | " + " | ".join(PARTILER) + " |",
            "|---" + "|---:" * len(PARTILER) + "|"]
    for alan, ad in (("ozerklik_vurgusu", "özerklik"), ("is_negative", "red")):
        h = []
        for p in PARTILER:
            ks = [r for r in hepsi[p] if (r["gen_meta"].get(alan) if alan == "ozerklik_vurgusu"
                                          else r.get(alan))]
            e = sum(1 for r in ks if alan in r["gen_meta"].get("elle_onay", []))
            h.append(f"{len(ks)-e}/{len(ks)} (%{100*(len(ks)-e)/max(1,len(ks)):.0f})")
        sat.append(f"| {ad} | " + " | ".join(h) + " |")
    # ⭐⭐ Kapsama YÜKSEK ama şablon DÜŞÜK olabilir mi? Desen SÖZCÜK arar;
    # şablon kapısı DİZİ sayar. İkisi ayrı şeyler ve ayrıldıkları yer burası:
    # aynı fiil (*«söyleyemem»*) farklı cümlelerde geçerse kapsama yükselir,
    # şablon yükselmez. ⇒ Red cümlelerinin BENZERSİZLİĞİ ayrıca sayılıyor.
    sat += ["", "⭐ Kapsama bir **sözcük** ölçüsü, şablon kapısı bir **dizi** "
                "ölçüsü. Aynı fiil farklı cümlelerde geçerse kapsama yükselir, "
                "şablon yükselmez. Red cümlelerinin benzersizliği:", "",
            "| | " + " | ".join(PARTILER) + " |",
            "|---" + "|---:" * len(PARTILER) + "|"]
    import re as _re
    _fiil = _re.compile(r"[^.!?\n]*\b(veremem|söyleyemem|yapamam|kuramam|tartamam|"
                        r"sayamam|çizemem|bakamam|edemem)\b[^.!?\n]*", _re.I)
    _c = []
    for pr in PARTILER:
        cum = []
        for r in hepsi[pr]:
            son_ = [m for m in r["messages"] if m["role"] == "assistant"][-1]["content"]
            cum += [c.strip().lower() for c in _fiil.findall(son_) or []]
            cum += [m.group(0).strip().lower() for m in _fiil.finditer(son_)]
        cum = [c for c in cum if len(c) > 12]
        _c.append(f"{len(set(cum))}/{len(cum)}" if cum else "0/0")
    sat.append("| benzersiz red cümlesi / toplam | " + " | ".join(_c) + " |")
    # ⛔⛔ BU CÜMLE SABİTTİ ve `--partiler=v6-parti5` ile koşulduğunda raporda
    # tablosu olmayan bir karşılaştırmayı iddia ediyordu. ➡️ *Parametreli bir
    # girdinin yanındaki sabit bir cümle, girdi değiştiğinde sessizce yalan olur.*
    if len(PARTILER) > 1:
        sat += ["", "⭐⭐ **Aynı desen partiler arasında farklı oranlar görüyor.** "
                    "Partileri aynı kişi aynı ölçütle yazdı; değişen tek şey, "
                    "özerklik ve red **biçimlerinin bilerek çeşitlendirilmesiydi**.", ""]
    sat += ["",
            "➡️ *Sözlük deseni yapıyı değil, KALIBA UYMAYI ölçüyor; şablonu azaltmak "
            "ölçülen oranı düşürür ve ölçüm bunu bir gerileme gibi gösterir.*", "",
            "⛔ Bu, T193'ün ölçtüğü oranı da niteler: o oran bir **alt sınır** değil, "
            "**kalıp bağımlı** bir sayıdır.", ""]

    eksik_n = len(eksik_ad)
    sat += ["## ⛔ Bu raporun söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Bu bir KALİTE raporu değil** | kapılar biçim ve dayanak denetler; "
            f"terapötik kaliteyi judge ölçer ve {', '.join(PARTILER)} bu raporda "
            "yargılanmadı |",
            # ⛔ Eksik satır artık VERİDEN sayılıyor; sabit `#54` cümlesi parti5'te
            # yanlıştı (60/60 üretildi).
            *([f"| ⛔ **{eksik_n} plan satırı üretilmedi** | üretilmeyenler: "
               f"{', '.join(eksik_ad)} — gerekçeleri `data/plan/elenen-tohumlar.jsonl` "
               "ve ilgili blok betiklerinde |"] if eksik_n else
              ["| ⭐ **Üretilmeyen plan satırı yok** | bu raporun kapsadığı "
               "partilerde plan satırlarının tamamı üretildi |"]),
            "| ⚠️ **Elle onay bir İNSAN kararıdır** | desen görmedi, ben onayladım; "
            "onay cümlesi betikte yazılı ve kayıtta `gen_meta.elle_onay`ta duruyor |"]

    if hata:
        print("⛔ KAPI REDDETTİ:")
        for h in hata[:20]:
            print("  ", h)
        return 1
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("✅ " + " · ".join(f"{p} {len(hepsi[p])}" for p in PARTILER)
          + f" kayıt · id çakışması 0 · rapor → {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
