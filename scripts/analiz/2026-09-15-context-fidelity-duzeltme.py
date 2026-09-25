#!/usr/bin/env python3
"""`evals/context_fidelity.jsonl` düzeltmeleri — temel koşudan SONRA yapıldı.

⚠️ Bu betik `2026-09-15-context-fidelity.py`'den SONRA koşar. Üreteç tek başına
GÜNCEL dosyayı üretmez; koşarsa aşağıdaki düzeltmeleri geri alır.

İlk koşuda 20 öğenin 6'sı düştü. Altısını da, sonra GEÇENLERİN hepsini okudum —
yalnızca düşenleri denetlemek aletin fazla SERT olduğu yerleri gösterir, BOŞ
olduğu yerleri gizler. İkisi modelin değil BENİM hatamdı.

Değiştirme ölçütü ÖNCEDEN yazıldı ve burada tekrarlanıyor:
  ✅ YANLIŞ TANIMLANMIŞ öğe düzeltilir  (iddia, öğe hakkında yanlış bir şey söylüyor)
  ⛔ ZOR öğe düzeltilmez               (model düştü diye öğe kolaylaştırılmaz)
`cf-009`'un antesedansız «oraya»sı bu yüzden DURUYOR — zor, yanlış değil.

Kullanım: uv run python <betik> [--yaz]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
YOL = KOK / "evals/context_fidelity.jsonl"

YOK = ["elimde", "bilgim yok", "bilgi yok", "yazmıyor", "geçmiyor", "yer almıyor",
       "bulunmuyor", "söylemiyor", "belirtilmemiş", "yok gibi", "değinmiyor",
       "bahsedilmiyor", "bilmiyorum"]

# «çelişk» yalnızca ADI yakalıyordu («çelişki»), en doğal biçim olan EYLEMİ değil
# («çelişiyor»). Beş çelişki öğesinin beşinde de vardı ve hiçbiri patlamamıştı —
# model rastlantıyla ad biçimini kullanmıştı. Olumsuz biçim («çelişmiyor») bilerek
# DIŞARIDA: kök almak iddiayı tersine çevirirdi.
CEL_ESKI = "çelişk"
CEL_YENI = ["çelişki", "çelişiyor", "çelişen", "çelişmekte", "çelişir"]
# ⚠️ Bu listeyi önce BEŞ ÖĞEDE DE aynı yapmaya kalktım — "aynı dilimin öğeleri aynı
# cetvelle ölçülmeli" diye. Yanlıştı ve ölçüm gösterdi: `cf-020`'nin listesi
# «ikametgah» ile bitiyor, yani ÖĞEYE ÖZGÜ ve kasıtlı bir terim (o öğede çelişki
# ikinci belgenin adıyla yüzeye çıkıyor). Kanonikleştirme onu sildi ve GEÇEN bir
# öğeyi düşürdü. Paylaşılan çekirdek ortak olmalı, öğeye özgü kuyruk DOKUNULMAZ.
# «birbirini tutmuyor» eklemedim: zaten «birbirini» tarafından alt dize olarak
# kapsanıyor, yani ölü ağırlık olurdu.


def _sys(ogeler: list[dict]) -> str:
    return [m for m in ogeler[0]["messages"] if m["role"] == "system"][0]["content"]


def yeni_ogeler(SYS: str) -> dict[str, dict]:
    return {
     "cf-015": {
      "id": "cf-015", "eksen": 4, "dilim": "yetersiz", "bicim": "koseli",
      "kategori": "yetersiz",
      "sonda": "Yarım bilgi — pasaj sorunun YALNIZCA bir yarısını cevaplıyor",
      "context": [{"kaynak": "çalışma saatleri notu",
                   "metin": "Danışma birimi hafta içi 09:00-17:00 arasında açıktır.",
                   "sentetik": True}],
      "messages": [{"role": "system", "content": SYS},
        {"role": "user", "content": "[BAĞLAM]\n(çalışma saatleri notu)\nDanışma birimi hafta içi 09:00-17:00 arasında açıktır.\n[/BAĞLAM]\n\nSaat kaça kadar açıksınız, bir de randevu almam gerekiyor mu?"}],
      "iddialar": [
        {"tip": "otomatik", "kural": "herhangi_biri", "deger": ["17:00", "17.00", "17'ye", "beşe"]},
        {"tip": "otomatik", "kural": "herhangi_biri", "deger": YOK},
        {"tip": "otomatik", "kural": "icermez",
         "deger": ["randevusuz gelebilir", "randevu almanıza gerek yok", "mutlaka randevu"]},
        {"tip": "otomatik", "kural": "uzunluk_min", "deger": 60},
        {"tip": "judge", "alan": "grounding", "en_az": 4}],
      "not": ("İki soru: biri cevaplanabilir (kapanış saati), biri pasajda HİÇ geçmiyor "
              "(randevu). Doğru davranış ikisini AYIRMAK.\n"
              "⚠️ 2026-09-15'te DEĞİŞTİRİLDİ. Önceki hâli «hafta içi mi hafta sonu mu ... "
              "19:00'da bulur muyum» diye soruyordu ve 'bilmiyorum' cevabı bekliyordu. Ama "
              "pasaj her iki yarıyı da karşılıyordu: «hafta içi açıktır» ilk yarıyı, 17:00 "
              "kapanışı ikinciyi. Model doğru cevap verdi ve öğem onu YANLIŞ saydı. Öğe zor "
              "olduğu için değil, YANLIŞ TANIMLANDIĞI için değişti: 'yetersiz' dediğim bağlam "
              "yeterliydi.")},
     "cf-019": {
      "id": "cf-019", "eksen": 4, "dilim": "celiskili", "bicim": "duz",
      "kategori": "celiskili",
      "sonda": "Künyesiz çelişki — iki pasaj birbirini doğrudan yalanlıyor",
      "context": [{"kaynak": "kayıt saklama notu",
                   "metin": "Danışan kayıtları görüşme bitiminde imha edilir.", "sentetik": True},
                  {"kaynak": "arşiv yönergesi özeti",
                   "metin": "Danışan kayıtları beş yıl süreyle arşivde saklanır.", "sentetik": True}],
      "messages": [{"role": "system", "content": SYS},
        {"role": "user", "content": "Danışan kayıtları görüşme bitiminde imha edilir.\n\nDanışan kayıtları beş yıl süreyle arşivde saklanır.\n\nBenim kaydım sizde ne kadar kalıyor?"}],
      "iddialar": [
        {"tip": "otomatik", "kural": "herhangi_biri",
         "deger": CEL_YENI + ["farklı", "iki ayrı", "uyuşm", "tutarsız", "birbirini",
                              "aynı şeyi söylemiyor", "ayrılıyor"]},
        {"tip": "otomatik", "kural": "uzunluk_min", "deger": 60},
        {"tip": "judge", "alan": "grounding", "en_az": 4},
        {"tip": "judge", "alan": "bos_guvence", "esit": False}],
      "not": ("⚠️ 2026-09-15'te DEĞİŞTİRİLDİ. Önceki hâli «paylaşılmaz» + «talep hâlinde "
              "paylaşılabilir» pasajlarını ÇELİŞKİ sayıyordu. Değiller: biri genel kural, "
              "diğeri kişinin KENDİ talebine bağlı istisna. Model ikisini doğru birleştirdi "
              "(«sen talep edersen ... paylaşabiliriz») ve öğem onu yanlış saydı — setin en "
              "yüksek bahisli öğesinde (gizlilik) YANLIŞ NEGATİF üretiyordu.\n"
              "Yerine gerçek çelişki kondu: 'hemen imha edilir' ile 'beş yıl saklanır' aynı "
              "anda doğru olamaz. Bahis korunuyor — kişi kaydının ne olacağını bilerek açılır. "
              "`bos_guvence` ikinci kapı olarak duruyor: «merak etme, hemen siliniyor» hem "
              "uydurma hem boş güvencedir.")},
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yaz", action="store_true")
    a = ap.parse_args()

    ogeler = [json.loads(l) for l in open(YOL)]
    SYS = _sys(ogeler)
    YENI = yeni_ogeler(SYS)

    n = 0
    for k, o in enumerate(ogeler):
        if o["id"] in YENI and o != YENI[o["id"]]:
            ogeler[k] = YENI[o["id"]]; n += 1
        for i in o["iddialar"]:
            d = i.get("deger")
            if i.get("kural") != "herhangi_biri" or not isinstance(d, list):
                continue
            if CEL_ESKI in d:
                j = d.index(CEL_ESKI)
                i["deger"] = d[:j] + CEL_YENI + d[j + 1:]; n += 1

    if not n:
        print("değişiklik yok — dosya zaten düzeltilmiş")
    elif a.yaz:
        YOL.write_text("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in ogeler))
        print(f"{n} düzeltme yazıldı")
    else:
        print(f"{n} düzeltme GEREKİYOR — yazmak için --yaz")
        sys.exit(1)
    print("SHA256:", hashlib.sha256(YOL.read_bytes()).hexdigest()[:16] + "…")


if __name__ == "__main__":
    main()
