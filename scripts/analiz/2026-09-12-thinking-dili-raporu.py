"""K48-b öğrenilebilirlik testinin raporu. Bkz. Kural 7, K49/K50/K51.
Ham veri: reports/analiz/thinking-dili-ogrenilebilirlik/ · üretim betiği: …-thinking-dili-uretim.py
"""
from __future__ import annotations
import hashlib
import json
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.resolve()
HAM = ROOT / "reports" / "analiz" / "thinking-dili-ogrenilebilirlik"
ABL = ROOT / "reports" / "analiz" / "prompt-dili-ablasyonu" / "generations.jsonl"
DATASET = ROOT / "datasets" / "v0.0.1" / "train.jsonl"
OUT = ROOT / "reports" / "analiz" / "2026-09-12-thinking-dili-ogrenilebilirlik.md"

DIMS = ["duygusal_tepki", "yorumlama", "kesif", "mi_uyumu",
        "grounding", "kisalik_dogallik", "dil_butunlugu"]
OLCEK = {"duygusal_tepki": 2, "yorumlama": 2, "kesif": 2, "mi_uyumu": 5,
         "grounding": 5, "kisalik_dogallik": 5, "dil_butunlugu": 5}
TR_KARAKTER = set("ğışçöüĞİŞÇÖÜ")
TR_KELIME = {"bir", "bu", "ve", "için", "ile", "ama", "değil", "kullanıcı", "soru",
             "cevap", "yani", "çünkü", "olarak", "var", "yok", "gibi"}
EN_KELIME = {"the", "a", "and", "to", "of", "is", "user", "response", "this", "that",
             "should", "not", "it", "for", "answer", "process", "thinking"}


def dil(m: str) -> str:
    k = re.findall(r"[A-Za-zğışçöüĞİŞÇÖÜıİ]+", m.lower())
    if not k:
        return "bos"
    tr = sum(w in TR_KELIME for w in k) + sum(c in TR_KARAKTER for c in m) / 5
    en = sum(w in EN_KELIME for w in k)
    return "tr" if tr > en else ("en" if en else "belirsiz")


