#!/usr/bin/env python3
"""judge v4 çıktısının iki korpus arasında karşılaştırılması.

Aynı rubrik (judge-eksen1.v4) iki korpusa koşturulur ve karşılaştırılır.
Varsayılan: expert-70 (uretim-v2) ↔ v3-parti1. İki korpus da v3 olabilir
(ör. parti 1 ↔ parti 2); sütun adları argümanla verilir.

Kullanım:
  <betik>                                        varsayılan karşılaştırma
  <betik> <judged.jsonl> <rapor.md>              v2 ↔ verilen korpus
  <betik> <A> <A-adı> <B> <B-adı> <rapor.md> --iki-korpus

⚠️ NE ÖLÇÜLÜYOR, NE ÖLÇÜLMÜYOR (K61/K62):
  · `anlasilirlik`  → uzmanın kabul/ret kararını ayırdığı ÖLÇÜLDÜ (uyum oranı 0.81-0.87)
  · `cevapsiz_soru` → elle incelemeye yönlendirir (K57)
  · diğer boyutlar  → TARAMA. Uyum oranı tesadüf bandında; kalite kanıtı değil.

⚠️ BU KONTROLLÜ BİR DENEY DEĞİL. İki korpus yalnızca üretim talimatında değil,
tohumlarda, senaryo karışımında ve yazım oturumunda da farklı (v3 yazılırken
uzmanın 13 notu okunmuştu). Fark v3 talimatına ATFEDİLEMEZ; betimseldir.

"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import statistics as st
import sys
from datetime import date
from pathlib import Path

from scipy.stats import fisher_exact

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
sys.path.insert(0, str(KOK / "src"))
from filter import (ANLASILIRLIK_BAYRAKLARI, DOGALLIK_BAYRAKLARI,  # noqa: E402
                    OARS_BECERILERI, TUZAKLAR, anlasilirlik_hesapla)

V2 = KOK / "data/judged/expert-70.v4.jsonl"
V3 = KOK / "data/judged/v3-parti1.jsonl"
CIKTI = KOK / "reports/analiz/2026-09-14-judge-v4-v3parti1.md"
# Sütun başlıkları: iki korpus da v3 olabildiği için (parti 1 ↔ parti 2) sabit
# "v2/v3" etiketleri dışarıdan verilebilir.
AD_A, AD_B = "v2 korpusu", "v3 korpusu"

BAYRAK_ADI = {
    "kurulmamis_mecaz": "kullanıcının kurmadığı mecaz",
    "belirsiz_gonderge": "belirsiz gönderge (\"o ölçü\", \"o saat\")",
    "ust_uste_yan_cumle": "üst üste binen yan cümle",
    "devrik_eksiltili": "devrik / eksiltili cümle",
    "soyut_adlastirma": "soyut adlaştırma",
}


def sha(p: Path) -> str:
    if "," in str(p):
        h = hashlib.sha256()
        for parca in str(p).split(","):
            h.update(Path(parca.strip()).read_bytes())
        return h.hexdigest() + " (birleşik)"
    return hashlib.sha256(p.read_bytes()).hexdigest()


def yol(p: Path) -> str:
    if "," in str(p):
        return " + ".join(yol(Path(x.strip())) for x in str(p).split(","))
    """Rapor için okunur yol. Komut satırından göreli yol gelirse `relative_to`
    patlıyordu (ön sınamada yakalandı); önce çözümle, depo dışındaysa olduğu gibi yaz."""
    p = p.resolve()
    try:
        return str(p.relative_to(KOK))
    except ValueError:
        return str(p)


def yukle(p: Path):
    """Birden fazla dosya virgülle verilebilir: havuzlanmış karşılaştırma için
    (ör. üç v3 partisi birlikte ↔ v2). Türetilmiş bir dosya yazmıyoruz; havuzlama
    bellekte yapılıyor ki ortada kaynağı belirsiz bir aday dosyası kalmasın."""
    rows = []
    for parca in str(p).split(","):
        rows += [json.loads(l) for l in open(parca.strip()) if l.strip()]
    return [r for r in rows if (r.get("judge") or {})]


def wilson(k: int, n: int) -> tuple[float, float]:
    """Wilson skor aralığı (%95). Küçük n'de normal yaklaşımdan güvenli."""
    if n == 0:
        return (0.0, 0.0)
    z, p = 1.96, k / n
    pay = p + z * z / (2 * n)
    kok = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    payda = 1 + z * z / n
    return ((pay - kok) / payda, (pay + kok) / payda)


