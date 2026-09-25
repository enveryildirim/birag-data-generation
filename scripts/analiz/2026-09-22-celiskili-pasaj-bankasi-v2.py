#!/usr/bin/env python3
"""§7a″ pasaj bankasının İKİNCİ partisi — 13 yeni çift (no 13-25).

⛔⛔ **Neden gerekli.** `v0.0.21`'de `celiskili` payı bağlamlı 234 kaydın
**%5,1**'i; §7a″ kotası **~%10**. Kotayı tutturmak **13 kayıt** daha
ister (25/247 = %10,1) ve birinci bankanın 12 çiftinin **hepsi
kullanıldı**.

⭐ **Denetim KOPYALANMIYOR, import ediliyor (K103):** birinci banka
betiğindeki `denetle()` çağrılır. O betik bu iş için refactor edildi ve
çıktısının **bayt bayt aynı** kaldığı doğrulandı.

⭐ **Ek denetim — ALAN ÇAKIŞMASI.** Birinci bankanın alanları
(`gün`, `randevu`, `süre`, `belge`, `yaş`, `ücret`, `eşlik`, `sıklık`,
`kanal`, `bekleme`, `kayıt`, `grup`) yeniden kullanılmaz: aynı çelişki
alanını iki kez öğretmek çeşitlilik değil **tekrar** olur.

⛔ Sınırlar birinci bankayla aynı ve aynı kodla denetlenir: §7b (kaynak
adı kategori, küçük harf, özel ad yok) · Kural 3/K18/K110 (klinik iddia,
doz, ilaç, teşhis, telefon, kurum özel adı yasak) · çelişki **temiz**
(aynı alanda iki farklı değer, biri ötekini içermez).

⛔ Çelişkinin tarafı seçilmez: `dogru_taraf` yine `null`.

Çıktı: data/celiskili-pasaj-bankasi.v2.json
"""
from __future__ import annotations

import json
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / "data/celiskili-pasaj-bankasi.v2.json"
BIRINCI = KOK / "data/celiskili-pasaj-bankasi.json"

# ⭐ K103: denetim kopyalanmıyor, birinci banka betiğinden geliyor.
_yol = KOK / "scripts/analiz/2026-09-22-celiskili-pasaj-bankasi.py"
_spec = _iu.spec_from_file_location("_banka1", _yol)
_b1 = _iu.module_from_spec(_spec)
_argv = sys.argv[:]
sys.argv = [str(_yol)]
_spec.loader.exec_module(_b1)
sys.argv = _argv
denetle = _b1.denetle

ILK_NO = 13

# (konu, alan, kaynak_a, metin_a, deger_a, kaynak_b, metin_b, deger_b)
CIFTLER = [
 ("görüşme yeri", "yer", "birim tanıtım metni",
  "Görüşmeler birimin kendi binasında yapılmaktadır.", "kendi binasında",
  "hizmet akış metni",
  "Görüşmeler bağlı bulunulan semt biriminde yürütülür.", "semt biriminde"),

 ("program uzunluğu", "program", "program bilgi metni",
  "Program toplam sekiz hafta sürmektedir.", "sekiz hafta",
  "izlem düzeni metni", "Program on iki hafta olarak uygulanır.", "on iki hafta"),

 ("devamsızlık sınırı", "devamsizlik", "katılım koşulları metni",
  "İki görüşmeye katılmayanların kaydı kapatılır.", "iki görüşme",
  "işleyiş özeti metni",
  "Devamsızlık sınırı dört görüşme olarak uygulanmaktadır.", "dört görüşme"),

 ("kayıtların saklanması", "saklama", "bilgi işlem bilgi metni",
  "Görüşme kayıtları bir yıl süreyle saklanır.", "bir yıl",
  "belge düzeni metni",
  "Görüşme kayıtları beş yıl boyunca saklanmaktadır.", "beş yıl"),

 ("grup mevcudu", "mevcut", "grup çalışması bilgi metni",
  "Gruplar en çok sekiz kişiden oluşmaktadır.", "en çok sekiz kişi",
  "etkinlik düzeni metni",
  "Grupların mevcudu on beş kişidir.", "on beş kişi"),

 ("kapanış saati", "kapanis", "birim çalışma düzeni metni",
  "Birim saat on yediye kadar açıktır.", "on yediye kadar",
  "duyuru panosu metni",
  "Birim akşam saat yirmiye kadar hizmet vermektedir.", "yirmiye kadar"),

 ("görüşmenin yapılış biçimi", "gorusme_bicimi", "hizmet kapsamı metni",
  "Görüşmeler yalnızca yüz yüze yapılmaktadır.", "yalnızca yüz yüze",
  "erişim bilgi metni",
  "Görüşmeler telefon üzerinden de yürütülebilmektedir.", "telefon üzerinden de"),

 ("sevk koşulu", "sevk", "başvuru yönerge metni",
  "Başvuru için hekim sevki gerekmektedir.", "sevk gerekir",
  "başvuru bilgi notu",
  "Başvurular sevk olmaksızın doğrudan alınmaktadır.", "sevksiz doğrudan"),

 ("üst yaş sınırı", "ust_yas", "hizmet kapsamı özeti",
  "Hizmet için üst yaş sınırı bulunmamaktadır.", "üst sınır yok",
  "kapsam bilgi metni",
  "Hizmet altmış beş yaşına kadar verilmektedir.", "altmış beşe kadar"),

 ("ikamet koşulu", "ikamet", "başvuru koşulları özeti",
  "Hizmetten ilçede ikamet edenler yararlanabilmektedir.", "ilçede ikamet şartı",
  "sık sorulanlar notu",
  "Hizmet için ikamet şartı aranmamaktadır.", "şart aranmaz"),

 ("iptal bildirimi", "iptal", "randevu düzeni metni",
  "Görüşme iptalinin en az yirmi dört saat önce bildirilmesi gerekir.",
  "yirmi dört saat", "işleyiş bilgi notu",
  "İptal bildirimi için kırk sekiz saat önceden haber verilmelidir.",
  "kırk sekiz saat"),

 ("görüşme dili", "dil", "hizmet bilgi özeti",
  "Görüşmeler yalnızca Türkçe yürütülmektedir.", "yalnızca türkçe",
  "erişim düzeni metni",
  "Görüşmeler talep hâlinde başka dillerde de yapılabilmektedir.",
  "başka dillerde de"),

 ("sonuç bildirimi", "bildirim", "işleyiş özeti notu",
  "Görüşme sonucu yazılı olarak bildirilmektedir.", "yazılı olarak",
  "birim bilgi metni",
  "Sonuç bildirimi sözlü olarak yapılmaktadır.", "sözlü olarak"),
]


