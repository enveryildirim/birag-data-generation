#!/usr/bin/env python3
"""K46'nın üç metriği koda girdi — ama biri SERT KAPI oldu, ikisi olmadı.

`plan.md` §7 üç otomatik metrik ilan etmişti ve üçü de yalnızca bir analiz
betiğinde duruyordu: **thinking dili · thinking:completion oranı · kullanıcıya
giden token payı**. ⚠️ Plan bir de **şart** koymuştu: *«Dil tespiti şu an
kelime/karakter vekili; `checks.py`'ye sert kapı olarak girmeden önce yanlış
pozitif oranı ölçülmeli (K40'ın dersi: kalibre edilmemiş vekil kapı veri
öldürür)»*. ⇒ Bu betik önce o şartı ölçüyor, sonra kararı yazıyor.

⭐⭐ **Üç metrik, iki farklı karar:**
  · `thinking_dili` → **sert kapı** (yanlış pozitif **0/2716**, korpus etkisi **0**)
  · oran ve pay      → ⛔ **yalnızca rapor** — gerekçe **T7**: sabit bir eşik
    dağılımı kendine çeker ve ölçtüğü şeyi bozar.

➡️ *Aynı üç metrik aynı dosyaya girdi ve ikisi kapı olmadı. Bir metriği kapıya
çevirmek onu ölçmekten AYRI bir karardır ve ayrı bir gerekçe ister.*

Girdi : datasets/v*/train.jsonl · data/judged/*.jsonl · data/candidates/*.jsonl ·
        reports/analiz/thinking-dili-ogrenilebilirlik/*.jsonl (gerçek etiket) ·
        src/checks.py · src/smoke_checks.py
Çıktı : reports/analiz/2026-09-16-k46-metrikleri.md
Kullanım: uv run python scripts/analiz/2026-09-16-k46-metrikleri.py
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
RAPOR = KOK / f"reports/analiz/{TARIH}-k46-metrikleri.md"
ETIKET = KOK / "reports/analiz/thinking-dili-ogrenilebilirlik"
sys.path.insert(0, str(KOK / "src"))
import checks as C  # noqa: E402
import smoke_checks as SC  # noqa: E402


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def korpus():
    """(kaynak, id, replay mi, thinking, completion) — yalnızca ASİSTAN turları."""
    out = []
    yollar = (sorted(KOK.glob("datasets/v*/train.jsonl"))
              + sorted(KOK.glob("data/judged/*.jsonl"))
              + sorted(KOK.glob("data/candidates/*.jsonl")))
    for p in yollar:
        for satir in p.read_text(encoding="utf-8").split("\n"):
            if not satir.strip():
                continue
            try:
                r = json.loads(satir)
            except json.JSONDecodeError:
                continue
            for m in r.get("messages", []):
                if m.get("role") == "assistant" and m.get("thinking"):
                    out.append((str(p.relative_to(KOK)), r.get("id"),
                                bool(r.get("replay")), m["thinking"],
                                m.get("content", "")))
    return out


def main() -> int:
    kay = korpus()
    L: list[str] = []
    L += ["# K46'nın üç metriği koda girdi — biri kapı oldu, ikisi olmadı", "",
          f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
          f"**Girdi:** `src/checks.py` SHA256 `{sha(KOK/'src/checks.py')}` "
          f"(metrikler **çağrılıyor**)  ",
          f"**Girdi:** `src/smoke_checks.py` SHA256 `{sha(KOK/'src/smoke_checks.py')}` "
          f"(dil dedektörü **oradan**, kopyalanmıyor)  ",
          f"**Girdi:** korpus — **{len(kay)}** thinking taşıyan asistan turu", "",
          "---", "", "## 1. Üç metrik ve birimleri", "",
          "| metrik | tanım | birim |", "|---|---|---|",
          "| `thinking_dili` | `smoke_checks._dil` — Türkçeye özgü harf + işlev sözcüğü "
          "sayımı | sınıf (`tr`/`en`/`belirsiz`) |",
          "| `thinking_completion_orani` | thinking ÷ completion | **kelime** |",
          "| `kullaniciya_giden_pay` | completion ÷ (thinking + completion) | **kelime** |", "",
          "⚠️ **Birim KELİME, token değil.** K46'nın *«~14x uzun»* ölçümü de kelimeyle",
          "yapılmıştı (`2026-09-12-thinking-dili-raporu.py`, `len(t.split())`); birim",
          "değişirse sayılar **karşılaştırılamaz** (Kural 5).", "", "---", ""]

    # --- §2 yanlış pozitif ------------------------------------------------------
    dil = collections.Counter(SC._dil(t) for _, _, _, t, _ in kay)
    tr_disi = [(a, b, t) for a, b, _rp, t, _ in kay if SC._dil(t) != "tr"]
    L += ["## 2. ⭐ Planın ŞARTI — vekil kapının yanlış pozitif oranı", "",
          "`plan.md` dil tespitinin sert kapı olmasını **ölçüme bağlamıştı**. Korpusun",
          "tamamı Türkçe yazılmış (K50: thinking Türkçe yazılmaya devam) ⇒ `en` ya da",
          "`belirsiz` çıkan **her** kayıt bir yanlış pozitif adayıdır.", "",
          "| sınıf | kayıt |", "|---|---:|"]
    for k, v in sorted(dil.items()):
        L.append(f"| `{k}` | {v} |")
    L += ["",
          f"⭐ **Yanlış pozitif: {len(tr_disi)}/{len(kay)}.**", "",
          "---", "", "## 3. Gerçek etikete karşı — ve ⛔ kanıtın zayıf tarafı", "",
          "`reports/analiz/thinking-dili-ogrenilebilirlik/` K50'nin üst sınır koşusundan",
          "**etiketli** thinking taşıyor: dar LoRA kolu İngilizce, geniş LoRA kolu Türkçe.", "",
          "| dosya | beklenen | dedektör | |", "|---|---|---|---|"]
    fn_ornek = []
    for p in sorted(ETIKET.glob("*.jsonl")):
        th = [r["thinking"] for r in
              (json.loads(l) for l in p.read_text(encoding="utf-8").split("\n") if l.strip())
              if r.get("thinking")]
        bekl = "en" if "dar" in p.name else "tr"
        c = collections.Counter(SC._dil(t) for t in th)
        dogru = c.get(bekl, 0)
        if bekl == "en":
            fn_ornek = th
        L.append(f"| `{p.name}` | `{bekl}` | {dict(c)} | "
                 f"{'✅ **' + str(dogru) + '/' + str(len(th)) + '**' if dogru == len(th) else '⛔'} |")
    kalip = collections.Counter(t.strip()[:40] for t in fn_ornek)
    L += ["",
          f"⛔⛔ **YANLIŞ NEGATİF KANITI ZAYIF ve bu raporun en önemli şerhi.** "
          f"İngilizce örnek sayısı **{len(fn_ornek)}** ama ⭐ ilk 40 karakterine göre "
          f"**yalnızca {len(kalip)} ayrık kalıp** var"
          + (f" (en sık: *«{kalip.most_common(1)[0][0]}…»* ×{kalip.most_common(1)[0][1]})"
             if kalip else "") + ".", "",
          "➡️ *Yani dedektör İngilizceyi değil, **avuç içi kadar bir İngilizce**",
          "***örneklemini** doğru sınıflandırdığı ölçüde sınanmış durumda — üstelik",
          "*örneklerin çoğu tek bir şablondan geliyor. ⚠️ Yanlış pozitif tarafı geniş ve",
          "çeşitli bir korpusla ölçüldü; yanlış negatif tarafı **tek bir şablonla**.*",
          "⇒ Kapının **veri öldürme** riski ölçülü, **kaçırma** riski değil — ve",
          "`plan.md`'nin şartı tam olarak birincisiydi.", "", "---", ""]

    # --- §4 kapı kararı ---------------------------------------------------------
    elenen = [(a, b) for a, b, rp, t, c2 in kay
              if not rp and C.thinking_metrikleri(t, c2)["thinking_dili"] not in (None, "tr")]
    L += ["## 4. ⭐⭐ Üç metrik, iki farklı karar", "", "| metrik | karar | gerekçe |",
          "|---|---|---|",
          "| `thinking_dili` | ⭐ **SERT KAPI** (yalnızca BıRAG kayıtları) | planın şartı "
          f"karşılandı: yanlış pozitif **{len(tr_disi)}/{len(kay)}**; korpus etkisi "
          f"**{len(elenen)} kayıt** |",
          "| `thinking_completion_orani` | ⛔ **yalnızca rapor** | **T7**: §4'ün *«sabit "
          "taban koyma»* dersi — sabit eşik dağılımı kendine çeker ve ölçtüğü şeyi bozar |",
          "| `kullaniciya_giden_pay` | ⛔ **yalnızca rapor** | aynı gerekçe; tavanın veriyle "
          "nasıl öğretileceği `plan.md`'de **açık kalem** |", "",
          "⚠️ **Kapı replay dilimine uygulanmıyor:** §9 replay verisinin İngilizce olması",
          "**tasarım gereğidir** (çeşitlilik). ⭐ Bugün replay kayıtlarının hiçbirinde",
          "thinking yok (**0/72**, ölçüldü) — kapı yine de kapsam dışı bırakıldı, çünkü",
          "*koşul veriye değil TASARIMA dayanmalı; veri yarın değişir, tasarım kararı*",
          "*yazılıdır.*", "",
          f"⭐ Kapı bugün **{len(elenen)} kayıt** eliyor. ⚠️ Yani bir **tuzak teli**:",
          "bugün hiçbir şey yapmıyor, İngilizce thinking üretildiği gün yakalıyor.", "",
          "➡️⭐⭐ *Aynı üç metrik aynı dosyaya girdi ve ikisi kapı olmadı. **Bir metriği**",
          "***kapıya çevirmek, onu ölçmekten AYRI bir karardır** ve ayrı bir gerekçe*",
          "*ister. Ölçüm «şu an şöyle» der; kapı «bundan sonra böyle olmayacak» der.*",
          "", "---", ""]

    # --- §5 dağılımlar ----------------------------------------------------------
    oran = sorted(C.thinking_metrikleri(t, c2)["thinking_completion_orani"]
                  for _, _, _, t, c2 in kay
                  if C.thinking_metrikleri(t, c2)["thinking_completion_orani"] is not None)
    pay = sorted(C.thinking_metrikleri(t, c2)["kullaniciya_giden_pay"]
                 for _, _, _, t, c2 in kay
                 if C.thinking_metrikleri(t, c2)["kullaniciya_giden_pay"] is not None)

    def y(v, q):
        return v[min(len(v) - 1, int(q * len(v)))]

    L += ["## 5. Bugünkü dağılımlar — eşik DEĞİL, taban", "",
          "| metrik | en düşük | %10 | ortanca | %90 | en yüksek |",
          "|---|---:|---:|---:|---:|---:|",
          f"| `thinking_completion_orani` | {oran[0]:.2f} | {y(oran,.1):.2f} | "
          f"**{statistics.median(oran):.2f}** | {y(oran,.9):.2f} | {oran[-1]:.2f} |",
          f"| `kullaniciya_giden_pay` | {pay[0]:.2f} | {y(pay,.1):.2f} | "
          f"**{statistics.median(pay):.2f}** | {y(pay,.9):.2f} | {pay[-1]:.2f} |", "",
          f"⭐ Ortanca oran **{statistics.median(oran):.2f}** — K50'nin *«~2x hedefi»*",
          "civarında. ⛔ K46'nın **~14x**'i eğitilmemiş MODELİN ölçüsüydü, veri setinin",
          "değil; ikisi karıştırılmamalı.", "",
          "⚠️ **Bu sayılar bir eşik önerisi DEĞİL**, bugünkü tabandır. Eşik koymak T7'nin",
          "uyardığı şeydir ve ayrı bir karar.", "",
          "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ **Yanlış negatif oranı** | 36 örnek, ~1 kalıp (§3). İngilizcenin "
          "çeşitliliği sınanmadı |",
          "| ⛔ `belirsiz` sınıfı | korpusta hiç çıkmadı ⇒ **hiç sınanmadı**; çok kısa bir "
          "thinking'te ne olacağı bilinmiyor. ⚠️ Kapı `belirsiz`'i **geçiriyor** (`tr` "
          "gibi değil, `None` gibi değil — açıkça `tr` değilse eler) |",
          "| ⛔ Oran ve pay için **eşik yok** | bilerek; T7'nin dersi |",
          "| ⚠️ Birim **kelime** | token değil; tokenizer'a bağlı bir sayı istenirse "
          "yeniden ölçülmeli ve K46'nın sayısıyla karşılaştırılamaz |", ""]

    RAPOR.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print(f"   thinking taşıyan tur {len(kay)} · dil dağılımı {dict(dil)} · "
          f"yanlış pozitif {len(tr_disi)}")
    print(f"   kapı bugün {len(elenen)} kayıt eliyor · oran ortancası "
          f"{statistics.median(oran):.2f} · pay ortancası {statistics.median(pay):.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
