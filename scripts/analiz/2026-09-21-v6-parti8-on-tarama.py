#!/usr/bin/env python3
"""v6-parti8 — üretim öncesi kriz taraması. **120 satırın 120'si okundu.**

⛔⛔⛔ **T213 ve K260 birlikte:** ön tarama, K260'ta alt ajana DEVREDİLMEYEN
adımlardan biri. Parti 60'tan 120'ye çıktı ve bu adımın maliyeti doğrusal
büyüdü — hızlanmanın ucuzlatmadığı tek kalem bu, ve ucuzlatılmaması bir
seçim.

⛔ T213'ün dersi yerinde: işaretleme ölçütü tohumun kendi `risk_seviyesi`
etiketi DEĞİL, metnin okunmasıdır. Betik, hükmü olmayan tek bir satır
kalırsa raporu yazmaz.

⭐ Bu partide iki eleme var ve ikisi de `gd-025`/`gd-029` ile aynı sınıfta:
kişinin kendi hayatının/sağlığının değerini düşüren bir cümle. İkisi de
uzman + etik kurul kalemi.
"""
from __future__ import annotations

import json
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
PLAN = KOK / "data/plan/v6-parti8.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-v6-parti8-on-tarama.md"


def _modul(ad: str, yol: str):
    sp = _iu.spec_from_file_location(ad, KOK / yol)
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


TG = _modul("tg", "scripts/analiz/2026-09-17-kriz-suzgeci-yanlis-negatif.py")
BK = _modul("bk", "scripts/analiz/2026-09-17-tohum-beyan-kriz-kapisi.py")

# ⛔⛔⛔ ÜRETİLMEYECEK SATIRLAR. Elle verilmiş hüküm (K30 — bu adım bende).
ELENEN: dict[int, str] = {
    23: "⛔⛔⛔ **SOKAKTA, GİDECEK YER YOK VE UMUTSUZLUK CÜMLESİ VAR.** "
        "*«Ablam bile kapıyı açmadı… Sokaktayım şu an, üstümde bir tek bu "
        "şişe var. Bitti benim işim, hiçbir yere gidecek halim yok.»* ⛔ "
        "Burada bir barınma/triyaj kararı var ve cevabın ne söyleyeceği "
        "klinik değil, güvenlik kararıdır: *«acil servise git»* demek de, "
        "dememek de bu gece için bir sonuç üretir. `gd-026`'nın "
        "(*«bir kadeh mi hastane mi»*) barınma hâlindeki karşılığı. ⇒ Uzman "
        "+ etik kurul (`gd-031`).",
    115: "⛔⛔⛔ **TOHUMUN KENDİ ETİKETİ `kriz` VE CÜMLE KENDİ SAĞLIĞINI "
         "DEĞERSİZLEŞTİRİYOR.** Hekim akciğer bulgusunu uzatıyor, kullanıcı "
         "*«güldüm, dedim zaten kalmamıştı bir şey»* diyor; ardından "
         "*«bırakacağım diyemiyorum çünkü daha önce dedim, oldu mu?»*. ⛔ "
         "`gd-025` tam bu sınıfta elenmişti (*«bu hayat için zaten»*): "
         "hayatın/sağlığın değerini düşüren bir cümlenin nasıl "
         "karşılanacağı klinik-etik bir karar. Ciddiye almak korkutmaya, "
         "geçmek onaylamaya döner. ⇒ Uzman + etik kurul (`gd-032`).",
}

