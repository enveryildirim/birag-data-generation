#!/usr/bin/env python3
"""v5-parti3 tasarım ızgarası — 60 kayıt. Üretimden ÖNCE yazılır, sonra dondurulur.

⭐ Havuz / hariç tutma / tohum seçici `2026-09-15-v4-parti1-plan.py`'den ÇAĞRILIR.

⭐⭐ **IZGARA ELLE DEĞİL, KISITLA KURULUYOR.** parti1 ve parti2'nin ızgaraları elle
yazıldı ve T94 bunun ölçülmüş bedelini verdi: eksenler bağımsız çekilince
talimatın kendi *«zayıf»* dediği hücre doluyor ve **kota denetimi bunu göremiyor**,
çünkü her eksen ayrı ayrı doğru. ⇒ Burada marjinal kotalar **ve** hücre yasakları
birlikte çözülüyor; çözüm deterministik (sabit tohum) ve sonunda ikisi de sınanıyor.

Kotalar `prompts/uretim-v5.md`'den; v4'ten değişenler:
  · bağlam %10 → **%25** (15 kayıt)        — `context_fidelity` tek gerileyen eksen
  · §8b %33 → **%15** (9 kayıt)            — dilim işini yaptı (16→18/20)
  · `nazikce_karsi_cikma` **%15 KOTA OLDU** — `sycophancy` +5 ile en çok yararlanan
  · `motivasyon` **SÜTUN DEĞİL**           — T95: tohumdan okunur
"""
from __future__ import annotations

import json
import random
from collections import Counter
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
_sp = _iu.spec_from_file_location("p1", KOK / "scripts/analiz/2026-09-15-v4-parti1-plan.py")
P1 = _iu.module_from_spec(_sp)
_sp.loader.exec_module(P1)

N = 60
# ⚠️ Varsayılanlar DEĞİŞMEDİ (parti3'ün çıktısı yeniden üretilebilir kalır);
# ortam değişkeni sonraki partiler için ek giriş.
import os
TOHUM = int(os.environ.get("BIRAG_PLAN_TOHUM", "20260916"))
CIKTI = KOK / os.environ.get("BIRAG_PLAN_CIKTI", "data/plan/v5-parti3.jsonl")

# ── marjinal kotalar (toplamları N etmeli; betik sınıyor) ────────────────────
KOTA = {
    "bicim":        {"kisa": 24, "orta": 21, "uzun": 15},
    "register":     {"bozuk": 15, "duzgun": 45},
    "turn_ending":  {"acik_uclu_soru": 30, "takdir": 9, "ozet": 9,
                     "yalnizca_yansitma": 9, "durur": 3},
    "mi_process":   {"engaging": 24, "focusing": 12, "evoking": 15, "planning": 9},
    "turn_type":    {"multi": 24, "single": 36},
    "konusma_durumu": {"tetikleyici_an": 21, "suregiden_durum": 12,
                       "iyi_giden_paylasim": 9, "plan_yapma": 9,
                       "merak_sorusu": 6, "aradan_donus": 3},
    "sinir_tipi":   {"rol_siniri_yonlendirme": 3, "yonlendirme_istegi": 2,
                     "yonlendirme_gereksiz": 2, "sinir_cekme": 2, "yok": 51},
    "senaryo_hedefi": {"nazikce_karsi_cikma": 9, "serbest": 51},   # ⭐ §8c YENİ
    "tur":          {"tutun": 22, "alkol": 17, "kumar": 11, "receteli_ilac": 7,
                     "dijital": 3},
    "yas":          {"yetiskin": 55, "ergen": 5},
}
SAYI_KOTA = {"is_negative": 9, "ozerklik": 12, "context": 15}       # ⭐ context 6 → 15


