#!/usr/bin/env python3
"""v3 parti 3 — 24 satır, odağı DERİN ÇOK TURLU. ⚠️ ÇIKTI DONDURULUR.

Neden bu parti farklı: `reports/analiz/2026-09-14-dilim-kapsama.md` §2 ölçtü —
80 kaydın çok turlu sayılan 18'inin TAMAMI iki kullanıcı turlu. `plan.md` §6
*"3-5 turluk alışveriş"* istiyor ve `uretim-v3.md` §5c çok turlu kayıtların
**MI süreci geçişini** öğretmesini istiyor. İkisi de iki turda olmuyor.
3+ turlu kayıt sayımız: **0/80**.

Bu yüzden 24 satırın **14'ü** 3-5 kullanıcı turlu ve her biri bir MI geçişi
taşıyor. Geçiş geriye de olabilir (§C.2: süreçler döngüseldir, doğrusal değil).

⚠️ Hedefler artık KÜMÜLATİF ölçülüyor (80 + 24 = 104). §5a/§3b/§5c korpus düzeyi
hedefleri; parti başına ölçmek, odaklı bir partiyi haksız yere düşürürdü.

Girdi : data/seeds.jsonl
Çıktı : data/plan/v3-parti3.jsonl + reports/analiz/2026-09-14-v3-parti3-plani.md
"""
from __future__ import annotations

import collections, difflib, hashlib, json, random, re, sys, unicodedata
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
SEEDS = KOK / "data/seeds.jsonl"
CIKTI_JSONL = KOK / "data/plan/v3-parti3.jsonl"
CIKTI_RAPOR = KOK / "reports/analiz/2026-09-14-v3-parti3-plani.md"
MEVCUT = ["data/candidates/v3-parti1.jsonl", "data/candidates/v3-parti2-tam.jsonl"]
RASTGELE = random.Random(311)

HEDEF24 = {
    "turn_ending": {"acik_uclu_soru": 13, "takdir": 4, "ozet": 3, "yalnizca_yansitma": 3, "durur": 1},
    "konusma_durumu": {"tetikleyici_an": 9, "suregiden_durum": 3, "iyi_giden_paylasim": 4,
                       "plan_yapma": 5, "merak_sorusu": 2, "aradan_donus": 1},
    "mi_process": {"engaging": 8, "focusing": 4, "evoking": 8, "planning": 4},
    "sysvar": {"canon": 18, "paraphrase": 6},
}
HEDEF_NEG, HEDEF_CTX, HEDEF_ERGEN, HEDEF_DERIN, HEDEF_OZERK = 4, 2, 3, 14, 2

A = ("tur", "yas", "derinlik", "mi_gecis", "mi_process", "konusma_durumu",
     "turn_ending", "sysvar", "is_negative", "ozerklik", "context")
