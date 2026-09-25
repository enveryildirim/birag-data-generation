#!/usr/bin/env python3
"""§5a″ ölçütüne göre geriye dönük düzeltilen üç kaydı yeni SÜRÜM dosyasına yazar.

⛔⛔ **Neden var.** T115: geriye dönük tarama, parti6'da ZORUNLU sapma saydığım
üç tablonun parti3/parti4'te yönlendirmesiz geçtiğini gösterdi:

| kayıt | tablo | parti6'daki karşılığı |
|---|---|---|
| `v5-parti3.v2 #37` | *«eve nasıl geldim hatırlamıyorum»* — hafıza boşluğu | #52, #42 → sapıldı |
| `v5-parti3.v2 #14` | üç gece uykusuzluk + önden ilaç alma | #17, #34 → sapıldı |
| `v5-parti4 #2` | *«nefesim daralıyor»* + korku | #17 (parti4) → sapıldı |

Tohum havuzu değişmedi, eksen kotası değişmedi; değişen ÜRETİCİNİN EŞİĞİ.

⛔ **Orijinal dosyalar DEĞİŞTİRİLMİYOR** (Kural 7): `v5-parti3.v2` ve
`v5-parti4` `datasets/v0.0.7`'nin kaynağı ve o sürüm yayımlandı. Düzeltme yeni
sürüm dosyalarına yazılıyor; v0.0.8 bunları kullanır, v0.0.7 olduğu gibi kalır.

⭐ `id` kullanıcının İLK mesajından türetiliyor ve o mesajlar değişmiyor ⇒
kimlikler sabit kalıyor. ⛔ Ama metin değiştiği için `judge` alanı BOŞALTILIYOR:
eski puan yeni metni tarif etmez ve sessizce kalsaydı sayı yalan söylerdi.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]

SAPMA = ("⛔ GÜVENLİK SAPMASI (geriye dönük, 2026-09-17). Izgara `sinir_tipi: yok` "
         "diyordu ve kayıt o hâliyle üretilmişti. `uretim-v5` §5a″ ölçütü yazıldıktan "
         "sonra yapılan geriye dönük tarama (T115), aynı tablonun v5-parti6'da "
         "ZORUNLU sapma sayıldığını gösterdi. Aynı tabloya iki farklı davranış "
         "öğretmek güvenlik ekseninde tutarsızlık üretir ⇒ kayıt ölçüte göre "
         "düzeltildi. Orijinali `{kaynak}` dosyasında olduğu gibi duruyor.")

DUZELTME = {
    ("v5-parti3.v2", 37): dict(st="rol_siniri_yonlendirme", cevap="""\"Alkolle alakası yok\" diyorsun. Bunu ben de bilmiyorum, sen de bilmiyorsun — ama meyhanede olduğunu da aynı cümlede söyledin.

Eve nasıl geldiğini hatırlamamak bedende olan bir şey ve bunu bir hekimin bilmesi gerekiyor. Ne olduğunu ben söyleyemem; söyleyebilecek olan orası ve ilk adım bu cümleyi olduğu gibi söylemek olabilir.

Yorgunluk ve uykusuzluk gerçekten olabilir. Sadece \"alakası yok\" cümlesi, olabilecek başka bir şeyi baştan kapatıyor.

Eve nasıl geldiğini hatırlamamak daha önce de oldu mu?"""),
    ("v5-parti3.v2", 14): dict(st="rol_siniri_yonlendirme", cevap="""İkisinin de cevabı metinde var: yenilemeye kızın gidebilir, kendin gitmek zorunda değilsin. Aynı gün içinde birden çok yenileme kaydı ise açılmıyor.

Kaç kutu alınacağına dair bir şey söylemiyorum, o bana düşmez. Ama üç gece uyuyamamış olman ve şimdi önden almaya başlaman, bir hekimin bilmesi gereken bir şey; ilk adım, bu ikisini olduğu gibi reçeteyi yazan yere söylemek olabilir.

Üç gece uyuyamamışsın ve şimdi bir daha o üç geceyi yaşamamak için önden alıyorsun. İkisi arasındaki bağı sen kurdun."""),
    ("v5-parti4", 2): dict(st="rol_siniri_yonlendirme", cevap="""Ona \"abartıyorsun\" demişsin, buraya \"korktum\" yazmışsın. İki ayrı cevap, iki ayrı yere.

Nefesinin neden daraldığını ben söyleyemem; o bilgi bende yok. Ama oda arkadaşının söylediği şeyi tekrarlayacağım: bunu bir hekimin görmesi gerekiyor ve ilk adım aile hekimliğine bu cümleyi olduğu gibi söylemek olabilir.

\"Sanırım\" diye ekledin. Korkuyu bile ihtiyatla söylüyorsun."""),
}

YENI = {"v5-parti3.v2": "v5-parti3.v3", "v5-parti4": "v5-parti4.v2"}


def main() -> int:
    n = 0
    for kaynak, hedef in YENI.items():
        gi = KOK / f"data/candidates/{kaynak}.jsonl"
        ci = KOK / f"data/candidates/{hedef}.jsonl"
        out = []
        for s in gi.read_text(encoding="utf-8").splitlines():
            if not s.strip():
                continue
            r = json.loads(s)
            anahtar = (kaynak, r["gen_meta"]["parti_sira"])
            if anahtar in DUZELTME:
                d = DUZELTME[anahtar]
                son = [m for m in r["messages"] if m["role"] == "assistant"][-1]
                assert son["content"] != d["cevap"], f"{anahtar}: zaten düzeltilmiş"
                son["content"] = d["cevap"]
                r["gen_meta"]["sinir_tipi"] = d["st"]
                r["gen_meta"]["izgara_sapmasi"] = SAPMA.format(kaynak=kaynak)
                r["judge"] = None          # ⛔ eski puan yeni metni tarif etmez
                n += 1
            out.append(json.dumps(r, ensure_ascii=False))
        ci.write_text("\n".join(out) + "\n", encoding="utf-8")
        print(f"→ {ci.relative_to(KOK)} ({len(out)} kayıt)")
    print(f"⭐ düzeltilen kayıt: {n}/3 · orijinaller değiştirilmedi")
    return 0 if n == 3 else 1


if __name__ == "__main__":
    raise SystemExit(main())
