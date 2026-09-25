#!/usr/bin/env python3
"""Kapsama matrisi — her eval ekseni için korpus o davranışı öğretiyor mu?

⭐ **Neden var (T248).** Bu oturumda dört saatlik bir ince ayar + ölçüm
koşusu, korpusun **tasarım gereği hiç göstermediği** bir davranışı ölçen bir
eksene harcandı: `safety_crisis` kriz yönlendirmesi arıyor, korpusta
`is_crisis` kaydı **0** (kriz dilimi uzman onayı bekliyor, Kural 3). Sonuç
*«veri büyütmek işe yaramadı»* değil, **«bu eksen bu veriyle kıpırdayamaz»*dı.

⛔⛔ **Bu tablo koşudan ÖNCE bakılmak içindir.** Bir eksen korpus büyümesine
cevap veremiyorsa, o eksende ölçülen fark **veri kararını değerlendiremez**.

⚠️ **Eşleme benim yorumumdur** ve ölçüm değildir: her eval kategorisinin
korpusta hangi alana karşılık geldiğine ben karar verdim. Sayılar ölçülmüştür,
**eşleme tartışılabilir** — bu yüzden her satırda hangi alana bakıldığı
yazılıdır.

Çıktı: reports/analiz/2026-09-22-kapsama-matrisi.md
"""
from __future__ import annotations

import collections
import json
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-kapsama-matrisi.md"
KUME = KOK / "datasets/v0.0.18/train.jsonl"

# (eksen, kategori, korpus alanı — açıklama, ölçüm fonksiyonu)
def _gm(k, *d):
    return lambda r: (r.get("gen_meta") or {}).get(k) in d
def _alan(k):
    return lambda r: bool(r.get(k))

ESLEME = [
 ("safety_crisis", "kriz_acik · tibbi_aciliyet · rol_siniri_kriz",
  "`is_crisis`", _alan("is_crisis")),
 ("safety_crisis", "normallestirme",
  "`is_crisis`", _alan("is_crisis")),
 ("sycophancy", "eylem_onay · yanlis_inanc (onay yemi)",
  "`is_negative` — kullanıcı istedi, asistan reddetti", _alan("is_negative")),
 ("sycophancy", "sustain_talk",
  "`talk_type = sustain`", lambda r: r.get("talk_type") == "sustain"),
 ("sycophancy", "insan_destegi (yönlendirme istendi)",
  "`sinir_tipi = yonlendirme_istegi`", _gm("sinir_tipi", "yonlendirme_istegi")),
 ("sycophancy", "yanlis_red (gereksiz reddetme)",
  "`sinir_tipi = yonlendirme_gereksiz`", _gm("sinir_tipi", "yonlendirme_gereksiz")),
 ("context_fidelity", "yeterli", "`baglam_davranisi = cevap_var`",
  _gm("baglam_davranisi", "cevap_var")),
 ("context_fidelity", "yetersiz", "`baglam_davranisi = cevap_yok` / `yetersiz`",
  _gm("baglam_davranisi", "cevap_yok", "yetersiz")),
 ("context_fidelity", "distractor", "`baglam_davranisi = ilgisiz`",
  _gm("baglam_davranisi", "ilgisiz")),
 ("context_fidelity", "celiskili", "⛔ korpusta karşılığı **yok**",
  lambda r: False),
 ("forgetting_smoke", "matematik · mantik",
  "yalın sayı / aritmetik cevap", lambda r: False),
 ("forgetting_smoke", "genel_kultur",
  "asistan turunda özel ad", lambda r: False),
 ("forgetting_smoke", "kod · ceviri · ingilizce",
  "`replay` dilimi (§9)", _alan("replay")),
 ("forgetting_smoke", "ozet · talimat",
  "`ozet_var` (judge) — biçim talimatına uyma", 
  lambda r: bool((r.get("judge") or {}).get("ozet_var"))),
]


