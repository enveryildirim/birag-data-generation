#!/usr/bin/env python3
"""Faz 4'ü bitirmek için ne kaldı — elle değil, `plan.md`'den TÜRETİLEREK.

⛔ T65'in dersi: *«elle tutulan bir durum tablosu iki ayrı yalan söyleyebilir —
durum bayatlar VE hiç uygulanmamış bir madde yıllarca işaretsiz durur.»* ⇒ Faz 4'ün
kalan işi bir cümleyle özetlenmiyor; `plan.md`'nin Faz 4 bölümündeki **her açık
madde** okunup **engel türüne** göre sınıflanıyor.

⭐⭐ **Asıl ayrım kalemlerin SAYISI değil, kimin elinde olduğu:**
  · **onay** — etik kurul / uzman / yürütücü / hukukçu. ⛔ Ben ilerletemem.
  · **mühür** — `K31` mührü açılmadan verilemez (ikinci set, `golden.locked`).
  · **ölçüm** — bugün yapılabilir; yalnız zaman ister.
  · **şerh** — kapanacak bir iş değil, **raporlama borcu**: tezde yazılacak bir
    sınırlılık. ⚠️ Bunları *«açık iş»* saymak kalan işi olduğundan büyük gösterir.

⛔ **Engel eşlemesi BİZİM okumamızdır** (Kural 6): betik anahtar sözcük arar ve
hangi sözcüğün hangi sınıfa gittiği aşağıda **ilan edilir**. Sınıflandırılamayan
madde `?` olarak **görünür kalır**, sessizce bir kovaya atılmaz.

Girdi : plan.md (Faz 4 bölümü)
Çıktı : reports/analiz/2026-09-16-faz4-kapanis-listesi.md
Kullanım: uv run python scripts/analiz/2026-09-16-faz4-kapanis-listesi.py
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from tohum_guvenlik import tr_fold  # noqa: E402
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-faz4-kapanis-listesi.md"
PLAN = KOK / "plan.md"

# ⭐ Engel eşlemesi — İLAN EDİLİYOR. Sıra önemlidir: ilk eşleşen kazanır,
#    çünkü bir madde hem «uzman» hem «ölçüm» sözcüğü taşıyabilir ve o zaman
#    ONAY baskındır (onay gelmeden ölçüm yapılamaz).
ENGEL = [
    ("onay", ["etik kurul", "yürütücü kalemi", "uzman kalemi", "uzman kararı",
              "uzman onayı", "hukukçu", "üniversite erişimi", "yürütücü onayı",
              "karar gerekiyor", "yürütücü"]),
    ("mühür", ["mühür", "ikinci set", "üçüncü set", "k31"]),
    ("şerh", ["sınırlılık", "tezde .{0,20}yazıl", "şerh", "kayda geçti",
              "raporda .{0,20}yazıl", "okunmalı"]),
    ("ölçüm", ["ölçülmeli", "ölçülmedi", "sınanmalı", "sınanmadı", "aranmalı",
               "yazılmalı", "koşulmalı", "doğrulanmalı", "eklenmeli", "gerekiyor"]),
]
# ⭐ Faz 4'ün ÇIKIŞ KAPISI — plan.md'nin kendi cümlesi.
CIKIS = "Çıkış kapısı: `test` eval'de plato + transfer korelasyonu sağlam"


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def faz4_maddeleri() -> tuple[list[str], list[str]]:
    """(açık, kapalı) — Faz 4 başlığı ile Faz 5 başlığı arasındaki maddeler."""
    satirlar = PLAN.read_text(encoding="utf-8").split("\n")
    bas = next(i for i, s in enumerate(satirlar) if s.startswith("### Faz 4"))
    son = next(i for i, s in enumerate(satirlar) if s.startswith("### Faz 5"))
    acik, kapali, tampon, tur = [], [], [], None
    for s in satirlar[bas:son]:
        m = re.match(r"^- \[([ x])\] (.*)", s)
        if m:
            if tampon:
                (acik if tur == " " else kapali).append(" ".join(tampon))
            tur, tampon = m.group(1), [m.group(2)]
        elif tampon is not None and s.startswith("      "):
            tampon.append(s.strip())
        elif tampon:
            (acik if tur == " " else kapali).append(" ".join(tampon))
            tampon, tur = [], None
    if tampon:
        (acik if tur == " " else kapali).append(" ".join(tampon))
    return acik, kapali


def sinifla(madde: str) -> str:
    """⛔⭐⭐ BU SATIR BİR HATANIN ÜSTÜNE YAZILDI — ailenin ONUNCU örneği.

    İlk sürüm `madde.lower()` kullanıyordu ve `"ÜNİVERSİTE ERİŞİMİ GEREKİYOR"`
    → `"üni̇versi̇te eri̇şi̇mi̇ gereki̇yor"` (İ → i + BİRLEŞEN NOKTA) olduğu için
    anahtar sözcükler **hiç eşleşmedi**: 64 maddenin **31'i** sınıflandırılamadı
    ve liste *«yarısı bilinmiyor»* dedi. ⚠️ Bu, T73'ün tuzağının **aynı oturumda
    üçüncü** tekrarı — ve bu kez ikincisi gibi yine YENİ yazılmış bir denetimde.

    ➡️ *Bir hata ailesi, aynı gün iki kez belgelenmiş olmasına rağmen aynı elden
    üçüncü kez çıkıyorsa, çözüm «dikkat etmek» değildir. `str.lower` Türkçe metinde
    yanlış VARSAYILANDIR ve erişilebilir olduğu sürece kullanılacaktır.*
    """
    # ⭐ Çıkış kapısının KENDİSİ bir iş değil, HEDEFtir — «açık madde» sayılması
    #    kalan işi olduğundan büyük gösterirdi.
    if madde.startswith("Çıkış kapısı") or madde.startswith("→ `datasets/v0.1.0/"):
        return "çıkış"
    d = tr_fold(madde)
    for ad, desenler in ENGEL:
        if any(re.search(tr_fold(k), d) for k in desenler):
            return ad
    return "?"


def baslik(madde: str) -> str:
    """Maddenin ilk kalın başlığı — yoksa ilk 90 karakter."""
    m = re.search(r"\*\*(.+?)\*\*", madde)
    t = m.group(1) if m else madde
    t = re.sub(r"[~`]", "", t).strip()
    return (t[:96] + "…") if len(t) > 96 else t


def main() -> int:
    acik, kapali = faz4_maddeleri()
    gruplar: dict[str, list[str]] = {}
    for m in acik:
        gruplar.setdefault(sinifla(m), []).append(m)

    L: list[str] = []
    L += ["# Faz 4'ü bitirmek için ne kaldı — `plan.md`'den türetildi", "",
          f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
          f"**Girdi:** `plan.md` SHA256 `{sha(PLAN)}` — Faz 4 bölümü", "", "---", "",
          "## Neden türetiliyor", "",
          "⛔ T65'in dersi: *elle tutulan bir durum tablosu iki ayrı yalan söyleyebilir —",
          "durum **bayatlar**, ve hiç uygulanmamış bir madde yıllarca **işaretsiz** durur.*",
          "⇒ Faz 4'ün kalan işi elle özetlenmiyor; bölümdeki **her** açık madde okunup",
          "**engel türüne** göre sınıflanıyor.", "",
          "⭐⭐ **Asıl ayrım kalemlerin sayısı değil, KİMİN ELİNDE olduğu.**", "",
          "| | |", "|---|---:|",
          f"| Faz 4 maddesi (toplam) | **{len(acik) + len(kapali)}** |",
          f"| ✅ kapalı | **{len(kapali)}** |",
          f"| açık | **{len(acik)}** |", "", "---", "",
          "## Açık maddeler — engel türüne göre", "", "| engel | madde | ben ilerletebilir miyim |",
          "|---|---:|---|"]
    aciklama = {
        "onay": "⛔ **hayır** — etik kurul · uzman · yürütücü · hukukçu",
        "mühür": "⛔ **hayır** — `K31` mührü açılmadan karar verilemez",
        "ölçüm": "✅ **evet** — yalnız zaman ister",
        "şerh": "⚠️ kapanacak iş **değil** — tezde yazılacak sınırlılık",
        "çıkış": "🎯 iş **değil** — Faz 4'ün HEDEFİ",
        "?": "❓ **mekanik olarak sınıflandırılamadı** — elle okundu, aşağıda",
    }
    for ad in ("onay", "mühür", "ölçüm", "şerh", "çıkış", "?"):
        n = len(gruplar.get(ad, []))
        if n:
            L.append(f"| **{ad}** | **{n}** | {aciklama[ad]} |")
    L += ["",
          "⚠️ **Sıra önemli:** bir madde hem *«uzman»* hem *«ölçülmeli»* sözcüğü",
          "taşıyabilir; o zaman **onay baskındır**, çünkü onay gelmeden ölçüm yapılamaz.",
          "Eşleme aşağıda ilan ediliyor ve sınıflandırılamayan madde `?` olarak",
          "**görünür kalır**.", "", "---", ""]

    for ad in ("onay", "mühür", "ölçüm", "şerh", "çıkış", "?"):
        if not gruplar.get(ad):
            continue
        L += [f"### {ad} — {len(gruplar[ad])} madde", ""]
        L += [f"· {baslik(m)}  " for m in gruplar[ad]] + [""]
        if ad == "?":
            L += ["⭐ **Elle okundu (Kural 6):** bu kovanın büyük çoğunluğu **kapanacak**",
                  "**iş değil, KAYIT** — ölçülmüş bir bulgunun şerhi ya da tezde",
                  "yazılacak bir sınırlılık (*«ERKEN DÖNEM KAYITLARI DENETLENEMEZ»*,",
                  "*«REPLAY SEYRELDİ»*, *«gürültü tabanı yansız değil»*). ⛔ İçlerinden",
                  "gerçekten **iş** olanlar: `T61`'in nedensellik deneyi (yeni judge",
                  "koşusu), `T34`'ün payda düzeltmesi, adım kontrolünün B/C/D/E'ye",
                  "genişletilmesi, `K108`'in Eksen 3 aleti ve dört doğrulanamayan",
                  "muafiyetin elle okunması.", "",
                  "⚠️ **Bu sayı mekanik değil, sınıflandırıcının SINIRIDIR ve öyle",
                  "bırakılıyor** — anahtar sözcük listesini bu 25 maddeye uydurmak",
                  "sınıflandırıcıyı kendi girdisine **aşırı uydurmak** olurdu ve",
                  "sonraki maddede yine tutmazdı.", ""]

    L += ["---", "", "## ⭐ Faz 4'ün çıkış kapısı", "",
          f"`plan.md`'nin kendi cümlesi: *«{CIKIS}»* → `datasets/v0.1.0/` + CARD.md +",
          "§8 rapor kanıtları.", "",
          "⛔⛔ **Kapı bugün açılamaz ve sebebi tek bir madde:** Pareto kapısının",
          "**birinci** basamağı (Eksen 2 gerilemesi = 0) üç taramada da beş kolun beşini",
          "eledi; kolları ayıracak tek şey **kriz dilimi** ve o **etik kurul**da.",
          "➡️ *Yani Faz 4'ün kalan işi bir liste değil, bir **kilit**: ölçüm kalemlerinin",
          "hepsi bitse bile kapı açılmıyor.*", "",
          "## ⛔ Bu listenin söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ **Engel eşlemesi bizim okumamızdır** (Kural 6) | anahtar sözcük araması; "
          "bir madde yanlış kovaya düşmüş olabilir. Eşleme yukarıda **ilan ediliyor** |",
          "| ⛔ **Sıra/öncelik yok** | liste ne yapılacağını söylüyor, hangi sırayla "
          "değil |",
          "| ⚠️ *«Ölçüm»* sınıfı **eşit büyüklükte değil** | bir satırlık şerh ile yeni "
          "bir judge koşusu aynı kovada |",
          "| ⛔ Faz 4 **dışındaki** engeller kapsam dışı | Faz 3'ün kapanamayan kalemi "
          "(vahşi doğa dilimi) burada görünmüyor ama Faz 4'ü de bekletiyor |", ""]

    RAPOR.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print(f"   Faz 4: kapalı {len(kapali)} · açık {len(acik)}")
    print("   " + " · ".join(f"{a} {len(gruplar.get(a, []))}"
                             for a in ("onay", "mühür", "ölçüm", "şerh", "?")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
