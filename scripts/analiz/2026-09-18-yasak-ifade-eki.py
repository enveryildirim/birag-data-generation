#!/usr/bin/env python3
"""§15 yasak ifade taramasında EK kusuru — sınama ve bedel ölçümü.

⛔⛔ **Kusuru inceleme kuyruğu buldu.** Kuyruk 2026-09-12'den beri okunmamıştı;
okunur okunmaz `bos_guvence` altında şu satır çıktı: *«…sayıyı yine de merak
ETMEK bunları geçersiz kılmıyor»* — yani bir boş güvence DEĞİL, tam tersi.
Sebep düz alt dizge araması: *«merak etme»* (olumsuz emir), *«merak etmek»*in
(mastar) içinde eşleşiyor. ➡️ *Okunmayan bir sinyal, sinyal değildir — ve
okunmadığı sürece onu üreten kusur da görünmez.*

⭐ **Düzeltme ifadenin BİÇİMİNE bağlı** (T142/T150 ailesi):
  · **tek sözcük** (*«doz»*, *«teşhis»*) — yalnız **AD ÇEKİM EKİ** alabilir;
    *«dozu»* aynı sözcüktür ama *«keşke»* *«keş»*in çekimi DEĞİLDİR
  · **çok sözcüklü** (*«merak etme»*) — son öge fiil çekimidir, ek aldığında kip
    değişir ⇒ sözcük sınırında bitmeli

⛔⛔ **«Ek serbest» ilk yazımda çok genişti ve ikinci ölçüm onu yakaladı.** Tek
sözcükte eki tamamen serbest bırakmak *«keş»*i *«keşke»*ye bağlıyordu — ve tuzak
canlı: *«keşke»* kullanıcı turlarında **9**, asistan `thinking`'inde **9** kez
geçiyor. ⇒ Kapalı çekim eki listesi (`tohum_guvenlik.AD_CEKIM_EKI`) kullanılıyor;
liste mekân kapısında T122 için ölçülmüştü ve iki yerde iki tanım olmasın diye
(K97) ortak modüle taşındı — mekân kapısının bulgusu birebir aynı kaldı (4 → 4).

⛔⛔ **SERT KATEGORİ BİLEREK DIŞARIDA — Kural 3.** `kriz_yasagi`'da durum daha ağır
ve ters yönde: *«bana söz ver»* ifadesi *«Senden bana söz VERMENİ istemiyorum»*
cümlesini de düşürüyor — kapı, kendi kuralını uygulayan cümleyi siliyor. ⚠️ Ama
sözcük sınırı oraya uygulanırsa *«bana söz verir misin»* KAÇAR ⇒ güvenlik
ekseninde yanlış negatif. *«Güvenlik ekseninde gerileme kabul edilebilir
değildir»* (Kural 3) ⇒ sert kategori AYNEN korundu; doğru çözüm ifade listesini
düzeltmektir ve o bir **uzman kararıdır**.

Girdi : datasets/v*/train.jsonl · data/candidates/*.jsonl
Çıktı : reports/analiz/2026-09-18-yasak-ifade-eki.md
Kullanım: uv run python scripts/analiz/2026-09-18-yasak-ifade-eki.py
"""
from __future__ import annotations

import collections
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-yasak-ifade-eki.md"

import checks as C  # noqa: E402

# (beklenti, açıklama, cümle) — beklenti: yakalanmalı mı?
VAKA = [
    (True, "gerçek boş güvence", "Merak etme, her şey yoluna girecek."),
    (False, "⭐ mastar — kip başka", "Sayıyı merak etmek bunları geçersiz kılmıyor."),
    (False, "⭐ zarf-fiil — kip başka", "Sayıyı merak etmeden önce fark etmişsin."),
    (True, "tek sözcük + Türkçe ek", "Dozu azaltan hekim bunu bilir."),
    (True, "tek sözcük, çekimsiz", "Teşhis koymak benim işim değil."),
    (True, "çok sözcüklü, sınırda biter", "Bunu herkes yapıyor zaten."),
    (True, "etiketleme", "Sen bağımlısın."),
    (False, "⭐⭐ «keş» ≠ «keşke» — çekim değil, başka sözcük",
     '"Keşke kavga etseydik" cümlesinin altında kavga isteği yok.'),
    (True, "tek sözcük + iyelik eki", "Dozun eskisi gibi işlememesi başka bir şey."),
]
# ⛔ SERT kategori — DEĞİŞMEMESİ beklenen davranış (Kural 3 tutması)
SERT_VAKA = [
    (True, "gerçek ihlal", "Bana söz ver, bir daha içmeyeceksin."),
    (True, "⛔⛔ DOĞRU REDDİ DE DÜŞÜRÜYOR", "Senden bana söz vermeni istemiyorum."),
    (True, "⛔ aktarım da düşüyor", "Bana söz verdiğini söyledin."),
]


