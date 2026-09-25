"""Tohum havuzunda kriz/risk içeriği taraması — TEK kaynak.

Neden ayrı modül: bu filtre K76'da bulunan bir açığın yamasıdır ve şu an
`scripts/analiz/2026-09-14-v3-parti{2,3}-plani.py` içinde **kopyalanmış** hâlde
duruyor. O iki betiğin çıktıları (`data/plan/v3-parti{2,3}.jsonl`) DONDURULMUŞ,
bu yüzden onlara dokunulmadı; yeni tüketiciler (golden eval) buradan alır.

K76'nın iki bulgusu buraya taşındı:
  1. `notlar.esdurumlar` hiç taranmıyordu — 2.240 tohumun 52'si riskli eşdurum
     taşıyor ve bunlar `user_message`'da görünmüyor.
  2. Türkçe büyük-İ tuzağı: `"İntihar".lower()` → `"i̇ntihar"` (i + birleşen
     nokta) ve `"intihar"` ile EŞLEŞMİYOR. 52 riskli tohumun 21'i bu yüzden
     taramadan kaçıyordu; düz `.lower()` yalnızca 31'ini buluyor.

2026-09-15 — aynı ailenin ÜÇÜNCÜ örneği (K103 oturumunda bulundu):
  3. `tr_kucult` NFKD uyguluyor, yani "ö" → "o"+U+0308. Yalnızca birleşen NOKTA
     (U+0307) siliniyor, diğer birleşen imler kalıyor. Sonuç: **ç ö ü ş ğ içeren
     her düz kalıp ölü desendir** — aranan metin ayrıştırılmış, iğne bileşik.
     `kriz_icerigi` bundan kurtulmuştu (iki tarafı da `tr_kucult`'tan geçiriyor),
     ama bir satır altındaki eşdurum taraması ham anahtarı kullanıyordu ve
     `RISKLI_ESDURUM`'un 11 kalıbından 4'ü hiç eşleşemiyordu ("öz kıyım",
     "özkıyım", "nöbet", "aşırı doz"). Bugünkü 2.240 tohumda kayba yol açmıyor
     (ölçüldü) ama **sessizce** bekliyordu.
     Aynı hata `2026-09-14-kriz-filtresi-bedensel-acik.py`'nin BEDENSEL regex'inde
     KAYBA yol açtı: 21 kalıbın 9'u ölüydü, golden havuzunda **19 yerine 25** tohum
     var ve kaçan 6'nın biri `locked` dilimindeki «göğsüm sıkıştı, kalbim deli gibi
     attı» kaydıydı.

Bu yüzden artık tek giriş noktası `desen()` ve modül yüklenirken `_olu_desen_taramasi()`
her listeyi denetliyor: ölü kalıp varsa **import patlar**, sessiz kalmaz.

⚠️ `KRIZ_ANAHTAR` TAM DEĞİL. Tam liste uzman Oturum 1'e bağlı (Kural 3).
Buradaki liste "bulduklarımız", "hepsi" değil — negatif sonuç kanıt sayılmaz.
"""
from __future__ import annotations

import re
import unicodedata

KRIZ_ANAHTAR = [
    "yaşamak istemiyorum", "ölmek istiyorum", "intihar", "canıma kıy", "kendimi asa",
    "kendime zarar", "bitirmek istiyorum", "son vermek istiyorum", "uyanmasam",
    "uyanmak istemiyorum", "yaşamaya değmez", "hayatıma son", "bileğimi", "hapları içt",
    "yok olmak istiyorum", "ölsem", "öldürmek istiyorum kendimi", "yük oluyorum",
    "bensiz daha iyi", "dayanamıyorum artık", "kurtulmak istiyorum bu hayattan",
    "acil servis", "acilde", "ambulans", "mide yıkan", "yoğun bakım", "doz aşımı",
    "aşırı doz", "taburcu", "entübe", "komaya",
    # K65'te bulunan açık: uyuşukluk hâlinde araç kullanma listede yoktu.
    "direksiyonda", "gözüm kapandı", "araba kullan",
]

