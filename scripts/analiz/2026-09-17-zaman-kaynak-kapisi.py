#!/usr/bin/env python3
"""Cevapta geçen ZAMAN ve KAYNAK-ATFI sözcükleri kullanıcı turlarında var mı.

⛔⛔ **Neden var.** T104: `uretim-v5` §3a′ uydurulmuş ayrıntıyı önlemek için
yazıldı ve sonraki partide kusur **2/54 → 6/58** çıktı. Altısının **hiçbiri
tırnaklı değildi** ⇒ `thinking-alinti-denetimi` (dizge arar) hiçbirini göremezdi.
Biçimleri: kaynak atfı · zaman damgası · zamansal ilişki · mekân · örüntü.

⭐ Bu kapı ailenin **iki üyesini** hedefliyor ve ikisi de KAPALI SÖZLÜKLE
aranabiliyor:
  1. **zaman** — *«dün gece»*, *«öğleden sonra»*, *«aynı akşam»*. Modelin bir
     zaman bilgisini KENDİSİ getirmesinin meşru hâli yok: ne zaman olduğunu
     yalnız kullanıcı bilir.
  2. **kaynak atfı** — *«doktorunun»*, *«eşinin»*: 2. tekil iyelik + tamlayan.
     Model bir kişiyi kullanıcıya ATFEDİYOR; o kişinin varlığını kullanıcı
     söylemiş olmalı.

⛔ **Mekân ve örüntü KAPSAM DIŞI** — kapalı sözlükle aranamıyorlar. Bu kapı
ailenin tamamını değil, **sözlükle bulunabilen kısmını** ölçer ve bulduğu sayı
bir ALT SINIRDIR.

⚠️ Yalnızca **tür adları** (*«seni gören bir hekim»*) kapsam dışı: iyelik eki
taşımayan meslek adı bir atıf değil, §8b'nin istediği yönlendirmedir.

Kullanım: uv run python scripts/analiz/2026-09-17-zaman-kaynak-kapisi.py <kayitlar.jsonl>
"""
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
sys.path.insert(0, str(KOK / "scripts/analiz"))
import _muafiyet as MUAF  # noqa: E402  ⭐ T140: bağışlanan her öge sayılır
from tohum_guvenlik import tr_fold  # noqa: E402

# ─── 1. ZAMAN sözcükleri (kapalı sözlük) ───────────────────────────────────
# ⛔ İLK SÜRÜM ÇOK GÜRÜLTÜLÜYDÜ ve sebebi ölçüldü: yalın «bugün»/«dün»/«yarın»
# 33 kaydın çoğunda ateşliyordu, çünkü asistan KONUŞMANIN KENDİ GÜNÜNE atıf
# yapıyor (*«Bunu bugün sen yaptın»*) ve bunun için kullanıcının «bugün» demesi
# gerekmiyor. ⇒ Yalın gün adları ÇIKARILDI; yalnız BİLEŞİK, belirli zaman
# ifadeleri kaldı — onları model kendiliğinden getiremez.
ZAMAN = [
    "önceki gün", "geçen hafta", "geçen ay", "geçen yıl",
    "dün gece", "dün akşam", "dün sabah", "dün öğlen",
    "öğleden sonra", "akşamüstü", "gece yarısı", "sabaha karşı",
    "aynı akşam", "aynı gece", "aynı sabah", "aynı gün", "o akşam", "o gece",
    # ⭐ JUDGE KOŞUSUYLA BULUNAN DELİKLER (2026-09-17, v5-parti4). Kör bir judge
    # 8 uydurma dayanak buldu; üçü bu sözlükte YOKTU:
    #   #3  *«İkisi de aynı hafta içinde»*   → «aynı hafta» eksikti
    #   #26 *«sayıyı on dakika önce öğrendin»* → süre+önce kalıbı eksikti
    # ➡️ *Bir kapının kör noktaları ancak BAŞKA BİR OKUYUCU tarafından
    #    haritalanabilir; kapı kendi sözlüğünün dışını göremez.*
    "aynı hafta", "aynı ay", "o hafta", "geçen akşam", "geçen gece",
]
# ⭐ Süre + «önce» kalıbı: *«on dakika önce»*, *«iki saat önce»*. Sözlükle değil
# desenle aranıyor çünkü sayı sonsuz.
SURE_ONCE = re.compile(
    r"\b(bir|iki|üç|dört|beş|altı|yedi|sekiz|dokuz|on|yirmi|otuz|kırk|elli|yarım|"
    r"\d+)\s*(dakika|saat|gün|hafta|ay|yıl)\s*önce\b", re.I)
