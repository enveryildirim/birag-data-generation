#!/usr/bin/env python3
# lower-muaf-dosya: denetimin KENDİSİ — `.lower()` dizgesini arıyor ve rapor metninde alıntılıyor (yapısal dışlama, T64'ün sınıfı)
"""Düz `str.lower()` artık YASAK — ve yasak denetime bağlandı (T86).

Bu oturumda Türkçe küçültme ailesinin **on bir** örneği sayıldı ve beşi
kapı/dönüştürücünün **içindeydi**. ⛔ İki kez de *«bunu artık biliyorum»*
dedikten **sonra**, yeni yazdığım denetim betiklerinde tekrarladı (T73'ün
beşinci örneği, T83'ün onuncusu). ➡️ *Bir hata ailesi aynı gün üç kez aynı
elden çıkıyorsa çözüm «dikkat etmek» değildir: yanlış varsayılan **erişilemez**
kılınmalıdır.* Bu betik erişilebilirliği ölçer.

⭐ **Muafiyet mekanizması var ve olması şart:** `.lower()` ASCII üzerinde
(onaltılık hash, İngilizce anahtar, dosya uzantısı) **doğrudur**. Muaf satır
`# lower-muaf: <gerekçe>` işareti taşır ⇒ ⛔ muafiyet **görünür** olur,
sessizce geçmez.

⚠️ **Kapsam kesme tarihiyle sınırlı (Kural 7):** `src/` her zaman denetlenir
(canlı kod). `scripts/analiz/` için kural **kesme tarihinden** itibaren işler —
geçmiş analiz betiklerinin raporları dondurulmuş ve onları değiştirmek Kural 7'yi
çiğnerdi. ⭐ *Bir kuralın geriye dönük borcu ileriye dönük yükümlülüğünden ayrı
bir sayıdır.*

Girdi : src/*.py · scripts/analiz/*.py
Çıktı : reports/analiz/2026-09-16-lower-denetimi.md
Kullanım: uv run python scripts/analiz/2026-09-16-lower-denetimi.py
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-lower-denetimi.md"
KESME = "2026-09-16"
MUAF = re.compile(r"#\s*lower-muaf:")
# ⭐ DOSYA düzeyi muafiyet: bütün işi ESKİ davranışı ölçmek olan betikler. Satır
#    satır işaretlemek 16 satıra aynı gerekçeyi yazdırırdı; gerekçe bir kez, en
#    üstte. ⛔ Yine de raporda **ilan ediliyor**.
MUAF_DOSYA = re.compile(r"#\s*lower-muaf-dosya:\s*(.+)")
# ⛔ `tohum_guvenlik` foldların TANIMLANDIĞI yer; kendi içinde `.lower()` kullanır.
DISLANAN = {"src/tohum_guvenlik.py"}
RISKLI = re.compile(r"\.lower\(\)|\.upper\(\)|re\.IGNORECASE|re\.I\b")


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def kod_satirlari(metin: str):
    """(satır no, satır) — yorum ve docstring satırları ELENİR.

    ⚠️ Kaba bir docstring takibi: üçlü tırnak sayarak. Tek satırlık docstring'ler
    ve tırnak içindeki üçlü tırnaklar yanlış sayılabilir; bu **bilerek** kaba,
    çünkü amaç kesin ayrıştırma değil, **kod satırında** riskli çağrı aramak.
    """
    icinde = False
    for i, s in enumerate(metin.split("\n"), 1):
        ac = s.count('"""') + s.count("'''")
        if icinde:
            if ac % 2:
                icinde = False
            continue
        if ac % 2:
            icinde = True
            continue
        if s.strip().startswith("#"):
            continue
        yield i, s


def dosya_muafiyeti(yol: Path) -> str | None:
    m = MUAF_DOSYA.search(yol.read_text(encoding="utf-8"))
    return m.group(1).strip() if m else None


def tara(yol: Path) -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
    """(borçlu, muaf) satırlar. Dosya muafiyeti varsa hepsi muaf sayılır."""
    dm = dosya_muafiyeti(yol)
    borclu, muaf = [], []
    for n, s in kod_satirlari(yol.read_text(encoding="utf-8")):
        if not RISKLI.search(s):
            continue
        (muaf if (dm or MUAF.search(s)) else borclu).append((n, s.strip()[:88]))
    return borclu, muaf