RISKLI_ESDURUM = ("intihar", "kendine zarar", "öz kıyım", "özkıyım", "psikoz",
                  "sanrı", "yoksunluk vakası", "deliryum", "nöbet", "overdoz", "aşırı doz")

# Kural 3: kriz davranışı uzman onayına bağlı. Bu iki senaryo golden.dev'e
# giremez; `evals/safety_crisis.jsonl` bekliyor.
YASAK_SENARYO = ("kriz", "sanrili_soylem")


def tr_kucult(s: str) -> str:
    """Türkçeye uygun küçültme — birleşen noktayı da düşürür. Bkz. modül başlığı."""
    s = s.replace("İ", "i").replace("I", "ı").lower()
    return unicodedata.normalize("NFKD", s).replace("̇", "")


def i_sinifi(s: str) -> str:
    """⭐⭐ ASCII özensiz BÜYÜTME Türkçede BİLGİ KAYBIDIR — geri getirilemez.

    `i` ve `ı` büyütülünce ikisi de `I` olur (Python'un `.upper()`'ı Türkçe bilmez,
    klavyesiz yazan insan da öyle yazar). ⛔ Hiçbir TEK YÖNLÜ küçültme hangisinin
    hangisi olduğunu geri getiremez:

        "ilaç adı" -> "ILAÇ ADI" -> tr okuması "ılaç adı" · ascii okuması "ilaç adi"

    İkisi de aranan kalıpla eşleşmez. Çözüm normalizasyon değil **SINIF**: dört harf
    (`i ı İ I`) tek harfe iner ve ayrım aramada hiç kullanılmaz.

    ⚠️ **Bedeli yazılı:** `ilaç` artık `ılaç`ı da yakalar (yanlış pozitif yönü).
    Uygulandığı her kapıda korpus etkisi ÖNCE ölçüldü ve **0** çıktı (T73, T75, T76).

    ⛔ 2026-09-16'da `checks.py`'den buraya TAŞINDI: bu modül kendini Türkçe
    küçültmenin *«TEK giriş noktası»* ilan ediyor ve ailenin sekiz örneğinden sonra
    fonksiyonun başka bir dosyada durması ailenin dokuzuncusunu davet ediyordu.
    """
    return s.replace("İ", "I").replace("i", "I").replace("ı", "I")


def tr_fold(s: str) -> str:
    r"""`i_sinifi` + küçültme, **NFKD YOK** — regex'le kullanılabilen sürüm.

    ⚠️ `tr_kucult` NFKD uyguluyor ve ayrıştırılmış metinde `\b`/`\w` semantiği
    bozuluyor; bu yüzden desen üzerinde çalışan yerler (`normalize.norm_sure`,
    `checks.KLINIK_IDDIA`) bunu kullanır. ⛔ Bedeli: ayrıştırılmış `ç`/`ş`/`ğ`
    taşıyan metin hâlâ kaçabilir — açık kalem (T75 · T76).
    """
    return i_sinifi(s).lower()


def tr_sadelestir(s: str) -> str:
    r"""`tr_fold` + **aksan düşürme** — ailenin en geniş foldu (T84).

    `tr_fold` `i/ı/İ/I` ayrımını kaldırır ama `ü→u`, `ş→s`, `ğ→g`, `ç→c`, `ö→o`
    ayrımını **kaldırmaz**. ⛔ Türkçe klavyesi olmayan biri `Universite` yazar ve
    o hâl eşleşmez. Bu fonksiyon o ayrımı da düşürür.

    ⚠️ **NFKD YOK** — `tr_kucult`'un ayrıştırması ``/`\w` semantiğini bozuyor;
    burada harfler **doğrudan** eşleniyor, ayrıştırılmıyor.

    ⛔ **Bedeli ölçüldü, sonra uygulandı** (K40'ın sırası): `configs/taxonomy.yaml`
    içindeki `egitim` kurallarında ve `stres_tipi`nin 76 anahtarında **çakışma
    yok** (iki farklı anahtar aynı sadeleşmiş dizgeye düşmüyor), ham 2240 kayıtta
    **hüküm farkı 0**.

    ⛔ **`checks.scan_forbidden`'a UYGULANMADI:** §15 bir güvenlik kapısı ve her
    genişletme ayrı gerekçe ister (T80'in dersi: yönü kapı belirler). Orada
    yalnızca `i_sinifi` var ve bedeli ayrıca ölçülmüştür.
    """
    for a, b in zip("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU"):
        s = s.replace(a, b)
    return tr_fold(s)


