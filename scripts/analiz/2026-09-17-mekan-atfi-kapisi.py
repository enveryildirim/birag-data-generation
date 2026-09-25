#!/usr/bin/env python3
"""Cevapta geçen MEKÂN adı kullanıcının turlarında var mı — T104'ün beşinci üyesi.

⛔⛔ **Neden var.** T104 kırpma kusurunun beş biçimini saymıştı: alıntı, zaman,
kaynak atfı, **mekân**, örüntü. İlk üçü için kapı yazıldı (T105/T109, T113);
mekân açıkta kaldı ve judge onu buldu: `v5-parti4 #47`'de cevap *«İkiniz de aynı
MUTFAKTA duruyorsunuz»* diyor — mutfak konuşmada hiç geçmiyor, yalnız üretim
sırasındaki iç muhakemede var.

⭐ **Önce daha geniş bir yol denendi ve ÇÜRÜDÜ:** «cevapta olup kullanıcıda
olmayan ama thinking'de olan sözcükler» 60 kaydın 43–57'sini işaretledi ve
sızanlar *«karar»*, *«metinde»*, *«doğrudan»* gibi sıradan kelimelerdi.
➡️ *Sözcük örtüşmesi, uydurulmuş ayrıntıyı konu ortaklığından ayıramıyor;
ayıran şey sözcüğün NEYİ GÖSTERDİĞİ ve bunu ancak kapalı bir sözlük verir.*

⭐ **Elle ölçülen kesinlik (2026-09-17, 300 kayıt):** ilk sürüm 11 aday
işaretledi, **3'ü gerçek** (%27). Yanlış pozitifler dört sınıfta toplandı ve
dördü de kapatıldı:
  1. **Ünsüz yumuşaması** — *«yatağa»* varken *«yatak»* aranıyordu.
  2. **Yönlendirme bağlamı** — *«ilacı aldığın eczaneye»*, *«okulun rehberlik
     birimi»*: bir mekân ADI değil, §8b'nin istediği KAYNAK TÜRÜ.
  3. **Eşadlılık** — *«meslek odası»* bir oda değil.
  4. **Mecaz** — *«ikisini aynı masaya koydun»*, *«bu odada kimse»*.

⛔ Kalan sayı bir ALT SINIRDIR: sözlükte olmayan mekân adları görünmez.
"""
from __future__ import annotations
import glob, hashlib, json, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
sys.path.insert(0, str(KOK / "scripts/analiz"))
import _muafiyet as MUAF  # noqa: E402  ⭐ T140: bağışlanan her öge sayılır
from tohum_guvenlik import tr_fold, AD_CEKIM_EKI  # noqa: E402

MEKAN = ["mutfak", "balkon", "salon", "bahçe", "araba", "market", "bakkal", "kafe",
         "kıraathane", "durak", "otopark", "tuvalet", "banyo", "yatak", "koltuk",
         "masa", "sofra", "apartman", "asansör", "ofis", "yurt", "teras", "avlu", "oda"]
# ⚠️ Ünsüz yumuşaması: «yatak» → «yatağa». ⛔ İLK DENEMEDE son harf KIRPILDI
# (`re.escape(k)[:-1]`) ve kapı patladı: «kafe» → `kaf\w*` *«kafanın»*ı,
# «durak» → `dura\w*` *«durabilmişsin»*i yakaladı; 11 aday 62'ye çıktı.
# ➡️ *Bir eki tanımak için kökü kısaltmak, kökü başka kelimelerin önekine
#    çevirir.* ⇒ Kırpma yerine YUMUŞAMIŞ VARYANT üretiliyor.
_YUM = {"k": "ğ", "p": "b", "ç": "c", "t": "d"}
def _varyant(k: str) -> list[str]:
    f = tr_fold(k)
    v = [f]
    if f and f[-1] in _YUM:
        v.append(f[:-1] + _YUM[f[-1]])
    return v

# ⛔⛔ İKİNCİ KÖK-ÖNEK DELİĞİ: `\w*` kökü keyfî bir ÖNEK yapıyor.
# T122 kök KIRPMAYI kaldırmıştı ama kökten SONRASINI serbest bırakmıştı ve
# eski katmanlarda ölçüldüğünde delik göründü: «durak» → *«durakLAMA»*
# (`v4-parti2 #30`: «Bugünkü duraklama da tam o aralıkta oldu»). «duraklamak»
# bir fiildir, durakla ilgisi yoktur.
# ➡️ *Bir kökü ekle aramak, ekin NE OLDUĞUNU söylemeyi gerektirir: `\w*` «her
#    şey ek olabilir» demektir ve Türkçede yapım ekleri kökün anlamını
#    değiştirir. Çekim eki kapalı bir kümedir, yapım eki değil.*
# ⇒ Kök yalnız AD ÇEKİM eklerini alabilir; kapalı liste aşağıda.
# ⛔ Liste 2026-09-18'de `src/tohum_guvenlik.py`'ye TAŞINDI: `checks.scan_forbidden`
# de aynı sorunu yaşıyordu (*«keş»* → *«keşke»*) ve iki yerde iki tanım iki sayı
# demektir (K97). Tanım aynı, yeri tek.
_EK = AD_CEKIM_EKI