def main() -> int:
    if len(CIFTLER) != 13:
        raise SystemExit(f"⛔ 13 çift bekleniyordu, {len(CIFTLER)} var")

    # ⭐ EK DENETİM: birinci bankanın alanları tekrar edilmesin.
    b1 = json.loads(BIRINCI.read_text())["ciftler"]
    eski_alan = {c["celiski_alani"] for c in b1}
    eski_no = {c["no"] for c in b1}
    hata = [f"#{ILK_NO+i}: `{a}` alanı birinci bankada ZATEN var"
            for i, (_, a, *_) in enumerate(CIFTLER) if a in eski_alan]
    yeni_no = set(range(ILK_NO, ILK_NO + len(CIFTLER)))
    if yeni_no & eski_no:
        hata.append(f"⛔ numara çakışması: {sorted(yeni_no & eski_no)}")
    # ⭐ Ana denetim — K103: kopyalanmadı, import edildi.
    hata += denetle(CIFTLER, ilk_no=ILK_NO)
    if hata:
        for h in hata[:12]:
            print("⛔", h)
        raise SystemExit(f"⛔ {len(hata)} denetim hatası — dosya YAZILMADI")

    banka = [{
        "no": k, "konu": konu, "celiski_alani": alan,
        "context": [{"kaynak": ka, "metin": ma, "sentetik": True},
                    {"kaynak": kb, "metin": mb, "sentetik": True}],
        "degerler": [da, db],
        "dogru_taraf": None,
    } for k, (konu, alan, ka, ma, da, kb, mb, db)
        in enumerate(CIFTLER, ILK_NO)]

    CIKTI.write_text(json.dumps({
        "surum": "celiskili-pasaj-bankasi.v2",
        "tarih": Path(__file__).name[:10],
        "sinif": "celiskili",
        "kural": "prompts/uretim-v5.md §7a″",
        "gerekce": ("v0.0.21'de celiskili payı %5,1; kota ~%10. 13 kayıt daha "
                    "gerekiyor ve birinci bankanın 12 çifti tükendi."),
        "not": ("Çelişkinin tarafı SEÇİLMEZ: hiçbir pasaj doğru işaretlenmez. "
                "Doğru davranış çelişkiyi adlandırmak, birini seçmemek, "
                "birleştirmemek."),
        "ciftler": banka}, ensure_ascii=False, indent=1), encoding="utf-8")
    assert CIKTI.exists()
    print(f"⭐ {len(banka)} yeni çift (no {ILK_NO}-{ILK_NO+len(banka)-1}) · "
          f"{len(CIFTLER)*2} pasaj, 0 hata")
    print(f"   yeni alanlar: {sorted(c['celiski_alani'] for c in banka)}")
    print(f"   birinci banka alanları (tekrar YOK): {sorted(eski_alan)}")
    print(f"→ {CIKTI.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
