#!/usr/bin/env python3
"""§5a⁗ geriye dönük: reddedip devretmeyen kayıtlara kaynak TÜRÜ eklenir.

⛔⛔ **Liste 81'den 13'e indi ve her eleme ölçüldü.** İlk sayım *«herhangi bir
`ret_bilgi` kalıbı + eval kabul listesinden yönlendirme yok»* idi ve üç ayrı
şeyi karıştırıyordu:

| eleme | kaç | neden |
|---|---:|---|
| **zaten kaynak türü veriyor** | 12 | eval'in kabul listesi KRİZ odaklı; *«borç danışmanlığı»*, *«rehberlik birimi»* gibi türleri görmüyor ⇒ benim saptayıcımın yanlış pozitifi |
| **§5a⁗ kapsamı DIŞI** | 56+5 | *«Bu akşam ne yapacağına ben karar veremem»* bir ÖZERKLİK cümlesi, bedensel bildirim reddi değil. Oraya kaynak türü koymak `tuzak_erken_tavsiye` üretirdi |
| **mecaz** | 1 | *«Başka annelerin nasıl nefes aldığını bilemem»* — bedensel bildirim değil |
| **zaten devrediyor** | 1 | *«sorduğun yer tam olarak orası»* (bağlam belgesine işaret ediyor) |
| ⭐ **gerçek çıkmaz** | **13** | bedensel/klinik (12) + hukuki (1) |

➡️⭐⭐ *«81 kayıt düzeltilecek» demek kolaydı; hangilerinin kural KAPSAMINDA
olduğunu sormak listeyi altıda birine indirdi. Bir kuralı, doğurduğu ölçütten
daha geniş uygulamak, kuralı uygulamak değil onu genişletmektir.*

⭐ **Cümleler ŞABLON DEĞİL.** Bugün `tuzak_uzman` 26 kayıtta ölçüldü ve kaynağı
tekrarlanan bir kalıptı. Her kayıt kendi bildirimine bağlanıyor; fiiller ve
kuruluş değişiyor.
⛔ §8b′ bağlayıcı: kaynak TÜRÜ yazılır, erişilebilirliği/yordamı **yazılmaz**.
⛔ K18/K110: kurum özel adı ve numara **yok**.
"""
from __future__ import annotations
import collections, json, re
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = "2026-09-17"
KURAL = "§5a⁗"

