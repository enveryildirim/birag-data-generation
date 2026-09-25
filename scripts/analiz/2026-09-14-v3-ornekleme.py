#!/usr/bin/env python3
"""v3 üretimi — ilk parti (40 kayıt) örnekleme planı.

⚠️ ÇIKTI DONDURULDU (2026-09-14). data/plan/v3-parti1.jsonl üretildi; kayıtlar bu
plana göre ELLE yazılacak. Betik belirlenimli ama KODU (özellikle PLAN tablosunu,
PIN'i ya da RASTGELE tohumunu) değiştirip yeniden koşmak tohum→satır atamasını
kaydırır ve yazılmış kayıtlarla uyumu bozar. Değişiklik gerekiyorsa: plan dosyasına
dokunma, sapmayı üretim betiğindeki DEGISIM tablosuna yaz.

v2'nin planından FARKI: `turn_ending`, `konusma_durumu` ve `mi_process` burada
**tasarlanır**, üretimde ortaya çıkmaz. v2'de bunlar serbest bırakıldı ve
sonuç 68/70 soruyla biten, %81 engaging bir korpus oldu (K54/K55).

Bu betik bir dağılım ÜRETMİYOR, elle tasarlanmış PLAN tablosunu **doğruluyor**
ve her satıra uygun bir tohum atıyor. Doğrulama başarısızsa plan yazılmaz.

Kural:
  · v0.0.1 (20) + ablasyon (12) + expert-70 (70) tohumları HARİÇ
  · senaryo == kriz ve risk == cok_yuksek HARİÇ (AGENTS Kural 3)
  · ⚠️ metadata yetmiyor — kriz İÇERİK taraması da uygulanır (K52)
  · içerik gerektiren arketip, tohumda dayanağı yoksa ATANMAZ (Kural 3)

Girdi : data/seeds.jsonl · data/candidates/expert-70.jsonl
Çıktı : data/plan/v3-parti1.jsonl + reports/analiz/2026-09-14-v3-ornekleme.md
"""
from __future__ import annotations

import collections
import hashlib
import json
import pathlib
import random
import re
import sys

KOK = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "scripts/analiz"))
SEEDS = KOK / "data/seeds.jsonl"
KULLANILAN = KOK / "data/candidates/expert-70.jsonl"
CIKTI_JSONL = KOK / "data/plan/v3-parti1.jsonl"
CIKTI_RAPOR = KOK / "reports/analiz/2026-09-14-v3-ornekleme.md"
RASTGELE = random.Random(103)

# ── v3 hedefleri (prompts/uretim-v3.md) ──────────────────────────────────────
HEDEF = {
    "turn_ending": {"acik_uclu_soru": .50, "takdir": .15, "ozet": .15,
                    "yalnizca_yansitma": .15, "durur": .05},
    "konusma_durumu": {"tetikleyici_an": .35, "suregiden_durum": .20,
                       "iyi_giden_paylasim": .15, "plan_yapma": .15,
                       "merak_sorusu": .10, "aradan_donus": .05},
    "mi_process": {"engaging": .40, "focusing": .20, "evoking": .25, "planning": .15},
    "sysvar": {"canon": .775, "paraphrase": .225},
}
HEDEF_IS_NEGATIVE, HEDEF_ERGEN, HEDEF_MULTI, HEDEF_OZERKLIK = .15, .15, .25, .20
BANT = .05   # ±5 puan — korpus raporuyla aynı konvansiyon (Kural 6)

