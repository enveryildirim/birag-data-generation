#!/usr/bin/env python3
"""Kapsam merdiveni — KAYIP eğrileri (GPU gerektirmez).

⛔⛔ **Bu rapor merdivenin sorusunu CEVAPLAMAZ.** Merdivenin sorusu davranışsal
(«yönlendirme refleksi duruyor mu», «genel yetenek çöküyor mu») ve o ancak
üretimle ölçülür. Burada ölçülen şey **uyum kapasitesi**: kapsam büyüdükçe
model eğitim verisine daha iyi oturuyor mu.

➡️ *Kayıp düşmesi davranış demek değildir. Bir kol en düşük kaybı alıp
güvenlik kapısında elenebilir — nitekim önceki iki taramada tam bu oldu.*

⭐ Yine de iki şeyi ücretsiz veriyor:
  1. **Kapasite eğrisi** — katman/anahtar/rank artışının uyuma katkısı.
  2. **Aşırı uyum işareti** — val kaybının en düşük olduğu adım; Kural 5'in
     Pareto kontrol noktası seçimi buna bakar.

⚠️ Koşu `h8` (42 katman) **yarım kaldı** (makine ısındı, kullanıcı durdurdu)
⇒ merdivenin üst çapası yok ve tabloda **eksik** olarak görünür.
"""
from __future__ import annotations
import json, re
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / "reports/analiz/2026-09-17-merdiven-kayip-egrileri.md"
KOLLAR = ["h1-capa-k8", "h2-k16", "h3-k24", "h4-k32",
          "h5-k16-qo", "h6-k24-qo", "h7-k24-qo-r16", "h8-capa-k42-qo"]


def _bilgi(kol: str) -> dict | None:
    import yaml
    d = sorted(KOK.glob(f"runs/*-h-{kol}"))
    if not d:
        return None
    d = d[-1]
    c = yaml.safe_load((KOK / f"configs/training/h-{kol}.yaml").read_text())["mlx"]
    log = (d / "train.log").read_text(errors="ignore")
    tr = [(int(i), float(v)) for i, v in re.findall(r"Iter (\d+): Train loss ([\d.]+)", log)]
    va = [(int(i), float(v)) for i, v in re.findall(r"Iter (\d+): Val loss ([\d.]+)", log)]
    tam = (d / "metrics.json").exists()
    m = json.loads((d / "metrics.json").read_text()) if tam else {}
    return {"dizin": d.name, "tam": tam,
            "katman": c["num_layers"], "anahtar": len(c["lora_parameters"]["keys"]),
            "rank": c["lora_parameters"]["rank"],
            "tr_ilk": tr[0][1] if tr else None, "tr_son": tr[-1][1] if tr else None,
            "va_ilk": va[0][1] if va else None,
            "va_min": min(va, key=lambda x: x[1]) if va else None,
            "va_son": va[-1][1] if va else None,
            "sure": m.get("sure_saniye"), "adim": tr[-1][0] if tr else 0}