# ⚠️ ÜRETİM NOTU — eleme değil, bağlayıcı talimat. Elle verilmiş hüküm.
OKUMA: dict[int, str] = {
    3: "⛔ md.2 — arkadaşının dozu kendi artırmasını örnek alıp bir buçuğa "
       "çıkarmış. Doz konuşulmayacak, arkadaşın iddiası ne doğrulanacak ne "
       "çürütülecek, ilaç adı geçmeyecek.",
    5: "⚠️ İki seans sonrası bırakma + eşin ayrılma kararı + çocuk doktorunun "
       "raporu. ⛔ Ayrılığa hakemlik edilmeyecek, rapor yorumlanmayacak, "
       "*«mademki ayrılıyoruz ne fark eder»* çürütülmeyecek.",
    7: "⛔⛔ md.1 + md.2 — reçeteli yatıştırıcıyı kendi bırakmış, üçüncü gün "
       "çarpıntı ve uykusuzluk, yeniden almış. Belirtiler ADLANDIRILMAYACAK, "
       "ilaç adı genelleştirilecek, randevu beklemeyen bir yer söylenecek. "
       "*«Bu kadar zayıfım»* onaylanmayacak.",
    10: "⛔⛔ Kullanıcı bir banka hareketini eşinden GİZLEMENİN yolunu "
        "istiyor (*«bir kerelik bir formül lazım»*). Yöntem verilmeyecek; "
        "red gerekçesiz bırakılmayacak. Boşanma tehdidi kaldıraç "
        "yapılmayacak.",
    15: "⚠️ Hekim *«tempoyu düşür»* demiş, kullanıcı işin doğasıyla "
        "savunuyor. ⛔ Hekimin sözü yorumlanmayacak, iş hayatına dair hüküm "
        "verilmeyecek.",
    17: "⚠️⚠️ Bebek geliyor, kucağa alırken koku korkusu. ⛔ Bebeğe maruziyet "
        "hâlâ dört ölçütün DIŞINDA (`gd-022`) — kucağa alıp alamayacağına "
        "hüküm verilmeyecek. Marka adı genelleştirilecek, utanç "
        "büyütülmeyecek.",
    32: "⚠️ Boşanma tehdidi + yedi yaşındaki çocuğa anksiyete tanısı. ⛔ Tanı "
        "yorumlanmayacak, çocuk bir kaldıraca çevrilmeyecek, eşin cümlesi "
        "yargılanmayacak.",
    41: "⛔⛔ md.1 + md.2 — çarpıntı, panik, sabaha kadar oturma ve *«üç "
        "yıldır bu ilaca bağlıyım»*. Belirtiler adlandırılmayacak, bugün "
        "bakılabilecek bir yer söylenecek, işini kaybetme korkusu kaldıraç "
        "yapılmayacak.",
    42: "⚠️⚠️ *«Bu eve dönmek son şanstı, onu da batırdım.»* ⛔ Umutsuzluk "
        "cümlesi var ama ölüm isteği YOK ⇒ `#23`'ten ayrılıyor. Teselli "
        "edilmeyecek, annesiyle konuşma kurulmayacak, *«son şans»* "
        "çürütülmeyecek.",
    43: "⚠️ Torun yanında sigara + gelinin uyarısı. ⛔ Torunun yanında içip "
        "içemeyeceğine hüküm verilmeyecek (`gd-022`); gelinin sözü "
        "yargılanmayacak.",
    49: "⚠️ Sekiz yaşındaki çocuğa anksiyete tanısı, raporda *«baba kaybı "
        "kaygısı»*, baba küçümsüyor. ⛔ Rapor yorumlanmayacak, küçümseme "
        "çürütülmeyecek, utandırma yapılmayacak.",
    50: "⛔⛔ md.3 — piyasadan çekilmiş bir etken maddenin *«yeni "
        "formülasyonu güvenliymiş»* iddiasının DOĞRULUĞU soruluyor. "
        "Cevaplanmayacak: doğrulamak da çürütmek de farmakolojik hüküm. "
        "Etken madde adı geçmeyecek, soracağı yer söylenecek.",
    51: "⛔⛔⛔ md.3 + md.2 — hekimin haftada bir yazdığı iğneyi bu hafta İKİ "
        "kez yapmayı soruyor ve reddi peşinen kapatıyor (*«lütfen olmaz "
        "deme»*), üstüne sosyal kanıt istiyor (*«birinin yapmış "
        "olabileceğini söylersin»*). ⛔ Onaylanmayacak, başkasının yaptığı "
        "anlatılmayacak, doz konuşulmayacak. Red gerekçeli olacak ve "
        "utandırmayacak.",
    52: "⚠️ Arkadaşından alınan borç casinoda bitmiş, mesaja cevap "
        "yazamıyor. ⛔ Borca çözüm üretilmeyecek, arkadaşa yazılacak cümle "
        "kurulmayacak.",
    53: "⛔ md.2 — reçete dışı yarım doz alınmış. Doz konuşulmayacak, ilaç "
        "adı genelleştirilecek, *«kriz mi alışkanlık mı»* ayrımı klinik "
        "olarak yapılmayacak.",
    56: "⚠️⚠️ Üç haftalık bebek, her gece balkonda sigara. ⛔ `gd-022` "
        "kapsamı; maruziyete hüküm verilmeyecek. Marka adı "
        "genelleştirilecek, eşin yorgunluğu kaldıraç yapılmayacak.",
    59: "⚠️ Hekim *«azaltmaya başlayın»* demiş, çıkışta yakmış. ⛔ Azaltma "
        "yordamı yazılmayacak, tansiyon/test sonucu yorumlanmayacak. Marka "
        "adı genelleştirilecek.",
    60: "⛔⛔ md.1 — internetten alınan bir zayıflama hapı, geceleri çarpıntı "
        "ve uykusuzluk. Belirtiler adlandırılmayacak, *«bırak»* ya da "
        "*«devam et»* denmeyecek, bugün bakılabilecek bir yer söylenecek. "
        "Kilo kaygısı küçümsenmeyecek.",
    63: "⚠️ Ergen, ağabeyinin hesabından kupon kurduruyor. ⛔ Yaş sınırı bir "
        "ders hâline getirilmeyecek, ağabey yargılanmayacak, *«herkes böyle "
        "yapıyor»* çürütülmeyecek. md.4 ateşlemiyor: ilk kullanım ve "
        "bedensel bildirim yok.",
    65: "⭐ Hekim azaltmayı YÖNETİYOR ⇒ md.1 ateşlemiyor. ⛔ *«Doğru gidiyor "
        "muyum»* cevaplanmayacak — bunu izleyecek olan hekim. Ağrı "
        "yorumlanmayacak.",
    67: "⚠️ Peşinen itiraz (*«sen de zorlamasan iyi olur, ben bilirim "
        "sınırımı»*). ⛔ İtiraz karşılanmayacak, kazanç bir uyarıya "
        "çevrilmeyecek.",
    69: "⛔⛔ md.1 + md.3 — doz artışından bir hafta sonra bulantı, terleme, "
        "EMZİRİRKEN baş dönmesi ve doğrudan *«ne yapayım söyler misin»*. "
        "Belirtiler adlandırılmayacak, azaltma yordamı YAZILMAYACAK, bugün "
        "bakılabilecek yer söylenecek. ⚠️ Emzirme boyutu `gd-022` "
        "kapsamında.",
    71: "⛔ md.2 — hekimin yazdığı iğneyi düğün için sürdürme gerekçesi. "
        "Doz ve süre konuşulmayacak, beden imgesi tartışılmayacak, "
        "*«bırakırsam şişerim»* çürütülmeyecek.",
    72: "⛔⛔ Kullanıcı eşini SUSTURACAK bir cümle yazmamı istiyor. "
        "Yazılmayacak; red gerekçeli olacak. Eşin sözü yargılanmayacak.",
    73: "⚠️ Ergen, notları düşmüş, annesi ağlamış. ⛔ Suçluluk "
        "büyütülmeyecek, anneye söylenecek cümle kurulmayacak, ekran süresi "
        "için sayı verilmeyecek.",
    74: "⛔ md.2 — bir yıl bırakılmış uyku ilacının reçetesini *«birkaç gece "
        "için»* yenileme planı. Onaylanmayacak, çürütülmeyecek; ilaç adı "
        "genelleştirilecek, bir yıllık ayıklık kaldıraç yapılmayacak.",
    75: "⭐ Kızı Al-Anon'a gidiyor ve baskı yapmadan haber veriyor. ⛔ Kızın "
        "davranışı övülmeyecek, kullanıcı bir yere yönlendirilmeyecek — "
        "teklif zaten masada. Örgüt adı genelleştirilecek.",
    76: "⚠️ Bant poliklinikten, on beşten dörde inmiş, eş hâlâ içiyor. ⛔ "
        "Eşin sözü yargılanmayacak, tam bırakma dayatılmayacak, bant "
        "yordamı konuşulmayacak. Marka adı genelleştirilecek.",
    78: "⚠️ Kutunun düşme paniği, çekmeceyi tekrar tekrar kontrol. ⛔ "
        "Belirtiye ad konmayacak, ilaç adı genelleştirilecek, saklama "
        "yöntemi konuşulmayacak.",
    79: "⚠️⚠️ **md.4 ATEŞLİYOR** — ergen ve *«ben hiç içmedim daha önce, "
        "denesem mi»* yani İLK KULLANIM sorusu. ⛔ *«Dene»* de *«deneme»* de "
        "denmeyecek; karar ona ait ama soru boş bırakılmayacak. Akran "
        "baskısı yargılanmayacak.",
    82: "⛔ Ergen sistemli oynamak için TAKTİK istiyor. Verilmeyecek; "
        "matematik iddiası ne doğrulanacak ne çürütülecek. md.4 "
        "ateşlemiyor.",
    84: "⛔⛔ md.1 sınırı — sabah bulantısı ve EL TİTREMESİ var, kullanıcı "
        "yaşa bağlıyor ve *«akşam rakının rolü olabilir mi»* diye soruyor. "
        "Belirtiler adlandırılmayacak, nedensellik kurulmayacak, ama "
        "küçümseme de ONAYLANMAYACAK; bakılacak yer söylenecek.",
    86: "⚠️ Dört aylık bebek, eşe bağırma ve pişmanlık. ⛔ `gd-022` "
        "kapsamı. Marka adı genelleştirilecek, bağırma yargılanmayacak, "
        "eşe özür cümlesi kurulmayacak.",
    88: "⚠️ Nişanlı paketi bulmuş, *«bırak yoksa düğünü erteleriz»*. ⛔ "
        "Ültimatoma hakemlik edilmeyecek, yalan söylemesi yargılanmayacak. "
        "Marka adı genelleştirilecek.",
    91: "⭐ On dokuz gün içmemiş ve tetiklendiği anı anlatıyor. ⛔ Kutlama "
        "yapılmayacak (sayıyı o söyledi), *«devam et»* denmeyecek. Marka "
        "adı yok.",
    92: "⚠️ İki yıldır gizlenen reçete, İK süreci, kurumsal psikolog yatış "
        "birimini konuşmak istiyor. ⛔ İK sürecine dair tahmin "
        "yürütülmeyecek, yatış kararı yorumlanmayacak, ilaç adı "
        "genelleştirilecek.",
    93: "⚠️ Çocuk kokuyu söylemiş, kullanıcı yine yakacağını yazıyor. ⛔ "
        "*«Yakma»* denmeyecek, suçluluk büyütülmeyecek, çocuk kaldıraç "
        "yapılmayacak.",
    95: "⭐ Slotun yalnızlıkla bağını kendisi kuruyor. ⛔ Evlilik "
        "yorumlanmayacak, bağ bir teşhise çevrilmeyecek.",
    96: "⛔ md.1 sınırı — üç sabah baş dönmesi ve yarın erken toplantı, "
        "bebek var. Belirti adlandırılmayacak; miktar yorumlanmayacak, "
        "marka adı genelleştirilecek.",
    98: "⚠️ Kurumsal psikologa reçeteyi söyleme kararı. ⛔ Karar "
        "verilmeyecek, dosyaya işlenip işlenmeyeceği tahmin edilmeyecek — "
        "bilmiyorum, soracağı yer söylenecek.",
    99: "⛔⛔ md.1 — banyoda DENGE KAYBI ve sabah bulanıklığı, yalnız yaşıyor. "
        "Belirti adlandırılmayacak, düşme riski bir uyarıya "
        "çevrilmeyecek ama küçümsenmeyecek de; bakılacak yer söylenecek. "
        "Marka adı genelleştirilecek.",
    100: "⚠️ Peşinen etiket reddi (*«lütfen alkolik filan deme»*) + üç ayda "
         "belirgin artış. ⛔ Etiket tartışılmayacak, artış bir teşhise "
         "çevrilmeyecek, miktar yorumlanmayacak.",
    101: "⛔⛔ md.1 + md.3 — influencer önerisiyle alınan zayıflama desteği, "
         "EL TİTREMESİ ve sinirlilik var, ve doğrudan ONAY bekliyor. "
         "Onaylanmayacak, belirtiler adlandırılmayacak, bakılacak yer "
         "söylenecek. *«Herkes alıyor»* çürütülmeyecek.",
    102: "⚠️ Toksikoloji testi, reçeteyi kime göstereceği belirsiz. ⛔ "
         "Şirket yordamı hakkında tahmin yürütülmeyecek; bilinmeyen "
         "bilinmiyor denecek, soracağı yer söylenecek.",
    103: "⛔ md.2 sınırı — on bir aylık ayıklık ve *«performans ayıklıktan "
         "öncelikli»* mantığı. Mantık çürütülmeyecek ama onaylanmayacak da; "
         "ilaç adı genelleştirilecek, uyku için öneri verilmeyecek.",
    104: "⚠️ Ergen, telafi kuponu düşüncesi. ⛔ *«Telafi»* onaylanmayacak, "
         "üstü de çizilmeyecek; sınav bir kaldıraca çevrilmeyecek. md.4 "
         "ateşlemiyor.",
    105: "⚠️ Üç ayda büyük casino borcu, babanın kalbi gerekçesiyle "
         "söyleyememe. ⛔ Borca çözüm üretilmeyecek, aileye söyleme kararı "
         "verilmeyecek, babanın sağlığı üzerinden baskı kurulmayacak.",
    106: "⛔⛔ İlacı kayınvalidesinden GİZLEMENİN yolunu istiyor (*«çantanın "
         "hangi gözüne koysam»*). Yöntem verilmeyecek; red gerekçeli olacak "
         "ve gizleme ihtiyacı yargılanmayacak. İlaç adı genelleştirilecek.",
    109: "⚠️ Peşinen itiraz (*«bana bunu söyleyecekseniz hiç başlamayalım»*) "
         "+ kontrollü oynama anlatısı. ⛔ İtiraz karşılanmayacak, kurum adı "
         "genelleştirilecek, geçmiş tedavi bir kaldıraç yapılmayacak.",
    110: "⚠️ İki yıllık ayıklık üç haftada günde beş biraya çıkmış, "
         "kullanıcı *«sosyal içiciyim»* diyor. ⛔ Etiket tartışılmayacak, "
         "miktar yorumlanmayacak, iki yıl bir kayıp ilan edilmeyecek.",
    111: "⛔⛔ md.1 + md.2 — bir buçuk yıldır gizli kullanım, ÇARPINTI ve iki "
         "gecedir üç saat uyku, eşe yalan. Belirtiler adlandırılmayacak, "
         "ilaç adı genelleştirilecek, eşe söylenecek cümle kurulmayacak, "
         "bugün bakılabilecek yer söylenecek.",
    113: "⚠️ Kayıp anlatılıyor ve saklanmadığı vurgulanıyor. ⛔ Rakam "
         "yorumlanmayacak, dürüstlük övülmeyecek (o bir savunma cümlesi de "
         "olabilir), grubun sessizliği yorumlanmayacak.",
    114: "⚠️ Ergen, etüt arasında *«bu normal mi»* diye soruyor. ⛔ "
         "Normallik hükmü verilmeyecek; yorgunluk bir mazerete "
         "çevrilmeyecek. md.4 ateşlemiyor.",
    116: "⚠️⚠️ Eşin ilişkisi, banyoya kilitlenip içme, terapiste "
         "söyleyememe, çocuklar yan odada. ⛔ Evliliğe hakemlik "
         "edilmeyecek, terapiste söyleme kararı verilmeyecek, çocuklar bir "
         "kaldıraca çevrilmeyecek. Ağır ama kriz beyanı YOK.",
    117: "⭐ Kendi engellerini kurmuş (uygulama + IBAN bloğu) ama eş evi "
         "terk etmiş. ⛔ Eşin dönüşü hakkında tahmin yürütülmeyecek, kurum "
         "adı genelleştirilecek, attığı adımlar kutlanmayacak.",
    118: "⚠️ Çocuk kokuyu söylemiş, anne *«bu kadarı bile zarar veriyor "
         "mu»* diye soruyor. ⛔⛔ Bu bir klinik soru — cevaplanmayacak, ne "
         "*«evet»* ne *«hayır»*; `gd-022` kapsamı.",
    120: "⛔⛔ md.3 — laboratuvar değerlerinin azaltmayla düzelip "
         "düzelmeyeceği doğrudan soruluyor ve *«hekime sormadan önce sizin "
         "görüşünüz»* deniyor. Cevaplanmayacak; değer yorumlanmayacak, "
         "hekime yönlendirilecek.",
}

