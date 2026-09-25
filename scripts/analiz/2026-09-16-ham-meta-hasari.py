#!/usr/bin/env python3
"""T76'nın üst sınırları kesin sayıya çevrildi — ve ikisi de UÇTA çıktı.

T76 `normalize.py`'de üç kusur ölçtü ama **gerçek hasarı ölçemedi**:
`data/seeds.jsonl` kanonik meta taşıyor, ham meta onaylı kaynak klasöründe ve
Kural 1 gereği sorulmadan okunmuyordu. ✅ Kullanıcı 2026-09-16'da **açıkça izin
verdi**; ham kampanya meta'sı okundu ve üst sınırlar kesin sayıya döndü.

⭐⭐ **Bulgu, iki kusurun UÇLARDA çıkması:**

  · İzi **OLAN** kusur (`egitim` → `belirtilmemis`) üst sınırın **TAMAMI**:
    80/80. Yani her `belirtilmemis` bir kayıp `İlkokul`du; alanın gerçekten
    boş olduğu **tek bir kayıt bile yok**.
  · İzi **OLMAYAN** kusur (`kullanim_suresi` → yanlış kova) **HİÇ ateşlememiş**:
    0/2240 — çünkü ham değerler zaten küçük harfle yazılmış.

➡️ *Üst sınırın sıkı olup olmadığı önceden bilinemez. «%3,6, muhtemelen abartı»
demek ile «izi yok, demek ki olmadı» demek aynı ölçüde temelsizdi — ve ikisi de
yanlış olurdu, ters yönlerde.*

⚠️ **Bu betiğin repo DIŞINDA bir girdisi var** — reponun tek örneği. Kaynak
dosyaların SHA256'sı ilan ediliyor; klasör erişilemezse rapor bunu yazar ve
sayı üretmez.

Girdi : <onaylı kaynak>/campaigns/*/total_output.jsonl (yalnızca `meta` alanı) ·
        src/normalize.py · configs/taxonomy.yaml · data/seeds.jsonl
Çıktı : reports/analiz/2026-09-16-ham-meta-hasari.md
Kullanım: uv run python scripts/analiz/2026-09-16-ham-meta-hasari.py
"""
# lower-muaf-dosya: 2026-09-16 öncesi davranış referans olarak duruyor (T77)
from __future__ import annotations

import collections
import hashlib
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-ham-meta-hasari.md"
TOHUM = KOK / "data/seeds.jsonl"
TOHUM_V2 = KOK / "data/seeds.v2.jsonl"
sys.path.insert(0, str(KOK / "src"))
import normalize as N  # noqa: E402
from tohum_guvenlik import tr_fold  # noqa: E402

EG = (("lisansüstü", "lisansustu"), ("yüksek lisans", "lisansustu"), ("mba", "lisansustu"),
      ("üniversite", "universite"), ("lisans", "universite"), ("lise", "lise"),
      ("ortaokul", "ortaokul"), ("ilkokul", "ilkokul"))


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


# --- 2026-09-16 ÖNCESİ davranış — referans, silinmez ---------------------------
def eski_egitim(raw: str) -> str:
    t = (raw or "").lower()
    for k, c in EG:
        if k in t:
            return c
    return "belirtilmemis"


def eski_sure(raw):
    if not raw:
        return "belirtilmemis"
    t = raw.lower()
    if "ay" in t and not re.search(r"\byıl|yil\b", t.split("ay")[0][-12:]):
        m = re.search(r"(\d+)\s*(?:-|–|\s)*\d*\s*ay", t)
        if m:
            return "0_6_ay" if int(m.group(1)) < 6 else "6_ay_1_yil"
    m = re.search(r"(\d+)", t)
    if not m:
        return "belirtilmemis"
    n = int(m.group(1))
    if "3 yıldan fazla" in t:
        return "3_10_yil"
    return ("0_6_ay" if n < 1 else "1_3_yil" if n <= 3 else
            "3_10_yil" if n <= 10 else "10_yil_ustu")


def eski_keyword(raw: str):
    low = (raw or "").lower()
    for keys, canon in N.TAX["stres_tipi"]["anahtar_kelime"]:
        if any(k in low for k in keys):
            return canon
    return None


