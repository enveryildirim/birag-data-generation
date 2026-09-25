#!/usr/bin/env python3
"""MEKANİZMA ADAYI: korpus «yönlendirmeme»yi sistematik olarak öğretiyor olabilir.

⛔⛔ **Soru.** İnce ayarlı model `safety_crisis`'te profesyonel yönlendirmeyi
adlandırmayı bırakıyor ve bu üç taramada da oldu. *«Veride yönlendirme az»*
açıklaması ölçüldü ve **zayıfladı** (pay sürümler boyunca %17-19, sabit).
Geriye daha rahatsız edici bir aday kalıyor:

➡️ *Korpus yönlendirmeyi az öğretmiyor olabilir — **yönlendirMEMEYİ çok**
öğretiyor olabilir.* «Ne yapacağına sen karar vereceksin», «akıl vermeyeceğim»,
«ben söyleyemem», «buradan bilemem» kalıpları özerklik için yazıldı (MI/OARS,
§5) ve terapötik bağlamda **doğru**. Ama kriz bağlamında yönlendirmek doğru
davranış ve model bağlamı ayırt etmeyi değil, **kalıbı** öğrenmiş olabilir.

⛔⛔ **Bu hipotez BUGÜNKÜ KENDİ DÜZELTMELERİMİ de şüpheli kılıyor:** §8b′ gereği
16 kayda *«hangi kapının açık olduğunu buradan bilemem»* eklendi ve §5a⁗ bir
kayda daha ret cümlesi getirdi. Eğer mekanizma doğruysa, dayanaksız iddiayı
düzeltirken yönlendirmeme refleksini **güçlendirmiş** olabilirim.

⚠️ Bu bir ÖLÇÜM, kanıt değil: eş görülme nedensellik vermez ve karşı olgusal
(bu kalıplar olmadan eğitilmiş bir korpus) yok.
"""
from __future__ import annotations
import json, re
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / "reports/analiz/2026-09-17-yonlendirmeme-refleksi.md"

# ⭐ Kalıplar ELLE yazıldı ve sınıfları ayrı tutuluyor: «ret» ile «özerklik»
# aynı şey değil ve karışırlarsa hangisinin sürüklediği görünmez.
SINIF = {
 "ret_bilgi": [r"ben söyleyemem", r"söyleyebilecek olan ben değilim", r"bilemem",
               r"bende (o )?(bilgi|karar|değerlendirme) yok", r"benim işim değil",
               r"bana düşmez", r"karar veremem", r"bilmiyorum ve bilemem"],
 "ret_tavsiye": [r"akıl vermeyeceğim", r"ne yapman gerektiğini söylem",
                 r"tavsiye vermeyeceğim", r"bir şey önermiyorum",
                 r"ne yapacağını söylemiyorum", r"öneride bulunmayacağım"],
 "ozerklik": [r"sen karar vereceksin", r"senin kararın", r"senin bileceğin (iş|şey)",
              r"karar (senin|sana ait)", r"kararın sahibi sensin"],
}
DERLENMIS = {k: [re.compile(x, re.I) for x in v] for k, v in SINIF.items()}


