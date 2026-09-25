"""T168 İngilizce kontrol deneyi — ÖLÇÜM.

Ön kayıt: `configs/deney/2026-09-22-t168-ingilizce-kontrol.yaml` (commit 07ce8d8,
üretimden ÖNCE mühürlendi). Ölçüt ve hüküm kuralları oradan aynen uygulanır.

Yöntem (ön kayıttaki dört adım):
  1. Cevaptaki tırnak içi parçalar çıkarılır
  2. difflib ile kullanıcı metnindeki EN YAKIN parça bulunur (T168'in yöntemi)
  3. Hizalanan KAYNAK parçası hedef ögeyi içermiyorsa öge SAYILMAZ
  4. İçeriyorsa ve alıntıda hedef yoksa → DÜŞME

Çıktı: reports/analiz/2026-09-22-t168-ingilizce-kontrol.md
"""

from __future__ import annotations

import difflib
import hashlib
import json
import re
import sys
from math import comb
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))

from tohum_guvenlik import tr_fold  # noqa: E402

# Tur seçimi: tur1 (varsayılan) · tur2 · birlesik (ikisi havuzlanır)
TUR = next((a for a in sys.argv[1:] if a in {"tur1", "tur2", "birlesik"}), "tur1")
_T1 = (KOK / "data/deney/2026-09-22-t168-ogeler.jsonl", KOK / "data/deney/ham")
_T2 = (KOK / "data/deney/2026-09-22-t168-ogeler-tur2.jsonl", KOK / "data/deney/ham2")
KAYNAKLAR = {"tur1": [_T1], "tur2": [_T2], "birlesik": [_T1, _T2]}[TUR]
RAPOR = KOK / "reports/analiz" / {
    "tur1": "2026-09-22-t168-ingilizce-kontrol.md",
    "tur2": "2026-09-22-t168-ingilizce-kontrol-tur2.md",
    "birlesik": "2026-09-22-t168-ingilizce-kontrol-birlesik.md",
}[TUR]

HUCRELER = ["tr_klitik", "en_klitik", "tr_serbest", "en_serbest"]
HIZALAMA_ESIGI = 0.60  # T168 bu eşiğin altındaki iki bulguya şerh düşmüştü

# Tırnak biçimleri: düz, tipografik, Türkçe çift tırnak
TIRNAK = re.compile(r'"([^"]{3,})"|“([^”]{3,})”|«([^»]{3,})»')
SOZCUK = re.compile(r"\w+", re.UNICODE)


