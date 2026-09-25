#!/usr/bin/env python3
"""Register etkisi soruldu — cevap SIFIR, ama sebebi soruyu değiştiriyor.

T77 şunu açık bırakmıştı: kaybedilen 80 `ilkokul` etiketi üretilen metnin
**register**'ine ne yaptı? ⭐⭐ Cevap: **hiçbir şey, çünkü `egitim` üretim
hattına HİÇ ulaşmıyor.** Örneklem planı satırlarında yok, üretim talimatında
geçmiyor, ve `normalize.py` dışında **hiçbir kod onu okumuyor**. `register`
bağımsız bir **kota** alanı (§3a); eğitim düzeyinden türetilmiyor.

⛔ Bu bir rahatlama değil, daha kötü bir soru: **`egitim` şemada, taksonomide
ve 2240 tohumda duruyor ve hiçbir tüketicisi yok.** ⇒ *Kaybının ölçülememesi
kusurun küçüklüğünden değil, alanın HİÇ KULLANILMAMASINDAN geliyor.*

⭐ Bu yüzden soru genelleştiriliyor: `SeedMeta`'nın **her** alanı için, o alanı
okuyan bir tüketici var mı? ⚠️ Ölçüm dizgeye dayalı ve sınırları §4'te yazılı —
`egitim` araması ilk denemede `egitim_ozeti`'ni (EĞİTİM KOŞUSU özeti) yakaladı
ve o bir eğitim DÜZEYİ tüketicisi değil.

Girdi : src/schemas.py · data/seeds.v2.jsonl · data/plan/*.jsonl ·
        prompts/uretim-v*.md · src/*.py · scripts/analiz/*.py · configs/*.yaml
Çıktı : reports/analiz/2026-09-16-tohum-alani-tuketimi.md
Kullanım: uv run python scripts/analiz/2026-09-16-tohum-alani-tuketimi.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-tohum-alani-tuketimi.md"
TOHUM_V2 = KOK / "data/seeds.v2.jsonl"
TOHUM_V1 = KOK / "data/seeds.jsonl"
SEMA = KOK / "src/schemas.py"
# ⛔ Alanı YAZAN dosya tüketici sayılmaz; yoksa her alan kendi kendini tüketirdi.
YAZAN = {"src/normalize.py", "src/schemas.py"}
# ⛔ Elle okunup dışlanan yanlış pozitifler — **ilan ediliyor**, gizlenmiyor.
YANLIS_POZITIF = {
    ("egitim", "scripts/analiz/2026-09-15-f4-kapsam-raporu.py"),  # eğitim KOŞUSU özeti
}

# ⭐⭐ ELLE OKUMA (Kural 6: bu bizim okumamız, ölçüm değil).
# Ne ad eşleşmesi ne değer eşleşmesi doğru cevabı veriyor (§3): biri yeniden
# adlandırmayı kaçırıyor, öteki rastlantı üretiyor. Örneklem ve güvenlik
# betikleri elle okunup tohum meta'sından GERÇEKTEN okudukları alanlar yazıldı.
ELLE = {
    "senaryo": "v3-ornekleme · v4-parti1-plan · uzman-ornekleme",
    "yas_grubu": "v3-ornekleme · v4-parti1-plan",
    "risk_seviyesi": "v3-ornekleme · uzman-ornekleme",
    "bagimlilik_turu": "v4-parti1-plan",
    "notlar": "tohum_guvenlik.py (`notlar.esdurumlar` — K76)",
}


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def sema_alanlari() -> list[str]:
    """`SeedMeta`'nın alanları — şemadan okunur, elle yazılmaz."""
    metin = SEMA.read_text(encoding="utf-8")
    govde = metin[metin.index("class SeedMeta(BaseModel):"):]
    govde = govde[:govde.index("\n\n\n")] if "\n\n\n" in govde else govde
    return [m.group(1) for m in re.finditer(r"^    ([a-z_]+):", govde, re.M)]


