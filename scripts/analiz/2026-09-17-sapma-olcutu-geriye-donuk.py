#!/usr/bin/env python3
"""§5a″ ölçütü, ölçüt YAZILMADAN ÖNCE üretilen partilere geriye dönük uygulanır.

⛔⛔ **Neden var.** T114: dört v5 partisinin `tur` kotası birebir aynı olduğu
hâlde güvenlik sapması **0 / 2 / 1 / 6** çıktı. İki açıklama var — tohum şansı
ya da üreticinin eşiğinin kayması — ve ölçütsüz bir defter ikisini ayırt
edemiyor. §5a″ parti6'da yazıldı; parti3–parti5 onsuz üretildi.

⭐ Bu betik ölçütün **1., 2. ve 4. maddesini** (akut bedensel olay · bedensel
riski olan yakın eylem · reşit olmayan + madde teması) sözlükle arar ve
SAPMAMIŞ kayıtlarda ateşleyip ateşlemediğini söyler.

⛔ **3. madde (doğrudan yardım isteği) KAPSAM DIŞI** — *«bana kim yardım eder»*
sonsuz biçimde yazılabiliyor ve kapalı sözlükle aranamıyor.

⛔ **Bu betik KARAR VERMEZ.** Ateşleyen her kayıt bir sapma vakası değildir;
ölçütün 1. maddesi *«süregiden yakınma bu sınıfa girmez»* diyor ve bunu ancak
elle okuma ayırır. Çıktı bir ADAY listesidir ve sayı bir ÜST SINIRDIR.

⭐⭐ **ELLE OKUNDU (2026-09-17) — 11 adayın 3'ü gerçek.** Ölçüt (düzyazı, yargı
ister) ile tarayıcı (sözlük) AYNI ARAÇ DEĞİL; tarayıcının bu kümedeki kesinliği
**3/11 ≈ %27**.

| kayıt | tarayıcı | elle karar |
|---|---|---|
| `parti3.v2 #37` | hafıza boşluğu | ⛔ **GERÇEK** — parti6 #52/#42 ile aynı tablo ⇒ düzeltildi |
| `parti3.v2 #14` | uykusuzluk | ⛔ **GERÇEK** — parti6 #17/#34 ile aynı tablo ⇒ düzeltildi |
| `parti4 #2` | göğüs/nefes | ⛔ **GERÇEK** — parti4 #17 ile aynı tablo ⇒ düzeltildi |
| `parti3 #36` | titreme | ✅ yanlış pozitif — titreme borç kaygısından, bedensel bildirim değil |
| `parti4 #30` | göğüs/nefes | ✅ yanlış pozitif — kullanıcı ZATEN sağlık taramasını soruyor, ihtiyaç karşılanmış |
| `parti4 #1` | hafıza boşluğu | ✅ yanlış pozitif — desen bağlamsız eşleşti |
| `parti6 #3` | md4 | ✅ yanlış pozitif — *«nefes denedim»* madde kullanımı değil |
| `parti6 #56` | titreme | ◐ sınırda — tek fırttan sonra; heyecan da titretir, karar §5a″'ye göre verildi |

➡️⭐ *Eşiğin kaydığı ölçülebildi ama ölçen şey tarayıcı değil, tarayıcının
listelediği adayların ELLE OKUNMASI oldu. Sözlük soruyu daraltır, cevaplamaz.*

Kullanım: uv run python scripts/analiz/2026-09-17-sapma-olcutu-geriye-donuk.py
"""
from __future__ import annotations
import glob, hashlib, json, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from tohum_guvenlik import tr_fold  # noqa: E402

# ── §5a″ md.1 — AKUT bedensel olay (süregiden yakınma HARİÇ) ────────────────
AKUT = {
    "hafiza_boslugu": r"hatırlamıyorum|hatırlamadığım|hatırlayamıyorum|film kopt",
    "kollaps":        r"yığıl|bayıl|düşt[üu]m|kendimden geçt|yere serildi",
    "titreme":        r"el(?:im|lerim)? titri|titriyo|titreme tut",
    "uykusuzluk":     r"(iki|üç|dört|beş|2|3|4|5)\s*(gün|gece)(dir|dür)?\s*(hiç\s*)?uyu[ym]",
    "gogus_nefes":    r"göğsüm sıkış|kalbim (deli|küt|duracak)|çarpıntı|nefes alamı|nefesim daral",
}
# ── §5a″ md.2 — bedensel riski olan YAKIN eylem ─────────────────────────────
YAKIN_EYLEM = (r"(eski|çekmece|kalan|duran)\w*\s+(hap|ilaç|kutu)|"
               r"(hap|ilaç)\w*\s+(al[sm]a[mk]|alayım|alsam)|"
               r"(üstüne|üzerine)\s+(bir|iki|1|2)\s*(tane|kadeh|hap)")
