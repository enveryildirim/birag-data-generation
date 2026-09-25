#!/usr/bin/env python3
"""Vahşi doğa dilimi — kaynak taraması ve NEDEN ŞU AN YAPILAMADIĞI.

Faz 3 maddesi: *"Vahşi doğa dilimi — bizim üretmediğimiz gerçek kullanıcı mesajları"*.

Niye gerekli (ölçülmüş): K42'de korpusun kullanıcı mesajı biçimi ölçüldü —
1-8 kelimelik mesaj **%0.5**, hiç noktalama içermeyen **%0.0**, medyan 36 kelime.
Bu sayı kullanıcı kanıtı değil **üretici artefaktı**. Veri "zengin girdi → detaylı
yansıtma" öğretiyor; model iki kelimelik girdide detay uydurur ve v0.0.1'in 4.95/5
grounding skoru **riskin en yüksek olduğu yerde kör**.

Bu betik dilim üretmiyor. Aday kaynakları tarıyor, her birinin neden yetmediğini
ÖLÇÜYOR ve kararı yürütücü/etik kurula bırakıyor — çünkü kalan tek gerçek kaynak
savunmasız bireylerin sağlık verisi niteliğinde (§14).

Kullanım: uv run python scripts/analiz/2026-09-15-vahsi-dilim-kaynak-taramasi.py
"""
from __future__ import annotations

import glob
import gzip
import json
import re
import statistics as st
import sys
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
sys.path.insert(0, str(KOK / "src"))

TOHUMLAR = KOK / "data/seeds.jsonl"
KORPUS = KOK / "data/candidates/v3-kumulatif.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-vahsi-dilim-kaynak-taramasi.md"
OASST = glob.glob("/Users/pc/.cache/huggingface/hub/datasets--OpenAssistant--oasst2/"
                  "**/*.jsonl.gz", recursive=True)

NOKTALAMA = re.compile(r"[.!?,;:]")


def olc(metinler: list[str]) -> dict:
    if not metinler:
        return {}
    kel = [len(m.split()) for m in metinler]
    return {
        "n": len(metinler),
        "medyan_kelime": st.median(kel),
        "kisa_orani": sum(1 for k in kel if k <= 8) / len(kel),
        "noktalamasiz_orani": sum(1 for m in metinler if not NOKTALAMA.search(m)) / len(metinler),
    }


