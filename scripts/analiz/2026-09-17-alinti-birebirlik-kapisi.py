#!/usr/bin/env python3
"""Cevap metnindeki TIRNAKLI dizgeler kullanıcının turlarında BİREBİR var mı.

⛔⛔ **Neden var.** T112: v5-parti5'in cevap metninde 22 tırnaklı alıntı kaynakta
bulunamadı; elle okunduğunda **8'i gerçek kusur** çıktı ve yedisi aynı biçimde
bozuktu — tırnak içinde **kelime eleme**: *«tutmadıysa ARTIK tutma sırası
gelmiştir»* → *«tutmadıysa tutma sırası gelmiştir»*. Sekizincisi doğrudan
T104'tü: `bicim` bandına sığsın diye KIRPILAN bir soru, cevapta alıntılanmaya
devam ediyordu.

⭐⭐ **Ayrım şu ve T105'in tam karşı kutbu.** T105 yansıtmanın dizgeyi
DEĞİŞTİRMEK ZORUNDA olduğunu ölçmüştü (*«eşim»* → *«eşin»*). Burada tersi
geçerli: değiştirmek serbest, ama **tırnak içinde** değiştirmek birebir olmayanı
birebir diye sunmaktır. ➡️ *Aynı kusur ailesinin iki üyesi için kural ters
yönde işliyor; bu yüzden iki ayrı kapı gerekiyor ve biri ötekinin yerine
geçemiyor.*

⭐ **Karşı olgusal alıntı muaf** — *«"Babana söylemelisin" demiyorum»* — çünkü
orada tırnak bir iddia değil, bir REDDİN nesnesi.

⛔⛔ **MUAFİYETİ ÖNCE YANLIŞ KORPUSTA ÖLÇTÜM VE MÜKEMMEL GÖRÜNDÜ.** İlk ölçüm
kusurların ZATEN DÜZELTİLDİĞİ korpusta yapıldı; orada kusurlu dizgeler artık yok
olduğu için her işaret *«kusurda 0»* verdi ve *«değil»* gibi Türkçenin en sık
sözcüklerinden biri ayırt edici göründü. Kusurlu hâl yeniden kurulup ölçüldüğünde
*«değil»* **5 meşru / 2 kusur**, *«demem»* **1/1** çıktı ⇒ ikisi de ATILDI.
➡️⭐ *Bir muafiyetin ayırt ediciliği, kusurların KALDIRILDIĞI korpusta ölçülemez —
orada her muafiyet kusursuz görünür. Ölçüm bilinen kusurlu hâl üzerinde yapılmalı
ve o hâl yoksa yeniden kurulmalıdır.*

⭐ **Güç (2026-09-17, bilinen kusurlu/temiz çift):** elle okunup KUSUR sayılan
11 ögenin **11'i de** yakalanıyor, iki korpusta da yanlış pozitif **0**.
⛔⛔ **AMA BU SAYI KANIT DEĞİL:** kapı tam olarak bu 22 öge üzerinde kuruldu;
kendi kurulum kümesinde mükemmel çıkması beklenen şeydir, genelleme kanıtı
değildir. Gerçek sınama, kapının kurulumunda KULLANILMAMIŞ partilerde ne
bulduğudur.

⛔ **Bu kapının ölçmediği:** `thinking` alanı KAPSAM DIŞI. Orada tırnakların
neredeyse tamamı karşı olgusal (168 alıntının 114'ü) ve alan bu denetim için
düşük bilgi taşıyor — dahil edilirse sayı gürültüye boğulur.

Kullanım: uv run python scripts/analiz/2026-09-17-alinti-birebirlik-kapisi.py <kayitlar.jsonl>
"""
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
sys.path.insert(0, str(KOK / "scripts/analiz"))
import _muafiyet as MUAF  # noqa: E402  ⭐ T140: bağışlanan her öge sayılır
from tohum_guvenlik import tr_fold  # noqa: E402

