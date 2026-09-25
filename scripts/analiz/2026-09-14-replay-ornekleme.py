#!/usr/bin/env python3
"""Replay dilimi örnekleyici — plan.md §6 (%15) ve §9 (catastrophic forgetting).

Replay Claude Code üretimi DEĞİL; açık, izin verici lisanslı setlerden örneklenir.
Kullanıcı kararı (2026-09-14): **yalnızca Apache-2.0** kulvarı.

Kaynaklar (lisans kart verisinden doğrulandı, etiketten değil):
  · TFLai/Turkish-Alpaca          Apache-2.0  TR, Alpaca türevi çeviri
  · merve/turkish_instructions    Apache-2.0  TR, Alpaca türevi çeviri (farklı çeviri)
  · OpenAssistant/oasst2          Apache-2.0  EN, insan yazımı

plan.md §"Replay çeşitlilik ekseni" beş eksen istiyor:
  genel kültür ve mantık · kısa/thinking'siz yanıtlar · İngilizce örnekler ·
  uzun-form yanıtlar · farklı system prompt'lar

⚠️ Kaynakların HİÇBİRİNDE system prompt yok. Beşinci eksen bu yüzden burada
üretiliyor: genel amaçlı bir prompt bankası dolaştırılıyor ve biri bilerek BOŞ
(system mesajı olmayan kayıt da bir varyanttır). Kanonik BıRAG prompt'u asla
kullanılmaz — `src/checks.py::replay_ok` bunu kapı olarak denetliyor.

⚠️ Türkçe kaynaklar makine çevirisi ve kusurlu: ölçüldü, kayıtların %3-4'ü
girdisi düşmüş olduğu için cevaplanamaz durumda, %7'si çok kısa çıktı taşıyor
(sonuncusu replay için İSTENEN bir şey). Kırık kayıtlar eleniyor; çeviri
tuhaflıkları elenemiyor ve veri kartına yazılmalı.

Kullanım: uv run python <betik> [hedef_kayit_sayisi]
Çıktı   : data/candidates/replay-v1.jsonl + reports/analiz/2026-09-14-replay-ornekleme.md
"""
from __future__ import annotations

import collections
import csv
import gzip
import hashlib
import json
import random
import re
import sys
from datetime import date
from pathlib import Path

from huggingface_hub import hf_hub_download

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
CIKTI = KOK / "data/candidates/replay-v1.jsonl"
RAPOR = KOK / "reports/analiz/2026-09-14-replay-ornekleme.md"
MEVCUT = KOK / "data/candidates/v3-kumulatif.jsonl"
RASTGELE = random.Random(915)

KAYNAKLAR = [
    ("TFLai/Turkish-Alpaca", "data.json", "apache-2.0", "tr"),
    ("merve/turkish_instructions", "instructions.csv", "apache-2.0", "tr"),
    ("OpenAssistant/oasst2", "2023-11-05_oasst2_ready.messages.jsonl.gz", "apache-2.0", "en"),
]

# 5. eksen: farklı system prompt'lar. Kaynaklarda yok, burada üretiliyor.
# Biri bilerek boş — system mesajı olmayan kayıt da bir varyanttır ve modelin
# tek bir prompt biçimine kilitlenmesini engeller (K19).
# ⚠️ Prompt dili kaydın diliyle EŞLEŞİR. İlk sürümde tek bir banka dolaşıyordu ve
# Türkçe talimatlara İngilizce system prompt düşüyordu — çalışır ama özensiz ve
# modele gereksiz bir karışım öğretir. Boş varyant iki dilde de var.
SYSTEM_BANKASI = {
    "tr": ["Sen yardımsever bir yapay zeka asistanısın.",
           "Kısa ve net cevaplar ver.",
           "Sen bilgili bir asistansın. Yanıtlarını tarafsız tut.",
           "Sen bir öğretmensin, açıklamalarını basit tut.",
           ""],                                   # system mesajı yok
    "en": ["You are a helpful assistant.",
           "Answer concisely and accurately.",
           "You are a knowledgeable assistant. Be precise.",
           ""],
}
# Dil karışımı ve uzunluk bantları — BİZİM önerimiz, literatürden değil (Kural 6).
HEDEF_DIL = {"tr": 0.70, "en": 0.30}
BANT = {"kisa": (0, 80), "orta": (80, 400), "uzun": (400, 4000)}
HEDEF_BANT = {"kisa": 0.25, "orta": 0.50, "uzun": 0.25}

# Girdiye atıf yapıp girdisi boş olan kayıt cevaplanamaz — Alpaca çevirisinin
# bilinen kusuru, ölçüldü: TFLai %3, merve %4.
GIRDI_ATIF = re.compile(r"aşağıdaki|verilen|bu metni|bu cümleyi|şu (metni|cümleyi|listeyi)|"
                        r"yukarıdaki|following|given (the|this)", re.IGNORECASE)