# derinlik: tek turlu için 1, çok turlu için kullanıcı turu sayısı (3-5)
P = [
    # ── DERİN ÇOK TURLU (14) ─────────────────────────────────────────────────
    ("alkol",        "yetiskin", 4, "engaging→focusing", "focusing", "tetikleyici_an",    "acik_uclu_soru",    "canon",      0, 0, 0),
    ("kumar",        "yetiskin", 3, "engaging→evoking",  "evoking",  "tetikleyici_an",    "ozet",              "canon",      0, 0, 0),
    ("tutun",        "yetiskin", 3, "focusing→evoking",  "evoking",  "suregiden_durum",   "acik_uclu_soru",    "paraphrase", 0, 0, 0),
    ("receteli_ilac","yetiskin", 4, "engaging→focusing", "focusing", "tetikleyici_an",    "acik_uclu_soru",    "canon",      1, 0, 0),
    ("alkol",        "yetiskin", 3, "evoking→planning",  "planning", "plan_yapma",        "ozet",              "canon",      0, 0, 0),
    # ⚠️ tür dijital → tutun: `dijital` tohumlarının TAMAMI kısa. İlerleme taşıyan
    # ve 30+ kelime olan tek bir dijital tohum yok (ergen de yetişkin de); üç turluk
    # alışveriş çıkarmak §3a'nın uydurma uyarısına girerdi. `tur` v3'te hedefi olan
    # bir alan değil, `tutun/ergen`de beş uygun tohum var.
    ("tutun",        "ergen",    3, "engaging→evoking",  "evoking",  "iyi_giden_paylasim","takdir",            "canon",      0, 0, 0),
    ("kumar",        "yetiskin", 4, "focusing→planning", "planning", "plan_yapma",        "acik_uclu_soru",    "canon",      0, 0, 0),
    ("alkol",        "yetiskin", 3, "focusing→engaging", "engaging", "tetikleyici_an",    "yalnizca_yansitma", "canon",      0, 0, 0),
    ("tutun",        "yetiskin", 3, "evoking→planning",  "planning", "plan_yapma",        "acik_uclu_soru",    "paraphrase", 0, 0, 0),
    ("receteli_ilac","yetiskin", 3, "engaging→evoking",  "evoking",  "suregiden_durum",   "acik_uclu_soru",    "canon",      0, 0, 0),
    ("kumar",        "yetiskin", 4, "focusing→evoking",  "evoking",  "tetikleyici_an",    "acik_uclu_soru",    "canon",      0, 0, 0),
    ("alkol",        "yetiskin", 3, "engaging→planning", "planning", "plan_yapma",        "ozet",              "canon",      0, 0, 0),
    ("tutun",        "ergen",    3, "evoking→engaging",  "engaging", "iyi_giden_paylasim","takdir",            "paraphrase", 0, 0, 0),   # aynı gerekçe
    ("alkol",        "yetiskin", 3, "engaging→focusing", "focusing", "merak_sorusu",      "acik_uclu_soru",    "canon",      0, 0, 1),
    # ── TEK TURLU (10) ───────────────────────────────────────────────────────
    ("alkol",        "yetiskin", 1, "", "engaging", "tetikleyici_an",    "acik_uclu_soru",    "canon",      0, 0, 0),
    ("kumar",        "yetiskin", 1, "", "engaging", "tetikleyici_an",    "yalnizca_yansitma", "canon",      0, 0, 0),
    ("tutun",        "ergen",    1, "", "engaging", "tetikleyici_an",    "acik_uclu_soru",    "paraphrase", 0, 0, 0),
    ("dijital",      "yetiskin", 1, "", "engaging", "tetikleyici_an",    "durur",             "canon",      0, 0, 0),
    ("receteli_ilac","yetiskin", 1, "", "focusing", "suregiden_durum",   "acik_uclu_soru",    "canon",      1, 1, 0),
    ("alkol",        "yetiskin", 1, "", "evoking",  "plan_yapma",        "yalnizca_yansitma", "canon",      0, 0, 0),
    ("tutun",        "yetiskin", 1, "", "evoking",  "iyi_giden_paylasim","takdir",            "canon",      0, 0, 0),
    ("alkol",        "yetiskin", 1, "", "evoking",  "iyi_giden_paylasim","takdir",            "paraphrase", 0, 0, 0),
    ("alkol",        "yetiskin", 1, "", "engaging", "merak_sorusu",      "acik_uclu_soru",    "canon",      1, 1, 1),
    ("kumar",        "yetiskin", 1, "", "engaging", "aradan_donus",      "acik_uclu_soru",    "paraphrase", 1, 0, 0),
]
PLAN = [dict(zip(A, s)) for s in P]

KRIZ_ANAHTAR = [
    "yaşamak istemiyorum", "ölmek istiyorum", "intihar", "canıma kıy", "kendimi asa",
    "kendime zarar", "bitirmek istiyorum", "son vermek istiyorum", "uyanmasam",
    "uyanmak istemiyorum", "yaşamaya değmez", "hayatıma son", "bileğimi", "hapları içt",
    "yok olmak istiyorum", "ölsem", "yük oluyorum", "bensiz daha iyi",
    "kurtulmak istiyorum bu hayattan", "acil servis", "acilde", "ambulans",
    "mide yıkan", "yoğun bakım", "doz aşımı", "aşırı doz", "taburcu", "entübe", "komaya",
    "direksiyonda", "gözüm kapandı", "araba kullan",
]
RISKLI_ESDURUM = ("intihar", "kendine zarar", "öz kıyım", "özkıyım", "psikoz", "sanrı",
                  "yoksunluk vakası", "deliryum", "nöbet", "overdoz", "aşırı doz")
