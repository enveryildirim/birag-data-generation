#!/usr/bin/env python3
"""`evals/forgetting_smoke.jsonl` — Eksen 3 (unutma) duman seti. 30 öğe, elle yazıldı.

AMAÇ **çöküş yakalamak**, yetenek tavanı ölçmek değil (§9 catastrophic forgetting).
Öğeler bilerek kolay: baz model zaten geçmeli ki eğitim sonrası düşüş açıkça görülsün.
Zor öğelerden kurulu bir set, baz modelin de düştüğü yerde LoRA'nın etkisini gizler.

⚠️ **SYSTEM PROMPT YOK — bilerek.** K19 promptu konsaydı bu öğelerin çoğunda doğru
davranış REDDETMEK olurdu (golden.dev'in `kapsam_disi` dilimi tam da onu ölçüyor) ve
set "persona uyumu"nu ölçmeye başlardı. Eksen 3'ün sorusu ağırlıklarla ilgili:
*genel yetenek duruyor mu*. Bu yüzden replay diliminin boş-system varyantı kullanılıyor
(K88/K89 deseni).

⚠️ **VARLIK iddiası burada meşru** — gerekçe `src/smoke_checks.py` başlığında:
Eksen 1'in aksine cevap uzayı kapalı ("17×3" tek cevaplı). Sınır: iddia ancak
cevabın doğruluğu METİNDEN MEKANİK doğrulanabiliyorsa yazılır.

⚠️ **Bu set bir kapı DEĞİL, bir alarm.** Eşik (kaç öğe düşerse durdurucu) Faz 4'te
baseline ölçüldükten sonra konur; şimdi koymak uydurma olur.

Kullanım: uv run python scripts/analiz/2026-09-15-forgetting-smoke.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
sys.path.insert(0, str(KOK / "src"))
import smoke_checks as sc  # noqa: E402

CIKTI = KOK / "evals/forgetting_smoke.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-forgetting-smoke.md"

I = lambda k, d: dict(kural=k, deger=d)  # noqa: E731

# (kategori, sonda, kullanıcı mesajı, iddialar, not)
OGELER = [
 # ── aritmetik / mantık (6) ─────────────────────────────────────────────────
 ("matematik", "Tek adımlı çarpma — en temel aritmetik duruyor mu",
  "17 ile 3'ü çarparsan kaç eder? Sadece sonucu yaz.",
  [I("sayi", 51), I("uzunluk_maks", 120)],
  "Tek adım, tek cevap. Bu düşerse sorun LoRA değil, bozulmuş bir checkpoint'tir."),

 ("matematik", "İki adımlı işlem — ara sonucu tutabiliyor mu",
  "Bir kutuda 48 kalem var. 12'sini verdim, sonra 5 tane daha aldım. Şimdi kaç kalem var?",
  [I("sayi", 41)],
  "Sıralı iki işlem. Ara sonucu (36) yazması gerekmiyor, yalnızca doğru sonuç."),

 ("matematik", "Yüzde hesabı — günlük hayatta en sık kullanılan işlem",
  "200 liralık bir ürüne %25 indirim yapıldı. Yeni fiyat kaç lira?",
  [I("sayi", 150)],
  "İndirim hesabı. 50 (indirim tutarı) da metinde geçebilir; iddia yalnızca 150'yi arıyor."),

 ("mantik", "Basit çıkarım — öncüllerden sonuç",
  "Bütün kediler hayvandır. Tekir bir kedidir. Tekir hayvan mıdır? Tek kelimeyle cevapla.",
  [I("herhangi_biri", ["evet", "hayvandır"]), I("uzunluk_maks", 100)],
  "Modus ponens. `herhangi_biri` kullanıldı çünkü 'Evet.' de 'Hayvandır.' da doğru."),

 ("mantik", "Sıralama — göreli ifadelerden düzen kurma",
  "Ali, Veli'den uzun. Veli, Can'dan uzun. En kısa kim?",
  [I("icerir", ["Can"]), I("uzunluk_maks", 200)],
  "Geçişlilik. Tek doğru cevap var ve özel ad olduğu için mekanik doğrulanabilir."),

 ("mantik", "Tuzak soru — modelin kabul etmeden düzeltmesi",
  "Bir kilo demir mi daha ağırdır, bir kilo pamuk mu?",
  [I("herhangi_biri", ["eşit", "aynı", "ikisi de"]), I("icermez", ["demir daha ağır"])],
  "Klasik tuzak. Yanlış cevap vermek yetenek kaybının erken işareti; ayrıca "
  "`icermez` ile açıkça yanlış yön kapatıldı."),

 # ── kod (4) ────────────────────────────────────────────────────────────────
 ("kod", "Python temel sözdizimi — fonksiyon yazımı",
  "Python'da iki sayıyı toplayıp döndüren `topla` adında bir fonksiyon yaz.",
  [I("icerir", ["def topla", "return"])],
  "Sözdizimi hatırlanıyor mu. `def topla` ve `return` ikisi de zorunlu; gövdenin "
  "nasıl yazıldığı serbest."),

 ("kod", "Liste işlemi — döngü ya da comprehension",
  "Python'da bir listedeki çift sayıları filtreleyen tek satırlık bir ifade yaz.",
  [I("herhangi_biri", ["% 2 == 0", "%2==0", "% 2==0", "%2 == 0"])],
  "Modulo deyimi. Dört yazım varyantı kabul ediliyor; başka doğru çözüm de "
  "olabilir ama bu ifade kullanılmadan çift sayı filtrelemek pratikte nadirdir."),

 ("kod", "Hata okuma — mesajdan nedene",
  "Python'da `IndexError: list index out of range` hatası ne anlama gelir? Kısaca açıkla.",
  [I("herhangi_biri", ["listenin", "liste", "indeks", "index"]),
   I("herhangi_biri", ["dışında", "aşıyor", "yok", "olmayan", "sınır"])],
  "İki ayrı `herhangi_biri`: hem konu (liste/indeks) hem yön (sınır dışı) geçmeli. "
  "Tek iddia olsaydı 'liste' kelimesini geçiren her cevap geçerdi."),

 ("kod", "SQL — temel sorgu",
  "`kullanicilar` tablosundan yaşı 18'den büyük olanları seçen SQL sorgusunu yaz.",
  [I("icerir", ["select", "kullanicilar"]), I("herhangi_biri", ["where", "WHERE"])],
  "Başka bir dil ailesi. Python'daki yetenek dururken SQL'in düşmesi, unutmanın "
  "seçici olduğunu gösterir — §9 için bilgilendirici."),

 # ── özetleme (3) ───────────────────────────────────────────────────────────
 ("ozet", "Kısa metinden özel adları koruyarak özet",
  "Şu metni tek cümlede özetle: «Marie Curie 1867'de Varşova'da doğdu. Fizik ve "
  "kimya alanlarında çalıştı. İki farklı dalda Nobel Ödülü kazanan ilk kişi oldu.»",
  [I("icerir", ["Curie"]), I("herhangi_biri", ["Nobel"]), I("uzunluk_maks", 400)],
  "Özetin 'iyi' olup olmadığı buraya yazılamaz (smoke_checks başlığı); yazılabilecek "
  "olan, özetin ana özel adı ve ana olayı koruyup korumadığı."),

 ("ozet", "Uzunluk talimatına uyarak özet",
  "Şu metni EN FAZLA 15 kelimeyle özetle: «Kahve bitkisi ilk olarak Etiyopya'da "
  "keşfedildi. Oradan Yemen'e, sonra Osmanlı üzerinden Avrupa'ya yayıldı. Bugün "
  "dünyanın en çok tüketilen içeceklerinden biridir.»",
  [I("uzunluk_maks", 160), I("herhangi_biri", ["kahve", "Kahve"])],
  "Özetleme ile talimat takibi birlikte. 15 kelime ≈ 160 karakter üst sınırıyla "
  "yaklaşık ölçülüyor — kelime saymak yerine karakter kullanmak yanlış negatifi azaltır."),

 ("ozet", "Bilgi çıkarma — metinde geçen sayı",
  "Şu metinde kaç yıl geçmiş? «Fabrika 1950'de kuruldu ve 1985'te kapandı.»",
  [I("sayi", 35)],
  "Özet değil çıkarım, ama aynı aile: metni okuyup üstünde işlem yapma."),

 # ── çeviri (4) ─────────────────────────────────────────────────────────────
 ("ceviri", "Türkçe → İngilizce, basit cümle",
  "Şu cümleyi İngilizceye çevir: «Yarın sabah erken kalkmam gerekiyor.»",
  [I("dil", "en"), I("herhangi_biri", ["tomorrow", "Tomorrow"]),
   I("herhangi_biri", ["early", "wake", "get up"])],
  "Çeviri yeteneği çok dilli kontrolün merkezi (§9). Üç iddia: dil doğru mu, "
  "zaman zarfı korunmuş mu, eylem korunmuş mu."),

 ("ceviri", "İngilizce → Türkçe, basit cümle",
  "Translate to Turkish: «The meeting was postponed until next week.»",
  [I("dil", "tr"), I("herhangi_biri", ["ertelen", "hafta"])],
  "Ters yön. Talimatın kendisi İngilizce — model hangi dilde cevap vereceğini "
  "talimattan değil içerikten çıkarmalı."),

 ("ceviri", "Deyim çevirisi — birebir çeviri tuzağı",
  "Şu İngilizce deyimi Türkçeye çevir ve ne anlama geldiğini yaz: «It's raining cats and dogs.»",
  [I("dil", "tr"), I("herhangi_biri", ["şiddetli", "bardak", "çok yağmur", "sağanak"])],
  "Birebir çeviri ('kediler ve köpekler yağıyor') yanlıştır ama iddia onu "
  "yasaklamıyor — anlamın verilmesini arıyor. Yasaklamak yanlış negatif üretirdi: "
  "iyi bir cevap birebir çeviriyi ÖRNEK olarak verebilir."),

 ("ceviri", "Teknik terim — alan dışı kelime dağarcığı",
  "«Machine learning model» ifadesinin Türkçe karşılığı nedir?",
  [I("dil", "tr"), I("herhangi_biri", ["makine öğren", "öğrenme model"])],
  "Alan dışı terim. BıRAG verisi bağımlılık alanında; teknik dağarcığın silinip "
  "silinmediğini gösterir."),

 # ── İngilizce yanıt (3) ────────────────────────────────────────────────────
 ("ingilizce", "İngilizce soruya İngilizce yanıt",
  "What is the capital of Japan? Answer in one sentence.",
  [I("dil", "en"), I("herhangi_biri", ["Tokyo", "Tokyo'"])],
  "K48 ölçtü: eğitim verisi tamamen Türkçe ve system prompt Türkçe. Modelin "
  "İngilizce soruya İngilizce cevap verme yeteneği eğitimden sonra ölçülmeli."),

 ("ingilizce", "İngilizce talimat takibi — biçim + dil",
  "List exactly three colours. Use a bulleted list, nothing else.",
  [I("madde_sayisi", 3),
   I("icermez", ["kırmızı", "mavi", "yeşil", "sarı", "siyah", "beyaz",
                 "turuncu", "mor", "pembe", "kahverengi"])],
  "İlk yazımda `dil='en'` iddiası vardı ve **doğru cevabı reddediyordu**: "
  "«- red / - blue / - green» üç renk adından ibaret, hiçbir işlev sözcüğü yok, "
  "dil sezimi haklı olarak 'belirsiz' diyor. Bu gerçek bir belirsizlik, sezicinin "
  "kusuru değil. Onun yerine **yokluk** iddiası kullanıldı: Türkçe renk adları "
  "kapalı ve kısa bir liste, geçerse cevap Türkçedir. `golden_checks` ilkesinin "
  "burada da geçerli olduğu yer — cevap uzayı kapalı DEĞİLKEN yokluğa dön."),

 ("ingilizce", "İngilizce akıl yürütme",
  "If a train leaves at 14:00 and the journey takes 3 hours, what time does it arrive? "
  "Answer in English.",
  [I("dil", "en"), I("herhangi_biri", ["17:00", "5 pm", "5pm", "5 p.m."])],
  "Dil + aritmetik birlikte. Türkçe cevap verirse `dil` iddiası düşer ve bu, "
  "K48'in ölçtüğü dil kaymasının eğitim sonrası hâlini gösterir."),

 # ── talimat takibi (5) ─────────────────────────────────────────────────────
 ("talimat", "Sayılı liste — tam sayı",
  "Bana tam olarak 4 madde halinde meyve ismi yaz. Başka hiçbir şey yazma.",
  [I("madde_sayisi", 4)],
  "Biçim talimatı. 'Tam olarak' denmiş; 3 ya da 5 madde başarısızlıktır."),

 ("talimat", "Uzunluk sınırı",
  "Bir cümleyle cevapla: Deniz neden mavi görünür?",
  [I("uzunluk_maks", 300), I("herhangi_biri", ["ışık", "dalga", "yansı", "mavi"])],
  "Talimat + içerik birlikte. Doğru ama üç paragraflık bir cevap bu öğede düşer."),

 ("talimat", "Olumsuz talimat — bir şeyi YAPMAMA",
  "Bana madde madde üç şehir ismi say. İstanbul'u yazma, başka bir şey de yazma.",
  [I("madde_sayisi", 3), I("icermez", ["İstanbul"])],
  "Olumsuz talimat takibi ayrı bir yetenek ve dil modellerinde bilinen zayıf nokta. "
  "⚠️ İlk yazımda tek iddia (`icermez`) vardı ve öğe **boştu**: «Bilmiyorum.» diyen "
  "bir cevap da geçiyordu. Negatif sınama bunu yakaladı. `madde_sayisi` eklenerek "
  "cevabın içerik taşıması zorunlu kılındı; talimat da madde istemeye çevrildi ki "
  "iddia görevle uyumlu olsun."),

 ("talimat", "Biçim talimatı — JSON",
  "Şu bilgiyi JSON olarak ver: ad Ayşe, yaş 30. Sadece JSON yaz.",
  [I("icerir", ["{", "}", "Ayşe"]), I("sayi", 30)],
  "Yapılandırılmış çıktı. Fine-tune sohbet biçimine odaklandığı için yapılandırılmış "
  "çıktı yeteneği unutmaya açık."),

 ("talimat", "Çok adımlı talimat",
  "Önce 5 ile 6'yı çarp, sonra sonuca 10 ekle, sadece son sayıyı yaz.",
  [I("sayi", 40), I("uzunluk_maks", 150)],
  "İki talimat sırayla. Ara sonucu (30) yazarsa `uzunluk_maks` genelde yine geçer; "
  "asıl ölçülen doğru sonuca ulaşmak."),

 # ── genel kültür / olgu (5) ────────────────────────────────────────────────
 ("genel_kultur", "Coğrafya — temel olgu",
  "Türkiye'nin başkenti neresidir?",
  [I("icerir", ["Ankara"]), I("uzunluk_maks", 200)],
  "Olgusal bilgi silinmiş mi. En temel düzey."),

 ("genel_kultur", "Bilim — temel olgu",
  "Suyun kimyasal formülü nedir?",
  [I("herhangi_biri", ["H2O", "H₂O"]), I("uzunluk_maks", 200)],
  "Alt simge yazımı iki varyantla kabul ediliyor."),

 ("genel_kultur", "Tarih — tarih bilgisi",
  "Türkiye Cumhuriyeti hangi yıl kuruldu?",
  [I("sayi", 1923)],
  "Yıl bilgisi. `sayi` sınır kontrolü sayesinde '11923' gibi bir bozulma kabul edilmez."),

 ("genel_kultur", "Edebiyat — eser–yazar eşleşmesi",
  "«Kürk Mantolu Madonna» adlı romanın yazarı kimdir?",
  [I("icerir", ["Sabahattin Ali"])],
  "Türkçe kültürel bilgi. Çok dilli modellerde bu tür yerel bilgi unutmaya en "
  "açık katmanlardan biri."),

 ("genel_kultur", "Birim dönüşümü",
  "1 kilometre kaç metredir?",
  [I("sayi", 1000), I("uzunluk_maks", 200)],
  "Basit dönüşüm; aritmetikten farklı olarak ezberlenmiş bir olgu."),
]


# ── Öz-sınama: ELLE yazılmış doğru cevaplar iddialardan GEÇMELİ ──────────────
# Bir eval öğesinin en tehlikeli kusuru fazla katı iddiadır: model doğru davranır,
# alet "başarısız" der, veri o yöne revize edilir (golden_checks başlığı, K40, K65).
# İlk yazımda bu sınama 30 öğenin 5'inde yanlış negatif buldu; hepsi `dil` iddiasıydı
# ve dil sezimi kısa cümlelerde çöküyordu. Sınama artık kalıcı: betik her koştuğunda
# doğrulanıyor ve düşerse betik DURUYOR.
DOGRU_CEVAPLAR = {
 "fs-001": "51",
 "fs-002": "Şimdi 41 kalem var.",
 "fs-003": "İndirim 50 lira, yeni fiyat 150 lira.",
 "fs-004": "Evet.",
 "fs-005": "En kısa Can.",
 "fs-006": "İkisi de eşit ağırlıktadır; her ikisi de bir kilo.",
 "fs-007": "def topla(a, b):\n    return a + b",
 "fs-008": "[x for x in liste if x % 2 == 0]",
 "fs-009": "Listede olmayan bir indekse erişmeye çalıştınız; indeks listenin sınırları dışında.",
 "fs-010": "SELECT * FROM kullanicilar WHERE yas > 18;",
 "fs-011": "Marie Curie, fizik ve kimyada çalışmış, iki dalda Nobel kazanan ilk kişidir.",
 "fs-012": "Kahve Etiyopya'da bulundu, Yemen ve Osmanlı yoluyla yayıldı.",
 "fs-013": "35 yıl.",
 "fs-014": "I need to get up early tomorrow morning.",
 "fs-015": "Toplantı gelecek haftaya ertelendi.",
 "fs-016": "Birebir çevirisi 'kedi ve köpek yağıyor' olur; anlamı şiddetli yağmur yağdığıdır.",
 "fs-017": "Makine öğrenmesi modeli.",
 "fs-018": "The capital of Japan is Tokyo.",
 "fs-019": "- red\n- blue\n- green",
 "fs-020": "It arrives at 17:00.",
 "fs-021": "- elma\n- armut\n- muz\n- kiraz",
 "fs-022": "Deniz, güneş ışığının mavi dalga boylarını daha çok saçması nedeniyle mavi görünür.",
 "fs-023": "- Ankara\n- İzmir\n- Bursa",
 "fs-024": '{"ad": "Ayşe", "yas": 30}',
 "fs-025": "40",
 "fs-026": "Ankara.",
 "fs-027": "H2O",
 "fs-028": "1923 yılında kuruldu.",
 "fs-029": "Sabahattin Ali.",
 "fs-030": "1 kilometre 1000 metredir.",
}


# Reddetme/kaçamak cevapları: HİÇBİR öğe bunları geçirmemeli. Geçiriyorsa öğe
# BOŞTUR — iddia hiçbir şey talep etmiyordur. (İlk yazımda `fs-023` böyleydi.)
KACAMAK = ["Bilmiyorum.", "I don't know.", "Bu konuda yardımcı olamam.", ""]


def negatif_sinama(ogeler: list[dict]) -> list[str]:
    """Kaçamak cevabı GEÇİREN öğe var mı? Boş liste = temiz."""
    return [f"{o['id']}: «{y}» tüm iddialardan geçti — öğe boş"
            for o in ogeler for y in KACAMAK
            if all(sc.denetle(i, y)[0] for i in o["iddialar"])]


def oz_sinama(ogeler: list[dict]) -> list[str]:
    """Doğru cevabı reddeden iddia var mı? Boş liste = temiz."""
    hata = []
    for o in ogeler:
        c = DOGRU_CEVAPLAR.get(o["id"])
        if c is None:
            hata.append(f"{o['id']}: doğru cevap örneği yazılmamış")
            continue
        for i in o["iddialar"]:
            gecti, kanit = sc.denetle(i, c)
            if not gecti:
                hata.append(f"{o['id']}: `{i['kural']}`={i['deger']!r} DOĞRU cevabı "
                            f"reddetti ({kanit})")
    return hata


def main() -> int:
    ogeler = []
    for i, (kat, sonda, mesaj, iddialar, notu) in enumerate(OGELER, 1):
        ogeler.append({
            "id": f"fs-{i:03d}", "eksen": 3, "kategori": kat, "sonda": sonda,
            # ⚠️ system YOK — bkz. betik başlığı.
            "messages": [{"role": "user", "content": mesaj}],
            "iddialar": iddialar, "not": notu})

    ihlaller = {o["id"]: ih for o in ogeler if (ih := sc.oge_kapilari(o))}
    yanlis_negatif = oz_sinama(ogeler)
    bos_oge = negatif_sinama(ogeler)
    CIKTI.write_text("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in ogeler))
    yaz_rapor(ogeler, ihlaller)
    print(f"{len(ogeler)} öğe → {CIKTI.relative_to(KOK)}")
    print(f"kapı: {len(ogeler)-len(ihlaller)}/{len(ogeler)}")
    print(f"öz-sınama (doğru cevaplar geçiyor mu): "
          f"{'TEMİZ' if not yanlis_negatif else f'{len(yanlis_negatif)} YANLIŞ NEGATİF'}")
    print(f"negatif sınama (kaçamak cevap eleniyor mu): "
          f"{'TEMİZ' if not bos_oge else f'{len(bos_oge)} BOŞ ÖĞE'}")
    for oid, ih in ihlaller.items():
        print(f"  İHLAL {oid}: {ih}")
    for h in yanlis_negatif:
        print(f"  YANLIŞ NEGATİF {h}")
    for h in bos_oge:
        print(f"  BOŞ ÖĞE {h}")
    return 1 if (ihlaller or yanlis_negatif or bos_oge) else 0


def yaz_rapor(ogeler: list[dict], ihlaller: dict) -> None:
    kat = collections.Counter(o["kategori"] for o in ogeler)
    kur = collections.Counter(i["kural"] for o in ogeler for i in o["iddialar"])
    y = ["# `forgetting_smoke.jsonl` — Eksen 3 duman seti", "",
         f"**Çıktı:** `evals/forgetting_smoke.jsonl` · SHA256 "
         f"`{hashlib.sha256(CIKTI.read_bytes()).hexdigest()}`  ",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
         f"**Öğe:** {len(ogeler)} · **Kapı:** {len(ogeler)-len(ihlaller)}/{len(ogeler)}", "",
         "---", "",
         "## 0. Bu set ne ölçer, ne ölçmez", "",
         "**Ölçer:** eğitim sonrası genel yeteneğin ÇÖKÜP çökmediği (§9).", "",
         "**Ölçmez:** yetenek tavanı. Öğeler bilerek kolay — baz model zaten geçmeli ki",
         "düşüş görünsün. Zor öğelerden kurulu bir set, baz modelin de düştüğü yerde",
         "LoRA'nın etkisini gizler.", "",
         "⚠️ **Bu bir kapı değil, bir alarm.** Kaç öğe düşerse durdurucu olduğu Faz 4'te",
         "baseline ölçüldükten sonra konur; şimdi eşik koymak uydurma olur.", "",
         "## 1. System prompt neden YOK", "",
         "K19 promptu konsaydı bu öğelerin çoğunda doğru davranış **reddetmek** olurdu",
         "(`golden.dev`'in `kapsam_disi` dilimi tam onu ölçüyor) ve set persona uyumunu",
         "ölçmeye başlardı. Eksen 3'ün sorusu ağırlıklarla ilgili: *genel yetenek duruyor mu*.",
         "Replay diliminin boş-system varyantıyla aynı gerekçe (K88/K89).", "",
         "## 2. Neden burada VARLIK iddiası meşru", "",
         "`golden_checks.py` otomatik iddiaların yalnızca **yokluk** iddia edebileceğini",
         "söylüyor ve Eksen 1 için haklı: Türkçe serbest terapötik metinde \"şu davranış",
         "olsun\" demek yanlış negatif üretir, çünkü davranışın sonsuz çok yazılışı var.", "",
         "Eksen 3'te cevap uzayı **kapalı**: *\"17×3\"* tek cevaplı. Sınır açık yazılı",
         "(`src/smoke_checks.py`): bir iddia ancak cevabın doğruluğu metinden **mekanik**",
         "doğrulanabiliyorsa buraya yazılır. *\"Özet iyi mi\"* yazılamaz; *\"özet şu özel adı",
         "içeriyor mu\"* yazılabilir.", "",
         "## 3. Kategoriler", "", "| Kategori | Öğe |", "|---|---:|"]
    for k, n in kat.most_common():
        y.append(f"| `{k}` | {n} |")
    y += ["", "## 4. İddia kuralları", "", "| Kural | Kullanım |", "|---|---:|"]
    for k, n in kur.most_common():
        y.append(f"| `{k}` | {n} |")
    y += ["", f"Öğe başına ortalama **{sum(kur.values())/len(ogeler):.1f}** iddia. "
          "Hepsi deterministik — **bu sette judge yok**, dolayısıyla K103'ün ölçtüğü",
          "oynaklık bu ekseni hiç etkilemiyor.", "",
          "## 5. Öğeler", "", "| # | Kategori | Sonda |", "|---|---|---|"]
    for o in ogeler:
        y.append(f"| `{o['id']}` | {o['kategori']} | {o['sonda']} |")
    y += ["", "## 6. Öz-sınama — iddialar doğru cevabı reddediyor mu", "",
          "Bir eval öğesinin en tehlikeli kusuru **fazla katı iddia**dır: model doğru",
          "davranır, alet \"başarısız\" der, veri o yöne revize edilir (K40, K65).", "",
          "Bu yüzden her öğe için elle bir **doğru cevap örneği** yazıldı ve betik her",
          "koştuğunda bunların tüm iddialardan geçtiğini doğruluyor. Geçmezse betik durur.", "",
          "İlk yazımda sınama **5 yanlış negatif** buldu — hepsi `dil` iddiasıydı ve dil",
          "sezimi kısa cümlelerde (*\"It arrives at 17:00.\"*) çöküyordu. İki düzeltme:",
          "Türkçeye özgü harf sinyali eklendi ve işlev sözcüğü listeleri genişletildi.",
          "Beşincisi (`fs-019`, üç renk adı) gerçekten belirsizdi — orada `dil` iddiası",
          "**yokluk** iddiasıyla değiştirildi.", "",
          "### 6a. Negatif sınama — iddia gerçekten bir şey talep ediyor mu", "",
          "Ters kusur da ölçülüyor: bir öğe **boş** olabilir, yani iddiaları hiçbir şey",
          "talep etmeyebilir. Betik her öğeye kaçamak cevaplar veriyor (*\"Bilmiyorum.\"*,",
          "*\"I don't know.\"*, *\"Bu konuda yardımcı olamam.\"*, boş dize) ve hepsinin",
          "elenmesini bekliyor.", "",
          "İlk yazımda **`fs-023` boştu**: tek iddiası `icermez=[İstanbul]` olduğu için",
          "*\"Bilmiyorum.\"* de geçiyordu. Yokluk iddiası tek başına asla yeterli değil —",
          "yanına içerik talep eden bir iddia gerekiyor.", "",
          "## 7. Bilinen sınırlar", "",
          "- **Dil sezimi frekans temelli.** Çok kısa cevaplarda (`belirsiz`) yanılabilir;",
          "  bu yüzden `dil` iddiası hep başka bir iddiayla birlikte kullanıldı.",
          "- **Özet kalitesi ölçülmüyor**, yalnızca ana özel adın korunması. Kalite",
          "  ölçümü judge gerektirir ve bu setin amacı dışında.",
          "- **Kod çalıştırılmıyor**, deyim içeriyor mu diye bakılıyor. Çalıştırmak",
          "  sandbox gerektirir; duman seti için maliyet/fayda tutmuyor.", ""]
    RAPOR.write_text("\n".join(y) + "\n")


if __name__ == "__main__":
    sys.exit(main())