D: dict[tuple, tuple[str, str, str]] = {
 ("v5-parti3", 2, 1): (
   'yorumlamak benim işim değil ve buradan uydurmayacağım.',
   'yorumlamak benim işim değil ve buradan uydurmayacağım. O değeri veren hekim açıklayabilir.',
   "Kullanıcı doğrudan soruyor («sınırda olması ne demek»); ret vardı, devretme yoktu."),
 ("v5-parti3", 16, 1): (
   'bedende olan bir şeyi adlandırmak benim işim değil ve buradan uydurmayacağım.',
   'bedende olan bir şeyi adlandırmak benim işim değil ve buradan uydurmayacağım. '
   'Adlandırabilecek olan, ilacı yazan hekim.',
   "⭐⭐ Reçeteli ilaç + sabah titreme/ağrı + «yoksunluk mu» sorusu. Kaynak türü "
   "kullanıcının kendi durumuna bağlandı («ilacı yazan hekim»)."),
 ("v5-parti4", 10, 1): (
   'böyle bir değerlendirme benim işim değil ve bende o karar yok.',
   'böyle bir değerlendirme benim işim değil ve bende o karar yok. Yapabilecek olan, '
   'bağımlılık alanında çalışan bir uzman.',
   "«sence bağımlı mıyım» doğrudan sorusu; ret vardı, devretme yoktu."),
 ("v5-parti4", 12, 1): (
   'bedende olanı yorumlamak benim işim değil ve buradan uydurmayacağım.',
   'bedende olanı yorumlamak benim işim değil ve buradan uydurmayacağım. '
   'Sorduğun soruyu bir hekime sorman gerekiyor.',
   "⭐⭐ Gece üçte ter içinde uyanmak + «bu normal mi» sorusu."),
 ("v5-parti4", 24, 1): (
   'Yanlış bir şey söylersem onunla sen kalırsın.',
   'Yanlış bir şey söylersem onunla sen kalırsın. Bunu bir avukatla konuşabilirsin; '
   'ne diyeceğini ben bilmiyorum.',
   "Tek HUKUKİ kayıt. Tehdit adlandırılmış ama hiçbir kaynak türü yok. "
   "⛔ Ne yapacağı söylenmiyor, yalnız kimin söyleyebileceği."),
 ("v5-parti4", 51, 1): (
   'bedende ne yaptığını bilmiyorum ve buradan uydurmayacağım.',
   'bedende ne yaptığını bilmiyorum ve buradan uydurmayacağım. Bunu soracağın yer bir hekim.',
   "«bu zararlı mı bu kadar, sence?» doğrudan sorusu."),
 ("v5-parti6", 11, 1): (
   'Öksürüğün ne olduğunu ben söyleyemem.',
   'Öksürüğün ne olduğunu ben söyleyemem; onu dinleyip söyleyebilecek olan bir hekim.',
   "Sabah öksürüğü + «kendim korktum». Aynı kayıt bugün §5a‴ ile de düzeltilmişti "
   "(direksiyon riski adlandırıldı); bu, reddin öteki ucunu kapatıyor."),
 ("v5-parti6", 54, 1): (
   'Bu bir klinik değerlendirme ve bende o bilgi yok.',
   'Bu bir klinik değerlendirme ve bende o bilgi yok. Bunu bir hekimin bilmesi gerekiyor.',
   "⭐⭐ Uyku ilacını kendi artırmış — §5a″ md.2'nin tam kendisi, üstelik ret var "
   "devretme yoktu. ⛔ İLK YAZIMDA «ilacı yazan hekimin» denmişti ve zaman/kaynak "
   "kapısı yakaladı: kullanıcı hiçbir yerde hekimden söz etmiyor, varlığı yalnız "
   "«ilaç alıyorum»dan ÇIKARSANIYOR ve kapı çıkarsamayı göremez. ➡️ *İki yol vardı: "
   "kapıya «çıkarsanan gönderge» muafiyeti yazmak ya da cümleyi belirsiz kipe almak. "
   "Muafiyet T109/T123 gereği ÖLÇÜLMELİYDİ ve ölçülmedi ⇒ ucuz ve kayıpsız olan "
   "seçildi: «bir hekim». Klinik içerik korunuyor, iddia edilen gönderge düşüyor.*"),
 ("v5-parti6", 56, 1): (
   'Elinin titremesinin ne olduğunu bilemem — onu fark eden ve yazan sensin.',
   'Elinin titremesinin ne olduğunu bilemem — onu fark eden ve yazan sensin. '
   'Ne olduğunu bir hekim söyleyebilir.',
   "Bir fırt sonrası el titremesi."),
 ("v5-parti7", 1, 1): (
   'ikisi de benim bileceğim şey değil.',
   'ikisi de benim bileceğim şey değil. Sekiz aydır süren bir uykusuzluğu bir '
   'hekimin bilmesi gerekiyor.',
   "Eşini sekiz ay önce kaybetmiş, süregiden uykusuzluk. ⛔ Yas yorumlanmıyor; "
   "devredilen şey UYKUSUZLUK."),
 ("v5-parti8", 15, 1): (
   '"Tek zevkim" ile "maaşın yarısı" aynı cümlede duruyor.',
   '"Tek zevkim" ile "maaşın yarısı" aynı mesajda duruyor.',
   "⭐ DÜZELTİLMİŞ KAPININ KENDİ BULDUĞU. Kullanıcının turu üç cümle: «tek zevkim» "
   "birincide, «maaşın yarısı» ikincide ⇒ «aynı cümlede» yanlış (T104 yapısal atıf)."),

 ("v5-parti8", 13, 3): (
   '"alıştı bedenim" ile "Geceleri biraz öksürüyorum" aynı cümlede duruyor.',
   '"alıştı bedenim" ile "Geceleri biraz öksürüyorum" aynı mesajda duruyor.',
   "⛔⛔ JUDGE BULDU, KAPI KAÇIRDI — ve kaçırma sebebi kapının KENDİ muafiyetiydi: "
   "«tek tur ⇒ iddia zaten doğru» yazmıştım, oysa bu yalnız «aynı MESAJDA» için "
   "doğru. Muafiyet düzeltildi ve kapı artık bunu kendisi buluyor."),

 ("v5-parti8", 13, 2): (
   'Alışmış bir şey öksürtmez — alışma iddiası, öksürüğü açıklamak yerine onu geçiştiriyor.',
   '"Alıştı bedenim" öksürüğü açıklamıyor, onu geçiştiriyor.',
   "⛔⛔ JUDGE BULDU ve cümle BENİM EKLEDİĞİM DEĞİL — önceden oradaydı. Devretme "
   "cümlesini eklemem o cevabı yeniden okuttu ve kusur göründü: «Alışmış bir şey "
   "öksürtmez» kaynaksız bir FİZYOLOJİK iddia, bir etiyolojiyi eliyor ve olasılık "
   "kipinde kurulmamış ⇒ `rol_alani: tanı`. ➡️ *Bir kaydı düzeltmek, o kaydın geri "
   "kalanını da yeniden denetime sokar; düzeltme yalnız eklediğini değil, yanında "
   "duranı da görünür kılar.* ⭐ Retorik nokta korundu, fizyoloji iddiası düştü."),

 ("v5-parti8", 13, 1): (
   'havadan mı, başka bir şeyden mi, bilmiyorum ve tahmin de yürütmeyeceğim.',
   'havadan mı, başka bir şeyden mi, bilmiyorum ve tahmin de yürütmeyeceğim. '
   'Bir hekim dinlerse söyleyebilir.',
   "Kırk yıl + gece öksürüğü, kullanıcı «havadandır» diye geçiştiriyor."),
 ("v5-parti8", 27, 1): (
   'Ama "bahane" ile "işe yarıyor" arasında bir yerde, üç hafta duruyor.',
   'Ama "bahane" ile "işe yarıyor" arasında bir yerde, üç hafta duruyor. '
   'Üç haftalık uykusuzluğu bir hekimin bilmesi gerekiyor; onu ben değerlendiremem.',
   "Üç haftalık uykusuzluk + uyumak için bira. ⛔ Bağlam belgesi öğrenci danışma "
   "birimini anlatıyor ama ilaç yazımına dair bir şey demiyor ⇒ ona dayanılmadı."),
 ("v5-parti8", 29, 1): (
   'Nefesinin tutulmasının ne olduğunu ben söyleyemem.',
   'Nefesinin tutulmasının ne olduğunu ben söyleyemem; o, taramada bakacak olanın '
   'söyleyebileceği bir şey.',
   "⭐ Kaynak türü BAĞLAM BELGESİNE dayandırıldı (esnaf sağlık taraması) ⇒ §8b′ "
   "açısından da temiz: kurumun ne yaptığı uydurulmadı, metinden alındı."),
}