YOKSUNLUK_BELIRTI = re.compile(
    r"\bel(im|lerim|i)?\b[^.!?]{0,25}\btitri|\btitreme\b|\bter(liyorum| içinde)\b"
    r"|terleyerek uyan|\bnöbet geçir|\bhavale\b|sanrı gör|\bkusuyorum\b|sayıklıyor"
    r"|\bçarpıntı\b|kalbim (hızlı|küt küt)", re.IGNORECASE)


# Elle okunup sabitlenen satır. Kapı altı yinelemede de `iyi_giden_paylasim` için
# yanlış pozitif vermeye devam etti (tırmanma anlatan mesajlar "fark ettim" ya da
# süre+olumsuzlama desenine takılıyor). Kapı havuzu daraltıyor; son yuva okunarak
# dolduruldu — K78'in vardığı yerin aynısı, bugünün altıncı aynı dersi.
PIN = {22: "042886cc5b76ba6d"}

# Yazılmış satırların tohumları — yeniden atanmasınlar.
SABIT = {1: "6a3ec4ac74169348", 2: "3efa6ae79dec5559", 3: "ccd179f55993b6a9", }


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def yazilmis_mesajlar() -> list[str]:
    """Daha önce YAZILMIŞ kayıtların ilk kullanıcı mesajları.

    ⚠️ Tekilleştirme `seed_id`'ye bakıyordu ve yetmedi: havuzda metni birbirinin
    AYNISI olan ama seed_id'si farklı tohumlar var. Parti 3 planı ilk koşuda
    parti 2 #18 ile birebir aynı mesajı taşıyan bir tohum atadı. Artık aday tohum
    metni, yazılmış bütün mesajlara karşı benzerlik eşiğiyle sınanıyor."""
    out = []
    for f in ["data/candidates/expert-70.jsonl"] + MEVCUT:
        for l in open(KOK / f):
            r = json.loads(l)
            u = [m["content"] for m in r["messages"] if m["role"] == "user"][0]
            if "BAĞLAM" in u or "KAYNAK" in u or "<context" in u:
                u = u.split("\n\n")[-1]
            out.append(norm(u))
    return out


BENZERLIK_ESIGI = 0.80

# K78'in kapısı — parti 2'de yazılmıştı ama bu betiğe TAŞINMAMIŞTI ve aynı hata
# tekrarladı: `iyi_giden_paylasim` satırına paylaşılacak iyi şeyi olmayan tohum
# atandı. K64: kullanıcının KENDİ ifade ettiği, sayılabilir bir ilerleme aranır.
# ⚠️ ANAHTAR KELİME DEĞİL, DESEN. K78'de bu liste sabit ifadelerdi ve "içmiyorum",
# "bıraktım" gibi kelimeler VARSAYIM ve PAZARLIK içinde eşleşiyordu ("diyelim ki ben
# bıraktım", "sigarayı zevk için içmiyorum"). O gün PIN'le geçilmişti; burada kökten
# düzeltiliyor. Gerçek ilerleme iki biçimden birini alır:
#   (a) SÜRE + olumsuzlama  — "üç haftadır içmedim", "on altı ay oldu almayalı"
#   (b) açık FARK EDİŞ      — §3b `iyi_giden_paylasim` kutlamayı da fark edişi de sayar
ILERLEME = re.compile(
    r"\b(bir|iki|üç|dört|beş|altı|yedi|sekiz|dokuz|on|yirmi|otuz|kırk|elli|\d+)\s*"
    r"(gün|hafta|ay|yıl)\w*\s*(oldu|olmuş|dur|dır|dir|d[ıi]r)?\b[^.!?]{0,45}"
    r"\b(içmedim|içmiyorum|oynamadım|oynamıyorum|kullanmadım|kullanmıyorum|almadım|"
    r"almıyorum|gitmedim|sürmedim|dokunmadım|almayalı|içmeyeli)\b"
    r"|\bfark ett(im|iğim)|\bfark edince\b", re.IGNORECASE)
