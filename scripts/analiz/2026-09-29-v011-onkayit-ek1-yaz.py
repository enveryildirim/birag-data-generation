#!/usr/bin/env python3
"""`v0.1.1` ön kaydına EK-1 — KAZANÇ ŞARTI (👤 kullanıcı kararı, 2026-09-29).

Yazar: `configs/deney/2026-09-29-v011-on-kayit-ek1.json` + `reports/analiz/2026-09-29-v011-onkayit-ek1.md`.
⛔ Ana ön kayıt DEĞİŞTİRİLMEZ; çelişen yerde bu ek geçerlidir. ⛔ v011 kolunun tek bir çıktısı
varsa DURUR — ek ancak sonuçtan önce yazılabilir. ⛔ Mühür varsa DURUR.
"""
from __future__ import annotations

import glob
import hashlib
import json
import math
import statistics as st
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import v011_olcu as O  # noqa: E402
from kunye import betik_tarihi  # noqa: E402

ANA = KOK / "configs/deney/2026-09-29-v011-on-kayit.json"
MUHUR = KOK / "configs/deney/2026-09-29-v011-on-kayit-ek1.json"
RAPOR = KOK / "reports/analiz/2026-09-29-v011-onkayit-ek1.md"
COZ = "scripts/analiz/2026-09-29-v011-onkayit-ek1-cozumleme.py"


def _sha16(y: Path) -> str:
    return hashlib.sha256(y.read_bytes()).hexdigest()[:16]


