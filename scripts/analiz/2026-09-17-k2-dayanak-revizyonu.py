#!/usr/bin/env python3
"""K2 — judge'ın DAYANAKSIZ bulduğu iddiaları düzeltir.

⛔⛔ **En büyük sınıf tek bir kusurdu: 16 kayıt kurumun NE YAPTIĞINI ya da NE
ZAMAN AÇIK OLDUĞUNU dayanaksız iddia ediyordu** — *«bugün gidilebilecek en
yakın yer»*, *«ikisi de gece açık»*, *«gitmek için randevu gerekmiyor»*,
*«bu hafta gidilebilecek yerler»*. Bu tam olarak §8b′'nin yasakladığı şey ve
kayıtların hepsi §8b′ yazılmadan ÖNCE üretildi.

⭐ **Düzeltme biçimi bilgiyi silmek DEĞİL, yanlış kesinliği silmek:** kurum
TÜRÜ söylenir, erişilebilirliği açıkça reddedilir (*«hangi kapının açık
olduğunu buradan bilemem»*). Bilgiyi silmek gece sokakta olan birinden
barınma biriminin varlığını gizlerdi; asıl kusur varlık değil, **kesinlik**.

➡️ *Bir kurumu anmak ile o kurumun kapısının açık olduğunu söylemek ayrı
iddialardır; ikincisi bende olmayan bir bilgidir ve eğitim verisinde
uydurulmuş bir yordam, modele yordam uydurmayı öğretir.*

⛔ **Dört bayrak DÜZELTİLMEDİ — araç eseri sayıldı ve gerekçesi yazılıdır:**
`teselli_dayanak_alintisi` rubrikte zorunlu bir seçimdir; cevapta gerçek bir
olgu tesellisi yoksa judge *«Buradayım.»* gibi **asistanın kendine dair**
cümlesini seçer ve ona dayanak bulamaz. Bu bir uydurma değil, seçimin
zorunlu olmasının yan ürünü.
"""
from __future__ import annotations
import json
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = "2026-09-17"
YORDAM = "§8b′ kurum yordamı"
AYRINTI = "K120 dayanak"

