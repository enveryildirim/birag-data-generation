# -*- coding: utf-8 -*-
"""v0.1.1 — düşünme ↔ cevap uyuşmazlığı taraması (T300 §4 · karar #1).

⛔ Bu bir ELEK, hüküm değil. Yanlış olumlu da kaçırma da verir; işaretlediği
   kayıt elle okunur. Sayıları tezde kullanmadan önce bulgu profilini yaz.

Aradığı sınıf: düşünme, açıkladığı cevabı YANLIŞ anlatıyor. Faz boyunca elle
bulunan örnekler: #0729 (eksik) · #0833 (kendi turn_ending'iyle çelişik) ·
#0840 (abartıyor) · #0909 (cevabın yaptığını reddediyor) · #0971 (dar çelişki) ·
#0991 (cevabın varsayımını devralıyor). Hiçbir betik kapısı bu karşılaştırmayı
yapmıyor — bu betik onu sayılabilir hâle getirir.

⛔⛔ ÖLÇÜLEN HATA PROFİLİ (2026-09-29, 1039 kayıt) — sayı kullanmadan önce oku:

  A) «düşünme yönlendirme YOK diyor, cevapta var»  →  7 işaret, **7/7 YANLIŞ OLUMLU**
     Yedisi de aynı ayrımı yapıyor: *yeni* bir yer önermemekle, var olanı ya da
     cevabın kimde olduğunu adlandırmak ayrı şeyler (#0004 · #0050 · #0139 ·
     #0163 · #0257 · #0984 · #0998). ⇒ #0909 tipi gerçek çelişki **seyrek**,
     sistemik değil; ayrıca #0971'in dar okumayla çözülmesini korpus destekliyor.

  B) «cevapta var düşünmede yok»  →  58 işaret, 5 örnekte **2 gerçek** (#0648 ·
     #0363 yönlendirmeyi adıyla anmıyor), 3 sınırda (RAG kayıtlarında cevap
     bağlam belgesinin yordamını alıntılıyor, düşünme «metindeki cevabı
     veriyorum» diyerek genel sahipleniyor). Kaba tahmin: ~%40 gerçek.

  C) «cevap soruyla bitiyor, düşünmede soru hamlesi yok»  →  28 işaret.
     İlk sürüm 341 işaret vermişti ve örneklenen 4'ün 4'ü yanlış olumluydu
     (düşünme «Sorumu … yöneltiyorum» diyordu); ölçüt gevşetildi. Kalan
     işaretlerde hâlâ yanlış olumlu var (#0659 «Sorduğum şey …» — `\bsoru`
     kalıbı «sorduğum»u yakalamıyor). ⚠️ Ayrıca `\bsoru` kalıbı «sorun»
     sözcüğünü de eşliyor ⇒ bazı gerçek boşluklar **kaçırılıyor**; 28 bir
     ALT SINIR.

Koşum: uv run python scripts/analiz/2026-09-29-v011-dusunme-cevap.py
"""
import json, re, sys, glob, os
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from tohum_guvenlik import tr_fold

# Yönlendirme sözcükleri — cevapta bir yer/kurum/eylem çağrısı var mı?
YER = re.compile(r"(poliklinik|hastane|sağlık merkez|danışma|AMATEM|ALO ?171|acil servis|"
                 r"aile hekim|hekim|doktor|uzman|terapist|psikiyatr|avukat|müdürlüğ|başvur|randevu)", re.I)
# Düşünme «yönlendirme YOK» diyor mu?
YOK = re.compile(r"(yönlendirme (koymuyorum|yok)|yönlendirmiyorum|bir yere göndermiyorum|"
                 r"yer önermiyorum|yeni bir yer önermiyorum|kurum (adı )?vermiyorum|"
                 r"bir yer daha önermek)", re.I)

def kayitlar():
    for f in sorted(glob.glob(str(KOK / "data/candidates/v011-faz2-b*.jsonl"))) + \
             [str(KOK / "data/candidates/v011-pilot.jsonl")]:
        if not os.path.exists(f): continue
        blok = os.path.basename(f).replace("v011-faz2-b", "").replace(".jsonl", "")
        for ln in open(f, encoding="utf-8"):
            r = json.loads(ln)
            th = " ".join(m.get("thinking", "") or "" for m in r["messages"])
            cev = ""
            for m in r["messages"]:
                if m["role"] == "assistant": cev = m.get("content", "") or ""
            if th.strip() and cev.strip():
                yield blok, r["id"][:8], th, cev

def main():
    tot = 0; bulgu = []
    for blok, rid, th, cev in kayitlar():
        tot += 1
        tf, cf = tr_fold(th), tr_fold(cev)
        cev_yer = sorted({m.group(0) for m in YER.finditer(cev)})
        th_yer  = {tr_fold(m.group(0))[:5] for m in YER.finditer(th)}
        notlar = []
        # A) düşünme «yönlendirme yok» diyor ama cevap bir yer/eylem veriyor
        if YOK.search(th) and cev_yer:
            notlar.append(f"düşünme yönlendirme YOK diyor, cevapta var: {cev_yer[:4]}")
        # B) cevap yer adı veriyor, düşünmede hiçbiri yok
        eksik = [w for w in cev_yer if tr_fold(w)[:5] not in th_yer]
        if eksik and not notlar:
            notlar.append(f"cevapta var düşünmede yok: {eksik[:4]}")
        # C) bitiş uyuşmazlığı, iki yön
        soru_c = cev.rstrip().endswith("?")
        # ⚠️ Kalibrasyon: ilk sürüm yalnız «soruyorum» arıyordu ve 4/4 örnekte yanlış
        #    olumlu verdi (düşünme «Sorumu … yöneltiyorum» diyordu). Ölçüt gevşetildi:
        #    düşünme bir soru hamlesinden HİÇ söz etmiyor mu?
        soru_t = bool(re.search(r"\bsoru", tf))
        if soru_c and not soru_t: notlar.append("cevap soruyla bitiyor, düşünmede soru hamlesi yok")
        if not soru_c and re.search(r"soruyu .{0,30}(soruyorum|yöneltiyorum)", tf):
            notlar.append("düşünme soru sorduğunu söylüyor, cevap soruyla bitmiyor")
        if notlar: bulgu.append((blok, rid, notlar))
    print(f"taranan kayıt: {tot}")
    print(f"işaretlenen  : {len(bulgu)}  (%{100*len(bulgu)/tot:.1f})\n")
    say = {}
    for blok, rid, notlar in bulgu:
        for n in notlar: say[n.split(":")[0]] = say.get(n.split(":")[0], 0) + 1
    for k, v in sorted(say.items(), key=lambda x: -x[1]): print(f"{v:4d}  {k}")
    print()
    for blok, rid, notlar in bulgu:
        print(f"b{blok:>5} {rid} | " + " ; ".join(notlar))

if __name__ == "__main__":
    main()
