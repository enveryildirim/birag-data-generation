#!/usr/bin/env python3
"""Aritmetik tazeleme (rehearsal) seti — T255'nin nedenselliğini sınar.

⛔⛔ **ÖN KAYIT — öngörüler koşudan ÖNCE yazıldı.**

T255 ölçtü: ince ayar `forgetting_smoke`'ta aritmetik (`fs-025` 0/8,
`fs-013` 4/8) ve olgusal ad (`fs-029` 1/8) ögelerini kaybediyor; korpusta bu
kiplerin **hiçbiri yok** (%0,0 yalın sayı, %0,0 aritmetik, asistan tarafında
özel ad yok). Ama nedensellik kurulmadı — aynı kaybı **LoRA kapsamı** da
üretebilir (K174/K175).

⭐⭐⭐ **AYIRICI TASARIM: yalnız ARİTMETİK tazelenir, OLGUSAL AD TAZELENMEZ.**
Olgusal kip **bilerek dışarıda bırakılıyor** ⇒ üç sonuç ayrılabilir:

| sonuç | anlamı |
|---|---|
| aritmetik düzelir, olgusal düzelmez | ⭐ **kip yokluğu sebep** — tazeleme kipe özgü çalışıyor |
| ikisi de düzelir | tazeleme genel bir onarım yapıyor; kip açıklaması **yetersiz** |
| ikisi de düzelmez | ⛔ sebep korpus değil **LoRA kapsamı** (K174/K175) |

⛔ **Sıfır uydurma riski:** bütün cevaplar Python'da hesaplanır ve betik
kendi çıktısını **doğrular**. Hiçbir olgu iddiası yazılmaz (Kural 3/6).

⚠️ **Bulaşma şerhi, önceden yazılı:** tazeleme seti `forgetting_smoke`'un
aritmetik ögeleriyle **aynı KİPİ** hedefliyor (çok adımlı işlem, yalın sayı
cevabı) ama **hiçbir ögeyi tekrarlamıyor** — sayılar ve ifadeler farklı,
çakışma betikte denetleniyor. ⇒ Kazanç okunurken *«kip tazelemesi işe
yaradı»* denir, *«genel yetenek geri geldi»* DENMEZ.

⛔ Bu set korpusa KALICI eklenmez; ayrı bir deney sürümü (`v0.0.19`) olur.

Çıktı: data/candidates/tazeleme-aritmetik.jsonl
"""
from __future__ import annotations

import hashlib
import json
import random
import re
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
CIKTI = KOK / "data/candidates/tazeleme-aritmetik.jsonl"
TOHUM = 20260922
N = 40

SISTEMLER = ["Kısa ve net cevaplar ver.",
             "Sen yardımsever bir yapay zeka asistanısın.",
             "Sorulara doğrudan cevap ver."]


def uret(rng):
    """Çok adımlı işlem + yalın sayı cevabı. Cevap HESAPLANIR, yazılmaz."""
    bicim = rng.choice(("carp_ekle", "topla_cikar", "yuzde", "bol_ekle",
                        "kat_fark", "toplam_adet"))
    if bicim == "carp_ekle":
        a, b, c = rng.randint(3, 12), rng.randint(3, 12), rng.randint(5, 40)
        s = f"{a} ile {b}'yi çarp, çıkan sonuca {c} ekle. Yalnızca sonucu yaz."
        d = a * b + c
    elif bicim == "topla_cikar":
        a, b, c = rng.randint(20, 90), rng.randint(5, 30), rng.randint(5, 25)
        s = f"{a} sayısına {b} ekle, sonra {c} çıkar. Yalnızca sayıyı yaz."
        d = a + b - c
    elif bicim == "yuzde":
        a = rng.choice((80, 120, 160, 200, 240, 300, 400))
        p = rng.choice((10, 20, 25, 50))
        s = f"{a} sayısının %{p}'si kaçtır? Yalnızca sayıyı yaz."
        d = a * p // 100
    elif bicim == "bol_ekle":
        b, k = rng.randint(2, 9), rng.randint(4, 20)
        a = b * k
        c = rng.randint(3, 30)
        s = f"{a} sayısını {b}'ye böl, çıkan sonuca {c} ekle. Yalnızca sonucu yaz."
        d = a // b + c
    elif bicim == "kat_fark":
        a, b = rng.randint(10, 60), rng.randint(2, 6)
        s = f"{a} sayısının {b} katından {a}'yı çıkar. Yalnızca sonucu yaz."
        d = a * b - a
    else:
        a, b, c = rng.randint(20, 80), rng.randint(5, 25), rng.randint(3, 15)
        s = (f"Bir kutuda {a} tane var. {b} tanesi alındı, sonra {c} tane "
             "daha kondu. Kaç tane kaldı? Yalnızca sayıyı yaz.")
        d = a - b + c
    return s, str(d), bicim