def _head_checks():
    g = subprocess.run(["git", "show", "HEAD:src/checks.py"], cwd=KOK,
                       capture_output=True, text=True)
    if g.returncode != 0:
        return None, None
    t = KOK / "src" / "checks_head_ek.py"
    t.write_text(g.stdout, encoding="utf-8")
    sp = importlib.util.spec_from_file_location("checks_head_ek", t)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m, t


def _kayitlar():
    for p in sorted(KOK.glob("datasets/v*/train.jsonl")) + sorted(KOK.glob("data/candidates/*.jsonl")):
        for satir in p.read_text(encoding="utf-8").splitlines():
            if satir.strip():
                yield p, json.loads(satir)


def main() -> int:
    eski, gecici = _head_checks()
    sat = ["# §15 yasak ifade taramasında ek kusuru", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}", "",
           "⛔⛔ **Kusuru inceleme kuyruğu buldu** — 2026-09-12'den beri okunmamış kuyruk.",
           "`bos_guvence` altında çıkan satır bir boş güvence değil, tam tersiydi:",
           "*«…sayıyı yine de merak ETMEK bunları geçersiz kılmıyor»*. Sebep düz alt dizge",
           "araması: *«merak etme»* (olumsuz emir), *«merak etmek»*in (mastar) içinde.", "",
           "➡️⭐⭐ *Okunmayan bir sinyal, sinyal değildir — ve okunmadığı sürece onu üreten",
           "kusur da görünmez.*", "",
           "## 1. ⭐ Regresyon — yumuşak kategoriler", "",
           "| beklenti | vaka | cümle | sonuç |", "|---|---|---|---|"]
    hata = 0
    for bekle, ad, metin in VAKA:
        h = {k: v for k, v in C.scan_forbidden(metin).items() if k not in C.SERT_KATEGORILER}
        ok = bool(h) == bekle
        hata += not ok
        sat.append(f"| {'⛔ yakalanmalı' if bekle else '⭐ geçmeli'} ({ad}) | {metin} | "
                   f"`{json.dumps(h, ensure_ascii=False) if h else '—'}` | "
                   f"{'✅' if ok else '⛔ **SAPMA**'} |")
    sat += ["", (f"⭐ **{len(VAKA)} vakanın hepsi beklendiği gibi.**" if not hata
                 else f"⛔⛔ **{hata} vaka sapıyor.**"), "",
            "## 2. ⛔⛔ Sert kategori — DEĞİŞTİRİLMEDİ ve neden", "",
            "`kriz_yasagi`'da eşleşme aynen korundu. Aşağıdaki tablo kapının BUGÜNKÜ",
            "davranışını gösteriyor — üç cümlenin üçü de düşüyor, oysa yalnız biri ihlal:", "",
            "| vaka | cümle | kapı | doğru mu? |", "|---|---|---|---|"]
    for _, ad, metin in SERT_VAKA:
        h = {k: v for k, v in C.scan_forbidden(metin).items() if k in C.SERT_KATEGORILER}
        dogru = "gerçek ihlal" in ad
        sat.append(f"| {ad} | {metin} | {'⛔ düşürür' if h else '✅ geçer'} | "
                   f"{'✅ doğru' if dogru else '⛔ **YANLIŞ POZİTİF**'} |")
    sat += ["", "⚠️ **Sözcük sınırı kuralı buraya UYGULANMADI** çünkü uygulanırsa",
            "*«bana söz verir misin»* kaçar ⇒ güvenlik ekseninde **yanlış negatif** doğar.",
            "*«Güvenlik ekseninde gerileme kabul edilebilir değildir»* (Kural 3).", "",
            "➡️⛔⛔ **Doğru çözüm ifade listesini düzeltmektir ve o bir UZMAN KARARIDIR.**",
            "Bugünkü hâliyle kapı, *«Senden bana söz vermeni istemiyorum»* diyen — yani",
            "§15'in tam olarak istediğini yapan — bir kaydı **sessizce eler**. Korpusta",
            "böyle bir cümle bugün **yok** (ölçüldü: bütün korpuslarda `kriz_yasagi` 0 vuruş),",
            "ama kapı o cümle yazıldığı gün onu silmeye hazır bekliyor.", ""]

    # --- 3. bedel
    once, sonra = collections.Counter(), collections.Counter()
    donen, toplam = [], 0
    for p, r in _kayitlar():
        toplam += 1
        for m in r.get("messages", []):
            if m.get("role") != "assistant":
                continue
            t = m.get("content") or ""
            if eski:
                for k, v in eski.scan_forbidden(t).items():
                    once[k] += len(v)
            for k, v in C.scan_forbidden(t).items():
                sonra[k] += len(v)
        if eski and eski.run_checks(r).get("passed") != C.run_checks(r).get("passed"):
            donen.append({"dosya": str(p.relative_to(KOK)), "id": r.get("id")})
    sat += ["## 3. ⛔ Bedel", "", f"Bütün korpuslar · **{toplam}** kayıt.", "",
            "| kategori | önce | sonra | fark |", "|---|---:|---:|---:|"]
    for k in sorted(set(once) | set(sonra)):
        d = sonra[k] - once[k]
        im = "⭐ **yanlış pozitif düştü**" if d < 0 else ("·" if d == 0 else "⛔ arttı")
        sat.append(f"| `{k}` | {once[k]} | {sonra[k]} | {d:+d} {im} |")
    tekil = {d["id"] for d in donen}
    sat += ["", f"| `passed` değeri dönen kayıt | **{len(tekil)} tekil** |", "|---|---|", "",
            ("⭐⭐ **Hiçbir kaydın kararı dönmedi** — düzeltme yalnız YUMUŞAK kategorileri "
             "etkiledi, yani inceleme kuyruğunu temizledi, eleme davranışını değil. "
             "⚠️ Tek sözcük kuralının bugünkü bedeli **sıfır**, çünkü *«keşke»* asistan "
             "cevaplarında henüz hiç geçmiyor (kullanıcı turlarında 9, `thinking`'de 9). "
             "➡️ *Ölçülen bedelin sıfır olması, kuralın gereksiz olduğu anlamına gelmez: "
             "bazı düzeltmeler bugünü değil, tuzağın kurulduğu günü hedefler.*"
             if not tekil else
             f"⛔⛔ **{len(tekil)} kaydın kararı döndü** — yumuşak bir düzeltmenin elemeyi "
             "etkilememesi gerekirdi."), "",
            "## ⛔ Bu düzeltmenin söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Sert kapının yanlış pozitifi DURUYOR** | *«bana söz vermeni "
            "istemiyorum»* hâlâ düşer; Kural 3 gereği dokunulmadı, uzman kararı bekliyor |",
            "| ⭐ **Tek sözcük kuralı kapatıldı** | kök yalnız AD ÇEKİM EKİ alabilir; "
            "*«keş»* artık *«keşke»*ye bağlanmıyor. ⚠️ Ama ölçülen bedel **0**: tuzak "
            "henüz `content`te hiç ateşlememişti ⇒ bu bir ÖNLEYİCİ düzeltme, "
            "sayıya yansımıyor |",
            "| ⛔ **Fiil çekimi kapsam dışı** | liste AD çekimi için; *«geçecek»* → "
            "*«geçecekti»* eşleşmez. Çıplak biçim yine yakalanır, türemiş kip yakalanmaz |",
            "| ⚠️ **Liste sözlüğe bağlı** | `configs/filters.yaml`'da olmayan bir ihlal ne "
            "kapıya ne kuyruğa girer |", ""]

    if gecici:
        gecici.unlink(missing_ok=True)
    (KOK / f"reports/analiz/{TARIH}-yasak-ifade-eki.json").write_text(
        json.dumps({"tarih": TARIH, "regresyon_hatasi": hata, "once": dict(once),
                    "sonra": dict(sonra), "donen": donen, "kayit": toplam},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[10:]))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 1 if (hata or tekil) else 0


if __name__ == "__main__":
    raise SystemExit(main())
