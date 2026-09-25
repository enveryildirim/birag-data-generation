#!/usr/bin/env python3
"""v3 korpusunun `plan.md` §6 dilim hedeflerine karşı kapsaması — parti 3 öncesi.

Korpus hedef raporu `uretim-v3.md`'nin hedeflerini ölçüyor (tur kapanışı, MI süreci,
konuşma durumu). Bu betik başka bir şeyi ölçüyor: `plan.md` §6'nın DİLİM karışımını.
İkisi farklı belgeler ve farklı hedefler; §6 bugüne kadar hiç ölçülmemişti.

Girdi : data/candidates/v3-parti1.jsonl + v3-parti2-tam.jsonl
Çıktı : reports/analiz/2026-09-14-dilim-kapsama.md
"""
from __future__ import annotations

import collections
import hashlib
import json
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
GIRDILER = [KOK / "data/candidates/v3-kumulatif.jsonl"]
CIKTI = KOK / "reports/analiz/2026-09-14-dilim-kapsama.md"

# plan.md §6 — oranlar oradan birebir alınır.
S6 = {"Terapötik diyalog, tek tur": .35, "Çok turlu diyalog": .15,
      "Kriz + rol sınırı": .10, "Direnç / inkâr / discord": .05,
      "Nazikçe karşı çıkma": .05, "RAG modu — context sadakati": .10,
      "Kapsam dışı / sınır": .05, "Replay (genel amaçlı)": .15}
BANT_IYI, BANT_UYARI = .05, .10   # korpus raporuyla aynı konvansiyon (Kural 6)
# 19 davranış kartı — docs/davranis-kartlari.md
KARTLAR = ["motivasyon", "kriz", "farkindalik", "kutlama", "bilgilendirme",
           "hedef_belirleme", "kayma_nuks", "ambivalans", "inkar", "discord",
           "rol_siniri", "durtu", "hukuki_kaygi", "borc_finansal", "kayip_kovalama",
           "nazikce_karsi_cikma", "anlasilmama", "bilmiyorum_cikmazi", "sanrili_soylem"]


def hukum(gercek: float, hedef: float) -> str:
    fark = abs(gercek - hedef)
    return "✅" if fark <= BANT_IYI else ("⚠️" if fark <= BANT_UYARI else "❌")


