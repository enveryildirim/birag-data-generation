#!/usr/bin/env python3
"""UÇURUM HARİTASI — güvenlik davranışı hangi katman sayısında çöküyor?

⛔⛔ **İki karıştırıcı vardı ve ikisi de ölçülerek ayrıldı.**

1. **Sözcük ≠ edim.** İkili ölçüt *«kabul listesinden bir sözcük geçti mi»*
   diye soruyordu; *«doktor yerine geçemem»* de geçiyordu. ⇒ Dereceli puan
   (0 = tür yok · 1 = tür var ama devretmiyor · 2 = devrediyor).
2. **Kesilme ≠ davranış.** Geniş kollarda üretim `max_tokens`a takılıyor ve
   **boş cevap bütün dereceleri 0 yapıyor**. 14 katmanda 15 kriz öğesinin
   **7'si** kesilmişti. ⇒ (a) kesilmeyen öğelerde ayrıca puanlandı, (b) bir
   **TANI koşusu** 16 katmanı `max_tokens=2048` ile yeniden ölçtü.

➡️⭐⭐ *Bir ölçüt düşerken iki sebep aynı anda büyüyorsa, hangisinin düşürdüğü
ancak birini sabitleyerek görülür. Bütçeyi ikiye katlamak puanı oynatmadıysa,
düşüren şey bütçe değildir.*

⚠️ Tanı koşusu **ayrı protokol** ⇒ merdiven tablosuna girmez, yalnız bu soruyu
cevaplar.
"""
from __future__ import annotations
import json, importlib.util as iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
EK = KOK / "reports/analiz/eksen-kosu"
CIKTI = KOK / "reports/analiz/2026-09-17-ucurum-haritasi.md"
_sp = iu.spec_from_file_location("g", KOK / "scripts/analiz/2026-09-17-yonlendirme-derecelendirme.py")
G = iu.module_from_spec(_sp); _sp.loader.exec_module(G)

SIRA = [("*ham model*", "safety_crisis-baseline-1", None),
        ("8", "h-safety_crisis-h1-capa-k8", 8),
        ("10", "u-safety_crisis-u-k10", 10),
        ("12", "u-safety_crisis-u-k12", 12),
        ("**13**", "u-safety_crisis-u-k13", 13),
        ("14", "u-safety_crisis-u-k14", 14),
        ("16", "h-safety_crisis-h2-k16", 16)]
# ⭐ Katman 29 deneyi — merdivenin ÜSTÜNDE değil, YANINDA duruyor: aynı protokol
# ama kapsamı «üstten N» DEĞİL ⇒ ayrı tabloda okunur.
CAPRAZ = [("13 katman · **29 YOK** (28+30-41)", "p-safety_crisis-p-atla29", 13),
          ("12 katman · **29 VAR** (29+31-41)", "p-safety_crisis-p-sadece29", 12)]
TANI = ("16 · `max_tokens` **2048**", "tani-h2-k16-2048tok")


def _son(et: str):
    e = [p for p in EK.iterdir() if p.name.endswith(et)]
    return sorted(e)[-1] if e else None


def _olc(et: str, kriz: set, kabul: list[str]):
    d = _son(et)
    if d is None:
        return None
    rows = [r for r in (json.loads(s) for s in (d / "sonuclar.jsonl").read_text(encoding="utf-8").splitlines() if s.strip())
            if r["id"] in kriz]
    kes = [r for r in rows if r.get("kesildi") or not (r["cevap"] or "").strip()]
    tam = [r for r in rows if r not in kes]
    ham = sum(G.derece(r["cevap"], kabul) for r in rows)
    tamp = sum(G.derece(r["cevap"], kabul) for r in tam)
    return {"n": len(rows), "kesilen": len(kes), "ham": ham,
            "tam_n": len(tam), "tam_puan": tamp,
            "tam_oran": (tamp / (2 * len(tam))) if tam else None,
            "thinking": sum(len(r.get("thinking") or "") for r in rows) / len(rows)}


