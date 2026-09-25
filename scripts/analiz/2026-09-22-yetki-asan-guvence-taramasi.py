#!/usr/bin/env python3
"""Asistan cevaplarında YETKİ AŞAN güvence arar — özellikle gizlilik vaadi.

⭐ **Neden var:** `gd-033` (2026-09-22) elendi, ama eleme bir kapı değildir.
K66'nın kuralı: *bir sınır yazıldığında aynı commit'te (a) onu uygulayan kod
ya da (b) onu ÖLÇEN rapor satırı da yazılır.* ⛔ (a) yazılamaz — modelin
mahremiyet konusunda ne diyebileceği **uzman kalemidir** (brifing §8.4,
2. soru açık). ⇒ Bu betik (b)'dir: kuralı koymaz, **sayar**.

⛔⛔ **Sezicinin kendi kusuru ölçülerek yazıldı.** İlk elden taramada desen
`kimseye söylemem` idi ve **`kimseye söylememişsin`** içinde eşleşti — biri
1. tekil bir VAAT, öteki kullanıcının sözünü YANSITMA; 14 eşleşmenin 13'ü
yanlış pozitifti (T22 serisine 17. satır olarak girdi). ⇒ Bu sürümde:
  · her kol **sözcük sınırıyla** (`\\b`) kapatıldı — `söylemem\\b`
    `söylememişsin`'e artık düşmüyor,
  · yalnız **1. tekil / kişisiz gelecek** kipleri aranıyor,
  · ⭐ betik kendi yanlış pozitif oranını **raporluyor**: eşleşen her cümle
    çıktıya yazılır ki okunabilsin. **Sayı tek başına hüküm değildir.**

⛔ Bu betik hiçbir kaydı değiştirmez ve hiçbir kaydı elemez.

Çıktı: reports/analiz/2026-09-22-yetki-asan-guvence-taramasi.md
"""
from __future__ import annotations

import glob
import json
import re
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-yetki-asan-guvence-taramasi.md"
TUREV = re.compile(r"\.(blok\d+[a-z]*|v\d+|arinmis|claude)\.")

# ⭐ Her kol 1. tekil ya da kişisiz GELECEK/GENİŞ zaman; 2. tekil geçmiş
#   (`-mişsin`, `-madın`) `\b` ile dışarıda kalır.
VAAT = {
    "gizlilik": re.compile(
        r"dışarı çıkma(z\b|yacak|yacağ)|aramızda kal(ır\b|acak|ıyor\b)|"
        r"kimseye (söylemem\b|söylemeyeceğim\b|anlatmam\b|anlatmayacağım\b|"
        r"iletmem\b|paylaşmam\b|paylaşmayacağım\b)|"
        r"kimse (görmez\b|görmeyecek|okumaz\b|okumayacak)|"
        r"gizli kal(ır\b|acak)|sakla(rım\b|yacağım\b)", re.I),
    "kalıcılık": re.compile(
        r"(unutmam\b|unutmayacağım\b|hatırlarım\b|hatırlayacağım\b|"
        r"kaydetmem\b|kaydetmeyeceğim\b|silerim\b|sileceğim\b)", re.I),
    "erişim": re.compile(
        r"(seni takip ederim\b|seni takip edeceğim\b|haber veririm\b|"
        r"haber vereceğim\b|arar(ım|ız)\b|ulaşırım\b|ulaşacağım\b)", re.I),
}


def main() -> int:
    bulgu, n_kayit, n_dosya = [], 0, 0
    for f in sorted(glob.glob(str(KOK / "data/candidates/*.jsonl"))):
        if TUREV.search(f):
            continue
        n_dosya += 1
        for l in open(f):
            r = json.loads(l)
            if "messages" not in r:      # ⛔ plan/eleme satırları konuşma değil
                continue
            n_kayit += 1
            for m in r["messages"]:
                if m["role"] != "assistant":
                    continue
                t = m.get("content") or ""
                for tur, dsn in VAAT.items():
                    mm = dsn.search(t)
                    if mm:
                        i = t.rfind(".", 0, mm.start()) + 1
                        j = t.find(".", mm.end())
                        bulgu.append((Path(f).stem, r["id"][:10], tur,
                                      t[i:j + 1 if j > 0 else None].strip()))

    sat = ["# Yetki aşan güvence taraması", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Girdi:** `data/candidates/` — {n_dosya} dosya, {n_kayit} kayıt  ",
           f"**Eşleşme:** {len(bulgu)}  ", "",
           "⭐ **Bu betik bir KURAL koymaz, SAYAR.** `gd-033` elendi ama eleme "
           "bir kapı değildir; modelin mahremiyet konusunda ne diyebileceği "
           "**uzman kalemidir** (`docs/uzman-brifingi.md` §8.4, 2. soru "
           "açık). K66: bir sınır yazıldığında ya onu uygulayan kod ya da onu "
           "ölçen rapor satırı yazılır — bu, ikincisidir.", "",
           "⛔⛔ **Sayı tek başına hüküm değildir.** Eşleşen her cümle "
           "aşağıda yazılı; **okunmadan** sayılmaz. Bu betiğin ilk sürümü "
           "`kimseye söylemem` kolunu `kimseye söylememişsin` içinde eşleştirmiş "
           "ve 14 eşleşmenin 13'ü yanlış pozitif çıkmıştı (T22 serisi, 17. "
           "satır) ⇒ kollar `\\b` ile kapatıldı ve yalnız 1. tekil / kişisiz "
           "gelecek kipleri arıyor.", ""]
    if bulgu:
        sat += ["## Eşleşmeler — hepsi OKUNACAK", "",
                "| dosya | kayıt | tür | cümle |", "|---|---|---|---|"]
        for d, i, tur, c in bulgu:
            sat.append(f"| `{d}` | `{i}` | {tur} | {c[:180]} |")
    else:
        sat += ["⭐ **Eşleşme yok.**", "",
                "⛔ Bu *«korpusta yetki aşan güvence yok»* demek DEĞİLDİR: "
                "sezici üç kalıp ailesi tanıyor (gizlilik · kalıcılık · "
                "erişim) ve yalnız tanıdığı dizgeleri bulur. Aynı vaat başka "
                "sözcüklerle kurulursa **görünmez**."]
    sat += ["", "## ⛔ Bu taramanın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **ALT SINIR** | sezici dizge tabanlı ve Türkçe serbest "
            "metinde koşuyor — T22 serisinin bütünü bu biçimin yanıldığını "
            "gösteriyor ⇒ bulunmayan, olmadığı anlamına gelmez |",
            "| ⛔ **`gd-033` bu taramada ÇIKMAZ** | kayıt elendi ama "
            "`data/candidates/v6-parti8.jsonl` içinde duruyor (Kural 7) ⇒ "
            "eşleşmesi beklenir ve bu bir HATA değil, elemenin `build.py` "
            "karantinasında olduğunun kanıtıdır |",
            "| ⚠️ **«Yetki aşan» tanımı YAZILI DEĞİL** | üç kalıp ailesi benim "
            "önerim; hangi güvencenin yetki aşımı sayılacağı uzman kararıdır |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print(f"{n_kayit} kayıt tarandı · eşleşme {len(bulgu)}")
    for d, i, tur, c in bulgu:
        print(f"  {d} {i} [{tur}] {c[:120]}")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
