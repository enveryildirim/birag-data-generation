#!/usr/bin/env python3
"""Üç kapının MUAFİYETLERİNİ T140'ın gözüyle yeniden okur.

⛔⛔ **Neden var.** T140: yapısal atıf kapısında bir muafiyet (`len(turlar) < 2`)
*«aynı mesajda»* için doğru, *«aynı cümlede»* için yanlıştı ve kapının kendi
ayrımını yok ediyordu. Kusuru **kapı değil judge** buldu. Düzeltilince elle okuma
yükü 10 → 26 çıktı: muafiyet denetimin üçte ikisini sessizce siliyordu.
T140 kapanırken açık kalan kalem şuydu — *«öteki üç kapının muafiyetleri aynı
gözle yeniden okunmadı»*. Bu betik o kalemi kapatır.

⭐ **Yöntem iki adımlı ve ikincisi olmadan birincisi işe yaramaz:**
  1. **Denklik sınaması** — kapının `HEAD`'deki sürümü ile defterli sürümü AYNI
     girdide koşulur ve `bulgu` listeleri karşılaştırılır. Bir denetim aracı
     denetlediği şeyi değiştiriyorsa ölçtüğü sayı kendi eseridir.
     ⛔⛔ **İlk yazımda bu sınama yanlış kurulmuştu:** «önce» tarafı olarak diskte
     duran eski rapor JSON'ları alınmıştı ve 16 koşunun 5'i FARKLI çıktı. Sebep
     defter değildi — o raporlar kapıların **bugün birkaç kez değişmiş** eski
     sürümlerinden kalmaydı (mekân kapısı `_EK` ve asimetrik kaynak deseni,
     zaman kapısı bağlaçlı rol muafiyeti). ➡️ *Bir «önce/sonra» sınamasında
     «önce» tarafı, değiştirilen şeyin dışındaki her şeyin AYNI olduğu bir
     noktadan alınmalı; diskteki bir çıktı bunu garanti etmez, sürüm denetimi eder.*
  2. **Muafiyet dökümü** — her muafiyetin BAĞIŞLADIĞI ögeler adıyla listelenir.

⛔⛔ **Korpus seçimi kritik ve daha önce bir kez yanlış yapıldı** (alıntı kapısının
şerhi): *«Bir muafiyetin ayırt ediciliği, kusurların KALDIRILDIĞI korpusta
ölçülemez — orada her muafiyet kusursuz görünür.»* ⇒ Denetim **ham** partiler
üzerinde koşar (`v5-parti8.jsonl`), temizlenmişler (`.arinmis`, `.v6`) üzerinde
değil. Mekân kapısının KENDİ varsayılanı `*.arinmis.jsonl` olduğu için tam bu
tuzağa düşüyordu; burada açıkça ham dosyalar veriliyor.

⚠️ Bu betik bir KARAR vermez: hangi muafiyetin fazla geniş olduğunu **elle okuma**
söyler. Betiğin işi, elle okunacak listeyi görünür kılmaktır — T140'ta o liste
hiç var olmadığı için kusur judge'a kalmıştı.

Girdi : data/candidates/v4-parti*.jsonl, v5-parti*.jsonl (ham sürümler)
Çıktı : reports/analiz/2026-09-17-muafiyet-denetimi.md
Kullanım: uv run python scripts/analiz/2026-09-17-muafiyet-denetimi.py
"""
from __future__ import annotations

import importlib.util
import io
import subprocess
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
sys.path.insert(0, str(KOK / "scripts/analiz"))
TARIH = Path(__file__).name[:10]          # ⛔ rapor tarihi betiğin ADINDAN (K126)
RAPOR = KOK / f"reports/analiz/{TARIH}-muafiyet-denetimi.md"
GIT_ONCE = "HEAD"    # ⭐ denkliğin «önce» tarafı: kapının sürüm denetimindeki hâli

import _muafiyet as MUAF  # noqa: E402


