#!/usr/bin/env python3
"""`slice` alanının ANLAMI v5 ile v6 arasında sessizce değişti.

⭐ **Nasıl çıktı:** subagent judge koşusunda `381` numaralı iş *«uydurma bir
ilaç/eş senaryosu + dayanaksız kurum yordamı»* diye işaretlendi. Kaydı
okurken dilimi `rag_tek_tur` göründü ⇒ *«RAG kaydıysa bağlam belgesi
nerede?»* diye bakıldı. Bağlam **yoktu** — ve sonra bunun tek bir kaydın
kusuru olmadığı çıktı.

⛔⛔ **Bulgu:** aynı alan adı iki ayrı şey demek.
  · **v4/v5** — `slice` = *kip × tur sayısı*. `rag_*` kayıtların
    **%100'ünde** bağlam var, `terapotik_*` kayıtların **%0'ında**.
    Alan tam bilgi taşıyor.
  · **v6** — sözlük **iki değere düştü** (`rag_tek_tur`, `cok_tur`);
    `terapotik_*` **kayboldu**, `cok_tur` **yeni**. Ve `rag_tek_tur`
    kayıtların yalnız **%35'inde** bağlam var ⇒ alan artık RAG hakkında
    **hiçbir şey söylemiyor**, yalnız tur sayısını söylüyor.

⛔⛔ **Hiçbir şey bunu göremezdi:** `schemas.py`'de alan `slice: str` —
`Literal` değil, yani şema her dizgeyi kabul eder; `checks.py`'de slice
denetimi **hiç yok**. İki kapı ailesi birden boş (T236 + T237).

⛔⛔⛔ **Neden acil:** veri kartı *«Dilim dağılımı»* satırını bu alandan
türetiyor (`datasets/v0.0.8/CARD.md`: *«`rag_tek_tur` 85…»*). v6 kayıtları
derlemeye girdiğinde kart, bağlamı olmayan yüzlerce kaydı **RAG kaydı diye
sayacak**. ⭐ Derleme v6 için **henüz koşmadı** ⇒ bu, yayımlanmış bir sayı
bozulmadan ÖNCE yakalandı (T121'in dersi).

⛔ Bu betik **hiçbir kaydı değiştirmez**. 530 kaydın etiketini yeniden
yazmak bir karardır, rutin bir düzeltme değil.

Çıktı: reports/analiz/2026-09-22-slice-anlami-degisti.md
"""
from __future__ import annotations

import collections
import glob
import json
import re
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-slice-anlami-degisti.md"
# ⛔ blok/sürüm/arınmış türevleri sayılmaz — aynı kayıt birden çok dosyada.
TUREV = re.compile(r"\.(blok\d+[a-z]*|v\d+|arinmis)\.")


def topla(desen: str):
    c, ctx, seen = collections.Counter(), collections.Counter(), set()
    for f in sorted(glob.glob(str(KOK / desen))):
        if TUREV.search(f):
            continue
        for l in open(f):
            r = json.loads(l)
            if r["id"] in seen:
                continue
            seen.add(r["id"])
            s = r.get("slice")
            c[s] += 1
            if r.get("context"):
                ctx[s] += 1
    return c, ctx, len(seen)


