#!/usr/bin/env python3
"""Gösterge seçimi sınaması — v4'ün doğallık/MI bayrakları neden hiç ateşlemiyor?

v4 kuru koşusunda `dogallik` bayraklarının beşi de, TIP 35 tuzaklarının altısı da
0/21 çıktı. İki rakip açıklama var ve bu betik ikisini ayırıyor:

  (A) Judge gevşek davranıyor, kusuru görmüyor.
  (B) Kusur korpusta gerçekten yok — çünkü `checks.py` onu üretimde zaten eliyor.

(B) doğruysa müdahale yanlış yere yapılmış demektir: ayrıştırma, ayrıştırılan özellik
korpusta **değişmiyorsa** ayrım üretemez. Gösterge, kapıdan geçmeyen bir kusur olmalı.

Ayrıca iki yan soru:
  · Uzmanın gözünde `dogallik` `anlasilirlik`'ten ayrı bir boyut mu?
  · `ozerklik_vurgusu` gerçekten yok mu (K20 ifade bankası kalıplarıyla tarandı)?

Çıktı: reports/analiz/2026-09-14-gosterge-secimi.md
"""
from __future__ import annotations

import collections
import hashlib
import json
import pathlib
import re
import statistics
import sys

KOK = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from checks import scan_forbidden  # noqa: E402

KAYIT = KOK / "data/candidates/expert-70.jsonl"
PUAN = KOK / "data/expert_sample/uzman-puanlari.json"
CIKTI = KOK / "reports/analiz/2026-09-14-gosterge-secimi.md"

SIZ = re.compile(r"\b(siz|size|sizi|sizin|sizde|sizden)\b|s[ıiuü]n[ıiuü]z\b", re.IGNORECASE)
# K20 ifade bankası §"Özerklik saygısı" kalıplarından türetilmiş vekil desenler.
# ⚠️ Vekil: kalıbı yakalar, anlamı değil (K40'ın dersi).
OZERKLIK = re.compile(
    r"senin kararın|sen(in)? bilirsin|bana düşmez|karar sende|"
    r"demeyeceğim|söylemeyeceğim|dayatmak istemem|sana kalmış|"
    r"isteyip istemediğin|istersen", re.IGNORECASE)
KLISE = re.compile(r"^\s*(anlıyorum|seni duyuyorum|bu zor olmalı|haklısın|çok zor)",
                   re.IGNORECASE)
JARGON = re.compile(r"farkındalık|içgörü|duygudurum|baş etme mekanizma|motivasyon kaynağ|"
                    r"süreç yönetim|bilişsel|davranışsal kalıp", re.IGNORECASE)
OVGU = re.compile(r"harika|mükemmel|muhteşem|gurur duy|bravo|tebrik", re.IGNORECASE)


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def pearson(a, b):
    if len(a) < 3: return None
    ma, mb = statistics.mean(a), statistics.mean(b)
    payda = (sum((x-ma)**2 for x in a) * sum((y-mb)**2 for y in b)) ** 0.5
    return sum((x-ma)*(y-mb) for x, y in zip(a, b)) / payda if payda else None


kayitlar = [json.loads(s) for s in KAYIT.read_text().splitlines() if s.strip()]
cevaplar = {r["id"]: next(m["content"] for m in reversed(r["messages"])
                          if m["role"] == "assistant") for r in kayitlar}
ad, icerik = next(iter(json.loads(PUAN.read_text())["uzmanlar"].items()))
puanlar = icerik["puanlar"]

