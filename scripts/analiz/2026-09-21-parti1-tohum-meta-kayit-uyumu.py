#!/usr/bin/env python3
"""`v6-parti1`: tohumun meta eksenleri KAYDI tarif ediyor mu?

⛔⛔⛔ **T219'UN AÇIK BIRAKTIĞI SORU.** T219 ölçtü: parti1'de kaydın kendi
tohumuyla sözcük örtüşmesi ortalama %6 (21 kayıtta sıfır), sonraki
partilerde %49-71. Yani tohum parti1'de ızgara hücresini verdi, metni
vermedi. ⇒ Kapsama envanteri eksenleri **tohumun meta'sından** alıyor;
parti1'de metin tohumdan gelmediği için o etiketlerin kaydı tarif etmeme
riski vardı ve **ölçülmemişti**. Bu betik onu ölçüyor.

⭐ **ÖLÇÜM ELLEDİR VE ÖYLE OLMALI (K30).** Bir etiketin metni tarif edip
etmediği bir okuma işidir; sözlükle yapılamaz (T192/T213: süzgeç kendi
sözlüğünü tanır). 59 kaydın tamamı altı eksene karşı okundu ve hüküm
aşağıda yazılı. Betik yalnız sayıyor; hükmü ben verdim.

⭐ Üç değerli ölçek — bunun sebebi de bir ders:
  `U` uyumlu    — metin etiketi DESTEKLİYOR
  `Ç` çelişiyor — metin etiketle ÇELİŞİYOR (ya da başka bir değeri anlatıyor)
  `S` sessiz    — metin etiket hakkında bir şey söylemiyor
⛔ `S` bir kusur değil, bir **görünmezlik**: etiket yanlış olabilir de doğru
olabilir de, kayıttan anlaşılmıyor. Kapsama envanteri açısından `Ç` ile `S`
aynı kapıya çıkar — ikisinde de sayılan şey kaydın kendisi değildir.

⛔⛔ **ÜÇ EKSEN ÖLÇÜLMEDİ VE SEBEBİ YAZILI:** `risk_seviyesi`,
`siddet_seviyesi`, `motivasyon_evresi`. Üçü de bir DERECE ve kısa bir
konuşmadan derece okumak, eşiği benim koymam demek olurdu — `gd-024`'ün
tam olarak yasakladığı şey. Ölçülmediler; ölçülmediği burada yazılı.

Çıktı: reports/analiz/2026-09-21-parti1-tohum-meta-kayit-uyumu.{md,json}
"""
from __future__ import annotations

import collections
import hashlib
import json
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-parti1-tohum-meta-kayit-uyumu.md"
JSON = KOK / f"reports/analiz/{TARIH}-parti1-tohum-meta-kayit-uyumu.json"
EKSEN = ["bagimlilik_turu", "yas_grubu", "profil", "senaryo", "evre", "stres_tipi"]
OLCULMEYEN = ["risk_seviyesi", "siddet_seviyesi", "motivasyon_evresi"]

