#!/usr/bin/env python3
"""`v6-parti3…6`: `profil` ve `evre` etiketleri kaydı tarif ediyor mu?

⛔⛔ **T220'NİN AÇIK BIRAKTIĞI KARŞILAŞTIRMA.** T220 parti1'i ölçtü ve iki
eksende kırıldığını buldu: `profil` %25 doğrulanabilir (59 kaydın 44'ünde
metin sessiz), `evre`'de 13 kayıt (%22) etiketle çelişiyor. Ama şerhinde
şu yazıyordu: *«karşılaştırma yok ⇒ bu sayılar «parti1 kötü» demiyor,
«parti1 ölçülemiyor» diyor»*. ⭐ Ve bir **test edilebilir tahmin**
bırakmıştı: `profil`'in sessizliği REJİMDEN BAĞIMSIZ çıkacak (meslek kısa
bir konuşmada nadiren geçer), `evre`'nin çelişkisi ise parti1'e ÖZGÜ
çıkacak (parti3-6'da metin tohumdan geliyor). Bu betik o tahmini sınıyor.

⭐ **ÖLÇEK VE YÖNTEM T220'NİNKİYLE AYNI (K97):** üç değerli okuma
(`U` uyumlu · `Ç` çelişiyor · `S` sessiz), hepsi elle (K30). 237 kayıt ×
2 eksen = 474 hüküm.

⛔ Okuma kapısı: hükmü olmayan kayıt kalırsa rapor yazılmaz.

Çıktı: reports/analiz/2026-09-21-parti3-6-profil-evre-uyumu.{md,json}
"""
from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-parti3-6-profil-evre-uyumu.md"
JSON = KOK / f"reports/analiz/{TARIH}-parti3-6-profil-evre-uyumu.json"
EKSEN = ["profil", "evre"]
# ⭐ parti1'in sayıları T220'den; burada yeniden hesaplanmıyor (K97).
# ⛔⛔⛔ T220'nin ÜÇÜNCÜ okuması (T224 sonrası): parti1'in künyesi onarıldıktan
# sonra DOĞRU tohumlara karşı yeniden okundu. İlk iki okuma (22 ve 14 çelişki)
# yanlış tohumları ölçüyordu ve geçersizdir.
PARTI1 = {"profil": {"U": 15, "S": 43, "Ç": 1}, "evre": {"U": 28, "S": 26, "Ç": 5}}

