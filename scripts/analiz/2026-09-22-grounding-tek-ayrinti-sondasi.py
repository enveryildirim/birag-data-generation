#!/usr/bin/env python3
"""`grounding` bir TEK-AYRINTI SONDASIDIR — ve bu, judge'ların aynı metinde
farklı puan vermesinin sebebi olabilir.

⭐ **Nasıl çıktı:** `v6` kalan partileri subagent judge'a verilirken bir alt
ajan `064` numaralı iş için *«cevap, kullanıcının hiç söylemediği bir
ayrıntıyı (uykusuzluk) listeye koyuyor»* diye not düştü. O kayıt **eşli**
kümedeydi ⇒ Gemini de yargılamıştı ⇒ iki yargı yan yana konabildi.

⛔⛔ **Mekanizma (`src/filter.py`):** `grounding` judge'dan GELMEZ, tek bir
alandan türer:

    uydurma = (_dogrula(data, "en_somut_ayrinti", ...)
               and not data.get("ayrinti_konusmada_var")
               and not data.get("ayrinti_hipotez_olarak_isaretli"))
    data["grounding"] = 2 if uydurma else 5

⇒ Ölçü *«cevapta uydurma var mı»* diye sormuyor; *«judge'ın SEÇTİĞİ tek
ayrıntı dayanaklı mı»* diye soruyor. Aynı cevapta dayanaklı bir ayrıntı da
uydurma bir ayrıntı da varsa, judge hangisini seçerse puan o olur.

⭐⭐⭐ **Bu, T236 ailesinin dördüncü biçimidir:** alan (`en_somut_ayrinti`)
DOLUYDU, biçimi geçerliydi, judge sorulan soruyu DOĞRU yanıtladı — yanlış
olan **sorunun kendisi**: tekil bir alan, çoğul bir olguyu ölçüyor.

Çıktı: reports/analiz/2026-09-22-grounding-tek-ayrinti-sondasi.md
"""
from __future__ import annotations

import json
import re
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-grounding-tek-ayrinti-sondasi.md"
GEMINI = ["v6-parti1", "v6-parti2", "v6-parti3"]

# ⛔⛔ Bu sezici DÜZ BİR DÜZENLİ İFADE ve Türkçe serbest metinde koşuyor —
#   yani T22 serisinin tam olarak uyardığı şey. Bulduğu sayı bir ALT SINIR
#   ve tek başına hiçbir şey kanıtlamaz; kanıt eşli vakada.
UYD = re.compile(r"konuşmada geçmeyen|geçmeyen bir ayrıntı|uydur|"
                 r"kullanıcının söylemediği|söylemediği bir|metinde olmayan|"
                 r"dayanağı olmayan", re.I)


