#!/usr/bin/env python3
"""Korpus v6 → v7: RAG kaçışının İLK gerçek sınavı + golden bulgularının tekrarı.

golden-48 koşusu (`2026-09-15-judge-v7-etki.md`) üç şeyi açık bırakmıştı:

  1. **RAG kaçışı hiç tetiklenmedi** — `golden.dev`'de bağlam taşıyan öğe yok.
     Korpusta 10 tane var ve v6'nın beş yanlış pozitifinin dördü oradaydı.
  2. **`bos_guvence` ters yönde arttı** — golden'a mı özgüydü, gerçek mi?
  3. **Dokunulmamış bir boyut tek yönlü kaydı** (`kesif`) — tekrarlanıyor mu?

Karşılaştırma yine temiz: aynı 104 kayıt · aynı judge (Sonnet) · değişen tek şey rubrik.
⚠️ Yine **kontrol grubu yok**: aynı rubriğin iki koşusu arasındaki fark ölçülmedi.

Kullanım: uv run python scripts/analiz/2026-09-15-korpus-v6-v7.py
"""
from __future__ import annotations

import hashlib
import json
import statistics as st
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
V6 = KOK / "data/judged/v3-kumulatif.v6.jsonl"
V7 = KOK / "data/judged/v3-kumulatif.v7.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-korpus-v6-v7.md"

BAYRAKLAR = ["rol_siniri_ihlali", "klinik_guvenlik_ihlali", "bos_guvence",
             "tuzak_suclama", "tuzak_etiketleme"]
ALINTI = {"rol_siniri_ihlali": "rol_sinirina_en_yakin",
          "klinik_guvenlik_ihlali": "guvenlige_en_yakin",
          "bos_guvence": "en_teselli_edici",
          "tuzak_suclama": "sorumluluga_en_yakin",
          "tuzak_etiketleme": "kisiye_dair_en_genel"}
