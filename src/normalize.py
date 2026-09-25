"""Ham campaigns metadata -> kanonik meta (configs/taxonomy.yaml).

Kullanim:
  uv run python src/normalize.py <input.jsonl> [--report]
  uv run python src/normalize.py --build-seeds [out.jsonl]   # data/seeds.jsonl (Faz 1, K26)

Bkz. plan.md §5, §13 Faz 1, PROJECT_MEMORY K26.
"""
from __future__ import annotations
import hashlib, json, re, sys, unicodedata
from pathlib import Path

import yaml

# ⛔ Türkçe küçültme TEK kaynaktan (T76). Düz `.lower()` burada üç yerde yanlıştı ve
# ikisi SESSİZCE YANLIŞ DEĞER üretiyordu: `"İlkokul"` -> `belirtilmemis` (fallback,
# izi var) ve `"3 YILDAN FAZLA"` -> `1_3_yil` (⛔ YANLIŞ KOVA, izi YOK).
# ⚠️ `tr_fold` NFKD uygulamaz: `norm_sure` regex'le çalışıyor ve NFKD `\b` semantiğini
# bozuyor. Ayrıştırılmış ç/ş/ğ hâlâ kaçabilir — açık kalem (T75 · T76).
# ⭐⭐ İKİ AYRI FOLD, BİLEREK (T84). Aynı modülde iki normalizasyon bir karmaşa
# değil, iki farklı RİSK profilinin karşılığı:
#   · `tr_sadelestir` (aksan da düşer) → `norm_egitim`, `norm_sure`. Kazanç:
#     `Universite`/`Lisansustu`/`3 yildan fazla` artık eşleşiyor. Bedeli ölçüldü:
#     taksonomide çakışma yok, ham 2240 kayıtta `egitim` farkı 0.
#   · `tr_fold` (yalnız i-sınıfı) → `_keyword`. ⛔ Orada aksan düşürmek
#     UYGULANMADI: anahtarların 31'i ≤5 karakter ve `iş` → `is` olunca
#     **`isolation`** içinde eşleşiyor. Bugün kural sırası bunu maskeliyor
#     (`monotony_isolation` önce `monoton`a düşüyor) ⚠️ ama maskeyi tasarım değil
#     RASTLANTI tutuyor. Kazanç 5 tartışmalı kayıt, risk sessiz yanlış etiket
#     (T76'nın sınıfı) ⇒ uygulanmadı.
from tohum_guvenlik import tr_fold, tr_sadelestir

TAX = yaml.safe_load((Path(__file__).parent.parent / "configs" / "taxonomy.yaml").read_text())

# Onaylı kaynak (plan.md §0) — yalnızca kullanıcı mesajı yeniden kullanılır (K26).
CAMPAIGNS_DIR = Path("/Users/pc/projects/birag/birag-tubitak/agentic_dataset_generation/campaigns")
CAMPAIGN_FILES = {
    "kimyasal_madde": CAMPAIGNS_DIR / "kimyasal_madde" / "total_output.jsonl",
    "dijital": CAMPAIGNS_DIR / "dijital" / "total_output.jsonl",
    "receteli_ilac": CAMPAIGNS_DIR / "receteli_ilac" / "total_output.jsonl",
    "davranissal": CAMPAIGNS_DIR / "davranissal" / "total_output.jsonl",
}

_PAREN = re.compile(r"\s*\(([^)]*)\)")
_AGE = re.compile(r"(\d{1,2})\s*[-–]\s*(\d{1,2})|(\d{1,2})")


def slug(s: str) -> str:
    s = s.strip().lower()  # lower-muaf: slug() ı->i eşlemesi yapıyor, ayrımı TASARIM GEREĞİ kullanmıyor (T76)
    for a, b in zip("çğıöşü", "cgiosu"):
        s = s.replace(a, b)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def _exact(field: str, raw: str):
    return TAX.get(field, {}).get("alias", {}).get(raw)


def _prefix(field: str, raw: str):
    for pre, canon in TAX.get(field, {}).get("alias_onek", {}).items():
        if raw.startswith(pre):
            return canon
    return None


def _contains(field: str, raw: str):
    """Öncelik sıralı alt-dizi eşleşmesi; ilk eşleşen kazanır."""
    for pat, canon in TAX.get(field, {}).get("alias_icerik", []):
        if pat in raw:
            return canon
    return None


_KW_DESEN: dict[str, "re.Pattern[str]"] = {}


def _kw_metin(raw: str) -> str:
    r"""Anahtar taramasının gördüğü metin. ⭐ `_` bir KELİME AYRIMI, harf değil:
    `physical_fatigue` iki sözcüktür ve `\b` onu öyle görmeli (T77)."""
    return tr_fold(raw or "").replace("_", " ")