# ── PLAN: 40 satır, elle tasarlandı ──────────────────────────────────────────
# (senaryo, tur, yas, turn_type, mi_process, konusma_durumu, turn_ending,
#  sysvar, is_negative, ozerklik)
# `ozerklik`: K63 — özerklik cümlesi bu kayıtta GÖRÜNÜR olacak (hedef ~%20).
P = [
    # ── tetikleyici an (14) — dürtü, duraklama; çoğu engaging ────────────────
    ("durtu",            "alkol",        "yetiskin", "single", "engaging", "tetikleyici_an", "acik_uclu_soru",    "canon",      0, 0),
    ("durtu",            "kumar",        "yetiskin", "single", "engaging", "tetikleyici_an", "yalnizca_yansitma", "canon",      0, 0),
    ("durtu",            "tutun",        "ergen",    "single", "engaging", "tetikleyici_an", "acik_uclu_soru",    "paraphrase", 0, 0),
    ("kayma_nuks",       "alkol",        "yetiskin", "single", "engaging", "tetikleyici_an", "yalnizca_yansitma", "canon",      0, 0),
    ("kayma_nuks",       "receteli_ilac","yetiskin", "multi",  "evoking",  "tetikleyici_an", "acik_uclu_soru",    "canon",      0, 1),
    ("ambivalans",       "tutun",        "yetiskin", "single", "engaging", "tetikleyici_an", "acik_uclu_soru",    "canon",      0, 0),
    ("ambivalans",       "kumar",        "yetiskin", "multi",  "evoking",  "tetikleyici_an", "ozet",              "paraphrase", 0, 1),
    ("inkar",            "alkol",        "yetiskin", "single", "engaging", "tetikleyici_an", "yalnizca_yansitma", "canon",      0, 0),
    ("discord",          "dijital",      "ergen",    "single", "engaging", "tetikleyici_an", "durur",             "canon",      0, 1),
    ("anlasilmama",      "receteli_ilac","yetiskin", "single", "engaging", "tetikleyici_an", "yalnizca_yansitma", "canon",      0, 0),
    ("bilmiyorum_cikmazi","alkol",       "yetiskin", "single", "focusing", "tetikleyici_an", "acik_uclu_soru",    "canon",      0, 0),
    ("borc_finansal",    "kumar",        "yetiskin", "single", "engaging", "tetikleyici_an", "acik_uclu_soru",    "canon",      0, 0),
    ("rol_siniri",       "receteli_ilac","yetiskin", "single", "engaging", "tetikleyici_an", "acik_uclu_soru",    "paraphrase", 1, 1),
    ("kayip_kovalama",   "kumar",        "yetiskin", "single", "engaging", "tetikleyici_an", "yalnizca_yansitma", "canon",      0, 0),

    # ── süregiden durum (8) — "bu hafta şöyle geçti" ─────────────────────────
    ("ambivalans",       "alkol",        "yetiskin", "multi",  "focusing", "suregiden_durum", "ozet",             "canon",      0, 0),
    ("inkar",            "tutun",        "yetiskin", "single", "focusing", "suregiden_durum", "acik_uclu_soru",   "canon",      0, 0),
    ("farkindalik",      "dijital",      "ergen",    "single", "evoking",  "suregiden_durum", "ozet",             "canon",      0, 0),
    ("motivasyon",       "kumar",        "yetiskin", "multi",  "evoking",  "suregiden_durum", "acik_uclu_soru",   "paraphrase", 0, 0),
    ("nazikce_karsi_cikma","alkol",      "yetiskin", "single", "focusing", "suregiden_durum", "acik_uclu_soru",   "canon",      0, 1),
    ("anlasilmama",      "tutun",        "yetiskin", "single", "engaging", "suregiden_durum", "yalnizca_yansitma","canon",      0, 0),
    ("hukuki_kaygi",     "alkol",        "yetiskin", "single", "focusing", "suregiden_durum", "acik_uclu_soru",   "canon",      1, 1),
    ("borc_finansal",    "kumar",        "yetiskin", "multi",  "focusing", "suregiden_durum", "ozet",             "canon",      0, 0),

    # ── iyi giden bir şeyin paylaşımı (6) — takdir ağırlıklı ────────────────
    ("kutlama",          "tutun",        "yetiskin", "single", "engaging", "iyi_giden_paylasim", "takdir",        "canon",      0, 0),
    ("motivasyon",       "alkol",        "yetiskin", "single", "evoking",  "iyi_giden_paylasim", "takdir",        "paraphrase", 0, 0),
    ("farkindalik",      "kumar",        "yetiskin", "single", "evoking",  "iyi_giden_paylasim", "takdir",        "canon",      0, 0),
    ("motivasyon",       "receteli_ilac","yetiskin", "multi",  "evoking",  "iyi_giden_paylasim", "ozet",          "canon",      0, 0),
    ("farkindalik",      "dijital",      "ergen",    "single", "engaging", "iyi_giden_paylasim", "takdir",        "canon",      0, 0),
    ("farkindalik",      "kumar",        "yetiskin", "single", "engaging", "iyi_giden_paylasim", "takdir",        "canon",      0, 0),

    # ── plan yapma (6) — planning süreci burada yoğunlaşıyor ────────────────
    ("hedef_belirleme",  "tutun",        "yetiskin", "multi",  "planning", "plan_yapma", "acik_uclu_soru",        "canon",      0, 0),
    ("hedef_belirleme",  "alkol",        "yetiskin", "single", "planning", "plan_yapma", "ozet",                  "canon",      0, 1),
    ("hedef_belirleme",  "kumar",        "yetiskin", "multi",  "planning", "plan_yapma", "acik_uclu_soru",        "paraphrase", 0, 0),
    ("kayma_nuks",       "tutun",        "yetiskin", "single", "planning", "plan_yapma", "acik_uclu_soru",        "canon",      0, 0),
    ("motivasyon",       "dijital",      "ergen",    "multi",  "planning", "plan_yapma", "ozet",                  "canon",      0, 0),
    ("hedef_belirleme",  "receteli_ilac","yetiskin", "single", "planning", "plan_yapma", "durur",                 "canon",      0, 1),

    # ── merak / bilgi sorusu (4) — is_negative burada yoğun ─────────────────
    ("bilgilendirme",    "tutun",        "yetiskin", "single", "focusing", "merak_sorusu", "acik_uclu_soru",      "canon",      1, 0),
    ("bilgilendirme",    "receteli_ilac","yetiskin", "single", "focusing", "merak_sorusu", "acik_uclu_soru",      "paraphrase", 1, 0),
    ("rol_siniri",       "alkol",        "yetiskin", "single", "engaging", "merak_sorusu", "acik_uclu_soru",      "canon",      1, 1),
    ("bilgilendirme",    "dijital",      "ergen",    "single", "focusing", "merak_sorusu", "yalnizca_yansitma",   "canon",      0, 0),

    # ── aradan sonra dönüş (2) ──────────────────────────────────────────────
    ("motivasyon",       "alkol",        "yetiskin", "single", "engaging", "aradan_donus", "takdir",              "paraphrase", 0, 0),
    ("kayma_nuks",       "kumar",        "yetiskin", "multi",  "evoking",  "aradan_donus", "acik_uclu_soru",      "canon",      0, 0),
]
# ── PIN: anahtar kelime kapısının yanlış eşlediği satırlar ELLE düzeltildi ──
# v2'de aynı kusur çıkmıştı ("işaret" → yoksunluk titremesine sanrili_soylem).
# Kapı kalıbı yakalar, anlamı değil (K40). Her satır OKUNARAK seçildi.
PIN = {
    21: "13894df524",  # "avukat" eşleşmesi YANLIŞTI: kullanıcı avukatın KENDİSİydi,
                       # ortada hukuki kaygı yoktu. Yerine: denetimli serbestlik + İK görüşmesi
    23: "f8d0ff7a82",  # "hiç içmedim" eşleşmesi YASI yakalamıştı ("o anneyi geri istiyorum").
                       # Yerine: "on gün oldu sigarasız", koşuya başlamış — gerçek ilerleme
    24: "6c330fd299",  # "kutlamasında içtim" = NÜKS hikâyesiydi. Yerine: "bir hafta oldu
                       # içmiyorum", tahlil sabırsızlığı → senaryo kutlama→motivasyon
    28: "4934904eb0",  # "10 gün oldu" TIRMANMAYI yakalamıştı. Yerine: GA toplantısına
                       # ilk kez katılmış → senaryo kutlama→farkindalik
    3:  "25a3142b37",  # Yaş gevşetmesi 32 yaşında evli bir adamın hikâyesini ERGEN satırına
                       # koymuştu ("Murat. Otuz iki. Eşim…"). İçerik ergen kaydına
                       # dönüştürülemez — başka biri uydurmak olur (K64 sınırı).
                       # Yerine: sınav stresi + tuvalette arkadaşın Juul'u — gerçek ergen
    35: "4e7f762f5c",  # Tohum "direksiyonda gözüm kapandı" idi — bilgi sorusu değil GÜVENLİK
                       # olayı, üstelik kriz taramasında yok. Yerine: "Slim daha az zararlı" miti
    38: "85e9203fa0",  # Tohum anlaşılmama anlatıyordu. Yerine: "telefonu bırakıp parka gittim,
                       # o iyi his neden devam etmiyor?" — gerçek merak sorusu
}

