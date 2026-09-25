#!/usr/bin/env python3
"""T73'ün altıncı ve yedinci örneği aranıyor — ve YÖN TERSİNE DÖNÜYOR.

T73 §15 kapısını düzeltti ve raporu bir borç bıraktı: *«`checks.py`'de düz
`.lower()` kullanan 3 satır daha var ve hiçbiri sınanmadı»*. Burada sınanıyor.

  · **A** — `context_ok` / `KLINIK_IDDIA` (`:207`, `:210`): sentetik bağlam
    pasajında klinik iddia izi arar (§7b-2)
  · **B** — `replay_ok` / `BIRAG_IMZA` (`:229`): replay kaydının kanonik BıRAG
    system prompt'unu kullanmadığını doğrular (§9 unutma savunması)

⭐⭐ **Beklenmedik bulgu: öldüren vektör TERS.** T73'te tehlike ASCII `I`'ydı,
çünkü yasak ifadeler **ı** taşıyordu. Burada A sitesinin kalıpları **i**
taşıyor ve bu yüzden öldüren şey `İ` — `"BELİRTİ".lower()` → `"beli̇rti̇"`
(i + BİRLEŞEN NOKTA) ve `\\bbelirti` ile eşleşmiyor. ➡️ *Hangi vektörün
öldürdüğü kalıbın HARFİNE bağlı; bu yüzden «hangi yöne normalize edelim»
sorusunun tek bir doğru cevabı yok — sınıf gerekiyor.*

⚠️ **A sitesi TOPLU bakınca sağlam görünüyor** ve bu bir tuzak: desen bir
kök AYRIMI, yani *«ilaç»* ölse bile *«tedavi»* yakalıyor. Ölü kök ancak
**tek tek** sınanınca görünür — bu yüzden ölçüm kök düzeyinde yapılıyor
(T60'ın dersi: serbestlik derecesi, sayının RAPORLANDIĞI düzeyde ölçülür).

Girdi : src/checks.py · datasets/v*/train.jsonl · data/judged/*.jsonl ·
        data/candidates/*.jsonl
Çıktı : reports/analiz/2026-09-16-kalan-lower-satirlari.md
Kullanım: uv run python scripts/analiz/2026-09-16-kalan-lower-satirlari.py
"""
# lower-muaf-dosya: aynı: eski davranış referans olarak duruyor (T75)
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-kalan-lower-satirlari.md"
sys.path.insert(0, str(KOK / "src"))
import checks as C  # noqa: E402

_s = importlib.util.spec_from_file_location("_tg", KOK / "src/tohum_guvenlik.py")
TG = importlib.util.module_from_spec(_s)
_s.loader.exec_module(TG)

# ⛔ Kalıbın 2026-09-16 ÖNCESİ hâli — referans olarak DURUYOR. Canlı kapı
#    düzeltilince ölü kök sayısı sıfırlanır ve tuzağın büyüklüğü raporda
#    görünmez olurdu (T73'te aynı sorun çıktı, aynı çözüm uygulanıyor).
ESKI_DESEN = re.compile(
    r"\bbelirti(si|leri|ler|yi|nin)?\b|\btanı(sı|ları|lar|nın)?\b|\bdoz(u|lar|ları|aj)?\b"
    r"|\byoksunluk\w*|\bsemptom\w*|\bteşhis\w*|\bilaç\w*|\bilac\w+|\bterapi\w*"
    r"|\btedavi\w*|\biyileş\w*|\bzararl\w*|\betkili\w*"
    r"|\bbağımlılık yap\w*|\betki eder\b"
    r"|\b(hafta|gün|ay|yıl) (sürer|içinde geçer)\b|\briski\s+(art|azal)\w*",
    re.IGNORECASE)
ESKI_IMZA = ("sen bırag'sın", "bırag sensin")

# Desenin düz kökleri — tek tek sınanacak. ⚠️ Elle yazılı: desenden kök çıkarmak
# regex ayrıştırması ister ve o ayrıştırıcı da ayrıca sınanması gereken bir şey
# olurdu. Bunun yerine kökler burada duruyor ve §2 her birinin desende GERÇEKTEN
# bulunduğunu doğruluyor — bulunamayan kök raporu düşürür.
KOKLER = ["belirti", "tanı", "doz", "yoksunluk", "semptom", "teşhis", "ilaç", "ilacı",
          "terapi", "tedavi", "iyileşir", "zararlı", "etkili", "bağımlılık yapar",
          "etki eder", "riski artar"]
