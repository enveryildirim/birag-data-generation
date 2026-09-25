#!/usr/bin/env python3
"""`evre` çelişkisinin ÜÇÜNCÜ kaynağı — parti karışımı mı, başka bir şey mi?

⛔⛔ **T221'İN AÇIK BIRAKTIĞI SORU.** `evre` çelişkisi parti4'te %2, parti6'da
%17. T222 rejimin payını neredeyse sıfırladı (parti1 %14 ↔ parti3-6 %10), ama
partiler ARASINDAKİ sekiz kat fark açıklanmadan kaldı. T221'in şerhi
*«üçüncü bir kaynak var — hangi tohumların o partiye düştüğü — ve o
ölçülmedi»* diyordu. Bu betik onu ölçüyor.

⭐ **YÖNTEM: STANDARDİZASYON.** Çelişki oranı `evre` DEĞERİNE göre çok
değişiyor (aşağıda). Her partinin kendi karışımı farklıysa, oranlar karışım
yüzünden de ayrışır. Her parti için **beklenen** oran hesaplanıyor: korpus
genelindeki değer-başına oranlar, o partinin kendi karışımıyla ağırlıklanıyor.
Gözlenen ile beklenen arasındaki fark, karışımın AÇIKLAMADIĞI kısımdır.

⭐ **VE BİR BANT.** Sayılar küçük (parti başına 1-10 çelişki); farkın
gürültüden ayırt edilebilir olup olmadığı Monte Carlo ile ölçülüyor: her kayıt
kendi değerinin korpus oranıyla Bernoulli çekiliyor, B=10.000.

⛔ **HÜKÜMLER YENİDEN VERİLMİYOR (K97).** İki okuma betiğinden ÇAĞRILIYOR:
`2026-09-21-parti1-tohum-meta-kayit-uyumu.py` (T220/T222) ve
`2026-09-21-parti3-6-profil-evre-uyumu.py` (T221). Bu betik yalnız sayıyor.

⛔ **İÇ ÖRNEKLEM UYARISI:** değer-başına oranlar, ayrıştırılan verinin
kendisinden hesaplanıyor. Bağımsız bir doğrulama kümesi yok ve bu, beklenen
oranları gözlenene doğru çeker (fark olduğundan küçük görünür).

Çıktı: reports/analiz/2026-09-21-evre-celiskisi-kaynak-ayrimi.{md,json}
"""
from __future__ import annotations

import collections
import json
import random
import statistics as st
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-evre-celiskisi-kaynak-ayrimi.md"
JSON = KOK / f"reports/analiz/{TARIH}-evre-celiskisi-kaynak-ayrimi.json"
B = 10_000
TOHUM = 20260921

# ⛔ ELLE: her çelişkide metnin ÖNE ÇIKARDIĞI değer (T222'nin ilan ettiği kural
#    gereği bir çelişki ancak başka bir değer görünüyorsa sayılır — o değer bu).
GORULEN: dict[str, str] = {
 # ⛔ parti1'in hükümleri T224 onarımından sonra ÜÇÜNCÜ kez okundu; eski beş
 #    çelişki (#19 #27 #43 #48 #49) yanlış tohumlardan geliyordu ve düştü.
 "v6-parti1#9": "tolerans",        "v6-parti1#22": "inkar",
 "v6-parti1#38": "birakma_cabasi", "v6-parti1#39": "inkar",
 "v6-parti1#41": "inkar",
 "v6-parti3#12": "tolerans",       "v6-parti3#22": "merak_deneme",
 "v6-parti3#27": "birakma_cabasi", "v6-parti3#33": "birakma_cabasi",
 "v6-parti3#45": "tolerans",       "v6-parti3#46": "tolerans",
 "v6-parti3#56": "nuksetme",
 "v6-parti4#2": "birakma_cabasi",
 "v6-parti5#16": "tolerans",       "v6-parti5#18": "tolerans",
 "v6-parti5#28": "tolerans",       "v6-parti5#33": "tolerans",
 "v6-parti5#53": "birakma_cabasi",
 "v6-parti6#19": "tolerans",       "v6-parti6#21": "tolerans",
 "v6-parti6#30": "nuksetme",       "v6-parti6#35": "nuksetme",
 "v6-parti6#39": "birakma_cabasi", "v6-parti6#41": "tolerans",
 "v6-parti6#43": "tolerans",       "v6-parti6#56": "tolerans",
 "v6-parti6#57": "nuksetme",       "v6-parti6#60": "birakma_cabasi",
}