def main() -> None:
    korpus = [json.loads(l) for l in open(KORPUS)]
    bizim = [m["content"] for r in korpus for m in r["messages"] if m["role"] == "user"]
    tohum = [json.loads(l)["user_message"] for l in open(TOHUMLAR) if l.strip()]

    oasst_tr = []
    if OASST:
        with gzip.open(OASST[0], "rt") as f:
            for l in f:
                r = json.loads(l)
                if r.get("lang") == "tr" and r.get("role") == "prompter":
                    oasst_tr.append(r["text"])

    b, t, o = olc(bizim), olc(tohum), olc(oasst_tr)

    y = ["# Vahşi doğa dilimi — kaynak taraması ve engel kaydı", "",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}", "",
         "---", "",
         "## 0. Sonuç önce", "",
         "⛔ **Bu dilim şu an ÜRETİLEMEZ ve sahtesi yapılmadı.** Gerekçe aşağıda ölçüldü.",
         "Gereken karar teknik değil: **yürütücü + etik kurul** (§14).", "",
         "## 1. Niye gerekli — ölçülmüş açık (K42)", "",
         "| Ölçüt | Bizim korpus | Tohum havuzu |", "|---|---:|---:|",
         f"| kullanıcı mesajı | {b['n']} | {t['n']} |",
         f"| medyan kelime | {b['medyan_kelime']:.0f} | {t['medyan_kelime']:.0f} |",
         f"| ≤8 kelimelik mesaj | %{b['kisa_orani']*100:.1f} | %{t['kisa_orani']*100:.1f} |",
         f"| hiç noktalama içermeyen | %{b['noktalamasiz_orani']*100:.1f} | "
         f"%{t['noktalamasiz_orani']*100:.1f} |", "",
         "İnsanlar sohbet botuna üç cümle yazmaz. Bu dağılım **üretici artefaktı** ve",
         "K42'nin uyarısı tam burada: model \"zengin girdi → detaylı yansıtma\" öğreniyor,",
         "iki kelimelik girdide **detay uyduruyor**. Grounding skoru riskin en yüksek",
         "olduğu yerde kör.", "",
         "## 2. Aday kaynaklar ve her birinin düştüğü yer", "",
         "| Kaynak | Lisans | İnsan yazımı mı | Alan uygun mu | Sonuç |", "|---|---|---|---|---|",
         "| `data/seeds.jsonl` (2.240) | proje içi | ⛔ hayır — sentetik | ✅ evet | "
         "⛔ K42 bunları *artefakt* diye ölçtü; vahşi değil |",
         "| `TFLai/Turkish-Alpaca` | apache-2.0 | ⛔ hayır — çeviri/sentetik | ⛔ hayır | ⛔ |",
         "| `merve/turkish_instructions` | apache-2.0 | ⛔ hayır — çeviri/sentetik | ⛔ hayır | ⛔ |",
         f"| `OpenAssistant/oasst2` | apache-2.0 | ✅ **evet** | ⛔ hayır (genel amaçlı) | "
         f"⛔ **Türkçe prompter mesajı yalnızca {len(oasst_tr)} tane** |",
         "| Forum (Reddit/Quora vb.) | — | ✅ evet | ✅ evet | 🔴 **etik kurul kararı** (§14) |",
         "| İP5 pilot kullanıcıları | — | ✅ evet | ✅ evet | 🔴 rıza + pilot süreci |", ""]
    if oasst_tr:
        y += [f"`oasst2` ölçümü ({o['n']} mesaj): medyan **{o['medyan_kelime']:.0f}** kelime · "
              f"≤8 kelime **%{o['kisa_orani']*100:.0f}** · noktalamasız "
              f"**%{o['noktalamasiz_orani']*100:.0f}**.", "",
              "⚠️ Bu sayılar **hiçbir şey kanıtlamaz** — n çok küçük. Buraya yazılmasının tek",
              "sebebi aramanın yapıldığının kaydı olması (Kural 7).", ""]
    y += ["## 3. Neden sahtesi yapılmadı", "",
          "K42'nin register hedeflerini (kısa açılış ~%40, noktalamasız vb.) kendi",
          "tohumlarımıza uygulayıp \"vahşi\" diye etiketlemek mümkündü. **Yapılmadı**, çünkü",
          "bu dilimin var oluş sebebi tam olarak *\"bizim üretmediğimiz\"* olması. Kendi",
          "üreticimizin register'ını kendimiz bozup vahşi demek, ölçmek istediğimiz şeyi",
          "ölçmez — yalnızca ölçüyormuş gibi görünür. Bu, K47'nin (*bir aracın \"yok\" dediği",
          "yerde \"göremedim\" mi demek istediği ayrıca gösterilmeli*) veri tarafındaki ikizi.", "",
          "## 4. Karar için gereken tek şey", "",
          "Aşağıdakilerden **biri** yeterli:", "",
          "1. 🔴 **Etik kurul + yürütücü:** forum verisi *eval girdisi* olarak kullanılabilir mi?",
          "   ⚠️ Not: §14'ün kendi önerisi forumları *eğitim verisi* değil **dil referansı**",
          "   olarak kullanmaktı. Eval girdisi o ikisinin arasında ve ayrıca karara bağlanmalı.",
          "2. **İP5 pilotundan rızalı örneklem** — doğru kaynak bu; pilot takvimine bağlı.",
          "3. **Uzman korpusu B dilimi** (K20) — insan yazımı ama danışan mesajları;",
          "   A/B/C duvarı ve PII riski var, uzman kararı.", "",
          "Karar gelene kadar **Faz 3 bu maddede açık kalır** ve bu dosya o açığın kaydıdır.", ""]
    RAPOR.write_text("\n".join(y) + "\n")
    print(f"yazıldı: {RAPOR.relative_to(KOK)}")
    print(f"bizim korpus ≤8 kelime %{b['kisa_orani']*100:.1f} · noktalamasız "
          f"%{b['noktalamasiz_orani']*100:.1f} · oasst2 Türkçe prompter: {len(oasst_tr)}")


if __name__ == "__main__":
    main()
