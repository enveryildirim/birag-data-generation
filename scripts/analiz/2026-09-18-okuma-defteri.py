#!/usr/bin/env python3
"""Okuma defteri — elle okunan bir yığının OKUNDUĞUNU kaydeder ve değişimi söyler.

⛔⛔ **Neden.** Yapısal atıf kapısının *«elle okunacak»* yığını her sürümde
insan okuması gerektiriyor ve `datasets/v0.0.12/CARD.md` bunu açıkça yazdı:
*«yığın her sürümde YENİDEN okunmalı ve bunu hatırlatan bir mekanizma yok»*.
Mekanizma yoksa iki kötü sonuç doğar: ya yığın hiç okunmaz (T155'te olan buydu —
27 iddia hiç okunmamıştı ve %26'sı yanlıştı), ya da her sürümde baştan okunur.

➡️⭐⭐ *Elle verilmiş bir hüküm, verildiği METNE bağlıdır. Metin değişmediyse hüküm
de geçerlidir — ama bunu SÖYLEYEN bir şey yoksa, hükmün hâlâ geçerli olduğunu
kimse bilemez ve okuma her sürümde sıfırdan tekrarlanır.*

⭐ Defter iki soruyu ayırır:
  · **değişmeyen** iddia → hüküm taşınır, yeniden okunmaz
  · **yeni/değişmiş** iddia → ⛔ okunmalı, ve defter onu açıkça listeler

⚠️ Defter bir HÜKÜM üretmez; yalnız hangi hükmün hâlâ geçerli olduğunu söyler.
Hüküm elle verilir (K30) ve gerekçesiyle birlikte defterde durur.

Kullanım: uv run python scripts/analiz/2026-09-18-okuma-defteri.py [datasets/v0.0.12]
"""
from __future__ import annotations

import hashlib
import importlib.util as iu
import io
import datetime
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
# ⛔ K126 rapor tarihini betiğin ADINDAN türetir ve TEK SEFERLİK ölçümler için bu
# doğrudur: ad, sayının alındığı günü sabitler. Ama bu betik YENİDEN KOŞULABİLİR
# (her sürüm için bir rapor) ⇒ addaki tarih artık ölçümün değil betiğin YAZILDIĞI
# günü gösterir. 2026-09-19'da koşulan bir rapor «Tarih: 2026-09-18» diyordu.
# ➡️ *Yeniden koşulabilir bir betikte ad kimliktir, tarih değil.* İkisi de yazılır.
KOSU = datetime.date.today().isoformat()
# ⭐ Defter KAPI-BAĞIMSIZ (2026-09-18, ikinci yazım). İlk hâli yalnız yapısal atıf
# yığınını tutuyordu ve mekân kapısının elle okunan iki bulgusu defterin dışında
# kaldı — yani «okundu» bilgisi yine kayboluyordu.
# ➡️ *Bir mekanizmayı tek kapıya yazmak, öteki kapılarda aynı eksiği bırakmaktır.*
KAPILAR = {
    "yapisal-atif": {
        "betik": "2026-09-17-yapisal-atif-kapisi.py",
        "rapor": "reports/analiz/2026-09-17-yapisal-atif-kapisi.json",
        "alan": "elle_okunacak",
        "kaynak": "T155 (2026-09-18) · 27 iddia elle okundu, 7'si yanlış çıktı ve düzeltildi",
        "hukum": "doğru — kullanıcının TEK cümlesi iki ögeyi taşıyor",
    },
    "mekan-atfi": {
        "betik": "2026-09-17-mekan-atfi-kapisi.py",
        "rapor": "reports/analiz/2026-09-17-mekan-atfi-kapisi.json",
        "alan": "bulgu",
        # ⭐ Yalnız ETİKETSİZ bulgular deftere girer: etiketliler zaten okuma
        # önceliği düşük diye işaretli (T170) ve hüküm gerektirmiyor.
        "suz": lambda b: not b.get("sinif"),
        "kaynak": "T170 (2026-09-18) · 11 bulgu elle okundu; 9 mecaz, 2 ılımlı çıkarım",
        "hukum": "kusur değil — mecaz ya da ılımlı çıkarım",
    },
}


def _kapi_yukle(ad: str):
    c = KAPILAR[ad]
    sp = iu.spec_from_file_location(ad, KOK / "scripts/analiz" / c["betik"])
    m = iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m, c

# ⭐ T155'te ELLE verilen hükümler — 27 iddia okundu, 7'si yanlıştı ve düzeltildi.
# Kalan 20 DOĞRU bulundu; hükümleri burada duruyor ve metin değişmedikçe geçerli.


def _imza(cumle: str) -> str:
    return hashlib.sha256(" ".join(cumle.split()).encode("utf-8")).hexdigest()[:16]


def _yigin(ad: str, tren: Path) -> dict[str, str]:
    m, c = _kapi_yukle(ad)
    with redirect_stdout(io.StringIO()):
        m.main([str(tren.relative_to(KOK))])
    rap = json.loads((KOK / c["rapor"]).read_text(encoding="utf-8"))
    suz = c.get("suz", lambda b: True)
    return {_imza(b["cumle"]): b["cumle"] for b in rap[c["alan"]] if suz(b)}


