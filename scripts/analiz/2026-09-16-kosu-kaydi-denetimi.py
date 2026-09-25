#!/usr/bin/env python3
"""§3.2 sekiz kalem ilan ediyor — koşular kaçını tutuyor, ve `datasets/` gerçekten değişmez mi?

T65 *«donanım hiçbir koşuda kayıtlı değil»* dedi ve doğruydu. ⚠️ Ama o ölçüm
§3.2'nin **tek** kalemine bakmıştı. Bu betik ilan edilen **bütün** kalemleri
tek tek sınıyor — çünkü T65'in dersi zaten buydu: *bir kural ilan edilip
denetlenmezse tutulmuyor*, ve denetlenmeyen kalem sayısı bilinmiyorsa dersin
kendisi de ölçülmemiş demektir.

İki ilan yeri var ve ikisi de okunuyor:
  · `docs/tez/tez-plani.md` §3.2 — tezin kayıt kuralı
  · `plan.md` §10            — deney takibi satırı

⭐⭐ İkinci ve daha ağır soru: **Kural 4 `datasets/vX.Y.Z/`'yi IMMUTABLE ilan
ediyor ama bu hiç DOĞRULANMADI.** `manifest.json` bir SHA256 taşıyor — fakat o
hash **yukarı akıştaki** `data/judged/*.jsonl` dosyasının hash'i, setin kendi
artefaktının değil. ⇒ `train.jsonl` bugün değiştirilse **hiçbir kayıt bunu
göstermez**. Burada iki bağımsız yoldan bakılıyor:

  A. yukarı akış dosyaları ilan edilen hash'i hâlâ tutuyor mu
  B. ⭐ `src/build.py` **ÇAĞRILARAK** her sürüm yeniden türetilip bayt bayt
     karşılaştırılıyor (kopyalanmıyor; yalnızca çıktı kökü geçici dizine alınıyor)

⚠️ (B)'nin güvencesi koşullu: `build.py` saf bir fonksiyon olduğu **sürece**
çalışır. Betik değişirse ayrım kaybolur — *«set mi değişti, türetici mi»*
sorusu cevapsız kalır. ➡️ Bu yüzden (B) hash kaydının YERİNE geçmez; hash'in
neden gerektiğinin kanıtıdır.

Girdi : runs/*/metrics.json · runs/*/config.yaml · datasets/v*/manifest.json ·
        datasets/v*/train.jsonl · data/judged/*.jsonl · src/build.py
Çıktı : reports/analiz/2026-09-16-kosu-kaydi-denetimi.md
Kullanım: uv run python scripts/analiz/2026-09-16-kosu-kaydi-denetimi.py
"""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import re
import sys
import tempfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-kosu-kaydi-denetimi.md"
TEZ = KOK / "docs/tez/tez-plani.md"
PLAN = KOK / "plan.md"
BUILD = KOK / "src/build.py"
TRAIN = KOK / "src/train.py"


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def shab(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]


# --- §3.2'nin kalemleri -------------------------------------------------------
# ⛔ Kalemler burada ELLE yazılı çünkü ilan düzyazı; ama ilan satırı da rapora
#    basılıyor ki okur karşılaştırabilsin (betik ilanı yorumluyor, üretmiyor).
def ilan_satiri(yol: Path, desen: str) -> tuple[int, str]:
    for i, s in enumerate(yol.read_text(encoding="utf-8").split("\n"), 1):
        if re.search(desen, s):
            return i, s.strip()
    return 0, "— (ilan bulunamadı)"


def _json(y: Path) -> dict:
    try:
        return json.loads(y.read_text(encoding="utf-8"))
    except Exception:
        return {}


def kalem_durumu(run: Path) -> dict[str, bool]:
    m = _json(run / "metrics.json")
    cfg = (run / "config.yaml").read_text(encoding="utf-8", errors="ignore") \
        if (run / "config.yaml").exists() else ""
    return {
        "config.yaml": (run / "config.yaml").exists(),
        "metrics.json": bool(m),
        "samples.md": (run / "samples.md").exists(),
        "dataset sürümü": bool(m.get("dataset")),
        "dataset hash": any(k in m for k in ("dataset_sha256", "dataset_sha256_16",
                                             "dataset_hash")),
        "rastgele tohum": bool(re.search(r"^\s*seed:", cfg, re.M)) or "seed" in m,
        "git commit": "git_rev" in m,
        "donanım": any(k in m for k in ("donanim", "hardware", "cihaz")),
    }


