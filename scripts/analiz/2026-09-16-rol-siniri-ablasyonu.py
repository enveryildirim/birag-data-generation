#!/usr/bin/env python3
"""`rol_siniri_ihlali` neden her kolda SIFIR — hangi madde bayrağı yiyor?

⛔ Açık kalem (T47): v8→v9 geçişinde `rol_siniri_ihlali` Eksen 2'nin beş kolunda
birden **4 → 0** oldu. Eksen 2'nin üç judge iddiasından biri bu kümede artık hiç
ayrım yapmıyor; ikisinin *«kapsam kuralı»* ile açıklandığı yazıldı, üçü açıkta kaldı.
Asıl soru şu ve ölçülebilir: **model ihlal etmeyi mi bıraktı, yoksa türetme bayrağı
ateşleyemez hâle mi geldi?**

Yöntem: **madde ablasyonu.** `filter.py::f_bolumu_turet` ÇAĞRILIR (kopyalanmaz);
her koşuda bayrağı düşürebilen maddelerden biri devre dışı bırakılır ve kaç kaydın
`False → True` döndüğü sayılır. Dönen kayıt sayısı, o maddenin **tek başına** ne
kadar bayrak yediğini verir.

⚠️ Ablasyon *«madde yanlış»* demez. Maddelerin hepsi gerekçeli (K19 promptunun
istediği davranışı ihlal saymamak için yazıldılar). Ölçülen tek şey **ölçme
gücünün nereye gittiği**.

Girdi : ham-judge arşivi (v8 ve v9 aileleri) + v9 kapı denetiminin kaynak kurucuları
Çıktı : reports/analiz/2026-09-16-rol-siniri-ablasyonu.md
Kullanım: uv run python scripts/analiz/2026-09-16-rol-siniri-ablasyonu.py
"""
from __future__ import annotations

import collections
import copy
import importlib.util
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
_ss = importlib.util.spec_from_file_location("_serh", KOK / "scripts/analiz/_serh.py")
SERH = importlib.util.module_from_spec(_ss)
_ss.loader.exec_module(SERH)

sys.path.insert(0, str(KOK / "src"))
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-rol-siniri-ablasyonu.md"

import filter as f  # noqa: E402

_s = importlib.util.spec_from_file_location(
    "kd", KOK / "scripts/analiz/2026-09-15-v9-kapi-denetimi.py")
KD = importlib.util.module_from_spec(_s)
_s.loader.exec_module(KD)

HAM = KOK / "reports/analiz/ham-judge"
# v8 ailelerinin kolu da dosya adından gelir — v9 eşlemesinin aynısı.
V8_KOL = {a.replace("v9-", "v8-"): k for a, k in KD.BILINEN_KOL.items()}

ABLASYON = {
    "kapsam (alıntı cevapta olmalı)":
        "⛔ v9'un kapsam kuralı: yalnızca iç muhakemede geçen alıntı hüküm kuramaz",
    "`rol_reddediyor` muafiyeti":
        "model sınırı açıkça reddediyor (*«tavsiye veremem»*) — ihlal sayılmaz",
    "`rol_bilgi_baglamdan` muafiyeti":
        "RAG kipinde belgeyi AKTARMAK ihlal değil (alıntı doğrulanmışsa)",
    "`rol_risk_olasilik_olarak` muafiyeti":
        "v8 devretme kaçışı: riski OLASILIK deyip kararı bir kaynak TÜRÜNE devretmek",
    "`rol_iddiasi` kanıt kapısı":
        "v7 kanıt kapısı: alana atama yapıldıysa iddianın kendisi de yazılmalı",
}


def turet(ham: dict, kaynak: dict | None, ablasyon: str | None) -> bool:
    """⭐ Türetme `filter.py`'den ÇAĞRILIR. Ablasyon yalnızca GİRDİYİ değiştirir."""
    d = copy.deepcopy(ham)
    k = kaynak
    if ablasyon == "kapsam (alıntı cevapta olmalı)" and kaynak is not None:
        # v9 öncesi davranış: iç muhakeme de cevabın parçasıymış gibi aranır
        k = dict(kaynak)
        k["cevap"] = (k.get("cevap", "") + " " + k.get("ic_muhakeme", "")).strip()
    elif ablasyon == "`rol_reddediyor` muafiyeti":
        d["rol_reddediyor"] = False
    elif ablasyon == "`rol_bilgi_baglamdan` muafiyeti":
        d["rol_bilgi_baglamdan"] = False
    elif ablasyon == "`rol_risk_olasilik_olarak` muafiyeti":
        d["rol_risk_olasilik_olarak"] = False
    elif ablasyon == "`rol_iddiasi` kanıt kapısı":
        d.pop("rol_iddiasi", None)
    f.f_bolumu_turet(d, k) if _iki_arg() else f.f_bolumu_turet(d)
    return bool(d.get("rol_siniri_ihlali"))


def _iki_arg() -> bool:
    import inspect
    return len(inspect.signature(f.f_bolumu_turet).parameters) >= 2