# ⚠️ KRİZ TARAMASI AÇIĞI (2026-09-14, bu planda bulundu)
# Tohum b96f72d01a: "direksiyonda bir anlığına gözüm kapandı" — uyuşukluk hâlinde
# araç kullanma. KRIZ_ANAHTAR listesinde karşılığı yok, metadata'da risk=yuksek ama
# senaryo=belirsiz. Kriz dilimine girmiyor ama olağan akışta da üretilmemeli:
# doğru cevap güvenlik konuşması gerektiriyor ve o davranış uzman onayına bağlı (Kural 3).
# Bu partide kullanılmadı. Liste genişletme kararı uzman Oturum 1'e bırakıldı.
ELENEN_GUVENLIK = {"b96f72d01a": "uyuşukluk hâlinde araç kullanma — kriz listesinde yok"}

ALANLAR = ("senaryo", "tur", "yas", "turn_type", "mi_process",
           "konusma_durumu", "turn_ending", "sysvar", "is_negative", "ozerklik")
PLAN = [dict(zip(ALANLAR, satir)) for satir in P]

# ── içerik kapıları — 2026-09-14-uzman-ornekleme.py'den kopyalandı ───────────
# Kopya, import değil: o betiğin çıktısı DONDURULMUŞ durumda (expert-70'in planı),
# import etmek onu çalıştırma riski taşır. Tablolar veri, kaynak orada.
KRIZ_ANAHTAR = [
    "yaşamak istemiyorum", "ölmek istiyorum", "intihar", "canıma kıy", "kendimi asa",
    "kendime zarar", "bitirmek istiyorum", "son vermek istiyorum", "uyanmasam",
    "uyanmak istemiyorum", "yaşamaya değmez", "hayatıma son", "bileğimi", "hapları içt",
    "yok olmak istiyorum", "ölsem", "öldürmek istiyorum kendimi", "yük oluyorum",
    "bensiz daha iyi", "dayanamıyorum artık", "kurtulmak istiyorum bu hayattan",
    "acil servis", "acilde", "ambulans", "mide yıkan", "yoğun bakım", "doz aşımı",
    "aşırı doz", "taburcu", "entübe", "komaya",
]
SENARYO_ANAHTAR = {
    "hukuki_kaygi": ["mahkeme", "dava", "savcı", "tck", "denetimli", "adli", "polis",
                     "ceza", "avukat", "kovuşturma", "karakol", "ehliyet", "trafik",
                     "zorunlu rehabilitasyon", "hüküm"],
    "borc_finansal": ["borç", "tefeci", "kredi", "icra", "faiz", "haciz", "taksit",
                      "maaşım", "ödeyemiyorum", "batt", "kart limiti"],
    "kayip_kovalama": ["kaybett", "geri almak", "geri kazan", "açığı kapat", "son bir",
                       "kovala", "zararı kapat", "kaybımı"],
    "rol_siniri": ["ne yapmalıyım", "ne yapayım", "sen söyle", "sen karar", "tarafsız",
                   "haklı mıyım", "bir formül", "bir sistem", "bir plan ver", "reçete",
                   "önerir misin", "tavsiye et", "doktor musun", "teşhis", "kaç gün",
                   "kaç mg", "bana bir yol"],
    "durtu": ["canım çekiyor", "içimden geçiyor", "elim gidiyor", "parmağım", "dayanamıyorum",
              "içim gidiyor", "indirsem", "yüklesem", "açsam mı", "şu an istiyorum",
              "ayağım kendiliğinden", "elim uzandı", "çekiyor canım"],
    "discord": ["sen de mi", "boşver", "anlamıyorsun", "kapatıyorum", "saçmala",
                "işe yaramıyor", "robot", "makine", "ne anlarsın", "bırak şimdi",
                "boş konuşma", "nutuk"],
    "anlasilmama": ["anlamıyor", "anlatamıyorum", "anlamaz", "kimse anlamıyor",
                    "beni anlamıyorsun", "anlaşılmıyorum"],
    "bilmiyorum_cikmazi": ["bilmiyorum", "kafam karışık", "karar veremiyorum",
                           "ne yapacağımı bilmiyorum", "emin değilim"],
    "kutlama": ["gün oldu", "ay oldu", "hiç içmedim", "hiç oynamadım", "başardım",
                "bir yıl oldu", "kutla", "hiç sigara"],
    "bilgilendirme": ["nedir", "nasıl olur", "doğru mu", "ne yapar", "zararlı mı",
                      "öğrenmek istiyorum", "bilgi", "gerçekten", "işe yarar mı"],
}


