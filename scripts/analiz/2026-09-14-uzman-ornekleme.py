"""Uzman değerlendirmesi için 70 kayıtlık üretim planı (K27, seçenek B).

⚠️ ÇIKTI DONDURULDU (2026-09-14). data/expert_sample/plan-70.jsonl üretildi ve
kayıtlar bu plana göre ELLE yazılmaya başlandı. Betik belirlenimli, ama KODU
değiştirip yeniden koşmak tohum→sıra atamasını kaydırır ve yazılmış kayıtlarla
uyumu bozar. Değişiklik gerekiyorsa: plan dosyasına dokunma, sapmayı üretim
betiğindeki DEGISIM tablosuna yaz.


Girdi : data/seeds.jsonl
Çıktı : data/expert_sample/plan-70.jsonl  +  reports/analiz/2026-09-14-uzman-ornekleme.md

Kural:
  · v0.0.1'de kullanılan 20 tohum ve ablasyon/üstsınır deneylerinde kullanılan 12 tohum HARİÇ
  · senaryo == kriz ve risk == cok_yuksek HARİÇ (AGENTS Kural 3 — uzman onayı bekliyor)
  · senaryo ataması üretim zamanı kararıdır (K37): 'belirsiz' tohumlar hedef arketipe atanır
  · mesaj biçimi dağılımı K42 (kısa %40 / orta %35 / uzun %25, register bağımsız)
"""
import collections
import hashlib
import json
import pathlib
import random

KOK = pathlib.Path(__file__).resolve().parents[2]
SEEDS = KOK / "data/seeds.jsonl"
CIKTI_JSONL = KOK / "data/expert_sample/plan-70.jsonl"
CIKTI_RAPOR = KOK / "reports/analiz/2026-09-14-uzman-ornekleme.md"
def _muhur_kapisi(yol, icerik) -> None:
    """Dondurulmuş/mühürlü çıktıyı sessizce yeniden yazmayı engeller.

    ⛔ 2026-09-16: `date.today()` yüzünden bu betiği ertesi gün koşmak dondurulmuş
    dosyanın SHA'sını değiştiriyordu ve hiçbir yerde uyarı çıkmıyordu (K126).
    Tarih artık sabit; kapı ikinci savunma hattı — içerik BAŞKA bir sebeple
    kayarsa da duruyor.
    """
    import sys as _s
    ham = icerik if isinstance(icerik, bytes) else icerik.encode("utf-8")
    if yol.exists() and yol.read_bytes() != ham and "--yenile" not in _s.argv:
        _s.exit(f"⛔ MÜHÜR: {yol.name} mevcut içerikten FARKLI üretildi ve "
                f"üzerine YAZILMADI.\n   Kasten yenilemek için: --yenile")
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_bytes(ham)
RASTGELE = random.Random(27)

# ── hedef bileşim ────────────────────────────────────────────────────────────
SENARYO_HEDEF = {
    "ambivalans": 7, "rol_siniri": 6, "nazikce_karsi_cikma": 5, "inkar": 6,
    "kayma_nuks": 5, "durtu": 5, "farkindalik": 4, "motivasyon": 4,
    "hedef_belirleme": 4, "anlasilmama": 4, "bilmiyorum_cikmazi": 4,
    "discord": 3, "bilgilendirme": 3, "hukuki_kaygi": 3, "borc_finansal": 3,
    "kayip_kovalama": 2, "kutlama": 2,
}
# sanrili_soylem YOK: 2.240 tohumun hiçbiri bu arketipi desteklemiyor (0 eşleşme,
# 2026-09-14 taraması). Dayanaksız arketip üretmek tohumda olmayan bir klinik tablo
# uydurmaktır (Kural 3). Yuva `inkar`a devredildi; kapsama açığı Faz 4'e kaldı.

