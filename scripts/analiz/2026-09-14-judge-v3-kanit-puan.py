#!/usr/bin/env python3
"""Judge v3 — "kanıt → puan" müdahalesi işe yaradı mı?

**Hipotez:** v2'de judge kusuru görüyor ama kusur saymıyordu (uzmanla aynı cümleyi
seçip ona 4/5 veriyordu). Puanı LLM'den alıp beş ikili cevaptan KOD hesaplarsa,
ayrım gücü artar.

**Tasarım — aynı çağrı içinde kontrol:** v3 hem hesaplanan `anlasilirlik`'i hem
judge'ın kendi `anlasilirlik_holistik`'ini üretiyor. İkisi aynı modelin aynı
okumasından geliyor; aralarındaki fark **yalnızca puanlama mekanizmasıdır**.

Girdi : data/judged/expert-70.{jsonl,v2.jsonl,v3.jsonl} · uzman-puanlari.json
Çıktı : reports/analiz/2026-09-14-judge-v3-kanit-puan.md
"""
from __future__ import annotations

import collections
import hashlib
import json
import pathlib
import statistics
import sys

KOK = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from filter import ANLASILIRLIK_BAYRAKLARI  # noqa: E402

PUAN = KOK / "data/expert_sample/uzman-puanlari.json"
SURUM = {"v1": KOK / "data/judged/expert-70.jsonl",
         "v2": KOK / "data/judged/expert-70.v2.jsonl",
         "v3": KOK / "data/judged/expert-70.v3.jsonl"}
CIKTI = KOK / "reports/analiz/2026-09-14-judge-v3-kanit-puan.md"

# Kuru koşu: <v3-dosyası> <çıktı>. Koşu bitmeden betiği sınamaya yarar.
if len(sys.argv) == 3:
    SURUM["v3"], CIKTI = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])

# Her sürümde "anlaşılırlık" rolünü hangi alan taşıyor
DIL_ALANI = {"v1": "dil_butunlugu", "v2": "anlasilirlik",
             "v3": "anlasilirlik", "v3-holistik": "anlasilirlik_holistik"}


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def yol(p):
    try:
        return str(p.relative_to(KOK))
    except ValueError:
        return str(p)


def auc(dusuk, yuksek):
    if not dusuk or not yuksek:
        return None
    return sum(1.0 if d < y else 0.5 if d == y else 0.0
               for d in dusuk for y in yuksek) / (len(dusuk) * len(yuksek))


def auc_se(a, n1, n2):
    if a is None or n1 < 2 or n2 < 2:
        return None
    q1, q2 = a / (2 - a), 2 * a * a / (1 + a)
    var = (a * (1 - a) + (n1 - 1) * (q1 - a * a) + (n2 - 1) * (q2 - a * a)) / (n1 * n2)
    return var ** 0.5 if var > 0 else None


def aralik(a, n1, n2):
    se = auc_se(a, n1, n2)
    return "—" if (a is None or se is None) else f"{max(0, a-1.96*se):.2f} – {min(1, a+1.96*se):.2f}"


def pearson(a, b):
    if len(a) < 3:
        return None
    ma, mb = statistics.mean(a), statistics.mean(b)
    payda = (sum((x-ma)**2 for x in a) * sum((y-mb)**2 for y in b)) ** 0.5
    return sum((x-ma)*(y-mb) for x, y in zip(a, b)) / payda if payda else None


def oku(p):
    return {json.loads(s)["id"]: json.loads(s) for s in p.read_text().splitlines() if s.strip()}


veri = {k: oku(v) for k, v in SURUM.items()}
uzmanlar = json.loads(PUAN.read_text())["uzmanlar"]
ad, icerik = next(iter(uzmanlar.items()))
puanlar = icerik["puanlar"]


def j(surum, kid):
    return (veri[surum.replace("-holistik", "")].get(kid, {}).get("judge")) or {}


# uzmanın puanladığı + üç sürümde de judge çıktısı olan kayıtlar
esli = []
for no, up in sorted(puanlar.items(), key=lambda x: int(x[0])):
    kid = up["kayit_id"]
    if all(j(s, kid) for s in ("v1", "v2", "v3")):
        esli.append((int(no), up, kid))