def _yukle(ad: str, dosya: str | Path):
    yol = dosya if isinstance(dosya, Path) else KOK / "scripts/analiz" / dosya
    s = importlib.util.spec_from_file_location(ad, yol)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _head_surumu(dosya: str) -> Path | None:
    """Kapının `HEAD`'deki hâlini `scripts/analiz/` içine geçici olarak açar.

    ⚠️ Dizin önemli: kapılar `KOK`'ü `__file__`'ın ATASINDAN buluyor; başka bir
    yere konursa kök yanlış çıkar ve kapı kendi girdisini bulamaz.

    ⛔⛔ **AD DA ÖNEMLİ VE İLK YAZIMDA YANLIŞTI.** Geçici dosya `.denklik-<ad>.py`
    diye açılıyordu; K126 gereği **rapor tarihini betiğin ADINDAN** türeten kapılar
    (`TARIH = Path(__file__).name[:10]`) bu addan *«.denklik-2»* okuyup raporlarını
    **başka bir dosyaya** yazdı. ⇒ Denklik sınaması «önce» tarafını hiç görmedi ve
    dosyayı **kendisiyle** karşılaştırıp ✅ verdi. Kusuru, denetimin arkasında kalan
    iki başıboş `.denklik-2-*.md` dosyası ele verdi.
    ➡️⭐⭐ *Bir sınamanın «aynı» demesi, iki şeyi karşılaştırdığı anlamına gelmez.
    Ve bir betiğin ADI davranışını belirliyorsa (K126), o adı değiştiren her araç
    o davranışı da değiştirir.*
    ⇒ Geçici ad TARİH ÖNEKİNİ korur: `<özgün-ad>.HEAD-denklik.py`.
    """
    g = subprocess.run(["git", "show", f"{GIT_ONCE}:scripts/analiz/{dosya}"],
                       cwd=KOK, capture_output=True, text=True)
    if g.returncode != 0:
        return None
    t = KOK / "scripts/analiz" / f"{Path(dosya).stem}.HEAD-denklik.py"
    t.write_text(g.stdout, encoding="utf-8")
    return t


KAPILAR = {
    "alıntı birebirliği": ("alinti", "2026-09-17-alinti-birebirlik-kapisi.py",
                           "alinti-birebirlik"),
    "zaman + kaynak atfı": ("zaman", "2026-09-17-zaman-kaynak-kapisi.py",
                            "zaman-kaynak"),
}
# ⛔ HAM partiler — temizlenmiş sürümler DEĞİL (bkz. korpus seçimi şerhi).
HAM = ["v4-parti1.jsonl", "v4-parti2.v2.jsonl", "v5-parti3.jsonl", "v5-parti4.jsonl",
       "v5-parti5.jsonl", "v5-parti6.jsonl", "v5-parti7.jsonl", "v5-parti8.jsonl"]

# Her muafiyetin NE İÇİN yazıldığı — T140'ın sorusu tam olarak budur:
# «bu muafiyet yazıldığı alt vakanın DIŞINDA da ateşliyor mu?»
GEREKCE = {
    "sure_birim_eslesme": "kalıp farklı ama SÜRE+BİRİM kaynakta var (*«üç ay önce»* ↔ *«üç ay oldu»*)",
    "anaforik_demir": "*«dün/geçen hafta»* öncülü kullanıcının turunda AYNI BİRİMDEN var",
    "belirsiz_artikel": "*«BİR hekimin»* — belirsiz tamlama, kullanıcının kendi hekimi değil",
    "rol_adlandirma_bitisik": "*«hekimin İŞİ»* — atıf değil, §8b'nin istediği rol adlandırma",
    "rol_adlandirma_baglacli": "*«hekimin ya da … uzmanın işi»* — rol sözcüğü bağlacın öbür ucunda",
    "karsi_olgusal": "*«… demiyorum»* — alıntı bir İDDİA değil, reddedilen bir kalıp",
    "ne_yapisi": "*«ne … ne …»* yapısı — alıntı olumsuzlanıyor",
    "yonlendirme_cumlesi": "*«okulun rehberlik birimi»* — mekân ADI değil, KAYNAK TÜRÜ",
    "mecaz": "*«aynı masaya koymak»* — mekân değil, mecaz",
    "kaynak_gevsek_eslesme": "⚠️ kaynak deseni GEVŞEK (`\\w*`), cevap deseni SERT — asimetri",
}