# ⛔ ELLE VERİLEN HÜKÜM (K30) — sıra: profil, evre.
HUKUM: dict[str, dict[int, str]] = {
 "v6-parti3": {
  1:"UU",  2:"UU",  3:"US",  4:"UU",  5:"UU",  6:"SU",  7:"SS",  8:"SU",  9:"UU", 10:"SS",
 11:"SU", 12:"UÇ", 13:"SU", 14:"US", 15:"SU", 16:"UU", 17:"SS", 18:"UU", 19:"SU", 20:"UU",
 21:"SU", 22:"UÇ", 23:"UU", 24:"SS", 25:"UU", 26:"SU", 27:"SÇ", 28:"SU", 29:"SU", 30:"SU",
 31:"SS", 32:"UU", 33:"SÇ", 34:"UU", 35:"SU", 36:"SU", 37:"UU", 38:"UU", 39:"UU", 40:"UU",
 41:"UU", 42:"UU", 43:"SU", 44:"SS", 45:"UÇ", 46:"UÇ", 47:"SU", 48:"SS", 49:"UU", 50:"UU",
 51:"US", 52:"UU", 53:"SU", 54:"SU", 55:"SS", 56:"SÇ", 57:"SU", 58:"UU", 59:"SU", 60:"UU"},
 "v6-parti4": {
  1:"SS",  2:"SÇ",  3:"SU",  4:"SU",  5:"SU",  6:"SS",  7:"SU",  8:"SU",  9:"SU", 10:"SU",
 11:"UU", 12:"US", 13:"UU", 14:"US", 15:"SU", 17:"UU", 18:"UU", 19:"UU", 20:"SU", 21:"UU",
 22:"UU", 23:"SS", 24:"SU", 25:"SU", 26:"SS", 27:"UU", 28:"SU", 29:"SU", 30:"UU", 31:"SU",
 32:"SU", 33:"UU", 34:"SU", 35:"SS", 36:"SS", 37:"UU", 38:"US", 39:"SS", 40:"SS", 41:"SU",
 42:"SS", 43:"SU", 44:"SS", 45:"UU", 46:"SU", 47:"US", 48:"SU", 49:"SU", 50:"UU", 51:"SS",
 52:"SU", 53:"UU", 54:"US", 55:"SU", 56:"SU", 57:"UU", 58:"SS", 59:"SU", 60:"SU"},
 "v6-parti5": {
  1:"UU",  2:"SU",  3:"SU",  4:"SU",  5:"SU",  6:"SU",  7:"SU",  8:"SU",  9:"SS", 10:"UU",
 11:"UU", 12:"SU", 13:"US", 14:"UU", 15:"UU", 16:"SÇ", 17:"SU", 18:"UÇ", 19:"SU", 20:"SU",
 21:"SU", 22:"SS", 23:"UU", 24:"SU", 25:"SU", 26:"UU", 27:"UU", 28:"UÇ", 29:"UU", 30:"SU",
 31:"UU", 32:"SU", 33:"UÇ", 34:"UU", 35:"ÇS", 36:"UU", 37:"SU", 38:"US", 39:"SU", 40:"SU",
 41:"UU", 42:"UU", 43:"UU", 44:"SU", 45:"ÇS", 46:"UU", 47:"SS", 48:"SU", 49:"UU", 50:"US",
 51:"UU", 52:"SU", 53:"SÇ", 54:"SS", 55:"UU", 56:"UU", 57:"SU", 58:"SU", 59:"UU", 60:"UU"},
 "v6-parti6": {
  1:"UU",  3:"UU",  4:"SU",  5:"SS",  6:"UU",  7:"UU",  8:"UU",  9:"US", 10:"SU", 11:"UU",
 12:"UU", 13:"UU", 14:"SU", 15:"SS", 16:"US", 17:"SU", 18:"SS", 19:"SÇ", 20:"SU", 21:"UÇ",
 22:"SU", 23:"SU", 24:"UU", 25:"US", 26:"US", 27:"SU", 28:"SU", 29:"SS", 30:"UÇ", 31:"SU",
 32:"UU", 33:"US", 34:"UU", 35:"SÇ", 37:"SS", 38:"UU", 39:"SÇ", 40:"US", 41:"SÇ", 42:"UU",
 43:"UÇ", 44:"SS", 45:"SU", 46:"UU", 47:"UU", 48:"UU", 49:"SS", 50:"UU", 51:"US", 52:"UU",
 53:"SU", 54:"US", 55:"US", 56:"SÇ", 57:"UÇ", 58:"UU", 59:"SU", 60:"SÇ"},
}


