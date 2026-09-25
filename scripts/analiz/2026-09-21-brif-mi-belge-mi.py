#!/usr/bin/env python3
"""Alt ajan brifi KENDİ KENDİNE YETERLİ mi olmalı, yoksa belgelere mi
yönlendirmeli — iki blok taslağının karşılaştırması (T234).

⛔⛔ **Doğal bir deney, tasarlanmış değil.** `v6-parti8`'in üç blok taslağı
AYNI brifle, aynı modelle (Sonnet), aynı gün dağıtıldı. Blok 3'ün ajanı
kendiliğinden proje belgelerini de okudu (`prompts/uretim-v5.md` §7/§5a″,
`docs/davranis-kartlari.md`, `AGENTS.md`, parti7 blok betikleri) ve
kendi doğrulama betiğini yazdı; blok 1'in ajanı yalnız brifle çalıştı.

⛔⛔⛔ **KARIŞTIRICILAR AÇIK ve sonucu tek başına açıklayabilirler:**
  · blok 3 ajanı **2780 sn** koştu, blok 1 ajanı **1903 sn** ⇒ daha uzun
    çalışmış olmak tek başına daha az kusur verebilir;
  · iki bloğun İÇERİĞİ farklı (blok 3'te 27 üretim notu, blok 1'de 7) ⇒
    talimat yoğunluğu farklı;
  · n=2 ve bu bir örneklem değil, iki koşu.
⇒ Aşağıdaki fark bir ETKİ ÖLÇÜSÜ DEĞİL, bir işarettir. *«Belge okumak
kusuru azaltır»* denemez; *«yalnız brifle çalışan koşuda kusur belirgin
biçimde fazlaydı»* denir.

Çıktı: reports/analiz/2026-09-21-brif-mi-belge-mi.md
"""
from __future__ import annotations

import json
import re
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
# Taslaklar depoda: data/taslaklar/ (bkz. oradaki OKU.md). Oturum
# scratchpad'i kaybolur ve bu karşılaştırma onsuz yeniden koşturulamaz.
SP = KOK / "data/taslaklar"
RAPOR = KOK / f"reports/analiz/{TARIH}-brif-mi-belge-mi.md"

# ⛔⛔ İLK HÂLİ SÖZCÜK SINIRI YOKTU ve `slim` **«teslim»** içinde eşleşti
#    (`b3 #111`, «teslim baskısı»). Yanlış pozitif, blok 3'ün marka sayısını
#    1 gösteriyordu; doğrusu 0. ➡️ *Bu oturumda üçüncü kez: sözlükle kurulan
#    bir ölçü, ölçtüğünü değil yazımını yakalıyor (T227, T228).*
MARKA = re.compile(r"\b(tekel\s*2000|samsun|marlboro|lark|slim|parliament|"
                   r"winston|xanax|rivotril|stilnox|ritalin|cipram|prozac|"
                   r"efexor|sertralin|sibutramin)\b", re.I)
TEKLIF = re.compile(r"paylaşabilirim|destek hattı|yardım bölümü|uygulamanın|"
                    r"kısa bilgi", re.I)
ICSEL = re.compile(r"bu sohbet|uygulama|profil bilgi|görüşme kayıtları|"
                   r"bu görüşme", re.I)
KOSU = {"b1": ("yalnız brif", 1903, 7, 62),
        "b2": ("belirtilmedi", 3594, 23, 15),
        "b3": ("brif + proje belgeleri", 2780, 27, 31)}


def _bant(m: str) -> str:
    n = len(re.sub(r"<context.*?</context>|<CTX>", " ", m, flags=re.S).split())
    return "kisa" if n <= 8 else "orta" if n <= 25 else "uzun"


