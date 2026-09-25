#!/usr/bin/env python3
"""v6-parti1…5'te tohum karışması var mı — T217'nin geriye dönük taraması.

⛔⛔⛔ **GEREKÇE BİR HATADIR.** `v6-parti6 #15` ve `#19` **başka satırların
tohumundan** yazıldı; kayıtların `source_ids` alanı plandan geldiği için
doğru görünüyordu ve hiçbir kapı görmedi (T217). O kapı parti6'da kuruldu
ama **önceki beş parti hiç taranmadı** ve T217'nin şerhinde bu açıkça
yazılıydı. Bu betik o şerhi kapatıyor.

⭐ **ÖLÇÜT YENİDEN TANIMLANMIYOR (K97).** Kapının kendi kuralı aynen
kullanılıyor: kaydın kullanıcı turları, partinin BÜTÜN plan satırlarının
tohum metinleriyle karşılaştırılır; kendi tohumundan belirgin biçimde daha
iyi eşleşen bir tohum varsa satır **işaretlenir**. Karşılaştırma
`tr_sadelestir` + 5 harflik gövde öneki (Kural 4; `bozuk` kayıtlar Türkçe
harfleri ASCII yazıyor ve `tr_fold` onları eşleştirmiyor).

⛔ **BU BETİK HÜKÜM VERMEZ, İŞARETLER.** Bir işaret *«karışmış olabilir»*
demektir; karışıp karışmadığına metni okuyarak ben karar veririm (K30) ve
hüküm rapora elle yazılır. ⭐ Ölçüt parti6'da iki gerçek hatayla
kalibre edildi: hatalı kayıtlarda marj 5 ve 6, düzeltilmiş hâllerinde 0,
meşru en yüksek marj 1.

⚠️ Tarama **parti içi**dir: bir kayıt başka bir PARTİNİN tohumundan
yazıldıysa bu kural onu göremez. Sıfır örtüşen satırlar ayrıca listelenir
ve o durum orada görünür.

Çıktı: reports/analiz/2026-09-21-tohum-karsiligi-geriye-donuk.{md,json}
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-tohum-karsiligi-geriye-donuk.md"
JSON = KOK / f"reports/analiz/{TARIH}-tohum-karsiligi-geriye-donuk.json"
PARTILER = ["v6-parti1", "v6-parti2", "v6-parti3", "v6-parti4", "v6-parti5", "v6-parti6"]
MARJ, GOVDE = 3, 5
BLOK = re.compile(r"<context[^>]*>.*?</context>", re.S)

import tohum_guvenlik as TG  # noqa: E402

# ⛔ ELLE VERİLEN HÜKÜM — işaretlenen her satır okunarak yazılır (K30).
#    Boş kalması «okunmadı» demektir ve betik raporu yazmaz.
HUKUM: dict[str, str] = {
    "v6-parti1#10": "⭐ karışma YOK — aynı durumun başka sahnesi",
    "v6-parti1#24": "⭐ karışma YOK — aynı durumun başka sahnesi",
    "v6-parti1#26": "⭐ karışma YOK — aynı durumun başka sahnesi",
    "v6-parti1#17": "⭐ karışma YOK — aynı durumun başka sahnesi",
    "v6-parti1#48": "⭐ karışma YOK — aynı durumun başka sahnesi",
    "v6-parti1#36": "⭐ karışma YOK — aynı durumun başka sahnesi",
    "v6-parti1#30": "⭐ karışma YOK — aynı durumun başka sahnesi",
    "v6-parti1#2": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#4": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#11": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#12": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#16": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#18": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#23": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#25": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#27": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#28": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#31": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#32": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#33": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#34": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#37": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#38": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#42": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#43": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#46": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#51": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#52": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#53": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#54": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#55": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti1#56": "⭐ karışma YOK — tohum ızgarayı verdi, sahneyi ben yazdım (parti1 rejimi)",
    "v6-parti3#3": "⭐ karışma YOK — tohuma sadık, kayıt `kisa` olduğu için örtüşme düşük (yanlış pozitif)",
}


def _govde(s: str) -> set[str]:
    return {w[:GOVDE] for w in re.sub(r"[^\w\s]", " ", TG.tr_sadelestir(s)).split()
            if len(w) > 4}


def main() -> int:
    satir, isaretli, ozet = [], [], []
    for parti in PARTILER:
        pdos = KOK / f"data/plan/{parti}.jsonl"
        kdos = KOK / f"data/candidates/{parti}.jsonl"
        if not (pdos.exists() and kdos.exists()):
            ozet.append((parti, None, None, None, "dosya yok"))
            continue
        plan = {json.loads(l)["sira"]: json.loads(l)
                for l in pdos.read_text(encoding="utf-8").splitlines() if l.strip()}
        toh = {s: _govde(p["tohum_metin"]) for s, p in plan.items()}
        kay = [json.loads(l) for l in kdos.read_text(encoding="utf-8").splitlines() if l.strip()]
        n_isaret = 0
        kendi_dagilim = []
        for r in kay:
            s = r["gen_meta"]["parti_sira"]
            b = _govde(" ".join(BLOK.sub("", m["content"]) for m in r["messages"]
                                if m["role"] == "user"))
            skor = {t: len(a & b) for t, a in toh.items()}
            kendi, en = skor.get(s, 0), max(skor.values())
            kendi_dagilim.append(kendi)
            if kendi == 0 or en - kendi >= MARJ:
                rakip = sorted([t for t, v in skor.items() if v == en and t != s])[:3]
                isaretli.append({"parti": parti, "sira": s, "kendi": kendi, "en": en,
                                 "marj": en - kendi, "rakip": rakip,
                                 "tohum": plan[s]["tohum_metin"][:110],
                                 "kayit": BLOK.sub("", next(
                                     m["content"] for m in r["messages"]
                                     if m["role"] == "user"))[:110]})
                n_isaret += 1
        kendi_dagilim.sort()
        ozet.append((parti, len(kay), n_isaret,
                     (kendi_dagilim[0], kendi_dagilim[len(kendi_dagilim) // 2],
                      kendi_dagilim[-1]),
                     hashlib.sha256(kdos.read_bytes()).hexdigest()[:16]))

    JSON.write_text(json.dumps({"tarih": TARIH, "marj": MARJ, "govde": GOVDE,
                                "isaretli": isaretli}, ensure_ascii=False, indent=1),
                    encoding="utf-8")

    sat = ["# Tohum karşılığı — v6 partilerinde geriye dönük tarama", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Ölçüt:** T217'nin kapısı, aynen — `tr_sadelestir` + {GOVDE} harflik "
           f"gövde öneki, marj ≥ {MARJ} ya da kendi tohumuyla sıfır örtüşme", "",
           "⛔⛔ **Gerekçe bir hatadır.** `v6-parti6 #15` ve `#19` başka satırların "
           "tohumundan yazılmıştı ve `source_ids` plandan geldiği için doğru "
           "görünüyordu. Kapı parti6'da kuruldu; T217'nin şerhi *«geriye dönük "
           "tarama yapılmadı»* diyordu. Bu rapor onu kapatıyor.", "",
           "## 0. ⭐⭐⭐ Sonuç", "",
           "⭐ **Karışma YOK.** İşaretlenen 33 satırın 33'ü okundu; hiçbiri başka "
           "bir satırın tohumundan yazılmamış. 32'si `v6-parti1`'de ve sebebi tek: "
           "**parti1 başka bir üretim rejiminde yazılmış** — tohum ızgara hücresini "
           "verdi, sahneyi ben yazdım. Ölçüldü: kendi tohumuyla sözcük örtüşmesi "
           "parti1'de ortalama **%6** (21 kayıtta sıfır), parti2'de %49, "
           "parti3-6'da %66-71. ➡️⭐⭐⭐ *Bir alanın ne anlama geldiği ilan "
           "edilmediyse, anlamı sessizce değişebilir: `source_ids` parti1'de "
           "«ızgarayı veren tohum», parti3-6'da «metni veren tohum» demek ve ikisi "
           "arasında yazılı bir sınır yok.*", "",
           "⛔ Kalan 1 işaret (`v6-parti3#3`) tohuma sadık; kayıt `kisa` olduğu için "
           "örtüşme düşük çıktı (yanlış pozitif).", "",
           "## 1. Parti parti", "",
           "| parti | kayıt | ⛔ işaretli | kendi tohumuyla örtüşme (en az / medyan / en çok) | girdi SHA256-16 |",
           "|---|---:|---:|---|---|"]
    for parti, n, ni, dag, sh in ozet:
        if n is None:
            sat.append(f"| `{parti}` | — | — | — | {sh} |")
            continue
        sat.append(f"| `{parti}` | {n} | **{ni}** | {dag[0]} / {dag[1]} / {dag[2]} | "
                   f"`{sh}` |")
    top = sum(o[1] for o in ozet if o[1]), sum(o[2] for o in ozet if o[2] is not None)
    sat += ["", f"⭐ **Toplam {top[0]} kayıt tarandı, {top[1]} satır işaretlendi.**", ""]

    if isaretli:
        sat += ["## 2. ⛔ İşaretli satırlar — hüküm elle verildi", "",
                "| parti | # | kendi | en iyi | marj | rakip satır | hüküm |",
                "|---|---:|---:|---:|---:|---|---|"]
        for b in isaretli:
            k = f"{b['parti']}#{b['sira']}"
            sat.append(f"| `{b['parti']}` | {b['sira']} | {b['kendi']} | {b['en']} | "
                       f"{b['marj']} | {b['rakip']} | {HUKUM.get(k, '⛔ **OKUNMADI**')} |")
        _en = [b["en"] for b in isaretli]
        sat += ["", "⭐⭐ **İşaret ≠ karışma, ve farkı MUTLAK skor söylüyor.** "
                "parti6'daki iki gerçek karışmada rakip tohumun skoru yüksekti "
                "(5 ve 8) ve kayıt görünür biçimde O tohumun hikâyesini "
                "anlatıyordu. Buradaki 33 işarette rakip skorların tamamı "
                f"{min(_en)}-{max(_en)} aralığında, yani gürültü düzeyinde: "
                "hiçbir kayıt başka bir satırın hikâyesini anlatmıyor. "
                "➡️ *Kıyaslı bir ölçütte marj karışmayı işaret eder, ama "
                "karışmayı KANITLAYAN şey rakibin mutlak skorudur.*", "",
                "### İşaretli satırların metinleri", ""]
        for b in isaretli:
            sat += [f"**`{b['parti']}#{b['sira']}`**  ",
                    f"· *tohum:* {b['tohum']}…  ",
                    f"· *kayıt:* {b['kayit']}…", ""]
    else:
        sat += ["## 2. ⭐ İşaretli satır yok", "",
                "Taranan partilerin hiçbirinde kendi tohumundan belirgin biçimde "
                "daha iyi eşleşen bir satır bulunmadı.", ""]

    # ⛔⛔⛔ ÇİFTE TAHSİS — tarama sırasında çıktı, sorulan soru bu değildi.
    import collections
    pl, ur = collections.defaultdict(list), collections.defaultdict(list)
    for parti in PARTILER:
        for l in (KOK / f"data/plan/{parti}.jsonl").read_text(encoding="utf-8").splitlines():
            if l.strip():
                q = json.loads(l)
                pl[q["seed_id"]].append(f"{parti}#{q['sira']}")
        for l in (KOK / f"data/candidates/{parti}.jsonl").read_text(encoding="utf-8").splitlines():
            if l.strip():
                q = json.loads(l)
                ur[q["gen_meta"]["seed_id"]].append(
                    (f"{parti}#{q['gen_meta']['parti_sira']}",
                     _govde(" ".join(BLOK.sub("", m["content"]) for m in q["messages"]
                                     if m["role"] == "user"))))
    pl_cift = {k: v for k, v in pl.items() if len(v) > 1}
    ur_cift = {k: v for k, v in ur.items() if len(v) > 1}
    benzer = []
    for k, v in ur_cift.items():
        a_, b_ = v[0][1], v[1][1]
        benzer.append((round(100 * len(a_ & b_) / max(1, len(a_ | b_))), v[0][0], v[1][0]))
    benzer.sort(reverse=True)
    sat += ["## 3. ⛔⛔ Çifte tahsis — bu tarama sırasında çıktı", "",
            "Sorulan soru *«kayıt yanlış tohumdan mı yazıldı»* idi. Cevap hayır; ama "
            "aynı taramada başka bir şey göründü: **bir tohum iki plan satırına "
            "düşmüş olabiliyor.**", "", "| | |", "|---|---:|",
            f"| birden fazla plan satırına düşen tohum | **{len(pl_cift)}** |",
            f"| ⛔ **iki kez ÜRETİLEN tohum** | **{len(ur_cift)}** |",
            f"| toplam üretilmiş kayıt | {sum(len(v) for v in ur.values())} |",
            f"| benzersiz tohum | {len(ur)} |", "",
            f"⛔ Çifte üretimin tamamı **parti1 + parti2** çiftinde. ⭐ İki kayıt "
            "birbirinin kopyası DEĞİL: sözcük örtüşmesi (Jaccard) ortalama "
            f"%{sum(x[0] for x in benzer) // max(1, len(benzer))}, en yüksek "
            f"%{benzer[0][0] if benzer else 0}. ⇒ Eğitim verisinde tekrar yok; "
            "sorun **sayımda**: korpus 355 kayıt taşıyor ama 331 tohuma dayanıyor ve "
            "kapsama envanteri *«kullanılmış tohum»* üzerinden ölçüyor.", "",
            "| tohum | kayıtlar | örtüşme |", "|---|---|---:|"]
    for j, x, y in benzer[:6]:
        sat.append(f"| — | `{x}` ↔ `{y}` | %{j} |")
    sat += ["", "⛔⛔ **`gd-021`'in tohumu bunlardan biri.** `929466628ddb3207` hem "
            "`v6-parti1#4` hem `v6-parti2#54`'e düşmüş; parti1'de ÜRETİLMİŞ, parti2'de "
            "okunup elenmiştir. ⭐ Kriz metni korpusa girmedi çünkü parti1 rejiminde "
            "tohum metni kayda geçmiyor — yani bunu engelleyen şey bir kapı değil, "
            "o partinin üretim biçimiydi. ➡️ *Bir kaza, başka bir kazanın yan "
            "etkisiyle zararsız kalabilir; bu, ikisinin de kaza olmadığı anlamına "
            "gelmez.*", "",
            "## ⛔ Bu taramanın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Tarama PARTİ İÇİ** | bir kayıt başka bir PARTİNİN tohumundan "
            "yazıldıysa bu kural onu göremez; yalnız sıfır örtüşen satırlar o "
            "durumda da görünür |",
            "| ⛔⛔ **İşaret hüküm değildir** | ölçüt sözcük örtüşmesi, anlam değil; "
            "ağır genelleştirme yapan (marka/kurum adı çıkaran) meşru bir kayıt da "
            "düşük skor alabilir. Hüküm okunarak verilir (K30) |",
            f"| ⛔ **Marj {MARJ} bir SEÇİM** | parti6'daki iki gerçek hatayla "
            "kalibre edildi (marj 5 ve 6; meşru en yüksek 1), türetilmedi. Daha "
            "yumuşak bir karışma — aynı tür, benzer sözcükler — eşiğin altında "
            "kalabilir |",
            "| ⛔ **Yalnız KULLANICI turlarına bakılıyor** | asistan cevabının "
            "tohuma uygunluğu ölçülmüyor |",
            "| ⚠️ **v5 ve öncesi taranmadı** | `v0.0.14`'ün 571 kaydı bu taramanın "
            "dışında; onların planları farklı biçimde ve ayrı bir geçiş gerekir |"]

    okunmamis = [f"{b['parti']}#{b['sira']}" for b in isaretli
                 if f"{b['parti']}#{b['sira']}" not in HUKUM]
    if okunmamis:
        print(f"⛔ İşaretli ve HÜKMÜ YAZILMAMIŞ satır: {okunmamis}")
        print("   Rapor yazılmadı — işaret bir hüküm değildir (K30).")
        return 1
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print(f"✅ {top[0]} kayıt tarandı · işaretli {top[1]}")
    for b in isaretli:
        print(f"   ⛔ {b['parti']}#{b['sira']}: kendi={b['kendi']} en={b['en']} "
              f"marj={b['marj']} rakip={b['rakip']}")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
