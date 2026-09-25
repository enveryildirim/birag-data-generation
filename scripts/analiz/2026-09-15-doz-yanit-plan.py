#!/usr/bin/env python3
"""T30 DOZ-YANIT EĞRİSİ — tasarım ızgarası ve düzeltme ölçütü (üretimden ÖNCE yazılı).

Neden var
---------
T30 negatif bir sonuç kaydetti: yönlendirme hamlesini korpusa %3,2 dozunda geri
koymak refleksi geri getirmedi. İki açıklama AYIRT EDİLMEDİ:
  (a) doz yetersiz   (b) ilişki yapısal olarak asimetrik
Ayıracak tek deney doz-yanıt eğrisidir. Şu an iki nokta ölçülü: %0 ve %3,6.
Bu betik ~%10 ve ~%25 noktalarının tasarımını sabitler.

⛔ TASARIM KARARI — NEDEN KORPUS BÜYÜTÜLMÜYOR
---------------------------------------------
K113'ün kontrol kolu şunu ölçtü: A-dar/v0.0.2/280 → 2 · A-dar/v0.0.3/280 → 2 ·
A-dar/v0.0.3/372 → 4. Yani ADIM SAYISI metriği veriden daha çok oynattı.
Korpus büyürse §9'un 3-epoch kuralı adımı da büyütür ve eğri okunamaz hale gelir.
Bu yüzden N SABİT: 155 kayıt (137 terapötik + 18 replay), üç doz noktasında da aynı.
Replay payı da sabit (%11,6) — Eksen 3'ün ikinci değişkeni dondurulmuş olur.

⭐ MANİPÜLASYON: EŞLEŞTİRİLMİŞ EKLEME (matched insert), silme YOK
-----------------------------------------------------------------
Var olan bir kaydın kullanıcı turları, thinking'i ve cevabının TAMAMI aynen kalır;
cevabın İÇİNE tek bir yönlendirme cümlesi eklenir. Böylece üç doz noktası arasındaki
metin farkı YALNIZCA eklenen cümlelerdir.

Bunun ölçüm açısından kritik sonucu: sınır çekme metninin korpustaki maruziyeti
ÜÇ DOZDA DA BİREBİR AYNI (20 kayıt, aynı cümleler). Değişen tek şey, o sınırın
ardından bir ADIM gösterilip gösterilmediği — T29'un ayrımı tam olarak budur.
`sinir_tipi` etiketi `sinir_cekme` → `rol_siniri_yonlendirme` olarak değişir; bu bir
defter kaydıdır, korpustan silinen davranış değildir.

Değişmezler (makineyle denetlenir, `2026-09-15-doz-yanit-derleme.py`):
  I1  Kayıt sayısı, id'ler, kullanıcı mesajları, context, source_ids: BİREBİR aynı.
  I2  Eklenen cümle çıkarılınca cevap orijinaliyle BAYT BAYT aynı olmalı.
  I3  Orijinal cevabın SON cümlesi yeni cevabın da son cümlesidir (§5a `turn_ending`
      korunur; yönlendirme tur sonu değildir — §8b).
  I4  Eklenen cümlede soru işareti YOK → `soru_sayisi ≤ 1` kapısı hiç oynamaz,
      `yansitma_soru_orani` yalnızca iyileşir.
  I5  Rakam yok, kurum özel adı yok, yordam yok (K18 / §8b ölçüt 3).
  I6  %10 kümesi %25 kümesinin ALT KÜMESİ (iç içe) → eğri yapıca monoton.

UYGUNLUK ÖLÇÜTÜ (seçimden önce yazılı, sonradan gevşetilmez — T24)
------------------------------------------------------------------
Bir kayda yönlendirme cümlesi EKLENEBİLİR ancak ve ancak:
  U1  Kullanıcı, adı konmuş bir meslek alanına (tıbbi · hukuki · ruh sağlığı) giren
      bir şey ortaya koymuş olmalı; VEYA açıkça destek almayı sormuş olmalı.
  U2  Mevcut cevap yönlendirme hamlesini ZATEN yapmıyor olmalı.
  U3  Kayıt `yonlendirme_gereksiz` olmamalı (karşı kutup korunur — §8b).
  U4  Kullanıcı yönlendirmeyi AÇIKÇA reddetmemiş olmalı (ısrar yasağı, K1/K21).
  U5  Kullanıcı hâlihazırda o bakımın içinde olmamalı VE gösterilecek bir adım
      kalmamış olmamalı (yoksa yönlendirme gereksiz tekrar olur).
  U6  RAG kaydı olmamalı — yönlendirme bilgisi pasajdan gelirse model davranışı
      ölçülemez (§7a grounding; envanterin `baglam_siniri` sınıfı).
  U7  `is_crisis` false (Kural 3 — bu dilim kriz dilimi DEĞİL, §8b).

DÜZELTME ÖLÇÜTÜ (T24 — üretimden önce yazılı)
----------------------------------------------
  D1  Her eklenen cümle kaynağın TÜRÜNÜ adlandırır ve bir ADIM gösterir;
      «orası hekimin işi» eklemesi SAYILMAZ (T29 ayrımı).
  D2  Hiçbir eklemede rakam, kurum özel adı ya da yordam (sıra/süre/ücret/randevu) yok.
  D3  Hiçbir eklemede emredici kip yok (§H.6); özerklik korunur (§5a, K1, K21).
  D4  I1-I6 değişmezlerinin hepsi makineyle geçer.
  D5  Sayım envanter betiğinin AYNI ayrımını kullanır ve sonuç ELLE okunur.
Tutmazsa ekleme yeniden yazılır; «yaklaşık tuttu» yoktur.
"""
from __future__ import annotations

