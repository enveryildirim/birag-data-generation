#!/usr/bin/env python3
"""v9 doğrulama kapısının KÜMÜLATİF defteri — kapı kaç kez ateşledi?

⛔ **Bu betik bir DÜZELTME olarak doğdu.** v9 ve korpus koşularının raporları
*«doğrulanamayan alıntı: 0»* yazıyordu; o sayı yalnızca **aşama 1**'i sayıyordu ve
hakemlik geçişleri hiç denetlenmiyordu. Bütün geçişler sayılınca kapının
**ateşlediği** ortaya çıktı (K123).

Defter üç ayrı soruyu ayırır, çünkü aynı kapı üç farklı işi yapıyor:

  1. **Muafiyet doğrulaması** (kapının yazılma sebebi) — bugüne dek 0 ateşleme.
  2. **Alıntı sadakati** — judge'ın cevaptan yaptığı alıntı gerçekten orada mı.
  3. **Sağlama bütünlüğü** — sonuç dosyası gerçekten o kayda mı ait
     (`eslesme_denetimi`); kapının ilk gerçek yakalaması buydu.

⚠️ Betik yalnızca ARŞİVLENMİŞ ham judge çıktısını okur; yeniden puanlama yapmaz.

Kullanım: uv run python scripts/analiz/2026-09-15-v9-kapi-denetimi.py
"""
from __future__ import annotations

import json
import sys
from datetime import date
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
sys.path.insert(0, str(KOK / "src"))
import filter as f  # noqa: E402

_sp = _iu.spec_from_file_location("b9", KOK / "scripts/analiz/2026-09-15-v9-birlestir.py")
B9 = _iu.module_from_spec(_sp)
sys.argv = [sys.argv[0]]
_sp.loader.exec_module(B9)

HAM = KOK / "reports/analiz/ham-judge"
KORPUS = KOK / "data/candidates/v3-kumulatif.jsonl"
SET1 = KOK / "evals/safety_crisis.jsonl"
KOSU = KOK / "reports/analiz/eksen-kosu"
RAPOR = KOK / f"reports/analiz/{TARIH}-v9-kapi-defteri.md"

# Alıntı alanı → kaynağı. `_dogrula` ile birebir aynı eşleme.
MUAFIYET = {"teselli_dayanak_alintisi": "konusma", "rol_baglam_alintisi": "baglam",
            "yordam_baglam_alintisi": "baglam"}
SUCLAMA = {a: "cevap" for a in
           ("en_belirsiz_cumle", "en_somut_ayrinti", "rol_sinirina_en_yakin",
            "rol_iddiasi", "guvenlige_en_yakin", "kisiye_dair_en_genel",
            "sorumluluga_en_yakin", "en_teselli_edici", "kurum_yordam_en_yakin",
            "kurum_adi", "yordam_iddiasi")}


def eksen2_kaynaklari() -> dict:
    ogeler = {o["id"]: o for o in (json.loads(l) for l in SET1.open(encoding="utf-8"))}
    out = {}
    for _etiket, (kol, dizin) in B9.HARITA.items():
        for r in (json.loads(l) for l in (KOSU / dizin / "sonuclar.jsonl").open(encoding="utf-8")):
            out[(kol, r["id"])] = B9.kaynak_kur(ogeler[r["id"]], r["cevap"],
                                                r.get("thinking"))
    return out


def korpus_kaynaklari() -> dict:
    return {r["id"]: f.kaynak_metinleri(r)
            for r in (json.loads(l) for l in KORPUS.open(encoding="utf-8"))}


# Bir kaydın hangi cevaba ait olduğunu belirlemeye yetecek uzunlukta alıntı alanları.
ESLESME_ALAN = ["en_belirsiz_cumle", "en_somut_ayrinti", "rol_sinirina_en_yakin",
                "guvenlige_en_yakin", "kisiye_dair_en_genel", "sorumluluga_en_yakin",
                "en_teselli_edici", "kurum_yordam_en_yakin"]


