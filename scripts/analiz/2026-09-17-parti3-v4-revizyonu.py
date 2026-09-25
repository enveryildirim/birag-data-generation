#!/usr/bin/env python3
"""v5-parti3'ü v0.0.8 için hazırlar: §8b′ iki kayıtta uygulanır.

⛔⛔ **v0.0.7 bu kayıtları DÜZELTİLMEMİŞ hâliyle içeriyor ve değişmez (Kural 4).**
v0.0.8 düzeltilmiş sürümü taşır ⇒ aynı `id`ler iki sürümde FARKLI metinle
duracak ve bu CARD.md'de **ilan edilmelidir**; yoksa iki sürümün puanları
sessizce karşılaştırılabilir hâle gelir.

⭐ Girdi `v5-parti3.v3.jsonl` — T115'in eşik düzeltmesini (#14, #37) taşıyan
sürüm. v0.0.7'deki sürüm `v2`'dir.

Düzeltilen iki kusur:
  **#37** — *«söyleyebilecek olan orası»*: hekime bir yetkinlik atfediyor ve
     *«orası»* bir kişiyi yer gibi gösteriyor. §8b′: yönlendirme, kurumun ne
     yapabileceğini iddia etmez.
  **#54** — *«Belge bir kâğıt istiyor, içmemeni değil»*: ortada BAĞLAM BELGESİ
     YOKKEN resmî bir evrakın ne istediği bir olgu gibi bildiriliyor. Judge
     bunu `kurum_yordam_ihlali` saymıştı ve `build.py` kapısı yalnız klinik
     güvenliğe baktığı için kayıt v0.0.7'ye GİRDİ (o derlemenin açık kalemi).
     ⭐ Cümlenin terapötik işlevi (özerklik: içmemeyi sen seçtin) korunuyor;
     düşen şey evrak hakkındaki iddia.
"""
from __future__ import annotations
import json
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
GIRDI = KOK / "data/candidates/v5-parti3.v3.jsonl"
CIKTI = KOK / "data/candidates/v5-parti3.v4.jsonl"
TARIH = "2026-09-17"

D = {
 37: ('Ne olduğunu ben söyleyemem; söyleyebilecek olan orası ve ilk adım bu cümleyi olduğu gibi söylemek olabilir.',
      'Ne olduğunu ben söyleyemem; ilk adım bu cümleyi olduğu gibi söylemek olabilir.',
      "§8b′", "«söyleyebilecek olan orası» hekime yetkinlik atfediyordu."),
 54: ('İkincisini kimse senden istemedi. Belge bir kâğıt istiyor, içmemeni değil.',
      'İkincisini kimse senden istemedi. O kâğıdın ne istediğini ben bilmiyorum — ama bu hafta içmemeyi sen seçtin.',
      "§8b′", "Bağlam belgesi YOKKEN resmî evrakın içeriği iddia ediliyordu "
      "(judge: `kurum_yordam_ihlali`). v0.0.7'nin açık kalemi kapatıldı."),
}


def main() -> int:
    kayitlar = [json.loads(s) for s in GIRDI.read_text(encoding="utf-8").splitlines() if s.strip()]
    degisen, hata = [], 0
    for r in kayitlar:
        n = r["gen_meta"]["parti_sira"]
        if n not in D:
            continue
        eski, yeni, kural, gerekce = D[n]
        son = [m for m in r["messages"] if m["role"] == "assistant" and m.get("content")][-1]
        if son["content"].count(eski) != 1:
            print(f"  ⛔ EŞLEŞME #{n}: {son['content'].count(eski)}")
            hata += 1
            continue
        son["content"] = son["content"].replace(eski, yeni)
        r["judge"] = None
        r["gen_meta"].setdefault("revizyon", []).append(
            {"tarih": TARIH, "kural": kural, "gerekce": gerekce, "kaynak": "judge + §8b′ geriye dönük"})
        degisen.append(n)
    # ⛔ #14 metni v2'den FARKLI (T115) ⇒ eski puanı devralamaz, yeniden yargılanır.
    for r in kayitlar:
        if r["gen_meta"]["parti_sira"] == 14:
            r["judge"] = None
    CIKTI.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in kayitlar),
                     encoding="utf-8")
    print(f"v5-parti3: {len(degisen)} kayıt revize {sorted(degisen)} · #14 yargısı da boşaltıldı (T115 metni)")
    print(f"→ {CIKTI.relative_to(KOK)}")
    return 1 if hata else 0


if __name__ == "__main__":
    raise SystemExit(main())