def sha(p: str) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def alpaca_yukle(repo, fn):
    p = hf_hub_download(repo, fn, repo_type="dataset")
    out = []
    if fn.endswith(".json"):
        for x in json.load(open(p)):
            out.append((x.get("instruction", ""), x.get("input", ""), x.get("output", "")))
    else:
        with open(p, encoding="utf-8") as f:
            for x in csv.DictReader(f):
                out.append(((x.get("talimat") or "").strip(),
                            (x.get(" giriş") or "").strip(),
                            (x.get(" çıktı") or "").strip()))
    return p, out


def oasst_yukle(repo, fn):
    p = hf_hub_download(repo, fn, repo_type="dataset")
    msgs = {}
    with gzip.open(p, "rt") as f:
        for l in f:
            m = json.loads(l)
            if m.get("lang") == "en" and not m.get("deleted") and m.get("review_result"):
                msgs[m["message_id"]] = m
    ciftler = []
    for m in msgs.values():
        ebeveyn = msgs.get(m.get("parent_id") or "")
        if (m["role"] == "assistant" and ebeveyn and ebeveyn["role"] == "prompter"
                and ebeveyn.get("parent_id") is None and (m.get("rank") or 0) == 0
                and not m.get("synthetic")):
            ciftler.append((ebeveyn["text"].strip(), "", m["text"].strip()))
    return p, ciftler


def temiz(talimat, girdi, cikti) -> bool:
    if not talimat.strip() or not cikti.strip():
        return False
    if not girdi.strip() and GIRDI_ATIF.search(talimat):
        return False           # girdisi düşmüş, cevaplanamaz
    if len(cikti) > BANT["uzun"][1]:
        return False
    return True


def bant(cikti: str) -> str:
    n = len(cikti)
    for ad, (a, b) in BANT.items():
        if a <= n < b:
            return ad
    return "uzun"