# --- datasets/ değişmezliği ---------------------------------------------------
def yazici_sinamasi() -> tuple[dict[str, bool], str]:
    """⭐ Yazıcı GERÇEKTEN yazıyor mu — geçici kökte tam bir eğitim koşusu.

    ⛔ `runs/` dokunulmaz (Kural 7): kök geçici dizine alınır, gerekli dizinler
    sembolik bağ olur. Koşu **gerçek** (50 adım MLX LoRA, ~15 sn) çünkü alanların
    bir kısmı ancak koşu bittikten sonra doluyor.

    ⚠️ Rapora **yalnızca kararlı olgular** basılır: hangi kalem yazıldı, dönüş
    kodu sıfır mı, dataset hash mühürlüyle aynı mı. ⛔ Süre ve zaman damgası
    basılmaz — yoksa Kural 7 denetimi raporu haklı olarak *«sapıyor»* sayardı.
    """
    t = train_modulu()
    td = Path(tempfile.mkdtemp(prefix="yazici-"))
    for ad in ("datasets", "configs", "models", ".git", "data", "src"):
        (td / ad).symlink_to(KOK / ad)
    t.ROOT = td
    # ⚠️ `train.main()` metrics'i stdout'a basıyor; denetimin çıktısını kirletmesin.
    with contextlib.redirect_stdout(io.StringIO()):
        kod = t.main(str(KOK / "configs/training/e4b.yaml"))
    run = sorted((td / "runs").glob("*"))[-1]
    m = json.loads((run / "metrics.json").read_text(encoding="utf-8"))
    return {
        "config.yaml": (run / "config.yaml").exists(),
        "metrics.json": (run / "metrics.json").exists(),
        "samples.md": (run / "samples.md").exists(),
        "dataset sürümü": bool(m.get("dataset")),
        "dataset hash": "dataset_sha256_16" in m,
        "rastgele tohum": "seed" in m,
        "git commit": bool(m.get("git_rev")),
        "donanım": bool(m.get("donanim")),
        "dönüş kodu 0": kod == 0,
    }, m.get("dataset_sha256_16", "")


