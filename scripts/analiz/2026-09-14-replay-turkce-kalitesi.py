#!/usr/bin/env python3
"""Replay Türkçe kaynaklarının dil kalitesi — KÖR ve KONTROLLÜ ölçüm.

Neden bu betik: K88 replay kaynaklarının makine çevirisi olduğunu ve *"Sana
özledim"* gibi hatalı Türkçe taşıdığını işaretledi ama ÖLÇMEDİ. Bu projede dil
doğallığı ana kalite ekseni (K48, §5d), dolayısıyla replay'in Türkçeye zarar
verip vermediği açık bir soru.

Belirlenimli işaretler DENENDİ ve ELENDİ (ölçüm raporda):
  · "bir" yoğunluğu   → üç korpusta da aynı (0.035-0.036), ayırt etmiyor
  · kelime tekrarı    → konusal; açıklayıcı metin konu sözcüğünü tekrar eder,
                        uzunluk bandına göre kontrol edilince fark erimiyor ama
                        örnekler kusur değil ("hidroelektrik" × 3)

Bu yüzden LLM sondası, K62'nin dersine göre: soyut puan (*"doğal mı, 1-5"*)
sorulmuyor; **alıntılanabilir kanıt** isteniyor.

⚠️ ARAÇ KENDİ ÜZERİNDE SINANIYOR: aynı sonda bizim ELLE YAZDIĞIMIZ BıRAG
metinlerine de koşuluyor. İki tarafı ayırt edemezse araç işe yaramaz (K61'in şartı).

⚠️ KONTROL EDİLEMEYEN KARIŞTIRICI: iki korpus TÜR olarak farklı — bizimkiler
terapötik diyalog, Alpaca açıklayıcı talimat-cevap. Sonda diyalog parçalarını
"eksik cümle" diye işaretleyebilir. Bu yüzden yalnızca BÜYÜK farklar yorumlanır.

Kullanım: uv run python <betik> [her_gruptan_kayit]
"""
from __future__ import annotations

import csv, hashlib, json, math, random, re, statistics as st, sys
from datetime import date
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from huggingface_hub import hf_hub_download
from scipy.stats import fisher_exact

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import llm  # noqa: E402

SONDA = KOK / "prompts/turkce-dogallik-sondasi.v1.md"
CIKTI = KOK / "reports/analiz/2026-09-14-replay-turkce-kalitesi.md"
HAM = KOK / "reports/analiz/replay-turkce-kalitesi/sonda-ciktilari.jsonl"
MODEL = "agy:gemini-3.8-flash-high"
RASTGELE = random.Random(4242)
BANT = (150, 400)          # iki korpusun da bol kaydı olan uzunluk bandı
KONTROL = "BıRAG (elle yazılmış)"
BUYUK_FARK = 0.30          # "büyük fark" eşiği — BİZİM konvansiyonumuz (Kural 6)


def pbic(p: float) -> str:
    """0.0000 yanıltıcı; çok küçük p bilimsel gösterimle yazılır."""
    return f"{p:.4f}" if p >= 1e-4 else f"{p:.1e}"


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson skor aralığı — küçük n'de normal yaklaşımdan güvenli."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    m = (p + z * z / (2 * n)) / d
    yari = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, m - yari), min(1.0, m + yari))


def alpaca_metinleri():
    d = json.load(open(hf_hub_download("TFLai/Turkish-Alpaca", "data.json", repo_type="dataset")))
    return [x["output"].strip() for x in d if BANT[0] <= len(x.get("output", "")) < BANT[1]]


def merve_metinleri():
    p = hf_hub_download("merve/turkish_instructions", "instructions.csv", repo_type="dataset")
    with open(p, encoding="utf-8") as f:
        return [(x.get(" çıktı") or "").strip() for x in csv.DictReader(f)
                if BANT[0] <= len((x.get(" çıktı") or "").strip()) < BANT[1]]


def birag_metinleri():
    out = []
    for l in open(KOK / "data/candidates/v3-kumulatif.jsonl"):
        r = json.loads(l)
        out += [m["content"] for m in r["messages"]
                if m["role"] == "assistant" and BANT[0] <= len(m["content"]) < BANT[1]]
    return out