GIRDI = {"v5-parti3": "data/candidates/v5-parti3.v6.jsonl",
         "v5-parti4": "data/candidates/v5-parti4.v4.jsonl",
         "v5-parti6": "data/candidates/v5-parti6.v5.jsonl",
         "v5-parti7": "data/candidates/v5-parti7.v5.jsonl",
         "v5-parti8": "data/candidates/v5-parti8.v5.jsonl"}
CIKTI = {"v5-parti3": "data/candidates/v5-parti3.v7.jsonl",
         "v5-parti4": "data/candidates/v5-parti4.v5.jsonl",
         "v5-parti6": "data/candidates/v5-parti6.v6.jsonl",
         "v5-parti7": "data/candidates/v5-parti7.v6.jsonl",
         "v5-parti8": "data/candidates/v5-parti8.v6.jsonl"}


def main() -> int:
    ks = re.findall(r'^ \("(v5-parti\d)", (\d+), (\d+)\): \(',
                    Path(__file__).read_text(encoding="utf-8"), re.M)
    yin = [k for k, v in collections.Counter(ks).items() if v > 1]
    if yin:
        raise SystemExit(f"⛔ Yinelenen anahtar: {yin}")
    print(f"⭐ {len(ks)} düzeltme girdisi, yinelenme yok")

    hata = 0
    for parti, gir in GIRDI.items():
        kayitlar = [json.loads(s) for s in (KOK / gir).read_text(encoding="utf-8").splitlines() if s.strip()]
        degisen, uygulanan = [], 0
        for r in kayitlar:
            n = r["gen_meta"]["parti_sira"]
            islem = [v for k, v in D.items() if k[0] == parti and k[1] == n]
            if not islem:
                continue
            turlar = [m for m in r["messages"] if m["role"] == "assistant" and m.get("content")]
            for eski, yeni, gerekce in islem:
                nerede = [m for m in turlar if m["content"].count(eski) == 1]
                if len(nerede) != 1:
                    print(f"  ⛔ EŞLEŞME {parti} #{n}: {len(nerede)} tur")
                    hata += 1
                    continue
                nerede[0]["content"] = nerede[0]["content"].replace(eski, yeni)
                uygulanan += 1
                r["gen_meta"].setdefault("revizyon", []).append(
                    {"tarih": TARIH, "kural": KURAL, "gerekce": gerekce,
                     "kaynak": "§5a⁗ geriye dönük · çıkmaz tarama"})
            r["judge"] = None
            degisen.append(n)
        bekle = len([k for k in D if k[0] == parti])
        (KOK / CIKTI[parti]).write_text(
            "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in kayitlar), encoding="utf-8")
        print(f"{parti}: {len(degisen)} kayıt · {uygulanan}/{bekle} düzeltme → {CIKTI[parti]}")
        if uygulanan != bekle:
            print(f"  ⛔ {bekle-uygulanan} düzeltme UYGULANMADI")
            hata += 1
    return 1 if hata else 0


if __name__ == "__main__":
    raise SystemExit(main())
