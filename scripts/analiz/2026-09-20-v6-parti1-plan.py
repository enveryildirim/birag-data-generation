#!/usr/bin/env python3
"""v6-parti1 tasarım ızgarası — 60 kayıt. Üretimden ÖNCE yazılır, sonra dondurulur.

⭐ Izgara çözücü, hücre yasakları ve üç kriz süzgeci `2026-09-16-v5-parti3-plan.py`
(P3) ve onun üzerinden `2026-09-15-v4-parti1-plan.py` (P1) **çağrılır** — yeniden
tanımlanmaz (K97: iki tanım iki sayı demektir).

⛔⛔ **BU PARTİNİN FARKI: tohum seçimi KANITLA hedefleniyor.** T190 havuzun
kapsama açığını ölçtü (üretilmiş 559 tohumun payı ↔ havuzun 2240'taki payı).
T132 zaten göstermişti ki *aynı türden* üretmek tıkanan şeyi açmıyor ⇒ parti
sırayla değil, ölçülmüş açığa göre seçilir.

⭐⭐ **AÇIKLAR İKİ AYRI YERDE YAŞIYOR ve iki ayrı mekanizma ister:**
  · **Izgara ekseni** olanlar (`tur`) → KOTA değiştirilir.
  · **Tohum özniteliği** olanlar (`senaryo`, `profil`, `evre`, `motivasyon_evresi`,
    `siddet_seviyesi`, `stres_tipi`) → ızgarada karşılığı YOK; bunlar ancak
    **tohum seçimiyle** kapatılır.
➡️ *Bir kapsama açığını yanlış mekanizmayla kapatmaya çalışmak, kapattığını
sanıp hiçbir şey değiştirmemektir: ızgara `profil`i hiç görmüyor.*

⭐⭐⭐ **HEDEFLEME SEÇİCİYİ DEĞİŞTİRMEDEN YAPILIYOR.** `P1.sec` **ilk-uyan**
bir seçicidir ⇒ havuzun SIRASI seçimi belirler. Havuz, açığı kapatan tohumlar
öne gelecek biçimde yeniden sıralanır; `P1.sec` bir satırı bile değişmez
(Kural 7: parti1/2/3'ün çıktıları ona dayanıyor). Sıralama deterministtir
(anahtar: kalan ihtiyaç, eşitlikte `seed_id`).
⚠️ Sıralama yalnız `(tur, yaş)` kovaları İÇİNDE etkilidir — `P1.sec` zaten o iki
alana göre süzüyor ⇒ ızgara kotaları bozulmaz.

⛔ **Hedefler TAVAN değil YÖNELİM:** greedy atama çakışabilir (bir tohumun tek
`profil`i vardır). Bu yüzden hedefler ilan edilir, **ulaşılan** ayrıca ölçülür
ve rapor edilir — tutmadıysa tutmadığı yazılır.

Girdi : data/seeds.jsonl (P1 üzerinden) · reports/analiz/2026-09-20-kapsama-acigi-envanteri.json
Çıktı : data/plan/v6-parti1.jsonl · reports/analiz/2026-09-20-v6-parti1-plan.md
"""
from __future__ import annotations

import json
import os
import random
from collections import Counter
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
N = 60
TOHUM = int(os.environ.get("BIRAG_PLAN_TOHUM", "20260920"))
CIKTI = KOK / os.environ.get("BIRAG_PLAN_CIKTI", "data/plan/v6-parti1.jsonl")
RAPOR = KOK / f"reports/analiz/{TARIH}-v6-parti1-plan.md"

_sp = _iu.spec_from_file_location("p3", KOK / "scripts/analiz/2026-09-16-v5-parti3-plan.py")
P3 = _iu.module_from_spec(_sp)
_sp.loader.exec_module(P3)
P1 = P3.P1

# ⛔⛔ `ESLEME` P3'ün `main()` içinde YEREL bir sabit; içe aktarılamıyor. Elle
# yeniden yazmak K97'nin yasakladığı ikinci tanımı yaratırdı (iki tanım iki sayı
# demektir), P3'ü düzenlemek ise parti3'ün dondurulmuş çıktısını riske atardı
# (Kural 7). ⇒ Tek tanım P3'te KALIYOR ve buradan **kaynaktan türetiliyor**:
# P3 değişirse bu satır sessizce eskimez, `literal_eval` ya da assert patlar.
def _p3_esleme() -> dict[str, str]:
    import ast
    import inspect
    kaynak = inspect.getsource(P3.main)
    i = kaynak.index("ESLEME = ")
    j = kaynak.index("}", i) + 1
    d = ast.literal_eval(kaynak[i + len("ESLEME = "):j])
    assert isinstance(d, dict) and "ic_motivasyon" in d, f"⛔ ESLEME beklenmedik: {d}"
    return d