def _desen(k: str) -> re.Pattern:
    """CEVAP tarafı — KATI: kök yalnız ad çekim eki alabilir."""
    return re.compile(r"\b(?:" + "|".join(re.escape(x) for x in _varyant(k)) + r")" + _EK + r"\b")


def _desen_kaynak(k: str) -> re.Pattern:
    """KULLANICI tarafı — GENİŞ: soru «bu yeri hiç andı mı», «hangi ekle andı» değil.

    ⛔⛔ **ASİMETRİ ÖLÇÜLEREK BULUNDU.** Çekim eki listesi iki tarafa birden
    uygulandığında yeni bir yanlış pozitif doğdu: `v4-parti2 #30`'da cevap
    *«terasta»* diyor ve kullanıcı *«terastayken»* demiş — ama `-ken` kapalı
    listede yok, dolayısıyla kullanıcının sözü GÖRÜNMEZ oldu ve dayanaklı bir
    cümle uydurma sayıldı.
    ➡️ *İki taraf aynı soruyu sormuyor. Cevap tarafında soru «bu sözcük gerçekten
    o mekân mı» (yapım eki ayırt edilmeli); kullanıcı tarafında soru «kullanıcı
    bu yeri andı mı» (herhangi bir biçim yeter). Aynı deseni iki yere koymak,
    ikinci sorunun yanlış sorulması demek.*
    ⚠️ Bedeli yazılı: kullanıcı *«duraklama»* deyip cevap *«durakta»* derse kapı
    haksız yere beraat verir. Bu yön **yanlış negatif** üretir ve kapı zaten bir
    ALT SINIR bildiriyor.
    """
    return re.compile(r"\b(?:" + "|".join(re.escape(x) for x in _varyant(k)) + r")\w*")

# ⭐ §8b YÖNLENDİRME bağlamı: mekân adı bir kaynak TÜRÜ olarak geçiyorsa atıf değil.
YONLENDIRME = re.compile(
    r"(birim|hat|merkez|danışmanlık|poliklinik|hekim|servis|kurum|yer var|"
    r"başvur|soracak|sorabilir|gidilebilecek|nöbetçi|meslek odası)", re.I)
# ⭐ MECAZ: «aynı X'te/da», «bu odada» gibi kalıplarda mekân somut bir yer değildir.
# ⛔⛔ İLK MECAZ MUAFİYETİ GERÇEK BİR BULGUYU ÖLDÜRDÜ. `aynı\s+\w+[dt][ae]`
# deseni *«aynı masaya koydun»*u (mecaz) elemek için yazılmıştı ama *«aynı
# MUTFAKTA duruyorsunuz»*u da eledi — oysa o, judge'ın bulduğu gerçek kusurdu.
# ➡️ *«Aynı X'te» kalıbı X soyutsa mecaz, X somut bir yerse GERÇEK bir atıftır;
#    kalıbın kendisi ayırt etmiyor, ayıran şey X.* ⇒ Kalıp yalnız MEKÂN
#    SÖZLÜĞÜNDE OLMAYAN bir X için muaf.
# ⭐ Muafiyet DAR tutuluyor ve FİİLE bağlanıyor: *«aynı masaya KOYMAK»* mecazdır
# (bir yere koymak = birlikte değerlendirmek), *«aynı mutfakta DURMAK»* değildir.
# ➡️ *«Aynı X'te» kalıbı tek başına ayırt etmiyor; ayıran şey X'in somutluğu
#    DEĞİL, yüklem: koymak soyut, durmak/olmak somut.*
MECAZ = re.compile(r"bu\s+odada|aynı\s+\w+[ya]a?\s+koy", re.I)

# ⭐⭐ SINIFLANDIRMA — MUAFİYET DEĞİL (2026-09-18). Yayımlanmış sette 11 bulgunun
# **11'i de** elle okundu: dokuzu mecaz (*«masada iki şey var»*, *«ben o odada
# olmayacağım»*), ikisi ılımlı çıkarım (*«restorana gittik»* → *«masaya oturdun»*).
# ⛔ Muafiyet GENİŞLETİLMEDİ: kapı T113'ün kusuru için kuruldu (*«İkiniz de aynı
#   MUTFAKTA duruyorsunuz»* — kullanıcının hiç anmadığı bir yerde durduğunun
#   iddia edilmesi) ve mecaz kalıplarını affetmek o gücü de aşındırırdı.
# ⇒ Bulgular ETİKETLENİYOR: okuma yükü 11'den 2'ye iniyor, tespit gücü duruyor.
# ⭐ Sınandı: T113'ün kendi cümlesi **etiketlenmiyor** — yani etiket, kapının
#   kurulduğu kusuru gizlemiyor.
# ➡️⭐⭐ *Bir yanlış pozitif sınıfını AFFETMEK ile ETİKETLEMEK aynı şey değildir:
#    ilki kapının gücünü, ikincisi yalnız okuyanın yükünü azaltır.*
SOYUT = re.compile(r"\b(şey|şeyler|konu|konular|rapor|cümle|karar|soru|mesele)\w*\b", re.I)
VARLIK = re.compile(r"\bben\b|\bsenin\b|olmayacağ|duran ben", re.I)
KIP = re.compile(r"\b(olabil|durabil|istediğin|ne olurdu|var mı)\w*", re.I)