def desen(kalip: str) -> re.Pattern[str]:
    """Kalıbı metinle AYNI normalizasyona sokup derler.

    `tr_kucult` NFKD uyguladığı için "çarpıntı" gibi bileşik yazılmış bir kalıp
    ayrıştırılmış metinde hiç eşleşmez. Regex meta karakterleri (|, (?:...), \b)
    ASCII olduğundan normalizasyondan etkilenmez; yalnızca harfler değişir.
    """
    return re.compile(tr_kucult(kalip))


# ⚠️ NFKD sonrası birleşen imler (U+0300-U+036F) `\w` sınıfına GİRMEZ. Bu yüzden
# "öksür\w*" kalıbı "öksürdüğümü"de ekin ortasında kesiliyor ve alıntı «öksürdu»
# gibi bozuk çıkıyordu. Türkçe ek eşlemesi bu sınıfla yapılır, `\w*` ile değil.
EK = r"[\w\u0300-\u036f]*"

# Bedensel belirti ekseni. `KRIZ_ANAHTAR` niyet ve olay sözcüklerinden kurulu
# ("intihar", "acil servis"); beden hiç yoktu — bkz.
# reports/analiz/2026-09-14-kriz-filtresi-bedensel-acik.md
# ⚠️ GENİŞ ve bilerek öyle: "elim titriyor" heyecandan da olur. Bu liste
# "kriz" demiyor, "uzmanın bakması gereken yer" diyor (Kural 3).
BEDENSEL_BELIRTI = desen(
    r"kan ter|terleyerek uyan|kalbim duracak|kalbim küt|kalbim (?:deli gibi )?(?:hızlı )?at"
    r"|çarpıntı|titreme|titriyor|el(?:im|lerim)? titri"
    r"|nöbet geçir|havale|bayıl|kustum|kusuyorum|kusma|mide(?:m)? bulan|bulantı"
    r"|görme bulan|halüsinasyon|göremiyorum|bilinc|uyuşma|felç"
    r"|nefes alamı|nefes(?:im)? (?:zor|daral)|göğsüm sıkış|göğsüm ağırlaş|göğsümde ağırlık"
    # Türkçe eklemeli: KÖKTEN sonra serbest. "öksürüyor" yazıp "öksürdüğümü"yü
    # kaçırmak, kalıbın kendisini ölü desen kadar işe yaramaz yapıyordu.
    rf"|öksür{EK}|kan tükür{EK}|kan geliyor|kan gelmiş|baş{EK} dön{EK}"
    rf"|dil{EK} tutul{EK}"
    # 2026-09-15: `7314affdd17dc420` (locked havuzu) elle tarama sırasında yakalandı —
    # «tuvalette siyaha çalan bir şey gördüm» kalıpta YOKTU. Sindirim kanaması
    # işareti bilinen bir kırmızı bayrak ve tarama onu hiç görmüyordu.
    # ⚠️ Bu bir KAPSAM genişletmesi; hangisinin aciliyet taşıdığı yine uzmana ait.
    rf"|siyah{EK} (?:çalan|dışkı|kaka)|dışkı{EK} siyah|kanl{EK} kusma|kahve telvesi")


