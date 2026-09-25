#!/usr/bin/env python3
"""Yayımlanmış her rapor, kendi betiğiyle yeniden üretilebiliyor mu?

⛔ **Neden var.** Kural 7 *«bir sayı raporlanıyorsa nasıl ölçüldüğü yazılı olmalı»*
diyor ve her rapor kendi betiğini adıyla taşıyor. Ama bunun **sınandığı** yer
yoktu: bir betiğin bugün hâlâ o raporu üretip üretmediği hiç ölçülmemişti.
2026-09-16'da tarih dönünce ortaya çıktı — 29 betik rapor adını `date.today()`'den
kuruyordu, yani hiçbiri ertesi gün kendi raporunu yeniden üretemiyordu.

⚠️ **Bu betik ÖTEKİ betikleri KOŞAR.** Bu yüzden:
  · çalışma ağacı **temiz** değilse hiç başlamaz,
  · her koşudan sonra `evals/`, `data/`, `reports/`, `runs/` **geri alınır**,
  · üretilen yeni (izlenmeyen) dosyalar **silinmez**, yalnızca raporlanır.

Sınıflar:
  ✅ aynı       — dosya baytı baytına aynı çıktı
  ⚠️ sıralama   — içerik aynı, satır sırası farklı (belirsiz tie-break)
  ⛔ kaydı      — sayılar değişti: rapor girdisinden KOPMUŞ
  ⛔ mühür      — mühürlü bir girdiyi yeniden yazmaya çalıştı (K31 kapısı durdurdu)
  ⛔ argüman    — komut satırı argümanı istiyor ve rapor onu kaydetmemiş
  ⛔ hata       — koşmuyor

Kullanım: uv run python scripts/analiz/2026-09-16-rapor-yeniden-uretilebilirlik.py
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (Kural 7).
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-rapor-yeniden-uretilebilirlik.md"
ANALIZ = KOK / "reports/analiz"
BEN = Path(__file__).name

GERI = ["evals", "data", "reports", "runs", "prompts", "configs", "plan.md",
        "PROJECT_MEMORY.md", "docs", "datasets"]
SURE = 240          # saniye; bundan uzun süren betik "zaman aşımı" sayılır
# ⛔ Model çağıran betikler KOŞULMAZ: pahalı, yavaş ve yeniden üretilebilirlikleri
# zaten modele bağlı (K97). Bunlar ayrı bir sınıf olarak raporlanır.
# ⛔ 2026-09-16 düzeltmesi: bu liste yalnızca yerel `llm`/`mlx` çağrılarını
# tanıyordu; ollama'yı HTTP ile çağıran betik "kararsız" diye işaretlendi. Model
# çağıran bir betik kararsız DEĞİL, yeniden üretilemezdir — ayrı sınıf.
MODELLI = ("import llm", "from llm", "mlx_lm", "import mlx",
           "11434", "ollama", "api/chat", "api/generate")


def git(*a) -> str:
    return subprocess.run(["git", "-C", str(KOK), *a],
                          capture_output=True, text=True).stdout


def temiz() -> list:
    """İZLENEN dosyalarda değişiklik var mı. İzlenmeyenler `git checkout`'tan
    etkilenmediği için engel değil (bu betiğin kendisi de öyle başlıyor)."""
    return [l for l in git("status", "--porcelain").splitlines()
            if not l.startswith("??")]


def geri_al() -> None:
    subprocess.run(["git", "-C", str(KOK), "checkout", "--", *GERI],
                   capture_output=True)


def esleme() -> dict:
    """rapor dosyası → onu ürettiğini SÖYLEYEN betik."""
    out = {}
    for p in sorted(ANALIZ.glob("*.md")):
        t = p.read_text(errors="ignore")
        # ⚠️ Başlıkta `betik ...` yazmayan raporlar da var; bu yüzden dosyanın
        # TAMAMINDA aranıyor ve ilk eşleşme alınıyor. Hiç betik adı geçmeyen rapor
        # zaten Kural 7'yi karşılamıyor demektir — ayrıca sayılıyor.
        m = re.search(r"[Bb]etik(?:ler)?[:*\s·]*`scripts/analiz/([A-Za-z0-9_.\-]+\.py)`", t)
        if m and (KOK / "scripts/analiz" / m.group(1)).exists():
            out.setdefault(m.group(1), []).append(p)
        elif not m:
            out.setdefault("", []).append(p)
    return out


def girdi_muhru(rapor: Path) -> str:
    """Rapor bir girdi SHA256'sı ilan etmiş mi, ve o SHA hâlâ tutuyor mu?

    ⭐ Kural 7 *«girdi dosyası + SHA256»* istiyor. Bunu yapan bir rapor, sayıları
    neden değiştiğini **kendi başına kanıtlayabilir**: mühür tutmuyorsa girdi
    değişmiştir. Yapmayan bir rapor, sapmanın sebebini gösteremez.
    """
    t = rapor.read_text(errors="ignore")
    hexler = {h[:16].lower() for h in re.findall(r"\b([0-9a-f]{16,64})\b", t)}  # lower-muaf: onaltılık hash — ASCII
    if not hexler:
        return "⛔ girdi SHA'sı **ilan edilmemiş** — sapmanın sebebi gösterilemiyor"
    yollar = [KOK / y for y in re.findall(r"`([A-Za-z0-9_./\-]+\.(?:jsonl|json|md|py|yaml))`", t)]
    tutan = 0
    for y in yollar:
        if y.is_file() and hashlib.sha256(y.read_bytes()).hexdigest()[:16] in hexler:
            tutan += 1
    return ("⚠️ girdi **DEĞİŞMİŞ** — ilan edilen SHA hiçbir girdiyle tutmuyor"
            if not tutan else
            f"✅ ilan edilen SHA {tutan} girdide hâlâ tutuyor — sapma başka sebepten")


DEFTER = json.loads((KOK / "reports/analiz/cagri-defteri.json")
                    .read_text(encoding="utf-8"))["cagrilar"]


def kosumlar(betik: str) -> list[list[str]]:
    """Betiğin çağrı(ları). Defterde yoksa tek argümansız koşum.

    ⛔ 2026-09-16: 7 betik komut satırı argümanı istiyordu ve argümanlar hiçbir
    yerde YAZILI DEĞİLDİ — raporların başlığında ilan edilmişlerdi ama
    çalıştırılabilir biçimde değil. Kural 7'nin *«betiği yazılı»* şartı
    karşılanmış görünüyordu; *«yeniden üretilebilir»* şartı karşılanmıyordu (T54).
    """
    return DEFTER.get(betik, [[]])


def kos(betik: str) -> subprocess.CompletedProcess:
    """Bütün koşumları sırayla çalıştırır; ilk hatada durur ve onu döndürür."""
    son = None
    for argv in kosumlar(betik):
        son = subprocess.run(
            [sys.executable, str(KOK / "scripts/analiz" / betik), *argv],
            capture_output=True, text=True, cwd=KOK, timeout=SURE)
        if son.returncode:
            break
    return son


def sirali_ayni(a: str, b: str) -> bool:
    return sorted(a.splitlines()) == sorted(b.splitlines())


def main() -> int:
    if temiz():
        print("⛔ Çalışma ağacı temiz değil — bu betik öteki betikleri koşuyor ve\n"
              "   çıktılarını geri alıyor. Önce değişikliklerini işle ya da sakla.")
        return 1

    sonuc = []
    for betik, raporlar in sorted(esleme().items()):
        if betik in ("", BEN):
            continue
        onceki = {p: p.read_text(encoding="utf-8") for p in raporlar}
        kaynak = (KOK / "scripts/analiz" / betik).read_text(errors="ignore")
        if any(x in kaynak for x in MODELLI):
            sonuc.append((betik, [p.name for p in raporlar], "⏭️ model",
                          "model çağırıyor — koşulmadı", []))
            continue
        try:
            r = kos(betik)
        except subprocess.TimeoutExpired:
            geri_al()
            sonuc.append((betik, [p.name for p in raporlar], "⏱️ zaman aşımı",
                          f"{SURE} sn içinde bitmedi", []))
            continue
        ciktilar = [l.split()[-1] for l in git("status", "--porcelain").splitlines()
                    if not l.startswith("??") or "reports/" in l]
        cikti_kume = {c for c in ciktilar}

        # ⛔ "MÜHÜR" alt dizesi YETMİYOR: `--yalniz-rapor` kipi de mühürden söz eden
        # bir bilgi satırı basıyor ve betik BAŞARIYLA bitiyor. Kapının ateşlediğini
        # gösteren şey çıkış koduyla birlikte gelen `⛔ MÜHÜR:` damgasıdır.
        if r.returncode and "⛔ MÜHÜR:" in (r.stdout + r.stderr):
            sinif, not_ = "⛔ mühür", "mühürlü girdiyi yeniden yazmaya çalıştı (K31 kapısı durdurdu)"
        elif r.returncode and "IndexError" in r.stderr and "argv" in r.stderr:
            sinif, not_ = "⛔ argüman", "komut satırı argümanı istiyor; rapor onu kaydetmemiş"
        elif r.returncode and not any(str(p.relative_to(KOK)) in cikti_kume
                                      for p in raporlar):
            sinif, not_ = "⛔ hata", (r.stderr.strip().splitlines() or ["?"])[-1][:80]
        else:
            degisen = [p for p in raporlar if p.read_text(encoding="utf-8") != onceki[p]]
            if not degisen:
                sinif, not_ = "✅ aynı", ""
            elif all(sirali_ayni(p.read_text(encoding="utf-8"), onceki[p])
                     for p in degisen):
                sinif, not_ = "⚠️ sıralama", "içerik aynı, satır sırası farklı"
            else:
                # ⭐ Asıl ayrım: betik KENDİ İÇİNDE mi kararsız, yoksa girdisi mi
                # değişmiş? İkinci kez koşup İKİ KOŞUYU birbiriyle karşılaştırmak
                # bunu doğrudan ayırır — yayımlanan dosyayla karşılaştırmak ayıramaz.
                kosu1 = {q: q.read_text(encoding="utf-8") for q in degisen}
                geri_al()
                kos(betik)
                kararsiz = any(q.read_text(encoding="utf-8") != kosu1[q]
                               for q in degisen)
                sinif = "⛔ kararsız" if kararsiz else "⛔ kaydı"
                not_ = ("⛔ **betik kendi içinde kararsız** — aynı girdiyle iki koşu "
                        "farklı çıktı veriyor" if kararsiz else
                        "iki koşu birbiriyle aynı, yayımlanan dosyadan farklı · " +
                        " · ".join(dict.fromkeys(girdi_muhru(q) for q in degisen)))
        ek = sorted(c for c in cikti_kume
                    if not any(c == str(p.relative_to(KOK)) for p in raporlar))
        sonuc.append((betik, [p.name for p in raporlar], sinif, not_, ek))
        geri_al()

    if temiz():
        print("⛔ Geri alma tamamlanamadı — elle bak:", git("status", "--porcelain")[:400])
        return 1

    say = {}
    for _b, _r, s, _n, _e in sonuc:
        say[s] = say.get(s, 0) + 1

    y = [
        "# Yayımlanmış raporlar kendi betikleriyle yeniden üretilebiliyor mu",
        "",
        f"*{TARIH} · betik `scripts/analiz/{BEN}`*",
        "*her betik koşuldu, çıktısı yayımlanan dosyayla karşılaştırıldı, sonra",
        "çalışma ağacı **geri alındı**; betik temiz olmayan bir ağaçta başlamaz*",
        "",
        "## Neden",
        "",
        "Kural 7 her raporun betiğini adıyla taşımasını istiyor ve bu kural tutuldu.",
        "Ama **tutulup tutulmadığı hiç sınanmamıştı**: bir betiğin bugün hâlâ o raporu",
        "ürettiği ölçülmedi. ⛔ 2026-09-16'da tarih dönünce açık kendiliğinden görüldü —",
        "48 betik rapor adını ya da tarih satırını `date.today()`'den kuruyordu ve",
        "hiçbiri ertesi gün kendi yayımlanmış raporunu yeniden üretemiyordu.",
        "",
        "⚠️ **Bu raporun ilk sürümü (aynı gün, commit `8314fbf`) kendi bulgusunu",
        "yanlış sınıflandırdı.** O koşuda 29 betik yamalanmıştı ve 21 rapor *«kaydı»*",
        "(girdi kaymış) diye işaretlendi. Yamanın eksik olduğu sonradan görüldü:",
        "raporuna tarih yazan **19 betik daha** vardı. Onlar da sabitlenince *«kaydı»*",
        "sayısı **21'den 3'e** düştü. ➡️ *Bir sınıflandırma, sınıflandırdığı kusurun",
        "kendisi tam onarılmadan okunursa en kalabalık kutu «sebebi bilinmiyor»",
        "kutusudur.* Bu yüzden sınama **onarımdan sonra yeniden koşuldu**.",
        "",
        "## Sonuç",
        "",
        "| | sayı |", "|---|---:|",
    ]
    for s in sorted(say, key=lambda x: (x[0] != "✅", x)):
        y.append(f"| {s} | **{say[s]}** |")
    adsiz = len(esleme().get("", []))
    y += [f"| **toplam** | **{len(sonuc)}** |", "",
          f"⚠️ Ayrıca **{adsiz}** rapor hiçbir betik adı taşımıyor ve bu sınamaya "
          "hiç giremiyor — Kural 7 onlarda **zaten** karşılanmamış.", "",
          "## Betik betik", "",
          "| Betik | rapor | sonuç | not |", "|---|---|---|---|"]
    for b, rl, s, n, ek in sonuc:
        y.append(f"| `{b}` | {', '.join('`' + x + '`' for x in rl)} | {s} | {n} |")
    y += [
        "",
        "## Sınıfların anlamı",
        "",
        "| sınıf | ne demek | ne yapılmalı |",
        "|---|---|---|",
        "| ✅ **aynı** | betik bugün de aynı dosyayı üretiyor | — |",
        "| ⚠️ **sıralama** | sayılar aynı, **satır sırası** farklı: bir yerde belirsiz "
        "tie-break var (`sorted(set(...))`) | ikincil anahtar eklenmeli; sayıları "
        "etkilemez ama *«yeniden üretilebilir»* iddiasını zayıflatır |",
        "| ⛔ **kaydı** | iki koşu **birbiriyle aynı**, yayımlanan dosyadan farklı: "
        "girdi ya da kod değişmiş | ⛔ yayımlanan sayı artık betiğin ürettiği sayı "
        "değil — rapor ya yenilenmeli ya girdisi sabitlenmeli |",
        "| ⛔ **kararsız** | aynı girdiyle **iki koşu birbirinden farklı**: betiğin "
        "içinde tohumsuz rastgelelik ya da belirsiz sıra var | ⛔ en ağır sınıf — "
        "rapor **hiçbir zaman** yeniden üretilemez; tohum sabitlenmeli |",
        "| ⛔ **mühür** | betik bir eval seti **üretiyor** ve mühürlü dosyayı yeniden "
        "yazmaya çalıştı (K31 kapısı durdurdu) | üretici ile raporlayıcı **ayrılmalı**: "
        "rapor, seti yeniden üretmeden yazılabilmeli |",
        "| ⛔ **argüman** | betik komut satırı argümanı istiyor ve **rapor onu "
        "kaydetmemiş** | çağrı satırı raporun başına yazılmalı |",
        "| ⛔ **hata** | bugün hiç koşmuyor | girdisi silinmiş olabilir (Kural 8) |",
        "| ⏭️ **model** | betik bir modeli çağırıyor; koşulmadı | yeniden üretilebilirliği "
        "zaten modele bağlı (K97) — ayrı bir soru |",
        "| ⏱️ **zaman aşımı** | sınama penceresine sığmadı | elle koşulmalı |",
        "",
        "⛔ **Bu tablo bir kusur listesi değil, bir ÖLÇÜM.** Bir raporun bugün yeniden",
        "üretilememesi onun yanlış olduğu anlamına gelmez; *«yeniden üretilebilir»*",
        "iddiasının **sınanmamış** olduğu anlamına gelir — ve artık sınanıyor.",
        "",
        "## ⛔ Bu sınamanın ölçmediği",
        "",
        "- **Raporun doğruluğu.** Ölçülen tek şey betik→dosya kararlılığı.",
        "- **Betiğin girdisini nereden aldığı.** Scratchpad'e bağlı betikler oturum",
        "  silinince *«hata»* sınıfına düşer; bu Kural 8'in bilinen bedeli.",
        "- **`runs/` altındaki koşular.** Onlar yeniden üretilmez, saklanır (Kural 7).",
    ]
    RAPOR.write_text("\n".join(y) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print("   " + " · ".join(f"{k} {v}" for k, v in sorted(say.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