IMZA_YAZIMLARI = ["Sen BıRAG'sın.", "SEN BıRAG'SIN.", "Sen BIRAG'sın.",
                  "SEN BIRAG'SIN.", "Sen BİRAG'sın.", "BıRAG sensin."]
OLUMSUZ = ["Bir kedi uyuyor.", "Sen bir çeviri asistanısın.", "You are a helpful assistant."]


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def tr_buyut(s: str) -> str:
    """DOĞRU Türkçe büyütme (`i`→`İ`, `ı`→`I`) — Python'un `.upper()`'ı bunu yapmaz."""
    return s.replace("i", "İ").replace("ı", "I").upper()


VEKTOR = [("olduğu gibi", lambda s: s),
          ("**doğru TR büyütme** (`i`→`İ`)", tr_buyut),
          ("**ASCII özensiz** `.upper()`", str.upper)]


# --- A sitesi ----------------------------------------------------------------
def a_eski(metin: str) -> bool:
    return bool(ESKI_DESEN.search(metin.lower()))


def a_canli(metin: str) -> bool:
    """⭐ Canlı kapı ÇAĞRILIYOR — `context_ok` üzerinden, mantık kopyalanmıyor."""
    kayit = {"context": [{"sentetik": True, "kaynak": "kurum yordamı", "metin": metin}]}
    return not C.context_ok(kayit)[0]


# --- B sitesi ----------------------------------------------------------------
def b_eski(sys_msg: str) -> bool:
    low = sys_msg.lower()
    return any(im in low for im in ESKI_IMZA)


def b_canli(sys_msg: str) -> bool:
    """⭐ Canlı kapı ÇAĞRILIYOR — `replay_ok` üzerinden."""
    kayit = {"replay": True, "messages": [{"role": "system", "content": sys_msg}]}
    return not C.replay_ok(kayit)[0]


def kayitlar():
    yollar = (sorted(KOK.glob("datasets/v*/train.jsonl"))
              + sorted(KOK.glob("data/judged/*.jsonl"))
              + sorted(KOK.glob("data/candidates/*.jsonl")))
    for p in yollar:
        for n, satir in enumerate(p.read_text(encoding="utf-8").split("\n")):
            if not satir.strip():
                continue
            try:
                yield str(p.relative_to(KOK)), json.loads(satir), n
            except json.JSONDecodeError:
                continue


