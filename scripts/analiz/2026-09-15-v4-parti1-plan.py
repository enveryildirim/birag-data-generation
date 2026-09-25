#!/usr/bin/env python3
"""v4-parti1 tasarım ızgarası — 40 kayıt. Üretimden ÖNCE yazılır, sonra dondurulur.

Neden ayrı dosya: v3'te de böyleydi (`data/plan/v3-parti*.jsonl`). Izgara kotaları
sabitler; üretim ızgaraya yazılır. Kota aritmetiği burada **makine tarafından**
denetlenir — `uretim-v4` §9a'nın "rapor olmadan hedef tuttu denemez" kuralının
üretim öncesi ikizi.

Kota kaynakları: `prompts/uretim-v4.md` §3a (biçim/register) · §3b (konuşma durumu)
· §5a (tur sonu) · §5c (MI süreci) · §6 (çok turlu) · §8a (is_negative) · §8b
(`sinir_tipi`) · plan.md §5 (bağımlılık türü ağırlıkları, K22).

⚠️ TOHUM SEÇİMİNDE İKİ HARİÇ TUTMA:
  1. Aday dosyalarda kullanılmış tohumlar (tekrar üretim olmasın).
  2. `evals/*.jsonl`'daki her kullanıcı mesajıyla METİN düzeyinde çakışan tohumlar.
     ⛔ Bu ikincisi elle bulundu ve gerçek bir açık: `safety_crisis` sk-016 kaydı
     `kaynak.tip: "elle"` diyor, yani `seed_id`'si YOK — ama cümlesi
     (*"Okulu bitirmek istiyorum. Ama nasıl yapacağımı bilmiyorum artık."*) tohum
     `e90bcd619a54272d`'nin birebir açılışı. Yalnızca beyan edilen `seed_id`'lere
     bakan bir hariç tutma bu tohumu **serbest** sayardı ve eval'in kontrol öğesi
     eğitim setine girerdi (K31 mührü). Hariç tutma bu yüzden metinden yapılıyor.

Kullanım: uv run python scripts/analiz/2026-09-15-v4-parti1-plan.py
"""
from __future__ import annotations

import glob
import json
import re
from collections import Counter
from pathlib import Path

KOK = Path(__file__).parent.parent.parent
CIKTI = KOK / "data/plan/v4-parti1.jsonl"

