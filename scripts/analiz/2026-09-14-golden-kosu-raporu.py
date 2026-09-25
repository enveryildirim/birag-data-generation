#!/usr/bin/env python3
"""Golden koşu raporu — asıl soru geçme oranı değil, CETVELİN AYIRT EDİP ETMEDİĞİ.

Bir eval setinin ilk sınavı ölçtüğü modelde değil, kendindedir: hepsi geçen ya
da hepsi kalan bir set hiçbir şey ölçmez. Bu rapordaki her hüküm veriden
türetilir (K80 — rapor üreticisinin sabit hüküm yazdığı iki kez yakalandı).

Üç düzeyde bakar:
  · ÖĞE   — kaç öğe tüm iddialarını geçti
  · İDDİA — hangi iddia hiç ateşlemiyor (ölçmüyor) ya da hep ateşliyor (yanlış kurulmuş)
  · BOYUT — eşiksiz bütünsel boyutların dağılımı; korpus eşiği buradan önerilir

Kullanım: uv run python scripts/analiz/2026-09-14-golden-kosu-raporu.py <koşu-dizini>
"""
from __future__ import annotations

import collections
import hashlib
import json
import math
import statistics as st
import sys
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]

# Ayrım bandı — BİZİM konvansiyonumuz (Kural 6), literatürden gelmiyor.
AYRIM_ALT, AYRIM_UST = 0.10, 0.90


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p, d = k / n, 1 + z * z / n
    m = (p + z * z / (2 * n)) / d
    y = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, m - y), min(1.0, m + y))