def kriz_icerigi(t):
    metin = (t["user_message"] + " " + t.get("scenario_context", "")).lower()
    return [a for a in KRIZ_ANAHTAR if a in metin]


def senaryo_uygun(t, senaryo):
    anahtarlar = SENARYO_ANAHTAR.get(senaryo)
    if not anahtarlar:
        return True
    metin = (t["user_message"] + " " + t.get("scenario_context", "")).lower()
    return any(a in metin for a in anahtarlar)


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def dogrula() -> list[str]:
    """PLAN tablosu v3 hedeflerini tutuyor mu? Tutmuyorsa plan YAZILMAZ."""
    n, sorun = len(PLAN), []
    for alan, hedefler in HEDEF.items():
        sayim = collections.Counter(s[alan] for s in PLAN)
        for anahtar, hedef in hedefler.items():
            oran = sayim.get(anahtar, 0) / n
            if abs(oran - hedef) > BANT:
                sorun.append(f"{alan}.{anahtar}: %{oran*100:.0f} (hedef %{hedef*100:.0f})")
        for fazla in set(sayim) - set(hedefler):
            sorun.append(f"{alan}.{fazla}: tanımsız değer")
    for ad, alan, hedef in [("is_negative", "is_negative", HEDEF_IS_NEGATIVE),
                            ("özerklik", "ozerklik", HEDEF_OZERKLIK)]:
        oran = sum(s[alan] for s in PLAN) / n
        if abs(oran - hedef) > BANT:
            sorun.append(f"{ad}: %{oran*100:.0f} (hedef %{hedef*100:.0f})")
    for ad, kosul, hedef in [("ergen", lambda s: s["yas"] == "ergen", HEDEF_ERGEN),
                             ("multi", lambda s: s["turn_type"] == "multi", HEDEF_MULTI)]:
        oran = sum(1 for s in PLAN if kosul(s)) / n
        if abs(oran - hedef) > BANT:
            sorun.append(f"{ad}: %{oran*100:.0f} (hedef %{hedef*100:.0f})")
    return sorun