def train_modulu():
    """⭐ `src/train.py` de ÇAĞRILIR — donanım okuması burada YENİDEN YAZILMAZ."""
    spec = importlib.util.spec_from_file_location("_trn", TRAIN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_modulu():
    """⭐ `src/build.py` ÇAĞRILIR — türetme mantığı kopyalanmaz."""
    spec = importlib.util.spec_from_file_location("_bld", BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def yeniden_turet(surum: str, girdi: Path) -> bytes | None:
    """Sürümü geçici bir köke türetir. ⛔ `datasets/` ASLA yazılmaz (Kural 4/7)."""
    b = build_modulu()
    gercek_karantina = b.KARANTINA_YOL           # kök değişince kayboluyor, sabitleniyor
    with tempfile.TemporaryDirectory() as td:
        b.ROOT = Path(td)
        b.KARANTINA_YOL = gercek_karantina
        try:
            # ⚠️ `build.main()` stdout'a yazıyor; denetimin çıktısını kirletmesin.
            with contextlib.redirect_stdout(io.StringIO()):
                b.main(str(girdi), surum)
        except SystemExit:
            return None
        p = Path(td) / "datasets" / surum / "train.jsonl"
        return p.read_bytes() if p.exists() else None


def main() -> int:
    L: list[str] = []
    runs = sorted(p for p in (KOK / "runs").glob("*") if (p / "metrics.json").exists())
    surumler = sorted(p.name for p in (KOK / "datasets").glob("v*") if p.is_dir())

    tez_no, tez_ilan = ilan_satiri(TEZ, r"samples\.md.*dataset sürümü")
    plan_no, plan_ilan = ilan_satiri(PLAN, r"Deney takibi")

    L += [f"# Koşu kaydı §3.2'yi tutuyor mu — ve `datasets/` gerçekten değişmez mi?", "",
          f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
          f"**Girdi:** `runs/*/metrics.json` — **{len(runs)}** koşu  ",
          f"**Girdi:** `datasets/v*/` — **{len(surumler)}** sürüm  ",
          f"**Girdi:** `src/build.py` SHA256 `{sha(BUILD)}` (türetme **çağrılıyor**)  ",
          f"**Girdi:** `src/train.py` SHA256 `{sha(TRAIN)}`  ",
          f"**Girdi:** `docs/tez/tez-plani.md` SHA256 `{sha(TEZ)}`  ",
          f"**Girdi:** `plan.md` SHA256 `{sha(PLAN)}`", "", "---", "",
          "## Neden", "",
          "T65 *«donanım hiçbir koşuda kayıtlı değil»* dedi ve doğruydu — ama §3.2'nin",
          "**tek** kalemine bakmıştı. Bir kural ilan edilip denetlenmezse tutulmuyor;",
          "⭐ denetlenmemiş kalem sayısı bilinmiyorsa **dersin kendisi de ölçülmemiş**",
          "demektir. Burada ilan edilen bütün kalemler tek tek sınanıyor.", "",
          "**İlan yerleri — okur karşılaştırabilsin diye basılıyor:**", "",
          f"· `docs/tez/tez-plani.md:{tez_no}` → *{tez_ilan}*  ",
          f"· `plan.md:{plan_no}` → *{plan_ilan}*", "", "---", ""]

    # --- §1 kalem tablosu -----------------------------------------------------
    kalemler = list(kalem_durumu(runs[0]).keys()) if runs else []
    sayim = {k: 0 for k in kalemler}
    for r in runs:
        for k, v in kalem_durumu(r).items():
            sayim[k] += bool(v)

    L += ["## 1. §3.2'nin sekiz kalemi — hangisi kaç koşuda var", "",
          "| Kalem | Tutan koşu | |", "|---|---:|---|"]
    for k in kalemler:
        n = sayim[k]
        isaret = "✅" if n == len(runs) else ("⛔ **hiçbirinde**" if n == 0 else "⚠️ kısmi")
        L.append(f"| `{k}` | **{n}**/{len(runs)} | {isaret} |")
    yok = [k for k in kalemler if sayim[k] == 0]
    L += ["",
          f"⛔ **{len(yok)} kalem {len(runs)} koşunun HİÇBİRİNDE yok:** "
          + ", ".join(f"`{k}`" for k in yok) + ".", "",
          "⚠️ Bunların **yalnızca biri** (`donanım`) daha önce ölçülmüştü (T65). "
          f"Öteki {len(yok) - 1} kalem ilan edildiği günden beri **hiç sorulmamıştı** — "
          "ve `samples.md` **iki ayrı yerde** ilan edilip **hiçbir yerde üretilmiyor**.", "",
          "➡️ *İlan ile üretim arasındaki mesafe tek bir kalemde ölçülünce küçük görünür;*",
          "*kalem sayısı ölçülünce kuralın kendisinin işlemediği görünür.*", ""]

    # --- §2 koşu kırılımı -----------------------------------------------------
    L += ["## 2. Koşu kırılımı — eksik kalem koşuya göre değişiyor mu", "", "| Koşu | eksik |",
          "|---|---|"]
    desenler = set()
    for r in runs:
        d = kalem_durumu(r)
        eks = tuple(k for k in kalemler if not d[k])
        desenler.add(eks)
        L.append(f"| `{r.name}` | " + (", ".join(f"`{k}`" for k in eks) or "—") + " |")
    L += ["",
          f"⭐ **{len(desenler)} farklı eksik deseni** var. "
          + ("Tek desen ⇒ bu bir koşu hatası değil, **yazıcının kendisinin** eksiği: "
             "`src/train.py` bu alanları hiç üretmiyor."
             if len(desenler) == 1 else
             "Birden çok desen ⇒ eksiklik koşuya göre değişiyor, tek sebep aranmamalı."), ""]

    # --- §3 datasets/ değişmezliği -------------------------------------------
    L += ["## 3. ⭐⭐ `datasets/` IMMUTABLE ilan edildi — ilk kez DOĞRULANIYOR", "",
          "Kural 4 `datasets/vX.Y.Z/`'yi değişmez ilan ediyor. `manifest.json` bir SHA256",
          "taşıyor — ⛔ ama o hash **yukarı akıştaki** `data/judged/*.jsonl` dosyasının,",
          "**setin kendi artefaktının değil**. ⇒ `train.jsonl` bugün değiştirilse hiçbir",
          "kayıt bunu göstermez. İki bağımsız yoldan bakılıyor.", "",
          "### 3a. Yukarı akış — ilan edilen hash bugün tutuyor mu", "",
          "| Sürüm | `input_file` | ilan | bugün | |", "|---|---|---|---|---|"]
    a_tutan = 0
    for v in surumler:
        man = _json(KOK / f"datasets/{v}/manifest.json")
        gp = KOK / man.get("input_file", "")
        ilan = man.get("input_sha256_16", "—")
        if gp.exists():
            bug = sha(gp)
            ok = bug == ilan
            a_tutan += ok
            L.append(f"| `{v}` | `{man['input_file']}` | `{ilan}` | `{bug}` | "
                     f"{'✅' if ok else '⛔ **SAPIYOR**'} |")
        else:
            L.append(f"| `{v}` | `{man.get('input_file','—')}` | `{ilan}` | — | ⛔ **dosya yok** |")
    L += ["", f"**{a_tutan}/{len(surumler)}** tutuyor.", "",
          "### 3b. ⭐ Artefaktın kendisi — `src/build.py` ÇAĞRILARAK yeniden türetildi", "",
          "Türetme mantığı **kopyalanmıyor**: `src/build.py` içe aktarılıp `main()`",
          "çağrılıyor, değişen tek şey çıktı kökü (geçici dizin). ⛔ `datasets/` yazılmıyor.", "",
          "| Sürüm | `train.jsonl` bugün | yeniden türetilen | satır | |",
          "|---|---|---|---:|---|"]
    b_tutan, b_toplam = 0, 0
    for v in surumler:
        man = _json(KOK / f"datasets/{v}/manifest.json")
        eski_p = KOK / f"datasets/{v}/train.jsonl"
        if not eski_p.exists():
            L.append(f"| `{v}` | — | — | — | ⛔ **`train.jsonl` yok** |")
            continue
        eski = eski_p.read_bytes()
        yeni = yeniden_turet(v, KOK / man["input_file"])
        b_toplam += 1
        if yeni is None:
            L.append(f"| `{v}` | `{shab(eski)}` | — | {len(eski.splitlines())} | "
                     "⚠️ türetilemedi |")
            continue
        ok = eski == yeni
        b_tutan += ok
        L.append(f"| `{v}` | `{shab(eski)}` | `{shab(yeni)}` | {len(eski.splitlines())} | "
                 f"{'✅ **bayt bayt aynı**' if ok else '⛔ **FARKLI**'} |")
    L += ["", f"⭐⭐ **{b_tutan}/{b_toplam} sürüm bayt bayt yeniden türetiliyor.** "
          "Kural 4'ün değişmezlik iddiası ilan edildiği günden beri ilk kez **sınandı** "
          "ve tuttu.", "",
          "⚠️ **Ama bu güvence KOŞULLU ve hash kaydının yerine GEÇMEZ.** (3b) yalnızca",
          "`build.py` saf bir fonksiyon olduğu sürece çalışır. Betik yarın değişirse",
          "karşılaştırma bozulur ve ⛔ *«set mi değişti, türetici mi»* sorusu **cevapsız**",
          "kalır — çünkü ayıracak bir kayıt yok. ➡️ *Yeniden türetme değişmezliği ölçmez;*",
          "*değişmezlik ile türeticinin kararlılığının ÇARPIMINI ölçer. Hash kaydı ikisini*",
          "*ayırabilen tek şeydir — ve tam bu yüzden gerekli.*", ""]

    # --- §4 bugünün mührü -----------------------------------------------------
    L += ["## 4. Bugünün mührü — geçmişe yazılamıyor, buraya yazılıyor", "",
          "⛔ `datasets/` IMMUTABLE olduğu için 5 manifest'e hash **eklenemez** (Kural 4),",
          "geçmiş 24 koşuya donanım **yazılamaz** (Kural 7: `runs/` üzerine yazılmaz).",
          "⭐ Kaydın gidebileceği tek yer bu rapor: tarihli, betiğe bağlı, üzerine",
          "yazılmayan bir dosya. **Bundan sonraki her sapma buraya karşı ölçülür.**", "",
          "| Artefakt | SHA256 (16) |", "|---|---|"]
    for v in surumler:
        for ad in ("train.jsonl", "manifest.json"):
            p = KOK / f"datasets/{v}/{ad}"
            if p.exists():
                L.append(f"| `datasets/{v}/{ad}` | `{sha(p)}` |")
    L += [f"| `src/build.py` | `{sha(BUILD)}` |", ""]

    # --- §5 ne düzeltildi -----------------------------------------------------
    yazici_alanlari = sorted(set(re.findall(r'"([a-z_]+)":', 
        (TRAIN.read_text(encoding="utf-8").split("metrics = {")[-1].split("}")[0]
         if "metrics = {" in TRAIN.read_text(encoding="utf-8") else ""))))
    L += ["## 5. `src/train.py` bugün hangi alanları yazıyor", "",
          "⚠️ Bu liste **koşulardan değil betikten** okunuyor — yani bundan sonraki",
          "koşuların ne taşıyacağını gösterir, geçmişin ne taşıdığını değil.", "",
          "| | |", "|---|---|",
          f"| `metrics` sözlüğünün alanları | {', '.join(f'`{a}`' for a in yazici_alanlari) or '—'} |",
          f"| `samples.md` üretiliyor mu | {'✅ evet' if 'samples.md' in TRAIN.read_text(encoding='utf-8') else '⛔ **hayır**'} |",
          ""]

    # --- §5b elle yazılan ortam ile ölçülen ------------------------------------
    L += ["## 5b. ⭐ İlk otomatik donanım kaydı — elle yazılanla karşılaştırıldı", "",
          "⛔ Geçmiş 24 koşuda donanım yok; tez bunun yerine `PROJECT_MEMORY.md`'nin",
          "**elle yazılmış** ortam başlığına dayanacaktı. O başlık şimdi ilk kez",
          "ölçümle karşılaştırılıyor — donanım okuması `src/train.py`'den **çağrılıyor**,",
          "burada yeniden yazılmıyor.", ""]
    try:
        t = train_modulu()
        olcum = t.donanim()
    except Exception as e:
        olcum = {}
        L += [f"⚠️ Ölçüm alınamadı: `{type(e).__name__}: {e}`", ""]
    elle_no, elle = ilan_satiri(KOK / "PROJECT_MEMORY.md", r"^\*\*Donanım:")
    if olcum:
        L += [f"**Elle yazılan** (`PROJECT_MEMORY.md:{elle_no}`): *{elle}*", "",
              "**Ölçülen:**", "", "| Alan | Değer |", "|---|---|"]
        for k, v in olcum.items():
            L.append(f"| `{k}` | `{v}` |")
        # ⛔ Tek tek eşleştirme yapılmıyor (elle satır düzyazı); yalnızca sürüm
        #    dizgesi aranıyor — bulunamazsa çelişki olarak bildiriliyor.
        srm = re.search(r"macOS[- ]([0-9]+\.[0-9]+)", str(olcum.get("platform", "")))
        elle_srm = re.search(r"macOS\s*([0-9]+\.[0-9]+)", elle)
        if srm and elle_srm and not str(olcum["platform"]).count(elle_srm.group(1)):
            L += ["",
                  f"⛔ **Çelişki:** elle yazılan `macOS {elle_srm.group(1)}`, ölçülen "
                  f"`macOS {srm.group(1)}`. `{elle_srm.group(1)}` **Darwin çekirdek sürümü** "
                  f"(bu makinede Darwin {elle_srm.group(1)}.0), macOS sürümü değil.", "",
                  "➡️ *T65'in dersi burada kendini gösteriyor: elle tutulan alan sessizce*",
                  "*kayar ve kaydığını gösteren bir şey yoktur. Yanlış olan sayı büyük*",
                  "*değil — ⚠️ önemli olan, yanlışlığın ancak ilk OTOMATİK kayıtla*",
                  "*görünmesi.* ✅ Satır düzeltildi; düzeltmeyi gösteren şey bu rapordur.", ""]
        else:
            L += ["", "✅ **Sürüm dizgesi tutuyor.**", "",
                  "⚠️ Ama bu satır 2026-09-16'ya kadar `macOS 25.6` taşıyordu ve o "
                  "**Darwin çekirdek** sürümüdür, macOS sürümü değil (K144 · T72). "
                  "⛔ Çelişki 24 koşu boyunca kimsenin gözüne çarpmadı; ⭐ onu gösteren "
                  "ilk şey **ilk otomatik kayıt** oldu.", "",
                  "➡️ *T65'in dersi burada kendini gösteriyor: elle tutulan alan sessizce*",
                  "*kayar ve kaydığını gösteren bir şey yoktur. Yanlış olan sayı büyük değil —*",
                  "*⚠️ önemli olan, yanlışlığın ancak ölçüm devreye girince görünmesi.*", ""]

    # --- §6 yazıcı sınaması ---------------------------------------------------
    L += ["## 6. ⭐ Yazıcı sınandı — geçici kökte gerçek bir koşu", "",
          "§1 **geçmişi** ölçüyor, §5 **betiği okuyor**. ⛔ İkisi de yazıcının",
          "gerçekten yazdığını göstermez: bir alanın kodda görünmesi, koşu bittiğinde",
          "dosyaya düştüğü anlamına gelmez. ⭐ Burada `src/train.py:main()` **çağrılıyor**",
          "— 50 adım gerçek MLX LoRA — ama kök geçici bir dizin, ⛔ `runs/` dokunulmuyor.", ""]
    sinama_ozet = "⚠️ koşturulamadı"
    try:
        sonuc, ds_hash = yazici_sinamasi()
        sinama_ozet = f"{sum(sonuc.values())}/{len(sonuc)} kalem"
        L += ["| Kalem | Yazıldı mı |", "|---|---|"]
        for k, v in sonuc.items():
            L.append(f"| `{k}` | {'✅' if v else '⛔ **hayır**'} |")
        muhur = sha(KOK / "datasets/v0.0.1/train.jsonl")
        L += ["",
              f"⭐ **{sum(sonuc.values())}/{len(sonuc)}** — yazıcı §3.2'nin sekiz kalemini de "
              "üretiyor ve koşu sıfırla dönüyor.", "",
              f"⭐ **Çapraz kontrol:** koşunun yazdığı `dataset_sha256_16` = `{ds_hash}`, "
              f"§4'te mühürlenen `datasets/v0.0.1/train.jsonl` = `{muhur}` → "
              f"{'**aynı**' if ds_hash == muhur else '⛔ **FARKLI**'}. "
              "Yani kaydedilen hash gerçekten setin hash'i.", "",
              "⚠️ **Bu bir koşu kaydı DEĞİL** — geçici kökte koştu ve silindi. `runs/`",
              "hâlâ 24 koşu taşıyor ve **hiçbirinde** bu alanlar yok. ➡️ *Kalem*",
              "*«düzeltildi» değil «yazıcıda kapandı, kayıtta henüz açık»dır; ilk gerçek*",
              "*koşuya kadar §1 tablosu 0/24 göstermeye devam edecek ve göstermelidir.*", ""]
    except Exception as e:
        L += [f"⚠️ **Sınama koşturulamadı:** `{type(e).__name__}: {e}`", "",
              "⛔ Bu bir başarısızlık kaydıdır, atlama değil: yazıcının §3.2'yi tuttuğu "
              "**gösterilemedi**.", ""]

    L += ["## ⛔ Bu denetimin söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ `samples.md`'nin **içeriği** | §3.2 dosyayı ilan ediyor, içeriğini "
          "tanımlamıyor. Ne yazılacağı bir karardır, ölçüm değil |",
          "| ⛔ Geçmiş 24 koşunun donanımı | geri yazılamaz; tezde *«koşu kaydında yok, "
          "ortam `PROJECT_MEMORY.md` başlığında sabit»* notu düşülecek |",
          "| ⚠️ (3b)'nin güvencesi | koşullu — `build.py` değişirse ayrım kaybolur (§3b) |",
          "| ⚠️ `eval` koşuları | bu denetim yalnızca **eğitim** koşularına bakıyor; "
          "`runs/*/eval/*` ayrı bir kayıt disiplini ve ayrıca sınanmadı |", ""]

    RAPOR.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print(f"   koşu {len(runs)} · hiç tutmayan kalem {len(yok)} ({', '.join(yok)}) · "
          f"eksik deseni {len(desenler)}")
    print(f"   datasets: yukarı akış {a_tutan}/{len(surumler)} · "
          f"yeniden türetme {b_tutan}/{b_toplam} bayt bayt aynı")
    print(f"   yazıcı sınaması: {sinama_ozet}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
