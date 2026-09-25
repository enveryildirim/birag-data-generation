#!/usr/bin/env python3
"""`is_negative` ölçüsünün NOKTALAMAYA bağımlılığı — kör noktası `register`
ile ilişkili mi?

⛔⛔ **Nereden çıktı.** v6-parti7 birleştirmesinde sıra kapısı `#27`'yi
yakaladı: blok kapısı kaydı «red» saymıştı, `beyan-metin-uyumu` saymadı.
Aynı ölçünün iki tanımı çarpıştı (K97'nin teması) ve bu kez ÇARPIŞMAYI
KARARA BAĞLAYAN ŞEY bir noktalama işaretiydi — kullanıcı turundaki eksik
soru işareti.

⭐ İki tanım:
  (a) **blok kapısı** — yalnız son asistan turunda red DESENİ arar.
  (b) **`beyan-metin-uyumu`** — deseni arar VE kullanıcı turunda bir
      TALEP işareti arar. Gerekçesi sağlam: red bir talep gerektirir
      (yoksa rol sınırı ya da bilgi sınırı ile karışır).

⛔ Ama (b)'nin talep sezici deseni `\\?` ile başlıyor ve geri kalan
alternatifleri de yazım varyantına duyarlı (`söyle`, `olur mu`, `mı$`).
Türkçe sohbette soru işaretini düşürmek `bozuk` kayıt düzeyinin tanımlayıcı
özelliklerinden biridir. ⇒ **Hipotez:** (b)'nin (a)'ya göre kaçırdığı
redler `bozuk` kayıtlarda yoğunlaşır; yani ölçü, ölçtüğü edimi değil
kullanıcının yazım alışkanlığını da ölçüyor olur.

⭐ Bu betik hipotezi KURMAZ, sayar. Üç sayı üretir:
  1. `bozuk` ve `duzgun` kayıtlarda kullanıcı turunun talep işareti taşıma
     oranı — *soru işareti düşme oranı doğrudan*;
  2. (a) diyor (b) demiyor olan kayıtların register dağılımı;
  3. (1)'in (2)'yi açıklamaya yetip yetmediği — yani (a)'nın red saydığı
     kayıtlar arasında talep işareti oranı.

⛔ **Bu bir düzeltme betiği DEĞİL.** Hiçbir kayda dokunmaz. Hangi tanımın
doğru olduğuna da karar vermez: (b)'nin talep şartı kavramsal olarak
haklıdır, sorgulanan şey şartın SEZİCİSİDİR.

Girdi : data/candidates/v6-parti*.jsonl (blok dosyaları hariç)
Çıktı : reports/analiz/2026-09-21-red-olcusunun-noktalama-bagimliligi.md
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]          # ⛔ K126: tarih betiğin ADINDAN
RAPOR = KOK / f"reports/analiz/{TARIH}-red-olcusunun-noktalama-bagimliligi.md"

# ⛔⛔ İKİSİ DE KOPYA DEĞİL, ALINTI. Tanımların sahibi şu iki betik ve burada
# yeniden tanımlanmıyorlar — karşılaştırılıyorlar (K97).
#   (a) scripts/analiz/2026-09-21-uretim-v6-parti7-blok*.py
#   (b) scripts/analiz/2026-09-20-beyan-metin-uyumu.py
RED_A = re.compile(r"veremem|söyleyemem|yapamam|bana düşmez|benim işim değil|"
                   r"yerine geçemem|karar veremem|bunu ben (söyle|belirle|yorumla)",
                   re.I)
RED_B = re.compile(r"veremem|söyleyemem|yapamam|bana düşmez|benim işim değil|"
                   r"yerine geçemem|karar veremem|cevabı bende yok|"
                   r"bunu ben (söyle|belirle|yorumla)", re.I)
TALEP = re.compile(r"\?|\bsöyle\b|\bsöyler misin\b|\bne yapayım\b|"
                   r"\bnasıl\b.*\bolur\b|\bolur mu\b|\bmı\b\s*$", re.I | re.M)


def _oku() -> list[dict]:
    kay = []
    for f in sorted(KOK.glob("data/candidates/v6-parti*.jsonl")):
        if ".blok" in f.name:
            continue
        for l in f.read_text(encoding="utf-8").splitlines():
            if l.strip():
                r = json.loads(l)
                r["_dosya"] = f.name
                kay.append(r)
    return kay


def _sha(ad: str) -> str:
    return hashlib.sha256((KOK / "data/candidates" / ad).read_bytes()).hexdigest()[:16]


def main() -> int:
    kay = _oku()
    # ⛔ Kayıt düzeyi `gen_meta.register`; yoksa kayıt sayımın dışında kalır ve
    #    bu rapor edilir (sessizce «duzgun» saymak sayıyı kayırır).
    sayim: dict[str, dict[str, int]] = {}
    kacan: list[tuple[str, int, str]] = []
    duzeysiz = 0
    for r in kay:
        gm = r["gen_meta"]
        dz = gm.get("register")
        if dz not in ("bozuk", "duzgun"):
            duzeysiz += 1
            continue
        d = sayim.setdefault(dz, {"n": 0, "talep": 0, "a": 0, "a_talep": 0, "kacan": 0})
        d["n"] += 1
        kul = " ".join(m["content"] for m in r["messages"] if m["role"] == "user")
        son = [m for m in r["messages"] if m["role"] == "assistant"][-1]["content"]
        t = bool(TALEP.search(kul))
        d["talep"] += t
        if RED_A.search(son):
            d["a"] += 1
            d["a_talep"] += t
            if not (RED_B.search(son) and t):
                d["kacan"] += 1
                kacan.append((r["_dosya"], gm.get("parti_sira", -1), dz))

    def yuz(a: int, b: int) -> str:
        return f"{a}/{b} (%{round(100 * a / b) if b else 0})"

    sat = [f"# `is_negative` ölçüsünün noktalamaya bağımlılığı", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           "**Girdi:** `data/candidates/v6-parti{1..7}.jsonl`  ", ""]
    sat += ["| dosya | SHA256-16 |", "|---|---|"]
    for f in sorted({r["_dosya"] for r in kay}):
        sat.append(f"| `{f}` | `{_sha(f)}` |")
    sat += ["", f"Okunan kayıt **{len(kay)}** · kayıt düzeyi beyan edilmemiş **{duzeysiz}** "
                f"(sayımın dışında)", ""]

    sat += ["## 1. Kullanıcı turunda talep işareti", "",
            "⭐ Doğrudan ölçüm: hipotezin dayandığı şey.", "",
            "| kayıt düzeyi | kayıt | talep işareti taşıyan |", "|---|---:|---:|"]
    for dz in ("duzgun", "bozuk"):
        d = sayim.get(dz)
        if d:
            sat.append(f"| `{dz}` | {d['n']} | {yuz(d['talep'], d['n'])} |")

    sat += ["", "## 2. (a) red diyor, (b) demiyor", "",
            "⛔ Bu kayıtlarda son asistan turunda red deseni VAR; (b) onları "
            "red saymıyor çünkü kullanıcı turunda talep işareti bulamıyor.", "",
            "| kayıt düzeyi | (a) red sayan | (b)'nin kaçırdığı |", "|---|---:|---:|"]
    for dz in ("duzgun", "bozuk"):
        d = sayim.get(dz)
        if d:
            sat.append(f"| `{dz}` | {d['a']} | {yuz(d['kacan'], d['a']) if d['a'] else '0/0'} |")

    # ⛔⛔ BU BÖLÜM SONRADAN EKLENDİ ve sebebi bu oturumun tekrarlayan hatası:
    # bir farkı, FARKIN GERÇEK OLDUĞUNU GÖSTERMEDEN bir olguya bağlamak
    # (T223'te bir kez çürüdü). %45 ile %34 arasındaki fark n=20 ve n=50'de
    # gözle ayırt edilemez ⇒ permütasyon.
    import random
    rng = random.Random(20260921)
    havuz = [(dz, 1) for dz in ("duzgun", "bozuk")
             for _ in range(sayim[dz]["kacan"])]
    havuz += [(dz, 0) for dz in ("duzgun", "bozuk")
              for _ in range(sayim[dz]["a"] - sayim[dz]["kacan"])]
    etiket = [dz for dz, _ in havuz]
    deger = [v for _, v in havuz]
    def _fark(et: list[str]) -> float:
        b = [v for e, v in zip(et, deger) if e == "bozuk"]
        d = [v for e, v in zip(et, deger) if e == "duzgun"]
        return abs(sum(b) / len(b) - sum(d) / len(d)) if b and d else 0.0
    gozlenen = _fark(etiket)
    B = 10000
    ust = 0
    for _ in range(B):
        rng.shuffle(etiket)
        ust += _fark(etiket) >= gozlenen - 1e-12
    p_deg = ust / B

    sat += ["", "## 2b. Register farkı gerçek mi — permütasyon", "",
            f"Gözlenen fark **{gozlenen:.3f}** (`bozuk` − `duzgun`, mutlak). "
            f"Etiketler {B} kez karıştırıldı (tohum 20260921); en az bu kadar "
            f"büyük fark üretme oranı **p = {p_deg:.3f}**.", "",
            ("⛔⛔ **Fark ayırt edilemiyor.** Register'a bağlanamaz."
             if p_deg > 0.05 else
             "⭐ Fark bu örneklemde gürültüyle açıklanmıyor."), "",
            "⭐⭐ Asıl sayı register'da değil TOPLAMDA: (a)'nın red saydığı "
            f"**{sum(sayim[d]['a'] for d in sayim)}** kaydın "
            f"**{sum(sayim[d]['kacan'] for d in sayim)}**'inde iki tanım "
            "ayrılıyor.", ""]

    sat += ["", "## 3. Kaçan kayıtlar", ""]
    if kacan:
        sat += ["| dosya | # | kayıt düzeyi |", "|---|---:|---|"]
        sat += [f"| `{f}` | {s} | `{d}` |" for f, s, d in sorted(kacan)]
    else:
        sat.append("Yok.")

    sat += ["", "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Hangi tanımın DOĞRU olduğu söylenmiyor** | (b)'nin talep şartı "
            "kavramsal olarak haklı: red bir talep gerektirir, yoksa rol sınırı ve "
            "bilgi sınırıyla karışır. Sorgulanan şey şart değil, şartın SEZİCİSİ |",
            "| ⛔ **Sezicinin kaçırdığı her kayıt gerçek red değildir** | desen (a) da "
            "bir sözlük; (a)'nın saydığı bir kayıt rol sınırı olabilir ⇒ bu tablo "
            "«kaçan red» değil, **iki tanımın ayrıldığı yer** sayımıdır |",
            "| ⛔ **Külliyatı ben yazdım (K30)** | kullanıcı turlarındaki noktalamayı "
            "da ben koydum; ölçülen şey gerçek kullanıcıların yazım alışkanlığı DEĞİL, "
            "benim `bozuk` register'ı kurarken kullandığım işaretler |",
            "| ⚠️ **Kayıt düzeyi bir IZGARA hücresi** | metinden ölçülmedi; "
            "`gen_meta.register`'dan okundu |"]

    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[sat.index("## 1. Kullanıcı turunda talep işareti"):]))
    print(f"\n→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
