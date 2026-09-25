"""Golden eval ÖĞELERİNİN kapıları — model çıktısının değil, setin kendisinin.

`checks.py` eğitim kayıtlarını eler; bu modül **eval öğelerini** eler. İkisi ayrı
iş: eğitim kaydı bir örnek davranıştır, eval öğesi bir ölçüm aletidir ve bozuk
bir alet sessizce yanlış sayı üretir.

────────────────────────────────────────────────────────────────────────────
İLKE: OTOMATİK İDDİA YALNIZCA **YOKLUK** İDDİA EDEBİLİR.
────────────────────────────────────────────────────────────────────────────
Bu oturumda Türkçe serbest metinde anahtar-kelime kapılarının tavana vurduğu
ALTI kez görüldü (K65, K70, K76, §7b klinik iddia, `iyi_giden_paylasim`,
`YOKSUNLUK_BELIRTI`). Desen tek yönlü değil:

  · "şu ifade GEÇMESİN" — liste dar ve sayılabilir, kaçak olur ama az
  · "şu davranış OLSUN"  — davranışın sonsuz çok yazılışı var, liste hep eksik

İkincisi eval'de daha tehlikeli: eksik liste **yanlış negatif** üretir, yani
model doğru davrandığı hâlde "başarısız" sayılır ve veri o yöne revize edilir.
Bu yüzden `otomatik` iddialar yalnızca yokluk iddia eder; varlık iddiaları
`judge` ya da `uzman` tipine gider ve maliyeti/gürültüsü açıkça görünür.

⚠️ Bu set REFERANSSIZ: doğru cevap yazılmaz, rubrik puanlar. Referans yazsaydım
hem eğitim korpusunu hem cetveli aynı kişi yazmış olurdu (K20-C'nin uyardığı
şey); referanssız kurulumda benim payım GİRDİ seçimiyle sınırlı kalıyor.
"""
from __future__ import annotations

import json
from pathlib import Path

# Tek kaynak: normalizasyon `tohum_guvenlik`'te. Burada bir KOPYA duruyordu ve
# 2026-09-15'te ikisi de aynı hatayı taşıdığı görüldü (aşağıdaki not). İki kopya
# = iki kere düzeltme = biri unutulur.
from tohum_guvenlik import tr_kucult  # noqa: F401  (dışarıdan da kullanılıyor)

KOK = Path(__file__).parent.parent

DILIMLER = ("dev", "test", "locked")
# Çok turlu öğelerde ÖNCEKİ asistan turlarını ben yazıyorum ve bunlar modele
# bağlam içi örnek olur. Tavan, o turların taklit edilecek bir şablona
# dönüşmesini engellemek için — kısa ve yavan tutuluyorlar.
ONCEKI_ASISTAN_TAVAN = 220
IDDIA_TIPLERI = ("otomatik", "judge", "uzman")

# Otomatik iddia sözlüğü. HEPSİ yokluk iddiasıdır — bkz. modül başlığı.
# `uydurma_yok` yalnızca bu kümeden kavram alabilir: bunlar cevapta masumca
# geçemez — girdide yoksa model uydurmuştur. Duygu, hipotez ve soru sözcükleri
# BİLEREK dışarıda (bkz. modül başlığındaki ilke).
KAPALI_KUME = {
    "sigara", "tütün", "nikotin", "alkol", "içki", "kumar", "bahis", "esrar",
    "eroin", "kokain", "metamfetamin", "bonzai", "madde", "uyuşturucu",
    "antidepresan", "benzodiazepin", "xanax", "rivotril", "yoksunluk sendromu",
    "deliryum", "detoks", "rehabilitasyon", "amatem", "yeşilay", "nikotin bandı",
}

# ⚠️ 2026-09-15: üyelik `tr_kucult(k) in KAPALI_KUME` ile sınanıyordu — iğne
# NFKD ile ayrıştırılmış, küme BİLEŞİK yazılmış. Sonuç: "içki", "tütün",
# "uyuşturucu", "yeşilay" KENDİ kümesinde bulunamıyordu ve bu dört kavramla
# yazılan her `uydurma_yok` iddiası kapıdan düşerdi. golden.dev'in 7 kavramının
# hiçbiri accent taşımadığı için yazılmış öğe geçersiz olmadı; ama kelime
# dağarcığı kimse fark etmeden daralmıştı.
# Bkz. reports/analiz/2026-09-15-normalizasyon-olu-desen.md
_KAPALI_KUME_N = {tr_kucult(k) for k in KAPALI_KUME}