def _modul(ad: str, yol: str):
    sp = _iu.spec_from_file_location(ad, KOK / yol)
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def main() -> int:
    K = _modul("kriz", "scripts/analiz/2026-09-17-tohum-beyan-kriz-kapisi.py")
    P1 = _modul("p1", "scripts/analiz/2026-09-21-parti1-tohum-meta-kayit-uyumu.py")
    P36 = _modul("p36", "scripts/analiz/2026-09-21-parti3-6-profil-evre-uyumu.py")
    toh = K._tohumlar()

    hukum: dict[str, dict[int, str]] = {
        "v6-parti1": {s: h[P1.EKSEN.index("evre")] for s, h in P1.HUKUM.items()}}
    for p, h in P36.HUKUM.items():
        hukum[p] = {s: v[P36.EKSEN.index("evre")] for s, v in h.items()}

    kayit = []   # (parti, sira, evre, hukum)
    for parti, hh in hukum.items():
        plan = {json.loads(l)["sira"]: json.loads(l)
                for l in (KOK / f"data/plan/{parti}.jsonl").read_text(
                    encoding="utf-8").splitlines() if l.strip()}
        for s, v in hh.items():
            ev = (toh.get(plan[s]["seed_id"], {}).get("meta") or {}).get("evre")
            kayit.append((parti, s, ev, v))

    # ── değer başına oran ──
    deger = collections.defaultdict(lambda: [0, 0])   # [n, Ç]
    for _, _, ev, v in kayit:
        deger[ev][0] += 1
        deger[ev][1] += (v == "Ç")
    oran = {ev: c / n for ev, (n, c) in deger.items()}

    # ── parti: gözlenen, beklenen (standardizasyon), Monte Carlo bandı ──
    rng = random.Random(TOHUM)
    partiler = sorted(hukum)
    sonuc = {}
    for parti in partiler:
        alt = [k for k in kayit if k[0] == parti]
        n = len(alt)
        gozlenen = sum(1 for k in alt if k[3] == "Ç")
        beklenen = sum(oran[k[2]] for k in alt)
        sim = []
        for _ in range(B):
            sim.append(sum(1 for k in alt if rng.random() < oran[k[2]]))
        sim.sort()
        alt_b, ust_b = sim[int(0.025 * B)], sim[int(0.975 * B) - 1]
        sonuc[parti] = {"n": n, "gozlenen": gozlenen, "beklenen": round(beklenen, 1),
                        "bant": [alt_b, ust_b],
                        "disarida": not (alt_b <= gozlenen <= ust_b)}

    # ── karışım ne kadar açıklıyor: gözlenen ve beklenen oranların yayılımı ──
    g = [100 * sonuc[p]["gozlenen"] / sonuc[p]["n"] for p in partiler]
    b_ = [100 * sonuc[p]["beklenen"] / sonuc[p]["n"] for p in partiler]
    yay_g, yay_b = max(g) - min(g), max(b_) - min(b_)

    # ── yön: hangi etiket hangi değerle karışıyor ──
    karisim = collections.Counter()
    for parti, s, ev, v in kayit:
        if v == "Ç":
            karisim[(ev, GORULEN.get(f"{parti}#{s}", "⛔ YAZILMAMIŞ"))] += 1

    eksik = [f"{p}#{s}" for p, s, _, v in kayit
             if v == "Ç" and f"{p}#{s}" not in GORULEN]
    if eksik:
        print(f"⛔ Görülen değeri yazılmamış çelişki: {eksik}")
        return 1

    JSON.write_text(json.dumps(
        {"tarih": TARIH, "B": B, "oran": {k: round(v, 3) for k, v in oran.items()},
         "parti": sonuc, "karisim": {f"{a}→{b}": c for (a, b), c in karisim.items()}},
        ensure_ascii=False, indent=1), encoding="utf-8")

    sat = ["# `evre` çelişkisinin kaynağı — parti karışımı ne kadar açıklıyor?", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Girdi:** T220/T222/**T224** ve T221'in hükümleri (yeniden verilmedi, "
           f"çağrıldı) · **{len(kayit)}** kayıt · Monte Carlo **B={B:,}**", "",
           "⛔⛔ T221 sormuştu: rejim açıklamıyorsa (T222: parti1 %14 ↔ parti3-6 "
           "%10) partiler arasındaki sekiz kat farkı ne açıklıyor?", "",
           "## 0. ⭐⭐⭐ Sonuç", "",
           f"⛔⛔⛔ **ARADIĞIM ÜÇÜNCÜ KAYNAK İÇİN KANIT YOK.** Beş partinin "
           "beşi de %95 bandının İÇİNDE. T221'de *«rejim sabitken bile sekiz kat "
           "oynuyor, demek ki üçüncü bir kaynak var»* demiştim; o cümle bir "
           "ölçüme değil, bir orana bakmaya dayanıyordu. ➡️⭐⭐⭐ *Bir oran "
           "farkı, o farkın gürültüden ayırt edilebildiği gösterilmeden bir "
           "KAYNAĞA işaret etmez; «sekiz kat» ifadesi paydası 59 olan iki "
           "sayının (1 ve 10) arasındaki farkı büyütüyordu.*", "",
           f"⭐ **İki şey birlikte doğru.** (a) Çelişki oranı etiketin DEĞERİNE "
           f"göre dört kat değişiyor (`tolerans` %{100*oran['tolerans']:.0f} ↔ "
           f"`merak_deneme` %{100*oran['merak_deneme']:.0f}) ve partilerin "
           f"karışımları farklı ⇒ karışım gerçek bir etken. (b) Ama karışım "
           f"gözlenen {yay_g:.0f} puanlık yayılımın yalnız {yay_b:.0f} puanını "
           "üretiyor; **geri kalanı da örnekleme gürültüsünün içinde kalıyor.** "
           "Yani karışım farkı tek başına açıklamıyor, ama açıklanacak bir "
           "kalıntı olduğu da gösterilemiyor.", "",
           "| parti | kayıt | gözlenen Ç | karışımdan beklenen | %95 bant | bandın dışında mı |",
           "|---|---:|---:|---:|---|---|"]
    for p in partiler:
        d = sonuc[p]
        sat.append(f"| `{p}` | {d['n']} | **{d['gozlenen']}** (%"
                   f"{100*d['gozlenen']/d['n']:.0f}) | {d['beklenen']} (%"
                   f"{100*d['beklenen']/d['n']:.0f}) | {d['bant'][0]}–{d['bant'][1]} | "
                   + ("⛔ **EVET**" if d["disarida"] else "⭐ hayır") + " |")
    disari = [p for p in partiler if sonuc[p]["disarida"]]
    sat += ["", (f"⛔ **{len(disari)} parti bandın dışında:** "
                 + ", ".join(f"`{p}`" for p in disari) +
                 ". Bu partilerde karışım + gürültü yetmiyor; başka bir şey var."
                 if disari else
                 "⭐ **Hiçbir parti bandın dışında değil** — en uç olan "
                 f"`v6-parti4` ({sonuc['v6-parti4']['gozlenen']} gözlenen, bant "
                 f"{sonuc['v6-parti4']['bant'][0]}-{sonuc['v6-parti4']['bant'][1]}) "
                 "tam alt sınırda ve o bile içeride. ⛔ *«Bandın içinde»* demek "
                 "*«fark yok»* demek değil: bu veriyle fark GÖSTERİLEMİYOR "
                 "demek."), "",
           "## 1. Çelişki oranı — `evre` değerine göre", "",
           "| değer | kayıt | ⛔ çelişen | oran |", "|---|---:|---:|---:|"]
    for ev, (n, c) in sorted(deger.items(), key=lambda x: -x[1][1] / max(1, x[1][0])):
        sat.append(f"| `{ev}` | {n} | {c} | **%{100*c/n:.0f}** |")
    sat += ["", "## 2. ⭐⭐ Yön: hangi etiket hangi değerle karışıyor", "",
            "| etiket | metinde görülen | kaç kez |", "|---|---|---:|"]
    for (a, b2), c in karisim.most_common():
        sat.append(f"| `{a}` | `{b2}` | **{c}** |")
    en = collections.Counter(b2 for (_, b2), c in karisim.items() for _ in range(c))
    toplam_c = sum(karisim.values())
    sat += ["", f"⭐⭐ **Yön tek taraflı:** {toplam_c} çelişkinin "
            f"**{en['tolerans']}'inde** (%{100*en['tolerans']/toplam_c:.0f}) "
            "metinde görülen değer `tolerans`, yani süren bir durum; etiket ise "
            "bir hareket adı taşıyor. ⭐ Tersi seyrek: `tolerans` ETİKETİ "
            f"{deger['tolerans'][1]} kez çelişti ve en az hata veren iki "
            "değerden biri. "
            "➡️⭐⭐⭐ *Etiketler hareketi anlatıyor (deneme, çaba, nüks, dip), "
            "kayıtlar ise çoğu zaman SÜREN BİR DURUMU gösteriyor. Hata rastgele "
            "değil: hareket etiketleri, durağan metinlere yapıştırılıyor.*", "",
            "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **İÇ ÖRNEKLEM** | değer-başına oranlar, ayrıştırılan verinin "
            "kendisinden hesaplandı; bağımsız bir doğrulama kümesi yok ve bu, "
            "beklenen oranları gözlenene doğru çeker |",
            "| ⛔⛤ **Sayılar küçük** | parti başına 1-10 çelişki; bant bu yüzden "
            "geniş ve *«bandın içinde»* demek *«fark yok»* demek değil, "
            "*«bu veriyle fark gösterilemiyor»* demek |",
            "| ⛔ **Hükümler benim** (K30) ve `GORULEN` sütunu da benim; "
            "ikinci anotatör yok |",
            "| ⛔ **Tohum düzeyi ölçülemez** | her tohum bir kez kullanıldığı için "
            "tohum-başına oran tahmin edilemiyor; ölçülebilen en ince birim "
            "etiketin DEĞERİ |",
            "| ⚠️ **Düzeltme yapılmadı** | ne etiketler değişti ne kayıtlar |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print(f"✅ {len(kayit)} kayıt · gözlenen yayılım {yay_g:.0f} puan · "
          f"karışımdan beklenen {yay_b:.0f} puan")
    for p in partiler:
        d = sonuc[p]
        print(f"   {p}: gözlenen {d['gozlenen']} · beklenen {d['beklenen']} · "
              f"bant {d['bant'][0]}-{d['bant'][1]}" + ("  ⛔ DIŞARIDA" if d["disarida"] else ""))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
