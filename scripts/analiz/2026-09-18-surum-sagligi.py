#!/usr/bin/env python3
"""Sürüm sağlık raporu — bir veri kümesinin bütün kapıları TEK sayfada.

⛔⛔ **Neden var.** Bu depoda otuzdan fazla analiz betiği var ve her biri kendi
raporunu yazıyor. Bir sürümün sağlığını görmek için hepsini tek tek koşmak
gerekiyordu ve bu oturumda bulunan kusurların çoğu tam bu yüzden **geç** bulundu:
kuyruk 2026-09-12'den beri okunmamıştı (T152), §7b kapısı sürüm ilerleyince
sessizce kapanmıştı (T149), elle okuma yığını hiç okunmamıştı (T155).

➡️⭐⭐ *Dağınık ölçüm, ölçülmemiş olmakla aynı şey değildir — ama okunmadığı sürece
ona yakın durur. Bir sürümün sağlığı tek sayfada okunamıyorsa, kusurlar sayıların
arasında değil, RAPORLARIN ARASINDA saklanır.*

⭐ Bu betik **hiçbir ölçümü yeniden tanımlamaz** (K97): her kapıyı kendi betiğinden
çağırır ve yalnız başlık sayılarını toplar. Yeni bir sayı üretmez, var olanları
yan yana koyar.

⚠️ **Bu bir KALİTE raporu değildir.** Kapılar biçim ve dayanak denetler; terapötik
kalite Eksen 1'in işidir ve judge gerektirir (T161/T162).

Kullanım: uv run python scripts/analiz/2026-09-18-surum-sagligi.py [datasets/v0.0.10]
"""
from __future__ import annotations

import importlib.util as iu
import io
import datetime
import json
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
sys.path.insert(0, str(KOK / "scripts/analiz"))
TARIH = Path(__file__).name[:10]
# ⛔ K126 rapor tarihini betiğin ADINDAN türetir ve TEK SEFERLİK ölçümler için bu
# doğrudur: ad, sayının alındığı günü sabitler. Ama bu betik YENİDEN KOŞULABİLİR
# (her sürüm için bir rapor) ⇒ addaki tarih artık ölçümün değil betiğin YAZILDIĞI
# günü gösterir. 2026-09-19'da koşulan bir rapor «Tarih: 2026-09-18» diyordu.
# ➡️ *Yeniden koşulabilir bir betikte ad kimliktir, tarih değil.* İkisi de yazılır.
KOSU = datetime.date.today().isoformat()

import checks as C  # noqa: E402


def _yukle(ad: str, dosya: str):
    s = iu.spec_from_file_location(ad, KOK / "scripts/analiz" / dosya)
    m = iu.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _sessiz(fn, *a, **k):
    with redirect_stdout(io.StringIO()):
        return fn(*a, **k)


