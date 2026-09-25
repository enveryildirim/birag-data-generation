#!/usr/bin/env python3
"""`anaforik_demir` muafiyetinin 13 bağışı elle okundu — ve bir düzeltme çürütüldü.

⛔ T141'in son açık kalemi: zaman kapısının `anaforik_demir` muafiyeti 13 kez
ateşliyordu ve yalnız 6'sı okunmuştu. Kalan 7 okundu ⇒ **13/13 tamam**.

⭐ **Sonuç: 12 yerinde, 1 kusurlu.** `v5-parti4 #3`te cevap *«İkisi de aynı hafta
içinde»* diyor ama kullanıcı hiçbir hafta çıpası koymamış — *«bir hafta içmesem
mi diye düşünmüştüm»* bir **plan süresidir**, zaman çıpası değil. Muafiyet
*«hafta»* sözcüğü kaynakta geçtiği için ateşledi.

⛔⛔ **Ve önerdiğim düzeltme ÖLÇÜLDÜ, ÇÜRÜDÜ, UYGULANMADI.** Kapı *«bir hekimin»*i
belirsiz sayıp atıf saymıyor; aynı ayrımı zamana taşımayı önerdim: *«bir hafta»*
çıpa sayılmasın. Ölçüm 8 vuruşu, tekilleştirince **2 kaydı** etkiliyordu:
  · `v5-parti4 #3` — ⭐ elle okunmuş kusur, doğru yakalanıyor
  · `v3-parti1 #9` — ⛔ **YANLIŞ POZİTİF**: *«bir hafta boyunca instagramı sildim
    gayet iyi oldum»* — burada *«bir hafta»* GERÇEKTEN YAŞANMIŞ bir haftadır ve
    cevabın *«o hafta iyi geçti»*si doğru bir geri göndermedir.

➡️⭐⭐⭐ *Ayrım BELİRSİZLİKTE değil, GERÇEKLEŞMİŞLİKTE: «bir hafta boyunca sildim»
olmuş bir haftadır (çıpalanabilir), «bir hafta içmesem mi diye düşünmüştüm»
düşünülmüş bir haftadır (çıpalanamaz). Bu bir kip ayrımıdır ve anahtar kelimeyle
yakalanmaz — rol tarafında işe yarayan «belirsiz artikel» sezgisi zamana
taşınamıyor.* ⇒ Kural 1 doğru, 1 yanlış pozitif verdi ⇒ **benimsenmedi**.

⛔ Kusurlu kayıt `v5-parti4 #3` düzeltilmedi: `datasets/` IMMUTABLE ve bu, bir
sonraki derlemeye eklenecek kalem.

Girdi : data/candidates/v*.jsonl
Çıktı : reports/analiz/2026-09-18-anaforik-demir-elle-okuma.md
Kullanım: uv run python scripts/analiz/2026-09-18-anaforik-demir-elle-okuma.py
"""
from __future__ import annotations

import importlib.util as iu
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-anaforik-demir-elle-okuma.md"

_s = iu.spec_from_file_location("z", KOK / "scripts/analiz/2026-09-17-zaman-kaynak-kapisi.py")
Z = iu.module_from_spec(_s); _s.loader.exec_module(Z)

# (parti, sıra, öge, yerinde mi, kullanıcının çıpası / gerekçe)
KARAR = [
    ("v4-parti2.v2", 33, "o hafta", True, "*«Bu hafta yarıya indirdim»*"),
    ("v4-parti2.v2", 41, "aynı gün", True, "*«Bu sabah kızıma astım tanısı kondu»*"),
    ("v4-parti2.v2", 56, "aynı gece", True, "*«Gece nöbetindeyim»*"),
    ("v5-parti3", 32, "aynı hafta", True, "*«bu hafta sabahları öksürüyorum … parmak ucum da sararmış»*"),
    ("v5-parti3", 43, "aynı sabah", True, "*«Sabah torunu okula götüremedim … İlaç zamanım vardı»*"),
    ("v5-parti4", 3, "aynı hafta", False,
     "⛔ **kusur** — *«bir hafta içmesem mi diye DÜŞÜNMÜŞTÜM»* bir plan süresi; "
     "kullanıcı hiçbir hafta çıpası koymamış"),
    ("v5-parti4", 13, "aynı gün", True, "*«Bugün dayanamayıp bir tane içtim»*"),
    ("v5-parti4", 32, "aynı akşam", True, "*«bu akşam yine çocukları yatırdım … bi an durdum»*"),
    ("v5-parti5", 7, "o akşam", True, "kullanıcının turunda *«akşam»* demiri var"),
    ("v5-parti6", 28, "aynı gün", True, "*«dördüncü gün oldu sigarayı bıraktığımdan beri»*"),
    ("v5-parti6", 30, "aynı gün", True, "*«Bugün eve dönerken … Beşinci gündeyim»*"),
    ("v5-parti6", 59, "aynı sabah", True, "*«Sabah duraktayım … Az önce komşunun çocuğu geçti»*"),
    ("v5-parti7", 46, "aynı hafta", True, "*«geçen hafta yine bir maç tutturdum»*"),
]