def _sinif(cumle: str) -> list[str]:
    """Bulgunun okuma önceliği — boşsa ⛔ ELLE OKU."""
    e = []
    if SOYUT.search(cumle):
        e.append("soyut")
    if VARLIK.search(cumle):
        e.append("varlık")
    if KIP.search(cumle):
        e.append("kip")
    return e


def _kullanici(r: dict) -> str:
    p = [m["content"] for m in r["messages"] if m["role"] == "user"]
    p += [c.get("metin", "") for c in (r.get("context") or [])]
    return tr_fold(" ".join(p))


def main(yollar: list[str]) -> int:
    if not yollar:
        yollar = sorted(glob.glob(str(KOK / "data/candidates/v5-parti*.arinmis.jsonl")))
    bulgu = []
    for f in yollar:
        p = Path(f) if Path(f).is_absolute() else KOK / f
        for s in p.read_text(encoding="utf-8").splitlines():
            if not s.strip():
                continue
            r = json.loads(s)
            kay = _kullanici(r)
            cv = [m for m in r["messages"] if m["role"] == "assistant"][-1]["content"]
            for cum in re.split(r"(?<=[.!?])\s+|\n\n", cv):
                # ⭐ T140: muafiyet ancak ADAY varken kaydedilir. Mekân sözcüğü hiç
                # geçmeyen bir cümleyi *«muaf tuttum»* diye saymak defteri şişirir ve
                # denetimi tam da kör etmemesi gereken yerde kör eder.
                aday = [k for k in MEKAN if _desen(k).search(tr_fold(cum))]
                if not aday:
                    continue
                # ⭐ İKİ MUAFİYET AYRI SAYILIR: tek `or` altında toplanınca biri
                # genişlediğinde öbürünün arkasına saklanabiliyordu.
                # ⭐⭐ NET BAĞIŞ: kaynakta zaten geçen bir mekân için muafiyetin
                # ateşlemesi kusur saklamaz; ayrı işaretlenir ki sayı şişmesin.
                _net = [k for k in aday if not _desen_kaynak(k).search(kay)]
                _ek = "" if _net else " [ZATEN YERDE]"
                if YONLENDIRME.search(cum):
                    MUAF.yaz("yonlendirme_cumlesi" + _ek, r, _net or aday, cum.strip())
                    continue
                if MECAZ.search(cum):
                    MUAF.yaz("mecaz" + _ek, r, _net or aday, cum.strip())
                    continue
                for k in aday:
                    if not _desen_kaynak(k).search(kay):
                        bulgu.append({"korpus": p.stem, "sira": r["gen_meta"]["parti_sira"],
                                      "mekan": k, "cumle": cum.strip()[:120],
                                      "sinif": _sinif(cum)})
                        break
                    # ⭐⭐ ASİMETRİNİN BEDELİ ÖLÇÜLÜR: kaynak deseni GEVŞEK (`\w*`),
                    # cevap deseni SERT. Gevşek desen, sert desenin bulamadığı bir
                    # yerde eşleşiyorsa bağışlanan şey tam da asimetridir — ve bu
                    # bağış hiç sayılmamıştı.
                    if not _desen(k).search(kay):
                        MUAF.yaz("kaynak_gevsek_eslesme", r, k, cum.strip())
    cikti = KOK / "reports/analiz/2026-09-17-mekan-atfi-kapisi.json"
    cikti.write_text(json.dumps(
        {"tarih": "2026-09-17", "betik": "scripts/analiz/2026-09-17-mekan-atfi-kapisi.py",
         "taranan_dosya": len(yollar), "bulgu": bulgu,
         "muafiyet_ozeti": MUAF.ozet(), "muafiyet": list(MUAF.DEFTER)}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"{len(yollar)} dosya · ⛔ işaretli {len(bulgu)} öge")
    for b in bulgu:
        et = "+".join(b.get("sinif") or []) or "⛔ ELLE OKU"
        print(f"   {b['korpus'].replace('.arinmis',''):<16} #{b['sira']:<3} «{b['mekan']}» "
              f"[{et}] → {b['cumle'][:64]}")
    print(f"→ {cikti.relative_to(KOK)}")
    return 1 if bulgu else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
