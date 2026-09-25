"""Prompt dili ablasyonunun raporu. Ham çıktı: reports/analiz/prompt-dili-ablasyonu/.
Bkz. `2026-09-12-prompt-dili-ablasyonu.py` (üretim) ve Kural 7.
"""
from __future__ import annotations
import hashlib
import json
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.resolve()
HAM = ROOT / "reports" / "analiz" / "prompt-dili-ablasyonu" / "generations.jsonl"
OUT = ROOT / "reports" / "analiz" / "2026-09-12-prompt-dili-ablasyonu.md"

TR_KARAKTER = set("ğışçöüĞİŞÇÖÜ")
TR_KELIME = {"bir", "bu", "ve", "için", "ile", "ama", "değil", "kullanıcı", "soru",
             "cevap", "yani", "çünkü", "olarak", "var", "yok", "gibi"}
EN_KELIME = {"the", "a", "and", "to", "of", "is", "user", "response", "this", "that",
             "should", "not", "it", "for", "answer", "process", "thinking"}
SIZ = re.compile(r"\b(siz|sizin|size|sizi|sizde|sizden)\b|nız\b|niz\b|nuz\b|nüz\b", re.I)
SEN = re.compile(r"\b(sen|senin|sana|seni|sende|senden)\b|(?:yor|ar|er|ir|ır|ur|ür|acak|ecek|dı|di)sun\b", re.I)
DIMS = ["duygusal_tepki", "yorumlama", "kesif", "mi_uyumu",
        "grounding", "kisalik_dogallik", "dil_butunlugu"]
OLCEK = {"duygusal_tepki": 2, "yorumlama": 2, "kesif": 2, "mi_uyumu": 5,
         "grounding": 5, "kisalik_dogallik": 5, "dil_butunlugu": 5}
ETIKET = {"tr_sys": "A · TR system", "en_sys": "B · EN system + \"answer in Turkish\"",
          "tr_sys_dusun": "C · TR system + \"Türkçe düşün\""}


def dil(metin: str) -> str:
    kelimeler = re.findall(r"[A-Za-zğışçöüĞİŞÇÖÜıİ]+", metin.lower())
    if not kelimeler:
        return "bos"
    tr = sum(w in TR_KELIME for w in kelimeler) + sum(c in TR_KARAKTER for c in metin) / 5
    en = sum(w in EN_KELIME for w in kelimeler)
    return "tr" if tr > en else ("en" if en else "belirsiz")


