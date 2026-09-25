#!/usr/bin/env python3
"""T22 vaka serisi — mekanik kapının Türkçe serbest metinde yanıldığı vakalar.

⛔⛔ **T22'nin açık kalemi:** *«K97 'yedinci örnek' diyor ama seri yazılı
değil; iddia ancak seri derlenince kurulur.»* Bu betik seriyi derler.

⭐ **ALMA ÖLÇÜTÜ — dar ve açık.** Bir vaka seriye girer ancak ve ancak:
  1. bir **mekanik kural** (dizge / düzenli ifade / sözlük) vardı,
  2. **Türkçe serbest metne** uygulandı,
  3. hükmü **yanlış** çıktı, ve
  4. yanlışlık, anlamın değil **yüzey biçiminin** bir özelliğine
     bağlanabildi (ek, eşseslilik, büyük harf, sözcük sınırı, ad/iddia
     ayrımı, formül/edim ayrımı, işaretleme).
⛔ Dışarıda kalanlar: ölçüm hattı hataları (K123), beyan↔tasarım
karışıklıkları (T193), ve kapının HAKLI olduğu ama sonucu tartışmalı
olan vakalar (T177).

⛔⛔ **SERİ BENİM DERLEMEM (K30) ve seçim yanlılığına açık:** yalnız
YAKALANMIŞ vakalar burada. Yakalanmamışların sayısı bilinmiyor ⇒ seri bir
**alt sınırdır** ve sıklık iddiası için kullanılamaz. Kullanılabileceği
şey: vakaların **mekanizmaya göre dağılımı** ve **nasıl bulundukları**.

Çıktı: reports/analiz/2026-09-22-t22-vaka-serisi.md
"""
from __future__ import annotations

import collections
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-t22-vaka-serisi.md"

# ⛔⛔ BİR SATIR HER ZAMAN BİR VAKA DEĞİL. Defterde adlandırılıp
#   NUMARALANMIŞ aileler var; onları tek satır saymak seriyi eksiltir.
#   ⭐ Bu düzeltmenin kendisi serinin dersinin bir örneği: eksik sayımı
#     hiçbir kapı görmedi, ikinci seri derlenirken OKUYARAK çıktı.
AILE_UYE = {
    # düz `.lower()` / Türkçe büyütme ailesi — defterdeki numaralandırma:
    #   T73 1.–5. (§15 + K146'nın aynı oturumda tekrarı)
    #   T75 6.–7. (`context_ok`/`KLINIK_IDDIA`)   T76 8. (`normalize.py`)
    #   T80 9. (`filter.alinti_nrm`)              T83 10. (plan sınıflandırıcı)
    #   T86 11. (puanlama kuralı; ardından denetim: borçlu 71 → 0)
    "T73 / K146 → T86": 11,
}

# ⛔ ÜYE ≠ BULUŞ OLAYI. Ailenin 11 üyesi 6 ayrı kayıtta (T73/T75/T76/T80/
#   T83/T86) bulundu. «Nasıl bulundu» tablosu OLAY sayar, mekanizma
#   tablosu ÜYE sayar — ikisi farklı soruya cevap veriyor.
AILE_BULUS = {"T73 / K146 → T86": 6}

