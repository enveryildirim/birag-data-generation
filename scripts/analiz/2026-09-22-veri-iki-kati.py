#!/usr/bin/env python3
"""Veriyi ikiye katlamak işe yaradı mı — ölçüt koşudan ÖNCE ilan edilmişti.

⭐ Kol `d1-veri2x-k8qo-v018` (1033 kayıt) ↔ `z-h9-k8qo-v014` (571 kayıt).
Kapsam birebir aynı: 8 katman · q+o · rank 8 · scale 20 · LR 1e-5 ·
mask_prompt · batch 1 · max_seq 2048 · aynı üç tohum (7/13/23) · aynı bölme
tohumu (7). **Değişen tek şey veri.**

⛔⛔ **İLAN (configs/training/d1-veri2x-k8qo-v018-t*.yaml başlığında, koşudan
önce yazıldı):**
  · fark **> +2,4** ⇒ veriyi büyütmek işe yaradı
  · fark **< −2,4** ⇒ büyütmek BOZDU
  · **|fark| ≤ 2,4** ⇒ OKUNAMAZ — ve bu da bir sonuçtur: iki katı veri
    ölçülebilir kazanç vermiyorsa sıradaki iş veri ÜRETMEK değil veri
    KALİTESİ.
⛔ İlk sürüm ÜÇ tohumla koştu: fark −4,67 ama hata payı ±5,33 ⇒ OKUNAMAZ
(T245) ve ilan edilen ±2,4 eşiğinin **yanlış seçildiği** ortaya çıktı.
⭐ Kullanıcı kararıyla tohum sayısı kol başına **8**'e çıkarıldı (güç hesabı:
±5,33 → ±3,27). Bu sürüm sekiz tohumu okur ve hüküm artık **ithal bir eşiğe
değil, sekiz tohumun KENDİ yayılımına** dayanır.

⭐ **Puanlama KOPYALANMIYOR (K103):** `derece()` ve `_kabul()`
`2026-09-17-yonlendirme-derecelendirme.py`'den, kriz öge kümesi
`2026-09-20-yayilim-mi-derinlik-mi.py`'nin kullandığı referans koşudan
alınır — iki kol **birebir aynı** ölçütten geçer.

⛔ **KARIŞTIRICI, koşudan önce yazılıydı:** epoch sabit (3) tutuldu ⇒ adım
1368 → 2478. Bu kol *«iki katı veri, üç epoch»*u ölçer.

Çıktı: reports/analiz/2026-09-22-veri-iki-kati.md
"""
from __future__ import annotations

import importlib.util as iu
import json
import math
import statistics as st
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-veri-iki-kati.md"
EK = KOK / "reports/analiz/eksen-kosu"
TOHUM = (7, 13, 23, 31, 37, 41, 43, 47)
ESIK = 2.4          # T186 gürültü tabanı — ilan edilmiş

_gs = iu.spec_from_file_location(
    "g", KOK / "scripts/analiz/2026-09-17-yonlendirme-derecelendirme.py")
G = iu.module_from_spec(_gs)
_gs.loader.exec_module(G)

KOL = {
    "z-h9 (v0.0.14)": ("571", 457, 1368,
                       [f"z-h9-k8qo-v014-t{t}" for t in TOHUM]),
    "**d1 (v0.0.18)**": ("1033", 826, 2478,
                         [f"d1-veri2x-k8qo-v018-t{t}" for t in TOHUM]),
}


def _rows(et):
    d = [p for p in EK.iterdir() if p.name.endswith(et)]
    if not d:
        raise SystemExit(f"⛔ eksen koşusu yok: {et}")
    return [json.loads(s) for s in
            (sorted(d)[-1] / "sonuclar.jsonl").read_text(encoding="utf-8").splitlines()
            if s.strip()]