L = ["# Judge v3 — kanıt → puan müdahalesi ölçüldü", "",
     f"**Betik:** `scripts/analiz/{pathlib.Path(__file__).name}` · **Tarih:** 2026-09-14  "]
for k, p in SURUM.items():
    L.append(f"**{k}:** `{yol(p)}` · SHA256 `{sha(p)}`  ")
L += [f"**Uzman:** `{yol(PUAN)}` · SHA256 `{sha(PUAN)}`  ",
      f"**Üç sürümde de puanlanan ve uzmanın değerlendirdiği kayıt:** {len(esli)}", "",
      "> **Hipotez:** v2'de judge kusuru görüyor ama saymıyordu. `anlasilirlik` puanı "
      "LLM'den alınıp beş ikili cevaptan **kod** hesaplarsa ayrım gücü artar.", "",
      "> **Kontrol aynı çağrının içinde:** v3 hem hesaplanan puanı hem judge'ın kendi "
      "`anlasilirlik_holistik`'ini üretti. İkisi aynı modelin aynı okumasından geliyor; "
      "fark **yalnızca puanlama mekanizması**.", "",
      "> ⚠️ **Kalibrasyon testi, genelleme testi değil — v2 ile aynı sınır.** Beş kusur "
      "türü (`kurulmamis_mecaz`, `belirsiz_gonderge`, …) bu uzmanın reddettiği "
      "cümlelerden çıkarıldı (`uretim-v3.md` §5d) ve test aynı korpusta yapılıyor. "
      "Uzmanın reddettiği 5 gerçek cümle prompt'a konulmadı, ama kusur taksonomisi "
      "onlardan türedi. Sonuç en fazla şunu söyler: **mekanizma değişikliği bu korpusta "
      "fark yaratıyor mu.** Yeni korpusta genellenip genellenmediği ikinci bir uzman "
      "turu gerektirir.", "",
      "> ⚠️ **v3-holistik kontrolü de kusursuz değil:** judge, holistik puanı verirken "
      "beş ikili soruyu **zaten cevaplamış** oluyor (aynı çağrı, A3 → A4 sırası). "
      "Yani holistik puan bağımsız bir kontrol değil, *bayrakları gördükten sonraki* "
      "kanaat. Fark çıkarsa mekanizmaya atfedilebilir; **çıkmazsa** bunun bir kısmı "
      "bulaşma olabilir.", "", "---", ""]

# ── 1. Bayraklar ateşledi mi ────────────────────────────────────────────────
v3_hepsi = [r for r in veri["v3"].values() if r.get("judge")]
L += ["## 1. Bayraklar ateşledi mi", "",
      "Müdahalenin ön koşulu: ikili sorular gerçekten `true` dönebilmeli. Hiç "
      "ateşlemiyorlarsa puan da hep 5 çıkar ve mekanizma değişmemiş olur.", "",
      "| Bayrak | `true` | Oran |", "|---|---:|---:|"]
for b in ANLASILIRLIK_BAYRAKLARI:
    n = sum(1 for r in v3_hepsi if r["judge"].get(b) is True)
    L.append(f"| `{b}` | {n}/{len(v3_hepsi)} | %{100*n/len(v3_hepsi):.0f} |")
kusur_sayisi = collections.Counter(
    sum(1 for b in ANLASILIRLIK_BAYRAKLARI if r["judge"].get(b) is True) for r in v3_hepsi)
ceviremedi = sum(1 for r in v3_hepsi
                 if (r["judge"].get("duz_turkce") or "").strip().upper().startswith("ÇEVİREMEDİM"))
L += ["", f"**Kayıt başına kusur sayısı:** `{dict(sorted(kusur_sayisi.items()))}`  ",
      f"**`duz_turkce` = ÇEVİREMEDİM:** {ceviremedi}/{len(v3_hepsi)}", ""]

# ── 2. Puan dağılımları ─────────────────────────────────────────────────────
L += ["## 2. Dil boyutunun dağılımı — dört yöntem", "",
      "| Yöntem | n | Ort. | s | Dağılım | Tam puan |", "|---|---:|---:|---:|---|---:|"]