# İçerik gerektiren arketiplerin tohumları ELLE seçildi — anahtar kelime eşleşmesi
# yanlış pozitif üretiyordu (ör. "işaret" → yoksunluk titremesi metnine sanrili_soylem,
# "kaybett" → okul taksiti metnine kayip_kovalama). Seçim kaydı: bu tablo.
PIN = {
    "ea6c9f5150c47721": "hukuki_kaygi",   # duruşmaya kadar içme pazarlığı
    "c5f83570ad5e7533": "hukuki_kaygi",   # gözetimli görüş kararı
    "3aff5f2e8332dbde": "hukuki_kaygi",   # işten çıkarma + boşanma davası
    "d8811df83e8ac181": "borc_finansal",  # icra kâğıdı, işsizlik
    "83d113fe667b9591": "borc_finansal",  # ikinci kredi başvurusu, onay tuşunda
    "13efd46b95db880d": "borc_finansal",  # 130 bin icra, "bir gece daha"
    "99e3ae24c158d8d9": "kayip_kovalama", # "bir el daha tutarsa kapatırım"
    "1e6feffa0d04795c": "kayip_kovalama", # tefeci parasını iki katına çıkarma
    "8c7db2f8051501ef": "kutlama",        # proje savunması geçti, kutlama daveti
    "e2c2f379aadc1dc8": "kutlama",        # dörtten üçe düşürdü
    "887c8c65e9b17e44": "bilgilendirme",  # KOAH okudu, kafası karıştı
    "f83792a333952b2f": "bilgilendirme",  # vape "yanma yok katran yok"
    "136fc403c3db8231": "bilgilendirme",  # "bu yaşta bırakırsan ölürsün" miti
}
TUR_HEDEF = {"tutun": 18, "alkol": 18, "kumar": 16, "receteli_ilac": 12, "dijital": 6}
# senaryo → yalnızca bu bağımlılık türleriyle anlamlı
SENARYO_TUR_KISITI = {
    "kayip_kovalama": {"kumar"},
    "borc_finansal": {"kumar", "alkol"},
    "hukuki_kaygi": {"alkol", "kumar", "receteli_ilac"},
}

# İçerik gerektiren arketipler: tohum metninde dayanağı yoksa o arketip ATANMAZ.
# Gerekçe: dayanağı olmayan arketip, tohumda bulunmayan bir öğe uydurmak demektir
# (AGENTS Kural 3). Serbest arketipler (ambivalans, inkar, farkindalik ...) her
# tohumdan geliştirilebilir — K37: senaryo ataması üretim zamanı kararıdır.
SENARYO_ANAHTAR = {
    "hukuki_kaygi": ["mahkeme", "dava", "savcı", "tck", "denetimli", "adli", "polis",
                     "ceza", "avukat", "kovuşturma", "karakol", "ehliyet", "trafik",
                     "zorunlu rehabilitasyon", "hüküm"],
    "borc_finansal": ["borç", "tefeci", "kredi", "icra", "faiz", "haciz", "taksit",
                      "maaşım", "ödeyemiyorum", "batt", "kart limiti"],
    "kayip_kovalama": ["kaybett", "geri almak", "geri kazan", "açığı kapat", "son bir",
                       "kovala", "zararı kapat", "kaybımı"],
    "sanrili_soylem": ["sistemi çözdüm", "algoritma", "bana özel", "işaret", "kesin kazanç", "şifresini", "formül", "garanti"],
    # davranış gerektirenler: arketip tohumda GÖRÜNÜR bir hamle istiyor
    "rol_siniri": ["ne yapmalıyım", "ne yapayım", "sen söyle", "sen karar", "tarafsız",
                   "haklı mıyım", "bir formül", "bir sistem", "bir plan ver", "reçete",
                   "önerir misin", "tavsiye et", "doktor musun", "teşhis", "kaç gün",
                   "kaç mg", "bana bir yol"],
    "durtu": ["canım çekiyor", "içimden geçiyor", "elim gidiyor", "parmağım", "dayanamıyorum",
              "içim gidiyor", "indirsem", "yüklesem", "açsam mı", "şu an istiyorum",
              "ayağım kendiliğinden", "elim uzandı", "çekiyor canım"],
    "discord": ["sen de mi", "boşver", "anlamıyorsun", "kapatıyorum", "saçmala",
                "işe yaramıyor", "robot", "makine", "ne anlarsın", "bırak şimdi",
                "boş konuşma", "nutuk"],
    "anlasilmama": ["anlamıyor", "anlatamıyorum", "anlamaz", "kimse anlamıyor",
                    "beni anlamıyorsun", "anlaşılmıyorum"],
    "bilmiyorum_cikmazi": ["bilmiyorum", "kafam karışık", "karar veremiyorum",
                           "ne yapacağımı bilmiyorum", "emin değilim"],
    "kutlama": ["gün oldu", "ay oldu", "hiç içmedim", "hiç oynamadım", "başardım",
                "bir yıl oldu", "kutla", "hiç sigara"],
    "bilgilendirme": ["nedir", "nasıl olur", "doğru mu", "ne yapar", "zararlı mı",
                      "öğrenmek istiyorum", "bilgi", "gerçekten", "işe yarar mı"],
}


