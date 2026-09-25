#!/usr/bin/env python3
"""Mühür açılmadan karar verilebilir mi — dejenerasyon ön koşulunun İKİNCİ OKUMASI (T87).

T82 dejenerasyon kapısını ekledi ama `golden_eval`'de **`on_kosul`'a koymadı**:
`tekrar` bayrağı cevabı **olan** kayıtları da yakalıyor ve onları ön koşula
eklemek `golden.locked` tabanının sayılarını **değiştirirdi** ⇒ K31 mührü
açılmadan verilemez.

⭐⭐ **Ama karar, mühür açılmadan da VERİLEBİLİR** — T62'nin yaptığı gibi:
mühürlü seti ve yayımlanmış tabanı **hiç değiştirmeden**, arşivlenmiş koşu
çıktıları üzerinde **iki okuma yan yana** hesaplanır.

  · **A okuması** — bugünkü `gecti` (yayımlanmış semantik, hiç dokunulmuyor)
  · **B okuması** — `dejenerasyon.tekrar` bir ön koşul olsaydı ne olurdu

⛔ **Hiçbir dosya değişmiyor, hiçbir sayı yeniden yayımlanmıyor.** Bu rapor
yalnızca *«mührü açtığımızda ne olacak»*ı **önceden** söylüyor ⇒ mühür
açılışında karar **hazır** olur, koşu sırasında tartışılmaz.

Girdi : reports/analiz/golden-kosu/*/sonuclar.jsonl (arşiv, yeniden koşu YOK) ·
        src/dejenerasyon.py
Çıktı : reports/analiz/2026-09-16-dejenerasyon-ikinci-okuma.md
Kullanım: uv run python scripts/analiz/2026-09-16-dejenerasyon-ikinci-okuma.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-dejenerasyon-ikinci-okuma.md"
KOSU = KOK / "reports/analiz/golden-kosu"
sys.path.insert(0, str(KOK / "src"))
import dejenerasyon as D  # noqa: E402


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def kayitlar():
    for d in sorted(KOSU.glob("*/sonuclar.jsonl")):
        for satir in d.read_text(encoding="utf-8").split("\n"):
            if satir.strip():
                try:
                    yield d.parent.name, json.loads(satir)
                except json.JSONDecodeError:
                    continue


def main() -> int:
    veri = [(k, r, D.denetle(r.get("thinking"), r.get("cevap")))
            for k, r in kayitlar()]
    # ⛔ Yalnızca hüküm TAŞIYAN kayıtlar: `gecti` alanı olmayan satır karşılaştırılamaz.
    hukum = [(k, r, d) for k, r, d in veri if "gecti" in r]

    a_gecen = sum(1 for _, r, _ in hukum if r["gecti"])
    # B okuması: `tekrar` bir ön koşul olsaydı — ön koşul varsa `gecti` False olur.
    b_gecen = sum(1 for _, r, d in hukum if r["gecti"] and not d["tekrar"])
    cevrilen = [(k, r, d) for k, r, d in hukum if r["gecti"] and d["tekrar"]]
    # Zaten kalmış ama `tekrar` da yanan kayıtlar — karar bunları etkilemez.
    zaten = [(k, r, d) for k, r, d in hukum if not r["gecti"] and d["tekrar"]]

    L: list[str] = []
    L += ["# Dejenerasyon ön koşulu — mühür açılmadan İKİNCİ OKUMA", "",
          f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
          f"**Girdi:** `reports/analiz/golden-kosu/*/sonuclar.jsonl` — "
          f"**{len(list(KOSU.glob('*/sonuclar.jsonl')))}** arşivlenmiş koşu "
          f"(yeniden koşu **YOK**)  ",
          f"**Girdi:** `src/dejenerasyon.py` SHA256 `{sha(KOK/'src/dejenerasyon.py')}` "
          f"(kapı **çağrılıyor**)", "", "---", "", "## Neden mühür açılmıyor", "",
          "T82 dejenerasyon kapısını ekledi ama `golden_eval`'de **`on_kosul`'a koymadı**:",
          "`tekrar` bayrağı cevabı **olan** kayıtları da yakalıyor ve onları ön koşula",
          "eklemek `golden.locked` tabanının sayılarını **değiştirirdi** ⇒ K31 mührü.", "",
          "⭐⭐ **Ama karar mühür açılmadan da verilebilir** — T62'nin yaptığı gibi:",
          "mühürlü set ve yayımlanmış taban **hiç değiştirilmeden**, arşivlenmiş koşu",
          "çıktıları üzerinde **iki okuma yan yana** hesaplanır. ⛔ Hiçbir dosya",
          "değişmiyor, hiçbir sayı yeniden yayımlanmıyor.", "", "---", "",
          "## 1. İki okuma", "", "| | |", "|---|---:|",
          f"| hüküm taşıyan arşiv kaydı | **{len(hukum)}** |",
          f"| **A okuması** — bugünkü `gecti` (yayımlanmış) | **{a_gecen}** |",
          f"| **B okuması** — `tekrar` ön koşul olsaydı | **{b_gecen}** |",
          f"| ⛔ **hükmü çevrilen** (geçti → kalırdı) | **{len(cevrilen)}** |",
          f"| ⚪ zaten kalmış, `tekrar` da yanıyor (karar etkilemez) | {len(zaten)} |", ""]

    if cevrilen:
        L += ["### ⛔ Hükmü çevrilecek kayıtlar", "",
              "| koşu | kayıt | distinct-5 | üretilen cevap |", "|---|---|---:|---|"]
        for k, r, d in sorted(cevrilen, key=lambda x: x[2]["distinct_5"])[:20]:
            c = " ".join((r.get("cevap") or "").split())[:56]
            L.append(f"| `{k}` | `{r.get('id')}` | {d['distinct_5']:.3f} | *«{c}»* |")
        L += ["",
              "⭐ Bu kayıtlar bugün **geçmiş** sayılıyor: cevap üretilmiş ve iddialar",
              "sağlanmış. ⛔ Ama muhakeme kendini tekrarlıyor ve cevap kırık — yani",
              "*«iddia sağlandı»* ile *«model çalıştı»* burada **ayrışıyor**.", ""]
    else:
        L += ["✅ **Hiçbir hüküm çevrilmiyor.**", "",
              "⭐⭐ **Karar böylece ucuzladı:** ön koşulu eklemenin yayımlanmış golden",
              "sayılarına etkisi **sıfır** ⇒ mühür açıldığında bu değişikliği yapmak",
              "tabanı **bozmaz**. ➡️ *Bir mührü açmadan önce, açtığında ne değişeceğini*",
              "*bilmek mührün maliyetini düşürür: karar koşu sırasında değil, ÖNCEDEN*",
              "*verilir ve koşu yalnızca uygular.*", ""]

    kosu_kir = collections.Counter(k for k, _, d in hukum if d["dejenere"])
    L += ["---", "", "## 2. Arşivde dejenerasyon dağılımı", "",
          "| koşu | dejenere | toplam |", "|---|---:|---:|"]
    top = collections.Counter(k for k, _, _ in hukum)
    for k, n in kosu_kir.most_common(10):
        L.append(f"| `{k}` | **{n}** | {top[k]} |")
    if not kosu_kir:
        L.append("| — | 0 | — |")
    L += ["",
          "## ⛔ Bu okumanın söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ **Mühür AÇILMADI** | hiçbir eval seti ve hiçbir yayımlanmış sayı "
          "değiştirilmedi; bu rapor yalnızca *«açıldığında ne olacak»*ı söylüyor |",
          "| ⛔ **Karar verilmedi** | ön koşulun eklenip eklenmeyeceği hâlâ bir karar; "
          "bu okuma onu **ucuzlatıyor**, yerine geçmiyor |",
          "| ⚠️ Yalnızca `golden-kosu` arşivi | Eksen 2/3/4/5 koşuları ayrı dizinlerde "
          "ve bu okumaya **dahil değil** |",
          "| ⚠️ `tekrar` eşiği **tek koldan** kalibre (T82) | B okuması o eşiğe bağlı |", ""]

    RAPOR.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print(f"   hüküm taşıyan kayıt {len(hukum)} · A geçen {a_gecen} · B geçen {b_gecen} · "
          f"çevrilen {len(cevrilen)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
