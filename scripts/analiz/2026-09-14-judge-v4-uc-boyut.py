#!/usr/bin/env python3
"""Judge v4 — "kanıt → puan" deseni üç boyutta.

v3 `anlasilirlik`'te işe yaradı (uyum oranı 0.53 → 0.87) ve kazancın büyük kısmının
**ayrıştırmadan** geldiği görüldü. v4 aynı deseni `dogallik` ve `mi_uyumu`'na uyguluyor.

İki protokol iyileştirmesi:
  1. Holistik puanlar artık sorulardan ÖNCE isteniyor → kontrol kirli değil.
  2. Bayrakların güvenilirliği, uzmandan bağımsız olarak **deterministik kontrollerle**
     sınanıyor (`bos_guvence` filtre listesi, `siz` register regex'i).

Çıktı: reports/analiz/2026-09-14-judge-v4-uc-boyut.md
"""
from __future__ import annotations

import collections
import hashlib
import json
import pathlib
import re
import statistics
import sys

KOK = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from filter import (ANLASILIRLIK_BAYRAKLARI, DOGALLIK_BAYRAKLARI,  # noqa: E402
                    OARS_BECERILERI, TUZAKLAR)
from checks import scan_forbidden  # noqa: E402

PUAN = KOK / "data/expert_sample/uzman-puanlari.json"
SURUM = {"v2": KOK / "data/judged/expert-70.v2.jsonl",
         "v3": KOK / "data/judged/expert-70.v3.jsonl",
         "v4": KOK / "data/judged/expert-70.v4.jsonl"}
CIKTI = KOK / "reports/analiz/2026-09-14-judge-v4-uc-boyut.md"
if len(sys.argv) == 3:
    SURUM["v4"], CIKTI = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])

# boyut -> (judge alanı, uzman alanı, kollar)
BOYUTLAR = {
    "anlasilirlik": ("anlasilirlik", "dil_butunlugu",
                     [("v2", "anlasilirlik"), ("v3", "anlasilirlik"),
                      ("v4", "anlasilirlik"), ("v4", "anlasilirlik_holistik")]),
    "dogallik": ("dogallik", "kisalik_dogallik",
                 [("v2", "dogallik"), ("v3", "dogallik"),
                  ("v4", "dogallik"), ("v4", "dogallik_holistik")]),
    "mi_uyumu": ("mi_uyumu", "mi_uyumu",
                 [("v2", "mi_uyumu"), ("v3", "mi_uyumu"),
                  ("v4", "mi_uyumu"), ("v4", "mi_uyumu_holistik")]),
}

SIZ = re.compile(r"\b(siz|size|sizi|sizin|sizde|sizden)\b|s[ıiuü]n[ıiuü]z\b", re.IGNORECASE)


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def yol(p):
    try: return str(p.relative_to(KOK))
    except ValueError: return str(p)


def auc(dusuk, yuksek):
    if not dusuk or not yuksek:
        return None
    return sum(1.0 if d < y else 0.5 if d == y else 0.0
               for d in dusuk for y in yuksek) / (len(dusuk) * len(yuksek))


def auc_se(a, n1, n2):
    if a is None or n1 < 2 or n2 < 2:
        return None
    q1, q2 = a / (2 - a), 2 * a * a / (1 + a)
    var = (a*(1-a) + (n1-1)*(q1-a*a) + (n2-1)*(q2-a*a)) / (n1*n2)
    return var ** 0.5 if var > 0 else None


def aralik(a, n1, n2):
    se = auc_se(a, n1, n2)
    return "—" if (a is None or se is None) else f"{max(0,a-1.96*se):.2f} – {min(1,a+1.96*se):.2f}"


def pearson(a, b):
    if len(a) < 3: return None
    ma, mb = statistics.mean(a), statistics.mean(b)
    payda = (sum((x-ma)**2 for x in a) * sum((y-mb)**2 for y in b)) ** 0.5
    return sum((x-ma)*(y-mb) for x, y in zip(a, b)) / payda if payda else None