def _olu_desen_taramasi() -> None:
    """Her güvenlik kalıbı KENDİ metninde bulunabiliyor mu? Bulamıyorsa import patlar.

    Şekil değil **davranış** sınaması: kalıbın bileşik yazılmış olması tek başına
    hata değil (`kriz_icerigi` iki tarafı da normalize ediyor, orada sorun yok).
    Hata, tüketen kodun HAM kalıbı normalize metinle karşılaştırmasıdır. Onu ancak
    kalıbı gerçek arama yolundan geçirerek görürüz.

    K44/K47/K49 ailesinin dersi: sessizce yanlış çalışan katman, doğrulanmadığı
    sürece doğru sayılıyor. Aşağıdaki üç kalem o sessizliği kaldırır ve üçü de
    bu depoda GERÇEKTEN olmuş hatalara karşılık gelir.
    """
    h: list[str] = []

    # 1) Kriz anahtarları — kriz_icerigi'nin kendi yolundan.
    for k in KRIZ_ANAHTAR:
        if not kriz_icerigi({"user_message": f"bugün {k} diyorum", "meta": {}}):
            h.append(f"KRIZ_ANAHTAR {k!r} kendi metninde bulunamadı")

    # 2) Riskli eşdurumlar — aynı yoldan, ama esdurumlar alanı üzerinden (K76 bulgu 1).
    for k in RISKLI_ESDURUM:
        sahte = {"user_message": "", "meta": {"notlar": {"esdurumlar": [k]}}}
        if not kriz_icerigi(sahte):
            h.append(f"RISKLI_ESDURUM {k!r} kendi eşdurum kaydında bulunamadı")

    # 3) Tarihsel tuzaklar — ikisi de bu depoda yaşandı, ikisi de sessizdi.
    for metin, bekle in (("İntihar etmeyi düşünüyorum", True),      # K76 bulgu 2 (büyük İ)
                         ("Nöbet geçirmiş", True),                  # bulgu 3 (ö)
                         ("Aşırı doz almış", True)):                # bulgu 3 (ş)
        var = bool(kriz_icerigi({"user_message": "",
                                 "meta": {"notlar": {"esdurumlar": [metin]}}})) or \
              bool(kriz_icerigi({"user_message": metin, "meta": {}}))
        if var is not bekle:
            h.append(f"tarihsel tuzak: {metin!r} -> {var}, beklenen {bekle}")

    # 4) Bedensel eksen — accent taşıyan kalıplar canlı mı (bulgu 3'ün kayıp veren yüzü).
    for metin in ("göğsüm sıkıştı", "çarpıntı oldu", "nöbet geçirdim",
                  "görme bulanıklığı var", "felç gibi", "uyuşma var"):
        if not bedensel_belirti(metin):
            h.append(f"BEDENSEL_BELIRTI {metin!r} yakalanamadı")

    if h:
        raise AssertionError("Güvenlik kalıbı kendi metninde bulunamıyor:\n  "
                             + "\n  ".join(h))


def kriz_icerigi(tohum: dict) -> list[str]:
    """Tohumda kriz/risk işareti varsa hangi anahtarların vurduğunu döndürür."""
    metin = tr_kucult(tohum["user_message"] + " " + tohum.get("scenario_context", ""))
    vurus = [a for a in KRIZ_ANAHTAR if tr_kucult(a) in metin]
    for e in tohum["meta"].get("notlar", {}).get("esdurumlar", []):
        # ⚠️ İKİ TARAF DA normalize edilir. Ham `k` kullanmak "nöbet"/"aşırı doz"
        # gibi kalıpları ölü desen yapıyordu (modül başlığı, bulgu 3).
        vurus += [f"eşdurum:{e}" for k in RISKLI_ESDURUM if tr_kucult(k) in tr_kucult(e)]
    return vurus


# Ölçülmüş yanlış pozitif sınıfı 1: duygusal deyim. «içim titriyor» beden değil
# heyecandır (golden.dev gd-011). Kalıptan ÖNCE düşülür — sınırlı ve dilbilgisel.
# Araya sıfat girebiliyor ("içim HÂLÂ titriyor"), o yüzden \s+ değil sınırlı pencere;
# cümle sınırı aşılmaz ([^.!?]) ki uzak iki cümle yanlışlıkla birleşmesin.
_DEYIM = desen(r"iç(?:im|i|imiz|iniz)\b[^.!?]{0,20}?titri\w*")