def sha16(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def sozcukle(metin: str) -> list[str]:
    return [tr_fold(m.group(0)) for m in SOZCUK.finditer(metin)]


def hedef_var(sozcukler: list[str], hedef: str) -> bool:
    """Hedef öge sözcük dizisinde SÖZCÜK OLARAK var mı (çok sözcüklü de olabilir)."""
    h = [tr_fold(x) for x in SOZCUK.findall(hedef)]
    n = len(h)
    return any(sozcukler[i : i + n] == h for i in range(len(sozcukler) - n + 1))


def alintilar(cevap: str) -> list[str]:
    return [next(g for g in m.groups() if g) for m in TIRNAK.finditer(cevap)]


def hizala(kaynak: list[str], alinti: list[str]) -> tuple[int, int, float]:
    """Alıntının kaynakta kapsadığı sözcük aralığı ve o ARALIĞA karşı hizalama oranı.

    ⛔⛔ İlk uygulamada oran **tüm kaynağa** karşı hesaplanıyordu ve bu, kısa
    alıntıları sistematik olarak eliyordu: 4 sözcüklük bir alıntı 9 sözcüklük bir
    kaynağa karşı ~0,6 veriyor ⇒ eşiğin altında kalıyor. Oysa T168'in olgusu tam
    da **kısaltmada** oluyor ⇒ kusur, aranan şeyi aramanın önüne geçiyordu
    (*«coming home regularly too»* hedefi içerdiği hâlde «sayılmadı» çıkmıştı).
    Ön kayıt *«en yakın PARÇA bulunur»* diyor; doğrusu aralığa karşı orandır.
    """
    sm = difflib.SequenceMatcher(None, kaynak, alinti, autojunk=False)
    bloklar = [b for b in sm.get_matching_blocks() if b.size > 0]
    if not bloklar:
        return (0, 0, 0.0)
    bas = bloklar[0].a
    son = bloklar[-1].a + bloklar[-1].size
    oran = difflib.SequenceMatcher(None, kaynak[bas:son], alinti, autojunk=False).ratio()
    return (bas, son, oran)


def fisher(a: int, b: int, c: int, d: int) -> float:
    n, s1, s2, k = a + b + c + d, a + b, c + d, a + c

    def P(x: int) -> float:
        return comb(s1, x) * comb(s2, k - x) / comb(n, k)

    g = P(a)
    return sum(P(x) for x in range(max(0, k - s2), min(s1, k) + 1) if P(x) <= g * (1 + 1e-9))


def main() -> int:
    sonuc: dict[str, list[dict]] = {h: [] for h in HUCRELER}
    for tur_no, (OGELER, HAM) in enumerate(KAYNAKLAR, 1):
      ogeler = {
        o["id"]: o
        for o in (json.loads(s) for s in OGELER.read_text(encoding="utf-8").splitlines() if s.strip())
      }
      for hucre in HUCRELER:
        yol = HAM / f"{hucre}.jsonl"
        for satir in yol.read_text(encoding="utf-8").splitlines():
            if not satir.strip():
                continue
            kayit = json.loads(satir)
            oge = ogeler[kayit["id"]]
            kaynak_s = sozcukle(oge["metin"])
            hedef = oge["hedef"]

            en_iyi = None
            for al in alintilar(kayit["cevap"]):
                al_s = sozcukle(al)
                bas, son, oran = hizala(kaynak_s, al_s)
                if oran < HIZALAMA_ESIGI:
                    continue
                kapsanan = kaynak_s[bas:son]
                if not hedef_var(kapsanan, hedef):
                    continue                       # adım 3: öge SAYILMAZ
                dustu = not hedef_var(al_s, hedef)  # adım 4
                aday = {
                    "alinti": al,
                    "kapsanan": " ".join(kapsanan),
                    "oran": round(oran, 3),
                    "dustu": dustu,
                }
                if en_iyi is None or aday["oran"] > en_iyi["oran"]:
                    en_iyi = aday

            sonuc[hucre].append(
                {
                    "id": f"t{tur_no}-" + kayit["id"],
                    "hedef": hedef,
                    "metin": oge["metin"],
                    "cevap": kayit["cevap"],
                    "tum_alintilar": alintilar(kayit["cevap"]),
                    "sayilir": en_iyi is not None,
                    **(en_iyi or {}),
                }
            )

    # ─── Sayım ─────────────────────────────────────────────────────────────
    ozet = {}
    for h in HUCRELER:
        sayilan = [r for r in sonuc[h] if r["sayilir"]]
        dusen = [r for r in sayilan if r["dustu"]]
        ozet[h] = {
            "toplam": len(sonuc[h]),
            "sayilan": len(sayilan),
            "dusen": len(dusen),
            "oran": (len(dusen) / len(sayilan)) if sayilan else None,
        }

    def karsilastir(a: str, b: str) -> tuple[float, str]:
        oa, ob = ozet[a], ozet[b]
        if not oa["sayilan"] or not ob["sayilan"]:
            return (1.0, "⛔ hücrelerden biri boş")
        p = fisher(
            oa["dusen"], oa["sayilan"] - oa["dusen"],
            ob["dusen"], ob["sayilan"] - ob["dusen"],
        )
        return (p, "**anlamlı**" if p < 0.05 else "anlamlı değil")

    p_klitik, y_klitik = karsilastir("tr_klitik", "en_klitik")
    p_serbest, y_serbest = karsilastir("tr_serbest", "en_serbest")
    p_tr_ici, y_tr_ici = karsilastir("tr_klitik", "tr_serbest")

    # ─── ÖN KAYITLI hüküm kuralları, mekanik uygulanır ─────────────────────
    o = {h: ozet[h]["oran"] for h in HUCRELER}
    kurallar = []
    if p_klitik < 0.05 and (o["tr_klitik"] or 0) > (o["en_klitik"] or 0) and p_serbest >= 0.05:
        kurallar.append("(b) **EKLEŞİKLİĞE ÖZGÜ** — klitik hücrede ayrım var, serbest hücrede yok")
    if p_klitik < 0.05 and p_serbest < 0.05 and (o["tr_klitik"] or 0) > (o["en_klitik"] or 0) \
            and (o["tr_serbest"] or 0) > (o["en_serbest"] or 0):
        kurallar.append("(a) **DİLE ÖZGÜ** — TR'nin iki hücresi de yüksek")
    if p_klitik >= 0.05 and p_serbest >= 0.05:
        yuksek = all((o[h] or 0) >= 0.5 for h in HUCRELER)
        dusuk = all((o[h] or 0) <= 0.2 for h in HUCRELER)
        if yuksek:
            kurallar.append("(c) **GENEL** — dört hücre de yüksek ⇒ T168'in «Türkçe'ye özgü» ucu DÜŞER")
        elif dusuk:
            kurallar.append("⛔ **OLGU YENİDEN ÜRETİLEMEDİ** — dört hücre de düşük; T168'in kendisi sorgulanır")
        else:
            kurallar.append("⛔ **SONUÇSUZ** — hiçbir karşılaştırma anlamlı değil; bu bir yokluk kanıtı DEĞİLDİR")

    # ─── Rapor ─────────────────────────────────────────────────────────────
    s = [f"# T168 İngilizce kontrol deneyi — SONUÇ ({TUR})\n\n"]
    s.append(
        f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** 2026-09-22  \n"
        f"**Ön kayıt:** `configs/deney/2026-09-22-t168-ingilizce-kontrol.yaml` "
        f"(**üretimden önce** commit `07ce8d8`)  \n"
        + "".join(
            f"**Öge kümesi ({i}):** `{o.relative_to(KOK)}` SHA256 `{sha16(o)}`  \n"
            for i, (o, _) in enumerate(KAYNAKLAR, 1)
        )
        + "**Ham üretim:** "
        + " · ".join(
            f"`{ha.name}/{h}.jsonl` `{sha16(ha / (h + '.jsonl'))}`"
            for _, ha in KAYNAKLAR for h in HUCRELER
        )
        + "  \n**Üretici:** `claude-sonnet-subagent`, kör (ölçülen şey söylenmedi) · "
        "⛔ yeniden koşulamaz (K30) — ham çıktılar saklandı\n\n---\n\n"
    )

    s.append("## 1. Sonuç tablosu\n\n")
    s.append("| Hücre | Öge | Sayılan | Düşen | Düşme oranı |\n|---|---:|---:|---:|---:|\n")
    for h in HUCRELER:
        z = ozet[h]
        oran = f"**%{100 * z['oran']:.0f}**" if z["oran"] is not None else "—"
        s.append(f"| `{h}` | {z['toplam']} | {z['sayilan']} | {z['dusen']} | {oran} |\n")
    s.append(
        "\n*«Sayılan»* = alıntının hizalandığı **kaynak parçası hedef ögeyi içeren** "
        "öge sayısı (ön kayıt adım 3). Model hedefi içermeyen bir yeri alıntıladıysa "
        "o öge **sayılmaz** — düşme sayılmaz.\n\n"
    )

    s.append("## 2. Ön kayıtlı sınamalar\n\n")
    s.append("| Karşılaştırma | Fisher p | Sonuç |\n|---|---:|---|\n")
    s.append(f"| `tr_klitik` ↔ `en_klitik` (**birincil**) | {p_klitik:.4f} | {y_klitik} |\n")
    s.append(f"| `tr_serbest` ↔ `en_serbest` (iç kontrol) | {p_serbest:.4f} | {y_serbest} |\n")
    s.append(f"| `tr_klitik` ↔ `tr_serbest` (TR içi) | {p_tr_ici:.4f} | {y_tr_ici} |\n")

    s.append("\n## 3. ⭐ HÜKÜM — ön kayıttaki kurallar mekanik uygulandı\n\n")
    for k in kurallar:
        s.append(f"- {k}\n")
    s.append(
        f"\n⛔ **Güç şerhi (koşudan önce ilan edildi):** n=12/hücre ile karşı hücre "
        f"sıfırken bile anlamlılık **5/12** düşme ister. Anlamsız bir sonuç "
        f"*«fark yok»* değil *«bu tasarımla gösterilemiyor»* demektir.\n\n"
    )

    s.append("---\n\n## 4. Öge öge kayıt\n\n")
    for h in HUCRELER:
        s.append(f"### `{h}`\n\n")
        s.append("| # | hedef | kullanıcı | alıntı | hizalanan kaynak | oran | hüküm |\n")
        s.append("|---|---|---|---|---|---:|---|\n")
        for r in sonuc[h]:
            if not r["sayilir"]:
                nicelik = "⚪ sayılmadı (hedefi içermeyen yer alıntılandı)"
                s.append(
                    f"| {r['id'][-2:]} | `{r['hedef']}` | {r['metin']} | "
                    f"{' / '.join(r['tum_alintilar']) or '—'} | — | — | {nicelik} |\n"
                )
            else:
                nicelik = "⛔ **DÜŞTÜ**" if r["dustu"] else "✅ korundu"
                s.append(
                    f"| {r['id'][-2:]} | `{r['hedef']}` | {r['metin']} | {r['alinti']} | "
                    f"{r['kapsanan']} | {r['oran']} | {nicelik} |\n"
                )
        s.append("\n")

    s.append("---\n\n## 5. ⛔ Sınırlar (ön kayıttan, değişmedi)\n\n")
    s.append(
        "| | |\n|---|---|\n"
        "| ⛔ **`de/da` klitik, `too` serbest sözcük** | iki klitik hücresi yapıca eşit değil — sorunun kendisi bu |\n"
        "| ⛔ **Ögeleri ben yazdım** (K30) | çeviri denkliği tek okuyucunun |\n"
        "| ⛔ **Tek üretici ailesi** | Claude; agy kotası dolu, OPENAI_API_KEY yok |\n"
        "| ⛔ **Blok üretimi** | 12 öge tek çağrıda ⇒ öge bağımsızlığı tam değil |\n"
        "| ⛔ **Üretim yeniden koşulamaz** | K30; ham çıktı ve SHA saklandı, köken izlenir |\n"
        f"| ⚠️ **Hizalama eşiği {HIZALAMA_ESIGI}** | bir SEÇİM; T168 de 0,53-0,60 aralığına şerh düşmüştü |\n"
    )

    RAPOR.write_text("".join(s), encoding="utf-8")
    print(f"yazıldı: {RAPOR.relative_to(KOK)}\n")
    for h in HUCRELER:
        z = ozet[h]
        oran = f"%{100 * z['oran']:.0f}" if z["oran"] is not None else "—"
        print(f"  {h:12s} sayılan {z['sayilan']:2d}/12 · düşen {z['dusen']:2d} · {oran}")
    print(f"\n  birincil (tr_klitik↔en_klitik) p = {p_klitik:.4f}  {y_klitik}")
    print(f"  iç kontrol (tr_serbest↔en_serbest) p = {p_serbest:.4f}  {y_serbest}")
    print(f"  TR içi (klitik↔serbest)            p = {p_tr_ici:.4f}  {y_tr_ici}")
    print("\n  HÜKÜM:")
    for k in kurallar:
        print("   ", re.sub(r"\*\*|`", "", k))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