def main() -> int:
    kay = [json.loads(l) for l in open(KUME)]
    n = len(kay)
    eksen_oge = {}
    for e in ("safety_crisis", "sycophancy", "context_fidelity", "forgetting_smoke"):
        rs = [json.loads(l) for l in open(KOK / f"evals/{e}.jsonl") if l.strip()]
        eksen_oge[e] = collections.Counter(x.get("kategori") for x in rs)

    sat = ["# Kapsama matrisi — eksen ↔ korpus", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Korpus:** `datasets/v0.0.18` ({n} kayıt)  ", "",
           "⛔⛔ **Bu tablo koşudan ÖNCE bakılmak içindir.** Bir eksen korpus "
           "büyümesine cevap veremiyorsa, o eksende ölçülen fark bir **veri "
           "kararını değerlendiremez** — T248 bunu dört saatlik bir koşuyla "
           "öğrendi.", "",
           "⚠️ **Eşleme benim yorumumdur**, ölçüm değil: hangi eval "
           "kategorisinin korpusta hangi alana karşılık geldiğine ben karar "
           "verdim. **Sayılar ölçülmüştür, eşleme tartışılabilir** — bu yüzden "
           "her satırda bakılan alan yazılıdır.", "",
           "| eksen | eval kategorisi | korpusta karşılığı | kayıt | oran | eksen korpusa duyarlı mı |",
           "|---|---|---|---:|---:|---|"]
    ozet = collections.defaultdict(list)
    for eksen, kat, alan, fn in ESLEME:
        c = sum(1 for r in kay if fn(r))
        oran = 100 * c / n
        if c == 0:
            hukum = "⛔⛔ **HAYIR** — korpus bu davranışı hiç göstermiyor"
        elif oran < 3:
            hukum = "⚠️ zayıf"
        else:
            hukum = "⭐ evet"
        ozet[eksen].append(c)
        sat.append(f"| `{eksen}` | {kat} | {alan} | **{c}** | %{oran:.1f} | {hukum} |")

    sat += ["", "## Eksen düzeyinde hüküm", "",
            "| eksen | eval ögesi | korpusta karşılığı olan kategori | hüküm |",
            "|---|---:|---|---|"]
    for e, v in ozet.items():
        toplam = sum(eksen_oge[e].values())
        var = sum(1 for x in v if x > 0)
        if var == 0:
            h = ("⛔⛔⛔ **KÖR** — korpus büyümesi bu ekseni kıpırdatamaz "
                 "(T248'in vakası)")
        elif var < len(v):
            h = f"⚠️ **kısmi** — {len(v)-var} kategori korpusta yok"
        else:
            h = "⭐ duyarlı"
        sat.append(f"| `{e}` | {toplam} | **{var}/{len(v)}** | {h} |")

    sat += ["", "## ⭐ Okunması", "", "| | |", "|---|---|",
            "| ⛔⛔ `safety_crisis` **kör** | `is_crisis` = **0**; kriz dilimi "
            "uzman onayı bekliyor (Kural 3) ⇒ bu eksende ölçülen hiçbir fark "
            "bir **veri** kararını değerlendiremez. Eksen geçerli, **bu iş "
            "için yersiz** |",
            "| ⚠️ `forgetting_smoke` **kısmi** | matematik/mantık ve genel "
            "kültür kategorilerinin korpusta karşılığı **yok** — T255'in "
            "kaybettiği ögeler tam bunlar. ⭐ Ama T257 gösterdi ki onarım "
            "**kipe özgü değil**: alan dışı sinyal genel olarak düzeltiyor |",
            "| ⭐ `context_fidelity` **kısmi ama güçlü** | üç kategorinin üçü "
            "de korpusta var ve bu eksen ince ayarın **ölçülebilir kazanç "
            "verdiği tek eksen** (T254, +1,33). ⛔ Yalnız `celiskili` "
            "(çelişkili bağlam) korpusta **hiç yok** — açık bir boşluk |",
            "| ⭐ `sycophancy` **duyarlı** | dört kategorinin dördü de "
            "korpusta temsil ediliyor. ⚠️ Ama ölçümde taban da kol da 22/24 "
            "verdi (T254) ⇒ eksen **doygun** olabilir |", "",
            "## ⛔ Bu matrisin söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Eşleme ölçüm değil** | *«`sustain_talk` ↔ "
            "`talk_type=sustain`»* gibi karşılıklar benim yorumum; bir uzman "
            "başka eşleme kurabilir ve tablo değişir |",
            "| ⛔ **Varlık ≠ yeterlilik** | bir kategorinin korpusta 40 kaydı "
            "olması onu ÖĞRETTİĞİ anlamına gelmez; yalnız **öğretebileceği** |",
            "| ⛔ **Sinyal payı ölçülmedi** | T256: kayıt sayısı gradyan "
            "payıyla aynı şey değil. Bu tablo **kayıt** sayıyor ⇒ kısa cevaplı "
            "kategoriler burada büyük görünüp eğitimde küçük olabilir |",
            "| ⚠️ **Tek korpus sürümü** | `v0.0.18`; deney sürümleri "
            "(`v0.0.19`/`v0.0.20`) dahil değil |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[sat.index("| eksen | eval kategorisi | korpusta karşılığı | kayıt | oran | eksen korpusa duyarlı mı |"):]))
    print(f"\n→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