def _bulgu_imzasi(o: dict) -> list:
    """Karşılaştırılabilir bulgu imzası — anahtar sırasından bağımsız."""
    return sorted(json.dumps(b, ensure_ascii=False, sort_keys=True) for b in o["bulgu"])


# ⭐ Hangi kapının DAVRANIŞININ değişmesi BEKLENİYOR? Defter hiçbirinde
# değiştirmemeli; denetimin bulduğu kusur yüzünden yalnız alıntı kapısı değişti.
# ⛔ Beklenti önceden yazılır: sonradan yazılan beklenti, sonucu açıklamaz.
# ⚠️ Düzeltme ARTIK `HEAD`'DE: alıntı kapısının kusuru işlendiği için bu tablo
# bugün üç kapıda da ✅ vermeli. Düzeltmenin ETKİSİ (21 → 22 bulgu, kayıp yok)
# işlenmeden önce ölçüldü ve T142/K177'de kayıtlı; burada yeniden üretilemez,
# çünkü karşılaştırmanın «önce» tarafı artık düzeltilmiş hâl.
BEKLENTI = {"alıntı birebirliği": "değişmemeli (düzeltme HEAD'de)",
            "zaman + kaynak atfı": "değişmemeli (yalnız defter)",
            "mekân atfı": "değişmemeli (yalnız defter)"}