# ⛔⛔ TIRNAK EŞLEŞTİRİCİSİ SESSİZCE BOZUKTU (2026-09-17, muafiyet denetimi buldu).
# Eski desen `"([^"]{3,120})"` idi: uzunluk süzgeci EŞLEMENİN İÇİNDEYDİ. Bir alıntı
# kısa olduğu için (*«az»*, 2 harf) elendiğinde tarama onun KAPANIŞ tırnağını bir
# SONRAKİNİN AÇILIŞI sanıyor ve o cevaptaki bütün alıntılar kayıyordu.
# `v5-parti8 #12`'de gerçek alıntı *«Yastığın o tarafı boş»* hiç sınanmadı; onun
# yerine iki alıntı arasındaki *«. Bunu söyleyebilecek olan …»* metni sınandı.
# ⚠️ Sayı küçük (714 cevabın 4'ü) ama kusurun TÜRÜ ağır: görünmez YANLIŞ NEGATİF —
# kaçan alıntılar tam da §5a'nın *«ne "az" ne "çok"»* cümleleriydi.
# ➡️⭐ *Bir süzgeç, eşlemenin İÇİNE konursa eşlemeyi bozar. Önce eşleştir, sonra ele.*
_KISA = 3            # ⚠️ bu sınırın altındaki alıntılar sınanmaz ama SAYILIR


def _alintilar(c: str) -> list[str]:
    """Tırnakları SIRAYLA eşler (1-2, 3-4 …); uzunluk süzgeci eşlemeden SONRA."""
    yer = [m.start() for m in re.finditer(r'"', c)]
    ciftler = [(yer[i], yer[i + 1]) for i in range(0, len(yer) - 1, 2)]
    ciftler += [(m.start(), m.end() - 1) for m in re.finditer(r"«[^»]*»", c)]
    return sorted(ciftler)
SINIR = ".", "\n", "?", "!"

# ⛔ PENCERE İKİ KEZ YANLIŞ ÇİZİLDİ, ikisi de ölçümle bulundu:
#  1. 60 KARAKTERLİK pencere KOMŞU CÜMLEDEN muafiyet sızdırıyordu — bir önceki
#     cümlenin meşru karşı olgusalı (*«… bulunmayacağım»*) yanındaki uydurma
#     alıntıyı akladı. ⇒ Pencere alıntının KENDİ CÜMLESİ.
#  2. Pencere ALINTININ KENDİSİNİ içeriyordu: *«"kimse bir şey demiyor"»*
#     alıntısının içindeki *«demiyor»* karşı olgusal işaret sanıldı ve kusur
#     kaçtı. ⇒ Alıntının span'i pencereden ÇIKARILIYOR.
# ➡️ *Bir muafiyetin kapsamı, muafiyetin kendisi kadar ölçülmeli.*

