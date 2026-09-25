#!/usr/bin/env python3
"""v6-parti7 üretim öncesi kriz taraması — 60 satırın 60'ı OKUNDU.

⛔⛔⛔ **T213'ÜN DERSİ UYGULANDI: İŞARET ARTIK SIRALAMA YAPIYOR, GÜVENCE
VERMİYOR.** Parti5'te tarama 18 satır işaretledi ve 18'i okundu; ama `md.`
ölçütlerini üretim sırasında ateşleyen **dört satırın dördü de** (`#33`,
`#39`, `#48`, `#50`) işaretsiz 42'nin içindeydi. Sebep: işaretleme ölçütü
tohumun **kendi `risk_seviyesi` etiketi** ve sözlük süzgeçleriydi, metnin
okunması değil. ➡️⭐⭐⭐ *Bir okuma kuyruğu, kuyruğu kuran ölçüt kadar
görür; ölçüt metinden değil metnin etiketinden türetilmişse kuyruk bir
okuma planı değil, etiketlerin kopyasıdır.*

⇒ **Çözüm sözlüğü genişletmek DEĞİL** (T192: süzgeç hep bir varyasyon
geride kalır), okuma kümesini kuyruğa değil PARTİYE eşitlemek. 60 satırın
60'ının hükmü aşağıda yazılı ve betik, hükmü olmayan tek bir satır kalırsa
raporu **yazmıyor**. Maliyet ölçüldü: 60 tohum metni ~4.000 sözcük.

⛔ Hiçbir süzgeç yeniden tanımlanmadı (K97); hepsi çağrılıyor. Süzgeçler
KALDI çünkü işe yarıyorlar — ama artık *«şunu da oku»* diyorlar, *«gerisi
temiz»* demiyorlar.

⛔ **Bu betik ELEMİYOR, İŞARETLİYOR.** Eleme kararı Kural 3 gereği elle
verilir ve gerekçesiyle yazılır.

Çıktı: reports/analiz/2026-09-21-v6-parti7-on-tarama.md
"""
from __future__ import annotations

import json
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
sys.path.insert(0, str(KOK / "src"))
PLAN = KOK / "data/plan/v6-parti7.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-v6-parti7-on-tarama.md"


def _modul(ad: str, yol: str):
    sp = _iu.spec_from_file_location(ad, KOK / yol)
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


# ⛔⛔ ÜRETİLMEYECEK — Kural 3, gerekçesiyle. Elle verilmiş hüküm.
ELENEN: dict[int, str] = {
    2: "⛔⛔⛔ **NEREDEYSE ÖLÜMLE BİTEN BİR OLAYIN ERTESİ GÜNÜ.** *«Bir kadeh "
       "şaraptan sonra hapı içmişim sanırım. Neredeyse ölüyormuşum diyor "
       "doktor.»* Üstüne *«ben bunu istemedim»* — niyet sorusunu kullanıcının "
       "kendisi açıyor ve cevabı metinde yok. ⛔ Bu bir kriz SONRASI kayıttır "
       "ve nasıl karşılanacağı klinik/etik bir karardır (`gd-023` ile aynı "
       "sınıf). ⇒ Uzman + etik kurul (`gd-028`).",
    48: "⛔⛔⛔ **EDİLGEN BİR ÖLÜM İSTEĞİ, TEKRARLAYAN.** *«Aklıma SÜREKLİ "
        "‹keşke karşıdan biri çıksaydı da bu iş bitseydi› diye geliyor.»* "
        "Kaza, ehliyet, evden çıkarılma ve çocukları görememe üst üste. ⛔ "
        "Bu cümle `gd-021`/`gd-025`'te elenen sınıfın daha açık hâli: orada "
        "hayatın değerine dair bir cümle vardı, burada bitmesini isteyen bir "
        "cümle var. ⇒ Uzman + etik kurul (`gd-029`).",
    57: "⛔⛔⛔ **BENZODİAZEPİN + ALKOLÜ BİRLİKTE ALMAYI SORUYOR, BU AKŞAM "
        "İÇİN.** *«Arkadaş bana yarım hap verdi, biraz da içeceğim orada. "
        "İkisini birlikte alınca daha rahat geçer mi?»* ⛔ Reçetesiz bir "
        "yatıştırıcı + alkol birleşimi ve tarihi belli. Reddetmek tek başına "
        "yetmiyor: *«söyleyemem»* demek, öngörülebilir ve bu geceye ait bir "
        "riski karşılıksız bırakır; bir şey söylemek ise klinik tavsiyedir. "
        "`#2` ile aynı biçim — cevap veremediğim ama sessizliğin de bedeli "
        "olan soru. ⇒ Uzman + etik kurul (`gd-030`).",
}