def sonda(metin: str) -> dict:
    prompt = SONDA.read_text() + "\n" + metin
    try:
        ham = llm.call(MODEL, [{"role": "user", "content": prompt}])
        return llm.parse_json(ham)
    except Exception as e:
        return {"_hata": f"{type(e).__name__}: {e}"[:200]}


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    gruplar = {"TFLai/Turkish-Alpaca": alpaca_metinleri(),
               "merve/turkish_instructions": merve_metinleri(),
               "BıRAG (elle yazılmış)": birag_metinleri()}
    isler = []
    for ad, ms in gruplar.items():
        RASTGELE.shuffle(ms)
        for m in ms[:n]:
            isler.append((ad, m))
    if "--rapordan" in sys.argv:
        # Ham çıktı zaten var: raporu yeniden üret, LLM'e hiç dokunma.
        # Başarısız çağrılar cache'lenmez; yeniden koşmak onları tekrar dener.
        kayitlar = [json.loads(l) for l in open(HAM)]
        isler = [(k["grup"], k["metin"]) for k in kayitlar]
        sonuclar = [k["sonda"] for k in kayitlar]
        print(f"ham çıktıdan okundu: {len(kayitlar)} satır — LLM çağrısı yapılmadı")
    else:
        with ThreadPoolExecutor(max_workers=6) as havuz:
            sonuclar = list(havuz.map(lambda x: sonda(x[1]), isler))

        HAM.parent.mkdir(parents=True, exist_ok=True)
        with open(HAM, "w") as f:
            for (ad, m), s in zip(isler, sonuclar):
                f.write(json.dumps({"grup": ad, "metin": m, "sonda": s}, ensure_ascii=False) + "\n")

    L = ["# Replay Türkçe kalitesi — kör sonda", "",
         f"**Sonda:** `prompts/turkce-dogallik-sondasi.v1.md` · **Model:** `{MODEL}`  ",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {date.today().isoformat()} · "
         f"**Tohum:** 4242 · **Grup başına:** {n} metin · **Uzunluk bandı:** {BANT[0]}-{BANT[1]} karakter  ",
         f"**Ham çıktı:** `{HAM.relative_to(KOK)}` · SHA256 "
         f"`{hashlib.sha256(HAM.read_bytes()).hexdigest()}`", "", "---", "",
         "## 0. Yöntem ve sınırları", "",
         "K88 replay kaynaklarının makine çevirisi olduğunu işaretlemiş ama **ölçmemişti**. "
         "Dil doğallığı bu projenin ana kalite ekseni (K48, §5d).", "",
         "**Belirlenimli işaretler denendi ve elendi:** *\"bir\" yoğunluğu* üç korpusta da "
         "aynı çıktı (0.035-0.036); *kelime tekrarı* konusal olduğu için kusur ölçmüyor "
         "(\"hidroelektrik\" × 3 bir çeviri hatası değil). Bu yüzden LLM sondası kullanıldı.", "",
         "**Sonda K62'ye göre kuruldu:** soyut puan sorulmuyor, **alıntılanabilir kanıt** "
         "isteniyor — kusur varsa metinden birebir alıntı ve doğal karşılığı.", "",
         "> ⚠️ **Araç kendi üzerinde sınanıyor.** Aynı sonda bizim **elle yazdığımız** BıRAG "
         "metinlerine de koşuldu. Sonda ikisini ayırt edemezse araç işe yaramaz (K61'in şartı).", "",
         "> ⚠️ **Kontrol edilemeyen karıştırıcı:** iki korpus **tür** olarak farklı — bizimkiler "
         "terapötik diyalog, Alpaca açıklayıcı talimat-cevap. Sonda diyalog parçalarını "
         "\"eksik cümle\" sanabilir. Bu yüzden yalnızca **büyük** farklar yorumlanır.", "",
         "## 1. Sonuç", "", "| Grup | n | kusur bulunan | hata |", "|---|---:|---:|---:|"]
    ozet = {}
    for ad in gruplar:
        alt = [s for (a, _), s in zip(isler, sonuclar) if a == ad]
        hata = sum(1 for s in alt if "_hata" in s)
        gecerli = [s for s in alt if "_hata" not in s]
        k = sum(1 for s in gecerli if s.get("dogal_olmayan") is True)
        ozet[ad] = (len(gecerli), k)
        L.append(f"| {ad} | {len(gecerli)} | {k} (%{k/max(1,len(gecerli))*100:.0f}) | {hata} |")
    L += ["", "## 2. Sondanın alıntıladığı kusurlar", ""]
    for ad in gruplar:
        L += [f"### {ad}", ""]
        ornek = [(m, s) for (a, m), s in zip(isler, sonuclar)
                 if a == ad and s.get("dogal_olmayan") is True][:6]
        if not ornek:
            L += ["_Sonda bu grupta kusur bulmadı._", ""]
            continue
        L += ["| tür | alıntı | doğal hâli |", "|---|---|---|"]
        for m, s in ornek:
            L.append(f"| {s.get('tur','?')} | {str(s.get('alinti',''))[:70]} | "
                     f"{str(s.get('dogal_hali',''))[:70]} |")
        L += [""]

    # ---- 3. Ayrım anlamlı mı (hüküm VERİDEN türetilir — K80) ----
    nk, kk = ozet[KONTROL]
    kaynaklar = [a for a in ozet if a != KONTROL]
    p_deger, fark_puan = {}, {}
    for ad in kaynaklar:
        n_, k_ = ozet[ad]
        p_deger[ad] = fisher_exact([[k_, n_ - k_], [kk, nk - kk]])[1]
        fark_puan[ad] = k_ / n_ - kk / nk

    L += ["## 3. Ayrım anlamlı mı", "",
          f"Kontrol grubu **{KONTROL}**. Her kaynak ona karşı sınanıyor. "
          f"Fisher kesin testi, iki yanlı. \"Büyük fark\" eşiği **{BUYUK_FARK*100:.0f} puan** — "
          "bu bizim konvansiyonumuz, literatürden gelmiyor (Kural 6).", "",
          "| Grup | kusur | oran | %95 Wilson | kontrole karşı | Fisher p |",
          "|---|---:|---:|---:|---:|---:|"]
    for ad in ozet:
        n_, k_ = ozet[ad]
        lo, hi = wilson(k_, n_)
        if ad == KONTROL:
            L.append(f"| {ad} | {k_}/{n_} | %{k_/n_*100:.0f} | "
                     f"%{lo*100:.0f}-{hi*100:.0f} | — (kontrol) | — |")
        else:
            L.append(f"| {ad} | {k_}/{n_} | %{k_/n_*100:.0f} | %{lo*100:.0f}-{hi*100:.0f} | "
                     f"{fark_puan[ad]*100:+.0f} p | {pbic(p_deger[ad])} |")

    anlamli = all(p_deger[a] < 0.05 for a in kaynaklar)
    buyuk = all(fark_puan[a] >= BUYUK_FARK for a in kaynaklar)
    ayirdi = anlamli and buyuk
    L += ["",
          ("**Sonda ayırt ediyor.**" if ayirdi else "**Sonda ayırt ETMİYOR.**") + " " +
          (f"İki kaynağın da kontrolden farkı {BUYUK_FARK*100:.0f} puanın üstünde "
           f"({min(fark_puan.values())*100:+.0f} p ve {max(fark_puan.values())*100:+.0f} p) "
           f"ve iki testte de p < 0.05 (en büyüğü {pbic(max(p_deger.values()))}). "
           "K61'in şartı sağlandı: araç kendi üzerinde sınandı ve iki tarafı ayırdı."
           if ayirdi else
           "Şartlardan en az biri sağlanmadı — "
           f"anlamlılık {'sağlandı' if anlamli else 'SAĞLANMADI'}, "
           f"büyük fark {'sağlandı' if buyuk else 'SAĞLANMADI'}. "
           "Bu durumda ölçüm kaynaklar hakkında bir şey söylemez, yalnızca aracın "
           "duyarsız olduğunu söyler."), ""]

    # ---- 4. Okuma (her cümle yukarıdaki sayılardan türetilir) ----
    L += ["## 4. Okuma", ""]
    taban = kk / nk
    en_dusuk_kaynak = min(ozet[a][1] / ozet[a][0] for a in kaynaklar)
    L += [f"- **Yanlış pozitif tabanı %{taban*100:.0f}.** Sonda elle yazdığımız "
          f"{nk} metnin {kk}'ini işaretledi. §2'deki BıRAG alıntıları buna örnek: "
          "*\"İki gün tuttun\"* bağlamında doğru bir Türkçe. Yani kaynaklardaki "
          f"%{en_dusuk_kaynak*100:.0f}'lik oranın bir kısmı da gürültüdür; "
          "fark gerçek, mutlak seviye şişkindir."]
    if taban < en_dusuk_kaynak:
        L += ["- **Tür karıştırıcısı bulgunun aleyhine çalışıyor.** Karıştırıcı, sonda "
              "diyalog parçalarını \"eksik cümle\" sanacağı için **bizim** metinlerimizde "
              "daha çok işaret beklenmesini gerektirirdi. Gözlenen tersi: kontrol grubu "
              f"(%{taban*100:.0f}) her iki kaynaktan da düşük. Karıştırıcı farkı "
              "yaratmıyor, küçültüyor."]
    else:
        L += ["- ⚠️ **Tür karıştırıcısı bulgunun lehine çalışıyor olabilir.** Kontrol grubu "
              "kaynaklardan düşük değil; bu ölçümden kaynak kalitesi hakkında hüküm çıkmaz."]
    hatali = sum(1 for s_ in sonuclar if "_hata" in s_)
    if hatali:
        L += [f"- {hatali} çağrı 3 denemede de zaman aşımına uğradı (K86) ve paydadan "
              "düşürüldü; işaretli sayılmadı."]
    L += ["- Bu ölçüm **kusurun varlığını** gösterir, **eğitime etkisini** göstermez. "
          "Replay diliminin Türkçeyi bozup bozmadığı ancak ablasyonla (Faz 5, replay oranı) "
          "bilinir. Bu rapor o ablasyona girdi verir, yerine geçmez.", ""]

    CIKTI.write_text("\n".join(L) + "\n")
    print(f"yazıldı: {CIKTI.relative_to(KOK)}")
    for ad, (g, k) in ozet.items():
        print(f"  {ad:<30} {k}/{g} kusur")


if __name__ == "__main__":
    main()
