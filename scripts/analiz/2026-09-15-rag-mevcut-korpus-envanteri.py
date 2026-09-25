#!/usr/bin/env python3
"""R0 — İP3 tarafında zaten bir belge korpusu var mı, varsa bizim katmanımızı karşılıyor mu?

Kullanıcı 2026-09-15'te komşu klasörlere bakma izni verdi (Kural 1; kaynaklar
`plan.md` §0'a yazıldı). Bu betik YALNIZCA dizin bilgisi okur — dosya adı, boyut,
klasör. Belge içeriği okunmaz.

Soru üç katmanlı (plan.md §17.2): elimizdeki malzeme A (yordam/kurum), B (klinik/
psikoeğitim), yoksa C (deneyim/dil) katmanına mı düşüyor? Çünkü İP1'in ihtiyacı
A katmanı ve R1 (soru envanteri) tek gerçek cevheri gizlilik/kayıt sorularında buldu.

Girdi : birag-tubitak/3005-…Knowledge-base…zip (dizin) · datasets/md_rag_ressources/ · turkce/
Çıktı : reports/analiz/2026-09-15-rag-mevcut-korpus-envanteri.md
"""
from __future__ import annotations

import collections
import zipfile
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
KOMSU = KOK.parent / "birag-tubitak"
ZIP = KOMSU / "3005-Bagımlılık-Knowledge-base-20260217T184927Z-1-001.zip"
CIKTI = KOK / "reports/analiz/2026-09-15-rag-mevcut-korpus-envanteri.md"
TSV = KOK / "reports/analiz/2026-09-15-rag-mevcut-korpus-envanteri.tsv"

# Katman ataması dosya adından yapılır ve VEKİLDİR — içerik okunmadı.
KATMAN = {
    "türkce/YOK_TEZ": ("B", "akademik tez — klinik/psikoeğitim"),
    "türkce/Blog": ("C / B", "blog ve deneyim anlatısı; YEDAM yazıları kurumun ama yordam metni değil"),
    "türkce": ("B", "kitap ve klinik görüşme metni"),
    "ingilizce": ("B", "terapist el kitabı"),
    "ingilizce/Makale": ("B", "akademik makale"),
}


def zip_envanteri():
    z = zipfile.ZipFile(ZIP)
    kayit = []
    for i in z.infolist():
        if i.is_dir():
            continue
        ad = i.filename
        if not (i.flag_bits & 0x800):          # UTF-8 bayrağı yoksa cp437 okunmuş
            ad = ad.encode("cp437").decode("utf-8", "replace")
        p = ad.split("/")
        kayit.append(("/".join(p[1:-1]).replace("türkce", "türkce"), p[-1], i.file_size))
    return kayit


