#!/usr/bin/env python3
"""Kayma ölçümü — aynı model, aynı metin, BAŞKA GÜN.

⭐ T175 gürültüyü ölçtü ama kaymayı ölçemedi: elde Gemini'nin yalnız **bir günü**
vardı. Ayırt edici olan tek şey ikinci bir gündür. Bu betik onu ölçer.

**Tasarım — dört karşılaştırma, üçü kontrol:**
  1. **dün içi**  (B ↔ C, 09-18) — dünkü gürültü tabanı, JSON'dan okunur
  2. **bugün içi** (D ↔ E, 09-19) — bugünkü gürültü tabanı, TAZE çekilir
  3. **günler arası** (dün ↔ bugün) — kayma varsa BURASI 1 ve 2'den büyük çıkar
  4. **düzey** — boyut ortalamaları dün ↔ bugün; gürültü ortalamada sönümlendiği
     için kayma en temiz burada görünür (T175 §5)

➡️ *Gürültü her iki günde de aynı büyüklükteyse ve günler arası fark ondan
büyük değilse, kayma yoktur. Fark büyükse, aradaki tek değişken gündür.*

⛔ **Karşılaştırma yalnız aynı judge_model içinde yapılır** (K97). Dünün A sütunu
(`claude-sonnet-subagent`) bu betiğe HİÇ girmez — T173'ün hatası oydu.

⛔ Bu betik de kendi sayısını yeniden üretmez (ölçtüğü şey çekiliş) ⇒ ham puanlar
JSON'a dökülür, `--kurtar` kipi aynı cevaplardan aynı tabloyu servise gitmeden
türetir. Çekilişler `.cache/cekilisler/<tarih>-<harf>/` altında saklanır.

Girdi : data/judged/v0.0.14.jsonl · reports/analiz/2026-09-18-judge-gurultu-kayma.json
Çıktı : reports/analiz/2026-09-19-judge-kayma.{md,json}
Kullanım: uv run python scripts/analiz/2026-09-19-judge-kayma.py [N]
         ... [N] --kurtar .cache/cekilisler/2026-09-19-D .cache/cekilisler/2026-09-19-E
"""
from __future__ import annotations

import hashlib
import json
import random
import statistics as st
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
KAYIT = KOK / "data/judged/v0.0.14.jsonl"
DUN = KOK / "reports/analiz/2026-09-18-judge-gurultu-kayma.json"
BOYUT = ["duygusal_tepki", "yorumlama", "kesif", "mi_uyumu", "grounding"]
ELEYEN = "klinik_guvenlik_ihlali"

import filter as F  # noqa: E402
import llm  # noqa: E402


def _cek(kayitlar, etiket, kurtar: Path | None):
    """Taze çekiliş — `llm.CACHE_DIR` ayrı bir dizine çevrilir.

    `kurtar` verilirse o dizin önbellek olur ve ıska servise GİTMEZ ⇒ eski bir
    çekiliş birebir yeniden türetilir, kısmen yeni bir çekiliş olmaz.
    """
    havuz = kurtar or (KOK / ".cache/cekilisler" / f"{TARIH}-{etiket}")
    havuz.mkdir(parents=True, exist_ok=True)
    onceki = len(list(havuz.glob("*.json")))
    ger_dir, ger_call = llm.CACHE_DIR, llm.call
    llm.CACHE_DIR = havuz
    if kurtar is not None:
        def _sadece_onbellek(model, messages, api_base=None):
            if not (havuz / f"{llm._cache_key(model, messages)}.json").exists():
                raise RuntimeError("kurtarma kipi: bu çekilişte cevap yok")
            return ger_call(model, messages, api_base)
        llm.call = _sadece_onbellek
    try:
        # ⭐ 2026-09-19: düşen çağrılar kuyruğun SONUNDA toplanıyor ve kuyruk sırası
        # determinist olduğu için her ikinci çekilişte AYNI kayıtlar eleniyordu ⇒
        # hayatta kalan örneklem rastgele bir alt küme değil sabit bir ÖN EK'ti
        # (`2026-09-19-dusen-cagrilar-konumu.md`). Sıra artık çekiliş başına ayrı
        # karıştırılıyor: kayıp rastgeleleşir. ⚠️ Karıştırma yalnız GÖNDERİM sırasını
        # değiştirir; önbellek anahtarı sıraya bağlı olmadığı için `--kurtar` etkilenmez.
        kuyruk = list(kayitlar)
        random.Random(f"sira-{etiket}").shuffle(kuyruk)

        def f(r):
            try:
                return r["id"], dict(F.judge_record(r))
            except Exception as e:
                print(f"    ⚠️ {r['id'][:8]}: {type(e).__name__}", flush=True)
                return r["id"], None
        with ThreadPoolExecutor(max_workers=6) as h:
            out = list(h.map(f, kuyruk))
    finally:
        llm.CACHE_DIR, llm.call = ger_dir, ger_call
    print(f"  çekiliş {etiket}: {sum(1 for _, j in out if j)}/{len(out)} başarılı · "
          f"{len(list(havuz.glob('*.json'))) - onceki} taze çağrı · {havuz}", flush=True)
    return {i: j for i, j in out if j}


