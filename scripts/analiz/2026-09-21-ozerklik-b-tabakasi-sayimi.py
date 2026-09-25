#!/usr/bin/env python3
"""`ozerklik_vurgusu` — `B` tabakasının TAM SAYIMI (T230).

⛔⛔ **Bu tabaka ötekilerden farklı: ölçülen şey BENİM KENDİ HÜKÜMLERİM.**
`B` = desen görmedi, ben elle onayladım (T196'nın *«okuma kuyruğu»*
mekanizması). T228 bu tabakanın 20/65'ini okuyabilmiş ve onaylarımın
%85'inin tuttuğunu bulmuştu. Burada 65'in tamamı okunuyor.

⭐ **K30 açısından bu bir öz-denetim:** kayıtları ben yazdım, onayları ben
verdim, ve şimdi onayların ne kadarının tuttuğunu ölçüyorum. ⛔ Hakem yine
benim ⇒ ayrışan kayıtlarda kendi onayımı üçüncü kez değerlendiriyorum ve
bu bir bağımsızlık kusurudur, raporda duruyor.

⭐⭐ T228'de okunan 20 kayıt listeye karıştırıldı ve söylenmedi — T229'daki
gibi bir **gizli tekrar testi**. T229'da bu oran %100 çıkmıştı; ikinci bir
ölçüm, o sonucun tek seferlik olup olmadığını söyler.

Girdi : scratchpad/bs-{X,Y}.json + bs-anahtar.json (+ bs-hakem.json)
Çıktı : reports/analiz/2026-09-21-ozerklik-b-tabakasi-sayimi.md
"""
from __future__ import annotations

import json
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
# Girdi: depodaki kalıcı kopya — T227-T230'un kanıt tabanı
# (bkz. data/anotasyon/OKU.md).
SP = KOK / "data/anotasyon"
RAPOR = KOK / f"reports/analiz/{TARIH}-ozerklik-b-tabakasi-sayimi.md"