def main() -> None:
    hedef = int(sys.argv[1]) if len(sys.argv) > 1 else None
    if hedef is None:
        mevcut = sum(1 for _ in open(MEVCUT))
        hedef = round(mevcut * 0.15 / 0.85)   # replay / (replay + mevcut) = %15

    havuz, kaynak_bilgi = {"tr": [], "en": []}, []
    for repo, fn, lisans, dil in KAYNAKLAR:
        p, kayitlar = (oasst_yukle if "oasst" in repo else alpaca_yukle)(repo, fn)
        uygun = [k for k in kayitlar if temiz(*k)]
        kaynak_bilgi.append((repo, fn, lisans, dil, len(kayitlar), len(uygun), sha(p)))
        havuz[dil] += [(repo, *k) for k in uygun]

    # Dil ve uzunluk bandı hedeflerine göre seç. Bant başına yuvarlama eksik kayıt
    # bırakabiliyordu (18 istenip 16 üretilmişti); artık eksik kalan sayı en büyük
    # banttan tamamlanıyor, böylece toplam hedefi tutuyor.
    secilen = []
    for dil, oran in HEDEF_DIL.items():
        n_dil = round(hedef * oran)
        aday = havuz[dil][:]
        RASTGELE.shuffle(aday)
        alinan_dil = 0
        for ad_bant, b_oran in HEDEF_BANT.items():
            n_b = round(n_dil * b_oran)
            alinan = 0
            for k in aday:
                if alinan >= n_b:
                    break
                if bant(k[3]) != ad_bant or k in secilen:
                    continue
                secilen.append(k); alinan += 1; alinan_dil += 1
        for k in aday:                       # yuvarlama artığını tamamla
            if alinan_dil >= n_dil:
                break
            if k in secilen:
                continue
            secilen.append(k); alinan_dil += 1

    kayitlar = []
    sayaclar = collections.Counter()
    for repo, talimat, girdi, cikti in secilen:
        dil_k = "en" if repo.startswith("OpenAssistant") else "tr"
        banka = SYSTEM_BANKASI[dil_k]
        sysm = banka[sayaclar[dil_k] % len(banka)]
        sayaclar[dil_k] += 1
        kullanici = talimat if not girdi.strip() else f"{talimat}\n\n{girdi}"
        msgs = ([{"role": "system", "content": sysm}] if sysm else []) + [
            {"role": "user", "content": kullanici},
            {"role": "assistant", "content": cikti},
        ]
        dil = dil_k
        kayitlar.append({
            "id": hashlib.sha256((kullanici + repo).encode()).hexdigest()[:24],
            "slice": "replay", "scenario": "genel", "addiction_type": "yok",
            "motivation": "ic", "mi_process": "yok", "talk_type": "yok",
            "age_group": "yetiskin", "turn_type": "single", "messages": msgs,
            "context": None, "source_ids": [f"replay:{repo}"], "is_crisis": False,
            "is_negative": False, "has_thinking": False, "judge": None, "replay": True,
            "gen_meta": {"generator": "acik-veri-ornekleme", "kaynak": repo,
                         "lisans": "apache-2.0", "dil": dil, "uzunluk_bandi": bant(cikti),
                         "system_prompt_var": bool(sysm), "date": TARIH,
                         "ornekleme_betigi": Path(__file__).name, "rastgele_tohum": 915},
        })

    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    with open(CIKTI, "w") as f:
        for r in kayitlar:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    d = collections.Counter(r["gen_meta"]["dil"] for r in kayitlar)
    b = collections.Counter(r["gen_meta"]["uzunluk_bandi"] for r in kayitlar)
    sp = len({(m["content"] for m in r["messages"] if m["role"] == "system").__str__()
              for r in kayitlar})
    sys_farkli = len({next((m["content"] for m in r["messages"] if m["role"] == "system"), "")
                      for r in kayitlar})
    L = ["# Replay dilimi — örnekleme raporu", "",
         f"**Çıktı:** `data/candidates/replay-v1.jsonl` · SHA256 `{sha(str(CIKTI))}`  ",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH} · "
         f"**Rastgele tohum:** 915  ", "",
         f"**Kayıt:** {len(kayitlar)} — mevcut korpus {sum(1 for _ in open(MEVCUT))} kayıt, "
         f"karışımda replay payı **%{len(kayitlar)/(len(kayitlar)+sum(1 for _ in open(MEVCUT)))*100:.0f}** "
         "(plan.md §6 hedefi %15)", "", "---", "",
         "## 1. Kaynaklar ve köken", "",
         "> Kullanıcı kararı (2026-09-14): **yalnızca Apache-2.0**. Lisanslar HF etiketinden "
         "değil **kart verisinden** doğrulandı.", "",
         "| Kaynak | Dosya | Lisans | Dil | Ham kayıt | Kalite süzgecinden geçen | Dosya SHA256 |",
         "|---|---|---|---|---:|---:|---|"]
    for repo, fn, lisans, dil, ham, uyg, h in kaynak_bilgi:
        L.append(f"| `{repo}` | `{fn}` | {lisans} | {dil} | {ham} | {uyg} | `{h[:16]}…` |")
    L += ["", "## 2. plan.md §\"Replay çeşitlilik ekseni\" karşılanıyor mu", "",
          "| Eksen | Durum |", "|---|---|",
          f"| genel kültür ve mantık | ✅ üç kaynak da talimat-cevap |",
          f"| kısa / thinking'siz yanıtlar | ✅ `has_thinking` **hepsi False**; kısa bant {b['kisa']}/{len(kayitlar)} |",
          f"| İngilizce örnekler | ✅ {d['en']}/{len(kayitlar)} (oasst2, insan yazımı) |",
          f"| uzun-form yanıtlar | ✅ uzun bant {b['uzun']}/{len(kayitlar)} |",
          f"| farklı system prompt'lar | ✅ {sys_farkli} farklı (biri BOŞ — system mesajı olmayan varyant) |", "",
          "## 3. Dağılımlar", "",
          "| Ölçüm | Değer | Hedef |", "|---|---|---|",
          f"| Türkçe | {d['tr']} (%{d['tr']/len(kayitlar)*100:.0f}) | %70 *(bizim önerimiz)* |",
          f"| İngilizce | {d['en']} (%{d['en']/len(kayitlar)*100:.0f}) | %30 *(bizim önerimiz)* |",
          f"| kısa (<80 kr) | {b['kisa']} | %25 |",
          f"| orta (80-400) | {b['orta']} | %50 |",
          f"| uzun (400+) | {b['uzun']} | %25 |", "",
          "## 4. ⚠️ Bilinen kalite sorunları — veri kartına girmeli", "",
          "- **Türkçe kaynakların ikisi de makine çevirisi Alpaca türevi.** Ölçüldü: iki "
          "kümenin talimatları yalnızca **%13** örtüşüyor (farklı çeviriler), yani birbirinin "
          "kopyası değiller; ama ikisi de aynı İngilizce kaynaktan geliyor.",
          "- **Çeviri kusurları elenemiyor.** Girdisi düşmüş (cevaplanamaz) kayıtlar süzüldü "
          "(kaynakta %3-4), ama *\"Sana özledim\"* gibi hatalı Türkçe otomatik ayıklanamıyor. "
          "Bu projede dil doğallığı ana kalite ekseni (K48, §5d) olduğu için bu bir **gerilim**: "
          "replay genel yeteneği korurken Türkçe doğallığa zarar verebilir. Ölçülmedi.",
          "- **oasst2'de Türkçe pratikte yok:** 135.174 mesajın **37'si** Türkçe. Bu yüzden "
          "oasst2 yalnızca İngilizce ekseni için kullanıldı.",
          "- **System prompt'lar kaynakta yok, bu betikte üretildi.** Beşinci çeşitlilik ekseni "
          "başka türlü karşılanamıyordu.", ""]
    RAPOR.write_text("\n".join(L) + "\n")
    print(f"{len(kayitlar)} kayıt → {CIKTI.relative_to(KOK)}")
    print(f"  dil {dict(d)} · bant {dict(b)} · farklı system prompt {sys_farkli}")
    print(f"rapor: {RAPOR.relative_to(KOK)}")


if __name__ == "__main__":
    main()