def kod_tuketicileri(alan: str) -> tuple[list[str], list[str]]:
    """⭐⭐ İKİ SINIF döner: **hat** (boru hattı) ve **denetim**.

    ⛔ Ayrım zorunlu: bir alanı yalnızca bir ÖLÇÜM betiği okuyorsa o alan
    *tüketilmiyor* demektir — doğruluğu boru hattında hiç sınanmaz. İlk sürüm
    ikisini karıştırdı ve `egitim` için **4 tüketici** saydı; üçü bugünün kendi
    denetimleriydi, biri (`f4-kapsam-raporu.py`) ⛔ **yanlış pozitif**: oradaki
    `egitim_ozeti()` bir **eğitim KOŞUSU** özeti (val loss, tepe bellek),
    eğitim **düzeyi** tüketicisi değil.

    ⚠️ Yanlış pozitifi dizge ayıramaz; elle okundu ve aşağıda **ilan edilerek**
    dışlanıyor — gizlice değil.
    """
    desen = re.compile(rf"""["']{re.escape(alan)}["']""")
    hat, denetim = [], []
    for kok in ("src", "scripts/analiz", "configs"):
        for q in sorted((KOK / kok).rglob("*")):
            if q.suffix not in (".py", ".yaml", ".yml") or not q.is_file():
                continue
            rel = str(q.relative_to(KOK))
            if rel in YAZAN or rel == str(Path(__file__).relative_to(KOK)):
                continue
            if (alan, rel) in YANLIS_POZITIF:
                continue
            if desen.search(q.read_text(encoding="utf-8", errors="ignore")):
                (denetim if rel.startswith("scripts/analiz/") else hat).append(rel)
    return hat, denetim


def plan_satirlari() -> list[dict]:
    out = []
    for q in sorted((KOK / "data/plan").glob("*.jsonl")):
        for satir in q.read_text(encoding="utf-8").split("\n"):
            if satir.strip():
                out.append(json.loads(satir))
    return out


def plan_eslemesi(alanlar: list[str], planlar: list[dict],
                  tohum: dict) -> dict[str, tuple[str, int, int]]:
    """⭐⭐ Alan adı DEĞİL, DEĞER eşleşmesi.

    ⛔ Örneklem planı alanları **yeniden adlandırıyor** (`bagimlilik_turu` →
    `tur`, `yas_grubu` → `yas`), bu yüzden ad araması yanlış negatif verir —
    ilk sürüm tam bunu yaptı ve *«12/16 alanın tüketicisi yok»* dedi. Bunun
    yerine her plan satırı `seed_id` ile tohuma bağlanıp **hangi plan
    anahtarının hangi şema alanıyla aynı değeri taşıdığı** sayılıyor.

    Dönen: alan -> (plan anahtarı, eşleşen satır, karşılaştırılabilir satır).
    ⚠️ Eşik yok: oran raporda yazılıyor ve okur karar veriyor.
    """
    out: dict[str, tuple[str, int, int]] = {}
    anahtarlar = sorted({k for r in planlar for k in r})
    for alan in alanlar:
        en_iyi = ("—", 0, 0)
        for k in anahtarlar:
            esit = toplam = 0
            for r in planlar:
                t = tohum.get(r.get("seed_id"))
                if not t or k not in r:
                    continue
                tv, pv = t["meta"].get(alan), r[k]
                if tv is None or pv is None or not isinstance(pv, str):
                    continue
                toplam += 1
                esit += (str(tv) == str(pv))
            if toplam and esit > en_iyi[1]:
                en_iyi = (k, esit, toplam)
        out[alan] = en_iyi
    return out


def talimatta(alan: str) -> list[str]:
    out = []
    for p in sorted((KOK / "prompts").glob("uretim-v*.md")):
        if re.search(rf"\b{re.escape(alan)}\b", p.read_text(encoding="utf-8")):
            out.append(p.name)
    return out