def _oran(x, y, ortak):
    """Kayıt düzeyinde kaç kayıt oynadı + alan düzeyinde yön."""
    d = u = ayni = 0
    for i in ortak:
        f = [(x[i].get(k), y[i].get(k)) for k in BOYUT
             if x[i].get(k) is not None and y[i].get(k) is not None and x[i][k] != y[i][k]]
        ayni += not f
        for a, b in f:
            d += b < a
            u += b > a
    n = len(ortak)
    return {"kayit": n, "degisen": n - ayni, "yuzde": round(100 * (n - ayni) / max(1, n)),
            "dustu": d, "yukseldi": u}


def main(n: int, kurtar=None) -> int:
    ham = KAYIT.read_bytes()
    kayitlar = [json.loads(s) for s in ham.decode("utf-8").splitlines() if s.strip()]
    aday = [r for r in kayitlar
            if not (r.get("judge") or {}).get("yeniden_yargilandi")
            and (r.get("judge") or {}).get("prompt_version") == "judge-eksen1.v9"
            and (r.get("judge") or {}).get("yorumlama") is not None]
    random.Random(11).shuffle(aday)          # ⭐ T175 ile AYNI tohum ⇒ aynı örneklem
    ornek = aday[:n]

    dun = json.loads(DUN.read_text(encoding="utf-8"))
    if dun["bc_model"] != F.JUDGE_MODEL:
        print(f"⛔ DUR: dünkü model {dun['bc_model']}, bugünkü {F.JUDGE_MODEL} — "
              "K97 gereği farklı judge'lar aynı tabloda karşılaştırılmaz.")
        return 1
    B = {i: v for i, v in dun["ham_cekilisler"]["B"].items()}
    C = {i: v for i, v in dun["ham_cekilisler"]["C"].items()}
    print(f"örnek: {len(ornek)} kayıt · model {F.JUDGE_MODEL} · rubrik "
          f"{F.JUDGE_PROMPT_VERSION} · dün: {len(B)} kayıt", flush=True)

    D = _cek(ornek, "D", kurtar[0] if kurtar else None)
    E = _cek(ornek, "E", kurtar[1] if kurtar else None)
    ortak = sorted(set(B) & set(C) & set(D) & set(E))
    if not ortak:
        print("⛔ ortak kayıt yok")
        return 1

    dun_ici = _oran(B, C, ortak)
    bugun_ici = _oran(D, E, ortak)
    gunler = _oran(B, D, ortak)
    ort = {k: {e: st.mean([J[i][k] for i in ortak if J[i].get(k) is not None])
               for e, J in (("B", B), ("C", C), ("D", D), ("E", E))} for k in BOYUT}
    # ⭐ Kayma ölçütü: günler arası fark, İKİ GÜNÜN gürültü tabanının üstünde mi?
    taban = max(dun_ici["yuzde"], bugun_ici["yuzde"])
    kayma_var = gunler["yuzde"] > taban + 15
    duzey = {k: (ort[k]["D"] + ort[k]["E"]) / 2 - (ort[k]["B"] + ort[k]["C"]) / 2
             for k in BOYUT}
    kayan = [k for k, v in duzey.items() if abs(v) >= 0.25]

    sat = [
        "# Kayma ölçümü — aynı model, başka gün", "",
        f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
        f"**Girdi:** `data/judged/v0.0.14.jsonl` SHA256 `{hashlib.sha256(ham).hexdigest()[:16]}` · "
        f"taban `reports/analiz/2026-09-18-judge-gurultu-kayma.json`  ",
        f"**Model:** `{F.JUDGE_MODEL}` (dün de aynı — K97) · **rubrik:** "
        f"`{F.JUDGE_PROMPT_VERSION}` · **ortak kayıt:** {len(ortak)}", "",
        "⭐ Kayma, gürültüden ancak **kendi tabanına karşı** ayrılır: günler arası fark, "
        "iki günün kendi içindeki oynaklığından belirgin büyük olmalıdır.", "",
        "## 1. Üç oran — ikisi kontrol", "",
        "| karşılaştırma | ne ölçer | oynayan kayıt | ↓ / ↑ |", "|---|---|---:|---:|",
        f"| **B ↔ C** (09-18 içi) | dünkü gürültü tabanı | {dun_ici['degisen']}/{dun_ici['kayit']} "
        f"(**%{dun_ici['yuzde']}**) | {dun_ici['dustu']} / {dun_ici['yukseldi']} |",
        f"| **D ↔ E** ({TARIH} içi) | bugünkü gürültü tabanı | {bugun_ici['degisen']}/"
        f"{bugun_ici['kayit']} (**%{bugun_ici['yuzde']}**) | {bugun_ici['dustu']} / "
        f"{bugun_ici['yukseldi']} |",
        f"| **B ↔ D** (günler arası) | gürültü **+ varsa kayma** | {gunler['degisen']}/"
        f"{gunler['kayit']} (**%{gunler['yuzde']}**) | {gunler['dustu']} / {gunler['yukseldi']} |",
        "",
        (f"⛔⛔ **KAYMA İŞARETİ VAR:** günler arası %{gunler['yuzde']}, gürültü tabanı "
         f"%{taban} ⇒ aradaki tek değişken gündür."
         if kayma_var else
         f"⭐⭐ **KAYMA İŞARETİ YOK:** günler arası %{gunler['yuzde']}, gürültü tabanı "
         f"%{taban} ⇒ günler arası fark gürültüyle açıklanıyor; ayrıca bir kaymaya "
         "gerek kalmıyor."), "",
        "### ⚠️ Yön sınaması — iki taze çekiliş simetrik mi", ""]
    import math
    for ad, o in (("dün B ↔ C", dun_ici), ("bugün D ↔ E", bugun_ici)):
        n_ol = o["dustu"] + o["yukseldi"]
        az = min(o["dustu"], o["yukseldi"])
        # adil yazı-tura altında «az olan taraf ≤ az» olasılığı (tek yönlü)
        pk = sum(math.comb(n_ol, k) for k in range(az + 1)) / 2 ** n_ol if n_ol else 1.0
        sat.append(f"· **{ad}**: {o['dustu']}↓ / {o['yukseldi']}↑ · adil çekilişte bu kadar "
                   f"tek yanlı olma olasılığı ≈ **%{100 * pk:.1f}**"
                   + ("  ⚠️ **beklenenden tek yanlı**" if pk < 0.05 else ""))
    sat += ["",
            "⚠️ Aynı günün iki taze çekilişi **değiştirilebilir** olmalıydı: yön "
            "beklenmez. Belirgin tek yanlılık çıkarsa iki açıklama var ve bu ölçüm "
            "onları ayırmıyor: (a) küçük sayı tesadüfü, (b) iki çekilişin **aynı "
            "koşullarda alınmadığı** — ikinci çekiliş günün kota/hız baskısı altında "
            "koşuyor ve düşen çağrıları da o üretiyor "
            "(`2026-09-19-dusen-cagrilar-konumu.md`). ⛔ İki günün yönleri ters "
            "çıktıysa (b) zayıflar, tesadüf güçlenir.", "",
            "## 2. ⭐ Düzey — gürültünün sönümlendiği yer", "",
        "| boyut | B (dün) | C (dün) | D (bugün) | E (bugün) | dün → bugün |",
        "|---|---:|---:|---:|---:|---:|"]
    for k in BOYUT:
        o = ort[k]
        sat.append(f"| `{k}` | {o['B']:.2f} | {o['C']:.2f} | {o['D']:.2f} | {o['E']:.2f} | "
                   f"**{duzey[k]:+.2f}** |")
    sat += ["",
            (f"⛔⛔ **Düzey kaydı: {kayan}** — ortalama gürültüyü sönümlediği için bu, "
             "kaymanın en temiz göstergesidir."
             if kayan else
             "⭐ **Hiçbir boyutta 0,25'lik düzey kayması yok** — iki günün ortalamaları "
             "üst üste biniyor."), "",
            "## 3. ⛔ Eleyen kapı bayrağı", "", "| | dün B | dün C | bugün D | bugün E |",
            "|---|---:|---:|---:|---:|",
            f"| `{ELEYEN}` ateşleyen kayıt | " + " | ".join(
                str(sum(1 for i in ortak if J[i].get(ELEYEN))) for J in (B, C, D, E)) + " |", ""]
    hep = [i for i in ortak if any(J[i].get(ELEYEN) for J in (B, C, D, E))]
    for i in hep:
        r = next((x for x in ornek if x["id"] == i), {})
        sat.append(f"· `{(r.get('source_ids') or ['?'])[0]}` → B={bool(B[i].get(ELEYEN))} "
                   f"C={bool(C[i].get(ELEYEN))} D={bool(D[i].get(ELEYEN))} "
                   f"E={bool(E[i].get(ELEYEN))}")
    sat += ["",
            "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            f"| ⛔ **n={len(ortak)} küçük** | oranlar geniş güven aralığı taşır |",
            "| ⛔ **İki gün bir eğilim değildir** | kayma ancak birkaç gün üst üste "
            "ölçülürse eğilim olur; burada yalnız *«dün ile bugün ayrı mı»* soruluyor |",
            "| ⛔ **Eşik seçilmiştir** | «taban + 15 puan» benim koyduğum ayraç, "
            "türetilmiş değil (bu benim önerim) |",
            "| ⛔⛔ **Bayrağın kararlılığı hâlâ pozitifçe zengin kümede ölçülmedi** | "
            "`gd-019` bekletmesini bitirecek olan ölçüm budur, bu değil |",
            "| ⚠️ **Doğruluk değil tutarlılık** | dört çekiliş de yanlış olabilir |", ""]

    (KOK / f"reports/analiz/{TARIH}-judge-kayma.json").write_text(
        json.dumps({"tarih": TARIH, "n": len(ortak), "model": F.JUDGE_MODEL,
                    "dun_ici": dun_ici, "bugun_ici": bugun_ici, "gunler_arasi": gunler,
                    "kayma_var": kayma_var, "ortalama": ort, "duzey_farki": duzey,
                    "ham_cekilisler": {e: {i: {k: J[i].get(k) for k in BOYUT + [ELEYEN]}
                                           for i in ortak}
                                       for e, J in (("D", D), ("E", E))}},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    (KOK / f"reports/analiz/{TARIH}-judge-kayma.md").write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[6:]))
    return 0


if __name__ == "__main__":
    arg = sys.argv[1:]
    k = None
    if "--kurtar" in arg:
        i = arg.index("--kurtar")
        k = (Path(arg[i + 1]), Path(arg[i + 2]))
        arg = arg[:i]
    raise SystemExit(main(int(arg[0]) if arg else 24, k))
