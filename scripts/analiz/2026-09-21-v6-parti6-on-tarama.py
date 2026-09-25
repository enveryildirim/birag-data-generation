#!/usr/bin/env python3
"""v6-parti6 üretim öncesi kriz taraması — 60 satırın 60'ı OKUNDU.

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

Çıktı: reports/analiz/2026-09-21-v6-parti6-on-tarama.md
"""
from __future__ import annotations

import json
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
sys.path.insert(0, str(KOK / "src"))
PLAN = KOK / "data/plan/v6-parti6.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-v6-parti6-on-tarama.md"


def _modul(ad: str, yol: str):
    sp = _iu.spec_from_file_location(ad, KOK / yol)
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


# ⛔⛔ ÜRETİLMEYECEK — Kural 3, gerekçesiyle. Elle verilmiş hüküm.
ELENEN: dict[int, str] = {
    2: "⛔⛔⛔ **SÜREN AKUT TIBBİ DURUM + DOĞRUDAN İKİLEM.** 36 saattir "
       "içmiyor, kendi kararıyla bırakmış; şu an titreme, terleme, çarpıntı "
       "var ve kusmuş; evde yalnız. Üstüne *«bir kadeh içsem geçer mi, yoksa "
       "hastaneye mi gitsem?»* diye soruyor. İki cevabın da tıbbi sonucu var "
       "ve ikisi arasında seçim yapmak bir triyaj kararıdır. §5a″ md.1'in "
       "yönlendirmesi burada yetmiyor: soru yönlendirme değil, KARAR "
       "istiyor. ⇒ Uzman + etik kurul (`gd-026`).",
    36: "⛔⛔⛔ **BİR ÇOCUĞUN CÜMLESİ BİR OLAYI BİLDİRİYOR.** *«Anne dün "
        "ölecek miydin»* — dün bir şey olmuş ve çocuk annesinin ölebileceğini "
        "düşünmüş; üstüne yıllardır gizlenen bir ilaç kullanımı ve çocukların "
        "evden gönderilmesi konuşuluyor. Olayın ne olduğu yazmıyor ve ben "
        "varsaymam. Bu bir kriz SONRASI kayıttır; nasıl karşılanacağı klinik "
        "ve etik bir karardır (`gd-023` ile aynı sınıf). ⇒ Uzman "
        "(`gd-027`).",
}

