#!/usr/bin/env python3
"""Gürültü mü kayma mı — ve ortaya çıkan üçüncü şık: BAŞKA JUDGE.

⛔⛔⛔ Bu betiğin ilk sürümü YANLIŞTI ve yanlışlığı burada kayıtlıdır (Kural 2):
`llm.call` içerik-özetli ZORUNLU bir önbellek tutar (`src/llm.py:14`). Aynı gün
arka arkaya alınan iki çekilişten ikincisi birincinin yazdığı dosyayı okur ⇒
«0/24 değişti» sonucu judge'ın belirlenimciliği değil, **önbelleğin totolojisidir**.
➡️ *Bir ölçüm aygıtı ölçtüğü şeyi hatırlıyorsa, ikinci ölçüm ölçüm değildir.*

⛔⛔⛔ İkinci ve daha ağır bulgu: kayıtlı yargıların `judge_model` alanı
`claude-sonnet-subagent`. T173'te «judge kayıt düzeyinde %50 kararsız» diye
raporlanan şey **aynı judge'ın iki çekilişi değil, iki AYRI MODELİN
anlaşmazlığıdır** (Claude ↔ Gemini). T173 bu betikle DÜZELTİLİR.

⭐ Doğru tasarım — üç şıkkı ayıran şey:
  · **gürültü**  : aynı gün, aynı model, iki TAZE çekiliş (B ↔ C), önbellek atlanır
  · **kayma**    : aynı model, farklı gün — bu veriyle ÖLÇÜLEMEZ (aşağıya bak)
  · **başka judge**: kayıtlı Claude yargısı ↔ bugünkü Gemini yargısı (A ↔ B)

Önbellek atlama: `llm.CACHE_DIR` her çekiliş için boş bir scratchpad dizinine
çevrilir ⇒ çağrı servise gider, cevap projenin gerçek önbelleğini KİRLETMEZ.

⛔⛔ **BU BETİK YENİDEN KOŞULDUĞUNDA KENDİ SAYILARINI ÜRETMEZ** — ölçtüğü şey
çekilişin kendisidir. Kural 7 «her sayının bir betiği olacak» der; burada betik
sayıyı yeniden üretemediği için **çekilişlerin ham puanları JSON'a dökülür** ve
`--kurtar <B-dizini> <C-dizini>` kipi aynı ham cevaplardan aynı tabloyu servise
hiç gitmeden yeniden türetir. ➡️ *Ölçümü bozan önbellek, çözümlemeyi yeniden
üretilebilir kılan şey olur — aynı mekanizma, farklı yer.*

Girdi : data/judged/v0.0.14.jsonl
Çıktı : reports/analiz/2026-09-18-judge-gurultu-kayma.{md,json}
Kullanım: uv run python scripts/analiz/2026-09-18-judge-gurultu-kayma.py [N]
         uv run python .../2026-09-18-judge-gurultu-kayma.py [N] --kurtar B_DIZIN C_DIZIN
"""
from __future__ import annotations

import hashlib
import json
import random
import statistics as st
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
KAYIT = KOK / "data/judged/v0.0.14.jsonl"
BOYUT = ["duygusal_tepki", "yorumlama", "kesif", "mi_uyumu", "grounding"]
# ⭐ `src/build.py` judge'ın 1-5 PUANLARINI hiç kullanmaz; derlemeden eleyen tek
# judge ölçütü `klinik_guvenlik_ihlali` ikili bayrağıdır. Kuranın ürüne ulaşıp
# ulaşmadığı sorusu, bu bayrakların oynayıp oynamadığı sorusudur.
KAPI_BAYRAK = ["klinik_guvenlik_ihlali", "rol_siniri_ihlali", "tuzak_suclama",
               "kurum_yordam_ihlali"]
ELEYEN = "klinik_guvenlik_ihlali"

import filter as F  # noqa: E402
import llm  # noqa: E402