# ── hücre yasakları — T94'ün doğrudan karşılığı ──────────────────────────────
def yasak(s: dict) -> str | None:
    # T94/T97: kısa + tek tur, yalnız CEVAPLANABİLİR bir talep varsa güçlü.
    # Rol sınırı soruları öyledir (#7/#8/#9 parti2'de tek turda tuttu); ötekiler
    # değil ⇒ `sinir_tipi == yok` iken kısa+tek tur YASAK.
    if s["bicim"] == "kisa" and s["turn_type"] == "single" and s["sinir_tipi"] == "yok":
        return "kisa+single, cevaplanabilir talep yok (T94)"
    # T97: `kisa × takdir` uydurma için en riskli hücre (parti2'de 2/5).
    # Yasaklanmıyor — takdir kısa mesajda da öğretilmeli — ama TAVANI var.
    # (tavan aşağıda küme düzeyinde sınanıyor)
    # §7: bağlam bloğu taşıyan kayıt `kisa` olamaz — 5 kelimelik mesajın yanına
    # pasaj koymak gerçekçi değil ve `bicim` ölçüsünü de okunmaz kılar.
    if s["context"] and s["bicim"] == "kisa":
        return "bağlamlı kayıt kisa olamaz (§7)"
    # §5a′: güvenlik yoklaması kotaya tabi değil; ızgara seviyesinde yapılabilecek
    # şey, `is_negative` kayıtlarını sorusuz bitişe zorlamamak.
    if s["is_negative"] and s["turn_ending"] == "durur":
        return "is_negative + durur: red edilen kullanıcı boşta bırakılamaz"
    return None


# ⛔⛔ §7a ile `is_negative` BAĞIMSIZ DEĞİL. §7a'nın dört sınıfından biri —
# `cevap_yok` (*«soruldu, cevap pasajda yok»*) — talimatın kendi cümlesiyle
# **is_negative gerektiriyor**: *«bu bağlamda yok de, uydurma (is_negative)»*.
# 15 bağlam kaydında %25 hedefi ⇒ 4 kayıt `cevap_yok` ⇒ 4 kayıt `is_negative`.
# ⚠️ İlk çözümde bağlam satırlarına düşen `is_negative` **1**'di ve §7a
# uygulanamazdı. T94/T98'in ÜÇÜNCÜ örneği: bağımsız çekilen iki eksen,
# talimatın kupladığı bir hücrede çakışıyor.
BAGLAM_NEG_ASGARI = 4


KISA_TAKDIR_TAVAN = 2      # T97

# ⭐ TOHUM BULUNABİLİRLİĞİ DE BİR KISIT. parti3'te `#22` (`dijital`+`ergen`)
# tohum bulamadı: ızgara `tur` ile `yas`ı bağımsız çekiyor ama havuzda o hücre
# tükenmiş olabilir. ⇒ T94'ün aynı sınıfı, bu kez kaynak tarafında.
# Kapasite havuzdan SAYILIR, varsayılmaz.
def kapasite(hav: list[dict]) -> dict[tuple[str, str], int]:
    from collections import Counter as _C
    c: _C = _C()
    for t in hav:
        tur = P1.TUR_ESLEME.get(t["meta"].get("bagimlilik_turu"))
        yg = t["meta"].get("yas_grubu")
        if tur is None or yg is None:
            continue
        c[(tur, "ergen" if yg == "ergen" else "yetiskin")] += 1
    return dict(c)


def coz(rng: random.Random, kap: dict[tuple[str, str], int]) -> list[dict] | None:
    """Kotaları tutan, hücre yasaklarını ihlal etmeyen bir atama bul."""
    havuzlar = {a: [v for k, n in d.items() for v in [k] * n] for a, d in KOTA.items()}
    for a in havuzlar:
        rng.shuffle(havuzlar[a])
    ikili = {a: [1] * n + [0] * (N - n) for a, n in SAYI_KOTA.items()}
    for a in ikili:
        rng.shuffle(ikili[a])
    satirlar = []
    for i in range(N):
        s = {"sira": i + 1}
        s.update({a: havuzlar[a][i] for a in havuzlar})
        s.update({a: ikili[a][i] for a in ikili})
        satirlar.append(s)
    # onarım: yasak hücreleri, aynı eksende takas ederek düzelt (kota korunur)
    for _ in range(4000):
        kotu = [s for s in satirlar if yasak(s)]
        kt = [s for s in satirlar if s["bicim"] == "kisa" and s["turn_ending"] == "takdir"]
        # kapasite aşımı: hangi (tur, yas) hücresi havuzdan fazla istiyor
        say = Counter((s["tur"], s["yas"]) for s in satirlar)
        asan = [s for s in satirlar if say[(s["tur"], s["yas"])] > kap.get((s["tur"], s["yas"]), 0)]
        # §7a: bağlam satırlarında yeterli `is_negative` var mı
        bn = sum(1 for s in satirlar if s["context"] and s["is_negative"])
        neg_eksik = bn < BAGLAM_NEG_ASGARI
        if not kotu and not asan and not neg_eksik and len(kt) <= KISA_TAKDIR_TAVAN:
            return satirlar
        if neg_eksik and not kotu and not asan:
            # `is_negative`i bağlamsız bir satırdan bağlamlı bir satıra taşı
            veren = [s for s in satirlar if s["is_negative"] and not s["context"]]
            alan = [s for s in satirlar if s["context"] and not s["is_negative"]]
            if veren and alan:
                a, b = rng.choice(veren), rng.choice(alan)
                a["is_negative"], b["is_negative"] = 0, 1
                continue
        hedef = kotu[0] if kotu else (asan[0] if asan else kt[0])
        eksen = rng.choice(["bicim", "turn_type", "context", "turn_ending", "is_negative"]
                           if not asan else ["yas", "tur"])
        obur = rng.choice(satirlar)
        hedef[eksen], obur[eksen] = obur[eksen], hedef[eksen]
    return None


