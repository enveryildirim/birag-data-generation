"""T168 kontrol deneyi — İKİNCİ TUR ögeleri (ZEYİL, üretimden ÖNCE).

⛔⛔ **Birinci tur kendi varsayımını çürüttü.** Ön kayıt ögelerin uzunluğu
hakkında hiçbir şey söylememişti ve koşu şunu gösterdi:

  · korpustaki kullanıcı turları **medyan 15 kelime** (ort. 20,7 · %25-75: 7-30)
  · birinci turun ögeleri **medyan 6 kelime** (ort. 7,1 · en uzun 15)

T168'in olgusu *«alıntı KISALTILIRKEN vurgu ögesi atılıyor»* ⇒ kısaltılacak bir
şey olmayan 6 kelimelik ögede olgu **oluşamaz**. Birinci turun null'ı bu yüzden
T168 hakkında bir kanıt değil, **tasarım hakkında** bir kanıttır.

⛔ İkinci kusur: `aslında`/`actually` ögeleri **cümle başındaydı** ⇒ model
alıntıya sonradan başlayınca hedef hizalanan aralığın dışında kalıyor ve ön
kayıt adım 3 gereği öge **sayılmıyor** (12 ögenin 12'si). Simetrik bir kusur,
ama hücreleri yarıya indiriyor.

⭐ **Zeyilde değişen YALNIZ öge kümesi.** Ölçüt, ölçüm adımları, sınama ve hüküm
kuralları birinci turun ön kaydından **aynen** gelir (T245: ilan düzeltilir ama
sonuca bakılarak değil, varsayım çürüdüğü için).

Çıktı: data/deney/2026-09-22-t168-ogeler-tur2.jsonl
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / "data" / "deney" / "2026-09-22-t168-ogeler-tur2.jsonl"

TR_KLITIK = [
    ("de", "Geçen hafta sonu kardeşimin düğünü vardı, herkes içiyordu ve ben masada sadece oturdum; kimse fark etmedi ama benim içim de bütün gece tuhaftı."),
    ("de", "Sabahları erken kalkıp işe gidiyorum, akşam eve dönünce de doğrudan yatağa gitmemeye çalışıyorum, çünkü boş saatler beni zorluyor."),
    ("da", "Doktor üç ayda bir kontrole gel dedi, ilaçları da aksatmamam gerektiğini söyledi ve ben ikisini yapmaya çalışıyorum ama unutuyorum."),
    ("da", "Eşim artık akşamları benimle konuşmuyor, çocuklar da odalarına kapanıyor; eve girdiğimde ev sessiz oluyor ve bu sessizlik bana ağır geliyor."),
    ("da", "İşten çıkarıldıktan sonra üç ay hiçbir şey yapmadım, param da bitti, şimdi başvuru yapıyorum ama geri dönen olmuyor."),
    ("de", "Arkadaşlarım eskiden her hafta arardı, ben de onları aramayı bıraktım; şimdi kimse aramıyor ve bunun bir kısmı benim suçum."),
    ("da", "O gün çok kötüydüm, ertesi sabah da yataktan kalkamadım, iki gün işe gitmedim ve kimseye neden olduğunu söyleyemedim."),
    ("de", "Bıraktığımı kimseye söylemedim, eşime de söylemedim; tek başıma tutmaya çalışıyorum çünkü söyleyip başaramazsam daha kötü olacak."),
    ("da", "Sabah yürüyüşe çıkmaya başladım, akşam da kısa bir tur atıyorum; yorulunca akşamları daha az düşünüyorum."),
    ("de", "Annem her aradığında aynı şeyi soruyor, abim de aynı şeyi söylüyor; ikisi iyi niyetli ama ben kendimi hesap veriyormuş gibi hissediyorum."),
    ("de", "Sigarayı bıraktım, kahveyi de azalttım çünkü ikisi birbirini tetikliyordu; şimdi sabahları elim boş kalıyor ve ne yapacağımı bilemiyorum."),
    ("da", "Uyuyamıyorum, iştahım da kapandı, gece boyunca tavana bakıyorum ve sabah olunca hiç dinlenmemiş gibi kalkıyorum."),
]

EN_KLITIK = [
    ("also", "Last weekend was my brother's wedding, everyone was drinking and I just sat at the table; nobody noticed, but I also felt strange inside all night."),
    ("also", "I get up early and go to work in the mornings, and when I come home in the evening I also try not to go straight to bed, because the empty hours are hard."),
    ("also", "The doctor said to come for a check-up every three months, and he also said I shouldn't skip my medication, and I try to do both but I forget."),
    ("also", "My wife doesn't talk to me in the evenings anymore, and the kids also shut themselves in their rooms; the house is silent when I walk in and that silence weighs on me."),
    ("also", "After I was laid off I did nothing for three months, and my money also ran out; now I'm applying but nobody gets back to me."),
    ("also", "My friends used to call every week, and I also stopped calling them; now nobody calls and part of that is my own fault."),
    ("also", "I was very bad that day, and the next morning I also couldn't get out of bed, I didn't go to work for two days and I couldn't tell anyone why."),
    ("also", "I didn't tell anyone I quit, and I also didn't tell my wife; I'm trying to hold it alone because if I say it and fail it will be worse."),
    ("also", "I started going for a walk in the morning, and in the evening I also take a short round; when I'm tired I think less at night."),
    ("also", "My mother asks the same thing every time she calls, and my brother also says the same thing; they both mean well but I feel like I'm giving an account of myself."),
    ("also", "I quit smoking, and I also cut down on coffee because the two triggered each other; now I don't know what to do in the mornings."),
    ("also", "I can't sleep, and my appetite is also gone, I stare at the ceiling all night and when morning comes I get up feeling like I never rested."),
]

TR_SERBEST = [
    ("biraz", "Bu hafta üç kez yürüyüşe çıktım ve bugün kendimi biraz daha iyi hissediyorum, ama bunun ne kadar süreceğini bilmediğim için güvenmiyorum."),
    ("aslında", "Eşim bana kızdığında susuyorum çünkü aslında haklı olduğunu biliyorum ve tartışırsam kendimi savunmak zorunda kalacağım."),
    ("biraz", "Toplantıdan sonra eve döndüm ve biraz rahatladım, orada oturup dinlemek bile beni yormuştu ama çıkarken içim hafiflemişti."),
    ("aslında", "Herkes bana kızgın olduğumu söylüyor ama aslında kimseye kızgın değilim, sadece çok yorgunum ve bunu anlatamıyorum."),
    ("biraz", "Gün içinde iyiyim, akşamları biraz huzursuz oluyorum ve o saatlerde ne yapacağımı bilemediğim için telefona sarılıyorum."),
    ("aslında", "Kimseye söylemedim ama aslında bu ilk denemem değil, dört yıl önce bırakmıştım ve sekiz ay sonra geri döndüm."),
    ("biraz", "Kardeşim geçen ay taşındı ve ailemle aram biraz düzeldi, en azından artık telefonu açıyorum ve konuşabiliyoruz."),
    ("aslında", "İnsanlar kalabalıkta rahat olduğumu sanıyor ama aslında yalnız kalmaktan korkuyorum ve bu yüzden gereksiz yere dışarıda kalıyorum."),
    ("biraz", "İlacı düzenli kullanmaya başladıktan sonra uyku düzenim biraz oturdu, artık gece ikide değil on birde yatabiliyorum."),
    ("aslında", "Danışmanla konuşmayı haftalardır erteliyorum çünkü aslında yardım istemeye utanıyorum, sanki bunu tek başıma beceremediğimi kabul etmiş olacağım."),
    ("biraz", "İki haftadır düzenli yemek yiyorum ve iştahım biraz açıldı, eskiden öğle yemeğini tamamen atlıyor ve akşama kadar bir şey yemiyordum."),
    ("aslında", "O gün gittim ama aslında gitmek istememiştim, eşim ısrar etti ve ben tartışmamak için arabaya bindim."),
]

EN_SERBEST = [
    ("a bit", "I went for a walk three times this week and today I feel a bit better, but I don't trust it because I don't know how long it will last."),
    ("actually", "When my wife gets angry at me I stay quiet because I actually know she's right, and if I argue I'll have to defend myself."),
    ("a bit", "I came home after the meeting and relaxed a bit; even sitting there listening had worn me out, but I felt lighter on the way out."),
    ("actually", "Everyone tells me I'm angry but I'm actually not angry at anyone, I'm just very tired and I can't explain it."),
    ("a bit", "I'm fine during the day, in the evenings I get a bit restless, and at those hours I don't know what to do so I cling to my phone."),
    ("actually", "I haven't told anyone, but this actually isn't my first attempt; I quit four years ago and came back eight months later."),
    ("a bit", "My brother moved out last month and things with my family got a bit better; at least I answer the phone now and we can talk."),
    ("actually", "People think I'm comfortable in crowds but I'm actually afraid of being alone, and that's why I stay out longer than I need to."),
    ("a bit", "After I started taking the medication regularly my sleep schedule settled a bit; I can go to bed at eleven now instead of two."),
    ("actually", "I keep putting off talking to the counsellor because I'm actually ashamed to ask for help, as if I'd be admitting I failed."),
    ("a bit", "I've been eating regularly for two weeks and my appetite opened up a bit; I used to skip lunch completely."),
    ("actually", "I went that day but I actually didn't want to go; my wife insisted and I got in the car to avoid an argument."),
]

HUCRELER = {
    "tr_klitik": ("tr", "klitik_benzeri", TR_KLITIK),
    "en_klitik": ("en", "klitik_benzeri", EN_KLITIK),
    "tr_serbest": ("tr", "serbest_belirtec", TR_SERBEST),
    "en_serbest": ("en", "serbest_belirtec", EN_SERBEST),
}

# ─── Kapılar: zeyilin ilan ettiği iki düzeltme SINANARAK uygulanır ─────────
TR_KLITIK_DESEN = re.compile(r"(?<!\w)(de|da)(?!\w)", re.IGNORECASE)
EN_KLITIK_DESEN = re.compile(r"(?<!\w)(too|also)(?!\w)", re.IGNORECASE)
TR_SERBEST_DESEN = re.compile(r"(?<!\w)(biraz|aslında)(?!\w)", re.IGNORECASE)
EN_SERBEST_DESEN = re.compile(r"(?<!\w)(a bit|actually)(?!\w)", re.IGNORECASE)


def main() -> None:
    satirlar, uzunluklar, hatalar = [], [], []
    for hucre, (dil, tur, ogeler) in HUCRELER.items():
        for i, (hedef, metin) in enumerate(ogeler, 1):
            oid = f"{hucre}-{i:02d}"
            kelime = len(metin.split())
            uzunluklar.append(kelime)

            # kapı 1: hedef metinde ve TAM OLARAK BİR KEZ
            adet = len(re.findall(rf"(?<!\w){re.escape(hedef)}(?!\w)", metin, re.IGNORECASE))
            if adet != 1:
                hatalar.append(f"{oid}: hedef '{hedef}' {adet} kez (1 olmalı)")

            # kapı 2: hedef CÜMLE BAŞINDA OLMAMALI (birinci turun kusuru)
            ilk = metin.split()[0].strip(",.;:").lower()
            if ilk == hedef.split()[0].lower():
                hatalar.append(f"{oid}: hedef cümle başında — tur 1 kusuru")

            # kapı 3: uzunluk korpus medyanına yakın olmalı (>= 15 kelime)
            if kelime < 15:
                hatalar.append(f"{oid}: {kelime} kelime (>= 15 olmalı)")

            # kapı 4: hücreler arası bulaşma yok
            if tur == "serbest_belirtec":
                desen = TR_KLITIK_DESEN if dil == "tr" else EN_KLITIK_DESEN
                if desen.search(metin):
                    hatalar.append(f"{oid}: serbest ögede KLİTİK bulaşması: {desen.search(metin).group(0)!r}")
            else:
                desen = TR_SERBEST_DESEN if dil == "tr" else EN_SERBEST_DESEN
                if desen.search(metin):
                    hatalar.append(f"{oid}: klitik ögede SERBEST bulaşması: {desen.search(metin).group(0)!r}")

            satirlar.append(
                json.dumps(
                    {"id": oid, "hucre": hucre, "dil": dil, "oge_turu": tur,
                     "hedef": hedef, "metin": metin},
                    ensure_ascii=False,
                )
            )

    if hatalar:
        print("⛔ KAPI AÇILMADI — öge kümesi yazılmadı:")
        for h in hatalar:
            print("   ", h)
        raise SystemExit(1)

    CIKTI.write_text("\n".join(satirlar) + "\n", encoding="utf-8")
    uzunluklar.sort()
    medyan = uzunluklar[len(uzunluklar) // 2]
    print(f"✅ dört kapı da geçti · {len(satirlar)} öge")
    print(f"   kelime: medyan {medyan} · en kısa {uzunluklar[0]} · en uzun {uzunluklar[-1]}")
    print(f"   (korpus medyanı 15 — tur 1 medyanı 6)")
    print(f"   {CIKTI.relative_to(KOK)} SHA256 {hashlib.sha256(CIKTI.read_bytes()).hexdigest()[:16]}")


if __name__ == "__main__":
    main()
