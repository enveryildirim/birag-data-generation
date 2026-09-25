#!/usr/bin/env python3
"""`v6-parti1` yargılanır — 59 kayıt, Eksen 1 rubriği.

⭐ Kullanıcı kararı (2026-09-20): kota bugün 76 + 48 çağrı gördü, 59 kayıt daha
sınırı zorlar ⇒ **yarın koşulur**.

⛔ **Judge Claude OLAMAZ (K43/K45).** Korpusu ben yazdım ve ölçülmüş öz-şişirme
+6/+11 puan. ⇒ `filter.judge_record`, yani `agy:gemini-3.8-flash-high`.
⚠️ T176 havuzun 527/577 kaydının `claude-sonnet-subagent` ile puanlı olduğunu
ölçtü; bu parti **baştan Gemini ile** yargılanıyor ve `judge_model` her kayda
yazılıyor ⇒ K97 gereği iki judge'ın sayıları aynı tabloya konmayacak.

⭐ **Önbellek AÇIK ve bu doğru:** her kayıt bir kez yargılanıyor, tekrar ölçümü
yapılmıyor. T174'ün totolojisi yalnız *aynı kaydı iki kez sorarken* geçerliydi.

⛔ **Kota:** `src/llm.py` artık 429'u zaman aşımından ayırıyor (K216) ⇒ kota
biterse koşu **hızlı** durur, 14 dakika/kayıt yakmaz.

Girdi : data/candidates/v6-parti1.jsonl
Çıktı : data/judged/v6-parti1.jsonl · reports/analiz/2026-09-21-v6-parti1-judge.md
Kullanım: uv run python scripts/analiz/2026-09-21-v6-parti1-judge.py [--sinama]
          ... [--parti=v6-parti2]   ⭐ varsayılan `v6-parti1`
"""
from __future__ import annotations

import collections
import hashlib
import json
import statistics as st
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
# ⭐ Parti parametre oldu (T200: girdi parametreleşiyorsa ÇIKTI da
# parametreleşmeli, yoksa ikinci parti birincinin raporunu ezer).
# ⛔ Varsayılan `v6-parti1` — K240'ta yazılı komut aynen çalışmayı sürdürür.
PARTI = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--parti=")),
             "v6-parti1")
GIRDI = KOK / f"data/candidates/{PARTI}.jsonl"
CIKTI = KOK / f"data/judged/{PARTI}.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-{PARTI}-judge.md"
BOYUT = ["duygusal_tepki", "yorumlama", "kesif", "mi_uyumu", "grounding"]

import filter as F  # noqa: E402


