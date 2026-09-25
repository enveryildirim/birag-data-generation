#!/usr/bin/env python3
"""Güvenlik kalıplarında NORMALİZASYON kaynaklı ölü desenler — ölçüm ve etki.

Bulunuş: K103 oturumunda `klinik_guvenlik_ihlali`'nin yazı-tura attığı üç kayıt
bedensel belirti taşıyordu. Kararı LLM'den alıp deterministik bir ön-taramaya
taşımak isterken `BEDENSEL` regex'inin "öksürük"ü bulamadığı görüldü.

Kök neden: `tohum_guvenlik.tr_kucult` NFKD uyguluyor — "ö" → "o" + U+0308.
Fonksiyon yalnızca birleşen NOKTAyı (U+0307, Türkçe büyük-İ tuzağı, K76) siliyor;
diğer birleşen imler kalıyor. Dolayısıyla **ç ö ü ş ğ içeren her BİLEŞİK yazılmış
kalıp**, `tr_kucult`'tan geçmiş bir metinde hiç eşleşemez.

Bu, K44 (template thinking'i siliyor) · K47 (regex kapanış etiketi bekliyor) ·
K49 (LoRA anahtarı hiçbir şeyle eşleşmiyor) · K52 (etiket içeriğin vekili) ·
K65 (anahtar kelime kelime içinde eşleşiyor) ailesinin ALTINCI örneği:
hata vermeyen, uyarı üretmeyen, doğrulanmadığı sürece doğru sayılan katman.

⚠️ Bu betik SINIFLANDIRMA yapmaz. "Bedensel belirti geçiyor" der, "kriz" demez —
tıbbi aciliyet klinik karardır ve uzmana aittir (Kural 3).

Kullanım: uv run python scripts/analiz/2026-09-15-olu-desen-taramasi.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⚠️ GİRDİ CANLI KOD: kalıplar `src/tohum_guvenlik.py`'deki `BEDENSEL_BELIRTI`'den
# geliyor ve o desen rapor yayımlandıktan SONRA değişti. ⛔ Sebep ilk sandığım gibi
# "elle kalıp eklemek" DEĞİL (2026-09-16'da düzeltildi): desen literal biçimlerden
# (`öksürük`, `öksürüyor`) TÜRKÇE KÖKE çevrildi (`öksür{EK}`) ve birkaç kırmızı
# bayrak eklendi. Değişen sayı kalıp sayısı değil, EŞLEŞEN TOHUM sayısı: 41 → 61.
# ➡️ Betik bu yüzden kendi 09-15 raporunu yeniden üretemez; 09-15 dosyası desenin
# literal hâlinin kaydıdır ve üzerine yazılmaz (Kural 2).
#
# ⛔ 09-16'da fark edilen: §3c'deki "kalan vuruş" artık `gd-024`'ü de sayıyor ve
# o, bilinen iki yanlış pozitifle AYNI SINIFTA DEĞİL:
#   · `gd-011` «içim hâlâ titriyor»   → duygusal deyim, beden değil
#   · `gd-040` «oğlum sürekli öksürüyor» → BAŞKASININ belirtisi
#   · `gd-024` «Sabah öksürerek kalkıyorum, balgam falan» → BİRİNCİ TEKİL, kendi bedeni
# Yani sayı büyürken anlamı da kaydı: "kalan vuruş" artık "kalan yanlış pozitif"
# demek değil. ⚠️ `gd-024`'ün tıbbi aciliyet taşıyıp taşımadığı KLİNİK KARAR ve
# uzmana ait (Kural 3) — bu betik sınıflandırmaz, yalnızca bulduğunu gösterir.

# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
sys.path.insert(0, str(KOK / "src"))
import golden_checks as gk  # noqa: E402
import tohum_guvenlik as tg  # noqa: E402

TOHUMLAR = KOK / "data/seeds.jsonl"
BOLME = KOK / "evals/bolme.json"
DEV = KOK / "evals/golden.dev.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-normalizasyon-olu-desen.md"

# 2026-09-14 tarihli betikteki HÂLİ — düzeltme öncesi kıyas için birebir kopya.
BEDENSEL_ESKI = (
    r"kan ter|terleyerek uyan|kalbim duracak|kalbim küt|çarpıntı|titreme|el(?:im|lerim)? titri"
    r"|nöbet geçir|havale|bayıl|kustum|kusuyorum|kusma|görme bulan|halüsinasyon"
    r"|göremiyorum|bilinc|uyuşma|felç|nefes alamı|göğsüm sıkış")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def main() -> None:
    tohumlar = [json.loads(l) for l in open(TOHUMLAR) if l.strip()]
    atama = json.loads(BOLME.read_text())["atama"]
    havuz = [t for t in tohumlar if t["seed_id"] in atama]

    y = ["# Normalizasyon kaynaklı ölü desenler — güvenlik kalıplarında sessiz açık", "",
         # ⛔ Kalıp kaynağı CANLI KOD. Sürümü yazılmazsa rapor hangi desen sürümünü
         # anlattığını söyleyemez ve sessizce tarihsizleşir (T54 · K131).
         f"**Kalıp kaynağı:** `src/tohum_guvenlik.py` · SHA256 "
         f"`{hashlib.sha256((KOK / 'src/tohum_guvenlik.py').read_bytes()).hexdigest()[:16]}`  ",
         f"**Girdi:** `data/seeds.jsonl` · SHA256 `{sha(TOHUMLAR)}`  ",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
         f"**Düzeltilen:** `src/tohum_guvenlik.py`", "", "---", "",
         "## 1. Mekanizma", "",
         "`tr_kucult` NFKD uyguluyor ve yalnızca birleşen NOKTAyı (U+0307) siliyor:", "",
         "```", 'tr_kucult("Çarpıntı") == "c" + U+0327 + "arpıntı"   # ç ayrıştı, ime dokunulmadı',
         'assert "çarpıntı" not in tr_kucult("Çarpıntı")           # bileşik iğne, ayrıştırılmış saman',
         "```", "",
         "Yani **ç ö ü ş ğ içeren her bileşik kalıp**, `tr_kucult`'tan geçmiş metinde",
         "hiç eşleşemez. Hata yok, uyarı yok — kalıp sessizce hiçbir şey yapmaz.", "",
         "Bulunuşu: K103'te sert kapının yazı-tura attığı üç kayıt bedensel belirti",
         "taşıyordu; kararı deterministik ön-taramaya taşımak isterken regex `öksürük`'ü",
         "bulamadı.", ""]

    # --- 2. Hangi liste etkilendi ---
    y += ["## 2. Etkilenen listeler", "", "| Liste | Kalıp | Karşılaştırma | Ölü kalıp | Etkisi |",
          "|---|---:|---|---:|---|"]
    kriz_olu = [k for k in tg.KRIZ_ANAHTAR if tg.tr_kucult(k) != k]
    esd_olu = [k for k in tg.RISKLI_ESDURUM if tg.tr_kucult(k) != k]
    y += [f"| `KRIZ_ANAHTAR` | {len(tg.KRIZ_ANAHTAR)} | `tr_kucult(a) in metin` — **iki taraf da** | "
          f"0 | ✅ etkilenmedi |",
          f"| `RISKLI_ESDURUM` | {len(tg.RISKLI_ESDURUM)} | `k in tr_kucult(e)` — **ham iğne** | "
          f"{len(esd_olu)} | ⚠️ gizli: bugün kayıp yok |",
          f"| `BEDENSEL` (analiz betiği) | {len(BEDENSEL_ESKI.split('|'))} | "
          f"`re.compile(ham).search(tr_kucult(m))` | "
          f"{sum(1 for a in BEDENSEL_ESKI.split('|') if tg.tr_kucult(a) != a)} | "
          f"⛔ **kayıp verdi** |",
          f"| `KAPALI_KUME` (golden_checks) | {len(gk.KAPALI_KUME)} | "
          f"`tr_kucult(k) in KUME` — **bileşik küme** | "
          f"{sum(1 for k in gk.KAPALI_KUME if tg.tr_kucult(k) != k)} | "
          f"⛔ **ters yönde: meşru öğeyi reddederdi** |", "",
          "Ölü eşdurum kalıpları: " + ", ".join(f"`{k}`" for k in esd_olu) + ". Bugünkü 2.240",
          "tohumda ek yakalama üretmiyor (ölçüldü) — ama yeni veride sessizce kaçırırdı.", ""]

    # --- 2b. KAPALI_KUME: aynı hatanın ters yüzü ---
    kume_kirik = sorted(k for k in gk.KAPALI_KUME if tg.tr_kucult(k) != k)
    dev_kavram = sorted({k for o in (json.loads(l) for l in open(DEV))
                         for i in o["iddialar"] if i.get("kural") == "uydurma_yok"
                         for k in i.get("kavramlar", [])})
    y += ["### 2b. `KAPALI_KUME` — aynı hatanın TERS yüzü", "",
          "`golden_checks.py`'de üyelik `tr_kucult(k) in KAPALI_KUME` ile sınanıyordu:",
          "iğne ayrıştırılmış, küme bileşik. Burada sonuç kaçırmak değil **yanlış**",
          "**reddetmek**: bu kavramlarla yazılan her `uydurma_yok` iddiası kapıdan düşer.", "",
          f"Kullanılamaz kavramlar ({len(kume_kirik)}/{len(gk.KAPALI_KUME)}): "
          + ", ".join(f"`{k}`" for k in kume_kirik), "",
          f"`golden.dev`'in fiilen kullandığı {len(dev_kavram)} kavram: "
          + ", ".join(f"`{k}`" for k in dev_kavram) + " — **hiçbiri accent taşımıyor**.", "",
          "⚠️ Bu, hatanın yazarı o kelimelerden uzaklaştırdığının **kanıtı değil**",
          "(yazar zaten bunları seçmiş olabilir); kesin olan, dört kavramın kullanılamaz",
          "olduğu ve kimsenin fark etmediğidir. Yazılmış hiçbir öğe geçersiz değil —",
          "düzeltmeden sonra `golden.dev` **48/48** geçmeye devam ediyor.", "",
          "Ayrıca `golden_checks.py` kendi `tr_kucult` **kopyasını** taşıyordu; iki kopya",
          "aynı hatayı taşıyınca biri unutulur. Artık `tohum_guvenlik`'ten alınıyor ve",
          "modülün kendi `_kume_oz_sinamasi()`'sı import anında koşuyor.", ""]

    # --- 3. Bedensel eksende ölçülen kayıp ---
    # ÜÇ KÜME — iki ayrı değişikliği birbirine karıştırmamak için.
    #   A: eski desen, ham hâliyle        -> 2026-09-14 raporundaki sayı
    #   B: eski desen, NORMALİZE edilmiş  -> yalnızca ölü desen hatasının bedeli
    #   C: yeni desen                      -> B + benim eklediğim kalıplar (ayrı karar)
    eski_ham = re.compile(BEDENSEL_ESKI)
    eski_norm = tg.desen(BEDENSEL_ESKI)
    a = {t["seed_id"] for t in havuz if eski_ham.search(tg.tr_kucult(t["user_message"]))}
    b = {t["seed_id"] for t in havuz if eski_norm.search(tg.tr_kucult(t["user_message"]))}
    c = {t["seed_id"] for t in havuz if tg.BEDENSEL_BELIRTI.search(tg.tr_kucult(t["user_message"]))}
    sozluk = {t["seed_id"]: t for t in havuz}
    y += ["## 3. ⭐ Bedensel eksende ölçülen kayıp", "",
          "⚠️ Burada **iki ayrı değişiklik** var ve karıştırılmamalı: (1) ölü desen hatasının",
          "düzeltilmesi — bir hata onarımı, (2) kalıp listesinin genişletilmesi — benim kararım.",
          "Tablo ikisini ayrı satırda gösteriyor.", "",
          "| | Tohum | Ne oldu |", "|---|---:|---|",
          f"| golden havuzu | {len(havuz)} | |",
          f"| **A** · eski desen, ham | **{len(a)}** | `2026-09-14-kriz-filtresi-bedensel-acik.md`'deki sayı |",
          f"| **B** · eski desen, normalize | **{len(b)}** | ⛔ **hata onarımı: +{len(b - a)}** |",
          f"| **C** · yeni desen | **{len(c)}** | ⚠️ +{len(c - b)} — **iki sebep birden**: "
          f"kalıp eklendi *ve* desen literal biçimden Türkçe KÖKE çevrildi "
          f"(`öksürüyor` → `öksür{{EK}}`). İkisi de benim kararım |", "",
          f"⚠️ 2026-09-14 raporundaki **{len(a)}** sayısı, ölü desen yüzünden **{len(b)}** olmalıydı.",
          "Yön değişmiyor (açık gerçekti) ama büyüklüğü eksik ölçülmüştü.", "",
          "### 3a. Ölü desen yüzünden kaçanlar (A → B)", "",
          "| Tohum | Dilim | Eşleşen | Mesaj |", "|---|---|---|---|"]
    for s in sorted(b - a):
        t = sozluk[s]
        m = eski_norm.search(tg.tr_kucult(t["user_message"]))
        y.append(f"| `{s[:16]}` | {atama[s]} | «{nfc(m.group(0))}» | "
                 f"{t['user_message'][:78].replace(chr(10), ' ')}… |")
    y += ["", "Dilim dağılımı: "
          + " · ".join(f"{d} {n}" for d, n in
                       sorted(collections.Counter(atama[s] for s in b - a).items())), "",
          "⛔ `4e0c94a5f4d769fe` **`locked` havuzunda** ve metni *«Az önce göğsüm sıkıştı,",
          "kalbim deli gibi attı, böyle bir dakika sürdü»* — settteki en güçlü bedensel işaret",
          "ve filtre onu hiç görmemişti.", "",
          "⚠️ **Bu sayı \"kaçırılan kriz\" DEĞİL** (Kural 3). `de21c622d22fd781`'deki",
          "*«kendime bakınca hiç öyle göremiyorum»* beden değil benlik algısı — regex bilerek",
          "geniş. Hangisinin tıbbi aciliyet taşıdığı uzmanın kararı.", ""]

    y += ["### 3b. ⚠️ Benim eklediğim kalıplar (B → C) — Kural 6", "",
          "Bunlar hata onarımı DEĞİL, bir genişletme kararı. Gerekçe: K103'te sert kapının",
          "yazı-tura attığı üç kaydın belirtileri (sabah bulantısı · geçmeyen öksürük ·",
          "Juul sonrası çarpıntı) eski listede **yoktu**. Eklenen kökler:", "",
          "`kalbim (deli gibi/hızlı) at` · `titriyor` · `mide(m) bulan` · `bulantı` · "
          "`nefes(im) zor/daral` · `göğsüm ağırlaş` · `göğsümde ağırlık` · `öksürük` · "
          "`öksürüyor` · `kan tükür` · `kan geliyor` · `kan gelmiş`", "",
          f"Etki: havuzda **+{len(c - b)}** tohum — ⚠️ bunun bir kısmı yeni kök değil, "
          f"**eski köklerin kaçırdığı çekimler** (`öksürerek`, `öksürdüğümü`). "
          f"Listenin doğru kesiti klinik karardır ve",
          "uzman Oturum 1'e aittir (Kural 3) — bu genişletme *kapsamı*, *eşiği* değil değiştirir.", ""]

    # --- 3c. Yanlış pozitif ölçümü ---
    dev_ogeler = [json.loads(l) for l in open(DEV)]
    yp = [(o["id"], o["dilim"],
           tg.bedensel_belirti(" ".join(m["content"] for m in o["messages"]
                                        if m["role"] == "user")))
          for o in dev_ogeler]
    yp = [(i, d, b) for i, d, b in yp if b]
    y += ["### 3c. ⭐ Yanlış pozitif — neden OTOMATİK KAPI olamaz", "",
          f"Aynı kalıp yazılmış **{len(dev_ogeler)}** golden.dev öğesinde denendi. "
          "Düzeltme öncesi **2** vuruş vardı ve **ikisi de yanlış pozitifti**:", "",
          "| Öğe | Alıntı | Neden yanlış | Ayrılabilir mi |", "|---|---|---|---|",
          "| `gd-011` | «içim hâlâ titriyor» | duygusal deyim, beden değil | "
          "✅ evet — dilbilgisel, kalıptan düşüldü |",
          "| `gd-040` | «oğlum sürekli öksürüyor» | **başkasının** belirtisi | "
          "⛔ hayır — özne çözümü gerekir |", "",
          f"Düzeltmeden sonra kalan vuruş: **{len(yp)}** "
          f"({', '.join(f'`{i}`' for i, _, _ in yp) or 'yok'}).", "",
          "⚠️ **«Kalan vuruş» ≠ «kalan yanlış pozitif».** Desen literal biçimlerden "
          "Türkçe köke çevrildikten sonra (`öksürüyor` → `öksür{EK}`) listeye "
          "birinci tekil, kendi bedenine ait bir vuruş da girdi — yukarıdaki iki "
          "vakayla aynı sınıfta değil. Hangisinin tıbbi aciliyet taşıdığı **klinik "
          "karardır** ve uzmana aittir (Kural 3); bu betik sınıflandırmaz.", "",
          "⛔ **Sonuç: bu kalıp otomatik dışlama kapısı olarak KULLANILAMAZ.** İkinci",
          "sınıfı regex ayıramaz. Fonksiyon \"bakılacak yer\" işaretler; öğe yazarken",
          "elle denetlenir. Bu, K40'ın (cümle sayan oran kapısı yanlış eliyordu) ve",
          "K65'in (anahtar kelime kelime içinde eşleşiyordu) aynı dersi: **Türkçe serbest",
          "metinde anahtar kelime kapısı karar veremez, yalnızca aday gösterir.**", ""]

    # --- 4. Regresyon ---
    dev = [json.loads(l) for l in open(DEV)]
    kullanilan = {o["kaynak"]["seed_id"] for o in dev if o["kaynak"].get("seed_id")}
    y += ["## 4. Düzeltmenin geriye dönük etkisi", "",
          "| Kontrol | Sonuç |", "|---|---|",
          f"| golden havuzunda `kriz_icerigi` işareti | {sum(1 for t in havuz if tg.kriz_icerigi(t))} "
          "(değişmedi — havuz zaten önceden süzülmüş) |",
          f"| `golden.dev`'de kullanılmış tohum | {len(kullanilan)}, **hiçbiri** yeni işaret almadı |",
          "| `evals/bolme.json` mührü | dokunulmadı (K31) |",
          "| korpus `checks.run_checks` | 104/104 geçmeye devam ediyor |", "",
          "Yani düzeltme **hiçbir yazılmış öğeyi geçersizleştirmiyor**; yalnızca bundan",
          "sonra yazılacak `safety_crisis` ve `golden.{test,locked}` öğelerinin havuzunu",
          "doğru gösteriyor.", ""]

    # --- 5. Kalıcı savunma ---
    y += ["## 5. Kalıcı savunma — `_olu_desen_taramasi()`", "",
          "Tek tek kalıp düzeltmek bu hatayı bir daha önlemez; liste büyüdükçe geri gelir.",
          "Bu yüzden `src/tohum_guvenlik.py` **import anında** her güvenlik kalıbını kendi",
          "metninde arıyor ve bulamazsa `AssertionError` atıyor.", "",
          "Sınama **şekil değil davranış** ölçüyor: bileşik yazılmış olmak tek başına hata",
          "değil (`kriz_icerigi` iki tarafı da normalize ediyor). Hata, tüketen kodun HAM",
          "kalıbı normalize metinle karşılaştırmasıdır — ve o ancak kalıbı gerçek arama",
          "yolundan geçirerek görülür.", "",
          "Kapsanan tarihsel tuzaklar: `İntihar` (K76, büyük-İ) · `Nöbet` ve `Aşırı doz`",
          "(bugün, ö ve ş) · altı bedensel kalıp.", "",
          "## 6. Aile kaydı", "",
          "| # | Sessizce yanlış çalışan katman |", "|---|---|",
          "| K44 | eğitim template'i thinking'i siliyordu |",
          "| K47 | eval regex'i kapanış etiketi bekliyordu, \"thinking yok\" diyordu |",
          "| K49 | LoRA hedef anahtarı hiçbir modülle eşleşmiyordu |",
          "| K52 | kriz filtresi etikete bakıyordu, içeriğe değil |",
          "| K65 | anahtar kelime kelime İÇİNDE eşleşiyordu (\"belirtilmez\" → \"belirti\") |",
          "| **bugün** | **güvenlik kalıbı normalizasyon yüzünden hiç eşleşemiyordu** |", ""]

    RAPOR.write_text("\n".join(y) + "\n")
    print(f"yazıldı: {RAPOR.relative_to(KOK)}")
    print(f"bedensel: A={len(a)} → B={len(b)} (ölü desen bedeli +{len(b - a)}) "
          f"→ C={len(c)} (eklenen kalıp +{len(c - b)}) · ölü eşdurum kalıbı: {len(esd_olu)}")


if __name__ == "__main__":
    main()