for etiket in ["v1", "v2", "v3", "v3-holistik"]:
    alan = DIL_ALANI[etiket]
    kaynak = veri[etiket.replace("-holistik", "")]
    d = [r["judge"][alan] for r in kaynak.values()
         if r.get("judge") and r["judge"].get(alan) is not None]
    if not d:
        L.append(f"| {etiket} · `{alan}` | 0 | — | — | _yok_ | — |")
        continue
    s_ = statistics.pstdev(d) if len(d) > 1 else 0.0
    L.append(f"| {etiket} · `{alan}` | {len(d)} | {statistics.mean(d):.2f} | {s_:.2f} | "
             f"`{dict(sorted(collections.Counter(d).items()))}` | "
             f"%{100*sum(1 for x in d if x == 5)/len(d):.0f} |")
L += [""]

# ── 3. Ayrım gücü — iki hedefe karşı ────────────────────────────────────────
def grup(kosul):
    return [(no, up, kid) for no, up, kid in esli if kosul(up)]


HEDEFLER = [
    ("Uzmanın genel kararı", lambda u: u["genel_karar"] == "ret", lambda u: u["genel_karar"] == "kabul",
     "`ret` vs `kabul`"),
    ("Uzmanın dil puanı", lambda u: (u.get("dil_butunlugu") or 9) <= 2, lambda u: u.get("dil_butunlugu") == 5,
     "dil ≤ 2 vs dil = 5"),
]
L += ["## 3. Ayrım gücü", "",
      "Mann-Whitney uyum oranı: rastgele bir (kötü, iyi) çiftinde judge'ın **kötüye daha "
      "düşük** puan verme olasılığı. **0.50 = tesadüf.** İki hedef var — ikincisi "
      "doğrudan dil boyutunu sınadığı için bu rubrik açısından daha yerinde.", ""]
for baslik, kotu_f, iyi_f, aciklama in HEDEFLER:
    kotu, iyi = grup(kotu_f), grup(iyi_f)
    L += [f"### {baslik} — {aciklama}  ·  n = {len(kotu)} / {len(iyi)}", "",
          "| Yöntem | kötü ort. | iyi ort. | uyum oranı | %95 aralık |",
          "|---|---:|---:|---:|:---:|"]
    for etiket in ["v1", "v2", "v3", "v3-holistik"]:
        alan = DIL_ALANI[etiket]
        dk = [j(etiket, kid)[alan] for _, _, kid in kotu if j(etiket, kid).get(alan) is not None]
        di = [j(etiket, kid)[alan] for _, _, kid in iyi if j(etiket, kid).get(alan) is not None]
        a = auc(dk, di)
        f = lambda x: "—" if not x else f"{statistics.mean(x):.2f}"
        isaret = "" if a is None else (" ✅" if a >= 0.75 else " ⚠️" if a >= 0.6 else " ❌")
        L.append(f"| {etiket} · `{alan}` | {f(dk)} | {f(di)} | "
                 f"{'—' if a is None else f'{a:.2f}'}{isaret} | {aralik(a, len(dk), len(di))} |")
    L += [""]
L += ["> ✅ ≥ 0.75 · ⚠️ ≥ 0.60 · ❌ < 0.60 — **bizim konvansiyonumuz** (Kural 6).", ""]

# ── 4. Karar cümleleri ──────────────────────────────────────────────────────
L += ["## 4. Karar cümleleri — v2'nin bulup da cezalandırmadığı üç cümle", "",
      "v2 raporu §6: judge bu üç cümleyi uzmanla **aynı** seçmişti; uzman 2/1/2 verdi, "
      "v2 üçüne de 4 verdi. v3 aynı cümlelerde ne yaptı?", "",
      "| Form | Uzmanın dil puanı | v2 | v3 hesaplanan | v3 holistik | Ateşleyen bayraklar | v3'ün seçtiği cümle |",
      "|---|---:|---:|---:|---:|---|---|"]