def main() -> int:
    tot = g5 = g2 = celiskili = 0
    vaka = []
    for p in GEMINI:
        for l in open(KOK / f"data/judged/{p}.jsonl"):
            r = json.loads(l)
            j = r.get("judge")
            if not j:
                continue
            tot += 1
            g = j.get("grounding")
            g5 += g == 5
            g2 += g == 2
            if g == 5 and UYD.search(j.get("gerekce") or ""):
                celiskili += 1
                vaka.append((p, r["id"][:8], j.get("en_somut_ayrinti"),
                             j.get("ayrinti_konusmada_var"), j.get("gerekce")))

    sat = ["# `grounding` bir tek-ayrıntı sondasıdır", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Girdi:** `data/judged/v6-parti{{1,2,3}}.jsonl` ({tot} Gemini yargısı)  ", "",
           "## Mekanizma", "",
           "`grounding` judge'dan gelmez; `src/filter.py` **tek bir alandan** "
           "türetir:", "", "```python",
           'uydurma = (_dogrula(data, "en_somut_ayrinti", ...)',
           '           and not data.get("ayrinti_konusmada_var")',
           '           and not data.get("ayrinti_hipotez_olarak_isaretli"))',
           'data["grounding"] = 2 if uydurma else 5', "```", "",
           "⛔⛔ Ölçü *«cevapta uydurma var mı»* diye **sormuyor**; *«judge'ın "
           "SEÇTİĞİ tek ayrıntı dayanaklı mı»* diye soruyor. Aynı cevapta hem "
           "dayanaklı hem uydurma bir ayrıntı varsa, puanı **seçim** belirler.", "",
           "## ⭐⭐⭐ Eşli kanıt — aynı kayıt, iki judge", "",
           "`v6-parti3 / 9bba8db7` bugünkü koşuda **eşli** kümedeydi: Gemini "
           "onu daha önce, Claude bugün yargıladı. Cevabın son cümlesi:", "",
           "> *«…iki gündür aldığın bir ilaç, birbirini tutmayan iki yazı, "
           "**uyuyamadığın geceler** ve yanında kimse yok.»*", "",
           "Kullanıcı uykudan **hiç söz etmiyor**.", "",
           "| | Gemini | Claude |", "|---|---|---|",
           "| seçtiği `en_somut_ayrinti` | *«iki gündür aldığın bir ilaç»* | "
           "*«uyuyamadığın geceler»* |",
           "| `ayrinti_konusmada_var` | `True` | `False` |",
           "| ⇒ türetilen `grounding` | **5** | **2** |",
           "| kendi `gerekce`'si | ⭐ *«…konuşmada geçmeyen uyuyamadığı "
           "ayrıntısını eklemektedir»* | *«…hiç söylemediği bir ayrıntıyı "
           "kesin bir liste içinde sunuyor»* |", "",
           "⭐⭐⭐ **İki judge metin konusunda ANLAŞIYOR.** İkisi de uydurmayı "
           "gördü ve ikisi de gerekçesinde yazdı. Puanları ayıran şey "
           "sertlik değil, **hangi ayrıntıyı adlandırdıkları**.", "",
           "⛔⛔ Bu, K45'in bir cümlesini niteler. K45 *«Gemini grounding'de "
           "5.00 verdi — uydurulmuş «beş gece» hatasını **o da kaçırdı**»* "
           "diyordu. Burada Gemini **kaçırmadı**: gördü, yazdı, ve **ölçü onu "
           "attı**. ⇒ *«judge kaçırdı»* ile *«ölçü taşımadı»* ayrı şeyler ve "
           "grounding sayısı ikisini ayırt etmiyor.", "",
           "## Tarama — ölçü kendi gerekçesiyle kaç kez çelişiyor", "",
           "| | |", "|---|---:|", f"| Gemini yargısı | {tot} |",
           f"| `grounding` = 5 | {g5} |", f"| `grounding` = 2 | {g2} |",
           f"| ⛔ **5 ama gerekçe uydurma diyor** | **{celiskili}** |", ""]
    if vaka:
        sat += ["| kayıt | seçilen ayrıntı | konuşmada var? | gerekçe |",
                "|---|---|---|---|"]
        for p, i, a, v, g in vaka:
            sat.append(f"| `{p} / {i}` | *«{a}»* | `{v}` | {g[:110]} |")
    sat += ["", "⛔⛔ **Bu sayı bir ALT SINIRDIR ve seziciye güvenilmez.** "
            "Çelişkiyi arayan şey `gerekce` üzerinde koşan **düz bir düzenli "
            "ifade** — yani T22 serisinin tam olarak uyardığı biçim. Ayrıca "
            "`gerekce` tek cümledir: bir uydurma varken judge'ın ondan söz "
            "etmemesi olağan ⇒ görülmeyenler sayılamaz. ⭐ Asıl kanıt sayıda "
            "değil, **eşli vakadadır**: orada mekanizma doğrudan görülüyor.", "",
            "## ⭐ Bu ölçümün koşuya etkisi", "",
            "| | |", "|---|---|",
            "| ⛔⛔ **`grounding` farkı bir SERTLİK farkı sayılamaz** | iki "
            "judge arasındaki `grounding` ayrışması **örnekleme** farkından "
            "gelebilir (hangi ayrıntı seçildi) ⇒ Claude↔Gemini kalibrasyonunda "
            "bu boyut böyle okunmalı |",
            "| ⭐ **K98'in tabanı bu boyutta %100'dü** | yani judge kendisiyle "
            "hep aynı ayrıntıyı seçiyor; ⛔ ama **aynı judge** demek **aynı "
            "seçim eğilimi** demek ⇒ yüksek taban, sondanın dar olduğunu "
            "gizler |",
            "| ⚠️ **Onarım önerisi ölçülmedi** | *«bu benim önerim»*: alan "
            "**çoğul** olmalı (`en_somut_ayrintilar`) ya da ayrı bir "
            "*«başka dayanaksız ayrıntı var mı»* sorusu eklenmeli. İkisinin de "
            "maliyeti ve yanlış-pozitif oranı ölçülmedi |", "",
            "## ⛔ Bu raporun söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **Uydurma SIKLIĞI ölçülmedi** | ölçülen şey, ölçünün bir "
            "uydurmayı taşıyıp taşımadığı; korpusta kaç uydurma olduğu **hâlâ "
            "bilinmiyor** ve bu sonda ile bilinemez |",
            "| ⛔ **İki vaka ELLE doğrulandı, ötekiler değil** | 160 yargının "
            "158'inin gerekçesi okunmadı |",
            "| ⚠️ **Claude tarafı henüz eksik** | bu tarama yalnız Gemini "
            "yargıları üzerinde koştu; Claude yargıları koşu bitince aynı "
            "betikle taranabilir |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print(f"Gemini yargısı {tot} · g5 {g5} · g2 {g2} · ⛔ çelişkili {celiskili}")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
