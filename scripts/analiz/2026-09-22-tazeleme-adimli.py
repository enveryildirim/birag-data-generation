#!/usr/bin/env python3
"""Aritmetik tazeleme — ADIMLI sürüm. T256'in ölçtüğü hatayı onarır.

⛔⛔ **T256 NE BULDU.** İlk tazeleme kolu (40 yalın sayı cevabı) hipotezi
sınayamadı: `mask_prompt: true` kaybı yalnız CEVAP jetonlarına uyguluyor ve
yalın sayı cevapları ortalama **2,1 jeton** ⇒ küme kayıtların %3,7'siydi ama
gradyanın **%0,034'ü**. ➡️ *Kayıt saymak sinyal saymak değildir.*

⭐⭐⭐ **BU SÜRÜMDE PAY KOŞUDAN ÖNCE ÖLÇÜLÜYOR.** Betik hedef payı
(`HEDEF_PAY`) tutturana kadar kayıt üretir ve **gerçek tokenizer'la sayar**.
Tutturamazsa yazmaz.

⭐ **İki kip birden:**
  · **adımlı** (~%80) — işlemi yazarak çözer; SİNYAL buradan gelir
  · **yalın** (~%20) — *«yalnızca sonucu yaz»* der ve yalın sayı verir;
    BİÇİME UYUM buradan gelir
⛔ İkincisi şart: eval'in bazı ögelerinde `uzunluk_maks` var (fs-001: 120,
fs-025: 150) ⇒ yalnız adımlı öğretilirse model biçim kısıtını ihlal eder.

⛔ **Sıfır uydurma riski:** bütün cevaplar hesaplanır, betik 2 kez doğrular
(üretimde ve yazmadan önce). Hiçbir olgu iddiası yazılmaz.
⛔ **Bulaşma:** `forgetting_smoke`'un 30 ögesiyle çakışma betikte denetlenir.

Çıktı: data/candidates/tazeleme-adimli.jsonl
"""
from __future__ import annotations

import collections
import hashlib
import json
import random
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
CIKTI = KOK / "data/candidates/tazeleme-adimli.jsonl"
TOHUM = 20260922
HEDEF_PAY = 0.05          # kayıp sinyalinin %5'i
YALIN_ORAN = 0.20
SISTEMLER = ["Kısa ve net cevaplar ver.",
             "Sen yardımsever bir yapay zeka asistanısın.",
             "Sorulara doğrudan cevap ver."]


def soru_uret(rng):
    """(soru_govdesi, cevap, adim_metni, bicim) — cevap HESAPLANIR."""
    b = rng.choice(("carp_ekle", "topla_cikar", "yuzde", "bol_ekle",
                    "kat_fark", "toplam_adet", "iki_asamali"))
    if b == "carp_ekle":
        a, c, d = rng.randint(3, 14), rng.randint(3, 14), rng.randint(5, 45)
        g = f"{a} ile {c}'yi çarp, çıkan sonuca {d} ekle."
        s = a * c + d
        adim = f"Önce çarpalım: {a} × {c} = {a*c}. Sonra {d} ekleyelim: {a*c} + {d} = {s}."
    elif b == "topla_cikar":
        a, c, d = rng.randint(20, 95), rng.randint(5, 35), rng.randint(5, 30)
        g = f"{a} sayısına {c} ekle, sonra {d} çıkar."
        s = a + c - d
        adim = f"Önce toplayalım: {a} + {c} = {a+c}. Sonra çıkaralım: {a+c} − {d} = {s}."
    elif b == "yuzde":
        a = rng.choice((80, 120, 160, 180, 200, 240, 300, 360, 400))
        p = rng.choice((10, 15, 20, 25, 50, 75))
        g = f"{a} sayısının %{p}'si kaçtır?"
        s = a * p // 100
        adim = (f"Yüzde hesabı için sayıyı 100'e bölüp oranla çarpıyoruz: "
                f"{a} ÷ 100 = {a/100:g}, sonra {a/100:g} × {p} = {s}.")
    elif b == "bol_ekle":
        c, k = rng.randint(2, 9), rng.randint(4, 22)
        a, d = c * k, rng.randint(3, 35)
        g = f"{a} sayısını {c}'ye böl, çıkan sonuca {d} ekle."
        s = a // c + d
        adim = f"Önce bölelim: {a} ÷ {c} = {a//c}. Sonra {d} ekleyelim: {a//c} + {d} = {s}."
    elif b == "kat_fark":
        a, c = rng.randint(10, 65), rng.randint(2, 7)
        g = f"{a} sayısının {c} katından {a}'yı çıkar."
        s = a * c - a
        adim = f"Önce katını alalım: {a} × {c} = {a*c}. Sonra {a} çıkaralım: {a*c} − {a} = {s}."
    elif b == "toplam_adet":
        a, c, d = rng.randint(20, 85), rng.randint(5, 30), rng.randint(3, 18)
        g = (f"Bir kutuda {a} tane var. {c} tanesi alındı, sonra {d} tane daha kondu. "
             "Kaç tane kaldı?")
        s = a - c + d
        adim = (f"Alınanları çıkaralım: {a} − {c} = {a-c}. Sonra eklenenleri "
                f"katalım: {a-c} + {d} = {s}.")
    else:
        a, c, d = rng.randint(4, 12), rng.randint(3, 11), rng.randint(2, 9)
        g = f"{a} kutunun her birinde {c} tane var. Bunlardan {d} tanesi kırıldı. Kaç tane sağlam kaldı?"
        s = a * c - d
        adim = (f"Önce toplamı bulalım: {a} × {c} = {a*c}. Sonra kırılanları "
                f"çıkaralım: {a*c} − {d} = {s}.")
    return g, s, adim, b