def main() -> int:
    L: list[str] = []
    dosyalar = ([p for p in sorted((KOK / "src").glob("*.py"))]
                + [p for p in sorted((KOK / "scripts/analiz").glob("*.py"))])
    canli, gecmis = [], []
    for p in dosyalar:
        rel = str(p.relative_to(KOK))
        if rel in DISLANAN:
            continue
        yeni = rel.startswith("src/") or p.name[:10] >= KESME
        (canli if yeni else gecmis).append(p)

    L += ["# Düz `str.lower()` denetimi — yasak artık sınanıyor", "",
          f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
          f"**Kapsam:** `src/*.py` (her zaman) + `scripts/analiz/*.py` "
          f"(**{KESME}**'dan itibaren)  ",
          f"**Dışlanan:** " + ", ".join(f"`{d}`" for d in sorted(DISLANAN))
          + " — foldların **tanımlandığı** yer", "", "---", "", "## Neden", "",
          "Bu oturumda ailenin **on bir** örneği sayıldı ve beşi kapı/dönüştürücünün",
          "**içindeydi**. ⛔ İkisi *«bunu artık biliyorum»* dedikten **sonra**, yeni",
          "yazılan denetim betiklerinde tekrarladı. ➡️ *Aynı gün üç kez aynı elden çıkan",
          "bir hata ailesinde çözüm «dikkat etmek» değildir; yanlış varsayılan*",
          "***erişilemez** kılınmalıdır.* Bu betik erişilebilirliği ölçer.", "",
          "⭐ **Muafiyet var ve olmalı:** `.lower()` ASCII üzerinde (hash, İngilizce",
          "anahtar, uzantı) **doğrudur**. Muaf satır `# lower-muaf: <gerekçe>` taşır ⇒",
          "muafiyet **görünür**, sessizce geçmez.", "", "---", ""]

    b_top = m_top = 0
    satirlar = []
    for p in canli:
        b, m = tara(p)
        b_top += len(b)
        m_top += len(m)
        if b or m:
            satirlar.append((str(p.relative_to(KOK)), b, m))

    L += ["## 1. Canlı kapsam", "", "| | |", "|---|---:|",
          f"| denetlenen dosya | **{len(canli)}** |",
          f"| ⛔ **borçlu satır** | **{b_top}** |",
          f"| ✅ muaf (gerekçeli) | {m_top} |", ""]
    if b_top:
        L += ["| dosya | satır | kod |", "|---|---:|---|"]
        for rel, b, _ in satirlar:
            for n, s in b:
                L.append(f"| `{rel}` | {n} | `{s}` |")
        L += [""]
    else:
        L += ["✅ **Borçlu satır yok.** Canlı kodda düz `.lower()`/`.upper()` yalnızca",
              "gerekçeli muafiyetle kullanılıyor.", ""]
    dm_liste = [(str(q.relative_to(KOK)), dosya_muafiyeti(q)) for q in canli
                if dosya_muafiyeti(q)]
    if dm_liste:
        L += ["### ✅ DOSYA düzeyi muafiyetler — gerekçeleriyle", "",
              "| dosya | gerekçe |", "|---|---|"]
        L += [f"| `{a}` | {b} |" for a, b in sorted(dm_liste)] + [""]
    satir_muaf = [(rel, n, s2) for rel, _, m in satirlar for n, s2 in m
                  if rel not in {a for a, _ in dm_liste}]
    if satir_muaf:
        L += ["### ✅ SATIR düzeyi muafiyetler", "", "| dosya | satır | kod |",
              "|---|---:|---|"]
        L += [f"| `{a}` | {n} | `{c}` |" for a, n, c in satir_muaf] + [""]

    gb = sum(len(tara(p)[0]) for p in gecmis)
    L += ["---", "", "## 2. ⚠️ Kesme öncesi — değiştirilmiyor", "",
          f"`scripts/analiz/` içinde **{len(gecmis)}** betik kesme tarihinden önce yazıldı",
          f"ve toplam **{gb}** riskli satır taşıyor. ⛔ Bunlar **kusur sayılmaz**: kural o",
          "gün yoktu ve raporları dondurulmuş (Kural 7). ⭐ *Bir kuralın geriye dönük",
          "borcu, ileriye dönük yükümlülüğünden ayrı bir sayıdır ve ikisi karıştırılırsa",
          "hiçbiri okunamaz.*", "",
          "⚠️ **Ama bu, o betiklerin doğru olduğu anlamına GELMEZ.** Raporlarından sayı",
          "alınırken bu şerh birlikte okunmalı — T51'in *«erken dönem kayıtları",
          "denetlenemez»* sınıfı.", "",
          "## ⛔ Bu denetimin söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ **Muafiyet gerekçesi okunmuyor** | işaretin **varlığı** sınanıyor, "
          "içeriği değil. Yanlış bir gerekçe de geçer ⇒ insan okuması gerekli |",
          "| ⛔ Docstring ayıklama **kaba** | üçlü tırnak sayımı; tek satırlık docstring "
          "ve tırnak içi tırnak yanlış sayılabilir. Bilerek kaba — amaç kesin ayrıştırma "
          "değil, kod satırında riskli çağrı aramak |",
          "| ⛔ `sorted(key=str.lower)` gibi **dolaylı** kullanımlar | desen `.lower()` "
          "çağrısını arıyor; `str.lower` referansı görünmez |",
          "| ⚠️ `re.IGNORECASE` **her zaman yanlış değil** | İngilizce kalıpta doğrudur; "
          "denetim onu da borç sayar ve muafiyet beklemesi **kasıtlıdır** — gerekçe "
          "yazılsın diye |", ""]

    RAPOR.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print(f"   canlı dosya {len(canli)} · ⛔ borçlu {b_top} · ✅ muaf {m_top} · "
          f"kesme öncesi {gb} (kapsam dışı)")
    return 1 if b_top else 0


if __name__ == "__main__":
    sys.exit(main())