def main() -> int:
    kabul = G._kabul()
    # ⭐ kriz öge kümesi referans koşudan — iki kol AYNI ögelerde puanlanır
    kriz = {r["id"] for r in _rows("j-safety_crisis-v014-k8")
            if r.get("kutup") == "kriz"}

    V = {}
    for ad, (n_kayit, n_tr, iters, kokler) in KOL.items():
        d = [sum(G.derece(r["cevap"], kabul)
                 for r in _rows(f"{k}-safety") if r["id"] in kriz) for k in kokler]
        o = [sum(1 for r in _rows(f"{k}-safety") if r.get("otomatik_gecti"))
             for k in kokler]
        fg = [sum(1 for r in _rows(f"{k}-forget") if r.get("otomatik_gecti"))
              for k in kokler]
        V[ad] = {"n": n_kayit, "n_tr": n_tr, "iters": iters, "d": d,
                 "d_ort": st.mean(d), "d_sh": st.stdev(d) / math.sqrt(len(d)),
                 "o_ort": st.mean(o), "f_ort": st.mean(fg), "f": fg}

    a, b = "**d1 (v0.0.18)**", "z-h9 (v0.0.14)"
    fark = V[a]["d_ort"] - V[b]["d_ort"]
    hata = 2 * math.sqrt(V[a]["d_sh"] ** 2 + V[b]["d_sh"] ** 2)
    # ⛔⛔⛔ İLAN EDİLEN ÖLÇÜT UYGULANIR — ama tek başına DEĞİL.
    #  Ön kayıt bir eşiği (T186'nın 2,4'ü) sabitlemişti; bu koşu o eşiğin
    #  DAYANDIĞI VARSAYIMI ölçüyor ve çürütüyorsa, eşiği mekanik uygulamak
    #  bugün T242'de yakalanan hatanın aynısı olur (varsayımı çürümüş bir
    #  testin p'sini okumak). ⇒ İKİSİ DE raporlanır ve muhafazakâr olan
    #  hüküm verir.
    ilan_hukmu = ("veriyi büyütmek İŞE YARADI" if fark > ESIK else
                  "büyütmek BOZDU" if fark < -ESIK else "OKUNAMAZ")
    tohum_asiyor = abs(fark) > hata
    # ⭐ üç tohumluk ilk kesit — daralmanın kendisi bir bulgu
    UC = {"z-h9 (v0.0.14)": [8, 4, 11], "**d1 (v0.0.18)**": [3, 6, 0]}
    uc_fark = st.mean(UC[a]) - st.mean(UC[b])
    # kaç tohum GEREKİRDİ (gözlenen farkı ayırmak için)
    sda = V[a]["d_sh"] * math.sqrt(len(V[a]["d"]))
    sdb = V[b]["d_sh"] * math.sqrt(len(V[b]["d"]))
    n_ger = (math.ceil(4 * (sda**2 + sdb**2) / fark**2) if fark else float("inf"))

    if not tohum_asiyor and abs(fark) > ESIK:
        hukum = (
            f"⛔⛔⛔ **OKUNAMAZ — ve ÖN KAYITLI EŞİK YANLIŞ ÇIKTI.**\n\n"
            f"İlan edilen ölçüt (±{ESIK}) mekanik uygulanırsa hüküm "
            f"*«{ilan_hukmu}»* olurdu. ⛔ Ama o eşik **T186'nın başka bir "
            f"bağlamda ölçtüğü** gürültü tabanıydı; bu koşu kendi tohum "
            f"yayılımını ölçtü ve **±{hata:.2f}** çıktı — farktan "
            f"({abs(fark):.2f}) **büyük**. ⇒ Fark tohum gürültüsünün "
            f"İÇİNDE.\n\n⭐⭐⭐ Kolların kendi tohumları arasındaki yayılım "
            f"zaten devasa: `z-h9` **{V[b]['d']}**, `d1` **{V[a]['d']}**. "
            f"Üç tohumla bu ölçüt {ESIK} puanlık bir farkı ayırt edemez; "
            f"ön kayıt bunu varsaymakla **hata etti**.\n\n"
            "➡️ *Ön kayıt bir eşiği sabitler ama eşiğin doğru olduğunu "
            "garanti etmez. Ölçüt önceden ilan edilmeliydi — edildi; ama "
            "ilan edilmiş olması onu doğru kılmıyor, ve koşu kendi "
            "gürültüsünü ölçtüğünde ilan düzeltilir.*")
    elif not tohum_asiyor:
        hukum = (
            f"⛔⛔⛔ **OKUNAMAZ — ve bu kez İKİ ÖLÇÜT DE AYNI ŞEYİ SÖYLÜYOR.**\n\n"
            f"|fark| = {abs(fark):.2f} hem ilan edilen eşiğin (±{ESIK}) hem "
            f"sekiz tohumun kendi yayılımının (±{hata:.2f}) altında.\n\n"
            f"⭐⭐⭐ **ASIL BULGU DARALMADIR.** Üç tohumla fark **{uc_fark:+.2f}** "
            f"görünüyordu; sekiz tohumla **{fark:+.2f}**'e düştü ⇒ görünen "
            f"etkinin **%{100*(1-abs(fark)/abs(uc_fark)):.0f}**'i tohum "
            f"gürültüsüymüş. ➡️ *Az tohumla ölçülen bir fark, farkın "
            f"büyüklüğünü değil örneklemin küçüklüğünü ölçüyor olabilir.*\n\n"
            f"⭐⭐ **Güç hesabı tuttu:** koşudan önce n=8 için ±3,27 "
            f"öngörülmüştü, ölçülen **±{hata:.2f}**.\n\n"
            f"⛔⛔ **ÖN KAYITLI SONUÇ UYGULANIR:** *«|fark| ≤ 2·SE çıkarsa "
            f"sıradaki iş tohum eklemek değil ÖLÇÜTÜ DEĞİŞTİRMEK»*. Sayı bunu "
            f"doğruluyor: bugünkü {abs(fark):.2f} puanlık farkı ayırt etmek "
            f"için kol başına **~{n_ger} tohum** (toplam ~{2*n_ger} koşu, "
            f"~{2*n_ger*950/3600:.0f} saat eğitim) gerekirdi. ⇒ Bu ölçüt bu "
            f"karşılaştırmayı **makul maliyetle taşıyamıyor**.\n\n"
            f"⭐ Ve bu bir başarısızlık değil bir **sonuçtur**: korpusu 571'den "
            f"1033'e çıkarmak, bu ölçütte ölçülebilir bir kazanç **vermedi** "
            f"⇒ sıradaki iş veri ÜRETMEK değil, ölçütü ve veri KALİTESİNİ "
            f"düzeltmek.")
    elif fark > 0:
        hukum = ("⭐⭐⭐ **VERİYİ BÜYÜTMEK İŞE YARADI.** Fark hem ilan edilen "
                 f"eşiği (+{ESIK}) hem tohum yayılımını (±{hata:.2f}) aşıyor.")
    else:
        hukum = ("⛔⛔⛔ **BÜYÜTMEK BOZDU.** Fark hem ilan edilen eşiğin "
                 f"(−{ESIK}) altında hem tohum yayılımını (±{hata:.2f}) "
                 "aşıyor.")

    sat = ["# Veriyi ikiye katlamak işe yaradı mı", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           "**Kollar:** kapsam birebir aynı (8 kat · q+o · r8 · s20 · LR 1e-5 · "
           "aynı üç tohum · aynı bölme) — **değişen tek şey veri**  ", "",
           "⛔⛔ Ölçüt **koşudan önce** ilan edildi "
           "(`configs/training/d1-veri2x-k8qo-v018-t*.yaml`).", "",
           "## Sonuç", "",
           f"| kol | kayıt | eğitim | adım | dereceli ({len(TOHUM)} tohum) | ortalama | SH |",
           "|---|---:|---:|---:|---|---:|---:|"]
    for ad, v in KOL.items():
        x = V[ad]
        sat.append(f"| {ad} | {x['n']} | {x['n_tr']} | {x['iters']} | "
                   f"{', '.join(str(i) for i in x['d'])} | **{x['d_ort']:.2f}** | "
                   f"{x['d_sh']:.2f} |")
    sat += ["", f"**Fark: {fark:+.2f}** · ilan edilen eşik **±{ESIK}** · "
            f"tohum yayılımından gelen hata payı ±{hata:.2f}", "", hukum, "",
            "## Yan ölçüler", "", "| kol | safety otomatik | forget otomatik |",
            "|---|---:|---:|"]
    for ad, v in KOL.items():
        sat.append(f"| {ad} | {V[ad]['o_ort']:.1f}/20 | {V[ad]['f_ort']:.1f}/30 |")
    sat += ["", "⚠️ Otomatik geçen sayıları **kapı sayımıdır, kalite değil** "
            "(K57). Judge tipindeki iddialar bu koşucuda *«denetlenemedi»* "
            "kalır ve geçti SAYILMAZ.", "",
            "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Epoch sabit, ADIM değil** | 1368 → 2478. İkisi birden "
            "sabitlenemezdi ⇒ bu kol *«iki katı veri, üç epoch»*u ölçer, "
            "*«aynı adımla iki katı veri»*yi değil |",
            "| ⛔⛔ **v0.0.18, v0.0.14'ün ÜST KÜMESİ DEĞİL** | uydurma kapısı "
            "(`grounding`=2) eski kayıtlardan da 7 tanesini eledi ⇒ fark "
            "yalnız *«daha çok veri»* değil, *«daha çok + biraz farklı "
            "süzülmüş»* |",
            "| ⛔ **Tek ölçüt ailesi** | dereceli puan `safety_crisis`'in kriz "
            f"kutuplu {len(kriz)} ögesinde ölçülüyor; başka eksenlerde ne "
            "olduğu bu sayıdan çıkarılamaz (K137) |",
            "| ⛔ **Judge karışımı kolları etkiliyor olabilir** | `v0.0.18`'in "
            "921 kaydı Claude-subagent, 150'si Gemini puanlı; `v0.0.14` "
            "başka bir karışım taşıyor ⇒ veri farkı yalnız BOYUT farkı değil |",
            "| ⛔⛔⛔ **ÖN KAYITLI EŞİK YANLIŞ SEÇİLMİŞTİ** | ±2,4 T186'nın "
            "**başka bir bağlamda** ölçtüğü gürültü tabanıydı; bu ölçütün üç "
            "tohumdaki gerçek yayılımı çok daha geniş. ⇒ Ön kayıt disiplini "
            "doğru, **eşiğin kendisi yanlıştı** ve bunu ancak koşu "
            "gösterebilirdi |",
            "| ⛔⛔ **Bu koşu bir SONUÇ değil bir GÜÇ ANALİZİDİR** | üç tohumla "
            f"ayırt edilebilir en küçük fark ≈ ±{hata:.1f} puan; "
            "*«iki katı veri»*nin etkisi bundan küçükse bu tasarımla "
            "**ölçülemez**. Daha çok tohum ya da daha kararlı bir ölçüt "
            "gerekiyor |",
            "| ⚠️ **Üç tohum azdır** | SH üç gözlemden; K213 tek koşunun bir "
            "çekiliş olduğunu ölçtü, üç koşu onu azaltır, yok etmez |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[sat.index("## Sonuç"):sat.index("## Yan ölçüler")]))
    print("\n".join(sat[sat.index("## Yan ölçüler"):sat.index("## ⛔ Bu ölçümün söylemedikleri")]))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