def _kw_desen(anahtar: str) -> "re.Pattern[str]":
    r"""Anahtarı metinle AYNI normalizasyona sokup **kelime BAŞI** sınırıyla derler.

    ⛔ `.strip()` YOK ve `\w*` YOK — ikisi de anlambilimi genişletirdi:
    `"eş "` anahtarının sondaki boşluğu kasıtlı (`eşya`/`eşit` eşleşmesin diye),
    ek serbestliği ise `\b` ile zaten geliyor (`\biş` → `işim` ✅, `girişimci` ⛔).
    """
    if anahtar not in _KW_DESEN:
        _KW_DESEN[anahtar] = re.compile(r"\b" + re.escape(_kw_metin(anahtar)))
    return _KW_DESEN[anahtar]


def _keyword(field: str, raw: str):
    r"""Anahtar kelimeyle kanon bulma — İKİ kusuru 2026-09-16'da kapatıldı (T77).

    1. **Kasing:** düz `.lower()` doğru Türkçe büyütmede 76 anahtarın 37'sini
       öldürüyordu; `"İş stresi"` hiçbir kanona düşmüyordu (**ham veride 20 kayıt**).
    2. **Alt-dize:** `iş` anahtarı `girişimci`/`gelişim`/`değişim` kelimelerini
       `is_stresi` sayıyordu — **K65'in ailesi**, çözümü `checks.KLINIK_IDDIA`'da
       zaten vardı, buraya hiç gelmemişti.

    ⭐ İkisi ayrı ayrı kapatılamıyordu: yalnız i-sınıfı **5 gerileme** üretiyor
    (`"Aile çatışması stresi"` → `çatişmasi` içinde `iş` var), yalnız kelime sınırı
    kasingi çözmüyor. ⛔ Ve `\b` tek başına İngilizce `snake_case` değerleri bozdu
    (`physical_fatigue`'de `_` bir kelime karakteri, `fatigue`'ün önünde `\b` yok):
    **14 gerileme**. Üçü birden — i-sınıfı + `_`→boşluk + kelime başı — ham 2240
    kayıtta **20 düzeltme, 0 gerileme** veriyor ve ölçüm kullanıcı onayıyla okunan
    ham kampanya meta'sına karşı yapıldı (Kural 1).
    """
    low = _kw_metin(raw)
    for keys, canon in TAX.get(field, {}).get("anahtar_kelime", []):
        if any(_kw_desen(k).search(low) for k in keys):
            return canon
    return None


def split_paren(raw: str) -> tuple[str, str | None]:
    m = _PAREN.search(raw)
    return (_PAREN.sub("", raw).strip(), m.group(1)) if m else (raw.strip(), None)


def age_band(text: str | None) -> str | None:
    if not text:
        return None
    m = _AGE.search(str(text))
    if not m:
        return None
    n = int(m.group(1) or m.group(3))
    return ("ergen" if n < 18 else "genc_yetiskin" if n <= 25 else
            "yetiskin" if n <= 44 else "orta_yas" if n <= 64 else "yasli")


def norm_profil(raw: str):
    base, paren = split_paren(raw)
    base = re.sub(r"\b(Erkek|Kadın|Kız|Genç|Yetişkin)\b", "", base).strip()
    return _contains("profil", base) or "diger", paren


def norm_sure(raw: str):
    if not raw:
        return "belirtilmemis"
    t = tr_sadelestir(raw)    # ⛔ "3 YILDAN FAZLA" sessizce `1_3_yil` oluyordu (T76)
    if "ay" in t and not re.search(tr_sadelestir(r"\byıl|yil\b"), t.split("ay")[0][-12:]):
        m = re.search(r"(\d+)\s*(?:-|–|\s)*\d*\s*ay", t)
        if m:
            return "0_6_ay" if int(m.group(1)) < 6 else "6_ay_1_yil"
    m = re.search(r"(\d+)", t)
    if not m:
        return "belirtilmemis"
    n = int(m.group(1))
    if tr_sadelestir("3 yıldan fazla") in t:
        return "3_10_yil"
    return ("0_6_ay" if n < 1 else "1_3_yil" if n <= 3 else
            "3_10_yil" if n <= 10 else "10_yil_ustu")


def norm_egitim(raw: str):
    t = tr_sadelestir(raw or "")  # ⛔ "İlkokul"/"LİSE" düşüyordu (T76), "Universite" de (T84)
    for key, canon in (("lisansüstü", "lisansustu"), ("yüksek lisans", "lisansustu"),
                       ("mba", "lisansustu"), ("üniversite", "universite"),
                       ("lisans", "universite"), ("lise", "lise"),
                       ("ortaokul", "ortaokul"), ("ilkokul", "ilkokul")):
        if tr_sadelestir(key) in t:
            return canon
    return "belirtilmemis"