def oku(p):
    return {json.loads(s)["id"]: json.loads(s) for s in p.read_text().splitlines() if s.strip()}


veri = {k: oku(v) for k, v in SURUM.items()}
kayitlar = oku(KOK / "data/candidates/expert-70.jsonl")
ad, icerik = next(iter(json.loads(PUAN.read_text())["uzmanlar"].items()))
puanlar = icerik["puanlar"]


def j(surum, kid):
    return (veri[surum].get(kid, {}).get("judge")) or {}


esli = [(int(no), up, up["kayit_id"]) for no, up in sorted(puanlar.items(), key=lambda x: int(x[0]))
        if all(j(s, up["kayit_id"]) for s in SURUM)]
v4_hepsi = [r for r in veri["v4"].values() if r.get("judge")]

L = ["# Judge v4 — kanıt → puan deseni üç boyutta", "",
     f"**Betik:** `scripts/analiz/{pathlib.Path(__file__).name}` · **Tarih:** 2026-09-14  "]
for k, p in SURUM.items():
    L.append(f"**{k}:** `{yol(p)}` · SHA256 `{sha(p)}`  ")
L += [f"**Uzman:** `{yol(PUAN)}` · SHA256 `{sha(PUAN)}`  ",
      f"**Üç sürümde de puanlanan ve uzmanın değerlendirdiği kayıt:** {len(esli)}", "",
      "> **Hipotez (K59'un devamı):** `anlasilirlik`'te işe yarayan ayrıştırma deseni "
      "`dogallik` ve `mi_uyumu`'nda da ayrım kazandırır.", "",
      "> **Protokol düzeltmesi:** v3'te holistik puan sorulardan **sonra** isteniyordu, "
      "yani kontrol kirliydi. v4'te holistik puanlar **en başta** isteniyor — bu tablodaki "
      "holistik kol artık gerçek bir taban. ⚠️ Karşılığında ters yönde bir risk doğuyor: "
      "önce verilen holistik puan, sonraki ikili cevapları çıpalayabilir.", "",
      "> ⚠️ **Kalibrasyon testi, genelleme testi değil.** Taksonomiler projenin kendi "
      "kaynaklarından (§C.3 OARS, §C.5 TIP 35, K20 ifade bankası, K48 register bulgusu) "
      "geliyor ama test aynı korpusta, aynı tek uzmana karşı yapılıyor.", "", "---", ""]

# ── 1. Bayraklar ──────────────────────────────────────────────────────────
L += ["## 1. Bayraklar ateşledi mi", ""]
for baslik, grup in [("Anlaşılırlık (B3)", ANLASILIRLIK_BAYRAKLARI),
                     ("Doğallık (C) ⭐", DOGALLIK_BAYRAKLARI),
                     ("OARS becerisi (D1) ⭐", OARS_BECERILERI),
                     ("TIP 35 tuzağı (D2) ⭐", tuple(TUZAKLAR))]:
    L += [f"### {baslik}", "", "| Alan | `true` | Oran |", "|---|---:|---:|"]
    for b in grup:
        n = sum(1 for r in v4_hepsi if r["judge"].get(b) is True)
        L.append(f"| `{b}` | {n}/{len(v4_hepsi)} | %{100*n/len(v4_hepsi):.0f} |")
    L += [""]
for ad_, grup in [("kusur", DOGALLIK_BAYRAKLARI), ("tuzak", tuple(TUZAKLAR)),
                  ("OARS becerisi", OARS_BECERILERI)]:
    c = collections.Counter(sum(1 for b in grup if r["judge"].get(b) is True) for r in v4_hepsi)
    L.append(f"**Kayıt başına {ad_} sayısı:** `{dict(sorted(c.items()))}`  ")
L += ["", f"⚠️ v2'de `tuzak_ihlali` **liste** olarak soruluyordu ve 70 kayıtta "
      f"yalnızca 2 kez doldu. İkili sorulara çevrilince: "
      f"{sum(1 for r in v4_hepsi if any(r['judge'].get(k) for k in TUZAKLAR))}/{len(v4_hepsi)} "
      "kayıtta en az bir tuzak. Aynı kusur, uzmanın 5. maddesinde de vardı (K58).", ""]