ESLEME = _p3_esleme()

# ── (1) IZGARA EKSENİ olan açık: `tur` ───────────────────────────────────────
# T190: `receteli_ilac` sette %12,2 ↔ havuz %18,8 · `kumar` %18,8 ↔ %23,2.
# ⭐ Kota ELLE değil, ÜRETİLEBİLİR HAVUZUN payından türetilir (en büyük artık
# yöntemiyle 60'a yuvarlanır) ⇒ sayı bir tercih değil, havuzun kendisi.
def tur_kotasi(hav: list[dict]) -> dict[str, int]:
    c = Counter(P1.TUR_ESLEME.get(t["meta"].get("bagimlilik_turu")) for t in hav)
    c.pop(None, None)
    top = sum(c.values())
    ham = {k: N * v / top for k, v in c.items()}
    kota = {k: int(v) for k, v in ham.items()}
    for k, _ in sorted(ham.items(), key=lambda x: -(x[1] - int(x[1])))[:N - sum(kota.values())]:
        kota[k] += 1
    return kota


# ── (2) TOHUM ÖZNİTELİĞİ olan açıklar ────────────────────────────────────────
# Hedef = partide o değerden en az kaç kayıt olsun. Havuz payının ÜSTÜNE
# çıkarılır ki kümülatif set pariteye doğru hareket etsin (60 kayıt tek başına
# 559'luk seti pariteye getiremez; bu parti bir ADIM).
# ⭐ Çağıran betik `TOHUM_HEDEF`i ölçümden türetip değiştirirse bunu işaretler;
# rapor şerhi buna göre yazılır (bkz. §«söylemedikleri»).
_TURETILMIS = False

TOHUM_HEDEF = {
    ("senaryo", "rol_siniri"): 24,
    ("siddet_seviyesi", "agir"): 21,
    ("motivasyon_evresi", "hazirlik"): 15,
    ("evre", "birakma_cabasi"): 12,
    ("evre", "nuksetme"): 11,
    ("profil", "ev_kadini"): 9,
    ("profil", "yeni_ebeveyn"): 9,
    ("stres_tipi", "kronik_agri"): 5,     # T190: hiç üretilmemiş ama SERT DEĞİL
}


def _ihtiyac_sirasi(hav: list[dict], kalan: dict) -> list[dict]:
    """Açığı kapatan tohumlar öne. Deterministik; `P1.sec` değişmez."""
    def anahtar(t):
        puan = sum(kalan.get((e, v), 0) for (e, v) in TOHUM_HEDEF
                   if str(t["meta"].get(e)) == v)
        return (-puan, t["seed_id"])
    return sorted(hav, key=anahtar)