import json
from pathlib import Path

KOK = Path(__file__).parent.parent.parent
KAYNAK = KOK / "datasets/v0.0.3/train.jsonl"
CIKTI = KOK / "data/plan/doz-yanit-ekler.jsonl"

# v0.0.3'te yönlendirme hamlesini ZATEN taşıyan kayıtlar — dokunulmaz (U2).
# ⚠️ Son iki satır bu ÜRETİM SIRASINDA bulundu: K110'un «yönlendirme 0» sayısı dar
# terim listesinden geliyordu ve HUKUKİ yönlendirmeyi görmüyordu. Ölçüm ve düzeltme:
# scripts/analiz/2026-09-15-yonlendirme-genis-tarama.py
#   v0.0.2: 0 → 2 (%2,0) · v0.0.3: 5 → 7 (%5,1). TIBBİ eksende v0.0.2 gerçekten 0.
MEVCUT = {
    "df75bf642d48904e": "yonlendirme_istegi",       # tıbbi, v4 partisi
    "3625b64e70cbfad9": "yonlendirme_istegi",       # tıbbi, v4 partisi
    "33ec128826ffc390": "rol_siniri_yonlendirme",   # tıbbi, v4 partisi
    "0012779f72357fda": "rol_siniri_yonlendirme",   # tıbbi, v4 partisi
    "5784119fc5c8b0a3": "rol_siniri_yonlendirme",   # tıbbi, v4 partisi
    "b4e29adf258c173d": "rol_siniri_yonlendirme",   # HUKUKİ — «bir avukata sorman gerekir»
    "ac1d50c5a31fd3b6": "rol_siniri_yonlendirme",   # HUKUKİ — RAG kaydı, hamle modelin
}
# Karşı kutup — ASLA yönlendirme eklenmez (§8b, U3).
KORUNAN = {"6d8d53ba416255ef", "dc39aded229ea7b8"}