# ── 2. Dağılımlar + ayrım gücü, boyut boyut ───────────────────────────────
HEDEFLER = [("`ret` vs `kabul`", lambda u, a: u["genel_karar"] == "ret",
             lambda u, a: u["genel_karar"] == "kabul"),
            ("uzman ≤ 2 vs = 5", lambda u, a: (u.get(a) or 9) <= 2,
             lambda u, a: u.get(a) == 5)]

for boyut, (judge_alan, uzman_alan, kollar) in BOYUTLAR.items():
    L += [f"## 2.{list(BOYUTLAR).index(boyut)+1} `{boyut}`", "",
          "| Kol | n | Ort. | s | Dağılım |", "|---|---:|---:|---:|---|"]
    for surum, alan in kollar:
        d = [r["judge"][alan] for r in veri[surum].values()
             if r.get("judge") and r["judge"].get(alan) is not None]
        if not d:
            L.append(f"| {surum} · `{alan}` | 0 | — | — | _yok_ |"); continue
        L.append(f"| {surum} · `{alan}` | {len(d)} | {statistics.mean(d):.2f} | "
                 f"{statistics.pstdev(d):.2f} | `{dict(sorted(collections.Counter(d).items()))}` |")
    L += [""]

    # uzman tarafında varyans var mı
    ud = [up.get(uzman_alan) for _, up, _ in esli if up.get(uzman_alan) is not None]
    dag = dict(sorted(collections.Counter(ud).items()))
    L += [f"**Uzmanın `{uzman_alan}` dağılımı:** `{dag}` (n={len(ud)})", ""]
    if len(set(ud)) < 3 or sum(1 for x in ud if x <= 2) < 2:
        L += [f"> ⚠️ Uzman bu boyutta neredeyse hiç ayrım yapmamış — "
              f"*uzman ≤ 2 vs = 5* testi anlamsız. Yalnızca `ret` vs `kabul` raporlanıyor.", ""]

    for hedef_ad, kotu_f, iyi_f in HEDEFLER:
        kotu = [(no, up, kid) for no, up, kid in esli if kotu_f(up, uzman_alan)]
        iyi = [(no, up, kid) for no, up, kid in esli if iyi_f(up, uzman_alan)]
        if len(kotu) < 2 or len(iyi) < 2:
            continue
        L += [f"### {boyut} — {hedef_ad} · n = {len(kotu)} / {len(iyi)}", "",
              "| Kol | kötü ort. | iyi ort. | uyum oranı | %95 aralık |",
              "|---|---:|---:|---:|:---:|"]
        for surum, alan in kollar:
            dk = [j(surum, kid)[alan] for _, _, kid in kotu if j(surum, kid).get(alan) is not None]
            di = [j(surum, kid)[alan] for _, _, kid in iyi if j(surum, kid).get(alan) is not None]
            a = auc(dk, di)
            f = lambda x: "—" if not x else f"{statistics.mean(x):.2f}"
            im = "" if a is None else (" ✅" if a >= 0.75 else " ⚠️" if a >= 0.6 else " ❌")
            L.append(f"| {surum} · `{alan}` | {f(dk)} | {f(di)} | "
                     f"{'—' if a is None else f'{a:.2f}'}{im} | {aralik(a, len(dk), len(di))} |")
        L += [""]

    # korelasyon
    L += [f"**Uzmanın `{uzman_alan}` puanıyla korelasyon**", "", "| Kol | n | r |", "|---|---:|---:|"]
    for surum, alan in kollar:
        ua, ja = [], []
        for _, up, kid in esli:
            if up.get(uzman_alan) is not None and j(surum, kid).get(alan) is not None:
                ua.append(up[uzman_alan]); ja.append(j(surum, kid)[alan])
        r = pearson(ua, ja)
        L.append(f"| {surum} · `{alan}` | {len(ua)} | {'—' if r is None else f'{r:+.2f}'} |")
    L += ["", "> ✅ ≥ 0.75 · ⚠️ ≥ 0.60 · ❌ < 0.60 — bizim konvansiyonumuz (Kural 6).", ""]

