#!/usr/bin/env python3
"""v0.0.9'un kümülatif yargılanmış dosyasını KAYNAK DEFTERİYLE kurar.

⛔⛔ **Neden var.** `data/judged/v0.0.7.jsonl` bir betikle değil elle
birleştirilmişti: hangi kaydın hangi dosyadan, hangi rubrik sürümüyle geldiği
hiçbir yerde yazılı değil ve dosya yeniden üretilemiyor. Kural 7 *«raporlanan
her sayının bir betiği ve girdi SHA256'sı olmalı»* diyor; bir veri kümesinin
kendisi de raporlanan bir şeydir.

➡️ *Elle birleştirilmiş bir kümülatif dosya, sürümler arası her karşılaştırmayı
denetlenemez yapar — çünkü iki sürüm arasındaki farkın NEREDEN geldiği ancak
dosyalar tekrar açılarak tahmin edilebilir.*

⭐ Kurgu: taban olarak `v0.0.7.jsonl` alınır (tarihsel katmanları taşır), sonra
**ilan edilmiş** değiştirme ve ekleme listeleri uygulanır. Her adım rapora
girer: kaç kayıt, hangi dosya, SHA256, rubrik.

⛔ Aynı `id` iki kez gelirse SONRAKİ kazanır ve bu **çakışma listesine yazılır**
— sessiz üzerine yazma yok.
"""
from __future__ import annotations
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TABAN = KOK / "data/judged/v0.0.8.jsonl"
CIKTI = KOK / "data/judged/v0.0.9.jsonl"
RAPOR = KOK / "reports/analiz/2026-09-17-v009-kaynak-defteri.md"

# ⭐ İLAN EDİLMİŞ KAYNAKLAR — sıra önemlidir, sonraki öncekini değiştirir.
KAYNAKLAR = [
 ("data/judged/v5-parti3.v7.v9.jsonl", "v5-parti3 — §5a⁗ çıkmaz düzeltmesi (2 kayıt)"),
 ("data/judged/v5-parti4.v5.v9.jsonl", "v5-parti4 — §5a⁗ çıkmaz düzeltmesi (4 kayıt)"),
 ("data/judged/v5-parti6.v6.v9.jsonl", "v5-parti6 — §5a⁗ çıkmaz düzeltmesi (3 kayıt)"),
 ("data/judged/v5-parti7.v6.v9.jsonl", "v5-parti7 — §5a⁗ çıkmaz düzeltmesi (1 kayıt)"),
 ("data/judged/v5-parti8.v6.v9.jsonl", "v5-parti8 — §5a⁗ (3) + tanı iddiası (1) + yapısal atıf (2)"),
]


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def _yukle(p: Path) -> list[dict]:
    return [json.loads(s) for s in p.read_text(encoding="utf-8").splitlines() if s.strip()]


