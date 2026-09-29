#!/usr/bin/env python3
"""`v0.1.1` derlemesi — HAZIRLIK dosyası (Faz 3 · K277).

`datasets/v0.1.0/train.jsonl`'den başlar ve YALNIZ kabul edilmiş yeniden kurmaları
yerine koyar. `src/build.py` kullanılmaz: o, judged → dataset yolunda süzgeç
uygular ve yeniden kurulmuş düşünmeyle FARKLI bir kayıt kümesi düşürebilir; K277
ise *«kayıt kümesi: yeni kayıt yok, silme yok»* diyor.

Kural:
  kabul edilmiş yeniden kurma (Faz 2 raporundaki hüküm)  → aday kayıt
  reddedilmiş kayıt                                        → v0.1.0 hâli (silinmez)
  replay (18 genel alan kaydı, düşünmesi yok)              → v0.1.0 hâli
  uretim-v6 §1e örneği (ORNEK_ID)                          → v0.1.0 hâli ⛔ §1e metni
      bağımsız denetimden geçmedi; eğitime kendi başıma sokmuyorum (👤 açık madde)

⛔ `datasets/` altına YAZMAZ (IMMUTABLE). Çıktı hazırlık dosyasıdır; ön kayıt onun
SHA'sını mühürler, Faz 4 dondururken aynı SHA'yı üretmek zorundadır.

Kullanım: BIRAG_SCRATCH=<scratchpad> uv run python scripts/analiz/2026-09-29-v011-derleme.py
"""
from __future__ import annotations

import collections
import glob
import hashlib
import json
import re
import statistics as st
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from kunye import betik_tarihi  # noqa: E402

TARIH = Path(__file__).name[:10]
KAYNAK = KOK / "datasets/v0.1.0/train.jsonl"
CIKTI = KOK / "data/candidates/v011-derleme.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-v011-derleme.md"
ORNEK_ID = "833a3c51bbbd1adc139c7201"      # uretim-v6 §1e


def _modul(ad: str, yol: str):
    argv = sys.argv[:]; sys.argv = [str(KOK / yol)]
    sp = _iu.spec_from_file_location(ad, KOK / yol); m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m); sys.argv = argv
    return m


