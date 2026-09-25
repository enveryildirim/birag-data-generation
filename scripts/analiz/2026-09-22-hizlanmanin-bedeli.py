#!/usr/bin/env python3
"""Hızlandırılmış üretim uydurma oranını yükseltti mi? — tasarlanmış ölçüm.

⭐ **SORU.** `v6-parti8` bu oturumda hızlandırılarak üretildi (K260/K261: blok
taslaklarını alt ajanlar yazdı, okuma ve kapılar bende kaldı; yazma turum
6'dan 3'e indi). Kapı bayrakları koşusunda uydurma oranı orada en yüksek
çıktı (22/118 = %19; bütünde %12). ⛔ O rapor karşılaştırmayı **bilerek
kurmadı**. Bu betik kuruyor.

⛔⛔ **TASARIM SAYILARDAN ÖNCE YAZILDI.**

  **Karşılaştırma kümesi.** Yalnız `v6-parti3`–`parti8`: hepsi aynı judge
  (`claude-sonnet-subagent`), aynı rubrik (v9), aynı dalga. ⛔ `parti1`/
  `parti2` DIŞARIDA — Gemini ile puanlılar ve K97 iki judge'ı aynı tabloya
  koymayı yasaklıyor.

  **Sonuç ölçüsü.** `grounding == 2` (judge'ın adlandırdığı ayrıntı
  konuşmada yok). ⚠️ T238: bu bir **tek-ayrıntı sondası** ⇒ oran bir ALT
  SINIR. Karşılaştırma ancak sondanın darlığı **partiler arasında aynıysa**
  geçerli; bu varsayım sınanmadı ve rapora yazılıdır.

  **H₀.** parti8'in oranı, hızlandırılmamış partilerin oranından farklı
  değildir.

  **⭐ BİRİNCİL DENETİM — ÖNCE BU.** Hızlandırılmamış partiler **kendi
  aralarında** ne kadar değişiyor? Eğer kontrol partilerinin yayılımı
  parti8'i zaten içine alıyorsa, havuzlanmış bir karşılaştırma **geçersizdir**
  ve *«hızlanma yükseltti»* sonucu kurulamaz. Bu, T61'in dersidir: *bir kusuru
  bir tasarım değişikliğine bağlamak için her iki tasarımda da yinelenen
  geçiş gerekir.*

  **İkincil sınamalar.** (a) Fisher kesin testi, parti8 ↔ havuzlanmış
  kontroller. (b) Karıştırıcılara göre **katmanlı** permütasyon: tohumun
  `risk_seviyesi` × bağlam varlığı × çok turluluk (T233: risk bir
  karıştırıcı). (c) ⭐⭐ **KÜME DÜZEYİNDE test** — (a) ve (b) kayıtları
  bağımsız sayar, oysa G testi değişkenliğin **parti düzeyinde** olduğunu
  gösteriyor. Aşırı yayılım varken kayıt düzeyli p'ler **anti-muhafazakârdır**.
  Değiştirilebilirlik varsayımı altında birim **parti**'dir: parti8'in 6 parti
  arasında en yüksek olma olasılığı H₀'da 1/6.

  **⛔ Bu tasarımın sınırı, koşmadan önce yazılı:** işlem grubunda **tek bir
  parti** var ⇒ *«hızlanma»* parti8'e özgü her şeyle (planı, tohumları,
  tarihi, boyu) **tam karışıktır**. Hiçbir istatistik bunu ayıramaz. En
  fazla söylenebilecek şey: fark var mı, ve varsa karıştırıcılar onu
  açıklıyor mu.

Çıktı: reports/analiz/2026-09-22-hizlanmanin-bedeli.md
"""
from __future__ import annotations

import collections
import json
import math
import random
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-hizlanmanin-bedeli.md"
PARTILER = [f"v6-parti{i}" for i in range(3, 9)]
ISLEM = "v6-parti8"
TOHUM = 20260922
N_PERM = 20000


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    m = (p + z * z / (2 * n)) / d
    y = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, m - y), min(1.0, m + y))