def _karsilastir(ad: str, simdi: dict[str, str]) -> tuple[list, list, dict]:
    c = KAPILAR[ad]
    yol = KOK / f"reports/analiz/okuma-defteri-{ad}.json"
    defter = json.loads(yol.read_text(encoding="utf-8")) if yol.exists() else {"hukum": {}}
    if not defter["hukum"]:
        defter = {"kaynak": c["kaynak"], "tarih": TARIH,
                  "hukum": {i: {"cumle": x, "hukum": c["hukum"]} for i, x in simdi.items()}}
        yol.write_text(json.dumps(defter, ensure_ascii=False, indent=2), encoding="utf-8")
    bilinen = set(defter["hukum"])
    return ([x for i, x in simdi.items() if i not in bilinen],
            [defter["hukum"][i]["cumle"] for i in bilinen - set(simdi)], defter)


def main(surum: str) -> int:
    tren = (Path(surum) if Path(surum).is_absolute() else KOK / surum) / "train.jsonl"
    hepsi = {}
    for ad in KAPILAR:
        simdi = _yigin(ad, tren)
        yeni, dusen, defter = _karsilastir(ad, simdi)
        hepsi[ad] = {"simdi": simdi, "yeni": yeni, "dusen": dusen, "defter": defter}
    # geriye uyum: rapor gövdesi ilk kapıyı ayrıntılı, ötekileri özet yazar
    simdi = hepsi["yapisal-atif"]["simdi"]
    yeni = hepsi["yapisal-atif"]["yeni"]
    dusen = hepsi["yapisal-atif"]["dusen"]
    defter = hepsi["yapisal-atif"]["defter"]

    sat = [f"# Okuma defteri — yapısal atıf yığını · `{Path(surum).name}`", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` (yazıldı {TARIH}) · "
           f"**koşu tarihi:** {KOSU}  ",
           f"**Defter:** `reports/analiz/okuma-defteri-*.json` · "
           f"hüküm kaynağı: {defter.get('kaynak')}", "",
           "⛔⛔ **Neden var.** Yığın her sürümde insan okuması gerektiriyor ve bunu hatırlatan",
           "bir mekanizma yoktu. Mekanizma yoksa ya yığın hiç okunmaz (T155'te olan buydu:",
           "27 iddia hiç okunmamıştı ve **%26'sı yanlıştı**) ya da her sürümde baştan okunur.", "",
           "➡️⭐⭐ *Elle verilmiş bir hüküm, verildiği METNE bağlıdır. Metin değişmediyse hüküm",
           "de geçerlidir — ama bunu SÖYLEYEN bir şey yoksa, hükmün hâlâ geçerli olduğunu",
           "kimse bilemez.*", "",
           "| | |", "|---|---:|",
           f"| yığındaki iddia | **{len(simdi)}** |",
           f"| ⭐ hükmü TAŞINAN (metin değişmemiş) | **{len(simdi)-len(yeni)}** |",
           f"| ⛔ **YENİ/DEĞİŞMİŞ — okunmalı** | **{len(yeni)}** |",
           f"| defterden düşen (artık yığında yok) | {len(dusen)} |", ""]
    if yeni:
        sat += ["## ⛔ Okunması gereken iddialar", ""]
        for c in yeni:
            sat.append(f"- {c[:150]}")
        sat.append("")
    else:
        sat += ["⭐ **Okunacak yeni iddia yok** — yığındaki her iddianın hükmü defterde ve",
                "metni değişmemiş. ⇒ Bu sürüm için elle okuma **yeniden gerekmiyor**.", ""]
    if dusen:
        sat += ["## Defterden düşenler (düzeltilmiş ya da elenmiş)", ""]
        for c in dusen[:10]:
            sat.append(f"- ~~{c[:140]}~~")
        sat.append("")
    sat += ["## Bütün kapılar", "", "| kapı | yığın | hükmü taşınan | ⛔ okunmalı |",
            "|---|---:|---:|---:|"]
    for ad, h in hepsi.items():
        sat.append(f"| `{ad}` | {len(h['simdi'])} | {len(h['simdi'])-len(h['yeni'])} | "
                   f"**{len(h['yeni'])}** |")
    toplam_yeni = sum(len(h["yeni"]) for h in hepsi.values())
    sat += ["", ("⭐ **Hiçbir kapıda okunacak yeni bulgu yok.**" if not toplam_yeni else
                 f"⛔ **{toplam_yeni} bulgu okunmalı.**"), "",
            "## ⛔ Bu defterin söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **Defter HÜKÜM üretmez** | yalnız hangi hükmün hâlâ geçerli olduğunu söyler; "
            "hüküm elle verilir (K30) |",
            "| ⛔ **İmza cümlenin kendisi** | aynı iddia başka bir kayda taşınırsa defter onu "
            "«bilinen» sayar; kayıt kimliği izlenmiyor |",
            "| ⚠️ **İki kapı kapsanıyor** | yapısal atıf ve mekân; alıntı ve zaman kapılarının "
            "bulguları şu an **sıfır** olduğu için deftere gerek yok, ama sıfırdan çıkarlarsa "
            "defter onları kapsamıyor |",
            "| ⚠️ Mekânda yalnız **etiketsiz** bulgular deftere giriyor | etiketliler okuma "
            "önceliği düşük diye işaretli (T170) ve hüküm gerektirmiyor |", ""]
    (KOK / f"reports/analiz/{TARIH}-okuma-defteri.md").write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[4:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "datasets/v0.0.12"))