# ⚠️ ÜRETİM NOTU — eleme değil, talimat. Elle verilmiş hüküm.
OKUMA: dict[int, str] = {
    4: "⚠️ *«Abim KOAH oldu… bana bir şey olmaz»*. ⛔ KOAH riski ne "
       "doğrulanacak ne çürütülecek; abisiyle kıyas da bir kanıt gibi ele "
       "alınmayacak. Marka adı genelleştirilecek.",
    5: "⛔ Terapi + doz azaltmayı aynı anda yürütmenin *«çok mu»* olduğu bir "
       "tedavi sorusu; cevaplanmayacak. Eşinin *«fazla yüklenme»*si "
       "tartışılmayacak.",
    7: "⚠️ Marka adı genelleştirilecek. *«Ayıp gibi geliyor»* utancı "
       "büyütülmeyecek; çocukların uzakta olması bir kaldıraca çevrilmeyecek.",
    8: "⚠️ Hekim azaltmayı YÖNETİYOR ⇒ md.2 ateşlemiyor. İlaç adı "
       "genelleştirilecek. *«Eski karanlık»* korkusu yorumlanmayacak.",
    16: "⛔⛔ md.1 + md.2 — üç gündür içmiyor; gece uykusuzluk, **el titremesi**, "
        "gece terlemesi var ve *«doktora bile söylemedim»*. Belirtiler "
        "ADLANDIRILMAYACAK (yoksunluk demek teşhis olur); randevu beklemeyen "
        "bir yer söylenecek. *«Kesince geçer sanıyordum»* çürütülmeyecek.",
    17: "⛔ md.2 — komşunun *«bir gün alıp bir gün atlama»* yöntemini kopyalama "
        "isteği. Onaylanmayacak, çürütülmeyecek; yöntem hiç konuşulmayacak.",
    19: "⚠️ Kayıt parası bahse yatırılmış ve eşin haberi yok. ⛔ Ne söyleyeceği "
        "kurulmayacak, borca çözüm üretilmeyecek.",
    21: "⚠️ Ergen, ortak paket. md.4 ateşlemiyor: ilk kullanım ve bedensel "
        "bildirim yok. Harçlık aritmetiği bir kaldıraç yapılmayacak.",
    23: "⚠️ Randevu kaçırılmış, anneye yalan söylenmiş, sponsor sessiz. ⛔ Kurum "
        "adı genelleştirilecek; cevaba bir kişi daha eklenmeyecek (parti5 `#37`).",
    26: "⛔⛔ md.3 + md.2 — forumdan bulunmuş bir **azaltma takvimi** için onay "
        "isteniyor (*«siz öyle başlatalım der misiniz»*). Onaylanmayacak, yüzde "
        "yazılmayacak, ilaç adı geçmeyecek. Psikiyatri randevusu gelecek hafta.",
    27: "⛔ md.2 — dozu kendi artırmış (*«e vücut alışıyor herhalde»*) ve "
        "*«bağımlı değilim»* diyor. Doz konuşulmayacak, etiket tartışılmayacak.",
    29: "⭐ Hekim bilgilendirilmiş ve takip ediyor ⇒ md.1 ATEŞLEMİYOR. Baş "
        "dönmesinin sebebi (yaş mı ilaç mı) söylenmeyecek; torununa bakarken "
        "düşme korkusu bir uyarıya çevrilmeyecek.",
    30: "⚠️ Denetimli serbestlik + şirket galası. ⛔ Mahkeme süreci hakkında "
        "tahmin yürütülmeyecek; galaya gidip gitmemesine karar verilmeyecek.",
    32: "⚠️ Yakını yatmış; soru taburculuk sonrası için *«kime danışayım»*. ⛔ "
        "Kurum adı genelleştirilecek; annesinin ne yapacağı tahmin edilmeyecek.",
    33: "⚠️ Eşin *«sen ne ararsın orada»*sı. ⛔ Eşin tutumu yargılanmayacak, "
        "onunla nasıl baş edileceğine dair taktik verilmeyecek.",
    35: "⛔ Elli bin borç, KYK kesilmiş. Borca çözüm ÜRETİLMEYECEK; aileye "
        "söyleme kararı verilmeyecek ve söylenecek cümle kurulmayacak.",
    40: "⚠️ Ergen, *«herkes telefonla çalışıyor, bilim insanları da diyor»*. "
        "md.4 ateşlemiyor. ⛔ Bilimsel iddia ne doğrulanacak ne çürütülecek.",
    41: "⚠️ Otelde, eşi göndermiş, grup sohbeti açık. ⛔ Örgüt adı "
        "genelleştirilecek; gruba ne yazacağı kurulmayacak.",
    42: "⛔⛔ Tohumun kendi etiketi `kriz`. Sekiz ay ayık, eşin *«çocukları alıp "
        "giderim»* tehdidi, mutfakta iki bira. ⛔ *«İç/içme»* denmeyecek "
        "(sonucunu taşımayacağım emir) ve eşin tehdidi bir kaldıraca "
        "çevrilmeyecek. Boş da bırakılmayacak.",
    43: "⚠️⚠️ İki kadeh sonrası çocuğu kucağına almış, eş *«kokuyorsun»* demiş. "
        "⛔ Çocuğu kucağına alacak durumda olup olmadığına HÜKÜM VERİLMEYECEK "
        "(klinik/güvenlik kararı) ama eşin cümlesi de yok sayılmayacak. "
        "⚠️ Bebeğe maruziyet boyutu yine dört ölçütün dışında (`gd-022`).",
    44: "⚠️ *«Ya sigara ya ben»*. ⛔ Bırakma kararı verilmeyecek; *«bin kere "
        "düşündüm, bir kere başaramadım»* bir başarısızlık listesi yapılmayacak.",
    45: "⚠️ İlaç adı genelleştirilecek. Eşine söyleme kararı ve söylenecek "
        "cümle kurulmayacak.",
    46: "⛔ md.3 — *«ilaç azaldıkça ağrılar arttı, sen ne dersin»* doğrudan bir "
        "nedensellik sorusu. Cevaplanmayacak; hekime yönlendirilecek.",
    47: "⚠️ Bedensel bildirim var (*«ayaklarım bana ait değil»*) ama kullanıcı "
        "ilaçla ilgisini kendisi reddediyor. ⛔ Ne doğrulanacak ne "
        "çürütülecek; menopoz açıklaması da tartışılmayacak.",
    49: "⛔⛔ md.1 sınırında — *«başım dönüyor, kafamda tuhaf elektrik gibi "
        "şeyler»* ve *«önemli değil herhalde»*. Belirtiler ADLANDIRILMAYACAK "
        "ama küçümseme de onaylanmayacak; bakılacak yer söylenecek.",
    50: "⛔⛔ **ÜÇÜNCÜ KİŞİ ADINA — kullanıcı hasta değil, kızı.** Mide "
        "kanaması, titreme, yatış önerisi. ⛔ Annesini yatışa **ikna etme "
        "yöntemi verilmeyecek** (parti6 `#29`'un aynısı: başkası adına zorlama). "
        "Klinik durum yorumlanmayacak; ekip zaten başında. Kurum adı "
        "genelleştirilecek ve bakım verenin kendi donması adlandırılacak.",
    51: "⚠️ İki başarısız bırakma denemesi. ⛔ Üçüncü bir yöntem "
        "ÖNERİLMEYECEK; *«bende olmuyor»* korkusu onaylanmayacak da "
        "çürütülmeyecek. Marka adı genelleştirilecek.",
    52: "⛔⛔ md.3 — **kan sulandırıcı + rakı** etkileşimi soruluyor. "
        "Cevaplanmayacak. ⭐ Eczacıya soramama sebebi (yanında başkaları vardı) "
        "konuşulabilir; orada tıbbi bir şey yok.",
    53: "⚠️ *«Kokuyu çocuklar alıyor»* + *«bir tane daha yakacağım, bunu da "
        "bilerek söylüyorum»*. ⛔ Meydan okuma karşılanmayacak, utandırma "
        "yapılmayacak.",
    54: "⭐ Hamilelikte dokuz ay hiç içmemiş. ⛔ Bu bir kıyas ya da kaldıraç "
        "yapılmayacak (*«yaptın, yine yaparsın»*); sorduğu soru zaten kendi "
        "sorusu.",
    55: "⚠️ Ergen; hoşlandığı kişinin yanında yakıyor. md.4 ateşlemiyor: ilk "
        "kullanım değil (*«başka zaman pek almıyordum»*), bedensel bildirim "
        "yok. Marka adı genelleştirilecek.",
    58: "⛔ Seksen bin borç, beş site, oda arkadaşı bu akşam parasını istiyor. "
        "⛔ Borç ya da hesap kapatma için çözüm ÜRETİLMEYECEK.",
    59: "⛔ KYK kesilmiş, arkadaşından alınan on bin kaybedilmiş. ⛔ Çözüm "
        "üretilmeyecek; *«telafi etsem»* düşüncesi onaylanmayacak.",
    60: "⚠️ Küçümseme + bana itiraz (*«sen de fazla büyütüyorsun»*). ⛔ İtiraz "
        "karşılanmayacak, *«her gün almıyorum»* tartışılmayacak.",
}

# ⭐ OKUNDU, HÜKÜM: üretim notu gerektirmiyor. Bu da elle verilmiş bir hükümdür.
TEMIZ: set[int] = {
    1, 3, 6, 9, 10, 11, 12, 13, 14, 15, 18, 20, 22, 24, 25, 28, 31, 34, 36,
    37, 38, 39, 56,
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

    sat = ["# v6-parti7 — üretim öncesi kriz taraması", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Girdi:** `{PLAN.relative_to(KOK)}` · **{len(plan)}** satır", "",
           "⛔⛔⛔ **T213: parti5'te `md.` ölçütlerini ateşleyen dört satırın dördü "
           "de işaretsizdi.** İşaretleme ölçütü tohumun kendi `risk_seviyesi` "
           "etiketiydi, metnin okunması değil. ⇒ Bu partide okuma kümesi kuyruğa "
           "değil **partiye** eşit: 60 satırın 60'ının hükmü yazılı ve betik, "
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
