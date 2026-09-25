#!/usr/bin/env python3
"""Düşen judge çağrıları kayda değil KONUMA bağlı.

⛔⛔ 2026-09-18 raporunda (T175) şöyle yazdım: *«Ayırt edici özellik ARANDI ve
bulunamadı: istem uzunluğu ortanca 1057 ↔ 1077 krk ⇒ n=18 yanlı sayılmadı ama
yansızlığı da kanıtlanmadı.»* **Yanlıştı — özellik vardı, ben yanlış yerde
aradım.** İçerikte aradım (kategori, uzunluk); bakmadığım şey kaydın **kuyruktaki
sırası**ydı.

⭐ **Bulgu:** düşen çağrılar kuyruğun SONUNDA toplanıyor. Kuyruk sırası
determinist olduğu için (aynı tohum, `ThreadPoolExecutor.map` sırayı korur)
her ikinci çekilişte **aynı kayıtlar** eleniyor ⇒ hayatta kalan örneklem
rastgele bir alt küme değil, sabit bir ÖN EK.

➡️ *Bir örneklem kaybı «rastgele mi» diye sorulurken kaydın özelliklerine
bakılır; oysa kayıp kaydın değil BORU HATTININ özelliğinden doğabilir. Ölçüm
aracının kendi sırası da bir değişkendir.*

⚠️ Sebep ölçülmedi: servis tarafında hız sınırlama, kota baskısı ya da hub'ın
sıra davranışı olabilir — hiçbiri bizden görünmüyor. Ölçülen şey **düşenlerin
nerede olduğu**.

Girdi : data/judged/v0.0.14.jsonl (sıra tohum 11 ile yeniden türetilir)
        düşen listeleri iki koşunun çıktısından alınmıştır (aşağıda kaynak yazılı)
Çıktı : reports/analiz/2026-09-19-dusen-cagrilar-konumu.{md,json}
"""
from __future__ import annotations

import json
import random
import statistics as st
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]

# Düşen kayıtlar — iki koşunun kendi çıktısından (⚠️ elle taşındı, kaynak yazılı):
#   C: 2026-09-18 judge-gurultu-kayma koşusu, «çekiliş C: 18/24 başarılı»
#   E: 2026-09-19 judge-kayma koşusu,        «çekiliş E: 15/24 başarılı»
# Her ikisi de o günün İKİNCİ çekilişi. Birinci çekilişlerde (B, D) düşen yok.
DUSEN = {
    "C (09-18, ikinci çekiliş)": ["5a4684b9", "1f14f47e", "1475abda", "3bcb2545",
                                  "c8b282be", "ea39a038"],
    "E (09-19, ikinci çekiliş)": ["4ac84292", "5a4684b9", "d5e1ed62", "1f14f47e",
                                  "17908b51", "1475abda", "3bcb2545", "c8b282be",
                                  "ea39a038"],
}
BIRINCI = {"B (09-18, birinci)": 0, "D (09-19, birinci)": 0}   # düşen sayısı