def kullanilmis(tohumlar) -> set[str]:
    """v0.0.1 (20) + ablasyon (12) + expert-70 (70)."""
    kaynak_id = set()
    for satir in open(KOK / "data/candidates/v0.0.1.jsonl"):
        kaynak_id.update(json.loads(satir).get("source_ids") or [])
    kul = {t["seed_id"] for t in tohumlar if t["source_id"] in kaynak_id}
    for yol in ["reports/analiz/prompt-dili-ablasyonu/generations.jsonl",
                "reports/analiz/thinking-dili-ogrenilebilirlik/dar-lora.jsonl"]:
        for satir in open(KOK / yol):
            k = json.loads(satir)
            if "seed_id" in k:
                kul.add(k["seed_id"])
    for satir in open(KULLANILAN):                      # expert-70
        kul.add(json.loads(satir)["gen_meta"]["seed_id"])
    return kul


def ata(tohumlar):
    """Her PLAN satırına tohum atar. Kısıtı en dar satırlar önce doldurulur."""
    kul = kullanilmis(tohumlar)
    havuz = [t for t in tohumlar
             if t["seed_id"] not in kul
             and t["meta"].get("senaryo") != "kriz"
             and t["meta"].get("risk_seviyesi") != "cok_yuksek"
             and not kriz_icerigi(t)
             # ⚠️ 2026-09-14: bu satır ÖNCE YOKTU. ELENEN_GUVENLIK sözlüğü gerekçesiyle
             # yazılmıştı ama filtreye bağlanmamıştı; elenmesi gereken tohum plana girdi
             # (#6). Aynı kalıbın dördüncü tekrarı: belgede yazan, kodda olmayan kural
             # (K56 tavan, K61 göstergeler, K65 kriz listesi). Gözden geçirmede yakalandı.
             and not any(t["seed_id"].startswith(o) for o in ELENEN_GUVENLIK)]
    RASTGELE.shuffle(havuz)

    # PIN anahtarları kısaltılmış önektir (rapor/okuma kolaylığı); benzersizlik sınanır.
    alinan_pin, atama_pin = set(), {}
    for sira, onek in PIN.items():
        eslesen = [t for t in havuz if t["seed_id"].startswith(onek)]
        if len(eslesen) != 1:
            raise SystemExit(f"PIN öneki {onek}: havuzda {len(eslesen)} eşleşme "
                             f"(1 bekleniyordu) — kullanılmış ya da belirsiz olabilir")
        t = eslesen[0]
        atama_pin[sira - 1] = t
        alinan_pin.add(t["seed_id"])

    sirali = sorted(range(len(PLAN)),
                    key=lambda i: (PLAN[i]["senaryo"] not in SENARYO_ANAHTAR,
                                   PLAN[i]["yas"] != "ergen"))
    alinan, atama, eksik, gevsetilen = set(alinan_pin), dict(atama_pin), [], []
    for i in sirali:
        if i in atama:
            continue
        s = PLAN[i]
        aday = None
        # 1. tercih: tür + yaş + senaryo dayanağı  → 2. tercih: yaş kısıtını gevşet
        for yas_zorunlu in (True, False):
            for t in havuz:
                if t["seed_id"] in alinan:
                    continue
                m = t["meta"]
                if m.get("bagimlilik_turu") != s["tur"]:
                    continue
                if yas_zorunlu and (m.get("yas_grubu") or "yetiskin") != s["yas"]:
                    continue
                if not senaryo_uygun(t, s["senaryo"]):
                    continue
                aday = t
                break
            if aday:
                break
        if aday is None:
            eksik.append(i)
            continue
        if (aday["meta"].get("yas_grubu") or "yetiskin") != s["yas"]:
            gevsetilen.append((i + 1, aday["meta"].get("yas_grubu"), s["yas"]))
        alinan.add(aday["seed_id"])
        atama[i] = aday
    return atama, eksik, len(havuz), gevsetilen