# ⚠️ Metadata ile kriz elemek YETMİYOR: `senaryo != kriz` etiketli tohumların içinde
# açık intihar düşüncesi taşıyanlar var (2026-09-14'te bulundu). İçerik taraması şart.
KRIZ_ANAHTAR = [
    "yaşamak istemiyorum", "ölmek istiyorum", "intihar", "canıma kıy", "kendimi asa",
    "kendime zarar", "bitirmek istiyorum", "son vermek istiyorum", "uyanmasam",
    "uyanmak istemiyorum", "yaşamaya değmez", "hayatıma son", "bileğimi", "hapları içt",
    "yok olmak istiyorum", "ölsem", "öldürmek istiyorum kendimi", "yük oluyorum",
    "bensiz daha iyi", "dayanamıyorum artık", "kurtulmak istiyorum bu hayattan",
    # tıbbi aciliyet / doz aşımı sonrası — kriz komşusu, aynı uzman onayına bağlı
    "acil servis", "acilde", "ambulans", "mide yıkan", "yoğun bakım", "doz aşımı",
    "aşırı doz", "taburcu", "entübe", "komaya",
]


def kriz_icerigi(tohum):
    metin = (tohum["user_message"] + " " + tohum.get("scenario_context", "")).lower()
    return [a for a in KRIZ_ANAHTAR if a in metin]


def _uygun(tohum, senaryo):
    anahtarlar = SENARYO_ANAHTAR.get(senaryo)
    if not anahtarlar:
        return True
    metin = (tohum["user_message"] + " " + tohum.get("scenario_context", "")).lower()
    return any(a.strip() in metin for a in anahtarlar)

BICIM_HEDEF = {"kisa": 28, "orta": 25, "uzun": 17}      # K42
REGISTER_BOZUK = 14                                     # noktalamasız / yazım hatalı (%20)
COK_TURLU = 14                                          # %20
CONTEXT_VAR = 10                                        # Eksen 4 (2'si yetersiz bağlam)


def sha256(yol):
    h = hashlib.sha256()
    h.update(yol.read_bytes())
    return h.hexdigest()


def kullanilmis_tohumlar(tohumlar):
    """v0.0.1 (20) + ablasyon/üstsınır (12) tohumları."""
    kaynak_id = set()
    for satir in open(KOK / "data/candidates/v0.0.1.jsonl"):
        kaynak_id.update(json.loads(satir).get("source_ids") or [])
    kullanilan = {t["seed_id"] for t in tohumlar if t["source_id"] in kaynak_id}
    for yol in ["reports/analiz/prompt-dili-ablasyonu/generations.jsonl",
                "reports/analiz/thinking-dili-ogrenilebilirlik/dar-lora.jsonl"]:
        for satir in open(KOK / yol):
            kayit = json.loads(satir)
            if "seed_id" in kayit:
                kullanilan.add(kayit["seed_id"])
    return kullanilan