# (kayıt, kapı, ne oldu, mekanizma, nasıl bulundu, bedeli)
VAKA = [
 ("T22", "`KLINIK_IDDIA` §7b", "Kurumun KENDİ adındaki *«tedavi»* kapıyı "
  "ateşledi: 22 satırın 7'si takıldı, **5'i yalnız kurum adından** "
  "(*Alkol ve Madde Bağımlıları **Tedavi** Merkezi*)",
  "ad ≠ iddia", "okuma", "7 yanlış pozitif"),
 ("T27", "`icermez` yasaklı terim listesi", "Terimi **reddeden** cevap "
  "ihlal sayıldı: *«İlacın adını, dozunu… konuşamam»* kaydı `doz` yüzünden "
  "düştü", "alt dizge", "okuma", "2 öğe"),
 ("T73 / K146 → T86", "düz `.lower()` kullanan HER kapı",
  "⭐⭐ **Bu tek bir vaka değil, deftere ADLANDIRILMIŞ ve NUMARALANMIŞ bir "
  "aile: 11 üye.** T73'te §15 `scan_forbidden` düz `.lower()` kullanıyordu "
  "ve doğru Türkçe büyütmede 38 yasak ifadenin 26'sı görünmez geçiyordu "
  "(2'si **sert**). T73 bir borç bıraktı (*«3 satır daha var, hiçbiri "
  "sınanmadı»*) ve borç ödendikçe aile büyüdü — üstelik **öldüren vektör "
  "yön değiştirerek** (T75: tehlike `I` değil `İ`)",
  "büyük harf / ASCII", "ölçüm → borç takibi → denetim",
  "⛔ 26 kaçak (2 sert) + 8 ölü kök + 1 sessiz yanlış kova + 6/9 yanlış "
  "eşleşme + 31 yanlış sınıflandırma"),
 ("T109", "atıf kapısı `_kok()`", "Ekler tek zincir sayılmıştı; Türkçede "
  "hâl eki doğrudan köke gelir ⇒ `_kok(\"doktora\")` = *«doktora»* ve kapı "
  "kullanıcının **kendi doktorunu** atfedilmiş kaynak sandı",
  "biçimbilim", "ölçüm", "—"),
 ("T142", "alıntı kapısı karşı olgusal muafiyeti", "`(söyle|de|sor)(ma|me)` "
  "yazılmıştı; Türkçede `-ma/-me` hem **olumsuzluk** hem **adfiil** eki ⇒ "
  "*«anlatmak»*, *«demesi»* de eşleşti ve muafiyet **üç gerçek kusurun "
  "üstünü örttü**", "eşseslilik", "ölçüm", "3 gerçek kusur gizlendi"),
 ("T150", "`KLINIK_IDDIA`", "§7b'nin **yedi yanlış pozitifinin hepsi** "
  "klinik ADI klinik İDDİA sanmaktan geliyordu ⇒ ölçüt ikiye ayrıldı",
  "ad ≠ iddia", "ölçüm", "7 yanlış pozitif"),
 ("T153 / K189", "§15 taraması", "`ifade in metin`; *«merak etme»* "
  "*«merak etmeK»*in içinde eşleşiyor ⇒ `bos_guvence`'in **16 vuruşunun "
  "16'sı** bu kusurdan, korpusta gerçek boş güvence yok",
  "alt dizge", "okuma kuyruğu", "16/16 sahte"),
 ("T192", "dört kriz süzgeci", "*«ortadan çekilsem»* — edilgen intihar "
  "düşüncesi; **dört kapının dördü de kaçırdı**. Sözlükle kurulan bir "
  "süzgeç ailesinde aynı düşüncenin başka fiili her seferinde yeni bir "
  "kaçak", "formül ≠ edim", "okuma", "1 tohum plana girmişti"),
 ("T196", "`ozerklik`/`is_negative` desenleri", "Kapı red CÜMLESİNİ "
  "ödüllendirdi, ben de cümleyi ürettim: *«sana ben söyleyemem»* **%1,2 → "
  "%11,9** (on kat). Formülü zorunlu kılan kapı şablonu da zorunlu kılıyor",
  "formül ≠ edim", "şablon taraması", "10× şablonlaşma"),
 ("T215", "`DOZ_SAYISI`", "`\\d+\\s*(mg|ml)` arıyor; *«iki hap alıyorum»* "
  "bir dozdur ve geçerdi. ⭐ Kapı bilerek genişletilmedi: aynı ifade "
  "*«çantamda iki hap»*ta bulundurmayı yazıyor", "birim/adet",
  "okuma", "2 kayıt elle yazıldı"),
 ("T217", "tohum karşılığı (ilk hâli)", "Tam sözcük karşılaştırıyordu ve "
  "8 sözcüklük bir kaydı 40 sözcüklük tohuma karşı **yanlış reddetti** — "
  "eklemeli dilde gövde önekine çevrildi", "biçimbilim", "kapı reddi",
  "1 yanlış red"),
 ("T227", "`RED` sözlüğü", "`bunu ben (söyle|…)` kolu *«bunu ben "
  "**söylemedim**»*i red saydı (parti3 `#8`, `#54`). Ayrıca sözlük "
  "ateşlediği 70 kaydın **22'sinde fazla**, ateşlemediği 7 kontrolün "
  "**5,7'sinde az** saydı", "formül ≠ edim", "üç anotatörle okuma",
  "26 ayrışma"),
 ("T228", "`OZERKLIK` sözlüğü", "Desen fazla saymıyor (%96) ama az "
  "sayıyor: işaretsiz 323 kaydın **%16'sında** özerklik vardı. Ayrışmaların "
  "tamamı *kaçınmak ≠ devretmek* sınırında", "formül ≠ edim",
  "iki anotatör + hakem", "51 kayıt eksik sayılmış"),
 ("T234 taraması", "marka deseni", "`slim` **«teslim»** içinde eşleşti "
  "(*«teslim baskısı»*) ⇒ blok 3'e olmayan bir marka ihlali yazıldı",
  "alt dizge", "okuma", "1 sahte ihlal"),
 ("T226 sezicisi", "`talep` deseni", "`\\bsöyle\\b`; ASCII yazılmış emir "
  "kipi *«onu **soyle**»* eşleşmedi ⇒ gerçek bir istek görünmez oldu",
  "büyük harf / ASCII", "sıra kapısı + okuma", "1 kayıt"),
 ("T233 sezicisi", "bant ölçüsü", "`<CTX>` yer tutucusu **sözcük sayıldı** "
  "⇒ üç blokta da tam 26 sözcüklük sahte *«bant ihlalleri»* (hepsi 25'ti)",
  "işaretleme", "okuma", "12 sahte ihlal"),
 ("gizlilik taraması (2026-09-22)", "gizlilik vaadi deseni",
  "⭐ **Bugün üretildi.** `v6-parti8 / ad5658bc`'de gerçek bir gizlilik vaadi "
  "bulunduktan sonra korpus tarandı: desen `kimseye söylemem` kolunu "
  "taşıyordu ve **`kimseye söylememişsin`** içinde eşleşti — biri **1. tekil "
  "bir VAAT**, öteki kullanıcının sözünü **yansıtma**. 14 eşleşmenin **13'ü** "
  "yanlış pozitif",
  "biçimbilim", "okuma", "13 yanlış pozitif, 1 gerçek vaka"),
 ("thinking kapısı (2026-09-22)", "«soru sormuyorum» ilanı deseni",
  "⭐ **Bugün üretildi, T239'un kapısını yazarken.** Desen `soru sormuyorum` "
  "idi ve **«İzin isterken KAPALI BİR soru sormuyorum»** içinde eşleşti ⇒ "
  "**nitelikli** bir ilanı **mutlak** sandı. O kayıt açık uçlu bir soru "
  "soruyor, yani tutarlı; tek ihlal sanılan şey **yanlış pozitifti**",
  "nitelik ≠ mutlak", "okuma", "1 yanlış pozitif / 0 gerçek")
]