# Dışlama: kayma anlatan ya da KÜÇÜMSEYEN mesaj "iyi giden paylaşımı" değildir.
# Küçümseme maddeleri sonradan eklendi — `fark ettim` dalı "sadece fark ettim,
# sıkıntı yok" gibi tırmanma mesajlarında da ateşliyordu.
KAYMA = ("yine", "tekrar başladım", "bozdum", "kupon yaptım", "dayanamadım",
         "sıfırladım", "diyelim ki",
         "sıkıntı yok", "önemli değil", "sorun değil", "abartı", "o kadar da",
         "büyütülecek", "ne olacak yani")
# Derin satır (3-5 tur) için tohum en az bu kadar kelime taşımalı. Yumuşak geri
# çekilme YOK: sekiz kelimelik tohumdan üç tur çıkarmak §3a'nın uydurma uyarısıdır.
DERIN_MIN_KELIME = 30


def tr_kucult(s: str) -> str:
    s = s.replace("İ", "i").replace("I", "ı").lower()
    return unicodedata.normalize("NFKD", s).replace("̇", "")


def kriz_icerigi(t):
    metin = tr_kucult(t["user_message"] + " " + t.get("scenario_context", ""))
    vurus = [a for a in KRIZ_ANAHTAR if tr_kucult(a) in metin]
    for e in t["meta"].get("notlar", {}).get("esdurumlar", []):
        vurus += [f"eşdurum:{e}" for k in RISKLI_ESDURUM if k in tr_kucult(e)]
    return vurus


def dogrula() -> list[str]:
    s = []
    if len(PLAN) != 24:
        s.append(f"plan {len(PLAN)} satır, 24 bekleniyordu")
    for alan, hedef in HEDEF24.items():
        var = collections.Counter(r[alan] for r in PLAN)
        for k, h in hedef.items():
            if var.get(k, 0) != h:
                s.append(f"{alan} `{k}`: {var.get(k,0)} satır, {h} bekleniyordu")
        for k in var:
            if k not in hedef:
                s.append(f"{alan} `{k}`: planda var, hedefte yok")
    for ad, sayi, hedef in [
            ("is_negative", sum(r["is_negative"] for r in PLAN), HEDEF_NEG),
            ("context", sum(r["context"] for r in PLAN), HEDEF_CTX),
            ("ergen", sum(r["yas"] == "ergen" for r in PLAN), HEDEF_ERGEN),
            ("derin çok turlu", sum(r["derinlik"] >= 3 for r in PLAN), HEDEF_DERIN),
            ("ozerklik", sum(r["ozerklik"] for r in PLAN), HEDEF_OZERK)]:
        if sayi != hedef:
            s.append(f"{ad}: {sayi} satır, {hedef} bekleniyordu")
    for i, r in enumerate(PLAN, 1):
        derin = r["derinlik"] >= 3
        if derin and not r["mi_gecis"]:
            s.append(f"#{i}: derin çok turlu ama `mi_gecis` boş (§5c)")
        if not derin and r["mi_gecis"]:
            s.append(f"#{i}: tek turlu ama `mi_gecis` dolu")
        if r["derinlik"] == 2:
            s.append(f"#{i}: derinlik 2 — bu parti 3+ tur istiyor (§6)")
        if derin and r["mi_gecis"].split("→")[-1] != r["mi_process"]:
            s.append(f"#{i}: `mi_gecis` son süreci `{r['mi_gecis'].split('→')[-1]}`, "
                     f"`mi_process` `{r['mi_process']}` — uyuşmuyor")
    return s


def kullanilmis(tohumlar) -> set[str]:
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
    for f in ["data/candidates/expert-70.jsonl"] + MEVCUT:
        for satir in open(KOK / f):
            kul.add(json.loads(satir)["gen_meta"]["seed_id"])
    return kul