def main() -> int:
    sat = [f"# Muafiyet denetimi — üç kapının BAĞIŞLADIKLARI", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}", "",
           "⛔⛔ **Açık kalemi kapatır (T140).** Yapısal atıf kapısında bir muafiyet,",
           "yazıldığı alt vakanın dışında da ateşleyip kapının kendi ayrımını yok etmişti",
           "ve bunu kapı değil **judge** bulmuştu. Öteki kapılarda aynı şey var mı?", "",
           "⭐ **Ön koşul:** kapılar artık bağışladıkları her ögeyi `_muafiyet.DEFTER`'e",
           "yazıyor. *Bir muafiyet sayılmadıkça denetlenemez.*", "",
           "⛔ **Korpus ham seçildi.** Muafiyetin ayırt ediciliği, kusurların kaldırıldığı",
           "korpusta ölçülemez; orada her muafiyet kusursuz görünür.", ""]

    denklik, tum, gecici = [], {}, []
    for baslik, (_ad, dosya, onek) in KAPILAR.items():
        mod = _yukle(_ad, dosya)
        eski_yol = _head_surumu(dosya)
        eski_mod = _yukle(_ad + "_head", eski_yol) if eski_yol else None
        if eski_yol:
            gecici.append(eski_yol)
        for h in HAM:
            girdi = f"data/candidates/{h}"
            if not (KOK / girdi).exists():
                continue
            rapor = KOK / f"reports/analiz/{TARIH}-{onek}-{Path(h).stem}.json"
            eski = None
            if eski_mod:
                with redirect_stdout(io.StringIO()):
                    eski_mod.main(girdi)
                eski = json.loads(rapor.read_text(encoding="utf-8"))
            MUAF.sifirla()
            with redirect_stdout(io.StringIO()):
                mod.main(girdi)
            yeni = json.loads(rapor.read_text(encoding="utf-8"))
            for m in MUAF.DEFTER:
                m["kapi"], m["korpus"] = baslik, Path(h).stem
            tum.setdefault(baslik, []).extend(MUAF.DEFTER)
            if eski is not None:
                ei, yi = _bulgu_imzasi(eski), _bulgu_imzasi(yeni)
                denklik.append((baslik, Path(h).stem, len(eski["bulgu"]), len(yeni["bulgu"]),
                                ei == yi, [json.loads(x) for x in yi if x not in ei],
                                [json.loads(x) for x in ei if x not in yi]))

    # mekân kapısı listeyle çalışır
    mek = _yukle("mekan", "2026-09-17-mekan-atfi-kapisi.py")
    MUAF.sifirla()
    with redirect_stdout(io.StringIO()):
        mek.main([f"data/candidates/{h}" for h in HAM if (KOK / f"data/candidates/{h}").exists()])
    for m in MUAF.DEFTER:
        m["kapi"], m["korpus"] = "mekân atfı", "ham"
    tum["mekân atfı"] = list(MUAF.DEFTER)
    ham_mekan = json.loads((KOK / f"reports/analiz/{TARIH}-mekan-atfi-kapisi.json"
                            ).read_text(encoding="utf-8"))
    # ⭐ denklik için mekân kapısı KENDİ varsayılanıyla (arinmis) da koşulur
    mek_eski_yol = _head_surumu("2026-09-17-mekan-atfi-kapisi.py")
    if mek_eski_yol:
        gecici.append(mek_eski_yol)
        mek_eski = _yukle("mekan_head", mek_eski_yol)
        with redirect_stdout(io.StringIO()):
            mek_eski.main([])
        eski_m = json.loads((KOK / f"reports/analiz/{TARIH}-mekan-atfi-kapisi.json"
                             ).read_text(encoding="utf-8"))
        MUAF.sifirla()
        with redirect_stdout(io.StringIO()):
            mek.main([])
        yeni_m = json.loads((KOK / f"reports/analiz/{TARIH}-mekan-atfi-kapisi.json"
                             ).read_text(encoding="utf-8"))
        em, ym = _bulgu_imzasi(eski_m), _bulgu_imzasi(yeni_m)
        denklik.append(("mekân atfı", "arinmis (varsayılan)", len(eski_m["bulgu"]),
                        len(yeni_m["bulgu"]), em == ym,
                        [json.loads(x) for x in ym if x not in em],
                        [json.loads(x) for x in em if x not in ym]))
    for t in gecici:      # ⛔ Kural 8: geçici sürümler bırakılmaz
        t.unlink(missing_ok=True)

    sat += ["## 1. ⭐ `HEAD` ↔ şimdi — hangi kapının kararı değişti?", "",
            "⭐ **Defter eklendiğinde bu tablo 17 koşunun 17'sinde de ✅ veriyordu** —",
            "yani bağışlananları saymak hiçbir kapının kararını değiştirmedi. Aşağıdaki",
            "farklar defterin değil, defterin GÖRÜNÜR KILDIĞI kusurun düzeltilmesinindir.", "",
            "| kapı | korpus | `HEAD` | şimdi | aynı? | beklenti |",
            "|---|---|---:|---:|---|---|"]
    for k, c, a, b, ayni, _y, _e in denklik:
        sat.append(f"| {k} | `{c}` | {a} | {b} | {'✅' if ayni else '⛔ **FARKLI**'} "
                   f"| {BEKLENTI.get(k, '—')} |")
    sapan = [x for x in denklik if not x[4] and "değişmemeli" in BEKLENTI.get(x[0], "")]
    hepsi = not sapan
    degisen = [x[0] for x in denklik if not x[4]]
    sat += ["", ("⭐ **Üç kapının üçünde de karar birebir aynı.**" if not degisen else
                 f"⛔⛔ **DEĞİŞEN KAPI: {', '.join(sorted(set(degisen)))}** — beklenti "
                 "tabloda yazılı; beklenmeyen bir değişim varsa aşağıdaki sayılar okunamaz."),
            "", "⚠️ **Alıntı kapısının düzeltmesi artık `HEAD`'de** ⇒ etkisi bu tabloda "
            "GÖRÜNMEZ. Düzeltme işlenmeden önce ölçüldü: `v0.0.9/train` üzerinde 21 → 22 "
            "bulgu, **kayıp bulgu yok** (T142/K177).", ""]
    yeni_bulgular = [(k, c, y) for k, c, _a, _b, _ay, y, _e in denklik if y]
    kaybolan = [(k, c, e) for k, c, _a, _b, _ay, _y, e in denklik if e]
    if yeni_bulgular or kaybolan:
        sat += ["### ⭐ Düzeltmenin açtığı bulgular — elle okunacak", ""]
        for k, c, ys in yeni_bulgular:
            for y in ys:
                sat.append(f"- ➕ `{c}` #{y.get('parti_sira')} — «{str(y.get('alinti', y))[:90]}»")
        for k, c, es in kaybolan:
            for e in es:
                sat.append(f"- ➖ `{c}` #{e.get('parti_sira')} — «{str(e.get('alinti', e))[:90]}» "
                           f"⚠️ ARTIK BULUNMUYOR: düzeltme bir yakalamayı da kaybettiyse sorun budur")
        sat.append("")

    sat += ["## 2. ⭐ Muafiyet dökümü — hangi muafiyet ne kadar bağışlıyor?", ""]
    for baslik, kayitlar in tum.items():
        say: dict[str, int] = {}
        for m in kayitlar:
            say[m["muafiyet"]] = say.get(m["muafiyet"], 0) + 1
        sat += [f"### {baslik}", "", "| muafiyet | ateşleme | ne için yazıldı |",
                "|---|---:|---|"]
        for ad, n in sorted(say.items(), key=lambda x: -x[1]):
            sat.append(f"| `{ad}` | **{n}** | {GEREKCE.get(ad, '⛔ gerekçe yazılmamış')} |")
        if not say:
            sat.append("| — | 0 | ⚠️ hiç ateşlemedi |")
        sat.append("")

    sat += ["## 3. ⭐ Elle okuma kararları — muafiyet gerçekten kusur mu sakladı?", "",
            "⛔ Üç bulgu da **ham partilerde** elle okundu; hiçbiri yanlış pozitif değil.", "",
            "| bulgu | kullanıcı ne yazmış | karar |", "|---|---|---|",
            "| `v5-parti3 #56` «her şeye karışmak» | *«her şeye karışıyorlar»* | ⛔ kusur — çekim değişmiş, tırnak birebirlik iddia ediyor |",
            "| `v5-parti4 #5` «belki abartıyorum» | *«Belki ben abartıyorum»* | ⛔ kusur — *«ben»* düşmüş; bilinen «kelime düşürme» kipi |",
            "| `v5-parti7 #33` «peki» | *«doktor yine yatış dedi. ben yatamam»* | ⛔ kusur — *«peki»* hiç geçmiyor, kullanıcının yazdığı uyduruluyor |", "",
            "### ⛔⛔ Düzeltmenin kendi yanlış pozitifleri — ölçülüp kapatıldı", "",
            "Aynı düzeltme `datasets/v0.0.9/train.jsonl` üzerinde koşulunca **üç** yeni bulgu",
            "verdi ve elle okununca **ikisi yanlış pozitif** çıktı. İkisi de kapatıldı:", "",
            "| yanlış pozitif | neden meşru | eklenen muafiyet |", "|---|---|---|",
            "| *«Senin yerine \"devam et\" ya da \"kes\" demek bana düşmez»* | mastar alıntının yüklemi ama araya **bağlaçlı ikinci alıntı** giriyor | `anma_oneri` genişletildi |",
            "| *«\"Gerçeği söylemek mümkün değil\" demişsin, \"istemiyorum\" DEĞİL»* | olumsuzluğu söz fiili değil **sıfat** taşıyor | `karsit_degil` (yeni) |", "",
            "➡️⭐ *Eski kapı ikinciyi DOĞRU bağışlıyordu ama YANLIŞ sebeple — pencerede",
            "*«söylemek»* geçtiği için. Gerekçe düzeltilince doğru karar da düştü. Bu yüzden",
            "her gerekçe ayrı yazılır: doğru sonuç, doğru kural demek değildir.*", "",
            "### ⭐ Ölçülüp ÇÜRÜTÜLEN bir hipotez", "",
            "Kapının «kaynak»ı yalnız **kullanıcı** turlarını içeriyor ⇒ asistanın kendi",
            "önceki turunu alıntılaması yapısal olarak hep uydurma sayılır. Asistan turları",
            "kaynağa eklenip ölçüldü: `v0.0.9/train` **22 → 22 öge**, düşen öge **yok**.",
            "➡️ *Boşluk gerçek ama bu korpusta ÖRNEĞİ yok; kapı değiştirilmedi.*", "",
            "### ⭐ Öteki iki kapı — muafiyet başına karar", "",
            "⭐ **`[ZATEN YERDE]` ayrımı iki şüpheyi çürüttü.** Bir muafiyet, öge zaten",
            "kaynakta geçerken ateşlerse hiçbir kusur saklamaz; ayrılmadan önce bu ikisi",
            "«fazla geniş muafiyet» gibi görünüyordu.", "",
            "| kapı · muafiyet | net bağış | karar |", "|---|---:|---|",
            "| zaman · `belirsiz_artikel` | 7 | ✅ yedisi de *«bir hekimin»* — yazıldığı vaka |",
            "| zaman · `rol_adlandirma_bitisik` | 8 | ✅ sekizi de *«hekimin işi»* |",
            "| zaman · `rol_adlandirma_baglacli` | 2 | ✅ ikisi de *«hekimin ya da … uzmanın işi»* |",
            "| zaman · `sure_birim_eslesme` | 8 | ✅ sekizinde de süre+birim kullanıcıda var |",
            "| zaman · `anaforik_demir` | 13 | ✅ altısı elle okundu, altısı da demirli |",
            "| mekân · `yonlendirme_cumlesi` | 2 | ✅ *«ilk durak»*, *«meslek odası»* — kaynak türü |",
            "| mekân · `mecaz` | 2 | ✅ *«bu odada kimse»*, *«aynı masaya koyan»* |",
            "| mekân · `kaynak_gevsek_eslesme` | 7 | ✅ yedisi de kullanıcının kendi sözcüğünün çekimi (*«terasta»* → *«teras»*) |", "",
            "⛔ **Ama biri gizli kusurlu: `rol_adlandirma_bitisik` yanlış şeye bakıyor.**",
            "Muafiyet tamlayanın ARDILINA bakıyor (*«işi»*, *«alanı»*), ROL adına değil ⇒",
            "*«sevgilinin işi»*, *«doktorunun alanı»* da muaf oluyor; oysa muafiyet §8b'nin",
            "MESLEK rolleri için yazılmıştı. ⭐ Bu korpusta ikisi de `[ZATEN YERDE]` çıktı,",
            "yani **bugün hiçbir kusur saklamıyor** — ama sızıntı gerçek ve kayıtlıdır.",
            "➡️ *Bir muafiyetin bugün bir şey saklamaması, dar olduğu anlamına gelmez;",
            "ölçüm muafiyetin GENİŞLİĞİNİ değil, o genişliğin BU korpustaki bedelini verir.*", "",
            "## 4. ⛔ Elle okunacaklar — muafiyetin bağışladığı ögeler", "",
            "⚠️ *Bu liste bir suçlama değil.* Her satır, kapının «kusur değil» dediği bir",
            "ögedir; T140'ın sorusu **her birinin yazıldığı alt vakada mı olduğu**dur.", ""]
    for baslik, kayitlar in tum.items():
        grup: dict[str, list] = {}
        for m in kayitlar:
            grup.setdefault(m["muafiyet"], []).append(m)
        for ad, ms in sorted(grup.items()):
            sat += [f"#### {baslik} · `{ad}` ({len(ms)})", ""]
            for m in ms[:40]:
                yer = f"{m['korpus']} #{m['parti_sira']}"
                sat.append(f"- `{yer}` — «{m['oge']}» ⟵ *{m['baglam'][:150]}*")
            if len(ms) > 40:
                sat.append(f"- ⚠️ … ve {len(ms)-40} tane daha (JSON'da tamamı)")
            sat.append("")

    (KOK / f"reports/analiz/{TARIH}-muafiyet-denetimi.json").write_text(
        json.dumps({"tarih": TARIH, "denklik": denklik, "muafiyet": tum,
                    "ham_mekan_bulgu": ham_mekan["bulgu"]},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[:1] + sat[12:]))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0 if hepsi else 1


if __name__ == "__main__":
    raise SystemExit(main())