# ⛔ ÇELİŞKİLERİN GEREKÇESİ — T220'de yazılmıştı, bu raporun ilk hâlinde
#    yoktu ve şerhinde *«denetlenebilirlik parti1'inkinden DÜŞÜK»* diye
#    yazılıydı. Yazıldı. ⭐⭐ Yazmak SAYIYI DEĞİŞTİRDİ: 28 çelişkinin 5'i
#    gerekçelendirilemedi ve geri alındı (aşağıda `GERI_ALINAN`).
GEREKCE: dict[str, str] = {
 "v6-parti3#12": "`inkar`; metin *«çok mu sık alıyorum acaba»* diye SORUYOR — "
                 "inkârın tersi",
 "v6-parti3#22": "`nuksetme`; metinde kırılan bir ayıklık dönemi yok, iki günlük "
                 "yeni bir kullanım var",
 "v6-parti3#27": "`dibe_vurma`; metin ilk grup katılımını ve markete girip "
                 "içmeden çıkmayı anlatıyor — bu bir çaba",
 "v6-parti3#33": "`tolerans`; metin her ay temiz çıkan testleri anlatıyor, "
                 "artan kullanımı değil",
 "v6-parti3#45": "`sosyal_kullanim`; metin *«tek başıma uğruyorum»* diyor ve "
                 "sıklığın arttığını söylüyor",
 "v6-parti3#46": "`birakma_cabasi`; metin dozu KENDİ artırdığını söylüyor",
 "v6-parti3#56": "`tolerans`; metin silme–yeniden indirme döngüsünü anlatıyor, "
                 "artan kullanımı değil",
 "v6-parti4#2": "`tolerans`; metin içmediği bir akşamı ve *«aklımdan bile "
                "geçmedi»*yi anlatıyor",
 "v6-parti5#16": "`merak_deneme`; metinde grubun danıştığı yerleşik bir kimlik "
                 "var, deneme yok",
 "v6-parti5#18": "`birakma_cabasi`; metin iki hafta önce BAŞLAYAN bir eklemeyi "
                 "ve *«kendime dur diyemiyorum»*u anlatıyor",
 "v6-parti5#28": "`merak_deneme`; metinde oturmuş bir *«sistem»* ve ücretli bir "
                 "grup var",
 "v6-parti5#33": "`birakma_cabasi`; metin yazılandan fazlasını aldığını söylüyor",
 "v6-parti5#53": "`dibe_vurma`; metin süren (ve denetimsiz) bir bırakma "
                 "girişimini ve *«başaracağım galiba»*yı anlatıyor",
 "v6-parti6#19": "`merak_deneme`; metinde üç haftalık düzenli oyun ve kaybı "
                 "kapatma planı var",
 "v6-parti6#21": "`nuksetme`; metin *«dönemde böyle bir şey yaşamamıştım»* diyor "
                 "— kırılan bir ayıklık değil, yeni bir tırmanış",
 "v6-parti6#30": "`dibe_vurma`; metin azalmayı ve düzelen aile ilişkisini "
                 "anlatıyor, kelimeyi de kendisi veriyor: *«nüks»*",
 "v6-parti6#35": "`tolerans`; metin üç günlük aradan sonraki kaymayı anlatıyor",
 "v6-parti6#39": "`nuksetme`; metin yarından itibaren bırakma KARARINI anlatıyor",
 "v6-parti6#41": "`merak_deneme`; metin aylık aidatlı bir aboneliği *«yatırım»* "
                 "diye kuruyor",
 "v6-parti6#43": "`merak_deneme`; metin her sınav döneminde tekrarlanan bir "
                 "kullanımı anlatıyor",
 "v6-parti6#56": "`nuksetme`; metin azaltılmış ama SÜREN bir kullanımı anlatıyor, "
                 "geri dönüşü değil",
 "v6-parti6#57": "`birakma_cabasi`; metin *«üç aydır geri döndüm»* diyor",
 "v6-parti6#60": "`nuksetme`; metin hâlâ ayık olduğunu söylüyor — bu bir "
                 "nüks değil, bir istek gecesi",
}

