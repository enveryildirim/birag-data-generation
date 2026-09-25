# -*- coding: utf-8 -*-
"""«Kaç kaydımız var, 1.000'e ne kaldı» — sayının nasıl hesaplandığı (Kural 5).

⛔ `data/candidates/` ile `datasets/` TOPLANMAZ: adayların çoğu zaten
yayımlanmış kayıtların kendisi (v4-parti1'in 40 kaydının **38'i** `v0.0.3+`
içinde). Tekil `id` birleşimiyle çalışılır (T91).

⭐ 1.000 hedefi `plan.md` §6'dan: **v0.1.0 = ~800-1.200**, *«HER dilim temsil
edilir — iterasyon döngüsünün girdisi»*. Form hedefi (İP1) ayrı ve **10.000**.

⚠️ plan.md §6'nın 8 satırı **bölüntü değil**: "Terapötik tek tur" ile
"Kriz + rol sınırı" aynı kaydı sayabilir (biri tur yapısı, öteki senaryo).
Yüzdeleri 100 ediyor ama kesişimleri var ⇒ iki ayrı görünüm hesaplanır.
"""
from __future__ import annotations
import glob, hashlib, json
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent.parent
CIKTI = KOK / "reports/analiz/2026-09-16-bin-kayit-mesafesi.json"
HEDEF = 1000  # plan.md §6, v0.1.0 bandının ortası

# plan.md §6 — tur YAPISI görünümü (gerçek bölüntü)
YAPI_HEDEF = {"replay": 15, "rag": 10, "terapotik_cok_tur": 15, "terapotik_tek_tur": 35}
# plan.md §6 — SENARYO görünümü (örtüşebilir)
SENARYO_HEDEF = {"kriz_rol_siniri": 10, "direnc_inkar_discord": 5,
                 "nazikce_karsi_cikma": 5, "kapsam_disi_sinir": 5}
SENARYO_UYE = {
    "kriz_rol_siniri": {"rol_siniri", "hukuki_kaygi", "kriz"},
    "direnc_inkar_discord": {"inkar", "discord", "anlasilmama"},
    "nazikce_karsi_cikma": {"nazikce_karsi_cikma"},
    "kapsam_disi_sinir": {"bilgilendirme"},  # ⚠️ vekil; ayrı bir etiketi yok
}
# ⛔ Claude Code üretimiyle KAPANMAYAN dilimler
KILITLI = {
    "kriz_rol_siniri": "kriz alt-dilimi ETİK KURUL bekliyor (K23, uretim-v4 §8b)",
    "replay": "Claude Code üretimi DEĞİL — açık genel amaçlı setlerden örneklenir (plan §6)",
}


def _oku(yol: str) -> list[dict]:
    out = []
    for satir in Path(yol).read_text(encoding="utf-8").splitlines():
        satir = satir.strip()
        if satir:
            try:
                out.append(json.loads(satir))
            except json.JSONDecodeError:
                pass
    return out


def _yapi(k: dict) -> str:
    if k.get("replay"):
        return "replay"
    d = k.get("slice") or ""
    if d.startswith("rag"):
        return "rag"
    return d if d in YAPI_HEDEF else "diger"