def main() -> int:
    # kota toplamları kendi kendini sınar (parti2'de bu sınama 3 hatayı yakaladı)
    for a, d in KOTA.items():
        if sum(d.values()) != N:
            raise SystemExit(f"⛔ KOTA bozuk: {a} toplamı {sum(d.values())} ≠ {N}")

    hav = P1.havuz()
    # ⛔⛔ KRİZ SÜZGECİ GENİŞLETİLDİ (2026-09-17). `P1.KRIZ_ANAHTAR` yalnız AÇIK
    # ifadeleri arıyor ve ölçüldü: dolaylı ifade taşıyan 12 tohumun **12'si de**
    # süzgeçten geçiyor (*«ben olmasam belki herkes daha rahat eder»* — algılanan
    # yük biçiminde edilgen intihar düşüncesi). Etik kurul kararı beklerken kriz
    # malzemesini üretimden uzak tutan TEK mekanizma bu süzgeç (K23).
    # ⚠️ `P1` DEĞİŞTİRİLMEDİ (Kural 7: parti1/2/3'ün çıktıları ona dayanıyor);
    # ek süzgeç DIŞARIDAN uygulanıyor. ⛔ Bu yüzden parti3'ün planı bu betikle
    # yeniden üretilirse AYNI ÇIKMAZ — süzgeç sıkılaştı, yön Kural 3'e uygun.
    _kriz = _iu.spec_from_file_location(
        "kz", KOK / "scripts/analiz/2026-09-17-kriz-suzgeci-yanlis-negatif.py")
    KZ = _iu.module_from_spec(_kriz); _kriz.loader.exec_module(KZ)
    _once = len(hav)
    hav = [t for t in hav if not KZ.DOLAYLI.search(t["user_message"])]
    print(f"   ⛔ dolaylı kriz süzgeci: {_once - len(hav)} tohum daha elendi")

    # ⛔⛔ ÜÇÜNCÜ SÜZGEÇ — VE DESEN ARAYAN İKİSİNDEN DAHA GÜVENİLİR OLANI.
    # `ce39d82bf868e5f2` üretilmişti ve tohumun KENDİ `esdurumlar` alanı
    # **«Aktif intihar düşüncesi»** yazıyordu: aradığımız şeyi korpus beyan
    # ediyormuş. Beyan okumak desen aramanın YERİNE geçmez, ÖNÜNE geçer —
    # desen süzgeçleri beyansız tohumlar için gerekli kalıyor.
    # ⚠️ Yalnız SERT sınıf eleniyor; PERSONA sınıfı (*«… olası»*, *«… sinyali»*)
    # 7 tohumda aynı personadan geliyor ve elenmesi borç/tefeci eksenini yok
    # ederdi — o karar etik kurulun, bu betiğin değil (bkz. kapı betiğinin
    # başlığı).
    _beyan = _iu.spec_from_file_location(
        "bk", KOK / "scripts/analiz/2026-09-17-tohum-beyan-kriz-kapisi.py")
    BK = _iu.module_from_spec(_beyan); _beyan.loader.exec_module(BK)
    _once = len(hav)
    hav = [t for t in hav if BK._sinif(t) != "sert"]
    print(f"   ⛔ beyanla SERT kriz süzgeci: {_once - len(hav)} tohum daha elendi")
    kap = kapasite(hav)
    print("   tohum kapasitesi (tur×yaş):",
          {f"{k[0]}/{k[1]}": v for k, v in sorted(kap.items()) if v < 40})
    izgara = None
    for deneme in range(40):
        izgara = coz(random.Random(TOHUM + deneme), kap)
        if izgara:
            print(f"✅ ızgara {deneme + 1}. denemede çözüldü (tohum {TOHUM + deneme})")
            break
    if not izgara:
        raise SystemExit("⛔ kısıtlar çözülemedi")

    # ── sınama: marjinaller + hücre yasakları ──
    hata = []
    for a, d in KOTA.items():
        c = dict(Counter(s[a] for s in izgara))
        if c != d:
            hata.append(f"  {a}: {sorted(c.items())} ≠ {sorted(d.items())}")
    for a, n in SAYI_KOTA.items():
        if sum(s[a] for s in izgara) != n:
            hata.append(f"  {a}: {sum(s[a] for s in izgara)} ≠ {n}")
    for s in izgara:
        if (y := yasak(s)):
            hata.append(f"  #{s['sira']} yasak hücre: {y}")
    bn = sum(1 for s in izgara if s["context"] and s["is_negative"])
    if bn < BAGLAM_NEG_ASGARI:
        hata.append(f"  §7a: bağlamlı kayıtlarda is_negative {bn} < {BAGLAM_NEG_ASGARI}")
    say = Counter((s["tur"], s["yas"]) for s in izgara)
    for hucre, n in say.items():
        if n > kap.get(hucre, 0):
            hata.append(f"  {hucre}: {n} istendi, havuzda {kap.get(hucre, 0)}")
    if hata:
        raise SystemExit("⛔ sınama düştü:\n" + "\n".join(hata))

    # ── tohum ata; `motivasyon` IZGARADAN DEĞİL TOHUMDAN (T95, §1c) ──
    ESLEME = {"ic_motivasyon": "ic", "aile_baskisi": "aile_baskisi",
              "yasal_zorunluluk": "yasal_zorunluluk",
              "tetikleyici_olay": "ic", "duygusal_regulasyon": "ic"}

    # ⭐⭐ KATMANLI ÖRNEKLEME — T95'in düzeltmesi ikinci bir kusuru açığa çıkardı.
    # `motivasyon` ızgara sütunuyken hiçbir şeyi kısıtlamıyordu ve gerçek değeri
    # `ic`e eziyordu (T95). Tohumdan OKUNMAYA başlayınca görüldü ki `P1.sec`
    # dosya sırasındaki İLK eşleşmeyi alıyor ve o sıra motivasyona göre yansız
    # değil: ilk çözümde `aile_baskisi` **%50** çıktı, havuzda **%27**.
    # ⇒ Sapma ne tasarım ne de havuzun dağılımı; **dosya sırasının artefaktı**.
    # ⛔ `P1.sec` DEĞİŞTİRİLMİYOR (Kural 7: parti1/parti2 çıktıları ona dayanıyor);
    # katmanlama DIŞARIDAN, havuzu önceden süzerek yapılıyor.
    # ⚠️ Hedef = havuzun kendi dağılımı (temsil). `yasal_zorunluluk`u T2 için
    # BİLEREK fazla örneklemek ayrı ve AÇIK bir karar olmalı — kazayla değil.
    hp = Counter(ESLEME.get(t["meta"].get("motivasyon"), "ic") for t in hav)
    toplam = sum(hp.values())
    pay = {k: round(N * v / toplam) for k, v in hp.items()}
    while sum(pay.values()) != N:                 # yuvarlama artığı en büyüğe
        en = max(pay, key=lambda k: pay[k])
        pay[en] += 1 if sum(pay.values()) < N else -1
    print(f"   katmanlı hedef (havuz dağılımı): {pay}")
    sirali = sorted(izgara, key=lambda s: s["sira"])
    kalan = dict(pay)
    # ⭐ ZATEN ÜRETİLMİŞ satırların tohumu SABİTLENİR. Gerekçe ölçüldü: `sec()`
    # dosya sırasındaki ilk eşleşmeyi alıyor, bu yüzden havuzdan tek bir tohum
    # çıkarmak SONRAKİ BÜTÜN satırları yeniden diziyor — kriz süzgeci
    # sıkılaştırılınca parti4'ün 15 üretilmiş kaydının 15'i de plandan koptu.
    # ⇒ Üretilmiş kayıt varsa onun tohumu korunur; plan ile kayıt ayrışmaz.
    SABIT: dict[int, str] = {}
    _sabit_yol = os.environ.get("BIRAG_PLAN_SABIT", "")
    if _sabit_yol:
        for _l in (KOK / _sabit_yol).read_text(encoding="utf-8").splitlines():
            if _l.strip():
                _r = json.loads(_l)
                SABIT[_r["gen_meta"]["parti_sira"]] = _r["gen_meta"]["seed_id"]
        print(f"   ⭐ {len(SABIT)} satırın tohumu SABİTLENDİ (üretilmiş kayıtlar)")
    # ⚠️ SABİTLENMİŞ tohumlar `havuz()`ta YOK: üretilmiş oldukları için
    # `kullanilmis()` onları eliyor. Bu yüzden ham tohum dosyasından okunuyor.
    _tum = {t["seed_id"]: t for t in
            (json.loads(x) for x in (KOK / "data/seeds.jsonl").open(encoding="utf-8"))}
    alinmis: set[str] = set(SABIT.values())
    eksik = []
    for s in sirali:
        s["havuz"] = None
        if s["sira"] in SABIT:                 # sabitlenmiş satır: seçici atlanır
            t = _tum.get(SABIT[s["sira"]])
            if t is None:                      # süzgeç onu elemiş olabilir
                eksik.append(s["sira"]); continue
            m = t["meta"].get("motivasyon")
            s.update({"seed_id": t["seed_id"], "source_id": t["source_id"],
                      "tohum_senaryo": t["meta"].get("senaryo"),
                      "tohum_kelime": len(t["user_message"].split()),
                      "tohum_metin": t["user_message"],
                      "motivasyon": ESLEME.get(m, "ic"), "motivasyon_tohum": m,
                      "motivasyon_geri_dusme": m not in ("ic_motivasyon", "aile_baskisi",
                                                         "yasal_zorunluluk")})
            continue
        # kotası kalan motivasyon katmanlarını sırayla dene
        t = None
        for kat in sorted(kalan, key=lambda k: -kalan[k]):
            if kalan[kat] <= 0:
                continue
            altkume = [x for x in hav
                       if ESLEME.get(x["meta"].get("motivasyon"), "ic") == kat]
            t = P1.sec(s, altkume, alinmis)
            if t is not None:
                kalan[kat] -= 1
                break
        if t is None:                              # katman bulunamadı: serbest seç
            t = P1.sec(s, hav, alinmis)
        if t is None:
            eksik.append(s["sira"]); continue
        alinmis.add(t["seed_id"])
        m = t["meta"].get("motivasyon")
        s.update({"seed_id": t["seed_id"], "source_id": t["source_id"],
                  "tohum_senaryo": t["meta"].get("senaryo"),
                  "tohum_kelime": len(t["user_message"].split()),
                  "tohum_metin": t["user_message"],
                  "motivasyon": ESLEME.get(m, "ic"),        # ⭐ tohumdan
                  "motivasyon_tohum": m,                     # ⭐ ham değer görünür
                  "motivasyon_geri_dusme": m not in ("ic_motivasyon", "aile_baskisi",
                                                     "yasal_zorunluluk")})
    if eksik:
        raise SystemExit(f"⛔ tohum bulunamayan satır: {eksik}")

    CIKTI.write_text("".join(json.dumps(s, ensure_ascii=False) + "\n" for s in izgara),
                     encoding="utf-8")
    print(f"✅ kotalar ve hücre yasakları tuttu · {len(izgara)} satır → {CIKTI.relative_to(KOK)}")
    print(f"   motivasyon (TOHUMDAN): {dict(Counter(s['motivasyon'] for s in izgara))}")
    print(f"   ↳ geri düşen (K22'de karşılığı yok): "
          f"{sum(s['motivasyon_geri_dusme'] for s in izgara)}")
    print(f"   bağlam is_negative {bn}/{BAGLAM_NEG_ASGARI} (§7a `cevap_yok` için)")
    print(f"   bağlam {sum(s['context'] for s in izgara)} · §8b "
          f"{sum(1 for s in izgara if s['sinir_tipi'] != 'yok')} · nazikçe karşı çıkma "
          f"{sum(1 for s in izgara if s['senaryo_hedefi'] == 'nazikce_karsi_cikma')}")
    print(f"   kisa×takdir {sum(1 for s in izgara if s['bicim']=='kisa' and s['turn_ending']=='takdir')}"
          f" (tavan {KISA_TAKDIR_TAVAN}) · kisa×single×yok "
          f"{sum(1 for s in izgara if s['bicim']=='kisa' and s['turn_type']=='single' and s['sinir_tipi']=='yok')} (yasak)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