# ⛔⛔⛔ KURAL İLAN EDİLDİ (2026-09-21, ikinci okuma). İlk okumada `Ç` ile `S`
# arasındaki sınırı yazmamıştım ve **iki raporda farklı uygulamışım**: burada
# *«metin başka bir hayat gösteriyor»*u çelişki saymışım, parti3-6 raporunda
# ise yalnız *«metin aynı eksenin başka bir DEĞERİNİ öne çıkarıyor»*u. Sınır
# yazılmayınca ölçü kaydı. ➡️⭐⭐⭐ *Üç değerli bir ölçekte asıl iş orta
# değerin sınırındadır; o sınır yazılmazsa ölçek okuyucuya göre kayar ve iki
# rapor aynı adı taşıyan iki ayrı şeyi ölçer.*
#
# ⭐ İLAN: eksenler şemada TEK DEĞERLİ. Buna göre
#   `Ç` = metin, aynı eksenin etiketten FARKLI bir değerini öne çıkarıyor
#   `S` = metin o eksen hakkında hiçbir değer öne çıkarmıyor
#   `U` = metin etiketi destekliyor
# ⛔ *«Etiket buraya oturmuyor»* sezgisi tek başına `Ç` değildir; hangi başka
#   değerin göründüğü söylenebilmelidir.
#
# ⛔⛔⛔ ÜÇÜNCÜ OKUMA (T224 sonrası). İlk iki okuma YANLIŞ TOHUMLARA karşı
# yapılmıştı: parti1'in planı üretimden sonra ezilmiş, kayıtların künyesi yeni
# plandan damgalanmıştı. Künye onarıldıktan sonra 59 kaydın altı ekseni BAŞTAN
# okundu. ⛔ Önceki iki okumanın sayıları (22 → kural ilan edilince 14)
# GEÇERSİZDİR: başka tohumları ölçüyorlardı.
#
# ⛔ ELLE VERİLEN HÜKÜM (K30) — sıra: bagimlilik_turu, yas_grubu, profil,
#    senaryo, evre, stres_tipi. U=uyumlu · Ç=çelişiyor · S=sessiz
HUKUM: dict[int, str] = {
    1: "USSSSU",  2: "ÇUÇSSU",  3: "SUUSUU",  4: "SSSUSU",  5: "UUSUUS",
    6: "UUSSUU",  7: "USSSSU",  8: "SUSSUU",  9: "SSSSÇU",  10: "USSSUU",
    11: "UUSUUU",  12: "SUUUUU",  13: "UUSSSU",  14: "USSSUU",  15: "USSUSU",
    16: "SUUUSU",  17: "UUUUSÇ",  18: "SSSSSU",  19: "UUUUUÇ",  20: "UUSUUÇ",
    21: "UUSSSU",  22: "UUSUÇU",  23: "USSSUU",  24: "USUSUU",  25: "SSSSSU",
    26: "UUSUUU",  27: "SUSSUU",  28: "USSUUS",  30: "UUSSUU",  31: "USSSSU",
    32: "SSSSSU",  33: "UUUUUÇ",  34: "UUSSSU",  35: "SUSUSU",  36: "UUSSUU",
    37: "SUUSSU",  38: "SUSSÇU",  39: "UUSUÇU",  40: "UUSUSU",  41: "USSUÇU",
    42: "UUUUUS",  43: "USSSUS",  44: "UUSSSU",  45: "UUUUSU",  46: "SSSSSU",
    47: "UUSSUU",  48: "USSUUU",  49: "USUUUÇ",  50: "UUSSUU",  51: "USSUSU",
    52: "USUUUS",  53: "SUSUSU",  54: "USSUUS",  55: "SUUUSU",  56: "SSSSSU",
    57: "SSSSUU",  58: "USSUSS",  59: "UUUSSU",  60: "UUUUUU",
}

# ⭐⭐ İKİNCİ OKUMADA GERİ ALINAN — kural ilan edilince düşenler. Sekizinin
#    sekizi de aynı yönde: metin BAŞKA BİR HAYAT gösteriyordu ama aynı eksenin
#    başka bir DEĞERİNİ göstermiyordu.
GERI_ALINAN: dict[str, str] = {}   # ⛔ üçüncü okumada geri alınan yok

