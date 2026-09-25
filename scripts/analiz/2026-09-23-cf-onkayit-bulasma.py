#!/usr/bin/env python3
"""⛔⛔⛔ Ön kaydın «BULAŞMAMIŞ» baş ölçüsü hiç ölçülmemişti — şimdi ölçülüyor.

**Ne oldu.** `v0.0.22` ön kaydı (`65a50c3`) baş ölçüyü
*«`context_fidelity`'nin bulaşmamış 15 ögesi»* diye koydu
(`yeterli`+`distractor`+`yetersiz`). 09-22 bulaşma raporu da *«Temiz kalan
ölçüler»* diye aynı 15 ögeyi saydı. ⛔ **Ama o 15 öge hiç ölçülmedi** —
bulaşma ölçüsü yalnız 5 `celiskili` ögesine koşuldu; öteki 15'i
**kategorisi yüzünden** temiz sayıldı. T22 ailesinin biçimi: *iddia yazılı,
ölçüm yok.*

⭐ Örtüşmez eval setini yazarken (`2026-09-23-cf-ortusmez-eval-yaz.py`)
aynı ölçüyü sınama amaçlı o 15 ögeye uyguladım ve fark ettim.

**Bu betik** 09-22 ölçüsünü (`olc()`, K103 — kopyalanmadı, değiştirilmedi)
**üç gruba** aynı anda uygular ki fark yan yana görülsün:

  · eski `celiskili` ögeleri (5) — 09-22'de «bulaşmalı» ilan edilen
  · eski «temiz» ögeler (15) — ön kaydın BAŞ ÖLÇÜSÜ, kategoriye göre
  · yeni örtüşmez set (15) — `evals/context_fidelity.ortusmez.jsonl`

⛔ **«Değer çakışması» kök düzeyindedir, birebir değil:** bir eğitim
değerinin (ör. «randevu gerekir») 6 harflik köklerinin **hepsi** eval
pasajında geçiyorsa sayılır. 09-22 raporu bunu *«birebir»* diye
yazmıştı; o ifade fazla güçlüydü.

⛔ Bu betik ön kaydı **DEĞİŞTİRMEZ**. Ölçüm 5/40'ta durdu ve t7
çözümlenmedi ⇒ ön kayıt hâlâ **sonuç görülmeden** düzeltilebilir, ama
bu bir **karardır** ve kullanıcınındır.

Çıktı: reports/analiz/2026-09-23-cf-onkayit-bulasma.md
"""
from __future__ import annotations

import collections
import json
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from kunye import betik_tarihi  # noqa: E402

RAPOR = KOK / "reports/analiz/2026-09-23-cf-onkayit-bulasma.md"
ESKI = KOK / "evals/context_fidelity.jsonl"
YENI = KOK / "evals/context_fidelity.ortusmez.jsonl"
ONKAYIT = KOK / "configs/deney/2026-09-22-v0022-celiskili-on-kayit.json"

_y = KOK / "scripts/analiz/2026-09-22-celiskili-eval-bulasma.py"
_sp = _iu.spec_from_file_location("_bulasma", _y)
_b = _iu.module_from_spec(_sp)
_sp.loader.exec_module(_b)