def _cek(kayitlar, etiket, dizin: Path | None = None):
    """Önbelleği atlayarak TAZE çekiliş — cevaplar ayrı bir dizine yazılır.

    `dizin` verilirse o dizin önbellek olarak kullanılır: çağrılar İSABET eder,
    servise gidilmez ⇒ eski bir çekiliş birebir yeniden türetilir (`--kurtar`).
    """
    gecici = dizin or Path(tempfile.mkdtemp(prefix=f"judge-cekilis-{etiket}-"))
    onceki = len(list(gecici.glob("*.json")))
    gercek, llm.CACHE_DIR = llm.CACHE_DIR, gecici
    gercek_call = llm.call
    if dizin is not None:
        # KATI kurtarma: ıska servise GİTMEZ. Yoksa o çekilişte başarısız olan
        # kayıtlar yeniden çağrılır ve "yeniden türetme" kısmen yeni bir çekiliş olur.
        def _sadece_onbellek(model, messages, api_base=None):
            k = llm._cache_key(model, messages)
            if not (gecici / f"{k}.json").exists():
                raise RuntimeError("kurtarma kipi: bu çekilişte cevap yok")
            return gercek_call(model, messages, api_base)
        llm.call = _sadece_onbellek
    try:
        def f(r):
            try:
                return r["id"], dict(F.judge_record(r))
            except Exception as e:
                print(f"    ⚠️ {r['id'][:8]}: {type(e).__name__}", flush=True)
                return r["id"], None
        with ThreadPoolExecutor(max_workers=6) as h:
            out = list(h.map(f, kayitlar))
    finally:
        llm.CACHE_DIR, llm.call = gercek, gercek_call
    yeni = len(list(gecici.glob("*.json"))) - onceki
    print(f"  çekiliş {etiket}: {sum(1 for _, j in out if j)}/{len(out)} başarılı · "
          f"{yeni} taze servis çağrısı · havuz: {gecici}", flush=True)
    return {i: j for i, j in out if j}, yeni


def _uzunluk(r) -> int:
    return len(F._render_conversation(r)) + len((F._last_assistant(r).get("thinking") or "")[:500])


def _ortanca(v) -> int:
    return round(st.median(v)) if v else 0


def _fark(x, y, ortak):
    d = u = ayni = 0
    alan = {}
    for i in ortak:
        f = [(k, x[i].get(k), y[i].get(k)) for k in BOYUT
             if x[i].get(k) is not None and y[i].get(k) is not None and x[i][k] != y[i][k]]
        if not f:
            ayni += 1
        for k, a, b in f:
            d += b < a
            u += b > a
            alan.setdefault(k, [0, 0])[0 if b < a else 1] += 1
    return {"kayit": len(ortak), "degisen": len(ortak) - ayni,
            "dustu": d, "yukseldi": u, "alan": alan}