def main() -> int:
    alanlar = sema_alanlari()
    v2 = {json.loads(l)["seed_id"]: json.loads(l)
          for l in TOHUM_V2.read_text(encoding="utf-8").split("\n") if l.strip()}
    planlar = plan_satirlari()
    ilkokul = {sid for sid, s in v2.items() if s["meta"].get("egitim") == "ilkokul"}
    kullanilan: set[str] = set()
    plan_satir = []
    for p in sorted((KOK / "data/plan").glob("*.jsonl")):
        for satir in p.read_text(encoding="utf-8").split("\n"):
            if not satir.strip():
                continue
            r = json.loads(satir)
            if r.get("seed_id"):
                kullanilan.add(r["seed_id"])
                if r["seed_id"] in ilkokul:
                    plan_satir.append((p.name, r))

    L: list[str] = []
    L += ["# Register etkisi sıfır — ama sebebi soruyu değiştiriyor", "",
          f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
          f"**Girdi:** `src/schemas.py` SHA256 `{sha(SEMA)}`  ",
          f"**Girdi:** `data/seeds.v2.jsonl` SHA256 `{sha(TOHUM_V2)}`  ",
          f"**Girdi:** `data/seeds.jsonl` SHA256 `{sha(TOHUM_V1)}`  ",
          f"**Girdi:** `data/plan/*.jsonl` · `prompts/uretim-v*.md` · `src/*.py` · "
          f"`scripts/analiz/*.py` · `configs/*.yaml`", "", "---", "", "## Soru", "",
          "T77 şunu açık bırakmıştı: kaybedilen **80** `ilkokul` etiketi üretilen metnin",
          "**register**'ine ne yaptı? (T25 · K42 ekseni)", "", "---", ""]

    # --- §1 maruziyet ----------------------------------------------------------
    L += ["## 1. Önce maruziyet — 80 tohumun kaçı üretime girdi", "",
          "| | |", "|---|---:|",
          f"| `egitim=ilkokul` tohum (v2) | **{len(ilkokul)}** |",
          f"| üretim planlarına giren tohum (toplam) | **{len(kullanilan)}** |",
          f"| ⭐ bunlardan `ilkokul` olanı | **{len(kullanilan & ilkokul)}** |", "",
          "| plan | sıra | `register` | `bicim` | tohum `profil` |", "|---|---:|---|---|---|"]
    for ad, r in plan_satir:
        L.append(f"| `{ad}` | {r.get('sira')} | `{r.get('register')}` | "
                 f"`{r.get('bicim')}` | `{v2[r['seed_id']]['meta'].get('profil')}` |")
    duzgun = sum(1 for _, r in plan_satir if r.get("register") == "duzgun")
    kotali = [r for _, r in plan_satir if r.get("register")]
    L += ["",
          f"⚠️ **{duzgun}/{len(kotali)}** kotalı kayıt `duzgun` register aldı. ⛔ **Bu bir "
          "desen DEĞİL:** v4'ün `bozuk` kotası ~%25 ve n={n}; hepsinin `duzgun` çıkma "
          "olasılığı ≈ **%{p:.0f}** — yani tamamen olağan. ➡️ *Küçük bir sayıda desen "
          "aramak, ölçüm değil beklenti okumaktır.*".format(
              n=len(kotali), p=100 * (0.75 ** len(kotali)) if kotali else 0), "", "---", ""]

    # --- §2 egitim hattı -------------------------------------------------------
    eg_hat, eg_den = kod_tuketicileri("egitim")
    esleme = plan_eslemesi(alanlar, planlar, v2)
    eg_plan = esleme["egitim"][1] > 0
    eg_talimat = talimatta("egitim")
    L += ["## 2. ⭐⭐ Asıl cevap: `egitim` üretim hattına **hiç ulaşmıyor**", "",
          "| Aşama | `egitim` var mı |", "|---|---|",
          f"| örneklem planı satırı (`data/plan/*.jsonl`) — **değer eşleşmesiyle** | "
          f"{'✅ var' if eg_plan else '⛔ **YOK** (hiçbir plan anahtarı taşımıyor)'} |",
          f"| üretim talimatı (`prompts/uretim-v*.md`) | "
          + (", ".join(f"`{x}`" for x in eg_talimat) if eg_talimat else "⛔ **geçmiyor**")
          + " |",
          f"| ⭐ **boru hattı** kodu (`src/`, `configs/`) | "
          + (", ".join(f"`{x}`" for x in eg_hat) if eg_hat else "⛔ **okuyan YOK**") + " |",
          f"| yalnızca **denetim** betikleri | "
          + (", ".join(f"`{x}`" for x in eg_den) if eg_den else "—")
          + " ⚠️ *hepsi bugünkü ölçümler* |",
          "", "⇒ **Register etkisi: yapısal olarak SIFIR.** `register` bağımsız bir",
          "**kota** alanı (`prompts/uretim-v4.md` §3a) ve eğitim düzeyinden",
          "**türetilmiyor**.", "",
          "⛔ Bu bir rahatlama değil, **daha kötü bir soru**: `egitim` `SeedMeta`'da,",
          "`configs/taxonomy.yaml`'da (6 kanonik değer) ve 2240 tohumun hepsinde duruyor",
          "— ve **hiçbir tüketicisi yok**. ➡️ *Kaybının ölçülememesi kusurun*",
          "*küçüklüğünden değil, alanın HİÇ KULLANILMAMASINDAN geliyor.*", "",
          "⚠️ İlk arama `egitim`i `scripts/analiz/2026-09-15-f4-kapsam-raporu.py`'de",
          "buldu — ama oradaki `egitim_ozeti()` bir **eğitim KOŞUSU** özeti (val loss,",
          "tepe bellek), eğitim **düzeyi** tüketicisi değil. ⛔ Dizgeye dayalı ölçümün",
          "ilk cevabı yanlıştı ve elle okunmadan düzelmezdi.", "", "---", ""]

    # --- §3 genelleme ----------------------------------------------------------
    L += ["## 3. ⭐⭐ Soru genelleşti — ve ÖLÇMENİN KENDİSİ sorun çıkardı", "",
          f"`SeedMeta` **{len(alanlar)}** alan ilan ediyor. *«Bu alan tüketiliyor mu»*",
          "sorusu mekanik olarak **iki** yoldan sorulabilir ve ⛔ **ikisi de yanlış**:", "",
          "| yöntem | kaçırdığı | uydurduğu |", "|---|---|---|",
          "| **ad eşleşmesi** (`\"alan\"` ara) | ⛔ plan alanları **yeniden adlandırıyor** "
          "(`bagimlilik_turu` → `tur`): yanlış negatif | `egitim` için "
          "`egitim_ozeti()`'ni yakaladı — o bir **eğitim KOŞUSU** özeti |",
          "| **değer eşleşmesi** (`seed_id` ile bağla) | ⛔ **sözcük dağarcığı** değişince "
          "kaçırıyor: `plan.motivasyon`=`ic` ↔ `tohum.motivasyon`=`ic_motivasyon` | "
          "⛔ rastlantı: `risk_seviyesi` ↔ `bicim` **9/40** çünkü ikisinde de `orta` var |",
          "", "➡️⭐⭐ *«Bu alan kullanılıyor mu» sorusunun MEKANİK bir cevabı yok. Ad*",
          "*eşleşmesi yeniden adlandırmayı, değer eşleşmesi yeniden sözcüklendirmeyi*",
          "*göremez; ve değer eşleşmesi eşiksiz kullanıldığında ortak bir değer*",
          "*(`orta`) iki ilgisiz alanı akraba gösterir.* ⇒ Üçüncü sütun **elle okundu**",
          "(Kural 6) ve raporda **kaynağıyla** yazılıyor.", "",
          "| alan | ad eşleşmesi | değer eşleşmesi | ⭐ **elle okuma** | |",
          "|---|---|---|---|---|"]
    olu = []
    for a in alanlar:
        k, esit, toplam = esleme[a]
        hat, den = kod_tuketicileri(a)
        ad_var = bool(talimatta(a)) or bool(hat)
        deger = f"`{k}` {esit}/{toplam}" if esit else "—"
        elle = ELLE.get(a)
        if not elle:
            olu.append(a)
        L.append(f"| `{a}` | {'✅' if ad_var else '—'} | {deger} | "
                 + (f"✅ {elle}" if elle else "⛔ **okuyan yok**") + " | "
                 + ("⛔" if not elle else "✅") + " |")
    L += ["",
          f"⛔ **{len(olu)}/{len(alanlar)} alanı boru hattında hiçbir şey okumuyor:** "
          + ", ".join(f"`{a}`" for a in olu) + ".", "",
          "⛔⭐ **Ve tabloda bir tuzak var:** örneklem planında `motivasyon` adında bir",
          "anahtar **var** ama tohumunkiyle **aynı şey değil** — planınki `ic`/`aile_baskisi`",
          "sözcük dağarcığını, tohumunki `ic_motivasyon`/`tetikleyici_olay`'ı kullanıyor ve",
          "plan betikleri tohumun alanını **hiç okumuyor**. ➡️ *Aynı adı taşıyan iki alan,*",
          "*aynı alan olduğunun kanıtı değildir; ad eşleşmesi burada «tüketiliyor» derdi.*", "",
          "⚠️ **Bu «gereksiz» demek DEĞİL:** bir alan bugün okunmuyor olabilir ve tezde",
          "betimleyici istatistik olarak, ya da ileride tabakalı örneklemede",
          "kullanılabilir. ⭐ Ama **kayıt disiplini açısından fark var**: okunmayan bir",
          f"alanın **yanlış olduğu hiçbir yerde ortaya çıkmaz**. T76'nın `egitim` kusuru",
          f"{len(ilkokul)} tohumda durdu ve onu gösteren şey üretim değil, **ayrı bir**",
          "**denetim** oldu.", "",
          "➡️⭐⭐ *Bir alanın doğruluğu, onu okuyan bir tüketici varsa **kendiliğinden***",
          "*sınanır; okuyanı yoksa yalnızca ona bakan bir denetimle sınanır — ve o*",
          "*denetim yazılmamışsa alan sessizce yanlıştır. ⇒ «Şemada duruyor» bir*",
          "*doğruluk güvencesi değil, bir BAKIM BORCUDUR.*", "", "---", ""]

    # --- §4 sınırlar -----------------------------------------------------------
    L += ["## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ **Üretilen metinde register ÖLÇÜLMEDİ** | gerek kalmadı: `egitim` üretim "
          "hattına ulaşmıyor (§2). ⚠️ Ulaşsaydı bile maruziyet **5 kayıt**tı ve o sayıda "
          "register farkı ölçülemezdi |",
          "| ⛔ **Tüketim taraması dizgeye dayalı** | alan adı `\"alan\"` biçiminde aranıyor; "
          "bir alanı **başka adla** okuyan kod (ör. `meta.get(k)` döngüsü) görünmez. "
          "⚠️ İlk arama `egitim_ozeti`'ni yanlış yakaladı ve **elle okunmadan** düzelmedi |",
          "| ⛔ *«Tüketilmiyor»* ≠ *«gereksiz»* | betimleyici istatistik ve ileride tabakalı "
          "örneklem meşru kullanımlar; ölçülen şey **bugünkü** tüketim |",
          "| ⚠️ `data/plan` yalnızca **144** tohum kullanıyor | 2240'ın %6,4'ü; alanların "
          "çoğu için maruziyet zaten düşük |",
          "| ⛔ `notlar` alt alanları | `notlar` bir sözlük ve içindeki anahtarlar "
          "(`esdurumlar` vb.) ayrıca taranmadı — `esdurumlar` `tohum_guvenlik.py`'de "
          "**tüketiliyor** (K76) ve bu tabloda görünmüyor |", ""]

    RAPOR.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print(f"   ilkokul tohum {len(ilkokul)} · üretime giren {len(kullanilan & ilkokul)}/"
          f"{len(kullanilan)}")
    print(f"   egitim: plan {'var' if eg_plan else 'YOK'} · talimat {len(eg_talimat)} · "
          f"hat kodu {len(eg_hat)} · yalnızca denetim {len(eg_den)}")
    print(f"   SeedMeta {len(alanlar)} alan · boru hattında OKUNMAYAN {len(olu)}: "
          + ", ".join(olu))
    return 0


if __name__ == "__main__":
    sys.exit(main())