# ── 3. Bayrak güvenilirliği — uzmandan bağımsız ───────────────────────────
L += ["## 3. Bayraklar güvenilir mi — deterministik çapraz kontrol ⭐", "",
      "İki bayrağın karşılığı kodla da bulunabiliyor. Bu, **uzmandan bağımsız** bir "
      "geçerlilik sınaması: judge'ın *evet/hayır* cevapları metinle uyuşuyor mu?", "",
      "| Bayrak | Deterministik kaynak | Uyum | Judge evet/kod hayır | Judge hayır/kod evet |",
      "|---|---|---:|---:|---:|"]
for bayrak, ad_kaynak, kod_f in [
        ("bos_guvence", "`configs/filters.yaml` yasak ifade listesi",
         lambda t: "bos_guvence" in scan_forbidden(t)),
        ("siz_kaymasi", "`siz`/`-sınız` regex'i", lambda t: bool(SIZ.search(t)))]:
    uyum = yp = yn = 0
    for r in v4_hepsi:
        metin = next(m["content"] for m in reversed(kayitlar[r["id"]]["messages"])
                     if m["role"] == "assistant")
        kod, llm_ = kod_f(metin), r["judge"].get(bayrak) is True
        if kod == llm_: uyum += 1
        elif llm_: yp += 1
        else: yn += 1
    L.append(f"| `{bayrak}` | {ad_kaynak} | {uyum}/{len(v4_hepsi)} "
             f"(%{100*uyum/len(v4_hepsi):.0f}) | {yp} | {yn} |")
L += ["", "> Kod da kusursuz değil (kelime taraması bağlam görmez, K40'ın dersi) — "
      "bu tablo **mutabakat** ölçer, doğruluk değil. Yüksek uyuşmazlık, ikili sorunun "
      "sanıldığı kadar nesnel olmadığını gösterir.", ""]

# ── 4. anlasilirlik tekrar üretildi mi ────────────────────────────────────
ayni_puan = sum(1 for _, _, kid in esli
                if j("v3", kid).get("anlasilirlik") == j("v4", kid).get("anlasilirlik"))
ayni_cumle = sum(1 for _, _, kid in esli
                 if (j("v3", kid).get("en_belirsiz_cumle") or "").strip()
                 == (j("v4", kid).get("en_belirsiz_cumle") or "").strip())
L += ["## 4. `anlasilirlik` tekrar üretildi mi", "",
      f"v3 ile v4 **aynı hesaplanan puanı** verdi: **{ayni_puan}/{len(esli)}**  ",
      f"v3 ile v4 **aynı cümleyi** seçti: **{ayni_cumle}/{len(esli)}**", "",
      "v4'te sorular aynı, ama holistik puan öne alındı ve iki yeni bölüm eklendi. "
      "Aynı kayıtta aynı puan çıkması mekanizmanın kararlı olduğunu gösterir; "
      "büyük fark çıkması çıpalama/bağlam etkisine işaret eder.", ""]

# ── 5. Alternatif formül — bayraklar duruyor, aritmetik değişirse ─────────
# MI'da tuzaklar (D2) neredeyse hiç ateşlemiyor ama OARS becerileri (D1) ateşliyor.
# Formülüm puanı TUZAKLARDAN türetiyordu; değişen sinyali kullanmıyordu.
# Bu, yeni LLM çağrısı GEREKTİRMEYEN bir yeniden hesap: aynı ikili cevaplar, başka formül.
#
# ⚠️ POST-HOC. Tek bir alternatif önceden belirlendi (beceri sayısına dayalı) ve
# yalnızca o raporlanıyor. n=5'te birden çok formül deneyip en iyisini seçmek
# aşırı uydurma olurdu; bu yüzden burada TEK formül var ve keşifsel etiketli.
def mi_alternatif(jd):
    beceri = sum(1 for k in OARS_BECERILERI if jd.get(k) is True)
    tuzak = sum(1 for k in TUZAKLAR if jd.get(k) is True)
    return max(1, min(5, 1 + beceri - tuzak))