def normalize(meta: dict) -> dict:
    out, notes = {}, {}
    g = lambda k: str(meta.get(k, "") or "").strip()

    out["bagimlilik_turu"] = _exact("bagimlilik_turu", g("addiction_type")) or "diger"
    alt, plat = split_paren(g("addiction_sub_category"))
    out["bagimlilik_alt_turu"] = TAX["bagimlilik_alt_turu"]["alias_kural"].get(alt) or slug(alt) or None
    if plat:
        notes["platform_notu"] = plat

    st = g("stress_type")
    out["senaryo"] = _exact("senaryo", st) or "belirsiz"
    out["stres_tipi"] = (_exact("stres_tipi", st) or _keyword("stres_tipi", st)
                         or ("yok" if out["senaryo"] != "belirsiz" else None))

    out["profil"], yas_p = norm_profil(g("profile"))
    out["yas_grubu"] = age_band(g("yas") or yas_p)

    out["evre"] = _exact("evre", g("stage")) or _exact("evre", g("baslangic_evresi"))
    out["motivasyon_evresi"] = _exact("motivasyon_evresi", g("motivasyon_evresi"))

    mot = g("motivation")
    out["motivasyon"] = _prefix("motivasyon", mot)
    if "—" in mot:
        notes["motivasyon_notu"] = mot.split("—", 1)[1].strip()

    risk = g("risk_seviyesi")
    out["risk_seviyesi"] = _exact("risk_seviyesi", risk) or _exact("risk_seviyesi", split_paren(risk)[0])
    if split_paren(risk)[1]:
        notes["risk_notu"] = split_paren(risk)[1]
    out["siddet_seviyesi"] = _exact("siddet_seviyesi", g("siddet_seviyesi"))

    out["egitim"] = norm_egitim(g("egitim_durumu"))
    out["kullanim_suresi"] = norm_sure(g("kullanim_suresi"))
    out["onceki_tedavi"] = _prefix("onceki_tedavi", g("onceki_tedavi") or g("onceki_tedevi")) or "bilinmiyor"

    cins = g("cinsiyet")
    out["cinsiyet"] = ("belirtilmemis" if cins.startswith("Karışık") or not cins
                       else {"Kadın": "kadin", "Erkek": "erkek"}.get(cins, "belirtilmemis"))

    for k in TAX["serbest_alanlar"]:
        if meta.get(k):
            notes[k] = meta[k]
    out["notlar"] = notes
    return out


def build_seed(row: dict, campaign: str, idx: int) -> dict:
    """Tek kayıttan tohum üretir. Yalnızca kullanıcı mesajı + kanonik meta taşınır —
    asistan cevabı DOĞRULANMAMIŞ sayıldığından (K26) buraya girmez."""
    user_msgs = [m["content"] for m in row.get("messages", []) if m.get("role") == "user"]
    source_id = f"{campaign}:{row.get('meta', {}).get('sub_task_id', 'na')}:{idx:04d}"
    return {
        "seed_id": hashlib.sha256(source_id.encode()).hexdigest()[:16],
        "source_id": source_id,
        "campaign": campaign,
        "user_message": user_msgs[0] if user_msgs else "",
        "turn_count": len(user_msgs),
        "scenario_context": row.get("scenario"),  # 3. şahıs betimleme — kampanya mimarisi, düşük risk
        "meta": normalize(row["meta"]),
    }


def build_seeds(out_path: Path) -> None:
    from schemas import SeedMeta  # local import: normalize.py tek başına da çalışabilsin
    from pydantic import ValidationError

    seeds, invalid = [], []
    for campaign, path in CAMPAIGN_FILES.items():
        if not path.exists():
            print(f"⚠️  atlanan (bulunamadı): {path}")
            continue
        rows = [json.loads(l) for l in open(path) if l.strip()]
        for i, r in enumerate(rows):
            seed = build_seed(r, campaign, i)
            try:
                SeedMeta(**seed["meta"])
            except ValidationError as e:
                invalid.append((seed["source_id"], str(e)))
                continue
            seeds.append(seed)

    ids = [s["seed_id"] for s in seeds]
    dup = len(ids) - len(set(ids))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        for s in seeds:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    belirsiz = sum(1 for s in seeds if s["meta"]["senaryo"] == "belirsiz")
    print(f"yazıldı: {out_path}  tohum: {len(seeds)}  geçersiz meta: {len(invalid)}  "
          f"yinelenen seed_id: {dup}  senaryo=belirsiz: {belirsiz}")
    for sid, err in invalid[:3]:
        print(f"  [{sid}] {err.splitlines()[0]}")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "--build-seeds":
        out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).parent.parent / "data" / "seeds.jsonl"
        build_seeds(out)
        sys.exit(0)

    import collections
    rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
    normed = [normalize(r["meta"]) for r in rows]
    fields = [k for k in normed[0] if k != "notlar"]
    print(f"kayit: {len(normed)}\n")
    print(f"{'alan':22s} {'kapsama':>8s}  {'essiz':>5s}  eksik ornek")
    for f in fields:
        vals = [n.get(f) for n in normed]
        MISSING = (None, "", "belirsiz")
        miss = sum(1 for v in vals if v in MISSING)
        ex = next((rows[i]["meta"] for i, v in enumerate(vals) if v in MISSING), None)
        exs = ""
        if ex:
            src = {"senaryo": "stress_type", "stres_tipi": "stress_type", "evre": "stage",
                   "profil": "profile", "bagimlilik_alt_turu": "addiction_sub_category"}.get(f, f)
            exs = str(ex.get(src, ""))[:42]
        print(f"{f:22s} {100*(len(vals)-miss)/len(vals):7.1f}%  {len(set(v for v in vals if v)):5d}  {exs}")