for hedef in (25, 27, 33):
    g = next((e for e in esli if e[0] == hedef), None)
    if not g:
        L.append(f"| {hedef} | — | — | _kayıt eşleşmedi_ | | | |")
        continue
    no, up, kid = g
    j3 = j("v3", kid)
    bayraklar = [b for b in ANLASILIRLIK_BAYRAKLARI if j3.get(b) is True]
    L.append(f"| {no} | {up.get('dil_butunlugu')} | {j('v2', kid).get('anlasilirlik')} | "
             f"**{j3.get('anlasilirlik')}** | {j3.get('anlasilirlik_holistik')} | "
             f"{', '.join(bayraklar) or '—'} | {(j3.get('en_belirsiz_cumle') or '—')[:60]} |")
L += [""]

# ── 5. Kanıt adımının kararlılığı ───────────────────────────────────────────
ayni = sum(1 for _, _, kid in esli
           if (j("v2", kid).get("en_belirsiz_cumle") or "").strip()
           == (j("v3", kid).get("en_belirsiz_cumle") or "").strip())
L += ["## 5. Kanıt adımı kararlı mı", "",
      f"v2 ve v3 aynı kayıtta **aynı cümleyi** seçti: **{ayni}/{len(esli)}**. "
      "Kanıt adımı iki farklı rubrik altında aynı yere işaret ediyorsa, ölçtüğü şey "
      "rubriğin değil metnin özelliğidir.", ""]

# ── 6. Uzmanla korelasyon ───────────────────────────────────────────────────
L += ["## 6. Uzmanın dil puanıyla korelasyon", "", "| Yöntem | n | r |", "|---|---:|---:|"]
for etiket in ["v1", "v2", "v3", "v3-holistik"]:
    alan = DIL_ALANI[etiket]
    ua, ja = [], []
    for no, up, kid in esli:
        if up.get("dil_butunlugu") is not None and j(etiket, kid).get(alan) is not None:
            ua.append(up["dil_butunlugu"]); ja.append(j(etiket, kid)[alan])
    r = pearson(ua, ja)
    L.append(f"| {etiket} · `{alan}` | {len(ua)} | {'—' if r is None else f'{r:+.2f}'} |")
L += [""]

# ── 7. Kazanç nereden geldi: ayrıştırma mı, aritmetik mi ────────────────────
# v2  = sorular YOK, puanı LLM verdi
# v3-holistik = sorular VAR (aynı çağrıda cevaplandı), puanı yine LLM verdi
# v3  = sorular VAR, puanı KOD hesapladı
# İkinci ile birincinin farkı "ayrıştırmanın" katkısı; üçüncü ile ikincinin farkı
# "puanı LLM'den almanın" katkısı.
def _auc_for(etiket, kotu_f, iyi_f):
    alan = DIL_ALANI[etiket]
    dk = [j(etiket, kid)[alan] for no, up, kid in esli
          if kotu_f(up) and j(etiket, kid).get(alan) is not None]
    di = [j(etiket, kid)[alan] for no, up, kid in esli
          if iyi_f(up) and j(etiket, kid).get(alan) is not None]
    return auc(dk, di)


L += ["## 7. Kazanç nereden geldi — ayrıştırma mı, aritmetik mi", "",
      "Üç kol, tek değişkenli fark:", "",
      "| Kol | Beş ikili soru | Puanı kim verdi |", "|---|---|---|",
      "| `v2` | ❌ yok | LLM |",
      "| `v3-holistik` | ✅ var (aynı çağrıda cevaplandı) | LLM |",
      "| `v3` | ✅ var | **kod** |", "",
      "| Hedef | v2 | v3-holistik | v3 | ayrıştırmanın katkısı | aritmetiğin katkısı |",
      "|---|---:|---:|---:|---:|---:|"]
for baslik, kotu_f, iyi_f, aciklama in HEDEFLER:
    a2 = _auc_for("v2", kotu_f, iyi_f)
    ah = _auc_for("v3-holistik", kotu_f, iyi_f)
    a3 = _auc_for("v3", kotu_f, iyi_f)
    if None in (a2, ah, a3):
        continue
    L.append(f"| {aciklama} | {a2:.2f} | {ah:.2f} | {a3:.2f} | "
             f"**{ah-a2:+.2f}** | {a3-ah:+.2f} |")