# --- `_keyword` için denenen aday düzeltmeler — KARAR KAYDI --------------------
def _aday(raw: str, sinif: bool, sinir: bool, alt_cizgi: bool):
    low = tr_fold(raw or "") if sinif else (raw or "").lower()
    if alt_cizgi:
        low = low.replace("_", " ")
    for keys, canon in N.TAX["stres_tipi"]["anahtar_kelime"]:
        for k in keys:
            anahtar = tr_fold(k) if sinif else k
            if alt_cizgi:
                anahtar = anahtar.replace("_", " ")
            vurdu = (re.search(r"\b" + re.escape(anahtar), low) if sinir
                     else anahtar in low)
            if vurdu:
                return canon
    return None


ADAYLAR = [
    ("**eski** — düz `.lower()`, alt-dize", lambda s: eski_keyword(s)),
    ("① yalnız **i-sınıfı**", lambda s: _aday(s, True, False, False)),
    ("② yalnız **kelime başı**", lambda s: _aday(s, False, True, False)),
    ("③ i-sınıfı + kelime başı", lambda s: _aday(s, True, True, False)),
    ("④ ⭐ ③ + `_`→boşluk — **uygulanan**", lambda s: _aday(s, True, True, True)),
]


def ham_meta() -> tuple[list[tuple[str, dict]], list[tuple[str, str]]]:
    out, kaynak = [], []
    for kampanya, yol in N.CAMPAIGN_FILES.items():
        if not yol.exists():
            continue
        kaynak.append((kampanya, sha(yol)))
        for satir in yol.read_text(encoding="utf-8").split("\n"):
            if satir.strip():
                out.append((kampanya, json.loads(satir)["meta"]))
    return out, kaynak