def main():
    rows = [json.loads(l) for l in open(HAM) if l.strip()]
    varyantlar = list(dict.fromkeys(r["varyant"] for r in rows))
    n = len({r["seed_id"] for r in rows})

    L = [
        "# Prompt dili ablasyonu — system prompt ve thinking İngilizce olmalı mı?",
        "",
        f"**Girdi:** `{HAM.relative_to(ROOT)}` (sha256:{hashlib.sha256(HAM.read_bytes()).hexdigest()[:16]}) · "
        "**Betikler:** `scripts/analiz/2026-09-12-prompt-dili-ablasyonu.py` (üretim) + "
        "`…-prompt-dili-raporu.py` (rapor) · **Tarih:** 2026-09-12",
        "",
        f"**{n} tohum** (4 kampanyadan dengeli, tek turlu), 3 varyant, **birebir aynı tohumlar**, "
        "`gemma-4-E4B-it-bf16`, **adapter yok** (saf prompt etkisi), temp=0, max_tokens=2048.",
        "",
        "Soru (kullanıcı önerisi, Oturum 16): *system prompt ve thinking İngilizce olsun, içine "
        "\"Türkçe cevap ver\" yazalım — model komutları İngilizce daha iyi anlar.*",
        "",
        "| Varyant | system prompt | ek talimat |",
        "|---|---|---|",
        "| **A** `tr_sys` | Türkçe (mevcut) | — |",
        "| **B** `en_sys` | İngilizce (birebir çeviri) | *\"Always respond in Turkish\"* |",
        "| **C** `tr_sys_dusun` | Türkçe | *\"İç muhakemeni de Türkçe kurarsın\"* |",
        "",
        "## 1. thinking dili — prompt'la çevrilebiliyor mu?",
        "",
        "| Varyant | thinking TR | thinking EN | completion TR | completion EN |",
        "|---|---|---|---|---|",
    ]
    for v in varyantlar:
        g = [r for r in rows if r["varyant"] == v]
        td = [dil(r["thinking"]) for r in g]
        cd = [dil(r["completion"]) for r in g]
        L.append(f"| {ETIKET[v]} | **{td.count('tr')}/{len(g)}** | {td.count('en')}/{len(g)} | "
                 f"**{cd.count('tr')}/{len(g)}** | {cd.count('en')}/{len(g)} |")

    L += ["", "## 2. Token bütçesi ve gecikme", "",
          "| Varyant | thinking (token) | completion (token) | oran | cevap süresi | kullanıcıya giden pay |",
          "|---|---|---|---|---|---|"]
    for v in varyantlar:
        g = [r for r in rows if r["varyant"] == v]
        mt = statistics.median(r["thinking_token"] for r in g)
        mc = statistics.median(r["completion_token"] for r in g)
        sn = statistics.mean(r["sure_sn"] for r in g)
        pay = statistics.mean(r["completion_token"] / max(1, r["uretim_token"]) for r in g)
        L.append(f"| {ETIKET[v]} | {mt:.0f} | {mc:.0f} | **{mt / mc:.0f}x** | "
                 f"**{sn:.1f} sn** | %{100 * pay:.0f} |")

    L += ["", "## 3. Deterministik kapılar (`checks.py`)", "",
          "| Varyant | geçen | soru > 1 | thinking uzunluk | yasak ifade |", "|---|---|---|---|---|"]
    for v in varyantlar:
        g = [r for r in rows if r["varyant"] == v]
        L.append(f"| {ETIKET[v]} | **{sum(r['_checks']['passed'] for r in g)}/{len(g)}** | "
                 f"{sum(not r['_checks']['question_count_ok'] for r in g)} | "
                 f"{sum(not r['_checks']['length_ok'] for r in g)} | "
                 f"{sum(bool(r['_checks']['forbidden_hits']) for r in g)} |")

    L += ["", "## 4. Judge rubriği (`agy:gemini-3.8-flash-high`)", "",
          "| Boyut | Ölçek | " + " | ".join(ETIKET[v] for v in varyantlar) + " |",
          "|---|---|" + "---|" * len(varyantlar)]
    ort = {v: {} for v in varyantlar}
    for d in DIMS:
        satir = [f"| {d} | 0-{OLCEK[d]} "]
        for v in varyantlar:
            g = [r for r in rows if r["varyant"] == v and r.get("judge")]
            m = statistics.mean(r["judge"][d] for r in g) if g else float("nan")
            ort[v][d] = m
            satir.append(f"| {m:.2f} ")
        L.append("".join(satir) + "|")

    L += ["", "**Normalize genel ortalama (0-1):**", ""]
    genel = {}
    for v in varyantlar:
        genel[v] = statistics.mean(ort[v][d] / OLCEK[d] for d in DIMS)
        L.append(f"- {ETIKET[v]}: **{genel[v]:.3f}**")
    taban = genel[varyantlar[0]]
    L += ["", "**A'ya göre fark:**", ""]
    for v in varyantlar[1:]:
        L.append(f"- {ETIKET[v]}: {genel[v] - taban:+.3f} ({100 * (genel[v] - taban) / taban:+.1f}%)")

    L += ["", "## 5. Hitap register'ı (`sen` / `siz`)", "",
          "Veri setimiz ve `docs/turkce-ifade-bankasi.md` **`sen`** register'ında. System prompt",
          "bunu açıkça söylemiyor — Türkçe metnin kendisi taşıyor.", "",
          "| Varyant | `siz`e kayan cevap |", "|---|---|"]
    for v in varyantlar:
        g = [r for r in rows if r["varyant"] == v]
        kayan = sum(1 for r in g
                    if len(SIZ.findall(r["completion"])) > len(SEN.findall(r["completion"])))
        L.append(f"| {ETIKET[v]} | **{kayan}/{len(g)}** |")

    L += ["", "## 6. Sert kapılar", "",
          "| Varyant | klinik güvenlik ihlali | rol sınırı ihlali | tuzak ihlali (toplam) |",
          "|---|---|---|---|"]
    for v in varyantlar:
        g = [r for r in rows if r["varyant"] == v and r.get("judge")]
        L.append(f"| {ETIKET[v]} | {sum(r['judge']['klinik_guvenlik_ihlali'] for r in g)} | "
                 f"{sum(r['judge']['rol_siniri_ihlali'] for r in g)} | "
                 f"{sum(len(r['judge']['tuzak_ihlali']) for r in g)} |")

    tuzaklar = {}
    for r in rows:
        if r.get("judge"):
            for t in r["judge"]["tuzak_ihlali"]:
                tuzaklar.setdefault(t, {}).setdefault(r["varyant"], 0)
                tuzaklar[t][r["varyant"]] += 1
    ihlal = [r for r in rows if r.get("judge") and r["judge"]["klinik_guvenlik_ihlali"]]
    if ihlal:
        L += ["", "### ⚠️ Klinik güvenlik ihlali — aynı tohum, üç varyant", ""]
        for r in ihlal:
            L += [f"**Varyant:** {ETIKET[r['varyant']]} · tohum `{r['seed_id'][:8]}` "
                  f"({r['campaign']})", "",
                  f"> **Kullanıcı:** {r['user_message']}", "",
                  f"**Judge gerekçesi:** {r['judge']['gerekce']}", ""]
            for o in rows:
                if o["seed_id"] == r["seed_id"]:
                    L += [f"**{ETIKET[o['varyant']]}:**", "", "```",
                          o["completion"].strip(), "```", ""]

    if tuzaklar:
        L += ["", "**Tuzak türüne göre:**", "",
              "| Tuzak | " + " | ".join(ETIKET[v] for v in varyantlar) + " |",
              "|---|" + "---|" * len(varyantlar)]
        for t, d in sorted(tuzaklar.items()):
            L.append(f"| {t} | " + " | ".join(str(d.get(v, 0)) for v in varyantlar) + " |")

    OUT.write_text("\n".join(L) + "\n")
    print(f"yazıldı: {OUT}\n")
    print("\n".join(L[14:]))


if __name__ == "__main__":
    main()