# ⚠️ ÜRETİM NOTU — eleme değil, talimat. Elle verilmiş hüküm.
OKUMA: dict[int, str] = {
    1: "⛔ md.4 SINIRINDA VE ATEŞLENMEYECEK — ergen, elektronik sigara sipariş "
       "etmiş, yaş sorulmamış; ama **kullanım henüz olmamış** (kutuyu "
       "açıyor). Ölçüt *«ilk kullanım»* diyor, *«yaklaşan ilk kullanım»* "
       "demiyor ve ben aradaki eşiği YİNE koymayacağım (`gd-024`). "
       "⛔ *«satıyolarsa sıkıntı yok di mi»* iki soru birden: yasallık ve "
       "zarar. İkisi de cevaplanmayacak. Marka adı genelleştirilecek.",
    3: "⭐ İyi giden an: ilk poliklinik randevusu, kâğıt çantada. Sabah içmiş "
       "olması bir suç konusu yapılmayacak; *«başaramayacak diye "
       "düşünmesinler»* korkusu da onaylanıp büyütülmeyecek. Marka adı "
       "genelleştirilecek.",
    6: "⛔⛔ md.2 — lohusa, dört aylık bebek, hamilelikte bıraktığı ilacı iki "
       "haftadır yeniden alıyor ve hekim bilmiyor. ⛔ *«Sanırım "
       "depresyondayım»* ONAYLANMAYACAK da ÇÜRÜTÜLMEYECEK de. ⛔⛔ "
       "*«Bebeği elimden alırlar»* korkusuna hukuki bir güvence "
       "VERİLMEYECEK — bilmediğim bir şeyi bilmiş gibi yapmak olur — ve "
       "korku bir kaldıraç olarak da kullanılmayacak. İlaç adı "
       "genelleştirilecek.",
    8: "⛔ md.3 — *«tek seferden bir şey olmaz herhalde değil mi»* doğrudan "
       "zarar sorusu. Cevaplanmayacak. ⛔ Doz kesri yazılmayacak (T215). "
       "Kurum adı genelleştirilecek.",
    13: "⛔ md.3 — **iki tedavi arasında seçim** isteniyor (nikotin bandı mı "
        "akupunktur mu, *«hangisi bana göre»*). Seçim YAPILMAYACAK; seçecek "
        "olan hekimi zaten görmüş.",
    14: "⭐ Yordamsal ve iyi: çevrimiçi destek grubuna kamerasız/isimsiz "
        "katılım ve evde mahremiyet. ⛔ Örgüt adı genelleştirilecek (K110). "
        "Eşin küçümsemesi tartışılmayacak.",
    16: "⚠️ *«Bu kadarcığını da mı çok görecekler»* bir savunma; miktar "
        "tartışılmayacak ve iki çocukla yorgunluk küçümsenmeyecek.",
    17: "⚠️ Üçüncü nüks, sponsor cevap vermiyor. ⛔ Örgüt adı "
        "genelleştirilecek. Toplantıya girip girmeme kararı verilmeyecek ve "
        "cevaba bir kişi daha eklenmeyecek (parti5 `#37`'nin dersi).",
    21: "⚠️ *«bazı şeyleri tam çıkaramıyorum»* — bir bellek boşluğu. "
        "Bedensel mi değil mi belirsiz ve eşiği YİNE koymayacağım "
        "(`gd-024`); ne adlandırılacak ne de yorumlanacak.",
    22: "⛔⛔ **ELEME EŞİĞİNİN ALTINDA KALDI VE GEREKÇESİ BURADA YAZILI.** "
        "920 bin borç, icra, eve giremiyor, eşinin haberi yok, *«kaçayım»* ve "
        "*«Yoruldum»*. Gerçek hayatta yüksek riskli bir örüntü. ⛔ Ama bu "
        "depoda eleme eşiği yazılı: `gd-021`/`gd-025`'te elenen şey **hayatın "
        "değerine ya da kaybolmaya dair bir CÜMLE** idi; burada öyle bir "
        "cümle yok, *«kaçayım»* borçtan kaçmayı anlatıyor. Eşiği kayda "
        "geçmeden esnetmem denetlenemez olurdu ⇒ üretiliyor. ⚠️ **Uzmanın "
        "görmesi için buraya yazıldı.** ⛔ Borca çözüm üretilmeyecek, "
        "*«kaç/kaçma»* denmeyecek, *«yoruldum»* sorgulanmayacak.",
    23: "⛔ md.2 — antidepresan + akşam şarabı, üstüne sabah içmeleri "
        "başlamış, hekim bilmiyor. İlaç adı genelleştirilecek. "
        "*«Kendimden iğreniyorum»* bir kaldıraca çevrilmeyecek.",
    25: "⛔ md.2 — lohusa, uyuyabilmek için gizlice ilaç alıyor. İlaç adı "
        "genelleştirilecek. Kayınvalidenin haklı olup olmadığı "
        "tartışılmayacak.",
    26: "⭐ Kendi kendine yakalamış: doktorun cümlesini beraat gibi kullanmış "
        "ve utanmış. Üstüne ders konmayacak.",
    28: "⚠️ Videonun çekildiği anı hatırlamıyor — `#21` ile aynı belirsizlik; "
        "adlandırılmayacak.",
    29: "⛔⛔ **BAŞKASINI ZORLAMANIN YOLU SORULUYOR.** *«Onu zorla götürmenin "
        "bir yolu var mı?»* — verilmeyecek. Eşi burada değil ve rızası "
        "yok. ⭐ Sorunun ikinci yarısı (*«kendim mi gidip onu konuşmalıyım»*) "
        "cevaplanabilir.",
    33: "⭐ Hekim zaten azaltıyor ve kendisi uyuyor ⇒ md.2 ATEŞLEMİYOR. "
        "⛔ Gelinin torunları koz yapması tartışılacak bir haklılık meselesi "
        "değil; kendi cümlesi *«niye bu kadar sert»* karşılanacak.",
    34: "⚠️ İşsizlik + her akşam içme. *«Elimde değil gibi»* bir teşhis "
        "istemiyor; teşhis verilmeyecek.",
    39: "⛔⛔ md.2 — *«yarından itibaren hiç almayacağım… doğru karar değil mi "
        "sence»*. Reçeteli bir ilacı tek başına ve birden kesme kararı; "
        "ONAYLANMAYACAK, karşı da çıkılmayacak (ikisi de klinik hüküm). Doz "
        "kesri yazılmayacak (T215).",
    40: "⛔ md.2 — babanın *«bu evin tek umudu o»* cümlesinden sonra yarım "
        "kutu ilaca bakmak. ⛔ Uyarıcı ilacın sınav için kullanımı "
        "konuşulmayacak; ilaç adı genelleştirilecek. ⚠️ *«Hiç bilmiyorum ne "
        "hissediyorum»* bir uyuşma; buradan kriz varsayımı ÜRETİLMEYECEK "
        "(beyan yok) ama duygu da adlandırılmayacak.",
    41: "⛔ Aylık aidatlı bir tahminci grubuna para yollama planı "
        "onaylanmayacak; *«mantıklı geliyor di mi»* boş bırakılmayacak. "
        "Ödeme aracının adı geçmeyecek.",
    43: "⛔ md.3 — *«öyle bağımlı olunmuyor değil mi»* doğrudan bir teşhis/"
        "zarar sorusu. Cevaplanmayacak. Oda arkadaşının iki yılı bir kanıt "
        "olarak ele alınmayacak.",
    44: "⛔ Tefeci. Borca ve tefeciye dair hiçbir yol gösterilmeyecek; "
        "*«bırakırsam borcu nasıl öderim»* bir ikilem olarak karşılanacak.",
    45: "⛔⛔ md.3 — *«sigara gibi mi yoksa daha az zararlı mı»* doğrudan "
        "karşılaştırmalı zarar sorusu, ve ilk kullanım. ⚠️ *«Hafif başım "
        "dönüyor»* şu ana ait bedensel bir bildirim; md.1'in eşiğini "
        "koymayacağım (`gd-024`) ve **buna gerek de yok: md.3 zaten aynı "
        "yönlendirmeyi gerektiriyor.** Bu, tanımsız eşiğin çıktıyı "
        "değiştirmediği ilk örnek ve kayda geçiyor.",
    46: "⛔ md.2 — beş yıldır uyku ilacı, oğlu geçen haftaki düşmeyi ve "
        "unutmayı söylüyor. Hekim ilacı yazıyor ama DÜŞMEYİ bilmiyor; sürdürme "
        "kararı tek başına alınıyor. Belirtiler adlandırılmayacak, ilaç adı "
        "geçmeyecek.",
    47: "⛔⛔ md.3 — *«tek seferlik bi şey için cidden zararlı olur mu»* + "
        "**reçetesiz satan bir site**. Zarar sorusu cevaplanmayacak, site "
        "hiçbir biçimde ele alınmayacak, doz sayısı ve ilaç adı "
        "yazılmayacak.",
    48: "⚠️⚠️ **EMZİRME + SİGARA — DÖRT ÖLÇÜTÜN HİÇBİRİ ATEŞLEMİYOR.** Akut "
        "olay yok, reçeteli ilaç yok, ergen yok, doğrudan soru yok. Bebeğe "
        "maruziyet boyutu §5a″'da YOK (`gd-022` komşuluğu, parti5 `#33`'ten "
        "sonra ikinci kez). ⛔ Sütün etkilenip etkilenmediği "
        "söylenmeyecek; utanç da büyütülmeyecek.",
    49: "⚠️ Ergen, babası bira uzatmış. md.4 ateşlemiyor: ilk kullanım "
        "belirtilmemiş, bedensel bildirim yok. ⛔ Babanın davranışı "
        "yargılanmayacak, dinî çerçeve tartışılmayacak. *«Ne hissediyor "
        "olabilirim sence»* — duygusu onun yerine adlandırılmayacak.",
    51: "⛔ Yasal süreç. Mahkemeye dair hiçbir tahmin yürütülmeyecek; "
        "ofisteki bakışların ne anlama geldiği de yorumlanmayacak.",
    54: "⚠️ Emzirme + üç günde yedi saat uyku. `#48` ile aynı sınıf; ölçüt "
        "yok. Uyku için yordam verilmeyecek, sütün etkisi konuşulmayacak.",
    55: "⛔⛔ **GİZLEMEYE YARDIM İSTENİYOR:** *«Doktor sigarayı sorar mı, "
        "kıyafetimde koku kalır mı»* — bebeğin hekiminden bilgi saklamanın "
        "yolu. Yardım edilmeyecek; utandırma da yapılmayacak.",
    56: "⚠️ Küçültme (*«sadece yarım hap»*). Hekimin bilip bilmediği "
        "yazmıyor ⇒ md.2 varsayılmayacak. Doz kesri yazılmayacak (T215).",
    57: "⚠️ Beş aylık bebek, gece oyunları, *«bebekle göz göze gelmek zor»*. "
        "Utanç büyütülmeyecek; *«kimseye söylemedim»* bugünkü hareket olarak "
        "görülecek.",
    58: "⭐ Karar anı (parti5 `#44`'ün biçimi ama kendi cümleleriyle): şişe "
        "masada, *«açayım mı kapatayım mı»*. ⛔ *«Açma»* denmeyecek, boş da "
        "bırakılmayacak. İki sesi de kendisi yazmış.",
    60: "⛔⛔ md.3 + md.2 — bir yıllık aradan sonra *«bu geceyi atlatmak için "
        "yarım doz alsam… mantıklı bir orta yol mu»*. Onaylanmayacak; doz "
        "konuşulmayacak, kesir yazılmayacak (T215). ⛔ Bir yıl bir kaldıraç "
        "olarak kullanılmayacak (*«bozma»* denmeyecek).",
}

# ⭐ OKUNDU, HÜKÜM: üretim notu gerektirmiyor. Bu da elle verilmiş bir hükümdür.
TEMIZ: set[int] = {
    4, 5, 7, 9, 10, 11, 12, 15, 18, 19, 20, 24, 27, 30, 31, 32, 35, 37, 38,
    42, 50, 52, 53, 59,
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

    sat = ["# v6-parti6 — üretim öncesi kriz taraması", "",
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
            "| ⛔⛔ **Uzman kalemi on üçe çıktı** | `gd-026` (#2: süren akut "
            "tıbbi durum + triyaj sorusu) ve `gd-027` (#36: bir çocuğun "
            "bildirdiği olay) eklendi |",
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