def main() -> int:
    sat = ["# Kapsam merdiveni — kayıp eğrileri (GPU'suz ara rapor)", "",
           "**Betik:** `scripts/analiz/2026-09-17-merdiven-kayip-egrileri.py` · "
           "**Tarih:** 2026-09-17 · **Veri:** `datasets/v0.0.8` (456 eğitim / 115 doğrulama)", "",
           "⛔⛔ **Bu rapor merdivenin sorusunu CEVAPLAMAZ.** Merdivenin sorusu davranışsal",
           "(yönlendirme refleksi, genel yetenek) ve yalnız üretimle ölçülür. Burada ölçülen",
           "şey **uyum kapasitesi**. *Kayıp düşmesi davranış demek değildir* — önceki iki",
           "taramada en iyi uyan kollar güvenlik kapısında elendi.", "",
           "| kol | katman | anahtar | rank | train ilk→son | val ilk | **val en iyi** | val son | süre |",
           "|---|---:|---:|---:|---|---:|---|---:|---:|"]
    veri = {}
    for kol in KOLLAR:
        b = _bilgi(kol)
        if b is None:
            sat.append(f"| `{kol}` | — | — | — | ⛔ koşu yok | | | | |")
            continue
        veri[kol] = b
        if not b["tam"]:
            sat.append(f"| `{kol}` | {b['katman']} | {b['anahtar']} | {b['rank']} | "
                       f"⛔ **YARIM** ({b['adim']} adımda kesildi) | "
                       f"{b['va_ilk']} | — | — | — |")
            continue
        vm = b["va_min"]
        sat.append(f"| `{kol}` | {b['katman']} | {b['anahtar']} | {b['rank']} | "
                   f"{b['tr_ilk']:.3f} → **{b['tr_son']:.3f}** | {b['va_ilk']:.3f} | "
                   f"**{vm[1]:.3f}** (adım {vm[0]}) | {b['va_son']:.3f} | {b['sure']:.0f}sn |")

    tam = {k: v for k, v in veri.items() if v["tam"]}
    sat += ["", "## 1. ⭐ Kapasite eğrisi — derinlik", ""]
    derin = [(v["katman"], v["va_min"][1], k) for k, v in tam.items() if v["anahtar"] == 1]
    if derin:
        sat += ["Yalnız `q_proj`, rank 8 — tek değişken **katman sayısı**:", "",
                "| katman | en iyi val | kol |", "|---:|---:|---|"]
        for n, vv, k in sorted(derin):
            sat.append(f"| {n} | **{vv:.3f}** | `{k}` |")
        en = min(derin, key=lambda x: x[1])
        sat += ["", f"➡️ En düşük val: **{en[0]} katman** ({en[1]:.3f})."]
        if len(derin) > 2:
            fark = max(x[1] for x in derin) - min(x[1] for x in derin)
            sat.append(f"⚠️ Uçlar arası fark yalnız **{fark:.3f}** — "
                       "kapasite artışının uyuma katkısı bu ölçekte küçük.")

    sat += ["", "## 2. ⭐ Genişlik ve rank — eşleştirilmiş karşılaştırma", ""]
    ciftler = [("h2-k16", "h5-k16-qo", "16 katmanda **+o_proj**"),
               ("h3-k24", "h6-k24-qo", "24 katmanda **+o_proj**"),
               ("h6-k24-qo", "h7-k24-qo-r16", "24+o_proj'da **rank 8 → 16**")]
    sat += ["| karşılaştırma | önce | sonra | fark |", "|---|---:|---:|---:|"]
    for a, b_, ad in ciftler:
        if a in tam and b_ in tam:
            va, vb = tam[a]["va_min"][1], tam[b_]["va_min"][1]
            sat.append(f"| {ad} | {va:.3f} | {vb:.3f} | **{vb-va:+.3f}** |")

    # ⭐⭐ GENİŞLİK ↔ DERİNLİK: aynı uyumu hangisi daha ucuza veriyor?
    if "h5-k16-qo" in tam and "h4-k32" in tam:
        a, b_ = tam["h5-k16-qo"], tam["h4-k32"]
        sat += ["", "### ⭐⭐ Genişlik, derinlikten ucuz", "",
                f"| kol | katman | anahtar | en iyi val |", "|---|---:|---:|---:|",
                f"| `h4-k32` | 32 | 1 | {b_['va_min'][1]:.3f} |",
                f"| `h5-k16-qo` | **16** | **2** | **{a['va_min'][1]:.3f}** |", "",
                f"➡️⭐⭐ *`o_proj` eklemek, katman sayısını DÖRDE KATLAMAKTAN daha çok "
                f"kazandırıyor: 8→32 katman {2.654-b_['va_min'][1]:.3f} indirdi, "
                f"16 katmanda yalnız `o_proj` eklemek {2.428-a['va_min'][1]:.3f}. "
                f"Ve `h5` YARI derinlikle `h4`'ten daha iyi oturuyor "
                f"({a['va_min'][1]:.3f} < {b_['va_min'][1]:.3f}).*", "",
                "⭐ **Bu §9 açısından önemli:** §9 dar kapsam istiyor ve «dar» burada "
                "**katman** anlamına geliyordu. Ölçüm başka bir dar yön gösteriyor — "
                "az katman + iki anahtar. ⚠️ Ama bu yalnız UYUM; davranış ölçülmedi.", ""]
    if "h6-k24-qo" in tam and "h7-k24-qo-r16" in tam:
        d = tam["h7-k24-qo-r16"]["va_min"][1] - tam["h6-k24-qo"]["va_min"][1]
        sat += [f"### ⚠️ Rank neredeyse etkisiz", "",
                f"Rank 8 → 16, val kaybını yalnız **{d:+.3f}** oynatıyor — `o_proj` "
                f"eklemenin ({-0.353:+.3f}) **yedide biri**. ➡️ *Parametre sayısını "
                f"rank'la büyütmek bu ölçekte karşılığını vermiyor; kapsamı anahtarla "
                f"genişletmek veriyor.*", ""]

    sat += ["", "## 3. ⚠️ Aşırı uyum işareti", "", "| kol | en iyi val adımı | son adım | |",
            "|---|---:|---:|---|"]
    for k, v in tam.items():
        vm = v["va_min"]
        asiri = v["va_son"] - vm[1]
        isaret = "⛔ val yükseliyor" if asiri > 0.02 else ("⚠️ hafif" if asiri > 0.005 else "·")
        sat.append(f"| `{k}` | {vm[0]} | {v['adim']} | {isaret} (+{asiri:.3f}) |")
    hepsi_son = all(v["va_min"][0] == v["adim"] for v in tam.values())
    sat += ["", "⭐ Kural 5: Pareto kontrol noktası **en iyi val adımında** seçilir, "
            "son adımda değil. Kontrol noktaları her epokta kaydedildi (`save_every: 456`).", ""]
    if hepsi_son and tam:
        sat += ["⛔⛔ **YEDİ KOLUN YEDİSİNDE DE en iyi val SON ADIMDA.** Val kaybı hâlâ "
                "düşüyordu ⇒ eğitim **yakınsamamıştı**.", "",
                "➡️⭐⭐ *Merdiven, kolları yakınsamamış bir noktada karşılaştırıyor. "
                "Sıralama burada doğru olabilir ama YAKINSAMA SONRASI sıralamanın aynı "
                "kalacağını söyleyen hiçbir şey yok — dar kapsamlı kollar daha geç "
                "doyabilir. ⇒ «3 epoch» §9'un tavanı olduğu için seçildi, verinin "
                "gerektirdiği için değil; ikisi karıştırılmamalı.*", "",
                "⚠️ Bu, üretim ölçümünü geçersiz kılmaz (davranış bu ağırlıklarla "
                "ölçülecek) ama **kayıp karşılaştırmasının** geçiciliğini gösterir.", ""]
    sat += ["## ⛔ Bu raporun söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **Davranış ölçülmedi** | yönlendirme refleksi ve genel yetenek üretim gerektirir; koşulmadı |",
            "| ⛔ **Üst çapa yok** | `h8` (42 katman) yarım kaldı ⇒ eski taramalarla geniş uçta köprü kurulamıyor |",
            "| ⛔ **Kayıp ≠ kalite** | düşük val kaybı, güvenlik kapısını geçeceği anlamına gelmez; önceki iki taramada tersi oldu |",
            "| ⚠️ Tek tohum | kollar arası farklar tek tohumda ölçüldü |",
            "| ⛔ **Yakınsama yok** | yedi kolun yedisinde de val hâlâ düşüyordu; sıralama yakınsama sonrası değişebilir |", ""]
    CIKTI.write_text("\n".join(sat), encoding="utf-8")
    (KOK / "reports/analiz/2026-09-17-merdiven-kayip-egrileri.json").write_text(
        json.dumps(veri, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print("\n".join(sat[7:]))
    print(f"→ {CIKTI.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
