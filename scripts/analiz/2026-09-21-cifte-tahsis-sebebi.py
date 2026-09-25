#!/usr/bin/env python3
"""Çifte tahsisin sebebi — ve T219'un çürümesi.

⛔⛔ **SORU:** 24 tohum neden iki kez üretildi ve neden hepsi parti1+parti2
çiftinde? T212/T219 bunu açık bırakmıştı.

⭐⭐⭐ **CEVAP: `data/plan/v6-parti1.jsonl` ÜRETİMDEN SONRA YENİDEN
ÜRETİLDİ.** Git kaydı kesin: plan 09:48'de yazıldı, parti1 09:51-10:30
arasında ondan üretildi, ve **10:51'de plan yeniden üretilip üstüne
yazıldı** — 60 tohumun **60'ı da değişti**. Yeni plan, parti2'nin
planıyla aynı commit'te doğdu ve 26 satırda aynı tohumları aldı; çünkü
`kullanilmis()` yalnız `data/candidates`'ı tarar, **bir PLANI göremez.**
Sonra blok betikleri (`"source_ids": [p["source_id"]]`) başka bir kusur
için yeniden koşunca kayıtların künyesi yeni plandan yeniden damgalandı:
**59 kaydın 59'unun `source_ids` ve `gen_meta.seed_id` alanı değişti.**

⛔⛔⛔ **BUNUN BEDELİ T219'U ÇÜRÜTÜYOR.** T219 parti1'in *«başka bir
üretim rejiminde»* yazıldığını söylüyordu (kayıt-tohum örtüşmesi %6).
Ölçüldü: kayıtlar **üretildikleri plana (v1) göre %53 örtüşüyor** ve
sıfır örtüşen kayıt YOK — yani parti2 (%49) ile aynı düzeyde, sadık.
%6, kayıtların **yanlış tohumlarla** karşılaştırılmasının sonucuymuş.
➡️⭐⭐⭐ *Bir «rejim farkı» bulduğumu sandığım yerde, aslında bir veri
bozulması vardı; iki açıklama da aynı sayıyı üretiyordu ve ben
kolayını seçtim.*

Çıktı: reports/analiz/2026-09-21-cifte-tahsis-sebebi.md
"""
from __future__ import annotations

import collections
import json
import re
import subprocess
import sys
import statistics as st
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-cifte-tahsis-sebebi.md"
P1_V1 = "6816874"   # 09-20 09:49 — parti1'in ÜRETİLDİĞİ plan
P2_C = "1231d2b"    # 09-20 10:51 — parti1 planının ezildiği + parti2 planının doğduğu commit
URETIM = "4969d6f"  # 09-20 10:30 — parti1 üretimi bittiğinde kayıtlar
ONARIM_ONCESI = "HEAD~1"   # künye onarımından hemen önceki hâl
BLOK = re.compile(r"<context[^>]*>.*?</context>", re.S)

import tohum_guvenlik as TG  # noqa: E402


def _git(ref: str, yol: str) -> list[dict]:
    t = subprocess.run(["git", "show", f"{ref}:{yol}"], capture_output=True,
                       text=True, cwd=KOK).stdout
    return [json.loads(l) for l in t.splitlines() if l.strip()]


def _g(s: str) -> set[str]:
    return {w[:5] for w in re.sub(r"[^\w\s]", " ", TG.tr_sadelestir(s)).split()
            if len(w) > 4}


