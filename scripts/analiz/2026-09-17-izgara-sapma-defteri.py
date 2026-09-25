#!/usr/bin/env python3
"""İlan edilmiş ızgara sapmalarını partiler boyunca biriktirir.

⛔⛔ **Neden bir defter, neden bir kapı değil.** v5-parti4'te üç kayıt ızgaranın
`sinir_tipi` çekilişinden saptı ve üçünde de sebep aynıydı: **tohum bir güvenlik
işareti taşıyordu, ızgara `yok` çekmişti.** T94'ün eksen çarpışması ailesinin
altıncı örneği. Doğal refleks bunu bir hücre yasağına çevirmek — denendi ve
ÖLÇÜMDE ÇÜRÜDÜ:

  `src/tohum_guvenlik.BEDENSEL_BELIRTI` havuzun **%7.3**'ünde (119/1634)
  ateşliyor ve isabetlerin çoğu *«dün maçta koşarken nefes alamadım, öksürdüm»*
  türünden **sıradan** kayıtlar. Bunlara yönlendirmeyi zorunlu kılmak §8b
  bütçesinin yarısını harcar — §8b'nin %33'ten %15'e indirilme kararının
  (T100 ölçümü) tam tersi.

➡️⭐ *Sapmayı üreten ayrım (akut belirti ↔ süregiden yakınma) n=2 vakadan
çıkarılamaz. Bir tasarım kuralı, onu doğuran gözlemden DAHA GENİŞ bir kanıta
ihtiyaç duyar; n büyümeden yazılan kural, ölçülmüş bir kotayı ölçülmemiş bir
sezgiyle değiştirir.* ⇒ Kural yazılmadı; sapmalar **birikiyor**.

⚠️ Bu defter bir KAPI DEĞİL: hiçbir şeyi elemez, çıkış kodu her zaman 0.

Kullanım: uv run python scripts/analiz/2026-09-17-izgara-sapma-defteri.py
"""
from __future__ import annotations
import glob, hashlib, json, re, sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]


def main() -> int:
    satir, dosya_sha = [], {}
    for f in sorted(glob.glob(str(KOK / "data/candidates/*.jsonl"))):
        p = Path(f)
        if "kumulatif" in p.stem:
            continue
        ham = p.read_bytes()
        n = 0
        for s in ham.decode("utf-8").splitlines():
            if not s.strip():
                continue
            r = json.loads(s)
            n += 1
            g = r.get("gen_meta") or {}
            if not (ham_ilan := g.get("izgara_sapmasi")):
                continue
            # ⛔ AYNI ALAN, İKİ BİÇİM: v4-parti2 `{eksen: gerekçe}` SÖZLÜĞÜ
            # yazmış, v5 düz DİZE. İlan alanının şeması hiç tanımlanmamış ve
            # bu, alanı okuyan ilk betiği (bu betik) çalışma anında kırdı.
            # ➡️ Bir alanı ZORUNLU kılmak onu OKUNABİLİR kılmıyor; şeması
            #    olmayan beyan, beyan edilmemişten yalnızca biraz daha iyidir.
            # ⇒ İkisi de okunuyor, biçim kayda geçiyor.
            ilan = (" · ".join(f"{k}: {v}" for k, v in ham_ilan.items())
                    if isinstance(ham_ilan, dict) else str(ham_ilan))
            satir.append({"parti": p.stem, "sira": g.get("parti_sira"),
                          "seed_id": g.get("seed_id"),
                          "ilan_bicimi": type(ham_ilan).__name__,
                          "eksenler": sorted(ham_ilan) if isinstance(ham_ilan, dict) else None,
                          "guvenlik_mi": bool(re.search(r"GÜVENLİK SAPMASI|§5a′", ilan)),
                          "sinir_tipi": g.get("sinir_tipi"),
                          "turn_ending": g.get("turn_ending"),
                          "ilan": ilan})
        dosya_sha[p.stem] = {"sha256_16": hashlib.sha256(ham).hexdigest()[:16], "kayit": n}

    # ⚠️ AYNI PARTİ ÜÇ KEZ SAYILABİLİR: blok dosyaları + birleşik dosya +
    # `.v2` düzeltmesi. `v4-parti2` ile `v4-parti2.v2` AYNI 60 kayıt; ikisini
    # de saymak sapma oranını iki katına çıkarıyordu. ⇒ Parti adı hem `.blokN`
    # hem `.vN` atılarak normalleştiriliyor; kayıt olarak EN SON revizyon
    # (en yüksek `.vN`, blok değil birleşik dosya) kazanıyor.
    def _ad(x: str) -> str:
        return re.sub(r"\.v\d+$", "", re.sub(r"\.blok\d\w*$", "", x))

    def _rev(x: str) -> int:
        m = re.search(r"\.v(\d+)$", x)
        return int(m.group(1)) if m else 1

    gorulen, tekil = set(), []
    for s in sorted(satir, key=lambda x: ("blok" in x["parti"], -_rev(x["parti"]))):
        anahtar = (_ad(s["parti"]), s["sira"], s["seed_id"])
        if anahtar in gorulen:
            continue
        gorulen.add(anahtar)
        tekil.append(s)

    parti_kayit = {}
    for k, v in sorted(dosya_sha.items(), key=lambda kv: _rev(kv[0])):
        if "blok" not in k:
            parti_kayit[_ad(k)] = v["kayit"]        # ⚠️ en yüksek revizyon kazanır
    per = Counter(_ad(s["parti"]) for s in tekil)
    ozet = {"tarih": "2026-09-17",
            "betik": "scripts/analiz/2026-09-17-izgara-sapma-defteri.py",
            "dosya_sha256": dosya_sha,
            "toplam_sapma": len(tekil),
            "guvenlik_sapmasi": sum(1 for s in tekil if s["guvenlik_mi"]),
            "ilan_bicimi": dict(Counter(s["ilan_bicimi"] for s in tekil)),
            "parti_basina": {k: {"sapma": v, "kayit": parti_kayit.get(k),
                                 "oran": round(100 * v / parti_kayit[k], 1)
                                 if parti_kayit.get(k) else None}
                             for k, v in sorted(per.items())},
            "sapma": tekil}
    cikti = KOK / "reports/analiz/2026-09-17-izgara-sapma-defteri.json"
    cikti.write_text(json.dumps(ozet, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"ilan edilmiş sapma: {len(tekil)} · güvenlik kaynaklı: {ozet['guvenlik_sapmasi']}")
    for k, v in ozet["parti_basina"].items():
        print(f"   {k:<20} {v['sapma']:>2} / {v['kayit']}  (%{v['oran']})" if v["oran"] is not None
              else f"   {k:<20} {v['sapma']:>2}")
    print(f"⛔ ilan alanının biçimi: {ozet['ilan_bicimi']} — ŞEMASIZ")
    print(f"⚠️ kural yazmak için n hâlâ küçük — bkz. betik başlığı")
    print(f"→ {cikti.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