def main() -> int:
    banka = _b.banka_oku()
    eski = [json.loads(l) for l in open(ESKI)]
    yeni = [json.loads(l) for l in open(YENI)]
    onkayit = json.loads(ONKAYIT.read_text())

    gruplar = collections.OrderedDict()
    gruplar["eski `celiskili` (09-22'de bulaşmalı ilan edilen)"] = \
        [e for e in eski if e["kategori"] == "celiskili"]
    for kat in ("yeterli", "distractor", "yetersiz"):
        gruplar[f"eski `{kat}` — ⛔ ön kaydın baş ölçüsü"] = \
            [e for e in eski if e["kategori"] == kat]
    gruplar["⭐ yeni örtüşmez set"] = yeni

    sat, detay = [], {}
    for ad, ogeler in gruplar.items():
        _, deger = _b.olc(banka, ogeler)
        oge_carp = collections.defaultdict(set)
        for i, no, d, _ in deger:
            oge_carp[i].add(f"#{no} «{d}»")
        sat.append((ad, len(ogeler), len(oge_carp)))
        detay[ad] = oge_carp

    bas = [e for e in eski if e["kategori"] in ("yeterli", "distractor", "yetersiz")]
    _, bas_deger = _b.olc(banka, bas)
    bas_carp = {i for i, *_ in bas_deger}
    temiz_kalan = [e["id"] for e in bas if e["id"] not in bas_carp]

    s = ["# ⛔⛔⛔ Ön kaydın «bulaşmamış» baş ölçüsü — ölçüldü", "",
         f"**Betik:** `{Path(__file__).relative_to(KOK)}` · "
         f"**Tarih:** {betik_tarihi(__file__)}  ",
         f"**Ön kayıt:** `{ONKAYIT.relative_to(KOK)}` — baş ölçü: "
         f"*«{onkayit['bas_olcu']}»*  ",
         f"**Eğitim bankası:** {len(banka)} çift  ", "",
         "⛔⛔ **Ne oldu.** Ön kayıt baş ölçüyü *«bulaşmamış 15 öge»* diye "
         "koydu; 09-22 bulaşma raporu da *«Temiz kalan ölçüler»* diye aynı "
         "15'i saydı. **O 15 öge hiç ölçülmedi** — ölçü yalnız 5 `celiskili` "
         "ögesine koşuldu, öteki 15'i **kategorisi yüzünden** temiz sayıldı. "
         "*İddia yazılı, ölçüm yok* (T22 ailesi).", "",
         "## Aynı ölçü, üç grup", "",
         "| grup | öge | değer çakışması olan öge |", "|---|---:|---:|"]
    s += [f"| {ad} | {n} | **{c}/{n}** |" for ad, n, c in sat]
    s += ["", f"⛔⛔⛔ **Baş ölçünün {len(bas_carp)}/{len(bas)} ögesinde** bir "
          "eğitim çiftinin değer kökleri pasajda geçiyor. Çakışma `yeterli` "
          "ve `distractor` kategorilerinde toplanıyor; `yetersiz` temiz.", "",
          "## Öge başına", "", "| öge | kategori | çakışan eğitim değerleri |",
          "|---|---|---|"]
    kat_of = {e["id"]: e["kategori"] for e in eski}
    for e in bas:
        c = detay[f"eski `{e['kategori']}` — ⛔ ön kaydın baş ölçüsü"].get(e["id"])
        s.append(f"| `{e['id']}` | {kat_of[e['id']]} | "
                 + (", ".join(sorted(c)) if c else "—") + " |")
    s += ["", "## Neden önemli — bulaşmanın yönü belirsiz", "",
          "`e3` kolu, `d1`'den **yalnız** bu 25 çiftle ayrılıyor. Baş ölçünün "
          "ögeleri o çiftlerin pasajlarını (*«Görüşmeler ücretsizdir»*, "
          "*«randevusuz yapılabilir»*…) taşıyorsa, iki kol arasındaki bir "
          "fark **genel bağlam sadakatinden** değil, **o pasajlara "
          "aşinalıktan** gelebilir. ⛔ Yön de bilinmiyor:", "",
          "- **kayırabilir** — model bu cümleleri eğitimde görmüş, cevabı "
          "çıkarması kolaylaşır;",
          "- **bozabilir** — model «ücretsiz» görünce *çelişki var* demeyi "
          "öğrendi; tek pasajlı bir `yeterli` ögesinde olmayan bir çelişkiyi "
          "adlandırabilir.", "",
          "⇒ Her iki durumda da fark **yorumlanamaz**.", "",
          "## ⭐ Ön kayıt SONUÇ GÖRÜLMEDEN düzeltilebilir — ama bu bir karar", "",
          "Ölçüm 5/40'ta durdu (K272) ve t7 **çözümlenmedi** ⇒ baş ölçüyü "
          "değiştirmek şu an hâlâ temiz. Değiştirmek ise ön kaydın kendisini "
          "değiştirmektir ⇒ **bu betik değiştirmiyor**. Seçenekler:", "",
          f"1. **Baş ölçüyü çakışmasız ögelere daralt** — "
          f"{len(temiz_kalan)} öge kalır: "
          + ", ".join(f"`{i}`" for i in temiz_kalan)
          + ". ⛔ Güç düşer (n küçülür).",
          "2. **Baş ölçüyü örtüşmez sete taşı** — "
          f"`{YENI.relative_to(KOK)}` ({len(yeni)} öge, değer çakışması "
          f"{sat[-1][2]}). ⛔ Ama o set **yalnız `celiskili`** davranışını "
          "ölçer; genel bağlam sadakatini değil.",
          "3. **İkisini birlikte** ve sıralarını şimdi, sonuçtan önce yaz.", "",
          "*Hangisi — bu benim kararım değil.*", "",
          "## ⛔ Bunun söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ **Sözcük ölçüsü** | kök düzeyinde; anlamsal bulaşmayı görmez, "
          "işlev sözcüğünü içerikten ayıramaz. Değer çakışması bu ölçünün en "
          "güçlü ama yine kaba sinyali |",
          "| ⛔ **Yalnız `celiskili` bankasına karşı** | `d1`'in (v0.0.18) "
          "kendi `cevap_var`/`cevap_yok` kayıtlarının pasajlarıyla örtüşme "
          "**ölçülmedi** — ama o kayıtlar iki kolda da var, fark "
          "yaratmıyor |",
          "| ⛔ **Bulaşmanın büyüklüğü ≠ etkisi** | pasajın eğitimde geçmesi, "
          "puanı ne kadar oynattığını söylemez |",
          "| ⚠️ **Bunu ben kaçırmıştım** | 09-22 raporunda «temiz kalan "
          "ölçüler» cümlesini ben yazdım, ölçmeden |"]

    RAPOR.write_text("\n".join(s) + "\n", encoding="utf-8")
    assert RAPOR.exists()
    for ad, n, c in sat:
        print(f"  {c:2}/{n:<2} {ad}")
    print(f"⛔ baş ölçüde çakışmasız kalan: {len(temiz_kalan)} öge")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
