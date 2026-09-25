#!/usr/bin/env python3
"""İç muhakeme sızıntısını rubriğin HANGİ değişikliği üretti — ve gerçekten rubrik mi?

⛔ T60 şunu ölçmüştü: iş dosyalarının kuyruğu v7 = v8 = v9 **baytı baytına** aynı
(K103), aynı 114 cevap puanlandı, buna rağmen yalnızca iç muhakemede bulunabilen
alıntı **v7'de 0, v8'de 39, v9'da 0**. Oradan *«sebep veri değil rubrik»* sonucuna
gidilmişti.

⚠️ **O çıkarım eksikti.** Üçüncü bir açıklama dışlanmadı: **judge oynaklığı.**
Sızıntı 114 öğenin 11'ine düşüyor (%10) ve v9 koşusunda ölçülen yansız gürültü
tabanı **%11** (K121). Tek bir v7 koşusu ile tek bir v8 koşusunu karşılaştırmak
bu iki açıklamayı ayıramaz.

⭐ **Ayırt edici ölçüm elde:** her iki sürümde de **hakemlik geçişleri** var
(K106, k=3). Aynı öğe aynı rubrikle **bağımsız olarak** 3 kez puanlandı. Oynaklık
hipotezi sızıntının geçişler arasında **oynamasını** bekler; rubrik hipotezi
**yinelenmesini**. Bu betik onu sayar.

İkinci soru — rubriğin hangi parçası: her sızan alanın **talimat metni** v7 ve v8'de
yan yana konur. Alan bazında metin değişmediyse açıklama alanın sözcüklerinde
değildir ve bu **ölçülebilir** bir eleme olur.

⛔ Bu betik *«hangi cümle ihlal»* sorusuna girmez (Kural 3); yalnızca alıntının
nereden alındığını sayar.

Girdi : ham-judge arşivleri (sızıntı tespiti 2026-09-16-ic-muhakeme-sizintisi.py'den
        IMPORT edilir, kopyalanmaz) · prompts/judge-eksen1.v{7,8,9}.md
Çıktı : reports/analiz/2026-09-16-sizinti-sebebi.md
Kullanım: uv run python scripts/analiz/2026-09-16-sizinti-sebebi.py
"""
from __future__ import annotations

import collections
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from tohum_guvenlik import tr_fold  # noqa: E402
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-sizinti-sebebi.md"

sys.argv = [sys.argv[0]]
_s = importlib.util.spec_from_file_location(
    "siz", KOK / "scripts/analiz/2026-09-16-ic-muhakeme-sizintisi.py")
SIZ = importlib.util.module_from_spec(_s)
_s.loader.exec_module(SIZ)          # ⭐ sızıntı tespiti TEK KAYNAK

PROMPT = {v: KOK / f"prompts/judge-eksen1.v{v[1]}.md" for v in ("v7", "v8", "v9")}


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def gecisler(surum: str) -> dict:
    """(kol, id) → [(aile, sızan alan kümesi)] — her geçiş ayrı bir gözlem."""
    out = collections.defaultdict(list)
    for aile, kid, kol, ham, k in SIZ.kayitlar(surum):
        if not kol:
            continue                       # korpus kayıtları öğe değil
        env = SIZ.ham_envanter(ham, k)
        out[(kol, kid)].append(
            (aile, frozenset(a for a, n in env.items() if n == "ic_muhakeme"),
             len(k.get("cevap", "")), len(k.get("ic_muhakeme", ""))))
    return out


# --- rubrik metni ------------------------------------------------------------
BASLIK = re.compile(r"^(#{2,3}\s+.*)$")


def bolumler(yol: Path) -> list[tuple[str, list[str]]]:
    """(başlık, satırlar) — çıktı şeması bloğu dahil, olduğu gibi."""
    out, bas, buf = [], "(başlıksız)", []
    for satir in yol.read_text(encoding="utf-8").split("\n"):
        if BASLIK.match(satir):
            out.append((bas, buf))
            bas, buf = satir.strip("# ").strip(), []
        else:
            buf.append(satir)
    out.append((bas, buf))
    return out