# ⚠️ «aynı akşam» / «o gece» ANAFORİKTİR: yapısı gereği bir ÖNCÜL ister. Öncül
# kullanıcının turunda varsa model yeni bir zaman GETİRMİYOR, var olanı işaret
# ediyor. ⛔ Ama sözlükten atılamazlar: 9 bayrağın 4'ü demirli, **5'i demirsiz**
# çıktı (2026-09-17 ölçümü) — atmak ayırt eden yarıyı kaybettirirdi.
# ⇒ Sözlükte kalıyor, DEMİR varsa muaf.
# ⛔⛔ İLK MUAFİYET ÇOK GENİŞ YAZILDI VE ÖLÇÜMDE YAKALANDI: "kullanıcı turunda
# HERHANGİ bir zaman demiri varsa muaf" kuralı, kullanıcının *«dün»* dediği bir
# kaydı asistanın *«aynı akşam»*ını akladı — oysa **akşam** bilgisini oraya
# model koymuştu. ⇒ Demir AYNI BİRİMDEN olmalı: *«akşam»* için akşam, *«gece»*
# için gece. Yalnız *«gün»* her demirle karşılanır (her demir bir günü belirler).
# ⛔ SÖZLÜĞE EKLERKEN MUAFİYETİ GÜNCELLEMEYİ UNUTTUM: «aynı hafta» ZAMAN'a
# eklendi ama ANAFORIK'e eklenmedi ve `v5-parti7 #46`'da yanlış pozitif üretti —
# kullanıcı *«geçen hafta»* demişti, yani öncül vardı.
# ➡️ *Bir sözlüğe öge eklemek, o ögenin muafiyetini de eklemek demektir;
#    ikisi ayrı yerde durduğu sürece biri eksik kalır.*
ANAFORIK = {tr_fold(a + b): tr_fold(b)
            for a in ("aynı ", "o ")
            for b in ("akşam", "gece", "sabah", "gün", "hafta", "ay")}
GUN_DEMIRI = [tr_fold(x) for x in      # ⚠️ liste de tr_fold'dan geçer (T73/T75/T76)
              ("bugün", "bu akşam", "bu gece", "bu sabah", "bu öğlen",
               "dün", "önceki gün", "o gün", "geçen gece")]

# ─── 2. KAYNAK ATFI: 2. tekil iyelik + tamlayan (kişi adları) ──────────────
KISI = ["doktor", "hekim", "terapist", "psikolog", "eş", "karı", "koca", "anne",
        "baba", "oğul", "kız", "torun", "kardeş", "arkadaş", "patron", "amir",
        "ustabaşı", "komşu", "avukat", "öğretmen", "müdür", "hoca",
        # ⭐ Judge koşusu: #36 *«Abinin hesabıyla denemiştin»* kaçtı çünkü
        # «abi» listede yoktu — «kardeş» vardı ama Türkçede akrabalık adları
        # tek bir sözcüğe indirgenmiyor.
        "abi", "ağabey", "abla", "dayı", "amca", "hala", "teyze", "yeğen",
        "kayınvalide", "kayınpeder", "gelin", "damat", "sevgili", "nişanlı"]
# «doktorunun», «eşinin», «annenin»: kök + (2.tekil iyelik) + tamlayan
ATIF = re.compile(
    r"\b(" + "|".join(KISI) + r")(un|ın|in|ün|n)?(un|ın|in|ün)\b", re.IGNORECASE)

# ⛔⛔ İKİNCİ KUSUR — ÖLÇÜLDÜ VE DAHA ÖNEMLİ: asistan kullanıcının sözünü
# yansıtırken KİŞİ EKİNİ ZORUNLU OLARAK DEĞİŞTİRİYOR (*«eşim»* → *«eşin»*,
# *«annem»* → *«annen»*). Dizge karşılaştırması bu yüzden DOĞRU davranışın
# tamamında ateşliyordu. ⇒ Karşılaştırma KÖK üzerinden yapılır: iyelik ve
# tamlayan ekleri iki taraftan da düşürülür.
# ➡️ Alıntı doğrulaması (model KOPYALAR) dizgeyle çalışır; yansıtma doğrulaması
#    (model DÖNÜŞTÜRMEK ZORUNDADIR) dizgeyle çalışmaz.
# ⚠️ Ek listesi ÖLÇÜMLE genişletildi: ilk sürümde yalın «-m» (annem) ve yönelme
# «-ya/-ye» (komşuya) yoktu ve ikisi de yanlış pozitif üretti.
# ⛔⛔ ÜÇÜNCÜ KUSUR — ÖLÇÜLDÜ. İlk yazımda ekler TEK BİR ZİNCİR sayılmıştı:
# hâl eki yalnız bir iyelik ekinin ARDINDAN soyulabiliyordu. Türkçede hâl eki
# doğrudan köke gelir ve bu alanın en sık kalıbı tam olarak öyle: *«doktora
# gittim»*. ⇒ `_kok("doktora")` = **"doktora"**, `_kok("doktorunun")` = "doktor"
# ve kapı kullanıcının kendi doktorunu ATFEDİLMİŞ sayıyordu.
# ⇒ İki ek sınıfı SIRAYLA ve BAĞIMSIZ soyuluyor: önce hâl, sonra iyelik.
_HAL = re.compile(r"(nin|nın|nun|nün|ne|na|ni|nı|nu|nü|ya|ye|yı|yi|yu|yü"
                  r"|yla|yle|den|dan|de|da|le|la|in|ın|un|ün|e|a|i|ı|u|ü)$")
