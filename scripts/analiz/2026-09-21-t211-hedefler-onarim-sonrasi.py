#!/usr/bin/env python3
"""T211'in hedefleri — onarım sonrası zeminde yeniden türetildi.

⛔⛔ **GEREKÇE T224.** `v6-parti1`'in künyesi bozuktu; kapsama envanteri
*«kullanılmış tohum»* üzerinden ölçtüğü için parti1'in 59 kaydı yanlış
tohumlarla sayılıyordu. Künye onarıldı ⇒ T211'in ufuk kuralının girdisi
değişti ve hedeflerin yeniden türetilmesi gerekti.

⭐ **KURAL YENİDEN TANIMLANMIYOR (K97).** Ufuk kuralı parti6 planlayıcısının
`paylar()` fonksiyonundan **çağrılıyor**; bu betik yalnız girdiyi (envanter
dosyaları, N₀, K) değiştirip sonucu yazıyor.

⭐ **İKİ ZEMİN YAN YANA.** Aynı 6 parti, iki farklı *«kullanılmış»* kümesi:
onarım öncesi (bozuk künye) ve sonrası. Aradaki fark, bozulmanın
hedeflemeye ne yaptığını gösterir.

⛔ **K SEÇİMDİR** ve iki değerle birden raporlanıyor (K=2 ve K=3), çünkü
korpus hedeflenen büyüklüğe yaklaştı: N₀ + 2×60 ile N₀ + 3×60 arasındaki
fark artık kuralı belirgin biçimde oynatıyor.

Çıktı: reports/analiz/2026-09-21-t211-hedefler-onarim-sonrasi.md
"""
from __future__ import annotations

import json
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-t211-hedefler-onarim-sonrasi.md"
N = 60
ZEMIN = {
    "onarım ÖNCESİ": ("2026-09-20-kapsama-acigi-envanteri-parti1-6-onarim-oncesi",
                      "2026-09-21-hucre-kapsama-envanteri-parti1-6-onarim-oncesi"),
    "onarım SONRASI": ("2026-09-20-kapsama-acigi-envanteri-parti1-6-onarim-sonrasi",
                       "2026-09-21-hucre-kapsama-envanteri-parti1-6-onarim-sonrasi"),
}


