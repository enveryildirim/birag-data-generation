#!/usr/bin/env python3
"""Adımlı tazeleme kolu — unutma TAMAMEN geri alındı, ama kipe ÖZGÜ değil.

⛔ **Zincir.** T255 unutmanın iki kusurdan geldiğini ölçtü (aritmetik +
olgusal ad) ve iki aday sebep bıraktı: korpusun kipi hiç göstermemesi ↔ LoRA
kapsamı. T256 ilk ayırıcı kolu geçersiz kıldı: 40 yalın-cevap kaydı gradyanın
yalnız **%0,034'üydü**. Bu kol onarılmış tasarımdır: **%5,01 sinyal**, pay
koşudan ÖNCE ölçüldü.

⭐⭐⭐ **SONUÇ: ön kayıttaki İKİNCİ şık.** Hem tazelenen kip (aritmetik) hem
**tazelenMEYEN kontrol kipi** (olgusal ad) düzeldi ⇒ *«korpusta o kip yok, o
yüzden o kip bozuldu»* açıklaması **YETERSİZ**. Tazeleme kipe özgü bir onarım
değil, **genel** bir onarım yapıyor.

⭐⭐ Ve bedeli yok, tersine: terapötik güvenlik ekseni de **düzeldi**.

Çıktı: reports/analiz/2026-09-22-adimli-kol-sonuc.md
"""
from __future__ import annotations

import importlib.util as iu
import json
import math
import statistics as st
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-adimli-kol-sonuc.md"
EK = KOK / "reports/analiz/eksen-kosu"
T8 = (7, 13, 23, 31, 37, 41, 43, 47)
T3 = (7, 13, 23)
PAY = {"e1": 0.034, "e2": 5.01}          # kayıp sinyalindeki pay, ölçüldü

_g = iu.spec_from_file_location(
    "g", KOK / "scripts/analiz/2026-09-17-yonlendirme-derecelendirme.py")
G = iu.module_from_spec(_g)
_g.loader.exec_module(G)


def _rows(et):
    d = [p for p in EK.iterdir() if p.name.endswith(et)]
    return {r["id"]: r for r in (json.loads(s) for s in
            (sorted(d)[-1] / "sonuclar.jsonl").read_text(encoding="utf-8").splitlines()
            if s.strip())} if d else None


def _fark(a, b):
    f = st.mean(b) - st.mean(a)
    h = 2 * math.sqrt(st.stdev(a)**2 / len(a) + (st.stdev(b)**2 / len(b) if len(b) > 1 else 0))
    return f, h, abs(f) > h


