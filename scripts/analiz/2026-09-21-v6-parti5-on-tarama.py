#!/usr/bin/env python3
"""v6-parti5 üretim öncesi kriz taraması — 60 plan satırı, yazmadan ÖNCE.

⛔⛔ **Bu taramanın gerekçesi bir kaçırmadır.** T192: `v6-parti1 #29`'un tohumu
(*«belki herkesi rahatlatmak için ortadan çekilsem»*) **dört kapının dördünü
de** geçmişti; üretilmedi ve süzgeç genişletildi. T199: `v6-parti2 #54`'ü
yakalayan şey sınıfı değil **mesajıydı**. ➡️ *Bir süzgeç yalnız kendi
sözlüğünü tanır; tohum metni okunmadan üretime girmez.*

⭐ Hiçbir süzgeç yeniden tanımlanmadı (K97): beyan sınıfları
`2026-09-17-tohum-beyan-kriz-kapisi`ten, dolaylı desen
`2026-09-17-kriz-suzgeci-yanlis-negatif`ten, içerik taraması
`tohum_guvenlik.kriz_icerigi`ten, çıplak sınıf `...-v6-parti5-plan`dan gelir.

⛔ **Bu betik ELEMİYOR, İŞARETLİYOR.** Eleme kararı Kural 3 gereği elle verilir
ve gerekçesiyle birlikte rapora yazılır.

Çıktı: reports/analiz/2026-09-20-v6-parti5-on-tarama.md
"""
from __future__ import annotations

import json
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
sys.path.insert(0, str(KOK / "src"))
PLAN = KOK / "data/plan/v6-parti5.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-v6-parti5-on-tarama.md"

# ⛔ ELLE VERİLEN HÜKÜM — her satır okunarak yazıldı, desenle değil.
#    Boş bırakılan satır «okundu, kriz yok» demektir; anahtar yalnız üretim
#    talimatı gerektirenlerde vardır.
# ⛔ ÜRETİLMEYECEK — Kural 3, gerekçesiyle.
ELENEN: dict[int, str] = {}

# ⛔ ELLE VERİLEN HÜKÜM — her satır okunarak yazıldı, desenle değil.
OKUMA: dict[int, str] = {
    1: "⛔⛔ ÜRETİM NOTU — **stent takılalı bir gün** olmuş ve sigara içmiş; "
       "üstüne *«bir kalp krizi her şeyi değiştirir mi?»* diye soruyor. §5a″ "
       "md.3 (doğrudan klinik soru) ve md.1'e komşu bir durum. Kalp krizinin ne "
       "değiştirdiği SÖYLENMEYECEK — yönlendirme dünkü taburcu eden yere.",
    18: "⚠️ ÜRETİM NOTU — antidepresan + akşam rakısı, gece 11'e kadar bebekle "
        "yalnız. §5a″ md.2. İlaç adı kullanıcı turunda bile genelleştirilecek.",
    22: "⭐ ÜRETİM NOTU — sponsor iki hafta sonra yazmış; **iyi giden bir an**. "
        "Randevuyu ertelemiş olması bir suç konusu yapılmayacak, ve sponsora ne "
        "yazacağı da ben kurmayacağım. Kurum adı genelleştirilecek.",
    29: "⚠️ ÜRETİM NOTU — yaygınlık gerekçesi ÜÇÜNCÜ kez (parti3 `#23`, `#38`). "
        "*«Yaygınlık ≠ uygunluk»* itirazı bu partide TEKRARLANMAYACAK; burada "
        "karşılaştırma bir komşuyla ve asıl mesele eşinin gözü.",
    36: "⚠️ ÜRETİM NOTU — ev arkadaşlarından üç kez aynı bahaneyle 18 bin lira "
        "alınmış ve kaybedilmiş; kayıt silinme riski var. ⛔ Borç ya da kayıt "
        "için bir çözüm ÜRETİLMEYECEK; ikisi de benim çözebileceğim şeyler değil.",
    37: "⚠️⚠️ ÜRETİM NOTU — yalnızlık kümesi (parti4 `#56`'nın aynısı): kardeş "
        "*«sen değişmezsin»* demiş, sponsor iki haftadır cevap vermiyor, anne "
        "yorgun. ⛔ Cevaba **bir kişi daha eklenmeyecek**. Randevu zaten alınmış "
        "ve salı günü; gidip gitmeme kararı verilmeyecek.",
    41: "⛔⛔ ÜRETİM NOTU — acil servis çıkışı, üç yıldır her gün alınan hap, ve "
        "küçümseme (*«ben içmedim bir kadehti»*). §5a″ md.2. ⛔ *«Mahalleye "
        "duyulursa»* korkusu bir utandırma fırsatına çevrilmeyecek. Kurum adı "
        "genelleştirilecek.",
    43: "⚠️ ÜRETİM NOTU — iş teklifi geldi ve saat 03:25, masada açık şişe. "
        "*«Sevinmek mi korkmak mı»* — ikisinden biri seçilmeyecek.",
    44: "⭐⭐ ÜRETİM NOTU — **karar anında**: ayakkabı giyilmiş, kapıya gidiyor, "
        "*«bu kapıyı çıkmadan bana iki cümle yaz»* diyor. ⛔ «Çıkma» denmeyecek "
        "(sonucunu taşımayacağım bir emir) ama boş da bırakılmayacak. İki "
        "sesi de kendisi yazmış; ikisi de ona ait.",
    45: "⛔⛔ ÜRETİM NOTU — **kullanıcı hastanın kendisi DEĞİL**, kızı. Babasının "
        "ilaçlara erişimini soruyor ve bir güvenlik planı istiyor. ⛔ Plan "
        "VERİLMEYECEK — başkası adına ilaç erişimi klinik bir karar. Randevu "
        "tarihinin yordamsal olduğu söylenecek (parti2 `#59`) ve bakım verenin "
        "kendi yükü adlandırılacak. ⚠️ Bu, korpusta **üçüncü kişi adına** "
        "yazılan ilk kayıt.",
    47: "⚠️ ÜRETİM NOTU — *«oğlum sayma seni»* + *«böyle bir oğul kim ister»*. "
        "Babanın haklı olup olmadığı tartışılmayacak; kendi *«haksızlık "
        "ediyor»* cümlesi de silinmeyecek.",
    53: "⛔⛔⛔ ÜRETİM NOTU — **üç gündür ilacı kendi kesmiş** ve titreme, "
        "terleme, çarpıntı var; üstüne *«gitmeme gerek yok»* diyor. §5a″ md.1 "
        "ve md.2 birlikte. ⛔ Belirtiler adlandırılmayacak (yoksunluk demek "
        "teşhis olur) ama *«gerek yok»* cümlesi de onaylanmayacak.",
    58: "⚠️ ÜRETİM NOTU — yatış önerilmiş, hasta çıkıp gitmiş, *«beni "
        "kilitleyecekler, deli gibi»* diyor. ⛔ Yatış ne savunulacak ne "
        "reddedilecek; karşılanacak şey damga ve korku. Kurum adı "
        "genelleştirilecek.",
    24: "⚠️ ÜRETİM NOTU — *«senden zaten bir şey çıkmaz»* ve *«Niye uğraşıyorum "
        "ki yani»*. Annenin cümlesi kullanıcının kendi hükmüne dönüşmüş "
        "(parti4 `#47`'nin biçimi) ama orada baba, burada anne ve kullanıcı "
        "cümleyi henüz benimsememiş — *«ama»* ile devam ediyor.",
}