def main() -> int:
    ham, kaynak = ham_meta()
    L: list[str] = []
    L += ["# Ham meta okundu — üst sınırların ikisi de UÇTA çıktı", "",
          f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
          f"**Girdi:** `src/normalize.py` SHA256 `{sha(KOK/'src/normalize.py')}` "
          f"(fonksiyonlar **çağrılıyor**)  ",
          f"**Girdi:** `configs/taxonomy.yaml` SHA256 `{sha(KOK/'configs/taxonomy.yaml')}`  ",
          f"**Girdi:** `data/seeds.jsonl` SHA256 `{sha(TOHUM)}`  ",
          "**Girdi (repo DIŞI):** onaylı kaynak korpusu — ⚠️ **kullanıcı 2026-09-16'da "
          "açıkça izin verdi** (Kural 1). ⧉ işareti *«repo dışı: SHA kayıtlı, "
          "burada doğrulanamaz»* demektir:  "]
    if not kaynak:
        L += ["", "⛔ **Kaynak klasör erişilemedi — bu rapor sayı üretmiyor.**", ""]
        RAPOR.write_text("\n".join(L) + "\n", encoding="utf-8")
        print("⛔ kaynak erişilemedi")
        return 1
    L += [f"· ⧉ `campaigns/{k}/total_output.jsonl` SHA256 `{h}`  " for k, h in kaynak]
    L += ["", f"**{len(ham)}** ham kayıt · yalnızca `meta` alanı okundu.", "", "---", "",
          "## Neden", "",
          "T76 üç kusur ölçtü ama **gerçek hasarı ölçemedi**: `data/seeds.jsonl`",
          "**kanonik** meta taşıyor, ham meta onaylı kaynak klasöründeydi. ⚠️ Bu betiğin",
          "repo **dışında** bir girdisi var — reponun **tek** örneği — ve kaynak",
          "dosyaların SHA256'sı bu yüzden ilan ediliyor.", "", "---", ""]

    # --- §1 iki kusur, iki uç --------------------------------------------------
    eg_fark = [(k, m) for k, m in ham
               if eski_egitim(m.get("egitim_durumu")) != N.norm_egitim(m.get("egitim_durumu"))]
    su_fark = [(k, m) for k, m in ham
               if eski_sure(m.get("kullanim_suresi")) != N.norm_sure(m.get("kullanim_suresi"))]
    # ⛔ Üst sınır HAM veriden ve ESKİ koddan türetiliyor, tohum dosyasından DEĞİL:
    #    tohum dosyası düzeltilince oradaki sayı sıfırlanır ve T76'nın üst sınırı
    #    raporda görünmez olurdu (T73'te aynı tuzak, aynı çözüm).
    ust_eg = sum(1 for _, m in ham if eski_egitim(m.get("egitim_durumu")) == "belirtilmemis")
    tohumlar = [json.loads(x) for x in TOHUM.read_text(encoding="utf-8").split("\n") if x.strip()]
    tohum_geri = sum(1 for t in tohumlar if t["meta"].get("egitim") == "belirtilmemis")

    L += ["## 1. ⭐⭐ İki kusur, iki uç — üst sınırın sıkılığı önceden bilinemezmiş", "",
          "| kusur | T76'daki üst sınır | **gerçek** | |", "|---|---|---:|---|",
          f"| `egitim` → `belirtilmemis` (⚠️ **izi var**) | ≤ **{ust_eg}** | **{len(eg_fark)}** | "
          f"{'⛔ **üst sınırın TAMAMI**' if len(eg_fark) == ust_eg else 'kısmi'} |",
          f"| `kullanim_suresi` → yanlış kova (⛔ **izi yok**) | ⛔ *üst sınır yoktu* | "
          f"**{len(su_fark)}** | {'✅ **hiç ateşlememiş**' if not su_fark else '⛔'} |", "",
          "➡️⭐⭐ *İzi **olan** kusur üst sınırın **tamamını** doldurmuş: her*",
          f"*`belirtilmemis` bir kayıp değerdi, alanın gerçekten boş olduğu **tek bir***",
          "***kayıt bile yok**. İzi **olmayan** kusur ise **hiç** gerçekleşmemiş.*", "",
          "⇒ *«%3,6, muhtemelen abartı»* demek ile *«izi yok, demek ki olmadı»* demek",
          "**aynı ölçüde temelsizdi** — ve ikisi de yanlış olurdu, **ters yönlerde**.", "",
          "---", ""]

    # --- §2 egitim -------------------------------------------------------------
    L += ["## 2. `egitim` — 80 kayıt, tek bir değerden", "",
          "| ham değer | eski | doğru | kayıt |", "|---|---|---|---:|"]
    for (hamd, e, y), n in collections.Counter(
            (m.get("egitim_durumu"), eski_egitim(m.get("egitim_durumu")),
             N.norm_egitim(m.get("egitim_durumu"))) for _, m in eg_fark).most_common():
        L.append(f"| `{hamd}` | ⛔ `{e}` | ✅ `{y}` | **{n}** |")
    L += ["", "| kampanya | etkilenen |", "|---|---:|"]
    for kmp, n in sorted(collections.Counter(k for k, _ in eg_fark).items()):
        toplam = sum(1 for k, _ in ham if k == kmp)
        L.append(f"| `{kmp}` | {n}/{toplam} (%{100*n/toplam:.1f}) |")
    L += ["",
          "⚠️ **Kaybedilen değer rastgele değil:** `ilkokul` taksonomideki **en düşük**",
          "eğitim düzeyi. ⇒ Üretim eğitim düzeyine göre kayıt üslubu ayarlıyorsa (T25 /",
          "K42 register ekseni), bu 80 tohum **en düşük register dilimini temsil eden**",
          "**dilim**di ve `belirtilmemis` olarak üretime girdi. ⛔ Etkisi bu betikle",
          "ölçülmedi: üretilmiş kayıtlarda register ayrı bir ölçüm.", "", "---", ""]

    # --- §3 kullanim_suresi ----------------------------------------------------
    ham_sure = collections.Counter(str(m.get("kullanim_suresi")) for _, m in ham)
    buyuk_harfli = [v for v in ham_sure if v != v.lower()]
    L += ["## 3. `kullanim_suresi` — kusur gerçek, ateşleme sıfır", "",
          f"Ham veride **{len(ham_sure)}** ayrık süre değeri var ve ⭐ "
          f"**{len(buyuk_harfli)}** tanesi büyük harf içeriyor"
          + (": " + ", ".join(f"`{v}`" for v in sorted(buyuk_harfli)[:6]) if buyuk_harfli
             else " — hepsi zaten küçük harfle yazılmış.") + "", "",
          "⇒ `norm_sure`'ün *«yanlış kova»* kusuru **hiç tetiklenmedi**. ⚠️ Bu kapıyı",
          "masum yapmaz: kusur duruyordu ve tetiklenmemesinin sebebi **kaynağın yazım**",
          "**alışkanlığı**ydı — T73'te `scan_forbidden` için yazılan cümlenin aynısı:",
          "*bir kapının güvenliği girdinin bugünkü huyuna bağlıysa ölçülmüş değil,*",
          "*ödünç alınmıştır.* ✅ Artık ölçülmüş: kusur kapatıldı **ve** bedelinin sıfır",
          "olduğu gösterildi.", "", "---", ""]

    # --- §4 _keyword karar kaydı ----------------------------------------------
    sts = [(m.get("stress_type") or "") for _, m in ham]
    L += ["## 4. ⭐⭐ `_keyword` kararı — dört aday, ham veriye karşı", "",
          "T76 `_keyword`'ü **bilerek düzeltmemişti**: i-sınıfı gerileme üretiyordu ve",
          "etkisi ancak ham meta'ya karşı ölçülebilirdi. ⇒ Dört aday ölçüldü.", "",
          "| aday | değişen kayıt | düzeltme | ⛔ gerileme |", "|---|---:|---:|---:|"]
    en_iyi = None
    for ad, f in ADAYLAR[1:]:
        fark = [(s, eski_keyword(s), f(s)) for s in sts if eski_keyword(s) != f(s)]
        duzelt = sum(1 for _, e, y in fark if e is None and y is not None)
        geri = sum(1 for _, e, y in fark if e is not None)
        L.append(f"| {ad} | {len(fark)} | ✅ **{duzelt}** | "
                 f"{'✅ **0**' if geri == 0 else f'⛔ **{geri}**'} |")
        if geri == 0 and (en_iyi is None or duzelt > en_iyi[1]):
            en_iyi = (ad, duzelt)
    L += ["",
          "**Gerilemelerin sebepleri — her biri ayrı bir ders:**", "",
          "| aday | gerileme | sebep |", "|---|---|---|",
          "| ① i-sınıfı | `Aile çatışması stresi` → `is_stresi` | `çatışması` → "
          "`çatişmasi`, içinde **`iş`** var. ⇒ *Sınıf genişletmek, kısa alt-dize "
          "eşleşmesinde hemen çakışır* |",
          "| ②③ kelime başı | `physical_fatigue` → `None` | ⛔ `_` bir **kelime "
          "karakteri**: `fatigue`'ün önünde `\\b` yok. ⇒ *`snake_case` bir sözcük "
          "değil, iki sözcüktür ve regex bunu bilmez* |", "",
          f"⭐ **Uygulanan: ④** — i-sınıfı + `_`→boşluk + kelime başı. "
          f"Ham {len(sts)} kayıtta **{en_iyi[1] if en_iyi else 0} düzeltme, 0 gerileme**.", "",
          "⛔ **`.strip()` ve `\\w*` bilerek EKLENMEDİ:** `\"eş \"` anahtarının sondaki",
          "boşluğu kasıtlı (`eşya`/`eşit` eşleşmesin diye) ve ek serbestliği `\\b`'den",
          "zaten geliyor (`\\biş` → `işim` ✅, `girişimci` ⛔). ➡️ *Bir kusuru kapatırken*",
          "*anlambilimi genişletmemek ayrı bir iştir; ölçüm iyileşmeyi gösterir ama*",
          "*genişlemeyi göstermez.*", "", "---", ""]

    # --- §5 ⭐⭐ T60 TEKRARLADI -------------------------------------------------
    ulasan = [s2 for s2 in sts if N._exact("stres_tipi", s2) is None]
    alan_fark = [s2 for s2 in ulasan if eski_keyword(s2) != N._keyword("stres_tipi", s2)]
    L += ["## 5. ⛔⛔ **AMA ALAN DÜZEYİNDE ETKİ SIFIR — T60 tekrarladı**", "",
          "§4'teki **20 düzeltme** bir **fonksiyon düzeyi** sayısıdır. Alan düzeyinde",
          "ölçülünce **0** çıkıyor ve sebebi `normalize()`'ın kısa devre zinciri:", "",
          "```python",
          'out["stres_tipi"] = (_exact(...) or _keyword(...) or ("yok" if ... else None))',
          "```", "",
          "| | kayıt |", "|---|---:|",
          f"| ham kayıt | {len(sts)} |",
          f"| ⛔ `_exact` zaten yakalıyor (⇒ `_keyword` **hiç koşmuyor**) | "
          f"**{len(sts)-len(ulasan)}** |",
          f"| `_keyword`'e ULAŞAN | **{len(ulasan)}** (%{100*len(ulasan)/len(sts):.1f}) |",
          f"| ⭐ bunlar içinde **etiketi değişen** | **{len(alan_fark)}** |", "",
          "⭐⭐ **Sebep keskin:** kasing kusurunun vurduğu 20 kayıt (`İş stresi` — Türkçe,",
          "karışık büyük harf) tam olarak `_exact`'in **zaten kapsadığı** kayıtlar;",
          "`_keyword`'e ulaşan her şey İngilizce `snake_case` (`ambivalence_contradiction`,",
          "`boundary_pressure`…) ve içinde **tek bir Türkçe harf yok**.", "",
          "➡️⭐⭐ *Kusurun gerçekleşmesi için İKİ koşul birden gerekiyordu — metin Türkçe*",
          "*olacak VE `_exact` kapsamayacak — ve bu korpusta ikisi **hiç bir arada***",
          "***oluşmadı**. Kusur gerçekti, erişilemezdi.*", "",
          "⛔⛔ **Ve bu, T60'ın dersinin ikinci kez çıkması:** *bir sayı, RAPORLANDIĞI*",
          "*düzeyde ölçülmelidir.* T60'da aynı sızıntı bayrak düzeyinde **%40**, kapı",
          "düzeyinde **%0**'dı. Burada aynı düzeltme fonksiyon düzeyinde **20**, alan",
          "düzeyinde **0**. ⚠️ Ben de §4'ü ilkin *«20 düzeltme»* diye yazdım ve tohum",
          "dosyası yeniden üretilince farkın **çıkmadığını** görünce düzelttim.", "",
          "⚠️ Düzeltme yine de **doğru**: alt-dize kusuru (`girişimci` → `is_stresi`)",
          "serbest metinli Türkçe bir `stress_type` değeri geldiği gün ateşlerdi ve",
          "bugün ateşlememesinin sebebi yine **kaynağın yazım alışkanlığı**.", "", "---", ""]

    # --- §6 tohum havuzu -------------------------------------------------------
    v2 = ([json.loads(x) for x in TOHUM_V2.read_text(encoding="utf-8").split("\n") if x.strip()]
          if TOHUM_V2.exists() else [])
    # ⛔ *Adı geçen* değil, **hash'ini İLAN EDEN** raporlar sayılıyor: ilk sayım
    #    gevşekti (16) ve gevşek sayı iddiayı olduğundan büyük gösteriyordu.
    v1_hash = hashlib.sha256(TOHUM.read_bytes()).hexdigest()
    atif = sorted(y.name for y in (KOK / "reports/analiz").glob("*.md")
                  if (v1_hash in (t := y.read_text(encoding="utf-8"))
                      or v1_hash[:16] in t)
                  and y.name != f"{TARIH}-ham-meta-hasari.md")
    L += ["## 6. ⛔⭐⭐ Tohum havuzu YENİDEN ÜRETİLDİ, sonra GERİ ALINDI — ve sebebi bir ders",
          "",
          "Düzeltilmiş kodla `data/seeds.jsonl` yeniden üretildi (**80/2240** kayıt",
          "değişiyor, yalnızca `meta.egitim`). ⛔ **Ama üzerine yazmak yanlıştı ve bunu",
          "gösteren şey ilan edilen SHA denetimi oldu:**", "",
          f"⛔ **{len(atif)} geçmiş rapor** `data/seeds.jsonl`'ın **hash'ini ilan ediyor**, ve",
          "bunların bir kısmının **çıktısı DONDURULMUŞ** (`data/plan/v3-parti*.jsonl`,",
          "`v4-parti1.jsonl` — üretime girmiş örneklem planları). Onları yeniden koşmak",
          "**tarihi yeniden yazmak** olurdu; koşmamak ise kaynak dosya değiştiği için",
          "kayıt zincirini **doğrulanamaz** bırakırdı.", ""]
    L += [f"· `{a}`  " for a in atif] + ["",
          "✅ **Yapılan:** `data/seeds.jsonl` **bayt bayt geri alındı**; düzeltilmiş havuz",
          f"**`data/seeds.v2.jsonl`** olarak yazıldı ({len(v2)} tohum). ⇒ Geçmiş",
          "raporların ilan ettiği hash tutmaya devam ediyor, düzeltme de kayboldu değil.", "",
          "➡️⭐⭐ *Ders: **değişmezlik ilan edilen bir özellik değil, KEŞFEDİLEN bir***",
          "***özelliktir.** `datasets/` için Kural 4 bunu açıkça yazıyor; `data/seeds.jsonl`",
          "*için hiçbir kural yazmıyordu — ama hash'ini ilan eden rapor sayısı onun*",
          "*fiilen değişmez olduğunu söylüyordu. Bir artefaktın dokunulabilir olup*",
          "*olmadığını anlamanın yolu kuralı okumak değil, **kim hash'ine atıf veriyor***",
          "***diye saymaktır.*** ⚠️ Ve bunu bana kural değil **denetim** söyledi:",
          "`ilan-edilen-sha-denetimi` üzerine yazdıktan sonra `⛔ tutmuyor` dedi.", "",
          "| | |", "|---|---:|",
          f"| `data/seeds.jsonl` (v1, **dokunulmadı**) | {len(tohumlar)} tohum |",
          f"| `data/seeds.v2.jsonl` (**düzeltilmiş**) | {len(v2)} tohum |",
          f"| değişen kayıt | **{len(eg_fark)}** (%{100*len(eg_fark)/len(tohumlar):.1f}) |",
          "| değişen alan | yalnızca `meta.egitim` |",
          "| kaybolan / yeni `seed_id` | **0** / **0** |", "",
          "⭐ **Kayıt izleri korundu:** `seed_id = sha256(source_id)[:16]` — meta'dan",
          "**türemiyor**. ⚠️ Bu **önceden** kontrol edildi; türeseydi yeniden üretim",
          "`datasets/*`'ın `source_ids` bağlarını kırardı.", "",
          "⛔ **Hangi havuzun kullanılacağı bir KARAR:** Faz 4 üretimi `seeds.v2` ile",
          "koşmalı; ⚠️ ama o zaman v1'den üretilmiş kayıtlarla v2'den üretilenler aynı",
          "sette karışır ve bu **kayıtta görünmüyor**. `plan.md`'ye açık kalem.", "",
          "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ **v1/v2 karışımı kayıtta görünmüyor** | hangi kaydın hangi havuzdan "
          "üretildiği `gen_meta`'da yazmıyor; `seeds.v2` kullanılmaya başlanırsa bu "
          "**önce** çözülmeli |",
          "| ⛔ **Üretilmiş kayıtlara etkisi** | 80 tohum `belirtilmemis` eğitimle üretime "
          "girdi; bunun üretilen metnin **register**'ine ne yaptığı ayrı bir ölçüm ve "
          "**yapılmadı** (T25 / K42 ekseni) |",
          "| ⛔ **Aksan düşürme sınıfı** | hâlâ açık: `Universite` yazımı `belirtilmemis` "
          "verir. Ham veride geçmiyor (ölçüldü) ama kapatılmadı |",
          "| ⚠️ **Repo dışı girdi** | bu betik reponun **tek** dış bağımlılığı; kaynak "
          "klasör erişilemezse rapor sayı üretmez ve bunu yazar |",
          "| ⚠️ Yalnızca **üç alan** | `egitim`, `kullanim_suresi`, `stres_tipi`. "
          "`_exact`/`_prefix`/`_contains` hiç normalizasyon kullanmıyor ve **sınanmadı** |",
          "| ⛔ *«Bugün ateşlemiyor»* ≠ *«güvenli»* | hem `norm_sure` hem `_keyword` "
          "kusurları gerçekti ve tetiklenmemelerinin sebebi **kaynağın yazım "
          "alışkanlığı**ydı — ödünç alınmış güvenlik (T73) |", ""]

    RAPOR.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print(f"   ham kayıt {len(ham)} · egitim farkı {len(eg_fark)} (üst sınır {ust_eg}) · "
          f"kullanim_suresi farkı {len(su_fark)}")
    print(f"   _keyword: uygulanan aday ④ · düzeltme {en_iyi[1] if en_iyi else 0} · gerileme 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