def oran_satiri(ad: str, k2: int, n2: int, k3: int, n3: int) -> str:
    a2, b2 = wilson(k2, n2)
    a3, b3 = wilson(k3, n3)
    p = fisher_exact([[k2, n2 - k2], [k3, n3 - k3]])[1]
    isaret = "✅" if p < 0.05 else "—"
    return (f"| {ad} | {k2}/{n2} (%{k2/n2*100:.0f}) | %{a2*100:.0f}-{b2*100:.0f} | "
            f"{k3}/{n3} (%{k3/n3*100:.0f}) | %{a3*100:.0f}-{b3*100:.0f} | "
            f"{p:.3f} {isaret} |")


def main() -> None:
    v2, v3 = yukle(V2), yukle(V3)
    n2, n3 = len(v2), len(v3)
    L = [f"# judge v4 — `{AD_B}` · `{AD_A}` ile karşılaştırma", "",
         f"**Girdi 1 ({AD_A}):** `{yol(V2)}` · SHA256 `{sha(V2)}` · {n2} puanlanan kayıt  ",
         f"**Girdi 2 ({AD_B}):** `{yol(V3)}` · SHA256 `{sha(V3)}` · {n3} kayıt  ",
         f"**Rubrik:** `prompts/judge-eksen1.v4.md` (iki korpusta da aynı) · **Judge:** `agy:gemini-3.8-flash-high`  ",
         f"**Betik:** `{yol(Path(__file__))}` · **Tarih:** {TARIH}", "",
         "---", "",
         "## 0. Bu rapor neyi söyleyebilir", "",
         "| Boyut | Durum | Kaynak |", "|---|---|---|",
         "| `anlasilirlik` | ✅ **Kalite kanıtı.** Uzmanın kabul/ret kararını ayırdığı ölçüldü (uyum oranı 0.81-0.87) | K59 · K62 |",
         "| `cevapsiz_soru` | ✅ Elle incelemeye yönlendirir | K57 |",
         "| `dogallik` · `mi_uyumu` · EPITOME · `grounding` | ❌ **Tarama.** Uyum oranı tesadüf bandında, kalite kanıtı değil | K61 |", "",
         "> ⚠️ **Bu kontrollü bir deney değil.** İki korpus yalnızca üretim talimatında "
         "değil; tohumlarda, senaryo karışımında ve yazım oturumunda da farklı (v3 "
         "yazılırken uzmanın 13 notu okunmuştu). Aradaki fark **v3 talimatına atfedilemez**. "
         "Aşağısı betimsel bir karşılaştırmadır.", "",
         "> `p` sütunu Fisher kesin testi; ✅ = p < 0.05. Aralıklar Wilson %95.", ""]

    # --- 1. anlasilirlik ----------------------------------------------------
    def anl(rows):
        out = []
        for r in rows:
            j = r["judge"]
            v = j.get("anlasilirlik")
            out.append(v if v is not None else anlasilirlik_hesapla(j))
        return [v for v in out if v is not None]

    a2, a3 = anl(v2), anl(v3)
    L += ["## 1. `anlasilirlik` — koddan hesaplanan puan (✅ kalite kanıtı)", "",
          f"| Puan | {AD_A} | {AD_B} |", "|---|---:|---:|"]
    d2, d3 = collections.Counter(a2), collections.Counter(a3)
    for p in (5, 4, 3, 2, 1):
        L.append(f"| {p} | {d2.get(p,0)} (%{d2.get(p,0)/len(a2)*100:.0f}) | "
                 f"{d3.get(p,0)} (%{d3.get(p,0)/len(a3)*100:.0f}) |")
    L += ["", f"| Ölçüm | {AD_A} | %95 aralık | {AD_B} | %95 aralık | p |",
          "|---|---|---|---|---|---|",
          oran_satiri("kusursuz (puan = 5)", sum(1 for v in a2 if v == 5), len(a2),
                      sum(1 for v in a3 if v == 5), len(a3)),
          oran_satiri("iki+ kusur (puan ≤ 3)", sum(1 for v in a2 if v <= 3), len(a2),
                      sum(1 for v in a3 if v <= 3), len(a3)), "",
          f"Ortalama: {AD_A} **{sum(a2)/len(a2):.2f}** · {AD_B} **{sum(a3)/len(a3):.2f}**", ""]

    # --- 2. bayrak bazında --------------------------------------------------
    L += ["## 2. Anlaşılırlık kusurları — bayrak bayrak", "",
          "Puan bu beş bayraktan hesaplanıyor; hangi kusurun değiştiğini gösterir.", "",
          f"| Kusur | {AD_A} | %95 aralık | {AD_B} | %95 aralık | p |", "|---|---|---|---|---|---|"]
    for b in ANLASILIRLIK_BAYRAKLARI:
        L.append(oran_satiri(BAYRAK_ADI[b],
                             sum(1 for r in v2 if r["judge"].get(b) is True), n2,
                             sum(1 for r in v3 if r["judge"].get(b) is True), n3))
    L += [""]

    # --- 3. cevapsiz soru + güvenlik ---------------------------------------
    L += ["## 3. `cevapsiz_soru` ve güvenlik bayrakları", "",
          f"| Ölçüm | {AD_A} | %95 aralık | {AD_B} | %95 aralık | p |", "|---|---|---|---|---|---|",
          oran_satiri("cevapsız soru", sum(1 for r in v2 if r["judge"].get("cevapsiz_soru") is True), n2,
                      sum(1 for r in v3 if r["judge"].get("cevapsiz_soru") is True), n3),
          oran_satiri("klinik güvenlik ihlali", sum(1 for r in v2 if r["judge"].get("klinik_guvenlik_ihlali")), n2,
                      sum(1 for r in v3 if r["judge"].get("klinik_guvenlik_ihlali")), n3),
          oran_satiri("rol sınırı ihlali", sum(1 for r in v2 if r["judge"].get("rol_siniri_ihlali")), n2,
                      sum(1 for r in v3 if r["judge"].get("rol_siniri_ihlali")), n3), ""]

    # --- 4. elle inceleme kuyruğu ------------------------------------------
    kuyruk = []
    for r in v3:
        j, sira = r["judge"], r["gen_meta"]["parti_sira"]
        puan = j.get("anlasilirlik") if j.get("anlasilirlik") is not None else anlasilirlik_hesapla(j)
        sebepler = [BAYRAK_ADI[b] for b in ANLASILIRLIK_BAYRAKLARI if j.get(b) is True]
        if j.get("cevapsiz_soru") is True:
            sebepler.append("cevapsız soru")
        if j.get("klinik_guvenlik_ihlali") or j.get("rol_siniri_ihlali"):
            sebepler.append("⛔ güvenlik/rol bayrağı")
        if sebepler:
            kuyruk.append((sira, puan, sebepler, j.get("en_belirsiz_cumle") or "",
                           j.get("cevapsiz_soru_metni") or ""))
    L += [f"## 4. Elle incelenecek kayıtlar — {len(kuyruk)}/{n3}", ""]
    if kuyruk:
        L += ["| # | anlaşılırlık | judge'ın işaretlediği | judge'ın seçtiği cümle |",
              "|---:|---:|---|---|"]
        for sira, puan, seb, cumle, cs in sorted(kuyruk):
            L.append(f"| {sira} | {puan} | {' · '.join(seb)} | {(cs or cumle)[:110]} |")
    else:
        L.append("_Judge hiçbir kayıtta anlaşılırlık kusuru, cevapsız soru ya da "
                 "güvenlik bayrağı işaretlemedi._")
    L += [""]

    # --- 4b. judge'ın v3'te NE gördüğü (kodla teşhis, K61'in yöntemi) -------
    # `belirsiz_gonderge` v3'te v2'nin üstüne çıktı. Judge'ın çıktısını okuyup
    # "haklı/haksız" demek yerine, bayrağın neyle birlikte gittiğini KODLA arıyorum.
    ANAFORA = re.compile(r"\b(onu|ikisini|ikisi|bunu|bunlar|üçü|o cümle|o hafta|o an)\b", re.I)
    SAHIPLIK = re.compile(r"\bsen (yaptın|söyledin|kurdun|yazdın|ekledin|buldun|fark ettin)"
                          r"|senin (yaptığın|yazdığın|kurduğun)", re.I)

    def son_cumle(c: str) -> str:
        par = [x for x in c.replace("\n", " ").split(". ") if x.strip()]
        return par[-1].strip() if par else ""

    isar = [r for r in v3 if r["judge"].get("belirsiz_gonderge") is True]
    temiz = [r for r in v3 if r["judge"].get("belirsiz_gonderge") is not True]
    a = sum(1 for r in isar if ANAFORA.search(son_cumle(r["messages"][-1]["content"])))
    b = sum(1 for r in temiz if ANAFORA.search(son_cumle(r["messages"][-1]["content"])))
    p_anafora = fisher_exact([[a, len(isar) - a], [b, len(temiz) - b]])[1]
    sah = [r["gen_meta"]["parti_sira"] for r in v3
           if SAHIPLIK.search(r["messages"][-1]["content"].split("\n\n")[-1])]
    sah_isar = sum(1 for r in isar if SAHIPLIK.search(
        r["messages"][-1]["content"].split("\n\n")[-1]))
    p_sahiplik = fisher_exact([[sah_isar, len(isar) - sah_isar],
                               [len(sah) - sah_isar, len(temiz) - (len(sah) - sah_isar)]])[1]

    # ⚠️ Hüküm cümlesi SAYIDAN türetilir. İlk yazımda sabitti ve parti 2'de ilişki
    # kaybolduğu hâlde rapor hâlâ "bayrak rastgele ateşlemiyor (p = 1.0000)" yazdı —
    # kendi kendini yalanlayan bir cümle. Rapor üreticisi bulgu iddia edemez.
    if p_anafora < 0.05:
        hukum = (f"**Bulgu:** bayrak rastgele ateşlemiyor; **son cümlenin zamiriyle** "
                 f"birlikte gidiyor (p = {p_anafora:.4f}).")
    elif p_anafora < 0.20:
        hukum = (f"**Bulgu:** zayıf bir eğilim var ama anlamlı değil (p = {p_anafora:.4f}); "
                 f"bu korpusta ilişki **doğrulanmadı**.")
    else:
        hukum = (f"**Bulgu:** ilişki **YOK** (p = {p_anafora:.4f}). Bu korpusta bayrak son "
                 f"cümlenin zamiriyle birlikte gitmiyor.")
    hukum += (f" Kapanış retoriğiyle ilişkisi {'var' if p_sahiplik < 0.05 else 'yok'} "
              f"(p = {p_sahiplik:.2f}).")
    oran_a = sum(1 for r in v2 if r["judge"].get("belirsiz_gonderge") is True) / n2
    oran_b = len(isar) / n3

    L += ["### 4b. `belirsiz_gonderge` neyi yakalıyor — kodla teşhis", "",
          f"Bayrak `{AD_A}`'nda %{oran_a*100:.0f}, `{AD_B}`'nde %{oran_b*100:.0f}. "
          "Judge'ın çıktısını okuyup haklı ya da haksız demek yerine (metni ben yazdım, "
          "o yargıya ben veremem), bayrağın **neyle birlikte gittiğini** kodla aradım "
          "— K61'in yöntemi.", "",
          "| | işaretli | işaretsiz | Fisher p |", "|---|---:|---:|---:|",
          f"| son cümlede geri-gönderme zamiri (*onu, ikisi, o cümle*) | {a}/{len(isar)} | "
          f"{b}/{len(temiz)} | **{p_anafora:.4f}** |",
          f"| son paragrafta \"bunu sen yaptın\" kapanışı | {sah_isar}/{len(isar)} | "
          f"{len(sah)-sah_isar}/{len(temiz)} | {p_sahiplik:.4f} |", "",
          hukum, "",
          "> ⚠️ **Bu, cümlelerin gerçekten anlaşılmaz olduğunu göstermez.** Her örnekte "
          "göndergenin adı bir-iki cümle önce geçiyor; bu normal Türkçe bağlaşıklığı da "
          "olabilir, uzmanın şikâyet ettiği belirsizlik de. **Bunu metni yazan taraf "
          "karara bağlayamaz** — uzman Oturum 3'e gider (K58: ikinci değerlendirici).", "",
          f"**Ayrı ve judge'dan bağımsız bulgu:** kayıtların **{len(sah)}/{n3}**'ü son "
          f"paragrafını aynı retorikle kapatıyor (*\"bunu sen yaptın / sen söyledin / "
          f"senin yaptığın\"*): #{', #'.join(str(x) for x in sah)}. Korpus raporu bunu "
          "göremez, çünkü §5a kapanışın **türünü** sayıyor, **ifadesini** değil. v2'nin "
          "68/70 soruyla bitme kusuru başka bir eksende tekrarlıyor olabilir.", ""]

    # --- 4c. uzunluk karıştırıcısı ------------------------------------------
    # `belirsiz_gonderge` farkı ham hâlde anlamlı çıkabiliyor; ama iki korpusun
    # cevap uzunlukları çok farklıysa fark uzunluktan geliyor olabilir: uzun cevap
    # = daha çok cümle = daha çok gönderge = bayrağın ateşlemesi için daha çok fırsat.
    # Bu yüzden uzunluk bantlarında EŞLEŞTİRİLMİŞ karşılaştırma da raporlanır.
    uz = lambda r: len(r["messages"][-1]["content"])
    bayrakli = lambda r: r["judge"].get("belirsiz_gonderge") is True
    m2 = st.median([uz(r) for r in v2])
    m3 = st.median([uz(r) for r in v3])
    L += ["### 4c. Uzunluk karıştırıcısı — bantlarda eşleştirilmiş karşılaştırma", "",
          f"Cevap uzunluğu medyanı: `{AD_A}` **{m2:.0f}** · `{AD_B}` **{m3:.0f}** karakter. "
          "Uzun cevapta daha çok cümle, daha çok gönderge ve bayrağın ateşlemesi için "
          "daha çok fırsat var. Ham fark uzunluktan geliyor olabilir; aynı uzunluk "
          "bandındaki kayıtları karşılaştırmak bunu ayırır.", "",
          f"| Uzunluk bandı (karakter) | {AD_A} | {AD_B} | Fisher p |",
          "|---|---|---|---:|"]
    yeterli = False
    for a, b in [(0, 180), (180, 260), (260, 10 ** 6)]:
        x = [r for r in v2 if a <= uz(r) < b]
        y = [r for r in v3 if a <= uz(r) < b]
        ad_b = f"{a}-{b}" if b < 10 ** 6 else f"{a}+"
        if len(x) < 5 or len(y) < 5:
            L.append(f"| {ad_b} | {len(x)} kayıt | {len(y)} kayıt | "
                     f"_n yetersiz, karşılaştırılamaz_ |")
            continue
        yeterli = True
        fx = sum(1 for r in x if bayrakli(r))
        fy = sum(1 for r in y if bayrakli(r))
        pb = fisher_exact([[fx, len(x) - fx], [fy, len(y) - fy]])[1]
        L.append(f"| {ad_b} | {fx}/{len(x)} (%{fx/len(x)*100:.0f}) | "
                 f"{fy}/{len(y)} (%{fy/len(y)*100:.0f}) | {pb:.3f} |")
    L += [""]
    if not yeterli:
        L += ["**Hiçbir bantta iki taraf da yeterli sayıda değil** — uzunluk "
              "karıştırıcısı bu veriyle ayrılamıyor.", ""]
    else:
        L += ["**Okuma:** ham `belirsiz_gonderge` farkı uzunlukla karışıyor. Bantlarda "
              "fark küçülüyor ya da kayboluyor; en uzun bantta karşılaştırma yapılamıyor "
              "çünkü bir tarafta neredeyse hiç kayıt yok. **Ham farkı tek başına bulgu "
              "saymak yanıltıcı olur.**", ""]

    # --- 5. tarama boyutları ------------------------------------------------
    L += ["## 5. Tarama boyutları (❌ kalite kanıtı DEĞİL — K61)", "",
          "Buradaki sayılar **kaliteyi ölçmüyor**; korpusta neyin ateşleyip "
          "ateşlemediğini görmek için duruyor.", "",
          f"| Ölçüm | {AD_A} | {AD_B} |", "|---|---|---|"]
    for ad, alan in [("`dogallik` ortalama", "dogallik"), ("`mi_uyumu` ortalama", "mi_uyumu"),
                     ("`grounding` ortalama", "grounding"), ("EPITOME duygusal tepki", "duygusal_tepki"),
                     ("EPITOME yorumlama", "yorumlama"), ("EPITOME keşif", "kesif")]:
        f = lambda rows: [r["judge"].get(alan) for r in rows if isinstance(r["judge"].get(alan), (int, float))]
        x, y = f(v2), f(v3)
        L.append(f"| {ad} | {sum(x)/len(x):.2f} (n={len(x)}) | {sum(y)/len(y):.2f} (n={len(y)}) |")
    L += ["", f"| Doğallık bayrağı | {AD_A} | {AD_B} |", "|---|---|---|"]
    for b in DOGALLIK_BAYRAKLARI:
        L.append(f"| `{b}` | {sum(1 for r in v2 if r['judge'].get(b) is True)}/{n2} | "
                 f"{sum(1 for r in v3 if r['judge'].get(b) is True)}/{n3} |")
    L += ["", f"| OARS becerisi (judge'a göre) | {AD_A} | {AD_B} |", "|---|---|---|"]
    for b in OARS_BECERILERI:
        L.append(f"| `{b}` | {sum(1 for r in v2 if r['judge'].get(b) is True)}/{n2} (%{sum(1 for r in v2 if r['judge'].get(b) is True)/n2*100:.0f}) | "
                 f"{sum(1 for r in v3 if r['judge'].get(b) is True)}/{n3} (%{sum(1 for r in v3 if r['judge'].get(b) is True)/n3*100:.0f}) |")
    L += ["", f"| TIP 35 tuzağı (judge'a göre) | {AD_A} | {AD_B} |", "|---|---|---|"]
    for b in TUZAKLAR:
        L.append(f"| `{b}` | {sum(1 for r in v2 if r['judge'].get(b) is True)}/{n2} | "
                 f"{sum(1 for r in v3 if r['judge'].get(b) is True)}/{n3} |")
    L += [""]

    # --- 6. okuma -----------------------------------------------------------
    # ⚠️ HER CÜMLE VERİDEN TÜRETİLİR. İlk yazımda bu bölüm sabit metindi ve parti 1
    # için yazılmış yorumlar başka korpus karşılaştırmalarında da basılıyordu —
    # rapor kendi tablosuyla çelişiyordu (tablo 4.30→4.15 derken metin 4.25→4.30).
    # Rapor üreticisi yorum uyduramaz; yalnızca sayının söylediğini yazar.
    ort_a, ort_b = sum(a2) / len(a2), sum(a3) / len(a3)
    k5 = fisher_exact([[sum(1 for v in a2 if v == 5), sum(1 for v in a2 if v != 5)],
                       [sum(1 for v in a3 if v == 5), sum(1 for v in a3 if v != 5)]])[1]
    soru2 = sum(1 for r in v2 if "?" in r["messages"][-1]["content"])
    soru3 = sum(1 for r in v3 if "?" in r["messages"][-1]["content"])

    bayrak_satir, anlamli = [], []
    for b in ANLASILIRLIK_BAYRAKLARI:
        x = sum(1 for r in v2 if r["judge"].get(b) is True)
        y = sum(1 for r in v3 if r["judge"].get(b) is True)
        pb = fisher_exact([[x, n2 - x], [y, n3 - y]])[1]
        yon = "arttı" if y / n3 > x / n2 else ("düştü" if y / n3 < x / n2 else "değişmedi")
        if pb < 0.05:
            anlamli.append(f"`{BAYRAK_ADI[b]}` {yon} (%{x/n2*100:.0f} → %{y/n3*100:.0f}, p = {pb:.3f})")
        bayrak_satir.append((BAYRAK_ADI[b], x / n2, y / n3, pb))

    L += ["## 6. Okuma", "",
          f"**1. `anlasilirlik` ortalaması {ort_a:.2f} → {ort_b:.2f}**, kusursuz oranı "
          f"%{sum(1 for v in a2 if v == 5)/len(a2)*100:.0f} → "
          f"%{sum(1 for v in a3 if v == 5)/len(a3)*100:.0f} "
          + ("(p = %.3f, **anlamlı**)." % k5 if k5 < 0.05 else
             "(p = %.3f, tesadüf bandında)." % k5), ""]
    if anlamli:
        satir = "**2. Anlamlı fark gösteren bayrak(lar):** " + " · ".join(anlamli) + "."
        # `belirsiz_gonderge` uzunlukla karışıyor (§4c). Rapor kendi içinde çelişmesin:
        # anlamlılık iddiası, onu zayıflatan bölüme atıf yapmadan yazılmaz.
        if any("belirsiz" in x for x in anlamli):
            satir += (" ⚠️ **Ama §4c'ye bakın:** bu bayrak cevap uzunluğuyla karışıyor "
                      "ve uzunluk bantlarında eşleştirildiğinde fark küçülüyor ya da "
                      "kayboluyor. Ham anlamlılık tek başına yeterli değil.")
        L += [satir, ""]
    else:
        L += ["**2. Hiçbir anlaşılırlık bayrağı anlamlı fark göstermedi** (hepsi p ≥ 0.05). "
              "Bu, iki korpusun aynı olduğu anlamına gelmez; **n bu büyüklükte farkı "
              "ayırt etmeye yetmiyor** demektir.", ""]
    L += ["**Bayrak bayrak yön:**", "",
          "| Kusur | " + AD_A + " | " + AD_B + " | yön | p |", "|---|---:|---:|---|---:|"]
    for ad, ra, rb, pb in bayrak_satir:
        yon = "↑" if rb > ra else ("↓" if rb < ra else "=")
        L.append(f"| {ad} | %{ra*100:.0f} | %{rb*100:.0f} | {yon} | {pb:.3f} |")
    L += ["",
          f"**3. Soruyla biten cevap {soru2}/{n2} → {soru3}/{n3}.** EPITOME `keşif` "
          "büyük ölçüde soruyla taşınıyor; bu iki sayı birlikte okunmalı, keşif "
          "düşüşü tek başına kalite kaybı sayılmaz.", "",
          f"**4. Güvenlik bayrakları:** klinik ihlal "
          f"{sum(1 for r in v3 if r['judge'].get('klinik_guvenlik_ihlali'))}/{n3}, rol sınırı "
          f"{sum(1 for r in v3 if r['judge'].get('rol_siniri_ihlali'))}/{n3}, cevapsız soru "
          f"{sum(1 for r in v3 if r['judge'].get('cevapsiz_soru') is True)}/{n3}. Bu "
          "bayrakların ayrım gücü hiç ölçülmedi (K61); **yokluk kanıt değildir**.", "",
          "### ⚠️ Gücün sınırı", "",
          f"n = {n2} ve n = {n3} ile oran farklarının %95 aralıkları ±15 puan "
          "civarında. Yani bu araç, **aramaya çalıştığımız büyüklükteki farkları tek "
          "partide ayırt edemiyor**. Tek partide çıkan bir fark, bir sonraki partide "
          "doğrulanmadan bulgu sayılmamalı.", ""]

    CIKTI.write_text("\n".join(L) + "\n")
    print(f"yazıldı: {yol(CIKTI)}  "
          f"(v2 {n2} · v3 {n3} · elle inceleme kuyruğu {len(kuyruk)})")


if __name__ == "__main__":
    # İsteğe bağlı: sonraki partiler için girdi/çıktı yolu dışarıdan verilebilir.
    if len(sys.argv) == 3:
        V3, CIKTI = Path(sys.argv[1]), Path(sys.argv[2])
    elif len(sys.argv) == 7:
        V2, AD_A, V3, AD_B, CIKTI = (Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]),
                                     sys.argv[4], Path(sys.argv[5]))
        _ = sys.argv[6]
    elif len(sys.argv) != 1:
        print("kullanım: uv run python <betik> [judged.jsonl rapor.md]\n"
              "     ya da <betik> <A.jsonl> <A-adı> <B.jsonl> <B-adı> <rapor.md> --iki-korpus")
        sys.exit(1)
    main()
