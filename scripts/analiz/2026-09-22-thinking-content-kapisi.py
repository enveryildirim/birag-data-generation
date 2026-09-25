#!/usr/bin/env python3
"""`thinking` ↔ `content` tutarlılığı — T239'un bıraktığı denetim yüzeyi.

⛔⛔ **T239 ne bulmuştu.** `v6-parti8 / ad5658bc`'nin cevabı sistemin
veremeyeceği bir gizlilik güvencesi veriyordu ve kaydın **kendi iç
muhakemesi** *«abartılı bir gizlilik vaadi vermek kolay olurdu, ikisini de
yapmıyorum»* diyordu. ⇒ İç muhakeme de bir **beyandır** ve kaydın içinde
durur, ama hiçbir kapı onu cevaba karşı okumuyordu. `beyan-metin-uyumu`
yalnız `gen_meta` beyanlarını denetliyor.

⭐ **Desen hayal edilmedi, ÖLÇÜLDÜ.** Korpustaki 1015 iç muhakemede
**2980 olumsuz ilan** var (169 farklı fiil). En sık ve en temiz
denetlenebilir olanı **«soru sormuyorum»** (316 kayıt): ilan edilmişse
cevapta soru **olmamalı**.

⛔ **Soru sayımı KOPYALANMIYOR (K103):** `checks.count_questions` kullanılır
— aynı kayıt üretim kapısında ve burada **aynı sayıyı** görür.

⚠️ **Bu kapı bir ALT SINIRDIR.** 2980 ilanın yalnız bir ailesini
denetliyor; ötekiler (*«adını anmıyorum»*, *«önermiyorum»*, *«plan
kurmuyorum»*) nesnesi serbest metin olduğu için mekanik olarak
denetlenemiyor — T22 serisinin tam olarak uyardığı sınır.

Kullanım: uv run python <betik> [--kume datasets/v0.0.18/train.jsonl]
Çıktı: reports/analiz/2026-09-22-thinking-content-kapisi.md
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from checks import count_questions  # noqa: E402

TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-thinking-content-kapisi.md"
KUME = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--kume=")),
            "datasets/v0.0.18/train.jsonl")

# ⛔⛔ İLK SÜRÜM YANLIŞ POZİTİF ÜRETTİ ve okuma yakaladı (T260).
#   Desen `soru sormuyorum` idi ve **«İzin isterken KAPALI BİR soru
#   sormuyorum»** içinde eşleşti — nitelikli bir ilanı mutlak sanmış oldu;
#   o kayıt açık uçlu bir soru soruyor, yani TUTARLI. T22 ailesinin biçimi.
# ⭐ Onarım: ilan, kendi YAN CÜMLESİNİN BAŞINDA durmalı. Araya sıfat girerse
#   (`kapalı bir`, `yönlendiren`, `ikinci`) ilan MUTLAK değildir ⇒ sayılmaz.
#   Yalnız genel belirteçlere izin verilir.
BELIRTEC = r"(?:hiç|artık|ayrıca|burada|şimdi|bu\s+turda|de|da|bir\s+de)\s+"
ILAN_SORU = re.compile(
    rf"^(?:{BELIRTEC})*"
    r"(soru\s+sormuyorum|soru\s+ile\s+bitirmiyorum|soruyla\s+bitirmiyorum)\b",
    re.I)
IPTAL = re.compile(r"(değil|ama|yine de|fakat)\s*$", re.I)


def ilan_var(thinking: str) -> str | None:
    """İlan cümlesini döndürür; yoksa None. ⛔ KARAR VERMEZ, OKUR."""
    # ⭐ yan cümlelere de böl: «… bırakıyorum ve soru sormuyorum» geçerli bir
    #   ilandır, ama «… kapalı bir soru sormuyorum» değildir.
    for c in re.split(r"(?<=[.!?])\s+|\n|\s+(?:ve|ama|fakat)\s+", thinking or ""):
        c = c.strip(" ,;—-")
        if ILAN_SORU.match(c) and not IPTAL.search(c):
            return c
    return None


def main() -> int:
    kay = [json.loads(l) for l in open(KOK / KUME)]
    ilanli, ihlal = [], []
    for r in kay:
        son = [m for m in r["messages"] if m["role"] == "assistant"][-1]
        t = son.get("thinking") or ""
        c = son.get("content") or ""
        cum = ilan_var(t)
        if not cum:
            continue
        q = count_questions(c)
        ilanli.append(r["id"])
        if q > 0:
            ihlal.append((r["id"], (r.get("gen_meta") or {}).get("parti"), cum, q, c))

    n = len(kay)
    sat = ["# `thinking` ↔ `content` kapısı — ilk aile: «soru sormuyorum»", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Küme:** `{KUME}` ({n} kayıt)  ", "",
           "⛔⛔ **T239'un bıraktığı yüzey.** İç muhakeme de bir **beyandır** "
           "ve kaydın içinde durur; `beyan-metin-uyumu` yalnız `gen_meta` "
           "beyanlarını denetliyor, iç muhakemeyi **hiç okumuyor**.", "",
           "⭐ **Desen ölçüldü, hayal edilmedi:** korpustaki 1015 iç muhakemede "
           "**2980 olumsuz ilan** var (169 fiil). En sık ve mekanik olarak en "
           "temiz denetlenebilir olanı `sormuyorum` (316).", "",
           "## Ölçüm", "", "| | |", "|---|---:|",
           f"| iç muhakemede *«soru sormuyorum»* ilanı | **{len(ilanli)}** |",
           f"| ⛔ bunlardan cevabında **soru olan** | **{len(ihlal)}** |",
           f"| ihlal oranı | %{100*len(ihlal)/max(len(ilanli),1):.1f} |", ""]
    if ihlal:
        sat += ["## ⛔ İhlaller — hepsi OKUNACAK", "",
                "| kayıt | parti | iç muhakeme ilanı | soru | cevaptan |",
                "|---|---|---|---:|---|"]
        for i, parti, cum, q, c in ihlal[:20]:
            soru = next((s.strip() for s in re.split(r"(?<=[.!?])\s+", c)
                         if "?" in s), c[:60])
            sat.append(f"| `{i[:10]}` | `{parti}` | *«{cum[:60]}»* | {q} | "
                       f"*«{soru[:70]}»* |")
        if len(ihlal) > 20:
            sat.append(f"| … | | **+{len(ihlal)-20} kayıt daha** | | |")
    else:
        sat += ["⭐ **İhlal yok.** İlan edilen her kayıtta cevap gerçekten "
                "sorusuz.", "",
                "⛔ Bu *«iç muhakeme hep tutarlı»* demek DEĞİLDİR: denetlenen "
                "tek aile bu ve 2980 ilanın yalnız bir kısmı."]
    sat += ["", "## ⛔ Bu kapının söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **ALT SINIR** | 2980 ilanın yalnız **bir ailesi** "
            "denetleniyor. *«Adını anmıyorum»*, *«önermiyorum»*, *«plan "
            "kurmuyorum»* gibi ilanların nesnesi **serbest metindir** ve "
            "mekanik olarak denetlenemiyor — T22 serisinin uyardığı sınır |",
            "| ⛔ **T239'un kendi vakasını YAKALAMAZ** | `ad5658bc`'nin ilanı "
            "*«abartılı bir gizlilik vaadi vermiyorum»*; nesnesi bir kavram, "
            "dizge değil ⇒ bu kapı onu göremez. Onu **okuma** buldu |",
            "| ⛔ **İlan ≠ niyet** | iç muhakeme de üretilmiş metindir; "
            "*«soru sormuyorum»* yazıp soru sormak bir **tutarsızlıktır**, "
            "ama hangisinin doğru davranış olduğunu bu kapı söylemez |",
            "| ⛔⛔ **İLK SÜRÜM YANLIŞ POZİTİF ÜRETTİ** | desen `soru sormuyorum` idi ve *«İzin isterken **kapalı bir** soru sormuyorum»* içinde eşleşti — nitelikli bir ilanı mutlak sandı. O kayıt açık uçlu soru soruyor, yani **tutarlı**. ⭐ Okuma yakaladı, ölçüm değil (T260) |",
            "| ⚠️ **İptal deseni dar** | ilanı geçersiz kılan çevre (*«…değil»*, *«ama»*) yalnız cümle sonunda aranıyor ⇒ yanlış pozitif hâlâ mümkün; ihlaller bu yüzden tek tek yazılı |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[sat.index("## Ölçüm"):]))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