# ⛔⛔ **SESSİZ ÜZERİNE YAZMA BURADA BİR DÜZELTMEYİ YUTTU.** İlk yazımda anahtar
# `(parti, sıra)` idi ve `v5-parti8 #45` için İKİ düzeltme yazılmıştı; Python
# sözlüğü aynı anahtarı ikinci kez görünce birincisini **sessizce** attı ve
# yordam düzeltmesi hiç uygulanmadı — betik yine de «9 kayıt revize» dedi.
# ➡️ *Bir sözlük literali, aynı anahtarı iki kez yazmayı bir hata saymaz; bu
#    yüzden «kaç düzeltme yazdım» ile «kaç düzeltme uygulandı» ayrı sayılardır
#    ve ikincisi raporlanmıyorsa fark görünmez.*
# ⇒ Anahtara sıra numarası eklendi (aynı kayda birden çok düzeltme meşru) ve
#   `_yinelenme_denetimi()` betiğin KENDİ kaynağını okuyup yinelenme ararsa durur.
D: dict[tuple, tuple[str, str, str, str]] = {

# ── A. Kurum yordamı / erişilebilirlik iddiası (§8b′) ───────────────────────
 ("v5-parti4", 42): (
   'Ama bunu bugün birinin görmesi gerekiyor: aile hekimi ya da bir acil poliklinik, bugün gidilebilecek en yakın yer.',
   'Ama bunu bugün bir hekimin görmesi gerekiyor. Hangi kapının bugün sana açık olduğunu buradan bilemem; bildiğim tek şey, bunun yarına bırakılacak bir şey olmadığı.',
   YORDAM, "«bugün gidilebilecek en yakın yer» kurumun erişilebilirliğini iddia ediyordu."),

 ("v5-parti4", 57): (
   'Nereden bulunacağını söyleyebilirim: aile sağlık merkezlerinde hekim değişikliği yapılabiliyor ve bunu kişinin kendisi talep ediyor. Nasıl işlediğini buradan anlatamam, o bilgi bende yok; ilk adım kayıtlı olduğun merkeze bunu sormak olabilir.',
   'Nereden bulunacağını ben söyleyemem — hekim değiştirmenin nasıl işlediği, nereye başvurulduğu bende olan bir bilgi değil ve buradan uydurulmuş bir yordam seni boşa yorar. Sorabileceğin yer kayıtlı olduğun sağlık kuruluşu; ne cevap vereceklerini de bilmiyorum.',
   YORDAM, "Bağlam belgesi YOKKEN mevzuat anlatılıyordu («hekim değişikliği yapılabiliyor ve bunu kişinin kendisi talep ediyor»)."),

 ("v5-parti6", 2): (
   'Soracak yer var: okulun rehberlik birimi, bir de aile hekimliği. İkisi de bu soruyu karşılayabilecek yerde; ilk adım, hangisine gitmek sana daha kolay geliyorsa oraya bu cümleyi olduğu gibi söylemek olabilir.',
   'Nereye sorabileceğini tam olarak bilemem — hangi kapının sana açık olduğu buradan görünmüyor. Aklıma gelen iki yer var: okulunda bir rehberlik birimi varsa orası, bir de aile hekimliği. Ne cevap vereceklerini bilmiyorum; ama bu cümleyi olduğu gibi söylemek işe yarar.',
   YORDAM, "«İkisi de bu soruyu karşılayabilecek yerde» kurumun yetkinliğini iddia ediyordu. §8d′'nin «varsa»sı da eklendi: her okulda rehberlik birimi olduğu varsayılamaz."),

 ("v5-parti6", 17): (
   'Söyleyebileceğim şu: bunu bugün seni taburcu eden ekibe sormak gerekiyor. İlk adım, "ağrı yine başladı" demek ve çekmecedeki eski kutuyu da söylemek olabilir — telefonla da olur.',
   'Söyleyebileceğim şu: bunu bugün sizi taburcu eden ekibin bilmesi gerekiyor. Onlara nasıl ulaşılacağını buradan bilemem. Söylenecek şey ise kısa: "ağrı yine başladı" ve çekmecedeki eski kutu.',
   YORDAM, "«telefonla da olur» bir erişim biçimini iddia ediyordu. ⭐ Ayrıca register düzeltildi: kayıt «siz» kullanıyor, bu paragraf «sen»e kaymıştı."),

 ("v5-parti6", 34): (
   'bunların ne olduğunu ben söyleyemem, ama bugün birinin görmesi gerekiyor: aile hekimi ya da bir acil poliklinik, bugün gidilebilecek en yakın yer.',
   'bunların ne olduğunu ben söyleyemem, ama bugün bir hekimin görmesi gerekiyor. Hangi kapının bugün sana açık olduğunu buradan bilemem; bildiğim tek şey, bunun yarına bırakılacak bir şey olmadığı.',
   YORDAM, "parti4 #42 ile aynı cümle, aynı kusur."),

 ("v5-parti6", 43): (
   'bu yükü yalnız taşımak zorunda değilsin ve bunun için bir yer var — hasta yakınlarına destek veren danışmanlık hizmetleri, bir de hastanenin sosyal hizmet birimi. İlk adım, yarın vizitte "ben de konuşabileceğim biri var mı" diye sormak olabilir.',
   'bu yükü yalnız taşımak zorunda değilsin. Nereye gidileceğini kesin olarak söyleyemem — hangi birimin orada olduğunu, ne yaptığını bilmiyorum. Aklıma gelen: hasta yakınlarına destek veren danışmanlık hizmetleri, bir de hastanelerin sosyal hizmet birimleri. Yarın yanına gelen kim olursa, "ben de konuşabileceğim biri var mı" diye sormak bir başlangıç olabilir.',
   YORDAM, "«yarın vizitte» bir vizitin varlığını iddia ediyordu; kullanıcı yalnız «çocuklar yarın geliyor» dedi ⇒ onun kendi sözüne bağlandı."),

 ("v5-parti6", 45): (
   'Kural tarafını merak ediyorsan onu bilen yer de belli: çalıştığın kurumun kendi düzeni, bir de meslek odası. İlk adım, kuralın ne dediğini tartışmadan önce okumak olabilir.',
   'Kural tarafını buradan söyleyemem — nerede çalıştığını, hangi kuralın geçerli olduğunu bilmiyorum. Kuralın ne dediğini tartışmadan önce okumak bir başlangıç olabilir.',
   YORDAM, "«onu bilen yer de belli» hem kurumun varlığını hem yetkinliğini iddia ediyordu."),

 ("v5-parti7", 3): (
   'Bunun kaydını tutan bağımsız bir yer var: bir mali müşavir ya da borç danışmanlığı veren kurumlar aynı üç ayı senden bağımsız okuyabilir. İlk adım, üç aylık giren ve çıkanı yan yana yazmak olabilir.',
   'Kaydı senden bağımsız tutabilecek biri var mı, onu buradan bilemem. Ama üç aylık giren ve çıkanı yan yana yazmak senin elinde — o hesabı kimseye sormadan yapabilirsin.',
   YORDAM, "«aynı üç ayı senden bağımsız okuyabilir» kurumun ne yaptığına dair uydurulmuş bir iddiaydı."),

 ("v5-parti7", 13): (
   'Söyleyebileceğim tek şey şu: bu tabloyu bugün bir hekimin görmesi gerekiyor. Acil poliklinik bugün gidilebilecek en yakın yer ve gitmek için randevu gerekmiyor. Yanında biri varsa onunla gitmek daha iyi olur.',
   'Söyleyebileceğim tek şey şu: bu tabloyu bugün bir hekimin görmesi gerekiyor. Hangi kapının açık olduğunu, nasıl gidileceğini buradan bilemem — ama bunu yarına bırakmamak önemli. Yanında biri varsa onunla gitmek daha kolay olur.',
   YORDAM, "«gitmek için randevu gerekmiyor» doğrudan bir yordam iddiasıydı ve bağlam belgesi yoktu."),

 ("v5-parti7", 17): (
   'bu saatte gidilebilecek yerler var — bir acil poliklinik ya da belediyenin barınma birimi, ikisi de gece açık. İlk adım, en yakınına gitmek ya da birine telefon açmak olabilir.',
   'belediyelerin barınma birimleri ve acil poliklinikler var; hangisinin bu saatte açık olduğunu ya da sana ne kadar uzak olduğunu buradan bilemem. Birine telefon açabilmen de bir yol.',
   YORDAM, "⛔ «ikisi de gece açık» iddiası, gece sokakta olan birini KAPALI bir kapıya gönderebilirdi. ⭐ Kurum türü SİLİNMEDİ — silmek kişiden bilgiyi gizlerdi; silinen şey kesinlik."),

 ("v5-parti7", 22): (
   'Bu gece için söyleyebileceğim tek şey: bu soruyu bu saatte cevaplayabilecek bir yer var, eczanelerin nöbetçisi ya da bir acil poliklinik.',
   'Bu gece için söyleyebileceğim tek şey: nöbetçi eczaneler ve acil poliklinikler var, ama hangisinin bu saatte sana açık olduğunu buradan bilemem.',
   YORDAM, "«bu soruyu bu saatte cevaplayabilecek bir yer var» hem erişilebilirlik hem yetkinlik iddiasıydı."),

 ("v5-parti8", 26): (
   'Aile hekimliği ya da öğrenci sağlık birimi, ikisi de bu hafta gidilebilecek yerler.',
   'Aile hekimliği aklıma gelen yer; okulunda bir sağlık birimi varsa o da olur. Hangisinin sana ne zaman açık olduğunu buradan bilemem.',
   YORDAM, "«ikisi de bu hafta gidilebilecek yerler» erişilebilirlik iddiasıydı."),

 ("v5-parti8", 28): (
   'öğrenci sağlık birimi ya da aile hekimliği, ikisi de bu hafta gidilebilecek yerler.',
   'aile hekimliği, ya da yurdunun bağlı olduğu bir sağlık birimi varsa orası. Hangisinin ne zaman açık olduğunu buradan bilemem.',
   YORDAM, "parti8 #26 ile aynı cümle, aynı kusur."),

 ("v5-parti8", 37): (
   'Ama hesabı sizden bağımsız çıkarabilecek yerler var: bütçe danışmanlığı veren birimler ve borç danışmanlığı. İlk adım, bir ayın gidenini ve kalanını yan yana yazmak olabilir.',
   'Bütçe ya da borç danışmanlığı veren yerler var ama size açık olup olmadığını buradan bilemem. Bir ayın gidenini ve kalanını yan yana yazmak ise kimseye sormadan yapılabilir.',
   YORDAM, "«hesabı sizden bağımsız çıkarabilecek yerler var» kurumun ne yaptığını iddia ediyordu."),

 ("v5-parti8", 39): (
   'Bunu birlikte hesaplayabilecek yerler var: borç danışmanlığı veren kurumlar. İlk adım, son üç ayın giden ve kalanını yan yana yazmak olabilir.',
   'Borç danışmanlığı veren yerler var ama sana açık olup olmadığını buradan bilemem. Son üç ayın gideniyle kalanını yan yana yazmak ise kimseye sormadan yapılabilir.',
   YORDAM, "«birlikte hesaplayabilecek» kurumun yöntemini iddia ediyordu."),

 ("v5-parti8", 45, 1): (
   'Ama bunu konuşabileceğin yerler var: emeklilere yönelik çalışan halk eğitim ve belediye birimleri. İlk adım, en yakınına bir kez uğramak olabilir.',
   'Halk eğitim merkezleri ve belediyelerin birimleri var ama senin oturduğun yerde ne olduğunu, kimi kabul ettiğini buradan bilemem. Bir kez uğrayıp sormak, benim sayacağım her şeyden daha çok bilgi verir.',
   YORDAM, "«emeklilere yönelik çalışan» kurumun hedef kitlesini iddia ediyordu."),

 ("v5-parti8", 45, 2): (
   'Vakit geçmiyor dedin. Onu söyleyen biri, geçirecek bir şey arıyor demektir.',
   '"Elim hep pakette" dedin. Paket, boşalan bir şeyin yerini tutuyor olabilir.',
   AYRINTI, "⛔ «Vakit geçmiyor dedin» kullanıcıya SÖYLEMEDİĞİ bir cümleyi atfediyordu — "
   "yani aynı anda hem dayanak hem ALINTI kusuru (T105). ⭐ Bu düzeltme bir kez "
   "SESSİZCE YUTULMUŞTU: sözlükte aynı anahtar iki kez yazılmıştı."),

# ── B. Uydurulmuş kullanıcı ayrıntısı (K120) ────────────────────────────────
 ("v5-parti4", 6): (
   'İkisini de kimse senden istemedi.',
   'İkisini de kimsenin istediğini yazmadın.',
   AYRINTI, "«kimse istemedi» sevgili hakkında bir olgu iddiasıydı; kullanıcı yalnız kendi söylediğini yazdı."),

 ("v5-parti4", 36): (
   'Kazanıp kazanmadığını ben bilmiyorum ve bilemem de — ama şunu söyleyebilirim: kaybettiği günleri paylaşan birini görmedin, çünkü paylaşsaydı tüyo satamazdı.',
   'Kazanıp kazanmadığını ben bilmiyorum ve bilemem de. Bildiğim tek şey, senin de bilmiyor olduğun — yoksa bunu bana sormazdın.',
   AYRINTI, "⛔ İKİNCİ DÜZELTME. İlk revizyonda kapanış cümlesi düzeltilmişti ama judge aynı kayıtta BAŞKA bir uydurmayı gösterdi: «görmedin» kullanıcının ne gördüğünü, «tüyo satamazdı» adamın güdüsünü iddia ediyor. Yeni cümle yalnız konuşmanın kendisine dayanıyor: kullanıcı SORDU."),

 ("v5-parti5", 17): (
   'Eşinle aranızdaki bir konuda taraf tutmak',
   'Aranızdaki bir konuda taraf tutmak',
   AYRINTI, "Kullanıcı «kadın» dedi, «eşim» demedi; ilişki türü çıkarımdı."),

 ("v5-parti5", 42): (
   'Kapı kapandıktan sonra kendine kızman, kapı kapanmadan önce fark etmediğin bir şeyi fark etmiş olduğunu gösteriyor.',
   '"İyiyim" dedikten sonra buraya "aslında neredeyse hiç kalmadı" diye yazman, iki cümlenin arasındaki farkı senin gördüğünü gösteriyor.',
   AYRINTI, "Ne «kapı» ne «kendine kızmak» konuşmada var — mecazın öncülü de duygu da uydurmaydı."),

 ("v5-parti5", 44): (
   'Orada duran tek şey sigara değil demek ki; yarım saati dolduran başka bir şey var ve onun adını sen koymamışsın henüz.',
   'Orada duran tek şey sigara olmayabilir; yarım saati dolduran başka bir şey de olabilir ve onun adını henüz koymadın.',
   AYRINTI, "İddia olgu kipinden OLASILIK kipine çevrildi (rubrik: `ayrinti_hipotez_olarak_isaretli`). Cümlenin işlevi korundu."),

 ("v5-parti5", 45): (
   'Bugün yaptığın tek şey onu bir yere yazmak oldu ve o da bir şey.',
   'Bunu bir yere yazdın ve o da bir şey.',
   AYRINTI, "«Bugün yaptığın tek şey» kullanıcının bütün gününü iddia ediyordu."),

 ("v5-parti5", 59): (
   'Kimseye söylemediğini yazıyorsun. Söylemediğin şeyi bugün buraya yazmışsın',
   'Bunu bugün buraya yazmışsın',
   AYRINTI, "Kullanıcı kimseye söylemediğini hiç yazmadı; cümle bunu ona atfediyordu."),

 ("v5-parti6", 25): (
   'bunu bugün orada birinin bilmesi gerekiyor: hemşireye ya da vizitteki hekime, "düşmeyi hatırlamıyorum" cümlesini olduğu gibi söylemek en yakın adım.',
   'bunu bugün bir hekimin bilmesi gerekiyor: "düşmeyi hatırlamıyorum" cümlesini olduğu gibi söylemek en yakın adım.',
   AYRINTI, "«orada», «hemşire», «vizitteki hekim» bir yatış durumunu varsayıyordu; konuşmada böyle bir bilgi yok."),

 ("v5-parti7", 33): (
   'Yatmak istemediğini bana söyleyebiliyorsun ama "peki" diyemediğini de yazdın — yani ona hayır demek de kolay değilmiş.',
   'Yatmak istemediğini bana söyleyebiliyorsun. Aynı cümleyi ona söylemek de bu kadar kolay mıydı, orasını bilmiyorum.',
   AYRINTI, "⛔ Kullanıcı «peki» diye bir şey YAZMADI; cevabın bütün çıkarımı olmayan bir tura dayanıyordu."),

 ("v5-parti7", 41): (
   'Ama saymak kendi başına bir şey: üç gündür düzgün uyuyamadığını da aynı cümlede söyledin.',
   'Ama saymak kendi başına bir şey ve saat iki olduğunu da sen yazdın.',
   AYRINTI, "⛔⛔ Uyku konuşmada HİÇ geçmiyor — üstelik hekime yönlendirme bu olmayan cümleye dayandırılmıştı."),

 ("v5-parti7", 57): (
   'Bir şeye katılmıyorum ama: "kendime gülüyorum" diye yazmamışsın, sadece kontrol ettiğini yazmışsın. Yani bu sefer gülmemişsin.',
   '"kendime gülüyorum" diye yazmamışsın, sadece kontrol ettiğini yazmışsın. Kontrol etmek, gülmekten başka bir şey.',
   AYRINTI, "«bu sefer» önceki bir gülme anını varsayıyordu; ayrıca kullanıcının hiç kurmadığı bir cümleye itiraz ediliyordu."),

 ("v5-parti8", 7): (
   'Bırakmaktan söz etmediğini de eklemişsin; ben de etmeyeceğim.',
   'Bırakmaktan söz etmedin; ben de etmeyeceğim.',
   AYRINTI, "«eklemişsin» kullanıcıya söylemediği bir edimi atfediyordu; yokluk olduğu gibi bırakıldı."),

 ("v5-parti8", 52): (
   'Doktorunun ne gördüğünü de ben bilemem — grafiği de öksürüğü de görmedim.',
   'Doktorunun ne gördüğünü de ben bilemem — ne seni gördüm ne öksürüğünü duydum.',
   AYRINTI, "«grafi» konuşmada yok; kullanıcı yalnız «sabahları az bir öksürük» dedi."),

 ("v5-parti8", 57): (
   'Yıllardır içtiğinizi de yazdınız; ilk defa garip olmuş.\n\nBunu konuşmak isterseniz yer var: aile hekimliği ve bırakma danışma birimleri. İlk adım, torununuzun cümlesini olduğu gibi söylemek olabilir.',
   'Onun cümlesi dün söylendi ve siz bugün buradasınız.\n\nBunu konuşmak isterseniz aile hekimliği ve bırakma danışma birimleri var; hangisinin size açık olduğunu buradan bilemem. İlk adım, torununuzun cümlesini olduğu gibi söylemek olabilir.',
   AYRINTI + " + " + YORDAM,
   "İki kusur birden: «Yıllardır içtiğinizi de yazdınız» — kullanıcı böyle bir şey yazmadı; «ilk defa garip olmuş» — «garip» de cevabın kendi sözcüğü. Ayrıca kurum erişilebilirliği iddiası kaldırıldı."),

 ("v5-parti8", 60): (
   'Grafide ne görüldüğüne dair bir şey söylemeyeceğim — onu gören ve söyleyen hekim, açması gereken de o.',
   'Ne görüldüğüne dair bir şey söylemeyeceğim — onu gören ben değilim.',
   AYRINTI, "Kullanıcı «bir şey görmüşler» dedi; «grafi» cevabın uydurması. «açması gereken de o» ayrıca hekime bir yükümlülük atfediyordu."),

}