def main(sinama: bool = False) -> int:
    ham = GIRDI.read_bytes()
    kayitlar = [json.loads(s) for s in ham.decode("utf-8").splitlines() if s.strip()]
    # ⭐ SÜRDÜRME (2026-09-21). Kota `v6-parti2`'nin ortasında bitti: 28/59
    # yargılandı, dosya yazıldı ve betik yeniden koşmayı `assert` ile
    # engelliyordu ⇒ ya 28 atılacak ya hiç koşulmayacaktı.
    # ⭐ Yargılananlar önbellekte, yani yeniden sormak BEDAVA; engel yalnız
    #    dosyanın varlığıydı. ➡️ *Bir koşunun yarıda kalması, baştan
    #    başlamayı gerektirmez — gerektiren şey, nerede kaldığını bilmektir.*
    sur = 0
    if CIKTI.exists():
        onceki = {r["gen_meta"]["parti_sira"]: r for r in
                  (json.loads(l) for l in CIKTI.read_text(encoding="utf-8").splitlines()
                   if l.strip())}
        for r in kayitlar:
            o = onceki.get(r["gen_meta"]["parti_sira"])
            if o and o.get("judge"):
                r["judge"] = o["judge"]
                sur += 1
        if sur:
            print(f"⭐ SÜRDÜRME: {sur} kayıt önceki koşudan alındı", flush=True)
    print(f"girdi: {len(kayitlar)} kayıt · SHA256-16 "
          f"{hashlib.sha256(ham).hexdigest()[:16]}", flush=True)
    print(f"judge: {F.JUDGE_MODEL} · rubrik: {F.JUDGE_PROMPT_VERSION}", flush=True)
    if sinama:
        print("⚠️ SINAMA KİPİ — servise gidilmez, yalnız girdi ve yollar denetlenir")
        assert CIKTI.parent.exists(), "⛔ data/judged/ yok"
        assert len({r["gen_meta"]["parti_sira"] for r in kayitlar}) == len(kayitlar)
        kalan = [r for r in kayitlar if r.get("judge") is None]
        print(f"✅ sınama geçti · {len(kalan)}/{len(kayitlar)} kayıt yargılanacak"
              + (f" ({sur} sürdürülüyor)" if sur else " (çıktı yolu boş)"))
        return 0

    # ⭐ Yalnız yargısı olmayanlar sorulur; sürdürülenler zaten elde.
    # ⛔⛔⛔ ANAHTAR UYUŞMAZLIĞI (bulundu 2026-09-21). Sürdürülen dal
    # `parti_sira` (int), taze dal `r["id"]` (str) döndürüyordu; aşağıdaki
    # geri yazma ise YALNIZ `r["id"]` ile arıyor ⇒ **sürdürülen her kaydın
    # puanı geri yazmada bulunamıyor ve `judge=None` olarak dosyaya
    # yazılıyordu.** `len(yargi)` iki anahtar türünü birden saydığı için
    # rapor *«58/59 yargılandı»* diyordu, oysa dosyada 30 puan vardı.
    # Üç koşu boyunca sayı 28→30→28 diye salındı: her koşu bir öncekinin
    # sürdürdüklerini siliyordu. ➡️⭐⭐⭐ *Bir sürdürme mekanizması, kaydı
    # iki yerde iki farklı anahtarla adlandırıyorsa sürdürmez — sessizce
    # siler; ve raporladığı sayı bellekteki sözlüğün boyu olduğu için
    # kaybı da gizler.*
    def f(r):
        if r.get("judge"):
            return (r["id"], r["judge"], None)
        try:
            return r["id"], dict(F.judge_record(r)), None
        except Exception as e:
            return r["id"], None, f"{type(e).__name__}: {e}"[:120]

    with ThreadPoolExecutor(max_workers=6) as h:
        out = list(h.map(f, kayitlar))
    yargi = {i: j for i, j, _ in out if j}
    hata = [(i, h_) for i, j, h_ in out if not j]
    print(f"yargılanan: {len(yargi)}/{len(kayitlar)} · hata {len(hata)}", flush=True)
    for i, h_ in hata[:5]:
        print(f"   ⚠️ {i[:8]}: {h_}")

    for r in kayitlar:
        r["judge"] = yargi.get(r["id"])
    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kayitlar),
                     encoding="utf-8")

    ort = {k: st.mean([j[k] for j in yargi.values() if j.get(k) is not None])
           for k in BOYUT if any(j.get(k) is not None for j in yargi.values())}
    bayrak = collections.Counter(
        k for j in yargi.values() for k in ("klinik_guvenlik_ihlali", "rol_siniri_ihlali",
                                            "tuzak_suclama", "kurum_yordam_ihlali")
        if j.get(k))
    sat = [f"# `{PARTI}` judge koşusu", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Girdi:** `{GIRDI.relative_to(KOK)}` SHA256-16 "
           f"`{hashlib.sha256(ham).hexdigest()[:16]}` · **{len(kayitlar)}** kayıt  ",
           f"**Judge:** `{F.JUDGE_MODEL}` · **rubrik:** `{F.JUDGE_PROMPT_VERSION}`", "",
           f"Yargılanan **{len(yargi)}/{len(kayitlar)}** · hata {len(hata)}", "",
           "## Boyut ortalamaları", "", "| boyut | ortalama |", "|---|---:|"]
    sat += [f"| `{k}` | {v:.2f} |" for k, v in ort.items()]
    sat += ["", "## Kapı bayrakları", "", "| bayrak | ateşleyen kayıt |", "|---|---:|"]
    sat += [f"| `{k}` | **{v}** |" for k, v in bayrak.most_common()] or ["| — | 0 |"]
    sat += ["", "## ⛔ Bu koşunun söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Kayıt düzeyinde puan bir ÇEKİLİŞ** | T175: aynı gün iki taze "
            "çekilişte kayıtların %61'i oynuyor ⇒ tek kaydın puanına bakıp karar "
            "verilemez, yalnız KÜME okunur |",
            "| ⛔⛔ **K97: bu sayılar Claude ile puanlanmış sayılarla AYNI TABLOYA "
            "konmaz** | havuzun 527/577'si `claude-sonnet-subagent` ile puanlı (T176) |",
            "| ⛔ **`klinik_guvenlik_ihlali` oynak** | T177: ateşleyen 4 kaydın 3'ü iki "
            "çekiliş arasında çevrildi ⇒ eleme kararı bu bayrağa dayanıyor ve `gd-019a` "
            "uzman kalemidir |",
            "| ⚠️ **Judge kalite ölçmez, tarar** | K57'den beri geçerli |", ""]
    # ⛔⛔ EKSİK KOŞU BAŞARILI SAYILMAZ. İlk sürüm 28/59 yargılayıp **0 ile**
    # çıktı ve ortalamaları bastı. İki ayrı tehlike: (a) aşağı akıştaki bir
    # adım partiyi tam sanabilir; (b) düşen çağrılar kuyruk sonunda
    # kümeleniyor (T179) ⇒ yargılanan alt küme RASTGELE DEĞİL ve
    # ortalaması partinin ortalaması değil.
    # ➡️ *Yorumlanamayacak bir sayı, şerhle değil hiç basılmamalıdır.*
    if hata:
        sat = [x for x in sat if not x.startswith("| `")]
        sat += ["", "⛔⛔ **BOYUT ORTALAMALARI BASILMADI — KOŞU EKSİK.** "
                f"{len(yargi)}/{len(kayitlar)} yargılandı. Düşen çağrılar kuyruk "
                "sonunda kümeleniyor (T179) ⇒ yargılanan alt küme rastgele "
                "değildir ve ortalaması partinin ortalaması değildir. "
                "Koşu tamamlanınca bu rapor yeniden üretilecek.", ""]
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[6:]))
    if hata:
        print(f"⛔ KOŞU EKSİK: {len(yargi)}/{len(kayitlar)} — "
              "aynı komutla yeniden koşulduğunda kaldığı yerden devam eder.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main("--sinama" in sys.argv))