# ⭐⭐ GERİ ALINAN — gerekçesi yazılamayan çelişkiler. Bunlar bir kusur değil,
#    bu raporun ölçüsü: *yazılmamış bir hüküm, dayanıksız bir hükümdür.*
GERI_ALINAN: dict[str, str] = {
 "v6-parti3#43": "Ç → **U**. Metin *«kendime kapı aralamak istemiştim, ama "
                 "içimden gelmedi»* diyor: gerekçeyi arayıp KULLANMAMIŞ. "
                 "`birakma_cabasi` bunu tarif ediyor. Kısaltılmış dökümde son "
                 "cümleyi görmemiştim.",
 "v6-parti4#9": "Ç → **U**. Metinde *«hafta içi sekizleri görüyorum zaten, üç "
                "bira hiçbir şey»* var — bu doğrudan bir TOLERANS ifadesi. "
                "Cumartesi girişimine takılıp etiketin karşılığını "
                "atlamışım.",
 "v6-parti4#47": "Ç → **S**. Metinde bırakma girişimi YOK ama girişimle "
                 "ÇELİŞEN bir şey de yok; yalnızca sessiz. Yokluğu çelişki "
                 "saymışım.",
 "v6-parti5#54": "Ç → **S**. Etiket ilacın dozuyla ilgili; metin şarabı "
                 "bırakmakla ilgili. Farklı şeylerden söz ediyorlar, "
                 "çelişmiyorlar.",
 "v6-parti6#40": "Ç → **S**. Metinde kullanım hiç yok — kutuya bakmak var. "
                 "Bir evreyi çürütmek için önce bir evre görünmeli.",
}


