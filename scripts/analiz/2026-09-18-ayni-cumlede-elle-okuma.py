#!/usr/bin/env python3
"""27 alıntısız *«aynı cümlede»* iddiası — T140'ın açık kalemi elle okundu.

⛔⛔ **T140 bunu öngörmüştü ve haklı çıktı.** Yapısal atıf kapısı yalnız **≥2
alıntı** taşıyan iddiaları otomatik sınayabiliyor; alıntısız ya da tek alıntılı
olanlar *«elle okunacak»* yığınına düşüyor ve o yığın **hiç okunmamıştı**.
T140'ın kaydı: *«26 alıntısız iddia hâlâ ELLE okunmadı»*.

⭐ Okundu: `datasets/v0.0.9/train.jsonl`'de **27** iddia · **7'si YANLIŞ** (%26).
Yanlışların hepsi aynı biçimde: iddia *«aynı CÜMLEDE»* diyor, oysa iki öge
kullanıcının **aynı mesajındaki AYRI cümlelerinde** duruyor.

➡️⭐⭐ *Kapının otomatik sınayabildiği kısım temiz (0 ihlal); kusurun tamamı
kapının ulaşamadığı yerde birikmiş. Bir kapının «0 ihlal» demesi, kapının
BAKABİLDİĞİ yerde 0 ihlal olduğu demektir.*

⛔ **Ve biri tam olarak daha önce iki kez düzeltilmiş kusur:** `#20`de iddia bir
alıntı taşıyor (*«net kazanmışım»*) ama **tek** alıntı taşıdığı için kapı onu
sınayamadı — aynı kusur `v5-parti8 #13` ve `#15`te iki alıntılı olduğu için
yakalanmıştı. ⇒ *Kapının eşiği (≥2 alıntı) kusurun kendisiyle ilgisiz; yalnız
kapının görme koşuluyla ilgili.*

⚠️ Kararlar ELLE verildi (K30) ve ölçüt şu: iddia *«aynı cümlede»* diyorsa,
kullanıcının TEK bir cümlesi iki ögeyi birden taşımalı. Cümle bölme kapının
kendi `_cumleler` işleviyle yapıldı — ikinci bir tanım yazılmadı (K97).

Girdi : datasets/v0.0.9/train.jsonl
Çıktı : reports/analiz/2026-09-18-ayni-cumlede-elle-okuma.md
Kullanım: uv run python scripts/analiz/2026-09-18-ayni-cumlede-elle-okuma.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-ayni-cumlede-elle-okuma.md"
SET = KOK / "datasets/v0.0.9/train.jsonl"

_s = importlib.util.spec_from_file_location(
    "yapisal", KOK / "scripts/analiz/2026-09-17-yapisal-atif-kapisi.py")
Y = importlib.util.module_from_spec(_s)
_s.loader.exec_module(Y)          # ⭐ cümle bölme ve iddia deseni ORADAN (K97)

# ⛔ KARAR: iddianın ayırt edici parçası -> (yanlış mı, gerekçe)
KARAR = {
    "Öğle arası çıkıp yaktığını da aynı cümlede":
        (True, "*«İnhaleri aldım, kullanmayı da öğrendim.»* ve *«Ama öğle arası çıkıp yine "
               "yaktım.»* — **iki ayrı cümle**"),
    "Üst kattaki oğlundan da aynı cümlede":
        (True, "*«Ben de aynı koltuğa oturmuşum gibi hissettim.»* ve *«Üst katta oğlum "
               "uyuyor.»* — **iki ayrı cümle**"),
    "Kahvaltı etmediğini ve iki tane içtiğini aynı cümlede":
        (True, "iki ayrı cümle ⛔ **ve ikinci kusur:** *«iki tane»* kullanıcının sözü değil, "
               "*«bir tane… sonra bir tane daha»*dan çıkarılmış bir SAYIM"),
    "Ama ikisini aynı cümlede tutabilmek":
        (True, "*«Hayatımın değişmesi gerektiğini biliyorum…»* ve *«Ama oyunu bırakmak "
               "istemiyorum…»* — **iki ayrı cümle**"),
    "İki şeyi aynı cümlede söyledin: hesabı":
        (True, "*«…hesabını yapmaya bile korkuyorum.»* ve *«Ama bu kahve bu sigara olmadan "
               "da yol gitmiyor…»* — **iki ayrı cümle**"),
    "aynı cümlede tam rakamı eşinin bilmediğini":
        (True, "⭐ *«…net kazanmışım.»* ve *«Bunu kimseye anlatmıyorum, eşim bile bilmiyor…»* "
               "— iki ayrı cümle. **Tek alıntı taşıdığı için kapı sınayamadı**"),
    "Üç haftadır uyuyamadığını da aynı cümlede":
        (True, "*«son üç haftadır uyuyamıyorum.»* ve *«…gerçekten işe yarıyor.»* — "
               "**iki ayrı cümle**"),
}


def _kayitlar():
    return [json.loads(s) for s in SET.read_text(encoding="utf-8").splitlines() if s.strip()]


def main() -> int:
    kayitlar = _kayitlar()
    d = json.loads((KOK / "reports/analiz/2026-09-17-yapisal-atif-kapisi.json"
                    ).read_text(encoding="utf-8"))
    if not any("train" in g["dosya"] for g in d.get("girdiler", [])):
        print("⛔ Kapı raporu bu sete ait değil; önce kapıyı bu setle koş.")
        return 1
    iddialar = d["elle_okunacak"]

    yanlis, dogru = [], []
    for b in iddialar:
        k = next((v for anahtar, v in KARAR.items() if anahtar in b["cumle"]), None)
        (yanlis if k and k[0] else dogru).append((b, k))

    # ⭐ Şablon bağlantısı (T139): bu kalıp sürümler boyunca büyüdü mü?
    # ⛔ İLK ÖLÇÜMÜM YANLIŞTI ve düzeltildi: satırda `thinking` ve `judge` alanları
    # da var; ham satır taraması *«aynı cümlede»*yi 97 kayıtta buluyordu, oysa
    # ASİSTAN CEVABINDA geçen cümle sayısı 42. ➡️ *Bir kalıbın korpusta ne kadar
    # büyüdüğünü ölçerken hangi ALANDA arandığı yazılmalı; JSONL satırı metin değil,
    # kayıttır ve kaydın çoğu modele hiç gitmez.*
    buyume = []
    for p in sorted(KOK.glob("datasets/v*/train.jsonl")):
        t = n = m = 0
        for satir in p.read_text(encoding="utf-8").splitlines():
            if not satir.strip():
                continue
            t += 1
            r = json.loads(satir)
            cev = " ".join(x.get("content") or "" for x in r.get("messages", [])
                           if x.get("role") == "assistant")
            n += "aynı cümlede" in cev
            m += "aynı mesajda" in cev
        buyume.append((p.parent.name, t, n, m))

    sat = ["# 27 alıntısız *«aynı cümlede»* iddiası — elle okundu", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Girdi:** `{SET.relative_to(KOK)}` · SHA256-16 "
           f"`{hashlib.sha256(SET.read_bytes()).hexdigest()[:16]}`", "",
           "⛔⛔ **T140'ın açık kalemi kapandı — ve T140 haklı çıktı.** Yapısal atıf kapısı",
           "yalnız **≥2 alıntı** taşıyan iddiaları otomatik sınayabiliyor; ötekiler *«elle",
           "okunacak»* yığınına düşüyor ve o yığın hiç okunmamıştı.", "",
           f"| | |", "|---|---:|",
           f"| kapının OTOMATİK sınadığı ihlal | **0** |",
           f"| elle okunacak iddia | **{len(iddialar)}** |",
           f"| ⛔ **elle okununca YANLIŞ çıkan** | **{len(yanlis)}** (%{100*len(yanlis)/len(iddialar):.0f}) |",
           "",
           "➡️⭐⭐ *Kapının otomatik sınayabildiği kısım temiz; kusurun tamamı kapının",
           "ULAŞAMADIĞI yerde birikmiş. Bir kapının «0 ihlal» demesi, kapının BAKABİLDİĞİ",
           "yerde 0 ihlal olduğu demektir.*", "",
           "## 1. ⛔ Yanlış çıkan iddialar", "",
           "Hepsi aynı biçimde yanlış: iddia *«aynı CÜMLEDE»* diyor, oysa iki öge",
           "kullanıcının **aynı mesajındaki AYRI cümlelerinde** duruyor.", "",
           "| # | iddia | neden yanlış |", "|---:|---|---|"]
    for b, k in yanlis:
        sat.append(f"| {b['sira']} | {b['cumle'][:100]} | {k[1]} |")
    sat += ["", "⭐ **Düzeltme mekanik ve aynı:** *«aynı cümlede»* → *«aynı mesajda»*. İki öge",
            "gerçekten aynı mesajda; yanlış olan tek şey iddianın **düzeyi**.", "",
            "⛔⛔ **Biri tam olarak daha önce iki kez düzeltilmiş kusur.** `#20`in iddiası bir",
            "alıntı taşıyor (*«net kazanmışım»*) ama **tek** alıntı taşıdığı için kapı onu",
            "sınayamadı; aynı kusur `v5-parti8 #13` ve `#15`te İKİ alıntılı olduğu için",
            "yakalanmıştı. ➡️ *Kapının eşiği (≥2 alıntı) kusurun kendisiyle ilgisiz, yalnız",
            "kapının GÖRME koşuluyla ilgili — ve kusur eşiğin altında da aynı sıklıkta var.*", "",
            "## 2. ⭐ Doğru çıkan iddialar", "", f"**{len(dogru)}** iddia doğrulandı; kullanıcının "
            "tek bir cümlesi iki ögeyi birden taşıyor. Örnekler:", "",
            "| # | iddia | kullanıcının cümlesi |", "|---:|---|---|"]
    ORNEK = {13: "Ama ağrım vardı, doktor verdi, ben de aldım.",
             53: "Suçlu hissediyorum ama aynı zamanda çok da kızgınım.",
             33: "ailem haklı olabilir oyun konusunda ama bunu kabul etmek çok zor.",
             47: "Kızıma yapıyorum bunu biliyorum ama elim gidiyor pakete."}
    for b, _ in dogru:
        o = ORNEK.get(b["sira"])
        if o:
            sat.append(f"| {b['sira']} | {b['cumle'][:80]} | *«{o}»* |")
    sat += ["", "## 3. ⭐ Şablon bağlantısı (T139)", "",
            "T139: *«her yeni kural, bir sonraki şablonun tohumu»*. Bu kalıp da bir kuralın",
            "(T104 yapısal atıf) ürünü — sürümler boyunca nasıl büyümüş:", "",
            "⚠️ Sayım **yalnız asistan cevabında** — `thinking` ve `judge` alanları hariç.",
           "⛔ İlk ölçümüm ham JSONL satırında aramıştı ve *«aynı cümlede»*yi 97 kayıtta",
           "buluyordu; asistan cevabındaki gerçek sayı **çok daha az**. ➡️ *Bir JSONL satırı",
           "metin değil KAYITTIR ve kaydın çoğu modele hiç gitmez.*", "",
           "| sürüm | kayıt | *«aynı cümlede»* | *«aynı mesajda»* |", "|---|---:|---:|---:|"]
    for ad, t, n, m in buyume:
        sat.append(f"| `{ad}` | {t} | {n} | {m} |")
    sat += ["", "⚠️ *«aynı mesajda»* sayısının artışı T140'ın düzeltmelerinden geliyor — yani",
            "kuralın kendisi de yeni bir kalıp doğuruyor. ⛔ Şablonlaşmayı yakalayan bir kapı",
            "hâlâ yok (T139'un açık kalemi).", "",
            "## ⛔ Bu okumanın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **Düzeltme UYGULANMADI** | `datasets/v0.0.9` IMMUTABLE (Kural 4); yedi kayıt "
            "sette **duruyor** ve düzeltme bir sonraki derlemeye kalıyor |",
            "| ⛔ **Kararlar elle verildi** (K30) | ölçüt yazılı — *«aynı cümlede»* diyen bir "
            "iddia için kullanıcının TEK cümlesi iki ögeyi taşımalı — ama hüküm benim |",
            "| ⛔ **Yalnız bu set okundu** | aday dosyalardaki aynı kalıp taranmadı |",
            "| ⚠️ **Kapı hâlâ ulaşamıyor** | ≥2 alıntı eşiği duruyor; bu okuma kapıyı "
            "güçlendirmedi, yalnız onun göremediği yeri bir kez okudu |", ""]

    (KOK / f"reports/analiz/{TARIH}-ayni-cumlede-elle-okuma.json").write_text(
        json.dumps({"tarih": TARIH, "girdi": str(SET.relative_to(KOK)),
                    "iddia": len(iddialar), "yanlis": [b["sira"] for b, _ in yanlis],
                    "buyume": buyume}, ensure_ascii=False, indent=2), encoding="utf-8")
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[5:]))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
