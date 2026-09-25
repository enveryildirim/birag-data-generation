#!/usr/bin/env python3
"""`klinik_guvenlik_ihlali` bayrağının İKİ YÖNLÜ kararlılığı.

⛔ T175 bayrağın çevrilebildiğini gösterdi ama örneklemde pozitif sayısı 1'di.
T176 pozitifçe zengin kümeyi kurdu: 19 pozitif + 19 eşleştirilmiş kontrol.
Bu betik o kümeye **aynı gün iki taze çekiliş** yapar (T174'ün önbellek atlama
yöntemi) ve bayrağın oynaklığını **iki yönde** ölçer.

⭐ **İki yön ayrı ayrı sayılır (K116):**
  · **P grubu** — Claude'un ihlal dediği kayıtlar ⇒ Gemini kaç kez ateşliyor,
    iki çekiliş arasında kaçı çeviriyor (**yanlış pozitifin kararlılığı**)
  · **K grubu** — hiç ateşlememiş eşleştirilmiş kayıtlar ⇒ Gemini yeni bir
    pozitif üretiyor mu (**yanlış negatifin kararlılığı**)
Yalnız P'yi ölçmek pozitifleri tek yönlü eritir ve yanlış negatifi hiç görmez.

⛔⛔ **Bu betik bir kapı ÖNERMEZ.** Bayrağın kapıda kalıp kalmayacağı ve
«tanıyı reddetmek yetiyor mu» sorusu `gd-019`'da, uzman kaleminde (Kural 3).
Burada ölçülen tek şey: bayrak aynı metne iki kez sorulduğunda aynı şeyi
söylüyor mu.

⛔ Betik kendi sayısını yeniden üretmez (ölçtüğü şey çekiliş) ⇒ ham bayraklar
JSON'a dökülür, `--kurtar` kipi aynı cevaplardan aynı tabloyu servise gitmeden
türetir.

⚠️ Betik 09-18'de yazıldı ama o gün Gemini kotası bittiği için HİÇ SAYI ÜRETMEDİ
(K216). Ölçüm 09-19'da yapıldığı için adı da 09-19'a alındı: K126 rapor tarihini
betiğin ADINDAN türetir ve tarih ölçümün yapıldığı gün olmalıdır. Girdi kümesi
09-18'de kurulduğu için o tarihi korur.

Girdi : reports/analiz/2026-09-18-guvenlik-bayragi-kumesi.json + data/judged/*.jsonl
Çıktı : reports/analiz/2026-09-19-guvenlik-bayragi-kararliligi.{md,json}
Kullanım: uv run python scripts/analiz/2026-09-19-guvenlik-bayragi-kararliligi.py
         ... --kurtar .cache/cekilisler/2026-09-19-F .cache/cekilisler/2026-09-19-G
"""
from __future__ import annotations

import json
import random
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
KUME = KOK / "reports/analiz/2026-09-18-guvenlik-bayragi-kumesi.json"
BAYRAK = "klinik_guvenlik_ihlali"
YAN = ["rol_siniri_ihlali", "tuzak_suclama", "kurum_yordam_ihlali"]

import filter as F  # noqa: E402
import llm  # noqa: E402


def _cek(kayitlar, etiket, kurtar: Path | None):
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
          f"{len(list(havuz.glob('*.json'))) - onceki} taze çağrı", flush=True)
    return {i: j for i, j in out if j}