def main() -> int:
    eski_c, eski_x, eski_n = topla("data/candidates/v[45]-parti*.jsonl")
    yeni_c, yeni_x, yeni_n = topla("data/candidates/v6-parti*.jsonl")

    sat = ["# `slice` alanının anlamı v5 ile v6 arasında sessizce değişti", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Girdi:** `data/candidates/` — v4/v5 {eski_n} benzersiz kayıt · "
           f"v6 {yeni_n} benzersiz kayıt  ", "",
           "⭐ Nasıl çıktı: subagent judge koşusunda bir kayıt uydurma diye "
           "işaretlendi; dilimi `rag_tek_tur` görününce *«bağlam belgesi "
           "nerede»* diye bakıldı ve **yoktu**.", "",
           "## Alan ne söylüyor", "",
           "| dönem | `slice` değeri | kayıt | bağlamlı | oran |",
           "|---|---|---:|---:|---:|"]
    for ad, c, x in (("v4/v5", eski_c, eski_x), ("**v6**", yeni_c, yeni_x)):
        for k in sorted(c, key=str):
            sat.append(f"| {ad} | `{k}` | {c[k]} | {x[k]} | "
                       f"**%{100*x[k]/c[k]:.0f}** |")

    sat += ["", "⭐⭐ **v4/v5'te alan TAM bilgi taşıyor:** `rag_*` → %100 "
            "bağlamlı, `terapotik_*` → %0. ⛔⛔ **v6'da taşımıyor:** sözlük iki "
            "değere düştü, `terapotik_*` kayboldu, `cok_tur` yeni, ve "
            "`rag_tek_tur` kayıtların yalnız **%35'inde** bağlam var.", "",
            "➡️ Aynı ad, iki anlam: **v5'te *«tek turlu VE bağlam belgeli»*, "
            "v6'da yalnızca *«tek turlu»*.** İki dönem aynı korpusun içinde ve "
            "alan onları **ayırt etmiyor**.", "",
            "## ⛔⛔ Neden hiçbir kapı görmedi", "", "| katman | durum |", "|---|---|",
            "| `src/schemas.py` | `slice: str` — **`Literal` değil** ⇒ şema her "
            "dizgeyi kabul eder; yeni bir sözlük sessizce geçerlidir |",
            "| `src/checks.py` | **slice denetimi yok** |",
            "| birleştirme raporu | dilimi saymıyor |",
            "| judge | dilimi görmüyor (körlük şartı) |", "",
            "⭐ Bu, iki serinin kesişimi: **T236** (alan dolu, biçimi geçerli, "
            "anlamı değişmiş) ve **T237** (kural yazılı, kapı yok). "
            "⛔ Ayrıca `slice` alanının kusur geçmişi var: **K69**'da bir "
            "varsayılan iki kaydı yanlış dilimle damgalamıştı.", "",
            "## ⛔⛔⛔ Neden acil", "",
            "Veri kartı *«Dilim dağılımı»* satırını **bu alandan** türetiyor — "
            "`datasets/v0.0.8/CARD.md`: *«`terapotik_tek_tur` 256 · "
            "`terapotik_cok_tur` 188 · `rag_tek_tur` 85 · `rag_cok_tur` 24 · "
            "`replay` 18»*. O kartta sayı **doğruydu**, çünkü v5 sözlüğü "
            "geçerliydi.", "",
            f"⛔ v6 kayıtları derlemeye girdiğinde kart `rag_tek_tur`'ü "
            f"**{eski_c['rag_tek_tur'] + yeni_c['rag_tek_tur']}** diye "
            f"sayacak; bağlamı gerçekten olan tek turlu kayıt ise "
            f"**{eski_x['rag_tek_tur'] + yeni_x['rag_tek_tur']}** ⇒ "
            "yayımlanan RAG payı **iki katından fazla** şişecek.", "",
            "⭐ **Derleme v6 için henüz koşmadı** ⇒ bu, yayımlanmış bir sayı "
            "bozulmadan ÖNCE yakalandı (T121'in dersi: kapıyı derlemeden önce "
            "denetle).", "",
            "## ⭐ Öneri — *bu benim önerim*, ölçülmedi ve UYGULANMADI", "",
            "| | |", "|---|---|",
            "| 1 | `slice` **`Literal`** olmalı; sözlük tek yerde yazılı "
            "olmalı ve genişlemesi bir karar gerektirmeli |",
            "| 2 | Dilim **türetilmeli, beyan edilmemeli**: tur sayısı "
            "`messages`'tan, RAG'lik `context`'in doluluğundan ⇒ alan "
            "kendisiyle çelişemez hâle gelir |",
            "| 3 | Geriye dönük etiketleme bir **karardır** (530 kayıt) ve "
            "burada yapılmadı; hangi dönemin sözlüğüne göre yazılacağı ve "
            "eski kartların ne olacağı ayrı sorular |", "",
            "## ⛔ Bu raporun söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **Hiçbir kayıt DEĞİŞTİRİLMEDİ** | 530 kaydın etiketini "
            "yeniden yazmak rutin bir düzeltme değil |",
            "| ⛔ **Yayımlanmış kartlar YANLIŞ DEĞİL** | `v0.0.5`–`v0.0.11` v5 "
            "sözlüğüyle derlendi ve o sözlükte sayı doğru; sorun **v6'nın "
            "girmesiyle** başlayacak |",
            "| ⚠️ **`cok_tur` kayıtlarının %10'unda bağlam var** | yani yeni "
            "sözlükte bağlam ile tur sayısı **bağımsız iki eksen**; tek bir "
            "alanla ikisi birden taşınamaz |",
            "| ⚠️ **Sebep aranmadı** | sözlüğün neden değiştiği (v6 üretim "
            "betiklerinin nereden kopyalandığı) bu raporda izlenmedi |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[sat.index("## Alan ne söylüyor"):sat.index("## ⛔⛔ Neden hiçbir kapı görmedi")]))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
