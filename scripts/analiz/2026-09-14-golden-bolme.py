#!/usr/bin/env python3
"""Golden eval havuzunun dev/test/locked bölmesi — K31'in mührü.

NEDEN ŞİMDİ VE HEPSİ BİRDEN: K31 `dev`in oyunlanmasını bekliyor, `test` ve
`locked`ın oyunlanmamasını şart koşuyor. Ama üç seti SIRAYLA yazarsam mühür
sahtedir: dev'de modelin nerede düştüğünü gördükten sonra test öğelerini
yazarken o bilgi elime bulaşır. Bu yüzden bölme, tek bir öğe yazılmadan önce
ve **deterministik** olarak sabitleniyor: her tohumun ait olduğu dilim
seed_id'sinin hash'inden geliyor, benim seçimimden değil.

Bölme oranı: dev %50 · test %25 · locked %25.
  · dev    — her iterasyonda koşar, oyunlanması BEKLENİR
  · test   — her 5. iterasyonda
  · locked — TOPLAM 2 KEZ (baseline + final), 🔒

⚠️ Bu bölme TOHUM havuzunun bölmesidir, öğelerin değil. Bir dilime öğe yazmak
istediğimde yalnızca o dilimin havuzundan tohum çekebilirim.

⚠️ Havuz Eksen 1 (terapötik kalite) içindir. Kriz ve yüksek risk `golden_uygun`
ile ELENİR — onlar Eksen 2'nin konusu ve protokolü uzman Oturum 1'e bağlı (Kural 3).

Kullanım: uv run python scripts/analiz/2026-09-14-golden-bolme.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
sys.path.insert(0, str(KOK / "src"))
import tohum_guvenlik as tg  # noqa: E402

TOHUMLAR = KOK / "data/seeds.jsonl"
BOLME = KOK / "evals/bolme.json"
def _muhur_kapisi(yol, icerik) -> None:
    """Dondurulmuş/mühürlü çıktıyı sessizce yeniden yazmayı engeller.

    ⛔ 2026-09-16: `date.today()` yüzünden bu betiği ertesi gün koşmak mühürlü
    dosyanın SHA'sını değiştiriyordu ve hiçbir yerde uyarı çıkmıyordu (K126).
    Tarih artık sabit; kapı ikinci savunma hattı — içerik BAŞKA bir sebeple
    kayarsa da duruyor.
    """
    import sys as _s
    ham = icerik if isinstance(icerik, bytes) else icerik.encode("utf-8")
    if yol.exists() and yol.read_bytes() != ham and "--yenile" not in _s.argv:
        _s.exit(f"⛔ MÜHÜR: {yol.name} mevcut içerikten FARKLI üretildi ve "
                f"üzerine YAZILMADI.\n   Kasten yenilemek için: --yenile")
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_bytes(ham)
RAPOR = KOK / "reports/analiz/2026-09-14-golden-bolme.md"
TUZ = "birag-golden-2026-09-14"          # bölmeyi sabitleyen tuz; DEĞİŞTİRİLMEZ
ORAN = [("dev", 50), ("test", 25), ("locked", 25)]


def dilim(seed_id: str) -> str:
    """seed_id → dilim. Deterministik, sırasız, benim seçimimden bağımsız."""
    h = hashlib.sha256((TUZ + seed_id).encode()).hexdigest()
    nokta = int(h[:8], 16) % 100
    esik = 0
    for ad, pay in ORAN:
        esik += pay
        if nokta < esik:
            return ad
    return ORAN[-1][0]


def kullanilmis_id() -> set[str]:
    """Üretimde kullanılmış tohumlar — golden'a giremez (eğitimde görülmüş olur)."""
    kul: set[str] = set()
    for yol in sorted((KOK / "data/candidates").glob("*.jsonl")):
        for satir in open(yol):
            r = json.loads(satir)
            kul.update(r.get("source_ids") or [])
            for anahtar in ("seed_id",):
                for kap in (r, r.get("gen_meta") or {}, r.get("seed_meta") or {}):
                    if isinstance(kap, dict) and kap.get(anahtar):
                        kul.add(kap[anahtar])
    return kul