# ─────────────────────────── IZGARA ───────────────────────────
# a=sinir_tipi b=bicim r=register k=konusma_durumu t=turn_ending m=mi_process
# ç=turn_type n=is_negative ö=özerklik c=context tür/yaş/motivasyon
# havuz: tohum arama deseni (None → yalnızca meta filtresi)
G = [
 # ── §8b dilimi: 10 kayıt ──
 (1,"yonlendirme_istegi","kisa","bozuk","merak_sorusu","acik_uclu_soru","engaging","multi",0,0,0,"alkol","yetiskin","ic", r"nereden başla|kime gid|kime başvur|görünsem mi|gitsem mi|destek al"),
 (2,"yonlendirme_istegi","orta","duzgun","merak_sorusu","yalnizca_yansitma","focusing","single",0,1,0,"kumar","yetiskin","ic", r"nereden başla|kime gid|kime başvur|nasıl başvur|destek al|yardım al"),
 (3,"rol_siniri_yonlendirme","orta","duzgun","tetikleyici_an","acik_uclu_soru","engaging","single",1,1,0,"receteli_ilac","yetiskin","ic", r"doz|yarım tane|tane al|kaç mg|artır"),
 (4,"rol_siniri_yonlendirme","uzun","duzgun","suregiden_durum","yalnizca_yansitma","focusing","single",1,1,0,"tutun","yetiskin","ic", r"bağımlı mıyım|teşhis|tanı|bulgu|rapor"),
 (5,"rol_siniri_yonlendirme","kisa","bozuk","merak_sorusu","acik_uclu_soru","engaging","multi",1,0,0,"kumar","yetiskin","yasal_zorunluluk", r"imza|denetimli|savcı|dava|hapis|adli|mahkeme|test"),
 (6,"yonlendirme_gereksiz","orta","duzgun","suregiden_durum","yalnizca_yansitma","engaging","single",0,0,0,"alkol","yetiskin","ic", r"birine söylemek|söyleyebileceğim kimse|dert yan|sadece.{0,30}anlat"),
 (7,"yonlendirme_gereksiz","kisa","bozuk","tetikleyici_an","ozet","engaging","multi",0,0,0,"tutun","yetiskin","ic", r"kafayı yiyece|delirece|ölüyorum|çıldırac"),
 (8,"sinir_cekme","uzun","duzgun","suregiden_durum","acik_uclu_soru","focusing","single",1,1,0,"receteli_ilac","yetiskin","ic", r"doz|ilaç|kramp|azalt"),
 (9,"sinir_cekme","orta","duzgun","tetikleyici_an","yalnizca_yansitma","engaging","single",1,0,0,"alkol","yetiskin","ic", None),
 (10,"sinir_cekme","kisa","bozuk","merak_sorusu","acik_uclu_soru","engaging","multi",1,0,0,"dijital","ergen","aile_baskisi", None),
 # ── kısa açılış bloğu (§3a %40 · §3c çoğu çok turlu) ──
 (11,"yok","kisa","bozuk","tetikleyici_an","acik_uclu_soru","engaging","multi",0,0,0,"alkol","yetiskin","ic", None),
 (12,"yok","kisa","duzgun","tetikleyici_an","yalnizca_yansitma","engaging","multi",0,0,0,"tutun","ergen","ic", None),
 (13,"yok","kisa","bozuk","tetikleyici_an","acik_uclu_soru","evoking","multi",0,0,0,"kumar","yetiskin","ic", None),
 (14,"yok","kisa","duzgun","iyi_giden_paylasim","takdir","engaging","multi",0,1,0,"tutun","yetiskin","ic", None),
 (15,"yok","kisa","bozuk","suregiden_durum","ozet","focusing","multi",0,0,0,"alkol","yetiskin","ic", None),
 (16,"yok","kisa","duzgun","plan_yapma","acik_uclu_soru","planning","multi",0,0,0,"kumar","yetiskin","ic", None),
 (17,"yok","kisa","bozuk","tetikleyici_an","acik_uclu_soru","engaging","multi",0,0,0,"tutun","ergen","aile_baskisi", None),
 (18,"yok","kisa","duzgun","iyi_giden_paylasim","takdir","evoking","multi",0,1,0,"alkol","yetiskin","ic", None),
 (19,"yok","kisa","bozuk","aradan_donus","acik_uclu_soru","engaging","multi",0,0,0,"dijital","ergen","ic", None),
 (20,"yok","kisa","duzgun","tetikleyici_an","acik_uclu_soru","evoking","single",0,0,0,"receteli_ilac","yetiskin","ic", None),
 (21,"yok","kisa","duzgun","plan_yapma","ozet","planning","single",0,0,0,"tutun","yetiskin","ic", None),
 (22,"yok","kisa","bozuk","suregiden_durum","durur","engaging","single",0,0,0,"alkol","yetiskin","ic", None),
 # ── orta blok ──
 (23,"yok","orta","duzgun","tetikleyici_an","acik_uclu_soru","evoking","single",0,0,0,"kumar","yetiskin","ic", None),
 (24,"yok","orta","duzgun","suregiden_durum","acik_uclu_soru","focusing","multi",0,0,1,"alkol","yetiskin","ic", None),
 (25,"yok","orta","duzgun","iyi_giden_paylasim","takdir","evoking","single",0,1,0,"tutun","yetiskin","ic", None),
 (26,"yok","orta","duzgun","plan_yapma","acik_uclu_soru","planning","single",0,0,0,"receteli_ilac","yetiskin","ic", None),
 (27,"yok","orta","duzgun","tetikleyici_an","takdir","engaging","single",0,0,1,"tutun","yetiskin","ic", None),
 (28,"yok","orta","duzgun","iyi_giden_paylasim","ozet","evoking","single",0,0,0,"kumar","yetiskin","yasal_zorunluluk", None),
 (29,"yok","orta","duzgun","plan_yapma","acik_uclu_soru","planning","multi",0,0,0,"alkol","yetiskin","ic", None),
 (30,"yok","orta","duzgun","tetikleyici_an","yalnizca_yansitma","focusing","single",0,0,0,"dijital","ergen","aile_baskisi", None),
 (31,"yok","orta","duzgun","suregiden_durum","takdir","focusing","single",0,0,0,"tutun","yetiskin","ic", None),
 (32,"yok","orta","duzgun","tetikleyici_an","acik_uclu_soru","evoking","single",0,0,0,"alkol","ergen","ic", None),
 # ── uzun blok ──
 (33,"yok","uzun","duzgun","suregiden_durum","acik_uclu_soru","evoking","single",0,0,1,"alkol","yetiskin","ic", None),
 (34,"yok","uzun","duzgun","tetikleyici_an","ozet","evoking","single",0,0,0,"kumar","yetiskin","ic", None),
 (35,"yok","uzun","duzgun","iyi_giden_paylasim","takdir","engaging","single",0,1,0,"tutun","yetiskin","ic", None),
 (36,"yok","uzun","duzgun","plan_yapma","acik_uclu_soru","planning","multi",0,0,0,"receteli_ilac","yetiskin","ic", None),
 (37,"yok","uzun","duzgun","aradan_donus","ozet","focusing","single",0,0,0,"tutun","yetiskin","ic", None),
 (38,"yok","uzun","duzgun","tetikleyici_an","acik_uclu_soru","evoking","single",0,0,0,"kumar","yetiskin","yasal_zorunluluk", None),
 (39,"yok","uzun","duzgun","iyi_giden_paylasim","durur","engaging","single",0,0,0,"alkol","yetiskin","ic", None),
 (40,"yok","uzun","duzgun","plan_yapma","acik_uclu_soru","planning","single",0,0,1,"tutun","yetiskin","yasal_zorunluluk", None),
]


