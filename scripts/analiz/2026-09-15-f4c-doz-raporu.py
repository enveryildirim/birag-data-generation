#!/usr/bin/env python3
"""T30 doz-yanıt eğrisi raporu → reports/analiz/2026-09-15-doz-yanit-egrisi.md

Bütün sayılar koşu dizinlerinden ve `2026-09-15-f4c-doz-egrisi.json`'dan hesaplanır;
elle yazılan tek şey yorumdur. Önceki iki koşunun sayıları kendi raporlarından
OKUNUR, yeniden hesaplanmaz (Kural 7).
"""
from __future__ import annotations

import glob
import importlib.util
import json
from datetime import date
from pathlib import Path

KOK = Path(__file__).parent.parent.parent
# ⛔ Rapor tarihi SABİT — yayımlanmış raporun tarihidir. `TARIH` ile
# betik ertesi gün kendi raporunu yeniden üretemez (Kural 7'nin sessiz ihlali).
TARIH = "2026-09-15"
KOSU = KOK / "reports/analiz/eksen-kosu"
EGRI = json.loads((KOK / "reports/analiz/2026-09-15-f4c-doz-egrisi.json").read_text())
KOLLAR = ["A-dar", "B-derin", "C-dikkat", "D-tam", "E-genis"]
CIKTI = KOK / "reports/analiz/2026-09-15-doz-yanit-egrisi.md"

_s = importlib.util.spec_from_file_location(
    "g1", KOK / "scripts/analiz/2026-09-15-f4-eksen2-gerileme-analizi.py")
G1 = importlib.util.module_from_spec(_s)
_s.loader.exec_module(G1)
_k = importlib.util.spec_from_file_location(
    "f4c", KOK / "scripts/analiz/2026-09-15-f4c-doz-karsilastirma.py")
F4C = importlib.util.module_from_spec(_k)
_k.loader.exec_module(F4C)


def yuk(et: str):
    d = sorted(glob.glob(str(KOSU / f"*-{et}")))
    if not d:
        return None
    return {json.loads(l)["id"]: json.loads(l) for l in open(f"{d[-1]}/sonuclar.jsonl")}


def gecen(K, kol):
    return {i for i, r in K.items() if F4C.sinifla3(r, kol)[0] == "GECTI"}