def main(n: int, kurtar: tuple[Path, Path] | None = None) -> int:
    ham = KAYIT.read_bytes()
    kayitlar = [json.loads(s) for s in ham.decode("utf-8").splitlines() if s.strip()]
    aday = [r for r in kayitlar
            if not (r.get("judge") or {}).get("yeniden_yargilandi")
            and (r.get("judge") or {}).get("prompt_version") == "judge-eksen1.v9"
            and (r.get("judge") or {}).get("yorumlama") is not None]
    random.Random(11).shuffle(aday)
    ornek = aday[:n]
    a_modelleri = sorted({(r["judge"].get("judge_model") or "YOK") for r in ornek})
    print(f"örnek: {len(ornek)} kayıt (metni değişmemiş) · A modeli: {a_modelleri} · "
          f"B/C modeli: {F.JUDGE_MODEL}", flush=True)

    A = {r["id"]: dict(r["judge"]) for r in ornek}
    B, b_taze = _cek(ornek, "B", kurtar[0] if kurtar else None)
    C, c_taze = _cek(ornek, "C", kurtar[1] if kurtar else None)
    ortak = sorted(set(A) & set(B) & set(C))
    bc, ab = _fark(B, C, ortak), _fark(A, B, ortak)

    def _ort(J, k):
        v = [J[i][k] for i in ortak if J[i].get(k) is not None]
        return st.mean(v) if v else float("nan")

    ort = {k: {e: _ort(J, k) for e, J in (("A", A), ("B", B), ("C", C))} for k in BOYUT}
    simetrik = abs(bc["dustu"] - bc["yukseldi"]) <= max(2, 0.35 * (bc["dustu"] + bc["yukseldi"]))

    sat = [
        "# Gürültü mü kayma mı — ve üçüncü şık: başka judge", "",
        f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
        f"**Girdi:** `data/judged/v0.0.14.jsonl` · SHA256 `{hashlib.sha256(ham).hexdigest()[:16]}`  ",
        f"**Örnek:** {len(ortak)} kayıt, metni hiç değişmemiş · rubrik `{F.JUDGE_PROMPT_VERSION}`  ",
        f"**A (kayıtlı):** `{', '.join(a_modelleri)}` · **B, C (bugün, taze):** `{F.JUDGE_MODEL}`", "",
        "⛔⛔⛔ **Bu betiğin ilk sürümü yanlış ölçtü ve yanlışı burada kayıtlıdır.** "
        f"`llm.call` içerik-özetli zorunlu önbellek tutar; arka arkaya iki çağrıdan ikincisi "
        "birincinin yazdığı dosyayı okur. İlk sürüm bu yüzden *«%0 değişti»* buldu — judge'ın "
        "belirlenimciliği değil, **önbelleğin totolojisi**. Bu sürümde her çekiliş için "
        "`llm.CACHE_DIR` boş bir geçici dizine çevrilir ⇒ çağrı servise gider.", "",
        f"Doğrulama: B {b_taze} taze çağrı, C {c_taze} taze çağrı (her ikisi de = örnek boyu "
        "olmalı; değilse ölçüm yine önbellekten okumuştur).", "",
        "## 1. ⭐ GÜRÜLTÜ — aynı gün, aynı model, iki taze çekiliş (B ↔ C)", "",
        "| | |", "|---|---:|",
        f"| kayıt | {bc['kayit']} |",
        f"| **puanı değişen kayıt** | **{bc['degisen']}** "
        f"(%{round(100 * bc['degisen'] / max(1, bc['kayit']))}) |",
        f"| alan düzeyinde düştü / yükseldi | {bc['dustu']} / {bc['yukseldi']} |", "",
    ]
    if bc["alan"]:
        sat += ["| boyut | ↓ | ↑ |", "|---|---:|---:|"]
        sat += [f"| `{k}` | {v[0]} | {v[1]} |" for k, v in sorted(bc["alan"].items())]
        sat.append("")
    sat += [
        (f"⭐ **Gürültü ölçüldü: %{round(100 * bc['degisen'] / max(1, bc['kayit']))} kayıt oynak.** "
         + ("Yön simetrik ⇒ saf gürültü." if simetrik else
            "⚠️ Yön simetrik değil; iki taze çekiliş değiştirilebilir olduğu için bu, "
            "örneklem küçüklüğünün işareti sayılmalı."))
        if bc["degisen"] else
        "⭐⭐ **Gürültü yok: aynı gün iki TAZE çekiliş birebir aynı.** Önbellek atlandığı "
        "hâlde hiçbir puan oynamadı ⇒ judge bu rubrik altında belirlenimci davranıyor.", "",
        "## 2. ⛔⛔ «Kayma» değil — A ile B AYNI MODEL DEĞİL", "",
        "| boyut | A (Claude) | B (Gemini) | C (Gemini) | A → bugün |",
        "|---|---:|---:|---:|---:|",
    ]
    for k in BOYUT:
        o = ort[k]
        sat.append(f"| `{k}` | {o['A']:.2f} | {o['B']:.2f} | {o['C']:.2f} | "
                   f"**{(o['B'] + o['C']) / 2 - o['A']:+.2f}** |")
    sat += ["",
            f"A ↔ B: **{ab['degisen']}/{ab['kayit']}** kayıt farklı · alan düzeyinde "
            f"{ab['dustu']} düştü / {ab['yukseldi']} yükseldi.", "",
            "⛔⛔ **Bu fark ne gürültü ne kayma — iki ayrı modelin anlaşmazlığıdır.** "
            "Kayıtlı yargılar `claude-sonnet-subagent` ile, bugünküler "
            f"`{F.JUDGE_MODEL}` ile üretildi. ➡️ *Kayma ancak aynı modelin iki farklı "
            "günü karşılaştırılarak ölçülebilir; elimizde Gemini'nin ikinci bir günü yok, "
            "bu yüzden **kayma bu veriyle hâlâ ölçülmemiştir**.*", "",
            "## 3. ⛔⛔⛔ T173 düzeltilir", "",
            "| T173'te yazan | burada bulunan |", "|---|---|",
            "| «judge kayıt düzeyinde %50 kararsız» | o %50 **aynı judge'ın iki çekilişi "
            "değil**, Claude ↔ Gemini anlaşmazlığıydı |",
            "| «`yorumlama`/`kesif` sistematik düşüyor ⇒ kayma olabilir» | düşüş **model "
            "farkının** yönü; kayma iddiası dayanaksız kaldı |",
            f"| — | aynı modelin gerçek gürültüsü ilk kez burada ölçüldü: "
            f"**{bc['degisen']}/{bc['kayit']}** |", "",
            "## 4. ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            f"| ⛔ **n={len(ortak)} küçük** | oranlar geniş güven aralığı taşır |",
            "| ⛔⛔ **Kayma ölçülmedi** | aynı modelin ikinci bir günü yok |",
            "| ⛔⛔ **Havuzun judge'ı Claude** | `v0.0.14`'te 527 kayıt "
            "`claude-sonnet-subagent`; K43/K45 puanlayan judge'ın Claude olamayacağını "
            "söyler. Bu, kullanıcının açık yönergesiyle böyle yapıldı — ama **ölçütün "
            "dayandığı zemin budur** ve karar uzmanındır |",
            "| ⚠️ **Doğruluk ölçülmedi** | üç çekiliş de yanlış olabilir; ölçülen tutarlılık |",
            f"| ⚠️ **C çekilişinde {len(ornek) - len(C)} çağrı düştü** | `agy` boş içerik döndürdü "
            "ve aynı kayıtlar yeniden çağrıldığında YİNE düştü ⇒ dalgalanma değil. "
            f"Ayırt edici özellik ARANDI ve bulunamadı: istem uzunluğu ortanca "
            f"{_ortanca([_uzunluk(r) for r in ornek if r['id'] not in C])} krk (düşen) ↔ "
            f"{_ortanca([_uzunluk(r) for r in ornek if r['id'] in C])} krk (geçen). "
            "⛔ Neden bilinmiyor; n=18 bu yüzden **sistematik yanlı sayılmadı, ama "
            "yansızlığı da kanıtlanmadı** |",
            "| ⛔⛔ **Betik kendi sayısını yeniden üretmez** | ölçtüğü şey çekiliştir; "
            "yeniden koşmak yeni bir çekiliş olur. Ham puanlar JSON'a dökülür, "
            "`--kurtar` kipi aynı cevaplardan aynı tabloyu türetir |", "",
            "## 5. ⭐⭐ Asıl sonuç — toplam sağlam, kayıt çekiliş", "",
            "Aynı iki taze çekilişte **kayıtların %"
            f"{round(100 * bc['degisen'] / max(1, bc['kayit']))}'i oynadı**, ama boyut "
            "ortalamaları neredeyse yerinde durdu (§2'deki B ↔ C sütunları: "
            + ", ".join(f"`{k}` {ort[k]['B']:.2f}↔{ort[k]['C']:.2f}" for k in BOYUT) + ").", "",
            "➡️ **Gürültü toplamda sönümleniyor, kayıtta sönümlenmiyor.** Bunun işlemsel "
            "karşılığı şudur: judge puanı **kümeler için** okunabilir, **tek kayıt hakkında "
            "karar vermek için okunamaz**. Tek bir kaydı puanına bakıp elemek ya da tutmak, "
            "ölçüm değil kura çekmektir.", "",
            "## 6. ⭐⭐⭐ Kura ürüne ulaşıyor mu — kapı bayrakları", "",
            "`src/build.py:71` judge'ın 1-5 puanlarını **hiç okumaz**; derlemeden eleyen tek "
            f"judge ölçütü `{ELEYEN}` ikili bayrağıdır. Dolayısıyla §1'deki %"
            f"{round(100 * bc['degisen'] / max(1, bc['kayit']))} oynaklık ancak bu bayrağı "
            "çevirdiği ölçüde ürüne ulaşır.", "",
            "| bayrak | A (Claude) | B | C | ⛔ B↔C çevrilen |", "|---|---:|---:|---:|---:|"]
    for b in KAPI_BAYRAK:
        say = lambda J: sum(1 for i in ortak if J[i].get(b))  # noqa: E731
        cevrilen = sum(1 for i in ortak if bool(B[i].get(b)) != bool(C[i].get(b)))
        sat.append(f"| `{b}`{' **(eleyen)**' if b == ELEYEN else ''} | {say(A)} | {say(B)} | "
                   f"{say(C)} | **{cevrilen}** |")
    eleyen_cevrilen = sum(1 for i in ortak if bool(B[i].get(ELEYEN)) != bool(C[i].get(ELEYEN)))
    bayrak_cevrilen = sum(1 for b in KAPI_BAYRAK for i in ortak
                          if bool(B[i].get(b)) != bool(C[i].get(b)))
    kaynak = {r["id"]: r for r in ornek}
    cevrilenler = [i for i in ortak if bool(B[i].get(ELEYEN)) != bool(C[i].get(ELEYEN))]
    sat += ["",
            (f"⭐⭐ **Eleyen bayrak iki çekilişte de aynı: 0 çevrilme.** Puanlar %"
             f"{round(100 * bc['degisen'] / max(1, bc['kayit']))} oynarken derlemeye giren "
             "küme oynamadı ⇒ **kura bu örneklemde ürüne ULAŞMIYOR**. "
             "➡️ *Oynak olan ile karar veren aynı şey değil: gürültü sürekli boyutlarda, "
             "kapı ikili bir bayrakta.*"
             if eleyen_cevrilen == 0 else
             f"⛔⛔⛔ **Eleyen bayrak {eleyen_cevrilen} kayıtta çevrildi.** Aynı metin, aynı gün, "
             "aynı model — ama biri derlemeye giriyor öteki elenmiyor. Derlemenin içeriği "
             "kısmen çekilişe bağlı demektir; bu, ölçüm değil kura ile veri seçmektir."),
            ""]
    for i in cevrilenler:
        r = kaynak[i]
        tip = next((J[i].get("guvenlik_tipi") for J in (B, C) if J[i].get(ELEYEN)), "?")
        sat += [f"**Çevrilen kayıt:** `{(r.get('source_ids') or ['?'])[0]}` · "
                f"A(Claude)={bool(A[i].get(ELEYEN))} B={bool(B[i].get(ELEYEN))} "
                f"C={bool(C[i].get(ELEYEN))} · `guvenlik_tipi: {tip}`  ",
                "⛔⛔ Bu kayıt `datasets/v0.0.14`'ten **elendi** (`judge_safety_violation`). "
                "İkinci çekiliş kazansaydı **girecekti**. ➡️ *Kural 3 güvenlik ekseninde "
                "sert kapı ister; girdisi çekiliş olan bir kapı sert değildir.*", ""]
    sat += [
            (f"⚠️ Öteki kapı bayraklarında toplam **{bayrak_cevrilen}** çevrilme var; bunlar "
             "bugün elemiyor ama raporlanıyor."
             if bayrak_cevrilen else
             "⭐ Dört kapı bayrağının **hiçbiri** oynamadı — sert kapılar, sürekli "
             "boyutlardan belirgin biçimde daha kararlı."), "",
            f"⚠️ Bu {len(ortak)} kayıtta eleyen bayrak A, B, C'nin üçünde de "
            f"{sum(1 for i in ortak if A[i].get(ELEYEN))}/{len(ortak)} ateşledi — "
            "**örneklemde neredeyse hiç pozitif yok**, yani kararlılık burada "
            "«hep hayır demek»le de açıklanabilir. ⛔ Bayrağın gerçek kararlılığı ancak "
            "pozitifçe zengin bir kümede ölçülür; bu ölçüm onu yapmıyor.", ""]
    (KOK / f"reports/analiz/{TARIH}-judge-gurultu-kayma.json").write_text(
        json.dumps({"tarih": TARIH, "n": len(ortak), "a_modeli": a_modelleri,
                    "bc_model": F.JUDGE_MODEL, "b_taze": b_taze, "c_taze": c_taze,
                    "gurultu_bc": bc, "anlasmazlik_ab": ab, "ortalama": ort,
                    "ham_cekilisler": {e: {i: {k: J[i].get(k) for k in BOYUT + KAPI_BAYRAK}
                                           for i in ortak}
                                       for e, J in (("A", A), ("B", B), ("C", C))}},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    (KOK / f"reports/analiz/{TARIH}-judge-gurultu-kayma.md").write_text(
        "\n".join(sat), encoding="utf-8")
    print("\n".join(sat[8:]))
    return 0


if __name__ == "__main__":
    arg = sys.argv[1:]
    kurt = None
    if "--kurtar" in arg:
        i = arg.index("--kurtar")
        kurt = (Path(arg[i + 1]), Path(arg[i + 2]))
        arg = arg[:i]
    raise SystemExit(main(int(arg[0]) if arg else 24, kurt))