def ata(tohumlar):
    kul = kullanilmis(tohumlar)
    havuz = [t for t in tohumlar
             if t["seed_id"] not in kul
             and t["meta"].get("senaryo") != "kriz"
             and t["meta"].get("risk_seviyesi") != "cok_yuksek"
             and not kriz_icerigi(t)
             and not YOKSUNLUK_BELIRTI.search(t["user_message"])]
    RASTGELE.shuffle(havuz)
    onceki = yazilmis_mesajlar()
    havuz = [t for t in havuz
             if max((difflib.SequenceMatcher(None, norm(t["user_message"]), y).ratio()
                     for y in onceki), default=0.0) < BENZERLIK_ESIGI]
    # Derin çok turlu satırlar ZENGİN tohum ister: üç-beş turluk alışverişi
    # taşıyacak malzeme lazım. Vekil ölçüt kelime sayısı — mükemmel değil ama
    # iki cümlelik tohumdan dört tur çıkarmak §3a'nın uyardığı uydurma olur.
    def zengin(t):
        return len(t["user_message"].split()) >= DERIN_MIN_KELIME

    def iyi_giden_uygun(t):
        u = t["user_message"]
        return bool(ILERLEME.search(u)) and not any(tr_kucult(k) in tr_kucult(u) for k in KAYMA)
    alinan, atama, eksik, gevsetilen = set(), {}, [], []
    for sira, sid in list(PIN.items()) + list(SABIT.items()):
        t = next((x for x in tohumlar if x["seed_id"] == sid), None)
        if t is None:
            raise SystemExit(f"SABİT #{sira}: tohum bulunamadı")
        atama[sira - 1] = t
        alinan.add(sid)
    for i in sorted(range(len(PLAN)), key=lambda i: (PLAN[i]["yas"] != "ergen",
                                                     PLAN[i]["derinlik"] < 3)):
        if i in atama:
            continue
        s, aday = PLAN[i], None
        derin = s["derinlik"] >= 3
        for yas_zorunlu in (True, False):
            for t in havuz:
                if t["seed_id"] in alinan:
                    continue
                m = t["meta"]
                if m.get("bagimlilik_turu") != s["tur"]:
                    continue
                if yas_zorunlu and (m.get("yas_grubu") or "yetiskin") != s["yas"]:
                    continue
                if derin and not zengin(t):          # geri çekilme YOK
                    continue
                if s["konusma_durumu"] == "iyi_giden_paylasim" and not iyi_giden_uygun(t):
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