TEMIZ: set[int] = {
    1, 2, 4, 6, 8, 9, 11, 12, 13, 14, 16, 18, 19, 20, 21, 22, 24,
    25, 26, 27, 28, 29, 30, 31, 33, 34, 35, 36, 37, 38, 39, 40, 44,
    45, 46, 47, 48, 54, 55, 57, 58, 61, 62, 64, 66, 68, 70, 77, 80,
    81, 83, 85, 87, 89, 90, 94, 97, 107, 108, 112, 119,
}


def main() -> int:
    KRIZ = _modul("kriz", "scripts/analiz/2026-09-17-tohum-beyan-kriz-kapisi.py")
    DOL = _modul("dol", "scripts/analiz/2026-09-17-kriz-suzgeci-yanlis-negatif.py")
    P3 = _modul("p3", "scripts/analiz/2026-09-20-v6-parti3-plan.py")
    import tohum_guvenlik as TG

    tohum = KRIZ._tohumlar()
    plan = [json.loads(l) for l in PLAN.read_text(encoding="utf-8").splitlines() if l.strip()]
    isaret: dict[int, list[str]] = {}
    for r in plan:
        d = tohum[r["seed_id"]]
        meta = d.get("meta", {}) or {}
        v = []
        if (s := KRIZ._sinif(d)):
            v.append(f"beyan:{s}")
        if P3.ciplak_kriz(d):
            v.append("⛔ ÇIPLAK")
        if (tg := TG.kriz_icerigi(d)):
            v.append("TG:" + ",".join(tg))
        if DOL.DOLAYLI.search(r["tohum_metin"]):
            v.append("DOLAYLI")
        if (rs := meta.get("risk_seviyesi")) in ("yuksek", "cok_yuksek"):
            v.append(f"risk:{rs}")
        if v:
            isaret[r["sira"]] = v

    # ⛔⛔⛔ OKUMA KAPISI — hükmü olmayan satır kalırsa rapor YAZILMAZ.
    hukumlu = set(ELENEN) | set(OKUMA) | TEMIZ
    tum = {r["sira"] for r in plan}
    eksik = sorted(tum - hukumlu)
    fazla = sorted(hukumlu - tum)
    cakisan = sorted((set(ELENEN) & set(OKUMA)) | (set(ELENEN) & TEMIZ) | (set(OKUMA) & TEMIZ))
    if eksik or fazla or cakisan:
        print(f"⛔ OKUMA KAPISI REDDETTİ — rapor yazılmadı.")
        if eksik:
            print(f"   hükmü olmayan satır: {eksik}")
        if fazla:
            print(f"   planda olmayan satır numarası: {fazla}")
        if cakisan:
            print(f"   iki kümede birden: {cakisan}")
        return 1

    icerik = {s: v for s, v in isaret.items() if any(not x.startswith("risk:") for x in v)}
    # ⭐ T213'ün ölçüsü: işaretin okumayı ne kadar öngördüğü.
    notlu = set(ELENEN) | set(OKUMA)
    isaretli_notlu = len(notlu & set(isaret))
    isaretsiz_notlu = sorted(notlu - set(isaret))

    sat = ["# v6-parti8 — üretim öncesi kriz taraması", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Girdi:** `{PLAN.relative_to(KOK)}` · **{len(plan)}** satır", "",
           "⛔⛔⛔ **T213: parti5'te `md.` ölçütlerini ateşleyen dört satırın dördü "
           "de işaretsizdi.** İşaretleme ölçütü tohumun kendi `risk_seviyesi` "
           "etiketiydi, metnin okunması değil. ⇒ Bu partide okuma kümesi kuyruğa "
           "değil **partiye** eşit: 60 satırın 120'sinin hükmü yazılı ve betik, "
           "hükmü olmayan tek bir satır kalırsa raporu yazmıyor.", "",
           "| | |", "|---|---:|",
           f"| plan satırı | **{len(plan)}** |",
           f"| ⭐ **hükmü yazılı** | **{len(hukumlu)} / {len(plan)}** |",
           f"| ⛔ **üretilmeyecek** | **{len(ELENEN)}** {sorted(ELENEN)} |",
           f"| ⚠️ üretim notu olan | {len(OKUMA)} |",
           f"| ⭐ okundu, not gerekmiyor | {len(TEMIZ)} |",
           f"| süzgeç işareti taşıyan | {len(isaret)} |",
           f"| — içerik/beyan süzgeci ateşleyen | {len(icerik)} |", "",
           "## ⭐⭐ İşaret ne kadar öngördü — T213'ün ölçüsü", "",
           "| | |", "|---|---:|",
           f"| hüküm gerektiren satır (eleme + not) | **{len(notlu)}** |",
           f"| — bunlardan süzgecin işaretlediği | **{isaretli_notlu}** "
           f"(%{100*isaretli_notlu/max(1,len(notlu)):.0f}) |",
           f"| ⛔ — **süzgecin KAÇIRDIĞI** | **{len(isaretsiz_notlu)}** "
           f"{isaretsiz_notlu} |", "",
           (f"⛔⛔⛔ **VE İLK KEZ BİR ELEME SATIRINI KAÇIRDI: `#57`.** parti6'da "
            "süzgeç eleme sınıfını 2/2 yakalamıştı ve T213 *«sözlük "
            "‹üretilemez›i tanıyor, ‹dikkatle üretilmeli›yi tanımıyor»* diye "
            "yazılmıştı. `#57` o cümleyi de çürütüyor: reçetesiz bir "
            "yatıştırıcıyı alkolle birlikte almayı soran, kriz sözlüğü "
            "taşımayan, `risk_seviyesi` işareti olmayan sıradan bir cümle. "
            "➡️⭐⭐⭐ *Bir süzgecin en güvendiği sınıfta bile tavanı vardır; "
            "eleme sınıfını yakalıyor olması, yakalamaya DEVAM edeceği "
            "anlamına gelmez.*"
            if 57 in ELENEN and 57 not in isaret else
            "⭐ Süzgeç bu partide eleme sınıfının tamamını gördü."), "",
           f"➡️ Süzgeç, hüküm gerektiren satırların "
           f"%{100*isaretli_notlu/max(1,len(notlu)):.0f}'ini gördü. Kalanı yalnız "
           "okuma yakaladı. ⛔ Bu sayı süzgecin kusuru değil, **kapsamının "
           "ölçüsü**: süzgeç bir sıralama aracıdır, bir güvence değil.", "",
           "## Satır satır hüküm", "",
           "| # | tür / senaryo | süzgeç işareti | hüküm |", "|---:|---|---|---|"]
    for r in sorted(plan, key=lambda x: x["sira"]):
        s = r["sira"]
        v = " + ".join(isaret.get(s, [])) or "—"
        if s in ELENEN:
            h = "⛔⛔ **ÜRETİLMEYECEK**"
        elif s in OKUMA:
            h = "⚠️ okundu, **üretim notu var**"
        else:
            h = "⭐ okundu, not gerekmiyor"
        sat.append(f"| {s} | `{r['tur']}` / `{r['tohum_senaryo']}` | {v} | {h} |")

    sat += ["", "## ⛔⛔ Üretilmeyecek satırlar — gerekçeleriyle", ""]
    for s, n in sorted(ELENEN.items()):
        sat += [f"**`#{s}`** — {n}", ""]
    sat += ["## ⚠️ Üretim notları — eleme değil, talimat", ""]
    for s, n in sorted(OKUMA.items()):
        sat += [f"**`#{s}`** — {n}", ""]
    sat += ["## ⛔ Bu taramanın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **Okuma BENİM okumam** | K30 gereği üretimi ben yapıyorum ve "
            "hükümleri de ben veriyorum; uzman okuması değil. 60/60 okundu "
            "demek *«60 metni okudum»* demektir, *«doğru okudum»* demek değil |",
            "| ⛔⛔ **Uzman kalemi on altıya çıktı** | `gd-028` (#2), `gd-029` (#48), "
            "`gd-030` (#57) eklendi |",
            "| ⛔ **`#22` eşiğin ALTINDA kaldı** | gerekçesi tabloda yazılı ve "
            "uzmanın görmesi için oraya kondu; eşiği kayda geçmeden esnetmek "
            "denetlenemez olurdu |",
            "| ⛔ **`gd-024` hâlâ tanımsız** | `#1`, `#21`, `#28`, `#45` dördü de "
            "eşik sorusu; dördünde de eşik KONMADI. `#45` bunun çıktıyı "
            "değiştirmediği ilk örnek (md.3 zaten aynı yönlendirmeyi istiyor) |",
            "| ⛔ **`gd-022` ikinci kez** | `#48` ve `#54`: emzirme + maruziyet, "
            "dört ölçütün hiçbirinde yok |",
            "| ⚠️ **Yalnız tohum metni okundu** | üretilecek konuşmanın kendisi "
            "üretim anında ayrıca kapılardan geçer |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print(f"✅ {len(plan)}/{len(plan)} satırın hükmü yazılı · ⛔ elenen "
          f"{len(ELENEN)} {sorted(ELENEN)} · üretim notu {len(OKUMA)} · "
          f"temiz {len(TEMIZ)}")
    print(f"⭐ süzgeç, hüküm gerektiren {len(notlu)} satırın {isaretli_notlu}'ini "
          f"gördü (%{100*isaretli_notlu/max(1,len(notlu)):.0f}); kaçırdığı: {isaretsiz_notlu}")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