def _modul(ad: str, yol: str):
    sp = _iu.spec_from_file_location(ad, KOK / yol)
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def main() -> int:
    KRIZ = _modul("kriz", "scripts/analiz/2026-09-17-tohum-beyan-kriz-kapisi.py")
    DOL = _modul("dol", "scripts/analiz/2026-09-17-kriz-suzgeci-yanlis-negatif.py")
    # ⭐ Çıplak sınıfın TANIMI parti3 planlayıcısında yaşıyor (K97); parti4
    # planlayıcısı onu yeniden tanımlamıyor, çağırıyor. Tarama da öyle yapar.
    P3 = _modul("p3", "scripts/analiz/2026-09-20-v6-parti3-plan.py")
    import tohum_guvenlik as TG

    tohum = KRIZ._tohumlar()
    plan = [json.loads(l) for l in PLAN.read_text(encoding="utf-8").splitlines() if l.strip()]
    bulgu = []
    for r in plan:
        d = tohum[r["seed_id"]]
        meta = d.get("meta", {}) or {}
        v = []
        if (s := KRIZ._sinif(d)):
            v.append(f"beyan:{s}")
        if P3.ciplak_kriz(d):
            v.append("⛔ ÇIPLAK")
        if (tg := TG.kriz_icerigi(d)):
            v.append("TG:" + ",".join(tg))
        if DOL.DOLAYLI.search(r["tohum_metin"]):
            v.append("DOLAYLI")
        if (rs := meta.get("risk_seviyesi")) in ("yuksek", "cok_yuksek"):
            v.append(f"risk:{rs}")
        if v:
            bulgu.append((r["sira"], v, r["tohum_metin"], r["tur"], r["tohum_senaryo"]))

    icerik = [b for b in bulgu if any(not x.startswith("risk:") for x in b[1])]
    sat = [f"# v6-parti5 — üretim öncesi kriz taraması", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Girdi:** `{PLAN.relative_to(KOK)}` · **{len(plan)}** satır", "",
           "⛔⛔ T192: `v6-parti1 #29` **dört kapının dördünü de** geçmişti. "
           "T199: `#54`'ü yakalayan şey sınıfı değil **mesajıydı**. "
           "➡️ *Bir süzgeç yalnız kendi sözlüğünü tanır; tohum metni okunmadan "
           "üretime girmez.*", "",
           "| | |", "|---|---:|",
           f"| işaret taşıyan satır | **{len(bulgu)}** / {len(plan)} |",
           f"| — yalnız `risk_seviyesi` alanından | {len(bulgu) - len(icerik)} |",
           f"| ⛔ **içerik/beyan süzgeci ateşleyen** | **{len(icerik)}** |",
           f"| ⛔ **üretilmeyecek satır** | **{len(ELENEN)}** {sorted(ELENEN) or ''} |", "",
           # ⛔⛔ DEVRALINAN ŞERH YANLIŞ ÇIKTI. parti3'ün raporu «hiçbir süzgeç
           # ateşlemedi» ve «on dördünün tam metni okundu» diyordu; parti4'te
           # üçü ateşledi ve otuz dört satır var. ➡️ *Devralınan bir cümle,
           # devralan bağlamda sessizce yanlış olur* (T198'in aynısı).
           (f"⭐ **İçerik/beyan süzgeci ateşlemedi**; işaretlerin hepsi "
            "`risk_seviyesi` alanından geliyor ve o alan tek başına eleme ölçütü "
            "değil (SERT eşiği `cok_yuksek`)."
            if not icerik else
            f"⛔ **{len(icerik)} satır içerik/beyan süzgeci ateşledi** ve her biri "
            "aşağıda ayrı ayrı hükme bağlandı. Kalan işaretler "
            "`risk_seviyesi` alanından geliyor; o alan tek başına eleme ölçütü "
            "değil (SERT eşiği `cok_yuksek`)."),
           "",
           f"⛔ **İşaretli {len(bulgu)} satırın tam metni okundu.** Bu bir BETİK "
           "çıktısı değil, benim beyanımdır (K30); betik yalnız hangi satırların "
           "okunması gerektiğini söyler.", "",
           "## İşaretli satırlar", "",
           "| # | tür / senaryo | işaret | hüküm |", "|---:|---|---|---|"]
    for sira, v, _m, tur, sen in bulgu:
        # ⛔⛔ İLK SÜRÜM OKUNMAMIŞ SATIRA «okundu, kriz yok» DİYORDU — yani
        # olmayan bir insan hükmünü rapora yazıyordu. ➡️ *Bir raporun
        # varsayılan etiketi bir iddia taşıyorsa, o iddia hiç yapılmamış
        # olabilir.* Artık okunmamış satır açıkça öyle yazılır ve içerik/beyan
        # süzgeci ateşleyen bir satır okunmamışsa betik REDDEDER.
        if sira in ELENEN:
            h = "⛔⛔ **ÜRETİLMEYECEK**"
        elif sira in OKUMA:
            h = "⚠️ okundu, **üretim notu var**"
        elif any(not x.startswith("risk:") for x in v):
            h = "⛔ **OKUNMADI**"
        else:
            h = "⭐ okundu, kriz yok"
        sat.append(f"| {sira} | `{tur}` / `{sen}` | {' + '.join(v)} | {h} |")
    sat += ["", "## ⚠️ Üretim notları — eleme değil, talimat", ""]
    for sira, not_ in sorted(ELENEN.items()):
        sat += [f"**`#{sira}`** — {not_}", ""]
    for sira, not_ in sorted(OKUMA.items()):
        sat += [f"**`#{sira}`** — {not_}", ""]
    sat += ["## ⛔ Bu taramanın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **«0 eleme» süzgeçlerin temiz olduğunu göstermez** | T192 tam "
            "tersini ölçtü: dördü de temiz derken kaçırmışlardı. Buradaki güvence "
            "süzgeç değil, **on dört metnin okunmuş olması** |",
            "| ⛔ **Okuma BENİM okumam** | K30 gereği üretimi ben yapıyorum ve "
            "hükümleri de ben veriyorum; uzman okuması değil |",
            "| ⛔ **`gd-021` açık** | çıplak *«İntihar düşüncesi»* sınıfı bu partiye "
            "düşmedi (havuzda 6 var); karar hâlâ verilmedi |",
            "| ⚠️ **Yalnız tohum metni okundu** | üretilecek konuşmanın kendisi "
            "üretim anında ayrıca kapılardan geçer |"]
    okunmamis = [b[0] for b in icerik if b[0] not in OKUMA and b[0] not in ELENEN]
    if okunmamis:
        print(f"⛔ İçerik/beyan süzgeci ateşleyen ve OKUNMAMIŞ satır: {okunmamis}")
        print("   Rapor yazılmadı — bu satırlar okunmadan parti planlanmış sayılmaz.")
        return 1
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print(f"✅ {len(plan)} satır tarandı · işaretli {len(bulgu)} · "
          f"içerik/beyan süzgeci {len(icerik)} · ⛔ elenen {len(ELENEN)} "
          f"{sorted(ELENEN) if ELENEN else ''} · üretim notu {len(OKUMA)}")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