def main() -> None:
    tohumlar = [json.loads(l) for l in open(TOHUMLAR) if l.strip()]
    kullanilan = kullanilmis_id()

    havuz, elenen = [], collections.Counter()
    for t in tohumlar:
        if t["seed_id"] in kullanilan or t["source_id"] in kullanilan:
            elenen["üretimde kullanılmış"] += 1
            continue
        uygun, gerekce = tg.golden_uygun(t)
        if not uygun:
            elenen[gerekce.split(":")[0].split("=")[0].strip()] += 1
            continue
        havuz.append(t)

    atama = {t["seed_id"]: dilim(t["seed_id"]) for t in havuz}
    # ⛔ K31: `evals/bolme.json` MÜHÜRLÜ. Kapı olmadan bu satır mührü sessizce kırar.
    _muhur_kapisi(BOLME, json.dumps({
        "tuz": TUZ, "oran": dict(ORAN), "tarih": TARIH,
        "havuz_boyu": len(havuz), "atama": atama,
    }, ensure_ascii=False, indent=1))

    sayim = collections.Counter(atama.values())
    capraz = collections.Counter((t["meta"].get("senaryo"), atama[t["seed_id"]]) for t in havuz)
    senaryolar = sorted({s for s, _ in capraz})

    L = ["# Golden eval bölmesi — K31 mührü", "",
         f"**Girdi:** `data/seeds.jsonl` · SHA256 "
         f"`{hashlib.sha256(TOHUMLAR.read_bytes()).hexdigest()}`  ",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
         f"**Çıktı:** `evals/bolme.json` · **Tuz:** `{TUZ}`", "", "---", "",
         "## 0. Neden bölme öğelerden önce",
         "",
         "K31 `dev`in oyunlanmasını bekler, `test` ve `locked`ın oyunlanmamasını şart koşar. "
         "Üç seti sırayla yazsaydım mühür sahte olurdu: dev'de modelin nerede düştüğünü "
         "gördükten sonra test öğelerini yazarken o bilgi elime bulaşırdı. Bölme bu yüzden "
         "**tek bir öğe yazılmadan önce** ve seed_id hash'inden sabitlendi — benim seçimimden "
         "değil. Bir dilime öğe yazarken yalnızca o dilimin havuzundan tohum çekilebilir.", "",
         "## 1. Havuz", "",
         "| | Tohum |", "|---|---:|",
         f"| `data/seeds.jsonl` toplam | {len(tohumlar)} |"]
    for ad, n in elenen.most_common():
        L.append(f"| − elendi: {ad} | {n} |")
    L += [f"| **Eksen 1 golden havuzu** | **{len(havuz)}** |", "",
          "> Elenenlerin çoğu `risk_seviyesi` yüzünden. **Bu bir kapsama açığıdır, kusur değil:** "
          "kriz ve yüksek risk Eksen 2'nin konusu ve protokolü uzman Oturum 1'e bağlı (Kural 3). "
          "golden.dev sınır davranışını ÖLÇMEZ; `evals/safety_crisis.jsonl` bekliyor.", "",
          "## 2. Dilim dağılımı", "",
          "| Dilim | Tohum | Oran | Hedef |", "|---|---:|---:|---:|"]
    for ad, pay in ORAN:
        n = sayim[ad]
        L.append(f"| `{ad}` | {n} | %{n/len(havuz)*100:.1f} | %{pay} |")
    L += ["", "## 3. Senaryoya göre çapraz", "",
          "| Senaryo | " + " | ".join(a for a, _ in ORAN) + " | toplam |",
          "|---|" + "---:|" * (len(ORAN) + 1)]
    for s in senaryolar:
        satir = [capraz[(s, a)] for a, _ in ORAN]
        L.append(f"| `{s}` | " + " | ".join(str(x) for x in satir) + f" | {sum(satir)} |")
    L += ["",
          "> `kriz`, `sanrili_soylem` ve yüksek risk havuzda YOK — §1'deki eleme. "
          "`inkar`, `discord`, `kayma_nuks` havuzda çok az; bu senaryolarda öğe "
          "gerekiyorsa **elle yazılacak** ve kaynağı öyle işaretlenecek.", ""]
    RAPOR.write_text("\n".join(L) + "\n")
    print(f"havuz: {len(havuz)} tohum · " + " · ".join(f"{a}={sayim[a]}" for a, _ in ORAN))
    print(f"yazıldı: {BOLME.relative_to(KOK)} · {RAPOR.relative_to(KOK)}")


if __name__ == "__main__":
    main()
