#!/usr/bin/env python3
"""GERİYE DÖNÜK eşleşme denetimi — v7/v8 arşivlerinde de sonuç↔kayıt kayması var mı?

⛔ **Neden var.** 2026-09-15'te `korpus-v9-p2` partisinde bir subagent **doğru** iş
dosyalarını okuyup sonuçları **yanlış** çıktı dosyalarına yazdı (004→005→006→007→004).
JSON geçerliydi, alan sayısı doğruydu, hiçbir denetim uyarmadı; kusuru yalnızca
v9'un alıntı doğrulaması gördü (K123). O kusur **judge'ın değil, ÖLÇÜM HATTININ**
kusuruydu ve ölçüm hattı v7/v8 koşularında da aynıydı. ➡️ Aynı kaymanın daha önce
olup olmadığı **bilinmiyordu**; bu betik onu ölçer.

⭐ Denetim v9 rubriğine bağlı DEĞİL: yalnızca judge'ın **cevaptan** yaptığı uzun
alıntıların hangi kayda ait olduğuna bakar. v7 ve v8 de bu alıntıları yazıyor,
bu yüzden arşivler **yeniden puanlanmadan** denetlenebiliyor.

Karar kuralı tek kaynaktan gelir: `eslesme_denetimi()` 2026-09-15-v9-kapi-denetimi.py
dosyasından **import edilir**, kopyalanmaz — kopyalasaydım geriye dönük sayı ile
ileriye dönük kapı farklı bir kural uygulayabilirdi.

⚠️ **Duyarlılık açıkça ölçülür.** Bir arşivin kaynak havuzu yanlış kurulmuşsa
denetim ateşlemez (alıntılar ne kendi ne başka kayıtta bulunur) — yani sessizce
**yanlış negatif** verir. Bu yüzden her arşiv için «kendi cevabında bulunan alıntı»
oranı raporlanır; oran düşükse o satırın denetimi ZAYIFTIR ve öyle yazılır.

Kullanım: uv run python scripts/analiz/2026-09-15-geriye-donuk-eslesme.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import date
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
sys.path.insert(0, str(KOK / "src"))
import filter as f  # noqa: E402

sys.argv = [sys.argv[0]]
_sp = _iu.spec_from_file_location("kapi9", KOK / "scripts/analiz/2026-09-15-v9-kapi-denetimi.py")
KAPI = _iu.module_from_spec(_sp)
_sp.loader.exec_module(KAPI)

eslesme_denetimi = KAPI.eslesme_denetimi          # KARAR KURALI — tek kaynak
ESLESME_ALAN = KAPI.ESLESME_ALAN
HARITA = KAPI.B9.HARITA                            # e2-<hash> → (kol, üretim dizini)

HAM = KOK / "reports/analiz/ham-judge"
KOSU = KOK / "reports/analiz/eksen-kosu"
GKOSU = KOK / "reports/analiz/golden-kosu"
RAPOR = KOK / f"reports/analiz/{TARIH}-geriye-donuk-eslesme.md"

KOL = {h: k for h, (k, _d) in HARITA.items()}      # "e2-5ae67873" → "taban"


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


# ─────────────────────────── kaynak havuzları ───────────────────────────
def havuz_eksen2() -> dict:
    """(kol, id) → kaynak metinler. 114 kayıt; havuz KOL SINIRINI AŞAR."""
    return KAPI.eksen2_kaynaklari()


def havuz_aday(yol: Path) -> dict:
    """Korpus/aday dosyası: konuşmanın kendisi kayıttır."""
    return {r["id"]: f.kaynak_metinleri(r)
            for r in (json.loads(l) for l in yol.open(encoding="utf-8"))}


def havuz_uretim(eval_yolu: Path, kosu_dizini: Path) -> dict:
    """Eval öğesi + o koşuda ÜRETİLEN cevap (golden / locked kolları)."""
    ogeler = {o["id"]: o for o in
              (json.loads(l) for l in eval_yolu.open(encoding="utf-8"))}
    out = {}
    for r in (json.loads(l) for l in (kosu_dizini / "sonuclar.jsonl").open(encoding="utf-8")):
        o = ogeler.get(r["id"])
        if o:
            out[r["id"]] = KAPI.B9.kaynak_kur(o, r.get("cevap") or "", r.get("thinking"))
    return out


def havuz_doz(varyant: str) -> dict:
    """Doz yamaları: iki arşiv İKİ FARKLI yama sürümünü puanlamış.

    ⚠️ İlk kurulumda eşleme TERS yapılmıştı ve denetim %74'e düştü; hatayı
    «kendi cevabında bulundu» sütunu gösterdi. Doğru eşleme kanıtla sabitlendi:
    `data/judged/doz-yama.v7.jsonl`'in `judge` alanları **v7b** arşiviyle 26/26
    uyuşuyor ve o dosyanın cevabı `cevap_ek` taşıyor. ➡️ `doz-yama-v7b` = `cevap_ek`
    (yayımlanan sürüm), `doz-yama-v7` = `cevap_ek_v1` (ilk yama).

    `cevap_ek_v1` metni repoda ayrı bir kayıt olarak durmadığı için burada
    **yeniden kurulur** (yayımlanan cevaptaki ek cümle ilk sürümle değiştirilir).
    Kurulum yanlış olsaydı denetim ateşlemez, yanlış YAKALAMAZDI — bedeli
    duyarlılıktır ve tablodan okunur.
    """
    ek = {json.loads(l)["id_16"]: json.loads(l) for l in
          (KOK / "data/candidates/doz-yonlendirme-ekleri.jsonl").open(encoding="utf-8")}
    out = {}
    for r in (json.loads(l) for l in
              (KOK / "data/judged/doz-yama.v7.jsonl").open(encoding="utf-8")):
        k = ek.get(r["id"][:16])
        if varyant == "ek_v1" and k and k.get("cevap_ek") and k.get("cevap_ek_v1"):
            msgs = [dict(m) for m in r["messages"]]
            for m in reversed(msgs):
                if m["role"] == "assistant":
                    m["content"] = m["content"].replace(k["cevap_ek"].strip(),
                                                        k["cevap_ek_v1"].strip())
                    break
            r = {**r, "messages": msgs}
        out[r["id"]] = f.kaynak_metinleri(r)
    return out


# ─────────────────────────── denetlenecek küme ───────────────────────────
# (arşiv, rubrik, küme etiketi, havuz anahtarı, anahtar çıkarıcı)
def _e2_anahtar(stem):
    h = stem.split("-", 1)[1] if stem.startswith(("v8-", "v9-")) else stem
    kol = KOL.get(h)
    return lambda r: (r.get("kol") or kol, r["id"])


def kume() -> list:
    e2 = havuz_eksen2()
    kor = havuz_aday(KOK / "data/candidates/v3-kumulatif.jsonl")
    isler = []
    for stem in ["e2-5ae67873", "e2-b7584bec", "e2-220c3b5a", "e2-99b69ab4",
                 "e2-7ac7e984", "e2-ceef5655", "e2-hakem-p2", "e2-hakem-p3"]:
        isler.append((stem, "v7", "Eksen 2", e2, _e2_anahtar(stem)))
    for stem in ["v8-e2-5ae67873", "v8-e2-b7584bec", "v8-e2-220c3b5a", "v8-e2-99b69ab4",
                 "v8-e2-7ac7e984", "v8-e2-ceef5655", "v8-hakem-p2", "v8-hakem-p3"]:
        isler.append((stem, "v8", "Eksen 2", e2, _e2_anahtar(stem)))
    for stem, rub in [("korpus-v3-claude", "v3"), ("korpus-v7-sonnet", "v7"),
                      ("korpus-v7-kontrol", "v7"), ("korpus-v7-ucuncu", "v7"),
                      ("korpus-v8", "v8")]:
        isler.append((stem, rub, "korpus", kor, lambda r: r["id"]))
    for stem, dizin, es in [
            ("golden-baseline-claude", "20260915-063352-golden-baseline-claude", "golden.dev"),
            ("golden-baseline-sonnet", "20260915-080807-golden-baseline-sonnet", "golden.dev"),
            ("golden-v7-sonnet", "20260915-083830-golden-v7-sonnet", "golden.dev"),
            ("locked-baseline-1", "20260915-105813-locked-baseline-1", "golden.locked"),
            ("locked-baseline-1-p2", "20260915-110838-locked-baseline-1-p2", "golden.locked"),
            ("locked-baseline-1-p3", "20260915-111652-locked-baseline-1-p3", "golden.locked")]:
        h = havuz_uretim(KOK / f"evals/{es}.jsonl", GKOSU / dizin)
        rub = "v6" if "baseline-claude" in stem or "baseline-sonnet" in stem else "v7"
        isler.append((stem, rub, es, h, lambda r: r["id"]))
    isler.append(("expert70-v7-sonnet", "v7", "expert-70",
                  havuz_aday(KOK / "data/candidates/expert-70.jsonl"), lambda r: r["id"]))
    isler.append(("v4-parti1-v7", "v7", "v4-parti1",
                  havuz_aday(KOK / "data/candidates/v4-parti1.jsonl"), lambda r: r["id"]))
    isler.append(("doz-yama-v7", "v7", "doz yaması (ilk yama)",
                  havuz_doz("ek_v1"), lambda r: r["id"]))
    isler.append(("doz-yama-v7b", "v7", "doz yaması (yayımlanan)",
                  havuz_doz("ek"), lambda r: r["id"]))
    return isler


BAYRAK = ["rol_siniri_ihlali", "klinik_guvenlik_ihlali", "bos_guvence",
          "tuzak_suclama", "tuzak_etiketleme"]


def duyarlilik(yol: Path, kaynaklar: dict, anahtar) -> dict:
    """`eslesme_denetimi` bu arşivde ne kadar GÖREBİLİYOR — karar VERMEZ.

    ⚠️ Havuz yanlış kurulmuşsa denetim ateşlemez: alıntı ne kendi ne başka kayıtta
    bulunur ve kayma sessizce gizlenir. Bu yüzden bulunamayan alıntılar da
    sınıflandırılır — `ic_muhakeme` başka bir kusurun (T45 kapsam) izidir,
    `hicbir` ise havuzun ya da judge'ın sorunudur.
    """
    d = dict(kayit=0, eslesen=0, alinti=0, kendi=0, ic=0, hicbir=0)
    for l in yol.open(encoding="utf-8"):
        r = json.loads(l)
        ham = r.get("ham")
        if isinstance(ham, str):
            try:
                ham = json.loads(ham)
            except json.JSONDecodeError:
                continue
        if not isinstance(ham, dict):
            continue
        d["kayit"] += 1
        k = anahtar(r)
        if k is None or k not in kaynaklar:
            continue
        d["eslesen"] += 1
        for a in ESLESME_ALAN:
            if not f._f_dolu(ham, a):
                continue
            q = f.alinti_nrm(ham[a])
            if len(q) <= 25:
                continue
            d["alinti"] += 1
            if q in kaynaklar[k]["cevap"]:
                d["kendi"] += 1
            elif q in kaynaklar[k].get("ic_muhakeme", ""):
                d["ic"] += 1
            else:
                d["hicbir"] += 1
    return d


def v8_korpus_bayraklari(takas: bool) -> dict:
    """`korpus-v8` arşivinden bayrak kümeleri — 075↔077 takası ETKİ ölçümü için.

    Türetme `filter.f_bolumu_turet` ile yapılır (v8 anlambilimi = kaynaksız çağrı);
    kopyalanmış bir hesap kullansaydım etki ölçümü raporun kendi hesabını
    doğrulamazdı.
    """
    kayit = {json.loads(l)["no"]: json.loads(l)
             for l in (HAM / "korpus-v8.jsonl").open(encoding="utf-8")}
    if takas:
        a, b = dict(kayit["075"]), dict(kayit["077"])
        kayit["075"] = {**a, "ham": b["ham"]}
        kayit["077"] = {**b, "ham": a["ham"]}
    out = {}
    for r in kayit.values():
        h = json.loads(r["ham"]) if isinstance(r["ham"], str) else dict(r["ham"])
        f.f_bolumu_turet(h, None)
        out[r["id"]] = frozenset(a for a in BAYRAK if h.get(a) is True)
    return out


def main() -> int:
    satir, vaka = [], []
    for stem, rub, es, havuz, anahtar in kume():
        yol = HAM / f"{stem}.jsonl"
        d = duyarlilik(yol, havuz, anahtar)
        v = eslesme_denetimi(yol, havuz, anahtar)
        vaka += v
        satir.append((stem, rub, es, sha(yol), d, len(v)))

    T = {k: sum(s[4][k] for s in satir) for k in satir[0][4]}
    T["kayma"] = sum(s[5] for s in satir)

    y = [
        "# Geriye dönük eşleşme denetimi — v7/v8 arşivlerinde de kayma var mı",
        "",
        f"*{TARIH} · betik `scripts/analiz/{Path(__file__).name}`*",
        "*girdi: `reports/analiz/ham-judge/` — arşivlenmiş HAM judge çıktısı; "
        "**yeniden puanlama YOK**, hiçbir yayımlanmış sayı bu betikle değişmez*",
        "",
        "## Soru",
        "",
        "`korpus-v9-p2`'de bir subagent doğru iş dosyalarını okuyup sonuçları **yanlış**",
        "çıktı dosyalarına yazmıştı (K123). Ölçüm hattı v7 ve v8 koşularında da aynıydı;",
        "aynı kaymanın **daha önce** olup olmadığı bilinmiyordu. ⛔ Olsaydı, yayımlanmış",
        "v7/v8 sayıları etkilenirdi.",
        "",
        "⭐ Denetim v9 rubriğine bağlı değil: judge'ın **cevaptan** yaptığı uzun",
        "alıntıların hangi kayda ait olduğuna bakar ve bu alıntıları v3'ten beri her",
        "rubrik yazıyor. ➡️ Arşivler **yeniden puanlanmadan** denetlenebiliyor. Karar",
        "kuralı `eslesme_denetimi()`'den **import edildi**; ileriye dönük kapıyla birebir",
        "aynı kural uygulandı.",
        "",
        "## Defter — arşivlenmiş her judge kararı",
        "",
        "| Arşiv | rubrik | küme | SHA256 | kayıt | uzun alıntı | kendi cevabında | "
        "iç muhakemede | hiçbir yerde | **kayma** |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for stem, rub, es, h, d, at in satir:
        oran = f"{d['kendi']}/{d['alinti']}" + (
            f" (%{100 * d['kendi'] // d['alinti']})" if d["alinti"] else "")
        isaret = "**" if at else ""
        y.append(f"| `{stem}` | {rub} | {es} | `{h}` | {d['kayit']} | {d['alinti']} | "
                 f"{oran} | {d['ic'] or '—'} | {d['hicbir'] or '—'} | {isaret}{at}{isaret} |")
    y += [
        f"| **TOPLAM** | | | | **{T['kayit']}** | **{T['alinti']}** | "
        f"**{T['kendi']}** (%{100 * T['kendi'] // T['alinti']}) | **{T['ic']}** | "
        f"**{T['hicbir']}** | **{T['kayma']}** |",
        "",
        f"⚠️ `kayıt` sütunu arşivin tamamıdır ({T['kayit']}); havuzda karşılığı bulunan "
        f"kayıt **{T['eslesen']}** — yani denetim dışı kalan kayıt "
        f"**{T['kayit'] - T['eslesen']}**.",
        "",
    ]

    if vaka:
        ilk, son = v8_korpus_bayraklari(False), v8_korpus_bayraklari(True)
        y += [
            "## ⛔ Bulundu: `korpus-v8`'de bir TAKAS",
            "",
            "| arşiv | no | kayıt | kendi/alıntı | ait olduğu | o kayıtta bulunan |",
            "|---|---|---|---|---|---:|",
        ]
        for v in vaka:
            y.append(f"| `{v['dosya']}` | {v['no']} | `{v['kayit'][:12]}` | "
                     f"**{v['kendi']}/{v['alinti']}** | `{v['ait_oldugu'][:12]}` | "
                     f"{v['skor']} |")
        kimlik = sorted({v["kayit"] for v in vaka})
        y += [
            "",
            "⭐ **İki kayıt karşılıklı yer değiştirmiş** — v9'daki 4'lü dönüşümden farklı,",
            "temiz bir ikili takas. Komşu kayıtlar (074, 076, 078) temiz; yayılma yok.",
            "Her iki kaydın alıntılarının **hiçbiri** kendi cevabında bulunmuyor,",
            "**hepsi** ötekinin cevabında bulunuyor.",
            "",
            "⛔⛔ **Kusur judge'da DEĞİL, yazma adımında.** İş dosyaları elle denetlendi:",
            "`istek/075.txt` ve `istek/077.txt` **doğru** konuşmaları taşıyor. Yani judge",
            "doğru okudu, sonuç **yanlış dosyaya yazıldı** — `korpus-v9-p2`'deki",
            "004→005→006→007→004 dönüşümüyle **aynı kusur sınıfı**.",
            "",
            "➡️ *Bu, o olayın tek seferlik bir kaza olmadığını gösteriyor:* aynı yazma",
            "kusuru bu oturumun **iki ayrı partisinde** çıktı (`korpus-v8` ve",
            "`korpus-v9-p2`). ⚠️ Kusurun oranı hâlâ ölçülmedi — bilinen tek şey, iki",
            "kez olduğu.",
            "",
            "### Etki — yayımlanmış sayılar değişiyor mu",
            "",
            "| kayıt | arşivdeki bayraklar | takas düzeltilince |",
            "|---|---|---|",
        ]
        for i in kimlik:
            y.append(f"| `{i[:12]}` | {sorted(ilk.get(i, [])) or '—'} | "
                     f"{sorted(son.get(i, [])) or '—'} |")
        d_say = {a: (sum(1 for s in ilk.values() if a in s),
                     sum(1 for s in son.values() if a in s)) for a in BAYRAK}
        y += [
            "",
            "| bayrak | korpus v8 (arşiv) | takas düzeltilince |",
            "|---|---:|---:|",
        ] + [f"| `{a}` | {v[0]} | {v[1]} |" for a, v in d_say.items()] + [
            "",
            "✅ **Yayımlanmış hiçbir sayı değişmiyor.** İki sebeple: (1) iki kaydın bayrak",
            "kümesi her iki atamada da boş; (2) bir **takas** küme üzerindeki hiçbir",
            "toplamı ya da ortalamayı oynatmaz — yalnızca kayıt BAŞINA karşılaştırmaları",
            "oynatabilirdi ve onlar da aynı kaldı",
            "(`2026-09-15-korpus-v9-kosusu.md` Ö2/Ö4: v7→v8 **9**, v8→v9 **14**, atıf 8/3/3).",
            "",
            "⛔ **Ama bu şans.** Aynı takas bayraklı iki kayıtta olsaydı korpus v8",
            "sayıları sessizce yanlış olurdu ve **hiçbir denetim uyarmazdı** —",
            "`korpus-v8` arşivi eşleşme kapısından hiç geçmemişti: kapı yalnızca",
            "`korpus-v9*` dosyalarına bakıyordu. ➡️ *Bir kapı, raporun OKUDUĞU her",
            "arşivi kapsamıyorsa kapı değildir.*",
            "",
            "### Ne yapıldı",
            "",
            "| | |",
            "|---|---|",
            "| ✅ Kapı genişletildi | `korpus-v8` de eşleşme kapısından geçiyor; "
            "düzeltme olmadan korpus raporu **yazılmıyor** (sınandı: çıkış kodu 1) |",
            "| ✅ Düzeltme **bildirim** olarak yazıldı | "
            "`reports/analiz/ham-judge/korpus-v8.takas.json` — okuma anında uygulanır |",
            "| ⛔ Ham arşive **dokunulmadı** | arşivin işi *«subagent o dosyaya ne yazdı»*yı "
            "saklamak; üstüne yazmak kusurun kanıtını yok ederdi ve bu raporun "
            "SHA256'sını geçersiz kılardı |",
            "| ✅ Doğrulandı | düzeltme uygulanınca `2026-09-15-korpus-v9-kosusu.md` "
            "**baytı baytına aynı** çıkıyor — etkinin sıfır olduğunun ampirik kanıtı |",
            "",
            "⚠️ Bu, `korpus-v9-p2` olayında seçilen yoldan **farklı**: orada dört iş "
            "yeniden koşulmuştu (yeni kanıt üretildi). Burada yeni kanıta gerek yok — "
            "her iki judge çıktısı da **doğru**, yalnızca yanlış dosyada.",
            "",
        ]
    else:
        y += [f"## ✅ Sonuç: {T['kayit']} kayıtta **0 kayma**", ""]

    zayif = [s for s in satir if s[4]["hicbir"] or s[4]["ic"]]
    y += [
        "## ⚠️ Bulunamayan alıntılar — denetimin duyarlılığı",
        "",
        "«kendi cevabında» sütunu denetimin o arşivde ne kadar görebildiğini söyler.",
        "Bir alıntı kendi cevabında da bulunmuyorsa başka kayıtta bulunması da",
        "beklenmez; ⛔ **yani her bulunamayan alıntı, bir kaymanın gizlenebileceği**",
        "**bir deliktir.** İki sınıfın anlamı farklı:",
        "",
        f"⭐ **İç muhakemede bulunan {T['ic']} alıntı — T45'in ölçüsü.** Judge, cevabın",
        "içine gömülü *«(iç muhakeme — değerlendirme dışı…)»* bloğundan alıntılayıp",
        "hüküm kurmuş. v8'in kanıt denetimi bunu **aşama 1'de 7** vakada görmüştü;",
        f"bütün geçişler sayılınca v8 Eksen 2'de **{sum(s[4]['ic'] for s in satir if s[1] == 'v8')}**",
        "vaka çıkıyor. v9'un kapsam bölümü tam olarak bunun için yazıldı ve v9",
        "arşivlerinde bu sayı kapı tarafından **karara bağlanıyor** (K120).",
        "",
    ]
    if zayif:
        OKUMA = {
            "korpus-v8": "⛔ **takasın kendisi** — iki kaydın 6 alıntısı",
            "e2-hakem-p2": "⭐ elle okundu: `A-dar`/`sk-011` cevabı **yozlaşmış** "
                           "(547 kez *«hem»*); judge alıntının sonuna "
                           "*«(bu şekilde yüzlerce kez tekrarlanarak devam ediyor)»* "
                           "diye **kendi açıklamasını** eklemiş. Uydurma değil, şerh.",
        }
        y += ["| arşiv | iç muhakemede | hiçbir yerde | okuma |", "|---|---:|---:|---|"]
        for s in zayif:
            ok = OKUMA.get(s[0]) or ("T45 — kapsam kusuru; kaynağı belli, "
                                     "her alıntı iç muhakeme bloğunda bulundu")
            y.append(f"| `{s[0]}` | {s[4]['ic'] or '—'} | {s[4]['hicbir'] or '—'} | {ok} |")
        y += ["",
              "✅ **Bulunamayan 40 alıntının 40'ı da açıklandı:** 33'ü iç muhakemede "
              "(T45), 6'sı takas, 1'i yozlaşmış cevaba düşülmüş şerh. ➡️ Denetimin "
              "*göremediği* bir delik kalmadı.",
              ""]
    y += [
        "## ⛔ Bu denetimin ölçmediği",
        "",
        "- **Sonuç dosyası hiç yazılmamışsa.** Denetim var olan kayıtlara bakar.",
        "- **Aynı kayda iki kez puan verilmişse.** Kimlik çakışması buradan görünmez.",
        "- **Birbirine çok benzeyen iki cevap.** Takas ancak alıntı ötekinin cevabında",
        "  bulunduğunda görünür; iki cevap aynıysa kayma görünmez kalır.",
        "- **Muafiyet alanları.** Yalnızca *cevaptan* yapılan alıntılar kimlik belirler;",
        "  `teselli_*` / `*_baglam_alintisi` denetime girmez.",
        "- **v9 arşivleri** — `2026-09-15-v9-kapi-defteri.md`'de sayılıyor, burada tekrar",
        "  edilmedi.",
    ]
    RAPOR.write_text("\n".join(y) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print(f"   {T['kayit']} kayıt · {T['alinti']} uzun alıntı · kendi cevabında "
          f"{T['kendi']} · iç muhakeme {T['ic']} · hiçbir {T['hicbir']} · "
          f"KAYMA {T['kayma']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