# ⛔ Çelişkilerin GEREKÇESİ — sayı tek başına denetlenemez.
GEREKCE: dict[str, str] = {
 "2/bagimlilik_turu": "`kumar`; metinde bahis yok, *«iş için sürekli "
                      "ekrandayım»* — öne çıkan `dijital`",
 "2/profil": "`kronik_issiz`; metin *«iş için»* diyor, yani çalışıyor",
 "9/evre": "`sosyal_kullanim`; metin *«tek başıma uğruyorum»* ve artan sıklık "
           "diyor — öne çıkan `tolerans`",
 "17/stres_tipi": "`kronik_agri`; metinde ağrı yok, eş kaybı var (`yas_kayip`)",
 "19/stres_tipi": "`yok`; metin *«belim için»* diyor — `kronik_agri` öne çıkıyor",
 "20/stres_tipi": "`yok`; metin *«annemin yası»* diyor — `yas_kayip` öne çıkıyor",
 "22/evre": "`birakma_cabasi`; metin kullanımı savunuyor — `inkar` öne çıkıyor",
 "33/stres_tipi": "`kronik_agri`; metinde ağrı yok, kızının gelememesi ve "
                  "yalnızlık var",
 "38/evre": "`tolerans`; metin temiz test ve seans anlatıyor — `birakma_cabasi`",
 "39/evre": "`nuksetme`; metin kullanımı savunuyor — `inkar` öne çıkıyor",
 "41/evre": "`birakma_cabasi`; metin *«benimki de zaten bir iki kadeh»* diye "
            "gerekçe kuruyor — `inkar`",
 "49/stres_tipi": "`yalnizlik`; metinde eşle süren bir çatışma var "
                  "(`aile_catismasi`)",
}