# ⚠️ Düzeltilmeyenler — araç eseri, gerekçesi yazılı
ESER = {("v5-parti4", 35): "«Buradayım.» — asistanın kendine dair cümlesi; teselli dayanağı zorunlu seçim olduğu için işaretlendi",
        ("v5-parti7", 27): "«Buradayım.» — aynı",
        ("v5-parti5", 42): "teselli bayrağı ayrıntı bayrağıyla AYNI cümlede; ayrıntı düzeltilince düşer",
        }

GIRDI = {"v5-parti4": "data/candidates/v5-parti4.v3.jsonl",
         "v5-parti5": "data/candidates/v5-parti5.v3.jsonl",
         "v5-parti6": "data/candidates/v5-parti6.v3.jsonl",
         "v5-parti7": "data/candidates/v5-parti7.v3.jsonl",
         "v5-parti8": "data/candidates/v5-parti8.v3.jsonl"}


def _yinelenme_denetimi() -> None:
    """Betiğin kendi kaynağında yinelenen anahtar var mı? Varsa DUR."""
    import collections, re as _re
    kay = Path(__file__).read_text(encoding="utf-8")
    ks = _re.findall(r'^ \("(v5-parti\d)", (\d+)(?:, (\d+))?\): \(', kay, _re.M)
    c = collections.Counter(ks)
    yin = [k for k, v in c.items() if v > 1]
    if yin:
        raise SystemExit(f"⛔ Yinelenen anahtar, düzeltme sessizce yutulur: {yin}")
    print(f"⭐ {len(ks)} düzeltme girdisi, yinelenme yok")