def main() -> int:
    L: list[str] = []
    kaynak = (KOK / "src/checks.py").read_text(encoding="utf-8")
    kalan = [(n, s.strip()) for n, s in enumerate(kaynak.split("\n"), 1)
             if ".lower()" in s and "i_sinifi" not in s and "tr_kucult" not in s
             and not s.strip().startswith("#")]

    L += ["# `checks.py`'de kalan üç `.lower()` — ve öldüren vektör TERS çıktı", "",
          f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
          f"**Girdi:** `src/checks.py` SHA256 `{sha(KOK/'src/checks.py')}` "
          f"(kapılar **çağrılıyor**, mantık kopyalanmıyor)  ",
          f"**Girdi:** `datasets/v*/train.jsonl` · `data/judged/*.jsonl` · "
          f"`data/candidates/*.jsonl`", "", "---", "", "## Neden", "",
          "T73 §15 kapısını kapattı ve bir **borç** bıraktı: *«`checks.py`'de düz",
          "`.lower()` kullanan 3 satır daha var ve hiçbiri sınanmadı»*. Burada sınanıyor.", "",
          "| Site | Kapı | İşi |", "|---|---|---|",
          "| **A** | `context_ok` / `KLINIK_IDDIA` | sentetik bağlam pasajında klinik "
          "iddia izi (§7b-2) |",
          "| **B** | `replay_ok` / `BIRAG_IMZA` | replay kaydı kanonik BıRAG prompt'unu "
          "kullanmasın (§9 unutma savunması) |", "", "---", ""]

    # --- §1 A sitesi — kök kök --------------------------------------------------
    eksik_kok = [k for k in KOKLER if not a_eski(k + " sözcüğü.")
                 and not a_eski("ilacın" if k == "ilacı" else k)]
    L += ["## 1. A sitesi — ⚠️ toplu bakınca sağlam, kök kök bakınca değil", "",
          "⛔ Desen bir kök **ayrımı**: *«ilaç»* ölse bile *«tedavi»* yakalar, o yüzden",
          "tam bir cümle neredeyse her zaman tutar. ⭐ Ölü kök ancak **tek tek** sınanınca",
          "görünür — T60'ın dersi: *serbestlik derecesi, sayının RAPORLANDIĞI düzeyde*",
          "*ölçülür.* Her kök tek başına bir pasaja konup üç biçimde yazılıyor.", "",
          "| kök | " + " | ".join(f"eski · {v}" for v, _ in VEKTOR) + " | canlı (3 vektör) |",
          "|---|" + "---:|" * (len(VEKTOR) + 1)]
    a_olu = {v: [] for v, _ in VEKTOR}
    a_canli_olu = 0
    for k in KOKLER:
        hucre = []
        for vad, vf in VEKTOR:
            m = vf(k) + " sözcüğü."
            ok = a_eski(m)
            hucre.append("✅" if ok else "⛔")
            if not ok:
                a_olu[vad].append(k)
        cn = sum(1 for _, vf in VEKTOR if not a_canli(vf(k) + " sözcüğü."))
        a_canli_olu += cn
        hucre.append("✅ **0**" if cn == 0 else f"⛔ **{cn}**")
        L.append(f"| `{k}` | " + " | ".join(hucre) + " |")
    L += ["",
          f"⛔ **Doğru TR büyütmede {len(a_olu[VEKTOR[1][0]])}/{len(KOKLER)} kök ÖLÜ:** "
          + ", ".join(f"`{k}`" for k in a_olu[VEKTOR[1][0]]) + ".  ",
          f"⚠️ ASCII özensiz büyütmede ölü kök: **{len(a_olu[VEKTOR[2][0]])}**.  ",
          f"{'✅' if a_canli_olu == 0 else '⛔'} **Canlı kapıda ölü hücre: "
          f"{a_canli_olu}/{3*len(KOKLER)}.**", ""]

    # --- §2 ⭐⭐ yön tersine döndü ---------------------------------------------
    L += ["## 2. ⭐⭐ Öldüren vektör T73'ün TERSİ — ve sebebi kalıbın kendi harfi", "",
          "T73'te tehlike **ASCII `I`**'ydı: yasak ifadeler `ı` taşıyordu ve büyütülünce",
          "`I` olup geri gelemiyordu. ⛔ Burada tam tersi. A sitesinin kökleri **`i`**",
          "taşıyor:", "", "```text",
          '"BELİRTİ".lower()  ->  "beli̇rti̇"   ⛔ i + BİRLEŞEN NOKTA',
          '                       \\bbelirti ile EŞLEŞMEZ',
          '"BELIRTI".lower()  ->  "belirti"   ✅ eşleşir (ASCII I -> i)',
          "```", "",
          "➡️⭐⭐ *Yani **doğru** Türkçe yazan kaçıyor, **özensiz** yazan yakalanıyor —",
          "T73'ün tam tersi. Hangi vektörün öldürdüğü, kalıbın hangi harfi taşıdığına",
          "bağlı. ⇒ «Hangi yöne normalize edelim» sorusunun tek bir doğru cevabı YOK;",
          "her kapı için ayrı ve kalıba bakılarak verilmesi gereken bu karar, tam da",
          "unutulacak türden bir karardır. **Sınıf** (`i_sinifi`) bu kararı ortadan",
          "kaldırır: soru sorulmaz.*", ""]

    # --- §3 B sitesi -----------------------------------------------------------
    L += ["## 3. ⭐⭐ B sitesi — projenin KENDİ ADI tuzağın içinde", "",
          "`BIRAG_IMZA` kanonik system prompt'un ayırt edici cümlesini arıyor ve o cümle",
          "**`BıRAG`** içeriyor — ⭐ noktasız `ı` ile, bir büyük harf dizisinin ortasında.",
          "⛔ *Türkçe klavyesi olmayan herkesin yazacağı hâl* `BIRAG`'dır ve o hâl",
          "imzayla eşleşmez.", "",
          "| system prompt | eski | canlı |", "|---|---|---|"]
    b_eski_kacan = 0
    for y in IMZA_YAZIMLARI:
        e, c = b_eski(y), b_canli(y)
        b_eski_kacan += not e
        L.append(f"| `{y}` | {'✅ yakaladı' if e else '⛔ **KAÇTI**'} | "
                 f"{'✅ yakaladı' if c else '⛔ **KAÇTI**'} |")
    L += ["", "**Olumsuz kontrol** — replay prompt'u BıRAG değilse geçmeli:", "",
          "| system prompt | eski | canlı |", "|---|---|---|"]
    yanlis_pozitif = 0
    for y in OLUMSUZ:
        e, c = b_eski(y), b_canli(y)
        yanlis_pozitif += c
        L.append(f"| `{y}` | {'⛔ yanlış pozitif' if e else '✅ geçti'} | "
                 f"{'⛔ **yanlış pozitif**' if c else '✅ geçti'} |")
    L += ["",
          f"⛔ Eski kapı {len(IMZA_YAZIMLARI)} yazımın **{b_eski_kacan}**'ini kaçırıyordu; "
          f"canlı kapı **0**. ✅ Olumsuz kontrolde yanlış pozitif: **{yanlis_pozitif}**.", "",
          "⚠️ **Bu kapının kaçırması ne demek:** §9'un catastrophic forgetting savunması "
          "replay verisinin **farklı** promptlarla gelmesine dayanıyor. Kanonik promptla "
          "gelen bir replay kaydı savunmayı görmezden gelir ve modeli yine tek bir dizgeye "
          "kilitler. ⛔ Kapı bunu yakalamak için yazılmış ve `BIRAG` yazımında **görmüyordu**.", ""]

    # --- §4 korpus etkisi ------------------------------------------------------
    n_ctx = n_ctx_fark = n_rep = n_rep_fark = 0
    fark_ornek = []
    for kaynak_yol, r, sira in kayitlar():
        if r.get("context"):
            n_ctx += 1
            # ⛔ `context_ok` klinik iddia DIŞINDAKİ sebeplerle de düşüyor (boş kaynak,
            #    büyük harfle başlayan sentetik kaynak adı, `sentetik` bayrağı yok).
            #    Karşılaştırma o dalları içerirse kapının kendi kusuru değil, kaydın
            #    başka kusuru sayılır. Bu yüzden her pasaj ASGARİ GEÇERLİ bir kayda
            #    sarılıp yalnızca klinik iddia dalı sınanıyor.
            pasajlar = [k.get("metin") or "" for k in r["context"] if isinstance(k, dict)]
            eski_v = any(a_eski(m) for m in pasajlar)
            canli_v = any(a_canli(m) for m in pasajlar)
            if eski_v != canli_v:
                n_ctx_fark += 1
                if len(fark_ornek) < 10:
                    fark_ornek.append((kaynak_yol, r.get("id", f"satır{sira}"), "context"))
        if r.get("replay"):
            n_rep += 1
            sm = next((m["content"] for m in r.get("messages", [])
                       if m.get("role") == "system"), "")
            if b_eski(sm) != b_canli(sm):
                n_rep_fark += 1
                if len(fark_ornek) < 10:
                    fark_ornek.append((kaynak_yol, r.get("id", f"satır{sira}"), "replay"))
    L += ["## 4. Korpus etkisi — düzeltme bir hükmü çevirdi mi", "",
          "⛔ *«Kapı delik»* ile *«kapıdan bir şey kaçtı»* ayrı sorular (T73'ün ayrımı).",
          "Sert bir kapıyı değiştirmenin bedeli **önce** ölçülür (K40).", "",
          "| | |", "|---|---:|",
          f"| bağlamlı kayıt | **{n_ctx}** |",
          f"| ⛔ `context_ok` hükmü değişen | **{n_ctx_fark}** |",
          f"| replay kaydı | **{n_rep}** |",
          f"| ⛔ `replay_ok` hükmü değişen | **{n_rep_fark}** |", ""]
    if fark_ornek:
        L += ["| kaynak | kayıt | kapı |", "|---|---|---|"]
        L += [f"| `{a}` | `{b}` | `{c}` |" for a, b, c in fark_ornek] + [""]
    else:
        L += ["✅ **Hiçbir hüküm değişmedi** — düzeltme bu yüzden uygulanabildi.", "",
              "⛔⛔ **Ama bu kapıları masum yapmaz.** Sıfır fark, kapının çalıştığını",
              "değil, **korpusun o biçimde yazmadığını** gösteriyor. ⚠️ B sitesinde",
              f"bugün yalnızca **{n_rep}** replay kaydı var ve hepsi zaten farklı",
              "promptlarla geliyor; kapı hiç ateşlemedi — yani ⛔ **yanlış negatif oranı**",
              "**ölçülemedi** (T46'nın sınıfı: hiç ateşlemeyen koruma sınanamaz).", ""]

    # --- §5 kalan --------------------------------------------------------------
    L += ["## 5. `checks.py`'de düz `.lower()` kaldı mı", "", "| satır | kod |", "|---|---|"]
    L += [f"| `src/checks.py:{n}` | `{s[:88]}` |" for n, s in kalan] or \
         ["| — | ✅ **kalmadı** |"]
    disari = []
    for p in sorted((KOK / "src").glob("*.py")):
        if p.name in ("checks.py", "tohum_guvenlik.py"):
            continue
        for n, s in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
            if ".lower()" in s and not s.strip().startswith("#"):
                disari.append((p.name, n, s.strip()))
    # ⚠️ Hangi sitenin ne taşıdığı ELLE yazılı (Kural 6: bu bizim okumamız).
    #    Amaç sıralama değil, plana geçen maddenin eyleme dönüşebilmesi.
    ISI = {"filter.py": ("⚠️ **alıntı doğrulama kapısı** (`alinti_nrm`) — T43/T51'in "
                         "dayanağı; `İ` vakasını **yarım** ele alıyor, `I` vakasını hiç. "
                         "⭐ Ama normalizasyon **iki tarafa da** uygulanıyor ⇒ kusur kapıyı "
                         "kör etmez, **fazladan ateşletir** (gerçek alıntı *«doğrulanamadı»* "
                         "sayılır). Bugünkü üst sınır: v9 defterinde 1735 alıntının "
                         "**1**'i ateşledi ve o elle okunup gerçek judge hatası çıktı"),
           "golden_eval.py": ("⚠️ thinking'de İngilizce sözcük sayımı — İngilizce kalıplar, "
                              "Türkçe harf taşımıyor; **düşük risk**"),
           "normalize.py": ("⛔ taksonomi etiketi kanonikleştirme — `data/seeds.jsonl`'ın "
                            "kanonik meta'sı buradan çıkıyor (K26)")}
    L += ["",
          f"⛔ **`src/` içinde `checks.py` DIŞINDA {len(disari)} satır daha var ve bu ölçüm "
          "onlara BAKMADI:**", "", "| dosya | satır | ne taşıyor |", "|---|---|---|"]
    for ad in sorted({a for a, _, _ in disari}):
        L.append(f"| `src/{ad}` | "
                 + ", ".join(str(n) for a, n, _ in disari if a == ad)
                 + f" | {ISI.get(ad, '—')} |")
    L += ["",
          "➡️ *T73 dördüncü örneği buldu, beşincisi aynı gün yeni bir denetimde çıktı,",
          "altıncı ve yedincisi burada. ⚠️ Sayı arttıkça iddia değişiyor: bu artık*",
          "*«şurada bir hata var» değil, **«bu repoda düz `.lower()` VARSAYILAN OLARAK***",
          "***YANLIŞ»**. ⇒ Doğru kapatma tek tek yamamak değil, yanlış varsayılanı*",
          "*erişilemez kılmak — ama o bir **mimari karar** ve bu ölçümün işi değil.*", "",
          "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ `src/` geri kalanı | " + f"{len(disari)} satır sınanmadı (§5) |",
          "| ⛔ A sitesinde **NFKD** | canlı kapı `i_sinifi` kullanıyor ama `tr_kucult`'un "
          "NFKD ayrıştırmasını **kullanmıyor**: desen bir regex ve NFKD `\\b` ile `\\w` "
          "semantiğini bozuyor. ⚠️ Ayrıştırılmış `ç`/`ş`/`ğ` taşıyan bir metin hâlâ "
          "kaçabilir ve bu **ölçülmedi** |",
          "| ⛔ B sitesinde **yanlış negatif oranı** | kapı korpusta hiç ateşlemedi; "
          "gerçek replay verisinde ne kadar yakalayacağı bilinmiyor (T46) |",
          "| ⚠️ Kök listesi **elle** | desenden kök çıkarmak bir regex ayrıştırıcısı ister "
          "ve o da ayrıca sınanmalı olurdu; kökler betikte yazılı |",
          "| ⚠️ i-sınıfının **yanlış pozitif** yönü | `tanı` artık `tani`yi de yakalar; "
          "korpusta etkisi 0 ölçüldü, gelecekte ölçülemez (T73) |", ""]

    RAPOR.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print(f"   A: eski ölü kök (doğru TR) {len(a_olu[VEKTOR[1][0]])}/{len(KOKLER)} · "
          f"canlı ölü hücre {a_canli_olu}/{3*len(KOKLER)}")
    print(f"   B: eski kaçan yazım {b_eski_kacan}/{len(IMZA_YAZIMLARI)} · "
          f"yanlış pozitif {yanlis_pozitif}")
    print(f"   korpus: bağlamlı {n_ctx} (fark {n_ctx_fark}) · replay {n_rep} (fark {n_rep_fark})")
    print(f"   checks.py'de kalan düz .lower(): {len(kalan)} · src/ geri kalanı: {len(disari)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