def main() -> int:
    sp = _iu.spec_from_file_location(
        "kriz", KOK / "scripts/analiz/2026-09-17-tohum-beyan-kriz-kapisi.py")
    K = _iu.module_from_spec(sp)
    sp.loader.exec_module(K)
    toh = K._tohumlar()
    pdos, kdos = KOK / "data/plan/v6-parti1.jsonl", KOK / "data/candidates/v6-parti1.jsonl"
    plan = {json.loads(l)["sira"]: json.loads(l)
            for l in pdos.read_text(encoding="utf-8").splitlines() if l.strip()}
    kay = [json.loads(l) for l in kdos.read_text(encoding="utf-8").splitlines() if l.strip()]
    siralar = sorted(r["gen_meta"]["parti_sira"] for r in kay)

    # ⛔⛔ OKUMA KAPISI — hükmü olmayan kayıt kalırsa rapor YAZILMAZ (T213).
    eksik = [s for s in siralar if s not in HUKUM]
    fazla = [s for s in HUKUM if s not in siralar]
    bozuk = [s for s, h in HUKUM.items() if len(h) != len(EKSEN) or set(h) - set("UÇS")]
    if eksik or fazla or bozuk:
        print(f"⛔ OKUMA KAPISI: hükmü olmayan {eksik} · fazla {fazla} · bozuk {bozuk}")
        return 1

    say = {e: collections.Counter() for e in EKSEN}
    for s in siralar:
        for e, h in zip(EKSEN, HUKUM[s]):
            say[e][h] += 1
    n = len(siralar)
    celiskiler = [(s, e, HUKUM[s]) for s in siralar for i, e in enumerate(EKSEN)
                  if HUKUM[s][i] == "Ç"]

    JSON.write_text(json.dumps({"tarih": TARIH, "n": n, "eksen": EKSEN,
                                "hukum": HUKUM, "gerekce": GEREKCE},
                               ensure_ascii=False, indent=1), encoding="utf-8")

    top_c = sum(say[e]["Ç"] for e in EKSEN)
    top_s = sum(say[e]["S"] for e in EKSEN)
    top_u = sum(say[e]["U"] for e in EKSEN)
    sat = ["# `v6-parti1`: tohumun meta eksenleri kaydı tarif ediyor mu?", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Girdi:** `{kdos.relative_to(KOK)}` SHA256-16 "
           f"`{hashlib.sha256(kdos.read_bytes()).hexdigest()[:16]}` · **{n}** kayıt  ",
           f"**Ölçek:** `U` uyumlu · `Ç` çelişiyor · `S` sessiz — 59 kayıt × "
           f"{len(EKSEN)} eksen = **{n*len(EKSEN)}** hüküm, hepsi elle (K30)", "",
           "⛔⛔ T219 parti1'in başka bir rejimde yazıldığını ölçmüştü (kaydın kendi "
           "tohumuyla örtüşmesi %6). Bu rapor, o rejimin **kapsama ölçümüne** ne "
           "yaptığını ölçüyor.", "",
           "## 0. ⭐⭐⭐ Sonuç", "",
           f"| | | |", "|---|---:|---:|",
           f"| ⭐ **uyumlu** | {top_u} | %{100*top_u/(n*len(EKSEN)):.0f} |",
           f"| ⚠️ **sessiz** | {top_s} | %{100*top_s/(n*len(EKSEN)):.0f} |",
           f"| ⛔ **çelişiyor** | **{top_c}** | **%{100*top_c/(n*len(EKSEN)):.0f}** |", "",
           "## 1. Eksen eksen", "",
           "| eksen | uyumlu | sessiz | ⛔ çelişiyor | kayıttan doğrulanabilen |",
           "|---|---:|---:|---:|---:|"]
    for e in EKSEN:
        c = say[e]
        sat.append(f"| `{e}` | {c['U']} | {c['S']} | **{c['Ç']}** | "
                   f"%{100*(c['U']+c['Ç'])/n:.0f} |")
    sat += ["", "⛔⛔ **Ölçülmeyen eksenler:** " +
            ", ".join(f"`{e}`" for e in OLCULMEYEN) +
            " — üçü de bir DERECE ve kısa bir konuşmadan derece okumak eşiği benim "
            "koymam demek olurdu (`gd-024`). Ölçülmediler.", "",
            "## 2. ⛔ Çelişen etiketler — gerekçeleriyle", "",
            "| # | eksen | gerekçe |", "|---:|---|---|"]
    for s, e, _ in celiskiler:
        sat.append(f"| {s} | `{e}` | {GEREKCE.get(f'{s}/{e}', '⛔ **GEREKÇE YOK**')} |")
    sat += ["", "## 3. Satır satır hüküm", "",
            "| # | " + " | ".join(f"`{e[:12]}`" for e in EKSEN) + " |",
            "|---:|" + "---|" * len(EKSEN)]
    for s in siralar:
        sat.append(f"| {s} | " + " | ".join(HUKUM[s]) + " |")
    sat += ["", "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Hüküm BENİM okumam** (K30) | bağımsız bir okuyucu farklı "
            "ayırabilir; ikinci anotatör yok ve uyum oranı ölçülmedi |",
            "| ⛔⛔ **`S` bir aklanma değil** | kapsama envanteri açısından `Ç` ile "
            "`S` aynı kapıya çıkar: ikisinde de sayılan şey kaydın kendisi değildir. "
            f"Kayıttan doğrulanabilen oran yalnızca %{100*(top_u+top_c)/(n*len(EKSEN)):.0f} |",
            "| ⛔ **Karşılaştırma yok** | aynı ölçüm `v6-parti3-6` için yapılmadı; "
            "oradaki oranın daha yüksek olduğu BEKLENİYOR ama ölçülmedi ⇒ bu sayılar "
            "tek başına *«parti1 kötü»* demiyor, *«parti1 ölçülemiyor»* diyor |",
            "| ⛔⛔ **Düzeltme yapılmadı** | ne etiketler değişti ne kayıtlar; "
            "`datasets/` dokunulmadı |",
            "| ⚠️ **Etiketin kaynağı tohum, kaydın kaynağı ızgara** | ızgaranın "
            "kendi alanları (`tur`, `yas`) kayıtla tutarlı çünkü kayda plandan "
            "yazılıyorlar; ölçülen şey tohumun META'sı |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print(f"✅ {n} kayıt × {len(EKSEN)} eksen · uyumlu {top_u} · sessiz {top_s} · "
          f"⛔ çelişen {top_c}")
    for e in EKSEN:
        c = say[e]
        print(f"   {e:18s} U {c['U']:2d} · S {c['S']:2d} · Ç {c['Ç']:2d}")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