L += ["## 5. Alternatif MI formülü — keşifsel", "",
      "MI'da **tuzaklar ateşlemiyor** (1/68) ama **OARS becerileri ateşliyor** "
      "(yansıtma %87 · karmaşık %68 · takdir %15 · özet %7 · özerklik %10). "
      "Formülüm puanı tuzaklardan türetiyordu, yani veride **duran sinyali "
      "kullanmıyordu**. Aynı ikili cevaplarla, yeni çağrı yapmadan başka bir "
      "formül denenebilir:", "",
      "```", "mi_alternatif = 1 + (OARS becerisi sayısı) − (tuzak sayısı),  1-5 arası",
      "```", "",
      "⚠️ **Post-hoc ve keşifseldir.** Tek bir alternatif önceden belirlendi ve "
      "yalnızca o raporlanıyor; n=5'te birkaç formül deneyip en iyisini seçmek "
      "aşırı uydurma olurdu. Buradaki sayı **hipotez üretir, doğrulamaz** — "
      "doğrulaması yeni bir korpus ve yeni bir uzman turu gerektirir.", ""]

kotu = [(no, up, kid) for no, up, kid in esli if up["genel_karar"] == "ret"]
iyi = [(no, up, kid) for no, up, kid in esli if up["genel_karar"] == "kabul"]
dk = [mi_alternatif(j("v4", kid)) for _, _, kid in kotu]
di = [mi_alternatif(j("v4", kid)) for _, _, kid in iyi]
a_alt = auc(dk, di)
dag_alt = collections.Counter(mi_alternatif(r["judge"]) for r in v4_hepsi)
L += ["| Formül | Dağılım (68 kayıt) | s | ret ort. | kabul ort. | uyum oranı | %95 aralık |",
      "|---|---|---:|---:|---:|---:|:---:|"]
d_mev = [r["judge"]["mi_uyumu"] for r in v4_hepsi if r["judge"].get("mi_uyumu") is not None]
dk_m = [j("v4", kid)["mi_uyumu"] for _, _, kid in kotu if j("v4", kid).get("mi_uyumu") is not None]
di_m = [j("v4", kid)["mi_uyumu"] for _, _, kid in iyi if j("v4", kid).get("mi_uyumu") is not None]
a_mev = auc(dk_m, di_m)
L += [f"| mevcut (5 − tuzak) | `{dict(sorted(collections.Counter(d_mev).items()))}` | "
      f"{statistics.pstdev(d_mev):.2f} | {statistics.mean(dk_m):.2f} | "
      f"{statistics.mean(di_m):.2f} | {a_mev:.2f} | {aralik(a_mev, len(dk_m), len(di_m))} |",
      f"| **alternatif (1 + beceri − tuzak)** | `{dict(sorted(dag_alt.items()))}` | "
      f"{statistics.pstdev([mi_alternatif(r['judge']) for r in v4_hepsi]):.2f} | "
      f"{statistics.mean(dk):.2f} | {statistics.mean(di):.2f} | **{a_alt:.2f}** | "
      f"{aralik(a_alt, len(dk), len(di))} |", ""]