_IYELIK = re.compile(r"(lar|ler)?(im|ım|um|üm|in|ın|un|ün|si|sı|su|sü|i|ı|u|ü|m|n)$")
# ⚠️ Ünsüz yumuşaması: *«psikolog»* → *«psikoloğun»*. Sondaki yumuşak ünsüz
# sert karşılığına çevrilir, yoksa aynı kelimenin iki hâli iki kök verir.
_YUMUSAMA = str.maketrans({"ğ": "g", "c": "ç", "d": "t"})


# ⛔⛔ **MUAFİYET YANLIŞ ŞEYE BAKIYORDU (T141'de bulundu, 2026-09-18'de kapatıldı).**
# Kural tamlayanın ARDILINA bakıyordu (*«işi»*, *«alanı»*) ama muafiyet §8b'nin
# MESLEK rolleri için yazılmıştı ⇒ *«sevgilinin işi»*, *«eşinin işi»*, *«annenin
# işi»* de muaf oluyordu. T141 bunu ölçmüş ve *«bugün bedeli sıfır ama sızıntı
# gerçek»* diye kaydetmişti.
# ⭐ Ölçüldü (bütün aday + yayımlanmış korpuslar): muafiyet beş tamlayanda ateşliyor
# — *«hekimin işi»* ×113, *«hekimin alanı»* ×53, *«hekiminin işi»* ×14,
# *«doktorunun alanı»* ×10 (dördü meslek) ve *«sevgilinin işi»* ×10 (meslek DEĞİL).
# ⇒ Muafiyet artık tamlayanın da MESLEK ROLÜ olmasını istiyor. **Net bedel: 0 yeni
#   bulgu** — muafiyeti kaybeden tek öge (*«sevgilinin»*) zaten kullanıcının turunda.
# ⚠️ Karşılaştırma `_kok_ortusu` ile yapılıyor, ikinci bir eşleştirme yazılmadan:
#   kök çıkarıcı TEK KATMAN kırpıyor (*«hekimin»* → `hek`, *«hekiminin»* → `hekim`)
#   ve düz küme üyeliği ikisini birden tutamıyordu.
MESLEK_KOKU = ("hekim", "doktor", "uzman", "danışman", "psikolog",
               "psikiyatrist", "terapist", "eczacı", "hemşire")
ROL_ARDILI = {tr_fold(x) for x in
              ("işi", "işleri", "alanı", "alanıdır", "kararı", "işidir",
               "bileceği", "işiydi", "işi;", "alanı;")}


def _kok(kelime: str) -> str:
    k = _IYELIK.sub("", _HAL.sub("", tr_fold(kelime)))
    return k[:-1] + k[-1:].translate(_YUMUSAMA) if k else k


def _kok_ortusu(oge_koku: str, kokler: set[str]) -> bool:
    """Köklerden biri ÖGENİN KÖKÜYLE ÖNEK ilişkisinde mi.

    ⚠️ Eşitlik değil önek aranıyor çünkü yukarıdaki soyucu AŞIRI ve
    DÜZENSİZ soyuyor (*«hekim»*→"hek", *«anne»*→"an", *«patron»*→"patro") ve
    aynı kelimenin iki çekimi iki farklı uzunlukta kök verebiliyor. Önek
    karşılaştırması bu asimetriyi soğuruyor.
    ⛔ BEDELİ: kapı GEVŞİYOR — *«kız»* kökü *«kızkardeşinin»*i de aklıyor.
    Zaten alt sınır ölçen bir kapı için kabul edilen bir bedel; kaçırdığı
    atıflar sayıyı DÜŞÜRÜR, uydurma ayrıntıyı VAR göstermez.
    """
    if len(oge_koku) < 2:
        return True                      # ⚠️ ayırt edici değil: işaretleme
    return any(len(k) >= 2 and (k.startswith(oge_koku) or oge_koku.startswith(k))
               for k in kokler)