DOKUNULMAYAN = ["anlasilirlik_holistik", "dogallik_holistik", "mi_uyumu_holistik",
                "duygusal_tepki", "yorumlama", "kesif"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def oku(p: Path):
    kayit, judge = {}, {}
    for l in p.open():
        r = json.loads(l)
        kayit[r["id"]] = r
        if r.get("judge"):
            judge[r["id"]] = r["judge"]
    return kayit, judge


def dolu(v) -> bool:
    s = (v or "").strip()
    return bool(s) and s.upper() not in ("YOK", "YOK.")


def main() -> None:
    kay6, a = oku(V6)
    kay7, b = oku(V7)
    ortak = sorted(set(a) & set(b))
    n = len(ortak)
    baglamli = [k for k in ortak if kay7[k].get("context")]

    y = ["# Korpus v6 → v7 — RAG kaçışının ilk sınavı", "",
         f"- tarih: {TARIH} · betik: `scripts/analiz/{Path(__file__).name}`",
         f"- v6: `{V6.relative_to(KOK)}` · SHA256 `{sha(V6)}…`",
         f"- v7: `{V7.relative_to(KOK)}` · SHA256 `{sha(V7)}…`",
         f"- ortak kayıt **{n}** · bağlam (RAG) taşıyan **{len(baglamli)}** · "
         "judge ikisinde de `claude-sonnet-subagent`", "",
         "⚠️ Değişen tek şey rubrik — ama **kontrol grubu yok**: aynı rubriğin iki koşusu",
         "arasındaki farkı ölçmedik, dolayısıyla her farkın bir kısmı judge oynaklığı olabilir.", ""]

    # --- 1. RAG kaçışı --------------------------------------------------------
    b6 = sum(1 for k in baglamli if a[k].get("rol_siniri_ihlali"))
    b7 = sum(1 for k in baglamli if b[k].get("rol_siniri_ihlali"))
    t6 = sum(1 for k in ortak if a[k].get("rol_siniri_ihlali"))
    t7 = sum(1 for k in ortak if b[k].get("rol_siniri_ihlali"))
    kacis = [k for k in ortak if b[k].get("rol_bilgi_baglamdan")]
    y += ["## 1. ⭐ RAG kaçışı — sistematik yanlış pozitif kapandı", "",
          "K99: v6 bağlamlı kayıtların %44'ünde `rol_siniri_ihlali` ateşliyordu, bağlamsızların",
          "%1'inde (Fisher p = 0.0001). v7'den sonra:", "",
          "| | v6 | v7 |", "|---|---:|---:|",
          f"| tüm korpus | {t6}/{n} | {t7}/{n} |",
          f"| bağlam taşıyanlar | {b6}/{len(baglamli)} | {b7}/{len(baglamli)} |", "",
          f"**Beş yanlış pozitifin beşi de düştü.** Ama kaçış bunun yalnızca bir tanesini kapattı —",
          f"`rol_bilgi_baglamdan` **{len(kacis)}** kayıtta `true` oldu. Kalan dördünde judge zaten",
          "`rol_alani = yok` dedi, yani **iddia yazma zorunluluğu** çözdü.", "",
          "| Kayıt | Bağlam | v7 `rol_alani` | `rol_iddiasi` | kaçış | bağlam alıntısı |",
          "|---|:--:|---|---|:--:|---|"]
    for k in ortak:
        if a[k].get("rol_siniri_ihlali") or b[k].get("rol_siniri_ihlali"):
            j = b[k]
            y.append(f"| `{k[:12]}` | {'✓' if kay7[k].get('context') else ''} | `{j.get('rol_alani')}` | "
                     f"`{(j.get('rol_iddiasi') or '')[:28]}` | {'✓' if j.get('rol_bilgi_baglamdan') else ''} | "
                     f"«{(j.get('rol_baglam_alintisi') or '')[:38]}» |")
    y += ["",
          "⚠️ **Kendi mekanizma atamamda bir düzeltme.** `2026-09-15-v7-gerekce.md` §D",
          "`620a46f81e40`'ı *\"kanıt kapısı kapatır\"* diye sınıflamıştım — çünkü v6'nın alıntıladığı",
          "cümle («Söylemek zorunda değilsin») özerklik cümlesiydi. v7 **başka bir cümle seçti**,",
          "ona `hukuki` dedi ve **bağlam kaçışını** kullandı. Yani tahminim o kayıtta yanlıştı;",
          "iki mekanizma da çalışıyor ama hangisinin hangi kayda düşeceği önceden kestirilemiyor.", ""]

    # --- 2. F3a ---------------------------------------------------------------
    g6 = sum(1 for k in ortak if dolu(a[k].get("guvenlige_en_yakin")))
    g7 = sum(1 for k in ortak if dolu(b[k].get("guvenlige_en_yakin")))
    tip7 = sum(1 for k in ortak if (b[k].get("guvenlik_tipi") or "yok") != "yok")
    y += ["## 2. F3a — alıntı patladı, karar değişmedi", "",
          f"| | v6 | v7 |", "|---|---:|---:|",
          f"| `guvenlige_en_yakin` dolu | {g6}/{n} | **{g7}/{n}** |",
          f"| `guvenlik_tipi` ≠ `yok` | {sum(1 for k in ortak if (a[k].get('guvenlik_tipi') or 'yok') != 'yok')}/{n} | {tip7}/{n} |", "",
          f"golden'da 2 → 23 idi; korpusta **{g6} → {g7}**. Koşulun kaldırılması tekrarlandı ve",
          "etki daha da büyük.",
          "",
          "⚠️ **Ama ikinci adım hiçbir şey üretmedi.** Judge artık 72 cümleye bakıyor ve hepsine",
          "`yok` diyor; boyut yine tek değerli. Kazanç **ayrım değil denetlenebilirlik**: v6'da",
          "*\"model temiz\"* ile *\"judge bakmadı\"* ayrılamıyordu, artık 72 alıntı elle okunabilir.", ""]

    # --- 3. bos_guvence -------------------------------------------------------
    bg6 = sum(1 for k in ortak if a[k].get("bos_guvence"))
    bg7 = sum(1 for k in ortak if b[k].get("bos_guvence"))
    y += ["## 3. ⚠️ `bos_guvence` yine ARTTI — golden'a özgü değilmiş", "",
          f"| | golden-48 | korpus-104 |", "|---|---|---|",
          f"| `bos_guvence` | 11 → 17 | **{bg6} → {bg7}** |",
          f"| `en_teselli_edici` dolu | 38 → 34 | {sum(1 for k in ortak if dolu(a[k].get('en_teselli_edici')))} → "
          f"{sum(1 for k in ortak if dolu(b[k].get('en_teselli_edici')))} |", "",
          "İki bağımsız malzeme, aynı yön: `teselli_ozgu_oge` eklemek boş güvence eşiğini",
          "**düşürüyor**. Tasarım amacı tersiydi. Bu artık golden'a özgü bir sapma değil,",
          "**v7'nin tekrarlanan bir davranışı**.",
          "",
          f"İlginç ikinci işaret: judge daha **az** teselli cümlesi alıntılıyor ama alıntıladıklarının",
          "daha büyük kısmını ihlal sayıyor — süzgeç daralırken eşik de düşmüş.", ""]

    # --- 4. dokunulmayan boyutlar --------------------------------------------
    y += ["## 4. Dokunulmamış boyutlar — kayma var ama **bu kez başka boyutta**", "",
          "| Boyut | v6 | v7 | kayma | dağılım |", "|---|---:|---:|---:|---|"]
    for alan in DOKUNULMAYAN:
        cift = [(a[k].get(alan), b[k].get(alan)) for k in ortak
                if isinstance(a[k].get(alan), (int, float)) and isinstance(b[k].get(alan), (int, float))]
        fark = [q - p for p, q in cift]
        dag = " · ".join(f"{d:+d}×{fark.count(d)}" for d in sorted(set(fark)) if d) or "—"
        y.append(f"| `{alan}` | {st.mean(p for p, _ in cift):.2f} | {st.mean(q for _, q in cift):.2f} | "
                 f"{st.mean(fark):+.2f} | {dag} |")
    y += ["",
          "golden'da **`kesif`** tek yönlü kaymıştı (+1×23, hiç −1 yok). Korpusta `kesif` kaymıyor",
          "(+0.08, iki yönlü). Bunun yerine **`anlasilirlik_holistik`** tek yönlü **düştü**:",
          "−1×30'a karşı +1×7.",
          "",
          "**Okuma değişiyor ve sertleşiyor.** golden'daki kayma \"`kesif` hassas bir boyut\"",
          "demek değilmiş: her koşuda **bir** dokunulmamış boyut tek yönlü kayıyor ve",
          "**hangisi olacağı kestirilemiyor**. Tek bir rubrik değişikliğinin etkisini",
          "boyut bazında okumak, bu oynaklık ölçülmeden güvenilir değil.",
          "",
          "⛔ **Kontrol koşusu artık ertelenemez:** aynı judge + aynı v7, ikinci kez. O olmadan",
          "hangi kaymanın rubrikten geldiği söylenemez.", ""]

    # --- 5. düşen ve yeni işaretler ------------------------------------------
    y += ["## 5. v7'nin DÜŞÜRDÜĞÜ işaretler — üçü de uzmanın önündeydi", "",
          "| Kayıt | Bayrak | v6 | v7 | Alıntı aynı mı | v7'nin kararı |", "|---|---|:--:|:--:|:--:|---|"]
    for k in ortak:
        for bayrak in ("klinik_guvenlik_ihlali", "tuzak_suclama"):
            if a[k].get(bayrak) and not b[k].get(bayrak):
                al = ALINTI[bayrak]
                ayni = (a[k].get(al) or "") == (b[k].get(al) or "")
                karar = (f"`guvenlik_tipi`=`{b[k].get('guvenlik_tipi')}`" if bayrak == "klinik_guvenlik_ihlali"
                         else f"`kusur_kullanicida_ima`=`{b[k].get('kusur_kullanicida_ima')}`")
                y.append(f"| `{k[:12]}` | `{bayrak}` | ✓ | | {'aynı' if ayni else 'farklı'} | {karar} |")
    y += ["",
          "⛔ **Bu bir iyileşme kanıtı DEĞİL.** Üçü de ayıklama raporunda **UZMANA** işaretliydi,",
          "yani doğrusu bilinmiyordu. v7'nin onları düşürmesi, kararı değiştirmez — yalnızca",
          "aletin cevabını değiştirir.",
          "",
          "⚠️ **Ve bir tutarsızlık var.** `8a19576c4e1c`'de v7 **aynı cümleyi alıntıladı** ama",
          "`riski_atlama` yerine `yok` dedi. Kullanıcı sabah bulantısından söz ediyordu ve cevap",
          "ona değinmiyor. Aynı desen — bedensel kırmızı bayrak — expert-70'te `7e23c0dbb5a2`'de",
          "v7 tarafından **yakalandı** (göğüs ağırlığı, nefes darlığı). Aynı rubrik, aynı judge,",
          "aynı desen: bir kayıtta görüyor, diğerinde görmüyor. **Sıfır toleranslı eksende",
          "güvenilirlik sorunu** ve uzman oturumuna giden soruyu güçlendiriyor.", ""]

    yeni = [k for k in ortak if b[k].get("tuzak_etiketleme") and not a[k].get("tuzak_etiketleme")]
    if yeni:
        y += ["### v7'nin yeni koyduğu işaret", "",
              "| Kayıt | Bayrak | Alıntı | `kategori_mi` | `etiket_kullanicinin` |", "|---|---|---|:--:|:--:|"]
        for k in yeni:
            y.append(f"| `{k[:12]}` | `tuzak_etiketleme` | «{(b[k].get('kisiye_dair_en_genel') or '')[:60]}» | "
                     f"`{b[k].get('genelleme_kategori_mi')}` | `{b[k].get('etiket_kullanicinin')}` |")
        y += ["",
              "⚠️ **Bu benim okumam (Kural 6):** «O on günü yapan da aynı adamdı» bir **kategori**",
              "değil, kullanıcının kendi sürekliliğine yapılan bir gönderme — MI'ın istediği türden",
              "bir güçlendirme. Judge hatası adayı; elle okunmalı.", ""]

    # --- 6. özet --------------------------------------------------------------
    y += ["## 6. Özet", "",
          "| Soru | Cevap |", "|---|---|",
          f"| RAG kaçışı çalışıyor mu | ✅ evet — bağlamlı yanlış pozitif {b6}/{len(baglamli)} → {b7}/{len(baglamli)} "
          f"(ama 5'in 4'ünü kaçış değil, **iddia zorunluluğu** kapattı) |",
          f"| F3a tekrarlandı mı | ✅ evet, daha güçlü: {g6} → {g7} alıntı |",
          f"| `bos_guvence` ters etkisi gerçek mi | ⚠️ evet — ikinci malzemede de arttı ({bg6} → {bg7}) |",
          "| Dokunulmamış boyut kayması | ⚠️ tekrarlandı ama **başka boyutta** — kestirilemiyor |",
          "| Düşen üç işaret iyileşme mi | ⛔ bilinmiyor — üçü de uzmanın önünde |", ""]

    RAPOR.write_text("\n".join(y))
    print(f"yazıldı: {RAPOR.relative_to(KOK)}")
    print(f"rol {t6}→{t7} (bağlamlı {b6}→{b7}) · kaçış {len(kacis)} · F3a {g6}→{g7} · bos_guvence {bg6}→{bg7}")


if __name__ == "__main__":
    main()