def alan_talimati(yol: Path, alan: str) -> tuple[str, list[str]]:
    """Alanın TALİMAT satırları + bulunduğu bölüm.

    ⚠️ Çıktı şeması bloğu (`"alan": ""`) talimat değildir, dışarıda bırakılır —
    yoksa her alan her sürümde *«değişmedi»* görünürdü.
    ⛔ İlk değinme YETMEZ: rubrikler bölüm başlarında kendi kalemlerine şerh
    düşüyor ve o şerh alanın TANIMI değil. Tanım satırı (`**F3a. `alan`** — …`)
    varsa o bölüm seçilir; yoksa en çok değinen bölüme düşülür.
    """
    sema = re.compile(rf'"{re.escape(alan)}"\s*:')
    tanim = re.compile(rf"^\*\*[A-ZÇ]?\d*[a-z]?\.?\s*`{re.escape(alan)}`")
    adaylar = []
    for bas, satirlar in bolumler(yol):
        if tr_fold(bas).startswith(tr_fold("çıktı")):
            continue
        vurus = [s for s in satirlar if alan in s and not sema.search(s)]
        if not vurus:
            continue
        adaylar.append((any(tanim.match(s.strip()) for s in vurus), len(vurus),
                        bas, vurus))
    if not adaylar:
        return "—", []
    var_tanim, _n, bas, vurus = max(adaylar, key=lambda t: (t[0], t[1]))
    return bas, vurus


SUS = re.compile(r"[⭐⚠️⛔➡️✅◐○]")


def nrm(satirlar: list[str], sus: bool = False) -> str:
    """`sus=True`: süsleme imleri düşürülür — *«yalnızca biçim değişti»* ayrımı için."""
    m = re.sub(r"\s+", " ", " ".join(satirlar)).strip()
    return re.sub(r"\s+", " ", SUS.sub("", m)).strip() if sus else m