def main() -> None:
    kayit = zip_envanteri()
    klasor = collections.Counter(d for d, _, _ in kayit)
    boyut = collections.Counter()
    for d, _, s in kayit:
        boyut[d] += s

    md = sorted((KOMSU / "datasets/md_rag_ressources").rglob("*.md"))
    tr_md = sorted((KOMSU / "turkce").rglob("*.md"))
    yedam = [f for d, f, _ in kayit if "YEDAM" in f or "Yeşilay" in f]

    sat = [
        "# R0 — İP3 tarafındaki mevcut belge korpusu: var, ama bizim katmanımız yok",
        "",
        f"**Girdi:** `birag-tubitak/` (dizin taraması; belge içeriği OKUNMADI) · "
        f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}",
        "",
        "---",
        "",
        "## 1. Ne var",
        "",
        f"**`3005-Bagımlılık-Knowledge-base` — {len(kayit)} belge · {sum(boyut.values())/2**20:.0f} MB**",
        "",
        "| klasör | belge | boyut | tahmini katman (§17.2) |",
        "|---|---|---|---|",
    ]
    for d, n in klasor.most_common():
        k, aciklama = KATMAN.get(d, ("?", ""))
        sat.append(f"| `{d}` | {n} | {boyut[d]/2**20:.0f} MB | **{k}** — {aciklama} |")

    sat += [
        "",
        f"**Ayrıca dönüştürülmüş markdown:** `datasets/md_rag_ressources/` **{len(md)}** dosya"
        f" · `turkce/` **{len(tr_md)}** dosya",
        "",
        "## 2. Üç bulgu",
        "",
        "### 2.1 Türkçe taraf dönüştürülmemiş — ve K90 tam tersini istiyor",
        "",
        f"Arşivde **{klasor['türkce/YOK_TEZ'] + klasor['türkce/Blog'] + klasor['türkce']}** Türkçe PDF var;"
        f" dönüştürülmüş Türkçe markdown **{len(tr_md)}**. Buna karşılık İngilizce taraf"
        f" **{len(md)}** markdown'a dönüştürülmüş.",
        "",
        "K90 çeviri Türkçesinde kusur oranını %80-83, elle yazılanda %16 ölçmüştü. Yani",
        "hazırlık emeği, **düşük değerli** tarafa harcanmış: 104 YÖK tezi Türkçe-özgün",
        "akademik metindir ve bu korpusun en değerli, en el değmemiş parçasıdır.",
        "",
        "### 2.2 A katmanı içeriği yok",
        "",
        f"YEDAM/Yeşilay adı geçen **{len(yedam)}** belgenin tamamı **blog yazısı**:",
        "",
        *[f"- {f}" for f in sorted(yedam)],
        "",
        "Bunlar deneyim anlatısı ve psikoeğitim; **başvuru yordamı, gizlilik politikası,",
        "ücret, uygunluk metni değil.** R1'in tek gerçek cevheri tam da orasıydı:",
        "*\"kayıt aileme gider mi, sicilime düşer mi\"*, *\"siz aileme söylemezsiniz değil mi\"*.",
        "**Bu korpus o soruyu cevaplayamaz.**",
        "",
        "### 2.3 Dönüşüm kalitesi ve negatif alan",
        "",
        "İki örnek dosya açıldı:",
        "",
        "- `md_rag_ressources/.../gambling1.md` (644 KB) — YAML künyesi **var**"
        " (`source_file`, `folder`, `date`; lisans alanı **yok**), ama metin ham PDF çıkarımı:"
        " `(Page 2)` işaretleri ve sözcük başına satır kırılması. Kitap başına **tek dosya**,"
        " chunk yok.",
        "- `turkce/alkol/1.md` — Yeşilay sayfası, **temiz Türkçe**. Ama içeriği"
        " yoksunluk belirtileri, *\"6-8 saat sonra\"* zaman çizelgesi, *\"ölüm riski\"*:"
        " §17.3'ün **negatif alanı**. Mevcut malzemenin bir kısmı RAG havuzuna"
        " **olduğu gibi giremez**.",
        "",
        "## 3. Sonuç — plan değişmiyor, R2 netleşiyor",
        "",
        "| Katman | Durum |",
        "|---|---|",
        "| **A — yordam/kurum** | ⛔ korpusta **yok**. R2 için hâlâ dışarı çıkmak gerekiyor |",
        "| **B — klinik/psikoeğitim** | ✅ bol miktarda var (104 tez + 37 kitap/makale). Toplama işi bitmiş, **tasnif ve negatif alan ayıklaması** işi başlıyor |",
        "| **C — deneyim/dil** | ✅ 24 blog. §17.2 gereği RAG havuzuna girmez; kullanıcı register'ı için değerli |",
        "",
        "⚠️ **Sınır:** katman ataması dosya adından yapıldı, **içerik okunmadı**. Bir",
        "belgenin gerçekten hangi katmana düştüğü ancak açılınca bilinir; bu envanter",
        "hangisinin açılmaya değer olduğunu söyler, ne içerdiğini değil.",
        "",
    ]
    CIKTI.write_text("\n".join(sat), encoding="utf-8")

    # Çalışma listesi: R2 kaynak haritasının arşiv tarafı bunun üstüne kurulur.
    tsv = ["klasor\tkatman_tahmini\tdil\tboyut_kb\tdosya"]
    for d, f, s_ in sorted(kayit):
        k, _ = KATMAN.get(d, ("?", ""))
        dil = "tr" if d.startswith("türkce") else "en"
        tsv.append(f"{d}\t{k}\t{dil}\t{s_//1024}\t{f}")
    for f in md:
        tsv.append(f"md_rag_ressources\tB\ten\t{f.stat().st_size//1024}\t{f.name}")
    for f in tr_md:
        tsv.append(f"turkce (md)\tB\ttr\t{f.stat().st_size//1024}\t{f.name}")
    TSV.write_text("\n".join(tsv) + "\n", encoding="utf-8")

    print(f"{len(kayit)} belge · md {len(md)} · tr_md {len(tr_md)} · YEDAM {len(yedam)} · tsv {len(tsv)-1}")
    print(CIKTI.relative_to(KOK))


if __name__ == "__main__":
    main()