def _sha16(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def _redler() -> set[str]:
    """Redler Faz 2 raporundan DEĞİL, raporu üreten hükümden alınır: rapor betiği
    yeniden koşulur ve «Redler» tablosu okunur — tek kaynak, elle liste yok."""
    F = _modul("_faz2", "scripts/analiz/2026-09-24-v011-faz2.py")
    F.rapor()
    metin = F.RAPOR.read_text(encoding="utf-8")
    blok = metin.split("## Redler", 1)[1].split("\n## ", 1)[0]
    nolar = re.findall(r"^\| (\d{4}|P\d{2}) \|", blok, flags=re.M)
    plan = {r["no"]: r["id"] for r in F._plan_tum()}
    return {plan[n] for n in nolar}


def _son(r: dict) -> dict:
    return r["messages"][-1]


def _soru_mu(metin: str) -> bool:
    return metin.rstrip().rstrip("\"'»)").endswith("?")


def main() -> int:
    kaynak = [json.loads(x) for x in KAYNAK.read_text(encoding="utf-8").splitlines() if x.strip()]
    aday = {}
    for f in sorted(glob.glob(str(KOK / "data/candidates/v011-faz2-b[0-9][0-9].jsonl"))) \
            + [str(KOK / "data/candidates/v011-pilot.jsonl")]:
        for x in Path(f).read_text(encoding="utf-8").splitlines():
            if x.strip():
                r = json.loads(x); assert r["id"] not in aday, f"⛔ çift aday {r['id']}"
                aday[r["id"]] = r
    red = _redler()
    assert red <= set(aday), "⛔ reddedilen kayıt adaylarda yok"

    cikti, neden = [], collections.Counter()
    for e in kaynak:
        if e.get("replay"):
            cikti.append(e); neden["replay (değişmedi)"] += 1
        elif e["id"] == ORNEK_ID:
            cikti.append(e); neden["§1e örneği (v0.1.0 hâli)"] += 1
        elif e["id"] in red:
            cikti.append(e); neden["red (v0.1.0 hâli)"] += 1
        elif e["id"] in aday:
            y = aday[e["id"]]
            # zarf: yalnız son asistan turu ve gen_meta değişebilir
            assert set(y) == set(e), e["id"]
            assert all(y[k] == e[k] for k in e if k not in ("messages", "gen_meta")), e["id"]
            assert y["messages"][:-1] == e["messages"][:-1], e["id"]
            assert _son(y)["role"] == _son(e)["role"] == "assistant", e["id"]
            cikti.append(y); neden["yeniden kuruldu"] += 1
        else:
            raise SystemExit(f"⛔ kuralı olmayan kayıt: {e['id']}")

    # K277: kayıt kümesi ve sırası değişmez
    assert [r["id"] for r in cikti] == [r["id"] for r in kaynak], "⛔ kayıt kümesi/sırası değişti"
    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in cikti), encoding="utf-8")

    # ── veri düzeyi ölçüler: Faz 4'ün neyi gösterebileceğini önceden sınırlar ─────
    def olc(kayitlar):
        d = [r for r in kayitlar if not r.get("replay")]
        cev = [_son(r)["content"] for r in d]
        th = [(_son(r).get("thinking") or "") for r in d]
        soz = [len(t.split()) for t in th if t]
        return {
            "kayıt (replay hariç)": len(d),
            "son tur soruyla biten": f"{sum(map(_soru_mu, cev))}/{len(d)} (%{100*sum(map(_soru_mu, cev))/len(d):.1f})",
            "düşünme ortanca sözcük": st.median(soz),
            "düşünmede «sormuyorum»": f"%{100*sum('sormuyorum' in t.lower().replace('İ','i') for t in th)/len(d):.1f}",
            "düşünmede ⛔ ya da ⭐": f"%{100*sum(('⛔' in t) or ('⭐' in t) for t in th)/len(d):.1f}",
        }
    o_eski, o_yeni = olc(kaynak), olc(cikti)
    degisen_son = sum(_son(a)["content"] != _son(b)["content"] for a, b in zip(kaynak, cikti))
    degisen_dus = sum((_son(a).get("thinking") or "") != (_son(b).get("thinking") or "") for a, b in zip(kaynak, cikti))

    s = [f"# `v0.1.1` derlemesi — hazırlık dosyası", "",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {betik_tarihi(__file__)}  ",
         f"**Kaynak:** `{KAYNAK.relative_to(KOK)}` SHA256-16 `{_sha16(KAYNAK)}`  ",
         f"**Çıktı (hazırlık, dondurulmadı):** `{CIKTI.relative_to(KOK)}` SHA256-16 **`{_sha16(CIKTI)}`** · {len(cikti)} kayıt  ",
         "⛔ `datasets/v0.1.1` henüz YOK. Ön kayıt bu SHA'yı mühürler; Faz 4 dondururken aynısını üretmek zorundadır.", "",
         "## Kayıt kuralı", "", "| kural | kayıt |", "|---|---:|"]
    s += [f"| {k} | {v} |" for k, v in neden.items()]
    s += [f"| **toplam** | **{len(cikti)}** |", "",
          "⭐ Kayıt kümesi ve sırası `v0.1.0` ile **birebir** (assert). Değişen alan yalnız son asistan turu ve `gen_meta` (assert).", "",
          "## Veri düzeyinde ne değişti", "",
          f"Değişen düşünme: **{degisen_dus}** kayıt · değişen **cevap** (son cümle): **{degisen_son}** kayıt.", "",
          "| | `v0.1.0` | `v0.1.1` hazırlık |", "|---|---:|---:|"]
    s += [f"| {k} | {o_eski[k]} | {o_yeni[k]} |" for k in o_eski]
    s += ["", "## ⛔ Bunun söylemedikleri", "", "| | |", "|---|---|",
          f"| ⛔⛔ **Bitiş müdahalesi çok küçük** | cevabı değişen kayıt yalnız **{degisen_son}**; K277'nin *≤ ~170* beklentisinin çok altında (T300). Veri düzeyinde soruyla bitme payı neredeyse yerinde ⇒ Faz 4'te modelin soruyla bitme payında bir değişim **bu kanaldan beklenmez**; görülürse düşünme yapısından gelmiş olmalı |",
          "| ⚠️ **Soru = son karakter** | T281 ile aynı vekil; ortada soru, sonda yansıtma sayılmaz |",
          "| ⚠️ **«sormuyorum» vekil** | sözcük sayar, kalıbı değil (T281) |",
          "| 👤 **§1e örneği** | `v0.1.0` hâliyle kaldı; §1e'deki yeniden kurulmuş metin denetimden geçmediği için eğitime alınmadı |"]
    RAPOR.write_text("\n".join(s) + "\n", encoding="utf-8")
    print("\n".join(s[:4])); print(f"yazıldı: {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