def _modul(ad: str, yol: str):
    sp = _iu.spec_from_file_location(ad, KOK / yol)
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def main() -> int:
    PP6 = _modul("pp6", "scripts/analiz/2026-09-21-v6-parti6-plan.py")
    n0 = PP6.PP5.korpus_boyu()
    PP6.N = N

    sonuc = {}
    for zemin, (mj, hc) in ZEMIN.items():
        PP6.MARJINAL = KOK / f"reports/analiz/{mj}.json"
        PP6.HUCRE = KOK / f"reports/analiz/{hc}.json"
        for k in (2, 3):
            PP6.K_UFUK = k
            hedef, kacinma, kota, _n0, kirpik, kaynak = PP6.paylar()
            sonuc[(zemin, k)] = {"hedef": hedef, "kota": kota, "kaynak": kaynak,
                                 "kirpik": kirpik}

    anahtarlar = sorted({kaynak_ad
                         for v in sonuc.values()
                         for kaynak_ad in (b["ad"] for b in v["kaynak"].values())})
    sat = ["# T211'in hedefleri — onarım sonrası zeminde yeniden türetildi", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Kural:** T211'in ufuk kuralı, parti6 planlayıcısının `paylar()` "
           f"fonksiyonundan ÇAĞRILDI (yeniden tanımlanmadı) · **N₀ = {n0}** · n = {N}", "",
           "⛔⛔ T224: `v6-parti1`'in künyesi bozuktu ve kapsama envanteri "
           "*«kullanılmış tohum»* üzerinden ölçtüğü için parti1'in 59 kaydı yanlış "
           "tohumlarla sayılıyordu. Künye onarıldı ⇒ kuralın girdisi değişti.", "",
           "## 0. ⭐⭐⭐ Onarımın hedeflemeye etkisi KÜÇÜK", "",
           "| | onarım öncesi | onarım sonrası |", "|---|---:|---:|"]
    mo = json.loads((KOK / f"reports/analiz/{ZEMIN['onarım ÖNCESİ'][0]}.json").read_text(encoding="utf-8"))
    ms = json.loads((KOK / f"reports/analiz/{ZEMIN['onarım SONRASI'][0]}.json").read_text(encoding="utf-8"))
    sat += [f"| kullanılmış (benzersiz) tohum | {mo['uretilmis']} | {ms['uretilmis']} |",
            f"| eşiği aşan marjinal sınıf | {len(sonuc[('onarım ÖNCESİ',3)]['kota'])+len(sonuc[('onarım ÖNCESİ',3)]['hedef'])} "
            f"| {len(sonuc[('onarım SONRASI',3)]['kota'])+len(sonuc[('onarım SONRASI',3)]['hedef'])} |", "",
            "⭐ Bozulma 59 kaydın künyesini değiştirmişti ama envanter ~970 tohum "
            "üzerinden ölçüyor: her eksenin payı **bir puanın çok altında** oynadı "
            "(`evre=tolerans` −3,30 → −3,60 · `profil=mavi_yakali` −4,10 → −4,20) "
            "ve eşiği aşan birimlerin **kümesi hiç değişmedi**. ➡️⭐⭐ *Bir veri "
            "bozulması, ölçümün paydası yeterince büyükse hedeflemeye "
            "yansımayabilir; bu, bozulmanın önemsiz olduğunu değil, bu ölçümün "
            "ona duyarsız olduğunu gösterir.*", "",
            "## 0b. ⛔⛔⛔ ASIL SONUÇ: KURAL ARTIK YALNIZ İKİ EKSENDEN "
            "KONUŞUYOR — VE İKİSİ DE BU OTURUMDA SORUNLU ÇIKTI", "",
            "⭐ Altı parti sonra ufuk kuralı **sıfır hedef, altı tavan** "
            "üretiyor (her iki zeminde ve her iki K'de). Yani *«eksik taşınan»* "
            "diye bir birim kalmadı; kural yalnızca *«fazla taşıma»* diyor.", "",
            "⛔⛔ Altı tavanın **dördü `profil=mavi_yakali`** içeriyor "
            "(marjinal + üç hücre), kalan ikisi **`evre=tolerans`**. Başka hiçbir "
            "eksen eşiği aşmıyor.", "",
            "⛔⛔⛔ **Bu iki eksen de bu oturumda ölçüm sorunu çıkardı:** "
            "T220/T221 `profil`in v6 kayıtlarının **yarısından fazlasında "
            "metinde hiç görünmediğini** ölçtü (parti1 %27, parti3-6 %53 "
            "doğrulanabilir); T223 `evre` etiketlerinin **%10'unun metinle "
            "çeliştiğini** ve hatanın tek taraflı olduğunu ölçtü. ➡️⭐⭐⭐ *Bir "
            "hedefleme kuralı, korpus yeterince büyüdükçe yalnız en zor "
            "kapanan birimlerde konuşmaya başlar; ve bir eksenin zor kapanması "
            "ile o eksenin KAYITTA GÖRÜNMEMESİ aynı şeyin iki yüzü olabilir. "
            "`profil=mavi_yakali` altı partidir kapanmıyor çünkü belki de "
            "kapatılacak bir şey yok — ölçülen şey metinde değil, tohum "
            "dosyasında.*", "",
            "⛔ Bu bir **tasarım kararını** zorunlu kılıyor ve bu betik onu "
            "vermiyor: (a) `profil` ekseni hedeflemeden çıkarılsın mı, "
            "(b) tohum meta'sı yerine kayıttan okunabilir bir eksen tanımlansın "
            "mı, (c) kural olduğu gibi mi kalsın. Üçü de bir sonraki partinin "
            "planlayıcısında gerekçesiyle yazılmalı.", "",
            "## 1. ⭐ Yeni hedefler (onarım sonrası zemin)", "",
            "| birim | tür | fark | **K=2 payı** | **K=3 payı** |",
            "|---|---|---:|---:|---:|"]
    s2, s3 = sonuc[("onarım SONRASI", 2)], sonuc[("onarım SONRASI", 3)]
    for k, b in sorted(s3["kaynak"].items(), key=lambda x: x[1]["fark"]):
        yon = "hedef" if k in s3["hedef"] else "tavan"
        p2 = s2["kaynak"].get(k, {}).get("pay", "—")
        sat.append(f"| `{b['ad']}` | {b['tur']} · {yon} | {b['fark']:+.2f} | "
                   f"**{p2}** | **{b['pay']}** |")
    sat += ["", f"⛔ **K seçimi artık belirleyici.** N₀={n0}; K=2 korpusu "
            f"{n0 + 2*N}'ya, K=3 {n0 + 3*N}'ya taşır. Hedeflenen büyüklük "
            "~1.000-1.100 olduğu için **ikisi de savunulabilir** ve payları "
            "yukarıdaki tabloda yan yana duruyor. Bu betik bir seçim YAPMIYOR; "
            "seçim bir sonraki partinin planlayıcısında ve gerekçesiyle "
            "yazılmalı.", "",
            "## 2. İki zemin, aynı kural (K=3)", "",
            "| birim | öncesi payı | sonrası payı |", "|---|---:|---:|"]
    o3 = sonuc[("onarım ÖNCESİ", 3)]
    adlar = {b["ad"]: k for k, b in s3["kaynak"].items()}
    for ad in sorted(set(adlar) | {b["ad"] for b in o3["kaynak"].values()}):
        po = next((b["pay"] for b in o3["kaynak"].values() if b["ad"] == ad), "—")
        ps = next((b["pay"] for b in s3["kaynak"].values() if b["ad"] == ad), "—")
        isaret = " ⛔" if po != ps else ""
        sat.append(f"| `{ad}` | {po} | {ps}{isaret} |")
    sat += ["", "## ⛔ Bu türetmenin söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Hedef ≠ kalite** | T211'in kendi şerhi: payı havuza "
            "yaklaştırmak o birimde iyi kayıt üretileceğini göstermez |",
            "| ⛔⛤ **`profil` ekseni korpusta GÖRÜNMÜYOR** (T220/T221) | v6 "
            "kayıtlarının yarısından fazlasında metin mesleki profil hakkında "
            "hiçbir şey söylemiyor. `profil=mavi_yakali` tavanı bu yüzden "
            "**görünmeyen bir eksende** işliyor ve bu tabloda hâlâ en büyük "
            "birim. Kaldırmak ya da bırakmak bir tasarım kararı; verilmedi |",
            "| ⛔ **37 çift kayıt sayıma dahil** | aynı tohumdan iki kayıt "
            "üretilmiş durumda; envanter tohumu bir kez sayıyor, korpus iki "
            "kayıt taşıyor |",
            "| ⛔ **K seçilmedi** | iki değerle raporlandı; seçim planlayıcıya "
            "bırakıldı |",
            "| ⚠️ **Fazla temsilin KUSUR olduğu hâlâ gösterilmedi** | "
            "envanterin varsayımı *«set havuzu yansıtmalı»* ve havuz bir "
            "tasarım ürünü (T211'den beri açık) |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print(f"✅ N₀={n0} · onarım öncesi/sonrası iki zemin, K=2 ve K=3")
    for (z, k), v in sonuc.items():
        print(f"   {z} K={k}: hedef {len(v['hedef'])} · tavan {len(v['kota'])}")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