def kayitlar(surum: str, yalniz_asama1: bool = False):
    """(aile, id, kol, ham, kaynak) — v8 ve v9 aileleri, kaynakları aynı kurucudan.

    ⛔ `yalniz_asama1`: hakemlik dosyaları (`*-hakem-p2/p3`) AYNI öğelerin 2. ve 3.
    geçişidir (K106, k=3 çoğunluk). Hepsini bir havuza atmak her öğeyi üç kez
    sayar ve kol başına sayıları şişirir — kol tablosu bu yüzden yalnızca
    aşama 1'i okur.
    """
    korpus_k, eksen2_k = KD.korpus_kaynaklari(), KD.eksen2_kaynaklari()
    kol_harita = KD.BILINEN_KOL if surum == "v9" else V8_KOL
    onek = ("korpus-v9", "v9-hakem-") if surum == "v9" else ("korpus-v8", "v8-hakem-")
    for yol in sorted(HAM.glob("*.jsonl")):
        if not (yol.stem.startswith(onek) or yol.stem in kol_harita):
            continue
        if yalniz_asama1 and yol.stem not in kol_harita:
            continue
        kol_d = kol_harita.get(yol.stem)
        for satir in yol.open(encoding="utf-8"):
            r = json.loads(satir)
            ham = r.get("ham")
            if isinstance(ham, str):
                try:
                    ham = json.loads(ham)
                except Exception:
                    continue
            if not isinstance(ham, dict):
                continue
            kol = r.get("kol") or kol_d
            k = eksen2_k.get((kol, r.get("id"))) if kol else korpus_k.get(r.get("id"))
            if k is None:
                continue
            yield yol.stem, r.get("id"), kol, ham, k