def main() -> int:
    v1 = {r["sira"]: r for r in _git(P1_V1, "data/plan/v6-parti1.jsonl")}
    # ⛔ v2 artık çalışma ağacında DEĞİL (onarıldı); bozuk hâli commit'ten okunur
    # ki bu rapor yeniden üretilebilir kalsın.
    v2 = {r["sira"]: r for r in _git(P2_C, "data/plan/v6-parti1.jsonl")}
    p2 = {json.loads(l)["sira"]: json.loads(l)
          for l in (KOK / "data/plan/v6-parti2.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
    kay_u = {r["gen_meta"]["parti_sira"]: r for r in _git(URETIM, "data/candidates/v6-parti1.jsonl")}
    # ⛔ Kayıtlar da onarıldı; bozulmanın ölçüldüğü hâl `ONARIM_ONCESI`.
    kay = {r["gen_meta"]["parti_sira"]: r
           for r in _git(ONARIM_ONCESI, "data/candidates/v6-parti1.jsonl")}

    sv1, sv2 = {r["seed_id"] for r in v1.values()}, {r["seed_id"] for r in v2.values()}
    sp2 = {r["seed_id"] for r in p2.values()}

    # çift üretilen tohumlar
    uret = collections.defaultdict(list)
    for f in sorted((KOK / "data/candidates").glob("v6-parti?.jsonl")):
        for l in f.read_text(encoding="utf-8").splitlines():
            if l.strip():
                r = json.loads(l)
                uret[r["gen_meta"]["seed_id"]].append(f.stem.replace("v6-", ""))
    cift = {s for s, v in uret.items() if len(v) > 1}

    # örtüşme: kayıtlar hangi plana sadık?
    ort = {}
    for ad, plan in (("v1", v1), ("v2", v2)):
        o = []
        for s, r in kay.items():
            if s not in plan:
                continue
            a = _g(plan[s]["tohum_metin"])
            b = _g(" ".join(BLOK.sub("", m["content"]) for m in r["messages"]
                            if m["role"] == "user"))
            o.append(len(a & b) / max(1, len(a)))
        ort[ad] = (100 * st.mean(o), 100 * st.median(o), sum(1 for x in o if x == 0), len(o))

    kunye = sum(1 for s in kay if s in kay_u
                and kay_u[s]["source_ids"] != kay[s]["source_ids"])
    uyum_v1 = sum(1 for s in kay_u if s in v1
                  and kay_u[s]["source_ids"] == [v1[s]["source_id"]])

    sat = ["# Çifte tahsisin sebebi — ve T219'un çürümesi", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Kanıt:** git geçmişi — plan v1 `{P1_V1}` (09:49) · üretim sonu "
           f"`{URETIM}` (10:30) · planın ezildiği commit `{P2_C}` (10:51)", "",
           "## 0. ⭐⭐⭐ Sebep", "",
           "| adım | saat | ne oldu |", "|---|---|---|",
           "| 1 | 09:48–09:49 | `v6-parti1` planlandı (**v1**) |",
           "| 2 | 09:51–10:30 | parti1 v1'den ÜRETİLDİ; 59 kaydın 59'unun "
           f"`source_ids`'i v1 ile birebir uyumlu (**{uyum_v1}/59**) |",
           "| 3 | 10:51 | ⛔⛔ **parti1 planı YENİDEN ÜRETİLİP ÜSTÜNE YAZILDI "
           f"(v2)** — 60 tohumun **{len(sv1 ^ sv2)//2}/60**'ı değişti, ortak kalan "
           f"**{len(sv1 & sv2)}** |",
           "| 4 | 10:51 | parti2 aynı commit'te planlandı. `kullanilmis()` yalnız "
           "`data/candidates`'ı tarar, **bir PLANI göremez** ⇒ iki plan "
           f"**{len(sv2 & sp2)}** satırda aynı tohumu aldı |",
           "| 5 | 10:32–11:06 | blok betikleri başka kusurlar için yeniden koştu. "
           "Betik `source_ids`'i **plandan** yazıyor "
           "(`\"source_ids\": [p[\"source_id\"]]`) ⇒ "
           f"**{kunye}/59 kaydın künyesi yeni plandan yeniden damgalandı** |",
           "", f"⭐ Sonuç: {len(cift)} tohum iki kez üretilmiş görünüyor. ⛔ Ama bu "
           "bir *«çifte tahsis»* değil, **bir künye bozulmasının yan etkisi**: "
           "parti1'in kayıtları kendi tohumlarını kaybetti ve parti2'ninkileri "
           "üstlendi.", "",
           "## 1. ⛔⛔⛔ T219 çürüdü", "", "| karşılaştırma | ortalama | medyan | sıfır örtüşen |",
           "|---|---:|---:|---:|"]
    for ad, (m, md, z, n) in ort.items():
        et = "**v1 — üretildiği plan**" if ad == "v1" else "v2 — bugünkü plan"
        sat.append(f"| {et} | **%{m:.0f}** | %{md:.0f} | {z}/{n} |")
    sat += ["", "⛔ T219 *«parti1 başka bir üretim rejiminde yazıldı; tohum "
            "ızgarayı verdi, sahneyi ben yazdım»* diyordu ve dayanağı %6'lık "
            "örtüşmeydi. Kayıtlar **üretildikleri plana göre %53 örtüşüyor** ve "
            "sıfır örtüşen kayıt yok — `v6-parti2` (%49) ile aynı düzeyde. "
            "⇒ **Rejim farkı diye bir şey yok; bir veri bozulması var.** "
            "➡️⭐⭐⭐ *İki açıklama aynı sayıyı üretiyordu — «başka türlü "
            "yazdım» ve «yanlış tohumla karşılaştırıyorum» — ve ben ölçmeden "
            "kolayını seçtim.*", "",
            "## 2. ⛔ Etkilenen ölçümler", "", "| ölçüm | durum |", "|---|---|",
            "| **T219** | ⛔ **ÇÜRÜDÜ** — parti1 rejimi diye bir şey yok |",
            "| **T220 / T222** (parti1'in 6 ekseni) | ⛔ **GEÇERSİZ** — yanlış "
            "tohumların meta'sına karşı ölçüldü; yeniden ölçülmeli |",
            "| **T221** (parti1 ↔ parti3-6) | ◐ parti3-6 tarafı ayakta, **parti1 "
            "tarafı düştü** ⇒ karşılaştırma geçersiz |",
            "| **T223** (kaynak ayrımı) | ◐ parti1 dahil edilmişti; parti3-6 "
            "sonucu (bant içinde) parti1 çıkarılınca da ayakta kalır mı, "
            "**ölçülmedi** |",
            "| T217 (tohum karşılığı kapısı) | ⭐ etkilenmedi; kapı zaten bu "
            "sınıfı yakalamak için kuruldu |",
            "| Kapsama envanterleri | ⛔ parti1'in 59 kaydı **yanlış tohum "
            "meta'sıyla** sayılıyor ⇒ T211'in hedefleri o kadarıyla yanlış "
            "zemine oturuyor |",
            "", "## 3. ⭐ Onarım mümkün ve kayıpsız", "",
            "| | |", "|---|---|",
            f"| plan v1 git'te duruyor | `{P1_V1}:data/plan/v6-parti1.jsonl` |",
            f"| üretim anındaki künye git'te duruyor | `{URETIM}` — 59/59 kayıt |",
            "| kayıt METİNLERİ | bugünkü hâlleri korunur; onarım yalnız "
            "`source_ids` + `gen_meta.seed_id` alanlarına dokunur |",
            "| çifte tahsis | onarımdan sonra **kendiliğinden kalkar**: plan v1 ∩ "
            f"plan2 = **{len(sv1 & sp2)}** |",
            "", "⛔⛔ **ONARIM YAPILMADI.** `data/plan/` ve `data/candidates/` "
            "işlenmiş veridir; 59 kaydın künyesini değiştirmek ve ardından "
            "kapsama envanterlerini yeniden üretmek bir zincir başlatır. Karar "
            "kullanıcının.", "",
            "## 4. ⭐⭐⭐ ONARIM YAPILDI — ve gerçek hasarı görünür kıldı", "",
            "| | |", "|---|---:|",
            "| plan v1 geri kondu · künyesi düzeltilen kayıt | **59/59** |",
            "| onarım sonrası kayıt–tohum örtüşmesi | **%53** (sıfır örtüşen 0) |",
            "| ⛔ **çift üretilen tohum: 24 → 37** | parti1+parti2 çifti **sıfırlandı**, "
            "yerine parti1+parti3 (22) · parti1+parti4 (8) · parti1+parti5 (4) · "
            "parti1+parti6 (3) çıktı |", "",
            "⛔⛔ **Onarım hasarı YARATMADI, GÖRÜNÜR KILDI.** Bozulma sırasında "
            "parti1'in gerçek tohumları künyeden düştüğü için `kullanilmis()` "
            "onları **boşta** saydı ve parti3-6 onları yeniden çekti. Yani "
            "parti1'in 59 tohumunun **37'si** (%63) sonraki bir partide ikinci "
            "kez kullanılmış. ⭐ Asistan cevapları farklı (Jaccard ort. %10) ama "
            "**kullanıcı turları ortalama %35, en yükseği %85 örtüşüyor** ⇒ "
            "eğitim girdisinde gerçek bir yakın-tekrar var ve bu, künye "
            "bozulmasının asıl bedeli.", "",
            "## 5. ⭐ Kurulan iki kapı", "", "| kapı | ne yapar |", "|---|---|",
            "| **künye kapısı** (`birlestir.py`) | her kayıt için "
            "`source_ids` ve `gen_meta.seed_id`'yi PLANA karşı denetler; "
            "uyuşmazsa birleştirme reddeder. Uçtan uca sınandı |",
            "| **plan kapısı** (`P1.havuz`) | havuz artık `kullanilmis()` "
            "yanında **başka partilerin PLANLARINI** da dışlıyor (kendi çıktısı "
            "hariç) ⇒ iki plan aynı anda aynı tohumu alamaz |", "",
            "## ⛔ Bu soruşturmanın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Planın NEDEN yeniden üretildiği kesin değil** | commit "
            "mesajı parti1'in elle yazılmış hedef listesinin kapanmış açıkları "
            "kovaladığını söylüyor; plan muhtemelen bu yüzden yeniden türetildi. "
            "Ama üretilmiş bir partinin planını yeniden üretmenin **hiçbir işe "
            "yaramayacağı** o an fark edilmemiş |",
            "| ⭐ **Kapılar kuruldu** | bkz. §5; ama *«üretilmiş bir partinin planı "
            "hiç değişemez»* diye doğrudan bir yazma kilidi hâlâ yok — künye "
            "kapısı değişikliği ancak BİRLEŞTİRMEDE yakalar |",
            "| ⛔⛔ **T224'te bir cümle yanlıştı ve düzeltildi** | "
            "*«`gd-021`'in tohumu `v6-parti1#4`'te ÜRETİLMİŞTİ»* demiştim; o "
            "tohum **plan v1'de yok**, yalnız bozuk v2 planında vardı ⇒ kriz "
            "tohumu parti1'de hiç üretilmemiş. Bozuk planı okumaktan gelen bir "
            "iddiaydı |",
            "| ⛔ **`kullanilmis()` planları görmüyor** | iki plan aynı anda "
            "üretilirse hâlâ çakışabilirler; bu da düzeltilmedi |",
            "| ⚠️ **12 kaydın metni de değişmiş** | üretimden sonraki meşru "
            "düzeltmeler (elle onay, `is_negative`, iskele temizliği); onarım "
            "bunlara dokunmamalı |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print(f"✅ sebep: plan v1→v2 ezilmesi · değişen tohum {len(sv1 ^ sv2)//2}/60 · "
          f"v2∩plan2 {len(sv2 & sp2)} · v1∩plan2 {len(sv1 & sp2)}")
    print(f"⛔ T219 çürüdü: kayıt–tohum örtüşmesi v1'e göre %{ort['v1'][0]:.0f} "
          f"(sıfır örtüşen {ort['v1'][2]}), v2'ye göre %{ort['v2'][0]:.0f} "
          f"(sıfır örtüşen {ort['v2'][2]})")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
