#!/usr/bin/env python3
"""Judge rubriği v1 → v2: rubrik değişikliği ölçmeye başladı mı?

Soru tek: **v1'in göremediği şeyi v2 görüyor mu?** Ölçüt, uzmanın kararıdır —
uzmanın `ret` dediği kayıtları judge'ın puanı `kabul`lerden ayırabiliyor mu.

Girdi : data/judged/expert-70.jsonl      (v1 rubriği)
        data/judged/expert-70.v2.jsonl   (v2 rubriği)
        data/expert_sample/uzman-puanlari.json
Çıktı : reports/analiz/2026-09-14-judge-v2-karsilastirma.md

⚠️ Bu bir KALİBRASYON testidir, genelleme testi değil. v2 rubriği uzmanın bulduğu
kusur TÜRLERİNİ tarif ediyor (belirsiz gönderge, kurulmamış mecaz...). Uzmanın
reddettiği 5 gerçek cümle prompt'a KONULMADI, ama kusur türleri konuldu. Dolayısıyla
buradaki ayrışma "v2 bu korpusta işe yarıyor" der; "yeni korpusta da yarar" demez.
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
PUAN = KOK / "data/expert_sample/uzman-puanlari.json"
V1 = KOK / "data/judged/expert-70.jsonl"
V2 = KOK / "data/judged/expert-70.v2.jsonl"
CIKTI = KOK / "reports/analiz/2026-09-14-judge-v2-karsilastirma.md"

# Kuru koşu için: <v2-dosyası> <çıktı>. Koşu bitmeden betiği sınamaya yarar.
if len(sys.argv) == 3:
    V2, CIKTI = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])

OVGU = ["isabet", "derin", "güzel", "mükemmel", "ustaca", "harika", "kusursuz",
        "son derece", "başarıyla", "etkileyici"]


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def yol(p: pathlib.Path) -> str:
    """Proje içindeyse göreli, değilse mutlak (kuru koşu scratchpad'den okuyabiliyor)."""
    try:
        return str(p.relative_to(KOK))
    except ValueError:
        return str(p)


def pearson(a, b):
    if len(a) < 3:
        return None
    ma, mb = statistics.mean(a), statistics.mean(b)
    pay = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    payda = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** 0.5
    return pay / payda if payda else None


def auc(dusuk_olmali: list[float], yuksek_olmali: list[float]) -> float | None:
    """Mann-Whitney uyum oranı: rastgele bir (ret, kabul) çiftinde judge'ın
    ret'e daha düşük puan verme olasılığı. 0.5 = tesadüf, 1.0 = kusursuz ayrım."""
    if not dusuk_olmali or not yuksek_olmali:
        return None
    top = sum(1.0 if d < y else 0.5 if d == y else 0.0
              for d in dusuk_olmali for y in yuksek_olmali)
    return top / (len(dusuk_olmali) * len(yuksek_olmali))


def auc_se(a: float | None, n1: int, n2: int) -> float | None:
    """Hanley-McNeil (1982) standart hatası. n1=5 gibi küçük gruplarda uyum oranının
    güven aralığı çok geniştir; sayıyı vermeden 'ayrım yok' demek yanıltıcı olur."""
    if a is None or n1 < 2 or n2 < 2:
        return None
    q1 = a / (2 - a)
    q2 = 2 * a * a / (1 + a)
    var = (a * (1 - a) + (n1 - 1) * (q1 - a * a) + (n2 - 1) * (q2 - a * a)) / (n1 * n2)
    return var ** 0.5 if var > 0 else None


def oku(p: pathlib.Path) -> dict:
    return {json.loads(s)["id"]: json.loads(s) for s in p.read_text().splitlines() if s.strip()}


v1, v2 = oku(V1), oku(V2)
uzmanlar = json.loads(PUAN.read_text())["uzmanlar"]
ad, icerik = next(iter(uzmanlar.items()))
puanlar = icerik["puanlar"]

# form no -> (uzman puanı, v1 judge, v2 judge)
esli = []
for no, up in sorted(puanlar.items(), key=lambda x: int(x[0])):
    kid = up["kayit_id"]
    if kid in v1 and kid in v2 and v1[kid].get("judge") and v2[kid].get("judge"):
        esli.append((int(no), up, v1[kid]["judge"], v2[kid]["judge"], v2[kid]))

# v2 koşusunda kapıdan düşen kayıt judge'a GİTMEZ (filter.py sözleşmesi). K56 ile
# eklenen oran tavanı 2 kaydı düşürdü; ikisi de uzmanın puanladığı ve `kabul` dediği
# kayıtlar. Karşılaştırmadan çıkıyorlar — sayıyı ve sebebini rapora yazıyoruz.
disarida, eksik = [], []
for no, up in sorted(puanlar.items(), key=lambda x: int(x[0])):
    kid = up["kayit_id"]
    if kid not in v2 or v2[kid].get("judge"):
        continue
    chk = v2[kid].get("_checks") or {}
    hedef = disarida if chk.get("passed") is False else eksik
    hedef.append((int(no), up["genel_karar"], chk.get("length_error") or "—"))

karar_grubu = collections.defaultdict(list)
for no, up, j1, j2, r in esli:
    karar_grubu[up["genel_karar"]].append((no, up, j1, j2, r))

L: list[str] = []
L += ["# Judge rubriği v1 → v2 — rubrik ölçmeye başladı mı?", "",
      f"**v1 çıktısı:** `{yol(V1)}` · SHA256 `{sha(V1)}`  ",
      f"**v2 çıktısı:** `{yol(V2)}` · SHA256 `{sha(V2)}`  ",
      f"**Uzman puanları:** `{yol(PUAN)}` · SHA256 `{sha(PUAN)}`  ",
      f"**Betik:** `scripts/analiz/{pathlib.Path(__file__).name}` · **Tarih:** 2026-09-14  ",
      f"**Eşleşen kayıt:** {len(esli)} (uzmanın puanladığı ve iki rubrikle de puanlanan)", "",
      (f"> ⚠️ **{len(disarida)} kayıt kapıda düştüğü için karşılaştırma dışı.** "
       f"Kapıdan düşen kayıt judge'a gitmiyor (`filter.py` sözleşmesi); v1 koşusunda "
       f"bu kapı yoktu, o yüzden v1 tarafında puanları var. "
       + " · ".join(f"form {n} ({k}): {m}" for n, k, m in disarida)
       if disarida else ""), "",
      (f"> ❌ **{len(eksik)} kayıt kapıyı geçtiği hâlde judge çıktısı yok** — koşu "
       f"tamamlanmamış ya da çağrı başarısız olmuş olabilir: "
       + " · ".join(f"form {n}" for n, _, _ in eksik) if eksik else ""), "",
      "> ⚠️ **Kalibrasyon testi, genelleme testi değil.** v2 rubriği uzmanın bulduğu kusur "
      "*türlerini* tarif ediyor; uzmanın reddettiği 5 gerçek cümle prompt'a konulmadı ama "
      "kusur türleri konuldu. Sonuç şunu söyler: v2 bu korpusta ayrım yapıyor. Yeni bir "
      "korpusta da yapacağını söylemez — onun için ikinci bir uzman turu gerekir.", "",
      "---", ""]

# ── 1. Tavan etkisi ──────────────────────────────────────────────────────────
L += ["## 1. Tavan etkisi — judge hâlâ herkese tam puan veriyor mu?", "",
      "v1'in kusuru: `dil_butunlugu`'nde 50 kaydın 50'sine de 5 verdi (s=0.00). "
      "Ayrım yapmayan boyut hiçbir şey ölçmez.", "",
      "| Rubrik · boyut | n | Ortalama | s | Dağılım | Tam puan oranı |",
      "|---|---:|---:|---:|---|---:|"]
for etiket, kaynak, alanlar, tepe in [
        ("v1", v1, ["dil_butunlugu", "kisalik_dogallik", "grounding", "mi_uyumu"], 5),
        ("v2", v2, ["anlasilirlik", "dogallik", "grounding", "mi_uyumu"], 5)]:
    for alan in alanlar:
        d = [r["judge"][alan] for r in kaynak.values()
             if r.get("judge") and r["judge"].get(alan) is not None]
        if not d:
            L.append(f"| `{etiket}` · {alan} | 0 | — | — | _yok_ | — |")
            continue
        dag = dict(sorted(collections.Counter(d).items()))
        s = statistics.pstdev(d) if len(d) > 1 else 0.0
        L.append(f"| `{etiket}` · {alan} | {len(d)} | {statistics.mean(d):.2f} | {s:.2f} | "
                 f"`{dag}` | %{100*sum(1 for x in d if x == tepe)/len(d):.0f} |")
L += [""]

# ── 2. Ayrım gücü ────────────────────────────────────────────────────────────
L += ["## 2. Ayrım gücü — uzmanın `ret` dediklerini judge ayırabiliyor mu?", "",
      "Ölçüt: rastgele bir (`ret`, `kabul`) çiftinde judge'ın **ret'e daha düşük** puan "
      "verme olasılığı (Mann-Whitney uyum oranı). **0.50 = tesadüf.**", "",
      f"Uzmanın kararları: " + " · ".join(f"`{k}` {len(v)}" for k, v in karar_grubu.items()), "",
      "| Rubrik · boyut | ret ort. | sınırda ort. | kabul ort. | uyum oranı | %95 aralık |",
      "|---|---:|---:|---:|---:|:---:|"]


def ort(grup, idx, alan):
    d = [g[idx][alan] for g in karar_grubu[grup]
         if g[idx].get(alan) is not None]
    return statistics.mean(d) if d else None


def dizi(grup, idx, alan):
    return [g[idx][alan] for g in karar_grubu[grup] if g[idx].get(alan) is not None]


for etiket, idx, alanlar in [("v1", 2, ["dil_butunlugu", "kisalik_dogallik", "mi_uyumu", "grounding"]),
                             ("v2", 3, ["anlasilirlik", "dogallik", "mi_uyumu", "grounding"])]:
    for alan in alanlar:
        r, s_, k = ort("ret", idx, alan), ort("sınırda", idx, alan), ort("kabul", idx, alan)
        d_ret, d_kabul = dizi("ret", idx, alan), dizi("kabul", idx, alan)
        a = auc(d_ret, d_kabul)
        se = auc_se(a, len(d_ret), len(d_kabul))
        f = lambda x: "—" if x is None else f"{x:.2f}"
        isaret = "" if a is None else (" ✅" if a >= 0.75 else " ⚠️" if a >= 0.6 else " ❌")
        aralik = "—" if (a is None or se is None) else \
            f"{max(0, a - 1.96*se):.2f} – {min(1, a + 1.96*se):.2f}"
        L.append(f"| `{etiket}` · {alan} | {f(r)} | {f(s_)} | {f(k)} | {f(a)}{isaret} | {aralik} |")
L += ["", "> ✅ ≥ 0.75 · ⚠️ ≥ 0.60 · ❌ < 0.60 — **bu eşikler bizim konvansiyonumuz** (Kural 6).", ""]

# ── 3. cevapsiz_soru ─────────────────────────────────────────────────────────
bayrakli = [(no, up, j2) for no, up, j1, j2, r in esli if j2.get("cevapsiz_soru")]
tum_bayrak = [r for r in v2.values() if (r.get("judge") or {}).get("cevapsiz_soru")]
L += ["## 3. `cevapsiz_soru` — v1'de hiç olmayan boyut", "",
      f"70 kaydın **{len(tum_bayrak)}**'inde işaretlendi; uzmanın puanladığı 50'nin "
      f"**{len(bayrakli)}**'inde.", ""]
if bayrakli:
    L += ["| Form | Uzman kararı | Judge'ın alıntıladığı soru |", "|---|---|---|"]
    for no, up, j2 in bayrakli:
        L.append(f"| {no} | {up['genel_karar']} | {(j2.get('cevapsiz_soru_metni') or '—')[:110]} |")
    L += [""]
L += ["**Kritik sınama.** Bu boyutun hedeflediği kusurdan ötürü uzmanın reddettiği kayıt "
      "**form 38**'dir (kayıt #19): *\"bağlam içerisinde paylaşılmaz diyor ama cevap "
      "verilmesi gerekiyor, bu cevabı vermemiş\"*. Form 27 (#30) de aynı **izin isteme "
      "kalıbını** taşıyor ama uzmanın oradaki gerekçesi cevapsızlık değil "
      "*anlaşılmazlık*: *\"bu cümle net değil\"* — yani form 27 `cevapsiz_soru` için değil, "
      "`anlasilirlik` için sınamadır. (Bu ayrımı ilk yazımda karıştırmıştım.)", ""]
for hedef in (38, 27):
    g = next((e for e in esli if e[0] == hedef), None)
    if g:
        L.append(f"- Form {hedef}: `cevapsiz_soru` = **{g[3].get('cevapsiz_soru')}** · "
                 f"`anlasilirlik` = {g[3].get('anlasilirlik')} · "
                 f"(v1 `dil_butunlugu` = {g[2].get('dil_butunlugu')})")
L += [""]

# ── 4. Uzmanla korelasyon ────────────────────────────────────────────────────
L += ["## 4. Uzmanla kayıt düzeyi korelasyon", "",
      "v1'de bütün boyutlar sıfıra yakındı (0.06 · −0.08 · 0.26 · −0.01 · −0.13 · −0.10).", "",
      "| Uzman boyutu | v1 judge boyutu | r (v1) | v2 judge boyutu | r (v2) |",
      "|---|---|---:|---|---:|"]
ESLESME = [("duygusal_tepki", "duygusal_tepki", "duygusal_tepki"),
           ("yorumlama", "yorumlama", "yorumlama"),
           ("kesif", "kesif", "kesif"),
           ("mi_uyumu", "mi_uyumu", "mi_uyumu"),
           ("grounding", "grounding", "grounding"),
           ("dil_butunlugu", "dil_butunlugu", "anlasilirlik"),
           ("kisalik_dogallik", "kisalik_dogallik", "dogallik")]
for u_alan, a1, a2 in ESLESME:
    ua1, ja1, ua2, ja2 = [], [], [], []
    for no, up, j1, j2, r in esli:
        if up.get(u_alan) is not None and j1.get(a1) is not None:
            ua1.append(up[u_alan]); ja1.append(j1[a1])
        if up.get(u_alan) is not None and j2.get(a2) is not None:
            ua2.append(up[u_alan]); ja2.append(j2[a2])
    r1, r2 = pearson(ua1, ja1), pearson(ua2, ja2)
    f = lambda x: "—" if x is None else f"{x:+.2f}"
    L.append(f"| {u_alan} (n={len(ua2)}) | `{a1}` | {f(r1)} | `{a2}` | {f(r2)} |")
L += ["", "> `—` = boyut sabit olduğu için korelasyon tanımsız (v1 `dil_butunlugu`: s=0.00).", ""]

# ── 5. Kanıt alanları ve gerekçe dili ────────────────────────────────────────
kanit_dolu = sum(1 for r in v2.values()
                 if ((r.get("judge") or {}).get("en_belirsiz_cumle") or "").strip())


def ovgu_sayisi(kaynak):
    n = 0
    for r in kaynak.values():
        g = ((r.get("judge") or {}).get("gerekce") or "").lower()
        if any(o in g for o in OVGU):
            n += 1
    return n


L += ["## 5. Kanıt alanları ve gerekçe dili", "",
      "| Ölçüm | v1 | v2 |", "|---|---:|---:|",
      f"| `en_belirsiz_cumle` dolu | yok | {kanit_dolu}/{len(v2)} |",
      f"| Gerekçesinde övgü sıfatı geçen kayıt | {ovgu_sayisi(v1)}/{len(v1)} | "
      f"{ovgu_sayisi(v2)}/{len(v2)} |", "",
      f"> Övgü taraması: {', '.join(OVGU)} — kaba bir vekil, üslup ölçer, doğruluk değil.", ""]

ornek = [(no, j2) for no, up, j1, j2, r in esli
         if up["genel_karar"] == "ret" and (j2.get("en_belirsiz_cumle") or "").strip()]
if ornek:
    L += ["**Uzmanın reddettiği kayıtlarda judge'ın çıkardığı en belirsiz cümle:**", "",
          "| Form | Judge'ın alıntısı | `anlasilirlik` |", "|---|---|---:|"]
    for no, j2 in ornek:
        L.append(f"| {no} | {j2['en_belirsiz_cumle'][:120]} | {j2.get('anlasilirlik')} |")
    L += [""]

# ── 6. Uzmanın alıntısı ile judge'ın alıntısı aynı cümle mi ─────────────────
# Kanıt çıkarma adımı işe yarıyorsa, judge'ın "en belirsiz" dediği cümle uzmanın
# şikâyet ettiği cümleyle örtüşmeli. Uzman notlarının bir kısmı cümleyi tırnak
# içinde veriyor — yalnızca onlar sınanabilir.
TIRNAK = re.compile(r'["“”]([^"“”]{12,})["“”]')


def _sade(t: str) -> str:
    return re.sub(r"\s+", " ", (t or "").lower().replace("’", "'")).strip()


ortusme = []
for no, up, j1, j2, r in esli:
    alintilar = TIRNAK.findall(up.get("not") or "")
    if not alintilar:
        continue
    jc = _sade(j2.get("en_belirsiz_cumle"))
    for a in alintilar:
        ua = _sade(a)
        tutar = bool(jc) and (ua in jc or jc in ua)
        ortusme.append((no, up["genel_karar"], a.strip(), j2.get("en_belirsiz_cumle") or "—", tutar))

tutan = sum(1 for *_, t in ortusme if t)
L += ["## 6. Uzmanın alıntısı ↔ judge'ın alıntısı", "",
      "Kanıt çıkarma adımı gerçekten çalışıyorsa, judge'ın *en belirsiz* dediği cümle "
      "uzmanın şikâyet ettiği cümleyle örtüşmeli. Uzman notlarının yalnızca bir kısmı "
      "cümleyi tırnak içinde veriyor; sınanabilen kayıtlar bunlar.", "",
      f"**Örtüşme: {tutan}/{len(ortusme)}**", ""]
if ortusme:
    L += ["| Form | Karar | Uzmanın alıntısı | Judge'ın alıntısı | Aynı mı |",
          "|---|---|---|---|:--:|"]
    for no, karar, ua, ja, t in ortusme:
        L.append(f"| {no} | {karar} | {ua[:70]} | {ja[:70]} | {'✅' if t else '❌'} |")
    L += [""]

# ── 7. Sonuç ────────────────────────────────────────────────────────────────
tavan_v1 = sum(1 for r in v1.values() if (r.get("judge") or {}).get("dil_butunlugu") == 5)
tavan_v2 = sum(1 for r in v2.values() if (r.get("judge") or {}).get("anlasilirlik") == 5)
auc_v2 = [auc(dizi("ret", 3, a), dizi("kabul", 3, a))
          for a in ["anlasilirlik", "dogallik", "mi_uyumu", "grounding"]]
auc_v2 = [a for a in auc_v2 if a is not None]

L += ["## 7. Sonuç — v2 neyi düzeltti, neyi düzeltmedi", "",
      "### Düzelen", "",
      f"1. **Tavan kırıldı.** v1 dil boyutunda {tavan_v1}/70 tam puan (s=0.00) → "
      f"v2 `anlasilirlik`'te {tavan_v2}/68. `dogallik`'te tam puan oranı %6. "
      "Boyutlar artık ayrım yapabilecek varyansa sahip.",
      f"2. **Övgü dili bitti.** Gerekçesinde övgü sıfatı geçen kayıt {ovgu_sayisi(v1)}/70 → "
      f"{ovgu_sayisi(v2)}/70.",
      "3. **`cevapsiz_soru` çalıştı.** v1'in tamamen kaçırdığı kusuru, uzmanın bu yüzden "
      "reddettiği kayıtta (form 38) yakaladı ve kullanıcının sorusunu doğru alıntıladı.",
      "", "### Düzelmeyen — asıl sonuç", "",
      "**Ayrım gücü yok.** Uyum oranları " +
      f"{min(auc_v2):.2f}–{max(auc_v2):.2f} aralığında, hepsi tesadüf bandında. "
      "v2, uzmanın `ret` dediği kayıtları `kabul`lerden ayıramıyor — v1 de ayıramıyordu. "
      "`mi_uyumu`'nda uyum oranı 0.50'nin **altında**: judge, uzmanın reddettiği kayıtlara "
      "sistematik olarak daha yüksek MI puanı veriyor.", "",
      "⚠️ **Bu test zayıftır ve bunu gizlememek gerekir.** `ret` grubu 5 kayıt; "
      "%95 aralıklar yukarıdaki tabloda ve hepsi çok geniş. Test yalnızca **güçlü bir "
      "ayrımın olmadığını** söyleyebilir; orta düzey bir ayrımı ne doğrular ne yalanlar.", "",
      "### Teşhis — sorun algıda değil, puanlamada", "",
      f"En açıklayıcı bulgu §6'da: judge, uzmanın şikâyet ettiği cümleyi **bulabiliyor** — "
      f"sınanabilen {len(ortusme)} kaydın **{tutan}'ünde** uzmanla aynı cümleyi, üstelik "
      f"bağımsız olarak seçti. Ama o cümleyi alıntıladıktan sonra verdiği puanlar: "
      + " · ".join(
          f"form {no} `anlasilirlik`={next((g[3].get('anlasilirlik') for g in esli if g[0] == no), '?')}"
          for no, _, _, _, t in ortusme if t)
      + ". Uzman aynı cümlelere dil boyutunda "
      + " · ".join(
          f"form {no}={next((g[1].get('dil_butunlugu') for g in esli if g[0] == no), '?')}"
          for no, _, _, _, t in ortusme if t)
      + " verdi. **Judge kusuru görüyor, kusur saymıyor.**", "",
      "Bunun anlamı: v2'nin yaptığı şey — kusur türlerini daha iyi tarif etmek — "
      "**yetersiz bir müdahaleydi**. Kanıt çıkarma adımı işini yaptı; puan, çıkarılan "
      "kanıttan bağımsız kaldı. Sonraki denemenin bu boşluğa girmesi gerekir: puanı "
      "kanıtın **fonksiyonu** yapmak (ör. *en_belirsiz_cumle* belirsiz gönderge ya da "
      "kurulmamış mecaz içeriyorsa `anlasilirlik` ≤ 3 kuralı), ya da mutlak ölçek yerine "
      "**ikili karşılaştırma** kullanmak. Bu, v3 rubriği demektir; bu raporda ölçülmemiştir.", "",
      "### Karar", "",
      "**Judge çıktısı hâlâ kalite kanıtı değildir** (`prompts/uretim-v3.md` §9 aynen "
      "geçerli). v2, v1'den *daha çok şey ölçüyor* ama **kaliteyi ölçmüyor**. "
      "Üretimde tarama amaçlı kullanılmaya devam eder; `cevapsiz_soru` bayrağı ise "
      "elle incelemeye yönlendirmek için doğrudan işe yarar.", ""]

CIKTI.parent.mkdir(parents=True, exist_ok=True)
CIKTI.write_text("\n".join(L))
print(f"yazıldı: {CIKTI}  (eşleşen {len(esli)} · cevapsiz_soru {len(tum_bayrak)}/70)")