# ⚠️ Liste tr_fold'dan GEÇİRİLİR — T73/T75/T76 ailesi bu depoda üç kez ısırdı.
# ⛔ «değil» ve «demem» ÖLÇÜLEREK ÇIKARILDI (yukarı bak). ⚠️ «demiyorum» ve
# «söylemiyorum» bu çiftte HİÇ ateşlemedi — aileye ait oldukları için duruyorlar
# ama ayırt edicilikleri SINANMADI.
# ⭐ Olumsuz SÖZ FİİLİ (*«söylemeyeceğim»*, *«sormadın»*) ya da MASTAR/ANMA
# çerçevesi (*«"bir şeyim yok" demekten farklı»*) — ikisi de tırnağı bir iddia
# olmaktan çıkarır. ⚠️ Kökler dar tutuldu: ilk sürüm `de\w*m[ae]\w*` idi ve
# *«denenmemiş»*i söz fiili sandı.
# ⛔ İLK SÜRÜM ÇEKİMLERİ TEK TEK SAYIYORDU ve tutulmayan partilerde iki yanlış
# pozitif üretti: *«kurmadın»* ve *«söylemiyorum»* — ikisi de listede yoktu
# ama ikisi de ilan edilen ailenin üyesi (olumsuz söz fiili). ➡️ *Çekim
# saymak, kuralı yazmak değildir.* ⇒ Türkçenin olumsuzluk eki KÖKE doğrudan
# bağlanıyor: <söz kökü> + m + [aeıiuü].
# ⚠️ Bu aynı zamanda ilk sürümün `de\w*m[ae]\w*` hatasını da kapatıyor:
# *«denenmemiş»*te «de»den sonra «n» geliyor, «m» değil.
# ⛔⛔ İKİNCİ SÜRÜM `m[aeıiuü]` YAZDI VE BİR KUSUR KAÇTI: *«sormuşsunuz»* da
# eşleşti — oysa `-muş` OLUMSUZLUK DEĞİL, öğrenilen geçmiş. Türkçede olumsuzluk
# eki yalnız `-ma/-me`; ilerleyen zamanla birleşince `-mıyor/-miyor/-muyor/
# -müyor`. ⇒ Ünlü kümesi bu ikisine daraltıldı.
# ➡️ *Biçimbirimsel bir deseni genişletmek onu genelleştirmez; yanlış ayrıştırılan
# her ek, muafiyeti sessizce büyütür.*
# ⛔ ÜÇÜNCÜ KUSUR (judge koşusuyla bulundu, 2026-09-17): *«demek ki»* bir
# ÇIKARIM belirteci, söz fiili değil — ama `de`+`me` deseniyle eşleşiyordu ve
# `v5-parti4 #20`'de uydurma bir alıntıyı (*«"İş çıkışı" dediğin şeye … demek
# ki o da bir açıklamaydı»*) muaf tuttu. ➡️ *Bir biçimbirimsel desen, aynı
# harfleri taşıyan BAŞKA BİR DİLBİLGİSEL İŞLEVİ ayırt edemez; ayırt eden şey
# ardılıdır.* ⇒ «demek ki» / «demek oluyor» açıkça hariç.
# ⛔⛔ DÖRDÜNCÜ KUSUR (2026-09-17, muafiyet denetimi buldu) — ve ailenin en
# büyüğü: Türkçede olumsuzluk eki `-ma/-me` ile ADFİİL eki `-ma/-me` EŞSESLİDİR.
# *«anlatmak»*, *«sormak»*, *«demesi»* bu desene uyuyordu ⇒ alıntının kendi
# cümlesinde HERHANGİ bir söz fiili mastarı geçmesi muafiyeti ateşliyordu.
# `v5-parti4 #5`: *«hekime "belki abartıyorum" DEDİĞİN şeyi olduğu gibi
# ANLATMAK…»* — alıntı kullanıcıya OLUMLU atfediliyor ve kaynakta yok; muafiyet
# yalnızca cümlede *«anlatmak»* geçtiği için ateşledi ve kusuru sakladı.
# ➡️⭐ *Muafiyetin gerekçesi «söz fiili var» değil, «söz fiili OLUMSUZ»du; desen
#    gerekçeyi değil harfleri kodluyordu.*
# ⇒ Mastar (`-mak/-mek`) ve adfiil+iyelik (`-ması/-mesi`) AÇIKÇA dışarıda.
KARSI_OLGUSAL = re.compile(
    r"\b(söyle|de|sor|yaz|kur|bulun|geçir|anlat|iddia et)(m[ae]|m[ıiuü]yor)"
    r"(?!k|s[ıi]|n|ler)", re.I)
# ⚠️ Dışarıda bırakılanlar: `-mak/-mek` (mastar), `-ması/-mesi`, `-man/-men`,
# `-maları/-meleri` — hepsi ADFİİL. ⭐ `-mam/-mem` AMBİVALANT bırakıldı
# (*«söylemem»* hem «söylemeyeceğim» hem «benim söylemem» olabilir) ve
# olumsuzluk okuması bu korpusta baskın; bu bir SEÇİMDİR, ölçüm değil.
# ⭐ ANMA / ÖNERİ ÇERÇEVESİ — AYRI muafiyet, çünkü AYRI gerekçe (T140 dersi).
# *«"bir şeyim yok" DEMEKTEN farklı»* (anma) ve *«"…" diye SORMAK olabilir»*
# (öneri) alıntıyı bir iddia olmaktan çıkarır — ama olumsuzlukla değil, MASTARLA.
# ⛔ Bu iki çerçeve eskiden olumsuzluk muafiyetinin sırtına biniyordu; ayrılınca
# ikisi de kendi başına sayılabilir hâle geldi ve biri genişlerse görünür.
# ⛔⛔ İLK YAZIMDA BU MUAFİYET DE ÇOK GENİŞTİ ve regresyonun 5. vakası onu
# yakaladı: cümlenin HERHANGİ bir yerindeki mastar muafiyeti ateşliyordu — yani
# olumsuzluk muafiyetinin hatasını adı değişmiş hâliyle tekrarlıyordu.
# ➡️⭐ *Çerçeve bir SÖZDİZİM ilişkisidir: mastar, alıntının KENDİ yüklemi olmalı.
#    Türkçede bu ilişki bitişiktir — alıntı mastarın hemen önünde (*«"…" diye
#    sormak»*, *«"…" demekten»*) ya da öneri kalıbının hemen ardında durur
#    (*«… söylemek olabilir — "…"»*).*
# ⛔ Pencere DAR ve araya EN ÇOK BİR sözcük girebilir; *«"…" dediğin şeyi olduğu
#   gibi anlatmak»* muaf KALMAZ — orada mastar alıntının yüklemi değildir.
# ⛔⛔ İLK DAR HÂLİ İKİ MEŞRU ÇERÇEVEYİ DÜŞÜRDÜ (v0.0.9/train üzerinde ölçüldü):
#  1. **Eşgüdümlü anma** — *«Senin yerine "devam et" ya da "kes" DEMEK bana
#     düşmez»*: mastar alıntının yüklemi ama araya BAĞLAÇLI İKİNCİ ALINTI giriyor.
#     ⭐ Bu, zaman kapısının *«hekimin ya da … uzmanın işi»* için çoktan çözdüğü
#     sorunun aynısı. ➡️ *Bir kapıda ölçülmüş bir dil olgusu, kardeş kapıda
#     yeniden keşfedilmemeli.*
#  2. **Karşıt «değil»** — *«"Gerçeği söylemek mümkün değil" demişsin,
#     "istemiyorum" DEĞİL»*: olumsuzluğu söz fiili değil, sıfat taşıyor.
#     ⚠️ Eski kapı bunu DOĞRU bağışlıyordu ama YANLIŞ sebeple (pencerede
#     *«söylemek»* geçtiği için). ➡️ *Doğru karar, yanlış gerekçeyle verilmişse
#     gerekçe düzeltilince karar da düşer; o yüzden her gerekçe ayrı yazılır.*
ANMA_ARDIL = re.compile(
    r"^\s*((ya da|veya|ile|,)\s*[\"«][^\"»]{1,40}[\"»]\s*)?"
    r"(diye\s+)?(\w+\s+)?(söyle|de|sor|yaz|anlat)(m[ae]k)", re.I)