def main():
    tohumlar = [json.loads(s) for s in open(SEEDS)]
    sorun = dogrula()
    if sorun:
        print("PLAN hedefleri tutmuyor — plan yazılmadı:")
        for x in sorun:
            print("  ❌", x)
        sys.exit(1)

    atama, eksik, havuz_n, gevsetilen = ata(tohumlar)
    if gevsetilen:
        print("⚠️ yaş kısıtı gevşetilen satırlar (içerik uyumu ELLE doğrulanmalı): "
              + ", ".join(f"#{s} {a}→{b}" for s, a, b in gevsetilen))
    if eksik:
        print(f"⚠️ {len(eksik)} satıra tohum bulunamadı: "
              + ", ".join(f"#{i+1} {PLAN[i]['senaryo']}/{PLAN[i]['tur']}/{PLAN[i]['yas']}"
                          for i in eksik))

    CIKTI_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with open(CIKTI_JSONL, "w") as f:
        for i, s in enumerate(PLAN):
            t = atama.get(i)
            f.write(json.dumps({
                "sira": i + 1, **s,
                "seed_id": t["seed_id"] if t else None,
                "source_id": t["source_id"] if t else None,
                "tohum_senaryo": t["meta"].get("senaryo") if t else None,
                "tohum_yas": (t["meta"].get("yas_grubu") if t else None),
                "user_message": t["user_message"] if t else None,
            }, ensure_ascii=False) + "\n")

    L = ["# v3 üretimi — ilk parti örnekleme planı (40 kayıt)", "",
         f"**Girdi:** `{SEEDS.relative_to(KOK)}` · SHA256 `{sha256(SEEDS)}`  ",
         f"**Betik:** `scripts/analiz/{pathlib.Path(__file__).name}` · **Tarih:** 2026-09-14  ",
         f"**Çıktı:** `{CIKTI_JSONL.relative_to(KOK)}`  ",
         f"**Uygun tohum havuzu:** {havuz_n} (kullanılmış + kriz + çok yüksek risk çıkarıldı)  ",
         f"**Tohum atanamayan satır:** {len(eksik)}", "",
         "> Dağılım **tasarlandı**, üretimde ortaya çıkmadı. v2'de bu alanlar serbestti "
         "ve sonuç 68/70 soruyla biten, %81 `engaging` bir korpus oldu (K54). Betik "
         "dağılım üretmiyor; elle yazılmış PLAN tablosunu **doğruluyor** — hedefler "
         "tutmazsa plan yazılmaz.", "",
         "## Tasarlanan dağılım", ""]
    n = len(PLAN)
    for alan, hedefler in HEDEF.items():
        sayim = collections.Counter(s[alan] for s in PLAN)
        L += [f"### `{alan}`", "", "| Değer | Adet | Oran | Hedef |", "|---|---:|---:|---:|"]
        for k, h in hedefler.items():
            L.append(f"| `{k}` | {sayim.get(k,0)} | %{sayim.get(k,0)/n*100:.0f} | %{h*100:.0f} |")
        L += [""]
    L += ["### Diğer", "", "| Ölçüt | Adet | Oran | Hedef |", "|---|---:|---:|---:|"]
    for ad, deger, hedef in [
            ("is_negative", sum(s["is_negative"] for s in PLAN), HEDEF_IS_NEGATIVE),
            ("özerklik görünür", sum(s["ozerklik"] for s in PLAN), HEDEF_OZERKLIK),
            ("ergen", sum(1 for s in PLAN if s["yas"] == "ergen"), HEDEF_ERGEN),
            ("çok turlu", sum(1 for s in PLAN if s["turn_type"] == "multi"), HEDEF_MULTI)]:
        L.append(f"| {ad} | {deger} | %{deger/n*100:.0f} | %{hedef*100:.0f} |")
    tur = collections.Counter(s["tur"] for s in PLAN)
    sen = collections.Counter(s["senaryo"] for s in PLAN)
    L += ["", f"**Bağımlılık türü:** " + " · ".join(f"{k} {v}" for k, v in tur.most_common()),
          "", f"**Senaryo:** " + " · ".join(f"{k} {v}" for k, v in sen.most_common()), "",
          "## Tohum ataması", "",
          "| # | Senaryo | Tür | Yaş | Tur | MI | Durum | Kapanış | Tohum |",
          "|---|---|---|---|---|---|---|---|---|"]
    for i, s in enumerate(PLAN):
        t = atama.get(i)
        L.append(f"| {i+1} | {s['senaryo']} | {s['tur']} | {s['yas']} | {s['turn_type']} | "
                 f"{s['mi_process']} | {s['konusma_durumu']} | {s['turn_ending']} | "
                 f"`{t['seed_id'][:10] if t else '—'}` |")
    # ── gözden geçirme bölümü: insan gözüyle denetlenecek satırlar ──────────
    L += ["", "## Gözden geçirme — satır satır", "",
          "Her satırın tohum açılışı ve **dikkat isteyen yanı**. İşaretler:", "",
          "| İşaret | Anlamı |", "|---|---|",
          "| 🔁 | Tohumun kendi senaryosu hedeften farklı (K37 — izinli, ama okunmalı) |",
          "| 👤 | Yaş kısıtı gevşetildi: tohum farklı yaş grubundan |",
          "| 🧵 | `multi` planlandı ama tohumlar tek turlu açılış (K26) — turlar üretimde kurulacak |",
          "| ⛔ | `is_negative` — model bir şeyi yapamayacağını söyleyecek |",
          "| 🔓 | Özerklik cümlesi görünür olacak (K63) |",
          "| 📌 | Tohum elle seçildi (PIN) — kapı yanlış eşlemişti |",
          "| 🤫 | `durur` kapanışı — hiçbir şey istemeden bitecek, yazması en zor kapanış |", "",
          "| # | Senaryo · tür · yaş | Durum → kapanış | MI | İşaret | Tohum açılışı |",
          "|---|---|---|---|---|---|"]
    for i, sp in enumerate(PLAN):
        t = atama.get(i)
        isaret = []
        if t and t["meta"].get("senaryo") not in (sp["senaryo"], "belirsiz", None):
            isaret.append("🔁")
        if t and (t["meta"].get("yas_grubu") or "yetiskin") != sp["yas"]:
            isaret.append("👤")
        if sp["turn_type"] == "multi":
            isaret.append("🧵")
        if sp["is_negative"]:
            isaret.append("⛔")
        if sp["ozerklik"]:
            isaret.append("🔓")
        if (i + 1) in PIN:
            isaret.append("📌")
        if sp["turn_ending"] == "durur":
            isaret.append("🤫")
        mesaj = (t["user_message"] if t else "—").replace("\n", " ")[:95]
        L.append(f"| {i+1} | {sp['senaryo']} · {sp['tur']} · {sp['yas']} | "
                 f"{sp['konusma_durumu']} → **{sp['turn_ending']}** | {sp['mi_process']} | "
                 f"{''.join(isaret) or '—'} | {mesaj}… |")
    # yazarken uygulanacak kurallar — gözden geçirmede bulundu
    ATIF = re.compile(r"geçen (sefer|yazdım|konuş)|dediğin gibi|söylemiştin|bahsetmiştin",
                      re.I)
    atifli = [(i + 1, PLAN[i]["turn_type"]) for i in range(len(PLAN))
              if atama.get(i) and ATIF.search(atama[i]["user_message"])]
    kendi_adi = [i + 1 for i in range(len(PLAN))
                 if atama.get(i) and "BIRAG" in atama[i]["user_message"].upper()]
    L += ["", "### Yazarken uygulanacak kurallar (gözden geçirmede bulundu)", "",
          f"1. **Önceki konuşmaya atıf düşer.** {len(atifli)} tohum *\"dediğin gibi\"*, "
          f"*\"geçen yazdım\"* diye açılıyor: "
          + " · ".join(f"#{s} ({t})" for s, t in atifli) + ". "
          "Tek turlu kayıtta böyle bir açılış tutarsızdır — kayıtta o konuşma **yok** ve "
          "model ne dediğini uyduramaz. v3 §3a zaten kullanıcı mesajının tohumdan "
          "**yeniden kurulduğunu** söylüyor; atıf cümlesi yazarken atılır. Çok turlu "
          "kayıtta ise atıf yerine gerçek bir önceki tur yazılır.",
          f"2. **Kendi adımız kullanıcı ağzına konmaz.** {len(kendi_adi)} tohum metninde "
          f"`BIRAG` geçiyor ({', '.join('#'+str(x) for x in kendi_adi) or '—'}) — kurum "
          "listesi içinde. Kullanıcıya ürün adımızı söyletmek modeli kendine atıfla "
          "eğitir; yazarken çıkarılır.",
          "3. **Yaş gevşetilen satırda içerik elle doğrulanır.** Betik artık gevşetmeyi "
          "ekrana basıyor; sessizce geçmiyor. (Gözden geçirmede bir satır bu yüzden "
          "düzeltildi: 32 yaşında evli bir adamın hikâyesi `ergen` satırına atanmıştı.)", "",
          "### Üretimde karar bekleyen yerler", "",
          "1. **🧵 çok turlu kayıtlar ({}/40).** Tohumların tamamı tek turlu açılış (K26); "
          "ara turlar üretimde kurulacak. K64'ün sınırı geçerli: kişiyi/maddeyi/durumu "
          "koruyarak an kurulur, **klinik olgu uydurulmaz**.".format(
              sum(1 for x in PLAN if x["turn_type"] == "multi")),
          "2. **🤫 `durur` kapanışı ({} kayıt).** Kullanıcı bir şey istemediğinde hiçbir şey "
          "istemeden durmak — v2'de hiç üretilmedi, yazması en zor kapanış.".format(
              sum(1 for x in PLAN if x["turn_ending"] == "durur")),
          "3. **👤 yaş gevşetmesi.** Tohum farklı yaş grubundansa dil ergen/yetişkin "
          "register'ına taşınır; içerik değişmez.",
          "4. **⛔ `is_negative` ({} kayıt).** Red **yardımsever** olur: ne yapamayacağını "
          "söyler, ne yapabileceğini önerir (v3 §8).".format(
              sum(x["is_negative"] for x in PLAN)), "",
          "⚠️ **Tohumun kendi senaryosu ile hedef senaryo farklı olabilir** (K37: "
          "senaryo ataması üretim zamanı kararıdır). İçerik gerektiren arketiplerde "
          "tohumda dayanak aranır; dayanak yoksa satır tohumsuz kalır ve elle çözülür.", ""]
    CIKTI_RAPOR.write_text("\n".join(L) + "\n")
    print(f"plan → {CIKTI_JSONL}\nrapor → {CIKTI_RAPOR}")


if __name__ == "__main__":
    main()
