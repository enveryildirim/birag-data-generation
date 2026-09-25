#!/usr/bin/env python3
"""⛔⛔ BULAŞMA ÖLÇÜMÜ: eğitim pasaj bankası ↔ `context_fidelity` eval'i.

⛔⛔⛔ **Neden bu betik ince ayardan ÖNCE koşuyor.** `celiskili` sınıfı
`context_fidelity` eval'indeki **5 `celiskili` ögesinde** kazanç versin
diye tasarlandı. Ama eval ögeleri de, eğitim bankası da **aynı idari
konu havuzundan** yazıldı (randevu, ücret, saklama, belge, saat…). Eğer
aynı konu — hatta aynı **değerler** — iki tarafta da varsa, ölçülecek
kazanç öğrenme değil **ezberdir**.

➡️ *Bir kazanç iddiası, kazancın ölçüldüğü ögenin eğitimde bulunup
bulunmadığı ölçülmeden kurulamaz.* Bu ölçüm koşudan **önce** yapılır ve
sonucu ön kayda yazılır (K31/Kural 5).

⛔ Bu betik bir şey **düzeltmez**; yalnız bulaşmanın büyüklüğünü ölçer.

Çıktı: reports/analiz/2026-09-22-celiskili-eval-bulasma.md
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from kunye import betik_tarihi  # noqa: E402
from tohum_guvenlik import tr_sadelestir  # noqa: E402

RAPOR = KOK / "reports/analiz/2026-09-22-celiskili-eval-bulasma.md"
BANKALAR = ["data/celiskili-pasaj-bankasi.json",
            "data/celiskili-pasaj-bankasi.v2.json"]
EVAL = "evals/context_fidelity.jsonl"

DURAK = {tr_sadelestir(w) for w in """
danisma birim birimi hizmet gorusme gorusmeler icin ile olarak yapilir
yapilmaktadir verilmektedir verilir alinmaktadir alinir gerekir gerekmektedir
bir iki uc dort bes hafta gun saat kisi yil ay arasinda acik notu metni
metin ozeti duyuru duyurusu yonerge yonergesi bilgi bilgisi
""".split()}


def _kok(metin: str) -> set[str]:
    return {w[:6] for w in re.findall(r"\w{4,}", tr_sadelestir(metin))
            if w[:6] not in {d[:6] for d in DURAK}}


def olc(banka: list[dict], ogeler: list[dict]):
    """Eval ögeleri ↔ eğitim çiftleri: (konu satırları, değer çakışmaları).

    ⭐ Ayrı fonksiyon çünkü 09-23'teki örtüşmez eval seti bu ölçüyü
    **kopyalamadan** kullanır (K103). Davranış değişmedi: rapor bayt bayt
    aynı üretildiği doğrulandı.
    """
    satir = []
    for e in ogeler:
        e_kok = _kok(" ".join(p["metin"] for p in e["context"]))
        en_iyi = []
        for c in banka:
            ortak = e_kok & _kok(" ".join(p["metin"] for p in c["context"]))
            if ortak:
                en_iyi.append((len(ortak), c["no"], c["konu"], sorted(ortak)))
        en_iyi.sort(reverse=True)
        satir.append((e["id"], e.get("sonda", "")[:44], en_iyi[:2]))

    # ⛔ Değer düzeyinde birebir çakışma — en ağır bulaşma biçimi
    deger_cakisma = []
    for e in ogeler:
        e_d = _kok(" ".join(p["metin"] for p in e["context"]))
        for c in banka:
            for d in c["degerler"]:
                dk = _kok(d)
                if dk and dk <= e_d:
                    deger_cakisma.append((e["id"], c["no"], d, sorted(dk)))
    return satir, deger_cakisma


def banka_oku() -> list[dict]:
    banka = []
    for b in BANKALAR:
        banka += json.loads((KOK / b).read_text())["ciftler"]
    return banka


def main() -> int:
    banka = banka_oku()
    ev = [json.loads(l) for l in open(KOK / EVAL)]
    cel = [e for e in ev if e.get("kategori") == "celiskili"]
    satir, deger_cakisma = olc(banka, cel)

    ortakli = sum(1 for _, _, b in satir if b)
    s = [f"# ⛔⛔ Bulaşma ölçümü — eğitim bankası ↔ `context_fidelity` eval'i",
         "",
         f"**Betik:** `{Path(__file__).relative_to(KOK)}` · "
         f"**Tarih:** {betik_tarihi(__file__)}  ",
         f"**Banka:** {len(banka)} çift · **eval `celiskili` ögesi:** "
         f"{len(cel)}  ",
         f"**Bulgu:** {ortakli}/{len(cel)} eval ögesinin bankada konu "
         f"ortaklığı olan bir çifti var  ", "",
         "⛔⛔⛔ **Neden önemli.** `celiskili` sınıfı tam da bu 5 ögede kazanç "
         "versin diye tasarlandı. Eğer aynı konu — hatta aynı **değerler** — "
         "iki tarafta da varsa, ölçülecek kazanç **öğrenme değil ezber** "
         "olabilir. Bu ölçüm ince ayardan **önce** yapıldı ve ön kayda "
         "yazıldı.", "",
         "## Öge başına en yakın eğitim çiftleri", "",
         "| eval | sonda | bankadaki en yakın çift(ler) | ortak kök |",
         "|---|---|---|---|"]
    for eid, sonda, en in satir:
        if not en:
            s.append(f"| `{eid}` | {sonda} | — | — |")
            continue
        ilk = en[0]
        s.append(f"| `{eid}` | {sonda} | #{ilk[1]} {ilk[2]} | "
                 f"{', '.join('`'+x+'`' for x in ilk[3][:5])} |")

    s += ["", "## ⛔⛔ Değer düzeyinde çakışma (en ağır biçim)", ""]
    if deger_cakisma:
        s += ["| eval | banka | çakışan değer |", "|---|---:|---|"]
        s += [f"| `{a}` | #{b} | «{c}» |" for a, b, c, _ in deger_cakisma]
        s += ["", f"⛔⛔⛔ **{len(deger_cakisma)} çakışma.** Bir eğitim "
              "çiftinin **değeri** eval ögesinin pasajlarında birebir "
              "geçiyor ⇒ o öge için ölçülecek kazanç **ezberden ayırt "
              "edilemez**.", ""]
    else:
        s += ["⭐ Hiçbir eğitim çiftinin değeri bir eval ögesinde birebir "
              "geçmiyor.", ""]

    s += ["## ⭐ Ön kayda yazılacak hüküm", "",
          f"⛔ `context_fidelity`'nin **`celiskili` alt puanı** "
          f"({ortakli}/{len(cel)} ögede konu ortaklığı"
          + (f", {len(deger_cakisma)} değer çakışması" if deger_cakisma else "")
          + ") **temiz bir sınama değildir** ve baş sonuç olarak "
          "raporlanamaz.", "",
          "⭐ **Temiz kalan ölçüler:** `context_fidelity`'nin öteki üç "
          "kategorisi (`yeterli`, `distractor`, `yetersiz` — 15 öge), "
          "`context_fidelity.real` (15 gerçek öge), `safety_crisis`, "
          "`forgetting_smoke`, `sycophancy`. Baş sonuç **bunlardan** "
          "okunacak.", "",
          "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ **Kök eşleme kaba** | 6 harflik ön ek, elle yazılmış durak "
          "listesi ⇒ hem yanlış pozitif hem yanlış negatif verir; sayı bir "
          "**işarettir**, kesin bir örtüşme ölçüsü değil |",
          "| ⛔ **Anlamsal bulaşma ölçülmedi** | farklı sözcüklerle aynı "
          "yapıyı öğretmek de bulaşmadır ve bu tarama onu görmez |",
          "| ⛔ **Bulaşma GİDERİLMEDİ** | bu betik yalnız ölçer; eğitim "
          "kayıtları olduğu gibi duruyor ve karar ayrı bir iştir |",
          "| ⚠️ **Eval ögelerini de bu proje yazdı** | bağımsız bir sınama "
          "kümesi değil; bulaşma zaten yapısal olarak olası |"]

    RAPOR.write_text("\n".join(s) + "\n", encoding="utf-8")
    assert RAPOR.exists()
    print(f"⛔ {ortakli}/{len(cel)} eval ögesinde konu ortaklığı")
    for eid, sonda, en in satir:
        print(f"   {eid}: " + (f"#{en[0][1]} {en[0][2]} · {en[0][3][:4]}"
                               if en else "—"))
    print(f"⛔⛔ değer düzeyinde çakışma: {len(deger_cakisma)}")
    for a, b, c, _ in deger_cakisma:
        print(f"   {a} ↔ banka#{b}: «{c}»")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