def main() -> None:
    rows = []
    for g in GIRDILER:
        rows += [json.loads(l) for l in open(g) if l.strip()]
    n = len(rows)
    sen = collections.Counter(r["scenario"] for r in rows)
    kullanici_turu = [sum(1 for m in r["messages"] if m["role"] == "user") for r in rows]
    derin = sum(1 for k in kullanici_turu if k >= 3)

    olcum = {
        "Terapötik diyalog, tek tur": sum(1 for r in rows if r["slice"] == "terapotik_tek_tur"),
        "Çok turlu diyalog": sum(1 for r in rows if r["turn_type"] == "multi"),
        "Kriz + rol sınırı": sum(1 for r in rows if r["is_crisis"]) + sen["rol_siniri"] + sen["hukuki_kaygi"],
        "Direnç / inkâr / discord": sen["inkar"] + sen["discord"] + sen["anlasilmama"],
        "Nazikçe karşı çıkma": sen["nazikce_karsi_cikma"],
        "RAG modu — context sadakati": sum(1 for r in rows if r.get("context")),
        "Kapsam dışı / sınır": sum(1 for r in rows if r["is_negative"]),
        "Replay (genel amaçlı)": sum(1 for r in rows if r.get("replay")),
    }
    L = [f"# Dilim kapsaması — `plan.md` §6'ya karşı", "",
         "**Girdi:** " + " · ".join(
             f"`{g.relative_to(KOK)}` (SHA256 `{hashlib.sha256(g.read_bytes()).hexdigest()[:16]}…`)"
             for g in GIRDILER) + "  ",
         f"**Betik:** `scripts/analiz/2026-09-14-dilim-kapsama-raporu.py` · "
         f"**Tarih:** {TARIH} · **Kayıt:** {n}", "", "---", "",
         "> Bu rapor `uretim-v3.md` hedeflerini DEĞİL, `plan.md` §6'nın **dilim karışımını** "
         "ölçüyor. İkisi ayrı belgeler; §6 bugüne kadar hiç ölçülmemişti.", "",
         "## 1. §6 dilim karışımı", "",
         "| Dilim | Var | Oran | Hedef | Sapma | |", "|---|---:|---:|---:|---:|:--:|"]
    for k, h in S6.items():
        v = olcum[k]
        L.append(f"| {k} | {v} | %{v/n*100:.0f} | %{h*100:.0f} | "
                 f"{(v/n - h)*100:+.0f} p | {hukum(v/n, h)} |")

    L += ["", "## 2. ⚠️ Çok turlu kayıtların DERİNLİĞİ", "",
          "§6 *\"3-5 turluk alışveriş\"* diyor ve §5c çok turlu kayıtların **MI süreci "
          "geçişini** öğretmesini istiyor. Ölçüm:", "",
          "| Kullanıcı turu | Kayıt |", "|---:|---:|"]
    for k, v in sorted(collections.Counter(kullanici_turu).items()):
        L.append(f"| {k} | {v} |")
    # ⚠️ Hüküm cümlesi SAYIDAN türetilir. İlk yazımda sabitti ve parti 3 yazıldıktan
    # sonra rapor kendi tablosuyla çeliştı: tablo 3+ turlu 14 derken metin "yok"
    # diyordu. K80'in aynısı, aynı gün, başka bir betikte.
    iki_turlu = sum(1 for k in kullanici_turu if k == 2)
    if derin == 0:
        yorum = (f"§6'nın istediği derinlikte kayıt **yok**; çok turlu sayılan "
                 f"{olcum['Çok turlu diyalog']} kaydın tamamı iki kullanıcı turlu, yani "
                 "tek bir alışveriş. Süreç geçişi iki turda gösterilemez.")
    else:
        yorum = (f"Çok turlu {olcum['Çok turlu diyalog']} kaydın **{iki_turlu}**'i iki "
                 f"turlu (tek alışveriş), **{derin}**'ü 3-5 turlu. §6'nın istediği "
                 "derinlik artık korpusta var ama çoğunluk hâlâ iki turlu.")
    L += ["", f"**3+ turlu kayıt: {derin}/{n} (%{derin/n*100:.0f}).** " + yorum, "",
          "## 3. Davranış kartı kapsaması", "",
          f"19 karttan **{len([k for k in KARTLAR if sen.get(k)])}**'i üretildi.", "",
          "| Kart | Kayıt |", "|---|---:|"]
    for k in KARTLAR:
        L.append(f"| `{k}` | {sen.get(k, 0)}{'  ⛔ uzman onayı bekliyor' if k in ('kriz','sanrili_soylem') else ''} |")
    # ⚠️ Bu bölüm de SAYIDAN türetilir; sabit metin bırakılmaz (K80).
    L += ["", "## 4. Okuma", ""]
    L += [f"- {'❌' if olcum['Replay (genel amaçlı)'] == 0 else '⚠️'} **Replay "
          f"{olcum['Replay (genel amaçlı)']}/{n}.** §6 bu dilimi *\"açık genel amaçlı "
          "setlerden örneklenir\"* diye tanımlıyor — Claude Code üretimi değil. Ayrı bir "
          "iş kalemi (catastrophic forgetting savunması, §9)."]
    tt = olcum["Terapötik diyalog, tek tur"]
    L += [f"- {hukum(tt/n, .35)} **Terapötik tek tur %{tt/n*100:.0f}**, hedef %35. "
          "Diğer dilimler eksik olduğu sürece bu pay mekanik olarak şişer; kendi "
          "başına bir kusur değil."]
    kd = olcum["Kapsam dışı / sınır"]
    L += [f"- ⚠️ **Kapsam dışı / sınır %{kd/n*100:.0f}**, `plan.md` §6 %5 diyor — ama "
          "`uretim-v3.md` §8 aynı şey için **%15** diyor. **İki belge çelişiyor**; "
          "hangisinin geçerli olduğu kararlaştırılmalı (işaretlenen tutarsızlıktır, "
          "çözümü değil)."]
    nk = olcum["Nazikçe karşı çıkma"]
    L += [f"- {hukum(nk/n, .05)} **Nazikçe karşı çıkma %{nk/n*100:.0f}**, hedef %5. "
          "K21 bu dilimi *\"eğitilmezse ortaya çıkmaz\"* diye işaretliyor."]
    bos = [k for k in KARTLAR if not sen.get(k)]
    if bos:
        L += [f"- ⛔ Hiç üretilmemiş davranış kartı: " + ", ".join(f"`{k}`" for k in bos)
              + ". `kriz` ve `sanrili_soylem` uzman onayı bekliyor (Kural 3)."]
    L += [f"- Derin çok turlu (3-5 tur): **{derin}/{n}**. §6'nın \"3-5 turluk alışveriş\" "
          "beklentisi için ölçülen tek sayı budur; `turn_type=multi` iki turlu kayıtları "
          "da sayar ve tek başına yanıltıcıdır.", ""]

    CIKTI.write_text("\n".join(L) + "\n")
    print(f"yazıldı: {CIKTI.relative_to(KOK)} ({n} kayıt · 3+ turlu {derin})")


if __name__ == "__main__":
    main()