# ─── EKLEME IZGARASI ───────────────────────────────────────────────────────────
# doz: bu kaydın hangi korpustan itibaren yönlendirme taşıyacağı (10 → hem %10 hem
# %25'te; 25 → yalnızca %25'te). havuz: `sinir` = envanterin sinir_cekme kaydı
# (§H.3'ün üçüncü adımı eksik), `ek` = meslek alanına giren ama envanterde terim
# geçmediği için sayılmamış kayıt.
IZGARA: list[tuple[str, int, str, str, str]] = [
    # ── %10 korpusunda da yönlendirme taşıyanlar (9 kayıt) ────────────────────
    ("802a014fe91ebbc2", 10, "sinir", "rol_siniri_yonlendirme", "ilacın kesilip kesilmeyeceği — kanonik rol sınırı, cevap sınırı çekip duruyor"),
    ("049c62fa00f632d6", 10, "sinir", "rol_siniri_yonlendirme", "«devam et / kes» kararı; karar sahibi adlandırılmış, adım gösterilmemiş"),
    ("d1f87cc0222d652a", 10, "sinir", "rol_siniri_yonlendirme", "«bedeninde ne zaman ne değişir» — tıbbi seyir sorusu, hekime ait"),
    ("115aa036d383a1bf", 10, "sinir", "rol_siniri_yonlendirme", "⭐ thinking'i ZATEN «önce empati, sonra sınır, sonra yönlendirme» diyor — havuzun en güçlü kaydı"),
    ("dc5a22d008dee048", 10, "sinir", "rol_siniri_yonlendirme", "kızının raporu — üçüncü kişi hakkında tıbbi yorum istemi"),
    ("f3c15ff6bcfe53ac", 10, "ek",    "rol_siniri_yonlendirme", "kayınvalidesinin reçeteli ilacını kullanıyor — başkasının reçetesi, tıbbi alan"),
    ("96df24c1ba532186", 10, "ek",    "rol_siniri_yonlendirme", "«oğlum ilaçlarıma baktı, fazla dedi» — doz sorusu, hekimin alanı"),
    # ── yalnızca %25 korpusunda yönlendirme taşıyanlar (20 kayıt) ─────────────
    ("f79f465788374149", 25, "sinir", "rol_siniri_yonlendirme", "«bu soru bir hekime ya da eczacıya sorulur» — envanter «sınırda» demişti; adım yok"),
    ("aaa1c9a0ba4f4435", 25, "sinir", "rol_siniri_yonlendirme", "tahlil yorumu — hekimin"),
    ("afeb9133c01e8f71", 25, "sinir", "rol_siniri_yonlendirme", "ilacın azaltılma programı — hekimin planı"),
    ("ba6b849b8b77ef88", 25, "sinir", "rol_siniri_yonlendirme", "baş dönmesi + öksürük — bedensel belirti"),
    ("4a8af1467106bc53", 25, "sinir", "rol_siniri_yonlendirme", "emzirirken ilaç etkisi — hekim ve eczacının alanı"),
    ("528b1123cbeb14ae", 25, "sinir", "rol_siniri_yonlendirme", "hekime gitmenin işi karıştıracağı korkusu — engel adlandırılmış, adım yok"),
    ("69776ab9b10c60fc", 25, "sinir", "rol_siniri_yonlendirme", "«ilacı alıp almamak hekiminle senin aranda» — üçüncü adım eksik"),
    ("7a2be624a947e7c8", 25, "sinir", "rol_siniri_yonlendirme", "çocukluk öyküsünün ne olduğu — tanı alanı"),
    ("fdc6e5d25da7cd24", 25, "sinir", "rol_siniri_yonlendirme", "hekimine söylemediği kısım — konuşulacak yer belli, adım yok"),
    ("53b008b252a59816", 25, "sinir", "rol_siniri_yonlendirme", "hekimle ne paylaşacağı — karar kullanıcının, adım gösterilebilir"),
    ("dec0afd13a3f0325", 25, "sinir", "rol_siniri_yonlendirme", "öksürük — bedensel belirti"),
    ("44cd5dddffa56418", 25, "sinir", "rol_siniri_yonlendirme", "«uyku için ne yapmam lazım» + program istemi — uyku hekimin bakabileceği şey"),
    ("f9550f5bce7b9ca4", 25, "ek",    "rol_siniri_yonlendirme", "raporlu izinde ne kadarının paylaşılmak ZORUNDA olduğu hukuki bir soru"),
    ("4b31c887aa3a3ed0", 25, "ek",    "rol_siniri_yonlendirme", "gizli, artan hap kullanımı — miktarın anlamı hekimin alanı"),
    ("b1b92fd913b34c28", 25, "ek",    "rol_siniri_yonlendirme", "uyku için kadeh, bir parmaktan ikiye çıkmış — uyku ve artan miktar tıbbi alan"),
    ("8c735882349fdc1f", 25, "ek",    "rol_siniri_yonlendirme", "sahte faturayla açık kapatma — hukuki alan"),
    ("631dccc638aaefb8", 25, "ek",    "rol_siniri_yonlendirme", "borç yapılandırma — hukuki/finansal danışmanlık alanı"),
    ("c3e09721ddbdcfbb", 25, "ek",    "rol_siniri_yonlendirme", "«bir tane artık yetmiyor» — reçeteli ilaçta artan tolerans, hekimin alanı"),
    ("e9c273a5ad251288", 25, "ek",    "rol_siniri_yonlendirme", "kullanıcı «bu da mı tolerans» diye AÇIKÇA soruyor ve cevap o soruya hiç değmiyor"),
]

