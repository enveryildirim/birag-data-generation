#!/usr/bin/env python3
"""«Ne kadar veri var» — ve naif toplam neden üç kat sayar (T91).

⛔ Soru göründüğünden zor: `datasets/v0.0.3`, `v0.0.4` ve `v0.0.5` **aynı 155
kaydın** üç sürümü (aynı id, aynı kullanıcı mesajları; tek fark eklenen
yönlendirme cümleleri — K114). `data/judged/` ile `data/candidates/` de büyük
ölçüde **aynı kayıtları** taşıyor, farklı aşamalarında. ⇒ Dosya satırlarını
toplamak **üç kat sayar**.

⭐ Bu yüzden iki sayı ayrı ayrı veriliyor: **dosya satırı** (depolanan) ve
**tekil kayıt** (`id` bazında). ➡️ *Bir veri kümesinin büyüklüğü, dosyalarının
büyüklüğü değildir; ikisini karıştırmak tezde veri setini olduğundan büyük
gösterir.*

⛔ **Ve asıl soru «ne kadar» değil «ne kadarı KULLANILABİLİR»:** kriz dilimi
üretilmedi (etik kurul), vahşi doğa dilimi bulunamadı, 8 kayıt karantinada.

Girdi : datasets/v*/train.jsonl · data/{seeds,seeds.v2,guvenlik-karantinasi}.jsonl ·
        data/{candidates,judged,plan}/*.jsonl · evals/*.jsonl
Çıktı : reports/analiz/2026-09-16-veri-envanteri.md
Kullanım: uv run python scripts/analiz/2026-09-16-veri-envanteri.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-veri-envanteri.md"


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def oku(yol: Path):
    for satir in yol.read_text(encoding="utf-8").split("\n"):
        if satir.strip():
            try:
                yield json.loads(satir)
            except json.JSONDecodeError:
                continue


def kelime(r: dict) -> tuple[int, int, int]:
    """(kullanıcı, asistan cevap, asistan thinking) kelime."""
    k = a = t = 0
    for m in r.get("messages", []):
        w = len((m.get("content") or "").split())
        if m.get("role") == "user":
            k += w
        elif m.get("role") == "assistant":
            a += w
            t += len((m.get("thinking") or "").split())
    return k, a, t


def main() -> int:
    L: list[str] = []
    L += ["# Veri envanteri — ne kadar var, ve ne kadarı kullanılabilir", "",
          f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}", "",
          "---", "", "## 1. Katmanlar", "",
          "| katman | dosya | **dosya satırı** | ⭐ **tekil kayıt** |",
          "|---|---:|---:|---:|"]

    def katman(ad: str, yollar: list[Path], anahtar="id"):
        satir = 0
        tekil = set()
        for y in yollar:
            for r in oku(y):
                satir += 1
                k = r.get(anahtar)
                tekil.add(k if k is not None else f"{y.name}:{satir}")
        L.append(f"| {ad} | {len(yollar)} | **{satir}** | **{len(tekil)}** |")
        return satir, tekil

    tohum = sorted(KOK.glob("data/seeds*.jsonl"))
    katman("tohum havuzu (`data/seeds*`)", tohum, "seed_id")
    plan = sorted((KOK / "data/plan").glob("*.jsonl"))
    katman("örneklem planı (`data/plan/`)", plan, "seed_id")
    aday = sorted((KOK / "data/candidates").glob("*.jsonl"))
    _, aday_id = katman("üretilen aday (`data/candidates/`)", aday)
    jud = sorted((KOK / "data/judged").glob("*.jsonl"))
    _, jud_id = katman("yargılanmış (`data/judged/`)", jud)
    ds = sorted(KOK.glob("datasets/v*/train.jsonl"))
    _, ds_id = katman("yayımlanmış dataset (`datasets/v*`)", ds)
    ev = sorted((KOK / "evals").glob("*.jsonl"))
    katman("eval seti (`evals/`)", ev)
    kar = [KOK / "data/guvenlik-karantinasi.jsonl"]
    katman("⛔ karantina", kar)

    L += ["",
          "⛔⛔ **Dosya satırı ile tekil kayıt arasındaki fark tesadüf değil, TASARIM.**",
          "`datasets/v0.0.3`, `v0.0.4` ve `v0.0.5` **aynı 155 kaydın** üç sürümü: aynı",
          "`id`, aynı kullanıcı mesajları; tek fark eklenen yönlendirme cümleleri (K114,",
          "doz-yanıt kolları). ⇒ Dosya satırlarını toplamak **aynı veriyi üç kez sayar**.", "",
          "➡️ *Bir veri kümesinin büyüklüğü, dosyalarının büyüklüğü değildir — ve ikisini*",
          "*karıştırmak tezde veri setini olduğundan büyük gösterir.*", "", "---", ""]

    # --- §2 dataset sürümleri --------------------------------------------------
    L += ["## 2. Dataset sürümleri — hangisi neyin üstüne biniyor", "",
          "| sürüm | kayıt | bir öncekiyle ortak `id` | yeni |", "|---|---:|---:|---:|"]
    onceki: set[str] = set()
    surum_id = {}
    for y in ds:
        ids = {r["id"] for r in oku(y) if r.get("id")}
        v = y.parent.name
        surum_id[v] = ids
        L.append(f"| `{v}` | {len(ids)} | {len(ids & onceki)} | **{len(ids - onceki)}** |")
        onceki = ids
    hepsi = set().union(*surum_id.values()) if surum_id else set()
    L += ["", f"⭐ **Beş sürümün tekil kayıt birleşimi: {len(hepsi)}.** "
          f"Dosya satırı toplamı {sum(len(v) for v in surum_id.values())} — "
          f"**{sum(len(v) for v in surum_id.values()) - len(hepsi)} satır tekrar**.", "",
          "---", ""]

    # --- §3 metin hacmi --------------------------------------------------------
    son = sorted(surum_id, reverse=True)[0] if surum_id else None
    kayitlar = list(oku(KOK / f"datasets/{son}/train.jsonl")) if son else []
    kk = aa = tt = 0
    tur = 0
    for r in kayitlar:
        a, b, c = kelime(r)
        kk += a
        aa += b
        tt += c
        tur += len(r.get("messages", []))
    replay = sum(1 for r in kayitlar if r.get("replay"))
    L += [f"## 3. Metin hacmi — en güncel sürüm (`{son}`)", "", "| | |", "|---|---:|",
          f"| kayıt | **{len(kayitlar)}** |",
          f"| bunlardan replay (§9 unutma savunması) | {replay} |",
          f"| terapötik kayıt | **{len(kayitlar) - replay}** |",
          f"| mesaj (tur) | **{tur}** |",
          f"| kullanıcı kelimesi | **{kk:,}** |".replace(",", "."),
          f"| asistan cevap kelimesi | **{aa:,}** |".replace(",", "."),
          f"| asistan thinking kelimesi | **{tt:,}** |".replace(",", "."),
          f"| **toplam** | **{kk+aa+tt:,}** |".replace(",", "."), "",
          f"⭐ Kayıt başına ortalama **{(kk+aa+tt)//max(1,len(kayitlar))}** kelime · "
          f"thinking payı **%{100*tt/max(1,kk+aa+tt):.0f}**.", "",
          "⚠️ Birim **kelime** (K46/T81 ile aynı, Kural 5) — token değil.", "", "---", ""]

    # --- §4 kullanılabilirlik --------------------------------------------------
    sen = collections.Counter(r.get("scenario") for r in kayitlar if not r.get("replay"))
    L += ["## 4. ⛔ Asıl soru: ne kadarı KULLANILABİLİR", "",
          "| eksik | durum |", "|---|---|",
          "| **kriz dilimi** (~%10 hedef) | ⛔ üretilmedi — etik kurul + uzman onayı "
          "bekliyor (Kural 3) |",
          "| **vahşi doğa dilimi** | ⛔ üretilemedi — aday kaynakların tamamı elendi "
          "(`oasst2`'de yalnızca 10 Türkçe prompter mesajı) |",
          "| karantina | ⛔ **8 kayıt** eğitim setine giremiyor; gerekçesi (K76) "
          "**yazılmamış** |",
          "| uzman puanlaması | ◐ 50/70'te kapandı (K58) |", "",
          f"⭐ **En güncel sürümün senaryo dağılımı** ({len(kayitlar)-replay} terapötik kayıt):",
          "", "| senaryo | kayıt |", "|---|---:|"]
    for k, v in sen.most_common():
        L.append(f"| `{k}` | {v} |")
    L += ["",
          "⛔⛔ **Ölçek bağlamı: tohum havuzu 2.240, yayımlanmış tekil kayıt "
          f"{len(hepsi)}.** Yani havuzun **%{100*len(hepsi)/2240:.1f}**'i üretime girdi. "
          "➡️ *Darboğaz tohum değil; üretim, yargılama ve **onay**.*", "",
          "## ⛔ Bu envanterin söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ **Kalite** | sayılan şey hacim; `datasets/v0.0.1`'in kalite hedefi "
          "**yoktu** (Faz 2 dikey dilim) ve o da bu toplamın içinde |",
          "| ⛔ **Token değil kelime** | tokenizer'a bağlı bir sayı istenirse yeniden "
          "ölçülmeli (K46/T81 ile karşılaştırılabilirlik için kelime seçildi) |",
          "| ⚠️ `data/judged` ↔ `data/candidates` örtüşmesi | ikisi de aynı kayıtların "
          "farklı aşamaları; tekil sayılar bunu düzeltir ama **aşama** bilgisi bu tabloda yok |",
          "| ⛔ Eval setleri **eğitim verisi değil** | mühürlü (K31) ve toplama dahil "
          "edilmemeli |",
          "| ⚠️ Arşiv (`reports/analiz/ham-judge`, `*/sonuclar.jsonl`) | **ölçüm çıktısı**, "
          "veri seti değil — kapsam dışı |", ""]

    RAPOR.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print(f"   yayımlanmış tekil kayıt {len(hepsi)} · en güncel {son} {len(kayitlar)} "
          f"({replay} replay) · toplam {kk+aa+tt} kelime")
    return 0


if __name__ == "__main__":
    sys.exit(main())