# ── 6. Sonuç ──────────────────────────────────────────────────────────────
L += ["## 6. Sonuç", "", "### `anlasilirlik` — tekrar üretildi, kontrol artık temiz", "",
      "v3'ün sonucu v4'te tekrarlandı (uyum oranı 0.87 → 0.81; aynı cümle 45/48). "
      "Asıl kazanç şu: **K59'da zayıf diye işaretlediğim kontrol artık temiz.** "
      "v3'te holistik puan sorulardan sonra isteniyordu ve 0.82 çıkıyordu; v4'te "
      "sorulardan **önce** isteniyor ve **0.57**'ye düşüyor — v2'nin 0.53'ü ile aynı yerde.", "",
      "| Kol | Uyum oranı |", "|---|---:|",
      "| v2 — soru yok, puanı LLM verdi | 0.53 |",
      "| v4 holistik — soru **öncesi**, puanı LLM verdi | 0.57 |",
      "| v3 holistik — soru **sonrası**, puanı LLM verdi | 0.82 |",
      "| v3 / v4 hesaplanan — sorulardan kod hesapladı | 0.87 / 0.81 |", "",
      "**Okuma:** yardımsız bir LLM'den alınan bütünsel puan ölçmüyor (0.53-0.57). "
      "Somut ikili sorular sorulduğunda, LLM'in **kendi** puanı bile düzeliyor (0.82). "
      "Yani aktif madde **ayrıştırma**; puanı koddan hesaplamak onun üstüne küçük bir "
      "katkı ve bir **garanti** koyuyor (kod, gördüğü kusuru saymak zorunda). "
      "K59'un yönü doğruydu, v4 onu temiz kontrolle **doğruluyor**.", "",
      "### `dogallik` — başarısız, hem de daha kötüsü", "",
      "Bayraklar ateşlemedi (en yüksek %3), puan 66/68 kayıtta 5, s=0.17, uyum oranı "
      "**0.48**. Ayrıştırma bu boyutu **iyileştirmedi, bozdu**: v3'ün LLM'den gelen "
      "`dogallik`'i 0.67 ile daha iyiydi.", "",
      "Sebep `reports/analiz/2026-09-14-gosterge-secimi.md`'de, judge'a bakmadan "
      "gösterildi: seçtiğim beş göstergenin **hepsi korpusta yok** — üçü zaten "
      "`configs/filters.yaml` kapısında eleniyor, kod da 0/70 buluyor. "
      "Üstelik uzman `dil_butunlugu` ile `kisalik_dogallik`'i **r = +0.97** ile "
      "doldurmuş (43/46 kayıtta birebir aynı puan): bu korpusta doğallık ayrı bir "
      "boyut değil. **Var olmayan bir ayrım arandı.**", "",
      "### `mi_uyumu` — başarısız, ölçüt de yok", "",
      "Tuzaklar 1/68 ateşledi, puan 61/68 kayıtta 5, uyum oranı 0.41 — dört sürümün "
      "dördü de 0.50'nin **altında**. Ama burada bir de **ölçüt sorunu** var: uzman bu "
      "maddeyi 50 kaydın 18'inde doldurmuş ve 16'sına 5 vermiş. Yani MI uyumunda "
      "karşılaştırılacak bir insan yargısı pratikte **yok**; boyutun başarısız olduğunu "
      "bile kesin söyleyemeyiz.", "",
      "OARS becerileri (D1) ise **ateşliyor** ve formülüm o sinyali kullanmıyordu — "
      "ama §5'teki keşifsel yeniden hesap bunu da kapatıyor: beceri sayısına dayalı "
      "alternatif formül varyansı 0.36'dan 0.86'ya çıkarıyor, **uyum oranını ise "
      "değiştirmiyor (0.41 → 0.42)**. Yani sorun formül değil; bu ikili cevaplar "
      "uzmanın kararını basitçe **öngörmüyor**.", "",
      "### Genel ders", "",
      "**Ayrıştırma her boyutta işe yaramaz; işe yaraması için üç şart var:**",
      "1. Ayrıştırılan özellik korpusta **değişmeli** (doğallık: değişmiyordu).",
      "2. Gösterge, üretim kapısının **zaten elemediği** bir kusur olmalı "
      "(doğallık bayraklarının üçü kapının kopyasıydı).",
      "3. Karşılaştırılacak insan yargısında **varyans olmalı** "
      "(MI: uzmanın 18 puanının 16'sı 5).", "",
      "`anlasilirlik` üçünü de sağlıyordu — bu yüzden çalıştı.", ""]

CIKTI.write_text("\n".join(L) + "\n")
print(f"yazıldı: {CIKTI}  (eşleşen {len(esli)} · v4 judge {len(v4_hepsi)})")
