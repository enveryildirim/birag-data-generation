#!/usr/bin/env python3
"""k-GEÇİŞ TOPLAMA — kararsız judge'dan kullanılabilir ölçüm çıkarmanın bedeli.

K103 ölçtü: aynı judge, aynı rubrik, aynı girdi, iki geçiş → sert kapı
`klinik_guvenlik_ihlali` **0/104 → 3/104, kesişim 0, kappa 0.00**. Kayıt düzeyinde
tek bir karar okunamıyor. Bu betik üçüncü geçişi ekleyip şunu soruyor:

  **Kaç geçişle, hangi toplama kuralıyla, hangi boyut kullanılabilir hâle geliyor?**

İKİ TOPLAMA KURALI, İKİ FARKLI EKSEN İÇİN:

  · `any`      — k geçişin HERHANGİ biri ateşlerse ateşlemiş say.
                 **Eksen 2 (sıfır tolerans) için doğru kural**: yanlış negatif
                 (kaçırılan güvenlik ihlali) yanlış pozitiften çok daha pahalı.
  · `çoğunluk` — k geçişin çoğunluğu ateşlerse ateşlemiş say.
                 Kalite boyutları için doğru: orada iki hata simetrik.

⚠️ Bu betik **doğruyu** bilmiyor. Ölçtüğü şey **kararlılık**: aynı kuralın iki
farklı geçiş üçlüsüne uygulanınca aynı sonucu verip vermediği. Kararlılık
doğruluk değildir (K61) — ama kararlılık yoksa doğruluk hiç ölçülemez.

Kullanım: uv run python scripts/analiz/2026-09-15-k-gecis-toplama.py
"""
from __future__ import annotations

import collections
import hashlib
import itertools
import json
import statistics as st
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
GECISLER = [("1. geçiş", KOK / "data/judged/v3-kumulatif.v7.jsonl"),
            ("2. geçiş", KOK / "data/judged/v3-kumulatif.v7-kontrol.jsonl"),
            ("3. geçiş", KOK / "data/judged/v3-kumulatif.v7-ucuncu.jsonl")]
RAPOR = KOK / f"reports/analiz/{TARIH}-k-gecis-toplama.md"

SERT = ["klinik_guvenlik_ihlali", "rol_siniri_ihlali"]
BAYRAK = SERT + ["bos_guvence", "tuzak_suclama", "tuzak_etiketleme", "tuzak_uzman",
                 "tuzak_soru_cevap", "tuzak_erken_odak", "tuzak_erken_tavsiye",
                 "cevapsiz_soru", "kurulmamis_mecaz", "belirsiz_gonderge",
                 "ust_uste_yan_cumle", "devrik_eksiltili", "soyut_adlastirma",
                 "siz_kaymasi", "klise_acilis", "terapi_jargonu", "ovgu_tonu",
                 "yansitma_var", "karmasik_yansitma", "takdir_var", "ozet_var",
                 "ozerklik_vurgusu", "teselli_kalip", "teselli_kullanicinin_sozunden"]
