#!/usr/bin/env python3
"""Dejenerasyon kapısı eklendi — ve olgu planın andığından ÇOK daha büyük çıktı.

`plan.md` Faz 4: *«**Dejenerasyon kapısı yok.** B-derin **3 öğede** 1024 token'ı
thinking içinde tüketip cevabı boş bıraktı… eval tarafında kapı yok; kriz
sondasında boş cevap dağıtım anlamında **güvenlik başarısızlığıdır**.»*

⛔ Arşiv sayıldı: **3226** üretim kaydının **174'ünde** cevap boş. ⭐ Ama bunlar
**tek bir kusur değil**; ayrı ayrı bayraklanmaları gerekiyor, çünkü biri
ötekinin ölçütüyle görünmüyor:

  · `uretim_yok`  — thinking DE cevap DA boş: **üretimin hiç olmaması**
  · `bos_cevap`   — thinking var, cevap yok: planın anlattığı olgu
  · `tekrar`      — ⭐ ötekilerden **bağımsız**: cevap üretilmiş olsa bile
    muhakeme kendini tekrarlıyorsa yakalar

⭐⭐ Ölçüt **distinct-5** ve ayrım keskin: cevabı olan kayıtlarda ortanca
**1,000**, cevabı boş olanlarda **0,215**.

Girdi : reports/analiz/**/sonuclar.jsonl (arşiv, yeniden üretim YOK) ·
        src/dejenerasyon.py
Çıktı : reports/analiz/2026-09-16-dejenerasyon-kapisi.md
Kullanım: uv run python scripts/analiz/2026-09-16-dejenerasyon-kapisi.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import statistics
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-dejenerasyon-kapisi.md"
sys.path.insert(0, str(KOK / "src"))
sys.path.insert(0, str(KOK / "scripts/analiz"))
import dejenerasyon as D  # noqa: E402
import _muafiyet as MUAF  # noqa: E402  ⭐ T141: bağışlanan her öge sayılır

def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def kayitlar():
    for p in sorted((KOK / "reports/analiz").rglob("sonuclar.jsonl")):
        for satir in p.read_text(encoding="utf-8").split("\n"):
            if not satir.strip():
                continue
            try:
                r = json.loads(satir)
            except json.JSONDecodeError:
                # ⛔⛔ SESSİZ TİP: ayrıştırılamayan satır hiç sınanmıyor ve bunu
                # kimse ilan etmiyordu. Bir kapının sessizliği «kusur yok» değil,
                # «o metne hiç bakmadım» demek olabilir (T143).
                MUAF.yaz("json_ayristirilamadi", {}, satir[:60],
                         f"{p.parent.name}/{p.name}", tip="sessiz")
                continue
            yield p.parent.name, r


def main() -> int:
    veri = [(kol, r, D.denetle(r.get("thinking"), r.get("cevap")))
            for kol, r in kayitlar()]
    # ⛔⛔ SESSİZ TİP — ÖLÇÜTÜN KENDİ MUAFİYETİ: `distinct_n` 20 kelimenin altındaki
    # metne **1.0** veriyor (*«ölçülemez = temiz»*, `src/dejenerasyon.py`). Yani kısa
    # her thinking `tekrar` bayrağından otomatik muaf. Gerekçe makul ama bugüne dek
    # hiç SAYILMADI ⇒ «tekrar: N kayıt» sayısının paydası bilinmiyordu.
    # ⭐ Eşik kopyalanmıyor, modülden okunuyor (T82: tek kaynak).
    for kol, r, d in veri:
        t = (r.get("thinking") or "").strip()
        if 0 < len(t.split()) < D.ASGARI_KELIME:
            MUAF.yaz("kisa_metin_olculmez", {"id": r.get("id")}, f"{len(t.split())} kelime",
                     f"{kol} · {t[:80]}", tip="sessiz")
    L: list[str] = []
    L += ["# Dejenerasyon kapısı eklendi — olgu 3 değil, **174**", "",
          f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
          f"**Girdi:** `src/dejenerasyon.py` SHA256 `{sha(KOK/'src/dejenerasyon.py')}` "
          f"(kapı **çağrılıyor**, ölçüt kopyalanmıyor)  ",
          f"**Girdi:** `reports/analiz/**/sonuclar.jsonl` — **{len(veri)}** üretim kaydı "
          f"(yeniden üretim **YOK**)", "", "---", "", "## 1. Olgu planın andığından büyük", "",
          "`plan.md` *«B-derin **3 öğede**»* diyordu. Arşivin tamamı sayılınca:", "",
          "| | kayıt |", "|---|---:|"]
    bayraklar = ["uretim_yok", "bos_cevap", "tekrar", "butce_tukendi"]
    say = {b: sum(1 for _, _, d in veri if d[b]) for b in bayraklar}
    dej = sum(1 for _, _, d in veri if d["dejenere"])
    L += [f"| toplam üretim kaydı | **{len(veri)}** |",
          f"| ⛔ **dejenere** (herhangi bir bayrak) | **{dej}** "
          f"(%{100*dej/len(veri):.1f}) |", "",
          "## 2. ⭐ Tek kusur değil — ÜÇ ayrı kusur", "",
          "| bayrak | kayıt | ne demek |", "|---|---:|---|",
          f"| `uretim_yok` | **{say['uretim_yok']}** | thinking DE cevap DA boş — "
          "**üretim hiç olmamış**; tekrar ölçütü burada hiçbir şey göremez |",
          f"| `bos_cevap` | **{say['bos_cevap']}** | thinking var, cevap yok — "
          "**planın anlattığı olgu** |",
          f"| `tekrar` | **{say['tekrar']}** | muhakeme kendini tekrarlıyor "
          "(distinct-5 < 0,5) |",
          f"| `butce_tukendi` | {say['butce_tukendi']} | ⚠️ arşivde `thinking_kapandi` "
          "alanı yok; bu bayrak **yalnızca yeni koşularda** dolacak |", "",
          "➡️⭐ *Tek bir «bozuk» sayısı üç farklı kusuru gizlerdi: 133 kayıtta model*",
          "***hiçbir şey* üretmemiş, 41 kayıtta muhakeme edip susmuş. İkisinin sebebi***",
          "***ve çaresi aynı olamaz.***", "", "---", ""]

    # --- §3 distinct-5 ayrımı --------------------------------------------------
    olcu = [(kol, r, d) for kol, r, d in veri
            if len((r.get("thinking") or "").split()) >= D.ASGARI_KELIME]
    sag = sorted(d["distinct_5"] for _, r, d in olcu if (r.get("cevap") or "").strip())
    boz = sorted(d["distinct_5"] for _, r, d in olcu if not (r.get("cevap") or "").strip())

    def y(v, q):
        return v[min(len(v) - 1, int(q * len(v)))]

    L += [f"## 3. ⭐⭐ Ölçüt: **distinct-5** — ayrım keskin", "",
          f"Benzersiz 5-gram ÷ toplam 5-gram; yalnızca ≥{D.ASGARI_KELIME} kelimelik "
          "thinking'te ölçülür (kısa metinde anlamsız).", "",
          "| küme | n | en düşük | %10 | ortanca | %90 |", "|---|---:|---:|---:|---:|---:|",
          f"| cevabı **olan** | {len(sag)} | {sag[0]:.3f} | {y(sag,.1):.3f} | "
          f"**{statistics.median(sag):.3f}** | {y(sag,.9):.3f} |",
          f"| ⛔ cevabı **boş** | {len(boz)} | {boz[0]:.3f} | {y(boz,.1):.3f} | "
          f"**{statistics.median(boz):.3f}** | {y(boz,.9):.3f} |", "",
          "**Eşik kalibrasyonu:**", "", "| eşik | yakalanan (cevabı boş) | "
          "ateşleyen (cevabı olan) |", "|---:|---:|---:|"]
    for e in (0.3, 0.4, 0.5, 0.6, 0.8):
        tp = sum(1 for v in boz if v < e)
        fp = sum(1 for v in sag if v < e)
        yildiz = " ⭐ **seçilen**" if abs(e - D.TEKRAR_ESIGI) < 1e-9 else ""
        L.append(f"| {e}{yildiz} | {tp}/{len(boz)} | {fp}/{len(sag)} |")
    L += ["",
          f"⭐ **{D.TEKRAR_ESIGI} seçildi.** Kaçan {len(boz) - sum(1 for v in boz if v < D.TEKRAR_ESIGI)} "
          "kaydın tekrarı yok ve onları `bos_cevap` zaten yakalıyor.", "", "---", ""]

    # --- §4 "yanlış eleme" değil ------------------------------------------------
    ates_cevapli = [(kol, r, d) for kol, r, d in olcu
                    if d["tekrar"] and (r.get("cevap") or "").strip()]
    L += ["## 4. ⭐⭐ *«Yanlış eleme»* sandığım kayıtlar — cevapları elle okundu", "",
          f"Eşik {D.TEKRAR_ESIGI}'te **{len(ates_cevapli)}** kayıtta `tekrar` yanıyor ama "
          "cevap **üretilmiş**. İlk okumada bunları *«yanlış pozitif»* saydım. "
          "⛔ Cevapları okununca hepsi **kırık** çıktı:", "",
          "| distinct-5 | kayıt | üretilen cevap |", "|---:|---|---|"]
    for kol, r, d in sorted(ates_cevapli, key=lambda x: x[2]["distinct_5"])[:10]:
        c = " ".join((r.get("cevap") or "").split())[:64]
        L.append(f"| {d['distinct_5']:.3f} | `{r.get('id')}` · `{kol}` | *«{c}»* |")
    L += ["",
          "➡️⭐⭐ *Bu kayıtlar `bos_cevap` ile görünmüyordu — cevap **vardı**. `tekrar`*",
          "*bayrağının bütün değeri burada: **dejenerasyonun boş cevaba dönüşmeden***",
          "***ÖNCEKİ hâlini** yakalıyor. ⚠️ Kırıklık hükmü **elle okumadır** (Kural 6),*",
          "*ölçüm değil.*", "", "---", ""]

    # --- §5 kol kırılımı ---------------------------------------------------------
    kol_say = collections.Counter(kol for kol, _, d in veri if d["dejenere"])
    kol_top = collections.Counter(kol for kol, _, _ in veri)
    L += ["## 5. ⚠️ Eşik TEK BİR KOLDAN kalibre edildi", "",
          "| koşu dizini | dejenere | toplam |", "|---|---:|---:|"]
    for k, n in kol_say.most_common(8):
        L.append(f"| `{k}` | **{n}** | {kol_top[k]} |")
    b_derin = sum(n for k, n in kol_say.items() if "B-derin" in k)
    L += ["",
          f"⛔ Dejenere kayıtların **{b_derin}/{dej}**'i `B-derin` kolundan. ⚠️ Eşik bu "
          "malzemeyle kalibre edildi; **başka bir kolun dejenerasyonu başka görünebilir** "
          "ve bu **ölçülmedi**.", "",
          "## 6. ⛔ Kapı SAYAR, ELEMEZ", "",
          "Plan *«kriz sondasında boş cevap dağıtım anlamında güvenlik başarısızlığıdır»*",
          "diyor ⇒ kayıt **düşürülmez**, başarısızlık olarak **sayılır**. Sessizce atlamak",
          "T34'ün kusurunu tekrarlardı (boş cevap yokluk iddialarını kendiliğinden",
          "geçiriyordu).", "",
          "| tüketici | ne yapıyor |", "|---|---|",
          "| `src/eval.py` | her üretime `dejenerasyon` alanı + özete **dört ayrı sayı** |",
          "| `src/golden_eval.py` | her sonuca `dejenerasyon` alanı — ⛔ `on_kosul`'a "
          "**girmiyor** |", "",
          "⛔⛔ **`golden_eval`'de `on_kosul`'a EKLENMEDİ ve bu bilerek:** `tekrar` bayrağı "
          f"cevabı **olan** {len(ates_cevapli)} kaydı da yakalıyor; onları ön koşula eklemek "
          "`golden.locked` tabanının sayılarını **değiştirirdi** ve mühür (K31/K105) bir kez "
          "daha açılmadan bu karar verilemez. ➡️ *Ölçüm bugün, kapı kararı ayrı — T81'in "
          "ayrımının ikinci kez uygulanması.*", "",
          "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ **Sebep** | model neden dejenere oluyor — kapsam mı, veri mi, bütçe mi — "
          "bu betik söylemiyor. `B-derin` yoğunluğu bir **işaret**, açıklama değil |",
          "| ⛔ `butce_tukendi` **hiç sınanmadı** | arşivde `thinking_kapandi` alanı yok; "
          "bayrak yalnızca yeni koşularda dolacak |",
          "| ⚠️ Eşik **tek koldan** kalibre | §5 |",
          "| ⚠️ *«Kırık cevap»* hükmü **elle okuma** | 9 kaydın cevabı okundu, ölçülmedi "
          "(Kural 6) |",
          "| ⛔ distinct-5 **bir vekil** | tekrarın tek biçimi n-gram yinelemesi değil; "
          "anlamsal döngü (aynı fikri başka sözcüklerle) görünmez |", ""]

    RAPOR.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print(f"   üretim kaydı {len(veri)} · dejenere {dej} · " +
          " · ".join(f"{b} {say[b]}" for b in bayraklar))
    print(f"   distinct-5 ortanca: cevaplı {statistics.median(sag):.3f} · "
          f"boş {statistics.median(boz):.3f} · eşik {D.TEKRAR_ESIGI}")
    print(f"   cevabı OLDUĞU hâlde tekrar yanan: {len(ates_cevapli)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
