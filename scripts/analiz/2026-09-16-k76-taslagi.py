#!/usr/bin/env python3
"""K76 yazılamıyor — ama YAZILABİLİR HÂLE getirilebilir (T89).

`K76` `PROJECT_MEMORY.md`'de **yok**; buna karşılık `T23`, `K78`, `K112` ve
`K138` ona atıf veriyor ve artefaktı duruyor: `data/guvenlik-karantinasi.jsonl`.
⛔ **İçeriği uydurulamaz** — hangi kaydın neden silinmeyip karantinaya alındığı
bir **klinik güvenlik kararıdır** (Kural 3) ve onu yazmak bir yetki sorunu
değil, **yetkinlik ve kurum** sorunudur. Uydurulmuş bir gerekçe tezde gerçek bir
karar gibi okunur; bu, sahte kayıttır.

⭐ **Ama kararın DOĞRULANABİLİR kısmı burada üretilebilir:** kaç kayıt, hangi
işaretlerle, hangi partiden, hangi tarihte, kim atıf veriyor, tezin hangi
bölümü buna dayanıyor. ⇒ Yürütücünün yazması gereken şey **yalnızca hüküm**
olur; malzemeyi aramak zorunda kalmaz.

⚠️ **Kayıt METİNLERİ bu taslağa girmiyor** — yalnızca meta. Klinik içerik
karantinada kalır (K18/Kural 3).

Girdi : data/guvenlik-karantinasi.jsonl · PROJECT_MEMORY.md · docs/tez/katki-defteri.md
Çıktı : docs/karar-taslaklari/K76-guvenlik-karantinasi.md
Kullanım: uv run python scripts/analiz/2026-09-16-k76-taslagi.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
CIKTI = KOK / "docs/karar-taslaklari/K76-guvenlik-karantinasi.md"
KARANTINA = KOK / "data/guvenlik-karantinasi.jsonl"
HAFIZA = KOK / "PROJECT_MEMORY.md"
DEFTER = KOK / "docs/tez/katki-defteri.md"

IS_BAS = "<!-- TÜRETİLEN:kanit başlangıç — elle düzenleme; `scripts/analiz/%s` üretir -->"
IS_SON = "<!-- TÜRETİLEN:kanit bitiş -->"


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def main() -> int:
    if not KARANTINA.exists():
        print("⛔ karantina dosyası yok")
        return 1
    kayitlar = [json.loads(l) for l in KARANTINA.read_text(encoding="utf-8").split("\n") if l.strip()]
    atif = []
    for ad, yol in (("PROJECT_MEMORY.md", HAFIZA), ("docs/tez/katki-defteri.md", DEFTER)):
        for satir in yol.read_text(encoding="utf-8").split("\n"):
            if re.search(r"\bK76\b", satir):
                m = re.match(r"^\|\s*([TK]\d+)\s*\|", satir)
                atif.append((ad, m.group(1) if m else "—"))

    K: list[str] = []
    K += [IS_BAS % Path(__file__).name, "",
          f"**Üretildi:** `scripts/analiz/{Path(__file__).name}` · {TARIH}  ",
          f"**Artefakt:** `data/guvenlik-karantinasi.jsonl` SHA256 `{sha(KARANTINA)}` — "
          f"**{len(kayitlar)}** kayıt", "",
          "### Kayıtlar — yalnızca META (klinik metin karantinada kalır)", "",
          "| # | korpus | parti | tarih | durum | öncelik | eşdurum sayısı |",
          "|---:|---|---:|---|---|---|---:|"]
    for i, r in enumerate(kayitlar, 1):
        K.append(f"| {i} | `{r.get('korpus')}` | {r.get('parti_sira')} | {r.get('tarih')} | "
                 f"`{r.get('durum')}` | {r.get('oncelik')} | {len(r.get('esdurumlar') or [])} |")
    d = collections.Counter(str(r.get("durum")) for r in kayitlar)
    o = collections.Counter(str(r.get("oncelik")) for r in kayitlar)
    es = collections.Counter(e for r in kayitlar for e in (r.get("esdurumlar") or []))
    K += ["", "### Dağılımlar", "", "| | |", "|---|---|",
          f"| durum | {', '.join(f'`{k}` ×{v}' for k, v in sorted(d.items()))} |",
          f"| öncelik | {', '.join(f'`{k}` ×{v}' for k, v in sorted(o.items()))} |",
          f"| en sık eşdurum | {', '.join(f'{k} ×{v}' for k, v in es.most_common(6))} |", "",
          "### K76'ya atıf verenler", "", "| dosya | satır |", "|---|---|"]
    K += [f"| `{a}` | `{b}` |" for a, b in atif] or ["| — | — |"]
    K += ["",
          f"⛔ **{len(atif)} yerden atıf alıyor, kendisi yok.** Numaralandırma K75→K77 "
          "atlıyor.", "", IS_SON]

    metin = f"""# K76 — güvenlik karantinası kararı · **TASLAK, HÜKÜM YAZILMADI**