def main() -> int:
    eksik = [y for y, _ in KAYNAKLAR if not (KOK / y).exists()]
    if eksik:
        print("⛔ Kaynak dosyalar hazır değil:")
        for y in eksik:
            print(f"   {y}")
        return 2

    havuz: dict[str, dict] = {r["id"]: r for r in _yukle(TABAN)}
    katman = [{"dosya": str(TABAN.relative_to(KOK)), "sha256_16": _sha(TABAN),
               "kayit": len(havuz), "rol": "taban", "not": "v0.0.8'in yargılanmış dosyası (kendisi de betikle kuruldu)"}]

    cakisma = []
    for yol, aciklama in KAYNAKLAR:
        p = KOK / yol
        rs = _yukle(p)
        yeni = degisen = 0
        for r in rs:
            if r["id"] in havuz:
                eski = havuz[r["id"]]
                if json.dumps(eski.get("messages"), ensure_ascii=False) != \
                   json.dumps(r.get("messages"), ensure_ascii=False):
                    cakisma.append({"id": r["id"][:16], "dosya": yol,
                                    "parti_sira": r.get("gen_meta", {}).get("parti_sira")})
                degisen += 1
            else:
                yeni += 1
            havuz[r["id"]] = r
        katman.append({"dosya": yol, "sha256_16": _sha(p), "kayit": len(rs),
                       "yeni": yeni, "degistirilen": degisen, "rol": "katman", "not": aciklama})

    satirlar = list(havuz.values())
    CIKTI.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in satirlar),
                     encoding="utf-8")

    rub = Counter((r.get("judge") or {}).get("prompt_version") or "yok (replay/yargısız)"
                  for r in satirlar)
    yargisiz = [r["id"][:16] for r in satirlar if not r.get("judge") and not r.get("replay")]
    guv = [r["id"][:16] for r in satirlar if (r.get("judge") or {}).get("klinik_guvenlik_ihlali")]

    sat = ["# v0.0.9 — kümülatif yargı dosyasının kaynak defteri", "",
           "**Betik:** `scripts/analiz/2026-09-17-v008-kumulatif.py` · **Tarih:** 2026-09-17", "",
           "## 1. Katmanlar (sıra önemlidir; sonraki öncekini değiştirir)", "",
           "| # | dosya | SHA256-16 | kayıt | yeni | değiştirilen | not |",
           "|---:|---|---|---:|---:|---:|---|"]
    for i, k in enumerate(katman):
        sat.append(f"| {i} | `{k['dosya']}` | `{k['sha256_16']}` | {k['kayit']} | "
                   f"{k.get('yeni','—')} | {k.get('degistirilen','—')} | {k['not']} |")
    sat += ["", f"⭐ **Sonuç: {len(satirlar)} tekil kayıt** · çıktı `{CIKTI.relative_to(KOK)}` "
            f"SHA256 `{_sha(CIKTI)}`", "",
            "## 2. ⛔ Aynı `id`, farklı metin", ""]
    if cakisma:
        sat += [f"**{len(cakisma)} kayıt** tabandakinden farklı metinle geldi. ⛔ Bu, "
                "v0.0.7 ile v0.0.8'in aynı `id` altında **farklı içerik** taşıdığı anlamına "
                "gelir ve iki sürümün puanları kayıt düzeyinde karşılaştırılamaz.", "",
                "| id | kaynak | parti sırası |", "|---|---|---:|"]
        for c in cakisma[:80]:
            sat.append(f"| `{c['id']}` | `{c['dosya']}` | {c['parti_sira']} |")
    else:
        sat.append("Yok.")
    sat += ["", "## 3. Rubrik karışımı (K137)", "", "| rubrik | kayıt |", "|---|---:|"]
    for k, v in rub.most_common():
        sat.append(f"| `{k}` | {v} |")
    sat += ["", "⚠️ **Farklı rubrik sürümleriyle verilmiş puanlar aynı tabloda "
            "havuzlanamaz** (K137: rubrik sürümü sıralamayı değiştiriyor).", "",
            "## 4. Kapı öncesi durum", "",
            f"- yargılanmamış (replay olmayan): **{len(yargisiz)}** "
            f"⇒ `build.py` bunları `judge_yok` ile eler (T121)",
            f"- klinik güvenlik ihlali: **{len(guv)}** ⇒ elenir", "",
            "## ⛔ Bu defterin söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **Taban katman türetilmedi** | `v0.0.7.jsonl` elle birleştirilmişti; "
            "bu betik onu bir bütün olarak alır ve İÇİNİ açıklayamaz |",
            "| ⛔ **Kalite değil köken** | tablo hangi kaydın nereden geldiğini söyler, "
            "iyi olup olmadığını söylemez |",
            "| ⚠️ Çakışma ölçütü yalnız `messages` | `gen_meta` ya da `judge` farkları "
            "çakışma sayılmıyor |", ""]
    RAPOR.write_text("\n".join(sat), encoding="utf-8")

    print(f"⭐ {len(satirlar)} tekil kayıt → {CIKTI.relative_to(KOK)}")
    print(f"   aynı id farklı metin: {len(cakisma)}")
    print(f"   yargılanmamış (replay değil): {len(yargisiz)}")
    print(f"   klinik güvenlik ihlali: {len(guv)}")
    print(f"   rubrik: {dict(rub)}")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