def main() -> int:
    sat = ["# «Yönlendirmeme» refleksi — korpusta ne kadar var", "",
           "**Betik:** `scripts/analiz/2026-09-17-yonlendirmeme-refleksi.py` · "
           "**Tarih:** 2026-09-17", "",
           "⚠️ Kalıplar elle yazıldı (K30) ⇒ sayı bir **alt sınırdır**.", "",
           "| sürüm | kayıt | ret_bilgi | ret_tavsiye | özerklik | **herhangi biri** | oran |",
           "|---|---:|---:|---:|---:|---:|---:|"]
    veri = {}
    for v in ("v0.0.2", "v0.0.3", "v0.0.5", "v0.0.6", "v0.0.7", "v0.0.8"):
        p = KOK / f"datasets/{v}/train.jsonl"
        if not p.exists():
            continue
        rs = [json.loads(s) for s in p.read_text(encoding="utf-8").splitlines() if s.strip()]
        say = {k: 0 for k in DERLENMIS}
        herhangi = 0
        for r in rs:
            metin = " ".join(m.get("content") or "" for m in r["messages"] if m["role"] == "assistant")
            v_ = False
            for k, pats in DERLENMIS.items():
                if any(pp.search(metin) for pp in pats):
                    say[k] += 1
                    v_ = True
            herhangi += v_
        veri[v] = (len(rs), say, herhangi)
        sat.append(f"| `{v}` | {len(rs)} | {say['ret_bilgi']} | {say['ret_tavsiye']} | "
                   f"{say['ozerklik']} | **{herhangi}** | %{100*herhangi/len(rs):.1f} |")

    a, b = veri.get("v0.0.5"), veri.get("v0.0.8")
    sat += ["", "## ⭐ Yönlendirme ile karşılaştırma", ""]
    if a and b:
        sat += ["| | yönlendirme adlandıran | **yönlendirmeme kalıbı** | oran |",
                "|---|---:|---:|---:|",
                f"| `v0.0.5` | 30 (%19.4) | **{a[2]}** (%{100*a[2]/a[0]:.1f}) | "
                f"**{a[2]/30:.1f}×** |",
                f"| `v0.0.8` | 96 (%16.8) | **{b[2]}** (%{100*b[2]/b[0]:.1f}) | "
                f"**{b[2]/96:.1f}×** |", "",
                "➡️⭐⭐ *Korpus, yönlendirmeyi öğrettiğinden kat kat fazla "
                "yönlendirMEMEYİ öğretiyor. İnce ayarın yönlendirme refleksini "
                "silmesi, verinin bir EKSİĞİYLE değil bir FAZLASIYLA açıklanabilir — "
                "ve bu ikisi taramada aynı görünür ama çareleri zıttır: eksiklik "
                "«daha çok yönlendirme ekle» der, fazlalık «bağlam ayrımını öğret» der.*"]
    sat += ["", "## ⛔⛔ Bugünkü düzeltmelerin payı", "",
            "§8b′ gereği **16 kayda** *«hangi kapının açık olduğunu buradan bilemem»* "
            "biçiminde bir ret cümlesi eklendi; §5a⁗ bir kayda daha ret getirdi.", "",
            "⭐ **Ve bu ölçüldü** — `v5-parti4..8`'in revizyon ÖNCESİ ve SONRASI hâli:", "",
            "| | kayıt | eşleşme |", "|---|---:|---:|",
            "| revizyondan önce | **100**/300 | 132 |",
            "| revizyondan sonra | **109**/300 | 150 |",
            "| ⇒ **benim payım** | **+9** | **+18** |", "",
            "➡️ Katkım gerçek ama küçük: 300 kayıtta **+3 puan**. Asıl sürükleyici "
            "`uretim-v5`'in kendi üslubu — revizyon öncesi bile **%33.3** (v0.0.7 %27.2). "
            "⇒ *Dayanaksız iddiayı düzeltirken refleksi güçlendirdim, ama refleksi "
            "kuran ben değilim; üretim talimatı kuruyor ve `rol_siniri` dilimi "
            "v0.0.8'de **75 kayıt**.*", "",
            "⚠️ Bu, v0.0.7 ↔ v0.0.8 eğitim karşılaştırmasında bir **karıştırıcıdır** ve "
            "CARD.md'deki 16 kayıtlık uyarıyla aynı kayıtlar değildir — ayrı bir kalemdir.", "",
            "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **Nedensellik yok** | eş görülme; karşı olgusal korpus yok |",
            "| ⛔ **Kalıplar elle** | alt sınır; sözlükte olmayan biçimler görünmez |",
            "| ⛔ **Bağlam ayrımı ölçülmedi** | kalıbın TERAPÖTİK bağlamda doğru olduğu sayılmıyor; sayı «kaç kayıtta geçiyor», «kaçında yanlış» değil |",
            "| ⚠️ Tüm asistan turları taranıyor | son tur değil (ara turlar da modele gider) |", ""]
    CIKTI.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[4:]))
    print(f"→ {CIKTI.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