def eslesme_denetimi(yol: Path, kaynaklar: dict, anahtar, kayitlar=None) -> list:
    """SONUÇ ↔ KAYIT eşleşmesi doğru mu — 2026-09-15 olayının kapısı.

    ⛔ Gerçek olay: `korpus-v9-p2` partisinde bir subagent doğru iş dosyalarını okudu
    ama sonuçları YANLIŞ çıktı dosyalarına yazdı (004→005→006→007→004 dönüşümü).
    Dört kaydın judge çıktısı başka kayda ait oldu; hiçbir şey hata vermedi ve gürültü
    tabanı o dört kayıtla hesaplandı. Kusuru **alıntı doğrulaması** yakaladı: kendi
    cevabında bulunmayan alıntılar hep AYNI başka kayıtta bulunuyordu.

    Denetim: bir kaydın uzun alıntıları kendi cevabında mı, yoksa başka bir kaydın
    cevabında mı daha çok bulunuyor. İkincisi ise eşleşme kaymıştır.
    """
    kotu = []
    # `kayitlar`: arşivin DÜZELTİLMİŞ görüntüsü (bkz. `*.takas.json`). Kapı düzeltme
    # uygulandıktan SONRA koşmalı, yoksa bilinen bir kusur her koşuda yeniden ateşler.
    for r in (kayitlar if kayitlar is not None
              else (json.loads(l) for l in yol.open(encoding="utf-8"))):
        ham = r.get("ham")
        if isinstance(ham, str):
            try:
                ham = json.loads(ham)
            except json.JSONDecodeError:
                continue
        if not isinstance(ham, dict):
            continue
        kend = anahtar(r)
        if kend is None or kend not in kaynaklar:
            continue
        q = [f.alinti_nrm(ham[a]) for a in ESLESME_ALAN if f._f_dolu(ham, a)]
        q = [x for x in q if len(x) > 25]
        if not q:
            continue
        kendi = sum(1 for x in q if x in kaynaklar[kend]["cevap"])
        if kendi == len(q):
            continue
        en_iyi, en_skor = kend, kendi
        for i, k in kaynaklar.items():
            sk = sum(1 for x in q if x in k["cevap"])
            if sk > en_skor:
                en_iyi, en_skor = i, sk
        if en_iyi != kend:
            kotu.append({"dosya": yol.stem, "no": r.get("no"), "kayit": str(kend),
                         "kendi": kendi, "alinti": len(q),
                         "ait_oldugu": str(en_iyi), "skor": en_skor})
    return kotu


def tara(yol: Path, kaynak_bul) -> tuple[int, int, int, int, list]:
    """(kayıt, denetlenen alıntı, muafiyet alıntısı, ateşleme, vakalar)"""
    n = alinti = muaf = ates = 0
    vaka = []
    for l in yol.open(encoding="utf-8"):
        r = json.loads(l)
        ham = r.get("ham")
        if isinstance(ham, str):
            try:
                ham = json.loads(ham)
            except json.JSONDecodeError:
                continue
        if not isinstance(ham, dict):
            continue
        k = kaynak_bul(r)
        if k is None:
            continue
        n += 1
        for alan, nerede in {**SUCLAMA, **MUAFIYET}.items():
            if not f._f_dolu(ham, alan):
                continue
            alinti += 1
            if alan in MUAFIYET:
                muaf += 1
            q = f.alinti_nrm(ham.get(alan))
            if q and q in k.get(nerede, ""):
                continue
            ates += 1
            vaka.append((yol.stem, r.get("id", "?"), alan, nerede,
                         (ham.get(alan) or "")[:70]))
    return n, alinti, muaf, ates, vaka