def sec(tohumlar):
    kullanilan = kullanilmis_tohumlar(tohumlar)
    havuz = [t for t in tohumlar
             if t["seed_id"] not in kullanilan
             and t["meta"].get("senaryo") != "kriz"
             and t["meta"].get("risk_seviyesi") != "cok_yuksek"
             and not kriz_icerigi(t)]
    RASTGELE.shuffle(havuz)

    tur_kalan = dict(TUR_HEDEF)
    secilen, alinan = [], set()

    # 1) elle sabitlenen tohumlar
    index = {t["seed_id"]: t for t in havuz}
    for seed_id, senaryo in PIN.items():
        t = index.get(seed_id)
        if t is None:
            raise SystemExit(f"PIN tohumu havuzda yok: {seed_id}")
        alinan.add(seed_id)
        tur_kalan[t["meta"]["bagimlilik_turu"]] -= 1
        secilen.append({"tohum": t, "hedef_senaryo": senaryo})

    # senaryo yuvalarını kısıtlı olanlardan başlayarak doldur
    import collections as _c
    sabit = _c.Counter(PIN.values())
    yuvalar = []
    for senaryo, adet in SENARYO_HEDEF.items():
        yuvalar.extend([senaryo] * (adet - sabit.get(senaryo, 0)))
    yuvalar.sort(key=lambda s: (s not in SENARYO_ANAHTAR,
                                len(SENARYO_TUR_KISITI.get(s, TUR_HEDEF))))

    for senaryo in yuvalar:
        izinli = SENARYO_TUR_KISITI.get(senaryo, set(TUR_HEDEF))
        # kotası en çok kalan tür önce
        # ⛔ Eşitlik bozucu ad ZORUNLU: `izinli` bir KÜME, `sorted` kararlı — eşit
        # kotada sıra kümenin yineleme sırasına düşer, o da PYTHONHASHSEED'e bağlıdır.
        # Tohum (`random.Random(27)`) bunu KAPATMAZ: her koşu farklı 70'lik plan üretti.
        tur_sirasi = sorted(izinli, key=lambda t: (-tur_kalan.get(t, 0), t))
        aday = None
        for tur in tur_sirasi:
            if tur_kalan.get(tur, 0) <= 0:
                continue
            # tohumun kendi senaryosu hedefle uyuşuyorsa ya da 'belirsiz' ise tercih et (K37)
            for tercih in (senaryo, "belirsiz", None):
                for t in havuz:
                    if t["seed_id"] in alinan or t["meta"]["bagimlilik_turu"] != tur:
                        continue
                    if tercih is not None and t["meta"].get("senaryo") != tercih:
                        continue
                    if not _uygun(t, senaryo):
                        continue
                    aday = (t, tur)
                    break
                if aday:
                    break
            if aday:
                break
        if not aday:
            raise SystemExit(f"yuva doldurulamadı: {senaryo}")
        t, tur = aday
        alinan.add(t["seed_id"])
        tur_kalan[tur] -= 1
        secilen.append({"tohum": t, "hedef_senaryo": senaryo})
    return secilen


def uretim_plani(secilen):
    """Her kayda mesaj biçimi, register, tur yapısı, context modu atar."""
    n = len(secilen)
    sira = list(range(n))
    RASTGELE.shuffle(sira)

    bicim = ["kisa"] * BICIM_HEDEF["kisa"] + ["orta"] * BICIM_HEDEF["orta"] + ["uzun"] * BICIM_HEDEF["uzun"]
    register = ["bozuk"] * REGISTER_BOZUK + ["duzgun"] * (n - REGISTER_BOZUK)
    tur_yapisi = ["cok_turlu"] * COK_TURLU + ["tek_tur"] * (n - COK_TURLU)
    context = ["yetersiz"] * 2 + ["var"] * (CONTEXT_VAR - 2) + ["yok"] * (n - CONTEXT_VAR)
    for liste in (bicim, register, tur_yapisi, context):
        RASTGELE.shuffle(liste)

    for yeni_sira, i in enumerate(sira):
        kayit = secilen[i]
        kayit["plan"] = {
            "mesaj_bicimi": bicim[yeni_sira],
            "register": register[yeni_sira],
            "tur_yapisi": tur_yapisi[yeni_sira],
            "context_modu": context[yeni_sira],
        }
    # uzmana gidecek sıra da karıştırılmış olsun
    return [secilen[i] for i in sira]