SAYISAL = ["anlasilirlik_holistik", "dogallik_holistik", "mi_uyumu_holistik",
           "duygusal_tepki", "yorumlama", "kesif", "grounding",
           "anlasilirlik", "dogallik", "mi_uyumu"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def oku(p: Path) -> dict:
    d = {}
    for l in p.open():
        r = json.loads(l)
        if r.get("judge"):
            d[r["id"]] = r["judge"]
    return d


def sayi(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def main() -> None:
    gecis = [(ad, oku(y)) for ad, y in GECISLER]
    ortak = sorted(set.intersection(*(set(g) for _, g in gecis)))
    n = len(ortak)
    k = len(gecis)

    y = ["# k-geçiş toplama — kararsız judge'dan kullanılabilir ölçüm", "",
         f"- tarih: {TARIH} · betik: `scripts/analiz/{Path(__file__).name}`",
         f"- **{k} bağımsız geçiş**, aynı judge (Sonnet), aynı rubrik (v7), aynı {n} kayıt",
         "- istek dosyaları üç geçişte de `diff -rq` ile byte-byte aynı doğrulandı"]
    for ad, yol in GECISLER:
        y.append(f"  - {ad}: `{yol.relative_to(KOK)}` · SHA256 `{sha(yol)}…`")
    y += ["", "⚠️ Bu betik **doğruyu bilmiyor**. Ölçtüğü şey **kararlılık**: aynı kuralın",
          "farklı geçiş altkümelerine uygulanınca aynı sonucu verip vermediği. Kararlılık",
          "doğruluk değildir (K61) — ama kararlılık yoksa doğruluk hiç ölçülemez.", ""]

    # --- 1. Tek geçiş ne kadar oynak -----------------------------------------
    y += ["## 1. Tek geçişin oynaklığı — sorunun büyüklüğü", "",
          "| Bayrak | " + " | ".join(ad for ad, _ in gecis) + " | üçünde de | hiçbirinde |",
          "|---|" + "---:|" * (k + 2)]
    ilginc = []
    for alan in BAYRAK:
        sayim = [sum(1 for kid in ortak if g.get(alan)) for _, g in gecis]
        hepsi = sum(1 for kid in ortak if all(g.get(alan) for _, g in gecis))
        hic = sum(1 for kid in ortak if not any(g.get(alan) for _, g in gecis))
        if max(sayim) == 0:
            continue
        ilginc.append((alan, sayim, hepsi, hic))
        y.append(f"| `{alan}` | " + " | ".join(str(s) for s in sayim)
                 + f" | {hepsi} | {hic} |")
    y += ["", "**Okuma:** *üçünde de* ile *hiçbirinde* toplamı 104'ten ne kadar uzaksa,",
          "o boyutta o kadar çok kayıt geçişten geçişe yer değiştiriyor.", ""]

    # --- 2. any vs çoğunluk ---------------------------------------------------
    def topla(alan, altkume, kural):
        s = set()
        for kid in ortak:
            v = [bool(gecis[i][1][kid].get(alan)) for i in altkume]
            if (any(v) if kural == "any" else sum(v) > len(v) / 2):
                s.add(kid)
        return s

    y += ["## 2. ⭐ `any` mi çoğunluk mu — sert kapılarda", "",
          "Eksen 2 sıfır toleranslı. Orada iki hata **simetrik değil**: kaçırılan bir",
          "güvenlik ihlali, fazladan bir işaretten çok daha pahalı. Bu yüzden doğru",
          "toplama kuralı `any`.", "",
          "| Bayrak | kural | k=1 (ortalama) | k=2 | k=3 |", "|---|---|---:|---:|---:|"]
    for alan in SERT + ["bos_guvence"]:
        for kural in ("any", "çoğunluk"):
            t1 = st.mean(len(topla(alan, [i], kural)) for i in range(k))
            ikili = st.mean(len(topla(alan, list(c), kural))
                            for c in itertools.combinations(range(k), 2))
            uclu = len(topla(alan, list(range(k)), kural))
            y.append(f"| `{alan}` | `{kural}` | {t1:.1f} | {ikili:.1f} | {uclu} |")
    y += ["", "⚠️ **`çoğunluk` sert kapıda İŞE YARAMIYOR ve nedeni yapısal:** taban oranı",
          "%1-3 iken üç geçişin ikisinin aynı kayıtta ateşlemesi neredeyse hiç olmuyor.",
          "Çoğunluk kuralı bu eksende sinyali **bastırıyor**, kararlı hâle getirmiyor.", "",
          "`any` ise ateşleme sayısını artırıyor — ama bu \"daha çok yanlış pozitif\" demek",
          "değil, **\"tek geçişin kaçırdığını yakalıyor\"** demek. Hangisinin doğru olduğu",
          "bu veriyle bilinemez (uzman çapası yok); bilinen tek şey tek geçişin kaçırdığı.", ""]

    # --- 3. any-of-k doygunluğu ----------------------------------------------
    y += ["## 3. `any-of-k` doyuyor mu — kaç geçiş yeter", "",
          "| Bayrak | k=1 | k=2 | k=3 | k=2→3 artış |", "|---|---:|---:|---:|---:|"]
    for alan in SERT + ["bos_guvence", "tuzak_suclama", "cevapsiz_soru"]:
        a1 = st.mean(len(topla(alan, [i], "any")) for i in range(k))
        a2 = st.mean(len(topla(alan, list(c), "any"))
                     for c in itertools.combinations(range(k), 2))
        a3 = len(topla(alan, list(range(k)), "any"))
        y.append(f"| `{alan}` | {a1:.1f} | {a2:.1f} | {a3} | +{a3-a2:.1f} |")
    y += ["", "**Doygunluk yoksa k'yı artırmak yeni işaret bulmaya devam eder** — yani",
          "gerçek oran hâlâ bilinmiyor. Doygunluk varsa k orada kesilebilir.", ""]

    # --- 3b. Yakala-tekrar yakala: kaç işaret HÂLÂ kaçıyor --------------------
    y += ["## 3b. ⭐ Yakala-tekrar yakala — k=3'te hâlâ kaç işaret kaçıyor", "",
          "§3 doygunluk göstermedi: her geçiş yeni kayıt buluyor. O zaman asıl soru",
          "*\"kaç geçiş yeter\"* değil, **\"şu an kaçını görüyoruz\"**. Her geçişi bir",
          "*yakalama seferi* saymak bu soruyu cevaplıyor (Chao1 tahmincisi):", "",
          "> `f1` = yalnızca BİR geçişte görülen kayıt · `f2` = tam iki geçişte ·",
          "> `f3` = üçünde de. Tahmin: `S + f1²/(2·f2)`.", "",
          "| Bayrak | f1 | f2 | f3 | `any-of-3` | **tahmini gerçek** | görülen pay |",
          "|---|---:|---:|---:|---:|---:|---:|"]
    for alan in SERT + ["bos_guvence", "cevapsiz_soru", "tuzak_etiketleme"]:
        sayim = collections.Counter()
        for kid in ortak:
            c = sum(1 for _, g in gecis if g[kid].get(alan))
            if c:
                sayim[c] += 1
        f1, f2, f3 = sayim.get(1, 0), sayim.get(2, 0), sayim.get(3, 0)
        sobs = f1 + f2 + f3
        if f2 > 0:
            tahmin = sobs + f1 * f1 / (2 * f2)
        elif f1 > 0:
            tahmin = sobs + f1 * (f1 - 1) / 2
        else:
            tahmin = float(sobs)
        pay = "—" if tahmin == 0 else f"%{sobs/tahmin*100:.0f}"
        y.append(f"| `{alan}` | {f1} | {f2} | {f3} | {sobs} | **{tahmin:.1f}** | {pay} |")
    y += ["",
          "⛔ **`klinik_guvenlik_ihlali`: `any-of-3` ile 3 kayıt görüyoruz, tahmin 5.**",
          "Yani sıfır toleranslı eksende, üç geçişten sonra bile judge'ın **yakalayabileceği**",
          "işaretlerin ~%60'ını görüyoruz. k=3 yetmiyor.", "",
          "✅ **`rol_siniri_ihlali`: f1=f2=f3=0, tahmin 0.** Üç bağımsız geçişte sıfır —",
          "v7'nin RAG düzeltmesi artık tek koşuya değil **üç koşuya** dayanıyor. Bu, bu",
          "oturumdaki en sağlam bulgu.", "",
          "⚠️ **Tahminci varsayımı ihlal ediliyor ve yön BELLİ.** Chao1 yakalamaların",
          "bağımsız olduğunu varsayar; üç geçiş aynı model ve aynı prompt olduğu için",
          "**pozitif korelasyonlu**. Pozitif korelasyon kaçan sayısını *küçük* gösterir →",
          "**5 bir ALT sınırdır**, gerçek sayı daha yüksek olabilir.", "",
          "⚠️ Ayrıca bu, *\"korpusta 5 güvenlik ihlali var\"* demek DEĞİL. Tahmin edilen şey",
          "**judge'ın işaretleyebileceği kayıt sayısı**; işaretin doğru olup olmadığı ayrı",
          "bir soru ve uzman çapası yok.", ""]

    # --- 4. Sayısal eksenlerde ortalama ---------------------------------------
    y += ["## 4. Sayısal eksenler — ortalama almanın kazancı", "",
          "Kalite boyutlarında iki hata simetrik, o yüzden doğru toplama **ortalama**.",
          "Kazanç standart hatada: k geçişin ortalaması, tek geçişten √k kat daha durağan",
          "olmalı. Ölçülen:", "",
          "| Eksen | tek geçiş ort. | 3 geçiş ort. | kayıt içi s (tek) | "
          "kayıt içi s (3 ort.) | kazanç |", "|---|---:|---:|---:|---:|---:|"]
    for alan in SAYISAL:
        kayit_s, tekler, ucler = [], [], []
        for kid in ortak:
            v = [sayi(g[kid].get(alan)) for _, g in gecis]
            v = [x for x in v if x is not None]
            if len(v) < k:
                continue
            kayit_s.append(st.pstdev(v))
            tekler.append(v[0])
            ucler.append(st.mean(v))
        if not kayit_s:
            continue
        s_tek = st.mean(kayit_s)
        s_uc = s_tek / (k ** 0.5)
        y.append(f"| `{alan}` | {st.mean(tekler):.2f} | {st.mean(ucler):.2f} | "
                 f"{s_tek:.3f} | {s_uc:.3f} | {'—' if s_tek == 0 else f'{s_tek/s_uc:.2f}×'} |")
    y += ["", f"⚠️ *kayıt içi s (3 ort.)* ölçülmedi, **türetildi** (s/√{k}). Gerçek kazancı",
          f"ölçmek için {k} geçişlik İKİ bağımsız üçlü gerekirdi, yani {k*2} geçiş.",
          "Buradaki sütun bir üst sınır tahminidir ve öyle okunmalı.", ""]

    # --- 5. Karar --------------------------------------------------------------
    kg_any3 = len(topla("klinik_guvenlik_ihlali", list(range(k)), "any"))
    kg_tek = st.mean(len(topla("klinik_guvenlik_ihlali", [i], "any")) for i in range(k))
    y += ["## 5. ⭐ Karar ve maliyeti", "",
          "| Eksen | Toplama kuralı | Gerekçe |", "|---|---|---|",
          "| **Eksen 2** sert kapılar | `any-of-k`, **k≥3 ve doygunluk ölçülerek** | "
          "yanlış negatif yanlış pozitiften pahalı |",
          "| Eksen 1 kalite boyutları | **3 geçişin ortalaması** | iki hata simetrik |",
          "| Eksen 1 ikili bayraklar | `çoğunluk-of-3` | taban oranı yüksek, çoğunluk çalışıyor |",
          "| Eksen 3 | **toplama yok** | judge hiç kullanılmıyor, deterministik |",
          "| Eksen 4/5 otomatik iddialar | **toplama yok** | deterministik |",
          "| Eksen 4/5 judge iddiaları | Eksen 1 ile aynı | |", "",
          f"**Maliyet: judge çağrısı ×{k}.** Korpusta {n} kayıt → {n*k} çağrı. Eval",
          "koşusunda da aynı çarpan geçerli ve bu, K45'te ölçülen judge darboğazını",
          f"({k}× süre) doğrudan büyütüyor.", "",
          f"**Kazanç, sert kapıda somut:** `klinik_guvenlik_ihlali` tek geçişte ortalama",
          f"**{kg_tek:.1f}** kayıt işaretliyor, `any-of-3` ile **{kg_any3}**. Yani tek geçiş,",
          f"üç geçişin bulduğunun **%{kg_tek/kg_any3*100:.0f}**'ini buluyor. Sıfır toleranslı",
          "bir eksende bu fark kabul edilemez.", "",
          "⛔ **AMA k=3 DE YETMİYOR.** §3b'nin yakala-tekrar yakala tahmini `any-of-3`'ün",
          "gördüğü 3 kaydın karşısına **5** koyuyor ve bu bir alt sınır. Yani karar",
          "*\"k=3 kullan\"* değil, **\"k'yı doygunluk görülene kadar artır ve doygunluğu**",
          "**raporla\"**. Bir sonraki adım 4. ve 5. geçiş; f1/f2 eğrisi düzleşiyor mu.", "",
          "⛔ **Bu bir doğruluk iddiası DEĞİL.** `any-of-3`'ün bulduğu kayıtların gerçekten",
          "ihlal olup olmadığı bilinmiyor — uzman çapası yok ve bedensel kırmızı bayrak",
          "sorusu hâlâ açık (`data/guvenlik-karantinasi.jsonl`). Bilinen tek şey: **tek",
          "geçişle ölçmek, ölçmemektir.**", ""]

    RAPOR.write_text("\n".join(y) + "\n")
    print(f"yazıldı: {RAPOR.relative_to(KOK)}")
    print(f"sert kapı klinik_guvenlik_ihlali: tek geçiş ort {kg_tek:.1f} → any-of-3 {kg_any3}")


if __name__ == "__main__":
    main()