def _kullanici_metni(r: dict) -> str:
    parcalar = [m.get("content", "") for m in r["messages"] if m["role"] == "user"]
    parcalar += [c.get("metin", "") for c in (r.get("context") or [])]
    return tr_fold(" \n ".join(parcalar))


def _kullanici_kokleri(r: dict) -> set[str]:
    return {_kok(k) for k in re.findall(r"\w+", _kullanici_metni(r))}


def _son_cevap(r: dict) -> str:
    return [m for m in r["messages"] if m["role"] == "assistant"][-1]["content"]


# ⛔ İSİM ÇAKIŞMASI: `datasets/v0.0.8/train.jsonl` ile `datasets/v0.0.9/train.jsonl`
# ikisi de `…-train.json` yazıyordu ⇒ ikinci koşu birincinin raporunu siliyor ve
# dosya adı hangi sürüm olduğunu söylemiyordu. (JSON içindeki `girdi` + sha bunu
# kurtarıyordu ama ad yanıltıyordu.) ⇒ `datasets/` altındaki girdiler SÜRÜMLE adlanır.
def _rapor_adi(p: Path) -> str:
    return f"{p.parent.name}-{p.stem}" if p.parent.parent.name == "datasets" else p.stem

def main(yol: str) -> int:
    p = Path(yol) if Path(yol).is_absolute() else KOK / yol
    kayitlar = [json.loads(s) for s in p.read_text(encoding="utf-8").splitlines() if s.strip()]
    bulgu = []
    for r in kayitlar:
        kaynak = _kullanici_metni(r)
        cevap = _son_cevap(r)
        c_fold = tr_fold(cevap)
        for m in SURE_ONCE.finditer(cevap):
            # ⛔ `v5-parti8 #45`: cevap *«Üç ay önce»*, kullanıcı *«üç ay oldu»* —
            # aynı süre, başka kalıp. Tam dizge araması bunu uydurma sandı.
            # ➡️ *Bir zaman ifadesi uydurma değildir; ONU TAŞIYAN SÜRE uydurma
            #    olabilir. Aranacak şey kalıp değil, süre + birim.*
            sure_birim = tr_fold(m.group(1) + " " + m.group(2))
            if sure_birim in kaynak:
                MUAF.yaz("sure_birim_eslesme", r, m.group(0), sure_birim)
                continue
            if tr_fold(m.group(0)) not in kaynak:
                bulgu.append({"parti_sira": r["gen_meta"]["parti_sira"],
                              "tip": "zaman", "oge": m.group(0)})
        for z in ZAMAN:
            zf = tr_fold(z)
            if zf not in c_fold or zf in kaynak:
                continue
            birim = ANAFORIK.get(zf)
            if birim and (birim in kaynak if birim != tr_fold("gün")
                          else any(d in kaynak for d in GUN_DEMIRI)):
                # ⚠️ öncül kullanıcının turunda, aynı birimden
                MUAF.yaz("anaforik_demir", r, z, birim)
                continue
            bulgu.append({"parti_sira": r["gen_meta"]["parti_sira"],
                          "tip": "zaman", "oge": z})
        kokler = _kullanici_kokleri(r)
        for m in ATIF.finditer(cevap):
            oge = m.group(0)
            # ⭐⭐ NET BAĞIŞ: bir muafiyet ancak öge ZATEN bulgu olacakken anlamlıdır.
            # Kök örtüşmesi tutan bir ögeyi «muaf tuttum» diye saymak defteri şişirir
            # ve gerçekten saklanan kusurun üstünü örter (T140'ın kendi dersi).
            _net = not _kok_ortusu(_kok(oge), kokler)
            # ⚠️ TÜR ADLANDIRMA muaf: «hekimin işi», «hekimin alanı» bir ATIF
            # değil, §8b'nin İSTEDİĞİ yönlendirme biçimidir. Tamlayan ekini
            # izleyen sözcük bir "rol" adıysa atıf sayılmaz.
            # ⭐ BELİRSİZ ARTİKEL MUAFİYETİ (2026-09-17, v5-parti6'da ölçüldü):
            # *«bunu BİR hekimin bilmesi gerekir»* bir ATIF DEĞİL — «bir» tamlamayı
            # belirsiz kılıyor, yani kullanıcının kendi hekimini değil herhangi
            # birini gösteriyor. Atıf ancak BELİRLİ olduğunda atıftır.
            onceki = re.findall(r"\w+", cevap[max(0, m.start() - 12):m.start()])
            if onceki and tr_fold(onceki[-1]) == tr_fold("bir"):
                MUAF.yaz("belirsiz_artikel" + ("" if _net else " [ZATEN YERDE]"), r, oge, "bir " + oge)
                continue
            ardil = re.findall(r"\w+", cevap[m.end():m.end() + 20])   # ⚠️ noktalama
            # ⛔⛔ İLK YAZIMDA BU MUAFİYET HİÇ ATEŞLEMEDİ ve sebebi T73/T75/T76'nın
            # ailesi: liste düz ASCII yazılmıştı ("isi") ama `tr_fold("işi")`
            # **"ışı"** veriyor (i-sınıfı i'yi ı'ya çeker, ş korunur). ⇒ Desen ve
            # metin AYNI katlamadan geçmek zorunda; liste de tr_fold'dan geçiriliyor.
            _meslek = _kok_ortusu(_kok(oge), {_kok(x) for x in MESLEK_KOKU})
            if ardil and tr_fold(ardil[0]) in ROL_ARDILI and _meslek:
                MUAF.yaz("rol_adlandirma_bitisik" + ("" if _net else " [ZATEN YERDE]"), r, oge, oge + " " + ardil[0])
                continue
            # ⭐⭐ BAĞLAÇLI TÜR ADLANDIRMA (2026-09-17, eski katmanlarda ölçüldü).
            # *«…yapmak HEKİMİN ya da ruh sağlığı alanında çalışan bir uzmanın
            # İŞİ»* — rol sözcüğü tamlayanın hemen ardında değil, BAĞLACIN öbür
            # ucunda duruyor ve bitişik ardıla bakan muafiyet ateşlemiyordu.
            # Aynı cümle iki ayrı partide (v5-parti3 #27, v4-parti2 #10) yanlış
            # pozitif üretti.
            # ➡️ *Bir muafiyeti bitişikliğe bağlamak, Türkçenin sıralı tamlama
            #    yapısını görmezden gelmektir: «A'nın ya da B'nin işi»nde rol
            #    sözcüğü A'ya da aittir ama A'dan uzaktadır.*
            # ⛔ Pencere DAR ve bağlaç ZORUNLU: yalnız «ya da / veya / ile /
            #   virgül» geçen bir ara metinde geçerli ⇒ «hekimin bilmesi gereken
            #   bir şey» gibi gerçek atıflar muaf kalmaz.
            _ara = cevap[m.end():m.end() + 90]
            if (_meslek and re.search(r"\b(ya da|veya|ile)\b|,", _ara)
                    and any(tr_fold(w) in ROL_ARDILI for w in re.findall(r"\w+", _ara))):
                MUAF.yaz("rol_adlandirma_baglacli" + ("" if _net else " [ZATEN YERDE]"), r, oge, oge + " " + _ara)
                continue
            if not _kok_ortusu(_kok(oge), kokler):
                bulgu.append({"parti_sira": r["gen_meta"]["parti_sira"],
                              "tip": "kaynak_atfi", "oge": oge})
    kayit_sayisi = len({b["parti_sira"] for b in bulgu})
    ozet = {"tarih": "2026-09-17", "girdi": str(p.relative_to(KOK)),
            "girdi_sha256_16": hashlib.sha256(p.read_bytes()).hexdigest()[:16],
            "kayit": len(kayitlar), "isaretli_kayit": kayit_sayisi,
            "bulgu": bulgu,
            # ⭐ T140: kapının BAĞIŞLADIKLARI da raporlanır — sayılmayan muafiyet denetlenemez
            "muafiyet_ozeti": MUAF.ozet(), "muafiyet": list(MUAF.DEFTER)}
    cikti = KOK / f"reports/analiz/2026-09-17-zaman-kaynak-{_rapor_adi(p)}.json"
    cikti.write_text(json.dumps(ozet, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(kayitlar)} kayıt · ⛔ işaretli {kayit_sayisi} kayıt / {len(bulgu)} öge")
    for b in bulgu:
        print(f"   #{b['parti_sira']:>2} [{b['tip']:<11s}] «{b['oge']}»")
    print(f"→ {cikti.relative_to(KOK)}")
    return 1 if bulgu else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "data/candidates/v5-parti3.v2.jsonl"))