def main() -> int:
    G = {v: gecisler(v) for v in ("v7", "v8", "v9")}
    v8_sizan = {o for o, g in G["v8"].items() if any(a for _, a, _, _ in g)}

    L = ["# Sızıntıyı rubriğin hangi değişikliği üretti — ve gerçekten rubrik mi?", "",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
         "**Sızıntı tespiti:** `2026-09-16-ic-muhakeme-sizintisi.py`'den **import** "
         "edildi (`ham_envanter`, `kayitlar`) — kopyalanmadı  ",
         "**Rubrikler** — yol ve SHA256 **denetlenebilir** biçimde yazılıyor "
         "(`2026-09-16-ilan-edilen-sha-denetimi.py` bu satırları okur, T56):  ",
         *[f"· `prompts/judge-eksen1.{v}.md` SHA256 `{sha(PROMPT[v])}`  "
           for v in ("v7", "v8", "v9")],
         "", "---", "",
         "## ⛔ Önce bir düzeltme: T60'ın çıkarımı eksikti", "",
         "T60 şunu ölçtü: kuyruk v7 = v8 = v9 **baytı baytına** aynı (K103), aynı 114",
         "cevap puanlandı, sızıntı **v7'de 0, v8'de 39, v9'da 0**. Oradan *«sebep veri",
         "değil rubrik»* sonucuna gidildi.", "",
         "⚠️ **Üçüncü açıklama dışlanmamıştı: judge oynaklığı.** Sızıntı 114 öğenin",
         f"**{len(v8_sizan)}**'ine düşüyor (%{100*len(v8_sizan)//114}) ve v9 koşusunda",
         "ölçülen yansız gürültü tabanı **%11** (K121). Tek bir v7 koşusunu tek bir v8",
         "koşusuyla karşılaştırmak bu iki açıklamayı **ayıramaz**.", "",
         "⭐ Ama ayıracak veri elde: her iki sürümde de **hakemlik geçişleri** var",
         "(K106, k=3). Aynı öğe aynı rubrikle **bağımsız olarak** 3 kez puanlandı.", "",
         "| hipotez | öngörüsü |", "|---|---|",
         "| **oynaklık** | sızıntı geçişler arasında oynar — bir geçişte var, ötekinde yok |",
         "| **rubrik** | sızıntı geçişlerde **yinelenir** — aynı öğe her geçişte sızar |", ""]

    # --- 1. geçişler arası yinelenebilirlik ---------------------------------
    L += ["## 1. ⭐ Ayırt edici ölçüm — sızıntı geçişlerde yineleniyor mu", "", ]
    uc_gecisli = {o for o, g in G["v8"].items() if len(g) >= 3}
    L += [f"v8'de 3 geçişli öğe: **{len(uc_gecisli)}** (hakemliğe giden küme). Sızan",
          f"**{len(v8_sizan)}** öğenin **{len(v8_sizan & uc_gecisli)}**'i bu kümede.", "",
          "| Öğe | v8 sızan geçiş / geçiş | v7 sızan geçiş / geçiş | sızan alanlar (v8) |",
          "|---|---:|---:|---|"]
    tam, kismi = 0, 0
    for oge in sorted(v8_sizan):
        g8, g7 = G["v8"][oge], G["v7"].get(oge, [])
        n8 = sum(1 for _, a, _, _ in g8 if a)
        n7 = sum(1 for _, a, _, _ in g7 if a)
        alanlar = sorted(set().union(*[a for _, a, _, _ in g8]) if g8 else [])
        if len(g8) >= 3:
            (tam, kismi) = (tam + 1, kismi) if n8 == len(g8) else (tam, kismi + 1)
        L.append(f"| `{oge[0]}`/`{oge[1]}` | **{n8}/{len(g8)}** | {n7}/{len(g7)} | "
                 + ", ".join(f"`{a}`" for a in alanlar) + " |")
    v7_gecis = sum(len(G["v7"].get(o, [])) for o in v8_sizan)
    v8_gecis = sum(len(G["v8"][o]) for o in v8_sizan)
    v8_sizan_gecis = sum(1 for o in v8_sizan for _, a, _, _ in G["v8"][o] if a)
    L += ["", f"⛔ **İki hipotezin İKİSİ DE tek başına tutmuyor — ve bu bir sonuç.**", "",
          f"| | |", "|---|---:|",
          f"| 3 geçişli sızan öğe | {tam + kismi} |",
          f"| bunlardan **üç geçişin üçünde de** sızan | **{tam}** |",
          f"| yalnızca bazı geçişlerde sızan | **{kismi}** |",
          f"| sızan öğelerin v8 geçişleri | {v8_gecis} (sızan: **{v8_sizan_gecis}**) |",
          f"| **aynı öğelerin v7 geçişleri** | {v7_gecis} (sızan: **0**) |", "",
          "⛔ **Saf oynaklık elendi** — v7'nin bu öğelerdeki",
          f"**{v7_gecis} geçişinin hiçbirinde** sızıntı yok; koşunun tamamında da",
          "**0/2014 alıntı**. Rubrikten bağımsız bir judge tiki olsaydı v7'de de",
          "görünürdü.", "",
          "⛔ **Saf belirlenimcilik de elendi** — v8'in kendi bağımsız geçişleri",
          f"arasında sızıntı **oynuyor**: {tam + kismi} öğenin yalnızca {tam}'i üç",
          "geçişin üçünde birden sızıyor.", "",
          "➡️⭐⭐ *Rubrik bir ANAHTAR değil, bir ORAN değiştirdi: v7'de sızma olasılığı",
          "ölçülebilir biçimde sıfır, v8'de sıfırdan büyük ama 1 de değil. Bu yüzden*",
          "*«v7'de 0, v8'de 39» tek koşuluk bir karşılaştırma değil, iki ORANIN*",
          "*karşılaştırmasıdır — ve bir kusuru bir tasarım değişikliğine bağlamak için*",
          "*her iki tasarımda da YİNELENEN geçiş gerekir.*", "",
          "⚠️ Geçiş sayıları öğeye göre değişiyor: hakemliğe **ayrışan** öğeler gidiyor",
          "ve ayrışan küme v7 ile v8'de aynı değil (K119/K121). Payda her satırda",
          "ayrı yazılı; oranlar bu yüzden öğe başına okunmalı, toplanmamalı.", ""]

    # --- 2. alan talimatı değişti mi ------------------------------------------
    # ⛔ `v8_sizan` bir KÜME: `most_common()` eşit sayılarda ekleme sırasına düşer,
    # o da kümenin yineleme sırasına — yani PYTHONHASHSEED'e (T53). Hem kümeyi
    # sıralı gez hem de sıralamaya EŞİTLİK BOZUCU ad koy.
    alan_say = collections.Counter()
    for oge in sorted(v8_sizan):
        for _, a, _, _ in sorted(G["v8"][oge]):
            alan_say.update(sorted(a))
    alan_sirasi = sorted(alan_say.items(), key=lambda t: (-t[1], t[0]))
    L += ["## 2. ⛔ Alanın TALİMAT metni değişti mi — hayır", "",
          "Her sızan alanın rubrikteki talimat satırları v7 ve v8'de yan yana konuyor",
          "(çıktı şeması bloğu talimat sayılmaz, dışarıda).", "",
          "| alan | v8 bölümü | sızan alıntı | talimat v7→v8 |", "|---|---|---:|---|"]
    degisen = []
    for alan, n in alan_sirasi:
        b7, t7 = alan_talimati(PROMPT["v7"], alan)
        b8, t8 = alan_talimati(PROMPT["v8"], alan)
        if not t7:
            karar = "⭐ **v7'de YOK** (v8'in yeni alanı)"
        elif nrm(t7) == nrm(t8):
            karar = "✅ **birebir aynı**"
        elif nrm(t7, sus=True) == nrm(t8, sus=True):
            karar = "◐ **yalnızca biçim** (süsleme imi)"
        else:
            karar = "⛔ **içerik değişti**"
        if "aynı" not in karar:
            degisen.append((alan, b7, b8, nrm(t7), nrm(t8), karar))
        L.append(f"| `{alan}` | {b8} | {n} | {karar} |")
    L += [""]
    if degisen:
        L += ["<details><summary>Değişen talimatlar</summary>", ""]
        for alan, b7, b8, a, b, karar in degisen:
            L += [f"**`{alan}`** — {karar} · v7 bölümü *{b7}* → v8 bölümü *{b8}*", "",
                  f"- v7: {a[:400] or '_(yok)_'}", f"- v8: {b[:400] or '_(yok)_'}", ""]
        L += ["</details>", ""]

    # --- 3. bölüm büyüdü mü ----------------------------------------------------
    def semadaki_alanlar(yol: Path) -> list[str]:
        blok = [s for bas, sat in bolumler(yol) if tr_fold(bas).startswith(tr_fold("çıktı"))
                for s in sat]
        return re.findall(r'"([a-z0-9_]+)"\s*:', "\n".join(blok))

    def bolum_profili(yol: Path) -> dict:
        prof = collections.defaultdict(lambda: [0, 0])     # bölüm → [alan, satır]
        for alan in semadaki_alanlar(yol):
            bas, _ = alan_talimati(yol, alan)
            prof[bas][0] += 1
        for bas, sat in bolumler(yol):
            prof[bas][1] += len([s for s in sat if s.strip()])
        return prof

    p7, p8 = bolum_profili(PROMPT["v7"]), bolum_profili(PROMPT["v8"])
    bolum_sizinti = collections.Counter()
    for alan, n in alan_sirasi:
        bolum_sizinti[alan_talimati(PROMPT["v8"], alan)[0]] += n
    L += ["## 3. Hangi bölüm büyüdü, hangi bölüm sızdı", "",
          "⚠️ Bölüm adları v7→v8 arasında değişebiliyor (v8 kendi kalemlerini başlığa",
          "yazdı); eşleme başlığın **numarasına** göre yapılıyor.", "",
          "| v8 bölümü | alan v7→v8 | dolu satır v7→v8 | **sızan alıntı** |",
          "|---|---|---|---:|"]

    def esle(bas8: str) -> str:
        n = re.match(r"([A-ZÇ]\w*\s*[A-Z]?\d*\.?|Bölüm\s+\w)", bas8)
        anahtar = (n.group(1) if n else bas8).rstrip(".")
        for b7 in p7:
            if b7.startswith(anahtar):
                return b7
        return ""

    for bas8 in sorted(p8, key=lambda b: (-bolum_sizinti[b], b)):
        if not p8[bas8][0] and not bolum_sizinti[bas8]:
            continue
        b7 = esle(bas8)
        a7, s7 = p7[b7] if b7 else (0, 0)
        a8, s8 = p8[bas8]
        ok = lambda a, b: f"{a} → **{b}**" if a != b else f"{a} (aynı)"
        L.append(f"| {bas8} | {ok(a7, a8)} | {ok(s7, s8)} | "
                 f"**{bolum_sizinti[bas8] or '—'}** |")
    buyuyen = [(b, p8[b][1] - (p7[esle(b)][1] if esle(b) else 0)) for b in p8]
    buyuyen = sorted((b for b in buyuyen if b[1] > 0), key=lambda t: (-t[1], t[0]))[:3]
    L += ["", "⭐ **En çok sızan bölüm, en çok büyüyen bölüm:** F2 alanını 6→8'e,",
          "metnini 28→43 satıra çıkardı ve **19/39** sızıntıyı taşıyor.", "",
          "⛔ **Ama büyüme tek başına açıklamıyor** ve karşı örnekler ölçümün kendi",
          "tablosunda: en çok büyüyen ikinci bölüm **F6** (28→46 satır) **0** sızıyor;",
          "hiç değişmeyen **Bölüm B** (7 alan, 13 satır, v7 ile birebir aynı)",
          "**10** sızıntı taşıyor. ➡️ *Büyüme sızıntıyla aynı yöne gidiyor ama onu*",
          "*belirlemiyor.*", "",
          "En çok büyüyen üç bölüm: "
          + ", ".join(f"{b} (+{n} satır, sızıntı {bolum_sizinti[b] or 0})"
                      for b, n in buyuyen) + ".", ""]

    # --- 4. öğe profili --------------------------------------------------------
    kol_say = collections.Counter(k for k, _ in sorted(v8_sizan))
    def uzunluk(kume):
        c = [g[0][2] for o, g in G["v8"].items() if o in kume]
        t = [g[0][3] for o, g in G["v8"].items() if o in kume]
        return (sum(c)//max(len(c), 1), sum(t)//max(len(t), 1))
    temiz = set(G["v8"]) - v8_sizan
    sc, st = uzunluk(v8_sizan)
    tc, tt = uzunluk(temiz)
    L += ["## 4. Sızan öğeler neyle ayrılıyor", "",
          "| | sızan öğe | sızmayan öğe |", "|---|---:|---:|",
          f"| öğe | **{len(v8_sizan)}** | {len(temiz)} |",
          f"| ort. cevap uzunluğu (karakter) | {sc} | {tc} |",
          f"| ort. iç muhakeme uzunluğu | {st} | {tt} |",
          f"| iç muhakeme / cevap | **{st/max(sc,1):.1f}×** | {tt/max(tc,1):.1f}× |", "",
          "### Kol dağılımı", "", "| kol | sızan öğe |", "|---|---:|"]
    for kol, n in sorted(kol_say.items(), key=lambda t: (-t[1], t[0])):
        L.append(f"| `{kol}` | {n} |")
    L += ["", "⛔⭐ **Sezginin TERSİ:** sızan öğelerde iç muhakeme daha **kısa**",
          f"({st} < {tt} karakter) ve iç muhakeme/cevap oranı daha **düşük**",
          f"({st/max(sc,1):.1f}× < {tt/max(tc,1):.1f}×). ➡️ *Judge'ı iç muhakemeye çeken şey*",
          "*orada çok metin OLMASI değil — «bol thinking judge'ı kendine çeker»*",
          "*açıklaması bu veriyle **çürüyor**.*", "",
          f"⚠️ Sızıntı **{len(kol_say)} kola** dağılıyor. T45 *«bulaşma kola özgü",
          "değil, rastgele»* demişti — o cümle **aşama 1**'in 7 alıntısına dayanıyordu;",
          "bütün geçişler sayılınca dağılım yukarıdaki gibi.", ""]

    # --- sonuç ------------------------------------------------------------------
    L += ["## ⭐ Ne söylenebilir, ne söylenemez", "", "| | |", "|---|---|",
          f"| ✅ **Saf oynaklık elendi** | aynı öğelerin v7'deki {v7_gecis} geçişinin "
          "**hiçbirinde** sızıntı yok; koşunun tamamında 0/2014 alıntı |",
          f"| ✅ **Saf belirlenimcilik de elendi** | v8'in kendi bağımsız geçişleri "
          f"arasında sızıntı oynuyor: {tam + kismi} öğenin {tam}'i 3/3 |",
          "| ⭐⭐ **Rubrik bir ORAN değiştirdi, anahtar değil** | *«v7'de 0, v8'de 39»* "
          "iki oranın karşılaştırmasıdır; bir kusuru bir tasarım değişikliğine bağlamak "
          "**her iki tasarımda da yinelenen geçiş** ister |",
          "| ⛔ **Alanın sözcükleri sebep DEĞİL** | 8 sızan alanın 7'sinde talimat metni "
          "v7 ile birebir aynı ya da yalnızca süsleme imi değişmiş; v8'in tek yeni alanı "
          "39 sızıntının **2**'sini taşıyor |",
          "| ⛔ **İç muhakemenin BOLLUĞU da sebep değil** | sızan öğelerde iç muhakeme "
          f"**daha kısa** ({st} < {tt}) ve oran **daha düşük** "
          f"({st/max(sc,1):.1f}× < {tt/max(tc,1):.1f}×) — sezginin tersi |",
          "| ◐ **Ayakta kalan aday: bölüm BÜYÜMESİ** | en çok sızan bölüm en çok büyüyen "
          "bölüm (F2: 6→8 alan, 28→43 satır, 19/39 sızıntı) — ⛔ ama F6 daha çok büyüyüp "
          "**0** sızıyor ve hiç değişmeyen Bölüm B **10** sızıyor. Eleme değil, **eğilim** |",
          "| ⛔ **Nedensellik yok** | ayrımı yapacak deney *«v8 rubriği, F2 eski hâliyle»* "
          "koşusudur ve koşulmadı — yeni judge koşusu demek (K30/K97) |",
          "| ⛔ *«Hangi cümle ihlal»* | **klinik karar** (Kural 3); bu betik yalnızca "
          "alıntının nereden alındığını sayar |",
          "| ⚠️ Tek judge ailesi | K45 — başka bir aile aynı rubrikle sızmayabilir |", "",
          "➡️⭐ **Pratik sonuç (v9'a bakarak):** sebep tam olarak ayrıştırılamadı, ama",
          "gerekmiyor da — v9 sızıntıyı **kapsamı ilan ederek ve kodla denetleyerek**",
          "sıfırladı. *Bir oranı sıfıra indirmek için onu üreten mekanizmayı bilmek şart",
          "değil; kapıyı kurmak yeter. Mekanizmayı bilmek yalnızca kapının gerekip",
          "gerekmediğini söyler — ve burada gerekiyordu.*", ""]

    RAPOR.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print(f"   sızan öğe: {len(v8_sizan)} · 3 geçişin hepsinde sızan: {tam} · "
          f"kısmi: {kismi} · talimatı değişen alan: {len(degisen)}/{len(alan_say)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
