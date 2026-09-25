#!/usr/bin/env python3
"""v3 parti 2 — bağlamsız 32 satırın planı. ⚠️ ÇIKTI DONDURULUR.

K70'in yapısal düzeltmesi: **plan SENARYO yazmaz.** Parti 1'de senaryo planda
bağlanmıştı ve 40 satırın 13'ü tohumla çelişti; kök sebep, anahtar kelime kapısının
kelimeyi görüp durumu görmemesi. Senaryo artık tohumu okuyan YAZIM adımında
belirleniyor (K70: arketip ataması bir öneridir). Kapsama ise kaybolmasın diye
üretim betiğinde KOTA olarak denetleniyor.

Plan yalnızca DENETLENEN alanları bağlar: tur · yaş · turn_type · mi_process ·
konusma_durumu · turn_ending · sysvar · is_negative · ozerklik.

Oranlar parti 2'nin 40 kaydı için hesaplandı; bağlam dilimi (8 kayıt) neyi
harcadıysa kalan 32 onu tamamlıyor.

Girdi : data/seeds.jsonl
Çıktı : data/plan/v3-parti2.jsonl + reports/analiz/2026-09-14-v3-parti2-plani.md
"""
from __future__ import annotations

import collections, hashlib, json, random, re, sys, unicodedata
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
SEEDS = KOK / "data/seeds.jsonl"
CIKTI_JSONL = KOK / "data/plan/v3-parti2.jsonl"
CIKTI_RAPOR = KOK / "reports/analiz/2026-09-14-v3-parti2-plani.md"
RASTGELE = random.Random(207)

# Kalan 32'nin hedefleri (parti 2 = 40 kayıt; bağlam dilimi 8'i harcadı).
HEDEF32 = {
    "turn_ending": {"acik_uclu_soru": 15, "takdir": 6, "ozet": 6, "yalnizca_yansitma": 4, "durur": 1},
    "konusma_durumu": {"tetikleyici_an": 13, "suregiden_durum": 7, "iyi_giden_paylasim": 6,
                       "plan_yapma": 5, "aradan_donus": 1},
    "mi_process": {"engaging": 11, "focusing": 6, "evoking": 9, "planning": 6},
    "sysvar": {"canon": 25, "paraphrase": 7},
}
HEDEF_NEG, HEDEF_OZERK, HEDEF_MULTI, HEDEF_ERGEN = 4, 6, 8, 6

A = ("tur", "yas", "turn_type", "mi_process", "konusma_durumu", "turn_ending",
     "sysvar", "is_negative", "ozerklik")
