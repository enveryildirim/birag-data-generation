#!/usr/bin/env python3
"""Puanı ne açıklıyor — kapasite mi, güncellemenin GERÇEK büyüklüğü mü.

⛔ T185 h7'nin (24 kat·q+o·r16) neden yüksek olduğunu ayıramadı: `h6 → h7` tek
yapılandırma farkı `rank` ama `mlx_lm/tuner/lora.py:98` `self.scale * z` uyguluyor
ve `scale` rank'e bölünmüyor ⇒ rank'i katlamak etkin adımı da katlıyor.
`h8` (`rank 16` + `scale 10`) koşuldu ve **arada** kaldı (dereceli 4,00; h6 1,33,
h7 7,33), ikisinden de ayırt edilemedi — yapılandırma knob'larıyla bu soru n=3'te
ayrılmıyor.

⭐⭐ **Başka bir yol var: knob'u tartışmak yerine SONUCU ölçmek.** `lora.py:52`
güncellemeyi `(scale · lora_b.T) @ lora_a.T` diye kuruyor ⇒ her kolun ağırlıklara
gerçekte ne kadar dokunduğu **adaptör dosyasından doğrudan hesaplanabilir**.
Eğitim gerekmez, GPU-saat gerekmez; 24 adaptör zaten diskte (Kural 7).

➡️ *Bir yapılandırma alanının ne yaptığını tartışmak yerine, o alanın ÜRETTİĞİ
niceliği ölçmek mümkünse ölçülmelidir. `rank` ile `scale` iç içe; `‖ΔW‖` değil.*

İki nicelik ayrı tutulur:
  · **toplam enerji**  = sqrt(Σ‖ΔW_m‖²_F) — müdahalenin tamamı (kaç modül × ne kadar)
  · **modül başına**   = ortalama ‖ΔW_m‖_F — tek bir yerdeki adım büyüklüğü

Girdi : runs/*/adapters/adapters.safetensors · reports/analiz/eksen-kosu/*/sonuclar.jsonl
Çıktı : reports/analiz/2026-09-20-guncelleme-buyuklugu.{md,json}
"""
from __future__ import annotations

import importlib.util as iu
import json
import math
import statistics as st
from pathlib import Path

import mlx.core as mx
import yaml

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
EK = KOK / "reports/analiz/eksen-kosu"
TOHUM = (7, 13, 23)

_gs = iu.spec_from_file_location(
    "g", KOK / "scripts/analiz/2026-09-17-yonlendirme-derecelendirme.py")
G = iu.module_from_spec(_gs)
_gs.loader.exec_module(G)

# kol -> (tarif, koşu dizini kalıbı, eval etiketi kalıbı)  {t} = tohum
KOL = {
    "h1": ("8 kat · q · r8 · s20", "j-v014-k8|k-v014-k8-t13|l-v014-k8-t23",
           "j-safety_crisis-v014-k8|k-v014-k8-t13-safety|l-v014-k8-t23-safety"),
    "h2": ("16 kat · q · r8 · s20", "x-h2-v014-t{t}", "x-h2-v014-t{t}-safety"),
    "h3": ("24 kat · q · r8 · s20", "x-h3-v014-t{t}", "x-h3-v014-t{t}-safety"),
    "h4": ("32 kat · q · r8 · s20", "x-h4-v014-t{t}", "x-h4-v014-t{t}-safety"),
    "h5": ("16 kat · q+o · r8 · s20", "x-h5-v014-t{t}", "x-h5-v014-t{t}-safety"),
    "h6": ("24 kat · q+o · r8 · s20", "x-h6-v014-t{t}", "x-h6-v014-t{t}-safety"),
    "h7": ("24 kat · q+o · r16 · s20", "m-v014-k24qo-t7|n-v014-k24qo-t13|o-v014-k24qo-t23",
           "m-v014-k24qo-t7-safety|n-v014-k24qo-t13-safety|o-v014-k24qo-t23-safety"),
    "h8": ("24 kat · q+o · r16 · **s10**", "y-h8-r16s10-v014-t{t}",
           "y-h8-r16s10-v014-t{t}-safety"),
}


def _kaliplar(k: str):
    return k.split("|") if "|" in k else [k.format(t=t) for t in TOHUM]


def _kosu(parca):
    d = sorted(KOK.glob(f"runs/*-{parca}"))
    return d[-1] if d else None


def _norm(kosu: Path):
    """⭐ Gerçek güncelleme: lora.py:52 ile BİREBİR aynı ifade."""
    cfg = yaml.safe_load((kosu / "config.yaml").read_text(encoding="utf-8"))
    scale = float(cfg["mlx"]["lora_parameters"]["scale"])
    w = mx.load(str(kosu / "adapters" / "adapters.safetensors"))
    normlar = []
    for k in w:
        if not k.endswith(".lora_a"):
            continue
        b = w[k[:-len("lora_a")] + "lora_b"]
        delta = (scale * b.T) @ w[k].T
        normlar.append(float(mx.sqrt(mx.sum(delta * delta)).item()))
    return {"modul": len(normlar),
            "toplam": math.sqrt(sum(n * n for n in normlar)),
            "modul_basina": st.mean(normlar), "scale": scale}