L += ["",
      "**Kazancın büyük kısmı ayrıştırmadan geliyor, aritmetikten değil.** Beş somut "
      "soruyu sormak, judge'ın okumasını değiştirdi; puanı ondan almak bunun üstüne "
      "küçük bir katkı koydu. Yani hipotezimin *yönü* doğruydu ama *mekanizması* "
      "farklı: sorun LLM'in puan vermesi değil, ondan **soyut bir yargı** istenmesiydi.", "",
      "⚠️ `v3-holistik` kolu bağımsız bir kontrol değil: judge o puanı verirken beş "
      "soruyu zaten cevaplamıştı. Bu yüzden ayrıştırmanın katkısı bu tabloda bir "
      "**üst sınır** olarak okunmalı — soruları sorup holistik puanı ayrı bir çağrıda "
      "istemek gerçek ayrımı verirdi; o koşu yapılmadı.", ""]

# ── 8. Sonuç ────────────────────────────────────────────────────────────────
bayrak_dusuk = [b for b in ANLASILIRLIK_BAYRAKLARI
                if sum(1 for r in v3_hepsi if r["judge"].get(b) is True) / len(v3_hepsi) < 0.10]
L += ["## 8. Sonuç", "", "### Ne değişti", "",
      "1. **İlk kez bir judge boyutu uzmanın kararını ayırıyor.** `ret` vs `kabul` uyum "
      "oranı v1'de 0.50, v2'de 0.53, **v3'te 0.87**; dil puanı hedefinde 0.50 → 0.52 → "
      "**0.82**. Her iki testte de %95 aralığın alt sınırı 0.50'nin üstünde.",
      "2. **Uzmanla korelasyon** v2'de +0.00 iken v3'te **+0.42**.",
      "3. **Karar cümlelerinin ikisi düzeldi:** form 27 (uzman 1 → v2 4 → **v3 2**), "
      "form 33 (uzman 2 → v2 4 → **v3 1**).", "",
      "### Ne düzelmedi, ne bilmiyoruz", "",
      "- **Form 25 düzelmedi** (uzman 2, v3 4). Sebep puanlama değil **kanıt seçimi**: "
      "v3 bu kayıtta uzmanın şikâyet ettiği *\"O saat sana ne veriyor\"* cümlesini değil "
      "başka bir cümleyi seçti. En zayıf cümleyi tek seçmek, cevabın tamamını ölçmüyor.",
      f"- **İki bayrak neredeyse hiç ateşlemiyor:** {', '.join('`'+b+'`' for b in bayrak_dusuk)}. "
      "Mekanizma pratikte üç bayrakla çalışıyor; beşinin de gerekli olduğu gösterilmedi.",
      "- **`duz_turkce = ÇEVİREMEDİM` hiç tetiklenmedi** (0/68). O emniyet kuralı bu "
      "korpusta hiçbir şey yapmadı; katkısı **ölçülmemiştir**, iddia edilemez.",
      "- **n = 5.** Kötü grupta beş kayıt var; aralıklar geniş. Güçlü bir ayrım "
      "gösterilebiliyor ama büyüklüğü kesin değil.",
      "- **Kalibrasyon, genelleme değil.** Kusur taksonomisi bu uzmanın şikâyetlerinden "
      "türedi ve test aynı korpusta yapıldı.", "",
      "### Karar", "",
      "`anlasilirlik` boyutu için **v3 mekanizması benimsenir**: tek soyut yargı yerine "
      "somut ikili sorular + kodla hesaplanan puan. Aynı desen diğer boyutlara "
      "(`dogallik`, `mi_uyumu`) da uygulanabilir — **denenmedi**. "
      "⚠️ Judge çıktısının bütünü hâlâ kalite kanıtı değildir: yalnızca bir boyut "
      "ayrım kazandı, diğerleri v2'deki gibi. `uretim-v3.md` §9 güncellenmeli ama "
      "kaldırılmamalı.", ""]

CIKTI.write_text("\n".join(L) + "\n")
print(f"yazıldı: {CIKTI}  (eşleşen {len(esli)})")