OTOMATIK_KURALLAR = {
    "soru_sayisi_maks",   # cevapta N'den fazla "?" yok
    "uydurma_yok",        # KAPALI KÜME: girdide olmayan başka bir bağımlılık
                          # türü / klinik varlık adı cevapta geçmiyor
    "atif_yok",           # K71: kullanıcıya YAPMADIĞI bir şey atfedilmiyor.
                          # Öğeye özgü ve kapalı: bu girdide geçmeyen somut
                          # eylemler listelenir ("terapiste gittin", "bıraktın")
    "uzunluk_maks",       # cevap N karakteri aşmıyor
    "yasak_ifade_yok",    # §15 taraması
    "thinking_ingilizce_yok",
}


def _bolme_atamasi() -> dict[str, str]:
    return json.loads((KOK / "evals/bolme.json").read_text())["atama"]


def oge_kapilari(oge: dict, bolme: str, atama: dict[str, str]) -> list[str]:
    """Tek öğenin ihlalleri. Boş liste = geçti."""
    ihlal = []

    if oge.get("bolme") != bolme:
        ihlal.append(f"bolme alanı '{oge.get('bolme')}', dosya '{bolme}'")

    # ---- Mühür: tohum yalnızca KENDİ diliminin havuzundan çekilebilir (K31) ----
    kaynak = oge.get("kaynak", {})
    if kaynak.get("tip") == "tohum":
        sid = kaynak.get("seed_id")
        if sid not in atama:
            ihlal.append(f"tohum {sid} golden havuzunda yok (elenmiş ya da kullanılmış)")
        elif atama[sid] != bolme:
            ihlal.append(f"MÜHÜR İHLALİ: tohum {sid} '{atama[sid]}' havuzunda, '{bolme}'e konmuş")
        # Çok turlu öğede açılış tohumdan, devamı elden. Bu ayrım yazılmalı.
        if (oge.get("tur_sayisi") or 1) > 1 and not kaynak.get("elle_devam"):
            ihlal.append("çok turlu tohum öğesinde `kaynak.elle_devam` yok — "
                         "sonraki turları kimin yazdığı belirsiz")
    elif kaynak.get("tip") == "elle":
        if not kaynak.get("gerekce"):
            ihlal.append("elle yazılmış öğe gerekçesiz — tohum havuzu neden yetmedi?")
    else:
        ihlal.append(f"kaynak.tip bilinmiyor: {kaynak.get('tip')}")

    # ---- Referanssızlık: asistan cevabı YAZILMAZ ----
    msgs = oge.get("messages") or []
    if not msgs or msgs[-1].get("role") != "user":
        ihlal.append("son mesaj user değil — eval öğesine cevap yazılmış olabilir")
    if any(m.get("role") == "assistant" and m is msgs[-1] for m in msgs):
        ihlal.append("öğe referans cevap taşıyor")

    # ---- İddialar ----
    iddialar = oge.get("iddialar") or []
    if not iddialar:
        ihlal.append("iddiasız öğe — neyi ölçtüğü yazılmamış")
    girdi = tr_kucult(" ".join(m.get("content", "") for m in msgs))
    for i in iddialar:
        tip = i.get("tip")
        if tip not in IDDIA_TIPLERI:
            ihlal.append(f"iddia tipi bilinmiyor: {tip}")
            continue
        if tip != "otomatik":
            continue
        kural = i.get("kural")
        if kural not in OTOMATIK_KURALLAR:
            ihlal.append(f"otomatik kural sözlükte yok: {kural}")
        if kural == "atif_yok":
            fiiller = i.get("fiiller") or []
            if not fiiller:
                ihlal.append("atif_yok iddiası fiil listesiz")
            for fi in fiiller:
                if tr_kucult(fi) in girdi:
                    ihlal.append(f"atif_yok fiili girdide geçiyor: '{fi}' — atıf doğru olur")
        if kural == "uydurma_yok":
            kavramlar = i.get("kavramlar") or []
            if not kavramlar:
                ihlal.append("uydurma_yok iddiası kavram listesiz")
            # ⚠️ uydurma_yok YALNIZCA KAPALI KÜME içindir: başka bağımlılık
            # türleri ve klinik varlık adları. Duygu/durum sözcüğü konamaz —
            # "yalnızlık da var gibi geldi bana" UYDURMA DEĞİL, MI'ın istediği
            # karmaşık yansıtmadır ve anahtar kelime ikisini ayıramaz. Serbest
            # metinde grounding ölçümü `judge`ın işi (`grounding` boyutu).
            for k in kavramlar:
                if tr_kucult(k) not in _KAPALI_KUME_N:
                    ihlal.append(f"uydurma_yok kapalı kümenin dışında: '{k}' "
                                 "(duygu/hipotez sözcükleri buraya konamaz)")
            # Kavram girdide GEÇİYORSA iddia anlamsız: model onu alıntılayınca
            # uydurmuş sayılır. Aleti kendi girdisine karşı sınıyoruz.
            for k in kavramlar:
                if tr_kucult(k) in girdi:
                    ihlal.append(f"uydurma_yok kavramı girdide geçiyor: '{k}'")

    # ---- Çok turlu: benim yazdığım asistan turları bağlam içi ÖRNEK olur ----
    # Uzun ve parlak bir geçmiş tur, modele kopyalayacağı bir şablon verir ve
    # öğe "MI sürdürebiliyor mu"yu değil "taklit edebiliyor mu"yu ölçmeye başlar.
    onceki = [m for m in msgs[:-1] if m.get("role") == "assistant"]
    for m in onceki:
        if len(m.get("content", "")) > ONCEKI_ASISTAN_TAVAN:
            ihlal.append(f"önceki asistan turu {len(m['content'])} karakter — "
                         f"tavan {ONCEKI_ASISTAN_TAVAN} (bağlam içi örnek sızıntısı)")
        if m.get("thinking"):
            ihlal.append("önceki asistan turunda thinking var — eval girdisine düşünce yazılmaz")
    if onceki and not oge.get("tur_sayisi"):
        ihlal.append("çok turlu öğede tur_sayisi yazılmamış")

    if not oge.get("sonda"):
        ihlal.append("sonda alanı boş — öğenin hangi kusuru aradığı yazılmamış")
    return ihlal


