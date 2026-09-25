#!/usr/bin/env python3
"""Okunmayan 11 alan DOĞRU mu — T79'un (b) şıkkı ölçüldü (T90).

T79: `SeedMeta`'nın 16 alanından **11'ini** boru hattında hiçbir şey okumuyor ⇒
*«okunmayan bir alanın yanlış olduğu hiçbir yerde ortaya çıkmaz»*. Üç yol
vardı: (a) tüketen bir tabakalı örneklem yaz · **(b) betimleyici olarak kullan
ama doğruluklarını AYRICA denetle** · (c) şemadan çıkar.

⇒ (b) yapıldı. Ölçüt: **geri düşme oranı** — ham değer kanonik bir sınıfa
çevrilemeyip `diger`/`belirtilmemis`/`None`'a düşüyorsa, o alan ya kaynakta yok
ya da eşleme kopuk. ⛔ Ayrım bu betikle yapılamaz (T77'nin dersi: üst sınır ≠
gerçek), ama **yüksek geri düşme oranı bakılacak yeri gösterir**.

⚠️ Bu bir *«alan gereksiz»* ölçümü DEĞİL: okunmayan bir alan tezde betimleyici
istatistik olarak kullanılabilir — ama ancak **doğruysa**.

Girdi : <onaylı kaynak>/campaigns/*/total_output.jsonl (kullanıcı izniyle, Kural 1) ·
        data/seeds.jsonl · data/seeds.v2.jsonl
Çıktı : reports/analiz/2026-09-16-okunmayan-alan-denetimi.md
Kullanım: uv run python scripts/analiz/2026-09-16-okunmayan-alan-denetimi.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-okunmayan-alan-denetimi.md"
sys.path.insert(0, str(KOK / "src"))
import normalize as N  # noqa: E402

# ⭐ T79'un ELLE OKUMASI (Kural 6): boru hattının gerçekten okuduğu 5 alan.
OKUNAN = {"senaryo", "yas_grubu", "risk_seviyesi", "bagimlilik_turu", "notlar"}
# ⛔⛔ GERİ DÜŞME DEĞERİ ALANIN KENDİSİNE BAĞLIDIR — ilk sürüm `"yok"`u her alanda
#    geri düşme saydı ve `onceki_tedavi`yi %69 ile *«yüksek riskli»* gösterdi.
#    Oysa orada `yok` = **önceki tedavi yok**, yani GERÇEK bir değer; `stres_tipi`'nde
#    ise `normalize()` onu fallback olarak ÜRETİYOR
#    (`"yok" if senaryo != "belirsiz" else None`). ⭐ Aynı dizge bir alanda VERİ,
#    ötekinde YOKLUK. ⇒ Küme alan başına ilan ediliyor.
GENEL = {"diger", "belirtilmemis", "belirsiz", None, ""}
GERI_ALAN = {
    "stres_tipi": GENEL | {"yok"},      # `yok` fallback olarak üretiliyor
    "onceki_tedavi": GENEL | {"bilinmiyor"},   # `yok` GERÇEK değer
}


def geri_kume(alan: str) -> set:
    return GERI_ALAN.get(alan, GENEL)


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def main() -> int:
    tohum_yol = KOK / "data/seeds.v2.jsonl"
    tohumlar = [json.loads(l) for l in tohum_yol.read_text(encoding="utf-8").split("\n") if l.strip()]
    alanlar = [a for a in tohumlar[0]["meta"] if a != "notlar"] if tohumlar else []

    L: list[str] = []
    L += ["# Okunmayan alanlar doğru mu — T79'un (b) şıkkı", "",
          f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
          f"**Girdi:** `data/seeds.v2.jsonl` SHA256 `{sha(tohum_yol)}` — "
          f"**{len(tohumlar)}** tohum", "", "---", "", "## Neden", "",
          "T79: `SeedMeta`'nın 16 alanından **11'ini** boru hattında hiçbir şey okumuyor",
          "⇒ *okunmayan bir alanın yanlış olduğu hiçbir yerde ortaya çıkmaz.* Üç yoldan",
          "**(b)** seçildi: betimleyici olarak kullan ama doğruluğunu **ayrıca denetle**.", "",
          "⭐ Ölçüt **geri düşme oranı**: ham değer kanonik bir sınıfa çevrilemeyip",
          "`diger`/`belirtilmemis`/`belirsiz`/`None`'a düşüyorsa alan ya kaynakta yok",
          "ya da eşleme kopuk. ⛔ İkisini bu betik **ayıramaz** (T77: üst sınır ≠",
          "gerçek) — ama **bakılacak yeri gösterir**.", "",
          "⛔⛔ **Geri düşme değeri ALANIN KENDİSİNE bağlıdır ve ilk ölçümüm bunu",
          "kaçırdı:** `\"yok\"`u her alanda geri düşme saymıştım ve `onceki_tedavi` %69 ile",
          "*«yüksek riskli»* göründü. Oysa orada `yok` = **önceki tedavi yok**, yani",
          "gerçek bir değer; `stres_tipi`'nde ise `normalize()` onu **fallback olarak**",
          "**üretiyor**. ➡️ *Aynı dizge bir alanda VERİ, ötekinde YOKLUK — ve bunu ayıran",
          "şey değerin kendisi değil, onu üreten KODdur.*", "", "---", "",
          "## Geri düşme oranları", "",
          "| alan | okunuyor mu | geri düşen | oran | |", "|---|---|---:|---:|---|"]
    riskli = []
    for a in alanlar:
        n = sum(1 for t in tohumlar if t["meta"].get(a) in geri_kume(a))
        p = 100 * n / len(tohumlar)
        okunur = a in OKUNAN
        isaret = ("✅" if p < 10 else "⚠️" if p < 40 else "⛔ **yüksek**")
        if p >= 40 and not okunur:
            riskli.append((a, n, p))
        L.append(f"| `{a}` | {'⭐ evet' if okunur else '—'} | {n} | %{p:.1f} | {isaret} |")
    L += ["",
          (f"⛔ **{len(riskli)} okunmayan alanın geri düşme oranı %40'ın üstünde:** "
           + ", ".join(f"`{a}` (%{p:.0f})" for a, _, p in riskli) + "."
           if riskli else "✅ **Okunmayan alanların hiçbirinde %40 üstü geri düşme yok.**"),
          "",
          "⭐ **Kalan tek yüksek satır `stres_tipi` ve sebebi T77'de ölçülü:**",
          "`normalize()` zinciri `_exact`'i önce deniyor (374/2240 kayıt) ve `_keyword`'e",
          "ulaşan 1866 kaydın tamamı İngilizce `snake_case`; eşleşmeyen her kayıt",
          "`senaryo != belirsiz` ise **yapıca** `yok` alıyor. ⇒ Oran bir **kopukluk**",
          "değil, zincirin tasarımı. ⚠️ Yine de tezde betimleyici olarak kullanılırsa",
          "*«%76'sı `yok`»* cümlesi **yanıltıcıdır**: o `yok` ölçülmüş bir yokluk değil,",
          "**ölçülememiş** bir alandır.", "",
          "⚠️ **Yüksek oran kendiliğinden kusur DEĞİL:** `senaryo=belirsiz` %23,7 ve o",
          "**tasarım gereği** (K37: belirsiz bir etiketleme borcu değil, üretim-zamanı",
          "kararı). ⇒ Her yüksek satır **elle** okunmalı; bu betik onları **işaretler**,",
          "hükmetmez.", "", "---", "",
          "## ⭐ En sık değerler — okunmayan alanlar", ""]
    for a in alanlar:
        if a in OKUNAN:
            continue
        c = collections.Counter(str(t["meta"].get(a)) for t in tohumlar)
        ilk = ", ".join(f"`{k}` %{100*v/len(tohumlar):.0f}" for k, v in c.most_common(4))
        L.append(f"· **`{a}`** ({len(c)} ayrık) — {ilk}  ")
    L += ["",
          "➡️ *Bir alanın **ayrık değer sayısı** ve **en sık değerinin payı** birlikte*",
          "*okunur: 1-2 ayrık değer taşıyan bir alan ya gerçekten tekdüze ya da eşlemesi*",
          "*çökmüş demektir ve ikisi ayırt edilmelidir.*", "",
          "## ⛔ Bu denetimin söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ **«Kaynakta yok» ile «eşleme kopuk» ayrılmadı** | ayırmak için ham meta "
          "ile alan alan karşılaştırma gerekir; T77 bunu yalnızca `egitim`, "
          "`kullanim_suresi` ve `stres_tipi` için yaptı |",
          "| ⛔ **Doğruluk ölçülmedi, GERİ DÜŞME ölçüldü** | geri düşmeyen bir değer de "
          "yanlış olabilir (yanlış kova — T76'nın sınıfı) |",
          "| ⚠️ Yüksek oran kusur değil | `senaryo=belirsiz` tasarım gereği (K37) |",
          "| ⛔ `notlar` kapsam dışı | sözlük; alt anahtarları ayrıca taranmadı |", ""]

    RAPOR.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    print(f"   alan {len(alanlar)} · okunmayan ve %40+ geri düşen: {len(riskli)}" +
          (" -> " + ", ".join(a for a, _, _ in riskli) if riskli else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
