#!/usr/bin/env python3
"""v5-parti3..8 judge döngüsünün KONSOLİDE raporu: önce → sonra.

⛔⛔ **Bu tablo bir «iyileşme ölçümü» DEĞİLDİR ve öyle okunmamalı.** «Sonra»
sütunu korpusun yeniden yargılanmış hâli değil: **yalnız metni değişen kayıtlar**
yeniden puanlandı, kalanı eski puanını devraldı (metin birebir aynı olduğu
kanıtlanarak). ⇒ Tablodaki her fark **revize edilen kayıtlardan** gelir.

➡️ *Bir öncesi-sonrası tablosu, arada NE DEĞİŞTİĞİNİ yazmıyorsa bir müdahale
ölçümü gibi okunur; oysa burada değişen şey hem veri hem de veriyi değiştirme
kararıdır — ve ikincisi aynı hakemin bulgularından türedi.*

⚠️ K43/K45: hakem Claude ailesinden ⇒ bu sayılar **metrik değil**.
⚠️ K97/K137: tek rubrik (v9), tek koşu kurulumu ⇒ yalnız KENDİ içinde
karşılaştırılabilir; `v0.0.x` sayılarıyla aynı tabloya konamaz.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / "reports/analiz/2026-09-17-judge-konsolide.md"

CIFT = [  # (parti, ÖNCE, SONRA)
 ("v5-parti3", "data/judged/v5-parti3.v2.v9.jsonl", "data/judged/v5-parti3.v6.v9.jsonl"),
 ("v5-parti4", "data/judged/v5-parti4.arinmis.v9.jsonl", "data/judged/v5-parti4.v4.v9.jsonl"),
 ("v5-parti5", "data/judged/v5-parti5.arinmis.v9.jsonl", "data/judged/v5-parti5.v5.v9.jsonl"),
 ("v5-parti6", "data/judged/v5-parti6.arinmis.v9.jsonl", "data/judged/v5-parti6.v5.v9.jsonl"),
 ("v5-parti7", "data/judged/v5-parti7.arinmis.v9.jsonl", "data/judged/v5-parti7.v5.v9.jsonl"),
 ("v5-parti8", "data/judged/v5-parti8.arinmis.v9.jsonl", "data/judged/v5-parti8.v5.v9.jsonl"),
]
_sp = None
import importlib.util as _iu
_sp = _iu.spec_from_file_location("rl", KOK / "scripts/analiz/2026-09-17-revizyon-listesi.py")
RL = _iu.module_from_spec(_sp); _sp.loader.exec_module(RL)


def _yukle(y: str):
    p = KOK / y
    if not p.exists():
        return None
    return {r["gen_meta"]["parti_sira"]: r
            for r in (json.loads(s) for s in p.read_text(encoding="utf-8").splitlines() if s.strip())}


def _bayrak(rs) -> dict:
    """⭐ KATMANDAN BAĞIMSIZ bayrak sayısı.

    ⛔⛔ Katmanlı sayım tek başına YANILTTI: ilk tabloda K3 «36 → 50» çıktı ve
    veri kötüleşmiş gibi göründü. Oysa katman ataması `elif` ile yapılıyor —
    K1 ya da K2'si düzelen bir kayıt K3 katmanına **terfi ediyor**. Bağımsız
    sayımda K3 bayrakları **86 → 84**, yani düz.
    ➡️ *Katmanlı bir sayaç, üst katman boşaldığında alt katmanı şişirir; bu bir
    veri hareketi değil, SAYMA biçiminin kendisidir — ve iki sayı yan yana
    konmazsa fark edilemez.*
    """
    o = {"K1": 0, "K2": 0, "K3": 0}
    for r in rs.values():
        j = r.get("judge")
        if not j:
            continue
        for x in RL.kusurlar(j):
            o[x.split(":")[0]] += 1
    return o


def _say(rs) -> dict:
    o = {"K1": 0, "K2": 0, "K3": 0, "revize": 0}
    for n, r in rs.items():
        j = r.get("judge")
        if not j:
            continue
        k = RL.kusurlar(j)
        kat = {x.split(":")[0] for x in k}
        if "K1" in kat:
            o["K1"] += 1
        elif "K2" in kat:
            o["K2"] += 1
        elif "K3" in kat:
            o["K3"] += 1
        if r.get("gen_meta", {}).get("revizyon"):
            o["revize"] += 1
    return o


def main() -> int:
    eksik = [s for _, _, s in CIFT if not (KOK / s).exists()]
    if eksik:
        print("⛔ Henüz hazır olmayan 'sonra' dosyaları:")
        for e in eksik:
            print("  ", e)
        return 2
    sat = ["# Judge döngüsü — konsolide rapor (v5-parti3..8)", "",
           "**Betik:** `scripts/analiz/2026-09-17-judge-konsolide.py` · **Tarih:** 2026-09-17",
           "**Rubrik:** `judge-eksen1.v9` · k=1 · 360 kayıt", "",
           "⛔⛔ **«Sonra» sütunu korpusun yeniden yargılanmış hâli DEĞİL.** Yalnız metni",
           "değişen kayıtlar yeniden puanlandı; kalanı, puanlanan metnin BİREBİR aynı",
           "olduğu kanıtlanarak eski puanını devraldı. ⇒ Her fark revize edilen",
           "kayıtlardan gelir.", "",
           "⚠️ Hakem Claude ailesinden (K43/K45) ⇒ **metrik değil**, revizyon sinyali.", "",
           "## 1. Kusur KATMANLARI — önce → sonra", "",
           "⚠️ Katman ataması dışlayıcıdır (bir kayıt en üst katmanında sayılır).",
           "⛔ Bu yüzden K3 sütunu **yanıltır**: K1/K2'si düzelen kayıt K3'e *terfi eder*.",
           "Gerçek K3 hareketi için **Bölüm 2**'ye bakılmalı.", "",
           "| parti | K1 önce→sonra | K2 önce→sonra | K3 önce→sonra | revize kayıt |",
           "|---|---|---|---|---:|"]
    top = {"K1": [0, 0], "K2": [0, 0], "K3": [0, 0], "rev": 0}
    for parti, o, s in CIFT:
        a, b = _yukle(o), _yukle(s)
        ca, cb = _say(a), _say(b)
        for k in ("K1", "K2", "K3"):
            top[k][0] += ca[k]; top[k][1] += cb[k]
        top["rev"] += cb["revize"]
        ok = lambda k: ("✅" if cb[k] < ca[k] else ("⛔" if cb[k] > ca[k] else "·"))
        sat.append(f"| `{parti}` | {ca['K1']} → **{cb['K1']}** {ok('K1')} | "
                   f"{ca['K2']} → **{cb['K2']}** {ok('K2')} | "
                   f"{ca['K3']} → **{cb['K3']}** {ok('K3')} | {cb['revize']} |")
    sat.append(f"| **toplam** | {top['K1'][0]} → **{top['K1'][1]}** | "
               f"{top['K2'][0]} → **{top['K2'][1]}** | "
               f"{top['K3'][0]} → **{top['K3'][1]}** | **{top['rev']}** |")
    sat += ["", "## 2. ⭐ KATMANDAN BAĞIMSIZ bayrak sayısı", "",
            "| katman | önce | sonra |", "|---|---:|---:|"]
    ba = {"K1": 0, "K2": 0, "K3": 0}
    bb = {"K1": 0, "K2": 0, "K3": 0}
    for parti, o, s2 in CIFT:
        for k, v in _bayrak(_yukle(o)).items():
            ba[k] += v
        for k, v in _bayrak(_yukle(s2)).items():
            bb[k] += v
    for k in ("K1", "K2", "K3"):
        ok = "✅" if bb[k] < ba[k] else ("⛔" if bb[k] > ba[k] else "·")
        sat.append(f"| **{k}** | {ba[k]} | **{bb[k]}** {ok} |")
    sat += ["", "➡️ *K3 katmanlı sayımda 36 → 50 görünüyordu; bağımsız sayımda "
            f"{ba['K3']} → {bb['K3']}. Fark tamamen katman terfisinden geliyor ve "
            "bunu ancak iki sayıyı yan yana koymak gösteriyor.*", "",
            "⭐ **K1** = `build.py` eler (klinik güvenlik / rol sınırı) · "
            "**K2** = dayanaksız iddia · **K3** = MI tuzağı (elenmez, sete girer)", "",
            "## 3. ⛔ Bu raporun söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **Müdahale ölçümü değil** | revizyon kararı da, ölçüm de aynı hakemin "
            "bulgularından geliyor; bağımsız bir sınama yok |",
            "| ⛔ **K3 kasten düzeltilmedi** | 48 MI tuzağı sette duruyor: ilk eğitim "
            "ölçülmeden hepsini düzeltmek, hangi revizyonun işe yaradığını ölçülemez yapardı |",
            "| ⛔ **Uzman yok** | judge'ın yanlış pozitif oranı hâlâ ölçülmedi (K58 50/70'te kapandı) |",
            "| ⚠️ k=1 | hakemin kendi içi tutarlılığı ölçülmedi |",
            "| ⚠️ Devralınan puanlar | değişmeyen kayıtların puanı ilk koşudan; "
            "hakem aynı metni bugün farklı puanlayabilirdi |", ""]
    CIKTI.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[8:]))
    print(f"→ {CIKTI.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
