#!/usr/bin/env python3
"""Korpus düzeyi hedef raporu — `prompts/uretim-v3.md` §9a.

`checks.py` kayıt düzeyinde çalışır. v3'ün yeni hedefleri (§3b konuşma durumu,
§5a tur kapanışı, §5c MI süreci, §8 is_negative, §2 system prompt varyantı)
korpus düzeyindedir; tek kayda bakarak tutup tutmadıkları görülemez.

Bu betik bir aday dosyasını v3 hedeflerine karşı ölçer ve beyan (gen_meta) ile
metnin çelişip çelişmediğini denetler.

Kullanım:
  uv run python scripts/analiz/2026-09-14-korpus-hedef-raporu.py \
      data/candidates/expert-70.jsonl reports/analiz/2026-09-14-korpus-hedef-expert70.md
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import statistics
import sys
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
sys.path.insert(0, str(KOK / "src"))

from checks import count_questions, run_checks  # noqa: E402

# --- v3 hedefleri (oran) -----------------------------------------------------
# Kaynak: prompts/uretim-v3.md. Sayılar oradan birebir alınır, burada türetilmez.
HEDEF_TUR_KAPANISI = {
    "acik_uclu_soru": 0.50, "takdir": 0.15, "ozet": 0.15,
    "yalnizca_yansitma": 0.15, "durur": 0.05,
}
HEDEF_KONUSMA_DURUMU = {
    "tetikleyici_an": 0.35, "suregiden_durum": 0.20, "iyi_giden_paylasim": 0.15,
    "plan_yapma": 0.15, "merak_sorusu": 0.10, "aradan_donus": 0.05,
}
HEDEF_MI = {"engaging": 0.40, "focusing": 0.20, "evoking": 0.25, "planning": 0.15}
HEDEF_SYSVAR = {"canon": 0.775, "paraphrase": 0.225}  # v3 §2: %75-80 / %20-25
HEDEF_IS_NEGATIVE = 0.15                               # v3 §8
HEDEF_OZERKLIK = 0.20                                  # v3 §5a (2026-09-14 eklendi)

# K20 ifade bankası §"Özerklik saygısı" kalıplarından türetilmiş VEKİL desen.
# ⚠️ Kalıbı yakalar, anlamı değil (K40). Ölçüm alt sınırdır: kalıp dışı kurulmuş
# özerklik cümlesini kaçırır.
OZERKLIK = re.compile(
    r"senin kararın|sen(in)? bilirsin|bana düşmez|karar sende|"
    r"demeyeceğim|söylemeyeceğim|dayatmak istemem|sana kalmış|"
    r"isteyip istemediğin|istersen", re.IGNORECASE)

# GENİŞ desen — kararın sahibini adlandıran kalıplar. Dar desen bunları kaçırıyor:
# "senin kararın" var ama "o karar senin" yok; "karar sende" var ama "sen karar
# vereceksin" yok. v3-parti1'de plan 9 satıra özerklik yazmış, dokuzunda da açık bir
# özerklik cümlesi var, dar desen yalnızca 4'ünü görüyor (%10 yerine %22.5).
#
# ⚠️ Bu desen v3-parti1 OKUNDUKTAN SONRA yazıldı; o korpus için kör bir ölçüm değil.
# Körlük sınaması expert-70 üzerinde yapıldı: dar 2/70 → geniş 4/70 (%3 → %6) ve iki
# yeni eşleşme de gerçek sınır cümlesi. Yani genişletme v2'yi hedef bandına taşımıyor;
# K63'ün bulgusu (üretim özerkliği cümleye dökmüyor) ayakta kalıyor.
OZERKLIK_GENIS = re.compile(
    r"sen karar ver|karar(ı|ın)? senin|o karar senin|kararı sen|"
    r"ben karar ver(miyorum|emem)|karar (bana|benim) (ait değil|değil)|"
    r"benim (işim|kararım|yerim) değil|senin kararına", re.IGNORECASE)

# Sapma bandı — BU BİZİM KONVANSİYONUMUZ, literatürden değil (Kural 6).
# n=70'te tek kayıt ~1.4 puan; ±5 puan ≈ 3-4 kayıtlık oynama.
BANT_IYI, BANT_UYARI = 0.05, 0.10

# Beyan ↔ metin tutarlılığı: kapanış türü soru içerebilir mi?
SORU_BEKLENIR = {"acik_uclu_soru": True, "takdir": False, "ozet": False,
                 "yalnizca_yansitma": False, "durur": False}


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def hukum(gozlenen: float, hedef: float) -> str:
    sapma = abs(gozlenen - hedef)
    return "✅" if sapma <= BANT_IYI else ("⚠️" if sapma <= BANT_UYARI else "❌")


def son_asistan(r: dict) -> dict:
    return next(m for m in reversed(r["messages"]) if m["role"] == "assistant")


def son_kullanici(r: dict) -> dict:
    return next(m for m in reversed(r["messages"]) if m["role"] == "user")


def dagilim_tablosu(baslik: str, sayim: collections.Counter, hedefler: dict,
                    n: int, beyan_eksik: int = 0) -> list[str]:
    sat = [f"### {baslik}", ""]
    if beyan_eksik:
        sat += [f"> ⚠️ **{beyan_eksik}/{n} kayıtta beyan yok** — bu hedef bu korpusta "
                f"ölçülemiyor. Tutmuş sayılmaz (v3 §1).", ""]
    if not sayim:
        return sat + ["_ölçülemedi._", ""]
    olcuk = sum(sayim.values())
    sat += ["| Değer | Adet | Oran | Hedef | Sapma | |", "|---|---:|---:|---:|---:|:--:|"]
    for anahtar, hedef in hedefler.items():
        adet = sayim.get(anahtar, 0)
        oran = adet / olcuk
        sat.append(f"| `{anahtar}` | {adet} | %{oran*100:.0f} | %{hedef*100:.0f} | "
                   f"{(oran-hedef)*100:+.0f} p | {hukum(oran, hedef)} |")
    for anahtar in sorted(set(sayim) - set(hedefler)):
        sat.append(f"| `{anahtar}` ⛔ tanımsız | {sayim[anahtar]} | "
                   f"%{sayim[anahtar]/olcuk*100:.0f} | — | — | ❌ |")
    return sat + [""]


def main(girdi: str, cikti: str) -> None:
    gp, cp = Path(girdi), Path(cikti)
    kayitlar = [json.loads(s) for s in gp.read_text().splitlines() if s.strip()]
    n = len(kayitlar)

    # --- sert kapılar --------------------------------------------------------
    kapi_dusen = []
    for r in kayitlar:
        c = run_checks(r)
        if c.get("passed"):
            continue
        nedenler = [m for m in (c.get("schema_error"), c.get("turn_structure_error"),
                                c.get("length_error")) if m]
        if not c.get("question_count_ok", True):
            nedenler.append(f"soru sayısı {c.get('question_count')} > 1")
        if "kriz_yasagi" in (c.get("forbidden_hits") or {}):
            nedenler.append(f"yasak ifade (kriz_yasagi): {c['forbidden_hits']['kriz_yasagi']}")
        kapi_dusen.append((r.get("gen_meta", {}).get("expert_sample_sira", r["id"][:8]),
                           "; ".join(nedenler) or "bilinmeyen"))

    # --- beyan alanları ------------------------------------------------------
    kapanis = collections.Counter()
    durum = collections.Counter()
    kapanis_eksik = durum_eksik = 0
    tutarsiz = []
    for r in kayitlar:
        gm = r.get("gen_meta", {})
        sira = gm.get("expert_sample_sira", r["id"][:8])
        te, kd = gm.get("turn_ending"), gm.get("konusma_durumu")
        if te:
            kapanis[te] += 1
            soru_var = count_questions(son_asistan(r).get("content", "")) > 0
            if te in SORU_BEKLENIR and soru_var != SORU_BEKLENIR[te]:
                tutarsiz.append((sira, te, "soru var" if soru_var else "soru yok"))
        else:
            kapanis_eksik += 1
        if kd:
            durum[kd] += 1
        else:
            durum_eksik += 1

    # --- metinden doğrudan ölçülenler ---------------------------------------
    soru_ile_biten = sum(1 for r in kayitlar
                         if count_questions(son_asistan(r).get("content", "")) > 0)
    mi = collections.Counter(r["mi_process"] for r in kayitlar)
    sysvar = collections.Counter(r.get("gen_meta", {}).get("system_prompt_variant", "?")
                                 for r in kayitlar)
    negatif = sum(1 for r in kayitlar if r.get("is_negative"))
    ctx = sum(1 for r in kayitlar if r.get("context"))
    multi = sum(1 for r in kayitlar if r["turn_type"] == "multi")
    kriz = sum(1 for r in kayitlar if r.get("is_crisis"))

    cevap_uz = [len(son_asistan(r).get("content", "")) for r in kayitlar]
    oranlar = []
    for r in kayitlar:
        a = son_asistan(r)
        if a.get("thinking") and a.get("content"):
            oranlar.append(len(a["thinking"]) / len(a["content"]))
    tavan_asan = [r.get("gen_meta", {}).get("expert_sample_sira", r["id"][:8])
                  for r in kayitlar
                  if (a := son_asistan(r)).get("thinking") and a.get("content")
                  and len(a["thinking"]) / len(a["content"]) > 4.0]

    # kullanıcı mesajı biçimi (K42 / v3 §3a) — kelime sayısından
    bicim = collections.Counter()
    for r in kayitlar:
        k = len(son_kullanici(r)["content"].split())
        bicim["kisa (1-8)" if k <= 8 else "ara (9-14)" if k < 15
              else "orta (15-40)" if k <= 40 else "uzun (40+)"] += 1

    # tekillik
    id_tekrar = [i for i, c in collections.Counter(r["id"] for r in kayitlar).items() if c > 1]
    msj_tekrar = [h for h, c in collections.Counter(
        hashlib.sha256(son_kullanici(r)["content"].strip().lower().encode()).hexdigest()[:12]
        for r in kayitlar).items() if c > 1]

    surumler = collections.Counter(r.get("gen_meta", {}).get("prompt_version", "?")
                                   for r in kayitlar)

    # --- rapor ---------------------------------------------------------------
    L: list[str] = []
    L += [f"# Korpus hedef raporu — `{gp.name}`", "",
          f"**Girdi:** `{gp}` · SHA256 `{sha256(gp)}`  ",
          f"**Betik:** `{Path(__file__).relative_to(KOK)}` · **Tarih:** {TARIH}  ",
          f"**Hedef kaynağı:** `prompts/uretim-v3.md` §2, §3b, §5a, §5c, §8  ",
          f"**Kayıt sayısı:** {n} · **Üretim talimatı:** "
          + " · ".join(f"`{k}` × {v}" for k, v in surumler.most_common()), "",
          "> Sapma bandı ✅ ≤ 5 puan · ⚠️ ≤ 10 puan · ❌ > 10 puan. "
          "**Bu band bizim konvansiyonumuzdur**, literatürden gelmiyor (Kural 6).", "",
          "---", ""]

    L += ["## 1. Sert kapılar (`src/checks.py`)", "",
          f"- Kapılardan geçen: **{n - len(kapi_dusen)}/{n}**",
          f"- Soru sayısı ≤ 1 kapısı: tüm kayıtlarda geçerli (kapı `checks.py` içinde)", ""]
    if kapi_dusen:
        L += ["| Kayıt | Neden |", "|---|---|"]
        L += [f"| {sira} | {neden} |" for sira, neden in kapi_dusen]
        L += [""]
    else:
        L += ["Kapı düşüren kayıt yok.", ""]

    L += ["## 2. v3 korpus hedefleri", ""]
    L += dagilim_tablosu("2a. Tur kapanışı (§5a) — beyan: `gen_meta.turn_ending`",
                         kapanis, HEDEF_TUR_KAPANISI, n, kapanis_eksik)
    L += [f"**Metinden doğrudan ölçüm:** soruyla biten cevap **{soru_ile_biten}/{n}** "
          f"(%{soru_ile_biten/n*100:.0f}) — hedef ~%50, sapma "
          f"{(soru_ile_biten/n - 0.50)*100:+.0f} p {hukum(soru_ile_biten/n, 0.50)}", "",
          "> Bu satır beyandan bağımsızdır: soru işareti sayılır, beyan okunmaz. "
          "Beyan eksik olsa da bu ölçüm her korpusta yapılabilir.", ""]
    if tutarsiz:
        L += ["**Beyan ↔ metin tutarsızlığı:**", "",
              "| Kayıt | Beyan | Metinde |", "|---|---|---|"]
        L += [f"| {s} | `{t}` | {d} |" for s, t, d in tutarsiz]
        L += [""]
    elif kapanis:
        L += ["Beyan ile metin arasında tutarsızlık yok.", ""]

    L += dagilim_tablosu("2b. Konuşma durumu (§3b) — beyan: `gen_meta.konusma_durumu`",
                         durum, HEDEF_KONUSMA_DURUMU, n, durum_eksik)
    L += dagilim_tablosu("2c. MI süreci (§5c) — alan: `mi_process`", mi, HEDEF_MI, n)
    L += dagilim_tablosu("2d. System prompt varyantı (§2)", sysvar, HEDEF_SYSVAR, n)

    metinler = [son_asistan(r).get("content", "") for r in kayitlar]
    ozerklik = sum(1 for c in metinler if OZERKLIK.search(c))
    ozerklik_g = sum(1 for c in metinler if OZERKLIK.search(c) or OZERKLIK_GENIS.search(c))
    o_satir = lambda ad, k: (f"| {ad} | {k} | %{k/n*100:.0f} | %{HEDEF_OZERKLIK*100:.0f} | "
                             f"{(k/n - HEDEF_OZERKLIK)*100:+.0f} p | {hukum(k/n, HEDEF_OZERKLIK)} |")
    L += ["### 2e. Özerklik vurgusu (§5a)", "",
          "| Ölçüm | Adet | Oran | Hedef | Sapma | |", "|---|---:|---:|---:|---:|:--:|",
          o_satir("özerklik kalıbı — dar desen", ozerklik),
          o_satir("özerklik kalıbı — geniş desen", ozerklik_g), "",
          "> İki vekil desen de **alt sınır ölçer** (K40): kalıp dışı kurulmuş özerklik "
          "cümlesini kaçırır. Dar desen K20 ifade bankası kalıplarından geliyor; geniş "
          "desen kararın sahibini adlandıran kalıpları da sayıyor (*\"o karar senin\", "
          "\"ben karar vermiyorum\"*). **Geçerli sayı geniş olandır**; dar desen v2 "
          "raporlarıyla karşılaştırılabilsin diye duruyor.", "",
          "> ⚠️ Geniş desen 2026-09-14'te `v3-parti1` okunduktan sonra yazıldı, yani o "
          "korpus için kör bir ölçüm değil. Körlük sınaması `expert-70` üzerinde yapıldı: "
          "%3 → %6. Genişletme v2'yi hedefe taşımıyor.", "",
          "### 2f. `is_negative` (§8)", "",
          f"| Ölçüm | Adet | Oran | Hedef | Sapma | |", "|---|---:|---:|---:|---:|:--:|",
          f"| `is_negative` | {negatif} | %{negatif/n*100:.0f} | "
          f"%{HEDEF_IS_NEGATIVE*100:.0f} | {(negatif/n - HEDEF_IS_NEGATIVE)*100:+.0f} p | "
          f"{hukum(negatif/n, HEDEF_IS_NEGATIVE)} |", ""]

    L += ["## 3. Hedefi olmayan dağılımlar (betimsel)", "",
          "| Ölçüm | Değer |", "|---|---|",
          f"| Çok turlu (`turn_type=multi`) | {multi}/{n} (%{multi/n*100:.0f}) |",
          f"| Bağlam modu (`context` dolu) | {ctx}/{n} (%{ctx/n*100:.0f}) |",
          f"| Kriz (`is_crisis`) | {kriz}/{n} |",
          f"| Cevap uzunluğu (karakter) | medyan {statistics.median(cevap_uz):.0f} · "
          f"min {min(cevap_uz)} · maks {max(cevap_uz)} |",
          f"| `thinking:completion` oranı | ortalama {statistics.mean(oranlar):.2f}x · "
          f"maks {max(oranlar):.2f}x (tavan 4x) |",
          f"| Tavanı aşan kayıt | {len(tavan_asan)} {tavan_asan if tavan_asan else ''} |",
          f"| Yinelenen `id` | {len(id_tekrar)} |",
          f"| Yinelenen son kullanıcı mesajı | {len(msj_tekrar)} |", ""]

    L += ["### 3a. Kullanıcı mesajı biçimi (§3a / K42)", "",
          "| Bant | Adet |", "|---|---:|"]
    for k in ["kisa (1-8)", "ara (9-14)", "orta (15-40)", "uzun (40+)"]:
        L.append(f"| {k} | {bicim.get(k, 0)} |")
    L += ["", "> `ara (9-14)` v3 §3a'da tanımlı bir bant değil; oradaki kayıtlar "
          "biçim hedefinin dışında kalmış demektir.", ""]

    L += ["## 4. Özet", ""]
    olcumler = [("tur kapanışı — soru oranı", soru_ile_biten / n, 0.50)]
    olcumler += [(f"MI · {k}", mi.get(k, 0) / n, h) for k, h in HEDEF_MI.items()]
    olcumler += [("is_negative", negatif / n, HEDEF_IS_NEGATIVE),
                 ("özerklik vurgusu (geniş desen)", ozerklik_g / n, HEDEF_OZERKLIK)]
    olcumler += [(f"system prompt · {k}", sysvar.get(k, 0) / n, h)
                 for k, h in HEDEF_SYSVAR.items()]
    kotu = [(ad, g, h) for ad, g, h in olcumler if hukum(g, h) == "❌"]
    L += [f"- Beyana dayanmadan ölçülebilen {len(olcumler)} hedefin "
          f"**{len(olcumler)-len(kotu)} tanesi bandın içinde**, "
          f"**{len(kotu)} tanesi dışında**."]
    for ad, g, h in kotu:
        L.append(f"  - ❌ {ad}: %{g*100:.0f} (hedef %{h*100:.0f})")
    if tutarsiz:
        L.append(f"- ❌ **Beyan ↔ metin tutarsızlığı: {len(tutarsiz)}/{n} kayıt.** "
                 f"Beyan dağılımı hedefe uysa bile bu kayıtlarda beyan edilen hamle "
                 f"metinde yok (§2a). Beyan, niyetin değil yapılan hamlenin kaydıdır.")
    if kapi_dusen:
        L.append(f"- ❌ Kapıdan düşen kayıt: {len(kapi_dusen)}/{n} (§1).")
    if kapanis_eksik or durum_eksik:
        L.append(f"- ⚠️ Beyan eksikliği: `turn_ending` {kapanis_eksik}/{n} · "
                 f"`konusma_durumu` {durum_eksik}/{n} kayıtta yok — "
                 f"§5a ve §3b hedefleri bu korpusta **ölçülemez**.")
    L += [""]

    cp.parent.mkdir(parents=True, exist_ok=True)
    cp.write_text("\n".join(L))
    print(f"yazıldı: {cp}  ({n} kayıt · kapı düşen {len(kapi_dusen)} · "
          f"beyan eksik {kapanis_eksik}/{durum_eksik})")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
