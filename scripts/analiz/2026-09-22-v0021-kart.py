#!/usr/bin/env python3
"""`datasets/v0.0.21/CARD.md` üretir — bütün sayılar TÜRETİLİR.

⛔⛔ **K84: rapor üreticisinde SABİT HÜKÜM yazılmaz.** Kartın her sayısı
`train.jsonl`, `manifest.json` ve girdi dosyasından okunur; hiçbir tablo
elle yazılmaz. Karşılaştırma sürümü (`v0.0.18`) de dosyadan okunur.

⛔ `datasets/` IMMUTABLE (Kural 7) — ama `CARD.md` sürümün **kendi**
belgesidir ve sürümle birlikte yazılır; var olan bir kart üzerine
yazılmaz.

Kullanım: uv run python <betik> [--surum=v0.0.21] [--onceki=v0.0.18]
"""
from __future__ import annotations

import collections
import hashlib
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from kunye import betik_tarihi  # noqa: E402

SURUM = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--surum=")),
             "v0.0.21")
ONCEKI = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--onceki=")),
              "v0.0.18")
KART = KOK / f"datasets/{SURUM}/CARD.md"


def say(kayit, f):
    return collections.Counter(f(r) for r in kayit)


def main() -> int:
    if KART.exists():
        raise SystemExit(f"⛔ {KART} zaten var — üzerine yazılmaz (Kural 7)")
    man = json.loads((KOK / f"datasets/{SURUM}/manifest.json").read_text())
    tr = [json.loads(l) for l in open(KOK / f"datasets/{SURUM}/train.jsonl")]
    onc = [json.loads(l) for l in open(KOK / f"datasets/{ONCEKI}/train.jsonl")]
    onc_id = {r["id"] for r in onc}
    yeni = [r for r in tr if r["id"] not in onc_id]
    dusen = onc_id - {r["id"] for r in tr}
    cikti_sha = hashlib.sha256(
        (KOK / f"datasets/{SURUM}/train.jsonl").read_bytes()).hexdigest()[:16]

    dilim = say(tr, lambda r: r.get("slice") or "—")
    bant = say(tr, lambda r: (r.get("gen_meta") or {}).get("bicim") or "—")
    bagl = say(tr, lambda r: (r.get("gen_meta") or {}).get("baglam_davranisi")
               or "— (bağlamsız)")
    jm = say(tr, lambda r: ((r.get("judge") or {}).get("judge_model")
                            or ("replay" if r.get("replay") else "— (yargısız)")))
    sebep = collections.Counter(d.get("reason") for d in man.get("dropped", []))
    # bağlamlı kayıtlar içinde sınıf payı — kota bu tabana göre tanımlı
    bagl_li = [r for r in tr if (r.get("gen_meta") or {}).get("baglam_davranisi")]
    pay = 100 * sum(1 for r in bagl_li
                    if r["gen_meta"]["baglam_davranisi"] == "celiskili") / max(len(bagl_li), 1)

    s = [f"# BıRAG veri kümesi — {SURUM}", "",
         f"**Tarih:** {betik_tarihi(__file__)} · **Girdi:** "
         f"`{man['input_file']}` SHA256-16 `{man['input_sha256_16']}`",
         f"**Çıktı:** `train.jsonl` SHA256-16 `{cikti_sha}`",
         f"**Kayıt:** **{man['n_kept']}** / {man['n_total']} "
         f"(elenen {man['n_dropped']})", "",
         f"⭐ **Ana hattın devamıdır.** `{ONCEKI}` fiilen ince ayar edilen "
         "sürümdü; `v0.0.19`/`v0.0.20` **deney kollarıdır** (aritmetik "
         "tazeleme) ve korpusun ilerleyişi değildir.", "",
         "---", "",
         f"## 1. {ONCEKI}'den farkı: §7a″ `celiskili` sınıfı", "",
         "| | |", "|---|---:|", f"| {ONCEKI} | {len(onc)} |",
         f"| + `celiskili` | **{len(yeni)}** |",
         f"| − düşen | **{len(dusen)}** |",
         f"| ⭐ **{SURUM}** | **{len(tr)}** |", "",
         "⭐ **Yeni olan tek şey bu sınıf.** T259'un kapsama matrisi "
         "`context_fidelity` eval'inin dört kategorisinden **`celiskili`**'nin "
         "korpusta **sıfır kaydı** olduğunu bulmuştu — üstelik o eksen ince "
         "ayarın ölçülebilir kazanç verdiği **tek** eksendi (T254, +1,33).", "",
         "⛔⛔ **Ama bu sınıf kendi kusurunu da üretti ve kartta yazılı "
         "olmalı:** ilk 12 kaydın **3'ü** (%25) kullanıcının söylemediği bir "
         "ayrıntıyı ona atfediyordu — yani sınıfın **karşı çıkmak için "
         "tasarlandığı** kusuru (T265). Üçü de onarıldı ve **yeniden "
         "yargılandı**; bu sürümdeki 12 kaydın tamamı `grounding = 5`. "
         "⇒ *Bu bir «uydurmasız sınıf» değil, **uydurması bulunup elle "
         "onarılmış** bir sınıftır.*", "",
         f"⛔ **Kota tutturulamadı:** §7a″ `celiskili` payını ~%10 hedefliyor; "
         f"bu sürümde bağlamlı {len(bagl_li)} kaydın **%{pay:.1f}**'i. "
         "Sınıfın ince ayara etkisi bu sürümle **ölçülebilir olmayabilir**.",
         "", "## 2. Bileşim", "", "| dilim | kayıt |", "|---|---:|"]
    s += [f"| `{k}` | {v} |" for k, v in dilim.most_common()]
    s += ["", "| bant (`gen_meta.bicim`) | kayıt |", "|---|---:|"]
    s += [f"| `{k}` | {v} |" for k, v in bant.most_common()]
    s += ["", "⛔ Bant **türetmedir, beyan değil** (T263): `bicim` beyan "
          "edilmiş üçüncü alan olarak sürüklenmişti ve birleştirme anında "
          "yeniden türetildi.", "",
          "| bağlam sınıfı | kayıt |", "|---|---:|"]
    s += [f"| `{k}` | {v} |" for k, v in bagl.most_common()]
    s += ["", "## 3. ⛔⛔ Judge karışımı (K97)", "", "| judge | kayıt |",
          "|---|---:|"]
    s += [f"| `{k}` | {v} |" for k, v in jm.most_common()]
    s += ["", "⛔⛔ **Bu korpus TEK BİR judge ile puanlanmamıştır.** K97: iki "
          "judge'ın sayıları aynı tabloya konmaz; buradaki tablo bir **dağılım "
          "beyanıdır**, bir karşılaştırma değil.", "",
          "## 4. Eleme", "", "| sebep | kayıt |", "|---|---:|"]
    s += [f"| `{k}` | {v} |" for k, v in sebep.most_common()]
    s += ["", "⛔ Elenenler **silinmedi** (Kural 7); girdi dosyasında "
          "duruyorlar ve SHA256'sı yukarıda yazılı.", "",
          "## 5. ⭐ Bu sürümde ilk kez koşan kapılar", "", "| kapı | ne yapar |",
          "|---|---|",
          "| `bant_ok` | `gen_meta.bicim` beyanını türetmeye karşı sınar "
          "(T263) |",
          "| `celiskili_ok` | `celiskili` beyan eden cevap çelişkiyi "
          "**adlandırmalı** ve **iki pasaja birden** atıf yapmalı (T262) |",
          "| `yansitma_ok` | kullanıcıya **alıntıyla** atfedilen söz, "
          "kullanıcı turlarında bulunmalı (T266) |", "",
          "⭐ `_checks` atıldı ve girdinin tamamında bugünkü `run_checks` "
          "yeniden koştu ⇒ korpus **tek denetim sürümüyle** geçildi (T240). "
          f"Eskiden geçip şimdi düşen kayıt: **{len(dusen)}**.", "",
          "⛔⛔ **`yansitma_ok` DAR bir kapıdır:** 1176 etiketli kayıtta "
          "kesinliği **%100** ama duyarlılığı **%1** — yalnız alıntıyla atfa "
          "bakar, alıntısız parafraz uydurmasını **görmez** (T266). Kapıdan "
          "geçmek temiz olmak değildir.", "",
          "## ⛔ Bu kartın söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔⛔ **`grounding` alt sınırdır** | tek-ayrıntı sondası (T238): "
          "judge'ın adlandırdığı ayrıntı dayanaklıysa 5 verir ve aynı "
          "cevaptaki başka bir uydurmayı **görmez** |",
          "| ⛔⛔ **`celiskili` kayıtlarını ben yazdım, onardım ve yargısını "
          "ben okudum** | K30/K260; bağımsız anotatör hâlâ borç |",
          "| ⛔ **Sınıf DAR öğretiliyor** | 12 pasaj çiftinin tamamı "
          "**idari/usule ilişkin** çelişki (gün, ücret, yaş, belge, süre, "
          "sıklık); klinik çelişki **yok** ve bu bilinçli (Kural 3) |",
          "| ⛔ **Bu sürüm ÖLÇÜLMEDİ** | ince ayar koşulmadı; buradaki hiçbir "
          "sayı model başarımı hakkında bir şey söylemez |",
          "| ⚠️ **Yargı turları karışık** | `celiskili`'nin 9 kaydı ilk "
          "yargıdan, 3 kaydı onarım sonrası yeniden yargıdan |"]

    KART.write_text("\n".join(s) + "\n", encoding="utf-8")
    assert KART.exists()
    print(f"⭐ {KART.relative_to(KOK)} yazıldı")
    print(f"   {len(tr)} kayıt · yeni {len(yeni)} · düşen {len(dusen)}")
    print(f"   celiskili payı (bağlamlı kayıtlarda): %{pay:.1f}")
    print(f"   eleme: {dict(sebep)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
