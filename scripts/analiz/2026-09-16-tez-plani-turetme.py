#!/usr/bin/env python3
"""Tez planının §2 ve §4 tabloları REPODAN türetiliyor — elle bakımı bırakılıyor.

⛔ `docs/tez/tez-plani.md` 2026-09-12'de yazıldı ve o günden beri **elle**
güncellenmedi: §2'nin *«Sonuçlar 🔴 · Ablasyonlar 🔴 · Hata analizi 🔴»* satırları
o tarihte doğruydu, bugün değil. ⚠️ Bu T54'ün **EL** sınıfı — elle tutulan bir
durum tablosu, gerçekliğinden sessizce ayrılır ve kimse fark etmez.

⭐ Çözüm tabloyu doğru DOLDURMAK değil, **türetmek**: bölüm başına gereken
artefaktlar ilan edilir, varlıkları makineyle sınanır, durum çıkar.

⚠️ **Eşlemenin kendisi BİZİM kararımızdır** (Kural 6): *«hangi tez bölümü hangi
dosyadan yazılacak»* editoryal bir seçim, repodan türetilemez. Türetilen şey
yalnızca **durum** — ilan edilen artefakt duruyor mu, kaç tane.

⭐ Betik iki yere yazar: (a) denetim raporu, (b) `tez-plani.md` içindeki işaretli
bölgeler. (b) sayesinde tablo bir daha elle güncellenmez; işaret dışındaki her şey
olduğu gibi kalır.

Girdi : repo ağacı (ilan edilen yollar) · reports/analiz/2026-09-16-*.md
Çıktı : reports/analiz/2026-09-16-tez-plani-turetme.md
        + docs/tez/tez-plani.md içindeki `TÜRETİLEN:` işaretli bölgeler
Kullanım: uv run python scripts/analiz/2026-09-16-tez-plani-turetme.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]
PLAN = KOK / "docs/tez/tez-plani.md"
RAPOR = KOK / f"reports/analiz/{TARIH}-tez-plani-turetme.md"


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def bul(desen: str) -> list[Path]:
    """Yol ya da glob → bulunan dosyalar. Tek kaynak: repo ağacının kendisi."""
    if any(c in desen for c in "*?["):
        return sorted(KOK.glob(desen))
    y = KOK / desen
    return [y] if y.exists() else []


# ⚠️ EŞLEME BİZİM (Kural 6). Her bölüm: (ad, [(etiket, desen, en_az)]).
# `en_az` = bu desenden kaç dosya beklendiği; 1 = "var olsun yeter".
BOLUMLER: list[tuple[str, list[tuple[str, str, int]]]] = [
    ("1. Giriş — problem, motivasyon", [
        ("araştırma notları", "docs/arastirma-notlari.md", 1),
        ("kaynakça", "docs/tez/kaynakca.bib", 1)]),
    ("2. Literatür — empati, MI, BDT, nüks, kriz", [
        ("araştırma notları", "docs/arastirma-notlari.md", 1),
        ("kaynakça", "docs/tez/kaynakca.bib", 1)]),
    ("2.x Benzer çalışmalar — Türkçe ruh sağlığı NLP", [
        ("tarama belgesi", "docs/tez/benzer-calismalar.md", 1)]),
    ("3. Yöntem — veri üretim mimarisi", [
        ("plan", "plan.md", 1),
        ("üretim talimatı", "prompts/uretim-v*.md", 1),
        ("config", "configs/**/*.yaml", 3)]),
    ("3.x Alternatifler ve elenme gerekçeleri", [
        ("karar kaydı", "PROJECT_MEMORY.md", 1)]),
    ("4. Veri seti — taksonomi, karışım, kalite kapıları", [
        ("taksonomi", "configs/taxonomy.yaml", 1),
        ("veri kartı", "datasets/*/CARD.md", 3),
        ("yasak ifade / anti-pattern", "plan.md", 1)]),
    ("4.x Veri kökeni ve ön işleme", [
        ("normalize", "src/normalize.py", 1),
        ("manifest", "datasets/*/manifest.json", 3),
        ("kalite kapısı", "src/checks.py", 1)]),
    ("5. Deney kurulumu — modeller, hiperparametreler", [
        ("eğitim configi", "configs/training/*.yaml", 3),
        ("koşu configi", "runs/*/config.yaml", 10),
        ("eğitim kodu", "src/train.py", 1)]),
    ("6. Değerlendirme — 5 eksen, rubrik, uzman uyumu", [
        ("eval seti", "evals/*.jsonl", 4),
        ("judge rubriği", "prompts/judge-eksen1.v*.md", 5),
        ("uzman puanlaması", "reports/analiz/*uzman-puanlama*.md", 1)]),
    ("7. Sonuçlar — tablolar, şekiller", [
        ("eğitim koşusu", "runs/*/metrics.json", 10),
        ("tarama raporu", "reports/analiz/*lora-kapsam-taramasi*.md", 2),
        ("taban ölçümü", "reports/analiz/*eksen-baseline*.md", 1)]),
    ("8. Ablasyonlar", [
        ("doz-yanıt eğrisi", "reports/analiz/*doz-yanit-egrisi.md", 1),
        ("prompt dili ablasyonu", "reports/analiz/*prompt-dili-ablasyonu.md", 1),
        ("rol sınırı madde ablasyonu", "reports/analiz/*rol-siniri-ablasyonu.md", 1),
        ("muafiyet kapısı bozma deneyi", "reports/analiz/*muafiyet-kapisi-gucu.md", 1),
        ("iç muhakeme kapsam ablasyonu", "reports/analiz/*ic-muhakeme-sizintisi.md", 1)]),
    ("9. Hata analizi", [
        ("ham judge arşivi", "reports/analiz/ham-judge/*.jsonl", 20),
        ("kapı defteri", "reports/analiz/*v9-kapi-defteri.md", 1),
        ("eşleşme kusuru", "reports/analiz/*geriye-donuk-eslesme.md", 1),
        ("judge kapsama kalibrasyonu", "reports/analiz/*judge-kapsama-kalibrasyonu.md", 1)]),
    ("10. Tartışma, sınırlılıklar", [
        ("katkı defteri", "docs/tez/katki-defteri.md", 1),
        ("katkı defteri denetimi", "reports/analiz/*katki-defteri-denetimi.md", 1)]),
    ("11. Etik", [
        ("karantina kaydı", "data/guvenlik-karantinasi.jsonl", 1),
        ("etik kurul kaydı", "docs/tez/etik-kurul.md", 1)]),
    ("Ek. Yeniden üretilebilirlik", [
        ("kilit dosyası", "uv.lock", 1),
        ("yeniden üretilebilirlik denetimi", "reports/analiz/*rapor-yeniden-uretilebilirlik.md", 1),
        ("ilan edilen SHA denetimi", "reports/analiz/*ilan-edilen-sha-denetimi.md", 1)]),
]


def _tohumlu(y: Path) -> bool:
    return bool(re.search(r"^\s*seed:", (y.parent / "config.yaml").read_text(
        encoding="utf-8", errors="ignore"), re.M))


def _donanimli(y: Path) -> bool:
    d = json.loads(y.read_text(encoding="utf-8"))
    return any(k in d for k in ("donanim", "hardware", "cihaz"))


# §4 kontrol listesi — her madde MAKİNEYLE sınanan bir koşul.
def kontrol_listesi() -> list[tuple[str, bool, str]]:
    kosu = sorted(KOK.glob("runs/*/metrics.json"))
    ds = sorted(KOK.glob("datasets/*/manifest.json"))
    pyv = (KOK / ".python-version")
    out = [
        ("`uv.lock` commit edilir — tam sürüm ağacı",
         (KOK / "uv.lock").exists(), "`uv.lock`"),
        ("Python sürümü kilitli",
         pyv.exists() and pyv.read_text().strip().startswith("3.12"),
         f"`.python-version` = `{pyv.read_text().strip() if pyv.exists() else '—'}`"),
        ("Tüm rastgele tohumlar sabit ve kayıtlı",
         bool(kosu) and all(_tohumlu(y) for y in kosu),
         f"{sum(_tohumlu(y) for y in kosu)}/{len(kosu)} koşunun `config.yaml`'ında `seed:`"),
        ("Dataset sürümleri immutable + `manifest.json` (SHA256)",
         len(ds) >= 3 and all("sha256" in y.read_text(encoding="utf-8").lower() for y in ds),  # lower-muaf: JSON anahtarı `sha256` — ASCII
         f"{len(ds)} manifest, hepsinde SHA256"),
        ("Veri kartı her sürümde (`CARD.md`)",
         len(list(KOK.glob("datasets/*/CARD.md"))) == len(list(KOK.glob("datasets/v*"))),
         f"{len(list(KOK.glob('datasets/*/CARD.md')))}/"
         f"{len(list(KOK.glob('datasets/v*')))} sürümde `CARD.md`"),
        ("Prompt sürümleri sürümlenmiş dosyalarda",
         len(list(KOK.glob("prompts/judge-eksen1.v*.md"))) >= 5,
         f"{len(list(KOK.glob('prompts/*.md')))} prompt dosyası"),
        ("Her koşuda **süre** kaydedilir",
         bool(kosu) and all("sure_saniye" in json.loads(y.read_text(encoding='utf-8'))
                            for y in kosu),
         f"{sum('sure_saniye' in json.loads(y.read_text(encoding='utf-8')) for y in kosu)}"
         f"/{len(kosu)} koşuda `sure_saniye`"),
        ("Her koşuda **donanım** kaydedilir",
         bool(kosu) and all(_donanimli(y) for y in kosu),
         f"{sum(_donanimli(y) for y in kosu)}/{len(kosu)} koşuda donanım alanı"),
        ("Her koşuda **git commit** kaydedilir",
         bool(kosu) and all("git_rev" in json.loads(y.read_text(encoding='utf-8'))
                            for y in kosu),
         f"{sum('git_rev' in json.loads(y.read_text(encoding='utf-8')) for y in kosu)}"
         f"/{len(kosu)} koşuda `git_rev`"),
        ("`just` hedefleri tek komutla tekrar koşturur",
         (KOK / "justfile").exists(),
         f"`justfile` ({sum(1 for l in (KOK/'justfile').read_text(encoding='utf-8').split(chr(10)) if re.match(r'^[a-z][a-z0-9-]*:', l))} hedef)"
         if (KOK / "justfile").exists() else "—"),
        ("Her rapor betiğine bağlı ve yeniden üretiliyor (Kural 7)",
         (KOK / f"reports/analiz/{TARIH}-rapor-yeniden-uretilebilirlik.md").exists(),
         "`rapor-yeniden-uretilebilirlik.md`"),
        ("Raporların ilan ettiği SHA256 denetleniyor",
         (KOK / f"reports/analiz/{TARIH}-ilan-edilen-sha-denetimi.md").exists(),
         "`ilan-edilen-sha-denetimi.md`"),
    ]
    return out


def bolum_tablosu() -> tuple[list[str], dict]:
    sat = ["| Tez bölümü | İlan edilen artefakt | Bulunan | Durum |",
           "|---|---|---|---|"]
    say = {"✅": 0, "🟡": 0, "🔴": 0}
    for ad, gerek in BOLUMLER:
        parca, eksik, tam = [], [], 0
        for etiket, desen, en_az in gerek:
            n = len(bul(desen))
            parca.append(f"{etiket} `{desen}` → **{n}**")
            if n >= en_az:
                tam += 1
            else:
                eksik.append(etiket)
        durum = "✅" if tam == len(gerek) else ("🔴" if tam == 0 else "🟡")
        say[durum] += 1
        sat.append(f"| {ad} | " + "<br>".join(f"`{d}`" for _e, d, _n in gerek)
                   + " | " + "<br>".join(p.split("→ ")[1] for p in parca)
                   + f" | {durum}" + (f" — eksik: {', '.join(eksik)}" if eksik else "") + " |")
    return sat, say


IS_BAS = "<!-- TÜRETİLEN:{} başlangıç — elle düzenleme; `scripts/analiz/%s` üretir -->" % Path(__file__).name
IS_SON = "<!-- TÜRETİLEN:{} bitiş -->"


def bolgeyi_yaz(metin: str, ad: str, icerik: list[str]) -> str:
    """İşaretli bölgeyi değiştirir. ⛔ İşaret yoksa DOKUNMAZ ve bunu bildirir —
    sessizce dosyanın sonuna eklemek elle yazılmış bir bölümü gölgeleyebilirdi."""
    bas, son = IS_BAS.format(ad), IS_SON.format(ad)
    if bas not in metin or son not in metin:
        return metin
    i, j = metin.index(bas) + len(bas), metin.index(son)
    return metin[:i] + "\n" + "\n".join(icerik) + "\n" + metin[j:]


def main() -> int:
    sat, say = bolum_tablosu()
    kl = kontrol_listesi()
    tutan = sum(1 for _a, ok, _k in kl if ok)

    kl_sat = ["| | Kontrol | Repoda bulunan |", "|---|---|---|"]
    kl_sat += [f"| {'✅' if ok else '⛔'} | {ad} | {kanit} |" for ad, ok, kanit in kl]

    # --- tez planını güncelle -------------------------------------------------
    plan = PLAN.read_text(encoding="utf-8")
    yeni = bolgeyi_yaz(plan, "bolum-artefakt", sat)
    yeni = bolgeyi_yaz(yeni, "yeniden-uretilebilirlik", kl_sat)
    isaretli = yeni != plan or all(
        IS_BAS.format(a) in plan for a in ("bolum-artefakt", "yeniden-uretilebilirlik"))
    if yeni != plan:
        PLAN.write_text(yeni, encoding="utf-8")

    L = ["# Tez planı repodan türetildi — §2 ve §4 elle bakımdan çıktı", "",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
         f"**Yazdığı yer:** `docs/tez/tez-plani.md` — yalnızca `TÜRETİLEN:` işaretli bölgeler  ",
         "**Eşleme:** *«hangi bölüm hangi artefakttan yazılacak»* **bizim kararımız** "
         "(Kural 6); türetilen şey yalnızca **durum**", "", "---", "",
         "## Neden", "",
         "`tez-plani.md` 2026-09-12'de yazıldı ve elle güncellenmedi. §2'nin",
         "*«Sonuçlar 🔴 · Ablasyonlar 🔴 · Hata analizi 🔴»* satırları o gün doğruydu,",
         "bugün değil. ⚠️ Bu T54'ün **EL** sınıfı: elle tutulan bir durum tablosu",
         "gerçeğinden sessizce ayrılır. ➡️ *Çözüm tabloyu doğru doldurmak değil,",
         "TÜRETMEK — bir daha elle bakım istemesin.*", "",
         "## 1. Bölüm ↔ artefakt", ""] + sat + ["",
         f"**Durum:** ✅ {say['✅']} · 🟡 {say['🟡']} · 🔴 {say['🔴']} bölüm.", "",
         "## 2. Yeniden üretilebilirlik kontrol listesi", ""] + kl_sat + ["",
         f"**{tutan}/{len(kl)} kontrol tutuyor.**", "",
         "## ⛔ Bu türetmenin söylemedikleri", "", "| | |", "|---|---|",
         "| ⛔ **Eşleme türetilmedi** | hangi bölümün hangi artefakttan yazılacağı "
         "editoryal bir karar; betik onu **ilan eder**, repodan çıkarmaz (Kural 6) |",
         "| ⛔ **Varlık ≠ yeterlilik** | bir dosyanın durması o bölümün yazılabileceği "
         "anlamına gelmez; ölçülen şey **malzemenin varlığı**, olgunluğu değil |",
         "| ⛔ Onay durumları | etik kurul, danışman, uzman onayı repoda **yok** ve "
         "olamaz — §5 ve §7 elle kalmaya devam ediyor |",
         "| ⚠️ Sayılar glob'a bağlı | desen değişirse sayı değişir; desenler tabloda "
         "**açıkça yazılı** ki okuyucu neyin sayıldığını görsün |", ""]
    RAPOR.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print(f"   bölüm ✅{say['✅']} 🟡{say['🟡']} 🔴{say['🔴']} · kontrol {tutan}/{len(kl)}"
          + ("" if isaretli else " · ⚠️ tez-plani.md'de TÜRETİLEN işareti YOK, yazılmadı"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