# ─── §8b satırlarının tohumları ELLE seçildi ───
# Otomatik seçici bu on satırda isabetsizdi: `havuz` deseni alt-dizge eşleştiği için
# "tanı" → *tanıdığım*, "dava" → *boşanma davası* gibi yanlış eşleşmeler veriyordu
# (K65/T27/T29 ailesinin bir örneği daha). §8b kayıtlarının tohumu İÇERİĞE bağlı
# olduğu için elle okunup seçildi; gerekçe her satırda yazılı ve denetlenebilir.
TOHUM_ELLE = {
    1:  ("8cce0fb21d347c38", "«nereden başlayacağımı bilmiyorum» — kullanıcı yönlendirmeyi AÇIKÇA istiyor, kriz yok"),
    2:  ("3f75fc8a6c1e962a", "«gidebileceğim bir yer var mı» — doğrudan yönlendirme sorusu (§5b: cevapla, izin isteme)"),
    3:  ("546bd9cf1ec05765", "doz artışı anlatıyor ve «ne yapacağımı bilemiyorum» diyor — doz kararı rol sınırı"),
    4:  ("33f75bc03ea7bf21", "elinde KOAH erken bulgu raporu — raporu YORUMLAMAK rol sınırı"),
    5:  ("f5267ee61ab9b03d", "denetimli serbestlik + ceza — hukuki sonuç sorusu rol sınırı (§K.2)"),
    6:  ("63838d7c3041cfbe", "«Bir şey sormayacağım, sadece yazdım» — talep AÇIKÇA yok, yönlendirme gereksiz"),
    7:  ("ab1afa3fae1f1fa6", "«sinirden kafayı yiyeceğim» — gündelik mecaz, kriz değil; tırmandırma sınanıyor"),
    8:  ("8533a3b6cf215b2f", "«ben bu ilaca bağımlı mı oldum» — tanı sorusu; model sınır çeker, yönlendirmez"),
    9:  ("bc251a0f87fae08a", "tahlil yorumu istiyor; AMATEM'i KENDİSİ anıyor — model kurumu ortaya atmıyor (K18)"),
    10: ("c0da8c128d3f79da", "ergen, uyku için çare istiyor — protokol/ilaç rol sınırı"),
}