def main():
    dar = [json.loads(l) for l in open(HAM / "dar-lora.jsonl") if l.strip()]
    genis = [json.loads(l) for l in open(HAM / "genis-lora.jsonl") if l.strip()]
    jg = json.loads((HAM / "genis-lora-judge.json").read_text())
    abl = [json.loads(l) for l in open(ABL) if l.strip()]
    egitimsiz = [r for r in abl if r["varyant"] == "tr_sys"]
    ref = [json.loads(l) for l in open(DATASET) if l.strip()]
    ref_think = [m["thinking"] for r in ref for m in r["messages"]
                 if m["role"] == "assistant" and m.get("thinking")]

    L = [
        "# thinking dili öğrenilebilir mi? — K48-b öğrenilebilirlik testi",
        "",
        f"**Ham veri:** `{HAM.relative_to(ROOT)}/` "
        f"(dar sha256:{hashlib.sha256((HAM / 'dar-lora.jsonl').read_bytes()).hexdigest()[:12]} · "
        f"geniş sha256:{hashlib.sha256((HAM / 'genis-lora.jsonl').read_bytes()).hexdigest()[:12]}) · "
        # ⛔ Eskiden `…-thinking-dili-raporu.py` yazıyordu: tarih öneki «…» ile
        # kısaltılmıştı ve hiçbir sınama bu adı çözemiyordu (K131).
        "**Betik:** `scripts/analiz/2026-09-12-thinking-dili-raporu.py` · "
        "**Üretim:** `scripts/analiz/2026-09-12-thinking-dili-uretim.py` · "
        "**Tarih:** 2026-09-12",
        "",
        "## Soru ve yöntem",
        "",
        "K48 gösterdi ki muhakeme dili **talimatla** değişmiyor (36/36 İngilizce, açık",
        "*\"Türkçe düşün\"* talimatına rağmen). Geriye tek soru kaldı: **veriyle değişiyor mu?**",
        "",
        "Yöntem: 16 kayıtla 300 adım — **kasıtlı aşırı öğrenme**. Bu bir **üst sınır** testidir;",
        "model bu koşulda Türkçe düşünmüyorsa gerçek ölçekte hiç düşünmez. Değerlendirme",
        "12 tohumla yapıldı ve bu tohumların **hiçbiri eğitim setinde yok** (doğrulandı: 0/12 çakışma).",
        "",
        "İki kol, çünkü ilk (negatif) sonuç LoRA kapasitesiyle karışıyordu:",
        "",
        "| Kol | LoRA kapsamı | modül | eğitilebilir parametre |",
        "|---|---|---|---|",
        "| **dar** | `q_proj`, son 8 katman (üretim config'i) | 8 | 0.328M (%0.004) |",
        "| **geniş** | `q_proj`+`o_proj`+`gate`/`up`/`down`, 42 katman | 210 | **64.91M** (198×) |",
        "",
        "## 1. Sonuç — dil dönüyor, ama yalnızca geniş LoRA'da",
        "",
        "| Kol / kontrol noktası | thinking Türkçe | medyan thinking (kelime) |",
        "|---|---|---|",
    ]
    L.append(f"| *eğitilmemiş (K48 A kolu)* | 0/{len(egitimsiz)} | "
             f"{statistics.median(len(r['thinking'].split()) for r in egitimsiz):.0f} |")
    for ad, veri in (("dar", dar), ("geniş", genis)):
        for e in sorted({r["etiket"] for r in veri}):
            g = [r for r in veri if r["etiket"] == e]
            tr = sum(1 for r in g if dil(r["thinking"]) == "tr")
            L.append(f"| **{ad}** · {e} | {'**' if tr else ''}{tr}/{len(g)}{'**' if tr else ''} | "
                     f"{statistics.median(r['thinking_kelime'] for r in g):.0f} |")
    L.append(f"| *veri seti (hedef)* | {sum(1 for t in ref_think if dil(t) == 'tr')}/{len(ref_think)} | "
             f"{statistics.median(len(t.split()) for t in ref_think):.0f} |")

    L += ["",
          "**İki cevap birden:** geniş LoRA yalnızca dili çevirmedi, **uzunluğu da** veri setinin",
          "referansına oturttu (350 → ~70 kelime). K46'nın gecikme sorunu ile K48-b'nin dil sorunu",
          "**aynı kaldıracın** iki yüzü: ikisi de thinking verisiyle kontrol ediliyor.",
          "",
          "Dar kolun negatifliği veriyle ilgili değildi: aynı dar LoRA uzunluğu bir miktar",
          "oynatabildi (385 → 283 kelime) ama dili hiç oynatamadı — **dil, uzunluktan daha derin**",
          "bir yerde kodlanıyor ve `q_proj`'e sıkışmış bir adapter oraya erişemiyor.",
          "",
          "## 2. Kalite bedeli — aşırı öğrenme neyi bozdu",
          "",
          "geniş LoRA `adapter-100`, judge `agy:gemini-3.8-flash-high`, aynı 12 tohum:",
          "",
          "| Boyut | Ölçek | eğitilmemiş | geniş LoRA (aşırı öğrenilmiş) |",
          "|---|---|---|---|"]
    ok = [r for r in jg if r.get("judge")]
    eok = [r for r in egitimsiz if r.get("judge")]
    for d in DIMS:
        a = statistics.mean(r["judge"][d] for r in eok)
        b = statistics.mean(r["judge"][d] for r in ok)
        isaret = " ⚠️" if b < a - 0.2 else ""
        L.append(f"| {d} | 0-{OLCEK[d]} | {a:.2f} | {b:.2f}{isaret} |")
    ga = statistics.mean(statistics.mean(r["judge"][d] / OLCEK[d] for d in DIMS) for r in eok)
    gb = statistics.mean(statistics.mean(r["judge"][d] / OLCEK[d] for d in DIMS) for r in ok)
    L += ["", f"**Genel (0-1):** eğitilmemiş {ga:.3f} → geniş LoRA **{gb:.3f}**", "",
          "| Sert kapı | eğitilmemiş | geniş LoRA |", "|---|---|---|",
          f"| klinik güvenlik ihlali | {sum(1 for r in eok if r['judge']['klinik_guvenlik_ihlali'])} | "
          f"**{sum(1 for r in ok if r['judge']['klinik_guvenlik_ihlali'])}** |",
          f"| rol sınırı ihlali | {sum(1 for r in eok if r['judge']['rol_siniri_ihlali'])} | "
          f"{sum(1 for r in ok if r['judge']['rol_siniri_ihlali'])} |",
          f"| tuzak ihlali (toplam) | {sum(len(r['judge']['tuzak_ihlali']) for r in eok)} | "
          f"{sum(len(r['judge']['tuzak_ihlali']) for r in ok)} |",
          "",
          "Genel puan **korundu**, tuzak ihlalleri **düştü** — ama klinik güvenlik ihlali **arttı**.",
          "Eksen 2 sıfır toleranslı olduğu için bu, ortalamanın iyiliğine rağmen bir **durdurucudur**.",
          "",
          "## 3. ⚠️ En önemli bulgu — ezberlenen risk cümlesi",
          ""]

    KALIP = "ergen"
    kalip_uretim = [r for r in genis if r["etiket"] == "adapter-100" and KALIP in r["thinking"].lower()]
    kalip_egitim = [m["thinking"] for r in ref for m in r["messages"]
                    if m.get("thinking") and KALIP in m["thinking"].lower()]
    L += [f"Eğitim setinde **{len(kalip_egitim)}/{len(ref)}** kayıtta *\"…ergen kullanıcı, genel ilkeler…\"*",
          f"biçiminde bir **kapanış cümlesi** var. Aşırı öğrenilmiş model bunu, eğitimde görmediği",
          f"tohumların **{len(kalip_uretim)}/12'sinde** neredeyse birebir tekrarlıyor — üstelik",
          "kullanıcı ergen olmadığında bile.", "",
          "En tehlikeli örnek — emziren, doktorundan gizli doz aşan bir kullanıcı:", ""]
    for r in kalip_uretim:
        if "3db31090" in r["seed_id"]:
            j = next((x for x in jg if x["seed_id"] == r["seed_id"]), None)
            L += ["> **Kullanıcı:** " + (j["user_message"] if j else "")[:260], "",
                  "**Modelin thinking'i:**", "", "```", r["thinking"].strip(), "```", ""]
            if j and j.get("judge"):
                L += [f"**Judge:** {j['judge']['gerekce']}", ""]
    L += ["Model *\"Risk sinyali yok\"* diyen bir **kalıp cümleyi güvenlik onayı gibi** kullanıyor.",
          "Mekanizma T7 ile aynı: sabit bir biçim verilirse model biçimi doldurmayı öğrenir,",
          "yargıyı değil. Farkı, burada doldurulan biçimin **güvenlik değerlendirmesi** olması.",
          "",
          "**Veri tasarımı kuralı (K51):** thinking'de risk değerlendirmesi **kalıplaşmış bir",
          "kapanış cümlesi olarak yazılmaz.** Risk yoksa cümle de olmaz; risk varsa gerekçesiyle",
          "ve o kayda özgü yazılır.",
          "",
          "## 4. Açık kalan gerilim",
          "",
          "plan.md §9'un unutma savunması **dar LoRA** diyor. Bu test, Türkçe thinking'in",
          "**geniş LoRA gerektirdiğini** gösteriyor. İkisi doğrudan çelişiyor ve bu test",
          "çelişkiyi çözmüyor — yalnızca görünür kılıyor.",
          "",
          "⚠️ Ayrıca bu koşu **aşırı öğrenmedir** (train loss 0.000, val loss 2.22 → 3.52).",
          "Gösterdiği şey **öğrenilebilirlik**, kalite değil. Gerçek ayar — kapsam, rank, epoch —",
          "Eksen 3 (unutma) ölçümüyle birlikte aranmalı.",
          ]
    OUT.write_text("\n".join(L) + "\n")
    print(f"yazıldı: {OUT}")
    print("\n".join(L[18:60]))


if __name__ == "__main__":
    main()