def rapor(plan, seeds_hash):
    sat = ["# Uzman örneklemi — 70 kayıtlık üretim planı", "",
           f"**Girdi:** `data/seeds.jsonl` · SHA256 `{seeds_hash}`  ",
           "**Betik:** `scripts/analiz/2026-09-14-uzman-ornekleme.py` · rastgelelik tohumu 27  ",
           "**Tarih:** 2026-09-14  ",
           "**Karar:** K27 (seçenek B — kayıtların tamamı kendi pipeline'ımızdan)", "",
           "Hariç tutulanlar: v0.0.1'in 20 tohumu · ablasyon/üstsınır deneylerinin 12 tohumu ·",
           "`senaryo == kriz` · `risk_seviyesi == cok_yuksek` (AGENTS Kural 3 — uzman onayı bekliyor).", ""]
    for ad, anahtar in [("Hedef senaryo", None), ("Bağımlılık türü", "bagimlilik_turu"),
                        ("Yaş grubu", "yas_grubu"), ("Risk seviyesi", "risk_seviyesi"),
                        ("Motivasyon evresi", "motivasyon_evresi")]:
        if anahtar is None:
            sayac = collections.Counter(k["hedef_senaryo"] for k in plan)
        else:
            sayac = collections.Counter(k["tohum"]["meta"].get(anahtar) for k in plan)
        sat += [f"## {ad}", "", "| Değer | Adet |", "|---|---:|"]
        sat += [f"| {d} | {a} |" for d, a in sayac.most_common()]
        sat += [""]
    for ad, anahtar in [("Mesaj biçimi (K42)", "mesaj_bicimi"), ("Yazım register'ı", "register"),
                        ("Tur yapısı", "tur_yapisi"), ("Context modu (Eksen 4)", "context_modu")]:
        sayac = collections.Counter(k["plan"][anahtar] for k in plan)
        sat += [f"## {ad}", "", "| Değer | Adet |", "|---|---:|"]
        sat += [f"| {d} | {a} |" for d, a in sayac.most_common()]
        sat += [""]
    return "\n".join(sat) + "\n"


def main():
    tohumlar = [json.loads(s) for s in open(SEEDS)]
    plan = uretim_plani(sec(tohumlar))
    satirlar = []
    if True:
        for i, k in enumerate(plan, 1):
            satirlar.append(json.dumps({
                "sira": i,
                "seed_id": k["tohum"]["seed_id"],
                "source_id": k["tohum"]["source_id"],
                "hedef_senaryo": k["hedef_senaryo"],
                "plan": k["plan"],
                "meta": k["tohum"]["meta"],
                "user_message": k["tohum"]["user_message"],
                "scenario_context": k["tohum"]["scenario_context"],
            }, ensure_ascii=False) + "\n")
    # ⛔ ÇIKTI DONDURULDU (başlıktaki nota bak): plan-70 uzmana gönderildi ve
    # puanlandı. Sessizce yeniden yazmak, uzman puanlarını BAŞKA bir plana bağlar.
    _muhur_kapisi(CIKTI_JSONL, "".join(satirlar))
    _muhur_kapisi(CIKTI_RAPOR, rapor(plan, sha256(SEEDS)))
    print(f"{len(plan)} kayıt planlandı → {CIKTI_JSONL}")


if __name__ == "__main__":
    main()