# ─── ELENEN ADAYLAR (Kural 7: reddedilen seçenek de yazılır) ──────────────────
# Havuz taranırken uygun görünüp ELLE OKUNDUKTAN SONRA elenenler. Hepsi U1-U7'den
# birine takıldı; hiçbiri «yer kalmadı» diye elenmedi.
REDDEDILEN: dict[str, str] = {
    "bc00cda8f2a3f527": "U4 — kullanıcı «toplantıyı atlatmam lazım, sonrası ne olursa olsun» "
                        "diyor; son turda yönlendirme onun söylediğini duymamak olurdu",
    "677c665a6a49efca": "U5 — randevu iki gün sonra ZATEN var ve cevap o görüşmede kurulacak "
                        "cümleyi çalıştırıyor; gösterilecek yeni adım kalmamış",
    "9c44c1c5a5356b18": "U1 — açık bir meslek alanı sorusu yok; kullanıcı temiz, gerginliği "
                        "takip edilme hâlinden ve cevap bunu zaten adlandırmış",
    "cc534c25729cd257": "U4 — kullanıcı açılışta «'içme, bırak, doktora git' diyeceksen "
                        "yazmayayım» diyor; kanonik ısrar yasağı (K1/K21)",
    "5aff31c47af295c6": "U5 — poliklinik bandı kullanıyor ve aile hekimi takip ediyor",
    "6ddd6243c411d412": "U5 — bugün AMATEM'e gitmiş, randevusu var",
    "71fbd6ebf33e27f3": "U5 — ailesi danışmana götürmüş, süreç işliyor",
    "e4f2b26cc9c14f46": "U5 — terapisti var; cuma randevusu duruyor",
    "d0755679742fbd66": "U2/U5 — kaynağı kullanıcı kendisi bulmuş (GA toplantısı); model "
                        "yansıtırsa `kullanici_andi` olur, yönlendirme hamlesi değil",
    "ac1d50c5a31fd3b6": "U6 — RAG; yönlendirme bilgisi pasajdan gelir",
    "ba8bf2c8f096b14d": "U6 — RAG",
    "bb1e78418db0c741": "U6 — RAG",
    "b4e29adf258c173d": "U2 — ÜRETİM SIRASINDA bulundu: «Onu denetimli serbestlik "
                        "müdürlüğüne ya da bir avukata sorman gerekir» ZATEN yönlendirme; "
                        "MEVCUT'a taşındı, geniş tarama betiğine bakınız",
    "ac1d50c5a31fd3b6": "U2 + U6 — «Onu bir avukata sorman gerekir»; RAG kaydı ama hamle "
                        "modelin, MEVCUT'a taşındı",
    "5d24f424239fa0ad": "⛔ kaydın KENDİ thinking'i «Doktora gitmesini söylemiyorum — emir "
                        "kipi burada savunmayı sertleştirir ve zaten babasının gitmemesini "
                        "örnek olarak getirmiş» diyor; ekleme kaydı kendi gerekçesiyle "
                        "çelişkiye düşürürdü (U4)",
    "719823508e124d2a": "⛔ kaydın KENDİ thinking'i «Burada yönlendirme yapmıyorum, çünkü "
                        "zaten hekimiyle görüşüyor ve soruyu oraya itmek şu an konuştuğumuz "
                        "şeyi kapatır» diyor (U4 + U5)",
    "dfe09cffbbceaca9": "U5 — YEDAM'a gitmiş, randevusunu almış; envanterin `kullanici_andi` kaydı",
    "3e3d9f077adab11a": "U1 — kumar borcu ve annesinin parası; ortada adı konmuş bir meslek "
                        "alanı YOK, «bir danışmana» demek tam da karşı kutbun hatası olurdu",
    "755804e9730da6f4": "U1 — «çocuk büyürken doğru mu» bir değer sorusu, meslek alanı değil",
    "2756c055521fa06c": "⛔ kaydın KENDİ thinking'i «AMATEM'i kendisi söyledi. Ben üstüne "
                        "basıp 'git' dersem hem söylediğini duymamış olurum hem de bir hafta "
                        "boyunca gitmemesinin bir sebebi olduğunu atlarım» diyor (U4)",
    "f37585290d3ee12d": "U1 + U5 — açık bir meslek alanı sorusu yok (tur tamamen yalnızlık "
                        "üzerine) ve zaten denetimli serbestlik + YEDAM sürecinin içinde; "
                        "hukuki bir cümle burada konuyla ilgisiz düşerdi",
    "db79f39504283e3b": "⚠️ kayıp kovalama anı; yönlendirme savunulabilir ama kriz çerçevesine "
                        "yaklaşıyor — Kural 3 sınırında, elenmesi bilinçli",
}

# Yönlendirme taşıyan kayıt sayısı (137 terapötikte). ⚠️ ÜST NOKTA %25 DEĞİL %24,1:
# uygunluk ölçütü (U1-U7) uygulanınca havuzdan 26 kayıt çıktı, 27 değil. Sayıyı
# tutturmak için 27.'yi zorlamak, ölçütü sonradan gevşetmek olurdu (T24). Elenenlerin
# hepsi gerekçesiyle REDDEDILEN tablosunda; üçü kaydın KENDİ thinking'i yönlendirmeyi
# bilerek yapmadığını yazdığı için elendi.
HEDEF = {10: 14, 25: 33}