DOGRULA = {
    "carp_ekle": lambda n: n[0]*n[1]+n[2], "topla_cikar": lambda n: n[0]+n[1]-n[2],
    "yuzde": lambda n: n[0]*n[1]//100, "bol_ekle": lambda n: n[0]//n[1]+n[2],
    "kat_fark": lambda n: n[0]*n[1]-n[0], "toplam_adet": lambda n: n[0]-n[1]+n[2],
    "iki_asamali": lambda n: n[0]*n[1]-n[2]}


def main() -> int:
    sys.path.insert(0, str(KOK / "src"))
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(str(KOK / "models/gemma-4-E4B-it-bf16-train"))

    # korpusun cevap jetonu — hedef pay buna göre
    korpus_jeton = 0
    for l in open(KOK / "datasets/v0.0.18/train.jsonl"):
        r = json.loads(l)
        son = [m for m in r["messages"] if m["role"] == "assistant"][-1]
        korpus_jeton += len(tok.encode((son.get("content") or "") +
                                       (son.get("thinking") or ""), add_special_tokens=False))
    hedef_jeton = HEDEF_PAY * korpus_jeton / (1 - HEDEF_PAY)
    print(f"korpus cevap jetonu: {korpus_jeton:,} · %{100*HEDEF_PAY:.0f} için "
          f"gereken: {hedef_jeton:,.0f}")

    eval_metin = {re.sub(r"\s+", " ", m["content"]).strip().lower()
                  for l in open(KOK / "evals/forgetting_smoke.jsonl") if l.strip()
                  for m in json.loads(l).get("messages", []) if m["role"] == "user"}

    rng = random.Random(TOHUM)
    gorulen, kayitlar, jeton = set(), [], 0
    while jeton < hedef_jeton:
        g, s, adim, b = soru_uret(rng)
        yalin = rng.random() < YALIN_ORAN
        soru = g + (" Yalnızca sonucu yaz." if yalin else "")
        cevap = str(s) if yalin else f"{adim} Sonuç: {s}."
        anahtar = re.sub(r"\s+", " ", soru).strip().lower()
        if anahtar in gorulen:
            continue
        if anahtar in eval_metin:
            raise SystemExit(f"⛔ EVAL ÇAKIŞMASI: {soru}")
        gorulen.add(anahtar)
        n = len(tok.encode(cevap, add_special_tokens=False))
        jeton += n
        kid = hashlib.sha256(f"adimli-{anahtar}".encode()).hexdigest()[:24]
        kayitlar.append({
            "id": kid,
            "messages": [{"role": "system", "content": rng.choice(SISTEMLER)},
                         {"role": "user", "content": soru},
                         {"role": "assistant", "content": cevap}],
            "slice": "replay", "scenario": "genel", "addiction_type": "yok",
            "age_group": "yetiskin", "motivation": "ic", "mi_process": "engaging",
            "talk_type": "change_darn", "turn_type": "single",
            "is_crisis": False, "is_negative": False, "has_thinking": False,
            "replay": True, "context": [], "source_ids": [],
            "gen_meta": {"generator": "claude-code", "generator_model": "claude-opus-5",
                         "prompt_version": "tazeleme-adimli.v1", "date": TARIH,
                         "bicim": b, "kip": "yalin" if yalin else "adimli",
                         "tohum_havuzu": "uretilmis", "parti": "tazeleme-adimli"},
            "judge": None})

    # ⭐⭐ İKİNCİ DOĞRULAMA — yazmadan önce her cevabı yeniden hesapla
    yanlis = []
    for k in kayitlar:
        soru = k["messages"][1]["content"]
        c = k["messages"][2]["content"]
        son = int(re.findall(r"-?\d+", c)[-1])
        sayilar = [int(x) for x in re.findall(r"\d+", soru)]
        bek = DOGRULA[k["gen_meta"]["bicim"]](sayilar)
        if bek != son:
            yanlis.append((soru, son, bek))
    if yanlis:
        for s_, c_, b_ in yanlis[:5]:
            print(f"⛔ {s_} → {c_}, beklenen {b_}")
        raise SystemExit(f"⛔ {len(yanlis)} kayıt yanlış — YAZILMADI")

    CIKTI.write_text("".join(json.dumps(k, ensure_ascii=False) + "\n" for k in kayitlar),
                     encoding="utf-8")
    kip = collections.Counter(k["gen_meta"]["kip"] for k in kayitlar)
    pay = 100 * jeton / (korpus_jeton + jeton)
    print(f"⭐ {len(kayitlar)} kayıt · {jeton:,} cevap jetonu · "
          f"ort {jeton/len(kayitlar):.0f}")
    print(f"   kip: {dict(kip)} · biçim: "
          f"{dict(collections.Counter(k['gen_meta']['bicim'] for k in kayitlar))}")
    print(f"   ⭐⭐ KAYIP SİNYALİNDEKİ PAY: %{pay:.2f}  (kayıt payı %"
          f"{100*len(kayitlar)/(1033+len(kayitlar)):.1f})")
    print(f"   doğrulama: {len(kayitlar)}/{len(kayitlar)} DOĞRU · eval çakışması 0")
    print(f"→ {CIKTI.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