def main() -> None:
    yayim: dict[str, dict] = {}
    surum_sha = {}
    for f in sorted(glob.glob(str(KOK / "datasets/v*/train.jsonl"))):
        surum_sha[Path(f).parent.name] = hashlib.sha256(Path(f).read_bytes()).hexdigest()[:16]
        for k in _oku(f):
            if k.get("id"):
                yayim[k["id"]] = k

    aday: dict[str, dict] = {}
    parti2 = set()
    for f in sorted(glob.glob(str(KOK / "data/candidates/*.jsonl"))):
        for k in _oku(f):
            if k.get("id"):
                aday[k["id"]] = k
                if k.get("gen_meta", {}).get("parti") == "v4-parti2":
                    parti2.add(k["id"])

    bekleyen = {i: k for i, k in aday.items() if i not in yayim}
    havuz = {**aday, **yayim}          # üretilmiş her şey
    kalan = HEDEF - len(yayim)

    def dagilim(kayitlar: dict) -> dict:
        y = Counter(_yapi(k) for k in kayitlar.values())
        s = {ad: sum(1 for k in kayitlar.values()
                     if (k.get("scenario") or "") in uye) for ad, uye in SENARYO_UYE.items()}
        return {"yapi": dict(y), "senaryo": s}

    ozet = {
        "tarih": "2026-09-16",
        "betik": "scripts/analiz/2026-09-16-bin-kayit-mesafesi.py",
        "hedef": HEDEF,
        "hedef_kaynagi": "plan.md §6 · v0.1.0 = ~800-1.200 (İP1 form hedefi AYRI: 10.000)",
        "dataset_sha256_16": surum_sha,
        "yayimlanmis_tekil": len(yayim),
        "en_guncel_surum": "v0.0.5",
        "uretilmis_tekil": len(havuz),
        "yayimlanmayi_bekleyen": len(bekleyen),
        "bunun_v4_parti2_olani": len(parti2 - set(yayim)),
        "hedefe_kalan_yayimlanmisa_gore": kalan,
        "hedefe_kalan_uretilmise_gore": HEDEF - len(havuz),
        "dagilim_yayimlanmis": dagilim(yayim),
        "dagilim_uretilmis": dagilim(havuz),
        "hedef_yuzde_yapi": YAPI_HEDEF,
        "hedef_yuzde_senaryo": SENARYO_HEDEF,
        "kilitli_dilimler": KILITLI,
    }

    # dilim bazında 1.000 ölçeğinde açık
    acik = {}
    for ad, yuzde in {**YAPI_HEDEF, **SENARYO_HEDEF}.items():
        hedef_adet = round(HEDEF * yuzde / 100)
        var = (ozet["dagilim_uretilmis"]["yapi"].get(ad)
               or ozet["dagilim_uretilmis"]["senaryo"].get(ad, 0))
        acik[ad] = {"hedef": hedef_adet, "uretilmis": var, "acik": hedef_adet - var,
                    "kilit": KILITLI.get(ad)}
    ozet["dilim_acigi"] = acik

    # ⛔ "Bekleyen" hepsi yayıma ADAY değil: expert-70 uretim-v2 ile üretildi ve
    # uzman PUANLAMA seti olarak duruyor; v3/v4 artıkları judge'dan düşenler.
    ozet["bekleyen_kirilimi"] = dict(Counter(
        k.get("gen_meta", {}).get("prompt_version") or "belirtilmemis"
        for k in bekleyen.values()))
    ozet["bekleyen_parti"] = dict(Counter(
        k.get("gen_meta", {}).get("parti") or "-" for k in bekleyen.values()))

    CIKTI.write_text(json.dumps(ozet, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"yayımlanmış tekil {len(yayim)} · üretilmiş tekil {len(havuz)} "
          f"· bekleyen {len(bekleyen)} (v4-parti2: {len(parti2 - set(yayim))})")
    print(f"1.000'e kalan — yayımlanmışa göre {kalan}, üretilmişe göre {HEDEF - len(havuz)}")
    print("\ndilim açığı (1.000 ölçeğinde):")
    for ad, d in sorted(acik.items(), key=lambda x: -x[1]["acik"]):
        kilit = f"  ⛔ {d['kilit']}" if d["kilit"] else ""
        print(f"  {ad:24s} hedef {d['hedef']:>4} · var {d['uretilmis']:>4} · açık {d['acik']:>4}{kilit}")
    print(f"\nbekleyen {len(bekleyen)} kaydın kırılımı: {ozet['bekleyen_kirilimi']}")
    print(f"  parti: {ozet['bekleyen_parti']}")
    print(f"→ {CIKTI.relative_to(KOK)}")


if __name__ == "__main__":
    main()