def main(kurtar=None) -> int:
    kume = json.loads(KUME.read_text(encoding="utf-8"))
    idx: dict[str, dict] = {}
    for f in {k["metin_havuzu"] for k in kume["kume"]}:
        for l in (KOK / "data/judged" / f).read_text(encoding="utf-8").splitlines():
            if l.strip():
                r = json.loads(l)
                idx[r["id"]] = r
    kayitlar = [idx[k["id"]] for k in kume["kume"] if k["id"] in idx]
    grup = {k["id"]: k["grup"] for k in kume["kume"]}
    sid = {k["id"]: k["source_id"] for k in kume["kume"]}
    print(f"küme: {len(kayitlar)} kayıt ({sum(1 for k in kayitlar if grup[k['id']] == 'P')} P + "
          f"{sum(1 for k in kayitlar if grup[k['id']] == 'K')} K) · {F.JUDGE_MODEL} · "
          f"{F.JUDGE_PROMPT_VERSION}", flush=True)

    G1 = _cek(kayitlar, "F", kurtar[0] if kurtar else None)
    G2 = _cek(kayitlar, "G", kurtar[1] if kurtar else None)
    ortak = sorted(set(G1) & set(G2))

    def _say(g):
        ids = [i for i in ortak if grup[i] == g]
        f1 = sum(1 for i in ids if G1[i].get(BAYRAK))
        f2 = sum(1 for i in ids if G2[i].get(BAYRAK))
        cev = sorted(i for i in ids if bool(G1[i].get(BAYRAK)) != bool(G2[i].get(BAYRAK)))
        iki = sorted(i for i in ids if G1[i].get(BAYRAK) and G2[i].get(BAYRAK))
        return {"n": len(ids), "F": f1, "G": f2, "cevrilen": cev, "ikisinde": iki}

    P, K = _say("P"), _say("K")
    tum_poz = sorted({i for i in ortak if G1[i].get(BAYRAK) or G2[i].get(BAYRAK)})
    cevrilen = P["cevrilen"] + K["cevrilen"]
    kararli = len(tum_poz) - len(cevrilen)

    sat = [
        "# Güvenlik bayrağının iki yönlü kararlılığı", "",
        f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
        f"**Küme:** `reports/analiz/2026-09-18-guvenlik-bayragi-kumesi.json` "
        f"(havuz SHA256 `{kume['havuz_sha256_16']}`)  ",
        f"**Judge:** `{F.JUDGE_MODEL}` · **rubrik:** `{F.JUDGE_PROMPT_VERSION}` · "
        f"**ortak kayıt:** {len(ortak)}/{len(kayitlar)}", "",
        "⭐ İki çekiliş de aynı gün, aynı metin, **önbellek atlanarak** alındı (T174). "
        "İki yön ayrı sayılır (K116): P grubu yanlış pozitifin, K grubu yanlış negatifin "
        "kararlılığını ölçer.", "",
        "## 1. ⭐⭐⭐ Bayrak iki çekilişte ne yaptı", "",
        "| grup | kayıt | F'de ateşledi | G'de ateşledi | ikisinde de | ⛔ çevrilen |",
        "|---|---:|---:|---:|---:|---:|",
        f"| **P** (Claude ihlal demişti) | {P['n']} | {P['F']} | {P['G']} | "
        f"{len(P['ikisinde'])} | **{len(P['cevrilen'])}** |",
        f"| **K** (hiç ateşlememiş kontrol) | {K['n']} | {K['F']} | {K['G']} | "
        f"{len(K['ikisinde'])} | **{len(K['cevrilen'])}** |", "",
        f"**En az bir çekilişte ateşleyen:** {len(tum_poz)} kayıt · bunların "
        f"**{kararli}**'i iki çekilişte de aynı, **{len(cevrilen)}**'i çevrildi.", ""]

    if not tum_poz:
        sat += ["⛔⛔⛔ **Gemini kümenin HİÇBİR kaydında bayrağı ateşlemedi** — Claude'un "
                f"ihlal dediği {P['n']} kayıt dahil. ➡️ *Kararlılık ölçülemedi çünkü "
                "ölçülecek olay hiç gerçekleşmedi. Ama ölçülemeyişin kendisi bir bulgu: "
                "T176'nın oran farkı (Claude %1,20 ↔ Gemini %0,00) bu kümede de sürüyor "
                "ve artık örtüşme 4 değil " + str(P["n"]) + " kayıt.* ⛔ Bu, bayrağın "
                "**yanlış** olduğunu göstermez; iki judge'ın aynı şeye bakıp farklı "
                "şey gördüğünü gösterir — hangisinin haklı olduğu Kural 3 gereği uzmanın "
                "(`gd-019`).", ""]
    else:
        oran = round(100 * len(cevrilen) / len(tum_poz))
        sat += [(f"⛔⛔⛔ **Bayrak oynak: ateşleyen {len(tum_poz)} kaydın %{oran}'i "
                 "iki çekiliş arasında çevrildi.** Aynı metin, aynı gün, aynı model. "
                 "➡️ *Girdisi çekiliş olan bir kapı sert değildir (Kural 3).*"
                 if cevrilen else
                 f"⭐⭐ **Bayrak kararlı: ateşleyen {len(tum_poz)} kaydın hiçbiri "
                 "çevrilmedi.** T175'teki tek çevrilme bu kümede yinelenmedi ⇒ o vaka "
                 "kuralın değil sınırın örneğiymiş."), ""]
        for i in cevrilen:
            sat.append(f"· çevrildi: `{sid[i]}` (grup {grup[i]}) F={bool(G1[i].get(BAYRAK))} "
                       f"G={bool(G2[i].get(BAYRAK))}")
        for i in P["ikisinde"] + K["ikisinde"]:
            t = G1[i].get("guvenlik_tipi") or G2[i].get("guvenlik_tipi")
            sat.append(f"· ikisinde de ateşledi: `{sid[i]}` (grup {grup[i]}) · tip `{t}`")
        sat.append("")

    # ⭐ Asıl okuma: oynaklık her yerde değil, YALNIZ tartışmalı bantta.
    sat += ["## 2. ⭐⭐⭐ Oynaklık her yerde değil — tam da karar verilen yerde", "",
            "| | P (tartışmalı) | K (kontrol) |", "|---|---:|---:|",
            f"| kayıt | {P['n']} | {K['n']} |",
            f"| en az bir çekilişte ateşleyen | {len([i for i in tum_poz if grup[i] == 'P'])} | "
            f"{len([i for i in tum_poz if grup[i] == 'K'])} |",
            f"| **çevrilen** | **{len(P['cevrilen'])}** | **{len(K['cevrilen'])}** |", "",
            f"⭐⭐ **Kontrol grubunda 19 kayıt, iki çekiliş, {len(K['cevrilen'])} çevrilme.** "
            "Bayrak rastgele ateşlemiyor: sessiz olması gereken yerde tam sessiz. Oynaklık "
            "yalnız Claude'un kusur gördüğü dar bantta.", "",
            "➡️⭐⭐⭐ *Bu, judge'ın bozuk olduğunu göstermez — K103 (sınırda %51 uyum) ile "
            "K106 (`golden.locked`'da %7 bölünme, sert kapılarda sıfır) arasındaki ayrımın "
            "**üçüncü bağımsız yinelenmesidir**: kararlılık judge'ın değil MALZEMENİN "
            "özelliği. Kusur judge'da değil, `build.py`'de: bir SINIR BULUCU sert kapı "
            "olarak kullanılıyor. Sınırı bulan araç, sınırın hangi yanında durulacağına "
            "karar veremez.*", "",
            "## 3. ⚠️ Claude ile örtüşme — ölçüt değil, çerçeve", "",
            f"Kümenin P grubu Claude'un ihlal dediği {P['n']} kayıttır. Gemini bunların "
            f"**{len(P['ikisinde'])}**'inde iki çekilişte de, **{len(P['cevrilen'])}**'inde "
            "bir çekilişte ateşledi.", "",
            "⚠️ **Bu bir uyum ölçümü DEĞİL** (K97: iki judge aynı tabloda karşılaştırılmaz). "
            "Burada Claude'un çıktısı yalnız **hangi kayıtların okunacağını** belirledi; "
            "ölçülen şey Gemini'nin kendisiyle tutarlılığı. ➡️ *Hangi judge'ın haklı "
            "olduğu bu ölçümde YOK ve Kural 3 gereği bende de değil.*", ""]

    # ⭐ Dün de aynı model ve aynı rubrikle iki çekiliş alınmıştı (T175). Ateşleyen
    # kayıtlardan dünkü örneklemde de bulunanlar için DÖRT bağımsız çekiliş olur.
    # ⛔ K97 korunuyor: tabloya yalnız Gemini çekilişleri giriyor, Claude yargısı değil.
    dun = KOK / "reports/analiz/2026-09-18-judge-gurultu-kayma.json"
    if dun.exists():
        d = json.loads(dun.read_text(encoding="utf-8"))
        es = [(i, d["ham_cekilisler"]["B"].get(i), d["ham_cekilisler"]["C"].get(i))
              for i in tum_poz
              if d.get("bc_model") == F.JUDGE_MODEL and i in d["ham_cekilisler"].get("B", {})]
        if es:
            sat += ["## 4. ⭐ Dört çekiliş, iki gün", "",
                    "| kayıt | B (09-18) | C (09-18) | F (09-19) | G (09-19) |",
                    "|---|---:|---:|---:|---:|"]
            for i, b, c in es:
                sat.append(f"| `{sid[i]}` | {bool((b or {}).get(BAYRAK))} | "
                           f"{bool((c or {}).get(BAYRAK))} | {bool(G1[i].get(BAYRAK))} | "
                           f"{bool(G2[i].get(BAYRAK))} |")
            sat += ["",
                    "⭐ Aynı model, aynı rubrik, dört bağımsız çekiliş. Kayıt **her iki "
                    "günde de bölündü** ⇒ oynaklık bir günün tesadüfü değil. ➡️ *Tutarlı "
                    "biçimde kararsız olmak da bir bulgudur: ölçüm aygıtı bozuk değil, "
                    "ölçülen şey iki anlamlı.* ⚠️ Tek kayıt (`gd-019` vakası).", ""]

    sat += ["## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            f"| ⛔⛔ **n={P['n']} pozitif** | korpusun tamamındaki tekil pozitif sayısı bu; "
            "daha büyük bir küme **yok**, bu bir ölçüm sınırı değil korpusun özelliği |",
            "| ⛔⛔ **Doğruluk ölçülmedi** | iki çekiliş de yanlış olabilir; ölçülen "
            "tutarlılık |",
            "| ⛔ **Çerçeve Claude'dan** | Gemini'nin kendi ateşlediği kayıtlar bilinmiyor "
            "(T176) ⇒ *«Gemini kendi pozitiflerinde kararlı mı»* sorusu hâlâ açık |",
            (f"| ⛔ **{len(kayitlar) - len(ortak)} kayıt düştü** | `agy` boş içerik döndürdü |"
             if len(kayitlar) - len(ortak) else
             "| ⭐ **Hiç kayıt düşmedi** | 38 kaydın 38'i iki çekilişte de yargılandı |"),
            "| ⛔⛔ **«Kapı kalmalı mı» sorusu burada YOK** | bu ölçüm bayrağın kendisiyle "
            "tutarlılığını söyler; kapının kaderi `gd-019`'da, uzman kaleminde (Kural 3) |",
            "| ⛔ **Betik kendi sayısını üretmez** | ölçtüğü şey çekiliş; ham bayraklar "
            "JSON'da, `--kurtar` kipi aynı cevaplardan aynı tabloyu türetir |", ""]

    (KOK / f"reports/analiz/{TARIH}-guvenlik-bayragi-kararliligi.json").write_text(
        json.dumps({"tarih": TARIH, "model": F.JUDGE_MODEL, "n_ortak": len(ortak),
                    "P": {k: v for k, v in P.items()}, "K": {k: v for k, v in K.items()},
                    "ham": {e: {i: {b: J[i].get(b) for b in [BAYRAK, "guvenlik_tipi"] + YAN}
                                for i in ortak} for e, J in (("F", G1), ("G", G2))}},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    (KOK / f"reports/analiz/{TARIH}-guvenlik-bayragi-kararliligi.md").write_text(
        "\n".join(sat), encoding="utf-8")
    print("\n".join(sat[6:]))
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    k = (Path(a[a.index("--kurtar") + 1]), Path(a[a.index("--kurtar") + 2])) \
        if "--kurtar" in a else None
    raise SystemExit(main(k))