KARSIT_DEGIL = re.compile(r"^\s*değil\b", re.I)
# ⛔⛔ ÜÇ MUAFİYET BOŞLUĞU DAHA — yayımlanmış sette 21 bulgunun elle okunmasıyla
# bulundu (2026-09-18). Üçü de ANMA çerçevesi ama biçimleri farklı:
#  1. **Olumsuz yeterlilik** — *«ben "olur" DİYEMEM»*: alıntı reddedilen bir söz.
#     ⚠️ Türkçede `de-` kökü `-y` önünde **`di-`** oluyor (*demek → diyemem*) ⇒
#     desen `d[ei]` yazmak zorunda; `\bde` yazan ilk denemem hiç ateşlemedi.
#  2. **Ulaç çerçevesi** — *«"iyi olur" DİYEREK onu üstünden almayacağım»*:
#     olumsuzluk ulacın değil ana fiilin üstünde, ama alıntı yine anılıyor.
#  3. **Karşılaştırma çerçevesi** — *«"Bir şey olmadı" İLE "olmaz" AYNI ŞEY
#     DEĞİL»*: iki önerme karşılaştırılıyor, ikisi de kimseye atfedilmiyor.
# ➡️ *Anma çerçevesinin biçimleri sayılabilir ama listesi kapanmıyor; her yeni
#    biçim ancak elle okumayla görülüyor — kapı bu sınıfta hep bir adım geride.*
OLUMSUZ_YETERLILIK = re.compile(r"\b(d[ei]|söyle|sor|yaz|anlat)(y?eme|y?emi)\w*", re.I)
ANMA_ULAC = re.compile(r"^\s*(d[ei]|söyle|sor|yaz|anlat)(y?erek|y?arak)\b", re.I)
KARSILASTIRMA = re.compile(r"\bile\s+[\"«][^\"»]{1,60}[\"»]\s*ayn[ıi]\s+şey\s+değil", re.I)
ANMA_ONCUL = re.compile(
    r"(söyle|de|sor|yaz|anlat)(m[ae]k)\s+(olabilir|olur)\s*[—:\-]?\s*$", re.I)
NE_YAPISI = re.compile(r'\bne\s+"')      # ⭐ «ne "az", ne "çok"» — ikisi de reddediliyor


def _pencere(c: str, i: int, j: int) -> str:
    """Alıntının kendi cümlesi, alıntının kendisi HARİÇ."""
    a = max(c.rfind(x, 0, i) for x in SINIR) + 1
    k = [x for x in (c.find(y, j) for y in SINIR) if x != -1]
    return c[a:i] + " " + c[j:(min(k) if k else len(c))]


def _kaynak(r: dict) -> str:
    p = [m.get("content", "") for m in r["messages"] if m["role"] == "user"]
    p += [c.get("metin", "") for c in (r.get("context") or [])]
    return tr_fold(" \n ".join(p))