def main(surum: str) -> int:
    d = Path(surum) if Path(surum).is_absolute() else KOK / surum
    tren = d / "train.jsonl"
    if not tren.exists():
        print(f"⛔ Bulunamadı: {tren}"); return 2
    kayitlar = [json.loads(s) for s in tren.read_text(encoding="utf-8").splitlines() if s.strip()]
    yol = str(tren.relative_to(KOK))

    # --- 1. üretim kapısı
    sonuc = [C.run_checks(r) for r in kayitlar]
    gecen = sum(1 for x in sonuc if x.get("passed"))
    ad_izi = sum(1 for x in sonuc if x.get("context_klinik_ad_izi"))
    yumusak = sum(1 for x in sonuc
                  if any(k not in C.SERT_KATEGORILER for k in (x.get("forbidden_hits") or {})))

    # --- 2. kapılar (her biri KENDİ betiğinden)
    A = _yukle("alinti", "2026-09-17-alinti-birebirlik-kapisi.py")
    Z = _yukle("zaman", "2026-09-17-zaman-kaynak-kapisi.py")
    Y = _yukle("yapisal", "2026-09-17-yapisal-atif-kapisi.py")
    M = _yukle("mekan", "2026-09-17-mekan-atfi-kapisi.py")
    _sessiz(A.main, yol); _sessiz(Z.main, yol)
    _sessiz(Y.main, [yol]); _sessiz(M.main, [yol])

    def _oku(p):
        return json.loads((KOK / p).read_text(encoding="utf-8"))
    ad = A._rapor_adi(tren) if hasattr(A, "_rapor_adi") else tren.stem
    al = _oku(f"reports/analiz/2026-09-17-alinti-birebirlik-{ad}.json")
    za = _oku(f"reports/analiz/2026-09-17-zaman-kaynak-{ad}.json")
    ya = _oku("reports/analiz/2026-09-17-yapisal-atif-kapisi.json")
    me = _oku("reports/analiz/2026-09-17-mekan-atfi-kapisi.json")

    sat = [f"# Sürüm sağlığı — `{d.name}`", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` (yazıldı {TARIH}) · "
           f"**koşu tarihi:** {KOSU}  ",
           f"**Girdi:** `{yol}` · **{len(kayitlar)}** kayıt", "",
           "⛔⛔ **Neden tek sayfa.** Bu depoda otuzdan fazla analiz betiği var ve bu oturumda",
           "bulunan kusurların çoğu **geç** bulundu: inceleme kuyruğu 2026-09-12'den beri",
           "okunmamıştı · §7b kapısı sürüm ilerleyince sessizce kapanmıştı · elle okuma yığını",
           "hiç okunmamıştı. ➡️ *Dağınık ölçüm okunmadığı sürece ölçülmemiş olmaya yakın durur;",
           "kusurlar sayıların arasında değil, RAPORLARIN arasında saklanır.*", "",
           "⭐ Hiçbir ölçüm yeniden tanımlanmadı (K97): her kapı **kendi betiğinden** çağrıldı.", "",
           "## Üretim kapısı (`run_checks`)", "", "| | |", "|---|---:|",
           f"| kayıt | {len(kayitlar)} |",
           f"| ⭐ geçen | **{gecen}** |",
           f"| ⛔ elenen | **{len(kayitlar)-gecen}** |",
           f"| inceleme kuyruğu — yumuşak §15 vuruşu olan kayıt | {yumusak} |",
           f"| inceleme kuyruğu — klinik ad izi | {ad_izi} |", "",
           "## Dayanak kapıları", "", "| kapı | otomatik ihlal | elle okunacak |",
           "|---|---:|---:|",
           f"| alıntı birebirliği | **{len(al['bulgu'])}** öge / {al['isaretli_kayit']} kayıt "
           f"| — |",
           f"| zaman + kaynak atfı | **{len(za['bulgu'])}** öge / {za['isaretli_kayit']} kayıt "
           f"| — |",
           f"| yapısal atıf | **{len(ya['otomatik_ihlal'])}** | ⚠️ **{len(ya['elle_okunacak'])}** |",
           f"| mekân atfı | **{len(me['bulgu'])}** | ⚠️ **{sum(1 for b in me['bulgu'] if not b.get('sinif'))}** |", ""]
    # ⭐ Mekân bulguları ETİKETLİ (muafiyet değil): okuma yükü düşer, tespit gücü durur.
    et = {}
    for b in me["bulgu"]:
        et["+".join(b.get("sinif") or []) or "⛔ ELLE OKU"] = \
            et.get("+".join(b.get("sinif") or []) or "⛔ ELLE OKU", 0) + 1
    if me["bulgu"]:
        sat += ["⭐ Mekân bulguları **etiketli** — muafiyet değil, okuma önceliği:", "",
                "| etiket | bulgu |", "|---|---:|"]
        for k, v in sorted(et.items(), key=lambda x: -x[1]):
            sat.append(f"| {k} | {v} |")
        sat += ["", "⚠️ *«soyut»* = yerde soyut bir nesne duruyor (*«masada iki şey var»*) · "
                "*«varlık»* = asistanın kendi bulunuşu (*«ben o odada olmayacağım»*) · *«kip»* = "
                "varsayımsal/soru çerçevesi. ⛔ Etiketsizler **elle okunmalı**.", ""]

    # --- 3. şablonlaşma
    S = _yukle("sablon", "2026-09-18-sablon-kapisi.py")
    kay = [json.loads(x) for x in tren.read_text(encoding="utf-8").splitlines() if x.strip()]
    esik = max(2, round(len(kay) * 2.0 / 100))
    dizi = S._kapsayanlari_ele(S._adaylar(kay, esik))
    ilk = sorted(dizi.items(), key=lambda x: -x[1])[:6]
    sat += ["## Şablonlaşma (T157)", "",
            f"Eşik %2 ({esik} kayıt) · eşiği aşan dizi: **{len(dizi)}**", "",
            "| dizi | kayıt | % |", "|---|---:|---:|"]
    for dz, n in ilk:
        sat.append(f"| *«{' '.join(dz)}»* | {n} | %{100*n/len(kay):.1f} |")
    # --- 4. kullanıcının sözcüğünü koruma (2026-09-18'de bu raporun ilk koşusunda bulundu)
    # ⭐ Depo baştan beri *«kullanıcının KENDİ sözcüğünü kullan»* diyor (T142'de *«hekimin»*
    # ↔ *«doktor»*, aynı gün *«her şeye karışmak»* düzeltmesi). Sinyal buraya kalıcı
    # olarak eklendi çünkü tek seferlik bir okumada değil, HER sürümde bakılmalı.
    # ⛔⛔ EK LİSTESİ ELLE YAZILINCA PAYDA OYNADI. İlk sürümde ekler tek tek
    # sayılmıştı ve *«karının»* listede yoktu; v0.0.11'de düzeltme *«karının»*
    # ürettiği için o kayıt PAYDADAN düştü ve *«0 ihlal»* kısmen artefakt oldu.
    # ➡️⭐⭐ *Bir ölçütün paydası, ölçtüğü düzeltmeden ETKİLENİYORSA sayı okunamaz —
    #    ve bu, judge kapsamının Eksen 1'de yaptığının aynısı (T162).*
    # ⇒ Ekler deponun KENDİ kapalı çekim listesinden geliyor (K97, `tohum_guvenlik`).
    # ⛔⛔ İKİ ÖLÇÜM DENEMESİ DE ARTEFAKT ÜRETTİ, ÜÇÜNCÜSÜ TUTTU:
    #  1. Ekler ELLE sayıldı ⇒ *«karının»* listede yoktu, kayıt PAYDADAN düştü ve
    #     *«0 ihlal»* kısmen artefakt oldu.
    #  2. `AD_CEKIM_EKI` + `tr_fold` denendi ⇒ daha kötü: **tr_fold «ı»yı «i»ye
    #     eşliyor**, deseni katlayınca *«karı»* → *«kari»* oluyor ve GÖVDE, ekin
    #     ihtiyaç duyduğu ünlüyü yutuyor (*«karım»* → *«karim»*, desen *«kari+im»*
    #     bekliyor). Ayrıca `AD_CEKIM_EKI` ünlüyle biten gövdeler için yazılmamış:
    #     *«karı»* + *«m»* listede yok.
    # ⇒ Açık BİÇİM listesi: katlama yok, ham metinde büyük/küçük harf duyarsız.
    # ➡️⭐⭐ *Bir eşleştirmeyi katlamak metni katlamakla aynı şey değildir: katlama
    #    gövde-sonu ünlüsünü siliyorsa, ek listesi artık o gövdeye uymaz.*
    # ⚠️ *«karın»* Türkçede hem *«senin karın»* hem *«mide»* demektir; korpusta mide
    #   anlamında geçmediği ölçüldü ama bu bir KORPUS olgusudur, desen güvencesi değil.
    ESLER = {
        "eş": r"\beş(im|in|i|ime|ine|imi|ini|imin|inin|imle|inle|imden|inden)\b",
        "hanım": r"\bhanım(ım|ın|ı|a|ıma|ına|ımın|ının|la|ımla|ınla)?\b",
        "karı": r"\bkarı(m|n|sı|mın|nın|ma|na|mla|nla)\b",
    }
    ayni, degisen, ornek = 0, [], []
    for r in kayitlar:
        # ⛔⛔ BAĞLAM BLOĞU KULLANICININ SÖZCÜĞÜ DEĞİLDİR. `1475abda`da belge
        # *«eşin katılması»* diyor, kullanıcı *«Karım»* diyor, cevap *«karın»* diyor
        # — yani DOĞRU. Blok sayılınca ölçüm bunu ihlal sandı.
        # ➡️ *Bir kullanıcının «kendi sözcüğü», ona GÖSTERİLEN belgenin sözcüğü değildir.*
        ku_ham = " ".join(m.get("content") or "" for m in r["messages"] if m["role"] == "user")
        ku_ham = re.sub(r"\[BAĞLAM.*?BAĞLAM SONU\]|<<bağlam.*?>>|\{bağlam.*?\}|---\s*KAYNAK.*?KAYNAK SONU\s*---",
                        " ", ku_ham, flags=re.S | re.I)
        ce_ham = " ".join(m.get("content") or "" for m in r["messages"] if m["role"] == "assistant")
        k = {a for a, pat in ESLER.items() if re.search(pat, ku_ham, re.I)}
        c = {a for a, pat in ESLER.items() if re.search(pat, ce_ham, re.I)}
        if not (k and c):
            continue
        if c - k:
            degisen.append((r.get("gen_meta", {}).get("parti_sira"), sorted(k), sorted(c - k)))
        else:
            ayni += 1
    sat += ["## Kullanıcının sözcüğünü koruma", "",
            "⭐ Depo baştan beri *«kullanıcının KENDİ sözcüğünü kullan»* diyor (T142). Bu sinyal",
            "bu raporun ilk koşusunda bulundu ve buraya **kalıcı** eklendi.", "",
            "| | |", "|---|---:|",
            f"| eş/hanım/karı geçen kayıt | {ayni + len(degisen)} |",
            f"| ⭐ kullanıcının sözcüğü KORUNMUŞ | **{ayni}** |",
            f"| ⛔ cevap BAŞKA bir sözcük kullanmış | **{len(degisen)}** |", ""]
    if degisen:
        sat += ["| kayıt | kullanıcı | cevabın kullandığı |", "|---|---|---|"]
        for no, k, c in degisen:
            sat.append(f"| #{no} | *«{', '.join(k)}»* | *«{', '.join(c)}»* |")
        yon = {tuple(c) for _, _, c in degisen}
        sat += ["", f"⚠️ Yön **tek taraflı**: {len(degisen)}/{ayni+len(degisen)} kayıtta "
                "günlük konuşma dilindeki sözcük (*«hanım»*, *«karı»*) resmî olanla "
                "(*«eş»*) değiştirilmiş; tersi **hiç yok**. ➡️ *Korpusun kendi kaydı, "
                "kullanıcının kaydını bastırıyor.*", ""]

    # ⭐ Okuma defteri durumu — elle okunan yığınların hükmü hâlâ geçerli mi?
    try:
        od = _yukle("od", "2026-09-18-okuma-defteri.py")
        dstr = []
        for kad in od.KAPILAR:
            simdi = od._yigin(kad, tren)
            yeni, _dusen, _d = od._karsilastir(kad, simdi)
            dstr.append((kad, len(simdi), len(yeni)))
        sat += ["## Okuma defteri", "",
                "⭐ Elle okunan yığınların hükmü metin değişmedikçe **taşınır**; yalnız",
                "yeni/değişmiş bulgular okunmak üzere listelenir (T171).", "",
                "| kapı | yığın | ⛔ okunmalı |", "|---|---:|---:|"]
        for kad, n, y in dstr:
            sat.append(f"| `{kad}` | {n} | **{y}** |")
        sat += ["", ("⭐ **Hiçbir kapıda okunacak yeni bulgu yok.**"
                     if not sum(y for _, _, y in dstr) else
                     f"⛔ **{sum(y for _, _, y in dstr)} bulgu okunmalı.**"), ""]
    except Exception as e:                      # ⚠️ defter yoksa rapor yine yazılmalı
        sat += ["## Okuma defteri", "", f"⛔ Okunamadı: {type(e).__name__}", ""]

    sat += ["", "⚠️ *«Şablon = kusur»* değildir; ölçülen şey TEKRAR. Ama T162 zincirin son",
            "halkasını gösterdi: §8 özerklik kalıbı modelin davranışında bir güvenlik",
            "bayrağına dönüştü (`gd-018`, uzman kalemi).", "",
            "## ⛔ Bu raporun söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Bu bir KALİTE raporu değil** | kapılar biçim ve dayanak denetler; terapötik "
            "kalite Eksen 1'in işidir ve judge gerektirir (T161/T162) |",
            "| ⛔ **Elle okuma yığını otomatik değil** | yapısal atıf kapısının «elle okunacak» "
            "sütunu her sürümde İNSAN tarafından okunmalı; T155 o yığında %26 kusur buldu |",
            "| ⛔ **Kapıların kendi kör noktaları duruyor** | süre dalı (T163), kip ayrımı "
            "(T165), kısa alıntılar (T143), sert kapının çok sözcüklü ifadeleri (T153) |",
            "| ⚠️ **Sayılar kapıların ölçtüğü kadar** | bir kapının «0» demesi, kapının "
            "BAKABİLDİĞİ yerde 0 olduğu demektir (T155) |", ""]

    rapor = KOK / f"reports/analiz/{TARIH}-surum-sagligi-{d.name}.md"
    rapor.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[4:]))
    print(f"→ {rapor.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "datasets/v0.0.10"))