> ⛔ **Bu dosya bir karar DEĞİLDİR.** Kararın doğrulanabilir malzemesi aşağıda
> türetilmiştir; **hüküm bölümü boştur ve yürütücü tarafından doldurulur.**
>
> ⚠️ Hangi kaydın neden silinmeyip karantinaya alındığı bir **klinik güvenlik
> kararıdır** (Kural 3). Bunu yazmak bir izin sorunu değil, **yetkinlik ve kurum**
> sorunudur: uydurulmuş bir gerekçe tezde gerçek bir karar gibi okunur.

## 1. Kararın doğrulanabilir kısmı *(türetilir — elle düzenlenmez)*

{IS_BAS % Path(__file__).name}
{IS_SON}

## 2. ⛔ HÜKÜM — yürütücü doldurur

Aşağıdaki üç soru `PROJECT_MEMORY.md`'ye `K76` satırı olarak yazılacak metni
belirler. ⚠️ Boş bırakılan her satır, tezin §11 (Etik) ve §9 (Hata analizi)
bölümlerinde **eksik** kalır.

**(a) Neden silinmedi?** Kayıtlar `klinik_guvenlik_ihlali` aldı ve eğitim setine
girmedi; ama dosyadan da çıkarılmadı. Gerekçe:

> _(yazılacak)_

**(b) Karantinadan çıkış ölçütü nedir?** `durum: uzman_karari_bekliyor` — hangi
uzman, hangi ölçütle, hangi sonuçlar mümkün (`uzman_onayladi` / kalıcı ret /
yeniden yazım)?

> _(yazılacak)_

**(c) Tezde nasıl raporlanacak?** Bu 8 kayıt bir **veri kaybı** mı, bir
**güvenlik kapısının çalıştığının kanıtı** mı, yoksa ikisi birden mi?

> _(yazılacak)_

## 3. Bu taslağın söylemedikleri

| | |
|---|---|
| ⛔ **Hüküm** | yazılmadı ve bu betikle yazılamaz (Kural 3) |
| ⛔ **Klinik metinler** | taslağa girmiyor; yalnızca meta türetildi (K18) |
| ⚠️ Atıf taraması | `\\bK76\\b` dizgesi; düzyazı içinde başka biçimde anılmışsa görünmez |
| ⚠️ Bu dosya `docs/karar-taslaklari/` altında | ⛔ karar kaydı **değil**; `PROJECT_MEMORY.md` tek karar kaydıdır (Kural 2) |
"""
    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    if CIKTI.exists():
        eski = CIKTI.read_text(encoding="utf-8")
        bas, son = IS_BAS % Path(__file__).name, IS_SON
        if bas in eski and son in eski:
            i, j = eski.index(bas) + len(bas), eski.index(son)
            metin = eski[:i] + "\n" + "\n".join(K[1:-1]) + "\n" + eski[j:]
        else:
            metin = metin.replace(f"{IS_BAS % Path(__file__).name}\n{IS_SON}", "\n".join(K))
    else:
        metin = metin.replace(f"{IS_BAS % Path(__file__).name}\n{IS_SON}", "\n".join(K))
    CIKTI.write_text(metin, encoding="utf-8")
    print(f"✅ {CIKTI.relative_to(KOK)}")
    print(f"   karantina kaydı {len(kayitlar)} · K76 atfı {len(atif)} · hüküm bölümü BOŞ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
