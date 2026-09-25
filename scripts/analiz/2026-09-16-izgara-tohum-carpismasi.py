# -*- coding: utf-8 -*-
"""v4-parti2 ızgarası ile tohum meta'sı çarpışıyor mu — `motivasyon` ekseni.

⛔ Blok 3 yazılırken görüldü: ızgara `#44`, `#57`, `#59` için `yasal_zorunluluk`
diyor ama üç tohumun **hiçbirinde** hukuki öge yok (`ic_motivasyon`,
`ic_motivasyon`, `tetikleyici_olay`). Izgarayı onurlandırmak, olmayan bir hukuki
durum **uydurmayı** gerektirirdi (Kural 3/6).

⭐ Ayrım: **düzleştirme ile uydurma aynı şey değildir.**
  · düzleştirme — tohum daha özgül, ızgara genele çekmiş (`aile_baskisi -> ic`).
    Bilgi KAYBI; `gen_meta.motivasyon_tohum` yazılınca geri alınabilir.
  · uydurma — tohumda olmayan bir durum ızgaradan GELMİŞ. Bilgi ÜRETİMİ;
    geri alınamaz, korpusa sahte bir vaka girer.
⇒ Düzleştirmede ızgara korunur ve tohum değeri kayda yazılır; uydurmada
  **tohum kazanır** ve sapma kayda yazılır.
"""
from __future__ import annotations
import hashlib, json, os, sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent.parent
TOHUM = KOK / "data/seeds.jsonl"
# ⛔⛔ PLAN YOLU SABİT YAZILMIŞTI ve betik `sys.argv`'ye BAKMIYORDU: başka bir
# partinin dosyası verildiğinde onu SESSİZCE yok sayıp v4-parti2'nin sayılarını
# basıyordu. Bir betiğin argüman almaması, argümanı reddetmesi demek DEĞİL —
# görmezden gelmesi demek ve çıktı doğru görünüyor. ⇒ Ortam değişkeniyle
# parametreleştirildi; çıktı adı da girdiden türetiliyor ki iki parti aynı
# dosyayı ezmesin (Kural 7).
PLAN = KOK / os.environ.get("BIRAG_CARPISMA_PLAN", "data/plan/v4-parti2.jsonl")
CIKTI = KOK / f"reports/analiz/2026-09-16-izgara-tohum-carpismasi-{PLAN.stem}.json"

# ızgaranın 3 değerli sözlüğü (K22) <- tohumun 5 değerli sözlüğü.
# `tetikleyici_olay` ve `duygusal_regulasyon` K22'de KARŞILIĞI YOK -> `ic`e düşer.
ESLEME = {
    "ic_motivasyon": "ic",
    "aile_baskisi": "aile_baskisi",
    "yasal_zorunluluk": "yasal_zorunluluk",
    "tetikleyici_olay": "ic",        # ⚠️ karşılığı yok, geri düşme
    "duygusal_regulasyon": "ic",     # ⚠️ karşılığı yok, geri düşme
}
GERI_DUSME = {"tetikleyici_olay", "duygusal_regulasyon"}


def main() -> None:
    ham_t, ham_p = TOHUM.read_bytes(), PLAN.read_bytes()
    tohum = {r["seed_id"]: r.get("meta", {})
             for r in (json.loads(s) for s in ham_t.decode("utf-8").splitlines() if s.strip())}
    plan = [json.loads(s) for s in ham_p.decode("utf-8").splitlines() if s.strip()]

    duz, uydurma, tam = [], [], 0
    gecis = Counter()
    for r in plan:
        t = tohum.get(r["seed_id"], {}).get("motivasyon")
        g = r["motivasyon"]
        gecis[(t, g)] += 1
        esl = ESLEME.get(t)
        if esl == g:
            tam += 1
            continue
        # ızgara tohumdan DAHA ÖZGÜL bir durum iddia ediyorsa: uydurma
        if g != "ic" and esl != g:
            # ⭐ Kanıt: tohumun KENDİ notu. `yasal_zorunluluk` kimi tohumda
            # mahkeme değil KURUMSAL yönlendirme demek (okul, işyeri) ve bunu
            # tohumun `notlar.motivasyon_notu` alanı söylüyor — varsayılmıyor.
            notlar = tohum.get(r["seed_id"], {}).get("notlar") or {}
            uydurma.append({"sira": r["sira"], "seed_id": r["seed_id"],
                            "tohum": t, "izgara": g,
                            "geri_dusme_mi": t in GERI_DUSME,
                            "tohum_motivasyon_notu": notlar.get("motivasyon_notu"),
                            "tohum_context": notlar.get("context"),
                            "duzeltme": ESLEME.get(t)})
        else:
            duz.append({"sira": r["sira"], "tohum": t, "izgara": g})

    ozet = {
        "tarih": "2026-09-16",
        "betik": "scripts/analiz/2026-09-16-izgara-tohum-carpismasi.py",
        "girdi": [str(PLAN.relative_to(KOK)), str(TOHUM.relative_to(KOK))],
        "plan_sha256": hashlib.sha256(ham_p).hexdigest(),
        "tohum_sha256_16": hashlib.sha256(ham_t).hexdigest()[:16],
        "satir": len(plan),
        "tam_uyum": tam,
        "duzlestirme": len(duz),
        "uydurma": len(uydurma),
        "gecis_tablosu": {f"{k[0]} -> {k[1]}": v for k, v in gecis.most_common()},
        "uydurma_satirlari": uydurma,
        "duzlestirme_satirlari": duz,
    }
    CIKTI.write_text(json.dumps(ozet, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"satır {len(plan)} · tam uyum {tam} · düzleştirme {len(duz)} · ⛔ uydurma {len(uydurma)}")
    for k, v in gecis.most_common():
        isaret = "  " if ESLEME.get(k[0]) == k[1] else ("⛔" if k[1] != "ic" else "⚠️")
        print(f"  {isaret} {str(k[0]):>20} -> {k[1]:<18} {v}")
    print("⛔ uydurma satırları (tohum kazanır):")
    for u in uydurma:
        print(f"   #{u['sira']:>2} ızgara={u['izgara']:<18} tohum={u['tohum']:<18}"
              f" -> düzeltme={u['duzeltme']}"
              + (f"  · not: {u['tohum_motivasyon_notu']}" if u["tohum_motivasyon_notu"] else ""))
    print(f"→ {CIKTI.relative_to(KOK)}")


if __name__ == "__main__":
    main()
