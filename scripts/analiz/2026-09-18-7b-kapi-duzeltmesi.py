#!/usr/bin/env python3
"""§7b düzeltmesinin iki parçası — sınanıyor ve bedeli ölçülüyor.

T149 iki parçalı bir düzeltme önermişti ve *«tek parçası zarar verir»* demişti:
  **(a)** sürüm koşulu `startswith("uretim-v3")` → *«v3 VE SONRASI»* (sayı karşılaştırması)
  **(b)** `KLINIK_IDDIA` klinik **AD** ile klinik **YÜKLEM**'i ayırsın; ad izleri
      inceleme kuyruğuna gitsin, kapıyı yalnız yüklem kapatsın

⭐ **(b) yeni bir sözlük UYDURMUYOR.** Deponun kendi verdiği bir karar aynen
uygulanıyor: `rol_siniri` sert kapı DEĞİL, çünkü *«"teşhis" gibi kelimeler modelin
DOĞRU reddi içinde de geçiyor — kelime taraması bağlamı ayırt edemiyor»*
(2026-09-12 register sondası). §7b-2'nin ad yarısı tam olarak aynı durumda:
118 benzersiz bağlam pasajının 7'si takılıyordu ve **yedisi de çıplak ad**.

⚠️ **Olumsuzluk bir muafiyet DEĞİL** ve kasten öyle yazılmadı: *«Bu ilaç bağımlılık
YAPMAZ»* olumsuzdur ama bir klinik iddiadır ve yakalanmalıdır. T142'nin dersi
(olumsuzluk desenini genişletmek muafiyeti sessizce büyütür) burada baştan
uygulandı — ayrım olumsuzlukta değil, **ad/yüklem** ayrımında.

Üç sınama, üçü de geçmeden düzeltme yayımlanamaz:
  1. **Birleşik desen korundu mu** — dört analiz betiği `KLINIK_IDDIA`'yı içe
     aktarıyor; birleşimin eski desenle AYNI eşleşmeleri vermesi gerekir (K97).
  2. **Regresyon** — yakalanması gereken iddialar hâlâ yakalanıyor mu, geçmesi
     gereken yordam cümleleri geçiyor mu.
  3. **Bedel** — `HEAD`'deki `run_checks` ile yeni hâli bütün korpuslarda
     karşılaştırılır; `passed` değeri değişen her kayıt tek tek listelenir.

Girdi : datasets/v*/train.jsonl · data/candidates/*.jsonl
Çıktı : reports/analiz/2026-09-18-7b-kapi-duzeltmesi.md
Kullanım: uv run python scripts/analiz/2026-09-18-7b-kapi-duzeltmesi.py
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-7b-kapi-duzeltmesi.md"

import checks as C  # noqa: E402

# ⭐ YAKALANMALI — gerçek klinik iddialar. Hepsi ELLE yazıldı ve hiçbiri korpustan
# alınmadı; korpustan alınsaydı sınama kendi kurulum kümesinde koşmuş olurdu.
# ⚠️ 2. ve 5. vaka OLUMSUZ: olumsuzluk bir muafiyet olsaydı ikisi de kaçardı.
YAKALANMALI = [
    ("etki iddiası", "Bu program bağımlılığı iyileştirir."),
    ("⭐ OLUMSUZ ama iddia", "Bu ilaç bağımlılık yapmaz."),
    ("süre iddiası", "Yoksunluk belirtileri üç gün içinde geçer."),
    ("⭐ OLUMSUZ ama iddia", "Bu yöntem zararlı değildir."),
    ("etkililik iddiası", "Grup terapisi bireysel görüşmeden daha etkilidir."),
]
# ⛔⛔ BİLİNEN BOŞLUK — yakalanması GEREKEN ama desenin yakalamadığı iddialar.
# ⚠️ Bu boşluk `HEAD`'de de var (doğrulandı) ⇒ bu düzeltmenin ürünü DEĞİL. Yüklem
# desenleri çekimsiz biçimlere bağlı: *«riski azalır»* yakalanıyor, *«riskini
# azaltır»* yakalanmıyor. ⛔ Bilerek bu değişikliğe KARIŞTIRILMADI: desenleri
# genişletmek bir SERT kapıyı genişletmektir ve kendi yanlış pozitif ölçümünü
# gerektirir. ➡️ *Her gerekçe ayrı yazılır; iki düzeltme tek yamada birleşirse
# hangisinin ne yaptığı sorulamaz.* ⇒ Boşluk sınamada GÖRÜNÜR duruyor.
# ⭐ 2026-09-18: İKİSİ KAPATILDI, İKİSİ AÇIK KALDI — ve ayrım ölçümden geldi.
# `riski\w*` + `etki ed\w*` genişletmesi 28.084 metinlik havuzda **0 fark** verdi
# ⇒ açıldı. SÜRE dalı bağlam pasajında bedava ama serbest metinde **49 yanlış
# pozitif** ürettiği için ⛔ AÇILMADI.
BILINEN_BOSLUK = [
    ("⭐ KAPANDI: «riskini azaltır»", "Bırakmak kalp riskini azaltır."),
    ("⭐ KAPANDI: «etki ediyor»", "Bu madde uykuya etki ediyor."),
    ("⛔ AÇIK: «ay sürüyor» — serbest metinde 49 YP", "Yoksunluk iki ay sürüyor."),
    ("⛔ AÇIK: «haftada geçer» — serbest metinde 49 YP", "Belirtiler üç haftada geçer."),
]
# ⭐ GEÇMELİ — §7b'nin KENDİ izin verdiği kategoriler: yordam / erişim / gizlilik /
# uygunluk / sınır. İlk beşi korpustan (bilinen yanlış pozitifler), son ikisi elle.
GECMELI = [
    ("feragat", "Araç bir tarama aracıdır ve tanı koymaz."),
    ("uygunluk", "Programa katılmak için konulmuş bir tanı aranmaz; başvuru kişinin kendi isteğiyle yapılır."),
    ("birim adı", "Gündüz tedavi ünitelerinde geceleme yapılmaz; ünite kapanış saatinde kapanır."),
    ("yordam", "Nöbetçi eczaneler gece boyunca açıktır. Reçeteli ilaçlar için reçete aranır."),
    ("yordam", "Gebelik planlayan kişilerde ilaçların gözden geçirilmesi reçete eden hekimle birlikte yapılır."),
    ("gizlilik", "Yanıtlar oturum kapandığında cihazda saklanmaz ve üçüncü kişilerle paylaşılmaz."),
    ("⭐ süre AD'ı, fiil değil", "Ödünç alınan materyal iki hafta süreyle kullanılabilir."),
    ("⭐ kullanıcının geçen zamanı", "Altı ay geçti düğünden, hâlâ kullanıyorum."),
    ("sınır", "Görüşmeler arasında verilen bir ödev yükümlülüğü yoktur."),
]


def _head_checks():
    """`HEAD`'deki `checks.py` — `src/` içinde açılmalı: `FILTERS` yolu
    `Path(__file__).parent.parent`'tan türüyor (T147'nin ders verdiği bağımlılık)."""
    g = subprocess.run(["git", "show", "HEAD:src/checks.py"], cwd=KOK,
                       capture_output=True, text=True)
    if g.returncode != 0:
        return None, None
    t = KOK / "src" / "checks_head_denklik.py"
    t.write_text(g.stdout, encoding="utf-8")
    sp = importlib.util.spec_from_file_location("checks_head", t)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m, t


def _metinler() -> list[str]:
    """Desen denkliği için GENİŞ metin havuzu: bağlam pasajları + asistan cevapları."""
    out = []
    for p in sorted(KOK.glob("data/candidates/*.jsonl")) + sorted(KOK.glob("datasets/v*/train.jsonl")):
        for satir in p.read_text(encoding="utf-8").splitlines():
            if not satir.strip():
                continue
            r = json.loads(satir)
            out += [(k.get("metin") or "") for k in (r.get("context") or []) if isinstance(k, dict)]
            out += [m.get("content") or "" for m in r.get("messages", [])]
    return [x for x in out if x]


def _kayitlar():
    for p in sorted(KOK.glob("datasets/v*/train.jsonl")) + sorted(KOK.glob("data/candidates/*.jsonl")):
        for satir in p.read_text(encoding="utf-8").splitlines():
            if satir.strip():
                yield p, json.loads(satir)


def main() -> int:
    eski, gecici = _head_checks()
    sat = ["# §7b düzeltmesi — iki parça, üç sınama", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}", "",
           "T149: *«düzeltmenin tek parçası zarar verir»*. İki parça birlikte yazıldı:", "",
           "| parça | ne değişti |", "|---|---|",
           "| **(a)** | `startswith(\"uretim-v3\")` → `uretim_surumu(record) >= 3` "
           "(sürüm bir SAYIDIR; önek karşılaştırmak sayı karşılaştırmak değildir) |",
           "| **(b)** | `KLINIK_IDDIA` ikiye ayrıldı: `KLINIK_YUKLEM` kapıyı kapatır, "
           "`KLINIK_AD` **inceleme kuyruğuna** gider (`rol_siniri` emsali) |", "",
           "⚠️ **Olumsuzluk bir muafiyet olarak YAZILMADI.** *«Bu ilaç bağımlılık YAPMAZ»*",
           "olumsuzdur ama klinik iddiadır. T142'nin dersi baştan uygulandı: ayrım",
           "olumsuzlukta değil, **ad/yüklem** ayrımında.", ""]

    # --- 1. birleşik desen korundu mu
    havuz = _metinler()
    fark = 0
    if eski:
        for t in havuz:
            a = sorted({m.group(0) for m in eski.KLINIK_IDDIA.finditer(C.i_sinifi(t))})
            b = sorted({m.group(0) for m in C.KLINIK_IDDIA.finditer(C.i_sinifi(t))})
            fark += a != b
    sat += ["## 1. ⭐ Birleşik desen korundu mu?", "",
            f"Dört analiz betiği `KLINIK_IDDIA`'yı içe aktarıyor; sayıları değişmemeli (K97).",
            f"`HEAD` deseni ile yeni birleşim **{len(havuz)}** metin parçasında karşılaştırıldı.", "",
            (f"⭐ **Eşleşmeler birebir aynı** ({len(havuz)}/{len(havuz)}) ⇒ içe aktaran "
             "betiklerin sayıları değişmez." if not fark else
             f"⛔⛔ **{fark} metinde eşleşme FARKLI** — birleşim eski deseni korumuyor."), ""]

    # --- 2. regresyon
    sat += ["## 2. ⭐ Regresyon — yakalanması gereken yakalanıyor mu?", "",
            "⚠️ Vakalar **elle** yazıldı; korpustan alınsalardı sınama kendi kurulum",
            "kümesinde koşmuş olurdu.", "",
            "| beklenti | vaka | `KLINIK_YUKLEM` | sonuç |", "|---|---|---|---|"]
    hata = 0
    for ad, metin in YAKALANMALI:
        y = bool(C.KLINIK_YUKLEM.search(C.i_sinifi(metin)))
        hata += not y
        sat.append(f"| ⛔ yakalanmalı ({ad}) | {metin} | {'✅ ateşledi' if y else '⛔ SESSİZ'} "
                   f"| {'✅' if y else '⛔ **SAPMA**'} |")
    for ad, metin in GECMELI:
        y = bool(C.KLINIK_YUKLEM.search(C.i_sinifi(metin)))
        a_ = sorted({m.group(0) for m in C.KLINIK_AD.finditer(C.i_sinifi(metin))})
        hata += y
        sat.append(f"| ⭐ geçmeli ({ad}) | {metin[:70]} | {'⛔ ATEŞLEDİ' if y else '✅ sessiz'} "
                   f"| {'⛔ **SAPMA**' if y else '✅'}{' · ad izi: ' + str(a_) if a_ else ''} |")
    sat += ["", (f"⭐ **{len(YAKALANMALI)+len(GECMELI)} vakanın hepsi beklendiği gibi.**"
                 if not hata else f"⛔⛔ **{hata} vaka sapıyor — düzeltme yayımlanamaz.**"), "",
            "### ⛔⛔ Bilinen boşluk — bu düzeltmenin KAPATMADIĞI", "",
            "Yüklem desenleri çekimsiz biçimlere bağlı. ⚠️ Boşluk `HEAD`'de de var ⇒ bu",
            "düzeltmenin ürünü değil; bilerek karıştırılmadı, çünkü desen genişletmek bir",
            "**sert kapıyı** genişletmektir ve kendi yanlış pozitif ölçümünü gerektirir.", "",
            "| boşluk | vaka | şimdi |", "|---|---|---|"]
    for ad, metin in BILINEN_BOSLUK:
        y = bool(C.KLINIK_YUKLEM.search(C.i_sinifi(metin)))
        sat.append(f"| {ad} | {metin} | {'⭐ artık yakalanıyor' if y else '⛔ kaçıyor'} |")
    kacan = sum(1 for _, m in BILINEN_BOSLUK if not C.KLINIK_YUKLEM.search(C.i_sinifi(m)))
    sat += ["", f"➡️ **{kacan}/{len(BILINEN_BOSLUK)}** hâlâ kaçıyor ve bu **ilan edilmiş** bir "
            "boşluktur — *«yakalanmadı»* ile *«yok»* karıştırılmasın.", ""]

    # --- 3. bedel
    donen, izli, toplam = [], set(), 0
    if eski:
        for p, r in _kayitlar():
            toplam += 1
            a = eski.run_checks(r).get("passed")
            y = C.run_checks(r)
            if y.get("context_klinik_ad_izi"):
                izli.add(r.get("id"))
            if a != y.get("passed"):
                donen.append({"dosya": str(p.relative_to(KOK)), "id": r.get("id"),
                              "once": a, "sonra": y.get("passed"),
                              "sebep": y.get("context_error") or "?",
                              "surum": str((r.get("gen_meta") or {}).get("prompt_version"))})
    tekil = {d["id"] for d in donen}
    sat += ["## 3. ⛔ Bedel — hangi kayıtların kararı döndü?", "",
            f"`HEAD` `run_checks` ile yeni hâli **{toplam}** kayıtta karşılaştırıldı.", "",
            "| | |", "|---|---|",
            f"| kararı DÖNEN kayıt | **{len(tekil)} tekil** ({len(donen)} satır, sürüm kopyaları dahil) |",
            f"| ⭐ klinik AD izi raporlanan (inceleme kuyruğu) | **{len(izli)} tekil kayıt** |", ""]
    if donen:
        sat += ["| dosya | kayıt | önce → sonra | sürüm | sebep |", "|---|---|---|---|---|"]
        for d in donen[:20]:
            sat.append(f"| `{d['dosya']}` | `{str(d['id'])[:10]}` | {d['once']} → "
                       f"**{d['sonra']}** | `{d['surum']}` | {str(d['sebep'])[:70]} |")
        if len(donen) > 20:
            sat.append(f"| … | {len(donen)-20} satır daha | | | |")
        sat.append("")
    else:
        sat += ["⭐⭐ **Hiçbir kaydın kararı dönmedi.** ⇒ (a) kapıyı 4404 kayıtta açtı ve",
                "(b) o kapının bilinen yanlış pozitif sınıfını kapattı; ikisi birlikte",
                "veri setine **dokunmadan** kapıyı çalışır hâle getirdi.", "",
                "➡️⭐⭐ *T149'un öngörüsü ölçümle doğrulandı: tek parça 6 doğru kaydı",
                "düşürecekti, iki parça birlikte 0 kayıt düşürüyor.*", ""]

    sat += ["## ⛔ Bu düzeltmenin söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **Kapı artık ADLARA bakmıyor** | *«tedavi», «tanı», «ilaç»* geçen bir pasaj "
            "kapıyı kapatmaz; yalnız raporlanır. Gerçek bir iddia AD ile kurulmuşsa "
            "(*«Bu tanı kesindir»*) kapı görmez ⇒ ad izleri kuyruğu **okunmalı** |",
            "| ⛔ **İnceleme kuyruğunu okuyan yok** | `context_klinik_ad_izi` alanı yazılıyor "
            "ama onu tüketen bir betik henüz yazılmadı — `rol_siniri`'nin durumunun aynısı |",
            "| ⛔ **Sürümsüz kayıtlar hâlâ kapsam dışı** | `dikey-dilim-v1` ve "
            "`prompt_version` taşımayan 224 kayıt için §7b yine kapalı; bu bir TASARIM "
            "kararıydı ve bu düzeltme onu değiştirmiyor |",
            "| ⚠️ **«0 kayıt düştü» korpusa bağlıdır** | kapı kapalıyken üretilen bir korpusta "
            "üretici §7b'den geri bildirim almadı; sayı bugünün verisi için geçerli |",
            "| ⚠️ Regresyon vakaları elle yazıldı (K30) | kapının genelleme gücü değil, "
            "ilan edilen iki sınıfta tutarlılığı sınandı |",
            "| ⛔⛔ **Yüklem desenleri çekime kapalı** | *«riskini azaltır»*, *«iki ay sürüyor»*, "
            "*«etki ediyor»* kaçıyor. `HEAD`'de de kaçıyordu ⇒ bu düzeltmenin ürünü değil, "
            "ama artık **ölçülü ve ilan edilmiş** bir boşluk |", ""]

    if gecici:
        gecici.unlink(missing_ok=True)
    (KOK / f"reports/analiz/{TARIH}-7b-kapi-duzeltmesi.json").write_text(
        json.dumps({"tarih": TARIH, "desen_farki": fark, "regresyon_hatasi": hata,
                    "donen": donen, "ad_izli_kayit": len(izli), "kayit": toplam},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[:1] + sat[13:]))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 1 if (fark or hata) else 0


if __name__ == "__main__":
    raise SystemExit(main())