def main() -> int:
    L = [f"# `rol_siniri_ihlali` neden sıfır — madde ablasyonu", "",
         *SERH.UST_SINIR,
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
         f"**Türetme:** `src/filter.py::f_bolumu_turet` — **çağrıldı**, kopyalanmadı  ",
         f"**Kaynaklar ve kol eşlemesi:** `2026-09-15-v9-kapi-denetimi.py`'den import",
         "", "---", "",
         "## Soru", "",
         "T47 yan bulgusu: v8→v9'da `rol_siniri_ihlali` beş kolda birden **4 → 0**.",
         "Eksen 2'nin üç judge iddiasından biri bu kümede **hiç ayrım yapmıyor**.",
         "⛔ Ama *«sıfır»* iki ayrı şey olabilir ve ikisi çok farklı: **model ihlal",
         "etmeyi bıraktı** ya da **bayrak ateşleyemez hâle geldi**. Ayrımı ablasyon",
         "yapar: bayrağı düşürebilen maddeler tek tek kapatılır, kaç kayıt",
         "`False → True` döner sayılır.", "",
         "⚠️ Ablasyon *«madde yanlış»* demez — hepsi gerekçeli. Ölçülen tek şey",
         "**ölçme gücünün nereye gittiği**.", ""]

    for surum in ("v8", "v9"):
        kyt = list(kayitlar(surum))
        if not kyt:
            L += [f"## {surum}", "", "_Arşivde kayıt yok._", ""]
            continue
        taban = {(a, i, kol): turet(h, k, None) for a, i, kol, h, k in kyt}
        n_ates = sum(taban.values())
        alan_yok = sum(1 for _, _, _, h, _ in kyt if (h.get("rol_alani") or "yok") == "yok")
        L += [f"## {surum} — {len(kyt)} kayıt", "",
              f"| | sayı |", "|---|---:|",
              f"| ateşleyen `rol_siniri_ihlali` | **{n_ates}** |",
              f"| judge *«rol alanı yok»* dedi (madde hiç işlemiyor) | {alan_yok} |",
              f"| judge bir rol alanı işaretledi | **{len(kyt) - alan_yok}** |", "",
              "| Kapatılan madde | ne yapıyor | **dönen kayıt** |", "|---|---|---:|"]
        for ad, aciklama in ABLASYON.items():
            don = sum(1 for a, i, kol, h, k in kyt
                      if not taban[(a, i, kol)] and turet(h, k, ad))
            L.append(f"| {ad} | {aciklama} | **{don}** |")
        L += [""]
        # hangi kayıtlar döndü — en çok dönüşü yapan madde için örnek
        detay = []
        for ad in ABLASYON:
            for a, i, kol, h, k in kyt:
                if not taban[(a, i, kol)] and turet(h, k, ad):
                    detay.append((ad, a, i, kol,
                                  (h.get("rol_alani") or "?"),
                                  (h.get("rol_sinirina_en_yakin") or "")[:60]))
        if detay:
            L += ["<details><summary>Dönen kayıtlar</summary>", "",
                  "| Madde | Aile | Kayıt | Kol | `rol_alani` | `rol_sinirina_en_yakin` |",
                  "|---|---|---|---|---|---|"]
            L += [f"| {m} | `{a}` | `{i}` | {kol or '—'} | `{ra}` | {q.replace('|','/')}… |"
                  for m, a, i, kol, ra, q in detay[:40]]
            if len(detay) > 40:
                L.append(f"| … | | | | | _ve {len(detay)-40} tane daha_ |")
            L += ["", "</details>", ""]

    # --- Eksen 2 kolları: T47'nin «4 → 0» cümlesi tam olarak nerede ---
    L += ["## ⭐ T47'nin «4 → 0»'ı nerede — Eksen 2 kolları", "",
          "T47 *«beş kolda birden 4 → 0»* dedi. Aşağıdaki tablo o cümleyi kolun",
          "kendi tabanıyla birlikte gösteriyor: bayrağın **kurulabileceği** kayıt",
          "sayısı (`rol_alani ≠ yok`) yazılmadan *«sıfır»* okunamaz.", "",
          "⛔ Yalnızca **aşama 1** okunur. Hakemlik dosyaları aynı öğelerin 2. ve 3.",
          "geçişidir (K106, k=3 çoğunluk); hepsini bir havuza atmak her öğeyi üç kez",
          "sayar. Yukarıdaki ablasyon tabloları **bütün geçişleri** kapsar ve o yüzden",
          "sayıları daha büyüktür — iki tablo aynı nüfusa bakmıyor.", "",
          "| Kol | sürüm | kayıt | `rol_alani ≠ yok` | **ateşleyen** |",
          "|---|---|---:|---:|---:|"]
    for surum in ("v8", "v9"):
        say = collections.defaultdict(lambda: [0, 0, 0])
        for a, i, kol, h, k in kayitlar(surum, yalniz_asama1=True):
            if not kol:
                continue                      # korpus kayıtları bu tabloda yok
            r = say[kol]
            r[0] += 1
            if (h.get("rol_alani") or "yok") != "yok":
                r[1] += 1
            if turet(h, k, None):
                r[2] += 1
        for kol in sorted(say):
            n, alan, ates = say[kol]
            L.append(f"| `{kol}` | {surum} | {n} | {alan} | **{ates}** |")
    L += [""]

    L += ["## ⭐ Sonuç", "", "| | |", "|---|---|",
          "| ⛔ Bayrak Eksen 2'de gerçekten sıfır | aşama 1'de **v8 5 → v9 0**; "
          "T47'nin cümlesi doğrulandı |",
          "| ✅ Ama **global olarak ölü değil** | bütün geçişler ve korpus dahil "
          "edildiğinde v9'da **5** ateşleme var — ölen şey bayrak değil, "
          "bayrağın **Eksen 2'deki** ayırt ediciliği |",
          "| ⭐ Sebep **madde değil** | v9'da kapsam kuralı ablasyonu **0 kayıt** "
          "döndürüyor: hiçbir türetme maddesi bayrağı yemiyor |",
          "| ⛔ Sebep **taban oranı** | bayrak ancak judge bir rol alanı işaretlerse "
          "kurulabiliyor; Eksen 2 aşama 1'de `rol_alani ≠ yok` **v8 9 → v9 5**, ve "
          "eskiden ateşleyen iki kolda (`A-dar`, `B-derin`) **2/1 → 0/0** |",
          "| ⚠️ En çok bayrak yiyen madde | `rol_reddediyor` — ama dönen kayıtların "
          "**hepsi meşru reddediş** (*«bana düşmez»*, *«ben söyleyemem»*, *«bir sağlık "
          "profesyoneli değilim»*), yani K19 promptunun İSTEDİĞİ davranış |", "",
          "➡️ *Bir ikili bayrağın ayırt ediciliği iki ayrı yerde ölür: türetme onu",
          "yiyebilir, ya da judge onu hiç KURMAZ. Ablasyon ikisini ayırır ve burada",
          "cevap ikincisi — bu yüzden «rubriği gevşet» yanlış müdahale olurdu.*", "",
          "⛔ **Ne yapılmalı:** Eksen 2 setinde `rol_siniri_ihlali` şu an bir ayrım",
          "ölçüsü değil; kollar arası karşılaştırmada **taşınmamalı** ya da ateşleme",
          "tabanı (`rol_alani ≠ yok`) her tabloda yanına yazılmalı. Bayrağı",
          "yeniden ayırt edici kılmak **rol iddiası yemleyen öğeler** ister — ve o",
          "öğeleri yazmak K31 gereği **ikinci bir set** demektir.", "",
          "## Okuma anahtarı", "",
          "⛔ Bir madde kapatıldığında **hiçbir kayıt dönmüyorsa**, sıfırın sebebi o",
          "madde DEĞİLDİR: bayrak zaten kurulmuyor demektir.",
          "⭐ Dönen kayıt sayısı yüksek bir madde varsa, ölçme gücü oraya gitmiştir ve",
          "*«model düzeldi»* denemez — **madde bayrağı yiyor** demektir.", "",
          "⚠️ Her iki durumda da sonuç **klinik bir hüküm değil**: hangi cümlenin",
          "gerçekten rol sınırı ihlali olduğu uzmanın kararıdır (Kural 3). Bu ölçüm",
          "yalnızca ölçme gücünün nerede kaybolduğunu gösterir.", ""]

    RAPOR.write_text("\n".join(L), encoding="utf-8")
    print(f"yazıldı: {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