def main() -> int:
    _yinelenme_denetimi()
    hata = 0
    for parti, gir in GIRDI.items():
        kayitlar = [json.loads(s) for s in (KOK / gir).read_text(encoding="utf-8").splitlines() if s.strip()]
        degisen = []
        uygulanan = 0
        for r in kayitlar:
            n = r["gen_meta"]["parti_sira"]
            islem = [v for k, v in D.items() if k[0] == parti and k[1] == n]
            if not islem:
                continue
            son = [m for m in r["messages"] if m["role"] == "assistant" and m.get("content")][-1]
            for eski, yeni, kural, gerekce in islem:
                if son["content"].count(eski) != 1:
                    print(f"  ⛔ EŞLEŞME {parti} #{n}: {son['content'].count(eski)} kez")
                    hata += 1
                    continue
                son["content"] = son["content"].replace(eski, yeni)
                uygulanan += 1
                r["gen_meta"].setdefault("revizyon", []).append(
                    {"tarih": TARIH, "kural": kural, "gerekce": gerekce, "kaynak": "judge K2"})
            r["judge"] = None
            degisen.append(n)
        cikti = KOK / f"data/candidates/{parti}.v4.jsonl"
        cikti.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in kayitlar),
                         encoding="utf-8")
        # ⭐ İKİ SAYI birden: kaç KAYIT ve kaç DÜZELTME. Eşitsizlik, yutulmuş
        # bir düzeltmeyi görünür kılar (yukarıdaki kusurun tam sebebi buydu).
        bekle = len([k for k in D if k[0] == parti])
        print(f"{parti}: {len(degisen)} kayıt · {uygulanan}/{bekle} düzeltme → {sorted(degisen)}")
        if uygulanan != bekle:
            print(f"  ⛔ {bekle - uygulanan} düzeltme UYGULANMADI")
            hata += 1
    print(f"\n⚠️ araç eseri sayılıp düzeltilmeyen: {len(ESER)}")
    for k, v in ESER.items():
        print(f"   {k[0]} #{k[1]}: {v}")
    return 1 if hata else 0


if __name__ == "__main__":
    raise SystemExit(main())