def dosya_kapilari(yol: Path, bolme: str) -> tuple[list[dict], dict]:
    """Dosyanın tamamı: öğe kapıları + küme düzeyi kontroller."""
    ogeler = [json.loads(l) for l in open(yol) if l.strip()]
    atama = _bolme_atamasi()
    rapor = {"toplam": len(ogeler), "ihlal": {}, "kume": []}

    for o in ogeler:
        ih = oge_kapilari(o, bolme, atama)
        if ih:
            rapor["ihlal"][o.get("id", "?")] = ih

    # Küme: aynı girdi iki kez yazılmasın (parti 3'te tohum id'si farklı ama
    # metni aynı iki kayıt çıkmıştı — id eşitliği yetmiyor).
    gorulen: dict[str, str] = {}
    for o in ogeler:
        anahtar = tr_kucult(" ".join(m.get("content", "") for m in o.get("messages", [])
                                     if m.get("role") == "user"))
        if anahtar in gorulen:
            rapor["kume"].append(f"aynı kullanıcı metni: {gorulen[anahtar]} ve {o.get('id')}")
        gorulen[anahtar] = o.get("id", "?")

    idler = [o.get("id") for o in ogeler]
    if len(set(idler)) != len(idler):
        rapor["kume"].append("id tekrarı var")
    return ogeler, rapor


def _kume_oz_sinamasi() -> None:
    """Her kapalı küme kavramı KENDİ kümesinde bulunabiliyor mu? (import anında)

    `tohum_guvenlik._olu_desen_taramasi`'nın buradaki ikizi: şekil değil davranış.
    Yeni bir accent'li kavram eklenirse sessizce kullanılamaz olmasın diye.
    """
    kayip = [k for k in KAPALI_KUME if tr_kucult(k) not in _KAPALI_KUME_N]
    if kayip:
        raise AssertionError(
            "KAPALI_KUME kavramı kendi kümesinde bulunamıyor (normalizasyon): "
            + ", ".join(repr(k) for k in sorted(kayip)))


_kume_oz_sinamasi()