def main() -> int:
    kabul = G._kabul()
    kriz = {i for i, r in _rows("j-safety_crisis-v014-k8").items()
            if r.get("kutup") == "kriz"}
    tb_f = _rows("-forgetting_smoke-baseline-1")
    tb_s = _rows("-safety_crisis-baseline-1")
    kol = {"d1": ("d1-veri2x-k8qo-v018", T8), "e1": ("e1-tazeleme-v019", T3),
           "e2": ("e2-adimli-v020", T3)}
    F, S, D = {}, {}, {}
    for k, (kok, TT) in kol.items():
        F[k] = [sum(1 for r in _rows(f"{kok}-t{t}-forget").values()
                    if r.get("otomatik_gecti")) for t in TT]
        S[k] = [sum(1 for r in _rows(f"{kok}-t{t}-safety").values()
                    if r.get("otomatik_gecti")) for t in TT]
        D[k] = [sum(G.derece(r["cevap"], kabul) for i, r in
                    _rows(f"{kok}-t{t}-safety").items() if i in kriz) for t in TT]

    KIP = {"fs-025": ("ARİTMETİK", "⭐ tazelendi"),
           "fs-013": ("ARİTMETİK", "⭐ tazelendi"),
           "fs-029": ("olgusal ad", "⛔ **KONTROL** — tazelenMEDİ"),
           "fs-009": ("liste/indeks", "⛔ **KONTROL** — tazelenMEDİ")}

    f_f, h_f, ok_f = _fark(F["d1"], F["e2"])
    f_s, h_s, ok_s = _fark(S["d1"], S["e2"])
    f_d, h_d, ok_d = _fark(D["d1"], D["e2"])
    tb_fv = sum(1 for r in tb_f.values() if r.get("otomatik_gecti"))
    tb_sv = sum(1 for r in tb_s.values() if r.get("otomatik_gecti"))
    tb_dv = sum(G.derece(r["cevap"], kabul) for i, r in tb_s.items() if i in kriz)

    sat = ["# Adımlı tazeleme kolu — unutma geri alındı, ama kipe özgü değil", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           "**Kollar:** `d1` tazelemesiz (8 tohum) · `e1` %0,034 sinyal "
           "(3 tohum) · **`e2` %5,01 sinyal, adımlı** (3 tohum)  ", "",
           "⛔ Ön kayıt (koşudan önce): *aritmetik düzelir/olgusal düzelmez* ⇒ "
           "kip yokluğu sebep · *ikisi de düzelir* ⇒ genel onarım · *ikisi de "
           "düzelmez* ⇒ LoRA kapsamı.", "",
           "## Öge öge", "",
           "| öge | taban | `d1` | `e1` | **`e2`** | kip |",
           "|---|---|---:|---:|---:|---|"]
    for i, (k, durum) in KIP.items():
        t = "✅" if tb_f[i].get("otomatik_gecti") else "❌"
        v = [sum(1 for x in TT if _rows(f"{kok}-t{x}-forget")[i].get("otomatik_gecti"))
             for kok, TT in (kol["d1"], kol["e1"], kol["e2"])]
        sat.append(f"| `{i}` | {t} | {v[0]}/8 | {v[1]}/3 | **{v[2]}/3** | {k} · {durum} |")

    sat += ["", "## ⭐⭐⭐ Unutma tamamen geri alındı", "",
            "| kol | sinyal payı | `forgetting_smoke` | tohumlar |",
            "|---|---:|---|---|",
            f"| taban | — | **{tb_fv}/30** | (tek koşu) |",
            f"| `d1` tazelemesiz | %0 | {st.mean(F['d1']):.2f} ± "
            f"{2*st.stdev(F['d1'])/math.sqrt(8):.2f} | {F['d1']} |",
            f"| `e1` yalın | %{PAY['e1']} | {st.mean(F['e1']):.2f} ± "
            f"{2*st.stdev(F['e1'])/math.sqrt(3):.2f} | {F['e1']} |",
            f"| ⭐ **`e2` adımlı** | **%{PAY['e2']}** | **{st.mean(F['e2']):.2f} ± "
            f"{2*st.stdev(F['e2'])/math.sqrt(3):.2f}** | {F['e2']} |", "",
            f"**`e2` − `d1` = {f_f:+.2f} ± {h_f:.2f}** ⇒ "
            f"{'⭐ **OKUNABİLİR**' if ok_f else '⛔ gürültüde'}. "
            f"⭐⭐ `e2` **tabanla aynı** ({tb_fv}/30) ve üç tohumun üçü de "
            "aynı sayıyı verdi (sd = 0).", "",
            "## ⛔⛔ Ama kipe ÖZGÜ değil — kontrol ögesi de düzeldi", "",
            "`fs-029` (*«Kürk Mantolu Madonna»nın yazarı*) **tazelenmedi**; "
            "tazeleme setinde tek bir olgu iddiası yok. Yine de 1/8 → **2/3**:", "",
            "| | cevap |", "|---|---|",
            "| `d1` | *«…yazarı **Enem Şişmanoğlu**'dur.»* ❌ |",
            "| ⭐ `e2` | *«…yazarı **Enem Şişmanoğlu** değildir. …yazarı "
            "**Sabahattin Ali**'dir.»* ✅ |", "",
            "⭐ Model «Enem» çekicisini hâlâ üretiyor ama artık **kendini "
            "düzeltiyor**. ➡️⭐⭐⭐ *Tazeleme, öğrettiği kipi değil **genel "
            "bozulmayı** onarıyor. ⇒ T255'nin «korpusta o kip yok, o yüzden o "
            "kip bozuldu» açıklaması YETERSİZ; ölçülen şey, dar dağılımlı bir "
            "ince ayarın genel yeteneği bozması ve YETERİ KADAR alan dışı "
            "sinyalin bunu geri alması.*", "",
            "## ⭐⭐ Bedeli yok — terapötik eksen de düzeldi", "",
            "| kol | `safety_crisis` otomatik | dereceli (kriz) |",
            "|---|---|---|",
            f"| taban | {tb_sv}/20 | {tb_dv}/30 |",
            f"| `d1` | {st.mean(S['d1']):.2f} | {st.mean(D['d1']):.2f} |",
            f"| ⭐ **`e2`** | **{st.mean(S['e2']):.2f}** | **{st.mean(D['e2']):.2f}** |", "",
            f"`e2` − `d1`: otomatik **{f_s:+.2f} ± {h_s:.2f}** "
            f"({'okunabilir' if ok_s else 'gürültüde'}) · dereceli "
            f"**{f_d:+.2f} ± {h_d:.2f}** ({'okunabilir' if ok_d else 'gürültüde'}).", "",
            f"⭐ Otomatik sayım tabanı da **aşıyor** ({st.mean(S['e2']):.2f} ↔ "
            f"{tb_sv}). ⛔ Dereceli puan hâlâ tabanın çok altında "
            f"({st.mean(D['e2']):.2f} ↔ {tb_dv}) — T247 duruyor: korpusta kriz "
            "kaydı yok, bu eksen o açığı kapatamaz.", "",
            "## ⛔ Bu sonucun söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **«Korpusa aritmetik ekleyelim» SONUCU DEĞİLDİR** | ölçülen "
            "şey mekanizma: dar dağılım bozuyor, alan dışı sinyal geri alıyor. "
            "Hangi içeriğin ekleneceği ayrı bir **ürün kararı**dır ve "
            "`v0.0.20`'nin **%25,9'u alan dışı** |",
            "| ⛔⛔ **LoRA kapsamı hipotezi hâlâ ayrılmadı** | tazeleme genel "
            "onarım yaptığına göre sebep *«dar dağılım»* olabilir; bunu "
            "kapsamdan ayıracak kol (daha dar/geniş LoRA) **koşulmadı** |",
            "| ⛔ **`e2` 3 tohum, `d1` 8** | asimetrik; `e2`'nin sd = 0 olması "
            "aralığı daraltıyor ama 3 gözlemden |",
            "| ⛔ **Bulaşma şerhi duruyor** | tazeleme, eval'in aritmetik "
            "ögeleriyle **aynı kipi** hedefliyor ⇒ aritmetik kazancı *«kip "
            "tazelemesi çalıştı»* diye okunur. ⭐ **Ama `fs-029` kazancı bu "
            "şerhin dışındadır** — o kip hiç tazelenmedi |",
            "| ⚠️ **Biçim uyumu tam değil** | `e2` `fs-025`'e adımlı cevap "
            "veriyor (*«sadece son sayıyı yaz»* denmesine rağmen); "
            "`uzunluk_maks`=150 sınırını aşmadığı için geçiyor, ama biçim "
            "kısıtına uyum **ölçülmedi** |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[sat.index("## ⭐⭐⭐ Unutma tamamen geri alındı"):]))
    print(f"\n→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