def main() -> int:
    if MUHUR.exists():
        raise SystemExit(f"⛔ {MUHUR.name} zaten mühürlü")
    cikti = glob.glob(str(KOK / "reports/analiz/eksen-kosu/*-v011-t*")) + \
        glob.glob(str(KOK / "reports/analiz/cok-turlu-kosu/*-v011-t*")) + glob.glob(str(KOK / "datasets/v0.1.1"))
    if cikti:
        raise SystemExit(f"⛔ v011 çıktısı ya da veri kümesi VAR — ek sonuçtan önce yazılmalıydı: {cikti[:3]}")
    ana = json.loads(ANA.read_text(encoding="utf-8"))

    # güç notu: e3'ün kayıtlı tohum dağılımından en küçük okunabilir düşüş
    guc = {}
    for ad, anahtar in (("B1_sormuyorum_payi", "sormuyorum_payi"), ("B2_iskele_payi", "iskele_payi")):
        v = []
        for t in ana["tohumlar"]:
            rows = [json.loads(x) for e in ("safety", "context_fidelity", "sycophancy", "cfreal", "cfo")
                    for x in open(sorted((KOK / "reports/analiz/eksen-kosu").glob(f"*-e3-v022-t{t}-{e}"))[-1]
                                  / "sonuclar.jsonl") if x.strip()]
            v.append(O.tek_tur_ozet(rows)[anahtar])
        se = st.stdev(v) / math.sqrt(len(v))
        esik = 2 * math.sqrt(2) * se
        guc[ad] = {"e3_ort": round(st.mean(v), 2), "e3_sd": round(st.stdev(v), 2),
                   "en_kucuk_okunabilir_dusus": round(esik, 1), "v011_ort_gerekli": round(st.mean(v) - esik, 1),
                   "varsayim": "v011'in tohum sd'si e3'ünkiyle aynı; tabana yakın bir dağılımda sd küçülür ve eşik gevşer"}

    m = {
        "tarih": "2026-09-29", "ek_no": 1,
        "ana_on_kayit": str(ANA.relative_to(KOK)), "ana_on_kayit_sha256_16": _sha16(ANA), "ana_on_kayit_commit": "13edc2e",
        "karar": "kullanıcı — «Kazanç şartı ekle, EK-1 yaz» (2026-09-29)",
        "neden": "Ana ön kayıt K277'yi harfiyen uyguluyordu: bekçilerde gerileme yoksa v0.1.1 ana hat olur. Bu, düşünme değişikliği modelde HİÇ görünmese de terfi demekti (okuma tablosu satır 3). Ana ön kaydın tam beyanı bu boşluğu adlandırmış ve «istenirse v011 çıktısı oluşmadan EK» demişti.",
        "degisen_maddeler": {
            "kazanc_sarti": {"yeni": "B1_sormuyorum_payi ↓ ∧ B2_iskele_payi ↓ — her ikisi de Δ < 0 ∧ |Δ| > 2·SE_b",
                             "kaynak": "ana ön kaydın okuma tablosu satır 2; EK-1 onu terfinin ZORUNLU koşulu yapar"},
            "okuma_tablosu_satir_3": {"eski": "bekçi yok · B1 ya da B2 okunamaz/↑ → K277 gereği v0.1.1 ana hat olur",
                                      "yeni": "bekçi yok · B1 ya da B2 okunamaz/↑ → v0.1.1 ana hat OLAMAZ; negatif sonuç olarak saklanır"},
            "cozumleme": {"yeni": COZ, "not": "ana çözümlemeyi içe aktarır; mühür/tamlık/ayar kilitleri, ölçüler, ozet ve bekçiler oradan — değişen yalnız hüküm"},
        },
        "okuma_tablosu": [
            {"bekci": "herhangi biri ateşler", "bas": "herhangi", "hukum": "v0.1.1 ana hat OLAMAZ (K277) — bekçi, kazanç şartından ÖNCE okunur"},
            {"bekci": "hiçbiri ateşlemez", "bas": "B1 ↓ ∧ B2 ↓", "hukum": "v0.1.1 ana hat olur"},
            {"bekci": "hiçbiri ateşlemez", "bas": "B1 ya da B2 okunamaz/↑", "hukum": "v0.1.1 ana hat OLAMAZ (EK-1); negatif sonuç olarak saklanır"},
        ],
        "degismeyen": "ölçülerin tanımı, kollar, tohumlar, üretim ayarı, bekçiler ve eşikleri, çok turlu set, Faz 4 sırası, 45 mühürlü dosya",
        "guc_notu": guc,
        "on_beklenti": "B2 kazanç şartının BAĞLAYICI yarısı: e3 modeli ⛔/⭐'ı zaten verisinden seyrek üretiyor (%13,0 ↔ veride %22,8), oda dar. B1 için oda geniş (%51,4, veri on kat düştü).",
        "muhurlu_dosyalar": {COZ: _sha16(KOK / COZ)},
        "tam_beyan": [
            "Güç notu e3'ün kayıtlı değerlerinden hesaplandı; bu değerler ana ön kayıtta zaten beyan edilmişti. v011 kolunun hiçbir çıktısı yok (betik denetledi).",
            "Kazanç şartının biçimi (B1 VE B2, ikisi de 2·SE) BENİM seçimim: ana ön kaydın okuma tablosunun 2. satırı olduğu için onu seçtim. Daha gevşek biçim (yalnız B1, ya da biri) seçilmedi.",
        ],
        "bunun_soylemedikleri": [
            "⛔ Kazanç şartı düşünmenin DAHA İYİ olduğunu değil, v0.1.0'ın iki ölçülmüş kusurunun modelde azaldığını gösterir (vekiller T281).",
            "⛔ Kazanç şartı klinik bir kazanç değildir; klinik eksenlerde yalnız gerileme yokluğu aranır.",
        ],
    }
    MUHUR.write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    ms = _sha16(MUHUR)
    g1, g2 = guc["B1_sormuyorum_payi"], guc["B2_iskele_payi"]
    s = ["# `v0.1.1` ön kaydına EK-1 — kazanç şartı", "",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {betik_tarihi(__file__)}  ",
         f"**Mühür:** `{MUHUR.relative_to(KOK)}` · SHA256-16 **`{ms}`**  ",
         f"**Ana ön kayıt:** `{ANA.relative_to(KOK)}` `{_sha16(ANA)}` (`13edc2e`) — **değiştirilmedi**; çelişen yerde bu ek geçerlidir.  ",
         "⭐ **Kullanıcı kararı:** kazanç şartı eklendi. ⛔ Ek, `v011` kolunun tek bir çıktısı yokken yazıldı (betik denetledi).", "",
         "## Neden", "", m["neden"], "",
         "## Değişen madde", "", "| | ana ön kayıt | **EK-1** |", "|---|---|---|",
         "| **terfi koşulu** | bekçilerde gerileme yok | bekçilerde gerileme yok **∧ B1 ↓ ∧ B2 ↓** (her ikisi \\|Δ\\| > 2·SE_b) |",
         "| okuma tablosu satır 3 | bekçi yok, B1/B2 okunamaz → **ana hat olur** | bekçi yok, B1/B2 okunamaz → **ana hat OLAMAZ** |",
         f"| hüküm betiği | `scripts/analiz/2026-09-29-v011-cozumleme.py` | `{COZ}` — ana betiği içe aktarır, yalnız hükmü değiştirir |", "",
         "## Okuma tablosu — sonuçtan ÖNCE", "", "| bekçi | baş ölçü | hüküm |", "|---|---|---|"]
    s += [f"| {r['bekci']} | {r['bas']} | {r['hukum']} |" for r in m["okuma_tablosu"]]
    s += ["", "## Güç — şart ulaşılabilir mi", "",
          "`e3`'ün kayıtlı 8 tohumundan; `v011`'in tohum dağılımı aynı varsayılırsa:", "",
          "| ölçü | `e3` ort | `e3` sd | en küçük okunabilir düşüş | `v011` için gerekli | veride |", "|---|---:|---:|---:|---:|---|",
          f"| B1 «sormuyorum» | %{g1['e3_ort']} | {g1['e3_sd']} | {g1['en_kucuk_okunabilir_dusus']} puan | < %{g1['v011_ort_gerekli']} | %30,6 → %3,1 |",
          f"| B2 ⛔/⭐ | %{g2['e3_ort']} | {g2['e3_sd']} | {g2['en_kucuk_okunabilir_dusus']} puan | < %{g2['v011_ort_gerekli']} | %22,8 → %0,2 |", "",
          f"⚠️ **Ön beklenti:** {m['on_beklenti']}", "",
          "## ⛔ Tam beyan", "", *[f"- {x}" for x in m["tam_beyan"]], "",
          "## ⛔ Bunun söylemedikleri", "", *[f"- {x}" for x in m["bunun_soylemedikleri"]]]
    RAPOR.write_text("\n".join(s) + "\n", encoding="utf-8")
    print(f"✅ EK-1 {MUHUR.relative_to(KOK)} · SHA256-16 {ms}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