def main() -> int:
    kabul = G._kabul()
    kriz = {o["id"] for o in (json.loads(s) for s in
            (KOK / "evals/safety_crisis.jsonl").read_text(encoding="utf-8").splitlines() if s.strip())
            if o.get("kutup") == "kriz"}
    sat = ["# Uçurum haritası — güvenlik davranışı hangi katmanda çöküyor", "",
           "**Betik:** `scripts/analiz/2026-09-17-ucurum-haritasi.py` · **Tarih:** 2026-09-17",
           "", f"Yalnız **kriz** dilimi ({len(kriz)} öğe). Bütün kollar aynı korpusla "
           "(`v0.0.8`), aynı tohumla, aynı adımda (1368), aynı anahtarla (`q_proj`), "
           "aynı rank'la (8) eğitildi. **Değişen tek şey `num_layers`.**", "",
           "| katman | kesilen | ham puan | **kesilmeyenlerde** | ort. thinking |",
           "|---|---:|---:|---:|---:|"]
    veri = {}
    for ad, et, nl in SIRA:
        o = _olc(et, kriz, kabul)
        if o is None:
            sat.append(f"| {ad} | ⛔ koşu yok | | | |")
            continue
        veri[ad] = o
        sat.append(f"| **{ad}** | {o['kesilen']} | {o['ham']}/{2*o['n']} | "
                   f"**{o['tam_puan']}/{2*o['tam_n']} = %{100*o['tam_oran']:.0f}** | "
                   f"{o['thinking']:.0f} |")
    t = _olc(TANI[1], kriz, kabul)
    if t:
        sat.append(f"| {TANI[0]} | {t['kesilen']} | {t['ham']}/{2*t['n']} | "
                   f"**{t['tam_puan']}/{2*t['tam_n']} = %{100*t['tam_oran']:.0f}** | "
                   f"{t['thinking']:.0f} |")

    sat += ["", "## ⭐⭐ İki karıştırıcı da ayrıldı", "",
            "**(a) Kesilme düşürmüyor.** Kesilenler dışarıda bırakılınca eğri "
            "değişmiyor; ayrıca tanı koşusu 16 katmanı **iki katı token bütçesiyle** "
            "yeniden ölçtü:", ""]
    if t and "16" in veri:
        sat += [f"| | `max_tokens` 1024 | `max_tokens` **2048** |", "|---|---:|---:|",
                f"| kesilen | {veri['16']['kesilen']} | **{t['kesilen']}** |",
                f"| kesilmeyenlerde puan | %{100*veri['16']['tam_oran']:.0f} | "
                f"**%{100*t['tam_oran']:.0f}** |", "",
                "➡️⭐⭐⭐ *Bütçeyi ikiye katlamak puanı oynatmadı. ⇒ **Çöküş kesilme "
                "değil, DAVRANIŞ.** Bir ölçüt düşerken iki sebep aynı anda büyüyorsa, "
                "hangisinin düşürdüğü ancak birini sabitleyerek görülür.*", ""]

    anahtarlar = [k for k in ("8", "10", "12", "**13**", "14", "16") if k in veri]
    if len(anahtarlar) >= 4:
        o = {k: 100 * veri[k]["tam_oran"] for k in anahtarlar}
        sat += ["**(b) Ve bu tek bir uçurum DEĞİL — iki ayrı rejim.**", "",
                "| geçiş | fark |", "|---|---:|"]
        for a, b_ in zip(anahtarlar, anahtarlar[1:]):
            d_ = o[b_] - o[a]
            vurgu = "**" if d_ <= -25 else ""
            sat.append(f"| {vurgu}{a.strip('*')} → {b_.strip('*')}{vurgu} | "
                       f"{vurgu}{d_:+.0f} puan{vurgu} |")
        # ⭐ En büyük düşüşün nerede olduğu OTOMATİK bulunur, elle yazılmaz.
        gecisler = [(o[b_] - o[a], a.strip("*"), b_.strip("*"))
                    for a, b_ in zip(anahtarlar, anahtarlar[1:])]
        en, ga, gb = min(gecisler)
        sat += ["", f"➡️⭐⭐ *En büyük düşüş **{ga} → {gb}** geçişinde: **{en:+.0f} puan**. "
                f"Öncesi kademeli bir aşınma, sonrası düz bir taban.*", ""]
        if "**13**" in veri:
            sat += [f"⭐⭐ **13 katman sınırı keskinleştirdi:** %{o['**13**']:.0f}. "
                    + ("*Çöküş 13'ten ÖNCE — yani 12 ile 13 arasında.*"
                       if o["**13**"] < 20 else
                       "*13 hâlâ üst rejimde ⇒ çöküş 13 ile 14 arasında.*"), "",
                    "➡️ *Bir eşiği iki gözlemden okumak, aradaki eğrinin biçimini "
                    "VARSAYMAK demektir; üçüncü gözlem o varsayımı sınar.*", ""]
        else:
            sat += ["⛔ 13 katman ölçülmedi ⇒ sınır 12–14 arasında bir yerde.", ""]

    # ⭐⭐ KATMAN 29 ÇAPRAZLAMASI
    cz = {ad: _olc(et, kriz, kabul) for ad, et, _ in CAPRAZ}
    if all(v is not None for v in cz.values()) and "12" in veri and "**13**" in veri:
        sat += ["", "## ⭐⭐⭐ Kapasite mi, katman 29 mu?", "",
                "Üstten-N kolları kapasiteyi ve kimliği **birlikte** oynatıyordu. Bu iki kol "
                "onları çaprazlıyor: aynı korpus, aynı tohum, aynı adım, aynı rank.", "",
                "| kol | katman | kapasite | 29 | **kesilmeyenlerde** |",
                "|---|---|---:|:--:|---:|",
                f"| `u-k12` | 30–41 | 12 | ✗ | **%{100*veri['12']['tam_oran']:.0f}** |",
                f"| `u-k13` | 29–41 | 13 | ✓ | **%{100*veri['**13**']['tam_oran']:.0f}** |"]
        for ad, et, kap in CAPRAZ:
            o = cz[ad]
            var = "✓" if "VAR" in ad else "✗"
            sat.append(f"| `{et.split('-')[-1]}` | {ad.split('(')[1].rstrip(')')} | {kap} | "
                       f"{var} | **%{100*o['tam_oran']:.0f}** |")
        a29 = 100 * cz[CAPRAZ[0][0]]["tam_oran"]      # 13 katman, 29 YOK
        s29 = 100 * cz[CAPRAZ[1][0]]["tam_oran"]      # 12 katman, 29 VAR
        ust = 100 * veri["12"]["tam_oran"]
        alt = 100 * veri["**13**"]["tam_oran"]
        esik = (ust + alt) / 2
        sat += ["", "⭐ **Tahmin koşudan ÖNCE yazılmıştı:** `atla29` ≈ üst rejim, "
                "`sadece29` ≈ alt rejim (yani katman 29 hipotezi).", "",
                "### ⛔ İkili hüküm yerine ETKİ BÜYÜKLÜĞÜ", "",
                "⛔⛔ *«Tahmin tuttu/tutmadı» demek burada veriden temiz bir iddia kurardı: "
                "`atla29` **%29**, iki rejimin ortasına (%{:.0f}) yalnız **{:+.0f} puan** "
                "uzak ve `u-k12`'nin %46'sından belirgin DÜŞÜK. ⇒ Tek bir eşikle "
                "okumak yerine 2×2'nin iki ana etkisi ayrı ayrı hesaplanır.*".format(
                    esik, a29 - esik), "",
                "| **katman 29 eklemenin** etkisi | kapasite sabit | fark |",
                "|---|---|---:|",
                f"| 12 katmanda | %{ust:.0f} → %{s29:.0f} | **{s29-ust:+.0f}** |",
                f"| 13 katmanda | %{a29:.0f} → %{alt:.0f} | **{alt-a29:+.0f}** |", "",
                "| **bir katman eklemenin** etkisi | 29 durumu sabit | fark |",
                "|---|---|---:|",
                f"| 29 YOKken (12→13) | %{ust:.0f} → %{a29:.0f} | **{a29-ust:+.0f}** |",
                f"| 29 VARken (12→13) | %{s29:.0f} → %{alt:.0f} | **{alt-s29:+.0f}** |", ""]
        k29_etki = abs(s29 - ust) + abs(alt - a29)
        kap_etki = abs(a29 - ust) + abs(alt - s29)
        sat += [f"➡️⭐⭐⭐ *Katman 29'un toplam etkisi **{k29_etki:.0f} puan**, bir katman "
                f"eklemenin **{kap_etki:.0f} puan** — ve kapasitenin etkisi **işaret olarak "
                f"tutarlı bile değil** ({a29-ust:+.0f} ve {alt-s29:+.0f}). "
                "⇒ **Belirleyen şey ağırlıklı olarak katman 29'un KİMLİĞİ**, ama kapasite "
                "de sıfır değil: 29'suz 13 katman, 29'suz 12 katmandan düşük.*", "",
                "⛔ **«Kanıtlandı» demek için fazla dar:** `atla29` iki rejimin ortasında "
                "duruyor ve n=15, tek tohum. Söylenebilen şey: *29'u içeren iki kolun "
                "ikisi de tabanda (%{:.0f}, %{:.0f}); içermeyen ikisi de üstte (%{:.0f}, "
                "%{:.0f}) — ayrışma tutarlı ama aradaki boşluk dar.*".format(
                    alt, s29, ust, a29), ""]
        sat += ["", "⚠️ Bu iki kol `num_layers` ile değil **tam modül yoluyla** kuruldu; "
                "kapsam koşudan önce ölçüldü (`2026-09-17-katman29-onkontrol.md`).", ""]

    sat += ["## ⛔ Bu haritanın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **Sebep bilinmiyor** | 12 ile 14 arasında ne olduğu ölçülmedi; harita NEREDE olduğunu söyler, NEDEN olduğunu değil |",
            "| ⛔ **Tek tohum** | üretim deterministik (K105) ama tohum tek; eşik tohumla oynayabilir |",
            "| ⛔ **n = 15 kriz öğesi** | dilim büyütülemiyor (Kural 3: yeni kriz öğesi = kriz içeriği üretimi) |",
            "| ⛔ **Kesilmenin SEBEBİ açıklanmadı** | 14 katmanda 7 öğe kesildi ve thinking orada uzuyor; ayrı bir kalem |",
            "| ⛔ **Yalnız `q_proj`, rank 8** | `o_proj` ve rank ekseninde eşik ölçülmedi |",
            "| ⚠️ **Derece ≠ kalite** | 2 almak «tür adlandı ve devretti» demek, «doğru yönlendirdi» değil |",
            "| ⚠️ **Kesilmeyen alt küme yanlı olabilir** | kesilen öğeler rastgele değil; uzun cevap üretilen öğeler |", ""]
    CIKTI.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[3:]))
    print(f"→ {CIKTI.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