def main() -> int:
    say = {p: {e: collections.Counter() for e in EKSEN} for p in HUKUM}
    hata = []
    for parti, h in HUKUM.items():
        kdos = KOK / f"data/candidates/{parti}.jsonl"
        siralar = sorted(json.loads(l)["gen_meta"]["parti_sira"]
                         for l in kdos.read_text(encoding="utf-8").splitlines() if l.strip())
        eksik = [s for s in siralar if s not in h]
        fazla = [s for s in h if s not in siralar]
        bozuk = [s for s, v in h.items() if len(v) != 2 or set(v) - set("UÇS")]
        if eksik or fazla or bozuk:
            hata.append(f"{parti}: eksik {eksik} · fazla {fazla} · bozuk {bozuk}")
        for s in siralar:
            if s in h:
                for e, v in zip(EKSEN, h[s]):
                    say[parti][e][v] += 1
    if hata:
        print("⛔ OKUMA KAPISI REDDETTİ — rapor yazılmadı:")
        for x in hata:
            print("   " + x)
        return 1

    top = {e: collections.Counter() for e in EKSEN}
    for parti in HUKUM:
        for e in EKSEN:
            top[e] += say[parti][e]
    n = sum(sum(say[p][EKSEN[0]].values()) for p in HUKUM)
    JSON.write_text(json.dumps({"tarih": TARIH, "n": n, "hukum": HUKUM},
                               ensure_ascii=False, indent=1), encoding="utf-8")

    sat = ["# `v6-parti3…6`: `profil` ve `evre` etiketleri kaydı tarif ediyor mu?", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Girdi:** " + " · ".join(
               f"`{p}` `{hashlib.sha256((KOK/f'data/candidates/{p}.jsonl').read_bytes()).hexdigest()[:8]}`"
               for p in HUKUM) + f" · **{n}** kayıt  ",
           f"**Ölçek:** T220'nin ölçeği, aynen — `U` uyumlu · `Ç` çelişiyor · "
           f"`S` sessiz; {n}×2 = **{n*2}** hüküm, hepsi elle (K30)", "",
           "⛔⛔ T220 parti1'i ölçmüş ve bir **tahmin** bırakmıştı: `profil`'in "
           "sessizliği rejimden BAĞIMSIZ, `evre`'nin çelişkisi parti1'e ÖZGÜ "
           "olacak. Bu rapor o tahmini sınıyor.", "",
           "## 0. ⭐⭐⭐ Tahmin sınandı", "",
           "| eksen | parti1 | parti3-6 | tahmin | sonuç |", "|---|---|---|---|---|"]
    p1p, p1e = PARTI1["profil"], PARTI1["evre"]
    n1 = sum(p1p.values())
    pp, pe = top["profil"], top["evre"]
    sat += [f"| `profil` sessiz | %{100*p1p['S']/n1:.0f} | **%{100*pp['S']/n:.0f}** | "
            "rejimden **bağımsız** | ◐ **YARI** — düştü ama iki rejimde de çoğunluk |",
            f"| `evre` çelişen | %{100*p1e['Ç']/n1:.0f} | **%{100*pe['Ç']/n:.0f}** | "
            "parti1'e **özgü** | ⛔ **ÇÜRÜDÜ** — fark neredeyse yok |", "",
            "⛔⛔⛔ **`evre` TAHMİNİ ÇÜRÜDÜ — VE BUNU GÖRMEK İKİ DÜZELTME "
            "GEREKTİRDİ.** İlk karşılaştırma %22 ↔ %12 diyordu ve farkı rejime "
            "yoruyordu. (1) `Ç`/`S` sınırı iki raporda farklı uygulanmıştı; ilan "
            "edilince parti1 %14'e indi (T222). (2) Sonra parti1'in künyesinin "
            "bozuk olduğu ortaya çıktı (T224): ölçüm **yanlış tohumlara** karşı "
            "yapılmıştı. Künye onarılıp doğru tohumlarla yeniden okununca "
            f"karşılaştırma **%{100*p1e['Ç']/n1:.0f} ↔ %{100*pe['Ç']/n:.0f}** "
            "oldu — parti1 artık **daha iyi**. ⇒ `evre` çelişkisi parti1'e özgü "
            "değil; her partide var ve rejimle hiç ilgisi yok. ➡️⭐⭐⭐ *Bir "
            "karşılaştırmanın iki yanı da aynı ölçekle VE aynı veriyle "
            "kurulmalıdır; ben ikisini de ayrı ayrı kaçırdım ve her seferinde "
            "farkı bir OLGUYA yordum.*", "",
            f"⭐ **`profil` tahmini ise kısmen tuttu:** sessizlik "
            f"%{100*p1p['S']/n1:.0f} → %{100*pp['S']/n:.0f}. Rejim sayıyor ama "
            "sessizlik iki rejimde de çoğunluk.", "",
            f"⭐ **Asıl bulgu `profil`'de ve tahminden bağımsız:** kayıtların "
            f"%{100*pp['S']/n:.0f}'inde — metin tohumdan gelirken bile — kişinin "
            "mesleki profili hakkında hiçbir şey söylenmiyor. Çünkü tohumun "
            "kendi metni de çoğu zaman söylemiyor: kısa bir konuşmada meslek "
            "geçmiyor. ⇒ `profil` ekseni korpusun bir özelliğini değil, tohum "
            "dosyasının bir alanını ölçüyor ve bu **bütün partiler** için "
            "geçerli.", "",
           "## 1. Parti parti", "",
           "| parti | kayıt | `profil` U/S/Ç | `evre` U/S/Ç | `profil` doğrulanabilir | `evre` çelişen |",
           "|---|---:|---|---|---:|---:|"]
    for parti in HUKUM:
        c1, c2 = say[parti]["profil"], say[parti]["evre"]
        m = sum(c1.values())
        sat.append(f"| `{parti}` | {m} | {c1['U']}/{c1['S']}/{c1['Ç']} | "
                   f"{c2['U']}/{c2['S']}/{c2['Ç']} | %{100*(c1['U']+c1['Ç'])/m:.0f} | "
                   f"**%{100*c2['Ç']/m:.0f}** |")
    sat.append(f"| **parti1** *(T220)* | {n1} | {p1p['U']}/{p1p['S']}/{p1p['Ç']} | "
               f"{p1e['U']}/{p1e['S']}/{p1e['Ç']} | %{100*(p1p['U']+p1p['Ç'])/n1:.0f} | "
               f"**%{100*p1e['Ç']/n1:.0f}** |")
    sat += ["", "## 2. ⛔ Bunun kapsama ölçümüne anlamı", "",
            f"Kapsama envanteri `profil` eksenini de hedefliyor. Ölçülen şu: **{n+n1} "
            f"v6 kaydının {pp['S']+p1p['S']}'inde** (%"
            f"{100*(pp['S']+p1p['S'])/(n+n1):.0f}) metin, kişinin mesleki profili "
            "hakkında hiçbir şey söylemiyor. ⇒ T211'in beş partide kapanmayan "
            "`profil=mavi_yakali` açığı, korpusta **görünmeyen** bir eksende "
            "ölçülüyordu; o açığı kapatmak korpusun içeriğini değil tohum "
            "seçimini değiştirir.", "",
            "## 3. ⛔ Çelişen etiketler — gerekçeleriyle", "",
            f"⭐⭐ **Gerekçeleri yazmak sayıyı değiştirdi.** Bu raporun ilk hâli "
            f"{pe['Ç'] + len(GERI_ALINAN)} çelişki saymıştı ve şerhinde "
            "*«gerekçeler tek tek yazılmadı, denetlenebilirlik T220'ninkinden "
            f"düşük»* yazıyordu. Yazılınca **{len(GERI_ALINAN)}'i "
            f"gerekçelendirilemedi ve geri alındı**; sayı {pe['Ç']}'e indi. "
            "➡️⭐⭐⭐ *Yazılmamış bir hüküm dayanıksız bir hükümdür: gerekçe "
            "yazmak bir biçim işi değil, hükmün kendisini sınayan adımdır — ve "
            f"burada hükümlerin **%{100*len(GERI_ALINAN)/(pe['Ç']+len(GERI_ALINAN)):.0f}"
            "**'i sınavı geçemedi.*", "",
            "| # | gerekçe |", "|---|---|"]
    for k, v in GEREKCE.items():
        sat.append(f"| `{k}` | {v} |")
    sat += ["", "### ⭐ Geri alınan hükümler", "", "| # | düzeltme |", "|---|---|"]
    for k, v in GERI_ALINAN.items():
        sat.append(f"| `{k}` | {v} |")
    eksik_g = [f"{p}#{s_}" for p, h in HUKUM.items() for s_ in h
               if h[s_][1] == "Ç" and f"{p}#{s_}" not in GEREKCE]
    if eksik_g:
        print(f"⛔ Gerekçesi yazılmamış çelişki: {eksik_g}")
        return 1
    sat += ["", "## 4. Satır satır hüküm", ""]
    for parti, h in HUKUM.items():
        sat += [f"**`{parti}`** — sıra: `profil``evre`", "",
                "| " + " | ".join(f"{s}" for s in sorted(h)) + " |",
                "|" + "---|" * len(h),
                "| " + " | ".join(h[s] for s in sorted(h)) + " |", ""]
    sat += ["## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Hüküm BENİM okumam** (K30) | ve bu partilerin kayıtlarını da "
            "ben yazdım ⇒ kendi metnimi kendi etiketime karşı okuyorum; ikinci "
            "anotatör yok |",
            f"| ⭐ **Gerekçeler YAZILDI ve {len(GERI_ALINAN)} hüküm geri alındı** | "
            "bu şerh ilk hâlde bir eksiklik olarak duruyordu; kapatıldı. ⛔ Ama "
            "geri alınanların hepsini de ben buldum: bir hükmü sınayan yine "
            "hükmü veren kişi (K30) |",
            "| ⛔ **Diğer yedi eksen ölçülmedi** | yalnız `profil` ve `evre`; "
            "`risk_seviyesi`, `siddet_seviyesi`, `motivasyon_evresi` yine ölçülmedi "
            "(derece okumak eşiği benim koymam olurdu, `gd-024`) |",
            "| ⛔⛔ **Düzeltme yapılmadı** | ne etiketler değişti ne kayıtlar |",
            "| ⚠️ **`diger` profili çürütülemez** | metin onunla çelişemez; bu "
            "değerdeki kayıtlar yapısal olarak `S` alıyor |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print(f"✅ {n} kayıt × 2 eksen")
    for e in EKSEN:
        c = top[e]
        print(f"   {e:8s} U {c['U']:3d} · S {c['S']:3d} · Ç {c['Ç']:3d}  "
              f"(parti1: U {PARTI1[e]['U']} · S {PARTI1[e]['S']} · Ç {PARTI1[e]['Ç']})")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