def main() -> int:
    e2k = eksen2_kaynaklari()
    kork = korpus_kaynaklari()
    satir, tum_vaka = [], []

    for yol in sorted(HAM.glob("v9-e2-*.jsonl")) + [HAM / "v9-hakem-p2.jsonl",
                                                    HAM / "v9-hakem-p3.jsonl"]:
        def bul(r, _=None):
            kol = r.get("kol")
            if kol:
                return e2k.get((kol, r["id"]))
            # aşama 1 dosyalarında kol, dosya adından gelir
            for (k2, oid), v in e2k.items():
                if oid == r["id"] and k2 == BILINEN_KOL[yol.stem]:
                    return v
            return None
        satir.append((f"Eksen 2 · {yol.stem}",) + tara(yol, bul)[:4])
        tum_vaka += tara(yol, bul)[4]

    for yol in [HAM / "korpus-v9.jsonl", HAM / "korpus-v9-p2.jsonl",
                HAM / "korpus-v9-p3.jsonl"]:
        if not yol.exists():
            continue
        n, a, m, at, v = tara(yol, lambda r: kork.get(r["id"]))
        satir.append((f"korpus · {yol.stem}", n, a, m, at))
        tum_vaka += v

    T = [sum(s[i] for s in satir) for i in (1, 2, 3, 4)]
    y = [
        "# Kapının ilk yakalaması judge DEĞİL, ölçüm hattıydı — v9 kapı defteri",
        "",
        f"*{TARIH} · betik `scripts/analiz/{Path(__file__).name}`*",
        "*girdi: `reports/analiz/ham-judge/v9-*.jsonl` · `korpus-v9*.jsonl` (arşivlenmiş "
        "ham judge çıktısı; yeniden puanlama YOK)*",
        "",
        "## ⛔ Önce bir düzeltme",
        "",
        "v9 ve korpus koşularının raporları *«doğrulanamayan alıntı: 0»* yazıyordu. O sayı",
        "yalnızca **aşama 1** kayıtlarını sayıyordu; **hakemlik geçişleri hiç**",
        "**denetlenmiyordu**. Bütün geçişler sayılınca kapının ateşlediği görüldü.",
        "",
        "⭐⭐ **Kapının ilk gerçek yakalaması bir judge uydurması DEĞİL, bir SAĞLAMA**",
        "**KUSURUYDU.** `korpus-v9-p2` partisinde bir subagent **doğru** iş dosyalarını",
        "okudu ama sonuçları **yanlış** çıktı dosyalarına yazdı: 004→005→006→007→004",
        "dönüşümü. Dört kaydın judge çıktısı başka kayda ait oldu. Hiçbir şey hata",
        "vermedi, JSON geçerliydi, alan sayısı doğruydu — ve o dört kayıt **gürültü**",
        "**tabanı** hesabına girdi.",
        "",
        "Kusuru yakalayan şey alıntı doğrulamasıydı: bu kayıtların alıntıları kendi",
        "cevaplarında **hiç** bulunmuyor, ama hepsi **aynı başka kayıtta** bulunuyordu.",
        "➡️ *Alıntı doğrulaması yalnızca judge'ı denetlemiyor, ÖLÇÜM HATTINI da*",
        "*denetliyor: sonuç ile kayıt arasındaki eşleşme bozulduğunda bunu gösteren*",
        "*başka hiçbir sinyal yok.*",
        "",
        "✅ Dört iş yeniden koşuldu (her biri tek başına bir ajana verildi), arşiv",
        "güncellendi, `eslesme_denetimi()` artık her iki rapor betiğinde **sert kapı**.",
        "⚠️ Bozuk kayıtların ikisinin bayrak kümesi gerçekten yanlıştı",
        "(`bos_guvence`/`klinik_guvenlik_ihlali`); yayımlanan gürültü tabanı (%8) şans",
        "eseri değişmedi ama **doğru sebeple doğru değildi**.",
        "",
        "## Defter",
        "",
        "| Koşu | kayıt | denetlenen alıntı | bunlardan muafiyet | **ateşleme** |",
        "|---|---:|---:|---:|---:|",
    ]
    for ad, n, a, m, at in satir:
        y.append(f"| `{ad}` | {n} | {a} | {m} | **{at}** |")
    y += [
        f"| **TOPLAM** | **{T[0]}** | **{T[1]}** | **{T[2]}** | **{T[3]}** |",
        "",
        f"⭐ **{T[0]} judge kararı, {T[1]} alıntı, {T[3]} ateşleme** (sağlama kusuru",
        f"düzeltildikten sonra). Alıntıların {T[2]} tanesi **muafiyet** alıntısıydı —",
        "kapının yazılma sebebi olan sınıf.",
        "",
    ]
    if tum_vaka:
        y += ["⛔ **Kalan ateşleme — elle okundu:**", "",
              "| koşu | kayıt | alan | kaynak | alıntı |", "|---|---|---|---|---|"]
        for v in tum_vaka[:25]:
            y.append(f"| `{v[0]}` | `{v[1]}` | `{v[2]}` | {v[3]} | *«{v[4]}»* |")
        y += [
            "",
            "**Sınıflandırma (`B-derin`/`sk-019`):** eşleştirici hatası **değil**, gerçek",
            "bir alıntı hatası. Cevapta iki ayrı cümle var — *«Ne yapman gerektiğini",
            "söylemek, bir yol haritası çizmek olur»* ve *«Senin için neyin iyi geleceğini",
            "söylemek yerine, sadece şunu sorabilirim…»* — judge birincinin başını",
            "ikincinin gövdesine **ekleyerek** var olmayan bir cümle üretmiş.",
            "⚠️ `en_belirsiz_cumle` bir hüküm kurmuyor, bu yüzden sayı **değişmedi**;",
            "ama aynı hatanın hüküm kuran bir alanda olmayacağının güvencesi yok.",
            "",
        ]
    y += [
        "## Üç iş, üç ayrı sonuç",
        "",
        "| Kapının işi | ateşleme | okuma |",
        "|---|---:|---|",
        f"| **muafiyet doğrulaması** (yazılma sebebi) | **0**/{T[2]} | ⚠️ bu işte kapı hâlâ "
        "**sınanmadı**; işleyen şey rubriğin ilanı, yani **caydırıcılık** |",
        f"| **alıntı sadakati** | **{sum(1 for v in tum_vaka)}**/{T[1]} | ⭐ bir gerçek "
        "judge hatası yakalandı (cümle birleştirme) |",
        "| **sağlama bütünlüğü** | **4 kayıt** | ⭐⭐ kapının ilk gerçek yakalaması; "
        "başka hiçbir sinyal bunu göstermezdi |",
        "",
        "➡️ **Kapı «caydırıcılıktan ibaret» DEĞİL.** Yazılma sebebi olan işte (muafiyet)",
        "hâlâ ateşlemedi ve o işte caydırıcı sayılmalı; ama aynı mekanizma iki farklı",
        "gerçek kusuru yakaladı ve ikisi de başka türlü görünmezdi.",
        "",
        "## Bedel — açıkça yazılıyor",
        "",
        "| | |",
        "|---|---|",
        "| ⛔ **Muafiyet** doğrulamasının işleyişi | üretimde sınanmadı; yalnızca 18 kapı vakasında |",
        "| ⛔ Kapının **yarısı** | dayanağın kimin turundan geldiği kararı hiç fark yaratmadı |",
        "| ⚠️ Eşleştiricinin hata oranı | ateşleme olmadığı için **yanlış negatif oranı da** ölçülemedi |",
        "| ⚠️ Caydırıcılığın **kendisi** | ayrı bir kontrol koşusu olmadan (kapı ilan edilmeden aynı rubrik) nedensel değil |",
        "",
        "## ⭐ Ateşleme sayısı bir izleme göstergesidir",
        "",
        "Her ateşleme üç şeyden birini söyler ve üçü de araştırılmayı gerektirir:",
        "",
        "1. **Judge uydurmaya ya da birleştirmeye başladı** — model/aile/sürüm değişmiş",
        "   olabilir (K45). Bu koşuda 1 vaka çıktı.",
        "2. **Eşleştirici bozuldu** — `alinti_nrm` ya da kaynak kurulumu değişmiş olabilir.",
        "3. **Sağlama bozuldu** — sonuç ile kayıt eşleşmesi kaymış olabilir. Bu koşuda",
        "   4 kayıtta çıktı ve **başka hiçbir denetim bunu göstermiyordu.**",
        "",
        "Defter her v9 koşusundan sonra yeniden koşulur. ⛔ Ateşleme sayısı sıfırdan",
        "farklıysa, sebebi sınıflandırılmadan rapor yazılmaz.",
    ]
    RAPOR.write_text("\n".join(y) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print(f"   {T[0]} karar · {T[1]} alıntı · {T[2]} muafiyet · ATEŞLEME {T[3]}")
    return 0


BILINEN_KOL = {
    "v9-e2-5ae67873": "taban", "v9-e2-b7584bec": "A-dar",
    "v9-e2-220c3b5a": "B-derin", "v9-e2-99b69ab4": "C-dikkat",
    "v9-e2-7ac7e984": "D-tam", "v9-e2-ceef5655": "E-genis",
}

if __name__ == "__main__":
    sys.exit(main())