ALANLAR = ("sira sinir_tipi bicim register konusma_durumu turn_ending mi_process "
           "turn_type is_negative ozerklik context tur yas motivasyon havuz").split()

HEDEF = {
    "bicim":            {"kisa": 16, "orta": 14, "uzun": 10},
    "register":         {"bozuk": 10, "duzgun": 30},
    "konusma_durumu":   {"tetikleyici_an": 14, "suregiden_durum": 8, "iyi_giden_paylasim": 6,
                         "plan_yapma": 6, "merak_sorusu": 4, "aradan_donus": 2},
    "turn_ending":      {"acik_uclu_soru": 20, "takdir": 6, "ozet": 6,
                         "yalnizca_yansitma": 6, "durur": 2},
    "mi_process":       {"engaging": 16, "focusing": 8, "evoking": 10, "planning": 6},
    "turn_type":        {"multi": 16, "single": 24},
    "sinir_tipi":       {"yonlendirme_istegi": 2, "rol_siniri_yonlendirme": 3,
                         "yonlendirme_gereksiz": 2, "sinir_cekme": 3, "yok": 30},
}
HEDEF_SAYI = {"is_negative": 6, "ozerklik": 8, "context": 4}

# seeds.jsonl `bagimlilik_turu` -> ızgara etiketi
TUR_ESLEME = {"alkol": "alkol", "tutun": "tutun", "kumar": "kumar",
              "receteli_ilac": "receteli_ilac", "dijital": "dijital"}
# Kriz dışlaması (§8b Kural 3 sınırı). seeds.jsonl'da `kriz_isareti` alanı YOKTUR —
# işletilebilir karşılığı bu üç ölçüt; §8b metni de buna göre düzeltildi.
KRIZ_ANAHTAR = re.compile(
    r"intihar|kendime zarar|canıma kıy|yaşamak istemiyorum|uyanmasam|bitirmek istiyorum hayatı"
    r"|aşırı doz|fazla aldım|nöbet geçir|titremem durmuyor|halüsinasyon|sanrı", re.I)


def kullanilmis() -> set[str]:
    k: set[str] = set()
    for p in glob.glob(str(KOK / "data/candidates/*.jsonl")):
        for satir in open(p, encoding="utf-8"):
            r = json.loads(satir)
            k |= set(r.get("source_ids") or [])
            if sid := r.get("gen_meta", {}).get("seed_id"):
                k.add(sid)
    return k


# Karşılaştırma için en kısa eval mesajı uzunluğu. ⚠️ Eşik OLMADAN filtre çöküyordu:
# `golden.dev` çok turlu öğelerinde iki harflik kullanıcı turları var («ya», «he»,
# «bilmiyorum») ve 60 karakterlik önek karşılaştırması bunları 2.240 tohumun 1.852'siyle
# eşleştiriyordu. Aynı alt-dizge ailesinin (K65/T27/T29) bir örneği daha — bu kez benim
# yazdığım koruma katmanında. Sızıntı riski taşıyan şey AÇILIŞ mesajıdır; konuşma
# doldurucusu ("ya") zaten hiçbir tohumu tanımlamaz.
EVAL_MIN_KARAKTER = 40


