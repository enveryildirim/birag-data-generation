#!/usr/bin/env python3
"""`ozerklik_vurgusu` beyanını METİNDEN yeniden ölçer — beyan niyetin değil
hamlenin kaydıdır (v4 §5a).

⛔⛔ **Neden var.** Blok 6'da özerklik deseni genişletilirken ölçüldü: desen
`ozerklik=0` beyan edilmiş **3 kayıtta** da vuruyor (`#5 11 20`). Bunlar yanlış
pozitif değil — cevaplarda gerçekten *«o senin kararın»*, *«ne yapacağına sen
karar vereceksin»* geçiyor. Yani hamle yapılmış, beyan edilmemiş.

➡️⭐⭐ *Izgara bir TASARIM, `gen_meta` bir KAYIT. Tasarımın «bu satırda özerklik
yok» demesi, yazılan cevapta olmadığı anlamına gelmez; ve §5a'nın kendi cümlesi
beyanın yapılanı kaydettiğini söylüyor. Beyanı tasarımdan kopyalamak, kaydı
niyete eşitlemektir.*

⭐ **Bu betik ne yapar:** üretilmiş bloklarda `gen_meta.ozerklik_vurgusu`'nu
metinden ölçer, ızgaranın dediğini `izgara_ozerklik` alanına ayrıca yazar ve
ikisi ayrıldığında bunu **rapor eder**. ⛔ Izgaranın 1 dediği yerde metinde yoksa
bu bir EKSİKTİR ve blok betiklerinin kapısı onu zaten reddediyor; ters yön
(metinde var, ızgarada yok) bir eksik değil — §5a özerkliği **hedef** sayıyor
(~%20), tavan değil.

Girdi/Çıktı : data/candidates/v6-parti1.blok*.jsonl (yerinde güncellenir)
Rapor       : reports/analiz/2026-09-20-beyan-metin-uyumu.md
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]

# ⭐ Parti parametre oldu (T199 ile aynı gerekçe: TANIM tek, girdi değişken).
# ⛔ parti1 raporunun adı KORUNDU — dosya üretilmiş ve alıntılanıyor.
_ap = argparse.ArgumentParser()
_ap.add_argument("--parti", default="v6-parti1")
PARTI = _ap.parse_args().parti
_ek = "" if PARTI == "v6-parti1" else f"-{PARTI}"
PLAN = KOK / f"data/plan/{PARTI}.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-beyan-metin-uyumu{_ek}.md"

# ⭐ T193 `ozerklik` için yapılmıştı ve şerhi *«öteki beyan alanları taranmadı»*
# diyordu. `is_negative` eklendi: aynı sorun orada da var (`#48` ve `#51`'de
# ızgara `neg=0` diyor ama cevaplar açıkça reddediyor).
# ⛔ YÖN ASİMETRİK ve bilerek: özerklikte «metinde var, ızgarada yok» eksik
# sayılmıyor (§5a özerkliği HEDEF sayıyor); redde de öyle — ama tersi, yani
# «ızgara istiyor, metinde yok», ikisinde de EKSİKTİR ve blok kapısı tutar.
RED = re.compile(r"veremem|söyleyemem|yapamam|bana düşmez|benim işim değil|"
                 r"yerine geçemem|karar veremem|cevabı bende yok|"
                 r"bunu ben (söyle|belirle|yorumla)", re.I)
OZERKLIK = re.compile(r"senin kararın|sen karar ver|karar sende|bana düşmez|"
                      r"senin yerine karar|bırak demeyeceğim|ne yapacağını sen|"
                      r"senin bileceğin|sen bilirsin|bunu senin yerine (söyle|karar)|"
                      r"önerecek bir şeyim yok", re.I)


def main() -> int:
    plan = {json.loads(l)["sira"]: json.loads(l)
            for l in PLAN.read_text(encoding="utf-8").splitlines() if l.strip()}
    satir, degisen, eksik = [], [], []
    oku_kuyrugu: list[tuple[int, bool, bool]] = []
    kayitlar_tum: list[dict] = []
    for f in sorted(KOK.glob(f"data/candidates/{PARTI}.blok*.jsonl")):
        kayitlar = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
        for r in kayitlar:
            s = r["gen_meta"]["parti_sira"]
            son = [m for m in r["messages"] if m["role"] == "assistant"][-1]["content"]
            # ⛔⛔ K97 ÇARPIŞMASI. Blok kapısı «desen VEYA elle onay» diyor,
            # burası yalnız «desen» diyordu ⇒ bu betik parti1'in 6, parti2'nin
            # 19 elle onayını SESSİZCE geri aldı ve raporunda onları «eksik»
            # diye listeledi. ➡️ *Aynı ölçünün iki tanımı varsa, ikincisi
            #    birincinin kararını ölçüm gibi görünerek siler.*
            # Tanım artık tek: desen VEYA kayda geçmiş insan onayı.
            onayli = set(r["gen_meta"].get("elle_onay", []))
            olculen = bool(OZERKLIK.search(son)) or "ozerklik_vurgusu" in onayli
            izgara = bool(plan[s]["ozerklik"])
            if izgara and not olculen:
                eksik.append(s)                     # ⛔ blok kapısı bunu zaten tutuyor
            if olculen != r["gen_meta"].get("ozerklik_vurgusu"):
                degisen.append((s, r["gen_meta"].get("ozerklik_vurgusu"), olculen))
            # ⛔⛔ T228: UZLAŞTIRILMIŞ KAYITLAR KORUNUYOR. Özerklik deseni
            # fazla saymıyor (%96 kesinlik, 24 kayıtlık sayım) ⇒ kaldırılmadı;
            # ama üç anotatörle karara bağlanmış 70 kaydın hükmü desenin
            # üstündedir, yoksa bu betik bir sonraki koşuda onları siler
            # (K97'nin aynı tuzağı). Tanımın tek evi: `src/olcu_ozerklik.py`.
            if r["gen_meta"].get("ozerklik_kaynak"):
                olculen = bool(r["gen_meta"]["ozerklik_vurgusu"])
            r["gen_meta"]["ozerklik_vurgusu"] = olculen     # ⭐ ÖLÇÜLEN yazılır
            r["gen_meta"]["izgara_ozerklik"] = izgara       # ⭐ tasarım ayrıca durur
            # ⛔⛔ İLK SÜRÜM YANLIŞTI ve ölçümde çürüdü: yalnız red DESENİNE
            # bakınca 49 kaydın 18'i «red» çıktı (ızgara 7 diyor) ve `#9` ters
            # yöne döndü. Bakınca desenin ÜÇ ayrı edimi karıştırdığı görüldü:
            #   (a) RED        — istenen bir şeyi yapmama  («şu sayıyı söyleyemem»)
            #   (b) ROL SINIRI — ne olmadığını söyleme     («benim işim değil»)
            #   (c) BİLGİ SINIRI — bilmediğini söyleme     («belgede yazmıyor»)
            # K16'nın `is_negative`'i (a)'dır. Ayırt eden şey desende değil
            # BAĞLAMDA: red bir TALEP gerektirir. ⇒ Kullanıcı turunda bir istek
            # (soru işareti ya da emir kipi) aranıyor.
            # ➡️ *Bir edimi sözcüğünden tanımaya çalışmak, o edimi tanımlayan
            #    şeyin sözcük olmadığı yerde başarısız olur.*
            kul = " ".join(m["content"] for m in r["messages"] if m["role"] == "user")
            talep = bool(re.search(r"\?|\bsöyle\b|\bsöyler misin\b|\bne yapayım\b|"
                                   r"\bnasıl\b.*\bolur\b|\bolur mu\b|\bmı\b\s*$",
                                   kul, re.I | re.M))
            n_olc = (bool(RED.search(son)) and talep) or "is_negative" in onayli
            n_izg = bool(plan[s]["is_negative"])
            if n_izg and not n_olc:
                eksik.append(f"{s}(red)")
            # ⛔⛔⛔ BU SATIR 2026-09-21'DE KALDIRILDI (T227) ve sebebi ölçüldü:
            #     r["is_negative"] = n_olc
            # Desen, ateşlediği 70 kaydın 26'sında ötekiyle ayrışıyordu; 26'sı üç
            # anotatörle karara bağlandı ve **22'sinde desen FAZLA saymıştı** —
            # ateşleyen cümle rol sınırı ya da bilgi sınırıydı, geri çevrilen bir
            # istek yoktu. Dahası, desenin hiç ateşlemediği 7 kontrol kaydının
            # ortalama 5,7'sinde anotatörler red gördü ⇒ desen AZ da sayıyor.
            # ➡️ *Sözlük iki yönde birden yanlış ve onarılamaz: şablondan kaçınmak
            #    için red cümlesi her seferinde başka türlü kuruluyor (T218).*
            # ⇒ `is_negative` artık bir BEYAN; bu betik onu YAZMAZ, yalnız
            #   ayrıştığı yerleri OKUMA KUYRUĞUNA alır. Tanımın tek evi:
            #   `src/olcu_red.py`.
            if n_olc != r.get("is_negative"):
                oku_kuyrugu.append((s, bool(r.get("is_negative")), n_olc))
            r["gen_meta"]["izgara_negatif"] = n_izg
            satir.append((s, izgara, olculen))
        f.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kayitlar),
                     encoding="utf-8")
        kayitlar_tum += kayitlar

    n = len(satir)
    red_olc = red_izg = 0
    for f in sorted(KOK.glob(f"data/candidates/{PARTI}.blok*.jsonl")):
        for l in f.read_text(encoding="utf-8").splitlines():
            if l.strip():
                r = json.loads(l)
                red_olc += bool(r.get("is_negative"))
                red_izg += bool(r["gen_meta"].get("izgara_negatif"))
    olc = sum(1 for _, _, o in satir if o)
    izg = sum(1 for _, i, _ in satir if i)
    sat = [f"# `ozerklik_vurgusu` — beyan metinden yeniden ölçüldü", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Kapsam:** üretilmiş **{n}** kayıt (`{PARTI}` blokları)", "",
           "⭐ v4 §5a: *«beyan, yapılan hamlenin kaydıdır, niyetinin değil»*. Izgara bir "
           "TASARIM, `gen_meta` bir KAYIT — beyanı tasarımdan kopyalamak kaydı niyete "
           "eşitlemek olurdu.", "",
           "| | |", "|---|---:|",
           f"| ızgaranın özerklik dediği satır | {izg} |",
           f"| ⭐ **metinde ÖLÇÜLEN** | **{olc}** (%{100*olc//max(1,n)}) |",
           f"| ⭐ metinde ölçülen **red** | **{sum(1 for r in [0] for _ in [0] if False) or ''}"
           f"{sum(1 for x in satir if x)}".replace(str(len(satir)), "") +
           f"{sum(1 for _, _, _ in satir if False) or ''}" +
           f"{red_olc}** (ızgara: {red_izg}) |",
           f"| beyanı düzeltilen kayıt | **{len(degisen)}** |",
           f"| ⛔ ızgara 1 diyor ama metinde yok | {len(eksik) or '**0**'} |", "",
           (f"⛔ **Eksik satırlar: {eksik}**" if eksik else
            "⭐ **Izgaranın istediği her yerde özerklik cümlesi var** — blok betiklerinin "
            "kapısı bunu zaten koşuyordu."), "",
           f"⭐⭐ **Ölçülen oran %{100*olc//max(1,n)}**, §5a'nın hedefi ~%20 "
           f"*(hedef «bu benim önerim» olarak işaretli, literatürden değil)*. "
           + ("Hedefin üstünde." if 100*olc/max(1,n) > 20 else "Hedefin altında."), "",
           "## Beyanı düzeltilen kayıtlar", "", "| # | eskiden | **şimdi** |",
           "|---|---|---|"]
    sat += [f"| {s} | {e} | **{y}** |" for s, e, y in sorted(degisen)]
    # ⭐⭐ T227: `is_negative` ARTIK YAZILMIYOR. Desenin beyanla ayrıştığı yerler
    # yalnız okuma kuyruğuna alınıyor; alanı değiştiren tek şey üreticinin beyanı
    # ya da kayda yazılmış bir uzlaştırma kararı (`gen_meta.is_negative_kaynak`).
    sat += ["", "## `is_negative` — okuma kuyruğu (YAZILMADI)", "",
            "⛔ Desen ile beyan aşağıdaki kayıtlarda ayrılıyor. Bu bir düzeltme "
            "listesi DEĞİL: T227'de ölçüldüğü üzere desen iki yönde birden "
            "yanlış (ateşlediği 70 kaydın 26'sında fazla, ateşlemediği 7 kontrol "
            "kaydının 5,7'sinde az saydı). Tanımın tek evi `src/olcu_red.py`.", ""]
    if oku_kuyrugu:
        sat += ["| # | beyan | desen |", "|---|:-:|:-:|"]
        sat += [f"| {s} | {'red' if b else '—'} | {'red' if d else '—'} |"
                for s, b, d in sorted(oku_kuyrugu)]
    else:
        sat.append("Ayrışma yok.")
    sat += ["", "## ⛔ Bu düzeltmenin söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **`is_negative` ARTIK BU BETİKTE YAZILMIYOR (T227)** | üç "
            "anotatörle karara bağlanan 26 ayrışmanın 22'sinde desen fazla "
            "saymıştı; alan bir ÖLÇÜM değil BEYAN |",
            "| ⛔⛔ **Desen bir ÖLÇÜT DEĞİL, sonda** | özerklik cümlesi sözlükle "
            "aranıyor; bu depoda mekanik kuralın Türkçe serbest metinde tavana vurduğu "
            "yedi örnek var ⇒ ölçülen oran bir **alt sınır** |",
            "| ⛔ **Izgara DEĞİŞTİRİLMEDİ** | plan dondurulmuş (Kural 2); değişen yalnız "
            "kaydın beyanı, tasarım `izgara_ozerklik`te duruyor |",
            "| ⚠️ **Ters yön eksik sayılmaz** | metinde var ızgarada yok ⇒ §5a özerkliği "
            "hedef sayıyor, tavan değil |", ""]
    # ⛔⛔⛔ SIRA KAPISI (2026-09-21, ikinci hâl). Bu betik düzeltmeyi BLOK
    # dosyalarına yazıyor; korpusa giden `data/candidates/<parti>.jsonl` ise
    # birleştirme betiğinin ürünü. parti5'te birleştirme ÖNCE koştu ⇒ üç
    # düzeltme (#4 #15 #17) bloklara yazıldı, korpus dosyasında 0 kaldı.
    # ⛔ İLK HÂLİ YETMEDİ: kapı `degisen`e bakıyordu, oysa ikinci koşuda
    # `degisen` boş olur (düzeltme zaten yazılmıştır) ve rapor kapısı daha
    # erken `return 0` ediyordu ⇒ bayat dosya ikinci koşuda GÖRÜNMEZ oldu.
    # Sınandı ve görüldü; kapı artık `degisen`e değil, iki dosyanın KENDİSİNE
    # bakıyor ve rapor kapısından ÖNCE çalışıyor.
    # ➡️⭐⭐ *İki betik aynı veriyi farklı dosyalara yazıyorsa aralarındaki sıra
    #    bir kapı olmalıdır — ve o kapı, düzeltmenin yapıldığı koşuya değil,
    #    dosyaların o anki hâline bakmalıdır; yoksa yalnız bir kez görür.*
    birlesik = KOK / f"data/candidates/{PARTI}.jsonl"
    if birlesik.exists():
        bir = {json.loads(l)["gen_meta"]["parti_sira"]: json.loads(l)
               for l in birlesik.read_text(encoding="utf-8").splitlines() if l.strip()}
        bayat = sorted(r["gen_meta"]["parti_sira"] for r in kayitlar_tum
                       if r["gen_meta"]["parti_sira"] in bir
                       and bool(bir[r["gen_meta"]["parti_sira"]]["is_negative"])
                       is not bool(r["is_negative"]))
        if bayat:
            print(f"⛔⛔ {birlesik.name} BAYAT: {len(bayat)} kaydın `is_negative` "
                  f"değeri blok dosyalarıyla uyuşmuyor "
                  f"({', '.join('#' + str(x) for x in bayat)}).\n"
                  f"   Birleştirme bu betikten SONRA koşmalı:\n"
                  f"   uv run python scripts/analiz/2026-09-20-v6-parti2-birlestir.py "
                  f"--partiler={PARTI}")
            return 1
    if RAPOR.exists() and not degisen:
        print(f"⛔ {RAPOR.name} DURUYOR ve bu koşu 0 düzeltme buldu.\n"
              "   Düzeltmeler aday dosyalara yazılıyor ⇒ ikinci koşu hep 0 bulur.\n"
              "   Üstüne yazmak ilk koşunun kaydını siler. Yazılmadı.")
        return 0
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[4:]))

    return 1 if eksik else 0


if __name__ == "__main__":
    raise SystemExit(main())