def main() -> int:
    hav = P3.P1.havuz(CIKTI)   # ⛔ kendi çıktısı hariç (T224)
    for ad, yol, dsn in (
            ("dolaylı kriz", "2026-09-17-kriz-suzgeci-yanlis-negatif.py", "DOLAYLI"),
            ("beyanla SERT kriz", "2026-09-17-tohum-beyan-kriz-kapisi.py", None)):
        sp = _iu.spec_from_file_location("m", KOK / "scripts/analiz" / yol)
        M = _iu.module_from_spec(sp); sp.loader.exec_module(M)
        once = len(hav)
        hav = ([t for t in hav if not M.DOLAYLI.search(t["user_message"])] if dsn
               else [t for t in hav if M._sinif(t) != "sert"])
        print(f"   ⛔ {ad} süzgeci: {once - len(hav)} tohum elendi")

    # ⛔⛔ P3'ün KOTA'sı `tur` satırında DEĞİŞTİRİLİYOR. Modül globali yerinde
    # değiştiriliyor çünkü `P3.coz` onu okuyor; kopyalamak K97'nin yasakladığı
    # ikinci tanımı yaratırdı. Değişiklik TEK satır ve aşağıda sınanıyor.
    yeni_tur = tur_kotasi(hav)
    print(f"   ⭐ `tur` kotası havuzdan türetildi: {yeni_tur}")
    assert set(yeni_tur) <= set(P3.KOTA["tur"]) | {"receteli_ilac", "dijital"}
    P3.KOTA = {**P3.KOTA, "tur": yeni_tur}
    for a, d in P3.KOTA.items():
        if sum(d.values()) != N:
            raise SystemExit(f"⛔ KOTA bozuk: {a} toplamı {sum(d.values())} ≠ {N}")

    kap = P3.kapasite(hav)
    izgara = None
    for deneme in range(40):
        izgara = P3.coz(random.Random(TOHUM + deneme), kap)
        if izgara:
            print(f"✅ ızgara {deneme + 1}. denemede çözüldü (tohum {TOHUM + deneme})")
            break
    if not izgara:
        raise SystemExit("⛔ kısıtlar çözülemedi")

    # ⭐⭐ İKİ HEDEFLEME KATMANLI ÇALIŞIR, YARIŞMAZ.
    # v5-parti3 motivasyonu havuz payına göre KATMANLIYOR (T95/T98: katmansız
    # bırakılınca `aile_baskisi` %27'lik havuzdan %50 çıkmıştı — dosya sırasının
    # artefaktı). Bu parti ona kapsama hedeflemesi ekliyor. İkisi çakışmaz:
    # motivasyon havuzu ÖNCE süzer, kapsama sırası o alt kümenin İÇİNDE sıralar.
    hp = Counter(ESLEME.get(t["meta"].get("motivasyon"), "ic") for t in hav)
    _top = sum(hp.values())
    pay = {k: round(N * v / _top) for k, v in hp.items()}
    while sum(pay.values()) != N:
        _en = max(pay, key=lambda k: pay[k])
        pay[_en] += 1 if sum(pay.values()) < N else -1
    print(f"   katmanlı motivasyon hedefi (havuz dağılımı): {pay}")

    kalan_hedef = dict(TOHUM_HEDEF)
    kalan_mot = dict(pay)
    alinmis: set[str] = set()
    eksik = []
    # ⛔⛔ ATAMA SIRASI KARIŞTIRILIR — ilk sürümde `sira` düzeninde atanıyordu ve
    # ölçüldü: hedeflenen tohumlar BAŞA YIĞILDI (`rol_siniri` blok1'de 12/12,
    # blok5'te 1/12; `agir` 10→4). Sebep bileşik: havuz ihtiyaca göre sıralı
    # + `P1.sec` ilk-uyan + satırlar sırayla işleniyor. Üç sonucu vardı:
    #   (a) üretim BLOK BLOK yapılıyor ⇒ ilk blok 12 benzer konuşma olurdu ve
    #       şablonlaşma bu depoda ölçülmüş bir kusur (T139);
    #   (b) parti kısmen üretilirse o kısım partiyi TEMSİL ETMEZ (parti8 böyle
    #       üretilmişti);
    #   (c) `sira` ile tohum özniteliği korelasyonu sonraki çözümlemelerde
    #       karıştırıcı olurdu.
    # ⇒ Satırlar karıştırılmış sırada atanır, dosyaya `sira` düzeninde yazılır.
    # Hedefleme bozulmaz (greedy ihtiyaç sırası aynen çalışır), yalnız dağılır.
    atama_sirasi = list(izgara)
    random.Random(TOHUM).shuffle(atama_sirasi)
    for s in atama_sirasi:
        s["havuz"] = None          # `P1.sec` bu alanı okuyor (regex süzgeci; burada yok)
        t = None
        for kat in sorted(kalan_mot, key=lambda k: -kalan_mot[k]):
            if kalan_mot[kat] <= 0:
                continue
            altkume = [x for x in hav
                       if ESLEME.get(x["meta"].get("motivasyon"), "ic") == kat]
            t = P1.sec(s, _ihtiyac_sirasi(altkume, kalan_hedef), alinmis)
            if t is not None:
                kalan_mot[kat] -= 1
                break
        if t is None:              # katman bulunamadı: bütün havuzdan, yine hedefli
            t = P1.sec(s, _ihtiyac_sirasi(hav, kalan_hedef), alinmis)
        if t is None:
            eksik.append(s["sira"]); continue
        alinmis.add(t["seed_id"])
        for (e, v) in list(kalan_hedef):
            if str(t["meta"].get(e)) == v and kalan_hedef[(e, v)] > 0:
                kalan_hedef[(e, v)] -= 1
        m = t["meta"].get("motivasyon")
        s.update({"seed_id": t["seed_id"], "source_id": t["source_id"],
                  "tohum_senaryo": t["meta"].get("senaryo"),
                  "tohum_kelime": len(t["user_message"].split()),
                  "tohum_metin": t["user_message"],
                  "motivasyon": ESLEME.get(m, "ic"), "motivasyon_tohum": m,
                  "motivasyon_geri_dusme": m not in ("ic_motivasyon", "aile_baskisi",
                                                     "yasal_zorunluluk")})
    if eksik:
        raise SystemExit(f"⛔ tohum bulunamayan satır: {eksik}")

    # ── sınama: marjinaller, hücre yasakları, hedefler ──
    hata = []
    for a, d in P3.KOTA.items():
        g = Counter(s[a] for s in izgara)
        for v, n in d.items():
            if g.get(v, 0) != n:
                hata.append(f"{a}={v}: {g.get(v,0)} ≠ {n}")
    for s in izgara:
        if (y := P3.yasak(s)):
            hata.append(f"#{s['sira']} yasak hücre: {y}")
    if hata:
        raise SystemExit("⛔ " + " · ".join(hata[:6]))

    tohum_meta = {t["source_id"]: t["meta"] for t in hav}
    ulasilan = {k: sum(1 for s in izgara
                       if str(tohum_meta[s["source_id"]].get(k[0])) == k[1])
                for k in TOHUM_HEDEF}
    izgara = sorted(izgara, key=lambda x: x["sira"])
    CIKTI.write_text("".join(json.dumps(s, ensure_ascii=False) + "\n" for s in izgara),
                     encoding="utf-8")

    sat = [f"# `v6-parti1` tasarım ızgarası — {N} kayıt", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH} · "
           f"**tohum:** {TOHUM}  ",
           f"**Çıktı:** `{CIKTI.relative_to(KOK)}` — üretimden ÖNCE yazıldı, dondurulur  ",
           f"**Havuz:** üç kriz süzgecinden sonra **{len(hav)}** tohum", "",
           "⭐⭐ **Bu partinin farkı:** tohum seçimi T190'ın ölçtüğü kapsama açığına göre "
           "hedefleniyor. Açıklar iki ayrı yerde yaşıyor ve iki ayrı mekanizma istiyor: "
           "`tur` bir **ızgara ekseni** (kota değişti), ötekiler **tohum özniteliği** "
           "(ızgarada karşılığı yok, ancak seçimle kapanır).", "",
           "⭐ **Seçici değişmedi.** `P1.sec` ilk-uyan olduğu için havuz yeniden "
           "sıralandı; sıralama `(tur, yaş)` kovaları içinde etkili olduğundan ızgara "
           "kotaları bozulmuyor.", "",
           "## 1. `tur` kotası — havuzdan türetildi", "", "| tür | kota |", "|---|---:|"]
    sat += [f"| `{k}` | {v} |" for k, v in sorted(yeni_tur.items(), key=lambda x: -x[1])]
    sat += ["", "## 2. ⭐⭐⭐ Tohum hedefleri — ilan edilen ↔ ulaşılan", "",
            "| eksen = değer | hedef | **ulaşılan** | durum |", "|---|---:|---:|---|"]
    for k, h in sorted(TOHUM_HEDEF.items(), key=lambda x: -x[1]):
        u = ulasilan[k]
        sat.append(f"| `{k[0]}={k[1]}` | {h} | **{u}** | "
                   + ("⭐ tuttu" if u >= h else f"⛔ **{h - u} eksik**") + " |")
    tutan = sum(1 for k, h in TOHUM_HEDEF.items() if ulasilan[k] >= h)
    sat += ["",
            f"**{tutan}/{len(TOHUM_HEDEF)} hedef tuttu.** ⛔ Hedefler TAVAN değil "
            "YÖNELİM: bir tohumun tek `profil`i, tek `evre`si vardır ⇒ hedefler "
            "birbiriyle yarışır ve hepsi aynı anda tutamayabilir. Tutmayanlar yukarıda "
            "**yazılı**; sonraki parti onlardan devam eder.", "",
            "## 3. ⭐ Yığılma sınaması — hedeflenen tohumlar dağıldı mı", "",
            "Üretim blok blok yapılıyor ⇒ hedeflenen öznitelik parti başına yığılırsa "
            "ilk blok tekdüze olur (T139 şablonlaşma) ve kısmi üretim partiyi temsil "
            "etmez. 12'lik bloklarda sayılır.", "",
            "| eksen = değer | b1 | b2 | b3 | b4 | b5 | aralık |",
            "|---|---:|---:|---:|---:|---:|---:|"]
    _tm = {t["source_id"]: t["meta"] for t in hav}
    _yig = {}
    for (e, v) in TOHUM_HEDEF:
        say = [sum(1 for s in izgara[b * 12:(b + 1) * 12]
                   if str(_tm[s["source_id"]].get(e)) == v) for b in range(5)]
        _yig[f"{e}={v}"] = say
        sat.append(f"| `{e}={v}` | " + " | ".join(map(str, say)) +
                   f" | **{max(say) - min(say)}** |")
    # ⛔⛔ HEDEF LİSTESİ BOŞ OLABİLİR (ilk kez v6-parti7). Ufuk kuralı korpus
    # büyüdükçe hedef üretmeyi bırakıyor; o zaman yığılma diye bir şey de
    # yok ve bu kontrol sessizce çökmemeli. ➡️ *Bir denetim, denetlediği şey
    # sıfır olduğunda «geçti» demez — «denetlenecek bir şey yok» der.*
    _enfazla = max((max(v) - min(v) for v in _yig.values()), default=None)
    sat += ["",
            ("⭐ **Hedeflenen öznitelik yok** — yığılma denetimi bu partide "
             "boş; kapsama kuralı yalnız tavan üretti."
             if _enfazla is None else
             f"⭐ **En büyük blok aralığı {_enfazla}** — hedeflenen öznitelikler "
             "bloklara dağılmış durumda."
             if _enfazla <= 6 else
             f"⛔⛔ **En büyük blok aralığı {_enfazla}** — hâlâ yığılma var."), "",
            "## 4. Izgara özeti", "", "| | |", "|---|---:|",
            f"| bağlam (`context`) | {sum(s['context'] for s in izgara)} |",
            f"| §8b sınır tipi ≠ yok | {sum(1 for s in izgara if s['sinir_tipi'] != 'yok')} |",
            f"| nazikçe karşı çıkma | "
            f"{sum(1 for s in izgara if s['senaryo_hedefi'] == 'nazikce_karsi_cikma')} |",
            f"| `is_negative` | {sum(s['is_negative'] for s in izgara)} |",
            f"| motivasyon (tohumdan) | "
            f"{dict(Counter(s['motivasyon'] for s in izgara))} |",
            f"| kisa×takdir (tavan {P3.KISA_TAKDIR_TAVAN}) | "
            f"{sum(1 for s in izgara if s['bicim']=='kisa' and s['turn_ending']=='takdir')} |",
            "", "## ⛔ Bu planın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **T132 hâlâ geçerli** | kapsama açığını kapatmak da *«daha çok "
            "veri»*dir; güvenlik kapısını açacağına dair kanıt YOK |",
            "| ⛔⛔ **Kapsama ≠ kalite** | payı havuza yaklaştırmak o eksende iyi kayıt "
            "üretileceğini göstermez |",
            # ⚠️ Bu şerh, hedeflerin nasıl belirlendiğine göre DEĞİŞİR. Parti1'de
            # elle seçildiler; parti2 bu betiği çağırıp `TOHUM_HEDEF`i ölçümden
            # türetiyor ⇒ o koşuda «seçildi» demek yanlış olurdu.
            # ➡️ *Devralınan bir şerh, devralan bağlamda yanlış olabilir.*
            ("| ⛔ **Hedef sayıları SEÇİLDİ** | havuz payının üstüne çıkarıldı ki "
             "kümülatif set pariteye doğru hareket etsin; kesin değerler benim önerim |"
             if not _TURETILMIS else
             "| ⚠️ **Hedef sayıları TÜRETİLDİ** | ölçülmüş havuz payından; ama "
             "türetme kuralının çarpanı ve tavanı seçilmiştir (bu benim önerim) |"),
            "| ⛔ **Izgara kotaları v5-parti3'ten devralındı** | `tur` dışında "
            "değiştirilmedi — onlar ölçümle ayarlanmıştı (T94/T97/T98) ve bu parti "
            "onları yeniden sınamıyor |",
            "| ⚠️ **Plan üretim değildir** | dondurulan şey tasarım; üretim ayrı adım |", ""]
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[6:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