def main() -> int:
    kay = [json.loads(s) for s in
           (KOK / "data/judged/v0.0.14.jsonl").read_text(encoding="utf-8").splitlines()
           if s.strip()]
    aday = [r for r in kay
            if not (r.get("judge") or {}).get("yeniden_yargilandi")
            and (r.get("judge") or {}).get("prompt_version") == "judge-eksen1.v9"
            and (r.get("judge") or {}).get("yorumlama") is not None]
    random.Random(11).shuffle(aday)               # ⭐ ölçüm betikleriyle AYNI tohum
    ornek = aday[:24]
    sira = {r["id"][:8]: i for i, r in enumerate(ornek)}
    n = len(ornek)
    son_ceyrek = set(range(n - n // 4, n))

    sat = ["# Düşen judge çağrıları kayda değil konuma bağlı", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Sıra:** `data/judged/v0.0.14.jsonl` + tohum **11** (ölçüm betikleriyle "
           f"aynı) ⇒ kuyruk {n} kayıt, 0 = ilk işlenen", "",
           "⛔⛔ **Bu rapor 2026-09-18 tarihli kendi raporumu düzeltir.** Orada "
           "*«ayırt edici özellik arandı ve bulunamadı»* yazmıştım; içerikte aradım "
           "(kategori, istem uzunluğu) ve kaydın **kuyruktaki sırasına** hiç bakmadım.", "",
           "## 1. ⭐⭐⭐ Düşenler nerede", "",
           "| çekiliş | düşen | kuyruk konumları | ortanca konum | son çeyrekte |",
           "|---|---:|---|---:|---:|"]
    ozet = {}
    for ad, ids in DUSEN.items():
        k = sorted(sira[i] for i in ids if i in sira)
        ozet[ad] = {"konumlar": k, "ortanca": st.median(k) if k else None,
                    "son_ceyrekte": sum(1 for x in k if x in son_ceyrek)}
        sat.append(f"| {ad} | {len(k)} | {k} | {st.median(k):.0f} | "
                   f"{ozet[ad]['son_ceyrekte']}/{len(k)} |")
    for ad, d in BIRINCI.items():
        sat.append(f"| {ad} | {d} | — | — | — |")
    ortak = sorted(set(DUSEN["C (09-18, ikinci çekiliş)"]) &
                   set(DUSEN["E (09-19, ikinci çekiliş)"]))
    sat += ["",
            f"⭐⭐ **İki günün düşenleri örtüşüyor:** {len(ortak)} kayıt her iki ikinci "
            f"çekilişte de düştü, konumları {sorted(sira[i] for i in ortak)}. Kuyruk "
            "sırası determinist olduğu için bu **aynı kayıtların** elenmesi demektir.", "",
            "⭐⭐⭐ **Ve düşme yalnız İKİNCİ çekilişlerde:** birinci çekilişlerde (B, D) "
            f"{n}/{n} başarılı. ➡️ *Kayıp kaydın değil **boru hattının** özelliğinden "
            "doğuyor; ölçüm aracının kendi sırası da bir değişkendir.*", "",
            "## 2. ⛔ Bunun bozduğu şey", "", "| | |", "|---|---|",
            "| ⛔⛔ **Hayatta kalan örneklem sabit bir ÖN EK** | rastgele bir alt küme "
            "değil; her ikinci çekilişte kuyruğun aynı başı ölçülüyor |",
            "| ⛔ **T175'in «yansız sayılmadı ama yanlı da değil» şerhi zayıftı** | "
            "yanlılık vardı, yanlış yerde arandı |",
            "| ⚠️ **Gürültü ölçümleri bundan çok etkilenmez** | karşılaştırma aynı "
            "kayıtlar üzerinde yapılıyor; etkilenen şey örneklemin TEMSİL gücü |", "",
            "## 3. ⭐ Düzeltme", "",
            "Ölçüm betiklerinde kuyruk sırası artık **her çekiliş için ayrı "
            "karıştırılıyor** ⇒ düşenler sabit bir ön ekte toplanmaz, örneklem kaybı "
            "rastgeleleşir. Karıştırma yalnız gönderim sırasını değiştirir; önbellek "
            "anahtarı sıraya bağlı olmadığı için `--kurtar` kipi etkilenmez.", "",
            "## ⛔ Söylenmeyenler", "", "| | |", "|---|---|",
            "| ⛔⛔ **Sebep ölçülmedi** | hız sınırlama, kota baskısı, hub sıra davranışı "
            "— hiçbiri bizden görünmüyor |",
            "| ⛔ **İki koşu** | desen iki günde yinelendi ama n=2 koşu |",
            "| ⛔ **Düşen listeleri elle taşındı** | koşu çıktılarından; kaynak betiğin "
            "başında yazılı (Kural 7'nin zayıf halkası) |", ""]

    (KOK / f"reports/analiz/{TARIH}-dusen-cagrilar-konumu.json").write_text(
        json.dumps({"tarih": TARIH, "n": n, "sira_tohumu": 11, "ozet": ozet,
                    "iki_gunde_ortak": ortak}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    (KOK / f"reports/analiz/{TARIH}-dusen-cagrilar-konumu.md").write_text(
        "\n".join(sat), encoding="utf-8")
    print("\n".join(sat[4:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