# ⛔ İSİM ÇAKIŞMASI: `datasets/v0.0.8/train.jsonl` ile `datasets/v0.0.9/train.jsonl`
# ikisi de `…-train.json` yazıyordu ⇒ ikinci koşu birincinin raporunu siliyor ve
# dosya adı hangi sürüm olduğunu söylemiyordu. (JSON içindeki `girdi` + sha bunu
# kurtarıyordu ama ad yanıltıyordu.) ⇒ `datasets/` altındaki girdiler SÜRÜMLE adlanır.
def _rapor_adi(p: Path) -> str:
    return f"{p.parent.name}-{p.stem}" if p.parent.parent.name == "datasets" else p.stem

def main(yol: str) -> int:
    p = Path(yol) if Path(yol).is_absolute() else KOK / yol
    kayitlar = [json.loads(s) for s in p.read_text(encoding="utf-8").splitlines() if s.strip()]
    bulgu, muaf = [], 0
    for r in kayitlar:
        kaynak = _kaynak(r)
        for m in r["messages"]:
            if m["role"] != "assistant":
                continue
            c = m["content"]
            for i, j in _alintilar(c):
                s = c[i + 1:j].strip()
                if not (_KISA <= len(s) <= 120):
                    MUAF.yaz("kisa_alinti", r, s, c[max(0, i - 60):j + 20])
                    continue
                if tr_fold(s) in kaynak:
                    continue          # ⭐ MUAFİYET DEĞİL: alıntı kaynakta birebir var
                pencere = _pencere(c, i, j + 1)
                # ⭐ T140: iki muafiyet AYRI sayılır — biri genişlerse öbürünün
                # arkasına saklanamasın. Bağlam da yazılır: elle okuma penceresi
                # ancak görülebiliyorsa denetlenebilir (60 karakterlik sızıntı dersi).
                if KARSI_OLGUSAL.search(pencere):
                    MUAF.yaz("karsi_olgusal", r, s, pencere); muaf += 1
                    continue
                if NE_YAPISI.search(pencere):
                    MUAF.yaz("ne_yapisi", r, s, pencere); muaf += 1
                    continue
                if KARSIT_DEGIL.search(c[j + 1:j + 12]):
                    MUAF.yaz("karsit_degil", r, s, c[max(0, i - 60):j + 20]); muaf += 1
                    continue
                if OLUMSUZ_YETERLILIK.search(pencere):
                    MUAF.yaz("olumsuz_yeterlilik", r, s, pencere); muaf += 1
                    continue
                if KARSILASTIRMA.search(c[max(0, i - 80):j + 80]):
                    MUAF.yaz("karsilastirma", r, s, c[max(0, i - 80):j + 80]); muaf += 1
                    continue
                if ANMA_ULAC.search(c[j + 1:j + 30]):
                    MUAF.yaz("anma_ulac", r, s, c[j + 1:j + 60]); muaf += 1
                    continue
                if ANMA_ARDIL.search(c[j + 1:j + 60]) or ANMA_ONCUL.search(c[max(0, i - 45):i]):
                    MUAF.yaz("anma_oneri", r, s, c[max(0, i - 45):j + 30]); muaf += 1
                    continue
                bulgu.append({"parti_sira": r["gen_meta"]["parti_sira"], "alinti": s})
    ozet = {"tarih": "2026-09-17",
            "betik": "scripts/analiz/2026-09-17-alinti-birebirlik-kapisi.py",
            "girdi": str(p) if p.is_absolute() else str(p.relative_to(KOK)),
            "girdi_sha256_16": hashlib.sha256(p.read_bytes()).hexdigest()[:16],
            "kayit": len(kayitlar), "karsi_olgusal_muaf": muaf,
            "isaretli_kayit": len({b["parti_sira"] for b in bulgu}),
            "bulgu": bulgu,
            "muafiyet_ozeti": MUAF.ozet(), "muafiyet": list(MUAF.DEFTER)}
    cikti = KOK / f"reports/analiz/2026-09-17-alinti-birebirlik-{_rapor_adi(p)}.json"
    cikti.write_text(json.dumps(ozet, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(kayitlar)} kayıt · karşı olgusal muaf {muaf} · "
          f"⛔ işaretli {ozet['isaretli_kayit']} kayıt / {len(bulgu)} öge")
    for b in bulgu:
        print(f"   #{b['parti_sira']:>2} «{b['alinti'][:70]}»")
    print(f"→ {cikti.relative_to(KOK)}")
    return 1 if bulgu else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "data/candidates/v5-parti5.jsonl"))
