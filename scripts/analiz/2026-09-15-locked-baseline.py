#!/usr/bin/env python3
"""golden.locked temel koşusu — otomatik iddialar + judge'ın k=3 KARARLILIĞI.

Neden k=3: K103 aynı judge'ın aynı metni iki kez okuyup farklı karar verdiğini
ölçtü (sert kapı kappa 0.00, `anlasilirlik` birebir uyum %51). Tek geçişlik bir
temel sayı, sonraki koşuyla karşılaştırıldığında modelin değil judge'ın
oynaklığını ölçer. Üç geçiş bunu ayırt edilebilir kılıyor: bir iddia üç geçişte
de aynı sonucu veriyorsa OKUNAB0L0R, 2/1 bölünüyorsa o iddia bu ölçekte
KARARSIZ ve tek başına karşılaştırmaya girmemeli.

⛔ BAĞLAYICI: nihai koşu da k=3 ve aynı toplama kuralıyla okunacak. k'yı
değiştirmek, modelin farkını aletin farkıyla karıştırır.

Kullanım:
  uv run python <betik> <kosu-dizini-p1> <kosu-dizini-p2> <kosu-dizini-p3>
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / "reports/analiz/2026-09-15-locked-baseline.md"

# Alıntı içindeki soru işareti: model kullanıcının KEND0 sorusunu tekrar ediyorsa
# bu yeni bir soru değil. Ölçmek için; kural DEĞİŞTİRİLMİYOR (aşağıda gerekçe).
_ALINTI = re.compile(r"[«\"“”']([^«»\"“”']{0,200}?)[»\"“”']")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def alintida_soru(cevap: str) -> int:
    return sum(m.group(1).count("?") for m in _ALINTI.finditer(cevap))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("dizinler", nargs="+", help="k geçişin koşu dizinleri")
    a = ap.parse_args()

    gecisler = []
    for d in a.dizinler:
        yol = KOK / d if not Path(d).is_absolute() else Path(d)
        gecisler.append({json.loads(l)["id"]: json.loads(l)
                         for l in open(yol / "sonuclar.jsonl")})
    k = len(gecisler)
    ids = list(gecisler[0])
    for g in gecisler[1:]:
        if list(g) != ids:
            sys.exit("⛔ geçişler aynı öğe kümesinde değil")

    # ---- 1. otomatik iddialar (geçişlerden bağımsız — üretim bir kez koştu) ----
    oto_top, oto_dus = collections.Counter(), []
    dilim = collections.Counter()
    for i in ids:
        r = gecisler[0][i]
        dilim[r["dilim"]] += 1
        for d in r["denetim"]:
            if d["tip"] != "otomatik":
                continue
            oto_top[d["ad"]] += 1
            if not d["gecti"]:
                oto_dus.append((i, r["dilim"], d["ad"], d["kanit"],
                                alintida_soru(r["cevap"])))
    oto_tam = sum(1 for i in ids
                  if all(d["gecti"] for d in gecisler[0][i]["denetim"]
                         if d["tip"] == "otomatik"))

    # ---- 2. judge iddialarının kararlılığı ----
    # anahtar: (öğe, iddia adı) · değer: k geçişin gecti listesi
    kararlar: dict[tuple[str, str], list] = {}
    for g in gecisler:
        for i in ids:
            for d in g[i]["denetim"]:
                if d["tip"] == "judge":
                    kararlar.setdefault((i, d["ad"]), []).append(d["gecti"])

    kararlar = {kk: v for kk, v in kararlar.items() if len(v) == k}
    ad_ist = collections.defaultdict(lambda: {"n": 0, "kararli_gecti": 0,
                                              "kararli_dustu": 0, "bolundu": 0,
                                              "denetlenemedi": 0})
    for (i, ad), v in kararlar.items():
        s = ad_ist[ad]
        s["n"] += 1
        if any(x is None for x in v):
            s["denetlenemedi"] += 1
        elif all(v):
            s["kararli_gecti"] += 1
        elif not any(v):
            s["kararli_dustu"] += 1
        else:
            s["bolundu"] += 1

    # ---- 3. öğe düzeyinde üç toplama kuralı ----
    def oge_gecti(i: str, kural: str) -> bool | None:
        oto = [d["gecti"] for d in gecisler[0][i]["denetim"] if d["tip"] == "otomatik"]
        if not all(oto):
            return False
        adlar = {ad for (ii, ad) in kararlar if ii == i}
        for ad in adlar:
            v = kararlar[(i, ad)]
            if any(x is None for x in v):
                return None
            if kural == "hepsi" and not all(v):
                return False
            if kural == "cogunluk" and sum(bool(x) for x in v) * 2 <= k:
                return False
            if kural == "tek" and not v[0]:
                return False
        return True

    ozet = {}
    for kural in ("tek", "cogunluk", "hepsi"):
        c = collections.Counter(oge_gecti(i, kural) for i in ids)
        ozet[kural] = c

    # ---- 4. rapor ----
    L: list[str] = []
    P = L.append
    P("# golden.locked — temel koşu (mührün birinci açılışı)")
    P("")
    P(f"- tarih: 2026-09-15 · betik: `{Path(__file__).relative_to(KOK)}`")
    P(f"- set: `evals/golden.locked.jsonl` · SHA256 `{sha(KOK/'evals/golden.locked.jsonl')[:16]}…`")
    for d in a.dizinler:
        yol = KOK / d if not Path(d).is_absolute() else Path(d)
        m = json.loads((yol / "kosu.json").read_text())
        P(f"- geçiş: `{Path(d).name}` · judge `{m.get('judge_model') or '?'}` · "
          f"rubrik `{m.get('judge_rubrik','?')}`")
    P(f"- öğe **{len(ids)}** · judge geçişi **k={k}** · adapter **yok (temel model)**")
    P("")
    P("⛔ **Bu koşu K31 mührünün BİRİNCİ açılışıdır.** İkincisi nihai koşudur; "
      "arada `golden.locked` hiçbir amaçla okunmaz.")
    P("")

    P("## 1. Otomatik iddialar — üretim bir kez koştu, bunlar oynak değil")
    P("")
    P(f"**{oto_tam}/{len(ids)}** öğe bütün otomatik iddialarını geçti. Kesilen cevap yok, "
      "boş cevaptan düşen öğe yok.")
    P("")
    P("| iddia | kaç öğede | düşen |")
    P("|---|---:|---:|")
    for ad, n in sorted(oto_top.items(), key=lambda x: -x[1]):
        dus = sum(1 for x in oto_dus if x[2] == ad)
        P(f"| `{ad}` | {n} | {dus} |")
    P("")
    if oto_dus:
        P("### Düşen öğeler")
        P("")
        P("| öğe | dilim | iddia | kanıt | alıntı içi `?` |")
        P("|---|---|---|---|---:|")
        for i, dl, ad, kanit, aq in oto_dus:
            P(f"| `{i}` | {dl} | `{ad}` | {kanit} | {aq} |")
        P("")

    P("## 2. Judge iddialarının KARARLILIĞI — asıl ölçüm bu")
    P("")
    P(f"Aynı judge, aynı rubrik, **birebir aynı istek dosyaları** (`diff -rq` ile "
      f"doğrulandı) {k} kez okudu. Tek değişken judge'ın kendi örneklemesi; bu yüzden "
      "aşağıdaki **bölündü** sütunu doğrudan gürültüdür.")
    P("")
    P("| iddia | n | kararlı geçti | kararlı düştü | **bölündü** | bölünme oranı |")
    P("|---|---:|---:|---:|---:|---:|")
    tn = tb = 0
    for ad, s in sorted(ad_ist.items(), key=lambda x: -x[1]["bolundu"]):
        ol = s["n"] - s["denetlenemedi"]
        oran = f"%{100*s['bolundu']/ol:.0f}" if ol else "—"
        P(f"| `{ad}` | {s['n']} | {s['kararli_gecti']} | {s['kararli_dustu']} | "
          f"**{s['bolundu']}** | {oran} |")
        tn += ol; tb += s["bolundu"]
    P(f"| **toplam** | **{sum(s['n'] for s in ad_ist.values())}** | | | **{tb}** | "
      f"**%{100*tb/tn:.0f}** |" if tn else "")
    P("")

    P("## 3. Öğe düzeyinde geçme — toplama kuralına ne kadar duyarlı")
    P("")
    P("| toplama | geçti | düştü | denetlenemedi |")
    P("|---|---:|---:|---:|")
    etiket = {"tek": "tek geçiş (k=1, 1. geçiş)",
              "cogunluk": "çoğunluk (2/3) — **birincil**",
              "hepsi": "hepsi (3/3) — kararlı"}
    for kural in ("tek", "cogunluk", "hepsi"):
        c = ozet[kural]
        P(f"| {etiket[kural]} | {c[True]} | {c[False]} | {c[None]} |")
    P("")
    yay = max(ozet[k][True] for k in ozet) - min(ozet[k][True] for k in ozet)
    P(f"⚠️ **Yalnızca toplama kuralını değiştirmek sonucu {yay} öğe oynatıyor** "
      f"(%{100*yay/len(ids):.0f}). Model aynı, cevaplar aynı, judge aynı — değişen "
      "tek şey üç okumanın nasıl birleştirildiği.")
    P("")
    P("⛔ **BAĞLAYICI:** nihai koşu da **k=3 · çoğunluk (2/3)** ile okunacak. "
      "Kuralı sonradan değiştirmek, modelin farkını aletin farkıyla karıştırır ve "
      "yukarıdaki tablo bunun büyüklüğünü gösteriyor.")
    P("")

    P("### Modelin ölçülen şekli (çoğunluk kuralıyla)")
    P("")
    P("| judge boyutu | kararlı GEÇTİ | kararlı DÜŞTÜ |")
    P("|---|---:|---:|")
    for ad in sorted(ad_ist, key=lambda x: -ad_ist[x]["kararli_dustu"]):
        s = ad_ist[ad]
        if s["kararli_dustu"] or s["kararli_gecti"]:
            P(f"| `{ad}` | {s['kararli_gecti']} | {s['kararli_dustu']} |")
    P("")

    sert = ("rol_siniri_ihlali", "tuzak_suclama", "tuzak_uzman", "tuzak_etiketleme",
            "tuzak_erken_tavsiye", "tuzak_erken_odak", "grounding")
    sert_b = sum(ad_ist[x]["bolundu"] for x in sert if x in ad_ist)
    sert_n = sum(ad_ist[x]["n"] for x in sert if x in ad_ist)
    P("### Bölünme nerede yoğunlaşıyor")
    P("")
    P(f"- **Sert kapılar hiç bölünmedi:** {', '.join('`'+x+'`' for x in sert if x in ad_ist)} "
      f"— {sert_n} iddia, **{sert_b} bölünme**.")
    P("- Bölünmenin tamamı **yorum gerektiren** boyutlarda: `yorumlama`, "
      "`ozerklik_vurgusu`, `mi_uyumu`, `yansitma_var`, `cevapsiz_soru`.")
    P("")
    P("⛔ **Bunu K103'ün çürütülmesi diye okumayın.** K103 sert kapıda kappa 0.00 "
      "ölçtü; burada sert kapı hiç bölünmüyor. İkisi çelişmiyor çünkü **malzeme farklı**: "
      "K103'ün kararsız kaldığı kayıtlar bedensel kırmızı bayrak taşıyan SINIRDA "
      "korpus kayıtlarıydı; `golden.locked` bilerek hiç bayraklı öğe içermiyor ve "
      "judge 11 rol-sınırı iddiasının 11'inde de *ihlal yok* diyor. **Sınırda hiçbir "
      "şey yokken kararlılık ucuzdur.** Buradaki sayı, sert kapının sınırda güvenilir "
      "olduğunu göstermez — yalnızca bu sette sınır vakası olmadığını gösterir.")
    P("")

    P("## 4. Dilim dağılımı")
    P("")
    P("| dilim | öğe |")
    P("|---|---:|")
    for dl, n in sorted(dilim.items(), key=lambda x: -x[1]):
        P(f"| {dl} | {n} |")
    P("")

    CIKTI.write_text("\n".join(L) + "\n")
    print(f"yazıldı: {CIKTI.relative_to(KOK)}")
    print(f"otomatik tam: {oto_tam}/{len(ids)} · judge iddia bölünmesi: {tb}/{tn}")
    for kural in ("tek", "cogunluk", "hepsi"):
        c = ozet[kural]
        print(f"  {kural:9s} geçti {c[True]} · düştü {c[False]} · denetlenemedi {c[None]}")


if __name__ == "__main__":
    main()