def main() -> int:
    yerinde = sum(1 for *_, ok, _ in KARAR if ok)
    kusur = [k for k in KARAR if not k[3]]
    sat = ["# `anaforik_demir` — 13 bağışın hepsi elle okundu", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}", "",
           "⛔ T141'in son açık kalemi: muafiyet 13 kez ateşliyordu, yalnız 6'sı okunmuştu.", "",
           f"| | |", "|---|---:|", f"| okunan bağış | **{len(KARAR)}** |",
           f"| ⭐ yerinde | **{yerinde}** |", f"| ⛔ kusurlu | **{len(kusur)}** |", "",
           "| kayıt | öge | karar | kullanıcının çıpası |", "|---|---|---|---|"]
    for parti, no, oge, ok, ger in KARAR:
        sat.append(f"| `{parti} #{no}` | *«{oge}»* | {'⭐ yerinde' if ok else '⛔ **kusur**'} "
                   f"| {ger} |")
    sat += ["", "## ⛔⛔ Önerdiğim düzeltme ölçüldü, çürüdü, UYGULANMADI", "",
            "Kapı *«bir hekimin»*i belirsiz sayıp atıf saymıyor. Aynı ayrımı zamana taşımayı",
            "önerdim: *«bir hafta»* çıpa sayılmasın. Ölçüm **8 vuruşu**, tekilleştirince",
            "**2 kaydı** etkiliyordu:", "",
            "| kayıt | kuralın hükmü | elle okuma |", "|---|---|---|",
            "| `v5-parti4 #3` | bulgu | ⭐ **doğru** — plan süresi, çıpa değil |",
            "| `v3-parti1 #9` | bulgu | ⛔ **YANLIŞ POZİTİF** — *«bir hafta boyunca instagramı "
            "sildim gayet iyi oldum»*; burada *«bir hafta»* gerçekten yaşanmış bir haftadır ve "
            "cevabın *«o hafta iyi geçti»*si doğru bir geri göndermedir |", "",
            "➡️⭐⭐⭐ *Ayrım **belirsizlikte** değil, **gerçekleşmişlikte**: «bir hafta boyunca",
            "sildim» OLMUŞ bir haftadır (çıpalanabilir), «bir hafta içmesem mi diye düşünmüştüm»",
            "DÜŞÜNÜLMÜŞ bir haftadır (çıpalanamaz). Bu bir **kip** ayrımıdır ve anahtar kelimeyle",
            "yakalanmaz — rol tarafında işe yarayan «belirsiz artikel» sezgisi zamana",
            "taşınamıyor.* ⇒ 1 doğru, 1 yanlış pozitif ⇒ **kural benimsenmedi.**", "",
            "⭐ Muafiyetin geri kalanı sağlam: 80 vuruş kuralın etkilemediği yerde ve 12/13",
            "bağış elle doğrulandı.", "",
            "## ⛔ Bu okumanın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **Kusurlu kayıt DÜZELTİLMEDİ** | `v5-parti4 #3`in *«İkisi de aynı hafta "
            "içinde»* cümlesi dayanaksız; `datasets/` IMMUTABLE ⇒ bir sonraki derlemeye kalem |",
            "| ⛔ **Kip ayrımı için kapı yok** | gerçekleşmiş ↔ düşünülmüş zaman ayrımını yakalayan "
            "bir sezgi yazılmadı; muafiyet bugünkü hâliyle bu sınıfta kör kalıyor |",
            "| ⚠️ **Kararlar elle** (K30) | ölçüt yazılı — cevap *«aynı X»* diyorsa kullanıcının "
            "o X'i bir ÇIPA olarak anmış olması gerekir — ama hüküm bana ait |",
            "| ⚠️ 13 bağış küçük bir küme | oran (1/13) bir eğilim değil |", ""]
    (KOK / f"reports/analiz/{TARIH}-anaforik-demir-elle-okuma.json").write_text(
        json.dumps({"tarih": TARIH, "bagis": len(KARAR), "yerinde": yerinde,
                    "kusur": [{"parti": k[0], "sira": k[1], "oge": k[2]} for k in kusur],
                    "kural_benimsendi": False}, ensure_ascii=False, indent=2), encoding="utf-8")
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[4:]))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