def _rows(et):
    d = [p for p in EK.iterdir() if p.name.endswith(et)]
    return None if not d else [json.loads(s) for s in
        (sorted(d)[-1] / "sonuclar.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]


def main() -> int:
    kabul = G._kabul()
    kriz = {r["id"] for r in _rows("j-safety_crisis-v014-k8") if r.get("kutup") == "kriz"}
    veri = {}
    for kol, (tarif, kosu_k, eval_k) in KOL.items():
        kosular = [_kosu(p) for p in _kaliplar(kosu_k)]
        assert all(kosular), f"⛔ {kol}: eksik koşu {[p for p, k in zip(_kaliplar(kosu_k), kosular) if not k]}"
        n = [_norm(k) for k in kosular]
        d = [sum(G.derece(r["cevap"], kabul) for r in _rows(e) if r["id"] in kriz)
             for e in _kaliplar(eval_k)]
        veri[kol] = {"tarif": tarif, "modul": n[0]["modul"], "scale": n[0]["scale"],
                     "toplam": st.mean(x["toplam"] for x in n),
                     "modul_basina": st.mean(x["modul_basina"] for x in n),
                     "dereceli": st.mean(d), "dereceli_v": d}

    def kor(xa, ya):
        mx_, my = st.mean(xa), st.mean(ya)
        pay = sum((x - mx_) * (y - my) for x, y in zip(xa, ya))
        pd = math.sqrt(sum((x - mx_) ** 2 for x in xa) * sum((y - my) ** 2 for y in ya))
        return pay / pd if pd else 0.0

    kols = list(veri)
    r_top = kor([veri[k]["toplam"] for k in kols], [veri[k]["dereceli"] for k in kols])
    r_mod = kor([veri[k]["modul_basina"] for k in kols], [veri[k]["dereceli"] for k in kols])
    r_say = kor([veri[k]["modul"] for k in kols], [veri[k]["dereceli"] for k in kols])

    sat = ["# Puanı ne açıklıyor — kapasite mi, güncellemenin gerçek büyüklüğü mü", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           "**Kaynak:** 24 adaptör (8 kol × 3 tohum), `runs/*/adapters/adapters.safetensors`  ",
           "**Güncelleme:** `(scale · lora_b.T) @ lora_a.T` — `mlx_lm/tuner/lora.py:52` ile "
           "birebir aynı ifade", "",
           "⭐⭐ Yapılandırma alanlarını (`rank`, `scale`) tartışmak yerine, onların "
           "**ürettiği niceliği** ölçüyoruz: ağırlıklara gerçekte ne kadar dokunulduğu. "
           "`rank` ile `scale` iç içe; `‖ΔW‖` değil.", "",
           "## 1. ⭐⭐⭐ Kollar, güncelleme büyüklükleri ve dereceli puan", "",
           "| kol | kapsam | modül | ‖ΔW‖ toplam | modül başına | **dereceli** |",
           "|---|---|---:|---:|---:|---:|"]
    for k in sorted(kols, key=lambda x: -veri[x]["dereceli"]):
        v = veri[k]
        sat.append(f"| **{k}** | {v['tarif']} | {v['modul']} | {v['toplam']:.1f} | "
                   f"{v['modul_basina']:.2f} | **{v['dereceli']:.2f}** |")
    sat += ["",
            "| ilişki | Pearson r |", "|---|---:|",
            f"| ‖ΔW‖ **toplam** ↔ dereceli puan | **{r_top:+.2f}** |",
            f"| ‖ΔW‖ **modül başına** ↔ dereceli puan | **{r_mod:+.2f}** |",
            f"| **modül sayısı** ↔ dereceli puan | **{r_say:+.2f}** |", "",
            (f"⭐⭐⭐ **Puanı en iyi açıklayan şey güncellemenin TOPLAM büyüklüğü** "
             f"(r = {r_top:+.2f}): ağırlıklara ne kadar az dokunulursa kriz davranışı o "
             "kadar korunuyor. ➡️ *«Kapsam» diye tartıştığımız şey aslında bir vekil "
             "değişkendi; ölçülebilen nicelik `‖ΔW‖` ve merdivenin sıralaması onunla "
             "açıklanıyor.*"
             if abs(r_top) > max(abs(r_mod), abs(r_say)) and abs(r_top) > 0.7 else
             f"◐ **Tek bir nicelik puanı açıklamıyor** — toplam r={r_top:+.2f}, modül "
             f"başına r={r_mod:+.2f}, modül sayısı r={r_say:+.2f}. ➡️ *Bu, «kapasite mi "
             "adım mı» sorusunun yanlış kurulmuş olabileceğini düşündürür: iki nicelik de "
             "tek başına sıralamayı vermiyor.*"), "",
            "## 2. ⭐⭐⭐ Tasarlanmamış doğal deney — eşit enerji, farklı yayılım", "",
            "Toplam `‖ΔW‖` birbirine en yakın olup puanı en çok ayrılan çift aranır: "
            "toplam enerji eşitlenmişken geriye **yayılım** kalır.", ""]
    import itertools as _it
    en_iyi = None
    for a, b in _it.combinations(kols, 2):
        dt = abs(veri[a]["toplam"] - veri[b]["toplam"]) / max(veri[a]["toplam"], veri[b]["toplam"])
        dp = abs(veri[a]["dereceli"] - veri[b]["dereceli"])
        if dt <= 0.05 and (en_iyi is None or dp > en_iyi[2]):
            en_iyi = (a, b, dp)
    if en_iyi:
        a, b, _ = en_iyi
        if veri[a]["dereceli"] < veri[b]["dereceli"]:
            a, b = b, a
        sh = {k: st.stdev(veri[k]["dereceli_v"]) / math.sqrt(len(veri[k]["dereceli_v"]))
              for k in (a, b)}
        esik = 2 * math.sqrt(sh[a] ** 2 + sh[b] ** 2)
        f = veri[a]["dereceli"] - veri[b]["dereceli"]
        sat += ["| | " + a + " | " + b + " |", "|---|---:|---:|",
                f"| kapsam | {veri[a]['tarif']} | {veri[b]['tarif']} |",
                f"| ‖ΔW‖ **toplam** | {veri[a]['toplam']:.1f} | {veri[b]['toplam']:.1f} |",
                f"| dokunulan **modül** | {veri[a]['modul']} | {veri[b]['modul']} |",
                f"| **modül başına** | {veri[a]['modul_basina']:.2f} | "
                f"{veri[b]['modul_basina']:.2f} |",
                f"| **dereceli puan** | **{veri[a]['dereceli']:.2f}** | "
                f"**{veri[b]['dereceli']:.2f}** |", "",
                (f"⭐⭐⭐ **Toplam enerji neredeyse aynı ({veri[a]['toplam']:.1f} ↔ "
                 f"{veri[b]['toplam']:.1f}) ama puan {f:+.2f} ayrılıyor** (eşik {esik:.1f} ⇒ "
                 "**ayırt edilebiliyor**). Aradaki tek yapısal fark **yayılım**: "
                 f"{veri[a]['modul']} modül ↔ {veri[b]['modul']} modül. "
                 "➡️⭐⭐⭐ *Belirleyici olan ağırlıklara NE KADAR dokunulduğu değil, o "
                 "dokunuşun NEREYE YAYILDIĞI. Aynı enerjiyi az sayıda yere yoğunlaştırmak "
                 "kriz davranışını koruyor, çok sayıda yere dağıtmak bozuyor.*"
                 if abs(f) > esik else
                 f"◐ Toplam enerjisi eşit çift bulundu ({a} ↔ {b}) ama puan farkı "
                 f"({f:+.2f}) eşiğin ({esik:.1f}) altında ⇒ yayılım etkisi gösterilemedi."), "",
                "⛔ **Bu çift TASARLANMADI**, tabloda bulundu ⇒ seçim sonradan yapıldı "
                "(post-hoc). Hipotez olarak güçlü, kanıt olarak zayıf: doğrulamak için "
                "yayılımı ÖNCEDEN değiştiren bir kol koşulmalı (örneğin 8 kat · q+o · r16, "
                "aynı toplam enerji, iki katı modül) — koşulmadı.", ""]
    sat += ["## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **§2'nin çifti post-hoc seçildi** | tabloya bakıp en ayrık çift "
            "alındı; önceden ilan edilmiş bir karşılaştırma değil |",
            f"| ⛔⛔ **n={len(kols)} kol** | korelasyon sekiz noktadan; bir eğilim "
            "işareti, ölçülmüş bir yasa değil |",
            "| ⛔⛔ **Korelasyon nedensellik değil** | `‖ΔW‖` ile puan birlikte "
            "değişiyor; hangisinin ötekini ürettiği bu ölçümde YOK |",
            "| ⛔ **Frobenius normu bir seçim** | başka bir norm (spektral, katman "
            "bazında ağırlıklı) başka sıralama verebilir; seçim önceden ilan edildi |",
            "| ⛔ **Yalnız son kontrol noktası** | epok içi yörünge ölçülmedi |",
            "| ⚠️ **Dereceli ölçüt doğrulanmış değil** | anahtar sözcük listesi (T186) |", ""]

    (KOK / f"reports/analiz/{TARIH}-guncelleme-buyuklugu.json").write_text(
        json.dumps({"tarih": TARIH, "veri": veri,
                    "r_toplam": r_top, "r_modul_basina": r_mod, "r_modul_sayisi": r_say},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    (KOK / f"reports/analiz/{TARIH}-guncelleme-buyuklugu.md").write_text("\n".join(sat),
                                                                         encoding="utf-8")
    print("\n".join(sat[5:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