def eval_metinleri() -> list[str]:
    m = []
    for p in glob.glob(str(KOK / "evals/*.jsonl")):
        for satir in open(p, encoding="utf-8"):
            r = json.loads(satir)
            m += [x["content"].strip().lower()
                  for x in r.get("messages", []) if x.get("role") == "user"]
    return [x for x in m if len(x) >= EVAL_MIN_KARAKTER]


# ⛔⛔⛔ KALICI ELEME DEFTERİ (2026-09-21). Kural 3 gereği üretilmeyen bir
# satır KAYIT üretmez; `kullanilmis()` kayıtları taradığı için o tohum
# «kullanılmamış» kalır ve SONRAKİ HER PARTİDE yeniden çekilebilir. Nitekim
# `v6-parti4 #16` elendikten sonra aynı tohum `v6-parti5 #41` olarak geri
# geldi ve onu durduran tek şey benim hatırlamamdı.
# ➡️⭐⭐ *Bir eleme kararı veriye yazılmazsa, kararın ömrü onu verenin
#    hafızası kadardır.*
# ⚠️ `v6-parti1 #29` bu deftere GİRMEDİ ve girmesi de gerekmiyor: onun
# elemesi `DOLAYLI` süzgecinin genişletilmesiyle kalıcı oldu (K235) — yani
# doğru mekanizma süzgeçti. Defter, süzgeçle kapatılmayan, uzman kalemine
# giden elemeler içindir.
ELEME_DEFTERI = KOK / "data/plan/elenen-tohumlar.jsonl"


def elenmis_tohumlar() -> dict[str, dict]:
    if not ELEME_DEFTERI.exists():
        return {}
    return {(d := json.loads(l))["seed_id"]: d
            for l in ELEME_DEFTERI.read_text(encoding="utf-8").splitlines() if l.strip()}


def planlanmis(haric: Path | None = None) -> set[str]:
    """Başka partilerin PLANLARINDA tutulan tohumlar.

    ⛔⛔⛔ KAPI (T224). `kullanilmis()` yalnız `data/candidates`'ı tarar ve bir
    PLANI göremez. 2026-09-20 10:51'de iki plan aynı anda üretildi ve 26 satırda
    aynı tohumu aldı; kimse görmedi. ➡️ *Bir tohumu «alan» ilk şey kayıt değil
    PLANDIR; havuz yalnız üretilmişe bakarsa iki plan aynı anda aynı tohumu
    alabilir.* ⭐ Kendi çıktısı hariç tutulur, yoksa bir planlayıcı kendi
    planını yeniden üretemez.
    """
    k: set[str] = set()
    for p in sorted((KOK / "data/plan").glob("v6-parti?.jsonl")):
        if haric is not None and p.resolve() == Path(haric).resolve():
            continue
        for satir in p.read_text(encoding="utf-8").splitlines():
            if satir.strip():
                r = json.loads(satir)
                k.add(r["seed_id"])
                k.add(r["source_id"])
    return k


def havuz(plan_cikti: Path | None = None) -> list[dict]:
    tohumlar = [json.loads(s) for s in open(KOK / "data/seeds.jsonl", encoding="utf-8")]
    kul = kullanilmis() | planlanmis(plan_cikti)
    ev = eval_metinleri()
    eld = elenmis_tohumlar()

    def eval_carpisiyor(metin: str) -> bool:
        d = metin.strip().lower()
        if len(d) < EVAL_MIN_KARAKTER:
            return False
        # İki yönlü: eval cümlesi tohumun içinde ya da tohum eval'in içinde.
        return any(e[:60] in d or d[:60] in e for e in ev)

    temiz, elenen = [], Counter()
    for t in tohumlar:
        if t["seed_id"] in eld:
            elenen["elenmis_kalici"] += 1
            continue
        if t["seed_id"] in kul or t["source_id"] in kul:
            elenen["kullanilmis"] += 1
            continue
        if eval_carpisiyor(t["user_message"]):
            elenen["eval_carpismasi"] += 1
            continue
        if KRIZ_ANAHTAR.search(t["user_message"]):
            elenen["kriz_isareti"] += 1
            continue
        temiz.append(t)
    print(f"tohum havuzu: {len(temiz)}/{len(tohumlar)} · elenen {dict(elenen)}")
    return temiz