def main() -> int:
    uye = lambda v: AILE_UYE.get(v[0], 1)
    N_SATIR, N_UYE = len(VAKA), sum(uye(v) for v in VAKA)
    olay = lambda v: AILE_BULUS.get(v[0], 1)
    N_OLAY = sum(olay(v) for v in VAKA)
    mek, bul = collections.Counter(), collections.Counter()
    for v in VAKA:
        mek[v[3]] += uye(v)
        bul[v[4]] += olay(v)
    sat = ["# T22 vaka serisi — mekanik kapının Türkçe serbest metinde yanılması", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Seri satırı:** {N_SATIR} · **belgelenmiş vaka:** {N_UYE} · "
           f"**buluş olayı:** {N_OLAY}  ", "",
           "⛔ Üç sayı farklı: bir satır adlandırılmış bir AİLEYİ temsil "
           "edebiliyor (11 üye, 6 ayrı keşif, 1 satır). "
           "⭐ Önceki sürümde bu aile **2** sayılmıştı; düzeltme ikinci seri "
           "derlenirken OKUYARAK çıktı — serinin kendi dersinin bir örneği.", "",
           "⭐ **Alma ölçütü:** mekanik bir kural (dizge/düzenli ifade/sözlük) "
           "Türkçe serbest metne uygulandı, hükmü yanlış çıktı, ve yanlışlık "
           "**anlamın değil yüzey biçiminin** bir özelliğine bağlanabildi.", "",
           "## Seri", "",
           "| # | kayıt | kapı | ne oldu | mekanizma | nasıl bulundu | bedeli | üye |",
           "|---:|---|---|---|---|---|---|---:|"]
    for i, v in enumerate(VAKA, 1):
        k, kapi, ne, m, b, bd = v
        n = AILE_UYE.get(k)
        sat.append(f"| {i} | {k} | {kapi} | {ne} | **{m}** | {b} | {bd} | "
                   + (f"**{n}**" if n else "1") + " |")

    sat += ["", "## Mekanizmaya göre dağılım", "",
        "⛔ Satır değil **üye** sayılıyor: `düz .lower()` ailesi tek satırda "
        "duruyor ama 11 belgelenmiş üyesi var.", "",
        "| mekanizma | vaka |", "|---|---:|"]
    sat += [f"| {k} | {v} |" for k, v in mek.most_common()]
    sat += ["", f"⭐⭐ **{len(mek)} mekanizma ve hiçbiri tesadüfi değil — hepsi "
            "Türkçenin ya da ölçünün yapısal bir özelliğinden geliyor:** "
            "eklemeli dilde alt dizge sınırı yok sayılıyor · `-ma/-me` iki ek "
            "birden · `i/I` çifti düz `.lower()`'da kayboluyor · bir kavramın "
            "ADI meşru bağlamda en sık o kavramı koruyan metinde geçiyor · "
            "sözlük bir edimi değil onun bir FORMÜLÜNÜ tanıyor · ve ölçü, "
            "metne dokunurken işaretlemeyi içerikten ayıramıyor.", "",
            "## ⭐⭐⭐ Asıl sayı: bunları ne buldu", "",
            "| bulan | buluş olayı |", "|---|---:|"]
    sat += [f"| {k} | {v} |" for k, v in bul.most_common()]
    # ⭐ Asıl karşılaştırma ikili: son adımda bir İNSAN HÜKMÜ var mıydı?
    #   ⛔ «okuma kuyruğu», «sıra kapısı + okuma» ve anotasyon turları da
    #     insan hükmüne SAYILIYOR: üçünde de kapı yalnız BAKILACAK YERİ
    #     gösterdi, hükmü okuma verdi.
    insan = sum(v for k, v in bul.items()
                if any(x in k for x in ("okuma", "hakem", "anotatör", "kapı reddi")))
    sat += ["", "**İkiye indirgenince:**", "", "| son adım | buluş olayı |", "|---|---:|",
            f"| ⭐ **okuma / insan hükmü** | **{insan}** |",
            f"| mekanik ölçüm ya da tarama | {N_OLAY - insan} |", "",
            f"⭐⭐⭐ **{N_OLAY} buluş olayının {insan}'sinde son hükmü bir OKUMA "
            "verdi.** Kalan " + str(N_OLAY - insan) + "'ü ölçüm buldu — ama "
            "hiçbirini *«bu kapıyı denetleyen ikinci bir kapı»* bulmadı, çünkü "
            "öyle bir şey yok ve olsaydı o da aynı sınıftan bir kusur "
            "taşırdı.", "",
            "➡️⭐⭐⭐ *Mekanik bir kapının Türkçe serbest metindeki kusuru, "
            "başka bir mekanik kapıyla değil ancak OKUMAYLA bulunuyor. "
            "Bu, kapıları gereksiz kılmaz — kapılar ucuz ve sürekli çalışır — "
            "ama denetim zincirinin sonunda mekanik olmayan bir adım "
            "bırakmayı zorunlu kılar.*", "",
            "⭐ T22'nin özgün iddiası bu seride **1. ve 6. vakada** iki kez "
            "ayrı ayrı görülüyor (*«ad ≠ iddia»*): yasak listesi kavramın "
            "adını ararken, o ad meşru bağlamda en sık korunmak istenen "
            "metinde geçiyor.", "",
            "## ⛔ Bu serinin söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Seri bir ALT SINIRDIR** | yalnız YAKALANMIŞ vakalar "
            "burada; yakalanmamışların sayısı bilinmiyor ⇒ sıklık iddiası "
            "için kullanılamaz |",
            "| ⛔⛔ **Derleyen benim (K30)** | hangi vakanın seriye gireceğine "
            "ben karar verdim; alma ölçütü yazılı ama uygulaması benim |",
            "| ⛔⛔ **Aile MEKANİK tarafa yazıldı** | `düz .lower()` ailesinin "
            "6 buluş olayı topluca *«ölçüm → borç takibi → denetim»* sayıldı; "
            "en az biri (`T83`) makul görünen bir çıktının OKUNMASIYLA çıktı ⇒ "
            "atıf, kendi iddiamın ALEYHİNE yuvarlandı |",
            "| ⛔ **«Nasıl bulundu» sütunu geriye dönük** | kaydın yazıldığı "
            "andaki anlatıya dayanıyor, ayrı bir ölçüm değil |",
            "| ⚠️ **Kapıların FAYDASI ölçülmedi** | bu seri yalnız kusurları "
            "topluyor; aynı kapıların yakaladığı gerçek ihlaller sayılmadı ⇒ "
            "*«kapılar işe yaramıyor»* SONUCU ÇIKARILAMAZ |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[sat.index("## Mekanizmaya göre dağılım"):]))
    print(f"\n→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
