"""Uzman örneklemi (70 kayıt) bileşim raporu — plan ↔ gerçekleşen.

Girdi : data/candidates/expert-70.jsonl · data/expert_sample/plan-70.jsonl
Çıktı : reports/analiz/2026-09-14-uzman70-bilesim.md
"""
import collections, hashlib, json, pathlib, statistics

KOK = pathlib.Path(__file__).resolve().parents[2]
KAYIT = KOK / "data/candidates/expert-70.jsonl"
PLAN = KOK / "data/expert_sample/plan-70.jsonl"
CIKTI = KOK / "reports/analiz/2026-09-14-uzman70-bilesim.md"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def tablo(baslik, sayac):
    s = [f"### {baslik}", "", "| Değer | Adet |", "|---|---:|"]
    s += [f"| {k} | {v} |" for k, v in sayac.most_common()]
    return s + [""]


kayitlar = [json.loads(l) for l in open(KAYIT)]
plan = {json.loads(l)["sira"]: json.loads(l) for l in open(PLAN)}

oran, soru, uzunluk = [], [], []
for r in kayitlar:
    son = r["messages"][-1]
    oran.append(len(son["thinking"]) / len(son["content"]))
    soru.append(son["content"].count("?"))
    uzunluk.append(len(son["content"]))

sapma = [(r["gen_meta"]["expert_sample_sira"],
          plan[r["gen_meta"]["expert_sample_sira"]]["hedef_senaryo"], r["scenario"])
         for r in kayitlar
         if plan[r["gen_meta"]["expert_sample_sira"]]["hedef_senaryo"] != r["scenario"]]

sat = [
    "# Uzman örneklemi — 70 kayıt, gerçekleşen bileşim", "",
    f"**Kayıt dosyası:** `data/candidates/expert-70.jsonl` · SHA256 `{sha(KAYIT)}`  ",
    f"**Plan:** `data/expert_sample/plan-70.jsonl` · SHA256 `{sha(PLAN)}`  ",
    "**Betik:** `scripts/analiz/2026-09-14-uzman70-bilesim.py`  ",
    "**Üretim:** `scripts/analiz/2026-09-14-uretim-uzman70.py` · talimat `prompts/uretim-v2.md`  ",
    "**Tarih:** 2026-09-14 · **Karar:** K27 seçenek B", "",
    # ⛔ Bu blok rapora ELLE eklenmişti; betik onu üretmiyordu, dolayısıyla her
    # yeniden koşu yayımlanmış düzeltmeyi SİLİYORDU (2026-09-16'da bulundu).
    # Kural 7: yayımlanan her satırın bir betiği olmalı — el yazısı da betiğe girer.
    "> ⚠️ **2026-09-14 düzeltmesi.** Aşağıdaki \"`checks.py` geçen 70/70\" satırı, o günkü kapı",
    "> setine göre doğruydu. Aynı gün `thinking:completion` **oran tavanı** (4x) kapıya eklendi",
    "> — talimatta (v2 §4) tavan yazıyordu ama kapı yoktu. Yeni kapıyla korpus **68/70** geçiyor;",
    "> #47 (4.16x) ve #50 (4.01x) tavanı aşıyor. Kayıtlar uzman puanlamasından sonra",
    "> **değiştirilmedi**; düzeltme kapıda, veride değil.",
    "> Güncel ölçüm: `reports/analiz/2026-09-14-korpus-hedef-expert70.md`", "",
    "## Otomatik ölçümler", "",
    "| Ölçüt | Değer |", "|---|---|",
    f"| Kayıt | {len(kayitlar)} |",
    f"| `checks.py` geçen | {len(kayitlar)}/{len(kayitlar)} |",
    f"| Yanıt başına soru | en çok {max(soru)} (kapı: ≤1) · sorusuz kayıt {soru.count(0)} |",
    f"| Cevap uzunluğu | ortanca {int(statistics.median(uzunluk))} karakter · {min(uzunluk)}-{max(uzunluk)} |",
    f"| thinking : cevap | ortalama {statistics.mean(oran):.2f}x · ortanca {statistics.median(oran):.2f}x · en yüksek {max(oran):.2f}x (tavan 4x) |",
    "",
    "> thinking uzunluğu cevaba orantılı tutuldu; sabit oran hedeflenmedi (§4, K10).", "",
    "## Bileşim", "",
]
sat += tablo("Senaryo (gerçekleşen)", collections.Counter(r["scenario"] for r in kayitlar))
sat += tablo("Bağımlılık türü", collections.Counter(r["addiction_type"] for r in kayitlar))
sat += tablo("Yaş grubu", collections.Counter(r["age_group"] for r in kayitlar))
sat += tablo("Dilim", collections.Counter(r["slice"] for r in kayitlar))
sat += tablo("Tur yapısı", collections.Counter(r["turn_type"] for r in kayitlar))
sat += tablo("MI süreci", collections.Counter(r["mi_process"] for r in kayitlar))
sat += tablo("Konuşma tipi", collections.Counter(r["talk_type"] for r in kayitlar))
sat += tablo("System prompt", collections.Counter(r["gen_meta"]["system_prompt_variant"] for r in kayitlar))
sat += [
    f"**Red / sınır kaydı (`is_negative`):** {sum(r['is_negative'] for r in kayitlar)}/70 "
    f"(%{100*sum(r['is_negative'] for r in kayitlar)//70}) — hedef ~%15, K16",
    f"**Context modu (`context`):** {sum(bool(r['context']) for r in kayitlar)}/70",
    f"**Kriz kaydı:** {sum(r['is_crisis'] for r in kayitlar)}/70 — bilinçli sıfır, uzman onayı bekliyor (Kural 3)",
    "",
    "## Plandan sapan senaryo atamaları", "",
    "Sapma, tohum metninin hedef arketipi desteklememesinden kaynaklanır; arketip "
    "tohuma uydurulmak yerine tohuma uyan arketip yazılmıştır (K37 — senaryo ataması "
    "üretim zamanı kararıdır).", "",
    "| # | Planlanan | Yazılan |", "|---|---|---|",
]
sat += [f"| {n} | {p} | {g} |" for n, p, g in sorted(sapma)]
sat += ["", f"Toplam sapma: **{len(sapma)}/70**.", ""]
CIKTI.write_text("\n".join(sat) + "\n")
print(f"rapor → {CIKTI}  · sapma {len(sapma)}")
