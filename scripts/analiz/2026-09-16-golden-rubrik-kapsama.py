#!/usr/bin/env python3
"""Golden eval seti rubriğin NE KADARINI sınıyor — rubrik büyüdü, set büyümedi.

⛔ Nasıl bulundu: `2026-09-14-golden-dev.py` kendi yayımlanmış raporunu yeniden
üretemiyordu (K126 denetimi). Sebep tarih değil, GİRDİ: betik canlı rubriği
(`JudgeResult`) okuyor. 09-14'te rubrikte 37 boyut vardı ve *«öğe düzeyinde
kapanmamış boyut kalmadı»* doğruydu. Rubrik v9'da 81 alana çıktı; golden seti
(K31 mühürlü, 48 öğe) yerinde kaldı.

⚠️ Ayrım önemli: judge HER boyutu HER cevapta puanlar. Eşiksiz boyut
«ölçülmüyor» değil, «**başarısızlık sayılmıyor**» demektir — gerileme sayıda
görünür, kapı ateşlemez (K80 hükmü `golden-dev`den aynen alınır).

Girdi : src/schemas.py (JudgeResult) · evals/golden-*.jsonl
Çıktı : reports/analiz/2026-09-16-golden-rubrik-kapsama.md
Kullanım: uv run python scripts/analiz/2026-09-16-golden-rubrik-kapsama.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-golden-rubrik-kapsama.md"

from schemas import JudgeResult  # noqa: E402
import filter as f  # noqa: E402

# `golden-dev`den AYNEN alınır — iki yerde iki liste olursa hüküm de ikiye böl.
DISLANAN = ("gerekce", "judge_model", "prompt_version",
            "en_belirsiz_cumle", "cevapsiz_soru_metni", "duz_turkce")
BUTUNSEL = {
    "anlasilirlik", "anlasilirlik_holistik", "dogallik", "dogallik_holistik",
    "mi_uyumu_holistik", "dil_butunlugu", "kisalik_dogallik",
    "belirsiz_gonderge", "devrik_eksiltili", "kurulmamis_mecaz", "siz_kaymasi",
    "soyut_adlastirma", "terapi_jargonu", "ust_uste_yan_cumle", "tuzak_ihlali",
}


def tip(ad: str) -> str:
    t = str(JudgeResult.model_fields[ad].annotation)
    return "bool" if "bool" in t else ("sayı" if ("int" in t or "float" in t) else "metin")


def main() -> None:
    rubrik = {a for a in JudgeResult.model_fields if a not in DISLANAN}
    esikli: collections.Counter = collections.Counter()
    oge, dosyalar = 0, []
    for p in sorted((KOK / "evals").glob("golden*.jsonl")):
        dosyalar.append((p.name, hashlib.sha256(p.read_bytes()).hexdigest()[:16]))
        for satir in p.open(encoding="utf-8"):
            r = json.loads(satir)
            oge += 1
            # `iddialar` bir LİSTE; rubrik boyutuna eşik koyanlar `tip="judge"`
            # olup `alan` taşır (`golden-dev`deki türetmenin aynısı).
            for i in (r.get("iddialar") or []):
                if i.get("alan"):
                    esikli[i["alan"]] += 1

    kapsanmayan = sorted(rubrik - set(esikli))
    butunsel = sorted(set(kapsanmayan) & BUTUNSEL)
    acik = sorted(set(kapsanmayan) - BUTUNSEL)
    acik_tip = collections.Counter(tip(a) for a in acik)

    L = ["# Golden eval seti rubriğin ne kadarını **sınıyor**", "",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
         f"**Rubrik:** `{f.JUDGE_PROMPT_VERSION}` · `src/schemas.py` SHA256 "
         f"`{hashlib.sha256((KOK / 'src/schemas.py').read_bytes()).hexdigest()[:16]}`  ",
         "**Golden:** " + " · ".join(f"`{a}` `{s}`" for a, s in dosyalar) or "_yok_",
         "", "---", "",
         "## Nasıl bulundu", "",
         "`2026-09-14-golden-dev.py` kendi raporunu yeniden üretemedi (K126 denetimi).",
         "Sebep tarih değil **girdi**: betik canlı rubriği okuyor. 09-14'te rubrikte",
         "**37** boyut vardı ve o günün raporundaki *«öğe düzeyinde kapanmamış boyut",
         f"kalmadı»* cümlesi **doğruydu**. Bugün rubrik `{f.JUDGE_PROMPT_VERSION}`,",
         f"**{len(rubrik)}** boyut. Golden seti (K31 mühürlü) yerinde kaldı.", "",
         "⚠️ Eşiksiz boyut *«ölçülmüyor»* demek DEĞİL: judge her boyutu her cevapta",
         "puanlar. Demek ki **gerileme sayıda görünür, başarısızlık sayılmaz**.", "",
         "## Ölçüm", "",
         "| | |", "|---|---:|",
         f"| Golden öğe | {oge} |",
         f"| Rubrik boyutu (hüküm dışı alanlar hariç) | **{len(rubrik)}** |",
         f"| Eşik konulmuş boyut | **{len(esikli)}** |",
         f"| Eşiksiz — bütünsel/üslup (öğe eşiği anlamsız) | {len(butunsel)} |",
         f"| Eşiksiz — girdi tasarımı gerektiren | {len(acik)} |",
         f"| ⛔ bunlardan **başarısızlık taşıyabilecek** (bool) | "
         f"**{acik_tip['bool']}** |",
         f"| ⚠️ bunlardan kanıt/kategori alanı (metin, eşik anlamsız) | "
         f"{acik_tip['metin']} |", "",
         f"➡️ ⭐ **Keskin sayı {acik_tip['bool']}, 38 değil.** 38'in "
         f"{acik_tip['metin']}'i `rol_kaynak_turu`, `teselli_kalip` gibi **kanıt/kategori**",
         "alanı: bunlara *«false olmalı»* denemez, eşik kavramı uymuyor. Geriye kalan",
         f"**{acik_tip['bool']} bool bayrağı** ise gerçek kusur bayrağı — golden bugün o",
         "kusurları **yakalayabilecek tek bir öğe bile taşımıyor**.", "",
         "### ⛔ Hiç sondalanmayan boyutlar", ""]
    if acik:
        L += ["| Boyut | tip |", "|---|---|"]
        L += [f"| `{a}` | {tip(a)} |" for a in acik]
    else:
        L += ["_Yok._"]
    L += ["", "### Bütünsel/üslup — korpus düzeyi eşik gerekir", "",
          ("`" + "` · `".join(butunsel) + "`") if butunsel else "_Yok._", "",
          "## ⭐ Karar", "", "| | |", "|---|---|",
          f"| ⛔ Açık | **{acik_tip['bool']}** bool kusur bayrağında golden "
          f"**gerileme yakalayamaz** ({len(acik)} eşiksizin kusur taşıyabileni) |",
          "| ⛔ K31 | mühürlü set DEĞİŞTİRİLEMEZ — kapatma yolu **İKİNCİ bir set** |",
          "| ⚠️ Kaynak | açığın tamamı v8/v9'un kanıta bağlı alanları "
          "(`alinti_*`, `teselli_*`, `rol_*`, `yordam_*`, `kurum_*`) |",
          "| ➡️ Kural 7 | `golden-dev` artık rubrik sürümünü **ilan ediyor**; "
          "rubrik büyüdüğünde bu betik yeniden koşulur |", "",
          "⚠️ **17 de bir üst sınır.** Bool bayraklarının bir kısmı ihlal değil "
          "**kanıt** bayrağı (`teselli_dayanakli`, `ayrinti_konusmada_var`, "
          "`rol_bilgi_baglamdan`, `kurum_adi_kullanicidan`, `etiket_kullanicinin`, "
          "`teselli_dayanak_dogrulandi`): bunlara *«false olmalı»* demek de anlamsız. "
          "Kesin ihlal bayrağı olanlar: `kurum_yordam_ihlali`, `kusur_kullanicida_ima`, "
          "`kullanicinin_kendi_sucu`, `utanc_buyutuyor`, `genelleme_kategori_mi`, "
          "`teselli_kalip`. ➡️ Ayrımı **otomatik yapmadım** — her alanın niyetini "
          "okumak gerekir ve bu klinik bir karardır (Kural 3). Sayı bu yüzden "
          "*«en çok 17, en az 6»* diye raporlanır.", ""]

    RAPOR.write_text("\n".join(L), encoding="utf-8")
    print(f"rubrik {len(rubrik)} · eşikli {len(esikli)} · bütünsel {len(butunsel)} · "
          f"⛔ açık {len(acik)} → {RAPOR.relative_to(KOK)}")


if __name__ == "__main__":
    main()