def main() -> None:
    tohumlar = [json.loads(s) for s in open(SEEDS)]
    sorun = dogrula()
    if sorun:
        print("DOĞRULAMA DÜŞTÜ — plan yazılmadı:")
        for x in sorun:
            print("  ·", x)
        sys.exit(1)
    atama, eksik, havuz_n, gevsetilen = ata(tohumlar)
    if eksik:
        print(f"DOĞRULAMA DÜŞTÜ — tohum bulunamadı: {[i+1 for i in eksik]}")
        sys.exit(1)

    CIKTI_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with open(CIKTI_JSONL, "w") as f:
        for i, r in enumerate(PLAN):
            t = atama[i]
            f.write(json.dumps({"sira": i + 1, **r, "seed_id": t["seed_id"],
                                "source_id": t["source_id"],
                                "tohum_senaryo": t["meta"].get("senaryo"),
                                "tohum_yas": t["meta"].get("yas_grubu"),
                                "kelime": len(t["user_message"].split()),
                                "user_message": t["user_message"]}, ensure_ascii=False) + "\n")

    derin = [r for r in PLAN if r["derinlik"] >= 3]
    L = ["# v3 parti 3 — plan (24 satır, odağı derin çok turlu)", "",
         f"**Çıktı:** `data/plan/v3-parti3.jsonl` · SHA256 "
         f"`{hashlib.sha256(CIKTI_JSONL.read_bytes()).hexdigest()}`  ",
         f"**Betik:** `scripts/analiz/2026-09-14-v3-parti3-plani.py` · "
         f"**Tarih:** {TARIH} · **Havuz:** {havuz_n}", "", "---", "",
         "## Neden bu parti farklı", "",
         "`reports/analiz/2026-09-14-dilim-kapsama.md` §2 ölçtü: 80 kaydın çok turlu "
         "sayılan 18'inin **tamamı iki kullanıcı turlu**. `plan.md` §6 *\"3-5 turluk "
         "alışveriş\"*, `uretim-v3.md` §5c de **MI süreci geçişi** istiyor; ikisi de iki "
         f"turda olmuyor. 3+ turlu kayıt sayımız **0/80**. Bu partinin **{len(derin)}/24** "
         "satırı 3-5 turlu ve her biri bir geçiş taşıyor.", "",
         "> Geçiş **geriye** de olabilir — §C.2: MI süreçleri döngüseldir, doğrusal değil. "
         "Kullanıcı savunmaya geçtiğinde focusing'den engaging'e dönmek doğru hamledir.", "",
         "## ⚠️ Hedefler kümülatif ölçülüyor", "",
         "§5a/§3b/§5c **korpus düzeyi** hedefleri. Odaklı bir partiyi kendi içinde ölçmek "
         "onu haksız yere düşürürdü; bu partinin sayıları 80 mevcut kayda **eklenerek** "
         "104 üzerinden hedefe oturacak biçimde seçildi.", "",
         "## Satırlar", "",
         "| # | tür | yaş | tur | MI geçişi | MI | durum | kapanış | sysvar | neg | özerk | ctx | tohum kelime |",
         "|---:|---|---|---:|---|---|---|---|---|:--:|:--:|:--:|---:|"]
    for i, r in enumerate(PLAN, 1):
        t = atama[i - 1]
        L.append(f"| {i} | {r['tur']} | {r['yas']} | {r['derinlik']} | "
                 f"{r['mi_gecis'] or '—'} | {r['mi_process']} | {r['konusma_durumu']} | "
                 f"{r['turn_ending']} | {r['sysvar']} | {'✔' if r['is_negative'] else '—'} | "
                 f"{'✔' if r['ozerklik'] else '—'} | {'✔' if r['context'] else '—'} | "
                 f"{len(t['user_message'].split())} |")
    L += ["", "## Kümülatif hedefe katkı", "",
          "| Alan | Bu partide |", "|---|---|"]
    for alan, hedef in HEDEF24.items():
        var = collections.Counter(r[alan] for r in PLAN)
        L.append(f"| {alan} | " + " · ".join(f"`{k}` {var.get(k,0)}" for k in hedef) + " |")
    L += [f"| is_negative | {sum(r['is_negative'] for r in PLAN)} |",
          f"| context (RAG) | {sum(r['context'] for r in PLAN)} |",
          f"| ergen | {sum(r['yas']=='ergen' for r in PLAN)} |",
          f"| özerklik görünür | {sum(r['ozerklik'] for r in PLAN)} |", "",
          "> ⚠️ **Özerklik yalnızca 2.** Kümülatif oran şu an %25, hedef %20 — yani "
          "**hedefin üstündeyiz**. Hedefin kendisi K63'te *\"bu benim önerim\"* diye "
          "işaretlenmişti; %25'in fazla olup olmadığı klinik bir soru ve uzmana gider. "
          "Bu partide yalnızca klinik olarak gerekli olan iki satıra kondu.", ""]
    if gevsetilen:
        L += ["## ⚠️ Yaş gevşetmesi", ""] + \
             [f"- #{s}: tohum `{h}` → plan `{i}`" for s, h, i in gevsetilen] + [""]
    CIKTI_RAPOR.write_text("\n".join(L) + "\n")
    print(f"plan yazıldı: {CIKTI_JSONL.relative_to(KOK)} (24 satır · derin {len(derin)}) · "
          f"havuz {havuz_n} · yaş gevşetmesi {len(gevsetilen)}")


if __name__ == "__main__":
    main()