P = [
    # ── tetikleyici an (13) ──────────────────────────────────────────────────
    ("alkol",         "yetiskin", "single", "engaging", "tetikleyici_an", "acik_uclu_soru",    "canon",      0, 0),
    ("kumar",         "yetiskin", "single", "engaging", "tetikleyici_an", "yalnizca_yansitma", "canon",      0, 0),
    ("tutun",         "ergen",    "single", "engaging", "tetikleyici_an", "acik_uclu_soru",    "paraphrase", 0, 0),
    ("receteli_ilac", "yetiskin", "single", "engaging", "tetikleyici_an", "acik_uclu_soru",    "canon",      1, 1),
    ("alkol",         "yetiskin", "multi",  "evoking",  "tetikleyici_an", "acik_uclu_soru",    "canon",      0, 0),
    ("dijital",       "ergen",    "single", "engaging", "tetikleyici_an", "durur",             "canon",      0, 1),
    ("kumar",         "yetiskin", "single", "focusing", "tetikleyici_an", "acik_uclu_soru",    "canon",      0, 0),
    ("alkol",         "yetiskin", "single", "engaging", "tetikleyici_an", "yalnizca_yansitma", "paraphrase", 0, 0),
    ("tutun",         "yetiskin", "single", "focusing", "tetikleyici_an", "acik_uclu_soru",    "canon",      0, 0),
    ("receteli_ilac", "yetiskin", "multi",  "evoking",  "tetikleyici_an", "ozet",              "canon",      0, 0),
    ("kumar",         "yetiskin", "single", "engaging", "tetikleyici_an", "acik_uclu_soru",    "canon",      0, 0),
    ("dijital",       "ergen",    "single", "evoking",  "tetikleyici_an", "acik_uclu_soru",    "canon",      0, 0),
    ("alkol",         "yetiskin", "single", "focusing", "tetikleyici_an", "acik_uclu_soru",    "paraphrase", 1, 1),
    # ── süregiden durum (7) ──────────────────────────────────────────────────
    ("tutun",         "yetiskin", "single", "focusing", "suregiden_durum", "acik_uclu_soru",    "canon",      0, 0),
    ("alkol",         "yetiskin", "multi",  "focusing", "suregiden_durum", "ozet",              "canon",      0, 0),
    ("kumar",         "yetiskin", "single", "evoking",  "suregiden_durum", "yalnizca_yansitma", "canon",      0, 0),
    ("receteli_ilac", "yetiskin", "single", "focusing", "suregiden_durum", "acik_uclu_soru",    "canon",      1, 1),
    ("dijital",       "ergen",    "single", "evoking",  "suregiden_durum", "ozet",              "canon",      0, 0),
    ("tutun",         "yetiskin", "multi",  "evoking",  "suregiden_durum", "acik_uclu_soru",    "paraphrase", 0, 0),
    ("alkol",         "yetiskin", "single", "engaging", "suregiden_durum", "yalnizca_yansitma", "canon",      0, 0),
    # ── iyi giden paylaşım (6) ───────────────────────────────────────────────
    ("tutun",         "yetiskin", "single", "evoking",  "iyi_giden_paylasim", "takdir", "canon",      0, 0),
    ("alkol",         "yetiskin", "single", "evoking",  "iyi_giden_paylasim", "takdir", "canon",      0, 0),
    # ⚠️ tür kumar → alkol: kumar tohumlarında KULLANICININ KENDİ ifade ettiği,
    # sayılabilir bir ilerleme anlatan tek mesaj yok (K64'ün durumu). Uydurmak yerine
    # tür değiştirildi; `tur` v3'te hedef dağılımı olan bir alan değil.
    ("alkol",         "yetiskin", "single", "engaging", "iyi_giden_paylasim", "takdir", "paraphrase", 0, 0),
    ("dijital",       "ergen",    "single", "engaging", "iyi_giden_paylasim", "takdir", "canon",      0, 0),
    ("receteli_ilac", "yetiskin", "multi",  "evoking",  "iyi_giden_paylasim", "ozet",   "canon",      0, 0),
    ("alkol",         "yetiskin", "single", "planning", "iyi_giden_paylasim", "takdir", "canon",      0, 0),
    # ── plan yapma (5) ───────────────────────────────────────────────────────
    ("tutun",         "yetiskin", "multi",  "planning", "plan_yapma", "acik_uclu_soru", "canon",      0, 0),
    ("alkol",         "yetiskin", "single", "planning", "plan_yapma", "ozet",           "canon",      0, 1),
    ("kumar",         "yetiskin", "multi",  "planning", "plan_yapma", "acik_uclu_soru", "paraphrase", 0, 0),
    ("receteli_ilac", "yetiskin", "single", "planning", "plan_yapma", "takdir",         "canon",      0, 0),
    ("dijital",       "ergen",    "multi",  "planning", "plan_yapma", "ozet",           "canon",      0, 0),
    # ── aradan dönüş (1) ─────────────────────────────────────────────────────
    ("alkol",         "yetiskin", "single", "engaging", "aradan_donus", "acik_uclu_soru", "paraphrase", 1, 1),
]
PLAN = [dict(zip(A, s)) for s in P]

KRIZ_ANAHTAR = [
    "yaşamak istemiyorum", "ölmek istiyorum", "intihar", "canıma kıy", "kendimi asa",
    "kendime zarar", "bitirmek istiyorum", "son vermek istiyorum", "uyanmasam",
    "uyanmak istemiyorum", "yaşamaya değmez", "hayatıma son", "bileğimi", "hapları içt",
    "yok olmak istiyorum", "ölsem", "öldürmek istiyorum kendimi", "yük oluyorum",
    "bensiz daha iyi", "dayanamıyorum artık", "kurtulmak istiyorum bu hayattan",
    "acil servis", "acilde", "ambulans", "mide yıkan", "yoğun bakım", "doz aşımı",
    "aşırı doz", "taburcu", "entübe", "komaya",
    # K65'te bulunan açık: uyuşukluk hâlinde araç kullanma listede yoktu.
    "direksiyonda", "gözüm kapandı", "araba kullan",
]


