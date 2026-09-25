#!/usr/bin/env python3
"""`datasets/v0.1.0/CARD.md` üretir — ilk DONDURULMUŞ araştırma sürümü (K275).

⛔⛔ **K84: bütün sayılar TÜRETİLİR.** Bileşim `train.jsonl`'den, eleme
`manifest.json`'dan, model sonuçları kayıtlı eksen koşularından okunur.
Düz metin hüküm taşımaz; hüküm taşıyan her cümle bir sayıya bağlıdır.

⭐ **İçerik `v0.0.22` ile birebir aynıdır** — aynı girdiden (`data/judged/
v0.0.22.jsonl`) `src/build.py` ile yeniden derlendi. Betik bunu SHA ile
**denetler**; tutmazsa kart yazılmaz. Sürüm numarası bir içerik değişikliğini
değil, bir **karar**ı işaretler: veri üretimi durduruldu, sürüm donduruldu.

⭐ Model sonuçları `v0.0.22` ile eğitilmiş `e3` kolunun (8 tohum) EK-1
ölçümüdür; içerik aynı olduğu için bu sürümün de ölçümüdür. Yardımcılar EK-1
çözümleme betiğinden import edilir (K103) — iki ayrı puanlama doğmasın.

⛔ `datasets/` IMMUTABLE (Kural 7): var olan kart üzerine yazılmaz; `v0.0.22`
kartındaki bayat cümleler orada DÜZELTİLMEZ, bu kartın §7'sinde kaydedilir.

Kullanım: uv run python scripts/analiz/2026-09-24-v010-kart.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import math
import statistics as st
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
SURUM, KAYNAK, ONCEKI_ANA = "v0.1.0", "v0.0.22", "v0.0.18"
KART = KOK / f"datasets/{SURUM}/CARD.md"
EK = KOK / "reports/analiz/eksen-kosu"

_sp = _iu.spec_from_file_location(
    "_coz", KOK / "scripts/analiz/2026-09-23-onkayit-ek1-cozumleme.py")
C = _iu.module_from_spec(_sp)
_sp.loader.exec_module(C)

# plan.md §5 dilim hedefleri (plan.md:293-302) — karşılaştırma için okunur,
# kotaların kendisi bu kartta DEĞİŞTİRİLMEZ
PLAN = [("Terapötik, tek tur", 35), ("Çok turlu diyalog", 15),
        ("Kriz + rol sınırı", 10), ("Direnç / inkâr / discord", 5),
        ("Nazikçe karşı çıkma", 5), ("RAG — context sadakati", 10),
        ("Kapsam dışı / sınır", 5), ("Replay (genel amaçlı)", 15)]
K42 = {"kisa": 40, "orta": 35, "uzun": 25}      # plan.md:318-324, onaysız
# taban koşuları (adaptersiz, tek greedy koşu, max_tokens 1024) — 2026-09-24'te
# BUGÜNKÜ set ve denetleyiciyle yeniden koşuldu (T278): 09-15 tabanları set ve
# `smoke_checks` değişikliklerinden ÖNCE puanlanmıştı; `sycophancy` tabanı ise
# eski raporda ince ayarlı bir koşudan okunmuştu (`_son("-sycophancy")` hatası)
TABAN = {k: f"-taban-0924-{k}" for k in
         ("safety", "forget", "context_fidelity", "sycophancy", "cfreal", "cfo")}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def oku(p: Path) -> list[dict]:
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def taban_dir(desen: str) -> Path:
    d = sorted(p for p in EK.iterdir() if p.name.endswith(desen))
    if not d:
        raise SystemExit(f"⛔ taban koşusu yok: {desen}")
    return d[-1]


def main() -> int:
    if KART.exists():
        raise SystemExit(f"⛔ {KART.relative_to(KOK)} zaten var — üzerine yazılmaz (Kural 7)")
    d = KOK / f"datasets/{SURUM}"
    man = json.loads((d / "manifest.json").read_text())
    kman = json.loads((KOK / f"datasets/{KAYNAK}/manifest.json").read_text())
    s_cikti, s_kaynak = sha(d / "train.jsonl"), sha(KOK / f"datasets/{KAYNAK}/train.jsonl")
    if s_cikti != s_kaynak or man["dropped"] != kman["dropped"] \
            or man["input_sha256_16"] != kman["input_sha256_16"]:
        raise SystemExit(f"⛔ {SURUM} içeriği {KAYNAK} ile aynı değil — kart yazılmadı")
    if sha(KOK / man["input_file"]) != man["input_sha256_16"]:
        raise SystemExit("⛔ girdi dosyası manifestten sonra değişmiş")

    tr = oku(d / "train.jsonl")
    n = len(tr)
    say = lambda f: collections.Counter(f(r) for r in tr)
    pc = lambda k: f"{100 * k / n:.1f}"
    dilim = say(lambda r: r["slice"])
    sen = say(lambda r: r["scenario"])
    konus = say(lambda r: r["talk_type"])
    bant = say(lambda r: (r.get("gen_meta") or {}).get("bicim") or "—")
    kriz = sum(r["is_crisis"] for r in tr)
    jm = say(lambda r: (r.get("judge") or {}).get("judge_model")
             or ("replay" if r.get("replay") else "—"))
    sebep = collections.Counter(x["reason"] for x in man["dropped"])
    onc_id = {r["id"] for r in oku(KOK / f"datasets/{ONCEKI_ANA}/train.jsonl")}
    ekli = sum(1 for r in tr if r["id"] not in onc_id)
    dusen = len(onc_id - {r["id"] for r in tr})

    rag = dilim["rag_tek_tur"] + dilim["rag_cok_tur"]
    mevcut = [f"{dilim['terapotik_tek_tur']} ({pc(dilim['terapotik_tek_tur'])})",
              f"{dilim['terapotik_cok_tur']} ({pc(dilim['terapotik_cok_tur'])}) terapötik "
              f"+ {dilim['rag_cok_tur']} RAG",
              f"kriz **{kriz}** · `rol_siniri` {sen['rol_siniri']} ({pc(sen['rol_siniri'])})",
              f"`inkar` {sen['inkar']} ({pc(sen['inkar'])}) · `discord` {konus['discord']}",
              f"{sen['nazikce_karsi_cikma']} ({pc(sen['nazikce_karsi_cikma'])})",
              f"{rag} ({pc(rag)})",
              "⚠️ ayrı alanla türetilemiyor",
              f"**{dilim['replay']}** ({pc(dilim['replay'])})"]

    # ── model sonuçları: taban (tek koşu) · d1 = v0.0.18 · e3 = bu içerik ──
    h = C._hucreler()
    m = json.loads(C.MUHUR.read_text())
    b2 = set(m["degisen_maddeler"]["bas_olcu"]["yeni"]["B2"]["ogeler"])
    kabul = C._g._kabul()
    kriz_id = {o["id"] for o in oku(KOK / "evals/safety_crisis.jsonl") if o["kutup"] == "kriz"}
    gec = lambda rs, f=lambda r: True: sum(1 for r in rs if f(r) and r.get("otomatik_gecti"))
    der = lambda rs: sum(C._g.derece(r["cevap"], kabul) for r in rs if r["id"] in kriz_id)
    OLCU = [("`safety_crisis` kriz yönlendirmesi, dereceli", "safety", 30, der),
            ("`safety_crisis` otomatik", "safety", 20, gec),
            ("`forgetting_smoke`", "forget", 30, gec),
            ("`context_fidelity`", "context_fidelity", 20, gec),
            ("`context_fidelity` çakışmasız 8 (B2)", "context_fidelity", 8,
             lambda rs: gec(rs, lambda r: r["id"] in b2)),
            ("`context_fidelity.real`", "cfreal", 15, gec),
            ("`context_fidelity.ortusmez` (B1, `celiskili`)", "cfo", 15, gec),
            ("`sycophancy`", "sycophancy", 24, gec)]
    tab = []
    for ad, kisa, tavan, f in OLCU:
        t = f(C._satirlar(taban_dir(TABAN[kisa])))
        kol = {k: [f(C._satirlar(h[(k, s, kisa)])) for s in C._ek.TOHUM] for k in ("d1", "e3")}
        o = {k: (st.mean(v), 2 * st.stdev(v) / math.sqrt(len(v))) for k, v in kol.items()}
        tab.append(f"| {ad} | {tavan} | **{t}** | {o['d1'][0]:.2f} ± {o['d1'][1]:.2f} | "
                   f"**{o['e3'][0]:.2f} ± {o['e3'][1]:.2f}** | {o['e3'][0] - t:+.2f} | "
                   + ("↑" if o["e3"][0] - t > o["e3"][1] else "↓"
                      if t - o["e3"][0] > o["e3"][1] else "okunamaz") + " |")

    s = [f"# BıRAG veri kümesi — {SURUM}", "",
         f"**Tarih:** {man['date']} · **Girdi:** `{man['input_file']}` SHA256-16 "
         f"`{man['input_sha256_16']}`  ",
         f"**Çıktı:** `train.jsonl` SHA256-16 `{s_cikti}`  ",
         f"**Kayıt:** **{man['n_kept']}** / {man['n_total']} (elenen {man['n_dropped']})  ",
         f"**Durum:** ⭐ **ilk dondurulmuş araştırma sürümü** (K275) · ⛔ **kriz dilimi "
         f"HARİÇ** · ürün sürümü DEĞİL", "",
         f"⭐ **İçerik `{KAYNAK}` ile birebir aynıdır** — aynı girdiden yeniden derlendi, "
         f"`train.jsonl` SHA'sı ve elenen liste eşit (betik denetler). `{ONCEKI_ANA}`'e göre "
         f"+{ekli} kayıt (`celiskili` sınıfı), düşen {dusen}.", "",
         "---", "",
         "## 1. Neden şimdi dondu", "",
         "| gerekçe | kanıt |", "|---|---|",
         "| **Hacim hedefi karşılandı** | `plan.md:280-288`: *v0.1.0 ~800-1.200*; bu sürüm "
         f"{n} |",
         "| **Veri eklemek ölçülebilir kazanç vermiyor** | 571 → 1033: okunamaz (T246) · "
         "1033 → 1058: 11 karşılaştırmanın 11'i okunamaz (T277) |",
         "| **Kalan açıklar üretimle kapanmıyor** | kriz dilimi (uzman + etik kurul) · ikinci "
         "uzman + κ · bağımsız judge · K42 onayı · 12B — hepsi insan kararı |", "",
         "⛔ Plan v0.1.0'da **her dilimin temsil edilmesini** istiyor (`plan.md:286`); bu sürüm "
         "bunu **karşılamıyor** — §2. Kriz verisi uydurulmadı (Kural 3); açık kartta yazılı "
         "bırakıldı ve `v0.2.0`'ın konusu.", "",
         "## 2. Kapsam — plan hedefine karşı", "",
         "| plan dilimi | hedef | bu sürüm (%) |", "|---|---:|---|"]
    for (ad, hdf), mv in zip(PLAN, mevcut):
        s.append(f"| {ad} | %{hdf} | {mv} |")
    s += ["", "⛔⛔ **İki yapısal açık:**", "",
          f"- **Kriz: {kriz} kayıt.** Uzman onayına kadar bekletiliyor (Kural 3). `safety_crisis` "
          "ekseni bu yüzden korpusa **kör** (T259) — §5'teki kriz gerilemesinin sebebi.",
          f"- **Replay: {dilim['replay']} kayıt (%{pc(dilim['replay'])}, hedef %15).** Unutma "
          "savunması zayıf; %5 alan dışı sinyalin unutmayı tabana döndürdüğü deney kolunda "
          "ölçüldü (T253/T257) ama ana hatta alınmadı.", "",
          "⚠️ Tek/çok tur, RAG ve nazikçe karşı çıkma hedefin **üstünde**; bu bir kusur değil, "
          "hacim hedefin %10'unda olduğu için oranlar dengesiz.", "",
          "### Kullanıcı mesajı biçimi (K42) — ⚠️ kota yürütücü onayı almadı", "",
          "| bant | hedef | bu sürüm |", "|---|---:|---:|"]
    for b, hdf in K42.items():
        s.append(f"| `{b}` | %{hdf} | {bant[b]} (%{pc(bant[b])}) |")
    s += ["", "⛔ Kota **tutmuyor**. Kota onaylanmadığı için sürüm buna bekletilmedi; "
          "T261'e göre uzun girdi uydurmayı 6,4 kat bastırıyor ⇒ fazlalık bilinçli olarak "
          "düzeltilmedi.", "",
          "### Diğer dağılımlar", "", "| alan | dağılım |", "|---|---|"]
    for ad, alan in (("bağımlılık", "addiction_type"), ("yaş", "age_group"),
                     ("tur", "turn_type"), ("MI süreci", "mi_process")):
        c = say(lambda r: r[alan])
        s.append(f"| {ad} | " + " · ".join(f"{k} {v}" for k, v in c.most_common()) + " |")
    s += ["", "## 3. ⛔⛔ Judge karışımı (K97)", "", "| judge | kayıt |", "|---|---:|"]
    s += [f"| `{k}` | {v} |" for k, v in jm.most_common()]
    s += ["", "⛔ İki judge'ın puanları aynı tabloya konmaz; uydurma kapısı judge'a göre farklı "
          "sıklıkta ateşliyor (%5,6 ↔ %2,7 — `v0.0.18` kartı §1).", "",
          "## 4. Eleme", "", "| sebep | kayıt |", "|---|---:|"]
    s += [f"| `{k}` | {v} |" for k, v in sebep.most_common()]
    s += ["", "Elenenler silinmedi (Kural 7); girdi dosyasında duruyor.", "",
          "## 5. ⭐ Bu içerikle yapılan ince ayar ve ölçüm", "",
          "`e3` = bu içerik (`v0.0.22`), `d1` = `v0.0.18` — ikisi de **8 tohum**, kapsam birebir "
          "aynı (8 katman · q+o · r8). Taban adaptersiz **tek greedy koşu**. Değerler ort ± 2·SE.",
          "", "| ölçü | tavan | taban | `d1` | **`e3`** | e3 − taban | okuma |",
          "|---|---:|---:|---:|---:|---:|---|", *tab, "",
          "Okuma: taban deterministik tek koşu (hata payı yok) ⇒ |e3 − taban| > 2·SE_e3 "
          "ise ↑/↓. Tabanlar 2026-09-24'te bugünkü set ve denetleyiciyle yeniden koşuldu "
          "(T278).", "",
          "⛔⛔ **Model hâlâ ürüne verilemez:** kriz yönlendirmesi tabandan belirgin kötü; bu "
          "içerikte kriz kaydı olmadığı için veri eklemek onu kıpırdatmıyor (§2).",
          "⚠️ `e3` ↔ `d1` farklarının hiçbiri okunabilir değil (T277). B1'de iki kol da tabanın "
          "altında — ön kayıtsız gözlem, ayrı sınanacak.",
          "⛔ Gecikme KPI'ı (< 2 sn) bu sürümde ölçülmedi; `v0.0.18`'de ortanca ~6-7 sn idi.",
          "⚠️ Demo gözlemi (ölçülmedi): düşünme bölümü aynı cümleyi tekrarlayarak döngüye "
          "girebiliyor.", "",
          "## 6. ⛔ Bilinen kusurlar", "", "| | |", "|---|---|",
          "| ⛔⛔ **Uydurma temizlenmedi, yakalananlar elendi** | tek-ayrıntı sondası (T238); "
          "%12 bir alt sınır |",
          "| ⛔⛔ **Uydurma oranının kaynağı bilinmiyor** | partiler arası %1,7–%18,6 (T243) |",
          "| ⛔⛔ **Judge doğrulanmadı** | ikinci uzman + κ yok; judge AUC 0,45–0,57 |",
          "| ⛔ **`celiskili` sınıfı elle onarılmış** | uydurma ve güvenlik atlaması bulunup "
          "onarıldı (T265 · T267 · T271); yazar = onaran = okuyan (K30) |",
          "| ⛔ **`thinking` ↔ `content` denetlenmiyor** | T239 |",
          "| ⚠️ **`takdir` kapanışı risk sinyalini atlayabilir** | 2/2 vaka, payda sayılmadı "
          "(T271) |",
          "| ⚠️ **Üretici ile judge'ın çoğu aynı aileden** | K45 |", "",
          f"## 7. ⚠️ `{KAYNAK}` kartındaki bayat cümleler — orada düzeltilmedi (Kural 7)", "",
          "| o kartta | doğrusu |", "|---|---|",
          "| *«`v0.0.21` fiilen ince ayar edilen sürümdü»* | ince ayar edilen ana hat "
          "`v0.0.18`'di; `v0.0.21` eğitilmedi |",
          "| *«Kota tutturulamadı … %10.1»* | %10,1 ile §7a″ kotası **tuttu** (T272); cümle "
          "`v0.0.21` kartından sürüklenmiş |",
          "| *«Bu sürüm ÖLÇÜLMEDİ»* | 8 tohumla eğitildi ve ölçüldü (K272 · T277) |", "",
          "## ⛔ Bu kartın söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ **Dondurulmuş ≠ bitmiş** | kriz, replay ve vahşi doğa dilimleri eksik; "
          "`v0.2.0` bunlar için |",
          "| ⛔ **Test bölmesi yok** | test işini `evals/golden.{dev,test,locked}` görür; "
          "`locked` Faz 7'ye kadar açılmaz |",
          "| ⛔ **Eksen 1 (judge'lı golden) bu içerikte koşulmadı** | yalnız otomatik kapı "
          "sayımları var |"]
    KART.write_text("\n".join(s) + "\n", encoding="utf-8")
    print(f"yazıldı: {KART.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
