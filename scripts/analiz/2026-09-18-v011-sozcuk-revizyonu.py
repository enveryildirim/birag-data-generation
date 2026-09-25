#!/usr/bin/env python3
"""v0.0.11 — dört düzeltme: kullanıcının kendi sözcüğü geri konuluyor.

⛔ **Neden.** T166: sürüm sağlık raporu, modelin kullanıcının sözcüğünü
değiştirdiğini ölçtü — kullanıcı *«Hanım»* / *«Karım»* diyor, cevap *«Eşin»*
diyor. 63 kaydın 59'unda sözcük korunmuş, **4'ünde değiştirilmiş** ve yön tek
taraflı: günlük dildeki sözcük resmî olanla değiştiriliyor, tersi hiç yok.

➡️ *Korpusun kendi kaydı, kullanıcının kaydını bastırıyor.* Depo baştan beri
*«kullanıcının KENDİ sözcüğünü kullan»* diyor (T142'de *«hekimin»* ↔ *«doktor»*,
aynı gün *«her şeye karışmak»*) — bu dört kayıt o kuralın kendi ihlali.

⛔⛔ **BEŞİNCİ KALEM YOKTU VE BU DÜZELTİLDİ.** T165 `v5-parti4 #3`teki dayanaksız
*«İkisi de aynı hafta içinde»* iddiasını kusur saymıştı; ama o okuma **ham parti
dosyası** üzerindeydi. Yayımlanmış sette cümle çoktan *«İkisi de arka arkaya
oldu»* olmuş ⇒ kalem yok. ➡️ *Bir kusuru ham korpusta okuyup yayımlanmış sete
taşımak, düzeltilmiş bir şeyi iki kez düzeltmeye kalkmaktır; hangi dosyada
okuduğunu söylemek, ne bulduğunu söylemek kadar önemlidir.*

⚠️ Yol boyunca iki SINIR VAKA görüldü ve **bilerek değiştirilmedi**: *«Dün
durabilmişsin, bugün duramamışsın. İkisi de aynı hafta oldu»* ve *«İptali
soruyorsun ama devam ediyorsun — ikisi aynı hafta içinde duruyor»*. İkisi de
gündelik bir çıkarım (dün ile bugün çoğu zaman aynı haftadadır) ve savunulabilir
⇒ *savunulabilir bir çıkarımı «kusur» diye düzeltmek, aşırı düzeltmenin kendi
kusurudur.*

Girdi : data/judged/v0.0.10.jsonl
Çıktı : data/judged/v0.0.11.jsonl · reports/analiz/2026-09-18-v011-revizyon.md
Kullanım: uv run python scripts/analiz/2026-09-18-v011-sozcuk-revizyonu.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
GIRDI = KOK / "data/judged/v0.0.10.jsonl"
CIKTI = KOK / "data/judged/v0.0.11.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-v011-revizyon.md"

from checks import run_checks  # noqa: E402

# id öneki -> [(eski, yeni), …] · kullanıcının kendi sözcüğü
DUZELTME = {
    "693dea93d2ec0a8c": ([("Bugün eşin bir şey söylemedi", "Bugün hanımın bir şey söylemedi")],
                         "hanım"),
    "27723f592229e577": ([("Eşin oğlunu alıp annesine gitmiş", "Karın oğlunu alıp annesine gitmiş")],
                         "karı"),
    "dc5a22d008dee048": ([("eşinin avukatla konuştuğunu söylemesi",
                           "karının avukatla konuştuğunu söylemesi"),
                          ("Eşinin avukatla konuşması", "Karının avukatla konuşması")],
                         "karı"),
    "5d24f424239fa0ad": ([("Eşin bir an baktı", "Hanımın bir an baktı")], "hanım"),
    # ⛔ BEŞİNCİ KAYIT İLK TARAMADA GÖRÜNMEDİ: ölçüm deseni ekleri ELLE sayıyordu
    # ve *«eşine»* listede yoktu. Desen deponun kapalı çekim listesine bağlanınca
    # çıktı. ➡️ *Elle yazılmış bir ek listesi, aradığı şeyin bir kısmını görmez.*
    "92ece2a209490788": ([("eşine ne diyeceğini", "hanımına ne diyeceğini")], "hanım"),
    # ⛔ ALTINCI KAYIT ÜÇÜNCÜ ÖLÇÜM DENEMESİNDE ÇIKTI. İlk iki desen (elle ek listesi,
    # sonra `tr_fold`+`AD_CEKIM_EKI`) bunu göremiyordu ⇒ *«6 ihlal»* gerçek sayı,
    # daha önce raporladığım 4 ve 3 artefaktmış.
    "32e9e8ad57506950": ([("eşinin kurduğu cümle", "karının kurduğu cümle")], "karı"),
}
BAYAT = ("metin bu kayıtta düzeltildi; yargı düzeltmeden ÖNCEKİ metne verildi "
         "(kullanıcının sözcüğünü koruma, 2026-09-18)")
ES = re.compile(r"\b[EeĒ]ş(im|in|i|imle|inle|ime|ine|imin|inin|inden)?\b")


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]


def main() -> int:
    ham = GIRDI.read_bytes()
    kayitlar = [json.loads(s) for s in ham.decode("utf-8").splitlines() if s.strip()]
    rapor, hata = [], []
    for r in kayitlar:
        d = next(((k, v) for k, v in DUZELTME.items() if r["id"].startswith(k)), None)
        if not d:
            continue
        anahtar, (ciftler, sozcuk) = d
        asst = [m for m in r["messages"] if m["role"] == "assistant"]
        uygulanan = []
        for eski, yeni in ciftler:
            n = sum(m["content"].count(eski) for m in asst)
            if n != 1:
                hata.append(f"{anahtar}: «{eski[:40]}» {n} kez geçiyor (1 bekleniyordu)")
                continue
            for m in asst:
                if eski in m["content"]:
                    m["content"] = m["content"].replace(eski, yeni, 1)
                    uygulanan.append((eski, yeni))
        # ⭐ DOĞRULAMA: kayıtta artık «eş» biçimi KALMAMALI — tek tek değil, kayıt düzeyinde
        # ⭐ DOĞRULAMA: bu beş/altı kaydın hiçbirinde kullanıcı *«eş»* demiyor ⇒
        # düzeltmeden sonra asistan metninde de *«eş»* biçimi KALMAMALI.
        kalan = [mt.group(0) for m in asst for mt in ES.finditer(m["content"])]
        if kalan:
            hata.append(f"{anahtar}: düzeltmeden sonra hâlâ «eş» var: {kalan}")
            continue
        c = run_checks(r)
        if not c.get("passed"):
            hata.append(f"{anahtar}: run_checks DÜŞÜRÜYOR")
            continue
        j = r.setdefault("judge", {}) or {}
        j["bayat"] = True
        j["bayat_gerekce"] = BAYAT
        r["judge"] = j
        rapor.append({"id": r["id"], "sozcuk": sozcuk, "degisim": uygulanan,
                      "parti": (r.get("gen_meta") or {}).get("parti"),
                      "sira": (r.get("gen_meta") or {}).get("parti_sira")})

    bulunamayan = [k for k in DUZELTME if not any(x["id"].startswith(k) for x in rapor)]
    if hata or bulunamayan:
        print("⛔ REVİZYON UYGULANMADI:")
        for h in hata + [f"{b}: kayıt bulunamadı" for b in bulunamayan]:
            print("   ", h)
        return 1

    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kayitlar),
                     encoding="utf-8")
    sat = ["# v0.0.11 — kullanıcının kendi sözcüğü geri konuldu", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Girdi:** `{GIRDI.relative_to(KOK)}` SHA256-16 `{_sha(ham)}` · "
           f"**{len(kayitlar)}** kayıt  ",
           f"**Çıktı:** `{CIKTI.relative_to(KOK)}` SHA256-16 `{_sha(CIKTI.read_bytes())}`", "",
           f"⭐ **{len(rapor)} kayıt düzeltildi**, öteki {len(kayitlar)-len(rapor)} kayıt "
           "bayt bayt aynı.", "",
           "| kayıt | parti | kullanıcının sözcüğü | değişim |", "|---|---|---|---|"]
    for x in rapor:
        dg = " · ".join(f"*«{a}»* → *«{b}»*" for a, b in x["degisim"])
        sat.append(f"| `{x['id'][:10]}` | {x['parti']} #{x['sira']} | *«{x['sozcuk']}»* | {dg} |")
    sat += ["", "⭐ **Doğrulama kayıt düzeyinde:** düzeltmeden sonra dört kaydın asistan",
            "metninde *«eş»* biçimi **hiç kalmadı** — tek tek dizge saymak yetmez, çünkü",
            "aynı kayıtta başka bir yerde de geçebilirdi.", "",
            "## ⛔⛔ Beşinci kalem yoktu", "",
            "T165 `v5-parti4 #3`teki dayanaksız *«İkisi de aynı hafta içinde»* iddiasını kusur",
            "saymıştı; ama o okuma **ham parti dosyası** üzerindeydi. Yayımlanmış sette cümle",
            "çoktan *«İkisi de arka arkaya oldu»* olmuş ⇒ **kalem yok** (v0.0.10'da 0 eşleşme).", "",
            "➡️⭐⭐ *Bir kusuru ham korpusta okuyup yayımlanmış sete taşımak, düzeltilmiş bir şeyi",
            "iki kez düzeltmeye kalkmaktır. Hangi dosyada okuduğunu söylemek, ne bulduğunu",
            "söylemek kadar önemlidir.*", "",
            "## ⚠️ Değiştirilmeyen iki sınır vaka", "",
            "| kayıt | cümle | neden değiştirilmedi |", "|---|---|---|",
            "| `v4-parti2 #10` | *«Dün durabilmişsin, bugün duramamışsın. İkisi de aynı hafta "
            "oldu.»* | dün ile bugün çoğu zaman aynı haftadadır — savunulabilir çıkarım |",
            "| `v5-parti5 #14` | *«İptali soruyorsun ama devam ediyorsun — ikisi aynı hafta "
            "içinde duruyor.»* | konuşmada *«üç haftadır»* çerçevesi var; gevşek ama uydurma "
            "değil |", "",
            "➡️ *Savunulabilir bir çıkarımı «kusur» diye düzeltmek, aşırı düzeltmenin kendi",
            "kusurudur.*", "",
            "## ⛔⛔ Dört kaydın yargısı BAYAT", "",
            "Judge bu kayıtları düzeltmeden ÖNCEKİ metin üzerinde puanladı ⇒ `judge.bayat: true`",
            "ve gerekçe yazıldı. Puanlar düşürülmedi ama bu dört kaydın judge alanları hiçbir",
            "sayıda sessizce kullanılamaz. Yeniden yargılama **yapılmadı**.", ""]
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    (KOK / f"reports/analiz/{TARIH}-v011-revizyon.json").write_text(
        json.dumps({"tarih": TARIH, "girdi_sha256_16": _sha(ham),
                    "cikti_sha256_16": _sha(CIKTI.read_bytes()), "duzeltme": rapor},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n".join(sat))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