# ⚠️ 2026-09-14: eşdurum listesi taraması. Plan ilk koşuda #5'e "Aktif intihar
# düşüncesi + Hastane yoksunluk vakası" taşıyan bir tohum atadı; filtre bunu
# kaçırmıştı çünkü (a) `notlar.esdurumlar` hiç taranmıyordu, (b) `risk_seviyesi`
# yalnızca `cok_yuksek` eleniyordu, `yuksek` değil. Havuzda 2240 tohumun 52'si
# riskli eşdurum taşıyor.
RISKLI_ESDURUM = ("intihar", "kendine zarar", "öz kıyım", "özkıyım", "psikoz",
                  "sanrı", "yoksunluk vakası", "deliryum", "nöbet", "overdoz", "aşırı doz")


def tr_kucult(s: str) -> str:
    """Türkçeye uygun küçültme. `"İntihar".lower()` → `"i̇ntihar"` (i + birleşen
    nokta) çıkıyor ve `"intihar"` ile EŞLEŞMİYOR. Havuzda bu hata yüzünden 52
    riskli tohumun 21'i taramadan kaçıyordu — düz `.lower()` yalnızca 31'ini buluyor."""
    s = s.replace("İ", "i").replace("I", "ı").lower()
    return unicodedata.normalize("NFKD", s).replace("\u0307", "")


def kriz_icerigi(t):
    metin = tr_kucult(t["user_message"] + " " + t.get("scenario_context", ""))
    vurus = [a for a in KRIZ_ANAHTAR if tr_kucult(a) in metin]
    for e in t["meta"].get("notlar", {}).get("esdurumlar", []):
        vurus += [f"eşdurum:{e}" for k in RISKLI_ESDURUM if k in tr_kucult(e)]
    return vurus


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
    for f in ("expert-70", "v3-parti1", "v3-parti2-baglam"):
        for satir in open(KOK / f"data/candidates/{f}.jsonl"):
            kul.add(json.loads(satir)["gen_meta"]["seed_id"])
    return kul


def dogrula() -> list[str]:
    s = []
    if len(PLAN) != 32:
        s.append(f"plan {len(PLAN)} satır, 32 bekleniyordu")
    for alan, hedef in HEDEF32.items():
        var = collections.Counter(r[alan] for r in PLAN)
        for k, h in hedef.items():
            if var.get(k, 0) != h:
                s.append(f"{alan} `{k}`: {var.get(k,0)} satır, {h} bekleniyordu")
        for k in var:
            if k not in hedef:
                s.append(f"{alan} `{k}`: planda var, hedefte yok")
    for ad, sayi, hedef in [("is_negative", sum(r["is_negative"] for r in PLAN), HEDEF_NEG),
                            ("ozerklik", sum(r["ozerklik"] for r in PLAN), HEDEF_OZERK),
                            ("multi", sum(r["turn_type"] == "multi" for r in PLAN), HEDEF_MULTI),
                            ("ergen", sum(r["yas"] == "ergen" for r in PLAN), HEDEF_ERGEN)]:
        if sayi != hedef:
            s.append(f"{ad}: {sayi} satır, {hedef} bekleniyordu")
    for r in PLAN:
        if (r["turn_ending"] == "acik_uclu_soru") != (r["turn_ending"] == "acik_uclu_soru"):
            s.append("iç tutarsızlık")
    return s


# ⚠️ 2026-09-14: `iyi_giden_paylasim` İÇERİK KAPISI. Plan ilk koşuda bu satırlara
# paylaşılacak iyi bir şeyi OLMAYAN tohumlar atadı (komşunun sigarayı görmesi, eşin
# çocukları önden yatırması, "kimse anlamıyor"). Kök sebep: senaryo plandan çıkarılınca
# (K70) onunla birlikte içerik kapısı da düştü — oysa K64 bu durumu ayrıca şarta
# bağlamıştı: kullanıcının KENDİ ifade ettiği, sayılabilir bir ilerleme aranır.
# Yoksunluk BELİRTİSİ anlatan tohumlar elenir: titreme, gece terlemesi, nöbet vb.
# tıbbi aciliyet sinyalidir ve kriz davranışı uzman Oturum 1'e bağlı (Kural 3).
# K76'da karantinaya alınan kayıtla aynı sınıf.
# ⚠️ SABİT İFADE DEĞİL, DESEN. İlk yazımda sabit ifadeydi ve "sağ elim hafif titriyor"
# eşleşmedi — araya bir sıfat girince alt dize tutmuyor. Bugünün dördüncü aynı hatası
# (K65 anahtar kelime, K76 Türkçe kasa, §7b klinik iddia, şimdi bu).
YOKSUNLUK_BELIRTI = re.compile(
    r"\bel(im|lerim|i)?\b[^.!?]{0,25}\btitri|\btitreme\b|\bter(liyorum| içinde)\b"
    r"|terleyerek uyan|\bnöbet geçir|\bhavale\b|sanrı gör|\bkusuyorum\b|sayıklıyor"
    r"|\bçarpıntı\b|kalbim (hızlı|küt küt)", re.IGNORECASE)