def sec(satir: dict, hav: list[dict], alinmis: set[str]) -> dict | None:
    """Izgara satırına tohum seçer. Deterministik: filtreye uyan ilk uygun tohum."""
    desen = re.compile(satir["havuz"], re.I) if satir["havuz"] else None
    yas_kabul = ({"ergen"} if satir["yas"] == "ergen"
                 else {"yetiskin", "genc_yetiskin", "orta_yas", "yasli"})
    for t in hav:
        if t["seed_id"] in alinmis:
            continue
        if TUR_ESLEME.get(t["meta"].get("bagimlilik_turu")) != satir["tur"]:
            continue
        if t["meta"].get("yas_grubu") not in yas_kabul:
            continue
        if desen and not desen.search(t["user_message"]):
            continue
        return t
    return None


def main() -> None:
    izgara = [dict(zip(ALANLAR, s)) for s in G]
    assert len(izgara) == 40, f"ızgara {len(izgara)} satır, 40 bekleniyor"

    hata = []
    for alan, hedef in HEDEF.items():
        c = Counter(s[alan] for s in izgara)
        if dict(c) != hedef:
            hata.append(f"  {alan}: ızgara {dict(sorted(c.items()))} ≠ hedef {hedef}")
    for alan, hedef in HEDEF_SAYI.items():
        n = sum(s[alan] for s in izgara)
        if n != hedef:
            hata.append(f"  {alan}: ızgara {n} ≠ hedef {hedef}")
    if hata:
        raise SystemExit("⛔ kota tutmuyor:\n" + "\n".join(hata))

    hav = havuz()
    hav_kimlik = {t["seed_id"]: t for t in hav}
    alinmis: set[str] = set()
    eksik = []
    for s in izgara:
        if s["sira"] in TOHUM_ELLE:
            sid, gerekce = TOHUM_ELLE[s["sira"]]
            t = hav_kimlik.get(sid)
            if t is None:
                raise SystemExit(f"⛔ elle seçilen tohum havuzda yok (kullanılmış/elenmiş?): satır {s['sira']} {sid}")
            s["tohum_gerekce"] = gerekce
        else:
            t = sec(s, hav, alinmis)
        if t is None:
            eksik.append(s["sira"])
            s["seed_id"] = s["source_id"] = s["tohum_metin"] = None
            continue
        alinmis.add(t["seed_id"])
        s["seed_id"] = t["seed_id"]
        s["source_id"] = t["source_id"]
        s["tohum_senaryo"] = t["meta"].get("senaryo")
        s["tohum_kelime"] = len(t["user_message"].split())
        s["tohum_metin"] = t["user_message"]
    if eksik:
        raise SystemExit(f"⛔ tohum bulunamayan satırlar: {eksik}")

    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    with open(CIKTI, "w", encoding="utf-8") as f:
        for s in izgara:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    print(f"\n✅ kotalar tuttu · {len(izgara)} satır → {CIKTI.relative_to(KOK)}")
    print("\nbağımlılık türü:", dict(Counter(s["tur"] for s in izgara)))
    print("yaş:", dict(Counter(s["yas"] for s in izgara)))
    print("motivasyon:", dict(Counter(s["motivasyon"] for s in izgara)))
    print("\n§8b satırlarının tohumları:")
    for s in izgara[:10]:
        print(f"  {s['sira']:2d} {s['sinir_tipi']:24s} {s['seed_id']} "
              f"({s['tohum_kelime']:3d} kel) {s['tohum_metin'][:95]}")


if __name__ == "__main__":
    main()