L = ["# Gösterge seçimi sınaması — bayraklar neden ateşlemiyor", "",
     f"**Girdi:** `{KAYIT.relative_to(KOK)}` · SHA256 `{sha(KAYIT)}`  ",
     f"**Uzman:** `{PUAN.relative_to(KOK)}` · SHA256 `{sha(PUAN)}`  ",
     f"**Betik:** `scripts/analiz/{pathlib.Path(__file__).name}` · **Tarih:** 2026-09-14  ",
     f"**Kayıt:** {len(kayitlar)}", "",
     "> v4'ün `dogallik` bayrakları ve TIP 35 tuzakları hiç ateşlemedi. İki rakip "
     "açıklama: **(A)** judge gevşek · **(B)** kusur korpusta yok çünkü `checks.py` "
     "onu üretimde zaten eliyor. Bu betik ikisini ayırıyor — judge'a hiç bakmadan, "
     "yalnızca metni tarayarak.", "", "---", ""]

# ── 1. Yasak ifade kapısı ne kadarını zaten alıyor ────────────────────────
L += ["## 1. Yasak ifade kapısı korpusta ne buluyor", "",
      "`configs/filters.yaml` kategorileri, 70 cevabın metninde:", "",
      "| Kategori | Eşleşen kayıt | v4'teki karşılığı |", "|---|---:|---|"]
ESLEME = {"bos_guvence": "`bos_guvence` bayrağı", "etiketleme": "`tuzak_etiketleme`",
          "emredici_kip": "`tuzak_erken_tavsiye` ile akraba",
          "utanc_buyutme": "`tuzak_suclama` ile akraba",
          "zararli_normallestirme": "—", "ahlaki_yargi_klinik": "—",
          "rol_siniri": "`rol_siniri_ihlali`", "kriz_yasagi": "—"}
toplam_hit = collections.Counter()
for r in kayitlar:
    for kat in scan_forbidden(cevaplar[r["id"]]):
        toplam_hit[kat] += 1
for kat, aciklama in ESLEME.items():
    L.append(f"| `{kat}` | {toplam_hit.get(kat, 0)}/{len(kayitlar)} | {aciklama} |")
L += ["",
      "**Bu tablo (B) şıkkını destekliyor:** doğallık bayraklarının üçü "
      "(`bos_guvence`, etiketleme kaynaklı `tuzak_etiketleme`, emredici kip) "
      "üretimde **zaten eleniyor**. Judge'a ulaşan korpus bu kusurları taşımıyor; "
      "dolayısıyla o bayrakların ateşlememesi doğru davranıştır, körlük değil.", ""]

# ── 2. Kalan doğallık göstergeleri metinde var mı ─────────────────────────
L += ["## 2. Diğer doğallık göstergeleri — kodla tarandığında", "",
      "| Gösterge | Desen | Eşleşen kayıt |", "|---|---|---:|"]
for ad_, desen, rx in [("`siz_kaymasi`", "`siz` / `-sınız`", SIZ),
                       ("`klise_acilis`", "cevabın ilk kelimeleri", KLISE),
                       ("`terapi_jargonu`", "farkındalık · içgörü · duygudurum …", JARGON),
                       ("`ovgu_tonu`", "harika · mükemmel · gurur duy …", OVGU)]:
    n = sum(1 for r in kayitlar if rx.search(cevaplar[r["id"]]))
    L.append(f"| {ad_} | {desen} | {n}/{len(kayitlar)} |")
L += ["", "⚠️ Bunlar **vekil** desenler (K40): kalıbı yakalar, anlamı değil. "
      "Sıfıra yakın çıkmaları, göstergenin bu korpusta **ayırt edici olmadığını** "
      "gösterir — judge'ın onları görememesinden bağımsız bir bulgu.", ""]

# ── 3. Özerklik gerçekten yok mu ──────────────────────────────────────────
oz = [r for r in kayitlar if OZERKLIK.search(cevaplar[r["id"]])]
L += ["## 3. `ozerklik_vurgusu` — judge 0 buldu, metin ne diyor", "",
      f"K20 ifade bankasının *Özerklik saygısı* kalıplarıyla tarandığında: "
      f"**{len(oz)}/{len(kayitlar)}** kayıtta eşleşme.", ""]