def main() -> int:
    # ⛔ eval ögeleriyle çakışma denetimi
    eval_metin = {
        re.sub(r"\s+", " ", m["content"]).strip().lower()
        for l in open(KOK / "evals/forgetting_smoke.jsonl") if l.strip()
        for m in json.loads(l).get("messages", []) if m["role"] == "user"}

    rng = random.Random(TOHUM)
    gorulen, kayitlar = set(), []
    while len(kayitlar) < N:
        s, d, bicim = uret(rng)
        anahtar = re.sub(r"\s+", " ", s).strip().lower()
        if anahtar in gorulen:
            continue
        if anahtar in eval_metin:
            raise SystemExit(f"⛔ EVAL ÖGESİYLE ÇAKIŞMA: {s}")
        gorulen.add(anahtar)
        kid = hashlib.sha256(f"tazeleme-{anahtar}".encode()).hexdigest()[:24]
        kayitlar.append({
            "id": kid,
            "messages": [
                {"role": "system", "content": rng.choice(SISTEMLER)},
                {"role": "user", "content": s},
                {"role": "assistant", "content": d},
            ],
            "slice": "replay", "scenario": "genel", "addiction_type": "yok",
            "age_group": "yetiskin", "motivation": "ic", "mi_process": "engaging",
            "talk_type": "change_darn", "turn_type": "single",
            "is_crisis": False, "is_negative": False, "has_thinking": False,
            "replay": True, "context": [], "source_ids": [],
            "gen_meta": {"generator": "claude-code", "generator_model": "claude-opus-5",
                         "prompt_version": "tazeleme-aritmetik.v1",
                         "date": TARIH, "bicim": bicim,
                         "tohum_havuzu": "uretilmis", "parti": "tazeleme-aritmetik"},
            "judge": None,
        })

    # ⭐ KENDİ ÇIKTISINI DOĞRULA — cevap gerçekten doğru mu
    yanlis = []
    for k in kayitlar:
        soru = k["messages"][1]["content"]
        cevap = int(k["messages"][2]["content"])
        sayilar = [int(x) for x in re.findall(r"\d+", soru)]
        b = k["gen_meta"]["bicim"]
        bek = {"carp_ekle": lambda n: n[0]*n[1]+n[2],
               "topla_cikar": lambda n: n[0]+n[1]-n[2],
               "yuzde": lambda n: n[0]*n[1]//100,
               "bol_ekle": lambda n: n[0]//n[1]+n[2],
               "kat_fark": lambda n: n[0]*n[1]-n[0],
               "toplam_adet": lambda n: n[0]-n[1]+n[2]}[b](sayilar)
        if bek != cevap:
            yanlis.append((soru, cevap, bek))
    if yanlis:
        for s, c, b in yanlis[:5]:
            print(f"⛔ {s} → yazılan {c}, beklenen {b}")
        raise SystemExit(f"⛔ {len(yanlis)} kayıtta cevap yanlış — yazılmadı")

    CIKTI.write_text("".join(json.dumps(k, ensure_ascii=False) + "\n" for k in kayitlar),
                     encoding="utf-8")
    import collections
    print(f"⭐ {len(kayitlar)} tazeleme kaydı · biçim dağılımı: "
          f"{dict(collections.Counter(k['gen_meta']['bicim'] for k in kayitlar))}")
    print(f"   cevap doğrulaması: {len(kayitlar)}/{len(kayitlar)} DOĞRU")
    print(f"   eval çakışması: 0")
    print(f"→ {CIKTI.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