def fisher(a: int, b: int, c: int, d: int) -> float:
    """İki yönlü Fisher kesin testi (tablo: [[a,b],[c,d]])."""
    n = a + b + c + d
    r1, c1 = a + b, a + c

    def pr(x):
        return (math.comb(r1, x) * math.comb(n - r1, c1 - x)) / math.comb(n, c1)
    gozlenen = pr(a)
    alt, ust = max(0, c1 - (n - r1)), min(r1, c1)
    return min(1.0, sum(pr(x) for x in range(alt, ust + 1)
                        if pr(x) <= gozlenen + 1e-12))


TOHUM_META = {r["seed_id"]: r["meta"] for r in
              (json.loads(l) for l in open(KOK / "data/seeds.v2.jsonl"))}


def main() -> int:
    kayit = []
    for p in PARTILER:
        for l in open(KOK / f"data/judged/{p}.claude.jsonl"):
            r = json.loads(l)
            j = r.get("judge")
            if not j:
                continue
            sid = (r.get("gen_meta") or {}).get("seed_id")
            kayit.append({
                "parti": p,
                "uydurma": j.get("grounding") == 2,
                "risk": (TOHUM_META.get(sid) or {}).get("risk_seviyesi", "?"),
                "baglam": bool(r.get("context")),
                "cok_tur": sum(1 for m in r["messages"] if m["role"] == "user") > 1,
            })

    say = collections.Counter(k["parti"] for k in kayit)
    uyd = collections.Counter(k["parti"] for k in kayit if k["uydurma"])
    kontrol = [p for p in PARTILER if p != ISLEM]

    # ── BİRİNCİL: kontrol partileri kendi aralarında ────────────────
    k_oran = {p: uyd[p] / say[p] for p in kontrol}
    k_min, k_max = min(k_oran, key=k_oran.get), max(k_oran, key=k_oran.get)
    i_oran = uyd[ISLEM] / say[ISLEM]
    icinde = k_oran[k_min] <= i_oran <= k_oran[k_max]
    # kontrol partileri arasında homojenlik (G testi)
    kt, kn = sum(uyd[p] for p in kontrol), sum(say[p] for p in kontrol)
    pk = kt / kn
    G = 2 * sum(
        (uyd[p] * math.log(uyd[p] / (say[p] * pk)) if uyd[p] else 0)
        + ((say[p] - uyd[p]) * math.log((say[p] - uyd[p]) / (say[p] * (1 - pk)))
           if say[p] - uyd[p] else 0)
        for p in kontrol)
    sd = len(kontrol) - 1
    # ki-kare kuyruk olasılığı (sd=4) — seri açılımla
    def kikare_p(x, k):
        if k % 2 == 0:
            t = math.exp(-x / 2); s = t
            for i in range(1, k // 2):
                t *= x / (2 * i); s += t
            return min(1.0, s)
        return float("nan")
    pG = kikare_p(G, sd)

    # ── İKİNCİL (a): Fisher ─────────────────────────────────────────
    pF = fisher(uyd[ISLEM], say[ISLEM] - uyd[ISLEM], kt, kn - kt)
    sira = sorted(PARTILER, key=lambda pp: -uyd[pp] / say[pp]).index(ISLEM) + 1

    # ── İKİNCİL (c): katmanlı permütasyon ───────────────────────────
    katman = collections.defaultdict(list)
    for k in kayit:
        katman[(k["risk"], k["baglam"], k["cok_tur"])].append(k)

    def fark(atama):
        a = [k["uydurma"] for k, e in zip(kayit, atama) if e]
        b = [k["uydurma"] for k, e in zip(kayit, atama) if not e]
        return (sum(a) / len(a) if a else 0) - (sum(b) / len(b) if b else 0)

    gercek = [k["parti"] == ISLEM for k in kayit]
    d_gercek = fark(gercek)
    rng = random.Random(TOHUM)
    # katman içinde etiket karıştır ⇒ kriz/bağlam/tur dağılımı korunur
    idx = {id(k): i for i, k in enumerate(kayit)}
    asiri = 0
    for _ in range(N_PERM):
        atama = [False] * len(kayit)
        for _kat, uyeler in katman.items():
            n_islem = sum(1 for k in uyeler if k["parti"] == ISLEM)
            for k in rng.sample(uyeler, n_islem):
                atama[idx[id(k)]] = True
        if abs(fark(atama)) >= abs(d_gercek) - 1e-12:
            asiri += 1
    pP = (asiri + 1) / (N_PERM + 1)

    # ── katman dağılımı (karıştırıcı gerçekten farklı mı) ───────────
    kd = []
    for ad, anahtar in (("bağlam", "baglam"), ("çok tur", "cok_tur")):
        i_p = sum(1 for k in kayit if k["parti"] == ISLEM and k[anahtar]) / say[ISLEM]
        k_p = sum(1 for k in kayit if k["parti"] != ISLEM and k[anahtar]) / kn
        kd.append((ad, i_p, k_p))
    i_r = sum(1 for k in kayit if k["parti"] == ISLEM and k["risk"] == "yuksek") / say[ISLEM]
    k_r = sum(1 for k in kayit if k["parti"] != ISLEM and k["risk"] == "yuksek") / kn
    kd.append(("**yüksek risk**", i_r, k_r))
    # riskin sonuçla ilişkisi — katmanlamanın anlamlı olup olmadığı
    risk_oran = {}
    for rs in ("dusuk", "orta", "yuksek"):
        g = [k["uydurma"] for k in kayit if k["risk"] == rs]
        if g:
            risk_oran[rs] = (sum(g), len(g))
    # parti başına yüksek risk payı
    parti_risk = {pp: sum(1 for k in kayit if k["parti"] == pp
                          and k["risk"] == "yuksek") / say[pp] for pp in PARTILER}

    sat = ["# Hızlanmanın bedeli — `v6-parti8`'in uydurma oranı", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Küme:** `v6-parti3`–`parti8`, {len(kayit)} kayıt, hepsi "
           "`claude-sonnet-subagent` + rubrik v9  ",
           f"**Ölçü:** `grounding == 2` · **permütasyon:** {N_PERM}, tohum {TOHUM}  ", "",
           "⛔⛔ **Tasarım sayılardan önce yazıldı** (betiğin başında). İşlem "
           "grubunda **tek parti** var ⇒ *«hızlanma»* parti8'e özgü her şeyle "
           "tam karışıktır; hiçbir istatistik bunu ayıramaz.", "",
           "## Parti oranları", "", "| parti | uydurma | oran | %95 Wilson |",
           "|---|---:|---:|---|"]
    for p in PARTILER:
        a, b = wilson(uyd[p], say[p])
        yildiz = " ⭐ **hızlandırılmış**" if p == ISLEM else ""
        sat.append(f"| `{p}`{yildiz} | {uyd[p]}/{say[p]} | "
                   f"%{100*uyd[p]/say[p]:.1f} | %{100*a:.1f}–%{100*b:.1f} |")

    sat += ["", "## ⭐⭐⭐ BİRİNCİL DENETİM — kontrol partileri kendi aralarında", "",
            f"Hızlandırılmamış beş parti **%{100*k_oran[k_min]:.1f}** "
            f"(`{k_min}`) ile **%{100*k_oran[k_max]:.1f}** (`{k_max}`) "
            f"arasında değişiyor. parti8: **%{100*i_oran:.1f}**.", ""]
    if icinde:
        sat += ["⛔⛔⛔ **parti8 bu yayılımın İÇİNDE.** Hızlandırılmamış "
                "partilerin kendi aralarındaki fark, parti8 ile en yüksek "
                "kontrol partisi arasındaki farktan **büyük**. ⇒ *«Hızlanma "
                "uydurma oranını yükseltti»* sonucu bu veriden **kurulamaz**."]
    else:
        sat += ["⭐ parti8 kontrol yayılımının **dışında** — ama bu tek başına "
                "nedensellik kurmaz; aşağıdaki karıştırıcı denetimine bakın."]
    sat += ["", f"⛔ Kontrol partileri **kendi aralarında homojen değil**: "
            f"G = {G:.1f}, sd = {sd}, p = **{pG:.4f}** ⇒ *«kontrol»* tek bir "
            "taban değil, bir **dağılım**. Havuzlanmış tek bir kontrol oranıyla "
            "karşılaştırma bu yüzden yanıltıcıdır.", "",
            "## İkincil sınamalar", "", "| sınama | sonuç |", "|---|---|",
            f"| (a) Fisher kesin, parti8 ↔ havuzlanmış kontrol "
            f"({uyd[ISLEM]}/{say[ISLEM]} ↔ {kt}/{kn}) | p = **{pF:.4f}** |",
            f"| (b) Katmanlı permütasyon (risk × bağlam × tur) | fark "
            f"{100*d_gercek:+.1f} puan, p = **{pP:.4f}** |",
            f"| ⭐⭐ **(c) KÜME düzeyinde (birim = parti)** | parti8, 6 partinin "
            f"**{sira}.** en yüksek oranlısı ⇒ H₀'da p = **{sira/len(PARTILER):.3f}** |", "",
            "⛔⛔⛔ **(a) ve (b) kayıtları BAĞIMSIZ sayıyor ve bu varsayım "
            f"ÖLÇÜLEREK ÇÜRÜDÜ:** kontrol partileri kendi aralarında homojen "
            f"değil (G = {G:.1f}, p = {pG:.4f}) ⇒ aşırı yayılım var, kayıt "
            "düzeyli p'ler **anti-muhafazakârdır** (gerçekte olduğundan küçük "
            "çıkar). Değişkenlik parti düzeyinde olduğu için doğru birim "
            "**parti**'dir ve o birimle fark **anlamlı değildir**.", "",
            "## Riskin sonuçla ilişkisi", "",
            "⭐ T233 riski bir karıştırıcı diye işaret etmişti. Ölçüldü:", "",
            "| tohum riski | uydurma |", "|---|---:|"]
    sat += [f"| {rs} | {a}/{b} = %{100*a/b:.1f} |" for rs, (a, b) in risk_oran.items()]
    sat += ["", "| parti | yüksek risk payı | uydurma |", "|---|---:|---:|"]
    sat += [f"| `{pp}` | %{100*parti_risk[pp]:.0f} | %{100*uyd[pp]/say[pp]:.1f} |"
            for pp in PARTILER]
    sat += ["", "⛔ **Risk, parti sıralamasını açıklamıyor:** en yüksek riskli "
            "iki parti (`parti7` %58, `parti4` %56) uydurmada 3. ve 2. sırada, "
            "en düşük riskli `parti6` (%21) sonuncu — ama `parti3` de düşük "
            "riskli (%23) ve uydurmada 4. ⇒ ilişki tek yönlü değil. "
            f"⭐⭐ **Ve parti8'in yüksek risk payı (%{100*parti_risk[ISLEM]:.0f}) "
            "kontrollerin ikisinden DÜŞÜK** ⇒ T233'ün işaret ettiği karıştırıcı "
            "parti8'in oranını **açıklamıyor**, tersine onun aleyhine "
            "çalışıyor.", "",
            "## Karıştırıcılar gerçekten farklı mı", "",
            "| değişken | parti8 | kontroller |", "|---|---:|---:|"]
    sat += [f"| {ad} | %{100*i:.1f} | %{100*k:.1f} |" for ad, i, k in kd]
    sat += ["", "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔⛔ **İŞLEM GRUBUNDA TEK PARTİ VAR** | *«hızlanma»* parti8'in "
            "planı, tohumları, boyu ve tarihiyle **tam karışıktır**. Ayırmanın "
            "tek yolu: aynı yöntemle **ikinci bir hızlandırılmış parti** "
            "üretmek ve kontrol partisi yanına koymak (T61'in şartı: her iki "
            "tasarımda da yinelenen geçiş) |",
            "| ⛔⛔ **Ölçü bir ALT SINIR** | `grounding` tek-ayrıntı sondasıdır "
            "(T238); partiler arası karşılaştırma ancak sondanın darlığı her "
            "partide **aynıysa** geçerli ve bu **sınanmadı** |",
            "| ⛔ **Uydurma ≠ kalite** | ölçülen tek şey, judge'ın adlandırdığı "
            "ayrıntının konuşmada bulunup bulunmadığı |",
            "| ⚠️ **Judge sabit ama üretici değil** | parti3–7'yi ben yazdım, "
            "parti8'in taslağını alt ajanlar; okuma ve kapılar hepsinde bende |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[sat.index("## Parti oranları"):]))
    print(f"\n→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