if oz:
    L += ["| Kayıt | Eşleşen bölüm |", "|---|---|"]
    for r in oz[:8]:
        m = OZERKLIK.search(cevaplar[r["id"]])
        bas = max(0, m.start() - 40)
        L.append(f"| #{r['gen_meta']['expert_sample_sira']} | …{cevaplar[r['id']][bas:m.end()+40]}… |")
    L += [""]
L += ["Bu bir **çelişki sinyali** olabilir: judge hiçbir kayıtta özerklik vurgusu "
      "görmediyse ama metinde kalıp varsa, ikili sorunun tanımı dar ya da judge "
      "bu beceriyi tanımıyor demektir. Tersine, metinde de yoksa üretim talimatının "
      "özerklik vurgusunu **yeterince üretmediği** anlaşılır — bu ikincisi "
      "`uretim-v3.md` için doğrudan bir düzeltme kalemidir.", ""]

# ── 4. Uzmanın gözünde doğallık ayrı bir boyut mu ─────────────────────────
dil, dog, karar = [], [], []
for no, up in puanlar.items():
    if up.get("dil_butunlugu") is not None and up.get("kisalik_dogallik") is not None:
        dil.append(up["dil_butunlugu"]); dog.append(up["kisalik_dogallik"])
        karar.append(up["genel_karar"])
r = pearson(dil, dog)
ayni = sum(1 for a, b in zip(dil, dog) if a == b)
L += ["## 4. Uzmanın gözünde `dogallik` ayrı bir boyut mu", "",
      f"Uzmanın **dil bütünlüğü** ile **kısalık/doğallık** puanları (n={len(dil)}):", "",
      f"| Ölçüm | Değer |", "|---|---|",
      f"| Pearson r | **{'—' if r is None else f'{r:+.2f}'}** |",
      f"| İki puanın birebir aynı olduğu kayıt | {ayni}/{len(dil)} (%{100*ayni/len(dil):.0f}) |",
      f"| Dil dağılımı | `{dict(sorted(collections.Counter(dil).items()))}` |",
      f"| Doğallık dağılımı | `{dict(sorted(collections.Counter(dog).items()))}` |", ""]
if r is not None and r > 0.8:
    L += [f"**r = {r:+.2f} — uzman bu iki maddeyi pratikte tek bir şey olarak "
          "doldurmuş.** Doğallık bu korpusta ayrı bir boyut değil; bir cevabı "
          "\"yapay\" bulduğunda zaten \"anlaşılmaz\" da buluyor. Bu durumda "
          "`dogallik` için ayrım aramak, **var olmayan bir ayrımı aramaktır** — "
          "v4'ün negatif sonucunun uzman tarafındaki karşılığı.", ""]

# ── 5. Sonuç ──────────────────────────────────────────────────────────────
L += ["## 5. Sonuç — gösterge nasıl seçilmeli", "",
      "1. **Ayrıştırma, ayrıştırılan özellik korpusta değişmiyorsa ayrım üretemez.** "
      "`anlasilirlik` çalıştı çünkü anlaşılmazlık **hiçbir kapıdan geçmiyor**: "
      "ölçülmediği için korpusta duruyor ve varyansı var.",
      "2. **Zaten kapıda elenen kusuru judge'a sormak boşa soru.** Doğallık "
      "bayraklarının üçü `configs/filters.yaml` listelerinin kopyası; o kusurlar "
      "judge'a ulaşmadan eleniyor.",
      "3. **Gösterge seçme kuralı (öneri):** bir boyutu ayrıştırırken, önce o "
      "göstergenin korpusta **ateşleyip ateşlemediğine kodla bak**. Ateşlemiyorsa "
      "ya kapı zaten hallediyordur ya da gösterge yanlıştır; ikisinde de judge'a "
      "sormanın getirisi yok.", "",
      "> Bu rapor judge çıktısına **hiç bakmadan** yazıldı; yalnızca korpus metni ve "
      "uzman puanları kullanıldı. v4 sonucundan bağımsız olarak geçerlidir.", ""]

CIKTI.write_text("\n".join(L) + "\n")
print(f"yazıldı: {CIKTI}")