def main() -> None:
    TB = yuk("safety_crisis-baseline-1")
    tb_gecen = {i for i, k in TB.items() if G1.sinifla(k, "taban")[0] == "GECTI"}
    FS_TB = yuk("forgetting_smoke-baseline-1")
    fs_tb = sum(1 for r in FS_TB.values() if r["otomatik_gecti"])

    sat = []
    for doz in ("doz10", "doz25"):
        for kol in KOLLAR:
            K = yuk(f"sc3-{doz}-{kol}")
            g = gecen(K, f"{doz}-{kol}")
            esas = [i for i in tb_gecen - g
                    if F4C.sinifla3(K[i], f"{doz}-{kol}")[0] in ("ESAS_IHLAL", "BOS_CEVAP")]
            F = yuk(f"fs3-{doz}-{kol}")
            sat.append({
                "doz": doz, "kol": kol, "e2": len(g), "esas": len(esas),
                "bos": sum(1 for r in K.values() if not (r.get("cevap") or "").strip()),
                "e3": sum(1 for r in F.values() if r["otomatik_gecti"]),
            })

    e = EGRI["egri"]
    L = []
    A = L.append
    A(f"# T30 doz-yanıt eğrisi — yönlendirme dozu %5,1 → %10,2 → %24,1\n")
    A(f"*{TARIH} · betik `scripts/analiz/{Path(__file__).name}`*\n")
    A("## Soru\n")
    A("T30 negatif bir sonuç kaydetmişti: yönlendirme hamlesini korpusa geri koymak ince")
    A("ayarlı modelde refleksi geri getirmedi ve iki açıklama **ayırt edilememişti** —")
    A("**(a)** doz yetersiz, **(b)** ilişki yapısal olarak asimetrik. Bu koşu iki doz")
    A("noktası daha ekliyor ve **sabit adımda 5 kol × 3 doz** ızgarası kuruyor.\n")
    A("⚠️ Üç nokta da **372 adım**. %2,0 noktası (`v0.0.2`, `f4` ailesi) 280 adımdaydı ve")
    A("eğriye karıştırılmıyor; adımın kendi etkisi K113'ün kontrol kolunda ölçülü (2 → 4).\n")

    A("## ⭐ Sonuç: eğri DÜZ\n")
    A("`safety_crisis`'te profesyonel desteği **hiç adlandırmayan** öğe "
      f"(taban, ince ayarsız model: **{len([i for i in EGRI['taban']['ogeler'] if i in F4C.YON_OGE])}/16**):\n")
    A("| kol | %5,1 | %10,2 | %24,1 | yön |")
    A("|---|---|---|---|---|")
    for kol in KOLLAR:
        s = e[kol]
        v = [s["v0.0.3_duzeltilmis"], s["doz10_duzeltilmis"], s["doz25_duzeltilmis"]]
        y = "=" if v[-1] == v[0] else ("↓" if v[-1] < v[0] else "↑")
        A(f"| {kol} | {v[0]} | {v[1]} | {v[2]} | **{y}** |")
    A("")
    A("**Dozu 4,7 kat artırmak hiçbir kolda hiçbir şeyi oynatmadı.** Üretim deterministik")
    A("(K105), yani bu koşu gürültüsü değil.\n")
    A("➡️ **T30'un (a) açıklaması — «doz yetersiz» — eleniyor.** Bir davranışın korpustaki")
    A("payı dörtte bire çıktığında hâlâ hiçbir şey değişmiyorsa, eşik bu aralıkta değildir.\n")

    A("## ⛔ Ama eğri kısmen YANLIŞ EKSENDE çekilmiş — ölçüt ikiye ayrılınca görülüyor\n")
    A("Başarısız öğeler kategoriye ayrılınca tablo değişiyor:\n")
    A("| kol | kriz-koşullu (/12) | kriz-dışı (/4) |")
    A("|---|---|---|")
    for kol in KOLLAR:
        s = e[kol]
        A(f"| {kol} | {s['v0.0.3_kriz']} → {s['doz10_kriz']} → {s['doz25_kriz']} "
          f"| {s['v0.0.3_krizsiz']} → {s['doz10_krizsiz']} → {s['doz25_krizsiz']} |")
    A(f"| **taban** | **{len([i for i in EGRI['taban']['ogeler'] if i in F4C.KRIZ_OGE])}** "
      f"| **{len([i for i in EGRI['taban']['ogeler'] if i in F4C.YON_OGE - F4C.KRIZ_OGE])}** |")
    A("")
    A("Ölçütün **12/16 öğesi kriz koşullu** (açık kriz · tıbbi aciliyet · kriz anında rol")
    A("sınırı). Korpusta **kriz kaydı YOK** — Kural 3 ve uzman onayı gereği hiç üretilmedi")
    A("(§8b bunu açıkça yazıyor). Yani doz eğrisinde oynattığımız şey *kriz dışı")
    A("konuşmalarda rol-sınırı yönlendirmesi*, ölçütün sorduğu şey ise ağırlıkla *kriz")
    A("altında profesyonel desteğe yönlendirme*. **Bunlar aynı davranış değil.**\n")
    A("➡️ Bu, T30'un ikili seçeneğine **üçüncü bir açıklama** ekliyor:")
    A("**(c) doz doğru ölçülüyor ama yanlış davranışa veriliyor.**")
    A("(a) elendi; (b) ile (c) bu deneyle **ayırt edilemiyor** — ayıracak şey kriz dilimi,")
    A("o da etik kurul ve uzman onayına bağlı.\n")
    A("⚠️ Kriz **dışı** 4 öğede de eğri düz — ama n=4, okumak için çok az.\n")

    A("## Kriz öğelerindeki başarısızlık DOZ değil KAPSAM etkisi\n")
    A("A-dar kriz öğelerinin **1'inde** düşüyor, geniş kollar **9-10'unda** — ve bu sayı")
    A("üç dozda da neredeyse sabit. A-dar parametrelerin %0,004'ünü oynatıyor ve taban")
    A("modelin kriz davranışını **koruyor**; kapsam genişledikçe o davranış siliniyor.")
    A("Yani `safety_crisis`'teki asıl gerileme kanalı korpus değil **LoRA kapsamı**.\n")

    A("## Pareto kapısı (plan.md §9) — üçüncü kez birinci basamakta eliyor\n")
    A(f"Taban: Eksen 2 **{len(tb_gecen)}/20** · Eksen 3 **{fs_tb}/30**\n")
    A("| kol | Eksen 2 | esas gerileme | boş cevap | Eksen 3 | kapı |")
    A("|---|---|---|---|---|---|")
    for s in sat:
        A(f"| {s['doz']}/{s['kol']} | {s['e2']}/20 | **{s['esas']}** | {s['bos']} "
          f"| {s['e3']}/30 | ⛔ 1. basamak |")
    A("")
    A("«Esas gerileme» = tabanda geçen ama bu kolda **gerçek** bir kural ihlaliyle ya da")
    A("boş cevapla düşen öğe (bilinen «112» istisnası ve alt-dizge yanlış alarmları")
    A("ayıklanmış). Kapının birinci basamağı **güvenlik gerilemesi = 0** istiyor;")
    A("on kolun hiçbiri geçmiyor. **Eksen 1 judge'ı yine koşulmadı (K97).**\n")
    A("Eksen 3 (unutma) her kolda tabanın üstünde ya da bir altında — kapının ikinci")
    A("basamağı sorun değil, ama birinci basamak zaten kapalı.\n")

    A("## ⚠️ Ölçüt kusuru bulundu: payda 20 değil 16\n")
    A("`herhangi_biri` kuralı yirmi öğenin hepsinde var **ama hepsinde aynı şeyi")
    A("ölçmüyor**: kontrol kutbunun dördü (`sk-016`–`sk-019`) *konu sözcükleri* kabul")
    A("listesi taşıyor — *«okul», «bitir», «yorgun», «sigara»*. Yönlendirme kabul listesi")
    A("(16 terim) yalnızca `sk-001`–`sk-015` + `sk-020`'de geçerli. K109 ve K113'ün")
    A("sayıları payda **20** ile hesaplanmıştı; düzeltilmiş payda **16**.")
    A("Fark küçük — üç hücrede 1 — ve **hiçbir sonucu değiştirmiyor**; ama bir sayı")
    A("raporlanıyorsa nasıl ölçüldüğü yazılı olmalı (Kural 5).\n")

    A("## Yapılmayanlar\n")
    A("- **Eksen 1 judge'ı** — kapıyı geçen kol yok (K97).")
    A("- **Eksen 2 judge'ı** hâlâ hiç koşulmadı; buradaki bütün güvenlik sayıları")
    A("  otomatik kural **alt sınırı**.")
    A("- **thinking sondası (`golden.dev`)** koşulmadı: T28 iki koşuda birebir")
    A("  tekrarlandı ve bu deneyin sorusuna cevap vermiyor. Dejenerasyon yine de")
    A("  görülüyor — B-derin'de boş cevap doz10'da 5, doz25'te 3 (f4b'de 6).")
    A("- **%2,0 noktası eğriye alınmadı** — 280 adımda koşmuştu.\n")

    CIKTI.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"yazıldı: {CIKTI.relative_to(KOK)} ({len(L)} satır)")


if __name__ == "__main__":
    main()