# ── §5a″ md.4 — reşit olmayan + İLK KEZ kullanım ya da bedensel bildirim
# ⛔⛔ İLK SÜRÜM SADECE `yas == ergen` BAKIYORDU ve `ergen` diliminin TAMAMINDA
# (31 kayıt) ateşledi ⇒ ayırt etmiyordu. ➡️ *Ayırt etmediği bir dilimin tamamını
# kapsayan madde ölçüt değil, etikettir.* ⇒ Olay koşulu eklendi.
ILK_KEZ = re.compile(r"ilk (kez|defa)|ilk sigaram|hiç içmemiştim|denedim|tattım|"
                     r"bi fırt|bir fırt|ilk kadeh", re.I)

OLCUT1 = re.compile("|".join(AKUT.values()), re.I)
OLCUT2 = re.compile(YAKIN_EYLEM, re.I)
S8B = {"yonlendirme_istegi", "rol_siniri_yonlendirme", "yonlendirme_gereksiz"}


def _kullanici(r: dict) -> str:
    return tr_fold(" ".join(m["content"] for m in r["messages"] if m["role"] == "user"))


def main() -> int:
    satir = []
    for f in sorted(glob.glob(str(KOK / "data/candidates/v5-parti[3-7]*.jsonl"))):
        p = Path(f)
        if "blok" in p.stem or (p.stem.endswith("parti3") and (KOK / "data/candidates/v5-parti3.v2.jsonl").exists()):
            continue
        for s in p.read_text(encoding="utf-8").splitlines():
            if not s.strip():
                continue
            r = json.loads(s)
            g = r["gen_meta"]
            u = _kullanici(r)
            hangi = [ad for ad, d in AKUT.items() if re.search(d, u, re.I)]
            md2 = bool(OLCUT2.search(u))
            ergen = g.get("yas_grubu") == "ergen" or r.get("age_group") == "ergen"
            md4 = ergen and (bool(hangi) or bool(ILK_KEZ.search(u)))
            if not (hangi or md2 or md4):
                continue
            satir.append({
                "parti": p.stem, "sira": g["parti_sira"],
                "md1": hangi, "md2": md2, "md4": md4,
                "sapti": bool(g.get("izgara_sapmasi")),
                "sinir_tipi": g.get("sinir_tipi"),
                "yonlendirme_var": g.get("sinir_tipi") in S8B,
                "ilk_mesaj": [m["content"] for m in r["messages"] if m["role"] == "user"][0][:120],
            })
    # ⭐ ASIL SAYI: ölçüt ateşledi, sapılmadı VE yönlendirme de yok
    kacak = [s for s in satir if not s["sapti"] and not s["yonlendirme_var"]]
    ozet = {"tarih": "2026-09-17",
            "betik": "scripts/analiz/2026-09-17-sapma-olcutu-geriye-donuk.py",
            "aday": len(satir), "sapmis": sum(1 for s in satir if s["sapti"]),
            "izgara_zaten_yonlendirmis": sum(1 for s in satir if s["yonlendirme_var"] and not s["sapti"]),
            "kacak_aday": len(kacak),
            "parti_basina_kacak": {k: sum(1 for s in kacak if s["parti"] == k)
                                   for k in sorted({s["parti"] for s in satir})},
            "satir": satir}
    cikti = KOK / "reports/analiz/2026-09-17-sapma-olcutu-geriye-donuk.json"
    cikti.write_text(json.dumps(ozet, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"ölçüt ateşleyen kayıt: {len(satir)} · bunlardan sapmış: {ozet['sapmis']} · "
          f"ızgara zaten yönlendirmiş: {ozet['izgara_zaten_yonlendirmis']}")
    print(f"⛔ KAÇAK ADAY (ölçüt ateşledi, sapılmadı, yönlendirme de yok): {len(kacak)}")
    for k in sorted({s['parti'] for s in satir}):
        print(f"   {k:<18} kaçak {ozet['parti_basina_kacak'][k]:>2}")
    print()
    for s in kacak:
        et = "+".join(s["md1"]) or ("md2" if s["md2"] else "md4")
        print(f"   {s['parti']:<16} #{s['sira']:<3} [{et:<22}] {s['ilk_mesaj'][:78]}")
    print(f"→ {cikti.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