# Elle okunup PIN'lenen satırlar: anahtar kelime kapısı `iyi_giden_paylasim` için
# üç satırda yanlış pozitif verdi ("içmiyorum" alıntı ya da pazarlık içinde eşleşti).
PIN = {21: "4d8b5d0398", 23: "5696ab6d18", 26: "e2af6f9c35"}

ILERLEME = ("gün oldu", "gün olmuş", "ay oldu", "ay olmuş", "yıl oldu", "hiç içmedim",
            "hiç oynamadım", "hiç içmiyorum", "bıraktım", "bırakalı", "azalttım",
            "yarıya indirdim", "içmiyorum", "oynamıyorum", "kullanmıyorum", "başardım",
            "temiz tamamladım", "gitmedim", "elimi sürmedim")
# Aynı mesajda kaymayı anlatıyorsa "iyi giden paylaşımı" değildir.
KAYMA = ("yine", "tekrar başladım", "bozdum", "kupon yaptım", "içtim", "oynadım",
         "aldım gene", "dayanamadım", "sıfırladım")


# Yazılmış kayıtların tohumları (1-16). Bunlar zaten metne dönüştü;
# içerik kapısı eklendiğinde yeniden atanmamaları için sabitlendi.
SABIT = {
    1: "42fad6ddf97b0b7e",
    2: "ac4c83526b07c190",
    3: "ff6a975e4247eb49",
    4: "c10d8383d9be974f",
    5: "79b1db35e48acc9e",
    6: "7be15f2345988b9b",
    7: "e8b4cb74833dbe63",
    8: "d83bf265bc006dbf",
    9: "9cd9e6ff60f06176",
    10: "86bc03d728a432c2",
    11: "51dfa194262918b7",
    12: "851639fc4365fce7",
    13: "d00a5985b5d0a605",
    14: "f540261f79364549",
    15: "69c52cb9cb9ded6f",
    16: "e3334f734aa608ec",
}

def iyi_giden_uygun(t) -> bool:
    m = tr_kucult(t["user_message"])
    return any(tr_kucult(a) in m for a in ILERLEME) and not any(tr_kucult(k) in m for k in KAYMA)


def ata(tohumlar):
    kul = kullanilmis(tohumlar)
    havuz = [t for t in tohumlar
             if t["seed_id"] not in kul
             and t["meta"].get("senaryo") != "kriz"
             and t["meta"].get("risk_seviyesi") != "cok_yuksek"
             and not kriz_icerigi(t)
             and not YOKSUNLUK_BELIRTI.search(t["user_message"])]
    # Kriz dilimi uzman Oturum 1'e kadar kapalı (Kural 3); sınırdaki tohumlar da girmez.
    RASTGELE.shuffle(havuz)
    alinan, atama, eksik, gevsetilen = set(), {}, [], []
    # Elle okunup sabitlenen satırlar (PIN) ve yazılmış satırlar (SABIT) önce.
    # Yazılmış satırların tohumu SABİT: 1-16 zaten kayda dönüştü, yeniden atamak
    # yazılmış metinle planı ayırır. Kapı eklendiği için yalnızca 17-32 yeniden atanıyor.
    for sira, onek in PIN.items():
        eslesen = [t for t in havuz if t["seed_id"].startswith(onek)]
        if len(eslesen) != 1:
            raise SystemExit(f"PIN #{sira} öneki {onek}: havuzda {len(eslesen)} eşleşme")
        atama[sira - 1] = eslesen[0]
        alinan.add(eslesen[0]["seed_id"])
    for sira, sid in SABIT.items():
        t = next((x for x in tohumlar if x["seed_id"] == sid), None)
        if t is None:
            raise SystemExit(f"SABİT #{sira}: tohum bulunamadı ({sid})")
        atama[sira - 1] = t
        alinan.add(sid)
    # en dar kısıt önce: iyi_giden içerik kapısı, sonra ergen
    for i in sorted(range(len(PLAN)),
                    key=lambda i: (PLAN[i]["konusma_durumu"] != "iyi_giden_paylasim",
                                   PLAN[i]["yas"] != "ergen")):
        if i in atama:
            continue
        s, aday = PLAN[i], None
        for yas_zorunlu in (True, False):
            for t in havuz:
                if t["seed_id"] in alinan:
                    continue
                m = t["meta"]
                if m.get("bagimlilik_turu") != s["tur"]:
                    continue
                if yas_zorunlu and (m.get("yas_grubu") or "yetiskin") != s["yas"]:
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