def bedensel_belirti(metin: str) -> list[str]:
    """Metinde geçen bedensel belirti ifadeleri (bileşik biçime geri çevrilmiş).

    ⛔ **Tıbbi aciliyet kararı VERMEZ.** Yalnızca "burada bir beden ifadesi geçiyor"
    der. Aciliyet klinik karardır ve uzmana aittir (Kural 3).

    ⚠️ **Otomatik dışlama kapısı olarak KULLANILAMAZ.** Ölçüldü (2026-09-15): 48
    golden.dev öğesinde 2 kez vurdu, **ikisi de yanlış pozitif**:
      · `gd-011` «içim hâlâ titriyor» — duygusal deyim (aşağıda düşülüyor)
      · `gd-040` «oğlum sürekli öksürüyor» — **başkasının** belirtisi
    İkinci sınıf regex ile ayrılamaz: özneyi çözmek gerekir. Bu yüzden fonksiyon
    "bakılacak yer" işaretler, karar vermez — öğe yazarken elle denetlenir.
    """
    t = _DEYIM.sub(" ", tr_kucult(metin))
    return sorted({unicodedata.normalize("NFC", m.group(0))
                   for m in BEDENSEL_BELIRTI.finditer(t)})


def golden_uygun(tohum: dict) -> tuple[bool, str]:
    """Tohum golden eval'e (Eksen 1) girebilir mi? (uygun_mu, gerekçe).

    Eksen 1 terapötik kaliteyi ölçer; kriz ve çok yüksek risk AYRI eksenin
    (Eksen 2) konusu ve protokolü uzman onayı bekliyor.
    """
    if tohum["meta"].get("senaryo") in YASAK_SENARYO:
        return False, f"senaryo={tohum['meta'].get('senaryo')} (Eksen 2, uzman onayı)"
    if tohum["meta"].get("risk_seviyesi") in ("cok_yuksek", "yuksek"):
        return False, f"risk_seviyesi={tohum['meta'].get('risk_seviyesi')}"
    vurus = kriz_icerigi(tohum)
    if vurus:
        return False, "kriz içeriği: " + ", ".join(vurus[:3])
    return True, ""


_olu_desen_taramasi()


# ⭐⭐ AD ÇEKİM EKİ — KAPALI küme. İlk olarak `2026-09-17-mekan-atfi-kapisi.py`de
# ölçülerek kuruldu (T122'nin açtığı delik): kökten sonrasını `\w*` ile serbest
# bırakmak *«durak»*ı *«duraKLAMA»*ya, *«keş»*i *«keŞKE»*ye bağlar.
# ➡️⭐ *Bir kökü ekle aramak, ekin NE OLDUĞUNU söylemeyi gerektirir. `\w*` «her şey
#    ek olabilir» demektir ve Türkçede YAPIM eki kökün anlamını değiştirir. ÇEKİM
#    eki kapalı bir kümedir, yapım eki değil.*
# ⚠️ Küme AD çekimi içindir. Fiil çekimi (*«geçecekTİ»*) kapsam dışıdır ve bu
#   bilerek böyledir: çıplak biçim yine eşleşir, türemiş kip eşleşmez.
# ⛔ Buraya taşındı çünkü iki yerde iki tanım iki sayı demektir (K97): mekân kapısı
#   ve `checks.scan_forbidden` artık AYNI listeyi kullanıyor.
_COGUL = r"(?:lar|ler)?"
_IYE = r"(?:ımız|imiz|umuz|ümüz|ınız|iniz|unuz|ünüz|ım|im|um|üm|ın|in|un|ün|sı|si|su|sü|ı|i|u|ü)?"
_KAYNAS = r"(?:n)?"
_HAL = r"(?:dan|den|tan|ten|da|de|ta|te|ın|in|un|ün|yla|yle|la|le|ya|ye|a|e|ı|i|u|ü)?"
AD_CEKIM_EKI = _COGUL + _IYE + _KAYNAS + _HAL
