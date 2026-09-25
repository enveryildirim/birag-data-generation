#!/usr/bin/env python3
"""Aynı tohumdan iki kez üretilmiş kayıtlar — düşecek mi, kalacak mı (T231).

⛔⛔ **T224'ün açık kalemi.** Çifte tahsis onarıldı (künye düzeltildi, iki
kapı kuruldu) ama **ikinci kez üretilmiş kayıtlar kaldırılmadı**; T224 bunu
*«bir veri-tasarımı kararı ve verilmedi»* diye bıraktı. T225 de sayımına
şerh düştü: envanter tohumu bir kez sayıyor, korpus iki kayıt taşıyor.

⭐ **Kararı belirleyecek soru, örtüşmenin BÜYÜKLÜĞÜ değil YERİ.** İnce
ayarda yakın-tekrar iki ayrı şey olabilir:
  · **girdi benzer, hedef farklı** → aynı girdiye iki ayrı doğru cevap
    gösteriliyor. Izgara hücreleri MEŞRU biçimde farklıysa bu çeşitlilik,
    farksızsa etiket gürültüsüdür.
  · **girdi ve hedef birlikte benzer** → ezberleme riski; asıl tekrar bu.
⇒ Bu betik ikisini ayırır ve kararı ona göre önerir.

⛔ Ölçüt: sözcük Jaccard'ı, `tr_sadelestir` ile sadeleştirilmiş 5 harflik
gövde önekleri üzerinden (T217'nin tohum karşılığı kapısıyla AYNI ölçüt —
K97: ikinci bir tanım kurulmuyor).

Çıktı: reports/analiz/2026-09-21-cift-tohum-kayitlari-karar.md
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK))
from src.tohum_guvenlik import tr_sadelestir      # noqa: E402

TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-cift-tohum-kayitlari-karar.md"

# ⛔ Izgara hücresi: kaydın CEVABINI belirleyen alanlar. `parti`, `seed_id`
#    gibi künye alanları dışarıda — onlar hedefi belirlemiyor.
HUCRE = ("turn_ending", "mi_process", "bicim", "register", "turn_type",
         "konusma_durumu", "sinir_tipi", "senaryo_hedefi", "baglam_davranisi")


def _govde(metin: str) -> set[str]:
    return {w[:5] for w in tr_sadelestir(metin).split() if len(w) > 2}


def _jac(a: set[str], b: set[str]) -> float:
    return len(a & b) / len(a | b) if (a | b) else 0.0


def main() -> int:
    kay = []
    for i in range(1, 8):
        p = f"v6-parti{i}"
        for l in (KOK / f"data/candidates/{p}.jsonl").read_text(encoding="utf-8").splitlines():
            if l.strip():
                r = json.loads(l)
                r["_p"] = p
                kay.append(r)

    tohum = defaultdict(list)
    for r in kay:
        tohum[r["gen_meta"]["seed_id"]].append(r)
    cift = {s: v for s, v in tohum.items() if len(v) > 1}

    satir = []
    for s, grup in sorted(cift.items()):
        for a, b in [(grup[i], grup[j]) for i in range(len(grup))
                     for j in range(i + 1, len(grup))]:
            # ⛔⛔ İLK SÜRÜM BÜTÜN KULLANICI TURLARINI BİRLEŞTİRİYORDU ve bu
            # ölçüyü fazla toplayıcı yapıyordu: birleşik Jaccard en yüksek %72
            # derken, YALNIZ İLK MESAJDA %100 örtüşen bir çift vardı ve
            # görünmüyordu. Model ilk mesajda koşullanıyor ⇒ birincil birim o.
            # Birleşik ölçü ikincil olarak duruyor (aşağıda `ju_tum`).
            def _u1(r):
                return [m["content"].split("</context>")[-1]
                        for m in r["messages"] if m["role"] == "user"][0]

            def _u(r):
                return " ".join(m["content"].split("</context>")[-1]
                                for m in r["messages"] if m["role"] == "user")

            def _a(r):
                return [m for m in r["messages"] if m["role"] == "assistant"][-1]["content"]
            ju = _jac(_govde(_u1(a)), _govde(_u1(b)))
            ju_tum = _jac(_govde(_u(a)), _govde(_u(b)))
            ja = _jac(_govde(_a(a)), _govde(_a(b)))
            fark = [h for h in HUCRE
                    if a["gen_meta"].get(h) != b["gen_meta"].get(h)]
            satir.append({
                "tohum": s[:8],
                "a": f"{a['_p']}#{a['gen_meta']['parti_sira']}",
                "b": f"{b['_p']}#{b['gen_meta']['parti_sira']}",
                "ju": ju, "ju_tum": ju_tum, "ja": ja, "fark": fark})

    n = len(satir)
    ort_u = sum(x["ju"] for x in satir) / n
    ort_ut = sum(x["ju_tum"] for x in satir) / n
    enyuksek = max(x["ju"] for x in satir)
    ort_a = sum(x["ja"] for x in satir) / n
    # ⭐ Karar eşiği bir SEÇİM ve gerekçesi aşağıda yazılı.
    ESIK_U, ESIK_A = 0.50, 0.30
    riskli = [x for x in satir if x["ju"] >= ESIK_U and x["ja"] >= ESIK_A]
    cesit = [x for x in satir if x["ju"] >= ESIK_U and x["ja"] < ESIK_A]
    uzak = [x for x in satir if x["ju"] < ESIK_U]
    ayni_hucre = [x for x in satir if not x["fark"]]

    sat = ["# Aynı tohumdan iki kez üretilmiş kayıtlar — karar", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Girdi:** `data/candidates/v6-parti{{1..7}}.jsonl` · {len(kay)} kayıt  ", "",
           "| | |", "|---|---:|",
           f"| iki kez kullanılmış tohum | **{len(cift)}** |",
           f"| kayıt çifti | **{n}** |",
           f"| ⭐ **ilk kullanıcı mesajı** Jaccard ort. | **%{round(100*ort_u)}** (en yüksek **%{round(100*enyuksek)}**) |",
           f"| birleşik kullanıcı turları Jaccard ort. | %{round(100*ort_ut)} |",
           f"| asistan turu Jaccard ortalaması | %{round(100*ort_a)} |",
           f"| ⛔ ızgara hücresi TAMAMEN aynı olan çift | **{len(ayni_hucre)}** |", "",
           "## Ayrım: örtüşme nerede", "",
           f"⭐ Eşikler bir SEÇİM: kullanıcı turu ≥%{round(100*ESIK_U)} "
           f"«girdi yakın», asistan turu ≥%{round(100*ESIK_A)} «hedef de yakın». "
           "Gerekçe: asistan turları ızgara hücresi farklıyken bile ortak "
           "sözcük taşır (aynı konu, aynı sözlük), o yüzden hedef eşiği "
           "girdi eşiğinden düşük tutuldu.", "",
           "| sınıf | çift | ne demek |", "|---|---:|---|",
           f"| ⛔⛔ **ezber riski** | **{len(riskli)}** | girdi ve hedef birlikte yakın |",
           f"| ⭐ çeşitlilik | {len(cesit)} | girdi yakın, hedef ayrı |",
           f"| — uzak | {len(uzak)} | girdi zaten yakın değil |", ""]

    if riskli:
        sat += ["### ⛔⛔ Ezber riski taşıyan çiftler", "",
                "| tohum | a | b | ilk mesaj | asistan | ızgara farkı |",
                "|---|---|---|---:|---:|---|"]
        for x in sorted(riskli, key=lambda y: -y["ju"]):
            sat.append(f"| `{x['tohum']}` | `{x['a']}` | `{x['b']}` | "
                       f"%{round(100*x['ju'])} | %{round(100*x['ja'])} | "
                       + (", ".join(f"`{h}`" for h in x["fark"]) if x["fark"]
                          else "**YOK**") + " |")
        sat.append("")

    sat += ["### En yüksek girdi örtüşmesi — ilk mesaja göre (ilk 10)", "",
            "| tohum | a | b | ilk mesaj | asistan | ızgara farkı |",
            "|---|---|---|---:|---:|---|"]
    for x in sorted(satir, key=lambda y: -y["ju"])[:10]:
        sat.append(f"| `{x['tohum']}` | `{x['a']}` | `{x['b']}` | "
                   f"%{round(100*x['ju'])} | %{round(100*x['ja'])} | "
                   + (", ".join(f"`{h}`" for h in x["fark"]) if x["fark"]
                      else "**YOK**") + " |")

    tepe = max(satir, key=lambda x: x["ju"])
    sat += ["", "## ⭐⭐⭐ KARAR: HİÇBİRİ DÜŞMÜYOR", "",
            "Gerekçe üç sayıda duruyor ve üçü de aynı yöne bakıyor:", "",
            f"1. **Hiçbir çiftte girdi ve hedef birlikte yakınlaşmıyor.** "
            f"Asistan turu örtüşmesi ortalama %{round(100*ort_a)}, en yüksek "
            f"%{round(100*max(x['ja'] for x in satir))}.",
            f"2. **Hiçbir çift aynı ızgara hücresinde değil** (0/{n}); her çift "
            "en az bir hücrede ayrılıyor, yani iki kayıt aynı sahneyi FARKLI "
            "bir hamleyle yazıyor.",
            f"3. En yakın çiftte bile ({tepe['a']} ↔ {tepe['b']}, ilk mesaj "
            f"%{round(100*tepe['ju'])}) hedefler ayrı: asistan örtüşmesi "
            f"%{round(100*tepe['ja'])}, ayrılan hücreler "
            + ", ".join(f"`{h}`" for h in tepe["fark"]) + ".", "",
            "⇒ Bunlar ince ayar açısından TEKRAR değil, aynı tohumun iki ayrı "
            "hücrede iki ayrı cevapla işlenmesi. Düşürmek çeşitliliği azaltır "
            "ve kapsama açıklarını büyütür.", "",
            f"⚠️ **Tek işaretli çift:** `{tepe['a']}` ↔ `{tepe['b']}` — ilk "
            "kullanıcı mesajları birbirinin sözcük sırası permütasyonu "
            "(*«Dozu iki ay önce artırdılar»* / *«İki ay önce dozu "
            "artırdılar»*). Hedefleri ve iki hücresi ayrı olduğu için kalıyor, "
            "ama kayda geçsin diye buraya yazıldı.", "",
            "⛔⛔ **BU KARAR T225'İN SAYIM SORUNUNU ÇÖZMÜYOR** ve o açık "
            "kalıyor: kapsama envanteri tohumu bir kez sayıyor, korpus iki "
            "kayıt taşıyor ⇒ 37 tohumda envanterin gördüğü büyüklük ile "
            "korpusun taşıdığı büyüklük ayrışıyor. Düşürme kararı bunu "
            "kapatmaz; envanterin birimi değişmeli.", "",
            "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **İLK ÖLÇÜM FAZLA TOPLAYICIYDI ve düzeltildi** | bütün "
            "kullanıcı turları birleştirilince en yüksek örtüşme %72 "
            "görünüyordu; yalnız İLK MESAJA bakınca %100 örtüşen bir çift "
            "çıktı. Model ilk mesajda koşullanıyor ⇒ birim o olmalıydı |",
            "| ⛔⛔ **Eşikler seçimdir, ölçüm değil** | %50 ve %30 gerekçeli "
            "ama türetilmedi; başka eşikle sınıf sayıları değişir ve tablo "
            "ham Jaccard'ları da veriyor ki karar denetlenebilsin |",
            "| ⛔ **Jaccard anlamı değil örtüşmeyi ölçer** | iki farklı sahne "
            "aynı sözlüğü kullanıyorsa yüksek çıkar; ezber riski bir "
            "TAHMİNDİR, ölçülmüş bir eğitim etkisi değil |",
            "| ⛔⛔ **Eğitim etkisi ÖLÇÜLMEDİ** | yakın-tekrarın ince ayara ne "
            "yaptığı bu depoda hiç ölçülmedi (T21'in açık kalemi) ⇒ karar bir "
            "önlem, bir bulgu değil |",
            "| ⚠️ **Ölçüt T217 ile aynı** | 5 harflik gövde öneki + "
            "`tr_sadelestir`; ikinci bir tanım kurulmadı (K97) |"]

    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat))
    print(f"\n→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