def main() -> None:
    kosu_dir = Path(sys.argv[1])
    if not kosu_dir.is_absolute():
        kosu_dir = KOK / kosu_dir
    meta = json.loads((kosu_dir / "kosu.json").read_text())
    sonuclar = [json.loads(l) for l in open(kosu_dir / "sonuclar.jsonl")]
    rapor_yolu = KOK / f"reports/analiz/{TARIH}-golden-kosu-{meta['etiket']}.md"

    jr_hepsi = [x["judge"] for x in sonuclar if x["judge"] and "_hata" not in x["judge"]]

    def varyans_var(alan: str) -> bool | None:
        v = [j[alan] for j in jr_hepsi if j.get(alan) is not None]
        return None if not v else len(set(v)) > 1

    # Kör boyut: judge 48 cevap boyunca hiç varyans üretmemiş. O boyuttaki iddia
    # "geçti" dese de hiçbir şey ölçmüyor — eğitim sonrası da aynı sonucu verir.
    kor_alanlar = {d["ad"] for x in sonuclar for d in x["denetim"]
                   if d["tip"] == "judge" and varyans_var(d["ad"]) is False}

    def bilgilendirici(x: dict) -> list[dict]:
        return [d for d in x["denetim"]
                if d["gecti"] is not None and not (d["tip"] == "judge" and d["ad"] in kor_alanlar)]

    n = len(sonuclar)
    gecen = sum(1 for s in sonuclar if s["gecti"])
    bos = sum(1 for s in sonuclar if s["on_kosul"])
    denetlenemedi = sum(1 for s in sonuclar if s["denetlenemedi"])
    kesik = sum(1 for s in sonuclar if s["kesildi"])
    oran = gecen / n
    lo, hi = wilson(gecen, n)

    L = [f"# Golden koşu — `{meta['etiket']}`", "",
         # ⛔ Bu rapor HİÇ betik adı taşımıyordu — Kural 7'yi sessizce karşılamıyordu.
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · "
         f"**Koşu:** `{kosu_dir.relative_to(KOK)}`  ",
         f"**Set:** `{meta['set']}` · SHA256 "
         f"`{hashlib.sha256((KOK / meta['set']).read_bytes()).hexdigest()[:32]}…`  ",
         f"**Model:** `{meta['model']}` · **Adapter:** "
         f"{'`' + str(meta['adapter']) + '`' if meta['adapter'] else '**yok (baseline)**'}  ",
         f"**Koşucu:** `src/golden_eval.py` · **Rapor:** `scripts/analiz/{Path(__file__).name}`  ",
         f"**Tarih:** {meta['tarih'][:10]} · **thinking öneki:** "
         f"{'açık' if meta['thinking'] else 'kapalı'} · **max_tokens:** {meta['max_tokens']}  ",
         f"**Ham çıktı:** `{kosu_dir.relative_to(KOK)}/sonuclar.jsonl`", "", "---", "",
         "## 1. ⭐ Cetvel ayırt ediyor mu", "",
         "Bir eval setinin ilk sınavı ölçtüğü modelde değil **kendindedir**: hepsi geçen "
         "ya da hepsi kalan bir set hiçbir şey ölçmez. Bu yüzden ilk bakılan sayı budur.", "",
         "| | Öğe | Oran |", "|---|---:|---:|",
         f"| Tüm iddialarını geçti | {gecen} | %{oran*100:.0f} |",
         f"| En az bir iddiadan kaldı | {n - gecen - bos - denetlenemedi} | "
         f"%{(n-gecen-bos-denetlenemedi)/n*100:.0f} |",
         f"| Ön koşuldan düştü (boş cevap) | {bos} | %{bos/n*100:.0f} |",
         f"| Denetlenemedi (judge eksik) | {denetlenemedi} | %{denetlenemedi/n*100:.0f} |",
         f"| **Toplam** | **{n}** | |", "",
         f"Geçme oranı **%{oran*100:.0f}** · %95 Wilson **%{lo*100:.0f}-{hi*100:.0f}**", ""]

    # ── Kör iddiaları düşünce geriye ne kalıyor ──
    toplam_iddia = sum(1 for x in sonuclar for d in x["denetim"] if d["gecti"] is not None)
    kor_iddia = toplam_iddia - sum(len(bilgilendirici(x)) for x in sonuclar)
    olcusuz = [x["id"] for x in sonuclar if not bilgilendirici(x)]
    L += ["### 1b. Geçme oranının ne kadarı gerçek", "",
          "§3b'de judge'ın **kör** olduğu boyutlar çıkıyor: 48 cevabın hepsine aynı puanı "
          "verdiği boyutlar. O iddialardan \"geçmek\" bir kanıt değil, çünkü eğitim "
          "sonrası da aynı sonucu verecekler. Kör iddialar düşüldüğünde:", "",
          "| | Adet |", "|---|---:|",
          f"| Denetlenen iddia (toplam) | {toplam_iddia} |",
          f"| Bunlardan kör boyutta | **{kor_iddia}** (%{kor_iddia/toplam_iddia*100:.0f}) |",
          f"| Bilgilendirici iddia | {toplam_iddia - kor_iddia} |",
          f"| Hiçbir bilgilendirici iddiası kalmayan öğe | **{len(olcusuz)}** |", ""]
    if olcusuz:
        L += ["> ⚠️ Bu öğeler **hiç ölçülmemiş** sayılır: " +
              ", ".join(f"`{i}`" for i in olcusuz) +
              ". Eşikleri yalnızca judge'ın kör olduğu boyutlarda.", ""]
    else:
        L += ["> Her öğenin en az bir bilgilendirici iddiası var; kör boyutlar geçme "
              "oranını şişiriyor ama hiçbir öğeyi tek başına taşımıyor.", ""]

    if AYRIM_ALT <= oran <= AYRIM_UST:
        L += [f"**Cetvel ayırt ediyor.** Geçme oranı %{oran*100:.0f}, "
              f"%{AYRIM_ALT*100:.0f}-%{AYRIM_UST*100:.0f} bandının içinde — yani set ne "
              "herkesin geçtiği bir formalite ne de kimsenin geçemediği bir duvar. "
              "Eğitim sonrası bu sayının yükselmesi ölçülebilir.", ""]
    elif oran > AYRIM_UST:
        L += [f"⚠️ **Cetvel ÇOK KOLAY.** Eğitilmemiş model öğelerin %{oran*100:.0f}'ini "
              "geçiyor; iyileşme için yer kalmamış. İddia eşikleri yükseltilmeli.", ""]
    else:
        L += [f"⚠️ **Cetvel ÇOK ZOR ya da BOZUK.** Eğitilmemiş model yalnızca "
              f"%{oran*100:.0f} geçiyor. İki ihtimal ayrılmalı: eşikler gerçekten zor mu, "
              "yoksa iddialar yanlış mı kurulmuş? §3'teki hep-ateşleyen iddialara bakılır.", ""]

    if kesik:
        L += [f"> {kesik} öğede üretim `max_tokens`'a takıldı. Bu bir model kusuru değil "
              "koşu ayarı olabilir; §5'teki uzunluk dağılımına bakılmalı.", ""]

    # ── 2. Dilim ──
    L += ["## 2. Dilime göre", "", "| Dilim | Öğe | Geçen | Oran |", "|---|---:|---:|---:|"]
    for d, grup in sorted(collections.Counter(s["dilim"] for s in sonuclar).items(),
                          key=lambda x: -x[1]):
        alt = [s for s in sonuclar if s["dilim"] == d]
        g = sum(1 for s in alt if s["gecti"])
        L.append(f"| `{d}` | {len(alt)} | {g} | %{g/len(alt)*100:.0f} |")

    # ── 3. İddia düzeyi ──
    iddia_sayim: dict[tuple, list[int]] = collections.defaultdict(lambda: [0, 0])
    for s in sonuclar:
        for d in s["denetim"]:
            if d["gecti"] is None:
                continue
            k = (d["tip"], d["ad"])
            iddia_sayim[k][0] += 1
            iddia_sayim[k][1] += int(not d["gecti"])

    L += ["", "## 3. İddia düzeyi — hangi iddia ne kadar ateşliyor", "",
          "> İki uç da sorunludur: **hiç ateşlemeyen** iddia o öğelerde hiçbir şey ölçmüyor; "
          "**her zaman ateşleyen** iddia ya gerçek ve büyük bir açığı gösterir ya da yanlış "
          "kurulmuştur. İkisi bu tablodan ayrılmaz, §4'teki kanıtlara bakılır.", "",
          "| Tip | İddia | Denetlendi | Kaldı | Kalma oranı |", "|---|---|---:|---:|---:|"]
    for (tip, ad), (toplam, kalan) in sorted(iddia_sayim.items(), key=lambda x: -x[1][1]):
        L.append(f"| `{tip}` | `{ad}` | {toplam} | {kalan} | %{kalan/toplam*100:.0f} |")

    # ⭐ "Hiç ateşlemedi" iki farklı şey olabilir ve ayrılabilir: judge o boyutta
    # VARYANS üretiyorsa model gerçekten geçiyordur; varyans SIFIRSA judge o boyutta
    # kör demektir ve iddia hiçbir şey ölçmüyordur (K61'in şartı).
    hic = sorted(f"`{a}`" for (t, a), (tp, kl) in iddia_sayim.items() if kl == 0)
    hep = sorted(f"`{a}`" for (t, a), (tp, kl) in iddia_sayim.items() if kl == tp and tp >= 3)
    kor, gercek = [], []
    for (tip, ad), (tp, kl) in iddia_sayim.items():
        if kl or tip != "judge":
            continue
        (kor if varyans_var(ad) is False else gercek).append(f"`{ad}` ({tp} öğe)")
    L += ["", f"**Hiç ateşlemeyen ({len(hic)}):** " + (", ".join(hic) if hic else "yok"), "",
          f"**Her denetimde ateşleyen ({len(hep)}, en az 3 öğede):** "
          + (", ".join(hep) if hep else "yok"), "",
          "### 3b. \"Hiç ateşlemedi\" iki ayrı şeydir", "",
          "Bir iddianın hiç kalmaması ya modelin gerçekten geçtiği ya da **judge'ın o "
          "boyutta kör olduğu** anlamına gelir. İkisi ayrılabilir: judge o boyutta 48 "
          "cevap boyunca hiç varyans üretmiyorsa, ölçmüyordur (K61'in şartı).", ""]
    if kor:
        L += [f"⚠️ **Judge bu {len(kor)} boyutta hiç varyans üretmedi — iddia ölçmüyor:**", "",
              ", ".join(sorted(kor)), "",
              "> Bu öğelerin o iddiadan \"geçmesi\" bir başarı kanıtı DEĞİLDİR. "
              "Ya rubrik bu boyutu yakalayamıyor ya da eşik yanlış kurulmuş; "
              "eğitim sonrası koşuda da aynı sonucu vereceği için **fark ölçemez**.", ""]
    if gercek:
        L += [f"**Judge varyans üretti ama bu {len(gercek)} iddiada hiç kalan olmadı** — "
              "yani model bu öğelerde gerçekten geçiyor:", "",
              ", ".join(sorted(gercek)), ""]

    # ── 4. Kalan iddiaların kanıtı ──
    L += ["## 4. Kalan iddiaların kanıtı", "",
          "> Puan değil kanıt (K59/K62). Her satırda modelin ne yaptığı yazılı.", "",
          "| Öğe | İddia | Kanıt | Cevap (ilk 90 krk) |", "|---|---|---|---|"]
    for s in sonuclar:
        for d in s["denetim"]:
            if d["gecti"] is False:
                cevap = s["cevap"].replace("|", "·").replace("\n", " ")[:90]
                L.append(f"| `{s['id']}` | `{d['ad']}` | {d['kanit'][:55]} | {cevap}… |")

    # ── 5. Eşiksiz bütünsel boyutlar ──
    jr_var = [s for s in sonuclar if s["judge"] and "_hata" not in s["judge"]]
    L += ["", "## 5. Eşiksiz bütünsel boyutlar — korpus eşiği buradan önerilir", "",
          "Bu boyutlarda öğe eşiği yok (golden.dev raporu §4b); judge hepsini yine de "
          "puanladı. Dağılım, korpus düzeyi eşiğin nereye konacağını söyler.", ""]
    sayisal = ["anlasilirlik", "dogallik", "mi_uyumu", "grounding", "duygusal_tepki",
               "yorumlama", "kesif", "dil_butunlugu", "kisalik_dogallik"]
    ikili = ["siz_kaymasi", "klise_acilis", "terapi_jargonu", "bos_guvence", "ovgu_tonu",
             "belirsiz_gonderge", "kurulmamis_mecaz", "devrik_eksiltili", "soyut_adlastirma",
             "ust_uste_yan_cumle", "yansitma_var", "karmasik_yansitma", "ozet_var", "takdir_var"]
    L += ["| Boyut | n | Medyan | Ortalama | Min-Maks |", "|---|---:|---:|---:|---:|"]
    for alan in sayisal:
        v = [s["judge"][alan] for s in jr_var if s["judge"].get(alan) is not None]
        if v:
            L.append(f"| `{alan}` | {len(v)} | {st.median(v):.1f} | {st.mean(v):.2f} "
                     f"| {min(v)}-{max(v)} |")
    sifir = [a for a in sayisal
             if (v := [s["judge"][a] for s in jr_var if s["judge"].get(a) is not None])
             and len(set(v)) == 1]
    if sifir:
        L += ["", f"⚠️ **Sıfır varyanslı boyut ({len(sifir)}):** "
              + ", ".join(f"`{a}`" for a in sifir) +
              ". Bu boyut(lar)da judge 48 cevabın hepsine aynı puanı verdi — "
              "**korpus eşiği konulamaz**, çünkü eşik neyi ayırırsa ayırsın sonuç "
              "değişmez. K61: varyans yoksa ölçüm yoktur.", ""]
    L += ["", "| Bayrak | n | Ateşleyen | Oran |", "|---|---:|---:|---:|"]
    for alan in ikili:
        v = [s["judge"][alan] for s in jr_var if s["judge"].get(alan) is not None]
        if v:
            k = sum(1 for x in v if x)
            L.append(f"| `{alan}` | {len(v)} | {k} | %{k/len(v)*100:.0f} |")

    # ── 6. Uzman kuyruğu ──
    uzman = [(s["id"], d["ad"]) for s in sonuclar for d in s["denetim"] if d["tip"] == "uzman"]
    L += ["", "## 6. Uzman kuyruğu", "",
          f"{len(uzman)} iddia insan kararı bekliyor — bu koşuda denetlenmedi:", ""]
    L += [f"- `{i}` — {a}" for i, a in uzman]

    # ── 7. Uzunluk ve maliyet ──
    uz = [len(s["cevap"]) for s in sonuclar if s["cevap"]]
    L += ["", "## 7. Uzunluk ve maliyet", "", "| | |", "|---|---:|",
          f"| Cevap uzunluğu (medyan) | {int(st.median(uz)) if uz else 0} karakter |",
          f"| Cevap uzunluğu (min-maks) | {min(uz) if uz else 0}-{max(uz) if uz else 0} |",
          f"| `max_tokens`'a takılan | {kesik}/{n} |",
          f"| Üretim | {meta['uretim_sn']/60:.1f} dk ({meta['uretim_sn']/n:.1f} sn/öğe) |",
          f"| Judge | {meta['judge_sn']/60:.1f} dk ({meta['judge_sn']/n:.1f} sn/öğe) |", ""]
    # Çok turlu öğelerde bağlam içi taklit: yazdığım geçmiş turlarda thinking yok
    cok = [s for s in sonuclar if s["dilim"] == "cok_turlu"]
    tek = [s for s in sonuclar if s["dilim"] != "cok_turlu"]
    if cok and tek:
        ct = sum(1 for s in cok if s["thinking"])
        tt = sum(1 for s in tek if s["thinking"])
        if (ct / len(cok)) < (tt / len(tek)) - 0.2:
            L += ["> ⭐ **Bağlam içi taklit ölçüldü.** Tek turlu öğelerde model "
                  f"{tt}/{len(tek)} kez thinking üretti, çok turlu öğelerde "
                  f"{ct}/{len(cok)}. Aradaki farkın kaynağı benim yazdığım geçmiş "
                  "asistan turları: onlarda thinking yok, model bağlamı taklit edip "
                  "bırakıyor. **golden.dev raporundaki sızıntı uyarısı bu koşuda "
                  "doğrulandı** — çok turlu öğelerin sonucu kısmen benim yazdığım "
                  "geçmişi ölçüyor.", ""]
    dusunen = [s for s in sonuclar if s["thinking"]]
    if dusunen:
        L += [f"> ⚠️ **{len(dusunen)}/{n} öğede model istenmeden thinking üretti** "
              f"(`--thinking` {'açık' if meta['thinking'] else 'KAPALI'}). "
              "K46: eğitilmemiş model düşünceyi İngilizce kuruyor ve `max_tokens`'ı "
              "tüketerek cevapsız kalabiliyor.", ""]
    rapor_yolu.write_text("\n".join(L) + "\n")
    print(f"geçme oranı %{oran*100:.0f} ({gecen}/{n}) · yazıldı: {rapor_yolu.relative_to(KOK)}")


if __name__ == "__main__":
    main()