def main() -> int:
    plan = {json.loads(l)["sira"]: json.loads(l)
            for l in (KOK / "data/plan/v6-parti8.jsonl").read_text(
                encoding="utf-8").splitlines() if l.strip()}
    olcum = {}
    for blok in KOSU:
        # ⛔ blok1'in KARŞILAŞTIRILAN taslağı v1'dir (aykırı koşu); düzeltilmiş
        #    brifle yeniden taslaklandığı için dosya adı korunarak ayrıldı.
        _ad = "taslak-p8-b1.v1-aykiri.json" if blok == "b1" else f"taslak-p8-{blok}.json"
        d = json.loads((SP / _ad).read_text(encoding="utf-8"))
        ctx = [o for o in d if o.get("baglam")]
        bant = [o["sira"] for o in d
                if (i := next((t[1] for t in o.get("turns", []) if t[0] == "user"), ""))
                and _bant(i) != plan[o["sira"]]["bicim"]]
        soru = [o["sira"] for o in d
                if o["son"].count("?") !=
                (1 if plan[o["sira"]]["turn_ending"] == "acik_uclu_soru" else 0)]
        olcum[blok] = {
            "kayit": len(d), "baglamli": len(ctx),
            "bant": bant,
            "soru": soru,
            "marka": [o["sira"] for o in d if MARKA.search(o["son"])],
            "teklif": [o["sira"] for o in d if TEKLIF.search(o["son"])],
            "icsel": [o["sira"] for o in ctx if ICSEL.search(o["baglam"]["metin"])],
        }

    sat = ["# Brif kendi kendine yeterli mi olmalı — iki taslağın karşılaştırması", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           "**Girdi:** `v6-parti8` blok1 ve blok3 taslakları (39'ar kayıt)  ", "",
           "| | blok 1 | blok 2 | blok 3 |", "|---|---:|---:|---:|",
           f"| ne okudu | {KOSU['b1'][0]} | {KOSU['b2'][0]} | {KOSU['b3'][0]} |",
           f"| koşu süresi (sn) | {KOSU['b1'][1]} | {KOSU['b2'][1]} | {KOSU['b3'][1]} |",
           f"| araç çağrısı | {KOSU['b1'][3]} | {KOSU['b2'][3]} | {KOSU['b3'][3]} |",
           f"| bloktaki üretim notu | {KOSU['b1'][2]} | {KOSU['b2'][2]} | {KOSU['b3'][2]} |",
           f"| kayıt | {olcum['b1']['kayit']} | {olcum['b2']['kayit']} | "
           f"{olcum['b3']['kayit']} |", ""]
    sat += ["| kusur sınıfı | blok 1 | blok 2 | blok 3 |", "|---|---:|---:|---:|"]
    for ad, k in (("bant ihlali", "bant"), ("soru sayısı", "soru"),
                  ("⛔ marka/ilaç adı", "marka"),
                  ("⛔⛔ uydurulmuş hizmet", "teklif"),
                  ("⛔⛔ sohbeti anlatan pasaj", "icsel")):
        sat.append(f"| {ad} | {len(olcum['b1'][k])} | {len(olcum['b2'][k])} | "
                   f"{len(olcum['b3'][k])} |")
    _t = lambda b: sum(len(olcum[b][k])
                       for k in ("bant", "soru", "marka", "teklif", "icsel"))
    t1, t2, t3 = _t("b1"), _t("b2"), _t("b3")
    sat += ["", f"| **toplam kusur** | **{t1}** | **{t2}** | **{t3}** |", "",
            "## ⛔⛔⛔ İLK OKUMAM YANLIŞTI VE BLOK 2 ONU ÇÜRÜTTÜ", "",
            f"Blok 3'ün temizliğini *«proje belgelerini okudu»* diye "
            f"açıkladım. Blok 2 geldiğinde iddia düştü: blok 2 de **{t2}** "
            "kusur verdi ve belge okuduğuna dair bir işaret yok — üstelik "
            f"EN AZ araç çağrısını o yaptı ({KOSU['b2'][3]}), en çoğunu ise "
            f"en kusurlu koşu yaptı ({KOSU['b1'][3]}).", "",
            f"➡️ **Doğru okuma:** üç koşudan biri {t1} kusur verdi, ikisi "
            f"{t2} ve {t3}. Blok 1 bir AYKIRI KOŞU; blok 3 özel değil. "
            "*«Belge okumak»* ile kusur arasında bu üç koşuda bir ilişki "
            "görünmüyor.", "",
            "⭐ **Brif değişikliği yine de duruyor ve gerekçesi ayrı:** §7'nin "
            "iki kuralı (pasajın dış kaynaklı olması, olmayan hizmetin var "
            "sayılmaması) brifte GERÇEKTEN yoktu. Bu, ölçülen farktan "
            "bağımsız bir eksiklikti ve kapatıldı. Değişiklik bir önlem, "
            "ölçüm sonucu değil.", "",
            "➡️⭐⭐ *Bir açıklama, açıkladığı farkın kendisi sistematik "
            "olmadan kurulamaz; üç koşunun ikisi görülmeden kurulan mekanizma, "
            "aykırı bir koşuyu yasa sanmaktır.*", "",
            "## ⛔ Bu karşılaştırmanın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **n=3 ve bu bir deney değil** | koşular tasarlanmadı, "
            "gözlendi |",
            "| ⛔⛔ **Blok 1'in neden aykırı olduğu BİLİNMİYOR** | ilk denemesi "
            "Opus'ta güvenlik sınıflandırıcısına takılıp yeniden başlatılmıştı; "
            "bunun etkisi olup olmadığı ölçülmedi |",
            "| ⛔ **Kusur sayımı desenle yapıldı** | T227/T228: sözlükler iki "
            "yönde birden yanlış olabiliyor |",
            "| ⚠️ **Kusur ≠ kalite** | sayılan şey mekanik ihlal; terapötik "
            "kaliteyi judge ölçer ve bu taslaklar yargılanmadı |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