def main() -> None:
    T = [json.loads(l) for l in KAYNAK.open()]
    ter = [r for r in T if not r.get("replay")]
    kisa = {r["id"][:16]: r for r in ter}
    hata: list[str] = []

    ids = [g[0] for g in IZGARA]
    if len(set(ids)) != len(ids):
        hata.append("ızgarada tekrar eden id var")
    for i in ids:
        if i not in kisa:
            hata.append(f"{i}: v0.0.3 terapötik kümesinde yok")
        if i in MEVCUT:
            hata.append(f"{i}: zaten yönlendirme taşıyor (U2)")
        if i in KORUNAN:
            hata.append(f"{i}: yonlendirme_gereksiz — karşı kutup korunur (U3)")
        if i in REDDEDILEN:
            hata.append(f"{i}: elenmiş aday ızgaraya girmiş — {REDDEDILEN[i]}")
    for i in ids:
        r = kisa.get(i)
        if r is None:
            continue
        if r["slice"].startswith("rag"):
            hata.append(f"{i}: RAG kaydı — U6")
        if r.get("is_crisis"):
            hata.append(f"{i}: is_crisis — U7, Kural 3")

    n10 = sum(1 for g in IZGARA if g[1] == 10)
    n25 = len(IZGARA)
    if len(MEVCUT) + n10 != HEDEF[10]:
        hata.append(f"%10 hedefi tutmuyor: {len(MEVCUT)}+{n10} != {HEDEF[10]}")
    if len(MEVCUT) + n25 != HEDEF[25]:
        hata.append(f"üst nokta tutmuyor: {len(MEVCUT)}+{n25} != {HEDEF[25]}")

    if hata:
        raise SystemExit("⛔ ızgara geçersiz:\n" + "\n".join(f"  - {h}" for h in hata))

    with CIKTI.open("w", encoding="utf-8") as f:
        for kid, doz, havuz, tip, ger in IZGARA:
            r = kisa[kid]
            f.write(json.dumps({
                "id_16": kid, "id": r["id"], "doz": doz, "havuz": havuz,
                "sinir_tipi": tip, "gerekce": ger,
                "senaryo": r["scenario"], "dilim": r["slice"],
                "bagimlilik": r["addiction_type"], "yas": r["age_group"],
                "is_negative": r["is_negative"], "turn_type": r["turn_type"],
            }, ensure_ascii=False) + "\n")

    n = len(ter)
    print(f"kaynak: {KAYNAK.relative_to(KOK)} · terapötik {n} · replay {len(T)-n}")
    print(f"v0.0.3  yönlendirme {len(MEVCUT):>2}/{n} = %{100*len(MEVCUT)/n:.1f}  (ölçülü nokta)")
    print(f"v0.0.4  yönlendirme {len(MEVCUT)+n10:>2}/{n} = %{100*(len(MEVCUT)+n10)/n:.1f}  (+{n10} ekleme)")
    print(f"v0.0.5  yönlendirme {len(MEVCUT)+n25:>2}/{n} = %{100*(len(MEVCUT)+n25)/n:.1f}  (+{n25} ekleme)"
          f"   ⚠️ hedef ~%25 idi; ölçüt zorlanmadı")
    print(f"\nelenen aday: {len(REDDEDILEN)} (hepsi gerekçeli, REDDEDILEN tablosu)")
    n10_, n25_ = sum(1 for g in IZGARA if g[1] == 10), len(IZGARA)
    for etiket, alt in ((f"%10 ({n10_})", [g for g in IZGARA if g[1] == 10]),
                        (f"%25 ({n25_})", IZGARA)):
        hav = {h: sum(1 for g in alt if g[2] == h) for h in ("sinir", "ek")}
        bag = {}
        for g in alt:
            b = kisa[g[0]]["addiction_type"]
            bag[b] = bag.get(b, 0) + 1
        cok = sum(1 for g in alt if kisa[g[0]]["turn_type"] != "single")
        neg = sum(1 for g in alt if kisa[g[0]]["is_negative"])
        print(f"\n{etiket:9} havuz={hav} · çok-tur={cok} · is_negative={neg}\n"
              f"{'':9} bağımlılık={dict(sorted(bag.items(), key=lambda x: -x[1]))}")
    print(f"\nyazıldı: {CIKTI.relative_to(KOK)}")


if __name__ == "__main__":
    main()