def _kappa(x, y):
    n = len(x)
    po = sum(a == b for a, b in zip(x, y)) / n
    pe = sum((x.count(s) / n) * (y.count(s) / n) for s in set(x) | set(y))
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def main() -> int:
    anah = json.loads((SP / "bs-anahtar.json").read_text(encoding="utf-8"))
    oy = {}
    for kod in ("X", "Y"):
        y = SP / f"bs-{kod}.json"
        if not y.exists():
            print(f"⛔ {y.name} yok — anotatör bitmedi.")
            return 1
        oy[kod] = {o["id"]: o["ozerklik"] for o in json.loads(y.read_text(encoding="utf-8"))}
        if set(anah) - set(oy[kod]):
            print(f"⛔ {kod} eksik: {sorted(set(anah) - set(oy[kod]))}")
            return 1

    idler = sorted(anah)
    ayri = [i for i in idler if oy["X"][i] != oy["Y"][i]]
    hy = SP / "bs-hakem.json"
    hakem = json.loads(hy.read_text(encoding="utf-8")) if hy.exists() else {}
    ilke = hakem.pop("_ilke", "")
    kalan = [i for i in ayri if i not in hakem]
    if kalan:
        print(f"⛔ HAKEMLİK GEREKİYOR — {len(ayri)} ayrışmanın {len(kalan)}'i açık.\n"
              f"   Dosya: {hy}\n")
        for i in kalan:
            print(f"{i}  ({anah[i]['kimlik']})  X={oy['X'][i]}  Y={oy['Y'][i]}")
        return 1

    karar = {i: hakem.get(i, oy["X"][i]) for i in idler}
    tutan = [i for i in idler if karar[i] == "evet"]

    onc = json.loads((SP / "oz-uzlasma.json").read_text(encoding="utf-8"))
    tek = [i for i in idler if anah[i]["tekrar"]]
    ayni = [i for i in tek if onc[anah[i]["kimlik"]]["karar"] == karar[i]]

    sat = ["# `ozerklik_vurgusu` — `B` tabakasının tam sayımı", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Kapsam:** `B` tabakasının **{len(idler)}** kaydının tamamı "
           "(desen görmedi, ELLE ONAYLADIM)  ", "",
           "⛔⛔ **Ölçülen şey benim kendi hükümlerim.** Kayıtları ben yazdım, "
           "onayları ben verdim; burada onayların ne kadarının tuttuğu "
           "sayılıyor. Hakem de benim ⇒ ayrışan kayıtlarda kendi onayımı "
           "üçüncü kez değerlendiriyorum.", "",
           "## 1. İki anotatör ne kadar uyuştu", "", "| | |", "|---|---:|",
           f"| kayıt | {len(idler)} |",
           f"| ham uyum | %{round(100*(len(idler)-len(ayri))/len(idler))} |",
           f"| κ | {_kappa([oy['X'][i] for i in idler], [oy['Y'][i] for i in idler]):.2f} |",
           f"| hakeme düşen | **{len(ayri)}** |", "",
           "⛔⛔ **κ BURADA YANILTICI ve sebebi taban oranı.** Bu tabakanın "
           "%88'i tek sınıfta (*«evet»*) ⇒ rastlantısal uyum beklentisi çok "
           "yüksek ve κ, ham uyum %89 olmasına rağmen aşağı çekiliyor. "
           "`C` tabakasında dağılım dengeliydi ve aynı iş κ 0,80 vermişti. "
           "➡️ *κ'yı tabakalar arasında karşılaştırmak, taban oranları "
           "karşılaştırmaktır — uyumu değil.*", ""]
    if ayri:
        sat += [f"⛔ {sum(1 for i in ayri if oy['X'][i]=='evet')}/{len(ayri)}'inde "
                "`X` *«evet»* dedi. Hakemin ilkesi (T229'dakiyle aynı):", "",
                f"> {ilke}", "",
                f"⇒ Hakem `X` ile {sum(1 for i in ayri if hakem[i]==oy['X'][i])}/"
                f"{len(ayri)}, `Y` ile {sum(1 for i in ayri if hakem[i]==oy['Y'][i])}/"
                f"{len(ayri)} kayıtta aynı fikirde.", ""]

    sat += ["## 2. ⭐⭐ Gizli tekrar testi (ikinci ölçüm)", "",
            "⛔ T228'de okunmuş 20 kayıt listeye karıştırıldı, söylenmedi. "
            "T229'da aynı test %100 vermişti; bu ikinci ölçüm o sonucun tek "
            "seferlik olup olmadığını söyler.", "", "| | |", "|---|---:|",
            f"| tekrar edilen kayıt | {len(tek)} |",
            f"| ⭐ aynı hükme varılan | **{len(ayni)}/{len(tek)}** "
            f"(%{round(100*len(ayni)/max(1,len(tek)))}) |", ""]
    fark = [i for i in tek if i not in ayni]
    if fark:
        sat += ["| kayıt | T228 | **şimdi** |", "|---|:-:|:-:|"]
        sat += [f"| `{anah[i]['kimlik']}` | {onc[anah[i]['kimlik']]['karar']} | "
                f"**{karar[i]}** |" for i in fark] + [""]

    sat += ["## 3. ⭐⭐⭐ Elle onaylarım ne kadar tuttu", "", "| | |", "|---|---:|",
            f"| elle onay | {len(idler)} |",
            f"| ⭐ doğrulanan | **{len(tutan)}** "
            f"(%{round(100*len(tutan)/len(idler))}) |",
            f"| ⛔ tutmayan | **{len(idler)-len(tutan)}** |",
            f"| T228'in 20 kayıtlık kestirimi | %85 |", ""]
    tutmayan = [anah[i]["kimlik"] for i in idler if karar[i] != "evet"]
    if tutmayan:
        sat += [f"⛔ Tutmayanlar: {', '.join('`'+k+'`' for k in sorted(tutmayan))}", ""]

    # korpus
    onceki = 136
    zaten_dusuk = {anah[i]["kimlik"] for i in idler
                   if anah[i]["tekrar"] and onc[anah[i]["kimlik"]]["karar"] == "hayir"}
    yeni_dusen = [k for k in tutmayan if k not in zaten_dusuk]
    top = onceki - len(yeni_dusen)
    sat += ["## 4. Korpus", "", "| | |", "|---|---:|",
            f"| T229 sonrası beyan | {onceki}/412 (%{round(100*onceki/412)}) |",
            f"| bu sayımla düşen | **−{len(yeni_dusen)}** |",
            f"| ⭐⭐ **yeni toplam** | **{top}/412 (%{round(100*top/412)})** |", "",
            "⭐ Korpus sayısında artık KESTİRİM BİLEŞENİ KALMADI: `A` (24), "
            "`B` (65) ve `C` (323) tabakalarının üçü de tam sayıldı.", "",
            "## ⛔ Bu sayımın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Hakem, denetlenen onayların sahibi** | ayrışan kayıtlarda "
            "kendi kararımı üçüncü kez verdim; bağımsız bir hakem bu tabakada "
            "ötekilerden daha çok gerekiyor |",
            "| ⛔ **Ayrışmayan kayıtların iki oyu var** | T229'daki ödünün aynısı |",
            "| ⛔ **Üçü de Claude** | T227'den beri süren şerh |"]

    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    (SP / "bs-karar.json").write_text(json.dumps(
        {anah[i]["kimlik"]: karar[i] for i in idler}, ensure_ascii=False, indent=1),
        encoding="utf-8")
    print("\n".join(sat))
    print(f"\n→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
