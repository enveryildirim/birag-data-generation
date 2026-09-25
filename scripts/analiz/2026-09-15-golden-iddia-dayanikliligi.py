#!/usr/bin/env python3
"""golden.dev'in 29/48 tabanı judge'ın kararsız eksenlerine mi dayanıyor?

Tekrar-test (`2026-09-15-judge-tekrar-test.py`) judge'ın bazı eksenlerde kendisiyle
anlaşmadığını ölçtü. Cetvelin iddiaları o eksenlere dayanıyorsa taban sayısı da
oynaktır. Ayrıca işaret ayıklaması `rol_siniri_ihlali`nin BAĞLAM taşıyan kayıtlarda
sistematik yanlış pozitif verdiğini buldu — cetvelde bağlamlı öge varsa o da bulaşır.

Kullanım: uv run python scripts/analiz/2026-09-15-golden-iddia-dayanikliligi.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
GIRDI = KOK / "evals/golden.dev.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-golden-iddia-dayanikliligi.md"
BAGLAM = re.compile(r"<context|###\s*BAĞLAM|\[BAĞLAM\]|---\s*KAYNAK", re.I)

# Tekrar-testten (n=23) birebir uyum. `—` ölçülmedi.
KARARLILIK = {"grounding": 100, "mi_uyumu": 100, "kesif": 91, "dogallik": 91,
              "duygusal_tepki": 70, "yorumlama": 65, "anlasilirlik": 43,
              "rol_siniri_ihlali": 100, "soyut_adlastirma": 100, "siz_kaymasi": 100,
              "bos_guvence": 96, "karmasik_yansitma": 91, "ozerklik_vurgusu": 87,
              "takdir_var": 87, "ozet_var": 83, "yansitma_var": 100,
              "klise_acilis": 100, "ovgu_tonu": 100, "terapi_jargonu": 96,
              "cevapsiz_soru": 100, "klinik_guvenlik_ihlali": 100,
              "tuzak_uzman": 100, "tuzak_etiketleme": 100, "tuzak_soru_cevap": 100,
              "tuzak_erken_odak": 100, "tuzak_suclama": 100, "tuzak_erken_tavsiye": 100}
ESIK = 85


def main() -> None:
    ogeler = [json.loads(l) for l in open(GIRDI)]
    sha = hashlib.sha256(GIRDI.read_bytes()).hexdigest()

    alan = collections.Counter()
    tur = collections.Counter()
    for o in ogeler:
        for a in o.get("iddialar") or []:
            if not isinstance(a, dict):
                continue
            tur[a.get("tip", "?")] += 1
            if a.get("tip") == "judge":
                alan[a["alan"]] += 1

    baglamli = [o["id"] for o in ogeler
                if any(BAGLAM.search(m["content"]) for m in o["messages"] if m["role"] == "user")]
    toplam_judge = sum(alan.values())
    kararsiz = {k: v for k, v in alan.items() if KARARLILIK.get(k, 100) < ESIK}
    olculmemis = sorted(k for k in alan if k not in KARARLILIK)

    s = ["# golden.dev iddia dayanıklılığı", "",
         f"- tarih: {TARIH} · betik: `scripts/analiz/{Path(__file__).name}`",
         f"- girdi: `{GIRDI.relative_to(KOK)}` · SHA256 `{sha[:16]}…` · öge: {len(ogeler)}",
         f"- iddia: " + " · ".join(f"{k} {v}" for k, v in tur.most_common()), "",
         "Kararlılık sütunu tekrar-test ölçümünden gelir "
         "(`reports/analiz/2026-09-15-judge-tekrar-test.md`, n=23, aynı Sonnet iki geçiş). "
         f"Eşik: birebir uyum %{ESIK}.", "",
         "## Judge iddialarının dayandığı alanlar", "",
         "| alan | iddia | kendisiyle uyum | |", "|---|---:|---:|---|"]
    for k, v in alan.most_common():
        ka = KARARLILIK.get(k)
        isaret = "⚠️ kararsız" if ka is not None and ka < ESIK else ("" if ka is not None else "ölçülmedi")
        s.append(f"| `{k}` | {v} | {'—' if ka is None else '%' + str(ka)} | {isaret} |")

    tk = sum(kararsiz.values())
    s += ["", "## Okuma", "",
          f"- Judge iddiası toplam **{toplam_judge}**; kararsız eksene dayanan "
          f"**{tk}** (%{tk/toplam_judge*100:.0f}): " +
          (", ".join(f"`{k}`×{v}" for k, v in sorted(kararsiz.items(), key=lambda x: -x[1]))
           if kararsiz else "yok") + ".",
          f"- **`anlasilirlik` cetvelde hiç kullanılmıyor** — en kararsız eksen "
          f"(%43 uyum) tabana girmiyor." if "anlasilirlik" not in alan else
          f"- ⚠️ `anlasilirlik` cetvelde {alan['anlasilirlik']} iddiada kullanılıyor.",
          f"- En çok kullanılan iki alan `mi_uyumu` ({alan.get('mi_uyumu',0)}) ve "
          f"`grounding` ({alan.get('grounding',0)}); ikisi de tekrar-testte %100.",
          ]
    if olculmemis:
        s.append(f"- Kararlılığı ölçülmemiş alan: " + ", ".join(f"`{k}`" for k in olculmemis))

    s += ["", "## Bağlam (RAG) bulaşması", "",
          f"`rol_siniri_ihlali` üzerine **{alan.get('rol_siniri_ihlali', 0)}** iddia var ve "
          "işaret ayıklaması o boyutun BAĞLAM taşıyan kayıtlarda sistematik yanlış pozitif "
          "verdiğini buldu (Fisher p=0.0001).", ""]
    if baglamli:
        s += [f"⚠️ golden.dev'de **{len(baglamli)}** bağlamlı öge var: "
              + ", ".join(f"`{i}`" for i in baglamli) + ". Bu ögelerdeki "
              "`rol_siniri_ihlali` iddiaları v7 düzeltmesine kadar güvenilmez."]
    else:
        s += ["✅ golden.dev'de **hiç bağlamlı öge yok** — taban sayısı bu yanlış "
              "pozitiften etkilenmiyor.", "",
              "⚠️ **Ama bu bir kapsam açığıdır.** Korpusta 9/104 kayıt bağlam taşıyor; "
              "cetvelde sıfır. RAG kipinde gerileme ÖLÇÜLEMEZ. Cetvel genişletilirken "
              "bağlamlı öge eklenmeli — v7'nin `rol_bilgi_baglamdan` düzeltmesinden "
              "SONRA, yoksa eklenen ögeler doğrudan yanlış pozitif üretir."]

    RAPOR.write_text("\n".join(s) + "\n")
    print(f"judge iddiası {toplam_judge} · kararsız {tk} · bağlamlı öge {len(baglamli)} "
          f"· yazıldı: {RAPOR.relative_to(KOK)}")


if __name__ == "__main__":
    main()