def main():
    tohumlar = [json.loads(s) for s in open(SEEDS)]
    sorun = dogrula()
    if sorun:
        print("DOĞRULAMA DÜŞTÜ — plan yazılmadı:")
        for x in sorun:
            print("  ·", x)
        sys.exit(1)
    atama, eksik, havuz_n, gevsetilen = ata(tohumlar)
    if eksik:
        print(f"DOĞRULAMA DÜŞTÜ — {len(eksik)} satıra tohum bulunamadı: "
              f"{[i+1 for i in eksik]}")
        sys.exit(1)

    CIKTI_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with open(CIKTI_JSONL, "w") as f:
        for i, r in enumerate(PLAN):
            t = atama[i]
            d = {"sira": i + 1, **r, "seed_id": t["seed_id"], "source_id": t["source_id"],
                 "tohum_senaryo": t["meta"].get("senaryo"), "tohum_yas": t["meta"].get("yas_grubu"),
                 "user_message": t["user_message"]}
            f.write(json.dumps(d, ensure_ascii=False) + "\n")

    L = ["# v3 parti 2 — bağlamsız 32 satırın planı", "",
         f"**Çıktı:** `data/plan/v3-parti2.jsonl` · SHA256 "
         f"`{hashlib.sha256(CIKTI_JSONL.read_bytes()).hexdigest()}`  ",
         f"**Betik:** `scripts/analiz/2026-09-14-v3-parti2-plani.py` · "
         f"**Tarih:** {TARIH} · **Havuz:** {havuz_n} kullanılmamış tohum", "",
         "---", "",
         "## ⭐ Parti 1'den yapısal fark: plan SENARYO yazmıyor", "",
         "Parti 1'de senaryo planda bağlanmıştı ve **40 satırın 13'ü tohumla çelişti** "
         "(K70) — anahtar kelime kapısı kelimeyi görüyor, durumu görmüyor. Senaryo artık "
         "tohumu okuyan **yazım adımında** belirleniyor; kapsama kaybolmasın diye üretim "
         "betiğinde **kota** olarak denetleniyor.", "",
         "## Hedefler — parti 2'nin 40 kaydına göre", "",
         "Bağlam dilimi (8 kayıt) ne harcadıysa kalan 32 onu tamamlıyor.", ""]
    for alan, hedef in HEDEF32.items():
        var = collections.Counter(r[alan] for r in PLAN)
        L += [f"### {alan}", "", "| Değer | Plan | Hedef |", "|---|---:|---:|"]
        L += [f"| `{k}` | {var.get(k,0)} | {h} |" for k, h in hedef.items()]
        L += [""]
    L += ["### Diğer", "", "| Ölçüm | Plan | Hedef |", "|---|---:|---:|",
          f"| `is_negative` | {sum(r['is_negative'] for r in PLAN)} | {HEDEF_NEG} |",
          f"| özerklik görünür | {sum(r['ozerklik'] for r in PLAN)} | {HEDEF_OZERK} |",
          f"| çok turlu | {sum(r['turn_type']=='multi' for r in PLAN)} | {HEDEF_MULTI} |",
          f"| ergen | {sum(r['yas']=='ergen' for r in PLAN)} | {HEDEF_ERGEN} |", ""]
    if gevsetilen:
        L += ["## ⚠️ Yaş gevşetmesi", "",
              "Tür + yaş birlikte sağlanamadığında yaş kısıtı gevşetildi:", ""]
        L += [f"- #{s}: tohum `{ham}` → plan `{ist}`" for s, ham, ist in gevsetilen]
        L += [""]
    L += ["## ⚠️ Kriz listesi genişletildi", "",
          "K65'te bulunan açık kapatıldı: `direksiyonda`, `gözüm kapandı`, `araba kullan` "
          "`KRIZ_ANAHTAR`'a eklendi. Tam liste hâlâ uzman Oturum 1'e bağlı.", ""]
    CIKTI_RAPOR.write_text("\n".join(L) + "\n")
    print(f"plan yazıldı: {CIKTI_JSONL.relative_to(KOK)} (32 satır) · "
          f"havuz {havuz_n} · yaş gevşetmesi {len(gevsetilen)}")


if __name__ == "__main__":
    main()
